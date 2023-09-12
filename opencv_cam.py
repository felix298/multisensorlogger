import cv2
from datetime import datetime
import time
from pathlib import Path

#IP = "127.0.0.1"
#PORT = 65002
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((IP, PORT))

#s.sendall(bytes("thermal-cam\n", "utf-8"))
#s.sendall(bytes("txt\n", "utf-8")) # file extension type

#sessionId = uuid.uuid4()

class CamRecorder():

    def __init__(self):
        print("cam starting")

    def start(self, dataFolder, cam, width, height, fps):
        Path(dataFolder).mkdir(parents=True, exist_ok=True)
        vid = cv2.VideoCapture(cam)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        vid.set(cv2.CAP_PROP_FPS, fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videoWriter = cv2.VideoWriter(dataFolder + str(cam) + "cam.mp4", fourcc, 30.0, (1280,720))
        timestamps = open(dataFolder + "camTimestamps.txt", "w")
    
        while(True):
            
            # Capture the video frame by frame
            ret, frame = vid.read()
            #print("\n".join(" ".join(map(str, x)) for x in (frame)))
            #s.sendall(cv2.imencode('.jpg',frame)[1])
            #dateTimeObj = datetime.now()
            #timestampStr = dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S-%f")
            t = time.time()
            t_ms = int(t * 1000)
            #cv2.imwrite(dataFolder + participantID + "\\" + condition + "\\" + str(cam) + "cam\\" + str(t_ms) + ".jpg", frame)
            videoWriter.write(frame)
            timestamps.write(str(t_ms) + "\n")
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # After the loop release the cap object
        vid.release()
        videoWriter.release()
        timestamps.close()
        # Destroy all the windows
        cv2.destroyAllWindows()
