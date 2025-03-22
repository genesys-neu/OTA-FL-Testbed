#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL
export GR_CONF_CONTROLPORT_ON=False
export PATH="/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/python/OTA_FL":"$PATH"
export LD_LIBRARY_PATH="":$LD_LIBRARY_PATH
export PYTHONPATH=/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/test_modules:$PYTHONPATH
/usr/bin/python3 /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/qa_correlate_and_tag_py.py 
