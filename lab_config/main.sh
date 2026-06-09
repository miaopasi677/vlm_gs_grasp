#!/bin/bash
source /opt/ros/noetic/setup.bash
export ROS_HOSTNAME=localhost
export ROS_IP=127.0.0.1
export ROS_MASTER_URI=http://localhost:11311
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/main.py"
