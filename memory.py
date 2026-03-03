import json
import os

MEMORY_FILE = "history.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

memory_store = load_memory()

def store_event(event):
    memory_store.append(event)
    save_memory(memory_store)

def get_memory():
    return memory_store[-5:]

def get_historical_events(limit=5):
    return memory_store[-limit:]