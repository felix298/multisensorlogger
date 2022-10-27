import threading
from pathlib import Path
from opencv_cam import CamRecorder
from tobii_logger import EyeTracker

participantID = "0"
dataFolder = "C:\\Users\\whoop\\Desktop\\working-dir\\deepfake\\"

def main():

    print("Starting...")
    Path(dataFolder + "\\" + participantID + "\\").mkdir(parents=True, exist_ok=True)
    camThread = threading.Thread(target=CamRecorder().start, args=(participantID, dataFolder))
    camThread.start()
    tobiiThread = threading.Thread(target=EyeTracker().start, args=(participantID, dataFolder))
    tobiiThread.start()

    tobiiThread.join()
    camThread.join()

main()