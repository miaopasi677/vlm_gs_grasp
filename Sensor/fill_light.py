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
time.sleep(3)

s.setRGB(1, (255,255,255))  #两边RGB设置为白色
s.setRGB(0, (255,255,255))

