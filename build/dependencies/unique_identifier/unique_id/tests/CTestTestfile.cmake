# CMake generated Testfile for 
# Source directory: /home/ubuntu/ws/jackal_fyp/src/dependencies/unique_identifier/unique_id/tests
# Build directory: /home/ubuntu/ws/jackal_fyp/build/dependencies/unique_identifier/unique_id/tests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_unique_id_gtest_test_unique_id "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/ws/jackal_fyp/build/test_results/unique_id/gtest-test_unique_id.xml" "--return-code" "/home/ubuntu/ws/jackal_fyp/devel/lib/unique_id/test_unique_id --gtest_output=xml:/home/ubuntu/ws/jackal_fyp/build/test_results/unique_id/gtest-test_unique_id.xml")
add_test(_ctest_unique_id_nosetests_test_unique_id.py "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/ubuntu/ws/jackal_fyp/build/test_results/unique_id/nosetests-test_unique_id.py.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /home/ubuntu/ws/jackal_fyp/build/test_results/unique_id" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/ubuntu/ws/jackal_fyp/src/dependencies/unique_identifier/unique_id/tests/test_unique_id.py --with-xunit --xunit-file=/home/ubuntu/ws/jackal_fyp/build/test_results/unique_id/nosetests-test_unique_id.py.xml")
