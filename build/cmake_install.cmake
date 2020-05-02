# Install script for directory: /home/ubuntu/ws/jackal_fyp/src

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
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/ws/jackal_fyp/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/ubuntu/ws/jackal_fyp/install" TYPE PROGRAM FILES "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/ws/jackal_fyp/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/ubuntu/ws/jackal_fyp/install" TYPE PROGRAM FILES "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/ws/jackal_fyp/install/setup.bash;/home/ubuntu/ws/jackal_fyp/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/ubuntu/ws/jackal_fyp/install" TYPE FILE FILES
    "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/setup.bash"
    "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/ws/jackal_fyp/install/setup.sh;/home/ubuntu/ws/jackal_fyp/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/ubuntu/ws/jackal_fyp/install" TYPE FILE FILES
    "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/setup.sh"
    "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/ws/jackal_fyp/install/setup.zsh;/home/ubuntu/ws/jackal_fyp/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/ubuntu/ws/jackal_fyp/install" TYPE FILE FILES
    "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/setup.zsh"
    "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/ws/jackal_fyp/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/ubuntu/ws/jackal_fyp/install" TYPE FILE FILES "/home/ubuntu/ws/jackal_fyp/build/catkin_generated/installspace/.rosinstall")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/ubuntu/ws/jackal_fyp/build/gtest/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/development/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/geographic_info/geographic_info/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_desktop/jackal_desktop/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_simulator/jackal_simulator/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_tutorials/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_ros/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/pointgrey_camera_driver/pointgrey_camera_description/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/realsense/realsense2_description/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/pointgrey_camera_driver/statistics_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/pointgrey_camera_driver/image_exposure_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/unique_identifier/unique_identifier/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/unique_identifier/uuid_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/geographic_info/geographic_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/3rdparty/libpedsim/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_cartographer_navigation/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_control/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_description/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_simulator/jackal_gazebo/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_navigation/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/jackal/jackal_desktop/jackal_viz/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/2ndparty/spencer_messages/spencer_human_attribute_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/2ndparty/spencer_messages/spencer_tracking_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/ddynamic_reconfigure/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/lms1xx/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_srvs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_utils/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_visualizer/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/2ndparty/spencer_messages/spencer_social_relation_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/2ndparty/spencer_messages/spencer_vision_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/interactive_marker_twist_server/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_sensors/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/pedsim_simulator/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/realsense/realsense2_camera/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/realsense_gazebo_plugin/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/robot_localization/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/twist_mux/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/unique_identifier/unique_id/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/geographic_info/geodesy/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/pedsim/2ndparty/spencer_tracking_rviz_plugin/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/pointgrey_camera_driver/wfov_camera_msgs/cmake_install.cmake")
  include("/home/ubuntu/ws/jackal_fyp/build/dependencies/pointgrey_camera_driver/pointgrey_camera_driver/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/ubuntu/ws/jackal_fyp/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
