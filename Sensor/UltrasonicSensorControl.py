#!/usr/bin/env python3
import os
import sys
import time
import HiwonderSDK.Sonar as Sonar
import HiwonderSDK.Board as Board
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
from HiwonderSDK.Board import setBusServoPulse, getBusServoPulse

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，机械臂超声波控制实验例程*********
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
Version: --V1.0  2021/08/13
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

AK = ArmIK()
setBusServoPulse(1, 200, 500)
setBusServoPulse(2, 500, 500)
AK.setPitchRangeMoving((0, 10, 18), 0, -30, -90, 1500)

s = Sonar.Sonar()
s.setRGBMode(0)
s.startSymphony() # 设置超声波RGB颜色渐变模式

def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

while True:
    distance = s.getDistance() / 10
    print("Distance:", distance,"cm")
    if distance <= 15.0 :
        setBuzzer(0.1)   #设置蜂鸣器响0.1秒
        time.sleep(1.5)
        setBusServoPulse(1, 600, 500)
        time.sleep(1)
        AK.setPitchRangeMoving((0, 12, 1), -90, -30, -90, 2000)
        time.sleep(2.2)
        setBusServoPulse(1, 200, 500)
        time.sleep(0.5)
        AK.setPitchRangeMoving((0, 10, 18), 0, -30, -90, 2000)
        time.sleep(2.2)
        
    time.sleep(0.1)
    
