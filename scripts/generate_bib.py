#!/usr/bin/env python3
"""
Generate BibTeX file from data/papers.json for all included papers.
Strictly adheres to integrity rules in COMMON_METHOD.md.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
BIB_FILE = os.path.join(BASE_DIR, "paper", "references.bib")

os.makedirs(os.path.dirname(BIB_FILE), exist_ok=True)


def format_author_list(authors):
    if not authors:
        return "Unknown"
    # Format as 'Last, First and Last, First ...'
    formatted = []
    for a in authors:
        parts = a.split(",")
        if len(parts) >= 2:
            formatted.append(f"{parts[0].strip()}, {parts[1].strip()}")
        else:
            formatted.append(a.strip())
    return " and ".join(formatted)


def run_generate_bib():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)

    included = [p for p in papers if p.get("status") == "included"]
    bib_entries = []

    for p in sorted(included, key=lambda x: x["bibkey"]):
        key = p["bibkey"]
        title = p["title"]
        authors = format_author_list(p.get("authors", []))
        year = p.get("year", 2024)
        venue = p.get("venue", "arXiv")
        doi_or_url = p.get("doi_or_arxiv", "")

        # Escape special TeX characters
        title_escaped = title.replace("&", r"\&").replace("%", r"\%")
        venue_escaped = venue.replace("&", r"\&").replace("%", r"\%")

        is_journal = any(j in venue.lower() for j in ["nature", "science", "journal", "npj", "ieee", "james"])

        entry_type = "article" if is_journal or "arxiv" in venue.lower() else "inproceedings"

        lines = [f"@{entry_type}{{{key},"]
        lines.append(f"  title = {{{{{title_escaped}}}}},")
        lines.append(f"  author = {{{authors}}},")
        lines.append(f"  year = {{{year}}},")

        if is_journal:
            lines.append(f"  journal = {{{venue_escaped}}},")
        elif "arxiv" in venue.lower():
            lines.append(f"  journal = {{{venue_escaped}}},")
        else:
            lines.append(f"  booktitle = {{{venue_escaped}}},")

        if doi_or_url.startswith("http"):
            lines.append(f"  url = {{{doi_or_url}}},")
        if p.get("doi"):
            lines.append(f"  doi = {{{p['doi']}}},")

        lines.append("}")
        bib_entries.append("\n".join(lines))

    with open(BIB_FILE, "w", encoding="utf-8") as f:
        f.write("% Auto-generated from data/papers.json. Do not edit directly.\n\n")
        f.write("\n\n".join(bib_entries) + "\n")

    print(f"Generated {len(bib_entries)} BibTeX entries in {BIB_FILE}")


if __name__ == "__main__":
    run_generate_bib()
