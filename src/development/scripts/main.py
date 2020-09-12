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

import tf
from geometry_msgs.msg import PointStamped
import pickle
#import tf2_ros
#from tf2_msgs.msg import TFMessage
#from tf.msg import tfMessage
#from tf2_msgs.msg import tfMessage
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

    # Set exclusion zone around starting point
    start_point = get_robot_xy()
    dynamic_params.exclusion_zones.append(generate_zone(start_point, zone_length))

    # Begin navigation algorithm
    while True:
        print("\n\n------------------------- i = %d -------------------------" % i)

        # Choose pedestrian selection logic based on whether the robot is inside/outside building vicinity, and if an entrance has/has not been found
        if contains_pt(get_robot_xy(), building_polygon) and (not dynamic_params.entrance_found):
            print("Within building vicinity")

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
                goal_xy_robot_frame = move_within_vicinity(transformed_pt_xy)

                ##### Transform goal point FROM base_link (robot frame) BACK TO odom (world frame) #####
                original_pt = listener.transformPoint('odom', goal_xy_robot_frame)
                dynamic_params.goal_xy = [original_pt.point.x, original_pt.point.y]

                """
                with open('/home/chris/Documents/tf_point.pickle', 'wb') as f:
                    pickle.dump(transformed_pt_xy, f)
                """

                #print(trans); print('')
                #print(rot); print('')
                #print(original_pt); print('')
                #print(transformed_pt); print('')

                

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print('Transform failed')

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

        # Exit program if target is reached
        if dynamic_params.reached_target == 1:
            print("- Robot navigation complete!")
            break

        print("----------------------------------------------------------")
        i += 1
        time.sleep(t_delay)





if __name__ == '__main__':
    try:
        global listener
        rospy.init_node('movebase_client_py')
        listener = tf.TransformListener()
        result = movebase_client()
        

        
        """
        rospy.init_node('transform_listener')

        tfBuffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tfBuffer)

        try:
            # Transform from odom to base_link
            trans = tfBuffer.lookup_transform('velodyne2_base_link', 'front_mount', rospy.Time())
            print(trans)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print('failed')
            time.sleep(1)

        #listener.waitForTransform("/frame1", "/frame2", rospy.Time(), rospy.Duration(4.0))
        #(trans, rot) = listener.lookupTransform("/frame1", "/frame2", rospy.Time(0))
        #rospy.spin()
        """    

        #rospy.init_node('transform_listener')
        

        
        """
        for i in range(100):
            print("Before transform")
            transform = rospy.wait_for_message("/tf", tfMessage)
            print(transform)

            time.sleep(1)
        """
        


    except rospy.ROSInterruptException:
        print("Algorithm finished!")
