import time
import threading
import liesl
from liesl.files.labrecorder.cli_wrapper import LabRecorderCLI
from modules.config import Config

class ECG(threading.Thread):
    def __init__(self, config:Config):
        threading.Thread.__init__(self)
        self.config = config
        self.data_folder = config.get("data_folder")
        self.stream_name = config.get("stream_name")
        self.info = None
        self.labrecorder = LabRecorderCLI("backend/etc/LabRecorder/LabRecorderCLI.app/Contents/MacOS/LabRecorderCLI")

    def set_stream_info(self):
        self.info = liesl.open_streaminfo(name=self.stream_name)
        try:
            self.streamargs = [{'name': self.info.name(), 'hostname': self.info.hostname(), 'type': self.info.type()}]
        except:
            raise ValueError("Polarband not connected")

    def rec_resting(self):
        if self.info is None:
            raise ValueError("Polarband not connected")

        file_path = self.data_folder + 'resting_heartrate.xdf' 
        self.labrecorder.start_recording(file_path, streamargs=self.streamargs)
        time.sleep(60)
        self.labrecorder.stop_recording()

    def run(self):
        self.exception = None
        _stop = self.config.get_stop()
        if self.info is None:
            self.exception = ConnectionError("Polarband not connected")
            return
        
        try:
            file_path = self.data_folder + 'heartrate.xdf'
            self.labrecorder.start_recording(file_path, streamargs=self.streamargs)
            _stop.wait()
            self.labrecorder.stop_recording()
        except BaseException as e:
            self.exception = e

    def join(self):
        threading.Thread.join(self)
        
        if self.exception:
            raise self.exception