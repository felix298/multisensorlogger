from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from modules.config import Config
import os
import threading
from modules.ecg import ECG
from modules.camera import Camera
from modules.video_player import VideoPlayer
from modules.tobii_logger import EyeTracker

app = Flask(__name__)
CORS(app)

config = Config()
ecg = ECG()
cam = Camera()
tobii = EyeTracker()
player = VideoPlayer()

@app.get("/config")
def get_config():
    try:
        return jsonify(config.get())
    except Exception as e:
        abort(500, description=str(e))

@app.post("/config")
def set_config():
    data = request.get_json()
    try:
        if not os.path.exists(data["study_path"]):
            abort(400, description="Study Path is not a valid path. Please use absolute paths")
        config.set(data)
        return jsonify(config.get())
    except Exception as e:
        abort(500, description=str(e))

@app.get("/bluetooth")
def bluetooth():
    try:
        return jsonify(config.refresh_device())
    except ConnectionError:
        abort(500, description="PolarBand not found")
    except Exception as e:
        abort(500, description=str(e))

@app.get("/polarband")
def polarband():
    try:
        stream = threading.Thread(target=config.start_polar_stream())
        stream.start()
        return jsonify({}), 200
    except Exception as e:
        abort(500, description=str(e))

@app.get("/tobii")
def tobii_manager():
    try:
        stream = threading.Thread(target=config.start_tobii())
        stream.start()
        return jsonify({}), 200
    except Exception as e:
        abort(500, description=str(e))

@app.get("/camera")
def camera():
    try:
        if cam.test():
            return jsonify({}), 200
        else:
            abort(500, description="Camera test failed.")
    except Exception as e:
        abort(500, description=str(e))

@app.get("/heartrate")
def heartrate():
    try:
        ecg.rec_resting()
    except Exception as e:
        abort(500, description=str(e))
    finally:
        return jsonify({}), 200
        
@app.get("/start")
def start():
    try:
        ecg.start()
        tobii.start()
        cam.start()
        player.start()
        return jsonify({}), 200
    except Exception as e:
        abort(500, description=str(e))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)