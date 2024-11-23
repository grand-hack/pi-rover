#!/usr/bin/python3
import sys

sys.path.append("TurboPi")

from helpers.set_eye_color import set_eye_color

# Usage example: set right headlight to bright red, left headlight to bright blue
#
# python front-rgb-test.py 255 0 0 0 0 255

if __name__ == "__main__":
    if len(sys.argv) == 7:
        # Expect R1 G1 B1 R2 G2 B2 as arguments
        rgb1 = tuple(int(x) for x in sys.argv[1:4])
        rgb2 = tuple(int(x) for x in sys.argv[4:7])
        set_eye_color(rgb1, rgb2)

    else:
        # Turn off both LEDs
        set_eye_color((0, 0, 0), (0, 0, 0))
