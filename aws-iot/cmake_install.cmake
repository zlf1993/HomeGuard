# Install script for directory: /opt/intel/openvino/deployment_tools/inference_engine/samples

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

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/pi/Documents/aws-iot/thirdparty/gflags/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/common/format_reader/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/benchmark_app/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/classification_sample_async/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/hello_classification/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/hello_nv12_input_classification/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/hello_query_device/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/hello_reshape_ssd/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/object_detection_sample_ssd/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/speech_sample/cmake_install.cmake")
  include("/home/pi/Documents/aws-iot/style_transfer_sample/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/pi/Documents/aws-iot/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
