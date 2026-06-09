#!/usr/bin/env python3
import os
import sys
import time
import HiwonderSDK.Sonar as Sonar
import HiwonderSDK.Board as Board

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，超声波测距实验例程*********
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
----------------------------------------------------------
以下指令均需在LX终端使用，LX终端可通过ctrl+alt+t打开，或点
击上栏的黑色LX终端图标。
----------------------------------------------------------
Version: --V1.0  2021/08/13
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

s = Sonar.Sonar()
s.setRGBMode(0)
s.startSymphony() # 设置超声波RGB颜色渐变模式

def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

while True:
    distance = s.getDistance() / 10  # 获取超声波测距数据,单位cm
    if distance <= 15.0 :
        setBuzzer(0.1)   #设置蜂鸣器响0.1秒
        time.sleep(0.2)
    
    print("Distance:", distance)
    time.sleep(0.1)
    