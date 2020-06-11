import numpy as np
import rospy
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from utils import *

# Change references to 'target' and the like to 'building vicinity'

def select_ped_within_vicinity():
    pass


def select_ped_outside_vicinity(total_ped, i):
    send_goal = 0
    goal_xy = [0, 0]
    robot_xy = get_robot_xy()
    dist_ped_target_list = []   # Distance to target (always +ve, lower = better)
    vel = []                    # Velocity towards target (-ve = distance decreasing, +ve = distance increasing)
    dist_robot_ped_list = []
    dist_robot_target = get_distance(robot_xy[0], building_center_xy[0], robot_xy[1], building_center_xy[1])
    
    # Calculate pedestrian distances and velocities:
    ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    print("PEDESTRIANS:")
    for j in range(total_ped):
        ped_xy = [ped.agent_states[j].pose.position.x, ped.agent_states[j].pose.position.y]
        dist_ped_target = get_distance(building_center_xy[0], ped_xy[0], building_center_xy[1], ped_xy[1])
        dist_robot_ped = get_distance(robot_xy[0], ped_xy[0], robot_xy[1], ped_xy[1])

        dist_ped_target_list.append(dist_ped_target)
        dist_robot_ped_list.append(dist_robot_ped)

        if i > 0:
            vel.append((dist_ped_target_list[j]-dynamic_params.dist_last[j])/t_delay)
            print("- Ped: %d | Pose: (%.1f, %.1f) | Dist (Target): %.1f | Vel (Target): %.1f | Dist (Robot): %.1f" % (j, ped_xy[0], ped_xy[1], dist_ped_target_list[j], vel[j], dist_robot_ped))
    dynamic_params.dist_last = dist_ped_target_list # Save distance for next iteration
    dist_index = np.argsort(dist_ped_target_list)   # Indices of pedestrians, from closest to furthest from target

    # Pedestrian selection only after first iteration
    if i > 0:
        # Start by assuming there are no suitable peds to follow
        no_peds = True

        # Loop through pedestrians from closest to furthest from target
        for idx in dist_index:

            # Only follow a pedestrian if it is within range of robot
            if dist_robot_ped_list[idx] < robot_range:
                
                # Only follow a pedestrian if they are closer to the target than the robot currently is
                if dist_robot_target > dist_ped_target_list[idx]:
                
                    # Only follow a pedestrian if their velocity is -ve (distance is decreasing)...
                    if vel[idx] < 0:
                        best_ped_smart = idx # They are the best pedestrian!!!
                        dist_robot_ped = dist_robot_ped_list[idx]
                        no_peds = False
                        break
    
        # Only send a navigation goal if the selection logic found a suitable pedestrian to follow
        if not no_peds:
            # Selection summary:
            print("\nRESULTS:")
            #print("- Based on distance: Ped %d @ %.1fm distance from target..." % (best_ped_dist, dist_sort[0]))
            #print("- Based on velocity: Ped %d @ %.1fm/s velocity towards target..." % (best_ped_vel, -vel_sort[0]))
            #print("- Based on combination: Ped %d @ minimum distance AND moving towards target..." % (best_ped_smart))
            print("- Following: Ped %d @ %.1fm from pedestrian and %.1fm from target..." % (best_ped_smart, dist_robot_ped, dist_robot_target))
            #best_ped = best_ped_smart

            goal_xy = [ped.agent_states[best_ped_smart].pose.position.x, ped.agent_states[best_ped_smart].pose.position.y]
            send_goal = 1
        else:
            print("\nRESULTS\n- Did not find a pedestrian to follow...")

    else:
        print("- Please wait for the next iteration...")
    
    return (goal_xy, send_goal)