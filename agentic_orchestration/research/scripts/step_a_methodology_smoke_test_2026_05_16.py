"""
Step A — Emergent-grouping methodology smoke test on Pimen substrate.

Dispatch: agentic_orchestration/dispatches/2026-05-16-elrond-step-a-methodology-smoke-test.md
Author:   elrond
Date:     2026-05-16

Purpose:
    Validate that the emergent-grouping methodology produces COHERENT
    clusters on the 46-pack Pimen substrate (small enough to verify by
    hand). Binary verdict: green-light Step B / red-light Step B.

    NOT a cipher-width determination. NOT an outcome extrapolation.
    Methodology validation only.

Methodology (Section 1 of the findings):
    Feature representation : two-track. (1) Content features from style_tags
                              — element-family membership and mechanic-family
                              membership (collapsed from the 22 fragmented
                              mechanic-leaning tags to a controlled vocabulary
                              of 7 mechanic-families per pre-inventory § 2.8).
                              (2) Form features from rubric axes that ARE
                              populated — derived_register, resolution_band
                              (treating 'unknown' as its own value not as
                              missing), animation_frame_density, file_format,
                              cost_tier. Three 100%-unknown axes
                              (palette_size, shading_technique, linework_style)
                              are EXCLUDED per pre-inventory § 2.2.
    Distance metric        : Composite Gower-style — Jaccard on content tag-set
                              membership (binary one-hot), Hamming on form
                              categorical axes (one-hot). Weighted 0.6 content
                              / 0.4 form by default; sensitivity analyzed.
    Clustering algorithm   : Hierarchical agglomerative, average linkage.
                              n=47 makes O(n^2) free; dendrogram supports
                              hand-verification; no k-prior required (cut at
                              natural elbow).
    Coherence evaluation   : (a) silhouette score across k=2..8;
                              (b) cluster-purity against three independent
                              hand-labels (element-family, mechanic-family,
                              register-family); (c) hand-checkable
                              one-sentence semantic characterization;
                              (d) singleton-rate and dominant-cluster-share
                              as failure-mode detectors.

Outputs:
    Prints a section-by-section report to stdout suitable for paste into
    the findings file. Does NOT write to catalogue.db (read-only on curated
    per dispatch § Out of scope).
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

CURATED_JSONL = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "research/curated/pimen-catalogue-curated-2026-05-16.jsonl"
)

# ---------- Mechanic-family controlled vocabulary --------------------------
# Per pre-inventory § 2.8 the catalogue has 22 fragmented mechanic-leaning
# tags. To produce a usable feature axis we collapse them into 7 families
# defined by gestural/functional kinship. This is a methodology-design
# choice; documented openly so it can be challenged.
MECHANIC_FAMILIES: dict[str, set[str]] = {
    "buff-debuff-status": {"buff", "debuff", "status-effect", "magic"},
    "ambient-environmental": {"ambient", "environmental"},
    "smoke-dust": {"smoke", "dust"},
    "impact-burst": {"impact", "explosion", "hit-effect", "muzzle-flash"},
    "projectile-bullet": {"projectile", "bullet"},
    "melee-slash": {"slash", "thrust", "cutting", "smear"},
    "heal": {"heal", "healing"},
}

# Element-family controlled vocabulary (one-to-one with pimen-element tags).
# 'multi' kept separate because cross-element packs are a substrate-distinct
# class — they shouldn't be conflated with primary-element packs.
ELEMENT_FAMILIES = [
    "fire", "water", "earth", "wind", "thunder",
    "ice", "holy", "dark", "acid", "wood", "multi",
]

# Form-axis categorical values to one-hot encode. 'unknown' is preserved as
# its own value — the manual-review-pending state is a structurally distinct
# signal, not a missingness to impute.
FORM_AXES: dict[str, list[str]] = {
    "derived_register": [
        "hand-drawn-pixel", "retro-16bit", "manual-review",
        "clean-vector", "painterly-raster", "anime-cel",
    ],
    "resolution_band": [
        "tiny", "retro", "hd2d-pixel", "narrative-pixel",
        "cinematic-pixel", "raster", "vector", "unknown",
    ],
    "animation_frame_density": [
        "static", "low", "mid", "high", "cinematic", "unknown",
    ],
    "file_format": [
        "png", "png-spritesheet", "aseprite", "svg", "gif", "jpg",
        "mp4", "webm", "json-atlas", "tmx", "other", "unknown",
    ],
    "cost_tier": [
        "free", "paid-tier-03", "paid-tier-04", "paid-mid", "paid-bundle",
    ],
    "category": [
        "character", "enemy", "vfx", "environment", "ui",
        "audio", "tile", "icon", "portrait", "other",
    ],
}


def cost_tier(cost_usd: float) -> str:
    if cost_usd <= 0.0:
        return "free"
    if cost_usd < 4.0:
        return "paid-tier-03"
    if cost_usd < 7.0:
        return "paid-tier-04"
    if cost_usd < 15.0:
        return "paid-mid"
    return "paid-bundle"


def load_assets() -> list[dict]:
    with CURATED_JSONL.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def extract_element_family(asset: dict) -> str | None:
    for t in asset.get("style_tags", []):
        tag = t["tag"] if isinstance(t, dict) else t
        if tag.startswith("pimen-element:"):
            value = tag.split(":", 1)[1]
            return value if value in ELEMENT_FAMILIES else "multi"
    return None


def extract_mechanic_families(asset: dict) -> set[str]:
    raw = {t["tag"] if isinstance(t, dict) else t
           for t in asset.get("style_tags", [])}
    out: set[str] = set()
    for family, members in MECHANIC_FAMILIES.items():
        if raw & members:
            out.add(family)
    return out


def build_feature_matrix(assets: list[dict]) -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    """Build content (binary) and form (one-hot categorical) matrices.

    Returns
    -------
    content_matrix : (n, |elements|+|mechanics|) binary
    form_matrix    : (n, sum(|axis_values|)) one-hot
    content_labels : column names
    form_labels    : column names
    """
    n = len(assets)
    content_cols = [f"element:{e}" for e in ELEMENT_FAMILIES] + \
                   [f"mech:{m}" for m in MECHANIC_FAMILIES]
    content_matrix = np.zeros((n, len(content_cols)), dtype=np.int8)
    form_labels: list[str] = []
    for axis, values in FORM_AXES.items():
        for v in values:
            form_labels.append(f"{axis}:{v}")
    form_matrix = np.zeros((n, len(form_labels)), dtype=np.int8)

    for i, asset in enumerate(assets):
        elem = extract_element_family(asset)
        if elem is not None:
            content_matrix[i, ELEMENT_FAMILIES.index(elem)] = 1
        mechs = extract_mechanic_families(asset)
        for m in mechs:
            col_idx = len(ELEMENT_FAMILIES) + list(MECHANIC_FAMILIES).index(m)
            content_matrix[i, col_idx] = 1
        # form one-hot
        offset = 0
        for axis, values in FORM_AXES.items():
            val = asset.get(axis)
            if axis == "cost_tier":
                val = cost_tier(float(asset.get("cost_usd", 0.0)))
            if val in values:
                form_matrix[i, offset + values.index(val)] = 1
            offset += len(values)
    return content_matrix, form_matrix, content_cols, form_labels


def jaccard_distance_matrix(X: np.ndarray) -> np.ndarray:
    n = X.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            inter = int(np.bitwise_and(X[i], X[j]).sum())
            union = int(np.bitwise_or(X[i], X[j]).sum())
            d = 1.0 - (inter / union) if union > 0 else 1.0
            D[i, j] = D[j, i] = d
    return D


def hamming_distance_matrix(X: np.ndarray) -> np.ndarray:
    n, p = X.shape
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = D[j, i] = float((X[i] != X[j]).sum()) / p
    return D


def composite_distance(content_D: np.ndarray, form_D: np.ndarray,
                       w_content: float = 0.6) -> np.ndarray:
    return w_content * content_D + (1.0 - w_content) * form_D


def cluster_purity(labels: np.ndarray, hand: list[str | None]) -> float:
    """Cluster purity against a hand-label (None = unlabeled, excluded)."""
    by_cluster: dict[int, Counter] = defaultdict(Counter)
    total_labeled = 0
    for lbl, h in zip(labels, hand):
        if h is None:
            continue
        by_cluster[lbl][h] += 1
        total_labeled += 1
    if total_labeled == 0:
        return float("nan")
    correct = sum(max(c.values()) for c in by_cluster.values())
    return correct / total_labeled


def hand_label_element(asset: dict) -> str | None:
    return extract_element_family(asset)


def hand_label_mechanic(asset: dict) -> str | None:
    mechs = extract_mechanic_families(asset)
    if not mechs:
        return None
    # If only one family, that's the label. If multiple, pick the dominant
    # by a deterministic priority for hand-validation purposes.
    priority = ["heal", "melee-slash", "buff-debuff-status",
                "impact-burst", "projectile-bullet",
                "smoke-dust", "ambient-environmental"]
    for p in priority:
        if p in mechs:
            return p
    return None


def hand_label_register(asset: dict) -> str | None:
    reg = asset.get("derived_register")
    if reg in {"hand-drawn-pixel", "retro-16bit", "manual-review"}:
        return reg
    return None


def hand_label_category(asset: dict) -> str | None:
    return asset.get("category")


def characterize_cluster(members: list[dict]) -> str:
    """Produce a one-sentence semantic characterization."""
    elements = Counter(filter(None, (hand_label_element(a) for a in members)))
    mechanics = Counter(filter(None, (hand_label_mechanic(a) for a in members)))
    registers = Counter(a.get("derived_register") for a in members)
    categories = Counter(a.get("category") for a in members)
    costs = Counter(cost_tier(float(a.get("cost_usd", 0.0))) for a in members)

    parts = []
    if categories:
        cat, cn = categories.most_common(1)[0]
        if cn == len(members):
            parts.append(f"all-{cat}")
        else:
            parts.append(f"{cat}-dominant ({cn}/{len(members)})")
    if mechanics:
        m, mn = mechanics.most_common(1)[0]
        parts.append(f"mechanic={m} ({mn}/{len(members)})")
    elif elements:
        es = ",".join(sorted(elements.keys()))
        parts.append(f"elements=[{es}]")
    else:
        parts.append("no-element no-mechanic tag (form-only)")
    if registers:
        r, rn = registers.most_common(1)[0]
        parts.append(f"register={r} ({rn}/{len(members)})")
    if costs:
        c, cn = costs.most_common(1)[0]
        parts.append(f"cost={c} ({cn}/{len(members)})")
    return "; ".join(parts)


def run(weight_content: float = 0.6, k_range: range = range(2, 11)) -> None:
    assets = load_assets()
    n = len(assets)
    print(f"Loaded {n} assets from curated jsonl.")

    content_X, form_X, content_cols, form_cols = build_feature_matrix(assets)
    print(f"Content feature dims: {content_X.shape}  "
          f"(non-zero rows: {int((content_X.sum(axis=1) > 0).sum())})")
    print(f"Form feature dims:    {form_X.shape}")

    content_D = jaccard_distance_matrix(content_X)
    form_D = hamming_distance_matrix(form_X)

    print("\n=== SECTION 2.A — Cluster-count sweep (composite distance) ===")
    print(f"weight_content={weight_content:.2f}, weight_form={1-weight_content:.2f}")
    D = composite_distance(content_D, form_D, weight_content)
    condensed = squareform(D, checks=False)
    Z = linkage(condensed, method="average")

    hand_elem = [hand_label_element(a) for a in assets]
    hand_mech = [hand_label_mechanic(a) for a in assets]
    hand_reg = [hand_label_register(a) for a in assets]
    hand_cat = [hand_label_category(a) for a in assets]

    print(f"\n{'k':>3} {'sil':>7} {'purE':>6} {'purM':>6} {'purR':>6} {'purC':>6} "
          f"{'sgltn':>6} {'maxshare':>9}")
    sweep_rows = []
    for k in k_range:
        labels = fcluster(Z, t=k, criterion="maxclust")
        unique_k = len(set(labels))
        if unique_k < 2:
            continue
        sil = silhouette_score(D, labels, metric="precomputed")
        pE = cluster_purity(labels, hand_elem)
        pM = cluster_purity(labels, hand_mech)
        pR = cluster_purity(labels, hand_reg)
        pC = cluster_purity(labels, hand_cat)
        cluster_sizes = Counter(labels)
        singletons = sum(1 for s in cluster_sizes.values() if s == 1)
        max_share = max(cluster_sizes.values()) / n
        print(f"{k:>3} {sil:>7.3f} {pE:>6.2f} {pM:>6.2f} "
              f"{pR:>6.2f} {pC:>6.2f} {singletons:>6} {max_share:>9.2f}")
        sweep_rows.append((k, sil, pE, pM, pR, pC, singletons, max_share, labels))

    print("\n=== SECTION 2.B — Sensitivity sweep over weight_content ===")
    print(f"{'w_c':>5} {'k=4 sil':>9} {'k=5 sil':>9} {'k=6 sil':>9} {'k=7 sil':>9}")
    for w in [0.3, 0.5, 0.6, 0.7, 0.85, 1.0]:
        Dw = composite_distance(content_D, form_D, w)
        Zw = linkage(squareform(Dw, checks=False), method="average")
        sils = []
        for k in (4, 5, 6, 7):
            lbl = fcluster(Zw, t=k, criterion="maxclust")
            if len(set(lbl)) < 2:
                sils.append(float("nan"))
                continue
            sils.append(silhouette_score(Dw, lbl, metric="precomputed"))
        print(f"{w:>5.2f} {sils[0]:>9.3f} {sils[1]:>9.3f} "
              f"{sils[2]:>9.3f} {sils[3]:>9.3f}")

    # Pick the k that maximizes silhouette in mid-range (avoid trivial k=2
    # and degenerate large-k); pick best from k=3..k=8 inclusive.
    candidate = [r for r in sweep_rows if 3 <= r[0] <= 8]
    best = max(candidate, key=lambda r: r[1])
    k_best, sil_best, pE_best, pM_best, pR_best, pC_best, sgl, mxs, labels_best = best

    print(f"\n=== SECTION 2.C — Selected cut: k={k_best} ===")
    print(f"silhouette={sil_best:.3f}  purity(elem)={pE_best:.2f}  "
          f"purity(mech)={pM_best:.2f}  purity(reg)={pR_best:.2f}  "
          f"purity(cat)={pC_best:.2f}  singletons={sgl}  "
          f"max_cluster_share={mxs:.2f}")

    print("\n=== SECTION 2.D — Per-cluster characterization ===")
    by_cluster: dict[int, list[dict]] = defaultdict(list)
    for asset, lbl in zip(assets, labels_best):
        by_cluster[lbl].append(asset)
    for lbl in sorted(by_cluster):
        members = by_cluster[lbl]
        char = characterize_cluster(members)
        print(f"\nCluster {lbl} (n={len(members)}): {char}")
        for a in members:
            print(f"   - {a['name']}")

    print("\n=== SECTION 2.E — Failure-mode checks ===")
    n_clusters_with_one = sum(1 for c in by_cluster.values() if len(c) == 1)
    max_share = max(len(c) for c in by_cluster.values()) / n
    print(f"singleton clusters         : {n_clusters_with_one} "
          f"({'OK' if n_clusters_with_one <= 1 else 'WARN'})")
    print(f"max single-cluster share   : {max_share:.2f} "
          f"({'OK' if max_share < 0.6 else 'WARN'})")
    print(f"silhouette                 : {sil_best:.3f} "
          f"({'OK' if sil_best > 0.15 else 'WARN' if sil_best > 0.0 else 'FAIL'})")
    print(f"purity(category)           : {pC_best:.2f} "
          f"(sanity: vfx-dominant corpus should give high purity-cat unless "
          f"clusters mix vfx with character/enemy)")
    print(f"purity(register)           : {pR_best:.2f} "
          f"(should be high if register is a load-bearing axis)")
    print(f"purity(mechanic) [labeled] : {pM_best:.2f} "
          f"(labeled rows only; null-mechanic rows excluded)")
    print(f"purity(element)  [labeled] : {pE_best:.2f} "
          f"(labeled rows only; null-element rows excluded)")


if __name__ == "__main__":
    weight = 0.6
    if len(sys.argv) > 1:
        weight = float(sys.argv[1])
    run(weight)
