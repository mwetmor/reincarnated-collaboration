#!/usr/bin/env python3
"""
build_atlas_refit_candidate_1_json.py — deterministic emitter for atlas-refit-candidate-1.json.
==============================================================================================
REFIT CANDIDATE 1 — a COMPARISON EXPERIMENT, not an Edition. The string "Edition IV" appears
NOWHERE. Edition III (atlas-edition3.json) is the served truth and is READ-ONLY. This emits
ALONGSIDE it, schema-compatible so galadriel's render fork consumes it with minimal changes.

Schema-compatible with atlas-edition3.json (same top-level keys):
  atlas_version / edition-analog / register_ref / basis / loadings / counts / points / ghost_field
  + stamps. REFIT stamps: atlas_version="Refit-Candidate-1", ghost_field.edition="Refit-Candidate-1",
  unratified_comparison_artifact=true, emitted_alongside="atlas-edition3.json (served truth; Matt
  comparison pending)". Counts: active 628 / supplementary 37 / total 665.

UNLIKE the Edition-III emitter, this does NOT freeze the fit layer against Edition-I — the WHOLE
POINT of the refit is that the fit MOVED (628-active re-derivation). It reads the REFIT basis/coords/
loadings (refit-candidate-1-*.csv + refit-candidate-1-basis-draft.json), NOT the frozen Edition-I
CSVs. It calls ghost_field_refit_candidate_1 (pull + MELEE un-masked; v1.3 lattice byte-identical).

Fail-loud guards (this artifact's integrity — NOT frozen-fit regression):
  - Active point count != 628 -> raise
  - Supplementary count != 37 -> raise
  - depth_sum_check != v1.3 exact 767,411,820 -> raise (lattice must be byte-identical)
  - would overwrite atlas-edition3.json / atlas.json / atlas-edition2.json -> raise (served read-only)
  - any served Edition artifact path collision -> raise

Author: elrond (data steward). TOOL script. Commission: gandalf Tier-3 refit brief (R4).
Run:  python3 build_atlas_refit_candidate_1_json.py
"""

import csv
import json
import math
import os
import sys
import sqlite3
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import ghost_field_refit_candidate_1 as ghost_field_mod

CORPUS_DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))

# ---- REFIT inputs (NOT the frozen Edition-I CSVs) ----
ACTIVE_CSV = os.path.join(ATLAS_DIR, "refit-candidate-1-coordinates-active.csv")
SUPP_CSV = os.path.join(ATLAS_DIR, "refit-candidate-1-coordinates-supplementary.csv")
LOADINGS_CSV = os.path.join(ATLAS_DIR, "refit-candidate-1-loadings.csv")
BASIS_JSON = os.path.join(ATLAS_DIR, "refit-candidate-1-basis-draft.json")

OUTPUT_JSON = os.path.join(ATLAS_DIR, "atlas-refit-candidate-1.json")
COORD_CSV = os.path.join(ATLAS_DIR, "refit-candidate-1-coordinates.csv")   # slim kit_id,x,y,... for diffing

# ---- served artifacts that MUST NOT be overwritten (iron law: read-only) ----
SERVED_READ_ONLY = {
    os.path.join(ATLAS_DIR, "atlas-edition3.json"),
    os.path.join(ATLAS_DIR, "atlas-edition2.json"),
    os.path.join(ATLAS_DIR, "atlas.json"),
    os.path.join(ATLAS_DIR, "atlas-coordinates-active.csv"),
    os.path.join(ATLAS_DIR, "atlas-coordinates-supplementary.csv"),
    os.path.join(ATLAS_DIR, "atlas-loadings.csv"),
    os.path.join(ATLAS_DIR, "atlas-frozen-fit-cellkeys-edition1.csv"),
}

EXPECTED_ACTIVE = 628
EXPECTED_SUPP = 37
EXPECTED_TOTAL = 665
EXACT_DENOMINATOR = 767411820   # v1.3 — byte-identical (lattice unchanged)
FLOAT_FORMAT = ".8g"
NULL_DEATH_CLASS_SENTINEL = "unknown-pending-recrawl"


def _fmt(v):
    return float(format(v, FLOAT_FORMAT))


def _check_nan(val, ctx):
    if math.isnan(val) or math.isinf(val):
        raise ValueError(f"NaN/Inf coordinate: {ctx}")


def _assert_not_served(path):
    if os.path.abspath(path) in {os.path.abspath(p) for p in SERVED_READ_ONLY}:
        raise ValueError(f"IRON-LAW VIOLATION: refusing to write served read-only artifact {path}.")


def _read_active(path):
    """Read the refit active coordinates. dim1..dimN where N = retained dims (may be > 14 in the refit).
    x,y = dim1,dim2. Carries franchise_rollup + gateA_group + leiden_cluster + lca_class."""
    points = []
    ndim = None
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        dim_cols = [c for c in reader.fieldnames if c.startswith("dim")]
        ndim = len(dim_cols)
        for row in reader:
            kit_id = row["kit_id"].strip()
            if not kit_id:
                raise ValueError("Empty kit_id in active CSV")
            coords = {}
            for c in dim_cols:
                raw = row.get(c, "").strip()
                if not raw:
                    raise ValueError(f"Missing {c} for kit {kit_id}")
                val = float(raw)
                _check_nan(val, f"{kit_id} {c}")
                coords[c] = _fmt(val)
            points.append({
                "kit_id": kit_id, "x": coords["dim1"], "y": coords["dim2"],
                "supplementary": False,
                "gateA_group": (row.get("gateA_group", "").strip() or None),
                "franchise": (row.get("franchise_rollup", "").strip() or None),
                "_all_dims": coords,
            })
    points.sort(key=lambda p: p["kit_id"])
    return points, ndim


def _read_supp(path):
    points = []
    null_dc = 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        dim_cols = [c for c in reader.fieldnames if c.startswith("dim")]
        for row in reader:
            kit_id = row["kit_id"].strip()
            if not kit_id:
                raise ValueError("Empty kit_id in supplementary CSV")
            x = float(row["dim1"]); y = float(row["dim2"])
            _check_nan(x, f"{kit_id} dim1"); _check_nan(y, f"{kit_id} dim2")
            dc = row.get("death_class", "").strip() or NULL_DEATH_CLASS_SENTINEL
            if dc == NULL_DEATH_CLASS_SENTINEL:
                null_dc += 1
            points.append({"kit_id": kit_id, "x": _fmt(x), "y": _fmt(y),
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


def build():
    for p in (OUTPUT_JSON, COORD_CSV):
        _assert_not_served(p)

    with open(BASIS_JSON) as f:
        basis_draft = json.load(f)

    print(f"[refit] Reading refit active coordinates: {ACTIVE_CSV}")
    active_points, ndim = _read_active(ACTIVE_CSV)
    if len(active_points) != EXPECTED_ACTIVE:
        raise ValueError(f"Active count {len(active_points)} != expected {EXPECTED_ACTIVE}.")
    print(f"  Active points: {len(active_points)} (retained dims in CSV: {ndim})")

    supp_points, null_dc = _read_supp(SUPP_CSV)
    if len(supp_points) != EXPECTED_SUPP:
        raise ValueError(f"Supplementary count {len(supp_points)} != expected {EXPECTED_SUPP}.")
    print(f"  Supplementary points: {len(supp_points)} (null death_class: {null_dc})")

    loadings = _read_loadings(LOADINGS_CSV)

    # basis block — schema-compatible with edition3's basis, refit-stamped, NOT frozen-against-E1.
    basis = {
        "edition": "Refit-Candidate-1",
        "frozen": False,
        "unratified_comparison_artifact": True,
        "derived_on_active_n": basis_draft.get("n_active", EXPECTED_ACTIVE),
        "method": basis_draft.get("method"),
        "seed": basis_draft.get("seed"),
        "loadings_ref": "refit-candidate-1-loadings.csv",
        "fit_cellkeys_ref": "refit-candidate-1-fit-cellkeys.csv",
        "inertia_pct": basis_draft.get("inertia_pct_plane"),
        "inertia_pct_per_dim": basis_draft.get("inertia_pct"),
        "retained_dims": basis_draft.get("retained_dims"),
        "plane_diameter": basis_draft.get("plane_diameter"),
        "structure_statement": "continuum with condensations, not discrete cells",
        "gates": basis_draft.get("gates"),
        "pull_active_count": basis_draft.get("pull_active_count"),
        "pull_earned_column": basis_draft.get("pull_earned_column"),
        "delivery_melee_active_count": basis_draft.get("delivery_melee_active_count"),
        "delivery_melee_earned_column": basis_draft.get("delivery_melee_earned_column"),
        "axis_names": {
            "note": ("axis names NOT ratified for the refit — this is a comparison artifact. The R5 "
                     "report gives the post-alignment axis-identity correlations vs Edition-I "
                     "PERFORM<->DEPLOY / EMBODY<->LAUNCH.")},
    }

    all_points = []
    for p in active_points:
        all_points.append({"kit_id": p["kit_id"], "x": p["x"], "y": p["y"],
                           "supplementary": False, "gateA_group": p["gateA_group"],
                           "franchise": p["franchise"]})
    for p in supp_points:
        all_points.append({"kit_id": p["kit_id"], "x": p["x"], "y": p["y"],
                           "supplementary": True, "death_class": p["death_class"]})
    all_points.sort(key=lambda p: p["kit_id"])
    if len(all_points) != EXPECTED_TOTAL:
        raise ValueError(f"Total points {len(all_points)} != expected {EXPECTED_TOTAL}.")

    # --- ghost field: refit basis, pull + MELEE un-masked, v1.3 lattice byte-identical ---
    print("[refit] Building refit ghost_field (pull + MELEE un-masked; v1.3 lattice byte-identical)...")
    con = sqlite3.connect(CORPUS_DB)
    ghost = ghost_field_mod.build_ghost_field(con, atlas_points=all_points)
    con.close()
    if ghost["depth_sum_check"] != EXACT_DENOMINATOR:
        raise ValueError(f"depth_sum {ghost['depth_sum_check']} != v1.3 exact {EXACT_DENOMINATOR} "
                         f"(lattice must be byte-identical).")
    print(f"  [lattice-integrity] depth_sum == {EXACT_DENOMINATOR} (v1.3 byte-identical) OK")
    print(f"  ghost_field: {ghost['denominators']['meso_feasible']} feasible + "
          f"{ghost['denominators']['meso_sealed']} sealed; {ghost['lit_cells']} lit "
          f"(pull-lit {ghost['pull_slice']['lit_cells']}, melee-lit {ghost['melee_slice']['lit_cells']}); "
          f"off-plane N={ghost['off_plane_corpus']['n']}")

    emitted_at = datetime.now(timezone.utc).isoformat()
    atlas = {
        "atlas_version": "Refit-Candidate-1",
        "edition": "Refit-Candidate-1",
        "unratified_comparison_artifact": True,
        "register_ref": "feasibility-cuts-register-v1.3",
        "emitted_at": emitted_at,
        "emitter_script": "agentic_orchestration/research/scripts/build_atlas_refit_candidate_1_json.py",
        "emitted_alongside": "atlas-edition3.json (served truth; Matt comparison pending)",
        "comparison_note": ("Full re-derivation of the atlas FIT on the current 628-active corpus "
                            "(incl. 62 Lost Ark + pull/MELEE as live feature columns). Same "
                            "pre-registered methodology, same seed 20260714. Edition III served truth "
                            "is byte-untouched. This is the number surface for Matt's adoption decision "
                            "(Refit Candidate 1 vs Edition III); see refit-candidate-1-comparison-report.md."),
        "basis": basis,
        "loadings": loadings,
        "counts": {"active": len(active_points), "supplementary": len(supp_points),
                   "total": len(all_points), "null_death_class_sentineled": null_dc},
        "points": all_points,
        "ghost_field": ghost,
    }

    print(f"[refit] Writing {OUTPUT_JSON} (alongside atlas-edition3.json — never over)")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(atlas, f, sort_keys=True, indent=2, ensure_ascii=False)
    sz = os.path.getsize(OUTPUT_JSON)
    print(f"  Done. {len(all_points)} total points; atlas-refit-candidate-1.json = {sz/1e6:.2f} MB")

    # slim coordinates CSV for diffing (kit_id, x, y, game, gateA_group, supplementary)
    con = sqlite3.connect(CORPUS_DB)
    kit_game = dict(con.execute(
        "SELECT k.kit_id, c.game FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND k.cell_key IS NOT NULL").fetchall())
    con.close()
    with open(COORD_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kit_id", "x", "y", "game", "gateA_group", "supplementary"])
        for p in all_points:
            w.writerow([p["kit_id"], p["x"], p["y"], kit_game.get(p["kit_id"], ""),
                        p.get("gateA_group", "") or "", int(bool(p["supplementary"]))])
    print(f"  Slim coordinates CSV: {COORD_CSV}")
    return atlas


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"EMITTER FAILED (loud): {e}", file=sys.stderr)
        sys.exit(1)
