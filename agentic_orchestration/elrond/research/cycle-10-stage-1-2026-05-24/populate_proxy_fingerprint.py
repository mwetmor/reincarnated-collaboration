#!/usr/bin/env python3
"""
Cycle 10 Stage 1 — Cheap Proxy Mechanical Fingerprint Population
================================================================

Populates 5 proxy_* columns on weapon_knowledge_entries (69,137 active rows)
via heuristic name-token lookup + structured_properties length/weight extraction.

Bin vocabulary per dispatch + Stage 0 (`v1-bc-target-intent-2026-05-24.md`):
- proxy_range_class:    melee / mid / ranged
- proxy_geometry_class: single / multi-hit / cleave / AoE / scatter / cone
- proxy_tempo_class:    low / medium / high
- proxy_attribute_class: STR / INT / WIS / DEX (NULL where ambiguous)
- proxy_fingerprint_confidence: 0.0-1.0

Owners: elrond (lead) + rocket (token-table collab)
Authority: Cycle 10 dispatch (Matt 2026-05-23) — ADR-006 cost discipline: heuristic, $0 API spend.

Usage:
    python populate_proxy_fingerprint.py [--smoke-test] [--limit N] [--db PATH]

Notes:
- Smoke-test mode runs against 100 random rows; does NOT write the DB unless --commit-smoke given.
- Full mode writes in chunked transactions (10K rows per commit) to avoid lock contention.
- Idempotent: re-runs replace existing proxy_* values.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Optional

DB_PATH_DEFAULT = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOOKUP_PATH_DEFAULT = (
    "/Users/admin/Games/reincarnated-collaboration/"
    "agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/"
    "weapon_form_token_lookup.json"
)

# -----------------------------------------------------------------------------
# Schema management
# -----------------------------------------------------------------------------

PROXY_COLUMNS = [
    ("proxy_range_class", "TEXT"),
    ("proxy_geometry_class", "TEXT"),
    ("proxy_tempo_class", "TEXT"),
    ("proxy_attribute_class", "TEXT"),
    ("proxy_fingerprint_confidence", "REAL"),
]


def ensure_proxy_schema(conn: sqlite3.Connection) -> None:
    """Add proxy_* columns to weapon_knowledge_entries if not present. Additive only."""
    cur = conn.execute("PRAGMA table_info(weapon_knowledge_entries)")
    existing = {row[1] for row in cur.fetchall()}
    added = []
    for col, ctype in PROXY_COLUMNS:
        if col not in existing:
            conn.execute(f"ALTER TABLE weapon_knowledge_entries ADD COLUMN {col} {ctype}")
            added.append(col)
    if added:
        conn.commit()
        print(f"[schema] Added columns: {added}", file=sys.stderr)
    else:
        print("[schema] All proxy_* columns already present", file=sys.stderr)


# -----------------------------------------------------------------------------
# Lookup table loading + token matching
# -----------------------------------------------------------------------------

CONFIDENCE_TIER = {
    "high": 0.85,
    "medium": 0.65,
    "low": 0.45,
}


def load_lookup(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def build_token_index(lookup: dict) -> list[dict]:
    """Build a flat list of tokens sorted by length descending (longest-match-wins).

    Non-weapon tokens (armor / accessory / offhand) flagged for early-exit NULL.
    """
    tokens = lookup["tokens"]
    # Sort by token length descending so 'two handed sword' matches before 'sword'
    return sorted(tokens, key=lambda t: -len(t["token"]))


WORD_BOUNDARY_PRE = re.compile(r"(^|[\W_])")
WORD_BOUNDARY_POST = re.compile(r"($|[\W_])")


def _name_head_segment(name_lower: str) -> str:
    """Return the 'head' of a name: the part before parens and before ' and '/' with '.

    Example: 'Sword (jian) and scabbard' -> 'sword'
             'Knife (Khyber) with Sheath' -> 'knife'
             'Sword Guard (Tsuba)' -> 'sword guard'
    """
    h = name_lower
    # Strip parenthetical / bracketed parts
    h = re.sub(r"\([^)]*\)", " ", h)
    h = re.sub(r"\[[^\]]*\]", " ", h)
    # Cut at ' and ' / ' with ' / ',' (the head is what comes before)
    for sep in [" and ", " with ", ","]:
        idx = h.find(sep)
        if idx != -1:
            h = h[:idx]
    return h.strip()


def find_best_token(name_lower: str, token_index: list[dict]) -> Optional[dict]:
    """Find the best-matching token in name_lower.

    Strategy:
    1. Scan all tokens; collect every match with position + token meta.
    2. If a WEAPON token matches in the name-head segment (before parens / "and" / "with"),
       a weapon wins over any accessory token (a "Sword (jian) and scabbard" IS a sword).
    3. Else if any match is armor/accessory/offhand AND no weapon token is in the head, accessory wins
       (a "Sword Guard (Tsuba)" is an accessory because "guard"/"tsuba" is the head).
    4. Else longest-token + highest-specificity match (longest-match-wins).
    """
    matches: list[dict] = []
    for tok in token_index:
        t = tok["token"].lower()
        pattern = r"(?:^|[\W_])" + re.escape(t) + r"(?:$|[\W_])"
        if re.search(pattern, name_lower):
            matches.append(tok)
    if not matches:
        return None

    head = _name_head_segment(name_lower)
    spec_rank = {"high": 3, "medium": 2, "low": 1}

    # Partition into weapon-tokens (have range) and accessory-tokens (flagged)
    weapon_matches = [m for m in matches if not (m.get("_is_armor") or m.get("_is_accessory") or m.get("_is_offhand"))]
    accessory_matches = [m for m in matches if m.get("_is_armor") or m.get("_is_accessory") or m.get("_is_offhand")]

    # Check if any weapon token is in the head (before parens/and/with)
    def in_head(tok: dict) -> bool:
        t = tok["token"].lower()
        pattern = r"(?:^|[\W_])" + re.escape(t) + r"(?:$|[\W_])"
        return bool(re.search(pattern, head))

    head_weapons = [m for m in weapon_matches if in_head(m)]
    head_accessories = [m for m in accessory_matches if in_head(m)]

    # Decision:
    # 1. If both a weapon AND an accessory match in head, longer-token wins
    #    (e.g., "sword guard" beats "sword" for "Sword Guard (Tsuba)" pattern)
    if head_weapons and head_accessories:
        best_acc = max(head_accessories, key=lambda m: (len(m["token"]), spec_rank.get(m.get("specificity", "low"), 0)))
        best_wpn = max(head_weapons, key=lambda m: (len(m["token"]), spec_rank.get(m.get("specificity", "low"), 0)))
        if len(best_acc["token"]) >= len(best_wpn["token"]):
            return best_acc
        return best_wpn
    # 2. If accessory is in head AND no weapon in head → accessory wins
    if head_accessories:
        head_accessories.sort(key=lambda m: (-len(m["token"]), -spec_rank.get(m.get("specificity", "low"), 0)))
        return head_accessories[0]
    # 3. If weapon is in head → weapon wins (even if accessory also matches outside head)
    if head_weapons:
        head_weapons.sort(key=lambda m: (-len(m["token"]), -spec_rank.get(m.get("specificity", "low"), 0)))
        return head_weapons[0]
    # 4. No tokens in head (rare): fall back to accessory-wins-if-exists, else best weapon match
    if accessory_matches:
        return accessory_matches[0]
    weapon_matches.sort(key=lambda m: (-len(m["token"]), -spec_rank.get(m.get("specificity", "low"), 0)))
    return weapon_matches[0]


# -----------------------------------------------------------------------------
# Length / weight extraction from structured_properties JSON
# -----------------------------------------------------------------------------

# Match length in cm (e.g., "22.2 cm", "L. 8 3/4 in. (22.2 cm)")
LENGTH_CM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*cm\b", re.IGNORECASE)
# Match length in inches
LENGTH_IN_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:in\.|inches|\"|\bin\b)", re.IGNORECASE)
# Match weight in g
WEIGHT_G_RE = re.compile(r"(\d+(?:\.\d+)?)\s*g\b(?!\w)", re.IGNORECASE)
# Match weight in oz
WEIGHT_OZ_RE = re.compile(r"(\d+(?:\.\d+)?)\s*oz\b", re.IGNORECASE)
# Match weight in kg
WEIGHT_KG_RE = re.compile(r"(\d+(?:\.\d+)?)\s*kg\b", re.IGNORECASE)
# Match weight in lb
WEIGHT_LB_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:lb|lbs)\b", re.IGNORECASE)


def extract_length_cm(text: str) -> Optional[float]:
    """Extract a length value in cm from a free-form text blob (e.g., met museum dimensions)."""
    if not text:
        return None
    m = LENGTH_CM_RE.search(text)
    if m:
        return float(m.group(1))
    m = LENGTH_IN_RE.search(text)
    if m:
        return float(m.group(1)) * 2.54
    return None


def extract_weight_kg(text: str) -> Optional[float]:
    """Extract a weight in kg from a free-form text blob."""
    if not text:
        return None
    m = WEIGHT_KG_RE.search(text)
    if m:
        return float(m.group(1))
    m = WEIGHT_LB_RE.search(text)
    if m:
        return float(m.group(1)) * 0.4536
    m = WEIGHT_G_RE.search(text)
    if m:
        return float(m.group(1)) / 1000.0
    m = WEIGHT_OZ_RE.search(text)
    if m:
        return float(m.group(1)) * 0.0283
    return None


def parse_structured_props(raw: Optional[str]) -> tuple[Optional[float], Optional[float]]:
    """Pull length_cm + weight_kg from the structured_properties JSON if present.

    Handles diverse per-source schemas:
    - met-museum: 'dimensions' string with mixed units
    - royal_armouries: various; sometimes 'overall_length'
    - fextralife: 'Wgt' field
    - wikipedia/wikidata: 'mass' / 'length' if infobox-derived
    """
    if not raw:
        return None, None
    try:
        d = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None, None
    if not isinstance(d, dict):
        return None, None

    length_cm: Optional[float] = None
    weight_kg: Optional[float] = None

    # Try known fields first
    for field in ("dimensions", "length", "overall_length", "blade_length", "mass", "weight"):
        v = d.get(field)
        if isinstance(v, str):
            if length_cm is None:
                length_cm = extract_length_cm(v)
            if weight_kg is None:
                weight_kg = extract_weight_kg(v)
        elif isinstance(v, (int, float)) and v > 0:
            # Bare numbers; ambiguous units. Skip — too risky.
            pass

    # Fallback: scan all string values
    if length_cm is None or weight_kg is None:
        for v in d.values():
            if not isinstance(v, str):
                continue
            if length_cm is None:
                length_cm = extract_length_cm(v)
            if weight_kg is None:
                weight_kg = extract_weight_kg(v)
            if length_cm is not None and weight_kg is not None:
                break

    return length_cm, weight_kg


# -----------------------------------------------------------------------------
# Fingerprint derivation per row
# -----------------------------------------------------------------------------

def derive_fingerprint(
    canonical_name: str,
    wieldable_humanoid: str,
    weapon_kind: str,
    structured_properties: Optional[str],
    token_index: list[dict],
    lookup_meta: dict,
) -> dict:
    """Derive 5-tuple proxy fingerprint for a single row.

    Returns dict with keys: range, geometry, tempo, attribute, confidence.
    Any value may be None if ambiguous.
    """
    name_lower = (canonical_name or "").lower()
    length_cm, weight_kg = parse_structured_props(structured_properties)

    # 1. Token match
    matched = find_best_token(name_lower, token_index)

    # 2. Handle non-weapon tokens early (armor, accessories) — leave fingerprint NULL with low confidence
    if matched and (matched.get("_is_armor") or matched.get("_is_accessory") or matched.get("_is_offhand")):
        return {
            "range": None,
            "geometry": None,
            "tempo": None,
            "attribute": None,
            "confidence": 0.10,  # low; correctly identified as non-weapon
        }

    if matched is None:
        # No token match; fall back to wieldable_humanoid for coarse range only
        if wieldable_humanoid == "mount_required":
            return {
                "range": "mid",
                "geometry": "single",
                "tempo": "low",
                "attribute": "STR",
                "confidence": 0.20,
            }
        return {
            "range": None,
            "geometry": None,
            "tempo": None,
            "attribute": None,
            "confidence": 0.05,
        }

    # Base assignment from token
    range_class = matched.get("range")
    geometry_class = matched.get("geometry")
    tempo_class = matched.get("tempo")
    attribute_class = matched.get("attribute")
    specificity = matched.get("specificity", "low")
    base_conf = CONFIDENCE_TIER.get(specificity, 0.30)

    # 3. Length-based range refinement (only if token specificity is medium/low AND length is reliable)
    if length_cm is not None and specificity != "high":
        if length_cm <= 60:
            # Very short — likely melee single/dagger-class
            if range_class == "melee" and length_cm <= 30 and tempo_class != "high":
                tempo_class = "high"
        elif 60 < length_cm <= 180:
            range_class = range_class or "melee"
        elif 180 < length_cm <= 300:
            if range_class == "melee":
                range_class = "mid"
        # Above 300cm is rare; usually weapons quoting full string length on bows etc., not reliable

    # 4. Weight-based STR/DEX disambiguation (only if token attribute is STR or DEX or ambiguous)
    if weight_kg is not None and attribute_class in ("STR", "DEX", None):
        weight_threshold_str = lookup_meta.get("weight_heuristics_kg", {}).get("str_threshold_kg", 2.0)
        weight_threshold_dex = lookup_meta.get("weight_heuristics_kg", {}).get("dex_threshold_kg", 0.8)
        if weight_kg >= weight_threshold_str:
            if attribute_class == "DEX":
                # Conflict — token said DEX, weight says STR. Lower confidence; keep token.
                base_conf = min(base_conf, 0.40)
            elif attribute_class is None:
                attribute_class = "STR"
                base_conf = max(base_conf, 0.55)
        elif weight_kg <= weight_threshold_dex:
            if attribute_class == "STR":
                # Conflict — token said STR, weight says DEX. Lower confidence.
                base_conf = min(base_conf, 0.40)
            elif attribute_class is None:
                attribute_class = "DEX"
                base_conf = max(base_conf, 0.55)

    # 5. wieldable_humanoid sanity-check
    if wieldable_humanoid == "two_hand" and range_class == "melee" and tempo_class == "high":
        # Two-handed light-fast is unusual; lower confidence slightly
        base_conf = max(base_conf * 0.9, 0.25)
    if wieldable_humanoid == "one_hand" and range_class == "melee" and tempo_class == "low":
        # One-handed slow-heavy is unusual; lower confidence slightly
        base_conf = max(base_conf * 0.9, 0.25)

    # 6. Confidence boost for structured-properties presence
    has_structured = (length_cm is not None) or (weight_kg is not None)
    if has_structured and specificity == "high":
        base_conf = min(base_conf + 0.10, 0.95)
    elif has_structured and specificity == "medium":
        base_conf = min(base_conf + 0.05, 0.85)

    # 7. weapon_kind sanity: ammo_or_consumable likely armor/accessory mis-categorized as weapon
    if weapon_kind == "ammo_or_consumable":
        # Often armor/accessory in this DB; lower confidence
        base_conf = min(base_conf, 0.30)

    return {
        "range": range_class,
        "geometry": geometry_class,
        "tempo": tempo_class,
        "attribute": attribute_class,
        "confidence": round(base_conf, 3),
    }


# -----------------------------------------------------------------------------
# Main population loop
# -----------------------------------------------------------------------------

def populate(
    db_path: str,
    lookup_path: str,
    smoke_test: bool = False,
    limit: Optional[int] = None,
    commit_smoke: bool = False,
    chunk_size: int = 10000,
) -> None:
    t0 = time.time()
    lookup = load_lookup(lookup_path)
    token_index = build_token_index(lookup)
    lookup_meta = lookup.get("_meta", {})
    print(f"[init] Loaded {len(token_index)} tokens from lookup table", file=sys.stderr)

    conn = sqlite3.connect(db_path, timeout=120.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=120000")

    ensure_proxy_schema(conn)

    # Build query
    where = "WHERE dedup_status IN ('canonical','unprocessed')"
    if smoke_test:
        # Random 100 rows
        query = f"""SELECT id, canonical_name, wieldable_humanoid, weapon_kind, structured_properties
                    FROM weapon_knowledge_entries {where}
                    ORDER BY RANDOM() LIMIT {limit or 100}"""
    elif limit:
        query = f"""SELECT id, canonical_name, wieldable_humanoid, weapon_kind, structured_properties
                    FROM weapon_knowledge_entries {where} LIMIT {limit}"""
    else:
        query = f"""SELECT id, canonical_name, wieldable_humanoid, weapon_kind, structured_properties
                    FROM weapon_knowledge_entries {where}"""

    # Load all rows into memory first (read lock released before writes start)
    # 69K rows * ~500 bytes avg = ~35MB memory; trivial
    cur = conn.cursor()
    cur.execute(query)
    all_rows = cur.fetchall()
    cur.close()
    print(f"[load] Fetched {len(all_rows)} rows in {time.time() - t0:.1f}s", file=sys.stderr)

    updates: list[tuple] = []
    n_processed = 0
    n_committed = 0
    for row in all_rows:
        rid, name, wh, wk, sp = row
        fp = derive_fingerprint(name, wh, wk, sp, token_index, lookup_meta)
        updates.append((
            fp["range"], fp["geometry"], fp["tempo"], fp["attribute"], fp["confidence"], rid,
        ))
        n_processed += 1
        if not smoke_test and len(updates) >= chunk_size:
            _commit_chunk(conn, updates)
            n_committed += len(updates)
            updates = []
            elapsed = time.time() - t0
            print(f"[progress] {n_processed} processed; {n_committed} committed; {elapsed:.1f}s elapsed", file=sys.stderr)

    if smoke_test:
        # In smoke mode, print results without committing (unless --commit-smoke)
        print(f"[smoke] Processed {n_processed} rows in {time.time() - t0:.2f}s", file=sys.stderr)
        if commit_smoke:
            _commit_chunk(conn, updates)
            print(f"[smoke] Committed {len(updates)} updates", file=sys.stderr)
        # Print sample
        print("\n[smoke-sample] First 20 fingerprints (id | name | range | geom | tempo | attr | conf):")
        # Re-query to get names for display (since updates list is positional)
        ids_in_order = [u[5] for u in updates[:20]]
        if ids_in_order:
            id_to_name = {}
            placeholder = ",".join("?" * len(ids_in_order))
            cur2 = conn.execute(
                f"SELECT id, canonical_name FROM weapon_knowledge_entries WHERE id IN ({placeholder})",
                ids_in_order,
            )
            for rid, n in cur2:
                id_to_name[rid] = n
            for u in updates[:20]:
                rng, geom, tempo, attr, conf, rid = u
                print(f"  {rid:>6} | {id_to_name.get(rid, '?'):<45} | {str(rng):<6} | {str(geom):<10} | {str(tempo):<6} | {str(attr):<4} | {conf:.3f}")
    else:
        if updates:
            _commit_chunk(conn, updates)
            n_committed += len(updates)
        elapsed = time.time() - t0
        print(f"[done] {n_processed} processed; {n_committed} committed; {elapsed:.1f}s total", file=sys.stderr)

    conn.close()


def _commit_chunk(conn: sqlite3.Connection, updates: list[tuple]) -> None:
    conn.executemany(
        """UPDATE weapon_knowledge_entries
           SET proxy_range_class = ?,
               proxy_geometry_class = ?,
               proxy_tempo_class = ?,
               proxy_attribute_class = ?,
               proxy_fingerprint_confidence = ?
         WHERE id = ?""",
        updates,
    )
    conn.commit()


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Populate proxy fingerprint columns on weapon_knowledge_entries")
    ap.add_argument("--db", default=DB_PATH_DEFAULT, help="Path to substrate DB")
    ap.add_argument("--lookup", default=LOOKUP_PATH_DEFAULT, help="Path to lookup table JSON")
    ap.add_argument("--smoke-test", action="store_true", help="Run on 100 random rows; print sample; do not commit")
    ap.add_argument("--commit-smoke", action="store_true", help="If --smoke-test, also commit (for the smoke gate to test write)")
    ap.add_argument("--limit", type=int, default=None, help="Limit to N rows total")
    args = ap.parse_args()

    populate(
        db_path=args.db,
        lookup_path=args.lookup,
        smoke_test=args.smoke_test,
        limit=args.limit,
        commit_smoke=args.commit_smoke,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
