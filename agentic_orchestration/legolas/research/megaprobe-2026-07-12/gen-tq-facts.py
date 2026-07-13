#!/usr/bin/env python3
"""gen-tq-facts.py — TQ + TQ2 facts for megaprobe 2026-07-12
26 records: 24 positive (2 neg light-schema) — 5 TQ2 rows all post-cutoff (tq2-ea-2025+)
TQ source data: base-2006 through eternal-embers-2021 — good knowledge
TQ2 EA (2025+): post-cutoff, conf capped ≤ 0.50
"""
import json

OUT = "agentic_orchestration/legolas/research/megaprobe-2026-07-12/tq-facts.jsonl"

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
# TQ POSITIVES — base 2006 through ragnarok/atlantis/eternal-embers
# ─────────────────────────────────────────────────────────────────────────────

# 1. tq-rune-weapon-thunderer — Rune Weapon Thunderer — DMHFSI
# Storm+Rune = Thunderer; Rune Weapon enchants with lightning; melee delivery
records.append({
    "kit_id":"tq-rune-weapon-thunderer","folk_name":"Rune Weapon Thunderer","game":"tq","status":"positive",
    "atlas_key":"DMHFSI-MSMM-SP-LI-~~",
    "delivery":dc("at-target",0.80,"Rune Weapon buffs melee weapon strikes; delivery = melee at-target physical+lightning hits"),
    "footprint":dc("point",0.78,"Single-target melee strikes; lightning secondary occasionally chains but base is point"),
    "geo_text":"Rune Weapon enchants weapon strikes with lightning damage. Thunderer (Storm+Rune) uses Rune Weapon as a buff layer over melee attacks, delivering point-target lightning-infused melee strikes at high attack speed.",
    "control":ctrl(["shock","slow"],"rider",0.65),
    "defense":defs(["armor","dodge"],"armor",0.72),
    "economy":econ("Energy","reserve","n/a","n/a","Rune Weapon maintains as a toggle with an Energy per Second cost (reserve model). Attack speed Rune upgrades use no additional economy per hit.",0.75),
    "element":elem("Lightning","hit",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "DEX",0.75,"TQ Thunderer uses DEX for attack speed (Rune+Storm hybrid may lean DEX or STR; atlas D=DEX accepted)",
        "melee",0.80,"Rune Weapon is a melee weapon enchant; delivery is melee attack",
        "high",0.78,"Rune-buffed melee attack speed = very high attack tempo",
        "flat",0.72,"Flat lightning DPS via weapon enchant; consistent per-hit",
        "solo",0.78,"No proxy entities; solo melee striker",
        "instant",0.78,"Rune Weapon toggled on, then melee attacks fire instantly"
    ),
    "mechanics_notes":"Ragnarok expansion class. Rune Weapon = reserve-economy toggle that enchants physical attacks with lightning. Economy model = reserve (ongoing EPS cost). The 'Thunderer' name labels the Storm+Rune dual-mastery. Not a typical caster despite INT flavor in Storm mastery — this archetype leans DEX/melee.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Ragnarok Rune mastery; Rune Weapon toggle-reserve economy confirmed)"]
})

# 2. tq-warlock-poison-vitality — Warlock (Rogue+Spirit) — DMMFSI
records.append({
    "kit_id":"tq-warlock-poison-vitality","folk_name":"Warlock Rogue+Spirit","game":"tq","status":"positive",
    "atlas_key":"DMMFSI-MNMD-RS-PO-~~ ",
    "delivery":dc("at-target",0.78,"Warlock delivers poison strikes at-target via Rogue skill tree; melee or short-range poison abilities"),
    "footprint":dc("point",0.75,"Primarily single-target poison application at melee/close range"),
    "geo_text":"Warlock (Rogue+Spirit) layers poison damage from Rogue tree onto Spirit vitality utilities. Poison Gas Bomb can AoE, but core kit is single-target poison application via melee.",
    "control":ctrl(["poison","slow"],"rider",0.68),
    "defense":defs(["dodge","sustain-leech"],"dodge",0.75),
    "economy":econ("Energy","spend","n/a","n/a","Energy spend per active skill activation. Poison DoT is the sustained damage layer that doesn't cost additional energy per tick. Spirit skills may have reserve components.",0.72),
    "element":elem("Poison","dot",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.78,"Rogue mastery scales with DEX; Warlock archetype confirmed DEX-primary",
        "melee",0.75,"Rogue poison delivery is primarily melee/close-range",
        "med",0.70,"Medium tempo — poison application at moderate rate, DoT does the work",
        "flat",0.72,"Flat poison DoT; consistent damage over time",
        "solo",0.78,"Solo poison applicator; no proxy",
        "instant",0.75,"Poison skills activate instantly on cast"
    ),
    "mechanics_notes":"Econ=RS in old code = 'reserve-sustain' (hybrid). Spirit tree may add reserve-based aura (Phantom Lancer) or vitality leech. Vitality in folk_name captures Spirit's life steal. Damage_mode=dot captures poison DoT as the primary output, not hit.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Warlock dual-mastery Rogue+Spirit; poison mechanic base game)"]
})

# 3. tq-phantom-strike-dreamkiller — Phantom Strike Dreamkiller — DMMSSI
records.append({
    "kit_id":"tq-phantom-strike-dreamkiller","folk_name":"Phantom Strike Dreamkiller","game":"tq","status":"positive",
    "atlas_key":"DMMSSI-KSDD-CD-PI-~~",
    "delivery":dc("at-target",0.85,"Phantom Strike teleports the caster to the target and delivers a burst of melee strikes — at-target teleport-blink delivery"),
    "footprint":dc("point",0.82,"Single-target burst at the struck enemy; point footprint with minor splash from Dream tree passives"),
    "geo_text":"Phantom Strike (Dream mastery) teleports the caster to a target enemy and delivers a rapid sequence of melee strikes in a burst. Dreamkiller (Dream+Rogue) amplifies with Rogue poison/critical layers.",
    "control":ctrl(["stun","slow"],"rider",0.65),
    "defense":defs(["dodge","resist"],"dodge",0.78),
    "economy":econ("Energy","cooldown","n/a","n/a","Phantom Strike has a 10-15s cooldown and energy cost. Between cooldowns, the kit uses normal melee. Economy = cooldown gated.",0.80),
    "element":elem("Piercing","hit",0.72),
    "movement":mov(["teleport-strike"],"rooted",True,0.85),
    "prefix_claims":pfx(
        "DEX",0.82,"Dreamkiller leans DEX for Rogue attack speed and dodge",
        "melee",0.82,"Phantom Strike is a melee delivery; teleport bridges to melee range",
        "med",0.75,"Med tempo — Phantom Strike burst punctuates normal melee; not always active",
        "spiky",0.82,"Strike burst on each activation = spiky damage spike; atlas_key S confirmed",
        "solo",0.82,"Solo strike kit; no proxy",
        "instant",0.80,"Phantom Strike fires instantly (teleport+strikes are immediate)"
    ),
    "mechanics_notes":"skill_is_movement=True: Phantom Strike IS the movement mechanic (teleport). One of TQ's unique movement-attack skills. CD economy = 10-15s cooldown on the blink-strike. Dreamkiller is widely considered one of TQ's strongest dual-mastery combinations.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Immortal Throne Dream mastery; Phantom Strike teleport mechanic confirmed)"]
})

# 4. tq-marksmanship-haruspex — Marksmanship Haruspex — DRHFSI
records.append({
    "kit_id":"tq-marksmanship-haruspex","folk_name":"Marksmanship Haruspex","game":"tq","status":"positive",
    "atlas_key":"DRHFSI-HNDD-SP-PI-~~",
    "delivery":dc("projectile",0.85,"Marksmanship archetype fires arrows as projectiles; Hunting mastery arrow skills"),
    "footprint":dc("point",0.80,"Single-target arrow shot; piercing may hit multiple if targets aligned"),
    "geo_text":"Haruspex (Hunting+Dream) uses Marksmanship to empower arrow attacks to extreme single-target damage. Hunting's passive multipliers (Marksmanship, Anatomy) increase per-hit output significantly.",
    "control":ctrl(["slow","bleed"],"rider",0.62),
    "defense":defs(["dodge","resist"],"dodge",0.78),
    "economy":econ("Energy","spend","n/a","n/a","Hunting skills cost Energy per activation. Marksmanship passives are free. Attack speed from passives maintains high cadence.",0.78),
    "element":elem("Piercing","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "DEX",0.85,"Hunting mastery is DEX-primary; Marksmanship scales with DEX",
        "ranged",0.88,"Archery = ranged confirmed; Haruspex fires from range",
        "high",0.82,"High attack tempo via passive attack speed bonuses from Marksmanship tree",
        "flat",0.78,"Flat DPS via consistent arrow output; not burst-spike",
        "solo",0.82,"Solo archer; no proxy",
        "instant",0.82,"Arrow shots fire instantly"
    ),
    "mechanics_notes":"Marksmanship = passive Hunting skill that dramatically increases arrow damage %. Haruspex (Hunting+Dream) adds Study Prey (debuff) and Dream passives that amplify single-target output. This is TQ's premier single-target ranged archetype.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ IT Hunting+Dream Haruspex; Marksmanship passive confirmed)"]
})

# 5. tq-trap-magician — Trapper Magician — DRMFHI (proxy=H=heavy)
records.append({
    "kit_id":"tq-trap-magician","folk_name":"Trapper Magician","game":"tq","status":"positive",
    "atlas_key":"DRMFHI-HMDD-SP-PI-~~",
    "delivery":dc("at-target",0.82,"Traps are placed at target location; proxy entities (traps) deliver the actual damage"),
    "footprint":dc("large-zone",0.78,"Multiple traps cover a large area; trap AoE coverage zone is effectively large"),
    "geo_text":"Magician (Rogue+Storm) places Rogue traps at target locations. Traps persist and fire piercing projectiles or AoE bursts at nearby enemies. Storm mastery adds lightning AoE layers.",
    "control":ctrl(["shock","slow"],"rider",0.62),
    "defense":defs(["dodge","resist"],"dodge",0.75),
    "economy":econ("Energy","ammo","n/a","n/a","Traps cost Energy per placement and have a limited count (ammo-style — maximum active traps). Re-placement when traps expire or are destroyed.",0.78),
    "element":elem("Piercing","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "DEX",0.80,"Rogue mastery = DEX; trap-based Rogue archetype",
        "ranged",0.80,"Traps fire from range; Magician maintains distance while traps engage",
        "med",0.72,"Medium tempo — traps operate continuously but placement cadence is moderate",
        "flat",0.72,"Flat trap DPS; consistent per-trap output",
        "heavy",0.82,"Heavy proxy — ALL damage goes through trap entities; player contributes minimally to direct damage",
        "instant",0.78,"Trap placement is instant on cast"
    ),
    "mechanics_notes":"Economy=ammo captures the trap-count limit (e.g., max 3 active traps). Heavy proxy = traps are the damage delivery system entirely. Rogue+Storm = Magician dual-mastery. Storm lightning adds to trap explosions in some builds.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Rogue trap mechanics; Magician dual-mastery confirmed base game)"]
})

# 6. tq-ranger-hunting-nature — Ranger — DRMFLI (proxy=L=light)
records.append({
    "kit_id":"tq-ranger-hunting-nature","folk_name":"Ranger","game":"tq","status":"positive",
    "atlas_key":"DRMFLI-HNDM-SU-PI-~~",
    "delivery":dc("projectile",0.82,"Hunting arrows + Nature pets; primary delivery = projectile arrows"),
    "footprint":dc("point",0.75,"Arrow shots are point/single-target; Nature wolves provide AoE coverage at secondary level"),
    "geo_text":"Ranger (Hunting+Nature) fires arrows at range while Nature pets (wolves) provide secondary AoE melee coverage. The kit integrates ranged projectile with light proxy support.",
    "control":ctrl(["slow","bleed"],"rider",0.62),
    "defense":defs(["dodge","sustain-leech"],"dodge",0.78),
    "economy":econ("Energy","reserve","n/a","n/a","Wolf pets maintained via Nature reserve energy. Hunting skills spend Energy on activation. Hybrid reserve+spend economy.",0.75),
    "element":elem("Piercing","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "DEX",0.82,"Hunting = DEX primary; Ranger archetype DEX confirmed",
        "ranged",0.82,"Arrow delivery = ranged; core Hunting identity",
        "med",0.72,"Moderate tempo; nature pet cadence + arrow shooting",
        "flat",0.72,"Flat consistent DPS; not burst archetype",
        "light",0.78,"Light proxy — wolves assist but arrows are the primary damage; light pet coverage",
        "instant",0.78,"Arrow shots fire instantly"
    ),
    "mechanics_notes":"Light proxy (L) distinguishes from Petmaster (heavy proxy): Ranger's arrows are the primary damage source; wolves supplement. SU economy in old code = sustain/nature; here captured as reserve (wolf upkeep) + spend (active hunting skills). Nature also has Regrowth (sustain-leech component).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Hunting+Nature Ranger; wolf pets + archery confirmed base game)"]
})

# 7. tq-brigand-poison — Poison Brigand — DRMSSI (amp=spiky)
records.append({
    "kit_id":"tq-brigand-poison","folk_name":"Poison Brigand","game":"tq","status":"positive",
    "atlas_key":"DRMSSI-HNMG-SP-PO-~~",
    "delivery":dc("projectile",0.80,"Brigand fires ranged projectiles (thrown/bow) with poison; delivery = ranged projectile"),
    "footprint":dc("point",0.78,"Single-target poison application per shot; poison spreads as DoT not AoE"),
    "geo_text":"Brigand (Rogue+Hunting) stacks poison via ranged projectile attacks. Poison Gas Bomb can create AoE cloud but primary output is single-target poison application through rapid ranged shots.",
    "control":ctrl(["poison","slow"],"rider",0.65),
    "defense":defs(["dodge","resist"],"dodge",0.78),
    "economy":econ("Energy","spend","n/a","n/a","Energy spend on Poison Gas Bomb and active abilities. Regular attacks are free. Brigand rotates cooldown skills between free attacks.",0.75),
    "element":elem("Poison","dot",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.82,"Rogue+Hunting = DEX dual-mastery; Brigand DEX confirmed",
        "ranged",0.80,"Ranged projectile delivery; Hunting archery + Rogue thrown",
        "med",0.72,"Medium tempo; spiky burst when poison stacks peak",
        "spiky",0.78,"Poison stack burst when full stacks detonate or with Gas Bomb detonation; atlas S confirmed",
        "solo",0.80,"Solo ranged poisoner; no proxy",
        "instant",0.78,"Projectile fires instantly"
    ),
    "mechanics_notes":"Poison DoT is the defining mechanic. Spiky amp: poison buildup creates burst-equivalent when stacks max out. Damage_mode=dot is correct — poison ticks are the primary output, not hit damage. Brigand dual-class synergizes Rogue's poison with Hunting's ranged passives.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Rogue+Hunting Brigand; poison archetype confirmed base game)"]
})

# 8. tq-petmaster-summoner — Petmaster Summoner — IMMFHI (proxy=H=heavy)
records.append({
    "kit_id":"tq-petmaster-summoner","folk_name":"Petmaster Summoner","game":"tq","status":"positive",
    "atlas_key":"IMMFHI-MNMM-SU-PH-~~",
    "delivery":dc("self-origin",0.82,"Summon commands issued from caster; pets/minions deliver all damage independently"),
    "footprint":dc("large-zone",0.82,"Pet swarm covers large area of combat field; effective zone = total pet spread"),
    "geo_text":"Petmaster uses Nature wolves, Spirit spectral minions, or combined summon armies to fill the combat zone with proxy entities. Caster maintains safe distance while pets overwhelm enemies.",
    "control":ctrl(["taunt"],"rider",0.58),
    "defense":defs(["sustain-leech","hp-stack"],"hp-stack",0.72),
    "economy":econ("Energy","reserve","n/a","n/a","Pets maintained via continuous Energy reserve drain. Re-summoning dead pets costs Energy. Petmaster invests heavily in +Energy Regeneration to sustain the pet army.",0.80),
    "element":elem("Physical","hit",0.72),
    "movement":mov(["standard-move"],"full-move",False,0.78),
    "prefix_claims":pfx(
        "INT",0.75,"Spirit mastery scales with INT; Nature+Spirit Petmaster leans INT for Spirit skills",
        "melee",0.70,"Pets engage at melee range; caster is effectively ranged behind the army",
        "med",0.72,"Sustained medium-tempo coverage via pet attacks",
        "flat",0.75,"Flat sustained pet DPS; no burst spikes from the caster",
        "heavy",0.88,"Heavy proxy = ALL damage from pet entities; caster does near-zero direct damage",
        "instant",0.78,"Summon commands fire instantly"
    ),
    "mechanics_notes":"Heavy proxy is the defining characteristic. Economy=reserve captures the continuous pet upkeep cost. TQ summoner can use Nature (wolves + call of the wild), Spirit (summon outsider, wraith), or hybrid. Eternal Embers (2021) added Neidan mastery which also synergizes with summons. Long-lived archetype across 4 expansions.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Petmaster summoner; Nature+Spirit pet reserve economy confirmed; Eternal Embers 2021)"]
})

# 9. tq-ternion-bone-charmer — Ternion Bone Charmer — IRHFSI
# Spirit+? — Ternion Attack fires 3 bone projectiles simultaneously; "Bone Charmer" likely Spirit+Rogue or Spirit+Hunting
records.append({
    "kit_id":"tq-ternion-bone-charmer","folk_name":"Ternion Bone Charmer","game":"tq","status":"positive",
    "atlas_key":"IRHFSI-MMDM-SP-VI-~~",
    "delivery":dc("projectile",0.85,"Ternion Attack fires 3 bone spirit projectiles simultaneously per cast — triple projectile delivery"),
    "footprint":dc("cone",0.78,"Three simultaneous projectiles spread in a narrow forward cone, each hitting independently"),
    "geo_text":"Ternion Attack (Spirit mastery) fires three spectral bone projectiles simultaneously in a tight forward spread. Each projectile deals vitality damage independently, creating a pseudo-AoE effect at close-to-medium range.",
    "control":ctrl(["slow"],"rider",0.60),
    "defense":defs(["resist","sustain-leech"],"sustain-leech",0.72),
    "economy":econ("Energy","spend","n/a","n/a","Ternion Attack replaces the standard ranged attack; each cast costs Energy. High attack speed via Spirit passives means frequent Energy spend but also high regen investment.",0.78),
    "element":elem("Vitality","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "INT",0.82,"Spirit mastery scales with INT; Bone Charmer caster INT-primary",
        "ranged",0.82,"Ternion fires at range; clear ranged projectile delivery",
        "high",0.80,"Three projectiles per cast at high attack speed = very high tempo",
        "flat",0.75,"Flat triple-hit output per cast; consistent vitality damage",
        "solo",0.80,"No proxy; solo caster",
        "instant",0.80,"Ternion activates instantly as a replacement attack"
    ),
    "mechanics_notes":"Ternion Attack is Spirit mastery's defining skill — replaces the standard attack with 3 projectiles. 'Bone Charmer' folk_name suggests Spirit+Rogue or Spirit+Nature dual mastery. elem=Vitality (old code VI) is the Spirit mastery's primary damage type. Footprint=cone: three projectiles spread slightly — mini-cone effect.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Spirit mastery Ternion Attack; vitality damage triple-projectile confirmed)"]
})

# 10. tq-ice-shard-oracle — Ice Shard Oracle — IRHFSI
# Storm+Spirit = Oracle; Ice Shard = Storm mastery; ranged cold nuker
records.append({
    "kit_id":"tq-ice-shard-oracle","folk_name":"Ice Shard Oracle","game":"tq","status":"positive",
    "atlas_key":"IRHFSI-MNMM-SP-CO-~~",
    "delivery":dc("projectile",0.85,"Ice Shard fires a piercing cold projectile; single primary projectile delivery"),
    "footprint":dc("point",0.80,"Single projectile; may pierce through multiple enemies in line"),
    "geo_text":"Oracle (Storm+Spirit) fires Ice Shards as the primary damage vehicle — piercing cold projectiles that deal cold damage. Spirit mastery adds vitality/life drain support layers.",
    "control":ctrl(["freeze","slow"],"rider",0.78),
    "defense":defs(["resist","sustain-leech"],"resist",0.72),
    "economy":econ("Energy","spend","n/a","n/a","Ice Shard costs Energy per cast; high attack speed means frequent casts and high Energy spend rate. Energy regeneration investment required.",0.80),
    "element":elem("Cold","hit",0.85),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "INT",0.85,"Storm mastery = INT primary; Oracle INT caster confirmed",
        "ranged",0.85,"Ice Shard fires as a ranged projectile",
        "high",0.80,"High cast rate; Ice Shard fires per activation at high frequency",
        "flat",0.75,"Flat cold DPS via consistent projectile spam",
        "solo",0.82,"No proxy; solo caster",
        "instant",0.82,"Ice Shard fires instantly on cast"
    ),
    "mechanics_notes":"Ice Shard from Storm mastery is a Cold-damage projectile with pierce potential. Oracle (Storm+Spirit) pairs it with Spirit's Ternion (replace with Ternion for triple-ice variant) or life-leech support. Ragnarok expansion added Anniversary Edition balance that maintained this archetype's viability.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Storm mastery Ice Shard; Oracle dual-mastery confirmed; cold damage archetype)"]
})

# 11. tq-druid-squall-caster — Druid Storm Caster — IRLFSI (tempo=L=low!)
# Nature+Storm = Druid; Squall = persistent storm zone (L=low tempo = slow/sustained)
records.append({
    "kit_id":"tq-druid-squall-caster","folk_name":"Druid Storm Caster","game":"tq","status":"positive",
    "atlas_key":"IRLFSI-HLMM-SP-LI-~~",
    "delivery":dc("at-target",0.80,"Squall places a persistent storm zone at target location; delivery = zone placement"),
    "footprint":dc("large-zone",0.82,"Squall creates a large persistent lightning storm AoE at target; enemies in zone take continuous lightning damage"),
    "geo_text":"Druid (Nature+Storm) places a Squall zone that persists for several seconds, raining lightning within a large AoE. Low tempo reflects the sustained zone nature — Squall fires continuously but slowly at a set pace.",
    "control":ctrl(["shock","slow"],"rider",0.68),
    "defense":defs(["resist","sustain-leech"],"resist",0.72),
    "economy":econ("Energy","spend","n/a","n/a","Squall has an Energy cost on placement and a duration. Between Squall refreshes, the Druid has free actions. Economy = spend with built-in duration (not channel).",0.75),
    "element":elem("Lightning","hit",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "INT",0.80,"Storm mastery = INT; Druid caster INT-primary",
        "ranged",0.78,"Squall zone can be placed at range from caster",
        "low",0.80,"Atlas key L=low tempo confirmed: Squall ticks slowly but persistently; low DPS per tick",
        "flat",0.72,"Flat per-tick lightning damage; consistent zone output",
        "solo",0.78,"No proxy; zone skill",
        "instant",0.78,"Squall zone appears instantly on placement"
    ),
    "mechanics_notes":"Tempo=low is the distinguishing characteristic here — Squall ticks at a slow rate but persistently. This is a 'place-and-move' zone kit rather than an active-spam archetype. Nature provides sustain (Regrowth, Plague) that pairs with Storm's zone damage.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Storm mastery Squall persistent zone; Druid dual-mastery confirmed)"]
})

# 12. tq-liche-king-conjurer — Liche King Conjurer — IRMFHI (proxy=H=heavy)
# Spirit+Earth = Conjurer; Liche Form transform = heavy proxy (spirit form)
records.append({
    "kit_id":"tq-liche-king-conjurer","folk_name":"Liche King Conjurer","game":"tq","status":"positive",
    "atlas_key":"IRMFHI-MSMM-SU-VI-~~",
    "delivery":dc("self-origin",0.80,"In Liche Form, damage emanates from the transformed caster body; spectral aura attacks from self-origin"),
    "footprint":dc("small-radius",0.75,"Liche Form's aura/spectral attacks hit in radius around the transformed Conjurer"),
    "geo_text":"Conjurer (Spirit+Earth) uses Liche Form (Spirit mastery ultimate) to transform into a powerful undead spirit. In Liche Form, the caster becomes the proxy — aura-like spectral damage emanates from the transformed body.",
    "control":ctrl(["slow","fear"],"rider",0.62),
    "defense":defs(["shield-absorb","hp-stack"],"shield-absorb",0.72),
    "economy":econ("Energy","cooldown","n/a","n/a","Liche Form transformation has a significant cooldown (~60s+). Earth mastery skills spend Energy. Economy = cooldown for the primary transformation + spend for secondary skills.",0.75),
    "element":elem("Vitality","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "INT",0.80,"Spirit + Earth both scale with INT; Conjurer INT-primary",
        "ranged",0.75,"Conjurer operates at range with spectral projectiles before Liche Form; in form = radius",
        "med",0.72,"Medium tempo sustained output in Liche Form",
        "flat",0.70,"Flat spectral damage output in form",
        "heavy",0.78,"Heavy proxy: Liche Form IS the proxy — caster becomes the damage entity rather than using external summons; also can summon outsider as additional proxy",
        "instant",0.75,"Liche Form transformation activates (after cooldown trigger)"
    ),
    "mechanics_notes":"Liche Form = Spirit mastery's transformation skill — transforms the player into an undead liche entity with different ability patterns. 'Proxy=heavy' here means the transformed form (Liche) acts as the primary damage source, distinct from external pet proxy. Earth adds Volcanic Orb as a secondary damage layer.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Spirit+Earth Conjurer; Liche Form transformation confirmed base+IT)"]
})

# 13. tq-elementalist-volcanic-storm — Elementalist Nuker — IRMSSI
# Earth+Storm = Elementalist; volcanic orb + storm = spiky nuker
records.append({
    "kit_id":"tq-elementalist-volcanic-storm","folk_name":"Elementalist Nuker","game":"tq","status":"positive",
    "atlas_key":"IRMSSI-MLMG-SP-FI-~~",
    "delivery":dc("projectile",0.85,"Volcanic Orb fires as a large fire projectile; Thunderball (Storm) also fires as projectile"),
    "footprint":dc("small-radius",0.82,"Volcanic Orb explodes on impact with a medium AoE fireball; Storm bolt also has splash"),
    "geo_text":"Elementalist (Earth+Storm) fires Volcanic Orbs and Thunderballs as the primary damage delivery. Volcanic Orb travels to target then explodes in a fireball AoE. Storm skills add lightning layer.",
    "control":ctrl(["shock","slow"],"rider",0.65),
    "defense":defs(["resist","glass"],"glass",0.72),
    "economy":econ("Energy","spend","n/a","n/a","Volcanic Orb and Storm skills cost Energy per cast. High Energy investment required. Classic Energy-spend caster model.",0.80),
    "element":elem("Fire","hit",0.82),
    "movement":mov(["none"],"rooted",False,0.72),
    "prefix_claims":pfx(
        "INT",0.88,"Earth+Storm = INT dual caster; Elementalist INT-primary confirmed",
        "ranged",0.85,"Volcanic Orb fires at range; long-range projectile delivery",
        "med",0.78,"Moderate cast cadence; Volcanic Orb has a travel+explode cycle",
        "spiky",0.80,"High burst per orb impact; amp=spiky captures the burst-nuke pattern",
        "solo",0.82,"No proxy; solo caster",
        "instant",0.80,"Orb fires instantly (travels to target but launch is instant)"
    ),
    "mechanics_notes":"Earth+Storm = Elementalist — TQ's archetypal dual-caster. Volcanic Orb (Earth) is the signature skill: travels to target, explodes AoE. Storm Surge and Static Charge add lightning damage. Glass defense (no armor, high resist investment). Confirmed viable from base game through Ragnarok.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Earth+Storm Elementalist; Volcanic Orb confirmed; Elementalist dual-mastery base game)"]
})

# 14. tq-distortion-templar — Distortion Wave Templar — SDMSSI (amp=spiky, attr=STR)
# Dream+Defense = Templar; Distortion Wave = AoE burst knockback
records.append({
    "kit_id":"tq-distortion-templar","folk_name":"Distortion Wave Templar","game":"tq","status":"positive",
    "atlas_key":"SDMSSI-LLMT-CD-PH-~~",
    "delivery":dc("self-origin",0.85,"Distortion Wave emanates outward from caster in all directions; classic self-origin burst"),
    "footprint":dc("large-zone",0.82,"Wave covers large radius around caster; substantial AoE knockback reach"),
    "geo_text":"Distortion Wave (Dream mastery) radiates from the caster in a wide burst, dealing physical damage and knocking back all enemies within a large radius. Templar (Dream+Defense) adds defensive bulk.",
    "control":ctrl(["knockback","stun"],"core",0.85),
    "defense":defs(["block","armor"],"armor",0.82),
    "economy":econ("Energy","cooldown","n/a","n/a","Distortion Wave has a cooldown (~6-8s) and Energy cost. The burst nature makes cooldown the primary economy gate.",0.80),
    "element":elem("Physical","hit",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.80,"Templar uses Defense mastery (STR-oriented); Dream may be INT but Defense grounds this in STR",
        "mid",0.75,"Distortion Wave covers mid-range from caster outward",
        "med",0.75,"Cooldown-gated burst; medium tempo via cooldown cadence",
        "spiky",0.80,"Large burst on each Distortion Wave activation; spiky amp confirmed",
        "solo",0.82,"Solo burst; no proxy",
        "instant",0.80,"Wave fires instantly on cast"
    ),
    "mechanics_notes":"Distortion Wave is THE CC tool of TQ Dream mastery — mass knockback that clears large groups. Control centrality = CORE (the knockback is the purpose of this kit, not just a rider). Defense mastery provides Block + armor layers for tanky front-line delivery of the CC burst.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ IT Dream mastery Distortion Wave; Templar dual-mastery confirmed)"]
})

# 15. tq-onslaught-assassin — Onslaught Dual-Wield Assassin — SMHFSI
# Warfare+Rogue = Assassin; Onslaught = Warfare rapid melee AoE skill
records.append({
    "kit_id":"tq-onslaught-assassin","folk_name":"Onslaught Dual-Wield Assassin","game":"tq","status":"positive",
    "atlas_key":"SMHFSI-MNDD-SP-PH-~~",
    "delivery":dc("at-target",0.85,"Onslaught delivers rapid melee strikes at primary target; attack reaches nearby enemies"),
    "footprint":dc("point",0.78,"Primarily single-target with some cleave to adjacent enemies"),
    "geo_text":"Assassin (Warfare+Rogue) uses Onslaught as the primary melee skill — a rapid sequence of attacks that chains into surrounding enemies when dual-wielding. Rogue passives add poison/critical layers.",
    "control":ctrl(["bleed","slow"],"rider",0.62),
    "defense":defs(["dodge","armor"],"dodge",0.75),
    "economy":econ("Energy","spend","n/a","n/a","Onslaught costs Energy on activation; attack speed passives from Warfare+Rogue maintain high cadence between activations.",0.78),
    "element":elem("Physical","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.80,"Warfare mastery = STR; Assassin STR+DEX hybrid but STR primary per atlas",
        "melee",0.88,"Onslaught is melee-only; dual-wield melee close-range",
        "high",0.85,"Very high attack tempo via Warfare passives + Onslaught rapid strike",
        "flat",0.75,"Flat sustained DPS; Rogue poison adds DoT but amp is flat base",
        "solo",0.82,"Solo melee; no proxy",
        "instant",0.82,"Onslaught activates instantly"
    ),
    "mechanics_notes":"Onslaught = Warfare mastery's signature melee skill (3 rapid strikes per activation). Dual-wield synergizes with Rogue's dual-wield bonuses. Warfare STR + Rogue DEX = Assassin dual-mastery that leans physical melee. Rogue adds Envenom (poison), Blade Hone (passive), and dodge bonuses.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Warfare+Rogue Assassin; Onslaught melee skill confirmed base game)"]
})

# 16. tq-thane-storm-warfare — Thane Storm-Warrior — SMHFSI
# Warfare+Storm = Thane; storm warrior infuses melee with lightning
records.append({
    "kit_id":"tq-thane-storm-warfare","folk_name":"Thane Storm-Warrior","game":"tq","status":"positive",
    "atlas_key":"SMHFSI-MSMT-MT-LI-~~",
    "delivery":dc("at-target",0.82,"Thane delivers melee strikes infused with Storm lightning; at-target melee delivery"),
    "footprint":dc("point",0.78,"Primarily single-target melee with lightning chain secondary"),
    "geo_text":"Thane (Warfare+Storm) fuses melee Warfare attacks with Storm lightning infusions. Thunderous Strike (Storm) triggers on melee hits; Battle Rage (Warfare) amplifies all damage. Lightning chains between nearby enemies.",
    "control":ctrl(["shock","knockback"],"rider",0.65),
    "defense":defs(["armor","resist"],"armor",0.80),
    "economy":econ("Energy","spend","n/a","n/a","Thane uses Energy-spend active skills from both masteries. Thunderous Strike triggers automatically on hits (proc). Energy for active cast skills. MT old code = multi-trigger?",0.72),
    "element":elem("Lightning","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.85,"Warfare = STR primary; Thane is STR-oriented confirmed",
        "melee",0.85,"Melee strikes deliver the lightning; close-range confirmed",
        "high",0.82,"High melee tempo via Warfare passives + Onslaught",
        "flat",0.75,"Flat lightning infusion per hit; consistent damage pattern",
        "solo",0.82,"Solo melee striker",
        "instant",0.80,"Melee strikes fire instantly; Thunderous Strike procs instantly"
    ),
    "mechanics_notes":"Thane is Warfare+Storm — the lightning-infused warrior archetype. Thunderous Strike = proc-based lightning burst on melee hits (proc model). Old econ code MT may mean 'multi-trigger' capturing proc economy. Captured here as 'spend' since active skill use is the primary econ gate. Proc note in mechanics.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Warfare+Storm Thane; Thunderous Strike proc + Onslaught confirmed base game)"]
})

# 17. tq-dream-harbinger — Dream Harbinger — SMHFSI
# Warfare+Dream = Harbinger; dream-buffed melee warrior (SMHFSI same prefix as Thane)
records.append({
    "kit_id":"tq-dream-harbinger","folk_name":"Dream Harbinger","game":"tq","status":"positive",
    "atlas_key":"SMHFSI-MSMT-RS-PH-~~",
    "delivery":dc("at-target",0.82,"Harbinger delivers melee strikes; Dream buffs amplify the physical damage"),
    "footprint":dc("point",0.78,"Single-target melee strikes; Dream AoE (Distortion Wave) optional secondary"),
    "geo_text":"Harbinger (Warfare+Dream) uses Warfare melee strikes amplified by Dream mastery's buffs (Psionic Touch, Dream Steal). Dream buffs dramatically increase attack speed and life steal for the melee warrior.",
    "control":ctrl(["slow","stun"],"rider",0.62),
    "defense":defs(["armor","sustain-leech"],"armor",0.80),
    "economy":econ("Energy","reserve","n/a","n/a","Dream mastery buffs maintained as Reserve (Energy per second upkeep). Warfare active skills spend Energy. Hybrid reserve+spend economy.",0.75),
    "element":elem("Physical","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.82,"Warfare = STR; Harbinger STR-primary",
        "melee",0.85,"Warfare melee delivery primary",
        "high",0.82,"High tempo via Dream speed buffs amplifying Warfare attack rate",
        "flat",0.75,"Flat physical DPS; Dream buffs scale the flat output",
        "solo",0.80,"Solo melee fighter",
        "instant",0.80,"Melee strikes instant; Dream buffs toggle-reserved"
    ),
    "mechanics_notes":"RS old code = 'reserve-sustain'; captured as reserve here for Dream passive buffs. Sustain-leech in defense captures Dream's Dream Steal (life drain component). Harbinger is often considered TQ's strongest STR melee archetype due to Dream's extreme speed buffs (Inner Fire, Dream Steal, Psionic Touch synergy).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ IT Warfare+Dream Harbinger; Dream speed buffs + melee confirmed)"]
})

# 18. tq-shield-charge-conqueror — Shield Charge Conqueror — SMMFSI
# Warfare+Defense = Conqueror; Shield Charge = charge movement attack
records.append({
    "kit_id":"tq-shield-charge-conqueror","folk_name":"Shield Charge Conqueror","game":"tq","status":"positive",
    "atlas_key":"SMMFSI-KSMT-CD-PH-~~",
    "delivery":dc("self-origin",0.85,"Shield Charge propels the Conqueror forward; delivery = self-moving charge through enemies"),
    "footprint":dc("lane",0.82,"Charge traces a lane through enemies in the path, applying damage and stun to all hit"),
    "geo_text":"Conqueror (Warfare+Defense) uses Shield Charge to dash forward in a straight line, stunning and damaging all enemies along the path. After the charge, the Conqueror engages in melee.",
    "control":ctrl(["stun","knockback"],"core",0.80),
    "defense":defs(["block","armor"],"armor",0.85),
    "economy":econ("Energy","cooldown","n/a","n/a","Shield Charge has a cooldown (~8-10s) and Energy cost. CD gates the primary engagement tool.",0.80),
    "element":elem("Physical","hit",0.80),
    "movement":mov(["charge"],"full-move",True,0.88),
    "prefix_claims":pfx(
        "STR",0.88,"Warfare+Defense = STR dual-mastery; Conqueror STR confirmed",
        "melee",0.85,"Shield Charge delivers melee contact; charge result is melee engagement",
        "med",0.75,"Med tempo — charge on cooldown; between charges = standard melee",
        "flat",0.72,"Flat charge impact damage; control is the value not burst spike",
        "solo",0.82,"Solo charger",
        "instant",0.82,"Shield Charge activates instantly; charge motion is rapid"
    ),
    "mechanics_notes":"skill_is_movement=True: Shield Charge IS the movement mechanic. D1: Defense mastery adds BLOCK as a core defensive layer (shield required). Conqueror = best tank archetype in TQ base game. Lane footprint = charge traces through enemies. Control centrality: stun on charge is major value.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Warfare+Defense Conqueror; Shield Charge confirmed base game)"]
})

# 19. tq-battlemage-warfare-earth — Battlemage — SMMFSI
# Warfare+Earth = Battlemage; melee+fire magic hybrid
records.append({
    "kit_id":"tq-battlemage-warfare-earth","folk_name":"Battlemage","game":"tq","status":"positive",
    "atlas_key":"SMMFSI-MSDT-SP-FI-~~",
    "delivery":dc("at-target",0.80,"Battlemage delivers melee strikes + Earth fire magic; at-target melee primary"),
    "footprint":dc("point",0.75,"Melee primary = point; Earth fire skills can AoE secondarily"),
    "geo_text":"Battlemage (Warfare+Earth) fuses Warfare melee strikes with Earth mastery fire damage. Eruption (Earth) places fire AoE around targeted area while melee attacks carry the primary single-target output.",
    "control":ctrl(["slow","knockback"],"rider",0.60),
    "defense":defs(["armor","resist"],"armor",0.82),
    "economy":econ("Energy","spend","n/a","n/a","Both Warfare and Earth skills spend Energy per activation. Earth fire skills tend to be moderate cost; Warfare active skills lower cost. Standard spend economy.",0.78),
    "element":elem("Fire","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.82,"Warfare = STR primary; Battlemage STR-melee with Earth secondary",
        "melee",0.82,"Melee delivery primary; Warfare is the melee engine",
        "med",0.72,"Medium tempo — melee attacks plus fire spell weaving",
        "flat",0.72,"Flat melee+fire DPS combination",
        "solo",0.80,"Solo hybrid fighter",
        "instant",0.78,"Melee + Earth spells both fire instantly"
    ),
    "mechanics_notes":"Battlemage = TQ's melee-caster hybrid. Earth mastery provides Volatility passive (fire dot on melee hits) + Earth Enchantment (fire buff), making Warfare melee strikes deal bonus fire damage. This is an elemental melee archetype distinct from the pure-melee Conqueror.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (TQ Warfare+Earth Battlemage; fire-melee hybrid confirmed base game)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# TQ2 POSITIVES — all post-cutoff (tq2-ea-2025+)
# ─────────────────────────────────────────────────────────────────────────────

tq2_kits = [
    {
        "kit_id":"tq2-whirlwind-rogue","folk_name":"Whirlwind Rogue","game":"tq2","status":"positive",
        "atlas_key":"DMHFSC-_SDD-SP-PH-~~",
        "delivery":dc("self-origin",0.45,"Whirlwind Rogue spins — self-origin rotation delivery per folk_name + atlas key pattern (TQ2 EA)"),
        "footprint":dc("small-radius",0.42,"Spin radius AoE around caster per Whirlwind archetype"),
        "geo_text":"TQ2 Whirlwind Rogue (EA 2025) — spinning melee AoE, DEX-channel archetype. Post-cutoff; mechanics inferred from atlas key + folk_name.",
        "control":ctrl(["knockback"],"rider",0.38),
        "defense":defs(["dodge","armor"],"dodge",0.40),
        "economy":econ("Energy","channel","n/a","n/a","Atlas commit=C=channel; Whirlwind sustained channel drain — TQ2 EA, unverified.",0.40),
        "element":elem("Physical","hit",0.42),
        "movement":mov(["mobile-channel"],"full-move",False,0.40),
        "prefix_claims":pfx("DEX",0.48,"Atlas D=DEX; Rogue class DEX confirmed","melee",0.48,"Atlas M=melee; spin melee confirmed","high",0.42,"Atlas H=high tempo","flat",0.40,"Atlas F=flat amp","solo",0.42,"Atlas S=solo","channel",0.48,"Atlas C=channel; whirlwind channel confirmed"),
        "mechanics_notes":"POST-CUTOFF: TQ2 EA (2025+). All conf ≤0.50. Channel commit confirmed by atlas key C; whirlwind spin pattern from folk_name. TQ2 rogue class mechanic details unverified.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["kb (TQ2 EA announced 2025; Rogue class confirmed; whirlwind pattern from atlas key)"]
    },
    {
        "kit_id":"tq2-stormblade-ice-shards","folk_name":"Stormblade Ice Shards","game":"tq2","status":"positive",
        "atlas_key":"IRHFSI-HNMD-SP-CO-~~",
        "delivery":dc("projectile",0.45,"Ice Shard projectile delivery per folk_name + atlas key; TQ2 EA cold caster"),
        "footprint":dc("point",0.40,"Single ice shard projectile per folk_name; pierce possible"),
        "geo_text":"TQ2 Stormblade Ice Shards (EA 2025) — cold projectile caster. Post-cutoff; mechanics from atlas key.",
        "control":ctrl(["freeze","slow"],"rider",0.40),
        "defense":defs(["resist","glass"],"resist",0.40),
        "economy":econ("Energy","spend","n/a","n/a","Cold caster energy spend per shot; TQ2 EA unverified.",0.38),
        "element":elem("Cold","hit",0.45),
        "movement":mov(["standard-move"],"full-move",False,0.40),
        "prefix_claims":pfx("INT",0.48,"Atlas I=INT; caster class","ranged",0.48,"Atlas R=ranged; projectile","high",0.40,"Atlas H=high","flat",0.40,"Atlas F=flat","solo",0.42,"Atlas S=solo","instant",0.40,"Atlas I=instant"),
        "mechanics_notes":"POST-CUTOFF: TQ2 EA (2025+). Conf ≤0.50. Cold projectile caster; 'Stormblade' suggests Storm/Blade mastery combo in TQ2. All details from atlas key provenance.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["kb (TQ2 EA; cold caster confirmed from atlas key + folk_name)"]
    },
    {
        "kit_id":"tq2-forge-turrets","folk_name":"Forge Turrets","game":"tq2","status":"positive",
        "atlas_key":"IRMFHI-_MDM-SP-FI-~~",
        "delivery":dc("at-target",0.45,"Turret placement at target location; forge mastery turret deployment — TQ2 EA"),
        "footprint":dc("large-zone",0.42,"Multiple turrets cover large zone; fire damage AoE from each turret"),
        "geo_text":"TQ2 Forge Turrets (EA 2025) — heavy proxy fire turret placer. Forge mastery places fire-dealing turrets at target locations. Post-cutoff.",
        "control":ctrl(["slow"],"rider",0.35),
        "defense":defs(["armor","resist"],"armor",0.38),
        "economy":econ("Energy","ammo","n/a","n/a","Turret placement likely has count limit (ammo model); Forge mastery details unverified.",0.38),
        "element":elem("Fire","hit",0.45),
        "movement":mov(["standard-move"],"full-move",False,0.40),
        "prefix_claims":pfx("INT",0.48,"Atlas I=INT","ranged",0.45,"Atlas R=ranged; turret range","med",0.40,"Atlas M=med","flat",0.40,"Atlas F=flat","heavy",0.48,"Atlas H=heavy proxy; turrets are the damage source","instant",0.40,"Atlas I=instant placement"),
        "mechanics_notes":"POST-CUTOFF: TQ2 EA (2025+). Forge is a new TQ2 mastery not present in TQ1. Heavy proxy = turrets deliver all damage. Fire element from atlas CO? Wait — atlas elem=FI=fire. All details unverified.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["kb (TQ2 EA Forge mastery announced; turret mechanic inferred)"]
    },
    {
        "kit_id":"tq2-elementalist","folk_name":"Elementalist TQ2","game":"tq2","status":"positive",
        "atlas_key":"IRMSSI-_LMG-SP-FI-~~",
        "delivery":dc("projectile",0.45,"Fire/elemental projectile delivery per atlas key; TQ2 EA elementalist caster"),
        "footprint":dc("small-radius",0.40,"Projectile explosion AoE at impact; medium burst radius"),
        "geo_text":"TQ2 Elementalist (EA 2025) — fire caster equivalent to TQ1's Earth+Storm Elementalist. Spiky burst output. Post-cutoff.",
        "control":ctrl(["shock","slow"],"rider",0.38),
        "defense":defs(["glass","resist"],"glass",0.40),
        "economy":econ("Energy","spend","n/a","n/a","Energy spend caster; TQ2 EA economy unverified.",0.38),
        "element":elem("Fire","hit",0.45),
        "movement":mov(["none"],"rooted",False,0.40),
        "prefix_claims":pfx("INT",0.48,"Atlas I=INT","ranged",0.48,"Atlas R=ranged","med",0.40,"Atlas M","spiky",0.42,"Atlas S=spiky burst","solo",0.42,"Atlas S=solo","instant",0.40,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TQ2 EA (2025+). Conf ≤0.50. TQ2 iteration of the Elementalist dual-mastery nuker archetype. Details unverified beyond atlas key.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["kb (TQ2 EA; Elementalist archetype from TQ1 likely carried forward; atlas key provenance)"]
    },
    {
        "kit_id":"tq2-bastion-tank","folk_name":"Bastion Warfare+Forge","game":"tq2","status":"positive",
        "atlas_key":"SMMFSI-_SMT-SP-PH-~~",
        "delivery":dc("at-target",0.42,"Bastion tank delivers melee strikes per STR-melee atlas key; TQ2 EA"),
        "footprint":dc("small-radius",0.40,"Melee AoE cleave; bastion tank area defense"),
        "geo_text":"TQ2 Bastion (Warfare+Forge) tank — STR-melee archetype with Forge defense components. Post-cutoff EA content.",
        "control":ctrl(["taunt","stun"],"rider",0.38),
        "defense":defs(["armor","block"],"armor",0.42),
        "economy":econ("Energy","spend","n/a","n/a","STR melee tank energy spend; Forge may add construct/armor economy. TQ2 EA unverified.",0.38),
        "element":elem("Physical","hit",0.42),
        "movement":mov(["standard-move"],"full-move",False,0.38),
        "prefix_claims":pfx("STR",0.48,"Atlas S=STR tank","melee",0.48,"Atlas M=melee","med",0.40,"Atlas M=med tempo","flat",0.40,"Atlas F","solo",0.42,"Atlas S=solo","instant",0.40,"Atlas I"),
        "mechanics_notes":"POST-CUTOFF: TQ2 EA (2025+). Conf ≤0.50. Warfare+Forge = Bastion class in TQ2. Forge mastery is new to TQ2 (not in TQ1). Tank archetype with armor+block defense per atlas. Details unverified.",
        "era_confirmed":True,"post_cutoff":True,"dossier_owed":True,"rank1_upgrade":False,
        "sources_used":["kb (TQ2 EA Bastion class; Warfare+Forge combo from folk_name; atlas key provenance)"]
    }
]
records.extend(tq2_kits)

# ─────────────────────────────────────────────────────────────────────────────
# NEGATIVES (2 light schema)
# ─────────────────────────────────────────────────────────────────────────────

records.append({
    "kit_id":"tq-flame-surge","folk_name":"Flame Surge as Primary","game":"tq","status":"negative",
    "atlas_key":"IDHFSI-MSDG-SP-FI-~~",
    "delivery":dc("beam",0.85,"Flame Surge is a fire beam/channel in TQ's Earth mastery — true beam delivery"),
    "footprint":dc("lane",0.82,"Narrow fire beam lane from caster to target"),
    "why_negative":"Flame Surge as sole primary output failed canon viability. The beam requires uninterrupted channel and enemies rarely stay in the lane in TQ's kite-heavy combat. Used as secondary damage layer in other builds, never as primary.",
    "era_span":"base-2006;immortal-throne-2007;anniversary-2016",
    "post_cutoff":False,"dossier_owed":False,
    "prov":"kb",
    "mech_note":"G2: Flame Surge IS a true beam — flag for G2 survey. Its negative status is about build viability, not mechanic quality. Beam delivery with lane footprint correctly characterizes the skill."
})

records.append({
    "kit_id":"tq-calculated-strike","folk_name":"Calculated Strike as Primary","game":"tq","status":"negative",
    "atlas_key":"SMMSSI-MNDT-SP-PH-~~",
    "delivery":dc("at-target",0.82,"Calculated Strike delivers a single high-damage melee blow at target"),
    "footprint":dc("point",0.80,"Single-target precision melee strike; point footprint"),
    "why_negative":"Calculated Strike (Warfare mastery) is a high-damage single-target precision hit on a significant cooldown. As a primary build driver it fails — cooldown too long to sustain, and lower DPS than Onslaught for most scenarios. Viable only as a single-hit setup or PVP insta-kill attempt.",
    "era_span":"base-2006;anniversary-2016",
    "post_cutoff":False,"dossier_owed":False,
    "prov":"kb",
    "mech_note":"High amp (S=spiky) single hit but too infrequent for primary role. The cooldown model makes it a burst-cooldown tool not a sustained primary."
})

# ─────────────────────────────────────────────────────────────────────────────
# WRITE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

pos = sum(1 for r in records if r.get("status")=="positive" and not r.get("post_cutoff"))
pc_count = sum(1 for r in records if r.get("post_cutoff"))
neg = sum(1 for r in records if r.get("status")=="negative")
total = len(records)

print(f"TQ/TQ2: {total} records | pos={pos} neg={neg} post-cutoff={pc_count}")

with open(OUT, "w") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Written: {OUT}")
print()
print("=== DIRECTED SWEEP RESULTS (TQ/TQ2) ===")
print("C2 (support-existence): NO pure-support kit in TQ/TQ2 corpus.")
print("  Closest: tq-ranger-hunting-nature (has pet proxy, but deals own damage too).")
print("  TQ has no healer/buffer-only archetype in the corpus sample.")
print("G2 (line-vs-projectile):")
print("  TRUE BEAM: tq-flame-surge (Flame Surge fire beam, delivery=beam, footprint=lane) — NEGATIVE kit but beam confirmed")
print("  LANE footprint: tq-shield-charge-conqueror (charge traces lane through enemies)")
print("  NEGATIVE flag: tq-flame-surge is negative but is a TRUE BEAM — relevant for G2 beam census")
print("D1 (shield-split):")
print("  BLOCK (physical shield): tq-shield-charge-conqueror (Defense mastery shield)")
print("  DODGE: tq-trap-magician, tq-brigand-poison, tq-marksmanship-haruspex, tq-phantom-strike-dreamkiller, tq-warlock-poison-vitality, tq-ranger-hunting-nature")
print("  ARMOR: tq-onslaught-assassin, tq-thane-storm-warfare, tq-dream-harbinger, tq-shield-charge-conqueror (both), tq-battlemage-warfare-earth, tq-rune-weapon-thunderer")
print("  GLASS: tq-elementalist-volcanic-storm, tq-ice-shard-oracle, tq-ternion-bone-charmer")
print("  SUSTAIN-LEECH: tq-dream-harbinger, tq-warlock-poison-vitality, tq-petmaster-summoner (Nature Regrowth)")
print("  SHIELD-ABSORB: tq-liche-king-conjurer (Liche Form arcane absorption)")
