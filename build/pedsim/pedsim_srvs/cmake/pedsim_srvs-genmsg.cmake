# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "pedsim_srvs: 0 messages, 4 services")

set(MSG_I_FLAGS "-Ipedsim_msgs:/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/melodic/share/sensor_msgs/cmake/../msg;-Inav_msgs:/opt/ros/melodic/share/nav_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(pedsim_srvs_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" NAME_WE)
add_custom_target(_pedsim_srvs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pedsim_srvs" "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" "pedsim_msgs/AgentState:pedsim_msgs/AgentForce:geometry_msgs/Twist:geometry_msgs/Vector3:geometry_msgs/Pose:std_msgs/Header:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" NAME_WE)
add_custom_target(_pedsim_srvs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pedsim_srvs" "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" "pedsim_msgs/AgentState:pedsim_msgs/AgentForce:geometry_msgs/Twist:geometry_msgs/Vector3:geometry_msgs/Pose:pedsim_msgs/AgentStates:std_msgs/Header:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" NAME_WE)
add_custom_target(_pedsim_srvs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pedsim_srvs" "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" "pedsim_msgs/AgentState:pedsim_msgs/AgentForce:geometry_msgs/Twist:geometry_msgs/Vector3:geometry_msgs/Pose:std_msgs/Header:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" NAME_WE)
add_custom_target(_pedsim_srvs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "pedsim_srvs" "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" "pedsim_msgs/AgentState:pedsim_msgs/AgentForce:geometry_msgs/Twist:geometry_msgs/Vector3:geometry_msgs/Pose:pedsim_msgs/AgentStates:std_msgs/Header:geometry_msgs/Quaternion:geometry_msgs/Point"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_cpp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_cpp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_cpp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs
)

### Generating Module File
_generate_module_cpp(pedsim_srvs
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(pedsim_srvs_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(pedsim_srvs_generate_messages pedsim_srvs_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_cpp _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_cpp _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_cpp _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_cpp _pedsim_srvs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pedsim_srvs_gencpp)
add_dependencies(pedsim_srvs_gencpp pedsim_srvs_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pedsim_srvs_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services
_generate_srv_eus(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_eus(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_eus(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_eus(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs
)

### Generating Module File
_generate_module_eus(pedsim_srvs
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(pedsim_srvs_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(pedsim_srvs_generate_messages pedsim_srvs_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_eus _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_eus _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_eus _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_eus _pedsim_srvs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pedsim_srvs_geneus)
add_dependencies(pedsim_srvs_geneus pedsim_srvs_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pedsim_srvs_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_lisp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_lisp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_lisp(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs
)

### Generating Module File
_generate_module_lisp(pedsim_srvs
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(pedsim_srvs_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(pedsim_srvs_generate_messages pedsim_srvs_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_lisp _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_lisp _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_lisp _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_lisp _pedsim_srvs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pedsim_srvs_genlisp)
add_dependencies(pedsim_srvs_genlisp pedsim_srvs_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pedsim_srvs_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages

### Generating Services
_generate_srv_nodejs(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_nodejs(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_nodejs(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_nodejs(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs
)

### Generating Module File
_generate_module_nodejs(pedsim_srvs
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(pedsim_srvs_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(pedsim_srvs_generate_messages pedsim_srvs_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_nodejs _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_nodejs _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_nodejs _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_nodejs _pedsim_srvs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pedsim_srvs_gennodejs)
add_dependencies(pedsim_srvs_gennodejs pedsim_srvs_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pedsim_srvs_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_py(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_py(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs
)
_generate_srv_py(pedsim_srvs
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv"
  "${MSG_I_FLAGS}"
  "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg;/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Twist.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs
)

### Generating Module File
_generate_module_py(pedsim_srvs
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(pedsim_srvs_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(pedsim_srvs_generate_messages pedsim_srvs_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_py _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_py _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/SetAgentState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_py _pedsim_srvs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_srvs/srv/GetAllAgentsState.srv" NAME_WE)
add_dependencies(pedsim_srvs_generate_messages_py _pedsim_srvs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(pedsim_srvs_genpy)
add_dependencies(pedsim_srvs_genpy pedsim_srvs_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS pedsim_srvs_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/pedsim_srvs
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET pedsim_msgs_generate_messages_cpp)
  add_dependencies(pedsim_srvs_generate_messages_cpp pedsim_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(pedsim_srvs_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/pedsim_srvs
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET pedsim_msgs_generate_messages_eus)
  add_dependencies(pedsim_srvs_generate_messages_eus pedsim_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(pedsim_srvs_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/pedsim_srvs
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET pedsim_msgs_generate_messages_lisp)
  add_dependencies(pedsim_srvs_generate_messages_lisp pedsim_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(pedsim_srvs_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/pedsim_srvs
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET pedsim_msgs_generate_messages_nodejs)
  add_dependencies(pedsim_srvs_generate_messages_nodejs pedsim_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(pedsim_srvs_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/pedsim_srvs
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET pedsim_msgs_generate_messages_py)
  add_dependencies(pedsim_srvs_generate_messages_py pedsim_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(pedsim_srvs_generate_messages_py std_msgs_generate_messages_py)
endif()
