# QD-Engine BC Axes — Locked Operational Specification

**Status:** CANONICAL — locked through theory-craft session with Matt 2026-05-19/20
**Author:** gandalf (story-and-design steward)
**Companion to:** `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md`
**Last revised:** 2026-05-20

---

## 0. TL;DR

The QD-engine MAP-Elites archive operates over **8 Behavior Characteristic (BC) axes**, totaling **68,040 cells** at full discretization. Each axis is locked with: bin count, bin labels, operational definitions, primary + secondary measurements, bin-assignment priority, substrate dependencies, and sim deferral risk.

The architecture supports 4 hybrid archetypes (absorber, regenerator, thorns/reflection, self-harmer) plus 5 specialized mechanics (mind-control, damage-taken-converts, charge-stack, charge-up-skill, multi-resource kits) via cross-axis cell-address capture rather than dedicated bins where possible. Where a mechanic is structurally distinct enough to warrant a bin, it gets one (HP-economy, charge-stack, damage-taken-converts).

**Gate-to-rebuild dependencies:** (a) recompose-validation hive ships (in flight 2026-05-19/20); (b) Legolas substrate-sufficiency audit confirms each axis × bin has ≥5× substrate variability OR a costed enrichment path; (c) Discipline #17 empirical calibration of all thresholds on first-deployment telemetry.

---

## 1. Provenance and scope

### 1.1 How this doc came to be

This document captures the operational specification that emerged from a sustained Pattern-B theory-craft session between Matt and gandalf on 2026-05-19 (extending into 2026-05-20). The QD-engine architectural vision doc (`engine-architecture-vision-qd-profile-2026-05-19.md`) committed to **5 BC axes** as a sketch. The theory-craft session stress-tested that sketch and found it insufficient — the 5-axis count failed to discriminate multiple recognizable ARPG archetypes.

The lock work proceeded axis-by-axis. Each axis was:
1. Proposed with provisional bins from the vision doc or fresh
2. Stress-tested against ARPG canon (Diablo 1-4 + PoE + Last Epoch + Grim Dawn + Diablo Immortal)
3. Refined with operational definitions tied to simulator-measurable quantities
4. Tested against hybrid archetypes Matt surfaced (absorber, regenerator, thorns, reflection, self-harmer, mind-control, damage-taken-converts, charge mechanics)
5. Locked with substrate flags identifying generation-system and sim-extension dependencies
6. Confirmed by Matt before moving to the next axis

The session expanded the axis count from 5 → 8 and the bin counts within axes (notably Axis 5 from 4 → 7). Each expansion was individually justified; the cumulative effect was tracked.

### 1.2 What this doc claims and what it doesn't

**Claims:**
- These 8 axes capture the major mechanical-discrimination dimensions for ARPG class identity, validated against the cross-shipped-game canon
- The operational definitions are simulator-implementable given current engine state plus identified extensions
- The threshold values are ARPG-canonical priors suitable for Discipline #17 empirical-calibration refinement
- The cross-axis cell-address mechanism captures hybrid archetypes without bin explosion

**Does not claim:**
- That every shipped ARPG build maps cleanly to exactly one cell (some cluster around boundaries; that's design intent)
- That the substrate currently has ≥5× variability per axis (Legolas audit pending; ship gate)
- That the simulator supports every measurement today (deferral matrix in § 5)
- That these are the *only* axes worth measuring (visual + cohesion BC live in separate archives owned by galadriel and gandalf respectively)

### 1.3 Scope: mechanical BC only

This document specifies the **mechanical BC archive**. Two adjacent archive systems exist:

| Archive | Owner | What lives there |
|---|---|---|
| **Mechanical BC** (this doc) | gandalf | Simulator-measurable kit identity dimensions |
| **Cohesion BC** | gandalf | LLM-judge-measured thematic coherence (LUCB1 / information bottleneck) |
| **Visual BC** | galadriel | CV-pipeline-measured visual similarity (separate gate) |

The three archives use the same MAP-Elites machinery but different judges. They feed independently into profile-specific assembly (§ 10 of vision doc).

---

## 2. The 8 locked axes — overview

| # | Axis | Bins | Bin labels |
|---|---|---|---|
| 1 | Engagement profile | 6 | close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow |
| 2 | Damage geometry | 5 | single-target / small-AOE / large-AOE / chain / multi-spawn |
| 2A | Proxy density | 3 | solo / proxy-light / proxy-heavy |
| 2B | Control density | 3 | damage-pure / mixed / control-pure |
| 3A | Damage tempo | 3 | low / medium / high |
| 3B | Damage amplitude variance | 3 | flat / variable / spiky |
| 4 | Defensive profile | 4 | tank / mitigator / dodger / glass |
| 5 | Resource economy | 7 | HP-economy / charge-stack / damage-taken-converts / starved / overflow / generator-spender / steady |

**Total cells:** 6 × 5 × 3 × 3 × 3 × 3 × 4 × 7 = **68,040**

**Coverage analysis:** at 1,000 expected seasons in archive over the engine's productive lifetime, occupancy is ~1.5%. This is sparse — characteristic of MAP-Elites at higher dimensionality — but functional. Published QD research at 8-10 axes with similar sparsity ratios produces successful archives. Mahalanobis covariance estimation at 8D needs 44 samples for stability; will have orders of magnitude more. Crowding-distance signal becomes noisier in sparse archives but remains usable for diversity-preservation. § 7 discusses in detail.

---

## 3. Per-axis specifications

### 3.1 Axis 1 — Engagement Profile (6 bins)

**Composite axis:** range × mobility. Captures *where* the class fights from and *how mobile* it is during fights.

#### Bins

| Bin | Range component | Mobility component | Canonical exemplars |
|---|---|---|---|
| close-fast | melee (effective range ≤ 3 tiles) | high (≥ 30 tiles displacement / min from movement skills) | D3 Monk; PoE Cyclone-flicker |
| close-slow | melee | low (< 30 tiles / min) | D2 Barbarian Whirlwind-stationary; PoE Slayer-static |
| mid-fast | mid (effective range 3-8 tiles) | high | D3 Demon Hunter (vault-spam); D4 Rogue dash builds |
| mid-slow | mid | low | D3 Crusader Phalanx; D2 Paladin Hammerdin |
| ranged-fast | ranged (effective range ≥ 8 tiles) | high | D3 Wizard teleport-spam; PoE Trickster mobility-caster |
| ranged-slow | ranged | low | D2 Sorceress (Frozen Orb stand); PoE totem-stationary; D3 Archon-stand |

#### Measurement

**Range component:** mean weighted skill range, weighted by skill damage contribution. Thresholds: melee ≤ 3.0 tiles; mid 3.0–8.0; ranged > 8.0.

**Mobility component:** total movement-skill-attributable displacement per minute of fight time. Skills contribute their per-cast Euclidean displacement (origin → destination for teleport/blink; path length for dash/charge; mean-speed × duration for cyclone-style channel-move). Walking and reactive repositioning excluded.

#### Substrate flags

- `movement_displacement_per_cast` attribute on skills — needs adding to generation metadata
- Sim-policy positional intelligence affects measurement validity (a naive sim that never chooses to teleport when teleport is in the kit will register that kit as low-mobility — correct measurement, but means sim policy quality matters)

#### Sim deferral risk: LOW

Range is well-tagged today; mobility measurement requires skill-metadata extension but no architectural sim change.

---

### 3.2 Axis 2 — Damage Geometry (5 bins)

#### Bins

| Bin | Operational definition | Canonical exemplars |
|---|---|---|
| single-target | One entity hit per damage event; `aoe_radius ≤ 0.5` tiles | D2 Bone Spirit; D3 Magic Missile basic; single-target boss rotations |
| small-AOE | Area damage `0.5 < aoe_radius ≤ 3.0` tiles | D3 Monk Sweeping Wind; D2 Frost Nova; D4 small-radius spells |
| large-AOE | Area damage `aoe_radius > 3.0` tiles | D3 Black Hole; D2 Druid Tornado-large; PoE explosive-trap-radius |
| chain | Damage hops between targets via jump-targeting logic | D2 Chain Lightning; D3 Arcane Torrent chain; PoE chain spells |
| multi-spawn | Multiple independent damage entities/projectiles per cast | D3 Meteor shower; D2 Corpse Explosion cascade; D4 Hydra multi-head; PoE Vaal-skill spawns |

#### Measurement

Per-skill geometry detection via skill metadata (priority): chain-tag → multi-spawn-tag → `aoe_radius` thresholds → single-target default. Then damage-weighted argmax across the kit's actual rotation:

```
geometry_weight = {bin: 0 for bin in geometries}
for each damage_event in fight_telemetry:
    attribute event to its skill_geometry (including reactive-source events)
    geometry_weight[skill_geometry] += event.damage_dealt
kit_primary_geometry = argmax(geometry_weight)
```

#### Tie-break

When geometries tie within ε of damage contribution: (a) higher target-count geometry wins (chain > single-target; multi-spawn > AOE); (b) larger area geometry wins (large-AOE > small-AOE).

#### Folded mechanisms (not their own bins)

| Mechanism | Bin classification |
|---|---|
| Line / pierce | small-AOE or large-AOE (elongated AOE) |
| Cone / fan | small-AOE or large-AOE by radius |
| Persistent ground | small/large-AOE; persistence is time-dimension, captured in rhythm axis |
| DOT | Whatever application geometry; sustain captured in tempo axis |
| Reactive-damage (thorns/reflection trigger) | Whatever geometry the trigger produces (source-tag attribution) |
| Homing / bouncing projectile | single-target or chain by where damage lands |
| Aura constant-damage | small/large-AOE by aura radius |

#### Substrate flags

- Skill geometry tagging: `aoe_radius`, `is_chain`, `is_multi_spawn` attributes on skills
- Per-event source-tagged damage attribution in sim telemetry (source = `cast` / `reactive` / `proxy` / `environmental`)
- Per-bin substrate variety (5× rule = ~25 templates per bin)

#### Sim deferral risk: LOW

Most geometries supported today via the 16-type canonical palette (doc 09). Chain and multi-spawn distinction requires metadata confirmation.

---

### 3.3 Axis 2A — Proxy Density (3 bins)

#### Bins

| Bin | Operational definition | Canonical exemplars |
|---|---|---|
| solo | 0 player-allied proxy entities active during fights | D3 Barbarian; D2 Sorceress without familiar; PoE Cyclone-Slayer |
| proxy-light | 1–3 active proxies; player is primary action source | D3 Witch Doctor (fetish + dogs); D4 Sorcerer (hydra); PoE totem-secondary |
| proxy-heavy | 4+ active proxies; player is commander | D2 Necromancer skellie army; PoE summoner-pure; D4 minion necro |

#### Measurement

`mean count of active player-allied proxy entities over fight duration`. Thresholds: <1.0 / 1.0-3.0 / ≥3.0.

#### Proxy entity definition (revised after mind-control hybrid surface)

A **proxy entity** = any entity that:
1. Targets player-hostile entities under non-player-direct-control logic, AND
2. Persists in that state for ≥3 seconds OR has independent HP under player-alignment.

**Origin-agnostic.** Created (summoned, raised-from-corpse), converted (mind-controlled, charmed, dominated), or hijacked — all count.

**Includes:** summons, raised-from-corpse, mind-controlled, charmed, dominated, converted, totems, hydras, mines, traps, sentinels.

**Excludes:** berserked enemies (no preferential player-alignment), feared/panicked enemies, transient projectiles, brief-charm <3s, ground effects without independent action.

#### Substrate flags

- **Player-side proxy generation absent today** — major substrate gap. Legolas audit priority.
- Two distinct substrate types: player-side-creation (summons/totems) vs player-side-conversion-effect (charm/dominate). Audit each separately.

#### Sim deferral risk: HIGH for proxy-light + proxy-heavy

Current sim supports solo only. Proxy-light and proxy-heavy bins route to **deferred-evaluation pool** until sim extension lands. Required sim extensions:
- Player-side entity spawning
- Ally entity AI
- Monster-target-selection (player vs ally)
- Ally HP tracking + death handling
- Spawn limits / replenishment timers

**Profile filter:** Profile A (Reincarnated Phase 0 shipping) excludes proxy-light + proxy-heavy from shippable seasons until sim catches up.

---

### 3.4 Axis 2B — Control Density (3 bins)

#### Bins

| Bin | Operational definition | Canonical exemplars |
|---|---|---|
| damage-pure | < 20% of skill effect budget is control | D3 Barbarian Whirlwind-only; D4 Sorc fire builds |
| mixed | 20-60% control mixed with damage | D2 Paladin Hammerdin (with stun); D3 Wizard with frost passive |
| control-pure | ≥ 60% control; damage is secondary | D3 Wizard freeze-orb stand; PoE curser; support archetypes |

#### Measurement

`(sum of CC-tagged skill weights) / (total skill weight)`, where weight = damage potential + control-effect potential normalized to common units.

#### Control-effect inclusion list

**Counted:** stun, freeze, chill (with ≥30% slow component), root, fear, blind, knockback-with-knockdown, silence, slow ≥30%, taunt, mind-control / charm (also counts on Axis 2A under proxy definition).

**Excluded:** minor slows <30%, hit-feedback knockback, brief stagger on impact.

#### Substrate flags

- CC variety in generation — confirm sufficient distinct control-effect templates exist (Legolas audit)

#### Sim deferral risk: LOW

Most CC effects supported today. Confirm mind-control / charm attribution path in audit (it crosses 2A and 2B).

---

### 3.5 Axis 3A — Damage Tempo (3 bins)

#### Bins

| Bin | Operational definition | Canonical exemplars |
|---|---|---|
| low | Few damage events per second; < 2 events/s | D3 Crusader Phalanx; D3 Wizard Archon-cycle; big-CD nukes |
| medium | Moderate damage event rate; 2–6 events/s | D2 Paladin Hammerdin; D3 monk Sunwuko cycle; rotation builds |
| high | Many damage events per second; ≥ 6 events/s | D2 Bowazon Strafe; PoE Cyclone-channel; D3 DH Multishot |

#### Measurement

Mean count of distinct damage-application events per second across fight duration. Multi-hit single skills (Multishot, chain bounces) count each hit as an event.

#### Substrate flags

- Per-event damage-application logging in sim telemetry (not just per-skill or per-fight totals)

#### Sim deferral risk: LOW

Standard sim telemetry; event-level logging likely supported.

---

### 3.6 Axis 3B — Damage Amplitude Variance (3 bins)

#### Bins

| Bin | Operational definition | Canonical exemplars |
|---|---|---|
| flat | All damage events similar magnitude; CV < 0.3 | D2 Frozen Orb; D2 Strafe; D3 Phalanx |
| variable | Predictable rotation peaks; CV 0.3–0.7 | D2 Hammerdin; rotation builds with CD spikes |
| spiky | Rare big hits dominate; CV ≥ 0.7 | D3 Earthquake-aftershock; D3 Archon-window; PoE Detonate Dead |

#### Measurement

`CV (stdev/mean) of per-damage-event magnitudes` across full fight. **Event-level variance, not windowed.**

#### Channeled handling

**Channeled is a structural tag, NOT a bin.** Channel-tagged kits cluster at [high-tempo, flat-variance] naturally — the BC measurement captures that. The "channeled" character is a categorical property used for substrate-filtering and theme-coalescence but not an archive-coordinate dimension.

#### Substrate flags

- Per-event magnitude logging (joint with Axis 3A)
- Channel-tagged skill mechanic in skill metadata

#### Sim deferral risk: PARTIAL for channeled tag

If sim doesn't cleanly handle channel-tagged skills (continuous damage application, channel interruption, channel-resource-drain), channel-tagged kits may need deferred-evaluation routing. Legolas audit.

---

### 3.7 Axis 4 — Defensive Profile (4 bins)

#### Bins

| Bin | Defensive strategy | Canonical exemplars |
|---|---|---|
| tank | Eat damage and stand; high eHP | D2 Barbarian (BO+Iron Skin); D4 Druid Werebear; PoE Juggernaut |
| mitigator | Active damage reduction (block, regen, lifesteal, defensive CDs, armor stacking) | D2 Paladin (block+Holy Shield); D3 Wizard Energy Shield; D4 Sorc Ice Armor |
| dodger | Avoid damage via positioning/evasion (dodge rolls, evasion-chance, stealth, iframes, reflection) | D3 Demon Hunter (Smoke Screen); D4 Rogue dodge-roll; PoE Trickster evade-stack; player-side reflect builds |
| glass | Low eHP, low avoidance; relies on burst-before-being-hit | D2 HC summoner glass-cannons; PoE pure-damage no-defense; D4 fire-Sorc no-layers |

#### Measurement

**Primary (eHP_effective_ratio):**

```
eHP_effective = (HP + shield_pool + regen_per_sec × encounter_duration_target) / (1 - mitigation_fraction)
eHP_effective_ratio = eHP_effective / mean_encounter_damage
```

Where `encounter_duration_target` = 30s (initial; Discipline #17 empirical calibration).

**Secondary (avoidance_rate):**

```
avoidance_rate = (evasion_misses + iframe_coverage + stealth_no_hit + reflection_redirected) / incoming_damage_attempted
```

#### Bin assignment

```
if avoidance_rate >= 0.40:
    bin = "dodger"
elif eHP_effective_ratio >= 5.0:
    bin = "tank"
elif eHP_effective_ratio < 2.0:
    bin = "glass"
else:
    bin = "mitigator"
```

#### Hybrid archetype capture (no new bins)

| Archetype | Bin | Mechanism |
|---|---|---|
| Absorber (Energy Shield) | tank or mitigator | shield_pool boosts eHP_effective |
| Regenerator (Werebear) | tank or mitigator | regen×duration boosts eHP_effective |
| Thorns (Crusader thorns) | whatever base profile is | Reactive counter-damage on Axis 2 & 3; defender still takes hit |
| Reflection (player-side reflect) | dodger (avoidance ≥0.40) | Redirected damage counts on avoidance_rate |
| Self-harmer (Blood Magic) | glass typically | Captured by Axis 5 HP-economy primarily |

#### Substrate flags

- **Reflection damage attribution** — sim must distinguish reflection (redirected, defender takes zero) from thorns (counter-damage, defender takes hit) from other reactive mechanisms
- **Regen-per-second telemetry** — sim must log HoT recovery distinct from mitigation
- **Shield-pool tracking** — sim must track refillable buffers distinct from HP
- **Per-hit damage application logs** (joint with avoidance_rate measurement)

#### Sim deferral risk: PARTIAL for dodger bin

| Mechanism | Sim likely supports? |
|---|---|
| Probabilistic evasion (hit-chance roll = 0 damage) | YES — trivial extension |
| Stealth (untargetable for duration) | NO — needs AI target-selection-skip support |
| Iframe coverage during skill cast | NO — needs skill-cast-state tracking |
| Reflection (per-hit redirection) | NO — needs damage-resolution extension |

Sub-case partial defer: evasion-stack builds populate dodger bin today; stealth + iframe + reflection builds route to deferred-evaluation pool until sim extends.

---

### 3.8 Axis 5 — Resource Economy (7 bins)

#### Bins (with structural-vs-statistical detection method)

| Bin | Definition | Detection | Canonical exemplars |
|---|---|---|---|
| **HP-economy** | >50% of skill costs paid in HP | structural — skill cost type | PoE Blood Magic; D2 Bone Spirit; D4 Necro Sever |
| **damage-taken-converts** | Resource gained from incoming damage | structural — conversion mechanic | PoE CWDT; "% damage taken as mana"; D4 Barb fury-on-damage; berserker rage-on-hit |
| **charge-stack** | Stack-cap mechanic with build-then-hold pattern | structural — charge mechanic + statistical (mean ≥0.75, var <0.20) | PoE Frenzy/Power charges; D3 Wizard arcane orbs; charge-cap builds |
| **starved** | Resource frequently depleted | statistical — mean ≤0.30 | D2 Frozen Orb sorc; early-game mana-heavy |
| **overflow** | Surplus exists / no cost gates | statistical — mean ≥0.85 OR no-cost | D3 Wizard Archon; D2 Paladin auras |
| **generator-spender** | Explicit oscillating cycle | statistical — variance ≥0.20 | D3 Barb Fury; D3 Crusader Wrath; D4 Rogue combo points |
| **steady** | Resource maintains; reliable cadence | statistical — mid mean, low variance | D2 Hammerdin with pots; tuned-arcane wizard |

#### Bin assignment (structural priority order)

```python
# Structural checks first:
if hp_cost_fraction >= 0.50:
    bin = "HP-economy"
elif has_damage_to_resource_conversion_mechanic:
    bin = "damage-taken-converts"
elif has_charge_stack_mechanic AND mean_charge_fraction >= 0.75 AND variance < 0.20:
    bin = "charge-stack"

# Statistical checks for remaining kits:
elif mean_resource_fraction <= 0.30:
    bin = "starved"
elif mean_resource_fraction >= 0.85:
    bin = "overflow"
elif resource_fraction_variance >= 0.20:
    bin = "generator-spender"
else:
    bin = "steady"
```

#### Multi-resource handling

Some kits use multiple resources (D3 Crusader has Wrath + cooldowns; D3 DH has Hatred + Discipline). **Rule:** identify the primary bottlenecking resource — the one whose depletion most frequently blocks the kit's preferred rotation. Measure utilization on that resource.

This rule has known noise — primary may shift during a fight. Mitigation: measure on most-frequently-bottlenecking resource across multiple fights, not per-fight.

#### Folded mechanisms (not their own bins)

| Mechanism | Fold target |
|---|---|
| Damage-DEALT converts to resource | generator-spender (offensive-action source) |
| Kill-feed economy | generator-spender or steady |
| Sacrifice / pet-consumption | HP-economy or charge-stack by mechanic |
| Reservation economy | starved (reduced max → harder to maintain) |
| Cooldown-only | overflow (resource never gates) |
| Combo-point economy | generator-spender or charge-stack |
| Channel-resource-drain | steady or starved by drain rate |
| Buff-uptime economy | charge-stack (maintain at cap) |
| Absorber-buffer cycle | folds into 4 patterns by shield behavior |
| Charge-up-and-release skill | Axis 3A/3B (rhythm); not economy |

#### Substrate flags

1. Resource-per-tick telemetry
2. HP-cost as recognized skill cost type
3. Charge-pool mechanic with stack cap (sim must support: charge buildup triggers, cap behavior, decay timers, consumption skills)
4. Charge-up-and-release skill mechanic (variable cast-time + charge-state)
5. Damage-to-resource conversion mechanism (CWDT-style, damage-to-mana, hit-to-rage)
6. Multi-resource bottleneck identification logic
7. HP-cost skill variety (5× rule on 7-bin axis = ~35 distinguishable templates)
8. Charge-stack-mechanic substrate variety (similar substrate-volume requirement)

#### Sim deferral risk: MODERATE

- Resource tracking likely supported today
- HP-cost likely supported
- Charge-stack mechanic — may need sim extension
- Damage-to-resource conversion — may need sim extension
- Charge-up-and-release skill — may need variable-cast-time extension

---

## 4. Hybrid archetypes — cross-axis cell capture

The 8-axis architecture deliberately captures hybrid archetypes via *cross-axis cell address* rather than dedicated bins. This section documents how each surfaces.

### 4.1 Absorber (Energy Shield caster)

- Axis 4 (Defensive): tank (shield_pool boosts eHP_effective)
- Axis 5 (Economy): steady or generator-spender (shield refill cycle)
- **Cell:** [tank, steady/gen-spender]

### 4.2 Regenerator (Werebear, Jungle Fortitude)

- Axis 4: tank or mitigator (regen×duration boosts eHP_effective)
- Axis 5: steady (passive recovery)
- Axis 3A: often sustained engagement
- **Cell:** [tank, sustained-tempo, steady]

### 4.3 Thorns (D3 Crusader thorns)

- Axis 4: whatever base eHP profile is (typically tank)
- Axis 2: reactive counter-damage event geometry (often single-target back to attacker)
- Axis 3A/3B: damage events fire on incoming hits — affects tempo and variance signature
- **Cell:** [tank, single-target or small-AOE, reactive-tempo profile]

### 4.4 Reflection (player-side reflect)

- Axis 4: dodger (reflection on avoidance_rate ≥0.40)
- Axis 2: redirected damage attributed to player
- **Cell:** [dodger, geometry-of-redirected-damage]

### 4.5 Self-harmer (Blood Magic)

- Axis 5: HP-economy (load-bearing distinction)
- Axis 4: typically glass-defensive
- **Cell:** [glass, HP-economy]

### 4.6 Mind-control / charm

- Axis 2A: proxy entity (mind-controlled enemy under proxy definition)
- Axis 2B: control-pure if 60%+ control budget
- **Cell:** [proxy-light, control-pure] — distinct from solo control-pure (freeze sorc) and proxy-light damage (hydra wizard)

### 4.7 Damage-taken-converts (CWDT, berserker rage-on-hit)

- Axis 5: damage-taken-converts (structural bin)
- Axis 4: typically aggressive engagement (want to be hit)
- **Cell:** [defensive-profile, damage-taken-converts]

### 4.8 Charge-stack (PoE Frenzy stacker)

- Axis 5: charge-stack (structural bin)
- Cell: [defensive-profile, charge-stack, rhythm-profile]

### 4.9 Charge-up-and-release skill (PoE Charged Dash, bow-draw)

- Axis 3A: low tempo
- Axis 3B: spiky variance
- Axis 5: whatever economy supports the skill
- **Cell:** [low-tempo, spiky, economy-profile] — no special handling needed

---

## 5. Sim deferral matrix

Bins or sub-mechanisms that cannot be cleanly measured by the current sim route to **deferred-evaluation pool**. Generation continues for these; evaluation pauses until sim capability lands.

| Axis | Deferred element | Defer condition | Sim extension needed |
|---|---|---|---|
| 2A | proxy-light, proxy-heavy | Always — current sim solo-only | Player-side entity spawning, ally AI, target-selection extension, ally HP/death tracking |
| 3B | channeled-tagged kits | Conditional — depends on sim channel support | Continuous damage application, channel interruption, channel-resource-drain |
| 4 | dodger stealth/iframe sub-cases | Conditional — depends on sim mechanism support | Stealth (untargetable-for-duration); iframes (skill-cast-state); reflection (per-hit redirection) |
| 5 | charge-stack mechanic | Conditional — depends on sim charge support | Charge buildup triggers, cap behavior, decay timers, consumption skills |
| 5 | damage-taken-converts | Conditional — depends on sim conversion support | Damage-to-resource conversion at hit-resolution |

**Profile filter:** Profile A (Reincarnated Phase 0 shipping) excludes all currently-deferred bins from shippable seasons. As sim extends, deferred-pool kits get bulk-evaluated and the profile filter relaxes.

---

## 6. Substrate dependency summary

Consolidated list of substrate (generation-system + sim) extensions implied by the 8-axis lock. Legolas substrate-sufficiency audit will quantify gaps.

### Skill-metadata extensions (generation system)

1. `movement_displacement_per_cast` — Axis 1 mobility component
2. `aoe_radius` (likely exists) + `is_chain` + `is_multi_spawn` — Axis 2 geometry
3. `channel_tag` (likely exists) — Axis 3B channeled handling
4. Avoidance tags: `grants_evasion`, `grants_stealth`, `grants_iframes`, `grants_reflection` — Axis 4 dodger
5. `cost_type` ∈ {mana, rage, energy, spirit, HP, charge, ...} — Axis 5 resource handling
6. Charge-mechanic tags: `is_charge_pool`, `charge_cap`, `charge_decay` — Axis 5 charge-stack
7. `damage_to_resource_conversion` — Axis 5 damage-taken-converts
8. `is_reactive_trigger` (separate from reflection vs thorns) — Axis 2 measurement

### Sim telemetry extensions

1. Per-tick resource pool logging — Axis 5
2. Per-event damage application with source-tag (cast / reactive / proxy / environmental) — Axes 2, 3, 4
3. Per-hit damage application logs (not just totals) — Axis 4 avoidance_rate
4. HoT recovery distinct from mitigation — Axis 4 regenerator
5. Shield-pool tracking distinct from HP — Axis 4 absorber
6. Proxy entity lifecycle logging (spawn, action, despawn) — Axis 2A
7. Movement-skill displacement logging — Axis 1

### Sim mechanism extensions (deferred bins)

1. Player-side entity spawning + ally AI + target-selection — Axis 2A proxy-light/heavy
2. Stealth (untargetable-for-duration) — Axis 4 dodger sub-case
3. Iframe windows (skill-cast-state immunity) — Axis 4 dodger sub-case
4. Reflection (per-hit damage redirection) — Axis 4 reflection
5. Charge buildup + cap + decay mechanics — Axis 5 charge-stack
6. Damage-to-resource conversion at hit-resolution — Axis 5 damage-taken-converts
7. Variable cast-time + charge-state — Axis 5 charge-up-skill (affects Axis 3 rhythm)
8. Channel-tagged skill mechanics — Axis 3B channeled

### Substrate variety (5× rule per bin)

Per axis, generation must produce ≥ 5 × (bin count) distinguishably-different outputs to populate the archive meaningfully:

| Axis | Bins | Substrate count required |
|---|---|---|
| 1 | 6 | ~30 distinguishable engagement profiles |
| 2 | 5 | ~25 distinguishable damage geometries |
| 2A | 3 | ~15 distinguishable proxy configurations |
| 2B | 3 | ~15 distinguishable control compositions |
| 3A | 3 | ~15 distinguishable damage tempos |
| 3B | 3 | ~15 distinguishable variance profiles |
| 4 | 4 | ~20 distinguishable defensive profiles |
| 5 | 7 | ~35 distinguishable economy mechanisms |

The Legolas audit will measure current substrate state against each row.

---

## 7. Cell-count math + coverage analysis

### 7.1 Total cells

```
6 × 5 × 3 × 3 × 3 × 3 × 4 × 7 = 68,040 cells
```

### 7.2 Coverage at projected archive sizes

| Total seasons in archive | Coverage % | Functional? |
|---|---|---|
| 100 | 0.15% | Marginal — early-engine state |
| 500 | 0.7% | Below ideal but workable |
| 1,000 | 1.5% | **Target operating state** |
| 5,000 | 7.4% | Mature engine |
| 10,000 | 14.7% | Long-running deployment |

### 7.3 Math-gate stability checks

| Gate | Threshold | Status at 1k seasons |
|---|---|---|
| Pareto dominance | ≥ 2 entries | ✓ Trivially met |
| Mahalanobis covariance (8D) | ≥ 44 samples for stability | ✓ ~23× threshold |
| Crowding distance | ~10× cells populated | ⚠ Sparse; signal noisier than dense archive |
| Hypervolume contribution | Any cardinality | ✓ Functional |
| LUCB1 theme BAI | O(log(K/δ)/Δ²) pulls | ✓ Independent of archive size |
| KL information-gain | 100+ entries low-dim, 1000+ moderate | ✓ At threshold |

### 7.4 Caveats

- **Crowding-distance signal noise**: in sparse archives, neighborhoods have fewer occupants, so crowding-based diversity selection becomes noisier. Mitigation: use hypervolume contribution as primary diversity signal; crowding as secondary.
- **Empty-cell prevalence**: 98.5% of cells will be empty at 1k seasons. This is design intent — sparse-by-design exploration. Empty cells mark unexplored archetype space.
- **Substrate sufficiency is the harder constraint** than cell count. Per-axis substrate gaps (Axis 2A proxy-side, Axis 5 charge mechanics) matter more for archive quality than absolute coverage percentage.

---

## 8. Engineering disciplines mapping

The axis-lock work surfaces several connections to the existing engineering-disciplines.md:

| Discipline | Connection |
|---|---|
| #1 (math-before-code) | All measurement formulas specified before sim implementation |
| #2 (smoke-test vs full-regen) | Calibration sweeps will use smoke-test mode initially |
| #13a (drift detection) | Operational definitions enable code-vs-doc comparison at implementation review |
| #13b (per-variable attribution unknown without ablation) | Cross-axis cell address captures hybrids without inventing attribution claims |
| #17 (empirical-calibration smoke gate) | All ARPG-canonical-prior thresholds explicitly require first-deployment calibration |
| #18 (joint-gate ship criterion — pending Matt approval) | Mechanical BC measurement is one half; cohesion BC + visual BC complete the joint-gate |

The axis-lock work itself is an instance of Discipline #1 — every measurement is specified mathematically before any sim or generation code lands.

---

## 9. Open questions + calibration items

Items pending empirical calibration once the QD-engine deploys:

1. **Engagement profile thresholds** (Axis 1): range 3.0/8.0 tiles; mobility 30 tiles/min. Verify against shipping kit telemetry.
2. **Damage geometry thresholds** (Axis 2): `aoe_radius` 0.5/3.0. Verify against current 16-type palette distribution.
3. **Proxy count thresholds** (Axis 2A): 1.0/3.0 active proxies. May need adjustment post sim-extension.
4. **Control budget thresholds** (Axis 2B): 20%/60%. Verify against canonical-class telemetry.
5. **Damage tempo thresholds** (Axis 3A): 2/6 events/sec. Adjust by ARPG combat pace.
6. **Damage variance thresholds** (Axis 3B): CV 0.3/0.7. Adjust empirically.
7. **eHP_effective_ratio thresholds** (Axis 4): 2.0/5.0. May need balance-loop calibration.
8. **Avoidance_rate threshold** (Axis 4): 0.40. May need empirical adjustment.
9. **Resource economy thresholds** (Axis 5): mean 0.30/0.85, variance 0.20, hp_cost 0.50, charge 0.75. Multiple calibration points.
10. **encounter_duration_target** (Axis 4 eHP formula): 30s initial. Tune to actual fight-length distribution.

Per Discipline #17, all thresholds should be re-calibrated against shipping telemetry before first production use of the BC measurements.

### Multi-resource measurement noise

The Axis 5 primary-bottleneck rule for multi-resource kits has known noise — primary resource may shift mid-fight. Worth empirical study of how often this happens before locking the rule. Mitigation already specified: measure across multiple fights, not per-fight.

### Hybrid edge cases not yet tested

The 8-axis architecture has been stress-tested against named hybrid archetypes (§ 4). Additional edge cases may emerge from first-deployment telemetry:

- Multi-form classes (D2 Druid form-shifting) — does kit identity change per form?
- Companion-class hybrids (D3 monk Mystic Ally — is it proxy-light or proxy-heavy depending on stacks?)
- Buff-uptime stackers crossed with damage-taken-converts (PoE warcry + CWDT)

These get characterized post-deployment via Discipline #13b ablation if needed.

---

## 10. Dependencies + gates

### 10.1 Gates from current state to QD-engine rebuild start

1. **Recompose-validation hive ships** (currently firing 2026-05-19/20). Demonstrates floor-widening + recompose-trigger work. Unblocks generation-system confidence.
2. **Legolas substrate-sufficiency audit complete** (dispatch fired 2026-05-20). Confirms per-axis substrate variability or surfaces costed enrichment paths.
3. **Axis-lock approval** (this document — locked 2026-05-20 with Matt). Operational specification stable for rebuild planning.
4. **Discipline #17 calibration plan authored** — empirical-calibration procedure for all threshold values, fires on first-deployment telemetry.
5. **Sim extension scope-of-work authored** — for deferred bins (proxy-light/heavy, dodger sub-cases, charge mechanics, damage-conversion). May be parallel rebuild track or post-rebuild Phase.

### 10.2 What the rebuild produces

Per § 8 of vision doc, the QD-engine rebuild over 18-26 weeks delivers:

- Engine core implementing MAP-Elites over these 8 axes
- Profile assembly layer (Profile A/B/C/D)
- Theme coalescence via LUCB1 (cohesion-BC archive — parallel work)
- Visual-similarity scoring (visual-BC archive — galadriel-owned)
- Math-gate implementations per § 5 of vision doc (Pareto, Mahalanobis, hypervolume, etc.)

### 10.3 Reincarnated Phase 0 ship-readiness via Profile A

Profile A excludes currently-deferred bins from shippable seasons. With Axis 2A proxy-light/heavy deferred + Axis 4 dodger sub-cases partially deferred + Axis 5 charge mechanics deferred, Profile A operates on a reduced cell-space:

```
6 × 5 × 1 (solo only) × 3 × 3 × 3 × 4 × 4 (HP-econ + starved + gen-spender + steady)
= 25,920 cells
```

That's the *Profile A operational archive*. Reincarnated Phase 0 ships from this cell-space; expands as sim extensions land.

---

## 11. Cross-references

- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — the architectural target this doc operationalizes; § 2 BC axes (now superseded by this doc); § 5 math gates; § 6 dependency chain
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — currently-firing hive; ships before rebuild starts
- `canonical/09-geometry-palette-discussion.md` — 16-type palette feeding Axis 2 substrate
- `canonical/17-gear-and-spirit-guide-design.md` — gear architecture relevant to Axes 3, 4, 5
- `agentic_orchestration/dispatches/2026-05-20-legolas-substrate-sufficiency-audit.md` — substrate audit dispatch (will be updated to reflect 8-axis lock)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1, #2, #13a, #13b, #17, #18 referenced

---

## 12. Maintenance and revision protocol

### When to revise this doc

- Any threshold value changes after Discipline #17 calibration
- Any bin label changes (with cross-doc impact)
- Any axis count change (would require companion vision-doc amendment)
- New hybrid archetypes that don't fit cross-axis capture and warrant own bin
- Sim deferral status changes (deferred → supported, or vice versa)

### Who can revise

- **gandalf** authors revisions
- **Matt approves** for any structural change (axis count, bin count, bin labels)
- **knight-rider drafts** the decisions-log entry capturing the change
- **jack-ryan reviews** the revision against existing decisions and disciplines

### Versioning

This document is v1.0 (initial lock 2026-05-20). Subsequent versions bump v.minor for threshold calibrations and v.major for structural changes.

---

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine architectural commitment, operationalized.
