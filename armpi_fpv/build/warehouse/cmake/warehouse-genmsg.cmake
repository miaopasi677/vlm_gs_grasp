# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "warehouse: 3 messages, 3 services")

set(MSG_I_FLAGS "-Iwarehouse:/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(warehouse_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" NAME_WE)
add_custom_target(_warehouse_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "warehouse" "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" ""
)

get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" NAME_WE)
add_custom_target(_warehouse_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "warehouse" "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" "geometry_msgs/Point:warehouse/Rotate"
)

get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" NAME_WE)
add_custom_target(_warehouse_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "warehouse" "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" "geometry_msgs/Point:geometry_msgs/Vector3:warehouse/Rotate:warehouse/Pose"
)

get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" NAME_WE)
add_custom_target(_warehouse_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "warehouse" "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" ""
)

get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" NAME_WE)
add_custom_target(_warehouse_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "warehouse" "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" ""
)

get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" NAME_WE)
add_custom_target(_warehouse_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "warehouse" "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
)
_generate_msg_cpp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
)
_generate_msg_cpp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
)

### Generating Services
_generate_srv_cpp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
)
_generate_srv_cpp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
)
_generate_srv_cpp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
)

### Generating Module File
_generate_module_cpp(warehouse
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(warehouse_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(warehouse_generate_messages warehouse_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_cpp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_cpp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_cpp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_cpp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_cpp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_cpp _warehouse_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(warehouse_gencpp)
add_dependencies(warehouse_gencpp warehouse_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS warehouse_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
)
_generate_msg_eus(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
)
_generate_msg_eus(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
)

### Generating Services
_generate_srv_eus(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
)
_generate_srv_eus(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
)
_generate_srv_eus(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
)

### Generating Module File
_generate_module_eus(warehouse
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(warehouse_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(warehouse_generate_messages warehouse_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_eus _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_eus _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_eus _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_eus _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_eus _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_eus _warehouse_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(warehouse_geneus)
add_dependencies(warehouse_geneus warehouse_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS warehouse_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
)
_generate_msg_lisp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
)
_generate_msg_lisp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
)

### Generating Services
_generate_srv_lisp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
)
_generate_srv_lisp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
)
_generate_srv_lisp(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
)

### Generating Module File
_generate_module_lisp(warehouse
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(warehouse_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(warehouse_generate_messages warehouse_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_lisp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_lisp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_lisp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_lisp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_lisp _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_lisp _warehouse_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(warehouse_genlisp)
add_dependencies(warehouse_genlisp warehouse_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS warehouse_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
)
_generate_msg_nodejs(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
)
_generate_msg_nodejs(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
)

### Generating Services
_generate_srv_nodejs(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
)
_generate_srv_nodejs(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
)
_generate_srv_nodejs(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
)

### Generating Module File
_generate_module_nodejs(warehouse
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(warehouse_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(warehouse_generate_messages warehouse_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_nodejs _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_nodejs _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_nodejs _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_nodejs _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_nodejs _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_nodejs _warehouse_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(warehouse_gennodejs)
add_dependencies(warehouse_gennodejs warehouse_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS warehouse_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
)
_generate_msg_py(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
)
_generate_msg_py(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Point.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg;/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
)

### Generating Services
_generate_srv_py(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
)
_generate_srv_py(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
)
_generate_srv_py(warehouse
  "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
)

### Generating Module File
_generate_module_py(warehouse
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(warehouse_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(warehouse_generate_messages warehouse_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Rotate.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_py _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Pose.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_py _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/msg/Grasp.msg" NAME_WE)
add_dependencies(warehouse_generate_messages_py _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetInTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_py _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetOutTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_py _warehouse_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/armpi/桌面/ros/armpi_fpv/src/warehouse/srv/SetExchangeTarget.srv" NAME_WE)
add_dependencies(warehouse_generate_messages_py _warehouse_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(warehouse_genpy)
add_dependencies(warehouse_genpy warehouse_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS warehouse_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/warehouse
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(warehouse_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET std_srvs_generate_messages_cpp)
  add_dependencies(warehouse_generate_messages_cpp std_srvs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(warehouse_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/warehouse
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(warehouse_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET std_srvs_generate_messages_eus)
  add_dependencies(warehouse_generate_messages_eus std_srvs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(warehouse_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/warehouse
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(warehouse_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET std_srvs_generate_messages_lisp)
  add_dependencies(warehouse_generate_messages_lisp std_srvs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(warehouse_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/warehouse
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(warehouse_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET std_srvs_generate_messages_nodejs)
  add_dependencies(warehouse_generate_messages_nodejs std_srvs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(warehouse_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/warehouse
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(warehouse_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET std_srvs_generate_messages_py)
  add_dependencies(warehouse_generate_messages_py std_srvs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(warehouse_generate_messages_py geometry_msgs_generate_messages_py)
endif()
