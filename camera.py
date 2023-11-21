import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import cv2
import time
from config import Config

class Camera(ttk.Frame):
    def __init__(self, parent:tk.Tk, column=0, row=0):
        super().__init__(parent)
        self.grid(column=column, row=row)
        self.data_folder = Config().get()[0]
        self.width = 1920
        self.height = 1080
        self.fps = 60.0

        button = ttk.Button(self, text='test Camera', command=self.start)
        button.grid(column=0, row=1)
        stop_button = ttk.Button(self, text='stop', command=self.stop)
        stop_button.grid(column=1, row=1)
        self.label = ttk.Label(self, text="Camera ready")
        self.label.grid(column=0, row=0)

        


    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.fourcc = cv2.VideoWriter.fourcc(*'avc1')
        self.out = cv2.VideoWriter(self.data_folder + "camera_output.mp4", self.fourcc, self.fps, (self.width, self.height))
        self.stop_playback = False
        self.thread = threading.Thread(target=self._capture_video, daemon=True)
        self.thread.start()

    def _capture_video(self):
        self.label.config(text="Starting Camera")
        timestamps = open(self.data_folder + "camera_timestamps.txt", "w")
        while(True):
            # Capture the video frame by frame
            ret, frame = self.cap.read()
            t_ms = int(time.time() * 1000)
            if ret:
                self.out.write(frame)
                timestamps.write(str(t_ms) + "\n")
                # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # Convert the image from BGR to RGBA
                # image = Image.fromarray(image)  # Create an Image object from the array
                # image = ImageTk.PhotoImage(image)  # Convert the Image object to a Tkinter-compatible PhotoImage object
                # self.label.config(image=image)  # Update the label with the new image
                # self.label.image = image  # Keep a reference to the image to prevent it from being garbage collected

            if self.stop_playback:
                break
            
        self.label.config(image=None)
        self.out.release()
        self.cap.release()
        timestamps.close()
        self.label.config(text="Camera stopped")

    def stop(self):
        self.label.config(text="Stopping Camera")
        self.stop_playback = True