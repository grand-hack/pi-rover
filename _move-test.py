#!/usr/bin/python3
# coding=utf8
import sys
import asyncio

sys.path.append("TurboPi")
import signal
from helpers.move_robot import move_robot, stop_robot

print("Press Ctrl+C to stop")


# Process before closing
def stop(signum, frame):
    print("Shutting down...")
    stop_robot()
    sys.exit(0)


signal.signal(signal.SIGINT, stop)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(move_robot(sys.argv[1:]))
    else:
        asyncio.run(move_robot(["forward"]))
