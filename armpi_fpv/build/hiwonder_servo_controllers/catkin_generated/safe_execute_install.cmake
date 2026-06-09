execute_process(COMMAND "/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_controllers/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/armpi/桌面/ros/armpi_fpv/build/hiwonder_servo_controllers/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
