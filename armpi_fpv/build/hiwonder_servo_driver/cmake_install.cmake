# Install script for directory: /home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/armpi/桌面/ros/armpi_fpv/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
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
  include("/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_driver/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_driver/catkin_generated/installspace/hiwonder_servo_driver.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hiwonder_servo_driver/cmake" TYPE FILE FILES
    "/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_driver/catkin_generated/installspace/hiwonder_servo_driverConfig.cmake"
    "/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_driver/catkin_generated/installspace/hiwonder_servo_driverConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hiwonder_servo_driver" TYPE FILE FILES "/home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/hiwonder_servo_driver" TYPE PROGRAM FILES
    "/home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_const.py"
    "/home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py"
    "/home/armpi/桌面/ros/armpi_fpv/src/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py"
    )
endif()

