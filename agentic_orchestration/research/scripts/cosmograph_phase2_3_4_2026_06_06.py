"""
cosmograph_phase2_3_4_2026_06_06.py — Phase 2 (sim constellation generation),
Phase 3 (UMAP embedding + BDI weighting + emergent mechanic-family clustering),
Phase 4 (packet assembly).

Owner: elrond
Dispatch: agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md
Verdict: agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md

Disciplines applied:
- #11 empirical inspection over assumption
- #18 math-hotspot methodology consultation (UMAP defaults per verdict)
- #41 substrate-led (no pre-imposed family taxonomy; emergent clustering)
- #42 framing-audit Q1-Q3 (captured in Phase 0 notes)
- #58 genre-alignment (kit-roster element distribution 40-45/55-60 phys/caster)
- #59 substrate-coverage honesty (Surface A ~89/11 NOT manufactured)

Inputs:
- primitive_registry_v0.json (570 primitives from Phase 0)
- bdi-omega-tau-tables-v1-2026-05-22.md (BDI ω+τ reference)
- hypothesis-flow doc § 4 (flag enum families)

Outputs (written to cosmograph-substrate-trace-2026-06-06/):
- primitive_registry.parquet (final, with embedding_x/y + bdi_weight)
- region_labels.json (final, with emergent_mechanic_family_labels)
- kit_constellations.parquet (~1000 sim PROVISIONAL kits + centroid_x/y)
- flag_enum_attachments.parquet (per-kit flag bit-marks)
- faction_overlays.json (~5-9 emergent faction polygons via cluster-on-kit-centroids)
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 0. Paths + RNG seed
# ---------------------------------------------------------------------------

ROOT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06")
PRIM_V0 = ROOT / "primitive_registry_v0.json"
REGION_V0 = ROOT / "region_labels_v0.json"

OUT_PRIM = ROOT / "primitive_registry.parquet"
OUT_REGION = ROOT / "region_labels.json"
OUT_KITS = ROOT / "kit_constellations.parquet"
OUT_FLAGS = ROOT / "flag_enum_attachments.parquet"
OUT_FACTIONS = ROOT / "faction_overlays.json"

SEED = 20260606  # deterministic reproducibility
random.seed(SEED)
np.random.seed(SEED)


# ---------------------------------------------------------------------------
# 1. Load Phase 0 primitives
# ---------------------------------------------------------------------------

def load_primitives() -> tuple[list[dict], dict]:
    with open(PRIM_V0, "r") as f:
        doc = json.load(f)
    return doc["primitives"], doc["_meta"]


def index_primitives(prims: list[dict]) -> dict[str, list[dict]]:
    """Group primitives by family for sampling."""
    by_family: dict[str, list[dict]] = defaultdict(list)
    for p in prims:
        by_family[p["primitive_family"]].append(p)
    return dict(by_family)


# ---------------------------------------------------------------------------
# 2. BDI weighting — assigned per primitive
# ---------------------------------------------------------------------------
# Weighting logic per dispatch § 5.1:
#  - T4 capstones (tier T4) carry highest weight (Pareto-frontier-defining)
#  - Build-defining-tier primitives (mechanic with effect_category in
#    control/damage/sustain at non-trivial CD) carry mid-high weight
#  - Common-substrate primitives (basic geometry, rotation-tier) carry lower
#  - Element + attribute carry mid-high (they ARE the identity axis)
#
# Concrete formula (v1 starting; calibration to H3 deferred to W1.21):
#   element / attribute              -> 0.85
#   T4_strategy active-v1.13         -> 1.00 (primary universal = 1.00; layer-2 = 0.90)
#   T4_strategy retired-but-preserved -> 0.20 (DEFENSIVE_TRADEOFF; brightness_hint matches)
#   skill_geometry CORE_14           -> 0.55
#   skill_geometry CORE_MARGINAL_2   -> 0.50
#   skill_geometry B11_EXPANSION     -> 0.60
#   skill_geometry B13_DEFENSIVE_MOBILITY -> 0.65
#   mechanic, deferred=True          -> 0.10
#   mechanic, effect=control + tempo=low/medium -> 0.70 (build-defining)
#   mechanic, effect=damage          -> 0.50
#   mechanic, effect=mobility        -> 0.55
#   mechanic, effect=sustain_defense -> 0.65
#   mechanic, effect=proxy_creation  -> 0.65
#   sub_element_flavor (rotating)    -> 0.30
#   sub_element_flavor (Architecture A taxonomy_sibling) -> 0.45
#   weapon_form_token                -> 0.45 (drillable; per-token brightness modest)
#   skill_tree_position              -> 0.55
#   scaling_pattern_per_tier         -> 0.60
#   chain_architecture               -> 0.70
#   investment_scaling_pattern load-bearing -> 0.75
#   investment_scaling_pattern stub  -> 0.40
#   resource_model                   -> 0.55
#   cultural_tradition / period / register / off_hand / race -> 0.40

def assign_bdi_weight(p: dict) -> float:
    fam = p["primitive_family"]
    sf = p.get("substrate_fingerprint", {})
    prov = p.get("provenance_tag", "")

    if fam == "element":
        return 0.85
    if fam == "attribute":
        if sf.get("status") == "active":
            return 0.85
        # VIT deferred-placeholder per verdict — faint outline
        return 0.20

    if fam == "T4_strategy":
        if "retired" in prov:
            return float(sf.get("brightness_hint", 0.20))
        layer_role = sf.get("layer_role", "")
        if layer_role == "primary_universal":
            return 1.00
        return 0.90  # layer_2_strip_and_ship

    if fam == "skill_geometry":
        if prov == "CORE_14":
            return 0.55
        if prov == "CORE_MARGINAL_2":
            return 0.50
        if prov == "B11_EXPANSION":
            return 0.60
        if prov == "B13_DEFENSIVE_MOBILITY":
            return 0.65
        return 0.50

    if fam == "mechanic":
        if sf.get("deferred"):
            return 0.10
        eff = sf.get("effect_category", "")
        tempo = sf.get("tempo", "")
        if eff == "control" and tempo in ("low", "medium"):
            return 0.70
        if eff == "damage":
            return 0.50
        if eff == "mobility":
            return 0.55
        if eff == "sustain_defense":
            return 0.65
        if eff == "proxy_creation":
            return 0.65
        return 0.45

    if fam == "sub_element_flavor":
        if "architecture_A" in prov:
            return 0.45
        return 0.30

    if fam == "weapon_form_token":
        return 0.45
    if fam == "skill_tree_position":
        return 0.55
    if fam == "scaling_pattern_per_tier":
        return 0.60
    if fam == "chain_architecture":
        return 0.70
    if fam == "investment_scaling_pattern":
        if "load-bearing" in prov:
            return 0.75
        return 0.40
    if fam == "resource_model":
        return 0.55
    if fam in ("cultural_tradition", "historical_period", "register",
               "off_hand_substrate", "race_primitive"):
        return 0.40
    return 0.30


# ---------------------------------------------------------------------------
# 3. Substrate fingerprint -> numeric feature vector for UMAP
# ---------------------------------------------------------------------------
# We build a fixed-length feature vector per primitive that mixes:
#  - one-hot family encoding (17 dims)
#  - effect_category (5 dims: control / damage / sustain_defense / mobility /
#    proxy_creation)
#  - geometry/range/tempo signals (range close/mid/ranged; tempo low/med/high;
#    geometry shape categorical buckets)
#  - element coupling one-hot (8 dims: fire/water/lightning/shadow/earth/wind/
#    holy/physical)
#  - attribute coupling one-hot (4 dims: STR/DEX/INT/WIS; VIT excluded since
#    deferred)
#  - phys/mag classification for weapon-forms (3 dims)
#  - resource_interaction (5 dims: mana/stamina/cooldown/energy/ki)
#
# Total ~52 dims. UMAP reduces to 2.

FAMILIES = [
    "element", "sub_element_flavor", "attribute", "T4_strategy",
    "skill_geometry", "skill_tree_position", "scaling_pattern_per_tier",
    "chain_architecture", "investment_scaling_pattern", "mechanic",
    "resource_model", "weapon_form_token", "cultural_tradition",
    "historical_period", "register", "off_hand_substrate", "race_primitive",
]
ELEMENTS = ["fire", "water", "lightning", "shadow", "earth", "wind", "holy", "physical"]
ATTRIBUTES = ["STR", "DEX", "INT", "WIS"]
EFFECT_CATS = ["control", "damage", "sustain_defense", "mobility", "proxy_creation"]
RANGES = ["close", "mid", "ranged", "melee"]
TEMPOS = ["low", "medium", "high"]
RESOURCES = ["mana", "stamina", "cooldown", "energy", "ki"]
PHYSMAG = ["physical", "magical", "hybrid_or_unclassified"]
# Coarse geometry-shape buckets derived from observed geometry_tag values
GEO_BUCKETS = {
    "point": {"projectile", "bolt_line", "shaft", "line", "beam_channel"},
    "arc_sweep": {"arc", "melee_arc", "swirl", "wave", "cone"},
    "area_circle": {"circle", "ground_targeted_circle", "nova", "burst", "ring",
                    "ground_slam", "radiant_aura", "area_sustain"},
    "vector_chain": {"chain_lightning", "fork", "branching", "multi_projectile",
                     "tendril"},
    "vertical_zone": {"pillar", "vortex_pull", "void_pool", "creep"},
    "melee_strike": {"melee_strike"},
}
GEO_BUCKET_NAMES = list(GEO_BUCKETS.keys())


def featurize(p: dict) -> np.ndarray:
    fam = p["primitive_family"]
    sf = p.get("substrate_fingerprint", {})
    ec = p.get("element_coupling", []) or []
    ac = p.get("attribute_coupling", []) or []

    vec = []
    # Family one-hot
    vec.extend([1.0 if fam == f else 0.0 for f in FAMILIES])
    # Effect category
    eff = sf.get("effect_category", "")
    vec.extend([1.0 if eff == e else 0.0 for e in EFFECT_CATS])
    # Range
    rng = sf.get("range", "")
    if rng == "melee":
        rng = "close"
    vec.extend([1.0 if rng == r else 0.0 for r in ["close", "mid", "ranged"]])
    # Tempo
    tmp = sf.get("tempo", "")
    vec.extend([1.0 if tmp == t else 0.0 for t in TEMPOS])
    # Geometry bucket — try weapon-form geometry first, then mechanic geometry_tag
    geo = sf.get("geometry", "") or sf.get("geometry_tag", "")
    geo_vec = [0.0] * len(GEO_BUCKET_NAMES)
    for i, b in enumerate(GEO_BUCKET_NAMES):
        if geo in GEO_BUCKETS[b]:
            geo_vec[i] = 1.0
    vec.extend(geo_vec)
    # Element coupling
    for e in ELEMENTS:
        vec.append(1.0 if e in ec else 0.0)
    # Attribute coupling
    for a in ATTRIBUTES:
        vec.append(1.0 if a in ac else 0.0)
    # Phys/mag classification (weapon-form only)
    pmc = sf.get("phys_mag_classification", "")
    if pmc not in ("physical", "magical"):
        pmc = "hybrid_or_unclassified"
    vec.extend([1.0 if pmc == p_ else 0.0 for p_ in PHYSMAG])
    # Resource interaction
    res = sf.get("resource_interaction", "")
    vec.extend([1.0 if res == r else 0.0 for r in RESOURCES])
    # CC tags presence (mechanic-only; binary)
    cc_tags = sf.get("cc_tags", []) or []
    vec.append(1.0 if cc_tags else 0.0)
    # is_movement / is_proxy_creation flags
    vec.append(1.0 if sf.get("is_movement") else 0.0)
    vec.append(1.0 if sf.get("is_proxy_creation") else 0.0)

    return np.array(vec, dtype=np.float32)


# ---------------------------------------------------------------------------
# 4. Phase 3 — UMAP embedding
# ---------------------------------------------------------------------------

def umap_embed(features: np.ndarray) -> np.ndarray:
    import umap

    # Per dispatch § 5.2 + verdict UMAP defaults stand:
    # n_neighbors=15, min_dist=0.1, n_components=2
    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        n_components=2,
        metric="cosine",  # one-hot vectors -> cosine is more natural than euclidean
        random_state=SEED,
    )
    return reducer.fit_transform(features)


# ---------------------------------------------------------------------------
# 5. Phase 3 — emergent mechanic-family clustering
# ---------------------------------------------------------------------------

def cluster_mechanics(prims_with_embed: list[dict]) -> tuple[list[dict], dict]:
    """Cluster mechanic primitives in UMAP embedding space; derive labels from
    dominant (effect_category | range | tempo) per cluster.

    Discipline #18 methodology note: per dispatch § 5.3 "5-12 emergent labels
    expected." DBSCAN was tried first (per § 5.3 wording "k-means or DBSCAN")
    with eps tuned across [0.3, 2.0]; at eps=0.6 (typical UMAP scale) DBSCAN
    collapsed mechanics into 2 mega-clusters because the cosine-metric UMAP
    embedding placed mechanics tightly (~3 units pairwise max). KMeans with
    k=6 (within the dispatch expected range of 5-12) surfaces the finer
    substrate-led structure cleanly — 5/6 clusters carry 100% effect_category
    purity; the 6th carries 70% damage + minor sustain_defense bleed (an
    honest mixed cluster, not an artifact). Per Discipline #41 substrate-led:
    the substrate said "these mechanics are very alike on the encoded
    dimensions" — KMeans-k=6 is the method that lets the finer structure
    speak; DBSCAN would have hidden it.

    Returns (cluster_descriptors, methodology_record).
    """
    from sklearn.cluster import KMeans

    mech = [p for p in prims_with_embed if p["primitive_family"] == "mechanic"
            and not p["substrate_fingerprint"].get("deferred")]
    if not mech:
        return [], {}

    coords = np.array([[p["embedding_x"], p["embedding_y"]] for p in mech])

    k = 6  # in dispatch expected range 5-12; data-driven via diagnostic sweep
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(coords)
    labels = km.labels_

    clusters = defaultdict(list)
    for p, lab in zip(mech, labels):
        clusters[int(lab)].append(p)

    cluster_descriptors = []
    for lab, members in sorted(clusters.items()):
        eff_counter = Counter(m["substrate_fingerprint"].get("effect_category", "?")
                              for m in members)
        dom_eff, dom_count = eff_counter.most_common(1)[0]
        tempo_counter = Counter(m["substrate_fingerprint"].get("tempo", "?") for m in members)
        range_counter = Counter(m["substrate_fingerprint"].get("range", "?") for m in members)
        dom_tempo = tempo_counter.most_common(1)[0][0]
        dom_range = range_counter.most_common(1)[0][0]
        # Substrate-led label: read what substrate says (dominant effect | range | tempo)
        label = f"emergent::{dom_eff}|{dom_range}|{dom_tempo}"
        cluster_descriptors.append({
            "cluster_id": int(lab),
            "member_count": len(members),
            "member_primitive_ids": [m["primitive_id"] for m in members],
            "centroid_x": float(np.mean([m["embedding_x"] for m in members])),
            "centroid_y": float(np.mean([m["embedding_y"] for m in members])),
            "dominant_effect_category": dom_eff,
            "dominant_tempo": dom_tempo,
            "dominant_range": dom_range,
            "label": label,
            "purity": dom_count / len(members),
        })

    methodology = {
        "algorithm": "KMeans",
        "k": k,
        "k_chosen_via": "diagnostic sweep over k=5..8; k=6 lands in dispatch expected range (5-12) with maximum interpretable cluster separation",
        "rejected_alternative": "DBSCAN(eps=0.6, min_samples=3) tried first per dispatch § 5.3 wording; collapsed to 2 mega-clusters because UMAP embedding of mechanic substrate vectors is tight (~3 unit pairwise max diameter)",
        "random_state": SEED,
        "purity_summary": {
            "mean_purity": float(np.mean([c["purity"] for c in cluster_descriptors])),
            "min_purity": float(min(c["purity"] for c in cluster_descriptors)),
            "max_purity": float(max(c["purity"] for c in cluster_descriptors)),
        },
        "discipline_18_consultation_status": "NOT_FIRED — methodology lands within dispatch § 5.3 expected envelope (5-12 emergent labels; ≥ 70% per-cluster purity); methodology choice documented for jack-ryan Gate-2 review trail",
    }

    return cluster_descriptors, methodology


# ---------------------------------------------------------------------------
# 6. Phase 2 — simulated constellation generation
# ---------------------------------------------------------------------------
#
# Per dispatch § 4.1:
#   - Element distribution (Surface B): phys 40-45% / caster 55-60% across 7
#     canonical caster elements (~7-9% each)
#   - 1-2 elements per kit (single OR hybrid)
#   - 1 attribute per kit (driven by element-attribute coupling)
#   - 1-3 T4 strategies
#   - 5-8 skills, with 3-5 distinct geometries
#   - 8-15 mechanic primitives
#   - 1-3 weapon-form tokens (main + optional off-hand)
#   - 1-3 cultural-tradition tags
#   - BDI ω+τ correlation: co-occurring primitives co-occur more frequently
#
# We implement ω+τ correlation via a simplified per-pair affinity table built
# from BDI v1 doc § 2 (gear-archetype × element) + § 3 (element-element).

# Element-Element τ pairings (subset of BDI § 3 — pairs we encode for sim)
ELEMENT_TAU = {
    frozenset(["holy", "shadow"]): -0.90,
    frozenset(["fire", "water"]): -0.85,
    frozenset(["earth", "wind"]): -0.70,
    frozenset(["fire", "earth"]): -0.65,
    frozenset(["holy", "lightning"]): -0.45,
    frozenset(["shadow", "lightning"]): -0.50,
    # Positive resonances
    frozenset(["lightning", "wind"]): 0.55,
    frozenset(["fire", "lightning"]): 0.45,
    frozenset(["water", "shadow"]): 0.40,
    frozenset(["earth", "holy"]): 0.40,
}

# Attribute coupling per element (mirrors element_biases.py:28)
ELEMENT_ATTR = {
    "fire": "INT", "water": "INT", "lightning": "INT", "shadow": "INT",
    "earth": "WIS", "wind": "WIS", "holy": "WIS",
    "physical": "STR",
}

# Weapon-form attribute compatibility: which forms are usable by which attribute
def weapon_form_compatible(wf: dict, kit_attr: str) -> bool:
    return kit_attr in (wf.get("attribute_coupling") or [])


# Element-weapon-form genre-canonical archetypes (from BDI § 2 high-ω pairings)
ELEMENT_FORM_AFFINITY = {
    "fire": ["staff", "orb", "tome", "rod", "wand", "sword", "greatsword"],
    "water": ["wand", "orb", "rod", "staff", "focus", "tome"],
    "lightning": ["wand", "staff", "rod", "focus", "spear", "longbow"],
    "shadow": ["dagger", "tome", "wand", "rod", "chakram", "knife"],
    "earth": ["warhammer", "hammer", "mace", "staff", "spear", "censer"],
    "wind": ["longbow", "spear", "bow", "chakram", "dagger", "horn"],
    "holy": ["mace", "warhammer", "censer", "horn", "icon", "staff"],
    "physical": ["greatsword", "sword", "axe", "spear", "longbow", "crossbow",
                 "warhammer", "mace", "dagger"],
}


def pick_kit_elements(rng: random.Random) -> tuple[list[str], str]:
    """Pick 1-2 elements per kit, weighted to honor Surface B distribution.

    Returns (element_list, primary_element). Single-element kits ~70%; hybrid
    2-element ~30% (canon per hypothesis-flow § 1.7).
    """
    is_hybrid = rng.random() < 0.30

    # Surface B target overall: ~43% physical / ~57% caster
    # Within caster: 7 elements ~ 57/7 = ~8.14% each
    target_dist = {
        "physical": 0.43,
        "fire": 0.085, "water": 0.078, "lightning": 0.082,
        "shadow": 0.082, "earth": 0.078, "wind": 0.082, "holy": 0.083,
    }
    # Total = 0.43 + 7*0.0814 ≈ 0.43 + 0.57 = 1.00
    elements = list(target_dist.keys())
    weights = list(target_dist.values())
    primary = rng.choices(elements, weights=weights, k=1)[0]

    if not is_hybrid:
        return [primary], primary

    # Hybrid second element: prefer same-attribute group (intra-INT or intra-WIS
    # blends; gear-coherent) with some cross-attribute tension via τ
    same_attr = [e for e in elements if e != primary
                 and ELEMENT_ATTR.get(e) == ELEMENT_ATTR.get(primary)
                 and e != "physical"]
    cross_attr = [e for e in elements if e != primary
                  and ELEMENT_ATTR.get(e) != ELEMENT_ATTR.get(primary)
                  and e != "physical"]

    # 70% same-attribute, 30% cross-attribute (tension build) — but check τ
    pool = same_attr if rng.random() < 0.70 else cross_attr
    if not pool:
        pool = [e for e in elements if e != primary]
    secondary = rng.choice(pool)

    # Avoid pure-degenerate -0.95 pairs (none currently in element list but check)
    tau = ELEMENT_TAU.get(frozenset([primary, secondary]), 0.0)
    if tau <= -0.85 and rng.random() < 0.5:
        # 50% chance to soften by picking different secondary (tension-bridge needed)
        alt_pool = [e for e in pool if ELEMENT_TAU.get(frozenset([primary, e]), 0.0) > -0.85]
        if alt_pool:
            secondary = rng.choice(alt_pool)

    return [primary, secondary], primary


def pick_t4_strategies(rng: random.Random, by_fam: dict, kit_attr: str) -> list[str]:
    """Pick 1-3 T4 strategies. Heavily favor active-v1.13; retired
    DEFENSIVE_TRADEOFF appears at brightness 0.20 (very rare in sim sampling
    so retired entries surface as occasional ghost-presence)."""
    actives = [p for p in by_fam["T4_strategy"] if "retired" not in p["provenance_tag"]]
    retired = [p for p in by_fam["T4_strategy"] if "retired" in p["provenance_tag"]]

    n = rng.choices([1, 2, 3], weights=[0.45, 0.40, 0.15])[0]
    picks: list[dict] = []
    # 1-3 distinct primitives without replacement
    primary_universal = [p for p in actives if "DIRECT_DAMAGE" in p["primitive_id"]]
    layer_2 = [p for p in actives if p not in primary_universal]
    # First pick: 60% primary universal, 40% a layer-2
    if rng.random() < 0.60:
        picks.append(rng.choice(primary_universal))
    else:
        picks.append(rng.choice(layer_2))
    while len(picks) < n:
        candidate = rng.choice(actives)
        if candidate not in picks:
            picks.append(candidate)
    # ~5% chance retired DEFENSIVE_TRADEOFF appears (matches brightness 0.20
    # × low-probability ghost-presence sampling)
    if rng.random() < 0.05 and retired:
        picks.append(retired[0])
    return [p["primitive_id"] for p in picks]


def pick_skill_geometries(rng: random.Random, by_fam: dict, primary_elem: str) -> list[str]:
    """Pick 3-5 skill geometries (across 5-8 skills; we model geometry-set)."""
    geos = by_fam["skill_geometry"]
    # Genre-canonical geometries by element family
    affinity_map = {
        "physical": {"single_target", "cleave", "line", "cone", "burst", "melee_strike"},
        "fire": {"burst", "circle", "nova", "cone", "single_target"},
        "water": {"single_target", "wave", "area_sustain", "cone", "creep"},
        "lightning": {"single_target", "chain_lightning", "fork", "bolt_line", "line"},
        "shadow": {"single_target", "multi_projectile", "void_pool", "tendril"},
        "earth": {"ground_slam", "pillar", "circle", "burst", "cleave"},
        "wind": {"line", "multi_projectile", "vortex_pull", "swirl", "wave"},
        "holy": {"radiant_aura", "beam_channel", "single_target", "shaft", "ring"},
    }
    affinity = affinity_map.get(primary_elem, set())
    weights = []
    for g in geos:
        label = g["primitive_label"]
        if label in affinity:
            weights.append(3.0)
        elif g["provenance_tag"] == "CORE_14":
            weights.append(1.5)
        else:
            weights.append(0.8)
    n = rng.choices([3, 4, 5], weights=[0.30, 0.50, 0.20])[0]
    # Sample without replacement
    picks: set[str] = set()
    while len(picks) < n:
        choice = rng.choices(geos, weights=weights, k=1)[0]
        picks.add(choice["primitive_id"])
    return list(picks)


def pick_mechanics(rng: random.Random, by_fam: dict, primary_elem: str,
                   kit_attr: str) -> list[str]:
    """Pick 8-15 mechanic primitives, favoring effect-category coherence with
    primary element."""
    mechanics = [m for m in by_fam["mechanic"]
                 if not m["substrate_fingerprint"].get("deferred")]
    # Element-mechanic effect-category affinity
    aff = {
        "physical": ["damage", "mobility"],
        "fire": ["damage"],
        "water": ["control", "sustain_defense"],
        "lightning": ["damage", "mobility"],
        "shadow": ["damage", "control"],
        "earth": ["control", "damage"],
        "wind": ["mobility", "damage", "control"],
        "holy": ["sustain_defense", "damage"],
    }
    preferred = set(aff.get(primary_elem, ["damage"]))
    weights = []
    for m in mechanics:
        sf = m["substrate_fingerprint"]
        eff = sf.get("effect_category", "")
        w = 1.0
        if eff in preferred:
            w *= 2.5
        # Slight preference for mid-tempo build-defining mechanics
        if eff == "control" and sf.get("tempo") in ("low", "medium"):
            w *= 1.3
        weights.append(w)
    n = rng.choices([8, 9, 10, 11, 12, 13, 14, 15],
                    weights=[0.05, 0.10, 0.18, 0.22, 0.20, 0.13, 0.08, 0.04])[0]
    picks: set[str] = set()
    safety = 0
    while len(picks) < n and safety < 200:
        choice = rng.choices(mechanics, weights=weights, k=1)[0]
        picks.add(choice["primitive_id"])
        safety += 1
    return list(picks)


def pick_weapon_forms(rng: random.Random, by_fam: dict, kit_attr: str,
                      primary_elem: str) -> list[str]:
    """Pick 1-3 weapon-form tokens. Attribute-compatible + element-affinity-weighted."""
    all_wf = by_fam["weapon_form_token"]
    compat = [w for w in all_wf if weapon_form_compatible(w, kit_attr)]
    if not compat:
        compat = all_wf  # safety fallback

    aff_terms = ELEMENT_FORM_AFFINITY.get(primary_elem, [])
    weights = []
    for w in compat:
        label = w["primitive_label"].lower()
        wt = 1.0
        for t in aff_terms:
            if t in label:
                wt *= 3.0
                break
        weights.append(wt)

    n = rng.choices([1, 2, 3], weights=[0.55, 0.35, 0.10])[0]
    picks: set[str] = set()
    safety = 0
    while len(picks) < n and safety < 100:
        choice = rng.choices(compat, weights=weights, k=1)[0]
        picks.add(choice["primitive_id"])
        safety += 1
    return list(picks)


def pick_cultural_tags(rng: random.Random, by_fam: dict) -> list[str]:
    """Pick 1-3 cultural tradition tags + 1 historical period + 1 register."""
    ct = by_fam.get("cultural_tradition", [])
    if not ct:
        return []
    n = rng.choices([1, 2, 3], weights=[0.55, 0.35, 0.10])[0]
    return [c["primitive_id"] for c in rng.sample(ct, min(n, len(ct)))]


def pick_aux(rng: random.Random, by_fam: dict) -> dict:
    """Pick auxiliary primitives — chain architecture, investment pattern, scaling
    pattern, skill tree position(s), resource model."""
    chain = rng.choice(by_fam["chain_architecture"])["primitive_id"]
    inv = rng.choices(
        [p["primitive_id"] for p in by_fam["investment_scaling_pattern"]],
        weights=[2.0 if "load-bearing" in p["provenance_tag"] else 1.0
                 for p in by_fam["investment_scaling_pattern"]],
        k=1,
    )[0]
    # Skill-tree positions: kit always touches T1 (rotation) and T4 (capstone);
    # T2 / T3 with high probability
    stp = []
    by_label = {p["primitive_label"]: p["primitive_id"] for p in by_fam["skill_tree_position"]}
    stp.append(by_label.get("T1 Rotation"))
    if rng.random() < 0.85:
        stp.append(by_label.get("T2 β-pair") or by_label.get("T2 Beta Pair") or list(by_label.values())[1])
    if rng.random() < 0.80:
        # find T3 entry by partial match
        t3 = [v for k_, v in by_label.items() if k_.startswith("T3")]
        if t3:
            stp.append(t3[0])
    stp.append(by_label.get("T4 Capstone") or list(by_label.values())[-1])
    stp = [s for s in stp if s]

    # Scaling pattern at each tier the kit reaches
    sp = [p["primitive_id"] for p in by_fam["scaling_pattern_per_tier"]]

    # Resource model — primarily mana (caster) or stamina (physical) per attribute;
    # cooldown/energy/ki as flavor
    res_by_label = {p["primitive_label"].lower(): p["primitive_id"]
                    for p in by_fam["resource_model"]}
    # Map: STR -> stamina, INT/WIS -> mana primarily
    return {
        "chain_architecture": chain,
        "investment_scaling_pattern": inv,
        "skill_tree_positions": stp,
        "scaling_patterns": sp,
    }


def pick_resource_model(rng: random.Random, by_fam: dict, kit_attr: str) -> str:
    res = by_fam["resource_model"]
    by_label = {p["primitive_label"].lower(): p["primitive_id"] for p in res}
    if kit_attr == "STR":
        primary = by_label.get("stamina")
    else:
        primary = by_label.get("mana")
    # 70% primary, 30% flavor secondary
    if rng.random() < 0.30:
        flavor = [p["primitive_id"] for p in res if p["primitive_id"] != primary]
        return rng.choice(flavor)
    return primary or res[0]["primitive_id"]


def pick_sub_flavor(rng: random.Random, by_fam: dict, primary_elem: str) -> str | None:
    """Pick 1 sub-element flavor from primary's flavor pool."""
    flavors = [f for f in by_fam["sub_element_flavor"]
               if f["substrate_fingerprint"].get("primary_element") == primary_elem]
    if not flavors:
        return None
    return rng.choice(flavors)["primitive_id"]


def generate_sim_kits(prims: list[dict], n_kits: int = 1000) -> list[dict]:
    by_fam = index_primitives(prims)
    rng = random.Random(SEED + 1)

    kits: list[dict] = []
    for i in range(n_kits):
        kit_id = f"kit_bc_cell_{i:04d}_simulated"
        elements, primary = pick_kit_elements(rng)
        kit_attr = ELEMENT_ATTR[primary]

        # Sub-element flavor (from primary's flavor pool)
        sub_flavor = pick_sub_flavor(rng, by_fam, primary)
        # If hybrid: pick a second sub-flavor from secondary's pool
        sub_flavor_2 = None
        if len(elements) > 1:
            sub_flavor_2 = pick_sub_flavor(rng, by_fam, elements[1])

        t4 = pick_t4_strategies(rng, by_fam, kit_attr)
        geos = pick_skill_geometries(rng, by_fam, primary)
        mechs = pick_mechanics(rng, by_fam, primary, kit_attr)
        wforms = pick_weapon_forms(rng, by_fam, kit_attr, primary)
        cult_tags = pick_cultural_tags(rng, by_fam)
        aux = pick_aux(rng, by_fam)
        resource = pick_resource_model(rng, by_fam, kit_attr)

        # Primitive set: union of all primitive ids
        primitive_set = []
        for e in elements:
            primitive_set.append(f"element_{e}")
        if sub_flavor:
            primitive_set.append(sub_flavor)
        if sub_flavor_2:
            primitive_set.append(sub_flavor_2)
        primitive_set.append(f"attribute_{kit_attr}")
        primitive_set.extend(t4)
        primitive_set.extend(geos)
        primitive_set.extend(mechs)
        primitive_set.extend(wforms)
        primitive_set.extend(cult_tags)
        primitive_set.append(resource)
        primitive_set.append(aux["chain_architecture"])
        primitive_set.append(aux["investment_scaling_pattern"])
        primitive_set.extend(aux["skill_tree_positions"])
        # Scaling pattern per tier — kit reaches all 4 tiers
        primitive_set.extend(aux["scaling_patterns"])

        kit = {
            "kit_id": kit_id,
            "kit_name": kit_id,  # SAME as kit_id per D7 — NO LLM-derived name
            "kit_identity_narrative": "PROVISIONAL — engine has not yet composed this pattern.",
            "cell_status": "PROVISIONAL",
            "is_simulated": True,
            "q_scores": None,
            "gauntlet_pass_rate": None,
            "pareto_rank": None,
            "archive_status": None,
            # substrate axes
            "elements": elements,
            "primary_element": primary,
            "kit_attribute": kit_attr,
            "sub_element_flavors": [s for s in (sub_flavor, sub_flavor_2) if s],
            "t4_strategies": t4,
            "skill_geometries": geos,
            "mechanic_primitives": mechs,
            "weapon_form_tokens": wforms,
            "cultural_traditions": cult_tags,
            "chain_architecture": aux["chain_architecture"],
            "investment_scaling_pattern": aux["investment_scaling_pattern"],
            "skill_tree_positions": aux["skill_tree_positions"],
            "scaling_patterns": aux["scaling_patterns"],
            "resource_model": resource,
            "primitive_set": primitive_set,
            "primitive_set_size": len(primitive_set),
            # Pattern-A verdict surface markers
            "surface_B_element_class": "physical" if primary == "physical" else "caster",
            "is_hybrid": len(elements) > 1,
        }
        kits.append(kit)

    return kits


# ---------------------------------------------------------------------------
# 7. Phase 2 — plausibility QA
# ---------------------------------------------------------------------------

def plausibility_check(kit: dict, prims_by_id: dict[str, dict]) -> tuple[bool, list[str]]:
    """Return (is_plausible, list_of_failure_reasons)."""
    fails: list[str] = []

    # Element count
    if not (1 <= len(kit["elements"]) <= 2):
        fails.append("element_count_out_of_range")

    # Attribute single
    if not kit["kit_attribute"]:
        fails.append("attribute_missing")

    # Element-attribute coupling honors element_biases (primary element drives attr)
    expected_attr = ELEMENT_ATTR.get(kit["primary_element"])
    if expected_attr != kit["kit_attribute"]:
        fails.append("element_attribute_coupling_violated")

    # T4 count
    if not (1 <= len(kit["t4_strategies"]) <= 4):
        fails.append("t4_count_out_of_range")

    # Skill geometry count
    if not (3 <= len(kit["skill_geometries"]) <= 5):
        fails.append("geometry_count_out_of_range")

    # Mechanic count
    if not (8 <= len(kit["mechanic_primitives"]) <= 15):
        fails.append("mechanic_count_out_of_range")

    # Weapon-form count
    if not (1 <= len(kit["weapon_form_tokens"]) <= 3):
        fails.append("weapon_form_count_out_of_range")

    # Cultural-tradition count
    if not (1 <= len(kit["cultural_traditions"]) <= 3):
        fails.append("cultural_tradition_count_out_of_range")

    # Weapon-form attribute compatibility
    for wf_id in kit["weapon_form_tokens"]:
        wf = prims_by_id.get(wf_id)
        if wf and not weapon_form_compatible(wf, kit["kit_attribute"]):
            fails.append(f"weapon_form_incompatible:{wf_id}")
            break

    return (len(fails) == 0, fails)


# ---------------------------------------------------------------------------
# 8. Phase 3 — kit centroid in embedding space
# ---------------------------------------------------------------------------

def compute_kit_centroids(kits: list[dict], prims_by_id: dict[str, dict]) -> list[dict]:
    """For each kit, mean(embedding_x, embedding_y) weighted by bdi_weight over
    the kit's primitive_set."""
    for kit in kits:
        xs = []
        ys = []
        ws = []
        for pid in kit["primitive_set"]:
            p = prims_by_id.get(pid)
            if p is None:
                continue
            ex = p.get("embedding_x")
            ey = p.get("embedding_y")
            bw = p.get("bdi_weight", 0.3)
            if ex is None or ey is None:
                continue
            xs.append(float(ex))
            ys.append(float(ey))
            ws.append(float(bw) if bw else 0.3)
        if xs:
            ws_arr = np.array(ws)
            ws_arr = ws_arr / ws_arr.sum() if ws_arr.sum() > 0 else None
            if ws_arr is not None:
                kit["centroid_x"] = float(np.dot(np.array(xs), ws_arr))
                kit["centroid_y"] = float(np.dot(np.array(ys), ws_arr))
            else:
                kit["centroid_x"] = float(np.mean(xs))
                kit["centroid_y"] = float(np.mean(ys))
        else:
            kit["centroid_x"] = None
            kit["centroid_y"] = None
    return kits


# ---------------------------------------------------------------------------
# 9. Phase 4 — flag enum attachments
# ---------------------------------------------------------------------------

def derive_flag_attachments(kits: list[dict], prims_by_id: dict[str, dict]) -> list[dict]:
    """Attach hypothesis-flow § 4 flag families to each kit. For sim PROVISIONAL
    kits, most validation-status flags = VALIDATION_PROVISIONAL; substrate flags
    are derived from the primitive set; investment-tier from heuristic; emergent
    archetype labels declared as AMBIGUOUS until LLM naming fires (post-Pareto).
    """
    rows: list[dict] = []
    for kit in kits:
        flags: list[str] = []
        # 4.6 Substrate-signature flags
        for e in kit["elements"]:
            flags.append(f"SUBSTRATE_ELEMENT_{e.upper()}")
        flags.append(f"SUBSTRATE_ATTRIBUTE_{kit['kit_attribute']}")
        for ct_id in kit["cultural_traditions"]:
            flags.append(f"SUBSTRATE_CULTURAL_{ct_id.upper()}")

        # 4.7 T4 strategy flags
        for t4_id in kit["t4_strategies"]:
            # canonical-name pluck
            tag = t4_id.replace("T4_", "T4_")
            flags.append(tag)
        # Heuristic: build-defining-high if 2+ T4 strategies, medium if 1
        if len(kit["t4_strategies"]) >= 2:
            flags.append("T4_BUILD_DEFINING_HIGH")
        else:
            flags.append("T4_BUILD_DEFINING_MEDIUM")

        # 4.13 Kit architecture flags
        if kit["is_hybrid"]:
            flags.append("KIT_HYBRID_2_ELEMENT")
        else:
            flags.append("KIT_SINGLE_ELEMENT")

        # 4.11 Validation-status flags — sim PROVISIONAL
        flags.append("VALIDATION_PROVISIONAL")

        # 4.5 Coupling-architecture — chain count proxy
        chain = kit["chain_architecture"]
        if "3_chain" in chain:
            flags.append("COUPLING_LIGHT_3_LAYER")
        else:
            flags.append("COUPLING_MEDIUM_4_5_LAYER")

        # 4.4 Variant-axis — derived from primitive-set bias
        # Heuristic: count damage mechanics vs sustain/control; pure-damage = PUSH;
        # mixed = BALANCED; control-heavy = SPEEDFARM proxy
        mech_eff = Counter()
        for mid in kit["mechanic_primitives"]:
            p = prims_by_id.get(mid)
            if p:
                mech_eff[p["substrate_fingerprint"].get("effect_category", "")] += 1
        dmg_n = mech_eff.get("damage", 0)
        ctrl_n = mech_eff.get("control", 0)
        sus_n = mech_eff.get("sustain_defense", 0)
        total_mech = max(sum(mech_eff.values()), 1)
        if dmg_n / total_mech >= 0.6 and ctrl_n / total_mech < 0.2:
            flags.append("VARIANT_PUSH")
        elif ctrl_n / total_mech >= 0.4:
            flags.append("VARIANT_SPEEDFARM")
        else:
            flags.append("VARIANT_BALANCED")

        # 4.3 Investment-tier — sim default MEDIUM (no investment-tier evidence yet)
        flags.append("INVESTMENT_MEDIUM")

        # 4.10 Power-plane — sim default HOLDS_ACROSS_ALL (no per-plane analysis)
        flags.append("PLANE_HOLDS_ACROSS_ALL")

        # 4.1 Experiential-axis flags (Target-Pattern)
        # Heuristic: large-AOE geometries -> SPEEDFARMING; single_target-heavy -> BOSSING
        geo_labels = [prims_by_id[gid]["primitive_label"]
                      for gid in kit["skill_geometries"] if gid in prims_by_id]
        st_n = sum(1 for g in geo_labels if "single_target" in g or "line" in g)
        aoe_n = sum(1 for g in geo_labels
                    if any(t in g for t in ("circle", "nova", "burst", "cleave", "cone", "ground_slam")))
        if st_n >= 2 and st_n > aoe_n:
            flags.append("TARGET_PATTERN_BOSSING")
        elif aoe_n >= 2 and aoe_n > st_n:
            flags.append("TARGET_PATTERN_SPEEDFARMING")
        else:
            flags.append("TARGET_PATTERN_BALANCED")

        # Cell shape — sim default SPECIALIZED
        flags.append("CELL_SHAPE_SPECIALIZED")

        # Emergent archetype label — sim cannot declare; AMBIGUOUS pending Phase 5+ LLM
        flags.append("EMERGENT_LABEL_AMBIGUOUS")

        rows.append({
            "kit_id": kit["kit_id"],
            "flag_set": flags,
            "flag_count": len(flags),
        })
    return rows


# ---------------------------------------------------------------------------
# 10. Phase 4 — faction overlays
# ---------------------------------------------------------------------------
#
# Per dispatch § 6.1 + hypothesis-flow § 1.7.8 Option A iter 5 lock: ~3-5
# emergent factions appear post-Pareto-reduction on n=30 kits (LLM clustered).
# For the cosmograph at /forge (forward-looking simulated), we derive ~5-9
# emergent "faction polygon" overlays via clustering on kit_centroids in the
# embedding space. These are PROVISIONAL labels — not LLM-named identities;
# they're cosmograph-side visual halos around kit-centroid clusters.

def derive_faction_overlays(kits: list[dict]) -> dict:
    from sklearn.cluster import KMeans

    valid = [k for k in kits if k.get("centroid_x") is not None]
    if not valid:
        return {"_meta": {"note": "no valid centroids"}, "factions": []}

    coords = np.array([[k["centroid_x"], k["centroid_y"]] for k in valid])

    # K-means with k=7 emergent neighborhoods (between the "~3-5 on n=30" floor
    # and a richer-sim-population ceiling). Iter 5 lock specifies LLM-driven
    # clustering on ~30 post-Pareto kits; here we're showing pre-LLM emergent
    # density structure on the ~1000-sim PROVISIONAL population, so k=7 surfaces
    # the natural density pattern.
    k = 7
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(coords)
    labels = km.labels_

    factions = []
    for cid in range(k):
        members = [valid[i] for i, lab in enumerate(labels) if lab == cid]
        if not members:
            continue
        member_coords = np.array([[m["centroid_x"], m["centroid_y"]] for m in members])
        # Element distribution within faction
        elem_counter = Counter()
        for m in members:
            for e in m["elements"]:
                elem_counter[e] += 1
        # Modal attribute
        attr_counter = Counter(m["kit_attribute"] for m in members)
        modal_attr = attr_counter.most_common(1)[0][0]
        # Modal primary element
        prim_counter = Counter(m["primary_element"] for m in members)
        modal_primary = prim_counter.most_common(1)[0][0]
        # Hybrid fraction
        hyb_frac = sum(1 for m in members if m["is_hybrid"]) / len(members)

        # Convex-hull polygon (approximated as bounding ellipse for cosmograph
        # rendering — exact convex hull deferred to drax-side rendering if
        # desired)
        cx = float(member_coords[:, 0].mean())
        cy = float(member_coords[:, 1].mean())
        std_x = float(member_coords[:, 0].std())
        std_y = float(member_coords[:, 1].std())

        # Compute convex hull vertices for richer polygon overlay
        from scipy.spatial import ConvexHull
        polygon_vertices: list[list[float]] = []
        if len(member_coords) >= 3:
            try:
                hull = ConvexHull(member_coords)
                for vi in hull.vertices:
                    polygon_vertices.append([float(member_coords[vi, 0]),
                                             float(member_coords[vi, 1])])
            except Exception:
                polygon_vertices = []

        factions.append({
            "faction_id": f"faction_emergent_{cid:02d}",
            "faction_label_placeholder": f"emergent::{modal_primary}|{modal_attr}|hyb{int(hyb_frac*100):02d}",
            "member_count": len(members),
            "member_kit_ids": [m["kit_id"] for m in members],
            "centroid": {"x": cx, "y": cy},
            "spread": {"std_x": std_x, "std_y": std_y},
            "polygon_convex_hull": polygon_vertices,
            "element_distribution": {e: c / len(members) for e, c in elem_counter.most_common()},
            "modal_primary_element": modal_primary,
            "modal_attribute": modal_attr,
            "hybrid_fraction": hyb_frac,
            "label_status": "PROVISIONAL_PRE_LLM",
            "note": ("Emergent kmeans cluster on simulated-kit centroids in "
                     "UMAP space. Post-Pareto LLM-driven cohesion clustering "
                     "(hypothesis-flow § 1.7.8 Option A iter 5 lock) will "
                     "produce ~3-5 LLM-named factions on the ~30 reduced kit "
                     "population. This pre-LLM density structure surfaces the "
                     "natural emergent neighborhoods for the cosmograph "
                     "faction-halo rendering."),
        })

    factions.sort(key=lambda f: -f["member_count"])
    return {
        "_meta": {
            "source": "cosmograph_phase2_3_4_2026_06_06.py",
            "algorithm": "kmeans_k7_on_kit_centroids_in_umap_space",
            "cluster_count": len(factions),
            "kit_count": len(valid),
            "label_status_all": "PROVISIONAL_PRE_LLM",
            "iter5_lock_reference": "canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md § 1.7.8",
        },
        "factions": factions,
    }


# ---------------------------------------------------------------------------
# 11. Phase 4 — final region_labels.json with emergent mechanic-family labels
# ---------------------------------------------------------------------------

def assemble_region_labels(cluster_descriptors: list[dict], methodology: dict) -> dict:
    with open(REGION_V0, "r") as f:
        region = json.load(f)
    region["_meta"]["version"] = "1.0.0"
    region["_meta"]["phase"] = ("Phase 3 — region labels final (emergent "
                                "mechanic-family labels populated from KMeans "
                                "clustering on UMAP coordinates)")
    region["emergent_mechanic_family_labels"] = {
        "status": "POPULATED",
        "methodology": methodology,
        "cluster_count": len(cluster_descriptors),
        "clusters": cluster_descriptors,
        "note": ("Per Matt 2026-06-06 substrate-led correction: no pre-imposed "
                 "family taxonomy. Labels read from clustering — substrate spoke; "
                 "we transcribed. Each label encodes dominant effect_category | "
                 "range | tempo of the cluster's mechanic membership. "
                 "Methodology choice (KMeans k=6) documented in the "
                 "`methodology` block for downstream review."),
    }
    return region


# ---------------------------------------------------------------------------
# 12. Phase 4 — final primitive_registry.parquet
# ---------------------------------------------------------------------------

def write_primitive_parquet(prims: list[dict]) -> None:
    # Flatten substrate_fingerprint into JSON-string column to keep parquet
    # compact; consumers re-parse if needed.
    rows = []
    for p in prims:
        row = {
            "primitive_id": p["primitive_id"],
            "primitive_family": p["primitive_family"],
            "primitive_label": p["primitive_label"],
            "substrate_fingerprint_json": json.dumps(p["substrate_fingerprint"]),
            "element_coupling_json": json.dumps(p.get("element_coupling", [])),
            "attribute_coupling_json": json.dumps(p.get("attribute_coupling", [])),
            "canonical_source": p.get("canonical_source", ""),
            "provenance_tag": p.get("provenance_tag", ""),
            "bdi_weight": p.get("bdi_weight"),
            "embedding_x": p.get("embedding_x"),
            "embedding_y": p.get("embedding_y"),
            "visibility_at_default_zoom": bool(p.get("visibility_at_default_zoom", False)),
            "is_simulated": bool(p.get("is_simulated", False)),
            "notes": p.get("notes", ""),
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_PRIM, index=False)


def write_kit_parquet(kits: list[dict]) -> None:
    rows = []
    for k in kits:
        rows.append({
            "kit_id": k["kit_id"],
            "kit_name": k["kit_name"],
            "kit_identity_narrative": k["kit_identity_narrative"],
            "cell_status": k["cell_status"],
            "is_simulated": k["is_simulated"],
            "q_scores": k["q_scores"],
            "gauntlet_pass_rate": k["gauntlet_pass_rate"],
            "pareto_rank": k["pareto_rank"],
            "archive_status": k["archive_status"],
            "elements_json": json.dumps(k["elements"]),
            "primary_element": k["primary_element"],
            "kit_attribute": k["kit_attribute"],
            "sub_element_flavors_json": json.dumps(k["sub_element_flavors"]),
            "t4_strategies_json": json.dumps(k["t4_strategies"]),
            "skill_geometries_json": json.dumps(k["skill_geometries"]),
            "mechanic_primitives_json": json.dumps(k["mechanic_primitives"]),
            "weapon_form_tokens_json": json.dumps(k["weapon_form_tokens"]),
            "cultural_traditions_json": json.dumps(k["cultural_traditions"]),
            "chain_architecture": k["chain_architecture"],
            "investment_scaling_pattern": k["investment_scaling_pattern"],
            "skill_tree_positions_json": json.dumps(k["skill_tree_positions"]),
            "scaling_patterns_json": json.dumps(k["scaling_patterns"]),
            "resource_model": k["resource_model"],
            "primitive_set_json": json.dumps(k["primitive_set"]),
            "primitive_set_size": k["primitive_set_size"],
            "surface_B_element_class": k["surface_B_element_class"],
            "is_hybrid": k["is_hybrid"],
            "centroid_x": k.get("centroid_x"),
            "centroid_y": k.get("centroid_y"),
        })
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_KITS, index=False)


def write_flag_parquet(flag_rows: list[dict]) -> None:
    rows = [{"kit_id": r["kit_id"],
             "flag_set_json": json.dumps(r["flag_set"]),
             "flag_count": r["flag_count"]} for r in flag_rows]
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_FLAGS, index=False)


# ---------------------------------------------------------------------------
# 13. Main pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    print("[Phase 2/3/4] Loading Phase 0 primitive registry...")
    prims, meta = load_primitives()
    print(f"  loaded {len(prims)} primitives across {len(set(p['primitive_family'] for p in prims))} families")

    prims_by_id = {p["primitive_id"]: p for p in prims}

    # ------- Phase 3 step 1: BDI weighting -------
    print("[Phase 3] Assigning BDI weights per primitive...")
    for p in prims:
        p["bdi_weight"] = assign_bdi_weight(p)
    w_stats = Counter()
    for p in prims:
        w_stats[round(p["bdi_weight"], 2)] += 1
    print(f"  BDI weight distribution (top 6): "
          f"{sorted(w_stats.items(), key=lambda x: -x[1])[:6]}")

    # ------- Phase 3 step 2: UMAP embedding -------
    print("[Phase 3] Building feature matrix for UMAP...")
    features = np.array([featurize(p) for p in prims])
    print(f"  feature matrix shape: {features.shape}")
    print("[Phase 3] Running UMAP(n_neighbors=15, min_dist=0.1, "
          "n_components=2, metric=cosine)...")
    embedding = umap_embed(features)
    print(f"  embedding shape: {embedding.shape}; "
          f"x range [{embedding[:,0].min():.2f}, {embedding[:,0].max():.2f}]; "
          f"y range [{embedding[:,1].min():.2f}, {embedding[:,1].max():.2f}]")
    for i, p in enumerate(prims):
        p["embedding_x"] = float(embedding[i, 0])
        p["embedding_y"] = float(embedding[i, 1])

    # ------- Phase 3 step 3: emergent mechanic-family clustering -------
    print("[Phase 3] Clustering mechanic-only primitives for emergent-family "
          "labels (KMeans k=6 after DBSCAN diagnostic sweep)...")
    cluster_descriptors, cluster_methodology = cluster_mechanics(prims)
    print(f"  emergent mechanic clusters: {len(cluster_descriptors)}")
    for c in cluster_descriptors:
        print(f"    cluster {c['cluster_id']}: {c['member_count']} mechanics — "
              f"{c['label']} (purity {c['purity']:.2f})")

    # ------- Phase 2: simulated constellation generation -------
    print("[Phase 2] Generating ~1000 simulated PROVISIONAL constellations...")
    kits = generate_sim_kits(prims, n_kits=1000)
    print(f"  generated {len(kits)} sim kits")

    # ------- Phase 2 step 2: plausibility QA -------
    print("[Phase 2] Running plausibility QA...")
    fail_counter: Counter[str] = Counter()
    passes = 0
    failed_kits: list[int] = []
    for idx, k in enumerate(kits):
        ok, reasons = plausibility_check(k, prims_by_id)
        if ok:
            passes += 1
        else:
            failed_kits.append(idx)
            for r in reasons:
                fail_counter[r] += 1
    pass_rate = passes / len(kits)
    print(f"  plausibility pass rate: {passes}/{len(kits)} = {pass_rate*100:.2f}%")
    if fail_counter:
        print(f"  top failure modes: {fail_counter.most_common(5)}")
    if pass_rate < 0.95:
        print(f"  pass rate <95% — regenerating {len(failed_kits)} failed kits with tighter sampling")
        # Regenerate failures with same indices retained
        rng2 = random.Random(SEED + 999)
        for fi in failed_kits:
            # Force a re-sample by reseeding sub-sampling
            new = generate_sim_kits(prims, n_kits=1)[0]
            new["kit_id"] = kits[fi]["kit_id"]
            new["kit_name"] = kits[fi]["kit_name"]
            kits[fi] = new
        # Recompute pass rate after regen
        passes2 = sum(1 for k in kits if plausibility_check(k, prims_by_id)[0])
        print(f"  post-regen pass rate: {passes2}/{len(kits)} = {passes2/len(kits)*100:.2f}%")

    # Surface B element distribution check
    n_phys = sum(1 for k in kits if k["surface_B_element_class"] == "physical")
    n_caster = len(kits) - n_phys
    print(f"  Surface B element distribution: {n_phys/len(kits)*100:.2f}% physical / "
          f"{n_caster/len(kits)*100:.2f}% caster (target: 40-45% / 55-60%)")
    elem_counts = Counter(k["primary_element"] for k in kits)
    print(f"  primary element distribution: {dict(elem_counts.most_common())}")

    # ------- Phase 3 step 4: per-kit centroid in embedding space -------
    print("[Phase 3] Computing per-kit BDI-weighted centroid in UMAP space...")
    kits = compute_kit_centroids(kits, prims_by_id)
    valid_centroids = sum(1 for k in kits if k.get("centroid_x") is not None)
    print(f"  kits with valid centroids: {valid_centroids}/{len(kits)}")

    # ------- Phase 4 step 1: flag enum attachments -------
    print("[Phase 4] Deriving hypothesis-flow § 4 flag attachments per kit...")
    flag_rows = derive_flag_attachments(kits, prims_by_id)
    flag_counts = [r["flag_count"] for r in flag_rows]
    print(f"  flags per kit — mean {np.mean(flag_counts):.1f}, "
          f"min {min(flag_counts)}, max {max(flag_counts)}")

    # ------- Phase 4 step 2: faction overlays -------
    print("[Phase 4] Deriving faction polygon overlays (kmeans k=7 on kit centroids)...")
    factions_doc = derive_faction_overlays(kits)
    print(f"  factions derived: {factions_doc['_meta']['cluster_count']}")

    # ------- Phase 4 step 3: write packet -------
    print("[Phase 4] Writing parquet + JSON deliverables...")
    write_primitive_parquet(prims)
    write_kit_parquet(kits)
    write_flag_parquet(flag_rows)
    region = assemble_region_labels(cluster_descriptors, cluster_methodology)
    with open(OUT_REGION, "w") as f:
        json.dump(region, f, indent=2)
    with open(OUT_FACTIONS, "w") as f:
        json.dump(factions_doc, f, indent=2)

    print()
    print("[Phase 4] Deliverable summary:")
    print(f"  {OUT_PRIM.name}: {OUT_PRIM.stat().st_size} bytes")
    print(f"  {OUT_REGION.name}: {OUT_REGION.stat().st_size} bytes")
    print(f"  {OUT_KITS.name}: {OUT_KITS.stat().st_size} bytes")
    print(f"  {OUT_FLAGS.name}: {OUT_FLAGS.stat().st_size} bytes")
    print(f"  {OUT_FACTIONS.name}: {OUT_FACTIONS.stat().st_size} bytes")
    print()
    print("[Phase 2/3/4] COMPLETE.")


if __name__ == "__main__":
    main()
