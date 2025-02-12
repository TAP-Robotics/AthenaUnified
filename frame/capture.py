import cv2 as cv
import logging

from cv2.typing import MatLike

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler("AthenaUnified"),
    logging.StreamHandler()
])

class FrameCapture:
    def __init__(self):
        try:
            logger.info("Starting OpenCV video capture")
            self.camera_feed = cv.VideoCapture(0);
            if not self.camera_feed.isOpened():
                raise ValueError("Could not open device")
        except:
            print("Unable to create video capture")
            raise

    def get_camera_current_frame(self) -> MatLike:
        """Get current snapshot of camera feed"""
        nerr, image = self.camera_feed.read()
        if nerr == True:
            return image
        else:
            logger.info("Could not get current camera feed")
            raise

    def get_image_bytes(self, image: MatLike):
        """Converts a MatLike frame into a WebP image for transfer"""
        try:
            quality = [cv.IMWRITE_WEBP_QUALITY, 95]
            success, encoded_image = cv.imencode(".webp", image, quality)
            if not success:
                logger.error("Failed to encode image")
                raise ValueError("Image encoding error")

            return encoded_image
        except Exception as e:
            logger.error(f"Error during camera frame encoding: {e}")
            raise

    def release_camera(self):
        """Releases camera feed. Use at program clean up or anytime the camera feed will not be used"""
        if self.camera_feed is not None:
            self.camera_feed.release()
            logger.info("Camera feed released. Thank you! :)")

