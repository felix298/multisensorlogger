import os
import tkinter as tk
from tkinter import ttk, filedialog
from configparser import ConfigParser
import asyncio
from bleak import BleakScanner
import psutil
import subprocess
import threading

class Config():
    def __init__(self):
        self.study_path = tk.StringVar()
        self.participant_id = tk.IntVar()
        self.condition = tk.StringVar()
        self.device_address = tk.StringVar()
        self.device_name = tk.StringVar()
        self.stream_name = 'ECG'

        config_object = ConfigParser()
        config_object.read('config.ini')
        self.study_path.set(config_object.get('STUDY', 'study_path'))
        self.participant_id.set(config_object.get('STUDY', 'participant_id'))
        self.condition.set(config_object.get('STUDY', 'condition'))

        self.video_filepath = f"videos/{self.condition.get()}.mp4"
        self.data_folder = os.path.join(self.study_path.get(), f"{self.condition.get()}/{self.participant_id.get()}/")

        if not os.path.exists(self.study_path.get()):
            self.study_path.set("choose study path")

    def get(self):
        return [self.data_folder, self.video_filepath, self.device_address.get(), self.stream_name]
    
    def create_widgets(self, root, column=0, row=0):
        config_frame = ttk.Frame(root)
        config_frame.grid(column=column, row=row)
        _row = 0
        
        polar_stream = threading.Thread(target=self._start_polar_stream ,daemon=True)
        self.polar_stream_label = ttk.Label(config_frame, text="polarstream not running", foreground='orange')
        self.polar_stream_label.grid(column=0, row=_row)
        polar_stream_button = ttk.Button(config_frame, text="start", command=polar_stream.start)
        polar_stream_button.grid(column=1, row=_row)
        _row += 1

        # Bluetooth ECG device
        self.device_label = ttk.Label(config_frame, text='check for device', foreground='orange')
        self.device_label.grid(sticky='W', column=0, row=_row)
        device_reload_button = ttk.Button(config_frame, text='reload', command=self.refresh_device)
        device_reload_button.grid(sticky='W', column=1, row=_row)
        _row += 1

        # Participant ID
        def only_numbers(char):
            return char.isdigit()
        participant_id_label = ttk.Label(config_frame, text="Participant ID")
        validation = config_frame.register(only_numbers)
        self.entry = ttk.Entry(config_frame, textvariable=self.participant_id, width=3, justify='center', validate="key", validatecommand=(validation, '%S'))
        participant_id_label.grid(sticky='W', column=0, row=_row)
        self.entry.grid(sticky='W', column=1, row=_row)
        _row += 1

        # Condition
        condition_label = ttk.Label(config_frame, text="Group")
        condition_choices = ("A", "B")
        condition_option = ttk.OptionMenu(config_frame, self.condition, condition_choices[0], *condition_choices)
        condition_label.grid(sticky='W', column=0, row=_row)
        condition_option.grid(sticky='W', column=1, row=_row)
        _row += 1

        # Study path
        study_path_button = ttk.Button(config_frame, textvariable=self.study_path, command=self.get_study_path)
        study_path_button.grid(sticky='W', column=1, row=_row)
        study_path_label = ttk.Label(config_frame, text="Study Path")
        study_path_label.grid(sticky='W', column=0, row=_row)
        _row += 1

        # Save config button
        update_button = ttk.Button(config_frame, text="Save", command=self.update_config)
        update_button.grid(sticky='W', column=1, row=_row)

    def update_config(self):
        config_object = ConfigParser()
        config_object["STUDY"] = {
            "study_path": self.study_path.get(),
            "participant_id": self.participant_id.get(),
            "condition": self.condition.get()
        }
        with open("config.ini", "w") as conf:
            config_object.write(conf)

        # Update the variables as needed
        self.video_filepath = f"videos/{self.condition.get()}.mp4"
        self.data_folder = os.path.join(self.study_path.get(), f"{self.condition.get()}/{self.participant_id.get()}/")
        os.makedirs(os.path.dirname(self.data_folder), exist_ok=True)

    def get_study_path(self):
        dir = filedialog.askdirectory()
        self.study_path.set(dir)

    def set_device_status(self):
        if (len(self.device_address.get()) > 1):
            self.device_label.configure(text="Device connected", foreground='green')
        else:
            self.device_label.configure(text="Device not found!", foreground='red')
    
    async def discover_devices(self):
        devices = await BleakScanner.discover()
        return devices
    
    def refresh_device(self):
        devices = asyncio.run(self.discover_devices())
        device_names = [device.name for device in devices]
        device_addresses = [device.address for device in devices]
        device_dict = dict(zip(device_names, device_addresses))
        for name in device_dict:
            if name is not None and name.find('Polar') > -1:
                self.device_address.set(device_dict[name])
                self.device_name.set(name)
                self.set_device_status()
    

    def _start_polar_stream(self):
        try:
            psutil.Popen(["python", "polarstream.py", "-a", self.device_address.get(), "-s", self.stream_name])
            self.polar_stream_label.config(text="Running", foreground="green")
        except subprocess.CalledProcessError as e:
            self.polar_stream_label.config(text=f"Failed to run PolarBand stream: {e}", foreground="red")