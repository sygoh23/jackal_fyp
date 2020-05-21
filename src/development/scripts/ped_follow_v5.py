#!/usr/bin/env python
# V5: Follows pedestrians based on distance and velocity.
import rospy
import random
import time
import math
import actionlib
import numpy as np
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry

def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server() # Waits until the action server has started up:

    # Set final destination:
    # Building 1: (54,39)
    # Building 2: (54,-21)
    target_xy = [165, 65]

    # Determine number of pedestrians:
    ped_init = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    total_ped = len(ped_init.agent_states)

    # Following parameters:
    n_loop = 10000 # Number of following iterations
    t_delay = 1 # Time between iterations (lower = more responsive)
    print("Delay: %d | Iterations: %d | Target: (%d, %d)" % (t_delay, n_loop, target_xy[0], target_xy[1]))
    dist_last = [] # Last reported distance
    dist_ped_target_last = 100000 # Last distance from robot to target
    send_goal = 0
    reached_target = 0

    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)
        ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
        dist = [] # Distance to target (always +ve, lower = better)
        vel = [] # Velocity towards target (-ve = distance decreasing, +ve = distance increasing)

        # Calculate pedestrian distances and velocities:
        print("PEDESTRIANS:")
        for j in range(total_ped):
            ped_xy = [ped.agent_states[j].pose.position.x, ped.agent_states[j].pose.position.y]
            dist.append(math.sqrt((target_xy[0]-ped_xy[0])**2+(target_xy[1]-ped_xy[1])**2)) # Distance
            if i > 0:
                vel.append((dist[j]-dist_last[j])/t_delay) # Velocity
                print("- Ped: %d | Pose: (%.1f, %.1f) | Dist (Target): %.1f | Vel (Target): %.1f" % (j, ped_xy[0], ped_xy[1], dist[j], vel[j]))
        dist_last = dist # Save distance for next iteration

        # Process pedestrian information:
        dist_sort = sorted(dist) # Sort distance (ascending)
        dist_index = np.argsort(dist) # Index of sorted distance (ascending)
        vel_sort = sorted(vel) # Sort velocity (ascending)
        vel_index = np.argsort(vel) # Index of sorted velocity (ascending)
        best_ped_dist = dist_index[0] # Best pedestrian based on distance
        best_ped_vel = dist_index[0] # Best pedestrian based on velocity

        # Robot navigation algorithm:
        if i > 0:
            # Start by finding the best pedestrian:
            best_ped_smart = best_ped_dist
            for j in range(total_ped):
            # Loop through pedestrians from closest to furthest from target...
                if vel[dist_index[j]] < 0:
                # If their velocity is -ve (distance is decreasing)...
                    best_ped_smart = dist_index[j] # They are the best pedestrian!!!
                    break

            # Pedestrian selection summary:
            print("\nSELECTION:")
            print("- Based on distance: Ped %d @ %.1fm distance from target..." % (best_ped_dist, dist_sort[0]))
            print("- Based on velocity: Ped %d @ %.1fm/s velocity towards target..." % (best_ped_vel, -vel_sort[0]))
            print("- Based on combination: Ped %d @ minimum distance AND moving towards target..." % (best_ped_smart))
            best_ped = best_ped_smart

            # Robot logic:
            print("\nROBOT:")
            odom = rospy.wait_for_message("/odometry/filtered", Odometry)
            goal_xy = [ped.agent_states[best_ped].pose.position.x, ped.agent_states[best_ped].pose.position.y]
            robot_xy = [odom.pose.pose.position.x, odom.pose.pose.position.y]
            dist_robot_target = math.sqrt((robot_xy[0]-target_xy[0])**2+(robot_xy[1]-target_xy[1])**2)
            dist_robot_ped = math.sqrt((robot_xy[0]-goal_xy[0])**2+(robot_xy[1]-goal_xy[1])**2)

            # Make sure the best pedestrian is closer to target than last goal:
            if dist[best_ped_smart] < dist_ped_target_last:
                dist_ped_target_last = dist[best_ped_smart]
                # If the best pedestrian is closer to target:
                send_goal = 1
                print("- Following: Ped %d @ %.1fm from pedestrian and %.1fm from target..." % (best_ped, dist_robot_ped, dist_robot_target))
            else:
                # If the best pedestrian is further away, don't send a navigaiton goal:
                send_goal = 0
                print("- Waiting for a pedestrian closer to the target. Robot @ %.fm from target... " % dist_robot_target)
            if dist_robot_target < 2:
                reached_target = 1
        else:
            print("- Please wait for the next iteration...")

        # Send navigation goal to navigation stack:
        if send_goal == 1:
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "odom"
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = goal_xy[0]
            goal.target_pose.pose.position.y = goal_xy[1]
            goal.target_pose.pose.orientation.w = 1.0
            client.send_goal(goal)
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
