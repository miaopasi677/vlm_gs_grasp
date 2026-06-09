#!/usr/bin/python3
# coding=utf8
import sys
import os
import time

# 添加当前目录和父目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 添加 HiwonderSDK 目录到路径（Board.py 需要从当前目录导入 BusServoCmd）
hiwonder_sdk_dir = os.path.join(current_dir, 'HiwonderSDK')
if hiwonder_sdk_dir not in sys.path:
    sys.path.insert(0, hiwonder_sdk_dir)

try:
    # 先尝试直接导入
    import HiwonderSDK.Board as Board
    from ArmIK.ArmMoveIK import *
except ImportError:
    # 如果失败，尝试修改 Board.py 的路径依赖
    try:
        # Board.py 需要从同一目录导入 BusServoCmd
        # 确保 HiwonderSDK 目录在路径中
        sys.path.insert(0, hiwonder_sdk_dir)
        
        # 重新导入
        import importlib
        if 'HiwonderSDK.Board' in sys.modules:
            del sys.modules['HiwonderSDK.Board']
        if 'Board' in sys.modules:
            del sys.modules['Board']
        
        import HiwonderSDK.Board as Board
        from ArmIK.ArmMoveIK import *
    except ImportError as e:
        print("错误: 无法导入模块")
        print("错误详情: {}".format(e))
        print("\n请检查:")
        print("1. 当前工作目录: {}".format(os.getcwd()))
        print("2. 脚本所在目录: {}".format(current_dir))
        print("3. HiwonderSDK 目录是否存在: {}".format(os.path.exists(os.path.join(current_dir, 'HiwonderSDK'))))
        print("4. ArmIK 目录是否存在: {}".format(os.path.exists(os.path.join(current_dir, 'ArmIK'))))
        print("\n请确保:")
        print("- 在 Ai_FPV 目录下运行此程序")
        print("- 使用命令: cd ~/Ai_FPV && python3 SimpleGrasp.py")
        print("- 或者: python3 ~/Ai_FPV/SimpleGrasp.py")
        sys.exit(1)

# 简单的移动抓取测试程序

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

AK = ArmIK()

# 初始位置参数
x = 0.0
y = 12.0
z = 5.0

def initMove():
    """初始化机械臂位置"""
    print("初始化机械臂位置...")
    Board.setBusServoPulse(1, 150, 800)  # 夹持器打开
    Board.setBusServoPulse(2, 500, 800)  # 云台居中
    AK.setPitchRangeMoving((x, y, z), -90, -90, 0, 1500)
    time.sleep(2)
    print("初始化完成")

def setBuzzer(timer):
    """控制蜂鸣器"""
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

def move_to_position(x_pos, y_pos, z_pos, speed=1500):
    """移动到指定位置"""
    print("移动到位置: ({:.1f}, {:.1f}, {:.1f})".format(x_pos, y_pos, z_pos))
    result = AK.setPitchRangeMoving((x_pos, y_pos, z_pos), -90, -90, 0, speed)
    if result:
        time.sleep(speed / 1000.0 + 0.1)
        return True
    else:
        print("警告: 无法到达该位置")
        return False

def open_gripper():
    """打开夹持器"""
    print("打开夹持器")
    Board.setBusServoPulse(1, 150, 500)
    time.sleep(0.5)

def close_gripper():
    """关闭夹持器"""
    print("关闭夹持器")
    Board.setBusServoPulse(1, 450, 500)
    time.sleep(0.5)

def set_servo2(angle):
    """设置云台角度 (角度范围: 0-90度)"""
    # 将角度转换为脉冲宽度 (0度=500, 90度=700)
    if angle < 0:
        angle = 0
    if angle > 90:
        angle = 90
    pulse = int(500 + (angle / 90.0) * 200)
    print("设置云台角度: {:.1f}度 (脉冲: {})".format(angle, pulse))
    Board.setBusServoPulse(2, pulse, 500)
    time.sleep(0.5)

def simple_grasp_sequence():
    """简单的抓取序列"""
    print("\n" + "="*50)
    print("开始简单抓取序列")
    print("="*50)
    
    # 1. 初始化
    initMove()
    
    # 2. 移动到目标位置上方
    print("\n步骤1: 移动到目标位置上方")
    target_x = 0.0
    target_y = 12.0
    target_z = 5.0
    move_to_position(target_x, target_y, target_z, 1500)
    
    # 3. 打开夹持器
    print("\n步骤2: 打开夹持器")
    open_gripper()
    
    # 4. 调整云台角度（可选）
    print("\n步骤3: 调整云台角度")
    set_servo2(0)  # 0度
    
    # 5. 蜂鸣器提示
    print("\n步骤4: 准备抓取")
    setBuzzer(0.1)
    
    # 6. 下降到抓取高度
    print("\n步骤5: 下降到抓取高度")
    move_to_position(target_x, target_y + 1.6, 0, 800)
    
    # 7. 关闭夹持器（抓取）
    print("\n步骤6: 关闭夹持器（抓取物体）")
    close_gripper()
    time.sleep(0.5)
    
    # 8. 抬起物体
    print("\n步骤7: 抬起物体")
    move_to_position(target_x, target_y, target_z, 1500)
    
    # 9. 移动到放置位置
    print("\n步骤8: 移动到放置位置")
    place_x = -12.0
    place_y = 0.0
    place_z = 5.0
    move_to_position(place_x, place_y, place_z, 1500)
    
    # 10. 下降到放置高度
    print("\n步骤9: 下降到放置高度")
    move_to_position(place_x, place_y, place_z - 2, 1000)
    
    # 11. 打开夹持器（释放物体）
    print("\n步骤10: 打开夹持器（释放物体）")
    open_gripper()
    time.sleep(0.5)
    
    # 12. 抬起
    print("\n步骤11: 抬起")
    move_to_position(place_x, place_y, place_z, 1000)
    
    # 13. 回到初始位置
    print("\n步骤12: 回到初始位置")
    move_to_position(x, y, z, 1500)
    
    # 14. 完成提示
    print("\n步骤13: 完成")
    setBuzzer(0.2)
    
    print("\n" + "="*50)
    print("抓取序列完成！")
    print("="*50)

def manual_control():
    """手动控制模式"""
    print("\n" + "="*50)
    print("手动控制模式")
    print("="*50)
    print("命令说明:")
    print("  m x y z  - 移动到位置 (例如: m 0 12 5)")
    print("  o        - 打开夹持器")
    print("  c        - 关闭夹持器")
    print("  s 角度   - 设置云台角度 (例如: s 45)")
    print("  h        - 回到初始位置")
    print("  q        - 退出")
    print("="*50)
    
    initMove()
    
    while True:
        try:
            cmd = input("\n请输入命令: ").strip().split()
            if not cmd:
                continue
                
            action = cmd[0].lower()
            
            if action == 'q':
                print("退出手动控制")
                break
            elif action == 'm' and len(cmd) >= 4:
                x_pos = float(cmd[1])
                y_pos = float(cmd[2])
                z_pos = float(cmd[3])
                move_to_position(x_pos, y_pos, z_pos)
            elif action == 'o':
                open_gripper()
            elif action == 'c':
                close_gripper()
            elif action == 's' and len(cmd) >= 2:
                angle = float(cmd[1])
                set_servo2(angle)
            elif action == 'h':
                print("回到初始位置")
                move_to_position(x, y, z)
            else:
                print("无效命令，请重新输入")
        except ValueError as e:
            print("输入错误: {}".format(e))
        except KeyboardInterrupt:
            print("\n\n退出程序")
            break

if __name__ == '__main__':
    print('='*50)
    print('简单移动抓取测试程序')
    print('='*50)
    print('请选择模式:')
    print('1. 自动抓取序列')
    print('2. 手动控制')
    print('='*50)
    
    try:
        choice = input('\n请输入选择 (1 或 2): ').strip()
        
        if choice == '1':
            simple_grasp_sequence()
        elif choice == '2':
            manual_control()
        else:
            print("无效选择，运行自动抓取序列")
            simple_grasp_sequence()
            
    except KeyboardInterrupt:
        print("\n\n程序被中断")
    finally:
        print("\n程序结束")
        # 回到初始位置
        try:
            move_to_position(x, y, z, 1000)
            open_gripper()
        except:
            pass

