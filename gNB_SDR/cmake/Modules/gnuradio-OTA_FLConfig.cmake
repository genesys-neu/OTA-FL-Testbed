find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_OTA_FL gnuradio-OTA_FL)

FIND_PATH(
    GR_OTA_FL_INCLUDE_DIRS
    NAMES gnuradio/OTA_FL/api.h
    HINTS $ENV{OTA_FL_DIR}/include
        ${PC_OTA_FL_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_OTA_FL_LIBRARIES
    NAMES gnuradio-OTA_FL
    HINTS $ENV{OTA_FL_DIR}/lib
        ${PC_OTA_FL_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-OTA_FLTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_OTA_FL DEFAULT_MSG GR_OTA_FL_LIBRARIES GR_OTA_FL_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_OTA_FL_LIBRARIES GR_OTA_FL_INCLUDE_DIRS)
