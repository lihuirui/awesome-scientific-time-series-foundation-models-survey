# Continuous Iteration Log

## Iteration 1: Bootstrap & Systematic Review Initialization (P0 $\to$ P1)
- **Timestamp**: 2026-09-24T15:30:00+08:00
- **Phase**: P0 (Bootstrap) $\to$ P1 (Search, Screening & Skeleton Synthesis)
- **Git Commit**: Initial bootstrap commit
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
