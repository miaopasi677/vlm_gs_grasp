#!/bin/bash
# Gazebo + MoveIt 本机仿真（前台运行，输出直接打在终端）
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/setup_ros_env.sh"

echo "=========================================="
echo "  启动 Gazebo + MoveIt 仿真"
echo "  按 Ctrl+C 结束"
echo "=========================================="
exec roslaunch armpi_fpv_moveit_config demo_gazebo.launch
