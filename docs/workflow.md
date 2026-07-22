# System Workflow

## Overview

The SafePath AI workflow processes every captured frame through a sequence of well-defined stages to provide accurate real-time navigation assistance.

---

## Workflow Steps

### Step 1 – System Initialization

The application loads the YOLO26n model, initializes the camera, starts the Flask dashboard, and prepares the text-to-speech engine.

---

### Step 2 – Capture Frame

A frame is captured continuously from the webcam using OpenCV.

---

### Step 3 – Object Detection

The captured frame is analyzed by the YOLO26n model to identify surrounding objects.

---

### Step 4 – Detection Processing

Detected objects are filtered and analyzed based on confidence score, object class, and screen position.

---

### Step 5 – Navigation Decision

The navigation module determines the safest movement direction according to obstacle locations and danger levels.

Possible outputs include:

- Move Left
- Move Right
- Stop
- Path Clear

---

### Step 6 – Voice Guidance

The generated navigation instruction is converted into speech using the text-to-speech engine.

---

### Step 7 – Dashboard Update

The dashboard is updated with:

- Detected objects
- Navigation status
- Obstacle direction
- Danger level
- System statistics

---

### Step 8 – Display Output

The processed frame is displayed with bounding boxes, labels, and navigation information.

---

### Step 9 – Repeat

The workflow repeats continuously until the application is terminated.