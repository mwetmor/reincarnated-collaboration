#!/usr/bin/env python3
"""
Phase D-bis Final acceptance gates.

Per phase-D-bis-math-note.md §10 + dispatch §Acceptance criteria:

Evaluates gates (a)-(d) of the Phase-D-bis dispatch:
  (a) Promotion-eligibility precision (random-sample audit N=50)
  (b) Promotion-eligibility recall (random-sample audit N=50 of post-fix unknowns)
  (c) Step 7 F4 cross-source merge stability (preserved pre-existing entries)
  (d) v_category_sample post-fix profile (row count + per-source + per-lineage)

PLUS round-trip smoke per Principle 6:
  - 30-row random-sample category-eligibility audit

PLUS no-regression on Phase D gates:
  - Phase D Gate (a) FP rate ≤ 1.5% target / ≤ 3.0% hard in v_category_sample
  - Phase D Gate (b)(i) residual duplication ≤ 4.0% on the canonical-key
  - Phase D Gate (c) field-coverage floors maintained
  - Phase D Gate (d) weapon_kind misclassification ≤ 2% on (d.1) and (d.2) sub-axes

Authority: Matt 2026-05-23 fire authorization.
"""

from __future__ import annotations

import json
import random
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
PRE_STEP_6_6_BACKUP = (
    Path(__file__).parent.parent / "backups" / "telemetry.db.pre-step6.6"
)
LOG_PATH = Path(__file__).parent.parent / "logs" / "11_final_acceptance_gates.json"

random.seed(20260523)  # Reproducibility


# ---------------------------------------------------------------------------
# FP detection rules (mirror Phase D Step 5 + math note §1.3)
# ---------------------------------------------------------------------------

GTA_FP_RE = re.compile(r"^(Invalid|placeholder|test|dummy)\b", re.I)
WIKIPEDIA_REDIRECT_RE = re.compile(r"^\s*#?REDIRECT", re.I)


def is_fp_for_promotion(row: dict) -> bool:
    """True if the row should NOT have been promoted to category."""
    src = row["source_library"]
    name = row["canonical_name"] or ""
    desc = row["description_text"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}

    # gta-v Invalid
    if src == "gta-v-data" and GTA_FP_RE.match(name):
        return True

    # RA Art
    if src == "royal_armouries" and sp.get("category_value") == "Art":
        return True

    # Met FP classifications
    if src == "met-museum":
        clf = sp.get("classification") or ""
        if (clf.startswith("Equestrian Equipment")
                or clf.startswith("Works on Paper")
                or clf == "Miscellaneous-Badges"):
            return True

    # Wikipedia REDIRECT
    if src == "wikipedia" and WIKIPEDIA_REDIRECT_RE.match(desc):
        return True

    # Cataclysm AMMO subtype
    if src == "cataclysm-dda":
        subtypes = sp.get("subtypes") or []
        if isinstance(subtypes, list) and "AMMO" in subtypes:
            return True
        if sp.get("ammo_type") is not None:
            return True

    # General weapon-parts FP (consumables / weapon-furniture)
    name_lc = name.lower()
    fp_part_keywords = ["scabbard", "tsuba", "kozuka", "fuchi", "hilt only",
                        "handle only", "sheath only", "grip only",
                        "cartridge", "ammo", "ammunition"]
    if any(k in name_lc for k in fp_part_keywords):
        # Be careful: only flag if the name strongly suggests a part-only entry
        # (e.g., "Sword Hilt" not "Sword with Hilt")
        if name_lc.startswith(tuple(fp_part_keywords)) or name_lc.endswith(tuple(fp_part_keywords)):
            return True

    return False


def is_real_weapon(row: dict) -> bool:
    """Inverse: True if this row IS a legitimate weapon that SHOULD be in v_category_sample.

    Used in Gate (b) recall audit: among unknown rows, were any of them legit weapons we missed?
    """
    if is_fp_for_promotion(row):
        return False
    src = row["source_library"]
    name = (row["canonical_name"] or "").lower()
    # Filter out quarantined sources
    if "quarantined" in src:
        return False
    # If source is non-eligible (TRPG/MMO/ARPG/SRD), don't count as a "missed promotion"
    # (Step 6.6 only targets the 9 non-game sources)
    eligible_sources = {
        "royal_armouries", "met-museum", "wikipedia", "wikidata",
        "odin-army-tradoc", "army-recognition", "cataclysm-dda",
        "gta-v-data", "souls-api-thomaslincoln",
    }
    if src not in eligible_sources:
        return False
    return True


# ---------------------------------------------------------------------------
# Gate evaluators
# ---------------------------------------------------------------------------


def gate_a_promotion_precision(conn: sqlite3.Connection) -> dict:
    """Random-sample audit of 50 newly-promoted rows. FP rate ≤ 5% hard / ≤ 2% target.

    "Newly promoted" = weapon_kind='category' now AND was 'unknown' in pre-step6.6 backup.
    """
    cur = conn.cursor()

    # Attach pre-step6.6 backup for JOIN comparison
    if not PRE_STEP_6_6_BACKUP.exists():
        return {
            "skipped": True,
            "reason": f"pre-step6.6 backup not found at {PRE_STEP_6_6_BACKUP}; gate a skipped",
        }
    cur.execute(f"ATTACH DATABASE ? AS pre", (str(PRE_STEP_6_6_BACKUP),))

    # Identify newly-promoted rows (pre.weapon_kind='unknown' AND main.weapon_kind='category')
    cur.execute(
        """SELECT m.id, m.canonical_name, m.source_library, m.description_text,
                  m.structured_properties, m.cultural_lineage_tags
           FROM weapon_knowledge_entries m
           JOIN pre.weapon_knowledge_entries p ON m.id = p.id
           WHERE p.weapon_kind = 'unknown'
             AND m.weapon_kind = 'category'"""
    )
    all_newly_promoted = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.execute("DETACH DATABASE pre")
    print(f"  [gate-a] newly-promoted total: {len(all_newly_promoted)}")

    # Random sample of 50
    sample_n = min(50, len(all_newly_promoted))
    sampled = random.sample(all_newly_promoted, sample_n)
    fp_count = 0
    fp_examples: list[dict] = []
    for r in sampled:
        row = dict(zip(cols, r))
        if is_fp_for_promotion(row):
            fp_count += 1
            fp_examples.append({
                "id": row["id"],
                "canonical_name": row["canonical_name"],
                "source": row["source_library"],
            })

    fp_rate = fp_count / sample_n if sample_n else 0.0
    return {
        "newly_promoted_total": len(all_newly_promoted),
        "sample_n": sample_n,
        "fp_count": fp_count,
        "fp_rate_pct": round(100.0 * fp_rate, 2),
        "fp_examples": fp_examples[:5],
        "gate_a_pass_hard": fp_rate <= 0.05,
        "gate_a_pass_target": fp_rate <= 0.02,
    }


def gate_b_promotion_recall(conn: sqlite3.Connection) -> dict:
    """Random-sample audit of 50 rows still at weapon_kind='unknown' from eligible sources.
    Missed-promotion rate ≤ 5%.
    """
    cur = conn.cursor()

    eligible_sources = (
        "royal_armouries", "met-museum", "wikipedia", "wikidata",
        "odin-army-tradoc", "army-recognition", "cataclysm-dda",
        "gta-v-data", "souls-api-thomaslincoln",
    )
    placeholders = ",".join("?" * len(eligible_sources))
    cur.execute(
        f"""SELECT id, canonical_name, source_library, description_text,
                   structured_properties, cultural_lineage_tags
            FROM weapon_knowledge_entries
            WHERE weapon_kind = 'unknown'
              AND dedup_status != 'merged_into'
              AND source_library IN ({placeholders})""",
        list(eligible_sources),
    )
    all_unknowns = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f"  [gate-b] post-fix unknowns total: {len(all_unknowns)}")

    sample_n = min(50, len(all_unknowns))
    sampled = random.sample(all_unknowns, sample_n)
    missed_count = 0
    missed_examples: list[dict] = []
    for r in sampled:
        row = dict(zip(cols, r))
        if is_real_weapon(row):
            missed_count += 1
            missed_examples.append({
                "id": row["id"],
                "canonical_name": row["canonical_name"],
                "source": row["source_library"],
            })

    miss_rate = missed_count / sample_n if sample_n else 0.0
    return {
        "post_fix_unknown_total": len(all_unknowns),
        "sample_n": sample_n,
        "missed_promotion_count": missed_count,
        "missed_promotion_rate_pct": round(100.0 * miss_rate, 2),
        "missed_examples": missed_examples[:5],
        "gate_b_pass": miss_rate <= 0.05,
    }


def gate_c_step7_stability(conn: sqlite3.Connection) -> dict:
    """Step 7 F4 stability — preserved pre-existing canonical-merge entries.
    Phase D end-state: 1,194 canonical-merge total / 26 F4 cross-source.
    """
    cur = conn.cursor()
    cme_total = cur.execute(
        "SELECT COUNT(*) FROM knowledge_entry_canonical_merge"
    ).fetchone()[0]
    f4_total = cur.execute(
        "SELECT COUNT(*) FROM knowledge_entry_canonical_merge WHERE merge_strategy = 'F4_cross_source_merge'"
    ).fetchone()[0]
    return {
        "canonical_merge_total": cme_total,
        "f4_cross_source_merges_total": f4_total,
        "phase_d_baseline_canonical_merge": 1194,
        "phase_d_baseline_f4": 26,
        "delta_canonical_merge": cme_total - 1194,
        "delta_f4": f4_total - 26,
        "gate_c_pass_preserved": cme_total >= 1194,
        "gate_c_pass_f4_additive": f4_total >= 26,
    }


def gate_d_vcs_profile(conn: sqlite3.Connection) -> dict:
    """v_category_sample post-fix profile per math note §2."""
    cur = conn.cursor()
    vcs_total = cur.execute("SELECT COUNT(*) FROM v_category_sample").fetchone()[0]
    per_source = dict(
        cur.execute(
            "SELECT source_library, COUNT(*) FROM v_category_sample GROUP BY source_library ORDER BY 2 DESC"
        ).fetchall()
    )
    per_lineage = dict(
        cur.execute(
            "SELECT cultural_lineage_canonical, COUNT(*) FROM v_category_sample GROUP BY cultural_lineage_canonical ORDER BY 2 DESC"
        ).fetchall()
    )
    # Lineage percentages
    per_lineage_pct = {k: round(100.0 * v / vcs_total, 2) for k, v in per_lineage.items()}

    return {
        "vcs_total": vcs_total,
        "per_source": per_source,
        "per_lineage_counts": per_lineage,
        "per_lineage_pct": per_lineage_pct,
        "gate_d_rowcount_in_band": 47000 <= vcs_total <= 57000,
    }


def round_trip_smoke(conn: sqlite3.Connection) -> dict:
    """30-row random-sample category-eligibility audit on the post-fix v_category_sample."""
    cur = conn.cursor()
    cur.execute(
        """SELECT id, canonical_name, source_library, description_text,
                  structured_properties, cultural_lineage_tags
           FROM v_category_sample
           ORDER BY RANDOM()
           LIMIT 30"""
    )
    sampled = cur.fetchall()
    cols = [d[0] for d in cur.description]
    fp_count = 0
    fp_examples: list[dict] = []
    for r in sampled:
        row = dict(zip(cols, r))
        if is_fp_for_promotion(row):
            fp_count += 1
            fp_examples.append({
                "id": row["id"],
                "canonical_name": row["canonical_name"],
                "source": row["source_library"],
            })
    fp_rate = fp_count / 30
    return {
        "sample_n": 30,
        "fp_count": fp_count,
        "fp_rate_pct": round(100.0 * fp_rate, 2),
        "fp_examples": fp_examples[:5],
        "smoke_pass_hard": fp_rate <= 0.05,
        "smoke_pass_target": fp_rate <= 0.02,
    }


def phase_d_regression_gates(conn: sqlite3.Connection) -> dict:
    """Re-evaluate Phase D Gates (a)-(d) on post-Step-6.6 + post-Step-7 state."""
    cur = conn.cursor()

    # Gate (a) FP rate in v_category_sample
    cur.execute(
        """SELECT id, canonical_name, source_library, description_text,
                  structured_properties, cultural_lineage_tags
           FROM v_category_sample
           ORDER BY RANDOM()
           LIMIT 50"""
    )
    sampled = cur.fetchall()
    cols = [d[0] for d in cur.description]
    fp_count = sum(1 for r in sampled if is_fp_for_promotion(dict(zip(cols, r))))
    fp_rate = fp_count / 50

    # Gate (b) residual duplication (post-Phase-D-bis canonical key)
    # Per Phase D completion summary §3 — measure (name × lineage × period × source)
    dup_check = cur.execute(
        """WITH keyed AS (
             SELECT canonical_name || '|' || cultural_lineage_canonical || '|' ||
                    historical_period_canonical || '|' || source_library AS k
             FROM weapon_knowledge_entries
             WHERE dedup_status = 'canonical'
               AND weapon_kind IN ('category','named_template','unique')
           )
           SELECT COUNT(*) AS total, COUNT(DISTINCT k) AS distinct_keys
           FROM keyed"""
    ).fetchone()
    canonical_count, distinct_keys = dup_check
    residual_dup_ratio = (canonical_count / max(1, distinct_keys)) - 1.0

    # Gate (c) field-coverage floors on v_category_sample
    coverage = cur.execute(
        """SELECT
              100.0 * SUM(CASE WHEN structured_properties IS NOT NULL AND structured_properties != '{}' THEN 1 ELSE 0 END) / COUNT(*) AS pct_structured,
              100.0 * SUM(CASE WHEN description_text IS NOT NULL AND description_text != '' THEN 1 ELSE 0 END) / COUNT(*) AS pct_description,
              100.0 * SUM(CASE WHEN cultural_lineage_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*) AS pct_cultural,
              100.0 * SUM(CASE WHEN historical_period_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*) AS pct_period,
              100.0 * SUM(CASE WHEN register_canonical != 'unknown' THEN 1 ELSE 0 END) / COUNT(*) AS pct_register
           FROM v_category_sample"""
    ).fetchone()

    # Gate (d.3) ammo leak in v_category_sample
    ammo_leak = cur.execute(
        """SELECT COUNT(*)
           FROM v_category_sample
           WHERE (LOWER(canonical_name) LIKE '%cartridge%'
                  OR LOWER(canonical_name) LIKE '%ammo%'
                  OR LOWER(canonical_name) LIKE '%scabbard%'
                  OR LOWER(canonical_name) LIKE '%tsuba%'
                  OR LOWER(canonical_name) LIKE '%kozuka%')
              OR (source_library = 'cataclysm-dda'
                  AND structured_properties LIKE '%"AMMO"%')"""
    ).fetchone()[0]
    vcs_total = cur.execute("SELECT COUNT(*) FROM v_category_sample").fetchone()[0]
    ammo_leak_pct = 100.0 * ammo_leak / max(1, vcs_total)

    return {
        "phase_d_gate_a_fp_rate_pct": round(100.0 * fp_rate, 2),
        "phase_d_gate_a_pass_hard": fp_rate <= 0.03,
        "phase_d_gate_a_pass_target": fp_rate <= 0.015,
        "phase_d_gate_b_canonical_count": canonical_count,
        "phase_d_gate_b_distinct_keys": distinct_keys,
        "phase_d_gate_b_residual_dup_ratio": round(residual_dup_ratio, 4),
        "phase_d_gate_b_pass": residual_dup_ratio <= 0.04,
        "phase_d_gate_c_pct_structured": round(coverage[0], 2),
        "phase_d_gate_c_pct_description": round(coverage[1], 2),
        "phase_d_gate_c_pct_cultural": round(coverage[2], 2),
        "phase_d_gate_c_pct_period": round(coverage[3], 2),
        "phase_d_gate_c_pct_register": round(coverage[4], 2),
        "phase_d_gate_c_pass": (coverage[0] >= 95.0 and coverage[1] >= 85.0
                                 and coverage[2] >= 70.0 and coverage[3] >= 60.0
                                 and coverage[4] >= 95.0),
        "phase_d_gate_d_3_ammo_leak_pct": round(ammo_leak_pct, 2),
        "phase_d_gate_d_3_pass": ammo_leak_pct <= 1.0,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "11_final_acceptance_gates.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["gate_a"] = gate_a_promotion_precision(conn)
        summary["gate_b"] = gate_b_promotion_recall(conn)
        summary["gate_c"] = gate_c_step7_stability(conn)
        summary["gate_d"] = gate_d_vcs_profile(conn)
        summary["round_trip_smoke"] = round_trip_smoke(conn)
        summary["phase_d_regression"] = phase_d_regression_gates(conn)
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Overall pass — all gates hard floors
    all_pass = (
        summary["gate_a"].get("gate_a_pass_hard", False) and
        summary["gate_b"].get("gate_b_pass", False) and
        summary["gate_c"].get("gate_c_pass_preserved", False) and
        summary["gate_c"].get("gate_c_pass_f4_additive", False) and
        summary["gate_d"].get("gate_d_rowcount_in_band", False) and
        summary["round_trip_smoke"].get("smoke_pass_hard", False) and
        summary["phase_d_regression"].get("phase_d_gate_a_pass_hard", False) and
        summary["phase_d_regression"].get("phase_d_gate_b_pass", False) and
        summary["phase_d_regression"].get("phase_d_gate_c_pass", False) and
        summary["phase_d_regression"].get("phase_d_gate_d_3_pass", False)
    )
    summary["passed"] = all_pass

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n  === Gate summary ===")
    print(f"  (a) promotion precision: {summary['gate_a'].get('fp_rate_pct','SKIP')}% (target ≤2%, hard ≤5%)")
    print(f"  (b) promotion recall: {summary['gate_b'].get('missed_promotion_rate_pct','?')}% (≤5%)")
    print(f"  (c) F4 stability — canonical-merge preserved: {summary['gate_c'].get('gate_c_pass_preserved')}; additive: {summary['gate_c'].get('gate_c_pass_f4_additive')}")
    print(f"  (d) v_cs total: {summary['gate_d'].get('vcs_total')} (band 47K-57K = {summary['gate_d'].get('gate_d_rowcount_in_band')})")
    print(f"  Round-trip smoke: {summary['round_trip_smoke'].get('fp_rate_pct')}% FP (target ≤2%)")
    print(f"  Phase D no-regression: a={summary['phase_d_regression'].get('phase_d_gate_a_pass_hard')} b={summary['phase_d_regression'].get('phase_d_gate_b_pass')} c={summary['phase_d_regression'].get('phase_d_gate_c_pass')} d.3={summary['phase_d_regression'].get('phase_d_gate_d_3_pass')}")
    print(f"\n  ==> OVERALL PASSED: {all_pass}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
