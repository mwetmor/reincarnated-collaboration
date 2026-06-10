#!/usr/bin/env python3
"""
Zodiac Substrate Corpus — Aggregation Script
Combines all corpus-*.yaml per-tradition files into a single corpus.yaml
Run: python3 build_corpus.py
Output: corpus.yaml (same directory)
"""

import yaml, os, sys
from pathlib import Path

CORPUS_DIR = Path(__file__).parent
OUTPUT_FILE = CORPUS_DIR / "corpus.yaml"
HEADER = """# Zodiac Substrate Corpus — Aggregated Corpus
# Generated: 2026-06-09
# Commissioner: Gandalf (story-and-design steward)
# Mode: B (systematic catalogue crawl)
#
# This file combines all per-tradition YAML corpus files into a single
# machine-readable list. Each entry retains its tradition-specific sign_id
# and primary_culture field. Do not edit directly — edit per-tradition files
# and re-run build_corpus.py.
#
# Entry count: {count}
# Traditions: {traditions}

"""

def load_entries(filepath):
    """Load entries from a corpus YAML file, handling both list and dict formats."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ['entries', 'signs', 'figures', 'traditions', 'constellations']:
            if key in data:
                return data[key]
        # If it's a dict with no recognized key, try values
        return []
    return []

def main():
    # Find all corpus files (exclude corpus.yaml itself and build_corpus.py)
    corpus_files = sorted([
        f for f in CORPUS_DIR.glob("corpus-*.yaml")
        if f.name != "corpus.yaml"
    ])
    
    if not corpus_files:
        print("ERROR: No corpus-*.yaml files found.")
        sys.exit(1)
    
    all_entries = []
    tradition_counts = {}
    errors = []
    
    for fpath in corpus_files:
        tradition_name = fpath.stem.replace("corpus-", "")
        try:
            entries = load_entries(fpath)
            n = len(entries)
            all_entries.extend(entries)
            tradition_counts[tradition_name] = n
            print(f"  {tradition_name}: {n} entries")
        except Exception as e:
            errors.append(f"  ERROR in {fpath.name}: {e}")
            print(f"  ERROR in {fpath.name}: {e}")
    
    if errors:
        print(f"\nWARNING: {len(errors)} files had errors:")
        for err in errors:
            print(err)
    
    total = len(all_entries)
    tradition_list = ", ".join(f"{k}({v})" for k, v in tradition_counts.items())
    
    print(f"\nTotal: {total} entries from {len(tradition_counts)} traditions")
    
    # Write combined corpus
    header = HEADER.format(count=total, traditions=tradition_list)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(header)
        yaml.dump(all_entries, f, 
                  allow_unicode=True, 
                  default_flow_style=False,
                  sort_keys=False,
                  indent=2,
                  width=120)
    
    print(f"\nWrote {total} entries to {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size / 1024:.0f} KB")

if __name__ == "__main__":
    main()
