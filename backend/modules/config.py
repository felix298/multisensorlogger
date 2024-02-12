import os
from configparser import ConfigParser
import asyncio
from bleak import BleakScanner
import subprocess
import threading

class Config():
    def __init__(self):
        self.study_path:str
        self.participant_id:int
        self.device_address:str = ""
        self.device_name:str = ""
        self.stream_name = 'ECG'
        self.labrecorder_path:str = ""
        self.tobii_manager_path:str = ""
        self.event = threading.Event()

        config_object = ConfigParser()
        config_object.read('backend/etc/config.ini')
        self.study_path = config_object.get('STUDY', 'study_path')
        self.labrecorder_path = config_object.get('STUDY', 'labrecorder_path')
        self.tobii_manager_path = config_object.get('STUDY', 'tobii_manager_path')
        self.participant_id = config_object.get('STUDY', 'participant_id')

        self._create_video_and_data_folder_path()

        if not os.path.exists(self.study_path):
            print("Study Path does not exist")
            self.study_path = None

        if not os.path.exists(self.labrecorder_path):
            print("Labrecorder Path does not exist")
            self.labrecorder_path = None
        
        if not os.path.exists(self.tobii_manager_path):
            print("Tobii Manager Path does not exist")
            self.tobii_manager_path = None

    def get(self, filename=None):
        ret = {
            "data_folder": self.data_folder,
            "video_path": self.video_filepath,
            "stream_name": self.stream_name,
            "study_path": self.study_path,
            "group": self.group,
            "participant_id": self.participant_id,
            "device_address": self.device_address,
            "device_name": self.device_name,
            "labrecorder_path": self.labrecorder_path,
            "tobii_manager_path": self.tobii_manager_path
        }
        if filename == None:
            if self.study_path is None:
                raise ValueError("Study Path is not set. Please choose a Path in the Settings")
            
            if self.labrecorder_path is None:
                raise ValueError("Labrecorder Path is not set. Please choose a Path in the Settings")
            
            if self.tobii_manager_path is None:
                raise ValueError("Tobii Manager Path is not set. Please choose a Path in the Settings")
            return ret
        return ret[filename]

    def set(self, values):
        self.participant_id = values["participant_id"]
        self.study_path = values["study_path"]
        self.labrecorder_path = values["labrecorder_path"]
        self.tobii_manager_path = values["tobii_manager_path"]
        self._update_config()

    def refresh_device(self):
        devices = asyncio.run(self._discover_devices())
        device_names = [device.name for device in devices]
        device_addresses = [device.address for device in devices]
        device_dict = dict(zip(device_names, device_addresses))
        print(device_dict)
        for name in device_dict:
            if name is not None and name.find('Polar') > -1:
                self.device_address = device_dict[name]
                self.device_name = name
                if (len(self.device_address) > 1):
                    return self.device_name
        raise ConnectionError

    def start_polar_stream(self):
        subprocess.Popen(["python", "backend/etc/polarstream.py", "-a", self.device_address, "-s", self.stream_name], shell=True)

    def start_tobii_manager(self):
        if self.tobii_manager_path is None:
            raise ValueError("Tobii Manager Path is not set. Please choose a Path in the Settings")
        subprocess.Popen('start cmd /k ' + self.tobii_manager_path, shell=True)


    def get_stop(self) -> threading.Event:
        return self.event

    def _update_config(self):
        config_object = ConfigParser()
        config_object["STUDY"] = {
            "study_path": self.study_path,
            "participant_id": self.participant_id,
            "labrecorder_path": self.labrecorder_path,
            "tobii_manager_path": self.tobii_manager_path
        }
        with open("backend/etc/config.ini", "w") as conf:
            config_object.write(conf)
        
        self._create_video_and_data_folder_path()
        os.makedirs(os.path.dirname(self.data_folder), exist_ok=True)
    
    async def _discover_devices(self):
        devices = await BleakScanner.discover()
        return devices
    
    def _create_video_and_data_folder_path(self):
        self.group = 'A' if int(self.participant_id) % 2 == 1 else 'B'
        self.video_filepath = os.path.realpath(f"backend/videos/{self.group}.mp4")
        if self.study_path is not None:
            self.data_folder = os.path.join(self.study_path, f"{self.group}/{self.participant_id}/")