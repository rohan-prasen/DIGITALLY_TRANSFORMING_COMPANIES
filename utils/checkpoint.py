import json
import os

CHECKPOINT_FILE = "output/checkpoint.json"

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_checkpoint(processed):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(processed)), f, indent=2)
