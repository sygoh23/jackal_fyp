#!/usr/bin/env python
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
   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

    # Set target as first building:
    #target_x = 54
    #target_y = 39

    # Set target as second building:
    target_x = 54
    target_y = -21

    # Determine number of pedestrians:
    data = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    total_ped = len(data.agent_states)
    n_loop = 200 # Number of following iterations
    t_delay = 2 # Time between iterations
    print("Delay: %d | Iterations: %d | Target: (%d, %d)" % (t_delay, n_loop, target_x, target_y))
    dist_last = []
    vel_last = []
    # Follow pedestrian n_loop times:
    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)
        # Pedestrian position:
        ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
        dist = [] # distances to target
        vel = [] # change in distances to target
        min_dist = 100000 # initialize to large value
        max_vel = -100000 # initialize to small value
        best_ped_raw = 0
        best_ped_vel = 0
        print("PEDESTRIANS:")
        for j in range(total_ped):
            ped_x = ped.agent_states[j].pose.position.x
            ped_y = ped.agent_states[j].pose.position.y
            dist.append(math.sqrt((target_x-ped_x)**2+(target_y-ped_y)**2))
            if dist[j] < min_dist:
                min_dist = dist[j]
                best_ped_raw = j
            if i > 0:
                vel.append(dist_last[j]-dist[j])
                print("- Ped: %d | Pose: (%.1f, %.1f) | Distance (Target): %.1f | Velocity (Target): %.1f" % (j, ped_x, ped_y, dist[j], vel[j]))
                if vel[j] > max_vel:
                    max_vel = vel[j]
                    best_ped_vel = j
        dist_last = dist
        vel_last = vel

        best_ped = best_ped_raw # Select closest pedestrian first
        wait = 0;
        if i > 0:
            print("Best Ped (Position): Ped %d @ %.1fm distance from target..." % (best_ped_raw, min_dist))
            print("Best Ped (Velocity): Ped %d @ %.1fm/s velocity towards target..." % (best_ped_vel, max_vel))
            if dist_last[best_ped]*vel_last[best_ped] < 0:
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
