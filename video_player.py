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