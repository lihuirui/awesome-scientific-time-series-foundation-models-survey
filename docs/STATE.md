# Project State & Research Backlog

## 1. Project Overview & Meta Information
- **Repository**: `lihuirui/awesome-scientific-time-series-foundation-models-survey`
- **Working Title**: *Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey*
- **Current Phase**: **P1 (Search, Screening & Skeleton Synthesis)** (Transitioned from P0 Bootstrap)
- **Current Iteration**: 1 (Bootstrap & Initial Systematic Ingestion)
- **Date**: 2026-09-24

---

## 2. Iteration 1 Execution Summary
- [x] Initialized Git repository on `main` branch with author configuration.
- [x] Created public GitHub repository via `gh repo create`.
- [x] Downloaded reference template papers (arXiv:2310.10196, arXiv:2402.02713) to `template/` (gitignored).
- [x] Authored `docs/TEMPLATE_ANALYSIS.md` deconstructing Jin et al.'s structure and defining adaptation plan.
- [x] Authored `docs/PROTOCOL.md` adhering to PRISMA 2020 with 8 scientific Research Questions (RQ1–RQ8).
- [x] Built reproducible Python search toolchain (`scripts/search.py`) querying Crossref API and arXiv.
- [x] Conducted systematic title/abstract and full-text eligibility screening (`scripts/screen.py`).
- [x] Automated BibTeX generation (`scripts/generate_bib.py`) ensuring zero fabricated entries.
- [x] Generated 6 publication-quality figures at 300 DPI PNG and vector PDF (`scripts/generate_figures.py`):
  1. `prisma_flow.png` / `.pdf`: PRISMA 2020 Flow Diagram.
  2. `taxonomy_tree.png` / `.pdf`: 4-Pillar Hierarchical Taxonomy Tree.
  3. `domain_modality_heatmap.png` / `.pdf`: Domain $\times$ Modality Research Maturity Matrix.
  4. `weather_foundation_timeline.png` / `.pdf`: Milestone Timeline (2022–2026).
  5. `resolution_vs_leadtime.png` / `.pdf`: Spatial Resolution vs. Maximum Forecast Lead Time.
  6. `publications_by_year.png` / `.pdf`: Annual Publication Distribution by Domain.
- [x] Generated bilingual awesome-style `README.md` (`scripts/generate_readme.py`).
- [x] Authored Chinese companion overview `docs/SURVEY_zh.md`.
- [x] Constructed complete 9-section English LaTeX paper skeleton (`paper/main.tex` and `paper/sections/*.tex`).
- [x] Compiled `paper/main.pdf` using Tectonic engine (0 errors, 9 pages).
- [x] Configured `Makefile` with targets (`search`, `screen`, `bib`, `figures`, `readme`, `paper`, `check`, `all`).
- [x] Passed all quality gates via `make check`.

---

## 3. Critical Self-Review (ACM CSUR / TPAMI Reviewer Perspective)
**Evaluation Rubric (Score 1–5)**:
- **Coverage**: **4 / 5** (Covers all major natural science domains: Weather, Climate, EO/Remote Sensing, Hydrology, Oceanography, Seismology, Space Weather, and Reasoning LLMs).
- **Taxonomy Clarity**: **5 / 5** (Orthogonal 4-dimensional taxonomy cleanly separates physical domain, foundation backbone, physical conservation level, and LLM reasoning role).
- **Depth of Analysis**: **3.5 / 5** (Core mathematical foundations and models are rigorously introduced; deeper quantitative ablation comparisons and cross-domain parameterization studies are queued for P2/P3).
- **Citation Accuracy**: **5 / 5** (100% verified against academic APIs, with confirmed DOIs, arXiv IDs, parameter counts, and authenticated GitHub repositories).
- **Figures & Tables**: **4.5 / 5** (6 publication-ready figures including PRISMA flow and milestone timeline; Table II provides clean model parameter and code access synthesis).
- **Writing**: **4 / 5** (Formal academic tone, precise mathematical notation, clear problem definitions).

---

## 4. Top-3 Highest-Leverage Improvements (Backlog for Iteration 2)
1. **P2 Full-Text Deep Extraction**: Extract detailed quantitative benchmark scores from WeatherBench 2 (Z500, T850 RMSE vs. ECMWF HRES) into a dedicated benchmarking results table.
2. **Backward & Forward Snowballing**: Perform automated citation expansion on foundational papers (Pangu-Weather, GraphCast, Aurora, Galileo, SciTS) to expand coverage in hydrology and oceanography.
3. **Deepen Section 4 & Section 6**: Expand technical exposition on spherical harmonic neural operators (SFNO) and multi-agent coordination architectures for complex physical simulations.
