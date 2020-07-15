#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
from static_params import *
import dynamic_params
from static_params import *
from ped_selection import *
from utils import *
from movement import *


"""
Ideas:
--> Implement no-go zone around starting point, and enforce once out of starting point
--> Component approach for distance instead of radius: follow ped as long as distance in any one of x or y directions is decreasing
--> Set a no-go zone once a phase 1 ped is detected, and enforce once out of that range (likely dangerous)
--> Implement a last resort movement after say 4 rounds of phase 3 ped follows. Maybe a round of straight line movement, maybe 5m left then wait, 5m right then wait, ...
--> In phase 3 keep track of how much further you're moving away from the target. If you've moved more than say 20 metres in a straight line direction away from the target since starting the first phase 3 movement, stop and do something else? 
--> Make robot follow to the last position of phase 3 ped, without being interrupted by phase 1 (likely dangerous)
--> If statement in main that only sends the goal to movebase if the robot is outside the distance threshold from the target
"""


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    i = 0

    while True:
        print("\n\n------------------------- i = %d -------------------------" % i)

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity
        if check_vicinity():
            print("Within building vicinity")
            select_ped_within_vicinity()
        else:
            print("Outside building vicinity")
            ped_found, _ = select_ped_outside_vicinity(1, i)

            # Phase 1 pedestrian not found: use other movement logic to set robot goal
            if ped_found == 0:
                move_without_peds_outside_vicinity()
            
            # Phase 1 pedestrian found: clear various flags to prevent phases 2 and 3 from executing. Goal has already been updated by the ped selection function
            else:
                # Reset moving_to_last_ped flag if it was set, to indicate robot is no longer moving towards a pedestrian's last detected position (phase 2)
                if dynamic_params.moving_to_last_ped == 1:
                    dynamic_params.moving_to_last_ped = 0

                # Cancel timer if it is counting down, to prevent phase 3 from triggering
                elif dynamic_params.timer_set == 1:
                    dynamic_params.timer.cancel()
                    dynamic_params.timer_set = 0
                
        # Send navigation goal to navigation stack:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "odom"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = dynamic_params.goal_xy[0]
        goal.target_pose.pose.position.y = dynamic_params.goal_xy[1]
        goal.target_pose.pose.orientation.w = 1.0
        client.send_goal(goal)

        # Exit program if target is reached
        if dynamic_params.reached_target == 1:
            print("- Robot navigation complete!")
            break

        print("----------------------------------------------------------")
        i += 1
        time.sleep(t_delay)


if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
