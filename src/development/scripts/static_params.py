"""
Contains static parameters to be accessed throughout the algorithm

--> Import this file as 'from static_params import *', then all parameters will be added to the file namespace
--> Do not assign local variables with the same name as these parameters
--> Do not change the value of these parameters, only access their value
"""

#################### Coordinates ####################
offset_x = 105
offset_y = 10

eng_faculty_center = [-100+offset_x, -40+offset_y]
eng_faculty_entrance = [-104+offset_x, -17+offset_y]

new_horizons_center = [-60+offset_x, 70+offset_y]
new_horizons_entrance = [-72+offset_x, 45+offset_y]

HAL_center = [-110+offset_x, -90+offset_y]
HAL_entrance = [-94+offset_x, -110+offset_y]

motorsport_center = [20+offset_x, -10+offset_y]
motorsport_entrance = [25+offset_x, -44+offset_y]

lecture_theatres_center = [20+offset_x, -120+offset_y]
lecture_theatres_entrance = [25+offset_x, -140+offset_y]


#################### Set Target Building ####################
building_center_xy = new_horizons_center
building_entrance_xy = new_horizons_entrance


#################### Algorithm ####################
n_loop = 10000              # Number of following iterations
t_delay = 2                 # Seconds between iterations (lower = more responsive)
robot_range = 20            # Radius around the robot in which pedestrians must be in order to be 'detected'
building_threshold = 30     # Radius threshold to determine when the robot is in the vicinity of the target building