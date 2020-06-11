#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
from ped_selection import *
from utils import *

# May need to put navigation stack stuff within if statement
# No peds going to new horizons?
# Add code to keep moving when no peds are selected

def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    total_peds = get_total_peds()

    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)
        robot_xy = get_robot_xy()
        dist_robot_building = get_distance(robot_xy[0], building_center_xy[0], robot_xy[1], building_center_xy[1])

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity
        if dist_robot_building < building_threshold:
            pass
            # select_ped_within_vicinity()
        else:
            goal_xy, send_goal = select_ped_outside_vicinity(total_peds, i)

        # Send navigation goal to navigation stack:
        if send_goal == 1:
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "odom"
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = goal_xy[0]
            goal.target_pose.pose.position.y = goal_xy[1]
            goal.target_pose.pose.orientation.w = 1.0
            client.send_goal(goal)

        reached_target = 0 # temporary
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
