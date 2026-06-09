#!/bin/bash
# 在 RViz 中显示机械臂模型（无需真机）
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/setup_ros_env.sh"

if ! rosnode list &>/dev/null; then
  echo "未检测到 roscore，请先另开终端运行: roscore"
  echo "或在本终端先执行 roscore，再重新运行本脚本。"
  exit 1
fi

exec roslaunch armpi_fpv display.launch
