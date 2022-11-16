from msilib.schema import Directory
import tobii_research as tr
import time

class EyeTracker():

    global logFile
    global my_eyetracker
    global threadLock

    def __init__(self):
        found_eyetrackers = tr.find_all_eyetrackers()
        self.my_eyetracker = found_eyetrackers[0]
        print("Address: " + self.my_eyetracker.address)
        print("Model: " + self.my_eyetracker.model)
        print("Name (It's OK if this is empty): " + self.my_eyetracker.device_name)
        print("Serial number: " + self.my_eyetracker.serial_number)

    def gaze_data_callback(self, gaze_data):
        msg = "{gaze_left_eye};{gaze_right_eye}".format(gaze_left_eye=gaze_data['left_gaze_point_on_display_area'], gaze_right_eye=gaze_data['right_gaze_point_on_display_area'])
        t = time.time()
        t_ms = int(t * 1000)
        print(t_ms)
        print(gaze_data)
        self.logFile.write(str(t_ms) + "\n")
        self.logFile.write(str(gaze_data) + "\n")
        self.logFile.flush()
    
    def start(self, participantID, condition, dataFolder):
        self.logFile = open(dataFolder + "\\" + str(participantID) + "\\" + str(condition) + "\\tobii.txt", 'w')
        self.my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)
