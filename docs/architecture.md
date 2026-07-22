# System Architecture

## Overview

SafePath AI follows a modular architecture designed to ensure scalability, maintainability, and clear separation of responsibilities. Each module performs a specific task within the real-time navigation pipeline.

The system captures video frames from a webcam, detects surrounding objects using the YOLO26n object detection model, analyzes obstacle positions and danger levels, generates navigation decisions, and delivers real-time voice guidance while simultaneously updating the Flask dashboard.

---

## Architecture Layers

### Input Layer

The input layer captures real-time video frames using the computer camera.

Components:
- Webcam
- OpenCV Video Capture

---

### Processing Layer

The processing layer performs all computer vision and navigation logic.

Modules:
- YOLO26n Object Detection
- Detection Processing
- Navigation Decision Engine
- Voice Message Generation

---

### Output Layer

The output layer presents the processed information to the user.

Outputs:
- Live annotated camera view
- Voice alerts
- Flask Dashboard
- Navigation status

---

## Core Modules

### config.py

Stores configurable system parameters such as confidence threshold, target classes, colors, and dashboard settings.

### detector.py

Loads the YOLO26n model and performs object detection on each captured frame.

### processor.py

Processes detected objects, calculates obstacle positions, determines danger levels, prepares dashboard information, and coordinates the system workflow.

### navigation.py

Generates navigation decisions based on detected obstacle locations.

Example decisions:
- Move Left
- Move Right
- Stop
- Path Clear

### voice.py

Provides asynchronous text-to-speech notifications to the user.

### dashboard.py

Runs the Flask dashboard and displays real-time navigation information.

### safepath.py

Main application entry point that initializes all system modules and controls the execution loop.

---

## Data Flow

Camera

↓

Frame Capture

↓

YOLO26n Detection

↓

Detection Processing

↓

Navigation Decision

↓

Voice Guidance + Dashboard Update

↓

Display Annotated Frame

---

## Design Advantages

- Modular architecture
- Easy maintenance
- Real-time processing
- Scalable design
- Clear separation of responsibilities
- Reusable modules