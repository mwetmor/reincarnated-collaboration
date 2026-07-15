"""
build_atlas_json_edition2.py — Deterministic emitter for atlas.json EDITION II.

Edition II = pull vocabulary (register v1.2) + EAST-half geometry×commit drill-in +
lattice re-emission. The FIT layer is BYTE-FROZEN vs Edition-I (r6): the 14-dim basis,
all 506 point coordinates, tombstones, axis names, RIDER-1, F-1 — untouched. Only the
LATTICE layer (ghost glyphs, drill-in, denominators, off-plane disclosure) re-emits.

This emitter reads the SAME frozen basis CSVs as Edition-I (atlas-coordinates-active.csv,
atlas-coordinates-supplementary.csv, atlas-loadings.csv) — never regenerates them — and calls
ghost_field_edition2 for the Edition-II lattice. Output: atlas-edition2.json (Edition-I's
atlas.json is preserved as the archived Edition-I artifact).

Provenance: elrond (data steward) authors the ghost/lattice + this Edition-II builder per the
Edition-II chain (spec §10.4). star-lord owns the renderer; galadriel renders (suite 22-28).

Fail-loud rules (Edition-II §10.6 acceptance 23/24):
  - Active point count != 469 -> raise (fit-layer regression guard)
  - basis block must be byte-identical to Edition-I (asserted against atlas.json)
  - depth_sum_check != new exact denominator -> raise
  - any pull-lit cell not traceable to an intrinsic-evidence kit -> raise (25)
  - ANY mcd-lit cell -> raise (25)
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
import ghost_field_edition2 as ghost_field_mod

CORPUS_DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"

ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
ACTIVE_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-active.csv")
SUPPLEMENTARY_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-supplementary.csv")
LOADINGS_CSV = os.path.join(ATLAS_DIR, "atlas-loadings.csv")
EDITION1_JSON = os.path.join(ATLAS_DIR, "atlas.json")            # frozen Edition-I (basis source-of-truth for the regression guard)
OUTPUT_JSON = os.path.join(ATLAS_DIR, "atlas-edition2.json")

# ---- FROZEN basis constants (Edition I — carried forward UNCHANGED; the FIT layer is frozen) ----
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

# Edition-II stamp
EDITION = 2
EDITION_LABEL = "Edition-II"
REGISTER_V1_2_REF = "feasibility-cuts-register-v1.2"

EXPECTED_ACTIVE_COUNT = 469
DIM_COUNT = 14
FLOAT_FORMAT = ".8g"
BADGE_FIELDS_MANDATORY = ["inertia_pct", "retained_dims", "structure_statement"]
NULL_DEATH_CLASS_SENTINEL = "unknown-pending-recrawl"
NEW_EXACT_DENOMINATOR = 767411820

# The pull-lit cells must trace to intrinsic-evidence kits (acceptance 25). The intrinsic-evidence
# pull kits in the CURRENT census are the two Stage-3 re-keys (d3-zbarb rune, di-cyclone-monk-pvp
# base-skill). ZERO mcd-lit cells permitted.
INTRINSIC_PULL_KITS = {"d3-zbarb", "di-cyclone-monk-pvp"}


def _fmt(v):
    return float(format(v, FLOAT_FORMAT))


def _check_nan(val, context):
    if math.isnan(val) or math.isinf(val):
        raise ValueError(f"NaN/Inf coordinate detected: {context}")


def _read_active(path):
    points = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kit_id = row["kit_id"].strip()
            if not kit_id:
                raise ValueError("Empty kit_id in active CSV")
            coords = {}
            for d in range(1, DIM_COUNT + 1):
                raw = row.get(f"dim{d}", "").strip()
                if not raw:
                    raise ValueError(f"Missing dim{d} for kit {kit_id}")
                val = float(raw)
                _check_nan(val, f"{kit_id} dim{d}")
                coords[f"dim{d}"] = _fmt(val)
            gate_a = row.get("gateA_group", "").strip() or None
            franchise = row.get("franchise_rollup", "").strip() or None
            points.append({"kit_id": kit_id, "x": coords["dim1"], "y": coords["dim2"],
                           "supplementary": False, "gateA_group": gate_a, "franchise": franchise})
    points.sort(key=lambda p: p["kit_id"])
    return points


def _read_supplementary(path):
    points = []
    null_dc = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kit_id = row["kit_id"].strip()
            if not kit_id:
                raise ValueError("Empty kit_id in supplementary CSV")
            coords = {}
            for d in range(1, DIM_COUNT + 1):
                raw = row.get(f"dim{d}", "").strip()
                if not raw:
                    raise ValueError(f"Missing dim{d} for supplementary kit {kit_id}")
                val = float(raw)
                _check_nan(val, f"{kit_id} dim{d}")
                coords[f"dim{d}"] = _fmt(val)
            death_class = row.get("death_class", "").strip() or NULL_DEATH_CLASS_SENTINEL
            if death_class == NULL_DEATH_CLASS_SENTINEL:
                null_dc += 1
            points.append({"kit_id": kit_id, "x": coords["dim1"], "y": coords["dim2"],
                           "supplementary": True, "death_class": death_class})
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


def _validate_basis(basis):
    for field in BADGE_FIELDS_MANDATORY:
        if not basis.get(field):
            raise ValueError(f"MANDATORY badge field '{field}' missing/empty. Halted per RIDER-1.")


def _validate_active_count(points):
    if len(points) != EXPECTED_ACTIVE_COUNT:
        raise ValueError(f"Active count mismatch: expected {EXPECTED_ACTIVE_COUNT}, got {len(points)}.")


def _assert_fit_layer_frozen(basis, all_points):
    """Acceptance 23 (fit-layer-regression): basis + all 506 point coords + tombstone death_class
    strings byte-identical to Edition-I's atlas.json. Fail loud on ANY drift."""
    with open(EDITION1_JSON) as f:
        e1 = json.load(f)
    # basis block byte-identical
    if basis != e1["basis"]:
        raise ValueError(f"FIT-LAYER REGRESSION: basis block differs from Edition-I.\n"
                         f"  E1: {e1['basis']}\n  E2: {basis}")
    # points: same kit_ids, same x/y, same death_class on supplementary
    e1_pts = {p["kit_id"]: p for p in e1["points"]}
    e2_pts = {p["kit_id"]: p for p in all_points}
    if set(e1_pts) != set(e2_pts):
        raise ValueError("FIT-LAYER REGRESSION: point kit_id set differs from Edition-I.")
    for kid in e1_pts:
        a, b = e1_pts[kid], e2_pts[kid]
        if a["x"] != b["x"] or a["y"] != b["y"]:
            raise ValueError(f"FIT-LAYER REGRESSION: point {kid} coord moved "
                             f"({a['x']},{a['y']}) -> ({b['x']},{b['y']}).")
        if a.get("supplementary") != b.get("supplementary"):
            raise ValueError(f"FIT-LAYER REGRESSION: point {kid} supplementary flag changed.")
        if a.get("supplementary") and a.get("death_class") != b.get("death_class"):
            raise ValueError(f"FIT-LAYER REGRESSION: tombstone {kid} death_class changed "
                             f"{a.get('death_class')} -> {b.get('death_class')}.")
    print("  [acceptance 23] FIT-layer regression: basis + 506 point coords + tombstones "
          "byte-identical to Edition-I OK")


def _assert_pull_slice_integrity(ghost, db_conn):
    """Acceptance 25 (pull-slice-lit-integrity): every lit pull cell traces to an intrinsic-
    evidence kit; ZERO mcd-lit cells."""
    # which live kits light a pull cell?
    lit_counts, _, _, lit_pull_cells = ghost_field_mod.lit_map(db_conn)
    # find the kits contributing to each lit pull tuple
    rows = db_conn.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL"
    ).fetchall()
    pull_kits = []
    mcd_lit = []
    for kid, ck in rows:
        f = ck.split("|")
        if f[ghost_field_mod.CK_IDX["function"]] == "pull":
            pull_kits.append(kid)
            if kid.startswith("mcd-"):
                mcd_lit.append(kid)
    # every pull-lit kit must be an intrinsic-evidence kit
    non_intrinsic = set(pull_kits) - INTRINSIC_PULL_KITS
    if non_intrinsic:
        raise ValueError(f"PULL-SLICE INTEGRITY FAIL: pull-lit kits not in intrinsic-evidence set: "
                         f"{sorted(non_intrinsic)}")
    if mcd_lit:
        raise ValueError(f"PULL-SLICE INTEGRITY FAIL: mcd- kits lit a pull cell (must be ZERO): "
                         f"{sorted(mcd_lit)}")
    print(f"  [acceptance 25] pull-slice-lit-integrity: {len(pull_kits)} pull-lit kits, all "
          f"intrinsic-evidence ({sorted(pull_kits)}); ZERO mcd-lit OK")


def build():
    print(f"[edition2] Reading FROZEN active coordinates: {ACTIVE_CSV}")
    active_points = _read_active(ACTIVE_CSV)
    _validate_active_count(active_points)
    print(f"  Active points: {len(active_points)} (OK)")

    supplementary_points, null_dc = _read_supplementary(SUPPLEMENTARY_CSV)
    print(f"  Supplementary points: {len(supplementary_points)} (null death_class: {null_dc})")
    loadings = _read_loadings(LOADINGS_CSV)

    basis = {
        "edition": 1,   # the BASIS is Edition-I (frozen); Edition-II does not re-fit the basis.
        "frozen": FROZEN, "ratified": RATIFIED, "method": METHOD, "loadings_ref": LOADINGS_REF,
        "inertia_pct": INERTIA_PCT, "retained_dims": RETAINED_DIMS,
        "structure_statement": STRUCTURE_STATEMENT, "axis_names": AXIS_NAMES,
    }
    _validate_basis(basis)

    all_points = []
    for p in active_points:
        all_points.append({"kit_id": p["kit_id"], "x": p["x"], "y": p["y"],
                           "supplementary": False, "gateA_group": p["gateA_group"],
                           "franchise": p["franchise"]})
    for p in supplementary_points:
        all_points.append({"kit_id": p["kit_id"], "x": p["x"], "y": p["y"],
                           "supplementary": True, "death_class": p["death_class"]})
    all_points.sort(key=lambda p: p["kit_id"])

    # --- acceptance 23: FIT layer byte-frozen vs Edition-I ---
    _assert_fit_layer_frozen(basis, all_points)

    # --- LATTICE layer: Edition-II ghost field (pull + drill-in + off-plane + P-DF-1) ---
    print("[edition2] Building Edition-II ghost_field (register v1.2 + EAST-half drill-in)...")
    _con = sqlite3.connect(CORPUS_DB)
    ghost_field = ghost_field_mod.build_ghost_field(_con, atlas_points=all_points)
    # acceptance 24: depth_sum == new exact denominator
    if ghost_field["depth_sum_check"] != NEW_EXACT_DENOMINATOR:
        raise ValueError(f"[acceptance 24] depth_sum {ghost_field['depth_sum_check']} != new exact "
                         f"denominator {NEW_EXACT_DENOMINATOR}.")
    print(f"  [acceptance 24] lattice-integrity: depth_sum == {NEW_EXACT_DENOMINATOR} OK")
    # acceptance 25: pull-slice integrity
    _assert_pull_slice_integrity(ghost_field, _con)
    _con.close()

    print(f"  ghost_field: {ghost_field['denominators']['meso_feasible']} feasible + "
          f"{ghost_field['denominators']['meso_sealed']} sealed; {ghost_field['lit_cells']} lit "
          f"({ghost_field['pull_slice']['lit_cells']} pull-lit); "
          f"drill-in {ghost_field['drill_in']['n_sub_feasible']} sub-feasible + "
          f"{ghost_field['drill_in']['n_sub_sealed']} RED-3- sealed; "
          f"off-plane N={ghost_field['off_plane_corpus']['n']}; "
          f"P-DF-1 {ghost_field['p_df_1']['verdict']}")

    emitted_at = datetime.now(timezone.utc).isoformat()
    atlas = {
        "atlas_version": EDITION_LABEL,
        "edition": EDITION,
        "register_ref": REGISTER_V1_2_REF,
        "badge_fields_mandatory": BADGE_FIELDS_MANDATORY,
        "emitted_at": emitted_at,
        "emitter_script": "agentic_orchestration/research/scripts/build_atlas_json_edition2.py",
        "fit_layer_frozen_vs": "Edition-I (atlas.json) — basis + 506 point coords + tombstones byte-identical",
        "basis": basis,
        "loadings": loadings,
        "counts": {"active": len(active_points), "supplementary": len(supplementary_points),
                   "total": len(all_points), "null_death_class_sentineled": null_dc},
        "points": all_points,
        "ghost_field": ghost_field,
        "p_df_1_verdict": ghost_field["p_df_1"]["verdict"],
    }

    print(f"[edition2] Writing output: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(atlas, f, sort_keys=True, indent=2, ensure_ascii=False)
    sz = os.path.getsize(OUTPUT_JSON)
    print(f"  Done. {len(all_points)} total points; atlas-edition2.json = {sz/1e6:.2f} MB")
    return atlas


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"EMITTER FAILED (loud): {e}", file=sys.stderr)
        sys.exit(1)
