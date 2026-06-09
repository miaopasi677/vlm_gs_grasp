#!/usr/bin/python3
# coding=utf-8
"""
基于点云 + MoveIt 的抓取脚本

从深度相机点云中检测物体3D位置，使用 MoveIt 规划避障轨迹执行抓取。

流程:
  1. 接收 /camera/depth/points 点云
  2. TF 变换到 base_link 坐标系
  3. 去除桌面 + 欧式聚类分离物体
  4. 添加碰撞物体到 PlanningScene
  5. MoveIt 规划: 接近→抓取→抬升→撤离→放置

注意: ArmPi FPV 是 5 自由度机器人, 无法指定任意末端朝向,
      因此使用关节空间目标而非笛卡尔 pose 目标来规划抓取。

使用方式:
  roslaunch armpi_fpv_moveit_config pointcloud_grasp.launch
"""

import sys
import math
import numpy as np
import rospy
import moveit_commander
import tf2_ros
from scipy.spatial import KDTree
from collections import deque

from geometry_msgs.msg import Pose, PoseStamped
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive


class PointCloudGrasper:
    """点云抓取器：从点云检测物体并用 MoveIt 抓取"""

    # ===== 夹持器参数 =====
    GRIPPER_OPEN = -1.4312      # 夹持器打开时 r_joint 值
    GRIPPER_CLOSE = 0.0         # 夹持器闭合时 r_joint 值

    # ===== 关节空间抓取姿态 =====
    # 低位抓取姿态: joint1=0(后续根据物体位置计算), joint2~5 固定
    # 这些值通过实验确定, 使末端位于桌面上方约 6cm 处
    GRASP_J2 = -1.57
    GRASP_J3 = 2.09
    GRASP_J4 = 1.6
    GRASP_J5 = 0.0

    # 接近姿态 (略高于抓取点)
    APPROACH_J2 = -1.57
    APPROACH_J3 = 2.09
    APPROACH_J4 = 1.2   # 更弯曲 = 末端更高
    APPROACH_J5 = 0.0

    # 抬升姿态 (抓取后抬起)
    LIFT_J2 = -1.57
    LIFT_J3 = 2.09
    LIFT_J4 = 0.8   # 更弯曲 = 末端更高
    LIFT_J5 = 0.0

    # 放置姿态
    PLACE_J2 = -1.57
    PLACE_J3 = 2.09
    PLACE_J4 = 1.4
    PLACE_J5 = 0.0

    # ===== 点云处理参数 =====
    CLUSTER_DISTANCE = 0.025   # 欧式聚类距离阈值 (m)
    MIN_CLUSTER_POINTS = 30    # 最小聚类点数
    TABLE_Z_MIN = 0.005        # 物体最小高度(相对base_link), 过滤桌面和地面
    TABLE_Z_MAX = 0.30         # 物体最大高度, 过滤过高点

    def __init__(self):
        # 初始化 moveit_commander
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('pointcloud_grasper', anonymous=True)

        # 等待 MoveIt 服务就绪
        rospy.loginfo("等待 MoveIt 服务就绪...")
        rospy.wait_for_service('/get_planning_scene', timeout=30.0)

        # MoveIt 接口
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface(synchronous=True)
        self.arm_group = moveit_commander.MoveGroupCommander("arm")
        self.gripper_group = moveit_commander.MoveGroupCommander("gripper")

        # 设置规划参数
        self.arm_group.set_planning_time(10.0)
        self.arm_group.set_num_planning_attempts(20)
        self.arm_group.set_goal_position_tolerance(0.01)
        self.arm_group.set_goal_orientation_tolerance(0.1)

        # TF 监听器
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        # 点云缓存
        self.latest_cloud = None
        self.cloud_lock = False

        # 检测到的物体
        self.detected_objects = []

        # 订阅点云
        self.cloud_topic = rospy.get_param('~cloud_topic', '/camera/depth/points')
        self.cloud_sub = rospy.Subscriber(
            self.cloud_topic, PointCloud2, self.cloud_callback, queue_size=1)

        # 放置位置 (相对 base_link 的 xy, z 由姿态决定)
        self.place_x = rospy.get_param('~place_x', -0.15)
        self.place_y = rospy.get_param('~place_y', 0.05)

        rospy.loginfo("点云抓取器初始化完成")
        rospy.loginfo("  点云话题: %s", self.cloud_topic)
        rospy.loginfo("  放置位置: (%.3f, %.3f)", self.place_x, self.place_y)

    # ==================== 点云处理 ====================

    def cloud_callback(self, msg):
        """接收并缓存点云数据"""
        if not self.cloud_lock:
            self.latest_cloud = msg

    def transform_points(self, points, from_frame, to_frame):
        """将点云从 from_frame 变换到 to_link"""
        try:
            transform = self.tf_buffer.lookup_transform(
                to_frame, from_frame, rospy.Time(0), rospy.Duration(1.0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
                tf2_ros.ExtrapolationException) as e:
            rospy.logwarn("TF 变换失败 %s -> %s: %s", from_frame, to_frame, e)
            return None

        t = transform.transform.translation
        r = transform.transform.rotation
        qx, qy, qz, qw = r.x, r.y, r.z, r.w
        rot = np.array([
            [1 - 2*(qy*qy + qz*qz), 2*(qx*qy - qw*qz), 2*(qx*qz + qw*qy)],
            [2*(qx*qy + qw*qz), 1 - 2*(qx*qx + qz*qz), 2*(qy*qz - qw*qx)],
            [2*(qx*qz - qw*qy), 2*(qy*qz + qw*qx), 1 - 2*(qx*qx + qy*qy)]
        ])
        translation = np.array([t.x, t.y, t.z])
        return (rot @ points.T).T + translation

    def euclidean_clustering(self, points, cluster_distance):
        """基于 KDTree + BFS 的欧式聚类"""
        n = len(points)
        if n == 0:
            return []

        tree = KDTree(points)
        labels = [-1] * n
        cluster_id = 0

        for i in range(n):
            if labels[i] != -1:
                continue
            queue = deque([i])
            labels[i] = cluster_id
            while queue:
                idx = queue.popleft()
                neighbors = tree.query_ball_point(points[idx], cluster_distance)
                for nb in neighbors:
                    if labels[nb] == -1:
                        labels[nb] = cluster_id
                        queue.append(nb)
            cluster_id += 1

        return labels

    def process_cloud(self):
        """处理点云: 变换→去桌面→聚类→提取物体"""
        if self.latest_cloud is None:
            rospy.loginfo("等待点云数据...")
            timeout = rospy.Time.now() + rospy.Duration(10.0)
            while self.latest_cloud is None and not rospy.is_shutdown() and rospy.Time.now() < timeout:
                rospy.sleep(0.5)
            if self.latest_cloud is None:
                rospy.logwarn("等待点云超时")
                return []

        self.cloud_lock = True
        cloud_msg = self.latest_cloud
        self.latest_cloud = None
        self.cloud_lock = False

        # 1. 解析 PointCloud2
        frame_id = cloud_msg.header.frame_id
        gen = point_cloud2.read_points(cloud_msg, field_names=('x', 'y', 'z'), skip_nans=True)
        pts_list = list(gen)
        if len(pts_list) < 10:
            rospy.logwarn("点云点数过少: %d", len(pts_list))
            return []

        points = np.array(pts_list, dtype=np.float32)
        valid = np.all(np.isfinite(points), axis=1)
        points = points[valid]
        rospy.loginfo("收到点云: %d 点, 坐标系: %s", len(points), frame_id)

        # 2. 变换到 base_link
        if frame_id != 'base_link':
            points = self.transform_points(points, frame_id, 'base_link')
            if points is None:
                return []

        # 3. 高度过滤
        mask = (points[:, 2] > self.TABLE_Z_MIN) & (points[:, 2] < self.TABLE_Z_MAX)
        points_filtered = points[mask]
        rospy.loginfo("高度过滤后: %d 点 (z: %.3f ~ %.3f)",
                      len(points_filtered), self.TABLE_Z_MIN, self.TABLE_Z_MAX)

        if len(points_filtered) < self.MIN_CLUSTER_POINTS:
            rospy.logwarn("过滤后点数不足")
            return []

        # 4. 欧式聚类
        labels = self.euclidean_clustering(points_filtered, self.CLUSTER_DISTANCE)

        # 5. 提取每个聚类信息
        objects = []
        for label_id in set(labels):
            if label_id == -1:
                continue
            cluster_pts = points_filtered[np.array(labels) == label_id]
            if len(cluster_pts) < self.MIN_CLUSTER_POINTS:
                continue

            centroid = np.mean(cluster_pts, axis=0)
            bbox_min = np.min(cluster_pts, axis=0)
            bbox_max = np.max(cluster_pts, axis=0)
            size = bbox_max - bbox_min

            obj = {
                'position': centroid.tolist(),
                'size': size.tolist(),
                'points': cluster_pts
            }
            objects.append(obj)
            rospy.loginfo("  检测到物体: 质心=(%.3f, %.3f, %.3f), 尺寸=(%.3f, %.3f, %.3f)",
                          centroid[0], centroid[1], centroid[2],
                          size[0], size[1], size[2])

        # 按距机器人距离排序 (近的优先)
        objects.sort(key=lambda o: math.sqrt(o['position'][0]**2 + o['position'][1]**2))
        self.detected_objects = objects
        return objects

    # ==================== 碰撞物体管理 ====================

    def add_object_to_scene(self, obj_id, position, size):
        """添加碰撞物体到 PlanningScene"""
        collision_object = CollisionObject()
        collision_object.header.frame_id = self.arm_group.get_planning_frame()
        collision_object.id = obj_id

        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.BOX
        primitive.dimensions = [max(size[0], 0.01), max(size[1], 0.01), max(size[2], 0.01)]

        pose = Pose()
        pose.position.x = position[0]
        pose.position.y = position[1]
        pose.position.z = position[2]
        pose.orientation.w = 1.0

        collision_object.primitives = [primitive]
        collision_object.primitive_poses = [pose]
        collision_object.operation = CollisionObject.ADD

        self.scene.add_object(collision_object)
        rospy.sleep(0.5)
        rospy.loginfo("添加碰撞物体: %s 于 (%.3f, %.3f, %.3f)", obj_id, *position)

    def remove_all_objects(self):
        """移除所有碰撞物体"""
        for obj_id in self.scene.get_known_object_names():
            self.scene.remove_world_object(obj_id)
            rospy.sleep(0.1)

    # ==================== MoveIt 抓取 (关节空间) ====================

    def open_gripper(self):
        """打开夹持器"""
        self.gripper_group.set_joint_value_target({'r_joint': self.GRIPPER_OPEN})
        plan = self.gripper_group.plan()
        if plan[0]:
            self.gripper_group.execute(plan[1])
        else:
            rospy.logwarn("打开夹持器规划失败")

    def close_gripper(self):
        """关闭夹持器"""
        self.gripper_group.set_joint_value_target({'r_joint': self.GRIPPER_CLOSE})
        plan = self.gripper_group.plan()
        if plan[0]:
            self.gripper_group.execute(plan[1])
        else:
            rospy.logwarn("关闭夹持器规划失败")

    def pos_to_joint1(self, x, y):
        """根据物体 XY 坐标计算 joint1 (基座旋转角)

        joint1 控制机械臂绕 Z 轴旋转, 朝向目标方向。
        joint1=0 时臂朝 X 正方向, 增大 joint1 顺时针旋转。

        Args:
            x: base_link 下目标 X 坐标
            y: base_link 下目标 Y 坐标

        Returns:
            joint1 弧度值
        """
        return math.atan2(y, x)

    def move_to_joints(self, joints):
        """规划并移动到指定关节角度

        Args:
            joints: [j1, j2, j3, j4, j5] 关节角度列表

        Returns:
            True 表示成功
        """
        self.arm_group.set_joint_value_target(joints)
        plan = self.arm_group.plan()
        if not plan[0]:
            rospy.logwarn("关节规划失败: %s", [round(j, 3) for j in joints])
            return False
        result = self.arm_group.execute(plan[1])
        return result

    def go_home(self):
        """回到初始位置"""
        rospy.loginfo("回到初始位置...")
        self.arm_group.set_named_target("home")
        plan = self.arm_group.plan()
        if plan[0]:
            self.arm_group.execute(plan[1])
        self.open_gripper()

    def pick_object(self, obj_position, obj_size=None):
        """抓取物体 (使用关节空间目标)

        5自由度机器人无法指定任意末端朝向, 因此使用预定义的
        关节姿态组合, 仅调整 joint1 来对准物体方向。

        Args:
            obj_position: [x, y, z] 物体质心位置
            obj_size: [sx, sy, sz] 物体尺寸

        Returns:
            True 表示抓取成功
        """
        x, y, z = obj_position
        j1 = self.pos_to_joint1(x, y)

        rospy.loginfo("开始抓取: 目标 (%.3f, %.3f, %.3f), joint1=%.3f", x, y, z, j1)

        # 1. 打开夹持器
        self.open_gripper()
        rospy.sleep(0.5)

        # 2. 移动到接近点 (joint4 更弯曲, 末端更高)
        approach_joints = [j1, self.APPROACH_J2, self.APPROACH_J3, self.APPROACH_J4, self.APPROACH_J5]
        rospy.loginfo("  -> 移动到接近点")
        if not self.move_to_joints(approach_joints):
            rospy.logwarn("无法到达接近点, 尝试调整")
            # 尝试 home -> approach 的插值路径
            self.go_home()
            rospy.sleep(0.5)
            if not self.move_to_joints(approach_joints):
                rospy.logwarn("无法到达接近点, 放弃")
                return False
        rospy.sleep(0.5)

        # 3. 移动到抓取点 (低位)
        grasp_joints = [j1, self.GRASP_J2, self.GRASP_J3, self.GRASP_J4, self.GRASP_J5]
        rospy.loginfo("  -> 移动到抓取点")
        if not self.move_to_joints(grasp_joints):
            rospy.logwarn("无法到达抓取点, 尝试返回")
            self.go_home()
            return False
        rospy.sleep(0.5)

        # 4. 关闭夹持器
        rospy.loginfo("  -> 关闭夹持器")
        self.close_gripper()
        rospy.sleep(0.8)

        # 5. 抬升
        lift_joints = [j1, self.LIFT_J2, self.LIFT_J3, self.LIFT_J4, self.LIFT_J5]
        rospy.loginfo("  -> 抬升")
        if not self.move_to_joints(lift_joints):
            rospy.logwarn("抬升失败")
        rospy.sleep(0.3)

        rospy.loginfo("抓取完成")
        return True

    def place_object(self, place_x, place_y):
        """放置物体

        Args:
            place_x: 放置位置 X
            place_y: 放置位置 Y
        """
        j1 = self.pos_to_joint1(place_x, place_y)
        rospy.loginfo("开始放置: (%.3f, %.3f), joint1=%.3f", place_x, place_y, j1)

        # 1. 移动到放置点上方 (与 lift 同高度)
        approach_joints = [j1, self.LIFT_J2, self.LIFT_J3, self.LIFT_J4, self.LIFT_J5]
        rospy.loginfo("  -> 移动到放置上方")
        if not self.move_to_joints(approach_joints):
            rospy.logwarn("无法到达放置上方")
        rospy.sleep(0.3)

        # 2. 下降到放置点
        place_joints = [j1, self.PLACE_J2, self.PLACE_J3, self.PLACE_J4, self.PLACE_J5]
        rospy.loginfo("  -> 下降到放置点")
        if not self.move_to_joints(place_joints):
            rospy.logwarn("无法到达放置点")
        rospy.sleep(0.3)

        # 3. 打开夹持器
        rospy.loginfo("  -> 释放物体")
        self.open_gripper()
        rospy.sleep(0.5)

        # 4. 撤离 (先抬升)
        lift_joints = [j1, self.LIFT_J2, self.LIFT_J3, self.LIFT_J4, self.LIFT_J5]
        rospy.loginfo("  -> 撤离")
        self.move_to_joints(lift_joints)
        rospy.sleep(0.3)

        rospy.loginfo("放置完成")

    # ==================== 主流程 ====================

    def run(self):
        """执行一次完整的抓取-放置流程"""
        rospy.loginfo("===== 开始点云抓取流程 =====")

        # 1. 回到初始位置并打开夹持器
        self.go_home()
        rospy.sleep(1.0)

        # 2. 等待点云数据
        rospy.loginfo("等待点云数据...")
        timeout = rospy.Time.now() + rospy.Duration(10.0)
        while self.latest_cloud is None and not rospy.is_shutdown():
            if rospy.Time.now() > timeout:
                rospy.logerr("等待点云超时")
                return False
            rospy.sleep(0.5)

        # 3. 处理点云, 检测物体
        rospy.loginfo("处理点云...")
        objects = self.process_cloud()
        if not objects:
            rospy.logwarn("未检测到物体")
            return False

        rospy.loginfo("检测到 %d 个物体", len(objects))

        # 4. 添加碰撞物体
        self.remove_all_objects()
        for i, obj in enumerate(objects):
            self.add_object_to_scene(
                "object_{}".format(i), obj['position'], obj['size'])
        rospy.sleep(1.0)

        # 5. 抓取第一个检测到的物体
        target = objects[0]
        rospy.loginfo("目标物体: 质心=(%.3f, %.3f, %.3f)",
                      *target['position'])

        # 抓取前移除该物体的碰撞体 (避免自碰撞)
        self.scene.remove_world_object("object_0")
        rospy.sleep(0.5)

        success = self.pick_object(target['position'], target.get('size'))
        if not success:
            rospy.logwarn("抓取失败, 返回初始位置")
            self.go_home()
            return False

        # 6. 放置物体
        self.place_object(self.place_x, self.place_y)

        # 7. 回到初始位置
        self.go_home()

        # 清理碰撞物体
        self.remove_all_objects()

        rospy.loginfo("===== 点云抓取流程完成 =====")
        return True

    def run_interactive(self):
        """交互模式: 提供命令让用户选择操作"""
        rospy.loginfo("交互模式启动")
        rospy.loginfo("命令: d=检测物体, g=抓取第一个物体, p=放置, h=回家, a=全自动, q=退出")

        while not rospy.is_shutdown():
            try:
                cmd = input("\n> ").strip().lower()
            except EOFError:
                break

            if cmd == 'd':
                objects = self.process_cloud()
                if objects:
                    for i, obj in enumerate(objects):
                        rospy.loginfo("  物体 %d: (%.3f, %.3f, %.3f) 尺寸=(%.3f, %.3f, %.3f)",
                                      i, *obj['position'], *obj['size'])
                else:
                    rospy.loginfo("未检测到物体")

            elif cmd == 'g':
                if not self.detected_objects:
                    rospy.logwarn("请先执行检测 (d)")
                    continue
                target = self.detected_objects[0]
                self.scene.remove_world_object("object_0")
                rospy.sleep(0.3)
                self.pick_object(target['position'], target.get('size'))

            elif cmd == 'p':
                self.place_object(self.place_x, self.place_y)

            elif cmd == 'h':
                self.go_home()

            elif cmd == 'a':
                self.run()

            elif cmd == 'q':
                rospy.loginfo("退出")
                break

            else:
                rospy.loginfo("未知命令: %s", cmd)


def main():
    try:
        grasper = PointCloudGrasper()
        mode = rospy.get_param('~mode', 'auto')

        if mode == 'interactive':
            grasper.run_interactive()
        else:
            # 自动模式: 等待点云稳定后执行一次
            rospy.sleep(3.0)
            grasper.run()
            rospy.spin()

    except rospy.ROSInterruptException:
        pass
    finally:
        moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    main()
