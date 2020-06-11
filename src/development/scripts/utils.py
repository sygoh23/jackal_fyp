from math import sqrt
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry

def get_total_peds():
    peds = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    return len(peds.agent_states)

def get_robot_xy():
    odom = rospy.wait_for_message("/odometry/filtered", Odometry)
    return [odom.pose.pose.position.x, odom.pose.pose.position.y]

def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)