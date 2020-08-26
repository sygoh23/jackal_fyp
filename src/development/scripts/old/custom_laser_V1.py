#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf
import numpy as np
import math

rospy.init_node('laser_scan_publisher')
scan_pub = rospy.Publisher('custom/scan', LaserScan, queue_size=50)

num_readings = 100
laser_frequency = 40

count = 0
r = rospy.Rate(10)
while not rospy.is_shutdown():
    current_time = rospy.Time.now()
    scan = LaserScan()
    scan.header.stamp = current_time
    scan.header.frame_id = 'custom_laser_frame'
    scan.angle_min = 0
    scan.angle_max = 6.28
    scan.angle_increment = 3.14 / num_readings
    scan.time_increment = (1.0 / laser_frequency) / (num_readings)
    scan.range_min = 0.0
    scan.range_max = 100.0

    msg = rospy.wait_for_message("/odometry/filtered", Odometry)
    (R, P, Y) = tf.transformations.euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])
    print("Robot X: %d | Robot Y: %d | Robot Angle: %.2f" % (msg.pose.pose.position.x, msg.pose.pose.position.x,Y))

    BAD_X = 5
    BAD_Y = 5
    TRANS_X = BAD_X - msg.pose.pose.position.x
    TRANS_Y = BAD_Y - msg.pose.pose.position.y
    print([TRANS_X, TRANS_Y])

    if (TRANS_X > 0 and TRANS_Y > 0):
        angle = np.arctan(TRANS_Y/TRANS_X)
        print("1: %f" % (angle*180/math.pi))
    elif (TRANS_X < 0 and TRANS_Y > 0):
        angle = math.pi+np.arctan(TRANS_Y/TRANS_X)
        print("2: %f" % (angle*180/math.pi))
    elif (TRANS_X < 0 and TRANS_Y < 0):
        angle = math.pi+np.arctan(TRANS_Y/TRANS_X)
        print("3: %f" % (angle*180/math.pi))
    elif (TRANS_X > 0 and TRANS_Y < 0):
        angle = math.pi+np.arctan(TRANS_Y/TRANS_X)
        print("4: %f" % (angle*180/math.pi))

    scan.ranges = []
    scan.intensities = []
    print("Ray Angle: %.2f" % ((count*math.pi/num_readings)*180/math.pi))
    for i in range(0, count):
        scan.ranges.append(10.0)  # fake data
        scan.intensities.append(1)  # fake data

    if count == 2*num_readings:
        count = 0

    scan_pub.publish(scan)
    count += 1
    r.sleep()
