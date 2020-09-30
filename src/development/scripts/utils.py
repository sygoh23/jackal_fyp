"""
Contains helper functions for other parts of the program.
Import this file as 'from utils import *', then all functions will be added to the file namespace.
"""

from math import sqrt, sin, cos
import matplotlib.path as mpltPath
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

# Updates the map file
def update_map():
    plt.clf()
    plt.grid(b=True, which='major', color='#d6d6d6', linestyle='--')
    plt.scatter(dynamic_params.remove_x, dynamic_params.remove_y, c='y', marker='x', s=50, label='0')
    plt.plot(dynamic_params.hist_x, dynamic_params.hist_y, c='c', alpha=0.5, label='1')
    plt.scatter(dynamic_params.poi_x, dynamic_params.poi_y, c='b', marker='D', s=25, label='-1')
    #plt.scatter(dynamic_params.robot_xy[0], dynamic_params.robot_xy[1], c='b', marker='x', s=50)
    plt.scatter(dynamic_params.goal_xy[0], dynamic_params.goal_xy[1], c='fuchsia', marker='x', s=50)
    plt.scatter(dynamic_params.robot_xy[0], dynamic_params.robot_xy[1], c='k', marker='h', s=50)
    plt.scatter(dynamic_params.cloud_x, dynamic_params.cloud_y, c='dimgray', marker='.', s=10)
    plt.scatter(dynamic_params.ped_x_excl, dynamic_params.ped_y_excl, c='r', marker='.', s=20)
    plt.scatter(dynamic_params.ped_x_los, dynamic_params.ped_y_los, c='g', marker='.', s=30)
    plt.xlim((dynamic_params.robot_xy[0]-dynamic_params.map_range, dynamic_params.robot_xy[0]+dynamic_params.map_range))
    plt.ylim((dynamic_params.robot_xy[1]-dynamic_params.map_range, dynamic_params.robot_xy[1]+dynamic_params.map_range))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(simulation_setup.map_pth)


# Sets up a move base goal object to be sent to client
def setup_goal(x,y):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "odom"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0
    return goal


# Checks if pedestrian is in a zone removed by recovery behaviour
def ped_in_remove_zone(ped_coord):
    outcome = False
    for j in range(len(dynamic_params.remove_x)):
        dist = get_distance(ped_coord[0], dynamic_params.remove_x[j], ped_coord[1], dynamic_params.remove_y[j])
        if dist < dynamic_params.remove_radius:
            outcome = True
            break
    return outcome

# Checks if pedestrian is in robot recent history
def ped_in_recent_hist(ped_coord, recent_radius):
    outcome = False
    for j in range(len(dynamic_params.recent_x)):
        dist = get_distance(ped_coord[0], dynamic_params.recent_x[j], ped_coord[1], dynamic_params.recent_y[j])
        if dist < recent_radius:
            outcome = True
            break
    return outcome

# Extracts x/y/z coordinates from point cloud
def extract_xyz(list, num):
    return [item[num] for item in list]


# Returns the total number of pedsim pedestrians
def get_total_peds():
    peds = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    return len(peds.agent_states)


# Returns robot current x-y position
def get_robot_xy():
    odom = rospy.wait_for_message("/odometry/filtered", Odometry)
    return [odom.pose.pose.position.x, odom.pose.pose.position.y]


# Returns distance between two sets of x-y coordinates
def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Finds constants for linear equation given 2 coordinates
def linear_const(x1, x2, y1, y2):
    return (y1-y2), (x2-x1), (x1*y2-x2*y1)

# Finds minimum linear distance from linear equation using constants
def linear_dist(A, B, C, x, y):
    return abs(A*x+B*y+C)/sqrt(A**2+B**2)

# Returns the x-y coordinate that is d metres in the straight line direction of the specified target
def get_straight_line_pos(target, d):
    # Set target
    if target == "building_center":
        target_xy = building_center_xy
    elif target == "building_entrance":
        target_xy = building_entrance_xy
    else:
        print("Error - invalid parameter in get_straight_line_pos()")

    robot_xy = get_robot_xy()
    dist_robot_target = get_distance(robot_xy[0], target_xy[0], robot_xy[1], target_xy[1])

    # Unit vector in direction of target
    unit_x = (target_xy[0] - robot_xy[0])/dist_robot_target
    unit_y = (target_xy[1] - robot_xy[1])/dist_robot_target

    return [robot_xy[0] + d*unit_x, robot_xy[1] + d*unit_y]

# Check if a point is within a circle
def inside_radius(x0, y0, r, x_in, y_in):
    return (x_in-x0)**2+(y_in-y0)**2<=r**2

# Checks if a given point pt is contained within a given polygon A
def contains_pt(pt, A):
    path = mpltPath.Path(A)
    return path.contains_point(pt)


# Parses and returns velodyne point cloud data in a list. Each element of the list is a tuple (x, y, z) indicating a particular point in the point cloud
def get_pointcloud():
    data = rospy.wait_for_message("/velodyne_points2", PointCloud2)
    generator = point_cloud2.read_points(data, field_names = ("x", "y", "z"), skip_nans=True)
    points_list = []
    for point in generator:
        points_list.append(point)
    return points_list


# Generates a square polygon of side length L centered around point pt
def generate_zone(pt, L):
    L = float(L)
    return np.array([
        [pt[0]-L/2, pt[1]-L/2],
        [pt[0]+L/2, pt[1]-L/2],
        [pt[0]+L/2, pt[1]+L/2],
        [pt[0]-L/2, pt[1]+L/2],
        [pt[0]-L/2, pt[1]-L/2]
    ])


# Rotates a point counterclockwise by a given angle around a given origin
# The angle should be given in radians, and all points as (x, y) tuples
def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy
