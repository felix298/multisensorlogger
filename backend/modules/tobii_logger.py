import tobii_research as tr
import time
import threading
from modules.config import Config

class EyeTracker():
    def __init__(self):
        self.data_folder = Config().get("data_folder")
        self.my_eyetracker = tr.find_all_eyetrackers()

        if len(self.my_eyetracker) > 0:
            self.my_eyetracker = self.my_eyetracker[0]
            print("tobii EyeTracker ready")

    def gaze_data_callback(self, gaze_data):
        msg = "{gaze_left_eye};{gaze_right_eye}".format(gaze_left_eye=gaze_data['left_gaze_point_on_display_area'], gaze_right_eye=gaze_data['right_gaze_point_on_display_area'])
        t_ms = int(time.time() * 1000)
        with open(self.data_folder + 'tobii.txt', 'a') as f:
            f.write(f'{t_ms}\n{gaze_data}\n')

    def start(self):
        self.thread = threading.Thread(target=self._capture_eyes, daemon=True)
        self.thread.start()

    def _capture_eyes(self):
        if self.my_eyetracker is not None:
            print("Starting EyeTracker")
            self.my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)

    def stop(self):
        if self.my_eyetracker is not None:
            print("Stopping EyeTracker")
            self.my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)