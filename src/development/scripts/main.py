#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from ped_selection import select_ped_within_vicinity, select_ped_outside_vicinity
from utils import *


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    total_peds = get_total_peds()

    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)
        robot_xy = get_robot_xy()
        dist_robot_building_center = get_distance(robot_xy[0], building_center_xy[0], robot_xy[1], building_center_xy[1])

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity
        if dist_robot_building_center < building_threshold:
            print("Within building vicinity")
            select_ped_within_vicinity()
        else:
            print("Outside building vicinity")
            goal_xy, ped_found = select_ped_outside_vicinity(total_peds, i)

            # If no suitable peds detected, just move 5 metres in a straight line towards building center (or could move to last detected pedestrian position?)
            if ped_found == 0:
                goal_xy = get_straight_line_pos("building_center", 5)
                time.sleep(t_delay) # allow some more time for robot to finish its previous straight line movement
                
        # Send navigation goal to navigation stack:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "odom"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = goal_xy[0]
        goal.target_pose.pose.position.y = goal_xy[1]
        goal.target_pose.pose.orientation.w = 1.0
        client.send_goal(goal)

        if dynamic_params.reached_target == 1:
            print("- Robot navigation complete!")
            break

        print("----------------------------------------------------------")
        time.sleep(t_delay)


if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
