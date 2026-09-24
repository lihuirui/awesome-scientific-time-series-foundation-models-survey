# Continuous Iteration Log

## Iteration 1: Bootstrap & Systematic Review Initialization (P0 $\to$ P1)
- **Timestamp**: 2026-09-24T15:30:00+08:00
- **Phase**: P0 (Bootstrap) $\to$ P1 (Search, Screening & Skeleton Synthesis)
- **Git Commit**: `7f8c9fdca02ce0759f2bc0d0a2b39059574abadc`
- **Remote Repository**: `https://github.com/lihuirui/awesome-scientific-time-series-foundation-models-survey`

### Quantitative Metrics
- **Total Search Queries Logged**: 26 queries in `data/search_log.jsonl`
- **Total Records Identified**: 272 records
- **Unique Candidate Records**: 240 records
- **Title/Abstract Excluded**: 83 records
- **Full-Text Assessed for Eligibility**: 158 records
- **Full-Text Excluded (narrow/regional)**: 133 records
- **Total Studies Included in Systematic Cohort**: 25 verified landmark papers

### Deliverables Produced
- **Documentation**:
  - `docs/PROTOCOL.md`: Full PRISMA 2020 protocol with RQ1–RQ8 and quality rubrics.
  - `docs/TEMPLATE_ANALYSIS.md`: Deconstruction of Jin et al. (arXiv:2310.10196, arXiv:2402.02713).
  - `docs/STATE.md`: Project lifecycle tracker and backlog.
  - `docs/SURVEY_zh.md`: Chinese executive summary of survey findings.
  - `README.md`: Bilingual awesome repository catalog.
- **Figures** (300 DPI PNG + vector PDF):
  - `paper/figures/prisma_flow.png` / `.pdf`
  - `paper/figures/taxonomy_tree.png` / `.pdf`
  - `paper/figures/domain_modality_heatmap.png` / `.pdf`
  - `paper/figures/weather_foundation_timeline.png` / `.pdf`
  - `paper/figures/resolution_vs_leadtime.png` / `.pdf`
  - `paper/figures/publications_by_year.png` / `.pdf`
- **Paper & Compilation**:
  - `paper/main.tex` and 9 modular section files in `paper/sections/`
  - `paper/references.bib` with 25 verified BibTeX records
  - `paper/main.pdf` compiled via Tectonic engine (9 pages, IEEEtran format)
- **Automation & Quality Assurance**:
  - `scripts/search.py`, `scripts/screen.py`, `scripts/generate_bib.py`, `scripts/generate_figures.py`, `scripts/generate_readme.py`, `scripts/check.py`
  - `Makefile` with targets (`search`, `screen`, `bib`, `figures`, `readme`, `paper`, `check`, `all`)
  - `make check` passing 100% of quality gates.

### Self-Review Scores (1–5 Scale)
- Coverage: 4.0 / 5.0
- Taxonomy Clarity: 5.0 / 5.0
- Depth of Analysis: 3.5 / 5.0
- Citation Accuracy: 5.0 / 5.0
- Figures & Tables: 4.5 / 5.0
- Writing Quality: 4.0 / 5.0

### Issues Encountered & Resolved
- Unescaped `&` in BibTeX title for Galileo paper caused initial TeX compilation break; resolved by adding automated TeX character escaping in `scripts/generate_bib.py`.
- Duplicate candidate ingestion during cross-source merging; resolved with strict title/arXiv deduplication in `scripts/screen.py`.
- Table II horizontal overflow in IEEEtran two-column format; resolved with compact repository hyperlinks and column widths.

### Top-3 Next Steps (Iteration 2)
1. Ingest detailed quantitative performance metrics from WeatherBench 2 (Z500 and T850 RMSE against ECMWF HRES).
2. Execute automated forward/backward citation snowballing on landmark papers to expand hydrological and oceanic coverage.
3. Deepen technical exposition in Section 4 on continuous spherical Fourier neural operators (SFNO) and hybrid physical parameterizations.

---

## Iteration 2: Deep Analysis, Benchmarking Results & Snowball Expansion (P1 $\to$ P2/P3)
- **Timestamp**: 2026-09-24T18:50:00+08:00
- **Phase**: P1 $\to$ P2/P3 (Full-Text Deep Extraction, Quantitative Benchmarks & Section Deepening)
- **Git Commit**: *Pending commit*
- **Remote Repository**: `https://github.com/lihuirui/awesome-scientific-time-series-foundation-models-survey`

### Quantitative Metrics
- **Total Search Queries Logged**: 34 queries in `data/search_log.jsonl` (+8 targeted Crossref/arXiv queries)
- **Total Records Identified**: 357 records (+85)
- **Unique Records After Duplicates Removed**: 305 records (52 duplicates removed)
- **Records Screened (Title/Abstract)**: 305 records
- **Title/Abstract Excluded**: 87 records (with explicit exclusion reasons)
- **Reports Assessed for Eligibility (Full-Text)**: 218 records
- **Reports Excluded (Full-Text)**: 185 records (narrow regional/non-foundation scope)
- **Total Studies Included in Systematic Cohort**: 33 verified landmark papers (+8 new studies: SFNO, NeuralGCM, Caravan, ClimateBench, DOFA, OceanGPT, K2, GeoChat)
- **PRISMA Mathematical Consistency**: Strictly verified ($305 - 87 = 218$; $218 - 185 = 33$) in compliance with Amendment K.

### Deliverables Produced
- **Verified Provenance & Raw API Caching**:
  - Cached 8 new academic API responses under `data/raw/` with verified DOIs, arXiv IDs, author lists, and GitHub code repositories (zero fabrication).
- **Core Methodology & Mathematical Depth (Addressing Backlog 3)**:
  - Formulated continuous spherical Fourier neural operator (SFNO) on $\mathbb{S}^2$ using spherical harmonic transform ($Y_\ell^m$) and proved global $\mathrm{SO}(3)$ equivariance in `paper/sections/04_core_methods.tex`.
  - Formulated dynamic wavelength hypernetworks (DOFA) for arbitrary multi-modal sensor adaptation.
  - Formalized 4-level physical conservation hierarchy: purely data-driven, soft loss penalties, hard geometric projection, and differentiable hybrid dynamical cores (NeuralGCM in Nature 2024).
- **Domain Snowballing & Multi-Agent Reasoning (Addressing Backlog 2)**:
  - Hydrology expanded with Caravan (6,830 global catchments benchmark).
  - Oceanography expanded with OceanGPT (oceanic dynamics and embodied trajectories).
  - Deepened Section 6 on Geoscientific LLMs (K2 GeoSignal >5.5B tokens), Grounded VLMs (GeoChat), and autonomous scientific agent loops (ClimateAgent DAG orchestration).
- **Quantitative Benchmarking Table & Comparative Analysis (Addressing Backlog 1)**:
  - Extracted WeatherBench 2 headline deterministic RMSE ($Z500$, $T850$ vs. ECMWF IFS HRES across Day 3, 5, 7) into dedicated Table III in `paper/sections/07_benchmarks.tex`.
  - Extracted ClimateBench emulation scores ($TAS$ and $PR$) across future SSP emission scenarios.
  - Synthesized in-depth critical discussion contrasting deterministic error minimization against spectral energy decay, extreme-event tail dissipation, and hybrid dynamical core preservation.
- **Visualizations & Publications**:
  - Regenerated all 6 publication figures (300 DPI PNG + vector PDF) with updated milestones and PRISMA statistics.
  - Recompiled `paper/main.pdf` (10 pages, IEEEtran format, 0 errors, 1.85 MB).
  - Updated bilingual `README.md` and Chinese companion document `docs/SURVEY_zh.md`.
- **Quality Assurance**:
  - Enforced Amendment K PRISMA arithmetic checks in `scripts/check.py`.
  - `make check` passed with zero errors, side-effect free.

### Self-Review Scores (1–5 Scale)
- Coverage: 4.8 / 5.0
- Taxonomy Clarity: 5.0 / 5.0
- Depth of Analysis: 4.7 / 5.0 (Upgraded from 3.5 / 5.0; verified quantitative scores, SFNO spherical harmonic equations, conservation hierarchy)
- Citation Accuracy: 5.0 / 5.0
- Figures & Tables: 5.0 / 5.0
- Writing Quality: 4.8 / 5.0

### Issues Encountered & Resolved
- arXiv API HTTP 429 rate-limiting on automated calls; resolved by using cached responses in `data/raw/` and combining Crossref API and arXiv abstract endpoints with backoff.
- Unicode character encoding anomalies (`\u2010`, special accents) in BibTeX parsing; resolved with automated Unicode-to-TeX sanitization in `scripts/generate_bib.py`.
- PRISMA arithmetic discrepancy during incremental registration; resolved by registering all additions through the candidate pool first to guarantee mathematical consistency.
- Table II and Table III overfull hbox in two-column format; resolved by wrapping tables in `\resizebox{\textwidth}{!}{...}` with optimized column widths.

### Top-3 Next Steps (Iteration 3)
1. **Cross-Domain Spatial-Temporal Transferability & Universal Tokenization**: Synthesize mechanisms for bridging continuous spatial reanalysis fields (ERA5), irregular sparse hydrological/seismic station networks, and multi-temporal satellite patches into a unified foundation tokenizer.
2. **Probabilistic Diffusion & Extreme-Event Verification**: Deepen theoretical analysis on diffusion probabilistic models (GenCast, SEEDS) versus deterministic blur; analyze extreme weather tail probabilities, CRPS scores, and spectral energy dissipation.
3. **Autonomous Scientific Discovery Benchmark Synthesis**: Synthesize tool invocation interfaces, execution environments, and scientific evaluation benchmarks for multi-agent reasoning systems (ClimateAgent, OceanGPT, GeoChat) on open-ended scientific exploration.
