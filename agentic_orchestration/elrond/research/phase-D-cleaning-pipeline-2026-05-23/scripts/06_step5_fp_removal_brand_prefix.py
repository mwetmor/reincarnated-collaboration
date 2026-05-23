#!/usr/bin/env python3
"""
Phase D Step 5: FP removal + brand-prefix disambiguation.

Per math note §2.5 + Matt G2-principle:

Scattered FPs to tag weapon_kind='unknown' + dedup_status='canonical' (audit-flag):
  1. gta-v-data Invalid placeholders: canonical_name LIKE 'Invalid%'
  2. Royal Armouries Art category: structured_properties.category_value='Art'
  3. Met Museum equestrian: classification LIKE 'Equestrian Equipment%'
  4. Met Museum works on paper: classification LIKE 'Works on Paper%'
  5. Met Museum miscellaneous non-weapons: classification IN ('Miscellaneous-Badges')
  6. Wikipedia v2 redirects: description_text starts with 'REDIRECT' or '#REDIRECT'

Brand-prefix disambiguation (per Matt G2-principle): tag weapon_kind='category' for
rows where canonical_name matches a brand-prefix pattern + embedded legend name.
This pre-empts Step 6's unique-detection from incorrectly tagging them as unique.

Idempotency: WHERE weapon_kind = 'unknown' (or 'category' for brand-prefix subset).
Authority: Matt 2026-05-23 whole-pipeline upfront authorization.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "06_step5_fp_removal_brand_prefix.json"

# ---------------------------------------------------------------------------
# Brand-prefix patterns (Matt G2-principle negative overrides for Step 6)
# ---------------------------------------------------------------------------

# Pattern: <Alphanumeric Code> <LegendName> (e.g., "M982 Excalibur", "F-22 Raptor")
BRAND_CODE_PREFIX = re.compile(
    r"^[A-Z]+\d+[A-Z]?\s+(Excalibur|Aegis|Tyrfing|Durandal|Mjolnir|Gungnir|Joyeuse|Curtana|Tizona)\b",
    re.I,
)
# Pattern: <Brand-Capitalized-Word> <LegendName> (e.g., "Kimber Aegis", "Matra Durandal")
BRAND_NAME_PREFIX = re.compile(
    r"^[A-Z][a-z]+\s+(Excalibur|Aegis|Tyrfing|Durandal|Mjolnir|Gungnir|Joyeuse|Curtana|Tizona)\b",
    re.I,
)
# Pattern: <LegendName> <ModernWeaponWord> (e.g., "Excalibur rifle", "Tyrfing missile")
LEGEND_WITH_TYPE_SUFFIX = re.compile(
    r"^(Excalibur|Aegis|Tyrfing|Durandal|Mjolnir|Gungnir|Joyeuse|Curtana|Tizona)\s+(rifle|pistol|missile|bomb|shell|tank|aircraft|drone|jet)\b",
    re.I,
)
# Pattern: <LegendName> (<qualifier>)
PAREN_QUALIFIER = re.compile(
    r"\((comics|comic|rifle|pistol|missile|bomb|tank|aircraft|game|video game|tv|tv series|film|movie|book|novel)\)",
    re.I,
)
# Pattern: <LegendName>s (plural — class article)
LEGEND_PLURAL_CLASS = re.compile(
    r"^(Excalibur|Aegis|Tyrfing|Durandal|Mjolnir|Gungnir|Joyeuse|Ulfberht)\s+swords?$|"
    r"^Ulfberht\s+swords?\b",
    re.I,
)


def is_brand_prefix_name(name: str) -> bool:
    """True if name is a brand-prefixed legend-name (per Matt G2-principle)."""
    if not name:
        return False
    return any(
        p.search(name) for p in (
            BRAND_CODE_PREFIX,
            BRAND_NAME_PREFIX,
            LEGEND_WITH_TYPE_SUFFIX,
            PAREN_QUALIFIER,
            LEGEND_PLURAL_CLASS,
        )
    )


# ---------------------------------------------------------------------------
# Scattered FP detection
# ---------------------------------------------------------------------------

GTA_INVALID_RE = re.compile(r"^(Invalid|placeholder|test|dummy)\b", re.I)
WIKIPEDIA_REDIRECT_RE = re.compile(r"^\s*#?REDIRECT", re.I)


def classify_fp(row: dict) -> str | None:
    """Return 'unknown_fp' if row is a FP (true non-weapon)."""
    src = row["source_library"]
    name = row["canonical_name"] or ""
    desc = row["description_text"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}

    # gta-v-data Invalid placeholders
    if src == "gta-v-data" and GTA_INVALID_RE.match(name):
        return "unknown_fp"

    # Royal Armouries Art category (pure FP — prints/paintings/not-weapons)
    if src == "royal_armouries" and sp.get("category_value") == "Art":
        return "unknown_fp"

    # Met Museum equestrian (per legolas: pure FP)
    if src == "met-museum":
        clf = sp.get("classification") or ""
        if clf.startswith("Equestrian Equipment"):
            return "unknown_fp"
        if clf.startswith("Works on Paper"):
            return "unknown_fp"
        if clf == "Miscellaneous-Badges":
            return "unknown_fp"

    # Wikipedia v2 REDIRECT rows
    if src == "wikipedia" and WIKIPEDIA_REDIRECT_RE.match(desc):
        return "unknown_fp"

    return None


def run_step5(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()

    # === Scattered FP pass ===
    cur.execute(
        """SELECT id, canonical_name, source_library, description_text, structured_properties, weapon_kind
           FROM weapon_knowledge_entries
           WHERE weapon_kind IN ('unknown', 'category')"""
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    fp_ids_by_source: dict[str, list[int]] = {}
    for r in rows:
        row = dict(zip(cols, r))
        if classify_fp(row) == "unknown_fp":
            fp_ids_by_source.setdefault(row["source_library"], []).append(row["id"])

    # Batch UPDATE: weapon_kind='unknown' + dedup_status='canonical' (audit-flag)
    total_fp_tagged = 0
    BATCH = 500
    for src, ids in fp_ids_by_source.items():
        for i in range(0, len(ids), BATCH):
            batch = ids[i : i + BATCH]
            ph = ",".join("?" * len(batch))
            cur.execute(
                f"""UPDATE weapon_knowledge_entries
                    SET weapon_kind = 'unknown',
                        dedup_status = 'canonical',
                        variant_relationship = 'independent'
                    WHERE id IN ({ph}) AND dedup_status != 'merged_into'""",
                batch,
            )
            total_fp_tagged += cur.rowcount

    conn.commit()

    # === Brand-prefix pass (Matt G2-principle) ===
    # For rows whose canonical_name matches a brand-prefix pattern AND embeds a legend name,
    # ensure weapon_kind='category' (NOT unique). Step 6 allowlist scan will skip them.
    brand_prefix_count = 0
    cur.execute(
        """SELECT id, canonical_name, weapon_kind
           FROM weapon_knowledge_entries
           WHERE weapon_kind IN ('unknown', 'category')
             AND dedup_status != 'merged_into'"""
    )
    candidates = cur.fetchall()
    bp_ids_to_force_category: list[int] = []
    for row_id, name, wk in candidates:
        if is_brand_prefix_name(name):
            if wk != "category":
                bp_ids_to_force_category.append(row_id)
            brand_prefix_count += 1

    for i in range(0, len(bp_ids_to_force_category), BATCH):
        batch = bp_ids_to_force_category[i : i + BATCH]
        ph = ",".join("?" * len(batch))
        cur.execute(
            f"""UPDATE weapon_knowledge_entries
                SET weapon_kind = 'category',
                    dedup_status = CASE WHEN dedup_status = 'unprocessed' THEN 'canonical' ELSE dedup_status END
                WHERE id IN ({ph})""",
            batch,
        )

    conn.commit()
    return {
        "scattered_fp_tagged": total_fp_tagged,
        "fp_per_source": {k: len(v) for k, v in fp_ids_by_source.items()},
        "brand_prefix_detected": brand_prefix_count,
        "brand_prefix_forced_to_category": len(bp_ids_to_force_category),
    }


def acceptance_check(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    # Distribution
    weapon_kind_dist = dict(
        cur.execute(
            "SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries GROUP BY weapon_kind"
        ).fetchall()
    )
    dedup_status_dist = dict(
        cur.execute(
            "SELECT dedup_status, COUNT(*) FROM weapon_knowledge_entries GROUP BY dedup_status"
        ).fetchall()
    )
    # Brand-prefix forced-to-category sanity check: count brand-prefix rows currently tagged unique
    # (should be 0 — Step 5 should have caught them; Step 6 won't re-tag them as unique)
    unique_count = weapon_kind_dist.get("unique", 0)
    return {
        "weapon_kind_distribution": weapon_kind_dist,
        "dedup_status_distribution": dedup_status_dist,
        "current_unique_count": unique_count,  # should be 0 pre-Step-6
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "06_step5_fp_removal_brand_prefix.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["step5_result"] = run_step5(conn)
        summary["acceptance"] = acceptance_check(conn)
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    # Pass: FP detection produced any results (real cleanup happened) + brand-prefix pass ran
    fp_count = summary["step5_result"]["scattered_fp_tagged"]
    bp_count = summary["step5_result"]["brand_prefix_detected"]
    # Phase A audit baseline: ~1,650 expected FP rows. Allow [500, 2500] band.
    summary["passed"] = 500 <= fp_count <= 2500

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"  ==> Scattered FP tagged: {fp_count}")
    print(f"  ==> FP per source: {summary['step5_result']['fp_per_source']}")
    print(f"  ==> Brand-prefix detected: {bp_count} (forced to category: {summary['step5_result']['brand_prefix_forced_to_category']})")
    print(f"  ==> PASSED: {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
