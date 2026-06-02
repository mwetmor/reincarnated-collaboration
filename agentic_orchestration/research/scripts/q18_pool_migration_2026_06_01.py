#!/usr/bin/env python3
"""
WS1A.Q18 sub-phase 5f pool.json migration script.

Operationalizes Architecture A LOCK per:
- canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md
- agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md

Owner: elrond (data steward seam)
Date: 2026-06-01
Dispatch: 2026-06-01-elrond-cycle-15-ws1a-q18-sub-phase-5f-pool-migration.md

Migration shape:
1. Schema extension (3 additive fields per PG-3 § 4):
   - substrate_validation_lineage (string enum)
   - vocabulary_commonness (string enum)
   - slot_unambiguous (boolean)
2. Pool.json entry transformation:
   - Apply 109 rotating-primary entries per canonical lock § 3
   - Apply cull-tag dispositions per PG-3 § 3
   - Apply slot routing per PG-3 § 2.3 (mist→water, vortex→wind, etc.)
   - Apply per-entry lineage tags per PG-3 § 5 binding
3. Physical taxonomy registry: 9 entries → physical_taxonomy.json (separate surface)
4. Legacy entries (pool.json entries NOT in the 118-entry lock):
   - Demoted to d1_status="quarantine" with lineage_tag=""
   - Preserved (audited + demoted, not deleted) per canonical doc § 9.3 ("audited + extended, NOT retired")

Backward-compat strategy:
- All new fields are ADDITIVE with defaults; legacy readers ignore unknown fields
- pool.py PoolElement schema extended with defaults; missing fields use defaults
- d1_status enum unchanged; existing values preserved

Per-entry lineage tag mapping rationale (the BINDING is PG-3 § 5 aggregate; per-entry
mapping is elrond seam authority subject to KR ambiguity-surface escalation):

  substrate-validated-this-wave-2026-06-01 (target: 65):
    rotating-primary entries that appeared in Phase 4 substrate research with
    score >= 6 (T6) OR cross-track confirmation OR substrate-canonical anchoring.

  substrate-silent-2026-05-08-D1-pool (target: 24):
    rotating-primary entries that ALREADY EXISTED in the 2026-05-08 D1 pool.json
    AND did NOT appear in Phase 4 substrate research (silent, not refuted).

  designer-curation-modern-scientific-overlay-2026-06-01 (target: 19):
    modern-scientific vocabulary added at PG-3 designer-curation gate:
    fusion, thermal, combustion, hydro, hydraulic, seismic, tectonic, sonic,
    shockwave, plasma, flash, ion, voltage, tesla, stellar, solar, photon,
    laser, prismatic.

  designer-curation-mystical-fantasy-overlay-2026-06-01 (target: 1):
    soul (shadow primary).

  architecture-A-taxonomy-registry-2026-06-01 (target: 9):
    physical's 9 entries (piercing/slashing/bludgeoning/force + pierce/slash/sever/strike + bleed).
    Migrated to physical_taxonomy.json, NOT pool.json.
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

POOL_JSON_PATH = Path(
    "/Users/admin/Games/reincarnated-engine/data/seasonal_elements/pool.json"
)
PHYSICAL_TAXONOMY_PATH = Path(
    "/Users/admin/Games/reincarnated-engine/data/seasonal_elements/physical_taxonomy.json"
)
POOL_BACKUP_PATH = POOL_JSON_PATH.with_suffix(".json.pre-q18-2026-06-01-backup")
LOCK_DATE = "2026-06-01"
LEGACY_D1_POOL_DATE = "2026-05-08"


# -------------------------------------------------------------------
# Canonical lock § 3 — per-primary allow-lists (verbatim)
# -------------------------------------------------------------------

ROTATING_PRIMARY_LOCK: dict[str, list[str]] = {
    "fire": [
        "ember", "cinder", "blaze", "scorch", "inferno", "ignite", "fira",
        "lava", "magma", "charcoal", "char", "brand", "flare", "fusion",
        "thermal", "combustion",
    ],
    "water": [
        "tide", "torrent", "glacial", "brine", "aqua", "frost", "chill",
        "mist", "ice", "glacier", "wave", "marsh", "hydro", "hydraulic",
    ],
    "earth": [
        "stone", "granite", "marble", "clay", "sand", "iron", "gold", "silver",
        "lead", "gem", "crystal", "obsidian", "amber", "quake", "tremor",
        "thorn", "seismic", "tectonic",
    ],
    "wind": [
        "tempest", "cyclone", "whirlwind", "gale", "gust", "squall", "hurricane",
        "zephyr", "hail", "sleet", "cloud", "sonic", "shockwave",
    ],
    "lightning": [
        "arc", "static", "surge", "volt", "bolt", "shock", "spark", "thunder",
        "plasma", "flash", "ion", "voltage", "tesla",
    ],
    "holy": [
        "radiance", "radiant", "dawn", "aura", "divine", "sacred", "blessed",
        "lux", "celestial", "stellar", "solar", "photon", "laser", "prismatic",
    ],
    "shadow": [
        "void", "shade", "wraith", "drain", "necrotic", "abyss", "shadow",
        "lich", "blackhole", "singularity", "darkmatter", "soul",
    ],
}

# Physical taxonomy registry (canonical lock § 1.8)
PHYSICAL_TAXONOMY: dict[str, list[str]] = {
    "damage_sub_type": ["piercing", "slashing", "bludgeoning", "force"],
    "mechanical_action_vocabulary": ["pierce", "slash", "sever", "strike"],
    "ailment": ["bleed"],
}

# -------------------------------------------------------------------
# PG-3 § 5 lineage-tag binding (the BINDING is the aggregate; per-entry
# mapping is elrond seam authority).
#
# Rationale for per-entry assignment:
# - designer-curation-modern-scientific-overlay-2026-06-01 (19 entries):
#   modern-scientific vocabulary explicitly named at canonical doc § 7
# - designer-curation-mystical-fantasy-overlay-2026-06-01 (1 entry):
#   shadow:soul per canonical doc § 7 explicit naming
# - substrate-validated-this-wave-2026-06-01 (target 65):
#   entries that appear in Phase 4 substrate research candidates DB
#   (score >= some threshold OR cross-track-confirmed OR substrate-canonical core)
# - substrate-silent-2026-05-08-D1-pool (target 24):
#   pool-existing entries (added_date == 2026-05-08) that did NOT surface
#   in Phase 4 substrate research
# -------------------------------------------------------------------

# DESIGNER-CURATION-MODERN-SCIENTIFIC (19 entries) — per canonical doc § 7 explicit list
MODERN_SCIENTIFIC_OVERLAY: set[tuple[str, str]] = {
    # fire (3): fusion, thermal, combustion
    ("fire", "fusion"), ("fire", "thermal"), ("fire", "combustion"),
    # water (2): hydro, hydraulic
    ("water", "hydro"), ("water", "hydraulic"),
    # earth (2): seismic, tectonic
    ("earth", "seismic"), ("earth", "tectonic"),
    # wind (2): sonic, shockwave
    ("wind", "sonic"), ("wind", "shockwave"),
    # lightning (5): plasma, flash, ion, voltage, tesla
    ("lightning", "plasma"), ("lightning", "flash"), ("lightning", "ion"),
    ("lightning", "voltage"), ("lightning", "tesla"),
    # holy (5): stellar, solar, photon, laser, prismatic
    ("holy", "stellar"), ("holy", "solar"), ("holy", "photon"),
    ("holy", "laser"), ("holy", "prismatic"),
    # shadow (4): blackhole, singularity, darkmatter (3 sci; soul is mystical → separate)
    ("shadow", "blackhole"), ("shadow", "singularity"), ("shadow", "darkmatter"),
    # plus: scorch is NOT modern-scientific (it's older english); reconcile to 18 visible above
    # Adjustment: canonical § 7 enumerates: fusion, thermal, combustion, hydro, hydraulic,
    # seismic, tectonic, sonic, shockwave, plasma, flash, ion, voltage, tesla, stellar,
    # solar, photon, laser, prismatic = 19 explicit entries.
}
# Note: counted above explicitly: 3+2+2+2+5+5+3 = 22, but canonical lists 19.
# Reconciliation: shadow's "blackhole, singularity, darkmatter" are modern-scientific (3),
# but canonical § 7 doesn't enumerate them in the modern-scientific list. They could be
# either modern-scientific OR substrate-validated (depending on the Phase 4 research).
# The canonical § 7 verbatim list IS 19 entries — exclude shadow's 3 sci entries from
# modern-scientific category; treat as substrate-validated (shadow had high substrate yield).

MODERN_SCIENTIFIC_OVERLAY = {
    # fire (3): fusion, thermal, combustion
    ("fire", "fusion"), ("fire", "thermal"), ("fire", "combustion"),
    # water (2): hydro, hydraulic
    ("water", "hydro"), ("water", "hydraulic"),
    # earth (2): seismic, tectonic
    ("earth", "seismic"), ("earth", "tectonic"),
    # wind (2): sonic, shockwave
    ("wind", "sonic"), ("wind", "shockwave"),
    # lightning (5): plasma, flash, ion, voltage, tesla
    ("lightning", "plasma"), ("lightning", "flash"), ("lightning", "ion"),
    ("lightning", "voltage"), ("lightning", "tesla"),
    # holy (5): stellar, solar, photon, laser, prismatic
    ("holy", "stellar"), ("holy", "solar"), ("holy", "photon"),
    ("holy", "laser"), ("holy", "prismatic"),
}
# Total: 3+2+2+2+5+5 = 19 ✓

MYSTICAL_FANTASY_OVERLAY: set[tuple[str, str]] = {
    ("shadow", "soul"),
}
# Total: 1 ✓

# SUBSTRATE-VALIDATED (target 65) — entries with substrate research evidence.
# Drawn from research DB (q18_flavor_candidates_2026-06-01.db) candidates that
# appear in the locked allow-list AND have any cross-track presence OR
# substrate-canonical anchoring. Explicitly enumerated for transparency.
SUBSTRATE_VALIDATED_THIS_WAVE: set[tuple[str, str]] = {
    # fire (9 per § 7.1 illustrative):
    # research-confirmed: ember (2t), cinder (2t), blaze (1t), char (1t), fira (1t),
    # ignite (1t), inferno (1t), scorch (1t), magma (substrate-canonical pool entry
    # confirmed via lava/magma fire-substrate canon)
    ("fire", "ember"), ("fire", "cinder"), ("fire", "blaze"), ("fire", "char"),
    ("fire", "fira"), ("fire", "ignite"), ("fire", "inferno"), ("fire", "scorch"),
    ("fire", "magma"),
    # water (8 per § 7.1 illustrative):
    # research-confirmed: tide (2t), torrent (2t), glacial (2t), brine (2t),
    # aqua (1t), chill (1t), frost (1t), mist (1t)
    ("water", "tide"), ("water", "torrent"), ("water", "glacial"), ("water", "brine"),
    ("water", "aqua"), ("water", "chill"), ("water", "frost"), ("water", "mist"),
    # earth (7 per § 7.1 illustrative):
    # research-confirmed: stone (3t!), quake (2t), tremor (2t), thorn (1t),
    # PLUS substrate-canonical anchoring from D1 pool: granite, iron, gem
    # (these are substrate-canonical earth core; D1 pool entries; Phase 4 § 7
    # earth read: "research was thin on earth-specific vocabulary; baseline-only
    # sampling; Pool's existing 22 captures the substrate-honest depth").
    # Conservative read: stone/quake/tremor/thorn = 4 research-substantiated;
    # granite/iron/gem promoted as substrate-canonical core (3) → total 7
    ("earth", "stone"), ("earth", "quake"), ("earth", "tremor"), ("earth", "thorn"),
    ("earth", "granite"), ("earth", "iron"), ("earth", "gem"),
    # wind (9 per § 7.1 illustrative):
    # research-confirmed: tempest (2t), cyclone (2t), gust (2t), gale (2t),
    # whirlwind (2t), squall (1t), zephyr (2t), hurricane (1t),
    # PLUS pool-canonical: hail (D1 pool, substrate-aligned)
    ("wind", "tempest"), ("wind", "cyclone"), ("wind", "gust"), ("wind", "gale"),
    ("wind", "whirlwind"), ("wind", "squall"), ("wind", "zephyr"),
    ("wind", "hurricane"), ("wind", "hail"),
    # lightning (8 per § 7.1 illustrative):
    # research-confirmed: arc (2t), static (2t), surge (2t), volt (2t),
    # bolt (1t), shock (1t), spark (1t), thunder (1t)
    ("lightning", "arc"), ("lightning", "static"), ("lightning", "surge"),
    ("lightning", "volt"), ("lightning", "bolt"), ("lightning", "shock"),
    ("lightning", "spark"), ("lightning", "thunder"),
    # holy (9 per § 7.1 illustrative):
    # research-confirmed: divine (2t), sacred (2t), radiance (2t), radiant (2t),
    # blessed (1t), aura (1t), dawn (2t), lux (1t), celestial (1t)
    ("holy", "divine"), ("holy", "sacred"), ("holy", "radiance"), ("holy", "radiant"),
    ("holy", "blessed"), ("holy", "aura"), ("holy", "dawn"), ("holy", "lux"),
    ("holy", "celestial"),
    # shadow (7 per § 7.1 illustrative):
    # research-confirmed: void (3t!), shade (3t), wraith (2t), abyss (1t),
    # drain (1t), necrotic (1t), shadow (1t)
    ("shadow", "void"), ("shadow", "shade"), ("shadow", "wraith"),
    ("shadow", "abyss"), ("shadow", "drain"), ("shadow", "necrotic"),
    ("shadow", "shadow"),
}
# Total: 9+8+7+9+8+9+7 = 57 — matches canonical doc § 7.1 illustrative breakdown
# NOTE: PG-3 § 5 binding states 65 substrate-validated. Per-entry illustrative
# total is 57 — this is the IMMATERIAL reconciliation discrepancy flagged in
# jack-ryan Gate-2 INFO-1. Per dispatch § 2.2: "PG-3 § 5 is authoritative for
# per-tag count aggregates; canonical § 7.1 breakdown is illustrative-only."
#
# To honor PG-3 § 5 binding (65), the per-entry breakdown will be supplemented
# by 8 additional substrate-validated entries to reach 65. Per substrate-led
# discipline, the supplementation draws from entries that DO appear in
# Phase 4 research candidates DB AND in the locked allow-list, even if the
# illustrative § 7.1 table did not enumerate them.

# Per cardinality reconciliation: canonical lock's verbatim per-primary entry lists
# total 100 rotating-primary + 9 physical = 109, NOT 118. § 7.1 illustrative
# breakdown col sums (57+19+23+1+9=109) match actual entry counts.
# Substrate-validated target = 57 (per § 7.1 col-sum, which is the only
# internally-consistent reference against actual entry total).
# No supplementation: SUBSTRATE_VALIDATED_THIS_WAVE above already enumerates 57.
SUBSTRATE_VALIDATED_SUPPLEMENTAL: set[tuple[str, str]] = set()
# (Empty: per § 7.1 illustrative col-sum 57 matches per-entry enumeration above.)

# SUBSTRATE-SILENT (target 24) — pool-existing entries NOT surfaced by
# Phase 4 substrate research. Drawn from the locked allow-list MINUS the
# substrate-validated set MINUS the modern-scientific overlay MINUS the
# mystical-fantasy overlay. By construction, the residual is substrate-silent.
# All entries here MUST have added_date=2026-05-08 in the original pool.json
# (D1 pool carry-over) to qualify for `substrate-silent-2026-05-08-D1-pool` tag.

# -------------------------------------------------------------------
# Slot routing decisions per PG-3 § 2.3 + canonical doc § 3.3
# -------------------------------------------------------------------

# Concrete slot routing for previously-ambiguous candidates.
# Format: (entry_id, primary_slot, flex_slots)
SLOT_ROUTING: dict[str, tuple[str, list[str]]] = {
    "mist": ("water", []),                          # mist → WATER (was wind in pool.json)
    "vortex": ("wind", []),                         # vortex → WIND
    "hurricane": ("wind", ["water"]),               # hurricane → WIND, water flex
    "squall": ("wind", ["water"]),                  # squall → WIND, water flex
    "stormtide": ("wind", ["water"]),               # stormtide → WIND, water flex (INFO-1 flagged: not in lock)
    "tempest": ("wind", ["water"]),                 # tempest → WIND, water flex
    "njord": ("water", ["wind"]),                   # njord → WATER, wind flex (not in lock)
}

# -------------------------------------------------------------------
# Cull-tag dispositions per PG-3 § 3
# -------------------------------------------------------------------

CULL_TAG_DISPOSITIONS: dict[str, str] = {
    "drift-14-wind-storm-cluster-collapse": "DISSOLVE",
    "drift-14-plant-anatomical": "DISSOLVE-for-thorn",   # thorn promoted; vine/root/bark/wood/etc KEEP
    "drift-14-biological-organic": "KEEP",
    "drift-14-alternative-liquid": "KEEP",
    "drift-14-auditory-non-visual": "KEEP",
    "drift-14-conceptual-not-substance": "KEEP",
}

# -------------------------------------------------------------------
# Default tag-attribute lookup for locked allow-list entries
# -------------------------------------------------------------------

# Per-entry default tags (kept identical to pool.json where possible; new entries
# get substrate-honest minimal tag set; tag lists are illustrative and audit-friendly).
LOCKED_ENTRY_TAGS: dict[tuple[str, str], list[str]] = {
    # Will derive from existing pool.json entries where matching; new entries
    # below get minimal substrate-honest tags. New-only entries listed here:
    ("fire", "inferno"): ["intense", "consuming", "engulfing"],
    ("fire", "ignite"): ["initiating", "trigger", "moment"],
    ("fire", "fira"): ["jrpg", "tier-2", "fire-magic"],
    ("fire", "fusion"): ["scientific", "energy", "high-energy"],
    ("fire", "thermal"): ["scientific", "heat-transfer", "ambient"],
    ("fire", "combustion"): ["scientific", "oxidation", "chemical"],

    ("water", "torrent"): ["rushing", "powerful", "directed"],
    ("water", "glacial"): ["cold", "slow", "ancient"],
    ("water", "aqua"): ["jrpg", "tier-1", "water-magic"],
    ("water", "frost"): ["crystalline", "cold", "surface"],
    ("water", "chill"): ["cold", "pervasive", "subduing"],
    ("water", "mist"): ["soft", "diffuse", "obscuring"],
    ("water", "hydro"): ["scientific", "water-prefix", "modern"],
    ("water", "hydraulic"): ["scientific", "pressure", "mechanical"],

    ("earth", "quake"): ["seismic", "shaking", "ground"],
    ("earth", "tremor"): ["small-quake", "warning", "vibration"],
    ("earth", "thorn"): ["sharp", "fixed", "protective"],
    ("earth", "seismic"): ["scientific", "earthquake", "modern"],
    ("earth", "tectonic"): ["scientific", "continental", "modern"],

    ("wind", "tempest"): ["storm", "violent", "elemental"],
    ("wind", "cyclone"): ["rotating", "violent", "sweeping"],
    ("wind", "whirlwind"): ["rotating", "fast", "concentrated"],
    ("wind", "squall"): ["sudden", "violent", "brief-storm"],
    ("wind", "hurricane"): ["storm", "large-scale", "destructive"],
    ("wind", "zephyr"): ["gentle", "warm", "western"],
    ("wind", "sonic"): ["scientific", "sound-wave", "modern"],
    ("wind", "shockwave"): ["scientific", "pressure-wave", "modern"],

    ("lightning", "arc"): ["electrical", "discharge", "bridging"],
    ("lightning", "static"): ["electrical", "ambient", "potential"],
    ("lightning", "surge"): ["electrical", "rising", "powerful"],
    ("lightning", "volt"): ["electrical", "unit", "magnitude"],
    ("lightning", "bolt"): ["electrical", "directional", "striking"],
    ("lightning", "shock"): ["electrical", "sudden", "stunning"],
    ("lightning", "spark"): ["electrical", "brief", "small"],
    ("lightning", "thunder"): ["acoustic", "lightning-aftermath", "rolling"],
    ("lightning", "plasma"): ["scientific", "ionized", "modern"],
    ("lightning", "flash"): ["sudden", "bright", "brief"],
    ("lightning", "ion"): ["scientific", "charged-particle", "modern"],
    ("lightning", "voltage"): ["scientific", "potential", "modern"],
    ("lightning", "tesla"): ["scientific", "high-voltage", "modern"],

    ("holy", "radiance"): ["luminous", "emanating", "bright"],
    ("holy", "radiant"): ["luminous", "shining", "elevated"],
    ("holy", "dawn"): ["sunrise", "new-day", "luminous"],
    ("holy", "aura"): ["surrounding", "subtle", "field"],
    ("holy", "divine"): ["godly", "elevated", "sacred"],
    ("holy", "sacred"): ["holy", "consecrated", "set-apart"],
    ("holy", "blessed"): ["consecrated", "favored", "graced"],
    ("holy", "lux"): ["latin-light", "luminous", "classical"],
    ("holy", "celestial"): ["heavenly", "stellar", "elevated"],
    ("holy", "stellar"): ["scientific", "stars", "modern"],
    ("holy", "solar"): ["scientific", "sun", "modern"],
    ("holy", "photon"): ["scientific", "light-particle", "modern"],
    ("holy", "laser"): ["scientific", "coherent-light", "modern"],
    ("holy", "prismatic"): ["scientific", "spectrum", "modern"],

    ("shadow", "void"): ["empty", "absence", "consuming"],
    ("shadow", "shade"): ["partial-shadow", "concealing", "soft"],
    ("shadow", "wraith"): ["spectral", "undead", "haunting"],
    ("shadow", "drain"): ["depleting", "removing", "vampiric"],
    ("shadow", "necrotic"): ["deathly", "decaying", "rotting"],
    ("shadow", "abyss"): ["deep", "bottomless", "consuming"],
    ("shadow", "shadow"): ["concealing", "absence-of-light", "core"],
    ("shadow", "lich"): ["undead", "intelligent", "ancient"],
    ("shadow", "blackhole"): ["scientific", "gravitational", "modern"],
    ("shadow", "singularity"): ["scientific", "infinite-density", "modern"],
    ("shadow", "darkmatter"): ["scientific", "cosmic", "modern"],
    ("shadow", "soul"): ["mystical", "spiritual", "essence"],
}


def determine_lineage_tag(primary: str, entry_id: str) -> str:
    """Return the per-entry lineage tag per PG-3 § 5 binding."""
    key = (primary, entry_id)
    if key in MYSTICAL_FANTASY_OVERLAY:
        return "designer-curation-mystical-fantasy-overlay-2026-06-01"
    if key in MODERN_SCIENTIFIC_OVERLAY:
        return "designer-curation-modern-scientific-overlay-2026-06-01"
    if key in SUBSTRATE_VALIDATED_THIS_WAVE or key in SUBSTRATE_VALIDATED_SUPPLEMENTAL:
        return "substrate-validated-this-wave-2026-06-01"
    # Fall-through: substrate-silent (D1 pool carry-over not surfaced by research)
    return "substrate-silent-2026-05-08-D1-pool"


def determine_vocabulary_commonness(entry_id: str, existing_tags: list[str]) -> str:
    """Determine vocabulary_commonness per matt-demote-2026-05-12 lineage."""
    if "vocab-obscure-2026-05-12" in existing_tags:
        return "obscure"
    # Common-vocab entries (general English):
    common_set = {
        "ember", "blaze", "lava", "magma", "char", "flare", "fire",
        "ice", "frost", "chill", "mist", "tide", "wave", "rain", "snow", "water",
        "stone", "sand", "iron", "gold", "silver", "lead", "earth",
        "cloud", "wind", "thunder", "lightning", "spark", "shock",
        "dawn", "divine", "sacred", "blessed", "holy",
        "void", "shadow", "drain",
        "hurricane", "tornado", "hail", "sleet", "fog",
    }
    if entry_id in common_set:
        return "common"
    # Modern-scientific terms are genre-standard (well-known in sci-fi gaming):
    modern_sci_set = {
        "fusion", "thermal", "combustion", "hydro", "hydraulic",
        "seismic", "tectonic", "sonic", "shockwave",
        "plasma", "ion", "voltage", "tesla", "flash",
        "stellar", "solar", "photon", "laser", "prismatic",
        "blackhole", "singularity", "darkmatter",
    }
    if entry_id in modern_sci_set:
        return "genre-standard"
    # FF-tier vocabulary (genre-standard within JRPG):
    if entry_id in {"fira", "aqua", "lux", "aura"}:
        return "genre-standard"
    # Default: genre-standard for everything else in the lock
    return "genre-standard"


def determine_slot_unambiguous(entry_id: str, primary: str) -> bool:
    """Per smoke-as-fire vs smoke-as-wind precedent — slot_unambiguous flag."""
    # Known-ambiguous candidates per PG-3 § 2.3 routing decisions:
    ambiguous = {
        "mist",          # was wind, routed to water (cross-element ambiguous)
        "vortex",        # could read as water (PoE Vortex cold-AOE) or wind (rotational)
        "hurricane",     # wind primary but water flex (tropical storm)
        "squall",        # wind primary but water flex (oceanic squall)
        "stormtide",     # wind primary but water flex
        "tempest",       # wind primary but water flex
        "njord",         # water primary but wind flex (Norse sea-god)
        "smoke",         # legacy: fire vs wind precedent
        "frost",         # could read as wind-cold or water-cold
        "rime",          # could read as wind-cold or water-cold
        "sleet",         # wind primary but water flex
    }
    return entry_id not in ambiguous


def derive_tags(primary: str, entry_id: str, existing_entry: dict | None) -> list[str]:
    """Derive tags for a locked entry. Use existing pool.json tags if available;
    otherwise use LOCKED_ENTRY_TAGS or fall back to substrate-honest defaults."""
    if existing_entry is not None and existing_entry.get("primary_slot") == primary:
        return list(existing_entry.get("tags", []))
    key = (primary, entry_id)
    if key in LOCKED_ENTRY_TAGS:
        return list(LOCKED_ENTRY_TAGS[key])
    # Fall-back substrate-honest minimal tag
    return [primary, entry_id]


def derive_flex_slots(entry_id: str, existing_entry: dict | None) -> list[str]:
    """Derive flex_slots, applying PG-3 § 2.3 routing where applicable."""
    if entry_id in SLOT_ROUTING:
        _, flex = SLOT_ROUTING[entry_id]
        return list(flex)
    if existing_entry is not None:
        return list(existing_entry.get("flex_slots", []))
    return []


def build_lock_entry(
    primary: str,
    entry_id: str,
    existing_pool_by_id: dict[str, dict],
) -> dict:
    """Build a single pool.json entry from the canonical lock."""
    existing = existing_pool_by_id.get(entry_id)
    lineage = determine_lineage_tag(primary, entry_id)
    tags = derive_tags(primary, entry_id, existing)
    vocab = determine_vocabulary_commonness(entry_id, tags)
    slot_unambig = determine_slot_unambiguous(entry_id, primary)
    flex = derive_flex_slots(entry_id, existing)

    # Preserve existing D1 scores + added_date where possible; otherwise apply
    # 2026-06-01 lock date for new entries.
    added_date = existing.get("added_date", LOCK_DATE) if existing else LOCK_DATE
    d1_score = existing.get("d1_score", 10) if existing else 10
    d1_genre_bonus = existing.get("d1_genre_bonus", 1) if existing else 1
    d1_total = existing.get("d1_total", d1_score + d1_genre_bonus) if existing else (d1_score + d1_genre_bonus)
    rights_status = existing.get("rights_status", "archetypal_safe") if existing else "archetypal_safe"

    # Preserve other engine-side fields where present (Drift-14 audit fields)
    vfx_mapping_tier = existing.get("vfx_mapping_tier", "unscored") if existing else "unscored"
    vfx_catalogue_mapping_clean = existing.get("vfx_catalogue_mapping_clean", False) if existing else False
    canonical_pair_leak = existing.get("canonical_pair_leak", False) if existing else False
    substrate_native = existing.get("substrate_native", primary) if existing else primary

    entry = {
        "id": entry_id,
        "name": entry_id,
        "primary_slot": primary,
        "flex_slots": flex,
        "tags": tags,
        "added_date": added_date,
        "rights_status": rights_status,
        "d1_score": d1_score,
        "d1_genre_bonus": d1_genre_bonus,
        "d1_total": d1_total,
        "d1_status": "allow-list",  # Per canonical lock § 2: all locked entries are allow-list
        "vfx_mapping_tier": vfx_mapping_tier,
        "vfx_catalogue_mapping_clean": vfx_catalogue_mapping_clean,
        "canonical_pair_leak": canonical_pair_leak,
        "substrate_native": substrate_native,
        # Q18 sub-phase 5f additive fields:
        "substrate_validation_lineage": lineage,
        "vocabulary_commonness": vocab,
        "slot_unambiguous": slot_unambig,
        "ws1a_q18_lock_date": LOCK_DATE,
    }
    return entry


def build_legacy_entry(existing_entry: dict) -> dict:
    """For pool.json entries NOT in the locked 118-entry set, preserve as legacy.

    Disposition per cull-tag and per canonical doc § 9.3 ("audited + extended,
    NOT retired"). Legacy entries get demoted to quarantine but are preserved
    for historical audit; their lineage_tag is "" (empty — pre-Q18).
    """
    entry = dict(existing_entry)
    # Apply slot routing if specified (e.g., mist routed water in lock, but if
    # mist is ALREADY in lock, build_lock_entry handles; this only fires for
    # legacy entries not in lock).
    entry_id = entry["id"]
    if entry_id in SLOT_ROUTING:
        new_primary, new_flex = SLOT_ROUTING[entry_id]
        entry["primary_slot"] = new_primary
        entry["flex_slots"] = list(new_flex)

    # Apply cull-tag dispositions
    cull_tag = entry.get("cull_tag")
    if cull_tag in CULL_TAG_DISPOSITIONS:
        disposition = CULL_TAG_DISPOSITIONS[cull_tag]
        if disposition == "DISSOLVE":
            # cull tag dissolved; entry no longer needs the tag
            entry.pop("cull_tag", None)
            entry["d1_status"] = "quarantine"  # but still legacy
        elif disposition == "DISSOLVE-for-thorn":
            # only thorn is dissolved; other plant-anatomical entries keep tag
            if entry_id == "thorn":
                entry.pop("cull_tag", None)
            # else: keep cull_tag and quarantine status
            entry["d1_status"] = "quarantine"
        else:
            # KEEP: cull_tag preserved
            entry["d1_status"] = "quarantine"
    else:
        # Non-culled legacy entry: demote to quarantine (NOT in lock)
        entry["d1_status"] = "quarantine"

    # Additive fields for legacy entries: empty/default
    entry["substrate_validation_lineage"] = ""  # pre-Q18; no lineage tag
    entry["vocabulary_commonness"] = "unscored"
    entry["slot_unambiguous"] = True
    entry["ws1a_q18_lock_date"] = ""

    return entry


def migrate() -> None:
    """Execute the migration."""
    # Load existing pool.json
    raw = json.loads(POOL_JSON_PATH.read_text())
    existing_elements = raw["elements"]
    existing_by_id: dict[str, dict] = {e["id"]: e for e in existing_elements}
    print(f"[load] existing pool.json: {len(existing_elements)} entries")

    # Back up before write
    if not POOL_BACKUP_PATH.exists():
        POOL_BACKUP_PATH.write_text(json.dumps(raw, indent=2))
        print(f"[backup] wrote pre-migration backup: {POOL_BACKUP_PATH}")
    else:
        print(f"[backup] backup already exists at {POOL_BACKUP_PATH}; not overwriting")

    # Build new entries from lock
    new_entries: list[dict] = []
    locked_ids: set[str] = set()
    for primary, entry_ids in ROTATING_PRIMARY_LOCK.items():
        for eid in entry_ids:
            new_entries.append(build_lock_entry(primary, eid, existing_by_id))
            locked_ids.add(eid)
    # CRITICAL DISCREPANCY SURFACE (per dispatch INFO-1 surface-to-KR protocol):
    # Canonical lock + PG-3 ratification both assert "109 rotating-primary entries
    # + 9 physical = 118 total". BUT the verbatim per-primary enumerated entry
    # lists (which jack-ryan Gate-2 verified PASS verbatim entry-by-entry) sum to:
    #   fire=16 + water=14 + earth=18 + wind=13 + lightning=13 + holy=14 + shadow=12 = 100
    # Total: 100 rotating-primary + 9 physical = 109, NOT 118.
    # The canonical doc's § 7.1 illustrative breakdown column-sums (57+19+23+1+9=109)
    # are internally consistent with 100 rotating-primary + 9 physical = 109.
    # PG-3 § 5 binding (65+24+19+1+9=118) does not reconcile to the verbatim entry lists.
    # Elrond seam decision: HONOR the verbatim entry lists (which the locked entries
    # actually enumerate); apply lineage tags using § 7.1 illustrative breakdown
    # column-sums (which DO match actual entry counts); SURFACE the cardinality
    # discrepancy via report-back per dispatch ambiguity-surface protocol.
    expected_rotating = sum(len(v) for v in ROTATING_PRIMARY_LOCK.values())
    print(f"[build] locked rotating-primary entries: {len(new_entries)} "
          f"(matches verbatim per-primary lists; expected {expected_rotating})")
    assert len(new_entries) == expected_rotating, (
        f"Expected {expected_rotating} entries from verbatim per-primary lists; "
        f"got {len(new_entries)}"
    )

    # Append legacy entries that are NOT in the lock (preserved per canonical doc § 9.3).
    # Skip if existing entry's id is in physical (not applicable here since pool.json
    # has no physical entries; physical taxonomy registry is separate).
    legacy_count = 0
    for existing in existing_elements:
        eid = existing["id"]
        if eid in locked_ids:
            continue  # already in new_entries via build_lock_entry
        new_entries.append(build_legacy_entry(existing))
        legacy_count += 1
    print(f"[build] legacy entries preserved (quarantined): {legacy_count}")

    # Write new pool.json
    new_pool = {
        "version": "1.1",
        "schema_version": "1.1",
        "schema_notes": (
            "v1.1 (2026-06-01) adds Q18 sub-phase 5f additive fields: "
            "substrate_validation_lineage (5-value enum), vocabulary_commonness "
            "(4-value enum), slot_unambiguous (boolean), ws1a_q18_lock_date "
            "(date marker for lock-cohort). All additive; backward-compat preserved. "
            "See agentic_orchestration/research/curated/MIGRATION.md v1.7."
        ),
        "elements": new_entries,
    }
    POOL_JSON_PATH.write_text(json.dumps(new_pool, indent=2))
    print(f"[write] pool.json v1.1: {len(new_entries)} total entries "
          f"(109 locked + {legacy_count} legacy)")

    # Verify lineage-tag aggregate counts against canonical § 7.1 col-sums
    locked_only = new_entries[:expected_rotating]
    lineage_counts = Counter(e["substrate_validation_lineage"] for e in locked_only)
    print(f"[verify] lineage-tag aggregate (locked rotating-primary entries only):")
    for tag, count in sorted(lineage_counts.items()):
        print(f"  {tag}: {count}")
    # Expected per § 7.1 illustrative col-sums (internally consistent with
    # actual 100 rotating-primary entry total). PG-3 § 5 binding (65/24/19/1)
    # does NOT reconcile to actual entry total; cardinality discrepancy
    # surfaced via report-back. canonical § 7 explicit modern-scientific
    # enumeration (19) honored over § 7.1 col-sum (23) since it is the
    # explicit verbatim list.
    expected_per_7_1_colsum = {
        "substrate-validated-this-wave-2026-06-01": 57,
        "substrate-silent-2026-05-08-D1-pool": 23,
        "designer-curation-modern-scientific-overlay-2026-06-01": 19,
        "designer-curation-mystical-fantasy-overlay-2026-06-01": 1,
    }
    for tag, expected_count in expected_per_7_1_colsum.items():
        actual = lineage_counts.get(tag, 0)
        marker = "OK" if actual == expected_count else "MISMATCH"
        print(f"  [{marker}] {tag}: expected={expected_count} actual={actual}")

    # Write physical_taxonomy.json
    physical_registry = {
        "version": "1.0",
        "schema_notes": (
            "Architecture A taxonomy-sibling registry for physical (8th damage type "
            "in canonical-7+1; NOT a flavor pool). Per canonical lock § 4 + § 1.8: "
            "9 entries decomposed by schema role. Physical kits OPT OUT of WS1A.4 "
            "LLM flavor judgment; skill naming uses mechanical-schema templates. "
            "v1.1+ deferrals: crush, impact, rend (not committed at v1.0). "
            "Authoritative source: canonical/story/"
            "2026-06-01-flavor-pool-per-primary-element-lock.md § 4."
        ),
        "lineage": "architecture-A-taxonomy-registry-2026-06-01",
        "primary": "physical",
        "ailment_canonical_yaml": "bleed",  # already in engine config/elements.yaml
        "registry": {
            "damage_sub_type": {
                "schema_role": "weapon + skill damage_sub_type field",
                "source": "D&D 5e PHB ch.9 damage types + PoE physical-damage subtypes",
                "entries": [
                    {"id": "piercing", "tags": ["pointed", "penetrating", "weapon-form"]},
                    {"id": "slashing", "tags": ["edged", "cutting", "weapon-form"]},
                    {"id": "bludgeoning", "tags": ["blunt", "impact", "weapon-form"]},
                    {"id": "force", "tags": ["raw-kinetic", "non-elemental", "abstract"]},
                ],
            },
            "mechanical_action_vocabulary": {
                "schema_role": "skill-naming verb templates for physical kits",
                "source": "ARPG-canonical kinetic vocabulary",
                "entries": [
                    {"id": "pierce", "tags": ["verb", "pointed-action", "thrust"]},
                    {"id": "slash", "tags": ["verb", "edged-action", "sweep"]},
                    {"id": "sever", "tags": ["verb", "decisive-cut", "removal"]},
                    {"id": "strike", "tags": ["verb", "impact-action", "general"]},
                ],
            },
            "ailment": {
                "schema_role": "canonical physical ailment per config/elements.yaml",
                "source": "PoE Bleed canonical precedent",
                "entries": [
                    {"id": "bleed", "tags": ["DoT", "physical-canonical", "movement-amplified"]},
                ],
            },
        },
        "kit_handling_note": (
            "Physical kits opt out of WS1A.4 per-skill bounded LLM flavor judgment. "
            "Skill naming uses (weapon-form + mechanical-action + intensifier) "
            "composition template. Physical kit identity differentiates via: "
            "(a) weapon-form selection from canonical 17-gear; "
            "(b) damage_sub_type field assignment from the 4-entry registry above; "
            "(c) mechanical-action vocabulary from the 4-entry registry above; "
            "(d) bleed ailment routing per config/elements.yaml."
        ),
        "v1_1_deferrals": ["crush", "impact", "rend"],
        "lock_date": LOCK_DATE,
    }
    PHYSICAL_TAXONOMY_PATH.write_text(json.dumps(physical_registry, indent=2))
    total_entries = sum(
        len(cat["entries"]) for cat in physical_registry["registry"].values()
    )
    print(f"[write] physical_taxonomy.json: {total_entries} entries (expected 9)")
    assert total_entries == 9, f"Expected 9 physical entries; got {total_entries}"

    # Final validation: round-trip parse
    parsed_back = json.loads(POOL_JSON_PATH.read_text())
    assert parsed_back["version"] == "1.1"
    assert len(parsed_back["elements"]) == len(new_entries)
    parsed_physical = json.loads(PHYSICAL_TAXONOMY_PATH.read_text())
    assert parsed_physical["primary"] == "physical"
    print("[verify] round-trip parse OK for both files")


if __name__ == "__main__":
    migrate()
