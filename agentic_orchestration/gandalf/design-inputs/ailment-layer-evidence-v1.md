# Ailment-Layer Evidence Dossier — v1

**Commissioning ruling:** pause-2 convening 2026-07-12, item 4  
**Consumption target:** ailment-layer design session; feeds `config/ailments.yaml` + ailment-synergy design  
**Author:** gandalf evidence-extraction work unit, 2026-07-12  
**Source corpus:** 463 combat-kit records in `corpus.db` (463 = denominator; gap counts are exact DB counts)  
**Scope this dossier:** damage-amp (+ GX-15 exhibits + hades1 synergy precedent), freeze, stun, poison-dot, taunt annex

---

## 0 — Current engine ailment registry (contrast baseline)

From `~/Games/reincarnated-engine/config/ailments.yaml` (read-only; do not modify):

| Name | Category | is_control | Key params |
|---|---|---|---|
| burn | dot | none | tick_damage (dynamic), duration 3–7s (default 5s) |
| chill | soft_control | soft | slow_percent 20–50% (default 35%), duration 2–5s |
| root | hard_control | hard | duration 1.5–4s (default 2.5s) |
| knockback | hard_control | hard | distance 3–8 (default 5), stagger 0.3–1.0s |
| bleed | dot | none | tick_damage (dynamic), duration 3–7s (default 5s) |
| shock | hard_control | hard | duration 0.5–2.0s (default 1.0s) |
| consecrate | amplification | none | zone_duration 3–8s, dot_tick (dynamic, shadow targets only), heal_amp 5–20% |
| drain | dot | none | tick_damage (dynamic), duration 4–9s (default 6s) |

**Current engine shock** is paralysis-on-arc (interruption-by-discharge); it is NOT a damage-amplification debuff. The genre's primary use of shock (% increased damage taken) is entirely absent. This is the core tension the design session must resolve.

---

## Chapter 1 — GAP-AILMENT: damage-amp

### 1a — Kit census

**Total kits citing damage-amp gap: 100** (exact count from corpus.db; some kits carry duplicate entries — unique kit count is 97 after deduplication).  
Percentage of 463 combat kits: **~21%** — the single most-cited gap in the corpus.

**By game and tier:**

| Game | Tier | Kit count |
|---|---|---|
| poe1 | T1 | 29 |
| le | T1 | 13 |
| poe2 | T1 | 11 |
| gd | T1 | 10 |
| d4 | T1 | 5 |
| tq | T2 | 5 |
| d2 | T1 | 7 |
| hades1 | T2 | 3 |
| hades2 | T2 | 2 |
| chronicon | T2 | 2 |
| tq2 | T2 | 1 |
| tl2 | T2 | 1 |
| tli | T2 | 2 |
| d3 | T1 | 2 |
| di | T2b | 1 |
| hot | T3 | 1 |
| undecember | T2b | 1 |
| vs | T3 | 1 |

**Full kit list by game:**

**chronicon (T2):** chr-fulmination-templar (Fulmination Holy Reckoning Templar), chr-crown-proc-engine (Crown of Innate Probability)

**d2 (T1):** d2-trapsin (Trapsin), d2-mosaic-sin (Mosaic Assassin), d2-javazon (Javazon), d2-nova-sorc (Nova Sorceress), d2-lightning-sorc (Lightning Sorceress), d2-auradin (Auradin), d2-fohdin (FoHdin)

**d3 (T1):** d3-manald-heal (Manald Heal Paralysis), d3-raiment-shenlong (Raiment Generator)

**d4 (T1):** d4-lightning-spear (Lightning Spear Sorcerer), d4-ball-lightning (Ball Lightning Sorcerer), d4-chain-lightning (Chain Lightning Sorcerer), d4-lightning-storm (Lightning Storm Druid), d4-cataclysm (Cataclysm Druid)

**di (T2b):** di-tempest (Tempest / Mist Touched clones)

**gd (T1):** gd-phantasmal-blades-witch-hunter, gd-vitality-conjurer, gd-ravenous-earth-oppressor, gd-drain-essence-spellbinder, gd-panettis-mage-hunter, gd-stormbox-elementalist, gd-bloody-pox-conjurer, gd-doom-bolt-sentinel, gd-primal-strike-vindicator, gd-savagery-warder

**hades1 (T2):** hades1-merciful-end (Merciful End, Ares+Athena duo), hades1-ares-doom (Ares Doom Core), hades1-zeus-chain (Zeus Chain-Lightning Core)

**hades2 (T2):** hades2-glorious-disaster (Glorious Disaster, Zeus+Apollo duo), hades2-hail-storm (Hail Storm, Zeus+Demeter duo)

**hot (T3):** hot-kugelblitz (Kugelblitz, wandering ball lightning)

**le (T1):** le-dive-bomb-falconer, le-chthonic-fissure-warlock, le-reaper-form-lich, le-harvest-lich, le-lightning-blast, le-wraithlord-necro, le-runic-invocation, le-warpath-vk, le-erasing-strike-vk, le-smite-paladin, le-hammer-throw-paladin, le-storm-totem-shaman, le-shield-throw-time-rot-vk

**poe1 (T1):** poe1-lightning-arrow, poe1-pconc, poe1-spectral-throw, poe1-venom-gyre, poe1-lightning-strike, poe1-viper-poison, poe1-caustic-arrow, poe1-toxic-rain, poe1-scourge-arrow, poe1-dark-pact, poe1-cwdt-loop, poe1-ward-loop, poe1-bane, poe1-poison-bv, poe1-deaths-oath, poe1-hexblast-mines, poe1-arc, poe1-edc, poe1-soulrend, poe1-lightning-conduit, poe1-crackling-lance, poe1-mjolner, poe1-hoag, poe1-forbidden-rite, poe1-storm-brand, poe1-spark, poe1-archmage, poe1-ball-lightning, poe1-divine-ire

**poe2 (T1):** poe2-lightning-arrow-deadeye, poe2-tempest-flurry, poe2-howa-invoker, poe2-acolyte-darkness, poe2-tempest-bell, poe2-galvanic-shards, poe2-spark-stormweaver, poe2-erasure-edc-lich, poe2-blood-mage, poe2-lightning-spear-amazon, poe2-titan-hotg

**tl2 (T2):** tl2-prismatic-embermage (Prismatic Bolt Embermage)

**tli (T2):** tli-youga-spirit-magus (Youga Spirit Magus Summons), tli-iris2-thunder-magus (Iris 2 Thunder Magus Minions)

**tq (T2):** tq-rune-weapon-thunderer, tq-trap-magician, tq-druid-squall-caster, tq-elementalist-volcanic-storm, tq-thane-storm-warfare

**tq2 (T2):** tq2-elementalist

**undecember (T2b):** ud-lightning-vortex

**vs (T3):** vs-thunder-loop

### 1b — Implementation-pattern table

The corpus records the gap as "GAP-AILMENT:damage-amp" across heterogeneous host-game implementations. The probe facts and JSONL capture three distinct mechanical archetypes:

**Pattern A — Ailment-as-% increased damage taken (canonical shock flavor, PoE1)**  
PoE1 shock is the genre's purest expression: enemies under shock take % increased damage from all sources. Magnitude scales with the lightning damage of the hit that applied it (capped at 50% increased damage taken in PoE1). Lightning Conduit (poe1-lightning-conduit) explicitly *consumes* the shock for a massive hit: "Consumes the shock on enemies for a massive hit scaled by shock magnitude — apply the ailment, then cash it in; ailment mark-and-consume." [kit: poe1-lightning-conduit; family: economy, geo_text]. Arc (poe1-arc) lists shock as rider ailment with centrality=none — the chain-lightning loop is self-sustaining; shock is a bonus. Lightning Arrow (poe1-lightning-arrow) is structurally identical: shock rider, centrality=none. All PoE1 lightning kits carry shock as rider; the % increased damage is a background multiplier the build passively applies, not an active loop component for most of them.

*Magnitude note:* not-in-facts (exact % scaling formula not captured in probe facts or geo_text). `training-knowledge, verify at session:` PoE1 shock magnitude = min(50%, base_shock_effect * lightning_damage_dealt / monster_max_hp). Shock threshold for noticeable amp is ~5%; competitive builds target 15–50%.

**Pattern B — Flat multiplier window (D4 Vulnerable)**  
D4 lightning kits (d4-lightning-spear, d4-ball-lightning, d4-chain-lightning, d4-lightning-storm, d4-cataclysm) all carry shock with centrality=none. In D4, the canonical damage-amp mechanic is the Vulnerable debuff — a flat % increased damage taken applied by skills, aspects, or items on a timed window. The PoE-style shock (% increased damage taken scaling with hit) maps to Vulnerable mechanically but is a separate status.

*Magnitude note:* not-in-facts. `training-knowledge, verify at session:` D4 Vulnerable = 20% increased damage taken (fixed, not scaling).

**Pattern C — Resistance reduction / debuff (GD Resistance Reduction)**  
All 10 GD kits carry damage-amp gap. GD's primary damage-amplification mechanics are Resistance Reduction (RR) auras, curses, and item proc debuffs — not an ailment in the traditional sense. GD kits with "life-reduction" ailments mapped (gd-vitality-conjurer, gd-bloody-pox-conjurer, gd-drain-essence-spellbinder) are vitality-element; their damage-amp vector is wither/life-reduction overlap. The RR flavor (e.g., Revenant constellation's -% resistance devotion proc) is a passive persistent debuff, not a time-limited ailment. gd-panettis-mage-hunter carries shock rider; gd-stormbox-elementalist carries shock rider — both are lightning kits accessing PoE-analog shock via their element.

*Magnitude note:* not-in-facts. `training-knowledge, verify at session:` GD RR values vary by source; -% physical/elemental resistance devotion procs typically range -20% to -50% resist; some item affixes provide flat RR auras.

**Pattern D — Mark-and-consume (PoE2 combo prerequisite)**  
PoE2 extends Pattern A into prerequisites. poe2-titan-hotg (armor-break) is the clearest case: armor-break is prerequisite — "without fully broken armor, Hammer does less damage." [kit: poe2-titan-hotg; family: geo_text]. poe2-tempest-bell (shock+stun rider) buffs via bell-ringing mechanic. poe2-erasure-edc-lich carries chaos-exposure (resistance reduction analog). The PoE2 suite shows a trend toward damage-amp as gated trigger (cf. GX-03 mark-and-consume pattern) rather than passive uptime debuff.

**Pattern E — Doom / delayed-burst (Hades1)**  
hades1-ares-doom: "Tag-bank-payout grammar: the 'bank' is the Doom window; the 'payout' is detonation... hit-now-damage-later archetype." [kit: hades1-ares-doom; JSONL mechanics_notes]. Doom applies a damage burst on expiry; the hit that applies it is a form of damage-amp (the burst is the amplified payout). hades1-merciful-end: "Pair-grain-capstone: Athena deflect + Ares Doom tag. When Zagreus deflects a projectile, Doom is INSTANTLY triggered on the source enemy — bypassing Doom's normal delay." [kit: hades1-merciful-end; JSONL mechanics_notes]. hades2-glorious-disaster (Zeus+Apollo duo, post-cutoff): "Boss-shredder" channeled lightning loop with post-cutoff conf ≤0.50.

**Pattern F — Class-specific damage rider (LE necrotic-weakness)**  
LE necrotic kits (le-reaper-form-lich, le-harvest-lich, le-wraithlord-necro) carry necrotic-weakness rider. LE Necrotic Weakness = a resistance-reduction debuff specific to necrotic/void element. le-erasing-strike-vk carries void-corruption + time-stop; le-warpath-vk carries void-corruption. le-dive-bomb-falconer carries "exposed" ailment — physical resistance reduction (armor exposure). These are element-specific resist-reduction flavors functionally equivalent to damage-amp but not a universal debuff.

**Pattern G — Wither (chaos DoT + resistance shred, PoE1)**  
All PoE1 poison/chaos kits (poe1-caustic-arrow, poe1-toxic-rain, poe1-viper-poison, poe1-bane, poe1-edc, poe1-hexblast-mines, poe1-hoag, poe1-scourge-arrow, poe1-dark-pact, poe1-cwdt-loop, poe1-ward-loop, poe1-poison-bv, poe1-deaths-oath, poe1-forbidden-rite, poe1-soulrend, poe1-pconc, poe1-venom-gyre) carry wither as a rider alongside poison. Wither in PoE1 is a stacking chaos resistance reduction debuff (applied by Withering Step or Wither totem). The combination of poison DoT + wither (resistance shred) constitutes the damage-amp layer for chaos/poison kits.

### 1c — Magnitude / stacking / duration conventions

| Game | Mechanic name | Magnitude | Stacking | Duration | Source |
|---|---|---|---|---|---|
| PoE1 | Shock | % increased damage taken, scales with lightning hit | Single ailment, magnitude varies | ~2–4s base | not-in-facts; `training-knowledge, verify at session` |
| PoE1 | Wither | -% chaos resistance, stacks 15 times | Stacking to cap | 2s per stack refreshed | not-in-facts; `training-knowledge, verify at session` |
| D4 | Vulnerable | 20% increased damage taken (flat) | Single status, no stack | 2–4s window | not-in-facts; `training-knowledge, verify at session` |
| GD | Resistance Reduction | -% elemental/physical resist (varies by source) | Multiple RR sources stack up to resist floor | Persistent while in range / timed proc | not-in-facts; `training-knowledge, verify at session` |
| LE | Necrotic Weakness / Exposed / Void-Corruption | % resistance reduction (element-specific) | not-in-facts | not-in-facts | probe facts only carry ailment name |
| Hades1 | Doom | Fixed burst damage payout on expiry | Multiple Doom stacks apply independently | Brief delay window (varies by boon) | geo_text + mechanics_notes [hades1-ares-doom] |

### 1d — Cross-game convergence / divergence

**Convergence:** Every T1 ARPG in the corpus has a damage-amp layer. The pattern is universal — the genre agrees that "taking more damage" debuffs on enemies are as fundamental as DoTs. Lightning is the dominant host element (PoE1/PoE2/D4/GD/LE/Hades all associate shock/amp with lightning; 67 of 100 gap-citations are lightning-element kits). This is strong cross-game signal that damage-amp and the lightning element are deeply paired in genre expectation.

**Divergence:** Three distinct mechanical philosophies: (A) scaling-with-hit-magnitude (PoE1 shock — a live calculation based on the hit that applied it); (B) flat-window (D4 Vulnerable — simple timer, no scaling); (C) stacking-resist-reduction (GD RR — additive reduction up to a floor, layered across multiple sources). The genre does not agree on HOW to implement damage-amp, only that it must exist.

**Second divergence:** PoE1 shock is element-specific (lightning only); D4 Vulnerable is element-agnostic; GD RR is split by damage type (physical resist, elemental resist, chaos resist track separately). The design session must decide: element-locked or universal?

---

### 1e — GX-15 Exhibits (multi-element cap collisions, folds into damage-amp design)

From pipeline spec v2 §6: GX-15 = "Multi-element cap collisions" with exhibits: D2-10 (Avenger), PoE1 (Discharge, Golementalist, Wild Strike), and Privileged Status as "the cap authored at exactly 2, shipped in both Hades games." [pipeline-spec-v2.md line 74, 173]

**GX-15 exhibit 1 — PoE1 Discharge**  
Discharge (not in corpus as standalone kit; referenced as GX-15 exhibit): consumes charges of multiple types (power, frenzy, endurance) for a massive combined elemental nova. The multi-element collision is: each charge type contributes different elemental damage; consuming all three produces a blended explosion. This is element-additive at the detonation event.

**GX-15 exhibit 2 — PoE1 Wild Strike**  
Wild Strike = stochastic element selection (GX-12 relationship). Every hit randomly picks one element. Multi-element collision is statistical: the build encounters all elements' ailments over a run. Cited as GX-15 exhibit per pipeline spec (Wild Strike noted in both GX-12 and GX-15 — it spans both slots).

**GX-15 exhibit 3 — Hades1/Hades2 Privileged Status (mechanized cap)**

This is the corpus's direct system-record for the mechanic. Full record from `hades1-privileged-status`:

> "Privileged Status: any enemy afflicted with two or more status effects simultaneously receives bonus damage from all sources. The game mechanizes multi-element synergy: stacking ailments becomes the prerequisite for a universal damage multiplier." [kit: hades1-privileged-status; family: geo_text]

Economy facts: "No active resource — Privileged Status is a passive multiplier that auto-applies when 2+ status effects are present on an enemy. Proc grammar: condition (2+ statuses) → bonus damage payout." [family: economy]

The record spans both games: "Hades I (2020) introduced it; Hades II (2024+) carried it forward." [JSONL mechanics_notes]

Pipeline spec §9.13 notes: "GX-15 hearing gains the mechanized exhibit: Privileged Status = the cap authored at exactly 2, shipped in both Hades games." [pipeline-spec-v2.md line 173]

**GX-15 divergence note:** Hades1 caps at 2 statuses (clean binary gate). PoE1 Discharge scales with count of consumed charges (incremental). These represent the two architectural poles for multi-element threshold design: binary-gate vs incremental-stack.

---

### 1f — Hades1 Privileged Status — ailment-synergy precedent exhibit

The corpus routes `hades1-privileged-status` as `row_class=system-record`, `route=ailment-synergy`. It is the genre's most explicit mechanization of the question "why stack different elements' ailments."

**Corpus record summary:**
- `kit_id`: hades1-privileged-status  
- `folk_name`: Privileged Status (mechanized cap)  
- `game`: hades1; `tier`: T2  
- `row_class`: system-record; `route`: ailment-synergy  
- `delivery`: other (meta-mechanic, not a castable skill)  
- `footprint`: other (per-hit, no spatial footprint)  
- `amp_val`: flat (consistent bonus applied to all qualifying hits)  

**Key mechanic facts:**  
The 2-status gate is a flat damage multiplier applied universally to all damage sources when an enemy carries 2+ distinct status effects simultaneously. This incentivizes cross-god/cross-element boon stacking over single-element investment. The rank1 upgrade: "Certain boons increase the Privileged Status bonus damage multiplier." — confirming the multiplier itself is a scalable design parameter.

**Hades2 extension:** hades2-hail-storm (Zeus+Demeter duo) explicitly satisfies Privileged Status as a design feature: "Cold + lightning cross-element synergy satisfying Privileged Status." [geo_text, hades2-hail-storm]. The cross-element design intent is authored at the boon level — the duo capstone is designed to produce 2-status-effect states specifically to trigger the multiplier.

**Consumption-target note for design session:** Privileged Status is the genre's answer to "why stack ailments." If the engine's ailment-synergy design follows this precedent, damage-amp becomes the reward for multi-ailment stacking. This is additive to (not in conflict with) the question of whether damage-amp is also a standalone ailment applied by specific skills.

---

## Chapter 2 — GAP-AILMENT: freeze

### 2a — Kit census

**Total kits citing freeze gap: 43** (~9.3% of 463 combat kits).

**By game and tier:**

| Game | Tier | Kit count |
|---|---|---|
| poe1 | T1 | 13 |
| undecember | T2b | 3 |
| gd | T1 | 4 |
| d2 | T1 | 3 |
| le | T1 | 3 |
| tq | T2 | 1 |
| tq2 | T2 | 1 |
| chronicon | T2 | 1 |
| d3 | T1 | 1 |
| d4 | T1 | 2 |
| di | T2b | 1 |
| hades2 | T2 | 1 |
| hot | T3 | 1 |
| tl2 | T2 | 1 |
| tli | T2 | 2 |
| vs | T3 | 2 |

**Full kit list by game:**

**chronicon (T2):** chr-frost-berserker (Frost Shatter Berserker)

**d2 (T1):** d2-frost-bowazon (Frostmaiden), d2-frozen-orb-sorc (Frozen Orb Sorceress), d2-blizzard-sorc (Blizzard Sorceress)

**d3 (T1):** d3-mundunugu-sb (Mundunugu Spirit Barrage)

**d4 (T1):** d4-frozen-orb (Frozen Orb Sorcerer), d4-ice-shards (Ice Shards Sorcerer)

**di (T2b):** di-ray-of-frost-wizard (Ray of Frost Wizard)

**gd (T1):** gd-roh-infiltrator (Rune of Hagarrad Infiltrator), gd-shadow-strike-infiltrator (Shadow Strike Infiltrator), gd-trozan-druid (Trozan's Sky Shard Druid), gd-berserker-wereforms (Berserker FoA mastery)

**hades2 (T2):** hades2-hail-storm (Hail Storm, Zeus+Demeter duo)

**hot (T3):** hot-norseman-frost-avalanche (Frost Avalanche Norseman)

**le (T1):** le-frost-claw (Frost Claw Sorcerer), le-frost-wall-rm (Frost Wall Runemaster), le-erasing-strike-vk (Erasing Strike Void Knight)

**poe1 (T1):** poe1-coc-ice-nova, poe1-autobomber, poe1-frost-blades, poe1-ice-shot, poe1-winter-orb, poe1-freezing-pulse, poe1-cold-dot-occ, poe1-icicle-mines, poe1-glacial-cascade-mines, poe1-skeleton-mages, poe1-whispering-ice, poe1-aegis-max-block, poe1-aurastacker

**poe2 (T1):** poe2-ice-strike-invoker (Ice Strike Invoker), poe2-cof-comet (Cast on Freeze Comet)

**tl2 (T2):** tl2-hailstorm-embermage (Hailstorm Embermage)

**tli (T2):** tli-gemma-frost-caster (Gemma Frost Caster), tli-erika3-vendetta (Erika 3 Vendetta's Sting)

**tq (T2):** tq-ice-shard-oracle (Ice Shard Oracle)

**tq2 (T2):** tq2-stormblade-ice-shards (Stormblade Ice Shards)

**undecember (T2b):** ud-ice-crystal-arrow, ud-snowstorm-frost, ud-cwc-spin-caster

**vs (T3):** vs-infinite-corridor-crimson-shroud (death-kill tech), vs-out-of-bounds-freeze

### 2b — Implementation-pattern table

**Pattern A — Full immobilization + shatter (PoE1/PoE2/D4/D2)**  
The dominant genre pattern: freeze = full movement and action immobilization, timed. Frozen targets shatter on heavy cold hit for burst damage. PoE1/PoE2 freeze is a buildup mechanic — cold damage accumulates against a threshold; when threshold crossed, freeze triggers.

poe1-coc-ice-nova: "Cyclone crits machine-gun Ice Novas through Cast-on-Crit and Cospri's Malice — attack RATE becomes cast RATE." [geo_text] Freeze rider, centrality=none — freeze is a bonus of cold coverage, not the primary loop goal.

poe2-ice-strike-invoker: "Quarterstaff cold flurry freezes packs, then heavy hits SHATTER the frozen — PoE2's Monk freeze identity kit since 0.1. Freeze=core: shatter = the damage payoff for the freeze buildup." [JSONL mechanics_notes]. Control centrality=core. Two-phase loop: freeze → shatter.

poe2-cof-comet: "Freeze buildup auto-triggers meteor-grade Comets through the Cast-on-Freeze meta-gem. Control=core: freeze is the trigger and prerequisite, not a rider ailment." [JSONL mechanics_notes]. Cast-on-Freeze is an ailment-as-proc-trigger implementation — freeze triggers a secondary skill automatically.

d2-frozen-orb-sorc: freeze rider, centrality=none — Frozen Orb's freeze is background; the orb travels and sprays radial bolts regardless.

d4-ice-shards: "Machine-gun ice shards that seek FROZEN targets automatically — freeze the pack, watch the volley redirect itself into the statues." [geo_text]. Freeze here gates a secondary behavior (auto-targeting of frozen enemies), not just damage.

**Pattern B — Freeze as prerequisite for loop (PoE2 Cast-on-Freeze grammar)**  
poe2-cof-comet is the clearest example of freeze-as-trigger-gate. The mechanic is: freeze threshold fills → auto-fire Comet. This is GX-03 mark-and-consume applied to freeze. [kit: poe2-cof-comet; family: geo_text]. The design implication: freeze is not only a control ailment; in advanced implementations it is an economy resource (builds toward proc threshold).

**Pattern C — Freeze as secondary to chill (genre's consistent hierarchy)**  
All D2/D4/PoE1 cold kits map both chill AND freeze. Chill precedes freeze — slow before hard lock. D2-frozen-orb-sorc, d2-blizzard-sorc, d4-frozen-orb, d4-ice-shards, le-frost-claw, le-frost-wall-rm all carry `ailments: ["chill", "freeze"]`. This is cross-game consensus: cold element applies chill at low magnitude, freeze at high magnitude. The engine already has chill (soft_control) — freeze is its hard-lock counterpart, completing the cold element's two-tier control spectrum.

**Pattern D — Freeze as wall / terrain interaction (LE Frost Wall)**  
le-frost-wall-rm: "Runemaster places a wall of ice segments at targeted position. The wall creates a physical lane barrier that blocks movement and projectiles, chills/freezes passing enemies." [geo_text]. This is freeze-as-geometry — the ailment is embedded in a terrain feature. Unique to LE in this corpus; no other game captures freeze-as-terrain-segment.

**Pattern E — Freeze as Hades2 cross-element trigger (hades2-hail-storm)**  
hades2-hail-storm: "Freeze effects repeatedly trigger lightning bolts. Control converted into a damage engine — each Freeze status refreshes triggers additional lightning." [geo_text]. Freeze is the damage engine here; each freeze application is a proc trigger for lightning. Also satisfies Privileged Status (2-status condition: freeze + shock simultaneously). [post-cutoff, conf ≤0.50]

### 2c — Magnitude / stacking / duration conventions

| Convention | Evidence |
|---|---|
| Freeze gates full immobilization (no movement, no action) | Cross-game consensus across D2/D4/PoE1/PoE2/LE/GD |
| Chill precedes freeze on the cold damage spectrum | All cold kits carry chill+freeze paired; chill appears at lower cold intensity |
| Shatter on death while frozen = burst damage bonus | D2 (shattering strike visual), PoE (frozen shatter on overkill kill), PoE2 Ice Strike explicit in notes |
| Freeze duration range | not-in-facts; `training-knowledge, verify at session:` genre range ≈ 0.5–4s; scales with cold overkill magnitude in PoE |
| Freeze as buildup threshold (not single-hit) | PoE1/PoE2 explicit; D2 less clear |
| Freeze-as-trigger (proc on freeze application) | PoE2 Cast-on-Freeze; Hades2 Hail Storm; newer games favor this grammar |

### 2d — Cross-game convergence / divergence

**Convergence (strongest signal):** Freeze = the hard-lock escalation of chill. Every cold element in the corpus maps chill+freeze as a pair. The engine's current chill (soft_control) creates an implicit demand for freeze (hard_control) as the cold element's completion. 13 T1 games represent this pattern.

**Convergence (second signal):** Freeze-then-shatter as a two-phase damage loop is present in PoE1, PoE2, D2, D4, LE, and Chronicon. The genre agrees that frozen enemies should have a payoff mechanic (burst on shatter) not just a control window.

**Divergence:** The trigger-grammar (freeze-as-proc-source, PoE2/Hades2) is a modern evolution not present in D2/D3. Older games use freeze as pure immobilization. Newer games use freeze as an economy trigger that fires secondary effects.

---

## Chapter 3 — GAP-AILMENT: stun

### 3a — Kit census

**Total kits citing stun gap: 36** (~7.8% of 463 combat kits).

**By game and tier:**

| Game | Tier | Kit count |
|---|---|---|
| hot | T3 | 6 |
| tq | T2 | 4 |
| d2 | T1 | 4 |
| poe2 | T1 | 4 |
| hades1 | T2 | 3 |
| hades2 | T2 | 1 |
| le | T1 | 2 |
| di | T2b | 2 |
| chronicon | T2 | 1 |
| d3 | T1 | 1 |
| gd | T1 | 1 |
| poe1 | T1 | 1 |
| tl2 | T2 | 1 |
| tli | T2 | 1 |
| tq2 | T2 | 1 |
| undecember | T2b | 1 |
| vs | T3 | 2 |

**Full kit list by game:**

**chronicon (T2):** chr-fulmination-templar (also in damage-amp)

**d2 (T1):** d2-ghost-pvp (Ghost), d2-singer (Singer), d2-bvc (BvC), d2-smiter (Smiter)

**d3 (T1):** d3-manald-heal (Manald Heal Paralysis; also in damage-amp)

**di (T2b):** di-monk-sss (Seven-Sided Strike Monk), di-hota-wotb-barb (HotA Burst Barbarian)

**gd (T1):** gd-canister-saboteur (Canister Bomb Saboteur)

**hades1 (T2):** hades1-beowulf-cast (Beowulf Cast Build), hades1-athena-dash (Athena Divine Dash Core), hades1-zeus-chain (Zeus Chain-Lightning Core; also in damage-amp)

**hades2 (T2):** hades2-glorious-disaster (Zeus+Apollo duo; also in damage-amp)

**hot (T3):** hot-kugelblitz (also in damage-amp), hot-cleric-radiant (Radiant Aura Cleric), hot-astronomer-orbs (Astronomer's Orbs), hot-shieldmaiden-block (Block-Stack Shieldmaiden), hot-meteor-strike (Meteor Strike), hot-landsknecht-grenades (Grenade Landsknecht)

**le (T1):** le-manifest-armor (Manifest Armor Forge Guard), le-smite-paladin (also in damage-amp)

**poe1 (T1):** poe1-heavy-strike-stun (Heavy Strike Stun Berserker)

**poe2 (T1):** poe2-tempest-bell (also in damage-amp), poe2-witchhunter-grenades (Grenadier Witchhunter), poe2-warbringer-totems (Ancestral Totem Warrior), poe2-titan-hotg (Hammer of the Gods Titan; also in damage-amp)

**tl2 (T2):** tl2-flame-hammer-engineer (Flame Hammer Engineer)

**tli (T2):** tli-rehan-berserker (Rehan Berserker Melee)

**tq (T2):** tq-phantom-strike-dreamkiller, tq-distortion-templar, tq-dream-harbinger, tq-shield-charge-conqueror

**tq2 (T2):** tq2-bastion-tank (also in taunt)

**undecember (T2b):** ud-lightning-vortex (also in damage-amp)

**vs (T3):** vs-unholy-vespers (Unholy Vespers, King Bible evo), vs-thunder-loop (also in damage-amp)

### 3b — Implementation-pattern table

**Pattern A — Physical heavy hit stun (universal physical pattern)**  
The broadest stun pattern: high-damage physical hits exceed a stun threshold and apply brief immobilization. d2-smiter: "Smite shield-bashes with auto-hit, stun, and crushing-blow percent-HP shred — THE uber-boss executioner role build." [geo_text]. d2-singer: "Caster barbarian: War Cry stun-nukes in a radius off mana." [geo_text]. poe1-heavy-strike-stun: "3.28 stun-scaling Heavy Strike Berserker holding curated tier-list placement — the long-dead single-target thwack reborn through a stun-damage loop." [JSONL mechanics_notes].

PoE1 stun is threshold-based: damage dealt relative to target max life. poe2-titan-hotg (armor-break → stun): "Armor-break setup into the ultimate falling hammer." [geo_text]. Stun here is paired to a prerequisite debuff (armor-break first).

**Pattern B — Lightning chain stun (shock-escalation)**  
Multiple lightning kits carry stun as an escalation of shock. hades1-zeus-chain: "Zeus boon converts any attack into a chain-lightning engine. Each hit forks lightning through nearby enemies — chain-hop geometry." Control: `ailments: ["shock", "stun"]`. [probe facts]. vs-thunder-loop: "Thunder Loop: evolved Lightning Ring fires random sky-strikes at enemy positions that hit TWICE per bolt." Control: shock+stun. [probe facts]. le-smite-paladin: shock+stun both as riders on a lightning proc-spam build. The pattern: lightning builds accrue both shock and stun; stun is the escalated form of shock-on-overload.

**Pattern C — Area/grenade stun (explosive physics)**  
gd-canister-saboteur: "Lobbed cluster bombs stun-locking packs under fragment rain." [geo_text]. Control: `ailments: ["burn", "stun"]` — fire + stun via explosive concussive force. poe2-witchhunter-grenades and hot-landsknecht-grenades follow the same geometry: thrown explosive → stun on impact. The stun here is not elemental but kinetic/concussive.

**Pattern D — Stagger / displacement variant (Hades vocabulary)**  
hades1-beowulf-cast: "Shield+bloodstone is then launched as a heavy ranged projectile that lodges in a struck enemy." Control: `ailments: ["stagger"]`, centrality=rider. Hades vocabulary uses "stagger" rather than "stun" — a brief interruption without full immobilization. The corpus maps this to the stun gap because the functional effect (interrupt, brief control) is equivalent. hades1-athena-dash carries stun via deflect mechanics.

**Pattern E — High-hit-impact stun (melee burst)**  
poe2-titan-hotg: control `ailments: ["stun", "armor-break"]`, centrality=core — stun is part of the core loop, not a rider. tq-phantom-strike-dreamkiller: "Phantom Strike teleports the caster to a target enemy and delivers a rapid sequence of melee strikes in a burst." Stun+slow riders. "Dreamkiller amplifies with Rogue poison/critical layers." [geo_text]. TQ stun is melee-impact based across multiple kits (distortion wave, dream harbinger, shield charge).

**Pattern F — Proc/hit-rate stun (HoT Tier 3)**  
HoT has 6 stun-gap kits, the highest single-game stun count. hot-cleric-radiant: stun rider on radiant aura. hot-astronomer-orbs: stun on orb impact. hot-meteor-strike: stun on impact explicitly. hot-shieldmaiden-block: stun on block-retaliation. hot-kugelblitz: "Crackling ball of lightning that WANDERS the field on its own path, zapping whatever it drifts past." Shock+stun from repeated hit contact. HoT's stun density suggests the game normalizes stun as a common rider across archetypes rather than a specialized kit feature.

### 3c — Magnitude / stacking / duration conventions

| Convention | Evidence |
|---|---|
| Stun = brief full action interrupt | Cross-game consensus |
| Duration typically short (0.3–2s) | not-in-facts; `training-knowledge, verify at session:` genre range 0.3–3s for on-hit stun |
| Stun threshold (% of max HP) — PoE model | poe1-heavy-strike-stun notes reference stun-scaling as explicit build investment |
| Stun immunity after first stun (diminishing returns) | not-in-facts; `training-knowledge, verify at session:` PoE1/PoE2 implement stun immunity timers |
| Lightning stun as shock escalation | hades1-zeus-chain, vs-thunder-loop, le-smite-paladin carry both shock+stun — suggests stun is shock's hard-control counterpart |
| Stagger (Hades) vs stun distinction | "Stagger" is partial interrupt; "stun" is full immobilization — overlapping control registers |

### 3d — Cross-game convergence / divergence

**Convergence:** Stun is consistently a brief hard-control (full interrupt). Every game in the corpus implements it as a physical-impact or heavy-hit consequence. The genre agrees: heavy hits should stop enemies cold momentarily.

**Convergence (second signal):** Lightning builds consistently accrue both shock and stun. The engine's current shock (hard_control, paralysis-on-arc) is already the lightning stun analog. The gap may partially resolve if the engine's shock is repositioned or if stun is implemented as a higher-magnitude shock variant.

**Divergence:** Implementation threshold varies widely — PoE1 is HP-% threshold, D2 is per-hit, HoT normalizes it as a common rider. No cross-game agreement on what triggers stun beyond "big hit or rapid hits."

**Note for design session:** The engine currently has shock defined as "paralysis-on-arc; brief immobilization triggered by chain-arc damage." This is effectively the genre's stun (brief hard control from lightning chain). The gap between engine-shock and genre-stun may be smaller than the census implies — but the 36 stun-gap kits include many non-lightning physical archetypes where the engine has no equivalent.

---

## Chapter 4 — GAP-AILMENT: poison-dot

### 4a — Kit census

**Total kits citing poison-dot gap: 36** (~7.8% of 463 combat kits).

**By game and tier:**

| Game | Tier | Kit count |
|---|---|---|
| poe1 | T1 | 17 |
| d2 | T1 | 4 |
| d3 | T1 | 2 |
| d4 | T1 | 3 |
| chronicon | T2 | 3 |
| le | T1 | 1 |
| gd | T1 | 1 |
| tq | T2 | 2 |
| poe2 | T1 | 2 |
| undecember | T2b | 1 |

**Full kit list by game:**

**chronicon (T2):** chr-bee-warden (Bee Swarm Warden), chr-bloodbinder-warlock (Bloodbinder Warlock), chr-plague-curse-warlock (Plague Mage / Desecrator Curse Warlock; also curse/hex gap)

**d2 (T1):** d2-poison-javazon (Poison Javazon), d2-poison-nova-necro (Poison Nova Necromancer), d2-daggermancer (Daggermancer), d2-rabies-wolf (Rabies Wolf)

**d3 (T1):** d3-jade-harvester (Jade Harvester), d3-zuni-carnevil (Zunimassa Carnevil)

**d4 (T1):** d4-andariel-flurry (Andariel Flurry Rogue), d4-touch-of-death (Touch of Death Spiritborn), d4-rabies-lacerate (Rabies Lacerate Druid)

**gd (T1):** gd-doom-bolt-sentinel (also in damage-amp)

**le (T1):** le-swarmblade-druid (Swarmblade Druid)

**poe1 (T1):** poe1-pconc (also in damage-amp), poe1-venom-gyre (also in damage-amp), poe1-viper-poison (also in damage-amp), poe1-caustic-arrow (also in damage-amp), poe1-toxic-rain (also in damage-amp), poe1-scourge-arrow (also in damage-amp), poe1-dark-pact (also in damage-amp), poe1-cwdt-loop (also in damage-amp), poe1-ward-loop (also in damage-amp), poe1-bane (also in damage-amp), poe1-poison-bv (also in damage-amp), poe1-deaths-oath (also in damage-amp), poe1-hexblast-mines (also in damage-amp), poe1-edc (also in damage-amp), poe1-soulrend (also in damage-amp), poe1-hoag (also in damage-amp), poe1-forbidden-rite (also in damage-amp)

**poe2 (T1):** poe2-poison-pathfinder (Poison Pathfinder), poe2-gas-arrow-ignite (Gas Arrow Detonation)

**tq (T2):** tq-warlock-poison-vitality (Warlock, Rogue+Spirit), tq-brigand-poison (Poison Brigand)

**undecember (T2b):** ud-toxic-flame (Toxic Flame DoT)

### 4b — Implementation-pattern table

**Pattern A — Stacking poison DoT (PoE1 standard)**  
PoE1 poison = chaos damage over time. Stacks independently: each application is a separate DoT instance. poe1-viper-poison: "Fast poison-stacking strikes where kills burst remaining poison to neighbors — DoT melee with contagion pops." [geo_text]. poe1-caustic-arrow: "Arrow leaves a caustic ground cloud ticking chaos DoT — the original ground-DoT bow archetype." [geo_text]. poe1-toxic-rain: "Arrows rain pods that slow and tick chaos DoT in overlapping zones — the perennial low-budget league-start king." [geo_text]. The stacking model means DPS scales with application rate — more hits = more poison stacks running simultaneously.

poe1-edc: "Essence Drain ticks chaos DoT; Contagion makes the DoT JUMP to neighbors on death — a two-button plague that clears rooms by spreading." [geo_text]. This is the contagion sub-pattern: poison that propagates on kill.

**Pattern B — DoT-stack-consume (D3 Jade Harvester)**  
d3-jade-harvester: "Stack Haunt and Locust Swarm DoTs, then Soul Harvest CONSUMES them — detonating years of future damage in one instant; the genre's cleanest DoT mark-and-consume." [geo_text]. This is GX-03 applied to poison/DoT: accumulate stacks, then trigger burst detonation. The D3 pattern is authored (set bonus drives the mechanic); it is the archetype for "DoT as resource to detonate."

**Pattern C — Contagion-spread (Rabies lineage)**  
d2-rabies-wolf: "Werewolf bite spreads a contagious poison that jumps target-to-target; DoT plague delivered by a shapeshifted melee body." [geo_text]. d4-rabies-lacerate: "Werewolf contagion returns — RABIES, the D2 wolf's plague bite, resurfaces as a D4 S-tier." [geo_text]. The Rabies lineage (`lineage: genre/rabies`, per pipeline-spec references `genre/contagion` rename candidate) spans D2→D4→LE (Swarmblade is cited as le-swarmblade-druid with poison+slow). This is the genre's oldest contagion archetype; it is load-bearing across 25+ years of ARPG design.

chr-bloodbinder-warlock: "Blood-bound entities powered by own HP drain." Control: `ailments: ["poison", "bleed"]` [probe facts] — poison+bleed combined on a summoner chassis.

**Pattern D — Ground poison cloud (chaos ground zone)**  
poe1-caustic-arrow, poe2-gas-arrow-ignite: ground-zone poison delivery. The cloud persists and ticks any enemy standing in it. "Arrow leaves a caustic ground cloud" [geo_text, poe1-caustic-arrow]. This is distinct from stacking-DoT: it's a ground hazard with fixed tick rate, not per-hit accumulation.

**Pattern E — Wither companion (PoE1 chaos/poison)**  
All PoE1 chaos/poison kits carry wither as a second ailment alongside poison (poe1-caustic-arrow, poe1-toxic-rain, poe1-bane, poe1-edc, etc.: `ailments: ["poison", "wither"]`). Wither = stacking chaos resistance reduction. This pairing is strong PoE1 genre signal: poison DoT is routinely paired with a resist-shred debuff to amplify its damage. The implication for engine design: poison-dot and a resistance-reduction ailment are frequently co-deployed.

**Pattern F — Summoner-hosted poison (poe1-hoag, chr-bee-warden)**  
poe1-hoag: "YOUR poison hits do nothing but feed virulence stacks to a scorpion crawler pet who does ALL the killing — the player is the pet's ammunition." [JSONL mechanics_notes]. chr-bee-warden: bee swarms applying poison as the primary vector. Poison delivered by proxy/pet; the player's role is poison-stack accumulation for the proxy to consume or to maintain stacks. This pattern intersects with taunt (summoner proxy = taunt-adjacent).

### 4c — Magnitude / stacking / duration conventions

| Convention | Evidence |
|---|---|
| Poison = chaos/nature DoT distinct from bleed (physical DoT) | Cross-game consensus: D2/D4/PoE/GD/LE all maintain separate poison and bleed channels |
| Stacking model (multiple simultaneous instances) | PoE1 standard; D2 Rabies is stacking; D4 Andariel Flurry stacks |
| DoT instance duration | not-in-facts; `training-knowledge, verify at session:` PoE1 poison ≈ 2s per application, refreshed by new applications |
| Contagion on death (spread mechanic) | D2 Rabies, PoE1 Contagion/Viper, D4 Rabies confirm the spread-on-kill sub-pattern |
| Wither (resist shred) commonly paired with poison in PoE | All PoE1 chaos/poison kits carry wither alongside poison |
| DoT-stack-burst detonation | D3 Jade Harvester, PoE1 Hexblast mines (curse+consume), PoE1 Bane (curse bundle) |

### 4d — Cross-game convergence / divergence

**Convergence (strongest):** Poison is a distinct DoT from fire/bleed. Every T1 game maintains it as a separate damage type — not synonymous with burn or bleed. The engine's current burn (fire dot) and bleed (physical dot) both exist; poison is the third pillar of the dot triad, representing the chaos/nature/corrosive element.

**Convergence (second):** Contagion-on-kill is a persistent design pattern across D2/D4/PoE1/PoE2 (spread on death). This is not universal but is notably recurrent — 5 separate game implementations of "poison jumps to nearby enemies when carrier dies."

**Divergence:** PoE1 implements poison as stackable chaos DoT (each hit is a separate instance). D3 implements it as a consumable resource (stack and detonate). D2 implements it as a single-tick DoT with fixed duration. The design session must choose a stacking model.

**Engine note:** The engine already has burn (fire dot) and bleed (physical dot) as the dot category. Poison-dot would complete a three-element dot triad. The existing param_range template (tick_damage dynamic from base_mag, duration range) already accommodates the mechanic class.

---

## Chapter 5 — Taunt Annex

### 5a — Kit census

**Total kits citing taunt gap: 11** (~2.4% of 463 combat kits). All carry proxy/summoner chassis.

**By game and tier:**

| Game | Tier | Kit count |
|---|---|---|
| chronicon | T2 | 3 |
| di | T2b | 2 |
| tl1 | T2 | 1 |
| tl2 | T2 | 2 |
| tli | T2 | 1 |
| tq | T2 | 1 |
| tq2 | T2 | 1 |

**Full kit list by game:**

**chronicon (T2):** chr-pet-warden (Pet Zoo Warden), chr-demon-legion-warlock (Demon Legion Warlock; also fear gap), chr-thorns-templar (Thorns Barrier Templar)

**di (T2b):** di-minion-necro (Minion Necromancer), di-druid-bear (Bear Druid, heal-shift)

**tl1 (T2):** tl1-alchemist-summoner (Summoner Alchemist)

**tl2 (T2):** tl2-shadowling-outlander (Shadowling Outlander), tl2-bot-engineer (Bot Summoner Engineer)

**tli (T2):** tli-moto-bots (Moto Bot Commander)

**tq (T2):** tq-petmaster-summoner (Petmaster Summoner)

**tq2 (T2):** tq2-bastion-tank (Bastion, Warfare+Forge; also stun gap)

### 5b — Kit patterns and proxy adjacency

**Primary pattern — Summoner proxy taunt:**  
8 of 11 taunt kits are summoner/proxy builds. Taunt in these games functions as the pet's aggro-generation mechanic — pets draw enemy attention away from the player. This is a companion AI directive, not a player-character ailment.

chr-pet-warden: "Zoo of pets fills the combat zone, each type contributing different attack patterns." Control: `ailments: ["taunt"]`, centrality=rider, conf=0.60. [probe facts].  
chr-demon-legion-warlock: "Demon army is the primary damage source; Warlock commands from a safe distance." Control: `ailments: ["taunt", "fear"]`, centrality=rider. [probe facts].  
di-minion-necro: "Summoned skeletons and golems spread across the combat area, attacking enemies throughout the zone." Control: taunt rider, centrality=rider. [probe facts].  
tl2-bot-engineer: "Bots move and attack independently, covering the entire combat zone." Taunt rider.  
tl1-alchemist-summoner: "Golem and zombie minions fight across the surrounding combat zone." Taunt rider.  
tq-petmaster-summoner: "Nature wolves, Spirit spectral minions fill the combat zone with proxy entities." Taunt rider.  

**Secondary pattern — Tank-identity taunt:**  
chr-thorns-templar: "Thorns Barrier Templar builds a powerful damage-reflection barrier. Enemies who attack the Templar suffer Thorns damage." Control: taunt centrality=core. This is the only non-summoner build where taunt is a core mechanic — it is a tank-lure design: the build wants to be attacked. [probe facts].  
tq2-bastion-tank (Warfare+Forge): taunt+stun, centrality=rider, very low conf (0.38/0.42 — post-cutoff EA). [probe facts].  
di-druid-bear: bear form with taunt as rider — melee tank using form to draw aggression.

**Pet/proxy adjacency note:**  
The engine's current system-record route structure includes a summoner wave. The taunt annex is commissioned to ride this wave. The functional need: pets/proxies that engage enemies need an aggro-direction mechanic. Whether taunt is an ailment applied to the enemy (forced to attack the taunting entity) or a behavioral flag on the pet (AI directive: this pet generates high threat) is a design decision outside this dossier's scope. The evidence shows the genre treats it as an enemy-targeting override: enemies switch attack targets toward the taunting pet.

**Solo-context note:** 10 of 11 taunt kits are proxy-heavy (pets, minions, bots, constructs). The one exception (chr-thorns-templar) is a tank-identity build. In solo ARPG solo contexts, taunt is always proxy-mediated (you send a pet to taunt) or tank-self-taunt (you want to be the target). There is no "target-swap on another player" taunt because the corpus is solo.

### 5c — Cross-game convergence / divergence

**Convergence:** Taunt = summoner kit rider. Every non-tank taunt kit is a proxy/summoner. The genre is consistent: taunt belongs to summoner archetypes and is their proxies' primary control contribution.

**Divergence:** Chronicon's Thorns Templar is the outlier — tank-identity taunt where the player themselves is the taunt source. This is rare; most games don't implement this outside multiplayer contexts (where it is a tank role mechanic).

**Taunt is not in the engine's current registry.** It is also the lowest-corpus-count gap among the five commissioned items (11 kits vs 97 damage-amp), and all 11 are Tier 2 or lower. The summoner-wave context explains the ride-along inclusion.

---

## Appendix — Key kit identifiers for design session reference

**Highest-signal kits for damage-amp design (recommend deep-dossier if needed):**
- poe1-lightning-conduit (ailment mark-and-consume; shock-scaled hit)
- hades1-privileged-status (system-record; multi-ailment multiplier gate)
- hades1-ares-doom (delayed payout grammar)
- poe2-titan-hotg (prerequisite amp: armor-break before burst)
- gd-vitality-conjurer / gd-drain-essence-spellbinder (vitality RR flavor)

**Highest-signal kits for freeze design:**
- poe2-ice-strike-invoker (freeze → shatter two-phase; centrality=core)
- poe2-cof-comet (freeze-as-proc-trigger; Cast-on-Freeze grammar)
- le-frost-wall-rm (freeze-as-terrain geometry)
- hades2-hail-storm (freeze → lightning engine; post-cutoff, dossier-owed)

**Highest-signal kits for stun design:**
- poe2-titan-hotg (armor-break prerequisite; centrality=core)
- d2-smiter (physical heavy-hit archetype; stun=auto-hit+crushing-blow package)
- hades1-beowulf-cast (stagger vocabulary variant)
- hot-kugelblitz (lightning stun from repeated contact; wandering proxy)

**Highest-signal kits for poison-dot design:**
- poe1-edc (contagion spread on kill; two-button plague)
- d3-jade-harvester (DoT-stack-burst detonation; genre's cleanest mark-and-consume)
- d2-rabies-wolf / d4-rabies-lacerate (contagion lineage, genre/rabies; 25yr span)
- poe1-hoag (summoner-hosted poison; virulence stack feeding)
- poe2-poison-pathfinder (PoE2 poison stack buildup; Pathfinder chassis)

---

*Evidence-only dossier — no design proposals, no engine-fit recommendations. Judgment belongs to the design session.*
