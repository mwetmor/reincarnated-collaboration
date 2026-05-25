#!/usr/bin/env python3
"""
Cycle 10 Stage 4 — weapon_sim_props population script
Dispatch authority: agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md
Methodology: agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md
Composition policy: canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md § 3
BC-axes lock: canonical/story/qd-engine-bc-axes-lock-2026-05-20.md

3-Pass layered approach:
  Pass 1 (1,851 typed rows): heuristic from proxy columns + Stage 1.5 extracted_length
  Pass 2 (44 NULL-typed rows with weapon_type key): structured-property lookup
  Pass 3 (~250 NULL-typed rows): LLM-judge on canonical_name + cultural_lineage + structured_properties
  Pre-screen: odin-army-tradoc modern military vehicles → sim_viable=0 default
"""

import sqlite3
import json
import os
import re
import sys
import time
import logging
import anthropic
from datetime import datetime

# --- Configuration ---
DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/population-run.log"
AMBIGUOUS_LOG_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/ambiguous-cases.jsonl"
MYTHOLOGICAL_LOG_PATH = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/mythological-null-rescue-log.jsonl"
TODAY = datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("stage4")

# --- Per-bin lookup tables (from legolas methodology consult § c) ---

RANGE_BIN_DEFAULTS = {
    "melee":            (0.5, 2.5),
    "mid":              (2.5, 7.0),
    "ranged":           (5.0, 18.0),
    "melee_close_or_grapple": (0.5, 1.5),
    "off_hand_aura":    (0.0, 3.0),
}

TEMPO_BIN_DEFAULTS = {
    "high":             2.5,   # base_attack_speed attacks/sec
    "medium":           1.5,
    "low":              0.7,
    "reactive_block_tempo": 0.5,
    "aura_pulse_tempo": 0.3,
}

GEOMETRY_BIN_DEFAULTS = {
    "single":           (1, 0.0),   # (hits_per_attack, aoe_radius_units)
    "cleave":           (1, 1.5),
    "AoE":              (1, 3.5),
    "multi-hit":        (3, 0.0),
    "scatter":          (1, 1.0),
    "cone":             (1, 2.0),
    "shield_blocker":   (1, 0.0),
    "banner_rally_aura":(1, 3.0),
}

# charge_time by (tempo, attribute): (tempo_class, attribute_class) -> charge_time_s
def get_charge_time(tempo_class: str, attribute_class: str) -> float:
    if tempo_class in ("high", "medium"):
        return 0.0
    if tempo_class == "low":
        if attribute_class in ("INT", "WIS"):
            return 1.2
        return 0.5
    if tempo_class == "reactive_block_tempo":
        return 0.0
    if tempo_class == "aura_pulse_tempo":
        return 0.0
    return 0.0

# Damage amplitude by (geometry, tempo): returns (min, max)
# Source: legolas consult § c, amplitude ratio bins
def get_damage_amplitude(geometry_class: str, tempo_class: str, attribute_class: str) -> tuple:
    # Base from geometry x tempo cross
    combos = {
        ("single", "high"):   (0.8, 1.2),   # flat; ratio 1.5x
        ("single", "medium"): (0.7, 1.6),   # variable; ratio 2.3x
        ("single", "low"):    (0.3, 2.5),   # spiky; ratio 8.3x
        ("cleave", "high"):   (0.7, 1.3),   # flat; ratio 1.9x boundary
        ("cleave", "medium"): (0.7, 1.4),   # flat-variable; ratio 2.0x
        ("cleave", "low"):    (0.5, 1.8),   # variable; ratio 3.6x
        ("AoE", "high"):      (0.6, 1.3),   # variable; ratio 2.2x
        ("AoE", "medium"):    (0.5, 1.7),   # variable; ratio 3.4x
        ("AoE", "low"):       (0.4, 2.0),   # variable; ratio 5.0x
        ("multi-hit", "high"):(0.6, 1.0),   # flat; ratio 1.7x
        ("multi-hit", "medium"):(0.6, 1.0), # flat; ratio 1.7x
        ("multi-hit", "low"): (0.5, 1.0),   # flat; ratio 2.0x
        ("scatter", "high"):  (0.5, 1.3),   # variable; ratio 2.6x
        ("scatter", "medium"):(0.5, 1.5),   # variable; ratio 3.0x
        ("scatter", "low"):   (0.4, 1.8),   # variable; ratio 4.5x boundary
        ("cone", "high"):     (0.6, 1.2),   # flat-variable; ratio 2.0x
        ("cone", "medium"):   (0.5, 1.6),   # variable; ratio 3.2x
        ("cone", "low"):      (0.4, 1.9),   # variable; ratio 4.75x (spiky)
        ("shield_blocker", "medium"):  (0.3, 0.5),  # low damage; defensive item
        ("shield_blocker", "reactive_block_tempo"): (0.3, 0.5),
        ("banner_rally_aura", "aura_pulse_tempo"):   (0.0, 0.0),  # support item; no damage
    }
    amp_min, amp_max = combos.get(
        (geometry_class, tempo_class),
        combos.get((geometry_class, "medium"), (0.6, 1.5))   # fallback
    )
    # Option β upward bias for INT/WIS caster weapons (consult § c)
    if attribute_class in ("INT", "WIS"):
        amp_min = round(amp_min * 1.2, 3)
        amp_max = round(amp_max * 1.5, 3)
    return (amp_min, amp_max)

# range refinement from extracted_length_cm (consult § c)
LENGTH_SCALE_FACTOR = 0.028  # extracted_length_cm * 0.028 = refined range_max_tiles

def refine_range_max(range_class: str, length_cm: float, confidence: float) -> float:
    if confidence < 0.65 or length_cm is None:
        return RANGE_BIN_DEFAULTS.get(range_class, (0.5, 2.5))[1]
    refined = length_cm * LENGTH_SCALE_FACTOR
    bin_min, bin_max = RANGE_BIN_DEFAULTS.get(range_class, (0.5, 2.5))
    # Clamp to sensible range for the bin
    return max(bin_min + 0.5, min(refined, bin_max * 1.5))

# --- weapon_type to proxy 4-tuple lookup (Pass 2) ---
WEAPON_TYPE_LOOKUP = {
    "spear":              ("mid",    "single",   "medium", "STR"),
    "bow":                ("ranged", "single",   "high",   "DEX"),
    "sword":              ("melee",  "single",   "medium", "STR"),
    "mythological sword": ("melee",  "single",   "medium", "STR"),
    "mythological weapon":("melee",  "single",   "medium", "STR"),
    "hammer":             ("melee",  "single",   "low",    "STR"),
    "axe":                ("melee",  "cleave",   "medium", "STR"),
    "dagger":             ("melee",  "single",   "high",   "DEX"),
    "shield":             ("melee",  "single",   "medium", "STR"),
    "chakram":            ("ranged", "scatter",  "high",   "DEX"),
    "gun":                ("ranged", "single",   "low",    "DEX"),
    "staff":              ("mid",    "AoE",      "medium", "WIS"),
    "wand":               ("mid",    "single",   "medium", "INT"),
    "lance":              ("mid",    "single",   "medium", "STR"),
    "club":               ("melee",  "single",   "low",    "STR"),
    "mace":               ("melee",  "single",   "low",    "STR"),
    "flail":              ("melee",  "multi-hit","medium", "STR"),
    "javelin":            ("ranged", "single",   "medium", "STR"),
    "sling":              ("ranged", "single",   "high",   "DEX"),
    "crossbow":           ("ranged", "single",   "low",    "DEX"),
    "tanto":              ("melee",  "single",   "high",   "DEX"),
    "tantō":              ("melee",  "single",   "high",   "DEX"),
    "naginata":           ("mid",    "cleave",   "medium", "DEX"),
    "katana":             ("melee",  "single",   "high",   "DEX"),
    "Norse mythical object": ("melee","single",  "low",    "STR"),
    "religious concept":  ("mid",    "AoE",      "low",    "WIS"),
    "archaeological artefact": ("melee","single","medium", "STR"),
    "slash_sword":        ("melee",  "single",   "medium", "STR"),
    "mythological hammer":("melee",  "AoE",      "low",    "STR"),
    "trident":            ("mid",    "single",   "medium", "STR"),
    "polearm":            ("mid",    "cleave",   "medium", "STR"),
}

def lookup_weapon_type(weapon_type_str: str) -> tuple | None:
    """Returns (range_class, geometry_class, tempo_class, attribute_class) or None."""
    if not weapon_type_str:
        return None
    wt = weapon_type_str.lower().strip()
    for key, val in WEAPON_TYPE_LOOKUP.items():
        if wt == key.lower():
            return val
    # Partial match fallback
    for key, val in WEAPON_TYPE_LOOKUP.items():
        if key.lower() in wt or wt in key.lower():
            return val
    return None

# --- Known component/non-weapon patterns (sim_viable=0) ---
COMPONENT_PATTERNS = [
    "lockplate", "detached", "electrotype", "mannequin",
    "inner barrel", "fuse cutter", "holster", "case for",
    "replica of", "detached upper", "bayonet scabbard",
    "percussion cap", "bullet mould", "powder horn",
    "cartridge box", "sword knot", "sword belt",
]

def is_component_part(canonical_name: str) -> bool:
    name_lower = canonical_name.lower()
    return any(p in name_lower for p in COMPONENT_PATTERNS)

# --- LLM judge (Pass 3) ---
LLM_CLIENT = None

def get_llm_client():
    global LLM_CLIENT
    if LLM_CLIENT is None:
        LLM_CLIENT = anthropic.Anthropic()
    return LLM_CLIENT

def llm_classify_weapon(row: dict) -> dict:
    """
    Calls LLM to classify a weapon into proxy 4-tuple.
    Returns dict with keys: range_class, geometry_class, tempo_class, attribute_class, confidence
    """
    canonical_name = row.get("canonical_name", "")
    cultural_lineage = row.get("cultural_lineage_canonical", "unknown")
    register = row.get("register_canonical", "unknown")
    structured_props = row.get("structured_properties", "none") or "none"
    length_cm = row.get("extracted_length_value")
    length_str = str(length_cm) if length_cm else "unknown"

    prompt = f"""Given a weapon entry with the following attributes:
- canonical_name: {canonical_name}
- cultural_lineage: {cultural_lineage}
- register: {register}
- structured_properties: {structured_props[:300] if structured_props != 'none' else 'none'}
- extracted_length_cm: {length_str}

Classify the weapon into these bins:
- range_class: melee | mid | ranged
- geometry_class: single | cleave | AoE | multi-hit | scatter | cone
- tempo_class: low | medium | high
- attribute_class: STR | INT | WIS | DEX

Respond with JSON only: {{"range":"...", "geometry":"...", "tempo":"...", "attribute":"...", "confidence":0.0-1.0}}

Rules:
- If the weapon is a projectile launcher (bow, crossbow, gun, sling, atlatl), range = ranged
- If the weapon is a polearm, spear, lance, or reach weapon implied > 2 meters, range = mid
- If the weapon is a sword, axe, dagger, mace, fist weapon, staff < 1.5m, range = melee
- If the weapon is magical/ritual (wand, orb, tome, staff used for casting), attribute = INT or WIS
- If the weapon is for a warrior/knight archetype, attribute = STR
- If the weapon is for a rogue/archer/finesse archetype, attribute = DEX
- confidence = 0.9 if canonical_name unambiguously identifies the weapon type
- confidence = 0.6 if deduction from name/cultural_lineage only
- confidence = 0.4 if significant ambiguity"""

    client = get_llm_client()
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=128,
            system="You are a weapon classifier. Respond ONLY with a JSON object, no explanation, no preamble, no code fences.",
            messages=[{"role": "user", "content": prompt}]
        )
        text = msg.content[0].text.strip()
        # Extract JSON from response (handles reasoning text + code fences)
        # Priority 1: extract from ```json ... ``` fences
        fence_match = re.search(r'```(?:json)?\s*(\{[^`]+\})\s*```', text, re.DOTALL)
        if fence_match:
            text = fence_match.group(1).strip()
        else:
            # Priority 2: find first {...} JSON object in text
            json_match = re.search(r'\{[^{}]+\}', text)
            if json_match:
                text = json_match.group(0)
        # Parse JSON
        data = json.loads(text)
        range_class = data.get("range", "melee")
        geometry_class = data.get("geometry", "single")
        tempo_class = data.get("tempo", "medium")
        attribute_class = data.get("attribute", "STR")
        confidence = float(data.get("confidence", 0.5))

        # Normalize range_class to known bins
        range_map = {"melee": "melee", "mid": "mid", "ranged": "ranged"}
        range_class = range_map.get(range_class, "melee")

        return {
            "range_class": range_class,
            "geometry_class": geometry_class,
            "tempo_class": tempo_class,
            "attribute_class": attribute_class,
            "confidence": confidence,
        }
    except Exception as e:
        log.warning(f"LLM classify failed for {canonical_name}: {e}")
        return {
            "range_class": "melee",
            "geometry_class": "single",
            "tempo_class": "medium",
            "attribute_class": "STR",
            "confidence": 0.2,
        }

# --- sim_viable determination ---
def determine_sim_viable(row: dict, range_class: str, geometry_class: str,
                         tempo_class: str, attribute_class: str) -> tuple:
    """Returns (sim_viable: int, sim_viability_notes: str)"""
    canonical_name = row.get("canonical_name", "")
    source_library = row.get("source_library", "")
    register = row.get("register_canonical", "unknown")

    # odin-army-tradoc modern military vehicles
    if source_library == "odin-army-tradoc" or register == "military_modern":
        return (0, "military_modern_vehicle — out of genre scope for v1")

    # Component parts from royal_armouries
    if is_component_part(canonical_name):
        return (0, f"weapon_component_part — not a complete weapon; {canonical_name[:60]}")

    # Known non-viable geometry classes
    if geometry_class == "banner_rally_aura":
        return (0, "support_banner — no direct damage; Phase 2 binding as support item only")

    # shield_blocker: viable as secondary/off-hand sim item
    if geometry_class == "shield_blocker":
        return (1, "shield_blocker — off-hand defensive; sim viable as secondary")

    # Standard viable
    return (1, "")

# --- Main population logic ---

def compute_sim_props(row: dict, range_class: str, geometry_class: str,
                      tempo_class: str, attribute_class: str,
                      length_cm: float = None, confidence: float = 0.65) -> dict:
    """Compute all weapon_sim_props values from proxy 4-tuple + optional length."""
    rng_min, rng_max = RANGE_BIN_DEFAULTS.get(range_class, (0.5, 2.5))
    if length_cm and confidence >= 0.65:
        rng_max = refine_range_max(range_class, length_cm, confidence)

    atk_speed = TEMPO_BIN_DEFAULTS.get(tempo_class, 1.5)
    charge = get_charge_time(tempo_class, attribute_class)
    hits, aoe = GEOMETRY_BIN_DEFAULTS.get(geometry_class, (1, 0.0))
    amp_min, amp_max = get_damage_amplitude(geometry_class, tempo_class, attribute_class)
    sim_viable, sim_notes = determine_sim_viable(row, range_class, geometry_class,
                                                  tempo_class, attribute_class)

    return {
        "range_min_units": rng_min,
        "range_max_units": round(rng_max, 3),
        "base_attack_speed": atk_speed,
        "charge_time_s": charge,
        "hits_per_attack": hits,
        "aoe_radius_units": aoe,
        "primary_stat": attribute_class,
        "secondary_stat": "none",
        "damage_amplitude_min": amp_min,
        "damage_amplitude_max": amp_max,
        "sim_viable": sim_viable,
        "sim_viability_notes": sim_notes,
        "sim_verified_date": TODAY,
    }

def run_population():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch all v1_scope entries
    cur.execute("""
        SELECT id, canonical_name, source_library, register_canonical,
               proxy_range_class, proxy_geometry_class, proxy_tempo_class, proxy_attribute_class,
               proxy_fingerprint_confidence,
               extracted_length_value, extracted_length_unit,
               structured_properties, cultural_lineage_canonical,
               v1_scope_composition_trace, quality_tier
        FROM weapon_knowledge_entries
        WHERE v1_scope = 1
        ORDER BY id
    """)
    rows = cur.fetchall()
    log.info(f"Total v1_scope rows: {len(rows)}")

    stats = {
        "pass1_typed": 0,
        "pass2_weapon_type": 0,
        "pass2b_odin_prescreen": 0,
        "pass3_llm": 0,
        "pass3_component_default": 0,
        "llm_low_confidence": 0,
        "inserted": 0,
        "errors": 0,
        "mythological_rescue": 0,
    }

    ambiguous_log = open(AMBIGUOUS_LOG_PATH, "w")
    mythological_log = open(MYTHOLOGICAL_LOG_PATH, "w")

    # LLM rate: ~1 req / 2 sec to stay within limits
    LLM_DELAY = 0.5  # reduced; sonnet-4-6 can handle more

    insert_sql = """
        INSERT OR REPLACE INTO weapon_sim_props (
            weapon_id, range_min_units, range_max_units, base_attack_speed, charge_time_s,
            hits_per_attack, aoe_radius_units, primary_stat, secondary_stat,
            damage_amplitude_min, damage_amplitude_max,
            sim_viable, sim_viability_notes, sim_verified_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for i, row in enumerate(rows):
        row_dict = dict(row)
        weapon_id = row_dict["id"]
        canonical_name = row_dict["canonical_name"]
        source_library = row_dict["source_library"]
        register = row_dict["register_canonical"]

        range_class = row_dict["proxy_range_class"]
        geometry_class = row_dict["proxy_geometry_class"]
        tempo_class = row_dict["proxy_tempo_class"]
        attribute_class = row_dict["proxy_attribute_class"]
        length_cm = row_dict["extracted_length_value"]
        confidence = row_dict["proxy_fingerprint_confidence"] or 0.65
        pass_used = None

        # --- Pre-screen: odin-army-tradoc ---
        if source_library == "odin-army-tradoc":
            range_class = "ranged"
            geometry_class = "single"
            tempo_class = "low"
            attribute_class = "STR"
            confidence = 0.3
            pass_used = "pass2b_prescreen"
            stats["pass2b_odin_prescreen"] += 1

        # --- Pass 1: already-typed rows ---
        elif range_class is not None:
            # Normalize non-standard proxy classes
            if range_class == "melee_close_or_grapple":
                range_class = "melee"
                geometry_class = "single"
            elif range_class == "off_hand_aura":
                range_class = "melee"
                geometry_class = "banner_rally_aura"
            if attribute_class in ("STR_or_DEX",):
                attribute_class = "DEX"  # conservative for Option α
            elif attribute_class in ("STR_or_WIS",):
                attribute_class = "WIS"
            pass_used = "pass1_heuristic"
            stats["pass1_typed"] += 1

        else:
            # --- Pass 2: weapon_type key in structured_properties ---
            structured_props = row_dict.get("structured_properties") or ""
            weapon_type_val = None
            if structured_props and "weapon_type" in structured_props:
                try:
                    sp = json.loads(structured_props)
                    weapon_type_val = sp.get("weapon_type")
                except Exception:
                    pass

            if weapon_type_val:
                result = lookup_weapon_type(weapon_type_val)
                if result:
                    range_class, geometry_class, tempo_class, attribute_class = result
                    confidence = 0.65
                    pass_used = "pass2_weapon_type"
                    stats["pass2_weapon_type"] += 1

            # --- Pass 3: LLM judge ---
            if pass_used is None:
                # Component-part pre-screen
                if is_component_part(canonical_name):
                    range_class = "melee"
                    geometry_class = "single"
                    tempo_class = "medium"
                    attribute_class = "STR"
                    confidence = 0.3
                    pass_used = "pass3_component_default"
                    stats["pass3_component_default"] += 1
                else:
                    result = llm_classify_weapon(row_dict)
                    range_class = result["range_class"]
                    geometry_class = result["geometry_class"]
                    tempo_class = result["tempo_class"]
                    attribute_class = result["attribute_class"]
                    confidence = result["confidence"]
                    pass_used = "pass3_llm"
                    stats["pass3_llm"] += 1

                    if confidence < 0.6:
                        stats["llm_low_confidence"] += 1
                        ambiguous_log.write(json.dumps({
                            "weapon_id": weapon_id,
                            "canonical_name": canonical_name,
                            "source_library": source_library,
                            "register": register,
                            "classified": result,
                            "structured_properties": (structured_props or "")[:200],
                        }) + "\n")

                    time.sleep(LLM_DELAY)

        # Track mythological-NULL rescue
        is_mythological_rescue = (
            register == "mythological"
            and row_dict["proxy_range_class"] is None
            and pass_used != "pass2b_prescreen"
        )

        # Update proxy columns on weapon_knowledge_entries if this was NULL-typed
        if row_dict["proxy_range_class"] is None and pass_used != "pass1_heuristic":
            try:
                conn.execute("""
                    UPDATE weapon_knowledge_entries
                    SET proxy_range_class = ?,
                        proxy_geometry_class = ?,
                        proxy_tempo_class = ?,
                        proxy_attribute_class = ?,
                        proxy_fingerprint_confidence = ?
                    WHERE id = ?
                """, (range_class, geometry_class, tempo_class, attribute_class,
                      round(confidence, 3), weapon_id))
            except Exception as e:
                log.error(f"Failed to update proxy columns for {weapon_id} ({canonical_name}): {e}")

        # Compute sim props
        props = compute_sim_props(row_dict, range_class, geometry_class,
                                  tempo_class, attribute_class, length_cm, confidence)

        try:
            cur.execute(insert_sql, (
                weapon_id,
                props["range_min_units"],
                props["range_max_units"],
                props["base_attack_speed"],
                props["charge_time_s"],
                props["hits_per_attack"],
                props["aoe_radius_units"],
                props["primary_stat"],
                props["secondary_stat"],
                props["damage_amplitude_min"],
                props["damage_amplitude_max"],
                props["sim_viable"],
                props["sim_viability_notes"],
                props["sim_verified_date"],
            ))
            stats["inserted"] += 1
        except Exception as e:
            log.error(f"INSERT failed for {weapon_id} ({canonical_name}): {e}")
            stats["errors"] += 1

        # Mythological-NULL rescue: update composition trace + log
        if is_mythological_rescue:
            stats["mythological_rescue"] += 1
            try:
                conn.execute("""
                    UPDATE weapon_knowledge_entries
                    SET v1_scope_composition_trace = json_set(
                        COALESCE(v1_scope_composition_trace, '{}'),
                        '$.stage_4_mythological_rescue', 'complete',
                        '$.stage_4_rescue_pass', ?
                    )
                    WHERE id = ?
                """, (pass_used, weapon_id))
            except Exception as e:
                log.warning(f"Could not update composition_trace for mythological rescue {weapon_id}: {e}")

            mythological_log.write(json.dumps({
                "weapon_id": weapon_id,
                "canonical_name": canonical_name,
                "source_library": source_library,
                "pass_used": pass_used,
                "range_class": range_class,
                "geometry_class": geometry_class,
                "tempo_class": tempo_class,
                "attribute_class": attribute_class,
                "confidence": confidence,
                "sim_viable": props["sim_viable"],
                "sim_viability_notes": props["sim_viability_notes"],
                "rep_audit": "mode_bc_check_needed" if "fictional" in (row_dict.get("structured_properties") or "").lower() else "clean",
            }) + "\n")

        if i % 200 == 0:
            conn.commit()
            log.info(f"Progress: {i}/{len(rows)} rows processed; inserted={stats['inserted']} errors={stats['errors']}")

    conn.commit()
    ambiguous_log.close()
    mythological_log.close()

    log.info("=== Population complete ===")
    log.info(f"  Total v1_scope rows: {len(rows)}")
    log.info(f"  Pass 1 (typed heuristic): {stats['pass1_typed']}")
    log.info(f"  Pass 2 (weapon_type lookup): {stats['pass2_weapon_type']}")
    log.info(f"  Pass 2b (odin-army-tradoc prescreen): {stats['pass2b_odin_prescreen']}")
    log.info(f"  Pass 3 (LLM judge): {stats['pass3_llm']}")
    log.info(f"  Pass 3 (component default): {stats['pass3_component_default']}")
    log.info(f"  LLM low-confidence (<0.6): {stats['llm_low_confidence']}")
    log.info(f"  Mythological-NULL rescue: {stats['mythological_rescue']}")
    log.info(f"  Inserted: {stats['inserted']}")
    log.info(f"  Errors: {stats['errors']}")

    # Run cheapest-refuting-tests
    log.info("\n=== Cheapest-Refuting-Tests ===")

    # CRT-1: per-axis attribute distribution
    cur.execute("""
        SELECT wsp.primary_stat, COUNT(*) as n,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM weapon_sim_props) as pct
        FROM weapon_sim_props wsp
        GROUP BY wsp.primary_stat
        ORDER BY n DESC
    """)
    attr_dist = cur.fetchall()
    log.info("Attribute distribution:")
    int_wis_pct = 0.0
    for row in attr_dist:
        log.info(f"  {row[0]}: {row[1]} ({row[2]:.1f}%)")
        if row[0] in ("INT", "WIS"):
            int_wis_pct += row[2]
    log.info(f"  INT+WIS combined: {int_wis_pct:.1f}%")
    if int_wis_pct < 10.0:
        log.error("CRT-1 FAIL: INT+WIS combined < 10% — methodology under-assigns caster attributes — REVISE BEFORE COMMIT")
    elif int_wis_pct < 12.0:
        log.warning(f"CRT-1 WARN: INT+WIS combined {int_wis_pct:.1f}% — below 12% threshold; consider revision")
    else:
        log.info(f"CRT-1 PASS: INT+WIS combined {int_wis_pct:.1f}% >= 12%")

    # CRT-2: damage amplitude ratio distribution
    cur.execute("""
        SELECT
          CASE
            WHEN damage_amplitude_max / damage_amplitude_min < 1.9 THEN 'flat'
            WHEN damage_amplitude_max / damage_amplitude_min < 4.5 THEN 'variable'
            ELSE 'spiky'
          END as amplitude_bin,
          COUNT(*) as n
        FROM weapon_sim_props
        WHERE damage_amplitude_min > 0
        GROUP BY 1
    """)
    amp_dist = cur.fetchall()
    log.info("Damage amplitude bin distribution:")
    amp_total = sum(r[1] for r in amp_dist)
    for row in amp_dist:
        pct = row[1] * 100.0 / amp_total if amp_total > 0 else 0
        log.info(f"  {row[0]}: {row[1]} ({pct:.1f}%)")
        if pct > 60.0:
            log.warning(f"CRT-2 WARN: {row[0]} amplitude bin at {pct:.1f}% > 60% ceiling")

    # CRT-3: range distribution
    cur.execute("""
        SELECT wke.proxy_range_class, COUNT(*) as n,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1) as pct
        FROM weapon_knowledge_entries wke
        WHERE wke.v1_scope = 1 AND wke.proxy_range_class IS NOT NULL
        GROUP BY wke.proxy_range_class
        ORDER BY n DESC
    """)
    range_dist = cur.fetchall()
    log.info("Range distribution (post-tagging, non-NULL):")
    for row in range_dist:
        log.info(f"  {row[0]}: {row[1]} ({row[2]:.1f}%)")

    # CRT-4: NULL check on new columns
    cur.execute("""
        SELECT COUNT(*) FROM weapon_sim_props
        WHERE damage_amplitude_min IS NULL OR damage_amplitude_max IS NULL
    """)
    null_amp = cur.fetchone()[0]
    if null_amp > 0:
        log.error(f"CRT-4 FAIL: {null_amp} rows have NULL damage_amplitude_min/max")
    else:
        log.info("CRT-4 PASS: all rows have non-NULL damage_amplitude_min/max")

    conn.close()
    return stats

if __name__ == "__main__":
    log.info("=== Cycle 10 Stage 4 — weapon_sim_props population ===")
    log.info(f"DB: {DB_PATH}")
    log.info(f"Start: {datetime.now().isoformat()}")
    stats = run_population()
    log.info(f"End: {datetime.now().isoformat()}")
    # Exit 1 if errors
    if stats["errors"] > 0:
        sys.exit(1)
