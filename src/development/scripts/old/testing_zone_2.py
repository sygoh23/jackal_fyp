from math import sqrt
import math
import matplotlib
import matplotlib.pyplot as plt
import random

def linear_const(x1, x2, y1, y2):
    return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
    return abs(A*x+B*y+C)/sqrt(A**2+B**2)

def inside_radius(x0, y0, r, x_in, y_in):
    return (x_in-x0)**2+(y_in-y0)**2<=r**2

def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

min_dist = 3
max_dev_clean = 3
max_dev_boundary = 1
max_dev_remove = 3

def remove_points():
    #robot_xy = get_robot_xy()
    #x_in = dynamic_params.hist_x; y_in = dynamic_params.hist_y;
    #x_poi = dynamic_params.poi_x[-rec_attempts]; y_poi = dynamic_params.poi_y[-rec_attempts]
    #robot_x = robot_xy[0]; robot_y = robot_xy[1]

    x1 = -100
    y1 = 20

    x2 = 40
    y2 = -20

    x_poi = x1
    y_poi = y1

    robot_x = x2
    robot_y = y2

    x_in = range(x1, x2, 1)
    y_in = []
    const = linear_const(x1, x2, y1, y2)

    for i in range(len(x_in)):
        y_in.append((-const[2]-const[0]*x_in[i])/const[1])

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
    print(m)
    x_radius = []; y_radius = []
    for i in range(len(x_remove)):
        x_now = x_remove[i]
        y_now = y_remove[i]
        #x_radius.append(x_now)
        #y_radius.append(y_now)
        for j in range(-5, 5, 1):
            x_radius.append(x_now + j*math.cos(math.atan(m)))
            y_radius.append(y_now + j*math.sin(math.atan(m)))

    # Keep points that are close to the robot.
    # Don't set an obstacle too close to the robot.
    x_final = []; y_final = []
    for i in range(len(x_radius)):
        if (inside_radius(rb_seg_x[1], rb_seg_y[1], 5, x_radius[i], y_radius[i]) == False):
            x_final.append(x_radius[i])
            y_final.append(y_radius[i])
    return x_final, y_final, x_in, y_in

x_remove, y_remove, x_in, y_in = remove_points()
print(len(x_remove))
plt.scatter(x_in, y_in)
plt.gca().set_aspect('equal', adjustable='box')

plt.figure()
plt.scatter(x_remove, y_remove, c='r', marker='.', s=50, alpha=0.1, label='0')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
