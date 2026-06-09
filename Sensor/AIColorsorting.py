#!/usr/bin/python3
# coding=utf8
import sys
import cv2
import math
import time
import smbus
import threading
import numpy as np
import HiwonderSDK.Board as Board
import HiwonderSDK.Misc as Misc
from apds9960.const import *
from apds9960 import APDS9960
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.yaml_handle as yaml_handle

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

AK = ArmIK()
world_X, world_Y, world_Z= 0, 10, 5
def initMove():
    Board.setBusServoPulse(1, 200, 500)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 5), -90, -30, -90, 2000)
    time.sleep(3)

#校准值
R_W = 2600
G_W = 4400
B_W = 6400
R_B = 120
G_B = 180
B_B = 260

#颜色传感器初始化
bus = smbus.SMBus(1)
apds = APDS9960(bus)
apds.enableLightSensor()
detect_color = None
sensor_status = True
range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'None': (0, 0, 0),}

lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)
    
#设置扩展板的RGB灯颜色使其跟要追踪的颜色一致
def set_rgb(color):
    if color == "red":
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
    elif color == "green":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
    elif color == "blue":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
    else:
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()


def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

# 找出面积最大的轮廓
# 参数为要比较的轮廓的列表
def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None
    for c in contours:  # 历遍所有轮廓
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰
                area_max_contour = c
    return area_max_contour, contour_area_max  # 返回最大的轮廓

rect = None
size = (640, 480)
block_angle = 0
detect_color = 'None'
start_pick_up = False

def getPulse(angle):
    pulse = int(Misc.map(angle, 0, 90, 500, 875))
    return pulse

def move():
    global rect
    global block_angle
    global detect_color
    global __target_color
    global start_pick_up
    global sensor_status
    global world_X, world_Y, world_Z
    
    #放置坐标
    coordinate = {
        'red':   (-15 + 0.5, 12 - 0.5, 1.5),
        'green': (-15 + 0.5, 6 - 0.5,  1.5),
        'blue':  (-15 + 0.5, 0 - 0.5,  1.5)}
    
    servo1 = 500
    
    while True:
        if not sensor_status:
            #读取三个颜色通道值
            red = apds.readRedLight()
            green = apds.readGreenLight()
            blue = apds.readBlueLight()
            #加入校准
            r = abs(int((red - R_B)*255/(R_W - R_B)))
            g = abs(int((green - G_B)*255/(G_W - G_B)))
            b = abs(int((blue - B_B)*255/(B_W - B_B)))
            #判别颜色
            if r - max(g, b) > 40:
                detect_color = 'red'
                __target_color = ('red')
                sensor_status = True
            elif g - max(r, b) > 40:
                detect_color = 'green'
                __target_color = ('green')
                sensor_status = True
            elif b - max(r, g) > 40:
                detect_color = 'blue'
                __target_color = ('blue')
                sensor_status = True
            else:
                detect_color = None
            
        if start_pick_up :  
            set_rgb(detect_color)
            setBuzzer(0.1)
        
            Board.setBusServoPulse(1, servo1 - 280, 500)  # 爪子张开
            time.sleep(0.5)
            servo2_pulse = getPulse(block_angle)
            Board.setBusServoPulse(2, servo2_pulse, 800)
            time.sleep(0.8)
            
            AK.setPitchRangeMoving((world_X, world_Y, 1.5), -90, -90, 0, 1000)
            time.sleep(1.5)

            Board.setBusServoPulse(1, servo1, 500)  #夹持器闭合
            time.sleep(0.8)

            Board.setBusServoPulse(2, 500, 500)
            AK.setPitchRangeMoving((world_X, world_Y, 12), -90, -90, 0, 1000)  #机械臂抬起
            time.sleep(1)
        
            result = AK.setPitchRangeMoving((coordinate[detect_color][0], coordinate[detect_color][1], 12), -90, -90, 0)   
            time.sleep(result[2]/1000)
            
                           
            servo2_pulse = getAngle(coordinate[detect_color][0], coordinate[detect_color][1], -90)
            Board.setBusServoPulse(2, servo2_pulse, 500)
            time.sleep(0.5)

            AK.setPitchRangeMoving((coordinate[detect_color][0], coordinate[detect_color][1], coordinate[detect_color][2] + 3), -90, -90, 0, 500)
            time.sleep(0.5)
                    
            AK.setPitchRangeMoving((coordinate[detect_color]), -90, -90, 0, 1000)
            time.sleep(0.8)

        
            Board.setBusServoPulse(1, servo1 - 200, 500)  # 爪子张开  ，放下物体
            time.sleep(0.8)

         
            AK.setPitchRangeMoving((coordinate[detect_color][0], coordinate[detect_color][1], 12), -90, -90, 0, 800)
            time.sleep(0.8)

            initMove()  # 回到初始位置
            time.sleep(1.5)
            world_X, world_Y, world_Z= 0, 10, 5
            detect_color = 'None'
            start_pick_up = False
            sensor_status = False
            set_rgb(detect_color)
            
        time.sleep(0.01)
          
#运行子线程
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()    


def run(img):
    global rect
    global detect_color
    global start_pick_up
    global block_angle
    global world_X, world_Y, world_Z
    
    if detect_color is not None:
        
        if start_pick_up:
            return img
        
        img_copy = img.copy()
        frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间
        color_area_max = None
        max_area = 0
        areaMaxContour_max = 0
        if not start_pick_up:
            for i in lab_data:
                if i in __target_color:
                    frame_mask = cv2.inRange(frame_lab,
                                                 (lab_data[i]['min'][0],
                                                  lab_data[i]['min'][1],
                                                  lab_data[i]['min'][2]),
                                                 (lab_data[i]['max'][0],
                                                  lab_data[i]['max'][1],
                                                  lab_data[i]['max'][2]))  #对原图像和掩模进行位运算
                    opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算
                    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算
                    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓
                    areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓
                    
                    if areaMaxContour is not None:
                        if area_max > max_area:  # 找最大面积
                            max_area = area_max
                            color_area_max = i
                            areaMaxContour_max = areaMaxContour
            
            if max_area > 500:  # 有找到最大面积
                rect = cv2.minAreaRect(areaMaxContour_max)
                box = np.int0(cv2.boxPoints(rect))
                cv2.drawContours(img, [box], -1, range_rgb[color_area_max], 2)
                y = int((box[1][0]-box[0][0])/2+box[0][0])
                x = int((box[2][1]-box[0][1])/2+box[0][1])
                
                if x < 390:
                    world_Y += 0.1
                    st1 = False
                elif x > 420:
                    world_Y -= 0.1
                    st1 = False
                else:
                    st1 = True
                if y < 235:
                    world_X -= 0.1
                    st2 = False
                elif y > 260:
                    world_X += 0.1
                    st2 = False
                else:
                    st2 = True
                    
                if st1 and st2:
                    start_pick_up = True
                    block_angle = int(rect[2])
                AK.setPitchRangeMoving((world_X, world_Y, world_Z), -90, -30, -90, 100)
                time.sleep(0.1)
        draw_color = range_rgb[detect_color]    
        cv2.putText(img, "Color: " + detect_color, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, draw_color, 2)
    return img

    
if __name__ == '__main__':
    
    print('loading......')
    cap = cv2.VideoCapture(-1) #读取摄像头
    print('loading completed!')
    initMove()
    sensor_status = False
    while True:
            
        ret, img = cap.read()
        if ret:
            frame = img.copy()
            Frame = run(frame)           
            cv2.imshow('Frame', Frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()
    

        
