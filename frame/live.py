from multiprocessing.process import current_process
from frame.capture import FrameCapture
from messages.nanos import Message, Nanos

import logging
import time
import json
import asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("AthenaUnified"),
    logging.StreamHandler()
])


class LiveCaptureSend:
    def __init__(self):
        logger.info("Intializing live capture sender")

    async def caputure_main_loop(self) -> None:
        """Loop that handles sending frames to the server"""
        reference_time = time.time()
        capture = FrameCapture()
        nanos = Nanos()
        while True:
            try:
                current_time = time.time()
                if current_time - reference_time  >= 0.14:
                    snapshot = capture.get_camera_current_frame()
                    image_string = capture.get_image_string(snapshot)
                    message = Message(message="vision_infer", content=str(image_string))
                    json_message = (json.dumps(message.__dict__, indent=4)).encode("utf-8")
                    await nanos.send_message(json_message)
                await asyncio.sleep(0.01)

            except Exception as e:
                logger.error(f"An error occured in the capture loop: {e}")
                await asyncio.sleep(2)

    def main_loop_runner(self):
        """Let's try this for multiprocessing"""
        asyncio.run(self.caputure_main_loop())
