from static_params import *
from utils import *
from math import sqrt

# Parameters:
min_dist = 3 # Keep points given they are 'min_dist' apart from each other...
# Larger: Removes more points from original data.
# Smaller: Removes less points from original data.

max_dev_clean = 2 # Maximum deviation from a line segment to mark a POI...
# Larger: Sharper / tighter bends are needed to mark a POI.
# Smaller: Slight bends will mark a POI.

max_dev_boundary = 3 # Maximum deviation around robot and POI point...
# Larger: Points further away from robot position will be marked for removal

max_dev_remove = max_dev_clean # Maximum deviation from robot-POI line segment to remove points...
# This value can be set close to 'max_dev_clean'

# Function definitions:
def linear_const(x1, x2, y1, y2):
    return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
    return abs(A*x+B*y+C)/sqrt(A**2+B**2)

def inside_radius(x0, y0, r, x_in, y_in):
    return (x_in-x0)**2+(y_in-y0)**2<=r**2

def find_poi(x_in, y_in):
    x_out = x_in
    y_out = y_in
    p = 0

    # REMOVE POINTS TOO CLOSE:
    while p < (len(x_out)-1):
        dist = get_distance(x_in[p], x_in[p+1], y_in[p], y_in[p+1])
        if dist < min_dist:
            del_p = p + 1; p = 0;
            del x_out[del_p]; del y_out[del_p]
        else:
            p += 1

    # DETECT POINTS OF INTEREST:
    poi = []; i = 0; j = 2
    while True:
        if (j >= (len(x_out)-1)) or (i >= (len(x_out)-1)):
            break
        const = linear_const(x_out[i], x_out[j], y_out[i], y_out[j])
        for k in range(i+1, j):
            d = linear_dist(const[0], const[1], const[2], x_out[k], y_out[k])
            if d > max_dev_clean:
                poi.append(j)
                print("- POI detected at " + str([x_out[j], y_out[j]]))
                i = j; j = j + 2
                break
        j += 1
    x_poi = [x_out[i] for i in poi]; y_poi = [y_out[i] for i in poi]
    return x_poi, y_poi

def remove_points(x_in, y_in, x_poi, y_poi, robot_x, roboy_y):
    rb_seg_x = [robot_x, x_poi[-1]]
    rb_seg_y = [robot_y, y_poi[-1]]
    check_point = []
    for i in range(len(x_in)):
        if (x_in[i] > (min(rb_seg_x)-max_dev_boundary)) and (x_in[i] < (max(rb_seg_x)+max_dev_boundary)):
            if (y_in[i] > (min(rb_seg_y)-max_dev_boundary)) and (y_in[i] < (max(rb_seg_y)+max_dev_boundary)):
                check_point.append(i)
    print("- Points to Check: " + str(len(check_point)) + " points")
    x_flag = [x_in[i] for i in check_point]; y_flag = [y_in[i] for i in check_point]

    remove_point = []
    const = linear_const(rb_seg_x[0], rb_seg_x[1], rb_seg_y[0], rb_seg_y[1])
    for i in check_point:
        d = linear_dist(const[0], const[1], const[2], x_in[i], y_in[i])
        #print("-- Checking point: " + str(i) + " | Distance: " + str(d))
        if d < max_dev_remove and (inside_radius(rb_seg_x[1], rb_seg_y[1], max_dev_remove, x_in[i], y_in[i]) == False):
            remove_point.append(i)
    print("- Points to Remove: " + str(len(remove_point)) + " points")
    x_remove = [x_in[i] for i in remove_point]; y_remove= [y_in[i] for i in remove_point]
