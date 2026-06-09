#!/usr/bin/env python3
import os
import sys
import time
import HiwonderSDK.tm1640 as tm
import HiwonderSDK.Sonar as Sonar

if sys.version_info.major == 2:
    print('Please rnu this program with python3!')
    sys.exit(0)

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，数码管显示实验例程*********
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
s.startSymphony()

# 字模数据
data = {'0':0x3f,'1':0x06,'2':0x5b,'3':0x4f,'4':0x66,'5':0x6d,'6':0x7d,'7':0x07,'8':0x7f,'9':0x6f}
# 数码管显示'0000'
tm.display_buf = (data['0'],data['0'],data['0'],data['0'])
tm.update_display()
time.sleep(2)

def method(value):
    #divmod()是内置函数，返回整商和余数组成的元组
    result = []
    while value:
        value, r = divmod(value, 10)
        result.append(r)
    result.reverse()
    return result

while True:
    distance = int(s.getDistance()/10) # 获取超声波测距数据,单位cm
    print('dist:',distance)
    da = method(distance)
    nu = len(da)
    
    ## 数码管显示超声波测距数据
    if  nu ==  1:
        tm.display_buf = (data[str(0)], data[str(0)], data[str(0)], data[str(da[0])])
        tm.update_display()
    elif nu == 2:
        tm.display_buf = (data[str(0)], data[str(0)], data[str(da[0])], data[str(da[1])])
        tm.update_display()
    elif nu == 3:
        tm.display_buf = (data[str(0)], data[str(da[0])], data[str(da[1])], data[str(da[2])])
        tm.update_display()
    elif nu == 4:
        tm.display_buf = (data[str(da[0])], data[str(da[1])], data[str(da[2])], data[str(da[3])])
        tm.update_display()
    
    time.sleep(0.3)
