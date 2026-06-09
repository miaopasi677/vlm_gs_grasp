#!/usr/bin/env python3
import os
import sys
import time
import HiwonderSDK.Sonar as Sonar

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，超声波RGB控制实验例程*********
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
s.setRGBMode(0)      #设置灯的模式，0为彩灯模式，1为呼吸灯模式
s.setRGB(1, (0,0,0)) # 关闭两边RGB
s.setRGB(0, (0,0,0))
time.sleep(1)

while True:
    s.setRGBMode(0) #设置灯的模式，0为彩灯模式，1为呼吸灯模式
    s.setRGB(1, (255,0,0))  #两边RGB设置为红色
    s.setRGB(0, (255,0,0))
    time.sleep(2)
    s.setRGB(1, (0,255,0))  #两边RGB设置为绿色
    s.setRGB(0, (0,255,0))
    time.sleep(2)
    s.setRGB(1, (0,0,255))  #两边RGB设置为蓝色
    s.setRGB(0, (0,0,255))
    time.sleep(2)
    
    s.startSymphony() # 设置超声波RGB颜色渐变模式
    time.sleep(5)
    