"""
Contains pedestrian selection logic.
select_ped_within_vicinity(): used when the robot is within the building vicinity.
select_ped_outside_vicinity(): used when the robot is outside the building vicinity.
"""

import numpy as np
import rospy
import dynamic_params
from pedsim_msgs.msg import AgentStates
from static_params import *
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from utils import *
import pickle
import time
import tf
import tf2_ros
import sys
matplotlib.use('Agg')


"""
Selects a pedestrian to follow when the robot is within the building vicinity
--> Assumes there is only one doorway in the defined building vicinity
--> Currently doesn't use pedestrians at all, but kept the name because following pedestrians may be a better option. Depends how well the current idea performs
"""

def select_ped_within_vicinity():
    # While the goal point is outside the building vicinity
    while not contains_pt(dynamic_params.goal_xy, building_polygon):
        print("--> Current goal is outside vicinity, generating new goal...")

        # Generate new goal point that is close to a wall, and in the direction of the target
        pointcloud = get_pointcloud()

    # Calculate next goal point
    pointcloud = get_pointcloud()

    with open(simulation_setup.pointcloud_pth, 'wb') as f:
        pickle.dump(pointcloud, f)
    sys.exit()

    # If this goal point is outside the building vicinity, generate another point
    while not contains_pt(dynamic_params.goal_xy, building_polygon):
        print("--> Current goal is outside vicinity, generating new goal...")

    print("--> Looking for doorway")

# Selects a pedestrian when the robot is outside the building vicinity, based on which movement phase the robot is in
# Phase = 1: select pedestrian based on rigorous conditions
# Phase = 3: select pedestrian closest to robot
def select_ped_outside_vicinity(phase, i):

    ##############################################
    ############### Initialization ###############
    ##############################################

    ped_found = 0                           # Flag for whether a suitable pedestrian to follow was found (1) or not (0). Init to 0 to assume there are no peds
    robot_xy = get_robot_xy()               # Robot current x-y position
    dist_ped_building_center_list = []      # Distance to building center (always +ve, lower = better)
    vel = []                                # Velocity towards building center (-ve = distance decreasing, +ve = distance increasing)
    dist_robot_ped_list = []                # List of distances between the robot and each pedestrian
    dist_robot_building_center = get_distance(robot_xy[0], building_center_xy[0], robot_xy[1], building_center_xy[1])   # Distance between robot and building center
    total_ped = get_total_peds()

    ###############################################
    ############### Data Collection ###############
    ###############################################

    ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    for j in range(total_ped):
        # Calculate distance between a) pedestrian and building center, b) robot and pedestrian
        ped_xy = [ped.agent_states[j].pose.position.x, ped.agent_states[j].pose.position.y]
        dist_ped_building_center = get_distance(building_center_xy[0], ped_xy[0], building_center_xy[1], ped_xy[1])
        dist_robot_ped = get_distance(robot_xy[0], ped_xy[0], robot_xy[1], ped_xy[1])
        dist_ped_building_center_list.append(dist_ped_building_center)
        dist_robot_ped_list.append(dist_robot_ped)

        # Calculate pedestrian velocity
        if i > 0:
            vel.append((dist_ped_building_center_list[j]-dynamic_params.dist_last[j])/t_delay)

    dynamic_params.dist_last = dist_ped_building_center_list # Save distance for next iteration
    dist_index = np.argsort(dist_ped_building_center_list)   # Indices of pedestrians, from closest to furthest from building center

    ###############################################
    ############### LINE OF SIGHT   ###############
    ###############################################
    # Transform point cloud data:
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    time.sleep(0.05)
    data = rospy.wait_for_message("/velodyne_points2", PointCloud2)
    transform = tf_buffer.lookup_transform('odom', 'velodyne2', rospy.Time(0))
    data_odom = do_transform_cloud(data, transform)
    generator = point_cloud2.read_points(data_odom, field_names = ("x", "y", "z"), skip_nans=True)
    cloud = []
    for point in generator:
        cloud.append(point)
    x = extract_xyz(cloud, 0); y = extract_xyz(cloud, 1); z = extract_xyz(cloud, 2);

    # Filter point cloud information by z:
    cloud_x = []; cloud_y = [];
    for p in range(len(z)):
        if (z[p] > z_min) and (z[p] < z_max):
            cloud_x.append(x[p]); cloud_y.append(y[p]);

    # Gather pedestrian information:
    ped_x_all = []; ped_y_all = []; dist_robot_ped = [];
    ped_x_in_range = []; ped_y_in_range = []; ped_num_in_range = [];

    # Check if pedestrians are in range:
    for j in range(len(ped.agent_states)):
        current_ped_x = ped.agent_states[j].pose.position.x
        current_ped_y = ped.agent_states[j].pose.position.y
        ped_x_all.append(current_ped_x); ped_y_all.append(current_ped_y)
        dist_robot_ped = get_distance(robot_xy[0], current_ped_x, robot_xy[1], current_ped_y)
        if dist_robot_ped < robot_range:
            ped_x_in_range.append(current_ped_x); ped_y_in_range.append(current_ped_y);
            ped_num_in_range.append(j)

    # Line of sight detection:
    # For every single pedestrian, check if obstacles are blocking the way
    dynamic_params.ped_x_los = []; dynamic_params.ped_y_los = []; dynamic_params.ped_num_los = []
    for k in range(len(ped_x_in_range)):
        current_ped_x = ped_x_in_range[k];
        current_ped_y = ped_y_in_range[k];
        current_ped_num = ped_num_in_range[k];

        # Check to make sure the point cloud points fall between the robot
        # and the pedestrian...
        export_point = False
        cloud_x_in_boundary = []; cloud_y_in_boundary = [];
        for j in range(len(cloud_x)):
            if (current_ped_x > robot_xy[0]) and (current_ped_y > robot_xy[1]):
                if (robot_xy[0] - robot_tol) < cloud_x[j] < (current_ped_x - ped_tol):
                    if (robot_xy[1] - robot_tol) < cloud_y[j] < (current_ped_y - ped_tol):
                        export_point = True
            elif (current_ped_x > robot_xy[0]) and (current_ped_y < robot_xy[1]):
                if (robot_xy[0] - robot_tol) < cloud_x[j] < (current_ped_x - ped_tol):
                    if (current_ped_y + ped_tol) < cloud_y[j] < (robot_xy[1] + robot_tol):
                        export_point = True
            elif (current_ped_x < robot_xy[0]) and (current_ped_y > robot_xy[1]):
                if (current_ped_x + ped_tol) < cloud_x[j] < (robot_xy[0] + robot_tol):
                    if (robot_xy[1] - robot_tol) < cloud_y[j] < (current_ped_y - ped_tol):
                        export_point = True
            elif (current_ped_x < robot_xy[0]) and (current_ped_y < robot_xy[1]):
                if (current_ped_x + ped_tol) < cloud_x[j] < (robot_xy[0] + robot_tol):
                    if (current_ped_y + ped_tol) < cloud_y[j] < (robot_xy[1] + robot_tol):
                        export_point = True
            if export_point == True:
                cloud_x_in_boundary.append(current_ped_x)
                cloud_y_in_boundary.append(current_ped_y)

        # Check if a point cloud point lies between ped and robot
        # within a straight line deviation tolerance
        allow_pedestrian = True
        for j in range(len(cloud_x_in_boundary)):
            ABC = linear_const(robot_xy[0], current_ped_x, robot_xy[1], current_ped_y)
            dist = linear_dist(ABC[0], ABC[1], ABC[2], cloud_x_in_boundary[j], cloud_y_in_boundary[j])
            if dist < los_dev:
                allow_pedestrian = False
        if (allow_pedestrian == True):
            dynamic_params.ped_x_los.append(current_ped_x)
            dynamic_params.ped_y_los.append(current_ped_y)
            dynamic_params.ped_num_los.append(current_ped_num)

    dynamic_params.ped_x_excl = ped_x_all[:]
    dynamic_params.ped_y_excl = ped_y_all[:]
    for k in reversed(dynamic_params.ped_num_los):
        del dynamic_params.ped_x_excl[k]
        del dynamic_params.ped_y_excl[k]

    dynamic_params.robot_xy = robot_xy[:]
    dynamic_params.cloud_x = cloud_x[:]
    dynamic_params.cloud_y = cloud_y[:]
    dynamic_params.map_range = 50 + get_distance(robot_xy[0], 0, robot_xy[1], 0)
    print("- Available Peds: %d / %d" % (len(dynamic_params.ped_x_los), len(ped_x_all)))

    ###################################################
    ############### Ped Selection Logic ###############
    ###################################################

    # If in movement phase 1, we want to follow the best pedestrian
    if phase == 1:
        # Pedestrian selection only after first iteration
        if i > 0:

            # Loop through pedestrians from closest to furthest from building center
            for idx in dist_index:

                # Check if pedestrian is in line of sight (los):
                ped_in_los = False
                for k in range(len(dynamic_params.ped_num_los)):
                    if idx == dynamic_params.ped_num_los[k]:
                        ped_in_los = True

                if (ped_in_los == True):
                    # Additional flags for ped location:
                    ped_coord = [ped.agent_states[idx].pose.position.x, ped.agent_states[idx].pose.position.y]
                    ped_not_excl_zone_0 = (not contains_pt(ped_coord, dynamic_params.exclusion_zones[0]))
                    ped_not_excl_zone_1 = (not contains_pt(ped_coord, dynamic_params.exclusion_zones[1]))
                    ped_not_remove_zone = (not ped_in_remove_zone(ped_coord))
                    ped_not_recent_hist = (not ped_in_recent_hist(ped_coord, 3))
                    robot_in_excl_zone = (contains_pt(robot_xy, dynamic_params.exclusion_zones[1]))

                    if (ped_not_recent_hist == False):
                        print("--- Ped %d is in recent history. Skipped!" % idx)

                    # Only follow a pedestrian if it is not within the problem area outside eng faculty
                    if (ped_not_excl_zone_0 == True) and (ped_not_remove_zone == True) and (ped_not_recent_hist == True):

                        # Only follow a pedestrian if it is not in the dynamically created exclusion zone around the robot's starting point
                        if (ped_not_excl_zone_1 == True) or (robot_in_excl_zone == True):
                            dist_ped_building = dist_ped_building_center = get_distance(building_center_xy[0], ped_coord[0], building_center_xy[1], ped_coord[1])

                            if dist_ped_building < dist_robot_building_center:
                                # Only follow a pedestrian if their velocity is -ve (distance is decreasing)
                                if vel[idx] < 0:
                                    best_ped_smart = idx
                                    dist_robot_ped = dist_robot_ped_list[idx]
                                    ped_found = 1
                                    break

            # Update navigation goal if the selection logic found a pedestrian to follow
            if ped_found:
                print("- Phase 1: Following Ped %d" % (best_ped_smart))
                print("--- Ped %d is %.2fm from the robot" % (best_ped_smart, dist_robot_ped))
                print("--- Ped %d is %.1fm from the building center" % (best_ped_smart, dist_robot_building_center))
                dynamic_params.goal_xy = [ped.agent_states[best_ped_smart].pose.position.x, ped.agent_states[best_ped_smart].pose.position.y]
                dynamic_params.ped_last = dynamic_params.goal_xy
            else:
                print("- Phase 1: Did not find a pedestrian to follow")
                best_ped_smart = 8725

        else:
            print("- Please wait for the next iteration...")
            best_ped_smart = 8725       # junk, will not be used. Just need to set it to something

    # If in movement phase 3, we simply want to follow the closest pedestrian to the robot and ignore other conditions
    elif phase == 3:

        # Loop through pedestrians from closest to furthest from building center
        for idx in dist_index:

            # Check if pedestrian is in line of sight:
            ped_in_los = False
            for k in range(len(dynamic_params.ped_num_los)):
                if idx == dynamic_params.ped_num_los[k]:
                    ped_in_los = True

            # Only follow a pedestrian if it is within range of robot but not already within the threshold (otherwise the program will believe the robot has already reached the goal and will reset for another loop)
            if (ped_in_los == True) and (dist_robot_ped_list[idx] > target_threshold):

                # Only follow a pedestrian if it is not within the problem area outside eng faculty (usually not needed, but there are situations where if the navigation is started at a poor time the algorithm can fail)
                ped_coord = [ped.agent_states[idx].pose.position.x, ped.agent_states[idx].pose.position.y]
                ped_not_excl_zone_0 = (not contains_pt(ped_coord, dynamic_params.exclusion_zones[0]))
                ped_not_excl_zone_1 = (not contains_pt(ped_coord, dynamic_params.exclusion_zones[1]))
                ped_not_remove_zone = (not ped_in_remove_zone(ped_coord))
                ped_not_recent_hist = (not ped_in_recent_hist(ped_coord, 2))
                robot_in_excl_zone = (contains_pt(robot_xy, dynamic_params.exclusion_zones[1]))

                if (ped_not_recent_hist == False):
                    #print("--- Ped %d is in recent history. Skipped!" % idx)
                    pass

                if (ped_not_excl_zone_0 == True) and (ped_not_remove_zone == True) and (ped_not_recent_hist == True):

                    # Only follow a pedestrian if it is not in the dynamically created exclusion zone around the robot's starting point
                    if (ped_not_excl_zone_1 == True) or (robot_in_excl_zone == True):
                        # Only follow a pedestrian if they are closer to the robot than the previously checked pedestrian
                        if ped_found == 0:  # found the first potential ped, so there is no previous ped to compare to
                            best_ped_smart = idx
                            dist_robot_ped = dist_robot_ped_list[idx]
                            ped_found = 1
                        else:
                            if dist_robot_ped_list[idx] < dist_robot_ped:
                                best_ped_smart = idx
                                dist_robot_ped = dist_robot_ped_list[idx]

        # Update navigation goal if the selection logic found a pedestrian to follow
        if ped_found:
            print("- Phase 3: Following Ped %d" % (best_ped_smart))
            print("--- Ped %d is %.2fm from the robot" % (best_ped_smart, dist_robot_ped))
            print("--- Ped %d is %.1fm from the building center" % (best_ped_smart, dist_robot_building_center))
            dynamic_params.goal_xy = [ped.agent_states[best_ped_smart].pose.position.x, ped.agent_states[best_ped_smart].pose.position.y]

        else:
            print("- Phase 3: Did not find a pedestrian to follow")
            best_ped_smart = 8725   # junk, won't be used. Just need to set it to something

    else:
        print("ERR: select_ped_outside_vicinity(): phase must be 1 or 3")

    return ped_found, best_ped_smart
