#!/usr/bin/env python3
import os
import sys
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，触摸传感器实验例程*********
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

def setBuzzer(sleeptime):
    GPIO.setup(6, GPIO.OUT) #设置引脚为输出模式
    GPIO.output(6, 1)       #设置引脚输出高电平
    time.sleep(sleeptime)   #设置延时
    GPIO.output(6, 0)
    
st = 0

while True:
    GPIO.setup(24, GPIO.IN) #设置引脚为输入模式
    state = GPIO.input(24)  #读取引脚数字值
    
    if not state:
        if st :            #这里做一个判断，防止反复响
            st = 0
            setBuzzer(0.1)   #设置蜂鸣器响0.1秒     
    else:
        st = 1
        GPIO.setup(6, GPIO.OUT)
        GPIO.output(6, 0)
    time.sleep(0.1)
    
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, 0)
