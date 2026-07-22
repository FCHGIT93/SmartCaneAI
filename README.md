# 🦯 SafePath AI – Smart Navigation System for Visually Impaired People

An AI-powered smart navigation assistant that helps visually impaired individuals detect surrounding obstacles in real time using computer vision and voice guidance.

SafePath combines **YOLO object detection**, **OpenCV**, **Flask**, and **Text-to-Speech (TTS)** to analyze the user's surroundings, estimate obstacle danger levels, provide navigation decisions, and display live analytics through a modern web dashboard.

---

## ✨ Features

- 🎯 Real-time object detection using YOLO
- 🧠 AI-based obstacle prioritization
- 📢 Voice guidance using Text-to-Speech
- 🧭 Navigation decision support
- 🚨 Three danger levels (Safe, Warning, Critical)
- 📍 Virtual Left / Front / Right sensing zones
- 📊 Live monitoring dashboard
- 📈 Detection history and statistics
- ⚡ Real-time communication between AI engine and dashboard

---

## 🛠 Technologies

- Python
- YOLO (Ultralytics)
- OpenCV
- Flask
- Flask-CORS
- pyttsx3
- Requests
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

```
SafePathAI/
│
├── static/
├── templates/
├── dashboard.py
├── safepath.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SafePathAI.git
```

Move into the project

```bash
cd SafePathAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
python dashboard.py
```

Open another terminal

```bash
python safepath.py
```

---

## 🖥 Dashboard

The Flask dashboard provides:

- Live obstacle monitoring
- Object statistics
- Detection history
- Navigation decisions
- Danger timeline
- Sensor status visualization

---

## 🧠 AI Detection Pipeline

1. Capture video from the camera
2. Detect objects using YOLO
3. Filter target objects
4. Estimate distance using bounding box size
5. Calculate danger level
6. Determine navigation decision
7. Generate voice guidance
8. Send results to the Flask dashboard

---

## 🎯 Target Objects

- Person
- Car
- Chair
- Dining Table
- Backpack
- Bottle
- Cell Phone
- Bench
- Couch

---

## 📌 Future Improvements

- Hardware implementation using Raspberry Pi
- Ultrasonic sensors
- GPS navigation
- Object tracking
- Face recognition
- Outdoor navigation
- Mobile application
- Cloud analytics
- Emergency SOS system

---

## 👩‍💻 Authors

Developed as a Computer and Communication Engineering project.

```

---

**This project demonstrates the integration of Artificial Intelligence, Computer Vision, and Web Technologies to improve accessibility for visually impaired people.**