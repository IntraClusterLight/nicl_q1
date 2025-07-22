#! /bin/bash

# Submit all jobs for all tests in parallel

submit_measure_test.sh basic_test
submit_measure_test.sh basic_test no_noise
submit_measure_test.sh varying_background
submit_measure_test.sh real_background
