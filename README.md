# ECSE Final Year Project

#### Last Major Update: 6th May 2020
<img src="https://github.com/sygoh23/jackal_fyp/blob/master/.images/00-pedsim-demo.png" height="400"><img src="https://github.com/sygoh23/jackal_fyp/blob/master/.images/01-rviz.png" height="400">

### Source Code Structure:
```
jackal_fyp/src/...
```
- dependencies: Contains all of the miscellaneous ROS packages required to build the workspace.
- development: Main working folder for algorithm development and programming.
- jackal: Contains the modified Jackal robot (with additional sensors) for use in Gazebo and RViz.
- pedsim: Contains the 'pedsim_ros' library for simulating groups of pedestrians.

### Useful Start Commands:
```
jackal_fyp/start/...
```
- full_simulation.sh: Launches Gazebo (with Jackal robot), Pedsim, RViz and a listener for pedestrian positions.
- pedsim_jackal_1.sh: Launches Gazebo with the Jackal robot.
- pedsim_jackal_2.sh: Launches Pedsim and Rviz to visualise the Jackal and pedestrians together.
- setup.sh: Sources the ROS installation


### Other Dependencies:
* The Jackal robot requires the Intel Realsense SDK.
  * Installation: https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md
  * Make sure to install the developer and debug packages.
* The ROS Navigation package requires the following packages:
  * libsdl1-dev: `sudo apt-get install libsdl-dev`
  * libsdl-image1.2-dev: `sudo apt-get install libsdl-image1.2-dev`
