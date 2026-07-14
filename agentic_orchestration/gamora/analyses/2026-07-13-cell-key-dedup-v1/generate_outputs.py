#!/usr/bin/env python3
"""
Cell-key dedup v1 — Stage 1 (strict exact-match GROUP BY cell_key).
gamora, 2026-07-13. Dispatch: 2026-07-13-gamora-cell-key-dedup-v1.
Spec: gandalf/design-inputs/dedup-stage1-gamora-handoff-2026-07-13.md.
Canon: reap-die-rise-engine/coordinate-register-2026-07-13.md §6/§6.1/§8.

PURE DATA. Read-only over corpus.db. No sim, no coarsening, no deletion.
Emits three outputs:
  1. cell_table.csv            — cell_key · representative · isotopes · population
  2. isotope_depth_hist.csv    — depth histogram (support; expected trivial)
  3. near_twin_pairs.csv       — Hamming-1 cell-pairs, annotated (PRIMARY)
     + near_twin_percoord.csv  — the per-coord aggregate (the Stage-2 driver)
"""
import sqlite3, csv, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
# corpus.db lives at repo-relative agentic_orchestration/research/curated/corpus.db
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "research", "curated", "corpus.db"))

# 14-slot cell_key layout (register §2; #5 control contributes two slots).
POS = ['1-movement', '2-delivery', '3-amp', '4-geometry',
       '5a-ctrl_treatment', '5b-ctrl_function', '6-defense', '7-economy_model',
       '8-proxy', '9-range', '10-tempo', '11-commit', '12-activation', '13-dependency']

con = sqlite3.connect(DB)

# ---- Stage 1: strict GROUP BY cell_key over the 470 combat-kit rows ----
# Representative tiebreak (§6: longevity of lineage across games -> recency -> primary):
#   longevity  = era_span (# of ';'-delimited era segments in canon_corpus.eras)
#   recency    = era_year (MAX)
#   quality    = canon_tier rank (deep>moderate>shallow) — nudge before deterministic floor
#   primary    = kit_id ASC (deterministic, fully-ordered)
# NOTE: skill_debut_year is populated for only 7/470 rows -> unusable as longevity proxy.
# NOTE: no cell's members share a multi-GAME lineage in this corpus, so "across games"
#       longevity is not literally per-lineage computable; era_span is the faithful proxy
#       (how many balance-eras the lineage survived). Flagged to gandalf for confirm.
rows = con.execute("""
  SELECT k.cell_key, k.kit_id, c.game,
    CASE WHEN c.eras IS NULL OR c.eras='' THEN 0
         ELSE (LENGTH(c.eras) - LENGTH(REPLACE(c.eras,';',''))) + 1 END AS era_span,
    COALESCE(c.era_year, 0) AS era_year,
    CASE c.canon_tier WHEN 'deep' THEN 3 WHEN 'moderate' THEN 2 WHEN 'shallow' THEN 1 ELSE 0 END AS tier_rank,
    COALESCE(c.canon_tier,'') AS canon_tier, COALESCE(c.eras,'') AS eras
  FROM canon_engine_key k JOIN canon_corpus c ON k.kit_id = c.kit_id
  WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL
""").fetchall()

cells = {}
for cell_key, kit_id, game, era_span, era_year, tier_rank, canon_tier, eras in rows:
    cells.setdefault(cell_key, []).append(
        dict(kit_id=kit_id, game=game, era_span=era_span, era_year=era_year,
             tier_rank=tier_rank, canon_tier=canon_tier, eras=eras))

def rep_sort_key(m):
    # descending longevity, recency, quality; ascending kit_id (deterministic primary)
    return (-m['era_span'], -m['era_year'], -m['tier_rank'], m['kit_id'])

# ---- Output 1: cell table ----
with open(os.path.join(HERE, "cell_table.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cell_key", "population", "representative_kit_id", "isotope_kit_ids"])
    for cell_key in sorted(cells):
        members = sorted(cells[cell_key], key=rep_sort_key)
        rep = members[0]['kit_id']
        isos = ";".join(m['kit_id'] for m in members[1:])  # losers retained, never deleted
        w.writerow([cell_key, len(members), rep, isos])

# ---- Output 2: isotope-depth histogram (support; expected trivial) ----
depth = Counter(len(m) for m in cells.values())
with open(os.path.join(HERE, "isotope_depth_hist.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["depth", "num_cells", "kits_covered"])
    for d in sorted(depth):
        w.writerow([d, depth[d], d * depth[d]])

# ---- Output 3 (PRIMARY): near-twin adjacency (Hamming-1) ----
cell_keys = sorted(cells)
split = {ck: ck.split('|') for ck in cell_keys}
near = []
for i in range(len(cell_keys)):
    a = split[cell_keys[i]]
    for j in range(i + 1, len(cell_keys)):
        b = split[cell_keys[j]]
        diffs = [p for p in range(14) if a[p] != b[p]]
        if len(diffs) == 1:
            p = diffs[0]
            va, vb = sorted([a[p], b[p]])
            near.append((POS[p], va, vb, cell_keys[i], cell_keys[j]))

with open(os.path.join(HERE, "near_twin_pairs.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["differing_coord", "value_a", "value_b", "cell_key_a", "cell_key_b"])
    for coord, va, vb, ca, cb in sorted(near):
        w.writerow([coord, va, vb, ca, cb])

# ---- Output 3-aggregate (THE Stage-2 driver): near-twin pairs per coord ----
percoord = Counter(n[0] for n in near)
with open(os.path.join(HERE, "near_twin_percoord.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["differing_coord", "near_twin_pairs", "distinct_value_swaps", "top_swaps"])
    for coord in POS:  # register order, all 14 (incl. zeros)
        vp = Counter((n[1], n[2]) for n in near if n[0] == coord)
        top = "; ".join(f"{va}~{vb}({c})" for (va, vb), c in vp.most_common(12))
        w.writerow([coord, percoord[coord], len(vp), top])

print(f"cells={len(cells)}  kits={sum(len(m) for m in cells.values())}  "
      f"near_twin_pairs={len(near)}  depth={dict(sorted(depth.items()))}")
print("per-coord near-twin counts (desc):")
for coord in sorted(POS, key=lambda c: -percoord[c]):
    print(f"  {coord:22s} {percoord[coord]}")
