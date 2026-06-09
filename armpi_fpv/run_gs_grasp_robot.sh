#!/bin/bash
# 3DGS 点云抓取 - 远程控制真机
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/setup_ros_robot.sh"

echo "检查机器人连接..."
if ! ping -c1 -W2 192.168.2.46 &>/dev/null; then
  echo "无法 ping 通机器人 192.168.2.46，请检查网线/WiFi"
  exit 1
fi
if ! timeout 3 rostopic list &>/dev/null; then
  echo "无法连接机器人 roscore，请在机器人上确认已启动:"
  echo "  roscore"
  echo "  roslaunch hiwonder_servo_controllers start.launch"
  exit 1
fi
if ! rostopic list | grep -q arm_controller/follow_joint_trajectory; then
  echo "机器人上未检测到 arm_controller，请先启动舵机驱动"
  exit 1
fi

exec roslaunch armpi_fpv_moveit_config gs_grasp_robot.launch "$@"
