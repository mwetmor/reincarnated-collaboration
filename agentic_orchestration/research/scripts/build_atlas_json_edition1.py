"""
build_atlas_json_edition1.py — Deterministic emitter for atlas.json Edition I.

Frozen basis: MCA with Greenacre-corrected inertia, parallel-analysis retention
of 14 dims, seed 20260714, prereg v1.1. Ratified 2026-07-14 by Matt ("Ratify a").
Axis names: dim1 PERFORM <-> DEPLOY · dim2 EMBODY <-> LAUNCH.

Source CSVs (collab-side):
  agentic_orchestration/research/curated/atlas/atlas-coordinates-active.csv
  agentic_orchestration/research/curated/atlas/atlas-coordinates-supplementary.csv
  agentic_orchestration/research/curated/atlas/atlas-loadings.csv

Output:
  agentic_orchestration/research/curated/atlas/atlas.json

Fail-loud rules (per task contract + Discipline #8):
  - Any NaN coordinate -> raise
  - Active point count != 469 -> raise
  - Any supplementary row missing death_class -> emit with "unknown-pending-recrawl"
    (census gap, not a hard fail — per task contract)
  - Any mandatory badge field missing/empty -> raise
  - Points sorted by kit_id for byte-stable output
  - json.dump with sort_keys=True, fixed float format (6 decimal places)
"""

import csv
import json
import math
import os
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths (absolute, collab-repo relative to this script's location)
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.join(SCRIPT_DIR, "..", "curated", "atlas")
ATLAS_DIR = os.path.normpath(ATLAS_DIR)

ACTIVE_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-active.csv")
SUPPLEMENTARY_CSV = os.path.join(ATLAS_DIR, "atlas-coordinates-supplementary.csv")
LOADINGS_CSV = os.path.join(ATLAS_DIR, "atlas-loadings.csv")
OUTPUT_JSON = os.path.join(ATLAS_DIR, "atlas.json")

# ---------------------------------------------------------------------------
# Frozen basis constants (Edition I — DO NOT change without a numbered Edition bump)
# ---------------------------------------------------------------------------

EDITION = 1
FROZEN = True
RATIFIED = "2026-07-14"
METHOD = (
    "MCA with Greenacre-corrected inertia, MFA block-weighted; "
    "parallel-analysis retention of 14 dims (95th-pct null threshold); "
    "seed 20260714; prereg v1.1"
)
LOADINGS_REF = "atlas-loadings.csv"
INERTIA_PCT = 8.36          # sum of retained dim %-inertia from gate report (4.55+3.81 top 2; full 14-dim)
RETAINED_DIMS = 14
STRUCTURE_STATEMENT = "continuum with condensations, not discrete cells"
AXIS_NAMES = {
    "dim1": "PERFORM <-> DEPLOY",
    "dim2": "EMBODY <-> LAUNCH",
}

EXPECTED_ACTIVE_COUNT = 469
DIM_COUNT = 14
FLOAT_FORMAT = ".8g"   # enough precision; no trailing noise; deterministic via Python's float repr

# Badge fields mandatory (RIDER-1 — renderers must enforce)
BADGE_FIELDS_MANDATORY = ["inertia_pct", "retained_dims", "structure_statement"]

NULL_DEATH_CLASS_SENTINEL = "unknown-pending-recrawl"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fmt(v):
    """Format a float consistently for JSON output."""
    return float(format(v, FLOAT_FORMAT))


def _check_nan(val, context):
    if math.isnan(val) or math.isinf(val):
        raise ValueError(f"NaN/Inf coordinate detected: {context}")


def _read_active(path):
    """Read active kit coordinates. Returns list of point dicts, sorted by kit_id."""
    points = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kit_id = row["kit_id"].strip()
            if not kit_id:
                raise ValueError("Empty kit_id in active CSV")

            coords = {}
            for d in range(1, DIM_COUNT + 1):
                key = f"dim{d}"
                raw = row.get(key, "").strip()
                if raw == "" or raw is None:
                    raise ValueError(f"Missing dim{d} for kit {kit_id}")
                val = float(raw)
                _check_nan(val, f"{kit_id} dim{d}")
                coords[key] = _fmt(val)

            # gateA_group: empty string -> None
            gate_a = row.get("gateA_group", "").strip()
            gate_a = gate_a if gate_a else None

            # franchise: use franchise_rollup column
            franchise = row.get("franchise_rollup", "").strip()
            franchise = franchise if franchise else None

            points.append({
                "kit_id": kit_id,
                "x": coords["dim1"],
                "y": coords["dim2"],
                "dims": coords,
                "supplementary": False,
                "gateA_group": gate_a,
                "franchise": franchise,
            })

    # Sort by kit_id for byte-stable output
    points.sort(key=lambda p: p["kit_id"])
    return points


def _read_supplementary(path):
    """Read supplementary (corpse) coordinates. Returns list of point dicts, sorted by kit_id."""
    points = []
    null_death_class_count = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kit_id = row["kit_id"].strip()
            if not kit_id:
                raise ValueError("Empty kit_id in supplementary CSV")

            coords = {}
            for d in range(1, DIM_COUNT + 1):
                key = f"dim{d}"
                raw = row.get(key, "").strip()
                if raw == "" or raw is None:
                    raise ValueError(f"Missing dim{d} for supplementary kit {kit_id}")
                val = float(raw)
                _check_nan(val, f"{kit_id} dim{d}")
                coords[key] = _fmt(val)

            death_class = row.get("death_class", "").strip()
            if not death_class:
                # Known census gap -> sentinel rather than hard fail (per task contract)
                death_class = NULL_DEATH_CLASS_SENTINEL
                null_death_class_count += 1

            points.append({
                "kit_id": kit_id,
                "x": coords["dim1"],
                "y": coords["dim2"],
                "dims": coords,
                "supplementary": True,
                "death_class": death_class,
            })

    points.sort(key=lambda p: p["kit_id"])
    return points, null_death_class_count


def _read_loadings(path):
    """Read loadings CSV. Returns list of loading records."""
    loadings = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            loadings.append({
                "dim": int(row["dim"]),
                "rank": int(row["rank"]),
                "coordinate": row["coordinate"].strip(),
                "level": row["level"].strip(),
                "loading": _fmt(float(row["loading"])),
                "abs_loading": _fmt(float(row["abs_loading"])),
            })
    # Sort deterministically
    loadings.sort(key=lambda r: (r["dim"], r["rank"]))
    return loadings


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _validate_basis(basis):
    """Fail loud if any mandatory badge field is missing or empty."""
    for field in BADGE_FIELDS_MANDATORY:
        val = basis.get(field)
        if val is None or val == "" or val == []:
            raise ValueError(
                f"MANDATORY badge field '{field}' is missing or empty in basis block. "
                f"Emitter halted per RIDER-1."
            )


def _validate_active_count(points):
    n = len(points)
    if n != EXPECTED_ACTIVE_COUNT:
        raise ValueError(
            f"Active point count mismatch: expected {EXPECTED_ACTIVE_COUNT}, got {n}. "
            f"Emitter halted — do not emit a broken artifact."
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def build():
    print(f"[build_atlas_json_edition1] Reading active coordinates: {ACTIVE_CSV}")
    active_points = _read_active(ACTIVE_CSV)
    _validate_active_count(active_points)
    print(f"  Active points: {len(active_points)} (OK)")

    print(f"[build_atlas_json_edition1] Reading supplementary coordinates: {SUPPLEMENTARY_CSV}")
    supplementary_points, null_dc = _read_supplementary(SUPPLEMENTARY_CSV)
    print(f"  Supplementary points: {len(supplementary_points)}")
    if null_dc:
        print(
            f"  WARNING: {null_dc} supplementary row(s) had NULL death_class -> "
            f"emitted as '{NULL_DEATH_CLASS_SENTINEL}' (known census gap, Edition II)"
        )

    print(f"[build_atlas_json_edition1] Reading loadings: {LOADINGS_CSV}")
    loadings = _read_loadings(LOADINGS_CSV)
    print(f"  Loadings rows: {len(loadings)}")

    # Build basis block
    basis = {
        "edition": EDITION,
        "frozen": FROZEN,
        "ratified": RATIFIED,
        "method": METHOD,
        "loadings_ref": LOADINGS_REF,
        "inertia_pct": INERTIA_PCT,
        "retained_dims": RETAINED_DIMS,
        "structure_statement": STRUCTURE_STATEMENT,
        "axis_names": AXIS_NAMES,
    }
    _validate_basis(basis)

    # Build points list (active first, then supplementary; both already sorted by kit_id;
    # final merged sort so the overall list is deterministically ordered by kit_id)
    all_points = []
    for p in active_points:
        entry = {
            "kit_id": p["kit_id"],
            "x": p["x"],
            "y": p["y"],
            "supplementary": False,
            "gateA_group": p["gateA_group"],
            "franchise": p["franchise"],
        }
        all_points.append(entry)

    for p in supplementary_points:
        entry = {
            "kit_id": p["kit_id"],
            "x": p["x"],
            "y": p["y"],
            "supplementary": True,
            "death_class": p["death_class"],
        }
        all_points.append(entry)

    # Sort all points by kit_id for byte-stable output
    all_points.sort(key=lambda p: p["kit_id"])

    # Build the atlas.json payload
    emitted_at = datetime.now(timezone.utc).isoformat()
    atlas = {
        "atlas_version": "Edition-I",
        "badge_fields_mandatory": BADGE_FIELDS_MANDATORY,
        "emitted_at": emitted_at,
        "emitter_script": "agentic_orchestration/research/scripts/build_atlas_json_edition1.py",
        "basis": basis,
        "loadings": loadings,
        "counts": {
            "active": len(active_points),
            "supplementary": len(supplementary_points),
            "total": len(all_points),
            "null_death_class_sentineled": null_dc,
        },
        "points": all_points,
    }

    print(f"[build_atlas_json_edition1] Writing output: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(atlas, f, sort_keys=True, indent=2, ensure_ascii=False)
    print(f"  Done. {len(all_points)} total points written.")
    print(
        f"  Active: {len(active_points)} | "
        f"Supplementary: {len(supplementary_points)} | "
        f"Null death_class sentineled: {null_dc}"
    )
    return atlas


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"EMITTER FAILED (loud): {e}", file=sys.stderr)
        sys.exit(1)
