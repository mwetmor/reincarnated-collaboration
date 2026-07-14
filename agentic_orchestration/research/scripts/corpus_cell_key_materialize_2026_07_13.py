#!/usr/bin/env python3
"""
corpus_cell_key_materialize_2026_07_13.py

Materialize the ratified strict-13 cell key (coordinate-register-2026-07-13.md §6.1)
into corpus.db so gamora can run dedup v1 (strict GROUP BY cell_key).

Dispatch: agentic_orchestration/dispatches/2026-07-13-elrond-cell-key-materialization.md
Spec:     agentic_orchestration/gandalf/design-inputs/cell-key-materialization-elrond-handoff-2026-07-13.md
Canon:    canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md  §3 / §3A / §3A.1 / §3B / §6.1 / §7 / §8

WHAT THIS BUILDS (all ADDITIVE — never overwrites existing columns):
  4 new keyed columns on canon_engine_key:
    ctrl_function   ∈ {hard-stop,stun,taunt,fear,blind,knockback,expose,hex,silence,none,unknown}
    economy_model   ∈ {spend,cooldown,generator-spender,reserve,self-cost,finite,free,unknown} + literal COMPOUNDS
    activation_val  ∈ {active,triggered,unknown}
    dependency_val  ∈ {one-shot,build→spend,apply→detonate,unknown}
  1 display column (OUT of the cell key):
    resource_verbatim  (1:1 verbatim from economy family)
  1 serialized key column:
    cell_key  (canonical ordered 13-tuple; #5 = two slots; unknown/blank = literal; combat-kit rows only)

GUARDRAILS (non-negotiable — handoff §67-72):
  1. Strict exact-match FIRST — never pre-coarsen the key.
  2. Unknown/blank = its own literal value, never coalesced (never-merge-on-absence).
  3. #5 = treatment AND function (two slots in the tuple).
  4. Hybrid economy models keyed as literal COMPOUNDS, never collapsed.
  5. resource_verbatim is 1:1-preserved lineage — verbatim from source, OUT of cell_key.
  6. economy_model is ADDITIVE — do NOT touch econ_status / econ_meter_type.
  7. Does NOT run dedup (gamora's separate blocked dispatch).

IDEMPOTENT: re-runnable to byte-identical state. Additive columns are created IF NOT
present; all rows are recomputed from committed source (probe_facts / mech_note / the 9
already-present coord columns) every run. Raw columns untouched.

D6 rebuild slot: runs AFTER corpus_fold12_2026_07_13.py.
"""

import json
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "curated" / "corpus.db"

# --------------------------------------------------------------------------------------
# COORD #5b — ctrl_function derivation (§3)
# --------------------------------------------------------------------------------------
# §3 splits "ailment" into TWO concepts:
#   Layer-1 CONTROL   = crowd-control, kit-designed, ELEMENT-NEUTRAL  → Class A key (this column)
#   Layer-2 ELEMENTAL = damage-type debuff / DoT, element-INHERENT   → Class B emission (NOT here)
# The corpus `control.ailments` array mixes both vocabularies. We map ONLY the Layer-1
# tokens to the element-neutral function enum; Layer-2 (damage-DoT) tokens contribute NO
# control function. `slow` is soft-CC BELOW the §3 enum granularity — no enum slot — so it
# does not set a function either (documented steward call; see log). A kit with only
# Layer-2 and/or `slow` tokens keys ctrl_function='none'.
#
# Enum (§3, +'none' for pure-damage, +'unknown' literal for genuine absence):
#   {hard-stop, stun, taunt, fear, blind, knockback, expose, hex, silence, none, unknown}
#
# AILMENT-TOKEN -> FUNCTION map. Tokens absent from this map are Layer-2 elemental (no fn).
AILMENT_TO_FUNCTION = {
    # hard-stop family (full immobilise / freeze-lock / petrify / time-stop)
    "freeze":       "hard-stop",
    "immobilize":   "hard-stop",
    "stop":         "hard-stop",
    "time-stop":    "hard-stop",
    "instant-kill": "hard-stop",   # delete/instant-kill = terminal hard-stop (removal)
    "delete":       "hard-stop",
    # stun family (brief interrupt)
    "stun":         "stun",
    "stagger":      "stun",
    # taunt
    "taunt":        "taunt",
    # fear
    "fear":         "fear",
    # blind
    "blind":        "blind",
    # knockback family (displacement)
    "knockback":    "knockback",
    "pull":         "knockback",
    "drag":         "knockback",
    # expose / damage-amp family (armor-break, exposed, deflect-debuffs, chaos-exposure)
    "armor-break":  "expose",
    "exposed":      "expose",
    "chaos-exposure": "expose",
    "necrotic-weakness": "expose",
    "life-reduction": "expose",
    "deflect":      "expose",       # deflect = defense-shred exposure (control kits carry it as core)
    # hex / curse family
    "curse":        "hex",
    "curse-stacks": "hex",
    "doom":         "hex",
    "wither":       "hex",          # wither = curse-family chaos-defense-shred stacking hex (PoE)
    "chaos-debuff": "hex",
    "void-corruption": "hex",
    "time-rot":     "hex",
    "darkness-stacks": "hex",
    "drain":        "hex",          # drain = life/resource curse-drain
    "maul-wound":   "hex",          # persistent maiming debuff
    # silence  (no source token observed; reserved slot)
    # -- Layer-2 elemental (NO control function): burn ignite poison bleed chill shock
    #    electrify explosion acid-slow aether-slow roar-slow slow-tornado slow  → not mapped
}

# Priority order when a kit carries multiple Layer-1 function tokens.
# Hard-stop is the strongest identity signal; expose/hex are soft-shred riders → lowest.
FUNCTION_PRIORITY = [
    "hard-stop", "taunt", "fear", "silence", "blind", "knockback", "stun", "expose", "hex",
]

CTRL_FUNCTION_ENUM = set(FUNCTION_PRIORITY) | {"none", "unknown"}


def derive_ctrl_function(ctrl_treatment, control_facts):
    """control_facts = the parsed control family dict, or None if absent."""
    if control_facts is None:
        return "unknown"  # genuine absence (7 mint kits w/o probe facts) — never coalesce
    ailments = control_facts.get("ailments") or []
    matched = []
    for a in ailments:
        fn = AILMENT_TO_FUNCTION.get(a)
        if fn:
            matched.append(fn)
    if not matched:
        # No Layer-1 control token. Pure-damage or Layer-2-only or slow-only kit → 'none'.
        return "none"
    # Pick highest-priority matched function.
    for fn in FUNCTION_PRIORITY:
        if fn in matched:
            return fn
    return "none"


# --------------------------------------------------------------------------------------
# COORD #7 — economy_model derivation (§3B) + resource_verbatim (aux display)
# --------------------------------------------------------------------------------------
# Raw economy.model token -> 7-value consolidation (handoff map §39-52).
# Hybrids (containing '+') are kept as LITERAL COMPOUNDS of the mapped parts (guardrail 4).
RAW_MODEL_MAP = {
    "spend":     "spend",
    "cooldown":  "cooldown",
    "meter":     "generator-spender",  # carries {continuous·combo·stack} as sub-annotation, not a fork
    "reserve":   "reserve",
    "channel":   "reserve",            # §3B de-conflict: commit=channel lives on #11
    "self-cost": "self-cost",
    "recipe":    "finite",
    "ammo":      "finite",
    "harvest":   "finite",
    "charges":   "finite",
    "corpses":   "finite",
    "proc":      "free",               # §3B de-conflict: activation=triggered lives on #12
    # 'draft' handled explicitly below (spec-gap: NOT a consumable-input finite — see log)
    # 'other' -> 'free' residual only when the resource is genuinely 'no economy'; else 'unknown'
    # 'unknown' -> 'unknown' literal (conservative)
}

# 'other'-token resource_verbatim strings that are genuinely NO-ECONOMY (→ free residual).
# All other 'other' rows stay 'unknown' literal (conservative; never invents a model).
OTHER_AS_FREE = {"none", "stamina/none"}

ECONOMY_MODEL_PURE_ENUM = {
    "spend", "cooldown", "generator-spender", "reserve", "self-cost", "finite", "free", "unknown",
}


def consolidate_one_model(tok):
    """Map ONE raw model token to a 7-value (no hybrid handling here)."""
    if tok in RAW_MODEL_MAP:
        return RAW_MODEL_MAP[tok]
    if tok == "draft":
        # SPEC GAP (flagged): handoff says draft→finite low-confidence-confirm. The 2 draft rows
        # are roguelite draft/offer-pool BUILD-SELECTION economies (VS-style), NOT consumable
        # inputs. Keeping as 'unknown' literal is the conservative never-invent choice pending
        # gandalf ruling. (See completion record / MIGRATION for the flag.)
        return "unknown"
    if tok == "unknown":
        return "unknown"
    # 'other' or any unrecognised token resolved by caller with resource context.
    return None  # signal caller to resolve with resource_verbatim


def derive_economy(economy_facts):
    """Return (economy_model, resource_verbatim). economy_facts = dict or None."""
    if economy_facts is None:
        return "unknown", None  # 7 mint kits without economy probe facts
    raw = economy_facts.get("model")
    rv = economy_facts.get("resource_verbatim")
    if raw is None or raw == "":
        return "unknown", rv
    # Hybrid: literal compound of mapped parts (guardrail 4).
    if "+" in raw:
        parts = [p.strip() for p in raw.split("+")]
        mapped = []
        for p in parts:
            m = consolidate_one_model(p)
            if m is None:
                # 'other'/unrecognised inside a compound → resolve conservatively
                m = "free" if (rv in OTHER_AS_FREE) else "unknown"
            mapped.append(m)
        return "+".join(mapped), rv
    # Pure token.
    m = consolidate_one_model(raw)
    if m is None:  # raw == 'other' or unrecognised
        m = "free" if (rv in OTHER_AS_FREE) else "unknown"
    return m, rv


# --------------------------------------------------------------------------------------
# COORD #12 — activation_val (§3A / §3A.1)  &  #13 — dependency_val (§3A)
# --------------------------------------------------------------------------------------
# activation ∈ {active, triggered, unknown}. §3A.1 discriminator: intrinsic-trigger→triggered;
#   gear-granted reactivity→active (base kit). Tell in mech_note: "on-crit/on-hit/on-timer/
#   autonomous/cast-on-X gem/proc" that is the kit's CORE delivery → triggered; a "helm/unique
#   IS the build" reactivity → active. Default (no trigger tell) = active (player pulls trigger).
TRIGGER_TELLS = [
    "cast-on-crit", "cast on crit", "on-crit", "on crit", "coc",
    "on-hit", "on hit", "spell-on-attack", "on-attack", "on attack",
    "autonomous", "autobomber", "automatically", "fire autonomously",
    "on a timer", "on-timer", "ticking", "tick ", "ticks ",
    "poet's pen", "spell cascade", "trigger", "triggered", "proc ", "procs ",
    "on-kill", "on kill", "on-block", "on block",
]
# Gear-granted reactivity that does NOT count as intrinsic (→ active). If BOTH a trigger tell
# and a strong gear-source tell appear, §3A.1 says the base kit is 'active' (the reactivity is
# an equippable operator, not cell-identity).
GEAR_SOURCE_TELLS = [
    "the helm is the build", "helm is the build", "andariel", "unique item grants",
    "bespoke unique", "the item grants", "loot artifact",
]

# dependency ∈ {one-shot, build→spend, apply→detonate, unknown}.
#   apply→detonate : plant/apply then pop  (traps, mines, detonate-dead, mark-consume, corpse-explode)
#   build→spend    : accumulate-then-release (charge-stack, combo/generator ramp, stack-then-spend)
#   one-shot       : fire-and-resolve (default)
DETONATE_TELLS = [
    "detonate", "corpse explos", "corpse explod", "explode a corpse", "explodes a corpse",
    "trap", "mine ", "mines", "sentry", "totem", "plant", "seismic", "consume the mark",
    "mark-consume", "apply then", "curse then", "primed", "bloom", "seed then", "delayed kill",
    "delayed detonation", "detonat",
]
BUILD_SPEND_TELLS = [
    "charge-stack", "charge up", "charge-up", "charges up", "build elemental charges",
    "build up", "build-up", "ramp", "stacking", "stacks up", "combo point", "combo-point",
    "generator", "spender", "accumulate", "build via", "build toward", "build-toward",
    "wind up", "wind-up", "finishers consume", "finisher consume", "consume", "spend via",
    "stack then", "stacks then",
]


def _has_any(text, tells):
    return any(t in text for t in tells)


def derive_activation(mech_note, economy_facts):
    """§3A.1 discriminator. mech_note may be None/'' (7 mint kits)."""
    if not mech_note:
        return "unknown"
    t = mech_note.lower()
    # economy=proc is an activation=triggered tell (§3B de-conflict) IF intrinsic.
    proc_econ = bool(economy_facts and economy_facts.get("model") == "proc")
    has_trigger = _has_any(t, TRIGGER_TELLS) or proc_econ
    has_gear = _has_any(t, GEAR_SOURCE_TELLS)
    if has_trigger and not has_gear:
        return "triggered"
    # gear-granted reactivity OR no trigger tell → active (player pulls the trigger each cast)
    return "active"


def derive_dependency(mech_note):
    if not mech_note:
        return "unknown"
    t = mech_note.lower()
    if _has_any(t, DETONATE_TELLS):
        return "apply→detonate"
    if _has_any(t, BUILD_SPEND_TELLS):
        return "build→spend"
    return "one-shot"


# --------------------------------------------------------------------------------------
# cell_key serialization (§6.1 / handoff §56-60)
# --------------------------------------------------------------------------------------
# Canonical ordered 13-tuple, coord order 1..13, #5 = TWO slots (treatment, function):
#   1  mob_policy_while_casting   (canon_engine_key)
#   2  delivery_value             (canon_engine_key)
#   3  amp_val                    (canon_corpus)
#   4  geometry_value             (canon_engine_key)
#   5a ctrl_treatment             (canon_engine_key)
#   5b ctrl_function              (canon_engine_key — NEW)
#   6  def_bin                    (canon_engine_key)
#   7  economy_model              (canon_engine_key — NEW)
#   8  proxy_val                  (canon_corpus)
#   9  range_val                  (canon_corpus)
#   10 tempo_val                  (canon_corpus)
#   11 commit_val                 (canon_corpus)
#   12 activation_val             (canon_engine_key — NEW)
#   13 dependency_val             (canon_engine_key — NEW)
# Unknown/blank = literal value, never coalesced. A genuinely-absent (SQL NULL / '') slot
# becomes the literal token 'blank'; a source that itself carries 'unknown' stays 'unknown'.
CELL_KEY_ORDER = [
    "mob_policy_while_casting",  # 1
    "delivery_value",            # 2
    "amp_val",                   # 3
    "geometry_value",            # 4
    "ctrl_treatment",            # 5a
    "ctrl_function",             # 5b
    "def_bin",                   # 6
    "economy_model",             # 7
    "proxy_val",                 # 8
    "range_val",                 # 9
    "tempo_val",                 # 10
    "commit_val",                # 11
    "activation_val",            # 12
    "dependency_val",            # 13
]


def slot(v):
    """A NULL / empty slot becomes literal 'blank'; a source 'unknown' stays 'unknown'.
    Both are literal values — the never-merge-on-absence guarantee (guardrail 2)."""
    if v is None:
        return "blank"
    s = str(v).strip()
    if s == "":
        return "blank"
    return s


def serialize_cell_key(row):
    return "|".join(slot(row[c]) for c in CELL_KEY_ORDER)


# --------------------------------------------------------------------------------------
# Migration
# --------------------------------------------------------------------------------------
def column_exists(conn, table, col):
    return col in {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def add_columns(conn):
    adds = [
        ("canon_engine_key", "ctrl_function", "TEXT"),
        ("canon_engine_key", "economy_model", "TEXT"),
        ("canon_engine_key", "activation_val", "TEXT"),
        ("canon_engine_key", "dependency_val", "TEXT"),
        ("canon_engine_key", "resource_verbatim", "TEXT"),
        ("canon_engine_key", "cell_key", "TEXT"),
    ]
    for table, col, typ in adds:
        if not column_exists(conn, table, col):
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
            print(f"  + added {table}.{col} {typ}")
        else:
            print(f"  = {table}.{col} already present (idempotent)")


def parse_facts(row):
    if row is None:
        return None
    try:
        return json.loads(row)
    except (json.JSONDecodeError, TypeError):
        return None


def main():
    if not DB.exists():
        sys.exit(f"corpus.db not found at {DB}")
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row

    print(f"== corpus_cell_key_materialize == {DB}")
    add_columns(conn)

    # Pull all combat-kit rows joined to their probe facts + mech_note + the 5 canon_corpus coords.
    rows = conn.execute("""
        SELECT k.kit_id, k.ctrl_treatment,
               cc.mech_note,
               (SELECT facts_json FROM canon_probe_facts p WHERE p.kit_id=k.kit_id AND p.family='control')  AS control_json,
               (SELECT facts_json FROM canon_probe_facts p WHERE p.kit_id=k.kit_id AND p.family='economy')  AS economy_json
        FROM canon_engine_key k
        JOIN canon_corpus cc ON cc.kit_id = k.kit_id
        WHERE k.row_class = 'combat-kit'
    """).fetchall()

    n = 0
    for r in rows:
        control_facts = parse_facts(r["control_json"])
        economy_facts = parse_facts(r["economy_json"])
        ctrl_function = derive_ctrl_function(r["ctrl_treatment"], control_facts)
        economy_model, resource_verbatim = derive_economy(economy_facts)
        activation_val = derive_activation(r["mech_note"], economy_facts)
        dependency_val = derive_dependency(r["mech_note"])

        # enum validation (pure enums only; compounds/'+' allowed for economy_model)
        assert ctrl_function in CTRL_FUNCTION_ENUM, f"{r['kit_id']}: bad ctrl_function {ctrl_function}"
        for part in economy_model.split("+"):
            assert part in ECONOMY_MODEL_PURE_ENUM, f"{r['kit_id']}: bad economy_model part {part}"
        assert activation_val in {"active", "triggered", "unknown"}, f"{r['kit_id']}: bad activation {activation_val}"
        assert dependency_val in {"one-shot", "build→spend", "apply→detonate", "unknown"}, \
            f"{r['kit_id']}: bad dependency {dependency_val}"

        conn.execute("""
            UPDATE canon_engine_key
            SET ctrl_function=?, economy_model=?, activation_val=?, dependency_val=?, resource_verbatim=?
            WHERE kit_id=?
        """, (ctrl_function, economy_model, activation_val, dependency_val, resource_verbatim, r["kit_id"]))
        n += 1

    # Clear the 4 new columns + cell_key on system-records (scope: combat-kit only).
    conn.execute("""
        UPDATE canon_engine_key
        SET ctrl_function=NULL, economy_model=NULL, activation_val=NULL,
            dependency_val=NULL, resource_verbatim=NULL, cell_key=NULL
        WHERE row_class='system-record'
    """)

    conn.commit()
    print(f"  populated 4+1 columns on {n} combat-kit rows")

    # ---- serialize cell_key (combat-kit only) via the cross-table join ----
    keyrows = conn.execute("""
        SELECT k.kit_id,
               k.mob_policy_while_casting, k.delivery_value, k.geometry_value,
               k.ctrl_treatment, k.ctrl_function, k.def_bin, k.economy_model,
               k.activation_val, k.dependency_val,
               cc.amp_val, cc.proxy_val, cc.range_val, cc.tempo_val, cc.commit_val
        FROM canon_engine_key k
        JOIN canon_corpus cc ON cc.kit_id = k.kit_id
        WHERE k.row_class='combat-kit'
    """).fetchall()

    for r in keyrows:
        ck = serialize_cell_key(r)
        conn.execute("UPDATE canon_engine_key SET cell_key=? WHERE kit_id=?", (ck, r["kit_id"]))
    conn.commit()
    print(f"  serialized cell_key on {len(keyrows)} combat-kit rows")

    # ---- smoke ----
    total = conn.execute("SELECT count(*) FROM canon_engine_key WHERE row_class='combat-kit' AND cell_key IS NOT NULL").fetchone()[0]
    distinct = conn.execute("SELECT count(DISTINCT cell_key) FROM canon_engine_key WHERE row_class='combat-kit' AND cell_key IS NOT NULL").fetchone()[0]
    with_absence = conn.execute("""
        SELECT count(*) FROM canon_engine_key
        WHERE row_class='combat-kit' AND cell_key IS NOT NULL
          AND ('|'||cell_key||'|' LIKE '%|blank|%' OR '|'||cell_key||'|' LIKE '%|unknown|%')
    """).fetchone()[0]
    print("\n== SMOKE ==")
    print(f"  combat-kit rows with cell_key : {total}")
    print(f"  distinct cell_key (cells)     : {distinct}")
    print(f"  rows carrying any unknown/blank slot : {with_absence}")

    # bump schema_meta (idempotent: delete any prior 2.3 row first — table has no PK)
    conn.execute("DELETE FROM corpus_schema_meta WHERE version='2.3'")
    conn.execute("""
        INSERT INTO corpus_schema_meta (version, applied_utc, note)
        VALUES ('2.3', '2026-07-13T00:00:00Z',
        'Cell-key materialization (elrond §6.1/§8): +4 keyed cols (ctrl_function/economy_model/activation_val/dependency_val) + resource_verbatim (display, out-of-key) + cell_key (strict-13 serialization, combat-kit only, #5=2 slots, unknown/blank=literal). Additive; econ_status/econ_meter_type untouched. system-records: 4-cols+cell_key NULL (out of combat denominator). Rebuild = base + s1 + fold12 + this.')
    """)
    conn.commit()
    conn.close()
    print("\n  schema_meta bumped 2.2 -> 2.3")
    print("  DONE.")


if __name__ == "__main__":
    main()
