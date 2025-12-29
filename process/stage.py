def infer_stage(timeline, seniority):
    total = sum(p["count"] for p in timeline)
    months = len(timeline)

    if total >= 15 and seniority > 0 and months >= 6:
        return "Actively Transforming"
    if total >= 8 and months >= 4:
        return "Recently Transformed"
    if total >= 3:
        return "Early Digital Shift"
    return "Low Evidence"
