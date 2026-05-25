#!/usr/bin/env python3
"""
populate_gap_fills.py — Stage 3.5 engine-authored gap-fill DB insertion

Authority: Dispatch 2026-05-25-rocket-cycle-10-stage-3-5-engine-authored-gap-fill.md
Composition policy: canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md § 9
Named-bearer discipline: canonical/story/skill-system-2026-05-24.md § 12.3 / § 12.4
Cultural-sensitivity: Q-B verdict § 3.2 (Tier 1/2 OK; NO Tier 3)
Provenance flag: source_library = 'engine_authored_gap_fill_v1' (LOAD-BEARING for Stage 3.6 + v1.1+ replacement)

Resource-bounds check (Discipline #1.1):
  - 43 entries × ~1-2 KB per row = ~50-80 KB DB writes
  - Transaction rollback on any per-entry validation failure

D7 AI-tell compliance: all description_text values authored via templated structure with narrow blanks;
  gandalf curation pass record documented in per-entry artifact under entries/ directory.

Naming-space partitioning per anchor (composition policy § 5.3 + dispatch § 4.2):
  - Cell 14 Pyromantic: pyromantic / pyromancy / flame-conjuring / ember-channeler / fire-affinity / pan-fantasy
  - Hattori Hanzō: ninja / shadow / clan / iga / koga / shinobi / hanzō-naming-family
  - Lu Bu: warlord / cavalry / halberd / red-hare / fang-tian-hua-ji / three-kingdoms
  - Moctezuma: tenochtitlan / aztec / quetzalcoatl-nested / serpent / jade / obsidian / macuahuitl / xiuhcoatl
  - Gilgamesh: uruk / enkidu / lion / cedar-forest / humbaba / ishtar / utnapishtim
  - Roland (GF-5*): paladin / durandal / olifant / charlemagne / carolingian / roncevaux / aude
  - Karna (GF-6*): kavacha / kundala / vijaya / vasavi-shakti / sun-hero / suryaputra / radheya

Sim-viability: all entries within engine BC envelope; no mechanically-novel patterns requiring engine extension.
Stage 4 mechanical-tagging fields (range_min/max, base_attack_speed, etc.) NOT populated here — Wave 7 owns Stage 4.
"""

import sqlite3
import json
import sys
import os

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
STAGE_3_5_SOURCE_LIBRARY = "engine_authored_gap_fill_v1"
STAGE_3_5_COMPOSITION_TRACE = json.dumps({"rule": "stage_3_5_gap_fill_authored", "dispatch": "2026-05-25-rocket-cycle-10-stage-3-5-engine-authored-gap-fill"})


def build_entry(
    canonical_name, description_text, structured_properties_dict,
    register_canonical, historical_period_canonical, cultural_lineage_canonical,
    weapon_kind, weapon_kind_classified_subtype,
    proxy_attribute_class, proxy_range_class, proxy_geometry_class, proxy_tempo_class,
    quality_tier,
    extracted_named_bearer, named_mythological_match,
    v1_scope_genre_filter
):
    """Build a gap-fill DB row dict. source_library and v1_scope are locked values."""
    return {
        "canonical_name": canonical_name,
        "source_library": STAGE_3_5_SOURCE_LIBRARY,
        "source_url": f"engine_authored://{canonical_name}",  # synthetic URL for UNIQUE constraint compliance
        "source_id": None,
        "description_text": description_text,
        "structured_properties": json.dumps(structured_properties_dict),
        "cultural_lineage_tags": json.dumps([cultural_lineage_canonical]),
        "historical_period": historical_period_canonical,
        "genre_appearances": json.dumps([v1_scope_genre_filter]),
        "related_entries": json.dumps([]),
        "license_class": "engine_authored",
        "register_canonical": register_canonical,
        "historical_period_canonical": historical_period_canonical,
        "cultural_lineage_canonical": cultural_lineage_canonical,
        "weapon_kind": weapon_kind,
        "weapon_kind_classified_subtype": weapon_kind_classified_subtype,
        "proxy_attribute_class": proxy_attribute_class,
        "proxy_range_class": proxy_range_class,
        "proxy_geometry_class": proxy_geometry_class,
        "proxy_tempo_class": proxy_tempo_class,
        "proxy_fingerprint_confidence": 1.0,  # engine-authored = full confidence
        "quality_tier": quality_tier,
        "extracted_named_bearer": extracted_named_bearer,
        "named_mythological_match": named_mythological_match,
        "cultural_lineage_confidence": 1.0,
        "wieldable_humanoid": "one_hand",  # default; Wave 7 may refine
        "v1_scope": 1,
        "v1_scope_composition_trace": STAGE_3_5_COMPOSITION_TRACE,
        "v1_scope_genre_filter": v1_scope_genre_filter,
        "dedup_status": "canonical",
        "template_quality_score": 1.0,
    }


# ============================================================
# ENTRY DEFINITIONS
# Per dispatch § 3.1 schema + per-entry artifacts in entries/
# Stage 4 mechanical-tagging fields (range_min/max etc.) deferred to Wave 7
# ============================================================

ENTRIES = [

    # --- CELL 14 PYROMANTIC CASTER (~5-10 entries; Pan-Fantasy; Tier A) ---
    # BC cell: (mid, low, spiky, INT) — composition policy § 4.1 + § 9.1

    build_entry(
        canonical_name="pyromantic_ember_staff",
        description_text="A channeling staff shaped from heat-fused obsidian glass, its core perpetually smoldering with contained pyromantic ember-energy. Wielded by practitioners of the mid-range fire-conjuring tradition, it delivers slow-cast bursts of concentrated flame across an area from safe conjuring distance.",
        structured_properties_dict={"type": "staff", "materials": ["obsidian", "iron"], "reach": "mid", "style": "pyromantic_conjuring"},
        register_canonical="fantasy",
        historical_period_canonical="fictional",
        cultural_lineage_canonical="fantasy_generic",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="INT",
        proxy_range_class="mid",
        proxy_geometry_class="AoE",
        proxy_tempo_class="low",
        quality_tier="A",
        extracted_named_bearer=None,
        named_mythological_match=None,
        v1_scope_genre_filter="fantasy",
    ),

    build_entry(
        canonical_name="pyromantic_cinder_focus",
        description_text="A compact hand-held conjuring focus carved from fire-tempered ceramic, etched with pyromantic channeling runes. The focus concentrates cinder-energy into single high-amplitude bolts rather than area bursts, suited to precision pyromancers who prefer focused delivery over wide coverage.",
        structured_properties_dict={"type": "focus", "materials": ["ceramic", "fire-tempered_clay"], "reach": "mid", "style": "concentrated_cinder"},
        register_canonical="fantasy",
        historical_period_canonical="fictional",
        cultural_lineage_canonical="fantasy_generic",
        weapon_kind="category",
        weapon_kind_classified_subtype="accessory_handheld",
        proxy_attribute_class="INT",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="A",
        extracted_named_bearer=None,
        named_mythological_match=None,
        v1_scope_genre_filter="fantasy",
    ),

    build_entry(
        canonical_name="pyromantic_flamecaller_rod",
        description_text="A slender conjuring rod forged from condensed fire-crystal lattice, humming with directed pyromantic potential. The flamecaller's rod channels its energy into a directed cone of fire rather than a radial burst, allowing pyromancers to sweep a killing angle at low tempo with high-amplitude flame output.",
        structured_properties_dict={"type": "rod", "materials": ["fire_crystal", "iron"], "reach": "mid", "style": "directed_cone_burst"},
        register_canonical="fantasy",
        historical_period_canonical="fictional",
        cultural_lineage_canonical="fantasy_generic",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="INT",
        proxy_range_class="mid",
        proxy_geometry_class="cone",
        proxy_tempo_class="low",
        quality_tier="A",
        extracted_named_bearer=None,
        named_mythological_match=None,
        v1_scope_genre_filter="fantasy",
    ),

    build_entry(
        canonical_name="pyromantic_ashbound_wand",
        description_text="A wand bound with compacted ash residue from a thousand previous pyromantic castings, its surface darkened with accumulated fire-memory. The ashbound wand scatters low-tempo ash-spark volleys in a wide dispersal pattern, trading single-target precision for multi-point ignition capability.",
        structured_properties_dict={"type": "wand", "materials": ["ashwood", "compacted_ash", "iron_core"], "reach": "mid", "style": "scatter_spark"},
        register_canonical="fantasy",
        historical_period_canonical="fictional",
        cultural_lineage_canonical="fantasy_generic",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="INT",
        proxy_range_class="mid",
        proxy_geometry_class="scatter",
        proxy_tempo_class="low",
        quality_tier="A",
        extracted_named_bearer=None,
        named_mythological_match=None,
        v1_scope_genre_filter="fantasy",
    ),

    build_entry(
        canonical_name="pyromantic_conflagration_tome",
        description_text="A tome bound in flame-treated dragonhide, its pages inscribed with the oldest known pyromantic formulations for mass conflagration. Held off-hand as a channeling amplifier, the conflagration tome broadens a pyromancer's INT-scaling fire bursts into wide-area catastrophic events at the cost of casting speed.",
        structured_properties_dict={"type": "tome", "materials": ["dragonhide", "vellum", "fire_ink"], "reach": "mid", "style": "area_conflagration"},
        register_canonical="fantasy",
        historical_period_canonical="fictional",
        cultural_lineage_canonical="fantasy_generic",
        weapon_kind="category",
        weapon_kind_classified_subtype="accessory_handheld",
        proxy_attribute_class="INT",
        proxy_range_class="mid",
        proxy_geometry_class="AoE",
        proxy_tempo_class="low",
        quality_tier="A",
        extracted_named_bearer=None,
        named_mythological_match=None,
        v1_scope_genre_filter="fantasy",
    ),

    # --- HATTORI HANZO (7 entries; east_asian japanese_folklore; Tier S; Tier 2 soft-attribution) ---
    # BC axes: DEX primary; mid/melee/ranged range; various geometry; high/low tempo
    # Named-bearer: Hattori Hanzō (engine-internal); player-facing: soft-attribution archetypal

    build_entry(
        canonical_name="hattori_hanzo_shadow_ninjato",
        description_text="A straight-bladed ninjato honed to a hair's edge by a master of the Iga shadow-blade tradition. Compact and unadorned, it is wielded with the speed and precision of a shadow in motion, delivering high-tempo single strikes that dispatch targets before they register the draw.",
        structured_properties_dict={"type": "ninjato", "materials": ["tamahagane_steel"], "length_cm": 50, "tradition": "iga_shinobi", "reach": "mid"},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="hattori_hanzo_iga_shuriken_brace",
        description_text="A brace of hand-forged Iga-tradition shuriken, each star-blade balanced for maximum flight stability and penetration at mid-range. The shinobi's deliberate throwing technique transforms the brace into a wide-scatter volley delivering simultaneous multi-point impacts on the target zone.",
        structured_properties_dict={"type": "shuriken_brace", "materials": ["folded_steel"], "count": 6, "tradition": "iga_shinobi", "throw_range": "mid"},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="mid",
        proxy_geometry_class="scatter",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="hattori_hanzo_shinobi_wakizashi",
        description_text="A wakizashi carried by elite Iga shinobi as the companion blade to their primary weapon. Its shorter length enables rapid cleaving strikes in tight environments where a full-length sword would be an encumbrance, delivering high-tempo cleave patterns that clear space and follow-through with lethal efficiency.",
        structured_properties_dict={"type": "wakizashi", "materials": ["tamahagane_steel"], "length_cm": 40, "tradition": "iga_shinobi", "blade_style": "companion"},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="mid",
        proxy_geometry_class="cleave",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="hattori_hanzo_koga_kusarigama",
        description_text="A Kōga-tradition kusarigama whose weighted chain is spun at high velocity to generate a multi-hit arc before the sickle-blade follows through. The weapon rewards the patient practitioner who can sustain its spinning rhythm, delivering high-tempo multi-hit strikes across a wide reach from mid-range.",
        structured_properties_dict={"type": "kusarigama", "materials": ["iron_chain", "iron_sickle", "lead_weight"], "tradition": "koga_shinobi", "chain_length_cm": 150},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="mid",
        proxy_geometry_class="multi-hit",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="hattori_hanzo_ninja_tanto",
        description_text="A ninja tantō ground to a needle point for penetrating armor at close quarters. In the hands of a trained Iga operative, the tantō becomes a rapid melee instrument of high-tempo single-point strikes that target the gaps in an enemy's defense before they can react.",
        structured_properties_dict={"type": "tanto", "materials": ["tamahagane_steel"], "length_cm": 25, "tradition": "iga_shinobi", "style": "close_quarters"},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="hattori_hanzo_clan_kunai",
        description_text="An Iga clan kunai, utility-blade and thrown weapon combined in a single iron instrument. Deployed with a deliberate, committed throw at mid-range, the kunai sacrifices frequency for precision and power, making each launched blade a concentrated impact event rather than a rapid volley.",
        structured_properties_dict={"type": "kunai", "materials": ["iron"], "length_cm": 20, "tradition": "iga_clan", "use": "throw_and_melee"},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="hattori_hanzo_shadow_bow",
        description_text="A compact shinobi hankyū, the half-bow carried by Iga operatives for rapid-draw ranged engagement. Shorter and faster than a formal ceremonial bow, the shadow bow enables high-tempo single-arrow delivery from concealment, placing aimed shots with precise DEX-scaling accuracy at range.",
        structured_properties_dict={"type": "hankyu", "materials": ["laminated_bamboo", "silk_string"], "draw_weight_kg": 18, "tradition": "iga_shinobi", "style": "rapid_draw"},
        register_canonical="historical",
        historical_period_canonical="early_modern",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="ranged",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Hattori Hanzō",
        named_mythological_match="Hattori Hanzō",
        v1_scope_genre_filter="historical",
    ),

    # --- LU BU (7 entries; east_asian chinese_three_kingdoms; Tier S; Tier 2 soft-attribution) ---
    # BC axes: STR primary; melee/mid; various geometry; low/medium tempo
    # D1c: mounted-combat excluded — all entries dismounted-polearm or sword/crossbow

    build_entry(
        canonical_name="lu_bu_fang_tian_hua_ji",
        description_text="The fang tian hua ji — a ji halberd with a crescent blade and flanking spear-tip — the weapon most associated with the legendary warlord of the northern borderlands in the Romance of the Three Kingdoms. Wielded on foot, its heavy crescent-arc cleave can sweep through formations with concentrated STR-scaled power.",
        structured_properties_dict={"type": "ji_halberd", "subtype": "fang_tian_hua_ji", "materials": ["iron", "hardwood_pole"], "length_cm": 210, "tradition": "chinese_three_kingdoms", "style": "dismounted_polearm"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="cleave",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="lu_bu_three_kingdoms_ji_poleaxe",
        description_text="A ji-type poleaxe of Eastern Han military manufacture, heavier than a standard infantry spear and fitted with a broad swept blade for formation combat. When wielded on foot by a warrior of exceptional strength, the ji poleaxe sweeps wide-arc AoE patterns that can disrupt enemy lines.",
        structured_properties_dict={"type": "ji_poleaxe", "materials": ["iron", "hardwood_pole"], "length_cm": 200, "tradition": "chinese_three_kingdoms", "style": "dismounted_formation"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="AoE",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="lu_bu_warlord_guandao",
        description_text="A guandao — the long-hafted Chinese pole-blade with a heavy crescent blade at its tip — employed by Three Kingdoms warlords for dismounted extended-reach combat. The guandao's STR-scaling cleave at mid-polearm range is the weapon's signature, its sweep carrying force enough to cut through multiple layers of protection.",
        structured_properties_dict={"type": "guandao", "materials": ["iron", "hardwood_pole"], "length_cm": 180, "tradition": "chinese_three_kingdoms", "style": "mid_reach_polearm"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="mid",
        proxy_geometry_class="cleave",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="lu_bu_three_kingdoms_heavy_mace",
        description_text="A cast-iron flanged mace of Three Kingdoms military issue, heavy enough that only warriors of extraordinary physical strength could wield it with consistent combat effectiveness. Its single concentrated blow pattern focuses all STR-scaling force into a single impact zone, shattering shields and bones alike.",
        structured_properties_dict={"type": "mace", "materials": ["cast_iron"], "weight_kg": 4.5, "tradition": "chinese_three_kingdoms", "style": "heavy_single_impact"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="lu_bu_cavalry_lance_dismounted",
        description_text="A cavalry lance of Three Kingdoms vanguard design, its long shaft adapted for dismounted close-combat use once the charge has closed to engagement range. The lance's extended reach delivers STR-scaled spiky thrust strikes at mid-range, with a faster cadence than the heavy halberd family.",
        structured_properties_dict={"type": "lance", "materials": ["hardwood", "iron_tip"], "length_cm": 250, "tradition": "chinese_three_kingdoms", "style": "dismounted_thrust"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="lu_bu_red_hare_iron_sword",
        description_text="A straight iron jian associated with the warlord whose renowned red stallion became as famous as his own name. Faster and more versatile than the heavy polearm, the iron sword delivers consistent flat STR-scaled strikes at medium tempo, the mark of a warrior trained in both mounted and dismounted combat disciplines.",
        structured_properties_dict={"type": "jian_sword", "materials": ["iron"], "length_cm": 80, "tradition": "chinese_three_kingdoms", "style": "versatile_straight_sword"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="lu_bu_northern_crossbow",
        description_text="A heavy siege crossbow of northern Han military manufacture, requiring exceptional upper-body strength to draw and effective against armored targets at range. The deliberate aimed bolt delivery achieves concentrated spiky impact at ranged distance, the domain of the powerful archer-warrior rather than the rapid skirmisher.",
        structured_properties_dict={"type": "crossbow", "subtype": "heavy_siege", "materials": ["hardwood", "iron", "sinew"], "draw_weight_kg": 80, "tradition": "chinese_three_kingdoms", "style": "str_ranged_bolt"},
        register_canonical="historical",
        historical_period_canonical="classical",
        cultural_lineage_canonical="east_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="ranged",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Lu Bu",
        named_mythological_match="Lu Bu",
        v1_scope_genre_filter="historical",
    ),

    # --- MOCTEZUMA (8 entries; mesoamerican; Tier S; Tier 2 soft-attribution + nested Quetzalcoatl / Tlaloc Tier 1) ---
    # BC axes: INT/WIS hybrid via Option C; melee/mid; various geometry; medium/low tempo

    build_entry(
        canonical_name="moctezuma_macuahuitl",
        description_text="The macuahuitl — a hardwood club edged with a row of obsidian blades — was the signature weapon of the Aztec warrior caste. In the hands of a tlatoani who ruled as both sovereign and high priest, the macuahuitl carries both martial and ritual weight, its cleaving strikes guided by a discipline that crosses the physical and the ceremonial.",
        structured_properties_dict={"type": "macuahuitl", "materials": ["hardwood", "obsidian"], "length_cm": 100, "tradition": "aztec_mexica", "style": "obsidian_edged_club"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="INT",
        proxy_range_class="melee",
        proxy_geometry_class="cleave",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Moctezuma",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="moctezuma_atlatl",
        description_text="The atlatl spearthrower extended the Aztec warrior's effective range far beyond the unaided arm. In ritual-military context, the tlatoani's atlatl is blessed before use, transforming each deliberate spear-throw into a committed single-target strike of considerable force — a moment of calculation, release, and consequence.",
        structured_properties_dict={"type": "atlatl", "materials": ["hardwood", "deer_bone_hook"], "tradition": "aztec_mexica", "style": "ritual_throw"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="INT",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Moctezuma",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="moctezuma_xiuhcoatl_staff",
        description_text="A ritual staff carved in the form of Xiuhcoatl, the Fire Serpent — divine weapon of the sun-deity and instrument of the heavenly fire that defines the Aztec cosmos. Wielded as a channeling implement, it focuses WIS-scaled ritual energy into area fire effects, the tlatoani calling on fire-serpent power to cleanse and consecrate the battlefield.",
        structured_properties_dict={"type": "ritual_staff", "deity_association": "Xiuhcoatl", "materials": ["jadite", "turquoise", "hardwood"], "tradition": "aztec_mexica", "style": "fire_serpent_ritual"},
        register_canonical="mythological",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="WIS",
        proxy_range_class="mid",
        proxy_geometry_class="AoE",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Xiuhcoatl",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="moctezuma_obsidian_blade_knife",
        description_text="The tecpatl — the sacred obsidian-bladed knife of Aztec ceremonial tradition — was also a high-precision close-combat instrument. In ritual-military context, its razor obsidian edge delivers rapid, exacting single-point strikes; the tlatoani's INT-scaled precision driving each stroke with deliberate purpose.",
        structured_properties_dict={"type": "tecpatl_knife", "materials": ["obsidian", "hardwood_handle"], "length_cm": 20, "tradition": "aztec_mexica", "style": "ritual_close_combat"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="INT",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Moctezuma",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="moctezuma_quetzalcoatl_serpent_staff",
        description_text="A staff of profound ritual authority bearing the coiling image of Quetzalcoatl, the Feathered Serpent who gave humankind the arts of civilization. When the tlatoani invokes this staff's WIS-scaled power, Quetzalcoatl's manifestation bursts across the field as a serpentine area force — slow in its preparation but devastating in its release.",
        structured_properties_dict={"type": "serpent_staff", "deity_association": "Quetzalcoatl", "materials": ["quetzal_feathers", "jade", "hardwood"], "tradition": "aztec_mexica", "style": "feathered_serpent_invocation"},
        register_canonical="mythological",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="WIS",
        proxy_range_class="mid",
        proxy_geometry_class="AoE",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Quetzalcoatl",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="moctezuma_jade_shield",
        description_text="The chimalli — the round shield of Aztec military distinction — decorated with jade mosaic work befitting the tlatoani's station. Worn as a defensive secondary implement in the off-hand, the jade chimalli pairs with the macuahuitl in the classic Aztec warrior-noble loadout, providing WIS-scaled ritual protection in the sovereign's battle-rite.",
        structured_properties_dict={"type": "chimalli_shield", "materials": ["hardwood", "jade_mosaic", "feather_trim"], "diameter_cm": 50, "tradition": "aztec_mexica", "style": "noble_ceremonial_shield"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="unique",
        weapon_kind_classified_subtype="armor_shield",
        proxy_attribute_class="WIS",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Moctezuma",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="moctezuma_tlaloc_rain_staff",
        description_text="A staff bearing the goggled visage of Tlaloc, the rain deity of the Aztec cosmology, whose dominion over water and fertility made him one of the two great deities enshrined at the Templo Mayor. When channeled by the tlatoani's WIS-scaled invocation, the staff delivers sustained variable-amplitude rain-force across a wide area, the unpredictable weight of the storm made manifest.",
        structured_properties_dict={"type": "rain_staff", "deity_association": "Tlaloc", "materials": ["turquoise_mosaic", "hardwood", "jade"], "tradition": "aztec_mexica", "style": "rain_deity_invocation"},
        register_canonical="mythological",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="WIS",
        proxy_range_class="mid",
        proxy_geometry_class="AoE",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Tlaloc",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="moctezuma_aztec_war_club",
        description_text="The cuauhololli — the ball-ended hardwood war club of the Aztec warrior tradition — was a battlefield instrument of raw physical authority. Its concentrated single-blow pattern, driven by STR scaling, was a favored weapon of the Eagle Warriors who served as the tlatoani's elite fighting force.",
        structured_properties_dict={"type": "cuauhololli_club", "materials": ["hardwood", "stone_ball"], "weight_kg": 2.5, "tradition": "aztec_mexica", "style": "eagle_warrior_heavy_strike"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="mesoamerican",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Moctezuma",
        named_mythological_match="Moctezuma",
        v1_scope_genre_filter="historical",
    ),

    # --- GILGAMESH (7 entries; sumerian middle_eastern; Tier S; Tier 1 broadly-fictionalized) ---
    # BC axes: STR primary; melee/mid/ranged; various geometry; low/medium/high tempo

    build_entry(
        canonical_name="gilgamesh_sword_of_uruk",
        description_text="The bronze sword of the King of Uruk — two-thirds divine, one-third mortal — whose blade has never been turned aside in the legends of the great city between the Two Rivers. It is wielded with the certainty of a man who has tested himself against lions, cedar forests, and the gods themselves.",
        structured_properties_dict={"type": "bronze_sword", "materials": ["bronze", "cedar_handle"], "length_cm": 75, "tradition": "sumerian_mesopotamian", "style": "king_hero_blade"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="gilgamesh_enkidu_axe",
        description_text="An axe forged in the tradition of Enkidu — the wild man created by the gods who became Gilgamesh's truest companion and equal in strength. Swifter in cleaving arcs than the king's own deliberate sword, Enkidu's axe strikes at medium tempo with consistent flat STR output, the weapon of a warrior who learned combat in the wilderness rather than the palace.",
        structured_properties_dict={"type": "bronze_axe", "materials": ["bronze", "hardwood_handle"], "length_cm": 70, "tradition": "sumerian_mesopotamian", "style": "companion_cleave"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="cleave",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="gilgamesh_cedar_forest_spear",
        description_text="A spear cut from the great cedar trees of the Forest where Humbaba dwelt — trophy of the quest that proved Gilgamesh's heroic worth. At mid-range, the cedar-shafted spear delivers STR-scaled thrusts with focused force, the weapon of a king who chose to seek glory in the wild places rather than rest behind his city's walls.",
        structured_properties_dict={"type": "spear", "materials": ["cedar_shaft", "bronze_tip"], "length_cm": 200, "tradition": "sumerian_mesopotamian", "style": "cedar_quest_trophy"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="gilgamesh_lion_skin_mace",
        description_text="A bronze mace said to have been wielded against the lions of the Mesopotamian plain — the beasts that Gilgamesh hunted to demonstrate his dominion over the wild. Its sweeping AoE arc carries the weight of a king's STR, the killing weapon of a sovereign who wore the lion's skin as proof of what he had overcome.",
        structured_properties_dict={"type": "bronze_mace", "materials": ["bronze", "cedar_handle"], "weight_kg": 3.5, "tradition": "sumerian_mesopotamian", "style": "lion_slayer_sweep"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="AoE",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="gilgamesh_ishtar_bow",
        description_text="A bow drawn against the Bull of Heaven sent by the goddess Ishtar in her fury at Gilgamesh's rejection — his skill at range the equal of his strength in melee. The Ishtar's Rebuke bow delivers high-tempo single arrows with steady DEX precision, the ranged expression of the king's all-encompassing martial dominance.",
        structured_properties_dict={"type": "composite_bow", "materials": ["horn", "sinew", "wood"], "tradition": "sumerian_mesopotamian", "style": "divine_defiance_range"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="ranged",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="gilgamesh_humbaba_war_axe",
        description_text="An axe of conquest forged in remembrance of Humbaba — the terrible cedar-forest guardian whose severed head proved that even the gods' appointed sentinels could fall to a king with the will to challenge them. The Humbaba conquest axe delivers high-tempo flat cleave with the relentless energy of a warrior who will not be turned aside.",
        structured_properties_dict={"type": "war_axe", "materials": ["bronze", "hardwood"], "length_cm": 80, "tradition": "sumerian_mesopotamian", "style": "conquest_cleave"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="cleave",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="gilgamesh_utnapishtim_staff",
        description_text="A staff shaped from the rare cedar of the Waters of Death — the crossing-point on the journey to Utnapishtim, the one man who survived the great flood and was granted eternal life. Wielded as a WIS-channeled instrument, it delivers variable-amplitude area effects that echo the tidal uncertainty of the immortal's crossing: unpredictable, wide-reaching, and impossible to prepare for.",
        structured_properties_dict={"type": "cedar_staff", "materials": ["cedar", "lapis_lazuli_inlay"], "tradition": "sumerian_mesopotamian", "style": "immortality_quest_wisdom"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="middle_eastern",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="WIS",
        proxy_range_class="mid",
        proxy_geometry_class="AoE",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Gilgamesh",
        named_mythological_match="Gilgamesh",
        v1_scope_genre_filter="mythological",
    ),

    # --- ROLAND GF-5* (4 entries; european_medieval Carolingian; Tier S; Tier 1 broadly-fictionalized) ---
    # BC axes: STR primary; melee/mid/secondary; various geometry; low/medium tempo

    build_entry(
        canonical_name="roland_durandal",
        description_text="Durandal — the sword that could not be broken, given to Roland, the greatest paladin of Charlemagne's court. Its blade has been tested against armies and stone alike and remained unshattered; in the hands of the paladin for whom it was forged, it delivers concentrated STR-scaled strikes with the certainty of a weapon that cannot fail.",
        structured_properties_dict={"type": "longsword", "name": "Durandal", "materials": ["legendary_steel"], "tradition": "carolingian_french", "style": "indestructible_paladin_blade"},
        register_canonical="mythological",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="european",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Charlemagne; Roland",
        named_mythological_match="Roland",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="roland_olifant_horn",
        description_text="The Olifant — Roland's ivory horn, whose blast at Roncevaux was heard thirty leagues away, too late to save him but enough to seal his legend. Held in the off-hand as a WIS-scaling ritual instrument, the horn's blast delivers an AoE area effect of rallying force, the sound carrying across the entire engagement at a single committed blow.",
        structured_properties_dict={"type": "ivory_horn", "name": "Olifant", "materials": ["ivory"], "tradition": "carolingian_french", "style": "paladin_rally_horn"},
        register_canonical="mythological",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="european",
        weapon_kind="unique",
        weapon_kind_classified_subtype="accessory_handheld",
        proxy_attribute_class="WIS",
        proxy_range_class="ranged",
        proxy_geometry_class="AoE",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Charlemagne; Roland",
        named_mythological_match="Roland",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="roland_carolingian_lance",
        description_text="The lance carried by the paladins of Charlemagne's guard — long-shafted and iron-tipped, designed for the shock of the charge but equally deadly in the hands of a dismounted champion who uses its reach to deliver STR-scaled thrusts at medium tempo from mid-range.",
        structured_properties_dict={"type": "lance", "materials": ["ash_shaft", "iron_tip"], "length_cm": 350, "tradition": "carolingian_french", "style": "paladin_dismounted_thrust"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="european",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Charlemagne; Roland",
        named_mythological_match="Roland",
        v1_scope_genre_filter="historical",
    ),

    build_entry(
        canonical_name="roland_charlemagne_shield",
        description_text="A kite shield bearing the heraldry of Charlemagne's paladin household — the emperor's champion identified at a glance on any field of battle. Carried off-hand alongside Durandal in the canonical paladin loadout, the shield provides STR-scaling melee defense and completes the full arms of the knight who stood alone at Roncevaux.",
        structured_properties_dict={"type": "kite_shield", "materials": ["iron", "wood", "leather_facing"], "tradition": "carolingian_french", "style": "paladin_champion_shield"},
        register_canonical="historical",
        historical_period_canonical="medieval",
        cultural_lineage_canonical="european",
        weapon_kind="unique",
        weapon_kind_classified_subtype="armor_shield",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Charlemagne; Roland",
        named_mythological_match="Roland",
        v1_scope_genre_filter="historical",
    ),

    # --- KARNA GF-6* (5 entries; south_asian Vedic/Hindu Mahabharata; Tier S; Tier 1 + heightened curation) ---
    # BC axes: STR/DEX hybrid; ranged/melee/mid; various geometry; high/low/medium tempo
    # Heightened curation: epic-literary framing; no sacred-religious conflation; no Tier 3 leak

    build_entry(
        canonical_name="karna_vijaya_bow",
        description_text="Vijaya — the divine bow once held by Indra himself, given to the sun-hero Karna as recognition of his supreme archery. In the Mahabharata's account of the Kurukshetra war, no warrior on either side could match the speed and precision of Karna's release with Vijaya, delivering high-tempo single arrows with the steady accuracy of a master who has trained since birth.",
        structured_properties_dict={"type": "divine_bow", "name": "Vijaya", "materials": ["divine_material"], "tradition": "mahabharata_vedic", "style": "sun_hero_archery"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="south_asian",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="DEX",
        proxy_range_class="ranged",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Karna",
        named_mythological_match="Karna",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="karna_vasavi_shakti_spear",
        description_text="The Vasavi Shakti — the divine lightning-spear granted by Indra to Karna in exchange for his celestial armor — a weapon of ultimate force that can be used only once. In the Mahabharata's Kurukshetra account, its single release decides a life. The spear is wielded with the full commitment of a warrior who has chosen this moment above all others: slow in preparation, devastating in delivery.",
        structured_properties_dict={"type": "divine_spear", "name": "Vasavi Shakti", "materials": ["divine_lightning"], "tradition": "mahabharata_vedic", "style": "ultimate_throw", "use_constraint": "single_decisive"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="south_asian",
        weapon_kind="unique",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="low",
        quality_tier="S",
        extracted_named_bearer="Karna",
        named_mythological_match="Karna",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="karna_kavacha_armor",
        description_text="The kavacha — the celestial armor that Karna wore as his divine birthright, bestowed by his father the sun-deity Surya at the moment of his birth. In the Mahabharata's account, giving it away was the act that defined his fate and sealed his status as a figure of heroic tragedy. As a secondary armor item, the kavacha represents the full defensive inheritance of the sun-hero's lineage.",
        structured_properties_dict={"type": "celestial_armor", "name": "kavacha", "materials": ["divine_material"], "tradition": "mahabharata_vedic", "style": "divine_birthright_defense"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="south_asian",
        weapon_kind="unique",
        weapon_kind_classified_subtype="accessory_handheld",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Karna",
        named_mythological_match="Karna",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="karna_surya_sun_sword",
        description_text="A sword of solar heritage carried by the suryaputra — the son of Surya — whose divine lineage manifested in his bearing and his skill from the moment of his birth. The blade delivers high-tempo flat STR strikes with the steady brilliance of the sun: reliable, constant, unwavering — a different character than the spear's ultimate commitment.",
        structured_properties_dict={"type": "straight_sword", "materials": ["solar_forged_steel"], "tradition": "mahabharata_vedic", "style": "suryaputra_warrior_blade"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="south_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="melee",
        proxy_geometry_class="single",
        proxy_tempo_class="high",
        quality_tier="S",
        extracted_named_bearer="Karna",
        named_mythological_match="Karna",
        v1_scope_genre_filter="mythological",
    ),

    build_entry(
        canonical_name="karna_mahabharata_chariot_lance",
        description_text="A lance of the Kurukshetra battlefield tradition — the weapon of a chariot-archer who could be equally devastating in close combat when engagement closed to the range of the pole. Wielded on foot by a warrior of Karna's ability, it delivers STR-scaled mid-range thrusts at medium tempo, the sharp end of the sun-hero's adaptable martial range.",
        structured_properties_dict={"type": "chariot_lance", "materials": ["hardwood_shaft", "iron_tip"], "length_cm": 240, "tradition": "mahabharata_vedic", "style": "dismounted_warrior_thrust"},
        register_canonical="mythological",
        historical_period_canonical="pre_classical",
        cultural_lineage_canonical="south_asian",
        weapon_kind="category",
        weapon_kind_classified_subtype="handheld_weapon",
        proxy_attribute_class="STR",
        proxy_range_class="mid",
        proxy_geometry_class="single",
        proxy_tempo_class="medium",
        quality_tier="S",
        extracted_named_bearer="Karna",
        named_mythological_match="Karna",
        v1_scope_genre_filter="mythological",
    ),
]


def validate_entry(entry):
    """Validate required fields before insert."""
    required = ["canonical_name", "source_library", "source_url", "description_text",
                 "register_canonical", "cultural_lineage_canonical", "quality_tier",
                 "v1_scope", "v1_scope_composition_trace"]
    for field in required:
        if field not in entry or entry[field] is None or entry[field] == "":
            raise ValueError(f"Entry {entry.get('canonical_name', 'UNKNOWN')} missing required field: {field}")

    assert entry["source_library"] == STAGE_3_5_SOURCE_LIBRARY, \
        f"source_library must be '{STAGE_3_5_SOURCE_LIBRARY}' for all gap-fill entries"
    assert entry["proxy_fingerprint_confidence"] == 1.0, \
        f"engine-authored entries must have proxy_fingerprint_confidence=1.0"
    assert entry["v1_scope"] == 1, \
        f"all gap-fill entries must have v1_scope=1"
    assert entry["quality_tier"] in ("S", "A"), \
        f"gap-fill quality_tier must be S or A, got {entry['quality_tier']}"
    assert entry["cultural_lineage_canonical"] not in (None, "", "unknown"), \
        f"cultural_lineage_canonical must be populated for all gap-fill entries"


def insert_entries(conn, entries):
    cur = conn.cursor()
    inserted = 0
    skipped = 0

    for entry in entries:
        validate_entry(entry)

        # Check for duplicate canonical_name within engine_authored_gap_fill_v1
        cur.execute("SELECT id FROM weapon_knowledge_entries WHERE source_library = ? AND canonical_name = ?",
                    (STAGE_3_5_SOURCE_LIBRARY, entry["canonical_name"]))
        if cur.fetchone():
            print(f"  SKIP (already exists): {entry['canonical_name']}")
            skipped += 1
            continue

        # Build column list dynamically from entry keys
        cols = list(entry.keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_list = ", ".join(cols)
        values = [entry[c] for c in cols]

        try:
            cur.execute(f"INSERT INTO weapon_knowledge_entries ({col_list}) VALUES ({placeholders})", values)
            print(f"  INSERT: {entry['canonical_name']} [{entry['quality_tier']} / {entry['cultural_lineage_canonical']} / {entry.get('proxy_attribute_class','?')}-{entry.get('proxy_range_class','?')}-{entry.get('proxy_tempo_class','?')}]")
            inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"  ERROR (IntegrityError): {entry['canonical_name']} — {e}")
            conn.rollback()
            raise

    return inserted, skipped


def post_population_assertions(conn):
    """Run post-smoke SQL assertions per dispatch § 8."""
    cur = conn.cursor()
    print("\n--- Post-population smoke assertions ---")

    cur.execute("SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library = ?", (STAGE_3_5_SOURCE_LIBRARY,))
    count = cur.fetchone()[0]
    print(f"  Total gap-fill entries: {count} (expected 30-60)")
    assert 30 <= count <= 60, f"Count {count} outside expected range 30-60"

    cur.execute("""SELECT COUNT(*) FROM weapon_knowledge_entries
                   WHERE source_library = ? AND v1_scope = 1 AND quality_tier IN ('S', 'A')""",
                (STAGE_3_5_SOURCE_LIBRARY,))
    tier_count = cur.fetchone()[0]
    print(f"  Tier S/A with v1_scope=1: {tier_count} (should equal total {count})")
    assert tier_count == count, "All gap-fill entries must be Tier S or A with v1_scope=1"

    cur.execute("""SELECT COUNT(*) FROM weapon_knowledge_entries
                   WHERE source_library = ? AND (cultural_lineage_canonical IS NULL OR cultural_lineage_canonical = '')""",
                (STAGE_3_5_SOURCE_LIBRARY,))
    null_lineage = cur.fetchone()[0]
    print(f"  NULL cultural_lineage_canonical: {null_lineage} (must be 0)")
    assert null_lineage == 0, "All gap-fill entries must have cultural_lineage_canonical populated"

    print("  All assertions PASS")


def main():
    print(f"Stage 3.5 gap-fill insertion — {len(ENTRIES)} entries")
    print(f"DB: {DB_PATH}")
    print(f"source_library: {STAGE_3_5_SOURCE_LIBRARY}\n")

    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("BEGIN TRANSACTION")
        inserted, skipped = insert_entries(conn, ENTRIES)
        print(f"\nInsertion complete: {inserted} inserted, {skipped} skipped")
        post_population_assertions(conn)
        conn.commit()
        print(f"\nCommit successful. {inserted} new rows in weapon_knowledge_entries.")
    except Exception as e:
        conn.rollback()
        print(f"\nROLLBACK — error: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
