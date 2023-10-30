import liesl

class EKGReader:
    def __init__(self, condition, participant_id, data_folder):
        self.condition = condition
        self.participant_id = participant_id
        self.data_folder = data_folder
        self.session = None
        self.connect()

    def connect(self):
        try:
            # Establish a session
            self.session = liesl.Session(mainfolder=self.data_folder)
            print("Liesl session established")
        except Exception as e:
            print(f'Failed to establish Liesl session: {e}')

    def start(self):
        if self.session is not None:
            self.session.start_recording()
            print("Starting Liesl session recording...")

    def stop(self):
        if self.session is not None:
            self.session.stop_recording()
            print("Stopped Liesl session recording")
