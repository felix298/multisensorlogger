import vlc
import time
import threading
import tkinter as tk
from tkinter import ttk
from config import Config

class VideoPlayer(ttk.Frame):
    def __init__(self, parent, column=0, row=0):
        super().__init__(parent)
        self.grid(column=column, row=row)
        config = Config().get()
        self.data_folder = config[0]
        self.video_path = config[1]
        self.stop_playback = False

        # creating vlc media player object
        self.setup_player()
        self.canvas = tk.Canvas(self)
        self.canvas.grid(in_=self)

        # Get the window ID of the Canvas and pass it to the VLC player
        win_id = self.canvas.winfo_id()
        self.media_player.set_xwindow(win_id)

        self.label = ttk.Label(self, text="Media player is ready")
        self.label.grid(column=0, row=0)
        start_button = ttk.Button(self, text='start', command=self.start)
        start_button.grid(column=1, row=0)
        stop_button = ttk.Button(self, text='stop', command=self.stop)
        stop_button.grid(column=2, row=0)

    def setup_player(self):
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
        self.label.configure(text="Starting Video...")
        logFile = open(self.data_folder + "video_time.txt", 'w')
        self.media_player.play()
        # while True:
        #     t = time.time()
        #     t_ms = int(t * 1000)
        #     logFile.write(str(t_ms) + " " + str(self.media_player.get_time()) + "\n")
        #     logFile.flush()
        #     time.sleep(0.1)
        #     if self.stop_playback:
        #         break
        
        # logFile.write(str(self.media_player.get_time()))

    def stop(self):
        self.label.configure(text="Stopping VideoPlayer")
        self.media_player.stop()