# Multi Sensor Study Controller

Welcome to the Multi Sensor Study Controller, a Python-based solution designed to synchronize multiple devices including a Tobii Spark Pro eye tracker, a PolarBand H10, and a Webcamera. These devices are synched with a video.

## What is this for?

I created this Controller for my Bachelor`s thesis lab study. The study consists of 6 parts.

* Introduction
* Putting on and calibrating the sensors
* A first questionnaire
* A video
* A second questionnaire
* End

This controller is used for pairing with the sensors and synchronizing the video playback with the recording of the sensors.

## What is this not for?

* The controller doesn't include the questionnaire or anything that has to do with legal requirements such as a privacy disclosure.
* It can only synchronize a video with a length of 30 seconds.
* It only connects to a PolarBand H10.
* It only connects to a Tobii eye tracker.
* Frontend and Backend must be in the same Network.

## What are the prerequisites?

You need to have the following Equipment

### Hardware

* A Windows PC (macOS could work too however I couldn't test it)
* A Webcam with 1080p resolution and 30-60fps
* A Tobii Pro Spark eye tracker
* A PolarBand H10 sport ECG sensor

### Software

* Python 3.9
* A LabRecorder installation (see [LSL LabRecorder](https://github.com/labstreaminglayer/App-LabRecorder/tree/d52f02a8422b714e810e5f9ef4e24411e4f017cd))
* A Tobii Pro Manager installation (see [Tobii Pro Manager](https://connect.tobii.com/s/etm-downloads?language=en_US))

## Installation

Install all necessary packages with `pip install -r requirements.txt`
After everything is installed properly you can run the script `start_backend.bat` and `start_frontend.bat` by double-clicking on them.
`start_backend.bat` opens a command line window. `start_frontend.bat` opens a browser window. Note that `start_frontend.bat` assumes that Brave Browser is preinstalled. You can also just double-click on `multisensorlogger/frontend/index.html`.

## Settings

When both the frontend and backend are running. The frontend should not show any errors.
Make sure to fill in any missing data in the settings (upper right corner), like the study path or the LabRecorder installation path.

## Acknowledgment

We used [this script](https://github.com/markspan/PolarBand2lsl?tab=readme-ov-file) from markspan to convert the Bluetooth ECG Stream to an LSL-Stream.

## License

This project is licensed under the terms of the GNU General Public License.
