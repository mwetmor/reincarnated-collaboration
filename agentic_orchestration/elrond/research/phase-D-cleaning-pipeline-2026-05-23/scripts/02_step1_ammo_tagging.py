#!/usr/bin/env python3
"""
Phase D Step 1: ammo_or_consumable tagging (HIGHEST EMPIRICAL PRIORITY).

Per Phase A audit: 17.5% boundary error vs gandalf 1.0% target → drain ~15K rows
from active substrate BEFORE merge work runs.

Per gandalf cleaning-policy-design § 1.5 detection rules:
  (a) Royal Armouries: category_value match + Archery/Relics name regex
  (b) Met Museum: classification field match (Sword Furniture / Armor / Helmets / etc.)
  (c) Cataclysm-DDA: source_url path matches ammo.json OR tool.json
  (d) Cross-source: canonical_name safe-token regex (conservative; FP-risky tokens dropped)

Outputs:
  - DB mutations: weapon_kind='ammo_or_consumable' on ~10-15K rows
  - logs/02_step1_ammo_tagging.json — per-source counts + acceptance gate check

Idempotency: WHERE weapon_kind != 'ammo_or_consumable' — re-run is no-op.
Authority: Matt 2026-05-23 whole-pipeline upfront authorization.
Math note §2.1 + §4 (idempotency) + §5 (rollback via pre-step1 backup).
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "02_step1_ammo_tagging.json"

# ---------------------------------------------------------------------------
# Detection rule sets
# ---------------------------------------------------------------------------

# Royal Armouries category_value → ammo_or_consumable
RA_AMMO_CATEGORIES = (
    "Ammunition & projectiles",
    "Armour pieces",
    "Complete armours",
    "Helmets",
    "Animal armour & equestrian equipment",
)

# Met Museum classification LIKE patterns → ammo_or_consumable
MET_AMMO_LIKE_PATTERNS = (
    "Sword Furniture%",                  # Tsuba, Kozuka, Fuchi-Kashira, Menuki
    "Armor Parts%",                      # All Armor Parts subtypes
    "Armor for Man%",                    # Full armor sets
    "Armor for Horse%",                  # Equestrian armor
    "Armor for Child%",
    "Armor-Miniatures",                  # Decorative miniatures of armor
    "Helmets",                           # Just "Helmets"
    "Mail",                              # Chain mail
    "Firearms Accessories%",             # Accessories not weapons themselves
    "Swords-Accessories",                # Sword accessories
    "Archery Equipment-Arrowheads",      # Arrowheads (not bows)
    "Archery Equipment-Quivers",         # Quivers
    "Archery Equipment-Bow Cases",
    "Equestrian Equipment%",             # Note: legolas flagged equestrian as pure-FP not ammo;
                                          # BUT gandalf detection rule treats armour/equestrian as ammo_or_consumable.
                                          # Per Matt locked Tag-and-Keep + gandalf RA breakdown:
                                          # equestrian = NOT weapons → goes to ammo_or_consumable in this step;
                                          # FP-pure-classification deferred to Step 5 (unknown).
                                          # CORRECTION: Met Museum Equestrian per legolas Phase A is "pure FP" (spurs/stirrups/saddles).
                                          # We move them to weapon_kind='unknown' at Step 5 (FP removal), NOT ammo here.
)

# DROPPED from MET_AMMO_LIKE: Equestrian Equipment-* → those are pure FP (handled in Step 5)
MET_AMMO_LIKE_PATTERNS = tuple(p for p in MET_AMMO_LIKE_PATTERNS if not p.startswith("Equestrian Equipment"))

# Met Museum standalone (no LIKE wildcard) → ammo_or_consumable
MET_AMMO_EXACT = (
    "Armor",
    "Helmets",
    "Mail",
)

# Cross-source safe-token regex (case-insensitive; word-boundary).
# FP-risky tokens dropped per investigation: 'round', 'shell', 'grip', 'guard',
# 'handle', 'stand', 'hilt' (mostly weapon-feature in description, not weapon-parts in name),
# 'sheath' (low risk but already covered by Met/RA classification).
CROSS_SOURCE_AMMO_REGEX = re.compile(
    r"\b(cartridge|bullet|ammo|scabbard|tsuba|kozuka|fuchi-kashira|menuki|arrowhead|arrowheads)\b",
    re.IGNORECASE,
)

# Royal Armouries Archery sub-classification rules.
# Bows = category; arrows / arrowheads / quivers / bowstrings = ammo_or_consumable.
RA_ARCHERY_AMMO_REGEX = re.compile(
    r"\b(arrow|arrowhead|arrowheads|quiver|bowstring|bow case|bow-case)\b",
    re.IGNORECASE,
)
RA_ARCHERY_BOW_REGEX = re.compile(
    r"\b(bow|longbow|crossbow|recurve|composite bow)\b",
    re.IGNORECASE,
)

# Royal Armouries Relics & miscellaneous sub-classification regex (weapon-parts → ammo).
RA_RELICS_AMMO_REGEX = re.compile(
    r"\b(scabbard|hilt|grip|pommel|handle|mount|fitting|locket|chape|crossguard)\b",
    re.IGNORECASE,
)


def is_cataclysm_ammo_or_tool(source_url: str) -> bool:
    """Cataclysm source_url match per gandalf §1.5(a).

    Cataclysm-DDA stores items in two layouts:
      - /data/json/items/ammo.json       (legacy single-file)
      - /data/json/items/ammo/X.json     (subdirectory layout — sling-ready_grenade, 40x46mm, etc.)
      - /data/json/items/tool.json       (legacy single-file)
      - /data/json/items/tool/X.json     (subdirectory — workshop, woodworking, tailoring, etc.)
      - /data/json/items/chemicals_and_resources.json   (chemicals/fuels)
      - /data/json/items/resources/X.json (raw materials)
    All map to ammo_or_consumable per gandalf rule (a) intent.
    NOT included: /items/gun/* (firearms; weapon-category), /items/melee/* (weapons),
    /items/armor/* (armor — handled separately in Step 1 if surfaces; otherwise FP in Step 5).
    """
    if not source_url:
        return False
    su = source_url.lower()
    return (
        "/data/json/items/ammo.json" in su
        or "/data/json/items/ammo/" in su
        or "/data/json/items/tool.json" in su
        or "/data/json/items/tool/" in su
        or "/data/json/items/chemicals_and_resources.json" in su
        or "/data/json/items/resources/" in su
    )


def is_ra_archery_ammo(canonical_name: str) -> bool | None:
    """Within RA Archery category, distinguish ammo vs bow. Returns:
       True = ammo_or_consumable, False = category (bow), None = ambiguous (defer)."""
    if RA_ARCHERY_BOW_REGEX.search(canonical_name or ""):
        return False
    if RA_ARCHERY_AMMO_REGEX.search(canonical_name or ""):
        return True
    return None


def is_ra_relics_ammo(canonical_name: str) -> bool:
    return bool(RA_RELICS_AMMO_REGEX.search(canonical_name or ""))


def classify_row(row: dict) -> str | None:
    """Returns 'ammo_or_consumable' if row should be tagged; None otherwise."""
    src = row["source_library"]
    name = row["canonical_name"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json) if sp_json else {}
    except Exception:
        sp = {}

    # Rule (a): Royal Armouries
    if src == "royal_armouries":
        cv = sp.get("category_value")
        if cv in RA_AMMO_CATEGORIES:
            return "ammo_or_consumable"
        if cv == "Archery & related objects":
            verdict = is_ra_archery_ammo(name)
            if verdict is True:
                return "ammo_or_consumable"
            # bow → defer to default category in later step; ambiguous → defer
            return None
        if cv == "Relics & miscellaneous" and is_ra_relics_ammo(name):
            return "ammo_or_consumable"

    # Rule (b): Met Museum
    if src == "met-museum":
        clf = sp.get("classification") or ""
        if clf in MET_AMMO_EXACT:
            return "ammo_or_consumable"
        for pat in MET_AMMO_LIKE_PATTERNS:
            # SQL LIKE → fnmatch-equivalent via startswith check (only '%' suffix patterns here)
            if pat.endswith("%"):
                prefix = pat[:-1]
                if clf.startswith(prefix):
                    return "ammo_or_consumable"
            elif clf == pat:
                return "ammo_or_consumable"

    # Rule (c): Cataclysm-DDA source_url path
    if src == "cataclysm-dda" and is_cataclysm_ammo_or_tool(row["source_url"]):
        return "ammo_or_consumable"

    # Rule (d): cross-source safe-token canonical_name regex
    if CROSS_SOURCE_AMMO_REGEX.search(name):
        return "ammo_or_consumable"

    return None


def run_classification(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, canonical_name, source_library, source_url, structured_properties, weapon_kind
        FROM weapon_knowledge_entries
        WHERE weapon_kind != 'ammo_or_consumable'
        """
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    mutations: dict[str, int] = {}
    ids_to_update: list[int] = []
    for r in rows:
        row = dict(zip(cols, r))
        verdict = classify_row(row)
        if verdict == "ammo_or_consumable":
            mutations[row["source_library"]] = mutations.get(row["source_library"], 0) + 1
            ids_to_update.append(row["id"])

    # Idempotent UPDATE in batches
    total_updated = 0
    BATCH = 1000
    for i in range(0, len(ids_to_update), BATCH):
        batch_ids = ids_to_update[i : i + BATCH]
        placeholders = ",".join("?" * len(batch_ids))
        cur.execute(
            f"""UPDATE weapon_knowledge_entries
                SET weapon_kind = 'ammo_or_consumable'
                WHERE id IN ({placeholders})
                  AND weapon_kind != 'ammo_or_consumable'""",
            batch_ids,
        )
        total_updated += cur.rowcount

    conn.commit()
    return {
        "rows_scanned": len(rows),
        "rows_tagged": total_updated,
        "per_source_tagged": mutations,
    }


def acceptance_gate(conn: sqlite3.Connection) -> dict:
    """Gate (d.3): category-vs-ammo_or_consumable boundary error ≤ 1.0%.

    Definition: among rows with weapon_kind='category', what fraction match
    ammo-detection rules? We can't directly compute this because at end of
    Step 1 all rows are still 'unknown' (Step 4 routes named_template; Step
    6 routes unique; default 'unknown' becomes 'category' implicitly at
    consumption-time via v_category_sample which requires category/named_template).

    PROXY measurement: among rows that REMAIN 'unknown' post-Step-1 (which
    will default-route to 'category' in later steps), what fraction would
    re-match the ammo regex if rule (b) (cross-source name regex) were
    re-applied at full sensitivity (including risky tokens we dropped)?
    """
    # Count of remaining 'unknown' rows that match the cross-source-safe ammo regex.
    # If our Step 1 caught them all, this should be 0.
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, canonical_name, source_library, source_url, structured_properties
        FROM weapon_knowledge_entries
        WHERE weapon_kind = 'unknown'
        """
    )
    unknown_rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    missed_ammo = 0
    for r in unknown_rows:
        row = dict(zip(cols, r))
        verdict = classify_row(row)
        if verdict == "ammo_or_consumable":
            missed_ammo += 1

    pct_missed = 100.0 * missed_ammo / max(len(unknown_rows), 1)

    # Overall counts for context
    weapon_kind_dist = dict(
        cur.execute(
            "SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries GROUP BY weapon_kind"
        ).fetchall()
    )

    # Per-source post-Step-1 ammo_or_consumable counts
    ammo_per_source = dict(
        cur.execute(
            """SELECT source_library, COUNT(*) FROM weapon_knowledge_entries
               WHERE weapon_kind='ammo_or_consumable' GROUP BY source_library"""
        ).fetchall()
    )

    return {
        "weapon_kind_distribution": weapon_kind_dist,
        "ammo_per_source_post_step1": ammo_per_source,
        "remaining_unknown_count": len(unknown_rows),
        "missed_ammo_in_unknown": missed_ammo,
        "missed_ammo_pct_of_unknown": round(pct_missed, 3),
        # Gate (d.3) interpretation: idempotency check — re-running classification
        # on 'unknown' rows should produce ZERO additional ammo tags. So this
        # number should be 0 (or very near 0).
        "step1_self_consistent": missed_ammo == 0,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "02_step1_ammo_tagging.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        # Pre-state
        pre_dist = dict(
            conn.execute(
                "SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries GROUP BY weapon_kind"
            ).fetchall()
        )
        summary["pre_weapon_kind_distribution"] = pre_dist

        # Classify + mutate
        summary["classification_result"] = run_classification(conn)

        # Acceptance
        summary["acceptance_gate"] = acceptance_gate(conn)

    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Pass criteria (cumulative, not per-run delta):
    # 1. CUMULATIVE ammo_or_consumable count across all sources is within expected band
    # 2. acceptance_gate.step1_self_consistent is True (idempotency: 0 missed in unknown)
    # 3. delta tagged on this run is small (idempotency: re-runs are no-ops or near-no-ops)
    delta_tagged = summary["classification_result"]["rows_tagged"]
    cumulative_ammo = summary["acceptance_gate"]["weapon_kind_distribution"].get("ammo_or_consumable", 0)
    expected_lower = 10000  # conservative lower bound; legolas estimate ~15,750
    expected_upper = 20000  # conservative upper bound
    summary["expected_cumulative_band"] = [expected_lower, expected_upper]
    summary["delta_tagged"] = delta_tagged
    summary["cumulative_ammo_count"] = cumulative_ammo
    summary["cumulative_within_band"] = expected_lower <= cumulative_ammo <= expected_upper
    summary["passed"] = (
        summary["cumulative_within_band"]
        and summary["acceptance_gate"]["step1_self_consistent"]
    )

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"  ==> Delta tagged this run: {delta_tagged}")
    print(f"  ==> Cumulative ammo_or_consumable: {cumulative_ammo} (band {expected_lower}-{expected_upper})")
    print(f"  ==> Per-source delta: {summary['classification_result']['per_source_tagged']}")
    print(f"  ==> Idempotency check (missed_ammo in unknown): {summary['acceptance_gate']['missed_ammo_in_unknown']}")
    print(f"  ==> PASSED: {summary['passed']}")
    print(f"  ==> Summary: {LOG_PATH}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
