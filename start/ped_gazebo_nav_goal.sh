# Launches Jackal simulation with the following features:
## ped: Pedsim Simulator
## gazebo: Pedsim Gazebo Plugin
## nav: Navigation Stack (move_base)
## goal: Pedestrian Goal Setting
sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
roslaunch development ped_gazebo_nav_goal.launch
