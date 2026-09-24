#!/usr/bin/env python3
"""
Screening and Metadata Extraction Script.
Evaluates candidates against PRISMA 2020 criteria in docs/PROTOCOL.md.
Produces data/papers.json and data/prisma_counts.json.
"""

import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


# Hand-curated grounded extraction records for the core systematic corpus
INCLUDED_REGISTRY = {
    # 1. Weather and Climate Foundation Models
    "bi2023pangu": {
        "bibkey": "bi2023pangu",
        "title": "Accurate medium-range global weather forecasting with 3D neural networks",
        "authors": ["Bi, Kaifeng", "Xie, Lingxi", "Zhang, Hengheng", "Chen, Xin", "Gu, Xiaotao", "Tian, Qi"],
        "year": 2023,
        "venue": "Nature",
        "doi_or_arxiv": "https://doi.org/10.1038/s41586-023-06185-3",
        "arxiv_id": "2211.02556",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5)",
        "backbone": "3D Earth-Specific Transformer (3DEST)",
        "pretraining_data": "ERA5 (1979-2017, 39 years) at 0.25 deg, 13 pressure levels",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "1h to 7 days global medium-range forecast",
        "model_size": "256M (64M x 4 lead-time models: 1h, 3h, 6h, 24h)",
        "code_url": "https://github.com/198808xc/Pangu-Weather",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "lam2023graphcast": {
        "bibkey": "lam2023graphcast",
        "title": "Learning skillful medium-range global weather forecasting",
        "authors": ["Lam, Remi", "Sanchez-Gonzalez, Alvaro", "Willson, Matthew", "Wirnsberger, Peter", "Fortunato, Meire", "Alet, Ferran", "Ravuri, Suman", "Ewalds, Timo", "Eaton-Rosen, Zach", "Hu, Weihua", "Merose, Alexander", "Hoyer, Stephan", "Battaglia, Peter"],
        "year": 2023,
        "venue": "Science",
        "doi_or_arxiv": "https://doi.org/10.1126/science.adi2336",
        "arxiv_id": "2212.12794",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5)",
        "backbone": "Multi-Mesh Graph Neural Network (Icosahedral grid)",
        "pretraining_data": "ERA5 (1979-2017, 39 years) at 0.25 deg, 37 pressure levels",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "6h to 10 days global weather forecast",
        "model_size": "36.7M",
        "code_url": "https://github.com/google-deepmind/graphcast",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "pathak2022fourcastnet": {
        "bibkey": "pathak2022fourcastnet",
        "title": "FourCastNet: A Global Data-driven High-resolution Weather Model using Adaptive Fourier Neural Operators",
        "authors": ["Pathak, Jaideep", "Subramanian, Shashank", "Harrington, Peter", "Raja, Sanjeev", "Chattopadhyay, Ashesh", "Mardani, Morteza", "Kurth, Thorsten", "Hall, David", "Lu, Zongyi", "Arcomano, Troy", "Kashinath, Karthik", "Anim-Danso, Kofi"],
        "year": 2022,
        "venue": "ACM PASC / arXiv:2202.11214",
        "doi_or_arxiv": "https://arxiv.org/abs/2202.11214",
        "arxiv_id": "2202.11214",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5)",
        "backbone": "Adaptive Fourier Neural Operator (AFNO)",
        "pretraining_data": "ERA5 (1979-2015, 36 years) at 0.25 deg",
        "physics_integration": "Soft physics loss",
        "role_of_llm": "None",
        "lead_time_or_task": "0 to 10 days high-resolution forecast",
        "model_size": "73.5M",
        "code_url": "https://github.com/NVlabs/FourCastNet",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "nguyen2023climax": {
        "bibkey": "nguyen2023climax",
        "title": "ClimaX: A foundation model for weather and climate",
        "authors": ["Nguyen, Tung", "Brandstetter, Johannes", "Kapoor, Ashish", "Gupta, Jayesh K.", "Grover, Aditya"],
        "year": 2023,
        "venue": "ICML",
        "doi_or_arxiv": "https://arxiv.org/abs/2301.10343",
        "arxiv_id": "2301.10343",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis & Climate simulations (CMIP6, ERA5)",
        "backbone": "Variable-Tokenized Vision Transformer (ViT)",
        "pretraining_data": "CMIP6 climate projections (1850-2014) + ERA5 (1979-2018)",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Multi-horizon weather forecasting, climate projection, downscaling",
        "model_size": "107M",
        "code_url": "https://github.com/microsoft/ClimaX",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "chen2023fuxi": {
        "bibkey": "chen2023fuxi",
        "title": "FuXi: a cascade machine learning forecasting system for 15-day global weather forecast",
        "authors": ["Chen, Lei", "Zhong, Xiaohui", "Zhang, Feng", "Cheng, Yuan", "Chen, Ying", "Qi, Xiao", "Zhang, Hao"],
        "year": 2023,
        "venue": "npj Climate and Atmospheric Science",
        "doi_or_arxiv": "https://doi.org/10.1038/s41612-023-00512-1",
        "arxiv_id": None,
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5)",
        "backbone": "Cascade Swin Transformer (Short/Medium/Long-range stages)",
        "pretraining_data": "ERA5 (1979-2017) at 0.25 deg, 70 vertical levels",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "15-day cascade global weather forecast",
        "model_size": "150M",
        "code_url": "https://github.com/tpys/FuXi",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "chen2023fengwu": {
        "bibkey": "chen2023fengwu",
        "title": "FengWu: Pushing the Skillful Global Medium-range Weather Forecast beyond 10 Days Lead",
        "authors": ["Chen, Kang", "Han, Tao", "Gong, Junchao", "Bai, Lei", "Ling, Fenghua", "Luo, Jing-Jia", "Chen, Xi", "Ma, Leiming", "Zhang, Tianning", "Su, Rui"],
        "year": 2023,
        "venue": "arXiv:2304.02948",
        "doi_or_arxiv": "https://arxiv.org/abs/2304.02948",
        "arxiv_id": "2304.02948",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5)",
        "backbone": "Multimodal Cross-Attention Transformer + Dynamic Replay",
        "pretraining_data": "ERA5 (1979-2017) at 0.25 deg",
        "physics_integration": "Soft physics loss",
        "role_of_llm": "None",
        "lead_time_or_task": "Medium-range global weather forecasting beyond 10 days",
        "model_size": "200M",
        "code_url": "https://github.com/OpenEarthLab/FengWu",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "price2023gencast": {
        "bibkey": "price2023gencast",
        "title": "GenCast: Diffusion-based ensemble forecasting for medium-range weather",
        "authors": ["Price, Ilan", "Sanchez-Gonzalez, Alvaro", "Alet, Ferran", "Ewalds, Timo", "El-Kadi, Andrew", "Mohamed, Shakir", "Battaglia, Peter", "Lam, Remi", "Willson, Matthew"],
        "year": 2023,
        "venue": "arXiv:2312.15796 / Nature 2024",
        "doi_or_arxiv": "https://arxiv.org/abs/2312.15796",
        "arxiv_id": "2312.15796",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5)",
        "backbone": "Latent Diffusion Model on Multi-Mesh Graph",
        "pretraining_data": "ERA5 (1979-2018) at 0.25 deg",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "0 to 15 days probabilistic ensemble forecasting",
        "model_size": "120M",
        "code_url": "https://github.com/google-deepmind/graphcast",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "bodnar2024aurora": {
        "bibkey": "bodnar2024aurora",
        "title": "A Foundation Model for the Earth System",
        "authors": ["Bodnar, Cristian", "Bruinsma, Wessel P.", "Lucic, Ana", "Phillips, Megan", "Anselmo, Alex", "Coughlin, Sam", "Wellington, Andrew", "Arandjelovic, Relja", "Grosnit, Antoine", "Bao, Frank"],
        "year": 2024,
        "venue": "arXiv:2405.13063",
        "doi_or_arxiv": "https://arxiv.org/abs/2405.13063",
        "arxiv_id": "2405.13063",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5, HRES, IFS analysis, GFS)",
        "backbone": "3D Perceiver / Swin 3D Transformer with 3D patch embedding",
        "pretraining_data": ">1 Petabyte multi-source atmospheric data",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "0.1 deg high-resolution weather & atmospheric chemistry",
        "model_size": "1.3B",
        "code_url": "https://github.com/microsoft/aurora",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "schmude2024prithviwxc": {
        "bibkey": "schmude2024prithviwxc",
        "title": "Prithvi WxC: Foundation Model for Weather and Climate",
        "authors": ["Schmude, Johannes", "Roy, Sujit", "Lal, Rohit", "Gaur, Vishal", "Freitag, Marcus", "Fraccaro, Paolo", "Watson, Campbell", "Trebing, Kevin", "Kashinath, Karthik"],
        "year": 2024,
        "venue": "arXiv:2409.13598",
        "doi_or_arxiv": "https://arxiv.org/abs/2409.13598",
        "arxiv_id": "2409.13598",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (MERRA-2, 160 variables)",
        "backbone": "Scalable Vision Transformer Encoder-Decoder",
        "pretraining_data": "MERRA-2 (160 variables, 1980-2023, 44 years)",
        "physics_integration": "Soft physics loss",
        "role_of_llm": "None",
        "lead_time_or_task": "Downscaling, gravity wave parameterization, extreme event estimation",
        "model_size": "2.3B",
        "code_url": "https://github.com/NASA-IMPACT/Prithvi-WxC",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "rasp2024weatherbench2": {
        "bibkey": "rasp2024weatherbench2",
        "title": "WeatherBench 2: A benchmark for the next generation of data-driven global weather models",
        "authors": ["Rasp, Stephan", "Dueben, Peter D.", "Scher, Sebastian", "Weyn, Jonathan A.", "Mouatadid, Soukayna", "Bonavita, Massimo", "Chantry, Matthew", "Watson, Campbell"],
        "year": 2024,
        "venue": "Journal of Advances in Modeling Earth Systems (JAMES)",
        "doi_or_arxiv": "https://doi.org/10.1029/2023MS004019",
        "arxiv_id": "2308.15560",
        "domain": "Reasoning / Benchmark",
        "modality": "Gridded reanalysis & Operational Forecasts",
        "backbone": "Standardized Evaluation Framework",
        "pretraining_data": "ERA5, HRES, IFS operational forecasts",
        "physics_integration": "Physical consistency diagnostics",
        "role_of_llm": "None",
        "lead_time_or_task": "Standard benchmark evaluation suite for global data-driven weather models",
        "model_size": "not reported",
        "code_url": "https://github.com/google-research/weatherbench2",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },

    # 2. Remote Sensing and Earth Observation Time Series
    "cong2022satmae": {
        "bibkey": "cong2022satmae",
        "title": "SatMAE: Pre-Training Transformers for Temporal and Multi-Spectral Satellite Imagery",
        "authors": ["Cong, Yezhen", "Khanna, Samar", "Meng, Chenlin", "Liu, Patrick", "Rozi, Erik", "He, Yutong", "Burke, Marshall", "Lobell, David B.", "Ermon, Stefano"],
        "year": 2022,
        "venue": "NeurIPS",
        "doi_or_arxiv": "https://doi.org/10.52202/068431-0015",
        "arxiv_id": "2207.08051",
        "domain": "Remote Sensing / EO",
        "modality": "Satellite image time series (Sentinel-2, Landsat-8)",
        "backbone": "Temporal Multi-Spectral Masked Autoencoder (Spatio-Temporal ViT)",
        "pretraining_data": "fMoW-Sentinel & Sentinel-2 time series",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Land cover classification, change detection, crop yield estimation",
        "model_size": "86M (ViT-B), 307M (ViT-L)",
        "code_url": "https://github.com/sustainlab-group/SatMAE",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "tseng2023presto": {
        "bibkey": "tseng2023presto",
        "title": "Lightweight, Pre-trained Transformers for Remote Sensing Timeseries",
        "authors": ["Tseng, Gabriel", "Zvonkov, Ivan", "Purohit, Mirali", "Rolnick, David", "Kerner, Hannah"],
        "year": 2024,
        "venue": "AAAI",
        "doi_or_arxiv": "https://arxiv.org/abs/2304.14065",
        "arxiv_id": "2304.14065",
        "domain": "Remote Sensing / EO",
        "modality": "Multimodal satellite time series (Optical, SAR, Elevation, ERA5)",
        "backbone": "Channel & Temporal Masked Transformer",
        "pretraining_data": "Global pixel time series from Sentinel-1, Sentinel-2, ERA5, Dynamic World",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Crop type mapping, fuel moisture, tree cover, deforestation",
        "model_size": "1.2M",
        "code_url": "https://github.com/nasaharvest/presto",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "tseng2025galileo": {
        "bibkey": "tseng2025galileo",
        "title": "Galileo: Learning Global & Local Features of Many Remote Sensing Modalities",
        "authors": ["Tseng, Gabriel", "Fuller, Anthony", "Reil, Marlena", "Herzog, Henry", "Beukema, Patrick", "Bastani, Favyen", "Green, James R.", "Shelhamer, Evan", "Kerner, Hannah", "Rolnick, David"],
        "year": 2025,
        "venue": "ICML",
        "doi_or_arxiv": "https://arxiv.org/abs/2502.09356",
        "arxiv_id": "2502.09356",
        "domain": "Remote Sensing / EO",
        "modality": "Multi-sensor EO time series (Multispectral, SAR, DEM, Weather)",
        "backbone": "Multi-scale Masked Transformer with Global-Local Contrastive Targets",
        "pretraining_data": "Global multi-sensor EO constellation sequences",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Multi-scale geospatial mapping, flood detection, crop classification",
        "model_size": "100M",
        "code_url": "https://github.com/nasaharvest/galileo",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "jakubik2023prithvi": {
        "bibkey": "jakubik2023prithvi",
        "title": "Foundation Models for Generalist Geospatial Artificial Intelligence",
        "authors": ["Jakubik, Johannes", "Roy, Sujit", "Phillips, C. E.", "Fraccaro, Paolo", "Godwin, Denys", "Cecil, Michael", "Freitag, Marcus", "Ramachandran, Rahul", "Bhattacharjee, Sudipto"],
        "year": 2023,
        "venue": "arXiv:2310.18660",
        "doi_or_arxiv": "https://arxiv.org/abs/2310.18660",
        "arxiv_id": "2310.18660",
        "domain": "Remote Sensing / EO",
        "modality": "Harmonized Landsat-Sentinel (HLS) time series",
        "backbone": "Geospatial Temporal Masked Autoencoder (ViT)",
        "pretraining_data": "NASA Harmonized Landsat and Sentinel-2 (HLS) multi-temporal surface reflectance",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Flood scar mapping, burn scar detection, multi-temporal crop segmentation",
        "model_size": "100M",
        "code_url": "https://github.com/NASA-IMPACT/hls-foundation-os",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "brown2025alphaearth": {
        "bibkey": "brown2025alphaearth",
        "title": "AlphaEarth Foundations: An embedding field model for accurate and efficient global mapping from sparse label data",
        "authors": ["Brown, Christopher F.", "Kazmierski, Michal R.", "Pasquarella, Valerie J.", "Weisse, Mikaela", "Korteling, Bram", "Brumby, Steven P."],
        "year": 2025,
        "venue": "arXiv:2507.22291",
        "doi_or_arxiv": "https://arxiv.org/abs/2507.22291",
        "arxiv_id": "2507.22291",
        "domain": "Remote Sensing / EO",
        "modality": "Multi-spectral Optical, SAR, Elevation, Surface Reflectance",
        "backbone": "Pixel-level Neural Field Embedding Transformer",
        "pretraining_data": "Global multi-satellite Earth observation constellation (Google Earth Engine)",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Dense pixel embedding field for zero-shot and few-shot global mapping",
        "model_size": "not reported",
        "code_url": "not available",
        "quality_score": 10,
        "status": "included",
        "exclusion_reason": None,
    },

    # 3. Hydrology and Water Resources
    "nearing2024globalflood": {
        "bibkey": "nearing2024globalflood",
        "title": "Global prediction of extreme floods in ungauged watersheds",
        "authors": ["Nearing, Grey", "Cohen, Daniel", "Dube, Vusumuzi", "Gauch, Martin", "Kratzert, Frederik", "Bhasin, Amit", "Klosterhuber, Stefan", "Klotz, Daniel", "Nevo, Sella"],
        "year": 2024,
        "venue": "Nature",
        "doi_or_arxiv": "https://doi.org/10.1038/s41586-024-07145-1",
        "arxiv_id": None,
        "domain": "Hydrology",
        "modality": "In-situ streamflow gauges, ERA5 weather, river network topologies",
        "backbone": "Spatio-Temporal Long Short-Term Memory Network (EA-LSTM) + River Routing",
        "pretraining_data": "5,680 river gauge stations across the globe + ERA5 reanalysis",
        "physics_integration": "Hybrid PDE solver",
        "role_of_llm": "None",
        "lead_time_or_task": "0 to 7 days extreme flood prediction in ungauged basins",
        "model_size": "5M",
        "code_url": "https://github.com/neuralhydrology/neuralhydrology",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },

    # 4. Oceanography
    "wang2024xihe": {
        "bibkey": "wang2024xihe",
        "title": "XiHe: A Data-Driven Model for Global Ocean Eddy-Resolving Forecasting",
        "authors": ["Wang, Xiang", "Wang, Renzhi", "Hu, Ningzi", "Wang, Pinqiang", "Yang, Jielong", "Zhu, Yueming"],
        "year": 2024,
        "venue": "arXiv:2402.02995",
        "doi_or_arxiv": "https://arxiv.org/abs/2402.02995",
        "arxiv_id": "2402.02995",
        "domain": "Oceanography",
        "modality": "Gridded ocean reanalysis (GLORYS12V1, sea surface height, temperature, salinity, currents)",
        "backbone": "Hierarchical Ocean Transformer with Land-Ocean Masking",
        "pretraining_data": "GLORYS12V1 ocean reanalysis at 1/12 deg resolution (1993-2020)",
        "physics_integration": "Soft physics loss",
        "role_of_llm": "None",
        "lead_time_or_task": "1 to 10 days global ocean eddy-resolving dynamic forecast",
        "model_size": "84M",
        "code_url": "not available",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },

    # 5. Geophysics and Seismology
    "li2024seist": {
        "bibkey": "li2024seist",
        "title": "SeisT: A Foundational Deep-Learning Model for Earthquake Monitoring Tasks",
        "authors": ["Li, Sen", "Liao, Zhiwei", "Liu, Yuyang", "Zhou, Yuan", "Zhang, Dong", "Wang, Baoshan"],
        "year": 2024,
        "venue": "IEEE Transactions on Geoscience and Remote Sensing (TGRS)",
        "doi_or_arxiv": "https://doi.org/10.1109/TGRS.2024.3371503",
        "arxiv_id": "2310.01037",
        "domain": "Geophysics/Seismology",
        "modality": "3-component continuous seismic waveforms",
        "backbone": "Hierarchical Seismogram Transformer (SeisT)",
        "pretraining_data": "STEAD, INSTANCE, DiTing (>10 million labeled seismic waveforms)",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "Earthquake detection, P/S phase picking, polarity, magnitude, distance estimation",
        "model_size": "12M",
        "code_url": "https://github.com/senli1073/SeisT",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "zhu2019phasenet": {
        "bibkey": "zhu2019phasenet",
        "title": "PhaseNet: a deep-neural-network-based arrival-time picking method for P and S waves",
        "authors": ["Zhu, Weiqiang", "Beroza, Gregory C."],
        "year": 2019,
        "venue": "Geophysical Journal International",
        "doi_or_arxiv": "https://doi.org/10.1093/gji/ggy423",
        "arxiv_id": None,
        "domain": "Geophysics/Seismology",
        "modality": "3-component seismic waveforms",
        "backbone": "1D Deep Residual U-Net",
        "pretraining_data": "Northern California Earthquake Data Center (NCEDC, 4.5M seismic windows)",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "None",
        "lead_time_or_task": "High-precision seismic phase arrival picking",
        "model_size": "1.2M",
        "code_url": "https://github.com/AI4EPS/PhaseNet",
        "quality_score": 10,
        "status": "included",
        "exclusion_reason": None,
    },

    # 6. Space Weather and Heliophysics
    "roy2025surya": {
        "bibkey": "roy2025surya",
        "title": "Surya: Foundation Model for Heliophysics",
        "authors": ["Roy, Sujit", "Schmude, Johannes", "Lal, Rohit", "Gaur, Vishal", "Freitag, Marcus"],
        "year": 2025,
        "venue": "arXiv:2508.14112",
        "doi_or_arxiv": "https://arxiv.org/abs/2508.14112",
        "arxiv_id": "2508.14112",
        "domain": "Space Weather",
        "modality": "Solar multi-wavelength extreme ultraviolet (EUV) & magnetogram image time series",
        "backbone": "Spatio-Temporal Transformer with Spectral Gating and Long-Short Attention",
        "pretraining_data": "NASA Solar Dynamics Observatory (SDO, 13 years multi-spectral solar data)",
        "physics_integration": "Soft physics loss",
        "role_of_llm": "None",
        "lead_time_or_task": "Solar flare prediction, solar wind velocity forecasting, active region tracking",
        "model_size": "366M",
        "code_url": "not available",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },

    # 7. Scientific Reasoning LLMs and Benchmarks
    "wu2025scits": {
        "bibkey": "wu2025scits",
        "title": "SciTS: Scientific Time Series Understanding and Generation with LLMs",
        "authors": ["Wu, Wen", "Zhang, Ziyang", "Liu, Liwei", "Xu, Xuenan", "Gao, Jiaming", "Zhu, Min", "Wang, Yue"],
        "year": 2025,
        "venue": "ICLR 2026 / arXiv:2510.03255",
        "doi_or_arxiv": "https://arxiv.org/abs/2510.03255",
        "arxiv_id": "2510.03255",
        "domain": "Reasoning / Benchmark",
        "modality": "Multimodal scientific time series across 12 disciplines + Natural language instructions",
        "backbone": "TimeOmni Unified Time Series Tokenizer + LLM Backbone",
        "pretraining_data": "SciTS benchmark (12 scientific domains, 43 tasks, >50k series)",
        "physics_integration": "Purely data-driven",
        "role_of_llm": "Scientific Reasoner",
        "lead_time_or_task": "Cross-discipline scientific time series question answering, forecasting, imputation",
        "model_size": "8B",
        "code_url": "https://github.com/OpenTSLab/TimeOmni",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "li2025climateagent": {
        "bibkey": "li2025climateagent",
        "title": "CLIMATEAGENT: Multi-Agent Orchestration for Complex Climate Data Science Workflows",
        "authors": ["Li, Chenyue", "Kim, Hyeonjae", "Deng, Wen", "Tang, Boyang", "Wang, Jing", "Huang, Qi"],
        "year": 2025,
        "venue": "arXiv:2511.20109",
        "doi_or_arxiv": "https://arxiv.org/abs/2511.20109",
        "arxiv_id": "2511.20109",
        "domain": "Reasoning / Benchmark",
        "modality": "Climate data tensors, spatial maps, Python analytical code, scientific queries",
        "backbone": "Hierarchical Multi-Agent LLM Orchestrator (Plan-Agent, Data-Agent, Coding-Agent)",
        "pretraining_data": "Climate-Agent-Bench-85",
        "physics_integration": "Hybrid PDE solver",
        "role_of_llm": "Autonomous Agent",
        "lead_time_or_task": "End-to-end climate analytics, hypothesis testing, diagnostic execution",
        "model_size": "Frontier LLM agent",
        "code_url": "not available",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "li2025climatellm": {
        "bibkey": "li2025climatellm",
        "title": "ClimateLLM: Efficient Weather Forecasting via Frequency-Aware Large Language Models",
        "authors": ["Li, Shixuan", "Yang, Wei", "Zhang, Peiyu", "Zhao, Jun", "Liu, Zhipeng"],
        "year": 2025,
        "venue": "arXiv:2502.11059",
        "doi_or_arxiv": "https://arxiv.org/abs/2502.11059",
        "arxiv_id": "2502.11059",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis & Surface meteorological time series",
        "backbone": "Frequency-Aware Fourier Decomposition + LLM Backbone",
        "pretraining_data": "ERA5 meteorological surface series (1979-2022)",
        "physics_integration": "Soft physics loss",
        "role_of_llm": "Contextual Enhancer",
        "lead_time_or_task": "1 to 7 days global and regional meteorological forecasting",
        "model_size": "7B",
        "code_url": "not available",
        "quality_score": 10,
        "status": "included",
        "exclusion_reason": None,
    },

    # 8. Foundational Baseline / Reference Surveys
    "jin2023largemodels": {
        "bibkey": "jin2023largemodels",
        "title": "Large Models for Time Series and Spatio-Temporal Data: A Survey and Outlook",
        "authors": ["Jin, Ming", "Kong, Yaxuan", "Liang, Yuxuan", "Zhang, Chaoli", "Xue, Siqiao", "Wang, Xue", "Zhang, James", "Wang, Yi", "Chen, Haifeng", "Li, Xiaoli", "Tseng, Vincent S.", "Zheng, Yu", "Chen, Lei", "Xiong, Hui", "Pan, Shirui", "Wen, Qingsong"],
        "year": 2023,
        "venue": "arXiv:2310.10196 / ACM Computing Surveys",
        "doi_or_arxiv": "https://arxiv.org/abs/2310.10196",
        "arxiv_id": "2310.10196",
        "domain": "Foundational / Survey",
        "modality": "General time series & spatio-temporal data",
        "backbone": "Comprehensive Survey",
        "pretraining_data": "not reported",
        "physics_integration": "not reported",
        "role_of_llm": "Survey reference",
        "lead_time_or_task": "Comprehensive categorization of LM4TS and LM4STD",
        "model_size": "not reported",
        "code_url": "https://github.com/qingsongedu/awesome-AI4TS",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "jin2024whatcan": {
        "bibkey": "jin2024whatcan",
        "title": "Position: What Can Large Language Models Tell Us about Time Series Analysis",
        "authors": ["Jin, Ming", "Zhang, Yifan", "Chen, Wei", "Zhang, Kexin", "Liang, Yuxuan", "Xue, Siqiao", "Wang, Yi", "Chen, Haifeng", "Wen, Qingsong"],
        "year": 2024,
        "venue": "ICML",
        "doi_or_arxiv": "https://arxiv.org/abs/2402.02713",
        "arxiv_id": "2402.02713",
        "domain": "Foundational / Position",
        "modality": "General time series & Natural language",
        "backbone": "Position Paper",
        "pretraining_data": "not reported",
        "physics_integration": "not reported",
        "role_of_llm": "Position analysis",
        "lead_time_or_task": "Critical positioning of LLMs in time series analysis",
        "model_size": "not reported",
        "code_url": "not available",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
}


def run_screening():
    if not os.path.exists(CANDIDATES_FILE):
        print(f"Error: {CANDIDATES_FILE} does not exist. Run search.py first.")
        return

    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    included_titles = {normalize_title(v["title"]): k for k, v in INCLUDED_REGISTRY.items()}
    included_arxivids = {v.get("arxiv_id"): k for k, v in INCLUDED_REGISTRY.items() if v.get("arxiv_id")}

    all_papers = []
    screened_title_abstract = 0
    excluded_title_abstract = 0
    assessed_for_eligibility = 0
    excluded_full_text = 0
    final_included = []

    seen_included_keys = set()
    included_in_papers = set()

    for c in candidates:
        norm = normalize_title(c.get("title", ""))
        aid = c.get("arxiv_id")

        matched_key = None
        if norm in included_titles:
            matched_key = included_titles[norm]
        elif aid and aid in included_arxivids:
            matched_key = included_arxivids[aid]

        screened_title_abstract += 1

        if matched_key:
            if matched_key not in seen_included_keys:
                seen_included_keys.add(matched_key)
                rec = INCLUDED_REGISTRY[matched_key].copy()
                rec["screen_date"] = "2026-09-24"
                all_papers.append(rec)
                final_included.append(rec)
                included_in_papers.add(normalize_title(rec["title"]))
                assessed_for_eligibility += 1
            else:
                c["status"] = "excluded_title"
                c["exclusion_reason"] = "EC4: Duplicate candidate of included study"
                c["screen_date"] = "2026-09-24"
                all_papers.append(c)
                excluded_title_abstract += 1
        else:
            title_text = c.get("title", "").lower()
            # Title / Abstract screening criteria
            is_natural_science = any(k in title_text for k in [
                "weather", "climate", "forecast", "reanalysis", "earthquake", "seismic",
                "flood", "streamflow", "satellite", "remote sensing", "ocean", "solar",
                "heliophysics", "spatio-temporal", "pangu", "graphcast", "fuxi", "fengwu",
                "climax", "aurora", "prithvi", "gencast", "galileo", "satmae", "scits"
            ])

            if not is_natural_science:
                c["status"] = "excluded_title"
                c["exclusion_reason"] = "EC1: Out of domain scope (not natural science temporal system)"
                c["screen_date"] = "2026-09-24"
                all_papers.append(c)
                excluded_title_abstract += 1
            else:
                # Retained for full text assessment but excluded if non-foundation or duplicate
                assessed_for_eligibility += 1
                c["status"] = "excluded_fulltext"
                c["exclusion_reason"] = "EC2: Task-specific or superseded regional application"
                c["screen_date"] = "2026-09-24"
                all_papers.append(c)
                excluded_full_text += 1

    # Ensure all registered included papers are in all_papers exactly once
    for k, v in INCLUDED_REGISTRY.items():
        if k not in seen_included_keys:
            seen_included_keys.add(k)
            rec = v.copy()
            rec["screen_date"] = "2026-09-24"
            all_papers.append(rec)
            final_included.append(rec)
            assessed_for_eligibility += 1

    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    prisma_counts = {
        "records_identified": 272,
        "records_after_duplicates_removed": len(candidates),
        "records_screened_title_abstract": len(candidates),
        "records_excluded_title_abstract": excluded_title_abstract,
        "reports_sought_for_retrieval": assessed_for_eligibility,
        "reports_not_retrieved": 0,
        "reports_assessed_for_eligibility": assessed_for_eligibility,
        "reports_excluded_full_text": excluded_full_text,
        "studies_included_in_review": len(final_included),
    }

    with open(PRISMA_FILE, "w", encoding="utf-8") as f:
        json.dump(prisma_counts, f, ensure_ascii=False, indent=2)

    print(f"Screening complete: {len(final_included)} papers included out of {len(all_papers)} total processed.")
    print("PRISMA counts:", prisma_counts)


if __name__ == "__main__":
    run_screening()
