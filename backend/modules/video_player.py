import vlc
import time
import os
import threading
import subprocess
from modules.config import Config

class VideoPlayer(threading.Thread):
    def __init__(self, config:Config):
        threading.Thread.__init__(self)
        self.config = config
        self.data_folder = self.config.get("data_folder")
        self.video_path = self.config.get("video_path")
        self.stop_playback = False

        # creating vlc media player object
        #self._setup_player()

    def _setup_player(self):
        # creating vlc media player object
        self.instance = vlc.Instance()
        self.media = self.instance.media_new(self.video_path)
        self.media_player = self.instance.media_player_new()
        self.media_player.set_media(self.media)

    def run(self):
        time.sleep(5)
        self.exception = None
        _stop = self.config.get_stop()
        print("Starting Video...")
        stamp_path = self.data_folder + "video_time.txt"
        log_file = open(stamp_path, "w" if os.path.isfile(stamp_path) else "x")
        process = subprocess.Popen(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", self.video_path])
        t_control = time.time() * 1000
        while True:
            t_ms = int(time.time() * 1000)
            log_file.write(str(t_ms) + " " + str(t_ms) + "\n")
            log_file.flush()
            if _stop.isSet():
                process.terminate()
                log_file.close()
                print("Stopped Mediaplayer")
                return
            if t_ms - t_control > 29000:
                _stop.set()
                process.terminate()
                log_file.close()
                print("Stopped Mediaplayer")
                return
            time.sleep(1/50)

    def join(self):
        threading.Thread.join(self)

        if self.exception:
            print("Exception in VideoPlayer")
            raise self.exception