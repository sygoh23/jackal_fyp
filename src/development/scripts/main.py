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
from static_params import *
from ped_selection import *
from utils import *


"""
Ideas:

--> Map out a bounding box for each building to use as the building vicinity, circular radius method probably won't work. Would then need an area-checking method
--> Ped selection within building vicinity: follow a random pedestrian, move along edge of building
--> Stop navigation if robot is stuck driving into a wall
"""


def no_peds_movement():
    print("- Moving towards building center...")
    dynamic_params.goal_xy = get_straight_line_pos("building_center", straight_line_dist)
    
    # If function call was triggered because of the timer, reset the timer flag
    if dynamic_params.timer_set == 1:
        dynamic_params.timer_set = 0
    
    # If function call was triggered because robot has reached last detected pedestrian, reset the moving_to_last_ped flag
    if dynamic_params.moving_to_last_ped == 1:
        dynamic_params.moving_to_last_ped = 0


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

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
            ped_found = select_ped_outside_vicinity(i)

            # If no suitable peds detected, choose movement logic
            if ped_found == 0:

                # A last detected ped exists (list is non-empty)
                if dynamic_params.ped_last:
                    print("- Moving to last detected pedestrian...")
                    dynamic_params.goal_xy = dynamic_params.ped_last    # Set goal as last pedestrian position
                    dynamic_params.ped_last = []                        # Clear the last pedestrian position
                    dynamic_params.moving_to_last_ped = 1               # Set flag indicating robot is moving to location of last detected ped
                
                # No last detected ped exists AND not in the middle of moving towards a last detected ped
                elif dynamic_params.moving_to_last_ped == 0:
                    dist_robot_straight_line_goal = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
                    
                    # Reached target point
                    if dist_robot_straight_line_goal <= target_threshold:
                        # Waiting for timer to trigger and begin the next movement, or a new ped to be detected
                        if dynamic_params.timer_set == 1:
                            print("- Waiting for new peds...")
                        else:
                            timer = Timer(movement_pause, no_peds_movement)     # Create new countdown timer for no_peds_movement
                            timer.start()                                       # Start timer
                            dynamic_params.timer_set = 1                        # Set timer flag
                    
                    # In the middle of moving towards the previously set target point
                    else:
                        print("- Moving towards building center...")
                else:
                    # Reached last ped position and waiting for timer to trigger
                    if dynamic_params.timer_set == 1:
                        print("- Waiting for new peds...")
                    
                    # In the middle of moving towards a last detected ped
                    else:
                        print("- Moving to last detected pedestrian...")

                        # Check if robot has reached position of last detected ped
                        dist_robot_last_ped = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
                        if dist_robot_last_ped <= target_threshold:
                            print("- Reached last detected pedestrian\n- Waiting for new peds...")
                            timer = Timer(movement_pause, no_peds_movement)     # Create new countdown timer for no_peds_movement
                            timer.start()                                       # Start timer
                            dynamic_params.timer_set = 1                        # Set timer flag
            else:
                # Ped found. Reset moving_to_last_ped flag if it was set
                if dynamic_params.moving_to_last_ped == 1:
                    print("- New pedestrian detected, following...")
                    dynamic_params.moving_to_last_ped = 0

                # Ped found. Cancel timer if it is counting down
                elif dynamic_params.timer_set == 1:
                    print("- New pedestrian detected, following...")
                    timer.cancel()
                    dynamic_params.timer_set = 0
                

                
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
