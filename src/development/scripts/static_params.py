# Building coordinates
offset_x = 105
offset_y = 10
new_horizons_center = [-60+offset_x, 70+offset_y]
#new_horizons_entrance = [-60+offset_x, 70+offset_y]
building_center_xy = new_horizons_center

# Algorithm parameters
n_loop = 10000          # Number of following iterations
t_delay = 2             # Time between iterations (lower = more responsive)
robot_range = 20        # Radius around the robot in which pedestrians must be in order to be 'detected'
building_threshold = 10 # Radius threshold to determine when robot is in vicinity of target building
target_threshold = 2    # Radius threshold to determine when robot has reached target entrance