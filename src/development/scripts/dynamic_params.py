"""
Contains dynamic parameters to be accessed and modified throughout the algorithm
--> Import this file as 'import dynamic_params', then access/modify any parameters as 'dynamic_params.parameter'
--> Do not assign local variables with the same name as these parameters
--> Modifying a parameter will modify it for all files which access it
"""

########## Algorithm ##########
reached_target = 0          # Flag for whether robot has reached the target doorway
goal_xy = [0, 0]            # Navigation goal sent to move_base
dist_last = []              # Distance of each pedestrian from the building center, from the previous iteration
ped_last = []               # x-y position of the last detected pedestrian, from the previous iteration
timer = 0                   # Initialise this to any value (just needs to be in the global scope). Is assigned to a timer object for pausing between robot movements
timer_set = 0               # Flag for whether the robot movement timer has been set
moving_to_last_ped = 0      # Flag for whether the robot is currently moving towards the last detected pedestrian
total_dist = 0              # Phase 3: total distance moved while following a particular pedestrian
robot_xy_prev = [0, 0]      # Phase 3: the robot's position from the previous iteration, used to calculate how far it has moved
following_ped = 0           # Phase 3: flag for whether the robot is following a pedestrian
ped_number = 0              # Phase 3: index of the pedestrian which the robot is following
out_of_range = 0            # Phase 3: flag for whether the pedestrian is out of the robot's range