#!/usr/bin/env python3
"""
Ingest substrate enrichment bundle 2026-05-27 — INT-AoE + Monk + Hybrid sub-fixes.

Source: legolas Mode B catalogue crawl completion notes (2026-05-27)
- 75 INT-AoE rows from agentic_orchestration/elrond/notes/2026-05-27-substrate-enrichment-int-aoe-completion.md
- 61 Monk (WIS-melee-light) rows
- 70 Hybrid (cross-attribute) rows
Total: 206 rows

Curation authority: elrond (data steward) per dispatch
2026-05-27-substrate-enrichment-bundle-int-aoe-monk-hybrid.md
Edge-case resolutions (E1/E2/E3): elrond within-data-domain steward authority.
2 holy-fire crusader rows flagged for Cycle 15 Path A discriminator.

LUT patterns derived from existing v1_scope substrate inspection:
- INT-caster-arcane: range 5-18, base_atk_spd 1.5, amp 0.84/2.4, base_phys_dmg_l50 50.22
- WIS-caster-faith melee: range 0.5-2.5, base_atk_spd 1.5, amp 0.84/2.4, base_phys_dmg_l50 50.22
- Hybrid: per primary_stat archetype; secondary_stat set; OMEGA_CROSS_ATTRIBUTE_PENALTY=0.80 applies at evaluation

ADDITIVE INSERT only; no schema extension (Q-Enrich-3 resolved: secondary_stat column
already exists). Backup pre-fire at telemetry.db.pre-substrate-enrichment-2026-05-27.bak.

This is a tool script, not production code. Lives under elrond research/scripts/.
"""

import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
SOURCE_LIBRARY = "legolas_crawl_substrate_enrichment_v1_2026_05_27"
DISPATCH_TAG = "2026-05-27-substrate-enrichment-bundle-int-aoe-monk-hybrid"


def _slugify(name: str) -> str:
    s = name.lower()
    for ch in [" ", "-", "/", "(", ")", "'", "+", ",", "."]:
        s = s.replace(ch, "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def make_composition_trace(
    sub_fix: str,
    tier: str,
    weapon_kind_subtype: str | None,
    option_c_eligible: bool = False,
    cycle_15_path_a_candidate: bool = False,
    notes: str | None = None,
) -> str:
    trace = {
        "rule": f"substrate_enrichment_{sub_fix}",
        "tier": tier,
        "dispatch": DISPATCH_TAG,
        "matching_policy": "substrate_enrichment_2026_05_27",
        "weapon_kind_classified_subtype": weapon_kind_subtype,
        "filter_passes": ["genre_pass", "weapon_kind_gate"],
    }
    if option_c_eligible:
        trace["option_c_eligible"] = True
        trace["omega_cross_attribute_penalty"] = 0.80
    if cycle_15_path_a_candidate:
        trace["cycle_15_path_a_discriminator_candidate"] = True
        trace["cycle_15_path_a_note"] = "holy-fire crusader STR+WIS faith-AoE radiance; Interpretation III alignment"
    if notes:
        trace["elrond_curation_notes"] = notes
    return json.dumps(trace)


# ----------------------------------------------------------------------------
# Sub-Fix 1 — INT-AoE — 75 rows
# ----------------------------------------------------------------------------
# Schema: (canonical_name, element, geometry, tempo, range_class, lineage,
#          register, period, source_ref_brief, weapon_kind, subtype, tier)
# All rows: primary_stat=INT, weapon_type_family=caster-arcane,
#           proxy_geometry_class=AoE, proxy_attribute_class=INT

INT_AOE_ROWS = [
    # § 2.1 D&D / Fantasy TTRPG (16 rows)
    ("Fireball Tome", "fire", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e Evocation", "named_template", "accessory_handheld", "A"),
    ("Evocation Spellbook", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e Evocation school", "category", "accessory_handheld", "A"),
    ("Wand of Fireballs", "fire", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.210", "named_template", "handheld_weapon", "A"),
    ("Staff of the Magi", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.202", "named_template", "handheld_weapon", "S"),
    ("Staff of Fire", "fire", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.201", "named_template", "handheld_weapon", "A"),
    ("Staff of Frost", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.201", "named_template", "handheld_weapon", "A"),
    ("Staff of Thunder and Lightning", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.203", "named_template", "handheld_weapon", "A"),
    ("Rod of Absorption", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.195", "named_template", "handheld_weapon", "A"),
    ("Wand of Lightning Bolts", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.211", "named_template", "handheld_weapon", "A"),
    ("Wand of Chain Lightning", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e PHB chain lightning", "named_template", "handheld_weapon", "A"),
    ("Orb of Dragonkind", "fire", "AoE", "low", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.225", "named_template", "accessory_handheld", "A"),
    ("Orb of the Magi", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D generic arcane focus", "category", "accessory_handheld", "A"),
    ("Necklace of Fireballs", "fire", "AoE", "high", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.182", "named_template", "accessory_handheld", "A"),
    ("Meteor Swarm Tome", "fire", "AoE", "low", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e PHB p.261", "named_template", "accessory_handheld", "A"),
    ("Wand of the War Mage +3", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "D&D 5e DMG p.212", "named_template", "handheld_weapon", "A"),
    ("Arcane Grimoire", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e Tasha's Cauldron", "category", "accessory_handheld", "A"),
    # § 2.2 Elemental orbs and focus implements (7 rows)
    ("Pyromantic Orb", "fire", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon (PoE-inspired)", "category", "accessory_handheld", "A"),
    ("Glacial Orb", "ice", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    ("Thunderstone Orb", "lightning", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    ("Conflagration Orb", "fire", "AoE", "low", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    ("Voidfire Orb", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    ("Stormcaller's Orb", "lightning", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    ("Crystal Resonance Sphere", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    # § 2.3 AoE staves (11 rows)
    ("Elemental Devastation Staff", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Inferno Staff", "fire", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon (ARPG tradition)", "category", "handheld_weapon", "A"),
    ("Blizzard Staff", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Storm Herald Staff", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Gale Force Staff", "wind", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon (rare wind-arcane)", "category", "handheld_weapon", "A"),
    ("Pyroclastic Staff", "fire", "AoE", "low", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Chain Conductor Staff", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Frost Nova Staff", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Diablo II / genre canon", "category", "handheld_weapon", "A"),
    ("Meteor Staff", "fire", "AoE", "low", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Arcane Surge Staff", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Twister Staff", "wind", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    # § 2.4 Lightning rod implements (6 rows)
    ("Thundercaller's Rod", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon + lightning rod tradition", "category", "handheld_weapon", "A"),
    ("Arc Lightning Rod", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Ball Lightning Rod", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Static Accumulator Rod", "lightning", "AoE", "low", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Indra's Rod", "lightning", "AoE", "medium", "mid", "south_asian", "mythological", "pre_classical", "Vedic Indrastra (Wikipedia)", "named_template", "handheld_weapon", "S"),
    ("Indrastra Conductor", "lightning", "AoE", "medium", "mid", "south_asian", "mythological", "pre_classical", "Vedic Astra tradition (Wikipedia)", "named_template", "handheld_weapon", "A"),
    # § 2.5 Chain lightning implements (5 rows)
    ("Chain Lightning Tome", "lightning", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D Chain Lightning spell", "named_template", "accessory_handheld", "A"),
    ("Forking Lightning Wand", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon (PoE Fork/Chain)", "category", "handheld_weapon", "A"),
    ("Cascade Orb", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon (PoE Spell Cascade)", "category", "accessory_handheld", "A"),
    ("Storm Orb of Branching", "lightning", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    ("Mjolnir-Pattern Warhammer Rod", "lightning", "AoE", "low", "mid", "european", "mythological", "pre_classical", "Mjolnir Norse mythology (Wikipedia)", "named_template", "handheld_weapon", "S"),
    # § 2.6 Ice storm implements (5 rows)
    ("Ice Storm Tome", "ice", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "D&D 5e PHB p.252", "named_template", "accessory_handheld", "A"),
    ("Blizzard Orb", "ice", "AoE", "low", "ranged", "fantasy_generic", "fantasy", "fictional", "Final Fantasy Blizzaga tradition", "named_template", "accessory_handheld", "A"),
    ("Frost Cascade Staff", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Winter's Embrace Rod", "ice", "AoE", "low", "mid", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "handheld_weapon", "A"),
    ("Permafrost Orb", "ice", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "genre canon", "category", "accessory_handheld", "A"),
    # § 2.7 Mythological divine fire/storm AoE (7 rows)
    ("Agneyastra Focus", "fire", "AoE", "medium", "ranged", "south_asian", "mythological", "pre_classical", "Vedic Astra tradition (Wikipedia)", "named_template", "accessory_handheld", "S"),
    ("Pashupatastra Glyph-Staff", "arcane", "AoE", "low", "ranged", "south_asian", "mythological", "pre_classical", "Pashupatastra Vedic Astras", "named_template", "handheld_weapon", "S"),
    ("Brahmashirastra Tome", "arcane", "AoE", "low", "ranged", "south_asian", "mythological", "pre_classical", "Brahma's weapons Vedic Astras", "named_template", "accessory_handheld", "S"),
    ("Sudarshana Chakra Rod", "arcane", "AoE", "high", "ranged", "south_asian", "mythological", "pre_classical", "Sudarshana Chakra Vedic Astras", "named_template", "handheld_weapon", "S"),
    ("Vayavyastra Staff", "wind", "AoE", "medium", "mid", "south_asian", "mythological", "pre_classical", "Vedic Astras (Wikipedia)", "named_template", "handheld_weapon", "S"),
    ("Zeus's Thunderbolt Staff", "lightning", "AoE", "medium", "mid", "european", "mythological", "pre_classical", "Greek mythology", "named_template", "handheld_weapon", "S"),
    ("Thor's Lightning Orb", "lightning", "AoE", "medium", "ranged", "european", "mythological", "pre_classical", "Norse mythology (Wikipedia)", "named_template", "accessory_handheld", "S"),
    # § 2.8 PoE elemental arcane implements (8 rows)
    ("Spell Cascade Sceptre", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    ("Arc Staff", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    ("Ball Lightning Wand", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    ("Firestorm Staff", "fire", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    ("Ice Nova Sceptre", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    ("Glacial Cascade Staff", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    ("Bladefall Tome", "arcane", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "named_template", "accessory_handheld", "A"),
    ("Pyroclasm Wand", "fire", "AoE", "high", "mid", "fantasy_generic", "fantasy", "fictional", "Path of Exile genre canon", "category", "handheld_weapon", "A"),
    # § 2.9 Final Fantasy / Anime (10 rows)
    ("Black Magic Staff (Flare)", "arcane", "AoE", "low", "mid", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "handheld_weapon", "A"),
    ("Blizzaga Staff", "ice", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "handheld_weapon", "A"),
    ("Thundaga Staff", "lightning", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "handheld_weapon", "A"),
    ("Firaga Tome", "fire", "AoE", "medium", "ranged", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "accessory_handheld", "A"),
    ("Meteor Tome (FF)", "fire", "AoE", "low", "ranged", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "accessory_handheld", "A"),
    ("Ultima Orb", "arcane", "AoE", "low", "ranged", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "accessory_handheld", "S"),
    ("Comet Staff", "arcane", "AoE", "low", "mid", "fantasy_generic", "fantasy", "fictional", "Final Fantasy series", "named_template", "handheld_weapon", "A"),
    ("Ryuko Matoi Scissor Blade", "arcane", "AoE", "high", "mid", "fantasy_generic", "fantasy", "fictional", "Anime canon", "named_template", "handheld_weapon", "A"),
    ("Madou Sceptre", "arcane", "AoE", "medium", "mid", "fantasy_generic", "fantasy", "fictional", "Anime magical-girl canon", "category", "handheld_weapon", "A"),
    ("Gungnir-Stave (Thunder)", "lightning", "AoE", "medium", "mid", "european", "mythological", "pre_classical", "Norse/Final Fantasy composite", "named_template", "handheld_weapon", "A"),
]
assert len(INT_AOE_ROWS) == 75, f"INT-AoE rows: expected 75, got {len(INT_AOE_ROWS)}"


# ----------------------------------------------------------------------------
# Sub-Fix 2 — Monk WIS-melee-light — 61 rows
# ----------------------------------------------------------------------------
# Schema: (canonical_name, lineage, period, register, geometry, range_class, tempo,
#          weapon_kind, subtype, source_ref_brief, tier, elrond_note)
# All rows: primary_stat=WIS, weapon_type_family=caster-faith,
#           proxy_attribute_class=WIS
# Edge cases:
#   E1 Shakujo → WIS-melee-light, register=historical (combat use primary)
#   E2 Trishula → caster-faith retained but classified here under monk-staff form
#                 (since legolas put it in monk crawl); proxy_geometry=cleave (three-pronged sweep)
#   E3 Drunken Monk Fist → WIS-melee-light, range=melee_close_or_grapple

MONK_ROWS = [
    # § 2.1 Unarmed implements (14 rows)
    ("Brass Knuckles", "european", "industrial", "historical", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Knuckle duster", "A", None),
    ("Iron Fist (knuckleduster)", "european", "industrial", "historical", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Knuckle duster", "A", None),
    ("Apache Revolver Knuckle", "european", "industrial", "historical", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Apache pistol", "A", None),
    ("Mark I Trench Knife", "european", "industrial", "historical", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia WWI trench knife", "A", None),
    ("Bagh Nakh (Tiger Claw)", "south_asian", "early_modern", "historical", "multi-hit", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Bagh nakh (Maratha)", "S", None),
    ("Vagh Nakhya (Shivaji's Tiger Claw)", "south_asian", "early_modern", "mythological", "multi-hit", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Maratha tradition; named bearer Shivaji", "S", None),
    ("Nihang Sikh Bagh Nakh", "south_asian", "early_modern", "historical", "multi-hit", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Nihang wrestling tradition", "A", None),
    ("Cestus (Caestus)", "european", "pre_classical", "historical", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Cestus Greek/Roman", "S", None),
    ("Tekko (Okinawan Fist-Load)", "east_asian", "early_modern", "historical", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Tekko Okinawan", "A", None),
    ("Tekkokagi (Claw-Hook Tekko)", "east_asian", "early_modern", "historical", "multi-hit", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Tekkokagi", "A", None),
    ("Emeici (Emei Piercer)", "east_asian", "classical", "historical", "multi-hit", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wikipedia Emeici Chinese", "A", None),
    ("Emei Dagger Pair", "east_asian", "contemporary", "historical", "multi-hit", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "Wushu competition emeici", "A", None),
    ("Knuckle Knife (Spiked Brass)", "european", "industrial", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Knuckleduster + blade variant", "A", None),
    ("Cuchillo de Paracaidista", "south_american_indigenous", "modern", "historical", "single", "melee_close_or_grapple", "medium", "named_template", "handheld_weapon", "Argentine paratroop knuckle-knife", "A", None),
    # § 2.2 Monk staves (12 rows)
    ("Bo Staff", "east_asian", "classical", "historical", "cleave", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Bo weapon Shaolin", "S", None),
    ("Shakujo (Buddhist Monk Staff)", "east_asian", "classical", "historical", "single", "mid", "medium", "named_template", "handheld_weapon", "E1 RESOLVED: WIS-melee-light (Shorinji Kempo combat tradition); divine secondary", "S", "edge_case_E1_resolved_WIS_melee_light"),
    ("Khakkhara (Pewter Staff)", "south_asian", "classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Khakkhara Sanskrit variant", "A", None),
    ("Jo Staff", "east_asian", "early_modern", "historical", "single", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Jo Musō Gonnosuke", "S", None),
    ("Hanbo (Half-Staff)", "east_asian", "early_modern", "historical", "single", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Hanbo three-foot", "A", None),
    ("Shaolin Gun (Monk Staff)", "east_asian", "classical", "historical", "cleave", "mid", "medium", "category", "handheld_weapon", "Wushu Shaolin gun", "A", None),
    ("Tin Staff (Sengchou's)", "east_asian", "classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Sengchou of Shaolin named-bearer", "A", None),
    ("Jōdō Staff", "east_asian", "early_modern", "historical", "single", "mid", "medium", "category", "handheld_weapon", "Jōjutsu training jo", "A", None),
    ("Aiki-Jo", "east_asian", "modern", "historical", "single", "mid", "medium", "category", "handheld_weapon", "Aikido jo staff", "A", None),
    ("Trishula Staff (Shiva)", "south_asian", "pre_classical", "mythological", "cleave", "mid", "medium", "named_template", "handheld_weapon", "E2 RESOLVED: WIS-caster-faith (Shiva's iconographic divine spear); kept in monk-staff form factor", "S", "edge_case_E2_resolved_caster_faith_divine_implement"),
    ("Ame-no-Nuboko (Jeweled Spear-Staff)", "east_asian", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Izanagi creation spear", "S", None),
    ("Nangun (Southern Monk Staff)", "east_asian", "classical", "historical", "single", "mid", "medium", "category", "handheld_weapon", "Wushu nangun southern form", "A", None),
    # § 2.3 Sash / chain / flexible (13 rows)
    ("Nunchaku", "east_asian", "early_modern", "historical", "multi-hit", "melee", "high", "named_template", "handheld_weapon", "Wikipedia Nunchaku Okinawan/Shaolin", "S", None),
    ("Nunchucks (Modern)", "east_asian", "contemporary", "historical", "multi-hit", "melee", "high", "category", "handheld_weapon", "Modern nunchaku variant", "A", None),
    ("Sansetsukon (Three-Section Staff)", "east_asian", "classical", "historical", "multi-hit", "mid", "high", "named_template", "handheld_weapon", "Wikipedia Sansetsukon Chinese", "S", None),
    ("Sanjiebian (Three-Section Whip)", "east_asian", "classical", "historical", "multi-hit", "mid", "high", "named_template", "handheld_weapon", "Three-section whip Chinese", "A", None),
    ("Kusari-fundo (Manrikigusari)", "east_asian", "early_modern", "historical", "single", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Kusari-fundo Edo police", "S", None),
    ("Manriki (Short Chain)", "east_asian", "early_modern", "historical", "single", "melee", "medium", "named_template", "handheld_weapon", "Compact kusari-fundo", "A", None),
    ("Kusarigama (Chain-Sickle)", "east_asian", "early_modern", "historical", "cleave", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Kusarigama kama+chain", "S", None),
    ("Kyoketsu Shoge", "east_asian", "early_modern", "historical", "single", "mid", "medium", "named_template", "handheld_weapon", "Hook-blade on cord", "A", None),
    ("Jiujiebian (Nine-Section Whip)", "east_asian", "classical", "historical", "multi-hit", "mid", "high", "named_template", "handheld_weapon", "Wikipedia Jiujiebian Jin Dynasty", "A", None),
    ("Qijiebian (Seven-Section Whip)", "east_asian", "classical", "historical", "multi-hit", "mid", "high", "named_template", "handheld_weapon", "Chain whip seven-section variant", "A", None),
    ("Rope Dart (Shengbiao)", "east_asian", "classical", "historical", "single", "ranged", "medium", "named_template", "handheld_weapon", "Wikipedia Rope dart meteor hammer cousin", "A", None),
    ("Meteor Hammer", "east_asian", "classical", "historical", "AoE", "mid", "medium", "named_template", "handheld_weapon", "Spinning AoE pattern", "A", None),
    ("Drunken Staff (Zui Gun)", "east_asian", "classical", "historical", "single", "mid", "medium", "named_template", "handheld_weapon", "Zui quan drunken bo Shaolin", "A", None),
    # § 2.4 Tonfa / sai / kama (10 rows)
    ("Tonfa (T-Baton)", "east_asian", "early_modern", "historical", "single", "melee", "medium", "named_template", "handheld_weapon", "Wikipedia Tonfa Okinawan", "S", None),
    ("Tuifa (Chinese Tonfa)", "east_asian", "early_modern", "historical", "single", "melee", "medium", "named_template", "handheld_weapon", "Chinese tonfa variant guǎi", "A", None),
    ("Tonfa Pair", "east_asian", "early_modern", "historical", "single", "melee", "medium", "category", "handheld_weapon", "Okinawan kobudō paired form", "A", None),
    ("PR-24 Side-Handle Baton", "east_asian", "modern", "historical", "single", "melee", "medium", "named_template", "handheld_weapon", "Modern law-enforcement tonfa", "A", None),
    ("Sai (Stabbing Trident)", "east_asian", "early_modern", "historical", "single", "melee", "high", "named_template", "handheld_weapon", "Wikipedia Sai Okinawan", "S", None),
    ("Manji Sai (Reversed-Prong)", "east_asian", "early_modern", "historical", "single", "melee", "high", "named_template", "handheld_weapon", "Sai variant reversed prong", "A", None),
    ("Nicho Sai (Paired Sai)", "east_asian", "early_modern", "historical", "multi-hit", "melee", "high", "category", "handheld_weapon", "Paired sai standard form", "A", None),
    ("Sancho Sai (Triple Sai)", "east_asian", "early_modern", "historical", "multi-hit", "melee", "high", "category", "handheld_weapon", "Three-sai configuration", "A", None),
    ("Kama (Sickle)", "east_asian", "medieval", "historical", "cleave", "melee", "medium", "named_template", "handheld_weapon", "Wikipedia Kama Okinawan", "S", None),
    ("Kama Pair", "east_asian", "medieval", "historical", "cleave", "melee", "medium", "category", "handheld_weapon", "Paired kama form", "A", None),
    # § 2.5 Martial arts tradition category (12 rows)
    ("Shaolin Unarmed Form (Luohan Quan)", "east_asian", "classical", "historical", "multi-hit", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Wikipedia Shaolin Kung Fu", "A", None),
    ("Shaolin 18 Luohan Quan", "east_asian", "classical", "historical", "multi-hit", "melee_close_or_grapple", "high", "category", "handheld_weapon", "18-move foundational form", "A", None),
    ("Muay Thai Elbow (Sok)", "southeast_asian", "early_modern", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Wikipedia Muay Thai sok strike", "A", None),
    ("Muay Thai Knee Strike", "southeast_asian", "early_modern", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Wikipedia Muay Thai knee", "A", None),
    ("Muay Thai Shin Conditioned", "southeast_asian", "early_modern", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Wikipedia Muay Thai shin", "A", None),
    ("Khat Chueak (Rope-Wrapped Hands)", "southeast_asian", "early_modern", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Pre-glove rope hand-wrapping", "A", None),
    ("Capoeira Chanfolo (Double Dagger)", "south_american_indigenous", "modern", "historical", "single", "melee", "medium", "named_template", "handheld_weapon", "Capoeira Mestre Bimba dagger", "A", None),
    ("Capoeira Razor (Gilette Razor)", "south_american_indigenous", "modern", "historical", "single", "melee", "high", "category", "handheld_weapon", "Capoeira straight razor", "A", None),
    ("Pankration Gloves (Greek)", "european", "pre_classical", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Greek pankration leather wrap", "A", None),
    ("Caestus Wrapped Fist", "european", "pre_classical", "historical", "single", "melee_close_or_grapple", "high", "category", "handheld_weapon", "Roman cestus leather variant", "A", None),
    ("Drunken Monk Fist (Zui Quan Open Hand)", "east_asian", "classical", "historical", "single", "melee_close_or_grapple", "medium", "category", "handheld_weapon", "E3 RESOLVED: WIS-melee-light (discipline + spirit-cultivation tradition)", "A", "edge_case_E3_resolved_WIS_melee_light"),
    ("Wushu Open Hand (Changquan)", "east_asian", "contemporary", "historical", "single", "melee_close_or_grapple", "medium", "category", "handheld_weapon", "Wushu changquan competition form", "A", None),
]
assert len(MONK_ROWS) == 61, f"Monk rows: expected 61, got {len(MONK_ROWS)}"


# ----------------------------------------------------------------------------
# Sub-Fix 3 — Hybrid cross-attribute — 70 rows
# ----------------------------------------------------------------------------
# Schema: (canonical_name, primary_stat, secondary_stat, element, lineage, period,
#          register, geometry, range_class, tempo, weapon_kind, subtype,
#          source_ref_brief, tier, holy_fire_crusader_flag)
# All rows: weapon_type_family=hybrid (NEW family value),
#           proxy_attribute_class=primary_stat
# Cross-attribute → Option C ω-penalty 0.80 eligible
# Holy-fire flagging: 2 rows (Order's Lance, Paladin's Holy Sword) → Cycle 15 Path A discriminator candidates

HYBRID_ROWS = [
    # § 2.1 Spellblades / magus-arcane-blades (10 rows)
    ("Eldritch Knight's Longsword", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "D&D 5e Fighter EK", "A", False),
    ("Bladesinger Rapier", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "high", "named_template", "handheld_weapon", "D&D 5e Wizard Bladesinger", "A", False),
    ("Hexblade's Pact Blade", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "D&D 5e Warlock Hexblade", "A", False),
    ("Magus Spellblade", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "Pathfinder Magus Spellstrike", "S", False),
    ("Arcane Blade (generic)", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "D&D / genre canon", "A", False),
    ("Runeblade", "INT", "STR", "arcane", "european", "early_modern", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Norse/Germanic runecraft", "S", False),
    ("Sigil Sword", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Spell-Forged Shortsword", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Dueling Spellsword", "INT", "DEX", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "high", "category", "handheld_weapon", "genre canon", "A", False),
    ("Blood Hexblade", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "D&D Hexblade life-drain", "A", False),
    # § 2.2 Runeblades / rune-inscribed (10 rows)
    ("Runic Greatsword", "STR", "INT", "arcane", "european", "early_modern", "mythological", "cleave", "melee", "medium", "category", "handheld_weapon", "Norse runic tradition", "A", False),
    ("Rune Axe", "STR", "INT", "arcane", "european", "early_modern", "mythological", "cleave", "melee", "medium", "category", "handheld_weapon", "Norse runic tradition", "A", False),
    ("Gram (Sigurd's Runeblade)", "STR", "INT", "arcane", "european", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Völsunga saga Wikipedia", "S", False),
    ("Rune Staff (Seidr)", "WIS", "INT", "arcane", "european", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Norse seidr tradition", "S", False),
    ("Galdrbok Staff", "INT", "WIS", "arcane", "european", "early_modern", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Galdrabók grimoire Wikipedia", "A", False),
    ("Runic Focus Wand", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "mid", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Death Knight's Runeblade", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "named_template", "handheld_weapon", "WoW Death Knight tradition", "S", False),
    ("Frostmourne (Runeblade archetype)", "STR", "INT", "ice", "fantasy_generic", "fictional", "fantasy", "AoE", "melee", "medium", "named_template", "handheld_weapon", "WoW genre canon", "S", False),
    ("Rune-Forged Dagger", "DEX", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "high", "category", "handheld_weapon", "genre canon", "A", False),
    ("Runed Spellsword", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    # § 2.3 Rune-staves (7 rows)
    ("Seidr Rune Staff", "WIS", "INT", "arcane", "european", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Norse seidr volva tradition", "S", False),
    ("Galdr Staff", "INT", "WIS", "arcane", "european", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Norse galdr song-magic", "A", False),
    ("Druidic Runestaff", "WIS", "INT", "arcane", "european", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Celtic druidic ogham", "A", False),
    ("Runic Arcane Staff", "INT", "WIS", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "mid", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Elder Wand (Rune Wand)", "INT", "WIS", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "mid", "medium", "named_template", "handheld_weapon", "Wand tradition Wikipedia", "S", False),
    ("Caduceus (Hermes Wand)", "INT", "WIS", "arcane", "european", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Greek mythology Hermes", "S", False),
    ("Barsom (Zoroastrian Bundle)", "WIS", "INT", "arcane", "middle_eastern", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Zoroastrian tradition Wikipedia", "A", False),
    # § 2.4 Holy paladin-knight (11 rows) — STR+WIS holy-faith hybrid
    ("Holy Avenger Sword", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "D&D 5e DMG p.174", "S", False),
    ("Durendal (Paladin Sword)", "STR", "WIS", "holy", "european", "medieval", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Chanson de Roland", "S", False),
    ("Excalibur (Sovereign Blade)", "STR", "WIS", "holy", "european", "medieval", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Arthurian tradition", "S", False),
    ("Holy Lance (Spear of Longinus)", "STR", "WIS", "holy", "european", "classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Wikipedia Holy Lance", "S", False),
    ("Paladin's Mace of Devotion", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "D&D Paladin tradition", "A", False),
    ("Shield-Sword Crusader Combo", "STR", "WIS", "holy", "european", "medieval", "historical", "single", "melee", "medium", "category", "handheld_weapon", "Christian Crusader tradition", "A", False),
    ("Divine Sentinel Blade", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "D&D 5e Paladin Devotion", "A", False),
    ("Aasimar's Radiant Sword", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "AoE", "melee", "medium", "named_template", "handheld_weapon", "D&D 5e Aasimar heritage", "A", False),
    ("Paladin's Warhammer of Faith", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Order's Lance (FFXIV Paladin)", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "AoE", "mid", "medium", "named_template", "handheld_weapon", "FFXIV Paladin job", "S", True),  # HOLY-FIRE CRUSADER FLAG
    ("Greatsword of the Ancient", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    # § 2.5 Battle-mage (10 rows) — STR+INT
    ("Death Knight's Runeblade (STR+INT)", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "category", "handheld_weapon", "WoW Death Knight STR-primary classification", "A", None),
    ("FFXIV Red Mage Rapier", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "high", "named_template", "handheld_weapon", "FFXIV Red Mage", "A", False),
    ("FFXIV Dark Knight Claymore", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "named_template", "handheld_weapon", "FFXIV Dark Knight", "A", False),
    ("Magitek Knuckle Blade", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee_close_or_grapple", "high", "named_template", "handheld_weapon", "FFXIV/FF6 Magitek Empire", "A", False),
    ("Magic Warrior Zweihander", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "category", "handheld_weapon", "anime magic-knight", "A", False),
    ("Arcane Fighter's Battleaxe", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Spellsword Composite Blade", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "generic spellblade", "A", False),
    ("Battle-Mage's Glaive", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "mid", "medium", "category", "handheld_weapon", "magitek soldier polearm", "A", False),
    ("Arcane Halberd", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "mid", "medium", "category", "handheld_weapon", "genre canon", "A", False),
    ("Enchanted Greathammer", "STR", "INT", "lightning", "fantasy_generic", "fictional", "fantasy", "single", "melee", "low", "category", "handheld_weapon", "genre canon", "A", False),
    # § 2.6 Mythological hybrid warriors (10 rows)
    ("Gram/Balmung/Nothung", "STR", "INT", "arcane", "european", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Völsunga saga", "S", False),
    ("Mjolnir (Thor's Hammer)", "STR", "WIS", "lightning", "european", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Norse mythology Wikipedia", "S", False),
    ("Gáe Bolg (Cú Chulainn's Spear)", "STR", "WIS", "holy", "european", "pre_classical", "mythological", "single", "mid", "medium", "named_template", "handheld_weapon", "Celtic mythology", "S", False),
    ("Gandiva (Arjuna's Bow)", "DEX", "WIS", "holy", "south_asian", "pre_classical", "mythological", "single", "ranged", "medium", "named_template", "handheld_weapon", "Mahabharata Wikipedia", "S", False),
    ("Sudarshana Chakra (Vishnu's Discus)", "INT", "WIS", "holy", "south_asian", "pre_classical", "mythological", "AoE", "ranged", "high", "named_template", "handheld_weapon", "Vedic Astras Wikipedia", "S", False),
    ("Vajra (Indra's Thunderbolt)", "STR", "INT", "lightning", "south_asian", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Vedic tradition Wikipedia", "S", False),
    ("Trishula of Shiva", "STR", "WIS", "holy", "south_asian", "pre_classical", "mythological", "cleave", "mid", "medium", "named_template", "handheld_weapon", "Hindu tradition Wikipedia", "S", False),
    ("Totsuka-no-Tsurugi (Izanagi's Sword)", "STR", "WIS", "holy", "east_asian", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Japanese mythology Wikipedia", "S", False),
    ("Ame-no-Habakiri (Susanoo's Sword)", "STR", "WIS", "holy", "east_asian", "pre_classical", "mythological", "single", "melee", "medium", "named_template", "handheld_weapon", "Japanese mythology", "S", False),
    ("Holy Avenger (Arthurian variation)", "STR", "WIS", "holy", "european", "medieval", "mythological", "single", "melee", "medium", "category", "handheld_weapon", "Arthurian Excalibur-class", "A", False),
    # § 2.7 Genre hybrid (12 rows)
    ("Red Mage's Crystal (FFXIV)", "INT", "WIS", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "accessory_handheld", "FFXIV Red Mage crystal", "A", False),
    ("Soul Crystal Weapon", "STR", "WIS", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "FFXIV job system", "A", False),
    ("Arcanist's Codex-Staff", "INT", "WIS", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "mid", "medium", "named_template", "handheld_weapon", "FFXIV Arcanist", "A", False),
    ("Death Knight's Unholy Runeblade", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "AoE", "melee", "medium", "named_template", "handheld_weapon", "WoW Death Knight unholy", "A", False),
    ("Frost Death Knight Runeblade", "STR", "INT", "ice", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "named_template", "handheld_weapon", "WoW Death Knight frost", "A", False),
    ("Bladedancer's Twinblade", "DEX", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "multi-hit", "melee", "high", "category", "handheld_weapon", "FFXIV Dancer / ARPG genre", "A", False),
    ("Paladin's Holy Sword (FFXIV)", "STR", "WIS", "holy", "fantasy_generic", "fictional", "fantasy", "AoE", "melee", "medium", "named_template", "handheld_weapon", "FFXIV Paladin", "S", True),  # HOLY-FIRE CRUSADER FLAG
    ("Astrologian's Celestial Mace", "WIS", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "handheld_weapon", "FFXIV Astrologian", "A", False),
    ("Scholar's Grimoire-Shield", "INT", "STR", "arcane", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "named_template", "accessory_handheld", "FFXIV Scholar", "A", False),
    ("PoE Inquisitor Sceptre", "STR", "INT", "holy", "fantasy_generic", "fictional", "fantasy", "single", "melee", "medium", "category", "handheld_weapon", "Path of Exile Inquisitor", "A", False),
    ("PoE Chieftain War Staff", "STR", "INT", "fire", "fantasy_generic", "fictional", "fantasy", "single", "mid", "medium", "category", "handheld_weapon", "Path of Exile Chieftain", "A", False),
    ("PoE Champion-Mage Axe", "STR", "INT", "arcane", "fantasy_generic", "fictional", "fantasy", "cleave", "melee", "medium", "category", "handheld_weapon", "Path of Exile genre canon", "A", False),
]
assert len(HYBRID_ROWS) == 70, f"Hybrid rows: expected 70, got {len(HYBRID_ROWS)}"


# Patch one classification: Death Knight's Runeblade (STR+INT) has a None flag — replace with False
HYBRID_ROWS[40] = HYBRID_ROWS[40][:-1] + (False,)


# ----------------------------------------------------------------------------
# LUT helpers
# ----------------------------------------------------------------------------

def int_caster_range(geometry: str, range_class: str) -> tuple[float, float]:
    # All INT-AoE rows: ranged behavior (5-18 standard for caster-arcane per SC-6b LUT)
    if range_class == "ranged":
        return (8.0, 22.0)  # extended for tomes/orbs throwing
    return (5.0, 18.0)  # mid (staff/rod/wand standard)


def wis_melee_range(range_class: str) -> tuple[float, float]:
    if range_class == "melee_close_or_grapple":
        return (0.0, 1.5)  # unarmed / grapple
    elif range_class == "mid":
        return (1.5, 4.0)  # staves
    elif range_class == "ranged":
        return (3.0, 8.0)  # rope dart
    return (0.5, 2.5)  # default melee


def hybrid_range(primary: str, range_class: str) -> tuple[float, float]:
    # Composes: physical reach × magical attack-range; defer to range_class
    if range_class == "melee_close_or_grapple":
        return (0.0, 1.5)
    elif range_class == "melee":
        return (0.5, 2.5)
    elif range_class == "mid":
        return (1.5, 4.0)
    elif range_class == "ranged":
        return (5.0, 18.0)
    return (0.5, 2.5)


def attack_speed_for_tempo(tempo: str) -> float:
    return {"high": 2.0, "medium": 1.5, "low": 1.0}.get(tempo, 1.5)


def hits_per_attack(geometry: str) -> int:
    return {"multi-hit": 3, "AoE": 1, "single": 1, "cleave": 1, "scatter": 1, "cone": 1}.get(geometry, 1)


def aoe_radius(geometry: str) -> float:
    # 0.0 maintained for non-AoE; AoE uses standard 3.0 unit radius per genre convention
    if geometry == "AoE":
        return 3.0
    return 0.0


def element_json(element: str | None) -> str:
    if element is None or element == "arcane":
        return "{}"
    # Map element to affinity modifier; standard fantasy-genre 25% bias
    mapping = {
        "fire": '{"fire": 25}',
        "ice": '{"ice": 25}',
        "lightning": '{"lightning": 25}',
        "wind": '{"wind": 25}',
        "holy": '{"holy": 25}',
    }
    return mapping.get(element, "{}")


def spell_dmg_pct_for_tier(tier: str) -> float:
    # INT-AoE: 80-160 spread per existing substrate spread
    # WIS-melee-light: 30-90 spread (lower since martial-light)
    # Hybrid: dampened by ω-penalty at evaluation; per-tier base value
    return {"S": 130.0, "A": 90.0, "B": 60.0, "C": 40.0}.get(tier, 80.0)


def quality_composite_score_for_tier(tier: str) -> float:
    # Standard composite score per existing substrate; varies by tier
    return {"S": 0.75, "A": 0.62, "B": 0.50, "C": 0.40}.get(tier, 0.55)


# ----------------------------------------------------------------------------
# Ingest functions
# ----------------------------------------------------------------------------

def ingest_int_aoe(conn: sqlite3.Connection) -> int:
    """Ingest 75 INT-AoE rows. Returns count inserted."""
    cur = conn.cursor()
    inserted = 0
    for row in INT_AOE_ROWS:
        (name, element, geometry, tempo, range_class, lineage, register,
         period, source_ref, weapon_kind, subtype, tier) = row

        slug = _slugify(name)
        source_url = f"legolas_crawl_substrate_enrichment_v1://{slug}"

        trace = make_composition_trace(
            sub_fix="int_aoe",
            tier=tier,
            weapon_kind_subtype=subtype,
            notes=f"element={element}; source_ref={source_ref}",
        )

        cur.execute("""
            INSERT INTO weapon_knowledge_entries
            (canonical_name, source_library, source_url, description_text,
             cultural_lineage_canonical, register_canonical, historical_period_canonical,
             weapon_kind, weapon_kind_classified_subtype,
             proxy_range_class, proxy_geometry_class, proxy_tempo_class,
             proxy_attribute_class,
             cultural_lineage_confidence, template_quality_score,
             quality_composite_score, quality_tier,
             v1_scope, v1_scope_composition_trace, license_class)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, SOURCE_LIBRARY, source_url,
            f"INT-AoE substrate enrichment row; element={element}; source={source_ref}",
            lineage, register, period,
            weapon_kind, subtype,
            range_class, geometry, tempo,
            "INT",
            0.85, 0.75,
            quality_composite_score_for_tier(tier), tier,
            1, trace, "synthesis_public_domain",
        ))
        weapon_id = cur.lastrowid

        r_min, r_max = int_caster_range(geometry, range_class)
        spell_pct = spell_dmg_pct_for_tier(tier)
        cur.execute("""
            INSERT INTO weapon_sim_props
            (weapon_id, range_min_units, range_max_units, base_attack_speed,
             charge_time_s, hits_per_attack, aoe_radius_units,
             primary_stat, secondary_stat,
             damage_amplitude_min, damage_amplitude_max,
             sim_viable, base_physical_damage_l50, spell_damage_modifier_pct,
             element_affinity_modifiers_json, weapon_type_family)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            weapon_id, r_min, r_max, attack_speed_for_tempo(tempo),
            0.0, hits_per_attack(geometry), aoe_radius(geometry),
            "INT", "none",
            0.84, 2.4,
            1, 50.22, spell_pct,
            element_json(element), "caster-arcane",
        ))
        inserted += 1
    return inserted


def ingest_monk(conn: sqlite3.Connection) -> int:
    """Ingest 61 Monk (WIS-melee-light) rows. Returns count inserted."""
    cur = conn.cursor()
    inserted = 0
    for row in MONK_ROWS:
        (name, lineage, period, register, geometry, range_class, tempo,
         weapon_kind, subtype, source_ref, tier, edge_case_note) = row

        slug = _slugify(name)
        source_url = f"legolas_crawl_substrate_enrichment_v1://{slug}"

        # E2 Trishula: still WIS-caster-faith semantically but lands in monk crawl;
        # other rows: WIS-melee-light. Both → weapon_type_family=caster-faith
        # (per legolas recommendation in monk-completion § 4.2)

        trace = make_composition_trace(
            sub_fix="monk_wis_melee_light",
            tier=tier,
            weapon_kind_subtype=subtype,
            notes=f"source_ref={source_ref}" + (f"; edge_case={edge_case_note}" if edge_case_note else ""),
        )

        cur.execute("""
            INSERT INTO weapon_knowledge_entries
            (canonical_name, source_library, source_url, description_text,
             cultural_lineage_canonical, register_canonical, historical_period_canonical,
             weapon_kind, weapon_kind_classified_subtype,
             proxy_range_class, proxy_geometry_class, proxy_tempo_class,
             proxy_attribute_class,
             cultural_lineage_confidence, template_quality_score,
             quality_composite_score, quality_tier,
             v1_scope, v1_scope_composition_trace, license_class)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, SOURCE_LIBRARY, source_url,
            f"Monk WIS-melee-light substrate enrichment row; source={source_ref}",
            lineage, register, period,
            weapon_kind, subtype,
            range_class, geometry, tempo,
            "WIS",
            0.85, 0.75,
            quality_composite_score_for_tier(tier), tier,
            1, trace, "synthesis_public_domain",
        ))
        weapon_id = cur.lastrowid

        r_min, r_max = wis_melee_range(range_class)
        spell_pct = spell_dmg_pct_for_tier(tier) * 0.7  # monk has lower spell-dmg-mod than caster-mace
        cur.execute("""
            INSERT INTO weapon_sim_props
            (weapon_id, range_min_units, range_max_units, base_attack_speed,
             charge_time_s, hits_per_attack, aoe_radius_units,
             primary_stat, secondary_stat,
             damage_amplitude_min, damage_amplitude_max,
             sim_viable, base_physical_damage_l50, spell_damage_modifier_pct,
             element_affinity_modifiers_json, weapon_type_family)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            weapon_id, r_min, r_max, attack_speed_for_tempo(tempo),
            0.0, hits_per_attack(geometry), aoe_radius(geometry),
            "WIS", "none",
            0.84, 2.4,
            1, 50.22, spell_pct,
            "{}", "caster-faith",
        ))
        inserted += 1
    return inserted


def ingest_hybrid(conn: sqlite3.Connection) -> int:
    """Ingest 70 Hybrid cross-attribute rows. Returns count inserted."""
    cur = conn.cursor()
    inserted = 0
    for row in HYBRID_ROWS:
        (name, primary_stat, secondary_stat, element, lineage, period, register,
         geometry, range_class, tempo, weapon_kind, subtype, source_ref, tier,
         holy_fire_flag) = row

        slug = _slugify(name)
        source_url = f"legolas_crawl_substrate_enrichment_v1://{slug}"

        trace = make_composition_trace(
            sub_fix="hybrid_cross_attribute",
            tier=tier,
            weapon_kind_subtype=subtype,
            option_c_eligible=True,
            cycle_15_path_a_candidate=bool(holy_fire_flag),
            notes=f"primary={primary_stat}+secondary={secondary_stat}; element={element}; source_ref={source_ref}",
        )

        cur.execute("""
            INSERT INTO weapon_knowledge_entries
            (canonical_name, source_library, source_url, description_text,
             cultural_lineage_canonical, register_canonical, historical_period_canonical,
             weapon_kind, weapon_kind_classified_subtype,
             proxy_range_class, proxy_geometry_class, proxy_tempo_class,
             proxy_attribute_class,
             cultural_lineage_confidence, template_quality_score,
             quality_composite_score, quality_tier,
             v1_scope, v1_scope_composition_trace, license_class)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, SOURCE_LIBRARY, source_url,
            f"Hybrid cross-attribute substrate enrichment; primary={primary_stat}+secondary={secondary_stat}; element={element}; source={source_ref}",
            lineage, register, period,
            weapon_kind, subtype,
            range_class, geometry, tempo,
            primary_stat,
            0.85, 0.75,
            quality_composite_score_for_tier(tier), tier,
            1, trace, "synthesis_public_domain",
        ))
        weapon_id = cur.lastrowid

        r_min, r_max = hybrid_range(primary_stat, range_class)
        spell_pct = spell_dmg_pct_for_tier(tier)
        # Hybrid blend: physical baseline + magical baseline; ω-penalty at evaluation
        # Use primary-stat-archetype scaling
        if primary_stat == "STR":
            base_phys = 75.0  # STR-primary → higher physical baseline
            spell_pct = spell_pct * 0.5  # cross-attribute spell scaling reduced
        elif primary_stat == "INT":
            base_phys = 50.22  # INT-primary → caster baseline
            spell_pct = spell_pct * 1.0
        elif primary_stat == "WIS":
            base_phys = 50.22
            spell_pct = spell_pct * 0.7
        elif primary_stat == "DEX":
            base_phys = 65.0
            spell_pct = spell_pct * 0.6
        else:
            base_phys = 50.22

        cur.execute("""
            INSERT INTO weapon_sim_props
            (weapon_id, range_min_units, range_max_units, base_attack_speed,
             charge_time_s, hits_per_attack, aoe_radius_units,
             primary_stat, secondary_stat,
             damage_amplitude_min, damage_amplitude_max,
             sim_viable, base_physical_damage_l50, spell_damage_modifier_pct,
             element_affinity_modifiers_json, weapon_type_family)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            weapon_id, r_min, r_max, attack_speed_for_tempo(tempo),
            0.0, hits_per_attack(geometry), aoe_radius(geometry),
            primary_stat, secondary_stat,
            0.84, 2.4,
            1, base_phys, spell_pct,
            element_json(element), "hybrid",
        ))
        inserted += 1
    return inserted


# ----------------------------------------------------------------------------
# Verification queries
# ----------------------------------------------------------------------------

def run_verification(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    results = {}

    cur.execute("""
        SELECT COUNT(*) FROM weapon_sim_props wsp
        JOIN weapon_knowledge_entries wke ON wke.id=wsp.weapon_id
        WHERE wke.v1_scope=1 AND wsp.weapon_type_family='caster-arcane'
        AND wsp.primary_stat='INT' AND wke.proxy_geometry_class='AoE'
    """)
    results["int_aoe_caster_arcane"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM weapon_sim_props wsp
        JOIN weapon_knowledge_entries wke ON wke.id=wsp.weapon_id
        WHERE wke.v1_scope=1 AND wsp.weapon_type_family='caster-faith'
        AND wsp.primary_stat='WIS' AND wke.proxy_range_class IN ('melee','melee_close_or_grapple','mid')
        AND wke.source_library=?
    """, (SOURCE_LIBRARY,))
    results["monk_wis_caster_faith_new"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM weapon_sim_props WHERE weapon_type_family='hybrid'
    """)
    results["hybrid_family_total"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM weapon_sim_props
        WHERE secondary_stat IS NOT NULL AND secondary_stat != 'none'
    """)
    results["secondary_stat_not_none"] = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1")
    results["total_v1_scope"] = cur.fetchone()[0]

    cur.execute("""
        SELECT primary_stat, COUNT(*) FROM weapon_knowledge_entries wke
        JOIN weapon_sim_props wsp ON wsp.weapon_id=wke.id
        WHERE wke.v1_scope=1 GROUP BY primary_stat
    """)
    results["primary_stat_distribution"] = dict(cur.fetchall())

    cur.execute("""
        SELECT weapon_type_family, COUNT(*) FROM weapon_sim_props wsp
        JOIN weapon_knowledge_entries wke ON wke.id=wsp.weapon_id
        WHERE wke.v1_scope=1 GROUP BY weapon_type_family
    """)
    results["family_distribution"] = dict(cur.fetchall())

    cur.execute("""
        SELECT COUNT(*) FROM weapon_knowledge_entries
        WHERE v1_scope_composition_trace LIKE '%cycle_15_path_a_discriminator_candidate%'
    """)
    results["holy_fire_crusader_flagged"] = cur.fetchone()[0]

    return results


def main() -> int:
    if not Path(DB_PATH).exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1
    backup_path = Path(DB_PATH + ".pre-substrate-enrichment-2026-05-27.bak")
    if not backup_path.exists():
        print(f"ERROR: Pre-ingest backup not found at {backup_path}", file=sys.stderr)
        print("       Run: cp telemetry.db telemetry.db.pre-substrate-enrichment-2026-05-27.bak", file=sys.stderr)
        return 1

    print(f"Pre-ingest backup verified: {backup_path}")
    print(f"DB: {DB_PATH}")
    print()

    conn = sqlite3.connect(DB_PATH)
    try:
        # Pre-ingest verification
        pre = run_verification(conn)
        print("=== PRE-INGEST STATE ===")
        for k, v in pre.items():
            print(f"  {k}: {v}")
        print()

        # Ingest per-sub-fix
        print("=== SUB-FIX 1: INT-AoE ===")
        n1 = ingest_int_aoe(conn)
        conn.commit()
        print(f"  Inserted: {n1} rows")
        print()

        print("=== SUB-FIX 2: Monk WIS-melee-light ===")
        n2 = ingest_monk(conn)
        conn.commit()
        print(f"  Inserted: {n2} rows")
        print()

        print("=== SUB-FIX 3: Hybrid cross-attribute ===")
        n3 = ingest_hybrid(conn)
        conn.commit()
        print(f"  Inserted: {n3} rows")
        print()

        # Post-ingest verification
        post = run_verification(conn)
        print("=== POST-INGEST STATE ===")
        for k, v in post.items():
            print(f"  {k}: {v}")
        print()

        # Delta summary
        print("=== DELTAS ===")
        print(f"  Total v1_scope: {pre['total_v1_scope']} -> {post['total_v1_scope']} (+{post['total_v1_scope']-pre['total_v1_scope']})")
        print(f"  INT-AoE caster-arcane: {pre['int_aoe_caster_arcane']} -> {post['int_aoe_caster_arcane']} (+{post['int_aoe_caster_arcane']-pre['int_aoe_caster_arcane']})")
        print(f"  hybrid family: {pre['hybrid_family_total']} -> {post['hybrid_family_total']} (+{post['hybrid_family_total']-pre['hybrid_family_total']})")
        print(f"  secondary_stat != none: {pre['secondary_stat_not_none']} -> {post['secondary_stat_not_none']} (+{post['secondary_stat_not_none']-pre['secondary_stat_not_none']})")
        print(f"  holy-fire crusader flagged: {post['holy_fire_crusader_flagged']}")

        total = n1 + n2 + n3
        print()
        print(f"TOTAL INSERTED: {total} rows (expected: 206)")
        if total == 206:
            print("OK: all 206 rows inserted successfully")
            return 0
        else:
            print(f"ERROR: insertion count mismatch (expected 206, got {total})", file=sys.stderr)
            return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
