# Install script for directory: /home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/ubuntu/ws/jackal_fyp/install")
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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pedsim_msgs/msg" TYPE FILE FILES
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentState.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentStates.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentGroup.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentGroups.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/AgentForce.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/LineObstacle.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/LineObstacles.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/TrackedPerson.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/TrackedPersons.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/TrackedGroup.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/TrackedGroups.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/SocialRelation.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/SocialRelations.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/SocialActivity.msg"
    "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/msg/SocialActivities.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pedsim_msgs/cmake" TYPE FILE FILES "/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_msgs/catkin_generated/installspace/pedsim_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/ubuntu/ws/jackal_fyp/devel/include/pedsim_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/ubuntu/ws/jackal_fyp/devel/share/roseus/ros/pedsim_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/ubuntu/ws/jackal_fyp/devel/share/common-lisp/ros/pedsim_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/ubuntu/ws/jackal_fyp/devel/share/gennodejs/ros/pedsim_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/ubuntu/ws/jackal_fyp/devel/lib/python2.7/dist-packages/pedsim_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/ubuntu/ws/jackal_fyp/devel/lib/python2.7/dist-packages/pedsim_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_msgs/catkin_generated/installspace/pedsim_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pedsim_msgs/cmake" TYPE FILE FILES "/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_msgs/catkin_generated/installspace/pedsim_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pedsim_msgs/cmake" TYPE FILE FILES
    "/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_msgs/catkin_generated/installspace/pedsim_msgsConfig.cmake"
    "/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_msgs/catkin_generated/installspace/pedsim_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pedsim_msgs" TYPE FILE FILES "/home/ubuntu/ws/jackal_fyp/src/pedsim/pedsim_msgs/package.xml")
endif()

