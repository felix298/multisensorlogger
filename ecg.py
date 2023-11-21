import tkinter as tk
from tkinter import ttk
from config import Config
import liesl
import time


class ECG(ttk.Frame):
    def __init__(self, parent:tk.Tk, column=0, row=0):
        super().__init__(parent)
        self.grid(column=column, row=row)
        config = Config().get()
        self.data_folder = config[0]
        self.device_address = config[2]
        self.stream_name = config[3]

        self.label = ttk.Label(self, text="ECG")
        self.label.grid(column=0, row=0)
        connect_button = ttk.Button(self, text="Start", command=self.connect)
        connect_button.grid(column=1, row=0)
        
        start_resting_button = ttk.Button(self, text="Measure Resting Heartrate", command=self._rec_resting)
        start_resting_button.grid(column=2, row=0)
        
        stop_resting_button = ttk.Button(self, text="Stop measure", command=lambda: self.stop())
        stop_resting_button.grid(column=3, row=0)

        self.err_label = ttk.Label(self, text="", foreground="red")
        self.err_label.grid(column=2, row=0)

    def _rec_resting(self):
        info = liesl.open_streaminfo(name=self.stream_name)
        session = liesl.Session(prefix="", mainfolder=self.data_folder, streamargs=[{'name': info.name(), 'hostname': info.hostname(), 'type': info.type()}])
        with session('resting_heartrate') as ses:
            ses.start_recording()
            time.sleep(60)
            ses.stop_recording()

    def start(self):
        info = liesl.open_streaminfo(name=self.stream_name)
        self.session = liesl.Session(prefix="", mainfolder=self.data_folder, streamargs=[{'name': info.name(), 'hostname': info.hostname(), 'type': info.type()}])
        self.session.start_recording("heartrate")
    
    def stop(self):
        if self.session is not None:
            self.session.stop_recording()
