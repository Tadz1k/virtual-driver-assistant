![logo](https://i.imgur.com/P4VToJC.png)

## Description

The main task of the virtual driver assistant is supervision and minimizing the chance of causing an accident due to insufficient attention of the driver. 
The project was created as part of an engineering work at the Polish-Japanese Academy of Information Technology. The project covers the logical part of the presented system. Cameras are simulated with video files.

## Project details

The system detects and marks the selected markings and objects:

* Stop
* Crosswalk
* Speed-limit
* Build-up area (start and end)
* Speed-control
* Traffic lights

In addition, the system analyzes the posture of the person driving the vehicle. If the behavior of the driver is classified as dangerous - then he is warned with a light signal. Passing signs icons will appear on the screen if the driver is driving safely

<p align="center">
![gif-presentation](https://github.com/Tadz1k/virtual-driver-assistant/blob/main/presentation-gif.gif)
</p>

The project is divided into two threads that analyze images from both cameras (or video files) at the same time.

### Technologies

* Traffic sign detection - [YOLOv5](https://github.com/ultralytics/yolov5)
* Speed-limit and driver position classification - [FastAI](https://github.com/fastai/fastai)

### Datasets

* Traffic signs - [Kaggle](https://www.kaggle.com/datasets/valentynsichkar/traffic-signs-dataset-in-yolo-format)
* Additional traffic signs - [Kaggle](https://www.kaggle.com/datasets/kasia12345/polish-traffic-signs-dataset)
* Third pack of traffic signs - Own dataset created basing on youtube videos
* Distraction detection - [Kaggle](https://www.kaggle.com/competitions/state-farm-distracted-driver-detection)

### Tools

Additional, auxiliary scripts have been placed in the repository. They are used, among others, to convert YOLO label files to the appropriate format or other file operations.
