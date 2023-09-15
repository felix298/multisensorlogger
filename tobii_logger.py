import tobii_research as tr
import time

class EyeTracker():
    def __init__(self, data_folder):
        self.my_eyetracker = tr.find_all_eyetrackers()[0]
        self.data_folder = data_folder
        print("EyeTracker ready")

    def gaze_data_callback(self, gaze_data):
        msg = "{gaze_left_eye};{gaze_right_eye}".format(gaze_left_eye=gaze_data['left_gaze_point_on_display_area'], gaze_right_eye=gaze_data['right_gaze_point_on_display_area'])
        t_ms = int(time.time() * 1000)
        with open(self.data_folder + 'tobii.txt', 'a') as f:
            f.write(f'{t_ms}\n{gaze_data}\n')

    def start(self):
        print("Starting EyeTracker")
        self.my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)

    def stop(self):
        print("Stopping EyeTracker")
        self.my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)