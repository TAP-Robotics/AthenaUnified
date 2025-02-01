from messages import nanos
from frame import capture
import asyncio
import time

capture_handler = capture.FrameCapture()

nanos_socket = nanos.Nanos()

async def cv_loop():
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time >= 0.14:
            print(capture_handler.get_camera_current_frame())

        await asyncio.sleep(0.01) # This would apparently reduce CPU load.
def main():
    print("Hello World")

if __name__ == "__main__":
    asyncio.run(cv_loop())
