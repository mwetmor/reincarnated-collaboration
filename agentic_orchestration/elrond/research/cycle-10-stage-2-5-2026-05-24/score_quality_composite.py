#!/usr/bin/env python3
"""
Cycle 10 Stage 2.5 — Per-row quality / uniqueness / flavor composite scoring + Tier S/A/B/C assignment.

Owner: elrond (substrate seam — scoring + DB write)
Dispatch: agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md

Signals (9 total; weights sum to 1.0):
  1. source_library_reputation_tier   weight 0.20   gandalf-curated lookup
  2. description_richness             weight 0.15   description_text + structured props
  3. extracted_provenance_richness    weight 0.10   Stage 1.5 column directly
  4. extracted_named_bearer_presence  weight 0.15   Stage 1.5 non-NULL bonus
  5. extracted_materials_richness     weight 0.10   Stage 1.5 multi-material / rare exotics
  6. cultural_lineage_depth           weight 0.10   tags + genre_appearances + related_entries
  7. image_presence                   weight 0.05   knowledge_entry_reference_images JOIN
  8. cluster_centrality               weight 0.10   cluster_membership.confidence_score
  9. cultural_tradition_weight        weight 0.05   gandalf-curated Fate-genre lookup

Tier assignment (post-scoring; empirical thresholds):
  S — top 1% OR named_mythological_match in seed list (gandalf seed Tier 1+2; Mode-C contamination filtered out)
  A — top 10% (excluding S)
  B — standard pool
  C — bottom quartile

Cultural-sensitivity gate at Tier S: Tier 3 entries excluded by seed list at extraction time (Stage 1.5);
Stage 2.5 verifies no Tier 3 contamination at Tier S auto-include.

Discipline #25 Mode-C contamination filter: rows with rep_audit_mode_c_naming_allusion_suspected flag
in named-bearer-matches.json do NOT get Tier S auto-include via named-mythological-match path;
must qualify via top-1% composite score instead.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
NAMED_BEARER_MATCHES_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/research/"
    "cycle-10-stage-1-5-2026-05-24/named-bearer-matches.json"
)
GANDALF_SEED_LIST_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/"
    "2026-05-24-named-historical-figure-seed-list.md"
)
GANDALF_REPUTATION_TIER_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/"
    "2026-05-24-source-library-reputation-tier.md"
)
GANDALF_CULTURAL_WEIGHT_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/"
    "2026-05-24-cultural-tradition-weight-lookup.md"
)
OUTPUT_DIR = (
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/research/"
    "cycle-10-stage-2-5-2026-05-24"
)

# -------------------------------------------------------------------
# Weights
# -------------------------------------------------------------------
WEIGHTS = {
    "source_library_reputation_tier": 0.20,
    "description_richness": 0.15,
    "extracted_provenance_richness": 0.10,
    "extracted_named_bearer_presence": 0.15,
    "extracted_materials_richness": 0.10,
    "cultural_lineage_depth": 0.10,
    "image_presence": 0.05,
    "cluster_centrality": 0.10,
    "cultural_tradition_weight": 0.05,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "weights must sum to 1.0"


# -------------------------------------------------------------------
# Fallback lookups (used when gandalf prep not landed)
# -------------------------------------------------------------------
# Source-library reputation default tier mapping (elrond fallback).
# Tiers: museum_curated=1.00, designer_curated=0.75, community_scraped=0.50, game_data_dump=0.30
FALLBACK_REPUTATION = {
    "met-museum": ("museum_curated", 1.00),
    "royal_armouries": ("museum_curated", 1.00),
    "wikidata": ("designer_curated", 0.75),
    "wikipedia": ("designer_curated", 0.75),
    "odin-army-tradoc": ("designer_curated", 0.70),
    "army-recognition": ("designer_curated", 0.70),
    "nick-aschenbach-dnd-data": ("community_scraped", 0.50),
    "bsdata-warhammer-aos": ("community_scraped", 0.50),
    "5e-bits-5e-database": ("community_scraped", 0.50),
    "5e-bits-5e-database-2024": ("community_scraped", 0.50),
    "path-of-exile-repoe": ("community_scraped", 0.50),
    "bloqhead-demigods": ("community_scraped", 0.45),
    "fextralife-elden-ring": ("community_scraped", 0.45),
    "fextralife-ds1": ("community_scraped", 0.45),
    "fextralife-ds2": ("community_scraped", 0.45),
    "fextralife-ds3": ("community_scraped", 0.45),
    "elden-ring-erdb": ("community_scraped", 0.45),
    "osrsbox-db": ("game_data_dump", 0.30),
    "wow-classic-items": ("game_data_dump", 0.30),
    "cataclysm-dda": ("game_data_dump", 0.30),
    "diablo2-d2data": ("game_data_dump", 0.30),
    "gta-v-data": ("game_data_dump", 0.30),
    "pf2ools-pf2ools-data-quarantined": ("game_data_dump", 0.25),
    "souls-api-thomaslincoln": ("game_data_dump", 0.30),
    "souls-api-thomaslincoln-quarantined": ("game_data_dump", 0.25),
}

# Cultural-tradition Fate-genre weight fallback (elrond placeholder; uniform 0.5).
# Gandalf prep will provide canonical values.
FALLBACK_CULTURAL_WEIGHT = {
    "european": 0.65,
    "east_asian": 0.65,
    "cross_cultural": 0.55,
    "middle_eastern": 0.55,
    "south_asian": 0.55,
    "southeast_asian": 0.50,
    "african": 0.50,
    "south_american_indigenous": 0.45,
    "mesoamerican": 0.45,
    "arctic_circumpolar": 0.40,
    "oceanic": 0.45,
    "north_american_indigenous": 0.40,
    "fantasy_generic": 0.35,
    "sci_fi_generic": 0.30,
    "unknown": 0.30,
}
DEFAULT_CULTURAL_WEIGHT = 0.40

# Materials rarity scoring — common bulk vs exotic/heroic.
RARE_MATERIAL_TERMS = {
    "jade", "obsidian", "mithril", "adamantine", "adamantium", "orichalcum",
    "meteoric", "meteorite", "dragonbone", "starsteel", "moonsilver", "elven steel",
    "damascus", "wootz", "tamahagane", "celestial bronze", "ivory", "amber", "lapis",
    "lapis lazuli", "rock crystal", "rock-crystal", "rock crystal", "platinum",
    "ruby", "sapphire", "emerald", "diamond", "pearl", "ebony", "rosewood",
    "narwhal", "whalebone", "horn", "shagreen", "ray skin", "rayskin",
}
COMMON_MATERIAL_TERMS = {
    "steel", "iron", "wood", "leather", "bronze", "copper", "cloth", "stone",
    "metal", "rope", "plastic",
}


# -------------------------------------------------------------------
# Gandalf seed-list parser (YAML embedded in markdown)
# -------------------------------------------------------------------
def parse_seed_list(path: str) -> dict[str, dict[str, Any]]:
    """Parse the gandalf seed list YAML block.

    Returns dict: name_lowercase -> {tradition, tier, priority, aliases, notes}.
    Includes aliases as separate keys pointing to same entry.
    """
    if not os.path.exists(path):
        return {}

    with open(path) as f:
        text = f.read()

    # Extract YAML block between ```yaml ... ```
    m = re.search(r"```yaml\s*(.*?)```", text, re.DOTALL)
    if not m:
        return {}

    yaml_text = m.group(1)

    # Simple regex-based parser of the entry lines
    # Pattern: - {name: "Arthur", aliases: ["..."], tier: 1, regex_priority: low, notes: "..."}
    entry_re = re.compile(
        r"-\s*\{name:\s*\"([^\"]+)\",\s*aliases:\s*\[([^\]]*)\],\s*tier:\s*(\d+),\s*regex_priority:\s*(\w+),\s*notes:\s*\"([^\"]*)\"\}"
    )
    tradition_re = re.compile(r'tradition_tag:\s*"([^"]+)"')

    entries: dict[str, dict[str, Any]] = {}
    current_tradition = None

    for line in yaml_text.splitlines():
        tmatch = tradition_re.search(line)
        if tmatch:
            current_tradition = tmatch.group(1)
            continue
        ematch = entry_re.search(line)
        if ematch and current_tradition:
            name = ematch.group(1)
            aliases_str = ematch.group(2)
            tier = int(ematch.group(3))
            priority = ematch.group(4)
            notes = ematch.group(5)

            aliases = []
            for a in re.findall(r'"([^"]+)"', aliases_str):
                aliases.append(a)

            data = {
                "name": name,
                "tradition": current_tradition,
                "tier": tier,
                "priority": priority,
                "aliases": aliases,
                "notes": notes,
            }
            entries[name.lower().strip()] = data
            for alias in aliases:
                entries[alias.lower().strip()] = data

    return entries


# -------------------------------------------------------------------
# Mode-C flag extraction from match log JSON
# -------------------------------------------------------------------
def load_mode_c_flagged_ids(path: str) -> set[int]:
    """Load row IDs flagged with rep_audit_mode_c_naming_allusion_suspected from the Stage 1.5 match log."""
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        data = json.load(f)

    mode_c_ids: set[int] = set()
    for entry in data:
        for m in entry.get("pass_b_seed_matches", []):
            flag = m.get("rep_audit_flag")
            if flag and "mode_c_naming_allusion" in str(flag):
                mode_c_ids.add(int(entry["id"]))
                break

    return mode_c_ids


# -------------------------------------------------------------------
# Gandalf-prep readers (placeholder-aware)
# -------------------------------------------------------------------
def load_reputation_tier_lookup(path: str) -> dict[str, tuple[str, float]] | None:
    """Load gandalf source-library reputation tier lookup.

    Returns None if file not landed.
    Expected file: gandalf multi-line YAML block within markdown, with entries like:
        - source_library: "met-museum"
          reputation_tier: "A"
          numeric_score: 1.0
          reasoning: |
            ...
    """
    if not os.path.exists(path):
        return None

    with open(path) as f:
        text = f.read()

    # Extract YAML code block
    m = re.search(r"```yaml\s*(.*?)```", text, re.DOTALL)
    if not m:
        return None

    yaml_text = m.group(1)

    # Walk block-by-block: an entry is a 4-line group starting with `- source_library:`
    # capturing source_library, reputation_tier, numeric_score
    lookup: dict[str, tuple[str, float]] = {}
    current: dict[str, Any] = {}
    for line in yaml_text.splitlines():
        m_sl = re.match(r"\s*-\s*source_library:\s*\"([^\"]+)\"", line)
        if m_sl:
            if current.get("source_library") and "numeric_score" in current:
                lookup[current["source_library"]] = (
                    current.get("reputation_tier", "unknown"),
                    float(current["numeric_score"]),
                )
            current = {"source_library": m_sl.group(1)}
            continue
        m_rt = re.match(r"\s*reputation_tier:\s*\"([^\"]+)\"", line)
        if m_rt and current:
            current["reputation_tier"] = m_rt.group(1)
            continue
        m_ns = re.match(r"\s*numeric_score:\s*([0-9.]+)", line)
        if m_ns and current:
            current["numeric_score"] = float(m_ns.group(1))
            continue

    # Flush last entry
    if current.get("source_library") and "numeric_score" in current:
        lookup[current["source_library"]] = (
            current.get("reputation_tier", "unknown"),
            float(current["numeric_score"]),
        )

    return lookup if lookup else None


def load_cultural_weight_lookup(path: str) -> dict[str, dict[str, Any]] | None:
    """Load gandalf cultural-tradition Fate-genre weight lookup.

    Returns dict: lineage -> {weight, tier, excluded_from_tier_s} or None if not landed.
    Parses gandalf multi-line YAML block with entries like:
        - cultural_lineage_canonical: "european"
          fate_genre_weight: 1.0
          tier: 1
          excluded_from_tier_s: false
          reasoning: |
            ...
    """
    if not os.path.exists(path):
        return None

    with open(path) as f:
        text = f.read()

    m = re.search(r"```yaml\s*(.*?)```", text, re.DOTALL)
    if not m:
        return None

    yaml_text = m.group(1)

    lookup: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] = {}
    for line in yaml_text.splitlines():
        m_lin = re.match(r"\s*-\s*cultural_lineage_canonical:\s*\"([^\"]+)\"", line)
        if m_lin:
            if current.get("lineage"):
                lookup[current["lineage"]] = {
                    "weight": current.get("weight", DEFAULT_CULTURAL_WEIGHT),
                    "tier": current.get("tier", 1),
                    "excluded_from_tier_s": current.get("excluded_from_tier_s", False),
                }
            current = {"lineage": m_lin.group(1)}
            continue
        m_w = re.match(r"\s*fate_genre_weight:\s*([0-9.]+)", line)
        if m_w and current:
            current["weight"] = float(m_w.group(1))
            continue
        m_t = re.match(r"\s*tier:\s*(\d+)", line)
        if m_t and current:
            current["tier"] = int(m_t.group(1))
            continue
        m_e = re.match(r"\s*excluded_from_tier_s:\s*(true|false)", line)
        if m_e and current:
            current["excluded_from_tier_s"] = (m_e.group(1) == "true")
            continue

    if current.get("lineage"):
        lookup[current["lineage"]] = {
            "weight": current.get("weight", DEFAULT_CULTURAL_WEIGHT),
            "tier": current.get("tier", 1),
            "excluded_from_tier_s": current.get("excluded_from_tier_s", False),
        }

    return lookup if lookup else None


# -------------------------------------------------------------------
# Per-row signal computation
# -------------------------------------------------------------------
def normalize_log(value: float, scale: float = 500.0) -> float:
    """Log-scale normalization: maps 0 -> 0, scale -> ~0.6, 5*scale -> ~0.97, capped at 1.0."""
    if value <= 0:
        return 0.0
    return min(1.0, math.log1p(value) / math.log1p(scale * 2))


def compute_description_richness(desc_text: str | None, structured_props: str | None) -> float:
    """Compose description_text length + structured-property field density."""
    text_len = len(desc_text) if desc_text else 0

    # Field density from structured_properties JSON
    field_count = 0
    if structured_props:
        try:
            data = json.loads(structured_props)
            if isinstance(data, dict):
                # Count non-null leaf values
                def _count(obj):
                    n = 0
                    if isinstance(obj, dict):
                        for v in obj.values():
                            n += _count(v)
                    elif isinstance(obj, list):
                        for v in obj:
                            n += _count(v)
                    elif obj not in (None, "", []):
                        n += 1
                    return n
                field_count = _count(data)
        except (json.JSONDecodeError, TypeError):
            pass

    # Compose: 70% length, 30% field density
    text_score = normalize_log(text_len, scale=500.0)
    field_score = min(1.0, field_count / 20.0)
    return 0.70 * text_score + 0.30 * field_score


def compute_named_bearer_signal(extracted_named_bearer: str | None) -> float:
    """Non-NULL bonus for Stage 1.5 named-bearer extraction."""
    if extracted_named_bearer and extracted_named_bearer.strip():
        return 1.0
    return 0.0


def compute_materials_richness(materials_json: str | None) -> float:
    """Multi-material count + rare-exotic flag scoring."""
    if not materials_json:
        return 0.0

    try:
        materials = json.loads(materials_json)
    except (json.JSONDecodeError, TypeError):
        return 0.0

    if not isinstance(materials, list) or not materials:
        return 0.0

    material_strs = [str(m).lower().strip() for m in materials if m]
    if not material_strs:
        return 0.0

    # Count rare and common
    n_rare = sum(1 for m in material_strs if any(rare in m for rare in RARE_MATERIAL_TERMS))
    n_total = len(material_strs)
    n_common = sum(1 for m in material_strs if any(c in m for c in COMMON_MATERIAL_TERMS))

    # Base: multi-material count (more materials = richer)
    count_score = min(1.0, n_total / 5.0)
    # Rare-material bonus
    rare_score = min(1.0, n_rare * 0.5)
    # Common-only penalty
    if n_rare == 0 and n_total <= 1 and n_common >= 1:
        count_score *= 0.5

    return 0.6 * count_score + 0.4 * rare_score


def compute_cultural_lineage_depth(
    cultural_lineage_tags: str | None,
    genre_appearances: str | None,
    related_entries: str | None,
) -> float:
    """Sum normalized depths of three lineage-context columns."""
    def _count_array(val: str | None) -> int:
        if not val:
            return 0
        try:
            parsed = json.loads(val)
            if isinstance(parsed, list):
                return len(parsed)
            if isinstance(parsed, dict):
                return len(parsed)
        except (json.JSONDecodeError, TypeError):
            # Try semicolon-separated fallback
            return len([s for s in val.split(";") if s.strip()])
        return 0

    n_tags = _count_array(cultural_lineage_tags)
    n_genre = _count_array(genre_appearances)
    n_related = _count_array(related_entries)

    # Each component caps at 1.0 around ~3-5 entries
    tags_score = min(1.0, n_tags / 3.0)
    genre_score = min(1.0, n_genre / 3.0)
    related_score = min(1.0, n_related / 5.0)

    return 0.4 * tags_score + 0.3 * genre_score + 0.3 * related_score


def compute_cluster_centrality_score(confidence_score: float | None) -> float:
    """cluster_membership.confidence_score is already 0-1; higher = closer to centroid."""
    if confidence_score is None:
        return 0.0
    return max(0.0, min(1.0, float(confidence_score)))


# -------------------------------------------------------------------
# Main scoring pipeline
# -------------------------------------------------------------------
def score_all_rows(use_gandalf_prep: bool = False, verbose: bool = True) -> dict[str, Any]:
    """Compute composite scores + tier assignments for all rows.

    Returns summary dict for output reporting.
    """
    t_start = time.time()

    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] Loading inputs...")

    # Load gandalf seed list (for Tier S match metadata)
    seed_list = parse_seed_list(GANDALF_SEED_LIST_PATH)
    if verbose:
        print(f"  seed list entries (incl. aliases): {len(seed_list)}")

    # Load Mode-C flagged IDs
    mode_c_ids = load_mode_c_flagged_ids(NAMED_BEARER_MATCHES_PATH)
    if verbose:
        print(f"  Mode-C flagged IDs: {len(mode_c_ids)}")

    # Load gandalf prep lookups (if present)
    reputation_lookup = (
        load_reputation_tier_lookup(GANDALF_REPUTATION_TIER_PATH) if use_gandalf_prep else None
    )
    cultural_weight_lookup = (
        load_cultural_weight_lookup(GANDALF_CULTURAL_WEIGHT_PATH) if use_gandalf_prep else None
    )

    gandalf_rep_status = "LANDED" if reputation_lookup else "FALLBACK"
    gandalf_cw_status = "LANDED" if cultural_weight_lookup else "FALLBACK"
    if verbose:
        print(f"  gandalf reputation tier: {gandalf_rep_status} ({len(reputation_lookup) if reputation_lookup else len(FALLBACK_REPUTATION)} entries)")
        print(f"  gandalf cultural weight: {gandalf_cw_status} ({len(cultural_weight_lookup) if cultural_weight_lookup else len(FALLBACK_CULTURAL_WEIGHT)} entries)")

    # Effective lookups
    rep_lookup = reputation_lookup or {k: v for k, v in FALLBACK_REPUTATION.items()}

    # Cultural weight lookup: gandalf format is {weight, tier, excluded_from_tier_s} dicts;
    # fallback format is float weights only. Unify access via two helper dicts.
    cw_weight: dict[str, float] = {}
    cw_excluded_tier_s: dict[str, bool] = {}
    if cultural_weight_lookup:
        for lineage, info in cultural_weight_lookup.items():
            cw_weight[lineage] = info["weight"]
            cw_excluded_tier_s[lineage] = info["excluded_from_tier_s"]
    else:
        for lineage, w in FALLBACK_CULTURAL_WEIGHT.items():
            cw_weight[lineage] = w
            # Fallback: assume Tier 3 exclusion for indigenous + african per Sketch F § 6.3
            cw_excluded_tier_s[lineage] = lineage in {
                "north_american_indigenous",
                "arctic_circumpolar",
                "oceanic",
                "mesoamerican",
                "south_american_indigenous",
                "african",
            }

    n_tier_3_excluded_lineages = sum(1 for v in cw_excluded_tier_s.values() if v)
    if verbose:
        print(f"  Tier-3-excluded lineages (no Tier S auto-include): {n_tier_3_excluded_lineages}")

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Pre-load cluster_membership confidence scores
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] Pre-loading cluster_membership...")
    cluster_conf: dict[int, float] = {}
    for row in cur.execute(
        "SELECT knowledge_entry_id, MAX(confidence_score) AS conf FROM cluster_membership GROUP BY knowledge_entry_id"
    ):
        cluster_conf[row["knowledge_entry_id"]] = row["conf"]
    if verbose:
        print(f"  cluster_membership rows: {len(cluster_conf)}")

    # Pre-load image counts
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] Pre-loading image counts...")
    image_counts: dict[int, int] = defaultdict(int)
    for row in cur.execute(
        "SELECT knowledge_entry_id, COUNT(*) AS n FROM knowledge_entry_reference_images GROUP BY knowledge_entry_id"
    ):
        image_counts[row["knowledge_entry_id"]] = row["n"]
    if verbose:
        print(f"  rows with images: {len(image_counts)}")

    # Pre-compute total counts for normalization (max image count)
    max_image_count = max(image_counts.values()) if image_counts else 1
    if verbose:
        print(f"  max images per entry: {max_image_count}")

    # Stream rows, compute composite scores
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] Streaming rows + computing composite scores...")

    select_cols = [
        "id", "canonical_name", "source_library", "description_text", "structured_properties",
        "cultural_lineage_tags", "genre_appearances", "related_entries",
        "cultural_lineage_canonical",
        "extracted_materials", "extracted_named_bearer", "extracted_provenance_richness",
    ]
    cur.execute(f"SELECT {', '.join(select_cols)} FROM weapon_knowledge_entries")

    scores: list[tuple[int, float, str | None]] = []  # (id, composite, named_match_name or None)
    signal_distributions: dict[str, list[float]] = defaultdict(list)
    n_total = 0
    n_named_bearer_match = 0
    n_mode_c_blocked = 0
    n_tier_3_lineage_blocked = 0  # Tier-3 lineage with apparent seed match blocked from Tier S path

    for row in cur:
        rid = row["id"]
        n_total += 1

        # Signal 1: source-library reputation tier
        src = row["source_library"] or ""
        rep_tuple = rep_lookup.get(src, ("unknown", 0.30))
        # Handle both fallback (tuple) and gandalf (tuple) formats
        if isinstance(rep_tuple, tuple):
            sig_rep = rep_tuple[1]
        else:
            sig_rep = float(rep_tuple)

        # Signal 2: description richness
        sig_desc = compute_description_richness(row["description_text"], row["structured_properties"])

        # Signal 3: provenance richness (Stage 1.5 column)
        sig_prov = row["extracted_provenance_richness"] or 0.0

        # Signal 4: named-bearer presence
        sig_bearer = compute_named_bearer_signal(row["extracted_named_bearer"])

        # Signal 5: materials richness
        sig_mat = compute_materials_richness(row["extracted_materials"])

        # Signal 6: cultural lineage depth
        sig_lineage = compute_cultural_lineage_depth(
            row["cultural_lineage_tags"], row["genre_appearances"], row["related_entries"]
        )

        # Signal 7: image presence
        n_img = image_counts.get(rid, 0)
        sig_img = min(1.0, n_img / 3.0)  # 0 -> 0; 1 -> 0.33; 3+ -> 1.0

        # Signal 8: cluster centrality
        sig_centrality = compute_cluster_centrality_score(cluster_conf.get(rid))

        # Signal 9: cultural-tradition weight
        lineage = row["cultural_lineage_canonical"] or "unknown"
        sig_cw = cw_weight.get(lineage, DEFAULT_CULTURAL_WEIGHT)

        # Composite
        composite = (
            WEIGHTS["source_library_reputation_tier"] * sig_rep
            + WEIGHTS["description_richness"] * sig_desc
            + WEIGHTS["extracted_provenance_richness"] * sig_prov
            + WEIGHTS["extracted_named_bearer_presence"] * sig_bearer
            + WEIGHTS["extracted_materials_richness"] * sig_mat
            + WEIGHTS["cultural_lineage_depth"] * sig_lineage
            + WEIGHTS["image_presence"] * sig_img
            + WEIGHTS["cluster_centrality"] * sig_centrality
            + WEIGHTS["cultural_tradition_weight"] * sig_cw
        )

        # Track signal distributions (sample 5K rows for memory)
        if n_total % 18 == 0:
            signal_distributions["source_library_reputation_tier"].append(sig_rep)
            signal_distributions["description_richness"].append(sig_desc)
            signal_distributions["extracted_provenance_richness"].append(sig_prov)
            signal_distributions["extracted_named_bearer_presence"].append(sig_bearer)
            signal_distributions["extracted_materials_richness"].append(sig_mat)
            signal_distributions["cultural_lineage_depth"].append(sig_lineage)
            signal_distributions["image_presence"].append(sig_img)
            signal_distributions["cluster_centrality"].append(sig_centrality)
            signal_distributions["cultural_tradition_weight"].append(sig_cw)
            signal_distributions["composite"].append(composite)

        # Named mythological match (Tier S auto-include candidate)
        # Three gates:
        #   (1) seed-list match on extracted_named_bearer
        #   (2) NOT in Mode-C contamination set (Stage 1.5 rep_audit_flag)
        #   (3) NOT in Tier-3-excluded cultural_lineage_canonical (per gandalf cultural-weight lookup)
        named_match = None
        bearer = row["extracted_named_bearer"]
        if bearer:
            bearer_low = bearer.lower().strip()
            seed_entry = seed_list.get(bearer_low)
            if seed_entry is None:
                # Try cleaning trailing parenthetical / period
                bearer_clean = re.sub(r"\s*\([^)]*\)\s*$", "", bearer_low).strip()
                bearer_clean = bearer_clean.rstrip(".,;:")
                seed_entry = seed_list.get(bearer_clean)
            if seed_entry:
                # Gate 2: Mode-C contamination
                if rid in mode_c_ids:
                    n_mode_c_blocked += 1
                # Gate 3: Tier-3-excluded lineage (cultural-sensitivity per Sketch F § 6.3)
                elif cw_excluded_tier_s.get(lineage, False):
                    n_tier_3_lineage_blocked += 1
                else:
                    named_match = f"{seed_entry['name']} ({seed_entry['tradition']}, tier_{seed_entry['tier']})"
                    n_named_bearer_match += 1

        scores.append((rid, composite, named_match))

    elapsed_signal = time.time() - t_start
    if verbose:
        print(f"  scored {n_total} rows in {elapsed_signal:.1f}s")
        print(f"  named-mythological-match (all gates cleared): {n_named_bearer_match}")
        print(f"  Mode-C contamination blocked from Tier S match path: {n_mode_c_blocked}")
        print(f"  Tier-3-lineage blocked from Tier S match path: {n_tier_3_lineage_blocked}")

    # -------------------------------------------------------------
    # Tier assignment — empirical thresholds
    # -------------------------------------------------------------
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] Computing empirical tier thresholds...")

    composite_only = sorted([s[1] for s in scores], reverse=True)
    n = len(composite_only)
    threshold_S = composite_only[int(n * 0.01)] if n > 100 else composite_only[0]
    threshold_A = composite_only[int(n * 0.10)] if n > 100 else composite_only[0]
    threshold_C = composite_only[int(n * 0.75)] if n > 100 else composite_only[-1]

    if verbose:
        print(f"  threshold S (top 1%): {threshold_S:.4f}")
        print(f"  threshold A (top 10%): {threshold_A:.4f}")
        print(f"  threshold C (bottom 25%): {threshold_C:.4f}")

    # Assign tiers
    tier_counts = defaultdict(int)
    tier_assignments: list[tuple[int, str, str | None]] = []
    tier_s_samples: list[tuple[int, str | None]] = []  # for Tier S preview
    tier_s_named_match = 0
    tier_s_top_pct = 0

    for rid, composite, named_match in scores:
        tier: str
        if named_match is not None:
            tier = "S"
            tier_s_named_match += 1
        elif composite >= threshold_S:
            tier = "S"
            tier_s_top_pct += 1
        elif composite >= threshold_A:
            tier = "A"
        elif composite >= threshold_C:
            tier = "B"
        else:
            tier = "C"
        tier_counts[tier] += 1
        tier_assignments.append((rid, tier, named_match))
        if tier == "S" and len(tier_s_samples) < 50:
            tier_s_samples.append((rid, named_match))

    if verbose:
        print(f"  Tier S total: {tier_counts['S']}  (named-match: {tier_s_named_match}, top-1%: {tier_s_top_pct})")
        print(f"  Tier A: {tier_counts['A']}")
        print(f"  Tier B: {tier_counts['B']}")
        print(f"  Tier C: {tier_counts['C']}")

    # -------------------------------------------------------------
    # Write back to DB in batches
    # -------------------------------------------------------------
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] Writing scores + tiers to DB...")

    write_rows = []
    for (rid, composite, _), (rid2, tier, named_match) in zip(scores, tier_assignments, strict=True):
        assert rid == rid2
        write_rows.append((composite, tier, named_match, rid))

    cur.executemany(
        "UPDATE weapon_knowledge_entries SET quality_composite_score = ?, quality_tier = ?, named_mythological_match = ? WHERE id = ?",
        write_rows,
    )
    conn.commit()

    if verbose:
        print(f"  wrote {len(write_rows)} rows")

    conn.close()

    total_elapsed = time.time() - t_start
    if verbose:
        print(f"[{time.strftime('%H:%M:%S')}] DONE in {total_elapsed:.1f}s total")

    return {
        "n_total": n_total,
        "tier_counts": dict(tier_counts),
        "tier_s_named_match": tier_s_named_match,
        "tier_s_top_pct": tier_s_top_pct,
        "n_named_bearer_match_seed": n_named_bearer_match,
        "n_mode_c_blocked": n_mode_c_blocked,
        "n_tier_3_lineage_blocked": n_tier_3_lineage_blocked,
        "threshold_S": threshold_S,
        "threshold_A": threshold_A,
        "threshold_C": threshold_C,
        "elapsed_seconds": total_elapsed,
        "gandalf_rep_status": gandalf_rep_status,
        "gandalf_cw_status": gandalf_cw_status,
        "signal_distributions": {
            k: {
                "n": len(v),
                "min": min(v) if v else 0,
                "max": max(v) if v else 0,
                "mean": sum(v) / len(v) if v else 0,
                "p25": sorted(v)[int(len(v) * 0.25)] if v else 0,
                "p50": sorted(v)[int(len(v) * 0.50)] if v else 0,
                "p75": sorted(v)[int(len(v) * 0.75)] if v else 0,
            }
            for k, v in signal_distributions.items()
        },
        "tier_s_samples": tier_s_samples[:50],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-gandalf-prep",
        action="store_true",
        help="Consume gandalf prep files (reputation-tier + cultural-weight) if present",
    )
    parser.add_argument(
        "--smoke-only",
        action="store_true",
        help="Run smoke test on 100 random rows; no DB write",
    )
    parser.add_argument(
        "--output-json",
        default=os.path.join(OUTPUT_DIR, "scoring-summary.json"),
        help="Where to write summary JSON",
    )
    args = parser.parse_args()

    if args.smoke_only:
        run_smoke()
        return

    summary = score_all_rows(use_gandalf_prep=args.use_gandalf_prep)

    # Write summary JSON
    with open(args.output_json, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"Wrote summary -> {args.output_json}")


def run_smoke():
    """Pre-scoring smoke test on 100 random rows; report estimated vs computed for 10 high/low representatives."""
    seed_list = parse_seed_list(GANDALF_SEED_LIST_PATH)
    mode_c_ids = load_mode_c_flagged_ids(NAMED_BEARER_MATCHES_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Pre-load helpers
    cluster_conf: dict[int, float] = {}
    for row in cur.execute(
        "SELECT knowledge_entry_id, MAX(confidence_score) AS conf FROM cluster_membership GROUP BY knowledge_entry_id"
    ):
        cluster_conf[row["knowledge_entry_id"]] = row["conf"]
    image_counts: dict[int, int] = defaultdict(int)
    for row in cur.execute(
        "SELECT knowledge_entry_id, COUNT(*) AS n FROM knowledge_entry_reference_images GROUP BY knowledge_entry_id"
    ):
        image_counts[row["knowledge_entry_id"]] = row["n"]

    cur.execute(
        "SELECT id, canonical_name, source_library, description_text, structured_properties, "
        "cultural_lineage_tags, genre_appearances, related_entries, cultural_lineage_canonical, "
        "extracted_materials, extracted_named_bearer, extracted_provenance_richness "
        "FROM weapon_knowledge_entries ORDER BY RANDOM() LIMIT 100"
    )
    rows = cur.fetchall()

    print(f"SMOKE: scored {len(rows)} rows")
    print()
    print(f"{'id':>7s}  {'src':<25s}  {'name':<50s}  {'composite':>9s}")
    print("-" * 100)
    for row in rows[:30]:
        rid = row["id"]
        src = row["source_library"] or ""
        rep_score = FALLBACK_REPUTATION.get(src, ("unknown", 0.30))[1]
        sig_desc = compute_description_richness(row["description_text"], row["structured_properties"])
        sig_prov = row["extracted_provenance_richness"] or 0.0
        sig_bearer = compute_named_bearer_signal(row["extracted_named_bearer"])
        sig_mat = compute_materials_richness(row["extracted_materials"])
        sig_lineage = compute_cultural_lineage_depth(
            row["cultural_lineage_tags"], row["genre_appearances"], row["related_entries"]
        )
        sig_img = min(1.0, image_counts.get(rid, 0) / 3.0)
        sig_centrality = compute_cluster_centrality_score(cluster_conf.get(rid))
        lineage = row["cultural_lineage_canonical"] or "unknown"
        sig_cw = FALLBACK_CULTURAL_WEIGHT.get(lineage, DEFAULT_CULTURAL_WEIGHT)
        composite = (
            WEIGHTS["source_library_reputation_tier"] * rep_score
            + WEIGHTS["description_richness"] * sig_desc
            + WEIGHTS["extracted_provenance_richness"] * sig_prov
            + WEIGHTS["extracted_named_bearer_presence"] * sig_bearer
            + WEIGHTS["extracted_materials_richness"] * sig_mat
            + WEIGHTS["cultural_lineage_depth"] * sig_lineage
            + WEIGHTS["image_presence"] * sig_img
            + WEIGHTS["cluster_centrality"] * sig_centrality
            + WEIGHTS["cultural_tradition_weight"] * sig_cw
        )
        cname = (row["canonical_name"] or "")[:48]
        print(f"{rid:>7d}  {src[:25]:<25s}  {cname:<50s}  {composite:>9.4f}")

    conn.close()


if __name__ == "__main__":
    main()
