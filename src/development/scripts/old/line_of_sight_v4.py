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

def linear_const(x1, x2, y1, y2):
        return (y1-y2), (x2-x1), (x1*y2-x2*y1)

def linear_dist(A, B, C, x, y):
        return abs(A*x+B*y+C)/sqrt(A**2+B**2)

def inside_radius(x0, y0, r, x_in, y_in):
        return (x_in-x0)**2+(y_in-y0)**2<=r**2

robot_range = 75
ped_tol = 1.5
los_dev = 3
z_min = 0.1
z_max = 2
while True:
    rospy.init_node('los_detection', anonymous=True)

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
    ped_x_los = []; ped_y_los = []; ped_num_los = []
    print("\nRESULTS:")
    for k in range(len(ped_x_in_range)):
        current_ped_x = ped_x_in_range[k];
        current_ped_y = ped_y_in_range[k];
        current_ped_num = ped_num_in_range[k];

        # Check to make sure the point cloud points fall between the robot
        # and the pedestrian...
        export_point = False
        cloud_x_in_boundary = []; cloud_y_in_boundary = [];
        for j in range(len(cloud_x)):
            if (current_ped_x > robot[0]) and (current_ped_y > robot[1]):
                if robot[0] < cloud_x[j] < (current_ped_x - ped_tol):
                    if robot[1] < cloud_y[j] < (current_ped_y - ped_tol):
                        export_point = True
            elif (current_ped_x > robot[0]) and (current_ped_y < robot[1]):
                if robot[0] < cloud_x[j] < (current_ped_x - ped_tol):
                    if (current_ped_y + ped_tol) < cloud_y[j] < robot[1]:
                        export_point = True
            elif (current_ped_x < robot[0]) and (current_ped_y > robot[1]):
                if (current_ped_x + ped_tol) < cloud_x[j] < robot[0]:
                    if robot[1] < cloud_y[j] < (current_ped_y - ped_tol):
                        export_point = True
            elif (current_ped_x < robot[0]) and (current_ped_y < robot[1]):
                if (current_ped_x + ped_tol) < cloud_x[j] < robot[0]:
                    if (current_ped_y + ped_tol) < cloud_y[j] < robot[1]:
                        export_point = True
            if export_point == True:
                cloud_x_in_boundary.append(current_ped_x)
                cloud_y_in_boundary.append(current_ped_y)

        a1 = ped_num_in_range[k]
        a2 = len(cloud_x_in_boundary)
        a3 = len(cloud_x)

        allow_pedestrian = True
        for j in range(len(cloud_x_in_boundary)):
            ABC = linear_const(robot[0], current_ped_x, robot[1], current_ped_y)
            dist = linear_dist(ABC[0], ABC[1], ABC[2], cloud_x_in_boundary[j], cloud_y_in_boundary[j])
            if dist < los_dev:
                allow_pedestrian = False

        if (allow_pedestrian == True):
            ped_x_los.append(current_ped_x)
            ped_y_los.append(current_ped_y)
            ped_num_los.append(current_ped_num)
        #print("- Pedestrian %d | Boundary Score: %d / %d | LOS: %d" % (a1, a2, a3, allow_pedestrian))

    ped_x_excl = ped_x_all[:]
    ped_y_excl = ped_y_all[:]
    for k in reversed(ped_num_los):
        del ped_x_excl[k]
        del ped_y_excl[k]

    print("- Total Peds: %d" % len(ped_x_all))
    print("- Allowed Peds: %d" % len(ped_x_los))
    print("- Excluded Peds: %d" % len(ped_x_excl))

    # Plotting the image:
    plt.grid(b=True, which='major', color='#d6d6d6', linestyle='--')
    plt.scatter(robot[0], robot[1], c='b', marker='*', s=50)
    plt.scatter(cloud_x, cloud_y, c='dimgray', marker='.', s=10)
    plt.scatter(ped_x_excl, ped_y_excl, c='r', marker='.', s=20)
    plt.scatter(ped_x_los, ped_y_los, c='g', marker='.', s=30)
    plt.xlim((robot[0]-75, robot[0]+75))
    plt.ylim((robot[1]-75, robot[1]+75))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("/home/ubuntu/LOS.png")
    plt.clf()
    time.sleep(2)
