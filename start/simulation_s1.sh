# Launches Jackal simulation with pedestrians and gazebo integration...
sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
roslaunch development simulation_stage_1.launch
