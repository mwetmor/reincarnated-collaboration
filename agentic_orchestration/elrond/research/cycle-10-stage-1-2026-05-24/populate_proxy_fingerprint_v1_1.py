#!/usr/bin/env python3
"""
Cycle 10 Stage 1 v1.1 — Lookup-table micro-fix (UPDATE-only-on-improve)
========================================================================

v1.1 implements the 2 REQUIRED items from gandalf Stage 1 spot-check verdict
(spot-check-gandalf-request.md § 6.3):

ITEM 1: shortspear / longspear / boar-spear / ranseur weapon-form tokens
         (loaded from weapon_form_token_lookup_v1_1.json v1_1_added_tokens)

ITEM 2: compound-noun word-boundary refinement — `blade`/`sword`/`axe`/`hammer`
         tokens now also fire as suffix-matches within compound words
         (spiritblade, lightblade, doomaxe, warhammer, etc.). Plural forms
         (blades/swords/axes/hammers) covered by trailing-'s' strip.

UPDATE-only-on-improve discipline (Discipline #11 attribution clarity):
- NULL rows: populated if new computed confidence ≥ 0.30 (the suffix-match
  base confidence at low-specificity).
- Currently low-conf rows (< 0.30): UPDATE if new conf ≥ 0.30.
- Currently med/high-conf rows (≥ 0.30): UPDATE ONLY if new conf ≥ old + 0.10
  (strict improvement margin); otherwise PRESERVE existing row unchanged.

This guards the v1.0 baseline: no degradation of the existing 21,507 typed
rows; v1.1 is additive lift on currently-NULL / low-conf rows.

Owners: elrond (Cycle 10 Stage 1 v1.1)
Authority: Cycle 10 hive-mind state (Wave 2 follow-on); gandalf Stage 1 verdict
ADR-006: heuristic-only; $0 API spend.

Usage:
    python populate_proxy_fingerprint_v1_1.py [--smoke-test] [--limit N] [--db PATH]

Discipline #19 background execution:
    nohup python populate_proxy_fingerprint_v1_1.py > log_v1_1.out 2>&1 &
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
LOOKUP_V1_0_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/"
    "agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/"
    "weapon_form_token_lookup.json"
)
LOOKUP_V1_1_PATH = (
    "/Users/admin/Games/reincarnated-collaboration/"
    "agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/"
    "weapon_form_token_lookup_v1_1.json"
)

# -----------------------------------------------------------------------------
# Lookup table loading (v1.0 baseline + v1.1 additions)
# -----------------------------------------------------------------------------

CONFIDENCE_TIER = {
    "high": 0.85,
    "medium": 0.65,
    "low": 0.45,
}

# UPDATE-only-on-improve thresholds
NULL_REPLACE_MIN_CONF = 0.30  # populate currently-NULL rows when new conf ≥ this
LOW_CONF_THRESHOLD = 0.30  # rows below this treated as "improvable"
STRICT_IMPROVE_MARGIN = 0.10  # for med/high-conf rows, new conf must exceed by ≥ this


def load_lookup_combined(v1_0_path: str, v1_1_path: str) -> tuple[dict, list[dict]]:
    """Load v1.0 lookup + merge v1.1 additions. Returns (combined_meta, combined_tokens)."""
    with open(v1_0_path) as f:
        v1_0 = json.load(f)
    with open(v1_1_path) as f:
        v1_1 = json.load(f)

    # v1.0 tokens baseline + v1.1 additions
    combined_tokens = list(v1_0["tokens"])
    for tok in v1_1.get("v1_1_added_tokens", []):
        # Skip the documentation note entries
        if tok.get("token", "").startswith("_"):
            continue
        combined_tokens.append(tok)

    # Combined meta: v1.1 over v1.0 for keys both define
    combined_meta = dict(v1_0.get("_meta", {}))
    combined_meta.update(v1_1.get("_meta", {}))
    combined_meta["v1_1_active"] = True
    # Compound suffix block lives in v1.1 meta
    combined_meta["compound_suffix_tokens"] = v1_1["_meta"].get("compound_suffix_tokens", {})
    # Heuristics: prefer v1.1 if present, else v1.0
    combined_meta["length_heuristics_cm"] = v1_1.get(
        "length_heuristics_cm", v1_0.get("length_heuristics_cm", {})
    )
    combined_meta["weight_heuristics_kg"] = v1_1.get(
        "weight_heuristics_kg", v1_0.get("weight_heuristics_kg", {})
    )

    return combined_meta, combined_tokens


def build_token_index(tokens: list[dict]) -> list[dict]:
    """Build a flat list of tokens sorted by length descending (longest-match-wins)."""
    return sorted(tokens, key=lambda t: -len(t["token"]))


# -----------------------------------------------------------------------------
# Whole-word matcher (v1.0 behavior preserved)
# -----------------------------------------------------------------------------

def _name_head_segment(name_lower: str) -> str:
    h = name_lower
    h = re.sub(r"\([^)]*\)", " ", h)
    h = re.sub(r"\[[^\]]*\]", " ", h)
    for sep in [" and ", " with ", ","]:
        idx = h.find(sep)
        if idx != -1:
            h = h[:idx]
    return h.strip()


def find_best_token(name_lower: str, token_index: list[dict]) -> Optional[dict]:
    """v1.0 whole-word matcher — unchanged behavior."""
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

    weapon_matches = [m for m in matches if not (m.get("_is_armor") or m.get("_is_accessory") or m.get("_is_offhand"))]
    accessory_matches = [m for m in matches if m.get("_is_armor") or m.get("_is_accessory") or m.get("_is_offhand")]

    def in_head(tok: dict) -> bool:
        t = tok["token"].lower()
        pattern = r"(?:^|[\W_])" + re.escape(t) + r"(?:$|[\W_])"
        return bool(re.search(pattern, head))

    head_weapons = [m for m in weapon_matches if in_head(m)]
    head_accessories = [m for m in accessory_matches if in_head(m)]

    if head_weapons and head_accessories:
        best_acc = max(head_accessories, key=lambda m: (len(m["token"]), spec_rank.get(m.get("specificity", "low"), 0)))
        best_wpn = max(head_weapons, key=lambda m: (len(m["token"]), spec_rank.get(m.get("specificity", "low"), 0)))
        if len(best_acc["token"]) >= len(best_wpn["token"]):
            return best_acc
        return best_wpn
    if head_accessories:
        head_accessories.sort(key=lambda m: (-len(m["token"]), -spec_rank.get(m.get("specificity", "low"), 0)))
        return head_accessories[0]
    if head_weapons:
        head_weapons.sort(key=lambda m: (-len(m["token"]), -spec_rank.get(m.get("specificity", "low"), 0)))
        return head_weapons[0]
    if accessory_matches:
        return accessory_matches[0]
    weapon_matches.sort(key=lambda m: (-len(m["token"]), -spec_rank.get(m.get("specificity", "low"), 0)))
    return weapon_matches[0]


# -----------------------------------------------------------------------------
# v1.1 compound-suffix matcher (NEW)
# -----------------------------------------------------------------------------

# Compile compound-suffix-match regex: word ending in (suffix) preceded by ≥1 letter,
# also captures plurals (suffix + s). Trailing word-boundary via lookahead.
# Example match: "spiritblade", "doomaxe", "warhammer", "twinblades" (plural).
COMPOUND_SUFFIX_RE = re.compile(
    r"(?:^|[\s_\-])(?P<prefix>\w+?)(?P<suffix>blade|sword|axe|hammer)(?P<plural>s?)(?=$|[\s_\-,.\(\)])",
    re.IGNORECASE,
)

# Bare-plural regex: just "blades"/"swords"/"axes"/"hammers" as standalone word
# (v1.0 whole-word matcher catches singular "blade"/"sword"/etc., misses plural)
BARE_PLURAL_RE = re.compile(
    r"(?:^|[\s_\-,.\(\)])(?P<suffix>blade|sword|axe|hammer)(?P<plural>s)(?=$|[\s_\-,.\(\)])",
    re.IGNORECASE,
)


def find_compound_suffix_match(name_lower: str, suffix_block: dict) -> Optional[dict]:
    """v1.1 NEW: detect compound-suffix patterns (spiritblade, doomaxe, etc.)
    AND bare-plural patterns (blades, swords, axes, hammers).

    Returns a synthesized token dict if a compound-suffix or bare-plural word is found.
    """
    if not name_lower or not suffix_block:
        return None
    best_match = None
    best_prefix_len = 0

    # First: compound-suffix matches (longer = more specific)
    for m in COMPOUND_SUFFIX_RE.finditer(name_lower):
        prefix = m.group("prefix") or ""
        suffix = m.group("suffix").lower()
        if len(prefix) < 1:
            continue
        suffix_cfg = None
        for s in suffix_block.get("suffixes", []):
            if s["suffix"].lower() == suffix:
                suffix_cfg = s
                break
        if suffix_cfg is None:
            continue
        if len(prefix) > best_prefix_len:
            best_prefix_len = len(prefix)
            prefix_lower = prefix.lower()
            attribute = suffix_cfg.get("attribute_fallback", "STR")
            dex_hints = suffix_cfg.get("attribute_prefix_dex_hint", [])
            str_hints = suffix_cfg.get("attribute_prefix_str_hint", [])
            if any(h.lower() in prefix_lower for h in dex_hints):
                attribute = "DEX"
            elif any(h.lower() in prefix_lower for h in str_hints):
                attribute = "STR"
            best_match = {
                "token": prefix + suffix,
                "specificity": suffix_cfg.get("specificity", "low"),
                "range": suffix_cfg.get("range", "melee"),
                "geometry": suffix_cfg.get("geometry", "cleave"),
                "tempo": suffix_cfg.get("tempo", "medium"),
                "attribute": attribute,
                "_v1_1_compound_suffix": True,
            }

    # Second: bare-plural fallback if no compound-suffix found
    if best_match is None:
        for m in BARE_PLURAL_RE.finditer(name_lower):
            suffix = m.group("suffix").lower()
            suffix_cfg = None
            for s in suffix_block.get("suffixes", []):
                if s["suffix"].lower() == suffix:
                    suffix_cfg = s
                    break
            if suffix_cfg is None:
                continue
            # Use suffix_cfg defaults; attribute_fallback (STR) — no prefix to disambiguate
            best_match = {
                "token": suffix + "s",
                "specificity": suffix_cfg.get("specificity", "low"),
                "range": suffix_cfg.get("range", "melee"),
                "geometry": suffix_cfg.get("geometry", "cleave"),
                "tempo": suffix_cfg.get("tempo", "medium"),
                "attribute": suffix_cfg.get("attribute_fallback", "STR"),
                "_v1_1_bare_plural": True,
            }
            break  # first match suffices for bare plural

    return best_match


# -----------------------------------------------------------------------------
# Length / weight extraction (v1.0 unchanged)
# -----------------------------------------------------------------------------

LENGTH_CM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*cm\b", re.IGNORECASE)
LENGTH_IN_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:in\.|inches|\"|\bin\b)", re.IGNORECASE)
WEIGHT_G_RE = re.compile(r"(\d+(?:\.\d+)?)\s*g\b(?!\w)", re.IGNORECASE)
WEIGHT_OZ_RE = re.compile(r"(\d+(?:\.\d+)?)\s*oz\b", re.IGNORECASE)
WEIGHT_KG_RE = re.compile(r"(\d+(?:\.\d+)?)\s*kg\b", re.IGNORECASE)
WEIGHT_LB_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:lb|lbs)\b", re.IGNORECASE)


def extract_length_cm(text: str) -> Optional[float]:
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

    for field in ("dimensions", "length", "overall_length", "blade_length", "mass", "weight"):
        v = d.get(field)
        if isinstance(v, str):
            if length_cm is None:
                length_cm = extract_length_cm(v)
            if weight_kg is None:
                weight_kg = extract_weight_kg(v)

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
# Fingerprint derivation (v1.1: whole-word matcher → compound-suffix fallback)
# -----------------------------------------------------------------------------

def derive_fingerprint(
    canonical_name: str,
    wieldable_humanoid: str,
    weapon_kind: str,
    structured_properties: Optional[str],
    token_index: list[dict],
    lookup_meta: dict,
) -> dict:
    name_lower = (canonical_name or "").lower()
    length_cm, weight_kg = parse_structured_props(structured_properties)

    # 1. v1.0 whole-word token match
    matched = find_best_token(name_lower, token_index)

    # 2. v1.1 NEW: compound-suffix fallback when whole-word matcher returns None
    used_suffix_match = False
    if matched is None:
        suffix_block = lookup_meta.get("compound_suffix_tokens", {})
        matched = find_compound_suffix_match(name_lower, suffix_block)
        if matched is not None:
            used_suffix_match = True

    # 3. Handle non-weapon tokens early
    if matched and (matched.get("_is_armor") or matched.get("_is_accessory") or matched.get("_is_offhand")):
        return {
            "range": None, "geometry": None, "tempo": None, "attribute": None,
            "confidence": 0.10,
        }

    if matched is None:
        if wieldable_humanoid == "mount_required":
            return {
                "range": "mid", "geometry": "single", "tempo": "low", "attribute": "STR",
                "confidence": 0.20,
            }
        return {
            "range": None, "geometry": None, "tempo": None, "attribute": None,
            "confidence": 0.05,
        }

    range_class = matched.get("range")
    geometry_class = matched.get("geometry")
    tempo_class = matched.get("tempo")
    attribute_class = matched.get("attribute")
    specificity = matched.get("specificity", "low")
    base_conf = CONFIDENCE_TIER.get(specificity, 0.30)

    # Compound-suffix matches sit at low-specificity = 0.45 base, ensure no boost
    if used_suffix_match:
        # No length/weight boost for synthesized matches — they are less authoritative
        # than whole-word matches. Keep at base 0.45 unless structured data agrees.
        pass

    # 4. Length-based range refinement
    if length_cm is not None and specificity != "high":
        if length_cm <= 60:
            if range_class == "melee" and length_cm <= 30 and tempo_class != "high":
                tempo_class = "high"
        elif 60 < length_cm <= 180:
            range_class = range_class or "melee"
        elif 180 < length_cm <= 300:
            if range_class == "melee":
                range_class = "mid"

    # 5. Weight-based STR/DEX disambiguation
    if weight_kg is not None and attribute_class in ("STR", "DEX", None):
        weight_threshold_str = lookup_meta.get("weight_heuristics_kg", {}).get("str_threshold_kg", 2.0)
        weight_threshold_dex = lookup_meta.get("weight_heuristics_kg", {}).get("dex_threshold_kg", 0.8)
        if weight_kg >= weight_threshold_str:
            if attribute_class == "DEX":
                base_conf = min(base_conf, 0.40)
            elif attribute_class is None:
                attribute_class = "STR"
                base_conf = max(base_conf, 0.55)
        elif weight_kg <= weight_threshold_dex:
            if attribute_class == "STR":
                base_conf = min(base_conf, 0.40)
            elif attribute_class is None:
                attribute_class = "DEX"
                base_conf = max(base_conf, 0.55)

    # 6. wieldable_humanoid sanity-check
    if wieldable_humanoid == "two_hand" and range_class == "melee" and tempo_class == "high":
        base_conf = max(base_conf * 0.9, 0.25)
    if wieldable_humanoid == "one_hand" and range_class == "melee" and tempo_class == "low":
        base_conf = max(base_conf * 0.9, 0.25)

    # 7. Confidence boost for structured-properties presence (whole-word matches only)
    has_structured = (length_cm is not None) or (weight_kg is not None)
    if has_structured and specificity == "high" and not used_suffix_match:
        base_conf = min(base_conf + 0.10, 0.95)
    elif has_structured and specificity == "medium" and not used_suffix_match:
        base_conf = min(base_conf + 0.05, 0.85)

    # 8. weapon_kind sanity
    if weapon_kind == "ammo_or_consumable":
        base_conf = min(base_conf, 0.30)

    return {
        "range": range_class,
        "geometry": geometry_class,
        "tempo": tempo_class,
        "attribute": attribute_class,
        "confidence": round(base_conf, 3),
    }


# -----------------------------------------------------------------------------
# UPDATE-only-on-improve gate
# -----------------------------------------------------------------------------

def should_update(old_conf: Optional[float], new_conf: float) -> bool:
    """Decide whether to UPDATE the row per UPDATE-only-on-improve discipline.

    - Currently-NULL conf → update if new ≥ NULL_REPLACE_MIN_CONF (0.30)
    - Currently low-conf (< 0.30) → update if new ≥ 0.30
    - Currently med/high (≥ 0.30) → update only if new ≥ old + 0.10
    """
    if old_conf is None:
        return new_conf >= NULL_REPLACE_MIN_CONF
    if old_conf < LOW_CONF_THRESHOLD:
        return new_conf >= NULL_REPLACE_MIN_CONF
    # old_conf >= 0.30: strict improvement required
    return new_conf >= old_conf + STRICT_IMPROVE_MARGIN


# -----------------------------------------------------------------------------
# Main population loop
# -----------------------------------------------------------------------------

def populate(
    db_path: str,
    lookup_v1_0: str,
    lookup_v1_1: str,
    smoke_test: bool = False,
    limit: Optional[int] = None,
    commit_smoke: bool = False,
    chunk_size: int = 10000,
) -> dict:
    """Returns summary stats dict for post-execution reporting."""
    t0 = time.time()
    lookup_meta, tokens = load_lookup_combined(lookup_v1_0, lookup_v1_1)
    token_index = build_token_index(tokens)
    print(
        f"[init] Loaded {len(token_index)} tokens (v1.0 + v1.1) + compound-suffix block",
        file=sys.stderr,
    )

    conn = sqlite3.connect(db_path, timeout=120.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=120000")

    where = "WHERE dedup_status IN ('canonical','unprocessed')"
    if smoke_test:
        query = f"""SELECT id, canonical_name, wieldable_humanoid, weapon_kind,
                           structured_properties, proxy_fingerprint_confidence,
                           proxy_range_class, proxy_geometry_class, proxy_tempo_class,
                           proxy_attribute_class
                    FROM weapon_knowledge_entries {where}
                    ORDER BY RANDOM() LIMIT {limit or 100}"""
    elif limit:
        query = f"""SELECT id, canonical_name, wieldable_humanoid, weapon_kind,
                           structured_properties, proxy_fingerprint_confidence,
                           proxy_range_class, proxy_geometry_class, proxy_tempo_class,
                           proxy_attribute_class
                    FROM weapon_knowledge_entries {where} LIMIT {limit}"""
    else:
        query = f"""SELECT id, canonical_name, wieldable_humanoid, weapon_kind,
                           structured_properties, proxy_fingerprint_confidence,
                           proxy_range_class, proxy_geometry_class, proxy_tempo_class,
                           proxy_attribute_class
                    FROM weapon_knowledge_entries {where}"""

    cur = conn.cursor()
    cur.execute(query)
    all_rows = cur.fetchall()
    cur.close()
    print(f"[load] Fetched {len(all_rows)} rows in {time.time() - t0:.1f}s", file=sys.stderr)

    updates: list[tuple] = []
    stats = {
        "n_scanned": 0,
        "n_updated": 0,
        "n_null_to_typed": 0,
        "n_low_to_typed": 0,
        "n_already_better": 0,
        "n_suffix_match_fired": 0,
        "n_new_spear_tokens_fired": 0,
        "n_unchanged": 0,
    }

    # New spear-token names to count separately
    new_spear_tokens = {
        "shortspear", "short spear", "longspear", "long spear", "long-spear",
        "boar spear", "boar-spear", "boarspear", "bore-spear", "winged spear",
    }

    for row in all_rows:
        rid, name, wh, wk, sp, old_conf, old_range, old_geom, old_tempo, old_attr = row
        stats["n_scanned"] += 1
        fp = derive_fingerprint(name, wh, wk, sp, token_index, lookup_meta)
        new_conf = fp["confidence"]

        if not should_update(old_conf, new_conf):
            stats["n_unchanged"] += 1
            continue

        # Identify how the row got upgraded for attribution tracking
        name_lower = (name or "").lower()
        # Use whole-word matcher path detection
        whole_match = find_best_token(name_lower, token_index)
        if whole_match is None:
            # Must have been compound-suffix
            stats["n_suffix_match_fired"] += 1
        else:
            # If matched token is one of the new spear tokens
            mt = whole_match.get("token", "").lower()
            if mt in new_spear_tokens:
                stats["n_new_spear_tokens_fired"] += 1

        if old_conf is None:
            stats["n_null_to_typed"] += 1
        elif old_conf < LOW_CONF_THRESHOLD:
            stats["n_low_to_typed"] += 1
        else:
            stats["n_already_better"] += 1

        updates.append((
            fp["range"], fp["geometry"], fp["tempo"], fp["attribute"], fp["confidence"], rid,
        ))
        stats["n_updated"] += 1

        if not smoke_test and len(updates) >= chunk_size:
            _commit_chunk(conn, updates)
            updates = []
            elapsed = time.time() - t0
            print(
                f"[progress] {stats['n_scanned']} scanned; {stats['n_updated']} updated; "
                f"{elapsed:.1f}s elapsed",
                file=sys.stderr,
            )

    if smoke_test:
        print(f"[smoke] {stats}", file=sys.stderr)
        if commit_smoke and updates:
            _commit_chunk(conn, updates)
            print(f"[smoke] Committed {len(updates)} updates", file=sys.stderr)
        # Print 20-row sample
        print("\n[smoke-sample] First 20 update candidates:")
        ids_in_order = [u[5] for u in updates[:20]]
        if ids_in_order:
            placeholder = ",".join("?" * len(ids_in_order))
            cur2 = conn.execute(
                f"SELECT id, canonical_name, proxy_fingerprint_confidence FROM weapon_knowledge_entries "
                f"WHERE id IN ({placeholder})",
                ids_in_order,
            )
            id_to_meta = {rid: (n, c) for rid, n, c in cur2}
            for u in updates[:20]:
                rng, geom, tempo, attr, conf, rid = u
                name, old_c = id_to_meta.get(rid, ("?", None))
                old_c_str = f"{old_c:.2f}" if old_c is not None else "NULL"
                print(
                    f"  {rid:>6} | {name[:45]:<45} | old={old_c_str:<5} | "
                    f"new={conf:.2f} | {str(rng):<6} | {str(geom):<10} | "
                    f"{str(tempo):<6} | {str(attr):<4}"
                )
    else:
        if updates:
            _commit_chunk(conn, updates)
        elapsed = time.time() - t0
        print(f"[done] {stats}", file=sys.stderr)
        print(f"[done] {elapsed:.1f}s total", file=sys.stderr)

    conn.close()
    return stats


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
    ap = argparse.ArgumentParser(
        description="v1.1 Lookup-table micro-fix: spear vocab + compound-suffix word-boundary refinement"
    )
    ap.add_argument("--db", default=DB_PATH_DEFAULT)
    ap.add_argument("--lookup-v1-0", default=LOOKUP_V1_0_PATH)
    ap.add_argument("--lookup-v1-1", default=LOOKUP_V1_1_PATH)
    ap.add_argument("--smoke-test", action="store_true")
    ap.add_argument("--commit-smoke", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    populate(
        db_path=args.db,
        lookup_v1_0=args.lookup_v1_0,
        lookup_v1_1=args.lookup_v1_1,
        smoke_test=args.smoke_test,
        limit=args.limit,
        commit_smoke=args.commit_smoke,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
