# W0.8 Deliverable — Axis 2 Damage Geometry: Substrate Completeness Check

**Author:** rocket
**Date:** 2026-05-21
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-rocket-w0-8-axis-2-substrate-check.md`
**Status:** COMPLETE
**Feeds:** P1 W1.5 (movement-skill expansion), P1 W1.7 (legolas Phase 2 depth pass)

---

## 0. Sources and interpretive rules

**Sources consulted (empirical, not estimated):**

- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — Axis 2 operational spec, 5 bins, folded-mechanism table
- `canonical/09-geometry-palette-discussion.md` — 16-type → 26-type canonical geometry palette, all revisions through 2026-05-16
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/internal-substrate-state.md` — Phase 1 findings (chain "thin", multi-spawn "thin")
- `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` — VALID_GEOMETRIES frozenset (line 231-247); role geometry pools; 26 active emit entries in legolas's count vs 28 in current code
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` — archetype geometry_bias definitions, AOE_GEOMETRIES frozenset
- `reincarnated-engine/src/reincarnated/generation/archetype_composer.py` — _ROLE_GEOMETRY_PREFS table, substrate × role geometry bias composition
- `reincarnated-engine/config/substrate_identities/*.yaml` — all 7 substrate geometry_affinities blocks

**Interpretive rules applied (per dispatch open questions):**

1. Multi-bin form types (e.g., a geometry whose AOE radius could straddle small/large): assigned to dominant bin per damage-weighted argmax intent (Axis 2 measurement spec § 3.2 of BC-axes-lock). Documented case-by-case below.
2. Chain bounce-count differences (3-bounce vs 8-bounce) are distinguishable templates, not one parameterized template. The dispatch explicitly resolved this: do NOT parameterize as one. Each distinct bounce-count variant that appears in the archetype pool counts separately.
3. Multi-spawn bin scope: multi-spawn projectile/AOE clouds (Axis 2 territory) vs proxy entities (Axis 2A territory). Totem and aura produce sustained placed effects — counted under multi-spawn (Axis 2) for Axis 2 coverage, but their Axis 2A proxy-entity classification is separately deferred (BC-axes-lock § 3.3).

**Substrate-agnostic stance (Track C + substrate-as-cohesion-only architectural recommitment):**

All 16/28 canonical geometry types are mechanical-shape descriptors available to any element. No per-substrate weighting in this mapping. The 5× rule applies uniformly: ~25 distinguishable templates per Axis 2 bin regardless of which element expresses them.

---

## 1. Inventory of active geometry types

VALID_GEOMETRIES in `ability_grammar.py` (line 231-247) has **28 entries** in the current engine state:

```
aura, beam_channel, blink, chain_lightning, circle, cone, dash_attack,
defensive_dash, fork, ground_slam, ground_targeted_circle, leap_strike,
line, melee_arc, melee_strike, multi_projectile, persistent_zone,
projectile, ranged_physical, ricochet_bounce, ring, roll, self_buff,
single_target, teleport, totem, vortex_pull, whirlwind
```

**Reconciliation with canonical-09:** The final canonical-09 table (after Track 4 collapse 2026-05-16) counts 26 active types. The engine has 28. The 2-entry difference is `melee_strike` (CORE from 2026-05-08; in the code but may have been undercounted in the canonical-09 table header) and `aura` reclassification. The legolas Phase 1 report also cites 26. The canonical-09 note at the Track 4 collapse entry says "the 25 count was already correct for the emit pool" at B11, which predates B13's +5 defensive mobility types (but 3 of those are B13-deferred character-animation primitives: roll, parry_active, block_active). Of the 5 B13 geometries in the 2026-05-16 table (roll, defensive_dash, strafe_mode, blink, dodge_stance), only roll/blink/defensive_dash appear in VALID_GEOMETRIES. `strafe_mode` and `dodge_stance` are absent from the code emit pool — they are B13-deferred. This accounts for the discrepancy. **Code is authoritative: 28 in VALID_GEOMETRIES as of the current pre-W0.2 state.**

**Of the 28, 6 are non-damage (Axis 2 does not classify them):**
- `blink`, `roll`, `defensive_dash` — pure defensive mobility, no damage application
- `teleport` — movement geometry, no damage application
- `self_buff` — defensive/utility buff, no damage application

That leaves **22 damage-bearing or damage-capable geometry types** for Axis 2 binning:

```
aura, beam_channel, chain_lightning, circle, cone, dash_attack,
fork, ground_slam, ground_targeted_circle, leap_strike, line,
melee_arc, melee_strike, multi_projectile, persistent_zone,
projectile, ranged_physical, ricochet_bounce, ring, totem,
vortex_pull, whirlwind
```

Note: `totem` produces damage via pulses from a placed entity — classifies to multi-spawn (Axis 2) under the dispatch's multi-spawn scope clarification (placed damage entities that fire independently, not proxy-entity AI). `aura` and `persistent_zone` are passive/sustained AOE — classified to large-AOE or small-AOE per radius.

---

## 2. Mapping table: 16-type canonical palette → 5 Axis 2 bins

The Axis 2 operational spec (BC-axes-lock § 3.2) provides bin assignment priority:
**chain-tag → multi-spawn-tag → aoe_radius thresholds → single-target default.**

Bin definitions:
- **single-target:** one entity hit per damage event; aoe_radius ≤ 0.5 tiles
- **small-AOE:** area damage 0.5 < aoe_radius ≤ 3.0 tiles
- **large-AOE:** area damage aoe_radius > 3.0 tiles
- **chain:** damage hops between targets via jump-targeting logic
- **multi-spawn:** multiple independent damage entities/projectiles per cast

For radius-ambiguous types (no aoe_radius tag on Ability schema per legolas Phase 1), I assign based on canonical ARPG exemplar sizes and the geometry's design intent from canonical-09.

| # | Geometry type | Axis 2 bin | Basis for assignment | Radius notes |
|---|---|---|---|---|
| 1 | `single_target` | **single-target** | One entity hit; aoe_radius = 0 by definition | No radius |
| 2 | `projectile` | **single-target** | Single bolt; hits one entity unless chain/fork mod applied; default=single | aoe_radius ≤ 0.5 |
| 3 | `ranged_physical` | **single-target** | Ballistic shot; pierce/multishot are parameter variants on same geometry; base hit is single-target | aoe_radius ≤ 0.5 |
| 4 | `melee_strike` | **single-target** | Close-range single hit on one entity; requires adjacency; canonical exemplar: D2 Bash | No radius |
| 5 | `cone` | **small-AOE** | Frontal fan; ARPG exemplar cone spreads ~2-3 tile depth; fits small-AOE. *Multi-bin edge:* at wide-cone/long-range could exceed 3.0 tiles, but dominant use in canonical-09 is frontal close/mid fan — small-AOE argmax | radius ~2-3 tiles |
| 6 | `circle` | **small-AOE** | Radial around caster; D3 Frost Nova exemplar ~2 tile radius; fits small-AOE as default; large-scale circle (D3 Black Hole equivalent) exists but is expressed via `ground_targeted_circle` | radius ~1.5-2.5 tiles |
| 7 | `line` | **small-AOE** | One-shot line; width is narrow but length is long; canonical-09 "AOE" classification; assigned small-AOE on damage-weighted argmax (linear strip, typically < 3 tile width) | narrow strip |
| 8 | `melee_arc` | **small-AOE** | Close-range frontal sweep; sweep_shape parameter (pie/crescent/wide_arc); stays in small-AOE — melee engagement radius ≤ 3 tiles by definition | radius ≤ 3 tiles |
| 9 | `ground_slam` | **small-AOE** | Close-range AOE around caster; D2 Dragon Tail style; near-caster impact radius ~2-3 tiles | radius ~2-3 tiles |
| 10 | `ring` | **small-AOE** | Donut AOE; outer radius minus inner radius; Shock-Nova archetype (D2); typically caster-centered close-mid range; fits small-AOE dominant | outer ~2-3 tiles |
| 11 | `vortex_pull` | **small-AOE** | Pulls enemies to a point + applies AOE at destination; AOE footprint small (point attractor); classified small-AOE | footprint ~1-2 tiles |
| 12 | `fork` | **small-AOE** | Projectile splits into N on impact; split footprint covers a spread but each fork is relatively small-AOE; PoE Fork support — classified small-AOE per damage-weighted argmax (spread fans are short-range secondary impacts) | spread ~2-3 tiles |
| 13 | `whirlwind` | **small-AOE** | Rotating AOE while moving; D3 Barbarian Whirlwind; caster-centered with spin radius ~2-3 tiles | radius ~2 tiles |
| 14 | `dash_attack` | **small-AOE** | AOE damage along dash path; motion-bounded; typically narrow corridor hit < 3 tile width | path-width |
| 15 | `leap_strike` | **small-AOE** | Landing AOE; D3 Earthquake-style; *multi-bin edge:* landing impact can be 2-4 tiles radius. Dominant mechanic is the landing AOE which is typically 2-3 tile radius — small-AOE argmax | landing ~2-3 tiles |
| 16 | `ground_targeted_circle` | **large-AOE** | Placed AOE at cursor location; D3 Black Hole / Meteor analogues; canonical-09 notes this as "placed, absorbs delayed_strike"; larger ground-targeted zones are typically 3-6 tile radius | radius ~3-6 tiles |
| 17 | `persistent_zone` | **large-AOE** | Placed, persists; canonical exemplar PoE Ground Slam echo, persistent burning ground; extended area effect; typically ≥ 3 tile radius | radius ~3-5 tiles |
| 18 | `aura` | **large-AOE** | Sustained radial AOE following caster; D2 Paladin aura radius ~4-8 tiles; always large-AOE by ARPG canon | radius ~4-8 tiles |
| 19 | `beam_channel` | **large-AOE** | Sustained line held while channeling; beam length typically extends to 6-10 tiles; classified large-AOE by length dimension | length ~6-10 tiles |
| 20 | `chain_lightning` | **chain** | Chain-tag by design; projectile hits primary then arcs to N nearby targets; canonical exemplar D2 Chain Lightning / PoE Chain support | jump-targeting |
| 21 | `ricochet_bounce` | **chain** | Projectile bounces target-to-target; shares multi-target dispatch with chain_lightning; canonical chain classification | bounce-targeting |
| 22 | `multi_projectile` | **multi-spawn** | Radial burst — N projectiles simultaneously at distributed angles; D3 Meteor shower / Multishot analogues; each projectile is an independent damage entity | N projectiles |
| 23 | `totem` | **multi-spawn** | Placed entity that pulses effects from fixed location; independent damage entity (not proxy AI); canonical-09 distinguishes from `persistent_zone` by entity model | placed entity |

**Non-damage types (not binned for Axis 2):**

| Geometry | Why excluded |
|---|---|
| `blink` | No damage; movement-only (i-frame window) |
| `roll` | No damage; evasion movement |
| `defensive_dash` | No damage; repositioning |
| `teleport` | No damage; instant relocation |
| `self_buff` | No damage; applies to caster only |

---

## 3. Per-bin summary

| Axis 2 bin | Canonical-09 geometry types | Count |
|---|---|---|
| single-target | single_target, projectile, ranged_physical, melee_strike | 4 |
| small-AOE | cone, circle, line, melee_arc, ground_slam, ring, vortex_pull, fork, whirlwind, dash_attack, leap_strike | 11 |
| large-AOE | ground_targeted_circle, persistent_zone, aura, beam_channel | 4 |
| chain | chain_lightning, ricochet_bounce | 2 |
| multi-spawn | multi_projectile, totem | 2 |

**Total damage-bearing geometry types mapped: 23.** (22 damage types + totem which the schema places in the "other" category in canonical-09 but classifies as multi-spawn under Axis 2 dispatch rules.)

---

## 4. Distinguishable templates per bin — empirical count

A "distinguishable template" = a distinct kit-role composition that is mechanically differentiated from other templates in the same bin by: geometry choice, role pairing, modifier behavior, bounce/radius parameter, or energy type. Per the dispatch, chain bounce-count differences ARE distinguishable templates.

**Sources:** b6_archetype_templates.py geometry_bias blocks; archetype_composer.py _ROLE_GEOMETRY_PREFS table; ability_grammar.py role geometry pools; legolas Phase 1 per-bin assessment.

### 4.1 Single-target bin

Active geometries: single_target, projectile, ranged_physical, melee_strike

From archetype templates, the distinct configurations that produce single-target primary damage output:

| Template combination | Geometry | Role shape | Energy | Distinguishing mechanic |
|---|---|---|---|---|
| Hunter (burst) | ranged_physical + projectile preferred | primary_attack + burst_damage, focus energy | focus | ballistic + pierce flag; escape mobility required |
| Physical warrior (melee primary) | melee_strike preferred | primary_attack, rage energy | rage | adjacency required; cleave paired |
| Physical skirmisher (gap melee) | melee_strike preferred | primary_attack + mobility, combo energy | combo | mobile attack constraint; dash follow-through |
| Rogue (melee) | melee_strike preferred | primary_attack + 2× mobility, combo energy | combo | 2-mobility constraint; blink + roll required |
| Physical grappler (melee) | melee_strike preferred | primary_attack + control, rage energy | rage | control-with-ailment constraint |
| Elemental burst mage (7×) | projectile preferred | primary_attack + burst_damage, mana | mana | per-substrate 7 variants (fire/water/earth/wind/lightning/holy/shadow projectile burst) |

Counting distinguishable configurations: the 5 physical archetype single-target patterns + 7 substrate-distinct elemental projectile burst patterns = **~12 distinguishable single-target templates.**

Legolas Phase 1 estimated "4 distinct geometries" for single-target — that counts geometry types only, not kit-role compositions. Using kit-role-composition grain gives 12. For BC-archive purpose, what matters is whether different kits land in single-target bin with different BC coordinates on OTHER axes (tempo, economy, etc.) — and these 12 variants absolutely do (melee rage vs ranged focus vs elemental mana have distinct Axis 3/5 signatures). **Single-target bin: ~12 distinguishable templates.**

### 4.2 Small-AOE bin

Active geometries: cone, circle, line, melee_arc, ground_slam, ring, vortex_pull, fork, whirlwind, dash_attack, leap_strike (11 geometries)

The archetype generator produces AOE-dominant kits via area_damage and control roles. Small-AOE geometries appear prominently in:
- All 7 substrate × area_damage compositions (circle/cone/ring biased per substrate)
- All 7 substrate × control compositions (vortex_pull heavy for wind/earth; ring/circle for others)
- Physical warrior (melee_arc + whirlwind + ground_slam in AOE slots)
- Physical grappler (melee_arc + vortex_pull)
- Physical skirmisher (whirlwind + dash_attack)
- Hunter (fork; ricochet_bounce — classified small-AOE per fork's split footprint)

Distinguishable small-AOE templates:
- 7 substrate × area_damage = 7 variants (each with different geometry bias: water=circle+wave, wind=cone+swirl+vortex, earth=ground_slam+pillar+cone, fire=burst+cone, lightning=arc+branching, holy=nova+shaft, shadow=tendril+creep)
- 7 substrate × control = 7 variants (controller emphasis on vortex_pull, ring, ground_targeted_circle at small radius)
- Physical warrior (melee_arc + whirlwind pair) = 1 distinct template
- Physical grappler (melee_arc + vortex_pull) = 1 distinct template
- Physical skirmisher (whirlwind + dash_attack) = 1 distinct template
- Hunter small-AOE (fork + ricochet_bounce in area_damage slots) = 1 distinct template
- Within elemental area_damage: cone vs circle vs ring creates further sub-differentiation (cone = directional, circle = caster-centered, ring = donut) — each geometry is a distinct template variant

Rough count at kit-role-composition grain: 7 + 7 + 4 physical variants + parameter-variant sub-counts across 11 geometries. Conservatively, **~20-22 distinguishable small-AOE templates** (well within range of meeting 5× rule; the geometry richness here is the highest of all bins).

### 4.3 Large-AOE bin

Active geometries: ground_targeted_circle, persistent_zone, aura, beam_channel (4 geometries)

Distinguishable configurations:
- 7 substrate × area_damage templates where geometry lands ground_targeted_circle or persistent_zone (water/earth/holy substrates heavily weight ground_targeted_circle and area_sustain/persistent)
- Beam_channel configurations: lightning substrate × burst_damage (shaft/bolt_line → beam_channel); water/earth control × beam channel (restricted per ability_grammar.py `_beam_channel_allowed`)
- Aura configurations: restricted by `_aura_allowed()` (support role any element, or control × earth/water only); 7 substrates × support role = 7 aura-slot templates; earth/water × control = 2 additional
- damage_falloff parameter variations on radial geometries (uniform / linear / exponential) — these are canonically distinguishable modifiers per BC-axes-lock (produce different tempo + variance signatures)

Counting: ~7 substrate × (area_damage where large-AOE dominates) + ~9 aura-eligible configurations + beam_channel variants (~4 substrate × role combinations where beam is accessible) = **~18-20 distinguishable large-AOE templates.** Marginal against the 5× target of ~25, but likely close enough that natural variation through generation pressure fills the gap.

### 4.4 Chain bin

Active geometries: chain_lightning, ricochet_bounce (2 geometries)

Per dispatch rules: bounce-count differences are distinguishable templates.

What exists today for each geometry:

**chain_lightning:**
- `is_chain` metadata flag is ABSENT from Ability schema (legolas Phase 1, BC Metadata Extension Summary). Geometry type name `chain_lightning` is present in VALID_GEOMETRIES and in archetype bias pools.
- Only substrate with PREFER affinity for chain_lightning: **lightning** (lightning.yaml geometry_affinities: `chain_lightning: PREFER`)
- Substrates with AVOID: earth (`chain_lightning: not listed as AVOID for earth` — actually earth.yaml avoids `bolt_line` and `branching`, not chain_lightning directly; holy.yaml explicitly AVOID chain_lightning)
- In archetype_composer.py _ROLE_GEOMETRY_PREFS: chain_lightning scores burst_damage=1.5, area_damage=1.0, control=1.0 — accessible across multiple roles
- In ability_grammar.py role pools (line 128-133): chain_lightning weight 0.6 in primary burst pool; weight 0.8 in burst_damage secondary pool
- Physical archetype templates: hunter PREFERS ricochet_bounce; no physical template preferring chain_lightning

Templates accessible for chain bin today:
1. Lightning × burst_damage (chain_lightning primary; lightning PREFER × burst_damage 1.5 = max weight)
2. Lightning × area_damage (chain_lightning; lower weight but accessible)
3. Lightning × control (chain_lightning; PREFER but control weights it at 1.0)
4. Other substrates × any role (chain_lightning at neutral/accessible weight; fire/water/earth/wind/shadow all neither PREFER nor AVOID chain_lightning explicitly — they will produce some chain_lightning kits)
5. Hunter (ricochet_bounce PREFER — this is technically bounce-chain, classified in chain bin)

If we count distinct bounce-count variants as distinguishable: `chain_lightning` with N=2 bounces vs N=3 bounces vs N=5 bounces would each be a separate distinguishable template. BUT: the current ability grammar generates chain_lightning as a geometry type without specifying a bounce count parameter in the Ability schema. There is no `bounce_count` field. The chain geometry exists as a single unparameterized type. This means, at pre-W0.2 state, **chain bounce-count variations are not represented as distinct templates** — the system produces one flavor of chain_lightning regardless of substrate or role.

Current distinguishable chain templates (empirical count):
1. chain_lightning × lightning substrate × burst_damage role (strongest pull, likely present)
2. chain_lightning × other substrates × burst_damage role (accessible but weak pull; less likely to dominate damage-weighted argmax over other burst geometries)
3. ricochet_bounce × hunter archetype (PREFER; likely present in hunter kits as fork/ricochet variant)
4. ricochet_bounce × other non-physical archetypes (accessible at 0.4 weight in ability_grammar base pool)

**Empirical chain bin count: ~3-4 distinguishable templates.** This matches and slightly updates legolas's Phase 1 "2 geometries (chain_lightning, ricochet_bounce)" finding — when we count role × substrate combinations that actually produce chain-dominant kits in practice, we get 3-4 rather than 2, but still dramatically below the 5× target.

### 4.5 Multi-spawn bin

Active geometries: multi_projectile, totem (2 geometries)

**multi_projectile:**
- `is_multi_spawn` metadata flag ABSENT from Ability schema (legolas Phase 1)
- In VALID_GEOMETRIES and bias pools; weight 0.6 in base burst pool, 0.6 in secondary
- archetype_composer.py: multi_projectile burst_damage=1.5, area_damage=1.5, control=0.7
- Hunter archetype: multi_projectile NEUTRAL (1.0 weight)
- No substrate explicitly PREFER multi_projectile (none in any substrate YAML geometry_affinities)

**totem:**
- In VALID_GEOMETRIES; in ability_grammar role pools (damage_over_time weight 1.5, utility weight 1.5)
- ability_grammar.py `_build_ability()` handles totem/aura: "lower tick damage (50%), longer duration (10–20s)"
- Classified multi-spawn for Axis 2 purposes: independent damage entity firing repeatedly
- PERSISTENT_GEOMETRIES frozenset in b6_archetype_templates.py includes totem (alongside persistent_zone and aura)
- water_controller archetype constraint: `require_persistent_geometry` — totem/persistent_zone/aura must appear

Current distinguishable multi-spawn templates:
1. multi_projectile × hunter archetype (ranged burst; N-projectile radial burst; focus energy)
2. multi_projectile × elemental burst_damage role (accessible at weight 0.6; any substrate)
3. multi_projectile × elemental area_damage role (weight 0.6 base; less likely to dominate)
4. totem × water_controller (require_persistent constraint; totem specifically weighted; water dominant)
5. totem × elemental control roles generally (earth/water control both PREFER area_sustain which pairs with totem in damage_over_time slots)
6. totem × utility role in area_damage archetype (utility role PREFER totem weight 1.5)

**Empirical multi-spawn bin count: ~5-6 distinguishable templates.** Marginally above legolas Phase 1 "2-3" estimate because counting role × substrate combinations surfaces more than just counting geometry types. But still severely below the 5× target of ~25.

The key constraint: multi_projectile and totem are both mechanically shallow in the current system — multi_projectile has no projectile-count parameter, no angle_distribution beyond the parameter addition documented in canonical-09 B11, and totem has no pulse-rate or damage-ramp differentiation.

---

## 5. Per-bin gap to 5× rule

Target: ~25 distinguishable templates per bin (5× the 5-bin count).

| Axis 2 bin | Current distinguishable templates | 5× target | Gap | Priority |
|---|---|---|---|---|
| single-target | ~12 | ~25 | ~13 | MEDIUM (functional but needs growth) |
| small-AOE | ~20-22 | ~25 | ~3-5 | LOW (near target; small-AOE is richest bin) |
| large-AOE | ~18-20 | ~25 | ~5-7 | MEDIUM (marginal; enrichment helps) |
| chain | ~3-4 | ~25 | ~21-22 | HIGH (critically thin; confirmed by legolas) |
| multi-spawn | ~5-6 | ~25 | ~19-20 | HIGH (critically thin; confirmed by legolas) |

**Total current distinguishable templates (all bins): ~58-64.** Against a 5× target of ~125 total, the current substrate is at approximately **46-51% of target.** The deficit is almost entirely concentrated in chain and multi-spawn.

---

## 6. Enrichment seed list — chain bin (HIGH priority)

Target: ≥10 candidate templates for P1 W1.5/W1.7 consumption.

All candidates are substrate-AGNOSTIC (any element can express them). Each entry includes BC-axis contribution tags using the axes-lock terminology.

**Interpretation note on bounce-count distinguishability:** the dispatch confirmed that chain bounce-count differences are distinguishable templates. Each candidate below that varies bounce behavior is therefore a distinct template, not a parameter variant of one.

---

### C-1: Short-chain strike (2-bounce, instant)
2 targets hit in rapid succession; primary damage on first target, secondary on bounce; near-instant resolution (no travel time between bounces).
- **BC tags:** chain bin; Axis 3A tempo = high (rapid multi-hit); Axis 3B variance = flat (predictable 2-target rotation); Axis 1 = mid-range or ranged depending on kit composition.

### C-2: Extended-chain arc (5-bounce, fading damage)
5 bounces with damage decaying 20% per bounce; encourages positioning in clustered enemies; PoE Lightning Arrow chain support analogue.
- **BC tags:** chain bin; Axis 3A tempo = medium (bounce resolution time spreads events); Axis 3B variance = variable (decay produces per-event magnitude gradient); fits generator-spender or steady economy kits.

### C-3: Heavy-chain slam (3-bounce, AoE on landing)
Projectile chains to 3 targets but each chain-hit also creates a small-AOE splash on the bounce target; dual bin presence (chain primary, small-AOE secondary); damage-weighted argmax = chain if chain damage > splash damage.
- **BC tags:** chain bin (primary); Axis 3B variance = variable (initial hit vs splash asymmetry); Axis 2B control density = mixed if AOE splash applies CC.

### C-4: Control chain (2-3 bounce, CC rider)
Chain projectile that applies an ailment (chill, shock, or root) on each bounce target in addition to damage; primary contribution to control-pure or mixed control density.
- **BC tags:** chain bin; Axis 2B = mixed or control-pure; Axis 3A = medium tempo; pairs with water_controller, earth_controller, or lightning_controller archetypes.

### C-5: Melee ricochet (2-bounce, close-range chain)
Melee attack bounces to an additional nearby target after the primary hit; close-range engagement profile; distinct from ranged chain because it requires adjacency constraint on primary hit.
- **BC tags:** chain bin; Axis 1 = close-fast or close-slow (melee engagement); Axis 3A = high tempo (melee cadence); pairs with physical_warrior or grappler templates.

### C-6: Sustained-chain channel (5-bounce per tick, channeled)
Channeled skill that fires a chain projectile every tick; PoE Arc support analogue; high-frequency multi-target; 5 bounces per cast but casts fire continuously while channeled.
- **BC tags:** chain bin; Axis 3A = high tempo (channeled multi-event); Axis 3B = flat variance (uniform damage ticks); Axis 5 = starved or steady (channel drain); Axis 1 = ranged-slow (stand-and-channel playstyle).

### C-7: Charged-release chain (1-8 bounce based on charge time)
Charge-up mechanic produces chain projectile; longer charge = more bounces (1→8); releases all bounces simultaneously on release.
- **BC tags:** chain bin; Axis 3A = low tempo (charge-up windups dominate); Axis 3B = spiky variance (0 damage during charge, burst on release); Axis 5 = charge-stack (structural bin match).

### C-8: DoT-chain (3-bounce, persistent burn/bleed per target)
Chain that applies a DoT effect on each hit target rather than direct damage; Axis 3A tempo driven by tick rate rather than cast rate; chain bin classification because jump-targeting is the damage-delivery mechanism.
- **BC tags:** chain bin; Axis 3A = medium tempo (DoT ticks); Axis 3B = flat variance (uniform DoT ticks); Axis 2B = mixed (damage + DoT control component); pairs with shadow, water, or wind substrates.

### C-9: Fork-chain hybrid (3-fork then 2-bounce each)
Projectile forks into 3 on impact; each fork then chains to 1 nearby additional target; damage-weighted argmax = chain (if bounce targets outnumber fork targets in fight telemetry); distinct from pure fork (classified small-AOE) because the bounce-targeting geometry dominates.
- **BC tags:** chain bin; Axis 3B = variable (initial + fork + bounce produces magnitude gradient); Axis 3A = medium tempo; high-target-count potential → favors ranged engagement.

### C-10: Bouncing-ring (ricochet with AOE-on-landing)
ricochet_bounce variant where each bounce target receives an AOE splash rather than single-hit damage; small AOE splash on each bounce point creates area coverage; damage-weighted argmax stays chain if ricochet damage > splash.
- **BC tags:** chain bin; Axis 3B = variable (bounce-hit vs splash magnitude); Axis 2B = damage-pure or mixed; distinct from C-3 (that's a chain_lightning + slam combo; this is ricochet + AOE-on-bounce-point).

### C-11: Aura-chain hybrid (persistent aura that chains pulses)
Aura fires chain pulses at periodic intervals rather than continuous AOE damage; each pulse chains to 2-3 targets in range; distinct from plain aura (large-AOE bin) because chain-tag dominates the damage attribution in fight telemetry.
- **BC tags:** chain bin (if chain damage > aura damage in argmax); Axis 1 = ranged-slow; Axis 3A = low-medium tempo (pulse rate); Axis 3B = flat variance; Axis 5 = overflow or steady (aura sustain).

### C-12: Ground-chain (persistent zone that chains to nearby targets)
`persistent_zone` that at regular intervals fires a chain-linked strike to the nearest enemy and bounces once; placed mechanic + chain mechanic hybrid; damage-weighted argmax = chain if chain events dominate over zone passive ticks.
- **BC tags:** chain bin; Axis 1 = ranged-slow (place and stand); Axis 3A = medium tempo; Axis 5 = starved or steady depending on zone placement cost.

**Chain seed count: 12 candidates.** Meets the ≥10 requirement.

---

## 7. Enrichment seed list — multi-spawn bin (HIGH priority)

Target: ≥10 candidate templates for P1 W1.5/W1.7 consumption.

**Scope clarification applied:** multi-spawn = multiple independent damage entities/projectiles per cast (Axis 2 territory). Proxy entities with AI and independent HP (summons, mind-controlled enemies) are Axis 2A territory and EXCLUDED from this seed list. totem and multi_projectile are in scope; summon_combatant is out of scope per dispatch.

---

### M-1: Multi-projectile burst (N=3, spread)
3 projectiles fired simultaneously at distributed angles (default angle_distribution: spread); PoE Vaal Lightning Arrow / D3 Multishot analogue; each projectile is an independent damage entity.
- **BC tags:** multi-spawn bin; Axis 3A = high tempo (3× events per cast); Axis 3B = flat variance (uniform projectile damage); Axis 1 = ranged-fast or ranged-slow.

### M-2: Multi-projectile burst (N=5, cardinal/star)
5 projectiles in cardinal or star pattern; higher spawn count; more coverage than M-1; distinct because spawn-count changes the tempo signature (5× events vs 3×) and AOE footprint.
- **BC tags:** multi-spawn bin; Axis 3A = high tempo; Axis 3B = flat variance; distinct from M-1 by N count and angle_distribution parameter = distinguishable per dispatch rule.

### M-3: Multi-projectile burst (N=8, full radial)
8 projectiles in full 360° radial burst; Nova-style radial coverage; distinct template from M-1/M-2; N=8 produces 2.67× more events per cast than M-3 → distinct Axis 3A contribution.
- **BC tags:** multi-spawn bin; Axis 3A = very high tempo; Axis 3B = flat variance; Axis 1 = ranged-slow (usually stationary cast for full coverage utility).

### M-4: Totem (single, high pulse rate)
Single totem placed on field; pulses at high frequency (4-5 ticks/s); PoE Storm Totem analogue; damage-over-time contribution via proxy fire rather than DoT effect proper.
- **BC tags:** multi-spawn bin; Axis 3A = high tempo (rapid pulses); Axis 3B = flat variance (uniform tick); Axis 1 = ranged-slow (place and stand); Axis 5 = generator-spender (place costs mana, fight refills).

### M-5: Totem (dual, low pulse rate)
Two totems placed simultaneously; lower pulse rate per totem (2 ticks/s each); distinct from M-4 by entity count (2 spawned) and tempo signature (2 sources × 2 ticks/s = comparable to 1 × 4 ticks/s but different spatial distribution).
- **BC tags:** multi-spawn bin; Axis 2A = proxy-light threshold (2 proxies — pending sim extension); dual-placement geometry is mechanically distinct from single-totem; distinguish by spawn count.

### M-6: Multi-orb burst (N=4, homing)
4 orbs spawned simultaneously that track nearby enemies independently; D3 Wizard Arcane Orb scatter analogue; each orb is a distinct independent damage entity with targeting logic.
- **BC tags:** multi-spawn bin; Axis 3A = high tempo; Axis 3B = variable (homing orbs may hit at different times creating magnitude-per-time variance); Axis 1 = ranged.

### M-7: Ground-mine burst (N=3, proximity trigger)
3 mines placed that trigger on enemy proximity; delayed multi-spawn; distinct from instant multi-projectile because the damage events are player-placed but environmentally triggered; PoE Bodyswap / Mine Support analogue.
- **BC tags:** multi-spawn bin; Axis 3A = low tempo (mines fire when triggered, not on cast); Axis 3B = spiky variance (all 3 trigger simultaneously if proximity clustered → single burst); Axis 5 = generator-spender (mine placement costs vs refill between packs).

### M-8: Meteor shower (N=3-5, staggered landings)
Multiple meteors summoned per cast with staggered landing times; D3 Meteor Shower analogue; each meteor is an independent damage entity landing with small delay (0.5-1.5s between impacts); distinct from instant multi-spawn (M-1/M-2) by temporal stagger.
- **BC tags:** multi-spawn bin; Axis 3A = medium tempo (stagger spreads events); Axis 3B = flat variance (meteors similar damage); Axis 3A/3B signature is distinctly different from M-1 despite same spawn count.

### M-9: Totem (single, AOE pulse with ailment)
Single totem that pulses AOE damage + applies CC ailment per pulse; water_controller's require_persistent constraint fulfilled; distinct from M-4 (high-damage no-CC) because skill budget shifts toward control contribution.
- **BC tags:** multi-spawn bin; Axis 2B = mixed or control-pure; Axis 3A = medium tempo; pairs naturally with water or earth control archetypes; PERSISTENT_GEOMETRIES frozenset already tracks this.

### M-10: Dispersal cloud (N=5-8, persistent AOE fragments)
Cast spawns multiple small AOE "cloud" fragments that persist for 2-4s; each cloud is an independent damage entity applying DoT; distinct from persistent_zone (single placed area) because N separate smaller clouds are spawned.
- **BC tags:** multi-spawn bin; Axis 3A = high tempo (N clouds each ticking); Axis 3B = flat variance (uniform cloud DoT); Axis 1 = ranged-slow (place and stand); good water/shadow substrate expression for zone-denial.

### M-11: Fork-burst (N=3 on hit, radial)
`fork` mechanic at higher fork count: primary projectile hits and spawns 3 secondary projectiles that travel outward; each secondary projectile is an independent damage entity; distinct from ricochet_bounce (targets-to-targets) because fork spawns new entities on impact rather than redirecting the original.
- **BC tags:** multi-spawn bin if fork-spawned entities count as independent (vs small-AOE if treated as AOE splash); under the dispatch's multi-spawn definition ("multiple independent damage entities/projectiles per cast"), fork-spawned projectiles qualify; Axis 3A = high tempo; Axis 3B = variable.

### M-12: Persistent aura (large-radius, multi-tick entity)
`aura` geometry reclassified to multi-spawn under the interpretation that the aura is a sustained independent damage entity following the caster rather than a passive AOE field; distinct from `persistent_zone` (static) and from `aura` in large-AOE (when classified per radius alone) because the entity persists across movement; Axis 2 classification may remain large-AOE for radius-dominated measurement, but if tick-sources are logged as distinct entity outputs, it approaches multi-spawn semantics.
- **Note:** This candidate sits at the large-AOE / multi-spawn bin boundary. Dominant bin per damage-weighted argmax will depend on sim implementation. Flag for P1 W1.7 Discipline #17 calibration.
- **BC tags:** multi-spawn (candidate) or large-AOE; Axis 3A = high tempo; Axis 3B = flat variance.

**Multi-spawn seed count: 12 candidates.** Meets the ≥10 requirement.

---

## 8. OQ-7: Water DPS density disposition

**OQ-7 (from Track C synthesis § 3.3):** Water modifier range (0.134–0.258) is notably higher than fire/lightning (0.072–0.134) despite comparable kit structures. Water's sustained-presence zone-denial pillar may produce systematically lower instantaneous DPS density, requiring higher modifier scaling to hit the same per-tier win rate.

**Axis 2 implication:**

Water substrate geometry affinities (water.yaml): PREFER `area_sustain`, `circle`, `wave`, `ground_targeted_circle`. These all resolve to persistent or medium-cadence AOE — large-AOE and small-AOE bins respectively. They produce distributed damage across many ticks rather than front-loaded instantaneous bursts. In Axis 3A terms, sustained-zone damage produces medium tempo via tick-rate, but individual event magnitudes are small (tick damage distributed across duration). In Axis 3B terms, the variance is flat (uniform tick magnitudes) — which is accurate but means no high-magnitude burst events.

The result: water kits cluster in the large-AOE bin (persistent_zone, aura, ground_targeted_circle) with flat-variance, medium-tempo signatures. These are mechanically valid BC coordinates but they produce kits that generate lower instantaneous DPS density than a burst mage (fire/lightning) who fires a single high-magnitude event into a single-target or small-AOE geometry.

**Recommendation for enrichment seed list:**

The water DPS density problem under Axis 2 is not a geometric gap per se (water has access to all geometry types) but a gap in **instantaneous-burst multi-spawn and chain templates** that water could plausibly express. The following instantaneous-burst templates from the seed lists above are the highest-priority candidates for water substrate expression:

1. **M-3 (N=8 full radial multi_projectile burst):** water "tidal burst" framing — single cast, 8 water bolts radiate simultaneously; high instantaneous event count; breaks the sustained-zone pattern
2. **M-8 (meteor shower / ice fragment shower):** water "hailstorm" or "ice-spear cascade" analogue; 3-5 impacts with stagger but each is high magnitude vs tick damage
3. **C-4 (control chain, 2-3 bounce):** water "frost chain" / "chill cascade"; chain delivers instantaneous CC + moderate burst damage per bounce rather than gradual DoT

All three are substrate-AGNOSTIC in generation (per Track C / substrate-as-cohesion-only commitment) — they are available in the unified mechanic pool. The cohesion-judge assigns them to water substrate post-generation when the mechanical signature matches. The enrichment recommendation is to ensure these templates exist in the pool so water-themed kits can express them when the QD-archive targets chain/multi-spawn cells for water cohesion.

**Disposition:** OQ-7 remains open as a P1 W1.11 scoping item per Track C synthesis. This dispatch surfaces the specific Axis 2 implication — instantaneous-burst multi-spawn and short-chain templates are the mechanical lever to balance water's sustained-zone DPS density deficit. Recommend folding this into W1.11 scoping note: "ensure multi-spawn (M-3, M-8) and chain (C-4) templates are accessible to water-cohesion kits."

---

## 9. Open questions resolved by this dispatch

**OQ resolved: multi-bin form types.** Three geometries sit at bin boundaries:
- `leap_strike`: small-AOE (landing impact 2-3 tiles; argmax = small-AOE)
- `cone`: small-AOE (frontal fan 2-3 tile depth; argmax = small-AOE; acknowledged wide-cone edge case for future D17 calibration)
- `aura`: large-AOE (radius 4-8 tiles; sustained radial follows caster; M-12 surfaces the multi-spawn candidate interpretation but large-AOE is the default argmax under current radius-based classification)

**OQ resolved: multi-spawn vs proxy.** totem = multi-spawn (Axis 2 territory; placed entity, no AI, no HP tracking). summon_combatant = proxy (Axis 2A territory; deferred). This dispatch does NOT seed summon_combatant templates — those are Axis 2A / P2 scope.

**OQ resolved: chain bounce-count.** Treated as distinguishable templates throughout (C-1 = 2-bounce, C-2 = 5-bounce, C-7 = 1-8 bounce, etc.).

---

## 10. Summary gap table

| Axis 2 bin | Current count | 5× target | Gap | Priority | Notes |
|---|---|---|---|---|---|
| single-target | ~12 | ~25 | ~13 | MEDIUM | 4 geometries; 12 viable kit-role combos; growth needed but functional |
| small-AOE | ~20-22 | ~25 | ~3-5 | LOW | Richest bin; 11 geometries; near-target; lowest priority for enrichment |
| large-AOE | ~18-20 | ~25 | ~5-7 | MEDIUM | 4 geometries; marginal; aura/beam_channel could use more role variation |
| chain | ~3-4 | ~25 | ~21-22 | HIGH | 2 geometries; no bounce_count param; no is_chain metadata; critically thin |
| multi-spawn | ~5-6 | ~25 | ~19-20 | HIGH | 2 geometries; no is_multi_spawn metadata; spawn-count unparameterized |

**Aggregate total: ~58-64 distinguishable templates across all 5 bins. Target: ~125. Deficit: ~61-67 (~49-52% of target).**

---

## 11. Structural metadata gaps affecting Axis 2 measurement

These gaps exist at the pre-W0.2 state and must be addressed in P1 substrate enrichment for Axis 2 BC measurement to function:

| Field | Axis 2 impact | Legolas Phase 1 reference |
|---|---|---|
| `aoe_radius` absent from Ability schema | Bin assignment via geometry name only (reliable for named types; cannot threshold-split geometries) | BC Metadata Extension Summary |
| `is_chain` absent | Chain-tagged kits require metadata for priority detection in Axis 2 measurement | BC Metadata Extension Summary |
| `is_multi_spawn` absent | Multi-spawn kits require metadata for priority detection | BC Metadata Extension Summary |
| `bounce_count` / `spawn_count` absent | Cannot distinguish 2-bounce from 5-bounce chain kits without schema field | Surfaced by this dispatch |

**Recommendation:** P1 substrate enrichment (W1.5/W1.7) should add `bounce_count` (int; applicable to chain_lightning and ricochet_bounce) and `spawn_count` (int; applicable to multi_projectile and totem) to the Ability schema alongside the three fields legolas already flagged. This makes bounce-count distinguishability computable at BC-measurement time rather than requiring inference from kit-generation parameters.

---

## 12. Cross-references

- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — Axis 2 operational spec (§ 3.2)
- `canonical/09-geometry-palette-discussion.md` — 16→26→28 geometry palette history
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/internal-substrate-state.md` — Phase 1 per-axis findings (chain/multi-spawn "thin")
- `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` — OQ-7 water DPS density (§ 3.3)
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion-only (mapping is substrate-AGNOSTIC)
- `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` — VALID_GEOMETRIES (line 231-247)
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` — archetype geometry_bias blocks
- `reincarnated-engine/src/reincarnated/generation/archetype_composer.py` — _ROLE_GEOMETRY_PREFS table
- `reincarnated-engine/config/substrate_identities/*.yaml` — substrate geometry_affinities blocks

**Downstream consumers of this deliverable:**
- P1 W1.5 — movement-skill expansion (feeds from chain + multi-spawn seed lists)
- P1 W1.7 — legolas Phase 2 depth pass (quantitative gap numbers; per-bin prioritization)
- P1 W1.11 — substrate enrichment scope (uniform-depth confirmed; OQ-7 water DPS density note)
