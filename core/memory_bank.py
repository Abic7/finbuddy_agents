import json
import os

class MemoryBank:
    """
    Stores spending history, recurring merchants, behavioral patterns.
    """

    def __init__(self, path="memory_bank.json"):
        self.path = path
        self.memory = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {"history": []}

    def add_record(self, record):
        self.memory["history"].append(record)
        self._save()

    def get_history(self):
        return self.memory["history"]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)
