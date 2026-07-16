"""
build_atlas_json_edition3.py — Deterministic emitter for atlas.json EDITION III.

Edition III = census population (register v1.3): the Edition-III one-batch curated +65 corpus rows
(Stage A pull-7 re-insertion + Stage B Lost Ark 58). The LATTICE is UNCHANGED (v1.3 denominators
byte-identical to v1.2); the FIT layer is BYTE-FROZEN vs Edition-I (r6): the 14-dim basis, all 506
point coordinates, tombstones, axis names, RIDER-1, F-1 — untouched. Only the LATTICE-LAYER lit
occupancy re-emits (against the larger census).

FROZEN-BASIS GATE (charter §6): new rows PROJECT into the frozen Edition-I basis via supplementary
projection — NO basis re-derivation at an edition increment. This emitter reads the SAME frozen
basis CSVs as Edition-I/II (atlas-coordinates-active.csv, atlas-coordinates-supplementary.csv,
atlas-loadings.csv) — never regenerates them — and calls ghost_field_edition3 for the lattice.

Output: atlas-edition3.json, emitted ALONGSIDE atlas-edition2.json (never over). Edition-II stays
the served truth until Matt's Edition-III freeze ratification + re-vendor.

Provenance: elrond (data steward). Commission: gandalf Edition-III one-batch §4.

Fail-loud rules (Edition-III commission §4 + §5; Edition-II acceptance pattern carried forward):
  - Active point count != 469 -> raise (fit-layer regression guard)
  - basis block must be byte-identical to Edition-I (asserted against atlas.json)
  - all 506 point coords + tombstones byte-identical to Edition-I -> else raise (acceptance 23)
  - depth_sum_check != exact denominator 767,411,820 -> raise (acceptance 24)
  - any pull-lit cell not traceable to an intrinsic-evidence kit -> raise (acceptance 25)
  - ANY mcd-lit pull cell -> raise (acceptance 25)
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
import ghost_field_edition3 as ghost_field_mod

CORPUS_DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"

ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
ACTIVE_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-active.csv")
SUPPLEMENTARY_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-supplementary.csv")
LOADINGS_CSV = os.path.join(ATLAS_DIR, "atlas-loadings.csv")
EDITION1_JSON = os.path.join(ATLAS_DIR, "atlas.json")            # frozen Edition-I (basis source-of-truth)
EDITION2_JSON = os.path.join(ATLAS_DIR, "atlas-edition2.json")   # preserved Edition-II (never overwritten)
OUTPUT_JSON = os.path.join(ATLAS_DIR, "atlas-edition3.json")

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

# Edition-III stamp
EDITION = 3
EDITION_LABEL = "Edition-III"
REGISTER_V1_3_REF = "feasibility-cuts-register-v1.3"

EXPECTED_ACTIVE_COUNT = 469
DIM_COUNT = 14
FLOAT_FORMAT = ".8g"
BADGE_FIELDS_MANDATORY = ["inertia_pct", "retained_dims", "structure_statement"]
NULL_DEATH_CLASS_SENTINEL = "unknown-pending-recrawl"
EXACT_DENOMINATOR = 767411820   # register v1.3 — byte-identical to Edition-II (lattice unchanged)

# ---- Edition-III intrinsic-pull kit set (acceptance 25) ----
# EVERY kit carrying ctrl_function=pull in the post-batch census must be an intrinsic-evidence kit
# (skill/rune/talent/class-engraving level — never gear-assembled, never mcd). The 10 pull-function
# kits after the Edition-III batch: the 2 Edition-II Stage-3 re-keys (d3-zbarb rune,
# di-cyclone-monk-pvp base-skill) + the 5 pull-tranche pull rows (Vortex Gravity / Gravity Impact /
# Gravity Force skill-grain + d4-spiritborn-vortex class-tree + d3-wizard-black-hole class-skill +
# di-cyclone-strike-monk-base) + the 2 Destroyer class-engraving pull carriers (rage-hammer,
# gravity-training). ALL intrinsic. ZERO mcd-lit permitted.
INTRINSIC_PULL_KITS = {
    "d3-zbarb", "di-cyclone-monk-pvp",                       # Edition-II Stage-3 re-keys
    "la-destroyer-vortex-gravity", "la-destroyer-gravity-impact", "la-destroyer-gravity-force",
    "d4-spiritborn-vortex", "d3-wizard-black-hole", "di-cyclone-strike-monk-base",  # pull-tranche
    "la-destroyer-rage-hammer", "la-destroyer-gravity-training",  # Destroyer engraving-grain carriers
}


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
    strings byte-identical to Edition-I's atlas.json. Fail loud on ANY drift. (The +65 Edition-III
    census rows do NOT enter the FIT points — they are corpus rows projected into the frozen basis
    as ghost lighting, NOT active fit points. The 506-point fit set is Edition-I-frozen forever.)"""
    with open(EDITION1_JSON) as f:
        e1 = json.load(f)
    if basis != e1["basis"]:
        raise ValueError(f"FIT-LAYER REGRESSION: basis block differs from Edition-I.\n"
                         f"  E1: {e1['basis']}\n  E3: {basis}")
    e1_pts = {p["kit_id"]: p for p in e1["points"]}
    e3_pts = {p["kit_id"]: p for p in all_points}
    if set(e1_pts) != set(e3_pts):
        raise ValueError("FIT-LAYER REGRESSION: point kit_id set differs from Edition-I.")
    for kid in e1_pts:
        a, b = e1_pts[kid], e3_pts[kid]
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


def _assert_edition2_preserved():
    """Edition-III must NOT overwrite Edition-II. Assert atlas-edition2.json still exists and is
    an Edition-II artifact (served truth until Matt ratifies Edition-III)."""
    if not os.path.exists(EDITION2_JSON):
        raise ValueError("atlas-edition2.json MISSING — Edition-II must stay the served truth.")
    with open(EDITION2_JSON) as f:
        e2 = json.load(f)
    if e2.get("edition") != 2 or e2.get("atlas_version") != "Edition-II":
        raise ValueError("atlas-edition2.json is not an Edition-II artifact — refusing to proceed.")
    print("  [alongside] atlas-edition2.json preserved as Edition-II (served truth) OK")


def _assert_pull_slice_integrity(ghost, db_conn):
    """Acceptance 25 (pull-slice-lit-integrity): every kit carrying ctrl_function=pull traces to an
    intrinsic-evidence kit; ZERO mcd-lit cells."""
    rows = db_conn.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL"
    ).fetchall()
    pull_kits = []
    mcd_pull = []
    for kid, ck in rows:
        if ck.split("|")[ghost_field_mod.CK_IDX["function"]] == "pull":
            pull_kits.append(kid)
            if kid.startswith("mcd-"):
                mcd_pull.append(kid)
    non_intrinsic = set(pull_kits) - INTRINSIC_PULL_KITS
    if non_intrinsic:
        raise ValueError(f"PULL-SLICE INTEGRITY FAIL: pull kits not in intrinsic-evidence set: "
                         f"{sorted(non_intrinsic)}")
    if mcd_pull:
        raise ValueError(f"PULL-SLICE INTEGRITY FAIL: mcd- kits carry pull (must be ZERO): "
                         f"{sorted(mcd_pull)}")
    print(f"  [acceptance 25] pull-slice integrity: {len(pull_kits)} pull kits, all intrinsic-"
          f"evidence; ZERO mcd-lit OK")


def build():
    print(f"[edition3] Reading FROZEN active coordinates: {ACTIVE_CSV}")
    active_points = _read_active(ACTIVE_CSV)
    _validate_active_count(active_points)
    print(f"  Active points: {len(active_points)} (OK)")

    supplementary_points, null_dc = _read_supplementary(SUPPLEMENTARY_CSV)
    print(f"  Supplementary points: {len(supplementary_points)} (null death_class: {null_dc})")
    loadings = _read_loadings(LOADINGS_CSV)

    basis = {
        "edition": 1,   # the BASIS is Edition-I (frozen); Edition-III does not re-fit the basis.
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
    # --- alongside guard: Edition-II preserved ---
    _assert_edition2_preserved()

    # --- LATTICE layer: Edition-III ghost field (v1.3 census; lattice unchanged) ---
    print("[edition3] Building Edition-III ghost_field (register v1.3; census population)...")
    _con = sqlite3.connect(CORPUS_DB)
    ghost_field = ghost_field_mod.build_ghost_field(_con, atlas_points=all_points)
    if ghost_field["depth_sum_check"] != EXACT_DENOMINATOR:
        raise ValueError(f"[acceptance 24] depth_sum {ghost_field['depth_sum_check']} != exact "
                         f"denominator {EXACT_DENOMINATOR}.")
    print(f"  [acceptance 24] lattice-integrity: depth_sum == {EXACT_DENOMINATOR} (unchanged) OK")
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
        "register_ref": REGISTER_V1_3_REF,
        "badge_fields_mandatory": BADGE_FIELDS_MANDATORY,
        "emitted_at": emitted_at,
        "emitter_script": "agentic_orchestration/research/scripts/build_atlas_json_edition3.py",
        "fit_layer_frozen_vs": "Edition-I (atlas.json) — basis + 506 point coords + tombstones byte-identical",
        "emitted_alongside": "atlas-edition2.json (Edition-II stays served truth until Matt ratifies Edition-III freeze)",
        "basis": basis,
        "loadings": loadings,
        "counts": {"active": len(active_points), "supplementary": len(supplementary_points),
                   "total": len(all_points), "null_death_class_sentineled": null_dc},
        "points": all_points,
        "ghost_field": ghost_field,
        "p_df_1_verdict": ghost_field["p_df_1"]["verdict"],
    }

    print(f"[edition3] Writing output ALONGSIDE Edition-II: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(atlas, f, sort_keys=True, indent=2, ensure_ascii=False)
    sz = os.path.getsize(OUTPUT_JSON)
    print(f"  Done. {len(all_points)} total points; atlas-edition3.json = {sz/1e6:.2f} MB")
    return atlas


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"EMITTER FAILED (loud): {e}", file=sys.stderr)
        sys.exit(1)
