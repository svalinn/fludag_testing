#!/usr/bin/python
import sys
import os
import shutil
import math
import subprocess 
import re

# to make a dir
def mkdir_p(path):
    try:
        os.makedirs(path)
    except:
        print "Could not create, it already exists!"
        exit()
    return

# write the file to process data
def write_process_file(TestName,NumFluka):

    test_name = TestName
    name = test_name.split('.')
    file = open("process", 'w')
    # write command file to process data
    for i in range(1,NumFluka+1):
        
        string = name[0]+'00'+str(i)+'_fort.21\n'
        file.write(string)

    file.write('\r\n')
    file.write(name[0]+'\n')
    file.close()
    return 

# get the spectra from a given detctro file
def get_spec(egrps,filename):
    flux=[]

    error=[]

    det_num=0
    try:
        file = open(filename, 'r')
    except:
        print "Could not open the results file!"
        exit()

    while 1:
        line = file.readline()
        if not line:
            break
        if ' # N. of energy intervals' in line:
            det_num=det_num+1
            flux.append([])
            error.append([])
            for i in range (0,egrps):
                data=file.readline()
                count=0
                for token in data.split():
                    count=count+1
                    if count == 3:
                        flux[det_num-1].append(float(token))
                    if count == 4:
                        error[det_num-1].append(float(token))

    file.close()
    return flux,error

# function to get material assignments
def get_fluka_mat_assign(filename):

    reg_num=[]
    mat_name=[]

    try:
        file = open(filename, 'r')
    except:
        print "Could not open the fluka output file"
        print "Filename = ", filename
        exit()

    while 1:
        line = file.readline()
        if not line:
            break
        # look for regions line
        if '=== Regions:' in line:
            # read 4 lines
            for i in range(0,4):
                line = file.readline()
            line = file.readline()
            while len(line.split()) != 0:
                # if there are 7 tokens then we have a mat line
                if len(line.split()) == 7:
                    count=0
                    for token in line.split():
                        count=count+1
                        if count == 2:
                            reg_num.append(int(token))
                        elif count == 4:
                            mat_name.append(token)
                            line = file.readline()
                            break
                elif len(line.split()) == 5:
                    line = file.readline()                    
                else:
                    return reg_num,mat_name
            
    return reg_num,mat_name

#function to get the materiual ass
def get_mat_data(filename):
    
    mats=[]

    try:
        file = open(filename, 'r')
    except:
        print "Could not open the fluka input file"
        print "Filename = ", filename
        exit()

    while 1:
        line = file.readline()
        if not line:
            break
        if 'MATERIAL' in line:
            mats.append(line)

    file.close()

    return mats

# get the assign keywrods from file
def get_assign_data(filename):

    assignment=[]

    try:
        file = open(filename, 'r')
    except:
        print "Could not open the fluka input file"
        print "Filename = ", filename
        exit()

    while 1:
        line = file.readline()
        if not line:
            break
        if 'ASSIGNMA' in line:
            assignment.append(line)

    file.close()

    return assignment

# count the number of energy bins in each detector
def count_e_bins(file_check):
    
    nbins=0
    bins=[]

    try:
        file = open(file_check, 'r')
    except:
        print "Could not open the results file!"
        print "Filename = ", file_check
        exit()

    while 1:
        line = file.readline()
        if not line:
            break
        # look for the nunber of bins
        if ' # N. of energy intervals' in line:
            nbins=nbins+1
            for token in line.split():
                try:
                    # get the number of bins
                    if int(token):
                        bins.append(int(token))
                except:
                    continue
    file.close()
    return nbins,bins

    
# get the data from file looking for total response  
def get_total_response(fluka_data):
    # open the data file
    num_scores = 0
    score_data=[]
    score_error=[]
    try:
        file = open(fluka_data, 'r')
    except:
        print "Could not open the results file!"
        print "Filename = ", fluka_data
        exit()
    
    # while reading
    while 1:
        line = file.readline()
        if not line:
            break
        # if we find tot resp
        if 'Tot. resp' in line:
            num_scores=num_scores+1
            counter=0
            # get he results
            for token in line.split():
                try:
                    if float(token):
                        counter = counter+1
                        if counter == 1:
                            score_data.append(float(token))
                        else:
                            score_error.append(float(token))
                except:
                    continue
            else:
                continue

    file.close()
    return score_data,score_error


#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

# setup the input variables

TestName = str(sys.argv[1])
if os.path.exists(TestName):
    print "!! ERROR !!"
    print "Directory "+TestName+" Already exists"
    exit()
TestDir = str(sys.argv[2])
NumFluka=int(sys.argv[3])
NameFluka=str(sys.argv[4])
NumDag=int(sys.argv[5])
NameDag=str(sys.argv[6])
NameDagh5m=str(sys.argv[7])
InputData=str(sys.argv[8])
TestType=str(sys.argv[9])
Test = str(sys.argv[10])

try:
    float(sys.argv[11])
except:
    Tol = sys.argv[11]
else:
    Tol = float(sys.argv[11])


if not "FLUDAG" in os.environ:
    print "!! ERROR !!"
    print "FLUDAG shell variable not set"
    exit()

# get the fludag path
fludag_path = os.getenv('FLUDAG')

# check to ensure fludag exists
if not os.path.isfile(fludag_path+'/mainfludag'):
    print "!! ERROR !!"
    print "Could not get fludag executable"
    print "I looked for it in "+fludag_path+'/mainfludag'
    exit()


# check to make sure fluka file exists
if not os.path.isfile(InputData+'/fluka/'+NameFluka):
    print "!! ERROR !!"
    print "Fluka input "+NameFluka+" does not exist"
    exit()

# check for fludag files
if not os.path.isfile(InputData+'/fludag/'+NameDag):
    print "!! ERROR !!"
    print "Fluka input "+NameDag+" does not exist"
    exit()

if not os.path.isfile(InputData+'/fludag/'+NameDagh5m):
    print "!! ERROR !!"
    print "Fluka input "+NameDagh5m+" does not exist"
    exit()

# copy the input to the test location
mkdir_p(TestDir+'/fluka')
shutil.copy(InputData+'/fluka/'+NameFluka,TestDir+'/fluka/'+NameFluka)
# copy fludag input data
mkdir_p(TestDir+'/fludag')
shutil.copy(InputData+'/fludag/'+NameDag,TestDir+'/fludag/'+NameDag)
shutil.copy(InputData+'/fludag/'+NameDagh5m,TestDir+'/fludag/'+NameDagh5m)

# run the fluka file
os.chdir(TestDir+'/fluka')
if "code" not in TestType:
    os.system('$FLUPRO/flutil/rfluka -N0 -M'+str(NumFluka)+' '+NameFluka+' > /dev/null')

if "usrtrack" in TestType:
# its a usrtrack tally
    write_process_file(NameFluka,NumFluka)
    os.system('$FLUPRO/flutil/ustsuw < process > /dev/null')
elif "usrbdx" in TestType:

    write_process_file(NameFluka,NumFluka)
    os.system('$FLUPRO/flutil/usxsuw < process > /dev/null')
elif "code" in TestType:
    pass
else:
    print "!! ERROR Unknown test"
    exit()

# one below fluka and fludag

#print os.getcwd()
os.chdir('..')
os.chdir('fludag')

# run the fludag problem
if "code" not in TestType:
    os.system('$FLUPRO/flutil/rfluka -N0 -M'+str(NumDag)+' -e '+fludag_path+'/mainfludag'+' -d '+NameDagh5m+' '+NameDag+' > /dev/null')
else:
    # generate the mat.inp
    os.system(fludag_path+'bld/mainfludag '+NameDagh5m+' > /dev/null')


# process the fludag output
if "usrtrack" in TestType:
# its a usrtrack tally
    write_process_file(NameDag,NumDag)
    os.system('$FLUPRO/flutil/ustsuw < process > /dev/null')
elif "usrbdx" in TestType:
    write_process_file(NameDag,NumDag)
    os.system('$FLUPRO/flutil/usxsuw < process > /dev/null')
elif "code" in TestType:
    pass
else:
    print "!! ERROR Unknown test"
    exit()

os.chdir('..')
# perform comparison
if 'total' in Test:
    test_name = TestName
    name = test_name.split('.')
    diff = subprocess.Popen(["diff","-c","fluka/"+name[0]+"_sum.lis","fludag/"+name[0]+"_sum.lis"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
    if not diff:
        print "Test passed"
    else:
        # generate the data to test
        (fluka_data,fluka_error)=get_total_response('fluka/'+name[0]+'_sum.lis')
        (fludag_data,fludag_error)=get_total_response('fludag/'+name[0]+'_sum.lis')

        if len(fluka_data) == 0:
            print " !! ERROR !!"
            print " we have a problem the numebr of detectors is 0"
            exit()
                
        if len(fluka_data) != len(fludag_data):
            print "!! ERROR The number of scorers in each file do not match !!"
            print "There are ",len(fluka_data), " Fluka scorers"
            print "There are ",len(fludag_data)," Fludag scorers"
            exit()

        if '.' in str(Tol): # then its a number, check with tolerance
            for i in range (0,len(fluka_data)):
                if ( (math.fabs(fluka_data[i]-fludag_data[i]))/fluka_data[i] > Tol ):
                    print "Scores differ by more than tolerance"
                    print "!! Test failed !!"
                    exit()
                else:
                    continue

            print "Test Passed"
            exit()
        elif 'sig' in str(Tol): # then its a word

            if( NumFluka < 2 ): # make sure enough runs to get error estimate
                print " !! ERROR !! "
                print "To use standard deviation as tolerance more than 1 run"
                print "must be used"
                exit()


            n = int(''.join(x for x in Tol if x.isdigit()))
            for i in range(0,len(fluka_data)):             
                std_dev = math.sqrt(fluka_error[i]**2+fludag_error[i]**2)
                if ( (fludag_data[i]/fluka_data[i] >= 1.+(float(n)*std_dev)) and \
                   ((fludag_data[i]/fluka_data[i] <= 1.-(float(n)*std_dev)))):
                    print "Scores differ by more than ", str(n),"times the standard deviation"
                    print fludag_data[i]/fluka_data[i],' +/- ', (float(n)*std_dev)
                    print "!! Test failed !!"
                    exit()
                else:
                    continue

            print "Test Passed"
            exit()           


elif 'spectrum' in Test:

    # everything ok
    test_name = TestName
    name = test_name.split('.')

    # ensure the number of energy intervals is correct
    (num_tal_fluka,num_grp_fluka)=count_e_bins('fluka/'+name[0]+'_tab.lis')
    (num_tal_fludag,num_grp_fludag)=count_e_bins('fludag/'+name[0]+'_tab.lis')
    
    if num_tal_fluka != num_tal_fludag:
        print " !! ERROR There not the same number of detectors in each problem !!" 
        print "There are ", num_tal_fluka, " Detectors in the fluka problem"
        print "There are ", num_tal_fludag, " Detectors in thef fludag problem"
        exit()

    if num_tal_fluka == 0:
        print " !! ERROR !!"
        print " we have a problem the numebr of detectors is 0"
        exit()

    for egrp in range(0,num_tal_fluka):
        if num_grp_fluka[egrp] != num_grp_fludag[egrp]:
            print "!! ERROR There not the same number of detectors in each problem !!" 
            print "In the ", egrp+1,"th deterctor of fluka or fludag"
            exit()

    (fluka_spec,fluka_error) = get_spec(num_grp_fluka[0],'fluka/'+name[0]+'_tab.lis')
    (fludag_spec,fludag_error) = get_spec(num_grp_fludag[0],'fludag/'+name[0]+'_tab.lis')

    for det in range(0,num_tal_fluka):
        for grp in range(0,num_grp_fluka[0]):
            if '.' in str(Tol): # then its a number, check with tolerance              
                if fluka_spec[det][grp] > 0.0:
                    if (math.fabs(fluka_spec[det][grp]-fludag_spec[det][grp])/fluka_spec[det][grp]) \
                            > Tol:
                        print "Test failed "
                        print "In detector, ",det+1 
                        print fluka_spec[det][grp],fludag_spec[det][grp]
                        print "Difference in flux in Egrp ",grp+1," of scorers is greater than tol"
                        print "Diff = ",(math.fabs(fluka_spec[det][grp]-fludag_spec[det][grp])/fluka_spec[det][grp]), " tol = ", Tol
                        exit()
                else:
                    if (math.fabs(fluka_spec[det][grp]-fludag_spec[det][grp])) > Tol:
                        print "Test failed "
                        print "In detector, ",det+1 
                        print fluka_spec[det][grp],fludag_spec[det][grp]
                        print "Difference in flux in Egrp ",grp+1," of scorers is greater than tol"
                        print "Diff = ",  math.fabs(fluka_spec[det][grp]-fludag_spec[det][grp]), " tol = ", Tol
                        exit()
            elif 'sig' in str(Tol): # then its a word use error estimate
                n = int(''.join(x for x in Tol if x.isdigit()))
                if( NumFluka < 2 ): # make sure enough runs to get error estimate
                    print " !! ERROR !! "
                    print "To use standard deviation as tolerance more than 1 run"
                    print "must be used"
                    exit()
    
                if fluka_spec[det][grp] > 0.0:
                    # if the flux is greater than zero
                    std_dev = math.sqrt(fluka_error[det][grp]**2 + fludag_error[det][grp]**2)
                    flk_fld = fluka_spec[det][grp]/fludag_spec[det][grp]
                    if ( (flk_fld >= 1.+(float(n)*std_dev)) and \
                             ((flk_fld <= 1.-(float(n)*std_dev)))):
                        print "Difference greater than ", str(n),"times the standard deviation"
                        print "!! Test failed !!"
                        print fluka_spec[det][grp],fludag_spec[det][grp], \
                            fluka_error[det][grp],fludag_error[det][grp]
                        exit()        

    print "Test passed"                  
    exit()

elif 'material' in Test.strip():
    
    assignment_fluka=get_assign_data('fluka/'+NameFluka)
    assignment_fludag=get_assign_data('fludag/mat.inp')
    for i in range(0,len(assignment_fluka)):
        if assignment_fludag[i] not in assignment_fluka[i]:
            print "Test Failed"
            print "Material assignments are not equal"
            print "Fluka = ", assignment_fluka[i]
            print "FluDAG = ", assignment_fludag[i]
            exit()
            
    print "Test passed"
    exit()        


elif 'compound' in Test.strip():
    # check that the mat.inp file has the correct bindings
    
    mats_fluka=get_mat_data('fluka/'+NameFluka)    
    mats_fludag=get_mat_data('fludag/mat.inp')

    assignment_fluka=get_assign_data('fluka/'+NameFluka)
    assignment_fludag=get_assign_data('fludag/mat.inp')


    for i in range(0,len(mats_fluka)):
        for token in mats_fludag[i]:
            if token not in mats_fluka[i]:
                print "Test Failed" 
                print "Material tags are not the same"
                print "Fluka = ", mats_fluka[i]
                print "Fludag = ", mats_fludag[i]
                exit()


    for i in range(0,len(mats_fluka)):
        if assignment_fludag[i] not in assignment_fluka[i]:
            print "Test Failed"
            print "Material assignments are not equal"
            print "Fluka = ", assignment_fluka[i]
            print "FluDAG = ", assignment_fludag[i]
            exit()
            
    print "Test passed"
    exit()        

else:
    print "TestType = ",TestType
    print "Test = ", Test
    print "!! ERROR !!"
    print "Unknown type of test"
    exit()


exit()
