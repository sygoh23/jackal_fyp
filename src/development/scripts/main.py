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

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import pickle

"""
Ideas:
--> Ped selection within building vicinity: follow a random pedestrian, move along edge of building
--> Smarter navigation when there are no peds and outside building vicinity
--> Detect and recover when robot is stuck driving into a wall
--> Implement no-go zones
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

            # Manually set robot goal if a pedestrian was not found by the ped selection logic
            if ped_found == 0:
                move_without_peds_outside_vicinity()
            else:
                # Reset moving_to_last_ped flag if it was set
                if dynamic_params.moving_to_last_ped == 1:
                    dynamic_params.moving_to_last_ped = 0

                # Cancel timer if it is counting down
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

        """
        print("********** STARTED **********")
        rospy.init_node("parse_pc2", anonymous=True)
        data = rospy.wait_for_message("/velodyne_points2", PointCloud2)
        points_list = []
        gen = point_cloud2.read_points(data, field_names = ("x", "y", "z"), skip_nans=True)
        for point in gen:
            #print(point) # tuple (-44.07529067993164, 13.067326545715332, 8.661510467529297)
            points_list.append(point)
        with open("/home/bob/Documents/walls.pickle", "wb") as f:
            pickle.dump(points_list, f)
        print("********** Saved **********")
        """
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
