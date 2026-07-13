"""
Generate stats + delta deliverables for V1 Plane view.
Outputs: occupancy-stats.md, rollup-tables.md, delta-findings.md

Run after render_v1_plane.py completes (imports from it).
"""

import sys
import os
from pathlib import Path
from collections import defaultdict

# Import render module
sys.path.insert(0, str(Path(__file__).parent))
from render_v1_plane import (
    load_data, assign_plane_a, assign_plane_b, assign_roster,
    geo_to_plane_a, geo_to_plane_b_cols, roster_commit,
    PLANE_A_ROWS, PLANE_A_COLS, PLANE_A_COL_LABELS, PLANE_A_ROW_LABELS,
    PLANE_B_ROWS, PLANE_B_COLS,
    PLANE_B_ROW_TO_COMMIT, PLANE_B_ROLLUP, PLANE_B_ROLLUP_NOTES,
    GEO_ROLLUP, ROSTER_GEO_HINTS
)

OUT_DIR = Path(__file__).parent


def cell_count(cells, bucket, include_mint=True):
    d = cells.get(bucket, {})
    c = len(d.get("corpus", []))
    m = len(d.get("mint", []))
    return c + m if include_mint else c


def concentration(counts):
    """Simple HHI-style concentration: sum of squared proportions. 1.0 = all in one cell."""
    total = sum(counts)
    if total == 0:
        return 0.0
    return sum((c / total) ** 2 for c in counts)


def generate_occupancy_stats(cells_a, cells_b, roster_a, roster_b, corpus_kits, roster_kits):
    lines = []
    lines.append("# Occupancy Statistics — V1 Plane View")
    lines.append("")
    lines.append("> Generated 2026-07-12. Grain: ARCHIVE (geometry family × commitment class).")
    lines.append("> Corpus = 463 combat kits. Roster = 45 engine kits. Negatives = 37 (UNMAPPED strip, not in grid).")
    lines.append("")

    # ── PLANE A ──
    lines.append("## Plane A — Spec Grid (3 × 5 = 15 cells)")
    lines.append("")

    a_counts = {}
    for r in PLANE_A_ROWS:
        for c in PLANE_A_COLS:
            b = (r, c)
            a_counts[b] = cell_count(cells_a, b)

    occupied_a = [b for b, n in a_counts.items() if n > 0]
    empty_a    = [b for b, n in a_counts.items() if n == 0]
    max_cell_a = max(a_counts, key=a_counts.get)

    unmapped_a_corpus = len(cells_a.get("UNMAPPED", {}).get("corpus", []))
    unmapped_a_mint   = len(cells_a.get("UNMAPPED", {}).get("mint", []))

    lines.append(f"- **Occupied cells:** {len(occupied_a)} / 15")
    lines.append(f"- **Empty cells:** {len(empty_a)} / 15 — frontier gaps")
    lines.append(f"- **Max-cell pileup:** {a_counts[max_cell_a]} kits in {max_cell_a}")
    lines.append(f"- **UNMAPPED (below grid):** {unmapped_a_corpus + unmapped_a_mint} corpus kits "
                 f"(geometry type not mappable to 5-family dispersion axis)")
    lines.append(f"- **Concentration (HHI):** {concentration(list(a_counts.values())):.3f} "
                 f"(1.0 = all in one cell; lower = more even)")
    lines.append("")
    lines.append("### Per-cell counts (Plane A)")
    lines.append("")
    lines.append("| Commitment | Single | Chain | Small-AOE | Large-AOE | Multi-Spawn |")
    lines.append("|---|---|---|---|---|---|")
    for r in PLANE_A_ROWS:
        row_vals = [a_counts.get((r, c), 0) for c in PLANE_A_COLS]
        lines.append(f"| **{r}** | " + " | ".join(str(v) for v in row_vals) + " |")
    lines.append("")

    lines.append("### Empty cells (Plane A) — frontier list")
    lines.append("")
    for b in empty_a:
        lines.append(f"- `{b[0]} × {b[1]}`")
    lines.append("")

    # Roster spread A
    roster_a_in_grid = [(bucket, kid) for bucket, kid, name in roster_a
                        if bucket not in ("UNMAPPED", "COMMIT_UNKNOWN")]
    roster_a_unmapped = [(bucket, kid) for bucket, kid, name in roster_a
                         if bucket in ("UNMAPPED", "COMMIT_UNKNOWN")]
    cells_with_roster_a = len(set(b for b, kid in roster_a_in_grid))
    lines.append(f"### Roster-45 spread (Plane A)")
    lines.append("")
    lines.append(f"- **Roster kits placed in grid:** {len(roster_a_in_grid)} / 45")
    lines.append(f"- **Roster kits UNMAPPED or commit-unknown:** {len(roster_a_unmapped)}")
    lines.append(f"- **Grid cells containing ≥1 roster kit:** {cells_with_roster_a} / 15")
    lines.append("")

    # ── PLANE B ──
    lines.append("---")
    lines.append("")
    lines.append("## Plane B — Matt's Mock (3 × 8 = 24 cells)")
    lines.append("")

    b_counts = {}
    for r in PLANE_B_ROWS:
        for c in PLANE_B_COLS:
            b = (r, c)
            b_counts[b] = cell_count(cells_b, b)

    occupied_b = [b for b, n in b_counts.items() if n > 0]
    empty_b    = [b for b, n in b_counts.items() if n == 0]
    max_cell_b = max(b_counts, key=b_counts.get)

    unmapped_b_corpus = len(cells_b.get("UNMAPPED", {}).get("corpus", []))
    unmapped_b_mint   = len(cells_b.get("UNMAPPED", {}).get("mint", []))

    lines.append(f"- **Occupied cells:** {len(occupied_b)} / 24")
    lines.append(f"- **Empty cells:** {len(empty_b)} / 24 — frontier gaps")
    lines.append(f"- **Max-cell pileup:** {b_counts[max_cell_b]} kits in {max_cell_b}")
    lines.append(f"- **UNMAPPED (below grid):** {unmapped_b_corpus + unmapped_b_mint} corpus kits")
    lines.append(f"- **Concentration (HHI):** {concentration(list(b_counts.values())):.3f}")
    lines.append("")
    lines.append("### Per-cell counts (Plane B)")
    lines.append("")
    header = "| Commitment | " + " | ".join(PLANE_B_COLS) + " |"
    lines.append(header)
    lines.append("|---|" + "---|" * len(PLANE_B_COLS))
    for r in PLANE_B_ROWS:
        row_vals = [b_counts.get((r, c), 0) for c in PLANE_B_COLS]
        lines.append(f"| **{r}** | " + " | ".join(str(v) for v in row_vals) + " |")
    lines.append("")

    lines.append("### Empty cells (Plane B) — frontier list")
    lines.append("")
    for b in empty_b:
        lines.append(f"- `{b[0]} × {b[1]}`")
    lines.append("")

    roster_b_in_grid = [(bucket, kid) for bucket, kid, name in roster_b
                        if bucket not in ("UNMAPPED", "COMMIT_UNKNOWN")]
    roster_b_unmapped = [(bucket, kid) for bucket, kid, name in roster_b
                         if bucket in ("UNMAPPED", "COMMIT_UNKNOWN")]
    cells_with_roster_b = len(set(b for b, kid in roster_b_in_grid))
    lines.append(f"### Roster-45 spread (Plane B)")
    lines.append("")
    lines.append(f"- **Roster kits placed in grid:** {len(roster_b_in_grid)} / 45")
    lines.append(f"- **Roster kits UNMAPPED or commit-unknown:** {len(roster_b_unmapped)}")
    lines.append(f"- **Grid cells containing ≥1 roster kit:** {cells_with_roster_b} / 24")
    lines.append("")

    return "\n".join(lines)


def generate_rollup_tables():
    lines = []
    lines.append("# Rollup Tables — V1 Plane View")
    lines.append("")
    lines.append("> Discipline: assignments grounded in substrate-coordinates.md §1 Axis 2 definitions;")
    lines.append("> judgment calls flagged inline. UNMAPPED = genuinely unmappable; never silently bent.")
    lines.append("")

    # ── 24→5 Rollup (Plane A) ──
    lines.append("## Table 1: 24→5 Geometry Rollup (Plane A dispersion-v1 families)")
    lines.append("")
    lines.append("Axis 2 families (substrate-coordinates §1): "
                 "`single` · `chain` · `small_aoe` · `large_aoe` · `multi_spawn`")
    lines.append("Ordering rule: `dispersion-v1` (spec §2.3) — "
                 "single → chain → small-AOE → large-AOE → multi-spawn.")
    lines.append("")
    lines.append("| geometry_value (24-type rich palette) | → Axis 2 Family | Flag | Reasoning |")
    lines.append("|---|---|---|---|")

    # Sort by family then by geo_val
    family_order = ["single", "chain", "small_aoe", "large_aoe", "multi_spawn", "UNMAPPED"]
    sorted_entries = sorted(GEO_ROLLUP.items(),
                            key=lambda kv: (family_order.index(kv[1][0]), str(kv[0])))
    for geo_val, (family, flag, reason) in sorted_entries:
        geo_display = str(geo_val) if geo_val is not None else "NULL"
        lines.append(f"| `{geo_display}` | **{family}** | {flag} | {reason} |")

    lines.append("")
    lines.append("**Note on `multi_projectile` (judgment):** 41 corpus kits carry this type. "
                 "Filed as `chain` — canonical chain-pattern precursor (D2 Multi-Shot, PoE Barrage). "
                 "See table row above. Alternative mapping `large_aoe` would apply if the volley fans "
                 "wide rather than traveling as discrete bolts — a per-kit call, not resolvable at "
                 "geometry_value grain alone.")
    lines.append("")

    # ── Plane B mapping table ──
    lines.append("---")
    lines.append("")
    lines.append("## Table 2: Plane B Delivery-Family Mapping")
    lines.append("")
    lines.append("Parsed from Matt's mock SVG `reap-die-rise-atlas-chart-mock.svg` — text elements verbatim:")
    lines.append("")
    lines.append("**Column headers (8 columns, left→right):**")
    lines.append("> `➤ PROJECTILE` · `◎ ORBITAL` · `✳ NOVA` · `▒ ZONE` · `━ BEAM` · `✕ MELEE` · `☍ SUMMON` · `◯ RING`")
    lines.append("")
    lines.append("**Row headers (3 rows, top→bottom):**")
    lines.append("> `SNAP` · `WIND-UP` · `CHANNEL`")
    lines.append("")
    lines.append("**Plane B row → commit enum mapping:**")
    lines.append("> `SNAP` = instant · `WIND-UP` = wind-up · `CHANNEL` = channel")
    lines.append("")
    lines.append("| Plane B Column | Maps to geometry_value(s) | Flag | Notes |")
    lines.append("|---|---|---|---|")
    for col in PLANE_B_COLS:
        geos = PLANE_B_ROLLUP.get(col, [])
        geo_str = ", ".join(f"`{g}`" for g in geos)
        note = PLANE_B_ROLLUP_NOTES.get(col, "")
        flag = "judgment" if "OVERLAP" in note or "judgment" in note.lower() else "def"
        lines.append(f"| **{col}** | {geo_str} | {flag} | {note} |")

    lines.append("")
    lines.append("### Overlap flags")
    lines.append("")
    lines.append("Plane B has intentional column overlaps absent in Plane A:")
    lines.append("- **NOVA vs ZONE:** Both claim `circle` and `ground_targeted_circle`. "
                 "In the render, these kits are assigned to first-listed column (NOVA) "
                 "to avoid double-counting — true split would require per-kit sub-geometry.")
    lines.append("- **ORBITAL vs RING:** Both claim `ring` geometry. "
                 "In the render, these are assigned to ORBITAL first. "
                 "RING column receives only kits unambiguously ring-only (none in corpus after ORBITAL takes priority).")
    lines.append("")

    return "\n".join(lines)


def generate_delta_findings(cells_a, cells_b, corpus_kits):
    lines = []
    lines.append("# Delta Findings — Plane A vs Plane B")
    lines.append("")
    lines.append("> Findings only — no recommendation. Plane-lock read is gandalf's.")
    lines.append("> Delta = where the two planes DISAGREE on how to group corpus kits.")
    lines.append("> 'Merge' = Plane B lumps together what Plane A separates; 'Split' = reverse.")
    lines.append("")

    # Build per-kit assignments for both planes
    # For each corpus kit, get (commit, family_a, family_b)
    kit_assignments = []
    for kit in corpus_kits:
        commit   = kit["commit_val"] or "instant"
        geo      = kit["geometry_value"]
        family_a, _, _ = geo_to_plane_a(geo)
        b_cols_raw = geo_to_plane_b_cols(geo)
        family_b = b_cols_raw[0] if b_cols_raw else "UNMAPPED"

        kit_assignments.append({
            "kit_id":   kit["kit_id"],
            "folk_name": kit["folk_name"],
            "commit":   commit,
            "geo":      geo,
            "family_a": family_a,
            "family_b": family_b,
            "cell_a": (commit if commit in PLANE_A_ROWS else "instant", family_a),
            "cell_b": (PLANE_B_ROW_TO_COMMIT.get(
                         "SNAP" if (commit in ("instant", None)) else
                         "WIND-UP" if commit == "wind-up" else "CHANNEL",
                         "SNAP"),
                       family_b),
        })

    # Find kits where the plane assignment differs
    # Delta = kits where family_a != semantic-equivalent of family_b
    # Build a canonical A-family→B-family multi-map
    a_to_b = defaultdict(lambda: defaultdict(list))
    for ka in kit_assignments:
        if ka["family_a"] != "UNMAPPED" and ka["family_b"] != "UNMAPPED":
            a_to_b[ka["family_a"]][ka["family_b"]].append(ka)

    lines.append("## Top structural disagreements (ranked by kit count affected)")
    lines.append("")
    lines.append("Each disagreement = kits that Plane A puts in one family cell, "
                 "Plane B puts in a different column.")
    lines.append("")

    # Disagreements: same family_a, but multiple family_b values (A merge / B split)
    # Or multiple family_a, same family_b (B merge / A split)

    # Collect all cross-pairings where family_a ≠ semantic match to family_b
    # Rough semantic equivalents:
    # single → PROJECTILE/MELEE (both)
    # chain → PROJECTILE
    # small_aoe → ZONE/BEAM/ORBITAL
    # large_aoe → NOVA/ZONE/ORBITAL
    # multi_spawn → SUMMON

    # Find disagreements by looking at A-family cells that scatter across B columns
    disagree_entries = []

    for fam_a, b_col_dict in a_to_b.items():
        if len(b_col_dict) > 1:
            # This A-family scatters into multiple B columns → B SPLITS what A groups
            total = sum(len(v) for v in b_col_dict.values())
            b_breakdown = {col: len(kits) for col, kits in b_col_dict.items()}
            example_kits = []
            for kits in b_col_dict.values():
                example_kits.extend(k["folk_name"] or k["kit_id"] for k in kits[:2])
            disagree_entries.append({
                "type": "A-group SPLIT by B",
                "a_family": fam_a,
                "b_breakdown": b_breakdown,
                "total": total,
                "examples": example_kits[:6],
                "direction": f"Plane A groups into `{fam_a}`; Plane B splits across: " +
                             ", ".join(f"`{col}` ({n})" for col, n in sorted(b_breakdown.items(),
                                                                              key=lambda x: -x[1])),
            })

    # Also find: multiple A-families mapping to same B column → A SEPARATES what B merges
    b_to_a = defaultdict(lambda: defaultdict(list))
    for ka in kit_assignments:
        if ka["family_a"] != "UNMAPPED" and ka["family_b"] != "UNMAPPED":
            b_to_a[ka["family_b"]][ka["family_a"]].append(ka)

    for fam_b, a_fam_dict in b_to_a.items():
        if len(a_fam_dict) > 1:
            total = sum(len(v) for v in a_fam_dict.values())
            a_breakdown = {fam: len(kits) for fam, kits in a_fam_dict.items()}
            example_kits = []
            for kits in a_fam_dict.values():
                example_kits.extend(k["folk_name"] or k["kit_id"] for k in kits[:2])
            disagree_entries.append({
                "type": "B-column MERGES A-families",
                "b_family": fam_b,
                "a_breakdown": a_breakdown,
                "total": total,
                "examples": example_kits[:6],
                "direction": f"Plane B `{fam_b}` column merges: " +
                             ", ".join(f"A:`{fam}` ({n})" for fam, n in sorted(a_breakdown.items(),
                                                                                key=lambda x: -x[1])),
            })

    # Sort by total kits affected, descending; take top 10
    disagree_entries.sort(key=lambda x: -x["total"])
    top10 = disagree_entries[:10]

    for i, entry in enumerate(top10, 1):
        lines.append(f"### Disagreement #{i} — {entry['type']} ({entry['total']} kits affected)")
        lines.append("")
        lines.append(f"**{entry['direction']}**")
        lines.append("")
        if "b_breakdown" in entry:
            lines.append(f"Plane A cell: `{entry['a_family']}`")
            lines.append("Plane B distribution:")
            for col, n in sorted(entry["b_breakdown"].items(), key=lambda x: -x[1]):
                lines.append(f"  - `{col}`: {n} kits")
        elif "a_breakdown" in entry:
            lines.append(f"Plane B column: `{entry['b_family']}`")
            lines.append("Plane A distribution:")
            for fam, n in sorted(entry["a_breakdown"].items(), key=lambda x: -x[1]):
                lines.append(f"  - `{fam}`: {n} kits")
        lines.append("")
        if entry["examples"]:
            lines.append(f"Example kits: {', '.join(str(e) for e in entry['examples'][:5])}")
        lines.append("")

    # Overall summary table
    lines.append("---")
    lines.append("")
    lines.append("## Summary: Plane A vs Plane B structural comparison")
    lines.append("")
    lines.append("| Dimension | Plane A (spec) | Plane B (mock) |")
    lines.append("|---|---|---|")
    lines.append("| Total cells | 15 (3×5) | 24 (3×8) |")
    lines.append("| Column axis | 5 dispersion families (Axis 2 canon) | 8 delivery-family columns (visual/gameplay taxonomy) |")
    lines.append("| Row axis | 3 commitment classes (spec §2.2) | 3 classes (SNAP/WIND-UP/CHANNEL) — equivalent |")
    lines.append("| Column overlaps | None (mutually exclusive) | NOVA∩ZONE (circle types); ORBITAL∩RING (ring type) |")
    lines.append("| MELEE separation | Merged into `single` (footprint=1 per hit) | Explicit MELEE column separates contact-range |")
    lines.append("| BEAM separation | Merged into `small_aoe` | Explicit BEAM column separates sustained-linear |")
    lines.append("| SUMMON/ORBITAL | Both in `multi_spawn` | SUMMON and ORBITAL are separate columns |")
    lines.append("| Empty-cell count | See Plane A table above | See Plane B table above |")
    lines.append("")
    lines.append("## Key structural disagreement (single largest)")
    lines.append("")
    if top10:
        top = top10[0]
        lines.append(f"**{top['direction']}** — {top['total']} kits affected.")
        lines.append("")
        lines.append("This is the biggest separation: Plane B's column taxonomy distinguishes "
                     "delivery *mechanism* (projectile vs melee vs orbital) while Plane A's "
                     "Axis 2 measures dispersion *outcome* (how many damage origins, how wide). "
                     "Kits that Plane A groups by similar footprint are scattered by Plane B "
                     "based on how they *look* in motion.")
    lines.append("")

    return "\n".join(lines)


def main():
    print("Loading data...")
    corpus_kits, negative_kits, roster_kits = load_data()

    print("Assigning cells...")
    cells_a  = assign_plane_a(corpus_kits, negative_kits, roster_kits)
    cells_b  = assign_plane_b(corpus_kits, negative_kits, roster_kits)
    roster_a = assign_roster(roster_kits, plane="A")
    roster_b = assign_roster(roster_kits, plane="B")

    print("Generating occupancy-stats.md...")
    stats_md = generate_occupancy_stats(cells_a, cells_b, roster_a, roster_b, corpus_kits, roster_kits)
    (OUT_DIR / "occupancy-stats.md").write_text(stats_md)

    print("Generating rollup-tables.md...")
    rollup_md = generate_rollup_tables()
    (OUT_DIR / "rollup-tables.md").write_text(rollup_md)

    print("Generating delta-findings.md...")
    delta_md = generate_delta_findings(cells_a, cells_b, corpus_kits)
    (OUT_DIR / "delta-findings.md").write_text(delta_md)

    print("Done. All deliverables written.")


if __name__ == "__main__":
    main()
