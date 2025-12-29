def seniority_score(title):
    t = title.lower()
    if any(x in t for x in ["vp","director","head","chief"]):
        return 4
    if "senior" in t or "lead" in t:
        return 3
    return 2
