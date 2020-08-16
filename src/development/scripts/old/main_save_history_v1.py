#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from static_params import *
import dynamic_params
from static_params import *
from ped_selection import *
from utils import *
from movement import *
from std_msgs.msg import String
import matplotlib.pyplot as plt

"""
Ideas:
--> Don't follow a pedestrian if it's where the robot came from
--> Component approach for distance instead of radius: follow ped as long as distance in any one of x or y directions is decreasing
--> Implement a last resort movement logic after say 4 rounds of following a pedestrian in phase 3. Maybe a round of straight line movement, maybe 5m left then wait, 5m right then wait, etc
--> In phase 3 keep track of how much further the robot is moving away from the target. If it's moved more than say 20 metres in a straight line direction away from the target since starting the first phase 3 movement, stop and do something else?
--> Make robot move to the last position of the pedestrian in phase 3, without being interrupted by phase 1? (risky)
--> If statement in main that only sends the goal to movebase if the robot is outside the distance threshold from the target
--> Only follow pedestrians moving away from robot?
--> Obtain the result of movebase for use in decision making. Somehow published through a topic
"""


def movebase_client():
    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    i = 0

    # Recovery behaviour:
    rb_i = 0
    rb_pth_x = "/home/ubuntu/Mapping/x_v4.txt"
    rb_pth_y = "/home/ubuntu/Mapping/y_v4.txt"

    # Set exclusion zone around starting point
    start_point = get_robot_xy()
    dynamic_params.exclusion_zones.append(generate_zone(start_point, zone_length))

    # Begin navigation algorithm
    while True:
        print("\n\n------------------------- i = %d -------------------------" % i)

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity, and if an entrance has/has not been found
        if contains_pt(get_robot_xy(), building_polygon) and (not dynamic_params.entrance_found):
            print("Within building vicinity")
            select_ped_within_vicinity()

            # Read object detection results
            if process_img:
                is_door = rospy.wait_for_message("/detected_objects", String)
                print("Door detected: %s" % is_door.data)

                # If entrance was detected, trigger final movement to entrance
                if is_door.data == "true":
                    print("Moving to doorway")
                    dynamic_params.entrance_found = True
                    move_to_doorway()

        elif not dynamic_params.entrance_found:
            print("Outside building vicinity")
            ped_found, _ = select_ped_outside_vicinity(1, i)

            # Phase 1 pedestrian not found:import matplotlib
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

                # If phase 3 was interrputed while following a pedestrian, reset the following_ped flag
                if dynamic_params.following_ped == 1:
                    dynamic_params.following_ped = 0

                # If phase 3 was interrupted while moving to last ped position, reset out_of_range flag
                if dynamic_params.out_of_range == 1:
                    dynamic_params.out_of_range = 0

        # Send navigation goal to navigation stack:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "odom"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = dynamic_params.goal_xy[0]
        goal.target_pose.pose.position.y = dynamic_params.goal_xy[1]
        goal.target_pose.pose.orientation.w = 1.0
        client.send_goal(goal)

        # RB - Recovery behaviour:
        rb_threshold = 3
        robot_xy = get_robot_xy()
        dynamic_params.x_hist.append(robot_xy[0])
        dynamic_params.y_hist.append(robot_xy[1])
        print("- RB - Robot location: (%d, %d)" % (dynamic_params.x_hist[i], dynamic_params.y_hist[i]))

        # RB - Calculate distance covered:
        if i >= 20:
            dist_covered = 0
            for j in range(20):
                new_dist = get_distance(dynamic_params.x_hist[i-j], dynamic_params.x_hist[i-j-1],dynamic_params.y_hist[i-j], dynamic_params.y_hist[i-j-1])
                dist_covered = dist_covered + new_dist
            print("- RB - Averaged distance: %dm" % dist_covered)

        # RB - Saving history:
        if rb_i == 10:
            rb_i = 0
            with open(rb_pth_x, 'w') as filehandle:
                filehandle.writelines("%s\n" % x_coord for x_coord in dynamic_params.x_hist)
            with open(rb_pth_y, 'w') as filehandle:
                filehandle.writelines("%s\n" % y_coord for y_coord in dynamic_params.y_hist)
            print("- RB - Saved history!")

            plt.close()
            #plt.ion()
            fig = plt.figure()
            plt.scatter(dynamic_params.x_hist, dynamic_params.y_hist, c='k', marker='.', alpha=.5, label='1')
            #plt.pause(0.001)
            plt.show(block = False)

        rb_i += 1

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
