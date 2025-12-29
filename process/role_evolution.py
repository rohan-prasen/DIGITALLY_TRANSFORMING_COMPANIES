from collections import defaultdict
from process.seniority import seniority_score

def build_role_evolution(jobs):
    buckets = defaultdict(int)

    for j in jobs:
        title = j.get("title", "")
        s = seniority_score(title)

        if s >= 3:
            buckets["Leadership"] += 1
        elif s == 2:
            buckets["Senior"] += 1
        else:
            buckets["Junior"] += 1

    return dict(buckets)
