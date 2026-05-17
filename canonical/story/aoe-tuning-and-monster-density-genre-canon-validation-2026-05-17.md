# AOE Tuning + Monster Density — Genre-Canon Validation Briefing

**Authority:** gandalf (story-and-design steward). Pattern B briefing per knight-rider dispatch `2026-05-17-gandalf-aoe-tuning-genre-canon-validation.md` (Matt L3 routing decision 2026-05-17 — validate son's *"more monsters and more AOE moves"* feedback against ARPG canon BEFORE gamora hardcodes parameters into the post-D10 regen).
**Audience:** Matt (L3 review); gamora (post-D10 regen parameter consumer); knight-rider (sequencing); drax (AOE-indicator visual character downstream).
**Companion briefing:** `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` (the prior gandalf L3 brief; this briefing's § 5 hooks into that briefing's § 3 windup ranges).
**Tag intent:** `gandalf/v1.4-aoe-tuning-and-monster-density-canon-1`

**Reading order:** § 0 TL;DR → § 1 Why this matters → § 2 Surface 1 (AOE kit composition) → § 3 Surface 2 (monster density) → § 4 Surface 3 (AOE-radius / monster-spacing coupling) → § 5 Surface 4 (telegraph cognition budget) → § 6 Cross-impact map → § 7 Implementation parameter table → § 8 Open questions for Matt.

---

## § 0 — TL;DR

Son said *"more monsters and more AOE moves."* He was right on both counts, and he was naming the same thing both times: the engagement loop currently asks the player to fire AOEs at thin pack densities so the AOE feels like overkill on solo targets. **Two parameters move together, or the failure mode flips:** raise AOE-skill frequency without raising density and the player feels overarmed; raise density without raising AOE-frequency and the player feels overwhelmed. Genre canon resolves this with three load-bearing locks.

**The three locks (gamora's post-D10 envelope):**

1. **AOE kit composition: 40-60% of class kit is AOE-coded skills** (substrate-varying per § 2 table). Genre canon (D2/D3/D4/PoE/LE) clusters around 50% AOE at end-game; substrate identity modulates within a ±15% band. **Single-target skills stay load-bearing** — they kill elites/bosses and reward positioning; AOE clears trash and validates `geometry_affinities`.
2. **Monster density: 3-7 monsters per encounter at the perception-test target tier.** Pack composition: 1 elite (where present) + 2-6 trash adds. **TMPM (total-monsters-per-minute) target: 30-50** for the demo's 60-90sec fight context. This is *D4-nightmare-dungeon density,* not D3-rift density — substrate identity must remain perceptible, which is impossible at PoE-Delirium screen-spam levels.
3. **AOE-radius vs spacing coupling: target 3-5 monsters hit per AOE cast for medium-AOE skills; 6-10 for large-AOE.** Monster pack spawn-spread (~80-120 pixel radius around pack center per existing `packSpawnPositions`) must be tuned against substrate `geometry_affinities` so that fire `burst` (R≈100px) reliably hits 3-4 packed mobs while wind `cone` (length≈180px, width≈100px) reliably catches 4-5 in a line.

**Telegraphed-AOE cognition budget (§ 5):** *max 2 simultaneous enemy AOE telegraphs visible at any given moment.* PoE Delirium and D4-nightmare both demonstrate that 3+ simultaneous telegraphs in the player's field of view collapses positional play into prayer. With elite-tier-only telegraphs (per prior briefing § 3.1) and elite cap of 1 per encounter (next paragraph), the budget is naturally respected. Substrate-mixing in packs *is allowed and encouraged* at the trash tier (visual variety; teaches substrate vocabulary); restricted to substrate-coherent at the elite tier (the telegraph itself is the cosmological signal).

**§ 7 contains the gamora-implementable parameter table.** Eight rows; numerical; per-substrate where applicable.

---

## § 1 — Why this matters

Matt's son's feedback in focused-playtest test 6 was a two-clause sentence: *"need more monsters and more AOE moves."* The two clauses are not independent. They are the same observation expressed from two angles. The player perceived the engagement loop as **under-saturated relative to the AOE-coded kit the demo handed him**, AND **under-armed relative to the trash density the screen could hold.** Both gaps point to the same load-bearing dimension: the **AOE-radius ↔ monster-spacing coupling** that every mature ARPG tunes carefully and that the demo has not yet tuned at all.

The post-D10 regen is the right moment to tune this — gamora generates new kits + new monster spawn parameters in the same pipeline pass. Without grounding the parameters in genre canon, the regen ships first-guess values that will need re-tuning after the next playtest. Genre canon exists; the cost of consulting it is one briefing.

### § 1.1 — The four canonical failure modes (the design substrate this briefing prevents)

1. **Under-tuned AOE × under-dense monsters →** *"tagging single mobs."* The kit's AOE skills feel like overkill against 1-2 trash mobs; the player ends up using single-target skills out of habit. **Where the demo currently is.** Cosmological cost: substrate `geometry_affinities` never expressed in play (wind `cone` and fire `burst` resolve identically when hitting 1 target).

2. **Over-tuned AOE × under-dense monsters →** *"one button clears the screen."* The kit's AOE is so generous that the rare 2-mob group dies to one cast; the player learns "press AOE button" and stops reading the battlefield. **D3-vanilla failure mode (pre-Reaper-of-Souls).** Cosmological cost: substrate identity collapses into "do damage in a fixed area" regardless of substrate.

3. **Under-tuned AOE × over-dense monsters →** *"I die before I clear."* The kit's AOE cannot pace the spawn rate; the player kites infinitely and dies to attrition. **D2-Hell-Baal-runs failure mode for under-geared characters.** Cosmological cost: substrate identity erased by panic; player only perceives "I'm losing."

4. **Over-tuned AOE × over-dense monsters →** *"screen-spam; I can't see what's happening."* Every cast clears 12-15 mobs; particle effects and ground-indicators obscure the battlefield; substrate vocabulary is unreadable. **PoE-Delirium failure mode at high difficulty; D4-nightmare-dungeon failure mode at high tier.** Cosmological cost: substrate identity exists but is *cognitively unavailable* — the player cannot perceive what is happening fast enough to notice substrate differences.

**The recommendation in § 7 targets the centroid of the design space** — the small region where AOE feels rewarding (mode 2 avoided), density feels meaningful (mode 1 avoided), the player can pace the spawn (mode 3 avoided), and substrate identity remains legible (mode 4 avoided). This is a narrow target; the genre's mature ARPGs converge on similar values because the alternatives are bad.

### § 1.2 — Why the post-D10 regen is the correct lock point

Per the dispatch's pipeline ordering: gamora regen in flight → narrow-slice reactive escape AI (per prior briefing § 4) → D10 code (substrate-coherent generation rules) → post-D10 regen (the regen that consumes this briefing's parameters). The post-D10 regen has visibility into both the substrate-coherent generation outputs AND the narrow-slice telegraphed-combat substrate. **This briefing's parameters are tuned against both surfaces** — they assume telegraphed enemy AOEs (per prior briefing § 3) and reactive elite escape AI (per prior briefing § 4) are landing in the same regen-consuming engine state.

If the narrow-slice work slips, the parameters in § 7 still hold for the trash tier (the bulk of the density math). The elite-tier escape behavior shifts numerical optimum by ~5-10% in the spacing dimension, which is within the post-D10-regen tuning tolerance.

### § 1.3 — Connection to the D27 perception test

Substrate-coherent generation produces archetypes whose `geometry_affinities` differ across substrates. The D27 perception test asks whether players perceive these differences in 60-90 sec fights. **Spatial-combat substrate (prior briefing) is necessary; correct density-and-radius tuning (this briefing) is also necessary.** A fire-burst archetype hitting 1 mob per cast vs a wind-cone archetype hitting 1 mob per cast feels identical regardless of substrate; both archetypes hitting 4-5 mobs per cast in their substrate-coherent geometry feels substrate-distinct. **The D27 test will produce sharper signal with this briefing's parameters in place.**

---

## § 2 — Surface 1: AOE skill distribution in player kits — genre canon

### § 2.1 — End-game ARPG kit-composition canon

Different mature ARPGs converge on a similar 40-60% AOE share at end-game, varying by class fantasy:

| Game | Bar size | AOE share (canon) | Notes |
|---|---|---|---|
| **Diablo II (LoD)** | 1 right-click + 1 left-click hotkeys (full skill tree access) | ~40-70%; class-variable | Sorceress kits run 60-80% AOE (Frozen Orb / Blizzard / Meteor / Fire Wall / Hydra). Assassin kits run 30-40% AOE (Lightning Sentry being the main AOE; martial-arts trees are single-target with finishers). Necromancer ~50% (Corpse Explosion is the AOE workhorse; Bone Spear is single-target finisher). |
| **Diablo III (RoS)** | 6-slot bar (2 left, 4 right) | ~50%; generator+spender pattern | Canonical: 1-2 generators (often single-target or small-AOE like Hammer of the Ancients vs Whirlwind) + 3-4 spenders (almost always AOE-coded: Seismic Slam, Blessed Hammer, Disintegrate, Rain of Vengeance). Late D3 set-bonus builds homogenize toward 4-5 AOE skills. |
| **Diablo IV** | 6-slot bar | ~50-65% | Class fantasy more AOE-heavy than D3 (Sorcerer Arc Lash + Ball Lightning + Chain Lightning all AOE-coded; Druid Pulverize/Trample/Tornado AOE-heavy). Rogue is the single-target outlier (~40% AOE; Penetrating Shot + Rapid Fire single-target-leaning). |
| **Path of Exile** | Highly variable (skill gems; any number of skills) | ~50% map-clear; ~30% bossing | PoE explicitly splits the kit into "map skill" (AOE clear; often Tornado Shot, Spark, Lightning Conduit) + "boss skill" (single-target damage; often Vaal-of-X variants of the clear skill, or a dedicated single-target like Penance Brand or Boneshatter). The build *chooses* its ratio; canonical end-game build runs ~50% of skill-slots on AOE map-clear, ~30% on single-target boss. |
| **Last Epoch** | 5-slot bar | ~60%; specialization-driven | Skill specialization trees push most skills toward AOE (Avalanche, Hammer Throw, Storm Bolts converted to chain). Pure single-target builds exist but are minority; canon is "AOE-by-default with single-target conversion as opt-in." |
| **Grim Dawn** | 2-class hybrid; ~6-8 skills typical | ~40-55% | Two-class combinations skew the ratio; Demolitionist + anything = AOE-heavy (Grenado, Fire Strike, Stun Jacks, Blackwater Cocktail all AOE). Soldier + Nightblade = single-target-leaning. Genre median ~50%. |
| **Lost Ark** | 8-skill class roster | ~50-65% | Class-determined; Sorceress 70% AOE, Gunslinger ~40% AOE, most classes 50-60%. Mokoko stagger meta encourages mixed kits (some skills tagged "Stagger" — usually big AOE — kept for boss mechanics). |

**Canon-consensus: ~50% AOE share at end-game across the genre.** Class fantasy and substrate identity move this ±15% (substrates leaning AOE-heavy vs single-target-leaning). Pure single-target builds (<25% AOE) feel "sniper" — niche but legitimate. Pure AOE builds (>75% AOE) feel "screen-clear" but lose elite/boss reliability.

### § 2.2 — Phase-1 P1 implication: target proportion for substrate × role

Current state: gamora's generation produces **5-8 skills per class kit** (per existing generator). The recommendation: target **40-60% AOE-coded skills** with substrate × role modulation.

**Substrate-coupled AOE-share targets (anchored to `geometry_affinities` per `substrate-identity-declarations-2026-05-17.md`):**

| Substrate | AOE-share target | Reasoning (per substrate identity declarations) |
|---|---|---|
| **Fire** | **55-65%** | `combat_pillar: HIGH_BURST_LOW_PERSIST`; `geometry_affinities: burst PREFER + ground_targeted_circle PREFER + area_sustain PREFER + cone PREFER`. Fire is canonically AOE-heavy (D2 Sorc fire tree; D3 Wizard fire builds; PoE Detonate Dead / Volatile Dead). 55-65% honors the genre archetype. |
| **Water** | **65-75%** | `combat_pillar: SUSTAINED_PRESENCE_ZONE_DENIAL`; geometry leans area_sustain + ground_targeted_circle + wave. **Highest AOE-share of any substrate** — water is the *zone-control* substrate; nearly every water skill is AOE by cosmological commitment. Single-target water skills feel substrate-incoherent (water *suffuses* — it doesn't snipe). |
| **Earth** | **35-50%** | `combat_pillar: ANCHOR_AND_DISRUPT`; geometry mixes melee_arc + slam + pillar + ground_targeted_circle. Earth's identity admits *both* big-AOE (groundswell, earthquake) AND single-target-mass-strike (mountain-cleave). Lowest AOE-share of magical substrates; closest to genre-neutral mid-band. |
| **Wind** | **50-60%** | `combat_pillar: KINETIC_REDIRECTION`; geometry mixes cone + swirl + vortex_pull + projectile + line. Wind is AOE-leaning via cone/swirl but admits high-velocity single-target projectiles (D2 Druid Twister; PoE Tornado Shot's primary projectile). 50-60% is genre canon. |
| **Lightning** | **60-70%** | `combat_pillar: HIGH_BURST_LOW_PERSIST`; geometry leans branching + arc + bolt_line + chain_lightning. Lightning is canonically chain-AOE (D2 Sorc Lightning/Chain Lightning; D3 Wizard Arcane Orb; PoE Storm Brand). Single-target lightning exists (D2 Lightning Bolt) but is sub-canon; chain is the substrate's verb. |
| **Holy** | **40-55%** | `combat_pillar: REVELATION_AND_AMPLIFICATION`; geometry leans radiant_aura + shaft + nova + ground_targeted_circle + area_sustain. Holy admits both AOE (consecrate zones; nova) and single-target (smite; judgment). Support-leaning role (`role_affinities.support: 0.8`) keeps the AOE-share moderate — many holy skills are buff/heal, not damage. |
| **Shadow** | **45-60%** | `combat_pillar: CONCEALMENT_AND_DRAIN`; geometry leans tendril + void_pool + creep + area_sustain. Shadow is *DoT-zone-leaning* — drain-pool AOEs are canonical (D2 Necro Bone Spirit field; PoE Bane / Soulrend; Solo Leveling shadow-army). Moderate AOE-share; single-target drain skills also canonical (siphon spells). |

**Role modulation (overlay on substrate target):**

- **Damage role:** baseline substrate target (the table above).
- **Support role:** −10% AOE-share (more buffs/heals; fewer damage AOEs). E.g. holy_support → 30-45% AOE-share.
- **Control role:** +5% AOE-share (control skills are typically AOE — chill fields, root patches, fear waves). E.g. water_controller → 70-80% AOE-share.
- **Hybrid role:** baseline (no modulation).

**Total kit math (example):** A 6-skill water_controller kit targets ~75% AOE = 4-5 AOE skills, 1-2 single-target skills. The single-target skills serve elite/boss reliability; the AOE skills carry trash clearing.

### § 2.3 — AOE-character mix (not all AOE is the same)

Burst-AOE vs persistent-zone vs cone vs chain play very differently. Genre canon distinguishes them sharply, and substrate identity should determine the mix.

**AOE characters defined:**

| AOE character | Cast cost | Hit pattern | Genre exemplar |
|---|---|---|---|
| **Burst-AOE** | Instant; high frequency | Small radius (≈80-120px); 1-cast 1-hit | D2 Frozen Orb (final detonation); D3 Wizard Magic Missile's Glacial Spike rune; PoE Fireball |
| **Cone-AOE** | Instant or short windup; medium frequency | Medium length × medium width directional cone | D2 Druid Twister; D3 Witch Doctor Plague of Toads; PoE Shotgun-Tornado |
| **Persistent-zone-AOE** | Cooldown-gated; lower frequency | Large radius (≈150-220px); ground-bound; ticks for duration (2-6 sec) | D2 Sorc Blizzard; D3 Wizard Hydra; PoE Vortex |
| **Chain-AOE** | Instant; medium frequency | Single initial target, propagates to N nearby targets | D2 Sorc Chain Lightning; D3 Wizard Lightning Spectrum; PoE Spark / Lightning Conduit |
| **Nova-AOE** | Self-centered; cooldown-gated | Player-centered radial; large radius (≈180px); single tick | D2 Sorc Frost Nova; D3 Necro Death Nova; PoE Cast On Critical Strike Lightning Tendrils |
| **Line-AOE** | Instant or moderate windup; medium frequency | Long line through targets; medium width (≈60-80px) | D2 Lightning Bolt; D3 Disintegrate; PoE Lightning Conduit beams |

**Substrate-coupled AOE-character mix recommendations (anchored to substrate `geometry_affinities`):**

| Substrate | Canonical AOE character mix |
|---|---|
| **Fire** | 50% burst-AOE + 30% persistent-zone (fire-area-residue per D8 canonical fire pool) + 20% cone (flamethrower-coded) |
| **Water** | 60% persistent-zone (water is *the* zone substrate) + 20% nova (waves) + 20% burst (small ice burst) |
| **Earth** | 40% persistent-zone (consecrated ground; earth-spikes-field) + 30% nova (ground-slam) + 20% melee-arc (single-target-pack-hit) + 10% line (earth-spike-row) |
| **Wind** | 50% cone (wind's iconic geometry) + 25% line (gust-line) + 15% vortex_pull (suction; one of the most distinctive substrate geometries) + 10% burst (gust-pulse) |
| **Lightning** | 60% chain-AOE (substrate's verb) + 20% line (lightning-bolt) + 15% nova (discharge) + 5% burst |
| **Holy** | 35% nova (radiant burst) + 30% persistent-zone (consecrate ground) + 20% line (shaft-of-light) + 15% burst (smite-burst) |
| **Shadow** | 50% persistent-zone (drain pools; void zones) + 25% chain (creeping shadow propagation) + 15% nova (dark-pulse) + 10% line (shadow-tendril-line) |

**Why the character mix matters more than the AOE share:** A kit with 60% AOE share but all burst-AOE feels identical to a kit with 60% AOE share but all chain. The *character mix* is where substrate identity becomes mechanically perceptible. Two fire builds that both run 60% AOE but with different character mixes will read as substrate-coherent but archetype-distinct — exactly what the D27 perception test asks for at the H1 level.

### § 2.4 — Forward surface: AOE-share telemetry

Gamora's post-D10 regen should emit per-class **kit AOE-share** (count of AOE-coded skills / total skill count) into the telemetry stream. Jack-ryan validates against the targets in § 2.2; substrate identity declarations are the canonical source-of-truth for the targets. **This becomes a Layer-3 diversity-gate signal** — kits whose AOE-share falls outside the ±15% band of their substrate target are flagged for review.

This is a **forward-work surface**, not a Phase-1 P1 blocker. Surface as OBSERVATION; jack-ryan picks up after D14 mirror-match gate lands.

---

## § 3 — Surface 2: Monster density per encounter — genre canon

### § 3.1 — Pack size baseline across the genre

| Game | Trash pack size | Elite pack size | Mini-boss encounter | Density character |
|---|---|---|---|---|
| **Diablo II** | 4-8 standard mobs | 1-3 champions OR 1 unique + 2-3 minions | 1 unique + 0-3 retinue | "Pack of 6" was the LoD canonical reference |
| **Diablo III rifts** | 8-15+ (very dense) | 1 elite + 3-5 minions | 1 elite + 5-8 minions | D3 rift density is the genre's outlier high-bound |
| **Diablo III bounties** | 3-6 | 1 + 2-4 | 1 + 0-3 | More moderate; close to canon median |
| **Diablo IV dungeons** | 4-8 | 1 elite + 3-5 trash | 1 + 0-3 | "Helltide" events spike density to D3-rift levels temporarily |
| **D4 Nightmare Dungeons (T20+)** | 6-12 | 2-3 elites + 4-6 trash | 1 + 4-6 | Higher density; trades for visibility (well-known criticism) |
| **Path of Exile maps** | 3-6 per "pack" but many packs per zone | 1 rare (yellow) + 2-4 magic (blue) | Distinct boss room | Density varies by map mod and Atlas Tree configuration |
| **PoE Delirium/Breach** | Continuous spawn waves (no discrete packs) | 1-2 elites per wave | Specialized | Highest-density genre experience; explicit screen-spam zone |
| **Last Epoch monoliths** | 4-7 per pack | 1 rare + 2-4 magic | Echo boss room | Genre canon midpoint |
| **Grim Dawn** | 3-6 per pack; lower density overall | 1 hero + 2-4 trash | 1 + 0-3 | Lower-density-than-genre-median; slower-paced |
| **Lost Ark dungeons** | 5-12 | 1 elite + 5-8 trash | 1 + 0-4 | High density; close to D3 rift |
| **Lost Ark guardians** | 1 (single boss) | — | — | Pure boss; no density |

**Canon-consensus: 3-8 trash per encounter; 1-3 elites or 1 elite + 2-4 trash for elite encounters.** D3 rifts and PoE Delirium are intentional density outliers; mainstream ARPG canon clusters at **5-7 mobs per encounter.**

### § 3.2 — TMPM (total-monsters-per-minute) target

| Game | TMPM at canonical difficulty | TMPM at high difficulty |
|---|---|---|
| **D2 Hell-difficulty Baal-runs** | ~80-120 | ~150-200 (geared) |
| **D3 GR 70-80** | ~150-250 | ~300-500 at GR 100+ |
| **D4 NM Dungeon T15-25** | ~30-80 | ~80-150 at T50+ |
| **PoE T16 maps (regular)** | ~50-100 | ~150-300 (juiced; "headhunter MF" builds) |
| **PoE Delirium mirror-tier** | ~300-500 | ~500-800 (screen-spam) |
| **Last Epoch Empowered Monoliths** | ~40-80 | ~100-150 (corrupted) |
| **Grim Dawn Ultimate** | ~30-60 | ~60-100 |
| **Lost Ark Chaos Dungeons** | ~80-150 | — |

**Recommendation for the demo's perception-test target (60-90 sec fight):** **TMPM target 30-50.** This is **D4-nightmare-dungeon territory**, not D3-rift. Reasoning:

1. **Substrate identity legibility requires headroom.** PoE Delirium at 300-500 TMPM proves what is possible at the high end and *what the trade-off is*: substrate distinguishability collapses below the cognitive threshold of the player. The demo is testing *whether* substrates feel distinct; running the test at density that erases distinctness is testing the wrong thing.
2. **60-90 sec fight context.** TMPM 30 = 30-45 mobs killed per session. TMPM 50 = 50-75 mobs killed. The lower bound gives the player meaningful body-counts; the upper bound saturates the kit without overwhelming.
3. **Son's feedback was "more monsters," not "screen-spam."** Current state likely 10-20 TMPM (1-3 mobs per encounter, 4-6 encounters per minute). Bumping to 30-50 TMPM is 2-3× current; perceptually "more" without being "too many."
4. **Genre canon convergence.** D4-nightmare, Last Epoch Empowered, Grim Dawn Ultimate all cluster at 30-80 TMPM at canonical end-game difficulty. The demo's perception-test should sit in that band.

**Substrate coupling for density?** Limited but real:

- **Shadow regions ⇒ lower density, tougher individual monsters** (substrate identity: occlusion; concealment; shadow encounters should reward perception, not throughput). Target: 60-70% of baseline TMPM.
- **Fire regions ⇒ standard density** (substrate identity: escalation; fire is genre-canonical for waves).
- **Water regions ⇒ slightly lower density, more durable mobs** (substrate identity: suffusion; water-aligned mobs are slow-pressure, not high-frequency). Target: 80-90% of baseline.
- **Earth regions ⇒ standard density with elite-emphasis** (more elites per encounter; substrate identity: anchor; fewer trash, more bulwark-type mobs).
- **Wind regions ⇒ standard-to-slightly-higher density** (substrate identity: kinetic; wind regions are genre-canonical for swarms — D2 Hell Travincal swarm-and-skip).
- **Lightning regions ⇒ standard density** (no strong substrate-pull either way).
- **Holy regions ⇒ moderate density** (substrate identity: revelation; mobs declare themselves clearly; density doesn't obscure).

**Coupling implementation:** post-D10 regen seeds a `region_density_modifier` per substrate that gamora applies to the baseline TMPM. Range 0.6-1.1× of baseline. Default 1.0× if substrate doesn't have a strong tilt.

### § 3.3 — Pack composition: homogeneous vs heterogeneous

Two design strategies:

- **Substrate-homogeneous packs:** every monster in a pack shares the same substrate. Genre exemplars: D2 area-themed monster types (Cold Plains all skeleton-cold; Pandemonium all fallen-fire). Cognitive load: low; substrate vocabulary teaches quickly.
- **Substrate-heterogeneous packs:** monsters within a single pack span 2-3 substrates. Genre exemplars: D3 rifts (random mob composition); PoE map (modifier-driven). Cognitive load: high; visual chaos but maximum substrate-vocabulary exposure.

**Recommendation: 70% substrate-homogeneous packs + 30% substrate-heterogeneous packs (2-substrate mixing).** Reasoning:

1. **Substrate identity teaches via repetition.** A player who clears a pack of 6 fire-substrate mobs has 6 data points on fire's visual/mechanical signature. Mixed packs dilute the signal.
2. **30% mixed packs prevent monotony.** A pure-substrate game becomes predictable; mixed packs reward attention and create the *what kind of fight is this?* moment players love.
3. **No 3+-substrate packs in the perception-test build.** Three substrates in one pack = 3 different ailment types + 3 different attack patterns + 3 different VFX colors = cognitive overload at the perception-test cognition budget. Defer 3+-substrate packs to B13-proper or post-perception-test scope.
4. **Elite packs stay substrate-homogeneous** (the elite is the cosmological signal; mixing dilutes the "this is a Fire-Lord" read).

**Pack-composition rules for post-D10 regen:**

- 70% chance: pack substrate = dominant region substrate (homogeneous)
- 30% chance: pack substrate = dominant region substrate + 1 adjacent substrate (heterogeneous; 60% region / 40% adjacent split)
- "Adjacent" = paired substrate (fire/water; earth/wind; holy/shadow) OR unpaired-compatible (lightning composes with all) — per substrate-identity-declarations § 0 pairing summary
- **Forbidden mixing:** the `forbidden_hybrid_with` field per substrate (canonical-four anti-pole pairings) is honored at the pack-composition layer — no fire+water mixed packs, no earth+wind mixed packs. Holy/shadow CAN mix (they are amplification-pair, not erasure-pair, per substrate-identity-declarations § 6 + § 7).

---

## § 4 — Surface 3: AOE-radius vs monster-spacing coupling

### § 4.1 — The load-bearing math

The geometric relationship determining whether AOE feels good:

```
AOE hits ≈ (R / S)² × density_factor

where:
  R = AOE radius (skill's effective hit zone, in pixels)
  S = monster spacing (distance between adjacent monsters in the pack, in pixels)
  density_factor = 0.5 to 1.0 (depending on pack-cluster vs spread topology)
```

If R = 2S (AOE is 2× the inter-monster spacing), AOE hits ~4 monsters per cast in a clustered pack. If R = 0.5S, AOE hits ~0.25 monsters — *sometimes* 0, *sometimes* 1. The latter is the **"tagging single mobs"** failure mode of § 1.1.

### § 4.2 — Genre canon for the (R, S) target

Established ARPGs tune so that:

- **Medium-AOE skills** (R ≈ 100-150px in 2D-pixel coordinates) **hit 3-5 monsters per cast** in a standard pack.
- **Large-AOE skills** (R ≈ 180-260px) **hit 6-10 monsters per cast.**
- **Small-AOE skills / cone tips** (R ≈ 60-90px) **hit 1-3 monsters per cast.**

This requires monster-pack spacing S ≈ 50-80px center-to-center in standard packs. Tighter packs (S ≈ 30-50px) feel "clumped" and reward big-AOE disproportionately; looser packs (S ≈ 100-150px) feel "spread" and reward chain/projectile AOE over burst.

**Current demo state (per `packSpawnPositions` review):** pack spawn-spread is 60-180px depending on pack size. The spread *increases* with pack size, which is correct (more mobs need more room) but means the per-mob spacing stays approximately constant at S ≈ 60-90px for typical pack sizes of 3-6. **The demo's current spacing is genre-canon.** The fix is on the AOE-radius side: ensure substrate-coherent AOE radii fall in the right band.

### § 4.3 — Substrate-coupled AOE-radius targets

Per substrate `geometry_affinities` (from substrate-identity-declarations):

| Substrate | Primary AOE-character | Target R | Target hits/cast (standard pack S=70px) |
|---|---|---|---|
| **Fire** | burst (primary); persistent-zone (secondary); cone (tertiary) | Burst: R=100-120px; Zone: R=140-180px; Cone: 160px×80px | Burst: 3-4 mobs; Zone: 5-7 mobs; Cone: 3-4 mobs |
| **Water** | persistent-zone (primary); wave-nova (secondary) | Zone: R=180-220px (largest); Wave: R=160-200px | Zone: 8-12 mobs (sustained tick); Wave: 6-9 mobs (single tick) |
| **Earth** | persistent-zone (primary); nova (secondary); melee-arc (tertiary) | Zone: R=140-180px; Nova: R=150-180px; Arc: 100-130px sweep | Zone: 5-7 mobs; Nova: 6-8 mobs; Arc: 3-5 mobs |
| **Wind** | cone (primary); line (secondary); vortex_pull (tertiary) | Cone: 200px×100px; Line: 300px×60px; Vortex: R=120px attract | Cone: 4-6 mobs; Line: 4-6 mobs (longer reach, narrower); Vortex: pulls 4-6, then secondary damage |
| **Lightning** | chain (primary; arc-jumps); line (secondary); nova (tertiary) | Chain: R=100px per hop, 4-6 hops; Line: 250px×50px; Nova: R=140px | Chain: 4-6 mobs (one per hop); Line: 4-5 mobs; Nova: 4-6 mobs |
| **Holy** | nova (primary); persistent-zone (secondary); shaft-line (tertiary) | Nova: R=160-200px; Zone: R=140-180px; Shaft: 80px×280px (tall narrow) | Nova: 6-8 mobs; Zone: 5-7 mobs; Shaft: 3-4 mobs |
| **Shadow** | persistent-zone (primary); chain (secondary); nova (tertiary) | Zone: R=140-180px; Chain: R=80px per hop × 3-4 hops; Nova: R=130px | Zone: 5-7 mobs (slow-tick DoT); Chain: 3-4 mobs; Nova: 4-5 mobs |

**Design discipline:** the substrate's *primary* AOE-character should be the one that reliably hits 4-6 mobs per cast. Secondary characters can hit lower (2-4) — they're situational. Tertiary characters are flavor — single-mob-acceptable. **Match the radii to the genre median, not to the substrate's iconic-verbs poetry.** Players read the math; the cosmology is the poetry behind the math.

### § 4.4 — Encounter-design implication

Post-D10 regen's monster-spawn logic should produce packs where:

- **Mean inter-mob spacing S ≈ 70-90px** in standard packs (current demo state — preserve).
- **Pack cluster diameter D ≈ 150-220px** for a 5-7 mob pack (so the largest substrate AOEs at R≈200 can hit the full pack; medium AOEs hit 60-80% of the pack).
- **Pack-spawn-position-spread tied to substrate?** Yes, modestly: fire/lightning regions spawn slightly tighter (S≈60-70px; reward burst); water/holy regions spawn slightly looser (S≈80-100px; reward big-zone); wind regions spawn linear (favor cone/line); shadow regions spawn dispersed-clustered (S=70 with 2 sub-clusters; reward persistent-zone tagging).

This is a **post-D10 polish concern**, not a blocking concern. Default S≈70px for all regions works for the perception-test; substrate-coupling of spacing is forward work for B13-proper or Playtest Cycle 1.

### § 4.5 — When the geometry escapes the math: chain and vortex

Two substrate-coherent geometries explicitly escape the (R/S)² model:

- **Chain (lightning, secondarily shadow):** chain is *not* radius-based; it's hop-based. Lightning chain at 4-6 hops, each hop R≈100px, reliably hits 4-6 mobs in a *spread* pack — chain prefers wider spacing, not tighter. This is why lightning regions can run looser-than-canon spacing (S≈80-100px) without penalty.
- **Vortex_pull (wind):** vortex *moves the monsters into the AOE before the AOE resolves.* The R/S math reverses — vortex collapses spread packs into tight clusters, then the wind AOE (cone or burst) hits the now-clustered mobs. This is the substrate's iconic *kinetic_rearrangement* identity made geometrically functional.

These two exceptions are exactly where substrate identity becomes mechanically substrate-coherent in play. They are the **best perception-test signal opportunities** — a player who feels lightning chain bouncing across spread mobs vs vortex sucking spread mobs into a kill-zone is perceiving the substrate at the right level.

---

## § 5 — Surface 4: Telegraphed-AOE cognition budget

### § 5.1 — The cognitive-load math

A telegraphed enemy AOE asks the player to do four things simultaneously in the windup window:

1. **Notice the indicator** (visual parse, ~100ms)
2. **Identify substrate** (color/shape parse, ~150ms)
3. **Predict the AOE area** (geometry parse, ~150ms)
4. **Choose and execute escape** (decision + input, ~200ms)

Total: ~600ms of cognitive load per telegraphed AOE. **Player-cognition budget in active combat is ~1.5-2.0 seconds of parallel work** (per perception-test research consensus; D4-nightmare-dungeon postmortems confirm this empirically). At ~600ms per telegraph, **the budget supports 2-3 simultaneous telegraphs at most.**

### § 5.2 — Genre canon for simultaneous-telegraph budget

- **D3:** caps at 2-3 simultaneous large telegraphs in standard play; D3 Rift-Guardians often violate this and are widely criticized for "screen-explosion-soup."
- **D4:** explicit cap at 2 simultaneous boss-telegraph indicators; nightmare dungeons at T50+ break this and are *the* community criticism of D4 (the "screen vomit" complaint).
- **PoE:** no explicit cap; community converges on "if you can see 3+ ground-effects at once you're going to die." High-tier PoE play is partly *about* navigating this — and partly *about* building immune-to-ground-effects (the canonical PoE answer).
- **Last Epoch:** caps at 2-3 simultaneous indicators in standard play; explicit dev-talk acknowledgment that 4+ breaks player perception.
- **Lost Ark:** caps at 2-3 in dungeons; guardian raids run higher (4-6) but only because guardians have predictable mechanic-cycles the player memorizes.

**Canon-consensus: max 2-3 simultaneous enemy AOE telegraphs visible at any given moment.** Above 3 = screen-spam failure. Below 2 = under-stimulated; player ignores the read-the-battlefield game.

### § 5.3 — Phase-1 P1 application: 2-telegraph budget

**Recommendation: max 2 simultaneous enemy AOE telegraphs at any time in the perception-test build.**

**How this is enforced by encounter design:**

1. **Telegraphed AOEs are elite-and-above only** (per prior briefing § 3.1; trash mobs commit-and-die without telegraphs).
2. **Elite cap per encounter: 1** (per § 3.1 above — pack composition: 1 elite + 2-6 trash adds).
3. **Therefore: max 1 telegraph from the elite + 0 from trash = 1 simultaneous telegraph in standard encounter.**
4. **Mini-boss encounters (gauntlet rooms with named opponents): 1 mini-boss + 0-3 elite adds = max 2 simultaneous telegraphs.** Within budget.
5. **Boss encounters (act-end): 1 boss + 0-3 elite adds; boss telegraphs may cycle every 3-5 sec; max 2 simultaneous indicators visible at the peak.** Within budget.

**The cognition budget is naturally respected by the elite-tier-only telegraph rule + 1-elite-per-encounter pack-composition rule.** No special enforcement needed; the design constraint composes correctly.

### § 5.4 — Substrate-mixing implication for telegraph cognition

Per § 3.3 above, 30% of packs are 2-substrate heterogeneous. For elite-tier telegraphs:

- **Elite stays substrate-homogeneous** (the elite carries the cosmological signal of the pack). The elite's substrate may differ from the trash adds' substrate in heterogeneous packs — that is, the elite reads one substrate while the trash reads another, but each individual elite's telegraph is single-substrate.
- **No mixed-substrate elite** (e.g. a "fire-and-water" elite with valenced telegraph) in the perception-test build. The valenced-telegraph is forbidden by § 0 pairing summary (`forbidden_hybrid_with: water` for fire).
- **Holy/shadow elite-in-shadow-pack with shadow trash:** valid; substrates are amplification-pair, not erasure-pair. The elite's telegraph reads holy (white/gold radiant indicator) while the trash reads shadow (purple/dark visual). Cosmologically interesting; mechanically two distinct VFX languages on screen. **Cognitively manageable because trash do not telegraph.**

### § 5.5 — Windup-time variance across mixed packs

Per prior briefing § 3.2 the windup-time variance ranges from 0.2s (shadow) to 2.0s (holy). In a mixed-substrate elite encounter, the player would need to switch reading-cadence (shadow demands fast commit; holy permits slow read) across encounters.

**Recommendation: do not mix substrates with windup-time variance >1.0s in a single encounter.** Concretely:

- **Forbidden mixed elite pairings (within the heterogeneous-pack 30%):** shadow elite + holy elite in same encounter (0.2-0.5s shadow + 1.5-2.0s holy = perceptually disorienting cadence-switch).
- **Allowed mixed elite pairings:** fire + lightning (similar 0.8-1.2s + 0.4-0.6s windup); earth + shadow (0.4-0.7s + 0.3-0.5s); water + holy (1.0-1.5s + 1.5-2.0s — both slow); etc.
- **Practical implementation:** mixed-elite encounters are rare in Phase-1 P1 (one elite per encounter cap); the rule applies primarily to mini-boss encounters with elite adds, and to forward-work boss encounters with elite retinue. Surface as forward-work design rule rather than blocking constraint.

### § 5.6 — Player-AOE telegraph cognition

Per prior briefing § 3.1: player AOEs do NOT telegraph (single-player ARPG convention). This holds without modification. The cognition budget is reserved entirely for *enemy* AOE telegraphs.

The post-cast player-AOE indicator (per prior briefing § 3.3: 0.3s post-cast feedback at 0.92× hitbox) is **not a telegraph** in the cognitive sense — it's feedback, not a read-the-battlefield demand. It does not count against the 2-simultaneous budget.

---

## § 6 — Cross-impact map

### § 6.1 — D10 substrate-coherent generation rules

**Impact: LARGE.** D10 generates archetypes by composing substrate × role. This briefing's § 2.2 + § 2.3 + § 4.3 are the AOE-character-mix prescriptions D10 must consume. **D10 must respect:**

- AOE-share target per substrate × role (§ 2.2 + role modulation)
- AOE-character mix per substrate (§ 2.3)
- Substrate-coherent AOE radii per skill geometry (§ 4.3)

**Gamora's D10 implementation should consume the § 7 parameter table as a config.** If post-D10 regen finds the parameters are too prescriptive, surface to gandalf via HANDOFF; the briefing amends.

### § 6.2 — Post-D10 regen (the regen that consumes this briefing)

**Impact: LARGE.** The post-D10 regen is the lock-point for these parameters. Gamora applies the § 7 table values to:

- Monster spawn density per encounter (§ 7 row 1)
- Pack composition (§ 7 row 2)
- Pack spacing (§ 7 row 3)
- AOE radii per substrate (§ 7 row 4)
- Region-density modifier per substrate (§ 7 row 5)

**Acceptance criterion for the regen:** TMPM in the demo at perception-test difficulty falls in 30-50 range, measured across 5-10 sampled encounters. If significantly outside this band, re-tune.

### § 6.3 — D14 mirror-match diversity gate

**Impact: TELEMETRY-CHANNEL.** D14's perceptual metric (whether or not it becomes play-trace based) benefits from this briefing's AOE-share telemetry (§ 2.4). Kits with substrate-coherent AOE-share are more likely to push apart on the play-trace metric; kits with substrate-incoherent AOE-share collapse together. **D14 picks up an additional signal channel** without scope change.

### § 6.4 — D27 perception test

**Impact: SIGNAL-QUALITY-INFORMING.** D27's H1 (mechanically-distinct archetypes feel distinct) sharpens with this briefing's parameters in place. Without them, the test risks the same false-negative-from-loop-collapse failure mode the prior briefing diagnosed (engagement-loop-cannot-express-substrate). With them, two substrate-coherent archetypes produce visibly-different pack-clear patterns (fire burst-clusters vs wind cone-lines vs lightning chain-jumps), which the player can perceive in 60-90 sec.

**No D27 scope change.** Just better signal.

### § 6.5 — Narrow-slice work (already in flight per prior briefing § 5.1)

**Impact: COMPLEMENTARY.** Narrow-slice telegraphed-combat substrate (universal dodge + enemy-AOE indicators + elite reactive escape AI) and this briefing's density-and-radius parameters fit together. **Both ship in the regen window post-D10.** Narrow-slice provides the *expression substrate;* this briefing provides the *content tuning.*

### § 6.6 — D8/D9 canonical-four trait pools

**Impact: MINIMAL.** Existing D8 traits don't assume specific AOE-share or density; they assume *the substrate's identity is in play.* This briefing tunes density-and-radius to make substrate identity legible, which is what D8 traits depend on. **No D8 amendment needed.** D8 trait *additions* that interact with density (e.g. fire trait "burn-on-elite-only" or wind trait "vortex-radius-scaling") become design surface for forward work, not Phase-1 P1.

### § 6.7 — Drax AOE-indicator visual character

**Impact: VFX-DESIGN-COUPLING.** Drax's narrow-slice indicator render work (per prior briefing § 3.3 + rocket schema fields) consumes the per-substrate windup values + colors. This briefing's § 5.5 mixed-windup-cadence rules surface as design notes drax may want to respect in indicator clarity (e.g., shadow's late-commit indicator may need stronger pre-warning glow when adjacent to a holy elite to prevent missed reads).

**Surface as soft note to drax; not blocking.** Drax can ship indicators per existing dispatch; this briefing's mixed-windup-cadence concerns become forward-iteration polish.

### § 6.8 — Roadmap impact (`canonical/16-project-roadmap.md`)

**Impact: NEW SUBSECTION CANDIDATE.** Currently the roadmap has no explicit B-series item for monster-density / AOE-balance tuning. This briefing fills that gap *for Phase-1 P1 only;* a full B-series item ("BXX: density-and-radius balance audit") may be appropriate for Stage A2 closeout or Playtest Cycle 1. **Surface as OBSERVATION for knight-rider** — does this briefing's locks merit a B-series entry, or are they consumed entirely by the post-D10 regen?

---

## § 7 — Implementation parameters for gamora

**Direct-implementable numerical envelope. Each row maps to a regen-side config or generator parameter.**

### § 7.1 — Master parameter table

| # | Parameter | Value | Source § | Apply at |
|---|---|---|---|---|
| 1 | **TMPM target** | **30-50 monsters per minute** (perception-test difficulty) | § 3.2 | Demo spawn-rate config per region |
| 2 | **Trash pack size** | **3-7 mobs per encounter** (median 5) | § 3.1 | Wave-generation per encounter |
| 3 | **Elite per encounter** | **0-1 elite** (50% of encounters have 1 elite; 50% are trash-only) | § 3.1 | Wave-generation roll |
| 4 | **Elite+trash composition** | **1 elite + 2-4 trash adds** when elite present | § 3.1 | Wave-generation |
| 5 | **Mini-boss pack** | **1 mini-boss + 0-3 elite adds** | § 3.1 | Gauntlet room-end encounter |
| 6 | **Pack spawn-spread** | **inter-mob S = 70-90px** (current `packSpawnPositions` is genre-canon — preserve) | § 4.4 | `enemySpawnPositions()` |
| 7 | **Pack cluster diameter** | **D = 150-220px** for 5-7 mob packs | § 4.4 | Pack-spawn geometry |
| 8 | **Pack composition: homogeneous %** | **70% same-substrate** packs | § 3.3 | Per-encounter substrate-roll |
| 9 | **Pack composition: heterogeneous %** | **30% mixed (2-substrate, 60/40 split)** | § 3.3 | Per-encounter substrate-roll |
| 10 | **Heterogeneous mixing rule** | Honor `forbidden_hybrid_with` from substrate declarations; no fire+water, no earth+wind mixed packs | § 3.3 | Substrate-mix validator |
| 11 | **Kit AOE-share — fire** | 55-65% AOE-coded skills | § 2.2 | D10 generator |
| 12 | **Kit AOE-share — water** | 65-75% | § 2.2 | D10 generator |
| 13 | **Kit AOE-share — earth** | 35-50% | § 2.2 | D10 generator |
| 14 | **Kit AOE-share — wind** | 50-60% | § 2.2 | D10 generator |
| 15 | **Kit AOE-share — lightning** | 60-70% | § 2.2 | D10 generator |
| 16 | **Kit AOE-share — holy** | 40-55% | § 2.2 | D10 generator |
| 17 | **Kit AOE-share — shadow** | 45-60% | § 2.2 | D10 generator |
| 18 | **Role modulation** | support −10%; control +5%; damage/hybrid baseline | § 2.2 | D10 generator overlay |
| 19 | **AOE-character mix per substrate** | Per § 2.3 table (substrate-specific) | § 2.3 | D10 generator |
| 20 | **AOE radii per substrate** | Per § 4.3 table; aim for primary-AOE-character hits 4-6 mobs at S=70px pack-spacing | § 4.3 | D10 generator + skill schema |
| 21 | **Region-density modifier per substrate** | Shadow 0.6-0.7×; Water 0.8-0.9×; Holy ~0.9-1.0×; Fire/Earth/Wind/Lightning 1.0×; Wind-edge 1.0-1.1× | § 3.2 | Region density config |
| 22 | **Simultaneous telegraph cap** | Max 2 visible enemy AOE telegraphs at any time | § 5.3 | Naturally enforced by elite-1-per-encounter + trash-no-telegraph rules |
| 23 | **Telegraphs are elite-tier-and-above** | Trash mobs commit-and-die without telegraph (per prior briefing § 3.1) | § 5.3 | Skill schema flag |
| 24 | **Mixed-elite windup-cadence rule** | Avoid mixing elites with >1.0s windup-time delta (e.g. no shadow+holy elite co-presence) | § 5.5 | Mini-boss/boss retinue composer |

### § 7.2 — Acceptance criteria for post-D10 regen

Gamora's post-D10 regen passes if:

1. **TMPM measurement** at perception-test difficulty falls in **30-50 range** across 5-10 sampled encounters.
2. **AOE-share per substrate** falls within ±10% of § 7.1 row 11-17 targets (substrate × role).
3. **Pack composition** follows § 7.1 row 8-9 ratios (telemetry samples 70/30 within ±5%).
4. **Average AOE-hits-per-cast** for medium-AOE skills falls in **3-5 range** when measured against standard-density packs.
5. **Substrate distributions across regions** are not bottlenecked at one substrate (no region >60% single-substrate at the wave-substrate level beyond what § 3.2 region-density modifier prescribes).

**If acceptance criteria fail by >10%, regen returns to gamora for retune with this briefing as reference.** Iteration cost: ~0.5-1 day per retune cycle.

### § 7.3 — Smoke-test guidance

Per discipline #9 (smoke-test before full regen): gamora runs a 2-class smoke test (one substrate-AOE-heavy class — water_controller — and one substrate-AOE-light class — earth_damage) through the spawn engine and measures:

- Mobs killed in 60 sec across 5 sample encounters
- AOE-hits-per-cast for the primary AOE skill
- Visible telegraph count at peak engagement

If the smoke-test values are within ±20% of § 7.1 row 1 + 20 + 22, the full regen proceeds. If not, retune before regen.

---

## § 8 — Open questions for Matt

Non-blocking; § 7 is implementable without these. But Matt's preference shapes the final feel:

1. **TMPM target band (§ 3.2)** — 30-50 TMPM is *D4-nightmare-dungeon density*. Is that the right reference? Or do you want the perception-test build to feel closer to **D3-rift density (TMPM 80-150)** for "more screen action"? My recommendation is 30-50; the higher band starts to erode substrate-distinguishability per § 1.1 mode 4. Confirm or counter.

2. **Pack-composition mix (§ 3.3)** — 70/30 homogeneous/heterogeneous OK? Or do you want a higher mix-rate (e.g. 50/50) for visual variety, accepting the cognitive-load increase?

3. **Region-density-modifier per substrate (§ 3.2 / § 7.1 row 21)** — shadow regions at 0.6-0.7× baseline TMPM is substrate-coherent but means players spending time in shadow regions see notably less throughput. Do you want this substrate-coupling, or prefer uniform density across all regions?

4. **AOE-share substrate bands (§ 2.2 / § 7.1 rows 11-17)** — the ranges are based on genre canon + substrate identity declarations. Water at 65-75% is the highest; earth at 35-50% is the lowest. Comfortable with this asymmetry, or want narrower bands (e.g. all substrates 45-65%)?

5. **Mixed-elite windup-cadence rule (§ 5.5)** — forbid shadow+holy co-elite encounters? Or allow as design challenge (player learns to switch reading-cadence)? Phase-1 P1 has few mixed-elite encounters; the rule applies to forward work primarily.

6. **AOE-radius prescriptions per substrate (§ 4.3 / § 7.1 row 20)** — substrate-prescriptive AOE-radii constrain D10 generation. Comfortable with prescription at this level, or prefer D10 to generate freely and let post-regen telemetry tune-after-the-fact?

7. **B-series entry?** (§ 6.8) — should this briefing's locks become a formal B-series roadmap entry (e.g. **BXX: density-and-radius balance audit** at Stage A2 closeout) for forward maintenance, or is consumption-by-post-D10-regen sufficient and the topic closes?

---

## § 9 — Open questions surfaced from prior briefing (parked; not addressed here per dispatch out-of-scope)

The 7 open questions from `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 9 remain parked for Matt. Gandalf stays LIVE for follow-up Q&A on both briefings per continuous-availability ramp.

---

## § 10 — Cross-references

- `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` — prior L3 briefing; § 3 windup ranges and § 4 escape-AI tiers compose with this briefing's parameters
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate `geometry_affinities`, `combat_pillar`, `forbidden_hybrid_with`, `role_affinities` per substrate
- `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` — canonical-four trait pools; AOE-radius-bonus and area-persist-duration-bonus modifier keys
- `canonical/story/d8-trait-floor-design-phase-1-p1.md` — D8 trait floor design; substrate identity → trait pool mapping
- `canonical/story/perception-test-experiment-scoping-2026-05-17.md` — D27 perception test; signal-quality dependency on this briefing's parameters
- `canonical/34-monster-design-phase0-vs-production.md` — monster tier hierarchy informing § 3.1 pack composition
- `canonical/32-progression-design.md` § 12.5 (post-2026-05-17 amendment) — telegraphed-combat narrow-slice locks
- `canonical/16-project-roadmap.md` — B13 scope-reduction note; potential BXX entry per § 6.8
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py:34` — `PACK_PROXY_SIZE = 8` (simulation-side abstraction; demo-side spawn-density is the consumer of this briefing's parameters)
- `reincarnated-demo/src/main.ts:800-816` — `packSpawnPositions()` current implementation; current inter-mob spacing is genre-canon (preserve)
- `agentic_orchestration/dispatches/2026-05-17-gandalf-aoe-tuning-genre-canon-validation.md` — dispatch this briefing answers
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — focused-playtest test 6 son feedback context; drax v0.25-v0.33 ship trajectory
- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` — Legolas Mode A findings; substrate identity references

---

*Authored 2026-05-17 by gandalf. Genre-canon validation briefing for AOE-tuning + monster-density parameters. Pattern B; ~1 day. Tag intent: `gandalf/v1.4-aoe-tuning-and-monster-density-canon-1`. § 7 contains the direct-implementable numerical envelope gamora consumes in the post-D10 regen.*
