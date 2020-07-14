from ped_selection import *
from threading import Timer
from static_params import *
import dynamic_params
from utils import *
from pedsim_msgs.msg import AgentStates
import rospy


def follow_closest_ped(idx):
    ped = rospy.wait_for_message("/pedsim_simulator/simulated_agents", AgentStates)
    ped_xy = [ped.agent_states[idx].pose.position.x, ped.agent_states[idx].pose.position.y]
    robot_xy = get_robot_xy()
    dist_robot_ped = get_distance(robot_xy[0], ped_xy[0], robot_xy[1], ped_xy[1])

    # Keep following if the ped is within range and robot hasn't moved the desired cumulative distance yet
    if dist_robot_ped > robot_range:
        print("- Phase 3: Ped %d out of range" % dynamic_params.ped_number)
        #dynamic_params.goal_xy = robot_xy           # Set the goal as the robot's current position so that it doesn't keep moving to the last position of the random ped
        dynamic_params.following_ped = 0            # Reset the following_ped flag
        dynamic_params.out_of_range = 1
    elif dynamic_params.total_dist > phase3_dist:
        print("- Phase 3: Moved required distance")
        dynamic_params.goal_xy = robot_xy           # Set the goal as the robot's current position so that it doesn't keep moving to the last position of the random ped
        dynamic_params.following_ped = 0            # Reset the following_ped flag
    else:
        # Set goal as position of target ped
        dynamic_params.goal_xy = [ped_xy[0], ped_xy[1]]

        # Increment total distance by the straight line distance that the robot has moved since last time this function was called
        distance_moved = get_distance(robot_xy[0], dynamic_params.robot_xy_prev[0], robot_xy[1], dynamic_params.robot_xy_prev[1])
        dynamic_params.total_dist += distance_moved
        dynamic_params.robot_xy_prev = robot_xy
        #print("- Distance moved since last iteration: %.2fm" % distance_moved)
        print("- Phase 3: Total distance moved = %.2fm" % dynamic_params.total_dist)


# Now in movement phase 3
# Must be in a function so that it can be triggered by the timer
def phase3_movement():
    #print("- Phase 3: Timer triggered")

    # Set the robot goal as a specified number of metres towards the building center in a straight line
    #print("- Moving towards building center...")
    #dynamic_params.goal_xy = get_straight_line_pos("building_center", straight_line_dist)

    # Select ped that is closest to the robot regardless of velocity or other conditions
    ped_found, dynamic_params.ped_number = select_ped_outside_vicinity(3, 0)
    if ped_found:
        #dynamic_params.ped_last = []                    # Clear last detected ped so the program doesn't revert back to phase 2
        dynamic_params.total_dist = 0                   # Init cumulative distance to 0
        dynamic_params.robot_xy_prev = get_robot_xy()   # Init previous robot position to the current robot position
        dynamic_params.following_ped = 1                # Set the following_ped flag so that the pedestrian following will begin
        dynamic_params.out_of_range = 0                 # Reset out_of_range flag so program knows the ped is in range
        follow_closest_ped(dynamic_params.ped_number)
    
    # Probably need to set some other flag to tell program that the timer shouldn't be set again
    # Instead keep calling follow_last_ped until distance/time limit is up

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
        --> In case a), the robot continues moving to the last known position of the ped until it has moved x metres or reaches the goal. Then it reverts to phase 3 (i.e. look for a new closest ped to follow)
        --> In case b), the robot stops and reverts to phase 3 (i.e. look for a new closest ped to follow)
        --> In case c), the robot reverts to phase 1

--> Robot pauses between each movement section for a specified number of seconds, to wait for pedestrians to appear
--> Pedestrian scanning is continually taking place, and the robot will exit this 'no ped' behaviour as soon as a suitable pedestrian is found
--> The phase 3 logic can be replaced with some other logic by editing phase3_movement()
"""
def move_without_peds_outside_vicinity():
    #robot_xy = get_robot_xy()

    # A last detected ped exists (list is non-empty)
    if dynamic_params.ped_last:
        print("- Phase 2: Moving to last detected pedestrian from phase 1")
        dynamic_params.goal_xy = dynamic_params.ped_last    # Set goal as last pedestrian position
        dynamic_params.ped_last = []                        # Clear the last pedestrian position
        dynamic_params.moving_to_last_ped = 1               # Set flag indicating robot is moving to location of last detected ped
    
    # No last detected ped exists AND the robot is not in the middle of moving towards a last detected ped
    elif dynamic_params.moving_to_last_ped == 0:
        # if an if statement goes here with a flag set in phase3_movement, then follow_closest will be run again 
        # which will update the goal and therefore the distance will never be below the threshold so the timer will 
        # not be started again. But if say the ped goes out of range, then the goal won't be updated and it'll keep 
        # moving to the last spot of the ped. Would have to set the goal to the current position of the robot in that ase
        robot_xy = get_robot_xy()   # Want this to be as close as possible to the call inside follow_closest_ped, to minimise variation
        # In the middle of following a ped
        if dynamic_params.following_ped == 1:
            follow_closest_ped(dynamic_params.ped_number)
        elif dynamic_params.out_of_range == 1:   # moving to the last ped position, the ped is now out of range. Still moving because required distance has not been covered      
            distance_moved = get_distance(robot_xy[0], dynamic_params.robot_xy_prev[0], robot_xy[1], dynamic_params.robot_xy_prev[1])
            dynamic_params.total_dist += distance_moved
            dynamic_params.robot_xy_prev = robot_xy
            #print("- Phase 3: Distance moved since last iteration: %.2fm" % distance_moved)
            print("- Phase 3: Total distance moved = %.2fm" % dynamic_params.total_dist)

            if dynamic_params.total_dist > phase3_dist:
                print("- Phase 3: Moved required distance")
                dynamic_params.goal_xy = robot_xy           # Set the goal as the robot's current position so that it doesn't keep moving to the last position of the random ped
                dynamic_params.out_of_range = 0

        dist_robot_phase3_goal = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
        #print("- Dist robot phase 3 goal = %.2f" % dist_robot_phase3_goal)

        # Robot has reached the previously set straight-line goal
        if dist_robot_phase3_goal <= target_threshold:
            # Start timer if not started already, and wait for a new ped to be detected
            print("- Phase 3: Waiting for new peds...")
            if dynamic_params.timer_set == 0:
                #print("- Phase 3: Timer started")
                dynamic_params.timer = Timer(movement_pause, phase3_movement)           # Create new countdown timer for phase3_movement
                dynamic_params.timer.start()                                            # Start timer
                dynamic_params.timer_set = 1                                            # Set timer flag
        
        # Robot is in the middle of moving towards the previously set straight-line goal
        else:
            #print("- Moving towards building center...")
            if dynamic_params.out_of_range == 1:
                print("- Phase 3: Moving toward ped %d last position" % dynamic_params.ped_number)
            else:
                print("- Phase 3: Following ped %d" % dynamic_params.ped_number)
    else:
        # Robot has reached the last ped position and is waiting for a new ped to be detected
        if dynamic_params.timer_set == 1:
            print("- Phase 2: Waiting for new peds...")
        
        # Robot is in the middle of moving towards the last detected ped
        else:
            print("- Phase 2: Moving to last detected pedestrian from phase 1")

            # Check if robot has reached the last ped position. If it has, then start the timer and wait
            robot_xy = get_robot_xy()
            dist_robot_last_ped = get_distance(robot_xy[0], dynamic_params.goal_xy[0], robot_xy[1], dynamic_params.goal_xy[1])
            if dist_robot_last_ped <= target_threshold:
                print("- Phase 2: Reached last detected pedestrian")
                dynamic_params.timer = Timer(movement_pause, phase3_movement)           # Create new countdown timer for phase3_movement
                dynamic_params.timer.start()                                            # Start timer
                dynamic_params.timer_set = 1                                            # Set timer flag
                # Set no-go zone here?