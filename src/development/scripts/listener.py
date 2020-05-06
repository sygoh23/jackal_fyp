#!/usr/bin/env python2
import rospy
from pedsim_msgs.msg import AgentStates


def callback(data):
    
    print("\n*************************")

    # Number of simulated pedestrians
    n = len(data.agent_states)

    # Extract x/y location for each pedestrian
    for i in range(n):
        x = data.agent_states[i].pose.position.x
        y = data.agent_states[i].pose.position.y
        print("Ped %d: x = %.2f y = %.2f" % (i+1, x, y))
        

def listener():

    # Create a new node 'listener'
    rospy.init_node('listener', anonymous=True)

    # Subscribe to topic '/pedsim_simulator/simulated_agents'
    rospy.Subscriber("/pedsim_simulator/simulated_agents", AgentStates, callback)

    # Prevent python from exiting until the node is stopped
    rospy.spin()


if __name__ == '__main__':
    
    print("******************************LISTENER RUNNING**************************************")
    listener()
