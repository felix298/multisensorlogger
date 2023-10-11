import socket
from datetime import datetime

class LabRecorder:
    def __init__(self, condition, participant_id, data_folder):
        self.condition = condition
        self.participant_id = participant_id
        self.data_folder = data_folder
        self.connect()

    def connect(self):
        try:
            # Try to establish a connection
            self.conn = socket.create_connection(("localhost", 22345))
            print("Connection to LabRecorder established")
        except socket.error as e:
            print(f'Connection to LabRecorder failed with error: {e}')
            self.conn = None

        lr_config:str = "filename {root:" + self.data_folder + "} {" + "template:ecg_" + str(self.condition) +  "_" + str(self.participant_id) + ".xdf}\n"

        # First ensure that the connection was successfully made
        if self.conn is not None:
            try:
                self.conn.sendall(b"select all\n")
                self.conn.sendall(lr_config.encode())
                self.conn.sendall(b"start\n")
                print("Streaming ECG-Data...")
            except socket.error as e:
                print(f'Sending commands to Labrecorder failed with error: {e}')

    def start(self):
        self.setmarker('start video')

    def setmarker(self, marker):
        try:
            # Try to open the file and write the timestamp
            with open(self.data_folder + "labrecorder.txt", 'a+') as log_file:
                now = datetime.now()
                timestamp = int(datetime.timestamp(now))
                log_file.write(f"{marker}: {str(timestamp)}\n")
                print(marker + ' was logged')
        except IOError as e:
            print(f"Couldn't write to file: {e}")  

    def stop(self):
        print(self.conn)
        if self.conn is not None:
            self.conn.sendall(b"select all\n")
            self.conn.sendall(b"stop\n")
            self.conn.close()
            self.conn = None
            self.setmarker('stop video')
            print("LabRecorder stopped")