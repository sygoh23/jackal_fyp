import matplotlib.pyplot as plt
from math import sqrt

# Parameters:
min_dist = 10
max_dev_clean = 4
max_dev_filter = 1
x_pth = "/home/ubuntu/Mapping/x_v3.txt"
y_pth = "/home/ubuntu/Mapping/y_v3.txt"

# Function definitions:
def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def linear_const(x1, x2, y1, y2):
    return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
    return abs(A*x+B*y+C)/sqrt(A**2+B**2)

# Load files:
x_in = []; y_in = []
with open(x_pth, 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        x_in.append(float(line[:-1]))

with open(y_pth, 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        y_in.append(float(line[:-1]))

print("LIST LENGTH: " + str(len(x_in)))

print("PARAMETERS:")
print("- Min Distance: " + str(min_dist) + "m")
print("- Max Deviation " + str(max_dev_clean) + "m")

# Clean points which are too close to each other:
x_out = x_in
x_orig = x_in
y_out = y_in
y_orig = y_in

print("LIST LENGTH: " + str(len(x_in)))

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

print("LIST LENGTH: " + str(len(x_in)))

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
fig1.suptitle('Stage 2: Points of Interest')
plt.scatter(x_out, y_out, c='k', marker='.', alpha=.5, label='1')
plt.scatter(x_poi, y_poi, c='b', marker='D', s=50, label='-1')
plt.gca().set_aspect('equal', adjustable='box')

# Eliminate points between robot and POI:
rb_robot_xy = [140, -40]
rb_seg_x = [rb_robot_xy[0], x_poi[-1]]
rb_seg_y = [rb_robot_xy[1], y_poi[-1]]
print("STAGE 3: POINT FLAGGING")
print("- Robot Position: " + str(rb_robot_xy))
print("- Last POI: " + str([x_poi[-1], y_poi[-1]]))

# Check if points are between robot and POI:
filter_1 = []
for i in range(len(x_in)):
    if (x_in[i] > (min(rb_seg_x)-max_dev_filter)) and (x_in[i] < (max(rb_seg_x)+max_dev_filter)):
        if (y_in[i] > (min(rb_seg_y)-max_dev_filter)) and (y_in[i] < (max(rb_seg_y)+max_dev_filter)):
            filter_1.append(i)
print(filter_1)
x_filter = [x_in[i] for i in filter_1]; y_filter = [y_in[i] for i in filter_1]

fig2 = plt.figure()
fig2.suptitle('Stage 3: Points to Remove')
plt.scatter(x_in, y_in, c='k', marker='.', alpha=.5, label='1')
plt.scatter(x_poi, y_poi, c='b', marker='D', s=50, label='-1')
plt.scatter(x_filter, y_filter, c='r', marker='+', alpha=0.3, label='0')
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
