#!/usr/bin/env python3
"""
Publication-Quality Figure Generation Script for Scientific Multimodal Time Series Survey.
Generates:
1. PRISMA 2020 Flow Diagram (prisma_flow.png, .pdf)
2. Hierarchical Taxonomy Tree (taxonomy_tree.png, .pdf)
3. Domain x Modality Heatmap (domain_modality_heatmap.png, .pdf)
4. Milestone Timeline of Weather/Climate Foundation Models (weather_foundation_timeline.png, .pdf)
5. Spatial Resolution vs. Lead Time (resolution_vs_leadtime.png, .pdf)
6. Annual Publications by Domain (publications_by_year.png, .pdf)
"""

import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
FIG_DIR = os.path.join(BASE_DIR, "paper", "figures")

os.makedirs(FIG_DIR, exist_ok=True)

# Academic styling
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 13,
})


def plot_prisma_flow():
    with open(PRISMA_FILE, "r", encoding="utf-8") as f:
        counts = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_box(x, y, w, h, text, title=None, facecolor="#F0F4F8", edgecolor="#1E3A8A"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=1.5,rounding_size=2.0",
            facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5
        )
        ax.add_patch(rect)
        if title:
            ax.text(x + w / 2, y + h - 4, title, ha="center", va="top",
                    fontsize=10.5, fontweight="bold", color="#0F172A")
            ax.text(x + w / 2, y + (h - 6) / 2, text, ha="center", va="center",
                    fontsize=9.5, color="#1E293B", multialignment="center")
        else:
            ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=9.5, color="#1E293B", multialignment="center")

    def draw_arrow(x1, y1, x2, y2, color="#475569"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8, mutation_scale=14))

    # Phase Headers on Left
    phases = [
        ("Identification", 85, "#2563EB"),
        ("Screening", 57, "#0D9488"),
        ("Eligibility", 32, "#D97706"),
        ("Included", 9, "#16A34A")
    ]
    for name, y_pos, col in phases:
        rect = patches.FancyBboxPatch(
            (2, y_pos - 4), 16, 8,
            boxstyle="round,pad=1.0,rounding_size=2.0",
            facecolor=col, edgecolor="none"
        )
        ax.add_patch(rect)
        ax.text(10, y_pos, name, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="white", rotation=0)

    # 1. Identification Box
    draw_box(24, 78, 48, 14,
             f"Databases & APIs queried:\nCrossref & arXiv API (n = {counts['records_identified']})",
             "Records Identified")
    draw_arrow(48, 78, 48, 67)

    # Duplicates removed note
    ax.text(50, 72.5, f"Deduplicated\n(n = {counts['records_identified'] - counts['records_after_duplicates_removed']} removed)",
            fontsize=8.5, color="#64748B", ha="left")

    # 2. Screening Box
    draw_box(24, 51, 38, 14,
             f"Records screened by title\nand abstract (n = {counts['records_screened_title_abstract']})",
             "Screening")

    # Excluded Title/Abstract
    draw_arrow(62, 58, 74, 58, color="#DC2626")
    draw_box(75, 51, 23, 14,
             f"Irrelevant scope\n(n = {counts['records_excluded_title_abstract']})",
             "Excluded (Title/Abs)", facecolor="#FEF2F2", edgecolor="#DC2626")

    draw_arrow(43, 51, 43, 40)

    # 3. Eligibility Box
    draw_box(24, 25, 38, 14,
             f"Full-text articles assessed\nfor eligibility (n = {counts['reports_assessed_for_eligibility']})",
             "Eligibility Assessment")

    # Excluded Full-Text
    draw_arrow(62, 32, 74, 32, color="#DC2626")
    draw_box(75, 25, 23, 14,
             f"Regional/narrow\napplication (n = {counts['reports_excluded_full_text']})",
             "Excluded (Full-Text)", facecolor="#FEF2F2", edgecolor="#DC2626")

    draw_arrow(43, 25, 43, 15)

    # 4. Included Box
    draw_box(24, 2, 38, 13,
             f"Studies included in systematic review\n(n = {counts['studies_included_in_review']})",
             "Included Corpus", facecolor="#F0FDF4", edgecolor="#16A34A")

    plt.title("PRISMA 2020 Systematic Review Flow Diagram", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "prisma_flow.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "prisma_flow.pdf"))
    plt.close()
    print("Generated prisma_flow.png/.pdf")


def plot_taxonomy_tree():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def box(x, y, w, h, text, subtext="", bg="#F8FAFC", border="#334155", textcol="#0F172A"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=1.0,rounding_size=2.0",
            facecolor=bg, edgecolor=border, linewidth=1.5
        )
        ax.add_patch(rect)
        if subtext:
            ax.text(x + w / 2, y + h - 2.8, text, ha="center", va="top",
                    fontsize=9.5, fontweight="bold", color=textcol)
            ax.text(x + w / 2, y + 2.2, subtext, ha="center", va="bottom",
                    fontsize=7.8, color="#475569", multialignment="center")
        else:
            ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=textcol, multialignment="center")

    def connect(x1, y1, x2, y2, color="#94A3B8"):
        ax.plot([x1, x2], [y1, y2], color=color, lw=1.5, zorder=1)

    # Root Box
    root_x, root_y, root_w, root_h = 25, 87, 50, 9
    box(root_x, root_y, root_w, root_h,
        "Scientific Multimodal Time Series Foundation Models & Reasoning LLMs",
        "A Systematic Domain-Science Taxonomy Framework",
        bg="#1E3A8A", border="#1E40AF", textcol="white")

    # 4 Main Pillar Categories
    pillars = [
        ("Scientific Domains & Modalities", 12.5, "#DBEAFE", "#2563EB", [
            ("Weather & Climate", "ERA5, MERRA-2, Radar\n(Pangu, GraphCast, Aurora, NeuralGCM)"),
            ("Earth Observation & RS", "Multispectral, SAR, DEM\n(SatMAE, Presto, Galileo, DOFA)"),
            ("Hydrology & Oceans", "River gauges, GLORYS12\n(GlobalFlood, Caravan, XiHe, OceanGPT)"),
            ("Geophysics & Space", "Waveforms, SDO UV series\n(SeisT, Surya)")
        ]),
        ("Foundation Architectures", 37.5, "#DCFCE7", "#16A34A", [
            ("3D Spatial Transformers", "3D Swin, 3DEST, Perceiver\n(Pangu, Aurora)"),
            ("Multi-Mesh Graph Neural Nets", "Icosahedral spherical mesh\n(GraphCast, GenCast)"),
            ("Continuous Neural Operators", "AFNO, SFNO, Fourier Spec.\n(FourCastNet, SFNO)"),
            ("Multimodal Masked Encoders", "Temporal-spectral masking\n(SatMAE, Presto, Galileo, DOFA)")
        ]),
        ("Physics Integration Levels", 62.5, "#FEF3C7", "#D97706", [
            ("Purely Data-Driven", "Statistical auto-regression\n(Standard Vision Transformers)"),
            ("Soft Physics Loss Penalties", "Conservation & dynamic loss\n(FengWu, FourCastNet, SFNO)"),
            ("Hard Architectural Constraints", "Inherent symmetry & projection\n(Spherical Harmonics, Invariance)"),
            ("Hybrid PDE-Neural Solvers", "Coupled numerical solvers\n(NeuralGCM, GlobalFlood, Caravan)")
        ]),
        ("Roles of Reasoning LLMs", 87.5, "#F3E8FF", "#9333EA", [
            ("Scientific Reasoner", "Cross-domain time series QA\n(SciTS, TimeOmni, K2, OceanGPT)"),
            ("Contextual Enhancer", "Domain priors & text prefixes\n(ClimateLLM)"),
            ("Autonomous Scientific Agent", "Multi-step tool orchestration\n(ClimateAgent)"),
            ("Interactive Grounded Interface", "Multimodal chat & change reasoning\n(GeoChat)")
        ])
    ]

    col_w = 21
    for title, x_center, col_bg, col_border, leaves in pillars:
        x_col = x_center - col_w / 2
        # Connect Root to Pillar Header
        connect(root_x + root_w / 2, root_y, x_center, 77)

        # Pillar Header Box
        box(x_col, 68, col_w, 8, title, bg=col_bg, border=col_border, textcol=col_border)

        # Connect Pillar to Leaves
        y_curr = 53
        for leaf_title, leaf_desc in leaves:
            connect(x_center, 68, x_center, y_curr + 6)
            box(x_col, y_curr, col_w, 10, leaf_title, leaf_desc, bg="white", border=col_border)
            y_curr -= 13.5

    plt.title("Taxonomy Tree: Categorization of Scientific Multimodal Time Series Foundation Models",
              fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "taxonomy_tree.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "taxonomy_tree.pdf"))
    plt.close()
    print("Generated taxonomy_tree.png/.pdf")


def plot_domain_modality_heatmap():
    domains = [
        "Weather & Climate",
        "Earth Observation / RS",
        "Hydrology & Floods",
        "Oceanography",
        "Geophysics / Seismology",
        "Space Weather / Solar",
        "Reasoning Benchmarks"
    ]

    modalities = [
        "Gridded Reanalysis\n(ERA5 / MERRA)",
        "Satellite Imagery\n(Multi-Spectral / SAR)",
        "Station & Gauge\nTime Series",
        "Continuous\nWaveforms",
        "Scientific Text &\nObservation Reports"
    ]

    # Matrix values representing research maturity / paper count
    # 0 = Unexplored, 1 = Emerging, 2 = Growing, 3 = Highly Mature
    data = np.array([
        [3, 2, 2, 0, 1],  # Weather/Climate
        [1, 3, 0, 0, 1],  # Remote Sensing
        [2, 1, 3, 0, 1],  # Hydrology
        [3, 1, 1, 0, 0],  # Oceanography
        [0, 0, 1, 3, 0],  # Geophysics
        [2, 3, 1, 0, 1],  # Space Weather
        [2, 2, 3, 2, 3],  # Reasoning Benchmarks
    ])

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    cax = ax.imshow(data, cmap="Blues", aspect="auto", vmin=0, vmax=3)

    ax.set_xticks(range(len(modalities)))
    ax.set_xticklabels(modalities, rotation=20, ha="right", fontsize=9.5)
    ax.set_yticks(range(len(domains)))
    ax.set_yticklabels(domains, fontsize=10)

    # Annotate cells
    labels = {
        0: "Unexplored",
        1: "Emerging",
        2: "Active",
        3: "Mature / Core"
    }

    for i in range(len(domains)):
        for j in range(len(modalities)):
            val = data[i, j]
            text_color = "white" if val >= 2 else "#1E293B"
            ax.text(j, i, f"{val}\n({labels[val]})", ha="center", va="center",
                    color=text_color, fontsize=8.5, fontweight="bold" if val >= 2 else "normal")

    cbar = fig.colorbar(cax, ticks=[0, 1, 2, 3], shrink=0.8)
    cbar.ax.set_yticklabels(["0 (Unexplored)", "1 (Emerging)", "2 (Active)", "3 (Mature)"])

    plt.title("Domain × Modality Research Maturity Matrix", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "domain_modality_heatmap.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "domain_modality_heatmap.pdf"))
    plt.close()
    print("Generated domain_modality_heatmap.png/.pdf")


def plot_weather_foundation_timeline():
    milestones = [
        ("FourCastNet", "2022-02", "AFNO Operator", 2022.15, 1.4, "#2563EB"),
        ("SatMAE", "2022-07", "Temporal ViT MAE", 2022.55, -1.5, "#0D9488"),
        ("Pangu-Weather", "2022-11", "3D Earth Swin", 2022.88, 2.5, "#DC2626"),
        ("GraphCast", "2022-12", "Multi-Mesh GNN", 2022.98, -2.6, "#D97706"),
        ("ClimaX", "2023-01", "Variable ViT", 2023.08, 1.3, "#7C3AED"),
        ("Presto", "2023-04", "Lightweight EO", 2023.3, -1.4, "#059669"),
        ("SFNO", "2023-06", "Spherical Operator", 2023.45, 2.7, "#10B981"),
        ("ClimSim", "2023-06", "Subgrid Physics", 2023.50, -2.5, "#6366F1"),
        ("SEEDS", "2023-06", "Diffusion Ensembles", 2023.55, 1.6, "#DC2626"),
        ("FuXi", "2023-06", "Cascade Swin", 2023.60, -1.6, "#E11D48"),
        ("WeatherBench 2", "2023-08", "Evaluation Suite", 2023.68, 2.6, "#475569"),
        ("Prithvi-100M", "2023-10", "Geospatial ViT", 2023.82, -2.7, "#0D9488"),
        ("GenCast", "2023-12", "Diffusion Ensemble", 2023.95, 1.4, "#DC2626"),
        ("Stormer", "2023-12", "Random Patch ViT", 2023.98, -1.4, "#B45309"),
        ("SkySense", "2023-12", "1.9B Multi-Modal", 2023.96, 2.3, "#0D9488"),
        ("FengWu-4DVar", "2023-12", "Neural 4D-Var", 2023.97, -2.1, "#7C3AED"),
        ("DiffDA", "2024-01", "Diffusion DA", 2024.06, -1.3, "#DC2626"),
        ("Time-LLM", "2023-10", "Reprogrammed LLM", 2023.80, 1.4, "#2563EB"),
        ("FuXi-Extreme", "2023-10", "Extreme Diffusion", 2023.85, -1.8, "#DC2626"),
        ("MOMENT", "2024-02", "Open TS Foundation", 2024.12, 2.5, "#059669"),
        ("UniTS", "2024-03", "Unified Multi-Task", 2024.20, -2.4, "#7C3AED"),
        ("Chronos", "2024-03", "Quantized LM TS", 2024.22, 1.6, "#D97706"),
        ("DOFA", "2024-03", "Plasticity EO", 2024.25, 1.3, "#B45309"),
        ("GlobalFlood", "2024-03", "Ungauged Flood AI", 2024.28, -1.5, "#0284C7"),
        ("Aurora", "2024-05", "1.3B 3D Perceiver", 2024.40, 2.7, "#7C3AED"),
        ("AIFS", "2024-06", "ECMWF GNN-Transformer", 2024.48, 1.5, "#0D9488"),
        ("NeuralGCM", "2024-07", "Hybrid PDE-AI", 2024.55, -2.6, "#6366F1"),
        ("OceanGPT", "2024-08", "Ocean Science LLM", 2024.62, 1.5, "#0891B2"),
        ("Prithvi WxC", "2024-09", "2.3B Climate Model", 2024.72, 2.8, "#D97706"),
        ("Galileo", "2025-02", "Multi-Scale EO", 2025.15, -1.8, "#059669"),
        ("OceanBench", "2025-05", "Ocean Dynamics Bench", 2025.40, -2.7, "#0284C7"),
        ("SciTS", "2025-10", "Scientific TS LLM", 2025.80, 1.6, "#2563EB"),
    ]

    fig, ax = plt.subplots(figsize=(15, 7.5), dpi=300)

    # Base timeline axis
    ax.axhline(0, color="#334155", lw=2.5, zorder=1)
    ax.set_xlim(2021.8, 2026.2)
    ax.set_ylim(-3.9, 4.3)
    ax.axis("off")

    years = [2022, 2023, 2024, 2025, 2026]
    for yr in years:
        ax.plot([yr, yr], [-0.3, 0.3], color="#0F172A", lw=2)
        ax.text(yr, -0.6, str(yr), ha="center", va="top", fontsize=11, fontweight="bold", color="#0F172A")

    for name, date_str, arch, x_val, y_lvl, c in milestones:
        # Stem line
        ax.plot([x_val, x_val], [0, y_lvl], color=c, lw=1.2, linestyle="--", alpha=0.8, zorder=2)
        ax.scatter([x_val], [0], color=c, s=36, zorder=3)

        # Tag
        bbox_props = dict(boxstyle="round,pad=0.32,rounding_size=0.3", facecolor="white", edgecolor=c, lw=1.3)
        va = "bottom" if y_lvl > 0 else "top"
        ax.text(x_val, y_lvl, f"{name}\n({date_str})\n{arch}", ha="center", va=va,
                fontsize=7.4, fontweight="bold", color="#0F172A", bbox=bbox_props)

    plt.title("Milestone Timeline of Scientific Foundation Models (2022–2026)",
              fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "weather_foundation_timeline.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "weather_foundation_timeline.pdf"))
    plt.close()
    print("Generated weather_foundation_timeline.png/.pdf")


def plot_resolution_vs_leadtime():
    # Stated values directly extracted from verified papers
    models = [
        {"name": "Pangu-Weather", "res": 0.25, "lead": 7, "params": 256, "col": "#2563EB"},
        {"name": "GraphCast", "res": 0.25, "lead": 10, "params": 36.7, "col": "#DC2626"},
        {"name": "FourCastNet", "res": 0.25, "lead": 10, "params": 73.5, "col": "#059669"},
        {"name": "SFNO", "res": 0.25, "lead": 10, "params": 75, "col": "#10B981"},
        {"name": "FuXi", "res": 0.25, "lead": 15, "params": 150, "col": "#D97706"},
        {"name": "FengWu", "res": 0.25, "lead": 10.75, "params": 200, "col": "#7C3AED"},
        {"name": "GenCast", "res": 0.25, "lead": 15, "params": 120, "col": "#E11D48"},
        {"name": "Aurora", "res": 0.10, "lead": 10, "params": 1300, "col": "#0284C7"},
        {"name": "AIFS", "res": 0.25, "lead": 15, "params": 185, "col": "#0D9488"},
        {"name": "FuXi-Extreme", "res": 0.25, "lead": 10, "params": 150, "col": "#DC2626"},
        {"name": "NeuralGCM", "res": 0.70, "lead": 15, "params": 14.5, "col": "#6366F1"},
        {"name": "XiHe (Ocean)", "res": 0.083, "lead": 10, "params": 84, "col": "#0D9488"},
        {"name": "GlobalFlood", "res": 0.10, "lead": 7, "params": 5, "col": "#B45309"},
        {"name": "Stormer", "res": 1.406, "lead": 10, "params": 67, "col": "#CA8A04"},
        {"name": "SEEDS", "res": 1.00, "lead": 10, "params": 100, "col": "#EA580C"},
    ]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)

    for m in models:
        # Scale marker size by parameter count (log scale)
        s = 80 + 35 * np.log(max(m["params"], 2))
        ax.scatter(m["lead"], m["res"], s=s, color=m["col"], alpha=0.85, edgecolors="#1E293B", lw=1.2, zorder=3)
        # Text label offset
        offset_y = 0.02 if m["res"] < 0.20 else (-0.05 if m["res"] > 0.5 else -0.025)
        offset_x = 0.24
        ax.text(m["lead"] + offset_x, m["res"] + offset_y,
                f"{m['name']}\n({m['res']}°, {m['params']}M)",
                fontsize=8.0, fontweight="bold", color="#1E293B", zorder=4)

    ax.set_xlabel("Maximum Forecast Lead Time (Days)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Spatial Resolution (Degrees Lat/Lon, lower = finer)", fontsize=11, fontweight="bold")
    ax.set_ylim(0.02, 1.58)
    ax.set_xlim(5, 17)
    ax.grid(True, linestyle="--", alpha=0.5, zorder=0)

    # Highlight frontier zones
    ax.axhspan(0.04, 0.12, color="#EFF6FF", alpha=0.6, label="High-Resolution Planetary Frontier (<=0.10°)")
    ax.axvspan(12, 16.5, color="#F0FDF4", alpha=0.6, label="Extended Medium-Range Frontier (>=12 days)")

    ax.legend(loc="upper right", framealpha=0.9)
    plt.title("Spatial Resolution vs. Forecast Lead Time in Stated Literature",
              fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "resolution_vs_leadtime.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "resolution_vs_leadtime.pdf"))
    plt.close()
    print("Generated resolution_vs_leadtime.png/.pdf")


def plot_agent_reasoning_dag():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_box(x, y, w, h, text, title=None, facecolor="#F0F4F8", edgecolor="#1E3A8A", titlecolor="#0F172A"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=1.2,rounding_size=1.8",
            facecolor=facecolor, edgecolor=edgecolor, linewidth=1.6
        )
        ax.add_patch(rect)
        if title:
            ax.text(x + w / 2, y + h - 2.5, title, ha="center", va="top",
                    fontsize=9.5, fontweight="bold", color=titlecolor)
            ax.text(x + w / 2, y + (h - 4.2) / 2, text, ha="center", va="center",
                    fontsize=8.5, color="#1E293B", multialignment="center")
        else:
            ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=8.5, color="#1E293B", multialignment="center")

    def draw_arrow(x1, y1, x2, y2, color="#475569", label=None, label_offset=(0, 2), style="-|>", lw=1.8):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw, mutation_scale=14))
        if label:
            ax.text((x1 + x2) / 2 + label_offset[0], (y1 + y2) / 2 + label_offset[1], label,
                    ha="center", va="center", fontsize=8.0, fontweight="bold", color=color,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9))

    # Title
    ax.text(50, 96.5, "Autonomous Multi-Agent Scientific Reasoning DAG & Verification Loop",
            ha="center", va="top", fontsize=13, fontweight="bold", color="#0F172A")

    # 1. Scientific Objective
    draw_box(4, 76, 26, 15,
             "Natural Science Research Query\nSpatio-Temporal Bounds & Events\n(e.g., Extreme Heatwave / Vortex)",
             "Scientific Task & Context", facecolor="#EEF2FF", edgecolor="#4338CA", titlecolor="#312E81")

    # 2. Plan-Agent
    draw_box(37, 76, 26, 15,
             "Hierarchical Goal Decomposition\nTopological Task Scheduling\nDAG Dependency Formulation",
             "1. Plan-Agent (DAG Planning)", facecolor="#EFF6FF", edgecolor="#2563EB", titlecolor="#1E40AF")

    # 3. Data-Agent
    draw_box(70, 76, 26, 15,
             "CDS, USGS, GLORYS Retrieval\nNetCDF/Zarr Out-of-Core IO\nxarray & dask Tensor Chunking",
             "2. Data-Agent (Data Sourcing)", facecolor="#ECFDF5", edgecolor="#059669", titlecolor="#065F46")

    # 4. Coding-Agent
    draw_box(70, 44, 26, 16,
             "Python / REPL Code Synthesis\nAST Validation & Execution\nMetPy / ObsPy / PyTorch Solvers",
             "3. Coding-Agent (Execution)", facecolor="#FEF3C7", edgecolor="#D97706", titlecolor="#92400E")

    # 5. Autonomous Error Diagnostics
    draw_box(37, 44, 26, 16,
             "Stack Traceback & Error Parsing\nCoordinate Inversion / Axis Alignment\nDynamic Prompt Self-Correction",
             "4. Self-Correction Loop", facecolor="#FEE2E2", edgecolor="#DC2626", titlecolor="#991B1B")

    # 6. Critic-Agent & Guardrails
    draw_box(37, 10, 26, 18,
             "Physical Conservation Laws\nMass/Energy Balance & Continuity\nNon-Negativity (Precip >= 0)\nUnit Consistency & Range Bounds",
             "5. Critic-Agent (Guardrails)", facecolor="#F5F3FF", edgecolor="#7C3AED", titlecolor="#5B21B6")

    # 7. Scientific Discovery Artifacts
    draw_box(4, 10, 26, 18,
             "Publication-Grade Diagnostics\nMulti-Modal Verification Metrics\nStandardized NetCDF Outputs\nSynthesized Research Reports",
             "6. Scientific Discovery", facecolor="#F0FDF4", edgecolor="#16A34A", titlecolor="#166534")

    # Arrows
    draw_arrow(30, 83.5, 37, 83.5, color="#4338CA", label="User Intent")
    draw_arrow(63, 83.5, 70, 83.5, color="#2563EB", label="Task Specs")
    draw_arrow(83, 76, 83, 60, color="#059669", label="Tensors", label_offset=(4, 0))
    
    # Coding to Error Recovery & retry
    draw_arrow(70, 52, 63, 52, color="#DC2626", label="Exception / Mismatch", label_offset=(0, 2.5))
    draw_arrow(50, 60, 50, 76, color="#DC2626", label="Refined Plan", label_offset=(5, 0))
    
    # Coding to Critic-Agent
    draw_arrow(75, 44, 58, 28, color="#D97706", label="Raw Output", label_offset=(5, 2))
    
    # Critic feedback loop to coding
    draw_arrow(50, 28, 50, 44, color="#7C3AED", label="Violation Feedback", label_offset=(-7, 0))

    # Critic to Final Discovery
    draw_arrow(37, 19, 30, 19, color="#16A34A", label="Verified Laws", label_offset=(0, 2.5))

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "agent_reasoning_dag.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "agent_reasoning_dag.pdf"))
    plt.close()
    print("Generated agent_reasoning_dag.png/.pdf")


def plot_publications_by_year():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)

    included = [p for p in papers if p.get("status") == "included"]
    years = [2022, 2023, 2024, 2025, 2026]
    domains = [
        "Weather/Climate",
        "Remote Sensing / EO",
        "Hydrology",
        "Oceanography",
        "Geophysics/Seismology",
        "Space Weather",
        "Reasoning / Benchmark"
    ]

    domain_counts = {d: {y: 0 for y in years} for d in domains}
    for p in included:
        d = p.get("domain", "")
        y = p.get("year")
        if d in domain_counts and y in years:
            domain_counts[d][y] += 1

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    bottom = np.zeros(len(years))
    palette = ["#2563EB", "#0D9488", "#D97706", "#0284C7", "#7C3AED", "#E11D48", "#16A34A"]

    for idx, d in enumerate(domains):
        counts = [domain_counts[d][y] for y in years]
        ax.bar(years, counts, bottom=bottom, label=d, color=palette[idx % len(palette)],
               edgecolor="white", width=0.6)
        bottom += np.array(counts)

    ax.set_xlabel("Year of Publication / Preprint Release", fontsize=11, fontweight="bold")
    ax.set_ylabel("Number of Core Foundation Papers", fontsize=11, fontweight="bold")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), framealpha=0.9)

    plt.title("Distribution of Scientific Time Series Foundation Papers by Domain",
              fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "publications_by_year.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "publications_by_year.pdf"))
    plt.close()
    print("Generated publications_by_year.png/.pdf")


def plot_multimodal_alignment_arch():
    fig, ax = plt.subplots(figsize=(13.5, 7.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_box(x, y, w, h, text, title=None, facecolor="#F0F4F8", edgecolor="#1E3A8A", titlecolor="#0F172A"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=1.0,rounding_size=1.5",
            facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5
        )
        ax.add_patch(rect)
        if title:
            ax.text(x + w / 2, y + h - 2.8, title, ha="center", va="top",
                    fontsize=9.0, fontweight="bold", color=titlecolor)
            ax.text(x + w / 2, y + (h - 4.2) / 2, text, ha="center", va="center",
                    fontsize=7.8, color="#1E293B", multialignment="center")
        else:
            ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                    fontsize=7.8, color="#1E293B", multialignment="center")

    def draw_arrow(x1, y1, x2, y2, color="#475569", label=None, label_offset=(0, 2), style="-|>", lw=1.6):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw, mutation_scale=12))
        if label:
            ax.text((x1 + x2) / 2 + label_offset[0], (y1 + y2) / 2 + label_offset[1], label,
                    ha="center", va="center", fontsize=7.5, fontweight="bold", color=color,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9))

    # Header Title
    ax.text(50, 97.0, "Scientific Multimodal Cross-Attention Alignment & Neural Inversion Architecture",
            ha="center", va="top", fontsize=13, fontweight="bold", color="#0F172A")

    # Section 1: Observation Modalities (Left)
    ax.text(14, 91.5, "1. Heterogeneous Modalities", ha="center", va="center", fontsize=10, fontweight="bold", color="#1E40AF")
    
    draw_box(2, 70, 24, 17,
             "Optical & Radar Satellite Cubes\nSentinel-1/2, Landsat, MODIS\nIrregular revisit & multi-scale\n(X_sat in R^{T x C x H x W})",
             "Multispectral / SAR Imagery", facecolor="#EFF6FF", edgecolor="#2563EB", titlecolor="#1E40AF")
             
    draw_box(2, 48, 24, 17,
             "Global Gridded Reanalysis\nERA5, IFS Analysis, GFS\nUniform lat-lon / spherical grid\n(X_grid in R^{B x L x H x W})",
             "Gridded Atmospheric Tensors", facecolor="#ECFDF5", edgecolor="#059669", titlecolor="#065F46")

    draw_box(2, 26, 24, 17,
             "Sparse In-Situ Sensor Networks\nStreamflow gauges, Seismograms\nWeather stations, Ocean buoys\n(X_point in R^{N x T x D})",
             "Point Series & Waveforms", facecolor="#FEF3C7", edgecolor="#D97706", titlecolor="#92400E")

    draw_box(2, 4, 24, 17,
             "Asynchronous Soundings & Tracks\nRadiosondes, Aircraft AMDAR\nSatellite Altimetry (SSH Tracks)\n(y_k at irregular t_k)",
             "Asynchronous Sensor Tracks", facecolor="#FDF2F8", edgecolor="#DB2777", titlecolor="#9D174D")

    # Section 2: Modality Alignment Strategies (Center)
    ax.text(49, 91.5, "2. Cross-Modal Alignment Strategies", ha="center", va="center", fontsize=10, fontweight="bold", color="#4338CA")

    # Strategy A
    draw_box(31, 68, 36, 19,
             "Modality-Specific Patch Embeddings\nPositional Harmonization: PE(x, y, z, t)\nContinuous coordinate encodings\n(SatMAE, Presto, Galileo)",
             "Strategy A: Early Heterogeneous Patching",
             facecolor="#F5F3FF", edgecolor="#6366F1", titlecolor="#3730A3")

    # Strategy B
    draw_box(31, 37, 36, 26,
             "Fixed Learnable Latent Query Bank: Z in R^{M x D}\nCrossAttn(Z, X_modality, X_modality)\nDecouples irregular sensor density from backbone compute\nEnables arbitrary multi-sensor conditioning\n(Aurora, SkySense, ClimaX, Prithvi)",
             "Strategy B: Latent Cross-Attention Bottleneck",
             facecolor="#EEF2FF", edgecolor="#4F46E5", titlecolor="#312E81")

    # Strategy C
    draw_box(31, 4, 36, 28,
             "Continuous Spectral Wavelength Embedding: e_lambda\nDynamic Hypernetwork: H_phi(e_lambda) -> W_kernel\nZero-shot sensor adaptation across arbitrary bands\nContinuous band interpolation (400nm - 2200nm)\n(DOFA, AnySat)",
             "Strategy C: Dynamic Wavelength Hypernetworks",
             facecolor="#FFFBEB", edgecolor="#B45309", titlecolor="#78350F")

    # Section 3: Backbone & Variational Neural Inversion (Right)
    ax.text(85, 91.5, "3. Foundation Backbone & Inversion", ha="center", va="center", fontsize=10, fontweight="bold", color="#065F46")

    draw_box(71, 52, 27, 35,
             "Spherical Harmonic Transforms (SFNO)\nMulti-Mesh Message Passing (GraphCast)\n3D Earth Transformers (Pangu, FuXi)\nScore-Based Diffusion SDE (GenCast, SEEDS)\nPreserves Kolmogorov Turbulent Spectra",
             "Unified Spatio-Temporal Backbone",
             facecolor="#ECFDF5", edgecolor="#059669", titlecolor="#065F46")

    draw_box(71, 4, 27, 43,
             "Neural 4D-Var Unrolled Solvers\nx_0^{(i+1)} = x_0^{(i)} - Gamma_theta(grad J)\n(4DVarNet, FengWu-4DVar)\n---\nScore-Based Posterior Sampling\ndx = [f(x,t) - g^2(grad log p + grad log p(y|x))] dt\n(DiffDA, Score-based DA)\nSparse Observation -> Gridded Initial State",
             "Neural Variational Data Assimilation",
             facecolor="#F0FDF4", edgecolor="#16A34A", titlecolor="#14532D")

    # Connector Arrows
    # Inputs to Strategy A & B & C
    draw_arrow(26, 78.5, 31, 78.5, color="#2563EB")
    draw_arrow(26, 56.5, 31, 56.5, color="#059669")
    draw_arrow(26, 34.5, 31, 45.0, color="#D97706")
    draw_arrow(26, 12.5, 31, 16.0, color="#DB2777")

    # Strategies to Backbone
    draw_arrow(67, 77.5, 71, 77.5, color="#6366F1", label="Aligned Tokens", label_offset=(0, 2))
    draw_arrow(67, 50.0, 71, 62.0, color="#4F46E5", label="Latent Queries Z", label_offset=(0, 2))
    draw_arrow(67, 18.0, 71, 22.0, color="#B45309", label="Dynamic Kernels", label_offset=(0, 2))
    
    # DA coupling to Backbone
    draw_arrow(84.5, 47, 84.5, 52, color="#16A34A", label="Optimal x_0", label_offset=(4, 0), style="<|-|>")

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "multimodal_alignment_arch.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "multimodal_alignment_arch.pdf"))
    plt.close()
    print("Generated multimodal_alignment_arch.png/.pdf")


if __name__ == "__main__":
    plot_prisma_flow()
    plot_taxonomy_tree()
    plot_domain_modality_heatmap()
    plot_weather_foundation_timeline()
    plot_resolution_vs_leadtime()
    plot_agent_reasoning_dag()
    plot_multimodal_alignment_arch()
    plot_publications_by_year()
