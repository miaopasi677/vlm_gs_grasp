#!/bin/bash
# 真机完整启动（需连接机械臂、摄像头、串口权限）
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/setup_ros_env.sh"

for pkg in web_video_server rosbridge_server usb_cam; do
  if ! rospack find "$pkg" &>/dev/null; then
    echo "缺少 ROS 包: $pkg"
    echo "请安装: sudo apt install ros-noetic-web-video-server ros-noetic-rosbridge-server ros-noetic-usb-cam"
    exit 1
  fi
done

if ! rosnode list &>/dev/null; then
  echo "正在启动 roscore..."
  roscore &
  sleep 3
fi

roslaunch armpi_fpv_bringup start_dependence.launch &
sleep 10
roslaunch armpi_fpv_bringup start_camera.launch &
sleep 10
sudo "$SCRIPT_DIR/src/armpi_fpv_bringup/scripts/start_sensor_node.sh" &
sleep 10
roslaunch hiwonder_servo_controllers start.launch &
sleep 10
exec roslaunch armpi_fpv_bringup start_functions.launch
