import os
import json
from datetime import datetime
from utils.file_utils import safe_filename

BASE_DIR = "output/job_history"
os.makedirs(BASE_DIR, exist_ok=True)

def _path(company):
    safe = safe_filename(company)
    return os.path.join(BASE_DIR, f"{safe}.json")

def load_job_history(company):
    path = _path(company)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError, FileNotFoundError, OSError):
        return []

def save_job_history(company, jobs):
    path = _path(company)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2)
    except (OSError, IOError) as e:
        print(f"[WARN] Failed to save job history for '{company}': {e}")

def merge_jobs(old, new):
    seen = set()
    merged = []

    for j in old + new:
        key = (j.get("title"), j.get("date"))
        if key not in seen:
            seen.add(key)
            merged.append(j)

    return merged
