# CMake generated Testfile for 
# Source directory: /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL
# Build directory: /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/python/OTA_FL
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(qa_read_gold_seq "/bin/sh" "qa_read_gold_seq_test.sh")
add_test(qa_correlate_and_tag_py "/bin/sh" "qa_correlate_and_tag_py_test.sh")
add_test(qa_filter_payload_py "/bin/sh" "qa_filter_payload_py_test.sh")
add_test(qa_Precoder "/bin/sh" "qa_Precoder_test.sh")
add_test(qa_Dynamic_Padder "/bin/sh" "qa_Dynamic_Padder_test.sh")
subdirs("bindings")
