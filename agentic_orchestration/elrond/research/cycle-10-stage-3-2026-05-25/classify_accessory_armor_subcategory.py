#!/usr/bin/env python3
"""
Cycle 10 Stage 3 Phase 0a — Accessory + Armor Subcategory Classifier

Per dispatch agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md
§ 3.2 + § 4.1, subdivides 255 Tier-S accessory(130) + armor(125) rows into the
sub-enums specified by composition policy v1 § 1.1 (D1a/D1b/D1c):

    accessory  → accessory_handheld
               → accessory_weapon_integrated
               → accessory_horse_or_equipment

    armor      → armor_shield
               → armor_body_or_head

Heuristic only — name tokens + Stage 2.5 classifier `method` string (already
captures the source-side structured signal that drove the parent classification).
No LLM cost. Per Discipline #11, prints empirical counts pre/post.

PREREQUISITE STATE FINDING — empirical inspection 2026-05-25:
The dispatch describes column `weapon_kind_classified_subtype` as "already
populated on 1,126 Tier-S rows" but the column does NOT exist in the DB at
session start. The Stage 2.5 classifier wrote ONLY to JSON artifact
`tier-s-classification.json`; no ALTER-TABLE landed at Stage 2.5.

This Phase 0a script therefore (a) ALTER-TABLE-ADDs the column as additive
schema change, (b) populates parent category for all 1,126 Tier-S rows from the
Stage 2.5 JSON, (c) subdivides the 255 accessory + armor rows. Three-step
operation, not the dispatch's described single UPDATE-in-place. Recorded in
MIGRATION.md + completion record.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
STAGE_2_5_JSON = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond"
    "/research/cycle-10-stage-2-5-2026-05-24/tier-s-classification.json"
)
OUT_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond"
    "/research/cycle-10-stage-3-2026-05-25"
)

# ---------------------------------------------------------------------------
# Sub-category enums
# ---------------------------------------------------------------------------

# Accessory subcategories (composition policy § 1.1 D1b allow-list + D1c reject)
ACC_HANDHELD = "accessory_handheld"               # D1b allowed (banners, talismans, focuses, archery rings)
ACC_WEAPON_INTEGRATED = "accessory_weapon_integrated"  # D1b allowed (tsuba/menuki/pommels/scopes/magazines)
ACC_HORSE = "accessory_horse_or_equipment"        # D1c excluded (spurs, bits, shaffrons, horse trappings)

# Armor subcategories
ARM_SHIELD = "armor_shield"                       # D1b allowed
ARM_BODY_OR_HEAD = "armor_body_or_head"           # D1c excluded (helmets, gauntlets, complete-armours, masks, mail)

# ---------------------------------------------------------------------------
# Heuristic rules
# ---------------------------------------------------------------------------
# Rules driven by Stage 2.5 classifier `method` string. The method string
# captures source-side structured signals (met-museum classification, royal-
# armouries category_value, wikidata weapon_type, etc.) — the same signal that
# drove the parent category in Stage 2.5. Subcategory boundaries are determined
# by the underlying source-vocabulary, not re-derived from canonical_name.

# Accessory rules — keyed by exact-match-prefix on method string
ACCESSORY_METHOD_RULES = {
    # Sword Furniture — weapon-integrated (mounted to a sword's hilt)
    "met:classification=Sword Furniture": ACC_WEAPON_INTEGRATED,            # 5
    "met:classification=Sword Furniture-Menuki": ACC_WEAPON_INTEGRATED,     # 64
    "met:classification=Sword Furniture-Tsuba": ACC_WEAPON_INTEGRATED,      # 4
    # Firearms-integrated accessories (powder horns, bayonets)
    "met:classification=Firearms Accessories-Powder Horns": ACC_WEAPON_INTEGRATED,   # 2
    "ra:cv=bayonets+name": ACC_WEAPON_INTEGRATED,                                    # 1
    "ra:cv=firearms & related objects+name:powder flask": ACC_WEAPON_INTEGRATED,     # 1

    # Equestrian Equipment — horse-or-equipment
    "met:classification=Equestrian Equipment-Spurs": ACC_HORSE,            # 16
    "met:classification=Equestrian Equipment-Bits": ACC_HORSE,             # 7
    "met:classification=Equestrian Equipment-Shaffrons": ACC_HORSE,        # 3
    "met:classification=Equestrian Equipment-Horse Trappings": ACC_HORSE,  # 1
    "ra:cv=animal armour & equestrian equipment": ACC_HORSE,               # 12
    # Miscellaneous-Buckles: inspected — all 6 are "Ornament of Horse Trapping" → horse
    "met:classification=Miscellaneous-Buckles & Ornament": ACC_HORSE,      # 6

    # Hand-carriable items (banners, archery rings, costumes, militaria display objects)
    "met:classification=Banners": ACC_HANDHELD,                            # 3
    "met:classification=Costumes": ACC_HANDHELD,                           # 2
    "met:classification=Archery Equipment-Archer's Ring": ACC_HANDHELD,    # 1
    "ra:cv=militaria": ACC_HANDHELD,                                       # 2 (display board + storage tin — closest fit; ambiguous, flagged in trace)
}

# Armor rules — keyed by exact-match-prefix on method string
ARMOR_METHOD_RULES = {
    # Shields (D1b allow-list)
    "wd:weapon_type=shield": ARM_SHIELD,             # 3
    "met:classification=Shields": ARM_SHIELD,        # 3
    "ra:cv=shields": ARM_SHIELD,                     # 2
    "name:tok=shield": ARM_SHIELD,                   # 2

    # Body/head armor (D1c excluded) — everything else under armor parent
    # These are listed explicitly for documentation; default-fall-through
    # also catches any unenumerated method strings.
    "ra:cv=complete armours": ARM_BODY_OR_HEAD,                         # 56
    "met:classification=Helmets": ARM_BODY_OR_HEAD,                     # 10
    "met:classification=Armor Parts-Thigh and Leg Defense": ARM_BODY_OR_HEAD,  # 9
    "met:classification=Armor Parts": ARM_BODY_OR_HEAD,                 # 5
    "met:classification=Armor for Man": ARM_BODY_OR_HEAD,               # 5
    "met:classification=Armor Parts-Knee Defenses": ARM_BODY_OR_HEAD,   # 4
    "ra:cv=helmets": ARM_BODY_OR_HEAD,                                  # 3
    "ra:cv=armour pieces": ARM_BODY_OR_HEAD,                            # 3
    "met:classification=Armor for Man-1/2 Armor": ARM_BODY_OR_HEAD,     # 2
    "met:classification=Armor Parts-Masks": ARM_BODY_OR_HEAD,           # 2
    "met:classification=Armor Parts-Gauntlets": ARM_BODY_OR_HEAD,       # 2
    "met:classification=Armor for Horse and Man": ARM_BODY_OR_HEAD,     # 2
    "met:classification=Armor": ARM_BODY_OR_HEAD,                       # 2
    "met:classification=Armor Parts-Cuirasses": ARM_BODY_OR_HEAD,       # 2
    "met:classification=Armor Parts-Arms & Shoulders": ARM_BODY_OR_HEAD,  # 1
    "met:classification=Armor Parts-Sollerets": ARM_BODY_OR_HEAD,       # 1
    "met:classification=Armor for Horse": ARM_BODY_OR_HEAD,             # 1
    "met:classification=Armor Parts-Colletins": ARM_BODY_OR_HEAD,       # 1
    "met:classification=Helmets Parts": ARM_BODY_OR_HEAD,               # 1
    "met:classification=Mail": ARM_BODY_OR_HEAD,                        # 1
    "name:tok=armour": ARM_BODY_OR_HEAD,                                # 1 (Timoney APC — out-of-genre but classified armor; flagged in trace)
    "name:tok=plate armor": ARM_BODY_OR_HEAD,                           # 1 (Statuette — art-object but classified armor; flagged in trace)
}

# Method strings flagged for trace.notes — ambiguous or low-confidence routing.
AMBIGUOUS_METHODS = {
    "ra:cv=militaria": "display/storage object (Forsyth Primer display board / officer's helmet storage tin) — closest sub-fit accessory_handheld but not a combat item; gandalf-review candidate.",
    "name:tok=armour": "Timoney (armoured personnel carrier) — military vehicle, out-of-genre for Reincarnated v1; D1c excluded as armor_body_or_head; gandalf may re-route to siege_vehicle in a later stage.",
    "name:tok=plate armor": "Statuette of Knight Wearing Chain-mail and Plate Armor — art object, not combat armor; D1c excluded as armor_body_or_head; gandalf may re-route to art_object in a later stage.",
}


def subdivide_accessory(method: str) -> tuple[str, str | None]:
    """Return (subcategory, note) for an accessory row."""
    note = AMBIGUOUS_METHODS.get(method)
    if method in ACCESSORY_METHOD_RULES:
        return ACCESSORY_METHOD_RULES[method], note
    # Fallback: route to accessory_handheld with explicit note for gandalf review
    return ACC_HANDHELD, f"unenumerated_method={method!r} — defaulted to accessory_handheld; gandalf review."


def subdivide_armor(method: str) -> tuple[str, str | None]:
    """Return (subcategory, note) for an armor row."""
    note = AMBIGUOUS_METHODS.get(method)
    if method in ARMOR_METHOD_RULES:
        return ARMOR_METHOD_RULES[method], note
    # Fallback: route to armor_body_or_head (D1c-excluded; safe default)
    return ARM_BODY_OR_HEAD, f"unenumerated_method={method!r} — defaulted to armor_body_or_head; gandalf review."


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load Stage 2.5 classifier output
    with STAGE_2_5_JSON.open() as f:
        stage_2_5 = json.load(f)
    classifications: list[dict] = stage_2_5["classifications"]
    assert len(classifications) == 1126, f"expected 1126 Tier-S classifications, got {len(classifications)}"

    parent_counts = Counter(c["category"] for c in classifications)
    print("Stage 2.5 JSON loaded — parent counts:")
    for k, v in parent_counts.most_common():
        print(f"  {k}: {v}")

    # Subdivide accessory + armor
    accessory_rows = [c for c in classifications if c["category"] == "accessory"]
    armor_rows = [c for c in classifications if c["category"] == "armor"]
    assert len(accessory_rows) == 130, f"expected 130 accessory rows, got {len(accessory_rows)}"
    assert len(armor_rows) == 125, f"expected 125 armor rows, got {len(armor_rows)}"

    subdivided: list[dict] = []
    sub_counts: Counter[str] = Counter()
    notes_records: list[dict] = []

    for c in accessory_rows:
        subcat, note = subdivide_accessory(c["method"])
        rec = dict(c)
        rec["weapon_kind_classified_subtype"] = subcat
        rec["subdivision_method"] = "stage_3_phase_0a_accessory"
        rec["subdivision_note"] = note
        subdivided.append(rec)
        sub_counts[subcat] += 1
        if note:
            notes_records.append({"id": c["id"], "subcat": subcat, "note": note, "canonical_name": c["canonical_name"]})

    for c in armor_rows:
        subcat, note = subdivide_armor(c["method"])
        rec = dict(c)
        rec["weapon_kind_classified_subtype"] = subcat
        rec["subdivision_method"] = "stage_3_phase_0a_armor"
        rec["subdivision_note"] = note
        subdivided.append(rec)
        sub_counts[subcat] += 1
        if note:
            notes_records.append({"id": c["id"], "subcat": subcat, "note": note, "canonical_name": c["canonical_name"]})

    print()
    print("Phase 0a subcategory counts:")
    for k in (ACC_HANDHELD, ACC_WEAPON_INTEGRATED, ACC_HORSE, ARM_SHIELD, ARM_BODY_OR_HEAD):
        print(f"  {k}: {sub_counts[k]}")
    print(f"  TOTAL: {sum(sub_counts.values())}")

    # Build final values for DB UPDATE: for every Tier-S row, the subtype is
    # either (a) the subdivided value for accessory/armor or (b) the parent
    # category as-is for handheld_weapon / siege_vehicle / art_object / other /
    # ammo_consumable. This makes the column the single source of truth that
    # D1a auto-include rule references.
    final_values: list[tuple[str, int]] = []
    subdivided_by_id = {r["id"]: r["weapon_kind_classified_subtype"] for r in subdivided}
    for c in classifications:
        rid = c["id"]
        if rid in subdivided_by_id:
            v = subdivided_by_id[rid]
        else:
            v = c["category"]  # handheld_weapon, siege_vehicle, art_object, other, ammo_consumable
        final_values.append((v, rid))

    # Verify D1a count survives (449 handheld_weapon)
    final_count_by_subtype = Counter(v for v, _ in final_values)
    print()
    print("Final column-value distribution (all 1,126 Tier-S rows):")
    for k, v in final_count_by_subtype.most_common():
        print(f"  {k}: {v}")
    assert final_count_by_subtype["handheld_weapon"] == 449, "D1a handheld_weapon count drift detected"

    # ALTER TABLE + UPDATE
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()

        # Check if column exists; ALTER if not
        cursor.execute("PRAGMA table_info(weapon_knowledge_entries)")
        cols = {row[1] for row in cursor.fetchall()}
        if "weapon_kind_classified_subtype" not in cols:
            print()
            print("Adding column weapon_kind_classified_subtype (TEXT, nullable, no CHECK)...")
            cursor.execute(
                "ALTER TABLE weapon_knowledge_entries "
                "ADD COLUMN weapon_kind_classified_subtype TEXT"
            )
            conn.commit()
        else:
            print()
            print("Column weapon_kind_classified_subtype already exists; proceeding with UPDATE.")

        # UPDATE all 1,126 Tier-S rows
        print(f"Updating {len(final_values)} Tier-S rows...")
        cursor.executemany(
            "UPDATE weapon_knowledge_entries SET weapon_kind_classified_subtype = ? WHERE id = ?",
            final_values,
        )
        conn.commit()

        # Verify
        cursor.execute(
            "SELECT weapon_kind_classified_subtype, COUNT(*) "
            "FROM weapon_knowledge_entries "
            "WHERE quality_tier = 'S' "
            "GROUP BY weapon_kind_classified_subtype "
            "ORDER BY 2 DESC"
        )
        print()
        print("Verification — DB Tier-S rows by weapon_kind_classified_subtype:")
        db_counts = {row[0]: row[1] for row in cursor.fetchall()}
        for k, v in sorted(db_counts.items(), key=lambda x: -x[1]):
            print(f"  {k}: {v}")
        assert db_counts["handheld_weapon"] == 449, "post-UPDATE handheld_weapon count drift"
        assert db_counts[ACC_HANDHELD] + db_counts[ACC_WEAPON_INTEGRATED] + db_counts[ACC_HORSE] == 130, "accessory subcategory sum != 130"
        assert db_counts[ARM_SHIELD] + db_counts[ARM_BODY_OR_HEAD] == 125, "armor subcategory sum != 125"

        # Non-Tier-S rows must remain NULL (no leakage)
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE quality_tier IS NULL OR quality_tier <> 'S'"
        )
        non_tier_s = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE (quality_tier IS NULL OR quality_tier <> 'S') "
            "AND weapon_kind_classified_subtype IS NOT NULL"
        )
        non_tier_s_populated = cursor.fetchone()[0]
        print()
        print(f"Non-Tier-S rows: {non_tier_s} (expected {89841 - 1126} = {89841 - 1126})")
        print(f"Non-Tier-S rows with populated weapon_kind_classified_subtype: {non_tier_s_populated} (must be 0)")
        assert non_tier_s_populated == 0, "non-Tier-S leak detected"

    finally:
        conn.close()

    # Emit JSON companion artifact (full row-level details for downstream Phases)
    out_json = OUT_DIR / "accessory-armor-subcategory-classification.json"
    out_payload = {
        "phase": "cycle-10-stage-3-phase-0a",
        "date": "2026-05-25",
        "dispatch": (
            "agentic_orchestration/dispatches/"
            "2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md"
        ),
        "composition_policy": (
            "canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md § 1.1"
        ),
        "totals": {
            "accessory_input": 130,
            "armor_input": 125,
            "total_subdivided": 255,
        },
        "subcategory_counts": {k: sub_counts[k] for k in (
            ACC_HANDHELD, ACC_WEAPON_INTEGRATED, ACC_HORSE, ARM_SHIELD, ARM_BODY_OR_HEAD
        )},
        "d1b_allow_list_size": sub_counts[ACC_HANDHELD] + sub_counts[ACC_WEAPON_INTEGRATED] + sub_counts[ARM_SHIELD],
        "d1c_excluded_size": sub_counts[ACC_HORSE] + sub_counts[ARM_BODY_OR_HEAD],
        "ambiguous_or_flagged_rows": notes_records,
        "rows": subdivided,
    }
    with out_json.open("w") as f:
        json.dump(out_payload, f, indent=2, ensure_ascii=False)
    print()
    print(f"Wrote {out_json}")
    print(f"Ambiguous/flagged rows: {len(notes_records)}")


if __name__ == "__main__":
    main()
