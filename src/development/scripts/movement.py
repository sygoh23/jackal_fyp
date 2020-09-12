"""
Contains movement logic.
Currently all functions are for when the robot is in stage 1 and there are no detected phase 1 pedestrians. Nothing in here for stage 2 (yet).
"""

from ped_selection import *
from threading import Timer
from static_params import *
import dynamic_params
from utils import *
from pedsim_msgs.msg import AgentStates
import rospy

import cv2
import pickle
import sys
import numpy as np
import itertools
import matplotlib.pyplot as plt


# Used once object detection has found a doorway
def move_to_doorway():
    pass


"""
Movement logic when the robot is within the building vicinity
--> Assumes there is only one doorway in the defined building vicinity
"""
def move_within_vicinity(target_xy):
    
    ##########################################################################
    # Point cloud filtering
    ##########################################################################

    # Retrieve pointcloud scan
    pointcloud = get_pointcloud()

    # Process data
    x = []
    y = []
    for point in pointcloud:
        if point[2] > 0.5:
            x.append(point[0])
            y.append(point[1])
    
    # Scatterplot in robot frame
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
    ax.scatter(x, y)
    ax.scatter(0, 0, color='g', s=100)
    ax.scatter(target_xy[0], target_xy[1], color='r', s=100)


    ##########################################################################
    # Robot frame -> image space
    ##########################################################################

    # Convert to numpy array
    x_min = min(x)  # -67.5
    y_min = min(y)  # -100.6
    w = int(max(x) - x_min) + 2     # max x = 61.5
    h = int(max(y) - y_min) + 2     # max y = 95.7
    c = 3

    img = np.zeros((w, h, c), dtype=np.uint8)

    for pt_x, pt_y in zip(x, y):
        # Translate
        pt_x += abs(x_min)
        pt_y += abs(y_min)

        img[int(pt_x), int(pt_y), :] = [255, 255, 255]


    ##########################################################################
    # Hough transform
    ##########################################################################

    # Convert image to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find edges in the image using canny detector
    edges = cv2.Canny(gray, 50, 200)

    # Run the Hough transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=40, minLineLength=20, maxLineGap=70)

    # Save lines
    if lines is not None:
        lines_list = []     # [np.array[x1, y1, x2, y2], ...]
        for line in lines:
            x1, y1, x2, y2 = line[0]
            lines_list.append(line[0])
            #cv2.line(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
            
        # Show/save result
        #cv2.imwrite("/home/chris/Documents/HoughTransform.jpg", img)
        #cv2.imshow("Result Image", img)
        #cv2.waitKey()

    else:
        print("No lines found")


    ##########################################################################
    # Image space -> robot frame
    ##########################################################################


    """
    # Read image 
    img = cv2.imread('/home/chris/Documents/test4.jpg', cv2.IMREAD_COLOR)
    #cv2.imshow("Initial", img)
    #cv2.waitKey()

    # Convert the image to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Gray", gray)
    #cv2.waitKey()

    # Find the edges in the image using canny detector
    edges = cv2.Canny(gray, 50, 200)
    #cv2.imshow("Edges", gray)
    #cv2.waitKey()

    # Detect points that form a line
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=60, minLineLength=160, maxLineGap=250)

    # Draw lines on the image
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

    # Show result
    #cv2.imwrite("/home/chris/Documents/HoughTransform.jpg", img)
    #cv2.imshow("Result Image", img)
    #cv2.waitKey()
    """

    # Select line, and a target coordinate

    # Transform point back to robot frame cartesian x/y
    # return wall_xy

    """
    with open('/home/chris/Documents/pointcloud2.pickle', 'wb') as f:
        pickle.dump(pointcloud, f)
    """

    #sys.exit()
    

    # If this goal point is outside the building vicinity, generate another point
    #while not contains_pt(dynamic_params.goal_xy, building_polygon):
        #print("--> Current goal is outside vicinity, generating new goal...")
    
    # Scan for doorways
    print("--> Looking for doorway")


"""
Used in phase 3. Sets the robot goal as the closest pedestrian to the robot, regardless of their direction of movement or other constraints imposed in phase 1
--> Will be called repeatedly in phase 3 until a) ped is out of range, b) robot has moved x metres, c) a phase 1 ped is found
--> idx = index of the pedestrian to set the goal as
"""
def follow_closest_ped(idx):

    # Get position data for desired ped
    ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    ped_xy = [ped.agent_states[idx].pose.position.x, ped.agent_states[idx].pose.position.y]
    robot_xy = get_robot_xy()
    dist_robot_ped = get_distance(robot_xy[0], ped_xy[0], robot_xy[1], ped_xy[1])

    # Follow ped if they are within range and robot hasn't moved the desired cumulative distance yet
    if dist_robot_ped > robot_range:
        print("- Phase 3: Ped %d out of range" % idx)

        # Reset the following_ped flag to indicate robot is no longer following a phase 3 ped
        dynamic_params.following_ped = 0   

        # Set out_of_range flag to indicate that the ped is out of range, but the robot hasn't moved the required distance yet
        dynamic_params.out_of_range = 1    

    elif dynamic_params.total_dist > phase3_dist:
        print("- Phase 3: Moved required distance")

        # Set the goal as the robot's current position so that it doesn't keep moving to the last position of this ped
        dynamic_params.goal_xy = robot_xy      

        # Reset the following_ped flag to indicate robot is no longer following a phase 3 ped     
        dynamic_params.following_ped = 0    

    else:
        # Set goal as position of target ped
        dynamic_params.goal_xy = [ped_xy[0], ped_xy[1]]

        # Increment total distance by the straight line distance that the robot has moved since last time this function was called
        distance_moved = get_distance(robot_xy[0], dynamic_params.robot_xy_prev[0], robot_xy[1], dynamic_params.robot_xy_prev[1])
        dynamic_params.total_dist += distance_moved
        dynamic_params.robot_xy_prev = robot_xy
        #print("- Distance moved since last iteration: %.2fm" % distance_moved)
        print("- Phase 3: Total distance following ped %d = %.2fm" % (idx, dynamic_params.total_dist))


"""
Contains the logic to move the robot when phase 3 is triggered by the timer
--> Must be inside its own function so that the timer can trigger it
"""
def phase3_movement():

    #print("- Phase 3: Timer triggered")

    # Set the robot goal as a specified number of metres towards the building center in a straight line
    #print("- Moving towards building center...")
    #dynamic_params.goal_xy = get_straight_line_pos("building_center", straight_line_dist)

    # Select ped that is closest to the robot regardless of velocity or other conditions
    ped_found, dynamic_params.ped_number = select_ped_outside_vicinity(3, 0)
    if ped_found:
        #dynamic_params.ped_last = []                   # Clear last detected ped so the program doesn't revert back to phase 2
        dynamic_params.total_dist = 0                   # Init cumulative distance to 0
        dynamic_params.robot_xy_prev = get_robot_xy()   # Init previous robot position to the current robot position
        dynamic_params.following_ped = 1                # Set the following_ped flag so that the pedestrian following will begin
        dynamic_params.out_of_range = 0                 # Reset out_of_range flag so program knows the ped is in range
        follow_closest_ped(dynamic_params.ped_number)

    # If function call was triggered because of the timer, reset the timer flag
    if dynamic_params.timer_set == 1:
        dynamic_params.timer_set = 0
    
    # If function call was triggered because robot has reached last detected pedestrian, reset the moving_to_last_ped flag
    if dynamic_params.moving_to_last_ped == 1:
        dynamic_params.moving_to_last_ped = 0


"""
Used to set the robot navigation goal when no peds are found to follow
--> First enters phase 2: sets the goal as the position of the last detected phase 1 pedestrian
--> Then enters phase 3:
    --> Option A) set the goal as a specified number of metres in the straight-line direction of the building center
        --> Upon reaching the straight-line goal, it sets a new straight-line goal
        --> Straight-line goals are continually set until a) a pedestrian is found, or b) the target building vicinity is reached
    --> Option B) follow the closest ped ignoring the usual constraints on velocity
        --> Continues following the selected ped until a) ped is out of range, b) robot has moved x metres, c) a phase 1 ped is found
        --> In case a), the robot continues moving to the last known position of the ped until it has moved x metres, or reaches the goal, or a phase 1 ped is found. Then it repeats phase 3
        --> In case b), the robot stops. Then it repeats phase 3
        --> In case c), the robot reverts to phase 1
--> Robot pauses between each movement section for a specified number of seconds
--> The phase 3 logic can be replaced with some other logic by editing phase3_movement()
"""
def move_without_peds_outside_vicinity():

    # A last detected phase 1 ped exists (list is non-empty). I.e. this is phase 2
    if dynamic_params.ped_last:
        print("- Phase 2: Moving to last detected pedestrian from phase 1")
        dynamic_params.goal_xy = dynamic_params.ped_last    # Set goal as last pedestrian position
        dynamic_params.ped_last = []                        # Clear the last pedestrian position
        dynamic_params.moving_to_last_ped = 1               # Set flag indicating robot is moving to location of last detected ped
    
    # No last detected phase 1 ped exists AND the robot is not in the middle of moving towards a last detected phase 1 ped. I.e. this is phase 3
    elif dynamic_params.moving_to_last_ped == 0:
        # Want this call to get_robot_xy() to be as close as possible to the call inside follow_closest_ped, to minimise variation
        robot_xy = get_robot_xy()   
        
        # Robot is in the middle of following a phase 3 ped. In this case run follow_closest_ped() again to update goal
        if dynamic_params.following_ped == 1:
            follow_closest_ped(dynamic_params.ped_number)

        # Phase 3 ped has moved out of range, but the required distance has not yet been covered. Keep moving to the ped's last detected position  
        elif dynamic_params.out_of_range == 1:       
            # Increment the distance moved
            distance_moved = get_distance(robot_xy[0], dynamic_params.robot_xy_prev[0], robot_xy[1], dynamic_params.robot_xy_prev[1])
            dynamic_params.total_dist += distance_moved
            dynamic_params.robot_xy_prev = robot_xy
            #print("- Phase 3: Distance moved since last iteration: %.2fm" % distance_moved)
            print("- Phase 3: Total distance following ped %d = %.2fm" % (dynamic_params.ped_number, dynamic_params.total_dist))

            # If the required distance has been covered, reset the out_of_range flag and repeat phase 3
            if dynamic_params.total_dist > phase3_dist:
                print("- Phase 3: Moved required distance")
                dynamic_params.goal_xy = robot_xy           # Set the goal as the robot's current position so that it doesn't keep moving to the last position of the random ped
                dynamic_params.out_of_range = 0

        # Distance between robot and current goal point
        dist_robot_phase3_goal = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
        #print("- Dist robot phase 3 goal = %.2f" % dist_robot_phase3_goal)

        # Robot has reached the previously set goal point (by reaching the last detected phase 3 ped position, or by covering the required distance)
        if dist_robot_phase3_goal <= target_threshold:
            print("- Phase 3: Waiting for new peds...")

            # Start timer if not started already, and wait for a new ped to be detected
            if dynamic_params.timer_set == 0:
                #print("- Phase 3: Timer started")
                dynamic_params.timer = Timer(movement_pause, phase3_movement)           # Create new countdown timer for phase3_movement
                dynamic_params.timer.start()                                            # Start timer
                dynamic_params.timer_set = 1                                            # Set timer flag
        
        # Robot is in the middle of moving towards the previously set goal point
        else:
            # If the phase 3 ped is out of range, robot must be moving towards its last detected position
            if dynamic_params.out_of_range == 1:
                print("- Phase 3: Moving toward ped %d last position" % dynamic_params.ped_number)
            
            # Otherwise, phase 3 ped is in range and robot must be following it
            else:
                print("- Phase 3: Following ped %d" % dynamic_params.ped_number)
    else:
        # Robot has reached the last detected phase 1 ped position and is waiting for a new ped to be detected
        if dynamic_params.timer_set == 1:
            print("- Phase 2: Waiting for new peds...")
        
        # Robot is in the middle of moving towards the last detected phase 1 ped
        else:
            print("- Phase 2: Moving to last detected pedestrian from phase 1")

            # Calculate distance to last phase 1 ped position
            robot_xy = get_robot_xy()
            dist_robot_last_ped = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])

            # Check if robot has reached the last phase 1 ped position. If it has, then start the timer and wait
            if dist_robot_last_ped <= target_threshold:
                print("- Phase 2: Reached last detected pedestrian")
                dynamic_params.timer = Timer(movement_pause, phase3_movement)           # Create new countdown timer for phase3_movement
                dynamic_params.timer.start()                                            # Start timer
                dynamic_params.timer_set = 1                                            # Set timer flag