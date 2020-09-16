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

def get_pointcloud():
    data = rospy.wait_for_message("/velodyne_points2", PointCloud2)
    generator = point_cloud2.read_points(data, field_names = ("x", "y", "z"), skip_nans=True)
    points_list = []
    for point in generator:
        points_list.append(point)
    return points_list

def extract_x(list):
    return [item[0] for item in list]

def extract_y(list):
    return [item[1] for item in list]

def extract_z(list):
    return [item[2] for item in list]

while True:
    time.sleep(3)
    rospy.init_node('los_detection', anonymous=True)
    tf_buffer = tf2_ros.Buffer()
    tf_listener = tf2_ros.TransformListener(tf_buffer)
    data = rospy.wait_for_message("/velodyne_points2", PointCloud2)
    transform = tf_buffer.lookup_transform('odom', 'velodyne2', rospy.Time(0))
    data_odom = do_transform_cloud(data, transform)
    generator = point_cloud2.read_points(data_odom, field_names = ("x", "y", "z"), skip_nans=True)
    cloud = []
    for point in generator:
        cloud.append(point)

    x = extract_x(cloud)
    y = extract_y(cloud)
    z = extract_z(cloud)
    print("X: " + str(sum(x)/len(x)) + " | Y: " + str(sum(y)/len(y)) + " | Z: " + str(sum(z)/len(z)))

    ped_x = []
    ped_y = []
    peds = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    for j in range(len(peds.agent_states)):
        ped_x.append(peds.agent_states[j].pose.position.x)
        ped_y.append(peds.agent_states[j].pose.position.y)

    plt.scatter(x, y, marker='.', s=50)
    plt.scatter(ped_x, ped_y, marker='x', s=50)
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.show()
    plt.savefig("/home/ubuntu/LOS.png")
    plt.clf()
    time.sleep(5)
