#!/bin/bash
# 本地开发/仿真用 ROS 环境（覆盖 ~/.bashrc 里指向机械臂局域网的配置）
export ROS_HOSTNAME=localhost
export ROS_IP=127.0.0.1
export ROS_MASTER_URI=http://localhost:11311

# ROS Noetic 依赖系统 Python；若安装了 conda，需优先使用 /usr/bin
if [ -d "$HOME/miniconda3/bin" ] || [ -d "$HOME/anaconda3/bin" ]; then
  export PATH="/usr/bin:/bin:/usr/sbin:/sbin:$(echo "$PATH" | tr ':' '\n' | grep -vE 'miniconda|anaconda' | tr '\n' ':' | sed 's/:$//')"
fi

source /opt/ros/noetic/setup.bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/devel/setup.bash"

echo "ROS 环境已加载: $ROS_DISTRO @ $ROS_MASTER_URI"
echo "工作空间: $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
