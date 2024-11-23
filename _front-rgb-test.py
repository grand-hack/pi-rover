#!/usr/bin/python3
import sys
sys.path.append('TurboPi')
from smbus2 import SMBus

# Usage example: set right headlight to bright red, left headlight to bright blue
#
# python front-rgb-test.py 255 0 0 0 0 255

class LEDController:
    def __init__(self):
        self.i2c_addr = 0x77
        self.i2c = 1

    def set_led(self, index, rgb):
        try:
            start_reg = 3 if index == 0 else 6
            with SMBus(self.i2c) as bus:
                bus.write_byte_data(self.i2c_addr, start_reg, rgb[0])
                bus.write_byte_data(self.i2c_addr, start_reg+1, rgb[1])
                bus.write_byte_data(self.i2c_addr, start_reg+2, rgb[2])
        except Exception as e:
            print(f"Error setting LED: {e}")

if __name__ == '__main__':
    leds = LEDController()
    
    if len(sys.argv) == 7:
        # Expect R1 G1 B1 R2 G2 B2 as arguments
        rgb1 = [int(x) for x in sys.argv[1:4]]
        rgb2 = [int(x) for x in sys.argv[4:7]]
        leds.set_led(0, rgb1)
        leds.set_led(1, rgb2)
    else:
        # Turn off both LEDs
        leds.set_led(0, [0, 0, 0])
        leds.set_led(1, [0, 0, 0])
