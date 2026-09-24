# Project brief: Survey of Scientific Multimodal Time Series Foundation Models and Scientific Reasoning Time Series LLMs

- Local folder: `/workspace/survey-sci-ts` · GitHub repo: `lihuirui/awesome-scientific-time-series-foundation-models-survey`
- Working title: "Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey"
- Scope, 2021–present, natural-science domains: weather and climate (e.g. Pangu-Weather, GraphCast, FourCastNet, FuXi,
  FengWu, GenCast, Aurora, ClimaX, Prithvi WxC), hydrology (streamflow, floods, drought), environment and air quality,
  oceanography, geography and Earth observation / remote-sensing image time series (e.g. Prithvi, SatMAE, Presto, Galileo,
  AlphaEarth-style embeddings where a paper exists), seismology and geophysics (earthquake detection/phase picking,
  seismic foundation models), ecology/biodiversity, space weather and astronomy time series, energy/geo-energy where
  physically grounded. Plus scientific reasoning LLMs / agents over time series and spatio-temporal data (LLM agents for
  climate/earth science, time series reasoning benchmarks in science, e.g. SciTS). Verify each named example; drop any
  that cannot be verified.
- Suggested RQs: which scientific data modalities (station series, gridded reanalysis, satellite image time series,
  waveforms, text reports) are combined and how; foundation-model pretraining data (e.g. ERA5) and objectives; physics
  integration (physics-informed losses, hybrid models, conservation constraints); spatio-temporal architectures (graph,
  3D transformer, neural operator, diffusion); uncertainty quantification; evaluation protocols (WeatherBench 2 etc.);
  how LLMs reason about scientific time series; data, compute and trust gaps.
- Taxonomy seeds: by scientific domain × data modality; by model family; by role of LLM (interface, reasoner, agent,
  tool user); by physics integration level.
- Extra figures: domain × modality heatmap; timeline of weather/climate foundation models; spatial resolution vs. lead
  time (only stated values); model-size vs. training-data table.
- Coordinate with, but do not duplicate, Jin et al.'s spatio-temporal coverage: this survey is domain-science focused.


## Iteration 2 focus (read docs/STATE.md first)
Prioritize the Top-3 backlog in `docs/STATE.md`. Persistent weakness: **Depth of Analysis** (3.5/5).
1. Extract WeatherBench 2 / ClimateBench quantitative scores (Z500, T850 RMSE vs HRES) only from verified sources into a results table.
2. Forward/backward snowball Pangu-Weather, GraphCast, Aurora, Galileo, SciTS; strengthen hydrology and oceanography.
3. Deepen Sections 4 & 6 (SFNO / conservation constraints; scientific reasoning LLM agents).
Stay within ~90 minutes; pass `make check`; commit and push; print Chinese report.
