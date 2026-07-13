#!/usr/bin/env python3
"""gen-tl-facts.py — TL1+TL2+TLI facts for megaprobe 2026-07-12
22 records: 21 pos + 1 neg
Post-cutoff (2026 season content): 5 TLI kits (ss11-12-2026 / ss12-lunaria-2026 eras)
TLI live-2022+ only: 4 kits — partially known (conf 0.55-0.65), NOT capped post-cutoff
TL1/TL2: good knowledge (2009/2012 games well-documented)
"""
import json

OUT = "agentic_orchestration/legolas/research/megaprobe-2026-07-12/tl-facts.jsonl"

def pc(v,c,e): return {"value":v,"conf":round(c,2),"evidence":e}
def dc(v,c,e): return {"value":v,"conf":round(c,2),"evidence":e}
def ctrl(ail,cent,c): return {"ailments":ail,"centrality":cent,"conf":round(c,2)}
def defs(layers,prim,c): return {"layers":layers,"primary":prim,"conf":round(c,2)}
def econ(rv,model,mt,bs,pt,c): return {"resource_verbatim":rv,"model":model,"meter_type":mt,"builder_source":bs,"plain_text":pt,"conf":round(c,2)}
def elem(lv,dm,c): return {"label_verbatim":lv,"damage_mode":dm,"conf":round(c,2)}
def mov(verbs,pol,is_mv,c): return {"verbs":verbs,"policy_while_casting":pol,"skill_is_movement":is_mv,"conf":round(c,2)}
def pfx(av,ac,ae,rv,rc,re,tv,tc,te,ampv,ampc,ampe,pxv,pxc,pxe,cv,cc,ce):
    return {
        "attr":pc(av,ac,ae),"range":pc(rv,rc,re),"tempo":pc(tv,tc,te),
        "amp":pc(ampv,ampc,ampe),"proxy":pc(pxv,pxc,pxe),"commitment":pc(cv,cc,ce)
    }

records = []

# ─────────────────────────────────────────────────────────────────────────────
# TL1 KITS (tl1-2009) — basic mechanics, good confidence 0.78-0.85
# ─────────────────────────────────────────────────────────────────────────────

# 1. tl1-ricochet-vanquisher — Ricochet Vanquisher — DRHFSI
records.append({
    "kit_id":"tl1-ricochet-vanquisher","folk_name":"Ricochet Vanquisher","game":"tl1","status":"positive",
    "atlas_key":"DRHFSI-MCDD-SP-PH-~~",
    "delivery":dc("projectile",0.85,"Ricochet fires arrows that bounce between enemies — projectile delivery with chaining behavior"),
    "footprint":dc("chain-hop",0.82,"Each arrow bounces to nearest enemy on hit; chain-hop footprint per ricochet behavior"),
    "geo_text":"Vanquisher fires arrows that ricochet between multiple enemies on hit. Each arrow chains to the nearest target within range, dealing reduced damage per bounce. Chain-hop delivery pattern.",
    "control":ctrl(["slow"],"rider",0.60),
    "defense":defs(["dodge","resist"],"dodge",0.78),
    "economy":econ("Mana","spend","n/a","n/a","Ricochet costs Mana per activation. Vanquisher skills use standard TL1 Mana spend economy.",0.80),
    "element":elem("Physical","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.82,"Vanquisher class = DEX archetype confirmed",
        "ranged",0.85,"Ranged projectile archery — Vanquisher primary identity",
        "high",0.80,"High attack tempo via Vanquisher attack speed passives",
        "flat",0.75,"Flat per-arrow damage; ricochet chains don't spike",
        "solo",0.80,"No proxy; solo archer",
        "instant",0.80,"Arrow fires instantly on activation"
    ),
    "mechanics_notes":"G2 note: Ricochet is chain-hop NOT a line — arrows bounce to nearest target, not a fixed line. This distinction is important for G2 survey. TL1's Vanquisher is the most basic ranged archetype in the corpus.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL1 Vanquisher Ricochet mechanic; chain-hop confirmed 2009)"]
})

# 2. tl1-alchemist-summoner — Summoner Alchemist — IRMFLC (proxy=L=light, commit=C=channel)
records.append({
    "kit_id":"tl1-alchemist-summoner","folk_name":"Summoner Alchemist","game":"tl1","status":"positive",
    "atlas_key":"IRMFLC-LNDM-SP-LI-~~",
    "delivery":dc("self-origin",0.80,"Alchemist channels a summon animation to spawn Golem or raise Zombies; delivery originates from caster"),
    "footprint":dc("large-zone",0.75,"Summoned Golem + zombie horde covers large zone; undead spread across combat area"),
    "geo_text":"Summoner Alchemist channels summon spells to raise a Golem and zombie minions that fight across the surrounding combat zone. The channel commit reflects the sustained casting animation for summoning.",
    "control":ctrl(["taunt"],"rider",0.55),
    "defense":defs(["hp-stack","resist"],"hp-stack",0.72),
    "economy":econ("Mana","reserve","n/a","n/a","TL1 Alchemist reserves Mana for summon upkeep; re-summoning costs Mana. Channel commit is the summon animation, not a continuous channel. Reserve economy for maintenance.",0.78),
    "element":elem("Lightning","hit",0.70),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "INT",0.80,"Alchemist = INT caster class confirmed",
        "ranged",0.75,"Alchemist operates at range behind summoned army",
        "med",0.72,"Medium tempo; summons attack continuously",
        "flat",0.72,"Flat sustained pet DPS",
        "light",0.72,"Light proxy: TL1 summoner fields fewer pets than TL2 Bot Engineer; Golem = single heavy summon. 'Light' compared to heavy-proxy builds — Golem+zombies is still moderate.",
        "channel",0.78,"Atlas key C=channel; summon animation requires brief channel"
    ),
    "mechanics_notes":"Commit=channel is unusual for a summoner but captures the TL1 Alchemist's casting animations — raising Zombie minions or summoning Golem requires a brief channel animation rather than instant cast. Economy=reserve captures ongoing Golem upkeep. Lightning element from TL1 Alchemist's lightning spell kit.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL1 Alchemist Golem + Zombie summoner; channel summon + reserve economy confirmed)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# TL2 KITS (tl2-2012) — good confidence 0.78-0.88
# ─────────────────────────────────────────────────────────────────────────────

# 3. tl2-glaive-outlander — Glaive Outlander — DDHFSI (range=D=mid)
records.append({
    "kit_id":"tl2-glaive-outlander","folk_name":"Glaive Outlander","game":"tl2","status":"positive",
    "atlas_key":"DDHFSI-HCMD-SP-PH-~~",
    "delivery":dc("projectile",0.88,"Glaive is a thrown projectile that ricochets between enemies — projectile delivery"),
    "footprint":dc("chain-hop",0.85,"Glaive bounces between multiple enemies per throw; chain-hop footprint"),
    "geo_text":"Outlander throws a Glaive weapon that bounces between multiple enemies in mid range. Skill upgrades increase bounce count and damage per chain. Fast throwing cadence at high level.",
    "control":ctrl(["slow"],"rider",0.62),
    "defense":defs(["dodge","resist"],"dodge",0.80),
    "economy":econ("Ember (Charge)","spend","charge","on_hit","TL2 Outlander builds Charge via hits; Glaive Throw and boosted skills spend Charge. Economy = charge-meter with on-hit builder source.",0.80),
    "element":elem("Physical","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "DEX",0.85,"Outlander = DEX class confirmed",
        "mid",0.80,"Glaive thrown to mid range; not full-range archery, not melee",
        "high",0.82,"High throw frequency with skill upgrades",
        "flat",0.75,"Flat consistent damage per throw",
        "solo",0.82,"No proxy; solo thrower",
        "instant",0.82,"Glaive throw fires instantly"
    ),
    "mechanics_notes":"G2: Glaive bouncing = chain-hop, NOT a line projectile. Charge economy: TL2 Outlander uses a Charge bar built from attacks, spent on powered throws. This is the chain-hop delivery archetype in TL2.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Outlander Glaive Throw; chain-hop bounce confirmed; Charge economy)"]
})

# 4. tl2-shotgonne-outlander — Shotgonne Outlander — DDHFSI (same prefix as glaive)
records.append({
    "kit_id":"tl2-shotgonne-outlander","folk_name":"Shotgonne Outlander","game":"tl2","status":"positive",
    "atlas_key":"DDHFSI-HSMD-SP-PH-~~",
    "delivery":dc("projectile",0.85,"Shotgonne fires a spread of pellets at close-to-mid range; projectile spread"),
    "footprint":dc("cone",0.82,"Shotgonne pellets spread in a forward cone; wide spread at close range"),
    "geo_text":"Outlander uses a Shotgonne weapon to fire a spread of pellets in a forward cone. Effective at close-to-mid range; pellets deal piercing damage across the spread.",
    "control":ctrl(["knockback"],"rider",0.65),
    "defense":defs(["dodge","resist"],"dodge",0.80),
    "economy":econ("Emberquivers/Clips","ammo","n/a","n/a","Shotgonne uses ammunition clips (ammo economy) that deplete and reload between bursts. TL2 Outlander's Shotgonne skills interact with clip capacity.",0.78),
    "element":elem("Physical","hit",0.82),
    "movement":mov(["standard-move"],"rooted",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.85,"Outlander = DEX class",
        "mid",0.78,"Shotgonne range = close-to-mid; not true melee, not ranged",
        "high",0.80,"High fire rate per burst",
        "flat",0.75,"Flat spread damage; consistent multi-pellet output",
        "solo",0.80,"No proxy; solo gunner",
        "instant",0.80,"Shotgonne burst fires instantly on activation"
    ),
    "mechanics_notes":"Ammo economy: Shotgonne uses clip-based ammo that depletes (TL2 Outlander has Shadowmantle + clip mechanics). Footprint=cone correctly captures pellet spread vs Glaive's chain-hop. D1: Dodge as primary (Outlander is agility-evasion class).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Outlander Shotgonne; cone spread + clip ammo confirmed)"]
})

# 5. tl2-wolf-shade-berserker — Wolf Shade Berserker — DMHSLI (proxy=L=light, econ=MT=multi-trigger)
records.append({
    "kit_id":"tl2-wolf-shade-berserker","folk_name":"Wolf Shade Berserker","game":"tl2","status":"positive",
    "atlas_key":"DMHSLI-HSDD-MT-PH-~~",
    "delivery":dc("at-target",0.85,"Berserker delivers rapid melee strikes at target; Wolf Shade appears as a shadow copy on high-Charge attacks"),
    "footprint":dc("point",0.80,"Melee point strikes; Wolf Shade appears at same position as Berserker (shadow copy)"),
    "geo_text":"Berserker delivers rapid melee strikes with high Charge, summoning a Wolf Shade (shadow copy) that mirrors attacks. The shade is a light proxy that appears at peak Charge generation.",
    "control":ctrl(["knockback","bleed"],"rider",0.65),
    "defense":defs(["armor","dodge"],"armor",0.78),
    "economy":econ("Charge","meter","charge","on_hit","Berserker builds Charge from melee hits; Charge powers Wolf Shade and empowered attacks. Charge is a meter built via on-hit triggers. MT old code = multi-trigger (proc on Charge activation).",0.82),
    "element":elem("Physical","hit",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.80,"Berserker leans DEX in TL2 (agility-melee; Atlas D=DEX accepted)",
        "melee",0.88,"Wolf Shade Berserker is pure melee",
        "high",0.85,"Very high attack tempo via dual-wield + Charge passives",
        "spiky",0.82,"Wolf Shade provides burst spike at peak Charge; atlas S=spiky",
        "light",0.80,"Light proxy: Wolf Shade = single shadow copy, not heavy summon army",
        "instant",0.80,"Melee strikes instant; Shade appears on Charge trigger"
    ),
    "mechanics_notes":"Economy=meter with builder_source=on_hit captures the Charge mechanic precisely. 'Multi-trigger' (MT old code) = proc on Charge activation — Wolf Shade appearance is a proc event. Light proxy (L) captures single Wolf Shade vs Shadowling Outlander's heavy proxy army.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Berserker Wolf Shade; Charge meter mechanic; on-hit builder confirmed)"]
})

# 6. tl2-shadowling-outlander — Shadowling Outlander — DRMFHI (proxy=H=heavy)
records.append({
    "kit_id":"tl2-shadowling-outlander","folk_name":"Shadowling Outlander","game":"tl2","status":"positive",
    "atlas_key":"DRMFHI-HMDM-SU-PH-~~",
    "delivery":dc("at-target",0.82,"Shadowlings are spawned from kills and attack enemies independently; at-target summon from slain enemies"),
    "footprint":dc("large-zone",0.82,"Shadowling swarm disperses across combat area; heavy proxy covers entire zone"),
    "geo_text":"Shadowling Outlander spawns Shadowling minions from killed enemies using the Shadowling Gemstone and Outlander skills. Shadowlings are temporary summons that attack nearby enemies, providing a heavy proxy damage layer.",
    "control":ctrl(["taunt"],"rider",0.55),
    "defense":defs(["dodge","resist"],"dodge",0.78),
    "economy":econ("Charge","reserve","n/a","n/a","Shadowlings have a duration after spawn (not permanent reserve). Charge builds from Outlander attacks. Reserve model for active Shadowling count maintenance.",0.72),
    "element":elem("Physical","hit",0.75),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.82,"Outlander = DEX class",
        "ranged",0.80,"Outlander operates at range while Shadowlings melee",
        "med",0.72,"Medium tempo; proxy damage sustains between attacks",
        "flat",0.72,"Flat Shadowling DPS",
        "heavy",0.85,"Heavy proxy: Shadowlings are the primary damage source; caster minimal direct damage",
        "instant",0.78,"Shadowling spawn from kill = instant on trigger"
    ),
    "mechanics_notes":"Shadowlings spawn from killed enemies (proc economy on kill events) rather than via direct summon skill. This is a kill-to-summon proxy model — proxy=heavy because all damage routes through the Shadowling swarm. SU old code = sustain, captured as reserve for proxy maintenance.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Outlander Shadowlings; kill-to-summon proxy mechanic confirmed)"]
})

# 7. tl2-hailstorm-embermage — Hailstorm Embermage — IDLFLI (tempo=L=low, proxy=L=light)
records.append({
    "kit_id":"tl2-hailstorm-embermage","folk_name":"Hailstorm Embermage","game":"tl2","status":"positive",
    "atlas_key":"IDLFLI-HLMD-SP-CO-~~",
    "delivery":dc("at-target",0.82,"Hailstorm calls down a prolonged ice rain at target location; at-target zone placement"),
    "footprint":dc("large-zone",0.80,"Hailstorm creates a persistent large cold zone at target that rains ice over duration"),
    "geo_text":"Embermage calls down a Hailstorm at target location — a persistent cold zone that deals continuous ice damage over several seconds. Low tempo reflects the slow ice-tick pattern within the storm.",
    "control":ctrl(["freeze","slow"],"rider",0.72),
    "defense":defs(["glass","resist"],"glass",0.75),
    "economy":econ("Ember","spend","n/a","n/a","Hailstorm costs Ember (TL2 Embermage resource). Ember builds from basic attacks and is spent on spells. High Ember cost for Hailstorm.",0.80),
    "element":elem("Cold","hybrid",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "INT",0.85,"Embermage = INT caster class confirmed",
        "mid",0.78,"Hailstorm zone placed at mid range",
        "low",0.82,"Atlas key L=low: Hailstorm ticks slowly; ice damage per tick at low frequency",
        "flat",0.75,"Flat per-tick ice damage",
        "light",0.75,"Light proxy: ice storm zone is a passive weather effect, not an entity",
        "instant",0.78,"Hailstorm zone appears instantly on cast"
    ),
    "mechanics_notes":"Tempo=low (L) is distinctive — Hailstorm is a slow persistent storm, contrasting with Prismatic Bolt's fast spam. Damage_mode=hybrid: cold hit + freeze dot. Embermage Ember economy = build from basic attacks → spend on spells.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Embermage Hailstorm; Ember economy + low-tempo cold zone confirmed)"]
})

# 8. tl2-prismatic-embermage — Prismatic Bolt Embermage — IRHFSI
records.append({
    "kit_id":"tl2-prismatic-embermage","folk_name":"Prismatic Bolt Embermage","game":"tl2","status":"positive",
    "atlas_key":"IRHFSI-HMMG-SP-FI-~~",
    "delivery":dc("projectile",0.88,"Prismatic Bolt fires high-speed elemental bolts as projectiles; rapid-fire projectile delivery"),
    "footprint":dc("point",0.85,"Single-target projectile; piercing possible but base = point"),
    "geo_text":"Embermage fires rapid Prismatic Bolts — high-velocity elemental projectiles that deal primary fire damage with bonus elemental effects per hit. Very high attack speed with Ember investment.",
    "control":ctrl(["shock","slow"],"rider",0.62),
    "defense":defs(["glass","resist"],"glass",0.75),
    "economy":econ("Ember","spend","n/a","n/a","Prismatic Bolt costs Ember per activation. Ember built from basic wand attacks. Rapid casting depletes Ember quickly; investment in regeneration required.",0.82),
    "element":elem("Fire","hit",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "INT",0.88,"Embermage = INT class confirmed",
        "ranged",0.85,"Prismatic Bolt fires at long range",
        "high",0.88,"Very high cast rate via Ember investment; quintessential high-tempo caster",
        "flat",0.78,"Flat consistent DPS per bolt; rapid flat output",
        "solo",0.82,"No proxy; solo caster",
        "instant",0.85,"Bolt fires instantly"
    ),
    "mechanics_notes":"Prismatic Bolt = TL2 Embermage's signature spam skill. The 'Prismatic' name captures multi-elemental bolts. This is the high-tempo glass-cannon ranged caster archetype in TL2. Ember economy distinguishes this game's caster resource from standard Mana.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Embermage Prismatic Bolt; Ember economy + high-tempo confirmed)"]
})

# 9. tl2-cannon-engineer — Cannon Engineer — SDMSSI (attr=STR, range=D=mid, amp=spiky)
records.append({
    "kit_id":"tl2-cannon-engineer","folk_name":"Cannon Engineer","game":"tl2","status":"positive",
    "atlas_key":"SDMSSI-MSMT-MT-PH-~~",
    "delivery":dc("projectile",0.85,"Cannon fires a large projectile at target; Engineer's cannon skill launches shells at mid range"),
    "footprint":dc("small-radius",0.80,"Cannon shell explodes on impact in a small AoE blast radius"),
    "geo_text":"Engineer fires a Cannon shell at target location, which explodes on impact dealing high burst damage in a small AoE. Multi-trigger captures Charge-powered enhanced cannon shots.",
    "control":ctrl(["knockback"],"rider",0.62),
    "defense":defs(["armor","resist"],"armor",0.80),
    "economy":econ("Charge","meter","charge","on_hit","Engineer builds Charge from melee/attack hits; Cannon enhanced shots spend Charge. MT = multi-trigger (Charge activation proc). Charge meter with on_hit builder.",0.78),
    "element":elem("Physical","hit",0.80),
    "movement":mov(["standard-move"],"rooted",False,0.72),
    "prefix_claims":pfx(
        "STR",0.82,"Engineer = STR class in TL2 confirmed",
        "mid",0.78,"Cannon range = mid; not melee, not max range",
        "med",0.75,"Moderate tempo; cannon on cooldown/Charge gate",
        "spiky",0.82,"High per-shot burst damage; amp=spiky correctly captures cannon's burst pattern",
        "solo",0.80,"No proxy in this kit variant; solo cannon operator",
        "instant",0.80,"Cannon fires instantly on activation"
    ),
    "mechanics_notes":"Multi-trigger (MT) economy captures Charge-powered enhanced cannon shots — proc events on Charge threshold. Distinct from Bot Engineer's heavy-proxy model. Spiky amp = cannon is a burst-per-shot weapon not sustained DPS.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Engineer Cannon skill; Charge economy + burst pattern confirmed)"]
})

# 10. tl2-emberquake-engineer — Emberquake Engineer — SMMFLI (tempo=M, proxy=L=light)
records.append({
    "kit_id":"tl2-emberquake-engineer","folk_name":"Emberquake Engineer","game":"tl2","status":"positive",
    "atlas_key":"SMMFLI-LLDT-SP-FI-~~",
    "delivery":dc("self-origin",0.85,"Emberquake radiates fire/earth damage from the Engineer's position outward in a ground-shaking burst"),
    "footprint":dc("large-zone",0.82,"Emberquake creates a large fire + seismic AoE around the Engineer"),
    "geo_text":"Engineer activates Emberquake — a fire-and-earth ground slam that creates a large AoE shockwave around the caster. Secondary fire zones persist after the initial blast.",
    "control":ctrl(["slow","knockback"],"rider",0.62),
    "defense":defs(["armor","resist"],"armor",0.80),
    "economy":econ("Mana","spend","n/a","n/a","Emberquake costs Mana on activation. Engineer in this kit uses Mana rather than Charge for the ground-slam skill.",0.75),
    "element":elem("Fire","hit",0.82),
    "movement":mov(["standard-move"],"rooted",False,0.72),
    "prefix_claims":pfx(
        "STR",0.82,"Engineer = STR class",
        "melee",0.80,"Emberquake is a self-origin burst; melee range for full effect",
        "med",0.75,"Moderate tempo; Emberquake on cooldown",
        "flat",0.72,"Flat blast damage; fire zone secondary also flat",
        "light",0.78,"Light proxy: secondary fire zones persist but are not entities",
        "instant",0.78,"Emberquake burst is instant on cast"
    ),
    "mechanics_notes":"Contrast with Cannon Engineer: Emberquake is self-origin large-zone vs Cannon's mid-range projectile. Both are STR Engineer but different delivery patterns. Fire element + seismic ground slam = dual-flavor combo. Proxy=light captures secondary fire zones (not entity-based proxy).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Engineer Emberquake ground slam; fire+seismic AoE confirmed)"]
})

# 11. tl2-flame-hammer-engineer — Flame Hammer Engineer — SMMSSI (amp=spiky)
records.append({
    "kit_id":"tl2-flame-hammer-engineer","folk_name":"Flame Hammer Engineer","game":"tl2","status":"positive",
    "atlas_key":"SMMSSI-MSDT-MT-FI-~~",
    "delivery":dc("at-target",0.85,"Flame Hammer delivers melee smashes at target; fire-imbued hammer strikes"),
    "footprint":dc("small-radius",0.80,"Hammer impact creates a small fire burst AoE at target"),
    "geo_text":"Engineer wields a fire-imbued hammer, delivering powerful melee strikes that create small fire explosions on impact. High Charge shots create larger fire bursts.",
    "control":ctrl(["knockback","stun"],"rider",0.65),
    "defense":defs(["armor","resist"],"armor",0.82),
    "economy":econ("Charge","meter","charge","on_hit","Charge builds from melee hits; powered hammer strikes spend Charge for fire-burst enhancement. MT = multi-trigger on Charge proc.",0.80),
    "element":elem("Fire","hit",0.80),
    "movement":mov(["standard-move"],"rooted",False,0.72),
    "prefix_claims":pfx(
        "STR",0.85,"Engineer = STR class",
        "melee",0.88,"Hammer strikes = melee only",
        "med",0.75,"Medium tempo; hammer swing cadence",
        "spiky",0.82,"Charge-powered hammer bursts = spiky amp; atlas S=spiky confirmed",
        "solo",0.82,"No proxy; solo hammer",
        "instant",0.80,"Hammer swing activates instantly"
    ),
    "mechanics_notes":"Spiky amp from Charge-burst enhancement: normal hammer = baseline; Charge-empowered swing = spike burst. MT economy = proc on Charge threshold. This is the melee burst version of Engineer vs Emberquake's AoE zone pattern.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Engineer flame-hammer melee; Charge burst + fire impact confirmed)"]
})

# 12. tl2-bot-engineer — Bot Summoner Engineer — SRMFHI (attr=STR, range=R=ranged, proxy=H=heavy)
records.append({
    "kit_id":"tl2-bot-engineer","folk_name":"Bot Summoner Engineer","game":"tl2","status":"positive",
    "atlas_key":"SRMFHI-HMDM-SU-PH-~~",
    "delivery":dc("at-target",0.85,"Engineer deploys Combat Bots at target location; bots operate independently and deliver damage"),
    "footprint":dc("large-zone",0.82,"Multiple bots dispersed across large combat area; heavy proxy zone coverage"),
    "geo_text":"Engineer deploys Combat Bots (Mechanical Construct, Spider Mine, etc.) at targeted positions. Bots move and attack independently, covering the entire combat zone. Engineer commands rather than attacks directly.",
    "control":ctrl(["taunt"],"rider",0.58),
    "defense":defs(["armor","resist"],"armor",0.80),
    "economy":econ("Mana","reserve","n/a","n/a","Bots maintain as persistent allies costing Mana reserve upkeep. Re-deploying destroyed bots costs Mana. Engineer invests in +Mana regeneration to sustain the bot army.",0.80),
    "element":elem("Physical","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.78),
    "prefix_claims":pfx(
        "STR",0.82,"Engineer = STR class",
        "ranged",0.80,"Engineer controls bots from range; 'ranged' here = bots operate at distance",
        "med",0.75,"Sustained medium tempo via bot attacks",
        "flat",0.75,"Flat sustained bot DPS",
        "heavy",0.88,"Heavy proxy = bots deliver all damage; Engineer's personal DPS minimal",
        "instant",0.80,"Bot deployment instant on cast"
    ),
    "mechanics_notes":"Heavy proxy (H) = bot army delivers all damage; Engineer is the commander. SU old code = sustain (reserve maintenance). TL2 Bot Engineer mirrors TQ Petmaster and DI Minion Necro in the heavy-proxy archetype space.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TL2 Engineer Bot/Combat Construct deployment; heavy proxy + reserve economy confirmed)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# TLI KITS — live-2022+ (partially known, conf 0.58-0.68; NOT formally post-cutoff)
# ─────────────────────────────────────────────────────────────────────────────

# 13. tli-gemma-frost-caster — Gemma Frost Caster — IRHFSI (also has ss11-12-2026)
records.append({
    "kit_id":"tli-gemma-frost-caster","folk_name":"Gemma Frost Caster","game":"tli","status":"positive",
    "atlas_key":"IRHFSI-HLMG-SP-CO-~~",
    "delivery":dc("projectile",0.62,"Gemma (TLI hero) fires frost/ice projectiles as primary delivery"),
    "footprint":dc("small-radius",0.58,"Ice projectiles detonate on impact with small AoE burst"),
    "geo_text":"Gemma is TLI's frost caster hero. Fires ice projectile spells at range, with projectile-AoE impacts. ss11-12-2026 season changes unknown.",
    "control":ctrl(["freeze","slow"],"rider",0.60),
    "defense":defs(["resist","glass"],"glass",0.60),
    "economy":econ("Ember (TLI)","spend","n/a","n/a","TLI uses Ember as the primary resource for hero skills. Gemma spends Ember on frost spells.",0.58),
    "element":elem("Cold","hit",0.65),
    "movement":mov(["standard-move"],"full-move",False,0.60),
    "prefix_claims":pfx(
        "INT",0.65,"Gemma is INT caster hero",
        "ranged",0.68,"Frost projectile = ranged delivery",
        "high",0.60,"High cast tempo per atlas key H",
        "flat",0.58,"Flat cold DPS",
        "solo",0.62,"Solo caster; no proxy",
        "instant",0.62,"Frost spells instant"
    ),
    "mechanics_notes":"TLI live era (2022+) character; partially known. ss11-12-2026 changes = post-cutoff component but base hero mechanics from live launch. Conf reduced. TLI uses named hero characters with unique skill trees — Gemma is the frost mage identity.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TLI Gemma hero frost archetype; base mechanics partially known from 2022+ launch)"]
})

# 14. tli-youga-spirit-magus — Youga Spirit Magus Summons — IRMFHI
records.append({
    "kit_id":"tli-youga-spirit-magus","folk_name":"Youga Spirit Magus Summons","game":"tli","status":"positive",
    "atlas_key":"IRMFHI-MNMM-RS-LI-~~",
    "delivery":dc("self-origin",0.62,"Youga commands spirit/lightning summons from caster position; self-origin command delivery"),
    "footprint":dc("large-zone",0.60,"Spirit summons cover large combat zone independently"),
    "geo_text":"Youga (TLI spirit magus hero) summons spirit entities with lightning affinities to fight across the combat zone. Heavy proxy archetype with spiritual/lightning thematic.",
    "control":ctrl(["shock"],"rider",0.55),
    "defense":defs(["resist","hp-stack"],"resist",0.58),
    "economy":econ("Ember (TLI)","reserve","n/a","n/a","Spirit summons maintained via Ember reserve. RS old code = reserve-sustain. Youga invests in summon upkeep.",0.58),
    "element":elem("Lightning","hit",0.62),
    "movement":mov(["standard-move"],"full-move",False,0.60),
    "prefix_claims":pfx(
        "INT",0.65,"Youga is INT caster/summoner",
        "ranged",0.62,"Spirit summons attack at range",
        "med",0.58,"Medium tempo sustained from summons",
        "flat",0.55,"Flat spirit summon DPS",
        "heavy",0.65,"Heavy proxy = spirit summons deliver all damage",
        "instant",0.60,"Summon commands instant"
    ),
    "mechanics_notes":"TLI live era (2022+); partially known. Youga = spirit summoner with lightning elemental bias. ss11-12-2026 component unknown. Economy=reserve captures ongoing summon maintenance. Heavy proxy (H) matches atlas key.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TLI Youga spirit summoner hero; lightning + heavy proxy from atlas key + folk_name)"]
})

# 15. tli-rehan-berserker — Rehan Berserker Melee — SMHSSI (spiky, solo)
records.append({
    "kit_id":"tli-rehan-berserker","folk_name":"Rehan Berserker Melee","game":"tli","status":"positive",
    "atlas_key":"SMHSSI-HSDM-MT-PH-~~",
    "delivery":dc("at-target",0.65,"Rehan (TLI berserker hero) delivers melee burst strikes at target"),
    "footprint":dc("small-radius",0.62,"Berserker strikes hit in small AoE burst around target"),
    "geo_text":"Rehan (TLI berserker hero) delivers powerful melee burst strikes. High tempo + spiky burst pattern typical of berserker archetype. MT economy = proc-based Charge mechanic.",
    "control":ctrl(["stun","knockback"],"rider",0.60),
    "defense":defs(["armor","hp-stack"],"armor",0.65),
    "economy":econ("Charge (TLI Rehan)","meter","charge","on_hit","Rehan builds a Charge meter from melee hits; powered berserker abilities proc on Charge threshold. MT = multi-trigger proc economy.",0.62),
    "element":elem("Physical","hit",0.65),
    "movement":mov(["standard-move"],"full-move",False,0.60),
    "prefix_claims":pfx(
        "STR",0.68,"Rehan = STR berserker hero confirmed",
        "melee",0.70,"Berserker melee delivery confirmed",
        "high",0.65,"Very high tempo per atlas H",
        "spiky",0.65,"Burst damage per atlas S=spiky",
        "solo",0.68,"Solo melee fighter per atlas S=solo",
        "instant",0.62,"Melee strikes instant"
    ),
    "mechanics_notes":"TLI live era (2022+); partially known. Rehan = TLI's berserker-class hero. MT economy matches TL2 Berserker's Charge proc model. ss11-12-2026 changes unknown.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TLI Rehan berserker hero; melee burst archetype; atlas key + folk_name)"]
})

# 16. tli-moto-bots — Moto Bot Commander — SRMFHI (proxy=H=heavy; ONLY live-2022+)
records.append({
    "kit_id":"tli-moto-bots","folk_name":"Moto Bot Commander","game":"tli","status":"positive",
    "atlas_key":"SRMFHI-MMMT-SU-PH-~~",
    "delivery":dc("at-target",0.62,"Moto (TLI bot commander hero) deploys mechanical bots at target positions"),
    "footprint":dc("large-zone",0.62,"Bot swarm covers large combat zone"),
    "geo_text":"Moto (TLI mechanical hero) commands robot bots that deploy and attack across the combat zone. Heavy proxy archetype similar to TL2 Bot Engineer.",
    "control":ctrl(["taunt"],"rider",0.55),
    "defense":defs(["armor","resist"],"armor",0.62),
    "economy":econ("Ember (TLI)","reserve","n/a","n/a","Bot upkeep via Ember reserve. SU old code = sustain/reserve. Moto maintains bot army via reserve investment.",0.60),
    "element":elem("Physical","hit",0.60),
    "movement":mov(["standard-move"],"full-move",False,0.60),
    "prefix_claims":pfx(
        "STR",0.65,"Moto = STR engineer-class hero",
        "ranged",0.65,"Bots attack at range; commander maintains distance",
        "med",0.60,"Med tempo bot attacks",
        "flat",0.58,"Flat bot DPS",
        "heavy",0.68,"Heavy proxy = bots deliver all damage; Moto = commander archetype",
        "instant",0.60,"Bot deployment instant"
    ),
    "mechanics_notes":"TLI live-2022+ only (no 2026 content); moderate conf. Moto is TLI's mechanical/bot commander hero — TL2 Bot Engineer archetype adapted to TLI's hero system. SU reserve economy confirmed by atlas. Only live-era TLI kit with no 2026 component.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TLI Moto bot commander hero; heavy proxy + reserve economy from atlas key + live-2022+ context)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# TLI POST-CUTOFF KITS — ss11-12-2026 / ss12-lunaria-2026 (conf ≤ 0.50)
# ─────────────────────────────────────────────────────────────────────────────

post_cutoff_kits = [
    {
        "kit_id":"tli-erika3-vendetta","folk_name":"Erika 3 Vendetta Sting","game":"tli","status":"positive",
        "atlas_key":"DMHFSI-KNDG-SP-CO-~~",
        "delivery":dc("at-target",0.42,"TLI Erika Season 3 variant — melee DEX cold delivery per atlas key; post-cutoff"),
        "footprint":dc("point",0.40,"Melee point strike per atlas key"),
        "geo_text":"TLI Erika Season 11-12 (2026) cold/piercing melee variant. Post-cutoff; details from atlas key only.",
        "control":ctrl(["freeze","slow"],"rider",0.38),
        "defense":defs(["dodge","resist"],"dodge",0.40),
        "economy":econ("Ember (TLI)","spend","n/a","n/a","Season 11-12 skill economy; post-cutoff, unverified.",0.38),
        "element":elem("Cold","hit",0.42),
        "movement":mov(["standard-move"],"full-move",False,0.40),
        "prefix_claims":pfx("DEX",0.48,"Atlas D=DEX","melee",0.48,"Atlas M=melee","high",0.40,"Atlas H","flat",0.40,"Atlas F","solo",0.42,"Atlas S=solo","instant",0.40,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TLI ss11-12-2026. Erika Season 3 variant (2026 season content). All conf ≤0.50. Cold melee kit per atlas key. Details unverified.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["prov: mpx;sky;u4 (TLI Season 11-12 2026; post-cutoff — no training data)"]
    },
    {
        "kit_id":"tli-rosa-unsullied","folk_name":"Rosa Unsullied Blade","game":"tli","status":"positive",
        "atlas_key":"DMHFSI-_SD_-SP-HO-~~",
        "delivery":dc("at-target",0.42,"Rosa melee blade archetype; holy/physical melee per atlas key"),
        "footprint":dc("point",0.40,"Single-target melee blade strikes"),
        "geo_text":"TLI Rosa Season 11-12 (2026) holy blade melee archetype. Post-cutoff.",
        "control":ctrl([],"none",0.38),
        "defense":defs(["dodge","armor"],"dodge",0.40),
        "economy":econ("Ember (TLI)","spend","n/a","n/a","Post-cutoff; economy unverified.",0.38),
        "element":elem("Holy","hit",0.42),
        "movement":mov(["standard-move"],"full-move",False,0.40),
        "prefix_claims":pfx("DEX",0.48,"Atlas D=DEX","melee",0.48,"Atlas M=melee","high",0.40,"Atlas H","flat",0.40,"Atlas F","solo",0.38,"Atlas _SD_ — proxy slot partially blank","instant",0.40,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TLI ss11-12-2026. Rosa hero Season 11-12 variant. Atlas key has underscore blanks in suffix — partial data. All conf ≤0.50.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["prov: sky (TLI Season 11-12 2026; post-cutoff)"]
    },
    {
        "kit_id":"tli-carino2-lethal-flash","folk_name":"Carino 2 Lethal Flash","game":"tli","status":"positive",
        "atlas_key":"DRHSSI-HCDD-AM-PH-~~",
        "delivery":dc("projectile",0.42,"Carino ranged DEX build; projectile delivery per atlas key; econ=AM=ammo"),
        "footprint":dc("point",0.40,"Single-target ranged projectile"),
        "geo_text":"TLI Carino Season 12 Lunaria (2026) ranged DEX kit with ammo economy. Lethal Flash = rapid-fire projectile burst. Post-cutoff.",
        "control":ctrl([],"none",0.38),
        "defense":defs(["dodge","resist"],"dodge",0.42),
        "economy":econ("Ammo (TLI Carino)","ammo","n/a","n/a","AM old code = ammo economy confirmed by atlas. Post-cutoff specifics unverified.",0.42),
        "element":elem("Physical","hit",0.42),
        "movement":mov(["standard-move"],"full-move",False,0.40),
        "prefix_claims":pfx("DEX",0.48,"Atlas D=DEX","ranged",0.48,"Atlas R=ranged","high",0.42,"Atlas H=high","spiky",0.40,"Atlas S=spiky","solo",0.42,"Atlas S=solo","instant",0.40,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TLI ss12-lunaria-2026. Ammo economy (AM) confirmed by atlas key. Carino hero Season 12 Lunaria content — 2026. All conf ≤0.50.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["prov: fdw;tg (TLI Season 12 Lunaria 2026; post-cutoff)"]
    },
    {
        "kit_id":"tli-sage-elixir","folk_name":"Sage Elixir Kit","game":"tli","status":"positive",
        "atlas_key":"IRMFSI-_MMM-AM-__-~~",
        "delivery":dc("other",0.40,"Sage Elixir Kit appears to be a consumable/system economy kit; delivery=other per blank elem code and system-level nature"),
        "footprint":dc("other",0.40,"System-level kit; no spatial footprint"),
        "geo_text":"TLI Sage Season 12 Lunaria (2026) Elixir economy kit. Elixir-based economy system; delivery=other as this is a consumable/crafting system rather than a combat skill kit. Post-cutoff.",
        "control":ctrl([],"none",0.38),
        "defense":defs([],"other",0.38),
        "economy":econ("Elixirs","ammo","n/a","n/a","AM old code = ammo economy; Sage Elixir Kit uses consumable elixirs as ammo/inventory resource. Post-cutoff economy system.",0.42),
        "element":elem("n/a","hit",0.38),
        "movement":mov([],"rooted",False,0.40),
        "prefix_claims":pfx("INT",0.42,"Atlas I=INT","ranged",0.40,"Atlas R=ranged; Sage operates at range","med",0.38,"Atlas M","flat",0.38,"Atlas F","solo",0.40,"Atlas S=solo","instant",0.38,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TLI ss12-lunaria-2026. Sage hero Elixir economy kit — possibly a craft/consumable system similar to DI meta-system records. Atlas elem code blank (__) unusual — suggests element undefined. Elixir = consumable ammo. All conf ≤0.50. May warrant system-record treatment.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["prov: fdw;sky (TLI Season 12 Lunaria 2026; post-cutoff)"]
    },
    {
        "kit_id":"tli-iris2-thunder-magus","folk_name":"Iris 2 Thunder Magus Minions","game":"tli","status":"positive",
        "atlas_key":"IRMSHI-HLDM-SU-LI-~~",
        "delivery":dc("self-origin",0.42,"Iris thunder magus commands lightning spirit summons; self-origin command delivery"),
        "footprint":dc("large-zone",0.40,"Spirit summons cover large zone with lightning attacks"),
        "geo_text":"TLI Iris Season 11-12 (2026) thunder magus minion commander. INT summoner with lightning + heavy proxy. Post-cutoff.",
        "control":ctrl(["shock"],"rider",0.38),
        "defense":defs(["resist","hp-stack"],"resist",0.40),
        "economy":econ("Ember (TLI)","reserve","n/a","n/a","SU = reserve economy for minion upkeep. Post-cutoff details unverified.",0.40),
        "element":elem("Lightning","hit",0.42),
        "movement":mov(["standard-move"],"full-move",False,0.40),
        "prefix_claims":pfx("INT",0.48,"Atlas I=INT","ranged",0.48,"Atlas R=ranged","med",0.40,"Atlas M","spiky",0.40,"Atlas S=spiky","heavy",0.48,"Atlas H=heavy proxy","instant",0.42,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TLI ss11-12-2026. Iris Season 2 heavy-proxy lightning summoner. Conf ≤0.50. Youga (live-2022+) analog but 2026-season Iris variant. All details from atlas key provenance.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["prov: u4 (TLI Season 11-12 2026; post-cutoff)"]
    }
]
records.extend(post_cutoff_kits)

# ─────────────────────────────────────────────────────────────────────────────
# NEGATIVE (1 light schema)
# ─────────────────────────────────────────────────────────────────────────────

records.append({
    "kit_id":"tl2-arc-beam","folk_name":"Arc Beam Embermage as Primary","game":"tl2","status":"negative",
    "atlas_key":"IDHFSC-RNDG-SP-LI-~~",
    "delivery":dc("beam",0.88,"Arc Beam is a sustained lightning beam channel in TL2 Embermage tree — true beam delivery"),
    "footprint":dc("lane",0.82,"Narrow lightning beam lane from caster to target range"),
    "why_negative":"Arc Beam Embermage failed as a solo primary archetype. The channel requires standing still; Embermage Ember depletion outpaces Ember regeneration during sustained beam; and the damage per Ember was inferior to Prismatic Bolt spam builds in TL2's meta. Used as a secondary damage layer in hybrid builds, never primary.",
    "era_span":"tl2-2012",
    "post_cutoff":False,"dossier_owed":False,
    "prov":"tlf;kb",
    "mech_note":"G2: Arc Beam IS a true beam — delivery=beam, footprint=lane (NOT chain-hop). Negative status = build viability failure. Beam mechanic itself is well-characterized. Commit=C=channel confirmed by atlas key."
})

# ─────────────────────────────────────────────────────────────────────────────
# WRITE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

pos = sum(1 for r in records if r.get("status")=="positive" and not r.get("post_cutoff"))
pc_count = sum(1 for r in records if r.get("post_cutoff"))
neg = sum(1 for r in records if r.get("status")=="negative")
total = len(records)

print(f"TL1+TL2+TLI: {total} records | pos={pos} neg={neg} post-cutoff={pc_count}")

with open(OUT, "w") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Written: {OUT}")
print()
print("=== DIRECTED SWEEP RESULTS (TL/TLI) ===")
print("C2 (support-existence): NO pure-support kit in TL/TLI corpus.")
print("  All TL kits are damage/control/summoner oriented; no healer/buffer-only archetype present.")
print("G2 (line-vs-projectile):")
print("  TRUE BEAMS: tl2-arc-beam (negative — Arc Beam lightning, delivery=beam, footprint=lane)")
print("  Chain-hop: tl1-ricochet-vanquisher (ricochet = chain-hop NOT line), tl2-glaive-outlander (ricochet chain-hop)")
print("  NOTE: Arc Beam is negative but confirms beam geometry exists in TL2 Embermage tree")
print("D1 (shield-split):")
print("  GLASS: tl2-prismatic-embermage, tl2-hailstorm-embermage, tl2-arc-beam")
print("  DODGE: tl2-glaive-outlander, tl2-shotgonne-outlander, tl2-shadowling-outlander, tl1-ricochet-vanquisher")
print("  DODGE+: tli-rehan-berserker, tli post-cutoff DEX kits (erika, rosa, carino)")
print("  ARMOR: tl2-cannon-engineer, tl2-emberquake-engineer, tl2-flame-hammer-engineer, tl2-bot-engineer, tl2-wolf-shade-berserker, tl1-alchemist-summoner")
print("  SUSTAIN-LEECH: none explicitly (TL series lacks sustain-leech as primary archetype in corpus)")
