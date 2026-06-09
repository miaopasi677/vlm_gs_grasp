#!/usr/bin/python3
# coding=utf8
import sys
import cv2
import math
import time
import threading
import numpy as np
import HiwonderSDK.Board as Board
import HiwonderSDK.Misc as Misc
import HiwonderSDK.yaml_handle as yaml_handle
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *

# 针状物体识别与抓取程序

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

AK = ArmIK()

# 初始位置参数
x = 0.0
y = 12.0
z = 5.0

# 图像中心点（用于对准）
centerX = 320
centerY = 240

# 针状物体判断阈值：长宽比
ASPECT_RATIO_THRESHOLD = 3.0  # 长宽比大于3认为是针状物体
MIN_AREA = 200  # 最小轮廓面积

# 状态标志
st = True  # 是否允许开始抓取
needle_detected = False
object_center_x = 0.0
object_center_y = 0.0
object_angle = 0.0
object_length = 0.0
object_width = 0.0
aspect_ratio = 0.0

# 线程锁
lock = threading.Lock()

# 放置位置坐标
PLACE_POSITION = (-12, 0, 5)  # 放置位置

def reset():
    """重置位置参数"""
    global x, y, z
    x = 0.0
    y = 12.0
    z = 5.0

def initMove():
    """初始化机械臂位置"""
    Board.setBusServoPulse(1, 150, 800)  # 夹持器打开
    Board.setBusServoPulse(2, 500, 800)   # 云台居中
    AK.setPitchRangeMoving((x, y, z), -90, -90, 0, 1500)
    time.sleep(1.5)

def setBuzzer(timer):
    """控制蜂鸣器"""
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

def getAreaMaxContour(contours):
    """找出面积最大的轮廓"""
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None
    
    for c in contours:
        contour_area_temp = math.fabs(cv2.contourArea(c))
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > MIN_AREA:
                area_max_contour = c
    
    return area_max_contour, contour_area_max

def detect_needle(img):
    """检测针状物体"""
    global needle_detected, object_center_x, object_center_y
    global object_angle, object_length, object_width, aspect_ratio
    
    with lock:
        needle_detected = False
    img_h, img_w = img.shape[:2]
    
    # 转换为LAB颜色空间进行颜色识别（可选，也可以使用边缘检测）
    # 这里使用Canny边缘检测 + 轮廓分析
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)
    
    # 形态学操作，连接断开的边缘
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # 查找轮廓
    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    
    # 找出最大轮廓
    areaMaxContour, area_max = getAreaMaxContour(contours)
    
    if areaMaxContour is not None and area_max > MIN_AREA:
        # 计算最小外接矩形
        rect = cv2.minAreaRect(areaMaxContour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        # 计算矩形的长和宽
        width = rect[1][0]
        height = rect[1][1]
        
        # 确保长度总是大于宽度
        if width > height:
            length = width
            width_val = height
            angle = rect[2]
        else:
            length = height
            width_val = width
            angle = rect[2] + 90
        
        # 计算长宽比
        if width_val > 0:
            ratio = length / width_val
        else:
            ratio = 0
        
        # 判断是否为针状物体（长宽比大于阈值）
        if ratio >= ASPECT_RATIO_THRESHOLD:
            with lock:
                needle_detected = True
                object_center_x = int(rect[0][0])
                object_center_y = int(rect[0][1])
                object_angle = angle
                object_length = length
                object_width = width_val
                aspect_ratio = ratio
            
            # 绘制检测框
            cv2.drawContours(img, [box], -1, (0, 255, 0), 2)
            cv2.circle(img, (object_center_x, object_center_y), 5, (0, 0, 255), -1)
            
            # 绘制方向线
            center = (object_center_x, object_center_y)
            angle_rad = math.radians(object_angle)
            end_x = int(center[0] + 50 * math.cos(angle_rad))
            end_y = int(center[1] + 50 * math.sin(angle_rad))
            cv2.line(img, center, (end_x, end_y), (255, 0, 0), 2)
            
            return True, img
    
    return False, img

def move():
    """机械臂控制线程"""
    global x, y, z, st
    global needle_detected, object_center_x, object_center_y, object_angle, aspect_ratio
    
    num = 0  # 码垛计数
    slow = True
    x_st = False
    y_st = False
    
    while True:
        with lock:
            detected = needle_detected
        
        if detected and st:
            # 获取当前检测到的物体位置
            with lock:
                center_x = object_center_x
                center_y = object_center_y
            
            # 调整X轴位置
            if (center_x - centerX) > 20:
                x += 0.2
                x_st = False
            elif (center_x - centerX) < -20:
                x -= 0.2
                x_st = False
            else:
                x_st = True
            
            # 调整Y轴位置
            if (center_y - centerY) > 10:
                y -= 0.1
                y_st = False
            elif (center_y - centerY) < -10:
                y += 0.1
                y_st = False
            else:
                y_st = True
            
            # 移动机械臂
            if slow:
                AK.setPitchRangeMoving((x, y, 3), -90, -90, 0, 800)
                time.sleep(0.8)
                slow = False
            else:
                AK.setPitchRangeMoving((x, y, 3), -90, -90, 0, 100)
                time.sleep(0.1)
            
            # 当机械臂已经对准物体上方时，开始抓取
            if x_st and y_st:
                st = False
                x_st = False
                y_st = False
                slow = True
                
                setBuzzer(0.1)
                print(f"检测到针状物体，长宽比: {aspect_ratio:.2f}, 角度: {object_angle:.1f}°")
                
                if not HARDWARE_AVAILABLE:
                    print("[模拟模式] 跳过实际抓取操作")
                    st = True
                    time.sleep(1)
                    continue
                
                # 调整云台角度以匹配物体方向
                # 将角度转换为舵机脉冲宽度（-45到45度映射到300-700）
                angle_normalized = object_angle % 180
                if angle_normalized > 90:
                    angle_normalized = 180 - angle_normalized
                
                if angle_normalized > 45:
                    angle_normalized = angle_normalized - 45
                    Servo2_Pulse = int(Misc.map(angle_normalized, 0, 45, 300, 500))
                else:
                    Servo2_Pulse = int(Misc.map(angle_normalized, 0, 45, 500, 700))
                
                Board.setBusServoPulse(2, Servo2_Pulse, 500)
                time.sleep(0.5)
                
                # 机械臂下降进行夹取
                AK.setPitchRangeMoving((x, y + 1.6, 0), -90, -90, 0, 500)
                time.sleep(0.5)
                
                # 夹持器闭合
                Board.setBusServoPulse(1, 450, 500)
                time.sleep(0.5)
                
                # 抬起物体
                AK.setPitchRangeMoving((x, y, z), -90, -90, 0, 1500)
                time.sleep(1.5)
                
                # 移动到放置位置上方
                AK.setPitchRangeMoving((PLACE_POSITION[0], PLACE_POSITION[1], PLACE_POSITION[2] + 3*num), -90, -90, 0, 1500)
                time.sleep(1.5)
                
                # 调整放置角度
                Board.setBusServoPulse(2, 500, 500)
                time.sleep(0.5)
                
                # 放置物体
                AK.setPitchRangeMoving((PLACE_POSITION[0], PLACE_POSITION[1], PLACE_POSITION[2] + 3*num), -90, -90, 0, 1000)
                time.sleep(1)
                
                # 夹持器打开
                Board.setBusServoPulse(1, 150, 500)
                time.sleep(0.5)
                
                # 重置位置
                reset()
                
                # 抬起机械臂
                AK.setPitchRangeMoving((PLACE_POSITION[0], PLACE_POSITION[1], PLACE_POSITION[2] + 3*num + 5), -90, -90, 0, 1000)
                time.sleep(1)
                
                # 回到检测位置
                AK.setPitchRangeMoving((x, y, z), -90, -90, 0, 1000)
                time.sleep(1)
                
                # 码垛高度调整
                num += 1
                num = 0 if num > 2 else num
                
                st = True
                time.sleep(1)
        else:
            slow = True
            time.sleep(0.01)

# 启动机械臂控制线程
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()

def run(img):
    """图像处理主函数"""
    global st, needle_detected
    global object_center_x, object_center_y, aspect_ratio
    
    img_h, img_w = img.shape[:2]
    
    if st:  # 只有在允许抓取时才进行检测
        detected, img = detect_needle(img)
        
        if detected:
            cv2.putText(img, f"Needle Detected! Ratio: {aspect_ratio:.2f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, f"Center: ({object_center_x}, {object_center_y})", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(img, f"Angle: {object_angle:.1f} deg", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(img, "No Needle Detected", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.putText(img, "Grasping...", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    return img

def find_camera():
    """查找可用的摄像头"""
    print("正在查找可用的摄像头...")
    for i in range(10):  # 尝试0-9号摄像头
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                print(f"找到摄像头: /dev/video{i}")
                return cap, i
            cap.release()
    return None, -1

if __name__ == '__main__':
    print('=' * 50)
    print('针状物体识别与抓取程序')
    print('=' * 50)
    print('按ESC键退出')
    print()
    
    # 初始化机械臂
    initMove()
    
    # 查找可用摄像头
    cap, camera_index = find_camera()
    
    if cap is None:
        print("错误: 未找到可用的摄像头设备")
        print("请检查:")
        print("1. 摄像头是否已连接")
        print("2. 运行 'ls /dev/video*' 查看可用设备")
        print("3. 检查用户权限 (可能需要将用户添加到 video 组)")
        print("4. 尝试使用 'sudo python3 NeedleDetection.py'")
        sys.exit(1)
    
    print(f"成功打开摄像头 (索引: {camera_index})")
    print("开始检测...")
    print()
    
    try:
        while True:
            ret, img = cap.read()
            if ret:
                frame = img.copy()
                Frame = run(frame)
                cv2.imshow('Needle Detection', Frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC键退出
                    print("\n用户退出程序")
                    break
            else:
                print("警告: 无法读取摄像头画面")
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n程序被中断")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if HARDWARE_AVAILABLE:
            initMove()  # 回到初始位置
        print("程序已退出")

