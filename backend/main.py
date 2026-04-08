from fastapi import FastAPI
from backend.db import add_event, get_all_sessions, get_events
from backend.event_schema import Event
from backend.detection import calculate_metrics, get_session_status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    metrics = calculate_metrics(events)
    status = get_session_status(events)

    return {"events": events, "metrics": metrics, "status": status}