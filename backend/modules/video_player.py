import vlc
import time
import threading
from modules.config import Config

class VideoPlayer(threading.Thread):
    def __init__(self, config:Config):
        threading.Thread.__init__(self)
        self.config = config
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

    def run(self):
        self.exception = None
        _stop = self.config.get_stop()
        print("Starting Video...")
        logFile = open(self.data_folder + "video_time.txt", 'w')
        
        try:
            self.media_player.play()
        except BaseException as e:
            self.exception = e

        if self.media_player.get_fullscreen() == 0:
            self.exception = BaseException("Fullscreen could not be activated")
            _stop.set()

        while True:
            t = time.time()
            t_ms = int(t * 1000)
            logFile.write(str(t_ms) + " " + str(self.media_player.get_time()) + "\n")
            logFile.flush()
            time.sleep(0.1)
            if _stop.isSet():
                self.media_player.stop()
                print("Stopped Mediaplayer")
                return
            if self.media_player.get_time() > 27700:
                _stop.set()
                self.media_player.stop()
                print("Stopped Mediaplayer")
                return


    def join(self):
        threading.Thread.join(self)

        if self.exception:
            raise self.exception