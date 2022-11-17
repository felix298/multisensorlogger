import os
import vlc
import time
import socket

IP = "192.168.6.68"
PORT = 9000

video_folder = "D:\\WICHTIGE KOPIE\\WRITE Untersuchungen Paper\\ZZZ System Aufsetzen Eyetracking Dual PC\\ArbeItsordner Stimuli\\"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

files = []
for (dirpath, dirnames, filenames) in os.walk(video_folder):
    files.extend(filenames)
    break

def start(video_path):
    # creating vlc media player object
    media_player = vlc.MediaPlayer()
    # media object
    media = vlc.Media(video_path)
    # setting media to the media player
    media_player.set_media(media)
    # toggling full screen
    media_player.toggle_fullscreen()
    # start playing video
    media_player.play()
    # wait so the video can be played for 5 seconds
    # irrespective for length of video
    mediaTimestamp = media_player.get_time()
    time.sleep(2)
    while True:
        if mediaTimestamp != media_player.get_time():
            mediaTimestamp = media_player.get_time()
            time.sleep(2)
        else:
            break
    media_player.stop()

for video in files:
    s.sendall(bytes(video, "ASCII"))
    #start(video_folder + video)
    start("C:\\Users\\whoop\\Desktop\\working-dir\\data_src.mp4")
    s.sendall(bytes(video, "ASCII"))
    time.sleep(5)
