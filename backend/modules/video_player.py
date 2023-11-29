import vlc
import time
import threading
from modules.config import Config

class VideoPlayer():
    def __init__(self):

        config = Config()
        self.data_folder = config.get("data_folder")
        self.video_path = config.get("video_path")
        self.stop_playback = False

        # creating vlc media player object
        self._setup_player()

    def _setup_player(self):
        # creating vlc media player object
        self.media_player = vlc.MediaPlayer()
        
        # media object
        media = vlc.Media(self.video_path)
        
        # setting media to the media player
        self.media_player.set_media(media)


    def start(self):
        self.thread = threading.Thread(target=self._play_video, daemon=True)
        self.thread.start()

    def _play_video(self):
        print("Starting Video...")
        logFile = open(self.data_folder + "video_time.txt", 'w')
        self.media_player.play()
        while True:
            t = time.time()
            t_ms = int(t * 1000)
            logFile.write(str(t_ms) + " " + str(self.media_player.get_time()) + "\n")
            logFile.flush()
            time.sleep(0.1)
            if self.stop_playback:
                break
        
        # logFile.write(str(self.media_player.get_time()))

    def stop(self):
        print("Stopping VideoPlayer")
        self.media_player.stop()