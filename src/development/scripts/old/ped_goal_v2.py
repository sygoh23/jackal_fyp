#!/usr/bin/env python
# license removed for brevity

import rospy
import random
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates

def movebase_client():
   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Select a pedsim pedestrian
    data = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    n = len(data.agent_states)
    ped_n = random.randint(1,1)
    ped_x = data.agent_states[ped_n-1].pose.position.x
    ped_y = data.agent_states[ped_n-1].pose.position.y
    print("Pedestrian Info: x = %.2f, y = %.2f" % (ped_x, ped_y))

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

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        #if result:
        #    rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
