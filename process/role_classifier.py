from config import DIGITAL_ROLE_KEYWORDS

def classify_role(title):
    t = title.lower()
    for role, kws in DIGITAL_ROLE_KEYWORDS.items():
        if any(k in t for k in kws):
            return role
    return "Other"
