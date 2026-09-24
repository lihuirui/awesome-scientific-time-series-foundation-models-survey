# Systematic Review Protocol: Scientific Multimodal Time Series Foundation Models and Reasoning LLMs

**Protocol Version**: 1.0.0  
**Initial Date**: 2026-09-24  
**Last Updated**: 2026-09-24  
**Framework**: PRISMA 2020 (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)  
**Survey Project**: *Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey*

---

## 1. Research Questions (RQs)

Based on `maintenance/PROJECT_BRIEF.md`, the survey addresses eight central research questions:

- **RQ1 (Data Modalities & Multimodal Fusion)**: Which scientific data modalities (in-situ station time series, gridded reanalysis tensors, multi-spectral remote sensing imagery, seismic waveforms, textual observation logs) are integrated in scientific foundation models, and what cross-modal fusion mechanisms (e.g. cross-attention, token alignment, spatial projection) are employed?
- **RQ2 (Pretraining Data & Objectives)**: What large-scale scientific pretraining corpora (e.g., ERA5, CMIP6, HRES, USGS, Sentinel, Landsat, IRIS seismology) are used, and what self-supervised learning objectives (masked autoencoding, multi-step autoregressive rollout, score matching, diffusion denoising) drive pretraining?
- **RQ3 (Physics Integration & Physical Consistency)**: How are physical laws, partial differential equations (PDEs), and conservation constraints (conservation of mass, energy, momentum, moisture) incorporated into foundation model architectures (purely data-driven vs. soft physics-informed loss penalties vs. hard architectural projection vs. hybrid PDE-neural solvers)?
- **RQ4 (Spatio-Temporal Architectures)**: What architectural backbones (spherical Fourier neural operators, 3D swin transformers, multi-mesh graph neural networks, latent diffusion models) best scale to spherical geometries, non-Euclidean topologies, and multi-scale continuous temporal dynamics?
- **RQ5 (Uncertainty Quantification & Ensembling)**: How do scientific foundation models quantify predictive uncertainty, capture extreme tail events, and generate calibrated probabilistic forecasts (e.g., Monte Carlo rollout, perturbation ensembles, generative diffusion sampling)?
- **RQ6 (Evaluation Protocols & Scientific Benchmarks)**: What standardized evaluation frameworks (e.g., WeatherBench 2, ClimateBench, SEVIR, EarthNet, SciTS) are established, and how do machine learning models compare against operational numerical models (e.g. ECMWF IFS/HRES, NOAA GFS)?
- **RQ7 (Scientific Reasoning LLMs & Autonomous Agents)**: What functional roles do Large Language Models (LLMs) play when operating over scientific temporal and spatio-temporal data (natural language interface, semantic contextual enhancer, multi-step domain reasoner, or autonomous tool-using agent interacting with simulators)?
- **RQ8 (Gaps, Compute Bottlenecks & Trust)**: What are the prevailing compute limitations, data governance gaps, physical hallucination risks, and trust bottlenecks hindering operational deployment in critical natural science institutions?

---

## 2. Review Scope and Eligibility Criteria

### 2.1 Time Window
- **Eligibility Window**: `2021-01-01` to `2026-09-24` (continuously updated on each iteration).
- Seminal prior works (e.g. initial neural operator foundations) may be referenced in background but are not counted in the PRISMA systematic cohort.

### 2.2 Target Scientific Domains
1. **Atmosphere, Weather & Climate**: Global and regional numerical weather prediction, seasonal climate projection, extreme storm tracking, precipitation nowcasting.
2. **Hydrology & Water Resources**: Streamflow forecasting, flood modeling, drought indices, groundwater dynamics, river network graphs.
3. **Earth Observation & Remote Sensing**: Satellite multispectral image time series, land cover dynamics, phenology, carbon flux.
4. **Oceanography & Marine Systems**: Sea surface temperature, ocean currents, wave heights, marine heatwaves.
5. **Geophysics & Seismology**: Earthquake early warning, waveform phase picking, seismic tomography, fault slip prediction.
6. **Ecology & Biodiversity**: Acoustic monitoring time series, species distribution trajectories, vegetation health.
7. **Space Weather & Astronomy**: Solar flare prediction, geomagnetic disturbance indices, stellar light curves.
8. **Geo-Energy & Subsurface**: Physically grounded geothermal reservoir monitoring, carbon capture plume tracking, wind/solar physical power forecasting.
9. **Scientific Reasoning & Agent Systems**: LLM agents operating over temporal/spatio-temporal scientific datasets and benchmarks (e.g., SciTS).

### 2.3 Inclusion Criteria (IC)
- **IC1 (Domain Relevance)**: The paper focuses on natural science domains involving temporal or spatio-temporal dynamics, or develops foundation models / LLM reasoning specifically for scientific temporal data.
- **IC2 (Model Paradigm)**: The work proposes or extensively investigates a foundation model, pre-trained large model, neural operator, generative spatio-temporal model, or LLM reasoning/agent framework.
- **IC3 (Empirical Rigor & Reproducibility)**: The paper provides clear empirical evaluation on scientific datasets or established operational benchmarks.
- **IC4 (Peer-Reviewed or Primary Preprint)**: Published in reputable peer-reviewed conferences (NeurIPS, ICML, ICLR, KDD, AAAI, CVPR), journals (Nature, Science, Nature family, AMS, AGU, IEEE TPAMI/TGRS), or formal preprints on arXiv.

### 2.4 Exclusion Criteria (EC)
- **EC1 (Out of Scope Domain)**: Pure urban traffic flow, financial stock prediction, retail demand forecasting, or general video generation without physical grounding.
- **EC2 (Classical Local Models)**: Small classical task-specific models (e.g., standard 2-layer LSTM or small MLP trained from scratch on a single station) without pretraining, transferability, or foundation model properties.
- **EC3 (Non-Verifiable / Unsubstantiated)**: Papers without accessible technical reports, retracted works, or claims lacking empirical evidence.
- **EC4 (Duplicate / Superseded)**: Earlier preliminary workshop abstracts when a full conference or journal version exists.

---

## 3. Information Sources and Search Strategy

### 3.1 Targeted Databases & APIs
- **arXiv API / Web**: Primary source for bleeding-edge preprints in `cs.LG`, `cs.AI`, `physics.ao-ph`, `stat.ML`, `physics.geo-ph`.
- **Crossref REST API**: Automated resolution of DOIs, peer-reviewed publication metadata, and journal venues.
- **OpenAlex REST API**: Comprehensive academic graph indexing works across disciplines.
- **Semantic Scholar Graph API**: Forward and backward citation snowballing and venue tracking.
- **GitHub API**: Active verification of open-source model checkpoints, evaluation suites, and code repositories.

### 3.2 Verbatim Boolean Search Strings
1. **Query Set A (Weather & Climate Foundation Models)**:
   `("foundation model" OR "large model" OR "pre-trained") AND ("weather" OR "climate" OR "ERA5") AND ("forecast" OR "reanalysis")`
2. **Query Set B (Scientific Spatio-Temporal & Neural Operators)**:
   `("neural operator" OR "Fourier neural operator" OR "transformer") AND ("spatio-temporal" OR "spatiotemporal") AND ("fluid" OR "atmosphere" OR "ocean" OR "geophysics")`
3. **Query Set C (Remote Sensing & Earth Observation Time Series)**:
   `("foundation model" OR "masked autoencoder" OR "self-supervised") AND ("satellite" OR "remote sensing" OR "Earth observation") AND ("time series" OR "temporal")`
4. **Query Set D (Hydrology & Seismology Foundation Models)**:
   `("foundation model" OR "deep learning") AND ("streamflow" OR "hydrology" OR "seismic" OR "earthquake") AND ("waveform" OR "time series")`
5. **Query Set E (Scientific Reasoning LLMs for Time Series)**:
   `("large language model" OR "LLM agent" OR "reasoning") AND ("scientific" OR "physical" OR "spatio-temporal") AND ("time series")`

---

## 4. Screening and Selection Procedure

1. **Identification Phase**:
   - Automated ingestion from APIs via `scripts/search.py`.
   - Logging of query string, timestamp, hit count, and unique candidates in `data/search_log.jsonl`.
2. **Deduplication Phase**:
   - Automated normalization of title (lowercase, stripping punctuation and whitespace) and resolution against DOI and arXiv identifier.
3. **Title and Abstract Screening**:
   - Inspection against IC1–IC4 and EC1–EC4.
   - Tagged as `included`, `excluded_title`, or `candidate`.
4. **Full-Text Eligibility Review**:
   - Examination of paper text for model size, pretraining corpus, physics incorporation, evaluation benchmark, and code availability.
5. **Snowballing Phase**:
   - Backward snowballing: scanning reference lists of milestone papers (e.g., Pangu-Weather, GraphCast, ClimaX, Prithvi, SatMAE).
   - Forward snowballing: querying Semantic Scholar for key papers citing foundational works.

---

## 5. Data Extraction Schema & Quality Rubric

Every included paper in `data/papers.json` is annotated with the following standardized fields:
- `bibkey`: Unique citation key (`AuthorYearTitleKeyword`).
- `title`: Complete formal title.
- `authors`: Author list.
- `year`: Publication / preprint year.
- `venue`: Conference, journal, or arXiv identifier.
- `domain`: One of `Weather/Climate`, `Hydrology`, `Remote Sensing / EO`, `Oceanography`, `Geophysics/Seismology`, `Ecology`, `Space Weather`, `Reasoning / Benchmark`.
- `modality`: Combination of `Gridded reanalysis`, `In-situ stations`, `Satellite imagery`, `Waveforms`, `Text/Reports`.
- `backbone`: Architecture family (e.g. `3D Swin Transformer`, `Graph Neural Network`, `Spherical FNO`, `Diffusion Model`, `LLM Agent`).
- `pretraining_data`: Dataset name (e.g., `ERA5`, `HRES`, `Sentinel-2`, `Landsat`, `IRIS`) and scale.
- `physics_integration`: Category (`Purely data-driven`, `Soft physics loss`, `Hard constraint projection`, `Hybrid PDE solver`).
- `role_of_llm`: Category (`None`, `Interface/Prompting`, `Contextual Enhancer`, `Autonomous Agent`, `Scientific Reasoner`).
- `lead_time_or_task`: Downstream forecasting horizon or task description.
- `model_size`: Parameter count (strictly stated value or "not reported").
- `code_url`: Verified repository URL or "not available".
- `quality_score`: Sum of scores across 4 dimensions (0–3 each, max 12):
  1. *Novelty & Architectural Contribution* (0–3)
  2. *Empirical Rigor & Benchmark Standard* (0–3)
  3. *Scientific Grounding & Physical Relevance* (0–3)
  4. *Openness & Reproducibility* (0–3)

---

## 6. PRISMA Tracking and Flow Metrics
PRISMA metrics are maintained in `data/prisma_counts.json`:
- `records_identified`: Total hits across search queries.
- `records_after_duplicates_removed`: Unique candidates.
- `records_screened_title_abstract`: Screened candidates.
- `records_excluded_title_abstract`: Excluded based on title/abstract.
- `reports_sought_for_retrieval`: Retained for full-text assessment.
- `reports_not_retrieved`: Inaccessible or invalid documents.
- `reports_assessed_for_eligibility`: Fully analyzed works.
- `reports_excluded_full_text`: Excluded with explicit reason.
- `studies_included_in_review`: Final included systematic corpus.
