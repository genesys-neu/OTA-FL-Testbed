# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build

# Utility rule file for doxygen_target.

# Include the progress variables for this target.
include docs/doxygen/CMakeFiles/doxygen_target.dir/progress.make

docs/doxygen/CMakeFiles/doxygen_target: docs/doxygen/xml
docs/doxygen/CMakeFiles/doxygen_target: docs/doxygen/html


docs/doxygen/xml:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating documentation with doxygen"
	cd /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/docs/doxygen && /usr/bin/doxygen /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/docs/doxygen/Doxyfile

docs/doxygen/html: docs/doxygen/xml
	@$(CMAKE_COMMAND) -E touch_nocreate docs/doxygen/html

doxygen_target: docs/doxygen/CMakeFiles/doxygen_target
doxygen_target: docs/doxygen/xml
doxygen_target: docs/doxygen/html
doxygen_target: docs/doxygen/CMakeFiles/doxygen_target.dir/build.make

.PHONY : doxygen_target

# Rule to build all files generated by this target.
docs/doxygen/CMakeFiles/doxygen_target.dir/build: doxygen_target

.PHONY : docs/doxygen/CMakeFiles/doxygen_target.dir/build

docs/doxygen/CMakeFiles/doxygen_target.dir/clean:
	cd /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/docs/doxygen && $(CMAKE_COMMAND) -P CMakeFiles/doxygen_target.dir/cmake_clean.cmake
.PHONY : docs/doxygen/CMakeFiles/doxygen_target.dir/clean

docs/doxygen/CMakeFiles/doxygen_target.dir/depend:
	cd /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/docs/doxygen /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/docs/doxygen /home/genesys/Demo/Suyash_OTA_FL/gr-OTA_FL/build/docs/doxygen/CMakeFiles/doxygen_target.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : docs/doxygen/CMakeFiles/doxygen_target.dir/depend

