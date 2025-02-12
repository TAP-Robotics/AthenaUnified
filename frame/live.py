from multiprocessing.process import current_process
from frame.capture import FrameCapture
from messages.nanos import Message, Nanos

import logging
import time
import json
import asyncio
import base64

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("AthenaUnified"),
    logging.StreamHandler()
])

class LiveCaptureSend:
    def __init__(self):
        logger.info("Intializing live capture sender")

    async def caputure_main_loop(self) -> None:
        """Loop that handles sending frames to the server and receiving responses."""
        reference_time = time.time()
        capture = FrameCapture()
        nanos = Nanos()
        
        while True:
            try:

                # Sending message (with time debouncing)
                current_time = time.time()
                if current_time - reference_time >= 0.14:
                    snapshot = capture.get_camera_current_frame()
                    image_string = capture.get_image_bytes(snapshot)
                    encoded_string = base64.b64encode(image_string).decode('utf-8')
                    message = Message(message="vision_infer", content=encoded_string)
                    json_message = json.dumps(message.__dict__, indent=4).encode("utf-8")
                    await nanos.send_message(json_message)


                rec = await nanos.receive_message()  # Receive raw bytes
                json_data = json.loads(rec.decode("utf-8"))  # Decode JSON
                message_obj = Message(**json_data)  # Convert to Message object
                logger.info(f"Received message: {message_obj.message}, Content: {message_obj.content}")
                await asyncio.sleep(0.01)

            except Exception as e:
                logger.error(f"An error occurred in the capture loop: {e}")
                await asyncio.sleep(2)
        
    def main_loop_runner(self):
        """Let's try this for multiprocessing"""
        logger.info("Inside main loop runner")
        asyncio.run(self.caputure_main_loop())
