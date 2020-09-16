#!/usr/bin/env python
from math import sqrt
import rospy
import time
import tf
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import matplotlib
import matplotlib.pyplot as plt
from pedsim_msgs.msg import AgentStates
from nav_msgs.msg import Odometry
time.sleep(1)

def get_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def get_robot_xy():
    odom = rospy.wait_for_message("/odometry/filtered", Odometry)
    return [odom.pose.pose.position.x, odom.pose.pose.position.y]

def extract_x(list):
    return [item[0] for item in list]

def extract_y(list):
    return [item[1] for item in list]

def extract_z(list):
    return [item[2] for item in list]

robot_range = 75
z_min = 1
z_max = 2
while True:
    rospy.init_node('los_detection', anonymous=True)

    # Transform point cloud data:
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    data = rospy.wait_for_message("/velodyne_points2", PointCloud2)
    transform = tf_buffer.lookup_transform('odom', 'velodyne2', rospy.Time(0))
    data_odom = do_transform_cloud(data, transform)
    generator = point_cloud2.read_points(data_odom, field_names = ("x", "y", "z"), skip_nans=True)
    cloud = []
    for point in generator:
        cloud.append(point)
    x = extract_x(cloud); y = extract_y(cloud); z = extract_z(cloud);

    # Filter point cloud information by z:
    cloud_x = []; cloud_y = [];
    for i in range(len(z)):
        if (z[i] > z_min) and (z[i] < z_max):
            cloud_x.append(x[i]); cloud_y.append(y[i]);

    # Gather pedestrian information:
    robot = get_robot_xy()
    ped_x_all = []; ped_y_all = []; dist_robot_ped = [];
    ped_x_in_range = []; ped_y_in_range = []; ped_num_in_range = [];
    peds = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    for j in range(len(peds.agent_states)):
        current_ped_x = peds.agent_states[j].pose.position.x
        current_ped_y = peds.agent_states[j].pose.position.y
        ped_x_all.append(current_ped_x)
        ped_y_all.append(current_ped_y)
        dist_robot_ped = get_distance(robot[0], current_ped_x, robot[1], current_ped_y)
        if dist_robot_ped < robot_range:
            ped_x_in_range.append(current_ped_x)
            ped_y_in_range.append(current_ped_y)
            ped_num_in_range.append(j)

    # Line of sight detection:
    for k in range(len(ped_x_in_range)):
        current_ped_x = ped_x_in_range[k];
        current_ped_y = ped_x_in_range[k];


    # Plotting the image:
    plt.scatter(robot[0], robot[1], c='b', marker='*', s=50)
    plt.scatter(cloud_x, cloud_y, c='dimgray', marker='.', s=5)
    plt.scatter(ped_x_all, ped_y_all, c='r', marker='.', s=10)
    plt.scatter(ped_x_in_range, ped_y_in_range, c='g', marker='.', s=15)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("/home/ubuntu/LOS.png")
    plt.clf()
    time.sleep(5)
