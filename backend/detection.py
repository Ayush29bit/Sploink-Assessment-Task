def calculate_metrics(events):
    total_steps = len(events)
    success = 0
    failure = 0
    action_counts = {}

    for e in events:
        status = e.metadata.status if e.metadata else "success"

        if status == "success":
            success += 1
        else:
            failure += 1

        action_counts[e.action] = action_counts.get(e.action, 0) + 1

    return {
        "total_steps": total_steps,
        "success_rate": success / total_steps if total_steps else 0,
        "failure_rate": failure / total_steps if total_steps else 0,
        "action_distribution": action_counts
    }

# Loop Detection
def detect_loop(events):
    if len(events) < 3:
        return False

    # Checking for consecutive same actions
    consecutive_count = 1
    max_consecutive = 1

    for i in range(1, len(events)):
        if events[i].action == events[i - 1].action:
            consecutive_count += 1
            max_consecutive = max(max_consecutive, consecutive_count)
        else:
            consecutive_count = 1

    # Checking for dominant action
    action_counts = {}
    for e in events:
        action_counts[e.action] = action_counts.get(e.action, 0) + 1

    dominant_ratio = max(action_counts.values()) / len(events)

    if max_consecutive >= 3:
        return True

    if dominant_ratio > 0.8: 
        return True

    return False

# Drift Detection
def detect_drift(events):
    if len(events) < 4:
        return False

    # Take early and late inputs
    early_inputs = [e.input.lower() for e in events[:2] if e.input]
    late_inputs = [e.input.lower() for e in events[-2:] if e.input]

    if not early_inputs or not late_inputs:
        return False

    early_text = " ".join(early_inputs)
    late_text = " ".join(late_inputs)

    # Simple keyword-based shift detection
    keywords = ["summarize", "code", "analyze", "write", "execute"]

    early_set = {k for k in keywords if k in early_text}
    late_set = {k for k in keywords if k in late_text}

    # If intent changed significantly
    if early_set != late_set and len(late_set - early_set) > 0:
        return True

    return False

# Failure Pattern Detection
def detect_failure(events):
    if not events:
        return False

    consecutive_failures = 0
    max_consecutive = 0
    total_failures = 0

    for e in events:
        status = e.metadata.status if e.metadata else "success"

        if status == "failure":
            consecutive_failures += 1
            total_failures += 1
            max_consecutive = max(max_consecutive, consecutive_failures)
        else:
            consecutive_failures = 0

    failure_rate = total_failures / len(events)

    if max_consecutive >= 3 or failure_rate > 0.5:
        return True

    return False

def get_session_status(events):
    if not events:
        return "empty"

    if detect_failure(events):
        return "failing"

    if detect_drift(events):
       return "drifting"

    if detect_loop(events):
        return "looping"

    return "healthy"