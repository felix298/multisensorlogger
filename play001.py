import cv2
import numpy as np
import os
from datetime import datetime
import time
from pathlib import Path
from ffpyplayer.player import MediaPlayer

video_path="C:\\Users\Violetta\Desktop\LMU\8. Semester\Bachelorarbeit\Study Preparation\Videos DF\DF1.mp4"
dataFolder ="C:\\Users\Violetta\Desktop\DatenErhebungStudie"
participantID = "0"

def PlayVideo(video_path, participantID, dataFolder):
    video=cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    
    Path(dataFolder + "\\" + participantID + "\\videotime\\").mkdir(parents=True, exist_ok=True)
    
    while(True):
        grabbed, frame=video.read()
        audio_frame, val = player.get_frame()
    
        #printcurrenttimestamp
        logFile = open(dataFolder + "\\" + str(participantID) + "\\videotime.txt", 'w')
        t = time.time()
        t_ms = int(t * 1000)
        logFile.write(str(t_ms) + "\n")
    
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame


    video.release()
    cv2.destroyAllWindows()
PlayVideo(video_path, participantID, dataFolder)
