#!/usr/bin/env python3
"""
Cycle 10 Wave 5.5 Phase 0c — Tier-A NULL-Subtype Classifier Extension

Per dispatch agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-
phase-0c-and-mode-c-eviction.md § 3.1 + gandalf sign-off (`2026-05-25-stage-3-
distribution-report-sign-off.md` § 3 Condition 1) + gandalf SO-4 RATIFY-WITH-
AMENDMENT (`2026-05-25-so-1-2-4-sign-off-verdicts.md`).

Extends the Phase 0a heuristic-classifier pattern from Tier-S (1,126 rows;
`accessory-armor-subcategory-classification.md`) to the Tier-A NULL-subtype pool.
The dispatch describes this pool as "940 rows" (figure originally from gandalf
50-row spot-check § Diagnosis 1, which counted Tier-A v1_scope=1 NULL-typed
rows). Empirically this script operates on the broader Tier-A NULL-subtype pool
(7,943 rows DB-wide; 1,431 within v1_scope=1). Classification value extends
beyond v1_scope; v1_scope downgrade applies only to the v1_scope=1 subset that
classifies to D1c-excluded subtypes.

Per-source heuristic strategy (see Phase 0a precedent § 2.1 — keyed on source-
side structured signal at higher fidelity than canonical_name token-matching):

  met-museum         → structured_properties.classification
  royal_armouries    → structured_properties.object_type[0] + .category_type
  odin-army-tradoc   → structured_properties.properties."System.Type" (all
                       military_modern; siege_vehicle dominant)
  wikipedia          → structured_properties.type (military-modern weapon types)
  wow-classic-items  → canonical_name token + structured_properties heuristics
  nick-aschenbach-dnd-data → canonical_name token + structured_properties
  pf2ools / wikidata → canonical_name token fallback (rare in this pool)

Heuristic only — no LLM cost. Per Discipline #11, prints empirical counts pre/
post + emits an exhaustive JSON trace of per-row classification rationale.

The Wave 5.5 pass is ADDITIVE: it (a) populates weapon_kind_classified_subtype
on Tier-A NULL-subtype rows, (b) for v1_scope=1 Tier-A rows that classify to
D1c-excluded subtypes (siege_vehicle / art_object / other / ammo_consumable /
accessory_horse_or_equipment / armor_body_or_head), it sets v1_scope=0 and
appends 'd1c_excluded_scope_deferred_tier_a_post_phase_0c' to the trace.
"""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
OUT_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond"
    "/research/cycle-10-wave-5-5-2026-05-25"
)

# -----------------------------------------------------------------------------
# Sub-category enums (consistent with Phase 0a vocabulary)
# -----------------------------------------------------------------------------
HANDHELD_WEAPON = "handheld_weapon"                       # D1a allowed
SIEGE_VEHICLE = "siege_vehicle"                           # D1c excluded
ARM_SHIELD = "armor_shield"                               # D1b allowed
ARM_BODY = "armor_body_or_head"                           # D1c excluded
ACC_HANDHELD = "accessory_handheld"                       # D1b allowed
ACC_WEAPON_INTEGRATED = "accessory_weapon_integrated"     # D1b allowed
ACC_HORSE = "accessory_horse_or_equipment"                # D1c excluded
ART_OBJECT = "art_object"                                 # D1c excluded
OTHER = "other"                                           # D1c excluded
AMMO = "ammo_consumable"                                  # D1c excluded

D1C_EXCLUDED = {SIEGE_VEHICLE, ART_OBJECT, OTHER, AMMO, ACC_HORSE, ARM_BODY}
D1A_ALLOWED = {HANDHELD_WEAPON}
D1B_ALLOWED = {ARM_SHIELD, ACC_HANDHELD, ACC_WEAPON_INTEGRATED}

# -----------------------------------------------------------------------------
# Met-museum classification rules (extends Phase 0a vocabulary)
# -----------------------------------------------------------------------------
# Phase 0a covered the Tier-S subset; Tier-A pool surfaces additional class
# strings. Exact-prefix match (the classification field uses dash-separated
# hierarchical paths; prefix matching captures sub-leaves).
MET_RULES_PREFIX: list[tuple[str, str]] = [
    # Order matters — longest/most-specific prefixes first
    ("Sword Furniture", ACC_WEAPON_INTEGRATED),
    ("Firearms Accessories", ACC_WEAPON_INTEGRATED),
    ("Firearms Equipment", ACC_WEAPON_INTEGRATED),
    ("Equestrian Equipment", ACC_HORSE),
    ("Equestrian", ACC_HORSE),
    ("Armor for Horse", ARM_BODY),
    ("Armor for Man", ARM_BODY),
    ("Armor Parts", ARM_BODY),
    ("Helmets Parts", ARM_BODY),
    ("Helmets", ARM_BODY),
    ("Helmet Crests", ARM_BODY),
    ("Mail", ARM_BODY),
    ("Brigandines", ARM_BODY),
    ("Surcoat", ARM_BODY),
    ("Cuirass", ARM_BODY),
    ("Armor", ARM_BODY),  # catch-all for 'Armor', 'Armor ...' that didn't match above
    ("Shields", ARM_SHIELD),
    ("Banners", ACC_HANDHELD),
    ("Costumes", ACC_HANDHELD),
    ("Archery Equipment-Archer's Ring", ACC_HANDHELD),
    ("Archery Equipment-Arrows & Quivers", AMMO),
    ("Archery Equipment", HANDHELD_WEAPON),  # bows
    ("Shafted Weapons", HANDHELD_WEAPON),    # spears, halberds, polearms
    ("Swords", HANDHELD_WEAPON),
    ("Daggers", HANDHELD_WEAPON),
    ("Knives", HANDHELD_WEAPON),
    ("Krisses", HANDHELD_WEAPON),
    ("Sabres", HANDHELD_WEAPON),
    ("Rapiers", HANDHELD_WEAPON),
    ("Axes", HANDHELD_WEAPON),
    ("Maces", HANDHELD_WEAPON),
    ("Hammers", HANDHELD_WEAPON),
    ("Clubs", HANDHELD_WEAPON),
    ("Whips", HANDHELD_WEAPON),
    ("Fencing", HANDHELD_WEAPON),
    ("Staff", HANDHELD_WEAPON),
    ("Polearms", HANDHELD_WEAPON),
    ("Firearms-Pistols", HANDHELD_WEAPON),  # firearms in Wave 5.5: assigned handheld_weapon for D1a;
                                            # Mode-C eviction in Part B handles modern_industrial filtration
    ("Firearms-Guns", HANDHELD_WEAPON),
    ("Firearms", HANDHELD_WEAPON),
    ("Cannon", SIEGE_VEHICLE),
    ("Artillery", SIEGE_VEHICLE),
    ("Mortars", SIEGE_VEHICLE),
    ("Tools", OTHER),                       # craft tools, not weapons
    ("Books & Manuscripts", ART_OBJECT),
    ("Sculpture", ART_OBJECT),
    ("Glass-Vessels", ART_OBJECT),
    ("Glass", ART_OBJECT),
    ("Coins", ART_OBJECT),
    ("Medals", ART_OBJECT),
    ("Drawings", ART_OBJECT),
    ("Prints", ART_OBJECT),
    ("Photographs", ART_OBJECT),
    ("Paintings", ART_OBJECT),
    ("Forgeries", ART_OBJECT),              # museum-categorized forgeries
    ("Miscellaneous-Buckles & Ornament", ACC_HORSE),  # Phase 0a empirically: all horse-trappings
    ("Miscellaneous-Coins and Medals", ART_OBJECT),
    ("Miscellaneous", OTHER),
]

# -----------------------------------------------------------------------------
# Royal Armouries object_type rules (object_type is an array; use [0])
# -----------------------------------------------------------------------------
RA_OBJECT_TYPE_RULES: dict[str, str] = {
    # Weapons (D1a)
    "Swords": HANDHELD_WEAPON,
    "Daggers, knives and bayonets": HANDHELD_WEAPON,
    "Maces, hammers, axes, and clubs": HANDHELD_WEAPON,
    "Staff weapons": HANDHELD_WEAPON,
    "Bows, arrows, crossbows, and related equipment": HANDHELD_WEAPON,  # bows are weapons; arrows are AMMO — refine below via name token
    "Combination weapons": HANDHELD_WEAPON,
    # Armor + accessories
    "Armour": ARM_BODY,
    "Animal armour and Equestrian Equipment": ACC_HORSE,
    "Ammunition & Artillery projectiles": AMMO,
    # Heavy weapons / siege
    "Artillery & Equipment": SIEGE_VEHICLE,
    # Display / art
    "Sculptures, mannequins, and trophies": ART_OBJECT,
    "Art": ART_OBJECT,
    "Replicas, fakes, and forgeries": ART_OBJECT,
    "Instruments of torture and punishment": OTHER,
    "Militaria": OTHER,         # belt pouches, badges, miscellaneous militaria
    "Miscellaneous": OTHER,
    # Firearms — handheld_weapon at this pass; Mode-C eviction handles modern_industrial subset
    "Firearms & Equipment": HANDHELD_WEAPON,
}

# Some firearms have category_type='Firearms & Artillery' — split via object_type below
RA_CATEGORY_TYPE_RULES: dict[str, str] = {
    "Firearms & Artillery": HANDHELD_WEAPON,   # default; Mode-C eviction Wave 5.5 Part B handles modern_industrial
    "Edged Weapons": HANDHELD_WEAPON,
    "Armour": ARM_BODY,                        # body armor default
    "Miscellany": OTHER,
}

# Name-token refinements for RA rows (applied after primary rule)
RA_NAMETOK_OVERRIDES: list[tuple[str, str]] = [
    # Token         Subtype                  Note
    ("shield", ARM_SHIELD),                   # promoted from ARM_BODY when 'shield' in name
    ("buckler", ARM_SHIELD),
    ("targe", ARM_SHIELD),
    ("rondache", ARM_SHIELD),
    ("pavise", ARM_SHIELD),
    ("arrow", AMMO),                          # arrows from the bow group
    ("bolt", AMMO),                           # crossbow bolts
    ("quiver", ACC_WEAPON_INTEGRATED),
    ("scabbard", ACC_WEAPON_INTEGRATED),
    ("sheath", ACC_WEAPON_INTEGRATED),
    ("powder horn", ACC_WEAPON_INTEGRATED),
    ("powder flask", ACC_WEAPON_INTEGRATED),
    ("magazine", ACC_WEAPON_INTEGRATED),
    ("bayonet", ACC_WEAPON_INTEGRATED),       # spot-check FAIL example: bayonets paired to firearm
    ("primer", ACC_WEAPON_INTEGRATED),
    ("cartridge", AMMO),
    ("bullet", AMMO),
    ("shell", AMMO),
    ("musket ball", AMMO),
    ("grenade", AMMO),
    ("torpedo", AMMO),
    ("mine", AMMO),
    ("plinth", ART_OBJECT),
    ("statuette", ART_OBJECT),
    ("painting", ART_OBJECT),
    ("medal", ART_OBJECT),
    # Helmet sub-tokens (force ARM_BODY for unambiguous head gear)
    ("helmet", ARM_BODY),
    ("sallet", ARM_BODY),
    ("bacinet", ARM_BODY),
    ("bascinet", ARM_BODY),
    ("barbute", ARM_BODY),
    ("burgonet", ARM_BODY),
    ("morion", ARM_BODY),
    ("kettle hat", ARM_BODY),
    ("close helm", ARM_BODY),
    ("armet", ARM_BODY),
    ("bevor", ARM_BODY),                      # spot-check FAIL example: chin defense
    ("gorget", ARM_BODY),
    ("cuisse", ARM_BODY),                     # spot-check FAIL example: leg armor
    ("greave", ARM_BODY),
    ("pauldron", ARM_BODY),
    ("vambrace", ARM_BODY),
    ("gauntlet", ARM_BODY),
    ("breastplate", ARM_BODY),
    ("cuirass", ARM_BODY),
    ("backplate", ARM_BODY),
    ("brigandine", ARM_BODY),
    ("jerkin", ARM_BODY),
    ("doublet", ARM_BODY),
    ("mail coif", ARM_BODY),
    ("riding boot", ACC_HORSE),               # spot-check FAIL example
    ("saddle", ACC_HORSE),
    ("stirrup", ACC_HORSE),
    ("rein", ACC_HORSE),
    ("bridle", ACC_HORSE),
    ("spur", ACC_HORSE),
    ("bit ", ACC_HORSE),
    # Vehicle subtypes within Firearms & Artillery
    ("gun carriage", SIEGE_VEHICLE),
    ("limber", SIEGE_VEHICLE),
    ("howitzer", SIEGE_VEHICLE),
    ("mortar", SIEGE_VEHICLE),
    ("cannon", SIEGE_VEHICLE),
]

# -----------------------------------------------------------------------------
# Odin-army-tradoc rules — System.Type signature lookup
# -----------------------------------------------------------------------------
# Empirically virtually all odin-army-tradoc rows are vehicles, missiles, UAVs,
# drone systems, naval craft, anti-personnel mines, etc. — D1c-excluded
# siege_vehicle. The few exceptions (Sniper Rifle, Mortar, etc.) are still
# heavy-military / modern hardware and resolve via secondary rules.

ODIN_SYSTEM_TYPE_HANDHELD_TOKENS = {
    "sniper rifle", "assault rifle", "battle rifle", "designated marksman",
    "machine pistol", "carbine", "shotgun", "submachine gun",
}
ODIN_SYSTEM_TYPE_HEAVY_TOKENS = {
    "machine gun", "anti-tank guided missile", "atgm", "rpg", "rocket launcher",
    "mortar", "grenade launcher", "anti-aircraft", "anti-personnel mine",
    "anti-vehicle mine",
}
ODIN_SYSTEM_TYPE_AMMO_TOKENS = {
    "missile", "mine", "rocket", "munition", "warhead", "bomb",
    "anti-personnel mine", "anti-vehicle mine",
}

# Default for odin-army-tradoc when System.Type doesn't match a non-siege bucket
ODIN_DEFAULT = SIEGE_VEHICLE

# -----------------------------------------------------------------------------
# Wikipedia type-field rules (military-modern weapons primarily)
# -----------------------------------------------------------------------------
# Wikipedia rows often have HTML-comment debris in the type field; normalize.

WIKIPEDIA_TYPE_HEAVY_TOKENS = {
    "naval gun", "anti-tank gun", "field gun", "mountain gun", "railway gun",
    "railroad gun", "coast defence gun", "anti-aircraft gun", "howitzer",
    "multiple rocket launcher", "cruise missile", "intercontinental ballistic",
    "ballistic missile", "anti-ship missile", "anti-tank missile", "anti-aircraft missile",
    "heavy tank", "light tank", "cruiser tank", "main battle tank",
    "infantry mobility vehicle", "armored personnel carrier", "infantry fighting vehicle",
    "self-propelled", "anti-tank rocket", "anti-radiation missile",
    "surface-to-air missile",
}
WIKIPEDIA_TYPE_HANDHELD_TOKENS = {
    "revolver", "semi-automatic pistol", "automatic pistol", "machine pistol",
    "submachine gun", "assault rifle", "battle rifle", "sniper rifle",
    "bolt-action rifle", "semi-automatic rifle", "rifle", "shotgun",
    "light machine gun", "heavy machine gun", "machine gun", "carbine",
    "musket", "pistol",
}

# -----------------------------------------------------------------------------
# Generic name-token fallback (applied to any row without primary signal)
# -----------------------------------------------------------------------------
NAME_TOK_RULES: list[tuple[str, str]] = [
    # weapons
    ("sword", HANDHELD_WEAPON),
    ("dagger", HANDHELD_WEAPON),
    ("knife", HANDHELD_WEAPON),
    ("axe", HANDHELD_WEAPON),
    ("hammer", HANDHELD_WEAPON),
    ("mace", HANDHELD_WEAPON),
    ("spear", HANDHELD_WEAPON),
    ("lance", HANDHELD_WEAPON),
    ("halberd", HANDHELD_WEAPON),
    ("polearm", HANDHELD_WEAPON),
    ("staff", HANDHELD_WEAPON),
    ("bow", HANDHELD_WEAPON),
    ("crossbow", HANDHELD_WEAPON),
    ("club", HANDHELD_WEAPON),
    ("flail", HANDHELD_WEAPON),
    ("whip", HANDHELD_WEAPON),
    ("rapier", HANDHELD_WEAPON),
    ("sabre", HANDHELD_WEAPON),
    ("saber", HANDHELD_WEAPON),
    ("scimitar", HANDHELD_WEAPON),
    ("katana", HANDHELD_WEAPON),
    ("musket", HANDHELD_WEAPON),
    ("rifle", HANDHELD_WEAPON),
    ("pistol", HANDHELD_WEAPON),
    ("revolver", HANDHELD_WEAPON),
    ("carbine", HANDHELD_WEAPON),
    ("shotgun", HANDHELD_WEAPON),
    # shields
    ("shield", ARM_SHIELD),
    ("buckler", ARM_SHIELD),
    ("targe", ARM_SHIELD),
    # armor
    ("helmet", ARM_BODY),
    ("helm", ARM_BODY),
    ("breastplate", ARM_BODY),
    ("cuirass", ARM_BODY),
    ("armour", ARM_BODY),
    ("armor", ARM_BODY),
    ("mail", ARM_BODY),
    ("gauntlet", ARM_BODY),
    ("greave", ARM_BODY),
    # accessories
    ("banner", ACC_HANDHELD),
    ("scabbard", ACC_WEAPON_INTEGRATED),
    ("sheath", ACC_WEAPON_INTEGRATED),
    ("powder horn", ACC_WEAPON_INTEGRATED),
    ("powder flask", ACC_WEAPON_INTEGRATED),
    ("magazine", ACC_WEAPON_INTEGRATED),
    ("bayonet", ACC_WEAPON_INTEGRATED),
    # siege
    ("cannon", SIEGE_VEHICLE),
    ("howitzer", SIEGE_VEHICLE),
    ("mortar", SIEGE_VEHICLE),
    ("artillery", SIEGE_VEHICLE),
    ("tank", SIEGE_VEHICLE),
    ("uav", SIEGE_VEHICLE),
    ("drone", SIEGE_VEHICLE),
    ("missile system", SIEGE_VEHICLE),
    ("helicopter", SIEGE_VEHICLE),
    # ammo
    ("arrow", AMMO),
    ("bolt", AMMO),
    ("cartridge", AMMO),
    ("missile", AMMO),
    ("rocket", AMMO),
    ("grenade", AMMO),
    ("mine", AMMO),
    ("torpedo", AMMO),
]


def normalize(s: str | None) -> str:
    if s is None:
        return ""
    # strip wikipedia HTML-comment debris
    cleaned = s
    while "<!--" in cleaned and "-->" in cleaned:
        a = cleaned.index("<!--")
        b = cleaned.index("-->", a) + 3
        cleaned = cleaned[:a] + cleaned[b:]
    return cleaned.strip().lower()


def classify_met_museum(row: dict) -> tuple[str, str]:
    """Return (subtype, rationale)."""
    sp = row.get("sp") or {}
    cls = sp.get("classification") or ""
    if not cls:
        return classify_by_name_token(row, fallback=OTHER, prefix="met:empty-classification ")
    for prefix, subtype in MET_RULES_PREFIX:
        if cls.startswith(prefix):
            return subtype, f"met:classification={cls!r} → prefix={prefix!r}"
    # Fallback to name-token
    return classify_by_name_token(row, fallback=OTHER, prefix=f"met:classification={cls!r} unmatched-prefix; ")


def classify_royal_armouries(row: dict) -> tuple[str, str]:
    sp = row.get("sp") or {}
    object_type = sp.get("object_type") or []
    obj0 = object_type[0] if isinstance(object_type, list) and object_type else ""
    cat = sp.get("category_type") or ""
    name = (row.get("canonical_name") or "").lower()

    # Primary rule from object_type[0]
    primary = RA_OBJECT_TYPE_RULES.get(obj0)
    if primary is None and cat in RA_CATEGORY_TYPE_RULES:
        primary = RA_CATEGORY_TYPE_RULES[cat]
    if primary is None:
        primary = OTHER
        primary_note = f"ra:object_type[0]={obj0!r} + category_type={cat!r} unmatched → default OTHER"
    else:
        primary_note = f"ra:object_type[0]={obj0!r} → {primary}"
        if obj0 == "" and cat:
            primary_note = f"ra:category_type={cat!r} → {primary}"

    # Name-token overrides — these refine the primary
    for tok, override in RA_NAMETOK_OVERRIDES:
        if tok in name:
            return override, f"{primary_note}; name_tok={tok!r} → override {override}"

    return primary, primary_note


def classify_odin_army(row: dict) -> tuple[str, str]:
    sp = row.get("sp") or {}
    props = sp.get("properties") or {}
    sys_type = (props.get("System.Type") or "").lower().strip()
    name = (row.get("canonical_name") or "").lower()

    # Order matters — check ammo tokens first (more specific), then handheld, then heavy
    for tok in ODIN_SYSTEM_TYPE_AMMO_TOKENS:
        if tok in sys_type or tok in name:
            return AMMO, f"odin:System.Type={sys_type!r} → ammo via tok={tok!r}"
    for tok in ODIN_SYSTEM_TYPE_HANDHELD_TOKENS:
        if tok in sys_type:
            return HANDHELD_WEAPON, f"odin:System.Type={sys_type!r} → handheld via tok={tok!r}"
    for tok in ODIN_SYSTEM_TYPE_HEAVY_TOKENS:
        if tok in sys_type:
            return SIEGE_VEHICLE, f"odin:System.Type={sys_type!r} → siege via tok={tok!r}"
    return ODIN_DEFAULT, f"odin:System.Type={sys_type!r} → default siege_vehicle"


def classify_wikipedia(row: dict) -> tuple[str, str]:
    sp = row.get("sp") or {}
    t = normalize(sp.get("type"))
    if not t:
        return classify_by_name_token(row, fallback=OTHER, prefix="wiki:empty-type; ")
    for tok in WIKIPEDIA_TYPE_HEAVY_TOKENS:
        if tok in t:
            return SIEGE_VEHICLE, f"wiki:type={t!r} → siege via tok={tok!r}"
    for tok in WIKIPEDIA_TYPE_HANDHELD_TOKENS:
        if tok in t:
            return HANDHELD_WEAPON, f"wiki:type={t!r} → handheld via tok={tok!r}"
    # Ammo tokens
    for tok in ("missile", "rocket", "torpedo", "mine"):
        if tok in t and "missile system" not in t:
            return AMMO, f"wiki:type={t!r} → ammo via tok={tok!r}"
    return classify_by_name_token(row, fallback=OTHER, prefix=f"wiki:type={t!r} unmatched; ")


def classify_by_name_token(row: dict, fallback: str, prefix: str = "") -> tuple[str, str]:
    name = (row.get("canonical_name") or "").lower()
    for tok, subtype in NAME_TOK_RULES:
        if tok in name:
            return subtype, f"{prefix}name_tok={tok!r} → {subtype}"
    return fallback, f"{prefix}no name_tok match → fallback={fallback}"


def classify_generic(row: dict) -> tuple[str, str]:
    """Fallback for sources without per-source rules (wow-classic-items, dnd, etc.)."""
    return classify_by_name_token(row, fallback=OTHER, prefix=f"generic[{row.get('source_library')}]; ")


SOURCE_CLASSIFIER = {
    "met-museum": classify_met_museum,
    "royal_armouries": classify_royal_armouries,
    "odin-army-tradoc": classify_odin_army,
    "wikipedia": classify_wikipedia,
}


def classify(row: dict) -> tuple[str, str]:
    src = row.get("source_library")
    fn = SOURCE_CLASSIFIER.get(src, classify_generic)
    return fn(row)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()

        # Pre-state empirical query (Discipline #11)
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE quality_tier='A' AND weapon_kind_classified_subtype IS NULL"
        )
        pre_null = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE quality_tier='A' AND v1_scope=1 AND weapon_kind_classified_subtype IS NULL"
        )
        pre_v1_scope_null = cursor.fetchone()[0]
        print(f"Pre-Wave-5.5: Tier-A NULL-subtype = {pre_null}; of which v1_scope=1 = {pre_v1_scope_null}")

        cursor.execute(
            "SELECT id, canonical_name, source_library, structured_properties, "
            "       quality_tier, v1_scope, v1_scope_composition_trace "
            "FROM weapon_knowledge_entries "
            "WHERE quality_tier='A' AND weapon_kind_classified_subtype IS NULL "
            "ORDER BY id"
        )
        rows = []
        for r in cursor.fetchall():
            sp_raw = r["structured_properties"]
            sp = None
            if sp_raw:
                try:
                    sp = json.loads(sp_raw)
                except (json.JSONDecodeError, TypeError):
                    sp = {}
            rows.append({
                "id": r["id"],
                "canonical_name": r["canonical_name"],
                "source_library": r["source_library"],
                "quality_tier": r["quality_tier"],
                "v1_scope": r["v1_scope"],
                "v1_scope_composition_trace": r["v1_scope_composition_trace"],
                "sp": sp or {},
            })
        print(f"Loaded {len(rows)} Tier-A NULL-subtype rows for classification")

        # Classify
        classified: list[dict] = []
        by_source: Counter[str] = Counter()
        by_subtype: Counter[str] = Counter()
        by_source_subtype: Counter[tuple[str, str]] = Counter()
        for row in rows:
            subtype, rationale = classify(row)
            classified.append({
                "id": row["id"],
                "canonical_name": row["canonical_name"],
                "source_library": row["source_library"],
                "v1_scope": row["v1_scope"],
                "subtype": subtype,
                "rationale": rationale,
                "v1_scope_downgrade_eligible": (
                    bool(row["v1_scope"]) and subtype in D1C_EXCLUDED
                ),
            })
            by_source[row["source_library"]] += 1
            by_subtype[subtype] += 1
            by_source_subtype[(row["source_library"], subtype)] += 1

        print()
        print("Per-subtype classification counts:")
        for k, v in by_subtype.most_common():
            scope_flag = "  D1A" if k in D1A_ALLOWED else "  D1B" if k in D1B_ALLOWED else "  D1C-EXCL"
            print(f"  {k:<35}{scope_flag} {v}")

        print()
        print("Per-source × subtype counts:")
        for src in sorted({c["source_library"] for c in classified}):
            print(f"  -- {src} (total {by_source[src]}) --")
            sub_for_src = {s: by_source_subtype[(src, s)] for s in by_subtype if (src, s) in by_source_subtype}
            for s, c in sorted(sub_for_src.items(), key=lambda x: -x[1]):
                print(f"    {s:<35} {c}")

        # v1_scope downgrade candidates
        downgrade_candidates = [c for c in classified if c["v1_scope_downgrade_eligible"]]
        print()
        print(f"v1_scope downgrade candidates (Tier-A v1_scope=1 classifying to D1c-excluded): {len(downgrade_candidates)}")
        dg_by_subtype: Counter[str] = Counter(c["subtype"] for c in downgrade_candidates)
        for s, c in dg_by_subtype.most_common():
            print(f"  {s:<35} {c}")

        # ----- Apply UPDATE to DB -----
        # Step 1: populate weapon_kind_classified_subtype for all Tier-A NULL-subtype rows
        sub_values = [(c["subtype"], c["id"]) for c in classified]
        cursor.executemany(
            "UPDATE weapon_knowledge_entries "
            "SET weapon_kind_classified_subtype = ? "
            "WHERE id = ?",
            sub_values,
        )
        conn.commit()
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE quality_tier='A' AND weapon_kind_classified_subtype IS NOT NULL"
        )
        post_pop = cursor.fetchone()[0]
        print()
        print(f"Post-UPDATE Tier-A non-NULL subtype: {post_pop} (expected ~{pre_null})")

        # Step 2: downgrade v1_scope for D1c-excluded rows; append to composition_trace
        downgrade_updates: list[tuple[str, int]] = []
        for c in downgrade_candidates:
            # Read existing trace (already in row)
            cursor.execute(
                "SELECT v1_scope_composition_trace FROM weapon_knowledge_entries WHERE id = ?",
                (c["id"],),
            )
            existing_trace_raw = cursor.fetchone()[0]
            try:
                existing_trace = json.loads(existing_trace_raw) if existing_trace_raw else {}
            except (json.JSONDecodeError, TypeError):
                existing_trace = {"raw": existing_trace_raw}
            # Append downgrade record (preserves provenance — original trace.rule kept; new field added)
            existing_trace["wave_5_5_downgrade"] = {
                "rule": "d1c_excluded_scope_deferred_tier_a_post_phase_0c",
                "subtype_classified": c["subtype"],
                "subtype_classifier_rationale": c["rationale"],
                "previous_v1_scope": 1,
            }
            new_trace_raw = json.dumps(existing_trace, ensure_ascii=False)
            downgrade_updates.append((new_trace_raw, c["id"]))

        # Batch UPDATE v1_scope=0 + composition_trace
        cursor.executemany(
            "UPDATE weapon_knowledge_entries "
            "SET v1_scope = 0, v1_scope_composition_trace = ? "
            "WHERE id = ?",
            downgrade_updates,
        )
        conn.commit()

        # Empirical verification
        cursor.execute("SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1")
        post_v1_scope = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE quality_tier='A' AND weapon_kind_classified_subtype IS NULL"
        )
        post_null = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM weapon_knowledge_entries "
            "WHERE quality_tier='A' AND v1_scope=1 AND weapon_kind_classified_subtype IS NULL"
        )
        post_v1_scope_null = cursor.fetchone()[0]
        print()
        print(f"Post-Wave-5.5 Phase 0c:")
        print(f"  Tier-A NULL-subtype: {post_null} (expected 0; pre-state was {pre_null})")
        print(f"  Tier-A v1_scope=1 NULL-subtype: {post_v1_scope_null} (expected 0; pre-state was {pre_v1_scope_null})")
        print(f"  v1_scope total: {post_v1_scope} (expected {3042 - len(downgrade_candidates)} = {3042 - len(downgrade_candidates)})")

        # Distribution check by quality_tier
        cursor.execute(
            "SELECT quality_tier, COUNT(*) FROM weapon_knowledge_entries "
            "WHERE v1_scope=1 GROUP BY quality_tier ORDER BY 2 DESC"
        )
        print("  Per-tier v1_scope=1 distribution:")
        for tier, n in cursor.fetchall():
            print(f"    {tier}: {n}")

    finally:
        conn.close()

    # Emit JSON companion artifact
    out_json = OUT_DIR / "phase-0c-tier-a-subtype-classification.json"
    out_payload = {
        "phase": "cycle-10-wave-5-5-phase-0c",
        "date": "2026-05-25",
        "dispatch": (
            "agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-wave-5-5-"
            "phase-0c-and-mode-c-eviction.md"
        ),
        "authority_basis": (
            "gandalf SO-4 RATIFY-WITH-AMENDMENT (2026-05-25-so-1-2-4-sign-off-verdicts.md) + "
            "gandalf sign-off Condition 1 (2026-05-25-stage-3-distribution-report-sign-off.md § 3)"
        ),
        "pre_state": {
            "tier_a_null_subtype_total": pre_null,
            "tier_a_v1_scope_null_subtype": pre_v1_scope_null,
        },
        "classified_total": len(classified),
        "per_subtype_counts": dict(by_subtype.most_common()),
        "per_source_counts": dict(by_source.most_common()),
        "per_source_subtype_counts": {
            f"{src}|{sub}": cnt for (src, sub), cnt in by_source_subtype.most_common()
        },
        "v1_scope_downgrade_count": len(downgrade_candidates),
        "v1_scope_downgrade_per_subtype": dict(dg_by_subtype.most_common()),
        "post_state": {
            "tier_a_null_subtype_total": post_null,
            "tier_a_v1_scope_null_subtype": post_v1_scope_null,
            "v1_scope_total": post_v1_scope,
        },
        "rows": classified,
    }
    with out_json.open("w") as f:
        json.dump(out_payload, f, indent=2, ensure_ascii=False)
    print()
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
