import socket
from datetime import datetime

class LabRecorder:
    def __init__(self, participant_id, data_folder):
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

    def start(self):
        lr_config:str = "filename {root:" + self.data_folder + "} {" + "template:&m_%n_%p.xdf" + "} {participant:" + str(self.participant_id) + "} {" + "modality:eeg" + "}\n"

        try:
            # Try to open the file and write the timestamp
            logFile = open(self.data_folder + "labrecorder.txt", 'w')
        except IOError as e:
            print(f'IOError: {e}')   

        # First ensure that the connection was successfully made
        if self.conn is not None:
            try:
                # Get the current date and time
                now = datetime.now()

                # Convert to timestamp
                timestamp = int(datetime.timestamp(now))
                logFile.write(str(timestamp))
                self.conn.sendall(b"select all\n")
                self.conn.sendall(lr_config.encode())
                self.conn.sendall(b"start\n")
                print("Streaming EEG-Data...")
            except socket.error as e:
                print(f'Sending commands to Labrecorder failed with error: {e}')

    def stop(self):
        print(self.conn)
        if self.conn is not None:
            self.conn.sendall(b"select all\n")
            self.conn.sendall(b"stop\n")
            self.conn.close()
            self.conn = None
            print("LabRecorder stopped")