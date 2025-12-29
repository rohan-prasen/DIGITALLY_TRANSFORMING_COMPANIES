ME_KEYWORDS = {
    "saudi arabia", "ksa", "uae", "dubai", "abu dhabi",
    "egypt", "cairo", "jordan", "amman",
    "qatar", "doha", "oman", "muscat", "kuwait", "bahrain"
}

STRONG_NON_ME = {
    "usa", "united states", "u.s.", "california", "texas",
    "uk", "united kingdom", "london",
    "canada", "australia", "germany"
}

def infer_company_geo(company_name, company_text=""):
    text = f"{company_name} {company_text}".lower()

    for kw in STRONG_NON_ME:
        if kw in text:
            return "NON_ME"

    for kw in ME_KEYWORDS:
        if kw in text:
            return "ME"

    return "UNKNOWN"
