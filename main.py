import threading
import keyboard
import os
from video_player import VideoPlayer
from camera import Camera
from labrecorder import LabRecorder
from tobii_logger import EyeTracker



def main():
    participant_id:str = "1"
    condition:str = "B"
    study_path = os.getcwd() + "/../Studie"
    print(study_path)
    video_filepath = f"videos/{condition}.mp4"
    data_folder = os.path.join(study_path, f"{condition}/{participant_id}/")
    os.makedirs(os.path.dirname(data_folder), exist_ok=True)

    recorder = LabRecorder(condition, participant_id, data_folder)
    tracker = EyeTracker(data_folder)
    cam = Camera(data_folder)
    player = VideoPlayer(video_filepath, data_folder)

    def start_tasks():
        threading.Thread(target=recorder.start).start()
        threading.Thread(target=tracker.start).start()
        threading.Thread(target=cam.start).start()
        threading.Thread(target=player.start).start()

    def stop_tasks():
        recorder.stop()
        tracker.stop()
        cam.stop()
        player.stop()
    
    def end():
        os._exit(0)

    print("press [Space] to start...")

    keyboard.add_hotkey('space', start_tasks)
    keyboard.add_hotkey('s', stop_tasks)
    keyboard.add_hotkey('c', lambda: recorder.setmarker('start calibration'))
    keyboard.add_hotkey('shift + c', lambda: recorder.setmarker('end calibration'))
    keyboard.add_hotkey('q', end)

    keyboard.wait()

main()
