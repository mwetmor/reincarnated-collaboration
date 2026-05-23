#!/usr/bin/env python3
"""
Phase D-bis Step 7 F4 re-run wrapper.

Per phase-D-bis-math-note.md §6 + dispatch §Scope:

The Step 7 F4 cross-source merge logic from Phase D needs to re-fire against the
enlarged candidate pool (post-Step-6.6 promotion adds ~34,200 newly-eligible
category rows to the pairwise-comparison pool).

This script:
  1. Imports the Phase D Step 7 module (preserves all algorithm fidelity — same
     blocking, same lane router, same name_sim + TF-IDF cosine, same G2-principle
     auto-disposition).
  2. Re-runs run_step7() against the post-Step-6.6 DB state. Existing 1,194
     canonical-merge entries are preserved by the script's INSERT OR IGNORE pattern
     and idempotency guards.
  3. Writes flagged-clusters output to THIS directory's phase-D-bis-flagged-clusters.md
     (does NOT clobber Phase D's flagged-clusters.md).
  4. Logs per-step summary + acceptance audit for the Step 7 stability gate.

Idempotency: per Phase D math note §4 — Step 7 is idempotent over already-merged rows
(WHERE clause skips merged_into; UNIQUE constraint on canonical_name skips dup INSERTs).

Authority: Matt 2026-05-23 fire authorization (in-scope per dispatch §Scope).
"""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "10_step7_f4_rerun.json"
FLAGGED_CLUSTERS_PATH_BIS = Path(__file__).parent.parent / "phase-D-bis-flagged-clusters.md"

PHASE_D_STEP_7_SCRIPT = (
    Path(__file__).parent.parent.parent
    / "phase-D-cleaning-pipeline-2026-05-23"
    / "scripts"
    / "09_step7_f4_cross_source_merge.py"
)


def _load_step7_module():
    spec = importlib.util.spec_from_file_location("phase_d_step7", PHASE_D_STEP_7_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def baseline_state(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    return {
        "canonical_merge_total_pre": cur.execute(
            "SELECT COUNT(*) FROM knowledge_entry_canonical_merge"
        ).fetchone()[0],
        "f4_merges_pre": cur.execute(
            "SELECT COUNT(*) FROM knowledge_entry_canonical_merge WHERE merge_strategy = 'F4_cross_source_merge'"
        ).fetchone()[0],
        "canonical_count_pre": cur.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='canonical'"
        ).fetchone()[0],
        "merged_into_count_pre": cur.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='merged_into'"
        ).fetchone()[0],
        "v_category_sample_count_pre": cur.execute(
            "SELECT COUNT(*) FROM v_category_sample"
        ).fetchone()[0],
    }


def post_state(conn: sqlite3.Connection, baseline: dict) -> dict:
    cur = conn.cursor()
    return {
        "canonical_merge_total_post": cur.execute(
            "SELECT COUNT(*) FROM knowledge_entry_canonical_merge"
        ).fetchone()[0],
        "f4_merges_post": cur.execute(
            "SELECT COUNT(*) FROM knowledge_entry_canonical_merge WHERE merge_strategy = 'F4_cross_source_merge'"
        ).fetchone()[0],
        "canonical_count_post": cur.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='canonical'"
        ).fetchone()[0],
        "merged_into_count_post": cur.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE dedup_status='merged_into'"
        ).fetchone()[0],
        "v_category_sample_count_post": cur.execute(
            "SELECT COUNT(*) FROM v_category_sample"
        ).fetchone()[0],
        # Stability metric per math note §10.3 Gate (c)
        "delta_canonical_merge_entries": (
            cur.execute("SELECT COUNT(*) FROM knowledge_entry_canonical_merge").fetchone()[0]
            - baseline["canonical_merge_total_pre"]
        ),
        "delta_f4_merges": (
            cur.execute(
                "SELECT COUNT(*) FROM knowledge_entry_canonical_merge WHERE merge_strategy = 'F4_cross_source_merge'"
            ).fetchone()[0]
            - baseline["f4_merges_pre"]
        ),
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "10_step7_f4_rerun.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    # Import Phase D Step 7 module + patch the flagged-clusters output path
    step7_mod = _load_step7_module()
    step7_mod.FLAGGED_CLUSTERS_PATH = FLAGGED_CLUSTERS_PATH_BIS

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["baseline"] = baseline_state(conn)
        print(f"  [step7-rerun] BASELINE:")
        for k, v in summary["baseline"].items():
            print(f"        {k}: {v}")
        # Fire the Phase D Step 7 logic (run_step7 returns its own summary dict)
        step7_result = step7_mod.run_step7(conn)
        summary["step7_execution"] = step7_result
        summary["post"] = post_state(conn, summary["baseline"])
        print(f"  [step7-rerun] POST:")
        for k, v in summary["post"].items():
            print(f"        {k}: {v}")
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Acceptance per math note §10.3 Gate (c) Step 7 F4 stability:
    # - Existing 1,194 canonical-merge entries preserved
    # - delta_canonical_merge is positive (additive only)
    # - v_category_sample didn't shrink dramatically (some shrink expected as new
    #   F4 merges demote some canonical → merged_into)
    base = summary["baseline"]
    post = summary["post"]
    preserved = post["canonical_merge_total_post"] >= base["canonical_merge_total_pre"]
    additive_only = post["delta_canonical_merge_entries"] >= 0
    vcs_shrinkage_pct = 100.0 * (1.0 - post["v_category_sample_count_post"] / max(1, base["v_category_sample_count_pre"]))
    vcs_stable = vcs_shrinkage_pct <= 5.0  # allow up to 5% shrinkage from new merges

    summary["acceptance"] = {
        "gate_c_canonical_merge_preserved": preserved,
        "gate_c_additive_only": additive_only,
        "vcs_shrinkage_pct_from_pre_step7": round(vcs_shrinkage_pct, 2),
        "vcs_stable_within_5pct_shrinkage": vcs_stable,
    }
    summary["passed"] = preserved and additive_only and vcs_stable

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"  ==> Pre-existing canonical_merge entries preserved: {preserved}")
    print(f"  ==> Step 7 additive only (delta ≥ 0): {additive_only}")
    print(f"  ==> v_category_sample shrinkage from pre-Step-7 state: {vcs_shrinkage_pct:.2f}% (≤5% target)")
    print(f"  ==> Delta canonical-merge entries: {post['delta_canonical_merge_entries']}")
    print(f"  ==> Delta F4 cross-source merges: {post['delta_f4_merges']}")
    print(f"  ==> PASSED: {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
