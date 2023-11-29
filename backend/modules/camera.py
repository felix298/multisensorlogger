import threading
import cv2
import time
from modules.config import Config

class Camera():
    def __init__(self):
        self.data_folder = Config().get("data_folder")
        self.width = 1920
        self.height = 1080
        self.fps = 60.0

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.fourcc = cv2.VideoWriter.fourcc(*'avc1')
        self.out = cv2.VideoWriter(self.data_folder + "camera_output.mp4", self.fourcc, self.fps, (self.width, self.height))
        self.stop_playback = False

    def start(self):
        self.thread = threading.Thread(target=self._capture_video, daemon=True)
        self.thread.start()

    def test(self):
        ret, frame = self.cap.read()
        return ret

    def _capture_video(self):
        print("Starting Camera")
        timestamps = open(self.data_folder + "camera_timestamps.txt", "w")
        while(True):
            # Capture the video frame by frame
            ret, frame = self.cap.read()
            t_ms = int(time.time() * 1000)
            if ret:
                self.out.write(frame)
                timestamps.write(str(t_ms) + "\n")

            if self.stop_playback:
                break
        
        self.out.release()
        self.cap.release()
        timestamps.close()
        print("Camera stopped")

    def stop(self):
        print("Stopping Camera")
        self.stop_playback = True