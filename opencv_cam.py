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

    global vid
    vid = cv2.VideoCapture(0) # choose which connected camera should be captured

    def __init__(self):
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        vid.set(cv2.CAP_PROP_FPS,30)

    def start(self, participantID, dataFolder):
        Path(dataFolder + "\\" + participantID + "\\cam\\").mkdir(parents=True, exist_ok=True)
        while(True):
            
            # Capture the video frame by frame
            ret, frame = vid.read()
            #print("\n".join(" ".join(map(str, x)) for x in (frame)))
            #s.sendall(cv2.imencode('.jpg',frame)[1])
            #dateTimeObj = datetime.now()
            #timestampStr = dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S-%f")
            t = time.time()
            t_ms = int(t * 1000)
            cv2.imwrite(dataFolder + participantID + "\\cam\\" + str(t_ms) + ".jpg", frame)
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
