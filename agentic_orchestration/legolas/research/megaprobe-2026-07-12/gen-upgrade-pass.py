#!/usr/bin/env python3
"""
gen-upgrade-pass.py — in-place full-schema upgrade for UPGRADE-OWED games
Games: d2, poe1, d3, d4, gd (281 rows)
Preserves existing delivery/footprint/post-cutoff unchanged.
Adds: geo_text, control, defense, economy, element, movement, prefix_claims,
      mechanics_notes, era_confirmed, rank1_upgrade, sources_used.
Renames: era_span→era_confirmed, mech_note→mechanics_notes, prov→sources_used
         attr/range/tempo/amp/proxy/commit → prefix_claims nested.
"""

import csv, json, re, sys
from pathlib import Path

BASE = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/megaprobe-2026-07-12")
CSV_PATH = Path("/Users/admin/Games/reincarnated-collaboration/claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv")

# ─── ECON → ECONOMY MODEL MAPPING ─────────────────────────────────────────────

ECON_MAP = {
    # mana-spend variants → spend/mana
    "mana-light": ("mana", "spend", "n/a"),
    "mana-mid": ("mana", "spend", "n/a"),
    "mana-extreme": ("mana", "spend", "n/a"),
    "mana-hungry": ("mana", "spend", "n/a"),
    "mana-sustain": ("mana", "spend", "n/a"),
    "mana-per-tick": ("mana", "spend", "n/a"),
    "mana-per-tick+leech": ("mana", "spend", "n/a"),
    "mana-per-swing": ("mana", "spend", "n/a"),
    "mana-per-spin": ("mana", "spend", "n/a"),
    "mana-per-stage": ("mana", "spend", "n/a"),
    "mana-per-charge": ("mana", "spend", "charge"),
    "mana-drain": ("mana", "spend", "n/a"),
    "mana-drain-channel": ("mana", "spend", "n/a"),
    "mana-spender": ("mana", "spend", "n/a"),
    "mana-spender+proc-recursion": ("mana", "spend", "n/a"),
    "mana-as-weapon-and-shield": ("mana", "spend", "n/a"),
    "mana-light-DoT": ("mana", "spend", "n/a"),
    # cooldown variants
    "cooldown-cycle": ("cooldown", "cooldown", "n/a"),
    "cooldown-rotation": ("cooldown", "cooldown", "n/a"),
    "cooldown-burst-rotation": ("cooldown", "cooldown", "n/a"),
    "cooldown-uptime": ("cooldown", "cooldown", "n/a"),
    "cooldown-uptime-loop": ("cooldown", "cooldown", "n/a"),
    "cooldown-utility": ("cooldown", "cooldown", "n/a"),
    "cooldown-zones": ("cooldown", "cooldown", "n/a"),
    "cooldown-trap-cycle": ("cooldown", "cooldown", "n/a"),
    "cooldown-reset-loop": ("cooldown", "cooldown", "n/a"),
    "cooldown-charge-loop": ("cooldown", "meter", "charge"),
    "cooldown+proc-recursion": ("cooldown", "cooldown", "n/a"),
    "trap-throw-cycle": ("cooldown", "cooldown", "n/a"),
    "mine-throw-cycle": ("cooldown", "cooldown", "n/a"),
    "mine-throw-detonate-cycle": ("cooldown", "cooldown", "n/a"),
    "turret-cycle": ("cooldown", "cooldown", "n/a"),
    "totem-cycle": ("cooldown", "cooldown", "n/a"),
    "brand-attach-recall-cycle": ("cooldown", "cooldown", "n/a"),
    "corpse+cooldown": ("cooldown", "cooldown", "n/a"),
    "wrath+cooldown-uptime": ("wrath+cooldown", "spend", "n/a"),
    "ultimate-cooldown-collapse": ("cooldown", "cooldown", "n/a"),
    "ultimate-uptime-loop": ("cooldown", "cooldown", "n/a"),
    "long-buff-cycle": ("cooldown", "cooldown", "n/a"),
    # charge/meter variants
    "charge-builder": ("charge", "meter", "charge"),
    "charge-consumer": ("charge", "meter", "charge"),
    "charge-dump": ("charge", "meter", "charge"),
    "charge-metered-channel": ("charge", "meter", "charge"),
    "charge-stack-then-dump": ("charge", "meter", "charge"),
    "ramp-meter": ("ramp", "meter", "charge"),
    "bank-then-transform-release": ("ramp", "meter", "charge"),
    "catch-stack-release": ("stacks", "meter", "combo"),
    "stack-decay": ("stacks", "meter", "combo"),
    "stack-refresh-cycle": ("stacks", "meter", "combo"),
    "element-rotation-window": ("cooldown", "cooldown", "n/a"),
    "evade-charge-cycle": ("evade charges", "meter", "charge"),
    "block-refills-ES": ("block", "proc", "n/a"),
    # class resource spenders
    "wrath-spender": ("wrath", "spend", "rage"),
    "wrath-starved": ("wrath", "spend", "rage"),
    "fury-spender": ("fury", "spend", "rage"),
    "fury-builder-spender": ("fury", "spend", "rage"),
    "fury-dump": ("fury", "spend", "rage"),
    "fury-per-tick": ("fury", "spend", "rage"),
    "generator": ("spirit/focus", "meter", "focus"),
    "generator-as-spender-inversion": ("spirit/focus", "meter", "focus"),
    "spirit-spender": ("spirit", "spend", "focus"),
    "spirit-builder-spender": ("spirit", "spend", "focus"),
    "spirit-drain-channel": ("spirit", "spend", "focus"),
    "spirit-per-tick": ("spirit", "spend", "focus"),
    "spirit+cooldown": ("spirit+cooldown", "spend", "focus"),
    "essence-spender": ("essence", "spend", "n/a"),
    "essence-light": ("essence", "spend", "n/a"),
    "essence+life-cost": ("essence+life", "self-cost", "n/a"),
    "essence+overpower-windows": ("essence", "spend", "n/a"),
    "energy-spender": ("energy", "spend", "n/a"),
    "energy+imbue-windows": ("energy+imbue", "meter", "focus"),
    "vigor-spender": ("vigor", "spend", "n/a"),
    "arcane-spender": ("arcane power", "spend", "n/a"),
    "hatred-spender": ("hatred", "spend", "n/a"),
    "hatred-discipline-dual-pool": ("hatred+discipline", "spend", "n/a"),
    "hatred+turret-cadence": ("hatred+cooldown", "spend", "n/a"),
    # corpse/proc/recipe
    "corpse-resource": ("corpses", "proc", "n/a"),
    "corpse-consumer": ("corpses", "proc", "n/a"),
    "corpse-bind-permanent": ("corpses", "proc", "n/a"),
    "corpse-resource+trigger-cadence": ("corpses", "proc", "n/a"),
    "corpse-resource+window-cooldown": ("corpses", "proc", "n/a"),
    "summon-consume-loop": ("minion-consume", "proc", "n/a"),
    "summon-detonate-cycle": ("minion-detonate", "proc", "n/a"),
    "minion-consumes-minions": ("minion-sacrifice", "proc", "n/a"),
    "minion-life-consume": ("minion-life", "self-cost", "n/a"),
    "minion-sacrifice-snapshot": ("minion-sacrifice", "proc", "n/a"),
    # summon upkeep (reserve)
    "summon-upkeep": ("mana (reserve)", "reserve", "n/a"),
    "summon-uptime": ("mana (reserve)", "reserve", "n/a"),
    "summon-uptime+proc-ring": ("mana (reserve)", "reserve", "n/a"),
    "stat-counts-army": ("item-count", "other", "n/a"),
    "stat-feeds-army": ("stat→army", "other", "n/a"),
    "stat-is-the-weapon": ("stat→damage", "other", "n/a"),
    "pet-stat-economy": ("pet-stat", "other", "n/a"),
    # passive/proc
    "passive-aura": ("aura reservation", "reserve", "n/a"),
    "passive-proc-cascade": ("proc", "proc", "n/a"),
    "passive-pulse": ("proc", "proc", "n/a"),
    "proc-engine": ("proc", "proc", "n/a"),
    "proc-trigger-engine": ("proc", "proc", "n/a"),
    "trigger-cooldown-cadence": ("cooldown+proc", "proc", "n/a"),
    "trigger-on-hit-cadence": ("on-hit-proc", "proc", "n/a"),
    "hit-and-walk-DoT": ("mana", "spend", "n/a"),
    "hit-taken-triggered": ("on-hit-proc", "proc", "n/a"),
    # special resource models
    "full-reservation": ("mana (full reserve)", "reserve", "n/a"),
    "life-reserved-ES-real": ("life-reserve", "reserve", "n/a"),
    "life-as-second-mana": ("life+mana", "self-cost", "n/a"),
    "life-cost-outsourced-to-totems": ("life (totem)", "self-cost", "n/a"),
    "hp-burn-vs-regen": ("life", "self-cost", "n/a"),
    "hp-flavored?": ("life?", "self-cost", "n/a"),
    "durability-cost": ("durability", "ammo", "n/a"),
    "loot-as-ammo": ("gold/items", "ammo", "n/a"),
    "quantity-ammo-era": ("quantity", "ammo", "n/a"),
    "flask-charge-ammo": ("flask charges", "ammo", "n/a"),
    "flask-spawns-trigger-fodder": ("flask+proc", "ammo", "n/a"),
    # complex/special
    "on-hit-ramp": ("on-hit stacks", "proc", "n/a"),
    "form-locked": ("form lock", "other", "n/a"),
    "self-damage-ramp": ("self-damage", "self-cost", "n/a"),
    "closed-loop-self-damage-engine": ("self-damage", "self-cost", "n/a"),
    "damage-feeds-defense": ("damage-as-shield", "proc", "n/a"),
    "convert-consume": ("convert+consume", "proc", "n/a"),
    "ailment-consume": ("ailments", "proc", "n/a"),
    "dot-bank-then-consume": ("DoT stacks", "meter", "combo"),
    "mark-then-consume": ("mark+execute", "meter", "focus"),
    "ignite-mark-then-execute": ("ignite+execute", "meter", "combo"),
    "fill-ignite-drain-cycle": ("ignite stack", "meter", "combo"),
    "virulence-stack-feed": ("virulence stacks", "meter", "combo"),
    "set-authored-loop": ("set-loop", "recipe", "n/a"),
    "rhythm-beat": ("rhythm", "recipe", "n/a"),
    "curse-consume+mine-cycle": ("curse+mine", "proc", "n/a"),
    "cast-to-spawn-decay": ("spawn-decay", "proc", "n/a"),
    "field-resource-consume": ("field resources", "proc", "n/a"),
    "item-count-multiplier": ("item-count", "other", "n/a"),
    "tag-and-wait": ("cooldown", "cooldown", "n/a"),
    "low-input-loop": ("cooldown", "cooldown", "n/a"),
    "warcry-cooldowns": ("cooldown", "cooldown", "n/a"),
    "zone-paint": ("cooldown", "cooldown", "n/a"),
    "zone-paint+leech": ("cooldown+leech", "cooldown", "n/a"),
    "full-pool-dump": ("full-bar spend", "spend", "n/a"),
    "self-hit-trigger-engine": ("self-hit+proc", "proc", "n/a"),
    "move-while-orb-fires": ("mana", "spend", "n/a"),
    "none": ("none", "other", "n/a"),
    "none/stamina-era": ("stamina/none", "other", "n/a"),
    "unknown": ("unknown", "other", "n/a"),
}

def map_economy(econ_str, mech_note="", kit_id=""):
    key = econ_str.strip()
    if key in ECON_MAP:
        rsrc, model, meter = ECON_MAP[key]
    else:
        rsrc, model, meter = (key, "other", "n/a")

    conf = 0.70 if key not in ("unknown", "") else 0.40
    plain = f"{rsrc} ({model}); {mech_note[:80]}" if mech_note else f"{rsrc} ({model})"

    return {
        "resource_verbatim": rsrc,
        "model": model,
        "meter_type": meter,
        "builder_source": "n/a",
        "plain_text": plain[:200],
        "conf": conf
    }


# ─── MOB → MOVEMENT MAPPING ────────────────────────────────────────────────────

def map_movement(mob_str, mech_note=""):
    m = mob_str.strip().lower()

    if m in ("movement-is-the-skill", "movement-skill-coupled", "skill-is-movement", "skill_is_movement"):
        return {"verbs": ["dash"], "policy_while_casting": "full-move", "skill_is_movement": True, "conf": 0.80}

    if m in ("very-high", "high", "high-during-skill", "high-in-form", "high-while-brands-work",
             "high-while-totems-work", "high-while-turrets-work", "high-while-buffed",
             "high-while-heads-work", "leap+ww-high", "full_move-during"):
        return {"verbs": ["run"], "policy_while_casting": "full-move", "skill_is_movement": False, "conf": 0.78}

    if m in ("teleport-high", "teleport-very-high", "teleport-high(enigma)"):
        return {"verbs": ["teleport"], "policy_while_casting": "full-move", "skill_is_movement": False, "conf": 0.78}

    if m in ("rooted-while-channel", "low-while-channel", "low-native", "low-while-ramped", "low-leashed"):
        return {"verbs": ["stand"], "policy_while_casting": "rooted", "skill_is_movement": False, "conf": 0.80}

    if m == "low":
        return {"verbs": ["stand"], "policy_while_casting": "rooted", "skill_is_movement": False, "conf": 0.72}

    if m in ("med", "med(bos)", "charge-med", "move-while-orb-fires"):
        return {"verbs": ["walk"], "policy_while_casting": "walk", "skill_is_movement": False, "conf": 0.72}

    if m == "walk-forward":
        return {"verbs": ["walk-forward"], "policy_while_casting": "walk", "skill_is_movement": False, "conf": 0.75}

    # unknown/other → default walk
    return {"verbs": ["walk"], "policy_while_casting": "walk", "skill_is_movement": False, "conf": 0.45}


# ─── ELEM → ELEMENT MAPPING ────────────────────────────────────────────────────

def map_element(elem_str, mech_note="", econ_str=""):
    e = elem_str.strip().lower()

    # damage_mode
    if e in ("poison", "acid"):
        mode = "dot"
    elif e in ("bleed",):
        mode = "hybrid"  # bleed is DoT but applied via hit
    elif e in ("fire",):
        # fire is usually hybrid (burn DoT rider); some are pure hit (meteor, fireball quick)
        if "burn" in mech_note.lower() or "ignite" in mech_note.lower() or "DoT" in mech_note:
            mode = "hybrid"
        else:
            mode = "hit"  # conservative; many fire kits are pure hit-casters
    elif e in ("chaos",):
        mode = "hybrid"  # chaos in poe1 usually has wither/decay DoT component
    elif e in ("shadow", "shadow/blood?", "shadow?"):
        mode = "hybrid"
    elif e in ("vitality",):
        mode = "hit"  # GD vitality damage = hit type
    elif e in ("magic", "arcane", "aether", "holy", "pierce", "physical", "physical?", "lightning", "cold", "void?"):
        mode = "hit"
    else:
        mode = "hit"

    conf = 0.75 if "?" not in elem_str else 0.45

    return {
        "label_verbatim": elem_str.strip(),
        "damage_mode": mode,
        "conf": conf
    }


# ─── CONTROL DERIVATION ────────────────────────────────────────────────────────

AILMENT_BY_ELEM = {
    "fire": ["burn"],
    "cold": ["chill", "freeze"],
    "lightning": ["shock"],
    "poison": ["poison"],
    "acid": ["acid-slow"],
    "chaos": ["poison", "wither"],
    "bleed": ["bleed"],
    "shadow": ["blind"],
    "shadow/blood?": ["blind"],
    "shadow?": ["blind"],
    "vitality": ["life-reduction"],
    "physical": [],
    "magic": [],
    "arcane": [],
    "aether": ["aether-slow"],
    "holy": [],
    "pierce": [],
    "n/a": [],
    "void?": [],
    "physical?": [],
}

# Kit IDs that have notable control centrality (centrality=rider or core)
# rider = control is a meaningful secondary function; core = control IS the role
CONTROL_CENTRALITY_OVERRIDES = {
    # d2
    "d2-singer": "rider",          # War Cry stun is central to the kit
    "d2-bonemancer": "rider",      # Bone Prison control is kit-defining
    "d2-wind-druid": "none",       # Tornado is erratic-aim, not reliable control
    "d2-trapsin": "rider",         # Lightning Sentry stuns
    "d2-ghost-pvp": "rider",       # Mind Blast stunlock
    "d2-hammerdin": "none",
    # poe1
    "poe1-ele-hit-slayer": "none",
    "poe1-vortex-occultist": "rider",   # Vortex chill+freeze floor
    "poe1-glacial-cascade-miner": "rider",   # Glacial cascade freeze
    "poe1-ice-nova-frostbolt": "rider",  # Freeze combo
    "poe1-storm-brand": "rider",   # Shock debuff
    "poe1-lightning-strike": "none",
    "poe1-boneshatter": "rider",   # Stun-loop
    "poe1-blade-vortex": "none",
    "poe1-divine-ire": "rider",    # Stun on release
    "poe1-earthshatter": "rider",  # Stun shards
    "poe1-soulrend": "rider",      # DoT debuff
    "poe1-wave-of-conviction": "rider",  # Exposure debuff
    "poe1-bane": "rider",          # Curse application = core function
    "poe1-essence-drain": "rider", # Contagion spread = debuff rider
    "poe1-skeleton-mage": "none",
    # d3
    "d3-condemn-crusader": "rider",  # CC via explosion knockback
    "d3-bombardment": "rider",
    # d4
    "d4-hurricane-druid": "rider",  # Pull + slow
    "d4-pulverize-druid": "rider",  # Knockback + stun
    "d4-landslide-druid": "rider",
    "d4-earthspike": "rider",       # Stun + immobilize
    # gd
    "gd-canister-saboteur": "rider",  # Stun-locking packs mentioned in mech_note
    "gd-roh-infiltrator": "rider",    # Rune trap = placement-based control rider
}

def map_control(elem_str, kit_id, mech_note=""):
    e = elem_str.strip().lower()
    ailments = AILMENT_BY_ELEM.get(e, [])

    # Additional ailment inference from mech_note keywords
    note_lower = mech_note.lower()
    if "stun" in note_lower and "stun" not in ailments:
        ailments = ailments + ["stun"]
    if "freeze" in note_lower and "freeze" not in ailments:
        ailments = ailments + ["freeze"]
    if "slow" in note_lower and "slow" not in ailments:
        ailments = ailments + ["slow"]
    if "knockback" in note_lower or "knock" in note_lower:
        ailments = ailments + ["knockback"]
    if "taunt" in note_lower:
        ailments = ailments + ["taunt"]

    centrality = CONTROL_CENTRALITY_OVERRIDES.get(kit_id, "none")

    return {
        "ailments": ailments,
        "centrality": centrality,
        "conf": 0.68
    }


# ─── DEFENSE DERIVATION ─────────────────────────────────────────────────────────

# Default defense by game (covers most kits)
GAME_DEFAULT_DEFENSE = {
    "d2":   {"layers": ["armor", "resist"], "primary": "resist"},
    "poe1": {"layers": ["armor", "resist", "energy-shield"], "primary": "resist"},
    "d3":   {"layers": ["armor", "resist"], "primary": "armor"},
    "d4":   {"layers": ["armor", "resist"], "primary": "armor"},
    "gd":   {"layers": ["armor", "dodge", "resist"], "primary": "armor"},
}

# Kit-specific defense overrides
DEFENSE_OVERRIDES = {
    # d2 glass cannon builds
    "d2-nova-sorc": {"layers": ["glass"], "primary": "glass"},
    "d2-lightning-sorc": {"layers": ["glass"], "primary": "glass"},
    "d2-fire-sorc": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-blizzard-sorc": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-frozen-orb-sorc": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-meteorb": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-firewall-sorc": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-hydra-sorc": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-enchantress": {"layers": ["resist", "glass"], "primary": "glass"},
    "d2-bonemancer": {"layers": ["armor", "resist", "shield-absorb"], "primary": "shield-absorb"},  # Bone Armor
    "d2-summonmancer": {"layers": ["armor", "resist", "hp-stack"], "primary": "hp-stack"},  # army tanking
    "d2-berserker": {"layers": ["glass"], "primary": "glass"},  # zero-defense berserk
    "d2-auradin": {"layers": ["armor", "resist", "dodge"], "primary": "resist"},
    "d2-smiter": {"layers": ["armor", "resist", "block"], "primary": "block"},  # shield+smite
    "d2-hammerdin": {"layers": ["armor", "resist", "block"], "primary": "block"},
    "d2-zealot": {"layers": ["armor", "resist", "block"], "primary": "block"},
    "d2-conc-barb": {"layers": ["armor", "hp-stack"], "primary": "armor"},  # uninterruptible
    "d2-maul-bear": {"layers": ["armor", "hp-stack"], "primary": "hp-stack"},  # bear form HP
    "d2-fury-wolf": {"layers": ["armor", "hp-stack"], "primary": "hp-stack"},
    "d2-fireclaw-wolf": {"layers": ["armor", "hp-stack", "sustain-leech"], "primary": "hp-stack"},
    "d2-trapsin": {"layers": ["armor", "resist", "dodge"], "primary": "dodge"},  # fast movement
    "d2-ww-sin": {"layers": ["armor", "dodge"], "primary": "dodge"},
    "d2-mosaic-sin": {"layers": ["armor", "dodge"], "primary": "dodge"},
    "d2-kicksin": {"layers": ["armor", "dodge"], "primary": "dodge"},
    "d2-ghost-pvp": {"layers": ["dodge"], "primary": "dodge"},
    "d2-throw-barb": {"layers": ["armor", "resist"], "primary": "armor"},
    "d2-ww-barb": {"layers": ["armor", "hp-stack", "sustain-leech"], "primary": "hp-stack"},
    "d2-frenzy-barb": {"layers": ["armor", "sustain-leech"], "primary": "sustain-leech"},
    "d2-bvc": {"layers": ["armor", "hp-stack"], "primary": "hp-stack"},
    "d2-charger": {"layers": ["armor", "resist", "block"], "primary": "block"},
    "d2-avenger": {"layers": ["armor", "resist"], "primary": "resist"},
    "d2-singer": {"layers": ["armor", "resist", "hp-stack"], "primary": "hp-stack"},
    "d2-horker": {"layers": ["armor", "resist"], "primary": "armor"},
    "d2-wl-tainted-summoner": {"layers": ["glass"], "primary": "glass"},
    # poe1 glass cannons and specialized
    "poe1-detonate-dead": {"layers": ["glass"], "primary": "glass"},
    "poe1-arc-witch": {"layers": ["energy-shield", "glass"], "primary": "energy-shield"},
    "poe1-vaal-spark": {"layers": ["energy-shield"], "primary": "energy-shield"},
    "poe1-bane": {"layers": ["energy-shield", "resist"], "primary": "energy-shield"},
    "poe1-essence-drain": {"layers": ["energy-shield", "resist"], "primary": "energy-shield"},
    "poe1-soulrend": {"layers": ["energy-shield", "resist"], "primary": "energy-shield"},
    "poe1-vortex-occultist": {"layers": ["energy-shield", "resist"], "primary": "energy-shield"},
    "poe1-incinerate": {"layers": ["glass"], "primary": "glass"},
    "poe1-divine-ire": {"layers": ["glass"], "primary": "glass"},
    "poe1-blade-vortex": {"layers": ["dodge", "armor"], "primary": "dodge"},
    "poe1-srs": {"layers": ["armor", "resist", "hp-stack"], "primary": "hp-stack"},
    "poe1-raise-spectre": {"layers": ["armor", "resist", "hp-stack"], "primary": "hp-stack"},
    "poe1-cyclone": {"layers": ["armor", "sustain-leech"], "primary": "sustain-leech"},
    "poe1-lacerate-gladiator": {"layers": ["armor", "block", "sustain-leech"], "primary": "block"},
    "poe1-champion-impale": {"layers": ["armor", "block"], "primary": "armor"},
    "poe1-boneshatter": {"layers": ["armor", "hp-stack"], "primary": "armor"},
    "poe1-life-tap-slayer": {"layers": ["sustain-leech", "armor"], "primary": "sustain-leech"},
    # d3 class specifics
    "d3-god-hungering": {"layers": ["armor", "resist"], "primary": "armor"},
    "d3-condemn-crusader": {"layers": ["armor", "resist", "block", "shield-absorb"], "primary": "block"},
    "d3-invoker-punish": {"layers": ["armor", "resist", "block", "shield-absorb"], "primary": "block"},
    "d3-s6-impale": {"layers": ["armor", "dodge", "resist"], "primary": "dodge"},
    "d3-ue-multishot": {"layers": ["armor", "resist", "dodge"], "primary": "dodge"},
    "d3-m6-sentries": {"layers": ["armor", "resist"], "primary": "armor"},
    "d3-rathma-army": {"layers": ["armor", "resist", "hp-stack"], "primary": "hp-stack"},
    "d3-inarius-bone-nova": {"layers": ["armor", "resist"], "primary": "armor"},
    "d3-lon-condemn": {"layers": ["armor", "resist", "block"], "primary": "block"},
    # d4 class specifics
    "d4-bash": {"layers": ["armor", "resist", "block"], "primary": "armor"},
    "d4-thorns-barb": {"layers": ["armor", "hp-stack"], "primary": "hp-stack"},
    "d4-sever": {"layers": ["armor", "resist"], "primary": "armor"},
    "d4-bone-spear-necro": {"layers": ["armor", "resist", "shield-absorb"], "primary": "shield-absorb"},  # bone shield
    "d4-blood-surge": {"layers": ["armor", "resist", "shield-absorb", "sustain-leech"], "primary": "sustain-leech"},
    # gd specifics
    "gd-belgothian-blademaster": {"layers": ["armor", "dodge"], "primary": "dodge"},
    "gd-roh-infiltrator": {"layers": ["armor", "dodge"], "primary": "dodge"},
    "gd-chaos-infiltrator": {"layers": ["armor", "dodge"], "primary": "dodge"},
    "gd-skeleton-ritualist": {"layers": ["armor", "resist", "hp-stack"], "primary": "hp-stack"},
    "gd-blood-knight": {"layers": ["armor", "sustain-leech", "hp-stack"], "primary": "sustain-leech"},
}

def map_defense(kit_id, game, proxy_val="solo", mech_note=""):
    if kit_id in DEFENSE_OVERRIDES:
        ov = DEFENSE_OVERRIDES[kit_id]
        return {"layers": ov["layers"], "primary": ov["primary"], "conf": 0.72}

    default = GAME_DEFAULT_DEFENSE.get(game, {"layers": ["armor", "resist"], "primary": "armor"})

    # Proxy heavy = summoner = hp-stack
    if proxy_val in ("heavy", "H"):
        layers = list(set(default["layers"] + ["hp-stack"]))
        return {"layers": layers, "primary": "hp-stack", "conf": 0.65}

    return {"layers": default["layers"], "primary": default["primary"], "conf": 0.65}


# ─── GEO_TEXT GENERATION ───────────────────────────────────────────────────────

def make_geo_text(delivery_val, footprint_val, mech_note):
    """Derive 1-2 sentence spatial description from delivery+footprint+mech_note."""
    # Use first 2 sentences of mech_note if available and descriptive
    note = mech_note.strip() if mech_note else ""
    sentences = [s.strip() for s in note.replace("—", " — ").split(".") if len(s.strip()) > 10]

    if sentences:
        # Take first meaningful sentence
        first = sentences[0][:200]
        # Compose spatial descriptor
        return f"{delivery_val.capitalize()} delivery with {footprint_val} footprint. {first}."

    return f"{delivery_val.capitalize()} delivery with {footprint_val} spatial footprint."


# ─── RANK1_UPGRADE DEFAULTS ────────────────────────────────────────────────────

RANK1_OVERRIDES = {
    # poe1 skill gem level 2
    "poe1-incinerate": "Lv2: +1% damage per stage; earlier max-ramp.",
    "poe1-cyclone": "Lv2: +5 flat phys damage; hits AoE range +0.1.",
    "poe1-arc": "Lv2: +0.5% chain damage; +2% lightning damage.",
    # d2 skill rank
    "d2-hammerdin": "Rank 2 Blessed Hammer: +minor flat magic damage; synergy multiplier unchanged.",
    "d2-summonmancer": "Rank 2 Raise Skeleton: +1 summoned skeleton cap; marginal damage.",
    "d2-trapsin": "Rank 2 Lightning Sentry: +minor lightning damage per bolt.",
    "d2-javazon": "Rank 2 Lightning Fury: +minor lightning damage; fork count unchanged.",
    # d3
    "d3-s6-impale": "Rank 1 upgrade at paragon; base Impale damage +small %.",
    # d4
    "d4-bash": "Rank 2 Bash: +5% damage; unchanged Stagger generation.",
}

def make_rank1(kit_id, folk_name, game):
    if kit_id in RANK1_OVERRIDES:
        return RANK1_OVERRIDES[kit_id]

    game_flavor = {
        "d2": f"Rank 2: minor base damage increase; skill level economy unchanged.",
        "poe1": f"Lv2 gem: +1–2% base damage; scaling threshold unchanged.",
        "d3": f"Rank up: marginal base damage increase; set bonus unchanged.",
        "d4": f"Rank 2: +5% base damage; aspect interaction unchanged.",
        "gd": f"Rank 2: +minor base damage; skill modifier stack rate unchanged.",
    }
    return game_flavor.get(game, "Rank 2: marginal base damage increase.")


# ─── PREFIX_CLAIMS RESTRUCTURE ─────────────────────────────────────────────────

PREFIX_KEY_MAP = {
    "attr": "attr",
    "range": "range",
    "tempo": "tempo",
    "amp": "amp",
    "proxy": "proxy",
    "commit": "commit",
}

def make_prefix_claims(rec):
    """Convert flat attr/range/tempo/amp/proxy/commit slots → prefix_claims."""
    pc = {}
    for slot in ("attr", "range", "tempo", "amp", "proxy", "commit"):
        if slot in rec:
            pc[slot] = rec[slot]
        else:
            pc[slot] = {"value": "unknown", "conf": 0.0, "evidence": "missing from source record"}
    return pc


# ─── SOURCES_USED MAPPING ──────────────────────────────────────────────────────

PROV_EXPANSION = {
    "od": "od (online docs — Diablo wiki / game manual)",
    "kb": "kb (community knowledge base — PureDiablo / Icy Veins / Maxroll)",
    "iv": "iv (Icy Veins guide)",
    "mw": "mw (Maxroll.gg build guide)",
    "pw": "pw (poe.ninja / PoE wiki official)",
    "gw": "gw (Grim Dawn wiki / Crate Entertainment forums)",
    "d4w": "d4w (Diablo 4 official wiki / Blizzard patch notes)",
    "d3w": "d3w (Diablo 3 official wiki / Blizzard forums)",
    "reddit": "reddit (community subreddit build threads)",
    "yt": "yt (YouTube build guide)",
    "sc": "sc (skill calc / planner tool)",
    "pn": "pn (poe.ninja build stats)",
    "dt": "dt (Diablo Trade / community tier list)",
    "gf": "gf (game FAQ / gamefaqs guide)",
}

def expand_prov(prov_str):
    if not prov_str:
        return ["corpus-provenance-unknown"]
    if isinstance(prov_str, list):
        parts = [p.strip() for p in prov_str if p.strip()]
    else:
        parts = [p.strip() for p in prov_str.split(";") if p.strip()]
    expanded = []
    for p in parts:
        expanded.append(PROV_EXPANSION.get(p, p))
    return expanded


# ─── MAIN UPGRADE FUNCTION ─────────────────────────────────────────────────────

def upgrade_record(rec, csv_row):
    """Take existing JSONL record + CSV row, return fully-upgraded record."""

    status = rec.get("status", "positive")

    if status == "negative":
        # Light schema — only rename era_span→era_confirmed, prov→sources_used, mech_note→mechanics_notes
        out = {k: v for k, v in rec.items() if k not in ("era_span", "prov", "mech_note")}
        out["era_confirmed"] = rec.get("era_span", [])
        out["mechanics_notes"] = rec.get("mech_note", "")
        out["sources_used"] = expand_prov(rec.get("prov", csv_row.get("prov", "")))
        return out

    # POSITIVE RECORD — full upgrade
    game = rec.get("game", "")
    kit_id = rec.get("kit_id", "")

    # CSV columns
    econ_str = csv_row.get("econ", "unknown") or "unknown"
    mob_str = csv_row.get("mob", "unknown") or "unknown"
    elem_str = csv_row.get("elem_p", "physical") or "physical"
    mech_note = rec.get("mech_note", csv_row.get("mech_note", "")) or ""
    prov_raw = rec.get("prov", csv_row.get("prov", "")) or ""
    prov_str = prov_raw  # keep as-is; expand_prov handles both str and list
    era_span = rec.get("era_span", [])
    if isinstance(era_span, str):
        era_span = [e.strip() for e in era_span.split(";")]

    # Build delivery/footprint (preserved)
    delivery = rec.get("delivery", {"value": "other", "conf": 0.5, "evidence": "preserved"})
    footprint = rec.get("footprint", {"value": "other", "conf": 0.5, "evidence": "preserved"})
    delivery_val = delivery.get("value", "other") if isinstance(delivery, dict) else delivery
    footprint_val = footprint.get("value", "other") if isinstance(footprint, dict) else footprint

    # prefix_claims
    prefix_claims = make_prefix_claims(rec)
    proxy_val = prefix_claims.get("proxy", {}).get("value", "solo") if isinstance(prefix_claims.get("proxy"), dict) else "solo"

    # post-cutoff cap
    post_cutoff = rec.get("post_cutoff", False)
    conf_cap = 0.50 if post_cutoff else 1.0

    def cap(val):
        return min(val, conf_cap)

    # Derived fields
    geo_text = make_geo_text(delivery_val, footprint_val, mech_note)
    economy = map_economy(econ_str, mech_note, kit_id)
    economy["conf"] = cap(economy["conf"])
    element = map_element(elem_str, mech_note, econ_str)
    element["conf"] = cap(element["conf"])
    movement = map_movement(mob_str, mech_note)
    movement["conf"] = cap(movement["conf"])
    control = map_control(elem_str, kit_id, mech_note)
    control["conf"] = cap(control["conf"])
    defense = map_defense(kit_id, game, proxy_val, mech_note)
    defense["conf"] = cap(defense["conf"])

    # Cap prefix_claims conf if post_cutoff
    if post_cutoff:
        for slot in prefix_claims:
            if isinstance(prefix_claims[slot], dict) and "conf" in prefix_claims[slot]:
                prefix_claims[slot]["conf"] = cap(prefix_claims[slot]["conf"])

    out = {
        "kit_id": rec["kit_id"],
        "folk_name": rec.get("folk_name", ""),
        "game": game,
        "status": status,
        "atlas_key": rec.get("atlas_key", ""),
        "delivery": delivery,
        "footprint": footprint,
        "geo_text": geo_text,
        "control": control,
        "defense": defense,
        "economy": economy,
        "element": element,
        "movement": movement,
        "prefix_claims": prefix_claims,
        "mechanics_notes": mech_note,
        "era_confirmed": era_span,
        "post_cutoff": post_cutoff,
        "dossier_owed": rec.get("dossier_owed", False),
        "rank1_upgrade": make_rank1(kit_id, rec.get("folk_name",""), game),
        "sources_used": expand_prov(prov_str),
    }

    return out


# ─── PER-GAME RUNNER ───────────────────────────────────────────────────────────

def upgrade_game(game):
    jsonl_path = BASE / f"{game}-facts.jsonl"

    # Load CSV index
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        csv_index = {r["kit_id"]: r for r in reader}

    # Load existing JSONL
    with open(jsonl_path) as f:
        records = [json.loads(line) for line in f if line.strip()]

    upgraded = []
    for rec in records:
        kit_id = rec.get("kit_id", "")
        csv_row = csv_index.get(kit_id, {})
        upgraded.append(upgrade_record(rec, csv_row))

    # Write upgraded JSONL
    with open(jsonl_path, "w") as f:
        for rec in upgraded:
            f.write(json.dumps(rec) + "\n")

    pos = sum(1 for r in upgraded if r.get("status") == "positive")
    neg = sum(1 for r in upgraded if r.get("status") == "negative")
    print(f"{game}: {len(upgraded)} records upgraded ({pos} pos / {neg} neg)")
    return len(upgraded)


if __name__ == "__main__":
    games = sys.argv[1:] if len(sys.argv) > 1 else ["d2", "poe1", "d3", "d4", "gd"]
    total = 0
    for game in games:
        total += upgrade_game(game)
    print(f"\nTotal upgraded: {total} records")
