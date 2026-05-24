#!/usr/bin/env python3
"""
Cycle 10 Stage 1.5 — Half A: structured-field extractor (length / weight /
materials / provenance / historical-use).

Independent of gandalf seed list; bearer extraction lives in 03_extract_named_bearer.py.

Per-source branch logic per per-source-schema-mapping.md §1.

Idempotent: re-running overwrites the 6 columns this script owns (does NOT
touch extracted_named_bearer).

Discipline #2 + #2.1: pre-execution smoke recommended via --limit N flag for
50-row dry-run before full population.

Discipline #19: this script is foreground for the dispatch wall-time budget
(~5-10 min) but can be invoked via nohup if preferred.

Usage:
  python 02_extract_structured_fields.py --limit 50      # smoke
  python 02_extract_structured_fields.py                  # full
  python 02_extract_structured_fields.py --source met-museum
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Regex library
# ---------------------------------------------------------------------------

# Met-museum dimensions: prefer the metric form in parens "(54.5 cm)" / "(2750 g)"
RE_MET_LENGTH = re.compile(
    r"\bL\.?\s*[\d\s./]+(?:in\.?\s*)?\(\s*(\d+(?:\.\d+)?)\s*(cm|mm|m)\s*\)",
    re.IGNORECASE,
)
RE_MET_LENGTH_NO_PAREN = re.compile(
    r"\bL\.?\s*(\d+(?:\.\d+)?)\s*(in|cm|mm|m)\b",
    re.IGNORECASE,
)
RE_MET_WEIGHT = re.compile(
    r"\bWt\.?\s*[\d\s./lboz]+\(\s*(\d+(?:\.\d+)?)\s*(g|kg)\s*\)",
    re.IGNORECASE,
)
RE_MET_WEIGHT_LB = re.compile(
    r"\bWt\.?\s*(\d+(?:\.\d+)?)\s*(lb|oz|kg|g)\b",
    re.IGNORECASE,
)

# Wikipedia infobox: messy with wiki-cruft. Strip HTML/refs, then extract
# first plausible "X.X cm" / "X.X kg" / "X mm" / "X g".
RE_WIKI_NUM_UNIT_LEN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(mm|cm|m|in|inch|inches|ft|feet)\b",
    re.IGNORECASE,
)
RE_WIKI_NUM_UNIT_WT = re.compile(
    r"(\d+(?:\.\d+)?)\s*(g|kg|lb|lbs|oz)\b",
    re.IGNORECASE,
)
RE_WIKI_CRUFT = re.compile(r"<[^>]+>|\{[^}]*\}|\[\[|\]\]")

# Generic "573 mg" / "1.2 kg" / "100 ml" extractor
RE_CDDA_WEIGHT = re.compile(
    r"^([\d.]+)\s*(mg|g|kg|lb|lbs|oz)$",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Unit normalization (canonical: cm for length, g for weight)
# ---------------------------------------------------------------------------

LENGTH_TO_CM = {
    "mm": 0.1,
    "cm": 1.0,
    "m": 100.0,
    "in": 2.54,
    "inch": 2.54,
    "inches": 2.54,
    "ft": 30.48,
    "feet": 30.48,
}
WEIGHT_TO_G = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "lb": 453.59237,
    "lbs": 453.59237,
    "oz": 28.349523125,
}


def normalize_length(value: float, unit: str) -> tuple[float | None, str]:
    unit_l = unit.lower()
    if unit_l not in LENGTH_TO_CM:
        return None, unit
    return value * LENGTH_TO_CM[unit_l], unit_l


def normalize_weight(value: float, unit: str) -> tuple[float | None, str]:
    unit_l = unit.lower()
    if unit_l not in WEIGHT_TO_G:
        return None, unit
    return value * WEIGHT_TO_G[unit_l], unit_l


# ---------------------------------------------------------------------------
# Per-source extractors
# ---------------------------------------------------------------------------


def extract_met_museum(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    dims = props.get("dimensions", "") or ""
    # Length
    m = RE_MET_LENGTH.search(dims)
    if m:
        v, u = normalize_length(float(m.group(1)), m.group(2))
        if v is not None:
            out["length_value"] = round(v, 2)
            out["length_unit"] = m.group(2).lower()
    else:
        m2 = RE_MET_LENGTH_NO_PAREN.search(dims)
        if m2:
            v, u = normalize_length(float(m2.group(1)), m2.group(2))
            if v is not None:
                out["length_value"] = round(v, 2)
                out["length_unit"] = m2.group(2).lower()
    # Weight
    m = RE_MET_WEIGHT.search(dims)
    if m:
        v, u = normalize_weight(float(m.group(1)), m.group(2))
        if v is not None:
            out["weight_value"] = round(v, 2)
            out["weight_unit"] = m.group(2).lower()
    else:
        m2 = RE_MET_WEIGHT_LB.search(dims)
        if m2:
            v, u = normalize_weight(float(m2.group(1)), m2.group(2))
            if v is not None:
                out["weight_value"] = round(v, 2)
                out["weight_unit"] = m2.group(2).lower()
    # Materials
    medium = props.get("medium", "") or ""
    if medium.strip():
        out["materials"] = medium.strip()
    # Provenance richness
    sig_fields = ("culture", "country", "period", "objectDate", "creditLine", "accessionNumber")
    populated = sum(1 for f in sig_fields if (props.get(f) or "").strip())
    out["provenance_richness"] = round(populated / len(sig_fields), 3)
    # Historical use
    od = props.get("objectDate", "") or ""
    cl = props.get("creditLine", "") or ""
    parts = [s for s in [od.strip(), cl.strip()] if s]
    if parts:
        out["historical_use"] = "; ".join(parts)[:500]
    return out


def extract_wikipedia(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    # Length
    raw_len = props.get("length", "") or ""
    clean_len = RE_WIKI_CRUFT.sub(" ", raw_len)
    m = RE_WIKI_NUM_UNIT_LEN.search(clean_len)
    if m:
        v, _ = normalize_length(float(m.group(1)), m.group(2))
        if v is not None:
            out["length_value"] = round(v, 2)
            out["length_unit"] = m.group(2).lower()
    # Weight
    raw_wt = props.get("weight", "") or ""
    clean_wt = RE_WIKI_CRUFT.sub(" ", raw_wt)
    m = RE_WIKI_NUM_UNIT_WT.search(clean_wt)
    if m:
        v, _ = normalize_weight(float(m.group(1)), m.group(2))
        if v is not None:
            out["weight_value"] = round(v, 2)
            out["weight_unit"] = m.group(2).lower()
    # Materials: not infobox-keyed in wikipedia for weapons (typically); leave NULL
    # Provenance richness: origin + manufacturer + used_by + wars
    sig_fields = ("origin", "manufacturer", "used_by", "wars")
    populated = sum(1 for f in sig_fields if (props.get(f) or "").strip())
    out["provenance_richness"] = round(populated / len(sig_fields), 3)
    # Historical use
    wars = props.get("wars", "") or ""
    if wars.strip():
        clean_wars = RE_WIKI_CRUFT.sub(" ", wars).strip()
        out["historical_use"] = clean_wars[:500]
    return out


def extract_wikidata(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    mat = props.get("material", "") or ""
    if isinstance(mat, list):
        mat = ", ".join(str(x) for x in mat if x)
    if mat and isinstance(mat, str) and mat.strip():
        out["materials"] = mat.strip()
    sig_fields = ("country", "inception", "weapon_type", "material")
    populated = sum(1 for f in sig_fields if str(props.get(f) or "").strip())
    out["provenance_richness"] = round(populated / len(sig_fields), 3)
    return out


def extract_odin_army_tradoc(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    inner = props.get("properties", {}) or {}
    # Length
    for key in (
        "Dimensions.Length",
        "Dimensions.Length ",
        "Dimensions.Overall Length",
    ):
        v = inner.get(key)
        if not v or str(v).strip().upper() == "INA":
            continue
        m = RE_WIKI_NUM_UNIT_LEN.search(str(v))
        if m:
            vv, _ = normalize_length(float(m.group(1)), m.group(2))
            if vv is not None:
                out["length_value"] = round(vv, 2)
                out["length_unit"] = m.group(2).lower()
                break
    # Weight
    for key in (
        "Dimensions.Weight",
        "Dimensions.Weight ",
        "Dimensions.Maximum Takeoff Weight",
        "Dimensions.Combat Weight",
    ):
        v = inner.get(key)
        if not v or str(v).strip().upper() == "INA":
            continue
        m = RE_WIKI_NUM_UNIT_WT.search(str(v))
        if m:
            vv, _ = normalize_weight(float(m.group(1)), m.group(2))
            if vv is not None:
                out["weight_value"] = round(vv, 2)
                out["weight_unit"] = m.group(2).lower()
                break
    sig_keys = (
        "System.Manufacturer",
        "System.Type",
        "System.Caliber",
        "System.Alternate Designation",
    )
    populated = sum(1 for k in sig_keys if str(inner.get(k) or "").strip() and str(inner.get(k) or "").upper() != "INA")
    out["provenance_richness"] = round(populated / len(sig_keys), 3)
    # Historical use: any Variants.* keys
    variant_keys = [k for k in inner.keys() if k.startswith("Variants.")]
    if variant_keys:
        parts = [f"{k.split('.', 1)[1]}: {str(inner[k])[:120]}" for k in variant_keys[:3]]
        out["historical_use"] = "; ".join(parts)[:500]
    return out


def extract_royal_armouries(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    sig_fields = ("place", "date", "accession_number", "location_in_museum")
    populated = sum(1 for f in sig_fields if str(props.get(f) or "").strip())
    out["provenance_richness"] = round(populated / len(sig_fields), 3)
    return out


def extract_osrsbox(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    w = props.get("weight")
    if isinstance(w, (int, float)):
        out["weight_value"] = float(w)
        out["weight_unit"] = "g_game"
    sig_fields = ("members", "tradeable", "weapon_type")
    populated = sum(1 for f in sig_fields if props.get(f) is not None)
    out["provenance_richness"] = round(populated / len(sig_fields), 3) * 0.3  # cap at 0.3 — game-data not historically-provenant
    return out


def extract_cataclysm_dda(props: dict) -> dict:
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    w = props.get("weight", "") or ""
    m = RE_CDDA_WEIGHT.match(str(w).strip())
    if m:
        v, _ = normalize_weight(float(m.group(1)), m.group(2))
        if v is not None:
            out["weight_value"] = round(v, 4)
            out["weight_unit"] = m.group(2).lower()
    mat = props.get("material")
    if isinstance(mat, list):
        materials_str = ", ".join(str(x) for x in mat if x)
        if materials_str:
            out["materials"] = materials_str
    elif isinstance(mat, str) and mat.strip():
        out["materials"] = mat.strip()
    sig_fields = ("subtypes", "material", "ammo_type")
    populated = sum(1 for f in sig_fields if props.get(f) is not None)
    out["provenance_richness"] = round(populated / len(sig_fields), 3) * 0.3
    return out


def extract_generic_thin(props: dict) -> dict:
    """Default extractor for thin sources: provenance only, low score."""
    out = {
        "length_value": None,
        "length_unit": None,
        "weight_value": None,
        "weight_unit": None,
        "materials": None,
        "provenance_richness": 0.0,
        "historical_use": None,
    }
    if props:
        # Score = number of non-empty keys / 10 (capped at 0.3)
        populated = sum(1 for v in props.values() if (v if isinstance(v, (int, float)) else str(v or "").strip()))
        out["provenance_richness"] = round(min(populated / 10.0, 0.3), 3)
    return out


SOURCE_EXTRACTORS = {
    "met-museum": extract_met_museum,
    "wikipedia": extract_wikipedia,
    "wikidata": extract_wikidata,
    "odin-army-tradoc": extract_odin_army_tradoc,
    "royal_armouries": extract_royal_armouries,
    "osrsbox-db": extract_osrsbox,
    "cataclysm-dda": extract_cataclysm_dda,
}


def extractor_for(source: str):
    return SOURCE_EXTRACTORS.get(source, extract_generic_thin)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Process only N rows (smoke).")
    parser.add_argument("--source", type=str, default=None, help="Filter to one source_library.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to DB.")
    args = parser.parse_args()

    started = time.time()
    log_name = "02_extract_structured_fields"
    if args.limit:
        log_name += f"_smoke_{args.limit}"
    if args.source:
        log_name += f"_{args.source}"
    if args.dry_run:
        log_name += "_dryrun"
    log_path = LOG_DIR / f"{log_name}.json"

    log = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "args": vars(args),
        "rows_scanned": 0,
        "rows_written": 0,
        "per_source": {},
        "errors": [],
        "first_5_examples": [],
    }

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        query = (
            "SELECT id, canonical_name, source_library, structured_properties "
            "FROM weapon_knowledge_entries"
        )
        params: list = []
        if args.source:
            query += " WHERE source_library = ?"
            params.append(args.source)
        if args.limit:
            query += " LIMIT ?"
            params.append(args.limit)
        cur = conn.execute(query, params)
        updates: list = []
        for row in cur:
            log["rows_scanned"] += 1
            try:
                props = json.loads(row["structured_properties"] or "{}")
            except (json.JSONDecodeError, TypeError):
                props = {}
            ex = extractor_for(row["source_library"])
            result = ex(props)
            src_stats = log["per_source"].setdefault(
                row["source_library"],
                {
                    "scanned": 0,
                    "length_pop": 0,
                    "weight_pop": 0,
                    "materials_pop": 0,
                    "provenance_avg_sum": 0.0,
                    "historical_use_pop": 0,
                },
            )
            src_stats["scanned"] += 1
            if result["length_value"] is not None:
                src_stats["length_pop"] += 1
            if result["weight_value"] is not None:
                src_stats["weight_pop"] += 1
            if result["materials"]:
                src_stats["materials_pop"] += 1
            if result["historical_use"]:
                src_stats["historical_use_pop"] += 1
            src_stats["provenance_avg_sum"] += result["provenance_richness"]

            if len(log["first_5_examples"]) < 5 and result["length_value"]:
                log["first_5_examples"].append(
                    {
                        "id": row["id"],
                        "canonical_name": row["canonical_name"],
                        "source_library": row["source_library"],
                        "extracted": result,
                    }
                )
            updates.append(
                (
                    result["length_value"],
                    result["length_unit"],
                    result["weight_value"],
                    result["weight_unit"],
                    result["materials"],
                    result["provenance_richness"],
                    result["historical_use"],
                    row["id"],
                )
            )

        if not args.dry_run:
            conn.executemany(
                "UPDATE weapon_knowledge_entries SET "
                "  extracted_length_value = ?, "
                "  extracted_length_unit = ?, "
                "  extracted_weight_value = ?, "
                "  extracted_weight_unit = ?, "
                "  extracted_materials = ?, "
                "  extracted_provenance_richness = ?, "
                "  extracted_historical_use = ? "
                "WHERE id = ?",
                updates,
            )
            conn.commit()
            log["rows_written"] = len(updates)

        # Finalize per-source provenance avg
        for src, stats in log["per_source"].items():
            n = max(stats["scanned"], 1)
            stats["provenance_richness_avg"] = round(stats["provenance_avg_sum"] / n, 3)
            stats["length_coverage_pct"] = round(100.0 * stats["length_pop"] / n, 1)
            stats["weight_coverage_pct"] = round(100.0 * stats["weight_pop"] / n, 1)
            stats["materials_coverage_pct"] = round(100.0 * stats["materials_pop"] / n, 1)
            stats["historical_use_coverage_pct"] = round(100.0 * stats["historical_use_pop"] / n, 1)
            del stats["provenance_avg_sum"]

    finally:
        conn.close()

    log["elapsed_sec"] = round(time.time() - started, 2)
    log["status"] = "ok" if not log["errors"] else "partial"
    log_path.write_text(json.dumps(log, indent=2))
    # Print compact summary to stdout
    summary = {
        "status": log["status"],
        "rows_scanned": log["rows_scanned"],
        "rows_written": log["rows_written"],
        "elapsed_sec": log["elapsed_sec"],
        "per_source_coverage": {
            src: {
                "n": stats["scanned"],
                "len%": stats["length_coverage_pct"],
                "wt%": stats["weight_coverage_pct"],
                "mat%": stats["materials_coverage_pct"],
                "prov_avg": stats["provenance_richness_avg"],
            }
            for src, stats in log["per_source"].items()
        },
    }
    print(json.dumps(summary, indent=2))
    return 0 if log["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
