#!/usr/bin/env python3
"""PoE2 facts generator — megaprobe-2026-07-12 (full schema)
38 rows: 34 positives (6 post-cutoff) + 4 negatives (1 post-cutoff)
Post-cutoff: 0.4/0.5-ancients-only kits with conf<=0.5
"""
import json

OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/megaprobe-2026-07-12/poe2-facts.jsonl"


def pc(v, c, ev): return {"value": v, "conf": round(c, 2), "evidence": ev}
def dc(v, c, ev): return {"value": v, "conf": round(c, 2), "evidence": ev}
def ctrl(ailments, centrality, conf): return {"ailments": ailments, "centrality": centrality, "conf": round(conf, 2)}
def defs(layers, primary, conf): return {"layers": layers, "primary": primary, "conf": round(conf, 2)}
def econ(rv, model, mt, bs, pt, conf):
    return {"resource_verbatim": rv, "model": model, "meter_type": mt, "builder_source": bs, "plain_text": pt, "conf": round(conf, 2)}
def elem(lv, dm, conf): return {"label_verbatim": lv, "damage_mode": dm, "conf": round(conf, 2)}
def mov(verbs, policy, sim, conf): return {"verbs": verbs, "policy_while_casting": policy, "skill_is_movement": sim, "conf": round(conf, 2)}
def pfx(av, ac, ae, rv, rc, re, tv, tc, te, ampv, ampc, ampe, pxv, pxc, pxe, cv, cc, ce):
    return {
        "attr":       pc(av, ac, ae),
        "range":      pc(rv, rc, re),
        "tempo":      pc(tv, tc, te),
        "amp":        pc(ampv, ampc, ampe),
        "proxy":      pc(pxv, pxc, pxe),
        "commitment": pc(cv, cc, ce),
    }


RECORDS = []

# ── POSITIVES ────────────────────────────────────────────────────────────────

# 1. poe2-lightning-arrow-deadeye
RECORDS.append({
    "kit_id": "poe2-lightning-arrow-deadeye", "folk_name": "Lightning Arrow Deadeye", "game": "poe2",
    "status": "positive", "atlas_key": "DRHFSI",
    "delivery": dc("projectile", 0.90, "Fires arrows that chain lightning between targets; projectile delivery confirmed"),
    "footprint": dc("chain-hop", 0.88, "Atlas geo=chain; lightning chains hop between targets; chain-hop footprint"),
    "geo_text": "Deadeye fires Lightning Arrow that hits primary target and chains lightning to additional nearby enemies. Projectile multiplication nodes increase arrow count, creating a spreading chain network across packs.",
    "control": ctrl(["shock"], "rider", 0.82),
    "defense": defs(["evasion", "dodge"], "evasion", 0.85),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Mana spend per shot. High attack speed enables rapid shots. Deadeye nodes provide additional projectiles at no extra cost.", 0.85),
    "element": elem("Lightning", "hit", 0.90),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.90, "Ranger/Deadeye is DEX-primary; bow attacks scale DEX",
        "ranged", 0.92, "Bow attack; R=ranged confirmed unambiguously",
        "high", 0.88, "High attack tempo: rapid arrow volleys at high attack speed; H=high confirmed",
        "flat", 0.82, "Flat lightning damage per chain; no spike model; F=flat confirmed",
        "solo", 0.88, "No proxy; player fires own arrows; S=solo confirmed",
        "instant", 0.92, "Instant bow fire; no wind-up"),
    "mechanics_notes": "prov=kb. mech_note: 'Chaining lightning arrows with Deadeye projectile multiplication — PoE2's static-striker archetype.' Chain-hop footprint is the core mechanic. PoE2 Deadeye: ascendancy specializes in projectile multiplication and movement speed. Era spans 0.1 through 0.5-ancients with conf=0.85 — well-documented baseline in training, later-era patches may have balance-changed specifics.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 2. poe2-ice-strike-invoker
RECORDS.append({
    "kit_id": "poe2-ice-strike-invoker", "folk_name": "Ice Strike Invoker", "game": "poe2",
    "status": "positive", "atlas_key": "DMHFSI",
    "delivery": dc("at-target", 0.88, "Quarterstaff cold flurry delivers at-target melee hits; heavy shatter hit at frozen targets"),
    "footprint": dc("small-radius", 0.85, "Melee flurry hits within close quarterstaff range; geo=small-AOE confirmed"),
    "geo_text": "Invoker executes quarterstaff cold flurry that freezes packs on rapid hits. A heavy follow-up attack SHATTERS frozen enemies for multiplied physical-cold burst. Two-phase: freeze → shatter.",
    "control": ctrl(["freeze", "chill"], "core", 0.88),
    "defense": defs(["evasion", "energy-shield"], "evasion", 0.82),
    "economy": econ("Mana + Combo Points", "meter", "combo", "quarterstaff hits generate combo points",
                    "Monk combat generates Combo Points (3-point system). Finisher attacks spend accumulated combo for powered effects. Mana funds each cast.", 0.82),
    "element": elem("Cold", "hit", 0.90),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": pfx(
        "DEX", 0.88, "Monk is DEX-primary; quarterstaff scaling DEX confirmed",
        "melee", 0.92, "Quarterstaff melee; M=melee confirmed",
        "high", 0.88, "High flurry cadence; freeze requires rapid hit buildup; H=high confirmed",
        "flat", 0.82, "Flat cold damage per hit; shatter is a conditional multiplier, not an amp spike; F=flat confirmed",
        "solo", 0.90, "No proxy; Monk attacks directly; S=solo confirmed",
        "instant", 0.90, "Instant quarterstaff flurry hits"),
    "mechanics_notes": "prov=kb. mech_note: 'Quarterstaff cold flurry freezes packs, then heavy hits SHATTER the frozen — PoE2's Monk freeze identity kit since 0.1.' Freeze=core: shatter = the damage payoff for the freeze buildup. Combo system: Monk PoE2-specific; 3 combo points build up on basic attacks, spent on power moves.",
    "era_confirmed": ["0.1", "0.2-dawn"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 3. poe2-tempest-flurry
RECORDS.append({
    "kit_id": "poe2-tempest-flurry", "folk_name": "Tempest Flurry Monk", "game": "poe2",
    "status": "positive", "atlas_key": "DMHFSI",
    "delivery": dc("at-target", 0.85, "Lightning quarterstaff flurry delivers rapid at-target melee hits; final combo hit erupts in a burst"),
    "footprint": dc("small-radius", 0.82, "Flurry covers small-radius melee range; final eruption hit extends slightly"),
    "geo_text": "Monk executes a multi-hit quarterstaff flurry with a rhythm-building cadence. The final hit of the combo chain erupts in a lightning burst. The rhythm pattern (fast-fast-fast-ERUPT) is the core loop.",
    "control": ctrl(["shock"], "rider", 0.75),
    "defense": defs(["evasion", "energy-shield"], "evasion", 0.82),
    "economy": econ("Mana + Combo Points", "meter", "combo", "quarterstaff hits generate combo points",
                    "Same Monk combo system as Ice Strike Invoker; Mana per cast + Combo Points from hits.", 0.80),
    "element": elem("Lightning", "hit", 0.88),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": pfx(
        "DEX", 0.88, "Monk DEX-primary confirmed",
        "melee", 0.90, "Quarterstaff melee confirmed",
        "high", 0.90, "High tempo flurry; H=high confirmed by rapid-hit rhythm mechanic",
        "flat", 0.80, "Flat lightning per hit; eruption is a consistent finale, not unpredictable spike; F=flat confirmed",
        "solo", 0.90, "No proxy; solo confirmed",
        "instant", 0.90, "Instant flurry hits; no wind-up"),
    "mechanics_notes": "prov=kb. mech_note: 'Lightning quarterstaff flurry whose final combo hit erupts — the rhythm-melee build since beta.' Spans 0.1 through 0.5-ancients — long-lived Monk identity. Same prefix as poe2-ice-strike-invoker (DMHFSI); distinguished by element (Lightning vs Cold) and control (shock vs freeze).",
    "era_confirmed": ["0.1", "0.2-dawn", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 4. poe2-howa-invoker
RECORDS.append({
    "kit_id": "poe2-howa-invoker", "folk_name": "HoWA Invoker", "game": "poe2",
    "status": "positive", "atlas_key": "DMHVSI",
    "delivery": dc("at-target", 0.83, "HoWA converts INT+DEX to melee damage; delivery is at-target melee via the empowered quarterstaff"),
    "footprint": dc("small-radius", 0.80, "Melee quarterstaff range; small-radius confirmed"),
    "geo_text": "Hand of Wisdom and Action converts stacked Intelligence and Dexterity directly into melee lightning damage per hit. The Invoker stacks all three primary attributes to maximize the per-hit conversion. Variable amp (V) reflects the attribute-dependent damage output variance.",
    "control": ctrl(["shock"], "rider", 0.72),
    "defense": defs(["evasion", "energy-shield"], "evasion", 0.80),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Mana spend per attack. Damage scales from attribute investment, not skill ranks.", 0.80),
    "element": elem("Lightning (converted from attribute stacking)", "hit", 0.85),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.85, "Monk/Invoker DEX-primary; HoWA requires DEX stacking alongside INT",
        "melee", 0.90, "Quarterstaff melee confirmed",
        "high", 0.85, "High attack cadence; H=high confirmed",
        "variable", 0.78, "V=variable amp: damage varies with attribute stack composition; V confirmed over F",
        "solo", 0.90, "No proxy; S=solo confirmed",
        "instant", 0.90, "Instant melee strikes"),
    "mechanics_notes": "prov=kb. mech_note: 'Hand of Wisdom and Action converts stacked Intelligence and Dexterity directly into melee lightning damage per hit.' The unique weapon HoWA is the build-enabling item. V=variable amp reflects attribute-stack variance (diff INT:DEX ratios produce different damage curves). Control=rider (shock from lightning hits, not core identity).",
    "era_confirmed": ["0.1", "0.2-dawn"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; unique item HoWA is the rank-anchor",
    "sources_used": ["kb"],
})

# 5. poe2-acolyte-darkness
RECORDS.append({
    "kit_id": "poe2-acolyte-darkness", "folk_name": "Darkness Acolyte", "game": "poe2",
    "status": "positive", "atlas_key": "DMHFSI",
    "delivery": dc("at-target", 0.83, "Chaos Monk delivers at-target melee strikes powered by Waking Dream darkness resource"),
    "footprint": dc("small-radius", 0.80, "Melee quarterstaff strikes at close range"),
    "geo_text": "Chaos Monk who trades Spirit for the Waking Dream darkness resource. Darkness charges enable enhanced melee strikes and chaos skill effects. The Acolyte converts spirit reservation into a darkness-powered combat engine.",
    "control": ctrl(["chaos-debuff", "darkness-stacks"], "core", 0.75),
    "defense": defs(["evasion", "energy-shield"], "evasion", 0.80),
    "economy": econ("Waking Dream (Darkness)", "meter", "n/a", "Spirit converted to Darkness charges",
                    "Acolyte trades Spirit reservation for Waking Dream charges (darkness resource). Darkness charges power chaos-enhanced attacks. Novel resource unique to this ascendancy path.", 0.75),
    "element": elem("Chaos", "hit", 0.82),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.85, "Monk base class DEX-primary; Acolyte is a Monk ascendancy path",
        "melee", 0.88, "Melee quarterstaff attacks; M=melee confirmed",
        "high", 0.82, "High melee tempo; H=high confirmed",
        "flat", 0.80, "Flat chaos damage per hit; F=flat confirmed",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "instant", 0.88, "Instant melee strikes"),
    "mechanics_notes": "prov=kb. mech_note: 'Chaos monk who trades spirit for the Waking Dream darkness resource, converting [Spirit] into chaos-skill powered attacks.' Era=0.1;0.2-dawn only — earlier PoE2 version before the Monk ascendancy paths were further developed. The 'Acolyte of Chayula' path with Waking Dream is the Chaos Monk archetype.",
    "era_confirmed": ["0.1", "0.2-dawn"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 6. poe2-rake-ritualist
RECORDS.append({
    "kit_id": "poe2-rake-ritualist", "folk_name": "Bleed Ritualist", "game": "poe2",
    "status": "positive", "atlas_key": "DMLFSI",
    "delivery": dc("at-target", 0.83, "Rake executes a dash-slash to target; melee delivery at the dash destination"),
    "footprint": dc("point", 0.80, "Single-target dash-to-slash; atlas geo=single confirmed; point footprint"),
    "geo_text": "Rake's dash-slash movement attack lands on the target position, stacking aggravated bleeds on impact. The Ritualist ascendancy amplifies blood mechanics to multiply bleed stacks per hit. Point-delivery, high bleed accumulation per dash.",
    "control": ctrl(["bleed"], "core", 0.88),
    "defense": defs(["evasion", "hp-stack"], "evasion", 0.78),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Mana spend per Rake dash. Multiple dash-slashes stack bleed rapidly.", 0.80),
    "element": elem("Physical / Bleed", "dot", 0.85),
    "movement": mov(["dash-to-target"], "rooted", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.85, "Ranger-class Ritualist is DEX-primary (Pathfinder/Ritualist ascendancy tree)",
        "melee", 0.82, "Rake is a melee dash; M=melee confirmed",
        "low", 0.80, "L=low tempo: deliberate single-target dash cadence; not rapid-fire; L confirmed",
        "flat", 0.82, "Flat bleed application per dash; each bleed stack adds flat DoT; F=flat confirmed",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "instant", 0.88, "Instant dash-slash; no wind-up"),
    "mechanics_notes": "prov=kb. mech_note: 'Rake dash-slash stacks aggravated bleeds while Ritualist blood mechanics multiply the bleed count per dash.' damage_mode=dot (bleed is the primary damage, not initial hit). The Ritualist ascendancy is the bleed-specialist path. Movement verb: 'dash-to-target' (Rake dashes to the target, not a self-movement skill). Era=0.2-dawn;0.3-edict only — may not persist to later patches.",
    "era_confirmed": ["0.2-dawn", "0.3-edict"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 7. poe2-tempest-bell
RECORDS.append({
    "kit_id": "poe2-tempest-bell", "folk_name": "Tempest Bell Monk", "game": "poe2",
    "status": "positive", "atlas_key": "DMMSLI",
    "delivery": dc("at-target", 0.83, "Bell placed at location; strikes to the bell deliver its damage pulse; at-target delivery mediated through bell proxy"),
    "footprint": dc("small-radius", 0.80, "Bell pulse area is small-radius around bell position; atlas geo=small-AOE confirmed"),
    "geo_text": "Combo Points summon a Tempest Bell at a target position. Every attack that physically strikes the Bell RINGS it, pulsing lightning damage in a small area. The bell-ringing loop: place bell → attack bell → pulse → attack bell → pulse.",
    "control": ctrl(["shock", "stun"], "rider", 0.75),
    "defense": defs(["evasion", "energy-shield"], "evasion", 0.80),
    "economy": econ("Combo Points + Mana", "meter", "combo", "Combo Points accumulated from hits; spent to summon Bell",
                    "Bell summoned using accumulated Combo Points (Monk system). Subsequent bell-striking is a regular attack (Mana cost). The Bell itself is the light proxy.", 0.80),
    "element": elem("Lightning / Physical", "hit", 0.82),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.88, "Monk DEX-primary confirmed",
        "melee", 0.85, "Monk attacks bell at melee range; M=melee confirmed",
        "med", 0.80, "M=med tempo: bell-placement rhythm is deliberate; not as rapid as flurry; M confirmed",
        "spiky", 0.80, "S=spiky: bell ring creates burst pulses per strike; distinct spike events; S=spiky confirmed over F",
        "light", 0.82, "L=light: bell is a placed light-proxy; player still attacks to ring it; L=light confirmed",
        "instant", 0.88, "Bell placement instant via combo spend; strikes instant"),
    "mechanics_notes": "prov=kb. mech_note: 'Combo points SUMMON a bell; every attack that strikes the bell RINGS it, pulsing damage in a radius.' Long-lived kit: 0.1 through 0.5-ancients. Light proxy: bell is a placed stationary object struck by the player — between 'at-target' (player decides where to place) and 'at-target' (player attacks it). proxy=light because bell amplifies player attacks but player must manually ring it.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 8. poe2-galvanic-shards
RECORDS.append({
    "kit_id": "poe2-galvanic-shards", "folk_name": "Galvanic Shards Merc", "game": "poe2",
    "status": "positive", "atlas_key": "DRHFSI",
    "delivery": dc("projectile", 0.88, "Fires multiple lightning shotgun rounds that fork into shard sprays; projectile delivery in wide spread"),
    "footprint": dc("cone", 0.85, "Shards fan out in a cone from firing point; shotgun-spread cone footprint; atlas geo=multi-spawn captured as cone spread"),
    "geo_text": "Mercenary fires Galvanic Shards: multiple lightning rounds that spawn additional shard projectiles on fork. The spread covers a wide cone, clearing whole screens at close-medium range. 0.1 EA launch meta kit.",
    "control": ctrl(["shock"], "rider", 0.80),
    "defense": defs(["evasion", "armor"], "evasion", 0.80),
    "economy": econ("Mana + Ammo", "spend+ammo", "n/a", "n/a",
                    "Mana cost per volley. Crossbow has ammo mechanic in PoE2 (load bolts before firing). Galvanic Shards loads and fires rapidly.", 0.75),
    "element": elem("Lightning", "hit", 0.88),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.88, "Mercenary DEX-primary; crossbow scaling DEX",
        "ranged", 0.92, "Crossbow ranged attack; R=ranged confirmed",
        "high", 0.88, "High attack speed with rapid reload; H=high confirmed",
        "flat", 0.82, "Flat lightning damage per shard; F=flat confirmed",
        "solo", 0.88, "No proxy; player fires; S=solo confirmed",
        "instant", 0.90, "Instant crossbow fire (pre-loaded ammo)"),
    "mechanics_notes": "prov=kb. mech_note: 'Lightning shotgun rounds fork into shard sprays that clear whole screens — the 0.1 launch Mercenary top-tier build.' Era=0.1 ONLY — this was the launch-meta build; later patches may have nerfed or restructured it. Crossbow ammo: PoE2 Mercenary loads crossbow bolts (ammo types) before firing; different bolt types change behavior.",
    "era_confirmed": ["0.1"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 9. poe2-poison-pathfinder
RECORDS.append({
    "kit_id": "poe2-poison-pathfinder", "folk_name": "Poison Pathfinder", "game": "poe2",
    "status": "positive", "atlas_key": "DRLFSI",
    "delivery": dc("projectile", 0.85, "Poisonburst Arrow fires a projectile; detonates to apply poison AOE; projectile delivery"),
    "footprint": dc("small-radius", 0.82, "Poison explosion covers small-radius at impact; geo=small-AOE confirmed"),
    "geo_text": "Pathfinder stacks Poison magnitude through Poisonburst Arrow and Overwhelming Toxicity nodes. Each arrow strike applies heavy poison stacks; the buildup accelerates via Pathfinder's Flask + Poison scaling passives.",
    "control": ctrl(["poison", "slow"], "core", 0.85),
    "defense": defs(["evasion", "flask"], "evasion", 0.82),
    "economy": econ("Mana + Flask Charges", "spend", "n/a", "flask charges regenerate over time and on kill",
                    "Mana spend per arrow. Flask charge system (Pathfinder specialty): generates extra flask charges on kill, enabling near-permanent flask uptime. Flask effects power Poison scaling.", 0.80),
    "element": elem("Chaos / Poison", "dot", 0.88),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.90, "Ranger/Pathfinder DEX-primary; bow scaling DEX",
        "ranged", 0.92, "Bow ranged attack; R=ranged confirmed",
        "low", 0.82, "L=low tempo: deliberate single-shot poison application; each arrow stacks; not rapid-fire volley; L confirmed",
        "flat", 0.82, "Flat poison magnitude per stack; cumulative DoT is flat per-tick; F=flat confirmed",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "instant", 0.90, "Instant bow fire"),
    "mechanics_notes": "prov=kb. mech_note: 'Poison magnitude stacking through Poisonburst Arrow and Overwhelming Toxicity, scaling toward [DoT] cap.' damage_mode=dot (poison is the damage, not initial hit). Pathfinder: PoE2 ranger ascendancy specializing in flasks and poison. Era=0.1 through 0.4 — sustained meta presence.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 10. poe2-supporting-fire
RECORDS.append({
    "kit_id": "poe2-supporting-fire", "folk_name": "Supporting Fire Tactician", "game": "poe2",
    "status": "positive", "atlas_key": "DRMFLI",
    "delivery": dc("at-target", 0.78, "Banner-and-volley: marked zones receive automatic covering fire; at-target delivery to banner zone positions"),
    "footprint": dc("large-zone", 0.80, "Banner zones cover large area; covering fire saturates the zone; atlas geo=large-AOE confirmed"),
    "geo_text": "Tactician places banners marking zones; allies or enemies within the zone receive automatic covering fire from the Tactician's position. A zone-control and suppression pattern — the banner defines the large-zone footprint.",
    "control": ctrl(["slow", "knockback"], "rider", 0.68),
    "defense": defs(["evasion", "armor"], "evasion", 0.75),
    "economy": econ("Mana + Banner Charges", "spend", "n/a", "Banner placement has a charge/cooldown system",
                    "Mana spend for volley attacks. Banner placement uses a charge system (place banners, then fire into banner zones). Tactician is Mercenary support ascendancy.", 0.70),
    "element": elem("Physical / Lightning", "hit", 0.75),
    "movement": mov([], "rooted", False, 0.72),
    "prefix_claims": pfx(
        "DEX", 0.85, "Mercenary DEX-primary; Tactician is Mercenary support ascendancy",
        "ranged", 0.88, "Ranged covering fire; R=ranged confirmed",
        "med", 0.75, "M=med tempo: banner placement cadence is deliberate; covering fire is automatic but moderate rate; M confirmed",
        "flat", 0.75, "Flat damage covering fire; F=flat confirmed",
        "light", 0.78, "L=light proxy: banner placement acts as a light proxy that directs fire; banner is placed stationary guide; L=light confirmed",
        "instant", 0.82, "Instant banner placement"),
    "mechanics_notes": "prov=kb. mech_note: 'Tactician banner-and-volley kit where marked zones get automatic covering fire — the squad-tactics archetype.' conf=0.70 reflects moderate training coverage. Era=0.2-dawn through 0.5-ancients — emerged post-launch. Light proxy: banners are zone-markers (light proxy type — they direct fire rather than deal damage directly). Support-existence C2: Tactician is the closest thing to a support kit in PoE2 corpus but it's primarily self-buffing, not pure party support.",
    "era_confirmed": ["0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 11. poe2-gas-arrow-ignite
RECORDS.append({
    "kit_id": "poe2-gas-arrow-ignite", "folk_name": "Gas Arrow Detonation", "game": "poe2",
    "status": "positive", "atlas_key": "DRMSSI",
    "delivery": dc("projectile", 0.85, "Arrow projectile places gas cloud; any fire source detonates it; projectile delivery for cloud placement"),
    "footprint": dc("large-zone", 0.85, "Gas cloud explosion covers large AoE; screen-clearing detonation; atlas geo=large-AOE confirmed"),
    "geo_text": "Ranger fires a Gas Arrow that deposits a poison/chaos gas cloud at target. Any fire damage source ignites the cloud, triggering a screen-clearing detonation. Two-stage: place cloud → ignite for explosion.",
    "control": ctrl(["poison", "ignite"], "core", 0.85),
    "defense": defs(["evasion", "flask"], "evasion", 0.80),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Two-Mana cycle: Gas Arrow (cloud placement) + ignite source (fire arrow/skill). Each cloud costs Mana to place; ignition source may be a separate cast.", 0.80),
    "element": elem("Chaos / Fire (hybrid: poison gas + fire ignition)", "dot", 0.82),
    "movement": mov([], "full-move", False, 0.80),
    "prefix_claims": pfx(
        "DEX", 0.88, "Ranger DEX-primary; bow scaling DEX",
        "ranged", 0.90, "Bow ranged cloud placement; R=ranged confirmed",
        "med", 0.80, "M=med tempo: two-stage cycle (place cloud + ignite); moderate cadence; M confirmed",
        "spiky", 0.82, "S=spiky: detonation produces burst damage spike; S confirmed over F",
        "solo", 0.88, "No proxy; player controls both stages; S=solo confirmed",
        "instant", 0.88, "Instant arrow fire for cloud placement"),
    "mechanics_notes": "prov=kb. mech_note: 'Lay a poison gas cloud, then IGNITE it with any fire source for a screen-clearing detonation.' damage_mode=dot (poison gas + ignite both produce DoT damage on detonation). Two-delivery sequence: Gas Arrow (projectile/large-zone) + ignite source. Era=0.1 through 0.3-edict.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 12. poe2-witchhunter-grenades
RECORDS.append({
    "kit_id": "poe2-witchhunter-grenades", "folk_name": "Grenadier Witchhunter", "game": "poe2",
    "status": "positive", "atlas_key": "DRMSSI",
    "delivery": dc("projectile", 0.85, "Grenades lobbed as projectiles to target positions; timed fuse detonation"),
    "footprint": dc("large-zone", 0.83, "Grenade explosion covers large AoE; cluster grenades expand zone further; atlas geo=large-AOE confirmed"),
    "geo_text": "Witchhunter lobs timed grenades (cluster, flash, oil types) at target positions. Fuse timing rewards pre-stacking debuffs before detonation. A kill-zone setup archetype — lay grenades, then trigger the zone.",
    "control": ctrl(["stun", "ignite", "blind"], "rider", 0.75),
    "defense": defs(["evasion", "armor"], "evasion", 0.78),
    "economy": econ("Grenades (Ammo)", "ammo", "n/a", "grenade stock is limited per encounter; replenished on kill or time",
                    "Witchhunter uses Grenade ammo charges — a limited stock that refills over time or on kill. Different grenade types (cluster, flash, oil) have separate stocks.", 0.75),
    "element": elem("Physical / Fire", "hit", 0.80),
    "movement": mov([], "full-move", False, 0.80),
    "prefix_claims": pfx(
        "DEX", 0.85, "Mercenary/Witchhunter DEX-primary",
        "ranged", 0.88, "Grenade throw is ranged; R=ranged confirmed",
        "med", 0.80, "M=med tempo: deliberate grenade placement cadence; not rapid-fire; M confirmed",
        "spiky", 0.82, "S=spiky: grenade detonation creates burst damage; pre-stacking rewards the spike; S confirmed",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "instant", 0.88, "Instant grenade throw"),
    "mechanics_notes": "prov=kb. mech_note: 'Lob timed grenades — cluster, flash, oil — whose fuses reward pre-stacking a kill-zone.' Era=0.1 through 0.5-ancients — sustained Mercenary identity. Same DRMSSI prefix as poe2-gas-arrow-ignite (both are ranged/med/spiky Ranger-class builds); distinguished by proxy type and economy model.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 13. poe2-infernal-legion
RECORDS.append({
    "kit_id": "poe2-infernal-legion", "folk_name": "Infernal Legion Minions", "game": "poe2",
    "status": "positive", "atlas_key": "IMMFHI",
    "delivery": dc("at-target", 0.83, "Self-immolating minions radiate fire to nearby enemies; minions are the delivery vehicle"),
    "footprint": dc("small-radius", 0.80, "Each burning minion covers small-radius fire aura around itself; multiple minions = multi-point coverage"),
    "geo_text": "Infernal Legion support gem sets own minions on fire — they self-immolate while radiating fire damage to all nearby enemies. The minions' burning deaths become the damage source. A slow-burn proxy suicide mechanic.",
    "control": ctrl(["ignite"], "rider", 0.75),
    "defense": defs(["minion-shield", "energy-shield"], "minion-shield", 0.80),
    "economy": econ("Spirit", "reserve", "n/a", "Spirit reserves pay persistent minion upkeep",
                    "PoE2 Spirit resource: reserved permanently for each active minion. Infernalist class has enhanced Spirit capacity. Minions are persistent Spirit investments.", 0.82),
    "element": elem("Fire", "dot", 0.88),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": pfx(
        "INT", 0.88, "Witch/Infernalist INT-primary; minion scaling via INT",
        "mid", 0.75, "Mid-range characterization: minions engage at mid-distance from player; D=mid approximate",
        "med", 0.80, "M=med tempo: minions attack at moderate cadence; M confirmed",
        "flat", 0.80, "Flat fire DoT per burning minion tick; F=flat confirmed",
        "heavy", 0.88, "Minions ARE the damage; player deals no direct damage; H=heavy proxy confirmed",
        "instant", 0.88, "Minion summon instant"),
    "mechanics_notes": "prov=kb. mech_note: 'Support gem sets your OWN minions on fire — they burn themselves down while radiating fire damage.' Era=0.2-dawn through 0.4. Spirit economy: PoE2's new persistent reservation resource replacing PoE1 mana reservation. damage_mode=dot (fire burning is the primary damage). Infernalist ascendancy: Witch subclass specializing in fire/demon minion mechanics.",
    "era_confirmed": ["0.2-dawn", "0.3-edict", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 14. poe2-cof-comet
RECORDS.append({
    "kit_id": "poe2-cof-comet", "folk_name": "Cast on Freeze Comet", "game": "poe2",
    "status": "positive", "atlas_key": "IRHSSI",
    "delivery": dc("at-target", 0.85, "Comet falls on frozen target position; at-target delivery triggered by freeze proc"),
    "footprint": dc("large-zone", 0.83, "Comet impact AoE is large-zone; meteor-grade splash; atlas geo=large-AOE confirmed"),
    "geo_text": "Cast-on-Freeze meta gem triggers Comet automatically whenever an enemy is Frozen. Freeze buildup via Cold spells fills the trigger threshold, causing meteor-grade Comets to rain on frozen targets. Proc loop: cast cold → freeze → Comet auto-fires.",
    "control": ctrl(["freeze", "chill"], "core", 0.90),
    "defense": defs(["energy-shield"], "energy-shield", 0.85),
    "economy": econ("Mana", "proc", "n/a", "Freeze trigger auto-fires Comet at no additional Mana cost",
                    "Two-layer economy: primary cold skill costs Mana; Comet fires automatically on freeze proc (free). The proc chain is the power engine.", 0.82),
    "element": elem("Cold (Comet)", "hit", 0.88),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": pfx(
        "INT", 0.90, "Sorceress/Stormweaver INT-primary; cold spell scaling INT",
        "ranged", 0.85, "Ranged cold spell delivery; R=ranged confirmed",
        "high", 0.85, "H=high: proc chain fires Comets rapidly at high freeze rate; H confirmed",
        "spiky", 0.88, "S=spiky: each Comet is a meteor burst spike; proc-chain creates repeated spiky events; S confirmed",
        "solo", 0.90, "No proxy; S=solo confirmed",
        "instant", 0.90, "Comet auto-fires instantly on freeze trigger"),
    "mechanics_notes": "prov=kb. mech_note: 'Freeze buildup auto-triggers meteor-grade Comets through the Cast-on-Freeze meta-gem.' Era=0.1;0.4 (absent from 0.2/0.3 eras in corpus — may indicate this build was nerfed then re-emerged). Control=core: freeze is the trigger and prerequisite, not a rider ailment. Cast-on-Freeze is PoE2's new version of CoC (Cast on Crit) — a trigger gem that procs a linked spell on event.",
    "era_confirmed": ["0.1", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 15. poe2-demon-form
RECORDS.append({
    "kit_id": "poe2-demon-form", "folk_name": "Demon Form Infernalist", "game": "poe2",
    "status": "positive", "atlas_key": "IRHVSI",
    "delivery": dc("self-origin", 0.83, "Demon Form transformation changes the player body; primary delivery is self-origin (the form radiates fire skills)"),
    "footprint": dc("large-zone", 0.80, "Demon form fire skills cover large zones; atlas geo=large-AOE confirmed for the form's primary attacks"),
    "geo_text": "Infernalist transforms into a Demon — a different body with its own skill economy and fire-focused powers. The form increases fire power and grants unique demon skills at the cost of Life over time. A transformation-based large-zone fire presence.",
    "control": ctrl(["ignite"], "rider", 0.72),
    "defense": defs(["energy-shield", "self-cost"], "energy-shield", 0.78),
    "economy": econ("Spirit + Life (form drain)", "self-cost", "n/a", "Demon Form uses Spirit and drains Life while active",
                    "Infernalist's Demon Form activates via Spirit reservation and drains Life while active. The form has its own skill economy. Self-cost + Spirit = dual resource pressure.", 0.75),
    "element": elem("Fire", "hit+dot", 0.85),
    "movement": mov([], "full-move", False, 0.80),
    "prefix_claims": pfx(
        "INT", 0.88, "Witch/Infernalist INT-primary; fire magic scaling INT",
        "ranged", 0.80, "Demon form uses ranged fire skills; R=ranged confirmed",
        "high", 0.80, "H=high: demon form attacks at high tempo; H confirmed",
        "variable", 0.75, "V=variable: demon form skill output varies by active demon skills; V=variable captures the shifting output",
        "solo", 0.88, "No proxy in demon form; solo confirmed",
        "instant", 0.85, "Transformation triggered instantly"),
    "mechanics_notes": "prov=kb. mech_note: 'Transform into a demon — a DIFFERENT body with its own skill economy — gaining scaled fire power.' Era=0.1;0.2-dawn;0.4. Variable amp (V): the demon form's skill set produces variable output depending on which demon skills are equipped. Self-cost economy parallels LE Reaper Form. Spirit + Life drain = dual resource sacrifice.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 16. poe2-spark-stormweaver
RECORDS.append({
    "kit_id": "poe2-spark-stormweaver", "folk_name": "Spark Stormweaver", "game": "poe2",
    "status": "positive", "atlas_key": "IRHVSI",
    "delivery": dc("projectile", 0.90, "Spark fires multiple bouncing lightning projectiles; projectile delivery confirmed"),
    "footprint": dc("multi-point", 0.88, "Spark projectiles flood corridors and bounce off walls; multi-point coverage across room"),
    "geo_text": "Stormweaver's Spark fills enclosed areas with bouncing lightning projectiles that saturate corridors and open areas. Archmage support scales total damage by unreserved mana, making mana investment = damage scaling.",
    "control": ctrl(["shock"], "rider", 0.80),
    "defense": defs(["energy-shield"], "energy-shield", 0.88),
    "economy": econ("Mana (unreserved = damage)", "spend", "n/a", "n/a",
                    "Mana spend per cast. Archmage scales damage from unreserved mana — keeping mana high is both an economy and a damage investment. Don't reserve mana for auras; keep it unreserved for Archmage bonus.", 0.85),
    "element": elem("Lightning", "hit", 0.90),
    "movement": mov([], "rooted", False, 0.85),
    "prefix_claims": pfx(
        "INT", 0.90, "Sorceress/Stormweaver INT-primary; lightning spell scaling INT",
        "ranged", 0.88, "Ranged lightning projectile; R=ranged confirmed",
        "high", 0.88, "H=high: Spark spam at high cast rate floods room; H confirmed",
        "variable", 0.82, "V=variable: Spark bounces create variable coverage patterns; atlas V confirmed",
        "solo", 0.90, "No proxy; solo confirmed",
        "instant", 0.90, "Instant cast Spark"),
    "mechanics_notes": "prov=kb. mech_note: 'Spark projectiles flood corridors and bounce walls while Archmage scales the damage from unreserved mana.' Era=0.1 through 0.5-ancients — long-lived meta staple. Archmage: PoE2 support gem that converts unreserved mana into spell damage bonus. Same IRHVSI prefix as poe2-demon-form; distinguished by delivery (projectile vs self-origin) and element (Lightning vs Fire).",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 17. poe2-erasure-edc-lich
RECORDS.append({
    "kit_id": "poe2-erasure-edc-lich", "folk_name": "Erasure DoT Contagion Lich", "game": "poe2",
    "status": "positive", "atlas_key": "IRLFSI",
    "delivery": dc("projectile", 0.85, "Essence Drain fires a projectile; Contagion is at-target AOE that spreads; Erasure mechanic chains; primary delivery = projectile (ED)"),
    "footprint": dc("chain-hop", 0.85, "Contagion spreads (chains) the DoT plague to new targets on kill; atlas geo=chain confirmed as chain-hop"),
    "geo_text": "Essence Drain fires a chaos projectile applying heavy DoT. On kill, Contagion auto-spreads the DoT to nearby enemies. The Erasure mechanic amplifies the spread chain via Lich ascendancy bonus. An exponentially spreading plague loop.",
    "control": ctrl(["wither", "chaos-exposure"], "rider", 0.75),
    "defense": defs(["energy-shield", "sustain-leech"], "energy-shield", 0.85),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per ED cast. Contagion spread is free (triggers on kill). The economy scales by DoT efficiency, not cast frequency.", 0.82),
    "element": elem("Chaos", "dot", 0.88),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "INT", 0.88, "Sorceress/Lich INT-primary; chaos DoT scaling INT",
        "ranged", 0.88, "ED is a ranged projectile; R=ranged confirmed",
        "low", 0.82, "L=low tempo: DoT builds don't need frequent casting; single ED application + Contagion spread; L confirmed",
        "flat", 0.82, "Flat DoT per tick; the plague spreads flat damage; F=flat confirmed",
        "solo", 0.88, "No proxy; solo player casts; S=solo confirmed",
        "instant", 0.88, "Instant ED projectile fire"),
    "mechanics_notes": "prov=kb. mech_note: 'The ED-and-Contagion plague loop reborn in PoE2's Lich chassis with the Erasure-[mechanic] amplifying spread.' Era=0.2-dawn through 0.5-ancients. The Lich ascendancy (Sorceress path) enables advanced DoT scaling. Erasure = PoE2-specific mechanic that accelerates Contagion spread. damage_mode=dot (chaos DoT is ALL the damage).",
    "era_confirmed": ["0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 18. poe2-minion-infernalist
RECORDS.append({
    "kit_id": "poe2-minion-infernalist", "folk_name": "Minion Infernalist", "game": "poe2",
    "status": "positive", "atlas_key": "IRMFHI",
    "delivery": dc("at-target", 0.83, "Skeleton warriors and arsonists autonomously attack targets; at-target delivery via minion army"),
    "footprint": dc("small-radius", 0.80, "Individual minion attacks cover small-radius each; collective coverage is distributed"),
    "geo_text": "Infernalist maintains persistent skeleton warriors and arsonist minions paid out of Spirit reservation. The minion army autonomously pursues and attacks. The Infernalist class enables fire-enhanced minion interactions.",
    "control": ctrl(["ignite"], "rider", 0.72),
    "defense": defs(["minion-shield", "energy-shield"], "minion-shield", 0.82),
    "economy": econ("Spirit", "reserve", "n/a", "Spirit permanently reserved per minion type",
                    "Spirit is the persistent reservation resource; each skeleton/arsonist slot costs Spirit to maintain. PoE2 Spirit replaces PoE1 mana reservation for minions.", 0.82),
    "element": elem("Physical / Fire", "hit", 0.80),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": pfx(
        "INT", 0.88, "Witch/Infernalist INT-primary; minion scaling INT",
        "ranged", 0.75, "Player positions at range while minions engage; R=ranged characterizes player positioning; conf MED",
        "med", 0.80, "M=med tempo: minion attack cadence moderate; M confirmed",
        "flat", 0.80, "Flat physical/fire damage per minion hit; F=flat confirmed",
        "heavy", 0.90, "Minions ARE the primary damage; H=heavy proxy confirmed",
        "instant", 0.88, "Minion summon instant"),
    "mechanics_notes": "prov=kb. mech_note: 'Persistent skeleton warriors and arsonists paid for out of the SPIRIT reservation [system].' Era=0.1 through 0.4. Spirit economy confirms PoE2's new resource model. Infernalist: fire-specialty Witch ascendancy whose demon form + minion integration creates the fire-minion archetype.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 19. poe2-blood-mage
RECORDS.append({
    "kit_id": "poe2-blood-mage", "folk_name": "Blood Mage", "game": "poe2",
    "status": "positive", "atlas_key": "IRMSSW",
    "delivery": dc("projectile", 0.80, "Blood Mage casts blood-powered spell projectiles; projectile delivery confirmed; atlas geo=multi-spawn = multiple projectiles"),
    "footprint": dc("multi-point", 0.78, "Multiple blood spell projectiles hit at various points; multi-point footprint"),
    "geo_text": "Blood Mage casts spells that cost Life on top of Mana. Life sacrificed on cast is recovered from kills in bursts. A high-risk, high-recovery loop: each spell costs health, each kill returns it.",
    "control": ctrl(["bleed", "chaos-exposure"], "rider", 0.70),
    "defense": defs(["hp-stack", "self-cost"], "hp-stack", 0.80),
    "economy": econ("Life + Mana", "self-cost", "n/a", "Life recovered from kills",
                    "Blood Mage ascendancy: spells cost Life in addition to Mana. Life-orb recovery on kill returns the spent Life. Sustained play requires steady kill cadence to maintain HP.", 0.82),
    "element": elem("Chaos / Physical", "hit", 0.78),
    "movement": mov([], "rooted", False, 0.78),
    "prefix_claims": pfx(
        "INT", 0.88, "Witch/Blood Mage INT-primary; spell scaling INT",
        "ranged", 0.80, "Ranged spell projectiles; R=ranged confirmed",
        "med", 0.78, "M=med tempo: wind-up spells have deliberate cadence; M confirmed",
        "spiky", 0.78, "S=spiky: blood spells deliver burst damage per cast; S confirmed",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "wind-up", 0.82, "W=wind-up: Blood Mage's signature spells require charge-up before release; W confirmed"),
    "mechanics_notes": "prov=kb. mech_note: 'Casts cost LIFE on top of mana with life-orb recovery from kills — launched as a [risky] playstyle.' Era=0.1 through 0.4. Blood Mage = Witch ascendancy. The self-cost defense (Life as currency) mirrors LE Harvest Lich / D2 Sacrifice patterns across the corpus.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 20. poe2-bonestorm
RECORDS.append({
    "kit_id": "poe2-bonestorm", "folk_name": "Bonestorm", "game": "poe2",
    "status": "positive", "atlas_key": "IRMSSW",
    "delivery": dc("projectile", 0.82, "Bone shards charged then released as barrage of physical projectiles; projectile delivery"),
    "footprint": dc("multi-point", 0.80, "Bone shard barrage sprays multiple projectiles to multiple impact points; atlas geo=multi-spawn confirmed"),
    "geo_text": "Charge a volley of bone shards during wind-up, then release the full barrage simultaneously. The physical-spell crit archetype: bone shard density + crit scaling for burst. A deliberate charge-and-release pattern.",
    "control": ctrl(["bleed"], "rider", 0.68),
    "defense": defs(["energy-shield", "armor"], "energy-shield", 0.78),
    "economy": econ("Mana", "spend", "n/a", "n/a",
                    "Mana spend per Bonestorm cast. Wind-up charges the shard count; longer hold = more shards released.", 0.78),
    "element": elem("Physical", "hit", 0.85),
    "movement": mov([], "rooted", False, 0.80),
    "prefix_claims": pfx(
        "INT", 0.85, "Witch/Blood Mage or Sorceress context; bone-spell is INT-scaling",
        "ranged", 0.80, "Ranged bone shard barrage; R=ranged confirmed",
        "med", 0.78, "M=med tempo: wind-up before each volley moderates cadence; M confirmed",
        "spiky", 0.82, "S=spiky: full volley release creates burst damage spike; S confirmed",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "wind-up", 0.85, "W=wind-up: charge the shard count before release; W confirmed"),
    "mechanics_notes": "prov=kb. mech_note: 'Charge a volley of bone shards, release the barrage — a physical-spell crit chassis.' Era=0.1;0.2-dawn;0.5-ancients (gap in 0.3/0.4 — possibly nerfed then buffed). Same IRMSSW prefix as poe2-blood-mage; distinguished by element (Physical vs Chaos) and identity (crit barrage vs life-cost sustained).",
    "era_confirmed": ["0.1", "0.2-dawn", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 21. poe2-twister
RECORDS.append({
    "kit_id": "poe2-twister", "folk_name": "Twister Spirit Walker", "game": "poe2",
    "status": "positive", "atlas_key": "DDHVLI",
    "delivery": dc("self-origin", 0.80, "Whirling Slash spins off Twister projectiles from player position; self-origin spin generates the twisters"),
    "footprint": dc("multi-point", 0.80, "Twisters bounce along walls to multiple positions; atlas geo=multi-spawn confirmed as multi-point coverage"),
    "geo_text": "Whirling Slash creates spinning Twister projectiles that diverge and bounce along walls, covering the area in wandering vortices. Spirit Walker class enables the Twister generation mechanic through Spirit resource.",
    "control": ctrl(["slow", "knockback"], "rider", 0.68),
    "defense": defs(["evasion"], "evasion", 0.78),
    "economy": econ("Spirit + Mana", "reserve", "n/a", "Spirit enables Twister generation; Mana for the base attack",
                    "Spirit Walker uses Spirit reservation to enable Twister-generation nodes. Mana funds the base Whirling Slash.", 0.72),
    "element": elem("Physical / Lightning (variable)", "hit", 0.75),
    "movement": mov(["whirl"], "full-move", True, 0.78),
    "prefix_claims": pfx(
        "DEX", 0.85, "Monk/Spirit Walker DEX-primary",
        "mid", 0.75, "D=mid: Whirling Slash operates at mid-range; twisters extend further; D=mid for the primary attack",
        "high", 0.80, "H=high: rapid whirl cadence generating twisters; H confirmed",
        "variable", 0.78, "V=variable: twister bounce paths create variable damage distribution; V confirmed",
        "light", 0.78, "L=light: twisters are light-proxy entities that wander autonomously after generation; L confirmed",
        "instant", 0.82, "Whirling Slash instant"),
    "mechanics_notes": "prov=kb. mech_note: 'Whirling Slash spins off wandering TWISTER projectiles that bounce along walls and corners.' Era=0.2-dawn through 0.5-ancients. Spirit Walker: Monk sub-path using Spirit for combat enhancement. skill_is_movement=true for Whirling Slash (it has a directional movement component).",
    "era_confirmed": ["0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 22. poe2-lightning-spear-amazon
RECORDS.append({
    "kit_id": "poe2-lightning-spear-amazon", "folk_name": "Lightning Spear Amazon", "game": "poe2",
    "status": "positive", "atlas_key": "DDHVSI",
    "delivery": dc("projectile", 0.85, "Thrown lightning spear travels as projectile, then forks into bolt cascades on impact"),
    "footprint": dc("chain-hop", 0.82, "Fork cascades hop between targets after spear impact; atlas geo=multi-spawn captured as chain-hop fanout"),
    "geo_text": "Amazon hurls a Lightning Spear that travels to impact and forks into multiple lightning bolt cascades. The elemental crit engine triggers on the fork bolts for explosive damage amplification. A thrown-weapon cascade archetype.",
    "control": ctrl(["shock"], "rider", 0.78),
    "defense": defs(["evasion"], "evasion", 0.80),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Mana spend per throw. Amazon's elemental crit engine scales on fork bolt hits.", 0.80),
    "element": elem("Lightning", "hit", 0.88),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "DEX", 0.88, "Amazon is a DEX-primary class (spear/javelin thrower)",
        "mid", 0.78, "D=mid: thrown spear has mid-range trajectory; D=mid confirmed",
        "high", 0.82, "H=high: rapid spear throw cadence; H confirmed",
        "variable", 0.78, "V=variable: fork bolt cascade patterns create variable hit distribution; V confirmed over F",
        "solo", 0.88, "No proxy; S=solo confirmed",
        "instant", 0.88, "Instant spear throw"),
    "mechanics_notes": "prov=kb. mech_note: 'Thrown lightning spears fork into bolt cascades under Amazon's elemental crit engine.' Era=0.2-dawn;0.3-edict. Amazon: new class in PoE2 (spear-based, D/W hybrid). Elemental crit: PoE2 mechanic where critting with an element triggers a secondary effect (lightning = shock cascades).",
    "era_confirmed": ["0.2-dawn", "0.3-edict"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 23. poe2-warbringer-totems
RECORDS.append({
    "kit_id": "poe2-warbringer-totems", "folk_name": "Ancestral Totem Warrior", "game": "poe2",
    "status": "positive", "atlas_key": "SMLFHI",
    "delivery": dc("at-target", 0.83, "Ancestral totems swing slam attacks at nearby enemies; at-target delivery via placed totem proxy"),
    "footprint": dc("large-zone", 0.83, "Totem slams cover large-zone AoE; atlas geo=large-AOE confirmed"),
    "geo_text": "Warbringer places Ancestral totems that execute massive slam attacks while the Warrior stacks armor into five figures. The totems slam for the Warrior, who provides defensive bulk and support. A slam-proxy + extreme-armor pattern.",
    "control": ctrl(["stun"], "rider", 0.75),
    "defense": defs(["armor", "resist"], "armor", 0.90),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Mana spend per totem placed. Totems persist and slam autonomously.", 0.82),
    "element": elem("Physical", "hit", 0.85),
    "movement": mov([], "full-move", False, 0.85),
    "prefix_claims": pfx(
        "STR", 0.90, "Warrior STR-primary; totem slam scaling STR; S=STR confirmed",
        "melee", 0.85, "Totems perform melee slams; M=melee confirmed",
        "low", 0.82, "L=low tempo: totem slams are deliberate heavy hits at low cadence; L confirmed",
        "flat", 0.82, "Flat physical slam damage; F=flat confirmed",
        "heavy", 0.88, "Totems ARE the primary damage; Warrior is defensive support; H=heavy proxy confirmed",
        "instant", 0.88, "Instant totem placement"),
    "mechanics_notes": "prov=kb. mech_note: 'Ancestral totems swing the slams while the warrior stacks armor into five digits.' Era=0.1 through 0.5-ancients — long-lived Warrior identity. Warbringer: Warrior ascendancy specializing in totems and armor. Extreme armor stacking = defense layer. Heavy proxy: totems do ALL the damage; Warrior is purely a defensive presence.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 24. poe2-titan-hotg
RECORDS.append({
    "kit_id": "poe2-titan-hotg", "folk_name": "Hammer of the Gods Titan", "game": "poe2",
    "status": "positive", "atlas_key": "SMLSSW",
    "delivery": dc("at-target", 0.88, "Hammer of the Gods falls from sky onto targeted position; at-target overhead delivery"),
    "footprint": dc("large-zone", 0.88, "Hammer impact creates large-zone AoE; atlas geo=large-AOE confirmed; 'biggest single-hit' implies large zone"),
    "geo_text": "Titan executes armor-break setup, then calls down the Hammer of the Gods — a colossal hammer falling from above onto a targeted zone for the slowest, most devastating single-hit in PoE2's warrior toolkit.",
    "control": ctrl(["stun", "armor-break"], "core", 0.88),
    "defense": defs(["armor", "resist"], "armor", 0.92),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Mana spend per Hammer activation. Wind-up before release. Armor-break setup is a prerequisite investment.", 0.85),
    "element": elem("Physical", "hit", 0.90),
    "movement": mov([], "rooted", False, 0.82),
    "prefix_claims": pfx(
        "STR", 0.92, "Warrior/Titan STR-primary; HotG is pure Warrior skill scaling STR",
        "melee", 0.88, "Hammer falls at melee/close target range; M=melee confirmed (Titan positions close for the strike)",
        "low", 0.88, "L=low tempo: single colossal strike per long cooldown cycle; L confirmed",
        "spiky", 0.92, "S=spiky: the single Hammer hit IS the damage event; maximum spike; S confirmed",
        "solo", 0.90, "No proxy; S=solo confirmed",
        "wind-up", 0.90, "W=wind-up: Hammer requires wind-up before falling; W confirmed; also armor-break setup is a meta-level wind-up"),
    "mechanics_notes": "prov=kb. mech_note: 'Armor-break setup into the ultimate falling hammer — the slowest, biggest single-hit in PoE2 Warrior toolkit.' Era=0.1 through 0.3-edict. Control=core: armor-break is prerequisite (without fully broken armor, Hammer does less damage). Titan ascendancy: the STR-first Warrior path focused on the highest-impact single hits. This is the PoE2 correlate of D2's Leap Attack barb pattern.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 25. poe2-smith-ignite
RECORDS.append({
    "kit_id": "poe2-smith-ignite", "folk_name": "Smith of Kitava Ignite", "game": "poe2",
    "status": "positive", "atlas_key": "SMLSSW",
    "delivery": dc("at-target", 0.85, "Forge-heated slow slams deliver ignite at target; at-target melee slam delivery"),
    "footprint": dc("large-zone", 0.85, "Large slow slam covers large AoE with fire ignite; atlas geo=large-AOE confirmed"),
    "geo_text": "Smith of Kitava turns weapon heat into scaled ignites off huge slow slams. The forge-ascendancy mechanic: heat up the weapon through crafting/skill interaction, then slam to apply a massive ignite DoT. Walk forward, slam, burn everything.",
    "control": ctrl(["ignite"], "core", 0.88),
    "defense": defs(["armor", "resist", "hp-stack"], "armor", 0.88),
    "economy": econ("Mana + Weapon Heat", "spend", "n/a", "crafting and forge skills generate weapon heat",
                    "Smith of Kitava generates Weapon Heat through specific skills/crafting interactions. Heat is the damage multiplier for ignites. Mana pays per slam. Walk-forward ignite damage applies after slam.", 0.80),
    "element": elem("Fire (Ignite DoT)", "dot", 0.90),
    "movement": mov([], "full-move", False, 0.82),
    "prefix_claims": pfx(
        "STR", 0.90, "Warrior/Smith STR-primary; melee slam scaling STR",
        "melee", 0.88, "Melee slam; M=melee confirmed",
        "low", 0.88, "L=low tempo: slow deliberate slams; L confirmed by 'huge slow slams' mech_note",
        "spiky", 0.88, "S=spiky: each slam delivers high-impact ignite application; S confirmed",
        "solo", 0.90, "No proxy; S=solo confirmed",
        "wind-up", 0.88, "W=wind-up: slow slams have visible wind-up before release; W confirmed"),
    "mechanics_notes": "prov=kb. mech_note: 'The forge-ascendancy turns weapon heat into scaled ignites off huge slow slams — walk-forward damage.' Era=0.2-dawn through 0.5-ancients. damage_mode=dot (ignite is the damage, not the hit). Same SMLSSW prefix as poe2-titan-hotg and poe2-perfect-strike-01 (all STR/melee/low/spiky/solo/wind-up Warriors); distinguished by element (Fire DoT vs Physical hit) and ascendancy.",
    "era_confirmed": ["0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# 26. poe2-gemling-stacker
RECORDS.append({
    "kit_id": "poe2-gemling-stacker", "folk_name": "Gemling Attribute Stacker", "game": "poe2",
    "status": "positive", "atlas_key": "_MHVSI",
    "delivery": dc("at-target", 0.72, "Attribute-stacked melee attacks; delivery is at-target melee; conf MED (archetype-level, not skill-specific)"),
    "footprint": dc("small-radius", 0.70, "Melee range attack footprint; small-radius confirmed; conf MED"),
    "geo_text": "Gemling Legionnaire ascendancy monetizes all three primary attributes simultaneously — every STR, DEX, and INT point feeds damage scaling. The kit's damage is the attribute investment, not any specific skill's design.",
    "control": ctrl([], "none", 0.65),
    "defense": defs(["armor", "energy-shield", "evasion"], "armor", 0.72),
    "economy": econ("Mana", "spend", "n/a", "n/a", "Standard Mana spend; the economy is the attribute investment (not a special resource).", 0.70),
    "element": elem("Variable (all attributes = Physical/Cold/Lightning hybrid)", "hit", 0.68),
    "movement": mov([], "full-move", False, 0.72),
    "prefix_claims": pfx(
        "unknown", 0.62, "Atlas bc6 pos-1 = _ (unknown): Gemling Stacker can be any class; attribute-class-neutral; underscore confirmed",
        "melee", 0.75, "M=melee: attribute stacker typically expressed as melee; M=melee is the corpus characterization",
        "high", 0.72, "H=high: high attack tempo for the attribute-conversion melee kit; H confirmed",
        "variable", 0.70, "V=variable: all three attributes contribute varying damage types; variable amp confirmed",
        "solo", 0.80, "No proxy; solo confirmed",
        "instant", 0.78, "Instant melee attacks"),
    "mechanics_notes": "prov=kb. mech_note: 'The ascendancy monetizes RAW ATTRIBUTES — every point of all three stats feeds damage.' conf=0.68 in atlas reflects archetype-level abstraction (the 'kit' is really a stat-stacking pattern, not a named skill). Underscore attr confirms class-neutral nature. Era=0.1 through 0.5-ancients — persistent attribute stacking archetype. Variable element: STR contributes physical, DEX contributes lightning (via HoWA-like conversion), INT contributes spell damage.",
    "era_confirmed": ["0.1", "0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "NOT APPLICABLE — archetype defined by stat investment, not a rankable skill",
    "sources_used": ["kb"],
})

# 27. poe2-temporalis-blink
RECORDS.append({
    "kit_id": "poe2-temporalis-blink", "folk_name": "Temporalis Blink", "game": "poe2",
    "status": "positive", "atlas_key": "IDHFSI",
    "delivery": dc("self-origin", 0.83, "Blink is a movement skill (teleport); self-origin delivery — the player repositions to a new location"),
    "footprint": dc("point", 0.82, "Teleport to a specific point; point-footprint confirmed; minimal AoE at destination"),
    "geo_text": "The Temporalis unique chest shaves seconds off all skill cooldowns, reducing Blink's cooldown to near-zero (1-2 second cycles). The kit is defined by near-continuous teleportation — using Blink as both mobility and combat tool.",
    "control": ctrl([], "none", 0.70),
    "defense": defs(["energy-shield"], "energy-shield", 0.85),
    "economy": econ("Cooldown (Temporalis-reduced)", "cooldown", "n/a", "n/a",
                    "Temporalis unique reduces ALL cooldowns substantially. Blink's cooldown becomes near-negligible (~1-2s). Mana cost per Blink.", 0.78),
    "element": elem("none (movement utility kit)", "hit", 0.65),
    "movement": mov(["teleport"], "full-move", True, 0.90),
    "prefix_claims": pfx(
        "INT", 0.85, "Sorceress/Witch INT-primary; Blink is a Sorceress/caster movement skill",
        "mid", 0.75, "D=mid: Blink teleports to mid-range target; D=mid characterizes typical blink distance",
        "high", 0.82, "H=high: Temporalis enables near-continuous Blink (high usage rate); H confirmed",
        "flat", 0.72, "F=flat: any damage at Blink destination is flat; but this kit is primarily movement not damage",
        "solo", 0.85, "No proxy; S=solo confirmed",
        "instant", 0.88, "Instant teleport; no wind-up"),
    "mechanics_notes": "prov=kb. mech_note: 'Temporalis shaves seconds off ALL skill cooldowns, turning Blink into near-continuous repositioning.' Era=0.1;0.2-dawn. skill_is_movement=true: Blink IS a movement skill. The build is defined by using Blink offensively (blink into packs, AoE on arrival) or defensively (blink away from danger). Temporalis is a unique item build-enabler. element='none' because the kit identity is movement frequency, not damage type.",
    "era_confirmed": ["0.1", "0.2-dawn"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred; Temporalis unique item is the rank-anchor",
    "sources_used": ["kb"],
})

# 28. poe2-grim-feast
RECORDS.append({
    "kit_id": "poe2-grim-feast", "folk_name": "Grim Feast Overleech", "game": "poe2",
    "status": "positive", "atlas_key": "IMMFSI",
    "delivery": dc("self-origin", 0.78, "Grim Feast is a Spirit-reserved buff that radiates vacuum to nearby remnants; self-origin aura-style delivery"),
    "footprint": dc("small-radius", 0.75, "Life remnant vacuum operates in small-radius around player; geo=small-AOE confirmed"),
    "geo_text": "Grim Feast reserves Spirit to vacuum leftover life remnants (from enemy death) into Energy Shield above maximum (overleech). The archetype is a defensive layer — trading Spirit reservation for a continuously regenerating ES buffer.",
    "control": ctrl([], "none", 0.65),
    "defense": defs(["shield-absorb", "energy-shield", "sustain-leech"], "shield-absorb", 0.85),
    "economy": econ("Spirit (reserved)", "reserve", "n/a", "enemy death drops life remnants that feed overleech",
                    "Spirit reserved for Grim Feast buff. Life remnants dropped by dying enemies are vacuumed and converted to ES overleech. The intake rate scales with kill density.", 0.72),
    "element": elem("none (defensive buff, not a damage skill)", "hit", 0.60),
    "movement": mov([], "full-move", False, 0.80),
    "prefix_claims": pfx(
        "INT", 0.82, "Witch/Sorceress INT-primary; Grim Feast is a caster-class buff",
        "mid", 0.68, "D=mid: archetype characterization; remnant vacuum operates at mid-radius; conf LOW",
        "med", 0.72, "M=med: moderate ES regeneration rate; M confirmed",
        "flat", 0.72, "F=flat: steady ES overleech rate; F confirmed",
        "solo", 0.82, "No proxy; S=solo confirmed",
        "instant", 0.80, "Buff activation instant"),
    "mechanics_notes": "prov=kb. mech_note: 'Spirit-reserved buff that vacuums leftover life remnants into energy shield OVER[leech max].' Era=0.2-dawn through 0.4. conf=0.63 in atlas — lower confidence; this is a defensive buff mechanic more than a named skill-build. Shield-split D1: definitively a Ward/ES overleech kit. element='none' because Grim Feast is purely defensive.",
    "era_confirmed": ["0.2-dawn", "0.3-edict", "0.4"],
    "post_cutoff": False, "dossier_owed": False,
    "rank1_upgrade": "live source verification deferred",
    "sources_used": ["kb"],
})

# ── POST-CUTOFF POSITIVES ────────────────────────────────────────────────────

for pc_kit in [
    {"kit_id": "poe2-spiral-volley", "folk_name": "Spiral Volley", "atlas_key": "DDHFSI",
     "conf": 0.33, "eras": ["0.4", "0.5-ancients"],
     "note": "Spear projectiles on spiraling flight paths, named among 0.4's top-tier archetypes.",
     "del_v": "projectile", "fp_v": "multi-point", "prov": "kb"},
    {"kit_id": "poe2-whirling-assault-ma", "folk_name": "Whirling Assault Martial Artist", "atlas_key": "DMHFLI",
     "conf": 0.37, "eras": ["0.5-ancients"],
     "note": "Hollow Form CLONES cast Whirling Assault for you, bypassing attack restrictions.",
     "del_v": "at-target", "fp_v": "small-radius", "prov": "kb"},
    {"kit_id": "poe2-snipe-mirage-deadeye", "folk_name": "Snipe Mirage Deadeye", "atlas_key": "DRMSLC",
     "conf": 0.47, "eras": ["0.5-ancients"],
     "note": "Snipe's channeled shot one-taps bosses while Mirage Deadeye lets clones continue sniping.",
     "del_v": "projectile", "fp_v": "point", "prov": "kb"},
    {"kit_id": "poe2-walking-calamity", "folk_name": "Walking Calamity Autobomber", "atlas_key": "SMHFSI",
     "conf": 0.37, "eras": ["0.5-ancients"],
     "note": "Walk across map and everything dies automatically — ~20K armor autobomber.",
     "del_v": "self-origin", "fp_v": "small-radius", "prov": "kb"},
    {"kit_id": "poe2-shaman-bear", "folk_name": "Shaman Bear", "atlas_key": "WMHFSI",
     "conf": 0.40, "eras": ["0.4", "0.5-ancients"],
     "note": "Druid shapeshifts into bear — built-in armour tank body, Rampage momentum clear.",
     "del_v": "self-origin", "fp_v": "small-radius", "prov": "kb"},
    {"kit_id": "poe2-archmage-totems", "folk_name": "Archmage Totems Oracle", "atlas_key": "WRMVHI",
     "conf": 0.47, "eras": ["0.5-ancients"],
     "note": "Totems cast mana-scaled spells at NO COST while Oracle chassis enables sustain.",
     "del_v": "at-target", "fp_v": "large-zone", "prov": "kb"},
]:
    RECORDS.append({
        "kit_id": pc_kit["kit_id"], "folk_name": pc_kit["folk_name"], "game": "poe2",
        "status": "positive", "atlas_key": pc_kit["atlas_key"],
        "delivery": dc(pc_kit["del_v"], pc_kit["conf"], f"POST-CUTOFF: inferred from mech_note; live verification required"),
        "footprint": dc(pc_kit["fp_v"], pc_kit["conf"], f"POST-CUTOFF: inferred from atlas geo; live verification required"),
        "geo_text": f"POST-CUTOFF ({'; '.join(pc_kit['eras'])}). " + pc_kit["note"] + " Full spatial characterization deferred to dossier.",
        "control": ctrl([], "unknown", pc_kit["conf"]),
        "defense": defs(["unknown"], "unknown", pc_kit["conf"]),
        "economy": econ("unknown", "unknown", "n/a", "n/a", "POST-CUTOFF: economy deferred", pc_kit["conf"]),
        "element": elem("unknown", "hit", pc_kit["conf"]),
        "movement": mov([], "unknown", False, pc_kit["conf"]),
        "prefix_claims": {
            "attr":       pc("unknown", pc_kit["conf"], f"POST-CUTOFF: atlas bc6 pos-1={pc_kit['atlas_key'][0] if pc_kit['atlas_key'] else '?'}; conf capped"),
            "range":      pc("unknown", pc_kit["conf"], "POST-CUTOFF: conf capped"),
            "tempo":      pc("unknown", pc_kit["conf"], "POST-CUTOFF: conf capped"),
            "amp":        pc("unknown", pc_kit["conf"], "POST-CUTOFF: conf capped"),
            "proxy":      pc("unknown", pc_kit["conf"], "POST-CUTOFF: conf capped"),
            "commitment": pc("unknown", pc_kit["conf"], "POST-CUTOFF: conf capped"),
        },
        "mechanics_notes": f"POST-CUTOFF. prov={pc_kit['prov']}. mech_note ref: '{pc_kit['note']}' Full dossier required.",
        "era_confirmed": pc_kit["eras"],
        "post_cutoff": True, "dossier_owed": True,
        "rank1_upgrade": "DEFERRED — post-cutoff; live source required",
        "sources_used": [pc_kit["prov"] + " (post-cutoff)"],
    })

# ── NEGATIVES ────────────────────────────────────────────────────────────────

NEGATIVES = [
    {
        "kit_id": "poe2-concoction", "folk_name": "Concoction Pathfinder", "game": "poe2",
        "status": "negative", "atlas_key": "DDMFSI",
        "delivery": dc("at-target", 0.82, "Flask-charge throw lands at target; at-target delivery"),
        "footprint": dc("small-radius", 0.78, "Flask explosion at target covers small-radius; atlas geo=small-AOE confirmed"),
        "why_negative": "ported-and-failed: PoE1's Concoction (flask-charge throwing) was ported to PoE2 but flask-charge system changes made the economy non-viable; the build lost its identity in translation",
        "era_span": ["0.2-dawn", "0.3-edict", "0.4", "0.5-ancients"],
        "post_cutoff": False, "dossier_owed": False, "prov": "kb",
        "mech_note": "mech_note: 'PoE1 league-start QUEEN ported to PoE2 and died — flask-charge throwing suffered.' PoE2 flask rework removed the economy that made Concoction work in PoE1.",
    },
    {
        "kit_id": "poe2-chronomancer-01", "folk_name": "Chronomancer (launch)", "game": "poe2",
        "status": "negative", "atlas_key": "IRMVSI",
        "delivery": dc("at-target", 0.70, "Time-manipulation skills target enemies/areas; at-target delivery"),
        "footprint": dc("large-zone", 0.68, "Time-rewind and freeze-time cover large zones; atlas geo=large-AOE confirmed"),
        "why_negative": "failed-meta: time-manipulation ascendancy mechanics (freeze-time, rewind) were too slow and imprecise for PoE2's fast combat loop; never achieved meta tier in 0.1-0.4 era",
        "era_span": ["0.1", "0.2-dawn", "0.3-edict", "0.4"],
        "post_cutoff": False, "dossier_owed": False, "prov": "kb",
        "mech_note": "mech_note: 'Time-manipulation ascendancy whose freeze-time and rewind toys never paid rent at any tier.' The IRMVSI prefix (INT/ranged/med/variable) reflects the multi-tool nature of time skills — variable amp because different time effects produce different damage patterns. conf=0.68.",
    },
    {
        "kit_id": "poe2-wall-of-shields", "folk_name": "Wall of Shields", "game": "poe2",
        "status": "negative", "atlas_key": "SMLFLI",
        "delivery": dc("at-target", 0.37, "POST-CUTOFF: shield array placed at target positions; at-target placement inferred"),
        "footprint": dc("large-zone", 0.37, "POST-CUTOFF: shield-array endgame archetype covers large zone; atlas geo=large-AOE inferred"),
        "why_negative": "POST-CUTOFF + failed-meta: shield-array endgame archetype on 0.5's dead-on-arrival list per mech_note; never achieved viable tier even in its release era",
        "era_span": ["0.3-edict", "0.4"],
        "post_cutoff": True, "dossier_owed": True, "prov": "kb",
        "mech_note": "POST-CUTOFF. mech_note: 'Shield-array endgame archetype named verbatim on 0.5's dead-on-arrival list.' conf=0.37. poe2-wall-of-shields is the unique PoE2 negative AND post-cutoff case — confirmed dead build from a post-training era.",
    },
    {
        "kit_id": "poe2-perfect-strike-01", "folk_name": "Perfect Strike (launch)", "game": "poe2",
        "status": "negative", "atlas_key": "SMLSSW",
        "delivery": dc("at-target", 0.87, "Melee strike at target; at-target confirmed"),
        "footprint": dc("point", 0.85, "Single-target timing-skill hit; atlas geo=single confirmed"),
        "why_negative": "mechanic-too-narrow: Perfect Strike's rhythm-timing bonus (hold to timing window for bonus fire hit) was too small a power premium vs other Warrior skills; community abandoned it quickly after 0.1 launch",
        "era_span": ["0.1"],
        "post_cutoff": False, "dossier_owed": False, "prov": "kb",
        "mech_note": "mech_note: 'Hold to a PERFECT-TIMING window for a bonus fire hit — a rhythm-game flourish [without sufficient power premium].' conf=0.87 (well-known launch skill). Era=0.1 only — immediately recognized as weak. Same SMLSSW prefix as poe2-titan-hotg and poe2-smith-ignite — all are STR/melee/low/spiky/solo/wind-up Warriors; Perfect Strike was the under-powered member of that prefix family.",
    },
]

# ── OUTPUT ───────────────────────────────────────────────────────────────────

all_records = RECORDS + NEGATIVES

with open(OUT, "w") as f:
    for rec in all_records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

pos_count = sum(1 for r in all_records if r["status"] == "positive")
neg_count = sum(1 for r in all_records if r["status"] == "negative")
pc_count  = sum(1 for r in all_records if r.get("post_cutoff"))
print(f"PoE2: {len(all_records)} records | pos={pos_count} neg={neg_count} post-cutoff={pc_count}")
print(f"Written: {OUT}")

# Directed sweep notes
print()
print("=== DIRECTED SWEEP RESULTS (PoE2) ===")
print("C2 (support-existence): CLOSEST candidate = poe2-supporting-fire (Tactician banner-volley)")
print("  However Tactician primarily self-buffs + provides covering fire, not pure party healer.")
print("  C2 finding for PoE2: NO pure solo-context support kit. Tactician is zone-control/self-buff.")
print("G2 (line-vs-projectile): No true-line/beam delivery found in PoE2 corpus.")
print("  Chains: lightning-arrow (chain-hop), erasure-edc-lich (chain-hop)")
print("  Directional spreads: galvanic-shards (cone), twister (multi-point bounce)")
print("D1 (shield-split): ES kits: spark-stormweaver, cof-comet, demon-form,")
print("  erasure-edc-lich, minion-infernalist, blood-mage, bonestorm, grim-feast,")
print("  temporalis-blink. Armor: titan-hotg, smith-ignite, warbringer-totems, walking-calamity.")
print("  Evasion: all Ranger+Monk+Merc kits. Mixed ES+Eva: ice-strike, howa, tempest-flurry.")
