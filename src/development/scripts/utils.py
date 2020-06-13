"""
Contains helper functions

--> Import this file as 'from utils import *', then all functions will be added to the file namespace
"""

from math import sqrt
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *


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