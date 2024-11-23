#!/usr/bin/python3
import sys

sys.path.append("TurboPi")
import signal
import asyncio
from helpers.move_robot import move_robot, stop_robot
from helpers.move_camera import move_camera, reset_camera
from helpers.set_eye_color import set_eye_color

print("Press Ctrl+C to stop")

# Define RGB color mappings (each value 0-255)
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "purple": (128, 0, 128),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "off": (0, 0, 0),
}


def stop(signum, frame):
    print("Shutting down...")
    stop_robot()
    reset_camera()
    sys.exit(0)


signal.signal(signal.SIGINT, stop)


async def dance_moves():
    await move_robot(["forward", "left", "backward", "right"])


async def camera_moves():
    await move_camera(["up", "down", "left", "right", "center"])


async def eye_moves():
    color_sequence = [
        ("red", "blue"),
        ("green", "yellow"),
        ("purple", "cyan"),
        ("blue", "red"),
        ("yellow", "green"),
        ("cyan", "purple"),
        ("off", "off"),
    ]
    for i, (left_color, right_color) in enumerate(color_sequence):
        if i != 0:
            await asyncio.sleep(0.5)
        set_eye_color(COLORS[left_color], COLORS[right_color])


async def dance():
    # Create tasks for parallel execution
    robot_task = asyncio.create_task(dance_moves())
    camera_task = asyncio.create_task(camera_moves())
    eye_task = asyncio.create_task(eye_moves())

    try:
        # Wait for all tasks to complete
        await asyncio.gather(robot_task, camera_task, eye_task)
    except Exception:
        stop(signal.SIGINT, None)


if __name__ == "__main__":
    asyncio.run(dance())
