test
# ECSE Final Year Project

#### Last Major Update: 21st May 2020
<img src="https://github.com/sygoh23/jackal_fyp/blob/master/.images/02-jackal-pedsim.png" height="250">

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
 
### Jackal Configuration:
The Jackal sensor configuration can be adjusted by changing the configuration argument in the simulation launch files. The following configurations are available:
 * `base`: Generates Jackal model only (fastest).
 * `fyp_laser`: Generates Jackal model with 2D laser scanner (fast).
 * `fyp_velodyne`: Generates Jackal model with 3D Velodyne Lidar at low resolution (slow).
 * `fyp_velodyne_hd`: Generates Jackal model with 3D Velodyne Lidar using GPU at high resolution (slowest).

### Simulation Instructions:
1. Source Required Files: Change directory to `jackal_fyp` and source the ROS installation and package files by running `setup.sh`.
2. Launch Simulation: Change directory to `jackal_fyp/start` and run one of the following scripts:
 * `ped_gazebo.sh`: Launches the Pedsim simulator with Gazebo integration.
 * `ped_only.sh`: Launches the Pedsim simulator only.

Alternatively, the simulation can be launched directly using `roslaunch development ped_gazebo.launch` or `roslaunch development ped_only.launch`.

3. Navigation & Pedestrian Following: To initiate the navigation stack, run `nav_addon.sh`. Ensure that the following arguments inside of `nav_addon.launch` are set correctly:
 * `ped_follow`: If set to true, the script will automatically start the pedestrian following algorithm.
 * `use_velodyne`: Set to true if using the `fyp_velodyne` or `fyp_velodyne_hd` sensor configurations.
 * `use_laser`: Set to true if using the `fyp_laser` sensor configuration.
 
Alternatively, the navigation stack can be launched directly using `roslaunch development nav_addon.launch`.

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
