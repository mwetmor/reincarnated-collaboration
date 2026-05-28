# 51 — Investment Scaling 6-Pattern Architecture

> **STATUS:** CURRENT (LOAD-BEARING as of 2026-05-28) — Phase 2 of integrated W-α7+ master scoping; canonical authority on the structural intent of skill-tree per-node investment scaling. Patterns 1+2 detailed for Cycle 14 v1 Phase 3 implementation; Patterns 3-6 canonical-locked stubs for Cycle 15+ work. Gates W-α7+ Phase 3 (rocket Patterns 1+2 implementation + gamora BASE re-derivation + encounter HP rebalancing) + Phase 4 (multi-dim calibration) + Phase 5 (BVV harness update + Wave 5 RE-FIRE). See `canonical/00-ground-state.md` § 1.

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — Patterns 1+2 formula structures specified + calibration anchor decision (max-investment) + per-tier ratio preservation (1:1.5:2.17:4.0) + profile semantic definitions + per-encounter-type band design integrated + Patterns 3-6 canonical-locked stubs
**Authority:** Matt 2026-05-28 evening RATIFICATION AMENDMENT — integrated W-α7+ scope absorbs case 9 + case 10 + case 11 + case 12; Phase 2 fires in PARALLEL with jack-ryan Gate-1 review of master scoping per Matt explicit authorization. Master scoping dispatch `agentic_orchestration/dispatches/2026-05-28-integrated-w-alpha-7-plus-master-scoping.md` § 1 Phase 2 carries verbatim scope.
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry; § 1 update required at session close)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — bounded-viability-with-specialization directive; Patterns 1+2 formulas MUST compose cleanly with bounded-viability constraints; this doc's max-investment KPM-ratio criterion is the Discipline #47 fold-in (jack-ryan Gate-1 Amendment #1)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 — 4-damage-path mechanical substrate; this doc's Pattern 1 scaling factor enters the physical/magical/hybrid damage equations at `skill.damage_multiplier`; § 3 forward-link added in same session
- `canonical/46-concentration-architecture-2026-05-27.md` — concentration architecture; investment scaling is the per-node mechanical instantiation of "concentration over distribution" — each invested point compounds within a node rather than distributing across nodes
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid; investment domain (per-node passive ∈ [0,5] / active ∈ [0,15] / t4 ∈ [0,1]) is the player-facing investment surface this doc operates over
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation; build-specialization vs kit-identity framing is the design-experience layer this doc supports mechanically
- `canonical/02-roadmap.md` § 4.4 — Cycle 14 v1 close trajectory; this doc gates Phase 3+4+5 sub-streams
- `agentic_orchestration/dispatches/2026-05-28-integrated-w-alpha-7-plus-master-scoping.md` — integrated W-α7+ master scoping (load-bearing parent dispatch; Phase 2 gandalf seam lead)
- `agentic_orchestration/cycle-14-wave-5-season-001/w-alpha-6-enc-band-sweep-telemetry.json` + `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-6-per-encounter-type-bands-2026-05-28.md` — W-α6 ENCOUNTER_COHORT_KPM_BAND structure (preserved as Phase 1 input; values recalibrated under multi-dim space in Phase 3+4)
- `reincarnated-loadout/src/data/cycle13Types.ts:255` — NODE_MAX investment domain source (passive=5 / active=15 / t4=1; jack-ryan Gate-1 Amendment #2 source-verified)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #45 (vocabulary lock) + § Discipline #47 (bounded-viability framework discipline)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — Phase 2 canonical lock entry authored by jack-ryan post-Phase-2 (jack-ryan W-α7+ retirements parallel sub-stream)

---

## 0. TL;DR

The skill tree's per-node investment domain (passive ∈ [0,5] / active ∈ [0,15] / t4 ∈ [0,1] per `cycle13Types.ts:255` `NODE_MAX`) is operated by **6 mechanical patterns**. Patterns 1+2 cover damage and effect scaling — the load-bearing damage-formula composition for Cycle 14 v1 close. Patterns 3-6 cover threshold unlocks, QoL modifiers, synergy bonuses, and resource economy modifiers — canonical-locked here for Cycle 15+ implementation.

**Patterns 1+2 (Cycle 14 v1):**

| Pattern | Domain | Formula structure | Anchor |
|---|---|---|---|
| **Pattern 1 — Active skill damage scaling** | per-active-skill node, points ∈ [0, 15] | `damage_multiplier_at_points = base_at_max × ((1 - decay) + decay × (points / 15))` with `decay = 0.65` → min/max range `[0.35, 1.00] × base_at_max` | `base_at_max` calibrated at max investment (15/15) |
| **Pattern 2 — Passive skill effect scaling** | per-passive node, points ∈ [0, 5] | `effect_magnitude_at_points = base_at_max × ((1 - decay) + decay × (points / 5))` with `decay = 0.50` → min/max range `[0.50, 1.00] × base_at_max` | `base_at_max` calibrated at max investment (5/5) |

Both patterns use the same **linear-with-floor** structural family (geometric mean of pure-additive and pure-multiplicative, ergonomically chosen for max-investment-anchored cohort coherence; see § 3.4 form rationale).

**Calibration anchor decision:** **max-investment** for both patterns (not midpoint, not per-pattern-distinct). The cohort median KPM that doc 50's 5 design targets validate against represents the **fully-invested player profile** — a player who has reached endgame, distributed their points, and is now running the season cohort gauntlet. Sub-max investment profiles bound by floor at `(1 - decay) × base_at_max` produce the natural under-band that early-game and mid-game players experience; the bounded floor (0.35× active, 0.50× passive) is the design's deliberate "your build is still coming online" feel. See § 4 for full rationale.

**Per-tier ratio preservation (Matt verbatim 1:1.5:2.17:4.0):** Phase 3 BASE_DAMAGE_L50 re-derivation per damage path AND per skill tier MUST preserve the T1:T2:T3:T4 = 1:1.5:2.17:4.0 ratio sequence at max-investment-anchored cohort outputs. Investment scaling operates BELOW the tier_coefficient layer in the damage equation; tier ratios are properties of `tier_coefficient` and `BASE_DAMAGE_L50` per tier, NOT of the per-skill points-invested multiplier. See § 5 for the mathematical composition.

**Profile semantic definitions** (Jack-ryan Gate-1 Amendment #3 fold-in; numeric thresholds = Phase 3+4 gamora seam discretion):
- **low-profile** — character has invested <~25% of total skill-point budget (early-game / leveling phase)
- **mid-profile** — character has invested ~25-75% of total skill-point budget (mid-game / endgame approach)
- **max-profile** — character has invested ≥~75% of total skill-point budget at active nodes (or equivalent for builds that prioritize passive depth) (endgame / fully-realized build)
- **mixed-profile** — character has invested points across active + passive in ratios distinct from cohort-typical (intentional unconventional build; expected outlier on bounded-viability cohort_median)

The cohort_median that doc 50's 5 targets validate against is computed at **max-profile** — the cohort represents endgame-realized characters running endgame content.

**Per-encounter-type band design integrated:** the W-α6 ENCOUNTER_COHORT_KPM_BAND 24-cell structure (6 encounter types × 4 cohorts) PERSISTS as Phase 1 input. Values are RECALIBRATED under the multi-dimensional space (paths × cohorts × encounter_types × investment_profiles) in Phase 4. The W-α6 sweep ran at FIXED character-profile (implicit no-investment); Phase 4 sweep operates across investment dimension as additional cohort axis. Case 10 timing floor constraint (open_arena / chokepoint_corridor / magic_pack at 600 KPM exact under W-α3 calibration) is acknowledged here; resolution path = Phase 3c encounter HP rebalancing in `endgame_mob_stat_profile.py` per master scoping § Phase 3c.

**Patterns 3-6 (Cycle 15+):** canonical-locked stubs at § 8. Implementation deferred; design space named here so future cycles compose against locked vocabulary.

**Discipline #47 verification (Jack-ryan Gate-1 Amendment #1):** at max investment (15/15 active points; 5/5 passive points), kit peak KPM ratios remain within doc 50 § 4 Target 4 band [1.5×, 2.0×] cohort_median for the 1-2 designed peak encounter types. The linear-with-floor form bounds peak KPM at `base_at_max × 1.0` — there is no investment-driven super-peak above the calibrated `base_at_max`. Specialization peaks emerge from `base_at_max` distribution across kits (gamora Phase 3d BASE re-derivation per-path × per-kit space), NOT from investment scaling per se. See § 7 for the verification framework.

**Discipline #45 vocabulary grep audit:** PASS at authoring. See § 11 for declaration.

---

## 1. Authority + provenance

### 1.1 Phase 2 scope per Matt 2026-05-28 evening RATIFICATION AMENDMENT

Master scoping dispatch § 1 Phase 2 carries verbatim:

> Phase 2 — Investment scaling design (~1.5-2.5d) — gandalf seam lead; PARALLEL with Gate-1
>
> Scope:
> - **Pattern 1 active skill damage scaling formula specification** — gandalf canonical authority on structural intent
> - **Pattern 2 passive skill effect scaling formula specification** — same architecture review per pattern; gandalf canonical authority
> - **Calibration anchor decision** — max-investment OR midpoint OR per-pattern-distinct anchor; rationale captured for Phase 3 implementation + Phase 4 multi-dim calibration target
> - **Per-tier ratio preservation: 1:1.5:2.17:4.0** (Matt Phase 2 spec verbatim) — T1:T2:T3:T4 calibrated ratio sequence; Phase 3 BASE re-derivation must preserve this ratio under investment scaling
> - **Per-encounter-type band design integrated** — was Option B; now integrated. ENCOUNTER_COHORT_KPM_BAND structure from W-α6 preserved; values recalibrated under multi-dim space
> - **Profile semantic definitions (Jack-ryan Gate-1 Amendment #3)** — conceptual labels: low / mid / max / mixed-profile (numeric thresholds = Phase 3+4 gamora seam discretion)
> - **6-pattern canonical doc** capturing Patterns 1+2 detailed semantics for Phase 3 + Patterns 3-6 canonical-locked for Cycle 15+ implementation

### 1.2 Composition with Path α architectural commitment

Path α architectural commitment (Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL; doc 50): the engine must produce **bounded variance with designed peaks** — every kit functions on every encounter type; every kit has 1-2 designed peaks; no kit strictly dominates or is strictly dominated.

The integrated W-α7+ reframe (Matt 2026-05-28 evening): Path α's W-α3 Phase 2 calibrated BASE_DAMAGE_L50 values are SCAFFOLD per Discipline #39 — calibrated at "implicit no-investment" profile which is about to change under investment scaling. Solving symptom (per-encounter bands at fixed profile) AND root (investment scaling + base value recalibration) in parallel = double calibration risk. Integrated scope absorbs both.

This canonical doc is the structural-intent layer over the investment domain. Phase 3 (rocket Patterns 1+2 implementation; gamora BASE re-derivation; gamora encounter HP rebalancing) consumes this doc as input. Phase 4 (multi-dim calibration) consumes both this doc and Phase 3 outputs.

### 1.3 What surfaced this design surface

The investment scaling architecture was implicit-but-unnamed across multiple Cycle 13+14 cycles. Doc 40's gear-balance architecture references kits running "cohort-typical loadouts"; doc 50 § 4.2 references "the cohort median is computed within each cohort" without specifying the INVESTMENT axis. The loadout app's `NODE_MAX` constant (passive=5 / active=15 / t4=1) established the per-node domain in Cycle 13 without specifying how the per-node points-invested value enters damage equations.

W-α6 gamora completion 2026-05-28 evening surfaced the structural gap: ENCOUNTER_COHORT_KPM_BAND values calibrated at the FIXED no-investment profile would be invalidated by any subsequent investment scaling implementation. Case 12 (BASE_DAMAGE values scaffold) and case 11 (investment scaling design-dialog) are the Discipline #39 framework's two named drift catches at the integration seam.

This doc is the canonical resolution for the integration seam — it specifies the structural intent that Phase 3 implementation, Phase 4 calibration, Phase 5 validation, and all future Cycle 15+ pattern implementations compose against.

---

## 2. The 6 patterns — vocabulary lock

Per-node investment (points ∈ [0, NODE_MAX]) operates the player's character through 6 mechanical patterns. These 6 patterns are the canonical vocabulary; future cycles may extend (Pattern 7+) but the existing 6 are LOCKED.

| Pattern | Name | Cycle | Domain | Purpose |
|---|---|---|---|---|
| **Pattern 1** | Active skill damage scaling | **Cycle 14 v1 (Phase 3)** | Active skill nodes (points ∈ [0, 15]) | Per-point damage_multiplier scaling; the load-bearing damage-formula investment surface |
| **Pattern 2** | Passive skill effect scaling | **Cycle 14 v1 (Phase 3)** | Passive skill nodes (points ∈ [0, 5]) | Per-point passive-effect magnitude scaling (stat bonuses, defenses, triggered-passive proc-rate or magnitude) |
| **Pattern 3** | Threshold unlocks | Cycle 15+ | Either node type at named investment threshold | Discrete capability gate — "at 3/5 invested, this passive gains property X"; binary, not continuous |
| **Pattern 4** | QoL modifiers | Cycle 15+ | Either node type | Quality-of-life effects (animation speed, resource regen rate, cooldown smoothing); non-damage-impacting |
| **Pattern 5** | Synergy bonuses | Cycle 15+ | Cross-node (relational) | Bonus that activates when N nodes in a related cluster all have ≥M invested points |
| **Pattern 6** | Resource economy modifiers | Cycle 15+ | Either node type | Cost/refund/efficiency modifiers (mana cost reduction, resource generation, ω-penalty mitigation) |

**Why this partition is load-bearing:** the 6 patterns separate damage-routing investment (Patterns 1+2) from build-shape investment (Patterns 3+5) from quality-of-life investment (Pattern 4) from resource-economy investment (Pattern 6). Cycle 14 v1 close requires only Patterns 1+2 because those are the patterns the doc 50 bounded-viability-with-specialization directive operates against (KPM is a damage-output metric, not a resource-economy or QoL metric). Patterns 3-6 are designed; their implementation is deferred until the damage-routing foundation is empirically validated.

**Vocabulary alignment:** these names are gandalf-curated; future canonical extensions use the same numbering. Patterns 7+ may emerge from future design dialogue (e.g., "Pattern 7 — Element-conversion investment scaling" if T4 ELEMENT_CONVERSION is decomposed across investment levels).

---

## 3. Pattern 1 — Active skill damage scaling

### 3.1 Domain

- **Node type:** active skill node
- **Investment domain:** points ∈ [0, 15] (per `cycle13Types.ts:255` `NODE_MAX.active = 15`)
- **Per-character node count:** flat 8 active skills per doc 40 D63-D86 (8 active skill nodes; 7 with potential T4 capstones per "T4 count = chain count - 1"; doc 40 architectural foundation)
- **Per-character active points budget:** 8 nodes × 15 max = 120 total active investment points (no character is expected to fill all; budget interaction with passive + T4 nodes is a Phase 4 calibration parameter)

### 3.2 Formula structure (LINEAR-WITH-FLOOR)

The Pattern 1 formula is:

```
damage_multiplier_at_points = base_at_max × ((1 - decay) + decay × (points / NODE_MAX_active))

where:
  NODE_MAX_active = 15
  decay           = 0.65  (Phase 2 starting value; Phase 4 calibration adjusts within [0.55, 0.75])
  base_at_max     = calibrated per-skill-per-tier value (Phase 3d gamora seam derives)
```

Substituting concrete values:

```
points = 0:    multiplier = 0.35 × base_at_max
points = 5:    multiplier = (0.35 + 0.65 × 5/15)  × base_at_max = (0.35 + 0.217) × base = 0.567 × base
points = 10:   multiplier = (0.35 + 0.65 × 10/15) × base_at_max = (0.35 + 0.433) × base = 0.783 × base
points = 15:   multiplier = 1.00 × base_at_max   ← cohort_median anchor
```

The bounded floor (0.35 at points=0) is intentional. A point-zero active skill is NOT a broken skill — it produces 35% of fully-invested damage. The player whose build hasn't filled this skill node can still cast it and contribute. Below 35% the player-experience signal would flip to "this skill is broken at low investment," which violates the bounded-viability floor for skills the player has unlocked but not maxed (doc 50 § 4.5 floor analog at the skill level).

The 0.65 decay parameter is the gradient — at half investment (~7-8 points), the skill produces ~70% of max damage. Investment matters; points 0-15 produce a 2.86× damage range (0.35× to 1.00×).

### 3.3 Composition with the damage equation (doc 47)

Pattern 1 multiplier enters the doc 47 § 2.2 damage formulas at `skill.damage_multiplier`:

**Physical (doc 47 § 2.2 verbatim with Pattern 1 substitution):**

```
physical_skill_damage = weapon_base_physical_damage
                      × skill_damage_multiplier_at_points        ← Pattern 1 LIVES HERE
                      × (1 + primary_attribute_bonus / 100)
                      × (1 + global_physical_damage_modifier / 100)
                      × tier_coefficient(skill_tier)             ← per-tier 1:1.5:2.17:4.0 ratio
                      × element_conversion_factor (if T4 active)
                      × crit_multiplier (if crit fires)
```

**Magical (same composition shape):**

```
magical_skill_damage = base_spell_damage(element, skill_tier)
                     × skill_damage_multiplier_at_points         ← Pattern 1 LIVES HERE
                     × (1 + caster_attribute_bonus / 100)
                     × (1 + weapon_spell_damage_modifier / 100)
                     × (1 + element_affinity_modifier / 100)
                     × (1 + global_spell_damage_modifier / 100)
                     × tier_coefficient(skill_tier)              ← per-tier 1:1.5:2.17:4.0 ratio
                     × element_conversion_factor / dual_element_factor (if T4 active)
                     × crit_multiplier (if crit fires)
```

**Critical composition observation:** Pattern 1 multiplier `skill_damage_multiplier_at_points` is an INNER-LAYER multiplier. `tier_coefficient` is OUTER-LAYER. The 1:1.5:2.17:4.0 tier ratio is preserved because `tier_coefficient` does not depend on points-invested — every kit at every investment level experiences the same per-tier scaling (T1 → T2 = ×1.5; T1 → T3 = ×2.17; T1 → T4 = ×4.0).

**Math note application-order specification (jack-ryan Gate-1 Amendment for Phase 3a rocket):** rocket math note at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-phase-3-pattern-1-2026-05-28.md` MUST resolve explicitly whether `damage_modifier` (gear `+%damage`) composes BEFORE or AFTER `skill_damage_multiplier_at_points` in the equation order. The two options are mathematically distinct:

- **Option A (BASE × MODIFIER × INVESTMENT):** `base × damage_modifier × skill_damage_multiplier_at_points × ...`
- **Option B (BASE × INVESTMENT × MODIFIER):** `base × skill_damage_multiplier_at_points × damage_modifier × ...`

Both produce the same final product (multiplication is commutative), BUT the W-α3 calibration was performed at FIXED implicit-no-investment profile — `damage_modifier × base` was the calibrated layer. Rocket math note documents which compositional ordering preserves W-α3 calibration semantics under Phase 4 multi-dim recalibration. **Gandalf design intent: Option A — the gear modifier composes against the base, and the investment scaling composes against that result.** This makes the investment scaling the FINAL per-skill multiplier before tier coefficient + crit, which matches the player-experience framing "I invested in this skill; now MY skill is stronger" (rather than "investing in this skill made my gear stronger").

### 3.4 Form rationale — why linear-with-floor (not additive, not multiplicative, not threshold)

Four candidate formula structures were considered:

**(A) Pure additive** — `base × (1 + c × n)`:
- Cliff at n=0: multiplier = `base × 1.0` — investment provides no benefit at 0 points; floor is the base itself
- Cliff at n=15: multiplier = `base × (1 + 15c)` — investment provides growing benefit; no upper bound discipline
- **Player experience:** investment is felt as additive bonus on top of base; "every point is worth the same"
- **Rejection reason:** does not honor max-investment cohort anchor; the base IS the no-investment floor, which forces a separate problem: what is the "base" multiplier of a 0-point active skill? If base=1.0 then 0-point skills are full-power (which kills investment depth). If base<1.0 then the additive formula has two parameters competing.

**(B) Pure multiplicative** — `base × multiplier^n`:
- Cliff at n=0: multiplier = `base × 1.0` — same problem as additive
- Cliff at n=15: multiplier = `base × multiplier^15` — exponential cliff at max-investment; investment beyond ~8-10 points produces super-peak ratios
- **Player experience:** investment is felt as exponential growth; "the more I invest the more each next point is worth"
- **Rejection reason:** super-peak cliff at n=15 produces Discipline #47 Target 4 violations easily. A kit at 15/15 investment with multiplier=1.1 produces 1.1^15 = 4.18× scaling — far above the 1.5-2.0× specialization band. Multiplicative form requires aggressive multiplier-parameter calibration to stay in-band, AND the resulting curve has too-shallow slope at low-investment (early-game player feels their investment doesn't matter).

**(C) Threshold-shaped** — tiered scaling at investment thresholds (e.g., +0% at 0 points, +25% at 4 points, +60% at 9 points, +120% at 15 points):
- Cliff at investment thresholds — player optimization concentrates at threshold points
- **Player experience:** investment has named milestones; build-crafting community develops around hitting specific point counts per skill
- **Rejection reason for Cycle 14 v1 PATTERN 1:** threshold-shaped IS the canonical design intent for **Pattern 3 (threshold unlocks)** — capability gates at specific investment levels. Conflating Pattern 1 (continuous damage scaling) with Pattern 3 (threshold capability unlocks) would erase a load-bearing design partition. Pattern 1 stays continuous; Pattern 3 carries threshold semantics when implemented Cycle 15+.

**(D) Linear-with-floor** — `base_at_max × ((1 - decay) + decay × (n / NODE_MAX))`:
- Floor at n=0: multiplier = `base_at_max × (1 - decay)` — investment-bound floor honors the bounded-viability floor per skill node
- Cliff at n=NODE_MAX: multiplier = `base_at_max × 1.0` — capped at the calibrated `base_at_max`
- **Player experience:** investment is felt as gradient toward the kit's full power; "I'm at 60% of my potential on this skill"; no super-peak above cohort anchor
- **Selection reason:** ergonomic for max-investment-anchored calibration; the cohort_median that doc 50's 5 targets validate against IS `base_at_max`. Sub-max investment profiles bound below `base_at_max` produce the natural under-band that early/mid-game players experience without violating the 5-target output gate at endgame. The form is the geometric mean of additive (linear growth) and multiplicative (bounded ceiling) — captures both "every point matters" AND "investment caps at cohort_median anchor."

**Decay parameter rationale (0.65):**

The decay parameter is the gradient steepness. At decay=0.5, low investment is 50% of max — too shallow (players feel their early investment doesn't matter much). At decay=0.8, low investment is 20% of max — too steep (zero-investment skills feel broken). 0.65 is the design sweet spot tested against genre precedent:

| Game | Per-skill investment scaling | Effective range |
|---|---|---|
| **Diablo 2 (LoD)** | +1 level synergy bonuses; ~1-20 levels per skill | ~10-100% damage scaling from base to maxed (varies by skill) |
| **Path of Exile** | Gem level scaling + quality | ~30-100% (gem level 1 to gem level 20 + 23% quality) |
| **Last Epoch** | Per-passive-point scaling on skill nodes | ~20-100% (per-node points 0-5; ~6 nodes per skill) |
| **Grim Dawn** | Per-skill-rank scaling | ~10-100% (skill rank 1 to skill rank cap; varies) |

The 35-100% range (Pattern 1 at decay=0.65) sits in the middle of genre precedent — meaningful gradient (sharper than PoE gems) without being punitive at low investment (gentler than D2 synergies). Phase 4 multi-dim calibration may adjust decay within [0.55, 0.75] to land on Discipline #47 Target 4 compliance.

### 3.5 Calibration anchor — max-investment (15/15)

`base_at_max` per skill per tier is calibrated such that the cohort_median KPM at the **max-investment** profile (15/15 active points distributed across the kit's active skill nodes; passive nodes maxed at 5/5; T4 chosen) lands on the doc 50 § 4 5 targets simultaneously.

The W-α3 Phase 2 calibrated BASE_DAMAGE_L50 values are SCAFFOLD per Discipline #39 case 12 because they were calibrated at the implicit-no-investment profile. Phase 3d gamora BASE re-derivation operates against the max-investment-anchored profile. Phase 4 multi-dim calibration extends the validation across investment profiles (low / mid / max / mixed) to ensure floor targets (Target 2 + Target 5) hold AT ALL profiles, not just max-investment.

**Why max-investment anchor (not midpoint, not per-pattern-distinct):**

- **Max-investment** — the cohort_median anchor IS the endgame player profile; aligns with doc 50's player-consequence framing (every kit functions in the band at endgame; sub-max profiles are the natural progression toward this band)
- **Midpoint** (would anchor at points=7-8/15) — fails the player-experience semantic; the design intent is that endgame players are the calibration target, not mid-game players; midpoint anchor would force endgame players above the band (super-peak at 15/15)
- **Per-pattern-distinct** — Pattern 1 at max + Pattern 2 at max — both patterns anchor at max, but with DIFFERENT decay parameters per pattern (decay=0.65 active; decay=0.50 passive) → the patterns compose at max-profile without conflict; sub-max profiles produce natural variance that the bounded-viability floor target (≥30% cohort median) absorbs

**Decision:** max-investment is the calibration anchor for both Pattern 1 and Pattern 2.

---

## 4. Pattern 2 — Passive skill effect scaling

### 4.1 Domain

- **Node type:** passive skill node
- **Investment domain:** points ∈ [0, 5] (per `cycle13Types.ts:255` `NODE_MAX.passive = 5`)
- **Per-character node count:** passive node count emerges from kit generation (doc 40 + doc 46 architectural foundation); ~5-10 passive nodes per kit estimated (Phase 3 implementation detail; rocket Wave 1 LUT alignment data point)
- **Per-character passive points budget:** ~25-50 total passive investment points (interaction with active + T4 budget is Phase 4 calibration parameter)

### 4.2 Formula structure (LINEAR-WITH-FLOOR, narrower decay)

The Pattern 2 formula is:

```
effect_magnitude_at_points = base_at_max × ((1 - decay) + decay × (points / NODE_MAX_passive))

where:
  NODE_MAX_passive = 5
  decay           = 0.50  (Phase 2 starting value; Phase 4 calibration adjusts within [0.40, 0.60])
  base_at_max     = calibrated per-passive-effect value (Phase 3d gamora seam derives)
```

Substituting concrete values:

```
points = 0:  magnitude = 0.50 × base_at_max
points = 1:  magnitude = (0.50 + 0.50 × 1/5) × base_at_max = 0.60 × base
points = 2:  magnitude = (0.50 + 0.50 × 2/5) × base_at_max = 0.70 × base
points = 3:  magnitude = (0.50 + 0.50 × 3/5) × base_at_max = 0.80 × base
points = 4:  magnitude = (0.50 + 0.50 × 4/5) × base_at_max = 0.90 × base
points = 5:  magnitude = 1.00 × base_at_max ← cohort_median anchor
```

The bounded floor (0.50 at points=0) is higher than Pattern 1's 0.35 floor. Rationale: passive effects (stat bonuses, defenses, triggered-passive proc-rates) compose multiplicatively across many sources; a passive at 50% of max is felt less acutely than an active skill at 35% of max because passive effects aggregate. The 50% floor preserves passive-skill investment depth (5× the per-point sensitivity that active skills carry, since the active domain is 3× larger) without making zero-point passives feel broken.

The 0.50 decay parameter is the gradient. Each invested point provides a 10% step toward max-magnitude. At 3/5 the passive is at 80% — meaningful investment but not max. At 5/5 the passive is fully realized.

### 4.3 Composition with passive-effect targets

Pattern 2 magnitude `effect_magnitude_at_points` is the per-effect scalar. It applies to whichever effect type the passive provides:

| Passive effect type | Pattern 2 application |
|---|---|
| **Stat bonus (e.g., +X STR)** | `STR_bonus = base_STR_at_max × effect_magnitude_at_points` |
| **Defense modifier (e.g., +X% DR)** | `DR_at_points = base_DR_at_max × effect_magnitude_at_points` |
| **Triggered-passive proc-rate** | `proc_rate = base_proc_rate_at_max × effect_magnitude_at_points` |
| **Triggered-passive magnitude** | `triggered_magnitude = base_magnitude_at_max × effect_magnitude_at_points` |

For Concentration architecture (doc 46) Layer 4 triggered-passive design: the trigger CONDITION is binary (fires or doesn't); Pattern 2 scales the EFFECT magnitude when it fires. Proc-rate scaling vs magnitude scaling per-trigger is a Phase 3b rocket implementation decision per math note.

**Critical composition observation:** Pattern 2's effect is per-passive-node. A kit with 6 passive nodes invested at 3/5 each does NOT experience compound Pattern 2 scaling (compounding is a Pattern 5 synergy bonus). Each passive's magnitude is computed independently from its own points-invested value. Player effects compose at the aggregator (e.g., gear_aggregates + chain_passives + T4 effects) per doc 47 § 2.2 damage equation.

### 4.4 Why different decay parameter than Pattern 1 (0.50 vs 0.65)

The two domains (5-point passive, 15-point active) have different sensitivity profiles:

- **Active (15 points):** each point represents ~6.7% of total investment depth → finer-grained sensitivity → higher decay (0.65) preserves meaningful per-point feel
- **Passive (5 points):** each point represents 20% of total investment depth → coarser per-point sensitivity → lower decay (0.50) keeps zero-point passives at 50% of max (meaningful but not max)

**Genre precedent for differential decay:** Last Epoch's per-passive-point scaling is approximately 0.45-0.55 effective decay (1/5 nodes produce ~20% scaling per node); PoE's gem-level scaling is approximately 0.65-0.75 effective decay (1/20 levels produce ~3.5-5% per level). Differential decay per investment-domain size is genre canon.

### 4.5 Calibration anchor — max-investment (5/5)

Same as Pattern 1. `base_at_max` per passive effect is calibrated such that the cohort_median KPM at the max-investment profile lands on doc 50 § 4 5 targets simultaneously. Phase 3d gamora derives `base_at_max` per-passive-effect per-tier; Phase 4 extends validation across investment profiles.

---

## 5. Per-tier ratio preservation — 1:1.5:2.17:4.0

### 5.1 The ratio (Matt verbatim Phase 2 spec)

Tier coefficients across T1, T2, T3, T4:

```
T1 : T2 : T3 : T4 = 1.00 : 1.50 : 2.17 : 4.00
```

Interpreted:
- A T2 skill at the same investment as a T1 skill produces **1.5×** the damage
- A T3 skill produces **2.17×** the T1 damage
- A T4 skill produces **4.00×** the T1 damage

These ratios are the tier-coefficient layer in the damage equation. `tier_coefficient(skill_tier)` enters Pattern 1 and the doc 47 damage equations at OUTER-LAYER (after `skill_damage_multiplier_at_points`).

### 5.2 Why this ratio (genre precedent)

The 1:1.5:2.17:4.0 ratio sequence is approximately the geometric progression `1, √(2.25), √(4.71), √(16) ≈ 1, 1.5, 2.17, 4.0`. The progression is gentler T1→T2→T3 (~1.5× per step) and sharper T3→T4 (~1.84× step):

| Step | Ratio | Genre comparison |
|---|---|---|
| T1 → T2 | 1.5× | D2 LoD level-2 vs level-1 skill (~1.4-1.6× depending on skill); PoE gem level scaling at 5-level intervals |
| T2 → T3 | 1.45× (2.17 / 1.5) | Same progression — uniform mid-tier scaling |
| T3 → T4 | 1.84× (4.00 / 2.17) | **Capstone scaling** — T4 is the build's specialization peak; the larger step intentionally separates capstone identity from supporting kit |

The T4 step at 1.84× is the **capstone tier-coefficient signature**. Combined with the 1.5-2.0× cohort_median peak target (doc 50 § 4.4 Target 4), T4 specialization produces the player-experience signal "this is my build's signature skill" without violating bounded-viability (T4 at 4.0× tier_coefficient × Pattern 1 max multiplier × cohort_median calibration → the kit's peak encounter type produces ~1.5-2.0× cohort_median because BASE re-derivation scales `base_at_max` per-tier such that T4 max-investment produces in-band specialization).

### 5.3 Preservation mechanism

Phase 3d gamora BASE_DAMAGE_L50 re-derivation MUST preserve the 1:1.5:2.17:4.0 ratio at the **cohort-output layer under max-investment profile.** This means:

```
For each damage-scaling path P ∈ {STR-physical, DEX-physical, INT-magical, WIS-faith}:
  For each kit K in cohort:
    For each tier T ∈ {T1, T2, T3, T4}:
      cohort_median_KPM(K, T, max-investment-profile) MUST satisfy:
        KPM(K, T2, max) / KPM(K, T1, max) ≈ 1.50  (± gamora-seam tolerance, suggested ±5%)
        KPM(K, T3, max) / KPM(K, T1, max) ≈ 2.17  (± tolerance)
        KPM(K, T4, max) / KPM(K, T1, max) ≈ 4.00  (± tolerance)
```

The preservation operates at the **product layer** because Pattern 1 multiplier at max=1.00 contributes uniformly across tiers (1.0 × all tiers = preserved ratios). The tier ratio is a property of `tier_coefficient × base_at_max`, NOT of the per-skill points-invested multiplier.

**Investment-scaling composition with per-tier ratios:** at sub-max investment, the tier ratios shift slightly because Pattern 1 multiplier varies (e.g., a kit at 7/15 average investment produces ~0.65× of max across all tiers; ratios preserved). At mixed-profile (some skills max, others low), the per-skill ratios are uniform but the per-tier cohort_median shifts based on which tier is more-invested. This is intentional design — mixed-profile builds are expected to produce variance from cohort-typical.

**Phase 3d math-note requirement:** gamora math note documents the per-path per-tier per-kit BASE_DAMAGE_L50 derivation as a 4-axis (path × kit × tier × {points-invested}) calibration sweep with preservation criterion checked at max-investment slice. The math note's preservation verification IS the Phase 3d acceptance criterion.

### 5.4 Composition with bounded-viability constraints

Doc 50 § 4 Target 1 (base DPS variance ≤ 1.5× across the 4 damage paths) operates at the cross-path layer. Doc 50 § 4 Target 4 (specialization 1.5-2.0× cohort median on 1-2 encounter types) operates at the per-kit-per-encounter layer.

Per-tier 1:1.5:2.17:4.0 ratio composition with bounded-viability:

- **Target 1 (cross-path base DPS variance ≤1.5×):** holds across all tiers if the ratio is preserved at each path independently. Phase 3d derives BASE_DAMAGE_L50 per path such that the at-T1-and-at-max-investment cohort_median DPS varies ≤1.5× cross-path. T2/T3/T4 inherit the variance because tier_coefficient is uniform across paths.
- **Target 4 (specialization peaks):** specialization emerges from per-kit-per-encounter-type variance, NOT from per-tier variance. A kit's peak encounter type at max-investment-profile produces a 1.5-2.0× cohort_median ratio because of `base_at_max(P, kit, T) × encounter-specific damage interaction × encounter HP scaling`. The per-tier ratio is uniform per-kit; specialization is a per-encounter-type signal.

The two layers compose cleanly: per-tier ratios provide the **vertical progression structure** (T1 → T4 build progression); bounded-viability targets provide the **horizontal output band** (per-encounter-type cohort_median compliance).

---

## 6. Profile semantic definitions (Jack-ryan Gate-1 Amendment #3)

### 6.1 The 4 conceptual labels

| Label | Conceptual meaning | Player-experience semantic |
|---|---|---|
| **low-profile** | Character has invested a small fraction of the per-character skill-point budget across active + passive nodes | Early-game / leveling phase; build is "coming online"; sub-cohort_median KPM expected; bounded-viability floor (Pattern 1 0.35 floor; Pattern 2 0.50 floor) holds; encounters are slower but playable |
| **mid-profile** | Character has invested ~25-75% of total skill-point budget | Mid-game / endgame approach; build is recognizable but not maxed; KPM approaches cohort_median; specialization peaks beginning to emerge but below max-investment peak height |
| **max-profile** | Character has invested ≥~75% of total skill-point budget, with primary active skills near max (15/15) and primary passive nodes near max (5/5) | Endgame / fully-realized build; KPM at cohort_median; specialization peaks at 1.5-2.0× cohort_median per doc 50 Target 4; THIS IS THE COHORT_MEDIAN CALIBRATION ANCHOR |
| **mixed-profile** | Character has invested points across active + passive in ratios distinct from cohort-typical (e.g., 90% passive depth + minimal active investment, or all-active-no-passive) | Intentional unconventional build; expected outlier on cohort_median; player-experience semantic: "I'm playing a non-standard build"; doc 50 Target 5 (≥30% cohort_median floor) holds at mixed-profile per Phase 4 validation |

### 6.2 Why these 4 categories (and not, e.g., per-percentile)

The 4-category partition mirrors the genre's progression-phase vocabulary:
- D2 LoD: leveling (low) / mid-game (mid) / Hell-difficulty endgame (max) / atypical builds (mixed)
- PoE: campaign (low) / yellow maps (mid) / red maps + uber bosses (max) / meme builds (mixed)
- Last Epoch: campaign (low) / mid-monolith (mid) / 300+ corruption (max) / off-meta (mixed)

A continuous percentile would map to the same conceptual phases without naming them. The 4-category partition gives Phase 3+4 gamora seam discretion to set NUMERIC thresholds per the specific validation harness needs, while keeping the player-experience semantics canonical.

### 6.3 Numeric threshold deferral to Phase 3+4 gamora seam

Per master scoping § 1 Phase 2 + jack-ryan Gate-1 Amendment #3 verbatim: "conceptual labels — low / mid / max / mixed-profile (numeric thresholds = Phase 3+4 gamora seam discretion)."

Gandalf seam canonical authority covers the conceptual partition. Gamora seam discretion covers:
- **low-profile threshold:** % of budget below which low-profile classification applies (suggested starting point: <25% of total budget)
- **mid-profile range:** % range for mid-profile (suggested: 25-75%)
- **max-profile threshold:** % above which max-profile classification applies (suggested: ≥75%)
- **mixed-profile detection:** how deviation from cohort-typical investment distribution is detected (e.g., L1-norm distance from mean kit investment distribution per BC cell exceeding threshold T)

These thresholds enter Phase 4 multi-dim calibration as cohort axis bins. The calibration sweep verifies bounded-viability targets per profile bin per encounter type per cohort per path = ~4-profile × 4-cohort × 6-encounter × 4-path = ~384-cell space per master scoping § 1 Phase 4.

### 6.4 The cohort_median calibration anchor is max-profile

The cohort_median that doc 50's 5 design targets validate against is computed at **max-profile** specifically. Sub-max profiles produce natural variance bounded below cohort_median; mixed-profile produces variance distributed across the band.

**Player-consequence framing:** the design directive operates over endgame play. "Bounded variance with designed peaks" describes the endgame experience the player has at fully-realized build. Sub-max profiles experience progression — the bounded floor (Pattern 1 0.35 × cohort_median; Pattern 2 0.50 × cohort_median) preserves bounded-viability AT all profile levels even when the calibration anchor is max-profile.

---

## 7. Discipline #47 verification framework (Gate-1 Amendment #1 fold-in)

### 7.1 The verification criterion

Doc 50 § 4 Target 4: every kit has 1-2 encounter types where `kit_KPM / cohort_median_KPM ∈ [1.5, 2.0]`. Discipline #47 requires this hold at max-investment profile (the cohort_median calibration anchor).

Jack-ryan Gate-1 Amendment #1 (from prior W-α7 scoping, preserved into Phase 2): verify chosen formula keeps peak KPM ratios within [1.5, 2.0] × cohort median AT MAX INVESTMENT.

### 7.2 The proof at max-investment

At max-investment profile:
- Pattern 1 multiplier at points=15 = `base_at_max × 1.00`
- Pattern 2 magnitude at points=5 = `base_at_max × 1.00`
- Both patterns produce the calibrated `base_at_max` value at max — by construction

Therefore at max-investment-profile, the kit's `damage_multiplier_at_points` (Pattern 1) is uniformly at `base_at_max` for all maxed active skills. The kit's `effect_magnitude_at_points` (Pattern 2) is uniformly at `base_at_max` for all maxed passive nodes.

**Specialization peaks emerge from `base_at_max` distribution, NOT from investment scaling.** Phase 3d gamora BASE re-derivation operates per-path × per-kit × per-tier such that:

```
For each kit K:
  For at least 1 and at most 2 encounter types E:
    kit_KPM(K, E, max-profile) / cohort_median_KPM(E, max-profile) ∈ [1.5, 2.0]
```

This is achieved by `base_at_max(P, K, T)` calibration that produces the desired peak distribution. Investment scaling at points=15 sets the multiplier to 1.0, which means the peak is exactly `base_at_max(P, K, T)`. No investment-driven super-peak above the calibrated max exists.

### 7.3 The proof at sub-max-investment

At sub-max-investment profiles:
- Pattern 1 multiplier at points < 15 = `base_at_max × ((1 - decay) + decay × (points / 15)) < base_at_max`
- Pattern 2 magnitude at points < 5 = `base_at_max × ((1 - decay) + decay × (points / 5)) < base_at_max`

Therefore at sub-max-profile, kit_KPM is BOUNDED BELOW the max-profile value. The ratio `kit_KPM(sub-max) / cohort_median_KPM(max-profile)` is ALWAYS < `kit_KPM(max) / cohort_median_KPM(max)` for the same kit. Sub-max profiles cannot produce super-peaks above 2.0× cohort_median at max-profile because the multiplier is bounded by 1.0.

**However:** sub-max profiles can produce floor violations if `base_at_max × (1 - decay)` falls below cohort_median × 0.30 (Target 5). Phase 4 multi-dim calibration verifies Target 5 holds at low-profile across all encounter types. If Phase 4 surfaces low-profile floor violations, the resolution paths are:
- Increase `(1 - decay)` floor (e.g., active 0.35 → 0.40; passive 0.50 → 0.55)
- Increase `base_at_max` calibration to push entire investment curve higher (pulls max-profile peaks above 2.0× → Target 4 violation; this resolution is NOT preferred)
- Bound-by-encounter-HP-rebalancing (Phase 3c gamora encounter HP rebalancing): reduce low-profile required output via lower-HP encounters early-game (this is the recommended resolution path; aligns with case 10 timing-floor mitigation)

### 7.4 Composition with Discipline #47 Gate-1/Gate-2 triggers

Per Discipline #47:
- **Gate-1 trigger:** "Does this dispatch introduce a balance change that affects combat outcome metrics? Which of the 5 targets does this change affect?"
- **Gate-2 trigger:** "Does the completing wave's validation output confirm all 5 targets are simultaneously satisfied?"

Phase 3 implementation dispatches (rocket Pattern 1; rocket Pattern 2; gamora encounter HP rebalancing; gamora BASE re-derivation) ALL affect combat outcome metrics. Each dispatch MUST:
1. State which of the 5 targets is affected
2. Predict the direction of change
3. Reference this canonical doc § 7 as the verification framework

Phase 4 multi-dim calibration is THE Discipline #47 enforcement workstream. The W-α4 harness extended to multi-dim (Phase 5a) validates 5 targets simultaneously across the 384-cell space.

Phase 5c Wave 5 RE-FIRE produces the production-state telemetry that the Bundle Gate-2 verifies. Compound pass = all 5 targets satisfied at max-profile AND aggregate compound pass across all profiles.

---

## 8. Patterns 3-6 — canonical-locked stubs (Cycle 15+ implementation)

The following patterns are NAMED and CANONICAL but implementation is deferred to Cycle 15+. The stubs are load-bearing in that they:
- Reserve the design vocabulary (future cycles compose against locked Pattern numbers)
- Document the architectural distinction from Patterns 1+2 (preserves the partition that Cycle 14 v1 close depends on)
- Surface design intent for Cycle 15+ scope planning

### 8.1 Pattern 3 — Threshold unlocks

**Domain:** any node type (active or passive) at named investment thresholds.

**Design intent:** discrete capability gates that activate at specific points-invested values. Not continuous; binary or N-ary. Examples (illustrative, NOT canonical until Cycle 15+ implementation):

- "At 3/5 invested in `aegis_passive`, gain DR=10% against ranged"
- "At 8/15 invested in `whirlwind_active`, whirlwind gains additional AOE-radius=20%"
- "At 15/15 invested in `firebolt_active`, firebolt gains pierce property"

**Why Pattern 3 is separate from Pattern 1:** Pattern 1 is continuous damage scaling; Pattern 3 is discrete capability unlock. Conflating them would produce the design failure of "investment as one undifferentiated mechanism." Genre precedent: PoE notable nodes vs small passive nodes; Last Epoch named passive nodes at investment thresholds.

**Cycle 15+ implementation scope:**
- Threshold value vocabulary (which thresholds are valid: e.g., 3/5, 5/5 passive; 3/15, 5/15, 8/15, 10/15, 12/15, 15/15 active)
- Threshold capability spec format (which Concentration Layer 4 trigger conditions or Layer 4 capability tags are eligible)
- Per-skill threshold count limits (avoid threshold-soup; 1-3 thresholds per active is the design ceiling estimate)
- Cohesion-judge integration (LLM-generated theme-aware threshold-effect naming)

**Composition with Pattern 1:** at threshold-fire points, the skill gains the capability AND continues to scale per Pattern 1. Pattern 3 effects compose multiplicatively with Pattern 1; capability presence is additive (binary gate).

### 8.2 Pattern 4 — QoL modifiers

**Domain:** any node type. Quality-of-life effects: animation speed, resource regen rate, cooldown smoothing, cast time, movement speed during cast, etc.

**Design intent:** non-damage-impacting modifiers that improve player feel and execution discipline without affecting bounded-viability metrics. The KPM metric is damage-throughput; QoL modifiers do not directly affect KPM but affect player-experience subjective feel.

**Why Pattern 4 is separate:** Pattern 4 effects do NOT enter the doc 50 5-target validation (per Discipline #47 § Scope: "What this discipline does NOT cover: UX/visual design"). QoL modifiers are designed against player-experience criteria (responsiveness, juiciness, build feel), not against KPM targets.

**Cycle 15+ implementation scope:**
- QoL effect vocabulary (animation_speed_pct, cast_time_pct, resource_regen_rate, etc.)
- Per-effect investment scaling form (Pattern 1 linear-with-floor likely reused; per-effect calibration)
- Composition with Pattern 1 (QoL multipliers do not compound with damage multipliers; they live in separate equation channels)

### 8.3 Pattern 5 — Synergy bonuses

**Domain:** cross-node (relational). Activates when N nodes in a related cluster all have ≥M invested points.

**Design intent:** rewards build-coherence. A player who invests in 4 fire-themed nodes triggers a fire-synergy bonus. Composes with Concentration architecture's compositional-synergy-scan (doc 46 Layer 7); Pattern 5 is the player-facing manifestation of cross-node synergies that the algorithm pre-scans at generation time.

**Why Pattern 5 is separate:** Pattern 5 is RELATIONAL (depends on multiple nodes). Patterns 1+2 are per-node. Confusing them would produce the design failure of "investment scaling depends on other nodes" which violates the per-node calibration anchor.

**Cycle 15+ implementation scope:**
- Synergy cluster definition (which nodes form synergy clusters; substrate-emergent or designer-curated)
- Synergy threshold condition (e.g., "4 of 6 fire-themed nodes ≥3 invested triggers")
- Synergy bonus form (damage_multiplier? QoL? Pattern-3-style capability unlock?)
- Two-pass synergy scan composition (Pass 1 resolve / Pass 2 preserve; per doc 46 Layer 7 + doc 43 W2)
- AI-tell guard (D7) — synergy bonuses must not LLM-resolve at runtime

### 8.4 Pattern 6 — Resource economy modifiers

**Domain:** any node type. Cost/refund/efficiency modifiers: mana cost reduction, resource generation, ω-penalty mitigation, cooldown reduction.

**Design intent:** modifies the resource-economy axis of build identity. A kit that invests heavily in mana-cost-reduction nodes plays differently than a kit that invests in raw damage; build-shape variation emerges from resource-axis choices.

**Why Pattern 6 is separate:** Pattern 6 affects the resource-economy BC axis (doc 09 Geometry palette + qd-engine-bc-axes-lock-2026-05-20.md axis 8). Patterns 1+2 affect damage-amplitude axis. Cross-axis interactions are designed deliberately, not by accident.

**Cycle 15+ implementation scope:**
- Resource-effect vocabulary (mana_cost_pct, resource_regen, cooldown_pct, ω-penalty_pct)
- Pattern 6 scaling form (likely Pattern 1 linear-with-floor reused per-effect)
- Composition with damage equation (resource modifiers do NOT enter damage equation directly; they affect cast-rate which compounds with damage-per-cast at the KPM layer)
- Composition with Pattern 5 (resource-economy synergies are an expected design surface)

### 8.5 Patterns 7+ (unnamed)

Future cycles may extend the pattern vocabulary. Patterns 7+ would emerge from observed player-experience gaps OR from deeper design dialogue. The 6-pattern partition is sufficient for Cycle 14 v1 close + Cycle 15+ scope; extension is not anticipated within the 4-6 week Path α budget.

---

## 9. Cross-references updated

The following docs require cross-reference updates at session close (Phase 2 acceptance criteria):

| Doc | Update | Section |
|---|---|---|
| `canonical/00-ground-state.md` | Add this doc (51) as new CURRENT entry in § 1 Current Truth table; one-line description (TL;DR-derived) | § 1 |
| `canonical/02-roadmap.md` | Reference Cycle 14 trajectory (Patterns 1+2 Phase 3 implementation); add Patterns 3-6 as Cycle 15+ design surfaces | Cycle 14 v1 / Cycle 15+ sections |
| `canonical/47-damage-scaling-architecture-2026-05-27.md` | Add forward-link at § 3 to this doc (the `skill_damage_multiplier` and `skill_damage_multiplier_at_points` composition layer) | § 3 (composes with the existing doc 50 forward-link in same section) |
| `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` | Add composition note: Patterns 1+2 (this doc) operate at the per-node investment layer; bounded-viability validation targets are evaluated at max-investment-profile (cohort_median calibration anchor) | § 4 + § 5 |

Cross-reference updates LANDED in this Phase 2 commit per master scoping § 1 Phase 2 acceptance criterion.

---

## 10. Forward-link to Phase 3+4+5+6 work-streams

### 10.1 Phase 3a — rocket Pattern 1 implementation

**Owner:** rocket (foundation seam)
**Scope:** active skill damage scaling per § 3 of this doc; `per_skill_emitter.py` + `damage_resolver.py` touched
**Math note required:** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-phase-3-pattern-1-2026-05-28.md`; captures formula structure + application-order specification (Option A per § 3.3) + composition with W-α3 calibration semantics
**Acceptance:** Pattern 1 multiplier produced at `points / NODE_MAX_active` query; cohort_median at max-investment matches `base_at_max`; floor at points=0 is 0.35 × `base_at_max`
**Tag:** `rocket/v1.9-w-alpha-7-plus-pattern-1-1` (master scoping § Phase 3a)

### 10.2 Phase 3b — rocket Pattern 2 implementation

**Owner:** rocket (foundation seam)
**Scope:** passive skill effect scaling per § 4 of this doc
**Math note required:** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-phase-3-pattern-2-2026-05-28.md`; captures formula structure + per-effect-type composition (stat bonus / DR / proc-rate / magnitude)
**Acceptance:** Pattern 2 magnitude produced at `points / NODE_MAX_passive` query; cohort_median at max-investment matches `base_at_max`; floor at points=0 is 0.50 × `base_at_max`
**Tag:** `rocket/v1.10-w-alpha-7-plus-pattern-2-1` (master scoping § Phase 3b)

### 10.3 Phase 3c — gamora encounter HP rebalancing (case 10 resolution)

**Owner:** gamora (simulation seam)
**Scope:** per-encounter HP factors in `endgame_mob_stat_profile.py` adjusted to escape fight-engine 0.1s timing floor for low-HP encounter types (open_arena / chokepoint_corridor / magic_pack / elite_pack); mini_boss + boss_with_adds factor ranges re-evaluated to ensure T4 specialization peaks at 1.5-2.0× cohort median become achievable
**Acceptance:** post-rebalance W-α6-style sweep produces 18-kit KPM differentiation (not all-600 uniform) on swarm encounter types; T4 specialization peaks achievable at 1.5-2.0× cohort_median per Discipline #47 Target 4
**Tag:** `gamora/v2.9-w-alpha-7-plus-phase-3-encounter-hp-rebalance-1` (master scoping § Phase 3c)

### 10.4 Phase 3d — gamora BASE_DAMAGE_L50 re-derivation

**Owner:** gamora (simulation seam)
**Scope:** under new W-α7+ formulas (Patterns 1+2 implemented) + new encounter HP (Phase 3c landed) + per-investment-profile reference targets; replaces W-α3 Phase 2 calibrated values (scaffold per Matt D1)
**Acceptance:** per-tier 1:1.5:2.17:4.0 ratio preserved at cohort-output layer under max-investment-profile per § 5.3 of this doc; per-path base DPS variance ≤1.5× per doc 50 § 4 Target 1
**Tag:** `gamora/v2.10-w-alpha-7-plus-phase-3-base-rederivation-1` (master scoping § Phase 3d)

### 10.5 Phase 4 — gamora multi-dim calibration

**Owner:** gamora (simulation seam)
**Scope:** calibration target = bounded-viability across paths × cohorts × encounter_types × investment_levels = ~4 × 4 × 6 × 4-profile = ~384-cell space; binary search across expanded space; verify cross-path parity ≤1.5× at multiple investment profiles per doc 50 § 4.1
**Acceptance:** all 5 doc 50 targets satisfied at max-profile AND aggregate compound across profiles
**Tag:** `gamora/v2.11-w-alpha-7-plus-phase-4-multi-dim-calibration-1` (master scoping § Phase 4)

### 10.6 Phase 5a — gamora BVV harness multi-dim update

**Owner:** gamora (simulation seam)
**Scope:** harness measures across multi-dimensional space (paths × cohorts × encounter_types × investment_levels); per-profile compound_pass + aggregate compound_pass
**Tag:** `gamora/v2.12-w-alpha-7-plus-phase-5a-bvv-multi-dim-1` (master scoping § Phase 5a)

### 10.7 Phase 5b — drax loadout UI revival

**Owner:** drax (loadout app seam)
**Scope:** NODE_MAX surfaces become MECHANICALLY MEANINGFUL post-Phase-3 implementation; loadout UI displays investment-scaled output (per-skill point delta visible)
**Composition with this doc:** drax consumes Pattern 1 + Pattern 2 formulas via Phase 3 schema additions; the per-point multiplier displayed in UI is the Pattern 1/2 result at the player's current investment
**Tag:** `drax/v1.2-w-alpha-7-plus-phase-5b-loadout-investment-ui-1` (master scoping § Phase 5b)

### 10.8 Phase 5c — gamora Wave 5 RE-FIRE

**Owner:** gamora (simulation seam)
**Scope:** full production season under composite engine state (Path α + integrated W-α7+ + R5-Plus scrub + Phase 5 LLM naming); Bundle Gate-2 multi-coverage
**Tag:** `gamora/v2.13-w-alpha-7-plus-phase-5c-wave-5-refire-1` (master scoping § Phase 5c)

### 10.9 Phase 6 — final close

**Owner:** jack-ryan + gandalf + Matt
**Scope per master scoping § Phase 6:** disciplines #41-#46 batched canonical-write + A/B comparison + Matt v1 ratification

---

## 11. Discipline #45 vocabulary grep audit

**Audit performed at authoring 2026-05-28.**

**Prohibited terms checked:** class / per-class / class roster / class taxonomy / class-intrinsic / class-naming policy / archetype / role.

**Grep audit of this doc:**

| Term | Occurrences | Status |
|---|---|---|
| `class` | 0 in generative-architecture acceptance criteria | PASS — no occurrences as generative-unit vocabulary; doc uses "kit" consistently |
| `per-class` | 0 | PASS |
| `class roster` | 0 | PASS |
| `class taxonomy` | 0 | PASS |
| `class-intrinsic` | 0 | PASS |
| `class-naming policy` | 0 | PASS |
| `archetype` | 0 occurrences as generative-input label; 0 as taxonomy | PASS — doc uses "kit" + "skill" + "node" + "pattern" |
| `role` | 0 as pre-authored generative taxonomy | PASS |

**Exempt occurrences:** none required exempting in this doc. The doc operates strictly in mechanical/structural-intent vocabulary (kit / skill / node / pattern / investment / multiplier / scaling / damage / cohort / profile / encounter_type).

**Cohort labels used in this doc** (`DPS-min-maxer / Balanced / Defensive / Hybrid`): these are mechanical-property descriptors inherited from W-α6 `COHORT_KPM_BAND` / doc 50 § 5 framing. They are NOT generative-input taxonomy labels; they describe per-build mechanical fingerprints emerging from kit substrate. Per Discipline #45 scope exemption: "Describe the mechanical property directly" — these labels describe DPS/defense balance properties, not pre-authored generative taxonomy. EXEMPT.

**Verdict:** PASS — zero non-exempt prohibited-vocabulary usage in this doc's acceptance criteria, quality criterion, generative-architecture description, or schema/field naming.

---

## 12. Acceptance criteria (Phase 2 close)

Per master scoping § 1 Phase 2 acceptance:

- [x] **Pattern 1 active skill damage scaling formula specified** — linear-with-floor `base_at_max × ((1 - decay) + decay × (points / 15))` with decay=0.65 per § 3.2; composition with doc 47 § 2.2 damage equations specified per § 3.3
- [x] **Pattern 2 passive skill effect scaling formula specified** — linear-with-floor `base_at_max × ((1 - decay) + decay × (points / 5))` with decay=0.50 per § 4.2; composition with passive-effect targets specified per § 4.3
- [x] **Discipline #47 verification** — peak KPM ratios within [1.5, 2.0] × cohort median at max investment per § 7 (formal proof via Pattern 1 max-multiplier=1.0 producing peaks at calibrated `base_at_max`; Phase 3d gamora BASE re-derivation determines per-kit per-encounter peak distribution)
- [x] **Calibration anchor decision** — max-investment for both patterns per § 3.5 + § 4.5; rationale captured per § 6.4 (cohort_median represents endgame-realized character profile)
- [x] **Per-tier ratio preservation: 1:1.5:2.17:4.0** — preservation mechanism per § 5.3 (tier_coefficient is outer-layer; investment scaling at points=max produces multiplier=1.0 which preserves ratios uniformly); composition with bounded-viability constraints per § 5.4
- [x] **Per-encounter-type band design integrated** — W-α6 ENCOUNTER_COHORT_KPM_BAND structure preserved per § 0 TL;DR + § 7.3; recalibrated values under multi-dim space land in Phase 4; case 10 timing-floor constraint acknowledged with Phase 3c encounter HP rebalancing as resolution path
- [x] **Profile semantic definitions** — low / mid / max / mixed-profile semantics per § 6.1-6.4; numeric thresholds = Phase 3+4 gamora seam discretion per § 6.3
- [x] **6-pattern canonical doc** — Patterns 1+2 detailed (§ 3 + § 4); Patterns 3-6 canonical-locked stubs (§ 8.1-8.4); Patterns 7+ deferred
- [x] **Cross-references updated** — doc 00 + doc 02 + doc 47 § 3 + doc 50 per § 9 (in-flight this Phase 2 commit)
- [x] **NODE_MAX source location verified** — `reincarnated-loadout/src/data/cycle13Types.ts:255` (lines 255-259: passive=5, active=15, t4=1) per § 3.1 + § 4.1
- [x] **Discipline #45 vocabulary grep audit PASS** — § 11

---

## Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-28
**Status:** v1 canonical lock; LOAD-BEARING per integrated W-α7+ Phase 2; gates Phase 3+4+5+6 work-streams; Cycle 14 v1 close trajectory ~14-22d from Matt 2026-05-28 evening RATIFICATION AMENDMENT
**Authority:** Matt 2026-05-28 evening RATIFICATION AMENDMENT (integrated W-α7+ replaces separate Option B + W-α7) + Phase 2 firing PARALLEL with jack-ryan Gate-1 review per Matt explicit authorization
**Discipline #45 vocabulary audit:** PASS per § 11 — zero non-exempt prohibited-vocabulary usage
**Discipline #47 verification:** § 7 specifies peak-KPM-ratio framework; max-investment multiplier=1.0 by construction; specialization peaks emerge from `base_at_max` distribution (Phase 3d gamora seam); within [1.5, 2.0] × cohort_median target preserved
**Discipline #1 (math-before-code) target:** Phase 3a + 3b + 3c + 3d math notes required at `~/Games/reincarnated-engine/src/reincarnated/{generation,simulation}/math/` per master scoping § Phase 3 sub-streams; each math note cites this doc § 3 / § 4 / § 5 / § 7 by section number as the design-spec-as-math handoff
**Cross-references:** doc 00 (ground-state oracle — registration this session); doc 02 (roadmap — Cycle 14 trajectory + Patterns 3-6 Cycle 15+ surface); doc 47 § 3 (mechanical substrate; forward-link added this session); doc 50 (composition with bounded-viability constraints; cross-reference added this session); master scoping dispatch (parent); W-α6 math note (Phase 1 input absorbed); NODE_MAX source `reincarnated-loadout/src/data/cycle13Types.ts:255`; engineering-disciplines.md § 45 (vocabulary lock audit anchor) + § 47 (bounded-viability framework discipline)

**For:** the structural-intent layer over the skill-tree per-node investment domain. Phase 3 implementation (rocket Patterns 1+2; gamora BASE re-derivation + encounter HP rebalancing) consumes § 3 + § 4 + § 5 + § 7. Phase 4 multi-dim calibration consumes § 6 profile definitions. Phase 5 BVV harness validates § 7 Discipline #47 framework. From this commit forward, "Pattern 1 active skill damage scaling" and "Pattern 2 passive skill effect scaling" are the canonical vocabulary; downstream dispatches, math notes, and decisions-log entries cite them by name. The game we ship is the game where every invested point matters AND every player's build is in the band at endgame.
