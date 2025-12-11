import os
import json

DATA_FILE = "logs.json"


def load_logs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=2)
