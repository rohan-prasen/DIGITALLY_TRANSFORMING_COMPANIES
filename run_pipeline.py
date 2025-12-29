from seed.company_seed import seed_companies
from ingest.linkedin_jobs import fetch_linkedin_jobs
from process.sector_inference import infer_sector

from process.role_classifier import classify_role
from process.seniority import seniority_score
from process.time_series import momentum
from process.company_cleaner import is_valid_company
from process.company_geo import infer_company_geo
from process.tech_inference import infer_tech_from_jobs

from scoring.dts import compute_dts
from scoring.explainability import explain

from visualize.dashboard import generate_html

from utils.checkpoint import load_checkpoint, save_checkpoint
from utils.cache import load_cache, save_cache
from utils.job_history import load_job_history, save_job_history, merge_jobs

from process.job_window import filter_recent_jobs
from process.timeline import build_timeline
from process.role_evolution import build_role_evolution
from process.stage import infer_stage
from narrative.evidence_summary import generate_evidence_summary

import time, os
from collections import Counter


# =====================================================
# CONFIDENCE SCORE (EVIDENCE-BASED)
# =====================================================
def compute_confidence(sig):
    score = 0
    if sig["momentum"] > 0:
        score += 0.3
    if sig["role_diversity"] >= 2:
        score += 0.2
    if sig["seniority"] > 0:
        score += 0.2
    if len(sig["tech_signals"]) >= 1:
        score += 0.3
    return round(min(score, 1.0), 2)


# =====================================================
# CONTROLS
# =====================================================
DRY_RUN = False
BASE_SLEEP = 2


# =====================================================
# SETUP
# =====================================================
os.makedirs("output", exist_ok=True)

processed = load_checkpoint()
cache = load_cache()

FINAL_RESULTS = []

companies = seed_companies()
total = len(companies)

print(f"[INFO] Seeded {total} raw companies")
print(f"[INFO] Previously processed: {len(processed)}")
print(f"[INFO] Cached companies: {len(cache)}")


# =====================================================
# MAIN PIPELINE
# =====================================================
for idx, c in enumerate(companies, start=1):

    if idx % 5 == 0:
        print(f"[PROGRESS] {idx}/{total} companies checked")

    name = c["name"]

    if name in processed:
        continue

    time.sleep(BASE_SLEEP)

    try:
        # -------------------------
        # BASIC SANITY FILTER
        # -------------------------
        if not is_valid_company(name):
            processed.add(name)
            save_checkpoint(processed)
            continue

        # -------------------------
        # JOB INGESTION (ACTIVE + RECENT HISTORY)
        # -------------------------
        active_jobs = fetch_linkedin_jobs(name)
        historical_jobs = load_job_history(name)

        all_jobs = merge_jobs(historical_jobs, active_jobs)
        save_job_history(name, all_jobs)

        jobs = filter_recent_jobs(all_jobs)
        if not jobs:
            processed.add(name)
            save_checkpoint(processed)
            continue

        # -------------------------
        # STRICT GEO FILTER
        # -------------------------
        company_text = " ".join(j.get("company_hint", "") for j in jobs)
        geo = infer_company_geo(name, company_text)

        # 🔴 ONLY ACCEPT STRONG ME SIGNALS
        if geo != "ME":
            processed.add(name)
            save_checkpoint(processed)
            continue

        # -------------------------
        # SIGNAL EXTRACTION
        # -------------------------
        roles = [classify_role(j.get("title", "")) for j in jobs if j.get("title")]
        dates = [j.get("date") for j in jobs if j.get("date")]

        timeline = build_timeline(dates)
        role_counts = dict(Counter(roles))
        role_evolution = build_role_evolution(jobs)
        tech_signals = infer_tech_from_jobs(jobs)
        sector = infer_sector(roles)

        sig = {
            "momentum": round(momentum(dates), 3),
            "role_diversity": len(set(roles)),
            "seniority": sum(seniority_score(j.get("title", "")) for j in jobs if j.get("title")),
            "tech_signals": tech_signals,
            "roles": sorted(set(roles)),
            "timeline": timeline,
            "role_evolution": role_evolution
        }

        # -------------------------
        # HARD EVIDENCE GATE
        # -------------------------
        if sig["role_diversity"] == 1 and sig["momentum"] <= 0:
            processed.add(name)
            save_checkpoint(processed)
            continue

        # -------------------------
        # SCORING + STAGING
        # -------------------------
        score = round(compute_dts(sig), 2)
        confidence = compute_confidence(sig)
        stage = infer_stage(timeline, sig["seniority"])

        result = {
            "name": name,
            "country": "Middle East",
            "sector": sector,
            "score": score,
            "confidence": confidence,
            "stage": stage,
            "signals": sig,
            "role_counts": role_counts,
            "explainability": explain(sig)
        }

        # -------------------------
        # GUARANTEED EVIDENCE SUMMARY
        # -------------------------
        result["evidence_summary"] = generate_evidence_summary(result)

        FINAL_RESULTS.append(result)
        cache[name] = result

        processed.add(name)
        save_checkpoint(processed)
        save_cache(cache)

        print(f"[OK] {name} | DTS={score} | Stage={stage}")

    except Exception as e:
        raise RuntimeError(f"[PIPELINE ERROR] {name}: {e}")


# =====================================================
# FINAL RANKING
# =====================================================
FINAL_RESULTS = sorted(FINAL_RESULTS, key=lambda x: x["score"], reverse=True)[:50]

print(f"[INFO] Final shortlisted companies: {len(FINAL_RESULTS)}")


# =====================================================
# DASHBOARD
# =====================================================
html = generate_html(FINAL_RESULTS)

with open("output/digitally_transforming_companies_ME.html", "w", encoding="utf-8") as f:
    f.write(html)

print("[DONE] Dashboard generated successfully")
