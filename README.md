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

- Run ```wget http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/19.08/mini.h5``` where this README is located so that you have access to commonsense knowledge graph embeddings. This is from the
conceptnet numberbatch [project](https://github.com/commonsense/conceptnet-numberbatch?tab=readme-ov-file)
- install requirements.txt with your prefered method. I am using python 3.10.19 if you want to ensure your results are consistent with mine. 



