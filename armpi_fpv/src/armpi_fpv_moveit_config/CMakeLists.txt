cmake_minimum_required(VERSION 3.1.3)
project(armpi_fpv_moveit_config)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(PROGRAMS
  scripts/fake_point_cloud.py
  scripts/pointcloud_grasp.py
  scripts/gs_grasp_sim.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
