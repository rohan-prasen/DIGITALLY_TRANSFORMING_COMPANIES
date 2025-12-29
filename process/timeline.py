from collections import Counter
from datetime import datetime

def build_timeline(dates):
    months = []
    for d in dates:
        try:
            dt = datetime.fromisoformat(d[:10])
            months.append(dt.strftime("%Y-%m"))
        except:
            continue

    counts = Counter(months)
    return sorted(
        [{"month": m, "count": counts[m]} for m in counts],
        key=lambda x: x["month"]
    )
