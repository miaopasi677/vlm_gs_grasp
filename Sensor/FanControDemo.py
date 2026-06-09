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
********功能:幻尔科技树莓派扩展板，风扇模块实验例程*********
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
 * 3秒之后程序会自动关闭
----------------------------------------------------------
''')

## 初始化引脚模式
GPIO.setup(22, GPIO.OUT) #设置引脚为输出模式
GPIO.setup(24, GPIO.OUT)

## 开启风扇
GPIO.output(22, 1)     #设置引脚输出高电平
GPIO.output(24, 0)     #设置引脚输出低电平

## 延时3秒
time.sleep(3)

## 关闭风扇
GPIO.output(22, 0)
GPIO.output(24, 0)

    
