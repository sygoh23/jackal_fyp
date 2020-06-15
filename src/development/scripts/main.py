#!/usr/bin/env python
import time
from threading import Timer
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from ped_selection import *
from utils import *


"""
Ideas:

--> When robot is outside building vicinity and no peds are detected, first move to last detected pedestrian position, and then start moving towards building center
--> Map out a bounding box for each building to use as the building vicinity, circular radius method probably won't work. Would then need an area-checking method
--> Ped selection within building vicinity: follow a random pedestrian, move along edge of building
--> Stop navigation if robot is stuck driving into a wall
"""


def test():
    print("- Timer finished, still no peds detected, starting straight line movement")
    dynamic_params.goal_xy = get_straight_line_pos("building_center", 5)
    dynamic_params.timer_set = 0


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    total_peds = get_total_peds()
    timer = Timer(20, test)    # Initialise the timer to begin straight line movement

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
            ped_found = select_ped_outside_vicinity(total_peds, i)

            # If no suitable peds detected, just move 5 metres in a straight line towards building center
            if ped_found == 0:
                
                # Set a timer that starts straight line movement after x seconds, giving time for the robot to finish moving to last ped location
                # The timer should allow ped detection to still occur
                # If a ped is found, reset everything
                # If a ped still isn't found and the timer has expired, start straight line movement

                # Check if a last selected ped exists (i.e. is list NOT empty)
                if dynamic_params.ped_last:
                    print("- Moving to location of last selected pedestrian")
                    dynamic_params.goal_xy = dynamic_params.ped_last   # Set goal as last pedestrian position
                    dynamic_params.ped_last = []        # Clear the last pedestrian position
                    timer = Timer(20, test)              # Create a new timer to begin straight line movement
                    timer.start()                       # Start the new timer
                    dynamic_params.timer_set = 1        # Set the timer flag
                
                # If last selected ped does not exist, AND the timer has not been set (indicating the robot is stationary, not moving towards the last ped position)
                # THEN start straight line movement
                elif dynamic_params.timer_set == 0:
                    print("- No last selected ped, and not in the middle of moving toward last ped position. Starting straight line movement")
                    dynamic_params.goal_xy = get_straight_line_pos("building_center", 5)
                else:
                    print("- Moving to location of last selected pedestrian (else statement)")
            else:
                # Ped found. Cancel the timer if it is running
                if dynamic_params.timer_set == 1:
                    print("- Ped found, cancelling timer and following new ped")
                    timer.cancel()
                    dynamic_params.timer_set == 0

                
        # Send navigation goal to navigation stack:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "odom"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = dynamic_params.goal_xy[0]
        goal.target_pose.pose.position.y = dynamic_params.goal_xy[1]
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
