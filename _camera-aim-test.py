import sys

sys.path.append("TurboPi")
import signal
import asyncio
from helpers.move_camera import reset_camera, move_camera

print("Press Ctrl+C to stop")


async def stop(signum, frame):
    print("Shutting down...")
    await reset_camera()
    sys.exit(0)


signal.signal(signal.SIGINT, stop)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(move_camera(sys.argv[1:]))
    else:
        asyncio.run(move_camera(["center"]))
