#!/usr/bin/env python3
import os
import sys
import time
import signal
import smbus
import RPi.GPIO as GPIO
from HiwonderSDK import Board
from apds9960.const import *
from apds9960 import APDS9960


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，颜色传感器实验例程*********
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

start = True
#关闭前处理
def Stop(signum, frame):
    global start

    start = False
    print('关闭中...')

#先将所有灯关闭
Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
Board.RGB.show()

signal.signal(signal.SIGINT, Stop)

while True:

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
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))  #设置2个灯为红色
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
    elif g - max(r, b) > 40:
        detect_color = 'green'
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))  #设置2个灯为绿色
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
    elif b - max(r, g) > 40:
        detect_color = 'blue'
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))  #设置2个灯为蓝色
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
    else:
        detect_color = None
        Board.RGB.setPixelColor(0, Board.PixelColor(50, 50, 50))   #所有灯低亮度白色
        Board.RGB.setPixelColor(1, Board.PixelColor(50, 50, 50))
        Board.RGB.show()
    print(detect_color)
    
    if not start:
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))  #所有灯关闭
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()
        print('已关闭')
        break


