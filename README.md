# Lab Recording System

The Lab Recording System is a Python program that allows you to synchronize and record data from LabRecorder, EyeTracker, Camera, and VideoPlayer. It provides a user-friendly interface for starting and stopping the recordings using keyboard shortcuts.

## Prerequisites

Before running the program, make sure you have the following dependencies installed:

- Python 3.x (Python 3.10 or earlier for tobii_research SDK compatibility)
- OpenCV (cv2)
- VLC Media Player
- Tobii Research Python SDK
- PolarBand2lsl
- Keyboard module

You can install the required Python packages by running the following command:

```
pip install opencv-python vlc tobii-research keyboard
```

Please note that Tobii Research Python SDK is only compatible with Python 3.10 or earlier. We recommend to install all dependencies in their own environment with Python 3.10.


### VLC Media Player Installation

To enable video playback, you need to have VLC Media Player installed on your system. You can download it from the official website: [https://www.videolan.org/vlc/index.html](https://www.videolan.org/vlc/index.html)

### EKG Setup

For the LabRecorder to work, you need an lsl stream. We used a PolarBand H10 with Bluetooth connection and PolarBand2lsl for the conversion of the stream. Please follow the manufacturer's instructions to connect and set up the PolarBand H10 device.

### PolarBand2lsl Installation and Setup

To enable data streaming from PolarBand H10 to LabRecorder, you need to install and run PolarBand2lsl. You can find the installation instructions and more details on the GitHub repository: [https://github.com/markspan/PolarBand2lsl](https://github.com/markspan/PolarBand2lsl)

## Tobii Pro Lab Configuration

To use the eye tracking functionality, you need to have Tobii Pro Lab installed and running with the eye tracker properly configured. Make sure the eye tracker is connected to your system and recognized by Tobii Pro Lab.

## Usage

1. Clone the repository to your local machine.

2. Open a terminal or command prompt and navigate to the project directory.

3. Modify the `main.py` file to set the following variables according to your requirements:
   - `participant_id`: The ID of the participant.
   - `condition`: The condition or group of the participant.
   - `study_path`: The base folder where data will be saved.
   - `video_filepath`: The path to the video file you want to play during the recording.

4. Modify the `camera.py` file to set the width height and fps of the camera:
   - `width`: the width of the camera in px
   - `height`: the height of the camera in px
   - `fps`: the frames per second of the camera

5. Run the following command to start the Lab Recording System:

   ```
   python main.py
   ```

6. The program will display a message to press the [Space] key to start the recording.

7. Press the [Space] key to start the recordings. The LabRecorder, EyeTracker, Camera, and VideoPlayer will start recording data simultaneously.

8. Press the [S] key to stop the recordings. All data recording will be stopped, and the program will save the recorded data in the specified output folders.

9. Press the [Q] key to exit the program.

## Output

The recorded data will be saved in the following folders:

- LabRecorder data: `study_path/condition/participant_id/labrecorder.txt`
- EyeTracker data: `study_path/condition/participant_id/tobii.txt`
- Camera video: `study_path/condition/participant_id/camera_output.avi`

## Troubleshooting

- If you encounter any issues with the video playback, make sure you have VLC Media Player installed on your system and the `vlc` executable is in your system's PATH.

- If the program is not detecting keyboard inputs, try running the program with administrator privileges.

- If you face any issues with the Tobii Research Python SDK, make sure you have installed the compatible version for your Python version and that the eye tracker is properly connected to your system and configured in Tobii Pro Lab.

- If you encounter any problems with the PolarBandEKG and PolarBand2lsl setup, refer to the documentation and troubleshooting guide provided by the manufacturer and on the GitHub repository.

## Contributing

Contributions to the Lab Recording System are welcome. If you find any bugs or want to suggest enhancements, please open an issue on the project's GitHub repository: [https://github.com/felix298/multisensorlogger](https://github.com/felix298/multisensorlogger)

## Acknowledgements

- The Lab Recording System utilizes the following libraries and components:
  - OpenCV (cv2) for video processing
  - VLC Media Player for video playback
  - Tobii Research Python SDK for eye tracking
  - PolarBandEKG for heart rate monitoring
  - PolarBand2lsl for data streaming from PolarBandEKG to LabRecorder
  - Keyboard module for handling keyboard inputs

We would like to acknowledge the authors and contributors of these libraries and components for their valuable work.