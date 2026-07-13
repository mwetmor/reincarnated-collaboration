"""
gen-vs-facts.py
Mega-probe Unit A — Vampire Survivors (vs) — 24 records
22 positive / 2 negative / 1 post-cutoff (vs-1.13-14-2025+ ONLY)
Full schema (6 fact families per positive kit; light schema for negatives).

VS notes:
- Attr slot always '_' (no STR/DEX/INT mapping; VS uses passive stat arrays)
- Commit always 'I' (instant — all weapons auto-fire on their timer)
- Movement: all player-verb (player moves freely; weapons auto-fire independently)
- Element: most VS weapons = n/a or generic; noted where explicit
- Economy: RC=recipe/evolution, HV=harvest, RS=reserve/aura, SP=spend/auto, DR=draft
"""
import json
from pathlib import Path

OUT = Path("agentic_orchestration/legolas/research/megaprobe-2026-07-12/vs-facts.jsonl")

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

# VS movement: always full-move (auto-fire fires while player walks freely)
VS_MOV = mov(["auto-fire-while-moving"], "full-move", False, 0.95)

KITS = []

# ── 1. vs-holy-wand ───────────────────────────────────────────────────────────
# Magic Wand evolution: fires at nearest enemy, no cooldown post-evo
# Atlas: _RHFSI = _, ranged, high, flat, solo, instant; RC economy
KITS.append({
    "kit_id": "vs-holy-wand",
    "folk_name": "Holy Wand (Magic Wand evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RHFSI-PNDD-RC-__-~~",
    "delivery": dc("projectile", 0.92, "projectile fires at nearest enemy automatically; zero cooldown after evolution = continuous fire"),
    "footprint": dc("point", 0.90, "single-target homing projectile; one enemy per projectile"),
    "geo_text": "Holy Wand: evolved Magic Wand removes all cooldown. Fires auto-homing projectiles at the nearest enemy in a continuous stream. Aim is entirely automated — the player never directs targeting.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("evolution recipe (Magic Wand max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Requires Magic Wand at max level plus specific passive item to unlock evolution. Weapon then fires automatically at no per-shot resource cost — the evolution is the investment.", 0.88),
    "element": elem("n/a (holy/arcane)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank — no STR/DEX/INT mapping"),
        pc("R", 0.90, "ranged projectile; auto-targets nearest enemy"),
        pc("H", 0.90, "high tempo — no cooldown = maximum fire rate"),
        pc("F", 0.88, "flat per-projectile damage; consistent amplitude"),
        pc("S", 0.88, "solo; no proxy element"),
        pc("I", 0.92, "instant auto-fire trigger per timer tick"),
    ),
    "mechanics_notes": "Aim-automation as defining identity: 'fires at nearest enemy with no cooldown after evolution.' The player's only strategic input is positioning relative to enemy clusters. RC (recipe) economy = evolution recipe system. The zero-cooldown post-evo differentiates from base Magic Wand.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Holy Wand inherits Magic Wand stat boosts; additional projectile count from passive items (Spellbinder, etc.).",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 2. vs-thousand-edge ───────────────────────────────────────────────────────
# Knife evolution: endless wall of daggers in FACED direction (player movement direction)
# Atlas: _RHFSI-PNDD = ranged, high, flat, solo; RC
KITS.append({
    "kit_id": "vs-thousand-edge",
    "folk_name": "Thousand Edge (Knife evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RHFSI-PNDD-RC-__-~~",
    "delivery": dc("projectile", 0.90, "rapid-fire daggers fired in the direction the player is facing/moving; not a sustained beam — individual projectiles"),
    "footprint": dc("multi-point", 0.85, "wall of simultaneous daggers fills the faced direction; many projectiles = multi-point coverage in a forward arc"),
    "geo_text": "Thousand Edge fires an unceasing volley of daggers in the direction the player faces (movement direction). Player movement direction IS the aiming system. Daggers are individual projectiles creating a dense forward wall — not a beam, but effective as a lane-deny.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("evolution recipe (Knife max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Knife at max + spinach passive = Thousand Edge. No per-shot cost; auto-fires at maximum rate after evolution.", 0.88),
    "element": elem("n/a (physical)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("R", 0.88, "ranged projectile volley in faced direction"),
        pc("H", 0.88, "high tempo — maximum fire rate, no cooldown"),
        pc("F", 0.85, "flat per-dagger; wall density = many flat-amplitude hits"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.90, "instant auto-fire per tick"),
    ),
    "mechanics_notes": "Movement-direction aiming: the player WALKS into enemies to direct the dagger wall. 'The one weapon family where the player's movement direction IS the aiming system' per mech_note. G2: projectile-spam in faced direction, NOT a true beam — individual daggers, not sustained. Effective lane-deny without being beam delivery.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Thousand Edge inherits Knife stats; increased projectile count via cooldown reduction items.",
    "sources_used": ["cg (character guide)", "eg (evolution guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 3. vs-je-ne-viv ───────────────────────────────────────────────────────────
# Insatiable character: damage scales with MAGNET and GREED stats (pickup economy stats)
# Atlas: _DHFLI = _, mid, high, flat, light, instant; HV economy
KITS.append({
    "kit_id": "vs-je-ne-viv",
    "folk_name": "Je-Ne-Viv (Insatiable)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DHFLI-PLDM-HV-__-~~",
    "delivery": dc("at-target", 0.80, "large-AOE attack drops at or near player position targeting nearby enemies"),
    "footprint": dc("large-zone", 0.80, "large-AOE zone around player from Insatiable character's weapon pattern"),
    "geo_text": "Je-Ne-Viv's weapon converts MAGNET (pickup range) and GREED (gold) stats directly into weapon damage. Pickup-economy stats become the scaling axis — the more you prioritize vacuum economy, the harder you hit. Large-AOE zone damage.",
    "control": ctrl([], "none", 0.75),
    "defense": defs(["glass"], "glass", 0.75),
    "economy": econ("harvest-stats-as-damage (MAGNET+GREED scale weapon)", "harvest", "n/a", "n/a",
                    "HV = harvest. Damage scaled by MAGNET stat (pickup range) and GREED stat (gold multiplier) — the pickup economy stats are converted into damage scaling. Unusual: non-combat stats drive combat output.", 0.78),
    "element": elem("n/a", "hit", 0.72),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.78, "mid-range AOE zone; not melee contact, not long-range projectile"),
        pc("H", 0.78, "high tempo auto-fire"),
        pc("F", 0.75, "flat zone damage; harvest-stats-as-damage is a flat scaling multiplier"),
        pc("L", 0.78, "light-proxy from Insatiable character's kit interaction"),
        pc("I", 0.80, "instant auto-fire"),
    ),
    "mechanics_notes": "Harvest-stats-as-damage: the defining economy innovation in the corpus for pickup-scaling. MAGNET = how wide you vacuum gems; GREED = gold multiplier. Both are typically utility stats in VS; Je-Ne-Viv converts them to attack scaling. DLC-era character; s11 changes unknown.",
    "era_confirmed": "vs-dlc-era",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Stacking MAGNET and GREED items (Attract Orb, Stone Mask etc.) increases weapon damage scaling.",
    "sources_used": ["vv (Vampire Survivors video/wiki)", "pg (player guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 4. vs-death-spiral ────────────────────────────────────────────────────────
# Axe evolution: axes become a full rotating spiral sweeping outward from body
# Atlas: _DHFSI = _, mid, high, flat, solo, instant; RC
KITS.append({
    "kit_id": "vs-death-spiral",
    "folk_name": "Death Spiral (Axe evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DHFSI-PMDD-RC-__-~~",
    "delivery": dc("self-origin", 0.88, "rotating axe spiral emanates from player body outward; orbit delivery"),
    "footprint": dc("ring", 0.88, "spiral/ring footprint expanding outward from body; axes rotate in expanding orbit pattern"),
    "geo_text": "Death Spiral: evolved Axe promotes the arc-throw into a full rotating spiral that sweeps outward continuously from the player body. The entire screen-adjacent ring is covered by rotating axe projectiles.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("evolution recipe (Axe max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Axe at max + Candelabrador = Death Spiral. Auto-fires continuously post-evolution.", 0.88),
    "element": elem("n/a (physical)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.85, "mid-range orbit — expanding ring covers mid-range around body"),
        pc("H", 0.85, "high-tempo rotation; axes sweep continuously"),
        pc("F", 0.82, "flat per-axe-hit; consistent orbit damage"),
        pc("S", 0.85, "solo; self-contained orbit"),
        pc("I", 0.88, "instant orbit continuous auto-fire"),
    ),
    "mechanics_notes": "Orbit delivery: Death Spiral promoted from projectile-arc to orbit. The 'arc-throw promoted to whole-ring orbit' per mech_note. Death Spiral + Red Death character = iconic combo (Red Death inherits Death Spiral). Ring footprint distinguishes from simple radius.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Death Spiral inherits Axe stat boosts; Area and Cooldown items expand ring radius and rotation speed.",
    "sources_used": ["cg (character guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 5. vs-red-death ───────────────────────────────────────────────────────────
# Mask of Red Death: kill the Reaper → become the Reaper; unlock-trophy character
# Atlas: _DHFSI = _, mid, high, flat, solo, instant; SP economy (unlock-trophy)
KITS.append({
    "kit_id": "vs-red-death",
    "folk_name": "Red Death / Mask of the Red Death",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DHFSI-PMDD-SP-__-~~",
    "delivery": dc("self-origin", 0.85, "Death Spiral orbiting axes radiate from Red Death body; aura-adjacent orbit delivery"),
    "footprint": dc("ring", 0.85, "rotating orbit ring of Death Spiral axes around player body"),
    "geo_text": "Red Death character: unlock requires slaying the Grim Reaper. Starts with Death Spiral (rotating axe spiral) and 100% move speed. The archetype is the Reaper: orbit ring of axes at maximum speed. 'Kill the Reaper, BECOME the Reaper.'",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("unlock-trophy (slay Reaper secret unlock)", "other", "n/a", "n/a",
                    "SP base (Death Spiral auto-fires continuously). The economy is the UNLOCK: slaying the Grim Reaper during a run unlocks this character permanently. No per-shot resource in-run.", 0.85),
    "element": elem("n/a (death/chaos)", "hit", 0.80),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.82, "mid-range orbit ring"),
        pc("H", 0.85, "high tempo + 100% move speed bonus"),
        pc("F", 0.82, "flat orbit damage per axe-hit"),
        pc("S", 0.82, "solo; orbit is self-contained"),
        pc("I", 0.85, "instant continuous auto-fire"),
    ),
    "mechanics_notes": "Unlock-trophy economy: the investment is slaying the Reaper during a run (a feat requiring a full-length build). Once unlocked, Red Death is a permanent selectable character. Death Spiral synergy = starting weapon. 100% move speed is the 'Reaper speed' narrative flavor made mechanical.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Red Death inherits Death Spiral upgrades; 100% move speed base adds to all movement bonuses.",
    "sources_used": ["cg (character guide)", "dd (data dump)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 6. vs-heaven-sword ────────────────────────────────────────────────────────
# Cross evolution: cross flies out and boomerangs back through everything twice (lane geometry)
# Atlas: _DHFSI = _, mid, high, flat, solo, instant; RC
KITS.append({
    "kit_id": "vs-heaven-sword",
    "folk_name": "Heaven Sword (Cross evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DHFSI-PNDD-RC-__-~~",
    "delivery": dc("projectile", 0.88, "cross projectile flies out, boomerangs back; two linear passes through enemy cluster on one throw"),
    "footprint": dc("lane", 0.82, "forward flight path + return path = linear lane cut twice; piercing both ways through enemy line"),
    "geo_text": "Heaven Sword: cross boomerangs out and returns, piercing enemies on both the outward and return paths. The return path is the key differentiation — same linear lane, hit twice. Range and pierce create a double-lane cut.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("evolution recipe (Cross max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Cross at max + Clover = Heaven Sword. Return-path is part of the evolved weapon identity.", 0.88),
    "element": elem("n/a (holy)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.85, "mid-range outward arc, returns to caster"),
        pc("H", 0.85, "high tempo — cross fires frequently"),
        pc("F", 0.82, "flat per-pass damage; each pass is a consistent hit"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant auto-fire throw"),
    ),
    "mechanics_notes": "Return-path = lane geometry: the boomerang creates a linear pierce both out and back. NOT a true beam (no sustained channel), but the footprint=lane due to double linear traversal. 'Return-path archetype in its purest form' per mech_note.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Heaven Sword inherits Cross stat boosts; Area items extend boomerang range.",
    "sources_used": ["eg (evolution guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 7. vs-la-borra ────────────────────────────────────────────────────────────
# Santa Water evolution: growing holy puddles that follow the player
# Atlas: _DLFLI = _, mid, low, flat, light, instant; RC
KITS.append({
    "kit_id": "vs-la-borra",
    "folk_name": "La Borra (Santa Water evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DLFLI-PLDM-RC-__-~~",
    "delivery": dc("self-origin", 0.85, "holy puddles spawn near player and follow; mobile zone-paint that tracks player position"),
    "footprint": dc("large-zone", 0.85, "puddles grow over time into large persistent damage zones; mobile zone-paint"),
    "geo_text": "La Borra: evolved Santa Water drops holy puddles that GROW in radius and FOLLOW the player. Zone-paint becomes mobile: puddles persist and expand while trailing behind movement. The area grows as combat continues.",
    "control": ctrl(["slow"], "rider", 0.78),
    "defense": defs(["glass"], "glass", 0.78),
    "economy": econ("evolution recipe (Santa Water max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Santa Water max + Attracter = La Borra. Puddles auto-spawn at no per-puddle cost after evolution.", 0.85),
    "element": elem("n/a (holy)", "hit", 0.80),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.82, "mid-range mobile zone trailing player"),
        pc("L", 0.82, "low tempo — puddle spawn cadence is slow but zones persist and grow"),
        pc("F", 0.80, "flat zone damage; consistent per-tick damage in zone"),
        pc("L", 0.80, "light-proxy — multiple puddles trailing = light zone coverage"),
        pc("I", 0.85, "instant puddle spawn on auto-fire timer"),
    ),
    "mechanics_notes": "Mobile zone-paint: 'evolved Santa Water converts zone-paint into a mobile puddle trail' per mech_note. Light-proxy from multiple co-existing puddles. The low tempo + large-zone growth = area denial over time rather than burst. Growing zone radius is the evolved identity.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "La Borra inherits Santa Water stats; Area items increase puddle growth radius.",
    "sources_used": ["sg (survival-game guide)", "eg (evolution guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 8. vs-infinite-corridor-crimson-shroud ────────────────────────────────────
# Death-kill tech: Clock Lancet+ring = Infinite Corridor (halves HP) + Crimson Shroud (damage cap)
# Atlas: _DLSSI = _, mid, low, spiky, solo, instant; RC+relic-gated
# G2 FLAG: TRUE BEAM (Clock Lancet freeze beams = sustained directional beam delivery)
KITS.append({
    "kit_id": "vs-infinite-corridor-crimson-shroud",
    "folk_name": "Infinite Corridor + Crimson Shroud (Death-kill tech)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DLSSI-PNCM-RC-__-~~",
    "delivery": dc("beam", 0.85, "Clock Lancet fires sustained freeze beams across screen; TRUE BEAM delivery — sustained directional energy lines"),
    "footprint": dc("lane", 0.85, "freeze beams traverse screen in fixed lanes; G2 true lane/beam confirmed"),
    "geo_text": "Infinite Corridor (evolved Clock Lancet): fires sustained freeze beams that HALVE enemy HP on contact. Crimson Shroud (relic): caps incoming damage to prevent death. The combination enables killing the Reaper (normally immortal) — the death-kill tech combo. Relic-gated: requires finding the relics in-run.",
    "control": ctrl(["freeze", "stop"], "core", 0.85),
    "defense": defs(["shield-absorb"], "shield-absorb", 0.88),
    "economy": econ("relic-gated recipe (Clock Lancet + Laurel max + specific relics)", "recipe", "n/a", "n/a",
                    "RC + relic-gated: requires Clock Lancet AND Silver Ring AND Gold Ring at max level, PLUS the Yellow Sign relic. Crimson Shroud requires Laurel + Metaglio relics. Two separate evolution recipes in one build. Relic-gated = requires specific found relics.", 0.85),
    "element": elem("n/a (time/magic)", "hit", 0.80),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.82, "mid-range freeze beam traverses mid-screen"),
        pc("L", 0.82, "low tempo — beams fire slowly but halve HP each hit"),
        pc("S", 0.85, "spiky amplitude — halving enemy HP is a single massive spike per hit"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant auto-fire per beam cycle"),
    ),
    "mechanics_notes": "G2 flag: TRUE BEAM — Clock Lancet fires sustained directional freeze beams across screen lanes. Lane footprint confirmed. Death-kill tech: Infinite Corridor's HP-halving effect + Crimson Shroud's damage cap = can kill the otherwise-unkillable Reaper. Corpus records this as the canonical death-kill combo.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Infinite Corridor: higher tiers increase beam count and frequency. Crimson Shroud: higher tiers lower the damage cap threshold.",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 9. vs-gatti-amari — NEGATIVE ──────────────────────────────────────────────
# Negative: summoned cats eat your pickups and occasionally attack enemies
KITS.append({
    "kit_id": "vs-gatti-amari",
    "folk_name": "Gatti Amari (as drafted)",
    "game": "vs",
    "status": "negative",
    "atlas_key": "_DLVHI-PNDD-HV-__-~~",
    "delivery": dc("other", 0.80, "chaotic wandering cat summons; anti-harvest delivery (they consume your pickups)"),
    "footprint": dc("other", 0.80, "no consistent spatial footprint; cats wander independently"),
    "why_negative": "Anti-harvest: cats eat gem pickups (your primary resource); weapon mechanics are adversarial to the player's own economy. Not a build-enabler — it is a build-disabler. Negative kit status: documented as anti-pattern in the arsenal.",
    "era_span": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "prov": "kb",
    "mech_note": "Summoned cats wander, eat your pickups, and occasionally attack enemies. Arsenal chaos archetype. Anti-harvest economy: HV here = reverse-harvest (consuming player pickups). Noted as notable because it proves the VS engine can express deliberately anti-synergistic weapons.",
})

# ── 10. vs-vandalier ──────────────────────────────────────────────────────────
# Peachone + Ebony Wings union: two birds fuse into one, frees a slot
# Atlas: _DMFLI = _, mid, med, flat, light, instant; RC union
KITS.append({
    "kit_id": "vs-vandalier",
    "folk_name": "Vandalier (Peachone+Ebony Wings union)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DMFLI-PSDD-RC-__-~~",
    "delivery": dc("projectile", 0.85, "bird summons fire circular bomb projectiles in patterns; union doubles bomb density"),
    "footprint": dc("small-radius", 0.85, "bomb projectiles detonate in small-radius AOE on impact"),
    "geo_text": "Vandalier: Peachone + Ebony Wings union. Both bird weapons fuse into one, freeing a weapon slot and doubling bomb output in one combined bird. Two weapon inputs → one output + slot liberation. Circular bomb patterns circle and fire.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("union recipe (Peachone + Ebony Wings max both)", "recipe", "n/a", "n/a",
                    "RC = union-recipe. Both bird weapons must be maxed to unlock union. Fuses into a single weapon and frees the second weapon slot — slot liberation as economy bonus.", 0.85),
    "element": elem("n/a (physical/bomb)", "hit", 0.80),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.82, "mid-range bomb projection patterns"),
        pc("M", 0.82, "medium tempo — bird orbit + bomb fire cadence"),
        pc("F", 0.82, "flat per-bomb AOE damage"),
        pc("L", 0.80, "light-proxy from orbiting bird summon pair merged into one"),
        pc("I", 0.85, "instant bomb release on auto-fire timer"),
    ),
    "mechanics_notes": "Union-recipe system: not a standard evolution (passive item) but a weapon-pair fusion (two weapons combine). 'TWO weapons fuse into one' — slot liberation is the economy benefit unique to union recipes vs standard evolutions. Peachone+Ebony Wings is the founding union pair.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Vandalier inherits stats from both bird weapons; bomb patterns scale with Area/Power items.",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 11. vs-vlad-dracula ───────────────────────────────────────────────────────
# Castlevania DLC secret character: Vlad Tepes Dracula
# Atlas: _DMSSI = _, mid, med, spiky, solo, instant; SP unlock-trophy
KITS.append({
    "kit_id": "vs-vlad-dracula",
    "folk_name": "Vlad Tepes Dracula",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DMSSI-PLDM-SP-__-~~",
    "delivery": dc("at-target", 0.75, "Castlevania DLC character with large-AOE vampire attacks; mid-range zone delivery"),
    "footprint": dc("large-zone", 0.75, "large-AOE zone attacks from Dracula's arsenal; DLC character"),
    "geo_text": "Vlad Tepes Dracula from the Castlevania DLC. Secret unlock character ranked among the best in the game. Large-AOE vampire weaponry. Spiky amplitude — his kit has high-burst capability rather than flat sustained DPS.",
    "control": ctrl(["drain"], "rider", 0.70),
    "defense": defs(["sustain-leech"], "sustain-leech", 0.72),
    "economy": econ("unlock-trophy (Castlevania DLC secret unlock)", "other", "n/a", "n/a",
                    "SP auto-fire base. Unlock is a secret-completion achievement in the Castlevania DLC. Post-unlock, character auto-fires like all VS characters.", 0.72),
    "element": elem("n/a (vampire/dark)", "hybrid", 0.70),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("D", 0.72, "mid-range; DLC character weapon range; reduced conf due to DLC provenance"),
        pc("M", 0.70, "medium tempo auto-fire"),
        pc("S", 0.70, "spiky amplitude — Dracula builds around high-burst vampire hits"),
        pc("S", 0.72, "solo; no proxy element"),
        pc("I", 0.75, "instant auto-fire"),
    ),
    "mechanics_notes": "DLC character (Castlevania / Operation Guns DLC). Secret unlock. Provenance = VV (video/wiki), limited documentation. Reduced conf for DLC content. Era: dlc-era + s11-2025+ (s11 changes unknown). 'The Castlevania DLC's hidden lord' per mech_note.",
    "era_confirmed": "vs-dlc-era",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Dracula character inherits Castlevania DLC weapon scaling; specific unlock conditions in DLC.",
    "sources_used": ["vv (Vampire Survivors video/wiki)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 12. vs-out-of-bounds-freeze ───────────────────────────────────────────────
# Arcana: Out of Bounds makes freeze trigger explosions — POST-CUTOFF (vs-1.13-14-2025+ ONLY)
KITS.append({
    "kit_id": "vs-out-of-bounds-freeze",
    "folk_name": "Out of Bounds freeze build",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_DMSSI-PSMM-SP-__-~~",
    "delivery": dc("at-target", 0.45, "freeze effect triggers explosion at enemy position; post-cutoff conf capped"),
    "footprint": dc("small-radius", 0.45, "explosion on freeze = small-radius detonation at frozen enemy; post-cutoff conf capped"),
    "geo_text": "Out of Bounds arcana makes FREEZE trigger explosions. Weapons that merely chill become detonators — control converted into burst damage engine. Arcana-authored stack grammar: the arcana investment transforms the nature of another weapon's control effect.",
    "control": ctrl(["freeze", "explosion"], "core", 0.42),
    "defense": defs(["glass"], "glass", 0.42),
    "economy": econ("arcana-authored stack (arcana slot investment)", "other", "n/a", "n/a",
                    "Arcana system: Out of Bounds is an arcana card that modifies freeze behavior globally. The investment is the arcana slot. Post-cutoff specifics unknown.", 0.42),
    "element": elem("n/a (cold+explosion)", "hybrid", 0.42),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank; post-cutoff conf capped"),
        pc("D", 0.45, "mid-range freeze + explosion; post-cutoff conf capped"),
        pc("M", 0.42, "medium tempo; post-cutoff conf capped"),
        pc("S", 0.42, "spiky — freeze+explode = high burst per freeze application; post-cutoff conf capped"),
        pc("S", 0.42, "solo; post-cutoff conf capped"),
        pc("I", 0.45, "instant auto-fire; post-cutoff conf capped"),
    ),
    "mechanics_notes": "POST-CUTOFF: vs-1.13-14-2025+ is the ONLY era; all conf capped ≤0.50. Arcana system (added to VS in updates) = a meta-layer of strategic choices that modify run mechanics. Out of Bounds arcana converts control (freeze) into a damage-delivery trigger. Arcana-authored-stack economy.",
    "era_confirmed": "vs-1.13-14-2025+",
    "post_cutoff": True,
    "dossier_owed": True,
    "rank1_upgrade": "Arcana slot investment in Out of Bounds; explosion damage scales with Power stat (post-cutoff, unconfirmed).",
    "sources_used": ["sg (survival-game guide, s11 content)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 13. vs-bloody-tear ────────────────────────────────────────────────────────
# Whip evolution: heals on hit — the founding VS evolution and genre anchor
# Atlas: _MHFSI = _, melee, high, flat, solo, instant; RC
KITS.append({
    "kit_id": "vs-bloody-tear",
    "folk_name": "Bloody Tear (Whip evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_MHFSI-PSDM-RC-__-~~",
    "delivery": dc("self-origin", 0.92, "whip lash sweeps from player body in a melee arc; sustain-on-hit delivery"),
    "footprint": dc("small-radius", 0.90, "whip arc covers small-radius cone in front of player"),
    "geo_text": "Bloody Tear (Whip + Hollow Heart): the whip lash HEALS ON HIT. The founding VS evolution — every guide introduces evolution with this example. Melee arc sweeps in front of the player. Sustain from combat output is the identity.",
    "control": ctrl([], "none", 0.85),
    "defense": defs(["sustain-leech"], "sustain-leech", 0.92),
    "economy": econ("evolution recipe (Whip max + Hollow Heart max)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Whip + Hollow Heart = Bloody Tear. Heal-on-hit is the evolved mechanic; no per-hit resource cost.", 0.90),
    "element": elem("n/a (physical/blood)", "hit", 0.85),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("M", 0.92, "melee arc; whip is the archetypal melee weapon in VS"),
        pc("H", 0.90, "high tempo — whip has one of the highest natural attack rates"),
        pc("F", 0.88, "flat per-hit damage; consistent sustain per-hit"),
        pc("S", 0.88, "solo; no proxy element"),
        pc("I", 0.92, "instant auto-fire lash per timer tick"),
    ),
    "mechanics_notes": "'The genre anchor's founding evolution' per mech_note. Heal-on-hit = the survival mechanic that makes VS's auto-attack-while-walking design viable at early difficulty. D1 sweep: SUSTAIN-LEECH primary. Multiple eras (1.0, dlc, 1.13) confirm longevity as a foundational evolution.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Bloody Tear inherits Whip and Hollow Heart stats; heal-per-hit scales with Power.",
    "sources_used": ["sg (survival-game guide)", "cg (character guide)", "eg (evolution guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 14. vs-unholy-vespers ─────────────────────────────────────────────────────
# King Bible evolution: bibles orbit the body permanently — never drops
# Atlas: _MHFSI = _, melee, high, flat, solo, instant; RC
KITS.append({
    "kit_id": "vs-unholy-vespers",
    "folk_name": "Unholy Vespers (King Bible evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_MHFSI-PSMM-RC-__-~~",
    "delivery": dc("orbit", 0.92, "bibles orbit the player body permanently after evolution; continuous orbit delivery"),
    "footprint": dc("ring", 0.92, "orbit ring around player; 'the ring never closes, the wall never drops'"),
    "geo_text": "Unholy Vespers: evolved King Bible makes bibles orbit the body permanently — no wave limit, no downtime. The ring of bibles is an impenetrable melee-orbit wall. 'The ring never closes, the wall never drops' = the canonical orbit archetype in VS.",
    "control": ctrl(["stagger"], "rider", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("evolution recipe (King Bible max + Spellbinder)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. King Bible max + Spellbinder = Unholy Vespers. Orbit is perpetual post-evolution; no cooldown.", 0.90),
    "element": elem("n/a (holy/dark)", "hit", 0.85),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("M", 0.92, "melee orbit ring; contact at melee range"),
        pc("H", 0.90, "high tempo — continuous orbit hits at high rate"),
        pc("F", 0.88, "flat orbit damage per bible contact"),
        pc("S", 0.85, "solo; orbit is self-contained wall"),
        pc("I", 0.92, "instant continuous orbit; no cast"),
    ),
    "mechanics_notes": "Orbit delivery (distinct from projectile and self-origin): bibles perpetually circle the player body at fixed radius. Ring footprint. 'The ring never closes' = no arc-gap in the orbit. The canonical orbit weapon for the VS corpus.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Unholy Vespers: more bibles added via Area/Cooldown; orbit speed increases.",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 15. vs-soul-eater ─────────────────────────────────────────────────────────
# Garlic evolution: body-hugging damage aura with lifesteal
# Atlas: _MHFSI = _, melee, high, flat, solo, instant; RS (reserve/aura)
KITS.append({
    "kit_id": "vs-soul-eater",
    "folk_name": "Soul Eater (Garlic evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_MHFSI-PSMM-RS-__-~~",
    "delivery": dc("aura-pulse", 0.90, "body-hugging aura pulses damage continuously around player; garlic aura delivery"),
    "footprint": dc("small-radius", 0.92, "body-adjacent small-radius aura; enemies must be nearly touching player to take damage"),
    "geo_text": "Soul Eater (Garlic evolution): a body-hugging damage aura that pulses around the player continuously. 'The garlic aura — a body-hugging damage shell that carries the first twenty minutes.' Evolved version adds lifesteal from enemies damaged in the aura.",
    "control": ctrl(["slow"], "rider", 0.82),
    "defense": defs(["sustain-leech"], "sustain-leech", 0.85),
    "economy": econ("aura-passive reserve (always-on damage field)", "reserve", "n/a", "n/a",
                    "RS = reserve/aura-passive. Soul Eater is always active — no per-pulse cost. The reserve cost is the slot this weapon occupies. Evolution requires Garlic max + Pummarola.", 0.88),
    "element": elem("n/a (garlic/aura)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("M", 0.92, "melee-adjacent body aura; requires enemies to nearly contact player"),
        pc("H", 0.90, "high-frequency pulse; garlic aura hits very frequently"),
        pc("F", 0.88, "flat aura damage per pulse; consistent body-contact DPS"),
        pc("S", 0.88, "solo; self-contained aura"),
        pc("I", 0.90, "instant continuous aura; no cast"),
    ),
    "mechanics_notes": "Aura-pulse delivery: body-hugging continuous pulse (not a projectile, not at-target — the aura IS the weapon surface). RS economy (reserve/aura-passive): always-on slot investment. The early-game survival staple. Lifesteal from soul-eating is the evolved mechanic vs base Garlic.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Soul Eater inherits Garlic + Pummarola stats; Area items expand aura radius.",
    "sources_used": ["eg (evolution guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 16. vs-fuwalafuwaloo ──────────────────────────────────────────────────────
# Vento Sacro + Bloody Tear union: recursive union (evolved weapon + base weapon)
# Atlas: _MHSSI = _, melee, high, spiky, solo, instant; RC union-recursive
KITS.append({
    "kit_id": "vs-fuwalafuwaloo",
    "folk_name": "Fuwalafuwaloo (Vento Sacro+Bloody Tear union)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_MHSSI-PSDM-RC-__-~~",
    "delivery": dc("self-origin", 0.85, "whirlwind slash zone around player from fused Vento Sacro + Bloody Tear; melee spin AOE"),
    "footprint": dc("small-radius", 0.85, "whirlwind slash small-radius around player body; melee spin zone"),
    "geo_text": "Fuwalafuwaloo: Vento Sacro (an EVOLVED weapon) unions with Bloody Tear (also an evolved weapon from Whip). An EVOLVED weapon unioning with an evolved weapon — 'recursive union.' Whirlwind slashes with heal-on-hit. Double-evolution chain into a union.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["sustain-leech"], "sustain-leech", 0.85),
    "economy": econ("union-recipe-recursive (two evolved weapons combine)", "recipe", "n/a", "n/a",
                    "RC = union-recipe. UNUSUAL: this union requires two ALREADY-EVOLVED weapons (Vento Sacro + Bloody Tear), not base+passive. Recursive evolution chain: evolve both separately, then union them. Highest investment path in VS.", 0.85),
    "element": elem("n/a (wind/blood hybrid)", "hybrid", 0.80),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("M", 0.85, "melee whirlwind slash zone"),
        pc("H", 0.85, "high tempo whirlwind hits"),
        pc("S", 0.82, "spiky amplitude — whirlwind has burst damage character"),
        pc("S", 0.82, "solo; self-contained"),
        pc("I", 0.85, "instant auto-fire whirlwind"),
    ),
    "mechanics_notes": "Union-recipe-recursive: 'an EVOLVED weapon unions with a base weapon' — actually Vento Sacro + Bloody Tear are BOTH evolutions. This is the most investment-heavy recipe path in VS. Heal-on-hit from Bloody Tear carries through. DLC era + s11 span confirmed.",
    "era_confirmed": "vs-dlc-era",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Fuwalafuwaloo inherits both contributing evolution stats; whirlwind damage scales with Power/Area.",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 17. vs-queen-sigma ────────────────────────────────────────────────────────
# 100% completion reward character: Victory Sword start, +1% Might+Growth/level
# Atlas: _MHSSI = _, melee, high, spiky, solo, instant; DR (draft/pre-converged)
KITS.append({
    "kit_id": "vs-queen-sigma",
    "folk_name": "Queen Sigma",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_MHSSI-PSDT-DR-__-~~",
    "delivery": dc("self-origin", 0.82, "Victory Sword melee slash as starting weapon; close-range melee attack from character"),
    "footprint": dc("small-radius", 0.82, "melee sword arc around player body; small-radius slash zone"),
    "geo_text": "Queen Sigma: 100% completion reward character. Starts with Victory Sword. Gains +1% Might AND +1% Growth per character level — scaling permanently accelerates. 'Pre-converged draft': the character IS the build convergence, not built toward it.",
    "control": ctrl([], "none", 0.80),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("pre-converged-draft (100% completion unlock + per-level scaling)", "draft", "n/a", "n/a",
                    "DR = draft/pre-converged. The character STARTS with the draft position — no build-toward needed. Per-level Might+Growth scaling = the economy compounds with level rather than weapon choices.", 0.82),
    "element": elem("n/a (sword/victory)", "hit", 0.78),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("M", 0.82, "melee Victory Sword start"),
        pc("H", 0.82, "high tempo auto-swing"),
        pc("S", 0.80, "spiky — Victory Sword has high-burst-per-swing character"),
        pc("S", 0.80, "solo; self-sufficient character"),
        pc("I", 0.82, "instant auto-swing"),
    ),
    "mechanics_notes": "Pre-converged-draft economy: Queen Sigma IS the convergence — 100% completion IS the draft investment. Per-level scaling (+1% Might, +1% Growth per level) compounds exponentially. 'The character's build is the hundred-percent' per mech_note framing.",
    "era_confirmed": "vs-dlc-era",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Queen Sigma scales with level intrinsically; all weapon upgrades apply normally. Per-level compounding accelerates every item's effective value.",
    "sources_used": ["cg (character guide)", "vv (Vampire Survivors video/wiki)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 18. vs-runetracer-no-future ───────────────────────────────────────────────
# Runetracer evolution: bouncing rune explodes on every ricochet — chain-hop NOT line
# Atlas: _RHFSI = _, ranged, high, flat, solo, instant; RC
KITS.append({
    "kit_id": "vs-runetracer-no-future",
    "folk_name": "No Future (Runetracer evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RHFSI-PCDD-RC-__-~~",
    "delivery": dc("projectile", 0.88, "bouncing rune projectile ricochets off walls/enemies and explodes on each bounce"),
    "footprint": dc("chain-hop", 0.88, "ricochet chain = chain-hop footprint; NOT a line — bouncing between surfaces/enemies"),
    "geo_text": "No Future: evolved Runetracer fires a rune that bounces off walls and enemies and EXPLODES on every ricochet. Wall-bounce geometry is the defining footprint — the rune caroms through the screen, detonating at each reflection point.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("evolution recipe (Runetracer max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Runetracer max + Armor = No Future. Bouncing explosions auto-fire continuously post-evolution.", 0.88),
    "element": elem("n/a (runic/arcane)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("R", 0.88, "ranged projectile that bounces"),
        pc("H", 0.85, "high fire rate; many runes bouncing simultaneously"),
        pc("F", 0.82, "flat per-explosion damage at each bounce"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant auto-fire per timer"),
    ),
    "mechanics_notes": "G2: chain-hop, NOT a line. The bouncing rune IS a projectile with ricochet behavior (chain-hop footprint). 'Wall-bounce geometry weaponized' per mech_note. Explosions on ricochet = the evolved mechanic. Ricochet count scales with Arena + enemy density.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "No Future: rune damage and bounce count scale with Power/Amount items.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 19. vs-phieraggi ──────────────────────────────────────────────────────────
# Gun union (Peachone+Ebony Wings+gun pair): rotating laser fans that scale with revives
# Atlas: _RHFSI = _, ranged, high, flat, solo, instant; SP + revive-stock-as-power
# G2 FLAG: TRUE BEAM (rotating laser fans = beam delivery, ring footprint)
KITS.append({
    "kit_id": "vs-phieraggi",
    "folk_name": "Phieraggi (guns union)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RHFSI-PMDM-SP-__-~~",
    "delivery": dc("beam", 0.85, "rotating laser fans fire sustained beams in rotating pattern; TRUE BEAM delivery confirmed"),
    "footprint": dc("ring", 0.82, "rotating beams sweep ring pattern around player; beams extend outward in rotating arc"),
    "geo_text": "Phieraggi: pistol pair union fuses into rotating laser fans. The lasers ROTATE, sweeping ring coverage. SCALE WITH REVIVES — unspent extra lives convert into damage multiplier. Rotating beam fans = ring footprint + beam delivery.",
    "control": ctrl([], "none", 0.82),
    "defense": defs(["glass"], "glass", 0.82),
    "economy": econ("revive-stock-as-power (unspent revives = damage multiplier)", "other", "n/a", "n/a",
                    "REVIVE-STOCK: unspent extra lives (the SP-derived revive resource) convert directly into weapon damage scaling. Each unspent revive = a damage multiplier stack. Revive is normally a survival resource; here it becomes an offensive investment choice.", 0.85),
    "element": elem("n/a (laser/physical)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("R", 0.85, "ranged rotating laser fans extend outward"),
        pc("H", 0.85, "high tempo rotating beam output"),
        pc("F", 0.82, "flat per-beam sustained damage"),
        pc("S", 0.82, "solo; self-contained rotating beams"),
        pc("I", 0.85, "instant continuous beam rotation"),
    ),
    "mechanics_notes": "G2 flag: TRUE BEAM — rotating laser fans are sustained directional beams (not projectiles). Ring footprint from rotation. Revive-stock-as-power is the distinctive economy: it converts a survival resource (extra lives) into offensive scaling, creating a risk-reward trade. Union recipe: both gun weapons required.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Phieraggi: more revives = more damage; beam count scales with Amount items.",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 20. vs-gorgeous-moon ──────────────────────────────────────────────────────
# Pentagram evolution: erases screen AND vacuums all gems — harvest+deletion fusion
# Atlas: _RLSSI = _, ranged, low, spiky, solo, instant; HV
KITS.append({
    "kit_id": "vs-gorgeous-moon",
    "folk_name": "Gorgeous Moon (Pentagram evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RLSSI-PLDM-HV-__-~~",
    "delivery": dc("self-origin", 0.88, "screen-wide deletion pulse emanates from player position; global screen erasure"),
    "footprint": dc("large-zone", 0.92, "entire visible screen is the zone; large-zone erasure footprint"),
    "geo_text": "Gorgeous Moon: evolved Pentagram ERASES the screen (kills all on-screen enemies) AND VACUUMS every gem simultaneously. Screen deletion fused with mass harvest. Low tempo — fires rarely but the effect is total-screen when it does.",
    "control": ctrl(["instant-kill", "delete"], "core", 0.85),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("harvest-verb (vacuum all gems on screen erasure)", "harvest", "n/a", "n/a",
                    "HV = harvest-verb. Every Gorgeous Moon pulse auto-collects all gems on screen. The economy is self-refueling: deletion generates gems; harvest captures them. Evolved Pentagram + Attractorb = Gorgeous Moon.", 0.88),
    "element": elem("n/a (void/moon)", "hit", 0.82),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("R", 0.85, "ranged screen-wide pulse; extends to full screen edge"),
        pc("L", 0.88, "low tempo — fires slowly; when it fires, full screen erasure"),
        pc("S", 0.88, "spiky amplitude — entire-screen deletion = maximum burst"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant screen erasure when it fires"),
    ),
    "mechanics_notes": "Harvest-deletion fusion: 'erase the screen AND vacuum every gem on it' — the two functions are simultaneous. HV (harvest-verb) economy: the deletion IS the harvest trigger. Low tempo justified by catastrophic impact. Pentagram's base function (screen erasure) amplified by gem vacuum on evolution.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Gorgeous Moon: Cooldown reduction items fire the screen erasure more frequently.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 21. vs-hellfire ───────────────────────────────────────────────────────────
# Fire Wand evolution: piercing fireballs → screen-length flame lance (lane footprint)
# Atlas: _RMSSI = _, ranged, med, spiky, solo, instant; RC
KITS.append({
    "kit_id": "vs-hellfire",
    "folk_name": "Hellfire (Fire Wand evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RMSSI-PNDD-RC-__-~~",
    "delivery": dc("projectile", 0.88, "piercing fireball projectile traverses full screen length; single powerful projectile not a sustained beam"),
    "footprint": dc("lane", 0.85, "screen-length flame lance travels in a linear piercing lane; everything in the line is hit"),
    "geo_text": "Hellfire: evolved Fire Wand fires screen-length piercing flame lance projectiles at random elite enemies. The fireball travels the full screen length, hitting everything in its path. Spiky amplitude — fewer shots but each is a massive hit.",
    "control": ctrl(["burn"], "rider", 0.80),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("evolution recipe (Fire Wand max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Fire Wand max + Spinach = Hellfire. Fires at random elites automatically.", 0.88),
    "element": elem("fire", "hybrid", 0.85),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("R", 0.88, "ranged screen-length projectile"),
        pc("M", 0.82, "medium tempo — fewer shots, each powerful"),
        pc("S", 0.88, "spiky amplitude — each flame lance is a large damage spike"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant auto-fire projectile launch"),
    ),
    "mechanics_notes": "Lane footprint (NOT beam): Hellfire is a piercing projectile that traverses a full-screen linear path — footprint=lane from piercing effect. Delivery=projectile (not a sustained beam; each fireball is a discrete shot). Burn rider on fire element. 'Screen-length flame lance stream' per mech_note.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Hellfire inherits Fire Wand stats; Power items increase flame lance damage.",
    "sources_used": ["sg (survival-game guide)", "kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 22. vs-thunder-loop ───────────────────────────────────────────────────────
# Lightning Ring evolution: random sky-strikes that hit twice per bolt
# Atlas: _RMSSI = _, ranged, med, spiky, solo, instant; RC
KITS.append({
    "kit_id": "vs-thunder-loop",
    "folk_name": "Thunder Loop (Lightning Ring evo)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "_RMSSI-PSDD-RC-__-~~",
    "delivery": dc("at-target", 0.88, "random sky-strike lightning bolts descend at random enemy positions; no player aiming"),
    "footprint": dc("point", 0.85, "each bolt hits at a single point; TWICE per bolt (the loop)"),
    "geo_text": "Thunder Loop: evolved Lightning Ring fires random sky-strikes at enemy positions that hit TWICE per bolt — the 'loop.' Off-screen artillery: player has no aiming control over where bolts land, only enemy density determines targeting probability.",
    "control": ctrl(["shock", "stun"], "rider", 0.82),
    "defense": defs(["glass"], "glass", 0.80),
    "economy": econ("evolution recipe (Lightning Ring max + passive item)", "recipe", "n/a", "n/a",
                    "RC = recipe/evolution. Lightning Ring max + Duplicator = Thunder Loop. Bolts auto-target random enemies.", 0.88),
    "element": elem("lightning", "hit", 0.88),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank"),
        pc("R", 0.88, "ranged sky-strike from off-screen; no aiming"),
        pc("M", 0.82, "medium tempo; bolt cadence is moderate"),
        pc("S", 0.85, "spiky — two-hit bolt = each strike is a dual spike"),
        pc("S", 0.85, "solo; no proxy"),
        pc("I", 0.88, "instant sky-strike when it triggers"),
    ),
    "mechanics_notes": "Double-hit per bolt ('loop') is the evolved mechanic: base Lightning Ring hits once; Thunder Loop hits twice per bolt. 'Off-screen artillery you neither aim nor see firing' per mech_note — the randomness is the identity. Shock/stun riders from lightning.",
    "era_confirmed": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Thunder Loop: Cooldown + Amount items increase bolt frequency and count.",
    "sources_used": ["kb (knowledge base)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 23. vs-big-trouser ────────────────────────────────────────────────────────
# Gold-farm archetype character: Candybox access + greed scaling
# Atlas: ____SI = blank, blank, blank, blank, solo, instant; SP + meta-currency-farm
KITS.append({
    "kit_id": "vs-big-trouser",
    "folk_name": "Big Trouser (gold-farm archetype)",
    "game": "vs",
    "status": "positive",
    "atlas_key": "____SI-P___-SP-__-~~",
    "delivery": dc("other", 0.78, "meta-character record; gold-farm archetype; no specific weapon delivery identity"),
    "footprint": dc("other", 0.75, "meta-character; no distinctive spatial footprint beyond weapon choices"),
    "geo_text": "Big Trouser: Greed scaling character with Candybox access. Build IS the bank — runs are currency-generation engines rather than survival challenges. Greed stats + Candybox (any weapon slot filler) make his runs meta-currency farms.",
    "control": ctrl([], "none", 0.72),
    "defense": defs(["glass"], "glass", 0.72),
    "economy": econ("meta-currency-farm (Greed + Candybox + gold scaling)", "harvest", "n/a", "n/a",
                    "Meta-currency: Big Trouser's economy is gold generation for the persistent meta-progression shop. Greed stat multiplies gold pickup; Candybox fills weapon slots with any weapon needed to survive long enough to maximize gold yield.", 0.78),
    "element": elem("n/a", "hit", 0.70),
    "movement": VS_MOV,
    "prefix_claims": pfx(
        pc("_", 0.50, "VS attr blank; meta-character, weapon-agnostic"),
        pc("_", 0.50, "meta-character; weapon choice varies per run goal"),
        pc("_", 0.50, "meta-character; tempo varies by weapon"),
        pc("_", 0.50, "meta-character; amp varies by weapon"),
        pc("S", 0.72, "solo build; no proxy"),
        pc("I", 0.78, "instant auto-fire; base VS auto-attack pattern"),
    ),
    "mechanics_notes": "Meta-currency-farm archetype: 'the character whose BUILD is the bank' per mech_note. Greed scaling + Candybox access = flexible weapon selection optimized for gold yield over damage output. DLC character. Economy extends to the meta-game (coin shop between runs).",
    "era_confirmed": "vs-dlc-era",
    "post_cutoff": False,
    "dossier_owed": False,
    "rank1_upgrade": "Big Trouser: invest in Greed stat and gold-multiplier items; Candybox fills remaining weapon slots.",
    "sources_used": ["ax (achievements guide)", "pg (player guide)", "rdr-kit-atlas-v3.csv provenance"],
})

# ── 24. vs-golden-egg-scaling — NEGATIVE ──────────────────────────────────────
# Negative: eternal stat inflation from Golden Eggs dissolves build identity
KITS.append({
    "kit_id": "vs-golden-egg-scaling",
    "folk_name": "Golden Egg eternal scaling",
    "game": "vs",
    "status": "negative",
    "atlas_key": "______-____-SP-__-~~",
    "delivery": dc("other", 0.80, "meta-progression: permanent stat eggs; not a combat weapon"),
    "footprint": dc("other", 0.80, "no spatial footprint; meta-progression record"),
    "why_negative": "Eternal-stat-inflation: 'infinite permanent stat eggs that eventually DISSOLVE build identity' — the guide's own words flag this as a build-dissolution mechanic. At sufficient Golden Egg stacks, the player's intrinsic stats overwhelm all weapon choices, making weapon selection irrelevant. Negative: documents the mechanism that eventually undoes build identity in VS.",
    "era_span": "vs-1.0-2022",
    "post_cutoff": False,
    "dossier_owed": False,
    "prov": "sg",
    "mech_note": "Golden Eggs are purchasable permanent stat boosts from the main menu shop (bought with gold). At sufficient stacks, base stats outscale weapon scaling — 'dissolve build identity.' The corpus records this as a documented anti-pattern in the endgame meta.",
})

# ── output ────────────────────────────────────────────────────────────────────
pos  = [k for k in KITS if k.get("status") == "positive"]
neg  = [k for k in KITS if k.get("status") == "negative"]
pct  = [k for k in KITS if k.get("post_cutoff")]

with OUT.open("w") as f:
    for k in KITS:
        f.write(json.dumps(k) + "\n")

print(f"Vampire Survivors: {len(KITS)} records | pos={len(pos)} neg={len(neg)} post-cutoff={len(pct)}")
print(f"Written: {OUT}")

print("\n=== DIRECTED SWEEP RESULTS (Vampire Survivors) ===")
print("C2 (support-existence): NO pure-support kit. VS is auto-attack solo survival; no multi-actor context.")
print("G2 (line-vs-projectile):")
print("  TRUE BEAM: vs-infinite-corridor-crimson-shroud (Clock Lancet freeze beams = beam + lane)")
print("  TRUE BEAM: vs-phieraggi (rotating laser fans = beam + ring)")
print("  Lane footprint (projectile, NOT beam): vs-heaven-sword (boomerang return-path), vs-hellfire (screen-length piercing)")
print("  Chain-hop NOT line: vs-runetracer-no-future (wall-bounce ricochet)")
print("  Projectile-spam NOT beam: vs-thousand-edge (dagger wall in faced direction)")
print("D1 (shield-split):")
print("  SUSTAIN-LEECH: vs-bloody-tear, vs-soul-eater, vs-fuwalafuwaloo (heal-on-hit / aura-leech)")
print("  SHIELD-ABSORB: vs-infinite-corridor-crimson-shroud (Crimson Shroud damage cap = shield layer)")
print("  GLASS: all remaining VS positive kits (no traditional defense layers)")
print("POST-CUTOFF roster:")
for k in pct:
    print(f"  {k['kit_id']} | {k.get('era_confirmed','')}")
print("NEGATIVES:")
for k in neg:
    print(f"  {k['kit_id']} | {k.get('why_negative','')[:80]}")
