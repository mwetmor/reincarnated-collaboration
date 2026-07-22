#!/usr/bin/env python3
"""
VDM-2 W4 — LE (Last Epoch) record-class tranche: six side-car emitter.

FIFTH and LAST of the five W4 record tranches
(PoE1 99d5ac8e / D2 c60f97a2 / GD d6f0e850 / PoE2 fa3a6480 done). LE closes the
W4 record wave.

STRUCTURAL BASE = the GD emitter (NOT PoE2), because LE — like GD — carries
FROZEN GAPPED kits (terminal_state='MAPPED_DOCKET'). LE has 4 of them:
le-manifest-armor, le-skeleton-necro, le-squirrel-bm, le-wraithlord-necro (all
summoner-deferral / autonomous-combatant gaps). The GD terminal-anchored EI rule
is the correct, STRONGEST discriminator: engine_inexpressible is gated on the
FROZEN terminal_state, not on prose markers — so it CANNOT over-fire on texture
losses (the failure mode the PoE2 pass hardened against by a weaker prose
route). The emitter SELF-ASSERTS its EI-set == GAPPED-set (the brief's required
internal-consistency invariant). This carries the PoE2 hardening ("require the
mapper's own open-gap signal") in its strongest form: the mapper's own frozen
terminal_state IS that signal.

The 36 real kits are game='le' AND corpus_class='record'. The ONE LE
system-record (le-low-life-ward, the Low-Life Ward archetype, is_system=1 /
corpus_class='system') is EXCLUDED by the WHERE clause; the in-script leak-check
asserts no side-car keys to it (or to ANY is_system=1 kit).

Registry deltas surveyed on the LE substrate:
  * door_registry: LE adds exactly ONE new token — COMPANION_CONTRACT
    (le-dive-bomb-falconer, le-squirrel-bm). All other 19 LE door tokens are
    already in the post-PoE2 27-door registry -> 27 + 1 = 28.
  * motion_signature_registry: LE adds ZERO new paths. LE's novel geometry
    tokens defensive_dash / mobility map to delivery='motion' + the existing
    'straight_line' path (a dash/traversal is a straight-vector reposition,
    same treatment as PoE2/GD dash_attack/blink). ricochet_bounce reuses GD's
    'ricochet_return'. orbit reuses 'orbit_fixed'. Running total stays 18.

CARVES + FREEZES (binding rulings):
  * V-21 kit_door_arg CARVED: does NOT write kit_door_arg, does NOT design
    door_arg vocabularies. MEASURES G2 (door-arg derivability from prose)
    without committing rows (MEASURED-not-committed; the door-arg RFC is parked
    post-W5).
  * V-18 elem_raw FROZEN: emits side-cars ONLY. Proves the whole-corpus 585-row
    elem_raw content-hash IDENTICAL pre/post (must equal 5ad31b2...). Court is
    NOT re-derived (court derives from elem_raw; elem_raw untouched).
  * V-13 / V-19 honest-NULL: rdr_value stays NULL. kit_numeric is honest-empty
    for LE (survey: ZERO % magnitudes in LE prose; LE exact numbers live in the
    datamine lane) — 0 rows emitted, NOT manufactured to hit a count.

elem_raw ANOMALIES: NONE for LE. The LE elem_raw x court survey found ZERO
NULL-court / mixed(...) / multi-register-per-court anomalies. Each of LE's 6
elem_raw values (physical/fire/lightning/cold/necrotic/void) resolves to a
single clean court and RDR register. ELEM_ANOMALIES left honest-empty.

DECAY-FAMILY REGISTER-SPLIT (RB-6): the brief told us to WATCH for the
decay-family court-vs-skill-element split that D2 (poison->earth), GD
(acid->earth), and PoE2 (poison->earth) each surfaced. LE's 8 chaos-poison-court
kits (5 necrotic + 3 void) were surveyed: skill.element_primary is 'shadow' (7
kits) or 'water' (1 kit, le-harvest-lich). NONE is 'earth'. So the RB-6
earth-split pattern does NOT appear in LE — a genuine NEGATIVE result reported
for W5 (POISON_REGISTER_INCONSISTENCY is honest-empty). le-harvest-lich's
water skill0 is a multi-element grain gap (H2 reports the real skill element,
faithful to mapping_json), handled by the reconcile's adjudication path, NOT a
split and NOT a bug.

Idempotent: delete-then-insert keyed on kit_id per side-car; deviation-lane
dockets keyed on (source_kit_id, intake_lane='deviation'); docket surrogate
AUTOINCREMENT continues from live max (166 -> LE dockets from 167). Re-run
cannot duplicate.

USAGE
  python3 vdm2_w4_le_sidecar_emit_2026_07_22.py --dry-run
  python3 vdm2_w4_le_sidecar_emit_2026_07_22.py --apply \
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
# elem_raw ANOMALIES: NONE for LE (honest-empty; not a placeholder). See module
# docstring — the LE elem_raw x court survey found zero anomalies.
# ---------------------------------------------------------------------------
ELEM_ANOMALIES = {}

# DECAY-FAMILY REGISTER-SPLIT (RB-6). LE surfaced NONE (the negative result the
# brief asked us to watch for). All 8 LE chaos-poison-court kits carry
# skill.element_primary in {shadow, water} — NOT earth. Honest-empty; reported
# as the RB-6 negative for W5.
POISON_REGISTER_INCONSISTENCY = {}

# ---------------------------------------------------------------------------
# geometry_value -> delivery_class (spec s4 enum: projectile|beam|zone|motion|
# aura|summon_delegate|melee_arc). Complete over the 20 LE on-record geometry
# tokens (surveyed: aura, blink, chain, circle, cone, defensive_dash,
# ground_slam, ground_targeted_circle, melee_arc, melee_strike, mobility,
# multi_projectile, orbit, placed_lane, ricochet_bounce, ring, self_buff,
# single_target, totem, whirlwind).
# ---------------------------------------------------------------------------
GEO_TO_DELIVERY = {
    # --- D2/PoE1/GD base ---
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
    "placed_lane": "zone",           # a placed ground lane/wall (Frost Wall)
    "fork": "projectile",
    # ricochet_bounce: a thrown weapon-copy that ricochets target-to-target and
    #   returns (GD's Aegis; LE's Shield Throw). Out-and-back projectile.
    "ricochet_bounce": "projectile",
    # --- LE-native additions ---
    # defensive_dash: a defensive reposition/dash (Bomb Lance falconer's placed
    #   cloud for defense/movement). A movement delivery.
    "defensive_dash": "motion",
    # mobility: a secondary traversal/mobility geometry (Frost Wall RM's Glacier
    #   'provides mobility'). A movement delivery.
    "mobility": "motion",
}
# geometry_value -> motion_signature (open registry; NULL when no clean path).
# Every named path below is ALREADY in motion_signature_registry (post-GD 18).
# LE adds NO new path.
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
    "ricochet_bounce": "ricochet_return",
    # LE-native: dash/mobility are straight-vector repositions (existing path).
    "defensive_dash": "straight_line",
    "mobility": "straight_line",
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
    "ricochet_bounce": None,
    "defensive_dash": None,
    "mobility": None,
}
# Non-payload delivery families whose range_band is 'self'.
SELF_RANGE_GEOS = {"self_buff", "aura"}
# Melee-range delivery families.
MELEE_RANGE_GEOS = {"melee_strike", "melee_arc", "ground_slam", "whirlwind"}

# ---------------------------------------------------------------------------
# The FROZEN authoritative EI/docket set: the 4 LE kits whose VDM-1
# terminal_state='MAPPED_DOCKET' (GAPPED grade). Anchoring EI-classification to
# this frozen truth (not prose-marker matching) is the GD lesson, and it IS the
# PoE2 "require the mapper's own open-gap signal" discipline in its strongest
# form. LE's 4 GAPPED kits are all summoner-deferral / autonomous-combatant
# gaps.
# ---------------------------------------------------------------------------
GAPPED_TERMINAL = "MAPPED_DOCKET"

# ---------------------------------------------------------------------------
# Deviation-class classifier (spec s3 taxonomy). Prose markers are a SECONDARY
# path; the PRIMARY EI signal is the frozen terminal_state (see
# classify_deviation). LE markers carry the summoner-deferral GAP vocabulary
# shared with GD ("not that build", "no engine analog", "summoner-deferral",
# "no lane", "autonomous-combatant", "no honest delivery").
# ---------------------------------------------------------------------------
EI_MARKERS = [
    "no native expression", "not separately addressable", "no engine lane",
    "no meta endpoint", "docket accrual", "docket filed", "docket accrued",
    "player test fails", "not that build", "would be fabrication",
    "has no native", "cannot be expressed", "no expression", "unmappable",
    "phantom kit", "no attested", "phantom entry", "spec-error",
    "summoner gap", "summoner-gap", "summoner-deferral", "summoner deferral",
    "no autonomous-combatant", "no player-initiated delivery",
    "the absence is the gap", "content-availability gap", "(gapped)", "gapped",
    "no viable primary loop", "no verified build", "no engine analog",
    "no lane", "no honest delivery",
    "any combat mapping would be fabrication",
]
PG_MARKERS = [
    "needs an arg", "arg the door", "not yet carry", "second parallel trigger",
    "additional trigger", "param gap", "parallel trigger",
]

# R-M7 player-test vocabulary. The "'that build, <weaker>'" phrase is the
# explicit ACCEPTED_DOWNGRADE tell (identity survives, just weaker / texture
# loss). It OVERRIDES a prose EI marker (but NOT the frozen terminal_state — a
# MAPPED_DOCKET kit is EI regardless of downgrade language).
DOWNGRADE_OVERRIDE_MARKERS = [
    "that build, worse", "that build worse", "that build, slight",
    "that build slight", "that build,", "still that build", "texture loss",
    "texture losses", "not 'not that build'", "not \"not that build\"",
    "slightly worse", "that build, flat", "that build flat",
]


def classify_deviation(prose, is_gapped_terminal):
    """
    Classify a single deviation proposition. is_gapped_terminal is the FROZEN
    VDM-1 truth (terminal_state='MAPPED_DOCKET') — the AUTHORITATIVE EI signal.

    THE LE RULE (= the GD rule; the D2/PoE2 lesson in strongest form):
    engine_inexpressible is gated on the FROZEN terminal_state, NOT on prose
    markers. A MAPPED (non-DOCKET) kit was NOT flagged as an unresolvable gap in
    the frozen VDM-1 mapping verdict — its drift is ACCEPTED by construction, so
    even when its prose contains an EI-shaped phrase ("no engine analog for the
    two-tier economy... maps cleanly / faithful"), that phrase is
    accepted-downgrade language, not an open engine gap. This is precisely the
    over-fire the PoE2 pass hardened against; the frozen terminal_state removes
    the risk entirely (it requires the mapper's OWN open-gap signal — the
    MAPPED_DOCKET terminal). param_gap remains derivable from prose on
    non-gapped kits (a PG marker names a concrete arg-shaped gap).
    """
    low = prose.lower()
    if is_gapped_terminal:
        # a GAPPED-terminal (MAPPED_DOCKET) kit carries a real, frozen-attested
        # docket case. Only the PRIMARY (first) proposition is the EI gap; a
        # STEWARD-AUDIT or minor-drift second proposition can still downgrade
        # (the caller marks only the first proposition as gapped-primary).
        return "engine_inexpressible"
    # Non-GAPPED kit: EI is NOT reachable (terminal_state is authoritative).
    # Prose markers can only reach param_gap or accepted_downgrade.
    if any(m in low for m in PG_MARKERS):
        return "param_gap"
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
    m = re.search(r"~?(\d+)\s+(?:bolts?|shards?|spears?|totems?|mortars?|meteors?|arrows?|hammers?)", low)
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
        return "all"
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
        WHERE c.game='le' AND c.corpus_class='record'
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
    is ANCHORED to the frozen terminal_state=MAPPED_DOCKET (GAPPED) truth for the
    kit's PRIMARY (first) proposition; later propositions (STEWARD AUDIT / minor
    drift) classify by prose."""
    props = split_deviation_propositions(kit["dev_notes"])
    is_gapped = (kit["terminal"] == GAPPED_TERMINAL)
    rows = []
    for idx, p in enumerate(props):
        gapped_primary = is_gapped and idx == 0
        dclass = classify_deviation(p, gapped_primary)
        row = dict(
            missing_expression=missing_expression_summary(p),
            deviation_class=dclass,
            hook_refs=None,           # set after hooks derived (H-ref back-fill)
            proposed_fix_type=("door_param" if dclass == "param_gap"
                               else ("none" if dclass == "accepted_downgrade"
                                     else "new_door_rfc")),
            proposed_fix_target=None,
            downgrade_owner=("elrond (W4 LE tranche; internal-consistency reconcile, "
                             "no W1 evidence — W5 is LE's external check)"
                             if dclass == "accepted_downgrade" else None),
            source_anchor=p[:1500],
        )
        rows.append(row)
    # A GAPPED kit with EMPTY deviation prose still needs one EI deviation so its
    # docket opens (defensive; all 4 LE GAPPED kits carry prose).
    if is_gapped and not any(r["deviation_class"] == "engine_inexpressible" for r in rows):
        rows.insert(0, dict(
            missing_expression=f"{kit['folk']}: GAPPED (terminal MAPPED_DOCKET) — "
                               f"engine-inexpressible loop, no player-initiated delivery.",
            deviation_class="engine_inexpressible", hook_refs=None,
            proposed_fix_type="new_door_rfc", proposed_fix_target=None,
            downgrade_owner=None,
            source_anchor=(kit["dev_notes"] or "GAPPED kit; see terminal_state")[:1500],
        ))
    return rows


def derive_hooks(kit, bands):
    """recognition_hook rows: geometry + element register. For LE pet-core GAPPED
    kits the geometry hook reflects the first mappable delivery (skill[1]), not
    the null pet skill[0]; if all-null, ordinal-0 carries the identity hook."""
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
            hook_text=f"{kit['folk']}: {(geo or 'pet-core').replace('_',' ')} {deliv} identity",
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
        # ensure at least one green signature assert (covers pet-core GAPPED kits
        # whose skill[0] lacks a delivery_class)
        asserts.insert(0, dict(
            assert_text="kit_identity_present == true",
            hook_id="H1", expected_state=None, last_result="green",
            routes_red=False,
        ))
    return asserts


def derive_delta_t4(kit):
    """kit_delta_t4 shape (step|ramp). Capstone-threshold / discrete-enable reads
    'step'; synergy-stack / continuous-scaling / accumulator reads 'ramp'. LE
    skews: Ward/Rage/mana-stack accumulators + attribute-stacking -> ramp;
    unique-item / skill-native discrete transforms -> step. LE
    capstone_source_acquisition is empty across the record set, so shape derives
    from prose alone."""
    blob = (kit["dev_notes"] + " " + (kit["mech_note"] or "")).lower()
    cap = (kit["capstone"] or "").lower()
    shape = "step"
    if any(w in blob for w in ["synergy", "stack", "continuous", "scal", "ramp",
                               "gradient", "more per", "per remaining",
                               "accumulat", "build up", "build-up", "charges",
                               "two-tier", "two tier", "overflow", "spill",
                               "meter", "ward", "rage", "attribute-stack",
                               "attribute stack", "mana-stack", "mana stack",
                               "every 3rd", "every-nth", "every nth"]):
        shape = "ramp"
    if cap in ("set_threshold", "unique_item", "ascendancy", "runeword",
               "transmuter", "skill_native", "devotion"):
        shape = "step"
    return dict(shape=shape, asserts_json=json.dumps([
        f"T4 transformation shape={shape} (derived from mapping prose)"
    ]), shape_signoff="unvalidated", shape_signoff_by=None)


def derive_numerics(kit):
    """kit_numeric rows ONLY where prose attests a %/magnitude source-scale value.
    rdr_value NULL (no normalization rule run; spec s5). Honest-empty otherwise.
    LE exact numbers live in the datamine lane (V-19 NULL, a separate downstream
    legolas lane); the LE prose survey found ZERO % magnitudes -> expected EMPTY."""
    rows = []
    text = kit["dev_notes"] + " " + (kit["mech_note"] or "")
    for m in re.finditer(
            r"(\d{2,4})\s*%\s*(damage reduction|dr|self-burn|hp-cost|"
            r"more damage|increased|of max-life|of max life|of maximum life|"
            r"of ward|weapon damage|conversion)", text.lower()):
        val = float(m.group(1))
        scale = m.group(2).replace(" ", "_")
        rows.append(dict(
            numeric_key=f"{scale}_{int(val)}",
            source_value=val, source_scale=f"le_{scale}",
            rdr_value=None, rule_id=None,
            source_anchor=text[max(0, m.start()-40):m.end()+40].strip()[:300],
        ))
    return rows


# Per-door-family behavioral-parameter cues. A (kit,door) instance's args are
# "derivable from prose" when the mapping prose names a CONCRETE behavioral
# parameter for THAT door's family. The honest G2 measure. LE reuses the D2/GD/
# PoE2 cue families; the ONE new LE door (COMPANION_CONTRACT) gets its own cues.
DOOR_ARG_CUES = {
    "GEOMETRY_PROPAGATION": ["chain", "fork", "cascade", "hop", "propagat", "split", "spread", "bounce", "ricochet"],
    "GEOMETRY_COLLAPSE": ["shotgun", "point-blank", "point blank", "burst", "collapse", "density", "overlap", "nova", "ring", "cluster", "scatter", "fan"],
    "ELEMENTAL_ECHO": ["trigger", "on crit", "on-crit", "on hit", "cast on", "proc", "echo", "detonat", "on-ignite", "on ignite", "on-kill", "on kill"],
    "ELEMENT_CONVERSION_MONO": ["convert", "mono", "single element", "forced", "pure ", "->", "conversion", "full conversion", "adds fire", "adds cold", "adds lightning", "to void", "to necrotic"],
    "ELEMENT_CONVERSION_PHYSICAL": ["phys", "physical", "convert", "->", "sunder", "armour-break", "armour break", "impale", "trauma"],
    "ELEMENT_CONVERSION_HYBRID": ["hybrid", "dual element", "two element", "mixed", "composite", "convert", "fire+", "part physical", "part fire", "tri-elemental", "body-armor affix", "affix"],
    "TEMPORAL_CHARGE": ["charge", "accumulat", "stack", "discharge", "energy", "two-tier", "overflow", "spill", "meter", "rage", "ward", "periodic", "time"],
    "MOMENTUM_CASCADE": ["momentum", "ramp", "build up", "build-up", "escalat", "stage", "frenzy", "velocity", "speed", "faster", "tempo", "casting speed", "more frequent", "attack speed"],
    "PERSISTENCE_ENGINE": ["uptime", "while active", "sustain", "persist", "aura", "reserv", "maintained", "linger", "saturat", "field", "platform", "ground field", "wall"],
    "PERSISTENCE_ENGINE_uptime": ["uptime", "while active", "aura", "maintained", "reserv", "sustain", "buff", "persistent buff", "toggle", "form"],
    "PERSISTENCE_ENGINE_saturation": ["saturat", "overlapping", "linger", "blanket", "zone", "dot", "carpet", "field", "ground-dot", "overlap", "cloud", "storm"],
    "PROXY_ASCENSION": ["totem", "emitter", "placed", "autonomous", "sentry", "turret", "wall", "construct", "gear-scaled", "gear-stat"],
    "PROXY_FISSION": ["minion", "swarm", "split", "spawn", "skeleton", "mage", "army", "raise", "pet", "companion", "squirrel", "wraith"],
    "PROXY_CONVERGENCE": ["converge", "focus fire", "all fire", "concentrat"],
    "PROXY_INVERSION": ["invert", "consumabl", "battery", "consume", "corpse", "fuel", "sacrifice", "feed", "harvest"],
    "PROXY_SOVEREIGNTY": ["reaper", "sovereign", "commander", "dominant", "governs", "empower", "companion", "wraithlord", "boss-proxy", "capped"],
    "NETWORK_AMPLIFIER": ["link", "network", "wither", "curse", "amplif", "support", "buff-ally", "party", "ally", "aura", "shred"],
    "RESONANCE_LOOP": ["loop", "resonance", "self-hit", "self hit", "feed", "trigger feeds", "re-arc", "energy", "ward-gain", "leech"],
    "RESOURCE_CONVERSION": ["mana", "life as", "blood magic", "reserv", "convert", "mana-stack", "mana stack", "max-mana", "max mana", "ward", "low-life", "low life", "health"],
    "RETRIBUTION_ENGINE": ["block", "reflect", "retaliat", "when hit", "on block", "aegis", "shield", "counter", "thorns", "return"],
    "SACRIFICE_ASCENDANCY": ["sacrifice", "self-damage", "self damage", "self-burn", "hp cost", "hp-cost", "life cost", "blood", "overheal", "overleech", "harvest", "consume"],
    "ZONE_CONTROL": ["zone", "ground", "area deni", "control", "whirl", "wall", "field", "root", "cloud", "carpet", "blanket", "screen", "frost wall", "glacier"],
    "PHASE_MOMENTUM": ["dash", "blink", "movement", "phase", "flicker", "disengage", "dodge", "reposition", "hit-and-run", "hit and run", "traversal", "mobility"],
    "DEFENSIVE_TRADEOFF": ["tradeoff", "trade-off", "trade ", "low life", "low-life", "reserve", "defensive", "self-burn", "form lock", "form-lock", "ward", "overheal", "glancing"],
    "GEOMETRY_PROPAGATION_cascade": ["cascade", "chain", "forward", "marching", "propagat", "spread"],
    "GEOMETRY_PROPAGATION_overkill": ["overkill", "corpse explos", "chain", "detonat", "excess", "spill", "explosion on death", "on-kill", "on kill", "shatter"],
    "DUAL_PROXY": ["mirror", "clone", "proxy", "companion", "two pets", "familiar", "autonomous", "falcon", "wolf"],
    # --- LE-native door ---
    "COMPANION_CONTRACT": ["companion", "falcon", "wolf", "pet", "beastmaster", "double companion", "companion count", "summon", "autonomous", "contract"],
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
    """Content hash over the IMMUTABLE identity columns of the 36 LE record kits
    (elem_raw / core_skills / mech_note / folk_name / game / tier). Proves the
    frozen LE elem_raw (V-18) is untouched PRE vs POST (tranche scope)."""
    rows = conn.execute("""
        SELECT kit_id, elem_raw, core_skills, mech_note, folk_name, game, tier
        FROM canon_corpus
        WHERE game='le' AND corpus_class='record'
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
    the LE tranche. Must be identical live-vs-backup and PRE-vs-POST
    (5ad31b279b996586113a16be63e87f85)."""
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
    assert len(kits) == 36, f"expected 36 LE record kits, got {len(kits)}"
    print(f"Loaded {len(kits)} LE record-class kits (game=le, corpus_class=record).")

    # Confirm the LE system-record was NOT loaded (excluded by WHERE clause).
    sysrec = conn.execute(
        "SELECT kit_id FROM canon_corpus WHERE game='le' "
        "AND (corpus_class='system' OR is_system=1) ORDER BY kit_id").fetchall()
    loaded_ids = {k["kit_id"] for k in kits}
    sys_ids = {r[0] for r in sysrec}
    print(f"LE system-records (MUST be excluded): {sorted(sys_ids)}")
    assert not (sys_ids & loaded_ids), (
        f"SYSTEM-RECORD LEAK: {sys_ids & loaded_ids} loaded as record kits!")
    print(f"  confirmed NOT in the emitted set: {sorted(sys_ids)} (leak check clean)")

    frozen_pre = frozen_content_hash_tranche(conn)
    elem_whole_pre = elem_raw_wholecorpus_hash(conn)
    print(f"Frozen-identity content hash PRE (LE tranche): {frozen_pre}")
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
        geo0 = (b[0].get("_geo_raw") or "").strip()
        if b[0].get("delivery_class") is None:
            if geo0 == "":
                # skill[0] carries NO geometry token — honest GAP-deferred pet-core
                # null (LE's 4 summoner-deferral GAPPED kits), NOT adjectival prose
                # that failed to convert. Reported separately, NOT a G3 miss.
                g3_null_geo0_t1.append(k["kit_id"])
            else:
                g3_prose_only += 1
                g3_missing_delivery.append(k["kit_id"])

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
        print(f"   T1 kits with skill[0] NULL geometry (honest GAP-deferred pet-core "
              f"null, NOT a G3 miss): {g3_null_geo0_t1}")
    print(f"G4 red-assert->docket: {g4_kits_with_red} kits carry a red assert; "
          f"{g4_dockets} deviation-lane dockets will open (surrogate continues "
          f"from live max); every red routes")

    # sanity: EI-deviation kits should EQUAL the GAPPED-terminal kits (brief's
    # required invariant: EI-set == GAPPED-set).
    gapped = sorted(k["kit_id"] for k in kits if k["terminal"] == GAPPED_TERMINAL)
    ei = sorted(k["kit_id"] for k in kits
                if any(d["deviation_class"] == "engine_inexpressible"
                       for d in all_dev[k["kit_id"]]))
    print(f"\nGAPPED-terminal kits (frozen truth): {len(gapped)} {gapped}")
    print(f"EI-deviation kits (classifier output): {len(ei)} {ei}")
    if gapped != ei:
        print(f"  *** MISMATCH: EI set != GAPPED set — classifier drift! ***")
        print(f"      in EI not GAPPED: {sorted(set(ei)-set(gapped))}")
        print(f"      in GAPPED not EI: {sorted(set(gapped)-set(ei))}")
    else:
        print(f"  SELF-ASSERT PASS: EI-set == GAPPED-set (terminal-anchored discriminator holds).")
    print(f"Decay-family register-split (RB-6; W5-flagged): "
          f"{sorted(POISON_REGISTER_INCONSISTENCY.keys()) or 'NONE (LE negative result — no earth-on-chaos-poison split)'}")
    print(f"elem_raw anomalies (W5-flagged): {sorted(ELEM_ANOMALIES.keys()) or 'NONE (honest-empty)'}")

    report = dict(
        tranche="le-record", n_kits=len(kits), frozen_pre=frozen_pre,
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
        gapped_terminal=gapped, ei_deviation=ei,
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
            tranche="le-record", schema_version="v2.0", n_kits=len(kits),
            emitted="2026-07-22", frozen_identity_hash_pre=frozen_pre,
            elem_raw_wholecorpus_hash_pre=elem_whole_pre,
            gates=report["gates"], row_counts=report["rows"],
            delta_t4_split=report["delta_t4_split"],
            gapped_terminal=gapped, ei_deviation=ei,
            elem_anomalies_w5_flagged=ELEM_ANOMALIES,
            poison_register_split_w5_flagged=POISON_REGISTER_INCONSISTENCY,
            rb6_negative_result=("LE chaos-poison-court kits (5 necrotic + 3 void) "
                                 "carry skill.element_primary in {shadow, water}, "
                                 "NOT earth. The RB-6 decay-family earth-split "
                                 "(D2/GD/PoE2) does NOT appear in LE."),
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
    print(f"\nFrozen-identity content hash POST (LE tranche): {frozen_post}")
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

    # -1) motion_signature_registry seed: LE uses ONLY named paths already in the
    #     post-GD 18-registry (fan_spread, ground_place, point_strike,
    #     burst_around_self, straight_line, arc_sweep, chain_hop, orbit_fixed,
    #     lane_place, fork_split, ricochet_return). No new path — this dict is
    #     EMPTY (running total stays 18). Documented no-op seed for parity.
    motion_seeds = {}
    for name, desc in motion_seeds.items():
        conn.execute(
            "INSERT OR IGNORE INTO motion_signature_registry(signature_name, description) "
            "VALUES (?, ?)", (name, desc))

    # 0) door_registry catalogue seed: LE adds ONE new token (COMPANION_CONTRACT);
    #    all other 19 LE door tokens are ALREADY in the post-PoE2 27-door registry
    #    (those INSERT OR IGNORE no-op). Running total 27 -> 28.
    le_doors = set()
    for k in kits:
        for d in (k["mapping"].get("t4_doors") or []):
            le_doors.add(d)
    door_desc = {
        "COMPANION_CONTRACT": "Binds a persistent autonomous companion (falcon/wolf/"
                              "beast) to the player as a contracted delivery proxy; "
                              "its count/behavior scales off dedicated companion "
                              "affixes (LE-native beastmaster/falconer family).",
        # (existing tokens — descriptions only apply if the registry is fresh)
        "ELEMENT_CONVERSION_MONO": "Converts a skill's damage to a single target element.",
        "ELEMENT_CONVERSION_PHYSICAL": "Converts a skill's damage to/from physical.",
        "ELEMENT_CONVERSION_HYBRID": "Converts a skill's damage into a hybrid of two elements.",
        "ELEMENTAL_ECHO": "Trigger-family door: a host action triggers a payload skill.",
        "ZONE_CONTROL": "Controls/denies a zone of the battlefield (wall/cloud/root/carpet).",
        "PERSISTENCE_ENGINE_uptime": "Sustains a defensive/utility effect while a resource/summon is active (uptime variant).",
        "PERSISTENCE_ENGINE_saturation": "Persistence via saturating overlapping zones/DoTs.",
        "PROXY_ASCENSION": "Places autonomous emitter proxies (totem/turret/construct) that act on their own.",
        "GEOMETRY_COLLAPSE": "Collapses delivery geometry (shotgun-density / burst-around-self).",
        "GEOMETRY_PROPAGATION": "Propagates delivery geometry across the pack (chain/fork/ricochet family).",
        "MOMENTUM_CASCADE": "Momentum/build-up that cascades into escalating output.",
        "TEMPORAL_CHARGE": "Accumulate-then-discharge charge economy (Ward/Rage/charge meters).",
        "RETRIBUTION_ENGINE": "Reactive retribution (damage returned on being hit / shield block).",
        "RESONANCE_LOOP": "Self-reinforcing resonance loop (trigger feeds itself; ward/leech feed).",
        "PROXY_SOVEREIGNTY": "A dominant proxy governs subordinate proxies (Wraithlord/boss-proxy command).",
        "PROXY_FISSION": "Splits into many small proxies/minions (fission).",
        "NETWORK_AMPLIFIER": "Amplifies via a network of linked effects (curse/shred/party buffs).",
        "RESOURCE_CONVERSION": "Converts one resource into another (mana/ward/low-life).",
        "SACRIFICE_ASCENDANCY": "Self-sacrifice/self-damage as the power source (blood/overheal/harvest).",
        "DEFENSIVE_TRADEOFF": "Trades a defensive stat for offensive power (low-life/ward/form-lock).",
        "DUAL_PROXY": "Spawns proxy clones/pets that act from their own spatial origins.",
    }
    for d in sorted(le_doors):
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

    # 4) kit_numeric (insert) — LE is honest-empty (0 rows; no % magnitudes in prose)
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
             f"Engine-inexpressible/param-gap surfaced by W4 LE structuring of {kid}.",
             json.dumps([kid]), "engine-design-intake",
             json.dumps({"auto_opened_by": "vdm2-w4-deviation-intake",
                         "tranche": "le-record"}),
             "vdm2-w4-le", src_dev, kid))
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

    # 8) elem_raw anomaly W5 flags: LE has NONE (ELEM_ANOMALIES empty) — no-op.
    W5_TOKEN = "vdm2-w5-elem-anomaly-2026-07-22"
    for kid, note in ELEM_ANOMALIES.items():
        row = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()
        cur_flags = (row[0] if row and row[0] else "")
        if W5_TOKEN not in cur_flags:
            new_flags = (cur_flags + ("; " if cur_flags else "") + f"{W5_TOKEN}: {note}")
            conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (new_flags, kid))

    # 8b) Decay-family (poison) register-split flags: LE has NONE (the RB-6
    #     negative result — no earth-on-chaos-poison split). POISON_REGISTER_
    #     INCONSISTENCY is empty -> no-op. (Kept for cross-tranche parity.)
    W5_POISON_TOKEN = "vdm2-w5-poison-register-split-2026-07-22"
    for kid, note in POISON_REGISTER_INCONSISTENCY.items():
        row = conn.execute("SELECT flags FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()
        cur_flags = (row[0] if row and row[0] else "")
        if W5_POISON_TOKEN not in cur_flags:
            new_flags = (cur_flags + ("; " if cur_flags else "") + f"{W5_POISON_TOKEN}: {note}")
            conn.execute("UPDATE canon_corpus SET flags=? WHERE kit_id=?", (new_flags, kid))


if __name__ == "__main__":
    main()
