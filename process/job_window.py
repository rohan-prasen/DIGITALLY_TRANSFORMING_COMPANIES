from datetime import datetime, timedelta

WINDOW_MONTHS = 24   # ✅ THIS is your “recent history” definition

def filter_recent_jobs(jobs):
    cutoff = datetime.utcnow() - timedelta(days=30 * WINDOW_MONTHS)

    recent = []
    for j in jobs:
        try:
            dt = datetime.fromisoformat(j["date"][:10])
            if dt >= cutoff:
                recent.append(j)
        except Exception:
            continue

    return recent
