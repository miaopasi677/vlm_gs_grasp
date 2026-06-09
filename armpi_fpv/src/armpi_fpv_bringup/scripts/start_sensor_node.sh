#!/bin/bash
source /opt/ros/melodic/setup.bash
source /home/ubuntu/armpi_fpv/devel/setup.bash
export ROS_HOSTNAME=ubuntu
export ROS_MASTER_URI=http://ubuntu:11311

roslaunch /home/ubuntu/armpi_fpv/src/armpi_fpv_bringup/launch/start_sensor.launch
