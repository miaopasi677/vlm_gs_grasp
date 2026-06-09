#!/usr/bin/python3
# coding=utf-8
"""
3DGS 模型导入 + MoveIt 模拟抓取

从 3DGS 训练产出的 ply 文件中提取点云，聚类识别物体，
在 MoveIt 仿真环境中模拟抓取验证。

流程:
  1. 加载 3DGS ply 文件 (gsplat 或标准点云格式)
  2. 自动检测桌面平面高度
  3. 颜色过滤 (去除暗色背景/桌面)
  4. 坐标系变换: COLMAP world → base_link (含桌面Z偏移)
  5. ROI 过滤: 只保留机械臂可达范围内的点
  6. 体素下采样 + 聚类 → 物体列表
  7. 添加碰撞物体到 PlanningScene
  8. 交互式抓取仿真

使用方式:
  roslaunch armpi_fpv_moveit_config gs_grasp_sim.launch
  roslaunch armpi_fpv_moveit_config gs_grasp_sim.launch gs_ply:=/path/to/point_cloud.ply
"""

import os
import sys
import math
import struct
import numpy as np
import rospy
import moveit_commander

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vlm_client import VLMClient

from geometry_msgs.msg import Pose, Point
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from std_msgs.msg import Header, ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray
from hiwonder_servo_msgs.msg import MultiRawIdPosDur

try:
    from armpi_fpv import bus_servo_control
except ImportError:
    bus_servo_control = None

# open3d 可能因 AVX 指令集问题 crash (SIGILL), 用子进程检测
HAS_OPEN3D = False
try:
    import subprocess
    result = subprocess.run(
        ['/usr/bin/python3', '-c', 'import open3d; print(open3d.__version__)'],
        capture_output=True, timeout=5)
    if result.returncode == 0:
        import open3d as o3d
        HAS_OPEN3D = True
except Exception:
    pass


class GSGraspSim:
    """3DGS 模型导入 + MoveIt 模拟抓取"""

    # ===== 抓取参数 (同 pointcloud_grasp.py) =====
    GRIPPER_OPEN = -1.4312
    GRIPPER_CLOSE = 0.0

    GRASP_J2 = -1.57
    GRASP_J3 = 2.09
    GRASP_J4 = 1.6
    GRASP_J5 = 0.0

    APPROACH_J2 = -1.57
    APPROACH_J3 = 2.09
    APPROACH_J4 = 1.2
    APPROACH_J5 = 0.0

    LIFT_J2 = -1.57
    LIFT_J3 = 2.09
    LIFT_J4 = 0.8
    LIFT_J5 = 0.0

    PLACE_J2 = -1.57
    PLACE_J3 = 2.09
    PLACE_J4 = 1.4
    PLACE_J5 = 0.0

    # ===== 点云处理参数 =====
    MIN_OPACITY = 0.005        # 过滤低不透明度高斯
    VOXEL_SIZE = 0.005         # 体素下采样大小 (m)
    CLUSTER_DISTANCE = 0.02   # 聚类距离阈值 (m)
    MIN_CLUSTER_POINTS = 50    # 最小聚类点数
    TABLE_Z_MIN = 0.005        # 物体最小高度 (相对桌面)
    TABLE_Z_MAX = 0.20         # 物体最大高度
    ROI_XY_MAX = 0.35          # ROI: 只保留距base_link中心此距离内的点
    DARK_THRESHOLD = 30        # RGB max < 此值视为暗色点(桌面/背景)

    # MoveIt SRDF home + 仓库脚本使用的舵机零位 (servo_id, pulse)
    HOME_ARM_JOINTS = [0.0, 0.0, 0.0, 0.0, 0.0]
    HOME_SERVO_POS = ((1, 75), (2, 500), (3, 80), (4, 825), (5, 625), (6, 500))
    GRIPPER_OPEN_SERVO = 75

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('gs_grasp_sim', anonymous=True)

        rospy.loginfo("等待 MoveIt 服务就绪...")
        rospy.wait_for_service('/get_planning_scene', timeout=30.0)

        # MoveIt 接口
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface(synchronous=True)
        self.arm_group = moveit_commander.MoveGroupCommander("arm")
        self.gripper_group = moveit_commander.MoveGroupCommander("gripper")

        self.arm_group.set_planning_time(10.0)
        self.arm_group.set_num_planning_attempts(20)
        self.arm_group.set_goal_position_tolerance(0.01)
        self.arm_group.set_goal_orientation_tolerance(0.1)

        # 发布器
        self.cloud_pub = rospy.Publisher('/gs_reconstructed_cloud', PointCloud2, queue_size=1, latch=True)
        self.marker_pub = rospy.Publisher('/gs_object_markers', MarkerArray, queue_size=1, latch=True)
        self.joints_pub = rospy.Publisher(
            '/servo_controllers/port_id_1/multi_id_pos_dur', MultiRawIdPosDur, queue_size=1)

        # 参数
        self.gs_ply = rospy.get_param('~gs_ply', '')
        self.scale = rospy.get_param('~scale', 1.0)
        self.auto_table = rospy.get_param('~auto_table', True)  # 自动检测桌面高度
        self.transform_param = rospy.get_param('~transform', None)

        # 坐标变换矩阵
        # 默认: COLMAP world → ROS base_link (单位: 米)
        # 对于 nerfstudio 导出的点云, COLMAP 世界坐标系是任意的,
        # 需要根据实际数据调整。auto_table 会自动添加 Z 方向平移。
        if self.transform_param is not None:
            vals = [float(v) for v in self.transform_param.split(',')]
            self.T = np.array(vals).reshape(4, 4)
        else:
            # 默认: 保持 XYZ 不变, auto_table 会设置 Z 偏移
            self.T = np.eye(4)

        self.detected_objects = []
        self.table_z_offset = 0.0  # 桌面Z偏移, auto_table 自动设置

        # 从 ROS 参数覆盖类默认值
        self.ROI_XY_MAX = rospy.get_param('~roi_xy_max', self.ROI_XY_MAX)
        self.DARK_THRESHOLD = rospy.get_param('~dark_thresh', self.DARK_THRESHOLD)

        # 放置位置
        self.place_x = rospy.get_param('~place_x', -0.15)
        self.place_y = rospy.get_param('~place_y', 0.05)

        # VLM 自然语言选物
        self.vlm_enabled = rospy.get_param('~vlm/enabled', False)
        self.vlm_use_camera = rospy.get_param('~vlm/use_camera', True)
        self.vlm_client = None
        self.latest_image = None
        self.cv_bridge = None
        if self.vlm_enabled:
            self.vlm_client = VLMClient(
                api_base=rospy.get_param('~vlm/api_base', 'https://api.openai.com/v1'),
                api_key=rospy.get_param('~vlm/api_key', ''),
                model=rospy.get_param('~vlm/model', 'gpt-4o-mini'),
                timeout=int(rospy.get_param('~vlm/timeout', 60)),
            )
            if self.vlm_use_camera:
                from sensor_msgs.msg import Image
                from cv_bridge import CvBridge
                self.cv_bridge = CvBridge()
                cam_topic = rospy.get_param('~vlm/camera_topic', '/usb_cam/image_raw')
                rospy.Subscriber(cam_topic, Image, self._camera_callback, queue_size=1)
                rospy.loginfo("VLM 已启用, 相机话题: %s", cam_topic)
            else:
                rospy.loginfo("VLM 已启用 (仅文本模式)")
        else:
            rospy.loginfo("VLM 未启用 (设 vlm/enabled:=true 开启)")

        rospy.loginfo("3DGS 抓取仿真器初始化完成")

    # ==================== PLY 文件加载 ====================

    def load_gs_ply(self, filepath):
        """加载 ply 文件

        支持:
          - 标准点云 ply (xyz + rgb)
          - gsplat 格式 (含 opacity, scale, rot 等属性)

        Returns:
            dict: {'positions': Nx3, 'opacities': N, 'colors': Nx3, 'normals': Nx3 or None}
        """
        rospy.loginfo("加载 3DGS 模型: %s", filepath)

        # 尝试用 open3d 加载 (更快, 但可能不支持 gsplat 自定义属性)
        if HAS_OPEN3D:
            try:
                pcd = o3d.io.read_point_cloud(filepath)
                if len(pcd.points) > 0:
                    positions = np.asarray(pcd.points, dtype=np.float64)
                    colors = np.asarray(pcd.colors, dtype=np.float64) * 255 if pcd.has_colors() else None
                    normals = np.asarray(pcd.normals, dtype=np.float64) if pcd.has_normals() else None
                    rospy.loginfo("Open3D 加载成功: %d 点, 颜色: %s, 法向量: %s",
                                  len(positions),
                                  colors is not None, normals is not None)
                    return {
                        'positions': positions,
                        'opacities': np.ones(len(positions)),
                        'colors': colors.astype(np.uint8) if colors is not None else None,
                        'normals': normals
                    }
            except Exception as e:
                rospy.logwarn("Open3D 加载失败, fallback 到手动解析: %s", e)

        return self._parse_ply_raw(filepath)

    def _parse_ply_raw(self, filepath):
        """手动解析 ply 文件, 支持 gsplat 自定义属性, 用 numpy 高效读取

        Returns:
            dict 或 None
        """
        try:
            with open(filepath, 'rb') as f:
                # 解析 header
                line = f.readline().decode().strip()
                if line != 'ply':
                    rospy.logerr("不是 ply 文件")
                    return None

                format_type = 'ascii'
                vertex_count = 0
                properties = []

                while True:
                    line = f.readline().decode().strip()
                    if line.startswith('format'):
                        format_type = line.split()[1]
                    elif line.startswith('element vertex'):
                        vertex_count = int(line.split()[2])
                    elif line.startswith('property'):
                        parts = line.split()
                        prop_type = parts[1]
                        prop_name = parts[2]
                        properties.append((prop_type, prop_name))
                    elif line == 'end_header':
                        break

                rospy.loginfo("PLY: %d 顶点, %d 属性, 格式: %s",
                              vertex_count, len(properties), format_type)

                prop_idx = {name: i for i, (_, name) in enumerate(properties)}
                has_opacity = 'opacity' in prop_idx
                has_normals = all(k in prop_idx for k in ('nx', 'ny', 'nz'))
                has_colors = all(k in prop_idx for k in ('red', 'green', 'blue'))

                # 类型大小映射
                type_sizes = {
                    'char': 1, 'uchar': 1, 'short': 2, 'ushort': 2,
                    'int': 4, 'uint': 4, 'float': 4, 'double': 8
                }
                type_numpy = {
                    'char': 'i1', 'uchar': 'u1', 'short': 'i2', 'ushort': 'u2',
                    'int': 'i4', 'uint': 'u4', 'float': 'f4', 'double': 'f8'
                }

                positions = np.zeros((vertex_count, 3), dtype=np.float64)
                opacities = np.ones(vertex_count, dtype=np.float64)
                colors = np.zeros((vertex_count, 3), dtype=np.uint8) if has_colors else None
                normals = np.zeros((vertex_count, 3), dtype=np.float64) if has_normals else None

                if format_type == 'binary_little_endian':
                    # 高效: 一次性读取所有数据, 用 numpy 解析
                    row_size = sum(type_sizes.get(t, 4) for t, _ in properties)
                    dtype_list = []
                    for prop_type, prop_name in properties:
                        np_type = type_numpy.get(prop_type, 'f4')
                        dtype_list.append((prop_name, np_type))

                    all_data = np.frombuffer(f.read(vertex_count * row_size),
                                             dtype=np.dtype(dtype_list))
                    positions[:, 0] = all_data['x']
                    positions[:, 1] = all_data['y']
                    positions[:, 2] = all_data['z']

                    if has_opacity:
                        raw = all_data['opacity'].astype(np.float64)
                        opacities = np.where(raw < 50, 1.0 / (1.0 + np.exp(-raw)), 1.0)
                    if has_colors:
                        colors[:, 0] = all_data['red']
                        colors[:, 1] = all_data['green']
                        colors[:, 2] = all_data['blue']
                    if has_normals:
                        normals[:, 0] = all_data['nx']
                        normals[:, 1] = all_data['ny']
                        normals[:, 2] = all_data['nz']

                elif format_type == 'ascii':
                    # ASCII 格式: 逐行解析 (较慢)
                    for i in range(vertex_count):
                        line = f.readline().decode().strip()
                        vals = line.split()
                        positions[i, 0] = float(vals[prop_idx['x']])
                        positions[i, 1] = float(vals[prop_idx['y']])
                        positions[i, 2] = float(vals[prop_idx['z']])
                        if has_opacity:
                            raw = float(vals[prop_idx['opacity']])
                            opacities[i] = 1.0 / (1.0 + math.exp(-raw)) if raw < 50 else 1.0
                        if has_colors:
                            colors[i, 0] = int(vals[prop_idx['red']])
                            colors[i, 1] = int(vals[prop_idx['green']])
                            colors[i, 2] = int(vals[prop_idx['blue']])
                        if has_normals:
                            normals[i, 0] = float(vals[prop_idx['nx']])
                            normals[i, 1] = float(vals[prop_idx['ny']])
                            normals[i, 2] = float(vals[prop_idx['nz']])

                elif format_type == 'binary_big_endian':
                    rospy.logerr("不支持 big endian ply")
                    return None

                rospy.loginfo("解析完成: %d 点, opacity: %s, colors: %s, normals: %s",
                              vertex_count, has_opacity, has_colors, has_normals)
                return {
                    'positions': positions,
                    'opacities': opacities,
                    'colors': colors,
                    'normals': normals
                }

        except Exception as e:
            rospy.logerr("加载 ply 失败: %s", e)
            import traceback
            traceback.print_exc()
            return None

    # ==================== 桌面检测 ====================

    def _detect_table_z(self, positions, colors=None):
        """自动检测桌面平面的 Z 坐标

        方法: 在 Z 轴上做直方图, 找到点数最多的 bin 作为桌面高度

        Args:
            positions: Nx3 原始坐标点云
            colors: Nx3 RGB 颜色 (可选, 用于辅助判断)

        Returns:
            float: 桌面 Z 坐标 (原始坐标系下)
        """
        # 用 50 个 bin 做 Z 直方图
        z_vals = positions[:, 2]
        n_bins = 50
        hist, edges = np.histogram(z_vals, bins=n_bins)

        # 找到点数最多的 bin
        max_idx = np.argmax(hist)
        table_z = (edges[max_idx] + edges[max_idx + 1]) / 2.0

        rospy.loginfo("桌面检测: Z ≈ %.4f (histogram peak: %d 点 in bin [%.3f, %.3f])",
                      table_z, hist[max_idx], edges[max_idx], edges[max_idx + 1])

        # 也打印 Z 分布概览
        rospy.loginfo("Z 直方图 (top 5 bins):")
        top5 = np.argsort(hist)[-5:][::-1]
        for idx in top5:
            rospy.loginfo("  Z=[%.3f, %.3f]: %d 点", edges[idx], edges[idx+1], hist[idx])

        return table_z

    # ==================== 点云处理 ====================

    def _voxel_downsample_numpy(self, points, voxel_size):
        """用 numpy 实现体素下采样 (open3d 不可用时的 fallback)

        Args:
            points: Nx3 点云
            voxel_size: 体素边长

        Returns:
            下采样后的点云 (每个体素内取均值)
        """
        if len(points) == 0:
            return points

        # 量化到体素网格
        voxel_indices = np.floor(points / voxel_size).astype(np.int32)

        # 用字典合并同一体素内的点
        voxel_dict = {}
        for i in range(len(voxel_indices)):
            key = tuple(voxel_indices[i])
            if key not in voxel_dict:
                voxel_dict[key] = []
            voxel_dict[key].append(points[i])

        # 每个体素取均值
        downsampled = np.array([np.mean(pts, axis=0) for pts in voxel_dict.values()])
        return downsampled

    def process_gs_model(self, data):
        """处理 3DGS 模型数据

        流程: opacity过滤 → 自动桌面检测 → 坐标变换 → 暗色过滤
              → 高度过滤 → ROI过滤 → 下采样 → 聚类 → 提取物体

        Args:
            data: load_gs_ply 返回的 dict

        Returns:
            物体列表
        """
        positions = data['positions']
        opacities = data['opacities']
        colors = data.get('colors', None)
        normals = data.get('normals', None)

        # 1. 按 opacity 过滤 (gsplat 格式)
        if not np.all(opacities == 1.0):
            mask = opacities > self.MIN_OPACITY
            positions = positions[mask]
            opacities = opacities[mask]
            if colors is not None:
                colors = colors[mask]
            if normals is not None:
                normals = normals[mask]
            rospy.loginfo("Opacity 过滤: → %d 点", len(positions))

        # 2. 自动检测桌面并更新变换矩阵
        if self.auto_table:
            table_z = self._detect_table_z(positions, colors)
            # 将桌面移到 Z=0 (base_link 地面高度)
            # 桌面上的物体 Z > 0
            self.T[2, 3] = -table_z  # Z 平移 = -table_z
            self.table_z_offset = -table_z
            rospy.loginfo("自动设置 Z 偏移: %.4f (桌面移到 Z=0)", -table_z)

        # 3. 坐标系变换 + 缩放
        ones = np.ones((len(positions), 1), dtype=np.float64)
        pts_homo = np.hstack([positions * self.scale, ones])
        pts_transformed = (self.T @ pts_homo.T).T[:, :3]
        rospy.loginfo("坐标变换完成: X=[%.3f,%.3f] Y=[%.3f,%.3f] Z=[%.3f,%.3f]",
                      pts_transformed[:,0].min(), pts_transformed[:,0].max(),
                      pts_transformed[:,1].min(), pts_transformed[:,1].max(),
                      pts_transformed[:,2].min(), pts_transformed[:,2].max())

        if normals is not None:
            R = self.T[:3, :3]
            normals_t = (R @ normals.T).T
        else:
            normals_t = None

        # 4. 暗色点过滤 (去除桌面/背景, 保留彩色物体)
        if colors is not None:
            bright_mask = colors.max(axis=1) > self.DARK_THRESHOLD
            pts_bright = pts_transformed[bright_mask]
            normals_bright = normals_t[bright_mask] if normals_t is not None else None
            rospy.loginfo("暗色过滤: %d → %d 点 (保留 RGB max > %d)",
                          len(pts_transformed), len(pts_bright), self.DARK_THRESHOLD)
        else:
            pts_bright = pts_transformed
            normals_bright = normals_t

        # 5. 高度过滤 (只保留桌面以上、不太高的点)
        mask_z = (pts_bright[:, 2] > self.TABLE_Z_MIN) & \
                 (pts_bright[:, 2] < self.TABLE_Z_MAX)
        pts_filtered = pts_bright[mask_z]
        normals_filtered = normals_bright[mask_z] if normals_bright is not None else None
        rospy.loginfo("高度过滤 (Z: %.3f~%.3f): %d → %d 点",
                      self.TABLE_Z_MIN, self.TABLE_Z_MAX, len(pts_bright), len(pts_filtered))

        if len(pts_filtered) < self.MIN_CLUSTER_POINTS:
            rospy.logwarn("过滤后点数不足: %d (尝试调整 TABLE_Z_MIN/MAX 或 DARK_THRESHOLD)", len(pts_filtered))
            # fallback: 不做暗色过滤，只用高度过滤
            if colors is not None:
                mask_z2 = (pts_transformed[:, 2] > self.TABLE_Z_MIN) & \
                          (pts_transformed[:, 2] < self.TABLE_Z_MAX)
                pts_filtered = pts_transformed[mask_z2]
                normals_filtered = normals_t[mask_z2] if normals_t is not None else None
                rospy.loginfo("Fallback (无暗色过滤): %d 点", len(pts_filtered))
            if len(pts_filtered) < self.MIN_CLUSTER_POINTS:
                return []

        # 6. ROI 过滤 (只保留机械臂可达范围内的点)
        xy_dist = np.sqrt(pts_filtered[:, 0]**2 + pts_filtered[:, 1]**2)
        roi_mask = xy_dist < self.ROI_XY_MAX
        pts_roi = pts_filtered[roi_mask]
        normals_roi = normals_filtered[roi_mask] if normals_filtered is not None else None
        rospy.loginfo("ROI 过滤 (XY < %.2fm): %d → %d 点",
                      self.ROI_XY_MAX, len(pts_filtered), len(pts_roi))

        if len(pts_roi) < self.MIN_CLUSTER_POINTS:
            rospy.logwarn("ROI 内点数不足: %d (尝试增大 ROI_XY_MAX=%.2f)",
                          len(pts_roi), self.ROI_XY_MAX)
            # fallback: 用全部高度过滤后的点
            pts_roi = pts_filtered
            normals_roi = normals_filtered

        # 7. 体素下采样
        if len(pts_roi) > 50000:
            if HAS_OPEN3D:
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(pts_roi)
                if normals_roi is not None:
                    pcd.normals = o3d.utility.Vector3dVector(normals_roi)
                pcd = pcd.voxel_down_sample(self.VOXEL_SIZE)
                pts_roi = np.asarray(pcd.points)
                normals_roi = np.asarray(pcd.normals) if pcd.has_normals() else None
            else:
                pts_roi = self._voxel_downsample_numpy(pts_roi, self.VOXEL_SIZE)
                normals_roi = None
            rospy.loginfo("体素下采样: → %d 点", len(pts_roi))

        # 8. 估算法向量
        if normals_roi is None and HAS_OPEN3D and len(pts_roi) > 30:
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(pts_roi)
            pcd.estimate_normals(
                search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.02, max_nn=30))
            normals_roi = np.asarray(pcd.normals)

        # 9. 聚类
        objects = self._cluster_objects(pts_roi, normals_roi)

        # 10. 发布点云到 RViz
        self._publish_cloud(pts_roi)

        # 11. 发布物体标记
        self._publish_markers(objects)

        return objects

    def _cluster_objects(self, points, normals=None):
        """聚类提取物体"""
        if HAS_OPEN3D:
            return self._cluster_open3d(points, normals)
        else:
            return self._cluster_numpy(points, normals)

    def _cluster_open3d(self, points, normals):
        """用 Open3D DBSCAN 聚类"""
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        if normals is not None:
            pcd.normals = o3d.utility.Vector3dVector(normals)

        labels = np.array(pcd.cluster_dbscan(
            eps=self.CLUSTER_DISTANCE, min_points=self.MIN_CLUSTER_POINTS))

        objects = []
        for label_id in set(labels):
            if label_id == -1:
                continue
            mask = labels == label_id
            cluster_pts = points[mask]
            cluster_normals = normals[mask] if normals is not None else None
            if len(cluster_pts) < self.MIN_CLUSTER_POINTS:
                continue

            centroid = np.mean(cluster_pts, axis=0)
            bbox_min = np.min(cluster_pts, axis=0)
            bbox_max = np.max(cluster_pts, axis=0)
            size = bbox_max - bbox_min

            avg_normal = None
            if cluster_normals is not None:
                avg_normal = np.mean(cluster_normals, axis=0)
                norm = np.linalg.norm(avg_normal)
                if norm > 1e-6:
                    avg_normal /= norm

            obj = {
                'position': centroid.tolist(),
                'size': size.tolist(),
                'normal': avg_normal.tolist() if avg_normal is not None else None,
                'points': cluster_pts,
            }
            objects.append(obj)
            rospy.loginfo("  物体: 质心=(%.3f, %.3f, %.3f) 尺寸=(%.3f, %.3f, %.3f)",
                          centroid[0], centroid[1], centroid[2],
                          size[0], size[1], size[2])

        objects.sort(key=lambda o: math.sqrt(o['position'][0]**2 + o['position'][1]**2))
        return objects

    def _cluster_numpy(self, points, normals):
        """用 numpy + scipy 聚类 (fallback)"""
        try:
            from scipy.spatial import KDTree
        except ImportError:
            rospy.logerr("scipy 不可用, 无法聚类")
            return []

        from collections import deque

        # 先降采样避免太慢
        if len(points) > 20000:
            idx = np.random.choice(len(points), 20000, replace=False)
            points = points[idx]
            if normals is not None:
                normals = normals[idx]

        tree = KDTree(points)
        labels = [-1] * len(points)
        cluster_id = 0

        for i in range(len(points)):
            if labels[i] != -1:
                continue
            queue = deque([i])
            labels[i] = cluster_id
            while queue:
                idx_ = queue.popleft()
                neighbors = tree.query_ball_point(points[idx_], self.CLUSTER_DISTANCE)
                for nb in neighbors:
                    if labels[nb] == -1:
                        labels[nb] = cluster_id
                        queue.append(nb)
            cluster_id += 1

        objects = []
        for label_id in set(labels):
            if label_id == -1:
                continue
            mask = np.array(labels) == label_id
            cluster_pts = points[mask]
            if len(cluster_pts) < self.MIN_CLUSTER_POINTS:
                continue

            centroid = np.mean(cluster_pts, axis=0)
            bbox_min = np.min(cluster_pts, axis=0)
            bbox_max = np.max(cluster_pts, axis=0)
            size = bbox_max - bbox_min

            objects.append({
                'position': centroid.tolist(),
                'size': size.tolist(),
                'normal': None,
                'points': cluster_pts,
            })
            rospy.loginfo("  物体: 质心=(%.3f, %.3f, %.3f) 尺寸=(%.3f, %.3f, %.3f)",
                          centroid[0], centroid[1], centroid[2],
                          size[0], size[1], size[2])

        objects.sort(key=lambda o: math.sqrt(o['position'][0]**2 + o['position'][1]**2))
        return objects

    # ==================== 可视化 ====================

    def _publish_cloud(self, points):
        """发布点云到 RViz"""
        header = Header()
        header.frame_id = "base_link"
        header.stamp = rospy.Time.now()

        fields = [
            point_cloud2.PointField('x', 0, point_cloud2.PointField.FLOAT32, 1),
            point_cloud2.PointField('y', 4, point_cloud2.PointField.FLOAT32, 1),
            point_cloud2.PointField('z', 8, point_cloud2.PointField.FLOAT32, 1),
        ]

        cloud_msg = point_cloud2.create_cloud(header, fields, points)
        self.cloud_pub.publish(cloud_msg)
        rospy.loginfo("发布点云: %d 点 -> /gs_reconstructed_cloud", len(points))

    def _publish_markers(self, objects):
        """发布物体标记 (包围盒 + 编号) 到 RViz"""
        markers = MarkerArray()

        for i, obj in enumerate(objects):
            # 包围盒
            marker = Marker()
            marker.header.frame_id = "base_link"
            marker.header.stamp = rospy.Time.now()
            marker.ns = "gs_objects"
            marker.id = i
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose.position.x = obj['position'][0]
            marker.pose.position.y = obj['position'][1]
            marker.pose.position.z = obj['position'][2]
            marker.pose.orientation.w = 1.0
            marker.scale.x = max(obj['size'][0], 0.01)
            marker.scale.y = max(obj['size'][1], 0.01)
            marker.scale.z = max(obj['size'][2], 0.01)
            marker.color = ColorRGBA(0.2, 0.6, 1.0, 0.4)
            markers.markers.append(marker)

            # 编号文字
            text = Marker()
            text.header.frame_id = "base_link"
            text.header.stamp = rospy.Time.now()
            text.ns = "gs_labels"
            text.id = i
            text.type = Marker.TEXT_VIEW_FACING
            text.action = Marker.ADD
            text.pose.position.x = obj['position'][0]
            text.pose.position.y = obj['position'][1]
            text.pose.position.z = obj['position'][2] + max(obj['size'][2], 0.01) / 2 + 0.02
            text.pose.orientation.w = 1.0
            text.scale.z = 0.02
            text.color = ColorRGBA(1.0, 1.0, 1.0, 1.0)
            text.text = "obj_{}".format(i)
            markers.markers.append(text)

        self.marker_pub.publish(markers)

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

    def remove_all_objects(self):
        """移除所有碰撞物体"""
        for obj_id in self.scene.get_known_object_names():
            self.scene.remove_world_object(obj_id)
            rospy.sleep(0.1)

    # ==================== MoveIt 抓取 ====================

    @staticmethod
    def _plan_ok(plan):
        if isinstance(plan, tuple):
            return bool(plan[0])
        return bool(plan)

    @staticmethod
    def _plan_trajectory(plan):
        return plan[1] if isinstance(plan, tuple) else plan

    def _set_gripper_servo(self, pulse, duration_ms=800):
        """夹爪舵机直控，绕过 MoveIt 碰撞检测"""
        if bus_servo_control is None:
            rospy.logwarn("bus_servo_control 不可用，跳过夹爪直控")
            return
        bus_servo_control.set_servos(self.joints_pub, duration_ms, ((1, int(pulse)),))
        rospy.sleep(duration_ms / 1000.0 + 0.1)

    def _go_home_servos(self, duration_ms=1500):
        """舵机直控回零（最终兜底，不依赖 MoveIt 规划）"""
        if bus_servo_control is None:
            rospy.logerr("bus_servo_control 不可用，无法舵机直控回零")
            return False
        rospy.loginfo("使用舵机直控回零...")
        bus_servo_control.set_servos(self.joints_pub, duration_ms, self.HOME_SERVO_POS)
        rospy.sleep(duration_ms / 1000.0 + 0.3)
        return True

    def open_gripper(self):
        self.gripper_group.set_joint_value_target({'r_joint': self.GRIPPER_OPEN})
        plan = self.gripper_group.plan()
        if self._plan_ok(plan):
            self.gripper_group.execute(self._plan_trajectory(plan))
        else:
            rospy.logwarn("夹爪 MoveIt 规划失败，改用舵机直控打开")
            self._set_gripper_servo(self.GRIPPER_OPEN_SERVO)

    def close_gripper(self):
        self.gripper_group.set_joint_value_target({'r_joint': self.GRIPPER_CLOSE})
        plan = self.gripper_group.plan()
        if self._plan_ok(plan):
            self.gripper_group.execute(self._plan_trajectory(plan))
        else:
            rospy.logwarn("夹爪 MoveIt 规划失败，改用舵机直控闭合")
            self._set_gripper_servo(500)

    def pos_to_joint1(self, x, y):
        """XY坐标 -> joint1 (基座旋转角)"""
        return math.atan2(y, x)

    def move_to_joints(self, joints):
        """移动到指定关节角度"""
        self.arm_group.set_joint_value_target(joints)
        plan = self.arm_group.plan()
        if not plan[0]:
            rospy.logwarn("关节规划失败: %s", [round(j, 3) for j in joints])
            return False
        result = self.arm_group.execute(plan[1])
        return result

    def go_home(self):
        """回零：清碰撞体 → MoveIt 规划 → 关节直目标 → 舵机直控（逐级兜底）"""
        rospy.loginfo("回到初始位置...")

        # 清除点云碰撞体，避免 START_STATE_IN_COLLISION
        try:
            self.remove_all_objects()
        except Exception as e:
            rospy.logwarn("清除碰撞物体时出错(继续回零): %s", e)
        rospy.sleep(0.5)

        self.arm_group.clear_path_constraints()
        self.gripper_group.clear_path_constraints()

        arm_ok = False

        # 1) MoveIt 命名姿态 home
        try:
            self.arm_group.set_start_state_to_current_state()
            self.arm_group.set_named_target("home")
            plan = self.arm_group.plan()
            if self._plan_ok(plan):
                arm_ok = bool(self.arm_group.execute(self._plan_trajectory(plan), wait=True))
        except Exception as e:
            rospy.logwarn("MoveIt home 异常: %s", e)

        # 2) MoveIt 关节直目标
        if not arm_ok:
            rospy.logwarn("MoveIt home 失败，尝试关节直目标...")
            try:
                self.arm_group.set_start_state_to_current_state()
                arm_ok = self.move_to_joints(self.HOME_ARM_JOINTS)
            except Exception as e:
                rospy.logwarn("关节直目标异常: %s", e)

        # 3) 舵机直控（必定执行）
        if not arm_ok:
            rospy.logwarn("MoveIt 均失败，改用舵机直控回零")
            self._go_home_servos()
        else:
            # 臂已到位，夹爪单独打开（不用 MoveIt，避免与残留场景碰撞）
            self._set_gripper_servo(self.GRIPPER_OPEN_SERVO)

        rospy.loginfo("回零完成")
        return True

    def check_reachable(self, x, y):
        """检查物体是否在机械臂可达范围内"""
        j1 = self.pos_to_joint1(x, y)
        dist = math.sqrt(x**2 + y**2)

        if abs(j1) > 1.57:
            rospy.logwarn("joint1=%.3f 超出限位 (±1.57), 物体在 (%.3f, %.3f)", j1, x, y)
            return False, j1
        if dist > 0.25:
            rospy.logwarn("物体距离 %.3fm 超出最大伸展", dist)
            return False, j1
        if dist < 0.03:
            rospy.logwarn("物体距离 %.3fm 太近", dist)
            return False, j1

        return True, j1

    def pick_object(self, obj):
        """抓取物体"""
        x, y, z = obj['position']

        reachable, j1 = self.check_reachable(x, y)
        if not reachable:
            return False

        rospy.loginfo("开始抓取: (%.3f, %.3f, %.3f), joint1=%.3f", x, y, z, j1)

        # 1. 打开夹持器
        self.open_gripper()
        rospy.sleep(0.5)

        # 2. 移动到接近点
        approach_joints = [j1, self.APPROACH_J2, self.APPROACH_J3, self.APPROACH_J4, self.APPROACH_J5]
        rospy.loginfo("  -> 移动到接近点")
        if not self.move_to_joints(approach_joints):
            self.go_home()
            rospy.sleep(0.5)
            if not self.move_to_joints(approach_joints):
                rospy.logwarn("无法到达接近点")
                return False
        rospy.sleep(0.5)

        # 3. 移动到抓取点
        grasp_joints = [j1, self.GRASP_J2, self.GRASP_J3, self.GRASP_J4, self.GRASP_J5]
        rospy.loginfo("  -> 移动到抓取点")
        if not self.move_to_joints(grasp_joints):
            rospy.logwarn("无法到达抓取点")
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
        self.move_to_joints(lift_joints)
        rospy.sleep(0.3)

        rospy.loginfo("抓取完成")
        return True

    def place_object(self, place_x, place_y):
        """放置物体"""
        j1 = self.pos_to_joint1(place_x, place_y)
        rospy.loginfo("放置: (%.3f, %.3f), joint1=%.3f", place_x, place_y, j1)

        approach_joints = [j1, self.LIFT_J2, self.LIFT_J3, self.LIFT_J4, self.LIFT_J5]
        self.move_to_joints(approach_joints)
        rospy.sleep(0.3)

        place_joints = [j1, self.PLACE_J2, self.PLACE_J3, self.PLACE_J4, self.PLACE_J5]
        self.move_to_joints(place_joints)
        rospy.sleep(0.3)

        rospy.loginfo("  -> 释放")
        self.open_gripper()
        rospy.sleep(0.5)

        self.move_to_joints(approach_joints)
        rospy.sleep(0.3)

    # ==================== VLM 自然语言 ====================

    def _camera_callback(self, msg):
        if self.cv_bridge is None:
            return
        try:
            self.latest_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            rospy.logwarn_throttle(5.0, "相机图像转换失败: %s", e)

    def format_objects_for_vlm(self):
        lines = []
        for i, obj in enumerate(self.detected_objects):
            x, y, z = obj['position']
            sx, sy, sz = obj['size']
            dist = math.sqrt(x * x + y * y)
            side = '左侧' if y > 0.02 else ('右侧' if y < -0.02 else '正前方')
            color = obj.get('color_name', '未知')
            reachable, _ = self.check_reachable(x, y)
            lines.append(
                '[%d] 颜色=%s 位置=(%.3f,%.3f,%.3f) 尺寸=(%.3f,%.3f,%.3f) '
                '距中心=%.3fm 方位=%s 可达=%s' % (
                    i, color, x, y, z, sx, sy, sz, dist, side,
                    '是' if reachable else '否'))
        return '\n'.join(lines)

    def grasp_object_by_index(self, idx):
        if idx < 0 or idx >= len(self.detected_objects):
            rospy.logwarn("物体索引超出范围 (0~%d)", len(self.detected_objects) - 1)
            return False
        target = self.detected_objects[idx]
        self.scene.remove_world_object("gs_obj_{}".format(idx))
        rospy.sleep(0.3)
        if self.pick_object(target):
            rospy.loginfo("抓取成功!")
            return True
        rospy.logwarn("抓取失败")
        return False

    def grasp_by_vlm(self, query):
        if not self.vlm_client:
            rospy.logerr("VLM 未启用，请设置 vlm/enabled:=true 并配置 API")
            return False
        if not self.detected_objects:
            rospy.logwarn("未检测到物体, 先用 d 加载")
            return False

        rospy.loginfo("VLM 解析指令: %s", query)
        image = self.latest_image if self.vlm_use_camera else None
        if self.vlm_use_camera and image is None:
            rospy.logwarn("尚无相机图像，仅使用物体列表文本")

        try:
            idx, reason = self.vlm_client.select_object_index(
                query, self.format_objects_for_vlm(), image_bgr=image)
        except Exception as e:
            rospy.logerr("VLM 调用失败: %s", e)
            return False

        rospy.loginfo("VLM 选择: index=%s, reason=%s", idx, reason)
        if idx is None:
            rospy.logwarn("VLM 未能匹配物体: %s", reason)
            return False
        return self.grasp_object_by_index(idx)

    # ==================== 主流程 ====================

    def load_and_process(self):
        """加载 3DGS 模型并处理"""
        if not self.gs_ply:
            rospy.logerr("未指定 ply 文件, 请设置 ~gs_ply 参数")
            return False

        data = self.load_gs_ply(self.gs_ply)
        if data is None:
            rospy.logerr("加载 ply 失败")
            return False

        rospy.loginfo("模型加载完成: %d 个点", len(data['positions']))

        self.detected_objects = self.process_gs_model(data)

        if not self.detected_objects:
            rospy.logwarn("未检测到物体")
            rospy.logwarn("  调整建议:")
            rospy.logwarn("  - 增大 ROI_XY_MAX (当前 %.2f) 让更多点进入范围", self.ROI_XY_MAX)
            rospy.logwarn("  - 调整 DARK_THRESHOLD (当前 %d) 或关闭暗色过滤", self.DARK_THRESHOLD)
            rospy.logwarn("  - 检查 scale (当前 %.4f) 是否正确", self.scale)
            return False

        rospy.loginfo("检测到 %d 个物体", len(self.detected_objects))

        # 添加碰撞物体
        self.remove_all_objects()
        for i, obj in enumerate(self.detected_objects):
            self.add_object_to_scene("gs_obj_{}".format(i), obj['position'], obj['size'])
        rospy.sleep(1.0)

        return True

    def run_interactive(self):
        """交互模式"""
        rospy.loginfo("===== 3DGS 抓取仿真 - 交互模式 =====")
        rospy.loginfo("命令:")
        rospy.loginfo("  l <path>  = 加载 ply 文件")
        rospy.loginfo("  d         = 重新检测物体")
        rospy.loginfo("  o         = 列出物体")
        rospy.loginfo("  g <id>    = 抓取指定物体 (默认0)")
        if self.vlm_enabled:
            rospy.loginfo("  v <描述>  = VLM 自然语言抓取 (如: v 抓左边红色的)")
        rospy.loginfo("  p         = 放置物体")
        rospy.loginfo("  h         = 回家")
        rospy.loginfo("  r         = 可达性检查所有物体")
        rospy.loginfo("  s <scale> = 设置缩放因子并重新处理")
        rospy.loginfo("  t <16浮点> = 设置4x4变换矩阵并重新处理")
        rospy.loginfo("  roi <val> = 设置 ROI_XY_MAX 并重新处理")
        rospy.loginfo("  dark <val>= 设置 DARK_THRESHOLD 并重新处理")
        rospy.loginfo("  q         = 退出")

        # 如果启动时已指定 ply, 自动加载
        if self.gs_ply:
            self.load_and_process()

        while not rospy.is_shutdown():
            try:
                cmd = input("\n> ").strip()
            except EOFError:
                break

            if not cmd:
                continue

            parts = cmd.split()
            action = parts[0].lower()

            if action == 'l' and len(parts) > 1:
                self.gs_ply = parts[1]
                self.load_and_process()

            elif action == 'd':
                if self.gs_ply:
                    self.load_and_process()
                else:
                    rospy.logwarn("请先加载 ply 文件: l <path>")

            elif action == 'o':
                for i, obj in enumerate(self.detected_objects):
                    reachable, j1 = self.check_reachable(*obj['position'][:2])
                    status = "OK" if reachable else "UNREACHABLE"
                    rospy.loginfo("  [%d] %s (%.3f, %.3f, %.3f) size=(%.3f, %.3f, %.3f)",
                                  i, status, *obj['position'], *obj['size'])

            elif action == 'g':
                if not self.detected_objects:
                    rospy.logwarn("未检测到物体, 先用 d 加载")
                    continue
                idx = int(parts[1]) if len(parts) > 1 else 0
                self.grasp_object_by_index(idx)

            elif action == 'v':
                if len(parts) < 2:
                    rospy.loginfo("用法: v <自然语言描述>, 例: v 抓最左边的物体")
                    continue
                query = ' '.join(parts[1:])
                self.grasp_by_vlm(query)

            elif action == 'p':
                self.place_object(self.place_x, self.place_y)

            elif action == 'h':
                self.go_home()

            elif action == 'r':
                for i, obj in enumerate(self.detected_objects):
                    reachable, j1 = self.check_reachable(*obj['position'][:2])
                    rospy.loginfo("  [%d] %s j1=%.3f (%.3f, %.3f, %.3f)",
                                  i, "REACHABLE" if reachable else "UNREACHABLE",
                                  j1, *obj['position'])

            elif action == 's':
                if len(parts) > 1:
                    self.scale = float(parts[1])
                    rospy.loginfo("缩放因子: %.4f", self.scale)
                    if self.gs_ply:
                        self.load_and_process()

            elif action == 't':
                if len(parts) == 17:
                    vals = [float(v) for v in parts[1:]]
                    self.T = np.array(vals).reshape(4, 4)
                    rospy.loginfo("变换矩阵已更新")
                    if self.gs_ply:
                        self.load_and_process()
                else:
                    rospy.loginfo("用法: t m00 m01 m02 m03 m10 m11 m12 m13 m20 m21 m22 m23 m30 m31 m32 m33")

            elif action == 'roi':
                if len(parts) > 1:
                    self.ROI_XY_MAX = float(parts[1])
                    rospy.loginfo("ROI_XY_MAX: %.3f", self.ROI_XY_MAX)
                    if self.gs_ply:
                        self.load_and_process()

            elif action == 'dark':
                if len(parts) > 1:
                    self.DARK_THRESHOLD = int(parts[1])
                    rospy.loginfo("DARK_THRESHOLD: %d", self.DARK_THRESHOLD)
                    if self.gs_ply:
                        self.load_and_process()

            elif action == 'q':
                break

            else:
                rospy.loginfo("未知命令: %s", action)

    def run_auto(self):
        """自动模式: 加载 -> 抓取第一个物体 -> 放置"""
        if not self.load_and_process():
            return False

        target = None
        for i, obj in enumerate(self.detected_objects):
            reachable, _ = self.check_reachable(*obj['position'][:2])
            if reachable:
                target = obj
                target_idx = i
                break

        if target is None:
            rospy.logwarn("没有可达的物体")
            self.go_home()
            return False

        rospy.loginfo("选择物体 %d: (%.3f, %.3f, %.3f)",
                      target_idx, *target['position'])

        self.go_home()
        rospy.sleep(0.5)

        self.scene.remove_world_object("gs_obj_{}".format(target_idx))
        rospy.sleep(0.3)

        if self.pick_object(target):
            self.place_object(self.place_x, self.place_y)

        self.go_home()
        self.remove_all_objects()
        return True


def main():
    try:
        sim = GSGraspSim()
        mode = rospy.get_param('~mode', 'interactive')

        if mode == 'auto':
            sim.run_auto()
            rospy.spin()
        else:
            sim.run_interactive()

    except rospy.ROSInterruptException:
        pass
    finally:
        moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    main()
