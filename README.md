Usage
==========
The testing script framework being composed entirely of bash scripts. To run,

     ./run_test

run_tests quite simply runs the tests with the specified criteria contained within test_input. 

Adding more tests
==========
The format of test_input is very simple also;
 
      <test name> <test dir> <num_fluka> <fluka_input> <num_fludag> <fludag_inp> <fludag_h5m> <path_to_test_files> <success_criteria>

Adding more tests is very simple, simply add another unique line to test_input, running run_tests will complete and include their result.

