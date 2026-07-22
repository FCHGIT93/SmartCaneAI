MODEL_PATH = "models/yolo26n.pt"
CAMERA_INDEX = 0

TARGET_OBJECTS = [
    "person",
    "car",
    "chair",
    "dining table",
    "backpack",
    "bottle",
    "cell phone",
    "bench",
    "couch",
]

PRIORITY = {
    "person": 1,
    "car": 2,
    "chair": 3,
    "dining table": 4,
    "bench": 5,
    "couch": 6,
    "backpack": 7,
    "bottle": 8,
    "cell phone": 9,
}

CONFIDENCE_THRESHOLD = 0.45
SPEAK_DELAY = 4
VOICE_RATE = 145

DASHBOARD_URL = "http://127.0.0.1:5000/update"
DASHBOARD_TIMEOUT = 0.2