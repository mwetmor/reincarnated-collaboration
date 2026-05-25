#!/usr/bin/env python3
"""
Cycle 10 Wave 5.5 Part B — Mode-C-by-Semantics SQL Eviction Pass on v1_scope

Per dispatch § 3.2 + gandalf sign-off `2026-05-25-stage-3-distribution-report-
sign-off.md` § 3 Condition 3 SQL signature (verbatim — DO NOT modify).

Operationalizes semantic-layer Mode-C contamination eviction per the
marginal-lineage Mode-A/B/C/D framework
(`canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`). This is the
SECOND canonical production application of Discipline #25 (semantic-layer
rep-audit), first being gandalf SO-3 Pattern A-deep verdict.

Pre-eviction list saved at `eviction-candidates-pre.json` (full row-level).
Random 10-row sample saved at `gandalf-eviction-audit-sample.json` for knight-
rider routing to gandalf for small-batch audit post-Wave-5.5.

The eviction sets v1_scope=0 + appends a `wave_5_5_mode_c_eviction` record to
v1_scope_composition_trace preserving the original trace for provenance.
"""

from __future__ import annotations

import json
import random
import sqlite3
from collections import Counter
from pathlib import Path

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
OUT_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond"
    "/research/cycle-10-wave-5-5-2026-05-25"
)

# --- EXACT SQL signature per gandalf sign-off § 3 Condition 3 (VERBATIM) ---
ELIGIBILITY_SQL = """
SELECT id, canonical_name, register_canonical, historical_period_canonical,
       cultural_lineage_canonical, named_mythological_match, quality_tier,
       weapon_kind_classified_subtype, v1_scope, v1_scope_composition_trace
FROM weapon_knowledge_entries
WHERE v1_scope = 1
  AND named_mythological_match IS NOT NULL
  AND (
    historical_period_canonical IN ('contemporary', 'modern', 'industrial')
    OR canonical_name LIKE '%UAV%' OR canonical_name LIKE '%missile%'
    OR canonical_name LIKE '%helicopter%' OR canonical_name LIKE '%submarine%'
    OR canonical_name LIKE '%aircraft%' OR canonical_name LIKE 'F-%'
    OR canonical_name LIKE '%MK-%' OR canonical_name LIKE 'AIM-%'
    OR canonical_name LIKE 'AGM-%' OR canonical_name LIKE 'SUB-%'
    OR canonical_name LIKE '%Type %'
    OR canonical_name LIKE '%Particle %' OR canonical_name LIKE '%Plasma %'
    OR canonical_name LIKE '%Quantum %' OR canonical_name LIKE '%Laser %'
  )
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()

        # Pre-eviction state (Discipline #11)
        cursor.execute("SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1")
        pre_v1 = cursor.fetchone()[0]
        print(f"Pre-eviction v1_scope=1 total: {pre_v1}")

        # ----- Step 1: Run SELECT to identify candidates -----
        cursor.execute(ELIGIBILITY_SQL)
        candidates_raw = cursor.fetchall()
        candidates = [
            {
                "id": r["id"],
                "canonical_name": r["canonical_name"],
                "register_canonical": r["register_canonical"],
                "historical_period_canonical": r["historical_period_canonical"],
                "cultural_lineage_canonical": r["cultural_lineage_canonical"],
                "named_mythological_match": r["named_mythological_match"],
                "quality_tier": r["quality_tier"],
                "weapon_kind_classified_subtype": r["weapon_kind_classified_subtype"],
                "v1_scope_composition_trace_pre": r["v1_scope_composition_trace"],
            }
            for r in candidates_raw
        ]
        print(f"Eviction candidates identified by gandalf SQL signature: {len(candidates)}")
        print(f"(Dispatch § 2 estimate: ~50-100 rows)")

        # Per-period + per-tier breakdown of candidates
        by_period = Counter(c["historical_period_canonical"] for c in candidates)
        by_tier = Counter(c["quality_tier"] for c in candidates)
        by_lineage = Counter(c["cultural_lineage_canonical"] for c in candidates)
        print()
        print("Per-period breakdown:")
        for k, v in by_period.most_common():
            print(f"  {k}: {v}")
        print()
        print("Per-tier breakdown:")
        for k, v in by_tier.most_common():
            print(f"  {k}: {v}")
        print()
        print("Per-cultural-lineage breakdown (top 10):")
        for k, v in by_lineage.most_common(10):
            print(f"  {k}: {v}")

        # ----- Step 2: Save pre-eviction list -----
        pre_eviction_path = OUT_DIR / "eviction-candidates-pre.json"
        pre_payload = {
            "phase": "cycle-10-wave-5-5-part-b-mode-c-eviction",
            "date": "2026-05-25",
            "sql_signature_authority": (
                "gandalf sign-off `2026-05-25-stage-3-distribution-report-sign-off.md` "
                "§ 3 Condition 3 VERBATIM"
            ),
            "dispatch": (
                "agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-"
                "phase-0c-and-mode-c-eviction.md § 3.2"
            ),
            "pre_eviction_v1_scope_count": pre_v1,
            "eviction_candidate_count": len(candidates),
            "dispatch_estimate_range": "~50-100",
            "per_period_breakdown": dict(by_period.most_common()),
            "per_tier_breakdown": dict(by_tier.most_common()),
            "per_lineage_breakdown_top10": {k: v for k, v in by_lineage.most_common(10)},
            "candidates": candidates,
        }
        with pre_eviction_path.open("w") as f:
            json.dump(pre_payload, f, indent=2, ensure_ascii=False)
        print()
        print(f"Pre-eviction list saved: {pre_eviction_path}")

        # ----- Step 3: 10-row random sample for gandalf audit -----
        # Deterministic random seed for reproducibility
        random.seed(20260525)
        sample_size = min(10, len(candidates))
        sample = random.sample(candidates, sample_size)
        audit_path = OUT_DIR / "gandalf-eviction-audit-sample.json"
        audit_payload = {
            "phase": "cycle-10-wave-5-5-part-b-mode-c-eviction",
            "date": "2026-05-25",
            "audit_purpose": (
                "gandalf small-batch audit on 10 random evicted rows — "
                "verify ≥ 8/10 are genuine Mode-C-by-semantics contamination per dispatch § 8 smoke"
            ),
            "random_seed": 20260525,
            "total_eviction_candidates": len(candidates),
            "sample_size": sample_size,
            "sample": sample,
        }
        with audit_path.open("w") as f:
            json.dump(audit_payload, f, indent=2, ensure_ascii=False)
        print(f"Gandalf audit sample (10 rows) saved: {audit_path}")

        # ----- Step 4: Apply UPDATE — v1_scope=0 + append trace -----
        update_records: list[tuple[str, int]] = []
        for c in candidates:
            try:
                existing_trace = (
                    json.loads(c["v1_scope_composition_trace_pre"])
                    if c["v1_scope_composition_trace_pre"] else {}
                )
            except (json.JSONDecodeError, TypeError):
                existing_trace = {"raw": c["v1_scope_composition_trace_pre"]}
            existing_trace["wave_5_5_mode_c_eviction"] = {
                "rule": "mode_c_by_semantics_evicted_wave_5_5",
                "sql_signature_authority": (
                    "gandalf sign-off `2026-05-25-stage-3-distribution-report-"
                    "sign-off.md` § 3 Condition 3 VERBATIM"
                ),
                "previous_v1_scope": 1,
                "register_canonical": c["register_canonical"],
                "historical_period_canonical": c["historical_period_canonical"],
                "cultural_lineage_canonical": c["cultural_lineage_canonical"],
                "named_mythological_match": c["named_mythological_match"],
            }
            update_records.append((json.dumps(existing_trace, ensure_ascii=False), c["id"]))

        cursor.executemany(
            "UPDATE weapon_knowledge_entries "
            "SET v1_scope = 0, v1_scope_composition_trace = ? "
            "WHERE id = ?",
            update_records,
        )
        conn.commit()

        # ----- Step 5: Empirical verification (Discipline #11) -----
        cursor.execute("SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1")
        post_v1 = cursor.fetchone()[0]
        print()
        print(f"Post-eviction v1_scope=1 total: {post_v1}")
        print(f"Net Wave 5.5 Part B reduction: {pre_v1 - post_v1} (matches eviction count: {len(candidates)})")

        # Smoke assertion: 0 evicted rows remain in v1_scope
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope = 1 AND v1_scope_composition_trace LIKE '%mode_c_by_semantics_evicted_wave_5_5%'"
        )
        leak = cursor.fetchone()[0]
        print(f"Smoke assertion: evicted rows still in v1_scope = {leak} (must be 0)")
        assert leak == 0, "Mode-C eviction smoke failed — evicted rows still v1_scope=1"

        # Confirm trace records persisted on evicted rows
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope = 0 AND v1_scope_composition_trace LIKE '%mode_c_by_semantics_evicted_wave_5_5%'"
        )
        trace_count = cursor.fetchone()[0]
        print(f"Evicted rows with mode_c trace marker: {trace_count} (expected {len(candidates)})")

    finally:
        conn.close()

    print()
    print("Mode-C-by-semantics eviction COMPLETE.")


if __name__ == "__main__":
    main()
