import time
import requests
from bs4 import BeautifulSoup

# -------------------------
# MIDDLE EAST–BIASED QUERIES
# -------------------------
ME_LOCATIONS = [
    "Dubai",
    "Abu Dhabi",
    "UAE",
    "Saudi Arabia",
    "Riyadh",
    "Jeddah",
    "KSA",
    "Qatar",
    "Doha",
    "Oman",
    "Muscat",
    "Kuwait",
    "Bahrain",
    "Egypt",
    "Cairo",
    "Jordan",
    "Amman"
]

DIGITAL_KEYWORDS = [
    "software",
    "technology",
    "digital",
    "data",
    "cloud",
    "platform",
    "engineering",
    "ai"
]

def seed_companies(max_pages=5):
    """
    Seeds companies by querying LinkedIn job search
    with Middle East–biased location keywords.
    """

    companies = {}

    for loc in ME_LOCATIONS:
        for kw in DIGITAL_KEYWORDS:
            for page in range(max_pages):
                time.sleep(4)  # IMPORTANT: avoid blocking
                start = page * 25

                url = "https://www.linkedin.com/jobs/search/"
                params = {
                    "keywords": f"{kw} {loc}",
                    "start": start
                }

                try:
                    html = requests.get(url, params=params, timeout=20).text
                except Exception:
                    continue

                soup = BeautifulSoup(html, "html.parser")

                for tag in soup.select("h4.base-search-card__subtitle"):
                    name = tag.get_text(strip=True)

                    # Basic sanity check
                    if not name or len(name) < 3:
                        continue

                    companies[name] = {"name": name}

    return list(companies.values())
