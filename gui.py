import tkinter as tk
from tkinter import ttk
from ecg import ECG
from config import Config
from camera import Camera
from video_player import VideoPlayer
from tobii_logger import EyeTracker

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study")
        self.geometry('800x600')
        self.columnconfigure(0)
        self.rowconfigure(0, pad=16)
        self.rowconfigure(1, pad=16)
        self.rowconfigure(2, pad=16)
        self.grid()
        _row = 0
        cfg = Config()
        cfg.create_widgets(self, column=0, row=_row)
        _row += 1

        self.camera = Camera(self, column=0, row=_row)
        _row += 1
        self.ecg = ECG(self, column=0, row=_row)
        _row += 1
        self.tobii = EyeTracker(self, column=0, row=_row)
        _row += 1
        self.video = VideoPlayer(self, column=0, row=_row)
        _row += 1
        button = ttk.Button(self, text="Run all", command=self.start)
        button.grid(column=0, row=_row)

        self.mainloop()

    def start(self):
        self.camera.start()
        self.video.start()
        self.ecg.start()
        self.tobii.start()

App()
