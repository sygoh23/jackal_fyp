# Launches Jackal simulation with the following features:
## ped: Pedsim Simulator
sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
roslaunch development ped.launch
