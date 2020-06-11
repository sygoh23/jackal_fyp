#!/usr/bin/env python
# V5: Follows pedestrians based on distance and velocity.
import rospy
import random
import time
import math
import actionlib
import numpy as np
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
from ped_selection import *
from utils import *


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server() # Waits until the action server has started up:
    total_peds = get_total_peds()
    print("Delay: %d | Iterations: %d | Target: (%d, %d)" % (t_delay, n_loop, target_xy[0], target_xy[1]))

    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)
        goal_xy, send_goal, reached_target = select_ped_no_building(total_peds, i)

        # Send navigation goal to navigation stack:
        if send_goal == 1:
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "odom"
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = goal_xy[0]
            goal.target_pose.pose.position.y = goal_xy[1]
            goal.target_pose.pose.orientation.w = 1.0
            client.send_goal(goal)
        if reached_target == 1:
            print("- Robot navigation complete!")
            break
        print("----------------------------------------------------------")
        time.sleep(t_delay)


# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        result = movebase_client()
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
