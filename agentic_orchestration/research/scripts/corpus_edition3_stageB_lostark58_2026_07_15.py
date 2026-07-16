#!/usr/bin/env python3
"""
corpus_edition3_stageB_lostark58_2026_07_15.py — EDITION-III STAGE B

Ingest + key the Lost Ark class-kit tranche (gandalf-verified ACCEPT) at CLASS-ENGRAVING grain:
  agentic_orchestration/legolas/findings/2026-07-15-lost-ark-classkit-tranche/rows/<class>.jsonl
  = 29 files x 2 identity-path rows = 58 rows, la- prefix, NOT yet in corpus.

Authority: gandalf ONE-BATCH commission (gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md §2).
elrond OWNS the corpus.db write. TOOL script (curation), not engine code.

SOURCE OF TRUTH: the 29 JSONL row files (parsed directly here; source-anchored + reversible). The
  raw JSONL row is preserved verbatim in canon_engine_key.raw_json — no destructive transform.

=========================== LAWS (brief §2) ===========================

HONING-ECONOMY CONFOUND LAW (every row):
  LA power is gear-honing-indexed; kit-IDENTITY claims key ONLY from class design. The tranche
  annotates the confound per row (honing_confound + il_confound). We CARRY the confound into the
  curation notes (flags + mech_note) and NEVER let honing economy leak into treatment/function
  keys. Concretely: amp_val is derived from the CLASS-DESIGN tempo structure (BURST identity ->
  spiky; SUSTAINED -> flat), NEVER from the honing-scaled amp magnitude prose. tempo_val is
  design-cadence (BURST/SUSTAINED), not a honing-ceiling tier claim.

SIX NORMALIZATION DISPOSITIONS (gandalf verify flags — executed with provenance):
  1. group_context ABSENT on la-destroyer-* x2      -> normalize FALSE
       (index census names the 6 group-context rows; destroyer NOT among them).
  2. group_context ABSENT on la-slayer-* x2         -> normalize FALSE (same census backing).
  3. pull_carrier  ABSENT on la-slayer-* x2         -> normalize FALSE (index pull census EXACT:
       destroyer x2 only).
  4-5. la-souleater-* x2 legacy_engraving_system:false -> CORRECT to TRUE
       (in-row evidence: legacy_engraving_name present + engraving_debut 'Global December 2023';
        index finding 4 lists Ark-Passive natives as Valkyrie/Guardianknight/Wildsoul ONLY ->
        Souleater Nov/Dec 2023 is a legacy-converted class, not a native).
  6. la-sorceress-reflux pull_carrier:null (PENDING) -> RESOLVED via bounded targeted search
       ("Lost Ark Sorceress Reflux Reverse Gravity vacuum pull skill", executed 2026-07-15).
       FINDING: Reverse Gravity is a TRIPOD-conditioned lift-and-slam ("float upward then slam
       down") with a vacuum-GROUP side effect; the source frames it as push/lift ("won't LIFT
       push-immune bad guys"). Under the register v1.2 boundary rule (pull = INWARD HORIZONTAL
       displacement; force DIRECTION defines the level) + the intrinsic-only bar (tripod outcomes
       are a conditional-behavior/configuration layer, not base-skill-intrinsic), the evidence does
       NOT establish an intrinsic horizontal pull at class-identity grain. -> pull_carrier=FALSE,
       RESOLVED (not merely PENDING): the search RAN; the PENDING provenance is preserved in flags
       + mech_note. The raw control.ailments 'pull' token stays in raw_json (never destroyed) but
       does NOT set ctrl_function=pull. Keeps the pull census honest (Destroyer x2 only).

GROUP-SUPPORT ROWS (6, per index census — Bard/Paladin/Artist/Gunlancer/Valkyrie family):
  la-artist-full-bloom, la-bard-desperate-salvation, la-bard-true-courage,
  la-gunlancer-combat-readiness, la-paladin-blessed-aura, la-valkyrie-liberator.
  Keyed as COMBAT-KIT with group_context=TRUE preserved (C2 ruling: collected, NOT silently
  dropped, NOT force-negated). treatment/function keys reflect the SOLO-LEGIBLE identity; the
  group-context flag is carried first-class so downstream analysis can segment them.

UPGRADE-OWED confidence bands (index): Valkyrie <=0.8, Guardianknight <=0.8, Wildsoul 0.75-0.8,
  Souleater 0.85, Aeromancer tier-uncited. CARRIED per-row into flags (conf-band token). Keys are
  CATEGORICAL, so conf-banded NUMERIC values do not block keying. The official-patch-notes backfill
  stays a REGISTERED future legolas item, not this batch.

NAMING: "Dragonknight" (brief) = Guardianknight (official Global). Index resolution stands; kit_ids
  as-committed (la-guardianknight-*). No separate dragonknight rows.

PULL CENSUS (index, EXACT): 2 confirmed carriers, both Destroyer engraving-grain paths
  (la-destroyer-rage-hammer, la-destroyer-gravity-training). Both key ctrl_function=pull as the
  RIDER on a damage-primary identity (honing-confound-clean: pull is a class-design density
  mechanic, not gear). All 56 other paths: ctrl_function per the ailment map (NOT pull).

IDEMPOTENT: additive; the 58 rows upsert from the JSONL each run; the 469 survivor cell_keys +
  the Stage-A 7 rows are guarded untouched (survivor digest byte-identical before+after).
  Backup taken by caller (corpus.db.pre-edition3-2026-07-15-backup).
"""

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from corpus_cell_key_materialize_2026_07_13 import (  # noqa: E402
    serialize_cell_key, AILMENT_TO_FUNCTION, FUNCTION_PRIORITY,
)

ROOT = SCRIPTS.parent.parent.parent  # -> reincarnated-collaboration
DB = ROOT / "agentic_orchestration/research/curated/corpus.db"
ROWS_DIR = ROOT / "agentic_orchestration/legolas/findings/2026-07-15-lost-ark-classkit-tranche/rows"

PROVENANCE_TAG = "lost-ark-classkit-edition3-2026-07-15"
SOURCE_DATE = "2026-07-15"
ERAS = "la-kr-2019;la-global-2022;la-arkpassive-2025"

# ---- the 7 Stage-A rows + the 58 LA rows are additive; excluded from the survivor digest ----
STAGE_A_KIT_IDS = {
    "la-destroyer-vortex-gravity", "la-destroyer-gravity-impact", "la-destroyer-gravity-force",
    "la-destroyer-gravity-compression", "d4-spiritborn-vortex", "d3-wizard-black-hole",
    "di-cyclone-strike-monk-base",
}

# ---- normalization-disposition targets (brief §2) ----
GROUP_CONTEXT_ABSENT_FALSE = {  # dispositions 1 + 2
    "la-destroyer-rage-hammer", "la-destroyer-gravity-training",
    "la-slayer-predator", "la-slayer-punisher",
}
PULL_CARRIER_ABSENT_FALSE = {"la-slayer-predator", "la-slayer-punisher"}          # disposition 3
LEGACY_ENGRAVING_FALSE_TO_TRUE = {"la-souleater-nights-edge", "la-souleater-full-moon-harvester"}  # 4-5
SORCERESS_REFLUX = "la-sorceress-reflux"                                          # disposition 6

# The 6 group-context census rows (index) — asserted after normalization.
GROUP_SUPPORT_6 = {
    "la-artist-full-bloom", "la-bard-desperate-salvation", "la-bard-true-courage",
    "la-gunlancer-combat-readiness", "la-paladin-blessed-aura", "la-valkyrie-liberator",
}

# The 2 pull carriers (index EXACT census, engraving-grain).
PULL_CARRIERS_2 = {"la-destroyer-rage-hammer", "la-destroyer-gravity-training"}

# UPGRADE-OWED confidence bands (index) keyed by class slug.
UPGRADE_OWED = {
    "valkyrie": "conf<=0.8 (UPGRADE-OWED: Enlightenment node numerics; official patch notes backfill)",
    "guardianknight": "conf<=0.8 (UPGRADE-OWED: Embereth Orb fill rates; official patch notes backfill)",
    "wildsoul": "conf 0.75-0.8 (UPGRADE-OWED: mana-drain/meter-fill specifics; nexus+playlostark)",
    "souleater": "conf 0.85 (UPGRADE-OWED: edge-of-cutoff; live sources primary)",
    "aeromancer": "tier-uncited (UPGRADE-OWED: tier standings not primary-sourced; B-tier community consensus)",
}


# ============================ FIELD MAPPERS (source -> corpus cell_key vocab) ============================
# Source-anchored, documented, reversible. Every mapping is a stated rule over the tranche's own
# fields; the raw JSONL row is preserved verbatim so nothing is destructively transformed.

def map_attr(v):
    """prefix_claims.attr {CLOSE,NEAR,MEDIUM,FAR} -> engine attr proxy is not an attr axis here;
    the corpus attr_val is STR/DEX/INT/WIS. LA classes have a canonical stat per archetype; we take
    it from the row's element/class where legible, else leave NULL (honest — attr is not the load-
    bearing coord for the atlas plane). Warriors/MA=STR/DEX-lean; Mages=INT; Gunners=DEX; the
    tranche does not give a clean STR/DEX/INT/WIS token, so attr_val stays NULL (never-invent)."""
    return None  # LA rows do not carry a clean STR/DEX/INT/WIS attr; leave NULL (not plane-core)


def map_range(range_text, attr_text):
    """range_val in {melee,mid,ranged,dual}. Derive from the numeric range band + attr proximity."""
    t = (range_text or "").lower()
    # explicit long bands
    if any(x in t for x in ("15-30", "20-40", "20-30", "8-25", "5-30", "15-25")):
        return "ranged"
    if "0-24" in t or "8-20" in t or "5-20" in t or "5-15" in t:
        return "mid"
    if any(x in t for x in ("0-5", "0-6", "0-8", "0-4", "0-10", "melee")):
        # close band; attr CLOSE/NEAR confirms melee
        return "melee"
    if "0-15" in t or "3-12" in t or "12m aura" in t:
        return "mid"
    if "weapon-dependent" in t or "stance-dependent" in t or "form-dependent" in t:
        return "dual"
    # fall back on attr proximity
    a = (attr_text or "").upper()
    return {"CLOSE": "melee", "NEAR": "melee", "MEDIUM": "mid", "FAR": "ranged"}.get(a, "mid")


def map_tempo(tempo_text):
    """tempo_val in {low,med,high}. LA design-cadence: BURST -> high; SUSTAINED -> med.
    (Honing-confound-clean: this is the identity's DESIGN cadence, not a honing-ceiling tier.)"""
    t = (tempo_text or "").upper()
    if "BURST" in t:
        return "high"
    if "SUSTAINED" in t:
        return "med"
    return "med"


def map_amp(tempo_text):
    """amp_val in {flat,spiky,var}. HONING-CONFOUND LAW: derive from DESIGN structure, NOT the
    honing-scaled amp magnitude prose. BURST identity -> spiky (windowed amplification); SUSTAINED
    identity -> flat (steady output). This refuses to read a honing-tier number into the key."""
    t = (tempo_text or "").upper()
    if "BURST" in t:
        return "spiky"
    if "SUSTAINED" in t:
        return "flat"
    return "flat"


def map_commit(commit_text):
    """commit_val in {instant,wind-up,channel}. Direct (source vocab matches)."""
    c = (commit_text or "").lower()
    if "channel" in c:
        return "channel"
    if "wind-up" in c or "windup" in c:
        return "wind-up"
    if "instant" in c:
        return "instant"
    return "wind-up"


def map_proxy(proxy_val):
    """proxy_val in {solo,light,heavy}. LA proxy: None -> solo; drone/summon -> light (single/few
    proxies) unless the identity is pet-heavy. Summoner/Machinist have persistent pets -> light."""
    if proxy_val in (None, "", "null"):
        return "solo"
    if proxy_val in ("drone", "summon"):
        return "light"
    return "solo"


def map_movement(row):
    """mob_policy_while_casting -> cell_key #1. ALL LA rows: policy_while_casting='rooted' (skills
    root the caster during animation — the tranche's uniform, sourced finding). Honest source value
    -> 'rooted' (maps to ROOTED in the register crosswalk; lights on the movement gate)."""
    return (row.get("movement", {}) or {}).get("policy_while_casting") or "rooted"


def map_delivery(row):
    """delivery_value (cell_key #2 vocab). Source delivery {at-target, aura-pulse, projectile} are
    ALL legal DB delivery values -> preserve directly (source-anchored)."""
    v = (row.get("delivery", {}) or {}).get("value")
    return v if v in ("at-target", "aura-pulse", "projectile", "self-origin", "beam", "melee",
                      "orbit", "line") else "at-target"


def map_geometry(row):
    """geometry_value from delivery + footprint + control-shape. DB geometry vocab is rich; map to
    the closest existing bin (never invent a new geometry level)."""
    delivery = (row.get("delivery", {}) or {}).get("value")
    footprint = (row.get("footprint", {}) or {}).get("value")
    if delivery == "aura-pulse":
        return "aura"                          # persistent buff/HoT zone (Bard/Paladin/Artist support)
    if delivery == "projectile":
        return "multi_projectile" if footprint == "multi-point" else "single_target"
    # at-target family
    if footprint == "large-zone":
        return "ground_targeted_circle"        # AoE zone at target
    if footprint == "multi-point":
        return "chain"                         # multi-point strike sequence
    # small-radius melee identity
    return "melee_strike"


def map_defense(row):
    """def_bin in {tank,mitigate,evade,absorb,glass}. From defense.primary."""
    p = (row.get("defense", {}) or {}).get("primary")
    return {
        "dodge": "evade", "glass": "glass", "armor": "tank", "shield-absorb": "absorb",
        "sustain-leech": "mitigate", "hp-stack": "tank", "immunity": "mitigate",
        "shield": "absorb",
    }.get(p, "mitigate")


def map_economy(row):
    """economy_model in the pure enum. LA meter/identity-gauge = builder->spender loop ->
    'generator-spender' (matches the Destroyer pull rows' Gravity-Core system keying). LA cooldown
    model -> 'cooldown'."""
    m = (row.get("economy", {}) or {}).get("model")
    if m == "meter":
        return "generator-spender"
    if m == "cooldown":
        return "cooldown"
    return "generator-spender"


def derive_activation(row):
    """activation_val in {active,triggered}. LA identity skills are player-activated (Z/X key,
    manual) -> 'active'. No triggered-on-condition identity path in the tranche."""
    return "active"


def derive_dependency(row):
    """dependency_val in {one-shot, build->spend, apply->detonate}. LA identity gauges are
    builder->spender (blue skills build cores/meter -> purple/identity spends) -> 'build->spend'
    for meter economies; cooldown-model identities are 'one-shot'."""
    m = (row.get("economy", {}) or {}).get("model")
    return "build→spend" if m == "meter" else "one-shot"


def derive_ctrl(row, kit_id, is_pull_carrier):
    """Return (ctrl_treatment, ctrl_function, ailments_mapped_list, gaps_list).
    treatment: LA identity paths are DAMAGE-primary (or support). control.centrality core/rider/none
      maps: 'core' would be control-primary, but NO LA path is control-primary at identity grain
      (even Glaivier Control is a damage identity with CC riders) EXCEPT where centrality=core AND
      the core ailment is a genuine control fn. Destroyer Gravity Training has centrality=core with
      ailment 'pull' -> but pull is a density-RIDER on a damage identity (honing-confound-clean),
      NOT control-primary. So: treatment=damage for all combat identities; support paths keep
      treatment=damage on their solo-legible (damage/utility) form + group_context flag.
    function: from control.ailments via the Layer-1 map, EXCEPT the pull tokens (Edition-II aware):
      pull carriers (index EXACT census) key ctrl_function=pull; the raw 'pull' token on non-carriers
      (Sorceress Reflux, resolved false) does NOT key pull."""
    ctrl = row.get("control", {}) or {}
    ailments = list(ctrl.get("ailments") or [])
    # PULL handling (Edition-II aware): only the index-EXACT pull carriers key function=pull.
    if is_pull_carrier:
        return "damage", "pull", ailments, []
    # Non-carrier: map ailments to functions, but the raw 'pull' token (Reflux) must NOT map to
    # knockback (the stock map does that) NOR to pull (it's resolved-false). Drop 'pull' from the
    # function-derivation set for non-carriers; it stays in raw_json + ailments_mapped record.
    fn_tokens = [a for a in ailments if a != "pull"]
    matched = []
    for a in fn_tokens:
        fn = AILMENT_TO_FUNCTION.get(a)
        # 'knockdown' is a displacement token not in the stock map -> maps to knockback family
        if fn is None and a == "knockdown":
            fn = "knockback"
        # 'push' is outward displacement -> knockback
        if fn is None and a == "push":
            fn = "knockback"
        # 'dissonance' / 'synergy-debuff' are LA support-debuff tokens -> expose (damage-amp shred)
        if fn is None and a in ("dissonance", "synergy-debuff"):
            fn = "expose"
        if fn:
            matched.append(fn)
    if not matched:
        return "damage", "none", ailments, []
    for fn in FUNCTION_PRIORITY:
        if fn in matched:
            return "damage", fn, ailments, sorted(set(matched) - {fn})
    return "damage", "none", ailments, []


# ============================ NORMALIZATION (six dispositions) ============================
def normalize_row(row, kit_id):
    """Apply the six normalization dispositions, returning (row, provenance_notes list).
    NON-DESTRUCTIVE: the returned row's normalized values are used for KEYING; the ORIGINAL raw
    JSONL (raw_json) preserves the pre-normalization state."""
    notes = []
    # group_context normalization (dispositions 1+2)
    if kit_id in GROUP_CONTEXT_ABSENT_FALSE and "group_context" not in row:
        row = dict(row); row["group_context"] = False
        notes.append("group_context ABSENT -> normalized FALSE (index census: 6 group-context rows; "
                     "this kit not among them)")
    # pull_carrier normalization (disposition 3)
    if kit_id in PULL_CARRIER_ABSENT_FALSE and "pull_carrier" not in row:
        row = dict(row); row["pull_carrier"] = False
        notes.append("pull_carrier ABSENT -> normalized FALSE (index pull census EXACT: Destroyer x2 only)")
    # legacy_engraving correction (dispositions 4-5)
    if kit_id in LEGACY_ENGRAVING_FALSE_TO_TRUE and row.get("legacy_engraving_system") is False:
        row = dict(row); row["legacy_engraving_system"] = True
        notes.append("legacy_engraving_system false->TRUE CORRECTED (legacy_engraving_name present + "
                     "engraving_debut Global Dec 2023; index finding 4: Ark-Passive natives are "
                     "Valkyrie/Guardianknight/Wildsoul ONLY -> Souleater is legacy-converted)")
    # Sorceress Reflux pull_carrier resolution (disposition 6)
    if kit_id == SORCERESS_REFLUX and row.get("pull_carrier") is None:
        row = dict(row); row["pull_carrier"] = False
        notes.append("pull_carrier null->FALSE RESOLVED via bounded search (2026-07-15 'Lost Ark "
                     "Sorceress Reflux Reverse Gravity vacuum pull skill'): Reverse Gravity is a "
                     "TRIPOD-conditioned lift-and-slam (float-up + slam-down) with a vacuum-GROUP "
                     "side effect; source frames it push/lift ('won't LIFT push-immune'). Under the "
                     "register v1.2 boundary rule (pull=INWARD HORIZONTAL displacement) + intrinsic-"
                     "only bar (tripod outcome != base-skill-intrinsic), NOT an intrinsic pull. "
                     "PENDING provenance preserved; raw 'pull' ailment token kept in raw_json.")
    return row, notes


# ============================ UPSERT ============================
def upsert(cur, row, kit_id, class_slug):
    row, norm_notes = normalize_row(row, kit_id)

    is_pull_carrier = kit_id in PULL_CARRIERS_2
    group_context = bool(row.get("group_context", False))

    # coords
    mob = map_movement(row)
    delivery = map_delivery(row)
    geometry = map_geometry(row)
    tempo_txt = (row.get("prefix_claims", {}) or {}).get("tempo", {}).get("value")
    commit_txt = (row.get("prefix_claims", {}) or {}).get("commitment", {}).get("value")
    range_txt = (row.get("prefix_claims", {}) or {}).get("range", {}).get("value")
    attr_txt = (row.get("prefix_claims", {}) or {}).get("attr", {}).get("value")
    proxy_src = (row.get("prefix_claims", {}) or {}).get("proxy", {}).get("value")

    range_val = map_range(range_txt, attr_txt)
    tempo_val = map_tempo(tempo_txt)
    amp_val = map_amp(tempo_txt)
    commit_val = map_commit(commit_txt)
    proxy_val = map_proxy(proxy_src)
    defense = map_defense(row)
    economy = map_economy(row)
    activation = derive_activation(row)
    dependency = derive_dependency(row)
    treatment, function, ail_mapped, ail_gaps = derive_ctrl(row, kit_id, is_pull_carrier)

    # cell_key
    keyrow = {
        "mob_policy_while_casting": mob, "delivery_value": delivery, "amp_val": amp_val,
        "geometry_value": geometry, "ctrl_treatment": treatment, "ctrl_function": function,
        "def_bin": defense, "economy_model": economy, "proxy_val": proxy_val,
        "range_val": range_val, "tempo_val": tempo_val, "commit_val": commit_val,
        "activation_val": activation, "dependency_val": dependency,
    }
    cell_key = serialize_cell_key(keyrow)

    # ---- flags (JSON array): confound law + confidence band + normalization + group/pull context ----
    flags = [
        "honing-economy-confound:LA-power-gear-honing-indexed;identity-keyed-from-class-design-only",
        f"il_confound:{bool(row.get('il_confound', False))}",
        "grain:class-engraving",
    ]
    if row.get("legacy_engraving_system") is not None:
        flags.append(f"legacy_engraving_system:{bool(row.get('legacy_engraving_system'))}")
    if group_context:
        flags.append("group_context:true;context=group-support;solo-legible-identity-keyed;C2-preserved")
    if is_pull_carrier:
        flags.append("pull_carrier:true;rider-on-damage-identity;index-EXACT-census")
    if class_slug in UPGRADE_OWED:
        flags.append(f"UPGRADE-OWED:{UPGRADE_OWED[class_slug]}")
    for n in norm_notes:
        flags.append(f"normalization:{n}")

    # honing confound + confidence into mech_note (curation notes, human-legible)
    honing = row.get("honing_confound", "")
    mech_note = (
        f"[LA class-engraving grain] {row.get('folk_name','')} — "
        f"legacy_engraving={row.get('legacy_engraving_name','?')}; path={row.get('ark_passive_path','?')}. "
        f"HONING-CONFOUND (carried, never keyed into treatment/function): {honing[:600]} "
        f"| geo: {(row.get('geo_text') or '')[:300]}"
    )
    if norm_notes:
        mech_note += " || NORMALIZATION: " + " ; ".join(norm_notes)

    # ---- upsert canon_corpus ----
    cur.execute("""
        INSERT INTO canon_corpus
          (kit_id, folk_name, game, corpus_bucket, tier, canon_tier, eras, negative, source,
           is_system, unresolved, provenance_tag, source_date, attr_val, range_val, tempo_val,
           amp_val, proxy_val, commit_val, prefix_conf_provenance, key_completeness, mech_note,
           source_urls, era_year, stabilization_patch, pull_pending_vocab, architecture, flags, prov)
        VALUES (?,?, 'lost-ark','lost-ark','T1','deep',?,0,'canon',
                0,0,?,?,?,?,?, ?,?,?, 'la-classkit-steward-derived', ?, ?,
                ?, ?, ?, 0, 'class-engraving', ?, 'legolas-mode-b;elrond-curated')
        ON CONFLICT(kit_id) DO UPDATE SET
          folk_name=excluded.folk_name, eras=excluded.eras, provenance_tag=excluded.provenance_tag,
          source_date=excluded.source_date, attr_val=excluded.attr_val, range_val=excluded.range_val,
          tempo_val=excluded.tempo_val, amp_val=excluded.amp_val, proxy_val=excluded.proxy_val,
          commit_val=excluded.commit_val, key_completeness=excluded.key_completeness,
          mech_note=excluded.mech_note, source_urls=excluded.source_urls, era_year=excluded.era_year,
          stabilization_patch=excluded.stabilization_patch, architecture=excluded.architecture,
          flags=excluded.flags, prov=excluded.prov
    """, (
        kit_id, row.get("folk_name", kit_id), ERAS,
        PROVENANCE_TAG, SOURCE_DATE, attr_txt and map_attr(attr_txt), range_val, tempo_val,
        amp_val, proxy_val, commit_val,
        sum(1 for x in (range_val, tempo_val, amp_val, proxy_val, commit_val) if x is not None),
        mech_note,
        json.dumps(row.get("sources_used", [])),
        (row.get("era_year", {}) or {}).get("global"),
        (row.get("stabilization_patch") or "")[:500],
        json.dumps(flags),
    ))

    # ---- upsert canon_engine_key ----
    prov = {"source": "lost-ark-classkit-edition3", "curator": "elrond", "date": SOURCE_DATE,
            "grain": "class-engraving", "group_context": group_context,
            "pull_carrier": is_pull_carrier, "honing_confound": True,
            "normalizations": norm_notes}
    cur.execute("""
        INSERT INTO canon_engine_key
          (kit_id, geometry_value, ctrl_treatment, ctrl_function, ctrl_ailments_mapped,
           ctrl_ailment_gaps, def_bin, delivery_value, economy_model, activation_val,
           dependency_val, mob_policy_while_casting, mob_verbs, mob_skill_is_movement,
           econ_meter_type, resource_verbatim, row_class, flags, provenance_json, raw_json, cell_key)
        VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?, ?,?, 'combat-kit', ?, ?, ?, ?)
        ON CONFLICT(kit_id) DO UPDATE SET
          geometry_value=excluded.geometry_value, ctrl_treatment=excluded.ctrl_treatment,
          ctrl_function=excluded.ctrl_function, ctrl_ailments_mapped=excluded.ctrl_ailments_mapped,
          ctrl_ailment_gaps=excluded.ctrl_ailment_gaps, def_bin=excluded.def_bin,
          delivery_value=excluded.delivery_value, economy_model=excluded.economy_model,
          activation_val=excluded.activation_val, dependency_val=excluded.dependency_val,
          mob_policy_while_casting=excluded.mob_policy_while_casting,
          econ_meter_type=excluded.econ_meter_type, resource_verbatim=excluded.resource_verbatim,
          flags=excluded.flags, provenance_json=excluded.provenance_json, raw_json=excluded.raw_json,
          cell_key=excluded.cell_key
    """, (
        kit_id, geometry, treatment, function, json.dumps(ail_mapped),
        json.dumps(ail_gaps), defense, delivery, economy, activation,
        dependency, mob, json.dumps((row.get("movement", {}) or {}).get("verbs") or []),
        1 if (row.get("movement", {}) or {}).get("skill_is_movement") else 0,
        (row.get("economy", {}) or {}).get("meter_type"),
        (row.get("economy", {}) or {}).get("resource_verbatim"),
        json.dumps(flags), json.dumps(prov), json.dumps(row), cell_key,
    ))
    return cell_key, treatment, function, group_context, is_pull_carrier


# ============================ SURVIVOR + STAGE-A GUARD ============================
def frozen_rows(cur):
    """The 469 survivors + the 7 Stage-A rows must be byte-identical before+after (LA is additive).
    We guard BOTH: (a) the 469 non-mcd non-new survivors; (b) the 7 Stage-A cell_keys."""
    surv = cur.execute(
        "SELECT k.kit_id||'|'||k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND c.game!='mcd' ORDER BY k.kit_id"
    ).fetchall()
    la_new = {r.split(".")[0] for r in []}  # placeholder
    # exclude LA-58 (game='lost-ark') and Stage-A new kit_ids from the survivor set; keep Stage-A as
    # a SEPARATE frozen assertion.
    surv = [r[0] for r in surv if not r[0].startswith("la-destroyer-vortex")
            and r[0].split("|", 1)[0] not in STAGE_A_KIT_IDS
            and not _is_la58(r[0].split("|", 1)[0], cur)]
    return surv


_LA58_CACHE = None
def _is_la58(kit_id, cur):
    global _LA58_CACHE
    if _LA58_CACHE is None:
        _LA58_CACHE = {r[0] for r in cur.execute(
            "SELECT kit_id FROM canon_corpus WHERE game='lost-ark'").fetchall()}
    return kit_id in _LA58_CACHE


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    n_corpus_pre = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_key_pre = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    print("== EDITION-III STAGE B: Lost Ark 58-row curation (class-engraving grain) ==")
    print(f"  pre-state: corpus={n_corpus_pre}, engine_key={n_key_pre}")

    # ---- frozen guard PRE (469 survivors + 7 Stage-A rows) ----
    surv_pre_digest = hashlib.sha256("\n".join(frozen_rows(cur)).encode()).hexdigest()
    stageA_pre = {kid: cur.execute("SELECT cell_key FROM canon_engine_key WHERE kit_id=?", (kid,)).fetchone()[0]
                  for kid in sorted(STAGE_A_KIT_IDS)}

    # ---- parse + ingest 58 rows ----
    files = sorted(ROWS_DIR.glob("*.jsonl"))
    assert len(files) == 29, f"expected 29 row files, found {len(files)}"
    n = 0
    pull_keyed = []
    group_keyed = []
    tf_dist = {}
    for fp in files:
        class_slug = fp.stem
        for line in fp.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            kit_id = row["kit_id"]
            ck, treatment, function, gc, pc = upsert(cur, row, kit_id, class_slug)
            n += 1
            tf_dist[(treatment, function)] = tf_dist.get((treatment, function), 0) + 1
            if function == "pull":
                pull_keyed.append(kit_id)
            if gc:
                group_keyed.append(kit_id)
    assert n == 58, f"expected 58 rows ingested, got {n}"
    global _LA58_CACHE
    _LA58_CACHE = None  # refresh after insert

    # ---- disposition assertions ----
    # normalization proof: verify the corrected/normalized values landed
    def flags_of(kid):
        return cur.execute("SELECT flags FROM canon_engine_key WHERE kit_id=?", (kid,)).fetchone()[0]
    for kid in LEGACY_ENGRAVING_FALSE_TO_TRUE:
        assert "legacy_engraving_system:True" in flags_of(kid), f"{kid} legacy correction not applied"
    print(f"  [disp 4-5] souleater legacy_engraving_system false->TRUE applied OK")
    # pull carriers EXACTLY the 2 index-census rows
    assert set(pull_keyed) == PULL_CARRIERS_2, (
        f"pull-keyed LA rows != index EXACT census.\n  keyed: {sorted(pull_keyed)}\n"
        f"  expected: {sorted(PULL_CARRIERS_2)}")
    print(f"  [pull census] 2 pull carriers keyed function=pull (both Destroyer engraving-grain): "
          f"{sorted(pull_keyed)} OK")
    # Sorceress Reflux keyed NOT pull (resolved false)
    reflux_fn = cur.execute("SELECT ctrl_function FROM canon_engine_key WHERE kit_id=?",
                            (SORCERESS_REFLUX,)).fetchone()[0]
    assert reflux_fn != "pull", f"Reflux keyed function={reflux_fn} (must NOT be pull — resolved false)"
    print(f"  [disp 6] Sorceress Reflux resolved -> function={reflux_fn} (NOT pull; census honest) OK")
    # group-support rows EXACTLY the 6 index-census rows
    assert set(group_keyed) == GROUP_SUPPORT_6, (
        f"group_context rows != index census 6.\n  keyed: {sorted(group_keyed)}\n"
        f"  expected: {sorted(GROUP_SUPPORT_6)}")
    print(f"  [group-support] 6 group-context rows keyed combat-kit w/ context preserved: "
          f"{sorted(group_keyed)} OK")

    # ---- schema marker ----
    cur.execute("INSERT INTO corpus_schema_meta VALUES (?,?,?)", (
        "edition3-stageB-lostark58-2026-07-15", "2026-07-15T00:00:00Z",
        "Edition-III Stage B (elrond): Lost Ark 58-row class-engraving-grain curation. 29 classes x "
        "2 identity paths, la- prefix. HONING-ECONOMY CONFOUND LAW on every row (amp/tempo keyed "
        "from class-design cadence, never honing magnitude). Six normalizations applied w/ "
        "provenance: group_context absent->false (destroyer x2 + slayer x2); pull_carrier absent->"
        "false (slayer x2); souleater legacy_engraving false->TRUE (x2); sorceress-reflux "
        "pull_carrier null->FALSE (bounded search resolved: tripod lift-slam, not intrinsic pull). "
        "Pull census EXACT: 2 carriers (Destroyer rage-hammer + gravity-training) key function=pull "
        "rider on damage identity. 6 group-support rows keyed combat-kit w/ group_context=true "
        "preserved (C2). UPGRADE-OWED conf bands carried in flags (Valkyrie/Guardianknight/Wildsoul/"
        "Souleater/Aeromancer). Additive; 469 survivors + 7 Stage-A rows byte-identical. Raw JSONL "
        "preserved in raw_json (reversible).",
    ))

    # ---- frozen guard POST ----
    _LA58_CACHE = None
    surv_post_digest = hashlib.sha256("\n".join(frozen_rows(cur)).encode()).hexdigest()
    assert surv_post_digest == surv_pre_digest, (
        f"SURVIVOR DIGEST CHANGED during Stage B (must be additive)!\n"
        f"  before {surv_pre_digest}\n  after  {surv_post_digest}")
    for kid, ck in stageA_pre.items():
        now = cur.execute("SELECT cell_key FROM canon_engine_key WHERE kit_id=?", (kid,)).fetchone()[0]
        assert now == ck, f"Stage-A row {kid} cell_key changed during Stage B: {ck} -> {now}"
    print(f"  [frozen-guard] 469 survivors + 7 Stage-A rows byte-identical before+after OK")

    con.commit()

    # ---- report ----
    n_corpus = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_key = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    n_la = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE kit_id LIKE 'la-%'").fetchone()[0]
    n_pull = cur.execute("SELECT COUNT(*) FROM canon_engine_key WHERE ctrl_function='pull'").fetchone()[0]
    n_hybrid = cur.execute("SELECT COUNT(*) FROM canon_engine_key WHERE ctrl_treatment='hybrid'").fetchone()[0]
    print(f"\n  post-state: corpus={n_corpus} (+{n_corpus-n_corpus_pre}), engine_key={n_key} "
          f"(+{n_key-n_key_pre})")
    print(f"  la- rows total: {n_la} | ctrl_function='pull' rows (all sources): {n_pull} | hybrid: {n_hybrid}")
    print(f"  treatment×function distribution (LA 58): "
          f"{ {f'{t}/{f}': c for (t,f),c in sorted(tf_dist.items(), key=lambda x:-x[1])} }")
    con.close()
    print("STAGE B COMPLETE.")


if __name__ == "__main__":
    main()
