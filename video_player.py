""" import time
import vlc

class VideoPlayer():

    def __init__(self):
        print("video started")
    
    def start(self, dataFolder, video_path):        
        logFile = open(dataFolder + "videotime.txt", 'w')
        
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
        lastMediaTimestamp = media_player.get_time()
        lastTime = time.time()
        while(True):
            t = time.time()
            t_ms = int(t * 1000)
            logFile.write(str(t_ms) + " " + str(media_player.get_time()) + "\n")
            logFile.flush()
            time.sleep(0.1)
            if time.time() - lastTime > 1:
                if lastMediaTimestamp == media_player.get_time():
                    media_player.stop()
                    break
                else:
                    lastMediaTimestamp = media_player.get_time()
                lastTime = time.time()
         """
import vlc
import time

class VideoPlayer:
    def __init__(self, video_filepath, data_folder):
        self.data_folder = data_folder
        self.stop_playback = False
         # creating vlc media player object
        self.media_player = vlc.MediaPlayer()
        # media object
        media = vlc.Media(video_filepath)
        # setting media to the media player
        self.media_player.set_media(media)
        # toggling full screen
        self.media_player.toggle_fullscreen()
        print("Media player is ready")

    def start(self):
        print("Starting Video...")
        logFile = open(self.data_folder + "videotime.txt", 'w')
        self.media_player.play()
        lastMediaTimestamp = self.media_player.get_time()
        lastTime = time.time()
        while(True):
            t = time.time()
            t_ms = int(t * 1000)
            logFile.write(str(t_ms) + " " + str(self.media_player.get_time()) + "\n")
            logFile.flush()
            time.sleep(0.1)
            if self.stop_playback:
                break
        self.media_player.stop()
            

    def stop(self):
        print("Stopping VideoPlayer")
        self.stop_playback = True