# Launches Jackal simulation with the following features:
## ped: Pedsim Simulator
## nav: Navigation Stack (move_base)
sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
roslaunch development ped_nav.launch
