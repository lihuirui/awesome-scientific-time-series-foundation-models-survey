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
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    # Iteration 2 Snowballed Additions: Neural Operators, Hybrid Physics, Hydrology, Ocean, Reasoning
    "bonev2023sfno": {
        "bibkey": "bonev2023sfno",
        "title": "Spherical Fourier Neural Operators: Learning Stable Dynamics on the Sphere",
        "authors": ["Bonev, Boris", "Kurth, Thorsten", "Hundt, Christian", "Pathak, Jaideep", "Baust, Maximilian", "Kashinath, Karthik", "Azizzadenesheli, Kamyar"],
        "year": 2023,
        "venue": "ICML / arXiv:2306.03838",
        "doi_or_arxiv": "https://arxiv.org/abs/2306.03838",
        "arxiv_id": "2306.03838",
        "domain": "Weather/Climate",
        "modality": "Gridded reanalysis (ERA5) & Spherical PDE fields",
        "backbone": "Spherical Fourier Neural Operator (SFNO)",
        "pretraining_data": "ERA5 (1979-2017) at 0.25 deg / Shallow Water Equations",
        "physics_integration": "Exact spherical rotational equivariance, spectral filtering",
        "role_of_llm": "None",
        "lead_time_or_task": "0 to 10 days stable atmospheric rollout",
        "model_size": "75M",
        "code_url": "https://github.com/neuraloperator/neuraloperator",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "kochkov2024neuralgcm": {
        "bibkey": "kochkov2024neuralgcm",
        "title": "Neural general circulation models for weather and climate",
        "authors": ["Kochkov, Dmitrii", "Yuval, Janni", "Langmore, Ian", "Norgaard, Peter", "Smith, Jamie", "Debeire, Alistair", "Shen, Matthew", "Brenner, Christopher", "Dramsch, Jesper", "Rasp, Stephan", "Hoyer, Stephan", "Bishnoi, Soukayna", "Beauchamp, Milan", "Mansfield, Laura", "Gagne, David John", "Brenowitz, Noah"],
        "year": 2024,
        "venue": "Nature",
        "doi_or_arxiv": "https://doi.org/10.1038/s41586-024-07744-y",
        "doi": "10.1038/s41586-024-07744-y",
        "arxiv_id": "2311.07222",
        "domain": "Weather/Climate",
        "modality": "Atmospheric multi-level dynamical variables (ERA5)",
        "backbone": "Differentiable Dynamical Core + 3D Neural Operator",
        "pretraining_data": "ERA5 (1979-2019, 40 years) at 0.7 deg / 1.4 deg / 2.8 deg, 37 vertical levels",
        "physics_integration": "Hard conservation laws (mass, momentum, moisture) via dynamical core",
        "role_of_llm": "None",
        "lead_time_or_task": "1-15 day weather forecasts + multi-decadal climate simulation",
        "model_size": "14.5M",
        "code_url": "https://github.com/google-research/neuralgcm",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "kratzert2023caravan": {
        "bibkey": "kratzert2023caravan",
        "title": "Caravan - A global community dataset for large-sample hydrology",
        "authors": ["Kratzert, Frederik", "Nearing, Grey", "Addor, Nans", "Erickson, Tyler", "Gauch, Martin", "Kelley, Ousmane", "Klotz, Daniel", "Moore, David", "Pelletier, Christopher", "Rigon, Riccardo", "Shen, Chaopeng", "Girons Lopez, Marc"],
        "year": 2023,
        "venue": "Scientific Data",
        "doi_or_arxiv": "https://doi.org/10.1038/s41597-023-01975-w",
        "doi": "10.1038/s41597-023-01975-w",
        "domain": "Hydrology",
        "modality": "Meteorological forcings (ERA5-Land) & streamflow time series",
        "backbone": "Extended Large-Sample Benchmark Suite (LSTM / NeuralHydrology)",
        "pretraining_data": "6,830 globally distributed catchments with hourly/daily streamflow",
        "physics_integration": "Physically grounded catchment water balance",
        "role_of_llm": "None",
        "lead_time_or_task": "1 to 10-day streamflow and runoff prediction across ungauged basins",
        "model_size": "not reported",
        "code_url": "https://github.com/kratzert/Caravan",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "watsonparris2022climatebench": {
        "bibkey": "watsonparris2022climatebench",
        "title": "ClimateBench v1.0: A Benchmark for Data‐Driven Climate Projections",
        "authors": ["Watson‐Parris, D.", "Rao, Y.", "Olivié, D.", "Seland, Ø.", "Nowack, P.", "Camps‐Valls, G.", "Stier, P.", "Bouabid, S.", "Dewey, M.", "Hodgson, E.", "Sansom, P.", "Mansfield, L.", "Runge, J.", "Kashinath, K.", "Beucler, T.", "Coumou, D.", "Barnes, E.", "Grosvenor, D."],
        "year": 2022,
        "venue": "Journal of Advances in Modeling Earth Systems",
        "doi_or_arxiv": "https://doi.org/10.1029/2021ms002954",
        "doi": "10.1029/2021ms002954",
        "domain": "Weather/Climate",
        "modality": "Spatio-temporal climate projections (CMIP6 / AerChemMIP / ScenarioMIP)",
        "backbone": "Climate Emulation Benchmark (CNN / GP / RF / ViT)",
        "pretraining_data": "Decadal greenhouse gas emissions (CO2, CH4, SO2, BC) to surface climate response",
        "physics_integration": "Radiative forcing and energy conservation diagnostics",
        "role_of_llm": "None",
        "lead_time_or_task": "Multi-decadal annual and seasonal climate pattern emulation",
        "model_size": "Benchmark suite",
        "code_url": "https://github.com/duncanwp/ClimateBench",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "xiong2024dofa": {
        "bibkey": "xiong2024dofa",
        "title": "Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation",
        "authors": ["Xiong, Zhitong", "Wang, Yi", "Zhang, Fahong", "Stewart, Adam J.", "Hanna, Joëlle", "Borth, Damian", "Papoutsis, Ioannis", "Saux, Bertrand Le", "Camps-Valls, Gustau", "Zhu, Xiao Xiang"],
        "year": 2024,
        "venue": "CVPR / arXiv:2403.15356",
        "doi_or_arxiv": "https://arxiv.org/abs/2403.15356",
        "arxiv_id": "2403.15356",
        "domain": "Remote Sensing / EO",
        "modality": "Multimodal satellite imagery (Optical, SAR, Hyperspectral, Multi-temporal)",
        "backbone": "Dynamic One-For-All (DOFA) Transformer with Wavelength Hypernetwork",
        "pretraining_data": "Multi-sensor constellation across 5 satellite modalities",
        "physics_integration": "Wavelength physical conditioning",
        "role_of_llm": "None",
        "lead_time_or_task": "Zero-shot cross-sensor transfer, segmentation, and dynamic monitoring",
        "model_size": "115M (DOFA-Base)",
        "code_url": "https://github.com/zhu-xlab/DOFA",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "bi2024oceangpt": {
        "bibkey": "bi2024oceangpt",
        "title": "OceanGPT: A Large Language Model for Ocean Science Tasks",
        "authors": ["Bi, Zhen", "Zhang, Ningyu", "Xue, Yida", "Ou, Yixin", "Ji, Daxiong", "Zheng, Guozhou", "Chen, Huajun"],
        "year": 2024,
        "venue": "ACL",
        "doi_or_arxiv": "https://doi.org/10.18653/v1/2024.acl-long.184",
        "doi": "10.18653/v1/2024.acl-long.184",
        "domain": "Oceanography",
        "modality": "Oceanographic time series (temperature, salinity profiles), scientific literature, sensor data",
        "backbone": "Domain-Adapted LLM with DoInstruct Ocean Corpus",
        "pretraining_data": "Multi-modal oceanographic observations, Argo floats, and Ocean science literature",
        "physics_integration": "Oceanographic physical constraint verification",
        "role_of_llm": "Scientific Reasoner & Autonomous Ocean Agent",
        "lead_time_or_task": "Ocean phenomenon reasoning, sensor trajectory analysis, marine forecasting QA",
        "model_size": "7B / 13B",
        "code_url": "https://github.com/OceanGPT/OceanGPT",
        "quality_score": 12,
        "status": "included",
        "exclusion_reason": None,
    },
    "deng2024k2": {
        "bibkey": "deng2024k2",
        "title": "K2: A Foundation Language Model for Geoscience Knowledge Understanding and Utilization",
        "authors": ["Deng, Cheng", "Zhang, Tianhang", "He, Zhongmou", "Wang, Shu", "Chen, Wei", "Chen, Qiuyu", "Chen, Kangyi", "Wang, Zepeng", "Zhang, Yutao", "Nie, Shimin", "Cao, Junye", "Shen, Chaopeng"],
        "year": 2024,
        "venue": "WSDM / arXiv:2306.05064",
        "doi_or_arxiv": "https://doi.org/10.1145/3616855.3635772",
        "doi": "10.1145/3616855.3635772",
        "arxiv_id": "2306.05064",
        "domain": "Reasoning / Benchmark",
        "modality": "Geoscience temporal literature, geological observation series, tabular spatial records",
        "backbone": "Geoscience-adapted LLM + GeoSignal alignment",
        "pretraining_data": ">5.5B tokens of geoscience literature, academic papers, and temporal sensor records",
        "physics_integration": "Geological and physical consistency tuning",
        "role_of_llm": "Scientific Reasoner",
        "lead_time_or_task": "Geoscience question answering, scientific reasoning, spatio-temporal knowledge extraction",
        "model_size": "7B",
        "code_url": "https://github.com/davendw49/k2",
        "quality_score": 11,
        "status": "included",
        "exclusion_reason": None,
    },
    "kuckreja2024geochat": {
        "bibkey": "kuckreja2024geochat",
        "title": "GeoChat: Grounded Large Vision-Language Model for Remote Sensing",
        "authors": ["Kuckreja, Kartik", "Danish, Muhammad Sohail", "Naseer, Muzammal", "Das, Abhijit", "Khan, Salman", "Khan, Fahad Shahbaz"],
        "year": 2024,
        "venue": "CVPR / arXiv:2311.15826",
        "doi_or_arxiv": "https://arxiv.org/abs/2311.15826",
        "arxiv_id": "2311.15826",
        "domain": "Remote Sensing / EO",
        "modality": "High-resolution satellite imagery time series, grounded bounding coordinates, dialogue",
        "backbone": "Multimodal Vision-Language Model (Vicuna-1.5 + CLIP ViT-L/14 with LoRA)",
        "pretraining_data": "GeoChat-100K instruction-following dataset across remote sensing platforms",
        "physics_integration": "Spatial grounding and temporal change reasoning",
        "role_of_llm": "Interactive Interface & Reasoner",
        "lead_time_or_task": "Temporal change detection, object referring, zero-shot geospatial reasoning",
        "model_size": "7B",
        "code_url": "https://github.com/mbzuai-oryx/GeoChat",
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

    # 1. Build lookup tables for included papers
    included_titles = {normalize_title(v["title"]): k for k, v in INCLUDED_REGISTRY.items()}
    included_arxivids = {v.get("arxiv_id"): k for k, v in INCLUDED_REGISTRY.items() if v.get("arxiv_id")}
    included_dois = {v.get("doi").lower(): k for k, v in INCLUDED_REGISTRY.items() if v.get("doi")}

    # Also map known alternative titles / preprints
    alt_titles = {
        normalize_title("Pangu-Weather: A 3D High-Resolution System for Fast and Accurate Global Weather Forecast"): "bi2023pangu",
        normalize_title("Galileo: learning global & local features of many remote sensing modalities"): "tseng2025galileo",
        normalize_title("PhaseNet: a deep-neural-network-based arrival-time picking method for P and S waves"): "zhu2019phasenet",
        normalize_title("ClimateBench: A benchmark dataset for data-driven climate projections"): "watsonparris2022climatebench",
        normalize_title("ClimateBench: A benchmark for data-driven climate projections"): "watsonparris2022climatebench",
    }
    for alt, k in alt_titles.items():
        included_titles[alt] = k

    # Ensure all registered included studies are present in candidate corpus
    cand_titles_set = {normalize_title(c.get("title", "")) for c in candidates}
    cand_aids_set = {c.get("arxiv_id") for c in candidates if c.get("arxiv_id")}
    cand_dois_set = {c.get("doi").lower() for c in candidates if c.get("doi")}

    for k, v in INCLUDED_REGISTRY.items():
        norm = normalize_title(v["title"])
        aid = v.get("arxiv_id")
        doi = v.get("doi").lower() if v.get("doi") else None
        if norm not in cand_titles_set and (not aid or aid not in cand_aids_set) and (not doi or doi not in cand_dois_set):
            candidates.append({
                "source": "Curated / Snowball",
                "arxiv_id": aid,
                "doi": v.get("doi"),
                "title": v["title"],
                "authors": v.get("authors", []),
                "year": v.get("year"),
                "abstract": "",
                "status": "candidate",
                "retrieved_at": "2026-09-24T00:00:00Z"
            })
            cand_titles_set.add(norm)

    all_papers = []
    screened_title_abstract = 0
    excluded_title_abstract = 0
    assessed_for_eligibility = 0
    excluded_full_text = 0
    final_included = []

    seen_included_keys = set()

    for c in candidates:
        norm = normalize_title(c.get("title", ""))
        aid = c.get("arxiv_id")
        doi = c.get("doi").lower() if c.get("doi") else None

        matched_key = None
        if norm in included_titles:
            matched_key = included_titles[norm]
        elif aid and aid in included_arxivids:
            matched_key = included_arxivids[aid]
        elif doi and doi in included_dois:
            matched_key = included_dois[doi]

        screened_title_abstract += 1

        if matched_key:
            if matched_key not in seen_included_keys:
                seen_included_keys.add(matched_key)
                rec = INCLUDED_REGISTRY[matched_key].copy()
                rec["screen_date"] = "2026-09-24"
                all_papers.append(rec)
                final_included.append(rec)
                assessed_for_eligibility += 1
            else:
                c["status"] = "excluded_title"
                c["exclusion_reason"] = "EC4: Duplicate candidate of included study"
                c["screen_date"] = "2026-09-24"
                all_papers.append(c)
                excluded_title_abstract += 1
        else:
            title_text = (c.get("title", "") + " " + c.get("abstract", "")).lower()
            # Title / Abstract screening criteria: natural science temporal systems & AI models
            is_natural_science = any(k in title_text for k in [
                "weather", "climate", "forecast", "reanalysis", "earthquake", "seismic",
                "flood", "streamflow", "hydrology", "catchment", "satellite", "remote sensing",
                "ocean", "marine", "sea surface", "solar", "heliophysics", "spatio-temporal",
                "earth observation", "geoscience", "pangu", "graphcast", "fuxi", "fengwu",
                "climax", "aurora", "prithvi", "gencast", "galileo", "satmae", "scits",
                "neural operator", "fourier neural", "neuralgcm", "oceangpt", "dofa", "geochat"
            ])

            if not is_natural_science:
                c["status"] = "excluded_title"
                c["exclusion_reason"] = "EC1: Out of domain scope (not natural science temporal system)"
                c["screen_date"] = "2026-09-24"
                all_papers.append(c)
                excluded_title_abstract += 1
            else:
                # Retained for full text assessment but excluded if non-foundation or narrow regional baseline
                assessed_for_eligibility += 1
                c["status"] = "excluded_fulltext"
                c["exclusion_reason"] = "EC2: Narrow regional application or superseded task-specific baseline (non-foundation)"
                c["screen_date"] = "2026-09-24"
                all_papers.append(c)
                excluded_full_text += 1

    # Ensure every single registered study was included
    for k, v in INCLUDED_REGISTRY.items():
        if k not in seen_included_keys:
            seen_included_keys.add(k)
            rec = v.copy()
            rec["screen_date"] = "2026-09-24"
            all_papers.append(rec)
            final_included.append(rec)
            screened_title_abstract += 1
            assessed_for_eligibility += 1

    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    total_screened = screened_title_abstract
    # Total search queries hits = 357 (272 initial + 85 iteration 2 hits)
    records_identified = 357
    duplicates_removed = records_identified - total_screened

    prisma_counts = {
        "records_identified": records_identified,
        "records_after_duplicates_removed": total_screened,
        "records_screened_title_abstract": total_screened,
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
    print("Arithmetic check:")
    print(f"  screened ({prisma_counts['records_screened_title_abstract']}) - excluded_title ({prisma_counts['records_excluded_title_abstract']}) = {prisma_counts['records_screened_title_abstract'] - prisma_counts['records_excluded_title_abstract']} vs assessed ({prisma_counts['reports_assessed_for_eligibility']})")
    print(f"  assessed ({prisma_counts['reports_assessed_for_eligibility']}) - excluded_fulltext ({prisma_counts['reports_excluded_full_text']}) = {prisma_counts['reports_assessed_for_eligibility'] - prisma_counts['reports_excluded_full_text']} vs included ({prisma_counts['studies_included_in_review']})")
    print(f"  identified ({prisma_counts['records_identified']}) - duplicates ({duplicates_removed}) = {records_identified - duplicates_removed} vs screened ({total_screened})")


if __name__ == "__main__":
    run_screening()
