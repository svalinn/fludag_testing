Usage
==========
The testing script framework being composed entirely of bash scripts. To run,

      export FLUDAG=<path to DAGMC/FluDAG >
     ./run_test

run_tests quite simply runs the tests with the specified criteria contained within test_input. 

The tests
==========
There are currently 11 tests

      Test 1,2,3
      1) Slabs of vacuum 10 cubes 10 cm's in side stacked in the z direction
      2) 10 cubes 10 cm's in side stacked in the z direction, with the odd numbered cubes filled with iron
      3) 10 cubes 10 cm's in side stacked in the z direction, with the odd numbered cubes filled with water
      Test 11,12,13
      4) Spheres, 3 spherical shells of radii 10,20 and 30 cm, filled with vacuum
      5) Spheres, 3 spherical shells of radii 10,20 and 30 cm, filled with water
      6) Spheres, 3 spherical shells of radii 10,20 and 30 cm, filled with Be, Water and W respectively
      Test 21,22
      7) Cylinders, filled with vacuum and water, proton irradiation, USRTRACK 
     *8) Cylinders, filled with vacuum and water, proton irradiation, USRBIN
      Test 31
      9) Cylinders, filled with Al,HDPE and water, Fe ion irradiation at 1 GeV/u, USRTRACK
      Test 41,42
      10) Cylinder, vacuum, composed of many volumes subdivided by inclined planes, USRBDX
     *11) Sphere, composed of heavy water, 2d USRBDX neutron score 

We can further subdivide these tests into fast and slow tests, fast tests typically contain vacuum and can show that the code
is working well with respect to theory. The slow tests involve many repeted simulations in order to determine a good estimate
of the statistical error.

Fast Tests: 1,4,10
Slow Tests: 2,3,5,6,7,8,9,11

Adding more tests
==========
The format of test_input is very simple also;
 
      <test name> <test dir> <num_fluka> <fluka_input> <num_fludag> <fludag_inp> <fludag_h5m> <path_to_test_files> <success_criteria>

Adding more tests is very simple, simply add another unique line to test_input, running run_tests will complete and include their result.

Types of Test
==========
Currently there is a single test \

   *type "total" where the values of each tally in the problem are compared against one another and compared to the specified tolerance. 
   *type "spectrum" where the values of each bin the spectrum are compared against one another and compared to the specified tolerance.

To Do:
* I would like to also add "error" to the success criteria list, where the results are compared to with the computed statistical error