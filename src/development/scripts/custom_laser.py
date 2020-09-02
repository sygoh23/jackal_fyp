#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf
import numpy as np
import math
import time
import pickle

rospy.init_node('laser_scan_publisher')
scan_pub = rospy.Publisher('custom/scan', LaserScan, queue_size=50)
num_readings = 600
laser_frequency = 40
count = 0
time.sleep(3)
r = rospy.Rate(2)

while not rospy.is_shutdown():
    current_time = rospy.Time.now()
    scan = LaserScan()
    scan.header.stamp = current_time
    scan.header.frame_id = 'custom_laser_frame'
    scan.angle_min = 0
    scan.angle_max = 6.28
    scan.angle_increment = 6.28 / num_readings
    scan.time_increment = (1.0 / laser_frequency) / (num_readings)
    scan.range_min = 1.0
    scan.range_max = 50.0
    msg = rospy.wait_for_message("/odometry/filtered", Odometry)
    (R, P, Y) = tf.transformations.euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
    if Y < 0:
        robot_angle = 2*math.pi-abs(Y)
    else:
        robot_angle = Y

    remove_X = pickle.load(open("/home/ubuntu/x.pkl", "rb"))
    remove_Y = pickle.load(open("/home/ubuntu/y.pkl", "rb"))

    # Translate cartesian coordinates:
    delta_X = [A-msg.pose.pose.position.x for A in remove_X]
    delta_Y = [A-msg.pose.pose.position.y for A in remove_Y]

    # Compute ray tracing angle:
    ref_angles = []
    ref_dist = []
    for j in range(len(remove_X)):
        del_X = delta_X[j]
        del_Y = delta_Y[j]
        if (del_X > 0 and del_Y > 0):
            angle = np.arctan(del_Y/del_X)
        elif (del_X < 0 and del_Y > 0):
            angle = math.pi+np.arctan(del_Y/del_X)
        elif (del_X < 0 and del_Y < 0):
            angle = math.pi+np.arctan(del_Y/del_X)
        elif (del_X > 0 and del_Y < 0):
            angle = 2*math.pi+np.arctan(del_Y/del_X)
        ref_angles.append(angle)
        ref_dist.append(math.sqrt(del_X**2+del_Y**2))

    # Perform rotation compensation:
    rotated_angles = [A-robot_angle for A in ref_angles]
    final_angles = []
    for i in range(len(rotated_angles)):
        if rotated_angles[i] > 0:
            final_angles.append(rotated_angles[i])
        else:
            final_angles.append(2*math.pi+rotated_angles[i])
    ref_angles = final_angles[:]
    scan.ranges = []
    scan.intensities = []

    # Output laser rays:
    for i in range(0, num_readings):
        ray_angle = 2*i*math.pi/num_readings
        extract_dist = []
        for j in range(len(ref_dist)):
            extract_angle = ref_angles[j]
            sample_dist = ref_dist[j]
            threshold = 1.5/(2*math.pi*sample_dist)*(600/num_readings)
            #threshold = 1/(sample_dist**(2))
            #if (threshold < 0.05): threshold = 0.05
            if (abs(extract_angle - ray_angle) < threshold):
                extract_dist.append(ref_dist[j])
        if len(extract_dist) > 0:
            scan.ranges.append(min(extract_dist))
            scan.intensities.append(1)
        else:
            scan.ranges.append(100)
            scan.intensities.append(0)
    scan_pub.publish(scan)
    count += 1
    r.sleep()
