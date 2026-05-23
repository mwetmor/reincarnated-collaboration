# Per-Tier Recompose Validation — Canonical Findings (recompose-validation hive P3 synthesis)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** Canonical-story doc. P3 deliverable per `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` § 3 P3 + dispatch `agentic_orchestration/dispatches/2026-05-20-gandalf-plus-jack-ryan-p3-validation-synthesis.md` § 3.1.

**Author:** gandalf (story-and-design steward).
**Date:** 2026-05-20.
**Authority:** AUTONOMOUS L2-equivalent per engine-rebuild protocol § 4.0 (Architectural / load-bearing cross-cutting decisions — gandalf decides; verdict-call is not escalation-eligible).
**Predecessor artifacts:** P0 (Option A floor widening — engine `a58b60f`); P1 (Option B MECHANICALLY COMPLETE / BEHAVIORALLY SOFT-DISABLED — engine `22b1c3c`); P2 (rocket Phase 1 `07d13f8` + gamora Phase 2 `6cb7fa4` + star-lord Phase 3 `46d850c`).
**Verdict gate:** scope-of-work § 1 thresholds (≥ 80% kit-acceptable → PASS strong; 60-80% → PASS moderate; < 60% → CANNOT REJECT NULL).
**Sign:** Mithrandir.

**Amended:** 2026-05-20 per jack-ryan Gate-2 critique — 2 REQUIRED + 1 RECOMMENDED amendments folded:
- A1 (REQUIRED): recompose_attempts count corrected 33 → 35
- A2 (REQUIRED): § 6 sub-pattern 5 + § 6.1 class_0001 note disaggregated (compression-only vs lever-signal-gap)
- A3 (RECOMMENDED): § 0 TL;DR substrate scope parenthetical added

---

## § 0 — TL;DR + Verdict

**Verdict: CANNOT REJECT NULL.** Hypothesis H_RC ("per-tier convergence is satisfiable for existing generation rules if recompose can fire") is **not supported** by season_100005 empirical evidence. Null hypothesis H_RC_0 ("even with recompose unblocked, per-tier convergence does not produce shippable kits — generation rules require revision") is **not refuted**, and is in fact reinforced by an unambiguous data shape: 0% kit-acceptable, 100% kit-broken, 100% Pattern-A (boss-DPS-floor structural), 0/10 floor-lock-recovery candidates (on shadow substrate seed=100005 under disposition-3 calibration). The empirical figure is far below the < 60% CANNOT REJECT NULL threshold — it is 0%.

This is **not a hive failure.** Per protocol § 11 ("If H_RC fails, we have the cleanest possible diagnosis of where the actual pathology lives — and the next architectural decision becomes obvious"), the hive has produced exactly that: Option A's mechanism is verified (prior floor-lock failure mode IS eliminated); Option B's mechanism is verified mechanically (unit tests + production-path round-trip) but its served population is empirically absent at full-season scope on shadow substrate; the load-bearing diagnosis is now unambiguously **kit-composition pathology at the boss + mini-boss tiers**. The recompose mechanism cannot fix kit composition that lacks fundamental boss-kill capability — and at season_100005, every class lacks it.

**Recommendation:** wind-down trigger #3 signals at P3 per scope-of-work § 1 + protocol § 7. Hive deactivates pending Matt direction. The natural next-step architectural decision for Matt's consideration is **kit-redesign queue execution** per `canonical/story/r1-kit-redesign-queue-2026-05-19.md` — empirically corroborated at full-season scope by this hive's P2 evidence; previously surfaced by R2+ST counterfactual joint synthesis Row 5 ("catalogue has deeper pathology") and the 38/51 broken-kits finding earlier this week. The hive does not commit Matt to that path; it surfaces the recommendation transparently.

---

## § 1 — Hive mission recap

### § 1.1 — What was tested

The recompose-validation hive's mission (per scope-of-work § 0) was to *validate that per-tier WR convergence with the recompose mechanism unblocked produces a shippable season under the new tuning contract; ship a true season under that mechanism if validation succeeds.*

The architectural insight from engine-rebuild Phase D (AMENDED with Matt's methodological correction; see `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` § 8):

> *We were running a fully converged season (tuned for old aggregate-mean contract) against a new tuning mechanism (per-tier WR bands) and asking "why doesn't this tune?" The single modifier scalar can't bridge the contract mismatch. The recompose mechanism IS the bridge that varies kit composition — but it's been architecturally blocked by the floor-lock since per-tier targets were authored. Unblock recompose → recompose can operate → kits naturally converge to per-tier targets.*

### § 1.2 — H_RC vs H_RC_0

Per scope-of-work § 1:

- **H_RC (recompose-as-lever):** *Per-tier WR target convergence is satisfiable for the existing generation rules — IF the recompose mechanism can fire. Composition variation that recompose produces is the lever that bridges the contract mismatch.*
- **H_RC_0 (null):** *Even with recompose unblocked, per-tier convergence does not produce shippable kits. Generation rules require revision.*

### § 1.3 — PASS thresholds

| Outcome | Threshold | Disposition |
|---|---|---|
| PASS strong | ≥ 80% kit-acceptable | Ship true season (P4); declare mechanism validated |
| PASS moderate | 60-80% kit-acceptable | Ship partial; flag failures for kit-redesign queue |
| CANNOT REJECT NULL | < 60% kit-acceptable | Surface to Matt (wind-down trigger #3) |

**Test instrument:** P2 fresh diagnostic regen (cold-start canonical convergence on a full-roster season under Option A + Option B engine state); P3 synthesis (this document).

---

## § 2 — P0 outcome (Option A floor widening)

**Disposition:** SHIPPED 2026-05-19; engine `a58b60f`; tags `gamora/v1.13-balance-loop-floor-widened-option-a` + `recompose-hive/v0.1-option-a-floor-widened`.

**Mechanism delivered:** `MODIFIER_SEARCH_FLOOR` widened from 0.05 → 0.01; named-constant introduced per Discipline #18 with full module-level docstring; `MODIFIER_SEARCH_CEILING = 4.0` paired; `modifier_extreme_low` telemetry flag added (schema v2.12); 4 inline literal sites updated to use the named constants; `tests/test_range_profile.py` literal-floor assertion updated to reference `MODIFIER_SEARCH_FLOOR`.

**Empirical validation:**
- Stop-gap warm-start regen on 3 diagnostic seasons (099002 / 100001 / 100002): 24/31 classes that previously failed at floor=0.05 now converge under floor=0.01 (FAILED → CONVERGED, all 31 classes).
- Cold-start canonical confirmation deferred to P2; P2 cold-start observed equilibrium modifiers `m* ∈ [0.0719, 0.3812]` on season_100005 — all above the new floor=0.01, all below the old floor=0.05. **The prior floor-lock failure mode is empirically eliminated.**

**Verdict on P0 mechanism:** Option A's mechanism is correct and ships its intended unblock. The 22 Pattern-B classes from Phase B.2 with `m* ∈ [0.01, 2.0]` are now reachable. The architectural surgery did exactly what it was designed to do.

**What Option A does NOT do** (load-bearing for interpretation of P3 verdict): Option A unblocks *modifier reachability* — it does not change *what the converged modifier produces for per-tier WR*. A class whose true equilibrium modifier is 0.0719 (class_0002 fire_mage, P2 season_100005) now converges cleanly at that modifier — but at that modifier, boss WR is still 0.0. The floor-widening is **necessary but not sufficient** for shippable kits, and that distinction is the whole shape of the P3 verdict.

---

## § 3 — P1 outcome (Option B recompose-trigger conditioning)

**Disposition:** MECHANICALLY COMPLETE / BEHAVIORALLY SOFT-DISABLED 2026-05-19; engine `22b1c3c` + `554e310`; seam tag `gamora/v1.14-balance-loop-option-b-recompose-conditioned-soft-disable` (load-bearing `-soft-disable` qualifier); hive milestone tag `recompose-hive/v0.2-option-b-recompose-conditioned` HELD.

### § 3.1 — Mechanism delivered

Per gandalf brief v1.1 (`agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md`) + jack-ryan Gate-1 (APPROVE-WITH-AMEND, 4 required + 1 recommended + 1 optional, all folded):

- **Re-condition signal:** `last_wr > RECOMPOSE_SIGNAL_HI` (departure from gamora § 5.2's `eval_modifier ≤ floor + ε` — the brief's § 2.3 substitution is principled, jack-ryan-confirmed-clean, and architecturally symmetric for any future B-prime ceiling-lock extension).
- **Probe value:** `LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` (half the new floor; explicit Discipline #18 named constant; ~55-LOC docstring covering rationale, semantic shift, reversibility, cross-refs).
- **Module-level constants:** `RECOMPOSE_SIGNAL_LO = 0.30`, `RECOMPOSE_SIGNAL_HI = 0.70` (Amendment 1; single source of truth replacing local literals at two sites).
- **Telemetry:** schema v2.13 — `floor_lock_recompose: bool | None` on ClassBalanceResult; `working_modifier` + `floor_lock_detected` per `recompose_attempts` entry; `n_floor_lock_recompose_true` aggregate.
- **Fail-loud logging:** Amendment 2 — log.debug for the two edge cases (still-saturated at probe + over-suppressed at probe).
- **Test surface:** 4 unit tests added (Amendment 3); 179/179 PASS at implementation; 179/179 PASS at soft-disable.
- **MIGRATION.md:** v1.22 entry with explicit R11(b) round-trip clause + rocket informational watchpoint (Amendment 6).

### § 3.2 — Smoke B1 BLOCKING failure + test-class-selection diagnosis

Smoke B1 BLOCKING failed conditions 1 + 2 on class_0001 cold-start:
- Condition 1 (`floor_lock_detected=True` in any recompose_attempt): **FAIL** (no attempt fired the detection branch)
- Condition 2 (at least one attempt with `working_modifier=0.005`): **FAIL** (no branch fired so no probe value applied)
- Conditions 3 + 4 (lever traction at probe + post-recompose `modifier_extreme_low=False`): **PASS**

Root cause (Discipline #11 — empirical inspection over assumption): class_0001's true cold-start equilibrium `m* ≈ 0.072` — *above* MODIFIER_SEARCH_FLOOR = 0.01. The brief's v1.0 § 4.1 selection of class_0001 as canonical smoke subject rested on its warm-start signature (`modifier=0.0509` + saturated WR), which gamora's cold-start exposed as a TOLERANCE-satisfied-at-old-floor artifact, not a true equilibrium below floor. **Class_0001 is not in the masked-Pattern-B-extreme sub-population the smoke was designed to test.** The three test classes (0001 / 0003 / 0006) all cold-start above floor; 0/3 floor-lock detection rate.

The mechanism is verified independently (unit tests under controlled mocks confirm: `last_wr=0.98` → `floor_lock_detected=True` fires; `last_wr=0.55` → does not; production path through `ClassBalanceResult.floor_lock_recompose` is correct; telemetry round-trip with `eval_modifier` vs `working_modifier` separation works). The failure is a smoke-design issue, not a mechanism defect.

### § 3.3 — Soft-disable disposition (Option 2)

I re-dispositioned to Option 2 — soft-disable via `LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR` — over Option 1 (full revert) and Option 1' (fire-with-caveat; knight-rider's framing).

Three load-bearing governance principles surfaced by the re-disposition (decisions-log entry 2026-05-19 P1; hive log STATE `2026-05-19 EDT — gandalf STATE — P1 smoke-B1-FRICTION RE-DISPOSITION: OPTION 2 (SOFT-DISABLE)`):

1. **A BLOCKING smoke gate exists to falsify the design diagnosis, not the mechanism.** Smoke B1's failure mode "test class doesn't have the property the test was designed to check" is materially different from "mechanism is wrong." The dispatch's literal § 4.5 BLOCKING semantics did not distinguish these; v1.1 § 4.4 amendment tightens.
2. **Hive milestone tags do not fire on un-empirically-tested behavioral changes.** Tag-firing discipline as governance precedent.
3. **When your test arena lacks the monster you designed your synergy against, you fix the arena, not the synergy.** Diablo II Iron Maiden / Returned-Damage lesson. Full rollback would have thrown away 165 LOC of Gate-1-approved infrastructure for a test-design miss.

### § 3.4 — Brief v1.1 amendment + smoke-design discipline candidate

Brief v1.1 amendments (substance):
- § 4.1 explicit retrospective on the warm-start-signature error
- § 4.4 BLOCKING semantics tightened ("BLOCKING fails when smoke conditions fail AND post-hoc analysis confirms the test class actually has the property the smoke was designed to detect")
- § 9 Reversibility Option 2 elevated from "alternative" to "preferred path when smoke fails due to test-class-selection issues"

**Engineering-disciplines candidate (P1 finding):** *"Mandatory cold-start dry-run on any candidate canonical smoke test class before locking it as the canonical subject."* Discipline #11 (empirical inspection over assumption) elaboration. See § 9 below for the framing recommendation.

### § 3.5 — Verdict on P1 mechanism

Option B's mechanism is **mechanically correct** (unit tests verify the branch logic under controlled conditions; production path through schema v2.13 fields confirmed; 0/3 false-positive rate across cold-start triage; round-trip telemetry round-trips). Option B's **behavioral landing is unverified** at this hive's end — and per P2's empirical record (§ 4 below), the behavioral landing is *unverifiable from this season's evidence* because the served population (kits with true `m* < 0.01`) is empirically absent at full-season scope.

The soft-disable state is the correct end state for this hive. The mechanism remains a "sleeping safety net" — preserved infrastructure, instrumented telemetry, one-line re-enable cost — for a future season's evidence or a Matt-directed substrate-generalization study to either confirm or further refute the served population's existence.

---

## § 4 — P2 outcome (fresh diagnostic regen on shadow substrate, seed=100005)

**Disposition:** ACCEPTED 2026-05-20; tag `recompose-hive/v0.3-diagnostic-regen-complete` fired (engine + collab).

### § 4.1 — Phase 1 (rocket generation)

Engine `07d13f8`; tag `rocket/v1.22-p2-fresh-regen-shadow-100005`; substrate=shadow; seed=100005; R8 inverted pipeline; wall time 49.9 min. Cosmology: element='ember', anchor='The Bridge of Sighs Between Fires'. 10 classes generated; full canonical roster for shadow-first rotation. Trial defeat rate 52.8% at generation-time convergence. 44 monsters, 200 gear items (120 rare+).

**Generation-time embedded-balance-loop signal (rocket diagnostic table):** 6/10 classes reported `floor_lock_recompose=True`; 7/10 `modifier_extreme_low=True`. This is the **pre-canonical** signal that, on initial read, *appeared* to load-bearingly support the masked-Pattern-B-extreme hypothesis at ~60% rate (far above § 2.5's 3-8/season conservative estimate).

**This signal was incorrect** as a population-property estimator. See § 9 for the methodological finding.

### § 4.2 — Phase 2 (gamora cold-start balance convergence)

Engine `6cb7fa4`; tag `gamora/v1.15-p2-balance-convergence-shadow-100005`; cold-start (`initial_modifier=1.0` per class); 100 fights/matchup production-grade; 283.0s wall time across all 10 classes. Engine state at execution: Option A floor active (MODIFIER_SEARCH_FLOOR=0.01); Option B soft-disabled (LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR); disposition-3 calibration active (boss HP × 0.40, armor × 0.45, swarm HP × 3.5, 240s boss timeout, 150s mini-boss timeout).

**Cold-start canonical signal:**

| Metric | Count |
|---|---|
| Total classes | 10 |
| Converged (all 5 per-tier targets met) | 0/10 |
| Partially-converged | 10/10 |
| Failed_regenerate | 0/10 |
| `floor_lock_recompose=True` | **0/10** |
| `modifier_extreme_low=True` | 0/10 |
| Equilibrium modifier range observed | `m* ∈ [0.0719, 0.3812]` |

Gamora surfaced FRICTION (Phase 1 vs Phase 2 signal reversal: 6/10 → 0/10); root cause is the pipeline-state vs equilibrium-conditioned distinction (§ 9). FRICTION resolved cleanly within the same workflow.

### § 4.3 — Phase 3 (star-lord classification + floor-lock analysis)

Engine `46d850c`; tag `star-lord/v1.14-p2-classification-shadow-100005`; canonical analysis at `output/p2-fresh-diagnostic-regen-2026-05-19/p2-classification-and-floor-lock-analysis.md`.

**Floor-lock candidate count (canonical):** 0/10 across **35** recompose_attempts on 9 canonical classes (class_0001=3 attempts, classes 0002-0009=4 attempts each; experimental class_0010 NULL — correct per MIGRATION.md v1.22 spec). Cross-check via class-level `floor_lock_recompose` field: 0/9 (NULL on experimental). **The masked-Pattern-B-extreme sub-population is empirically absent from season_100005 at full-season scope on shadow substrate.**

**Kit classification (per gandalf brief § 2.5 carve):** 0 kit-acceptable / 0 kit-mediocre / **10 kit-broken**.

**Pattern A/B classification (per Phase B.2 + dispatch § 3.2 Phase 3):** **10/10 Pattern-A** (boss WR = 0.0 at converged modifier; lever-irrecoverable kit-composition pathology). 0/10 Pattern-B. 0/10 Pattern-B-extreme.

### § 4.4 — The shape of the data (load-bearing for verdict)

Per star-lord's analysis § 9 raw-data cross-reference (and § 4 classification):

- **Swarm tier:** WR ∈ [0.815, 1.000]. **All 10 classes over-perform** at converged modifier — kit is too easy at swarm tier. Structural over-power.
- **Magic tier:** WR ∈ [0.920, 1.000]. **All 10 classes over-perform.**
- **Elite tier:** 9/10 pass (most ∈ [0.45, 0.55]); 1/10 fails (class_0009 shadow_controller over-shoots at 0.670).
- **Mini-boss tier:** WR = 0.000 for **all 10 classes**. Zero mini-boss kills at converged modifier.
- **Boss tier:** WR = 0.000 for **all 10 classes**. Zero boss kills at converged modifier.

The per-tier shape is unambiguous: **lower tiers saturate; upper tiers (boss + mini-boss) collapse to zero.** This is the exact pattern Phase B.2's "saturate-low + collapse-boss" diagnosis described pre-recompose-validation — and the recompose mechanism's intended bridge does not fire because *the population that would benefit from it (true `m* < 0.01`) is empirically absent*. The pathology lives upstream of the modifier search and upstream of the recompose lever, at the kit-composition layer.

---

## § 5 — Per-class classification analysis

Consumed from star-lord's canonical analysis (`output/p2-fresh-diagnostic-regen-2026-05-19/p2-classification-and-floor-lock-analysis.md` § 4).

| class_id | archetype | element | final_modifier | swarm WR | magic WR | elite WR | mini-boss WR | boss WR | tier failures | classification |
|---|---|---|---|---|---|---|---|---|---|---|
| class_0001 | shadow_mage | shadow | 0.1956 | 1.000 | 1.000 | 0.495 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0002 | fire_mage | fire | 0.0719 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0003 | water_mage | water | 0.1338 | 1.000 | 0.955 | 0.500 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0004 | earth_caster | earth | 0.1338 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0005 | wind_caster | wind | 0.1338 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0006 | lightning_mage | lightning | 0.0719 | 1.000 | 1.000 | 0.535 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0007 | holy_caster | holy | 0.1338 | 1.000 | 0.985 | 0.500 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0008 | physical_warrior | physical | 0.3812 | 0.988 | 1.000 | 0.470 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |
| class_0009 | shadow_controller | shadow | 0.3812 | 0.815 | 0.920 | **0.670** | 0.000 | 0.000 | swarm + magic + **elite** + mini-boss + boss (5) | **kit-broken** |
| class_0010 | experimental | fire | 0.1338 | 1.000 | 1.000 | 0.555 | 0.000 | 0.000 | swarm + magic + mini-boss + boss (4) | **kit-broken** |

**Kit-broken count: 10/10 (100%).**

**Observations per class:**

- **9/10 classes share the canonical pattern:** swarm/magic over-power + elite in-band (~0.50) + mini-boss/boss collapse. This is the **boss-DPS-floor structural** pattern — kits have the damage to clear lower-tier monsters but cannot generate sustained DPS against bosses with disposition-3 calibrated HP/armor/timeout.
- **class_0009 (shadow_controller) is the one variant** — additionally fails elite tier on the over-shoot side (0.670 vs band upper bound ~0.55). This is the **controller-mechanic mismatch** pattern (per `r1-kit-redesign-queue-2026-05-19.md` § 0 pathology #1) layered on top of the base boss-DPS-floor pattern. The controller archetype's lock-down/CC kit out-controls elite-tier monsters but the same CC has no effect on boss tier (boss CC immunity or high CC resistance presumed); the result is "over-controls weak, fails strong" — exactly the controller-archetype anti-pattern Diablo II's CC-stacked builds historically display in MP-difficulty bosses where CC immunity kicks in.
- **All four element-caster classes (0003 water, 0004 earth, 0005 wind, 0007 holy) converge at identical `final_modifier=0.1338`** with near-identical per-tier shapes. This is empirical evidence of element-symmetric kit composition — the element-pool selection isn't differentiating kit DPS/survivability profiles. This is itself a data point for the kit-redesign queue (R1 queue § 1.2 archetype-mechanic-mismatch pathology applies to "caster" classes converging at the same point because their kits are structurally indistinguishable across elements).
- **class_0008 (physical_warrior) converges highest at 0.3812** — meaning the kit's DPS density is the lowest of the season (highest modifier to reach WR≈0.5 at aggregate). Warrior class with `final_modifier=0.3812` is consistent with R1 queue § 1.1 evidence that physical-melee kits without burst architecture cannot reach boss tier even at modifier 4.0.

The per-class shape reinforces R1 kit-redesign-queue pathology framing: this is not a tuning problem; this is a kit-architecture problem.

---

## § 6 — Per-failure-mode analysis

Per protocol § 3 P3 + dispatch § 3.1 (§ 6) requirement: which sub-pattern fired for each class. Per the R1 kit-redesign-queue taxonomy (§ 0), three pathology patterns are canonically named:

1. **Archetype-mechanic mismatch** (HIGH severity; § 1.2 R1 queue example: class_0016 "lightning_mage" with 5 melee-range skills)
2. **Boss-DPS-floor structural insufficiency** (HIGH severity; § 1.1 R1 queue example: modifier-saturated classes failing boss tier even at modifier 4.0)
3. **Defensive-layer absence** (MEDIUM severity; single-vector defensive layer against melee-aggressive boss)

Three additional candidate sub-patterns the recompose-validation hive's failure-mode framing surfaced (per dispatch § 6 prompt):

4. **Floor-lock-still-active** (lever-applied-but-no-traction at probe value)
5. **Recompose-couldn't-recover** (lever fired but composition change still left class at zero boss WR)
6. **Generation-rule-pathology** (kit emitted from R8 inverted pipeline that violates per-tier-WR-achievability at any modifier)

Mapping P2 evidence to these patterns:

| Sub-pattern | Class evidence in season_100005 | Disposition |
|---|---|---|
| 1. Archetype-mechanic mismatch | 9/10 classes (`shadow_mage`, `fire_mage`, `water_mage`, `earth_caster`, `wind_caster`, `lightning_mage`, `holy_caster`, `physical_warrior`, `experimental`) — none of which exhibit boss-kill capability at converged modifier; R1 queue evidence suggests these are likely melee-range kits with "caster"/"mage"/"warrior" archetype tags that imply ranged or burst capability. **Strongly implicated** for 9/10, but requires per-class kit-composition inspection (not done in this hive; that's kit-redesign queue P5+ work, downstream of R3 schema). | **Implicated; not verified per-class.** Recommendation: surface to kit-redesign queue as the leading candidate explanation. |
| 2. Boss-DPS-floor structural insufficiency | **10/10 classes** show boss_wr=0.000 + mini_boss_wr=0.000 at converged modifier. This is the **load-bearing universal sub-pattern.** All 10 classes have this. | **Confirmed universal.** |
| 3. Defensive-layer absence | Not directly observable from P2 data (defensive-layer composition requires per-skill inspection). Probable contributor for the universal pattern (R1 queue § 1.2 evidence: most kits carry 1 defensive skill + 4 damage skills; insufficient against melee-aggressive boss). | **Probable contributor; not verified per-class.** Surface to kit-redesign queue. |
| 4. Floor-lock-still-active | 0/10 — no class triggered `floor_lock_detected=True`; all classes' true `m* > MODIFIER_SEARCH_FLOOR`. **Empirically refuted at this season.** | **Not implicated.** |
| 5. Recompose-couldn't-recover | 9/9 canonical (0/10 over all classes; experimental class_0010 skipped by design). Disaggregates into two operational sub-mechanisms: **(5a) compression-only — 8 classes (0002-0009)**: at least one lever accepted (negative delta ∈ [-0.13, -0.03]); WR compression occurred at lower tiers only; boss_wr unchanged at 0. Levers found signal and applied DPS reduction; the reduction direction is wrong for boss tier (boss tier doesn't benefit from DPS suppression). Outcome on all 8: `primary_loop_converged`. **(5b) lever-signal-gap — 1 class (class_0001)**: 3 attempts, all delta=0, none accepted; the lever library found no signal at all at the eval_modifier (0.0719). The loop exhausted lever options and fell through to `modifier_fallback`. Problem is upstream of lever-direction-choice — the lever evaluation produced delta=0 before any directionality question could be asked. | **Mechanism is operating; output cannot reach boss WR > 0 — through two distinct paths.** (5a) is "lever-direction-wrong" (DPS compression doesn't help boss tier); (5b) is "lever-signal-absent" (lever library cannot find any composition shift to evaluate). Kit-redesign queue prioritization implication: (5a) cases may admit composition-shift redesigns that move DPS density into boss-tier-effective skills; (5b) cases (class_0001) may require deeper kit-architecture revision — not just reshape skill composition but redesign the kit's damage paradigm (burst vs sustained, AOE vs single-target, primary-attack-skill identity). Diablo II analog: (5a) is "Sorceress Frozen-Orb build that scales DPS but bosses are cold-immune" — composition can shift element/skill mix; (5b) is "Sorceress Lightning build where every lever returns delta=0 because the kit's damage architecture is structurally incompatible with the test arena" — the redesign question is paradigm-level, not skill-mix-level. |
| 6. Generation-rule-pathology | **10/10 classes** emitted from R8 inverted pipeline with kit compositions that converge cleanly at modifiers in [0.07, 0.38] (above floor) but produce 0 boss kills under disposition-3 calibration. The generation rules emit kits that the recompose lever cannot rescue *because the kit-composition lever space available to recompose (skill-swap / role-swap / element-swap) cannot inject what isn't in the kit pool: ranged skills for mages, multi-vector defense, sustained-damage windows, kiting tools.* The lever library is compositional-rearrangement, not generation-rule rewrite. | **Confirmed universal at this season.** This is the architectural finding the kit-redesign queue framing names. |

### § 6.1 — Sub-pattern summary

**Per-class failure-mode mapping (P2 evidence-supported):**

| class_id | sub-pattern 2 (boss-DPS-floor) | sub-pattern 4 (floor-lock-still-active) | sub-pattern 5 (recompose-couldn't-recover) | sub-pattern 6 (gen-rule-pathology) | additional |
|---|---|---|---|---|---|
| 0001 shadow_mage | ✓ | — | ✓ (sub-mechanism **5b lever-signal-gap**) | ✓ | recompose outcome: `modifier_fallback` — 3 attempts, all delta=0, none accepted; lever library found no signal at eval_modifier=0.0719 before fallback path. Kit-redesign queue implication: paradigm-level rebuild candidate (damage architecture restructuring), not composition-shift redesign |
| 0002 fire_mage | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.105; lower-tier WR compression; boss_wr unchanged at 0 |
| 0003 water_mage | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.0417 |
| 0004 earth_caster | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.1333 |
| 0005 wind_caster | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.0767 |
| 0006 lightning_mage | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.0317 |
| 0007 holy_caster | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.1108 |
| 0008 physical_warrior | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.1142; highest converged modifier (0.3812) — kit DPS density lowest of season; consistent with R1 queue § 1.1 modifier-saturated warrior |
| 0009 shadow_controller | ✓ | — | ✓ (**5a compression-only**) | ✓ | accepted lever delta=-0.0925; + elite tier over-shoot (0.670) — controller-mechanic mismatch (R1 § 0 pattern 1 layered on base sub-pattern 2/5/6) |
| 0010 experimental | ✓ | — | (N/A — experimental skips recompose by design) | ✓ | `recompose_outcome=skipped_experimental` per design |

**100% of canonical-class failures (9/9, excluding experimental) fire sub-patterns 2 + 5 + 6 jointly. 0% fire sub-pattern 4 (floor-lock-still-active).** The base failure mode is *"recompose operates correctly + boss-DPS-floor structural insufficiency persists because lever library cannot rewrite generation rules"* — which is exactly the architectural shape the recompose mechanism was always going to expose, *once it was unblocked*. The hive's job was to verify that shape; the hive has verified it.

**Sub-pattern 5 operational disaggregation (kit-redesign queue prioritization input):** of the 9 canonical classes firing sub-pattern 5, **8 (classes 0002-0009) exhibit sub-mechanism 5a (compression-only)** — lever library found signal and applied DPS suppression (accepted delta ∈ [-0.13, -0.03]), but the suppression direction is wrong for boss tier (boss tier doesn't benefit from DPS compression); these are composition-shift redesign candidates (move DPS density into boss-tier-effective skills — burst windows, single-target multipliers, sustained-damage skills with higher per-cast yield against high-HP/high-armor targets). **1 (class_0001) exhibits sub-mechanism 5b (lever-signal-gap)** — all 3 attempts at delta=0, no lever accepted; lever evaluation produced no signal whatsoever at eval_modifier=0.0719, exhausting options before falling through to `modifier_fallback`; this is paradigm-level redesign territory — not just reshape skill composition but reconsider the kit's damage architecture (burst vs sustained, AOE vs single-target, primary-attack-skill identity). The Diablo II analog for the distinction: 5a is "Sorceress Frozen-Orb build whose lever-library can swap element mix and cooldown weighting" — composition shifts have signal; 5b is "Sorceress Lightning build where every lever returns delta=0 because the kit's damage paradigm and the test-arena tier requirements are structurally mismatched" — the redesign question is paradigm-level, not skill-mix-level. The kit-redesign queue should consume this distinction so the queue's first authoring session prioritizes (5b) cases (deeper architectural intervention) separately from (5a) cases (composition shifts).

### § 6.2 — Where I push back on knight-rider's framing (transparency)

Knight-rider's STATE entry (`2026-05-20 EDT — knight-rider STATE — P2 FULL ACCEPTANCE`) frames the per-failure-mode finding as "100% of failures are boss-DPS-floor-structural (boss WR = 0 + mini-boss WR = 0)." I agree with the load-bearing conclusion but want to disaggregate transparently:

- **Sub-pattern 2 (boss-DPS-floor) is 10/10 universal — the *observable* failure mode.** Knight-rider's framing names this correctly.
- **Sub-pattern 5 (recompose-couldn't-recover) is the *operational* failure mode** — meaning what the recompose mechanism actually did. Knight-rider's framing implies this; my analysis names it explicitly.
- **Sub-pattern 6 (generation-rule-pathology) is the *architectural* failure mode** — meaning where the fix has to live. Knight-rider's framing arrives here via "kit-composition pathology is now the unambiguous load-bearing problem"; my analysis names it as a sub-pattern in the failure-mode taxonomy so the kit-redesign queue's next-step framing has explicit anchor.
- **Class_0009's elite over-shoot is a meaningfully distinct sub-pattern layer** (controller-mechanic mismatch on the elite tier). Knight-rider's framing groups it into "100% boss-DPS-floor structural"; I disaggregate it because the kit-redesign queue should treat class_0009's elite over-shoot as evidence the controller-archetype kit needs different redesign work than the 9 "caster"-style kits. Diablo II canonical example: Sorceress Nova builds and Druid Tornado builds both fail Hell-difficulty bosses, but for *different* reasons — element immunity (Sorceress) vs sustained-DPS-window (Druid). One-size-fits-all kit-redesign would miss the distinction.

This is not adversarial with knight-rider's framing — it is the design-judgment refinement the P3 synthesis owes the kit-redesign queue authoring downstream.

---

## § 7 — Verdict on H_RC vs H_RC_0

### § 7.1 — The verdict

**Verdict: CANNOT REJECT NULL.**

Per scope-of-work § 1: H_RC requires ≥ 60% kit-acceptable for any PASS verdict (60-80% PASS moderate; ≥ 80% PASS strong). Observed: **0% kit-acceptable** (0/10 classes). This is unambiguously below the < 60% CANNOT REJECT NULL threshold. The verdict is not at an edge case; it is at the worst-case bound of the verdict gate.

H_RC is **not supported** by season_100005 evidence. The recompose mechanism (Option A unblock + Option B mechanism preserved) does not, on this season, produce shippable kits — because the load-bearing pathology is upstream of where recompose can operate.

H_RC_0 is **not refuted** by season_100005 evidence. The null hypothesis ("generation rules require revision") is reinforced. The recompose mechanism's lever library operates at the kit-composition layer (skill-swap / role-swap / element-swap), but the structural insufficiency in season_100005 kits — boss-DPS-floor + likely archetype-mechanic mismatch + likely defensive-layer absence — lives at the *kit-architecture* layer (per-skill range, defensive-vector multiplicity, sustained-damage burst windows), which generation rules emit and recompose cannot rewrite.

### § 7.2 — Nuance the verdict carries

The verdict is CANNOT REJECT NULL, not "H_RC is decisively wrong." Three load-bearing nuances:

1. **Option A's mechanism is independently validated.** The prior floor-lock failure mode is empirically eliminated. The 22 Pattern-B classes from Phase B.2 (m* ∈ [0.01, 2.0]) reach their equilibrium modifiers cleanly. This is a real architectural win; it just doesn't ship the season alone because the per-tier WR shape requires more than modifier-reachability.

2. **Option B's mechanism is mechanically verified but behaviorally unexercised at this hive.** The served population (kits with true m* < 0.01) is empirically absent from season_100005 — but absent ≠ proven nonexistent across all substrates. A future substrate-generalization study (Matt-direction next step or post-kit-redesign-queue rerun) could surface the served population on a different substrate, at which point the mechanism re-enables via the documented one-line cost. The verdict applies to *this season*; the mechanism's value applies to *any future season that surfaces the served population*.

3. **The catalogue pathology is now empirically unambiguous at full-season scope.** This is the canonical-record-worthy finding. R1 kit-redesign-queue (38/51 broken kits) was a 51-class sample; R2+ST counterfactual joint synthesis Row 5 ("catalogue has deeper pathology") was math-only on the existing R2 telemetry; this hive's P2 evidence corroborates both at full-season scope on a fresh substrate (shadow) under the new tuning contract (per-tier WR + disposition-3 calibration). **Three independent lines of evidence converge on the same diagnosis.** The kit-redesign queue is now the load-bearing actionable workstream by triangulation.

### § 7.3 — Why this verdict is the cleanest possible diagnosis (not a failure)

Per protocol § 11 (gandalf's wizard's note from the protocol-authoring session):

> *If H_RC fails, we have the cleanest possible diagnosis of where the actual pathology lives — and the next architectural decision becomes obvious. Either outcome resolves a major open question. Both outcomes are valuable.*

The hive's verdict is exactly that. The recompose-validation hive was the cheapest, sharpest test of whether recompose-as-bridge could substitute for kit-redesign. The test ran clean (P0 mechanism verified; P1 mechanism verified mechanically; P2 fresh diagnostic regen at full-season scope on a substrate not previously exhausted; P3 synthesis under autonomous-operation framework). The answer to "can recompose substitute for kit-redesign?" is — for the existing R8 inverted pipeline catalogue under disposition-3 calibration on shadow substrate seed=100005 — **no.** The pathology lives at kit-architecture; recompose operates at kit-composition; the lever space available to recompose cannot rewrite what isn't in the kit pool.

**The next architectural decision becomes obvious.** It is the kit-redesign queue (R1 disposition's queue + R2+ST joint synthesis Row 5's recommendation + this hive's P2 corroboration). The hive's mission was to test whether that work was avoidable. It is not. The hive's value at CANNOT REJECT NULL is that it answered the question definitively, with full empirical record, with verified-independent mechanisms preserved for future use, and with two methodological findings worth canonical record (§ 9).

---

## § 8 — Recommendation

Per protocol § 3 P3 + dispatch § 3.1 (§ 8): ship to P4 / diagnose further / surface to Matt.

**Recommendation: SURFACE TO MATT (wind-down trigger #3 per protocol § 7).**

P4 (ship true season) does NOT fire autonomously per protocol § 7 trigger #3 + dispatch § 6 HARD out-of-scope #1. The hive deactivates pending Matt direction on the next architectural step.

Knight-rider authors the Matt briefing per protocol § 7 trigger #3 + dispatch § 3.3 (Phase 3 of P3). The Matt briefing routes the verdict + the recommended next-step architectural decision (§ 10) for Matt's consideration without committing Matt to any specific path.

**Why not "diagnose further" within this hive:**

- The empirical evidence is unambiguous (0% kit-acceptable; 100% Pattern-A; 10/10 kit-broken). There is no edge-case interpretation that shifts the verdict.
- Additional regens on other substrates (earth, fire, etc.) would test substrate-generalization, but that is a Matt-direction architectural question (does the kit-redesign queue work apply across all substrates, or does shadow have a unique pathology profile?), not a P3-internal diagnostic question. Surfacing to Matt is the right place for that decision.
- The recompose mechanism's behavioral landing (Option B) is documented as preserved-pending-future-substrate; further hive work to surface a real subject would duplicate the substrate-generalization question.

**Why not "ship partial" (PASS moderate at the edge):**

- PASS moderate threshold (60-80%) is not within edge-of-observation distance. The observed value is 0%; the nearest PASS moderate edge is 60%. There is no reasonable interpretation that shifts 0/10 kit-acceptable into 6/10. The verdict is at the worst-case bound.

---

## § 9 — The Phase-1-vs-Phase-2 signal-reversal methodology finding

This is **canonical-record-worthy** per protocol § 11 and worthy of engineering-disciplines.md amendment at P5 (if the hive completes its full arc) or surface inclusion in the Matt briefing at trigger #3 (if CANNOT REJECT NULL signals — which it does).

### § 9.1 — The reversal

- **Phase 1 (generation-time signal, rocket):** 6/10 classes reported `floor_lock_recompose=True` in rocket's diagnostic summary (the generation-time embedded balance loop signal during R8 inverted pipeline kit construction). On initial read by knight-rider, this signal *appeared* to load-bearingly support the masked-Pattern-B-extreme hypothesis at far above § 2.5's 3-8/season conservative estimate.
- **Phase 2 (cold-start canonical, gamora):** 0/10 classes have `floor_lock_recompose=True` under cold-start from `initial_modifier=1.0`. Equilibrium modifiers observed: `m* ∈ [0.0719, 0.3812]` — all above MODIFIER_SEARCH_FLOOR=0.01.

**Reversal magnitude: 6/10 → 0/10.** The generation-time signal was the opposite polarity from the cold-start canonical signal at the population level.

### § 9.2 — Root cause (per star-lord analysis § 7 + gamora FRICTION diagnostic)

The R8 inverted pipeline's embedded balance loop runs at whatever modifier state the class holds at that pipeline stage during kit construction. For classes being built by the inverted pipeline, the embedded loop is invoked at modifiers near or at the search floor (a property of how the inverted pipeline constructs kits — it builds kits at low modifiers and checks whether they pass at those low modifiers, by design). At those pipeline-internal near-floor states, `last_wr > RECOMPOSE_SIGNAL_HI=0.70` because the class in that pipeline state is over-performing at a floor-range modifier (over-performing at the lower tiers, where the pipeline-internal evaluation lands). The `floor_lock_detected=True` flag fires *correctly for that pipeline state* — the detection branch is doing exactly what it was designed to do.

But those pipeline states do NOT equal the class's true cold-start equilibrium modifier. Under cold-start from `initial_modifier=1.0`, `_quick_modifier_estimate` descends from 1.0 to find the true equilibrium. For all 10 classes in season_100005, the true `m*` falls in `[0.0719, 0.3812]` — all above MODIFIER_SEARCH_FLOOR=0.01. The signal-range `[0.30, 0.70]` is reached during descent. `floor_lock_detected=False` is the correct cold-start outcome.

### § 9.3 — Why this matters (canonical-record-worthy)

**The load-bearing finding:** generation-time embedded convergence signals (pipeline-state-conditioned) are NOT equivalent to cold-start equilibrium convergence signals (equilibrium-conditioned). A class that appears floor-locked at generation time may not be floor-locked at true equilibrium.

This is the same epistemic structure as the P1 smoke B1 test-class-selection failure (gandalf brief v1.0 § 4.1 selected class_0001 based on warm-start signature `modifier=0.0509` + saturated WR; cold-start exposed that signature as a TOLERANCE-satisfied-at-old-floor artifact, not true equilibrium below floor). **Two independent hive events surfaced the same methodological pattern within ~24 hours.** That convergence is the load-bearing argument for elevating the pattern to engineering-disciplines amendment.

### § 9.4 — Retrospective application

- **Gandalf brief v1.0 § 4.1 (P1 smoke B1 design):** test-class-selection error rested on warm-start signature interpretation. v1.1 amendment corrected the discipline.
- **Knight-rider's Phase 1 read (P2 phase 1 disposition):** initial interpretation of 6/10 generation-time `floor_lock_recompose=True` as supporting the masked-Pattern-B-extreme hypothesis at population level — was the same epistemic mistake. Gamora's Phase 2 FRICTION caught it cleanly; the autonomous-operation framework dispositioned the finding without escalation.

Both retrospective applications point at the same root-cause pattern. Future hive-internal interpretation of generation-time embedded-loop signals must apply the equilibrium-state cold-start check before treating the signal as canonical.

### § 9.5 — Prospective application

Any future hive that wants to validate convergence properties from generation-time signals must explicitly distinguish pipeline-state signals from equilibrium-state signals. Cold-start dry-run verification is mandatory before treating generation-time signals as canonical. This applies to:

- **Smoke gate design** (P1 finding): mandatory cold-start dry-run on any candidate canonical smoke test class.
- **Population-level diagnostic reads** (P2 finding): generation-time aggregate signals (e.g., "6/10 classes show property X") are pipeline-state-conditioned and require equilibrium-conditioned cross-check before treating as canonical population-property estimates.
- **Any future R-batch work** that uses generation-time embedded-loop telemetry as a population-property estimator.

### § 9.6 — Engineering-disciplines candidate framing

Two engineering-disciplines candidates queued by this hive:

**Candidate 1 (P1 smoke-design finding):** *"Mandatory cold-start dry-run on any candidate canonical smoke test class before locking it as the canonical subject. The warm-start signature observed during prior runs is symptomatic of multiple kit conditions and only cold-start equilibrium disambiguates them."*

**Candidate 2 (P2 signal-reversal finding):** *"Pipeline-state-conditioned generation-time signals are NOT equivalent to equilibrium-state-conditioned canonical convergence signals. Any signal extracted from an embedded-loop invocation at pipeline-internal modifier states (kit construction, warm-start, mid-pipeline diagnostics) must be cross-checked against cold-start equilibrium-conditioned canonical convergence before being treated as a population-property estimator."*

**Framing recommendation (gandalf design judgment):** these two candidates share the same root-cause pattern — *signals from non-equilibrium pipeline states conflated with equilibrium-state population properties.* I recommend they be folded into engineering-disciplines.md as a **single Discipline #11 elaboration** rather than two standalone disciplines. Discipline #11 (empirical inspection over assumption) is the natural anchor; the elaboration would be:

> **Discipline #11 elaboration (proposed P5 amendment):** *Empirical signals must be measured in the same state space as the property being estimated. Generation-time embedded-loop signals, warm-start convergence signatures, and pipeline-internal modifier states are pipeline-state-conditioned — they reflect the loop's behavior under those specific pipeline states, NOT the class's true cold-start equilibrium property. Before any signal extracted from a non-cold-start state is treated as a canonical population-property estimator (smoke gate canonical subject selection, population-level rate estimate, design-direction empirical input), cold-start dry-run verification is mandatory. Two retrospective examples (gandalf brief v1.0 § 4.1 smoke B1 test-class selection; recompose-validation hive P1-vs-P2 signal reversal) demonstrate the cost of conflating these state spaces.*

This is my recommendation for P5 amendment language; the final framing remains a P5 deliverable for gandalf + jack-ryan to co-author with the rest of the engineering-disciplines amendment work. Jack-ryan Gate-2 critique on this synthesis may refine the language further.

**Tradeoff considered:** the alternative is two standalone discipline candidates (one for smoke-design, one for population-property signals). I reject the alternative because the two candidates share the same root-cause epistemic pattern; treating them as one discipline preserves the load-bearing insight (state-space conflation) at the cost of one specific application context. The two specific applications can be carried as sub-clauses or examples within the parent discipline. This is the simpler artifact for future hive authors to internalize.

---

## § 10 — Recommended next-step architectural decision for Matt's consideration

Per protocol § 3 P3 + dispatch § 3.1 (§ 10) + dispatch § 6 HARD out-of-scope #5 ("architectural recommendations beyond what evidence supports — gandalf's § 10 recommends; doesn't decide; Matt directs"):

### § 10.1 — Primary recommendation: kit-redesign queue execution

**Surface the kit-redesign queue (`canonical/story/r1-kit-redesign-queue-2026-05-19.md`) as the natural next-step architectural decision for Matt's consideration.**

Empirical triangulation supporting this recommendation:
- R1 sprint v2 evidence (engine commit `2546180`, 2026-05-19): 51/51 boss-tier failure at the catalogue layer; 38/51 broken-kits surfaced; three pathology patterns identified (archetype-mechanic mismatch, boss-DPS-floor structural, defensive-layer absence)
- R2+ST counterfactual joint synthesis Row 5 (2026-05-19, AMENDED): "catalogue has deeper pathology" — R2-as-canonical and ST-K-as-lever both eliminated as load-bearing fixes at the floor-locked modifier
- **This hive's P2 evidence (2026-05-20): 10/10 Pattern-A at full-season scope on shadow substrate under disposition-3 calibration — kit-composition pathology empirically reinforced at fresh-substrate full-season scope under the new tuning contract**

The three independent lines converge on the same diagnosis: the load-bearing fix is generation-rule revision + per-class kit-architecture redesign, not modifier-tuning + not lever-mechanism extension.

**Sequencing dependencies (per R1 queue § 0):** the kit-redesign queue is downstream of R3 (per-skill range + AI behavior schema migration; rocket + star-lord + elrond; 2-4 wk effort) — R3 is the schema prerequisite that enables the kit-redesign to express what it needs to express (a "lightning mage with 10m primary attack" requires the per-skill range field).

**Effort estimate (per R1 queue § 0):**
- ~20-30 classes require partial kit redesign (range diversity injection)
- ~10 classes require deep kit redesign (rebuild defensive layer + redistribute energy-cycling + align archetype description)
- ~5-10 classes are kit-acceptable post-disposition-3 (no redesign required)

This is multi-week work. Matt's direction on sequencing and authorization is required; the hive does not commit Matt to that timeline.

### § 10.2 — Alternative options for Matt's consideration

For transparency, three alternative architectural paths Matt may consider:

**(A) Substrate-generalization study before kit-redesign.** Run P2-equivalent fresh diagnostic regens on earth, fire, water, and one element-symmetric substrate to verify the 10/10 Pattern-A finding generalizes. If the finding generalizes, kit-redesign queue is unambiguous. If a substrate surfaces 1-2 floor-lock-recovery candidates, Option B re-enables under autonomous L1 and validates the mechanism behaviorally. **Cost:** ~16-24 wall hours of regen + analysis. **Value:** stronger empirical foundation for the kit-redesign decision.

**(B) Disposition-3 recalibration sensitivity check.** The current disposition-3 calibration (boss HP × 0.40, armor × 0.45, swarm HP × 3.5, 240s boss timeout) was authored to bring boss effective-HP within reach of well-designed kits. The 0% kit-acceptable result at full-season scope on shadow substrate may be sensitive to disposition-3 specifically. A sensitivity sweep across alternative calibrations (e.g., boss HP × 0.30, × 0.50; boss armor × 0.35, × 0.55) would test whether the calibration is structurally too aggressive or whether the kit pathology is calibration-independent. **Cost:** ~8-16 wall hours. **Value:** confirms the kit pathology is calibration-independent before committing to kit-redesign.

**(C) Targeted single-class kit-redesign pilot before queue authorization.** Pick one canonical class (e.g., class_0006 lightning_mage — has the cleanest archetype-mechanic-mismatch signature per R1 queue § 1.2) and execute a manual kit-redesign per R1 queue § 2's "kit-acceptable" definition. Regen + cold-start convergence on the redesigned kit. If the redesigned kit converges into per-tier band, the kit-redesign queue work is empirically de-risked. **Cost:** ~8-16 wall hours per class. **Value:** smallest empirical proof that kit-redesign is the right lever before committing to the full queue.

**My design-judgment recommendation among the three:** primary recommendation (kit-redesign queue execution after R3 schema lands) is the highest-confidence path given the triangulation. Option (C) targeted pilot is the lowest-cost de-risking step if Matt wants additional empirical confirmation before authorizing the full queue. Options (A) and (B) are sensitivity checks that I judge lower-value given the triangulation strength, but Matt may weight them differently based on roadmap priorities.

### § 10.3 — What this recommendation does NOT decide

Per dispatch § 6 HARD out-of-scope #6: the recommendation surfaces; Matt directs. Specifically:

- Whether to authorize the kit-redesign queue sprint at all (Matt-level architectural decision)
- The sequencing of kit-redesign vs other in-flight workstreams (VS2a continuation, Pattern-B PARKED thread, etc. — Matt + knight-rider roadmap-commit decision)
- The roster of classes in the queue's first wave (gandalf + rocket co-author at queue-authorization-time, not at P3)
- Whether to execute any of options (A), (B), or (C) as preliminaries (Matt-direction)

This recommendation is the design steward's read of where the evidence points. The decision is Matt's.

---

## § 11 — What the hive accomplished

Per protocol § 11 (gandalf's wizard's note) + dispatch § 3.1 (§ 11): the cleanest possible diagnosis.

The recompose-validation hive accomplished the following, in canonical-record order:

### § 11.1 — Mechanisms verified

1. **Option A's mechanism is independently verified.** Floor widening from 0.05 → 0.01 lands cleanly under autonomous L1 gamora implementation; smoke gates A1/A2/A3 pass; named constants `MODIFIER_SEARCH_FLOOR` + `MODIFIER_SEARCH_CEILING` introduced per Discipline #18; stop-gap warm-start regen on 3 diagnostic seasons confirms 24/31 prior-failed classes now converge; P2 cold-start observes equilibrium modifiers in [0.0719, 0.3812] — above the new floor, below the old floor — confirming the prior floor-lock failure mode is eliminated.

2. **Option B's mechanism is mechanically verified.** Recompose-trigger re-conditioning at `last_wr > RECOMPOSE_SIGNAL_HI` (the brief's principled departure from gamora § 5.2's `eval_modifier ≤ floor + ε` semantic, jack-ryan-confirmed-clean) lands under autonomous L1 gamora implementation; 4 unit tests confirm the floor-lock-detection branch fires correctly under controlled mocks; production path through schema v2.13 fields (ClassBalanceResult.floor_lock_recompose + per-attempt working_modifier + floor_lock_detected) is round-trip-verified by jack-ryan Amendment 6 R11(b) test; 179/179 test suite PASS at implementation; 179/179 test suite PASS at soft-disable. The mechanism is ready for behavioral re-enable via one-line constant change when a future substrate surfaces a confirmed served-population subject.

### § 11.2 — Hypotheses eliminated from candidate-lever space

The hive's empirical evidence eliminates the following from the candidate-lever space (load-bearing for future hive scope-setting):

1. **R2-as-canonical convergence target** (eliminated by R2+ST joint synthesis 2026-05-19; reinforced by this hive's evidence that the boss-tier pathology is kit-composition-architectural, not measurement-system-artifact)
2. **ST per-cast damage-multiplier K as lever** (eliminated by R2+ST joint synthesis Phase C K-sweep)
3. **Recompose-as-substitute-for-kit-redesign** (eliminated by this hive's P3 verdict — H_RC CANNOT REJECT NULL)
4. **Floor-lock-recovery as the load-bearing missing mechanism** (eliminated by this hive's P2 evidence — masked-Pattern-B-extreme population empirically absent at full-season scope on shadow substrate)
5. **Generation-time embedded-loop signals as canonical population-property estimators** (eliminated by this hive's P1-vs-P2 signal-reversal methodological finding)

### § 11.3 — Canonical empirical evidence produced

The canonical empirical record at `output/p2-fresh-diagnostic-regen-2026-05-19/` is the artifact:

- **rocket Phase 1 generation artifacts:** season_100005 full canonical roster (10 classes; 44 monsters; 200 gear items; cosmology + anchor; manifest)
- **gamora Phase 2 balance telemetry:** balance_results.json with full schema v2.12 + v2.13 fields populated; 10/10 classes; **35** recompose_attempts across 9 canonical classes (class_0001=3, classes 0002-0009=4 each); cold-start equilibrium modifiers; per-tier WR at converged modifier
- **star-lord Phase 3 classification analysis:** `p2-classification-and-floor-lock-analysis.md` — per-class kit-acceptable/mediocre/broken classification; Pattern-A/B classification; floor-lock candidate count; signal-reversal methodological documentation; aggregate statistics

This is the first full-season cold-start canonical regen under per-tier WR + disposition-3 calibration + Option A floor-widened + Option B mechanism-installed engine state. **It is the canonical empirical record of catalogue pathology at full-season scope on shadow substrate under the new tuning contract.** Future hives reference this record; the kit-redesign queue execution work uses this record as the empirical baseline.

### § 11.4 — Methodological findings worth canonical record

Two methodological findings worth engineering-disciplines record (per § 9):

1. **Mandatory cold-start dry-run on any candidate canonical smoke test class** (P1 finding)
2. **Pipeline-state vs equilibrium-conditioned signal distinction** (P2 finding)

Both fold into a single Discipline #11 elaboration per my framing recommendation (§ 9.6).

### § 11.5 — Governance precedents established

Three governance precedents established by P1 disposition (decisions-log 2026-05-19 P1 entry):

1. **A BLOCKING smoke gate exists to falsify the design diagnosis, not the mechanism.** Future smoke designs distinguish these failure modes explicitly.
2. **Hive milestone tags do not fire on un-empirically-tested behavioral changes.** Tag-firing discipline as governance precedent.
3. **When your test arena lacks the monster you designed your synergy against, you fix the arena, not the synergy.** Test-design-failure-as-disposition-category established.

### § 11.6 — The cleanest possible diagnosis (the wizard's measure)

The hive was authored to test whether recompose-as-bridge could substitute for kit-redesign. The hive's P3 verdict is: it cannot, on this season's evidence. The diagnosis is unambiguous, full-empirical, mechanism-preserved-for-future-use, methodology-finding-captured, governance-precedent-established. **This is exactly what protocol § 11 named as the value-at-failure case.** The hive succeeded by producing the diagnosis the project needed, even though the diagnosis is the null-hypothesis disposition.

The cleanest possible diagnosis. The road forward is clear: kit-redesign queue (or one of the alternatives § 10.2 enumerates, per Matt's direction). The recompose mechanism waits in its soft-disabled state, instrumented, preserved, ready for a future season where the served population may appear. The kit-redesign work proceeds at Matt's authorization. The hive's autonomous-operation phase ends.

Mithrandir's measure: the hive walked the road it was authored to walk. It arrived where the evidence took it. The road forward is named. That is what the road was for.

---

## § 12 — References

### § 12.1 — Hive empirical artifacts

- `reincarnated-engine/output/p2-fresh-diagnostic-regen-2026-05-19/season_100005/` — rocket Phase 1 generation artifacts
- `reincarnated-engine/output/p2-fresh-diagnostic-regen-2026-05-19/season_100005/balance_results.json` — gamora Phase 2 balance telemetry
- `reincarnated-engine/output/p2-fresh-diagnostic-regen-2026-05-19/p2-classification-and-floor-lock-analysis.md` — star-lord Phase 3 canonical analysis

### § 12.2 — Hive protocol + scope + operational artifacts

- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — hive operating protocol
- `agentic_orchestration/hive-mind/scope-of-work-recompose-validation.md` — hive mission scope + PASS thresholds
- `agentic_orchestration/hive-mind/coordination-matrix-recompose-validation.md` — coordination matrix
- `agentic_orchestration/hive-mind/recompose-validation-log.md` — hive log (append-only, continuous broadcast)
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-20-recompose-validation.md` — Day-1 state-of-hive

### § 12.3 — Phase dispatches

- `agentic_orchestration/dispatches/2026-05-19-knight-rider-recompose-validation-hive-launch.md` — hive launch
- `agentic_orchestration/dispatches/2026-05-19-gamora-balance-loop-floor-option-A-implementation.md` — P0 dispatch
- `agentic_orchestration/dispatches/2026-05-19-gandalf-p1-option-b-recompose-trigger-design-brief.md` v1.1 — P1 brief (gandalf; v1.1 amendment captures smoke-design discipline candidate)
- `agentic_orchestration/qa/pending/2026-05-19-p1-option-b-recompose-trigger-gate1.md` — P1 Gate-1 (jack-ryan; APPROVE-WITH-AMEND)
- `agentic_orchestration/dispatches/2026-05-19-gamora-p1-option-b-recompose-trigger-implementation.md` — P1 implementation dispatch
- `agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-plus-gamora-p2-fresh-diagnostic-regen.md` — P2 dispatch
- `agentic_orchestration/dispatches/2026-05-20-gandalf-plus-jack-ryan-p3-validation-synthesis.md` — P3 dispatch (this synthesis is its primary deliverable)

### § 12.4 — Decisions-log entries (engine repo)

- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-19 P0 entry — Option A floor widening (engine `a58b60f`)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-19 P1 entry — Option B MECHANICALLY COMPLETE / BEHAVIORALLY SOFT-DISABLED (engine `22b1c3c`)
- **Pending:** P3 verdict entry — gandalf authors a one-paragraph decisions-log update per ADR-001 routing (jack-ryan reviews Gate-2; knight-rider files at verdict-handoff); content: H_RC verdict + recommendation + cross-references to this canonical findings document

### § 12.5 — Tags fired (per knight-rider STATE entries)

- `recompose-hive/v0.0-pre-activation` (all 4 repos; pre-hive baseline)
- `gamora/v1.13-balance-loop-floor-widened-option-a` (engine; P0 seam tag)
- `recompose-hive/v0.1-option-a-floor-widened` (engine + collab; P0 hive milestone)
- `gamora/v1.14-balance-loop-option-b-recompose-conditioned-soft-disable` (engine; P1 seam tag with load-bearing `-soft-disable` qualifier)
- **HELD:** `recompose-hive/v0.2-option-b-recompose-conditioned` (P1 hive milestone — fires only on future P2-or-later substrate surface of confirmed served-population subject + re-enable + smoke PASS)
- `rocket/v1.22-p2-fresh-regen-shadow-100005` (engine; P2 Phase 1 seam tag)
- `gamora/v1.15-p2-balance-convergence-shadow-100005` (engine; P2 Phase 2 seam tag)
- `star-lord/v1.14-p2-classification-shadow-100005` (engine; P2 Phase 3 seam tag)
- `recompose-hive/v0.3-diagnostic-regen-complete` (engine + collab; P2 hive milestone)
- **Pending:** `gandalf/<X.Y>-p3-canonical-findings-synthesis` (this synthesis's seam tag; gandalf fires on synthesis acceptance)
- **Pending:** `jack-ryan/<X.Y>-p3-gate2-disposition` (P3 Gate-2 seam tag; jack-ryan fires on Gate-2 disposition)
- **Pending:** `recompose-hive/v0.4-validation-verdict` (P3 hive milestone; knight-rider fires on verdict-handoff per dispatch § 7)

### § 12.6 — Adjacent canonical work (informational; not in hive scope)

- `canonical/story/r1-firstbatch-fail-disposition-2026-05-19.md` — gandalf S1 disposition + § 11 staged-approval framing
- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` — kit-redesign queue (the primary § 10 recommendation)
- `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` (AMENDED) — R2-as-canonical + ST-K-as-lever joint synthesis Row 5 ("catalogue has deeper pathology") — empirically reinforced by this hive's P2 evidence
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — original 5-axis gap diagnosis
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — Matt's QD-engine + profile architecture vision (informational)

### § 12.7 — Working-agreement documents (engine repo)

- `reincarnated-engine/design/working-agreement/balance-loop-floor-investigation-2026-05-19.md` — gamora investigation establishing Option A + Option B math
- `reincarnated-engine/design/working-agreement/r2-counterfactual-convergence-math-2026-05-19.md` — gamora Phase B R2 counterfactual
- `reincarnated-engine/design/working-agreement/st-damage-multiplier-counterfactual-math-2026-05-19.md` — gamora Phase C ST K-sweep
- `reincarnated-engine/design/working-agreement/r2-st-counterfactual-joint-synthesis-2026-05-19.md` — gamora Phase D joint synthesis
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines anchored throughout (#1, #2, #11, #12, #13a, #15, #18, R11(b), Pattern P7); P5 amendment candidate at § 9.6 of this document

### § 12.8 — ADR-001 routing note

Per ADR-001 (decisions-log entry routing): this canonical findings document is the gandalf-authored design-steward synthesis; the one-paragraph decisions-log entry that records the P3 verdict in `reincarnated-engine/design/decisions/decisions-log.md` is knight-rider's verdict-handoff deliverable (per dispatch § 3.3 Phase 3 of P3). Jack-ryan Gate-2 reviews this document before the decisions-log entry is filed. The decisions-log entry references this document for full reasoning.

---

*Authored 2026-05-20 by gandalf as recompose-validation hive P3 synthesis. The verdict is CANNOT REJECT NULL; the diagnosis is the cleanest possible; the road forward is the kit-redesign queue (or one of the § 10.2 alternatives at Matt's direction). The hive walked its full road. Mithrandir signs the verdict.*
