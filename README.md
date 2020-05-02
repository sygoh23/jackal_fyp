# ECSE Final Year Project

#### Last Major Update: 30th April 2020
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
- jackal_gazebo.sh: Launches the Jackal robot with all sensors enabled in a sample world.
- jackal_rviz.sh: Launches RViz with appropriate Jackal configuration. Used with `jackal_gazebo.sh`.
- pedsim_demo.sh: Launches a sample Pedsim demonstration visualised in RViz.
- setup.sh: Sources the ROS installation


### Other Dependencies:
* The Jackal robot requires the Intel Realsense SDK. 
  * Installation: https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md
  * Make sure to install the developer and debug packages.
