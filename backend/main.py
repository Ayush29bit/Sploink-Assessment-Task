from fastapi import FastAPI
from db import add_event, get_all_sessions, get_events
from event_schema import Event

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}


@app.post("/events")
def ingest_event(event: Event):
    add_event(event)
    return {"status": "event received"}


@app.get("/sessions")
def list_sessions():
    return {"sessions": list(get_all_sessions())}


@app.get("/sessions/{session_id}")
def session_events(session_id: str):
    events = get_events(session_id)
    return {"events": events}