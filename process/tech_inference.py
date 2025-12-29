TECH_KEYWORDS = {
    "Cloud": ["aws", "azure", "gcp", "cloud"],
    "Containers": ["docker", "kubernetes", "k8s"],
    "Data": ["data platform", "spark", "big data", "warehouse"],
    "AI/ML": ["machine learning", "ml", "ai", "model"],
    "DevOps": ["ci/cd", "terraform", "devops", "sre"],
    "Frontend": ["react", "angular", "vue"]
}

def infer_tech_from_jobs(jobs):
    found = set()
    for j in jobs:
        text = j.get("title", "").lower()
        for tech, kws in TECH_KEYWORDS.items():
            if any(k in text for k in kws):
                found.add(tech)
    return sorted(found)
