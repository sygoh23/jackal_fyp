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

    # Set target point:
    target_x = 54
    target_y = -21

    # Determine number of pedestrians:
    data = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    total_ped = len(data.agent_states)
    n_loop = 200
    t_delay = 2
    print("Delay: %d | Iterations: %d | Target: (%d, %d)" % (t_delay, n_loop, target_x, target_y))
    
    # Follow pedestrian n_loop times:
    for i in range(n_loop):
        print("\n\n------------------------- i = %d -------------------------" % i)

        # Pedestrian position:
        ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
        
        # Distance between each pedestrian and the target:
        print("PEDESTRIANS:")
        dist_list = []
        min_dist = 100000 # initialize to large value
        closest_ped = 0
        for j in range(total_ped):
            ped_x = ped.agent_states[j].pose.position.x
            ped_y = ped.agent_states[j].pose.position.y
            dist_list.append(math.sqrt((target_x-ped_x)**2+(target_y-ped_y)**2))
            if dist_list[j] < min_dist:
                min_dist = dist_list[j]
                closest_ped = j
            print("--Ped: %d | Pose: (%.2f, %.2f) | Dist to Target: %.2f" % (j, ped_x, ped_y, dist_list[j]))
        print("Ped %d is closest to target, %.2fm away" % (closest_ped, min_dist))

        # Select pedestrian closest to target:
        ped_x = ped.agent_states[closest_ped].pose.position.x
        ped_y = ped.agent_states[closest_ped].pose.position.y

        # Robot position:
        odom = rospy.wait_for_message("/odometry/filtered", Odometry)
        odom_x = odom.pose.pose.position.x
        odom_y = odom.pose.pose.position.y
        dist = math.sqrt((odom_x-ped_x)**2+(odom_y-ped_y)**2)
        print("\nROBOT:")
        print("--Follow: ped %d | Dist to ped: %.2fm" % (closest_ped, dist))
        print("----------------------------------------------------------")

        if dist > 2:
           # Creates a new goal with the MoveBaseGoal constructor
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "odom"
            goal.target_pose.header.stamp = rospy.Time.now()
           # Move 0.5 meters forward along the x axis of the "map" coordinate frame
            goal.target_pose.pose.position.x = ped_x
            goal.target_pose.pose.position.y = ped_y
           # No rotation of the mobile base frame w.r.t. map frame
            goal.target_pose.pose.orientation.w = 1.0
           # Sends the goal to the action server.
            client.send_goal(goal)

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
