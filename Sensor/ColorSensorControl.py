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
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
from HiwonderSDK.Board import setBusServoPulse, getBusServoPulse

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，颜色传感器例程*********
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
AK.setPitchRangeMoving((0, 10, 10), -45, -30, -90, 1500)

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

def setBuzzer(sleeptime):
    GPIO.setup(6, GPIO.OUT) #设置引脚为输出模式
    GPIO.output(6, 1)       #设置引脚输出高电平
    time.sleep(sleeptime)   #设置延时
    GPIO.output(6, 0)

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
        print(detect_color)
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))  #设置2个灯为红色
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
        
        setBusServoPulse(6, 400, 300)
        time.sleep(0.3)
        setBusServoPulse(6, 600, 600)
        time.sleep(0.6)
        setBusServoPulse(6, 500, 300)
        time.sleep(0.3)
        
    elif g - max(r, b) > 40:
        detect_color = 'green'
        print(detect_color)
        setBuzzer(0.1)
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))  #设置2个灯为绿色
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
        time.sleep(1)
        setBusServoPulse(1, 450, 500)
        time.sleep(1)
        setBusServoPulse(6, 875, 2000)
        time.sleep(2)
        AK.setPitchRangeMoving((-10, 0, 1), -90, -30, -90, 2000)
        time.sleep(2)
        setBusServoPulse(1, 200, 500)
        time.sleep(1)
        AK.setPitchRangeMoving((-10, 0, 10), -45, -30, -90, 1000)
        time.sleep(1)
        AK.setPitchRangeMoving((0, 10, 10), -45, -30, -90, 2000)
        time.sleep(2)
    elif b - max(r, g) > 40:
        detect_color = 'blue'
        setBuzzer(0.1)
        print(detect_color)
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))  #设置2个灯为蓝色
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
        time.sleep(1)
        setBusServoPulse(1, 450, 500)
        time.sleep(1)
        setBusServoPulse(6, 135, 2000)
        time.sleep(2)
        AK.setPitchRangeMoving((10, 0, 1), -90, -30, -90, 2000)
        time.sleep(2)
        setBusServoPulse(1, 200, 500)
        time.sleep(1)
        AK.setPitchRangeMoving((10, 0, 10), -45, -30, -90, 1000)
        time.sleep(1)
        AK.setPitchRangeMoving((0, 10, 10), -45, -30, -90, 2000)
        time.sleep(2)
    else:
        detect_color = None
        Board.RGB.setPixelColor(0, Board.PixelColor(50, 50, 50))   #所有灯低亮度白色
        Board.RGB.setPixelColor(1, Board.PixelColor(50, 50, 50))
        Board.RGB.show()
    
    if not start:
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))  #所有灯关闭
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()
        print('已关闭')
        break


