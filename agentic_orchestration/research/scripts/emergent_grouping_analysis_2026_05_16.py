"""
Emergent-grouping analysis at full substrate width.

Dispatch: agentic_orchestration/dispatches/2026-05-16-elrond-emergent-grouping-analysis.md
Author:   elrond
Date:     2026-05-16

Two-pass methodology:
  Pass 1 — Step A methodology AS-LOCKED (7 mechanic-families,
           Gower composite distance 0.6 content / 0.4 form,
           hierarchical agglomerative average-linkage).
  Pass 2 — EXTENDED per gandalf gate-3 amendment-trigger:
           - 10 mechanic-families (+movement-displacement,
             +reactive-defensive, +cast-prep-sustained)
           - split aura-vs-instant within buff-debuff-status
           - vendor-namespaced mechanic-tags preserved as
             content-signal augmentation.

For each pass: compute cluster assignments, silhouette, purity
against four hand-labels (substrate / mechanic / register /
vendor), characterize clusters, then evaluate clusters against
the four cipher-width viability criteria.

Pixogen treatment: dual-run — once including the 2 Pixogen packs,
once excluding — to surface license-flag sensitivity.

Reads only; never writes to engine DB; never writes to
catalogue.db. Outputs printable analysis to stdout.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from sklearn.metrics import silhouette_score

CATALOGUE_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "research/catalogue"
)

VENDORS = [
    "pimen", "ansimuz", "brackeys", "codemanu", "craftpix",
    "creativekind", "fellor", "frostwindz", "pipoya", "pixogen",
]

# ---------------------------------------------------------------------------
# Mechanic-family vocabularies
# ---------------------------------------------------------------------------

MECHANIC_FAMILIES_P1: dict[str, set[str]] = {
    "buff-debuff-status": {
        "buff", "debuff", "status-effect", "magic",
        # vendor-namespaced extensions that clearly belong here
        "aura-effect", "ambient-glow", "healing-aura", "shield-barrier",
        "shield-cast", "shield-idle", "bubble-shield",
        "barrier-cast", "hex-shield", "protective-aura",
        "paladin-aura", "death-aura", "frost-knight-aura",
        "censer-aura", "biological-dot",
    },
    "ambient-environmental": {
        "ambient", "environmental", "ambient-effect", "ambient-particle",
        "ambient-loop", "ambient-smoke", "ambient-light",
        "object-glow", "mysterious-object-pulse", "arcane-ambient",
        "atmospheric-plume", "smoke-cloud", "smoke-dissipate",
        "totem-summon", "cube-conjure", "book-of-summoning",
        "necro-summon", "undead-raise", "corpse-explosion",
        "light-pillar", "divine-beam", "holy-column",
    },
    "smoke-dust": {
        "smoke", "dust", "smoke-puff", "smoke-column", "smoke-vertical",
        "vapor",
    },
    "impact-burst": {
        "impact", "explosion", "hit-effect", "muzzle-flash",
        "impact-burst", "hit-spark", "collision-flash", "strike-effect",
        "physical-impact", "force-impact", "slash-impact",
        "explosion-impact", "particle-burst", "impact-flash",
        "explosion-burst", "big-explosion", "bomb-explosion",
        "electric-explosion", "in-air-explosion", "medium-blast",
        "reaction", "warped-explosion", "distorted-impact",
        "fireworks-burst", "void-explosion", "holy-explosion",
        "cosmic-impact", "stellar-pulse", "magic-explosion",
        "blast-cast", "explosive-magic", "fire-blast", "fire-burst",
        "pyromancer-blast", "flame-burst", "fire-bomb",
        "cryo-burst", "frost-burst", "venom-burst", "toxic-splash",
        "poison-cloud", "poison-AOE", "blood-burst",
        "sanguine-burst", "blood-splatter", "blood-impact",
        "ice-spike", "icicle-burst", "frost-wave", "ground-burst",
        "rock-rise", "earth-pillar", "soil-wave", "rock-wave",
        "ground-strike", "stone-barrier", "terrain-cast",
        "lightning-strike", "electric-burst", "wind-gust",
        "wind-spell", "typhoon-aoe", "water-strike", "wave-cast",
        "water-pillar", "water-beam", "spell-cast", "magic-blast",
        "fantasy-spell", "darkness-wave", "dark-blast",
        "shadow-cast", "darkness-spear", "dark-AOE", "dark-explosion",
        "dark-fireball", "dark-lightning", "stellar-cast",
        "stellar-wave", "cosmic-cast", "cosmic-burst", "space-cast",
        "space-beam", "void-bolt", "warlock-curse",
        "arcane-corruption", "eldritch-blast", "dark-pact",
        "necrotic-cast", "death-bolt", "shadow-wave", "soul-drain",
        "midas-touch", "sun-strike", "black-hole-effect",
        "implosion-gravity", "death-punch", "acid-splash",
        "spikes-cast", "fire-wall", "fireball-cast",
        "lightning-bolt", "lightning-arrow", "ball-lightning",
        "horizontal-lightning", "energy-explosion",
        "darknness-spear", "wave", "crystal-burst", "gem-shatter",
        "arcane-crystal", "mineral-resonance", "crystal-cast",
        "color-cast", "chromatic-burst", "multi-hue-wave",
        "arcane-rainbow", "prismatic-spell", "fire-loop",
        "pyro-wave", "thunder-cast", "lightning-loop",
        "freeze-cast", "freeze-effect", "ice-cast", "ice-pillar",
        "earth-cast", "fire-cast", "blood-cast", "blood-wave",
        "blood-surge", "blood-drain", "sanguine-bolt",
        "vampiric-bite", "void-shield", "void-portal",
        "void-black-hole", "void-slash", "void-spin",
        "technology-vfx", "attack-slash", "water-wave",
        "earth-strike", "holy-cross", "electric-bolt",
        "fire-flame", "fireworks-burst", "darkness-spear",
        "void-explosion", "wound-effect", "blood-pool",
        "celestial-beam", "star-fall", "lightning-spell",
        "ice-strike", "frost-slash",
    },
    "projectile-bullet": {
        "projectile", "bullet", "water-projectile", "poison-projectile",
        "arrows-volley", "spear-thrust", "darkness-spear",
        "spell-cast", "icicle-drop", "attack-sphere",
        "dark-projectile",
    },
    "melee-slash": {
        "slash", "thrust", "cutting", "smear", "weapon-trail",
        "sword-trail", "melee-swing", "cut-arc", "sword-slash",
        "magic-staff-strike", "cut-swing", "melee-arc",
        "rogue-slash", "backstab-flash", "vanish",
        "melee-slash-blood", "divine-slash", "holy-strike",
        "radiant-smash", "frost-slash", "ice-strike",
        "sword-enchant", "dark-slash", "shadow-spell",
        "death-punch", "physical-impact",
    },
    "heal": {
        "heal", "healing", "healing-cast", "healing-aura",
        "holy-heal", "divine-blessing", "sacred-restoration",
        "priest-cast", "mana-gather",
    },
}

# Pass 2 — extended families (gandalf Q-PRI-2 amendment-trigger)
MECHANIC_FAMILIES_P2: dict[str, set[str]] = {
    # buff-debuff-status SPLIT into aura-sustained and instant-buff
    "aura-sustained": {
        "aura-effect", "ambient-glow", "healing-aura", "shield-idle",
        "paladin-aura", "death-aura", "frost-knight-aura",
        "censer-aura", "protective-aura", "biological-dot",
        "buff", "ambient-light",
    },
    "instant-buff-debuff": {
        "debuff", "status-effect", "magic", "freeze-cast",
        "freeze-effect", "shield-cast", "bubble-shield",
        "barrier-cast", "hex-shield", "shield-barrier",
        "void-shield",
    },
    "ambient-environmental": MECHANIC_FAMILIES_P1["ambient-environmental"],
    "smoke-dust": MECHANIC_FAMILIES_P1["smoke-dust"],
    "impact-burst": MECHANIC_FAMILIES_P1["impact-burst"]
        - {"void-shield", "freeze-cast", "freeze-effect"},  # avoid double-count
    "projectile-bullet": MECHANIC_FAMILIES_P1["projectile-bullet"],
    "melee-slash": MECHANIC_FAMILIES_P1["melee-slash"],
    "heal": MECHANIC_FAMILIES_P1["heal"] - {"healing-aura"},
    # NEW (gandalf amendment)
    "movement-displacement": {
        "shadow-step", "vanish", "teleport-open", "teleport-transit",
        "warp-portal", "portal-swirl", "portal-color-variant",
        "stealth-burst",
    },
    "reactive-defensive": {
        "shield-cast", "shield-idle", "bubble-shield",
        "barrier-cast", "hex-shield", "protective-aura",
        "void-shield",
    },
    "cast-prep-sustained": {
        "mana-gather", "cosmic-burst", "stellar-cast",
        "cosmic-cast", "space-cast", "starcaller", "celestial-beam",
        "channeling", "windup", "cast-prep", "summoning-ritual",
        "totem-summon", "book-of-summoning", "necro-summon",
    },
}


# ---------------------------------------------------------------------------
# Substrate-classification → canonical-substrate normalization
# ---------------------------------------------------------------------------
# The 28 substrate-rows from cross-vendor inventory consolidate into a
# normalized substrate vocabulary the analysis works against. Pack-level
# substrate_classification field maps into one of these.

SUBSTRATE_NORMALIZE: dict[str, str] = {
    # elemental — overlap-with-Pimen
    "fire": "fire",
    "water": "water",
    "earth": "earth",
    "ice": "ice",
    "ice-kinetic": "ice",
    "lightning-thunder": "lightning",
    "wind-lightning-vector": "lightning",  # vector pack
    "holy": "holy",
    "holy-kinetic": "holy",
    "holy-healing": "holy",
    "holy-light-ambient": "holy",
    "dark-arcane": "dark-arcane",
    "acid": "acid",
    # novel — Step B-surfaced
    "death-necrotic": "death-necrotic",
    "blood-life-drain": "blood-sanguine",  # Frostwindz register
    "blood-wound": "blood-wound",  # CodeManu register — split per dispatch flag
    "cosmic-stellar": "cosmic-stellar",
    "void-spatial": "void-spatial",
    "void-adjacent-arcane": "void-adjacent-arcane",
    "technology-vfx": "technology",
    "crystal-gem-arcane": "crystal",
    "poison-biological": "poison-biological",  # split-vs-merge-with-acid flag
    "time-temporal": "time-temporal",
    "time-warp-spatial": "warp-spatial",
    "warp-teleportation": "warp-spatial",
    "shadow-kinetic": "shadow-kinetic",
    "chromatic-arcane": "chromatic-arcane",
    "midas-golden-transform": "midas-transmute",
    "smoke-atmospheric": "smoke-ambient",
    "implosion-gravity": "implosion-gravity",
    "summoning-ritual-object": "summoning-object",
    "defensive-barrier": "buff-defensive",
    "arcane-ambient-object": "ambient-arcane",
    # kinetic — Step B
    "impact-kinetic": "impact-kinetic",
    "melee-slash-kinetic": "melee-slash",
    "explosion-burst": "impact-kinetic",
    "explosion-impact": "impact-kinetic",
    "explosion-impact-ambient": "impact-kinetic",
    "explosion-multi-element": "impact-kinetic",
    "impact-burst-general": "impact-kinetic",
    "miscellaneous-kinetic": "impact-kinetic",
    # status
    "buff-debuff-status": "buff-defensive",
    # multi-* packs collapse to a meta "multi-element" tag
    "multi-element-niche-mechanic": "multi-element",
    "multi-element-general": "multi-element",
    "multi-element-void-technology": "multi-element",
    "multi-element-void-sample": "multi-element",
    "multi-element-aura-vector": "multi-element",
    "niche-mechanic-multi": "multi-element",
    # ambient-object
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def normalize_substrate(label: str) -> str:
    return SUBSTRATE_NORMALIZE.get(label, label)


def load_pimen_packs() -> list[dict]:
    """Load Pimen packs and normalize to per-pack substrate-row shape."""
    path = CATALOGUE_DIR / "pimen" / "full-2026-05-16.jsonl"
    out = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        a = json.loads(line)
        # Build substrate_classification from pimen_element for VFX rows;
        # category-mapped for character/enemy rows.
        cat = a.get("category", "vfx")
        elem = a.get("pimen_element")
        style_tags = [
            t["tag"] if isinstance(t, dict) else t
            for t in a.get("style_tags", [])
        ]
        # determine substrate
        if cat in {"character", "enemy"}:
            substrate = f"{cat}-asset"
        else:
            mechanic_signals = {
                "buff", "debuff", "status-effect",
                "ambient", "environmental", "smoke", "dust",
                "impact", "explosion", "hit-effect", "muzzle-flash",
                "projectile", "bullet",
                "slash", "thrust", "cutting", "smear",
                "heal", "healing",
            }
            mechs_seen = set(style_tags) & mechanic_signals
            if elem and elem in {"fire", "water", "earth", "wind", "thunder",
                                  "ice", "holy", "dark", "acid", "wood"}:
                substrate = {
                    "wind": "wind",
                    "thunder": "lightning",
                    "dark": "dark-arcane",
                    "wood": "wood",
                }.get(elem, elem)
            elif "heal" in mechs_seen or "healing" in mechs_seen:
                substrate = "heal-support"
            elif "slash" in mechs_seen or "thrust" in mechs_seen \
                    or "cutting" in mechs_seen or "smear" in mechs_seen:
                substrate = "melee-slash"
            elif "impact" in mechs_seen or "hit-effect" in mechs_seen \
                    or "muzzle-flash" in mechs_seen:
                substrate = "impact-kinetic"
            elif "projectile" in mechs_seen or "bullet" in mechs_seen:
                substrate = "projectile-bullet"
            elif "buff" in mechs_seen or "debuff" in mechs_seen \
                    or "status-effect" in mechs_seen:
                substrate = "buff-defensive"
            elif "smoke" in mechs_seen or "dust" in mechs_seen:
                substrate = "smoke-ambient"
            elif "ambient" in mechs_seen or "environmental" in mechs_seen:
                substrate = "ambient-arcane"
            else:
                substrate = "multi-element"
        out.append({
            "asset_id": a.get("asset_id"),
            "vendor": "pimen",
            "name": a.get("name"),
            "category": cat,
            "style_register": "pixel-art",
            "derived_register": "hand-drawn-pixel"
                if "hand-drawn-pixel" in style_tags else
                "retro-pixel" if "retro-pixel" in style_tags or "retro-16bit" in style_tags
                else "manual-review",
            "cost": float(a.get("cost", 0.0)) if a.get("cost") is not None else 0.0,
            "substrate_classification": substrate,
            "substrate_canonical": normalize_substrate(substrate),
            "substrate_distinct": False,  # Pimen baseline
            "license_unverified": False,
            "vector_format": False,
            "style_tags": style_tags,
            "vendor_mechanic_tags": [],
            "animations_count": a.get("animations_count"),
        })
    return out


def load_step_b_vendor_packs(vendor: str) -> list[dict]:
    path = CATALOGUE_DIR / vendor / "full-2026-05-16.jsonl"
    out = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        a = json.loads(line)
        substrate = a.get("substrate_classification", "unknown")
        style_tags = a.get("style_tags", []) or []
        register = a.get("style_register", "pixel-art")
        derived_register = (
            "vector" if register == "vector" else
            "hand-drawn-pixel" if "hand-drawn-pixel" in style_tags else
            "retro-pixel"
        )
        out.append({
            "asset_id": a.get("asset_id"),
            "vendor": vendor,
            "name": a.get("name"),
            "category": a.get("category", "vfx"),
            "style_register": register,
            "derived_register": derived_register,
            "cost": float(a.get("cost") or 0.0),
            "substrate_classification": substrate,
            "substrate_canonical": normalize_substrate(substrate),
            "substrate_distinct": bool(a.get("substrate_distinct", False)),
            "license_unverified": bool(a.get("license_unverified", False)),
            "vector_format": register == "vector",
            "style_tags": style_tags,
            "vendor_mechanic_tags": a.get("vendor_mechanic_tags", []) or [],
            "animations_count": a.get("animations_count"),
        })
    return out


def load_all_packs(*, exclude_pixogen: bool = True,
                    exclude_vectors: bool = False) -> list[dict]:
    all_packs: list[dict] = []
    for v in VENDORS:
        if v == "pimen":
            packs = load_pimen_packs()
        else:
            packs = load_step_b_vendor_packs(v)
        if exclude_pixogen and v == "pixogen":
            continue
        if exclude_vectors:
            packs = [p for p in packs if not p["vector_format"]]
        all_packs.extend(packs)
    return all_packs


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------


def extract_mechanic_families(pack: dict, families: dict[str, set[str]]) -> set[str]:
    """Tag-set membership for the mechanic-family vocabulary."""
    raw = set(pack.get("style_tags", []))
    raw |= set(pack.get("vendor_mechanic_tags", []))
    out = set()
    for family, members in families.items():
        if raw & members:
            out.add(family)
    return out


def build_pass1_features(packs: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """Pass 1 — 7 mechanic-families; substrate is content."""
    substrates = sorted({p["substrate_canonical"] for p in packs})
    mechs = sorted(MECHANIC_FAMILIES_P1.keys())
    registers = sorted({p["derived_register"] for p in packs})
    cats = sorted({p["category"] for p in packs})

    content_cols = [f"sub:{s}" for s in substrates] + \
                   [f"mech:{m}" for m in mechs]
    form_cols = [f"reg:{r}" for r in registers] + [f"cat:{c}" for c in cats]

    n = len(packs)
    content = np.zeros((n, len(content_cols)), dtype=np.int8)
    form = np.zeros((n, len(form_cols)), dtype=np.int8)
    for i, p in enumerate(packs):
        s = p["substrate_canonical"]
        content[i, substrates.index(s)] = 1
        for m in extract_mechanic_families(p, MECHANIC_FAMILIES_P1):
            content[i, len(substrates) + mechs.index(m)] = 1
        form[i, registers.index(p["derived_register"])] = 1
        form[i, len(registers) + cats.index(p["category"])] = 1
    return content, form


def build_pass2_features(packs: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """Pass 2 — 10 mechanic-families (aura-vs-instant split, +3 new);
    additional vendor-namespaced mechanic-tag contributions retained as
    distinct content features (one-hot over the top-N most-frequent
    vendor-mechanic-tags)."""
    substrates = sorted({p["substrate_canonical"] for p in packs})
    mechs = sorted(MECHANIC_FAMILIES_P2.keys())
    registers = sorted({p["derived_register"] for p in packs})
    cats = sorted({p["category"] for p in packs})

    # Top vendor-mechanic-tags (frequency >= 2) preserved as their own
    # content signals — this is the "vendor-namespaced mechanic-tag
    # preservation" the gandalf amendment requires.
    tag_freq: Counter = Counter()
    for p in packs:
        for t in p.get("vendor_mechanic_tags", []):
            tag_freq[t] += 1
    namespaced_tags = sorted([t for t, c in tag_freq.items() if c >= 3])

    content_cols = (
        [f"sub:{s}" for s in substrates] +
        [f"mech:{m}" for m in mechs] +
        [f"vtag:{t}" for t in namespaced_tags]
    )
    form_cols = [f"reg:{r}" for r in registers] + [f"cat:{c}" for c in cats]

    n = len(packs)
    content = np.zeros((n, len(content_cols)), dtype=np.int8)
    form = np.zeros((n, len(form_cols)), dtype=np.int8)
    for i, p in enumerate(packs):
        s = p["substrate_canonical"]
        content[i, substrates.index(s)] = 1
        for m in extract_mechanic_families(p, MECHANIC_FAMILIES_P2):
            content[i, len(substrates) + mechs.index(m)] = 1
        # vendor-namespaced tags
        offset = len(substrates) + len(mechs)
        for t in p.get("vendor_mechanic_tags", []):
            if t in namespaced_tags:
                content[i, offset + namespaced_tags.index(t)] = 1
        form[i, registers.index(p["derived_register"])] = 1
        form[i, len(registers) + cats.index(p["category"])] = 1
    return content, form


# ---------------------------------------------------------------------------
# Distance / clustering / metrics
# ---------------------------------------------------------------------------


def jaccard_distance(X: np.ndarray) -> np.ndarray:
    n = X.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            inter = int(np.bitwise_and(X[i], X[j]).sum())
            union = int(np.bitwise_or(X[i], X[j]).sum())
            d = 1.0 - (inter / union) if union > 0 else 1.0
            D[i, j] = D[j, i] = d
    return D


def hamming_distance(X: np.ndarray) -> np.ndarray:
    n, p = X.shape
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = D[j, i] = float((X[i] != X[j]).sum()) / max(p, 1)
    return D


def composite(C: np.ndarray, F: np.ndarray, w: float = 0.6) -> np.ndarray:
    return w * C + (1 - w) * F


def cluster_purity(labels: np.ndarray, hand: list) -> float:
    by_c: dict[int, Counter] = defaultdict(Counter)
    total = 0
    for lbl, h in zip(labels, hand):
        if h is None:
            continue
        by_c[lbl][h] += 1
        total += 1
    if total == 0:
        return float("nan")
    correct = sum(max(c.values()) for c in by_c.values())
    return correct / total


def characterize(members: list[dict]) -> str:
    subs = Counter(m["substrate_canonical"] for m in members)
    regs = Counter(m["derived_register"] for m in members)
    vends = Counter(m["vendor"] for m in members)
    cats = Counter(m["category"] for m in members)
    parts = []
    parts.append(
        "subs=[" + ", ".join(f"{s}:{c}" for s, c in subs.most_common(4)) + "]"
    )
    parts.append(
        "reg=" + regs.most_common(1)[0][0]
        + f" ({regs.most_common(1)[0][1]}/{len(members)})"
    )
    parts.append("vendors=" + str(len(vends)))
    if cats.most_common(1)[0][1] < len(members):
        parts.append(f"cats={dict(cats)}")
    return "; ".join(parts)


def run_pass(packs: list[dict], pass_name: str,
              build_features, families: dict[str, set[str]],
              w_content: float = 0.6) -> dict:
    n = len(packs)
    print(f"\n{'=' * 70}")
    print(f"PASS: {pass_name}  (n={n} packs)")
    print(f"{'=' * 70}")
    C, F = build_features(packs)
    print(f"  content dims: {C.shape}, form dims: {F.shape}")
    Dc = jaccard_distance(C)
    Df = hamming_distance(F)
    D = composite(Dc, Df, w_content)
    Z = linkage(squareform(D, checks=False), method="average")
    hand_sub = [p["substrate_canonical"] for p in packs]
    hand_reg = [p["derived_register"] for p in packs]
    hand_vend = [p["vendor"] for p in packs]
    hand_cat = [p["category"] for p in packs]
    hand_mech = []
    for p in packs:
        ms = extract_mechanic_families(p, families)
        hand_mech.append(sorted(ms)[0] if ms else None)

    print(f"\n  k     sil    pur(sub)  pur(reg)  pur(vend)  pur(cat)  "
          f"sgltn  max_share")
    sweep = []
    for k in range(2, 16):
        lbl = fcluster(Z, t=k, criterion="maxclust")
        if len(set(lbl)) < 2:
            continue
        sil = silhouette_score(D, lbl, metric="precomputed")
        ps = cluster_purity(lbl, hand_sub)
        pr = cluster_purity(lbl, hand_reg)
        pv = cluster_purity(lbl, hand_vend)
        pc = cluster_purity(lbl, hand_cat)
        sizes = Counter(lbl)
        sgl = sum(1 for s in sizes.values() if s == 1)
        mxs = max(sizes.values()) / n
        print(f"  {k:>2}  {sil:>6.3f}  {ps:>7.2f}  {pr:>7.2f}  "
              f"{pv:>8.2f}  {pc:>7.2f}  {sgl:>5}  {mxs:>9.2f}")
        sweep.append((k, sil, ps, pr, pv, pc, sgl, mxs, lbl))

    # Sensitivity sweep
    print(f"\n  Sensitivity over weight_content (k=6, 8, 10):")
    print(f"  w_c   k=6 sil   k=8 sil   k=10 sil")
    for w in [0.3, 0.5, 0.6, 0.7, 0.85, 1.0]:
        Dw = composite(Dc, Df, w)
        Zw = linkage(squareform(Dw, checks=False), method="average")
        sils = []
        for kk in (6, 8, 10):
            lb = fcluster(Zw, t=kk, criterion="maxclust")
            if len(set(lb)) < 2:
                sils.append(float("nan"))
                continue
            sils.append(silhouette_score(Dw, lb, metric="precomputed"))
        print(f"  {w:>3.2f}    {sils[0]:>6.3f}    {sils[1]:>6.3f}    "
              f"{sils[2]:>7.3f}")

    # Pick best in mid-range k=5..10
    cand = [r for r in sweep if 5 <= r[0] <= 12]
    best = max(cand, key=lambda r: r[1])
    kb, silb, psb, prb, pvb, pcb, sgl, mxs, lbl = best
    print(f"\n  *** selected cut k={kb}: sil={silb:.3f}  pur(sub)={psb:.2f}"
          f"  pur(reg)={prb:.2f}  pur(vend)={pvb:.2f}  sgltn={sgl}  "
          f"max_share={mxs:.2f}")

    # Per-cluster characterizations
    print(f"\n  Per-cluster (k={kb}):")
    by_c: dict[int, list[dict]] = defaultdict(list)
    for p, l in zip(packs, lbl):
        by_c[l].append(p)
    cluster_chars: dict[int, str] = {}
    for cid in sorted(by_c):
        members = by_c[cid]
        char = characterize(members)
        cluster_chars[cid] = char
        names = [m["vendor"] + ":" + (m["asset_id"] or "?") for m in members]
        print(f"\n  C{cid} (n={len(members)}): {char}")
        for nm in names[:6]:
            print(f"       - {nm}")
        if len(names) > 6:
            print(f"       ... ({len(names) - 6} more)")

    return {
        "pass_name": pass_name,
        "n": n,
        "selected_k": kb,
        "silhouette": silb,
        "purity_substrate": psb,
        "purity_register": prb,
        "purity_vendor": pvb,
        "purity_category": pcb,
        "singletons": sgl,
        "max_share": mxs,
        "labels": lbl,
        "by_cluster": by_c,
        "cluster_chars": cluster_chars,
        "packs": packs,
    }


# ---------------------------------------------------------------------------
# Cipher-width viability assessment
# ---------------------------------------------------------------------------

def viability_assess(result: dict) -> list[dict]:
    """Evaluate each cluster against the 4 framework criteria.

    Heuristics:
      - mechanical-distinctness: cluster has >=1 dominant substrate
        with mechanical signature, contains >=3 packs (avoids singleton
        groupings), and the substrate is NOT just an aggregate
        (multi-element) bucket.
      - role-orientation coverage: cluster admits damage / control /
        hybrid; checked via mechanic-family composition.
      - thematic-coherence: vendor-diversity OR cosmological coherence
        — at least 2 vendors confirm OR the substrate has an established
        anchor in the cosmology doc.
      - genre-recognition: substrate is recognizable in modern ARPG
        canon (PoE / D4 / Last Epoch / Grim Dawn).
    """
    by_c = result["by_cluster"]
    out = []
    # Substrate genre-recognition catalogue
    GENRE_RECOGNIZED = {
        "fire", "water", "earth", "ice", "lightning", "wind",
        "holy", "dark-arcane", "poison-biological", "death-necrotic",
        "blood-sanguine", "blood-wound", "void-spatial",
        "void-adjacent-arcane", "cosmic-stellar",
        "warp-spatial", "time-temporal",
        "melee-slash", "impact-kinetic",
        "crystal",  # PoE has crystallization; D4 has Spiritborn crystal
        "shadow-kinetic",
        "acid",
        # NOT genre-recognized: chromatic-arcane, midas-transmute,
        # implosion-gravity (mechanic not substrate), summoning-object,
        # ambient-arcane, smoke-ambient, technology, multi-element,
        # heal-support, buff-defensive, character-asset, enemy-asset
    }
    # Substrate damage/control orientation
    DAMAGE_SUBSTRATES = {
        "fire", "lightning", "ice", "earth", "water", "wind",
        "death-necrotic", "blood-sanguine", "blood-wound",
        "impact-kinetic", "melee-slash", "void-spatial",
        "cosmic-stellar", "void-adjacent-arcane",
        "shadow-kinetic", "implosion-gravity",
        "midas-transmute", "chromatic-arcane",
    }
    CONTROL_SUBSTRATES = {
        "poison-biological", "acid", "time-temporal", "warp-spatial",
        "ice", "earth",  # earth/ice often control in ARPGs
        "buff-defensive", "holy",  # holy admits both
        "smoke-ambient", "summoning-object", "ambient-arcane",
        "crystal", "chromatic-arcane",
    }
    for cid, members in by_c.items():
        n = len(members)
        subs = Counter(m["substrate_canonical"] for m in members)
        vends = Counter(m["vendor"] for m in members)
        cats = Counter(m["category"] for m in members)
        dominant_sub, dom_count = subs.most_common(1)[0]
        is_multi_aggregate = dominant_sub == "multi-element"
        is_character = "character" in cats or "enemy" in cats
        # Mechanical-distinctness
        mech_distinct = (
            n >= 3 and not is_multi_aggregate and not is_character
            and dom_count / n >= 0.4
        )
        # Role-orientation coverage
        admits_damage = any(s in DAMAGE_SUBSTRATES for s in subs)
        admits_control = any(s in CONTROL_SUBSTRATES for s in subs)
        role_coverage = admits_damage  # require damage at minimum
        # Thematic-coherence
        thematic = len(vends) >= 2 or dominant_sub in {
            "fire", "water", "earth", "ice", "lightning",
            "holy", "dark-arcane", "death-necrotic",
            "blood-sanguine", "void-spatial", "cosmic-stellar",
        }
        # Genre-recognition
        genre_ok = dominant_sub in GENRE_RECOGNIZED
        # Robust = all 4
        robust = mech_distinct and role_coverage and thematic and genre_ok
        out.append({
            "cluster_id": cid,
            "n": n,
            "dominant_substrate": dominant_sub,
            "dom_share": dom_count / n,
            "vendor_count": len(vends),
            "mech_distinct": mech_distinct,
            "role_coverage": role_coverage,
            "thematic": thematic,
            "genre_recognized": genre_ok,
            "robust": robust,
            "admits_damage": admits_damage,
            "admits_control": admits_control,
        })
    return out


def report_viability(name: str, assessment: list[dict],
                     chars: dict[int, str]) -> int:
    print(f"\n  Viability assessment — {name}")
    print(f"  {'C':>3}  {'n':>3}  {'dom-sub':>22}  {'mech':>5}  "
          f"{'role':>5}  {'them':>5}  {'genre':>5}  {'ROBUST':>6}")
    robust_count = 0
    for a in assessment:
        flags = [a["mech_distinct"], a["role_coverage"],
                  a["thematic"], a["genre_recognized"]]
        if a["robust"]:
            robust_count += 1
        marks = ["Y" if f else "n" for f in flags]
        rb = "YES" if a["robust"] else "no"
        print(f"  {a['cluster_id']:>3}  {a['n']:>3}  "
              f"{a['dominant_substrate']:>22}  {marks[0]:>5}  "
              f"{marks[1]:>5}  {marks[2]:>5}  {marks[3]:>5}  {rb:>6}")
    print(f"  → Robust grouping count: {robust_count}")
    return robust_count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    # Section 1 — Input snapshot
    print("=" * 70)
    print("SECTION 1 — Input substrate snapshot")
    print("=" * 70)

    # Build the no-Pixogen, all-formats default base
    packs_default = load_all_packs(exclude_pixogen=True, exclude_vectors=False)
    print(f"\nTotal packs (default: Pixogen EXCLUDED): {len(packs_default)}")
    by_vendor = Counter(p["vendor"] for p in packs_default)
    for v, c in sorted(by_vendor.items(), key=lambda x: -x[1]):
        print(f"  {v:<14}  {c:>3} packs")
    substrate_counter = Counter(p["substrate_canonical"] for p in packs_default)
    print(f"\nNormalized substrate distribution ({len(substrate_counter)} tags):")
    for s, c in sorted(substrate_counter.items(), key=lambda x: -x[1]):
        print(f"  {s:<30}  {c:>3}")

    # Vector packs
    vector_packs = [p for p in packs_default if p["vector_format"]]
    print(f"\nVector packs in default set: {len(vector_packs)}")
    for p in vector_packs:
        print(f"  - {p['vendor']}:{p['asset_id']} (sub={p['substrate_canonical']})")

    # Section 2 — Pass 1
    print("\n" + "=" * 70)
    print("SECTION 2 — Methodology execution (two passes)")
    print("=" * 70)
    r1 = run_pass(packs_default, "PASS 1 — AS-LOCKED (7 families)",
                   build_pass1_features, MECHANIC_FAMILIES_P1)
    a1 = viability_assess(r1)
    robust1 = report_viability("Pass 1", a1, r1["cluster_chars"])

    # Pass 2
    r2 = run_pass(packs_default, "PASS 2 — EXTENDED (10 families + namespaced)",
                   build_pass2_features, MECHANIC_FAMILIES_P2)
    a2 = viability_assess(r2)
    robust2 = report_viability("Pass 2", a2, r2["cluster_chars"])

    # Pixogen sensitivity
    print("\n" + "=" * 70)
    print("SECTION 2c — Pixogen include-sensitivity check")
    print("=" * 70)
    packs_with_pixogen = load_all_packs(exclude_pixogen=False,
                                        exclude_vectors=False)
    print(f"\nWith Pixogen: {len(packs_with_pixogen)} packs "
          f"(+{len(packs_with_pixogen) - len(packs_default)} Pixogen packs)")
    r1px = run_pass(packs_with_pixogen,
                     "PASS 1 (Pixogen INCLUDED)",
                     build_pass1_features, MECHANIC_FAMILIES_P1)
    a1px = viability_assess(r1px)
    robust1px = report_viability("Pass 1 + Pixogen", a1px, r1px["cluster_chars"])

    # Vectors excluded sensitivity
    print("\n" + "=" * 70)
    print("SECTION 2d — CraftPix vector sensitivity check")
    print("=" * 70)
    packs_no_vector = load_all_packs(exclude_pixogen=True, exclude_vectors=True)
    print(f"\nNo vector packs: {len(packs_no_vector)}")
    r1nv = run_pass(packs_no_vector, "PASS 1 (vector EXCLUDED)",
                     build_pass1_features, MECHANIC_FAMILIES_P1)
    a1nv = viability_assess(r1nv)
    robust1nv = report_viability("Pass 1 no vectors", a1nv, r1nv["cluster_chars"])

    # Section 3 — Framework outcome summary
    print("\n" + "=" * 70)
    print("SECTION 3 — Cipher-width framework outcome")
    print("=" * 70)
    print(f"\n  Pass 1 (default)        : {robust1} robust groupings")
    print(f"  Pass 2 (extended)       : {robust2} robust groupings")
    print(f"  Pass 1 + Pixogen        : {robust1px} robust groupings")
    print(f"  Pass 1 (no vectors)     : {robust1nv} robust groupings")
    for count, label in [
        (robust1, "Pass 1"),
        (robust2, "Pass 2"),
        (robust1px, "Pass 1+Pixogen"),
        (robust1nv, "Pass 1-vectors"),
    ]:
        if count >= 3 and count <= 5:
            outcome = "OUTCOME 1 (multi-grouping architecture viable)"
        elif count in (1, 2):
            outcome = "OUTCOME 2 (refined-Option-A; 1-2 groupings)"
        else:
            outcome = "OUTCOME 3 (canonical-four cipher remains operative)"
        print(f"  {label:<18}  {outcome}")

    # Sub-substrate behavior probes (for flag adjudications)
    print("\n" + "=" * 70)
    print("SECTION 7 — Flag adjudication evidence")
    print("=" * 70)

    # Blood split-vs-merge
    print("\n  Blood: which cluster do blood-sanguine vs blood-wound land in?")
    for r, name in [(r1, "Pass1"), (r2, "Pass2")]:
        blood_groups = defaultdict(set)
        for p, l in zip(r["packs"], r["labels"]):
            if p["substrate_canonical"] in ("blood-sanguine", "blood-wound"):
                blood_groups[p["substrate_canonical"]].add(int(l))
        if blood_groups:
            print(f"    {name}: blood-sanguine→{blood_groups.get('blood-sanguine')}; "
                  f"blood-wound→{blood_groups.get('blood-wound')}")

    # Acid vs Poison
    print("\n  Acid vs Poison: cluster behavior")
    for r, name in [(r1, "Pass1"), (r2, "Pass2")]:
        ap = defaultdict(set)
        for p, l in zip(r["packs"], r["labels"]):
            if p["substrate_canonical"] in ("acid", "poison-biological"):
                ap[p["substrate_canonical"]].add(int(l))
        if ap:
            print(f"    {name}: acid→{ap.get('acid')}; "
                  f"poison-biological→{ap.get('poison-biological')}")

    # Void variants
    print("\n  Void variants (sanity)")
    for r, name in [(r1, "Pass1"), (r2, "Pass2")]:
        vv = defaultdict(set)
        for p, l in zip(r["packs"], r["labels"]):
            if p["substrate_canonical"] in (
                "dark-arcane", "void-spatial", "void-adjacent-arcane",
                "warp-spatial", "shadow-kinetic",
            ):
                vv[p["substrate_canonical"]].add(int(l))
        if vv:
            print(f"    {name}:")
            for k, v in vv.items():
                print(f"      {k}→{v}")


if __name__ == "__main__":
    main()
