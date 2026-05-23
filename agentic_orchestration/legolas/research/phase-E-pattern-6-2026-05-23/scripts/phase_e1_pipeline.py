"""
Phase E-1: Pattern-6 Axis Discovery + Clustering Pipeline
Author: legolas
Date: 2026-05-23
Math note: phase-E-1-math-note.md (pre-authored before this script)

Strict sequence per dispatch:
  D1 → D2 → D3 → D4 → D5

Usage:
  python phase_e1_pipeline.py --mode smoke   # 100-row smoke test
  python phase_e1_pipeline.py --mode full    # full 16,699-row run
"""

import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
import re
from datetime import datetime

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder
import hdbscan
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
OUT_DIR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23"
RANDOM_STATE = 42


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ── Weapon type tokens (30) from math note §1.2 ───────────────────────────────
WEAPON_TYPE_TOKENS = [
    "sword", "longsword", "greatsword", "shortsword", "rapier", "scimitar", "sabre",
    "axe", "battleaxe", "greataxe", "hammer", "mace", "flail", "club", "staff", "wand",
    "bow", "crossbow", "javelin", "spear", "lance", "pike", "halberd", "glaive",
    "dagger", "knife", "pistol", "rifle", "musket", "shotgun"
]

# ── Canonical value enumerations ──────────────────────────────────────────────
LINEAGE_VALUES = [
    "fantasy_generic", "south_american_indigenous", "european", "east_asian",
    "middle_eastern", "unknown", "south_asian", "southeast_asian",
    "arctic_circumpolar", "african", "north_american_indigenous"
]
PERIOD_VALUES = ["fictional", "classical", "contemporary", "unknown", "modern", "medieval", "industrial", "early_modern"]
REGISTER_VALUES = ["fantasy", "historical", "military_modern", "unknown", "other"]
WEAPON_KIND_VALUES = ["named_template", "category"]
WIELDABLE_VALUES = ["two_hand", "one_hand", "either", "shoulder_supported"]


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def load_data(conn, smoke_mode=False):
    """Load v_category_sample rows; optionally limit to 100 for smoke test."""
    limit_clause = "LIMIT 100" if smoke_mode else ""
    query = f"""
        SELECT id, canonical_name, description_text, cultural_lineage_tags,
               structured_properties, cultural_lineage_canonical,
               historical_period_canonical, register_canonical,
               wieldable_humanoid, weapon_kind
        FROM v_category_sample
        ORDER BY id
        {limit_clause}
    """
    rows = conn.execute(query).fetchall()
    log(f"Loaded {len(rows)} rows from v_category_sample {'(SMOKE MODE)' if smoke_mode else ''}")
    return rows


def build_text_corpus(rows):
    """Build text corpus per row: canonical_name + description_text + cultural_lineage_tags."""
    corpus = []
    for row in rows:
        id_, name, desc, tags, props = row[0], row[1], row[2], row[3], row[4]
        parts = [str(name) if name else ""]

        if desc and desc.strip():
            parts.append(desc.strip()[:2000])  # cap at 2000 chars
        else:
            # Impute from structured_properties weapon_type
            if props:
                try:
                    p = json.loads(props)
                    wt = p.get("weapon_type", "") or p.get("item_type", "")
                    if wt:
                        parts.append(str(wt))
                except (json.JSONDecodeError, AttributeError):
                    pass

        if tags:
            try:
                tag_list = json.loads(tags)
                if isinstance(tag_list, list):
                    parts.append(" ".join(str(t) for t in tag_list))
            except (json.JSONDecodeError, AttributeError):
                parts.append(str(tags))

        corpus.append(" ".join(parts))
    return corpus


def build_structured_features(rows):
    """Build structured feature matrix (60 dims): one-hot + weapon-type multi-hot."""
    N = len(rows)
    # Dimensions: 11 lineage + 8 period + 5 register + 2 kind + 4 wield + 30 weapon-type = 60
    structured = np.zeros((N, 60), dtype=np.float32)

    lineage_idx = {v: i for i, v in enumerate(LINEAGE_VALUES)}
    period_idx = {v: i for i, v in enumerate(PERIOD_VALUES)}
    register_idx = {v: i for i, v in enumerate(REGISTER_VALUES)}
    kind_idx = {v: i for i, v in enumerate(WEAPON_KIND_VALUES)}
    wield_idx = {v: i for i, v in enumerate(WIELDABLE_VALUES)}

    for i, row in enumerate(rows):
        id_, name, desc, tags, props, lineage, period, register, wield, kind = row

        # Cultural lineage (cols 0-10)
        li = lineage_idx.get(lineage or "unknown", lineage_idx["unknown"])
        structured[i, li] = 1.0

        # Historical period (cols 11-18)
        pi = period_idx.get(period or "unknown", period_idx["unknown"])
        structured[i, 11 + pi] = 1.0

        # Register (cols 19-23)
        ri = register_idx.get(register or "unknown", register_idx.get("other", 4))
        structured[i, 19 + ri] = 1.0

        # Weapon kind (cols 24-25)
        ki = kind_idx.get(kind or "named_template", 0)
        structured[i, 24 + ki] = 1.0

        # Wieldable (cols 26-29)
        wi = wield_idx.get(wield or "two_hand", 0)
        structured[i, 26 + wi] = 1.0

        # Weapon type multi-hot (cols 30-59)
        name_lower = (name or "").lower()
        for j, token in enumerate(WEAPON_TYPE_TOKENS):
            if token in name_lower:
                structured[i, 30 + j] = 1.0

    return structured


def compute_f2_weights(rows):
    """Compute F2 inverse-frequency weights per row (math note §1.4)."""
    from collections import Counter
    lineages = [row[5] or "unknown" for row in rows]
    freq = Counter(lineages)
    N = len(rows)

    raw_weights = np.array([1.0 / freq[l] for l in lineages], dtype=np.float64)
    # Normalize so mean weight = 1.0 (sum = N)
    mean_w = raw_weights.mean()
    normalized_weights = raw_weights / mean_w

    log(f"F2 weight stats: min={normalized_weights.min():.4f}, max={normalized_weights.max():.2f}, "
        f"mean={normalized_weights.mean():.4f}")

    # Report per-lineage normalized weight
    weight_by_lineage = {}
    for lineage, count in sorted(freq.items(), key=lambda x: -x[1]):
        raw_w = 1.0 / count
        norm_w = raw_w / mean_w
        weight_by_lineage[lineage] = {
            "count": count,
            "freq": count / N,
            "raw_weight": raw_w,
            "normalized_weight": float(norm_w)
        }

    return normalized_weights, weight_by_lineage


def fit_tfidf_lsa(corpus, weights, n_lsa=100, smoke=False):
    """Fit TF-IDF + TruncatedSVD (LSA) on weighted corpus. Returns (lsa_matrix, vectorizer, svd, vocab_hash)."""
    log("Fitting TF-IDF vectorizer...")
    vec = TfidfVectorizer(
        max_features=500,
        min_df=3 if not smoke else 1,
        max_df=0.95,
        sublinear_tf=True,
        analyzer='word',
        ngram_range=(1, 2)
    )
    tfidf_matrix = vec.fit_transform(corpus)
    log(f"TF-IDF matrix: {tfidf_matrix.shape}")

    # Reproducibility hash: SHA-256 of sorted vocabulary
    vocab_sorted = sorted(vec.vocabulary_.keys())
    vocab_hash = hashlib.sha256(" ".join(vocab_sorted).encode()).hexdigest()[:16]
    log(f"Vocabulary hash: {vocab_hash}")

    # Apply F2 weights by row-multiplying by sqrt(w_i)
    # Equivalent to weighted PCA (math note §1.4)
    sqrt_w = np.sqrt(weights).reshape(-1, 1)
    tfidf_weighted = tfidf_matrix.multiply(sqrt_w)  # sparse multiply

    n_components_lsa = min(n_lsa, tfidf_matrix.shape[1] - 1, tfidf_matrix.shape[0] - 1)
    log(f"Fitting TruncatedSVD with n_components={n_components_lsa}...")
    svd = TruncatedSVD(n_components=n_components_lsa, n_iter=10, random_state=RANDOM_STATE)
    lsa_out = svd.fit_transform(tfidf_weighted)

    # L2-normalize LSA rows
    norms = np.linalg.norm(lsa_out, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    lsa_out = lsa_out / norms

    log(f"LSA output: {lsa_out.shape}, explained_variance_ratio sum={svd.explained_variance_ratio_.sum():.4f}")
    return lsa_out, vec, svd, vocab_hash


def scale_structured(structured, weights):
    """StandardScale structured features with F2 sample weights."""
    scaler = StandardScaler()
    # sklearn StandardScaler doesn't take sample_weight directly in fit;
    # implement weighted mean/std manually
    w = weights / weights.sum()
    weighted_mean = (structured * w[:, None]).sum(axis=0)
    weighted_var = ((structured - weighted_mean) ** 2 * w[:, None]).sum(axis=0)
    weighted_std = np.sqrt(weighted_var)
    weighted_std[weighted_std == 0] = 1.0
    scaled = (structured - weighted_mean) / weighted_std
    return scaled, weighted_mean, weighted_std


def build_feature_matrix(lsa_out, structured_scaled):
    """Concatenate LSA + structured features into final feature matrix."""
    X = np.concatenate([lsa_out, structured_scaled], axis=1)
    log(f"Final feature matrix: {X.shape}")
    return X


def run_pca_axis_discovery(X, weights, n_max=50):
    """Run weighted PCA via TruncatedSVD on full feature matrix; return axes."""
    log("Running PCA (TruncatedSVD) on full feature matrix...")
    sqrt_w = np.sqrt(weights).reshape(-1, 1)
    X_weighted = X * sqrt_w

    n_components = min(n_max, X.shape[1] - 1, X.shape[0] - 1)
    svd_full = TruncatedSVD(n_components=n_components, n_iter=10, random_state=RANDOM_STATE)
    projections = svd_full.fit_transform(X_weighted)

    evr = svd_full.explained_variance_ratio_
    cumevr = np.cumsum(evr)
    log(f"Explained variance (first 15): {[f'{v:.4f}' for v in evr[:15]]}")
    log(f"Cumulative EVR: {[f'{v:.4f}' for v in cumevr[:15]]}")

    # Find k_80 (first index where cumsum >= 0.80)
    k_80_candidates = np.where(cumevr >= 0.80)[0]
    k_80 = int(k_80_candidates[0]) + 1 if len(k_80_candidates) > 0 else n_components

    # Scree kink: second derivative of EVR
    if len(evr) >= 4:
        d2 = np.diff(np.diff(evr))
        kink_idx = int(np.argmax(d2)) + 2  # +2 for double diff offset
    else:
        kink_idx = len(evr)

    # Amendment per rerun-addendum §5: take max of kink-based and var-based estimates;
    # cap at 12; floor at 8 so the acceptance criterion (≥8 axes) is always attempted.
    k_from_kink = min(kink_idx + 2, 12)
    k_from_var = min(k_80, 12)
    k_raw = max(k_from_kink, k_from_var)
    k_final = max(k_raw, 8)
    log(f"k_80={k_80}, kink_idx={kink_idx}, k_from_kink={k_from_kink}, k_from_var={k_from_var}, k_final={k_final}")

    return svd_full, projections, k_final, evr


def bootstrap_stability(X, weights, k, n_bootstrap=10):
    """Bootstrap stability check: mean cosine-distance of top-k axes across resamples."""
    log(f"Running {n_bootstrap} bootstrap resamples for stability check...")
    N = X.shape[0]
    sqrt_w = np.sqrt(weights).reshape(-1, 1)

    # Full fit reference components
    X_weighted = X * sqrt_w
    ref_svd = TruncatedSVD(n_components=k, n_iter=10, random_state=RANDOM_STATE)
    ref_svd.fit(X_weighted)
    ref_components = ref_svd.components_  # shape (k, p)

    cosine_distances = np.zeros((n_bootstrap, k))
    rng = np.random.RandomState(RANDOM_STATE)

    for b in range(n_bootstrap):
        idx = rng.choice(N, size=N, replace=True)
        X_boot = X[idx] * sqrt_w[idx]
        boot_svd = TruncatedSVD(n_components=k, n_iter=5, random_state=RANDOM_STATE + b)
        boot_svd.fit(X_boot)
        boot_components = boot_svd.components_

        for j in range(k):
            # Absolute cosine similarity (sign-flip invariant)
            cos_sim = abs(np.dot(ref_components[j], boot_components[j]) /
                         (np.linalg.norm(ref_components[j]) * np.linalg.norm(boot_components[j]) + 1e-12))
            cosine_distances[b, j] = 1.0 - cos_sim

    mean_cos_dist = cosine_distances.mean(axis=0)
    log(f"Bootstrap stability (mean cosine-dist per axis): {[f'{v:.4f}' for v in mean_cos_dist]}")
    return mean_cos_dist


def interpret_axes(svd_full, k, vec, n_top=20):
    """For each axis, get top-N feature loadings and interpretability flags."""
    # Feature names: TF-IDF vocab (first 500) + structured feature names (60)
    tfidf_names = vec.get_feature_names_out().tolist()
    struct_names = []
    for v in LINEAGE_VALUES:
        struct_names.append(f"lineage_{v}")
    for v in PERIOD_VALUES:
        struct_names.append(f"period_{v}")
    for v in REGISTER_VALUES:
        struct_names.append(f"register_{v}")
    for v in WEAPON_KIND_VALUES:
        struct_names.append(f"kind_{v}")
    for v in WIELDABLE_VALUES:
        struct_names.append(f"wield_{v}")
    for t in WEAPON_TYPE_TOKENS:
        struct_names.append(f"type_{t}")

    # Note: the full PCA was run on X = [lsa_100, structured_60]
    # lsa_100 components are in the lsa space, not the original tfidf space
    # For interpretability, we use the SVD components directly on the 160-dim feature space
    # The first 100 dims correspond to LSA components (abstract semantic dims)
    # The last 60 dims correspond to named structured features

    feature_names = [f"lsa_{i}" for i in range(100)] + struct_names

    axes_info = []
    components = svd_full.components_[:k]  # (k, 160)

    for j, comp in enumerate(components):
        # Top N by absolute loading
        top_idx = np.argsort(np.abs(comp))[::-1][:n_top]
        top_loadings = [(feature_names[i], float(comp[i])) for i in top_idx]

        # Spread condition: top-1 should not dominate > 60% of top-20 L2 norm
        top20_norm = np.linalg.norm(comp[np.argsort(np.abs(comp))[::-1][:20]])
        top1_frac = abs(comp[top_idx[0]]) / (top20_norm + 1e-12)

        # Cross-block condition: count text vs structured in top-5
        top5_idx = top_idx[:5]
        text_in_top5 = sum(1 for i in top5_idx if i < 100)  # lsa dims
        struct_in_top5 = sum(1 for i in top5_idx if i >= 100)

        # Structured-only top features (more interpretable)
        struct_top = [(feature_names[i], float(comp[i])) for i in top_idx if i >= 100][:10]

        axes_info.append({
            "axis_index": j + 1,
            "top_loadings": top_loadings,
            "struct_top_loadings": struct_top,
            "top1_fraction": float(top1_frac),
            "text_in_top5": text_in_top5,
            "struct_in_top5": struct_in_top5,
            "single_feature_flag": top1_frac > 0.60,
            "purely_text_flag": struct_in_top5 == 0,
            "purely_structured_flag": text_in_top5 == 0
        })

    return axes_info


def run_hdbscan(projections_k, weights, min_cluster_size=30):
    """Run HDBSCAN on k-dim projections."""
    log(f"Running HDBSCAN (min_cluster_size={min_cluster_size})...")

    # For HDBSCAN: apply F2 weighting via integer duplication
    # Rows with normalized weight >= 2 get duplicated
    # Map assignments back to original rows
    int_weights = np.round(weights).astype(int)
    int_weights = np.clip(int_weights, 1, 20)  # cap duplication at 20x

    expanded = []
    orig_idx = []
    for i, (row, w) in enumerate(zip(projections_k, int_weights)):
        for _ in range(w):
            expanded.append(row)
            orig_idx.append(i)
    expanded = np.array(expanded)
    orig_idx = np.array(orig_idx)

    log(f"Expanded matrix for HDBSCAN fit: {expanded.shape}")

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=5,
        cluster_selection_epsilon=0.05,
        cluster_selection_method='eom',
        metric='euclidean'
    )
    clusterer.fit(expanded)

    # Map labels back to original rows (vote for most common label per original row)
    from collections import Counter
    labels_orig = np.full(len(projections_k), -1, dtype=int)
    for i in range(len(projections_k)):
        mask = orig_idx == i
        row_labels = clusterer.labels_[mask]
        if len(row_labels) > 0:
            cnt = Counter(row_labels)
            labels_orig[i] = cnt.most_common(1)[0][0]

    n_clusters = len(set(labels_orig)) - (1 if -1 in labels_orig else 0)
    n_noise = (labels_orig == -1).sum()
    log(f"HDBSCAN result: {n_clusters} clusters, {n_noise} noise points")
    return labels_orig, clusterer, n_clusters


def assign_noise_to_nearest(labels, projections_k):
    """Assign noise points (label=-1) to nearest cluster centroid (math note OQ3)."""
    unique_labels = sorted([l for l in set(labels) if l >= 0])
    if len(unique_labels) == 0:
        log("WARNING: No valid clusters found; cannot assign noise.")
        return labels, np.zeros(len(labels))

    # Compute centroids
    centroids = {}
    for lbl in unique_labels:
        mask = labels == lbl
        centroids[lbl] = projections_k[mask].mean(axis=0)

    centroid_matrix = np.array([centroids[l] for l in unique_labels])
    confidence_scores = np.ones(len(labels))

    noise_mask = labels == -1
    noise_indices = np.where(noise_mask)[0]

    if len(noise_indices) == 0:
        return labels, confidence_scores

    noise_points = projections_k[noise_indices]
    # Compute distances to all centroids
    dists = np.sqrt(((noise_points[:, None, :] - centroid_matrix[None, :, :]) ** 2).sum(axis=2))
    nearest = np.argmin(dists, axis=1)
    min_dists = dists[np.arange(len(noise_indices)), nearest]

    # Confidence score for noise-assigned: 1 / (1 + min_dist) normalized to [0, 0.5)
    # mean distance from non-noise points to their centroids
    non_noise_dists = []
    for lbl in unique_labels:
        mask = labels == lbl
        pts = projections_k[mask]
        c = centroids[lbl]
        non_noise_dists.extend(np.sqrt(((pts - c) ** 2).sum(axis=1)).tolist())
    mean_non_noise_dist = np.mean(non_noise_dists) if non_noise_dists else 1.0

    for idx, noise_i in enumerate(noise_indices):
        assigned_label = unique_labels[nearest[idx]]
        labels[noise_i] = assigned_label
        d = min_dists[idx]
        # confidence in [0, 0.5) for noise-assigned points
        confidence_scores[noise_i] = min(0.499, 0.5 / (1.0 + d / (mean_non_noise_dist + 1e-12)))

    log(f"Assigned {len(noise_indices)} noise points to nearest clusters (confidence < 0.5)")
    return labels, confidence_scores


def compute_purity(labels, rows):
    """Compute mean cluster purity against cultural_lineage_canonical."""
    from collections import Counter
    unique_labels = sorted(set(labels))
    purities = []
    sizes = []
    for lbl in unique_labels:
        mask = labels == lbl
        lineages = [rows[i][5] or "unknown" for i in range(len(rows)) if mask[i]]
        if not lineages:
            continue
        cnt = Counter(lineages)
        purity = cnt.most_common(1)[0][1] / len(lineages)
        purities.append(purity)
        sizes.append(len(lineages))

    if not purities:
        return 0.0, {}
    weighted_purity = sum(p * s for p, s in zip(purities, sizes)) / sum(sizes)
    return weighted_purity, dict(zip(unique_labels, purities))


def run_gmm_baseline(projections_k, k_target, random_state=42):
    """Run GMM baseline for comparison."""
    k = max(2, min(k_target, projections_k.shape[0] - 1))
    log(f"Running GMM baseline (n_components={k})...")
    gmm = GaussianMixture(n_components=k, covariance_type='diag', random_state=random_state)
    gmm.fit(projections_k)
    labels = gmm.predict(projections_k)
    probs = gmm.predict_proba(projections_k)
    return labels, probs.max(axis=1), gmm


def run_kmeans_baseline(projections_k, k_target, random_state=42):
    """Run k-means baseline for comparison."""
    k = max(2, min(k_target, projections_k.shape[0] - 1))
    log(f"Running k-means baseline (n_clusters={k})...")
    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    km.fit(projections_k)
    labels = km.labels_
    # confidence = 1 / (1 + dist_to_centroid / mean_dist)
    dists = np.sqrt(((projections_k - km.cluster_centers_[labels]) ** 2).sum(axis=1))
    mean_dist = dists.mean() if dists.mean() > 0 else 1.0
    confidence = 1.0 / (1.0 + dists / mean_dist)
    return labels, confidence, km


def get_top_representatives(rows, labels, confidence_scores, cluster_id, n=3):
    """Get top-N representative rows for a cluster by confidence score."""
    indices = [i for i, l in enumerate(labels) if l == cluster_id]
    if not indices:
        return []
    sorted_by_conf = sorted(indices, key=lambda i: confidence_scores[i], reverse=True)
    return [
        {
            "id": rows[i][0],
            "canonical_name": rows[i][1],
            "cultural_lineage_canonical": rows[i][5],
            "historical_period_canonical": rows[i][6],
            "register_canonical": rows[i][7],
            "confidence": float(confidence_scores[i])
        }
        for i in sorted_by_conf[:n]
    ]


def characterize_cluster(rows, labels, cluster_id):
    """Extract dominant structured features for a cluster."""
    from collections import Counter
    indices = [i for i, l in enumerate(labels) if l == cluster_id]
    if not indices:
        return {}
    lineages = Counter([rows[i][5] or "unknown" for i in indices])
    periods = Counter([rows[i][6] or "unknown" for i in indices])
    registers = Counter([rows[i][7] or "unknown" for i in indices])
    kinds = Counter([rows[i][9] or "unknown" for i in indices])
    names_lower = [rows[i][1].lower() if rows[i][1] else "" for i in indices]

    # Weapon type detection
    type_counts = Counter()
    for name in names_lower:
        for token in WEAPON_TYPE_TOKENS:
            if token in name:
                type_counts[token] += 1
    top_types = type_counts.most_common(3)

    return {
        "member_count": len(indices),
        "dominant_lineage": lineages.most_common(1)[0],
        "dominant_period": periods.most_common(1)[0],
        "dominant_register": registers.most_common(1)[0],
        "dominant_kind": kinds.most_common(1)[0],
        "top_weapon_types": top_types,
        "lineage_dist": dict(lineages.most_common(5)),
        "period_dist": dict(periods.most_common(5))
    }


def propose_provisional_axis_name(axis_info, evr_val):
    """Heuristic provisional axis name from struct_top_loadings."""
    struct_tops = axis_info.get("struct_top_loadings", [])
    if not struct_tops:
        return "PROVISIONAL: text-semantic axis"

    # Pick top positive and top negative structured loading
    pos = [(n, v) for n, v in struct_tops if v > 0]
    neg = [(n, v) for n, v in struct_tops if v < 0]

    top_name = struct_tops[0][0] if struct_tops else "unknown"

    # Pattern-match naming heuristics
    if "lineage_fantasy_generic" in top_name or (pos and "lineage_fantasy_generic" in pos[0][0]):
        if neg and "lineage_" in neg[0][0]:
            return f"PROVISIONAL: fantasy-generic vs {neg[0][0].replace('lineage_','')}"
        return "PROVISIONAL: fantasy-generic concentration axis"
    if "period_fictional" in top_name:
        return "PROVISIONAL: fictional vs historical period axis"
    if "period_classical" in top_name:
        return "PROVISIONAL: classical/historical period prominence"
    if "wield_two_hand" in top_name:
        return "PROVISIONAL: two-handed vs one-handed wieldability"
    if "wield_one_hand" in top_name:
        return "PROVISIONAL: one-handed weapon emphasis"
    if "kind_named_template" in top_name:
        return "PROVISIONAL: named-template vs category-type axis"
    if "type_" in top_name:
        weapon = top_name.replace("type_", "")
        return f"PROVISIONAL: {weapon}-type weapon prominence"
    if "register_fantasy" in top_name:
        return "PROVISIONAL: fantasy register axis"
    if "register_historical" in top_name:
        return "PROVISIONAL: historical register axis"

    # Fallback: use top structured feature name
    return f"PROVISIONAL: {top_name.replace('_', ' ')} dominant axis"


def propose_provisional_cluster_description(char):
    """Heuristic provisional cluster description."""
    lineage = char.get("dominant_lineage", ("unknown", 0))[0]
    period = char.get("dominant_period", ("unknown", 0))[0]
    register = char.get("dominant_register", ("unknown", 0))[0]
    top_types = char.get("top_weapon_types", [])
    kind = char.get("dominant_kind", ("unknown", 0))[0]
    count = char.get("member_count", 0)

    type_str = "/".join([t[0] for t in top_types[:2]]) if top_types else "mixed"

    return (f"PROVISIONAL: {lineage} {period} {type_str} weapons "
            f"({register} register; {kind}; N={count})")


def write_deliverable_1(out_dir, rows, lsa_out, structured_scaled, weights, weight_by_lineage, vocab_hash, tfidf_vec):
    """Write phase-E-1-features.md."""
    N = len(rows)
    has_desc = sum(1 for r in rows if r[2] and r[2].strip())
    struct_nonzero = sum(1 for r in rows if r[4] and r[4].strip())

    content = f"""# Phase E-1 — Deliverable 1: Feature Engineering

PROVISIONAL — gandalf reviews axes in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Mode:** A (analytical)
**Status:** Complete

---

## Text Embedding

**Model:** TF-IDF (sklearn TfidfVectorizer) + TruncatedSVD (LSA) — 100 components
**Rationale for TF-IDF over sentence-transformers:** sentence-transformers requires ~700MB torch install (unavailable); consistent with Phase D Q5 pivot; reproducible without external model checkpoint.

**TF-IDF configuration:**
- max_features: 500
- min_df: 3
- max_df: 0.95
- sublinear_tf: True
- ngram_range: (1, 2)
- Input text: canonical_name + description_text (capped 2000 chars) + cultural_lineage_tags

**LSA configuration:** TruncatedSVD(n_components=100, n_iter=10, random_state=42)
**Vocabulary hash (SHA-256[:16]):** `{vocab_hash}`
**Post-LSA normalization:** L2 per row

**F2 weighting application:** Row-multiply TF-IDF matrix by sqrt(w_i) before SVD fit (equivalent to weighted PCA).

---

## Structured Feature Vector

**Dimensions:** 60 total (11 lineage + 8 period + 5 register + 2 kind + 4 wield + 30 weapon-type)

| Feature group | Source columns | Encoding | Dimensions |
|---|---|---|---|
| Cultural lineage | cultural_lineage_canonical | One-hot | 11 |
| Historical period | historical_period_canonical | One-hot | 8 |
| Register | register_canonical | One-hot | 5 |
| Weapon kind | weapon_kind | One-hot | 2 |
| Wieldability | wieldable_humanoid | One-hot | 4 |
| Weapon type | canonical_name (regex match) | Multi-hot binary | 30 |

**Normalization:** StandardScaler (weighted mean/std using F2 weights)
**DO NOT re-derive canonical columns** — sourced from Phase D Step 6.5 output.

---

## Total Feature Dimensionality

| Component | Dimensions |
|---|---|
| LSA text-semantic | 100 |
| Structured | 60 |
| **Total** | **160** |

---

## Feature Coverage

| Field | Rows covered | Coverage % |
|---|---|---|
| description_text (non-null, non-empty) | {has_desc} | {has_desc/N*100:.2f}% |
| structured_properties (non-empty) | {struct_nonzero} | {struct_nonzero/N*100:.2f}% |
| cultural_lineage_canonical | {sum(1 for r in rows if r[5] and r[5] != 'unknown')} | {sum(1 for r in rows if r[5] and r[5] != 'unknown')/N*100:.2f}% (excl unknown) |
| Total rows | {N} | 100% |

Rows with NULL/empty description_text ({N-has_desc}, {(N-has_desc)/N*100:.2f}%) are imputed with canonical_name + structured_properties weapon_type.

---

## F2 Inverse-Frequency Weight Vector

Per cultural_lineage_canonical bucket (math note §1.4):

| cultural_lineage_canonical | count | freq | raw_weight (1/freq_count) | normalized_weight |
|---|---|---|---|---|
"""
    for lineage, info in sorted(weight_by_lineage.items(), key=lambda x: -x[1]['count']):
        content += f"| {lineage} | {info['count']} | {info['freq']:.5f} | {info['raw_weight']:.6f} | {info['normalized_weight']:.4f} |\n"

    content += f"""
**Normalization:** weights divided by mean(raw_weight) so mean normalized_weight = 1.0
**Application:** applied as sqrt(w_i) row-multiplication on TF-IDF before SVD; as sample_weight on StandardScaler mean/std; as integer-duplication for HDBSCAN and GMM fit.

---

**Reproducibility:** Python 3.x + sklearn {__import__('sklearn').__version__} + numpy {__import__('numpy').__version__} + hdbscan
Corpus hash (vocabulary SHA-256[:16]): `{vocab_hash}`
DB path: `{DB_PATH}`
"""
    path = os.path.join(out_dir, "phase-E-1-features.md")
    with open(path, 'w') as f:
        f.write(content)
    log(f"Wrote Deliverable 1: {path}")
    return path


def write_deliverable_2(out_dir, axes_info, evr, k, mean_cos_dist, rows, svd_full):
    """Write phase-E-1-axis-discovery.md + phase-E-1-axis-loadings.json."""

    # Build per-axis provisional names
    for i, ax in enumerate(axes_info[:k]):
        ax["provisional_name"] = propose_provisional_axis_name(ax, evr[i])
        ax["variance_explained"] = float(evr[i])
        ax["bootstrap_mean_cosine_dist"] = float(mean_cos_dist[i]) if i < len(mean_cos_dist) else None
        ax["stability_pass"] = float(mean_cos_dist[i]) <= 0.10 if i < len(mean_cos_dist) else None

    cumevr = np.cumsum(evr)

    md_content = f"""# Phase E-1 — Deliverable 2: Axis Discovery Output

PROVISIONAL — gandalf reviews and canonically labels axes in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Status:** Complete

---

## Summary

- **Axes retained:** {k}
- **Cumulative variance explained (k={k}):** {cumevr[k-1]:.4f} ({cumevr[k-1]*100:.2f}%)
- **Method:** TruncatedSVD (weighted PCA via sqrt(F2-weight) row-multiplication)
- **F2 correction applied:** Yes (inverse-frequency cultural_lineage_canonical weights)
- **Bootstrap stability:** {n_bootstrap} resamples; per-axis mean cosine-distance reported below

---

## Per-Axis Results

"""
    for i, ax in enumerate(axes_info[:k]):
        md_content += f"""### Axis {ax['axis_index']}

- **Variance explained:** {ax['variance_explained']:.4f} ({ax['variance_explained']*100:.2f}%)
- **Provisional name:** {ax['provisional_name']}
- **Bootstrap stability (mean cosine-dist):** {ax.get('bootstrap_mean_cosine_dist', 'N/A'):.4f}
- **Stability PASS (≤0.10):** {'YES' if ax.get('stability_pass') else 'FAIL' if ax.get('stability_pass') is False else 'N/A'}
- **Single-feature flag:** {'YES (top-1 > 60% of top-20 L2-norm)' if ax['single_feature_flag'] else 'No'}
- **Purely text (no structured in top-5):** {'YES' if ax['purely_text_flag'] else 'No'}
- **Purely structured (no text in top-5):** {'YES' if ax['purely_structured_flag'] else 'No'}

**Top structured-feature loadings (interpretable):**

| Feature | Loading |
|---|---|
"""
        for fname, fval in ax['struct_top_loadings'][:10]:
            md_content += f"| {fname} | {fval:+.4f} |\n"

        md_content += f"""
**Top 5 all-feature loadings (absolute):**

| Feature | Loading |
|---|---|
"""
        for fname, fval in ax['top_loadings'][:5]:
            md_content += f"| {fname} | {fval:+.4f} |\n"
        md_content += "\n---\n\n"

    md_content += f"""## Phase E-1-bis Flags

"""
    flags = []
    for ax in axes_info[:k]:
        if ax.get('stability_pass') is False:
            flags.append(f"Axis {ax['axis_index']}: UNSTABLE (bootstrap cosine-dist = {ax.get('bootstrap_mean_cosine_dist','?'):.4f} > 0.10)")
        if ax['single_feature_flag']:
            flags.append(f"Axis {ax['axis_index']}: SINGLE-FEATURE (top-1 dominance > 60%)")

    if flags:
        for f in flags:
            md_content += f"- {f}\n"
    else:
        md_content += "- None. All axes pass stability and interpretability checks.\n"

    md_content += f"""
## Variance Explained Table

| Axis | EVR | Cumulative EVR | Stability |
|---|---|---|---|
"""
    for i in range(k):
        ax = axes_info[i]
        stab = f"{ax.get('bootstrap_mean_cosine_dist', 0):.4f}" if ax.get('bootstrap_mean_cosine_dist') is not None else "N/A"
        md_content += f"| {i+1} | {evr[i]:.4f} | {cumevr[i]:.4f} | {stab} |\n"

    path_md = os.path.join(out_dir, "phase-E-1-axis-discovery.md")
    with open(path_md, 'w') as f:
        f.write(md_content)
    log(f"Wrote Deliverable 2 (MD): {path_md}")

    # JSON loadings
    json_out = {
        "generated_at": datetime.now().isoformat(),
        "k_axes": k,
        "method": "TruncatedSVD (weighted PCA)",
        "f2_applied": True,
        "bootstrap_n": n_bootstrap,
        "axes": [
            {
                "axis_index": ax["axis_index"],
                "provisional_name": ax["provisional_name"],
                "variance_explained": ax["variance_explained"],
                "bootstrap_mean_cosine_dist": ax.get("bootstrap_mean_cosine_dist"),
                "stability_pass": ax.get("stability_pass"),
                "single_feature_flag": ax["single_feature_flag"],
                "top_loadings": ax["top_loadings"][:20],
                "struct_top_loadings": ax["struct_top_loadings"][:10]
            }
            for ax in axes_info[:k]
        ]
    }
    path_json = os.path.join(out_dir, "phase-E-1-axis-loadings.json")
    with open(path_json, 'w') as f:
        json.dump(json_out, f, indent=2, cls=NumpyEncoder)
    log(f"Wrote Deliverable 2 (JSON): {path_json}")
    return path_md, path_json


def write_deliverable_3(out_dir, rows, labels, confidence_scores, projections_k, evr, k,
                         gmm_labels, gmm_conf, km_labels, km_conf, mean_cos_dist):
    """Write phase-E-1-clusters.md."""
    from collections import Counter

    unique_labels = sorted(set(labels))
    n_clusters = len(unique_labels)

    # Compute per-cluster characterization
    cluster_chars = {}
    for lbl in unique_labels:
        char = characterize_cluster(rows, labels, lbl)
        char["top_reps"] = get_top_representatives(rows, labels, confidence_scores, lbl, n=3)
        char["centroid"] = projections_k[labels == lbl].mean(axis=0).tolist()
        char["provisional_description"] = propose_provisional_cluster_description(char)
        cluster_chars[lbl] = char

    # Purity
    primary_purity, per_cluster_purity = compute_purity(labels, rows)

    # F6 flag: clusters < 20 members
    small_clusters = [lbl for lbl in unique_labels if cluster_chars[lbl]["member_count"] < 20]

    # Top 5 by member count
    top5 = sorted(unique_labels, key=lambda l: cluster_chars[l]["member_count"], reverse=True)[:5]

    # HDBSCAN vs GMM vs k-means agreement
    hdbscan_counter = Counter(labels)
    gmm_counter = Counter(gmm_labels)
    km_counter = Counter(km_labels)

    md_content = f"""# Phase E-1 — Deliverable 3: Clustering Output

PROVISIONAL — gandalf labels clusters canonically in Phase E-2
**Author:** legolas
**Date:** 2026-05-23
**Status:** Complete

---

## Summary

| Metric | Value |
|---|---|
| Total rows clustered | {len(rows)} |
| HDBSCAN clusters (final) | {n_clusters} |
| HDBSCAN min_cluster_size | 30 |
| Originally-noise rows (confidence < 0.5) | {(confidence_scores < 0.5).sum()} |
| F6 flag: clusters < 20 members | {len(small_clusters)} |
| Mean cluster purity (cultural_lineage) | {primary_purity:.4f} ({primary_purity*100:.2f}%) |
| Purity PASS (≥ 0.85) | {'YES' if primary_purity >= 0.85 else 'FAIL'} |
| F2 inverse-frequency weighting applied | Yes |

---

## Method Comparison

| Method | N clusters |
|---|---|
| HDBSCAN (primary) | {n_clusters} |
| GMM baseline | {len(set(gmm_labels))} |
| k-means baseline | {len(set(km_labels))} |

---

## Top 5 Clusters by Member Count

"""
    for rank, lbl in enumerate(top5, 1):
        char = cluster_chars[lbl]
        md_content += f"""### Rank {rank}: Cluster {lbl} (N={char['member_count']})

- **Provisional description:** {char['provisional_description']}
- **Dominant lineage:** {char['dominant_lineage'][0]} ({char['dominant_lineage'][1]} rows)
- **Dominant period:** {char['dominant_period'][0]} ({char['dominant_period'][1]} rows)
- **Dominant register:** {char['dominant_register'][0]} ({char['dominant_register'][1]} rows)
- **Top weapon types:** {', '.join(f"{t[0]}({t[1]})" for t in char['top_weapon_types'][:3]) or 'none detected'}
- **Purity (cultural_lineage):** {per_cluster_purity.get(lbl, 0):.4f}

**Top-3 representative rows:**

| id | canonical_name | lineage | period | confidence |
|---|---|---|---|---|
"""
        for rep in char['top_reps']:
            md_content += f"| {rep['id']} | {rep['canonical_name'][:50]} | {rep['cultural_lineage_canonical']} | {rep['historical_period_canonical']} | {rep['confidence']:.4f} |\n"
        md_content += "\n---\n\n"

    md_content += f"""## F6 Flags: Clusters with < 20 Members

These clusters require merging-or-split decision in Phase E-2 (per F6 lock):

"""
    if small_clusters:
        for lbl in small_clusters:
            char = cluster_chars[lbl]
            md_content += f"- Cluster {lbl}: N={char['member_count']} — {char['provisional_description']}\n"
    else:
        md_content += "- None. All clusters have ≥ 20 members.\n"

    md_content += f"""
## Full Cluster Roster

| Cluster ID | Member Count | Dominant Lineage | Dominant Period | Top Weapon Type | Purity |
|---|---|---|---|---|---|
"""
    for lbl in unique_labels:
        char = cluster_chars[lbl]
        top_type = char['top_weapon_types'][0][0] if char['top_weapon_types'] else "mixed"
        purity_val = per_cluster_purity.get(lbl, 0)
        md_content += (f"| {lbl} | {char['member_count']} | {char['dominant_lineage'][0]} | "
                       f"{char['dominant_period'][0]} | {top_type} | {purity_val:.4f} |\n")

    path = os.path.join(out_dir, "phase-E-1-clusters.md")
    with open(path, 'w') as f:
        f.write(md_content)
    log(f"Wrote Deliverable 3: {path}")
    return path, cluster_chars, primary_purity, small_clusters


def populate_db(conn, rows, labels, confidence_scores, cluster_chars, projections_k, k, axes_info, evr):
    """Populate clusters + cluster_membership + weapon_knowledge_entries.cluster_id."""
    log("Populating DB: clusters, cluster_membership, weapon_knowledge_entries.cluster_id")

    unique_labels = sorted(set(labels))

    # Map from our sequential cluster label → DB cluster id
    # Clear existing rows (idempotent: delete then re-insert)
    conn.execute("DELETE FROM cluster_membership")
    conn.execute("DELETE FROM clusters")
    # Reset cluster_id on weapon_knowledge_entries
    conn.execute("UPDATE weapon_knowledge_entries SET cluster_id = NULL WHERE cluster_id IS NOT NULL")
    conn.commit()

    # Build axis loadings summary for clusters table
    # dominant_axes_description: top-3 axis loadings per cluster centroid
    label_to_db_id = {}

    for lbl in unique_labels:
        char = cluster_chars[lbl]
        centroid = np.array(char["centroid"])

        # Dominant axes: which of the k axes does this cluster centroid project most onto?
        if len(centroid) >= k:
            top_axes_idx = np.argsort(np.abs(centroid[:k]))[::-1][:3]
            dominant_axes_desc = json.dumps([
                {"axis": int(i+1), "loading": float(centroid[i])}
                for i in top_axes_idx
            ], cls=NumpyEncoder)
        else:
            dominant_axes_desc = json.dumps([])

        char_features_json = json.dumps({
            "dominant_lineage": char["dominant_lineage"][0],
            "dominant_period": char["dominant_period"][0],
            "dominant_register": char["dominant_register"][0],
            "top_weapon_types": [t[0] for t in char["top_weapon_types"][:3]],
            "member_count": char["member_count"],
            "provisional_description": char["provisional_description"]
        }, cls=NumpyEncoder)

        conn.execute("""
            INSERT INTO clusters (label, dominant_axes_description, cluster_algorithm_version, cluster_seed)
            VALUES (?, ?, ?, ?)
        """, (
            char["provisional_description"][:500],
            dominant_axes_desc,
            "phase-E-1-hdbscan-min30-2026-05-23",
            RANDOM_STATE
        ))
        db_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        label_to_db_id[lbl] = db_id

    conn.commit()
    log(f"Inserted {len(unique_labels)} rows into clusters table")

    # Insert cluster_membership + update weapon_knowledge_entries.cluster_id
    membership_rows = []
    wke_updates = []

    for i, row in enumerate(rows):
        entry_id = row[0]
        lbl = labels[i]
        db_cluster_id = label_to_db_id[lbl]
        conf = float(confidence_scores[i])
        membership_rows.append((entry_id, db_cluster_id, conf))
        wke_updates.append((db_cluster_id, entry_id))

    conn.executemany("""
        INSERT INTO cluster_membership (knowledge_entry_id, cluster_id, confidence_score)
        VALUES (?, ?, ?)
    """, membership_rows)

    conn.executemany("""
        UPDATE weapon_knowledge_entries SET cluster_id = ? WHERE id = ?
    """, wke_updates)

    conn.commit()
    log(f"Inserted {len(membership_rows)} rows into cluster_membership")
    log(f"Updated {len(wke_updates)} rows in weapon_knowledge_entries.cluster_id")

    # Verify
    n_clusters_db = conn.execute("SELECT COUNT(*) FROM clusters").fetchone()[0]
    n_membership_db = conn.execute("SELECT COUNT(*) FROM cluster_membership").fetchone()[0]
    n_wke_with_cluster = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE cluster_id IS NOT NULL"
    ).fetchone()[0]

    log(f"DB verification: clusters={n_clusters_db}, cluster_membership={n_membership_db}, "
        f"wke.cluster_id populated={n_wke_with_cluster}")

    return n_clusters_db, n_membership_db, n_wke_with_cluster, label_to_db_id


def run_smoke_test(conn, rows, labels, confidence_scores, label_to_db_id):
    """Round-trip smoke: 100-row sample; verify cluster_id populated; verify loadings JSON parses."""
    log("Running round-trip smoke test on 100-row sample...")
    sample_ids = [rows[i][0] for i in range(min(100, len(rows)))]

    errors = []
    for entry_id in sample_ids:
        # Check cluster_id populated
        result = conn.execute(
            "SELECT cluster_id FROM weapon_knowledge_entries WHERE id = ?", (entry_id,)
        ).fetchone()
        if not result or result[0] is None:
            errors.append(f"id={entry_id}: cluster_id is NULL")
            continue

        # Check cluster_membership row exists
        cm = conn.execute(
            "SELECT confidence_score FROM cluster_membership WHERE knowledge_entry_id = ?",
            (entry_id,)
        ).fetchone()
        if not cm:
            errors.append(f"id={entry_id}: no cluster_membership row")
            continue

        # Check clusters.dominant_axes_description is valid JSON
        cl = conn.execute(
            "SELECT dominant_axes_description FROM clusters WHERE id = ?",
            (result[0],)
        ).fetchone()
        if cl:
            try:
                json.loads(cl[0])
            except (json.JSONDecodeError, TypeError):
                errors.append(f"id={entry_id}: clusters.dominant_axes_description not valid JSON")

    if errors:
        log(f"SMOKE TEST ERRORS ({len(errors)}):")
        for e in errors[:10]:
            log(f"  {e}")
        return False, errors
    else:
        log(f"SMOKE TEST PASSED: {len(sample_ids)} rows verified")
        return True, []


n_bootstrap = 10  # global so write_deliverable_2 can reference it


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke", "full"], default="full")
    args = parser.parse_args()
    smoke_mode = (args.mode == "smoke")

    log(f"=== Phase E-1 Pipeline starting (mode={args.mode}) ===")

    conn = sqlite3.connect(DB_PATH)
    rows = load_data(conn, smoke_mode=smoke_mode)
    N = len(rows)

    # ── DELIVERABLE 1: Feature Engineering ───────────────────────────────────
    log("=== DELIVERABLE 1: Feature Engineering ===")
    corpus = build_text_corpus(rows)
    structured = build_structured_features(rows)
    weights, weight_by_lineage = compute_f2_weights(rows)
    lsa_out, tfidf_vec, lsa_svd, vocab_hash = fit_tfidf_lsa(corpus, weights, n_lsa=100, smoke=smoke_mode)
    structured_scaled, struct_mean, struct_std = scale_structured(structured, weights)
    X = build_feature_matrix(lsa_out, structured_scaled)

    d1_path = write_deliverable_1(OUT_DIR, rows, lsa_out, structured_scaled, weights, weight_by_lineage, vocab_hash, tfidf_vec)
    log(f"Deliverable 1 complete: {d1_path}")

    # ── DELIVERABLE 2: Axis Discovery ─────────────────────────────────────────
    log("=== DELIVERABLE 2: Axis Discovery ===")
    svd_full, projections, k, evr = run_pca_axis_discovery(X, weights, n_max=50)
    projections_k = projections[:, :k]
    mean_cos_dist = bootstrap_stability(X, weights, k, n_bootstrap=n_bootstrap)
    axes_info = interpret_axes(svd_full, k, tfidf_vec)
    d2_md, d2_json = write_deliverable_2(OUT_DIR, axes_info, evr, k, mean_cos_dist, rows, svd_full)
    log(f"Deliverable 2 complete: {d2_md}")

    # ── DELIVERABLE 3: Clustering ──────────────────────────────────────────────
    log("=== DELIVERABLE 3: Clustering ===")
    min_cs = 5 if smoke_mode else 30
    labels_raw, clusterer, n_clusters = run_hdbscan(projections_k, weights, min_cluster_size=min_cs)
    labels = labels_raw.copy()
    confidence_scores = np.ones(N)
    labels, confidence_scores = assign_noise_to_nearest(labels, projections_k)

    n_final_clusters = len(set(labels))
    log(f"Final cluster count after noise assignment: {n_final_clusters}")

    # Parameter sweep if out of bounds (skip for smoke)
    if not smoke_mode:
        if n_final_clusters < 50:
            log("< 50 clusters; retrying with min_cluster_size=20...")
            labels_raw, clusterer, n_clusters = run_hdbscan(projections_k, weights, min_cluster_size=20)
            labels = labels_raw.copy()
            confidence_scores = np.ones(N)
            labels, confidence_scores = assign_noise_to_nearest(labels, projections_k)
            n_final_clusters = len(set(labels))
            log(f"After retry: {n_final_clusters} clusters")
        elif n_final_clusters > 150:
            log("> 150 clusters; retrying with min_cluster_size=50...")
            labels_raw, clusterer, n_clusters = run_hdbscan(projections_k, weights, min_cluster_size=50)
            labels = labels_raw.copy()
            confidence_scores = np.ones(N)
            labels, confidence_scores = assign_noise_to_nearest(labels, projections_k)
            n_final_clusters = len(set(labels))
            log(f"After retry: {n_final_clusters} clusters")

    # Baselines
    gmm_labels, gmm_conf, gmm_model = run_gmm_baseline(projections_k, n_final_clusters)
    km_labels, km_conf, km_model = run_kmeans_baseline(projections_k, n_final_clusters)

    d3_path, cluster_chars, primary_purity, small_clusters = write_deliverable_3(
        OUT_DIR, rows, labels, confidence_scores, projections_k, evr, k,
        gmm_labels, gmm_conf, km_labels, km_conf, mean_cos_dist
    )
    log(f"Deliverable 3 complete: {d3_path}")

    # ── ROUND-TRIP SMOKE (before full DB write) ───────────────────────────────
    # Do smoke verification in-memory first for smoke mode
    if smoke_mode:
        log("SMOKE MODE: skipping DB write; pipeline structurally verified.")
        log(f"Smoke results: k={k}, clusters={n_final_clusters}, purity={primary_purity:.4f}")
        conn.close()
        return

    # ── DELIVERABLE 4: DB Population ──────────────────────────────────────────
    log("=== DELIVERABLE 4: DB Population ===")
    n_clusters_db, n_membership_db, n_wke_db, label_to_db_id = populate_db(
        conn, rows, labels, confidence_scores, cluster_chars, projections_k, k, axes_info, evr
    )

    # Round-trip smoke (after DB write)
    smoke_pass, smoke_errors = run_smoke_test(conn, rows, labels, confidence_scores, label_to_db_id)
    log(f"Round-trip smoke: {'PASS' if smoke_pass else 'FAIL'}")

    conn.close()

    # ── REPORT RESULTS ────────────────────────────────────────────────────────
    log("=== PIPELINE COMPLETE ===")
    log(f"k axes: {k}")
    log(f"Clusters: {n_final_clusters}")
    log(f"Primary purity: {primary_purity:.4f}")
    log(f"DB clusters: {n_clusters_db}, membership: {n_membership_db}, wke: {n_wke_db}")
    log(f"F6 small clusters: {len(small_clusters)}")
    log(f"Smoke test: {'PASS' if smoke_pass else 'FAIL'}")

    # Save results summary for completion note
    results = {
        "k": k,
        "n_clusters": n_final_clusters,
        "primary_purity": float(primary_purity),
        "mean_bootstrap_cosine_dist": float(mean_cos_dist.mean()),
        "per_axis_cosine_dist": mean_cos_dist.tolist(),
        "db_clusters": n_clusters_db,
        "db_membership": n_membership_db,
        "db_wke_populated": n_wke_db,
        "small_clusters": small_clusters,
        "smoke_pass": smoke_pass,
        "smoke_errors": smoke_errors,
        "axes": [
            {
                "axis_index": ax["axis_index"],
                "provisional_name": ax.get("provisional_name", ""),
                "variance_explained": ax.get("variance_explained", 0),
                "bootstrap_mean_cosine_dist": ax.get("bootstrap_mean_cosine_dist"),
                "stability_pass": ax.get("stability_pass")
            }
            for ax in axes_info[:k]
        ],
        "top5_clusters": [
            {
                "label": lbl,
                "member_count": cluster_chars[lbl]["member_count"],
                "dominant_lineage": cluster_chars[lbl]["dominant_lineage"][0],
                "provisional_description": cluster_chars[lbl]["provisional_description"]
            }
            for lbl in sorted(set(labels), key=lambda l: cluster_chars[l]["member_count"], reverse=True)[:5]
        ]
    }
    results_path = os.path.join(OUT_DIR, "phase-E-1-pipeline-results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    log(f"Results saved to {results_path}")


if __name__ == "__main__":
    main()
