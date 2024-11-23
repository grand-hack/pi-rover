#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/TurboPi/')
import time
import signal
import HiwonderSDK.mecanum as mecanum

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
print('''
**********************************************************
*********************功能:小车转向例程(function: car turning routine)**********************
**********************************************************
----------------------------------------------------------
Official website:https://www.hiwonder.com
Online mall:https://hiwonder.tmall.com
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(press Ctrl+C to close the running program, please try multiple times if failed)
----------------------------------------------------------
''')

chassis = mecanum.MecanumChassis()

start = True
#关闭前处理(process program before closing)
def Stop(signum, frame):
    global start

    start = False
    print('关闭中...')
    chassis.set_velocity(0,0,0)  # 关闭所有电机(close all motors)
    

signal.signal(signal.SIGINT, Stop)

if __name__ == '__main__':
    while start:
        chassis.set_velocity(0,90,0.3)# 顺时针旋转,控制机器人移动函数,线速度0(0~100)，方向角90(0~360)，偏航角速度0.3(-2~2)(clockwise rotation, robot motion control function, linear velocity 0(0~100), heading angle 90(0~360), yaw rate 0.3(-2~2))
        time.sleep(3)
        chassis.set_velocity(0,90,-0.3)# 逆时针旋转(counterclockwise rotation)
        time.sleep(3)
    chassis.set_velocity(0,0,0)  # 关闭所有电机(close all motors)
    print('已关闭')

        
