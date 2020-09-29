from static_params import *
from utils import *
from math import sqrt
import math
import dynamic_params
import matplotlib
import matplotlib.pyplot as plt
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
#matplotlib.use('Agg')

# Parameters:
min_dist = 3 # Keep points given they are 'min_dist' apart from each other...
# Larger: Removes more points from original data.
# Smaller: Removes less points from original data.

max_dev_clean = 3 # Maximum deviation from a line segment to mark a POI...
# Larger: Sharper / tighter bends are needed to mark a POI.
# Smaller: Slight bends will mark a POI.

max_dev_boundary = 1 # Maximum deviation around robot and POI point...
# Larger: Points further away from robot position will be marked for removal

max_dev_remove = 3 # Maximum deviation from robot-POI line segment to remove points...
# This value can be set close to 'max_dev_clean'


# Function definitions:
def linear_const(x1, x2, y1, y2):
    return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
    return abs(A*x+B*y+C)/sqrt(A**2+B**2)

def inside_radius(x0, y0, r, x_in, y_in):
    return (x_in-x0)**2+(y_in-y0)**2<=r**2

# Update map file:
def update_map_old():
    plt.grid(b=True, which='major', color='#d6d6d6', linestyle='--')
    plt.scatter(dynamic_params.remove_x, dynamic_params.remove_y, c='r', marker='.', s=50, label='0')
    plt.scatter(dynamic_params.hist_x, dynamic_params.hist_y, c='k', marker='.', alpha=0.5, label='1')
    plt.scatter(dynamic_params.poi_x, dynamic_params.poi_y, c='b', marker='D', s=50, label='-1')

    if (dynamic_params.rec_plot == False) and (dynamic_params.recovery_override == 1):
        plt.scatter(dynamic_params.rec_x, dynamic_params.rec_y, c='b', marker='D', s=50, label='0')
        dynamic_params.rec_plot == True
    elif (dynamic_params.rec_plot == True) and (dynamic_params.recovery_override == 1):
        plt.scatter(dynamic_params.rec_x, dynamic_params.rec_y, c='green', marker='D', s=50, label='0')
        dynamic_params.rec_plot == False

    plt.gca().set_aspect('equal', adjustable='box')
    #plt.savefig("/home/ubuntu/Map.png")

# Save robot history:
def save_history(i):
    robot_xy = get_robot_xy()
    dynamic_params.hist_x.append(robot_xy[0])
    dynamic_params.hist_y.append(robot_xy[1])

    # Extract most recent points up to certain distance
    # Used to ensure robot isn't moving backwards
    if i > 1:
        dynamic_params.recent_x = []
        dynamic_params.recent_y = []

        reverse_x = dynamic_params.hist_x[:]; reverse_y = dynamic_params.hist_y[:];
        reverse_x.reverse(); reverse_y.reverse()
        total_dist = 0
        for p in range(len(dynamic_params.hist_x)-1):
            recent_dist = get_distance(reverse_x[p], reverse_x[p+1], reverse_y[p], reverse_y[p+1])
            total_dist = total_dist + recent_dist
            dynamic_params.recent_x.append(reverse_x[p])
            dynamic_params.recent_y.append(reverse_y[p])
            if total_dist > robot_range:
                break

# Find points of interest in map:
def find_poi():
    x_in = dynamic_params.hist_x[:]; y_in =dynamic_params.hist_y[:]
    x_out = x_in; y_out = y_in
    prev_len = len(dynamic_params.poi_x)
    p = 0

    # Remove points which are too close to each other:
    while p < (len(x_out)-1):
        dist = get_distance(x_in[p], x_in[p+1], y_in[p], y_in[p+1])
        if dist < min_dist:
            del_p = p + 1; p = 0;
            del x_out[del_p]; del y_out[del_p]
        else:
            p += 1

    # Detect points of interest:
    # (Calculates points which deviate too far from a line segment)
    poi = []; i = 0; j = 2
    while True:
        if (j >= (len(x_out)-1)) or (i >= (len(x_out)-1)):
            break
        const = linear_const(x_out[i], x_out[j], y_out[i], y_out[j])
        for k in range(i+1, j):
            d = linear_dist(const[0], const[1], const[2], x_out[k], y_out[k])
            if d > max_dev_clean:
                poi.append(j)
                i = j; j = j + 2
                break
        j += 1
    x_poi = [x_out[i] for i in poi]; y_poi = [y_out[i] for i in poi]
    dynamic_params.poi_x = x_poi[:]; dynamic_params.poi_y = y_poi[:]

    if len(x_poi) > prev_len:
        print("--- POI detected @ " + str([x_poi[-1], y_poi[-1]]))
    return

# Remove points in a dead end:
def remove_points(rec_attempts):
    robot_xy = get_robot_xy()
    x_in = dynamic_params.hist_x; y_in = dynamic_params.hist_y;
    x_poi = dynamic_params.poi_x[-rec_attempts]; y_poi = dynamic_params.poi_y[-rec_attempts]
    robot_x = robot_xy[0]; robot_y = robot_xy[1]
    rb_seg_x = [robot_x, x_poi]; rb_seg_y = [robot_y, y_poi]

    # Highlight points that should be checked for removal:
    check_point = []
    for i in range(len(x_in)):
        if (x_in[i] > (min(rb_seg_x)-max_dev_boundary)) and (x_in[i] < (max(rb_seg_x)+max_dev_boundary)):
            if (y_in[i] > (min(rb_seg_y)-max_dev_boundary)) and (y_in[i] < (max(rb_seg_y)+max_dev_boundary)):
                check_point.append(i)
    print("- Points to Check: " + str(len(check_point)) + " points")
    x_flag = [x_in[i] for i in check_point]; y_flag = [y_in[i] for i in check_point]

    # Mark points to remove that deviate from line segment:
    remove_point = []
    const = linear_const(rb_seg_x[0], rb_seg_x[1], rb_seg_y[0], rb_seg_y[1])
    for i in check_point:
        d = linear_dist(const[0], const[1], const[2], x_in[i], y_in[i])
        if d < max_dev_remove and (inside_radius(rb_seg_x[1], rb_seg_y[1], max_dev_remove, x_in[i], y_in[i]) == False):
            remove_point.append(i)
    print("- Points to Remove: " + str(len(remove_point)) + " points")
    x_remove = [x_in[i] for i in remove_point]; y_remove= [y_in[i] for i in remove_point]

    # Add in additional points at a radius around each removed point:
    m = const[1]/const[0]
    x_radius = []; y_radius = []
    for i in range(len(x_remove)):
        x_now = x_remove[i]
        y_now = y_remove[i]
        clear_dist = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
        for j in range(len(clear_dist)):
            x_radius.append(x_now + clear_dist[j]*math.cos(math.atan(m)))
            y_radius.append(y_now + clear_dist[j]*math.sin(math.atan(m)))

    # Keep points that are close to the robot.
    # Don't set an obstacle too close to the robot.
    x_final = []; y_final = []
    for i in range(len(x_radius)):
        if (inside_radius(rb_seg_x[1], rb_seg_y[1], 5, x_radius[i], y_radius[i]) == False):
            x_final.append(x_radius[i])
            y_final.append(y_radius[i])

    dynamic_params.remove_x = x_final[:]
    dynamic_params.remove_y = y_final[:]
    return
