# Installation Guide

## Prerequisites

Before running the project, make sure the following software is installed:

- Python 3.10 or later
- Git
- Webcam
- Internet connection (for downloading dependencies)

---

## Clone the Repository

```bash
git clone https://github.com/your-username/SMARTCANEAI.git
cd SMARTCANEAI
```

---

## Create a Virtual Environment

```bash
python -m venv venv
```

---

## Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start the Flask Dashboard

```bash
python dashboard.py
```

---

## Run the Navigation System

```bash
python safepath.py
```

---

## Expected Result

Once both applications are running:

- The webcam opens automatically.
- The YOLO26n model starts detecting objects.
- The dashboard displays real-time navigation information.
- Voice alerts are generated when obstacles are detected.