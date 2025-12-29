import re

ME_KEYWORDS = [
    "uae","dubai","abu dhabi","saudi","riyadh","jeddah",
    "qatar","doha","oman","muscat","kuwait",
    "bahrain","manama","jordan","amman","egypt","cairo"
]

ME_TLDS = [".ae", ".sa", ".qa", ".om", ".kw", ".bh", ".jo", ".eg"]

def score_geo(company_name, jobs, domain=None):
    score = 0

    # 1. Job location signal
    locations = " ".join(j.get("location","").lower() for j in jobs)
    if any(k in locations for k in ME_KEYWORDS):
        score += 1

    # 2. Majority of jobs in ME
    me_jobs = sum(
        1 for j in jobs
        if any(k in j.get("location","").lower() for k in ME_KEYWORDS)
    )
    if jobs and (me_jobs / len(jobs)) >= 0.5:
        score += 1

    # 3. Domain TLD signal
    if domain and any(domain.endswith(tld) for tld in ME_TLDS):
        score += 1

    # 4. Company name regional hint
    if any(k in company_name.lower() for k in ME_KEYWORDS):
        score += 1

    return score


def is_middle_east(company_name, jobs, domain=None, threshold=2):
    return score_geo(company_name, jobs, domain) >= threshold
