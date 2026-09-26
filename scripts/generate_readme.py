#!/usr/bin/env python3
"""
Generate bilingual README.md (English + 中文简介) from data/papers.json.
Follows the requirements in COMMON_METHOD.md and PROJECT_BRIEF.md.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
README_FILE = os.path.join(BASE_DIR, "README.md")


def run_generate_readme():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)
    with open(PRISMA_FILE, "r", encoding="utf-8") as f:
        prisma = json.load(f)

    included = [p for p in papers if p.get("status") == "included"]

    # Group papers by taxonomy domain
    domains_order = [
        "Weather/Climate",
        "Polar Cryosphere",
        "Remote Sensing / EO",
        "Hydrology",
        "Oceanography",
        "Geophysics/Seismology",
        "Geo-Energy / Subsurface",
        "Space Weather",
        "Reasoning / Benchmark",
        "Foundational / Survey",
    ]

    domain_headers = {
        "Weather/Climate": "Atmosphere, Weather and Climate Foundation Models (气象与气候大模型)",
        "Polar Cryosphere": "Polar Cryosphere & Sea Ice Dynamics (极地冰冻圈与海冰动力学大模型)",
        "Remote Sensing / EO": "Earth Observation & Remote Sensing Time Series (对地观测与遥感时序)",
        "Hydrology": "Hydrology & Extreme Flood Modeling (水文与极端洪水大模型)",
        "Oceanography": "Ocean Dynamics & Marine Forecasting (海洋动力与数值预报)",
        "Geophysics/Seismology": "Geophysics & Seismology Foundation Models (地球物理与地震学大模型)",
        "Geo-Energy / Subsurface": "Geo-Energy, Geothermal & Subsurface Carbon Storage (地热与地下碳封存大模型)",
        "Space Weather": "Space Weather & Heliophysics (空间天气与日地物理)",
        "Reasoning / Benchmark": "Scientific Reasoning LLMs & Benchmarks (科学时序推理大模型与基准)",
        "Foundational / Survey": "Foundational Surveys & Methodology (基础综述与方法学)",
    }

    grouped = {d: [] for d in domains_order}
    for p in included:
        raw_d = p.get("domain", "Foundational / Survey")
        if "Polar Cryosphere" in raw_d:
            d = "Polar Cryosphere"
        elif "Geo-Energy" in raw_d or "Subsurface" in raw_d:
            d = "Geo-Energy / Subsurface"
        elif "Oceanography" in raw_d:
            d = "Oceanography"
        elif "Reasoning" in raw_d or "Cross-domain" in raw_d:
            d = "Reasoning / Benchmark"
        elif "Core Methods" in raw_d or "Position" in raw_d or "Foundational" in raw_d:
            d = "Foundational / Survey"
        elif raw_d in grouped:
            d = raw_d
        else:
            d = "Foundational / Survey"
        grouped[d].append(p)

    lines = []

    # Title & Badges
    lines.append("# Awesome Scientific Multimodal Time Series Foundation Models and Reasoning LLMs")
    lines.append("## 科学多模态时序大模型与科学推理大模型前沿进展精选\n")
    lines.append("[![Survey PDF](https://img.shields.io/badge/Paper-PDF-red.svg)](paper/main.pdf) "
                 f"[![PRISMA Included](https://img.shields.io/badge/PRISMA%20Included-{len(included)}%20papers-brightgreen.svg)](#prisma-systematic-review-statistics) "
                 "[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) "
                 "[![Maintenance](https://img.shields.io/badge/Maintained%20by-Antigravity%20CLI-purple.svg)](#how-this-survey-is-maintained)\n")

    # Introduction (English & Chinese)
    lines.append("## Overview / 项目概述\n")
    lines.append(
        "This repository hosts the curated paper collection, systematized metadata, code implementations, "
        "and a comprehensive survey paper on **Scientific Multimodal Time Series Foundation Models and Scientific Reasoning Time Series LLMs**.\n"
    )
    lines.append(
        "本项目收录自然科学领域（气象与气候、遥感与对地观测、水文与洪水、海洋学、地球物理与地震学、空间天气、物理能源等）中，"
        "面向多模态时间序列（站点观测、网格再分析场、卫星影像序列、物理波形、科学文本报告）的**基础模型（Foundation Models）**、"
        "**连续神经算子（Neural Operators）**与**科学时序大语言模型/智能体（Scientific Reasoning LLMs / Agents）**。\n"
    )
    lines.append("- **Full Survey Paper (PDF)**: [`paper/main.pdf`](paper/main.pdf)")
    lines.append("- **Systematic Review Protocol**: [`docs/PROTOCOL.md`](docs/PROTOCOL.md)")
    lines.append("- **Reference Survey Deconstruction**: [`docs/TEMPLATE_ANALYSIS.md`](docs/TEMPLATE_ANALYSIS.md)")
    lines.append("- **Chinese Summary Document**: [`docs/SURVEY_zh.md`](docs/SURVEY_zh.md)\n")

    # Taxonomy Figure
    lines.append("## Taxonomy Framework / 科学时序分类体系\n")
    lines.append("![Taxonomy Tree](paper/figures/taxonomy_tree.png)\n")
    lines.append("The taxonomy categorizes the literature across four core dimensions:")
    lines.append("1. **Scientific Domain & Modality**: Weather/Climate, Earth Observation, Hydrology, Oceanography, Geophysics, Space Weather.")
    lines.append("2. **Foundation Architecture**: 3D Spatial Transformers, Multi-Mesh GNNs, Continuous Neural Operators (AFNO/SFNO), Multimodal Masked Autoencoders.")
    lines.append("3. **Physics Integration Level**: Purely Data-Driven, Soft Physics Loss Penalties, Hard Conservation Constraints, Hybrid PDE-Neural Ensembles.")
    lines.append("4. **Role of Reasoning LLMs**: Scientific Reasoner, Contextual Enhancer, Autonomous Scientific Agent, Interactive Interface.\n")

    # PRISMA Flow & Stats
    lines.append("## PRISMA Systematic Review Statistics\n")
    lines.append("![PRISMA 2020 Flow](paper/figures/prisma_flow.png)\n")
    lines.append(f"- **Records Identified across Academic APIs**: {prisma['records_identified']}")
    lines.append(f"- **Unique Candidates Evaluated**: {prisma['records_after_duplicates_removed']}")
    lines.append(f"- **Title/Abstract Excluded**: {prisma['records_excluded_title_abstract']}")
    lines.append(f"- **Full-Text Assessed for Eligibility**: {prisma['reports_assessed_for_eligibility']}")
    lines.append(f"- **Full-Text Excluded (narrow/regional)**: {prisma['reports_excluded_full_text']}")
    lines.append(f"- **Studies Rigorously Included**: {prisma['studies_included_in_review']}\n")

    # Domain Heatmap & Timeline
    lines.append("## Research Landscape & Milestone Timeline\n")
    lines.append("### Domain × Modality Maturity Matrix")
    lines.append("![Domain Modality Heatmap](paper/figures/domain_modality_heatmap.png)\n")
    lines.append("### Milestone Timeline (2022–2026)")
    lines.append("![Milestone Timeline](paper/figures/weather_foundation_timeline.png)\n")
    lines.append("### Spatial Resolution vs. Lead Time")
    lines.append("![Resolution vs Lead Time](paper/figures/resolution_vs_leadtime.png)\n")

    # Curated Paper Lists
    lines.append("## Curated Paper Collection / 核心文献精选\n")

    for d in domains_order:
        papers_in_d = grouped.get(d, [])
        if not papers_in_d:
            continue
        header = domain_headers.get(d, d)
        lines.append(f"### {header}\n")

        for p in papers_in_d:
            title = p["title"]
            year = p.get("year", "N/A")
            venue = p.get("venue", "arXiv")
            authors = ", ".join(p.get("authors", [])[:3])
            if len(p.get("authors", [])) > 3:
                authors += " et al."
            doi_or_url = p.get("doi_or_arxiv", "#")
            code_url = p.get("code_url", "not available")
            backbone = p.get("backbone", "N/A")
            params = p.get("model_size", "not reported")
            physics = p.get("physics_integration", "Purely data-driven")

            code_badge = f"[![Code](https://img.shields.io/badge/Code-GitHub-blue.svg)]({code_url})" if code_url != "not available" else "`[Code not available]`"

            lines.append(f"- **{title}** ({venue} {year})")
            lines.append(f"  - *Authors*: {authors}")
            lines.append(f"  - *Architecture*: `{backbone}` | *Params*: `{params}` | *Physics*: `{physics}`")
            lines.append(f"  - *Links*: [Paper / DOI]({doi_or_url}) | {code_badge}\n")

    # How this survey is maintained
    lines.append("## How This Survey Is Maintained / 本项目自动化维护机制\n")
    lines.append(
        "This repository is maintained through an autonomous, protocol-driven systematic-review loop executed via the Antigravity CLI:\n"
    )
    lines.append("1. **Continuous Search & Ingestion**: Scheduled API calls query Crossref and arXiv for newly minted preprints and peer-reviewed works.")
    lines.append("2. **Strict PRISMA Quality Gates**: Title, abstract, and full-text eligibility criteria are automatically enforced without manual hallucination.")
    lines.append("3. **Verifiable Data Lineage**: All cited metadata, model sizes, training datasets, and GitHub repositories are checked against official sources.")
    lines.append("4. **Autonomous Compilation**: LaTeX paper drafts (`paper/main.tex`), vector figures, BibTeX records, and this README are synchronized on every iteration.")
    lines.append("\n```bash\n# Reproduce all artifacts and quality checks\nmake all\n```\n")

    lines.append("## Citation / 引用\n")
    lines.append("If you find this survey or repository useful in your research, please cite:\n")
    lines.append("```bibtex\n@article{scientific_multimodal_ts_survey_2026,\n"
                 "  title = {{Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey}},\n"
                 "  author = {Li, Huirui},\n"
                 "  journal = {arXiv preprint},\n"
                 "  year = {2026},\n"
                 "  url = {https://github.com/lihuirui/awesome-scientific-time-series-foundation-models-survey}\n"
                 "}\n```\n")

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated {README_FILE} with {len(included)} included papers.")


if __name__ == "__main__":
    run_generate_readme()
