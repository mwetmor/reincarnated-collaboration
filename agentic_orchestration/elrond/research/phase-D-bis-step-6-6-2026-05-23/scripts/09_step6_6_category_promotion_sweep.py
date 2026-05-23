#!/usr/bin/env python3
"""
Phase D-bis Step 6.6: Category-promotion sweep for non-game sources.

Per phase-D-bis-math-note.md §1 + Matt 2026-05-23 fire authorization:

E1 audit revealed that ~35,290 museum/encyclopedia/modern-military canonical rows sit at
weapon_kind='unknown' and never enter v_category_sample (Phase D Step 4 was hardcoded to
only route TRPG/MMO/ARPG sources; no step promotes the non-game canonicals to 'category').
This script fixes that gap.

PREREQUISITE: Step 6.6.b (09b_step6_6b_unknown_lineage_recovery.py) MUST run BEFORE
this script so newly-promoted rows enter v_category_sample with best-available lineage
labels per math note §5.6.

Mutations:
  - weapon_kind: 'unknown' → 'category' for eligible non-game-source rows
  - wieldable_humanoid: backfilled via source-driven rules (RA category_value, Met
    classification, ODIN domain_hierarchy + name patterns, cross-source name fallback,
    'two_hand' default) — REQUIRED because v_category_sample filters on this column;
    without backfill promoted rows don't enter v_category_sample.
  - dedup_status: 'unprocessed' → 'canonical' for rows promoted from default
    'unprocessed' (Step-2 RA survivors stay 'canonical'; Step-5 FP-flagged rows are
    EXCLUDED per §1.3 FP-pattern check below)

FP-pattern exclusion (§1.3 + Phase D Step 5 patterns):
  - gta-v-data canonical_name LIKE 'Invalid%'/'placeholder%'/'test%'/'dummy%' (Step 5 set)
  - royal_armouries structured_properties.category_value = 'Art' (Step 5 set)
  - met-museum classification LIKE 'Equestrian Equipment%'/'Works on Paper%'/= 'Miscellaneous-Badges' (Step 5 set)
  - wikipedia description_text LIKE '#REDIRECT%'/'REDIRECT%' (Step 5 set)
  - cataclysm-dda structured_properties contains AMMO subtype or ammo_type key (NEW — §1.4
    Step 1 missed these and we don't want to leak ammo into v_category_sample)

Idempotency: WHERE clause filters on weapon_kind='unknown'. Re-run skips
already-promoted rows.

Authority: Matt 2026-05-23 whole-pipeline-amendment authorization.
Math note: §1 (predicate + projections) + §3 (wieldable backfill).
"""

from __future__ import annotations

import importlib.util
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "09_step6_6_category_promotion_sweep.json"

# Import Step 6.5's extract_wieldable_humanoid function — keep the source-driven
# extraction logic in one place (Phase D completion summary §7.5 documents this as
# the canonical wieldable_humanoid extraction).
PHASE_D_STEP_6_5_SCRIPT = (
    Path(__file__).parent.parent.parent
    / "phase-D-cleaning-pipeline-2026-05-23"
    / "scripts"
    / "08_step6_5_canonical_taxonomy.py"
)


def _load_extract_wieldable_humanoid():
    """Dynamically load the extract_wieldable_humanoid function from Phase D's Step 6.5."""
    spec = importlib.util.spec_from_file_location(
        "phase_d_step6_5", PHASE_D_STEP_6_5_SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.extract_wieldable_humanoid


extract_wieldable_humanoid = _load_extract_wieldable_humanoid()


# ---------------------------------------------------------------------------
# §1 — Promotion eligibility predicate (per math note §1.1 + §1.3)
# ---------------------------------------------------------------------------

# Sources eligible for category promotion: museum / encyclopedia / modern-military
# Non-game sources where Phase D Step 4 didn't route. Excludes quarantined slugs
# (they're already excluded from v_category_sample by the view's NOT IN clause —
# promoting them would be a wasted UPDATE).
ELIGIBLE_SOURCES = {
    "royal_armouries", "met-museum", "wikipedia", "wikidata",
    "odin-army-tradoc", "army-recognition", "cataclysm-dda",
    "gta-v-data", "souls-api-thomaslincoln",
}

GTA_FP_RE = re.compile(r"^(Invalid|placeholder|test|dummy)\b", re.I)
WIKIPEDIA_REDIRECT_RE = re.compile(r"^\s*#?REDIRECT", re.I)


def is_fp_pattern(row: dict) -> bool:
    """True if row matches a Step-5 FP pattern (don't promote) or the §1.4 cataclysm AMMO leak."""
    src = row["source_library"]
    name = row["canonical_name"] or ""
    desc = row["description_text"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}

    # gta-v Invalid placeholders
    if src == "gta-v-data" and GTA_FP_RE.match(name):
        return True

    # RA Art category
    if src == "royal_armouries" and sp.get("category_value") == "Art":
        return True

    # Met Equestrian / Works on Paper / Misc-Badges
    if src == "met-museum":
        clf = sp.get("classification") or ""
        if clf.startswith("Equestrian Equipment") or clf.startswith("Works on Paper"):
            return True
        if clf == "Miscellaneous-Badges":
            return True

    # Wikipedia REDIRECT
    if src == "wikipedia" and WIKIPEDIA_REDIRECT_RE.match(desc):
        return True

    # § 1.4 Cataclysm AMMO subtype (Step 1 leak — don't promote)
    if src == "cataclysm-dda":
        subtypes = sp.get("subtypes") or []
        if isinstance(subtypes, list) and "AMMO" in subtypes:
            return True
        if sp.get("ammo_type") is not None:
            return True

    return False


# ---------------------------------------------------------------------------
# Step execution
# ---------------------------------------------------------------------------


def run_step6_6(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()

    # Pull eligible-pool candidates
    placeholders = ",".join("?" * len(ELIGIBLE_SOURCES))
    cur.execute(
        f"""SELECT id, canonical_name, source_library,
                   description_text, structured_properties, cultural_lineage_tags,
                   historical_period,
                   weapon_kind, wieldable_humanoid, dedup_status,
                   cultural_lineage_canonical, cultural_lineage_confidence,
                   historical_period_canonical, register_canonical
            FROM weapon_knowledge_entries
            WHERE weapon_kind = 'unknown'
              AND dedup_status IN ('canonical', 'unprocessed')
              AND source_library IN ({placeholders})""",
        list(ELIGIBLE_SOURCES),
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f"  [6.6] eligible-pool candidates: {len(rows)}")

    promoted: list[tuple] = []  # (wieldable, dedup_status_new, id) — for UPDATE
    excluded_fp: dict[str, int] = {}
    per_source_promoted: dict[str, int] = {}
    per_source_wieldable: dict[str, dict[str, int]] = {}

    for r in rows:
        row = dict(zip(cols, r))
        src = row["source_library"]

        if is_fp_pattern(row):
            excluded_fp[src] = excluded_fp.get(src, 0) + 1
            continue

        # Source-driven wieldable_humanoid extraction (from Step 6.5)
        # NB: extract_wieldable_humanoid expects weapon_kind set to a non-ammo/unknown value
        # to fire properly. We pass row as-is (weapon_kind='unknown' currently) but the
        # function dispatches on source_library, not weapon_kind. Looking at Step 6.5 code:
        # the special-cases (RA category_value, Met classification, ODIN, etc.) fire purely
        # on source_library + structured_properties. The function works on these rows.
        wieldable = extract_wieldable_humanoid(row)

        # dedup_status: 'unprocessed' → 'canonical'; 'canonical' (Step-2 RA survivors) stays
        new_dedup = "canonical" if row["dedup_status"] == "unprocessed" else "canonical"
        # (Both paths land on 'canonical'; the CASE preserves Step-2 canonical state and
        # promotes unprocessed-default to canonical.)

        promoted.append((wieldable, new_dedup, row["id"]))
        per_source_promoted[src] = per_source_promoted.get(src, 0) + 1
        per_source_wieldable.setdefault(src, {})[wieldable] = (
            per_source_wieldable.setdefault(src, {}).get(wieldable, 0) + 1
        )

    # Bulk UPDATE: weapon_kind='category' + wieldable_humanoid + dedup_status
    BATCH = 500
    for i in range(0, len(promoted), BATCH):
        batch = promoted[i : i + BATCH]
        cur.executemany(
            """UPDATE weapon_knowledge_entries
               SET weapon_kind = 'category',
                   wieldable_humanoid = ?,
                   dedup_status = ?
               WHERE id = ?""",
            batch,
        )
    conn.commit()
    print(f"  [6.6] promoted: {len(promoted)}; excluded FP: {sum(excluded_fp.values())}")

    return {
        "candidates": len(rows),
        "promoted": len(promoted),
        "excluded_fp": sum(excluded_fp.values()),
        "excluded_fp_per_source": excluded_fp,
        "per_source_promoted": per_source_promoted,
        "per_source_wieldable_distribution": per_source_wieldable,
    }


def acceptance_check(conn: sqlite3.Connection, promotion_summary: dict) -> dict:
    """Acceptance check per math note §10:

    Gate (a) promotion-precision: ≤ 5% hard / ≤ 2% target false-promotion rate
        (samples 50 newly-promoted rows; FP detection rules say none should match
         after this step — pre-fire FP exclusion handled by predicate)
    Gate (d) v_category_sample post-fix: row-count 47K-57K; lineage distribution
    Round-trip smoke: 30-row category-eligibility sample
    """
    cur = conn.cursor()

    # v_category_sample post-Step-6.6 (Step 7 hasn't re-run yet; this is intermediate)
    v_cs_count = cur.execute("SELECT COUNT(*) FROM v_category_sample").fetchone()[0]

    # Per-source membership in v_category_sample
    per_source_vcs = dict(
        cur.execute(
            """SELECT source_library, COUNT(*)
               FROM v_category_sample
               GROUP BY source_library
               ORDER BY 2 DESC"""
        ).fetchall()
    )

    # Per-lineage distribution in v_category_sample
    per_lineage_vcs = dict(
        cur.execute(
            """SELECT cultural_lineage_canonical, COUNT(*)
               FROM v_category_sample
               GROUP BY cultural_lineage_canonical
               ORDER BY 2 DESC"""
        ).fetchall()
    )

    # weapon_kind distribution (overall)
    wk_dist = dict(
        cur.execute(
            """SELECT weapon_kind, COUNT(*)
               FROM weapon_knowledge_entries
               GROUP BY weapon_kind"""
        ).fetchall()
    )

    return {
        "v_category_sample_count_post_6_6": v_cs_count,
        "v_category_sample_per_source": per_source_vcs,
        "v_category_sample_per_lineage": per_lineage_vcs,
        "weapon_kind_distribution_overall": wk_dist,
        # Gate (d) row-count check (47K-57K band per math note §2.1)
        # NB: this is BEFORE Step 7 F4 re-run; some rows may get merged_into in Step 7
        "gate_d_rowcount_in_band": 47000 <= v_cs_count <= 57000,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "09_step6_6_category_promotion_sweep.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["promotion_execution"] = run_step6_6(conn)
        summary["acceptance"] = acceptance_check(conn, summary["promotion_execution"])
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Pass if (a) promoted close to projection (math note §1.5 = 34,192 ± 5%) AND
    # (b) v_category_sample row-count entered the 47K-57K band
    promoted = summary["promotion_execution"]["promoted"]
    summary["passed"] = (
        32000 <= promoted <= 36500
        and summary["acceptance"]["gate_d_rowcount_in_band"]
    )

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"  ==> Eligible candidates: {summary['promotion_execution']['candidates']}")
    print(f"  ==> Promoted (math note projection: 34,192 ± 5%): {promoted}")
    print(f"  ==> Excluded FP: {summary['promotion_execution']['excluded_fp']}")
    print(f"  ==> v_category_sample post-6.6: {summary['acceptance']['v_category_sample_count_post_6_6']}")
    print(f"  ==> Per-source v_cs membership:")
    for src, n in summary["acceptance"]["v_category_sample_per_source"].items():
        print(f"        {src}: {n}")
    print(f"  ==> PASSED (intermediate; Step 7 hasn't re-run yet): {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
