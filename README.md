# ECSE Final Year Project

#### Last Major Update: 7th May 2020
<img src="https://github.com/sygoh23/jackal_fyp/blob/master/.images/02-jackal-pedsim.png" height="400">

### Source Code Structure:
```
jackal_fyp/src/...
```
- dependencies: Contains all of the miscellaneous ROS packages required to build the workspace.
- development: Main working folder for algorithm development and programming.
  - launch: Contains launch files for simulations.
  - resources: Contains resources for simulations with folders for `gazebo`, `pedsim` and `rviz`.
  - scripts: Contains scripts for listener and publisher nodes.
- jackal: Contains the modified Jackal robot (with additional sensors) for use in Gazebo and RViz.
- pedsim: Contains the 'pedsim_ros' library for simulating groups of pedestrians.

### Useful Start Commands:
```
jackal_fyp/start/...
```
- jackal_pedsim.sh: Launches Gazebo (with Jackal robot), Pedsim, RViz and a listener for pedestrian positions.
- jackal_pedsim_nav.sh: Launches Gazebo (with Jackal robot), Pedsim, Rviz, 'move_base' and a listener for pedestrian positions. Navigation goals can be set in RViz to demonstrate path planning.
- setup.sh: Sources the ROS installation


### Other Dependencies:
* The Jackal robot requires the Intel Realsense SDK.
  * Installation: https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md
  * Make sure to install the developer and debug packages.
* The ROS navigation package requires the following packages:
  * libsdl1-dev: `sudo apt-get install libsdl-dev`
  * libsdl-image1.2-dev: `sudo apt-get install libsdl-image1.2-dev`
* Gazebo requires the GAZEBO_MODEL_PATH environment variable to be set:
  1. Terminal: `source /usr/share/gazebo/setup.sh` (in case of error, replace with your gazebo install path to the file setup.sh)
  2. Terminal: `sudo nano /usr/share/gazebo/setup.sh` (in case of error, replace with your gazebo install path to the file setup.sh)
  3. Modify the file to include the path to this repo's /Models/ directory, which should be `"your-directory"/jackal_fyp/src/development/resources/gazebo/Models`. Enter this path in the line with the GAZEBO_MODEL_PATH variable, after the colon. Finish the path with another colon.
