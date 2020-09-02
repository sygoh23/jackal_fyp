"""
Contains pedestrian selection logic.
select_ped_within_vicinity(): used when the robot is within the building vicinity.
select_ped_outside_vicinity(): used when the robot is outside the building vicinity.
"""

import numpy as np
import rospy
from pedsim_msgs.msg import AgentStates
from static_params import *
import dynamic_params
from utils import *

def ped_in_remove_zone(ped_coord):
    outcome = False
    for j in range(len(dynamic_params.remove_x)):
        dist = get_distance(ped_coord[0], dynamic_params.remove_x[j], ped_coord[1], dynamic_params.remove_y[j])
        if dist < dynamic_params.remove_radius:
            outcome = True
            break
    return outcome

"""
Selects a pedestrian to follow when the robot is within the building vicinity
--> Assumes there is only one doorway in the defined building vicinity
--> Currently doesn't use pedestrians at all, but kept the name because following pedestrians may be a better option. Depends how well the current idea performs
"""
def select_ped_within_vicinity():

    # While the goal point is outside the building vicinity
    while not contains_pt(dynamic_params.goal_xy, building_polygon):
        print("--> Current goal is outside vicinity, generating new goal...")

        # Generate new goal point that is close to a wall, and in the direction of the target
        pointcloud = get_pointcloud()

    print("--> Looking for doorway")

# Selects a pedestrian when the robot is outside the building vicinity, based on which movement phase the robot is in
# Phase = 1: select pedestrian based on rigorous conditions
# Phase = 3: select pedestrian closest to robot
def select_ped_outside_vicinity(phase, i):

    ##############################################
    ############### Initialization ###############
    ##############################################

    ped_found = 0                           # Flag for whether a suitable pedestrian to follow was found (1) or not (0). Init to 0 to assume there are no peds
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

    # If in movement phase 1, we want to follow the best pedestrian
    if phase == 1:
        # Pedestrian selection only after first iteration
        if i > 0:

            # Loop through pedestrians from closest to furthest from building center
            for idx in dist_index:

                # Only follow a pedestrian if it is within range of robot (i.e. simulate the fact that we can only detect pedestrians in our immediate vicinity in real life)
                if dist_robot_ped_list[idx] < robot_range:
                    #dynamic_params.debug_please.append("A")

                    # Only follow a pedestrian if it is not within the problem area outside eng faculty (usually not needed, but there are situations where if the navigation is started at a poor time the algorithm can fail)
                    # Recovery behaviour extra - make sure pedestrian is not in a removed zone.
                    ped_coord = [ped.agent_states[idx].pose.position.x, ped.agent_states[idx].pose.position.y]
                    #if not contains_pt(ped_coord, dynamic_params.exclusion_zones[0]):
                    if (not contains_pt(ped_coord, dynamic_params.exclusion_zones[0])) and (not ped_in_remove_zone(ped_coord)):
                        # Only follow a pedestrian if it is not in the dynamically created exclusion zone around the robot's starting point
                        if (not contains_pt(ped_coord, dynamic_params.exclusion_zones[1])) or (contains_pt(robot_xy, dynamic_params.exclusion_zones[1])):

                            # Only follow a pedestrian if they are closer to the building center than the robot currently is
                            if dist_robot_building_center > dist_ped_building_center_list[idx]:

                                # Only follow a pedestrian if their velocity is -ve (distance is decreasing)
                                if vel[idx] < 0:
                                    best_ped_smart = idx
                                    dist_robot_ped = dist_robot_ped_list[idx]
                                    ped_found = 1
                                    #dynamic_params.debug_please.append("B")
                                    break

            # Update navigation goal if the selection logic found a pedestrian to follow
            if ped_found:
                print("- Phase 1: Following ped %d:" % (best_ped_smart))
                print("--- Ped %d is %.2fm from the robot" % (best_ped_smart, dist_robot_ped))
                print("--- Ped %d is %.1fm from the building center" % (best_ped_smart, dist_robot_building_center))
                dynamic_params.goal_xy = [ped.agent_states[best_ped_smart].pose.position.x, ped.agent_states[best_ped_smart].pose.position.y]
                dynamic_params.ped_last = dynamic_params.goal_xy
            else:
                print("- Phase 1: Did not find a pedestrian to follow")
                best_ped_smart = 8725
                #dynamic_params.debug_please.append("C")

        else:
            print("- Please wait for the next iteration...")
            best_ped_smart = 8725       # junk, will not be used. Just need to set it to something
            #dynamic_params.debug_please.append("D")

    # If in movement phase 3, we simply want to follow the closest pedestrian to the robot and ignore other conditions
    elif phase == 3:

        # Loop through pedestrians from closest to furthest from building center
        for idx in dist_index:

            # Only follow a pedestrian if it is within range of robot but not already within the threshold (otherwise the program will believe the robot has already reached the goal and will reset for another loop)
            if (dist_robot_ped_list[idx] < robot_range) and (dist_robot_ped_list[idx] > target_threshold):

                # Only follow a pedestrian if it is not within the problem area outside eng faculty (usually not needed, but there are situations where if the navigation is started at a poor time the algorithm can fail)
                ped_coord = [ped.agent_states[idx].pose.position.x, ped.agent_states[idx].pose.position.y]
                #if not contains_pt(ped_coord, dynamic_params.exclusion_zones[0]):
                if (not contains_pt(ped_coord, dynamic_params.exclusion_zones[0])) and (not ped_in_remove_zone(ped_coord)):
                    #dynamic_params.debug_please.append("E")

                    # Only follow a pedestrian if it is not in the dynamically created exclusion zone around the robot's starting point
                    if (not contains_pt(ped_coord, dynamic_params.exclusion_zones[1])) or (contains_pt(robot_xy, dynamic_params.exclusion_zones[1])):
                        #dynamic_params.debug_please.append("F")

                        # Only follow a pedestrian if they are closer to the robot than the previously checked pedestrian
                        if ped_found == 0:  # found the first potential ped, so there is no previous ped to compare to
                            best_ped_smart = idx
                            dist_robot_ped = dist_robot_ped_list[idx]
                            ped_found = 1
                            #dynamic_params.debug_please.append("G")
                        else:
                            if dist_robot_ped_list[idx] < dist_robot_ped:
                                best_ped_smart = idx
                                dist_robot_ped = dist_robot_ped_list[idx]
                            #dynamic_params.debug_please.append("H")

        # Update navigation goal if the selection logic found a pedestrian to follow
        if ped_found:
            print("- Phase 3: Following ped %d @ %.1fm from pedestrian and %.1fm from building center" % (best_ped_smart, dist_robot_ped, dist_robot_building_center))
            dynamic_params.goal_xy = [ped.agent_states[best_ped_smart].pose.position.x, ped.agent_states[best_ped_smart].pose.position.y]
            #dynamic_params.ped_last = dynamic_params.goal_xy
            #dynamic_params.debug_please.append("I")

        else:
            print("- Phase 3: Did not find a pedestrian to follow")
            best_ped_smart = 8725   # junk, won't be used. Just need to set it to something
            #dynamic_params.debug_please.append("J")

    else:
        print("ERR: select_ped_outside_vicinity(): phase must be 1 or 3")
        #dynamic_params.debug_please.append("K")

    return ped_found, best_ped_smart
