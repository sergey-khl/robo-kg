# Notes
additional videos and diagrams can be found here: [google_drive_link](https://drive.google.com/drive/folders/1oEIqRLxW2W3g_0OcPlHMBqxE6QW26Irz?usp=sharing)


# Install: Query to task 
- Run ```wget http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/19.08/mini.h5```  to access commonsense knowledge graph embeddings. This is from the
conceptnet numberbatch [project](https://github.com/commonsense/conceptnet-numberbatch?tab=readme-ov-file)
- install requirements.txt with your prefered method. I am using python 3.10.19 if you want to ensure your results are consistent with mine. 
- run ```python query.py``` to run the experiment done in the paper


# Install: DINOBot controller

- I am using ubuntu 24 with isaac sim locally installed and ros2 jazzy installed in docker following: https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html 
- realtime kernel is optional. I dont think it had that big of a performance improvement when switched to it.
- in your local isaac sim repo make sure to first 
```bash
export ROS_DISTRO=jazzy
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/krabby-patty-vault/MyApps/isaacsim/exts/isaacsim.ros2.bridge/jazzy/lib
```
- then you can ```./python.sh standalone_examples/api/isaacsim.ros2.bridge/moveit.py``` to bring up a default panda environment. You should get no errors
and this is useful for seeing if your setup works.

- the main code resides in [DINOBot implementation](https://github.com/sergey-khl/IsaacSim-ros_workspaces/tree/main/jazzy_ws/src/dino_kg)
- build the docker image by running the shell script [./build_ros.sh](https://github.com/sergey-khl/IsaacSim-ros_workspaces/blob/main/build_ros.sh)
- At this point you will need 2 terminals
1.
    - inside your Nvidia Isaacsim install folder
    - run `./python.sh /path/to/IsaacSim-ros_workspaces/scene_setup/fruit_cleanup.py`
    - You usually run this first then the dinobot code immediately after in the docker container.
2.
    - In the second start the docker container with [./start](https://github.com/sergey-khl/robo-kg/blob/main/start.sh). 
    - To record a skill launch `ros2 launch dino_kg dino_recorder.launch`
    - To execute a task launch `ros2 launch dino_kg dino_controller.launch` 



