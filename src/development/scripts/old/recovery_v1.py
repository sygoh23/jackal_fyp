from static_params import *
from utils import *
from math import sqrt

# Parameters:
min_dist = 5 # Keep points given they are 'min_dist' apart from each other...
# Larger: Removes more points from original data.
# Smaller: Removes less points from original data.

max_dev_clean = 3 # Maximum deviation from a line segment to mark a POI...
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
    #print("\nSTAGE 1: DATA CLEANING:")
    #print("- Original: " + str(len(x_out)) + " points")
    p = 0
    while p < (len(x_out)-1):
        #print([x_in[p], y_in[p]])
        #print([x_in[p+1], y_in[p+1]])
        dist = sqrt((x_in[p] - x_in[p+1])**2 + (y_in[p] - y_in[p+1])**2)
        #print("- Checking: " + str(len(x_out)) + " | Distance: " + str(dist))
        if dist < min_dist:
            del_p = p + 1; p = 0;
            del x_out[del_p]; del y_out[del_p]
        else:
            p += 1
    #print("- New Size: " + str(len(x_out)) + " points\n")

    # Check points distance from a line:
    #print("STAGE 2: POI DETECTION:")
    poi = []; i = 0; j = 2
    while True:
        if (j >= (len(x_out)-1)) or (i >= (len(x_out)-1)):
            break
        #print("- Checking segment from: " + str(i) + " -> " + str(j))
        const = linear_const(x_out[i], x_out[j], y_out[i], y_out[j])
        for k in range(i+1, j):
            d = linear_dist(const[0], const[1], const[2], x_out[k], y_out[k])
            if d > max_dev_clean:
                poi.append(j)
                #print("- POI Detected: " + str(j))
                print("- POI detected at " + str([x_out[j], y_out[j]]))
                i = j; j = j + 2
                break
        j += 1
    #print("- Points of interest: " + str(poi) +"\n")
    x_poi = [x_out[i] for i in poi]; y_poi = [y_out[i] for i in poi]
    return x_poi, y_poi
