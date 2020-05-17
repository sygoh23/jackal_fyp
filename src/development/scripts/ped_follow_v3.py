#!/usr/bin/env python
import rospy
import random
import time
import math
import actionlib
import numpy as np
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry

def movebase_client():
   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

    # First target:
    #target_x = 54
    #target_y = 39

    # Second target:
    target_x = 54
    target_y = -21

    # Determine number of pedestrians:
    data = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    total_ped = len(data.agent_states)
    n_loop = 200
    t_delay = 2
    print("Delay: %d | Iterations: %d | Target: (%d, %d)" % (t_delay, n_loop, target_x, target_y))
    dist_last = []
    dist_delta_last = []
    # Follow pedestrian n_loop times:
    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)
        # Pedestrian position:
        ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)

        # Distance between each pedestrian and the target:
        dist_list = [] # distances to target
        dist_delta = [] # change in distances to target
        min_dist_raw = 100000 # initialize to large value
        max_dist_delta = -100000 # initialize to small value
        best_ped_raw = 0
        best_ped_delta = 0
        print("PEDESTRIANS:")
        for j in range(total_ped):
            ped_x = ped.agent_states[j].pose.position.x
            ped_y = ped.agent_states[j].pose.position.y
            dist_list.append(math.sqrt((target_x-ped_x)**2+(target_y-ped_y)**2))
            if dist_list[j] < min_dist_raw:
                min_dist_raw = dist_list[j]
                best_ped_raw = j
            if i > 0:
                dist_delta.append(dist_last[j]-dist_list[j])
                print("- Ped: %d | Pose: (%.1f, %.1f) | Distance (Target): %.1f | Velocity (Target): %.1f" % (j, ped_x, ped_y, dist_list[j], dist_delta[j]))
                if dist_delta[j] > max_dist_delta:
                    max_dist_delta = dist_delta[j]
                    best_ped_delta = j
        dist_last = dist_list
        dist_delta_last = dist_delta

        best_ped = best_ped_raw # Select closest pedestrian first
        wait = 0;
        if i > 0:
            print("Best Ped (Position): Ped %d @ %.1fm distance from target..." % (best_ped_raw, min_dist_raw))
            print("Best Ped (Velocity): Ped %d @ %.1fm/s velocity towards target..." % (best_ped_delta, max_dist_delta))
            if dist_last[best_ped]*dist_delta_last[best_ped] < 0:
                wait = 1; # If the pedestrian is moving away from target: wait...
                print("NOTICE: Pedestrian is moving away from target, selecting new target...")
        else:
            print("- Wait for next iteration...")

        # Extract location of targetted pedestrian:
        goal_x = ped.agent_states[best_ped].pose.position.x
        goal_y = ped.agent_states[best_ped].pose.position.y

        # Extract robot position:
        odom = rospy.wait_for_message("/odometry/filtered", Odometry)
        odom_x = odom.pose.pose.position.x
        odom_y = odom.pose.pose.position.y
        dist_robot_ped = math.sqrt((odom_x-ped_x)**2+(odom_y-ped_y)**2)
        dist_robot_target = math.sqrt((odom_x-target_x)**2+(odom_y-target_y)**2)
        print("\nROBOT:")
        print("- Follow: Ped %d | Distance (Ped): %.1fm | Distance (Target): %.2fm" % (best_ped, dist_robot_ped, dist_robot_target))
        print("----------------------------------------------------------")

        if dist_robot_target > 5 and wait == 0:
           # Creates a new goal with the MoveBaseGoal constructor
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "odom"
            goal.target_pose.header.stamp = rospy.Time.now()
           # Move 0.5 meters forward along the x axis of the "map" coordinate frame
            goal.target_pose.pose.position.x = goal_x
            goal.target_pose.pose.position.y = goal_y
           # No rotation of the mobile base frame w.r.t. map frame
            goal.target_pose.pose.orientation.w = 1.0
           # Sends the goal to the action server.
            client.send_goal(goal)
        elif wait == 0:
            print("Navigation complete!!!")
            break
        time.sleep(t_delay)

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        #if result:
        #    rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        print("Finished.")
        #rospy.loginfo("Navigation test finished.")
