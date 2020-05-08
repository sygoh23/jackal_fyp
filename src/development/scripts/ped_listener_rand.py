#!/usr/bin/env python2
import rospy
import random
from pedsim_msgs.msg import AgentStates

def listener():
    # Create a new node 'listener'
    rospy.init_node('listener', anonymous=True)

    # Subscribe to topic '/pedsim_simulator/simulated_agents'
    data = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)

    # Process data:
    n = len(data.agent_states)
    ped_n = random.randint(1,n)
    x = data.agent_states[ped_n-1].pose.position.x
    y = data.agent_states[ped_n-1].pose.position.y
    print("x = %.2f, y = %.2f" % (x, y))

if __name__ == '__main__':
    listener()
