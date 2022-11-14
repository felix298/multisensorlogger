import threading
from pathlib import Path
from opencv_cam import CamRecorder
from tobii_logger import EyeTracker
from video_player import VideoPlayer
import time

participantID = "0"
video_path="C:\\Users\\whoop\\Downloads\\Deepfake Final bearbeitete Folien.mp4"
dataFolder = "C:\\Users\\whoop\\Desktop\\working-dir\\deepfake\\"

def main():

    print("Starting...")
    Path(dataFolder + "\\" + participantID + "\\").mkdir(parents=True, exist_ok=True)
    camThread = threading.Thread(target=CamRecorder().start, args=(participantID, dataFolder))
    camThread.start()
    tobiiThread = threading.Thread(target=EyeTracker().start, args=(participantID, dataFolder))
    tobiiThread.start()
    videoThread = threading.Thread(target=VideoPlayer().start, args=(participantID, dataFolder, video_path))
    videoThread.start()

    videoThread.join()
    tobiiThread.join()
    camThread.join()

main()