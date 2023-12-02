import threading
import cv2
import time
from modules.config import Config

class Camera(threading.Thread):
    def __init__(self, config:Config):
        threading.Thread.__init__(self)
        self.config = config
        self.data_folder = config.get("data_folder")
        self.width = 1920
        self.height = 1080
        self.fps = 60.0

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.fourcc = cv2.VideoWriter.fourcc(*'avc1')
        self.out = cv2.VideoWriter(self.data_folder + "camera_output.mp4", self.fourcc, self.fps, (self.width, self.height))

    def test(self):
        print("Testing Camera")
        ret, frame = self.cap.read()
        if not ret:
            raise BaseException("Camera test failed")

    def run(self):
        self.exception = None
        _stop = self.config.get_stop()
        print("Starting Camera")
        timestamps = open(self.data_folder + "camera_timestamps.txt", "w")
        try:
            while(not _stop.isSet()):
                # Capture the video frame by frame
                ret, frame = self.cap.read()
                t_ms = int(time.time() * 1000)

                if ret:
                    self.out.write(frame)
                    timestamps.write(str(t_ms) + "\n")
            
            self.out.release()
            self.cap.release()
            timestamps.close()
            print("Camera stopped")
        except BaseException as e:
            self.exception = e
        
    def join(self):
        threading.Thread.join(self)
        if self.exception:
            raise self.exception