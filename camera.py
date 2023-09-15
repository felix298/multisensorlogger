import cv2
import time

class Camera():
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        print("Camera ready")
        self.out = cv2.VideoWriter(data_folder + "camera_output.mp4", self.fourcc, 30.0, (1280, 720))
        self.stop_playback = False

    def start(self):
        print("Starting Camera")
        timestamps = open(self.data_folder + "camera_timestamps.txt", "w")
        while(True):
            # Capture the video frame by frame
            ret, frame = self.cap.read()
            t = time.time()
            t_ms = int(t * 1000)
            #cv2.imwrite(dataFolder + participantID + "\\" + condition + "\\" + str(cam) + "cam\\" + str(t_ms) + ".jpg", frame)
            self.out.write(frame)
            timestamps.write(str(t_ms) + "\n")
            # Display the resulting frame
            cv2.imshow('frame', frame)

            if self.stop_playback:
                break

        self.out.release()
        self.cap.release()
        timestamps.close()
        cv2.destroyAllWindows()

    def stop(self):
        print("Stopping Camera")
        self.stop_playback = True