import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -------------------------
# SESSION WITH RETRIES
# -------------------------
session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# -------------------------
# FETCH JOBS + COMPANY HINTS
# -------------------------
def fetch_linkedin_jobs(company):
    jobs = []
    company_hints = set()

    for page in range(3):
        start = page * 25
        time.sleep(random.uniform(3.5, 6.0))

        url = "https://www.linkedin.com/jobs/search/"
        params = {"keywords": company, "start": start}

        try:
            response = session.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=30
            )
            response.raise_for_status()
            html = response.text
        except requests.exceptions.RequestException:
            print(f"[WARN] LinkedIn blocked/timeout for '{company}'")
            break

        soup = BeautifulSoup(html, "html.parser")

        for card in soup.select("div.base-search-card"):
            title = card.select_one("h3")
            time_tag = card.select_one("time")
            location = card.select_one("span.job-search-card__location")
            company_info = card.select_one("h4.base-search-card__subtitle")

            if company_info:
                company_hints.add(company_info.get_text(strip=True))

            if title:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "date": time_tag.get("datetime") if time_tag else datetime.utcnow().isoformat(),
                    "location": location.get_text(strip=True) if location else "",
                    "company_hint": company_info.get_text(strip=True) if company_info else ""
                })

    return jobs
