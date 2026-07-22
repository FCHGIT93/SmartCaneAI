from ultralytics import YOLO
import cv2
import pyttsx3
import time
import threading
import requests

model = YOLO("models/yolo26n.pt")
cap = cv2.VideoCapture(0)

TARGET_OBJECTS = [
    "person", "car", "chair", "dining table",
    "backpack", "bottle", "cell phone", "bench", "couch"
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
    "cell phone": 9
}

last_message = ""
last_spoken_time = 0
SPEAK_DELAY = 4
speaking = False

DASHBOARD_URL = "http://127.0.0.1:5000/update"


def speak_message(message):
    global speaking
    speaking = True
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 145)
        engine.say(message)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Voice error:", e)
    speaking = False


def get_direction(center_x, left_limit, right_limit):
    if center_x < left_limit:
        return "on the left"
    elif center_x > right_limit:
        return "on the right"
    else:
        return "ahead"


def get_danger_level(area, frame_area):
    # Relative virtual distance estimation based on object size inside the frame
    area_ratio = area / frame_area

    if area_ratio > 0.35:
        return "CRITICAL", "very close"
    elif area_ratio > 0.15:
        return "WARNING", "close"
    else:
        return "SAFE", "far"


def get_navigation_advice(left_blocked, front_blocked, right_blocked):
    if front_blocked:
        if not left_blocked:
            return "Move left"
        elif not right_blocked:
            return "Move right"
        else:
            return "Stop"
    else:
        if left_blocked and right_blocked:
            return "Continue forward carefully"
        elif left_blocked:
            return "Keep slightly right"
        elif right_blocked:
            return "Keep slightly left"
        else:
            return "Path clear"


while True:
    success, frame = cap.read()

    if not success:
        print("Camera not working")
        break

    height, width, _ = frame.shape
    frame_area = width * height

    left_limit = width // 3
    right_limit = 2 * width // 3

    cv2.line(frame, (left_limit, 0), (left_limit, height), (255, 255, 0), 2)
    cv2.line(frame, (right_limit, 0), (right_limit, height), (255, 255, 0), 2)

    cv2.putText(frame, "LEFT SENSOR", (25, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame, "FRONT SENSOR", (left_limit + 20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame, "RIGHT SENSOR", (right_limit + 20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame,
                "SafePath AI Smart Navigation System",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                3)

    cv2.putText(frame,
                "AI Detection + Virtual Sensors Active",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 255, 0),
                2)

    results = model(frame, verbose=False)

    detected_messages = []
    detected_display = []

    left_blocked = False
    front_blocked = False
    right_blocked = False

    best_voice_message = ""
    best_priority = 999
    best_area = 0
    best_danger_rank = 0
    voice_candidates = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            object_name = model.names[class_id]
            confidence = float(box.conf[0])

            if object_name not in TARGET_OBJECTS:
                continue

            if confidence < 0.45:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2
            area = (x2 - x1) * (y2 - y1)

            direction = get_direction(center_x, left_limit, right_limit)
            danger_level, distance_text = get_danger_level(area, frame_area)

            if danger_level in ["WARNING", "CRITICAL"]:
                if direction == "on the left":
                    left_blocked = True
                elif direction == "on the right":
                    right_blocked = True
                else:
                    front_blocked = True

            message = f"{danger_level}: {object_name} {distance_text} {direction}"
            detected_messages.append(message)

            if danger_level == "CRITICAL":
                box_color = (0, 0, 255)
                danger_rank = 3
            elif danger_level == "WARNING":
                box_color = (0, 165, 255)
                danger_rank = 2
            else:
                box_color = (0, 255, 0)
                danger_rank = 1

            detected_display.append((message, box_color))

            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, message, (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, box_color, 2)

            object_priority = PRIORITY[object_name]

            voice_candidates.append({
                "message": message,
                "object": object_name,
                "danger": danger_level,
                "direction": direction,
                "danger_rank": danger_rank,
                "priority": object_priority,
                "area": area
            })

            if (
                danger_rank > best_danger_rank or
                (danger_rank == best_danger_rank and object_priority < best_priority) or
                (danger_rank == best_danger_rank and object_priority == best_priority and area > best_area)
            ):
                best_danger_rank = danger_rank
                best_priority = object_priority
                best_area = area
                best_voice_message = message

    navigation_advice = get_navigation_advice(left_blocked, front_blocked, right_blocked)

    if navigation_advice == "Stop":
        advice_color = (0, 0, 255)
    elif "Move" in navigation_advice:
        advice_color = (0, 165, 255)
    elif "Keep" in navigation_advice:
        advice_color = (0, 255, 255)
    else:
        advice_color = (0, 255, 0)

    cv2.putText(frame,
                "NAVIGATION: " + navigation_advice,
                (20, height - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                advice_color,
                3)

    if detected_display:
        unique_display = []
        seen = set()

        for msg, color in detected_display:
            if msg not in seen:
                unique_display.append((msg, color))
                seen.add(msg)

        y_position = height - 150

        for msg, color in unique_display[:3]:
            cv2.putText(frame,
                        msg,
                        (20, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2)
            y_position += 30

    now = time.time()

    if voice_candidates:
        voice_candidates = sorted(
            voice_candidates,
            key=lambda item: (
                -item["danger_rank"],
                item["priority"],
                -item["area"]
            )
        )

        selected_messages = []

        for item in voice_candidates:
            if len(selected_messages) >= 3:
                break
            selected_messages.append(item["message"])

        voice_output = ". ".join(selected_messages) + ". " + navigation_advice

        dashboard_object = voice_candidates[0]["object"]
        dashboard_danger = voice_candidates[0]["danger"]
        dashboard_direction = voice_candidates[0]["direction"]

    else:
        voice_output = navigation_advice
        dashboard_object = "None"
        dashboard_danger = "SAFE"
        dashboard_direction = "None"

    left_status = "BLOCKED" if left_blocked else "CLEAR"
    front_status = "BLOCKED" if front_blocked else "CLEAR"
    right_status = "BLOCKED" if right_blocked else "CLEAR"

    try:
        data = {
            "object": dashboard_object,
            "danger": dashboard_danger,
            "direction": dashboard_direction,
            "decision": navigation_advice,
            "count": len(detected_messages),
            "left_status": left_status,
            "front_status": front_status,
            "right_status": right_status,
            "last_voice": voice_output
        }

        requests.post(DASHBOARD_URL, json=data, timeout=0.2)
    except:
        pass

    if not speaking and (voice_output != last_message or (now - last_spoken_time) > SPEAK_DELAY):
        print("Speaking:", voice_output)
        threading.Thread(target=speak_message, args=(voice_output,), daemon=True).start()
        last_message = voice_output
        last_spoken_time = now

    cv2.imshow("SafePath AI Smart Cane Simulation", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()