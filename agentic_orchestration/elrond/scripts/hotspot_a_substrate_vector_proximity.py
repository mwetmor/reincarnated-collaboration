"""
Hotspot A — substrate-vector proximity metric

Per Discipline #18.2 methodology consultation. See companion methodology note:
  agentic_orchestration/elrond/notes/2026-06-09-hotspot-a-substrate-vector-proximity-methodology.md

What this computes
==================
Given:
  - 1000 kits (PROVISIONAL corpus); each kit has a `primitive_set` of ~34 atomic
    substrate primitives drawn from a 366-primitive universe (registry has 570;
    366 are referenced by at least one kit)
  - Two Phase 3 layouts: radial-baseline (constellation_layout.json) and
    force-directed (twolayer_layout_alt.json), each placing kits in an
    11000x8500 px world centered on 8 element anchors on a 4x2 grid

For each layout we measure how strongly the LAYOUT'S spatial distance reflects
the SUBSTRATE-VECTOR distance between kits, where substrate-vector distance is
the principled categorical distance on primitive_set membership (weighted
Jaccard with family-block weights).

The validation framework reports several complementary statistics so that a
single methodology choice does not silently fail (Discipline #25 rep-audit at
metric definition):

  1. Spearman correlation between pairwise spatial distance and substrate
     distance over a random sample of kit pairs (N=20000 pairs)
  2. Kendall tau (rank-based, rank-robust check on (1))
  3. Per-element kNN substrate purity at k=5: of the 5 spatially-nearest kits to
     each kit, what fraction share its primary element? (criterion 2 at face)
  4. Per-element kNN substrate-distance ratio: mean substrate distance from a
     kit to its 5 spatial-nearest neighbours, divided by the mean substrate
     distance to 5 random kits. Lower = layout preserves substrate proximity
  5. MDS-style stress on per-element-family subsets: how faithfully does the
     layout reproduce the substrate-distance matrix when restricted to one
     element family? Lower = better
  6. Cross-family spread: for each anchor element, mean spatial distance of
     non-element kits to the element's centroid. Used to detect anchor-bias
     artifacts (kits placed near anchor purely by element-coupling rather than
     full substrate similarity)

Per Discipline #1 / #1.2, formal definitions live in the methodology note and
each implementation block carries a `# MATH-NOTE:` citation matching a numbered
section in the note.

Output
------
JSON results file at
  agentic_orchestration/elrond/research/hotspot-a-substrate-vector-proximity-<DATE>/
    results.json
and a console summary table for inclusion in the methodology note.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import kendalltau, spearmanr

# -----------------------------------------------------------------------------
# Paths (absolute per agent contract)
# -----------------------------------------------------------------------------
META_ROOT = Path("/Users/admin/Games/reincarnated-collaboration")
SUBSTRATE_DIR = META_ROOT / "agentic_orchestration/elrond/research/cosmograph-substrate-trace-2026-06-06"
LOADOUT_PUBLIC = Path("/Users/admin/Games/reincarnated-loadout/public/data/cosmograph")
OUT_ROOT = META_ROOT / "agentic_orchestration/elrond/research/hotspot-a-substrate-vector-proximity-2026-06-09"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

PRIMITIVE_PARQUET = SUBSTRATE_DIR / "primitive_registry.parquet"
KITS_PARQUET = SUBSTRATE_DIR / "kit_constellations.parquet"
REGION_LABELS = SUBSTRATE_DIR / "region_labels.json"

RADIAL_LAYOUT = LOADOUT_PUBLIC / "twolayer_layout.json"          # baseline radial
FORCE_LAYOUT = LOADOUT_PUBLIC / "twolayer_layout_alt.json"       # force-directed
CONSTELLATION_LAYOUT = LOADOUT_PUBLIC / "constellation_layout.json"  # 4x2 grid w/ stage1

SEED = 20260609
N_PAIR_SAMPLE = 20_000   # for correlation statistics
K_NN = 5                 # for kNN purity / ratio
RANDOM_KNN_REPS = 1      # we use exactly K_NN random comparators per kit

# -----------------------------------------------------------------------------
# § A. Substrate-vector representation (MATH-NOTE § 2 in methodology note)
# -----------------------------------------------------------------------------
# Each kit is a set S_k subset of the 366-primitive universe.
# Family weights w_f scale a primitive's contribution by which kind of trait it
# is. Element / attribute / mechanic / geometry primitives carry MORE
# information about "kit identity" than e.g. T4 strategy or scaling pattern
# (which are nearly universal). We surface the weights explicitly so the
# methodology note can audit them.
#
# Weighted Jaccard distance between two kits A, B:
#   sum_w(A intersect B) / sum_w(A union B)
# d_substrate(A, B) = 1 - weighted_jaccard

FAMILY_WEIGHTS: dict[str, float] = {
    # high-information (kit identity)
    "element":                       1.0,
    "sub_element_flavor":            1.0,
    "mechanic":                      1.0,
    "skill_geometry":                1.0,
    "weapon_form_token":             1.0,
    "cultural_tradition":            1.0,
    "race_primitive":                1.0,
    # medium-information
    "attribute":                     0.7,
    "T4_strategy":                   0.7,
    "register":                      0.7,
    "historical_period":             0.7,
    "off_hand_substrate":            0.7,
    # low-information (nearly universal across kits)
    "chain_architecture":            0.3,
    "investment_scaling_pattern":    0.3,
    "skill_tree_position":           0.3,
    "scaling_pattern_per_tier":      0.3,
    "resource_model":                0.3,
}
# Fallback for unknown family
DEFAULT_FAMILY_WEIGHT = 0.5


# -----------------------------------------------------------------------------
# Loaders
# -----------------------------------------------------------------------------

def load_substrate() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str]]:
    """Load primitive registry, kit constellations, and primitive→family map."""
    prim = pd.read_parquet(PRIMITIVE_PARQUET)
    kits = pd.read_parquet(KITS_PARQUET)

    # Build primitive_id → family. We use prim where present, then derive from
    # primitive prefix for the remaining ~366-570 gap (kits reference a subset).
    fam_map: dict[str, str] = {
        row.primitive_id: row.primitive_family for row in prim.itertuples()
    }
    return prim, kits, fam_map


def parse_primitive_sets(kits: pd.DataFrame) -> list[set[str]]:
    return [set(json.loads(s)) for s in kits["primitive_set_json"]]


def family_of(prim_id: str, fam_map: dict[str, str]) -> str:
    if prim_id in fam_map:
        return fam_map[prim_id]
    # Heuristic prefix fallback (kits sometimes use prefix-style ids that don't
    # appear directly in the registry; per substrate inspection there are 0
    # unresolved currently, but we keep the fallback for robustness)
    for prefix, fam in [
        ("element_", "element"),
        ("flavor_", "sub_element_flavor"),
        ("mechanic_", "mechanic"),
        ("geometry_", "skill_geometry"),
        ("weapon_form_", "weapon_form_token"),
        ("cultural_tradition_", "cultural_tradition"),
        ("attribute_", "attribute"),
        ("T4_", "T4_strategy"),
        ("chain_arch_", "chain_architecture"),
        ("investment_pattern_", "investment_scaling_pattern"),
        ("position_tier_", "skill_tree_position"),
        ("scaling_pattern_", "scaling_pattern_per_tier"),
        ("resource_", "resource_model"),
        ("register_", "register"),
        ("historical_period_", "historical_period"),
        ("race_", "race_primitive"),
        ("offhand_", "off_hand_substrate"),
        ("physical_taxonomy_", "sub_element_flavor"),  # observed in registry
    ]:
        if prim_id.startswith(prefix):
            return fam
    return "unknown"


def primitive_weight(prim_id: str, fam_map: dict[str, str]) -> float:
    fam = family_of(prim_id, fam_map)
    return FAMILY_WEIGHTS.get(fam, DEFAULT_FAMILY_WEIGHT)


# -----------------------------------------------------------------------------
# § B. Substrate distance (MATH-NOTE § 3)
# -----------------------------------------------------------------------------

def build_weight_lookup(all_prims: list[str], fam_map: dict[str, str]) -> np.ndarray:
    return np.array([primitive_weight(p, fam_map) for p in all_prims], dtype=np.float64)


def build_membership_matrix(
    primitive_sets: list[set[str]], all_prims: list[str]
) -> np.ndarray:
    """boolean matrix shape (n_kits, n_prims) — 1 if kit contains primitive."""
    idx = {p: i for i, p in enumerate(all_prims)}
    n = len(primitive_sets)
    m = len(all_prims)
    mat = np.zeros((n, m), dtype=np.uint8)
    for i, s in enumerate(primitive_sets):
        for p in s:
            if p in idx:
                mat[i, idx[p]] = 1
    return mat


def weighted_jaccard_distance(
    mat: np.ndarray, weights: np.ndarray, i: int, j: int
) -> float:
    """d(i,j) = 1 - sum_w(A and B) / sum_w(A or B). MATH-NOTE § 3.1."""
    a = mat[i]
    b = mat[j]
    inter = np.logical_and(a, b)
    union = np.logical_or(a, b)
    w_inter = float(np.sum(weights[inter]))
    w_union = float(np.sum(weights[union]))
    if w_union == 0:
        return 0.0
    return 1.0 - w_inter / w_union


def weighted_jaccard_distance_batch(
    mat: np.ndarray, weights: np.ndarray, i: int, js: np.ndarray
) -> np.ndarray:
    """Distances from kit i to many kits js (vectorised)."""
    a = mat[i].astype(bool)
    b_mat = mat[js].astype(bool)
    inter = np.logical_and(a[None, :], b_mat)
    union = np.logical_or(a[None, :], b_mat)
    w_inter = (inter.astype(np.float64) * weights[None, :]).sum(axis=1)
    w_union = (union.astype(np.float64) * weights[None, :]).sum(axis=1)
    # avoid divide-by-zero
    safe = np.where(w_union > 0, w_union, 1.0)
    dist = 1.0 - w_inter / safe
    dist[w_union == 0] = 0.0
    return dist


# -----------------------------------------------------------------------------
# § C. Layout loaders
# -----------------------------------------------------------------------------

@dataclass
class Layout:
    name: str
    coords: np.ndarray            # shape (n_kits, 2) in same kit_id order as kits df
    anchors: dict[str, np.ndarray]  # element name -> (x,y) anchor position
    world_w: float
    world_h: float


def load_layout(path: Path, name: str, kit_id_order: list[str]) -> Layout:
    with open(path) as f:
        d = json.load(f)
    meta = d["meta"]
    centroid_map = {c["kit_id"]: (c["cx"], c["cy"]) for c in d["centroids"]}
    coords = np.array([centroid_map[k] for k in kit_id_order], dtype=np.float64)
    anchors: dict[str, np.ndarray] = {}
    if "anchors" in d:
        for a in d["anchors"]:
            anchors[a["element"]] = np.array([a["x"], a["y"]], dtype=np.float64)
    return Layout(
        name=name,
        coords=coords,
        anchors=anchors,
        world_w=float(meta.get("world_w", 0.0)),
        world_h=float(meta.get("world_h", 0.0)),
    )


# -----------------------------------------------------------------------------
# § D. Evaluations (MATH-NOTE § 4)
# -----------------------------------------------------------------------------

def sample_pair_correlation(
    mat: np.ndarray,
    weights: np.ndarray,
    coords: np.ndarray,
    n_pairs: int,
    rng: random.Random,
) -> dict[str, float]:
    """MATH-NOTE § 4.1 — Spearman/Kendall on random kit-pair distance."""
    n = mat.shape[0]
    pairs = set()
    while len(pairs) < n_pairs:
        i = rng.randrange(n)
        j = rng.randrange(n)
        if i == j:
            continue
        pairs.add((min(i, j), max(i, j)))
    pair_arr = np.array(sorted(pairs))
    sub = np.zeros(len(pair_arr))
    spa = np.zeros(len(pair_arr))
    # vectorise per i for the substrate distance
    by_i = defaultdict(list)
    for k, (i, j) in enumerate(pair_arr):
        by_i[i].append((k, j))
    for i, items in by_i.items():
        ks = np.array([k for k, _ in items])
        js = np.array([j for _, j in items])
        d = weighted_jaccard_distance_batch(mat, weights, i, js)
        sub[ks] = d
    diffs = coords[pair_arr[:, 0]] - coords[pair_arr[:, 1]]
    spa = np.sqrt((diffs ** 2).sum(axis=1))
    sp_r, sp_p = spearmanr(sub, spa)
    # kendall is O(n log n) but slow at 20k; subsample to 5k
    if len(sub) > 5000:
        idx = np.random.RandomState(SEED).choice(len(sub), 5000, replace=False)
        kt_r, kt_p = kendalltau(sub[idx], spa[idx])
    else:
        kt_r, kt_p = kendalltau(sub, spa)
    return {
        "n_pairs": int(len(pair_arr)),
        "spearman_r": float(sp_r),
        "spearman_p": float(sp_p),
        "kendall_tau": float(kt_r),
        "kendall_p": float(kt_p),
        "substrate_dist_mean": float(sub.mean()),
        "substrate_dist_std": float(sub.std()),
        "spatial_dist_mean": float(spa.mean()),
        "spatial_dist_std": float(spa.std()),
    }


def knn_substrate_purity_and_ratio(
    mat: np.ndarray,
    weights: np.ndarray,
    coords: np.ndarray,
    primary_elements: list[str],
    k: int,
    rng: random.Random,
) -> dict[str, Any]:
    """MATH-NOTE § 4.2 — kNN purity + substrate-distance ratio."""
    tree = cKDTree(coords)
    n = coords.shape[0]
    purities = np.zeros(n)
    knn_sub = np.zeros(n)
    rand_sub = np.zeros(n)
    rand_idxs_pool = list(range(n))
    for i in range(n):
        _, nbrs = tree.query(coords[i], k=k + 1)  # +1 to drop self
        nbrs = [j for j in nbrs if j != i][:k]
        purities[i] = sum(1 for j in nbrs if primary_elements[j] == primary_elements[i]) / k
        knn_d = weighted_jaccard_distance_batch(mat, weights, i, np.array(nbrs))
        knn_sub[i] = knn_d.mean()
        # k random comparators (different sample per kit; cheap)
        randoms = rng.sample(rand_idxs_pool, k + 1)
        randoms = [j for j in randoms if j != i][:k]
        rand_d = weighted_jaccard_distance_batch(mat, weights, i, np.array(randoms))
        rand_sub[i] = rand_d.mean()

    # per-element breakdown
    per_ele: dict[str, dict[str, float]] = {}
    for ele in sorted(set(primary_elements)):
        mask = np.array([1 if e == ele else 0 for e in primary_elements], dtype=bool)
        per_ele[ele] = {
            "n_kits": int(mask.sum()),
            "knn_purity": float(purities[mask].mean()),
            "knn_substrate_mean": float(knn_sub[mask].mean()),
            "random_substrate_mean": float(rand_sub[mask].mean()),
            "knn_over_random_ratio": (
                float(knn_sub[mask].mean() / rand_sub[mask].mean())
                if rand_sub[mask].mean() > 0
                else float("nan")
            ),
        }
    return {
        "k": k,
        "overall_purity_mean": float(purities.mean()),
        "overall_purity_median": float(np.median(purities)),
        "overall_knn_substrate_mean": float(knn_sub.mean()),
        "overall_random_substrate_mean": float(rand_sub.mean()),
        "overall_knn_over_random_ratio": float(knn_sub.mean() / rand_sub.mean()) if rand_sub.mean() > 0 else float("nan"),
        "per_element": per_ele,
    }


def per_element_mds_stress(
    mat: np.ndarray,
    weights: np.ndarray,
    coords: np.ndarray,
    primary_elements: list[str],
    sample_pairs_per_element: int,
    rng: random.Random,
) -> dict[str, Any]:
    """MATH-NOTE § 4.3 — Kruskal stress on per-element subsets.

    Stress-1 := sqrt(sum (d_sub - d_spa_normalised)^2 / sum d_sub^2)
    where d_spa_normalised = d_spa * (sum(d_sub * d_spa) / sum(d_spa^2))
    is the optimal scale match.
    """
    per_ele: dict[str, dict[str, float]] = {}
    for ele in sorted(set(primary_elements)):
        idxs = [i for i, e in enumerate(primary_elements) if e == ele]
        if len(idxs) < 5:
            continue
        # sample pairs
        pairs = set()
        attempts = 0
        target = min(sample_pairs_per_element, len(idxs) * (len(idxs) - 1) // 2)
        while len(pairs) < target and attempts < target * 4:
            i = rng.choice(idxs)
            j = rng.choice(idxs)
            attempts += 1
            if i == j:
                continue
            pairs.add((min(i, j), max(i, j)))
        if not pairs:
            continue
        pa = np.array(sorted(pairs))
        # vectorise substrate
        sub = np.zeros(len(pa))
        by_i = defaultdict(list)
        for k, (i, j) in enumerate(pa):
            by_i[i].append((k, j))
        for i, items in by_i.items():
            ks = np.array([k for k, _ in items])
            js = np.array([j for _, j in items])
            sub[ks] = weighted_jaccard_distance_batch(mat, weights, i, js)
        diffs = coords[pa[:, 0]] - coords[pa[:, 1]]
        spa = np.sqrt((diffs ** 2).sum(axis=1))
        if spa.sum() == 0:
            continue
        scale = float((sub * spa).sum() / (spa ** 2).sum())
        spa_n = spa * scale
        denom = float((sub ** 2).sum())
        if denom == 0:
            continue
        stress = float(math.sqrt(((sub - spa_n) ** 2).sum() / denom))
        sp_r, _ = spearmanr(sub, spa)
        per_ele[ele] = {
            "n_kits": int(len(idxs)),
            "n_pairs": int(len(pa)),
            "kruskal_stress_1": stress,
            "spearman_within_element": float(sp_r),
        }
    overall_stress = float(np.mean([v["kruskal_stress_1"] for v in per_ele.values()]))
    overall_within_spearman = float(np.mean([v["spearman_within_element"] for v in per_ele.values()]))
    return {
        "per_element": per_ele,
        "mean_kruskal_stress_1": overall_stress,
        "mean_within_element_spearman": overall_within_spearman,
    }


def anchor_proximity_check(
    layout: Layout,
    primary_elements: list[str],
) -> dict[str, Any]:
    """MATH-NOTE § 4.4 — does spatial proximity to anchor X correlate with
    primary_element=X membership? Reveals whether the layout's element
    neighbourhoods are just construction artifacts (anchor as fixed point)."""
    if not layout.anchors:
        return {"note": "no anchors in layout"}
    per_anchor: dict[str, dict[str, float]] = {}
    for ele, pos in layout.anchors.items():
        d_to_anchor = np.sqrt(((layout.coords - pos) ** 2).sum(axis=1))
        order = np.argsort(d_to_anchor)
        # closest 100 kits
        top100_ele_count = sum(
            1 for j in order[:100] if primary_elements[j] == ele
        )
        # closest 200
        top200_ele_count = sum(
            1 for j in order[:200] if primary_elements[j] == ele
        )
        # mean distance of element-matched kits
        ele_mask = np.array([1 if e == ele else 0 for e in primary_elements], dtype=bool)
        mean_d_ele = float(d_to_anchor[ele_mask].mean()) if ele_mask.any() else float("nan")
        mean_d_nonele = float(d_to_anchor[~ele_mask].mean()) if (~ele_mask).any() else float("nan")
        per_anchor[ele] = {
            "n_element_kits": int(ele_mask.sum()),
            "top100_match_count": int(top100_ele_count),
            "top200_match_count": int(top200_ele_count),
            "mean_distance_element_kits": mean_d_ele,
            "mean_distance_nonelement_kits": mean_d_nonele,
        }
    return {"per_anchor": per_anchor}


def evaluate_layout(
    layout: Layout,
    mat: np.ndarray,
    weights: np.ndarray,
    primary_elements: list[str],
    rng: random.Random,
) -> dict[str, Any]:
    print(f"\n=== Evaluating layout: {layout.name} ===")
    out: dict[str, Any] = {
        "layout_name": layout.name,
        "world_w": layout.world_w,
        "world_h": layout.world_h,
        "n_kits": int(layout.coords.shape[0]),
    }
    print("  [§4.1] pair-correlation ...")
    out["pair_correlation"] = sample_pair_correlation(
        mat, weights, layout.coords, n_pairs=N_PAIR_SAMPLE, rng=rng
    )
    print(f"    spearman={out['pair_correlation']['spearman_r']:.4f}  kendall={out['pair_correlation']['kendall_tau']:.4f}")
    print("  [§4.2] kNN purity + substrate ratio ...")
    out["knn_purity"] = knn_substrate_purity_and_ratio(
        mat, weights, layout.coords, primary_elements, k=K_NN, rng=rng
    )
    print(f"    purity@k={K_NN}: {out['knn_purity']['overall_purity_mean']:.4f}  "
          f"knn/random ratio: {out['knn_purity']['overall_knn_over_random_ratio']:.4f}")
    print("  [§4.3] per-element MDS stress ...")
    out["per_element_stress"] = per_element_mds_stress(
        mat, weights, layout.coords, primary_elements,
        sample_pairs_per_element=1500, rng=rng,
    )
    print(f"    mean Kruskal stress-1: {out['per_element_stress']['mean_kruskal_stress_1']:.4f}  "
          f"mean within-element spearman: {out['per_element_stress']['mean_within_element_spearman']:.4f}")
    print("  [§4.4] anchor proximity check ...")
    out["anchor_proximity"] = anchor_proximity_check(layout, primary_elements)
    return out


# -----------------------------------------------------------------------------
# § E. Main
# -----------------------------------------------------------------------------

def main() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    rng = random.Random(SEED)

    print("[1] loading substrate ...")
    prim, kits, fam_map = load_substrate()
    print(f"    primitives: {len(prim)}    kits: {len(kits)}")

    # canonical kit_id order
    kit_ids = kits["kit_id"].tolist()
    primitive_sets = parse_primitive_sets(kits)
    primary_elements = kits["primary_element"].tolist()

    # universe of primitives that appear in any kit
    all_prims = sorted({p for s in primitive_sets for p in s})
    print(f"    primitive universe (kit-referenced): {len(all_prims)}")

    weights = build_weight_lookup(all_prims, fam_map)
    fam_counts = Counter(family_of(p, fam_map) for p in all_prims)
    print(f"    family distribution in universe: {dict(fam_counts)}")

    print("[2] building membership matrix ...")
    mat = build_membership_matrix(primitive_sets, all_prims)
    print(f"    matrix shape {mat.shape}  density {mat.sum() / mat.size:.4f}")

    print("[3] loading layouts ...")
    layouts: list[Layout] = []
    if RADIAL_LAYOUT.exists():
        layouts.append(load_layout(RADIAL_LAYOUT, "radial_baseline", kit_ids))
    if FORCE_LAYOUT.exists():
        layouts.append(load_layout(FORCE_LAYOUT, "force_directed", kit_ids))
    print(f"    loaded {len(layouts)} layouts: {[l.name for l in layouts]}")

    results: dict[str, Any] = {
        "_meta": {
            "date": "2026-06-09",
            "author": "elrond",
            "commission": "Hotspot A substrate-vector proximity (Discipline #18.2)",
            "methodology_note": "agentic_orchestration/elrond/notes/2026-06-09-hotspot-a-substrate-vector-proximity-methodology.md",
            "substrate_root": str(SUBSTRATE_DIR),
            "n_kits": int(len(kits)),
            "n_primitives_in_universe": int(len(all_prims)),
            "family_weights": FAMILY_WEIGHTS,
            "default_family_weight": DEFAULT_FAMILY_WEIGHT,
            "n_pair_sample": N_PAIR_SAMPLE,
            "k_nn": K_NN,
            "seed": SEED,
        },
        "layouts": [],
    }
    for layout in layouts:
        results["layouts"].append(evaluate_layout(
            layout, mat, weights, primary_elements, rng,
        ))

    out_path = OUT_ROOT / "results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[4] wrote {out_path}")

    # Print compact comparison summary
    print("\n=== SUMMARY ===")
    print(f"{'layout':<22} {'spearman':>10} {'kendall':>10} {'purity@5':>10} {'knn/rand':>10} {'stress-1':>10} {'wgrp_sp':>10}")
    for r in results["layouts"]:
        print(
            f"{r['layout_name']:<22} "
            f"{r['pair_correlation']['spearman_r']:>10.4f} "
            f"{r['pair_correlation']['kendall_tau']:>10.4f} "
            f"{r['knn_purity']['overall_purity_mean']:>10.4f} "
            f"{r['knn_purity']['overall_knn_over_random_ratio']:>10.4f} "
            f"{r['per_element_stress']['mean_kruskal_stress_1']:>10.4f} "
            f"{r['per_element_stress']['mean_within_element_spearman']:>10.4f} "
        )
    print()
    print("Interpretation key:")
    print("  spearman / kendall: higher = spatial distance better tracks substrate distance globally")
    print("  purity@5: higher = spatial neighbours share primary element (face-level cluster check)")
    print("  knn/rand: <1 means kNN substrate distance < random — layout preserves substrate proximity")
    print("  stress-1: lower = layout faithfully reproduces substrate distance WITHIN element")
    print("  wgrp_sp: higher = WITHIN element, spatial distance tracks substrate distance")


if __name__ == "__main__":
    main()
