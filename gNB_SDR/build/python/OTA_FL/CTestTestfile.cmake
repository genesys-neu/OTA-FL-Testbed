# CMake generated Testfile for 
# Source directory: /home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL
# Build directory: /home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/build/python/OTA_FL
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(qa_read_gold_seq "/usr/bin/sh" "qa_read_gold_seq_test.sh")
set_tests_properties(qa_read_gold_seq PROPERTIES  _BACKTRACE_TRIPLES "/usr/local/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;45;GR_ADD_TEST;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;0;")
add_test(qa_correlate_and_tag_py "/usr/bin/sh" "qa_correlate_and_tag_py_test.sh")
set_tests_properties(qa_correlate_and_tag_py PROPERTIES  _BACKTRACE_TRIPLES "/usr/local/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;47;GR_ADD_TEST;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;0;")
add_test(qa_filter_payload_py "/usr/bin/sh" "qa_filter_payload_py_test.sh")
set_tests_properties(qa_filter_payload_py PROPERTIES  _BACKTRACE_TRIPLES "/usr/local/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;48;GR_ADD_TEST;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;0;")
add_test(qa_Precoder "/usr/bin/sh" "qa_Precoder_test.sh")
set_tests_properties(qa_Precoder PROPERTIES  _BACKTRACE_TRIPLES "/usr/local/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;49;GR_ADD_TEST;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;0;")
add_test(qa_Dynamic_Padder "/usr/bin/sh" "qa_Dynamic_Padder_test.sh")
set_tests_properties(qa_Dynamic_Padder PROPERTIES  _BACKTRACE_TRIPLES "/usr/local/lib/cmake/gnuradio/GrTest.cmake;119;add_test;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;50;GR_ADD_TEST;/home/ssp2943/Documents/gNB/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/CMakeLists.txt;0;")
subdirs("bindings")
