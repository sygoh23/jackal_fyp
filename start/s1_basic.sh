# Launches Stage 1 Jackal simulation with pedestrians and gazebo integration...
sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
roslaunch development simulation_basic.launch
