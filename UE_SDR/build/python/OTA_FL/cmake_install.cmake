# Install script for directory: /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.8/dist-packages/gnuradio/OTA_FL" TYPE FILE FILES
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/__init__.py"
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/read_gold_seq.py"
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/addSubSelect.py"
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/dynamic_padder_py.py"
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/correlate_and_tag_py.py"
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/filter_payload_py.py"
    "/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/python/OTA_FL/Precoder.py"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/python/OTA_FL/bindings/cmake_install.cmake")

endif()

