#!/usr/bin/env python3
"""
Phase D Step 6: unique detection + named-unique allowlist application.

Per gandalf §3 + legolas named-unique-verification + math note §2.6:

Allowlist (26 entries: 16 gandalf + 10 legolas):
  Historical-attested: Joyeuse, Curtana, Honjō Masamune, Mikazuki Munechika, Tizona,
    Colada, Szczerbiec, Sword of Goujian, Battersea Shield, Witham Shield,
    Kusanagi, Kusanagi no Tsurugi, Andúril
  Mythological: Excalibur, Mjolnir, Gungnir, Gáe Bulg, Aegis, Tyrfing, Fragarach,
    Caladbolg, Gram, Ruyi Jingu Bang, Sudarshana Chakra, Gandiva, Skofnung,
    Shield of Achilles

Special-cases:
  - Stormbringer → named_template (gandalf note; literary fictional)
  - Ulfberht class article → category (gandalf note; class not specific)
  - Narsil wikipedia redirect → unknown (Step 5 likely caught it)
  - OSRS mjolnir variants → named_template (Step 4 should have already tagged)

Brand-prefix exclusions (per Matt G2-principle): NEVER tag unique on rows where
canonical_name matches a brand-prefix pattern (M982 Excalibur, Kimber Aegis, etc.).

Idempotency: WHERE weapon_kind IN ('unknown', 'category').
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
LOG_PATH = Path(__file__).parent.parent / "logs" / "07_step6_unique_detection.json"

# ---------------------------------------------------------------------------
# Allowlist of named-unique weapons
# ---------------------------------------------------------------------------

# Lowercase canonical names → (register, cultural_lineage) hint pair.
# Register: 'historical' or 'mythological' (for Step 6.5 normalization assistance)
ALLOWLIST = {
    # Historical-attested
    "joyeuse": ("historical", "european"),
    "curtana": ("historical", "european"),
    "honjō masamune": ("historical", "east_asian"),
    "honjo masamune": ("historical", "east_asian"),  # alternate transliteration
    "mikazuki munechika": ("historical", "east_asian"),
    "tizona": ("historical", "european"),
    "colada": ("historical", "european"),
    "szczerbiec": ("historical", "european"),
    "sword of goujian": ("historical", "east_asian"),
    "battersea shield": ("historical", "european"),
    "witham shield": ("historical", "european"),
    "kusanagi": ("historical", "east_asian"),
    "kusanagi no tsurugi": ("historical", "east_asian"),
    "andúril": ("mythological", "european"),  # Tolkien fictional but unique-character
    "anduril": ("mythological", "european"),  # without diacritic

    # Mythological named uniques
    "excalibur": ("mythological", "european"),
    "mjolnir": ("mythological", "european"),
    "mjölnir": ("mythological", "european"),  # alternate transliteration
    "gungnir": ("mythological", "european"),
    "gáe bulg": ("mythological", "european"),
    "gae bulg": ("mythological", "european"),  # without diacritic
    "aegis": ("mythological", "european"),
    "tyrfing": ("mythological", "european"),
    "fragarach": ("mythological", "european"),
    "caladbolg": ("mythological", "european"),
    "gram": ("mythological", "european"),
    "ruyi jingu bang": ("mythological", "east_asian"),
    "sudarshana chakra": ("mythological", "south_asian"),
    "gandiva": ("mythological", "south_asian"),
    "skofnung": ("mythological", "european"),
    "shield of achilles": ("mythological", "european"),

    # Reichsschwert was in gandalf's allowlist but not found in substrate per legolas;
    # include for completeness in case it surfaces.
    "reichsschwert": ("historical", "european"),
    "imperial sword": ("historical", "european"),
}

# Names that should be tagged 'named_template' NOT 'unique' even though they hit allowlist
# (per gandalf notes).
NAMED_TEMPLATE_OVERRIDES = {
    "stormbringer": ("mythological", "european"),  # Moorcock literary fiction
    "narsil": ("mythological", "european"),        # Tolkien — but legolas confirmed redirect; will be unknown via Step 5
}

# Class-level article overrides → 'category' (gandalf note on Ulfberht)
CATEGORY_OVERRIDES = {
    "ulfberht swords",
    "ulfberht sword",
}

# Brand-prefix patterns (must NOT tag as unique; align with Step 5 patterns)
BRAND_CODE_PREFIX = re.compile(
    r"^[A-Z]+\d+[A-Z]?\s+", re.I,
)
LEGEND_WITH_TYPE_SUFFIX = re.compile(
    r"\s+(rifle|pistol|missile|bomb|shell|tank|aircraft|drone|jet|class|series)\b",
    re.I,
)
PAREN_QUALIFIER = re.compile(
    r"\((comics|comic|rifle|pistol|missile|bomb|tank|aircraft|game|video game|tv|film|movie|book|novel)\)",
    re.I,
)


def normalize_for_allowlist(name: str) -> str:
    """Strip parentheticals + extra whitespace + lower-case for allowlist match."""
    if not name:
        return ""
    # Remove parenthetical (e.g., "Mjolnir (comics)" → "Mjolnir")
    n = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip().lower()
    return n


def is_brand_prefix(name: str) -> bool:
    if not name:
        return False
    if BRAND_CODE_PREFIX.search(name):
        return True
    if LEGEND_WITH_TYPE_SUFFIX.search(name):
        return True
    if PAREN_QUALIFIER.search(name):
        return True
    # G2-principle: multi-capitalized-word prefix where penultimate is a brand and final is legend
    # e.g., "Kimber Aegis" — already in Step 5 brand-prefix detection; leave to Step 5.
    return False


GAME_SOURCE_LEGEND_TO_NAMED_TEMPLATE = {
    # Per gandalf G5 + Matt G2-principle: bare legend-name in GAME SOURCE → named_template, not unique
    "nick-aschenbach-dnd-data", "bsdata-warhammer-aos",
    "fextralife-elden-ring", "fextralife-ds1", "fextralife-ds2", "fextralife-ds3",
    "bloqhead-demigods", "elden-ring-erdb", "diablo2-d2data", "path-of-exile-repoe",
    "osrsbox-db", "wow-classic-items",
    "5e-bits-5e-database", "5e-bits-5e-database-2024",
    "cataclysm-dda",  # post-apocalyptic; bare legend-name = clone item, not unique
    "souls-api-thomaslincoln",
    "gta-v-data",
    "army-recognition", "odin-army-tradoc",  # modern military with brand-named items
}


def classify_unique(row: dict) -> tuple[str | None, str | None, str | None]:
    """Returns (new_weapon_kind, register_hint, cultural_hint) or (None, None, None) if no match."""
    name = row["canonical_name"] or ""
    src = row["source_library"] or ""
    norm = normalize_for_allowlist(name)

    # Class-level article overrides
    if norm in CATEGORY_OVERRIDES:
        return ("category", None, None)

    # Named_template overrides
    if norm in NAMED_TEMPLATE_OVERRIDES:
        reg, cul = NAMED_TEMPLATE_OVERRIDES[norm]
        return ("named_template", reg, cul)

    # Brand-prefix exclusion
    if is_brand_prefix(name):
        return (None, None, None)  # leave as-is; Step 5 should have set to category

    # Multi-word containing allowlist legend AS one of multiple words (Matt G2-principle):
    # e.g., "Star of Tyrfing" → category-instance (variant), not unique.
    # Heuristic: if the BARE name is in allowlist, tag unique; if name has extra words
    # AROUND the legend name (>1 word and not just possessive structure), it's G2 case.
    words = name.split()
    # Strip parenthetical
    bare_match_key = norm
    if bare_match_key in ALLOWLIST:
        # Per gandalf G5 + Matt G2-principle: GAME-SOURCE bare-legend-name → named_template
        # (game-canon clone of the mythological original; not the actual unique).
        if src in GAME_SOURCE_LEGEND_TO_NAMED_TEMPLATE:
            reg, cul = ALLOWLIST[bare_match_key]
            return ("named_template", reg, cul)
        reg, cul = ALLOWLIST[bare_match_key]
        return ("unique", reg, cul)

    # Allow "Sword of X" / "Shield of X" pattern — those ARE in allowlist (e.g., "Sword of Goujian")
    # Already handled if `norm` is exact-match.

    # Special: "X no Y" Japanese transliteration variants — check post-paren stripped
    # Already handled if `norm` is exact-match.

    return (None, None, None)


def run_step6(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    cur.execute(
        """SELECT id, canonical_name, source_library, weapon_kind
           FROM weapon_knowledge_entries
           WHERE weapon_kind IN ('unknown', 'category')
             AND dedup_status != 'merged_into'"""
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    unique_updates: list[tuple[str, str, int]] = []  # (register_hint, cultural_hint, id)
    named_template_updates: list[int] = []
    category_overrides_applied: list[int] = []
    per_allowlist_matches: dict[str, int] = {}

    for r in rows:
        row = dict(zip(cols, r))
        new_kind, reg_hint, cul_hint = classify_unique(row)
        if new_kind == "unique":
            unique_updates.append((reg_hint or "unknown", cul_hint or "unknown", row["id"]))
            key = normalize_for_allowlist(row["canonical_name"])
            per_allowlist_matches[key] = per_allowlist_matches.get(key, 0) + 1
        elif new_kind == "named_template":
            named_template_updates.append(row["id"])
        elif new_kind == "category":
            category_overrides_applied.append(row["id"])

    # Apply unique tags + register/cultural hints for Step 6.5 to use
    # NOTE: we set weapon_kind='unique' and ALSO populate register_canonical + cultural_lineage_canonical
    # with high-confidence hints — Step 6.5 will see populated values for these rows.
    for reg, cul, row_id in unique_updates:
        cur.execute(
            """UPDATE weapon_knowledge_entries
               SET weapon_kind = 'unique',
                   dedup_status = CASE WHEN dedup_status = 'unprocessed' THEN 'canonical' ELSE dedup_status END,
                   register_canonical = ?,
                   cultural_lineage_canonical = ?,
                   cultural_lineage_confidence = 1.0
               WHERE id = ?""",
            (reg, cul, row_id),
        )

    # Apply named_template overrides
    if named_template_updates:
        ph = ",".join("?" * len(named_template_updates))
        cur.execute(
            f"""UPDATE weapon_knowledge_entries
                SET weapon_kind = 'named_template',
                    dedup_status = CASE WHEN dedup_status = 'unprocessed' THEN 'canonical' ELSE dedup_status END
                WHERE id IN ({ph})""",
            named_template_updates,
        )

    # Apply category overrides (Ulfberht etc.)
    if category_overrides_applied:
        ph = ",".join("?" * len(category_overrides_applied))
        cur.execute(
            f"""UPDATE weapon_knowledge_entries
                SET weapon_kind = 'category',
                    dedup_status = CASE WHEN dedup_status = 'unprocessed' THEN 'canonical' ELSE dedup_status END
                WHERE id IN ({ph})""",
            category_overrides_applied,
        )

    conn.commit()
    return {
        "rows_scanned": len(rows),
        "unique_tagged": len(unique_updates),
        "named_template_overrides": len(named_template_updates),
        "category_overrides": len(category_overrides_applied),
        "per_allowlist_matches": per_allowlist_matches,
    }


def acceptance_check(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    # Distribution
    weapon_kind_dist = dict(
        cur.execute(
            "SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries GROUP BY weapon_kind"
        ).fetchall()
    )
    # Per-source unique counts
    unique_per_source = dict(
        cur.execute(
            """SELECT source_library, COUNT(*) FROM weapon_knowledge_entries
               WHERE weapon_kind='unique' GROUP BY source_library"""
        ).fetchall()
    )
    # Spot check: brand-prefix rows that ARE in DB and got tagged unique (should be 0)
    brand_prefix_unique = cur.execute(
        """SELECT COUNT(*) FROM weapon_knowledge_entries
           WHERE weapon_kind = 'unique'
             AND (canonical_name LIKE 'M9% Excalibur%'
                  OR canonical_name LIKE 'Kimber %'
                  OR canonical_name LIKE '%(comics)%'
                  OR canonical_name LIKE '%(rifle)%'
                  OR canonical_name LIKE '% missile')"""
    ).fetchone()[0]

    return {
        "weapon_kind_distribution": weapon_kind_dist,
        "unique_per_source": unique_per_source,
        "brand_prefix_leaked_to_unique": brand_prefix_unique,
        "gate_d1_pass": brand_prefix_unique == 0
                       and 50 <= weapon_kind_dist.get("unique", 0) <= 1000,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "07_step6_unique_detection.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["step6_result"] = run_step6(conn)
        summary["acceptance"] = acceptance_check(conn)
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    summary["passed"] = summary["acceptance"]["gate_d1_pass"]

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"  ==> Unique tagged: {summary['step6_result']['unique_tagged']}")
    print(f"  ==> Named_template overrides (Stormbringer/Narsil): {summary['step6_result']['named_template_overrides']}")
    print(f"  ==> Category overrides (Ulfberht): {summary['step6_result']['category_overrides']}")
    print(f"  ==> Per-allowlist matches: {summary['step6_result']['per_allowlist_matches']}")
    print(f"  ==> Brand-prefix leaked to unique: {summary['acceptance']['brand_prefix_leaked_to_unique']} (expect 0)")
    print(f"  ==> PASSED: {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
