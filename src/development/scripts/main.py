#!/usr/bin/env python
import time
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from static_params import *
import dynamic_params
from ped_selection import *
from recovery import *
from utils import *
from movement import *
from std_msgs.msg import String
import matplotlib
import matplotlib.pyplot as plt
import pickle
import tf
from geometry_msgs.msg import PointStamped
listener = 0

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
    global listener

    # Move_base initialisation:
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    i = 0

    # Recovery behaviour:
    rec_attempts = 1 # Number of recovery attempts
    rec_enable = 1 # Enable recovery
    rec_last_i = 0 # Last time recovery was initiated
    rec_smooth_filter = 10; # Amount of mean smoothing for recovery scores
    rec_threshold = 30; # Score threshold to activate recovery behaviour
    last_building_vel = []

    # Set exclusion zone around starting point
    start_point = get_robot_xy()
    dynamic_params.exclusion_zones.append(generate_zone(start_point, zone_length))

    # Initialisation for recovery beheaviour:
    pickle.dump(dynamic_params.remove_x, open(simulation_setup.remove_x_pth,"w"))
    pickle.dump(dynamic_params.remove_y, open(simulation_setup.remove_y_pth,"w"))
    dynamic_params.robot_xy = get_robot_xy()
    dynamic_params.map_range = 50

    # Axes to plot wall detection
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index

    # Begin navigation algorithm
    while True:
        print("\n\n------------------------- i = %d -------------------------\n" % i)

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity, and if an entrance has/has not been found
        if contains_pt(get_robot_xy(), building_polygon) and (not dynamic_params.entrance_found):
            print("- Status: Within building vicinity...")
            rec_enable = 0

            try:
                ##### Transform building entrance FROM odom (world frame) TO base_link (robot frame) #####
                # In terminal: rosrun tf tf_echo base_link odom
                #(trans, rot) = listener.lookupTransform('base_link', 'odom', rospy.Time(0))

                # Building entrance in odom (world) frame
                original_pt = PointStamped()
                original_pt.header.frame_id = "odom"
                original_pt.header.stamp = rospy.Time(0)
                original_pt.point.x = building_entrance_xy[0]
                original_pt.point.y = building_entrance_xy[1]
                original_pt.point.z = 0.0

                # Building_entrance in base_link (robot) frame
                transformed_pt = listener.transformPoint('base_link', original_pt)
                transformed_pt_xy = [transformed_pt.point.x, transformed_pt.point.y]

                # Get wall following goal point in base_link (robot) frame
                goal_xy_robot_frame = move_within_vicinity(target_xy=transformed_pt_xy, ax=ax, plot_results=True)
                #time.sleep(5) # Slow things down to debug!

                ##### Transform goal point FROM base_link (robot frame) BACK TO odom (world frame) #####
                base_link_pt = PointStamped()
                base_link_pt.header.frame_id = 'base_link'
                base_link_pt.header.stamp = rospy.Time(0)
                base_link_pt.point.x = goal_xy_robot_frame[0]
                base_link_pt.point.y = goal_xy_robot_frame[1]
                base_link_pt.point.z = 0.0
                
                odom_pt = listener.transformPoint('odom', base_link_pt)
                dynamic_params.goal_xy = [odom_pt.point.x, odom_pt.point.y]

                #print(trans); print('')
                #print(rot); print('')
                #print(original_pt); print('')
                #print(transformed_pt); print('')

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print('Transform failed')

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

            # Phase 1 pedestrian not found:
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
        if not manual_navigation:
            client.send_goal(setup_goal(dynamic_params.goal_xy[0], dynamic_params.goal_xy[1]))

        # Recovery behaviour:
        save_history(i)
        building_dist = get_distance(building_center_xy[0], dynamic_params.hist_x[i], building_center_xy[1], dynamic_params.hist_y[i])
        building_vel = get_distance(building_center_xy[0], dynamic_params.hist_x[i-1], building_center_xy[1], dynamic_params.hist_y[i-1]) - building_dist
        last_building_vel.append(building_vel)

        # Check robot progress towards building centre:
        avg_building_vel = 0
        if (i >= rec_smooth_filter):
            avg_building_vel = 0
            for j in range(rec_smooth_filter):
                new_vel = last_building_vel[i-j]
                avg_building_vel = avg_building_vel + new_vel
        if (avg_building_vel < 0):
            avg_building_vel = 0

        # Check robot movement for recovery:
        if (i >= rec_smooth_filter) and (len(dynamic_params.poi_x) > 1) and (rec_enable == 1):
            robot_disp = 0
            for j in range(rec_smooth_filter):
                new_dist = get_distance(dynamic_params.hist_x[i-j], dynamic_params.hist_x[i-j-1],dynamic_params.hist_y[i-j], dynamic_params.hist_y[i-j-1])
                robot_disp = robot_disp + new_dist
            rec_score = robot_disp + avg_building_vel

            print("- Recovery Behaviour: %.1f points / %.1f points" % (rec_score, rec_threshold))
            print("--- Building Progress Score: %.1f points" % (avg_building_vel))
            print("--- Robot Displacement Score: %.1f points" % (robot_disp))

            if (i-rec_last_i <= rec_smooth_filter):
                print("- Robot has recently recovered. Recovery reactivating in %d..." % (rec_smooth_filter-(i-rec_last_i)+1))

            if (rec_score < rec_threshold) and (i-rec_last_i > rec_smooth_filter):
                # Engage recovery behaviour, send robot to last POI:
                print("--- Robot movement failure! Recovery #%d initiated..." % (rec_attempts))
                remove_points(rec_attempts); rec_last_i = i
                dynamic_params.recovery_override = 1; robot_xy = get_robot_xy()
                rec_poi = select_rec_poi(rec_attempts)
                rec_x = dynamic_params.poi_x[rec_poi]
                rec_y = dynamic_params.poi_y[rec_poi]
                print("--- Last point of interest: " + str([rec_x, rec_y]))
                print("--- Robot position: " + str([robot_xy[0], robot_xy[1]]))
                while inside_radius(rec_x, rec_y, 3, robot_xy[0], robot_xy[1]) == False:
                    robot_xy = get_robot_xy()
                    rec_d = get_distance(rec_x, robot_xy[0], rec_y, robot_xy[1])
                    rec_goal_x = rec_x; rec_goal_y = rec_y; rec_goal_d = rec_d;
                    if rec_d > 20:
                        while (rec_goal_d > 20):
                            rec_goal_x = (rec_goal_x + robot_xy[0]) / 2
                            rec_goal_y = (rec_goal_y + robot_xy[1]) / 2
                            rec_goal_d = get_distance(rec_goal_x, robot_xy[0], rec_goal_y, robot_xy[1])
                    print("--- Recovery goal: " + str([rec_goal_x, rec_goal_y]))
                    client.send_goal(setup_goal(rec_goal_x, rec_goal_y))
                    robot_xy = get_robot_xy(); time.sleep(1)

                # Send removed points to custom laserscan plugin:
                pickle.dump(dynamic_params.remove_x, open(simulation_setup.remove_x_pth, "w"))
                pickle.dump(dynamic_params.remove_y, open(simulation_setup.remove_y_pth, "w"))

                # Reset pedestrian following logic:
                dynamic_params.ped_last = []; dynamic_params.following_ped = 0;
                dynamic_params.goal_xy = [robot_xy[0], robot_xy[1]]
                print("--- Robot has now moved to the last point of interest...")
                rec_attempts += 1; dynamic_params.recovery_override = 0
                time.sleep(1)
        else:
            print("- Recovery Score: Unavailable")

        find_poi()
        #update_map()

        # Exit program if target is reached
        if dynamic_params.reached_target == 1:
            print("-- Robot navigation complete!")
            break
        print("\n----------------------------------------------------------")
        i += 1
        time.sleep(t_delay)

if __name__ == '__main__':
    try:
        global listener
        rospy.init_node('movebase_client_py')
        listener = tf.TransformListener()
        result = movebase_client()
    except rospy.ROSInterruptException:
        print("Algorithm finished!")
