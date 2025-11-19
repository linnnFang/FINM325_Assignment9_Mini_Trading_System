# logger.py

from datetime import datetime
import json
import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, path="events.json"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.path = path
                cls._instance.events = []
            return cls._instance

    def log(self, event_type: str, data: dict):
        event_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "data": data
        }
        self.events.append(event_record)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.events, f, indent=4)
