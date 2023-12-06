import tobii_research as tr
import time
import threading
from modules.config import Config

class EyeTracker(threading.Thread):
    def __init__(self, config:Config):
        threading.Thread.__init__(self)
        self.config = config
        self.data_folder = config.get("data_folder")
        self.my_eyetracker = tr.find_all_eyetrackers()

        if len(self.my_eyetracker) > 0:
            self.my_eyetracker = self.my_eyetracker[0]
            print("tobii EyeTracker ready")

    def gaze_data_callback(self, gaze_data):
        msg = "{gaze_left_eye};{gaze_right_eye}".format(gaze_left_eye=gaze_data['left_gaze_point_on_display_area'], gaze_right_eye=gaze_data['right_gaze_point_on_display_area'])
        t_ms = int(time.time() * 1000)
        with open(self.data_folder + 'tobii.txt', 'a') as f:
            f.write(f'{t_ms}\n{msg}\n')

    def run(self):
        self.exception = None
        _stop = self.config.get_stop()
        if self.my_eyetracker is not None:
            print("Starting EyeTracker")
            try:
                self.my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
                _stop.wait()
                self.my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
            except BaseException as e:
                self.exception = e
        
    def join(self):
        threading.Thread.join(self)
        if self.exception:
            raise self.exception