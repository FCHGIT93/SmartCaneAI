# Project Structure

## Overview

The SafePath AI project is organized into multiple folders and modules to improve readability, maintainability, and scalability.

---

## Directory Structure

```text
SMARTCANEAI/
│
├── assets/
├── docs/
├── models/
├── safepath_core/
│   ├── __init__.py
│   ├── config.py
│   ├── detector.py
│   ├── navigation.py
│   ├── processor.py
│   └── voice.py
│
├── static/
├── templates/
│
├── dashboard.py
├── safepath.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Folder Description

### assets/

Contains images used in the project documentation, including screenshots, architecture diagrams, workflow diagrams, and branding assets.

### docs/

Contains detailed technical documentation.

### models/

Stores the trained YOLO26n model used for object detection.

### safepath_core/

Contains the core logic of the SafePath AI system.

### static/

Stores CSS, JavaScript, and other static resources used by the Flask dashboard.

### templates/

Contains HTML templates for the Flask dashboard.

---

## File Description

### config.py

Stores configurable system parameters.

### detector.py

Loads the YOLO26n model and performs object detection.

### navigation.py

Analyzes obstacle positions and generates navigation decisions.

### processor.py

Processes detection results, updates the dashboard, prepares annotations, and coordinates the system workflow.

### voice.py

Provides text-to-speech functionality.

### dashboard.py

Runs the Flask dashboard.

### safepath.py

Main application entry point.

### requirements.txt

Lists all required Python packages.

### README.md

Provides the main project documentation.

### .gitignore

Specifies files and folders ignored by Git.