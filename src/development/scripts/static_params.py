"""
Contains static parameters to be accessed throughout the algorithm.
Import this file as 'from static_params import *', then all parameters will be added to the file namespace.
Do not assign local variables with the same name as these parameters.
Do not change the value of these parameters, only access their value.
"""

import rospy
import numpy as np

#################### Coordinates ####################
# X-offset: 105 to test from start point, 63 to test from sticking point, -18 to test from within eng lectures vicinity
offset_x = 105  

# Y-offset: 10 to test from start point, 74 to test from sticking point, -140 to test from within eng lectures vicinity
offset_y = 10       

building_centers = [
    # Index 0: Eng Faculty
    [-100+offset_x, -40+offset_y],

    # Index 1: New Horizons
    [-60+offset_x, 70+offset_y],

    # Index 2: HAL
    [-110+offset_x, -90+offset_y],

    # Index 3: Monash Motorsport
    [20+offset_x, -10+offset_y],

    # Index 4: Eng Lecture Theatres. Y-value was -120
    [20+offset_x, -135+offset_y]
]

building_entrances = [
    # Index 0: Eng Faculty
    [-104+offset_x, -17+offset_y],

    # Index 1: New Horizons
    [-72+offset_x, 45+offset_y],

    # Index 2: HAL
    [-94+offset_x, -110+offset_y],

    # Index 3: Monash Motorsport
    [25+offset_x, -44+offset_y],

    # Index 4: Eng Lecture Theatres
    [25+offset_x, -140+offset_y]
]

building_bounding_polygons = [
    # Index 0: Eng Faculty
    np.array([
        [-70+offset_x, 5+offset_y],
        [-71+offset_x, -40+offset_y],
        [-135+offset_x, -40+offset_y],
        [-130+offset_x, 5+offset_y],
        [-70+offset_x, 5+offset_y]
    ]),

    # Index 1: New Horizons
    np.array([
        [-45+offset_x, 0+offset_y],
        [-42+offset_x, 50+offset_y],
        [-100+offset_x, 60+offset_y],
        [-100+offset_x, 40+offset_y],
        [-80+offset_x, 10+offset_y],
        [-45+offset_x, 0+offset_y]
    ]),

    # Index 2: HAL
    np.array([
        [-60+offset_x, -90+offset_y],
        [-60+offset_x, -112+offset_y],
        [-72+offset_x, -112+offset_y],
        [-97+offset_x, -128+offset_y],
        [-135+offset_x, -128+offset_y],
        [-135+offset_x, -110+offset_y],
        [-60+offset_x, -90+offset_y]
    ]),

    # Index 3: Monash Motorsport
    np.array([
        [-17+offset_x, -41+offset_y],
        [-17+offset_x, -53+offset_y],
        [65+offset_x, -56+offset_y],
        [65+offset_x, -41+offset_y],
        [-17+offset_x, -41+offset_y]
    ]),

    # Index 4: Eng Lecture Theatres
    np.array([
        [50+offset_x, -153+offset_y],
        [50+offset_x, -130+offset_y],
        [-20+offset_x, -130+offset_y],
        [-20+offset_x, -153+offset_y],
        [50+offset_x, -153+offset_y]
    ])
]

#################### Set Targets ####################
target = 4  # 0 = eng faculty, 1 = NH, 2 = HAL, 3 = MMS, 4 = lecture theatres
building_center_xy = building_entrances[target]         # Do not need to change (was set to building_centers[target])
building_entrance_xy = building_entrances[target]       # Do not need to change
building_polygon = building_bounding_polygons[target]   # Do not need to change

#################### Object Detection ####################
model_pth = "/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/Models/ssd300_epoch6.pth.tar"     # Full path to model
font_pth = "/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/OpenSans-Regular.ttf"              # Full path to font file
use_webcam = rospy.get_param("/move_base/webcam")           # Do not need to change
process_img = rospy.get_param("/move_base/img_process")     # Do not need to change

#################### Algorithm ####################
t_delay = 1                 # Seconds between iterations (lower = more responsive)
robot_range = 15            # Radius around the robot in which pedestrians must be in order to be 'detected'
target_threshold = 1        # Radius threshold to determine when the robot has reached a given target point
straight_line_dist = 2      # Distance that the robot should move in a straight line towards a given target point
movement_pause = 8          # Seconds that the robot should wait in between movements
phase3_dist = 10            # Distance that the robot should follow a pedestrian for in phase 3
zone_length = 5             # Side length of a generated square, which is currently used as a no-go zone