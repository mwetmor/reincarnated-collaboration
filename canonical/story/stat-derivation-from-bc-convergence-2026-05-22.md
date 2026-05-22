# Stat Derivation from BC Convergence — Replacement for "Traits Carry Stats"

**Date:** 2026-05-22 (evening session; canonical lock)
**Author:** gandalf (story-and-design steward; senior designer)
**Status:** v1 canonical lock — stats reframed as derived projection of substrate convergence state; "traits carry stats" framework retired
**Authority:** Matt 2026-05-22 evening — explicit canonical call (Pattern 3 of six vestigial-pattern retirements)
**Companion docs:**
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` § 3.3 (Pattern 3 detail)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` (Variant C strategic lock)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` (companion gear-substrate work)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes definitions — source for the per-axis mapping)
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` ELEMENT_SCALING_ATTRIBUTE (canonical INT/WIS/STR assignment)

---

## 0. TL;DR

Stats in Reincarnated are **not assigned via trait pools or archetype templates.** They are a **derived projection** of the kit's substrate convergence state:

```
stats(kit) = projection(element_scaling_attribute(kit.element),
                        per_axis_BC_magnitudes(kit.converged_signature))
```

The element substrate provides the **primary scaling attribute** (INT for fire/water/lightning/shadow; WIS for earth/wind/holy; STR for the excluded physical element). The 8 BC axes' measured magnitudes per kit provide the **derived secondary stat necessities** (DEX from range/mobility; CON/VIT from defensive profile; resource-scaling stat from resource economy; etc.).

**Traits become optional identity modulators v1.1+** — they may exist as cosmetic/identity flourishes (a fire kit's "Smoldering" trait, a tank kit's "Bulwark" trait) but they are **not load-bearing for stats**. The pre-W0.2 trait-stats coupling is retired.

**Why this is substrate-as-cohesion-coherent:** stats *emerge* from the kit's converged mechanical signature; they are not pre-assigned from a categorical taxonomy that selects which stats the kit gets. This is the same architectural pattern as Pattern 1 (archetype retired in favor of mechanical signature emergence) and Pattern 2 (role retired in favor of BC-axis emergence), applied to the stats layer.

**Per-BC-axis stat-necessity mapping (the canonical table):**

| BC axis | Stat necessity | Primary stat affected |
|---|---|---|
| Axis 1 range + mobility | Movement / dodge capability | DEX-equivalent |
| Axis 2 geometry | Magnitude inversion via element_scaling_attribute | (no separate stat; magnitude flows from element scaling) |
| Axis 2A proxy density | Summon-power scaling | WIS for holy / nature-aligned; INT for tech / shadow-aligned |
| Axis 2B control density | Control-duration scaling | Control-duration stat (per-element flavor) |
| Axis 3A damage tempo | Primary damage scaling | **element_scaling_attribute** (PRIMARY) |
| Axis 3B amplitude variance | Crit amplification | DEX-equivalent or LUCK |
| Axis 4 defensive profile | Survivability scaling | CON/VIT (tank); DEX (dodger) |
| Axis 5 resource economy | Resource-pool scaling | Resource-pool stat (INT for mana; STR for rage; etc.) |

**Open calibration questions** (v1.1+ revisit): relative weighting of axes for stat-magnitude; per-element variations; how dual-class hybrids resolve when two axes both demand a primary scaling attribute slot.

---

## 1. The framework — data flow from element + convergence to derived stats

### 1.1 Substrate inputs

Two substrate inputs drive stat derivation:

1. **Element substrate** — fire / water / earth / wind / lightning / holy / shadow (canonical-7 per D2). Each element has a canonical **scaling attribute** per `element_biases.py:28` ELEMENT_SCALING_ATTRIBUTE:

| Element | Scaling attribute | Identity stance (per `substrate-design-supplement-2026-05-21.md`) |
|---|---|---|
| fire | INT | combustion / volatility / burst |
| water | INT | precision / chill / tide |
| earth | WIS | mass / binding / weight |
| wind | WIS | momentum / precision / mobility |
| lightning | INT | speed / chain / branching |
| holy | WIS | judgment / blessing / sustain |
| shadow | INT | trade-off / drain / ambush |

(physical excluded from canonical-7 per D2; if reintroduced, scaling attribute = STR)

2. **Converged BC-axis magnitudes** — the 8 BC axes (per `qd-engine-bc-axes-lock-2026-05-20.md`), measured per kit *after convergence*:

- Axis 1: engagement profile (range + mobility composite)
- Axis 2: geometry (area shape + magnitude relationship)
- Axis 2A: proxy density (summons, pets, traps, ground-effects)
- Axis 2B: control density (CC frequency + duration)
- Axis 3A: damage tempo (DPS rhythm)
- Axis 3B: amplitude variance (crit vs steady-damage)
- Axis 4: defensive profile (tank / dodger / glass / sustainer)
- Axis 5: resource economy (mana / rage / stacks / cooldown-based)

### 1.2 Data flow

```
1. Kit generation runs substrate-agnostic
   ↓ (mechanical convergence loop per Discipline #1)
2. Kit cements: element substrate + skill substrate + weapon substrate fixed
   ↓
3. BC axes measured on cemented kit:
     measured_axis_magnitudes = {axis_1: value, axis_2: value, ...}
   ↓
4. Stats derived as projection:
     stats = project_to_stats(element_scaling_attribute, measured_axis_magnitudes)
   ↓
5. Stats applied to character; combat math uses derived stats
```

**No categorical assignment.** No archetype determines stats. No trait pool determines stats. No role_orientation determines stats. The kit's *measured mechanical signature* + the *element it scales by* determines stats.

### 1.3 The projection function (canonical specification)

The projection takes two inputs and outputs a stat vector:

```python
def project_to_stats(scaling_attr: ScalingAttribute,
                     axis_magnitudes: Dict[BCAxis, float]) -> Stats:
    """
    Derive stat vector from element scaling attribute + per-axis BC magnitudes.

    Returns Stats(INT, WIS, STR, DEX, CON, VIT, LUCK, CHA) where:
    - The primary scaling attribute receives the dominant magnitude (driven by
      element_scaling_attribute × Axis 3A damage tempo magnitude).
    - Secondary stats are derived per the per-axis stat-necessity mapping (§ 2).
    - Relative weights are calibrated v1.0 from heritage class targets;
      revised post-empirical (Phase 5 cohesion validation).
    """
    ...
```

The function is **declarative**, not procedural. The kit's substrate + convergence determines what stats it has; the function is a projection, not a decision tree.

**Calibration v1.0:** initial weights inherit from class-template stat distributions (the historical priority-14 stat-distribution decisions). These are *starting points* for the calibration; empirical Phase 5 cohesion-judge validation surfaces tuning needs. v1.1+ recalibration follows from Phase 5 + early B-series telemetry.

---

## 2. Per-BC-axis stat-necessity mapping (the canonical table)

This is the load-bearing detail. Each BC axis has stat necessities that the projection function honors.

### 2.1 Axis 1 — range + mobility → DEX-equivalent

**Stat necessity:** movement / dodge capability scales with the kit's engagement-profile range distance + mobility frequency.

**Why:**
- Ranged kits need to maintain distance — movement speed + dodge timing are how they survive incoming engagement
- Mobile kits (Wind Dancer, Voltaic Assassin) live or die by reposition cadence — DEX is the stat that gates this in genre canon (D&D / ARPG)
- Even melee kits with high mobility (rogue-archetype mechanical signature) need DEX for engagement timing

**Primary stat affected:** DEX-equivalent. In Reincarnated v1, this maps to whatever the canonical dexterity-equivalent stat is (`DEX` if D&D-naming retained; otherwise the engine's mobility-and-precision stat).

**Magnitude relationship:**
- High Axis 1 range value (ranged kits) + low/mid mobility → DEX moderate (precision over reposition)
- High Axis 1 range + high mobility → DEX high (kit needs both)
- Low Axis 1 range (melee) + high mobility → DEX high (rogue-pattern)
- Low Axis 1 range + low mobility → DEX low (tank-pattern; relies on Axis 4)

**Per-element variation:** wind / lightning kits naturally tilt DEX-high (their identity stance includes mobility + precision); earth kits naturally tilt DEX-low (mass stance trades mobility for power).

### 2.2 Axis 2 — geometry → magnitude inversion via element_scaling_attribute

**Stat necessity:** geometry (point / line / cone / area / chain) drives the damage-magnitude inversion (point hits hit one target hard; area hits hit many targets each less). This relationship is *already encoded* in the element scaling attribute's interaction with geometry — the engine's damage math computes per-target damage from base × geometry-modifier × element-scaling.

**Primary stat affected:** none separately. The magnitude inversion flows through the element_scaling_attribute (Axis 3A) and the engine's damage formulas; no separate "geometry stat" is needed.

**Why this is in the table even though it has no direct stat:** designers reading the audit need to know geometry is *not* a vestigial slot. It is a mechanical property that drives magnitude inversion via the damage math, not via a stat. The stats it does affect (via Axis 3A) are captured there.

### 2.3 Axis 2A — proxy density → summon-power scaling

**Stat necessity:** kits that summon (pets, minions, traps, ground-effects) need a stat that scales the *summon's* effectiveness — summon damage, summon survivability, summon count.

**Primary stat affected:** depends on element flavor:
- Holy / nature-aligned kits with summons → **WIS** (canon: cleric / druid summons scale on WIS)
- Tech / shadow-aligned kits with summons → **INT** (canon: necromancer / artificer summons scale on INT)
- Earth/wind kits with traps or ground-effects → WIS (channeled-ritual scaling)

**Magnitude relationship:**
- High Axis 2A (summon-heavy) → significant boost to the summon-power stat (WIS or INT per element)
- Low Axis 2A (no summons / minimal proxies) → no separate boost; primary scaling stat carries

**Genre canon:** Diablo II Necromancer's INT scaling for skeleton damage + summon HP; PoE Spectres scaling on minion-affix gear + INT for spell scaling. The pattern is genre-canonical and deserves direct stat-derivation support.

### 2.4 Axis 2B — control density → control-duration scaling

**Stat necessity:** kits with high CC frequency + duration need stats that scale the *duration* of their controls.

**Primary stat affected:** control-duration stat (per-element flavor):
- INT-natural elements (fire, water, lightning, shadow) → INT scales control duration
- WIS-natural elements (earth, wind, holy) → WIS scales control duration
- The control-duration scaling is *on top of* the primary scaling — kits with high Axis 2B effectively double-dip their scaling attribute for both damage and control

**Magnitude relationship:**
- High Axis 2B (controller-pattern kits) → stat allocation favors scaling attribute even more strongly (controller wants both damage and control to scale)
- Low Axis 2B → no separate boost

**Why no separate control-stat:** v1 keeps the stat list parsimonious. The control-duration scaling is multiplicative on the scaling attribute, not a separate stat. v1.1+ may introduce a separate control-duration stat if telemetry surfaces calibration friction.

### 2.5 Axis 3A — damage tempo → element_scaling_attribute (PRIMARY damage stat)

**Stat necessity:** this is the **load-bearing axis for primary damage stat allocation**. The kit's damage tempo (DPS rhythm — burst, steady, channeled, etc.) drives the dominant scaling stat magnitude.

**Primary stat affected:** **element_scaling_attribute** (INT for fire/water/lightning/shadow; WIS for earth/wind/holy; STR for physical-if-reintroduced).

**Magnitude relationship:**
- High Axis 3A damage tempo (burst / DPS-heavy kits) → scaling attribute gets dominant magnitude allocation
- Low Axis 3A damage tempo (utility / support / non-damage-primary kits) → scaling attribute still leads but with lower allocation; other stats (Axis 2A summon-scaling, Axis 4 defensive) get larger share

**The primary stat allocation rule:** the scaling attribute always wins the largest single-stat allocation; how *much* larger depends on damage-tempo magnitude. This is the canonical rule for the stat-derivation projection.

### 2.6 Axis 3B — amplitude variance → crit-amplifying stat (DEX-equivalent or LUCK)

**Stat necessity:** kits with high amplitude variance (crit-heavy, swingy, volatile) need crit-rate + crit-multiplier scaling. Steady-damage kits don't need this.

**Primary stat affected:** depends on stat-set canon:
- **DEX-equivalent** if Reincarnated maps DEX to "precision + crit" per ARPG canon (D2 Paladin/Sorceress; PoE crit nodes; Last Epoch Glancing Blow inversion)
- **LUCK** if Reincarnated introduces LUCK as a separate stat (D&D 5e; some isekai-canon)

**Magnitude relationship:**
- High Axis 3B variance (crit-burst kits) → DEX (or LUCK) gets a significant allocation
- Low Axis 3B variance (steady-DPS kits) → DEX (or LUCK) gets minimal allocation

**Open calibration question:** whether v1 carries a separate LUCK stat or folds crit into DEX. Lean: **fold into DEX for v1 simplicity**; LUCK reintroduction is v1.1+ if telemetry surfaces a need (Q-tier).

### 2.7 Axis 4 — defensive profile → CON/VIT (tank) or DEX (dodger)

**Stat necessity:** survivability scales differently depending on the kit's defensive-profile shape:
- Tank-pattern (high HP + high resist) → CON/VIT
- Dodger-pattern (low HP + high dodge) → DEX
- Glass-pattern (low HP + low dodge; high damage as compensation) → DEX low; primary scaling attribute carries
- Sustainer-pattern (mid HP + leech/regen) → CON/VIT moderate; WIS for sustain-stat flavor

**Primary stat affected:** branches per defensive-profile shape:
- Tank → CON + VIT
- Dodger → DEX
- Glass → (no separate defensive stat; primary scaling attribute carries the kit)
- Sustainer → CON + WIS

**Magnitude relationship:**
- The kit's measured Axis 4 magnitude + profile shape determines which defensive stats get allocation
- A high-Axis-4 tank-pattern kit gets significant CON/VIT
- A low-Axis-4 glass-pattern kit gets minimal defensive allocation (all eggs in damage basket)

**This is where the projection function branches the most.** The Axis 4 profile shape is what makes tank kits feel like tanks and glass kits feel like glass — not a categorical "tank class" assignment, but the *measured* defensive profile of the kit driving the stat derivation.

### 2.8 Axis 5 — resource economy → resource-pool-scaling stat

**Stat necessity:** kits with different resource economies need different resource-pool-scaling stats:
- Mana-based → INT scales mana pool
- Rage-based → STR scales rage cap
- Stack-based → no separate scaling (stacks have intrinsic caps)
- Cooldown-based → no separate scaling (cooldowns are mechanical, not stat-gated)

**Primary stat affected:** depends on resource flavor:
- Mana → INT
- Rage → STR
- Energy → DEX
- Stack/cooldown → no allocation

**Magnitude relationship:**
- High Axis 5 magnitude (resource-economy-heavy kits — fast-cycle mana-burn casters, rage-rampage barbarians) → resource-pool-scaling stat gets meaningful allocation
- Low Axis 5 magnitude → minimal allocation

**Genre canon:** D2 Sorceress scaling mana pool on Energy; D3 Barbarian fury cap scaling; PoE mana reservation auras requiring INT investment.

---

## 3. Why this is substrate-as-cohesion-coherent

### 3.1 Stats emerge; they are not pre-assigned

The architectural principle substrate-as-cohesion commits to: **identity emerges from substrate via convergence; it is not pre-imposed.**

Pre-W0.2, stats were pre-imposed via:
- Class template → primary stat allocation
- Trait pool (per class) → secondary stat allocation
- Gear affix → tertiary stat allocation

The pre-imposition was at the class-template layer. Stats came from "what class is this" + "which traits did you pick" + "what gear are you wearing."

Post-W0.2 substrate-as-cohesion, the architectural commitment is:
- Element substrate enters generation as primitive
- Skill substrate + weapon substrate enter generation as primitives
- Kit converges to a mechanical signature
- Stats are derived projection of (element_scaling_attribute × per-axis BC magnitudes)

There is no class template. There is no archetype. There is no role assignment. The kit's *measured signature* + the element it scales by determines stats. **Stats are downstream of convergence, not upstream.**

This is structurally identical to:
- Pattern 1: mechanical signature emerges from convergence (not archetype assignment)
- Pattern 2: role flavor emerges from BC axes (not role_orientation assignment)
- Pattern 5: gear emerges from substrate-vector queries against the library (not 15-entry enumeration)

The pattern is consistent. Stats join the family.

### 3.2 The derivation is deterministic + reproducible

The projection function takes substrate inputs and produces stats deterministically. Given the same substrate, the same stats. This is desirable:
- Reproducibility: a given kit's stats are computable from its substrate; no hidden state in trait selections
- Debuggability: stat anomalies trace to substrate or projection-function bugs, not to trait-pool tuning
- Telemetry clarity: stats can be attributed to substrate dimensions, not to opaque class-template tables

### 3.3 The derivation respects element identity

The element scaling attribute is **the primary load-bearing slot**. A fire kit always has INT as its largest stat. A holy kit always has WIS as its largest. This is identity preservation: the element you are determines how you scale, period.

Cross-attribute kits (a fire kit that is somehow STR-dominant, an earth kit that is somehow DEX-dominant) become *anomalies* under this framing — they exist when the convergence produces a signature that the projection function's calibration handles edge-case-ily. The framework supports them (because the projection function is a pure projection from substrate, not a categorical lookup) but they should be statistically rare in v1. v1.1+ can introduce intentional cross-attribute archetypes via trait modulators (§ 4 below).

### 3.4 Comparison to ARPG canon

**Diablo II:** stats are pre-allocated via class choice; player allocates stat points per level. Stat derivation is *fully manual*; the class only sets starting stats and growth rates. Identity is in the class + skill tree, not the stats.

**Diablo III / IV:** stats are auto-allocated per class; player has no stat-allocation agency. Stat derivation is *fully automatic from class*. Identity is in the class + skill choice; stats follow.

**Path of Exile:** stats come from the passive tree + gear; player has full stat-allocation agency via tree choices. Stat derivation is *emergent from passive choices*. Identity is in build composition (tree + gem links + gear); stats follow.

**Last Epoch:** stats come from class + masteries + skill trees + gear. Stat derivation is *layered*; identity is in the layer cake.

**Reincarnated v1 under this framework:** stats come from **element substrate + mechanical convergence**. No player stat allocation; no skill-tree-derived stat allocation; no class-template stat allocation. Stats are a pure projection of "what element are you" + "what is your converged mechanical signature."

This is **closer to PoE than D3** in spirit (emergent from build) but **simpler than PoE** in surface (no manual stat allocation; no passive tree to navigate). The player's expressive surface is the spirit-swap mechanic (per Reincarnated overlay) + the build-as-it-emerges via gear and skill choice; the stats are a consequence, not an input.

---

## 4. What this means for trait architecture

### 4.1 Traits demoted to optional identity modulators (v1.1+)

The pre-W0.2 trait architecture (per `project_trait_architecture.md` 2026-05-12) treated traits as the load-bearing surface for stats:
- B9a per-class intrinsic trait pool (5-10 traits, floors at L1/12/25/38, converge at L50)
- D9 gear-affix rolls (element/mechanic-gated, no skill-specific on gear)
- Rank-stacking across sources; gear tier sets per-rank rate, player level sets cap
- Experimental classes don't roll trait affixes

Under the new stat-derivation framework, this entire architecture is **vestigial for stat-derivation purposes** (Pattern 3 retirement). Traits don't *carry* stats; stats are derived from substrate convergence.

But traits don't have to disappear. They can be **demoted to optional identity modulators v1.1+**.

### 4.2 What traits could become

Traits as **identity flourishes** that add flavor without carrying mechanical load:
- A fire kit might have the "Smoldering" trait — cosmetic burn-aftershock VFX; no stat impact
- A tank kit might have the "Bulwark" trait — cosmetic defensive flourish + small VFX accent
- A controller kit might have the "Web-Weaver" trait — cosmetic web-style control VFX

These would be **post-convergence identity modulators**, not generation inputs. They land in v1.1+ if Matt wants them. v1 ships without traits as a load-bearing surface.

Alternative v1.1+ direction: traits as **passive bonus modulators** that don't change primary stats but tweak edge-case behaviors:
- Trait "Quickfooted" → +5% movement speed (doesn't change DEX; small movement bonus)
- Trait "Steady Hand" → -5% crit variance (doesn't change DEX; small crit-amplitude smoothing)
- Trait "Patience" → +10% mana regen during channel (doesn't change INT; small resource bonus)

These would be **identity expression at the margins**, not core mechanical load. They give players a way to express small build preferences without re-imposing the categorical-trait-pool framework.

### 4.3 Gear affixes still allowed (with caveat)

Gear affixes (per `d9-gear-affix-design-phase-1-p1.md`) can still roll **stat affixes** — gear-derived marginal stat variation. The caveat: **base stats come from BC-axis derivation, not trait sum.** Gear affixes provide *variation around the derived base*, not the base itself.

The math:
```
total_stats(kit, gear) = derived_stats(kit) + gear_affix_stats(gear)
                       ↑ load-bearing            ↑ marginal variation
```

Gear-derived stat variation gives players a meaningful loot reward (Quick gloves give +DEX, etc.) without making gear *the* source of stats. The kit's identity is in its substrate; gear is the marginal variation layer.

### 4.4 Existing trait docs: status

| Doc | Status under stat-derivation framework |
|---|---|
| `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` | Mark as v1.1+ optional-identity-modulator design; not load-bearing for v1 stats |
| `canonical/story/d8-trait-floor-design-phase-1-p1.md` | Same |
| `canonical/story/d9-gear-affix-design-phase-1-p1.md` | Audit: gear affixes can still roll stat affixes; base stats come from BC-axis derivation |
| `memory/project_trait_architecture.md` | Mark legacy / borderline vestigial under BC-axis-derived stats framework (per audit doc § 3.3) |
| `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` | Audit for trait-stats coupling; flag for revision under stat-derivation framework |

---

## 5. Open calibration questions

These are questions the v1 calibration pass surfaces; v1.1+ revisits with empirical data.

### 5.1 Relative weighting of axes for stat-magnitude

**Question:** how much weight does each BC axis contribute to each stat?

For example, a kit with high Axis 3A damage tempo and moderate Axis 2A proxy density and low Axis 4 defensive profile — what are the relative stat magnitudes?

**v1.0 starting point:** inherit from historical class-template stat distributions. The Stormcaller-pattern (lightning + ranged + controller mechanical signature) historically had stat distribution ~INT 14 / WIS 8 / STR 6 / DEX 10 / CON 8 / VIT 6 / LUCK 4 — extract weights from these patterns and use as calibration prior.

**v1.1+ revisit:** Phase 5 cohesion-judge empirical validation may surface tuning needs. If a derived kit feels mechanically right but stat-distribution-wrong (e.g., a "Stormcaller" kit comes out with DEX > INT despite lightning-INT scaling), the projection function weights need adjustment.

### 5.2 Per-element variations

**Question:** do per-element variations exist beyond the scaling attribute? Should a holy kit's defensive profile derive CON/VIT more strongly than a shadow kit's same defensive profile?

**v1.0 starting point:** no per-element variation beyond scaling attribute. The projection function uses element only to determine scaling attribute; secondary stat derivation is element-agnostic.

**v1.1+ revisit:** if telemetry surfaces that per-element variations meaningfully improve identity recognition, introduce element-flavor multipliers on secondary derivations. Lean: stay element-agnostic on secondaries for v1; revisit if Phase 5 surfaces need.

### 5.3 Dual-class hybrids — when two axes both demand primary scaling

**Question:** what happens when a kit has both very high Axis 3A damage tempo AND very high Axis 2A proxy density? Both want to be primary scaling targets. How does the projection function resolve?

**v1.0 starting point:** the element scaling attribute ALWAYS wins the largest single-stat allocation. Per-axis secondary derivations contribute to *secondary* stats; the primary slot is always element-determined. If a kit has high Axis 2A and high Axis 3A, both contribute to the scaling attribute's allocation (multiplicatively), not to a competing slot.

**v1.1+ revisit:** if Phase 5 surfaces that summoner kits with dominant proxy density feel mechanically wrong with INT/WIS allocation rules, introduce summoner-flavor modulators. Lean: keep the canonical rule (element scaling attribute always wins primary slot) for v1 simplicity.

### 5.4 Stat caps + level scaling

**Question:** the projection function outputs stat magnitudes; how do these scale with level? Are there caps?

**v1.0 starting point:** stats scale linearly with level via per-level stat growth (canonical D&D/ARPG pattern). Caps follow class-template historical caps (level 50 cap; stat caps ~30-40 per attribute).

**v1.1+ revisit:** if BC-axis-derived stat magnitudes don't fit the historical caps cleanly, recalibrate caps. Lean: tune caps to fit the projection, not vice versa — the projection is the canonical source.

### 5.5 Player agency in stat allocation

**Question:** does the player have any agency over stat allocation? Or is it fully derived?

**v1.0 starting point:** fully derived. No manual stat allocation; no skill-tree stat allocation. This matches Diablo III/IV style (no agency) rather than D2/PoE style (full agency).

**v1.1+ revisit:** if playtesting surfaces that fully-automatic stat allocation feels disempowering, introduce a small margin of player agency (e.g., 1-2 stat points per level the player allocates manually). Lean: hold fully-derived for v1; the player's expressive surface is the spirit-swap mechanic + gear choices + skill selection, not stats. Stats are downstream of substrate.

### 5.6 LUCK as separate stat vs folded into DEX

**Question:** does the canonical stat list include LUCK as a separate stat, or fold crit/luck mechanics into DEX?

**v1.0 starting point:** **fold into DEX for v1 simplicity.** Crit rate + crit multiplier scale on DEX; no separate LUCK stat. Matches Last Epoch / Grim Dawn convention.

**v1.1+ revisit:** if telemetry surfaces a need for separate LUCK (e.g., loot-luck mechanics, rare-affix-roll modifiers), introduce LUCK. Lean: hold off for v1.

### 5.7 CHA / utility stats

**Question:** do CHA or utility stats (Persuasion, Crafting) belong in the canonical stat list?

**v1.0 starting point:** no. Reincarnated v1 is ARPG-shaped (combat-centric); CHA / crafting / utility stats don't appear. Stat list = INT / WIS / STR / DEX / CON / VIT (+ LUCK if separated per § 5.6).

**v1.1+ revisit:** if non-combat surfaces (Earth Self meta-layer crafting; spirit-form library curation) deepen, introduce utility stats then.

---

## 6. Cross-references

### 6.1 This session's canonical foundations
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` § 3.3 — Pattern 3 vestigial-pattern detail (companion explanation)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock (parent doc)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — gear-substrate companion (Patterns 4-5-6)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — operationalizes substrate work

### 6.2 BC axes + element foundations
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes canonical definitions
- `canonical/story/substrate-design-supplement-2026-05-21.md` — per-element identity-stance definitions
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE canonical INT/WIS/STR assignment
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω/τ tables (recalibration pending under stat-derivation framework)

### 6.3 Trait architecture (now demoted to v1.1+ optional)
- `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` — v1.1+ optional-identity-modulator design
- `canonical/story/d8-trait-floor-design-phase-1-p1.md` — same
- `canonical/story/d9-gear-affix-design-phase-1-p1.md` — gear affixes can still roll stat affixes as marginal variation
- `memory/project_trait_architecture.md` — legacy / borderline vestigial (Matt manual update per audit § 6.3)

### 6.4 Progression docs (audit pending)
- `canonical/32-progression-design.md` — audit for trait-stats coupling references
- `canonical/33-progression-skeleton.md` — same

### 6.5 Discipline + governance
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 1 (math-before-code applies to projection function calibration); § 11 (empirical inspection before lock)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — pending entry for stat-derivation canonical lock

---

## 7. Closing — what this delivers

The stat-derivation framework completes the architectural triangle that substrate-as-cohesion needs:

1. **Mechanical signature emerges from convergence** (Pattern 1 retirement — archetype out)
2. **Role flavor emerges from BC axes** (Pattern 2 retirement — role_orientation out)
3. **Stats emerge from element substrate + BC convergence** (Pattern 3 retirement — traits-carry-stats out)

These three retirements are *the same retirement applied to different layers*: identity-determining surfaces that were pre-imposed under the old categorical pipeline become derived-from-substrate under substrate-as-cohesion.

Without stat-derivation completion, the trait-stats coupling would have been a vestigial back-door — the engine could claim substrate-as-cohesion architecturally while still pre-imposing identity via the trait pool that carries the stats. The audit caught this; the framework above replaces it.

What remains for v1 implementation:
- **Calibrate the projection function** (§ 5.1) — initial weights from heritage class-template patterns
- **Build the projection in code** — replace trait-stats application paths with substrate-derivation paths (per audit § 3.3 cleanup checklist)
- **Update telemetry attribution** — stat attribution becomes "derived from substrate," not "from trait X"
- **Audit existing docs** (§ 4.4) for trait-stats coupling references
- **Phase 5 empirical validation** — does the derived stat allocation feel right to cohesion-judge and to playtest?

What's deferred to v1.1+:
- Traits as optional identity modulators (§ 4.2)
- Per-element secondary stat variations (§ 5.2)
- Player agency in stat allocation (§ 5.5)
- LUCK as separate stat (§ 5.6)
- Utility stats (§ 5.7)

The framework is canonical; the implementation lands in P1 work; the calibration tightens through Phase 5; the v1.1+ optional layers come in once v1 ships and telemetry surfaces what they need to look like.

---

**Signed:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-22 evening — Pattern 3 vestigial retirement canonical call
**For:** canonical replacement for "traits carry stats" framework; per-BC-axis stat-necessity mapping locked; trait architecture demoted to v1.1+ optional identity modulators; calibration questions queued for Phase 5 empirical surfacing.
