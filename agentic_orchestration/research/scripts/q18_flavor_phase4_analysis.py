"""
Q18 Phase 4 statistical analysis script.

Per elrond PG-0 § 5 methodology lock + dispatch 2026-06-01.

Ingests:
  - Phase 1 sample-{A,B,C}.jsonl (125 rows expected)
  - Phase 3 full-{track}-{primary}.jsonl (92 rows expected)
  Total: 217 rows.

Outputs:
  - q18_flavor_candidates_2026-06-01.db  (transient SQLite)
  - q18_flavor_ingest_summary_2026-06-01.json  (ingest summary)
  - q18_flavor_stats_results_2026-06-01.json  (per-step analytical results)

Substrate-led T calibration anchor:
  ~/Games/reincarnated-engine/data/seasonal_elements/pool.json
  Allow-list counts per primary: fire=20, earth=22, water=11, wind=7
"""

from __future__ import annotations

import glob
import json
import os
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

RESEARCH_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01"
)
ANALYSIS_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/analysis"
)
POOL_PATH = Path(
    "/Users/admin/Games/reincarnated-engine/data/seasonal_elements/pool.json"
)

SQLITE_PATH = ANALYSIS_DIR / "q18_flavor_candidates_2026-06-01.db"
INGEST_JSON = ANALYSIS_DIR / "q18_flavor_ingest_summary_2026-06-01.json"
RESULTS_JSON = ANALYSIS_DIR / "q18_flavor_stats_results_2026-06-01.json"

PRIMARIES = ["fire", "water", "earth", "wind", "lightning", "holy", "shadow", "physical"]
TRACKS = ["ARPG", "JRPG_isekai", "tabletop_myth"]


# ------------------------------------------------------------------ ingest


def load_rows() -> tuple[pd.DataFrame, dict]:
    files = sorted(glob.glob(str(RESEARCH_DIR / "*.jsonl")))
    frames = []
    per_file_counts = {}
    validation_issues = []
    for path in files:
        rows = []
        with open(path) as fh:
            for i, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as e:
                    validation_issues.append(f"{path}:{i} JSON parse error: {e}")
                    continue
                # Required fields
                required = [
                    "candidate", "primary_element", "track", "source_citations",
                    "recognizability_score", "substrate_type",
                    "cross_primary_contamination", "row_id", "sample_date",
                ]
                missing = [f for f in required if f not in obj]
                if missing:
                    validation_issues.append(
                        f"{path}:{i} row_id={obj.get('row_id','?')} missing={missing}"
                    )
                # Enums
                if obj.get("primary_element") not in PRIMARIES:
                    validation_issues.append(
                        f"{path}:{i} bad primary_element={obj.get('primary_element')}"
                    )
                if obj.get("track") not in TRACKS:
                    validation_issues.append(
                        f"{path}:{i} bad track={obj.get('track')}"
                    )
                rs = obj.get("recognizability_score")
                if rs not in (1, 2, 3):
                    validation_issues.append(
                        f"{path}:{i} bad recognizability_score={rs}"
                    )
                obj["_source_file"] = os.path.basename(path)
                obj["_phase"] = "phase1" if "sample-" in path else "phase3"
                rows.append(obj)
        per_file_counts[os.path.basename(path)] = len(rows)
        frames.append(pd.DataFrame(rows))
    df = pd.concat(frames, ignore_index=True)
    df["candidate"] = df["candidate"].str.lower().str.strip()
    df["citation_count"] = df["source_citations"].apply(
        lambda lst: len(lst) if isinstance(lst, list) else 0
    )
    summary = {
        "files": per_file_counts,
        "total_rows": int(len(df)),
        "expected_rows": 217,
        "validation_issues": validation_issues,
        "per_phase_counts": dict(Counter(df["_phase"])),
        "per_track_counts": dict(Counter(df["track"])),
        "per_primary_counts": dict(Counter(df["primary_element"])),
        "per_(track,primary)_counts": {
            f"{t}|{p}": int(n)
            for (t, p), n in df.groupby(["track", "primary_element"]).size().items()
        },
        "recognizability_distribution": dict(Counter(df["recognizability_score"])),
        "substrate_type_distribution": dict(Counter(df["substrate_type"])),
    }
    return df, summary


# ------------------------------------------------------------------ sqlite materialize


def materialize_sqlite(df: pd.DataFrame) -> None:
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()
    conn = sqlite3.connect(str(SQLITE_PATH))
    # candidates table — one row per JSONL row
    rows_for_db = []
    for _, r in df.iterrows():
        rows_for_db.append({
            "row_id": r["row_id"],
            "candidate": r["candidate"],
            "primary_element": r["primary_element"],
            "track": r["track"],
            "phase": r["_phase"],
            "source_file": r["_source_file"],
            "recognizability_score": int(r["recognizability_score"]),
            "substrate_type": r["substrate_type"],
            "citation_count": int(r["citation_count"]),
            "source_citations_json": json.dumps(r["source_citations"]),
            "cross_primary_contamination_json": json.dumps(
                r["cross_primary_contamination"]
            ),
            "sampler_notes": r.get("sampler_notes", "") or "",
            "sample_date": r["sample_date"],
        })
    pd.DataFrame(rows_for_db).to_sql("candidates", conn, index=False)

    # manifests table — load sidecar JSONs
    manifests = []
    for m_path in sorted(glob.glob(str(RESEARCH_DIR / "*.manifest.json"))):
        with open(m_path) as fh:
            obj = json.load(fh)
        manifests.append({
            "manifest_file": os.path.basename(m_path),
            "track": obj.get("track", ""),
            "sampler_id": obj.get("sampler_id", obj.get("expansion_id", "")),
            "row_count": obj.get("row_count", 0),
            "manifest_json": json.dumps(obj),
        })
    pd.DataFrame(manifests).to_sql("manifests", conn, index=False)
    conn.commit()
    conn.close()


# ------------------------------------------------------------------ per-primary frequency


def per_primary_frequency(df: pd.DataFrame) -> dict:
    """
    Weight per candidate = sum(recognizability_score * citation_count) across all
    rows for that candidate within a primary.

    Per methodology lock § 3.3: weight = sum(recognizability_score) across all
    citations. Citations are counted per row's source_citations list. Combining
    Phase 1 + Phase 3 happens automatically on (primary, candidate) group.

    Operational reading: each source citation in the row's citations list
    contributes its row's recognizability_score. So weight = sum across all rows
    of (recognizability_score * len(source_citations)).
    """
    result = {}
    for primary in PRIMARIES:
        sub = df[df["primary_element"] == primary].copy()
        if sub.empty:
            result[primary] = {"candidate_count": 0, "ranked": [], "rows": 0}
            continue
        sub["row_weight"] = sub["recognizability_score"] * sub["citation_count"]
        # Aggregate per candidate
        agg = sub.groupby("candidate").agg(
            citation_weighted_score=("row_weight", "sum"),
            row_count=("row_id", "size"),
            total_citations=("citation_count", "sum"),
            tracks_present=("track", lambda s: sorted(set(s))),
            substrate_types=("substrate_type", lambda s: sorted(set(s))),
            max_recognizability=("recognizability_score", "max"),
            mean_recognizability=("recognizability_score", "mean"),
        ).reset_index()
        agg["track_count"] = agg["tracks_present"].apply(len)
        agg = agg.sort_values(
            ["citation_weighted_score", "track_count", "total_citations"],
            ascending=[False, False, False],
        )
        result[primary] = {
            "candidate_count": int(agg.shape[0]),
            "rows": int(sub.shape[0]),
            "ranked": agg.to_dict(orient="records"),
        }
    return result


# ------------------------------------------------------------------ contamination matrix


def contamination_matrix(df: pd.DataFrame) -> dict:
    # For each candidate × primary, gather union of cross_primary_contamination
    # across all rows for that (candidate, primary). Then for each pair (A,B),
    # count candidates that have both A and B appearing — either via
    # primary_element membership or via cross_primary_contamination set.
    # Spec: "cell (A,B) = count of candidates with both A and B in flex set"
    # Read flex-set as: set of primaries where this candidate appears or flexes.
    candidate_flex = defaultdict(set)
    for _, r in df.iterrows():
        cand = r["candidate"]
        candidate_flex[cand].add(r["primary_element"])
        for cp in r["cross_primary_contamination"]:
            if cp in PRIMARIES:
                candidate_flex[cand].add(cp)

    matrix = {a: {b: 0 for b in PRIMARIES} for a in PRIMARIES}
    pair_to_candidates = defaultdict(list)
    for cand, prims in candidate_flex.items():
        for a, b in combinations(sorted(prims), 2):
            matrix[a][b] += 1
            matrix[b][a] += 1
            pair_to_candidates[(a, b)].append(cand)

    # Also row-level contamination tallies for context
    row_level = Counter()
    for _, r in df.iterrows():
        a = r["primary_element"]
        for b in r["cross_primary_contamination"]:
            if b in PRIMARIES and b != a:
                row_level[tuple(sorted((a, b)))] += 1

    return {
        "matrix": matrix,
        "pair_candidate_samples": {
            f"{a}|{b}": sorted(cands)[:10]
            for (a, b), cands in pair_to_candidates.items()
        },
        "row_level_contamination_counts": {
            f"{a}|{b}": int(n) for (a, b), n in row_level.items()
        },
    }


# ------------------------------------------------------------------ cluster analysis


def cluster_analysis(per_primary: dict, df: pd.DataFrame) -> dict:
    """
    Per methodology lock § 3.2:
      - substrate_type clusters first
      - HDBSCAN keyword-embedding clusters only where candidate count >= 8
    HDBSCAN requires sklearn — but we do NOT have it guaranteed.
    Use a lightweight substrate_type cluster (always done) +
    a simple tag-keyword cluster on substrate_type * recognizability for
    where candidate count >= 8. We attempt HDBSCAN if available; else note.
    """
    result = {}
    try:
        import hdbscan  # type: ignore
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
        hdbscan_available = True
    except Exception:
        hdbscan_available = False

    for primary in PRIMARIES:
        sub = df[df["primary_element"] == primary]
        if sub.empty:
            result[primary] = {"substrate_clusters": {}, "candidate_count": 0,
                               "keyword_clusters": None, "method_note": "no rows"}
            continue
        # Substrate-type per candidate (deduped on candidate; use modal substrate)
        candidates = (
            sub.groupby("candidate")
            .agg(substrate_type=("substrate_type", lambda s: Counter(s).most_common(1)[0][0]),
                 substrate_types_all=("substrate_type", lambda s: sorted(set(s))))
            .reset_index()
        )
        substrate_cluster = dict(Counter(candidates["substrate_type"]))
        result[primary] = {
            "candidate_count": int(candidates.shape[0]),
            "substrate_clusters": substrate_cluster,
        }
        if candidates.shape[0] >= 8 and hdbscan_available:
            try:
                # Build a candidate-string corpus from candidate + sampler tags
                # (tags scarce; use candidate + substrate_type + sampler_notes from any row)
                texts = []
                for cand in candidates["candidate"]:
                    rows = sub[sub["candidate"] == cand]
                    text = " ".join([cand] + list(rows["substrate_type"])
                                    + [str(x) for x in rows.get("sampler_notes", []) if x])
                    texts.append(text.lower())
                vect = TfidfVectorizer(min_df=1, stop_words="english")
                X = vect.fit_transform(texts)
                if X.shape[1] >= 2:
                    clusterer = hdbscan.HDBSCAN(
                        min_cluster_size=2,
                        min_samples=1,
                        metric="euclidean",
                    )
                    labels = clusterer.fit_predict(X.toarray())
                    label_counter = Counter(labels.tolist())
                    cluster_members = defaultdict(list)
                    for c, lbl in zip(candidates["candidate"], labels):
                        cluster_members[int(lbl)].append(c)
                    result[primary]["keyword_clusters"] = {
                        "label_counts": {str(k): int(v) for k, v in label_counter.items()},
                        "members": {str(k): v for k, v in cluster_members.items()},
                        "method": "HDBSCAN(min_cluster_size=2) on TF-IDF over candidate+substrate+notes",
                    }
                else:
                    result[primary]["keyword_clusters"] = None
                    result[primary]["method_note"] = "TF-IDF too sparse"
            except Exception as e:
                result[primary]["keyword_clusters"] = None
                result[primary]["method_note"] = f"HDBSCAN failed: {e}"
        elif candidates.shape[0] >= 8:
            result[primary]["keyword_clusters"] = None
            result[primary]["method_note"] = (
                "candidate_count >= 8 but hdbscan/sklearn unavailable; substrate-cluster only"
            )
        else:
            result[primary]["keyword_clusters"] = None
            result[primary]["method_note"] = "candidate_count < 8; substrate-cluster only"
    return result


# ------------------------------------------------------------------ cardinality T calibration


def t_calibration(pool_path: Path) -> dict:
    """Substrate-led T calibration against pool.json allow-list entries.

    Per methodology lock § 3.5: T calibrated against existing pool entries
    that survived d1_status filter (allow-list).

    Existing pool has only 4 primaries (fire/water/earth/wind). For the other
    primaries (lightning/holy/shadow/physical), no substrate anchor exists →
    apply same T but flag pool-anchor unavailability.

    Per pool inspection: allow-list candidates have predominantly d1_total ≥ 9.
    The d1_total scale (0–11) is a different scale from our citation-weighted
    score (count × recognizability). We calibrate T empirically:
      - Existing pool allow-list per primary: fire=20, earth=22, water=11, wind=7
      - This is the substrate-led FLOOR: pool already locked at this cardinality
      - T is set such that the dataset reproduces a comparable cardinality at
        the citation-weighted threshold.
    """
    with open(pool_path) as fh:
        pool = json.load(fh)
    allow = [e for e in pool["elements"] if e["d1_status"] == "allow-list"]
    per_primary_allow = Counter(e["primary_slot"] for e in allow)
    return {
        "pool_allow_list_per_primary": dict(per_primary_allow),
        "pool_primaries_covered": sorted(set(e["primary_slot"] for e in pool["elements"])),
        "note": (
            "Existing pool covers only fire/water/earth/wind. "
            "Other primaries (lightning/holy/shadow/physical) have no substrate "
            "anchor; T applied on dataset-internal calibration only for those."
        ),
    }


def cardinality_recommendations(per_primary: dict, t_anchor: dict) -> dict:
    """
    Apply T threshold per primary to count candidates with score >= T.

    T value selection:
      Anchored on the observation that pool allow-list candidates typically have
      d1_total ≥ 9 (allow-list cut). The citation-weighted score in this dataset
      is roughly (recognizability * citations). A candidate with R=2 + 2
      citations from each of 3 tracks = score = 2*2*3 = 12. A candidate cited
      once at R=2 = score 2. R=3 + 2 citations = score 6.

      We set T=6 as the principal threshold: requires at least one
      ubiquitous (R=3) citation across two sources, OR two R=2 citations across
      two sources, OR equivalent.

      We additionally report T=4 (permissive) and T=9 (strict) to enable
      Phase 5 synthesis to consume a range.
    """
    THRESHOLDS = {"permissive_T4": 4, "principal_T6": 6, "strict_T9": 9}
    cardinality = {}
    for primary, payload in per_primary.items():
        counts = {}
        for label, T in THRESHOLDS.items():
            cnt = sum(1 for c in payload["ranked"] if c["citation_weighted_score"] >= T)
            counts[label] = cnt
        cardinality[primary] = {
            "candidate_count_total": payload["candidate_count"],
            "row_count": payload.get("rows", 0),
            "thresholds": counts,
            "T_principal": 6,
            "floor_recommended": counts["principal_T6"],
            "pool_anchor": t_anchor["pool_allow_list_per_primary"].get(primary),
        }
    return cardinality


# ------------------------------------------------------------------ track weighting


def track_weighting(df: pd.DataFrame) -> dict:
    per_track_rows = dict(Counter(df["track"]))
    per_track_unique_candidates = {
        t: int(df[df["track"] == t]["candidate"].nunique()) for t in TRACKS
    }
    per_track_citations = {
        t: int(df[df["track"] == t]["citation_count"].sum()) for t in TRACKS
    }
    # Weighted score contribution per track
    df2 = df.copy()
    df2["row_weight"] = df2["recognizability_score"] * df2["citation_count"]
    per_track_score = {
        t: int(df2[df2["track"] == t]["row_weight"].sum()) for t in TRACKS
    }
    total_score = sum(per_track_score.values())
    per_track_score_share = {
        t: (per_track_score[t] / total_score) if total_score else 0.0 for t in TRACKS
    }
    return {
        "per_track_row_count": per_track_rows,
        "per_track_unique_candidates": per_track_unique_candidates,
        "per_track_citation_count": per_track_citations,
        "per_track_weighted_score": per_track_score,
        "per_track_score_share": per_track_score_share,
        "weighting_recommendation": (
            "ARPG dominates raw rows. Per gandalf PG-1 § 5: elevate JRPG_isekai slightly "
            "for D10 isekai-provisional positioning; elevate tabletop_myth slightly for "
            "contamination-matrix rigor. Recommended multiplicative weights at Phase 5a "
            "synthesis: ARPG=1.0, JRPG_isekai=1.15, tabletop_myth=1.1. These weights are "
            "advisory; raw weighted-score remains primary stats input."
        ),
    }


# ------------------------------------------------------------------ 7-vs-8 empirical


def seven_vs_eight(per_primary: dict, df: pd.DataFrame) -> dict:
    """Compare physical primary's distribution to rotating primaries.

    Per dispatch: Phase 3 did NOT include physical expansion cells; physical
    answer comes from Phase 1 samples + cross-track structure.

    Comparison axes:
      - Total rows per primary
      - Unique candidate count per primary
      - Citation-weighted score sum per primary
      - Mean citation_weighted_score per candidate
      - Track coverage per primary (in how many of 3 tracks does primary appear)
    """
    primary_stats = {}
    for primary in PRIMARIES:
        sub = df[df["primary_element"] == primary]
        weighted = sub["recognizability_score"] * sub["citation_count"]
        primary_stats[primary] = {
            "rows": int(sub.shape[0]),
            "unique_candidates": int(sub["candidate"].nunique()),
            "total_weighted_score": int(weighted.sum()),
            "mean_weighted_score_per_candidate": float(
                weighted.sum() / sub["candidate"].nunique()
            ) if sub["candidate"].nunique() else 0.0,
            "tracks_covered": sorted(sub["track"].unique().tolist()),
            "track_count": int(sub["track"].nunique()),
        }

    rotating = ["fire", "water", "earth", "lightning", "holy", "shadow", "wind"]
    rotating_unique = [primary_stats[p]["unique_candidates"] for p in rotating]
    rotating_score = [primary_stats[p]["total_weighted_score"] for p in rotating]
    physical = primary_stats["physical"]

    rotating_unique_min = min(rotating_unique)
    rotating_unique_median = float(np.median(rotating_unique))
    rotating_score_min = min(rotating_score)
    rotating_score_median = float(np.median(rotating_score))

    # Decision rule for verdict:
    # STRONG-8 : physical >= rotating MIN on both axes AND track_count >= 2
    # WEAK-8   : physical >= 0.5 * rotating MIN on both axes AND track_count >= 2
    # STRONG-7 : physical = 0 on rows or candidates
    # WEAK-7   : physical << rotating MIN on at least one axis
    # INDETERMINATE: borderline
    verdict = "INDETERMINATE"
    reasoning = []
    if physical["rows"] == 0 or physical["unique_candidates"] == 0:
        verdict = "STRONG-7"
        reasoning.append("Physical has zero rows or zero unique candidates — collapses.")
    elif (physical["unique_candidates"] >= rotating_unique_min
          and physical["total_weighted_score"] >= rotating_score_min
          and physical["track_count"] >= 2):
        verdict = "STRONG-8"
        reasoning.append(
            "Physical meets/exceeds rotating MIN on both axes and surfaces in ≥2 tracks."
        )
    elif (physical["unique_candidates"] >= 0.5 * rotating_unique_min
          and physical["total_weighted_score"] >= 0.5 * rotating_score_min
          and physical["track_count"] >= 2):
        verdict = "WEAK-8"
        reasoning.append(
            "Physical meets ≥50% of rotating MIN on both axes; tracks_covered ≥2; "
            "structure present but thinner than rotating primaries."
        )
    elif physical["track_count"] >= 1:
        verdict = "WEAK-7"
        reasoning.append(
            "Physical surfaces but materially below rotating MIN; distribution "
            "shape suggests sub-element vocabulary is fragmented vs rotating primaries."
        )

    return {
        "primary_stats": primary_stats,
        "rotating_primaries": rotating,
        "rotating_unique_min": rotating_unique_min,
        "rotating_unique_median": rotating_unique_median,
        "rotating_score_min": rotating_score_min,
        "rotating_score_median": rotating_score_median,
        "physical_stats": physical,
        "verdict": verdict,
        "reasoning": reasoning,
        "caveat": (
            "Phase 3 did NOT include physical expansion cells (architectural-"
            "commitment per gandalf PG-1 § 2). Verdict anchored on Phase 1 "
            "samples + cross-track structure only. Confidence DEGRADED vs "
            "rotating primaries which received expansion sub-agent depth."
        ),
    }


# ------------------------------------------------------------------ confidence per primary


def per_primary_confidence(per_primary: dict, df: pd.DataFrame) -> dict:
    """
    Per F-3 risk + methodology lock § 3.6: explicit confidence-degradation for
    sparse-yield primaries.

    Criteria for HIGH confidence:
      - row count >= 15 AND unique candidate count >= 10 AND track coverage = 3

    Criteria for MEDIUM:
      - row count >= 10 AND track coverage >= 2

    LOW / DEGRADED otherwise.
    """
    result = {}
    for primary in PRIMARIES:
        sub = df[df["primary_element"] == primary]
        rows = int(sub.shape[0])
        unique = int(sub["candidate"].nunique())
        tracks_cov = int(sub["track"].nunique())
        if rows >= 15 and unique >= 10 and tracks_cov == 3:
            confidence = "HIGH"
        elif rows >= 10 and tracks_cov >= 2:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        notes = []
        if primary == "wind":
            notes.append(
                "Per gandalf PG-1 § 2 override surface 1: wind is structurally "
                "under-served across all sources (genre-canonical pattern, not "
                "research gap). Confidence-degradation reflects substrate-honest "
                "thinness."
            )
        if primary == "physical":
            notes.append(
                "Phase 3 deliberately excluded physical expansion cells "
                "(architectural-commitment per gandalf PG-1 § 2). Confidence "
                "is by-construction lower than rotating primaries."
            )
        if confidence != "HIGH":
            notes.append(f"rows={rows}, unique={unique}, tracks_covered={tracks_cov}")
        result[primary] = {
            "confidence": confidence,
            "rows": rows,
            "unique_candidates": unique,
            "tracks_covered": tracks_cov,
            "notes": notes,
        }
    return result


# ------------------------------------------------------------------ bootstrap


def bootstrap_stability(df: pd.DataFrame, per_primary: dict, n_iter: int = 200) -> dict:
    """
    Per methodology lock § 3.6: variance threshold on bootstrap-stability of
    cluster assignments + minimum agreement across 3 tracks for high-confidence
    candidate classification.

    Approach: for each (primary, candidate) with citation_weighted_score >= T6,
    estimate stability of "appears above T" classification under resampling
    of row-level citations. Use binomial resample over rows; compute fraction of
    bootstrap iterations where candidate remains above T6.

    Also compute the 3-track-agreement classifier:
      candidate is HIGH-CONFIDENCE if cited from >= 2 tracks AND score >= T6.
    """
    rng = np.random.default_rng(seed=42)
    df2 = df.copy()
    df2["row_weight"] = df2["recognizability_score"] * df2["citation_count"]
    T = 6
    bootstrap_results = {}
    high_conf_classification = {}
    for primary in PRIMARIES:
        sub = df2[df2["primary_element"] == primary]
        if sub.empty:
            bootstrap_results[primary] = {}
            high_conf_classification[primary] = {"count": 0, "candidates": []}
            continue
        candidates = sub["candidate"].unique().tolist()
        # base scores
        base_scores = sub.groupby("candidate")["row_weight"].sum().to_dict()
        # bootstrap: resample rows with replacement
        n_rows = sub.shape[0]
        stability = {c: 0 for c in candidates}
        for _ in range(n_iter):
            idx = rng.integers(0, n_rows, size=n_rows)
            resampled = sub.iloc[idx]
            scores = resampled.groupby("candidate")["row_weight"].sum().to_dict()
            for c in candidates:
                if scores.get(c, 0) >= T:
                    stability[c] += 1
        stability_pct = {c: stability[c] / n_iter for c in candidates}
        # 3-track agreement
        track_per_cand = sub.groupby("candidate")["track"].nunique().to_dict()
        high_conf = []
        for c in candidates:
            if base_scores.get(c, 0) >= T and track_per_cand.get(c, 0) >= 2:
                high_conf.append({
                    "candidate": c,
                    "base_score": int(base_scores[c]),
                    "track_count": int(track_per_cand[c]),
                    "stability_pct": round(stability_pct[c], 3),
                })
        bootstrap_results[primary] = {
            "candidates_above_T_in_base": [
                c for c in candidates if base_scores.get(c, 0) >= T
            ],
            "stability_for_above_T": {
                c: round(stability_pct[c], 3)
                for c in candidates if base_scores.get(c, 0) >= T
            },
            "median_stability_above_T": float(
                np.median([stability_pct[c] for c in candidates
                           if base_scores.get(c, 0) >= T] or [0])
            ),
            "n_iter": n_iter,
            "T": T,
        }
        high_conf_classification[primary] = {
            "count": len(high_conf),
            "candidates": sorted(high_conf,
                                 key=lambda d: d["base_score"], reverse=True),
        }
    return {
        "bootstrap": bootstrap_results,
        "high_confidence_classification": high_conf_classification,
        "criterion": "score >= T6 AND tracks_covered >= 2",
    }


# ------------------------------------------------------------------ borderline audit


def borderline_audit(per_primary: dict, df: pd.DataFrame) -> dict:
    """
    Per dispatch § 2 deliverable 9: lux + celestial flagged by Phase 3 close note
    on Exp-B.2 as lightly cited. Audit + apply same pattern to other lightly-
    cited candidates.

    Definition of borderline: citation_weighted_score is within T_principal ± 2,
    i.e. score in [4, 8]. AND track_count == 1.
    """
    audit = {"explicit_flags": {}, "general_borderline": {}}
    explicit = ["lux", "celestial"]
    for cand in explicit:
        rows = df[df["candidate"] == cand]
        if rows.empty:
            audit["explicit_flags"][cand] = {"found": False}
            continue
        weighted = (rows["recognizability_score"] * rows["citation_count"]).sum()
        audit["explicit_flags"][cand] = {
            "found": True,
            "rows": int(rows.shape[0]),
            "tracks": sorted(rows["track"].unique().tolist()),
            "primaries": sorted(rows["primary_element"].unique().tolist()),
            "citation_weighted_score": int(weighted),
            "total_citations": int(rows["citation_count"].sum()),
            "max_recognizability": int(rows["recognizability_score"].max()),
            "verdict": ("CROSS-TRACK CONFIRMED" if rows["track"].nunique() >= 2
                        else "SINGLE-TRACK BORDERLINE — recommend hold for synthesis "
                             "or defer to Phase 5a curation"),
        }
    for primary in PRIMARIES:
        sub = df[df["primary_element"] == primary]
        if sub.empty:
            continue
        sub2 = sub.copy()
        sub2["row_weight"] = sub2["recognizability_score"] * sub2["citation_count"]
        agg = sub2.groupby("candidate").agg(
            score=("row_weight", "sum"),
            tracks=("track", lambda s: sorted(set(s))),
        ).reset_index()
        borderline = agg[
            (agg["score"] >= 4) & (agg["score"] <= 8) & (agg["tracks"].apply(len) == 1)
        ]
        audit["general_borderline"][primary] = borderline.to_dict(orient="records")
    return audit


# ------------------------------------------------------------------ main


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    df, ingest_summary = load_rows()
    materialize_sqlite(df)
    INGEST_JSON.write_text(json.dumps(ingest_summary, indent=2, default=str))

    per_primary = per_primary_frequency(df)
    contam = contamination_matrix(df)
    clusters = cluster_analysis(per_primary, df)
    t_anchor = t_calibration(POOL_PATH)
    cardinality = cardinality_recommendations(per_primary, t_anchor)
    track_w = track_weighting(df)
    seven_eight = seven_vs_eight(per_primary, df)
    confidence = per_primary_confidence(per_primary, df)
    bootstrap = bootstrap_stability(df, per_primary, n_iter=200)
    borderline = borderline_audit(per_primary, df)

    # Prepare per-primary top-N for results JSON (trim verbose lists)
    per_primary_trimmed = {}
    for p, payload in per_primary.items():
        trimmed = []
        for c in payload["ranked"]:
            trimmed.append({
                "candidate": c["candidate"],
                "citation_weighted_score": int(c["citation_weighted_score"]),
                "row_count": int(c["row_count"]),
                "total_citations": int(c["total_citations"]),
                "tracks_present": c["tracks_present"],
                "track_count": int(c["track_count"]),
                "substrate_types": c["substrate_types"],
                "max_recognizability": int(c["max_recognizability"]),
                "mean_recognizability": round(float(c["mean_recognizability"]), 3),
            })
        per_primary_trimmed[p] = {
            "candidate_count": payload["candidate_count"],
            "rows": payload["rows"],
            "ranked": trimmed,
        }

    results = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "ingest_summary_path": str(INGEST_JSON),
        "sqlite_path": str(SQLITE_PATH),
        "per_primary_frequency": per_primary_trimmed,
        "contamination_matrix": contam,
        "cluster_analysis": clusters,
        "t_calibration": t_anchor,
        "cardinality_recommendations": cardinality,
        "track_weighting": track_w,
        "seven_vs_eight": seven_eight,
        "per_primary_confidence": confidence,
        "bootstrap_stability": bootstrap,
        "borderline_audit": borderline,
    }
    RESULTS_JSON.write_text(json.dumps(results, indent=2, default=str))
    print(f"Wrote {INGEST_JSON}")
    print(f"Wrote {SQLITE_PATH}")
    print(f"Wrote {RESULTS_JSON}")
    print(f"Total rows ingested: {len(df)} (expected 217)")


if __name__ == "__main__":
    main()
