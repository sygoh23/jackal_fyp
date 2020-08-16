#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from static_params import *
import dynamic_params
from static_params import *
from ped_selection import *
from recovery import *
from utils import *
from movement import *
from std_msgs.msg import String
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

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
    rec_attempts = 0

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

        # Recovery behaviour:
        rb_threshold = 5; rb_smooth = 10
        robot_xy = get_robot_xy()
        dynamic_params.x_hist.append(robot_xy[0])
        dynamic_params.y_hist.append(robot_xy[1])
        if (i % 5) == 0:
            poi_xy = find_poi(dynamic_params.x_hist[:], dynamic_params.y_hist[:])
            poi_x = poi_xy[0]; poi_y = poi_xy[1]
            plt.grid(b=True, which='major', color='#d6d6d6', linestyle='--')
            plt.scatter(dynamic_params.x_hist, dynamic_params.y_hist, c='k', marker='.', alpha=0.5, label='1')
            plt.scatter(poi_x, poi_y, c='b', marker='D', s=50, label='-1')
            plt.gca().set_aspect('equal', adjustable='box')
            plt.savefig("/home/ubuntu/Map.png")
        if (i >= rb_smooth) and (len(poi_x) > 1):
            dist_score = 0
            disp_score = get_distance(dynamic_params.x_hist[i-rb_smooth], dynamic_params.x_hist[i], dynamic_params.y_hist[i-rb_smooth], dynamic_params.y_hist[i],)
            for j in range(rb_smooth):
                new_dist = get_distance(dynamic_params.x_hist[i-j], dynamic_params.x_hist[i-j-1],dynamic_params.y_hist[i-j], dynamic_params.y_hist[i-j-1])
                dist_score = dist_score + new_dist
            print("- Displacement score: %dm / Distance score: %dm" % (disp_score, dist_score))
            print("- Recovery score: %d points / Threshold: %d points" % (dist_score, rb_threshold))

            if dist_score < rb_threshold:
                rec_attempts += 1

                # Remove points:
                print("- Robot movement failure! Recovery #%d initiated..." % rec_attempts)
                remove_xy = remove_points(dynamic_params.x_hist, dynamic_params.y_hist, poi_x[-rec_attempts], poi_y[-rec_attempts], robot_xy[0], robot_xy[1])
                remove_x = remove_xy[0]; remove_y = remove_xy[1]
                plt.grid(b=True, which='major', color='#d6d6d6', linestyle='--')
                plt.scatter(remove_x, remove_y, c='r', marker='x', s=50, label='0')
                plt.scatter(poi_x[-rec_attempts], poi_y[-rec_attempts], c='green', marker='D', s=100, label='0')
                plt.gca().set_aspect('equal', adjustable='box')
                plt.savefig("/home/ubuntu/Map.png")

                # Attempt to move to last POI:
                dynamic_params.recovery_override = 1
                robot_xy = get_robot_xy()
                rec_x = poi_x[-rec_attempts]
                rec_y = poi_y[-rec_attempts]
                print("- Last point of interest: " + str([rec_x, rec_y]))
                print("- Robot position: " + str([robot_xy[0], robot_xy[1]]))
                while inside_radius(rec_x, rec_y, 3, robot_xy[0], robot_xy[1]) == False:
                    robot_xy = get_robot_xy()
                    #print("- Entering recovery loop...")
                    rec_d = get_distance(rec_x, robot_xy[0], rec_y, robot_xy[1])
                    rec_goal_x = rec_x
                    rec_goal_y = rec_y
                    rec_goal_d = rec_d
                    if rec_d > 20:
                        while (rec_goal_d > 20):
                            rec_goal_x = (rec_goal_x + robot_xy[0]) / 2
                            rec_goal_y = (rec_goal_y + robot_xy[1]) / 2
                            rec_goal_d = get_distance(rec_goal_x, robot_xy[0], rec_goal_y, robot_xy[1])
                    print("- Recovery goal: " + str([rec_goal_x, rec_goal_y]))
                    goal = MoveBaseGoal()
                    goal.target_pose.header.frame_id = "odom"
                    goal.target_pose.header.stamp = rospy.Time.now()
                    goal.target_pose.pose.position.x = rec_goal_x
                    goal.target_pose.pose.position.y = rec_goal_y
                    goal.target_pose.pose.orientation.w = 1.0
                    client.send_goal(goal)
                    robot_xy = get_robot_xy()
                    time.sleep(1)
                    # Recovery behaviour (finish)
                print("- Robot has now recovered to last point of interest.")
                dynamic_params.recovery_override = 0
                time.sleep(500000)
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
