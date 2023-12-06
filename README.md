# Multi Sensor Study Controller

Welcome to the Multi Sensor Study Controller, a comprehensive Python-based solution designed to synchronize multiple devices including a Tobii eyetracker, a PolarBand H10, and a camera with a video.

## Project Overview

This project was born out of the necessity to create a usable software for my Bachelor's thesis. The main goal was to develop a system that could seamlessly integrate and synchronize data from multiple sensors, providing a unified platform for data collection and analysis.

## Features

Tobii Eyetracker Integration: The software can connect and synchronize with Tobii eyetracker, providing real-time eye tracking data. The EyeTracker class in the tobii_logger.py module handles this functionality.
PolarBand H10 Integration: The software is capable of receiving and processing heart rate data from the PolarBand H10. The ECG class in the ecg.py module is responsible for this.
Camera and Video Synchronization: The software can synchronize a camera with a video, allowing for simultaneous recording and playback. The Camera class in the camera.py module and the VideoPlayer class in the video_player.py module handle these functionalities.
Web Frontend: The software provides a web frontend for user interaction, built using Flask. The app.py module contains the Flask application and the routes for the web frontend.
Getting Started
To get started with the Multi Sensor Study Controller, you'll need to have Python installed on your machine. Once you've done that, you can clone this repository and install the necessary dependencies.

## Usage

The main entry point of the application is the app.py module. Run this module to start the Flask application. The application runs on 0.0.0.0 and port 5555.

The application provides several endpoints for interacting with the different components of the system. For example, the /config endpoint allows you to get and set the configuration, the /bluetooth endpoint refreshes the device list, and the /start endpoint starts the data collection process.

## License

This project is licensed under the terms of the [INSERT LICENSE HERE]. Feel free to reuse any part of the codebase, as long as it adheres to the license agreement.

## Acknowledgements

I would like to express my gratitude to everyone who contributed to this project and made it a success. Your contributions have been invaluable.

Please replace "[INSERT LICENSE HERE]" with the actual license you're using for your project. If you have any specific instructions for installation or usage, or if there are any other details you'd like to include, let me know!