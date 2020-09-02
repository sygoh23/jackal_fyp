import matplotlib.pyplot as plt
from math import sqrt

# Parameters:
min_dist = 10 # Keep points given they are 'min_dist' apart from each other...
# Larger: Removes more points from original data.
# Smaller: Removes less points from original data.

max_dev_clean = 3 # Maximum deviation from a line segment to mark a POI...
# Larger: Sharper / tighter bends are needed to mark a POI.
# Smaller: Slight bends will mark a POI.

max_dev_boundary = 3 # Maximum deviation around robot and POI point...
# Larger: Points further away from robot position will be marked for removal

max_dev_remove = max_dev_clean # Maximum deviation from robot-POI line segment to remove points...
# This value can be set close to 'max_dev_clean'

x_pth = "/home/ubuntu/Mapping/x_v3-motorsport.txt"
y_pth = "/home/ubuntu/Mapping/y_v3-motorsport.txt"

# Function definitions:
def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def linear_const(x1, x2, y1, y2):
    return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
    return abs(A*x+B*y+C)/sqrt(A**2+B**2)

def inside_radius(x0, y0, r, x_in, y_in):
    return (x_in-x0)**2+(y_in-y0)**2<=r**2

def read_x(pth):
    x = []
    with open(pth, 'r') as filehandle:
        filecontents = filehandle.readlines()
        for line in filecontents:
            x.append(float(line[:-1]))
    return x

def read_y(pth):
    with open(pth, 'r') as filehandle:
        y = []
        filecontents = filehandle.readlines()
        for line in filecontents:
            y.append(float(line[:-1]))
        return y

# Get started!
print("PARAMETERS:")
print("- Min Distance: " + str(min_dist) + "m")
print("- Max Deviation " + str(max_dev_clean) + "m")

# Clean points which are too close to each other:
x_in = read_x(x_pth); x_out = x_in
y_in = read_y(y_pth); y_out = y_in
print("\nSTAGE 1: DATA CLEANING:")
print("- Original: " + str(len(x_out)) + " points")
i = 0
while i < (len(x_out)-1):
    dist = get_distance(x_in[i], x_in[i+1], y_in[i], y_in[i+1])
    if dist < min_dist:
        del_i = i + 1; i = 0;
        del x_out[del_i]; del y_out[del_i]
    else:
        i += 1
print("- New Size: " + str(len(x_out)) + " points\n")
# Check points distance from a line:
print("STAGE 2: POI DETECTION:")
poi = []; i = 0; j = 2
length = len(x_out)

while True:
    if (j >= (len(x_out)-1)) or (i >= (len(x_out)-1)):
        break
    print("- Checking segment from: " + str(i) + " -> " + str(j))
    const = linear_const(x_out[i], x_out[j], y_out[i], y_out[j])
    for k in range(i+1, j):
        d = linear_dist(const[0], const[1], const[2], x_out[k], y_out[k])
        #print("-- Point: " + str(k) + " | Distance: " + str(d))
        if d > max_dev_clean:
            poi.append(j)
            print("-- POI Detected: " + str(j))
            i = j; j = j + 2
            break
    j += 1

print("- Points of interest: " + str(poi) +"\n")
x_poi = [x_out[i] for i in poi]; y_poi = [y_out[i] for i in poi]

# Plot results:
fig1 = plt.figure()
fig1.suptitle('Stage 2: Points of Interest (Cleaned)')
plt.scatter(x_out, y_out, c='k', marker='.', alpha=.8, label='1')
plt.scatter(x_poi, y_poi, c='b', marker='D', s=50, label='-1')
plt.gca().set_aspect('equal', adjustable='box')

# Eliminate points between robot and POI:
x_in = read_x(x_pth);
y_in = read_y(y_pth);
rb_robot_xy = [135, -39]
rb_seg_x = [rb_robot_xy[0], x_poi[-1]]
rb_seg_y = [rb_robot_xy[1], y_poi[-1]]
print("STAGE 3: POINT FLAGGING")
print("- Robot Position: " + str(rb_robot_xy))
print("- Last POI: " + str([x_poi[-1], y_poi[-1]]))

# Check if points are between robot and POI:
check_point = []
for i in range(len(x_in)):
    if (x_in[i] > (min(rb_seg_x)-max_dev_boundary)) and (x_in[i] < (max(rb_seg_x)+max_dev_boundary)):
        if (y_in[i] > (min(rb_seg_y)-max_dev_boundary)) and (y_in[i] < (max(rb_seg_y)+max_dev_boundary)):
            check_point.append(i)
print("- Points to Check: " + str(len(check_point)) + " points")
x_flag = [x_in[i] for i in check_point]; y_flag = [y_in[i] for i in check_point]

# Flagged points:
fig2 = plt.figure()
fig2.suptitle('Stage 3A: Points for Checking')
plt.scatter(x_in, y_in, c='k', marker='.', alpha=.5, label='1')
plt.scatter(x_poi, y_poi, c='b', marker='D', s=50, label='-1')
plt.scatter(x_flag, y_flag, c='y', marker='*', label='0')
plt.gca().set_aspect('equal', adjustable='box')

# Check if points deviate from line connecting robot and POI:
remove_point = []
const = linear_const(rb_seg_x[0], rb_seg_x[1], rb_seg_y[0], rb_seg_y[1])
for i in check_point:
    d = linear_dist(const[0], const[1], const[2], x_in[i], y_in[i])
    #print("-- Checking point: " + str(i) + " | Distance: " + str(d))
    if d < max_dev_remove and (inside_radius(rb_seg_x[1], rb_seg_y[1], max_dev_remove, x_in[i], y_in[i]) == False):
        remove_point.append(i)
print("- Points to Remove: " + str(len(remove_point)) + " points")
x_remove = [x_in[i] for i in remove_point]; y_remove= [y_in[i] for i in remove_point]

print("- Flagged Points (x): " + str(x_remove))
print("- Flagged Points (y): " + str(y_remove))

# Removed points:
fig3 = plt.figure()
fig3.suptitle('Stage 3B: Points for Removal')
plt.scatter(x_in, y_in, c='k', marker='.', alpha=.5, label='1')
plt.scatter(x_poi, y_poi, c='b', marker='D', s=50, label='-1')
plt.scatter(x_remove, y_remove, c='r', marker='+', label='0')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
