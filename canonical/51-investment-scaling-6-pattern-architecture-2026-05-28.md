# 51 — Investment Scaling 6-Pattern Architecture

> **STATUS:** CURRENT (LOAD-BEARING as of 2026-05-28) — SECOND ITERATION 2026-05-28 evening (§§ 9 + 10 scope-completeness amendment batch per Matt D1+D2+D3+D4 RATIFICATION + Discipline #40 case (c) extension protocol). Phase 2 of integrated W-α7+ master scoping; canonical authority on the structural intent of skill-tree per-node investment scaling. Patterns 1+2 detailed for Cycle 14 v1 Phase 3 implementation; Patterns 3-6 canonical-locked stubs for Cycle 15+ work. § 9 captures KNOWN-GAP cross-node prerequisite unlocks (T4_UNLOCK_THRESHOLD = 0.70 acknowledgment + Cycle 15+ deferral). § 10 captures investment-profile distribution rules (calibration anchor profile decision + multi-profile distribution rules + per-profile point allocation algorithm). Gates W-α7+ Phase 3d gamora BASE re-derivation + Phase 4 multi-profile sweep. See `canonical/00-ground-state.md` § 1.

**Date:** 2026-05-28 (Phase 2 lock); 2026-05-28 evening (scope-completeness amendment batch §§ 9 + 10)
**Author:** gandalf (story-and-design steward)
**Status:** v1.1 canonical lock SECOND ITERATION — Patterns 1+2 formula structures specified + calibration anchor decision (max-investment) + per-tier ratio preservation (1:1.5:2.17:4.0) + profile semantic definitions + per-encounter-type band design integrated + Patterns 3-6 canonical-locked stubs + NEW § 9 KNOWN-GAP T4_UNLOCK_THRESHOLD = 0.70 acknowledgment + NEW § 10 investment-profile distribution rules (calibration anchor + multi-profile distribution + per-profile allocation algorithm)
**Authority:**
- **First iteration (commit `ba1c4e7`):** Matt 2026-05-28 evening RATIFICATION AMENDMENT — integrated W-α7+ scope absorbs case 9 + case 10 + case 11 + case 12; Phase 2 fires in PARALLEL with jack-ryan Gate-1 review of master scoping per Matt explicit authorization. Master scoping dispatch `agentic_orchestration/dispatches/2026-05-28-integrated-w-alpha-7-plus-master-scoping.md` § 1 Phase 2 carries verbatim scope.
- **Second iteration (§§ 9 + 10 amendment batch):** Matt 2026-05-28 evening D1+D2+D3+D4 RATIFICATION — Phase 3d gamora HALTED via TaskStop (Matt finding: rocket Phase 3a coordination signal `skill.investment_points must be set to 15` is vague on WHICH skills; Phase 4 multi-profile sweep needs distribution rules locked); KR dispatch `agentic_orchestration/dispatches/2026-05-28-gandalf-doc-51-scope-completeness-amendment-batch.md` carries verbatim scope. Discipline #40 case (c) extension protocol (NOT retraction; scope-completeness fold-in to LOAD-BEARING canonical). Case 13 surfaced; Discipline #48 candidate VALIDATED at N=2 (case 11 investment scaling gap + case 13 this § 10 distribution rules gap; Phase 6a disciplines batch territory per jack-ryan).
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

**Discipline #45 vocabulary grep audit:** PASS at authoring (first iteration) + PASS at second iteration (§§ 9 + 10 amendment batch). See § 13 for declaration.

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

## 9. KNOWN-GAP — Cross-node prerequisite unlocks (T4_UNLOCK_THRESHOLD = 0.70)

> **Status:** KNOWN-GAP at v1.1 second iteration. Cycle 15+ canonical-lock and implementation. This section captures the prior gandalf+Matt design exchange (`agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.5 D71 lock; line 68: "T4-unlock threshold — 70% of chain max (per-chain calc; chain max varies by composition)") and makes the deferral explicit so Phase 3d gamora BASE re-derivation + Phase 4 multi-profile sweep do NOT assume T4 prerequisite unlock semantics at Cycle 14 v1 close.

### 9.1 What the prior exchange ratified

Matt + gandalf 2026-05-27 Pattern-B design session (Cycle 13 pre-launch) ratified the following skill-point-economy lock (D71, recorded at `2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.5):

| Sub-item | Lock |
|---|---|
| Per-node max — Passive | 5 points (`NODE_MAX.passive = 5`) |
| Per-node max — Active (T1-T3) | 15 points (`NODE_MAX.active = 15`) |
| Per-node max — T4 capstone | 1/1 binary (0/1 if another T4 selected; D66 ONE T4 unlocked at a time) |
| Endgame total budget | ~70 points (anchor; tunable per acquisition curve) |
| **T4-unlock threshold** | **70% of chain max** (per-chain calc; chain max varies by composition) |
| Earn rate | Per-level (L1 → L50 = 50 points) + per-content-completion bonuses (~20) |
| **Branched-chain T4-unlock** | All UNIQUE prerequisites along one path; other branch optional pay-extra |

Composition with chain-prerequisite gates (separate prior exchange — `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` § "Chain-prerequisite gates"): to unlock T2 in a chain, ≥3 points invested in T1; T3 requires ≥3 in T2; T4 requires ≥3 in T3 (chain-investment threshold = 9 points minimum to reach the T4 slot before the 70%-of-chain-max threshold check fires).

### 9.2 The named constant: T4_UNLOCK_THRESHOLD = 0.70

The numeric value `0.70` is the **per-chain investment fraction** above which the chain's T4 capstone becomes available for selection. Defined as:

```
T4_UNLOCK_THRESHOLD = 0.70  # per-chain investment fraction required to unlock the chain's T4 capstone

For each chain C in kit:
  chain_invested(C)    = sum of points invested in C's T1/T2/T3 nodes
  chain_max(C)         = sum of NODE_MAX over C's T1/T2/T3 nodes (depends on chain composition: active vs passive)
  chain_progress(C)    = chain_invested(C) / chain_max(C)

T4 of chain C is UNLOCKED iff:
  chain_progress(C) >= T4_UNLOCK_THRESHOLD       (= 0.70)
  AND all chain-prerequisite gates satisfied     (≥3 points per upstream tier per Pattern A-deep verdict)
  AND D66 active identity constraint preserved   (ONE T4 unlocked at a time; player chooses which)
```

Player-consequence framing: a player who spreads 70% of a chain's investment ceiling across the chain has signaled chain commitment; the T4 capstone becomes the build-defining moment. A player below 70% has the chain partially built but is not yet entitled to its capstone — preserves the "specialize in this chain, then choose how its T4 expresses" structure surfaced in the 2026-05-26 Pattern A-deep verdicts (genre precedent: PoE Ascendancy ratification at end of Labyrinth; D3 Paragon-style depth choice; Last Epoch chapter-completion gates).

### 9.3 Why this is a KNOWN-GAP at v1.1 second iteration (NOT a Cycle 14 v1 close item)

The 70%-of-chain-max threshold is **architecturally locked** (prior gandalf+Matt exchange) but **mechanically deferred** to Cycle 15+ for the following reasons:

1. **Cycle 14 v1 calibration scope:** Phase 3d gamora BASE_DAMAGE_L50 re-derivation + Phase 4 multi-profile sweep operate at the per-skill-node investment layer (Patterns 1+2 per §§ 3 + 4). Threshold unlocks are Pattern 3 (per § 8.1) which is Cycle 15+ scope. Folding T4_UNLOCK_THRESHOLD enforcement into Cycle 14 v1 close would expand Phase 4's calibration space (separate "T4-locked" vs "T4-unlocked" cohort axes) and risk timing the Path α 4-6 week budget.

2. **Phase 3d max-profile assumption:** Phase 3d gamora BASE re-derivation operates at the max-investment profile per § 3.5 + § 4.5. At max-profile, the player has ≥70% of every chain's max invested by construction (specialization peaks at max-investment) — therefore T4_UNLOCK_THRESHOLD is satisfied at max-profile by definition. The threshold becomes load-bearing at sub-max profiles where the player has NOT yet reached 70% in some chains; those profiles are Phase 4 multi-profile sweep territory but the threshold's IMPLEMENTATION is Cycle 15+.

3. **Pattern 3 implementation scope (Cycle 15+):** per § 8.1, Pattern 3 threshold unlocks include "threshold value vocabulary" + "threshold capability spec format" + "per-skill threshold count limits" + "cohesion-judge integration" — all Cycle 15+ implementation surface. T4_UNLOCK_THRESHOLD = 0.70 is the FIRST CANONICAL VALUE in the Pattern 3 vocabulary; it's locked here so future Pattern 3 implementation cycles cite it by name rather than re-deriving.

4. **Discipline #40 case (a) compliance:** T4_UNLOCK_THRESHOLD = 0.70 is RATIFIED here (this canonical doc, second iteration) — it is NOT a scaffold-with-pending-decision. Future code that introduces a `T4_UNLOCK_THRESHOLD` constant cites doc 51 § 9 as the canonical source. Pre-amendment, the value was implicit-in-prior-exchange (`2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.5 D71 line 68) but not load-bearing-canonical. This § 9 amendment makes it canonical without changing the value.

### 9.4 Composition with Patterns 1+2 at Phase 3d + Phase 4

**Phase 3d gamora BASE re-derivation (max-profile):** T4_UNLOCK_THRESHOLD is satisfied by construction (max-profile has every chain ≥70% per chain definition). Pattern 1 multiplier at points=15 = `base_at_max × 1.0` for the chain's T4-capstone-receiving node; Pattern 2 magnitude at points=5 = `base_at_max × 1.0` for the chain's passive nodes. No T4-unlock-related runtime gating affects Phase 3d derivation.

**Phase 4 multi-profile sweep (low / mid / max / mixed):** at low-profile and some mixed-profile builds, chain_progress(C) < 0.70 for some chains C. Under the Cycle 14 v1 close model, T4 capstones in those chains are treated as **always-available for calibration purposes** — the multi-profile sweep evaluates kits as if every chain's T4 is the algorithm-chosen capstone, regardless of in-play unlock state. Rationale: Phase 4's purpose is bounded-viability calibration of `base_at_max` distribution, not in-play unlock gating. Pattern 3 enforcement (Cycle 15+) layers the runtime unlock gate on top of the calibrated `base_at_max`; the gate doesn't change the calibrated value.

**Cycle 15+ Pattern 3 implementation note:** when T4_UNLOCK_THRESHOLD enforcement lands, the in-play behavior becomes "chain_progress < 0.70 → T4 of that chain is locked → its `damage_multiplier_at_points` contribution to KPM is zero for that chain's T4 node." The kit's KPM at sub-max-profile becomes a function of WHICH chains are above 70% (and therefore have T4 capstone available). The 4 named profiles (low / mid / max / mixed) per § 6 + § 10 retain their conceptual semantics; the numeric thresholds at gamora seam discretion per § 6.3 + § 10.2 may bin profiles around "expected unlocked-chain count" once Pattern 3 enforcement is live.

### 9.5 Branched-chain T4-unlock — chain_max(C) composition

Per the prior exchange D71 lock (line 70): "Branched-chain T4-unlock — All UNIQUE prerequisites along one path; other branch optional pay-extra." This composes with the chain_progress definition:

```
For a branched chain C with main-path nodes M(C) and optional-branch nodes B(C):
  chain_max(C) = sum of NODE_MAX over M(C)              # main-path-only; branch points are "extra"
  chain_invested(C) = sum of points invested in M(C)    # only main-path points count toward T4 unlock

Branch investment increases kit capability (Pattern 1/2 damage/effect at that node)
but does NOT advance T4 unlock progress.
```

Player-consequence framing: a player who invests in branches without completing the main path delays T4 unlock. This preserves the "specialize before capstone" intent and prevents branch-investment from being the cheap-T4-unlock workaround.

**Cycle 15+ Pattern 3 implementation note:** the `M(C)` vs `B(C)` partition is per-chain-composition data (rocket Phase 2a kit composition output); the partition flows to drax loadout UI (Phase 5b) for player-visible chain_progress display.

### 9.6 Deferral rationale + Cycle 15+ entry conditions

**Deferred to Cycle 15+ entry.** Entry conditions for Pattern 3 + T4_UNLOCK_THRESHOLD implementation:

1. Cycle 14 v1 LANDED (full Path α + integrated W-α7+ close; Wave 5 RE-FIRE compound pass)
2. Drax loadout UI revival (Phase 5b) consumed Patterns 1+2 — UI surface exists for chain_progress display
3. Pattern 3 implementation scope committed in Cycle 15+ kickoff (per § 8.1 Cycle 15+ scope list)
4. Cohesion-judge integration spec'd (LLM-generated theme-aware threshold-effect naming per § 8.1)

**Cross-references for Pattern 3 Cycle 15+ implementation:**
- This doc § 8.1 Pattern 3 threshold-unlock stub
- `2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.5 D71 (the prior exchange original record)
- `2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` § "Chain-prerequisite gates" (3-point upstream-tier gates)
- D66 active identity discipline (ONE T4 unlocked at a time; runtime mechanism; preserved across Patterns 1-6)
- D75 + D73 T4-swap UX (Spirit-Guide-mediated respec; player-facing chain_progress display)

### 9.7 Acknowledgment statement

T4_UNLOCK_THRESHOLD = 0.70 is the canonical value as of doc 51 v1.1 second iteration. The threshold is **architecturally ratified** but **mechanically deferred** to Cycle 15+ Pattern 3 implementation. Phase 3d gamora BASE re-derivation + Phase 4 multi-profile sweep proceed under the assumption "every chain's T4 is calibration-available at every profile" — the unlock gate is a runtime overlay landed in Cycle 15+ that does not alter the calibrated `base_at_max` values.

---

## 10. Investment-profile distribution rules

> **Status:** v1.1 second iteration — locked. This section closes the case 13 scope-completeness gap surfaced by Matt 2026-05-28 evening manual audit (rocket Phase 3a coordination signal `skill.investment_points must be set to 15` was vague on WHICH skills; Phase 4 multi-profile sweep needs distribution rules locked before it fires). Section provides Phase 3d + Phase 4 gamora seam with the per-profile investment distribution algorithm.

### 10.1 Calibration anchor profile decision — Option A vs Option B

Phase 3d gamora BASE_DAMAGE_L50 re-derivation operates against the max-investment profile per § 3.5 + § 4.5. But "max-investment" admits two distinct constructions:

**Option A — All-skills-max:** every active skill node in the kit at `NODE_MAX.active = 15` AND every passive node at `NODE_MAX.passive = 5` AND the algorithm-chosen T4 unlocked. The kit's full schema is at investment ceiling across all nodes simultaneously.

```
For each active skill node S in kit K:    S.investment_points = 15
For each passive node P in kit K:         P.investment_points_passive = 5
For the kit's single algorithm-chosen T4: T4.unlocked = True
```

**Option B — Realistic-max specialization-aware:** the kit invests within its per-kit skill-budget ceiling (~70 endgame points per D71); specialization concentrates into 1-2 active skill nodes at NODE_MAX with remaining active skills at lower investment; passive nodes split between primary-chain max-invest and supporting-chain partial. Mirrors actual endgame loadout patterns where a player has finite skill-point budget.

```
For chain c* (player's primary specialization chain):
  Primary active skill node S* in c*:    S*.investment_points = 15  (signature skill)
  Remaining active nodes in c*:           investment_points distributed per chain-allocation rule
  Passive nodes in c*:                    investment_points_passive at or near 5

For other chains:
  Lower-tier active skill nodes:          investment_points at chain-prerequisite floor (≥3 per Pattern A-deep) or higher
  Passive nodes:                          investment_points_passive partial (1-3)
```

**Trade-off analysis:**

| Property | Option A (all-skills-max) | Option B (realistic-max specialization-aware) |
|---|---|---|
| **Structural cleanness** | Multiplier=1.0 by construction across all skills; Pattern 1 + Pattern 2 produce `base_at_max` for every node | Multiplier=1.0 at specialization peaks only; per-skill variance at non-specialization slots |
| **Calibration anchor coherence** | cohort_median computed at uniformly-max-invested profile; specialization peaks emerge solely from `base_at_max` distribution per § 7.2 | cohort_median computed at per-build-realistic profile; specialization peaks have BOTH `base_at_max` distribution AND investment concentration as sources |
| **Genre realism** | Less realistic (no actual endgame player can max every skill simultaneously; ~70-point budget bounds simultaneous max nodes) | More realistic (mirrors how players actually distribute endgame points) |
| **Per-profile variance complexity** | Zero variance at calibration anchor (every kit at uniform max-invest) | Per-build variance at calibration anchor (different kits specialize differently) |
| **Phase 4 multi-profile composability** | Clean: sub-max profiles bound below `base_at_max` uniformly; the linear-with-floor floor (Pattern 1 0.35; Pattern 2 0.50) bounds sub-max KPM transparently | Complex: sub-max profiles relative to a specialization-aware anchor introduce additional axis (which-skill-the-player-specialized-in) |
| **Doc 50 § 4 5-target verification surface** | cleaner — Target 4 (1.5-2.0× cohort_median) verified at `base_at_max(K, peak_encounter)` distribution; Target 1 (cross-path DPS variance ≤1.5×) at uniform-max profile | more complex — Target 4 + Target 1 both have specialization-pattern as nuisance variable |
| **Player-experience semantic** | "If every skill were maxed simultaneously, where would the kit's KPM land?" — counterfactual upper bound | "How does an actual endgame realized-build perform?" — empirical endgame model |

**Gandalf RECOMMENDATION: Option A — all-skills-max.**

**Rationale (genre + design coherence):**

1. **Structural cleanness wins at the calibration anchor.** Doc 51 § 7.2 proves Discipline #47 Target 4 at max-profile via "Pattern 1 max-multiplier=1.0 producing peaks at calibrated `base_at_max`." That proof is CLEAN under Option A — Pattern 1 contributes 1.0 uniformly across all skills, specialization peaks emerge solely from `base_at_max(P, K, T)` per-encounter-type distribution. Under Option B, the proof has to thread which-skills-are-at-max and which-are-not into the calibration anchor itself — the kit's KPM at peak_encounter under Option B = `f(base_at_max, specialization_pattern)`, which makes Phase 3d gamora BASE re-derivation a 5-axis (path × kit × tier × encounter × specialization_pattern) calibration instead of 4-axis. Two extra dimensions of complexity at the LOAD-BEARING calibration anchor.

2. **Specialization-as-emergent-property is doc 50's load-bearing principle.** Doc 50 § 4 "bounded variance with designed peaks" + § 5 cohort framing position the calibration anchor as the **upper-bound canonical** against which sub-max profiles vary. Option A treats the upper bound literally — every skill at its ceiling. Option B encodes specialization INTO the upper bound, which means specialization is no longer purely emergent (from `base_at_max` distribution) but is partly baked into the calibration anchor. Doc 50's principle is cleaner under Option A.

3. **Genre precedent — calibration ≠ play.** PoE balances skills against "every gem at level 20 + 23% quality" theoretical maxes; GGG's calibration is the upper bound, not the realistic mid-game endgame loadout. Last Epoch tests per-skill scaling against max-rank-per-skill independently. D2 LoD synergy bonuses were balanced against the theoretical "all synergies at level 20" max even though no actual character can achieve it (budget bound). The genre's calibration anchor convention is the structural ceiling, not the realistic build. Reincarnated joins the convention.

4. **Phase 4 multi-profile sweep needs Option A as the reference baseline.** Phase 4 evaluates bounded-viability across `paths × cohorts × encounter_types × investment_profiles` (~384-cell space per § 12.5). The reference baseline at the max-end of the profile axis MUST be a single canonical construction (otherwise per-cell variance has TWO sources — profile axis AND specialization variance within profile). Option A gives Phase 4 a clean reference; Option B muddies it.

5. **Player-consequence framing — Option A is the "ideal build" the player aspires toward.** The cohort_median that doc 50's 5 targets validate against is the CEILING the player's actual build approaches as they level. The conceptual labels in § 6.1 (low → mid → max-profile) describe the player's journey TOWARD the ceiling. If the ceiling itself is specialization-aware (Option B), the journey's destination changes per-build, which defeats the "cohort_median is the kit's full-power signature" framing.

**Where Option B has merit (acknowledged):** Option B better captures actual endgame play, and Phase 4 multi-profile sweep DOES need to evaluate specialization-aware sub-max profiles per § 10.2 mixed-profile rule. The recommendation is NOT "ignore specialization in calibration" — it is "specialization is per-encounter-type variance under cohort_median anchor, NOT a re-anchor of cohort_median itself." Option B's realistic-max semantics are absorbed into the § 10.2 max-profile distribution rule (which IS specialization-aware) — but the calibration ANCHOR remains Option A.

**Final recommendation for Phase 3d gamora seam:** adopt Option A (all-skills-max) as the calibration anchor profile. Per Matt D2: gamora retains seam discretion to override (if gamora's implementation surfaces an empirical reason Option B better serves the harness), but gandalf's design anchor is Option A.

### 10.2 Multi-profile distribution rules — low / mid / max / mixed

Per § 6.1, the 4 conceptual profile labels carry distinct distribution semantics. Phase 4 multi-profile sweep operates across all 4. Per Matt D2 + D4: numeric thresholds remain gamora seam discretion per § 6.3, but the DISTRIBUTION ALGORITHM per profile is canonically locked here so gamora's Phase 4 sweep doesn't have to guess.

#### 10.2.1 low-profile — early-game leveling phase

**Conceptual:** character has invested a small fraction of total budget (<~25%; gamora threshold discretion). Build is "coming online"; most skills are barely touched.

**Distribution rule — `low_distribution(K, budget_fraction)`:**

```
1. Compute available_points = floor(budget_fraction × total_budget(K))     # gamora seam discretion on total_budget
2. Identify primary_chain(K) per kit composition (rocket Phase 2a output)
3. Allocate available_points across primary_chain in tier order:
   a. T1 active skill node: investment_points = min(NODE_MAX.active, remaining_available / N_T1_active_in_primary)
      Floor: at least 1 point per T1 active node in primary chain if any available_points exist
   b. T1 passive nodes in primary chain: investment_points_passive = ceil(remaining / N_T1_passive)
      Capped at NODE_MAX.passive = 5
   c. T2/T3 active skill nodes in primary chain: investment_points = leftover allocation
      Subject to chain-prerequisite gates (≥3 points in upstream-tier per Pattern A-deep)
   d. Non-primary chains: investment_points = 0 (no investment in non-primary at low-profile)
4. T4 capstone: unlocked = False (low-profile chain_progress < T4_UNLOCK_THRESHOLD per § 9.2)
```

**Player-experience semantic:** player has touched their primary chain's T1 and started moving up the chain; non-primary chains are unspent. KPM at this profile is bounded BELOW by Pattern 1 floor `0.35 × base_at_max(T1)` for primary-chain skills that have ≥1 point; Pattern 2 floor `0.50 × base_at_max(T1_passive)` for primary-chain passives.

**Phase 4 verification target:** Target 5 (≥30% cohort_median floor) holds at low-profile across all encounter types. If Phase 4 surfaces floor violations at low-profile, Phase 3c encounter HP rebalancing (already landed per `gamora/v2.9`) absorbs the early-game required-output via lower-HP early-encounters.

#### 10.2.2 mid-profile — mid-game endgame approach

**Conceptual:** character has invested ~25-75% of total budget (gamora threshold discretion). Build is recognizable; primary chain approaching T4 unlock; secondary chains beginning.

**Distribution rule — `mid_distribution(K, budget_fraction)`:**

```
1. Compute available_points = floor(budget_fraction × total_budget(K))
2. Allocate ~60% of available_points to primary_chain(K) per kit composition
3. Allocate ~25% to secondary_chain(K) (algorithm-determined secondary OR player-typical secondary)
4. Allocate ~15% to supporting_chain(K) (the T3-only chain per doc 40 D83 / closeout § 1.4)
5. Within each chain, distribute by tier:
   a. Primary chain: active points concentrated at chain's T3 active skill node (pushes toward T4 unlock)
      - chain_progress(primary_chain) target = at or just above T4_UNLOCK_THRESHOLD = 0.70 by end of mid-profile range
   b. Secondary chain: distributed evenly across T1+T2 active and passive
   c. Supporting chain: T1+T2 passive nodes at NODE_MAX.passive / 2 to 5
6. T4 capstone status:
   a. If primary_chain meets T4_UNLOCK_THRESHOLD: T4 unlocked (primary_chain's T4)
   b. Otherwise: T4 locked
   c. D66 enforced (ONE T4 at a time) — only primary's T4 is candidate
```

**Player-experience semantic:** primary chain is recognizable as the build's spine; T4 capstone is the imminent goal; secondary chain provides early synergy bonuses (Pattern 5 surface when implemented); supporting chain provides the kit-identity floor (the T3-only chain absorbs what closeout § 2.1 framed as the kit's foundational passives — vocabulary substituted per Discipline #45).

**Phase 4 verification target:** Target 1 (cross-path DPS variance ≤1.5×) and Target 4 (specialization 1.5-2.0× cohort_median on 1-2 encounter types) verified at mid-profile. Mid-profile is the empirical proof-of-progression test — the kit's KPM gradient from low → mid → max-profile MUST be monotonic-increasing per encounter type.

#### 10.2.3 max-profile — endgame fully-realized

**Conceptual:** character has invested ≥~75% of total budget (gamora threshold discretion). Build is at or near max; T4 unlocked; specialization at peak.

**Distribution rule — `max_distribution(K)`:**

**Two sub-modes per § 10.1 calibration anchor decision:**

- **Mode A (calibration anchor; gandalf recommendation):** all-skills-max
  ```
  For each active skill node S in K:        S.investment_points = NODE_MAX.active = 15
  For each passive node P in K:             P.investment_points_passive = NODE_MAX.passive = 5
  T4 capstone (algorithm-chosen): unlocked = True
  ```

- **Mode B (realistic endgame; for Phase 4 specialization-variance sweep):** specialization-aware
  ```
  1. Identify signature_skill(K) per kit composition (primary chain's T3 or T4-prerequisite active skill node)
  2. signature_skill.investment_points = NODE_MAX.active = 15
  3. Remaining active nodes in primary chain: distribute remaining ~30-40 points; floor ≥3 per chain-prerequisite gate
  4. Secondary chain active nodes: distribute remaining points; min 3 per active node per chain-prerequisite gate
  5. Supporting chain passive nodes: NODE_MAX.passive = 5 each
  6. T4 capstone: unlocked = True (primary_chain's T4 per D66)
  ```

**Phase 3d gamora BASE re-derivation uses Mode A** (calibration anchor per § 10.1).

**Phase 4 multi-profile sweep uses BOTH Mode A and Mode B at max-profile bin** — Mode A as the reference baseline; Mode B as the realistic-endgame variance check (does the cohort_median computed at Mode A hold within Target 1 cross-path variance ≤1.5× when evaluated against Mode B distributed builds? If yes, calibration anchor is robust; if no, calibration anchor needs adjustment).

**Player-experience semantic:** Mode A is the "what would the spreadsheet say at infinite budget" reference; Mode B is "what an actual endgame build looks like." Both inform Phase 4 calibration verification.

#### 10.2.4 mixed-profile — atypical builds

**Conceptual:** character has invested points across active + passive in ratios distinct from cohort-typical (e.g., 90% passive depth + minimal active; or all-active-no-passive; or supporting-chain-heavy). Intentional unconventional build; expected outlier on cohort_median.

**Distribution rule — `mixed_distribution(K, variant)`:**

Phase 4 sweep evaluates 3 canonical mixed-profile variants per kit:

- **mixed_variant_1 (passive-heavy):** all passive nodes at NODE_MAX.passive = 5; active skill nodes at chain-prerequisite floor (≥3 per gate) only
- **mixed_variant_2 (active-heavy):** all active skill nodes at NODE_MAX.active = 15 (primary chain) or 10 (secondary chains); passive nodes at investment_points_passive = 1
- **mixed_variant_3 (supporting-chain-heavy):** supporting chain's passive nodes all at NODE_MAX.passive = 5; primary + secondary chains at chain-prerequisite floor only

**Per Phase 4 sweep purpose:** mixed-profile variants verify Target 5 (≥30% cohort_median floor) holds at intentional-unconventional builds. Mixed-profile KPM is EXPECTED to be sub-cohort_median; the Target 5 floor (30%) is the design's "your unconventional build is still viable" floor.

**T4 capstone status under mixed-profile:** evaluated per chain_progress per § 9.2. Some mixed variants will have T4 unlocked (Variant 2 in primary chain); others will not (Variant 1 passive-heavy may not reach T4_UNLOCK_THRESHOLD on any chain). Phase 4 sweep records T4-unlocked-state per variant and evaluates KPM with the appropriate T4 contribution.

### 10.3 Per-profile point allocation algorithm

Phase 4 multi-profile sweep constructs per-profile investment distributions per the following algorithm:

```
ALGORITHM: construct_profile_distribution(kit K, profile P, variant V=None)

INPUTS:
  K            : kit (rocket Phase 2a kit composition output; active skill nodes + passive nodes + chain partition + T4 alteration)
  P            : profile ∈ {low, mid, max, mixed}
  V            : optional variant for mixed profile ∈ {passive_heavy, active_heavy, supporting_chain_heavy}; None for low/mid/max

OUTPUTS:
  distribution : dict mapping each node in K to its investment_points value
                 (active nodes → investment_points; passive nodes → investment_points_passive; T4 → unlocked boolean)

ALGORITHM:
  1. Identify chain partition:
     chains = K.chains                                    # list of chains per kit composition
     primary_chain = chains[0]                            # algorithm-determined primary (rocket Phase 2a)
     secondary_chains = chains[1:-1] if len(chains) > 2 else []
     supporting_chain = chains[-1]                        # T3-only supporting chain per doc 40 D83

  2. Compute total_budget(K):
     active_nodes_per_chain = K.active_node_count_per_chain     # per kit composition
     passive_nodes_per_chain = K.passive_node_count_per_chain
     # gamora seam discretion on whether to use empirical D71 budget (~70) or per-kit-ceiling-derived budget

  3. Branch on profile:

     IF P == low:
       budget_fraction = gamora_seam_low_threshold     # default suggestion: 0.20
       Apply low_distribution rule per § 10.2.1
       T4_unlocked = False                             # chain_progress < 0.70 per § 9

     ELIF P == mid:
       budget_fraction = gamora_seam_mid_midpoint      # default suggestion: 0.50
       Apply mid_distribution rule per § 10.2.2
       T4_unlocked = (chain_progress(primary_chain) >= T4_UNLOCK_THRESHOLD)
                                                       # typically True at mid-profile upper range

     ELIF P == max:
       budget_fraction = 1.0                           # all-skills-max (Mode A; calibration anchor)
       Apply max_distribution Mode A per § 10.2.3
       T4_unlocked = True                              # max-profile by construction unlocks T4

     ELIF P == max_realistic:                          # Phase 4 specialization-variance check
       budget_fraction = gamora_seam_max_realistic_threshold   # default suggestion: 0.75-0.85
       Apply max_distribution Mode B per § 10.2.3
       T4_unlocked = True

     ELIF P == mixed:
       Apply mixed_distribution rule per § 10.2.4 (variant V):
         IF V == passive_heavy: apply mixed_variant_1
         ELIF V == active_heavy: apply mixed_variant_2
         ELIF V == supporting_chain_heavy: apply mixed_variant_3
       T4_unlocked = (chain_progress(primary_chain) >= T4_UNLOCK_THRESHOLD)
                                                       # per-variant computation; Variant 2 likely True; Variants 1+3 likely False

  4. Validate per-node constraints:
     For each active node S in distribution:
       assert 0 <= S.investment_points <= NODE_MAX.active        # = 15
     For each passive node P in distribution:
       assert 0 <= P.investment_points_passive <= NODE_MAX.passive  # = 5
     Validate chain-prerequisite gates per Pattern A-deep verdict:
       For each non-T1 active skill node S in chain C:
         upstream_invested = sum of S.investment_points across upstream-tier nodes in C
         if S.investment_points > 0:
           assert upstream_invested >= 3                          # chain-prerequisite gate (Pattern A-deep)

  5. Validate construction property (Patterns 1+2):
     For max-profile Mode A (calibration anchor):
       For each active node: assert investment_points == 15      # Pattern 1 multiplier = 1.0 by construction
       For each passive node: assert investment_points_passive == 5  # Pattern 2 magnitude = 1.0 by construction

  6. Emit distribution → consumed by Pattern 1 (`damage_multiplier_at_points`) and Pattern 2 (`effect_magnitude_at_points`) at per-skill emitter

RETURNS: distribution
```

**Algorithm cross-references:**
- chain_progress computation per § 9.2
- T4_UNLOCK_THRESHOLD = 0.70 per § 9.2
- chain-prerequisite gates (≥3 points upstream-tier) per `2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` § "Chain-prerequisite gates"
- NODE_MAX source: `reincarnated-loadout/src/data/cycle13Types.ts:255`
- D66 active identity discipline: ONE T4 unlocked at a time
- D83 supporting chain T3-only architecture (closeout § 1.4)
- D71 endgame budget anchor ~70 points (closeout § 1.5)

**Construction property (Patterns 1+2 max-investment behavior):**

The algorithm preserves the Patterns 1+2 construction property at max-profile Mode A (calibration anchor):

```
At max-profile Mode A:
  For Pattern 1: every active skill node S has S.investment_points = NODE_MAX.active = 15
    → damage_multiplier_at_points(S, 15) = base_at_max × ((1 - 0.65) + 0.65 × 15/15)
                                          = base_at_max × (0.35 + 0.65)
                                          = base_at_max × 1.0  ✓ construction preserved
  For Pattern 2: every passive node P has P.investment_points_passive = NODE_MAX.passive = 5
    → effect_magnitude_at_points(P, 5) = base_at_max × ((1 - 0.50) + 0.50 × 5/5)
                                        = base_at_max × (0.50 + 0.50)
                                        = base_at_max × 1.0  ✓ construction preserved
```

This is the Discipline #47 § 7.2 max-investment proof: at calibration anchor, Patterns 1+2 multipliers are uniformly 1.0; specialization peaks emerge solely from `base_at_max(P, K, T)` distribution. Phase 3d gamora BASE re-derivation operates with confidence that the calibration anchor profile is a single canonical construction.

### 10.4 Phase 4 multi-profile sweep — operational composition

Phase 4 gamora multi-profile sweep consumes the § 10.3 algorithm to construct profile distributions per (kit × profile × variant) tuple. The sweep evaluates ~ (4 paths × 4 cohorts × 6 encounter types × 4 profile bins × mixed-variant expansion) cells per § 12.5; each cell evaluates the kit at its constructed distribution against the doc 50 § 4 5 targets.

**Coordination signal at Phase 4 firing (KR routes per Matt D4):**
- Reference: doc 51 § 10.2 multi-profile distribution rules (this section)
- Reference: doc 51 § 10.3 per-profile point allocation algorithm
- Reference: doc 51 § 10.1 max-profile Mode A as calibration anchor (gandalf recommendation; gamora seam discretion to override per Matt D2)
- Per-profile cell evaluation per § 10.2.{1,2,3,4}

**Coordination signal at Phase 3d firing (KR routes per Matt D3):**
- Reference: doc 51 § 10.1 Option A vs Option B decision (gandalf RECOMMENDS Option A; gamora seam discretion per Matt D2)
- If gamora adopts Option A: Phase 3d BASE re-derivation operates at max-profile Mode A per § 10.2.3 + § 10.3
- If gamora overrides to Option B: gamora records the override decision + rationale in gamora math note; Phase 4 sweep then uses Option B as calibration anchor + Mode A as variance check (inverse of recommendation)

### 10.5 Why the 4-profile-with-mixed-variant partition (and not a continuous percentile sweep)

The 4-category partition + 3-variant mixed expansion is BOUNDED by Phase 4 sweep complexity (~384 cells per § 12.5; mixed variants expand to ~768 cells). A continuous percentile sweep would explode the cell count without proportional design-signal gain.

The 4 conceptual labels mirror genre progression-phase vocabulary per § 6.2 (D2 leveling/mid/Hell/atypical; PoE campaign/yellow/red/meme; Last Epoch campaign/mid-monolith/300+/off-meta). Phase 4 calibration verifies bounded-viability AT the named phases the player will actually experience. Per-encounter-type cohort_median is the validation target at each phase.

**Mixed-profile is the design's "your unconventional build is viable" floor verification.** Without explicit mixed-profile sweep, Target 5 (≥30% cohort_median floor) becomes UNVERIFIED for the players who explicitly chose unconventional builds. The 3 mixed variants cover the substantive unconventional patterns; additional variants are Cycle 15+ scope.

### 10.6 Composition with § 9 T4_UNLOCK_THRESHOLD

At sub-max profiles, some chains have chain_progress < T4_UNLOCK_THRESHOLD = 0.70 per § 9.2. Per § 9.4 Cycle 14 v1 close model, Phase 4 sweep evaluates kits as if every chain's T4 is calibration-available — the unlock gate is Cycle 15+ Pattern 3 runtime overlay that does not change the calibrated `base_at_max`.

For Phase 4 telemetry, the sweep records per-profile chain_progress per chain and the implied T4-unlocked-state under § 9.2 enforcement, BUT the KPM evaluation includes T4 contribution at every profile (calibration is the upper-bound reference). Cycle 15+ Pattern 3 implementation later overlays the gate at runtime; the calibrated `base_at_max` values from Phase 3d + 4 stand.

---

## 11. Cross-references updated

The following docs require cross-reference updates at session close (Phase 2 acceptance criteria):

| Doc | Update | Section |
|---|---|---|
| `canonical/00-ground-state.md` | Add this doc (51) as new CURRENT entry in § 1 Current Truth table; one-line description (TL;DR-derived) | § 1 |
| `canonical/02-roadmap.md` | Reference Cycle 14 trajectory (Patterns 1+2 Phase 3 implementation); add Patterns 3-6 as Cycle 15+ design surfaces | Cycle 14 v1 / Cycle 15+ sections |
| `canonical/47-damage-scaling-architecture-2026-05-27.md` | Add forward-link at § 3 to this doc (the `skill_damage_multiplier` and `skill_damage_multiplier_at_points` composition layer) | § 3 (composes with the existing doc 50 forward-link in same section) |
| `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` | Add composition note: Patterns 1+2 (this doc) operate at the per-node investment layer; bounded-viability validation targets are evaluated at max-investment-profile (cohort_median calibration anchor) | § 4 + § 5 |

Cross-reference updates LANDED in this Phase 2 commit per master scoping § 1 Phase 2 acceptance criterion.

**Second iteration (§§ 9 + 10 amendment batch) cross-reference verification:**

| Doc | Verification | Status |
|---|---|---|
| `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 | Forward-link to doc 51 retained; no breaking changes from §§ 9 + 10 additions (the `skill_damage_multiplier` composition layer per § 3.3 unchanged) | PASS — no amendment required |
| `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4.7 | Composition note retained; bounded-viability validation targets evaluated at max-investment-profile per § 10.1 Mode A calibration anchor still aligns with doc 50 framing | PASS — no amendment required |
| `canonical/00-ground-state.md` § 1 | Doc 51 entry updated to reference v1.1 second iteration scope (§§ 9 + 10) | PENDING — knight-rider state-file maintenance routine post-tag |
| Internal references in this doc to §§ 9, 10, 11, 12 | Renumbered: old § 9 → new § 11; old § 10 → new § 12; old § 11 → new § 13; old § 12 → new § 14; cross-doc-internal references to those sections updated in-line | PASS |

No breaking-change cross-reference invalidations from §§ 9 + 10 additions. Patterns 1+2 formula structures (§§ 3 + 4) unchanged; calibration anchor decision (§§ 3.5 + 4.5) unchanged; per-tier ratio (§ 5) unchanged; Discipline #47 verification (§ 7) unchanged; Patterns 3-6 stubs (§ 8) unchanged.

---

## 12. Forward-link to Phase 3+4+5+6 work-streams

### 12.1 Phase 3a — rocket Pattern 1 implementation

**Owner:** rocket (foundation seam)
**Scope:** active skill damage scaling per § 3 of this doc; `per_skill_emitter.py` + `damage_resolver.py` touched
**Math note required:** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-phase-3-pattern-1-2026-05-28.md`; captures formula structure + application-order specification (Option A per § 3.3) + composition with W-α3 calibration semantics
**Acceptance:** Pattern 1 multiplier produced at `points / NODE_MAX_active` query; cohort_median at max-investment matches `base_at_max`; floor at points=0 is 0.35 × `base_at_max`
**Tag:** `rocket/v1.9-w-alpha-7-plus-pattern-1-1` (master scoping § Phase 3a)

### 12.2 Phase 3b — rocket Pattern 2 implementation

**Owner:** rocket (foundation seam)
**Scope:** passive skill effect scaling per § 4 of this doc
**Math note required:** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/w-alpha-7-plus-phase-3-pattern-2-2026-05-28.md`; captures formula structure + per-effect-type composition (stat bonus / DR / proc-rate / magnitude)
**Acceptance:** Pattern 2 magnitude produced at `points / NODE_MAX_passive` query; cohort_median at max-investment matches `base_at_max`; floor at points=0 is 0.50 × `base_at_max`
**Tag:** `rocket/v1.10-w-alpha-7-plus-pattern-2-1` (master scoping § Phase 3b)

### 12.3 Phase 3c — gamora encounter HP rebalancing (case 10 resolution)

**Owner:** gamora (simulation seam)
**Scope:** per-encounter HP factors in `endgame_mob_stat_profile.py` adjusted to escape fight-engine 0.1s timing floor for low-HP encounter types (open_arena / chokepoint_corridor / magic_pack / elite_pack); mini_boss + boss_with_adds factor ranges re-evaluated to ensure T4 specialization peaks at 1.5-2.0× cohort median become achievable
**Acceptance:** post-rebalance W-α6-style sweep produces 18-kit KPM differentiation (not all-600 uniform) on swarm encounter types; T4 specialization peaks achievable at 1.5-2.0× cohort_median per Discipline #47 Target 4
**Tag:** `gamora/v2.9-w-alpha-7-plus-phase-3-encounter-hp-rebalance-1` (master scoping § Phase 3c)

### 12.4 Phase 3d — gamora BASE_DAMAGE_L50 re-derivation

**Owner:** gamora (simulation seam)
**Scope:** under new W-α7+ formulas (Patterns 1+2 implemented) + new encounter HP (Phase 3c landed) + per-investment-profile reference targets; replaces W-α3 Phase 2 calibrated values (scaffold per Matt D1)
**Calibration anchor profile:** Option A — all-skills-max (gandalf RECOMMENDATION per § 10.1; gamora seam discretion to override per Matt D2). If Option A adopted, Phase 3d operates at max-profile Mode A per § 10.2.3 + § 10.3 construction algorithm.
**Acceptance:** per-tier 1:1.5:2.17:4.0 ratio preserved at cohort-output layer under max-investment-profile per § 5.3 of this doc; per-path base DPS variance ≤1.5× per doc 50 § 4 Target 1; calibration anchor profile decision recorded in gamora math note
**Tag:** `gamora/v2.10-w-alpha-7-plus-phase-3-base-rederivation-1` (master scoping § Phase 3d)

### 12.5 Phase 4 — gamora multi-dim calibration

**Owner:** gamora (simulation seam)
**Scope:** calibration target = bounded-viability across paths × cohorts × encounter_types × investment_levels = ~4 × 4 × 6 × 4-profile = ~384-cell base space (mixed-variant expansion to ~768 cells per § 10.2.4); binary search across expanded space; verify cross-path parity ≤1.5× at multiple investment profiles per doc 50 § 4.1
**Distribution rules per profile:** § 10.2 multi-profile distribution rules (low / mid / max / mixed) consumed for cell construction; § 10.3 per-profile point allocation algorithm executed per (kit × profile × variant) tuple
**Acceptance:** all 5 doc 50 targets satisfied at max-profile AND aggregate compound across profiles; Target 5 (≥30% cohort_median floor) verified at low-profile + mixed-profile per § 10.2.1 + § 10.2.4
**Tag:** `gamora/v2.11-w-alpha-7-plus-phase-4-multi-dim-calibration-1` (master scoping § Phase 4)

### 12.6 Phase 5a — gamora BVV harness multi-dim update

**Owner:** gamora (simulation seam)
**Scope:** harness measures across multi-dimensional space (paths × cohorts × encounter_types × investment_levels); per-profile compound_pass + aggregate compound_pass
**Tag:** `gamora/v2.12-w-alpha-7-plus-phase-5a-bvv-multi-dim-1` (master scoping § Phase 5a)

### 12.7 Phase 5b — drax loadout UI revival

**Owner:** drax (loadout app seam)
**Scope:** NODE_MAX surfaces become MECHANICALLY MEANINGFUL post-Phase-3 implementation; loadout UI displays investment-scaled output (per-skill point delta visible)
**Composition with this doc:** drax consumes Pattern 1 + Pattern 2 formulas via Phase 3 schema additions; the per-point multiplier displayed in UI is the Pattern 1/2 result at the player's current investment
**Tag:** `drax/v1.2-w-alpha-7-plus-phase-5b-loadout-investment-ui-1` (master scoping § Phase 5b)

### 12.8 Phase 5c — gamora Wave 5 RE-FIRE

**Owner:** gamora (simulation seam)
**Scope:** full production season under composite engine state (Path α + integrated W-α7+ + R5-Plus scrub + Phase 5 LLM naming); Bundle Gate-2 multi-coverage
**Tag:** `gamora/v2.13-w-alpha-7-plus-phase-5c-wave-5-refire-1` (master scoping § Phase 5c)

### 12.9 Phase 6 — final close

**Owner:** jack-ryan + gandalf + Matt
**Scope per master scoping § Phase 6:** disciplines #41-#46 batched canonical-write + A/B comparison + Matt v1 ratification

---

## 13. Discipline #45 vocabulary grep audit

### 13.1 First iteration audit (Phase 2 lock; 2026-05-28)

**Prohibited terms checked:** class / per-class / class roster / class taxonomy / class-intrinsic / class-naming policy / archetype / role.

**Grep audit of first-iteration scope (§§ 1-8 + original §§ 9-12):**

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

**Exempt occurrences:** none required exempting in the first iteration.

**Cohort labels used in this doc** (`DPS-min-maxer / Balanced / Defensive / Hybrid`): these are mechanical-property descriptors inherited from W-α6 `COHORT_KPM_BAND` / doc 50 § 5 framing. They are NOT generative-input taxonomy labels; they describe per-build mechanical fingerprints emerging from kit substrate. Per Discipline #45 scope exemption: "Describe the mechanical property directly" — these labels describe DPS/defense balance properties, not pre-authored generative taxonomy. EXEMPT.

**First iteration verdict:** PASS — zero non-exempt prohibited-vocabulary usage.

### 13.2 Second iteration audit (§§ 9 + 10 amendment batch; 2026-05-28 evening)

**Re-audit performed on new content in §§ 9 + 10 (KNOWN-GAP T4_UNLOCK_THRESHOLD + investment-profile distribution rules).**

**Grep results for new content:**

| Term | Occurrences in §§ 9 + 10 | Status |
|---|---|---|
| `class` | 0 in generative-architecture content; 0 in algorithm pseudocode; 0 in acceptance criteria; 0 in player-experience framing | PASS |
| `per-class` | 0 | PASS |
| `class roster` | 0 | PASS |
| `class taxonomy` | 0 | PASS |
| `class-intrinsic` | 0 | PASS |
| `archetype` | 0 as generative-input label | PASS |
| `role` | 0 as pre-authored taxonomy | PASS |

**Exempt occurrences in §§ 9 + 10:**

| Term | Context | Exemption basis |
|---|---|---|
| `"category"` in § 9.3 (item 3 "Pattern 3 implementation scope... vocabulary") and § 10.5 ("4-category partition") | "category" describes the 4-bin profile partition (low/mid/max/mixed), not generative units | EXEMPT — "category" is partition-vocabulary, not taxonomy-vocabulary; the partition describes per-profile mechanical state, not pre-authored kit shape |
| Chain-position references (`primary` / `secondary` / `supporting` chain references in § 10.2) | Chain-position descriptors per doc 40 D83 + closeout § 1.4 | EXEMPT — chain-position is substrate-emergent per kit composition (rocket Phase 2a output), not pre-authored generative taxonomy |

**Prohibited-vocabulary substitutions made during second iteration:**

The original prior-exchange reference at closeout § 2.1 used the legacy "class identity" framing; § 10.2.2 references this prior record but substitutes "kit-identity floor" + "foundational passives" per Discipline #45. The substitution preserves the substantive design content (supporting chain absorbs kit-baseline passives) while honoring the current vocabulary lock. The historical record at closeout § 2.1 remains as written per Discipline #40 case (c) retraction-procedure § 6 (anchored examples remain readable).

**Second iteration verdict:** PASS — zero non-exempt prohibited-vocabulary usage in §§ 9 + 10 amendment scope. The new content operates strictly in mechanical/structural-intent vocabulary (kit / chain / skill / node / pattern / profile / threshold / investment / distribution / variant / mode).

### 13.3 Composite verdict

**PASS — first iteration + second iteration both clean.** Doc 51 v1.1 second iteration introduces zero new Discipline #45 violations. Reciprocal cross-check: the new vocabulary introduced (`T4_UNLOCK_THRESHOLD` / `chain_progress` / `low_distribution` / `mid_distribution` / `max_distribution` / `mixed_distribution` / `mixed_variant_1` / `mixed_variant_2` / `mixed_variant_3` / `construct_profile_distribution`) is mechanical-algorithm vocabulary; future cross-references cite these by name as Cycle 15+ Pattern 3 implementation vocabulary anchors.

---

## 14. Acceptance criteria (Phase 2 close + scope-completeness amendment batch close)

### 14.1 First iteration acceptance (Phase 2 lock; commit `ba1c4e7`)

Per master scoping § 1 Phase 2 acceptance:

- [x] **Pattern 1 active skill damage scaling formula specified** — linear-with-floor `base_at_max × ((1 - decay) + decay × (points / 15))` with decay=0.65 per § 3.2; composition with doc 47 § 2.2 damage equations specified per § 3.3
- [x] **Pattern 2 passive skill effect scaling formula specified** — linear-with-floor `base_at_max × ((1 - decay) + decay × (points / 5))` with decay=0.50 per § 4.2; composition with passive-effect targets specified per § 4.3
- [x] **Discipline #47 verification** — peak KPM ratios within [1.5, 2.0] × cohort median at max investment per § 7 (formal proof via Pattern 1 max-multiplier=1.0 producing peaks at calibrated `base_at_max`; Phase 3d gamora BASE re-derivation determines per-kit per-encounter peak distribution)
- [x] **Calibration anchor decision** — max-investment for both patterns per § 3.5 + § 4.5; rationale captured per § 6.4 (cohort_median represents endgame-realized character profile)
- [x] **Per-tier ratio preservation: 1:1.5:2.17:4.0** — preservation mechanism per § 5.3 (tier_coefficient is outer-layer; investment scaling at points=max produces multiplier=1.0 which preserves ratios uniformly); composition with bounded-viability constraints per § 5.4
- [x] **Per-encounter-type band design integrated** — W-α6 ENCOUNTER_COHORT_KPM_BAND structure preserved per § 0 TL;DR + § 7.3; recalibrated values under multi-dim space land in Phase 4; case 10 timing-floor constraint acknowledged with Phase 3c encounter HP rebalancing as resolution path
- [x] **Profile semantic definitions** — low / mid / max / mixed-profile semantics per § 6.1-6.4; numeric thresholds = Phase 3+4 gamora seam discretion per § 6.3
- [x] **6-pattern canonical doc** — Patterns 1+2 detailed (§ 3 + § 4); Patterns 3-6 canonical-locked stubs (§ 8.1-8.4); Patterns 7+ deferred
- [x] **Cross-references updated** — doc 00 + doc 02 + doc 47 § 3 + doc 50 per § 11 (in-flight this Phase 2 commit)
- [x] **NODE_MAX source location verified** — `reincarnated-loadout/src/data/cycle13Types.ts:255` (lines 255-259: passive=5, active=15, t4=1) per § 3.1 + § 4.1
- [x] **Discipline #45 vocabulary grep audit PASS** — § 13.1

### 14.2 Second iteration acceptance (§§ 9 + 10 amendment batch; 2026-05-28 evening)

Per KR dispatch `agentic_orchestration/dispatches/2026-05-28-gandalf-doc-51-scope-completeness-amendment-batch.md` § 4 acceptance:

- [x] **§ 9 KNOWN-GAP T4_UNLOCK_THRESHOLD acknowledgment authored** — T4_UNLOCK_THRESHOLD = 0.70 captured per § 9.2 from prior gandalf+Matt design exchange (`2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.5 D71); Cycle 15+ deferral rationale per § 9.3; Pattern 3 implementation cross-reference per § 9.6; composition with Patterns 1+2 at Phase 3d + Phase 4 per § 9.4; branched-chain T4-unlock per § 9.5; acknowledgment statement per § 9.7
- [x] **§ 10.1 calibration anchor profile decision authored** — Option A (all-skills-max) vs Option B (realistic-max specialization-aware) trade-off table per § 10.1; gandalf RECOMMENDATION = Option A with 5-point rationale (structural cleanness + specialization-as-emergent + genre precedent + Phase 4 reference baseline + player-consequence framing); gamora seam discretion to override per Matt D2
- [x] **§ 10.2 multi-profile distribution rules authored** — low-profile distribution rule per § 10.2.1; mid-profile per § 10.2.2; max-profile (Mode A + Mode B) per § 10.2.3; mixed-profile (3 variants) per § 10.2.4
- [x] **§ 10.3 per-profile point allocation algorithm authored** — concrete pseudo-code algorithm `construct_profile_distribution(K, P, V)` per § 10.3 with per-profile branch + per-node constraint validation + chain-prerequisite gate validation + max-profile Mode A construction property preservation; cross-references to § 9.2 (chain_progress + T4_UNLOCK_THRESHOLD) and Pattern A-deep chain-prerequisite gates
- [x] **Header amended** — STATUS notice updated to "second iteration"; `**Date**` field extended; `**Status**` field updated to "v1.1 canonical lock SECOND ITERATION"; `**Authority**` field extended with second iteration record
- [x] **Discipline #45 vocabulary grep re-audit on new content** — PASS per § 13.2; exempt occurrences declared
- [x] **Cross-reference verification** — doc 50 § 4.7 + doc 47 § 3 forward-link blocks still valid; no breaking-change cross-reference invalidations from §§ 9 + 10 additions per § 11 second iteration table
- [x] **Tag cut** — `gandalf/v1.15-doc-51-scope-completeness-amendment-batch-1` (seam discretion per dispatch § 2)
- [x] **Discipline #40 case (c) extension framing** — captured in header authority block; this is scope-completeness fold-in to LOAD-BEARING canonical, NOT retraction (no retraction-procedure 6-step sequence required)
- [x] **Discipline #48 candidate validation at N=2** — referenced in header authority block + commit message (case 11 investment scaling gap + case 13 this § 10 distribution rules gap); minting deferred to Phase 6a disciplines batch per jack-ryan

---

## Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-28 (first iteration); 2026-05-28 evening (second iteration §§ 9 + 10 amendment batch)
**Status:** v1.1 canonical lock SECOND ITERATION; LOAD-BEARING per integrated W-α7+ Phase 2 + Matt 2026-05-28 evening D1+D2+D3+D4 RATIFICATION; gates Phase 3d gamora BASE re-derivation + Phase 4 multi-profile sweep + Phase 5+6 work-streams; Cycle 14 v1 close trajectory ~14-22d from Matt 2026-05-28 evening RATIFICATION AMENDMENT
**Authority — first iteration:** Matt 2026-05-28 evening RATIFICATION AMENDMENT (integrated W-α7+ replaces separate Option B + W-α7) + Phase 2 firing PARALLEL with jack-ryan Gate-1 review per Matt explicit authorization
**Authority — second iteration:** Matt 2026-05-28 evening D1+D2+D3+D4 RATIFICATION (scope-completeness amendment batch §§ 9 + 10) per KR dispatch `agentic_orchestration/dispatches/2026-05-28-gandalf-doc-51-scope-completeness-amendment-batch.md`; Discipline #40 case (c) extension protocol (NOT retraction; scope-completeness fold-in to LOAD-BEARING canonical); Phase 3d gamora HALTED via TaskStop pending § 10.1 calibration anchor profile decision lock
**Discipline #45 vocabulary audit:** PASS per § 13 — zero non-exempt prohibited-vocabulary usage (first iteration per § 13.1 + second iteration §§ 9 + 10 per § 13.2; composite verdict per § 13.3)
**Discipline #47 verification:** § 7 specifies peak-KPM-ratio framework; max-investment multiplier=1.0 by construction; specialization peaks emerge from `base_at_max` distribution (Phase 3d gamora seam); within [1.5, 2.0] × cohort_median target preserved; § 10.3 construction property preservation extends verification to per-profile distribution algorithm
**Discipline #48 candidate validation status:** N=2 production gaps confirmed (case 11 investment scaling gap → first iteration scope; case 13 § 10 distribution rules gap → second iteration scope); both caught by Matt manual scope-completeness audit; minting deferred to Phase 6a disciplines batch per jack-ryan
**Discipline #1 (math-before-code) target:** Phase 3a + 3b + 3c + 3d math notes required at `~/Games/reincarnated-engine/src/reincarnated/{generation,simulation}/math/` per master scoping § Phase 3 sub-streams; each math note cites this doc § 3 / § 4 / § 5 / § 7 / § 10 by section number as the design-spec-as-math handoff
**Cross-references:** doc 00 (ground-state oracle — registration first iteration; second iteration entry refresh pending knight-rider state-file maintenance); doc 02 (roadmap — Cycle 14 trajectory + Patterns 3-6 Cycle 15+ surface); doc 47 § 3 (mechanical substrate; forward-link unchanged at second iteration per § 11); doc 50 (composition with bounded-viability constraints; cross-reference unchanged at second iteration per § 11); master scoping dispatch (parent first iteration); scope-completeness amendment dispatch (second iteration parent); W-α6 math note (Phase 1 input absorbed); NODE_MAX source `reincarnated-loadout/src/data/cycle13Types.ts:255`; engineering-disciplines.md § 45 (vocabulary lock audit anchor) + § 47 (bounded-viability framework discipline) + § 40 case (c) (extension protocol for LOAD-BEARING canonical amendment); prior gandalf+Matt design exchange records `2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.5 D71 + `2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` § "Chain-prerequisite gates" (§ 9 KNOWN-GAP T4_UNLOCK_THRESHOLD provenance)

**For:** the structural-intent layer over the skill-tree per-node investment domain. Phase 3 implementation (rocket Patterns 1+2; gamora BASE re-derivation + encounter HP rebalancing) consumes § 3 + § 4 + § 5 + § 7. Phase 3d gamora BASE re-derivation additionally consumes § 10.1 calibration anchor profile decision + § 10.3 max-profile Mode A construction algorithm. Phase 4 multi-profile sweep consumes § 6 profile definitions + § 10.2 multi-profile distribution rules + § 10.3 per-profile point allocation algorithm. Phase 5 BVV harness validates § 7 Discipline #47 framework. Cycle 15+ Pattern 3 implementation consumes § 9 T4_UNLOCK_THRESHOLD = 0.70 acknowledgment + § 9.4-9.6 composition + deferral logic. From this commit forward, "Pattern 1 active skill damage scaling" and "Pattern 2 passive skill effect scaling" are the canonical vocabulary; downstream dispatches, math notes, and decisions-log entries cite them by name. T4_UNLOCK_THRESHOLD = 0.70 is the named canonical Pattern 3 vocabulary anchor for Cycle 15+. The game we ship is the game where every invested point matters AND every player's build is in the band at endgame AND every chain's capstone is earned, not given.
