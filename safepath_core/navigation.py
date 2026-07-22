def get_direction(center_x, left_limit, right_limit):
    if center_x < left_limit:
        return "on the left"
    elif center_x > right_limit:
        return "on the right"
    else:
        return "ahead"


def get_danger_level(area, frame_area):
    """Estimate obstacle proximity from its relative bounding-box area."""
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

    if left_blocked and right_blocked:
        return "Continue forward carefully"
    elif left_blocked:
        return "Keep slightly right"
    elif right_blocked:
        return "Keep slightly left"
    else:
        return "Path clear"