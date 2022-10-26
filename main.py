from opencv_cam import CamRecorder


def main():

    participantID = '0'

    print("Starting...")
    CamRecorder().start(participantID)


main()