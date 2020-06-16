"""
Contains helper functions for other parts of the program

--> Import this file as 'from utils import *', then all functions will be added to the file namespace
"""

from math import sqrt
from threading import Timer
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params


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


# Sets the robot goal as a specified number of metres towards the building center in a straight line
# Must be in a function so that it can be triggered by the timer
def straight_line_movement():
    print("- Moving towards building center...")
    dynamic_params.goal_xy = get_straight_line_pos("building_center", straight_line_dist)
    
    # If function call was triggered because of the timer, reset the timer flag
    if dynamic_params.timer_set == 1:
        dynamic_params.timer_set = 0
    
    # If function call was triggered because robot has reached last detected pedestrian, reset the moving_to_last_ped flag
    if dynamic_params.moving_to_last_ped == 1:
        dynamic_params.moving_to_last_ped = 0


"""
Used to set the robot navigation goal when no peds are found to follow

--> First sets the goal as the position of the last detected pedestrian
--> Once that goal is reached, it sets the goal as a specified number of metres in the straight-line direction of the building center
--> Upon reaching the straight-line goal, it sets a new straight-line goal
--> Straight-line goals are continually set until a) a pedestrian is found, or b) the target building vicinity is reached
--> Robot pauses between each movement section for a specified number of seconds, to wait for pedestrians to appear
--> Pedestrian scanning is continually taking place, and the robot will exit this 'no ped' behaviour as soon as a suitable pedestrian is found
--> The straight-line movement logic can be replaced with some other logic by editing straight_line_movement()
"""
def move_without_peds_outside_vicinity():
    robot_xy = get_robot_xy()

    # A last detected ped exists (list is non-empty)
    if dynamic_params.ped_last:
        print("- Moving to last detected pedestrian...")
        dynamic_params.goal_xy = dynamic_params.ped_last    # Set goal as last pedestrian position
        dynamic_params.ped_last = []                        # Clear the last pedestrian position
        dynamic_params.moving_to_last_ped = 1               # Set flag indicating robot is moving to location of last detected ped
    
    # No last detected ped exists AND the robot is not in the middle of moving towards a last detected ped
    elif dynamic_params.moving_to_last_ped == 0:
        dist_robot_straight_line_goal = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
        
        # Robot has reached the previously set straight-line goal
        if dist_robot_straight_line_goal <= target_threshold:
            # Start timer if not started already, and wait for a new ped to be detected
            print("- Waiting for new peds...")
            if dynamic_params.timer_set == 0:
                dynamic_params.timer = Timer(movement_pause, straight_line_movement)    # Create new countdown timer for straight_line_movement
                dynamic_params.timer.start()                                            # Start timer
                dynamic_params.timer_set = 1                                            # Set timer flag
        
        # Robot is in the middle of moving towards the previously set straight-line goal
        else:
            print("- Moving towards building center...")
    else:
        # Robot has reached the last ped position and is waiting for a new ped to be detected
        if dynamic_params.timer_set == 1:
            print("- Waiting for new peds...")
        
        # Robot is in the middle of moving towards the last detected ped
        else:
            print("- Moving to last detected pedestrian...")

            # Check if robot has reached the last ped position. If it has, then start the timer and wait
            dist_robot_last_ped = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
            if dist_robot_last_ped <= target_threshold:
                print("- Reached last detected pedestrian")
                dynamic_params.timer = Timer(movement_pause, straight_line_movement)    # Create new countdown timer for straight_line_movement
                dynamic_params.timer.start()                                            # Start timer
                dynamic_params.timer_set = 1                                            # Set timer flag