# ArmPi FPV ROS 工作空间

幻尔（Hiwonder）ArmPi FPV 机械臂 ROS 工程，基于 **ROS Noetic** + **catkin**。

## 环境要求

- Ubuntu 20.04 + ROS Noetic
- 已编译工作空间：`armpi_fpv/`

## 一键配置环境

```bash
cd /home/armpi/桌面/ros/armpi_fpv
source setup_ros_env.sh
```

> 若 `~/.bashrc` 中设置了 `ROS_MASTER_URI=http://192.168.x.x`（机械臂板子 IP），必须先 `source setup_ros_env.sh`，否则本机无法启动节点。

## 编译

```bash
cd /home/armpi/桌面/ros/armpi_fpv
source /opt/ros/noetic/setup.bash
catkin_make
source devel/setup.bash
```

## 运行方式

### 1. 仅看模型（开发机，无需硬件）

```bash
chmod +x run_display.sh
./run_display.sh
```

会打开 RViz 与关节滑块，用于查看 URDF。

### 2. MoveIt 规划演示（无需真机）

```bash
chmod +x run_moveit_demo.sh
./run_moveit_demo.sh
```

### 3. 真机完整功能

需要：机械臂、USB 摄像头、`/dev/ttyUSB*` 串口、sudo 权限。

先安装依赖：

```bash
sudo apt install ros-noetic-web-video-server \
  ros-noetic-rosbridge-server \
  ros-noetic-usb-cam
```

再启动：

```bash
chmod +x run_robot.sh
./run_robot.sh
```

## 包结构简述

| 包 | 作用 |
|---|---|
| `armpi_fpv` | URDF、RViz 显示 |
| `armpi_fpv_moveit_config` | MoveIt 规划 |
| `hiwonder_servo_*` | 舵机驱动与控制 |
| `armpi_fpv_bringup` | 启动入口 |
| `object_*` / `warehouse` / `face_detect` | 视觉与仓储功能节点 |

## 常见问题

**`Unable to contact my own server`**  
→ 执行 `source setup_ros_env.sh`，确保 `ROS_HOSTNAME=localhost`。

**`package 'web_video_server' not found`**  
→ 安装上表 apt 依赖后再跑 `run_robot.sh`。

**`roslaunch armpi_fpv display.launch` 找不到 launch**  
→ 先 `source devel/setup.bash`，或直接使用 `./run_display.sh`。
# vlm_gs_grasp


3dgs重建图示
<img width="1912" height="962" alt="7ea3ce09844ddea410d34991c075956a" src="https://github.com/user-attachments/assets/b907509c-7715-48fc-bc80-89f80f5473cd" />
rviz点云图示
<img width="1920" height="1017" alt="794dcea90f63c04f9a555351606ec841" src="https://github.com/user-attachments/assets/558704ee-3fb6-4d33-be5a-d8039e98887e" />
模拟抓取真机
https://github.com/user-attachments/assets/bb7629d5-0f4e-42a3-9507-c9e99a2d38e3

