#!/usr/bin/env python3
"""
Systematic Search Script for Scientific Multimodal Time Series Survey.
Compliant with PRISMA 2020 protocol and integrity rules in COMMON_METHOD.md.
"""

import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime

USER_AGENT = "AcademicSurveyBot/1.0 (mailto:lihuirui@users.noreply.github.com)"
HEADERS = {"User-Agent": USER_AGENT}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
SEARCH_LOG = os.path.join(DATA_DIR, "search_log.jsonl")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")

os.makedirs(RAW_DIR, exist_ok=True)


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def log_query(source: str, query: str, hits: int, new_candidates: int):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": source,
        "query": query,
        "hits": hits,
        "new_candidates": new_candidates,
    }
    with open(SEARCH_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def fetch_crossref(query: str, rows: int = 15):
    cache_key = "cr_" + re.sub(r"[^a-zA-Z0-9_]", "_", query)[:60] + ".json"
    cache_path = os.path.join(RAW_DIR, cache_key)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows={rows}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        time.sleep(1.0)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("message", {}).get("items", [])
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            return items
    except Exception as e:
        print(f"[Crossref Error] {query}: {e}")
        return []


def fetch_arxiv_abs(arxiv_id: str):
    cache_key = f"arxiv_{arxiv_id.replace('/', '_')}.json"
    cache_path = os.path.join(RAW_DIR, cache_key)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"https://arxiv.org/abs/{arxiv_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        time.sleep(1.0)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8")
            title_m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
            title = title_m.group(1) if title_m else ""
            desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
            abstract = desc_m.group(1) if desc_m else ""
            authors = re.findall(r'<meta name="citation_author" content="([^"]+)"', html)
            date_m = re.search(r'<meta name="citation_date" content="([^"]+)"', html)
            date = date_m.group(1) if date_m else ""
            year = int(date.split("/")[0]) if date else None

            record = {
                "source": "arXiv",
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "year": year,
                "abstract": abstract,
                "url": url,
            }
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            return record
    except Exception as e:
        print(f"[arXiv Error] {arxiv_id}: {e}")
        return None


def run_search():
    queries = [
        # Weather & Climate Foundation Models
        ("Crossref", "Pangu-Weather global weather forecast 3D neural networks"),
        ("Crossref", "GraphCast learning skillful medium-range global weather forecasting"),
        ("Crossref", "FourCastNet adaptive Fourier neural operators weather"),
        ("Crossref", "ClimaX foundation model weather climate"),
        ("Crossref", "FuXi cascade machine learning forecasting system 15-day"),
        ("Crossref", "FengWu skillful global medium-range weather forecast"),
        ("Crossref", "GenCast diffusion ensemble forecasting weather"),
        ("Crossref", "Aurora foundation model Earth system atmosphere"),
        ("Crossref", "Prithvi WxC foundation model weather climate"),
        ("Crossref", "WeatherBench 2 benchmark data-driven global weather"),
        # Remote Sensing / EO
        ("Crossref", "SatMAE pre-training transformers temporal multi-spectral satellite"),
        ("Crossref", "Presto lightweight pre-trained transformers remote sensing timeseries"),
        ("Crossref", "Galileo learning global local features remote sensing"),
        ("Crossref", "AlphaEarth Foundations embedding field model global mapping"),
        ("Crossref", "Foundation Models Generalist Geospatial Artificial Intelligence Prithvi"),
        # Hydrology & Seismology
        ("Crossref", "Global prediction extreme floods ungauged watersheds Nature"),
        ("Crossref", "SeisT foundational deep-learning model earthquake monitoring"),
        ("Crossref", "PhaseNet deep-neural-network-based arrival-time picking"),
        # Oceanography & Space Weather
        ("Crossref", "XiHe data-driven model global ocean eddy-resolving"),
        ("Crossref", "Surya foundation model heliophysics solar"),
        # Reasoning LLMs
        ("Crossref", "SciTS scientific time series understanding generation LLMs"),
        ("Crossref", "ClimateAgent multi-agent orchestration climate data science"),
        ("Crossref", "ClimateLLM efficient weather forecasting large language models"),
        ("Crossref", "Large Models for Time Series and Spatio-Temporal Data Survey Jin"),
        ("Crossref", "Position What Can Large Language Models Tell Us about Time Series Analysis"),
    ]

    verified_arxiv_ids = [
        "2211.02556",  # Pangu-Weather
        "2212.12794",  # GraphCast
        "2202.11214",  # FourCastNet
        "2301.10343",  # ClimaX
        "2304.02948",  # FengWu
        "2312.15796",  # GenCast
        "2405.13063",  # Aurora
        "2409.13598",  # Prithvi WxC
        "2308.15560",  # WeatherBench 2
        "2207.08051",  # SatMAE
        "2304.14065",  # Presto
        "2502.09356",  # Galileo
        "2310.18660",  # Prithvi-100M
        "2507.22291",  # AlphaEarth
        "2310.01037",  # SeisT
        "2402.02995",  # XiHe Ocean
        "2508.14112",  # Surya Space Weather
        "2510.03255",  # SciTS
        "2511.20109",  # ClimateAgent
        "2502.11059",  # ClimateLLM
        "2310.10196",  # Jin et al Survey
        "2402.02713",  # Jin et al Position
    ]

    candidates = {}
    if os.path.exists(CANDIDATES_FILE):
        with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
            for c in json.load(f):
                norm = normalize_title(c.get("title", ""))
                candidates[norm] = c

    initial_count = len(candidates)

    # 1. Fetch arXiv milestones
    for aid in verified_arxiv_ids:
        rec = fetch_arxiv_abs(aid)
        if rec and rec.get("title"):
            norm = normalize_title(rec["title"])
            if norm not in candidates:
                candidates[norm] = {
                    "source": "arXiv",
                    "arxiv_id": aid,
                    "doi": None,
                    "title": rec["title"],
                    "authors": rec["authors"],
                    "year": rec["year"],
                    "abstract": rec.get("abstract", ""),
                    "status": "candidate",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                }
    log_query("arXiv", "Curated verified seed list (22 papers)", len(verified_arxiv_ids), len(candidates) - initial_count)

    # 2. Run Crossref systematic queries
    for source, q in queries:
        prev = len(candidates)
        items = fetch_crossref(q, rows=10)
        for it in items:
            t = it.get("title", [""])[0].strip()
            if not t:
                continue
            norm = normalize_title(t)
            if norm not in candidates:
                year = None
                if "issued" in it and "date-parts" in it["issued"]:
                    year = it["issued"]["date-parts"][0][0]
                authors = [
                    f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
                    for a in it.get("author", [])
                ]
                candidates[norm] = {
                    "source": "Crossref",
                    "doi": it.get("DOI"),
                    "title": t,
                    "authors": authors,
                    "year": year,
                    "container_title": it.get("container-title", [""])[0] if it.get("container-title") else "",
                    "abstract": it.get("abstract", ""),
                    "status": "candidate",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                }
        log_query(source, q, len(items), len(candidates) - prev)

    candidate_list = list(candidates.values())
    with open(CANDIDATES_FILE, "w", encoding="utf-8") as f:
        json.dump(candidate_list, f, ensure_ascii=False, indent=2)

    print(f"Total unique candidates in {CANDIDATES_FILE}: {len(candidate_list)}")


if __name__ == "__main__":
    run_search()
