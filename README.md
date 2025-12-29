# Digital Transformation Tracker - Middle East

A comprehensive data intelligence pipeline that identifies and ranks companies actively undergoing digital transformation in the Middle East region. The system scrapes LinkedIn job postings, analyzes hiring patterns, and produces actionable insights on which organizations are investing in digital capabilities.

---

## Table of Contents

1. [Overview](#overview)
2. [Target Region](#target-region)
3. [How It Works](#how-it-works)
4. [Project Architecture](#project-architecture)
5. [Directory Structure](#directory-structure)
6. [Detailed Module Reference](#detailed-module-reference)
7. [Scoring Methodology](#scoring-methodology)
8. [Output Format](#output-format)
9. [Installation](#installation)
10. [Usage](#usage)
11. [Configuration](#configuration)
12. [Data Persistence](#data-persistence)
13. [Limitations](#limitations)

---

## Overview

This project solves a specific business intelligence problem: **identifying companies in the Middle East that are actively building digital capabilities**. Rather than relying on press releases or self-reported claims, the system uses **hiring behavior as a proxy signal** for genuine digital transformation.

The core hypothesis is simple:

- Companies undergoing digital transformation **hire for digital roles** (Cloud, DevOps, AI/ML, Data, Software, Product).
- The **velocity, diversity, and seniority** of these hires indicate transformation intensity.
- **Sustained hiring patterns** over time (24-month window) distinguish real transformation from one-off projects.

---

## Target Region

The pipeline is exclusively focused on the **Middle East** region. Companies are filtered to include only those with verifiable presence in:

| Country              | Key Cities       |
| -------------------- | ---------------- |
| Saudi Arabia         | Riyadh, Jeddah   |
| United Arab Emirates | Dubai, Abu Dhabi |
| Qatar                | Doha             |
| Oman                 | Muscat           |
| Kuwait               | Kuwait City      |
| Bahrain              | Manama           |
| Jordan               | Amman            |
| Egypt                | Cairo            |

Companies with primary operations in the USA, UK, Canada, Australia, or Germany are explicitly excluded to maintain regional focus.

---

## How It Works

The pipeline executes the following sequence:

```
1. SEED COMPANIES
   - Queries LinkedIn job search with Middle East location + digital keywords
   - Extracts company names from job postings
   - Builds initial candidate list

2. JOB INGESTION
   - For each candidate company, fetches current job listings
   - Merges with previously stored job history (persistent cache)
   - Filters to jobs posted within the last 24 months

3. GEOGRAPHIC FILTERING
   - Validates company has genuine Middle East presence
   - Rejects companies with strong non-ME signals (US, UK, etc.)
   - Only proceeds with confirmed ME companies

4. SIGNAL EXTRACTION
   - Classifies each job into role categories (Cloud, DevOps, AI/ML, etc.)
   - Calculates hiring momentum (acceleration vs. deceleration)
   - Scores seniority level of hires (VP/Director vs. Junior)
   - Extracts technology signals from job titles

5. SCORING
   - Computes Digital Transformation Score (DTS)
   - Calculates confidence score based on evidence quality
   - Infers transformation stage (Early, Active, Consolidated)

6. OUTPUT
   - Ranks top 50 companies by DTS
   - Generates interactive HTML dashboard
   - Stores all data for incremental updates
```

---

## Project Architecture

```
main.py          <-- Main entry point (orchestrates entire flow)
config.py                <-- Global configuration constants
requirements.txt         <-- Python dependencies

seed/                    <-- Company discovery
ingest/                  <-- Data collection from LinkedIn
process/                 <-- Signal extraction and filtering
scoring/                 <-- DTS calculation and explainability
narrative/               <-- Human-readable evidence summaries
visualize/               <-- HTML dashboard generation
utils/                   <-- Caching, checkpointing, file utilities
output/                  <-- Generated artifacts and persistent storage
```

---

## Directory Structure

### seed/

| File              | Purpose                                                                                                                                                                 |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `company_seed.py` | Queries LinkedIn with ME location + digital keywords to discover candidate companies. Iterates through combinations of 17 Middle East locations and 8 digital keywords. |

### ingest/

| File               | Purpose                                                                                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `linkedin_jobs.py` | Fetches job postings for a given company from LinkedIn. Uses session-based requests with retry logic and rate limiting. Extracts job title, date, location, and company hints. |
| `tech_stack.py`    | Placeholder for future BuiltWith/SimilarTech integration to infer technology stack from company domains.                                                                       |
| `press.py`         | Reserved for future press release ingestion. Currently empty.                                                                                                                  |

### process/

| File                  | Purpose                                                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `company_cleaner.py`  | Validates company names. Rejects entries with invalid characters, too short names, or staffing/recruitment agencies.                                   |
| `company_geo.py`      | Determines if a company is Middle East based. Returns `ME`, `NON_ME`, or `UNKNOWN` based on keyword matching in company name and job text.             |
| `country_filter.py`   | Alternative geographic filter using job locations and company name to detect Middle East presence.                                                     |
| `geo_inference.py`    | Scores geographic signals (0-4 scale) using job locations, domain TLD, and company name. Supports threshold-based filtering.                           |
| `job_window.py`       | Filters jobs to the recent 24-month window. Ensures analysis reflects current transformation activity.                                                 |
| `role_classifier.py`  | Classifies job titles into categories: Cloud, DevOps, AI/ML, Data, Product, Software, or Other. Uses keyword matching against `config.py` definitions. |
| `role_evolution.py`   | Tracks seniority distribution of hires: Leadership (VP/Director/Head), Senior (Lead/Senior), Junior (all others).                                      |
| `sector_inference.py` | Infers company sector from role keywords: Fintech, Telecom, Healthcare, Manufacturing, Energy, E-commerce, Logistics, Software.                        |
| `sector_cluster.py`   | Uses TF-IDF + K-Means clustering for unsupervised sector grouping. Available for advanced use cases.                                                   |
| `seniority.py`        | Scores job seniority: VP/Director/Head/Chief = 4, Senior/Lead = 3, Others = 2.                                                                         |
| `tech_inference.py`   | Extracts technology signals from job titles: Cloud (AWS/Azure/GCP), Containers (Docker/K8s), Data, AI/ML, DevOps, Frontend frameworks.                 |
| `time_series.py`      | Calculates hiring momentum using pandas time series resampling. Compares recent 6-month average vs. earlier average.                                   |
| `timeline.py`         | Builds month-by-month hiring timeline from job dates.                                                                                                  |
| `stage.py`            | Infers transformation stage: "Actively Transforming", "Recently Transformed", "Early Digital Shift", or "Low Evidence".                                |

### scoring/

| File                | Purpose                                                                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `dts.py`            | Computes Digital Transformation Score using weighted formula: momentum (35%), role diversity (10%), seniority (15%), tech signals (10%). |
| `confidence.py`     | Alternative confidence calculation based on job count, momentum, and role diversity.                                                     |
| `explainability.py` | Produces structured explanation object with hiring momentum, role diversity, leadership hiring, tech signals, and evidence strength.     |

### narrative/

| File                  | Purpose                                                                                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `evidence_summary.py` | Generates natural language paragraph summarizing why a company is included. Covers time-based hiring, role composition, seniority, technology signals, and momentum. |
| `narrative.py`        | Alternative narrative generator for detailed transformation analysis report.                                                                                         |

### visualize/

| File            | Purpose                                                                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dashboard.py`  | Generates interactive HTML dashboard with Chart.js bar charts for role distribution, SVG hiring timeline, explainability JSON, and evidence summary for each ranked company. |
| `timeseries.py` | Reserved for future time series visualizations. Currently empty.                                                                                                             |

### utils/

| File             | Purpose                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `cache.py`       | Loads and saves company analysis cache (`output/company_cache.json`). Enables incremental updates without re-processing.     |
| `checkpoint.py`  | Tracks which companies have been processed (`output/checkpoint.json`). Allows resume after interruption.                     |
| `job_history.py` | Persists job listings per company in `output/job_history/`. Merges new jobs with historical data to build longitudinal view. |
| `file_utils.py`  | Utility for converting company names to Windows-safe filenames.                                                              |

---

## Scoring Methodology

### Digital Transformation Score (DTS)

The DTS is a composite score (0-100 scale) calculated as:

| Component          | Weight | Description                                                       |
| ------------------ | ------ | ----------------------------------------------------------------- |
| Hiring Momentum    | 35%    | Acceleration in digital role postings (recent vs. earlier period) |
| Role Diversity     | 10%    | Number of distinct digital role categories                        |
| Seniority Score    | 15%    | Cumulative seniority of hires (leadership roles weighted higher)  |
| Technology Signals | 10%    | Count of modern technology keywords (Cloud, Containers, AI, etc.) |

Formula:

```
DTS = (momentum * 35) + (role_diversity * 10) + (seniority * 15) + (tech_signals * 10)
```

### Confidence Score

Measures evidence quality (0-1 scale):

- +0.3 if momentum is positive
- +0.2 if role diversity >= 2
- +0.2 if any leadership-level hires
- +0.3 if any technology signals detected

### Transformation Stage

Inferred from timeline depth and seniority:

| Stage                 | Criteria                                              |
| --------------------- | ----------------------------------------------------- |
| Actively Transforming | 15+ roles, 6+ months active, leadership hires present |
| Recently Transformed  | 8+ roles, 4+ months active                            |
| Early Digital Shift   | 3+ roles detected                                     |
| Low Evidence          | Below thresholds                                      |

---

## Output Format

### HTML Dashboard

Location: `output/digitally_transforming_companies_ME.html`

For each ranked company (top 50), the dashboard displays:

- Rank, company name, DTS score, confidence, and transformation stage
- Sector classification
- Role distribution bar chart (Chart.js)
- Monthly hiring timeline (SVG visualization)
- Explainability breakdown (JSON)
- Evidence summary (natural language paragraph)

### Persistent Data Files

| File                                | Purpose                                            |
| ----------------------------------- | -------------------------------------------------- |
| `output/checkpoint.json`            | List of all processed company names                |
| `output/company_cache.json`         | Full analysis results for all qualifying companies |
| `output/job_history/<company>.json` | Raw job data per company                           |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

```bash
# Clone the repository
git clone https://github.com/shaikashfaaqhamja/DIGITALLY_TRANSFORMING_COMPANIES.git
cd DIGITALLY_TRANSFORMING_COMPANIES

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package               | Purpose                             |
| --------------------- | ----------------------------------- |
| requests              | HTTP requests for LinkedIn scraping |
| beautifulsoup4        | HTML parsing                        |
| pandas                | Time series analysis                |
| numpy                 | Numerical operations                |
| matplotlib            | Plotting (if needed)                |
| scikit-learn          | TF-IDF and K-Means clustering       |
| tqdm                  | Progress bars                       |
| sentence-transformers | Semantic similarity (future use)    |

---

## Usage

### Running the Full Pipeline

```bash
python main.py
```

The pipeline will:

1. Seed companies from LinkedIn (if starting fresh)
2. Process each company incrementally
3. Save checkpoints after each company
4. Generate the final dashboard upon completion

### Expected Output

```
[INFO] Seeded 1500 raw companies
[INFO] Previously processed: 320
[INFO] Cached companies: 45
[PROGRESS] 5/1500 companies checked
[OK] Aramco | DTS=78.5 | Stage=Actively Transforming
[PROGRESS] 10/1500 companies checked
...
[INFO] Final shortlisted companies: 50
[DONE] Dashboard generated successfully
```

### Resuming After Interruption

The pipeline automatically resumes from the last checkpoint. Simply run:

```bash
python main.py
```

Previously processed companies will be skipped.

### Resetting the Pipeline

To start fresh, delete the output directory:

```bash
rm -rf output/
python main.py
```

---

## Configuration

### config.py

| Constant                | Default | Description                              |
| ----------------------- | ------- | ---------------------------------------- |
| `TIME_WINDOW_MONTHS`    | 24      | How far back to consider job postings    |
| `TOP_N`                 | 50      | Number of companies in final ranking     |
| `MIDDLE_EAST_LOCATIONS` | [list]  | Countries for geographic filtering       |
| `DIGITAL_ROLE_KEYWORDS` | {dict}  | Keyword mappings for role classification |

### main.py

| Constant     | Default | Description                                    |
| ------------ | ------- | ---------------------------------------------- |
| `DRY_RUN`    | False   | Set to True to skip web requests (for testing) |
| `BASE_SLEEP` | 2       | Seconds between company processing             |

---

## Data Persistence

The system maintains three types of persistent storage:

### 1. Checkpoint (`output/checkpoint.json`)

- Tracks all company names that have been processed
- Prevents duplicate processing on restart
- Format: JSON array of company names

### 2. Company Cache (`output/company_cache.json`)

- Stores full analysis results for qualifying companies
- Includes DTS, confidence, signals, and evidence summary
- Format: JSON object keyed by company name

### 3. Job History (`output/job_history/<company>.json`)

- One file per company with all observed job postings
- Merges historical and new jobs on each run
- Enables longitudinal analysis across multiple pipeline runs
- Format: JSON array of job objects with title, date, location

---

## Limitations

1. **LinkedIn Rate Limiting**: The scraper uses delays and retries, but LinkedIn may block requests if run too aggressively.

2. **Data Freshness**: Job postings have a natural lifecycle. Stale postings may be included until they expire from the 24-month window.

3. **Geographic Accuracy**: Geographic filtering uses keyword heuristics. Multinational companies may be misclassified.

4. **No Authentication**: The scraper uses public LinkedIn pages. Some job listings may not be visible without login.

5. **Sector Inference**: Sector classification is based on role keywords, not company metadata. May be inaccurate for diversified companies.

6. **Technology Signals**: Technology detection is limited to job title keywords. Does not analyze full job descriptions.

---

## License

This project is intended for research and business intelligence purposes. Ensure compliance with LinkedIn's Terms of Service when deploying.

---

## Contributing

To extend the pipeline:

1. Add new data sources in `ingest/` (e.g., press releases, tech stack APIs)
2. Add new signal extractors in `process/`
3. Adjust scoring weights in `scoring/dts.py`
4. Enhance visualizations in `visualize/`

All modules are designed to be stateless and composable for easy extension.
