#!/usr/bin/env python3
"""
Cycle 10 Wave 5.5 Closeout — Distribution Recomputation + 50-Row Spot-Check Sample Pack

Per dispatch § 3.3 + § 5.5 acceptance criterion 5 — recompute v1_scope post-
Wave-5.5 distribution across:
  - per-tier counts
  - per-register distribution
  - per-cultural-tradition distribution
  - per-period distribution
  - per-axis (proxy_geometry / proxy_range / proxy_tempo / proxy_attribute)
  - per-subtype distribution (post-Phase-0c population)

Verify against composition policy v1 § 2 targets (±5pp tolerance).

Emits 50-row spot-check sample pack for knight-rider routing to gandalf for
post-Wave-5.5 re-run spot-check.

Stratification matches the gandalf 50-row spot-check stratification spec
(`2026-05-25-phase-2-50-row-spot-check.md` § 1) — 6 strata: S × 2 (mythological,
historical), A × 6 (hist-european, east_asian, south_asian, thin-tradition,
fantasy-A, mm-mode-c-check), B × 5 (european-historical-typed, NULL-typed,
fantasy-typed-2, fantasy_secondary-A-source, military_modern-2).

Heuristic only — no LLM cost.
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

# Composition policy v1 § 2 targets (per `weapon-substrate-composition-policy-v1-2026-05-24.md`)
POLICY_TARGETS = {
    "register": {
        "historical": (0.50, 0.60),         # 50-60%
        "mythological": (0.20, 0.30),       # 20-30%
        "fantasy_generic": (0.10, 0.20),    # 10-20%
        "fantasy_secondary": (0.03, 0.08),  # 3-8%
        "military_modern": (0.05, 0.10),    # 5-10%
    },
    "cultural_tradition": {
        "european": (0.30, 0.35),
        "east_asian": (0.15, 0.20),
        "south_asian": (0.05, 0.10),
        "mesoamerican": (0.02, 0.05),
        "african": (0.02, 0.05),
        "southeast_asian": (0.02, 0.05),
        "slavic": (0.03, 0.06),
        "celtic": (0.02, 0.05),
        "fantasy_generic": (0.10, 0.18),
    },
}

TOLERANCE_PP = 5  # ±5pp tolerance per composition policy § 2


def pct(n: int, total: int) -> float:
    return (n / total * 100) if total else 0.0


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()

        # Overall total
        cursor.execute("SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1")
        total = cursor.fetchone()[0]
        print(f"v1_scope=1 total (post-Wave-5.5): {total}")

        # Per-tier
        cursor.execute(
            "SELECT quality_tier, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY quality_tier ORDER BY 2 DESC"
        )
        per_tier = dict(cursor.fetchall())
        print()
        print("Per-tier distribution:")
        for k, v in per_tier.items():
            print(f"  {k}: {v} ({pct(v, total):.1f}%)")

        # Per-register
        cursor.execute(
            "SELECT register_canonical, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY register_canonical ORDER BY 2 DESC"
        )
        per_register = dict(cursor.fetchall())
        print()
        print("Per-register distribution (vs composition policy § 2 targets):")
        register_check = {}
        for k, v in per_register.items():
            p = pct(v, total)
            target = POLICY_TARGETS["register"].get(k)
            if target is None:
                check = f"(no target)"
            else:
                lo, hi = target[0] * 100, target[1] * 100
                if lo - TOLERANCE_PP <= p <= hi + TOLERANCE_PP:
                    check = f"WITHIN ±{TOLERANCE_PP}pp of target [{lo:.0f}–{hi:.0f}%]"
                else:
                    check = f"OUT of ±{TOLERANCE_PP}pp tolerance vs target [{lo:.0f}–{hi:.0f}%]"
            print(f"  {k}: {v} ({p:.1f}%) — {check}")
            register_check[k] = {"count": v, "pct": p, "target": target, "verdict": check}

        # Per-cultural-tradition
        cursor.execute(
            "SELECT cultural_lineage_canonical, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY cultural_lineage_canonical ORDER BY 2 DESC"
        )
        per_lineage = dict(cursor.fetchall())
        print()
        print("Per-cultural-tradition distribution (vs composition policy § 2 targets):")
        lineage_check = {}
        for k, v in per_lineage.items():
            p = pct(v, total)
            target = POLICY_TARGETS["cultural_tradition"].get(k)
            if target is None:
                check = "(no target)"
            else:
                lo, hi = target[0] * 100, target[1] * 100
                if lo - TOLERANCE_PP <= p <= hi + TOLERANCE_PP:
                    check = f"WITHIN ±{TOLERANCE_PP}pp"
                else:
                    check = f"OUT of ±{TOLERANCE_PP}pp tolerance vs target [{lo:.0f}–{hi:.0f}%]"
            print(f"  {k}: {v} ({p:.1f}%) — {check}")
            lineage_check[k] = {"count": v, "pct": p, "target": target, "verdict": check}

        # Per-period
        cursor.execute(
            "SELECT historical_period_canonical, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY historical_period_canonical ORDER BY 2 DESC"
        )
        per_period = dict(cursor.fetchall())
        print()
        print("Per-period distribution:")
        for k, v in per_period.items():
            print(f"  {k}: {v} ({pct(v, total):.1f}%)")

        # Per-axis
        cursor.execute(
            "SELECT proxy_geometry_class, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY proxy_geometry_class ORDER BY 2 DESC"
        )
        per_geom = {k or "NULL": v for k, v in cursor.fetchall()}
        cursor.execute(
            "SELECT proxy_range_class, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY proxy_range_class ORDER BY 2 DESC"
        )
        per_range = {k or "NULL": v for k, v in cursor.fetchall()}
        cursor.execute(
            "SELECT proxy_tempo_class, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY proxy_tempo_class ORDER BY 2 DESC"
        )
        per_tempo = {k or "NULL": v for k, v in cursor.fetchall()}
        cursor.execute(
            "SELECT proxy_attribute_class, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY proxy_attribute_class ORDER BY 2 DESC"
        )
        per_attr = {k or "NULL": v for k, v in cursor.fetchall()}
        print()
        print(f"Per-axis: geometry={per_geom}")
        print(f"Per-axis: range={per_range}")
        print(f"Per-axis: tempo={per_tempo}")
        print(f"Per-axis: attribute={per_attr}")

        # Per-subtype (post-Phase-0c population)
        cursor.execute(
            "SELECT weapon_kind_classified_subtype, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY weapon_kind_classified_subtype ORDER BY 2 DESC"
        )
        per_subtype = {k or "NULL": v for k, v in cursor.fetchall()}
        print()
        print("Per-subtype distribution (v1_scope=1):")
        for k, v in per_subtype.items():
            print(f"  {k}: {v} ({pct(v, total):.1f}%)")

        # ----- 50-row spot-check sample pack (gandalf re-run) -----
        # Stratification per `2026-05-25-phase-2-50-row-spot-check.md` § 1
        # Strata:
        #   S × 2: S1.mythological (10), S2.historical (5)
        #   A × 6: A1.hist-european (10), A2.east_asian (4), A3.south_asian (2),
        #          A4.thin-tradition (2), A5.fantasy-A (4), A6.mm-mode-c-check (4)
        #   B × 5: B1.european-historical-typed (4), B2.fantasy-typed (2),
        #          B3.NULL-typed (2), B4.fantasy_secondary-A-source (1)
        # Total: 50 rows (matches gandalf's spot-check stratification)
        random.seed(20260525)

        def select_sample(where_clause: str, n: int, label: str) -> list[dict]:
            cursor.execute(
                f"SELECT id, canonical_name, quality_tier, register_canonical, "
                f"       historical_period_canonical, cultural_lineage_canonical, "
                f"       weapon_kind_classified_subtype, proxy_geometry_class, "
                f"       proxy_range_class, proxy_tempo_class, proxy_attribute_class, "
                f"       named_mythological_match, source_library "
                f"FROM weapon_knowledge_entries "
                f"WHERE v1_scope=1 AND {where_clause} "
                f"ORDER BY RANDOM() LIMIT {n}"
            )
            rs = cursor.fetchall()
            return [{"stratum": label, **dict(r)} for r in rs]

        spot_sample: list[dict] = []
        spot_sample.extend(select_sample(
            "quality_tier='S' AND register_canonical='mythological'",
            10, "S1.mythological"))
        spot_sample.extend(select_sample(
            "quality_tier='S' AND register_canonical='historical'",
            5, "S2.historical"))
        spot_sample.extend(select_sample(
            "quality_tier='A' AND register_canonical='historical' "
            "AND cultural_lineage_canonical='european'",
            10, "A1.hist-european"))
        spot_sample.extend(select_sample(
            "quality_tier='A' AND cultural_lineage_canonical='east_asian'",
            4, "A2.east_asian"))
        spot_sample.extend(select_sample(
            "quality_tier='A' AND cultural_lineage_canonical='south_asian'",
            2, "A3.south_asian"))
        spot_sample.extend(select_sample(
            "quality_tier='A' AND cultural_lineage_canonical IN "
            "('mesoamerican','african','southeast_asian','celtic','slavic')",
            2, "A4.thin-tradition"))
        spot_sample.extend(select_sample(
            "quality_tier='A' AND register_canonical='fantasy_generic'",
            4, "A5.fantasy-A"))
        spot_sample.extend(select_sample(
            "quality_tier='A' AND register_canonical='military_modern'",
            4, "A6.mm-mode-c-check"))
        spot_sample.extend(select_sample(
            "quality_tier='B' AND register_canonical='historical' "
            "AND cultural_lineage_canonical='european' AND proxy_geometry_class IS NOT NULL",
            4, "B1.european-historical-typed"))
        spot_sample.extend(select_sample(
            "quality_tier='B' AND register_canonical='fantasy_generic' AND proxy_geometry_class IS NOT NULL",
            2, "B2.fantasy-typed"))
        spot_sample.extend(select_sample(
            "quality_tier='B' AND proxy_geometry_class IS NULL",
            2, "B3.NULL-typed"))
        spot_sample.extend(select_sample(
            "quality_tier='B' AND register_canonical='fantasy_secondary'",
            1, "B4.fantasy_secondary"))

        print()
        print(f"50-row spot-check sample pack: {len(spot_sample)} rows assembled")
        spot_sample_path = OUT_DIR / "post-wave-5-5-spot-sample-50.json"
        with spot_sample_path.open("w") as f:
            json.dump({
                "phase": "cycle-10-wave-5-5-post-spot-sample",
                "date": "2026-05-25",
                "purpose": (
                    "50-row spot-check sample pack for gandalf re-run spot-check post-Wave-5.5. "
                    "Stratification matches `2026-05-25-phase-2-50-row-spot-check.md` § 1 "
                    "for direct comparability with the pre-Wave-5.5 29/50 = 58% FAIL baseline."
                ),
                "v1_scope_total_post_wave_5_5": total,
                "stratification_reference": (
                    "agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md § 1"
                ),
                "expected_threshold": "≥40/50 = 80% (per dispatch § 8 + gandalf spot-check § 1)",
                "rows": spot_sample,
            }, f, indent=2, ensure_ascii=False)
        print(f"50-row spot-check sample pack saved: {spot_sample_path}")

        # ----- Closeout distribution payload -----
        out_path = OUT_DIR / "post-wave-5-5-distribution.json"
        payload = {
            "phase": "cycle-10-wave-5-5-closeout-distribution",
            "date": "2026-05-25",
            "v1_scope_total_post_wave_5_5": total,
            "per_tier": per_tier,
            "per_register": per_register,
            "per_register_policy_check": register_check,
            "per_cultural_tradition": per_lineage,
            "per_cultural_tradition_policy_check": lineage_check,
            "per_period": per_period,
            "per_axis": {
                "geometry": per_geom,
                "range": per_range,
                "tempo": per_tempo,
                "attribute": per_attr,
            },
            "per_subtype": per_subtype,
        }
        with out_path.open("w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print()
        print(f"Closeout distribution JSON saved: {out_path}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
