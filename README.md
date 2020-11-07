# ECSE Final Year Project

<img src="https://github.com/sygoh23/jackal_fyp/blob/master/.images/04-poster.png" width="600">

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
2. Setup ROS Launch File: Choose simulation parameters inside of `development/launch/simulation.launch`. Select the world file by changing the "world_name" argument in Gazebo config. Select the corresponding PEDSIM scenario file by changing the "scene_file" argument in the PEDSIM config. 
* The available options are:
  * `start_at_b72.world/xml`: Start robot at Faculty of Engineering (Building 72)
  * `start_at_boiler_house.world/xml`: Start robot at Boiler House
  * `start_at_new_horizons.world/xml`: Start Jackal at New Horizons
  * `start_at_sticking_point.world/xml`: Start Jackal at Sticking Point
  * `start_within_vicinity.world/xml`: Start Jackal within Building Vicinity (Engineering Lecture Theatres)
3. Setup Python Launch File: Choose simulation parameters inside of `development/scripts/simulation_setup.py`. Select the same robot starting location used in the previous step. Select the robot target location and ensure you set the simulation computer so that the directories are correct. Edit `base_pth` if necessary to match your Ubuntu directories.
4. Launch Simulation: Change directory to `jackal_fyp/start` and run the following script: `simulation.sh`. Alternatively, the simulation can be launched directly using `roslaunch development simulation.launch`.
5. Launch Algorithm: To initiate the entire algorithm, run `algorithm.sh`. During the algorithm runtime, the algorithm map will be updated in the `/live/map.png` file during Stage 1 of the algorithm, and the wall following output will be updated in the `/live/hough.jpg` file during Stage 2 of the algorithm.

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
