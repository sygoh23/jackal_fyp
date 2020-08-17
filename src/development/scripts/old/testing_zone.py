def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)
from math import sqrt

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
