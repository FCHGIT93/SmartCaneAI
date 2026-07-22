"""Detection and frame-processing logic for SafePath AI."""

import cv2

from safepath_core.config import (
    CONFIDENCE_THRESHOLD,
    PRIORITY,
    TARGET_OBJECTS,
)
from safepath_core.navigation import (
    get_danger_level,
    get_direction,
    get_navigation_advice,
)


class DetectionProcessor:
    """Analyze camera frames and prepare visual, voice, and dashboard output."""

    SENSOR_COLOR = (255, 255, 0)

    DANGER_STYLES = {
        "SAFE": {"color": (0, 255, 0), "rank": 1},
        "WARNING": {"color": (0, 165, 255), "rank": 2},
        "CRITICAL": {"color": (0, 0, 255), "rank": 3},
    }

    def __init__(self, detector):
        self.detector = detector

    def process(self, frame):
        """Process one frame and return all SafePath outputs."""
        height, width = frame.shape[:2]
        frame_area = width * height
        left_limit = width // 3
        right_limit = 2 * width // 3

        self._draw_interface(frame, height, left_limit, right_limit)

        analysis = self._analyze_detections(
            frame,
            frame_area,
            left_limit,
            right_limit,
        )

        navigation_advice = get_navigation_advice(
            analysis["left_blocked"],
            analysis["front_blocked"],
            analysis["right_blocked"],
        )

        self._draw_detections(frame, analysis["display_items"])
        self._draw_detection_summary(
            frame,
            height,
            analysis["display_items"],
        )
        self._draw_navigation(
            frame,
            height,
            navigation_advice,
        )

        voice_data = self._prepare_voice_data(
            analysis["voice_candidates"],
            navigation_advice,
        )

        dashboard_data = {
            "object": voice_data["object"],
            "danger": voice_data["danger"],
            "direction": voice_data["direction"],
            "decision": navigation_advice,
            "count": len(analysis["messages"]),
            "left_status": self._zone_status(
                analysis["left_blocked"]
            ),
            "front_status": self._zone_status(
                analysis["front_blocked"]
            ),
            "right_status": self._zone_status(
                analysis["right_blocked"]
            ),
            "last_voice": voice_data["voice_output"],
        }

        return {
            "frame": frame,
            "voice_output": voice_data["voice_output"],
            "dashboard_data": dashboard_data,
        }

    def _analyze_detections(
        self,
        frame,
        frame_area,
        left_limit,
        right_limit,
    ):
        """Detect target objects and evaluate their danger and position."""
        messages = []
        display_items = []
        voice_candidates = []

        left_blocked = False
        front_blocked = False
        right_blocked = False

        results = self.detector.detect(frame)

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                object_name = self.detector.model.names[class_id]
                confidence = float(box.conf[0])

                if object_name not in TARGET_OBJECTS:
                    continue

                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2
                area = max(0, (x2 - x1) * (y2 - y1))

                direction = get_direction(
                    center_x,
                    left_limit,
                    right_limit,
                )

                danger_level, distance_text = get_danger_level(
                    area,
                    frame_area,
                )

                if danger_level in {"WARNING", "CRITICAL"}:
                    if direction == "on the left":
                        left_blocked = True
                    elif direction == "on the right":
                        right_blocked = True
                    else:
                        front_blocked = True

                message = (
                    f"{danger_level}: {object_name} "
                    f"{distance_text} {direction}"
                )

                style = self.DANGER_STYLES[danger_level]

                messages.append(message)

                display_items.append(
                    {
                        "message": message,
                        "color": style["color"],
                        "box": (x1, y1, x2, y2),
                    }
                )

                voice_candidates.append(
                    {
                        "message": message,
                        "object": object_name,
                        "danger": danger_level,
                        "direction": direction,
                        "danger_rank": style["rank"],
                        "priority": PRIORITY[object_name],
                        "area": area,
                    }
                )

        return {
            "messages": messages,
            "display_items": display_items,
            "voice_candidates": voice_candidates,
            "left_blocked": left_blocked,
            "front_blocked": front_blocked,
            "right_blocked": right_blocked,
        }

    def _draw_interface(
        self,
        frame,
        height,
        left_limit,
        right_limit,
    ):
        """Draw virtual sensor zones and system status."""
        cv2.line(
            frame,
            (left_limit, 0),
            (left_limit, height),
            self.SENSOR_COLOR,
            2,
        )
        cv2.line(
            frame,
            (right_limit, 0),
            (right_limit, height),
            self.SENSOR_COLOR,
            2,
        )

        labels = [
            ("LEFT SENSOR", (25, 40)),
            ("FRONT SENSOR", (left_limit + 20, 40)),
            ("RIGHT SENSOR", (right_limit + 20, 40)),
        ]

        for text, position in labels:
            cv2.putText(
                frame,
                text,
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                self.SENSOR_COLOR,
                2,
            )

        cv2.putText(
            frame,
            "SafePath AI Smart Navigation System",
            (20, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            3,
        )

        cv2.putText(
            frame,
            "AI Detection + Virtual Sensors Active",
            (20, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2,
        )

    @staticmethod
    def _draw_detections(frame, display_items):
        """Draw bounding boxes and object messages."""
        for item in display_items:
            x1, y1, x2, y2 = item["box"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                item["color"],
                2,
            )

            cv2.putText(
                frame,
                item["message"],
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                item["color"],
                2,
            )

    @staticmethod
    def _draw_detection_summary(
        frame,
        height,
        display_items,
    ):
        """Display up to three unique object messages."""
        unique_items = []
        seen_messages = set()

        for item in display_items:
            if item["message"] in seen_messages:
                continue

            seen_messages.add(item["message"])
            unique_items.append(item)

        y_position = height - 150

        for item in unique_items[:3]:
            cv2.putText(
                frame,
                item["message"],
                (20, y_position),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                item["color"],
                2,
            )
            y_position += 30

    @staticmethod
    def _draw_navigation(
        frame,
        height,
        navigation_advice,
    ):
        """Display the navigation decision."""
        if navigation_advice == "Stop":
            advice_color = (0, 0, 255)
        elif "Move" in navigation_advice:
            advice_color = (0, 165, 255)
        elif "Keep" in navigation_advice:
            advice_color = (0, 255, 255)
        else:
            advice_color = (0, 255, 0)

        cv2.putText(
            frame,
            f"NAVIGATION: {navigation_advice}",
            (20, height - 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            advice_color,
            3,
        )

    @staticmethod
    def _prepare_voice_data(
        voice_candidates,
        navigation_advice,
    ):
        """Rank detections and prepare spoken feedback."""
        if not voice_candidates:
            return {
                "voice_output": navigation_advice,
                "object": "None",
                "danger": "SAFE",
                "direction": "None",
            }

        ranked_candidates = sorted(
            voice_candidates,
            key=lambda item: (
                -item["danger_rank"],
                item["priority"],
                -item["area"],
            ),
        )

        selected_messages = [
            item["message"]
            for item in ranked_candidates[:3]
        ]

        primary = ranked_candidates[0]

        return {
            "voice_output": (
                f"{'. '.join(selected_messages)}. "
                f"{navigation_advice}"
            ),
            "object": primary["object"],
            "danger": primary["danger"],
            "direction": primary["direction"],
        }

    @staticmethod
    def _zone_status(is_blocked):
        """Convert a sensor state into dashboard text."""
        return "BLOCKED" if is_blocked else "CLEAR"