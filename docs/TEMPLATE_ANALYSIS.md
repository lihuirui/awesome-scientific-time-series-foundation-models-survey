# Analysis of Reference Surveys and Methodological Adaptation

This document analyzes the reference template surveys:
1. **Primary Reference**: Ming Jin et al., *"Large Models for Time Series and Spatio-Temporal Data: A Survey and Outlook"*, arXiv:2310.10196 (ACM Computing Surveys / TKDE style).
2. **Secondary Reference**: Ming Jin et al., *"Position: What Can Large Language Models Tell Us about Time Series Analysis"*, ICML 2024 / arXiv:2402.02713.

It outlines their organizational logic, taxonomy frameworks, visual styles, and specifies how we adapt these principles to our domain-science focused survey:
**"Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey"**.

---

## 1. Structural Deconstruction of Primary Template (arXiv:2310.10196)

### 1.1 Section Breakdown
1. **Introduction**:
   - High-level paradigm shift from classical deep learning / task-specific models to foundation models (PFMs) and large language models (LLMs).
   - Distinctive challenges of temporal/spatio-temporal dynamics (continuous dynamics, multi-rate sampling, spatial irregular topologies, distribution drift).
   - Core contributions (comprehensive taxonomy, multi-angle analysis, unified resource catalog, open opportunities).
   - **Survey Comparison Table**: Explicit tabular comparison contrasting the survey against prior surveys across temporal granularity, spatial context, multimodal capabilities, and domain coverage.
2. **Background & Problem Formulation**:
   - Formal mathematical definitions: 1D time series, multivariate time series, spatio-temporal graphs, regular grid tensors.
   - Task formulations: forecasting, imputation, classification, anomaly detection, spatio-temporal kriging/downscaling.
   - Backbone evolutions: RNNs/CNNs $\to$ Transformers $\to$ Neural Operators $\to$ Diffusion Models $\to$ Pre-trained LLM backbones.
3. **Overview & Taxonomy Framework**:
   - Multi-dimensional classification along 4 orthogonal axes:
     - *Data Modality / Structure*
     - *Model Category & Pretraining Paradigm*
     - *Methodology / Adaptation Strategy*
     - *Application Domain & Task*
   - Full-page Taxonomy Hierarchical Tree figure linking architectural paradigms to downstream tasks.
4. **Core Methodology: Time Series Foundation Models (LM4TS)**:
   - Stratified by pretraining objective and adaptation strategy:
     - LLM-direct / Prompting (reprogramming, tokenization, text-prompt templates).
     - Cross-domain pretraining from scratch (masked autoencoding, patch forecasting, diffusion).
     - Contrastive and self-supervised representations.
5. **Core Methodology: Spatio-Temporal Foundation Models (LM4STD)**:
   - Spatial discretization: Graph-based vs. Grid-based.
   - Domain-specific adaptations (traffic, environment, remote sensing, weather).
6. **Resources, Benchmarks, and Toolkits**:
   - Tabular curation of standard open datasets, pretraining corpora, public model checkpoints, and codebases.
7. **Open Challenges and Future Directions**:
   - Scaling behaviors, physical laws and constraints, multimodal alignment, efficiency/tokenization, uncertainty quantification, explainability and trustworthy deployment.
8. **Conclusion**.

---

## 2. Structural Deconstruction of Secondary Reference (arXiv:2402.02713)

### 2.1 Key Insights on the Role of LLMs in Temporal Reasoning
Jin et al. (2024) critically examines *why* and *how* LLMs assist temporal data processing:
1. **Direct Predictor vs. Reasoner**:
   - Direct numerical pattern fitting often does not benefit from LLM size unless cross-modal semantic context is involved.
   - The primary value of LLMs emerges when temporal patterns require **semantic contextualization**, **tool execution**, or **multi-step domain reasoning**.
2. **Taxonomy of LLM Engagement Modes**:
   - *LLM as Predictor*: Tokenizing continuous values into text or patch embeddings fed directly into frozen/fine-tuned transformer backbones.
   - *LLM as Enhancer/Prefix*: Providing contextual embeddings, domain priors, or metadata prompting.
   - *LLM as Agent/Reasoner*: Orchestrating external solvers, querying scientific databases, decomposing multi-horizon predictive tasks, and synthesizing physical explanations.

---

## 3. Adaptation Strategy for This Scientific Multimodal Survey

While Jin et al. covers general spatio-temporal data mining (with heavy emphasis on urban traffic, human mobility, and generic time series benchmarks), **our survey focuses strictly on Natural Science domains and physically-grounded systems**.

### 3.1 Scoping and Domain Boundaries
Unlike generic urban/traffic surveys, our survey investigates:
- **Physical domains**: Weather and climate, hydrology, Earth observation & remote sensing, oceanography, geophysics/seismology, ecology/biodiversity, space weather/astronomy, and geo-energy.
- **Multimodal data fusion**: Heterogeneous physical sensors (in-situ station observations, gridded atmospheric/oceanic reanalysis tensors e.g. ERA5, multi-spectral satellite imagery, seismic waveforms, textual field logs and storm reports).
- **Physical law integration**: Hard conservation constraints (mass, energy, vorticity), physics-informed loss functions, hybrid PDE-neural operator architectures.
- **Scientific reasoning LLMs**: Autonomous scientific discovery agents, tool-augmented climate assistants, and multi-step reasoning benchmarks (e.g. SciTS).

### 3.2 Taxonomy Framework (4 Core Dimensions)
```
                               Scientific Multimodal Time Series Foundation Models & Reasoning LLMs
                                                               │
     ┌─────────────────────────┼───────────────────────────────┴───────────────────────────────┐
     ▼                         ▼                               ▼                               ▼
[Dimension 1: Domain & Modality] [Dimension 2: Model Architecture] [Dimension 3: Physics Integration] [Dimension 4: Role of Reasoning LLMs]
 - Weather & Climate (ERA5, radar) - 3D Spherical/Spatial Transf.   - Purely Data-Driven              - Interface / Natural Lang. Query
 - Hydrology (streamflow, gauges)  - Neural Operators (FNO, SFNO)   - Physics-Informed Soft Losses   - Contextual Enhancer / Prefix
 - EO & Remote Sensing (SatMAE)   - Multi-scale Diffusion (GenCast) - Hard Conservation Constraints - Autonomous Tool-Using Agent
 - Geophysics & Seismology         - Graph Neural Networks (GraphCast) - Hybrid PDE-Neural Ensembles  - Multi-step Scientific Reasoner
 - Oceanography & Space Weather    - Cross-Modal Multimodal Tensors
```

### 3.3 Visual & Tabular Conventions
Following the rigorous standards of Jin et al.:
1. **Taxonomy Hierarchical Diagram**: Clear, publication-ready vector figure mapping scientific domains, data modalities, pretraining architectures, and downstream tasks.
2. **Domain $\times$ Modality Matrix**: Visual 2D heatmap showing where foundation models are mature (e.g. Gridded Weather) vs. sparse (e.g. Space Weather or Multimodal Hydrology).
3. **Timeline of Representative Scientific Foundation Models**: Milestone timeline from 2021 to 2026 tracing Pangu-Weather, GraphCast, ClimaX, FourCastNet, FuXi, FengWu, GenCast, Aurora, Prithvi WxC, etc.
4. **Standard Model Comparison Table**: Tabulating Model Name, Domain, Modalities, Pretraining Data (size/source), Spatial/Temporal Resolution, Physics Integration Level, Model Parameters, and Verified Code Repository.
5. **PRISMA 2020 Flow Diagram**: Explicit tracking of identification, screening, eligibility, and inclusion counts.

---

## 4. Verification and Anti-Hallucination Protocol
In strict adherence to `maintenance/COMMON_METHOD.md`:
- Every paper included in our analysis must have a recorded, authenticated API record from Crossref, arXiv, OpenAlex, or Semantic Scholar.
- Parameter counts, dataset hours, and lead times must be quoted directly from confirmed paper texts.
- All code repositories must be verified via GitHub API to ensure they are active and authentic.
