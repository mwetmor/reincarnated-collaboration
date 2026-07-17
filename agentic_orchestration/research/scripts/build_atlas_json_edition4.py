"""
build_atlas_json_edition4.py — Deterministic emitter for atlas-edition4.json EDITION IV.

PARENT: build_atlas_json_edition3.py (frozen-basis supplementary-admission lineage). This script
EXTENDS the Edition-III emitter for Path A (spec §5): the frozen Edition-I MCA basis is UNTOUCHED,
all 506 E3 point coords are byte-identical, and the curated LA/MCD rows (+ the 3 speced pull re-keys)
are admitted as SUPPLEMENTARY points via the SAME CA supplementary-projection the 37 tombstones used.

Spec:  agentic_orchestration/research/curated/atlas/edition4-refit-spec.md  (RATIFIED; Matt "Agreed, path A")
Charge: agentic_orchestration/gandalf/briefs/2026-07-16-elrond-e4-run-brief.md

WHAT EDITION IV ADDS vs EDITION III (Path A, supplementary admission):
  - 56 NEW supplementary points: 47 D1-derived positives (42 LA + 5 MCD) + 3 R-1 pull re-keys
    (d3/d4/di, speced-corpus, T2-PASS) + 6 D1-derived tombstones. Plate = 469 active + 93 supplementary
    = 562 (spec §2 "562 if the 3 pull re-keys pass T2").
  - `edition_admitted: 4` on every NEW point (parse-contract-friendly; existing 506 UNCHANGED).
  - § 9 cos² table (per admitted point, squared cosine in the frozen basis; medians vs E1-active).
  - § 9 NEW-LEVEL CENSUS (D1-derived levels absent from the frozen indicator matrix; per-point
    `level_flattened` stamps) + the P-3 two-arm refit-trigger evaluation.
  - gate_report block: G-1..G-4 + P-E4-1..6 prediction grades.

FROZEN-BASIS GATE (G-3, PASS-by-construction / vacuous-with-teeth): the byte-identity of the E3
basis block + all 506 E3 point coords is ASSERTED (the E2/E3 guarantee, now a run gate). The frozen
basis is reconstructed from the durable snapshot atlas-frozen-fit-cellkeys-edition1.csv (via
atlas_frozen_basis_reconstruct.FrozenBasis, whose smoke test reproduces the 469 served active + 37
served tombstones to < 1e-6 — the projection surface IS the frozen camera).

NOTHING SERVED. corpus.db was mutated ONLY by the D1 derivation script (cell_key/unresolved/death_class);
this emitter is READ-ONLY on corpus.db and writes ONLY atlas-edition4.json.

Provenance: elrond (data steward). TOOL script (curation/emission), not engine code.
"""

import csv
import json
import math
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import ghost_field_edition3 as ghost_field_mod
import atlas_frozen_basis_reconstruct as recon
from atlas_derivation_2026_07_14 import NAMES

CORPUS_DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
ACTIVE_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-active.csv")
SUPPLEMENTARY_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-supplementary.csv")
LOADINGS_CSV = os.path.join(ATLAS_DIR, "atlas-loadings.csv")
EDITION1_JSON = os.path.join(ATLAS_DIR, "atlas.json")            # frozen Edition-I (basis source-of-truth)
EDITION3_JSON = os.path.join(ATLAS_DIR, "atlas-edition3.json")   # served truth (E3 = 506 points)
OUTPUT_JSON = os.path.join(ATLAS_DIR, "atlas-edition4.json")

FROZEN = True
RATIFIED = "2026-07-14"
METHOD = ("MCA with Greenacre-corrected inertia, MFA block-weighted; "
          "parallel-analysis retention of 14 dims (95th-pct null threshold); "
          "seed 20260714; prereg v1.1")
LOADINGS_REF = "atlas-loadings.csv"
INERTIA_PCT = 8.36
RETAINED_DIMS = 14
STRUCTURE_STATEMENT = "continuum with condensations, not discrete cells"
AXIS_NAMES = {"dim1": "PERFORM <-> DEPLOY", "dim2": "EMBODY <-> LAUNCH"}

EDITION = 4
EDITION_LABEL = "Edition-IV"
EXPECTED_ACTIVE_COUNT = 469
EXPECTED_LEGACY_SUPP = 37
DIM_COUNT = 14
FLOAT_FORMAT = ".8g"
BADGE_FIELDS_MANDATORY = ["inertia_pct", "retained_dims", "structure_statement"]
NULL_DEATH_CLASS_SENTINEL = "unknown-pending-recrawl"
EXACT_DENOMINATOR = 767411820

# Edition-IV intrinsic-pull kit set (acceptance 25, refreshed to ACTUAL kit_ids): the E3 pull kits
# + the 2 curated Destroyer rows now keyed vortex_pull+pull. (The E3 set's stale la-destroyer-*
# names referred to deleted rows; the live pull carriers are the 2 engraving-grain Destroyers.)
INTRINSIC_PULL_KITS = {
    "d3-zbarb", "di-cyclone-monk-pvp",
    "d4-spiritborn-vortex", "d3-wizard-black-hole", "di-cyclone-strike-monk-base",
    "la-rage-hammer-destroyer", "la-gravity-training-destroyer",
}

# R-2: the non-record placeholder negative (named; death_class stays sentinel).
NON_RECORD_NEGATIVES = {"la-rage-hammer-destroyer-bt"}


def _fmt(v):
    return float(format(v, FLOAT_FORMAT))


def _sanitize(obj):
    """Recursively cast numpy scalar types (bool_/int_/float_) to Python natives for json.dump."""
    import numpy as _np
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, _np.bool_):
        return bool(obj)
    if isinstance(obj, _np.integer):
        return int(obj)
    if isinstance(obj, _np.floating):
        return float(obj)
    return obj


def _check_nan(val, ctx):
    if math.isnan(val) or math.isinf(val):
        raise ValueError(f"NaN/Inf coordinate detected: {ctx}")


# ---------------------------------------------------------------------------
# frozen 506 readers (byte-identical carry from E3 / E1)
# ---------------------------------------------------------------------------
def _read_active(path):
    points = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kit_id = row["kit_id"].strip()
            coords = {}
            for d in range(1, DIM_COUNT + 1):
                val = float(row[f"dim{d}"].strip())
                _check_nan(val, f"{kit_id} dim{d}")
                coords[f"dim{d}"] = _fmt(val)
            points.append({"kit_id": kit_id, "x": coords["dim1"], "y": coords["dim2"],
                           "supplementary": False,
                           "gateA_group": row.get("gateA_group", "").strip() or None,
                           "franchise": row.get("franchise_rollup", "").strip() or None})
    points.sort(key=lambda p: p["kit_id"])
    return points


def _read_supplementary(path):
    points = []
    null_dc = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kit_id = row["kit_id"].strip()
            coords = {}
            for d in range(1, DIM_COUNT + 1):
                val = float(row[f"dim{d}"].strip())
                _check_nan(val, f"{kit_id} dim{d}")
                coords[f"dim{d}"] = _fmt(val)
            dc = row.get("death_class", "").strip() or NULL_DEATH_CLASS_SENTINEL
            if dc == NULL_DEATH_CLASS_SENTINEL:
                null_dc += 1
            points.append({"kit_id": kit_id, "x": coords["dim1"], "y": coords["dim2"],
                           "supplementary": True, "death_class": dc})
    points.sort(key=lambda p: p["kit_id"])
    return points, null_dc


def _read_loadings(path):
    loadings = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            loadings.append({"dim": int(row["dim"]), "rank": int(row["rank"]),
                             "coordinate": row["coordinate"].strip(), "level": row["level"].strip(),
                             "loading": _fmt(float(row["loading"])),
                             "abs_loading": _fmt(float(row["abs_loading"]))})
    loadings.sort(key=lambda r: (r["dim"], r["rank"]))
    return loadings


# ---------------------------------------------------------------------------
# GATES
# ---------------------------------------------------------------------------
def gate1_grain(con):
    """G-1: staged population 100% grain='kit'; zero system/gear/class rows. Binary."""
    non_kit = con.execute(
        "SELECT COUNT(*) FROM canon_corpus cc JOIN canon_engine_key cek ON cc.kit_id=cek.kit_id "
        "WHERE cek.cell_key IS NOT NULL AND cc.dossier_owed=0 AND (cc.grain IS NULL OR cc.grain != 'kit')"
    ).fetchone()[0]
    return {"gate": "G-1", "name": "grain", "pass": non_kit == 0, "non_kit_staged": non_kit}


def gate2_provenance(con):
    """G-2: breach-path tripwire returns zero. Non-silent: any grain=kit row from a non-speced /
    non-9.19 / non-E1-lineage / non-pull-tranche provenance is a breach survivor (HALT)."""
    LEGIT = ("mobile-harvest-v3", "mint-dossier-reexpressed", "pull-tranche-edition2-2026-07-15",
             "canon-harvest-9.19-la-2026-07-16", "canon-harvest-9.19-mcd-2026-07-16")
    q = ("SELECT provenance_tag, COUNT(*) FROM canon_corpus WHERE grain='kit' AND provenance_tag NOT IN "
         "(" + ",".join("?" * len(LEGIT)) + ") GROUP BY provenance_tag")
    breach = con.execute(q, LEGIT).fetchall()
    return {"gate": "G-2", "name": "provenance", "pass": len(breach) == 0,
            "breach_survivors": [{"provenance_tag": p, "n": n} for p, n in breach]}


def gate3_congruence(basis, all_points, fb):
    """G-3 (Path A): byte-identity of the E3 basis + 506 E3 point coords in the E4 artifact
    (vacuous-with-teeth: the check RUNS). PLUS the reconstruction smoke test (the projection surface
    reproduces the 469 served active + 37 served tombstones to < 1e-6)."""
    with open(EDITION3_JSON) as f:
        e3 = json.load(f)
    # basis byte-identity (E3's basis is Edition-I frozen)
    if basis != e3["basis"]:
        return {"gate": "G-3", "name": "congruence", "pass": False,
                "fail": "basis block differs from E3", "e3_basis": e3["basis"], "e4_basis": basis}
    e3_pts = {p["kit_id"]: p for p in e3["points"]}
    e4_pts = {p["kit_id"]: p for p in all_points}
    # every E3 point must be present + byte-identical in E4
    missing = sorted(set(e3_pts) - set(e4_pts))
    if missing:
        return {"gate": "G-3", "name": "congruence", "pass": False,
                "fail": f"{len(missing)} E3 points missing from E4", "missing": missing[:10]}
    moved = []
    for kid, a in e3_pts.items():
        b = e4_pts[kid]
        if a["x"] != b["x"] or a["y"] != b["y"] or a.get("supplementary") != b.get("supplementary"):
            moved.append(kid)
        if a.get("supplementary") and a.get("death_class") != b.get("death_class"):
            moved.append(kid + "(death_class)")
    smoke_err, smoke_n, smoke_worst = fb.smoke_test()
    tomb_err, tomb_n = _tombstone_smoke(fb)
    ok = (len(moved) == 0 and smoke_err < 1e-6 and tomb_err < 1e-6)
    return {"gate": "G-3", "name": "congruence", "pass": ok, "type": "PASS-by-construction (Path A)",
            "e3_points_preserved": len(e3_pts) - len(moved), "e3_points_total": len(e3_pts),
            "moved_points": moved,
            "reconstruction_smoke": {"active_max_abs_err": smoke_err, "active_n": smoke_n,
                                     "active_worst": smoke_worst,
                                     "tombstone_max_abs_err": tomb_err, "tombstone_n": tomb_n,
                                     "tolerance": 1e-6}}


def _tombstone_smoke(fb):
    """Reproduce the 37 served tombstones from their DB cell_keys via the projection surface."""
    with open(EDITION3_JSON) as f:
        e3 = json.load(f)
    served = {p["kit_id"]: (float(p["x"]), float(p["y"])) for p in e3["points"] if p.get("supplementary")}
    con = sqlite3.connect(CORPUS_DB)
    ck = dict(con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL AND c.negative=1").fetchall())
    con.close()
    max_err, n = 0.0, 0
    for kid, (sx, sy) in served.items():
        if kid in ck:
            xy = fb.project_point_xy(ck[kid])
            if xy:
                max_err = max(max_err, abs(xy[0] - sx), abs(xy[1] - sy))
                n += 1
    return max_err, n


def gate4_census(con, new_points, e3_active, e3_supp):
    """G-4: staged census matches spec §2 expectations after named reconciliations R-1..R-3.
    Fail-loud, every delta named."""
    new_pos = [p for p in new_points if p.get("_neg") == 0]
    new_neg = [p for p in new_points if p.get("_neg") == 1]
    la_pos = [p for p in new_pos if p["kit_id"].startswith("la-")]
    mcd_pos = [p for p in new_pos if p["kit_id"].startswith("mcd-")]
    rekey_pos = [p for p in new_pos if not p["kit_id"].startswith(("la-", "mcd-"))]
    # held-out (T4)
    held = [r[0] for r in con.execute(
        "SELECT kit_id FROM canon_corpus WHERE dossier_owed=1 ORDER BY kit_id").fetchall()]
    # excluded (T1)
    excl = con.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL OR grain != 'kit'").fetchone()[0]
    terms = {
        "active_basis (frozen, unchanged)": e3_active,
        "legacy_tombstones (E3, unchanged; incl. hot-blood-catcher R-3)": e3_supp,
        "new_positives_D1 (42 LA + 5 MCD)": len(la_pos) + len(mcd_pos),
        "new_positives_R1_pull_rekeys (d3/d4/di, T2-PASS)": len(rekey_pos),
        "new_tombstones (5 seated + 1 sentinel non-record R-2)": len(new_neg),
    }
    staged = sum(terms.values())
    expected = 562
    return {"gate": "G-4", "name": "census", "pass": staged == expected,
            "staged_total": staged, "expected_total": expected,
            "terms": terms,
            "excluded_T1_system_records": excl,
            "held_out_T4_dossier_owed": {"n": len(held), "kits": held},
            "R1_pull_rekeys": sorted(p["kit_id"] for p in rekey_pos),
            "R2_new_tombstones": {"seated_extrinsic_tuning":
                                  sorted(p["kit_id"] for p in new_neg if p["kit_id"] not in NON_RECORD_NEGATIVES),
                                  "sentinel_non_record": sorted(NON_RECORD_NEGATIVES)},
            "R3_preexisting_unresolved_with_cellkey": "hot-blood-catcher (E3 tombstone; unresolved=1 is a "
            "patched-bug-relic re-verification flag, death_class=system-evidence; already keyed + admitted; "
            "orthogonal to fit-input resolution; carried forward unchanged)"}


# ---------------------------------------------------------------------------
# § 9 disclosures (cos² + NEW-LEVEL CENSUS) + P-3 trigger
# ---------------------------------------------------------------------------
def build_section9(con, fb, admitted_ids):
    """Per admitted point: cos² in the frozen basis (plane communality) + absent-from-basis levels.
    Returns (per_point dict, cos2_summary, new_level_census, refit_trigger)."""
    ck = dict(con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k WHERE k.cell_key IS NOT NULL").fetchall())
    per_point = {}
    admitted_cos2 = []
    census = Counter()
    census_kits = defaultdict(list)
    for kid in admitted_ids:
        cellk = ck.get(kid)
        if cellk is None:
            continue
        c2 = fb.cos2_one(cellk)
        flat = fb.level_flatten(cellk)   # list of (coord, level) absent from frozen basis
        flat_str = [f"{c}:{lv}" for c, lv in flat]
        per_point[kid] = {"cos2": None if c2 is None else round(c2, 6), "level_flattened": flat_str}
        if c2 is not None:
            admitted_cos2.append(c2)
        for c, lv in flat:
            census[f"{c}:{lv}"] += 1
            census_kits[f"{c}:{lv}"].append(kid)

    # E1-active baseline cos² (reconstruct the 469 actives' plane communality in the same basis)
    active_cos2 = []
    for kid in fb.ids:
        i = fb.ids.index(kid)
        coord = fb.active_row_pc[i]
        denom = float((coord ** 2).sum())
        if denom > 0:
            active_cos2.append(float((coord[:2] ** 2).sum() / denom))

    def med(a):
        return round(float(sorted(a)[len(a) // 2]), 6) if a else None
    admit_med = med(admitted_cos2)
    active_med = med(active_cos2)
    ratio = round(admit_med / active_med, 4) if (admit_med and active_med) else None

    cos2_summary = {
        "admitted_median_cos2_plane": admit_med,
        "e1_active_median_cos2_plane": active_med,
        "ratio_admitted_over_active": ratio,
        "n_admitted_scored": len(admitted_cos2),
        "n_e1_active": len(active_cos2),
        "note": ("cos² = plane communality (F1²+F2²)/Σ_d F_d² in the retained 14-dim frozen basis. "
                 "Low ratio = the frozen plane expresses the admitted cohort's variance weakly "
                 "(P-3 arm-1 input; the honest Path-A cost, made empirical).")}

    new_level_census = sorted(
        [{"level": k, "exhibit_count": v, "kits_sample": sorted(census_kits[k])[:6]}
         for k, v in census.items()], key=lambda r: -r["exhibit_count"])

    # P-3 two-arm refit trigger
    arm1_line = 0.5 * active_med if active_med else None
    arm1_fires = (admit_med is not None and arm1_line is not None and admit_med < arm1_line)
    top_absent = max((v for v in census.values()), default=0)
    arm2_level = max(census, key=census.get) if census else None
    arm2_fires = top_absent >= 20
    refit_trigger = {
        "arm1_expression": {"admitted_median_cos2": admit_med,
                            "threshold_0.5x_active_median": None if arm1_line is None else round(arm1_line, 6),
                            "fires": bool(arm1_fires)},
        "arm2_vocabulary": {"largest_absent_level": arm2_level, "exhibit_count": top_absent,
                            "threshold": 20, "fires": bool(arm2_fires)},
        "e5_refit_triggered": bool(arm1_fires or arm2_fires),
        "note": ("Either arm fires E5 as a Path-B refit (§6; gates pre-registered). Relative/structural "
                 "thresholds, self-calibrating against the frozen basis's own baseline.")}
    return per_point, cos2_summary, new_level_census, refit_trigger


# ---------------------------------------------------------------------------
# predictions P-E4-1..6
# ---------------------------------------------------------------------------
def grade_predictions(con, fb, new_points, section9):
    per_point, cos2_summary, new_level_census, refit_trigger = section9
    ck = dict(con.execute("SELECT kit_id, cell_key FROM canon_engine_key WHERE cell_key IS NOT NULL").fetchall())
    grades = {}

    # full-space coords for all keyed rows (for nearest-neighbour predictions)
    def full_coord(kid):
        c = ck.get(kid)
        return None if c is None else fb.project_one(c)
    # active full coords (reconstructed 14-dim)
    active_full = {kid: fb.active_row_pc[i] for i, kid in enumerate(fb.ids)}

    # P-E4-5 (D1-fidelity acceptance): both Destroyers geometry=vortex_pull
    destro = {}
    for kid in ("la-rage-hammer-destroyer", "la-gravity-training-destroyer"):
        c = ck.get(kid)
        destro[kid] = (c.split("|")[NAMES.index("geometry")] if c else None)
    p5 = all(v == "vortex_pull" for v in destro.values()) and len(destro) == 2
    grades["P-E4-5"] = {"claim": "both la-*-destroyer rows derive geometry=vortex_pull",
                        "computable": True, "result": "PASS" if p5 else "FAIL", "evidence": destro}

    # P-E4-6 (new-level census): identity-gauge economy is the largest absent-from-basis level (~30)
    gauge = next((r for r in new_level_census if r["level"].startswith("economy:identity-gauge")), None)
    top = new_level_census[0] if new_level_census else None
    p6_ok = (gauge is not None and top is not None and top["level"] == gauge["level"])
    grades["P-E4-6"] = {"claim": "identity-gauge economy is absent-from-basis with the largest exhibit mass",
                        "computable": True, "result": "PASS" if p6_ok else "FAIL",
                        "identity_gauge_count": (gauge or {}).get("exhibit_count"),
                        "largest_absent_level": (top or {}).get("level"),
                        "arm2_line": 20}

    # P-E4-4 (Path A diagnostic): admitted median cos² within 2× of E1-active median
    am, em = cos2_summary["admitted_median_cos2_plane"], cos2_summary["e1_active_median_cos2_plane"]
    within2x = (am is not None and em is not None and am >= em / 2.0)
    grades["P-E4-4"] = {"claim": "admitted median cos² within 2× of E1-actives' median",
                        "computable": True, "result": "PASS" if within2x else "FAIL",
                        "admitted_median": am, "active_median": em,
                        "ratio": cos2_summary["ratio_admitted_over_active"],
                        "note": "FAIL here = E1 axes express LA/MCD variance poorly -> refit pressure (P-3)."}

    # P-E4-2 (proto-GAUGE): LA gauge-melee identities mutually condense (mean pairwise full-space
    # distance below corpus mean). Gauge-melee = LA rows with economy=identity-gauge AND range=melee.
    gauge_melee = []
    for kid in [p["kit_id"] for p in new_points if p["kit_id"].startswith("la-")]:
        c = ck.get(kid)
        if not c:
            continue
        parts = c.split("|")
        if parts[NAMES.index("economy")] == "identity-gauge" and parts[NAMES.index("range")] == "melee":
            fc = full_coord(kid)
            if fc is not None:
                gauge_melee.append((kid, fc))
    p2 = _condense_test(gauge_melee, active_full, fb, ck)
    grades["P-E4-2"] = {"claim": "LA gauge-melee identities mutually condense (mean pairwise < corpus mean)",
                        "computable": p2 is not None, **(p2 or {"result": "UNGRADEABLE"})}

    # P-E4-1 (mcd-summoner nearest ratified family = MINION-PET) — full-space nearest ACTIVE seed
    p1 = _nearest_family(con, fb, ck, "mcd-summoner", active_full)
    grades["P-E4-1"] = {"claim": "mcd-summoner's nearest ratified family = MINION-PET", **p1}

    # P-E4-3 (tombstone-beside-parent): each of the 6 LA negative twins lands nearer its positive twin
    # than the corpus median nearest-neighbour distance.
    p3 = _twin_proximity(con, fb, ck)
    grades["P-E4-3"] = {"claim": "each LA negative twin nearer its positive twin than corpus median NN",
                        **p3}

    return grades


def _condense_test(cohort, active_full, fb, ck):
    if len(cohort) < 3:
        return None
    import itertools
    coords = [c for _, c in cohort]
    pair = [float(((coords[i] - coords[j]) ** 2).sum() ** 0.5)
            for i, j in itertools.combinations(range(len(coords)), 2)]
    mean_pair = sum(pair) / len(pair)
    # corpus mean pairwise over a sample of active full coords
    acts = list(active_full.values())
    import random
    random.seed(20260716)
    samp = random.sample(acts, min(60, len(acts)))
    cpair = [float(((samp[i] - samp[j]) ** 2).sum() ** 0.5)
             for i, j in itertools.combinations(range(len(samp)), 2)]
    corpus_mean = sum(cpair) / len(cpair)
    return {"result": "PASS" if mean_pair < corpus_mean else "FAIL",
            "n_cohort": len(cohort), "mean_pairwise": round(mean_pair, 4),
            "corpus_mean_pairwise": round(corpus_mean, 4)}


def _nearest_family(con, fb, ck, kid, active_full):
    c = ck.get(kid)
    if c is None:
        return {"computable": False, "result": "UNGRADEABLE", "why": f"{kid} has no cell_key"}
    fc = fb.project_one(c)
    # gateA family of nearest active seed
    labels = dict(con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k").fetchall())  # noqa (not used directly)
    # read gateA_group from active csv
    gateA = {}
    with open(ACTIVE_CSV, newline="") as f:
        for row in csv.DictReader(f):
            g = (row.get("gateA_group") or "").strip()
            if g:
                gateA[row["kit_id"].strip()] = g
    best, bestd = None, 1e18
    for akid, ac in active_full.items():
        if akid in gateA:
            d = float(((ac - fc) ** 2).sum() ** 0.5)
            if d < bestd:
                bestd, best = d, akid
    fam = gateA.get(best)
    return {"computable": True, "result": "PASS" if fam == "MINION-PET" else "FAIL",
            "nearest_active_seed": best, "nearest_family": fam, "distance": round(bestd, 4)}


def _twin_proximity(con, fb, ck):
    rows = con.execute(
        "SELECT k.kit_id, k.raw_json FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE c.negative=1 AND c.source_date='2026-07-16' AND k.cell_key IS NOT NULL").fetchall()
    # corpus median NN distance over all keyed full coords
    allk = [(kid, fb.project_one(c)) for kid, c in ck.items()]
    allk = [(k, v) for k, v in allk if v is not None]
    import random
    random.seed(20260716)
    samp = random.sample(allk, min(120, len(allk)))
    nn = []
    for i, (ki, ci) in enumerate(samp):
        d = min(float(((ci - cj) ** 2).sum() ** 0.5) for j, (kj, cj) in enumerate(samp) if j != i)
        nn.append(d)
    med_nn = sorted(nn)[len(nn) // 2]
    results = []
    for kid, raw in rows:
        d = json.loads(raw)
        twin = d.get("neg_twin")
        c_neg = ck.get(kid)
        c_pos = ck.get(twin) if twin else None
        if c_neg is None or c_pos is None:
            results.append({"neg": kid, "twin": twin, "gradeable": False})
            continue
        dist = float(((fb.project_one(c_neg) - fb.project_one(c_pos)) ** 2).sum() ** 0.5)
        results.append({"neg": kid, "twin": twin, "gradeable": True,
                        "dist_to_twin": round(dist, 4), "nearer_than_median_nn": bool(dist < med_nn)})
    gradeable = [r for r in results if r.get("gradeable")]
    n_pass = sum(1 for r in gradeable if r["nearer_than_median_nn"])
    return {"computable": len(gradeable) > 0,
            "result": ("PASS" if gradeable and n_pass == len(gradeable) else
                       ("PARTIAL" if n_pass else "FAIL")),
            "corpus_median_nn": round(med_nn, 4), "n_gradeable": len(gradeable),
            "n_nearer_twin": n_pass, "per_twin": results}


# ---------------------------------------------------------------------------
# main build
# ---------------------------------------------------------------------------
def build():
    print(f"[edition4] frozen basis reconstruction + smoke test...")
    fb = recon.FrozenBasis()
    smoke_err, smoke_n, worst = fb.smoke_test()
    if smoke_err >= 1e-6:
        raise ValueError(f"HALT: frozen-basis reconstruction drift {smoke_err:.3e} >= 1e-6 "
                         f"(projection surface is NOT the frozen camera). E3 remains truth.")
    print(f"  [smoke] reproduced {smoke_n} served active to {smoke_err:.2e} OK")

    active_points = _read_active(ACTIVE_CSV)
    if len(active_points) != EXPECTED_ACTIVE_COUNT:
        raise ValueError(f"HALT: active count {len(active_points)} != {EXPECTED_ACTIVE_COUNT}.")
    legacy_supp, null_dc = _read_supplementary(SUPPLEMENTARY_CSV)
    if len(legacy_supp) != EXPECTED_LEGACY_SUPP:
        raise ValueError(f"HALT: legacy supplementary {len(legacy_supp)} != {EXPECTED_LEGACY_SUPP}.")
    loadings = _read_loadings(LOADINGS_CSV)

    basis = {"edition": 1, "frozen": FROZEN, "ratified": RATIFIED, "method": METHOD,
             "loadings_ref": LOADINGS_REF, "inertia_pct": INERTIA_PCT, "retained_dims": RETAINED_DIMS,
             "structure_statement": STRUCTURE_STATEMENT, "axis_names": AXIS_NAMES}
    for field in BADGE_FIELDS_MANDATORY:
        if not basis.get(field):
            raise ValueError(f"HALT: mandatory badge field '{field}' missing.")

    con = sqlite3.connect(CORPUS_DB)
    con.row_factory = sqlite3.Row

    # NEW admits = grain=kit, cell_key NOT NULL, dossier_owed=0, NOT in E3
    e3_ids = set(p["kit_id"] for p in json.load(open(EDITION3_JSON))["points"])
    new_rows = con.execute(
        "SELECT cc.kit_id, cc.negative, cc.death_class, cek.cell_key "
        "FROM canon_corpus cc JOIN canon_engine_key cek ON cc.kit_id=cek.kit_id "
        "WHERE cc.grain='kit' AND cek.cell_key IS NOT NULL AND cc.dossier_owed=0 "
        "ORDER BY cc.kit_id").fetchall()
    new_points = []
    for r in new_rows:
        kid = r["kit_id"]
        if kid in e3_ids:
            continue
        xy = fb.project_point_xy(r["cell_key"])
        if xy is None:
            raise ValueError(f"HALT: new admit {kid} is unprojectable (all-mask cell_key). "
                             f"Cannot seat on plane. E3 remains truth.")
        pt = {"kit_id": kid, "x": _fmt(xy[0]), "y": _fmt(xy[1]), "supplementary": True,
              "edition_admitted": 4, "_neg": r["negative"]}
        if r["negative"] == 1:
            pt["death_class"] = r["death_class"] or NULL_DEATH_CLASS_SENTINEL
        new_points.append(pt)

    print(f"[edition4] new supplementary admits: {len(new_points)} "
          f"({sum(1 for p in new_points if p['_neg']==0)} pos + "
          f"{sum(1 for p in new_points if p['_neg']==1)} neg)")

    # assemble full point set (frozen 506 unchanged + new)
    all_points = []
    for p in active_points:
        all_points.append({"kit_id": p["kit_id"], "x": p["x"], "y": p["y"], "supplementary": False,
                           "gateA_group": p["gateA_group"], "franchise": p["franchise"]})
    for p in legacy_supp:
        all_points.append({"kit_id": p["kit_id"], "x": p["x"], "y": p["y"], "supplementary": True,
                           "death_class": p["death_class"]})
    for p in new_points:
        q = {"kit_id": p["kit_id"], "x": p["x"], "y": p["y"], "supplementary": True,
             "edition_admitted": 4}
        if "death_class" in p:
            q["death_class"] = p["death_class"]
        all_points.append(q)
    all_points.sort(key=lambda p: p["kit_id"])

    # ---- GATES ----
    print("[edition4] running gates G-1..G-4...")
    g1 = gate1_grain(con)
    g2 = gate2_provenance(con)
    g3 = gate3_congruence(basis, all_points, fb)
    g4 = gate4_census(con, new_points, EXPECTED_ACTIVE_COUNT, EXPECTED_LEGACY_SUPP)
    for g in (g1, g2, g3, g4):
        print(f"  {g['gate']} ({g['name']}): {'PASS' if g['pass'] else 'FAIL'}")
        if not g["pass"]:
            print(f"    !!! HALT: {g['gate']} FAILED: {json.dumps({k:v for k,v in g.items() if k!='pass'})[:400]}",
                  file=sys.stderr)
    if not all(g["pass"] for g in (g1, g2, g3, g4)):
        con.close()
        raise ValueError("HALT: a gate FAILED. E4 not emitted; E3 remains truth. See gate report above.")

    # ---- § 9 disclosures ----
    print("[edition4] § 9 cos² + NEW-LEVEL CENSUS + P-3 trigger...")
    admitted_ids = [p["kit_id"] for p in new_points]
    per_point, cos2_summary, new_level_census, refit_trigger = build_section9(con, fb, admitted_ids)
    section9 = (per_point, cos2_summary, new_level_census, refit_trigger)
    # stamp level_flattened + cos2 onto the new points
    for p in all_points:
        if p.get("edition_admitted") == 4 and p["kit_id"] in per_point:
            p["cos2"] = per_point[p["kit_id"]]["cos2"]
            if per_point[p["kit_id"]]["level_flattened"]:
                p["level_flattened"] = per_point[p["kit_id"]]["level_flattened"]

    print(f"  cos² admitted median={cos2_summary['admitted_median_cos2_plane']} vs "
          f"E1-active median={cos2_summary['e1_active_median_cos2_plane']} "
          f"(ratio {cos2_summary['ratio_admitted_over_active']})")
    print(f"  NEW-LEVEL CENSUS top: " +
          "; ".join(f"{r['level']}={r['exhibit_count']}" for r in new_level_census[:4]))
    print(f"  P-3 refit trigger: arm1={refit_trigger['arm1_expression']['fires']} "
          f"arm2={refit_trigger['arm2_vocabulary']['fires']} "
          f"-> E5={refit_trigger['e5_refit_triggered']}")

    # ---- predictions ----
    print("[edition4] grading predictions P-E4-1..6...")
    grades = grade_predictions(con, fb, new_points, section9)
    for k in sorted(grades):
        print(f"  {k}: {grades[k].get('result')}")

    # ---- ghost field (live census; lattice unchanged) ----
    print("[edition4] ghost field (live census; register frozen)...")
    ghost_field = ghost_field_mod.build_ghost_field(con, atlas_points=all_points)
    if ghost_field["depth_sum_check"] != EXACT_DENOMINATOR:
        raise ValueError(f"HALT: depth_sum {ghost_field['depth_sum_check']} != {EXACT_DENOMINATOR}.")
    ghost_field["edition"] = "IV"
    ghost_field["edition4_change"] = (
        "SUPPLEMENTARY-ADMISSION edition (Path A): 56 new supplementary points (47 D1-derived LA/MCD "
        "positives + 3 R-1 pull re-keys + 6 tombstones). Lattice UNCHANGED (denominators byte-identical; "
        "depth_sum 767,411,820). Frozen basis UNCHANGED (all 506 E3 coords byte-identical). Lit occupancy "
        "grows with the newly-keyed rows (read live). New points PROJECT into the frozen basis — no "
        "basis re-derivation. off_plane_corpus / unmapped are fit-relative facts RE-DERIVED live by the "
        "ghost machinery for the E4 membership (THREE-CLASS FACT RULE, atlas MIGRATION).")
    # pull-slice integrity with the refreshed INTRINSIC_PULL_KITS
    _assert_pull_slice(ghost_field, con)

    emitted_at = datetime.now(timezone.utc).isoformat()
    n_active = sum(1 for p in all_points if not p.get("supplementary"))
    n_supp = sum(1 for p in all_points if p.get("supplementary"))
    n_new = len(new_points)

    # strip the private _neg helper (not part of the contract) — new_points is not embedded raw
    gate_report = {
        "spec": "edition4-refit-spec.md (RATIFIED; Path A supplementary admission)",
        "G-1_grain": g1, "G-2_provenance": g2, "G-3_congruence": g3, "G-4_census": g4,
        "predictions": grades,
        "section9_cos2": cos2_summary,
        "section9_new_level_census": new_level_census,
        "section9_refit_trigger": refit_trigger,
    }

    atlas = {
        "atlas_version": EDITION_LABEL, "edition": EDITION,
        "path": "A — supplementary admission (frozen Edition-I basis; new citizens projected in)",
        "badge_fields_mandatory": BADGE_FIELDS_MANDATORY,
        "emitted_at": emitted_at,
        "emitter_script": "agentic_orchestration/research/scripts/build_atlas_json_edition4.py",
        "emitter_parent": "build_atlas_json_edition3.py",
        "fit_layer_frozen_vs": "Edition-I (atlas.json) — basis + 506 point coords + tombstones byte-identical (G-3)",
        "served_note": "NOTHING SERVED. Edition-III stays served truth until Matt ratifies Edition IV.",
        "basis": basis, "loadings": loadings,
        "counts": {"active": n_active, "supplementary": n_supp, "total": len(all_points),
                   "new_supplementary_edition4": n_new,
                   "new_positives": sum(1 for p in new_points if p["_neg"] == 0),
                   "new_tombstones": sum(1 for p in new_points if p["_neg"] == 1),
                   "legacy_tombstones": EXPECTED_LEGACY_SUPP,
                   "null_death_class_sentineled": null_dc,
                   "held_out_dossier_owed": g4["held_out_T4_dossier_owed"]["n"]},
        "points": all_points,
        "gate_report": gate_report,
        "ghost_field": ghost_field,
        "p_df_1_verdict": ghost_field["p_df_1"]["verdict"],
    }

    print(f"[edition4] writing {OUTPUT_JSON}")
    atlas = _sanitize(atlas)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(atlas, f, sort_keys=True, indent=2, ensure_ascii=False)
    con.close()
    sz = os.path.getsize(OUTPUT_JSON)
    print(f"  Done. {len(all_points)} total points ({n_active} active + {n_supp} supp; {n_new} new); "
          f"atlas-edition4.json = {sz/1e6:.2f} MB")
    return atlas


def _assert_pull_slice(ghost, con):
    rows = con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL").fetchall()
    pull, mcd_pull = [], []
    fi = ghost_field_mod.CK_IDX["function"]
    for kid, ck in rows:
        if ck.split("|")[fi] == "pull":
            pull.append(kid)
            if kid.startswith("mcd-"):
                mcd_pull.append(kid)
    non_intrinsic = set(pull) - INTRINSIC_PULL_KITS
    if non_intrinsic:
        raise ValueError(f"HALT: pull-slice integrity — non-intrinsic pull kits: {sorted(non_intrinsic)}")
    if mcd_pull:
        raise ValueError(f"HALT: pull-slice integrity — mcd pull kits (must be zero): {sorted(mcd_pull)}")
    print(f"  [pull-slice] {len(pull)} pull kits, all intrinsic; zero mcd-lit OK")


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"EMITTER FAILED (loud): {e}", file=sys.stderr)
        sys.exit(1)
