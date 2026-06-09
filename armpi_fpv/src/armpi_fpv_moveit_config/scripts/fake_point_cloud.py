#!/usr/bin/python3
"""
Fake point cloud publisher for MoveIt Octomap visualization.

Publishes simulated point cloud data representing objects (boxes) on a table
surface in front of the ArmPi FPV robotic arm.

Usage:
  rosrun armpi_fpv_moveit_config fake_point_cloud.py
"""

import struct
import random
import rospy
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header


def create_point_cloud2(points, frame_id, stamp=None):
    """Convert a list of (x,y,z) tuples into a PointCloud2 message."""
    header = Header()
    header.frame_id = frame_id
    header.stamp = stamp if stamp else rospy.Time.now()

    fields = [
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
    ]

    n = len(points)
    cloud = PointCloud2()
    cloud.header = header
    cloud.height = 1
    cloud.width = n
    cloud.fields = fields
    cloud.is_bigendian = False
    cloud.point_step = 12
    cloud.row_step = 12 * n
    cloud.is_dense = True

    buf = bytearray()
    for p in points:
        buf.extend(struct.pack('fff', p[0], p[1], p[2]))
    cloud.data = bytes(buf)

    return cloud


def generate_box_points(cx, cy, cz, sx, sy, sz, density=200):
    """Generate point cloud for a box centered at (cx,cy,cz) with size (sx,sy,sz)."""
    pts = []

    # Top face
    area = sx * sy
    n = max(int(area * density), 20)
    for _ in range(n):
        x = random.uniform(cx - sx/2, cx + sx/2)
        y = random.uniform(cy - sy/2, cy + sy/2)
        pts.append((x, y, cz + sz/2))

    # Front and back faces
    area = sx * sz
    n = max(int(area * density), 20)
    for _ in range(n):
        x = random.uniform(cx - sx/2, cx + sx/2)
        z = random.uniform(cz - sz/2, cz + sz/2)
        pts.append((x, cy - sy/2, z))
        pts.append((x, cy + sy/2, z))

    # Left and right faces
    area = sy * sz
    n = max(int(area * density), 20)
    for _ in range(n):
        y = random.uniform(cy - sy/2, cy + sy/2)
        z = random.uniform(cz - sz/2, cz + sz/2)
        pts.append((cx - sx/2, y, z))
        pts.append((cx + sx/2, y, z))

    return pts


def generate_table_points(tx, ty, tz, size_x, size_y, density=300):
    """Generate point cloud for a flat table surface."""
    area = size_x * size_y
    n = max(int(area * density), 50)
    pts = []
    for _ in range(n):
        x = random.uniform(tx - size_x/2, tx + size_x/2)
        y = random.uniform(ty - size_y/2, ty + size_y/2)
        pts.append((x, y, tz))
    return pts


def main():
    rospy.init_node('fake_point_cloud_publisher', anonymous=True)

    cloud_topic = rospy.get_param('~cloud_topic', '/camera/depth/points')
    cloud_frame = rospy.get_param('~cloud_frame', 'camera_depth_optical_frame')
    publish_rate = rospy.get_param('~publish_rate', 1.0)

    # Table in optical frame (Z = distance below camera)
    table_z = rospy.get_param('~table/z', 0.49)
    table_cx = rospy.get_param('~table/cx', 0.0)
    table_cy = rospy.get_param('~table/cy', 0.0)
    table_sx = rospy.get_param('~table/size_x', 0.5)
    table_sy = rospy.get_param('~table/size_y', 0.4)

    # Box 1
    b1_x = rospy.get_param('~box1/x', 0.0)
    b1_y = rospy.get_param('~box1/y', 0.02)
    b1_z = rospy.get_param('~box1/z', 0.44)
    b1_sx = rospy.get_param('~box1/sx', 0.03)
    b1_sy = rospy.get_param('~box1/sy', 0.03)
    b1_sz = rospy.get_param('~box1/sz', 0.04)

    # Box 2
    b2_x = rospy.get_param('~box2/x', 0.05)
    b2_y = rospy.get_param('~box2/y', 0.02)
    b2_z = rospy.get_param('~box2/z', 0.445)
    b2_sx = rospy.get_param('~box2/sx', 0.04)
    b2_sy = rospy.get_param('~box2/sy', 0.025)
    b2_sz = rospy.get_param('~box2/sz', 0.035)

    pub = rospy.Publisher(cloud_topic, PointCloud2, queue_size=1)
    rate = rospy.Rate(publish_rate)

    rospy.loginfo("Fake point cloud publisher started on %s [%s]", cloud_topic, cloud_frame)

    while not rospy.is_shutdown():
        pts = []
        pts.extend(generate_box_points(b1_x, b1_y, b1_z, b1_sx, b1_sy, b1_sz))
        pts.extend(generate_box_points(b2_x, b2_y, b2_z, b2_sx, b2_sy, b2_sz))
        pts.extend(generate_table_points(table_cx, table_cy, table_z, table_sx, table_sy))

        cloud_msg = create_point_cloud2(pts, cloud_frame)
        pub.publish(cloud_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
