import time
import threading
import liesl
from liesl.files.labrecorder.cli_wrapper import LabRecorderCLI
from modules.config import Config

class ECG():
    def __init__(self):
        config = Config()
        self.data_folder = config.get("data_folder")
        self.stream_name = config.get("stream_name")

        self.labrecorder = LabRecorderCLI("backend/etc/LabRecorder/LabRecorderCLI.app/Contents/MacOS/LabRecorderCLI")

    def rec_resting(self):
        resting = threading.Thread(target=self._rec_resting)
        resting.start()

    def _rec_resting(self):
        info = liesl.open_streaminfo(name=self.stream_name)
        file_path = self.data_folder + 'resting_heartrate.xdf'
        self.labrecorder.start_recording(file_path, streamargs=[{'name': info.name(), 'hostname': info.hostname(), 'type': info.type()}])
        time.sleep(60)
        self.labrecorder.stop_recording()

    def start(self):
        resting = threading.Thread(target=self._start)
        resting.start()

    def _start(self):
        file_path = self.data_folder + 'heartrate.xdf'
        info = liesl.open_streaminfo(name=self.stream_name)
        self.labrecorder.start_recording(file_path, streamargs=[{'name': info.name(), 'hostname': info.hostname(), 'type': info.type()}])
    
    def stop(self):
        self.labrecorder.stop_recording()
