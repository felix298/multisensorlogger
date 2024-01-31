import os
import time
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from modules.config import Config
from modules.ecg import ECG
from modules.camera import Camera
from modules.video_player import VideoPlayer
from modules.eyetracker import EyeTracker

app = Flask(__name__)
CORS(app)

config = Config()
ecg = ECG(config)
cam = Camera(config)
player = VideoPlayer(config)
tobii = EyeTracker(config)
device_connected = bool(False)

@app.get("/config")
def get_config():
    try:
        return jsonify(config.get())
    except BaseException as e:
        abort(500, description=str(e))

@app.post("/config")
def set_config():
    data = request.get_json()
    try:
        if not os.path.exists(data["study_path"]):
            abort(400, description="Study Path is not a valid path. Please use absolute paths")
        if not os.path.exists(data["labrecorder_path"]):
            abort(400, description="Path to Labrecorder_CLI.exe is not valid. Please use absolute paths")
        if not os.path.exists(data["tobii_manager_path"]):
            abort(400, description="Path to Tobii Manager.exe is not valid. Please use absolute paths")
        config.set(data)
        return jsonify(config.get())
    except BaseException as e:
        abort(500, description=str(e))

@app.get("/bluetooth")
def bluetooth():
    global device_connected
    try: 
        device_connected = True
        return jsonify(config.refresh_device())
    except ConnectionError:
        device_connected = False
        abort(500, description="PolarBand not found. Make sure it is turned on")
    except BaseException as e:
        device_connected = False
        abort(500, description=str(e))
       

@app.get("/polarband")
def polarband():
    try:
        if not device_connected: raise ConnectionError("Polarband not connected")
        config.start_polar_stream()
        time.sleep(4)
        ecg.set_stream_info()
    except ConnectionError as e:
        abort(500, description=str(e))
    except BaseException as e:
        abort(500, description=str(e))
    else:
        return jsonify({}), 200

@app.get("/tobii")
def tobii_manager():
    try:
        config.start_tobii_manager()
    except BaseException as e:
        abort(500, description=str(e))
    else:
        return jsonify({}), 200

@app.get("/camera")
def camera():
    try:
        cam.test()
    except BaseException as e:
        abort(500, description=str(e))
    else:
        return jsonify({}), 200

@app.get("/heartrate")
def heartrate():
    try:
        ecg.rec_reference()
    except BaseException as e:
        abort(500, description=str(e))
    else:
        return jsonify({}), 200
        
@app.get("/start")
def start():
    stamp_path = config.get("data_folder") + "reference_time.txt"
    log_file = open(stamp_path, "w" if os.path.isfile(stamp_path) else "x")
    log_file.write(str(int(time.time() * 1000)))
    log_file.flush()
    stop = config.get_stop()
    try:
        ecg.start()
        cam.start()
        tobii.start()
        player.start()
        ecg.join()
        cam.join()
        tobii.join()
        player.join()

    except ConnectionError as e:
        stop.set()
        abort(500, description=str(e))
    except BaseException as e:
        stop.set()
        abort(500, description=str(e))
    else:
        return jsonify({}), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)