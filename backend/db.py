from collections import defaultdict

# session_id => list of events
events_db = defaultdict(list)

def add_event(event):
    session_id = event.session_id

    # Avoid duplicates 
    existing = events_db[session_id]
    for e in existing:
        if (
            e.step == event.step and
            e.action == event.action and
            e.timestamp == event.timestamp
        ):
            return  # duplicate => ignore

    events_db[session_id].append(event)

def get_events(session_id):
    return sorted(events_db[session_id], key=lambda x: x.timestamp)

def get_all_sessions():
    return events_db.keys()