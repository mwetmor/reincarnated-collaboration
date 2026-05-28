# Path (1) — Failure Modes, Scope Creep, Design Drift Register

> **STATUS:** CURRENT — gandalf-authored. 17 patterns to watch during Cycle 14 Path (1) execution; KR includes audit references in dispatches; gandalf design-quality audit checks at wave-close (Discipline #43).

**Date:** 2026-05-27 evening
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 "confirm execute on all three"
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (recognition record)
- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` (load-bearing protection)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-in-advance-design-calls.md` (companion design calls)

---

## 0. TL;DR

17 patterns to monitor during Cycle 14 Path (1) execution. Categorized: 8 failure modes / 4 scope creeps / 5 design drifts. Each pattern has a watch + counter. KR includes audit references in dispatches; gandalf design-quality audit at wave-close (Discipline #43) checks; framing-refusal authority (Discipline #44) empowers sub-agents to catch in-flight.

---

## 1. Failure modes (8 patterns)

### F-1. Math methodology selection drift

**Pattern:** Pareto / Crowding / Mahalanobis / KL each have multiple formulations. Choosing the wrong formulation produces silent failure — algorithm executes but doesn't deliver intended semantics. E.g., NSGA-II crowding fails on non-dominated solutions; hypervolume in 8D explodes without WFG / Beume-Fonseca algorithm.

**Watch:** each math note specifies empirical validation criteria (Discipline #11 inspection over assumption); jack-ryan Gate-1 verifies methodology choice cites algorithm by exact name + reference; Matt-gate ratifies at Discipline #18 hotspot.

**Counter:** elrond methodology consultation required per Discipline #18 hotspot routing for each Phase 4 math gate; gandalf design-quality audit at wave-close verifies algorithm choice matches design intent.

### F-2. Per-cell capacity blowup

**Pattern:** Discipline #46 § 7 protects against GLOBAL O(n²) by per-cell bounding. But per-cell capacity drift (cells get 1000+ kits each) makes per-cell O(k²) become O(1M) — no longer trivial. Failure surfaces only when archive size exceeds expectations.

**Watch:** Per-cell capacity MUST be explicit (Design Call C ratification: 30 kits/cell gandalf-recommend); eviction MUST fire BEFORE capacity exceeded, not after; smoke tests verify per-cell capacity bounded under stress.

**Counter:** Per-cell capacity cap is an explicit math-note constant (MG-5 Eviction Rules); jack-ryan Gate-2 grep audit verifies the constant is referenced + enforced; Discipline #46 § 7 + Design Call C compose.

### F-3. Faction cardinality drift

**Pattern:** Phase 5 multimodal clustering produces 30+ factions per season (faction concept becomes meaningless) OR 1 faction per season (faction concept becomes meaningless). Target 3-8 factions per season.

**Watch:** Wave 5 smoke season produces faction count; if outside 2-8 range, algorithm parameters need tuning. Math Note PM-1 specifies target range + parameter-tuning protocol.

**Counter:** Design Call A ratification locks faction cardinality intent (gandalf-recommend A2 = K=2-4 emergent); Math Note PM-1 parameters tuned for target; empirical validation at Wave 5 smoke; Discipline #43 design-quality audit at Wave 5 close checks faction cardinality.

### F-4. Phase 5 LLM call volume drift

**Pattern:** Path (1) Phase 5 expansion adds multimodal clustering + faction-coalescence to existing per-kit cohesion-judge calls. Total LLM calls per season could 2x-3x from baseline ~2,100 to ~4,500-6,300. Token costs scale.

**Watch:** Math Note PM-2 (Faction-Label Assignment Policy) specifies LLM call budget per season; Phase 5 dispatch acceptance criteria include token-cost ceiling; star-lord telemetry tracks LLM calls per season.

**Counter:** Batch LLM calls where possible (multiple kits per call); cache deterministic outputs (substrate-derived placeholder names); algorithm-side clustering decides MEMBERSHIP; LLM only NAMES clusters (separation enforced at math-note authoring).

### F-5. Joint-gate threshold drift

**Pattern:** Phase 7 2-layer joint-gate thresholds set too high → no kits pass → empty season. Set too low → no filtering → defeats purpose. Calibration is empirical.

**Watch:** Wave 5 smoke seasons measure threshold-pass-rate; if 0% or 100%, thresholds need calibration; target 70-85% pass-rate post Phase 4 ACCEPT.

**Counter:** Phase 7 dispatch (per Path 1 record § 3.3) includes threshold-calibration empirical procedure; Matt-ratification at threshold-locking time; Discipline #11 inspection over assumption.

### F-6. Class concept resurrection (vocabulary drift)

**Pattern:** Sub-agents executing Phase 4 + 5 + 7 work might unconsciously revert to "class" vocabulary (e.g., "class-level Pareto frontier" instead of "per-kit Pareto frontier"; "class faction membership" instead of "kit faction membership"). Discipline #45 (vocabulary lock) protects against this BUT only if applied consistently.

**Watch:** gandalf design-quality audit at Phase 4 + 5 + 7 wave-close (Discipline #43) greps for "class" in newly-authored docs + code; jack-ryan Gate-2 grep audit secondary.

**Counter:** Discipline #45 vocabulary lock applies; sub-agent framing-audit at session-start (Discipline #42) catches vestigial vocabulary; framing-refusal authority (Discipline #44) empowers sub-agents to refuse dispatches with vestigial class vocabulary.

### F-7. Phase 6 implicit creep into Cycle 14

**Pattern:** Sub-agents authoring Phase 7 2-layer joint-gate might want to add visual layer "while we're at it." Phase 6 deferred for good reason (galadriel CV pipeline not ready); creep would extend Cycle 14 by 6-12 weeks unannounced.

**Watch:** Phase 7 dispatch (per Path 1 record § 3.3) explicitly out-of-scope-guards visual layer; jack-ryan Gate-1 verifies out-of-scope text present.

**Counter:** Phase 7 dispatch scope text: "**Visual layer DEFERRED to Cycle 15+**; Cycle 14 ships 2-layer (mechanical + cohesion) only; sub-agent authoring Phase 7 spec MUST NOT include visual gate evaluation."

### F-10. Spatial-gauntlet integration gap

**Pattern:** `kit_archive` (Phase 4 ACCEPTED kits substrate) does NOT natively feed `gauntlet_sim.py` (1D scalar-distance production gauntlet executor) without an explicit bridge module. `spatial_gauntlet/` (R2 2D spatial combat research substrate) is a CONCURRENT-but-distinct system — neither replaces the other; both run. Without bridge, Wave 5 production season cannot execute Phase 7 2-layer joint-gate because cohort-level KPM measurement on ACCEPTED kits has no executable path.

**Watch:** Phase 7 IMPLEMENTATION dispatch landing at `agentic_orchestration/dispatches/2026-05-27-gamora-phase-7-implementation-bridge.md` (gamora primary; ~1-2 weeks estimated; LOAD-BEARING gating Wave 5); gamora Pattern A-light response 2026-05-27 (5-question architectural query) is the detection record.

**Counter:** Bridge module per Phase 7 IMPL dispatch — explicit `kit_archive` ACCEPTED → `gauntlet_sim.py` encounter sweep → cohort KPM measurement pipeline. Bridge is a NAMED component (not "while we're at it" implicit infrastructure); dispatch acceptance criteria include bridge contract surface + smoke test on small ACCEPTED cohort before Wave 5 fires. **Composition with F-5 joint-gate threshold drift:** F-10 is the integration prerequisite that lets F-5 fire empirically — without the bridge, threshold calibration has no execution surface; with the bridge, F-5 watch (Wave 5 smoke threshold-pass-rate measurement) becomes actionable.

**Surfaced via:** gamora Pattern A-light response 2026-05-27 (5-question architectural query about `spatial_gauntlet/` vs `gauntlet_sim.py` integration semantics). RECOGNIZED 2026-05-27; CLOSES at Phase 7 IMPL dispatch landing.

---

## 2. Scope creep to anticipate (4 risks)

### S-1. Phase 8 multi-profile export creep

**Pattern:** "Let's add Profile B B2B SaaS export while we're implementing Reincarnated v1 export." Cycle 15+ commercial work.

**Watch:** Out-of-scope guard in every Phase 4 + 5 + 7 + 8 dispatch; Cycle 14 ships Reincarnated v1 export only via existing star-lord Track C.

**Counter:** Path 1 record § 3.5 explicit deferral; KR dispatch authoring includes out-of-scope section; gandalf design-quality audit checks at Phase 8 wave-close.

### S-2. Wave 4 T4-attuned gear cohesion × Phase 5 cohesion cascade

**Pattern:** Wave 4 T4-attuned gear cohesion + Phase 5 multimodal cohesion + Phase 7 gate could cascade scope — gear cohesion uses Phase 5 LLM; Phase 7 gate evaluates composition; iterations re-run.

**Watch:** Wave 4 dispatch bounds gear cohesion scope; Phase 7 dispatch composition explicitly named (mechanical AND cohesion); not multi-iteration.

**Counter:** Phase 7 fires ONCE per kit (not re-iterative); Wave 4 gear cohesion is GEAR-side cohesion, separate from KIT-side cohesion at Phase 5; jack-ryan Gate-1 verifies scope bounds.

### S-3. Monster-contrast pipeline (P5b) creep into Phase 5

**Pattern:** `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` § 2.2 names monster-contrast pipeline as post-faction-coalescence stage. Cycle 15+ explicitly. Sub-agents implementing Phase 5 multimodal might pull monster-contrast in scope.

**Watch:** Phase 5 multimodal dispatch (per Path 1 record § 3.2) explicit out-of-scope-guards monster-contrast pipeline.

**Counter:** Phase 5 dispatch text: "**Monster-contrast pipeline (P5b) DEFERRED to Cycle 15+**; Phase 5 Cycle 14 scope = multimodal clustering + faction-coalescence + cohesion-judge naming only."

### S-4. Visual style register validation creep into Phase 7

**Pattern:** Currently Phase 6 territory. Phase 7 2-layer dispatch might pull visual register validation into "cohesion" layer.

**Watch:** Phase 7 dispatch bounds "cohesion layer" to Phase 5 cohesion-judge output ONLY (not visual register compliance).

**Counter:** Phase 7 dispatch text: "**Visual style register validation = Phase 6 territory**; Phase 7 2-layer cohesion gate evaluates Phase 5 cohesion-judge threshold only."

---

## 3. Design drift to anticipate (5 risks)

### D-1. Substrate-led discipline erosion via designer-curation overrides

**Pattern:** "But I want this specific kit to survive Phase 4 reject" — designer (gandalf or Matt) wants to override math gate verdict. Substrate-led discipline says math gates are AUTHORITATIVE; overrides are discipline violations.

**Watch:** Any in-flight design-call to override math gate verdict; framing-refusal authority (Discipline #44) empowers sub-agents to surface; gandalf design-quality audit checks.

**Counter:** Discipline #41 (pre-authored taxonomy interrogation) + Discipline #46 § 7 (math gates AUTHORITATIVE) + Discipline #45 (substrate-anchored vocabulary). If override genuinely needed, requires explicit Matt-gate at design-call level, not silent override in code.

### D-2. Faction concept becoming pre-authored

**Pattern:** Designer wants to lock "the seasonal theme is Crimson Court vs Verdant Reach" as input to Phase 5 multimodal clustering. This is class-concept-redux at faction level — pre-authored taxonomy violating substrate-led discipline.

**Watch:** Any in-flight design surface that pre-authors faction names BEFORE multimodal clustering produces them post-hoc.

**Counter:** Discipline #41 applies; faction labels emerge POST-HOC from substrate clustering; gandalf design-quality audit at Phase 5 wave-close greps for pre-authored faction taxonomies; Discipline #45 vocabulary lock enforces "faction labels emerge from clustering."

**Composition note:** seasonal-brief CAN bias toward target K (Design Call A1/A2/A4) but cannot pre-author specific faction NAMES or MEMBERSHIPS. Bias + emergence is OK; pre-authoring is not.

### D-3. Phase 4 archive becoming "the canonical kit library" via accumulation

**Pattern:** If archive persistent across seasons (Design Call B = cross-season or B1 hybrid), archive grows into de facto canonical kit library by accumulation. Over many seasons, archive becomes the substrate-evidence-of-record.

**Watch:** Design Call B ratification determines persistence; if persistent, Discipline #46 § 7 per-cell bounding is CRITICAL + archive eviction policy + cross-season eviction implications.

**Counter:** Per-season archive (Design Call B per-season-reset) avoids this entirely; B1 hybrid (per-season archive + persistent Court archive) bounds the persistent surface to ASCENDED Spirits only (Court accumulation; not all-kits accumulation).

### D-4. Phase 5 LLM becoming the design oracle

**Pattern:** Phase 5 LLM doing naming + faction-coalescence + cross-kit clustering accumulates too much authority. Algorithm should decide cluster MEMBERSHIP; LLM only NAMES clusters.

**Watch:** Math Note PM-1 (Multimodal Clustering Algorithm) specifies clustering happens at ALGORITHM level (deterministic; reproducible); Math Note PM-2 (Faction-Label Assignment) specifies LLM only NAMES post-clustering clusters.

**Counter:** Separation enforced in math notes; gandalf design-quality audit at Phase 5 wave-close verifies LLM doesn't decide cluster membership; jack-ryan Gate-2 grep audit verifies clustering is algorithm-side (no LLM call in clustering code path).

### D-5. Phase 7 joint-gate becoming theological

**Pattern:** "all kits must pass mechanical AND cohesion AND visual" sounds clean but failure handling is unclear — if cohesion gate fails an otherwise-good kit, what happens? Re-roll? Edit? Discard?

**Watch:** Design Call E (Phase 4 reject handling) + Phase 7 HELD verdict policy ratification at Matt-gate; Phase 7 dispatch (per Path 1 record § 3.3) specifies HELD-kit handling.

**Counter:** Phase 7 dispatch text explicit: "**HELD verdict triggers: (a) return to specific phase per design call E; OR (b) discard; OR (c) human review per gandalf design-quality audit. NO silent re-roll loops.**"

---

## 4. Audit triggers + composition with disciplines

Each pattern above composes with specific disciplines. Audit table:

| Pattern | Discipline that catches it | Where it fires |
|---|---|---|
| F-1 Math methodology drift | Discipline #18 (math-hotspot routing) + #11 (empirical inspection) | jack-ryan Gate-1 + Gate-2 |
| F-2 Per-cell capacity blowup | Discipline #46 § 7 (per-cell bounding) + Design Call C | jack-ryan Gate-2 grep audit |
| F-3 Faction cardinality drift | Discipline #43 (design-quality audit at wave-close) | gandalf design-quality audit at Wave 5 close |
| F-4 Phase 5 LLM volume drift | Discipline #11 (empirical inspection) + star-lord telemetry | star-lord LLM-call telemetry sidecar |
| F-5 Joint-gate threshold drift | Discipline #11 (empirical inspection) + Discipline #43 | gandalf design-quality audit at Phase 7 close |
| F-6 Class concept resurrection | Discipline #45 (vocabulary lock) + Discipline #42 (framing-audit) | gandalf design-quality audit + sub-agent framing-audit at session-start |
| F-7 Phase 6 implicit creep | Discipline #43 + KR dispatch out-of-scope guards | jack-ryan Gate-1 + gandalf design-quality audit |
| F-10 Spatial-gauntlet integration gap | Phase 7 IMPL dispatch (bridge module) + Discipline #11 (empirical inspection) + composes with F-5 | jack-ryan Gate-1 on Phase 7 IMPL dispatch + gamora smoke-test on bridge before Wave 5 |
| S-1 Phase 8 multi-profile creep | KR dispatch out-of-scope guards + Discipline #43 | jack-ryan Gate-1 |
| S-2 Wave 4 × Phase 5 cascade | KR dispatch scope bounds + Discipline #43 | jack-ryan Gate-1 |
| S-3 Monster-contrast P5b creep | KR dispatch out-of-scope guards | jack-ryan Gate-1 |
| S-4 Visual register creep | KR dispatch out-of-scope guards | jack-ryan Gate-1 |
| D-1 Substrate-led erosion via override | Discipline #41 + #46 § 7 + #45 | gandalf design-quality audit |
| D-2 Pre-authored faction taxonomy | Discipline #41 (pre-authored taxonomy interrogation) | gandalf design-quality audit at Phase 5 close + framing-audit at dispatch consumption |
| D-3 Archive becoming canonical library | Design Call B ratification + Discipline #46 § 7 | Math-note Matt-gate ratification |
| D-4 Phase 5 LLM as oracle | Math-note separation + Discipline #43 | gandalf design-quality audit at Phase 5 close |
| D-5 Phase 7 theological failure-handling | Design Call E ratification + Phase 7 dispatch HELD policy | Matt-gate ratification + Phase 7 dispatch authoring |

---

## 5. Composition with KR dispatch authoring

KR authors each Phase 4 / Phase 5 / Phase 7 / Phase 8 dispatch with **explicit reference to this register** in the dispatch's "Risks + Watch Items" section:

```markdown
## Risks + Watch Items (per gandalf path-1-failure-modes-scope-creep-drift-register)

This dispatch must guard against the following patterns (see register):
- [F-X] specific failure mode applicable to this dispatch
- [S-Y] specific scope creep applicable
- [D-Z] specific design drift applicable

Acceptance criteria include avoiding these patterns; gandalf design-quality
audit at wave-close (Discipline #43) verifies.
```

This composes with Move 1 (quality-criterion in every dispatch) — the quality-criterion's "refutation conditions" reference applicable register patterns.

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — failure-modes / scope-creep / design-drift register for Path (1) Cycle 14 execution
**Authority:** Matt 2026-05-27 "confirm execute on all three"
**Composition:** with Path 1 recognition record + Discipline #46 candidate + in-advance design calls record; composes with 12-discipline stack (esp. #41 pre-authored taxonomy interrogation + #42 framing-audit + #43 design-quality audit + #44 framing-refusal + #45 vocabulary lock + #46 DB anti-materialization) for full operational protection during Cycle 14 Path (1) work

**For:** the 17-pattern audit register for Cycle 14 Path (1) execution — 8 failure modes + 4 scope creeps + 5 design drifts — each with watch + counter + discipline composition. KR includes register references in Phase 4 + 5 + 7 + 8 dispatch authoring per § 5; gandalf design-quality audit (Discipline #43) at wave-close checks each pattern; framing-refusal authority (Discipline #44) empowers sub-agents to catch in-flight. Composes with Move 1 quality-criterion in every dispatch for operational discipline.

**Signed:** gandalf (story-and-design steward)
