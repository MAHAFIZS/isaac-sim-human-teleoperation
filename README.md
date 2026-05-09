# Isaac Sim Human Teleoperation

Real-time human arm teleoperation system using webcam-based pose estimation and NVIDIA Isaac Sim.

## Overview

This project captures human arm motion from a webcam using MediaPipe pose estimation and maps it to a Franka Panda robot in NVIDIA Isaac Sim through a custom UDP-based motion retargeting pipeline.

The system demonstrates:

* real-time human pose tracking,
* multi-joint robot teleoperation,
* motion retargeting,
* simulation-based robot control.

## Features

* Webcam-based human pose estimation
* Real-time UDP communication
* Multi-joint Franka Panda control
* Robot teleoperation in Isaac Sim
* Motion retargeting pipeline
* Humanoid robotics research prototype

## Tech Stack

* Python
* MediaPipe
* OpenCV
* NVIDIA Isaac Sim
* UDP Networking

## System Pipeline

Human Motion → MediaPipe Pose Estimation → UDP Communication → Isaac Sim → Franka Panda Robot Motion

## Demo

A demo video is included in the `demo/` folder.

## Future Work

* End-effector task-space control
* Humanoid robot teleoperation
* IK-based motion retargeting
* VR/MoCap integration
* Imitation learning and RL workflows
