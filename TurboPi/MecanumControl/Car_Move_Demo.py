#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/grand/client-daily-python/TurboPi/')
import time
import signal
import HiwonderSDK.mecanum as mecanum

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
print('''
**********************************************************
**************** Car Movement Demo Program ******************
**********************************************************
----------------------------------------------------------
Official website: https://www.hiwonder.com
Online mall: https://hiwonder.tmall.com
----------------------------------------------------------
Tips:
 * Press Ctrl+C to stop the program. Try multiple times if needed.
----------------------------------------------------------
''')

chassis = mecanum.MecanumChassis()

start = True
#Process before closing
def Stop(signum, frame):
    global start

    start = False
    print('Shutting down...')
    chassis.set_velocity(0,0,0)  # Stop all motors
    

signal.signal(signal.SIGINT, Stop)

if __name__ == '__main__':
    while start:
        chassis.set_velocity(50,90,0) # Robot motion control function: linear velocity 50 (0-100), heading angle 90 (0-360), yaw rate 0 (-2 to 2)
        time.sleep(1)
        chassis.set_velocity(50,0,0)
        time.sleep(1)
        chassis.set_velocity(50,270,0)
        time.sleep(1)
        chassis.set_velocity(50,180,0)
        time.sleep(1)
    chassis.set_velocity(0,0,0)  # Turn off all motors
    print('Shutdown complete')

        
