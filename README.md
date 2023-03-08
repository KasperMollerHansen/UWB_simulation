# UWB_simulation

### Setup
in folder opt/ros/noetic/share/gazebo_ros/launch paste the file UWB.launch as UWB.launch

in folder opt/ros/noetic/share/husky_description/urdf overwrite the file husky.urdf.xacro with husky.urdf.xacro

in folder usr/share/gazebo-11/worlds paste the file UWB.world as UWB.world

in folder usr/share/gazebo-11/models paste the folders UWB_anchor0 through UWB_anchor5

Download src and place in catkin workspace. Make sure that all files are executable. Run catkin_make

### Simulation
You should now be able to run the command.
roslaunch husky_tut uwb_launch.launch 

### Thanks to

https://github.com/bekirbostanci/ieuagv_localization

https://github.com/advoard/pozyx_simulation

https://github.com/valentinbarral/gazebosensorplugins

### Add model folder to Gazebo
In  ~/.bashrch insert the following line

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/jonathannielsen/models

change the username to your username and create a folder in the location before sourcing the script. Now you can add custom models in a writeable folder
