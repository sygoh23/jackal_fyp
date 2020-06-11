import math
import numpy as np
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from utils import *


def select_ped_no_building(total_ped, i):
    reached_target = 0
    send_goal = 0
    goal_xy = [0, 0]
    robot_xy = get_robot_xy()

    ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    dist = [] # Distance to target (always +ve, lower = better)
    vel = [] # Velocity towards target (-ve = distance decreasing, +ve = distance increasing)
    robot_dist = []
    
    # Calculate pedestrian distances and velocities:
    print("PEDESTRIANS:")
    for j in range(total_ped):
        ped_xy = [ped.agent_states[j].pose.position.x, ped.agent_states[j].pose.position.y]
        dist_robot_ped = math.sqrt((robot_xy[0]-ped_xy[0])**2+(robot_xy[1]-ped_xy[1])**2)

        dist.append(math.sqrt((target_xy[0]-ped_xy[0])**2+(target_xy[1]-ped_xy[1])**2)) # Distance
        robot_dist.append(dist_robot_ped)

        if i > 0:
            vel.append((dist[j]-dynamic_params.dist_last[j])/t_delay) # Velocity
            print("- Ped: %d | Pose: (%.1f, %.1f) | Dist (Target): %.1f | Vel (Target): %.1f | Dist (Robot): %.1f" % (j, ped_xy[0], ped_xy[1], dist[j], vel[j], dist_robot_ped))
    dynamic_params.dist_last = dist # Save distance for next iteration

    # Process pedestrian information:
    dist_sort = sorted(dist) # Sort distance (ascending)
    dist_index = np.argsort(dist) # Index of sorted distance (ascending)
    vel_sort = sorted(vel) # Sort velocity (ascending)
    best_ped_dist = dist_index[0] # Best pedestrian based on distance
    best_ped_vel = dist_index[0] # Best pedestrian based on velocity

    
    # Selecting the best pedestrian:
    if i > 0:
        # Start by finding the best pedestrian:
        best_ped_smart = best_ped_dist
        # Loop through pedestrians from closest to furthest from target...
        for index in dist_index:
            # Only consider ped if within range of robot
            if robot_dist[index] < robot_range:
                if vel[index] < 0:
                # If their velocity is -ve (distance is decreasing)...
                    best_ped_smart = index # They are the best pedestrian!!!
                    dist_robot_ped = robot_dist[index]
                    break
    

        # Pedestrian selection summary:
        print("\nSELECTION:")
        print("- Based on distance: Ped %d @ %.1fm distance from target..." % (best_ped_dist, dist_sort[0]))
        print("- Based on velocity: Ped %d @ %.1fm/s velocity towards target..." % (best_ped_vel, -vel_sort[0]))
        print("- Based on combination: Ped %d @ minimum distance AND moving towards target..." % (best_ped_smart))
        best_ped = best_ped_smart

        # Robot logic:
        print("\nROBOT:")
        goal_xy = [ped.agent_states[best_ped].pose.position.x, ped.agent_states[best_ped].pose.position.y]
        dist_robot_target = math.sqrt((robot_xy[0]-target_xy[0])**2+(robot_xy[1]-target_xy[1])**2)

        # It does need an if statement in case there are no pedestrians in range
        # Do not follow if ped is further away than robot
        dynamic_params.dist_ped_target_last = dist[best_ped_smart]
        send_goal = 1
        print("- Following: Ped %d @ %.1fm from pedestrian and %.1fm from target..." % (best_ped, dist_robot_ped, dist_robot_target))
       
        """
        # Make sure the best pedestrian is closer to target than last goal:
        if dist[best_ped_smart] < dynamic_params.dist_ped_target_last:
            dynamic_params.dist_ped_target_last = dist[best_ped_smart]
            # If the best pedestrian is closer to target:
            send_goal = 1
            print("- Following: Ped %d @ %.1fm from pedestrian and %.1fm from target..." % (best_ped, dist_robot_ped, dist_robot_target))
        else:
            # If the best pedestrian is further away, don't send a navigaiton goal:
            print("- Waiting for a pedestrian closer to the target. Robot @ %.fm from target... " % dist_robot_target)
        """

        if dist_robot_target < 2:
            reached_target = 1
    else:
        print("- Please wait for the next iteration...")
    
    return (goal_xy, send_goal, reached_target)