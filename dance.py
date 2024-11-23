#!/usr/bin/python3
import sys

sys.path.append("TurboPi")
import signal
import asyncio
from helpers.move_robot import move_robot, stop_robot
from helpers.move_camera import move_camera, reset_camera

print("Press Ctrl+C to stop")


def stop(signum, frame):
    print("Shutting down...")
    stop_robot()
    reset_camera()
    sys.exit(0)


signal.signal(signal.SIGINT, stop)


async def dance_moves():
    await move_robot(["forward", "left", "backward", "right"])


async def camera_moves():
    await move_camera(["up", "down", "left", "right"])


async def main():
    # Create tasks for parallel execution
    robot_task = asyncio.create_task(dance_moves())
    camera_task = asyncio.create_task(camera_moves())

    # Wait for both tasks to complete
    await asyncio.gather(robot_task, camera_task)


if __name__ == "__main__":
    asyncio.run(main())
