# Wave A — Summon/Proxy Evidence Surface v1

**Commissioning ruling:** pause-2 convening 2026-07-12 — Wave A is the FIRST engine-expansion wave (summoner/proxy mechanics buildout).  
**Consumer:** gandalf Wave-A engine spec → KR sequences gamora/rocket.  
**Authored:** 2026-07-12 (evidence-extraction work unit, clean restart after API-timeout attempt).  
**Scope:** evidence-only; zero design proposals, zero code changes.

---

## §1 — Corpus Proxy Taxonomy: 48-Kit Demand Set

All 48 rows: `geometry_value='totem'` AND `row_class='combat-kit'` from `canon_engine_key` joined to `canon_corpus`. Five carry `resolved:totem-ratified` flags. The set spans 15 games (d2, d3, d4, di, gd, hades2, le, poe1, poe2, tl2, tli, tq, tq2, chronicon, undecember implicit via roster).

### Cluster 1: Persistent Army (autonomous fighters that persist and die) — 10 kits

The defining feature: proxy entities persist across the encounter, have HP, target enemies autonomously, and re-summon on a cadence or uptime economy. The master's role is upkeep/placement, not moment-to-moment direction.

| kit_id | folk_name | game | economy | proxy_val | evidence |
|---|---|---|---|---|---|
| gd-skeleton-ritualist | Skeleton Ritualist | gd | reserve (mana) | heavy | "skeletal legion with Primalist support totems healing the bone wall — GD's classic army necro" |
| le-skeleton-necro | Skeleton Necromancer | le | spend (mana) | heavy | "Each Skeleton summoned costs Mana. Army self-sustains once summoned. Death triggers re-summon cycle." |
| le-squirrel-bm | Squirrel Beastmaster | le | spend (mana) | heavy | "squirrels persist autonomously and resupply from Herald of the Scurry passive conversion" |
| le-wraithlord-necro | Wraithlord Necromancer | le | harvest (minion sacrifice) | heavy | "Wraithlord's Harbour: smaller wraiths are sacrificed to empower/maintain the single Wraithlord" |
| poe2-minion-infernalist | Minion Infernalist | poe2 | reserve (Spirit) | heavy | "Spirit is the persistent reservation resource; each skeleton/arsonist slot costs Spirit to maintain" |
| poe2-infernal-legion | Infernal Legion Minions | poe2 | reserve (Spirit) | heavy | "reserved permanently for each active minion. Infernalist class has enhanced Spirit capacity." |
| tl2-bot-engineer | Bot Summoner Engineer | tl2 | reserve (mana) | heavy | "Bots maintain as persistent allies costing Mana reserve upkeep." |
| tli-moto-bots | Moto Bot Commander | tli | reserve (Ember) | heavy | "Bot upkeep via Ember reserve. SU old code = sustain/reserve." |
| poe1-siege-ballista | Iron Commander Siege Ballista | poe1 | item-count (DEX stat) | heavy | "Iron Commander grants +1 ballista per 200 DEX — the attribute stack literally COUNTS the army" |
| d3-m6-sentries | Marauder Sentries | d3 | spend (hatred + cooldown) | heavy | "Sentries FIRE YOUR OWN hatred spenders — embodiment of the Marauder" |

**STRADDLER (Cluster 1 / Cluster 2):** `gd-skeleton-ritualist` has `flags=["resolved:totem-ratified"]` and `econ_status=gap` — the probe fact says reserve/mana but the engine-key records a `gap` status. Labeled in both clusters where applicable.

### Cluster 2: Stationary Turret / Totem (emplaced emitters, no HP death cycle) — 18 kits

The defining feature: placed at a location, fires autonomously from that position, removed by duration or replacement rather than being killed. Economy is predominantly cooldown-gated placement.

| kit_id | folk_name | game | economy | footprint | evidence |
|---|---|---|---|---|---|
| d2-hydra-sorc | Hydra Sorceress | d2 | cooldown | multi-point | "stationary fire-spitting hydra emitters on short cooldowns" |
| d2-trapsin | Trapsin | d2 | spend (mana) | chain | "stationary trap emitters (Lightning/Death Sentry) that fire autonomously" |
| gd-mortar-purifier | Mortar Trap Purifier | gd | cooldown | small-radius | "Mortar Traps lob shells autonomously from wherever you dropped them" |
| gd-wendigo-totem-ritualist | Wendigo Totem Ritualist | gd | cooldown | large-zone | "Plant hungering totems that LEECH the room for you while bleed stacks tick" |
| le-storm-totem-shaman | Storm Totem Shaman | le | spend (mana) | multi-point | "Totems placed at target location autonomously fire lightning at nearby enemies" |
| poe1-ea-ballista | Explosive Arrow Ballista | poe1 | cooldown | large-zone | "Ballista totems stack explosive arrows into a target that detonate in one massive explosion" |
| poe1-fire-trap | Fire Trap | poe1 | cooldown | large-zone | "Thrown trap arms on the ground and erupts when enemies step near" |
| poe1-glacial-cascade-mines | Glacial Cascade Mines | poe1 | cooldown | large-zone | "Thrown mines detonate cascading ice eruptions marching forward in a line" |
| poe1-pizza-sticks | Pizza Sticks | poe1 | cooldown | large-zone | "Totems channel Flameblast to full stages and detonate, over and over — the CHANNEL is outsourced" |
| poe1-seismic-trap | Seismic Trap | poe1 | cooldown | large-zone | "Thrown trap releases a SEQUENCE of shockwave pulses over its duration" |
| poe1-warchief | Ancestral Warchief | poe1 | cooldown | small-radius | "Totems perform your melee slams while you stand nearby buffing them" |
| poe2-warbringer-totems | Ancestral Totem Warrior | poe2 | spend (mana) | large-zone | "Mana spend per totem placed. Totems persist and slam autonomously." |
| poe2-archmage-totems | Archmage Totems Oracle | poe2 | unknown (POST-CUTOFF) | large-zone | "mana-as-weapon-outsourced" — post-cutoff conf capped at 0.47 |
| tq-druid-squall-caster | Druid Storm Caster | tq | spend (Energy) | large-zone | "Squall places a persistent storm zone at target location" |
| tq-trap-magician | Trapper Magician | tq | ammo (Energy+count) | large-zone | "Traps cost Energy per placement and have a limited count (ammo-style)" |
| tq2-forge-turrets | Forge Turrets | tq2 | ammo (Energy; unverified) | large-zone | "Turret placement likely has count limit (ammo model); Forge mastery details unverified" |
| chr-mechanist-turret-drone | Turret & Drone Mechanist | chronicon | spend (Power Cores) | large-zone | "Deploying turrets and drones costs Power Cores. Reserve economy for maintenance." |
| di-crusader-banner-support | Banner Support Crusader | di | cooldown | large-zone | "Banner radiates a buff aura over a large area around placement point" |

**STRADDLER (Cluster 1 / Cluster 2):** `tl2-bot-engineer` and `tli-moto-bots` are mechanical turrets with reserve economy — they could be in Cluster 1 (HP-bearing persistent entities) or Cluster 2 (emplaced machines). Listed in Cluster 1 due to reserve economy. [JUDGMENT CALL — flagged.]

### Cluster 3: Mirage / Echo (skill-executing proxy that fires then expires) — 8 kits

The defining feature: a short-lived proxy that executes one or a timed burst of player-like skill actions, then vanishes. Economy is spend or proc, not cooldown-placement. These are the GX-19 commitment-absorber examples.

| kit_id | folk_name | game | economy | duration character | evidence |
|---|---|---|---|---|---|
| poe1-forbidden-rite | Forbidden Rite | poe1 | self-cost (totem pays life) | brief emitter | "The spell costs LIFE and deals chaos nova plus seeking projectiles; totem delivery makes totems pay the blood price instead" |
| le-shadow-bladedancer | Shadow Bladedancer | le | spend (mana) | shadow persists while player acts | "Shadow placement costs Mana. Subsequent mirror attacks are free (shadows copy player actions without additional cost)." |
| poe1-storm-brand | Storm Brand | poe1 | cooldown | brand until recall | "Brand attaches and periodically zaps nearby enemies with chaining lightning while you continue acting" |
| poe1-armageddon-brand | Armageddon Brand | poe1 | cooldown | brand duration | "Brand attaches to an enemy and periodically calls meteors on it while you run" |
| d3-mundunugu-sb | Mundunugu Spirit Barrage | d3 | spend (mana) | ghostly turret-burst | "Gazing Demise phantasms hover as ghostly turrets pulsing Spirit Barrage" |
| poe2-tempest-bell | Tempest Bell Monk | poe2 | meter (combo) | bell persists until destroyed | "Bell summoned using accumulated Combo Points. Subsequent bell-striking is a regular attack." |
| hades2-glorious-disaster | Glorious Disaster | hades2 | meter (Magick channel) | channel-sustained | "Magick channel fed into placed cast drives strike count" — POST-CUTOFF, conf 0.42 |
| d4-lightning-spear | Lightning Spear Sorcerer | d4 | cooldown | autonomous until hits | "Conjured spears crackle around the sorcerer hunting targets autonomously while cooldown resets" |

### Cluster 4: Commitment-Absorber (proxy pays the wind-up, channel, or life cost) — 5 kits

**[GX-19 cluster — Matt-ratified]** The defining feature is NOT about dealing damage differently, but about absorbing an axis-cost (channel time, life cost, wind-up) so the player avoids it. The proxy is the payer, not just the deliverer.

| kit_id | folk_name | game | absorbed commitment | economy | evidence |
|---|---|---|---|---|---|
| poe1-pizza-sticks | Pizza Sticks | poe1 | channel (Flameblast stages) | cooldown | "Totems channel Flameblast to full stages and detonate — the CHANNEL is outsourced to totems" |
| poe1-forbidden-rite | Forbidden Rite | poe1 | life cost (spell cost) | self-cost (totem) | "The spell costs LIFE; totem delivery makes totems pay the blood price instead" |
| poe2-warbringer-totems | Ancestral Totem Warrior | poe2 | wind-up (slam) | spend (mana) | GX flags include GX-01 and GX-04; spec notes "Warbringer totems absorb slam wind-ups" |
| poe2-archmage-totems | Archmage Totems Oracle | poe2 | mana cost (spell mana) | unknown | "mana-as-weapon-outsourced" — totems absorb the mana cost per the econ_raw |
| chr-mechanist-turret-drone | Turret & Drone Mechanist | chronicon | recategorization multiplier | spend (Power Cores) | GX-19 flag; "GX-19 in a third lineage context" |

**[JUDGMENT CALL]** `poe1-pizza-sticks` appears in both Cluster 2 (stationary turret) and Cluster 4 (commitment-absorber). It is the canonical GX-19 example. Listed in both.

### Cluster 5: Taunt-Tank / Meat-Shield (proxy draws aggro, player kites behind) — 4 kits

The defining feature: proxy exists to take damage and redirect enemy attention, not primarily to deal damage. Player survives by hiding behind the proxy's threat table.

| kit_id | folk_name | game | evidence |
|---|---|---|---|
| gd-skeleton-ritualist | Skeleton Ritualist | gd | "skeletal legion" — defensive screen function, resolved:totem-ratified |
| le-skeleton-necro | Skeleton Necromancer | le | "Death of skeletons triggers re-summon cycle" — army re-summon on attrition |
| poe2-minion-infernalist | Minion Infernalist | poe2 | "skeleton warriors and arsonists autonomously attack targets" — frontline |
| le-wraithlord-necro | Wraithlord Necromancer | le | "Wraithlord autonomously seeks and attacks targets" — single large proxy as frontline tank |

**Note:** Bench row B11 (Inversion Summoner) also belongs here — "proxy tank, master hides" is its folk description. B11 is addressed in §4.

### Field/Environment Kits (do not fit the above clusters cleanly) — 8 kits

These kits use the totem geometry but their primary identity is terrain modification or field placement, not a mobile or persistent fighter. They share the `at-target` delivery pattern but the "proxy" is more a zone than an actor.

| kit_id | folk_name | game | character |
|---|---|---|---|
| le-frost-wall-rm | Frost Wall Runemaster | le | lane-blocking wall structure; not an actor |
| poe1-earthshatter | Earthshatter | poe1 | spike-field raised by player, detonated by warcry |
| poe1-earthquake | Earthquake | poe1 | delayed aftershock — field at location |
| poe1-bladefall-bladeblast | Bladefall + Blade Blast | poe1 | field resource (blades in ground) consumed by second skill |
| tq-battlemage-warfare-earth | Battlemage | tq | melee+spell hybrid; totem=minimal; primary is player attacks |
| d4-mighty-throw | Mighty Throw Barbarian | d4 | planted weapon zone |
| d4-touch-of-death | Touch of Death Spiritborn | d4 | centipede-spirit touch — chain-spreading; no persistent proxy |
| d4-death-trap | Death Trap Rogue | d4 | cooldown-reset loop; trap is the identity, not an entity |

**Solo-identity kits flagged as totem** (these have `proxy_val='solo'` but are tagged totem by geometry; they are the genre's weakest signal for proxy design):
- `d2-fire-sorc` (solo/instant — Fire Sorceress; Meteor/Fireball direct-cast)
- `poe1-earthquake` (solo/wind-up)
- `poe1-earthshatter` (solo/wind-up)
- `poe1-bladefall-bladeblast` (solo/instant)
- `tq-battlemage-warfare-earth` (solo/instant)
- `tq-druid-squall-caster` (solo/instant)
- `d4-touch-of-death` (solo/instant)

**Cluster count summary:**
- Cluster 1 (Persistent Army): 10 kits
- Cluster 2 (Stationary Turret/Totem): 18 kits
- Cluster 3 (Mirage/Echo): 8 kits
- Cluster 4 (Commitment-Absorber/GX-19): 5 kits (overlapping with C2/C3)
- Cluster 5 (Taunt-Tank): 4 kits (overlapping with C1)
- Field/Environment: 8 kits (not primarily proxy actors)
- Solo-identity/totem-tagged: 7 kits (weakest proxy signal)

---

## §2 — Economy Patterns: Table by Pattern × Game

Economy families observed across the 48 kits (from `canon_probe_facts` family=economy, `econ_status`, `econ_meter_type`, `econ_raw`):

### Pattern A: Cooldown (most common — 20 kits)
Proxy is deployed on a cooldown; no resource consumed per placement. Re-deployment replaces or supplements.
**Games:** d2 (hydra), d3 (sentries), d4 (death-trap, lightning-spear), gd (mortar, wendigo), poe1 (ea-ballista, fire-trap, glacial-cascade, pizza-sticks, seismic-trap, storm-brand, armageddon-brand, warchief, earthshatter), di (crusader-banner)
**Caps:** all with multi-spawn econ carry implicit caps (PoE1: 2 totems baseline, scalable; LE: per-skill cap; TQ: count-limited ammo)

### Pattern B: Mana Spend-per-Summon (10 kits)
Each summoned unit costs mana at placement. Army self-sustains once up; player mana recovery governs cadence.
**Games:** d2 (trapsin, fire-sorc), le (skeleton-necro, squirrel-bm, storm-totem, explosive-trap-falconer, frost-wall), poe1 (earthquake, forbidden-rite), d3 (mundunugu-sb), d4 (touch-of-death)
**Fact:** le-storm-totem: "Totems persist until killed or replaced. Multiple totems active simultaneously up to cap."

### Pattern C: Mana/Resource Reservation (6 kits)
Resource is reserved permanently per active proxy unit. No per-attack cost; upkeep is a passive drain on max-resource pool.
**Games:** gd (skeleton-ritualist), poe2 (minion-infernalist, infernal-legion), tl2 (bot-engineer), tli (moto-bots), poe1 (forbidden-rite counts here via totem-life-as-reserve)
**Key fact:** poe2: "Spirit is the persistent reservation resource; each skeleton/arsonist slot costs Spirit to maintain. PoE2 Spirit replaces PoE1 mana reservation for minions."
**Key fact:** gd: "mana (reserve) — The skeletal legion with Primalist support totems healing the bone wall"

### Pattern D: Harvest / Consume-Army (1 kit)
Smaller proxies are sacrificed to empower or feed a single larger proxy.
**Games:** le (wraithlord-necro only)
**Fact:** "Wraithlord's Harbour unique helm transforms the summon system: smaller wraiths are sacrificed to empower/maintain the single Wraithlord."

### Pattern E: Stat-Count Army (1 kit)
Army size is a function of a stat value rather than resource expenditure.
**Games:** poe1 (siege-ballista)
**Fact:** "Iron Commander grants +1 ballista per 200 DEX — the attribute stack literally COUNTS the army"

### Pattern F: Meter-Gated Proxy (2 kits)
A secondary meter (non-mana) accumulates from player actions, then is spent to summon/place.
**Games:** poe2 (tempest-bell, combo points), hades2 (glorious-disaster, Magick channel)
**Fact:** "Bell summoned using accumulated Combo Points (Monk system). Subsequent bell-striking is a regular attack."

### Pattern G: Ammo / Count-Limited Placement (2 kits)
A fixed stock of placeable units; re-supply on cooldown or energy.
**Games:** tq (trap-magician, tq2-forge-turrets)
**Fact:** "Traps cost Energy per placement and have a limited count (ammo-style — maximum active traps)."

### Pattern H: Hate/Fury Spend + Army (1 kit)
Proxy is maintained via a class-specific generated resource; army cadence tied to that resource's generation.
**Games:** d3 (d3-m6-sentries — hatred+turret-cadence)
**Fact:** "Embodiment of the Marauder makes deployed Sentries FIRE YOUR OWN hatred spenders"

### Pattern I: Self-Cost (totem absorbs life) — 1 kit
Proxy pays the life cost the player would otherwise pay.
**Games:** poe1 (forbidden-rite)
**Fact:** "The spell costs LIFE and deals chaos nova plus seeking projectiles; totem delivery makes totems pay the blood price instead"

### Economy patterns × summon cap behavior

| Pattern | Summon cap mechanism | Representative |
|---|---|---|
| Cooldown | Replacement on max count (hardcoded or gem-linked) | PoE1 totems (2 baseline) |
| Spend | Mana gate prevents over-summoning naturally | LE Skeleton Necro |
| Reserve | Pool ceiling = hard army cap (no mana = no more summons) | PoE2 Spirit / GD |
| Harvest | Single-unit ceiling by design | LE Wraithlord |
| Stat-count | DEX threshold → count; cap = item modifier | PoE1 Siege Ballista |
| Meter | Meter full = place one; must rebuild | PoE2 Bell |
| Ammo | Stock depletes; cooldown refills | TQ Trapper |

---

## §3 — Mint Re-Expressions (9 kits from mint-dossiers-reexpressed.jsonl)

Only 2 mint kits are relevant to Wave A (proxy/summon identity). The remaining 7 are non-proxy movement, self-cost, and solo-identity kits.

### Mint Priority: HIGH

**poe1-totem-hierophant** — Totem Hierophant (`mint_priority: HIGH`, `for_roster_kits: ["K18"]`)
- `atlas_key: SMLHHI-~~`
- Delivery: at-target (player places totem at cursor; totem auto-attacks autonomously)
- Footprint: small-radius (totem melee AoE strikes enemies in radius around its position)
- Economy: cooldown (totem placement on cooldown; mana light per-cast)
- Proxy: heavy — "Totems are the damage actors; player is placer"
- Commit: instant (placement is instant; no channel)
- Element: physical, damage_mode: hit
- Control: stun (centrality: none)
- Defense: armor + resist
- Mechanic note: "Ancestral Warchief / Ancestral Protector place melee totems that auto-attack; Hierophant node chain allows 2+ simultaneous. The genre's canonical totem-placer identity."
- Rank1 upgrade: +1% melee damage at Lv2; totem HP +marginal
- `dossier_owed: true` — deeper dossier still needed
- mint_note: "poe1 shipped totems for 10+ years; Ancestral Warchief + Hierophant are the defining corpus entries; absence is a harvest hole."

**d3-call-of-the-ancients** — Call of the Ancients Barbarian (`mint_priority: HIGH`, `for_roster_kits: ["K5"]`)
- `atlas_key: SMLSL_-~~`
- Delivery: at-target (summon three ancient warriors to fight at the targeted area)
- Footprint: large-zone (ancestors roam a large zone around cast point fighting enemies)
- Economy: cooldown (ultimate); wrath generation during the summon window
- Proxy: light — "K5 proxy-light classification; ancestors augment but don't replace player"
- Commit: instant (instant cast summon call)
- Element: physical, damage_mode: hit
- Control: none
- Mechanic note: "Call of the Ancients summons three named warriors (Talic, Korlic, Madawc); each specializes (whirlwind, leap, multi-hit). Immortal King 6-set makes them permanent (set-authored-loop). Defines D3 summon-burst window identity."
- mint_note: "STR proxy-light anchor ancestor for K5; genus-defining summon call archetype."

### Mint Priority: MED (non-proxy kits — brief note only)

- **poe1-ring-of-shields** — orbital guard (proxy-light, orbit delivery; H1/B7 ancestry, NOT Wave A primary target)
- **poe1-blood-magic-kit** — self-cost economy (INT solo; K26 ancestry)
- **d2-teleport-sorc** — movement-verb (INT solo; B5 ancestry)
- **d3-dashing-strike-monk** — movement-verb (WIS solo; B6 ancestry)
- **le-shift-bladedancer** — movement-verb (DEX solo; B6 ancestry)
- **poe1-vaal-blade-vortex** — Vaal charge economy (INT solo; B10 ancestry)
- **d2-sacrifice** — self-cost melee (STR solo; K26 ancestry; LOW priority, arguably negative-canon)

---

## §4 — Roster / Bench Gates

### K10 — Falconer
**roster_atlas row:** `name="Falconer"`, `attr=D`, `range_slot=R`, `tempo=H`, `amp=F`, `proxy=L` (light), `commit_slot=_`, `econ=__ (parametric)`, `class_v4r2=LINEAGE-5`, `note="shared pool w/ Cell 7"`

**lineage_enrichment:**
- `bc6_proxy=light`, `bc6_commit=_` (abstain), `bc6_raw=DRHFL_`
- `lineage_targets_json=[{"target_ref":"le:falconer","corpus_kit_id":"le-dive-bomb-falconer","corpus_bc6":{"attr":"DEX","range":"mid","tempo":"high","amp":"spiky","proxy":"heavy","commit":"instant"},"bc6_distance":3,"slots_compared":5,"resolved":true}]`
- `target_count=1`, `whitespace_flag=0`
- From `rdr-roster-kits.jsonl`: `mech_summary="DEX/proxy-light, shares w/ K7. Gates: proxy-P2 + E6; ranged-proxy nav gap (D3 archer proxy parks 38.9m) blocks ranged-proxy variant cert."`
- `cross_ref="gates:proxy-P2,E6"`
- **Gate status:** proxy-P2 (proxy light sim-cert) + E6 (engine unknown — likely nav extension); blocked by the ranged-proxy nav defect (§6 item c below)

**Notable lineage:** le-dive-bomb-falconer (GX-11, GX-19 flags): "YOUR BIRD does the killing — command Dive Bomb strikes while you kite untouchable, the falcon executing called attacks on your mark" (`rdr-kit-atlas-v3.csv`). GX-19 flag means the falcon absorbs the commitment (the dive-bomb is called by the player but executed by the bird).

### K11 — Trap Assassin
**roster_atlas row:** `name="Trap Assassin"`, `attr=D`, `range_slot=D`, `tempo=L`, `amp=S`, `proxy=H` (heavy), `commit_slot=_`, `econ=__ (parametric)`, `class_v4r2=LINEAGE-5`

**lineage_enrichment:**
- `bc6_proxy=heavy`, `bc6_commit=_` (abstain), `bc6_raw=DDLSH_`
- `lineage_targets_json=[d2-trapsin (distance=0, RESOLVED), poe2-witchhunter-grenades (distance=3, resolved), unknown:merc (unresolved, gap=true)]`
- `target_count=3`, `whitespace_flag=0`
- From `rdr-kit-atlas-v3.csv`: `mech_summary="mid/low/spiky/DEX/heavy — traps = stationary emitters. Gates: proxy-P0/P1 + E6."`
- `cross_ref="gates:proxy-P0/P1,E6"`
- **Gate status:** proxy-P0/P1 (baseline proxy gates before P2) + E6; the `soul-control troop command EXISTS` per atlas mechanics_status note
- The "soul-control troop command" is referenced in `canon-harvest-pipeline-spec-v2.md §213` as an existing engine surface: "battle-sim auto-aim, soul-control troop command, loot-operator framework, orbital/rotational addendum, element-hybridity addendum, reap/possession native"

### B11 — Inversion Summoner (bench)
**roster_atlas row:** `kit_id=B11`, `name="Inversion Summoner"`, `proxy=H` (heavy), `class_v4r2=INSUF`
- `rle.note="proxy tank, master hides"`, `bc6_raw=____H_`
- `whitespace_flag=1` (whitespace signal — this is a design gap coordinate)
- `rle.bc6_proxy=heavy`, `rle.bc6_commit=_` (abstain)
- The B11 "proxy tank, master hides" concept corresponds to Cluster 5 above. The master hides behind the proxy while the proxy taunts all enemy attention. No corpus kit at this exact coordinate (whitespace=1 confirmed).
- `class_v4r2=INSUF` — insufficient data for full classification.

### Proxy Gate Ladder (P0 through P2+E6)
Based on corpus evidence and atlas gate notes:
- **proxy-P0:** baseline proxy mechanics existing in the engine (troop command surface exists per canon-harvest-pipeline-spec-v2)
- **proxy-P1:** turret/pet AI variant support (stationary emitters that target autonomously)
- **proxy-P2:** proxy light sim-cert (positioned allies fight and are tracked in the spatial sim — Wave-A target)
- **E6:** unknown engine-side extension (nav-related; ranged proxy nav fix blocks K10)

---

## §5 — GX-19 Exhibits: Verbatim Ledger

From `canon-harvest-pipeline-spec-v2.md §9.1` (the GX-19 ratification row, VERBATIM):

> **GX-19 ⚑ | Commitment/cost transfer to proxies | PoE1 (Pizza Sticks carry the channel; FR totems pay the life cost) · PoE2 (Warbringer totems absorb slam wind-ups; Archmage totems absorb mana costs; Snipe's mirage executes the channel) | commitment axis — proxies that ABSORB an axis value are distinct from proxies that merely deliver damage**

From `canon-harvest-pipeline-spec-v2.md §9.8a / §9.10a` context records:

The GX-19 flag appears on 9 kits in the 48-kit set:
1. `chr-mechanist-turret-drone` — GX-19 (third lineage context per research notes)
2. `d3-m6-sentries` — GX-11 + GX-19 (sentries fire player's own hatred spenders)
3. `gd-mortar-purifier` — GX-19
4. `gd-wendigo-totem-ritualist` — GX-19
5. `hades2-glorious-disaster` — GX-19 (channel fed into placed cast)
6. `le-storm-totem-shaman` — GX-19 + GX-09
7. `poe2-archmage-totems` — GX-07 (mana-as-weapon-outsourced)
8. `poe2-warbringer-totems` — GX-01 + GX-04 (totem absorbs slam wind-up)
9. `tq-trap-magician` — GX-19
10. Also: `le-bomb-lance-falconer` and `le-dive-bomb-falconer` (corpus kits adjacent to K10) carry GX-19 flag

**The GX-19 design distinction for the Wave A spec:**

The critical split Matt ratified: proxies that ABSORB a commitment-axis value (channel time, wind-up, life cost, mana cost) are a DISTINCT mechanical species from proxies that merely DELIVER damage from a placed position.

- **Delivery proxies** (Clusters 1, 2): proxy fights/fires autonomously; player's commitment to cast the summon skill is normal; the proxy's own autonomous actions are its identity.
- **Absorption proxies** (Cluster 4/GX-19): the player would normally pay Channel, Wind-up, or Life; the proxy INTERCEPTS that payment. Example: Pizza Sticks totems sit and channel Flameblast for its full stage count — the player does NOT channel; the totem absorbs the channel commitment and detonates.

**Implication for Wave A spec:** the sim must represent both modes. A proxy that absorbs commitment does not simply inherit `damage_multiplier` — it changes what the PLAYER entity experiences on its action axis (the player's cast is instant; the proxy takes the channel time). This is a different sim seam than a persistent army fighter.

**GX-07 note:** `poe2-archmage-totems` carries GX-07 (mana-as-weapon), not GX-19 directly. The econ_raw says "mana-as-weapon-outsourced" — the totem IS the mana-weapon mechanism outsourced. Post-cutoff kit, conf 0.47.

---

## §6 — Engine What-IS Inventory (file:line citations)

### (a) Troop-Command Core — what EXISTS

The "soul-control troop command" is referenced in `canon-harvest-pipeline-spec-v2.md §213` as an EXISTING engine surface:
> "battle-sim auto-aim, soul-control troop command, loot-operator framework, orbital/rotational addendum, element-hybridity addendum, reap/possession native"

However, no `TroopCommand` or `troop_command` named entity exists in `src/reincarnated/simulation/` or `src/reincarnated/generation/` (grep returns zero matches). The reference is in the corpus harvest mechanics-status column — it describes the EXISTING engine's surface as viewed from the corpus mapping exercise (done pre-Wave-A). The troop-command surface referenced is the proxy population infrastructure that already EXISTS post-W1/W2 (documented below). The name "soul-control troop command" is the corpus-harvest team's label for what the engine provides, not a named code class.

### (b) `_DEFERRED_PROXY_BINS` — exact location and gate behavior

**File:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py`  
**Lines 95–99:**
```python
_DEFERRED_ECON_BINS = frozenset({"HP-economy", "charge-stack", "damage-taken-converts"})
_DEFERRED_PROXY_BINS = frozenset({"proxy-light", "proxy-heavy"})
_DEFERRED_DEF_SUBCASES: frozenset[str] = frozenset()
```
**Lines 317–318:**
```python
if proxy_bin in _DEFERRED_PROXY_BINS:
    [gate fires — no proxy kit is composed]
```

**What it gates:** Any kit whose BC axis lands in `proxy-light` or `proxy-heavy` bins is rejected at composition time. Currently ALL proxy kits are gated — the engine emits `"proxies": []` on every kit because both bins are deferred.

**What flipping it would expose:** Lifting `_DEFERRED_PROXY_BINS` would allow the BC-target composer to produce proxy-bin kits. The generation pipeline then routes to `proxy_vocabulary_bridge.build_proxies_surface()` and `proxy_decl_from_summon()` — machinery that EXISTS and is ready. The sim's `_build_positioned_allies()` in `spatial_engine.py` already consumes `proxy_decls`. The knob is present: `bc_target_cell_sampler.py:466` notes the `~25% target` proxy share, currently yielding 0.0 because the gate stays DOWN.

**Supporting evidence from `export/w3_emission_driver.py:116`:**
> "proxy bins (_DEFERRED_PROXY_BINS) remain gated; proxies=[] on all batch-1 kits"

**Supporting evidence from `generation/notes/w0_prereqs_smoke_2026_07_03.py:84`:**
> "with NO proxy cells READY (deferred), realized share == 0.0 … knob inert until W3 lifts _DEFERRED_PROXY_BINS"

### (c) D3-Archer-Proxy Nav Defect — located record

**Primary source (authoritative):** `canonical/current-to-end-state/current-to-end-state-engine.md:417` (verbatim):

> "the FLEX third kit `demo_gravecaller` (ranged caster-summoner) **cannot be build-floor-certified** — it D3-evaporates (WR 0.0) on a **navigation gap, NOT a magnitude**: the spectral archer ends 38.9 m from a boss it hits at 10 m because ally-nav chases nearest-enemy adds instead of holding boss-focus at range (`spatial_engine.py:~1996` nearest-enemy nav; `:2350` attack-phase boss-focus parity — no magnitude lever moves `proxy_realized_damage_dealt`). W2's 'fight mechanism complete' claim is **narrowed: melee-summon complete; ranged-summon nav-incomplete.**"

**Dispatch record:** `dispatches/2026-07-02-gamora-demo-summoner-cert.md:120` (gamora finding):

> "`proxy_realized_damage_dealt` is insensitive to all four levers except a linear dm term. Two fixes, BOTH outside the four-magnitude scope: (a) a D2 content edit (raise the gravecaller decl `count`), or (b) a ranged-ally boss-focus nav fix in production sim code (a W2-mechanism amendment). Per Gate-1 fold D I do NOT self-authorize either — escalated to KR."

**Disposition:** `demo_gravecaller` DEFERRED from demo (KR 2026-07-02). The ranged verb lands in "launch nav-mechanism work." Count-masking rejected (would corrupt §8 honesty instrument).

**Visible-band consequence:** `current-to-end-state-engine.md:92`: "the gravecaller archer proxy parks at **38.9 m** — inside Camera B's band, **outside B′'s**." Camera B′ visible band ≈ 29 m. The defect is now also a visible-band violation at B′.

**Code location of nav logic:** `spatial_engine.py` line ~1996 (nearest-enemy nav). The ally nav chases its nearest enemy (an add, not the boss) during the encounter while the attack phase has boss-focus parity at line ~2350 — the two are mismatched for ranged proxies.

**Wave A implication:** melee proxy nav (follow nearest enemy, chase to melee range) works. Ranged proxy nav requires a boss-focus amendment OR a positional hold at range — the proxy must maintain its engagement distance rather than running toward its nav_target until it parks at 38.9 m.

### (d) Actor / Combatant Class Structure — the seams a proxy actor touches

**Current solo-fight entity model:** `SpatialEntity` (defined at `spatial_engine.py:581`) is the unified fight entity. It carries `is_player: bool`, `allegiance: str = "enemy"` (W1 addition, 2026-06-22), and proxy runtime fields (`proxy_spawn_time`, `proxy_duration_s`, etc.) added as brownfield-safe keyword fields.

In a SOLO fight: `all_entities = [player] + mobs`. In a PROXY fight (W1/W2): `all_entities = [player] + positioned_allies + mobs`, where `positioned_allies` all have `allegiance="ally"`.

**Allegiance infrastructure (WAVE 1, 2026-06-22):** `_enemies_of(entity, world)` and `_allies_of(entity, world)` at `spatial_engine.py:1136,1141` filter by `entity.allegiance`. This generalizes targeting so any entity targets its allegiance-filtered enemies. In solo world it degenerates byte-identically (no allies = old behavior).

**Navigator generalization:** `_navigate_entity()` at `spatial_engine.py:1149` was renamed `player` → `nav_target` at W1. All five behavior branches (stationary_caster/melee_aggressive/ranged_kite/cast_at_range/hit_and_run) re-path against `nav_target` automatically. A proxy entity navigates toward its allegiance-filtered nearest enemy (a mob).

**Proxy spawn (WAVE 2):** `_build_positioned_allies()` at `spatial_engine.py:2067` spawns proxy entities on an "owner-relative summon ring." Each `proxy_decl` contributes `count` bodies (clamped to `proxy_max_active`). These allies FIGHT (realized damage), are TARGETABLE (have base_hp > 0 for mid/full tier), and DIE (hp <= 0 flip).

**Population tracker (COUNT instrument, separate from combat):** `_step_proxy_population()` at `spatial_engine.py:2100` runs the old ProxyCombatant lifecycle model (attrition, expiry, fission) as a COUNT-ONLY instrument. It does NOT assign spatial positions and deals NO spatial damage. It is gated by `track_proxy_population=True` (default OFF).

**ProxyCombatant entity model:** `proxy_population.py` (re-homed 2026-06-17 from deleted `proxy_combatant.py`). Contains `ProxyCombatant` dataclass with 14 typed proxy types mapped to behavioral tiers (minimal/mid/full). The 14 types:
- STRIKER family: `passive_fighter`, `autonomous_caster`
- BULWARK family: `golem_construct`, `bodyguard`
- BATTERY family: `totem_turret`, `volatile_emitter`, `slot_queue_emitter`
- TRIGGER family: `trap_mine`, `charged_threshold_proxy`
- ATTENDANT family: `warcry_buff_spirit`, `resource_conduit`, `fragile_escort`
- ECHO family: `terrain_anchor`, `delayed_position_shadow`

**Gen→Sim bridge:** `proxy_vocabulary_bridge.py` at `generation/proxy_vocabulary_bridge.py`. Translates summon-skill gen-side fields (`proxy_count`, `proxy_power_per`, `proxy_geometry`, `proxy_duration_s`, `proxy_spawn_cadence_s`, `proxy_max_active`) into `entity_from_proxy_dict`-consumable decls. The bridge EXISTS and is wired; it emits empty lists only because `_DEFERRED_PROXY_BINS` stays down.

**Set #6 (Proxy Commander) calibration:** `simulation/spatial_gauntlet/proxy_commander.py`. Calibrated balance constants: `C_2PC_FRICTION_REDUCTION=0.15`, `DELTA_COUNT=1`, `G_POWER=0.25`, `G_DUR=0.30`, `S_BASELINE=0.35`. Apply_set6_to_proxies and apply_clause_a_count are already coded.

**Proxy pairing layer (W2):** `generation/proxy_pairing_layer.py`. 65 valid CONVERGENCE pairs + 14×3 DUAL pools. Already coded, ratified. The 15 merge classes cover all 6 family-pair combinations.

**Demo summoner kits (hand-authored):** `generation/demo_summoner_kits.py`. Three fixtures: `demo_bone_acolyte`, `demo_crypt_lieutenant` (melee, CERTIFIED), `demo_gravecaller` (ranged, DEFERRED/nav-defect). Energy type: `focus` (death-economy upkeep fantasy). The two melee fixtures pass the §3 summoner mandate.

**PackProxy (mob-side, deprecated):** `combatant.py:279` — `pack_proxy_size: int = 0` on `CombatantState`. This is mob-side machinery (the pack-proxy multi-mob simulation for groups), NOT player proxies. Marked as `post-W0.9.1 deprecated`. Distinct from the W1/W2 player-ally proxy system.

### §7 — Fight Engine Shape

The spatial fight engine (`spatial_engine.py`, `SpatialFightEngine`) runs a tick-based loop at default `tick_size=0.1s`. Each tick: (1) advance timers and commitment states, (2) navigate entities toward their nav_target (allegiance-filtered nearest enemy), (3) resolve attacks for entities that are in range and off cooldown, (4) apply damage and check for kills, (5) evaluate win condition.

**Target selection:** Players use `_get_player_primary_target()` — boss-focus mode when a boss-focus entity is set and alive, else nearest mob. Mobs (and allies) use `_enemies_of(entity, world)` filtered to nearest-alive enemy by Euclidean distance. This is the seam the archer-proxy nav defect hits: an ally navigates to its nearest enemy (adds nearest to it), not to the player's boss-focus target.

**Position updates:** `_navigate_entity()` dispatches on `entity.preferred_behavior` (stationary_caster / melee_aggressive / ranged_kite / cast_at_range / hit_and_run). A melee-proxy will use `melee_aggressive` — close to within its `range_m` of nav_target and attack. A ranged-proxy needs `ranged_kite` or `cast_at_range` behavior, which maintains a distance from nav_target. The defect: the ranged proxy's nav_target may be an add at 3m, causing it to stay at 3m distance from the add while the boss sits at 45m unreachable.

**What a proxy actor enters into:** A positioned ally (`allegiance="ally"`) enters `all_entities`. It participates in: (a) targeting (is a valid target for mobs — targetable if `base_hp > 0`), (b) navigation on each tick (moves toward its nearest enemy), (c) attack resolution (if in-range of a mob, deals damage via its `proxy_decl` stats), (d) death detection (`hp <= 0`). It does NOT currently trigger AoE or commit-axis states — those sit on the player entity's action slots.

---

## §7 — Open Evidence Gaps

The following questions the corpus and engine inventory do NOT answer:

1. **Ranged proxy AI fix scope:** The nav defect is known (`spatial_engine.py:~1996`), but no evidence exists for the exact fix shape. Does ranged-ally nav need (a) boss-focus inheritance from the player's focus target, (b) a "hold at range" behavior variant, or (c) a nav_target priority override? The fix requires a new engine mechanic, not a magnitude tuning.

2. **Commitment-absorber sim seam (GX-19 deep case):** The existing proxy seam puts damage on the proxy entity. GX-19 absorption (totem carries the channel; player's action is instant) requires a different seam — the player's action-budget must see an "instant" cast while the proxy entity models the channel duration internally. No existing code handles this; `commitment_state_machine.py` only covers the PLAYER's commitment axis. How the proxy's channel-absorption interacts with the player's cadence clock is undefined.

3. **Multi-wave summon economy (re-summon cadence):** `proxy_spawn_cadence_s` exists in the bridge and decl schema, but `_build_positioned_allies()` only does spawn-at-fight-start. There is no re-spawn loop during the fight (the population tracker handles lifetime, but the positioned-ally fight path has no re-spawn mechanism). The W2 math notes mention the "count wall" but not the re-summon cadence during fight runtime.

4. **Proxy damage vs economy: calibration numbers:** `proxy_commander.py` carries scaffold magnitudes (`PROXY_REFERENCE_HP=20_000`, `PROXY_TIER_HP_FACTOR`, `PROXY_TIER_MAX_ACTIVE`). All are marked "gamora calibrates." The actual numbers that would make `proxy-light` and `proxy-heavy` BC cells pass the gauntlet at the correct band are unknown. The D3-evaporate failure mode (proxy HP too low → killed before dealing damage) and D2-dominance failure mode (proxy DPS too high → player has nothing to do) are design-risk documented but not calibrated.

5. **B11 (Inversion Summoner) spec gap:** `whitespace_flag=1` means no corpus kit exists at this coordinate (DEX/heavy/proxy-tank-hides). The "master hides behind proxy tank" identity requires a NEW sim mechanic: the player entity must be able to cede aggro entirely to the proxy. Currently, the player is always the primary mob target unless the proxy has `targeting_behavior="taunt"`. A taunt proxy drawing all aggro while the player deals damage from safety is technically possible with existing `golem_construct` + `AGGRO_FRACTION_TAUNT=0.6`, but the "master hides" extreme where the master takes ZERO aggro is not modeled.

6. **`poe2-archmage-totems` fact gap:** `econ_status=gap`, facts_json economy model `"unknown"` with POST-CUTOFF note. This is a HIGH-interest GX-19 kit (mana-as-weapon outsourced to totems) but its economy is unverified. A re-harvest pass is needed before it can serve as a design input.

7. **Proxy AI variant taxonomy gap:** The `rdr-kit-atlas-v3.csv` mechanics_status notes say "turret/pet AI variants + summon economy needed" for 12+ kits. The engine currently has one nav behavior per entity (`preferred_behavior`). Different proxy types need different AI: a `totem_turret` is stationary-caster, a `passive_fighter` is melee_aggressive, a `volatile_emitter` is proximity-triggered. The behavioral tier map (`PROXY_TYPE_TIER`) exists but the per-type AI assignment in `proxy_vocabulary_bridge.py:PROXY_TYPE_TARGETING` only covers targeting intent, not the full behavior branch.

8. **Fission proxy lifecycle vs fight:** `spawn_fission_subproxy()` in `proxy_population.py` handles LIFETIME fission (the COUNT instrument). Whether fission sub-proxies can exist as SpatialEntity positioned allies mid-fight (i.e., a dying proxy spawns combat-capable sub-proxies) is unspecified. The pairing layer's PROXY_FISSION T4 implies this, but no fight-path code handles mid-fight proxy spawning.

9. **Spirit/reserve analog in Reincarnated economy:** The corpus's strongest army archetypes (PoE2 Spirit reservation, GD mana reserve) gate army size via a permanent reservation resource. The engine's economy types are `mana`/`focus`/`rage` (combat-replenishing). A "reserved permanently per active proxy" economy (where summoning more proxies reduces your regenerating resource ceiling, not just spends from it) has no engine analog. The Wave A spec must decide whether to model this or map it to a simpler spend economy.
