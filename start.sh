rocker --nvidia --x11 --network host --name isaac_ros_bridge --volume $(pwd)/IsaacSim-ros_workspaces/jazzy_ws/src/dino_kg:/workspace/jazzy_ws/src/dino_kg --privileged isaac_sim_ros:ubuntu_24_jazzy
