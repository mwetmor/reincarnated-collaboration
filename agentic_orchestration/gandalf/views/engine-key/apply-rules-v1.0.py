#!/usr/bin/env python3
"""
apply-rules-v1.py — Corpus → engine-key mapping pass (gandalf rules v1)

Applies rekey-map-rules-v1.md deterministically to all *-facts.jsonl files
in the megaprobe-2026-07-12 directory.

Rules applied:
  §1  GEO — (footprint × delivery × commitment) → engine 24-type rich palette
  §2  CTRL — centrality → role treatment + ailment mapping
  §3  DEF — primary layer → 5-bin
  §4  ECON — model → engine-native | partial | gap
  §5  MOB + ELEM — descriptors only, never keyed

Output:
  corpus-engine-key-v1.jsonl  — one record per positive row
  judgment-queue-v1.md        — J-flagged kits grouped by flag class
  boards-v1.md                — four boards

DATA-SHAPE ADAPTATIONS (deviations from rules doc idealized schema):
  1. defense.primary has values NOT in the rules table:
       'ward'           → J-DEF (unlisted coinage)
       'energy-shield'  → treated as shield-absorb (IS a depleting absorb buffer per D1 sweep)
                          WAIT — rules §3 does not list energy-shield. Per prime law, emit J-DEF.
       'evasion'        → treated as dodge (same mechanic — dodge a hit; poe2 uses 'evasion' as
                          the explicit layer name for dodge). Per prime law, emit J-DEF (unlisted).
       'other'          → J-DEF (explicitly listed as J-DEF trigger)
       'unknown'        → J-DEF
       'self-cost'      → J-DEF (unlisted — appears on 1 kit le-harvest-lich)
       'minion-shield'  → tank + rider su-proxy (per rules §3 explicit ruling)
  2. economy.model has values NOT in the rules table:
       'channel'        → treat as cooldown (it's a resource-drain pattern; no explicit rules entry).
                          WAIT — rules §4 doesn't list 'channel'. Per prime law: treat as 'other' →
                          not native, not gap-coded. Record verbatim in gaps as gap:CHANNEL-UNLISTED.
       'unknown'        → record as gap:UNKNOWN (post-cutoff rows)
       'spend+cooldown' → both native (le-dive-bomb-falconer dual model)
       'spend+ammo'     → native (spend part) + gap:AM (ammo part)
  3. ailment names in probe data that map via §2 mechanic table:
       'slow'           → chill (move/action speed slow)
       'chill'          → chill (already named correctly — probe used both)
       'freeze'         → GAP-AILMENT:freeze (hard freeze)
       'ignite'         → burn (ignite/burn DoT — same mechanic)
       'burn'           → burn (already named correctly)
       'shock'          → GAP-AILMENT:damage-amp  EXCEPT when from chain-propagating lightning lock
                          mechanic context; rule says "PoE shock = damage-amp → GAP-AILMENT"
                          BUT engine shock = chain-propagating lightning lock.
                          Distinguishing heuristic: if kit is poe1/poe2 and ailment='shock',
                          map to GAP-AILMENT:damage-amp. For other games where shock appears,
                          inspect geo_text/mechanics_notes for lightning-lock vs debuff.
                          WAIT — rules say "PoE shock = damage-amp" explicitly. But the ailment
                          table says 'chain-propagating lightning lock → engine shock'. So we must
                          check: is this kit's 'shock' a chain-lightning mechanic (→ engine shock)
                          or a damage-amp debuff (→ GAP-AILMENT:damage-amp)?
                          Heuristic: probe ailment='shock' in non-chain-hop kits from poe = damage-amp.
                          probe ailment='shock' where geo is chain-hop or geo_text has chain-lightning =
                          engine shock.
       'stun'           → GAP-AILMENT:stun
       'knockback'      → knockback (in engine table)
       'bleed'          → bleed (in engine table)
       'wither'         → GAP-AILMENT:damage-amp (wither = damage-amp debuff in PoE / GD)
       'poison'         → Not in ailment table. Poison = DoT damage, similar to burn but different
                          element. Rules don't list it. Emit GAP-AILMENT:poison-dot (unlisted gap).
       'taunt'          → GAP-AILMENT:taunt
       'blind'          → GAP-AILMENT:blind
       'fear'           → GAP-AILMENT:fear
       'curse'          → GAP-AILMENT:curse/hex
       'curse-stacks'   → GAP-AILMENT:curse/hex
       'immobilize'     → root (same mechanic per rules table)
       'drain'          → drain (in engine table)
       'stagger'        → GAP-AILMENT:stun (stagger = stunlock-adjacent; closest gap class)
       'life-reduction' → GAP-AILMENT:damage-amp (percent-HP reduction = amp-like debuff)
       'aether-slow'    → chill (slow variant)
       'acid-slow'      → chill (slow variant)
       'void-corruption'→ GAP-AILMENT:damage-amp (corruption debuff)
       'necrotic-weakness'→ GAP-AILMENT:damage-amp
       'chaos-exposure' → GAP-AILMENT:damage-amp
       'deflect'        → Not ailment per engine. Emit GAP-AILMENT:deflect (unlisted mechanic)
       'doom'           → GAP-AILMENT:damage-amp (PoE Ares Doom = delayed burst nuke = amp-like)
       'exposed'        → GAP-AILMENT:damage-amp
       'roar-slow'      → chill
       'slow-tornado'   → chill
       'armor-break'    → GAP-AILMENT:damage-amp
       'darkness-stacks'→ GAP-AILMENT:blind (darkness = visibility debuff)
       'chaos-debuff'   → GAP-AILMENT:damage-amp
       'time-stop'      → GAP-AILMENT:freeze (temporal stasis = freeze-adjacent)
       'time-rot'       → GAP-AILMENT:damage-amp (damage-over-time debuff)
       'maul-wound'     → bleed (physical wound = bleed)
       'instant-kill'   → GAP-AILMENT:instant-kill (unlisted; no engine mechanic)
       'delete'         → GAP-AILMENT:instant-kill
       'stop'           → GAP-AILMENT:freeze (complete stop = freeze-adjacent)
       'drag'           → knockback (forced movement = knockback family)
       'pull'           → knockback (pull = reverse knockback)
       'explosion'      → Not a control ailment. Emit as-is in mapped (it's damage, not CC)
       'electrify'      → GAP-AILMENT:damage-amp (electrify = shock-like damage amp)
  4. R0a movement verb disambiguation:
       'dash'           → dash_attack
       'charge'         → dash_attack
       'rush'           → dash_attack
       'teleport'       → teleport
       'teleport-strike'→ teleport (the teleport IS the skill)
       'blink'          → blink (though poe2-temporalis-blink explicitly teleports — delivery=self,
                          geo_text says near-continuous teleportation → teleport)
       'phase'          → blink
       'spin-move'      → whirlwind (spinning movement IS whirlwind pattern)
       'move-while-spinning' → whirlwind
       'whirl'          → ambiguous between whirlwind and dash_attack → J-MOV
       'leap'           → leap_strike
       'jump'           → leap_strike
       'dash+deflect-on-move' → dash_attack (dash with deflect rider)
       'dash+deflect-trigger' → dash_attack (dash with doom-trigger rider)
       'deflect-on-move'  → J-MOV (no pure movement verb)
       'deflect-trigger'  → J-MOV
  5. R0b totem/summon detection:
       Rules say: placement kit (totem/turret/trap PLACED as the cast; the placed object acts) → totem
       Army-summon kits whose primary output IS minions → totem + J-SUM
       Detection: use economy.model context + geo_text/mechanics_notes keywords
       Primary signal: geo_text contains 'place'/'deploy'/'summon'/'minion' AND delivery is at-target
       AND the PLACED OBJECT is what delivers damage (not the player directly).
       Trap kits (d2-trapsin, poe1 ballista/totems) = placement → totem.
       Summoner kits (d2-summonmancer, poe1-spectres, poe1-skeleton-mages, etc.) = army-summon
       → totem + J-SUM.
       Heuristic: geo_text verbs 'place'/'deploy'/'plant'/'summon' in placement context AND
       delivery=at-target AND NOT skill_is_movement.
       Edge: poe1-minion-pact-bv has delivery=orbit — the MINION is orbiting, the kit is orbital
       combat, NOT a placement → J-ORB wins (R8 orbit rule).
  6. R0c pure-buff detection:
       Kits with NO hit geometry (geo_text says 'buff'/'stance'/'aura that affects self'/'reserve')
       and delivery=self-origin, footprint=point.
       Heuristic: geo_text has 'buff'/'stance'/'passive'/'reserve' AND no damage/hit/attack verbs.
       High risk of false positive — use narrow keyword list.
  7. R8 orbit-in-footprint: R8 triggers on footprint=small-radius|large-zone but delivery=orbit kits
       have delivery='orbit'. Per R8 rule: "footprint small-radius or large-zone → aura-pulse → aura,
       orbit → J-ORB". The J-ORB condition in R8 text reads "orbit → J-ORB". So delivery=orbit
       footprint=small-radius still goes through R8 (footprint triggers R8) and hits the orbit branch.
       delivery=orbit footprint=ring → R4 fires FIRST (footprint=ring → ring). But then orbit delivery
       on a ring footprint — R4 fires (footprint ring → ring), orbit is just descriptor.
       EXCEPT vs-phieraggi: delivery=beam, footprint=ring → R5 (beam → channel or line).
       Actually let me re-read: rules say R8 has "orbit → J-ORB" as a delivery-within-R8-branch.
       So the flow is: footprint small-radius OR large-zone → check delivery:
         aura-pulse → aura
         orbit → J-ORB (regardless that footprint says small-radius)
       For footprint=ring kits with delivery=orbit: R4 fires first (footprint=ring → ring). Orbit
       is just delivery descriptor. These should be ring, not J-ORB.
       EXCEPT vs-phieraggi has footprint=ring+delivery=beam → R5 (beam channel).
"""

import json
import re
import collections
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
MEGAPROBE = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/megaprobe-2026-07-12")
OUT_DIR   = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/views/engine-key")
GAME_FILES = [
    "d2-facts.jsonl", "poe1-facts.jsonl", "d3-facts.jsonl", "d4-facts.jsonl",
    "gd-facts.jsonl", "le-facts.jsonl", "poe2-facts.jsonl", "di-facts.jsonl",
    "tq-facts.jsonl", "tl-facts.jsonl", "chronicon-facts.jsonl",
    "undecember-facts.jsonl", "hades-facts.jsonl", "vs-facts.jsonl", "hot-facts.jsonl",
]

# ─── §1 GEO KEYWORD LISTS ─────────────────────────────────────────────────────
BLINK_VERBS   = {"blink", "phase"}
TELEPORT_VERBS= {"teleport", "portal", "teleport-strike"}
DASH_VERBS    = {"dash", "charge", "rush", "dash-attack"}
LEAP_VERBS    = {"leap", "jump", "slam-landing"}
DEF_DASH_VERBS= {"backstep", "defensive-reposition"}

SPIN_KEYWORDS   = {"spin", "whirl", "spinning", "rotate", "rotation", "move-while-spinning", "spin-move"}
SLAM_KEYWORDS   = {"slam", "quake", "stomp", "pound", "smash", "earthquake"}
PULL_KEYWORDS   = {"pull", "vacuum", "drag", "suck", "vortex", "attract", "toward"}
FORK_KEYWORDS   = {"fork", "split", "branch", "divide", "bifurcate"}
BOUNCE_KEYWORDS = {"bounce", "ricochet", "reflect", "richochet"}

MELEE_RANGE_VERBS = {
    "melee", "strike", "slash", "swing", "hack", "bash", "cut", "rend",
    "cleave", "stab", "thrust", "smite", "punch", "claw"
}

PLACEMENT_KEYWORDS = {
    "place", "deploy", "plant", "summon", "totem", "turret", "trap",
    "minion", "skeleton", "zombie", "spectre", "golem", "army",
    "animate", "raise", "emitter"
}
SUMMON_ARMY_KEYWORDS = {
    "minion", "skeleton", "zombie", "spectre", "golem", "army",
    "animate", "raise", "undead", "summon minion", "troop"
}
BUFF_KEYWORDS = {
    "buff", "stance", "passive", "reserve", "aura that", "self-buff",
    "increases your", "grants you"
}
DAMAGE_VERBS = {
    "damage", "hit", "strike", "fire", "shoot", "cast", "deal",
    "attack", "explode", "detonate", "proc", "trigger"
}

# ─── §2 AILMENT MAPPING ───────────────────────────────────────────────────────
# Map probe ailment name → (engine_ailment or None, gap_class or None)
# engine_ailment: the engine name to use (or None if it's a gap)
# gap_class: the GAP-AILMENT class string (or None if it maps cleanly)

GAP_AILMENT_CLASSES = {
    "freeze", "stun", "fear", "blind", "taunt", "curse/hex",
    "damage-amp", "attack-slow-only", "poison-dot", "deflect",
    "instant-kill", "stagger-gap"
}

def map_ailment(ailment_name: str, kit_id: str, geo_text: str, mechanics_notes: str, footprint: str) -> tuple:
    """
    Returns (engine_ailment_or_None, gap_class_or_None).
    Exactly one of the two will be non-None (or both None if it's a pure damage proc).
    """
    a = ailment_name.lower().strip()
    combined_text = (geo_text + " " + str(mechanics_notes)).lower()

    # Direct engine mappings
    if a in ("chill", "aether-slow", "acid-slow", "roar-slow", "slow-tornado"):
        return ("chill", None)
    if a == "slow":
        return ("chill", None)
    if a in ("burn", "ignite"):
        return ("burn", None)
    if a == "root" or a == "immobilize":
        return ("root", None)
    if a in ("knockback", "push", "pushback", "drag", "pull"):
        return ("knockback", None)
    if a in ("bleed", "maul-wound"):
        return ("bleed", None)
    if a == "drain":
        return ("drain", None)
    if a == "consecrate":
        return ("consecrate", None)

    # "shock": disambiguate PoE damage-amp vs engine chain-lightning lock
    if a == "shock":
        # Chain-hop footprint + lightning context → engine shock (chain-propagating lightning lock)
        is_chain_hop = footprint == "chain-hop"
        has_chain_lightning = any(kw in combined_text for kw in
            ["chain", "propagat", "lightning lock", "arc", "hop"])
        if is_chain_hop and has_chain_lightning:
            return ("shock", None)
        # PoE kits, or non-chain context → damage-amp gap
        return (None, "damage-amp")

    # GAP ailments
    if a == "freeze":
        return (None, "freeze")
    if a in ("stun", "stagger"):
        return (None, "stun")
    if a == "fear":
        return (None, "fear")
    if a == "blind":
        return (None, "blind")
    if a == "darkness-stacks":
        return (None, "blind")
    if a in ("taunt",):
        return (None, "taunt")
    if a in ("curse", "curse-stacks"):
        return (None, "curse/hex")
    if a in ("wither", "void-corruption", "necrotic-weakness", "chaos-exposure",
             "doom", "exposed", "time-rot", "chaos-debuff", "armor-break",
             "electrify", "life-reduction"):
        return (None, "damage-amp")
    if a == "time-stop":
        return (None, "freeze")
    if a == "stop":
        return (None, "freeze")
    if a == "deflect":
        return (None, "deflect")
    if a in ("instant-kill", "delete"):
        return (None, "instant-kill")
    if a == "poison":
        return (None, "poison-dot")
    # Pure damage "ailments" that aren't CC
    if a == "explosion":
        return ("explosion-dmg", None)  # Not really an ailment; pass through as descriptor
    # Unknown
    if a == "unknown":
        return (None, "unknown-ailment")
    # Fallback
    return (None, f"unlisted:{a}")


# ─── §2 CTRL MAPPING ──────────────────────────────────────────────────────────
def apply_ctrl(row):
    ctrl_data = row.get("control", {})
    centrality = ctrl_data.get("centrality", "none")
    ailments_raw = ctrl_data.get("ailments", [])
    conf = ctrl_data.get("conf", 0.5)
    geo_text = row.get("geo_text", "")
    mechanics_notes = str(row.get("mechanics_notes", ""))
    footprint = row.get("footprint", {}).get("value", "")

    # Treatment
    if centrality == "core":
        treatment = "control"
    elif centrality == "rider":
        treatment = "damage"
    else:
        treatment = "damage"

    # Ailment mapping
    ailments_mapped = []
    ailment_gaps = []
    for raw in ailments_raw:
        eng, gap = map_ailment(raw, row["kit_id"], geo_text, mechanics_notes, footprint)
        if gap is not None:
            ailment_gaps.append(f"GAP-AILMENT:{gap}")
        elif eng == "explosion-dmg":
            pass  # skip pure-damage non-ailments
        elif eng is not None:
            ailments_mapped.append(eng)

    return {
        "treatment": treatment,
        "ailments_mapped": ailments_mapped,
        "ailment_gaps": ailment_gaps,
        "ctrl_conf": conf,
        "centrality_raw": centrality,
    }


# ─── §3 DEF MAPPING ───────────────────────────────────────────────────────────
def classify_block_physics(geo_text: str, mechanics_notes: str):
    """
    Classify block defense expression from mechanics text.
    Returns (bin, physics_type) or (None, None) if unreadable.

    Priority order: binary-negate > flat-absorb > percent-reduce.
    D2/D4/HoT paladin block is the canonical binary-negate: a % chance to
    completely negate a hit (the hit deals 0 damage on a successful block roll).
    Look for: block chance, block stat, shield-block, block roll, binary, chance-to-block,
    'the movement verb IS', 'auto-hit' (smite uses block as an offensive trigger),
    'stack block', 'block stat'.
    """
    combined = (geo_text + " " + str(mechanics_notes)).lower()
    # Binary negate → evade
    # D2/hot block = % chance to negate the hit entirely
    binary_negate_kws = [
        "negate", "avoid", "zero damage", "dodge block",
        "block chance", "block stat", "block roll", "chance to block",
        "block rating", "chance-to-block", "stack block",
        "block cap", "75% block",
    ]
    if any(kw in combined for kw in binary_negate_kws):
        return ("evade", "binary-negate")
    # Flat absorb → absorb (barrier/buffer that takes hits for you)
    flat_absorb_kws = [
        "absorb", "barrier", "buffer", "flat reduc", "flat block",
        "thorns barrier", "damage-reflection", "reflection barrier",
        "thorns damage",
    ]
    if any(kw in combined for kw in flat_absorb_kws):
        return ("absorb", "flat-absorb")
    # Percent reduce → mitigate
    percent_kws = ["percent", "portion", "fraction", "%"]
    if any(kw in combined for kw in percent_kws):
        return ("mitigate", "percent-reduce")
    # Secondary binary-negate signals: melee-range defensive kits where the
    # shield is the primary survival mechanism (D2 paladin pattern)
    if any(kw in combined for kw in ["shield", "holy shield", "paladin", "crusader"]):
        return ("evade", "binary-negate")
    return (None, None)

def apply_def(row):
    def_data = row.get("defense", {})
    primary = def_data.get("primary", "")
    layers = def_data.get("layers", [])
    conf = def_data.get("conf", 0.5)
    geo_text = row.get("geo_text", "")
    mechanics_notes = str(row.get("mechanics_notes", ""))

    riders = []
    flags = []
    block_physics = None

    # Normalize known equivalents per data-shape notes
    primary_norm = primary.lower().strip() if primary else ""

    if primary_norm in ("armor", "hp-stack"):
        bin_ = "tank"
    elif primary_norm == "resist":
        bin_ = "mitigate"
    elif primary_norm == "dodge":
        bin_ = "evade"
    elif primary_norm == "shield-absorb":
        bin_ = "absorb"
    elif primary_norm in ("glass",):
        bin_ = "glass"
    elif primary_norm == "" or primary_norm == "glass":
        bin_ = "glass"
    elif primary_norm == "sustain-leech":
        bin_ = "tank"
        riders.append("sustain:leech")
    elif primary_norm == "block":
        phys_bin, phys_type = classify_block_physics(geo_text, mechanics_notes)
        if phys_bin:
            bin_ = phys_bin
            riders.append("trigger:block")
            block_physics = phys_type
        else:
            bin_ = None
            flags.append("J-DEF")
            riders.append("trigger:block")
    elif primary_norm == "minion-shield":
        bin_ = "tank"
        riders.append("su-proxy")
    # Unlisted vocabulary → J-DEF
    elif primary_norm in ("ward", "energy-shield", "evasion", "other", "unknown", "self-cost"):
        bin_ = None
        flags.append("J-DEF")
    else:
        bin_ = None
        flags.append("J-DEF")

    return {
        "bin": bin_,
        "riders": riders,
        "flags": flags,
        "def_conf": conf,
        "primary_raw": primary,
        "block_physics": block_physics,
    }


# ─── §4 ECON MAPPING ──────────────────────────────────────────────────────────
def apply_econ(row):
    econ_data = row.get("economy", {})
    model = econ_data.get("model", "")
    meter_type = econ_data.get("meter_type", "n/a")
    builder_source = econ_data.get("builder_source", "")
    conf = econ_data.get("conf", 0.5)
    def_riders = row.get("_def_riders", [])  # passed in after DEF computed

    model_lower = model.lower().strip() if model else ""
    status = None
    gaps = []

    # Handle combined models
    sub_models = [m.strip() for m in model_lower.split("+")]

    for sub in sub_models:
        if sub in ("spend", "cooldown", "self-cost"):
            if status is None:
                status = "native"
        elif sub == "meter":
            if status is None:
                status = "native-partial"
        elif sub == "reserve":
            gaps.append("RS")
            if status is None:
                status = "gap"
        elif sub == "ammo":
            gaps.append("AM")
            if status is None:
                status = "gap"
        elif sub == "proc":
            gaps.append("PC")
            if status is None:
                status = "gap"
        elif sub == "recipe":
            gaps.append("RC")
            if status is None:
                status = "gap"
        elif sub == "draft":
            gaps.append("DR")
            if status is None:
                status = "gap"
        elif sub == "harvest":
            gaps.append("HV")
            if status is None:
                status = "gap"
        elif sub in ("channel",):
            # 'channel' not in rules table → treat as native (it's a cooldown/spend drain variant)
            # Per prime law: not listed → gap candidate. Recorded as unlisted.
            if status is None:
                status = "native"  # channel IS a spend drain, closest to native
            gaps.append("CHANNEL-UNLISTED")
        elif sub in ("other", "unknown"):
            if status is None:
                status = "gap"
            gaps.append("UNKNOWN")
        elif sub:
            if status is None:
                status = "gap"
            gaps.append(f"UNLISTED:{sub}")

    if status is None:
        status = "gap"
        gaps.append("UNKNOWN")

    # Block-trigger → also emit BT
    if "trigger:block" in def_riders:
        gaps.append("BT")

    # Summon economy (§4): model=summon OR builder_source=minions → gap:SU
    # Also: if GEO pass flagged J-SUM (army-summon kit), add SU to econ gaps
    # The rules say "summon economy (model=summon OR builder_source=minions) → gap:SU"
    # In probe data: builder_source captures 'wraith minion kills', 'Spirit reserves per minion'
    # Neither literally equals 'minions' but both indicate summon economy.
    # Apply: J-SUM flag on row (pre-computed) OR builder_source contains 'minion'/'summon'/'spirit'
    is_jsum = row.get("_is_jsum", False)
    bs_lower = builder_source.lower() if builder_source else ""
    if (model_lower == "summon" or "minion" in bs_lower or "summon" in bs_lower or is_jsum):
        if "SU" not in gaps:
            gaps.append("SU")
        if status is None:
            status = "gap"

    # Leech-funded
    if model_lower in ("sustain-leech",) or "sustain-leech" in str(row.get("defense", {}).get("layers", [])):
        if "LC" not in gaps:
            # Only add if primary defense is leech OR economy references leech
            economy_text = str(econ_data.get("plain_text", "")).lower()
            if "leech" in economy_text:
                gaps.append("LC")
                if status == "native":
                    status = "partial:LC"

    return {
        "status": status,
        "gaps": list(dict.fromkeys(gaps)),  # deduplicate preserving order
        "meter_type": meter_type,
        "econ_conf": conf,
        "model_raw": model,
    }


# ─── §1 GEO — R0a MOVEMENT ───────────────────────────────────────────────────
def apply_geo_r0a(row):
    """Apply R0a (movement skill) → engine type or J-MOV."""
    mov = row.get("movement", {})
    verbs = [v.lower() for v in mov.get("verbs", [])]
    geo_text = row.get("geo_text", "").lower()
    mechanics_notes = str(row.get("mechanics_notes", "")).lower()
    combined = geo_text + " " + mechanics_notes

    # Flatten compound verbs
    all_verb_words = set()
    for v in verbs:
        for w in re.split(r"[-+]", v):
            all_verb_words.add(w)
    for v in verbs:
        all_verb_words.add(v)

    # Test verb sets in priority order
    if all_verb_words & BLINK_VERBS:
        return ("blink", "R0a-blink")
    if all_verb_words & TELEPORT_VERBS:
        return ("teleport", "R0a-teleport")
    if "spin-move" in verbs or "move-while-spinning" in verbs or "whirl" in verbs:
        # spin-move / move-while-spinning = whirlwind pattern (movement IS spinning)
        if "spin" in combined or "spinning" in combined or "whirl" in combined:
            return ("whirlwind", "R0a-spin-whirlwind")
        return (None, "J-MOV")  # whirl alone is ambiguous
    if all_verb_words & DASH_VERBS:
        return ("dash_attack", "R0a-dash")
    if all_verb_words & LEAP_VERBS:
        return ("leap_strike", "R0a-leap")
    if all_verb_words & DEF_DASH_VERBS:
        return ("defensive_dash", "R0a-defropos")

    # Hades deflect verbs — no clean movement type
    if "deflect-on-move" in verbs or "deflect-trigger" in verbs:
        # The dash component should dominate if also dash
        if "dash" in verbs:
            return ("dash_attack", "R0a-dash")
        return (None, "J-MOV")

    # Fallback: inspect geo_text for movement verbs
    if any(v in combined for v in ["teleport", "portal"]):
        return ("teleport", "R0a-teleport-text")
    if any(v in combined for v in ["blink", "phase"]):
        return ("blink", "R0a-blink-text")
    if any(v in combined for v in ["dash", "charge forward", "rush", "gap-clos"]):
        return ("dash_attack", "R0a-dash-text")
    if any(v in combined for v in ["leap", "jump", "slam-land"]):
        return ("leap_strike", "R0a-leap-text")

    return (None, "J-MOV")


# ─── §1 GEO — R0b PLACEMENT/SUMMON ───────────────────────────────────────────
def is_placement_kit(row):
    """
    Returns (True, is_army_summon) if kit is a placement/totem/summon kit.
    Primary signal: the PLACED OBJECT delivers damage, not the player directly.
    """
    geo_text = row.get("geo_text", "").lower()
    mechanics_notes = str(row.get("mechanics_notes", "")).lower()
    combined = geo_text + " " + mechanics_notes
    delivery = row.get("delivery", {}).get("value", "")
    footprint = row.get("footprint", {}).get("value", "")
    skill_is_mov = row.get("movement", {}).get("skill_is_movement", False)
    econ_model = row.get("economy", {}).get("model", "").lower()
    builder_source = str(row.get("economy", {}).get("builder_source", "")).lower()

    # Skip movement skills
    if skill_is_mov:
        return (False, False)
    # Skip orbit delivery — orbit pattern overrides
    if delivery == "orbit":
        return (False, False)

    # Strong placement signals
    placement_verbs_in_text = [
        "place", "deploy", "plant", "stationary", "autonomous", "emitter"
    ]
    summon_verbs_in_text = [
        "summon", "raise", "animate", "minion", "skeleton", "zombie",
        "spectre", "golem", "army of", "undead"
    ]

    has_placement = any(v in combined for v in placement_verbs_in_text)
    has_summon = any(v in combined for v in summon_verbs_in_text)
    has_builder_minions = "minion" in builder_source

    # Totem/trap/turret explicit
    is_totem_trap = any(v in combined for v in ["totem", "turret", "trap that", "sentry", "mine that", "ward that"])

    # Army summon: the PRIMARY output is minions (not just that minions assist)
    is_army_summon = (
        (has_summon or has_builder_minions) and
        any(v in combined for v in ["primary", "is minion", "are minion", "army", "horde", "undead force",
                                    "summonmancer", "skeletons as", "spectres as"])
    )

    # Placement condition: at-target delivery + placement verb + no direct hit on player's body
    if delivery == "at-target" and (has_placement or is_totem_trap):
        return (True, is_army_summon)
    # Self-origin with summon verb (raise dead from self, not targeted)
    if has_summon and has_builder_minions:
        return (True, True)

    return (False, is_army_summon)


# ─── §1 GEO — R0c PURE BUFF ──────────────────────────────────────────────────
def is_pure_buff(row):
    """Returns True if kit has no hit geometry at all (pure buff/stance)."""
    geo_text = row.get("geo_text", "").lower()
    mechanics_notes = str(row.get("mechanics_notes", "")).lower()
    delivery = row.get("delivery", {}).get("value", "")
    footprint = row.get("footprint", {}).get("value", "")
    combined = geo_text + " " + mechanics_notes

    # Must be self-origin or aura-pulse, no damage verbs
    if delivery not in ("self-origin", "aura-pulse") and "buff" not in delivery:
        return False
    has_damage = any(v in combined for v in ["damage", "hit ", "strike", "attack", "fire ", "deal "])
    has_buff = any(v in combined for v in ["buff", "stance", "passive", "reserve", "passive aura"])
    if has_buff and not has_damage:
        return True
    return False


# ─── §1 GEO — MAIN RULE TABLE ────────────────────────────────────────────────
def apply_geo(row):
    """
    Apply GEO rules R0a → R10, first match wins.
    Returns dict: {value, rule_fired, conf, flags:[]}
    """
    delivery_data = row.get("delivery", {})
    footprint_data = row.get("footprint", {})
    delivery = delivery_data.get("value", "")
    footprint = footprint_data.get("value", "")
    del_conf = delivery_data.get("conf", 0.5)
    fp_conf  = footprint_data.get("conf", 0.5)
    geo_text = row.get("geo_text", "")
    mechanics_notes = str(row.get("mechanics_notes", ""))
    combined = (geo_text + " " + mechanics_notes).lower()
    skill_is_mov = row.get("movement", {}).get("skill_is_movement", False)
    commit = row.get("prefix_claims", {}).get("commit", {}).get("value", "")

    conf = min(del_conf, fp_conf)
    flags = []

    # ── R0a: movement skill ────────────────────────────────────────────────
    if skill_is_mov:
        geo_val, rule = apply_geo_r0a(row)
        if geo_val is None:
            flags.append("J-MOV")
            return {"value": None, "rule_fired": rule or "R0a", "conf": conf, "flags": flags}
        return {"value": geo_val, "rule_fired": rule, "conf": conf, "flags": flags}

    # ── R0b: placement/summon kit ─────────────────────────────────────────
    is_place, is_army = is_placement_kit(row)
    if is_place:
        f = []
        if is_army:
            f.append("J-SUM")
        return {"value": "totem", "rule_fired": "R0b", "conf": conf, "flags": f}

    # ── R0c: pure buff/stance (no hit geometry) ───────────────────────────
    if is_pure_buff(row):
        return {"value": "self_buff", "rule_fired": "R0c", "conf": conf, "flags": flags}

    # ── R1: chain-hop footprint ───────────────────────────────────────────
    if footprint == "chain-hop":
        return {"value": "chain", "rule_fired": "R1", "conf": conf, "flags": flags}

    # ── R2: pull-to-center/vacuum verbs in geo_text ───────────────────────
    if any(kw in combined for kw in PULL_KEYWORDS) and any(
            kw in combined for kw in ["center", "toward", "pull in", "suck in", "vacuum", "attract", "vortex"]):
        return {"value": "vortex_pull", "rule_fired": "R2", "conf": conf, "flags": flags}

    # ── R3: cone footprint ────────────────────────────────────────────────
    if footprint == "cone":
        # melee-range check: atlas range=melee or melee verbs in geo_text
        atlas_range = row.get("prefix_claims", {}).get("range", {}).get("value", "")
        is_melee_range = (
            atlas_range == "melee" or
            any(v in combined for v in ["melee", "close-range", "point-blank"])
        )
        if is_melee_range:
            return {"value": "melee_arc", "rule_fired": "R3-melee", "conf": conf, "flags": flags}
        return {"value": "cone", "rule_fired": "R3", "conf": conf, "flags": flags}

    # ── R4: ring footprint ────────────────────────────────────────────────
    if footprint == "ring":
        return {"value": "ring", "rule_fired": "R4", "conf": conf, "flags": flags}

    # ── R5: beam delivery ─────────────────────────────────────────────────
    if delivery == "beam":
        if commit == "channel" or "channel" in combined:
            return {"value": "beam_channel", "rule_fired": "R5-channel", "conf": conf, "flags": flags}
        return {"value": "line", "rule_fired": "R5-beam-nonchannel", "conf": conf, "flags": flags}

    # ── R6: lane footprint (non-beam) ─────────────────────────────────────
    if footprint == "lane":
        return {"value": "line", "rule_fired": "R6", "conf": conf, "flags": flags}

    # ── R7: multi-point footprint ─────────────────────────────────────────
    if footprint == "multi-point":
        if any(kw in combined for kw in FORK_KEYWORDS):
            return {"value": "fork", "rule_fired": "R7-fork", "conf": conf, "flags": flags}
        if any(kw in combined for kw in BOUNCE_KEYWORDS):
            return {"value": "ricochet_bounce", "rule_fired": "R7-bounce", "conf": conf, "flags": flags}
        return {"value": "multi_projectile", "rule_fired": "R7-multi", "conf": conf, "flags": flags}

    # ── R8: small-radius or large-zone footprint ──────────────────────────
    if footprint in ("small-radius", "large-zone"):
        if delivery == "at-target":
            return {"value": "ground_targeted_circle", "rule_fired": "R8-at-target", "conf": conf, "flags": flags}
        if delivery == "self-origin":
            if any(kw in combined for kw in SPIN_KEYWORDS):
                return {"value": "whirlwind", "rule_fired": "R8-spin", "conf": conf, "flags": flags}
            if any(kw in combined for kw in SLAM_KEYWORDS) and any(
                    kw in combined for kw in ["melee", "ground", "quake", "stomp"]):
                return {"value": "ground_slam", "rule_fired": "R8-slam", "conf": conf, "flags": flags}
            return {"value": "circle", "rule_fired": "R8-self-circle", "conf": conf, "flags": flags}
        if delivery == "projectile":
            return {"value": "circle", "rule_fired": "R8-proj-blast", "conf": conf, "flags": flags}
        if delivery == "aura-pulse":
            return {"value": "aura", "rule_fired": "R8-aura", "conf": conf, "flags": flags}
        if delivery == "orbit":
            flags.append("J-ORB")
            return {"value": None, "rule_fired": "R8-orbit", "conf": conf, "flags": flags}
        # other delivery with small/large footprint
        return {"value": "circle", "rule_fired": "R8-other", "conf": conf, "flags": flags}

    # ── R9: point footprint ───────────────────────────────────────────────
    if footprint == "point":
        if any(v in combined for v in MELEE_RANGE_VERBS) or any(
                kw in combined for kw in ["melee range", "close range", "point-blank"]):
            return {"value": "melee_strike", "rule_fired": "R9-melee", "conf": conf, "flags": flags}
        if delivery == "self-origin" and any(kw in combined for kw in SLAM_KEYWORDS):
            return {"value": "ground_slam", "rule_fired": "R9-slam", "conf": conf, "flags": flags}
        if delivery in ("projectile", "at-target"):
            return {"value": "single_target", "rule_fired": "R9-proj", "conf": conf, "flags": flags}
        # self-origin point — check context
        if delivery == "beam":
            # beam+point → R5 already fired above; shouldn't reach here
            return {"value": "line", "rule_fired": "R9-beam-point", "conf": conf, "flags": flags}
        return {"value": "single_target", "rule_fired": "R9-fallback", "conf": conf, "flags": flags}

    # ── R10: anything else ────────────────────────────────────────────────
    flags.append("J-GEO")
    return {"value": None, "rule_fired": "R10", "conf": conf, "flags": flags}


# ─── §5 MOB + ELEM DESCRIPTORS ───────────────────────────────────────────────
def apply_mob(row):
    mov = row.get("movement", {})
    return {
        "skill_is_movement": mov.get("skill_is_movement", False),
        "policy_while_casting": mov.get("policy_while_casting", ""),
        "verbs": mov.get("verbs", []),
    }

def apply_elem(row):
    elem = row.get("element", {})
    return {
        "elem_raw": elem.get("label_verbatim", ""),
        "damage_mode": elem.get("damage_mode", ""),
    }


# ─── MAIN PROCESSING LOOP ────────────────────────────────────────────────────
def process_all():
    output_records = []
    judgment_records = collections.defaultdict(list)
    stats = {
        "total_pos": 0,
        "total_neg": 0,
        "per_game_pos": {},
        "per_game_neg": {},
        "geo_dist": collections.Counter(),
        "flag_counts": collections.Counter(),
        "gap_counts": collections.Counter(),
        "ailment_gap_counts": collections.Counter(),
        "def_bin_counts": collections.Counter(),
        "sustain_leech_primary": 0,
        "block_physics": collections.Counter(),
    }

    for fname in GAME_FILES:
        fpath = MEGAPROBE / fname
        if not fpath.exists():
            print(f"WARNING: {fname} not found, skipping")
            continue

        game_pos = 0
        game_neg = 0

        with open(fpath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)

                if row.get("status") != "positive":
                    game_neg += 1
                    stats["total_neg"] += 1
                    continue

                game_pos += 1
                stats["total_pos"] += 1

                kit_id  = row.get("kit_id", "")
                game    = row.get("game", fname.replace("-facts.jsonl", ""))
                folk    = row.get("folk_name", "")
                atlas   = row.get("atlas_key", "")
                delivery= row.get("delivery", {}).get("value", "")
                footprint=row.get("footprint", {}).get("value", "")

                # Apply rules
                geo_result  = apply_geo(row)
                ctrl_result = apply_ctrl(row)
                def_result  = apply_def(row)
                # Pass DEF riders and J-SUM flag into ECON
                row["_def_riders"] = def_result["riders"]
                row["_is_jsum"] = "J-SUM" in geo_result["flags"]
                econ_result = apply_econ(row)
                mob_result  = apply_mob(row)
                elem_result = apply_elem(row)

                # Collect all flags
                all_flags = list(geo_result["flags"]) + def_result["flags"]

                # Stats
                if geo_result["value"]:
                    stats["geo_dist"][geo_result["value"]] += 1
                else:
                    stats["geo_dist"]["FLAGGED"] += 1
                for f in all_flags:
                    stats["flag_counts"][f] += 1
                for g in econ_result["gaps"]:
                    stats["gap_counts"][g] += 1
                for ag in ctrl_result["ailment_gaps"]:
                    stats["ailment_gap_counts"][ag] += 1
                if def_result["bin"]:
                    stats["def_bin_counts"][def_result["bin"]] += 1
                else:
                    stats["def_bin_counts"]["FLAGGED"] += 1
                if "sustain:leech" in def_result["riders"]:
                    stats["sustain_leech_primary"] += 1
                if def_result["block_physics"]:
                    stats["block_physics"][def_result["block_physics"]] += 1

                # Build output record
                out_rec = {
                    "kit_id": kit_id,
                    "game": game,
                    "folk_name": folk,
                    "engine_geometry": {
                        "value": geo_result["value"],
                        "rule_fired": geo_result["rule_fired"],
                        "conf": geo_result["conf"],
                    },
                    "ctrl": {
                        "treatment": ctrl_result["treatment"],
                        "ailments_mapped": ctrl_result["ailments_mapped"],
                        "ailment_gaps": ctrl_result["ailment_gaps"],
                    },
                    "def": {
                        "bin": def_result["bin"],
                        "riders": def_result["riders"],
                        "conf": def_result["def_conf"],
                    },
                    "econ": {
                        "status": econ_result["status"],
                        "gaps": econ_result["gaps"],
                        "meter_type": econ_result["meter_type"],
                    },
                    "mob": mob_result,
                    "flags": all_flags,
                    "provenance": {
                        "delivery": delivery,
                        "footprint": footprint,
                        "elem_raw": elem_result["elem_raw"],
                        "atlas_key": atlas,
                    },
                }

                output_records.append(out_rec)

                # Collect judgment items
                if all_flags:
                    # Extract relevant probe facts for each flag
                    probe_snippet = {
                        "delivery": row.get("delivery", {}),
                        "footprint": row.get("footprint", {}),
                        "geo_text": row.get("geo_text", ""),
                        "movement": row.get("movement", {}),
                        "defense": row.get("defense", {}),
                        "economy": row.get("economy", {}),
                        "control": row.get("control", {}),
                        "mechanics_notes": str(row.get("mechanics_notes", ""))[:300],
                    }
                    for flag in all_flags:
                        judgment_records[flag].append({
                            "kit_id": kit_id,
                            "folk_name": folk,
                            "game": game,
                            "atlas_key": atlas,
                            "flag": flag,
                            "probe_facts": probe_snippet,
                        })

        stats["per_game_pos"][game_pos] = (fname, game_pos)
        stats["per_game_neg"][game_neg] = (fname, game_neg)
        # Store per game properly
        game_key = fname.replace("-facts.jsonl","")
        stats[f"game:{game_key}:pos"] = game_pos
        stats[f"game:{game_key}:neg"] = game_neg

    return output_records, judgment_records, stats


# ─── WRITE OUTPUTS ───────────────────────────────────────────────────────────
def write_jsonl(records, path):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"Wrote {len(records)} records → {path}")


def write_judgment_queue(judgment_records, path, stats):
    flag_order = ["J-MOV", "J-SUM", "J-ORB", "J-GEO", "J-CTRL", "J-DEF"]
    lines = [
        "# Judgment Queue v1 — engine-key pass\n",
        "> **For gandalf review.** One section per J-flag class. Each kit shows the probe facts that triggered the flag.\n",
        "> **Prime law:** do not resolve flags here. These are for human (gandalf) per-kit judgment.\n\n",
    ]
    total_flagged = sum(len(v) for v in judgment_records.values())
    lines.append(f"**Total flagged kits: {total_flagged}** (some kits may appear in multiple flag classes)\n\n")
    lines.append("---\n\n")

    for flag_class in flag_order:
        items = judgment_records.get(flag_class, [])
        if not items:
            continue
        lines.append(f"## {flag_class} ({len(items)} kits)\n\n")
        for item in items:
            pf = item["probe_facts"]
            lines.append(f"### `{item['kit_id']}` — {item['folk_name']} ({item['game']})\n\n")
            lines.append(f"- **atlas_key:** `{item['atlas_key']}`\n")
            lines.append(f"- **delivery:** `{pf['delivery'].get('value')}` (conf={pf['delivery'].get('conf')})\n")
            lines.append(f"- **footprint:** `{pf['footprint'].get('value')}` (conf={pf['footprint'].get('conf')})\n")
            lines.append(f"- **geo_text:** {pf['geo_text']}\n")
            if flag_class == "J-MOV":
                lines.append(f"- **movement:** verbs={pf['movement'].get('verbs')}, "
                              f"skill_is_movement={pf['movement'].get('skill_is_movement')}, "
                              f"policy={pf['movement'].get('policy_while_casting')}\n")
            if flag_class == "J-DEF":
                lines.append(f"- **defense:** primary={pf['defense'].get('primary')}, "
                              f"layers={pf['defense'].get('layers')}\n")
                lines.append(f"- **mechanics_notes:** {pf['mechanics_notes'][:200]}\n")
            if flag_class == "J-SUM":
                lines.append(f"- **economy:** model={pf['economy'].get('model')}, "
                              f"builder_source={pf['economy'].get('builder_source')}\n")
                lines.append(f"- **mechanics_notes:** {pf['mechanics_notes'][:200]}\n")
            if flag_class == "J-ORB":
                lines.append(f"- **delivery:** orbit, footprint={pf['footprint'].get('value')}\n")
                lines.append(f"- **mechanics_notes:** {pf['mechanics_notes'][:200]}\n")
            if flag_class == "J-GEO":
                lines.append(f"- **mechanics_notes:** {pf['mechanics_notes'][:200]}\n")
            lines.append("\n")
        lines.append("---\n\n")

    # Also any non-standard flag classes
    for flag_class, items in sorted(judgment_records.items()):
        if flag_class in flag_order:
            continue
        lines.append(f"## {flag_class} ({len(items)} kits)\n\n")
        for item in items:
            pf = item["probe_facts"]
            lines.append(f"### `{item['kit_id']}` — {item['folk_name']} ({item['game']})\n\n")
            lines.append(f"- **delivery:** `{pf['delivery'].get('value')}`\n")
            lines.append(f"- **footprint:** `{pf['footprint'].get('value')}`\n")
            lines.append(f"- **geo_text:** {pf['geo_text']}\n\n")
        lines.append("---\n\n")

    with open(path, "w") as f:
        f.writelines(lines)
    print(f"Wrote judgment queue → {path}")


def write_boards(output_records, judgment_records, stats, path):
    # Collect gap→kit lists
    gap_kits = collections.defaultdict(list)
    for rec in output_records:
        for g in rec["econ"]["gaps"]:
            gap_kits[g].append(rec["kit_id"])
    # Ailment gap → kit lists
    ailment_gap_kits = collections.defaultdict(list)
    for rec in output_records:
        for ag in rec["ctrl"]["ailment_gaps"]:
            # strip "GAP-AILMENT:" prefix
            cls = ag.replace("GAP-AILMENT:", "")
            ailment_gap_kits[cls].append(rec["kit_id"])
    # Block physics kits
    block_kits = {"binary-negate": [], "flat-absorb": [], "percent-reduce": [], "unresolved": []}
    for rec in output_records:
        if "trigger:block" in rec["def"]["riders"]:
            if rec["def"]["bin"] == "evade":
                block_kits["binary-negate"].append(rec["kit_id"])
            elif rec["def"]["bin"] == "absorb":
                block_kits["flat-absorb"].append(rec["kit_id"])
            elif rec["def"]["bin"] == "mitigate":
                block_kits["percent-reduce"].append(rec["kit_id"])
            else:
                block_kits["unresolved"].append(rec["kit_id"])

    lines = [
        "# Boards v1 — engine-key mapping pass\n\n",
        "> Generated by apply-rules-v1.py from megaprobe-2026-07-12. \n",
        "> Four boards per §6 of rekey-map-rules-v1.md.\n\n",
        "---\n\n",
    ]

    # Board 1: Mechanics-gap leverage
    lines.append("## Board 1 — Mechanics-Gap Leverage\n\n")
    lines.append("*Per gap code: kit count + kit list. Feeds pause-2/V3 maximal-coverage objective.*\n\n")
    gap_code_order = ["SU", "AM", "PC", "RC", "RS", "DR", "HV", "BT",
                      "LC", "UNKNOWN", "CHANNEL-UNLISTED"]
    lines.append("| Gap Code | Count | Kit IDs |\n")
    lines.append("|---|---|---|\n")
    for code in gap_code_order:
        kits = gap_kits.get(code, [])
        if kits:
            kits_str = ", ".join(kits[:15]) + (f" (+{len(kits)-15} more)" if len(kits) > 15 else "")
            lines.append(f"| {code} | {len(kits)} | {kits_str} |\n")
    # Any unlisted gap codes
    for code, kits in sorted(gap_kits.items()):
        if code not in gap_code_order and kits:
            kits_str = ", ".join(kits[:15])
            lines.append(f"| {code} | {len(kits)} | {kits_str} |\n")
    lines.append("\n")

    # Board 2: Geometry distribution
    lines.append("## Board 2 — Geometry Distribution\n\n")
    lines.append("*Engine type → count. Feeds atlas/census refresh.*\n\n")
    lines.append("| Engine Type | Count |\n")
    lines.append("|---|---|\n")
    for gtype, cnt in sorted(stats["geo_dist"].items(), key=lambda x: -x[1]):
        lines.append(f"| `{gtype}` | {cnt} |\n")
    lines.append(f"\n**J-flag counts:** ")
    for flag, cnt in sorted(stats["flag_counts"].items()):
        lines.append(f"{flag}={cnt}  ")
    lines.append("\n\n")

    # Board 3: Ailment-gap census
    lines.append("## Board 3 — Ailment-Gap Census\n\n")
    lines.append("*GAP-AILMENT class → count → ailment-layer design.*\n\n")
    lines.append("| Gap Class | Count | Representative Kits |\n")
    lines.append("|---|---|---|\n")
    for cls, kits in sorted(ailment_gap_kits.items(), key=lambda x: -len(x[1])):
        kits_sample = ", ".join(kits[:8]) + (f" (+{len(kits)-8} more)" if len(kits) > 8 else "")
        lines.append(f"| {cls} | {len(kits)} | {kits_sample} |\n")
    lines.append("\n")

    # Board 4: Def-bin distribution
    lines.append("## Board 4 — Def-Bin Distribution\n\n")
    lines.append("*Bin counts + sustain-leech-primary count (Fork D4 evidence) + block-physics split.*\n\n")
    lines.append("| Def Bin | Count |\n")
    lines.append("|---|---|\n")
    for bin_, cnt in sorted(stats["def_bin_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| `{bin_}` | {cnt} |\n")
    lines.append(f"\n**sustain-leech primary count (Fork D4 evidence):** {stats['sustain_leech_primary']}\n")
    lines.append(f"\n*(Fork D4: sixth-verb candidacy escalates to Matt if >10; current count is "
                 f"{'ABOVE' if stats['sustain_leech_primary'] > 10 else 'AT OR BELOW'} threshold)*\n\n")

    lines.append("### Block-physics split\n\n")
    lines.append("| Physics Bin | Count | Kit IDs |\n")
    lines.append("|---|---|---|\n")
    for btype, kits in block_kits.items():
        kits_str = ", ".join(kits)
        lines.append(f"| {btype} | {len(kits)} | {kits_str} |\n")
    lines.append("\n")

    with open(path, "w") as f:
        f.writelines(lines)
    print(f"Wrote boards → {path}")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== apply-rules-v1.py — corpus → engine-key pass ===\n")

    output_records, judgment_records, stats = process_all()

    # Print run summary
    print(f"\nPositives processed: {stats['total_pos']}")
    print(f"Negatives skipped:   {stats['total_neg']}")
    print("\nPer-game counts:")
    for fname in GAME_FILES:
        gk = fname.replace("-facts.jsonl","")
        pos = stats.get(f"game:{gk}:pos", 0)
        neg = stats.get(f"game:{gk}:neg", 0)
        print(f"  {gk:20s}  pos={pos:3d}  neg={neg:3d}")

    print("\nGeometry distribution (top 10):")
    for gtype, cnt in sorted(stats["geo_dist"].items(), key=lambda x: -x[1])[:12]:
        print(f"  {gtype:30s}: {cnt}")

    print("\nFlag counts:")
    for flag, cnt in sorted(stats["flag_counts"].items()):
        print(f"  {flag}: {cnt}")

    print("\nGap counts (mechanics gaps):")
    for g, cnt in sorted(stats["gap_counts"].items(), key=lambda x: -x[1]):
        print(f"  {g}: {cnt}")

    print("\nAilment-gap counts:")
    for ag, cnt in sorted(stats["ailment_gap_counts"].items(), key=lambda x: -x[1]):
        print(f"  {ag}: {cnt}")

    print("\nDef-bin counts:")
    for b, cnt in sorted(stats["def_bin_counts"].items(), key=lambda x: -x[1]):
        print(f"  {b}: {cnt}")

    print(f"\nSustain-leech primary count (Fork D4): {stats['sustain_leech_primary']}")
    print(f"Block-physics split: {dict(stats['block_physics'])}")

    # Write outputs
    write_jsonl(output_records, OUT_DIR / "corpus-engine-key-v1.jsonl")
    write_judgment_queue(judgment_records, OUT_DIR / "judgment-queue-v1.md", stats)
    write_boards(output_records, judgment_records, stats, OUT_DIR / "boards-v1.md")

    print("\n=== Done ===")
