"""Main entry point for the SafePath AI navigation system."""

import time

import cv2
import requests

from safepath_core.config import (
    CAMERA_INDEX,
    DASHBOARD_TIMEOUT,
    DASHBOARD_URL,
    SPEAK_DELAY,
)
from safepath_core.detector import ObjectDetector
from safepath_core.processor import DetectionProcessor
from safepath_core.voice import VoiceAssistant


WINDOW_TITLE = "SafePath AI Smart Cane Simulation"


def send_dashboard_update(data):
    """Send live data without stopping the system if the dashboard is offline."""
    try:
        requests.post(
            DASHBOARD_URL,
            json=data,
            timeout=DASHBOARD_TIMEOUT,
        )
    except requests.RequestException:
        pass


def main():
    """Run the real-time SafePath navigation system."""
    detector = ObjectDetector()
    processor = DetectionProcessor(detector)
    voice_assistant = VoiceAssistant()

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("Error: Camera could not be opened.")
        return

    last_message = ""
    last_spoken_time = 0.0

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Camera frame could not be captured.")
                break

            output = processor.process(frame)
            voice_output = output["voice_output"]

            send_dashboard_update(output["dashboard_data"])

            current_time = time.time()
            speech_delay_expired = (
                current_time - last_spoken_time > SPEAK_DELAY
            )
            message_changed = voice_output != last_message

            if (
                not voice_assistant.is_speaking
                and (message_changed or speech_delay_expired)
            ):
                print("Speaking:", voice_output)
                voice_assistant.speak_async(voice_output)

                last_message = voice_output
                last_spoken_time = current_time

            cv2.imshow(WINDOW_TITLE, output["frame"])

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nSafePath stopped by user.")

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()