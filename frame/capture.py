import cv2 as cv

class FrameCapture:
    def __init__(self):
        try:
            self.camera_feed = cv.VideoCapture(0);
        except:
            print("Unable to create video capture")

    def get_camera_current_frame(self):
        nerr, image = self.camera_feed.read()
        if nerr == True:
            return image
        else:
            print("Unable to read camera feed")
