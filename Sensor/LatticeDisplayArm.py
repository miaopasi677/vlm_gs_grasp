#!/usr/bin/env python3
import os
import sys
import time
import HiwonderSDK.tm1640 as tm
import HiwonderSDK.ActionGroupControl as AGC

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，点阵显示实验例程*********
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

## 显示'FPV'
tm.display_buf = (0xff, 0x09, 0x09, 0x09, 0x00, 0xff, 0x09, 0x09,
                  0x0f, 0x00, 0x3f,0x40, 0x80, 0x80, 0x40, 0x3f)

tm.update_display()
AGC.runAction('wave') # 参数为动作组的名称，不包含后缀，以字符形式传入

time.sleep(5)
tm.display_buf = [0] * 16
tm.update_display()
