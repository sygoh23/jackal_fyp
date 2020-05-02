source /opt/ros/melodic/setup.bash
source ../devel/setup.bash
sudo killall rosmaster
sudo killall gzserver
sudo killall gzclient
roslaunch jackal_gazebo jackal_world.launch
