sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
roslaunch development full_simulation.launch
