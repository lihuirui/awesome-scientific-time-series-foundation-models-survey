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


def fetch_crossref_doi(doi: str):
    cache_key = "cr_doi_" + re.sub(r"[^a-zA-Z0-9_]", "_", doi) + ".json"
    cache_path = os.path.join(RAW_DIR, cache_key)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        time.sleep(1.0)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            item = data.get("message", {})
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=2)
            return item
    except Exception as e:
        print(f"[Crossref DOI Error] {doi}: {e}")
        return None


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
        # Iteration 2 Additions: Neural Operators, Hybrid Physics, Hydrology, Ocean, Reasoning
        ("Crossref", "Spherical Fourier Neural Operators Learning Stable Dynamics Bonev"),
        ("Crossref", "Neural General Circulation Models for Weather and Climate Nature"),
        ("Crossref", "Caravan A global community dataset for large-sample hydrology"),
        ("Crossref", "ClimateBench A Benchmark for Data-Driven Climate Projections"),
        ("Crossref", "Neural Plasticity-Inspired Multimodal Foundation Model Earth Observation DOFA"),
        ("Crossref", "OceanGPT A Large Language Model for Ocean Science Tasks"),
        ("Crossref", "K2 A Foundation Language Model for Geoscience Knowledge Understanding"),
        ("Crossref", "GeoChat Grounded Large Vision-Language Model for Remote Sensing"),
        # Iteration 3 Additions: Probabilistic Diffusion, Universal Tokenization, Multi-Modal Science Benchmarks
        ("Crossref", "Generative emulation of weather forecast ensembles with diffusion models SEEDS"),
        ("Crossref", "UniTS A Unified Multi-Task Time Series Model"),
        ("Crossref", "MOMENT A Family of Open Time-series Foundation Models"),
        ("Crossref", "Scaling transformer neural networks for skillful and reliable medium-range weather forecasting Stormer"),
        ("Crossref", "SeisBench A Toolbox for Machine Learning in Seismology"),
        ("Crossref", "ClimSim An open large-scale dataset for training high-resolution physics emulators"),
        ("Crossref", "EarthPT a time series foundation model for Earth Observation"),
        ("Crossref", "OceanBench A Benchmark for Data-Driven Global Ocean Forecasting systems"),
        # Iteration 4 Additions: Operational NWP AI, Language-Based Time Series, Probabilistic Foundations
        ("Crossref", "AIFS ECMWF's data-driven forecasting system"),
        ("Crossref", "Chronos Learning the Language of Time Series"),
        ("Crossref", "Time-LLM Time Series Forecasting by Reprogramming Large Language Models"),
        ("Crossref", "Lag-Llama Towards Foundation Models for Probabilistic Time Series Forecasting"),
        ("Crossref", "FuXi-Extreme Improving extreme rainfall and wind forecasts with diffusion model"),
        ("Crossref", "GEO-Bench Toward Foundation Models for Earth Monitoring"),
        # Iteration 5 Additions: Neural Data Assimilation, Multimodal Alignment, Operational Reliability
        ("Crossref", "Learning Variational Data Assimilation Models and Solvers 4DVarNet"),
        ("Crossref", "FengWu-4DVar Coupling the Data-driven Weather Forecasting Model with 4D Variational Assimilation"),
        ("Crossref", "DiffDA a Diffusion Model for Weather-scale Data Assimilation"),
        ("Crossref", "Score-based Data Assimilation Rozet"),
        ("Crossref", "SkySense A Multi-Modal Remote Sensing Foundation Model Towards Universal Interpretation"),
        ("Crossref", "The Rise of Data-Driven Weather Forecasting A First Statistical Assessment"),
        # Iteration 6 Additions: Geometric Physics Invariants, Convective Downscaling, Autonomous Science Agents
        ("Crossref", "ClimODE Climate and Weather Forecasting with Physics-informed Neural ODEs"),
        ("Crossref", "Residual Corrective Diffusion Modeling for Km-scale Atmospheric Downscaling CorrDiff"),
        ("Crossref", "Deep Learning for Day Forecasts from Sparse Observations MetNet-3"),
        ("Crossref", "Skilful precipitation nowcasting using deep generative models of radar DGMR"),
        ("Crossref", "The AI Scientist Towards Fully Automated Open-Ended Scientific Discovery"),
        ("Crossref", "SciCode A Research Coding Benchmark Curated by Scientists"),
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
        "2306.03838",  # SFNO (Bonev et al.)
        "2311.07222",  # NeuralGCM (Kochkov et al.)
        "2403.15356",  # DOFA (Xiong et al.)
        "2306.05064",  # K2 (Deng et al.)
        "2311.15826",  # GeoChat (Kuckreja et al.)
        # Iteration 3 arXiv Additions
        "2306.14066",  # SEEDS (Li et al.)
        "2403.00131",  # UniTS (Gao et al.)
        "2402.03885",  # MOMENT (Goswami et al.)
        "2312.03876",  # Stormer (Nguyen et al.)
        "2111.00786",  # SeisBench (Woollam et al.)
        "2306.08754",  # ClimSim (Yu et al.)
        "2309.07207",  # EarthPT (Smith et al.)
        # Iteration 4 arXiv Additions
        "2406.01465",  # AIFS (Lang et al.)
        "2403.07815",  # Chronos (Ansari et al.)
        "2310.01728",  # Time-LLM (Jin et al.)
        "2310.08278",  # Lag-Llama (Rasul et al.)
        "2310.19822",  # FuXi-Extreme (Chen/Zhong et al.)
        "2306.03831",  # GEO-Bench (Lacoste et al.)
        # Iteration 5 arXiv Additions
        "2007.12941",  # 4DVarNet (Fablet et al.)
        "2312.12455",  # FengWu-4DVar (Xiao et al.)
        "2401.05932",  # DiffDA (Huang et al.)
        "2306.10574",  # Score-based Data Assimilation (Rozet & Louppe)
        "2312.10115",  # SkySense (Guo et al.)
        "2307.10128",  # The Rise of Data-Driven Weather Forecasting (Ben-Bouallegue et al.)
        # Iteration 6 arXiv Additions
        "2404.10024",  # ClimODE (Verma et al.)
        "2309.15214",  # CorrDiff (Mardani et al.)
        "2306.06079",  # MetNet-3 (Andrychowicz et al.)
        "2408.06292",  # The AI Scientist (Lu et al.)
        "2407.13168",  # SciCode (Tian et al.)
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
    log_query("arXiv", f"Curated verified seed list ({len(verified_arxiv_ids)} papers)", len(verified_arxiv_ids), len(candidates) - initial_count)

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
    
    # 3. Fetch verified DOIs directly
    verified_dois = [
        "10.1038/s41586-023-06185-3",  # Pangu-Weather
        "10.1126/science.adi2336",     # GraphCast
        "10.1038/s41612-023-00512-1",  # FuXi
        "10.1038/s41586-024-07145-1",  # GlobalFlood
        "10.1029/2023MS004019",        # WeatherBench 2
        "10.52202/068431-0015",        # SatMAE
        "10.1093/gji/ggz257",          # PhaseNet
        "10.1038/s41586-024-07744-y",  # NeuralGCM
        "10.1038/s41597-023-01975-w",  # Caravan
        "10.1029/2021ms002954",        # ClimateBench
        "10.18653/v1/2024.acl-long.184",  # OceanGPT
        "10.1145/3616855.3635772",     # K2
        "10.1126/sciadv.adk4489",      # SEEDS
        "10.52202/079017-4463",        # UniTS
        "10.1785/0220210324",          # SeisBench
        "10.52202/085713-0303",        # OceanBench
        "10.1029/2021ms002572",        # 4DVarNet
        "10.1175/bams-d-23-0162.1",    # Ben-Bouallegue (BAMS)
        "10.1038/s41586-021-03854-z",  # DGMR (Ravuri et al., Nature)
    ]
    prev_doi = len(candidates)
    for doi in verified_dois:
        item = fetch_crossref_doi(doi)
        if item and item.get("title"):
            t = item.get("title", [""])[0].strip()
            norm = normalize_title(t)
            if norm not in candidates:
                year = None
                if "issued" in item and "date-parts" in item["issued"]:
                    year = item["issued"]["date-parts"][0][0]
                authors = [
                    f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
                    for a in item.get("author", [])
                ]
                candidates[norm] = {
                    "source": "Crossref",
                    "doi": doi,
                    "title": t,
                    "authors": authors,
                    "year": year,
                    "container_title": item.get("container-title", [""])[0] if item.get("container-title") else "",
                    "abstract": item.get("abstract", ""),
                    "status": "candidate",
                    "retrieved_at": datetime.utcnow().isoformat() + "Z",
                }
    log_query("Crossref", "Verified landmark DOIs (16 papers)", len(verified_dois), len(candidates) - prev_doi)

    candidate_list = list(candidates.values())
    with open(CANDIDATES_FILE, "w", encoding="utf-8") as f:
        json.dump(candidate_list, f, ensure_ascii=False, indent=2)

    print(f"Total unique candidates in {CANDIDATES_FILE}: {len(candidate_list)}")


if __name__ == "__main__":
    run_search()
