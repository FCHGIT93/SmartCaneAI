from ultralytics import YOLO

from safepath_core.config import MODEL_PATH


class ObjectDetector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def detect(self, frame):
        return self.model(frame, verbose=False)