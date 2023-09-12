import threading
from pathlib import Path
from opencv_cam import CamRecorder
from tobii_logger import EyeTracker
from video_player import VideoPlayer
from labrecorder import LabRecorder 
import time
import cv2

participantID:str = "0"
condition:str = "A"
video_path:str = f"\\videos\\{condition}.mp4"
dataFolder:str = f"C:\\Users\\rawex\\Documents\\Studie\\{condition}\\{participantID}\\"

def stop_recording():
    EyeTracker().stop()
    LabRecorder().stop()

def main():

    print("Starting...")
    tobiiThread = threading.Thread(target=EyeTracker().start, args=(dataFolder,))
    tobiiThread.start()
    camThread = threading.Thread(target=CamRecorder().start, args=(dataFolder, 0, 1280, 720, 30))
    camThread.start()
    labrecorderThread = threading.Thread(target=LabRecorder().start, args=(participantID, dataFolder))
    labrecorderThread.start()
    time.sleep(30)
    videoThread = threading.Thread(target=VideoPlayer().start, args=(dataFolder, video_path))
    videoThread.start()

    videoThread.join()
    tobiiThread.join()
    camThread.join()
    labrecorderThread.join()

    #trying to stop Labrecorder at a given time since ctrl+c doesn't work
    while(True):
        if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_recording()
                exit(0)

main()