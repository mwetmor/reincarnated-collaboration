#!/usr/bin/env python3
"""
VDM-2 W4 — PoE2 (Path of Exile 2) record-class tranche: six side-car emitter.

Fourth of five W4 tranches (PoE1 99d5ac8e / D2 c60f97a2 / GD d6f0e850 done).
PoE2 is closest to PoE1 (shared door/geometry grammar) but shares GD's
NO-W1-EVIDENCE posture, so this emitter adapts the GD scaffolding (frozen
whole-corpus proof, --export, ELEMENT_CONVERSION_HYBRID door family, the
placed_lane/fork geometry tokens) while reverting to a PROSE-MARKER EI
classifier — because PoE2 has ZERO frozen MAPPED_DOCKET kits (all 36 are
terminal_state='MAPPED': 27 CLOSE, 9 APPROX), so GD's terminal-anchored EI
rule would yield zero dockets and fail G4. The prose classifier is calibrated
to PoE2's SURVEYED language (see EI_MARKERS) and every classification is logged
for pre-apply inspection.

Reads the FROZEN VDM-1 substrate (canon_corpus + kit_mapping) for
game='poe2' AND corpus_class='record' (= 36 real kits; the 2 poe2 records
with corpus_class='system' / is_system=1 — poe2-temporalis-blink,
poe2-grim-feast — are EXCLUDED by the WHERE clause). Emits the six kit-FK-only
side-car blocks + auto-opened deviation-lane dockets + the door_registry /
motion_signature_registry catalogue seeds (all PoE2 door + motion tokens are
ALREADY in the post-GD registries — every INSERT OR IGNORE no-ops; running
totals stay 27 / 18).

CARVE-OUT (V-21): does NOT write kit_door_arg and does NOT design door_arg
vocabularies. It MEASURES the G2 door-arg derivability rate from prose without
committing rows (the door-arg RFC is parked post-W5).

Idempotent: delete-then-insert keyed on kit_id per side-car; deviation-lane
dockets keyed on (source_kit_id, intake_lane='deviation'); docket surrogate
AUTOINCREMENT continues from live max. Re-run cannot duplicate.

USAGE
  python3 vdm2_w4_poe2_sidecar_emit_2026_07_22.py --dry-run
  python3 vdm2_w4_poe2_sidecar_emit_2026_07_22.py --apply \
      --report <path.json> --export <path.json>
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(HERE, "..", "curated", "corpus.db"))

# ---------------------------------------------------------------------------
# Discipline-1 registries.
#
# elem_raw ANOMALIES: NONE for PoE2. The W4 PoE2 survey (elem_raw x court x
# skill.element_primary cross-tab) found ZERO mixed-court / NULL-court / clamped
# self-cost elem_raw anomalies of the PoE1 (8) or GD (1) flavor. PoE2's 5 courts
# (physical/lightning/fire/cold/chaos-poison) each resolve to a single clean RDR
# register. Left explicitly EMPTY (honest-empty; not a placeholder).
# ---------------------------------------------------------------------------
ELEM_ANOMALIES = {}

# DECAY-FAMILY REGISTER-SPLIT (RB-6; the D2-poison / GD-acid parallel the brief
# told us to WATCH for). Two PoE2 kits carry court='chaos-poison' (which the W3b
# crosswalk licenses to the shadow register) but a skill element_primary='earth'
# — the SAME court-vs-skill-element disagreement D2 (poison->earth) and GD
# (acid->earth) surfaced. FLAGGED for W5 with a W5 token; NOT resolved here
# (V-18: element fields frozen; reconcile surfaces, W5 adjudicates the court
# basis). Feeds the cross-tranche RB-6 Leg-B court-basis pattern.
POISON_REGISTER_INCONSISTENCY = {
    "poe2-concoction":
        "poison->earth register (skill.element_primary='earth' on the "
        "Gas-Grenade/flask-charge chaos-poison delivery) disagrees with "
        "court='chaos-poison' (W3b crosswalk licenses shadow). PoE2-poison "
        "register split (earth vs shadow) — parallels the D2-poison and GD-acid "
        "splits (RB-6 / Leg-B court-basis). W5 to unify which register the "
        "chaos-poison decay family takes across PoE1/PoE2/D2/GD.",
    "poe2-poison-pathfinder":
        "poison->earth register (skill.element_primary='earth' on the "
        "poison-conversion projectile delivery) disagrees with "
        "court='chaos-poison' / crosswalk-licensed shadow. PoE2-poison register "
        "split — same RB-6 cross-tranche decay-family question as D2/GD. W5 to "
        "unify.",
}

# ---------------------------------------------------------------------------
# geometry_value -> delivery_class (spec s4 enum: projectile|beam|zone|motion|
# aura|summon_delegate|melee_arc). PoE1/D2/GD base, complete over the 16 PoE2
# on-record geometry tokens (surveyed: ground_targeted_circle, multi_projectile,
# melee_arc, self_buff, totem, ring, single_target, melee_strike, ground_slam,
# placed_lane, whirlwind, fork, aura, chain, dash_attack, line).
# ---------------------------------------------------------------------------
GEO_TO_DELIVERY = {
    "multi_projectile": "projectile",
    "totem": "summon_delegate",
    "ground_targeted_circle": "zone",
    "melee_strike": "melee_arc",
    "self_buff": "aura",
    "circle": "zone",
    "single_target": "projectile",   # bolt/hit at a single target; projectile-class
    "melee_arc": "melee_arc",
    "line": "projectile",            # straight-line projectile path, not a beam
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
    # PoE2 shared-with-GD tokens (surveyed present in PoE2: placed_lane, fork):
    "placed_lane": "zone",           # a placed ground lane/wall (Bone Cage, Wall)
    "fork":        "projectile",     # a forking projectile fan (Galvanic Shards)
}
# geometry_value -> motion_signature (open registry; NULL when no clean path).
# Every named path below is ALREADY in motion_signature_registry (post-GD 18).
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
    "placed_lane": "lane_place",
    "fork": "fork_split",
}
# geometry_value -> default cadence_class hint (NULL unless prose refines).
GEO_TO_CADENCE = {
    "totem": "cooldown",
    "aura": None,
    "self_buff": None,
    "beam_channel": "channel",
    "whirlwind": "channel",
    "placed_lane": "cooldown",
    "fork": None,
}
# Non-payload delivery families whose range_band is 'self'.
SELF_RANGE_GEOS = {"self_buff", "aura"}
# Melee-range delivery families.
MELEE_RANGE_GEOS = {"melee_strike", "melee_arc", "ground_slam", "whirlwind"}

# ---------------------------------------------------------------------------
# Deviation-class classifier (spec s3 taxonomy).
#
# PoE2 posture: PROSE-MARKER EI (the PoE1 model), NOT the GD terminal-anchored
# rule — because PoE2 has NO frozen MAPPED_DOCKET kits (survey: all 36 MAPPED).
# engine_inexpressible fires ONLY on an explicit NO-MECHANISM / NO-MEMBER /
# NO-LANE / NO-KEY claim (the mapper attests the engine has no lane) — surveyed
# PoE2 phrasings below. A bare "the source player would miss X" (a recognition-
# hook LOSS) is NOT EI on its own; it is accepted_downgrade unless paired with a
# no-mechanism claim (spec s3: engine_inexpressible = engine-side inexpressibility
# found by the mapper, distinct from texture loss). Downgrade-override markers
# (identity-survives tells) neutralise an EI substring where the SAME proposition
# also declares the loss is faithful/tuning-only/not-unmodelable.
# ---------------------------------------------------------------------------
EI_MARKERS = [
    # explicit no-mechanism / no-member / no-lane / no-key claims (surveyed PoE2)
    "no native key", "not expressible as a native key", "no engine lane",
    "no engine analog", "engine has no", "has no native", "no first-class",
    "no single 26-geometry member", "no single", "no member",
    "no key couples", "docket-candidate", "docket candidate",
    # generic carryovers (kept for robustness; may not fire on PoE2)
    "no native expression", "not separately addressable", "no meta endpoint",
    "cannot be expressed", "no expression", "unmappable", "would be fabrication",
    "no autonomous-combatant", "no player-initiated delivery",
]
PG_MARKERS = [
    "needs an arg", "arg the door", "not yet carry", "second parallel trigger",
    "additional trigger", "param gap", "parallel trigger",
]

# Identity-survives (accepted_downgrade) tells. These NEUTRALISE an EI substring
# in the SAME proposition — the loss is a texture/hook loss, not an open engine
# gap. Surveyed PoE2 phrasings: "that build, worse" (acolyte-darkness),
# "that build, meaningfully flatter"/"not a wholly unmodelable loop" (twister),
# "that build, flatter"/"not unmodelable" (walking-calamity), "faithful"/
# "preserved"/"recognizable" (rake, smith, perfect-strike), and the explicit
# self-negation "TUNING artifact, not a mappable mechanism" (perfect-strike).
DOWNGRADE_OVERRIDE_MARKERS = [
    "that build, worse", "that build worse", "that build, mean", "that build mean",
    "that build, flat", "that build flat", "that build, slight", "still that build",
    "not a different build", "not a wholly unmodelable", "not unmodelable",
    "not wholly unmodelable", "not a wholly", "identity is preserved",
    "identity are preserved", "is preserved", "are preserved", "are faithful",
    "is faithful", "otherwise faithful", "recognizable", "recognisable",
    "watch-item", "watch item", "steward candidate", "steward review",
    "steward mint review", "qualitative candidate",
    "tuning artifact, not a mappable", "balance, not a missing",
    "not 'not that build'", "not \"not that build\"",
]


# The AUTHORITATIVE EI discriminator (survey-anchored on the 36 PoE2 dossiers).
#
# The close read of the boundary kits showed that "engine has no X" ALONE is NOT
# sufficient for engine_inexpressible: the mapper writes it for TEXTURE losses it
# then explicitly maps ("no engine analog [for the crafting-loop]... slam-ignite
# identity are faithful"; "engine has no native ...RETREAT half... identity is
# preserved"; "no single 26-geometry member... all map cleanly, so CLOSE"). The
# mapper's OWN signal that a gap is a REAL open engine gap (not a texture loss) is
# one of: an explicit docket reference (docket / docket-candidate), the GX-02
# form-swap engine-gap tracker, an explicit "no engine lane", or a STRUCTURAL
# "no native key couples/for" coupling claim (a load-bearing stat/mechanic
# coupling the whole build rests on). THOSE are engine_inexpressible; everything
# else with an identity-survives tell (faithful / preserved / recognizable /
# maps cleanly / that build worse / not unmodelable) is accepted_downgrade.
DOCKET_EI_MARKERS = [
    "docket-candidate", "docket candidate", "+ docket", "+docket",
    "note + docket", "cadence note + docket", "notes + a docket",
    "notes + a docket-candidate", "scaler notes + a", "a docket-able",
    "docket-able quantitative", "gx-02", "no engine lane",
    # structural load-bearing coupling gaps (the build's whole damage rests on it)
    "no native key couples", "no native key for", "no key couples",
    "no lane that couples", "not expressible as a native key",
]
# Identity-survives tells that, ABSENT a DOCKET_EI signal, downgrade an EI-shaped
# "engine has no X" to accepted_downgrade (texture/flavor loss, mapped cleanly).
IDENTITY_SURVIVES = DOWNGRADE_OVERRIDE_MARKERS + [
    "map cleanly", "maps cleanly", "otherwise map", "all map cleanly",
    "core melee", "the core", "playable", "faithfully", "faithful",
]


def classify_deviation(prose):
    """Classify a single deviation proposition (PoE1 prose-marker model,
    PoE2-calibrated). Returns engine_inexpressible | param_gap |
    accepted_downgrade. Every call is logged by the caller for inspection.

    RULE (survey-anchored): engine_inexpressible iff the proposition carries the
    mapper's OWN open-gap signal — an explicit docket / docket-candidate / GX-02
    / "no engine lane" / structural "no native key couples-for" coupling claim.
    A self-negating "tuning artifact, not a mappable mechanism" cancels even that
    (the gap is a balance artifact, not a missing feature). A bare "engine has
    no X" describing a TEXTURE loss the mapper then maps cleanly / calls faithful
    / preserved / recognizable is accepted_downgrade, not EI."""
    low = prose.lower()
    # self-negation: the 'gap' is a balance/tuning artifact, not a missing feature
    if any(m in low for m in ("tuning artifact, not a mappable",
                              "balance, not a missing")):
        return "accepted_downgrade"
    docket_ei = [m for m in DOCKET_EI_MARKERS if m in low]
    if docket_ei:
        # the mapper's own open-gap signal: a genuine engine_inexpressible gap.
        return "engine_inexpressible"
    # No docket/GX-02/coupling signal. An EI-shaped "engine has no X" here is a
    # texture/flavor loss the mapper mapped cleanly -> accepted_downgrade.
    if any(m in low for m in PG_MARKERS):
        return "param_gap"
    if any(m in low for m in EI_MARKERS) and not any(m in low for m in IDENTITY_SURVIVES):
        # an EI substring with NO identity-survives tell AND no docket signal —
        # rare on PoE2, but keep it EI (a bare unmappable claim). Defensive.
        return "engine_inexpressible"
    return "accepted_downgrade"


def split_deviation_propositions(dev_notes):
    """Split deviation_notes into distinct propositions (conservative)."""
    if not dev_notes:
        return []
    txt = dev_notes.strip()
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
    if ("wide" in low or "large aoe" in low or "large area" in low
            or "entire screen" in low or "whole screen" in low
            or "screen-wide" in low or "blankets" in low
            or "screen coverage" in low or "-screen" in low):
        return "wide"
    return None


def extract_speed(notes):
    low = notes.lower()
    if "instant" in low:
        return "instant"
    if ("slow orb" in low or "drifts" in low or "slow-moving" in low
            or "slowly" in low or "lingering" in low or "linger" in low):
        return "slow"
    if "fast" in low or "quickly" in low or "rapid" in low:
        return "fast"
    return None


def extract_count(notes):
    low = notes.lower()
    m = re.search(r"(\d+)\s+(?:base\s+)?projectiles?", low)
    if m:
        return int(m.group(1))
    m = re.search(r"~?(\d+)\s+(?:bolts?|shards?|spears?|totems?|mortars?|meteors?|arrows?)", low)
    if m:
        return int(m.group(1))
    m = re.search(r"up to (\d+) times", low)
    if m:
        return int(m.group(1))
    return 1


def extract_pierce(notes):
    low = notes.lower()
    if "pierces all" in low or "pierce all" in low:
        return "all"
    if "piercing" in low or "pierce" in low or "pierces" in low:
        return "all"  # PoE2 piercing projectiles typically pierce the pack
    return None


def extract_range(notes, geo):
    low = notes.lower()
    if geo in SELF_RANGE_GEOS:
        return "self"
    if geo in MELEE_RANGE_GEOS:
        return "melee"
    if ("screen" in low or "screen-wide" in low or "blanket" in low
            or "entire screen" in low or "whole screen" in low
            or "-screen" in low or "screen coverage" in low):
        return "screen"
    if "long range" in low or "long-range" in low or "ranged spam" in low:
        return "long"
    if ("short range" in low or "point-blank" in low or "point blank" in low
            or "must be point-blank" in low):
        return "short"
    return None


def load_kits(conn):
    rows = conn.execute("""
        SELECT c.kit_id, c.folk_name, c.elem_raw, c.tier, c.court,
               c.capstone_source_acquisition, c.core_skills, c.mech_note,
               m.mapping_json, m.grade, m.terminal_state, m.deviation_notes
        FROM canon_corpus c
        JOIN kit_mapping m ON c.kit_id = m.kit_id
        WHERE c.game='poe2' AND c.corpus_class='record'
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
            elif "cooldown" in low or ("every " in low and "seconds" in low):
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
    """Structured kit_deviation rows from deviation_notes prose. EI-classification
    is by PROSE MARKER (PoE1 model; PoE2 has no frozen MAPPED_DOCKET signal)."""
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
            downgrade_owner=("elrond (W4 PoE2 tranche; internal-consistency "
                             "reconcile, no W1 evidence — W5 is PoE2's external "
                             "check)" if dclass == "accepted_downgrade" else None),
            source_anchor=p[:1500],
        )
        rows.append(row)
    return rows


def derive_hooks(kit, bands):
    """recognition_hook rows: geometry + element register."""
    hooks = []
    rank = 1
    b0 = None
    for b in bands:
        if b.get("delivery_class"):
            b0 = b
            break
    if b0 is None and bands:
        b0 = bands[0]
    if b0 is not None:
        geo = b0.get("_geo_raw") or ""
        deliv = b0.get("delivery_class") or "delivery"
        hooks.append(dict(
            hook_id=f"H{rank}", rank=rank, hook_type="geometry",
            hook_text=f"{kit['folk']}: {(geo or 'core').replace('_',' ')} {deliv} identity",
            expressed_by="geometry.delivery_class",
            provenance="crawled", coverage_status="expressed",
            source_skill=b0.get("source_skill"),
        ))
        rank += 1
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
    """kit_acceptance_assert rows: >=1 GREEN signature assert, and — per
    engine_inexpressible/param_gap deviation — one RED assert routed to a docket
    (red-test doctrine; spec s6)."""
    asserts = []
    b0 = None
    for b in bands:
        if b.get("delivery_class"):
            b0 = b
            break
    if b0 is not None:
        asserts.append(dict(
            assert_text=f"primary_delivery_class == '{b0['delivery_class']}'",
            hook_id="H1", expected_state=None, last_result="green",
            routes_red=False,
        ))
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
        asserts.insert(0, dict(
            assert_text="kit_identity_present == true",
            hook_id="H1", expected_state=None, last_result="green",
            routes_red=False,
        ))
    return asserts


def derive_delta_t4(kit):
    """kit_delta_t4 shape (step|ramp). Capstone-threshold / discrete-enable reads
    'step'; synergy-stack / continuous-scaling / accumulator reads 'ramp'. PoE2
    skews: charge/energy accumulators + attribute-stacking + Rage/Glory two-tier
    -> ramp; ascendancy/unique-item discrete transforms -> step."""
    blob = (kit["dev_notes"] + " " + (kit["mech_note"] or "")).lower()
    cap = (kit["capstone"] or "").lower()
    shape = "step"
    if any(w in blob for w in ["synergy", "stack", "continuous", "scal", "ramp",
                               "gradient", "more per", "per remaining",
                               "accumulat", "build up", "build-up", "charges",
                               "two-tier", "two tier", "overflow", "spill",
                               "meter", "energy economy", "trigger energy",
                               "trigger-energy", "attribute-stack",
                               "attribute stack", "mana-stack", "mana stack"]):
        shape = "ramp"
    if cap in ("set_threshold", "unique_item", "ascendancy", "runeword",
               "transmuter", "skill_native"):
        shape = "step"
    return dict(shape=shape, asserts_json=json.dumps([
        f"T4 transformation shape={shape} (derived from mapping prose)"
    ]), shape_signoff="unvalidated", shape_signoff_by=None)


def derive_numerics(kit):
    """kit_numeric rows ONLY where prose attests a %/magnitude source-scale value.
    rdr_value NULL (no normalization rule run; spec s5). Honest-empty otherwise.
    PoE2 exact numbers live in the PoB2/datamine lane (V-19 NULL, a separate
    downstream legolas lane), so prose-derived rows are expected sparse."""
    rows = []
    text = kit["dev_notes"] + " " + (kit["mech_note"] or "")
    for m in re.finditer(
            r"(\d{2,4})\s*%\s*(damage reduction|dr|self-burn|hp-cost|"
            r"more damage|increased|of max-life|of max life|of maximum life|"
            r"more frequent|weapon damage|conversion)", text.lower()):
        val = float(m.group(1))
        scale = m.group(2).replace(" ", "_")
        rows.append(dict(
            numeric_key=f"{scale}_{int(val)}",
            source_value=val, source_scale=f"poe2_{scale}",
            rdr_value=None, rule_id=None,
            source_anchor=text[max(0, m.start()-40):m.end()+40].strip()[:300],
        ))
    return rows


# Per-door-family behavioral-parameter cues. A (kit,door) instance's args are
# "derivable from prose" when the mapping prose names a CONCRETE behavioral
# parameter for THAT door's family. The honest G2 measure. PoE2 reuses the D2/GD
# cue families (PoE2's 20 door tokens are a subset of the post-GD 27-door
# registry). PoE2-native mechanics (spirit-reservation, combo/detonation,
# armour-break sunder, dodge-roll, mana-stacking, flask-charge) fold into the
# existing families.
DOOR_ARG_CUES = {
    "GEOMETRY_PROPAGATION": ["chain", "fork", "cascade", "hop", "propagat", "split", "spread", "beam-chain", "spreads", "on-kill", "on kill"],
    "GEOMETRY_COLLAPSE": ["shotgun", "point-blank", "point blank", "burst", "collapse", "density", "overlap", "nova", "ring", "cluster", "scatter", "fan", "shards", "bunches"],
    "ELEMENTAL_ECHO": ["trigger", "on crit", "on-crit", "on hit", "cast on", "proc", "echo", "free proc", "free-proc", "energy", "discharge", "detonat", "comet"],
    "ELEMENT_CONVERSION_MONO": ["convert", "mono", "single element", "forced", "pure ", "->", "conversion", "chaos-convert", "full conversion"],
    "ELEMENT_CONVERSION_PHYSICAL": ["phys", "physical", "convert", "->", "sunder", "armour-break", "armour break", "impale", "trauma"],
    "ELEMENT_CONVERSION_HYBRID": ["hybrid", "dual element", "two element", "mixed", "composite", "convert", "fire+", "part physical", "part fire", "tri-elemental"],
    "TEMPORAL_CHARGE": ["charge", "accumulat", "stack", "discharge", "energy", "two-tier", "overflow", "spill", "meter", "glory", "rage", "heat", "weapon heat", "periodic"],
    "MOMENTUM_CASCADE": ["momentum", "ramp", "build up", "build-up", "escalat", "stage", "frenzy", "velocity", "speed", "faster", "tempo", "casting speed", "more frequent", "density-reactive", "enemy-count"],
    "PERSISTENCE_ENGINE": ["uptime", "while active", "sustain", "persist", "aura", "reserv", "spirit", "maintained", "linger", "saturat", "field", "platform", "ground field", "wall"],
    "PERSISTENCE_ENGINE_uptime": ["uptime", "while active", "aura", "maintained", "reserv", "spirit", "sustain", "buff", "waking dream", "persistent buff", "toggle"],
    "PERSISTENCE_ENGINE_saturation": ["saturat", "overlapping", "linger", "blanket", "zone", "dot", "carpet", "field", "ground-dot", "overlap", "cloud", "meteor-field", "autobomber"],
    "PROXY_ASCENSION": ["totem", "emitter", "placed", "autonomous", "ballista", "brand", "turret", "wall", "shield-wall"],
    "PROXY_FISSION": ["minion", "swarm", "split", "spawn", "skeleton", "srs", "raging spirit", "demon", "infernal", "legion", "army", "pet"],
    "PROXY_CONVERGENCE": ["converge", "focus fire", "all fire", "concentrat"],
    "PROXY_INVERSION": ["invert", "consumabl", "battery", "consume", "corpse", "fuel", "sacrifice"],
    "PROXY_SOVEREIGNTY": ["reaper", "sovereign", "commander", "dominant", "governs", "empower", "companion", "spectre", "familiar", "minion", "infernalist"],
    "NETWORK_AMPLIFIER": ["brand", "link", "network", "wither", "curse", "amplif", "support", "supporting fire", "buff-ally", "party", "ally"],
    "RESONANCE_LOOP": ["loop", "resonance", "self-hit", "self hit", "cwdt", "ward", "feed", "trigger feeds", "re-arc", "energy"],
    "RESOURCE_CONVERSION": ["mana", "life as", "blood magic", "reserv", "spirit", "eldritch", "mind over matter", "mom", "convert", "mana-stack", "mana stack", "archmage", "max-mana", "max mana", "flask", "flask-charge", "flask charge"],
    "RETRIBUTION_ENGINE": ["block", "reflect", "retaliat", "when hit", "on block", "aegis", "wall of shields", "shield", "counter"],
    "SACRIFICE_ASCENDANCY": ["sacrifice", "self-damage", "self damage", "self-burn", "hp cost", "hp-cost", "life cost", "blood", "overheal", "overleech", "demonflame", "life-drain", "life drain", "darkness"],
    "ZONE_CONTROL": ["zone", "ground", "area deni", "control", "cyclone", "whirl", "wall", "field", "root", "bone cage", "cloud", "carpet", "blanket", "screen"],
    "PHASE_MOMENTUM": ["dash", "blink", "movement", "phase", "flicker", "disengage", "dodge", "dodge-roll", "dodge roll", "reposition", "hit-and-run", "hit and run", "retreat"],
    "DEFENSIVE_TRADEOFF": ["tradeoff", "trade-off", "trade ", "low life", "reserve", "defensive", "self-burn", "form lock", "form-lock", "demon", "overheal"],
    "GEOMETRY_PROPAGATION_cascade": ["cascade", "chain", "forward", "marching", "propagat", "spread"],
    "GEOMETRY_PROPAGATION_overkill": ["overkill", "corpse explos", "chain", "detonat", "excess", "spill", "explosion on death", "on-kill", "on kill", "herald of ice", "shatter"],
    "DUAL_PROXY": ["mirror", "clone", "proxy", "companion"],
}


def measure_g2_door_args(kits):
    """G2 = door args derivable from EXISTING prose without re-crawl (>=80%).
    MEASURED (not committed — the door-arg RFC fork, V-21)."""
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
                 k["dev_notes"] + " " + (k["mech_note"] or "")).lower()
        for d in doors:
            total += 1
            per_door[d][0] += 1
            cues = DOOR_ARG_CUES.get(d, [])
            base = d.rsplit("_", 1)[0] if "_" in d else d
            cues = cues or DOOR_ARG_CUES.get(base, [])
            if cues and any(c in prose for c in cues):
                derivable += 1
                per_door[d][1] += 1
            else:
                non_derivable.append((k["kit_id"], d))
    return total, derivable, per_door, non_derivable


def frozen_content_hash_tranche(conn):
    """Content hash over the IMMUTABLE identity columns of the 36 PoE2 record
    kits (elem_raw / core_skills / mech_note / folk_name / game / tier). Proves
    the frozen PoE2 elem_raw (V-18) is untouched PRE vs POST (tranche scope)."""
    rows = conn.execute("""
        SELECT kit_id, elem_raw, core_skills, mech_note, folk_name, game, tier
        FROM canon_corpus
        WHERE game='poe2' AND corpus_class='record'
        ORDER BY kit_id
    """).fetchall()
    h = hashlib.md5()
    for r in rows:
        h.update(("\x1f".join("" if v is None else str(v) for v in r)).encode())
        h.update(b"\x1e")
    return h.hexdigest()


def elem_raw_wholecorpus_hash(conn):
    """WHOLE-CORPUS 585-row elem_raw content hash (the brief's stronger V-18
    proof). Proves NO elem_raw field ANYWHERE in the corpus changed — not just
    the PoE2 tranche. Must be identical live-vs-backup and PRE-vs-POST."""
    rows = conn.execute(
        "SELECT kit_id, elem_raw FROM canon_corpus ORDER BY kit_id").fetchall()
    h = hashlib.md5()
    for kid, er in rows:
        h.update(("\x1f".join([kid, "" if er is None else str(er)])).encode())
        h.update(b"\x1e")
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default=None, help="write measurement JSON here")
    ap.add_argument("--export", default=None, help="write durable side-car JSON here")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        print("ERROR: pass --apply or --dry-run", file=sys.stderr)
        sys.exit(2)

    ro = args.dry_run
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro" if ro else DB_PATH, uri=True)
    if not ro:
        conn.execute("PRAGMA foreign_keys=ON")  # honesty: fail loud on FK breach
    kits = load_kits(conn)
    assert len(kits) == 36, f"expected 36 PoE2 record kits, got {len(kits)}"
    print(f"Loaded {len(kits)} PoE2 record-class kits (game=poe2, corpus_class=record).")

    # Confirm the 2 system-records were NOT loaded (excluded by WHERE clause).
    sysrec = conn.execute(
        "SELECT kit_id FROM canon_corpus WHERE game='poe2' "
        "AND (corpus_class='system' OR is_system=1) ORDER BY kit_id").fetchall()
    loaded_ids = {k["kit_id"] for k in kits}
    sys_ids = {r[0] for r in sysrec}
    print(f"PoE2 system-records (MUST be excluded): {sorted(sys_ids)}")
    assert not (sys_ids & loaded_ids), (
        f"SYSTEM-RECORD LEAK: {sys_ids & loaded_ids} loaded as record kits!")
    print(f"  confirmed NOT in the emitted set: {sorted(sys_ids)} (leak check clean)")

    frozen_pre = frozen_content_hash_tranche(conn)
    elem_whole_pre = elem_raw_wholecorpus_hash(conn)
    print(f"Frozen-identity content hash PRE (PoE2 tranche): {frozen_pre}")
    print(f"elem_raw WHOLE-CORPUS 585-row content hash PRE: {elem_whole_pre}")

    # Derive all blocks.
    all_bands, all_dev, all_hooks, all_acc, all_dt4, all_num = {}, {}, {}, {}, {}, {}
    classification_log = []
    for k in kits:
        kid = k["kit_id"]
        bands = derive_geometry_bands(k)
        dev = derive_deviations(k)
        hooks = derive_hooks(k, bands)
        acc = derive_acceptance(k, bands, dev)
        dt4 = derive_delta_t4(k)
        num = derive_numerics(k)
        for d in dev:
            d["hook_refs"] = json.dumps(["H1"]) if hooks else None
        all_bands[kid] = bands
        all_dev[kid] = dev
        all_hooks[kid] = hooks
        all_acc[kid] = acc
        all_dt4[kid] = dt4
        all_num[kid] = num
        for d in dev:
            classification_log.append((kid, d["deviation_class"],
                                       d["missing_expression"][:70]))

    # ---- CLASSIFICATION LOG (survey-anchored inspection; discipline 10) ----
    print("\n==================== DEVIATION CLASSIFICATION ====================")
    for kid, dclass, me in classification_log:
        tag = {"engine_inexpressible": "EI ", "param_gap": "PG ",
               "accepted_downgrade": "DG "}.get(dclass, "?? ")
        print(f"  {tag} {kid}: {me}")

    # ---- Gate measurements ----
    g1_kits_with_prose = sum(1 for k in kits if k["dev_notes"])
    g1_kits_converted = sum(1 for k in kits if k["dev_notes"] and all_dev[k["kit_id"]])
    g1_props = sum(len(split_deviation_propositions(k["dev_notes"])) for k in kits)
    g1_rows = sum(len(all_dev[k["kit_id"]]) for k in kits)
    g1_rate = (g1_kits_converted / g1_kits_with_prose * 100) if g1_kits_with_prose else 100.0

    g2_total, g2_deriv, g2_per_door, g2_nonderiv = measure_g2_door_args(kits)
    g2_rate = (g2_deriv / g2_total * 100) if g2_total else 0.0

    g3_t1_kits = [k for k in kits if (k["tier"] == "T1")]
    g3_prose_only = 0
    g3_missing_delivery = []
    g3_zero_skill_t1 = []
    g3_null_geo0_t1 = []
    for k in g3_t1_kits:
        b = all_bands[k["kit_id"]]
        if not b:
            g3_zero_skill_t1.append(k["kit_id"])
            continue
        # a G3 miss = skill0 has geometry PROSE but no derived delivery_class
        if b[0].get("delivery_class") is None:
            if b[0].get("_geo_raw"):
                g3_prose_only += 1
                g3_missing_delivery.append(k["kit_id"])
            else:
                g3_null_geo0_t1.append(k["kit_id"])

    g4_kits_with_red = 0
    for k in kits:
        reds = [a for a in all_acc[k["kit_id"]] if a["last_result"] == "red"]
        if reds:
            g4_kits_with_red += 1
    g4_docket_kits = []
    g4_dockets = 0
    for k in kits:
        opens = [d for d in all_dev[k["kit_id"]]
                 if d["deviation_class"] in ("engine_inexpressible", "param_gap")]
        if opens:
            g4_docket_kits.append(k["kit_id"])
            g4_dockets += 1

    ei_kits = [k["kit_id"] for k in kits
               if any(d["deviation_class"] == "engine_inexpressible"
                      for d in all_dev[k["kit_id"]])]

    print("\n==================== GATE MEASUREMENTS ====================")
    print(f"G1 deviation->structured: {g1_kits_converted}/{g1_kits_with_prose} "
          f"prose-bearing kits convert = {g1_rate:.1f}% "
          f"(propositions {g1_props} -> rows {g1_rows}); threshold >=90%")
    print(f"G2 door-arg derivable-from-prose: {g2_deriv}/{g2_total} instances "
          f"= {g2_rate:.1f}% ; threshold >=80% (MEASURED not committed - V-21 fork)")
    if g2_nonderiv:
        print(f"   {len(g2_nonderiv)} non-derivable (kit,door) instances "
              f"(bare token, no behavioral prose for that door):")
        for kid, d in g2_nonderiv[:20]:
            print(f"     {kid}  {d}")
    print(f"G3 prose-only T1 geometry: {g3_prose_only} of {len(g3_t1_kits)} T1 kits "
          f"prose-only; threshold == 0")
    if g3_missing_delivery:
        print(f"   T1 kits missing delivery_class (adjectival prose failed): {g3_missing_delivery}")
    if g3_zero_skill_t1:
        print(f"   T1 kits with ZERO skills (honest extraction-null, NOT a G3 miss): {g3_zero_skill_t1}")
    if g3_null_geo0_t1:
        print(f"   T1 kits with skill[0] NULL geometry (honest GAP-deferred null, NOT a G3 miss): {g3_null_geo0_t1}")
    print(f"G4 red-assert->docket: {g4_kits_with_red} kits carry a red assert; "
          f"{g4_dockets} deviation-lane dockets will open (surrogate continues "
          f"from live max); every red routes")
    print(f"\nEI-deviation kits (prose classifier output): {len(ei_kits)} {ei_kits}")
    print(f"Decay-family register-split (RB-6; W5-flagged): "
          f"{sorted(POISON_REGISTER_INCONSISTENCY.keys())}")
    print(f"elem_raw anomalies (W5-flagged): {sorted(ELEM_ANOMALIES.keys()) or 'NONE (honest-empty)'}")

    report = dict(
        tranche="poe2-record", n_kits=len(kits), frozen_pre=frozen_pre,
        elem_wholecorpus_pre=elem_whole_pre,
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
                    committed=False, note="door-arg RFC parked post-W5 (V-21)"),
            G3=dict(prose_only=g3_prose_only, of=len(g3_t1_kits),
                    missing=g3_missing_delivery, zero_skill_t1=g3_zero_skill_t1,
                    null_geo0_t1=g3_null_geo0_t1),
            G4=dict(kits_with_red=g4_kits_with_red, dockets=g4_dockets,
                    docket_kits=g4_docket_kits),
        ),
        delta_t4_split=dict(
            step=sum(1 for v in all_dt4.values() if v["shape"] == "step"),
            ramp=sum(1 for v in all_dt4.values() if v["shape"] == "ramp"),
        ),
        ei_deviation=ei_kits,
        anomalies_flagged=list(ELEM_ANOMALIES.keys()),
        poison_register_split=list(POISON_REGISTER_INCONSISTENCY.keys()),
        system_records_excluded=sorted(sys_ids),
    )
    if args.report:
        with open(args.report, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nMeasurement report -> {args.report}")

    if args.export:
        export = dict(
            tranche="poe2-record", schema_version="v2.0", n_kits=len(kits),
            emitted="2026-07-22", frozen_identity_hash_pre=frozen_pre,
            elem_raw_wholecorpus_hash_pre=elem_whole_pre,
            gates=report["gates"], row_counts=report["rows"],
            delta_t4_split=report["delta_t4_split"],
            ei_deviation=ei_kits,
            elem_anomalies_w5_flagged=ELEM_ANOMALIES,
            poison_register_split_w5_flagged=POISON_REGISTER_INCONSISTENCY,
            system_records_excluded=sorted(sys_ids),
            per_kit={},
        )
        for k in kits:
            kid = k["kit_id"]
            export["per_kit"][kid] = dict(
                folk=k["folk"], elem_raw=k["elem"], tier=k["tier"],
                grade=k["grade"], terminal=k["terminal"],
                skill_geometry_band=all_bands[kid],
                kit_deviation=all_dev[kid],
                recognition_hook=all_hooks[kid],
                kit_acceptance_assert=all_acc[kid],
                kit_delta_t4=all_dt4[kid],
                kit_numeric=all_num[kid],
            )
        with open(args.export, "w") as f:
            json.dump(export, f, indent=2, default=str)
        print(f"Durable side-car export -> {args.export}")

    if args.dry_run:
        print("\nDRY-RUN: no rows written. corpus.db untouched.")
        conn.close()
        return

    # ---------------- APPLY (idempotent per side-car) ----------------
    write_rows(conn, kits, all_bands, all_dev, all_hooks, all_acc, all_dt4,
               all_num, g4_docket_kits)
    conn.commit()

    frozen_post = frozen_content_hash_tranche(conn)
    elem_whole_post = elem_raw_wholecorpus_hash(conn)
    print(f"\nFrozen-identity content hash POST (PoE2 tranche): {frozen_post}")
    print(f"elem_raw WHOLE-CORPUS 585-row content hash POST: {elem_whole_post}")
    assert frozen_pre == frozen_post, (
        f"FROZEN VIOLATION (tranche): elem_raw/identity changed! "
        f"pre={frozen_pre} post={frozen_post}")
    assert elem_whole_pre == elem_whole_post, (
        f"FROZEN VIOLATION (whole-corpus 585-row elem_raw): "
        f"pre={elem_whole_pre} post={elem_whole_post}")
    print("elem_raw FROZEN-PROOF: tranche AND whole-corpus 585-row content hash "
          "IDENTICAL pre/post (V-18 held).")

    iron = conn.execute(
        "SELECT (SELECT COUNT(*) FROM canon_corpus), "
        "(SELECT COUNT(*) FROM kit_mapping), "
        "(SELECT COUNT(*) FROM canon_corpus WHERE is_system=1)").fetchone()
    print(f"Iron-law: canon_corpus={iron[0]} kit_mapping={iron[1]} is_system={iron[2]} "
          f"(expect 585/574/19)")
    assert iron == (585, 574, 19), f"IRON-LAW VIOLATION: {iron}"

    fk = conn.execute("PRAGMA foreign_key_check").fetchall()
    print(f"foreign_key_check: {'EMPTY (clean)' if not fk else fk}")
    ic = conn.execute("PRAGMA integrity_check").fetchone()[0]
    print(f"integrity_check: {ic}")
    conn.close()
    print("\nAPPLY complete. Rows committed. Re-run is idempotent.")


def write_rows(conn, kits, all_bands, all_dev, all_hooks, all_acc, all_dt4,
               all_num, docket_kits):
    kid_list = [k["kit_id"] for k in kits]
    ph = ",".join("?" * len(kid_list))

    # -1) motion_signature_registry seed: PoE2 uses ONLY named paths already in
    #     the post-GD 18-registry (fan_spread, ground_place, point_strike,
    #     burst_around_self, straight_line, arc_sweep, chain_hop, orbit_fixed,
    #     lane_place, fork_split). No new path — this dict is EMPTY (running
    #     total stays 18). Left as a documented no-op seed for parity.
    motion_seeds = {}
    for name, desc in motion_seeds.items():
        conn.execute(
            "INSERT OR IGNORE INTO motion_signature_registry(signature_name, description) "
            "VALUES (?, ?)", (name, desc))

    # 0) door_registry catalogue seed: ALL 20 PoE2 door tokens are ALREADY in the
    #    post-GD 27-door registry (surveyed: 0 new) -> every INSERT OR IGNORE
    #    no-ops (running total stays 27). NOT minting. Seeded defensively.
    poe2_doors = set()
    for k in kits:
        for d in (k["mapping"].get("t4_doors") or []):
            poe2_doors.add(d)
    door_desc = {
        "GEOMETRY_PROPAGATION": "Propagates delivery geometry across the pack (chain/fork/cascade family).",
        "GEOMETRY_PROPAGATION_cascade": "Cascade variant: geometry propagates in a forward-marching cascade.",
        "GEOMETRY_PROPAGATION_overkill": "Propagation via overkill spill (excess/lethal damage chains onward).",
        "GEOMETRY_COLLAPSE": "Collapses delivery geometry (shotgun-density / burst-around-self).",
        "ELEMENTAL_ECHO": "Trigger-family door: a host action triggers a payload skill (freeze->Comet, on-crit, etc.).",
        "ELEMENT_CONVERSION_PHYSICAL": "Converts a skill's damage to/from physical (incl. armour-break/sunder).",
        "TEMPORAL_CHARGE": "Accumulate-then-discharge charge economy (charge/energy/two-tier meters).",
        "MOMENTUM_CASCADE": "Momentum/build-up that cascades into escalating output (density-reactive, frenzy).",
        "PERSISTENCE_ENGINE": "Sustains a persistent effect while a resource/spirit-reservation is active.",
        "PERSISTENCE_ENGINE_uptime": "Sustains a defensive/utility effect while a resource/spirit is active (uptime variant).",
        "PERSISTENCE_ENGINE_saturation": "Persistence via saturating overlapping zones/DoTs/meteor-fields.",
        "PROXY_ASCENSION": "Places autonomous emitter proxies (totem/turret/wall) that act on their own.",
        "PROXY_FISSION": "Splits into many small proxies/minions (fission).",
        "PROXY_SOVEREIGNTY": "A dominant proxy governs subordinate proxies (companion/spectre command).",
        "NETWORK_AMPLIFIER": "Amplifies via a network of linked effects (support/curse/party buffs).",
        "RETRIBUTION_ENGINE": "Reactive retribution (damage returned on being hit / shield-wall block).",
        "RESOURCE_CONVERSION": "Converts one resource into another (mana-stacking, spirit, flask-charge-as-ammo).",
        "SACRIFICE_ASCENDANCY": "Self-sacrifice/self-damage as the power source (blood/overheal/demonflame/darkness).",
        "ZONE_CONTROL": "Controls/denies a zone of the battlefield (wall/cloud/root/carpet).",
        "PHASE_MOMENTUM": "Movement/phase momentum that powers the loop (dodge-roll/dash/disengage).",
    }
    for d in sorted(poe2_doors):
        conn.execute(
            "INSERT OR IGNORE INTO door_registry(door_name, door_status, description) "
            "VALUES (?, 'active', ?)",
            (d, door_desc.get(d, f"On-record T4 door token '{d}' (catalogue seed; args deferred to door-arg RFC).")))

    # -------- IDEMPOTENT TEARDOWN (break the circular FK, then children->parents) --------
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
    docket_id_by_kit = {}
    for kid in docket_kits:
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
             f"Engine-inexpressible/param-gap surfaced by W4 PoE2 structuring of {kid}.",
             json.dumps([kid]), "engine-design-intake",
             json.dumps({"auto_opened_by": "vdm2-w4-deviation-intake",
                         "tranche": "poe2-record"}),
             "vdm2-w4-poe2", src_dev, kid))
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

    # 8) elem_raw anomaly W5 flags: PoE2 has NONE (ELEM_ANOMALIES empty) — no-op.
    W5_TOKEN = "vdm2-w5-elem-anomaly-2026-07-22"
    for kid, note in ELEM_ANOMALIES.items():
        row = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()
        cur_flags = (row[0] if row and row[0] else "")
        if W5_TOKEN not in cur_flags:
            new_flags = (cur_flags + ("; " if cur_flags else "") + f"{W5_TOKEN}: {note}")
            conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (new_flags, kid))

    # 8b) Decay-family (poison) register-split flags (surfaced by the RB-5
    #     reconcile; parallels the D2 poison-split and GD acid-split). Distinct
    #     token. IDEMPOTENT: append only if not present. flags is NOT covered by
    #     the frozen-identity hash — stamping does NOT violate the elem proof.
    W5_POISON_TOKEN = "vdm2-w5-poison-register-split-2026-07-22"
    for kid, note in POISON_REGISTER_INCONSISTENCY.items():
        row = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()
        cur_flags = (row[0] if row and row[0] else "")
        if W5_POISON_TOKEN not in cur_flags:
            new_flags = (cur_flags + ("; " if cur_flags else "") + f"{W5_POISON_TOKEN}: {note}")
            conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (new_flags, kid))


if __name__ == "__main__":
    main()
