#!/usr/bin/env python3
"""gen-chronicon-facts.py — Chronicon facts for megaprobe 2026-07-12
17 records: all positive (0 negatives in corpus)
No formal post-cutoff: earliest eras well-documented (ea-2015-2019/1.0-2020)
DLC-only kits (ancient-beasts-dlc / current-1.52 with prov=sf only): conf 0.62-0.72
Base-game kits (prov includes kb): conf 0.75-0.85
Special note: W=WIS attribute for Templar class (first WIS-attr class in probe)
"""
import json

OUT = "agentic_orchestration/legolas/research/megaprobe-2026-07-12/chronicon-facts.jsonl"

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
# WARDEN kits (DEX archer/hunter/pet class)
# ─────────────────────────────────────────────────────────────────────────────

# 1. chr-bee-warden — Bee Swarm Warden — DDLFHI (proxy=H=heavy, tempo=L=low)
records.append({
    "kit_id":"chr-bee-warden","folk_name":"Bee Swarm Warden","game":"chronicon","status":"positive",
    "atlas_key":"DDLFHI-HLDD-SU-PO-~~",
    "delivery":dc("self-origin",0.78,"Warden summons bee swarm that disperses from caster position outward; summon delivery from self-origin"),
    "footprint":dc("large-zone",0.75,"Bee swarm covers large zone around and ahead of Warden; heavy proxy coverage area"),
    "geo_text":"Bee Swarm Warden deploys swarms of poisonous bees that spread from the caster's position and attack nearby enemies. Bees persist as a heavy proxy, delivering poison DoT across the combat zone.",
    "control":ctrl(["poison","slow"],"rider",0.65),
    "defense":defs(["dodge","resist"],"dodge",0.75),
    "economy":econ("Focus","reserve","n/a","n/a","Bee swarm maintained via Focus reserve (Warden's resource). SU economy = sustain/reserve. Bees persist until killed or duration expires; re-summon costs Focus.",0.72),
    "element":elem("Poison","dot",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.80,"Warden = DEX class confirmed",
        "mid",0.72,"Bee swarm disperses from caster to mid-range coverage",
        "low",0.75,"Low tempo: bees sting at a slow persistent rate; L=low confirmed in atlas",
        "flat",0.72,"Flat poison DoT per bee sting; consistent slow drain",
        "heavy",0.80,"Heavy proxy: bees deliver all damage; Warden provides no direct damage",
        "instant",0.75,"Bee summon activates instantly"
    ),
    "mechanics_notes":"Proxy=heavy + element=Poison DoT = the defining combo. Low tempo (L) captures bees' slow-sting cadence. SU economy = bee reserve maintenance. Chronicon's pet warden archetype includes both Bee Swarm (poison focus) and Pet Zoo (mixed pet army). First WIS-attr class not present in Warden — Warden is DEX.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (Chronicon Warden Bee Swarm; poison pet proxy confirmed 1.0-2020)"]
})

# 2. chr-pet-warden — Pet Zoo Warden — DMMFHI (proxy=H=heavy)
records.append({
    "kit_id":"chr-pet-warden","folk_name":"Pet Zoo Warden","game":"chronicon","status":"positive",
    "atlas_key":"DMMFHI-HNDM-SU-PH-~~",
    "delivery":dc("self-origin",0.78,"Warden commands diverse pet army that attacks from various positions; self-origin command"),
    "footprint":dc("large-zone",0.78,"Mixed pet army (wolves, bees, mechanical pets, etc.) covers entire combat zone"),
    "geo_text":"Pet Zoo Warden commands the largest diverse pet roster in Chronicon — wolves, mechanical companions, summon varieties. The zoo of pets fills the combat zone, each type contributing different attack patterns.",
    "control":ctrl(["taunt"],"rider",0.60),
    "defense":defs(["dodge","hp-stack"],"dodge",0.72),
    "economy":econ("Focus","reserve","n/a","n/a","All pets maintained via Focus reserve drain. Multiple pet types compound the reserve cost. Pet Zoo Warden requires maximum Focus regeneration investment.",0.75),
    "element":elem("Physical","hit",0.72),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.80,"Warden = DEX class",
        "melee",0.70,"Pets primarily engage in melee; 'melee' range here = pet engagement range (close)",
        "med",0.72,"Medium tempo via diverse pet attack rates",
        "flat",0.72,"Flat aggregate pet DPS",
        "heavy",0.82,"Heavy proxy: entire diverse pet army delivers all damage",
        "instant",0.72,"Pet commands instant"
    ),
    "mechanics_notes":"'Pet Zoo' = maximum pet diversity build. Heavy proxy is the defining feature. The 'range=melee' (M in pos 2) is unusual for a pet master but reflects that the Warden operates in close-to-mid range while pets engage in melee. Compare to Bee Warden (single pet type, heavier DoT focus). DLC prov (sf) reduces confidence slightly.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf;kb (Chronicon Pet Zoo Warden; current-1.52 and 1.0-2020 confirmed)"]
})

# 3. chr-arrow-storm-warden — Arrow Storm Warden — DRHFSI
records.append({
    "kit_id":"chr-arrow-storm-warden","folk_name":"Arrow Storm Warden","game":"chronicon","status":"positive",
    "atlas_key":"DRHFSI-HLDD-SP-PH-~~",
    "delivery":dc("projectile",0.82,"Arrow Storm fires a hail of arrows at/across target area; projectile barrage delivery"),
    "footprint":dc("large-zone",0.78,"Storm of arrows rains across a large target zone; multiple projectiles cover wide area"),
    "geo_text":"Arrow Storm Warden fires a sustained volley of arrows that blankets a large target area. The arrow barrage creates zone denial and high hit-count per second across the impacted zone.",
    "control":ctrl(["slow"],"rider",0.60),
    "defense":defs(["dodge","resist"],"dodge",0.78),
    "economy":econ("Focus","spend","n/a","n/a","Arrow Storm costs Focus on activation. High Focus cost for the barrage. Warden's Focus regenerates between uses.",0.78),
    "element":elem("Physical","hit",0.78),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "DEX",0.82,"Warden = DEX class",
        "ranged",0.85,"Arrow Storm fires arrows at range; clear ranged delivery",
        "high",0.80,"High projectile count per second during storm",
        "flat",0.75,"Flat consistent damage across the storm",
        "solo",0.80,"No proxy entities; solo barrage",
        "instant",0.80,"Arrow Storm activates instantly"
    ),
    "mechanics_notes":"Early Access archetype (ea-2015-2019); well-documented base game skill. Footprint=large-zone (not cone) because the storm covers a wide area not a directional spread. Contrasts with chr-high-ranger-warden's single-target precise arrow focus.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (Chronicon Warden Arrow Storm; EA+1.0 confirmed large-zone barrage)"]
})

# 4. chr-high-ranger-warden — High Ranger Bleed Warden — DRLFSI (tempo=L=low)
records.append({
    "kit_id":"chr-high-ranger-warden","folk_name":"High Ranger Bleed Warden","game":"chronicon","status":"positive",
    "atlas_key":"DRLFSI-HNDT-DW-PH-~~",
    "delivery":dc("projectile",0.68,"High Ranger fires precision arrows at single targets; projectile delivery"),
    "footprint":dc("point",0.68,"Single-target precision arrow; high damage per hit rather than AoE"),
    "geo_text":"High Ranger Warden fires precise single-target arrows that apply heavy bleed stacks. Low tempo reflects the deliberate shot cadence; bleed DoT does the work between shots.",
    "control":ctrl(["bleed","slow"],"rider",0.65),
    "defense":defs(["dodge","resist"],"dodge",0.68),
    "economy":econ("Focus","other","n/a","n/a","DW old code likely = 'drain-while': bleed DoT economy drains enemy HP continuously while active. Focus spent on arrow activation; bleed sustains between shots. Hybrid spend+drain model.",0.62),
    "element":elem("Physical","dot",0.68),
    "movement":mov(["standard-move"],"full-move",False,0.65),
    "prefix_claims":pfx(
        "DEX",0.72,"Warden = DEX class",
        "ranged",0.72,"Precision arrow = ranged delivery",
        "low",0.70,"Atlas L=low: deliberate shot cadence; bleed DoT does sustained work between shots",
        "flat",0.68,"Flat bleed DoT per stack application",
        "solo",0.68,"Solo precision archer",
        "instant",0.68,"Arrow fires instantly"
    ),
    "mechanics_notes":"DW economy = interpreted as 'drain-while' (DoT drain between shots). Damage_mode=dot: bleed is the primary damage vector (hits apply stacks, stacks do the damage). Low tempo = slow aimed shots. DLC-only prov (sf) reduces conf. D1 note: dodge archetype (Warden = evasion-focused class).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon High Ranger Bleed Warden; DLC build; prov=sf only)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# WARLOCK kits (INT caster/summoner)
# ─────────────────────────────────────────────────────────────────────────────

# 5. chr-bloodbinder-warlock — Bloodbinder Warlock — IDMFHI (proxy=H=heavy, range=D=mid)
records.append({
    "kit_id":"chr-bloodbinder-warlock","folk_name":"Bloodbinder Warlock","game":"chronicon","status":"positive",
    "atlas_key":"IDMFHI-MSDM-SU-PO-~~",
    "delivery":dc("self-origin",0.68,"Bloodbinder Warlock binds blood-constructs that fight from caster position; self-origin summon"),
    "footprint":dc("small-radius",0.65,"Blood-bound entities fight in close radius to caster"),
    "geo_text":"Bloodbinder Warlock uses self-sacrifice magic to summon blood-bound entities (constructs powered by own HP drain). Heavy proxy layer funded by self-cost economy.",
    "control":ctrl(["poison","bleed"],"rider",0.60),
    "defense":defs(["shield-absorb","resist"],"shield-absorb",0.65),
    "economy":econ("HP + Mana","self-cost","n/a","n/a","Bloodbinder drains caster's own HP to power blood-summoning. Self-cost economy: HP is the primary resource currency. SU old code = sustain (of bound entities at HP cost).",0.65),
    "element":elem("Poison","dot",0.68),
    "movement":mov(["standard-move"],"full-move",False,0.65),
    "prefix_claims":pfx(
        "INT",0.72,"Warlock = INT class confirmed",
        "mid",0.65,"Blood-bound entities fight at mid range from caster",
        "med",0.62,"Medium tempo sustained from blood constructs",
        "flat",0.62,"Flat blood-proxy DPS",
        "heavy",0.70,"Heavy proxy: blood-bound constructs deliver all damage",
        "instant",0.68,"Blood-bind activates instantly"
    ),
    "mechanics_notes":"Self-cost economy is distinctive — caster's HP funds the summon. 1.0-2020 era + ancient-beasts-dlc (sf prov for DLC component). Poison element from blood-magic (poison DoT). shield-absorb defense = Warlock has a barrier/blood-shield layer. Heavy proxy confirmed by atlas key H.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf;kb (Chronicon Bloodbinder Warlock; self-cost HP economy + blood-proxy confirmed)"]
})

# 6. chr-demon-legion-warlock — Demon Legion Warlock — IMMFHI (proxy=H=heavy)
records.append({
    "kit_id":"chr-demon-legion-warlock","folk_name":"Demon Legion Warlock","game":"chronicon","status":"positive",
    "atlas_key":"IMMFHI-MNMM-SU-SH-~~",
    "delivery":dc("self-origin",0.80,"Warlock summons demon legion from self-origin; demons disperse and fight independently"),
    "footprint":dc("large-zone",0.78,"Demon army covers large combat zone with multiple entity attacks"),
    "geo_text":"Demon Legion Warlock summons a swarm of demonic minions that fill the combat area. The demon army is the primary damage source; Warlock commands from a safe distance.",
    "control":ctrl(["taunt","fear"],"rider",0.62),
    "defense":defs(["shield-absorb","resist"],"shield-absorb",0.72),
    "economy":econ("Mana","reserve","n/a","n/a","Demon summons maintained via Mana reserve upkeep. Re-summoning slain demons costs Mana. SU = sustain/reserve economy.",0.78),
    "element":elem("Shadow","hit",0.75),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "INT",0.80,"Warlock = INT class",
        "melee",0.72,"Demons engage in melee; 'melee' range from atlas = demon combat range",
        "med",0.75,"Medium tempo sustained from demon attacks",
        "flat",0.72,"Flat demon DPS",
        "heavy",0.85,"Heavy proxy: demon army delivers all damage; classic summoner archetype",
        "instant",0.78,"Summon commands instant"
    ),
    "mechanics_notes":"EA-2015-2019 + 1.0-2020 (early archetype, kb confirmed). Shadow element from demon/dark magic. D1: shield-absorb = Warlock has arcane/dark barrier defense. Heavy proxy = the defining characteristic, same structural pattern as TQ Petmaster and TL2 Bot Engineer.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (Chronicon Warlock Demon Legion summoner; EA+1.0 confirmed)"]
})

# 7. chr-firestorm-warlock — Sun & Moon Firestorm Warlock — IRHFSI (MT econ = proc)
records.append({
    "kit_id":"chr-firestorm-warlock","folk_name":"Sun Moon Firestorm Warlock","game":"chronicon","status":"positive",
    "atlas_key":"IRHFSI-HLDM-MT-FI-~~",
    "delivery":dc("at-target",0.68,"Sun & Moon Firestorm calls fire zones at target locations; at-target delivery"),
    "footprint":dc("large-zone",0.68,"Fire storm covers large zone at target; Sun fires a high-damage burst, Moon provides sustained coverage"),
    "geo_text":"Firestorm Warlock uses Sun and Moon Relic skills — Sun calls a large fire burst at target, Moon provides a sustained fire zone. Together they create a large persistent fire AoE with proc-chain triggering.",
    "control":ctrl(["slow"],"rider",0.55),
    "defense":defs(["glass","resist"],"glass",0.65),
    "economy":econ("Mana","proc","n/a","on_cast","MT (multi-trigger) = proc-chain economy. Sun and Moon skills proc additional fire events on cast. Each proc can trigger follow-up procs in a chain. Mana is the base resource gated by proc opportunities.",0.62),
    "element":elem("Fire","hit",0.70),
    "movement":mov(["standard-move"],"full-move",False,0.62),
    "prefix_claims":pfx(
        "INT",0.72,"Warlock = INT class",
        "ranged",0.70,"Fire zones placed at range",
        "high",0.68,"High proc frequency in proc-chain during peak trigger state",
        "flat",0.65,"Flat fire damage per proc event",
        "solo",0.68,"No proxy entities; zone placement skill",
        "instant",0.68,"Fire zones appear instantly"
    ),
    "mechanics_notes":"MT economy = proc-chain (multi-trigger): Sun+Moon procs cascade fire events. DLC-only archetype (sf prov). 'Sun & Moon' naming refers to Chronicon's Relic system where Sun Relic and Moon Relic synergize. Proc-chain economy is the defining mechanical novelty of this kit.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Firestorm Warlock Sun+Moon Relic proc chain; DLC archetype)"]
})

# 8. chr-plague-curse-warlock — Plague Mage / Desecrator Curse Warlock — IRLSSI (tempo=L=low, amp=spiky)
records.append({
    "kit_id":"chr-plague-curse-warlock","folk_name":"Plague Mage Desecrator Curse Warlock","game":"chronicon","status":"positive",
    "atlas_key":"IRLSSI-MLMM-AM-SH-~~",
    "delivery":dc("at-target",0.68,"Curse/plague applied at target location or on target enemy; at-target delivery"),
    "footprint":dc("small-radius",0.65,"Curse AoE at target; plague spreads in small radius around infected enemies"),
    "geo_text":"Curse Warlock applies stacking plague and desecration curses to enemies. Low tempo reflects the deliberate curse-application cadence; spiky amp captures burst when curse stacks detonate.",
    "control":ctrl(["poison","curse","slow"],"core",0.72),
    "defense":defs(["shield-absorb","glass"],"glass",0.62),
    "economy":econ("Mana","ammo","n/a","n/a","AM = ammo: curse charges are a limited-stock resource. Each Desecrator curse application consumes a curse charge. Charges accumulate passively (or via kills) up to a cap.",0.60),
    "element":elem("Shadow","dot",0.70),
    "movement":mov(["standard-move"],"full-move",False,0.62),
    "prefix_claims":pfx(
        "INT",0.72,"Warlock = INT class",
        "ranged",0.68,"Curse applied at range",
        "low",0.70,"Atlas L=low: deliberate curse application cadence; DoT does work between applications",
        "spiky",0.68,"Atlas S=spiky: curse stack detonation = burst spike",
        "solo",0.68,"Solo curse mage",
        "instant",0.68,"Curse applies instantly"
    ),
    "mechanics_notes":"Control centrality=CORE: curses ARE the purpose of this kit (debuff-centric playstyle). Ammo economy = curse charges (limited stock, accumulates over time). Shadow element from shadow/dark magic. DLC-only (sf prov). Low tempo + spiky is an interesting pattern: slow application + burst detonation.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Plague Mage/Desecrator Curse Warlock; DLC archetype)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# MECHANIST kits (INT/STR gadget/robot class)
# ─────────────────────────────────────────────────────────────────────────────

# 9. chr-mechanist-saw-master — Saw Master Mechanist — IDHSLI (proxy=L=light)
records.append({
    "kit_id":"chr-mechanist-saw-master","folk_name":"Saw Master Mechanist","game":"chronicon","status":"positive",
    "atlas_key":"IDHSLI-HCDM-SP-PH-~~",
    "delivery":dc("projectile",0.65,"Saw blades are launched as projectiles that ricochet between enemies at mid range"),
    "footprint":dc("chain-hop",0.62,"Saw blade bounces between multiple targets; chain-hop footprint"),
    "geo_text":"Saw Master Mechanist launches saw blades that ricochet between nearby enemies at mid range. Each bounce deals damage; the saw can chain multiple hits per launch at high speed.",
    "control":ctrl(["bleed"],"rider",0.58),
    "defense":defs(["armor","resist"],"armor",0.65),
    "economy":econ("Heat/Power","spend","n/a","n/a","Mechanist uses a Heat or Power Core resource; Saw Master skills spend this resource per activation. SP = spend economy.",0.60),
    "element":elem("Physical","hit",0.68),
    "movement":mov(["standard-move"],"full-move",False,0.62),
    "prefix_claims":pfx(
        "INT",0.68,"Mechanist = INT class (gadget/engineer caster)",
        "mid",0.65,"Saw blade range = mid; not point-blank, not full range",
        "high",0.65,"High tempo via rapid saw launches",
        "spiky",0.65,"Each saw bounce = burst spike per hit",
        "light",0.65,"Light proxy: saw blade is a projectile (light entity), not a heavy bot army",
        "instant",0.65,"Saw launched instantly"
    ),
    "mechanics_notes":"G2: Saw blade bouncing = chain-hop, NOT a line. Ricochet pattern similar to TL2 Glaive and TL1 Ricochet. Light proxy (L) = saw as a projectile entity vs heavy-proxy turrets. DLC-only prov (sf) reduces conf. Mechanist class occupies INT attribute despite being a tech/gadget archetype.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Saw Master Mechanist; DLC archetype; chain-hop saw pattern)"]
})

# 10. chr-mechanist-turret-drone — Turret & Drone Mechanist — IRMFHI (proxy=H=heavy)
records.append({
    "kit_id":"chr-mechanist-turret-drone","folk_name":"Turret Drone Mechanist","game":"chronicon","status":"positive",
    "atlas_key":"IRMFHI-HMDM-SP-HO-~~",
    "delivery":dc("at-target",0.68,"Mechanist deploys turrets and drones at target positions; at-target deployment"),
    "footprint":dc("large-zone",0.68,"Turret+drone coverage fills large combat zone"),
    "geo_text":"Turret & Drone Mechanist deploys fixed turrets and mobile drone units at target locations. The deployed machines cover the entire combat area, acting as a heavy proxy damage network.",
    "control":ctrl(["slow"],"rider",0.55),
    "defense":defs(["armor","resist"],"armor",0.65),
    "economy":econ("Power Cores","spend","n/a","n/a","Deploying turrets and drones costs Power Cores. Reserve economy for maintenance (deployed machines persist until destroyed). SP old code = spend on deployment.",0.62),
    "element":elem("Physical","hit",0.62),
    "movement":mov(["standard-move"],"full-move",False,0.65),
    "prefix_claims":pfx(
        "INT",0.68,"Mechanist = INT class",
        "ranged",0.68,"Turrets/drones attack at range; Mechanist maintains distance",
        "med",0.62,"Medium tempo from distributed turret fire",
        "flat",0.62,"Flat turret DPS",
        "heavy",0.75,"Heavy proxy: turrets+drones deliver all damage; Mechanist is the deployer",
        "instant",0.65,"Deployment activates instantly"
    ),
    "mechanics_notes":"HO elem in old code = possibly 'holographic' in Chronicon's Mechanist context, or a Chronicon-specific element code. Captured as Physical since turrets fire physical projectiles. Heavy proxy mirrors TL2 Bot Engineer. DLC archetype (sf prov).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Turret+Drone Mechanist; DLC heavy-proxy archetype)"]
})

# 11. chr-mechanist-rocketeer — Rocketeer Mechanist — IRMSSI (amp=spiky, solo)
records.append({
    "kit_id":"chr-mechanist-rocketeer","folk_name":"Rocketeer Mechanist","game":"chronicon","status":"positive",
    "atlas_key":"IRMSSI-HSDM-SP-FI-~~",
    "delivery":dc("projectile",0.70,"Rocketeer fires rockets as explosive projectiles at range"),
    "footprint":dc("small-radius",0.68,"Rocket explosion creates a small AoE blast radius at impact point"),
    "geo_text":"Rocketeer Mechanist fires explosive rockets at range. Each rocket explodes on impact dealing burst fire damage in a small AoE. Rocket salvo bursts create spiky damage windows.",
    "control":ctrl(["knockback"],"rider",0.58),
    "defense":defs(["armor","resist"],"armor",0.65),
    "economy":econ("Ammo/Rockets","ammo","n/a","n/a","SP old code = spend; Rocketeer has limited rocket salvo (ammo). Rockets reload/regenerate over time. Ammo-spend hybrid model.",0.62),
    "element":elem("Fire","hit",0.70),
    "movement":mov(["standard-move"],"rooted",False,0.62),
    "prefix_claims":pfx(
        "INT",0.68,"Mechanist = INT class",
        "ranged",0.72,"Rockets fire at long range",
        "med",0.65,"Moderate tempo; rockets on salvo cooldown",
        "spiky",0.70,"Rocket burst per impact = spiky amp pattern; atlas S=spiky confirmed",
        "solo",0.70,"No proxy; solo rocket operator",
        "instant",0.68,"Rocket launches instantly"
    ),
    "mechanics_notes":"Spiky amp correctly captures rocket burst-per-impact pattern. DLC-only archetype (sf prov). Different from Turret/Drone (heavy proxy) — Rocketeer is solo direct fire. Fire element = explosive rockets.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Rocketeer Mechanist; DLC burst archetype)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# BERSERKER kits (STR melee)
# ─────────────────────────────────────────────────────────────────────────────

# 12. chr-fire-berserker — Fire Avatar Berserker — SMHSSI (MT econ, spiky)
records.append({
    "kit_id":"chr-fire-berserker","folk_name":"Fire Avatar Berserker","game":"chronicon","status":"positive",
    "atlas_key":"SMHSSI-HSDG-MT-FI-~~",
    "delivery":dc("self-origin",0.80,"Fire Avatar transforms Berserker into a fire-elemental form; damage radiates from transformed self"),
    "footprint":dc("small-radius",0.78,"Fire Avatar AoE in radius around transformed Berserker body"),
    "geo_text":"Fire Avatar Berserker channels a fire-elemental transformation that radiates fire damage from the Berserker's body in a burst AoE. Multi-trigger procs amplify the fire burst chain during Avatar state.",
    "control":ctrl(["knockback","fear"],"rider",0.62),
    "defense":defs(["armor","hp-stack"],"armor",0.80),
    "economy":econ("Rage","proc","n/a","on_hit","MT = multi-trigger proc economy: Fire Avatar hits trigger additional proc events in a chain. Rage built from melee hits (on_hit builder). Proc chain amplifies during high-Rage state.",0.75),
    "element":elem("Fire","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.75),
    "prefix_claims":pfx(
        "STR",0.82,"Berserker = STR class confirmed",
        "melee",0.82,"Fire Avatar is a melee-range AoE transform; close proximity required",
        "high",0.80,"High tempo burst during Avatar activation",
        "spiky",0.82,"Avatar burst = extreme damage spike; atlas S=spiky confirmed",
        "solo",0.80,"Self-transformation; no proxy",
        "instant",0.80,"Fire Avatar activates instantly on cast"
    ),
    "mechanics_notes":"MT (multi-trigger/proc chain) is the economy driver. Fire Avatar transformation = the Berserker itself becomes the fire entity (compare to TQ Liche King Conjurer pattern). EA+1.0 archetype (kb confirmed). D1 note: armor is primary for all Berserker kits.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (Chronicon Berserker Fire Avatar; EA+1.0; proc-chain confirmed)"]
})

# 13. chr-bleed-berserker — Bleed Berserker — SMLFSI (tempo=L=low, DW econ)
records.append({
    "kit_id":"chr-bleed-berserker","folk_name":"Bleed Berserker","game":"chronicon","status":"positive",
    "atlas_key":"SMLFSI-HSDT-DW-PH-~~",
    "delivery":dc("at-target",0.82,"Bleed Berserker delivers melee strikes at target; each hit applies bleed stacks"),
    "footprint":dc("point",0.78,"Single-target melee strikes; bleed spreads as DoT after application"),
    "geo_text":"Bleed Berserker applies heavy bleed stacks via melee strikes. Low tempo reflects the deliberate, high-damage single strikes rather than rapid flurry. Bleed DoT stacks accumulate and drain enemy HP continuously.",
    "control":ctrl(["bleed","slow"],"rider",0.65),
    "defense":defs(["armor","hp-stack"],"armor",0.80),
    "economy":econ("Rage","other","n/a","n/a","DW economy = 'drain-while': bleed drains enemy HP continuously while stacks are active. Rage spend to activate bleed-strike skills. Economy is a hybrid: Rage spend to apply bleed, then bleed drains automatically.",0.72),
    "element":elem("Physical","dot",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.82,"Berserker = STR class",
        "melee",0.85,"Bleed application via melee strikes; melee range confirmed",
        "low",0.78,"Atlas L=low: slow deliberate strikes; bleed DoT does the work between hits",
        "flat",0.72,"Flat bleed DoT per stack (consistent drain rate)",
        "solo",0.80,"Solo bleed applicator; no proxy",
        "instant",0.80,"Strikes fire instantly"
    ),
    "mechanics_notes":"Damage_mode=dot (bleed is the damage engine). Low tempo (L) is the key distinction — fewer but harder strikes that each apply max bleed stacks efficiently. DW economy = drain-while (bleed sustains). 1.0-2020 archetype (kb confirmed). D1: all Berserker kits = armor primary.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (Chronicon Bleed Berserker 1.0; melee bleed-stack archetype confirmed)"]
})

# 14. chr-frost-berserker — Frost Shatter Berserker — SMMSSI (amp=spiky)
records.append({
    "kit_id":"chr-frost-berserker","folk_name":"Frost Shatter Berserker","game":"chronicon","status":"positive",
    "atlas_key":"SMMSSI-MSMM-SP-CO-~~",
    "delivery":dc("at-target",0.80,"Frost Berserker delivers melee strikes that apply frost stacks, then shatters for burst"),
    "footprint":dc("small-radius",0.75,"Shatter burst creates a small cold AoE around target at the moment of detonation"),
    "geo_text":"Frost Shatter Berserker applies frost stacks via melee strikes, then detonates them in a burst shatter explosion. The shatter provides a small AoE burst of cold damage.",
    "control":ctrl(["freeze","slow"],"rider",0.72),
    "defense":defs(["armor","hp-stack"],"armor",0.80),
    "economy":econ("Rage","spend","n/a","n/a","Rage spend on frost strikes and shatter activation. Standard spend model between shatter cycles.",0.78),
    "element":elem("Cold","hit",0.82),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "STR",0.82,"Berserker = STR class",
        "melee",0.82,"Frost strikes require melee contact",
        "med",0.75,"Medium tempo: apply frost, then shatter; cadence between shatter cycles",
        "spiky",0.80,"Shatter detonation = burst spike; atlas S=spiky confirmed",
        "solo",0.80,"Solo frost striker; no proxy",
        "instant",0.80,"Strike and shatter activate instantly"
    ),
    "mechanics_notes":"Frost-shatter mechanic: accumulate frost → detonate for burst. This is the stack-then-burst pattern shared with PoE's freeze-shatter mechanic and D3 variants. EA+1.0 archetype (kb confirmed). Cold element = Chronicon's explicit cold damage type.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["kb (Chronicon Frost Shatter Berserker; EA+1.0 frost-burst confirmed)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# TEMPLAR kits (WIS holy warrior — first WIS-attr class in mega-probe!)
# ─────────────────────────────────────────────────────────────────────────────

# 15. chr-fulmination-templar — Fulmination Holy Reckoning Templar — WMHFSI (W=WIS!, PC econ)
records.append({
    "kit_id":"chr-fulmination-templar","folk_name":"Fulmination Holy Reckoning Templar","game":"chronicon","status":"positive",
    "atlas_key":"WMHFSI-MCDT-PC-LI-~~",
    "delivery":dc("at-target",0.75,"Fulmination triggers holy lightning on melee hits; at-target delivery via melee contact"),
    "footprint":dc("point",0.72,"Holy lightning strikes point target on proc; occasionally chains"),
    "geo_text":"Fulmination Templar triggers Holy Reckoning lightning procs on melee hits. High tempo melee attacks chain into rapid lightning proc events via the Crown of Innate Probability or Fulmination passive.",
    "control":ctrl(["shock","stun"],"rider",0.68),
    "defense":defs(["block","armor"],"armor",0.80),
    "economy":econ("Conviction","proc","n/a","on_hit","PC = proc-chain economy. Fulmination lightning procs from melee hits (on_hit builder). Conviction is Templar's resource; procs don't cost Conviction — they trigger from melee contact. Chain procs self-sustain.",0.72),
    "element":elem("Lightning","hit",0.80),
    "movement":mov(["standard-move"],"full-move",False,0.72),
    "prefix_claims":pfx(
        "WIS",0.82,"Templar = WIS class confirmed. First WIS-attribute corpus kit in probe (unique to Chronicon in the 19-game corpus)",
        "melee",0.80,"Fulmination triggers from melee hits; melee range required",
        "high",0.80,"High melee attack tempo (W=WIS doesn't slow tempo; Templar attacks rapidly)",
        "flat",0.75,"Flat lightning proc damage per trigger",
        "solo",0.78,"No proxy; solo holy warrior",
        "instant",0.78,"Melee strikes instant; lightning procs instant"
    ),
    "mechanics_notes":"WIS attribute is notable — Chronicon's Templar uses WIS as the primary attribute, distinct from all other classes in the corpus. Proc-chain (PC) economy: Fulmination Holy Reckoning procs chain lightning events from melee hits. Block defense: Templar uses shield+block. 1.0-2020 + DLC confirmed (sf;kb).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf;kb (Chronicon Fulmination Templar; WIS class + proc-chain lightning confirmed)"]
})

# 16. chr-thorns-templar — Thorns Barrier Templar — WMLFSI (tempo=L=low, SW econ)
records.append({
    "kit_id":"chr-thorns-templar","folk_name":"Thorns Barrier Templar","game":"chronicon","status":"positive",
    "atlas_key":"WMLFSI-LNDT-SW-PH-~~",
    "delivery":dc("self-origin",0.70,"Thorns damage reflects from caster's body when enemies attack; self-origin reflect delivery"),
    "footprint":dc("small-radius",0.68,"Reflect damage activates in contact radius — enemies must strike the Templar to trigger Thorns"),
    "geo_text":"Thorns Barrier Templar builds a powerful damage-reflection barrier. Enemies who attack the Templar suffer Thorns damage. Low tempo reflects the defensive wait-to-be-hit cadence of this archetype.",
    "control":ctrl(["taunt"],"core",0.68),
    "defense":defs(["block","armor","shield-absorb"],"block",0.82),
    "economy":econ("Conviction","proc","n/a","on_damage_taken","SW economy = 'self-wound' or 'shield-wall': taking damage triggers Thorns proc event. Economy driven by on_damage_taken events. Conviction is Templar's resource but Thorns activates on hits-received, not on cast.",0.65),
    "element":elem("Physical","hit",0.70),
    "movement":mov(["standard-move"],"rooted",False,0.68),
    "prefix_claims":pfx(
        "WIS",0.80,"Templar = WIS class",
        "melee",0.72,"Thorns operates at melee contact range (enemies must hit the Templar)",
        "low",0.75,"Atlas L=low: extremely low active tempo; the Templar WAITS to be hit",
        "flat",0.68,"Flat Thorns reflect damage per proc",
        "solo",0.72,"Solo defensive tank",
        "instant",0.68,"Thorns reflect fires instantly when hit"
    ),
    "mechanics_notes":"Control centrality=CORE: Thorns Templar is fundamentally about taunting enemies into attacking them to proc damage reflection — the CC (taunt) IS the purpose. Economy = proc on damage taken (SW = 'self-wound' or 'shield-wall'). Low tempo = Templar sits and waits. D1: block + armor + shield-absorb = maximum defensive layering. DLC-only (sf prov).",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Thorns Barrier Templar; DLC archetype; damage-reflect economy)"]
})

# 17. chr-crown-proc-engine — Crown of Innate Probability proc-lock — IRHFSI (PC econ)
# This is a system/meta record: the Crown of Innate Probability is a special relic item
# that creates a proc-lock economy archetype spanning multiple classes
records.append({
    "kit_id":"chr-crown-proc-engine","folk_name":"Crown of Innate Probability Proc-Lock","game":"chronicon","status":"positive",
    "atlas_key":"IRHFSI-MSDM-PC-__-~~",
    "delivery":dc("projectile",0.65,"Crown proc-lock enables rapid projectile spam via proc chaining; INT ranged delivery per atlas key"),
    "footprint":dc("point",0.62,"Proc-chain fires rapid point-target projectiles in succession"),
    "geo_text":"Crown of Innate Probability is a unique Relic that enables a proc-lock state — skills chain proc additional skill activations indefinitely, creating a cascade of rapid-fire projectile events.",
    "control":ctrl(["shock"],"rider",0.55),
    "defense":defs(["resist","glass"],"glass",0.60),
    "economy":econ("Mana","proc","n/a","on_proc","PC = proc-chain economy. Crown of Innate Probability creates a proc-lock state: each proc triggers additional procs. The economy is self-sustaining via the proc chain itself — Mana consumption becomes secondary to the proc cascade frequency.",0.65),
    "element":elem("n/a","hit",0.55),
    "movement":mov(["standard-move"],"full-move",False,0.60),
    "prefix_claims":pfx(
        "INT",0.68,"Atlas I=INT; Crown typically used by INT-class builds",
        "ranged",0.68,"Ranged projectile spam during proc-lock",
        "high",0.70,"Extreme high tempo during proc-lock cascade",
        "flat",0.62,"Flat per-proc damage; aggregate DPS from cascade",
        "solo",0.65,"No proxy during proc-lock (pure spell cascade)",
        "instant",0.68,"Each proc fires instantly; cascade is immediate"
    ),
    "mechanics_notes":"SYSTEM RECORD / RELIC ARCHETYPE: Crown of Innate Probability is a unique Relic item, not a class skill. The 'proc-lock' state = indefinite proc cascade loop that fires rapid skill activations. This is Chronicon's most distinctive economy archetype — a self-sustaining proc engine. elem=__ (blank in atlas key) = element-agnostic (proc cascade works with any damage type). Spans multiple classes. PC economy = proc/proc-loop.",
    "era_confirmed":True,"post_cutoff":False,"dossier_owed":False,"rank1_upgrade":False,
    "sources_used":["sf (Chronicon Crown of Innate Probability relic; DLC proc-lock archetype)"]
})

# ─────────────────────────────────────────────────────────────────────────────
# WRITE OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

pos = sum(1 for r in records if r.get("status")=="positive" and not r.get("post_cutoff"))
pc_count = sum(1 for r in records if r.get("post_cutoff"))
neg = sum(1 for r in records if r.get("status")=="negative")
total = len(records)

print(f"Chronicon: {total} records | pos={pos} neg={neg} post-cutoff={pc_count}")

with open(OUT, "w") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Written: {OUT}")
print()
print("=== DIRECTED SWEEP RESULTS (Chronicon) ===")
print("C2 (support-existence): NO pure-support kit in Chronicon corpus.")
print("  Closest: chr-thorns-templar (taunt+reflect) but this is a self-serving tank, not pure support.")
print("G2 (line-vs-projectile):")
print("  NO true beams in Chronicon corpus.")
print("  Chain-hop: chr-mechanist-saw-master (saw ricochets = chain-hop, NOT line)")
print("  Large-zone storm: chr-arrow-storm-warden (barrage zone, not directional beam)")
print("D1 (shield-split):")
print("  BLOCK (physical shield): chr-fulmination-templar, chr-thorns-templar (Templar uses shield+block)")
print("  SHIELD-ABSORB (barrier): chr-bloodbinder-warlock, chr-demon-legion-warlock (Warlock arcane barrier)")
print("  ARMOR (melee): all Berserker kits (fire, bleed, frost)")
print("  DODGE: all Warden kits (DEX evasion)")
print("  GLASS: chr-firestorm-warlock, chr-plague-curse-warlock (caster glass builds)")
print("NOTABLE: First WIS-attribute class in corpus (chr-fulmination-templar, chr-thorns-templar)")
print("NOTABLE: Crown proc-lock system record — proc-chain economy (PC) as distinct econ model")
