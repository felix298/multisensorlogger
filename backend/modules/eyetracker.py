from tobiiresearch.implementation import EyeTracker as tr
import time
import threading
import os
from modules.config import Config

class EyeTracker(threading.Thread):
    def __init__(self, config:Config):
        threading.Thread.__init__(self)
        self.config = config
        self.eyetracker = None

    def gaze_data_callback(self, gaze_data):
        msg = "{gaze_left_eye};{gaze_right_eye}".format(gaze_left_eye=gaze_data['left_gaze_point_on_display_area'], gaze_right_eye=gaze_data['right_gaze_point_on_display_area'])
        t_ms = int(time.time() * 1000)
        with open(self.data_folder + 'tobii.txt', "a" if os.path.isfile(self.data_folder + 'tobii.txt') else "x") as f:
            f.write(f'{t_ms}\n{msg}\n')

    def run(self):
        self.exception = None
        if len(tr.find_all_eyetrackers()) > 0:
            self.eyetracker: tr.EyeTracker = tr.find_all_eyetrackers()[0]
            print("tobii EyeTracker ready")
        if self.eyetracker is None:
            self.exception = ValueError("EyeTracker not found. Make sure it is connected and that Tobii Manager is running.")
        self.data_folder = self.config.get("data_folder")
        _stop = self.config.get_stop()
        if self.eyetracker is not None:
            print("Starting EyeTracker")
            try:
                self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
                _stop.wait()
                self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
            except BaseException as e:
                self.exception = e
        
    def join(self):
        threading.Thread.join(self)
        if self.exception:
            print("Exception in EyeTracker")
            raise self.exception