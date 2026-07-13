"""
gen-hot-facts.py
Mega-probe Unit A — Halls of Torment (hot) — 19 records
18 positive / 1 negative / 2 post-cutoff (hot-1.1-2026 ONLY)
Full schema (6 fact families per positive kit; light schema for negative).

hot = Halls of Torment
- Horde-survivor auto-attack game (VS-like) with ARPG gear drops mid-run
- Classes: Sorceress, Archer, Sage, Exterminator, Warlock, Norseman, Cleric, Swordsman,
  Spirit Warrior, Astronomer, Shieldmaiden, Landsknecht
- Gear must be carried to a Well for persistent extraction (ARPG bridge)
- Artifact modifiers self-author difficulty
- Auto-attack movement: player-verb (like VS — weapons auto-fire while player walks)

Post-cutoff:
- hot-ea-2023: within training window (EA June 2023)
- hot-1.0-2024: within training window (1.0 release 2024)
- hot-1.1-2026: POST-CUTOFF (2026 update); kits with ONLY this era capped ≤0.50
"""
import json
from pathlib import Path

OUT = Path("agentic_orchestration/legolas/research/megaprobe-2026-07-12/hot-facts.jsonl")

def pc(val, conf, ev): return {"value": val, "conf": conf, "evidence": ev}
def dc(val, conf, ev): return {"value": val, "conf": conf, "evidence": ev}
def ctrl(ailments, centrality, conf): return {"ailments": ailments, "centrality": centrality, "conf": conf}
def defs(layers, primary, conf): return {"layers": layers, "primary": primary, "conf": conf}
def econ(res, model, meter, builder, text, conf):
    return {"resource_verbatim": res, "model": model, "meter_type": meter,
            "builder_source": builder, "plain_text": text, "conf": conf}
def elem(label, mode, conf): return {"label_verbatim": label, "damage_mode": mode, "conf": conf}
def mov(verbs, policy, is_move, conf):
    return {"verbs": verbs, "policy_while_casting": policy, "skill_is_movement": is_move, "conf": conf}
def pfx(attr, rng, tempo, amp, proxy, commit):
    return {"attr": attr, "range": rng, "tempo": tempo, "amp": amp, "proxy": proxy, "commitment": commit}

# HoT movement: player-verb (auto-attack fires while player walks; same as VS)
HOT_MOV = mov(["auto-fire-while-moving"], "full-move", False, 0.92)

KITS = []

# ── 1. hot-sorceress-splinters ────────────────────────────────────────────────
# Arcane Splinters Sorceress: homing splinter volleys for range + screen coverage
# Atlas: _RHFSI = _, ranged, high, flat, solo, instant
# 1.0-2024 + 1.1-2026; prov: sf-hot;kb
KITS.append({
    "kit_id": "hot-sorceress-splinters",
    "folk_name": "Arcane Splinters Sorceress",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_RHFSI-PMDD-SP-__-~~",
    "delivery": dc("projectile", 0.82, "homing arcane splinter volleys fire at enemies automatically; each splinter tracks independently"),
    "footprint": dc("multi-point", 0.80, "fan of homing splinters hits multiple simultaneous targets; multi-point coverage"),
    "geo_text": "Arcane Splinters: homing projectile volleys stacked for range and screen coverage. Each splinter independently homes to a target. Forum-paired with Ring Blades as the kill-on-spawn toolkit. High projectile count = wide multi-point simultaneous coverage.",
    "control": ctrl([], "none", 0.78),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("projectile-count-scaling (SP)", "spend", "n/a", "n/a",
                    "SP = spend. Projectile count is the primary scaling axis — more splinters via upgrades and items. No per-projectile resource cost; the class ability fires automatically.", 0.80),
    "element": elem("arcane", "hit", 0.78),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank — no STR/DEX/INT mapping; class-based"),
        pc("R", 0.82, "ranged homing splinters; no melee contact"),
        pc("H", 0.82, "high tempo auto-fire splinter volleys"),
        pc("F", 0.80, "flat per-splinter damage; consistent multi-point output"),
        pc("S", 0.80, "solo; no proxy element"),
        pc("I", 0.82, "instant auto-fire per volley"),
    ),
    "mechanics_notes": "Projectile-count platform: 'stacked for range and screen coverage' — the scaling axis is splinter count, not per-hit amplitude. Forum-paired with Ring Blades (hot-sage-ring-blades) as the kill-on-spawn combo. 1.1-2026 changes unknown (s11 era).",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Splinter count and range increase per upgrade tier; Pierce trait adds lane-through behavior to homing splinters.",
    "sources_used": ["sf-hot (Steam forums HoT)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 2. hot-archer ─────────────────────────────────────────────────────────────
# Archer (multishot): fan-of-arrows scaled through multistrike and pierce
# Atlas: _RHFSI = _, ranged, high, flat, solo, instant
# EA-2023 + 1.0-2024; prov: fw;kb
KITS.append({
    "kit_id": "hot-archer",
    "folk_name": "Archer (multishot)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_RHFSI-PMDD-SP-__-~~",
    "delivery": dc("projectile", 0.85, "fan of arrows fires simultaneously in a spread; each arrow is an individual projectile"),
    "footprint": dc("multi-point", 0.85, "spread fan of arrows covers multiple simultaneous hit points; multi-point volley"),
    "geo_text": "Archer auto-fires a fan of arrows in a spread pattern. Multistrike trait increases arrow count; Pierce trait adds lane-through behavior. The projectile-count platform of the roster. Ranged, high-tempo, solo build.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("projectile-count-scaling (SP)", "spend", "n/a", "n/a",
                    "SP = spend. Primary scaling = arrow count via Multistrike + Pierce upgrades. No per-arrow resource cost; auto-fires on cooldown.", 0.85),
    "element": elem("physical", "hit", 0.82),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("R", 0.88, "ranged bow attacks; fan of arrows"),
        pc("H", 0.85, "high tempo auto-fire arrow volleys"),
        pc("F", 0.82, "flat per-arrow damage; spread fan = consistent multi-point output"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.85, "instant auto-fire per volley"),
    ),
    "mechanics_notes": "'The projectile-count platform of the roster, the Diablo-3-Demon-Hunter homage' per mech_note. EA-2023 anchor = solid pre-cutoff provenance. Multistrike + Pierce traits = the Archer's two scaling levers. Fan-of-arrows = multi-point footprint.",
    "era_confirmed": "hot-ea-2023",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Multistrike adds arrows per fan; Pierce adds lane-through; attack speed items increase volley frequency.",
    "sources_used": ["fw (first-week guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 3. hot-sage-ring-blades ───────────────────────────────────────────────────
# Ring Blades Sage: orbiting blade rings with kill-on-spawn coverage — POST-CUTOFF (1.1-2026 ONLY)
KITS.append({
    "kit_id": "hot-sage-ring-blades",
    "folk_name": "Ring Blades Sage",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_DHFSI-PMDG-SP-__-~~",
    "delivery": dc("orbit", 0.45, "orbiting blade rings around player; post-cutoff conf capped"),
    "footprint": dc("ring", 0.45, "ring orbit pattern at fixed radius; 'everything dies before it gets on screen'; post-cutoff conf capped"),
    "geo_text": "Ring Blades Sage: orbiting blade rings with range and coverage stacked until 'everything dies before it gets on screen.' Kill-on-spawn coverage at extreme orbit radius. Forum's own words per mech_note. Ring orbit footprint.",
    "control": ctrl([], "none", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("single-axis-scaling (ring range + orbit coverage)", "spend", "n/a", "n/a",
                    "SP = spend. Primary scaling axis is ring orbit radius/coverage. Post-cutoff specifics unknown.", 0.42),
    "element": elem("physical", "hit", 0.42),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank; post-cutoff conf capped"),
        pc("D", 0.45, "mid-range orbit rings; post-cutoff conf capped"),
        pc("H", 0.45, "high tempo orbit rotation; post-cutoff conf capped"),
        pc("F", 0.42, "flat orbit damage per blade contact; post-cutoff conf capped"),
        pc("S", 0.45, "solo; self-contained orbit; post-cutoff conf capped"),
        pc("I", 0.45, "instant continuous orbit; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: hot-1.1-2026 is the ONLY era; all conf capped ≤0.50. Forum citation: 'everything dies before it gets on screen' = extreme orbit range coverage. Forum-paired with Arcane Splinters Sorceress as kill-on-spawn combo. Sage class with Ring Blades ability.",
    "era_confirmed": "hot-1.1-2026",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Ring Blades: range and rotation speed per upgrade tier (post-cutoff, unconfirmed).",
    "sources_used": ["sf-hot (Steam forums HoT, 1.1-2026 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 4. hot-dragons-breath ─────────────────────────────────────────────────────
# Dragon's Breath burn stream: continuous flame cone with compounding burn stacks
# Atlas: _DHFSI = _, mid, high, flat, solo, instant; DW economy (stack-scaling)
# G2 FLAG: TRUE BEAM (continuous flame cone = beam delivery)
KITS.append({
    "kit_id": "hot-dragons-breath",
    "folk_name": "Dragon's Breath (burn stream)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_DHFSI-PSDD-DW-__-~~",
    "delivery": dc("beam", 0.82, "continuous flame cone — sustained directional flame spray; TRUE BEAM delivery; Refined Flame + Fire Stream confirm beam identity"),
    "footprint": dc("cone", 0.80, "flame cone sprays outward in a widening forward arc; cone footprint"),
    "geo_text": "Dragon's Breath: continuous flame cone whose burn stacks compound with each target hit. 'Refined Flame' and 'Fire Stream' upgrades confirm sustained directional delivery. Burn stacks = the compounding DPS engine: more targets in the cone = more stacks = more damage.",
    "control": ctrl(["burn"], "core", 0.82),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("stack-scaling (DW — burn stacks compound)", "proc", "n/a", "on_hit",
                    "DW = drain-while (continuous delivery). Economy is burn-stack compounding: each hit applies burn; stacks accumulate per target in the cone; more stacks = higher DPS. Not a traditional resource drain but a continuous delivery that generates accumulating DoT.", 0.80),
    "element": elem("fire", "hybrid", 0.82),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("D", 0.80, "mid-range flame cone; not melee contact, not long-range"),
        pc("H", 0.80, "high-tempo continuous delivery — flame cone fires at maximum rate"),
        pc("F", 0.78, "flat per-tick flame damage; burn stacks compound but individual ticks are flat"),
        pc("S", 0.80, "solo; no proxy"),
        pc("I", 0.82, "instant continuous auto-fire cone"),
    ),
    "mechanics_notes": "G2 flag: TRUE BEAM — continuous flame cone = sustained directional delivery (beam). Cone footprint (NOT lane — widening spread). Burn-stack compounding is the scale mechanic. 'Refined Flame and Fire Stream upgrades push it to S-tier' per mech_note.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Refined Flame upgrade increases burn stack rate; Fire Stream upgrade extends cone range; burn damage scales with stack count.",
    "sources_used": ["sf-hot (Steam forums HoT)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 5. hot-exterminator-burn ──────────────────────────────────────────────────
# Burn Exterminator: flamethrower class — scales ONE stat (BURN) with survivability
# Atlas: _DHFSI = _, mid, high, flat, solo, instant
# G2 FLAG: TRUE BEAM (flamethrower = beam delivery)
KITS.append({
    "kit_id": "hot-exterminator-burn",
    "folk_name": "Burn Exterminator",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_DHFSI-PSDM-SP-__-~~",
    "delivery": dc("beam", 0.80, "flamethrower class = sustained directional flame beam; TRUE BEAM delivery"),
    "footprint": dc("cone", 0.78, "flamethrower cone; widening flame spray in faced direction"),
    "geo_text": "Burn Exterminator: the flamethrower class builds around maximizing one stat — BURN — with survivability behind it. The July 2026 guide uses this as the example for 'single-axis mastery.' Flamethrower = beam delivery with cone footprint.",
    "control": ctrl(["burn"], "core", 0.80),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("single-axis-scaling (SP — burn stat only)", "spend", "n/a", "n/a",
                    "SP = spend / single-axis. One stat (BURN) is the sole scaling target. All other stats deprioritized except survivability floor. Simple scaling philosophy.", 0.80),
    "element": elem("fire", "hybrid", 0.80),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("D", 0.78, "mid-range flamethrower cone"),
        pc("H", 0.80, "high tempo continuous flamethrower output"),
        pc("F", 0.78, "flat burn DPS; single-axis scaling = flat per-tick fire"),
        pc("S", 0.78, "solo; no proxy"),
        pc("I", 0.80, "instant continuous auto-fire"),
    ),
    "mechanics_notes": "G2 flag: TRUE BEAM — flamethrower = sustained directional fire beam. Cone footprint. Distinct from Dragon's Breath: different class/character identity, though same beam/cone delivery. Single-axis-scaling (SP) philosophy: 'scale one thing.' '1.1-2026 guide uses it as the example' — note that 1.1 is post-cutoff; build philosophy captured from 1.0-era forum data.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "All upgrades funnel into BURN stat; survivability items add HP/defense as secondary floor.",
    "sources_used": ["pg (player guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 6. hot-kugelblitz ─────────────────────────────────────────────────────────
# Kugelblitz: wandering ball lightning that zaps whatever it drifts past
# Atlas: _DMFLI = _, mid, med, flat, light-proxy, instant; SU economy (uptime-passive)
KITS.append({
    "kit_id": "hot-kugelblitz",
    "folk_name": "Kugelblitz (wandering ball lightning)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_DMFLI-PSDD-SU-__-~~",
    "delivery": dc("other", 0.80, "autonomous wandering orb that zaps nearby enemies as it drifts; neither at-target nor orbit — self-propelled wandering entity"),
    "footprint": dc("small-radius", 0.78, "zap radius around orb's current position; small contact zone as orb drifts"),
    "geo_text": "Kugelblitz: a crackling ball of lightning that WANDERS the field on its own path, zapping whatever it drifts past. Not player-directed — the orb follows its own movement logic. Light-proxy: the wandering ball acts as an independent agent fighting alongside the player.",
    "control": ctrl(["shock", "stun"], "rider", 0.78),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("uptime-passive (SU — orb persists while active)", "reserve", "n/a", "n/a",
                    "SU = summon/uptime-passive. The Kugelblitz orb persists as an autonomous entity. No per-zap resource cost; the orb maintains itself while active. Light-proxy uptime economy.", 0.80),
    "element": elem("lightning", "hit", 0.80),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("D", 0.78, "mid-range field presence; orb wanders in mid-field proximity"),
        pc("M", 0.78, "medium tempo; zap cadence as orb drifts through enemies"),
        pc("F", 0.78, "flat per-zap lightning damage; consistent as orb drifts"),
        pc("L", 0.80, "light-proxy — wandering autonomous orb fights alongside player"),
        pc("I", 0.80, "instant zap on contact; no wind-up"),
    ),
    "mechanics_notes": "Wandering-hazard delivery: not orbit (fixed radius) and not at-target (no player aim). The orb follows its own wandering path — autonomous proxy entity. 'Wandering-hazard archetype' per mech_note. Shock/stun riders from lightning element. EA-2023 anchor — solid pre-cutoff provenance.",
    "era_confirmed": "hot-ea-2023",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Kugelblitz upgrades increase zap frequency, damage, and orb count; range upgrades expand zap radius.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 7. hot-warlock ────────────────────────────────────────────────────────────
# Warlock summon caster: dark-caster with light-proxy summons — damage-quest workhorse
# Atlas: _DMFLI = _, mid, med, flat, light-proxy, instant
KITS.append({
    "kit_id": "hot-warlock",
    "folk_name": "Warlock (summon caster)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_DMFLI-PSDM-SP-__-~~",
    "delivery": dc("at-target", 0.80, "dark caster spells target enemies; summons fight alongside as light-proxy"),
    "footprint": dc("small-radius", 0.78, "spell AOE at target + summon melee zone; small-radius per spell"),
    "geo_text": "Warlock: dark-caster seat of the roster. Forum-cited as a damage-quest workhorse. Casts dark spells at enemies and maintains light-proxy summons. The seventh game in the corpus to ship a caster-summoner archetype.",
    "control": ctrl(["drain", "curse"], "rider", 0.78),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("single-axis-scaling (SP — dark spell damage)", "spend", "n/a", "n/a",
                    "SP = spend. Scaling axis is dark magic damage output from spells. Summon uptime is secondary. No per-spell resource beyond auto-fire cooldown.", 0.80),
    "element": elem("dark/arcane", "hybrid", 0.78),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("D", 0.78, "mid-range caster; spells targeted at mid-range enemies"),
        pc("M", 0.78, "medium tempo spell cadence"),
        pc("F", 0.78, "flat dark spell damage per cast"),
        pc("L", 0.80, "light-proxy — summons fight alongside caster"),
        pc("I", 0.80, "instant auto-fire dark spells"),
    ),
    "mechanics_notes": "'The SEVENTH game in the corpus to ship a caster-summoner archetype' — Elrond/Gandalf note: convergence data point for summoner-caster pattern. Corpus cites this explicitly as a lineage marker. Damage-quest workhorse from forum data (sf-hot).",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Warlock: dark spell damage upgrades; summon HP/damage upgrades from item pool.",
    "sources_used": ["sf-hot (Steam forums HoT)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 8. hot-norseman-frost-avalanche ───────────────────────────────────────────
# Frost Avalanche Norseman: DR draft strategy — skip all else, focus ONLY on Frost Avalanche
# Atlas: _DMSSI = _, mid, med, spiky, solo, instant; DR economy (offer-pool-hygiene)
KITS.append({
    "kit_id": "hot-norseman-frost-avalanche",
    "folk_name": "Frost Avalanche Norseman",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_DMSSI-PLMM-DR-__-~~",
    "delivery": dc("at-target", 0.82, "large cold avalanche AOE strikes at enemy cluster positions; zone delivery"),
    "footprint": dc("large-zone", 0.82, "frost avalanche = large AOE zone of cold damage; area denial"),
    "geo_text": "Frost Avalanche Norseman: character guide explicitly says 'skip every other ability and hunt ONLY Frost Avalanche upgrades' because off-build upgrades dilute the offer pool. DR (draft) economy: offer-pool hygiene drives the strategy — intentionally narrow upgrade path to maximize Frost Avalanche appearances.",
    "control": ctrl(["freeze", "slow"], "core", 0.82),
    "defense": defs(["armor"], "armor", 0.80),
    "economy": econ("offer-pool-hygiene (DR — intentional narrow draft path)", "draft", "n/a", "n/a",
                    "DR = draft/offer-pool. The build economy is CHOOSING WHAT NOT TO TAKE — skipping all non-Frost-Avalanche upgrades keeps the offer pool pure. The strategic depth is negative selection in the draft.", 0.82),
    "element": elem("cold", "hybrid", 0.82),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("D", 0.80, "mid-range avalanche AOE zone"),
        pc("M", 0.80, "medium tempo — avalanche fires on cooldown"),
        pc("S", 0.82, "spiky amplitude — frost avalanche is a large burst per cast"),
        pc("S", 0.82, "solo; no proxy"),
        pc("I", 0.82, "instant trigger per auto-fire cycle"),
    ),
    "mechanics_notes": "Offer-pool-hygiene economy: 'skip every other ability — off-build upgrades dilute the offer pool' = the first explicit documentation of this meta-strategy in the corpus. DR in old vocab = draft/pool-management. Norseman class with Frost Avalanche as signature ability. Cold element with freeze/slow control.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Frost Avalanche upgrades: damage, AOE radius, and freeze duration. All other upgrades skipped per draft strategy.",
    "sources_used": ["fw (first-week guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 9. hot-cleric-radiant ─────────────────────────────────────────────────────
# Radiant Aura Cleric: holy body-aura + sustain — aura-passive RS economy
# Atlas: _MHFSI = _, melee, high, flat, solo, instant; RS (aura-passive)
KITS.append({
    "kit_id": "hot-cleric-radiant",
    "folk_name": "Radiant Aura Cleric",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_MHFSI-PSDM-RS-__-~~",
    "delivery": dc("aura-pulse", 0.85, "passive holy halo pulses damage around player body; aura-pulse delivery"),
    "footprint": dc("small-radius", 0.85, "body-adjacent holy aura zone; enemies must enter melee range"),
    "geo_text": "Radiant Aura Cleric: passive holy halo grinds everything that steps into arm's reach. Sustain loop: heals keep the Cleric alive while the aura does continuous damage. 'The holy-body-aura build' per mech_note.",
    "control": ctrl(["slow", "stagger"], "rider", 0.78),
    "defense": defs(["sustain-leech"], "sustain-leech", 0.85),
    "economy": econ("aura-passive reserve (RS — always-on holy halo)", "reserve", "n/a", "n/a",
                    "RS = reserve/aura-passive. Radiant Aura is always active — no per-pulse resource cost. The sustain-loop keeps the Cleric topped via heals. Slot investment = the only economy unit.", 0.85),
    "element": elem("holy", "hit", 0.82),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("M", 0.85, "melee-adjacent body aura; enemies must contact player to take damage"),
        pc("H", 0.85, "high-frequency pulse; aura hits at maximum continuous rate"),
        pc("F", 0.82, "flat aura damage per pulse; consistent per-contact output"),
        pc("S", 0.82, "solo; self-contained aura"),
        pc("I", 0.85, "instant continuous aura — no cast trigger"),
    ),
    "mechanics_notes": "Aura-pulse delivery (same as VS soul-eater pattern): body-hugging passive halo. RS (reserve) economy = always-on. Sustain-leech as primary defense — heals are the survival mechanism, not avoidance. Cleric class identity: holy aura + sustain.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Radiant Aura: damage and pulse rate per tier; Heal upgrades increase sustain throughput.",
    "sources_used": ["pg (player guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 10. hot-swordsman ─────────────────────────────────────────────────────────
# Swordsman starter slash: frontal slash-arc — Diablo-1-warrior homage
# Atlas: _MHFSI = _, melee, high, flat, solo, instant
KITS.append({
    "kit_id": "hot-swordsman",
    "folk_name": "Swordsman (starter slash)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_MHFSI-PSDM-SP-__-~~",
    "delivery": dc("self-origin", 0.88, "frontal sword slash-arc sweeps from player body; melee forward arc delivery"),
    "footprint": dc("small-radius", 0.85, "frontal slash-arc small-radius cone in front of player"),
    "geo_text": "Swordsman frontal slash-arc: the default first-run class. 'The Diablo-1-warrior homage whose whole identity is teaching the basics.' Slash fires as a frontal arc in the player's movement direction. High tempo, flat damage, melee contact.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["armor"], "armor", 0.85),
    "economy": econ("single-axis-scaling (SP — slash damage)", "spend", "n/a", "n/a",
                    "SP = spend. Slash damage is the primary upgrade target. High-tempo auto-slash fires continuously while moving.", 0.85),
    "element": elem("physical", "hit", 0.85),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("M", 0.88, "melee frontal arc; sword contact range"),
        pc("H", 0.88, "high tempo auto-slash"),
        pc("F", 0.85, "flat per-slash damage; consistent arc output"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant auto-slash trigger"),
    ),
    "mechanics_notes": "'The frontal slash-arc default everyone's first run uses — the Diablo-1-warrior homage whose whole identity is teaching the basics' per mech_note. EA-2023 anchor = launch-floor class. Armor primary defense (melee class = armor chassis). The tutorial-floor archetype in HoT.",
    "era_confirmed": "hot-ea-2023",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Swordsman: slash damage and arc width per tier; Multistrike adds additional slash swings per cycle.",
    "sources_used": ["fw (first-week guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 11. hot-spirit-warrior ────────────────────────────────────────────────────
# Spirit Warrior: phantom blade-wielder fighting alongside the player
# Atlas: _MMFLI = _, mid, med, flat, light-proxy, instant; SU (uptime-passive)
KITS.append({
    "kit_id": "hot-spirit-warrior",
    "folk_name": "Spirit Warrior",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_MMFLI-PSDM-SU-__-~~",
    "delivery": dc("at-target", 0.80, "phantom blade-wielder silhouette swings at enemies near player; proxy fights for caster"),
    "footprint": dc("small-radius", 0.78, "phantom melee zone around the spirit's position; small-radius contact range"),
    "geo_text": "Spirit Warrior: a phantom blade-wielder who swings alongside the player. 'The ghost-proxy strand where a second silhouette fights your fight.' Light-proxy: the phantom is independent but fragile — a light proxy layer, not a heavy summon.",
    "control": ctrl([], "none", 0.78),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("uptime-passive (SU — phantom persists while active)", "reserve", "n/a", "n/a",
                    "SU = summon-uptime. The spirit phantom persists continuously while active. No per-swing resource cost; the phantom auto-attacks independently.", 0.80),
    "element": elem("physical", "hit", 0.80),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("M", 0.78, "mid-range phantom melee; phantom fights at player-adjacent mid-range"),
        pc("M", 0.78, "medium tempo phantom swings"),
        pc("F", 0.78, "flat per-swing phantom damage"),
        pc("L", 0.80, "light-proxy — second silhouette fights alongside player"),
        pc("I", 0.80, "instant phantom auto-swing"),
    ),
    "mechanics_notes": "Ghost-proxy archetype: 'a second silhouette fights your fight' — the light-proxy category in clearest form. SU (summon) economy = persistent uptime. 1.0-2024 only era — pre-cutoff, solid confidence. Distinct from heavy summon (which tanks); phantom is light-proxy (aids without tanking).",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Spirit Warrior: phantom damage and swing speed per tier.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 12. hot-astronomer-orbs ───────────────────────────────────────────────────
# Astronomer's Orbs: celestial orbs circling body in slow orbital shells
# Atlas: _MMFSI = _, mid, med, flat, solo, instant; SU (uptime-passive)
KITS.append({
    "kit_id": "hot-astronomer-orbs",
    "folk_name": "Astronomer's Orbs",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_MMFSI-PSDM-SU-__-~~",
    "delivery": dc("orbit", 0.85, "celestial orbs orbit the player body in layered orbital shells; slow persistent orbit"),
    "footprint": dc("ring", 0.85, "multiple orbital shells create concentric ring coverage around player body"),
    "geo_text": "Astronomer's Orbs: celestial orbs circling the body in slow orbital shells. 'The second GX-09 member in the same small roster; orbit as this game's primary defensive grammar' per mech_note — orbit is the dominant delivery type in HoT.",
    "control": ctrl(["stagger"], "rider", 0.78),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("uptime-passive (SU — orbs persist in orbit)", "reserve", "n/a", "n/a",
                    "SU = summon-uptime. Orbs persist in orbit continuously. No per-hit resource cost.", 0.82),
    "element": elem("arcane/celestial", "hit", 0.78),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("M", 0.82, "mid-range orbit shells around body"),
        pc("M", 0.82, "medium tempo slow orbit rotation"),
        pc("F", 0.80, "flat per-orb contact damage; consistent orbit output"),
        pc("S", 0.82, "solo; orbit is self-contained shell"),
        pc("I", 0.82, "instant continuous orbit"),
    ),
    "mechanics_notes": "Orbit delivery + ring footprint (same grammar as VS-unholy-vespers). 'Second GX-09 member in the same roster' = corpus crossref noting that hot-astronomer-orbs and vs-unholy-vespers both share the orbit/ring grammar (GX-09 in old cell taxonomy). Concentric orbital shells = layered ring footprint.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Orb count and orbit radius per tier; additional orbital shell layers at higher upgrade levels.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 13. hot-shieldmaiden-block ────────────────────────────────────────────────
# Block-Stack Shieldmaiden: stack block stat → doubled hammer-splash at level 60
# Atlas: _MMFSI = _, mid, med, flat, solo, instant; SW economy (stat-threshold-payoff)
KITS.append({
    "kit_id": "hot-shieldmaiden-block",
    "folk_name": "Block-Stack Shieldmaiden",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_MMFSI-PSDT-SW-__-~~",
    "delivery": dc("self-origin", 0.82, "hammer-splash melee retaliation from player body when block threshold triggers"),
    "footprint": dc("small-radius", 0.82, "hammer-splash small-radius AOE on block-triggered retaliation"),
    "geo_text": "Shieldmaiden: stack block stat into the hundreds, then let the doubled hammer-splash at level 60 do the clearing. 'Tank-stat-as-weapon' build: the defensive stat (block) becomes the offensive output. Block threshold → hammer-splash proc.",
    "control": ctrl(["stagger", "knockback"], "rider", 0.80),
    "defense": defs(["block", "armor"], "block", 0.88),
    "economy": econ("stat-threshold-payoff (SW — block count → hammer proc)", "proc", "n/a", "on_block",
                    "SW = stat-threshold-payoff. Economy: invest entirely in BLOCK stat; when block count exceeds threshold, a hammer-splash proc triggers. At level 60, the hammer-splash damage is doubled. Block stat = both defense AND the offensive proc trigger.", 0.85),
    "element": elem("physical", "hit", 0.82),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("M", 0.82, "mid-range hammer splash from body"),
        pc("M", 0.82, "medium tempo — proc fires on block events, not continuous"),
        pc("F", 0.80, "flat hammer damage per proc; consistent splash amplitude"),
        pc("S", 0.82, "solo; self-contained block-proc loop"),
        pc("I", 0.85, "instant hammer proc on block"),
    ),
    "mechanics_notes": "Stat-threshold-payoff economy: 'stack block into the hundreds and let the doubled hammer-splash at level 60 do the clearing.' D1: BLOCK primary (block is both defense AND offense trigger). The unique mechanic is tank-stat-as-weapon: defensive investment creates offensive output. Level 60 double = capstone reward.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Block stat investment per item; Hammer-Splash upgrades increase proc damage; level 60 capstone doubles proc.",
    "sources_used": ["sf-hot (Steam forums HoT)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 14. hot-phantom-needles ───────────────────────────────────────────────────
# Phantom Needles: spectral pierce-line filler threading through the horde
# Atlas: _RHFSI = _, ranged, high, flat, solo, instant; SU (uptime-passive)
KITS.append({
    "kit_id": "hot-phantom-needles",
    "folk_name": "Phantom Needles",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_RHFSI-PNDD-SU-__-~~",
    "delivery": dc("projectile", 0.82, "spectral needle projectiles thread through enemy lines via pierce; ranged linear pierce"),
    "footprint": dc("lane", 0.82, "pierce-through lane: needles travel in a linear path hitting all enemies in a lane"),
    "geo_text": "Phantom Needles: spectral needle volleys threading through the horde via pierce. 'The pierce-line filler that stacks quietly under any main.' Pierce = every needle hits ALL enemies in a linear lane. Ranged, high-tempo, solo filler ability.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("uptime-passive (SU — needles auto-fire continuously)", "reserve", "n/a", "n/a",
                    "SU = uptime-passive. Phantom Needles auto-fire continuously without resource cost. 'Stacks quietly under any main' = passive filler economy — it just runs.", 0.82),
    "element": elem("physical/phantom", "hit", 0.80),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("R", 0.82, "ranged piercing needle projectiles"),
        pc("H", 0.82, "high tempo auto-fire volleys"),
        pc("F", 0.80, "flat per-needle damage; consistent pierce output"),
        pc("S", 0.82, "solo; filler ability with no proxy"),
        pc("I", 0.82, "instant auto-fire per volley"),
    ),
    "mechanics_notes": "Lane footprint from pierce behavior: needles travel in a straight line hitting all enemies in their path. Delivery=projectile (individual needle, not a sustained beam). 'Pierce-line filler' = secondary ability slot rather than primary damage dealer. Uptime-passive SU economy.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Pierce count and needle damage per tier; spread upgrades increase simultaneous needle volleys.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 15. hot-meteor-strike ─────────────────────────────────────────────────────
# Meteor Strike: skyfall payloads at random impact zones — off-screen artillery
# Atlas: _RLSSI = _, ranged, low, spiky, solo, instant; SU (uptime-passive)
KITS.append({
    "kit_id": "hot-meteor-strike",
    "folk_name": "Meteor Strike",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_RLSSI-PSDD-SU-__-~~",
    "delivery": dc("at-target", 0.85, "meteors fall at random enemy positions from off-screen; no player aiming"),
    "footprint": dc("small-radius", 0.85, "meteor AOE impact zone on landing; small-radius crater damage"),
    "geo_text": "Meteor Strike: skyfall payloads hammering random enemy impact zones. 'Off-screen artillery in the survivor idiom, the spike-damage slot of the ability roster' per mech_note. Low tempo (each meteor is massive burst); spiky amplitude.",
    "control": ctrl(["stagger", "knockback"], "rider", 0.80),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("uptime-passive (SU — meteors auto-fire on cooldown)", "reserve", "n/a", "n/a",
                    "SU = uptime-passive. Meteors auto-target random enemies on a slow cooldown. Low fire rate = each meteor is a significant spike.", 0.85),
    "element": elem("physical/fire", "hybrid", 0.80),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank"),
        pc("R", 0.85, "ranged skyfall; off-screen origin, no player aim"),
        pc("L", 0.85, "low tempo — slow meteor cadence; each is a large burst"),
        pc("S", 0.88, "spiky amplitude — each meteor is a large spike"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.85, "instant detonation on impact"),
    ),
    "mechanics_notes": "Off-screen artillery archetype (same as VS-thunder-loop, hades1-ares-doom). 'The spike-damage slot' = single large burst per meteor. Random targeting = player cannot direct. Spiky amplitude + low tempo = the spike-DPS slot, not the sustain slot. 1.0-2024 only era.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Meteor: damage and AOE radius per tier; cooldown reduction items increase fire rate.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 16. hot-landsknecht-grenades ──────────────────────────────────────────────
# Grenade Landsknecht: grenade damage SCALES OFF OTHER PROJECTILE DAMAGE — POST-CUTOFF (1.1-2026)
KITS.append({
    "kit_id": "hot-landsknecht-grenades",
    "folk_name": "Grenade Landsknecht",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_RMSSI-PSDD-SP-__-~~",
    "delivery": dc("projectile", 0.45, "grenade thrown projectile; detonates on impact; post-cutoff conf capped"),
    "footprint": dc("small-radius", 0.45, "grenade AOE detonation; post-cutoff conf capped"),
    "geo_text": "Grenade Landsknecht: grenade damage SCALES OFF THE DAMAGE YOUR OTHER PROJECTILES DEAL. The Arquebus (primary ranged weapon) feeds the bombs. Derived-scaling structure: grenade is a damage amplifier, not an independent damage source.",
    "control": ctrl(["stagger", "knockback"], "rider", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("derived-scaling (grenade damage = f(other projectile damage))", "proc", "n/a", "other_projectile_damage",
                    "SP but with derived scaling: grenade damage is a multiplier of the primary weapon's damage. The economy is 'stack the primary weapon (Arquebus), grenades scale automatically.' Post-cutoff conf capped.", 0.42),
    "element": elem("physical/explosive", "hit", 0.42),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "HoT attr blank; post-cutoff conf capped"),
        pc("R", 0.45, "ranged grenade throw; post-cutoff conf capped"),
        pc("M", 0.42, "medium tempo; post-cutoff conf capped"),
        pc("S", 0.45, "spiky per-grenade detonation; post-cutoff conf capped"),
        pc("S", 0.42, "solo; post-cutoff conf capped"),
        pc("I", 0.45, "instant auto-throw; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: hot-1.1-2026 is the ONLY era; all conf capped ≤0.50. DERIVED-SCALING structure: 'Arquebus feeds the bombs' — grenade damage is derived from primary weapon damage. This is a unique economy model in the corpus: one weapon's output becomes another weapon's scaling input.",
    "era_confirmed": "hot-1.1-2026",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Grenade damage scales with Arquebus upgrades; direct grenade upgrades also stack (post-cutoff, unconfirmed details).",
    "sources_used": ["fw (first-week guide, 1.1 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 17. hot-gear-well-retrieval ───────────────────────────────────────────────
# Gear/Well retrieval economy: real ARPG items drop mid-run, must be carried to Well
# Atlas: _____I = _, _, _, _, _, instant; AM economy (loot-retrieval+draft-lock)
# Meta-system record = ARPG bridge
KITS.append({
    "kit_id": "hot-gear-well-retrieval",
    "folk_name": "Gear/Well retrieval economy (the ARPG bridge)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_____I-P___-AM-__-~~",
    "delivery": dc("other", 0.85, "meta-system record: gear economy, not a combat skill"),
    "footprint": dc("other", 0.82, "meta-system; no spatial footprint"),
    "geo_text": "Real ARPG items drop mid-run with affixes. To extract them for persistent use, the player must physically carry gear to a WELL within the run. Draft-lock: once a gear item is committed, the run slot is locked. The ARPG bridge: horde-survivor meets item-drop economy.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["other"], "other", 0.80),
    "economy": econ("loot-retrieval+draft-lock (AM — carry gear to Well to extract)", "ammo", "n/a", "n/a",
                    "AM = ammo-retrieve analog. The gear item IS the ammo: player must physically carry it to the Well (like retrieving ammunition). Once extracted, gear persists. Draft-lock: committing to retrieve one item may mean skipping others. The Well is the extraction point.", 0.85),
    "element": elem("n/a", "hit", 0.78),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-system; no attr"), pc("_", 0.50, "meta-system; no range"),
        pc("_", 0.50, "meta-system; no tempo"), pc("_", 0.50, "meta-system; no amp"),
        pc("_", 0.50, "meta-system; no proxy"),
        pc("I", 0.80, "instant item pickup trigger"),
    ),
    "mechanics_notes": "ARPG bridge meta-system record. The loot-retrieval mechanic is unique in the horde-survivor corpus: VS and other survivors have auto-pickup; HoT requires active carry-to-Well. This creates spatial risk/reward: divert to retrieve valuable gear while enemies close in. AM (ammo) economy = the gear is 'carried ammo' that pays out on Well delivery. Prov: pg;sf-hot;kb.",
    "era_confirmed": "hot-ea-2023",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (meta-system record, not a skill/ability)",
    "sources_used": ["pg (player guide)", "sf-hot (Steam forums HoT)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 18. hot-artifact-stack ────────────────────────────────────────────────────
# Artifact-stack runs: Torment Banner + other artifacts = self-authored difficulty
# Atlas: _____I = _, _, _, _, _, instant; SP + self-authored-difficulty
# Meta-system record
KITS.append({
    "kit_id": "hot-artifact-stack",
    "folk_name": "Artifact-stack runs (Torment Banner et al.)",
    "game": "hot",
    "status": "positive",
    "atlas_key": "_____I-____-SP-__-~~",
    "delivery": dc("other", 0.82, "meta-system: artifact modifiers alter run parameters, not combat skills"),
    "footprint": dc("other", 0.80, "meta-system; no spatial footprint"),
    "geo_text": "Artifact-stack runs: stack run-modifier artifacts (Torment Banner for density, Hastening Sands, Restless Wheel, Malignant Mirror) to buy harder-but-more-rewarding runs. 'Self-authored difficulty': the player chooses their own challenge tier via artifact combinations.",
    "control": ctrl([], "none", 0.78),
    "defense": defs(["other"], "other", 0.78),
    "economy": econ("self-authored-difficulty (artifact slot investment)", "other", "n/a", "n/a",
                    "SP base economy (runs themselves). The artifact economy is meta: each artifact stacked = harder monsters + better loot. Hastening Sands (speed), Restless Wheel (spawn rate), Malignant Mirror (damage taken) — stacking these is the self-authored difficulty economy.", 0.82),
    "element": elem("n/a", "hit", 0.75),
    "movement": HOT_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "meta-system; no attr"), pc("_", 0.50, "meta-system; no range"),
        pc("_", 0.50, "meta-system; no tempo"), pc("_", 0.50, "meta-system; no amp"),
        pc("_", 0.50, "meta-system; no proxy"), pc("I", 0.78, "instant artifact activation pre-run"),
    ),
    "mechanics_notes": "Self-authored-difficulty grammar: the artifact stack IS the difficulty/reward modifier. Named artifacts: Torment Banner (enemy density), Hastening Sands (speed), Restless Wheel (spawn cadence), Malignant Mirror (damage taken). Each artifact stacked = compounding challenge + reward scaling. Meta-system spanning EA-2023 through 1.1-2026.",
    "era_confirmed": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "n/a (meta-system; artifact counts increase via completion unlocks)",
    "sources_used": ["sf-hot (Steam forums HoT)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 19. hot-blood-catcher — NEGATIVE ──────────────────────────────────────────
# Negative: Blood Catcher relic with unintended compounding → hundred-billion damage (pre-fix)
KITS.append({
    "kit_id": "hot-blood-catcher",
    "folk_name": "Blood Catcher (pre-fix)",
    "game": "hot",
    "status": "negative",
    "atlas_key": "___S__-____-SP-__-~~",
    "delivery": dc("other", 0.82, "relic interaction — not a direct combat delivery; compounding damage multiplier via unintended interaction"),
    "footprint": dc("other", 0.80, "no spatial footprint; numeric overflow mechanic"),
    "why_negative": "Unintended-compounding: Blood Catcher relic produced hundred-billion damage totals before the developer fix. The interaction compounded damage in an unintended recursive loop. Fixed in a subsequent patch. Negative: documents the failure mode, not a viable build. 'The forum eulogizes it fondly' = known-broken artifact of community nostalgia.",
    "era_span": "hot-1.0-2024",
    "post_cutoff": False,
    "dossier_owed": False,
    "prov": "sf-hot",
    "mech_note": "Pre-fix relic interaction. The forum documents this as a legendary bug: hundred-billion damage numbers from a compounding relic interaction. Developer fixed in a subsequent patch. Negative status: the interaction is patched, not a viable mechanic. Community nostalgia document.",
})

# ── output ────────────────────────────────────────────────────────────────────
pos  = [k for k in KITS if k.get("status") == "positive"]
neg  = [k for k in KITS if k.get("status") == "negative"]
pct  = [k for k in KITS if k.get("post_cutoff")]

with OUT.open("w") as f:
    for k in KITS:
        f.write(json.dumps(k) + "\n")

print(f"Halls of Torment: {len(KITS)} records | pos={len(pos)} neg={len(neg)} post-cutoff={len(pct)}")
print(f"Written: {OUT}")

print("\n=== DIRECTED SWEEP RESULTS (Halls of Torment) ===")
print("C2 (support-existence): NO pure-support kit. HoT is solo horde-survival; no multi-actor support.")
print("G2 (line-vs-projectile):")
print("  TRUE BEAM: hot-dragons-breath (continuous flame cone = beam + cone footprint)")
print("  TRUE BEAM: hot-exterminator-burn (flamethrower class = beam + cone footprint)")
print("  Lane footprint (projectile NOT beam): hot-phantom-needles (pierce-line)")
print("  No other true beams or lines in HoT corpus.")
print("D1 (shield-split):")
print("  BLOCK: hot-shieldmaiden-block (block-stat = primary defense AND offense proc)")
print("  SUSTAIN-LEECH: hot-cleric-radiant (holy aura + sustain heals)")
print("  ARMOR: hot-swordsman, hot-norseman-frost-avalanche (melee and heavy classes)")
print("  LIGHT-PROXY: hot-kugelblitz, hot-warlock, hot-spirit-warrior (proxy agent defense)")
print("  GLASS: hot-sorceress-splinters, hot-archer, hot-phantom-needles, hot-meteor-strike, etc.")
print("NOTABLE ECONOMIES:")
print("  Offer-pool-hygiene: hot-norseman-frost-avalanche (DR draft — intentional narrow pick path)")
print("  Stat-threshold-payoff: hot-shieldmaiden-block (block count → hammer proc)")
print("  Loot-retrieval+draft-lock: hot-gear-well-retrieval (AM — carry gear to Well = ARPG bridge)")
print("  Derived-scaling: hot-landsknecht-grenades (grenade = f(arquebus damage))")
print("POST-CUTOFF roster:")
for k in pct:
    print(f"  {k['kit_id']} | {k.get('era_confirmed','')}")
print("NEGATIVES:")
for k in neg:
    print(f"  {k['kit_id']} | {k.get('why_negative','')[:80]}")
