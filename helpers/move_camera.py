import asyncio
import HiwonderSDK.ros_robot_controller_sdk as rrc

# May need to adjust this for each robot
#
SERVO_V_CENTER = 1750
SERVO_V_DELTA = 400

SERVO_H_CENTER = 1500
SERVO_H_DELTA = 600

# 1 is one second.
# Argument must be an integer. Seems like it should be 1
MOVEMENT_DURATION = 0.7


board = rrc.Board()


async def reset_camera():
    board.pwm_servo_set_position(
        MOVEMENT_DURATION, [[1, SERVO_V_CENTER], [2, SERVO_H_CENTER]]
    )


async def move_camera(moves: list[str]):
    for i, command in enumerate(moves):
        if i != 0:
            await asyncio.sleep(MOVEMENT_DURATION)

        positions = {
            "up": [(1, SERVO_V_CENTER - SERVO_V_DELTA), (2, SERVO_H_CENTER)],
            "down": [(1, SERVO_V_CENTER + SERVO_V_DELTA), (2, SERVO_H_CENTER)],
            "center": [(1, SERVO_V_CENTER), (2, SERVO_H_CENTER)],
            "left": [(1, SERVO_V_CENTER), (2, SERVO_H_CENTER + SERVO_H_DELTA)],
            "right": [(1, SERVO_V_CENTER), (2, SERVO_H_CENTER - SERVO_H_DELTA)],
        }

        if command in positions:
            servo_movements = positions[command]
            for servo_movement in servo_movements:
                servo_num, final_pos = servo_movement
                board.pwm_servo_set_position(
                    MOVEMENT_DURATION, [[servo_num, final_pos]]
                )
