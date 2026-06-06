"""
Cosmograph Phase 0 — Primitive vocabulary enumeration + region labels v0.

Authored: elrond 2026-06-06 per dispatch
  agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md
  AMENDED in-place at § 2.5 + § 4.1 step 2 per Pattern-A verdict at
  agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md

Discipline anchors:
  #11 (empirical inspection) — every count traced to authoritative source
  #41 (substrate-led) — flat mechanic enumeration; no family pre-imposition
  #42 (framing-audit) — Q1-Q3 applied at top of execution
  #58 (genre-aligned kit-roster ratio) — surface B target, lives in Phase 2 not Phase 0
  #59 (substrate-coverage honesty) — render empirical phys/mag ratio honestly

Output (in same directory as script):
  - primitive_registry_v0.json — flat per-primitive enumeration (14+ families)
  - region_labels_v0.json — BC bin labels + tier labels + scaling labels + chain labels
                            (emergent mechanic-family labels DEFERRED to Phase 3)
  - cosmograph_phase0_notes.md — framing-audit Q1-Q3 + counts summary + provenance

ALL primitives carry source-anchored canonical_source + provenance tags where
applicable (per verdict § 3 refinements).

Substrate-led discipline: enumerate what the substrate says, not what we wish
it said. Per verdict, weapon-form-token region renders ~89% phys / ~11% mag
HONESTLY (Surface A); kit-roster element-axis-coverage 40-45/55-60 lives in
Phase 2, not here (Surface B).
"""
from __future__ import annotations

import json
import yaml
from pathlib import Path
from datetime import datetime

# Output directory — Phase 0 work directory (per dispatch § 1.1)
OUTPUT_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "elrond/research/cosmograph-substrate-trace-2026-06-06"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Authoritative source paths
ENGINE_ROOT = Path("/Users/admin/Games/reincarnated-engine")
ELEMENTS_YAML = ENGINE_ROOT / "config/elements.yaml"
RESOURCES_YAML = ENGINE_ROOT / "config/resources.yaml"
UNIFIED_MECHANIC_POOL = ENGINE_ROOT / "src/reincarnated/generation/unified_mechanic_pool.yaml"
WEAPON_FORM_LOOKUP = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/"
    "research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json"
)
COLLAB_ROOT = Path("/Users/admin/Games/reincarnated-collaboration")
FLAVOR_POOL_LOCK = COLLAB_ROOT / "canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md"
ATOMIC_SUBSTRATE_REGISTRY = COLLAB_ROOT / "canonical/story/2026-06-06-atomic-substrate-registry.md"


# ============================================================================
# Primitive registry — flat list of dict rows
# ============================================================================

primitives: list[dict] = []


def add_primitive(**kwargs) -> None:
    """Add a primitive row. Schema per dispatch § 2.2."""
    row = {
        # Required fields
        "primitive_id": kwargs["primitive_id"],
        "primitive_family": kwargs["primitive_family"],
        "primitive_label": kwargs.get("primitive_label", kwargs["primitive_id"]),
        # Substrate signature (populated per family; minimal for Phase 0)
        "substrate_fingerprint": kwargs.get("substrate_fingerprint", {}),
        # Couplings
        "element_coupling": kwargs.get("element_coupling", []),
        "attribute_coupling": kwargs.get("attribute_coupling", []),
        # Provenance
        "canonical_source": kwargs.get("canonical_source", ""),
        "provenance_tag": kwargs.get("provenance_tag", ""),  # per verdict § 3 refinements
        # Phase 3 populated (UMAP + BDI)
        "bdi_weight": None,
        "embedding_x": None,
        "embedding_y": None,
        # Rendering hints
        "visibility_at_default_zoom": kwargs.get("visibility_at_default_zoom", True),
        "is_simulated": False,
        # Optional notes
        "notes": kwargs.get("notes", ""),
    }
    primitives.append(row)


# ============================================================================
# 1.1 — Element primitives (8)
# ============================================================================

# Load elements.yaml for authoritative element data
with open(ELEMENTS_YAML) as f:
    elements_data = yaml.safe_load(f)

ELEMENT_ATTRIBUTE_COUPLING = {
    "fire": ["INT"],
    "water": ["INT"],
    "earth": ["WIS"],
    "wind": ["WIS"],
    "lightning": ["INT"],
    "holy": ["WIS"],
    "shadow": ["INT"],
    "physical": ["STR"],
}

for elem_entry in elements_data["elements"]:
    name = elem_entry["name"]
    rotating = elem_entry.get("rotating", False)
    prov_tag = "canonical_7_rotating" if rotating else "canonical_plus_physical"
    add_primitive(
        primitive_id=f"element_{name}",
        primitive_family="element",
        primitive_label=elem_entry["display"],
        substrate_fingerprint={
            "ailment": elem_entry.get("ailment"),
            "rotating": rotating,
            "resistance_type": elem_entry.get("resistance_type"),
            "scales_with": elem_entry.get("scales_with"),
            "theme_tags": elem_entry.get("theme_tags", []),
            "color_range": elem_entry.get("color_range", []),
        },
        attribute_coupling=ELEMENT_ATTRIBUTE_COUPLING.get(name, []),
        canonical_source="reincarnated-engine/config/elements.yaml",
        provenance_tag=prov_tag,
        visibility_at_default_zoom=True,
    )

# ============================================================================
# 1.2 — Sub-element / flavor primitives (109 total: 100 rotating + 9 physical)
# Per flavor-pool-per-primary-element-lock 2026-06-01
# ============================================================================

# Per-primary flavor pools verbatim from canonical lock § 2.1-2.8
ROTATING_FLAVOR_POOLS = {
    "fire": ["ember", "cinder", "blaze", "scorch", "inferno", "ignite", "fira", "lava",
             "magma", "charcoal", "char", "brand", "flare", "fusion", "thermal", "combustion"],
    "water": ["tide", "torrent", "glacial", "brine", "aqua", "frost", "chill", "mist",
              "ice", "glacier", "wave", "marsh", "hydro", "hydraulic"],
    "earth": ["stone", "granite", "marble", "clay", "sand", "iron", "gold", "silver",
              "lead", "gem", "crystal", "obsidian", "amber", "quake", "tremor", "thorn",
              "seismic", "tectonic"],
    "wind": ["tempest", "cyclone", "whirlwind", "gale", "gust", "squall", "hurricane",
             "zephyr", "hail", "sleet", "cloud", "sonic", "shockwave"],
    "lightning": ["arc", "static", "surge", "volt", "bolt", "shock", "spark", "thunder",
                  "plasma", "flash", "ion", "voltage", "tesla"],
    "holy": ["radiance", "radiant", "dawn", "aura", "divine", "sacred", "blessed", "lux",
             "celestial", "stellar", "solar", "photon", "laser", "prismatic"],
    "shadow": ["void", "shade", "wraith", "drain", "necrotic", "abyss", "shadow", "lich",
               "blackhole", "singularity", "darkmatter", "soul"],
}

# Architecture A — physical's 9 taxonomy-sibling entries (NOT flavor-pool)
PHYSICAL_TAXONOMY_REGISTRY = [
    # Damage sub-type field (D&D 5e PHB ch.9)
    ("piercing", "damage_subtype"),
    ("slashing", "damage_subtype"),
    ("bludgeoning", "damage_subtype"),
    ("force", "damage_subtype"),
    # Mechanical action vocabulary
    ("pierce", "mechanical_action"),
    ("slash", "mechanical_action"),
    ("sever", "mechanical_action"),
    ("strike", "mechanical_action"),
    # Pre-locked ailment
    ("bleed", "ailment"),
]

# Rotating flavor pool — 100 entries (per provenance § 7.1)
for primary, pool in ROTATING_FLAVOR_POOLS.items():
    for flavor in pool:
        add_primitive(
            primitive_id=f"flavor_{primary}_{flavor}",
            primitive_family="sub_element_flavor",
            primitive_label=flavor,
            substrate_fingerprint={
                "primary_element": primary,
                "shape": "rotating_flavor_pool",
            },
            element_coupling=[primary],
            canonical_source="canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md",
            provenance_tag="rotating_flavor_pool_v1_2026-06-01",
            visibility_at_default_zoom=False,  # rendered as small stars, drill-in
        )

# Physical taxonomy-sibling registry — 9 entries (Architecture A asymmetry)
for entry, schema_role in PHYSICAL_TAXONOMY_REGISTRY:
    add_primitive(
        primitive_id=f"physical_taxonomy_{entry}",
        primitive_family="sub_element_flavor",
        primitive_label=entry,
        substrate_fingerprint={
            "primary_element": "physical",
            "shape": "architecture_A_taxonomy_sibling",
            "schema_role": schema_role,
        },
        element_coupling=["physical"],
        canonical_source="canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md",
        provenance_tag="architecture_A_taxonomy_sibling_v1_2026-06-01",
        visibility_at_default_zoom=False,
        notes="Architecture A asymmetry — physical opts out of WS1A.4 LLM flavor judgment; "
              "render with distinct glyph (square vs star) per verdict § 3.4 visual encoding",
    )

# ============================================================================
# 1.3 — Attribute primitives (4 active + VIT deferred-placeholder)
# Per atomic-substrate-registry § 1.3 + verdict § 3.3
# ============================================================================

ATTRIBUTE_DEFINITIONS = [
    ("STR", "Strength", ["physical"], "active", "primary_attribute_v1"),
    ("DEX", "Dexterity", [], "active", "primary_attribute_v1"),  # uncoupled per registry § 1.3
    ("INT", "Intelligence", ["fire", "water", "lightning", "shadow"], "active", "primary_attribute_v1"),
    ("WIS", "Wisdom", ["earth", "wind", "holy"], "active", "primary_attribute_v1"),
    ("VIT", "Vitality", [], "deferred_placeholder",
     "deferred_placeholder_v1_2026-05-24"),  # per verdict § 3.3 — render as faint outline
]

for attr_id, attr_label, elem_coupling, status, prov_tag in ATTRIBUTE_DEFINITIONS:
    add_primitive(
        primitive_id=f"attribute_{attr_id}",
        primitive_family="attribute",
        primitive_label=attr_label,
        substrate_fingerprint={
            "status": status,
            "uncoupled_to_canonical_7": (attr_id == "DEX"),
        },
        element_coupling=elem_coupling,
        canonical_source="canonical/story/attribute-system-2026-05-24.md + "
                         "reincarnated-engine/src/reincarnated/generation/element_biases.py:28",
        provenance_tag=prov_tag,
        visibility_at_default_zoom=True,
        notes=("DEX intentionally uncoupled per registry § 1.3; cross-attribute via T4 "
               "ELEMENT_CONVERSION" if attr_id == "DEX"
               else "Render as faint outline / unfilled circle per verdict § 3.3 visual encoding"
               if attr_id == "VIT" else ""),
    )

# ============================================================================
# 1.4 — T4 strategy primitives (8 with provenance tags per verdict § 3.1)
# Per canonical 47 § 4.6 two-layer T4 architecture + Matt D3 ratification
# ============================================================================

T4_STRATEGIES = [
    # Active-v1.13 — Primary T4 universal (Discipline #39 scaffold w/ Cycle 15 retirement)
    ("DIRECT_DAMAGE_AMPLIFICATION", "Primary T4 (universal)", "1.75x preferred-encounter-type",
     "active-v1.13", "primary_universal"),
    # Active-v1.13 — Layer 2 strategies (per Matt D3 ratification)
    ("ELEMENT_CONVERSION_VARIANT_A", "Mono-caster Replace+Mult", "1.50x multiplicative",
     "active-v1.13", "layer_2_strip_and_ship"),
    ("ELEMENT_CONVERSION_VARIANT_B", "Hybrid-caster Dual_Add", "1.25x dual-element",
     "active-v1.13", "layer_2_strip_and_ship"),
    ("ELEMENT_CONVERSION_VARIANT_C", "Physical Hybrid", "0.25 additive + ailment",
     "active-v1.13", "layer_2_strip_and_ship"),
    ("TRADE_OFF_REVERSED", "Trade-off Reversed (Frenzy)", "engine-implemented per `combatant.py:588-609`",
     "active-v1.13", "layer_2_strip_and_ship"),
    ("GEOMETRY_COLLAPSE", "Geometry Collapse", "empirical 'try it out' per Matt D3",
     "active-v1.13", "layer_2_strip_and_ship"),
    ("RESOURCE_CONVERSION", "Resource Conversion", "empirical 'try it out' per Matt D3",
     "active-v1.13", "layer_2_strip_and_ship"),
    # Retired (per verdict § 3.1 — render dim at 0.20 brightness, archaeological reference)
    ("DEFENSIVE_TRADEOFF", "Defensive Tradeoff (RETIRED v1.13)",
     "removed pre-Phase-4-RE-RUN-3; no chaos encounter signal",
     "retired-but-preserved", "retired_v1.13"),
]

for t4_id, t4_label, t4_effect, prov_tag, layer_role in T4_STRATEGIES:
    is_retired = (prov_tag == "retired-but-preserved")
    add_primitive(
        primitive_id=f"T4_{t4_id}",
        primitive_family="T4_strategy",
        primitive_label=t4_label,
        substrate_fingerprint={
            "effect": t4_effect,
            "layer_role": layer_role,
            "brightness_hint": 0.20 if is_retired else 1.0,  # per verdict § 3.1
            "tier": "T4_capstone",
        },
        canonical_source="canonical/47-damage-scaling-architecture-2026-05-27.md § 4.6 "
                         "(two-layer T4 architecture v1.2 LOCKED)",
        provenance_tag=prov_tag,
        visibility_at_default_zoom=True,  # T4 = capstone-keystone; extra bright in cosmograph
        notes=("Discipline #39 scaffold w/ EXPLICIT Cycle 15 retirement commit per Matt D5"
               if t4_id == "DIRECT_DAMAGE_AMPLIFICATION"
               else "Render at brightness 0.20 (dim-but-visible) per verdict § 3.1 — "
                    "design-history visibility"
               if is_retired else ""),
    )

# ============================================================================
# 1.5 — Skill geometry palette (28 current-emit-pool per ability_grammar.py VALID_GEOMETRIES)
# Per verdict § 3.2 + canonical 09 + B11 + B13 + 2026-05-16 collapse
# Engine ground truth (28) used; dispatch said "25" but engine is the canonical source.
# ============================================================================

# Provenance traced from canonical/historical/09-geometry-palette-discussion.md
# (2026-05-08 CORE 14; 2026-05-11 B11 expansion; 2026-05-11 evening B13 defensive-mobility;
# 2026-05-16 collapse)
GEOMETRY_PROVENANCE = {
    # CORE_14 (pre-B11 baseline — 2026-05-08 decision table)
    "single_target": "CORE_14",
    "projectile": "CORE_14",
    "cone": "CORE_14",
    "circle": "CORE_14",
    "line": "CORE_14",
    "persistent_zone": "CORE_14",
    "melee_strike": "CORE_14",
    "melee_arc": "CORE_14",
    "ground_slam": "CORE_14",
    "ranged_physical": "CORE_14",
    "ground_targeted_circle": "CORE_14",
    "teleport": "CORE_14",
    "self_buff": "CORE_14",
    "totem": "CORE_14",
    # CORE_MARGINAL_2 (2026-05-08 marginal types — generator-restricted)
    "aura": "CORE_MARGINAL_2",
    "beam_channel": "CORE_MARGINAL_2",
    # B11_EXPANSION (2026-05-11 — 9 new + parameter expansions)
    "whirlwind": "B11_EXPANSION",
    "dash_attack": "B11_EXPANSION",
    "leap_strike": "B11_EXPANSION",
    "chain_lightning": "B11_EXPANSION",
    "ricochet_bounce": "B11_EXPANSION",
    "fork": "B11_EXPANSION",
    "vortex_pull": "B11_EXPANSION",
    "ring": "B11_EXPANSION",
    "multi_projectile": "B11_EXPANSION",
    # B13_DEFENSIVE_MOBILITY (2026-05-11 evening — 5 defensive-mobility geos;
    # 3 of 5 active in current emit pool; strafe_mode + dodge_stance vocabulary-only)
    "roll": "B13_DEFENSIVE_MOBILITY",
    "defensive_dash": "B13_DEFENSIVE_MOBILITY",
    "blink": "B13_DEFENSIVE_MOBILITY",
}

# Damage-radius category from doc 09 (used as ambient region label later)
GEOMETRY_RADIUS_CATEGORY = {
    # single_target
    "single_target": "single_target", "projectile": "single_target",
    "melee_strike": "single_target", "ranged_physical": "single_target",
    # AOE
    "cone": "AOE", "circle": "AOE", "line": "AOE", "persistent_zone": "AOE",
    "melee_arc": "AOE", "ground_slam": "AOE", "ground_targeted_circle": "AOE",
    "totem": "AOE", "aura": "AOE", "beam_channel": "AOE",
    "whirlwind": "AOE", "dash_attack": "AOE", "leap_strike": "AOE",
    "chain_lightning": "AOE", "ricochet_bounce": "AOE", "fork": "AOE",
    "vortex_pull": "AOE", "ring": "AOE", "multi_projectile": "AOE",
    # other
    "teleport": "other", "self_buff": "other",
    # B13 defensive-mobility
    "roll": "other", "defensive_dash": "other", "blink": "other",
}

for geo, prov in GEOMETRY_PROVENANCE.items():
    add_primitive(
        primitive_id=f"geometry_{geo}",
        primitive_family="skill_geometry",
        primitive_label=geo,
        substrate_fingerprint={
            "radius_category": GEOMETRY_RADIUS_CATEGORY.get(geo, "unknown"),
        },
        canonical_source="reincarnated-engine/src/reincarnated/generation/ability_grammar.py "
                         "VALID_GEOMETRIES + canonical/historical/09-geometry-palette-discussion.md",
        provenance_tag=prov,
        visibility_at_default_zoom=True,
        notes="Per verdict § 3.2 — provenance-tag visual encoding distinguishes expansion history",
    )

# ============================================================================
# 1.6 — Skill-tree position primitives (combinatorial — enumerate axis values)
# Per atomic-substrate-registry § 1.6 + canonical 39 § 2a
# ============================================================================

SKILL_TREE_TIERS = [
    ("T1_rotation", "T1 Rotation"),
    ("T2_beta_pair", "T2 β-Pair"),
    ("T3_build_defining", "T3 Build-Defining"),
    ("T4_capstone", "T4 Capstone"),
]

for tier_id, tier_label in SKILL_TREE_TIERS:
    add_primitive(
        primitive_id=f"position_tier_{tier_id}",
        primitive_family="skill_tree_position",
        primitive_label=tier_label,
        substrate_fingerprint={"axis": "tier_within_tree"},
        canonical_source="canonical/47-damage-scaling-architecture-2026-05-27.md + "
                         "canonical/story/2026-06-06-atomic-substrate-registry.md § 1.6",
        provenance_tag="tier_axis_v1",
        visibility_at_default_zoom=True,
    )

# Chain roles
for role_id, role_label in [
    ("capstone_chain", "Capstone Chain (T4-bearing)"),
    ("supporting_T3_only_chain", "Supporting Chain (T3-only)"),
]:
    add_primitive(
        primitive_id=f"position_chain_role_{role_id}",
        primitive_family="skill_tree_position",
        primitive_label=role_label,
        substrate_fingerprint={"axis": "chain_role"},
        canonical_source="canonical/40-gear-balance-guide-architecture-2026-05-26.md D83 + "
                         "canonical/story/2026-06-06-atomic-substrate-registry.md § 1.6",
        provenance_tag="chain_role_axis_v1",
        visibility_at_default_zoom=True,
    )

# ============================================================================
# 1.7 — Scaling-pattern-per-tier primitives (4 per canonical 47 § 1.7)
# ============================================================================

SCALING_PATTERNS = [
    ("additive", "T1 Additive", "T1_rotation"),
    ("additive_plus_multiplicative", "T2 Additive + Multiplicative", "T2_beta_pair"),
    ("multiplicative", "T3 Multiplicative", "T3_build_defining"),
    ("transformative", "T4 Transformative", "T4_capstone"),
]

for pat_id, pat_label, tier_couple in SCALING_PATTERNS:
    add_primitive(
        primitive_id=f"scaling_pattern_{pat_id}",
        primitive_family="scaling_pattern_per_tier",
        primitive_label=pat_label,
        substrate_fingerprint={"applies_at_tier": tier_couple},
        canonical_source="canonical/47-damage-scaling-architecture-2026-05-27.md "
                         "(per-tier scaling patterns)",
        provenance_tag="scaling_pattern_v1_2026-05-27",
        visibility_at_default_zoom=True,
    )

# ============================================================================
# 1.8 — Chain architecture primitives (2 active per atomic-substrate-registry § 1.8)
# ============================================================================

for chain_id, chain_label, composition in [
    ("3_chain_class", "3-Chain Class", "2 T4 capstone chains + 1 supporting T3-only chain"),
    ("4_chain_class", "4-Chain Class", "3 T4 capstone chains + 1 supporting T3-only chain"),
]:
    add_primitive(
        primitive_id=f"chain_arch_{chain_id}",
        primitive_family="chain_architecture",
        primitive_label=chain_label,
        substrate_fingerprint={"composition": composition},
        canonical_source="canonical/40-gear-balance-guide-architecture-2026-05-26.md D83",
        provenance_tag="chain_architecture_v1",
        visibility_at_default_zoom=True,
    )

# ============================================================================
# 1.9 — Investment scaling patterns (6 per canonical 51 § 2)
# Per atomic-substrate-registry § 1.9 + canonical 51 § 2
# ============================================================================

INVESTMENT_PATTERNS = [
    ("1_linear_additive", "Pattern 1 — Active skill damage scaling (LINEAR_ADDITIVE)",
     "Cycle 14 v1", "load-bearing"),
    ("2_passive_effect_scaling", "Pattern 2 — Passive skill effect scaling",
     "Cycle 14 v1", "load-bearing"),
    ("3_threshold_unlock", "Pattern 3 — Threshold unlocks",
     "Cycle 15+", "canonical_locked_stub"),
    ("4_qol_modifier", "Pattern 4 — QoL modifiers",
     "Cycle 15+", "canonical_locked_stub"),
    ("5_synergy_bonus", "Pattern 5 — Synergy bonuses (cross-node)",
     "Cycle 15+", "canonical_locked_stub"),
    ("6_resource_economy", "Pattern 6 — Resource economy modifiers",
     "Cycle 15+", "canonical_locked_stub"),
]

for inv_id, inv_label, cycle, status in INVESTMENT_PATTERNS:
    add_primitive(
        primitive_id=f"investment_pattern_{inv_id}",
        primitive_family="investment_scaling_pattern",
        primitive_label=inv_label,
        substrate_fingerprint={"cycle": cycle, "status": status},
        canonical_source="canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md § 2",
        provenance_tag=f"investment_pattern_v1.2_{status}",
        visibility_at_default_zoom=True,
    )

# ============================================================================
# 1.10 — Mechanic primitives (71 flat per unified_mechanic_pool.yaml)
# Per dispatch § 2.4 substrate-led FLAT enumeration; bc_axis_hints populated
# ============================================================================

with open(UNIFIED_MECHANIC_POOL) as f:
    mechanic_data = yaml.safe_load(f)

for entry in mechanic_data.get("mechanics", []):
    deferred = bool(entry.get("deferred", False))
    bc_hints = entry.get("bc_axis_hints", {})
    # Classify effect_category per dispatch § 2.4 substrate_fingerprint
    cc_tags = entry.get("cc_tags", [])
    is_movement = bool(entry.get("is_movement", False))
    is_proxy = bool(entry.get("is_proxy_creation", False))
    if is_movement:
        effect_category = "mobility"
    elif is_proxy:
        effect_category = "proxy_creation"
    elif cc_tags:
        effect_category = "control"
    elif entry.get("mechanic_id", "").endswith(("_aura", "_aura_moderate", "absorb_self")):
        effect_category = "sustain_defense"
    else:
        effect_category = "damage"

    add_primitive(
        primitive_id=f"mechanic_{entry['mechanic_id']}",
        primitive_family="mechanic",
        primitive_label=entry["mechanic_id"],
        substrate_fingerprint={
            # bc_axis_hints — already populated upstream
            "axis_1_range": bc_hints.get("axis_1_range", ""),
            "axis_2_geometry": bc_hints.get("axis_2_geometry", ""),
            "axis_2B_control": bc_hints.get("axis_2B_control", ""),
            "axis_3A_tempo": bc_hints.get("axis_3A_tempo", ""),
            "axis_3B_variance": bc_hints.get("axis_3B_variance", ""),
            # Per dispatch § 2.4 substrate_fingerprint
            "geometry_tag": entry.get("geometry_type", ""),
            "tempo": bc_hints.get("axis_3A_tempo", ""),
            "range": bc_hints.get("axis_1_range", ""),
            "resource_interaction": entry.get("cost_type", ""),
            "effect_category": effect_category,
            # Auxiliary
            "cc_tags": list(cc_tags),
            "is_movement": is_movement,
            "is_proxy_creation": is_proxy,
            "cd_seconds": entry.get("cd_seconds"),
            "deferred": deferred,
            "deferred_reason": entry.get("deferred_reason", ""),
        },
        canonical_source="reincarnated-engine/src/reincarnated/generation/unified_mechanic_pool.yaml",
        provenance_tag=("active_v1.13" if not deferred else "deferred_engine_v1.13"),
        visibility_at_default_zoom=False,  # ~71 mechanics — drillable
        notes=("Per Matt 2026-06-06 substrate-led correction: FLAT enumeration; "
               "family clustering EMERGES from Phase 3 UMAP embedding, not pre-imposed"),
    )

# ============================================================================
# 1.11 — Resource model primitives (5 per atomic-substrate-registry § 1.11)
# Provenance tagged per verdict § 3.5 — cycle13 schema + foundation/resources.py
# ============================================================================

# Per resources.yaml (currently only mana + stamina; canonical lock = 5 per registry)
RESOURCE_MODELS = [
    ("cooldown", "Cooldown", "foundation/resources.py + cycle13 schema"),
    ("energy", "Energy", "foundation/resources.py + cycle13 schema"),
    ("mana", "Mana", "config/resources.yaml + foundation/resources.py + cycle13 schema"),
    ("stamina", "Stamina", "config/resources.yaml + foundation/resources.py + cycle13 schema"),
    ("ki", "Ki", "foundation/resources.py + cycle13 schema"),
]

for res_id, res_label, provenance_detail in RESOURCE_MODELS:
    in_yaml = res_id in ("mana", "stamina")
    add_primitive(
        primitive_id=f"resource_{res_id}",
        primitive_family="resource_model",
        primitive_label=res_label,
        substrate_fingerprint={
            "in_config_yaml": in_yaml,
            "provenance_detail": provenance_detail,
        },
        canonical_source=("reincarnated-engine/config/resources.yaml + "
                          "reincarnated-engine/src/reincarnated/foundation/resources.py + "
                          "reincarnated-loadout cycle13_characters.db schema"),
        provenance_tag="resource_canonical_5_v1_cycle13_foundation",
        visibility_at_default_zoom=True,
        notes=("Per verdict § 3.5 — operationally-equivalent; YAML/code split is "
               "engine-canonical hygiene, not design-history. Provenance in side-panel "
               "hover only, not main encoding."),
    )

# ============================================================================
# 1.14 — Weapon-form token primitives (277 per weapon_form_token_lookup.json)
# Per dispatch § 2.5 AMENDED — substrate-honest ~89/11 phys/mag rendering
# Per Pattern-A verdict § 2.1 — Surface A; no over-sampling magical
# ============================================================================

with open(WEAPON_FORM_LOOKUP) as f:
    wf_data = json.load(f)

wf_tokens = wf_data.get("tokens", [])

# Phys/mag tagging per (attribute) heuristic:
# STR/DEX → physical_leaning; INT/WIS → magical_leaning; null → unclassified
def classify_token(token: dict) -> str:
    attr = token.get("attribute")
    if attr in ("STR", "DEX"):
        return "physical"
    if attr in ("INT", "WIS"):
        return "magical"
    return "unclassified"

# Empirical ratio measurement (substrate-coverage-honesty)
phys_count = sum(1 for t in wf_tokens if classify_token(t) == "physical")
mag_count = sum(1 for t in wf_tokens if classify_token(t) == "magical")
unclass_count = sum(1 for t in wf_tokens if classify_token(t) == "unclassified")
phys_ratio_at_classified = phys_count / (phys_count + mag_count) if (phys_count + mag_count) else 0

for tok in wf_tokens:
    token_str = tok["token"]
    phys_mag = classify_token(tok)
    add_primitive(
        primitive_id=f"weapon_form_{token_str.replace(' ', '_').replace('-', '_').replace('é', 'e')}",
        primitive_family="weapon_form_token",
        primitive_label=token_str,
        substrate_fingerprint={
            "specificity": tok.get("specificity"),
            "range": tok.get("range"),
            "geometry": tok.get("geometry"),
            "tempo": tok.get("tempo"),
            "attribute": tok.get("attribute"),
            "phys_mag_classification": phys_mag,
        },
        attribute_coupling=([tok["attribute"]] if tok.get("attribute") else []),
        canonical_source="elrond/research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json",
        provenance_tag="weapon_form_lookup_v1.0_cycle10",
        visibility_at_default_zoom=False,  # 277 tokens — drillable zoom-in
    )

# ============================================================================
# Additional families per atomic-substrate-registry — SCHEMA-only enumeration
# (per dispatch § 2.3 — counts authoritative; full enumeration awaits future work)
# ============================================================================

# 1.15 — Weapon-substrate property primitives (cultural_lineage 14-enum)
CULTURAL_TRADITIONS = [
    "germanic_medieval", "celtic_norse", "francophone_medieval", "italianate_renaissance",
    "iberian_medieval", "byzantine_eastern_roman", "islamic_classical", "indo_persian",
    "chinese_jianghu", "japanese_feudal", "korean_classical", "southeast_asian",
    "mesoamerican_pre_columbian", "andean_pre_columbian",
]
for tradition in CULTURAL_TRADITIONS:
    add_primitive(
        primitive_id=f"cultural_tradition_{tradition}",
        primitive_family="cultural_tradition",
        primitive_label=tradition.replace("_", " ").title(),
        canonical_source="canonical/story/weapon-substrate-conclusion-declaration.md + "
                         "weapon library cultural_lineage_canonical enum",
        provenance_tag="cultural_lineage_canonical_v1",
        visibility_at_default_zoom=False,
        notes="Per atomic-substrate-registry § 1.15; count target 14 per dispatch § 2.3",
    )

# Historical-period 9-enum (per registry § 1.15 + historical_period_canonical enum)
HISTORICAL_PERIODS = [
    "antiquity_pre_roman", "classical_antiquity", "late_antiquity_migration",
    "early_medieval", "high_medieval", "late_medieval", "renaissance", "early_modern",
    "industrial_to_modern",
]
for period in HISTORICAL_PERIODS:
    add_primitive(
        primitive_id=f"historical_period_{period}",
        primitive_family="historical_period",
        primitive_label=period.replace("_", " ").title(),
        canonical_source="weapon library historical_period_canonical enum",
        provenance_tag="historical_period_canonical_v1",
        visibility_at_default_zoom=False,
        notes="Per atomic-substrate-registry § 1.15; count target 9 per dispatch § 2.3",
    )

# Register 6-enum (per registry § 1.15 + register_canonical enum)
REGISTERS = ["formal_courtly", "martial_professional", "common_folk_utility",
             "ceremonial_religious", "scholarly_arcane", "outlaw_subaltern"]
for register in REGISTERS:
    add_primitive(
        primitive_id=f"register_{register}",
        primitive_family="register",
        primitive_label=register.replace("_", " ").title(),
        canonical_source="weapon library register_canonical enum",
        provenance_tag="register_canonical_v1",
        visibility_at_default_zoom=False,
        notes="Per atomic-substrate-registry § 1.15; count target 6 per dispatch § 2.3",
    )

# 1.16 — Off-hand item substrate primitives (7 estimate per off-hand-items doc)
OFF_HAND_TYPES = ["shield", "ammo_pouch", "focus_orb", "off_hand_weapon_form",
                  "tome_grimoire", "censer", "buckler"]
for oh in OFF_HAND_TYPES:
    add_primitive(
        primitive_id=f"off_hand_{oh}",
        primitive_family="off_hand_substrate",
        primitive_label=oh.replace("_", " ").title(),
        canonical_source="canonical/story/off-hand-items-2026-05-24.md",
        provenance_tag="off_hand_substrate_v1",
        visibility_at_default_zoom=False,
        notes="Per atomic-substrate-registry § 1.16; parallel substrate to main weapon",
    )

# 1.17 / 1.18 — Race + racial trait primitives (SCHEMA only; default-randomized per dispatch § 2.3)
# Per atomic-substrate-registry: per-season race-set authoring; default randomized
# For Phase A cosmograph: render a Tolkien S1 illustrative race-set (per registry § 1.19 example)
TOLKIEN_S1_RACES = [
    ("hobbit", ["shadow", "wind"], ["DEX"]),
    ("elf", ["wind", "holy", "water"], ["DEX", "WIS"]),
    ("dwarf", ["earth", "fire", "physical"], ["STR"]),
    ("man", ["physical", "holy"], ["STR", "WIS"]),
    ("wizard", ["fire", "lightning"], ["INT", "WIS"]),
]
for race_id, elem_aff, attr_aff in TOLKIEN_S1_RACES:
    add_primitive(
        primitive_id=f"race_tolkien_s1_{race_id}",
        primitive_family="race_primitive",
        primitive_label=f"Tolkien {race_id.title()}",
        substrate_fingerprint={
            "race_set_id": "tolkien_s1",
            "race_substrate_anchor": "Tolkien-medieval",
            "race_element_affinity_illustrative": elem_aff,
            "race_attribute_affinity_illustrative": attr_aff,
        },
        element_coupling=elem_aff,
        attribute_coupling=attr_aff,
        canonical_source="canonical/story/2026-06-06-atomic-substrate-registry.md § 1.17-1.20 "
                         "(SCHEMA only; Tolkien S1 illustrative race-set per § 1.19 example)",
        provenance_tag="race_set_tolkien_s1_illustrative_schema_only",
        visibility_at_default_zoom=True,
        notes="SCHEMA-only enumeration per atomic-substrate-registry. Default-randomized "
              "when no season-design selected; per-season per-race affinity authored at "
              "season-design time. Tolkien S1 illustrative used for Phase A.",
    )

# ============================================================================
# Write primitive_registry_v0.json
# ============================================================================

registry_path = OUTPUT_DIR / "primitive_registry_v0.json"
with open(registry_path, "w") as f:
    json.dump(
        {
            "_meta": {
                "version": "0.1.0",
                "phase": "Phase 0 — primitive vocabulary enumeration",
                "authored_by": "elrond",
                "authored_date": datetime.now().strftime("%Y-%m-%d"),
                "dispatch": "agentic_orchestration/dispatches/"
                            "2026-06-06-elrond-cosmograph-substrate-trace-extraction.md",
                "verdict": "agentic_orchestration/gandalf/notes/"
                           "2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md",
                "total_primitives": len(primitives),
                "by_family": {},
                "weapon_form_token_substrate_honesty": {
                    "phys_count": phys_count,
                    "mag_count": mag_count,
                    "unclassified_count": unclass_count,
                    "phys_ratio_at_classified": round(phys_ratio_at_classified, 4),
                    "phys_ratio_at_token_level_pct": round(phys_count / len(wf_tokens) * 100, 2),
                    "mag_ratio_at_token_level_pct": round(mag_count / len(wf_tokens) * 100, 2),
                    "note": ("Surface A per verdict § 2.1: render substrate-honest ratio. "
                             "Kit-roster element-axis-coverage ratio (Surface B, 40-45/55-60) "
                             "lives at Phase 2, not weapon-form-token enumeration."),
                },
            },
            "primitives": primitives,
        },
        f, indent=2,
    )

# Populate family counts
from collections import Counter
family_counts = Counter(p["primitive_family"] for p in primitives)

# Re-write with family counts populated (cleaner round-trip)
with open(registry_path) as f:
    registry_blob = json.load(f)
registry_blob["_meta"]["by_family"] = dict(family_counts)
with open(registry_path, "w") as f:
    json.dump(registry_blob, f, indent=2)

print(f"Wrote {registry_path}")
print(f"Total primitives: {len(primitives)}")
print("By family:")
for fam, cnt in family_counts.most_common():
    print(f"  {fam}: {cnt}")

# ============================================================================
# region_labels_v0.json — ambient navigation overlays per dispatch § 2.6
# ============================================================================

region_labels = {
    "_meta": {
        "version": "0.1.0",
        "phase": "Phase 0 — region labels v0",
        "note": ("Per dispatch § 2.6 — ambient navigation overlays, NOT first-class stars. "
                 "Emergent mechanic-family labels DEFERRED to Phase 3 (read from clustering)."),
    },
    "bc_bin_labels": {
        "source": "canonical/story/qd-engine-bc-axes-lock-2026-05-20.md § 2",
        "total_bins": 34,
        "axes": {
            "axis_1_engagement_profile": ["close-fast", "close-slow", "mid-fast", "mid-slow",
                                          "ranged-fast", "ranged-slow"],
            "axis_2_damage_geometry": ["single-target", "small-AOE", "large-AOE", "chain",
                                       "multi-spawn"],
            "axis_2A_proxy_density": ["solo", "proxy-light", "proxy-heavy"],
            "axis_2B_control_density": ["damage-pure", "mixed", "control-pure"],
            "axis_3A_damage_tempo": ["low", "medium", "high"],
            "axis_3B_damage_amplitude_variance": ["flat", "variable", "spiky"],
            "axis_4_defensive_profile": ["tank", "mitigator", "dodger", "glass"],
            "axis_5_resource_economy": ["HP-economy", "charge-stack", "damage-taken-converts",
                                        "starved", "overflow", "generator-spender", "steady"],
        },
        "total_cells": 68040,
    },
    "skill_tree_tier_labels": {
        "source": "canonical/47-damage-scaling-architecture-2026-05-27.md",
        "tiers": ["T1_rotation", "T2_beta_pair", "T3_build_defining", "T4_capstone"],
    },
    "scaling_pattern_per_tier_labels": {
        "source": "canonical/47-damage-scaling-architecture-2026-05-27.md § 1.7",
        "patterns": ["additive (T1)", "additive_plus_multiplicative (T2)",
                     "multiplicative (T3)", "transformative (T4)"],
    },
    "emergent_mechanic_family_labels": {
        "status": "DEFERRED to Phase 3 — read from clustering",
        "note": ("Per Matt 2026-06-06 substrate-led correction: no pre-imposed family "
                 "taxonomy. Clustering emerges from UMAP embedding in Phase 3."),
    },
    "chain_architecture_labels": {
        "source": "canonical/40-gear-balance-guide-architecture-2026-05-26.md D83",
        "architectures": ["3_chain (2 T4 capstone chains + 1 supporting T3-only)",
                          "4_chain (3 T4 capstone chains + 1 supporting T3-only)"],
    },
}

region_labels_path = OUTPUT_DIR / "region_labels_v0.json"
with open(region_labels_path, "w") as f:
    json.dump(region_labels, f, indent=2)

print()
print(f"Wrote {region_labels_path}")
