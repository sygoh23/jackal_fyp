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
import pickle
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

    # Recovery behaviour:
    rec_attempts = 1
    rec_enable = 1
    last_building_vel = []

    # Set exclusion zone around starting point
    start_point = get_robot_xy()
    dynamic_params.exclusion_zones.append(generate_zone(start_point, zone_length))

    pickle.dump(dynamic_params.remove_x, open("/home/ubuntu/x.pkl","w"))
    pickle.dump(dynamic_params.remove_y, open("/home/ubuntu/y.pkl","w"))

    # Begin navigation algorithm
    while True:
        print("\n\n------------------------- i = %d -------------------------\n" % i)

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity, and if an entrance has/has not been found
        if contains_pt(get_robot_xy(), building_polygon) and (not dynamic_params.entrance_found):
            print("- Status: Within building vicinity...")
            select_ped_within_vicinity()
            rec_enable = 0

            # Read object detection results
            if process_img:
                is_door = rospy.wait_for_message("/detected_objects", String)
                print("--- Door detected: %s" % is_door.data)

                # If entrance was detected, trigger final movement to entrance
                if is_door.data == "true":
                    print("--- Moving to doorway")
                    dynamic_params.entrance_found = True
                    move_to_doorway()

        elif not dynamic_params.entrance_found:
            print("- Status: Outside building vicinity...")
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
        # Every five iterations, update the map:
        rb_threshold = 7.5; rb_smooth = 10
        save_history()

        building_dist = get_distance(building_center_xy[0], dynamic_params.hist_x[i], building_center_xy[1], dynamic_params.hist_y[i])
        building_vel = get_distance(building_center_xy[0], dynamic_params.hist_x[i-1], building_center_xy[1], dynamic_params.hist_y[i-1]) - building_dist
        last_building_vel.append(building_vel)

        # Check robot progress towards building centre:
        avg_building_vel = 0
        if (i>=rb_smooth):
            avg_building_vel = 0
            for j in range(rb_smooth):
                new_vel = last_building_vel[i-j]
                avg_building_vel = avg_building_vel + new_vel
        if (avg_building_vel < 0):
            avg_building_vel = 0

        # Check robot movement for recovery:
        if (i >= rb_smooth) and (len(dynamic_params.poi_x) > 1) and (rec_enable == 1):
            robot_disp = 0
            for j in range(rb_smooth):
                new_dist = get_distance(dynamic_params.hist_x[i-j], dynamic_params.hist_x[i-j-1],dynamic_params.hist_y[i-j], dynamic_params.hist_y[i-j-1])
                robot_disp = robot_disp + new_dist
            rec_score = robot_disp + avg_building_vel
            print("- Recovery Behaviour: %.1f points / %.1f points" % (rec_score, rb_threshold))
            print("--- Building Progress Score: %.1f points" % (avg_building_vel))
            print("--- Robot Displacement Score: %.1f points" % (robot_disp))

            if rec_score < rb_threshold:
                # Engage recovery behaviour:
                print("--- Robot movement failure! Recovery #%d initiated..." % (rec_attempts))
                # Determine points to remove from map:
                remove_points(rec_attempts)
                update_map()

                # Send robot to last point of interest:
                dynamic_params.recovery_override = 1
                robot_xy = get_robot_xy()
                rec_x = dynamic_params.poi_x[-rec_attempts]
                rec_y = dynamic_params.poi_y[-rec_attempts]
                print("--- Last point of interest: " + str([rec_x, rec_y]))
                print("--- Robot position: " + str([robot_xy[0], robot_xy[1]]))
                while inside_radius(rec_x, rec_y, 3, robot_xy[0], robot_xy[1]) == False:
                    robot_xy = get_robot_xy()
                    rec_d = get_distance(rec_x, robot_xy[0], rec_y, robot_xy[1])
                    rec_goal_x = rec_x; rec_goal_y = rec_y; rec_goal_d = rec_d
                    if rec_d > 20:
                        while (rec_goal_d > 20):
                            rec_goal_x = (rec_goal_x + robot_xy[0]) / 2
                            rec_goal_y = (rec_goal_y + robot_xy[1]) / 2
                            rec_goal_d = get_distance(rec_goal_x, robot_xy[0], rec_goal_y, robot_xy[1])
                    print("--- Recovery goal: " + str([rec_goal_x, rec_goal_y]))
                    goal = MoveBaseGoal()
                    goal.target_pose.header.frame_id = "odom"
                    goal.target_pose.header.stamp = rospy.Time.now()
                    goal.target_pose.pose.position.x = rec_goal_x
                    goal.target_pose.pose.position.y = rec_goal_y
                    goal.target_pose.pose.orientation.w = 1.0
                    client.send_goal(goal)
                    robot_xy = get_robot_xy()
                    time.sleep(1)

                # Send removed points to custom laserscan plugin:
                pickle.dump(dynamic_params.remove_x, open("/home/ubuntu/x.pkl","w"))
                pickle.dump(dynamic_params.remove_y, open("/home/ubuntu/y.pkl","w"))

                # Reset pedestrian following logic:
                dynamic_params.ped_last = []
                dynamic_params.following_ped = 0
                dynamic_params.goal_xy = [robot_xy[0], robot_xy[1]]
                print("--- Robot has now moved to the last point of interest...")
                rec_attempts += 1
                dynamic_params.recovery_override = 0
                time.sleep(1)
        else:
            print("- Recovery Score: Unavailable")

        if (i % 5) == 0:
            find_poi()
            update_map()

        # Exit program if target is reached
        if dynamic_params.reached_target == 1:
            print("-- Robot navigation complete!")
            break
        dynamic_params.debug_please = []
        print("\n----------------------------------------------------------")
        i += 1
        time.sleep(t_delay)

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
