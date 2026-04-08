import argparse
import requests
import time
import random

API_URL = "http://127.0.0.1:8000/events"

def send_event(event):
    try:
        requests.post(API_URL, json=event)
    except Exception as e:
        print("Error sending event:", e)

def create_event(session_id, step, action, input_text, output_text, status="success"):
    return {
        "session_id": session_id,
        "timestamp": time.time(),
        "step": step,
        "action": action,
        "input": input_text,
        "output": output_text,
        "metadata": {
            "status": status
        }
    }

# Normal Scenario 
def normal_scenario(session_id):
    steps = [
        ("read_file", "read config", "file content"),
        ("llm_call", "summarize config", "summary"),
        ("write_file", "write summary", "done")
    ]

    for i, (action, inp, out) in enumerate(steps, 1):
        event = create_event(session_id, i, action, inp, out)
        send_event(event)
        time.sleep(0.5)

# Failure Scenario
def failure_scenario(session_id):
    for i in range(1, 6):
        status = "failure" if i >= 2 else "success"

        event = create_event(
            session_id,
            i,
            "run_command",
            "execute deployment",
            "error occurred" if status == "failure" else "started",
            status
        )
        send_event(event)
        time.sleep(0.4)

# Drift Scenario
def drift_scenario(session_id):
    steps = [
        ("llm_call", "summarize document", "summary"),
        ("llm_call", "refine summary", "refined"),
        ("llm_call", "write python code", "code output"),  
        ("run_command", "execute script", "done")
    ]

    for i, (action, inp, out) in enumerate(steps, 1):
        event = create_event(session_id, i, action, inp, out)
        send_event(event)
        time.sleep(0.5)

# Loop Scenario        
def loop_scenario(session_id):
    for i in range(1, 8):
        event = create_event(
            session_id,
            i,
            "llm_call",
            f"summarize part {i % 3}",  
            "partial summary"
        )
        send_event(event)
        time.sleep(0.3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=str, required=True)
    args = parser.parse_args()

    session_id = f"session_{random.randint(1000, 9999)}"

    if args.scenario == "normal":
        normal_scenario(session_id)
    elif args.scenario == "loop":
        loop_scenario(session_id)
    elif args.scenario == "drift":
        drift_scenario(session_id)
    elif args.scenario == "failure":
        failure_scenario(session_id)
    else:
        print("Invalid scenario")
