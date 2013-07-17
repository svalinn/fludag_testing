#!/bin/bash

# bash script to run a given test of FluDAG and 
# FLUKA. The script takes as arguments
# TestName  $1 the name of the test dir for this test 
# NumFluka  $2 the number of fluka runs
# NameFluka $3 the name of the fluka input deck
# NumDAG    $4 the number of fludag runs
# NameDag   $5 the name of the fludag input
# NameDagh5m   $6 the name of the dag cad file
# PathToData $7 is the path to the input data

TestName=$1

if [ -d $TestName ] ; then
    echo "!! ERROR !!"
    echo "Directory "$TestName" exists."
    exit
fi

NumFluka=$2 #number of fluka inputs
NameFluka=$3 #name of the fluka input
NumDag=$4 #number of dag runs
NameDag=$5 # name of the dag file
NameDagh5m=$6 #name of the h5m file
InputData=$7 # location of the input data
Test=$8 # type of test
Tol=$9 # tolerance of the test

# check for fluka file
if [ ! -f $InputData/fluka/$NameFluka ] ; then
    echo "!! ERROR !!"
    echo "Fluka input "$NameFluka" does not exist"
    exit
fi

# check for dag files
if [ ! -f $InputData/fludag/$NameDag ] ; then
    echo "!! ERROR !!"
    echo "Fludag input "$NameDag" does not exist"
    exit
fi

if [ ! -f $InputData/fludag/$NameDagh5m ] ; then
    echo "!! ERROR !!"
    echo "Fludag input "$NameDagh5m" does not exist"
    exit
fi


# copy fluka input
mkdir -p $TestName/fluka
cp $InputData/fluka/$NameFluka $TestName/fluka/.

# copy fludag input
mkdir -p $TestName/fludag
cp $InputData/fludag/$NameDag $TestName/fludag/.
cp $InputData/fludag/$NameDagh5m $TestName/fludag/.

name_stub=`echo $NameFluka | sed -e s'/\./ /'g | awk '{print $1}'`

# run the fluka input
cd $TestName/fluka
$FLUPRO/flutil/rfluka -N0 -M$NumFluka $NameFluka > /dev/null
# process the data
`{
    for (( i = 1 ; i <= $NumFluka ; i++ )) do
     echo $name_stub"00"$i"_fort.21"
    done
    echo " "
    echo $name_stub
  } | $FLUPRO/flutil/ustsuw > /dev/null`

# convert to ascii
`{
    echo $name_stub
 } | $FLUPRO/flutil/usbrea &> /dev/null` 
cd ..

# run the fludag problem
cd fludag
$FLUPRO/flutil/rfluka -N0 -M$NumDag -e $FLUDAG/bld/mainfludag -d $NameDagh5m $NameDag > /dev/null
# process the data
`{
    for (( i = 1 ; i <= $NumFluka ; i++ )) do
     echo $name_stub"00"$i"_fort.21"
    done
    echo " "
    echo $name_stub
  } | $FLUPRO/flutil/ustsuw > /dev/null`
# convert to ascii
`{
    echo $name_stub
 } | $FLUPRO/flutil/usbrea  &> /dev/null`
cd ..
 
# determine pass or fail
if [ $Test == "total" ] ; then
  num_diff=`diff fluka/$name_stub"_sum.lis" fludag/$name_stub"_sum.lis" | wc -l | awk '{print $1}'`
  if [ $num_diff -eq 0 ] ; then
      echo "Test passed"
      exit
  else 
      # need to check with tolerance
      grep 'Tot. response' fluka/$name_stub"_sum.lis" > fluka_res
      grep 'Tot. response' fludag/$name_stub"_sum.lis" > fludag_res
      
      num_scores_fluka=`grep -c "Tot. response" fluka/$name_stub"_sum.lis"`
      num_scores_fludag=`grep -c "Tot. response" fludag/$name_stub"_sum.lis"`
      
      if [ $num_scores_fluka -ne $num_scores_fludag ] ; then
	  echo "!! ERROR !! "
	  echo "Number of scorers in the fluka and fludag files do not match"
	  exit
      fi

      for (( j = 1 ; j <= $num_scores_fluka ; j++)) do
         fluka_val=`sed -n "$j"p fluka_res | awk '{print $4}'`
	 fludag_val=`sed -n "$j"p fludag_res | awk '{print $4}'`
	 diff=`{
                echo "$fluka_val-$fludag_val"
		} | bc`
         diffsq=`{
                  echo "sqrt($diff*$diff)"
		  } | bc -l`

	 if [[ $(echo "if (${diffsq} > ${Tol}) 1 else 0" | bc) -eq 1 ]]; then
	     echo "Scores differ by more than tolerance"
	     echo "!! Test FAILED !!"
	     exit
	 else
	     # we're ok
	     continue
	 fi

      done
      # if we are here then test pased
      echo "Test Passed"
      exit
  fi
  
elif [ $Test == "spectrum" ] ; then

    if ! grep -q 'N. of energy intervals' fluka/$name_stub"_tab.lis"; then
	echo "The fluka file does not contain energy intervals" 
	exit
    else
	nbins=`grep 'N. of energy intervals' fluka/$name_stub"_tab.lis" | awk '{print $6}' | sed -n 1p`
    fi

    if ! grep -q 'N. of energy intervals' fludag/$name_stub"_tab.lis"; then
	echo "The fludagfile does not contain energy intervals" 
	exit
    else
	nbins_fludag=`grep 'N. of energy intervals' fluka/$name_stub"_tab.lis" | awk '{print $6}' | sed -n 1p`
    fi

    if [ $nbins -ne $nbins_fludag ] ; then
	echo "The number of energy bins in the detectors do not match"
	exit
    fi

    # if we are here then everything is ok
    for (( i = 3 ; i <= `expr $nbins + 3` ; i++ )) ; do
	fluka_val=`sed -n "$i"p fluka/$name_stub"_tab.lis" | awk '{print $3}'`
	fludag_val=`sed -n "$i"p fludag/$name_stub"_tab.lis" | awk '{print $3}'`

	diff=`{
              echo "$fluka_val-$fludag_val"
	      } | bc`
        diffsq=`{
                echo "sqrt($diff*$diff)"
	        } | bc -l`

	 if [[ $(echo "if (${diffsq} > ${Tol}) 1 else 0" | bc) -eq 1 ]]; then
	     echo "Scores differ by more than tolerance"
	     echo "Difference = " $diff
	     echo "Magnitude = " $diffsq
	     echo "!! Test FAILED !!"
	     exit
	 else
	     # we're ok
	     continue
	 fi

    done
    # if here test passed

fi

