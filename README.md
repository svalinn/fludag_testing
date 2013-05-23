Usage
==========
The testing script framework being composed entirely of bash scripts. To run,

      export FLUDAG=<path to DAGMC/FluDAG >
     ./run_test

run_tests quite simply runs the tests with the specified criteria contained within test_input. 

The tests
==========
There are currently 6 tests

      1) Slabs of vacuum 10 cubes 10 cm's in side stacked in the z direction
      2) 10 cubes 10 cm's in side stacked in the z direction, with the odd numbered cubes filled with iron
      3) 10 cubes 10 cm's in side stacked in the z direction, with the odd numbered cubes filled with water
      4) Spheres, 3 spherical shells of radii 10,20 and 30 cm, filled with vacuum
      5) Spheres, 3 spherical shells of radii 10,20 and 30 cm, filled with water
      6) Spheres, 3 spherical shells of radii 10,20 and 30 cm, filled with Be, Water and W respectively


Adding more tests
==========
The format of test_input is very simple also;
 
      <test name> <test dir> <num_fluka> <fluka_input> <num_fludag> <fludag_inp> <fludag_h5m> <path_to_test_files> <success_criteria>

Adding more tests is very simple, simply add another unique line to test_input, running run_tests will complete and include their result.

Types of Test
==========
Currently there is a single test type "total" where the values of each tally in the problem are compared against one another and compared to
the specified tolerance. 

To Do:
* I would like to add to this at least the "spectra" test where each bin of each tally must match to within the specified tolerance.
* I would like to also add "error" to the success criteria list, where the results are compared to with the computed statistical error