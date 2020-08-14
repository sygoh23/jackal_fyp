import matplotlib.pyplot as plt
from math import sqrt
min_dist = 10
max_dev = 5
x_pth = "/home/ubuntu/Mapping/x.txt";
y_pth = "/home/ubuntu/Mapping/y.txt"

# Returns distance between two sets of x-y coordinates
def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def linear_ABC(x1, x2, y1, y2):
        return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
        dist = abs(A*x+B*y+C)/sqrt(A**2+B**2)
        return dist

# Open files:
x_in = []; y_in = []
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
    if dist < min_dist:
        del_i = i + 1; i = 0;
        del x_out[del_i]; del y_out[del_i]
    else:
        i += 1
print("- New Length: " + str(len(x_out)) + "\n")

# Check points distance from a line:
print("Segment detection:")
poi = []
i = 0
j = 2
length = len(x_out)
segment = 1

while segment == 1:
    print("- Checking Segment from: " + str(i) + " -> " + str(j))
    const = linear_ABC(x_in[i], x_in[j], y_in[i], y_in[j])

    for k in range(i+1, j):
        d = linear_dist(const[0], const[1], const[2], x_in[k], y_in[k])
        print("-- Point: " + str(k) + " | Distance: " + str(d))
        if d > max_dev:
            poi.append(k+1)
            print("-- Critical Point:" + str(k+1))
            i = k + 1
            j = k + 3
            break
        j += 1

    if j == (len(x_out)-1):
        break

    if i == (len(x_out)-1):
        break

x_poi = [x_out[i] for i in poi]
y_poi = [y_out[i] for i in poi]

plt.scatter(x_out, y_out, c='b', marker='x', label='1')
plt.scatter(x_poi, y_poi, c='r', marker='s', label='-1')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
