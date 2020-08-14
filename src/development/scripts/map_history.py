import matplotlib.pyplot as plt
from math import sqrt
dist_threshold = 3

# Returns distance between two sets of x-y coordinates
def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Open files:
x_in = []; y_in = []
x_pth = "/home/ubuntu/Mapping/x.txt"; y_pth = "/home/ubuntu/Mapping/y.txt"
with open(x_pth, 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        x_in.append(float(line[:-1]))

with open(y_pth, 'r') as filehandle:
    filecontents = filehandle.readlines()
    for line in filecontents:
        y_in.append(float(line[:-1]))

# Clean points which are too close to each other:
x_out = x_in; y_out = y_in
print("Cleaning points:\n- Original Length: " + str(len(x_out)))
i = 0
while i < (len(x_out)-1):
    dist = get_distance(x_in[i], x_in[i+1], y_in[i], y_in[i+1])
    if dist < dist_threshold:
        del_i = i + 1; i = 0;
        del x_out[del_i]; del y_out[del_i]
    else:
        i += 1
print("- New Length: " + str(len(x_out)))
plt.scatter(x_out, y_out)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
