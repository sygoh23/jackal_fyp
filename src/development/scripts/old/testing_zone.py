def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)
from math import sqrt
import math
import matplotlib
import matplotlib.pyplot as plt

# rec_x = 20
# rec_y = 10
# robot_xy = [35, 50]
# rec_d = get_distance(rec_x, robot_xy[0], rec_y, robot_xy[1])
# rec_goal_x = rec_x
# rec_goal_y = rec_y
# rec_goal_d = rec_d
# if rec_d > 10:
#     while (rec_goal_d > 10):
#         rec_goal_x = (rec_goal_x + robot_xy[0]) / 2
#         rec_goal_y = (rec_goal_y + robot_xy[1]) / 2
#         rec_goal_d = get_distance(rec_goal_x, robot_xy[0], rec_goal_y, robot_xy[1])
#
# print(rec_goal_x)
# print(rec_goal_y)
x_remove = [20, 20, 20]
y_remove = [50, -20, 30]

x_radius = []
y_radius = []
for i in range(len(x_remove)):
    x_now = x_remove[i]
    y_now = y_remove[i]
    x_radius.append(x_now)
    y_radius.append(y_now)
    for j in range(45):
        for k in range(5):
            x_radius.append(x_now+2*k*math.sin(8*j*math.pi/180))
            y_radius.append(y_now+2*k*math.cos(8*j*math.pi/180))
print(len(x_radius))
print(len(y_radius))

plt.scatter(x_radius, y_radius, c='r', marker='.', s=50, alpha=0.2, label='0')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
