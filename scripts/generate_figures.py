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
            ("Weather & Climate", "ERA5, MERRA-2, Radar\n(Pangu, GraphCast, Aurora)"),
            ("Earth Observation & RS", "Multispectral, SAR, DEM\n(SatMAE, Presto, Galileo)"),
            ("Hydrology & Oceans", "River gauges, GLORYS12\n(GlobalFlood, XiHe)"),
            ("Geophysics & Space", "Waveforms, SDO UV series\n(SeisT, Surya)")
        ]),
        ("Foundation Architectures", 37.5, "#DCFCE7", "#16A34A", [
            ("3D Spatial Transformers", "3D Swin, 3DEST, Perceiver\n(Pangu, Aurora)"),
            ("Multi-Mesh Graph Neural Nets", "Icosahedral spherical mesh\n(GraphCast, GenCast)"),
            ("Continuous Neural Operators", "AFNO, SFNO, Fourier Spec.\n(FourCastNet)"),
            ("Multimodal Masked Encoders", "Temporal-spectral masking\n(SatMAE, Presto, Galileo)")
        ]),
        ("Physics Integration Levels", 62.5, "#FEF3C7", "#D97706", [
            ("Purely Data-Driven", "Statistical auto-regression\n(Standard Vision Transformers)"),
            ("Soft Physics Loss Penalties", "Conservation & dynamic loss\n(FengWu, FourCastNet)"),
            ("Hard Architectural Constraints", "Inherent symmetry & projection\n(Spherical Harmonics, Invariance)"),
            ("Hybrid PDE-Neural Solvers", "Coupled numerical routing\n(GlobalFlood, NeuralHydrology)")
        ]),
        ("Roles of Reasoning LLMs", 87.5, "#F3E8FF", "#9333EA", [
            ("Scientific Reasoner", "Cross-domain time series QA\n(SciTS, TimeOmni)"),
            ("Contextual Enhancer", "Domain priors & text prefixes\n(ClimateLLM)"),
            ("Autonomous Scientific Agent", "Multi-step tool orchestration\n(ClimateAgent)"),
            ("Interactive Interface", "Natural language query to code\n(Scientific assistants)")
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
        ("FourCastNet", "2022-02", "AFNO Operator", 2022.15),
        ("SatMAE", "2022-07", "Temporal ViT MAE", 2022.55),
        ("Pangu-Weather", "2022-11", "3D Earth Swin", 2022.88),
        ("GraphCast", "2022-12", "Multi-Mesh GNN", 2022.98),
        ("ClimaX", "2023-01", "Variable ViT", 2023.08),
        ("Presto", "2023-04", "Lightweight EO", 2023.3),
        ("FengWu", "2023-04", "Cross-Modal Fuser", 2023.35),
        ("FuXi", "2023-06", "Cascade Swin", 2023.5),
        ("WeatherBench 2", "2023-08", "Evaluation Suite", 2023.65),
        ("Prithvi-100M", "2023-10", "Geospatial ViT", 2023.8),
        ("GenCast", "2023-12", "Diffusion Ensemble", 2023.95),
        ("GlobalFlood", "2024-03", "Ungauged Flood AI", 2024.2),
        ("Aurora", "2024-05", "1.3B 3D Perceiver", 2024.4),
        ("Prithvi WxC", "2024-09", "2.3B Climate Model", 2024.7),
        ("Galileo", "2025-02", "Multi-Scale EO", 2025.15),
        ("Surya", "2025-08", "Heliophysics Model", 2025.65),
        ("SciTS", "2025-10", "Scientific TS LLM", 2025.8),
    ]

    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)

    # Base timeline axis
    ax.axhline(0, color="#334155", lw=2.5, zorder=1)
    ax.set_xlim(2021.8, 2026.2)
    ax.set_ylim(-3.5, 4.0)
    ax.axis("off")

    years = [2022, 2023, 2024, 2025, 2026]
    for yr in years:
        ax.plot([yr, yr], [-0.3, 0.3], color="#0F172A", lw=2)
        ax.text(yr, -0.6, str(yr), ha="center", va="top", fontsize=11, fontweight="bold", color="#0F172A")

    levels = [1.2, -1.5, 2.3, -2.4, 1.4, -1.6, 2.6, -2.7, 1.3, -1.4, 2.4, -2.5, 1.5, 2.7, -1.6, 1.4, -2.6]
    colors = ["#2563EB", "#0D9488", "#DC2626", "#D97706", "#7C3AED", "#059669", "#E11D48", "#2563EB",
              "#475569", "#0D9488", "#DC2626", "#0284C7", "#7C3AED", "#D97706", "#059669", "#E11D48", "#2563EB"]

    for i, (name, date_str, arch, x_val) in enumerate(milestones):
        y_lvl = levels[i]
        c = colors[i % len(colors)]

        # Stem line
        ax.plot([x_val, x_val], [0, y_lvl], color=c, lw=1.2, linestyle="--", alpha=0.8, zorder=2)
        ax.scatter([x_val], [0], color=c, s=40, zorder=3)

        # Tag
        bbox_props = dict(boxstyle="round,pad=0.35,rounding_size=0.3", facecolor="white", edgecolor=c, lw=1.4)
        va = "bottom" if y_lvl > 0 else "top"
        ax.text(x_val, y_lvl, f"{name}\n({date_str})\n{arch}", ha="center", va=va,
                fontsize=8, fontweight="bold", color="#0F172A", bbox=bbox_props)

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
        {"name": "FuXi", "res": 0.25, "lead": 15, "params": 150, "col": "#D97706"},
        {"name": "FengWu", "res": 0.25, "lead": 10.75, "params": 200, "col": "#7C3AED"},
        {"name": "GenCast", "res": 0.25, "lead": 15, "params": 120, "col": "#E11D48"},
        {"name": "Aurora", "res": 0.10, "lead": 10, "params": 1300, "col": "#0284C7"},
        {"name": "XiHe (Ocean)", "res": 0.083, "lead": 10, "params": 84, "col": "#0D9488"},
        {"name": "GlobalFlood", "res": 0.10, "lead": 7, "params": 5, "col": "#B45309"},
    ]

    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)

    for m in models:
        # Scale marker size by parameter count (log scale)
        s = 80 + 35 * np.log(max(m["params"], 2))
        ax.scatter(m["lead"], m["res"], s=s, color=m["col"], alpha=0.85, edgecolors="#1E293B", lw=1.2, zorder=3)
        # Text label offset
        offset_y = 0.008 if m["res"] < 0.20 else -0.012
        offset_x = 0.2
        ax.text(m["lead"] + offset_x, m["res"] + offset_y,
                f"{m['name']}\n({m['res']}°, {m['params']}M)",
                fontsize=8.5, fontweight="bold", color="#1E293B", zorder=4)

    ax.set_xlabel("Maximum Forecast Lead Time (Days)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Spatial Resolution (Degrees Lat/Lon, lower = finer)", fontsize=11, fontweight="bold")
    ax.set_ylim(0.04, 0.32)
    ax.set_xlim(5, 17)
    ax.grid(True, linestyle="--", alpha=0.5, zorder=0)

    # Highlight frontier zone
    ax.axhspan(0.05, 0.12, color="#EFF6FF", alpha=0.6, label="High-Resolution Frontier (<=0.10°)")
    ax.axvspan(12, 16.5, color="#F0FDF4", alpha=0.6, label="Extended Medium-Range Frontier (>=12 days)")

    ax.legend(loc="upper right", framealpha=0.9)
    plt.title("Spatial Resolution vs. Forecast Lead Time in Stated Literature",
              fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "resolution_vs_leadtime.png"), dpi=300)
    plt.savefig(os.path.join(FIG_DIR, "resolution_vs_leadtime.pdf"))
    plt.close()
    print("Generated resolution_vs_leadtime.png/.pdf")


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


if __name__ == "__main__":
    plot_prisma_flow()
    plot_taxonomy_tree()
    plot_domain_modality_heatmap()
    plot_weather_foundation_timeline()
    plot_resolution_vs_leadtime()
    plot_publications_by_year()
