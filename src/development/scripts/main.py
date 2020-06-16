#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from static_params import *
from ped_selection import *
from utils import *


"""
Ideas:

--> Map out a bounding box for each building to use as the building vicinity, circular radius method probably won't work. Would then need an area-checking method
--> Ped selection within building vicinity: follow a random pedestrian, move along edge of building
--> Stop navigation if robot is stuck driving into a wall
"""


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    i = 0

    while True:
        print("\n\n------------------------- i = %d -------------------------" % i)
        robot_xy = get_robot_xy()
        dist_robot_building_center = get_distance(robot_xy[0], building_center_xy[0], robot_xy[1], building_center_xy[1])

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity
        if dist_robot_building_center < building_threshold:
            print("Within building vicinity")
            select_ped_within_vicinity()
        else:
            print("Outside building vicinity")
            ped_found = select_ped_outside_vicinity(i)

            # Manually set robot goal if a pedestrian was not found by the ped selection logic
            if ped_found == 0:
                move_without_peds_outside_vicinity()
            else:
                # Reset moving_to_last_ped flag if it was set
                if dynamic_params.moving_to_last_ped == 1:
                    dynamic_params.moving_to_last_ped = 0

                # Cancel timer if it is counting down
                elif dynamic_params.timer_set == 1:
                    dynamic_params.timer.cancel()
                    dynamic_params.timer_set = 0
                
        # Send navigation goal to navigation stack:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "odom"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = dynamic_params.goal_xy[0]
        goal.target_pose.pose.position.y = dynamic_params.goal_xy[1]
        goal.target_pose.pose.orientation.w = 1.0
        client.send_goal(goal)

        # Exit program if target is reached
        if dynamic_params.reached_target == 1:
            print("- Robot navigation complete!")
            break

        print("----------------------------------------------------------")
        i += 1
        time.sleep(t_delay)


if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
