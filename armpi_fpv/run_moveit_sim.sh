#!/bin/bash
# MoveIt + RViz 本机仿真（前台，无 Gazebo，最稳定）
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/setup_ros_env.sh"

echo "=========================================="
echo "  MoveIt 本机仿真 (RViz)"
echo "  按 Ctrl+C 结束"
echo "=========================================="
exec roslaunch armpi_fpv_moveit_config demo.launch
