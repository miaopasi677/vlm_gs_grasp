#!/bin/bash
# 远程连接机器人真机 ROS 环境
# 机器人在 192.168.2.46 运行 roscore + 舵机驱动
# 本机 192.168.2.80 运行 MoveIt 规划节点

export ROS_MASTER_URI=http://192.168.2.46:11311
export ROS_IP=192.168.2.80
export ROS_HOSTNAME=192.168.2.80

# ROS Noetic 依赖系统 Python；若安装了 conda，需优先使用 /usr/bin
if [ -d "$HOME/miniconda3/bin" ] || [ -d "$HOME/anaconda3/bin" ]; then
  export PATH="/usr/bin:/bin:/usr/sbin:/sbin:$(echo "$PATH" | tr ':' '\n' | grep -vE 'miniconda|anaconda' | tr '\n' ':' | sed 's/:$//')"
fi

source /opt/ros/noetic/setup.bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/devel/setup.bash"

echo "ROS 环境已加载 (远程模式): $ROS_DISTRO"
echo "  ROS_MASTER_URI = $ROS_MASTER_URI"
echo "  ROS_IP         = $ROS_IP"
echo "  机器人          = 192.168.2.46"
