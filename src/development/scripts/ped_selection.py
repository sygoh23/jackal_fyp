"""
Contains pedestrian selection logic

--> select_ped_within_vicinity(): used when the robot is within the building vicinity
--> select_ped_outside_vicinity(): used when the robot is outside the building vicinity
"""

import numpy as np
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from utils import *


# Selects a pedestrian when the robot is within the building vicinity
def select_ped_within_vicinity():
    pass
    # Follow a random ped, staying within vicinity
    # If no ped, try move forward but within vicinity, else move right within vicinity, else move left, ...
    # Continuously scan for doorways
    # This assumes there is only one doorway in the defined building vicinity


# Selects a pedestrian when the robot is outside the building vicinity
def select_ped_outside_vicinity(i):
    
    ##############################################
    ############### Initialization ###############
    ##############################################

    ped_found = 0                           # Flag for whether a suitable pedestrian to follow was found
    robot_xy = get_robot_xy()               # Robot current x-y position
    dist_ped_building_center_list = []      # Distance to building center (always +ve, lower = better)
    vel = []                                # Velocity towards building center (-ve = distance decreasing, +ve = distance increasing)
    dist_robot_ped_list = []                # List of distances between the robot and each pedestrian
    dist_robot_building_center = get_distance(robot_xy[0], building_center_xy[0], robot_xy[1], building_center_xy[1])   # Distance between robot and building center
    total_ped = get_total_peds()

    ###############################################
    ############### Data Collection ###############
    ###############################################

    ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    #print("PEDESTRIANS:")
    for j in range(total_ped):
        # Calculate distance between a) pedestrian and building center, b) robot and pedestrian
        ped_xy = [ped.agent_states[j].pose.position.x, ped.agent_states[j].pose.position.y]
        dist_ped_building_center = get_distance(building_center_xy[0], ped_xy[0], building_center_xy[1], ped_xy[1])
        dist_robot_ped = get_distance(robot_xy[0], ped_xy[0], robot_xy[1], ped_xy[1])

        dist_ped_building_center_list.append(dist_ped_building_center)
        dist_robot_ped_list.append(dist_robot_ped)

        # Calculate pedestrian velocity
        if i > 0:
            vel.append((dist_ped_building_center_list[j]-dynamic_params.dist_last[j])/t_delay)
            #print("- Ped: %d | Pose: (%.1f, %.1f) | Dist (Target): %.1f | Vel (Target): %.1f | Dist (Robot): %.1f" % (j, ped_xy[0], ped_xy[1], dist_ped_building_center_list[j], vel[j], dist_robot_ped))
    
    dynamic_params.dist_last = dist_ped_building_center_list # Save distance for next iteration
    dist_index = np.argsort(dist_ped_building_center_list)   # Indices of pedestrians, from closest to furthest from building center


    ###################################################
    ############### Ped Selection Logic ###############
    ###################################################

    # Pedestrian selection only after first iteration
    if i > 0:
        # Start by assuming there are no suitable peds to follow
        no_peds = True

        # Loop through pedestrians from closest to furthest from building center
        for idx in dist_index:

            # Only follow a pedestrian if it is within range of robot (i.e. simulate the fact that we can only detect pedestrians in our immediate vicinity in real life)
            if dist_robot_ped_list[idx] < robot_range:
                
                # Only follow a pedestrian if they are closer to the building center than the robot currently is
                if dist_robot_building_center > dist_ped_building_center_list[idx]:
                
                    # Only follow a pedestrian if their velocity is -ve (distance is decreasing)
                    if vel[idx] < 0:
                        best_ped_smart = idx
                        dist_robot_ped = dist_robot_ped_list[idx]
                        no_peds = False
                        break
    
        # Update navigation goal if the selection logic found a pedestrian to follow
        if not no_peds:
            print("\nRESULTS:")
            print("- Following: Ped %d @ %.1fm from pedestrian and %.1fm from building center..." % (best_ped_smart, dist_robot_ped, dist_robot_building_center))
            dynamic_params.goal_xy = [ped.agent_states[best_ped_smart].pose.position.x, ped.agent_states[best_ped_smart].pose.position.y]
            dynamic_params.ped_last = dynamic_params.goal_xy
            ped_found = 1
        else:
            print("\nRESULTS:")
            print("- Did not find a pedestrian to follow")

    #else:
        #print("- Please wait for the next iteration...")
    
    return ped_found