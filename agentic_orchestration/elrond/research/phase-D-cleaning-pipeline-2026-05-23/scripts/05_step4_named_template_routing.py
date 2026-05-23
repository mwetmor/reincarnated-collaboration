#!/usr/bin/env python3
"""
Phase D Step 4: named_template routing for TRPG/MMO/ARPG/Soulslike sources.

Per gandalf §1.5 Rule (a) + math note §2.4:

For rows in {nick-aschenbach-dnd-data, 5e-bits*, pf2ools-* (quarantined-skip),
bsdata-warhammer-aos, fextralife-*, bloqhead-demigods, elden-ring-erdb,
souls-api-thomaslincoln (2 weapons.js only), diablo2-d2data, path-of-exile-repoe,
osrsbox-db, wow-classic-items}:

  Tag named_template IF:
    - D&D rarity in {Uncommon, Rare, Very Rare, Legendary}, OR
    - Multi-word name with narrative-flavor modifier (capitalized non-generic word
      before/after a category-type word)
  Tag category IF:
    - Single-word generic name (e.g., "Katana", "Dagger") OR
    - SRD baseline (5e-bits sources blanket)

G3 (AOS-2 compound split): canonical_name LIKE 'Skull Bludgeon and Varanspire Gladius'
  → split into two child rows + retain compound with variant_relationship='model_line_sibling_of:'

G1 (WIKI-3 game-tier Gladius): keep per-game named_template; no cross-source merge here
  (Step 7 F4 will handle).

G5 (OSRS Excalibur): tag named_template, not unique. Stays separate from mythological
  Excalibur (handled in Step 6 by allowlist with brand-prefix exclusion).

Idempotency: WHERE weapon_kind = 'unknown' filter.
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
LOG_PATH = Path(__file__).parent.parent / "logs" / "05_step4_named_template_routing.json"

TRPG_MMO_ARPG_SOURCES = {
    "nick-aschenbach-dnd-data",
    "bsdata-warhammer-aos",
    "fextralife-elden-ring",
    "fextralife-ds1",
    "fextralife-ds2",
    "fextralife-ds3",
    "bloqhead-demigods",
    "elden-ring-erdb",
    "diablo2-d2data",
    "path-of-exile-repoe",
    "osrsbox-db",
    "wow-classic-items",
}

# SRD baseline sources: blanket weapon_kind='category' (no named_template content).
SRD_BASELINE_SOURCES = {
    "5e-bits-5e-database",
    "5e-bits-5e-database-2024",
}

# Generic-type category nouns (used for narrative-flavor detection)
GENERIC_TYPE_NOUNS = {
    "sword", "axe", "hammer", "bow", "staff", "wand", "dagger", "spear",
    "lance", "mace", "club", "shield", "orb", "tome", "chime", "focus",
    "blade", "knife", "sabre", "saber", "rapier", "scimitar", "halberd",
    "katana", "tachi", "wakizashi", "tanto", "tantō", "naginata", "yari",
    "pike", "polearm", "trident", "javelin", "morningstar", "warhammer",
    "greatsword", "shortsword", "longsword", "longbow", "shortbow",
    "crossbow", "musket", "pistol", "rifle", "revolver", "shotgun",
    "buckler", "gladius", "katar", "tulwar", "kris", "kukri",
}

# D&D rarity values that signal named_template
DND_NAMED_TEMPLATE_RARITIES = {"Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"}

# G3 AOS-2 compound detection regex
AOS2_COMPOUND_RE = re.compile(r"^Skull Bludgeon and Varanspire Gladius$", re.I)


def name_is_narrative_flavor(name: str) -> bool:
    """Return True if name has multi-word narrative-flavor pattern.

    Heuristic:
      - 2+ words AND at least one non-final word is capitalized non-generic
      - Examples (TRUE): "Magehunter Katana", "Worn Mace", "Bow of Grounding",
        "Moonlit Katana", "Abyss Warden's Axeblade"
      - Examples (FALSE): "Katana", "Greatsword", "Battle Axe" (the modifier
        "Battle" IS in GENERIC_TYPE_NOUNS would be a category word... but
        "Battle Axe" actually IS narrative; treat as borderline → TRUE if any
        leading word is capitalized non-generic).
    """
    if not name:
        return False
    words = name.split()
    if len(words) < 2:
        return False
    # Check non-final words for narrative-flavor modifier
    for w in words[:-1]:
        wl = w.lower().strip(",.'\"")
        # Capitalized AND not a generic type AND not a stopword
        if not wl:
            continue
        if w[0].isupper() and wl not in GENERIC_TYPE_NOUNS and wl not in {"of", "the", "and", "a", "an", "with", "from"}:
            return True
    return False


def classify_named_template(row: dict) -> str | None:
    """Returns 'named_template', 'category', or None (no decision in this step)."""
    src = row["source_library"]
    name = row["canonical_name"] or ""

    # SRD baseline → all category
    if src in SRD_BASELINE_SOURCES:
        return "category"

    if src not in TRPG_MMO_ARPG_SOURCES:
        return None  # not in scope for Step 4

    # D&D rarity check
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}
    rarity = sp.get("rarity")
    if rarity in DND_NAMED_TEMPLATE_RARITIES:
        return "named_template"

    # Narrative-flavor name pattern
    if name_is_narrative_flavor(name):
        return "named_template"

    # Default for in-scope sources: category
    return "category"


def handle_aos2_compound_split(conn: sqlite3.Connection) -> dict:
    """G3 — split AOS-2 compound row into two children + retain compound."""
    cur = conn.cursor()
    cur.execute(
        """SELECT id, canonical_name, source_library, source_url, source_id,
                  description_text, structured_properties, license_class
           FROM weapon_knowledge_entries
           WHERE canonical_name LIKE 'Skull Bludgeon and Varanspire Gladius%'
             AND source_library = 'bsdata-warhammer-aos'
             AND variant_relationship = 'independent'"""
    )
    compounds = cur.fetchall()
    if not compounds:
        return {"action": "SKIP_NO_COMPOUND", "splits": 0}

    cols = [d[0] for d in cur.description]
    splits = 0
    for r in compounds:
        parent = dict(zip(cols, r))
        parent_id = parent["id"]

        # Check if children already inserted (idempotency by source_url + child-name pattern)
        for child_name in ("Skull Bludgeon", "Varanspire Gladius"):
            child_url = f"{parent['source_url']}#child={child_name.replace(' ', '_')}"
            existing = cur.execute(
                "SELECT id FROM weapon_knowledge_entries WHERE source_url = ? AND source_library = ?",
                (child_url, parent["source_library"]),
            ).fetchone()
            if existing:
                continue
            cur.execute(
                """INSERT INTO weapon_knowledge_entries
                   (canonical_name, source_library, source_url, source_id,
                    description_text, structured_properties, license_class,
                    weapon_kind, dedup_status, variant_relationship)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'named_template', 'canonical', ?)""",
                (
                    child_name,
                    parent["source_library"],
                    child_url,
                    parent["source_id"],
                    f"Child of AOS-2 compound: {parent['canonical_name']}. Original description: "
                    + (parent["description_text"] or "")[:200],
                    parent["structured_properties"],
                    parent["license_class"],
                    f"sub_variant_of:{parent_id}",
                ),
            )
            splits += 1

        # Find newly-inserted child IDs and update parent variant_relationship to point at them
        child_ids = [
            r[0]
            for r in cur.execute(
                """SELECT id FROM weapon_knowledge_entries
                   WHERE source_library = 'bsdata-warhammer-aos'
                     AND source_url LIKE ?
                     AND canonical_name IN ('Skull Bludgeon', 'Varanspire Gladius')""",
                (f"{parent['source_url']}#child=%",),
            ).fetchall()
        ]
        if child_ids:
            cur.execute(
                """UPDATE weapon_knowledge_entries
                   SET weapon_kind = 'named_template',
                       variant_relationship = ?
                   WHERE id = ?""",
                (f"model_line_sibling_of:{','.join(str(c) for c in child_ids)}", parent_id),
            )

    conn.commit()
    return {"action": "SPLIT_APPLIED", "splits": splits, "compounds_processed": len(compounds)}


def run_step4(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    cur.execute(
        """SELECT id, canonical_name, source_library, structured_properties, weapon_kind
           FROM weapon_knowledge_entries
           WHERE weapon_kind = 'unknown'
             AND source_library IN ({0})""".format(
            ",".join(["?"] * len(TRPG_MMO_ARPG_SOURCES | SRD_BASELINE_SOURCES))
        ),
        tuple(TRPG_MMO_ARPG_SOURCES | SRD_BASELINE_SOURCES),
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    named_template_ids: list[int] = []
    category_ids: list[int] = []
    per_source_nt: dict[str, int] = {}
    per_source_cat: dict[str, int] = {}

    for r in rows:
        row = dict(zip(cols, r))
        verdict = classify_named_template(row)
        if verdict == "named_template":
            named_template_ids.append(row["id"])
            per_source_nt[row["source_library"]] = per_source_nt.get(row["source_library"], 0) + 1
        elif verdict == "category":
            category_ids.append(row["id"])
            per_source_cat[row["source_library"]] = per_source_cat.get(row["source_library"], 0) + 1

    # Batch UPDATEs
    BATCH = 1000
    for i in range(0, len(named_template_ids), BATCH):
        batch = named_template_ids[i : i + BATCH]
        ph = ",".join("?" * len(batch))
        cur.execute(
            f"""UPDATE weapon_knowledge_entries
                SET weapon_kind = 'named_template'
                WHERE id IN ({ph}) AND weapon_kind = 'unknown'""",
            batch,
        )
    for i in range(0, len(category_ids), BATCH):
        batch = category_ids[i : i + BATCH]
        ph = ",".join("?" * len(batch))
        cur.execute(
            f"""UPDATE weapon_knowledge_entries
                SET weapon_kind = 'category'
                WHERE id IN ({ph}) AND weapon_kind = 'unknown'""",
            batch,
        )

    conn.commit()
    return {
        "rows_scanned": len(rows),
        "named_template_count": len(named_template_ids),
        "category_count": len(category_ids),
        "per_source_named_template": per_source_nt,
        "per_source_category": per_source_cat,
    }


def acceptance_check(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    # Boundary error: TRPG/MMO/ARPG rows tagged 'category' that match named_template detection
    # would be a leak. Re-classify them to confirm.
    cur.execute(
        """SELECT id, canonical_name, source_library, structured_properties, weapon_kind
           FROM weapon_knowledge_entries
           WHERE weapon_kind = 'category'
             AND source_library IN ({0})""".format(
            ",".join(["?"] * len(TRPG_MMO_ARPG_SOURCES))
        ),
        tuple(TRPG_MMO_ARPG_SOURCES),
    )
    cat_rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    leaked = 0
    for r in cat_rows:
        row = dict(zip(cols, r))
        if classify_named_template(row) == "named_template":
            leaked += 1
    total_category_trpg = len(cat_rows)
    leak_pct = 100.0 * leaked / max(total_category_trpg, 1)

    # Overall distribution
    weapon_kind_dist = dict(
        cur.execute(
            "SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries GROUP BY weapon_kind"
        ).fetchall()
    )

    return {
        "weapon_kind_distribution": weapon_kind_dist,
        "trpg_category_total": total_category_trpg,
        "trpg_category_leaked_to_named_template": leaked,
        "leak_pct": round(leak_pct, 3),
        "gate_d2_pass": leak_pct <= 5.0,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "05_step4_named_template_routing.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["step4_classification"] = run_step4(conn)
        summary["aos2_split"] = handle_aos2_compound_split(conn)
        summary["acceptance"] = acceptance_check(conn)
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    summary["passed"] = summary["acceptance"]["gate_d2_pass"]

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    nt = summary["step4_classification"]["named_template_count"]
    cat = summary["step4_classification"]["category_count"]
    print(f"  ==> named_template tagged: {nt}")
    print(f"  ==> category tagged: {cat}")
    print(f"  ==> AOS-2 compound: {summary['aos2_split']}")
    print(f"  ==> Gate (d.2) leak rate: {summary['acceptance']['leak_pct']}% (≤5.0%)")
    print(f"  ==> PASSED: {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
