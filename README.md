# ECSE Final Year Project

#### Last Major Update: 10th June 2020
<img src="https://github.com/sygoh23/jackal_fyp/blob/master/.images/03-engineering-sim.png" height="350">

### Source Code Structure:
```
jackal_fyp/src/...
```
- dependencies: Contains all of the miscellaneous ROS packages required to build the workspace.
- development: Main working folder for algorithm development and programming.
  - launch: Contains launch files for simulations.
  - resources: Contains resources for simulations with folders for `gazebo`, `move_base`, `pedsim` and `rviz`.
  - scripts: Contains scripts for Jackal pedestrian following and path planning.
- jackal: Contains the modified Jackal robot (with additional sensors) for use in Gazebo and RViz.
- pedsim: Contains the 'pedsim_ros' library for simulating groups of pedestrians.

### Useful Scripts:
Change directory to `jackal_fyp` and run one of the following scripts:
 * `reset.sh`: Kills all ROS processes.
 * `setup.sh`: Sources the ROS installation.
 * `reconfigure.sh`: Launches dynamic reconfigure.
 
### Jackal Configuration:
The Jackal sensor configuration can be adjusted by changing the configuration argument in the simulation launch files. The following configurations are available:
 * `base`: Generates Jackal model only (fastest).
 * `fyp_laser`: Generates Jackal model with 2D laser scanner (fast).
 * `fyp_velodyne`: Generates Jackal model with 3D Velodyne Lidar at low resolution (slow).
 * `fyp_velodyne_hd`: Generates Jackal model with 3D Velodyne Lidar using GPU at high resolution (slowest).

### Simulation Instructions:
1. Source Required Files: Change directory to `jackal_fyp` and source the ROS installation and package files by running `setup.sh`.
2. Launch Simulation: Change directory to `jackal_fyp/start` and run the following script: `simulation.sh`. Alternatively, the simulation can be launched directly using `roslaunch development simulation.launch`.

3. Navigation & Pedestrian Following: To initiate the navigation stack, run `navigation.sh`. If the argument `ped_follow` inside `navigation.launch` is set to true, the script will automatically start the pedestrian following algorithm. The navigation stack can also be launched directly using `roslaunch development navigation.launch`.

### Other Dependencies:
* The Jackal robot requires the Intel Realsense SDK for the D435 Depth Cameras.
  * Installation: https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md
  * Make sure to install the developer and debug packages.
* The ROS navigation package requires the following packages:
  * libsdl1-dev: `sudo apt-get install libsdl-dev`
  * libsdl-image1.2-dev: `sudo apt-get install libsdl-image1.2-dev`
* Gazebo requires the `GAZEBO_MODEL_PATH` environment variable to be set:
  1. Terminal: `source /usr/share/gazebo/setup.sh` (in case of error, replace with your gazebo install path to the file setup.sh).
  2. Terminal: `sudo nano /usr/share/gazebo/setup.sh` (in case of error, replace with your gazebo install path to the file setup.sh),
  3. Modify the file to include the path to this repo's `/Models/` directory, which should be `"your-directory"/jackal_fyp/src/development/resources/gazebo/Models`. Enter this path in the line with the GAZEBO_MODEL_PATH variable, after the colon. Finish the path with another colon.
* The Velodyne Lidar scanner requires the following Gazebo plugins in your `/opt/ros/melodic/lib` folder. A copy of these files can be found in the `plugins` folder.
  * `libgazebo_ros_velodyne_gpu_laser.so`
  * `libgazebo_ros_velodyne_laser.so`
