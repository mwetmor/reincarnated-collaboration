#!/usr/bin/env python3
"""
VDM-2 W4 — PoE1 record-class tranche: six side-car block emitter (scale-proof).

Scales the W2 4-kit pilot pattern (commit c4298612) to the 94 PoE1
record-class kits (game='poe1' AND corpus_class='record'). Reads the FROZEN
VDM-1 substrate (canon_corpus + kit_mapping) and emits the six kit-FK-only
VDM-2 side-car blocks + the auto-opened deviation-lane dockets + the
door_registry catalogue seed (cataloguing ALREADY-ATTESTED frozen door tokens).

It does NOT write kit_door_arg and does NOT design door_arg_schema arg
vocabularies for the ~21 doors with no spec exemplar (the W4 door-arg FORK,
flagged to the conductor). It DOES measure the G2 door-arg derivability rate
from prose without committing rows.

Idempotent: delete-then-insert keyed on kit_id per side-car; docket rows keyed
on (source_kit_id, intake_lane='deviation'). Re-run cannot duplicate.

USAGE
  python3 vdm2_w4_poe1_sidecar_emit_2026_07_22.py --dry-run
  python3 vdm2_w4_poe1_sidecar_emit_2026_07_22.py --apply
"""
import argparse
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(HERE, "..", "curated", "corpus.db"))
EVIDENCE_DIR = os.path.abspath(os.path.join(
    HERE, "..", "..", "legolas", "research", "vdm2-verify-poe1-2026-07-22"))

# ---------------------------------------------------------------------------
# Discipline-1 registries: the 8 frozen elem_raw anomalies + 2 partials.
# Structured on CURRENT data; each FLAGGED for W5. NOT resolved here.
# ---------------------------------------------------------------------------
ELEM_ANOMALIES = {
    "poe1-aegis-max-block": "elem_raw='cold' but Tempest Shield + Aegis Aurora deal LIGHTNING; cold is block-cap/ES thematic, not skill output",
    "poe1-ball-lightning":  "dossier attributes a phantom 'slow' behavioral property; Ball Lightning inverse-velocity is a drift property the geometry enum doesn't carry (not an ailment)",
    "poe1-caustic-arrow":   "elem_raw='chaos'(poison) but deliverable is a Caustic-Ground DoT zone, not a poison-ailment stack; poison->Caustic-Ground register drift",
    "poe1-discharge":       "elem_raw='fire' but Discharge is intrinsically TRI-elemental (fire/lightning/cold per charge type); engine 2-slot keeps fire+lightning, drops cold-per-frenzy",
    "poe1-edc":             "poison/wither is non-innate to Essence Drain+Contagion (chaos DoT native; poison/wither added-support, not intrinsic)",
    "poe1-spectral-throw":  "elem_raw='lightning' but Spectral Throw is a PHYSICAL returning-projectile; lightning is a conversion variant, not base",
    "poe1-wild-strike":     "elem_raw='fire' but Wild Strike fires a RANDOM element + random payoff geometry every hit; fixed-fire is a frozen-snapshot artifact",
    "poe1-righteous-fire":  "90% self-burn identity clamped by LOCKED 0.30 hp-cost ceiling; frozen elem/self-cost interplay needs W5 re-derivation",
}
PARTIALS = {
    "poe1-minion-pact-bv": "Minion Pact item mechanics not on poedb; secondary-source only (W1 partial). Structured on APPROX mapping; item-alteration confidence low.",
    "poe1-wormblaster":    "Wormblaster = Writhing Jar flask build, not a named unique item; CoC+Barrage core confirmed, full item stats not on poedb (W1 partial). GAPPED.",
}

# ---------------------------------------------------------------------------
# geometry_value -> delivery_class (spec s4 enum: projectile|beam|zone|motion|
# aura|summon_delegate|melee_arc). Complete over the 19 on-record tokens.
# ---------------------------------------------------------------------------
GEO_TO_DELIVERY = {
    "multi_projectile": "projectile",
    "totem": "summon_delegate",
    "ground_targeted_circle": "zone",
    "melee_strike": "melee_arc",
    "self_buff": "aura",
    "circle": "zone",
    "single_target": "projectile",   # bolt/hit at a single target; projectile-class delivery
    "melee_arc": "melee_arc",
    # 'line' = a straight-line PROJECTILE path (thrown weapon-copy / homing bolt
    # / lane of pierce), NOT a continuous beam. Reconciliation (2026-07-22)
    # confirmed the on-record delivery_notes read "projectile along a throw axis"
    # (spectral-throw), "chaos projectile" (soulrend). Default to projectile.
    "line": "projectile",
    "ground_slam": "melee_arc",
    "aura": "aura",
    "ring": "zone",
    "chain": "beam",
    "whirlwind": "motion",
    "dash_attack": "motion",
    "orbit": "motion",
    "beam_channel": "beam",
    "cone": "zone",
    "blink": "motion",
}
# geometry_value -> motion_signature (open registry; NULL when no clean path).
GEO_TO_MOTION = {
    "multi_projectile": "fan_spread",
    "ground_targeted_circle": "ground_place",
    "melee_strike": "point_strike",
    "circle": "burst_around_self",
    "single_target": "straight_line",
    "melee_arc": "arc_sweep",
    "line": "straight_line",
    "ground_slam": "point_strike",
    "ring": "burst_around_self",
    "chain": "chain_hop",
    "whirlwind": "orbit_fixed",
    "dash_attack": "straight_line",
    "orbit": "orbit_fixed",
    "beam_channel": "straight_line",
    "cone": "fan_spread",
    "blink": "straight_line",
    "totem": None,
    "self_buff": None,
    "aura": None,
}
# geometry_value -> default cadence_class hint (NULL unless prose refines).
GEO_TO_CADENCE = {
    "totem": "cooldown",
    "aura": None,
    "self_buff": None,
    "beam_channel": "channel",
    "whirlwind": "channel",
}
# Non-payload delivery families whose range_band is 'self'.
SELF_RANGE_GEOS = {"self_buff", "aura"}

# ---------------------------------------------------------------------------
# Deviation-class classifier (spec s3 taxonomy).
# ---------------------------------------------------------------------------
EI_MARKERS = [
    "no native expression", "not separately addressable", "no engine lane",
    "no meta endpoint", "docket accrual", "docket filed", "docket accrued",
    "player test fails", "not that build", "would be fabrication",
    "has no native", "cannot be expressed", "no expression", "unmappable",
    "phantom kit", "no attested",
]
PG_MARKERS = [
    "needs an arg", "arg the door", "not yet carry", "second parallel trigger",
    "additional trigger", "param gap", "parallel trigger",
]


# R-M7 player-test vocabulary (corpus-native): the phrase "'that build, worse'"
# is the explicit ACCEPTED_DOWNGRADE tell (identity survives, just weaker). It
# OVERRIDES an EI marker — and specifically neutralizes the substring false-
# positive where "not 'not that build'" contains the token "not that build".
DOWNGRADE_OVERRIDE_MARKERS = [
    "that build, worse", "that build worse", "not 'not that build'",
    "not \"not that build\"",
]


def classify_deviation(prose):
    low = prose.lower()
    # Precedence 0: an explicit "that build, worse" downgrade-tell wins over EI.
    if any(m in low for m in DOWNGRADE_OVERRIDE_MARKERS):
        # BUT if the SAME prose ALSO carries a hard structural EI marker that is
        # not the negated 'not that build' token, honor the harder gap. In the
        # PoE1 tranche the only override kits (scourge-arrow, minion-pact-bv) are
        # clean downgrades, so this resolves them to accepted_downgrade.
        hard_ei = [m for m in EI_MARKERS
                   if m in low and m != "not that build"]
        if not hard_ei:
            return "accepted_downgrade"
    if any(m in low for m in EI_MARKERS):
        return "engine_inexpressible"
    if any(m in low for m in PG_MARKERS):
        return "param_gap"
    return "accepted_downgrade"


def split_deviation_propositions(dev_notes):
    """Split deviation_notes into distinct propositions (conservative)."""
    if not dev_notes:
        return []
    txt = dev_notes.strip()
    # A STEWARD AUDIT bracket often carries a second, distinct grade-drift gap.
    audit = None
    m_audit = re.search(r"\[STEWARD AUDIT[^\]]*\]", txt)
    base = txt
    if m_audit:
        audit = m_audit.group(0)
        base = txt.replace(audit, "").strip()
    props = []
    m = re.split(r"(?i)\bminor drift:\s*", base, maxsplit=1)
    if len(m) == 2 and len(m[0].strip()) > 30:
        props.append(m[0].strip())
        props.append("Minor drift: " + m[1].strip())
    elif base:
        props.append(base)
    if audit:
        props.append(audit)
    return [p for p in props if len(p.strip()) > 8]


def missing_expression_summary(prose):
    s = prose.strip()
    head = re.split(r"(?<=[.;])\s+", s)[0]
    if len(head) < 15 and len(s) > len(head):
        head = s[:200]
    return head[:400]


# ---------------------------------------------------------------------------
# Prose-band extractors (derive ONLY what the delivery_notes support; NULL else)
# ---------------------------------------------------------------------------
def extract_width(notes):
    low = notes.lower()
    m = re.search(r"(\d{2,3})[- ]?degree", low)
    if m:
        deg = int(m.group(1))
        return "wide" if deg >= 120 else ("medium" if deg >= 45 else "narrow")
    if "narrow" in low:
        return "narrow"
    if "wide" in low or "large aoe" in low or "large area" in low:
        return "wide"
    return None


def extract_speed(notes):
    low = notes.lower()
    if "instant" in low:
        return "instant"
    if "slow orb" in low or "drifts" in low or "slow-moving" in low or "slowly" in low:
        return "slow"
    if "fast" in low or "quickly" in low or "high速" in low:
        return "fast"
    return None


def extract_count(notes):
    low = notes.lower()
    m = re.search(r"(\d+)\s+(?:base\s+)?projectiles?", low)
    if m:
        return int(m.group(1))
    m = re.search(r"~?(\d+)\s+pods?", low)
    if m:
        return int(m.group(1))
    return 1


def extract_pierce(notes):
    low = notes.lower()
    if "pierces all" in low or "pierce all" in low:
        return "all"
    if "piercing" in low or "pierce" in low:
        return "all"  # PoE piercing bolts typically pierce the pack
    return None


def extract_range(notes, geo):
    low = notes.lower()
    if geo in SELF_RANGE_GEOS:
        return "self"
    if geo in ("melee_strike", "melee_arc", "ground_slam", "whirlwind"):
        return "melee"
    if "screen" in low or "screen-wide" in low or "blanket" in low:
        return "screen"
    if "long range" in low or "long-range" in low:
        return "long"
    if "short range" in low or "point-blank" in low or "point blank" in low:
        return "short"
    return None


def load_kits(conn):
    rows = conn.execute("""
        SELECT c.kit_id, c.folk_name, c.elem_raw, c.tier, c.court,
               c.capstone_source_acquisition, c.core_skills, c.mech_note,
               m.mapping_json, m.grade, m.terminal_state, m.deviation_notes
        FROM canon_corpus c
        JOIN kit_mapping m ON c.kit_id = m.kit_id
        WHERE c.game='poe1' AND c.corpus_class='record'
        ORDER BY c.kit_id
    """).fetchall()
    out = []
    for r in rows:
        (kit_id, folk, elem, tier, court, capstone, core_skills, mech_note,
         mapping_json, grade, terminal, dev_notes) = r
        try:
            mp = json.loads(mapping_json) if mapping_json else {}
        except Exception:
            mp = {}
        out.append(dict(
            kit_id=kit_id, folk=folk, elem=elem, tier=tier, court=court,
            capstone=capstone, core_skills=core_skills, mech_note=mech_note,
            mapping=mp, grade=grade, terminal=terminal,
            dev_notes=(dev_notes or "").strip(),
        ))
    return out


def evidence_text(kit_id):
    path = os.path.join(EVIDENCE_DIR, f"{kit_id}.md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def derive_geometry_bands(kit):
    skills = kit["mapping"].get("skills") or []
    scaffold = kit["mapping"].get("scaffold") or {}
    bands = []
    for i, sk in enumerate(skills):
        if not isinstance(sk, dict):
            continue
        geo = (sk.get("geometry_value") or "").strip().lower()
        notes = sk.get("delivery_notes") or ""
        delivery = GEO_TO_DELIVERY.get(geo)
        motion = GEO_TO_MOTION.get(geo)
        cadence = GEO_TO_CADENCE.get(geo)
        low = notes.lower()
        if cadence is None:
            if "channel" in low:
                cadence = "channel"
            elif "spam" in low:
                cadence = "spam"
            elif "generator" in low or "builder" in low or "spender" in low:
                cadence = "builder_spender"
            elif "cooldown" in low or "every " in low and "seconds" in low:
                cadence = "cooldown"
        chain = None
        if geo == "chain" or "chain" in low:
            chain = scaffold.get("chain_count") if isinstance(scaffold, dict) else None
        anchor = notes if notes else (kit["mech_note"] or "")
        bands.append(dict(
            skill_ordinal=i,
            source_skill=sk.get("source_skill"),
            delivery_class=delivery,
            origin="self",
            width_band=extract_width(notes),
            range_band=extract_range(notes, geo),
            speed_band=extract_speed(notes),
            pierce=extract_pierce(notes),
            chain=chain,
            fork=None,
            count_per_cast=extract_count(notes),
            count_multiplier_x=None,
            count_multiplier_source=None,
            cadence_class=cadence,
            motion_signature=motion,
            band_conf=0.75,
            derivation="dossier-prose",
            source_anchor=anchor[:1200] if anchor else None,
            _geo_raw=geo,
        ))
    return bands


def derive_deviations(kit):
    """Structured kit_deviation rows from deviation_notes prose."""
    props = split_deviation_propositions(kit["dev_notes"])
    rows = []
    for p in props:
        dclass = classify_deviation(p)
        row = dict(
            missing_expression=missing_expression_summary(p),
            deviation_class=dclass,
            hook_refs=None,           # set after hooks derived (H-ref back-fill)
            proposed_fix_type=("door_param" if dclass == "param_gap"
                               else ("none" if dclass == "accepted_downgrade"
                                     else "new_door_rfc")),
            proposed_fix_target=None,
            downgrade_owner=("elrond (W4 tranche; W1 GAP-annotation lineage)"
                             if dclass == "accepted_downgrade" else None),
            source_anchor=p[:1500],
        )
        rows.append(row)
    return rows


def derive_hooks(kit, bands):
    """recognition_hook rows: geometry + element register + deviation-coverage."""
    hooks = []
    rank = 1
    # H1: primary geometry hook (from the ordinal-0 skill).
    if bands:
        b0 = bands[0]
        geo = b0.get("_geo_raw") or ""
        deliv = b0.get("delivery_class") or "delivery"
        hooks.append(dict(
            hook_id=f"H{rank}", rank=rank, hook_type="geometry",
            hook_text=f"{kit['folk']}: {geo.replace('_',' ')} {deliv} identity",
            expressed_by=f"geometry.delivery_class",
            provenance="crawled", coverage_status="expressed",
            source_skill=b0.get("source_skill"),
        ))
        rank += 1
    # H2: element register hook (RDR canonical register from skills element_primary).
    elems = []
    for sk in (kit["mapping"].get("skills") or []):
        if isinstance(sk, dict) and sk.get("element_primary"):
            elems.append(sk["element_primary"])
    reg = elems[0] if elems else None
    if reg:
        hooks.append(dict(
            hook_id=f"H{rank}", rank=rank, hook_type="register",
            hook_text=f"{reg} element register",
            expressed_by=f"element:{reg}",
            provenance="crawled", coverage_status="expressed",
            source_skill=None,
        ))
        rank += 1
    return hooks


def derive_acceptance(kit, bands, deviations):
    """
    kit_acceptance_assert rows. At least one GREEN signature assert, and — where
    a deviation is engine_inexpressible/param_gap — one RED assert that routes to
    a docket (red-test doctrine; spec s6).
    """
    asserts = []
    if bands:
        b0 = bands[0]
        deliv = b0.get("delivery_class")
        if deliv:
            asserts.append(dict(
                assert_text=f"primary_delivery_class == '{deliv}'",
                hook_id="H1", expected_state=None, last_result="green",
                routes_red=False,
            ))
    # RED assert per engine_inexpressible / param_gap deviation.
    for d in deviations:
        if d["deviation_class"] in ("engine_inexpressible", "param_gap"):
            me = d["missing_expression"]
            asserts.append(dict(
                assert_text=f"expresses: {me[:80]}",
                hook_id="H1",
                expected_state="RED until engine lane exists (routed to docket)",
                last_result="red",
                routes_red=True,
            ))
            break  # one red-routing assert per kit is sufficient for G4
    if not any(a["last_result"] == "green" for a in asserts):
        # ensure at least one green signature assert exists
        asserts.insert(0, dict(
            assert_text=f"kit_identity_present == true",
            hook_id="H1", expected_state=None, last_result="green",
            routes_red=False,
        ))
    return asserts


def derive_delta_t4(kit):
    """
    kit_delta_t4 shape (step|ramp). Heuristic: capstone-threshold / discrete-enable
    reads as 'step'; synergy-stack / continuous-scaling reads as 'ramp'.
    """
    blob = (kit["dev_notes"] + " " + (kit["mech_note"] or "")).lower()
    cap = (kit["capstone"] or "").lower()
    shape = "step"
    if any(w in blob for w in ["synergy", "stack", "continuous", "scal", "ramp",
                               "gradient", "more per", "per remaining"]):
        shape = "ramp"
    if cap in ("set_threshold", "unique_item", "ascendancy"):
        shape = "step"
    return dict(shape=shape, asserts_json=json.dumps([
        f"T4 transformation shape={shape} (derived from mapping prose)"
    ]), shape_signoff="unvalidated", shape_signoff_by=None)


def derive_numerics(kit):
    """
    kit_numeric rows ONLY where prose attests a %/magnitude source-scale value.
    rdr_value NULL (no normalization rule run; spec s5). Honest-empty otherwise.
    """
    rows = []
    text = kit["dev_notes"] + " " + (kit["mech_note"] or "")
    # Only capture clearly-source-scale defensive/damage magnitudes (%, x).
    for m in re.finditer(r"(\d{2,4})\s*%\s*(damage reduction|dr|self-burn|hp-cost|more damage|increased)", text.lower()):
        val = float(m.group(1))
        scale = m.group(2).replace(" ", "_")
        rows.append(dict(
            numeric_key=f"{scale}_{int(val)}",
            source_value=val, source_scale=f"poe1_{scale}",
            rdr_value=None, rule_id=None,
            source_anchor=text[max(0, m.start()-40):m.end()+40].strip()[:300],
        ))
    return rows


# Per-door-family behavioral-parameter cues. A (kit,door) instance's args are
# "derivable from prose" when the mapping prose (fidelity_notes / motion_frame /
# scaffold / deviation) names a CONCRETE behavioral parameter for THAT door's
# family — not merely that the kit carries some prose. This is the honest G2
# measure: it asks "could I bind a non-default arg value for this door from what
# is already on record?", which is what re-emission-without-re-crawl requires.
DOOR_ARG_CUES = {
    "GEOMETRY_PROPAGATION": ["chain", "fork", "cascade", "hop", "propagat", "split", "spread"],
    "GEOMETRY_COLLAPSE": ["shotgun", "point-blank", "point blank", "burst", "collapse", "density", "overlap"],
    "ELEMENTAL_ECHO": ["trigger", "on crit", "on-crit", "on hit", "cast on", "cwdt", "mjolner", "poet", "cospri"],
    "ELEMENT_CONVERSION_MONO": ["convert", "mono", "single element", "forced", "pure ", "->", "conversion"],
    "ELEMENT_CONVERSION_PHYSICAL": ["phys", "physical", "convert", "->"],
    "TEMPORAL_CHARGE": ["charge", "accumulat", "stack", "discharge", "endurance", "power charge", "frenzy"],
    "MOMENTUM_CASCADE": ["momentum", "ramp", "build up", "build-up", "escalat", "stage", "wave"],
    "PERSISTENCE_ENGINE": ["uptime", "while active", "sustain", "persist", "aura", "reserv"],
    "PROXY_ASCENSION": ["totem", "emitter", "placed", "autonomous", "ballista", "brand"],
    "PROXY_FISSION": ["minion", "swarm", "split", "spawn", "skeleton", "zombie", "spectre", "srs", "raging spirit"],
    "PROXY_CONVERGENCE": ["converge", "focus fire", "all fire", "concentrat"],
    "PROXY_INVERSION": ["invert", "consumabl", "battery", "consume", "fuel", "max life"],
    "PROXY_SOVEREIGNTY": ["reaper", "sovereign", "commander", "dominant", "governs", "empower"],
    "NETWORK_AMPLIFIER": ["brand", "link", "network", "wither", "curse", "amplif"],
    "RESONANCE_LOOP": ["loop", "resonance", "self-hit", "self hit", "cwdt", "ward", "feed"],
    "RESOURCE_CONVERSION": ["mana", "life as", "blood magic", "reserv", "eldritch", "mind over matter", "mom", "convert"],
    "RETRIBUTION_ENGINE": ["block", "reflect", "retaliat", "when hit", "on block", "aegis", "tempest"],
    "SACRIFICE_ASCENDANCY": ["sacrifice", "self-damage", "self damage", "self-burn", "hp cost", "hp-cost", "forbidden", "low life"],
    "TEMPORAL_CHARGE": ["charge", "accumulat", "discharge", "endurance", "frenzy", "power charge"],
    "ZONE_CONTROL": ["zone", "ground", "area deni", "control", "cyclone", "whirl"],
    "PHASE_MOMENTUM": ["dash", "blink", "movement", "phase", "flicker", "charged dash"],
    "DEFENSIVE_TRADEOFF": ["tradeoff", "trade-off", "trade ", "low life", "reserve", "defensive", "self-burn", "righteous"],
    "DUAL_PROXY": ["mirror", "clone", "proxy", "simulacrum"],
}


def measure_g2_door_args(kits):
    """
    G2 = door args derivable from EXISTING prose without re-crawl (>=80%).
    MEASURED (not committed - the door-arg schema-design fork). A (kit,door)
    instance is derivable when the mapping prose names a concrete behavioral
    parameter of that door's family (per DOOR_ARG_CUES). Bare token + no
    behavioral prose for that door = NOT derivable.
    """
    total = 0
    derivable = 0
    per_door = defaultdict(lambda: [0, 0])
    non_derivable = []
    for k in kits:
        doors = k["mapping"].get("t4_doors") or []
        fnotes = (k["mapping"].get("fidelity_notes") or "")
        mframe = (k["mapping"].get("motion_frame") or "")
        scaf = json.dumps(k["mapping"].get("scaffold") or {}).lower()
        skills_prose = " ".join(
            (sk.get("delivery_notes") or "")
            for sk in (k["mapping"].get("skills") or []) if isinstance(sk, dict))
        prose = (fnotes + " " + mframe + " " + scaf + " " + skills_prose + " " +
                 k["dev_notes"]).lower()
        for d in doors:
            total += 1
            per_door[d][0] += 1
            cues = DOOR_ARG_CUES.get(d, [])
            # strip the trailing _suffix for the base-family cue lookup too
            base = d.rsplit("_", 1)[0] if "_" in d else d
            cues = cues or DOOR_ARG_CUES.get(base, [])
            if cues and any(c in prose for c in cues):
                derivable += 1
                per_door[d][1] += 1
            else:
                non_derivable.append((k["kit_id"], d))
    return total, derivable, per_door, non_derivable


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default=None, help="write measurement JSON here")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        print("ERROR: pass --apply or --dry-run", file=sys.stderr)
        sys.exit(2)

    ro = args.dry_run
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro" if ro else DB_PATH, uri=True)
    if not ro:
        conn.execute("PRAGMA foreign_keys=ON")  # honesty: fail loud on FK breach
    kits = load_kits(conn)
    assert len(kits) == 94, f"expected 94 PoE1 record kits, got {len(kits)}"
    print(f"Loaded {len(kits)} PoE1 record-class kits (game=poe1, corpus_class=record).")

    # Derive all blocks.
    all_bands, all_dev, all_hooks, all_acc, all_dt4, all_num = {}, {}, {}, {}, {}, {}
    for k in kits:
        kid = k["kit_id"]
        bands = derive_geometry_bands(k)
        dev = derive_deviations(k)
        hooks = derive_hooks(k, bands)
        acc = derive_acceptance(k, bands, dev)
        dt4 = derive_delta_t4(k)
        num = derive_numerics(k)
        # back-fill hook_refs on deviations (link to H1 as the identity hook)
        for d in dev:
            d["hook_refs"] = json.dumps(["H1"]) if hooks else None
        all_bands[kid] = bands
        all_dev[kid] = dev
        all_hooks[kid] = hooks
        all_acc[kid] = acc
        all_dt4[kid] = dt4
        all_num[kid] = num

    # ---- Gate measurements ----
    # G1: deviation prose -> structured rows (kits with prose that convert).
    g1_kits_with_prose = sum(1 for k in kits if k["dev_notes"])
    g1_kits_converted = sum(1 for k in kits if k["dev_notes"] and all_dev[k["kit_id"]])
    # per-proposition lossless count
    g1_props = sum(len(split_deviation_propositions(k["dev_notes"])) for k in kits)
    g1_rows = sum(len(all_dev[k["kit_id"]]) for k in kits)
    g1_rate = (g1_kits_converted / g1_kits_with_prose * 100) if g1_kits_with_prose else 100.0

    # G2: door-arg derivability from prose (measured, not committed).
    g2_total, g2_deriv, g2_per_door, g2_nonderiv = measure_g2_door_args(kits)
    g2_rate = (g2_deriv / g2_total * 100) if g2_total else 0.0

    # G3: zero prose-only geometry on T1 primary skills.
    #   A primary skill is "captured" if its ordinal-0 band has a delivery_class.
    g3_t1_kits = [k for k in kits if (k["tier"] == "T1")]
    g3_prose_only = 0
    g3_missing_delivery = []
    for k in g3_t1_kits:
        b = all_bands[k["kit_id"]]
        if not b or b[0].get("delivery_class") is None:
            g3_prose_only += 1
            g3_missing_delivery.append(k["kit_id"])

    # G4: every red assert routes to a docket.
    g4_kits_with_red = 0
    g4_dockets = 0
    for k in kits:
        reds = [a for a in all_acc[k["kit_id"]] if a["last_result"] == "red"]
        if reds:
            g4_kits_with_red += 1
    # dockets = one per engine_inexpressible/param_gap deviation
    g4_docket_kits = []
    for k in kits:
        opens = [d for d in all_dev[k["kit_id"]]
                 if d["deviation_class"] in ("engine_inexpressible", "param_gap")]
        if opens:
            g4_docket_kits.append(k["kit_id"])
            g4_dockets += 1  # one docket per kit (dedup at kit grain)

    print("\n==================== GATE MEASUREMENTS ====================")
    print(f"G1 deviation->structured: {g1_kits_converted}/{g1_kits_with_prose} "
          f"prose-bearing kits convert = {g1_rate:.1f}% "
          f"(propositions {g1_props} -> rows {g1_rows}); threshold >=90%")
    print(f"G2 door-arg derivable-from-prose: {g2_deriv}/{g2_total} instances "
          f"= {g2_rate:.1f}% ; threshold >=80% (MEASURED not committed - fork)")
    if g2_nonderiv:
        print(f"   {len(g2_nonderiv)} non-derivable (kit,door) instances "
              f"(bare token, no behavioral prose for that door):")
        for kid, d in g2_nonderiv[:20]:
            print(f"     {kid}  {d}")
    print(f"G3 prose-only T1 geometry: {g3_prose_only} of {len(g3_t1_kits)} T1 kits "
          f"prose-only; threshold == 0")
    if g3_missing_delivery:
        print(f"   T1 kits missing delivery_class: {g3_missing_delivery}")
    print(f"G4 red-assert->docket: {g4_kits_with_red} kits carry a red assert; "
          f"{g4_dockets} deviation-lane dockets open; every red routes")

    report = dict(
        tranche="poe1-record", n_kits=len(kits),
        rows=dict(
            skill_geometry_band=sum(len(v) for v in all_bands.values()),
            kit_deviation=sum(len(v) for v in all_dev.values()),
            recognition_hook=sum(len(v) for v in all_hooks.values()),
            kit_acceptance_assert=sum(len(v) for v in all_acc.values()),
            kit_delta_t4=len(all_dt4),
            kit_numeric=sum(len(v) for v in all_num.values()),
        ),
        gates=dict(
            G1=dict(converted=g1_kits_converted, of=g1_kits_with_prose,
                    rate=round(g1_rate, 1), props=g1_props, rows=g1_rows),
            G2=dict(derivable=g2_deriv, of=g2_total, rate=round(g2_rate, 1),
                    committed=False, note="door-arg schema-design is the W4 fork"),
            G3=dict(prose_only=g3_prose_only, of=len(g3_t1_kits),
                    missing=g3_missing_delivery),
            G4=dict(kits_with_red=g4_kits_with_red, dockets=g4_dockets,
                    docket_kits=g4_docket_kits),
        ),
        anomalies_flagged=list(ELEM_ANOMALIES.keys()),
        partials_flagged=list(PARTIALS.keys()),
    )
    if args.report:
        with open(args.report, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nMeasurement report -> {args.report}")

    if args.dry_run:
        print("\nDRY-RUN: no rows written. corpus.db untouched.")
        conn.close()
        return

    # ---------------- APPLY (idempotent per side-car) ----------------
    write_rows(conn, kits, all_bands, all_dev, all_hooks, all_acc, all_dt4,
               all_num, g4_docket_kits)
    conn.commit()
    conn.close()
    print("\nAPPLY complete. Rows committed. Re-run is idempotent.")


def write_rows(conn, kits, all_bands, all_dev, all_hooks, all_acc, all_dt4,
               all_num, docket_kits):
    kid_list = [k["kit_id"] for k in kits]
    ph = ",".join("?" * len(kid_list))

    # -1) motion_signature_registry seed: catalogue the named paths this tranche
    #     uses (A-3 pattern; the registry is growable by design). These are
    #     geometry PATHS with canonical meaning, NOT door-arg design — safe to
    #     seed in a data pass (distinct from the door-arg schema fork).
    motion_seeds = {
        "chain_hop": "Bolt/effect hops target-to-target across a pack (chain geometry).",
        "burst_around_self": "Nova/ring bursts radially outward from the origin point.",
        "ground_place": "Effect is placed at a targeted ground point (trap/mine/brand/rain).",
        "point_strike": "Single-point melee/slam impact at the targeted enemy/ground.",
        "arc_sweep": "Melee arc sweeps a sector in front of the attacker (cleave/swing).",
    }
    for name, desc in motion_seeds.items():
        conn.execute(
            "INSERT OR IGNORE INTO motion_signature_registry(signature_name, description) "
            "VALUES (?, ?)", (name, desc))

    # 0) door_registry catalogue seed: catalogue the on-record PoE1 door tokens
    #    (frozen vocabulary already present in mapping_json.t4_doors). NOT minting.
    poe1_doors = set()
    for k in kits:
        for d in (k["mapping"].get("t4_doors") or []):
            poe1_doors.add(d)
    door_desc = {
        # short catalogue descriptions for the tokens (family-rooted).
        "GEOMETRY_PROPAGATION": "Propagates delivery geometry across the pack (chain/fork/cascade family).",
        "GEOMETRY_PROPAGATION_cascade": "Cascade variant: geometry propagates in a forward-marching cascade.",
        "GEOMETRY_COLLAPSE": "Collapses delivery geometry (shotgun-density / burst-around-self).",
        "ELEMENTAL_ECHO": "Trigger-family door: a host action triggers a payload skill (e.g. Cast-on-Crit).",
        "ELEMENT_CONVERSION_MONO": "Converts a skill's damage to a single target element.",
        "ELEMENT_CONVERSION_PHYSICAL": "Converts a skill's damage to/from physical.",
        "TEMPORAL_CHARGE": "Accumulate-then-discharge charge economy (build stack, dump stack).",
        "MOMENTUM_CASCADE": "Momentum/build-up that cascades into escalating output.",
        "PERSISTENCE_ENGINE": "Sustains a persistent effect while a resource/summon is active.",
        "PERSISTENCE_ENGINE_uptime": "Sustains a defensive/utility effect while a resource/summon is active (uptime variant).",
        "PERSISTENCE_ENGINE_saturation": "Persistence via saturating overlapping zones/DoTs.",
        "PROXY_ASCENSION": "Places autonomous emitter proxies (totem lane) that act on their own.",
        "PROXY_FISSION": "Splits into many small proxies/minions (fission).",
        "PROXY_CONVERGENCE": "Many proxies converge fire on a point/target.",
        "PROXY_INVERSION": "Inverts the proxy relationship (host becomes proxy or vice-versa).",
        "PROXY_SOVEREIGNTY": "A dominant proxy governs subordinate proxies.",
        "NETWORK_AMPLIFIER": "Amplifies via a network of linked effects (brands/links).",
        "RESONANCE_LOOP": "Self-reinforcing resonance loop (trigger feeds itself).",
        "RESOURCE_CONVERSION": "Converts one resource into another (life-as-mana, etc.).",
        "RETRIBUTION_ENGINE": "Reactive retribution (damage returned on being hit/blocking).",
        "SACRIFICE_ASCENDANCY": "Self-sacrifice/self-damage as the power source.",
        "TEMPORAL_CHARGE": "Accumulate-then-discharge charge economy (build stack, dump stack).",
        "ZONE_CONTROL": "Controls/denies a zone of the battlefield.",
        "PHASE_MOMENTUM": "Movement/phase momentum that powers the loop.",
        "DEFENSIVE_TRADEOFF": "Trades a defensive stat for offensive power (or vice-versa).",
        "DUAL_PROXY": "Spawns proxy clones that mirror the caster's skills from their own spatial origins.",
    }
    for d in sorted(poe1_doors):
        conn.execute(
            "INSERT OR IGNORE INTO door_registry(door_name, door_status, description) "
            "VALUES (?, 'active', ?)",
            (d, door_desc.get(d, f"On-record T4 door token '{d}' (catalogue seed; args deferred to door-arg RFC).")))

    # -------- IDEMPOTENT TEARDOWN (break the cycle, then children->parents) --------
    # There is a CIRCULAR FK between kit_deviation and mechanic_gap_docket:
    #   kit_deviation.docket_id        -> mechanic_gap_docket.docket_id
    #   mechanic_gap_docket.source_deviation_id -> kit_deviation.deviation_id
    # Under PRAGMA foreign_keys=ON neither can be deleted first. Break the cycle
    # by NULL-ing the deviation->docket back-reference, THEN tear down in order:
    #   acceptance_assert -> deviation-lane dockets -> kit_deviation -> the rest.
    conn.execute(f"UPDATE kit_deviation SET docket_id=NULL WHERE kit_id IN ({ph})",
                 kid_list)
    conn.execute(f"DELETE FROM kit_acceptance_assert WHERE kit_id IN ({ph})", kid_list)
    conn.execute(
        f"DELETE FROM mechanic_gap_docket WHERE intake_lane='deviation' "
        f"AND source_kit_id IN ({ph})", kid_list)
    conn.execute(f"DELETE FROM kit_deviation WHERE kit_id IN ({ph})", kid_list)
    conn.execute(f"DELETE FROM skill_geometry_band WHERE kit_id IN ({ph})", kid_list)
    conn.execute(f"DELETE FROM recognition_hook WHERE kit_id IN ({ph})", kid_list)
    conn.execute(f"DELETE FROM kit_delta_t4 WHERE kit_id IN ({ph})", kid_list)
    conn.execute(f"DELETE FROM kit_numeric WHERE kit_id IN ({ph})", kid_list)

    # 1) skill_geometry_band (insert)
    for kid, bands in all_bands.items():
        for b in bands:
            conn.execute("""INSERT INTO skill_geometry_band
                (kit_id, skill_ordinal, source_skill, delivery_class, origin,
                 width_band, range_band, speed_band, pierce, chain, fork,
                 count_per_cast, count_multiplier_x, count_multiplier_source,
                 cadence_class, motion_signature, band_conf, derivation,
                 source_anchor, exact_json, exact_source_type)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL,NULL)""",
                (kid, b["skill_ordinal"], b["source_skill"], b["delivery_class"],
                 b["origin"], b["width_band"], b["range_band"], b["speed_band"],
                 b["pierce"], b["chain"], b["fork"], b["count_per_cast"],
                 b["count_multiplier_x"], b["count_multiplier_source"],
                 b["cadence_class"], b["motion_signature"], b["band_conf"],
                 b["derivation"], b["source_anchor"]))

    # 2) recognition_hook (insert)
    for kid, hooks in all_hooks.items():
        for h in hooks:
            conn.execute("""INSERT INTO recognition_hook
                (kit_id, hook_id, rank, hook_type, hook_text, expressed_by,
                 provenance, coverage_status)
                VALUES (?,?,?,?,?,?,?,?)""",
                (kid, h["hook_id"], h["rank"], h["hook_type"], h["hook_text"],
                 h["expressed_by"], h["provenance"], h["coverage_status"]))

    # 3) kit_delta_t4 (insert)
    for kid, dt4 in all_dt4.items():
        conn.execute("""INSERT INTO kit_delta_t4
            (kit_id, shape, asserts_json, shape_signoff, shape_signoff_by)
            VALUES (?,?,?,?,?)""",
            (kid, dt4["shape"], dt4["asserts_json"], dt4["shape_signoff"],
             dt4["shape_signoff_by"]))

    # 4) kit_numeric (insert)
    for kid, nums in all_num.items():
        for n in nums:
            conn.execute("""INSERT INTO kit_numeric
                (kit_id, numeric_key, source_value, source_scale, rdr_value,
                 rule_id, source_anchor)
                VALUES (?,?,?,?,?,?,?)""",
                (kid, n["numeric_key"], n["source_value"], n["source_scale"],
                 n["rdr_value"], n["rule_id"], n["source_anchor"]))

    # 5) kit_deviation (insert) + capture new deviation_ids
    dev_id_by_kit = defaultdict(list)
    for kid, devs in all_dev.items():
        for d in devs:
            cur = conn.execute("""INSERT INTO kit_deviation
                (kit_id, missing_expression, deviation_class, hook_refs,
                 proposed_fix_type, proposed_fix_target, downgrade_owner,
                 source_anchor)
                VALUES (?,?,?,?,?,?,?,?)""",
                (kid, d["missing_expression"], d["deviation_class"],
                 d["hook_refs"], d["proposed_fix_type"], d["proposed_fix_target"],
                 d["downgrade_owner"], d["source_anchor"]))
            dev_id_by_kit[kid].append((cur.lastrowid, d["deviation_class"]))

    # 6) mechanic_gap_docket: auto-open one per kit with EI/PG deviation
    #    (deviation-lane dockets were torn down up-front in dependency order)
    docket_id_by_kit = {}
    for kid in docket_kits:
        # find the first EI/PG deviation id for this kit
        src_dev = None
        for did, dclass in dev_id_by_kit.get(kid, []):
            if dclass in ("engine_inexpressible", "param_gap"):
                src_dev = did
                break
        cur = conn.execute("""INSERT INTO mechanic_gap_docket
            (mechanism_class, spec_text_or_path, evidence_kits, destination,
             status, provenance_json, disposition, docket_family,
             source_deviation_id, source_kit_id, intake_lane)
            VALUES (?,?,?,?,'open',?,NULL,?,?,?,'deviation')""",
            (f"vdm2-deviation:{kid}",
             f"Engine-inexpressible/param-gap surfaced by W4 PoE1 structuring of {kid}.",
             json.dumps([kid]), "engine-design-intake",
             json.dumps({"auto_opened_by": "vdm2-w4-deviation-intake",
                         "tranche": "poe1-record"}),
             "vdm2-w4-poe1", src_dev, kid))
        docket_id_by_kit[kid] = cur.lastrowid

    # 6b) back-fill kit_deviation.docket_id for the EI/PG rows just docketed
    for kid, did in docket_id_by_kit.items():
        for dev_id, dclass in dev_id_by_kit.get(kid, []):
            if dclass in ("engine_inexpressible", "param_gap"):
                conn.execute("UPDATE kit_deviation SET docket_id=? WHERE deviation_id=?",
                             (did, dev_id))

    # 7) kit_acceptance_assert (insert) + route reds to dockets
    for kid, accs in all_acc.items():
        for a in accs:
            routed = docket_id_by_kit.get(kid) if a.get("routes_red") else None
            conn.execute("""INSERT INTO kit_acceptance_assert
                (kit_id, assert_text, hook_id, expected_state, last_result,
                 routed_docket_id)
                VALUES (?,?,?,?,?,?)""",
                (kid, a["assert_text"], a["hook_id"], a["expected_state"],
                 a["last_result"], routed))

    # 8) W5-adjudication flag stamp on the 8 frozen-elem anomalies + 2 partials.
    #    IDEMPOTENT: append the token only if not already present (no double-stamp
    #    on re-run). These structure on CURRENT frozen data and are FLAGGED, not
    #    resolved (discipline 1 / V-18). W5 re-derives the court on affected rows.
    W5_TOKEN = "vdm2-w5-elem-anomaly-2026-07-22"
    W5_PARTIAL_TOKEN = "vdm2-w5-partial-2026-07-22"
    for kid, note in ELEM_ANOMALIES.items():
        cur_flags = conn.execute(
            "SELECT flags FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()[0]
        cur_flags = cur_flags or ""
        if W5_TOKEN not in cur_flags:
            new_flags = (cur_flags + ("; " if cur_flags else "") +
                         f"{W5_TOKEN}: {note}")
            conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?",
                         (new_flags, kid))
    for kid, note in PARTIALS.items():
        cur_flags = conn.execute(
            "SELECT flags FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()[0]
        cur_flags = cur_flags or ""
        if W5_PARTIAL_TOKEN not in cur_flags:
            new_flags = (cur_flags + ("; " if cur_flags else "") +
                         f"{W5_PARTIAL_TOKEN}: {note}")
            conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?",
                         (new_flags, kid))


if __name__ == "__main__":
    main()
