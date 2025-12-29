MIDDLE_EAST_KEYWORDS = [
    "saudi", "uae", "dubai", "abu dhabi", "qatar",
    "doha", "oman", "kuwait", "bahrain", "jordan",
    "egypt", "riyadh", "jeddah"
]

def is_middle_east(job_locations, company_name):
    text = " ".join(job_locations).lower() + " " + company_name.lower()
    return any(k in text for k in MIDDLE_EAST_KEYWORDS)
