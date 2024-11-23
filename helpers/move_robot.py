import asyncio
import HiwonderSDK.mecanum as mecanum

# 1 is one second.
# Argument must be an integer. Seems like it should be 1
MOVEMENT_DURATION = 0.7

chassis = mecanum.MecanumChassis()

movements = {
    "forward": (50, 90),
    "right": (50, 0),
    "backward": (50, 270),
    "left": (50, 180),
}


def stop_robot():
    chassis.set_velocity(0, 0, 0)


async def move_robot(moves: list[str]):
    for i, command in enumerate(moves):
        velocity, heading = movements[command]
        chassis.set_velocity(velocity, heading, 0)
        await asyncio.sleep(MOVEMENT_DURATION)
    chassis.set_velocity(0, 0, 0)
