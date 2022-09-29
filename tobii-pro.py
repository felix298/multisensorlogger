import tobii_research as tr
import time
import json
import socket

IP = "127.0.0.1"
PORT = 65002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)
s.sendall(bytes("eye-tracker\n", "utf-8"))
#s.sendall(bytes("txt\n", "utf-8")) # file extension type
s.sendall(bytes("Model: ", "utf-8") + bytes(my_eyetracker.model + "\n", "utf-8"))
s.sendall(bytes("Serial Number: ", "utf-8") + bytes(my_eyetracker.serial_number + "\n", "utf-8"))

def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    msg = "{gaze_left_eye};{gaze_right_eye}".format(gaze_left_eye=gaze_data['left_gaze_point_on_display_area'], gaze_right_eye=gaze_data['right_gaze_point_on_display_area'])
    #sock.sendto(bytes(json.dumps(gaze_data, indent = 4), "utf-8"), (UDP_IP, UDP_PORT))
    t = time.time()
    t_ms = int(t * 1000)
    print(t_ms)
    print(gaze_data)
    s.sendall(bytes(json.dumps(gaze_data) + "\n", "utf-8"))
    # parsed = json.loads(gaze_data)
    # print(json.dumps(parsed, indent=2, sort_keys=True))
    # print(json.dumps(gaze_data, indent = 4))
    # print("{gaze_data}")
    # sock.sendto("{gaze_left_eye};{gaze_right_eye}".format(
    #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
    #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']), (UDP_IP, UDP_PORT))

my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
  
time.sleep(30) 

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)