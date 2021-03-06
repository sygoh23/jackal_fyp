"""
Contains dynamic parameters to be accessed and modified throughout the algorithm.
Import this file as 'import dynamic_params', then access/modify any parameters as 'dynamic_params.parameter'.
Do not assign local variables with the same name as these parameters.
Modifying a parameter will modify it for all files which access it.
"""

import numpy as np
from static_params import *

########## Algorithm ##########
reached_target = 0          # Flag for whether robot has reached the target building entrance
entrance_found = False      # Flag for whether entrance has been found by object detection model
goal_xy = [0, 0]            # Navigation goal sent to move_base
dist_last = []              # Distance of each pedestrian from the building center, from the previous iteration
ped_last = []               # Phase 2: x-y position of the last detected pedestrian, from the previous iteration
timer = 0                   # Initialise this to any value (just needs to be in the global scope). Is assigned to a timer object for pausing between robot movements
timer_set = 0               # Flag for whether the robot movement timer has been set
moving_to_last_ped = 0      # Phase 2: flag for whether the robot is currently moving towards the last detected pedestrian
total_dist = 0              # Phase 3: total distance moved while following a particular pedestrian
robot_xy_prev = [0, 0]      # Phase 3: the robot's position from the previous iteration, used to calculate how far it has moved
following_ped = 0           # Phase 3: flag for whether the robot is following a pedestrian
ped_number = 0              # Phase 3: index of the pedestrian which the robot is following
out_of_range = 0            # Phase 3: flag for whether the pedestrian is out of the robot's range
exclusion_zones = [         # List of polygons in which the robot should not set its movement goal
    np.array([
        [-114+offset_x, -25+offset_y],
        [-98+offset_x, -25+offset_y],
        [-102+offset_x, -8+offset_y],
        [-116+offset_x, -3+offset_y],
        [-109+offset_x, -25+offset_y]
    ])
]

########## Recovery Behaviour ##########
recovery_override = 0       # Prevents other code running during recovery
remove_radius = 5           # Radius around points to prevent goal setting
hist_x = [];                # Robot location history
hist_y = []
remove_x = []               # Removed points due to recovery behaviour
remove_y = []
poi_x = []                  # Points of interest
poi_y = []
recent_x = []               # Most recent coordinates
recent_y = []
recovery_prev_poi = []

########## Mapping ##########
map_range = [];             # Robot mapping range
robot_xy = [];              # Robot current position
cloud_x = [];               # Point cloud
cloud_y = []
ped_x_excl = [];            # Excluded pedestrians
ped_y_excl = []
ped_x_los = [];             # Allowed pedestrians
ped_y_los = []

# Debugging:
debug_please = []
