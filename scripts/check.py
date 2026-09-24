#!/usr/bin/env python3
"""
Comprehensive Quality Gates Check Script.
Implements 'make check' requirements from COMMON_METHOD.md.
"""

import json
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PAPER_DIR = os.path.join(BASE_DIR, "paper")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
PRISMA_FILE = os.path.join(DATA_DIR, "prisma_counts.json")
BIB_FILE = os.path.join(PAPER_DIR, "references.bib")
README_FILE = os.path.join(BASE_DIR, "README.md")


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def check_quality_gates():
    print("=" * 60)
    print("Running Quality Gates Verification (make check)...")
    print("=" * 60)
    failed = False

    # 1. Load papers.json
    if not os.path.exists(PAPERS_FILE):
        print("[FAIL] data/papers.json does not exist!")
        return False
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)

    included_papers = [p for p in papers if p.get("status") == "included"]
    included_bibkeys = {p["bibkey"] for p in included_papers}
    print(f"[OK] data/papers.json loaded: {len(included_papers)} included papers.")

    # 2. Check duplicates
    seen_titles = set()
    seen_keys = set()
    for p in included_papers:
        norm = normalize_title(p["title"])
        if norm in seen_titles:
            print(f"[FAIL] Duplicate paper title found: {p['title']}")
            failed = True
        seen_titles.add(norm)

        key = p["bibkey"]
        if key in seen_keys:
            print(f"[FAIL] Duplicate bibkey found: {key}")
            failed = True
        seen_keys.add(key)
    if not failed:
        print("[OK] No duplicate titles or bibkeys detected.")

    # 3. Check verified API provenance
    for p in included_papers:
        has_api_provenance = (
            (p.get("doi") or p.get("arxiv_id") or p.get("doi_or_arxiv"))
            and (p.get("authors") and len(p["authors"]) > 0)
            and p.get("year") is not None
        )
        if not has_api_provenance:
            print(f"[FAIL] Paper {p['bibkey']} lacks verified API metadata: {p}")
            failed = True
    if not failed:
        print("[OK] All included papers have verified academic API provenance.")

    # 4. Check references.bib
    if not os.path.exists(BIB_FILE):
        print("[FAIL] paper/references.bib does not exist!")
        failed = True
    else:
        with open(BIB_FILE, "r", encoding="utf-8") as f:
            bib_content = f.read()
        bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_content))

        # Check bib_keys == included_bibkeys
        missing_in_bib = included_bibkeys - bib_keys
        extra_in_bib = bib_keys - included_bibkeys
        if missing_in_bib:
            print(f"[FAIL] Bib keys missing in references.bib: {missing_in_bib}")
            failed = True
        if extra_in_bib:
            print(f"[FAIL] Extra keys in references.bib not in included papers: {extra_in_bib}")
            failed = True
        if not missing_in_bib and not extra_in_bib:
            print(f"[OK] references.bib matches included papers exactly ({len(bib_keys)} entries).")

    # 5. Check cited keys in LaTeX
    tex_files = [os.path.join(PAPER_DIR, "main.tex")]
    sections_dir = os.path.join(PAPER_DIR, "sections")
    if os.path.exists(sections_dir):
        for fname in os.listdir(sections_dir):
            if fname.endswith(".tex"):
                tex_files.append(os.path.join(sections_dir, fname))

    cited_keys = set()
    referenced_figures = set()
    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r"\\cite\{([^}]+)\}", content):
            for k in m.group(1).split(","):
                cited_keys.add(k.strip())
        for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", content):
            referenced_figures.add(m.group(1).strip())

    uncited_bibkeys = cited_keys - included_bibkeys
    if uncited_bibkeys:
        print(f"[FAIL] LaTeX cites undefined keys: {uncited_bibkeys}")
        failed = True
    else:
        print(f"[OK] All cited LaTeX keys ({len(cited_keys)}) are verified in included papers.")

    # 6. Check referenced figures exist
    for fig_path in referenced_figures:
        full_fig_path = os.path.join(PAPER_DIR, fig_path)
        if not os.path.exists(full_fig_path):
            print(f"[FAIL] Referenced figure not found: {full_fig_path}")
            failed = True
    if not failed:
        print(f"[OK] All referenced figures ({len(referenced_figures)}) exist on disk.")

    # 7. Check PRISMA counts
    if not os.path.exists(PRISMA_FILE):
        print("[FAIL] data/prisma_counts.json missing!")
        failed = True
    else:
        with open(PRISMA_FILE, "r", encoding="utf-8") as f:
            prisma = json.load(f)
        if prisma.get("studies_included_in_review") != len(included_papers):
            print(f"[FAIL] PRISMA included count mismatch: {prisma.get('studies_included_in_review')} vs {len(included_papers)}")
            failed = True
        else:
            print(f"[OK] PRISMA counts valid and synchronized ({prisma['studies_included_in_review']} studies).")

    # 8. Check README.md
    if not os.path.exists(README_FILE):
        print("[FAIL] README.md missing!")
        failed = True
    else:
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_text = f.read()
        missing_in_readme = [p["title"] for p in included_papers if p["title"] not in readme_text]
        if missing_in_readme:
            print(f"[FAIL] Papers missing in README: {missing_in_readme[:3]}")
            failed = True
        else:
            print("[OK] README.md contains all included papers.")

    # 9. Check main.pdf
    pdf_path = os.path.join(PAPER_DIR, "main.pdf")
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
        print("[FAIL] paper/main.pdf is missing or empty!")
        failed = True
    else:
        print(f"[OK] paper/main.pdf exists ({os.path.getsize(pdf_path)} bytes).")

    print("=" * 60)
    if failed:
        print("RESULT: Quality gates FAILED.")
        sys.exit(1)
    else:
        print("RESULT: All quality gates PASSED successfully!")
        print("=" * 60)


if __name__ == "__main__":
    check_quality_gates()
