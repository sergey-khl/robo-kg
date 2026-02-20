## TODO:

1. update kinova template on lab github
2. create nested setup of kinova code, dinovit and nvidia scripts for n4j  


## NOTES

- a quick test has been run to see if DINO-ViT works between real and sim that you can see: ![image](./media/corr.png)
- I am using ubuntu 24 with isaac sim locally installed and ros2 jazzy installed in docker following: https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html 
- in your local isaac sim repo make sure to first 
```bash
export ROS_DISTRO=jazzy
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/krabby-patty-vault/MyApps/isaacsim/exts/isaacsim.ros2.bridge/jazzy/lib
```
- then you can ```./python.sh standalone_examples/api/isaacsim.ros2.bridge/moveit.py``` to bring up a default panda environment. You should get no errors
and this is useful for seeing if your setup works. I will be adding more interesting environmets in this repo later on.




