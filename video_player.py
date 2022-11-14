import cv2
import os
import numpy as np
import time
from ffpyplayer.player import MediaPlayer
import vlc

class VideoPlayer():

    def __init__(self):
        print("video started")
    
    def start(self, participantID, condition, dataFolder, video_path):        
        logFile = open(dataFolder + "\\" + str(participantID) + "\\" + str(condition) + "\\videotime.txt", 'w')
        
        # creating vlc media player object
        media_player = vlc.MediaPlayer()
        # media object
        media = vlc.Media(video_path)
        # setting media to the media player
        media_player.set_media(media)
        # toggling full screen
        media_player.toggle_fullscreen()
        # start playing video
        media_player.play()
        # wait so the video can be played for 5 seconds
        # irrespective for length of video
        while(True):
            t = time.time()
            t_ms = int(t * 1000)
            logFile.write(str(t_ms) + " " + str(media_player.get_time()) + "\n")
            logFile.flush()
            time.sleep(0.1)
