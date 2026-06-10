# Discipline-Recognition Candidate — Substrate-vs-Genre-Baseline Requires Target-vs-Watch-Flag Structure

**STATUS:** CURRENT (discipline-recognition candidate; jack-ryan ratification consideration at future cycle)
**Date:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** gandalf cross-cutting discipline-observation authority; surfaces empirical-observation pattern for jack-ryan ratification consideration per Discipline #18.2 amendment-candidate framework
**Routing:** jack-ryan reads at convenience; ratification consideration optional (non-blocking; bounded observation captured for cross-session continuity)
**Companion docs:**
- `canonical/story/2026-06-09-arpg-physical-magical-ratio-baseline.md` § 6 (where the observation was first captured)
- `agentic_orchestration/drax/notes/2026-06-09-forge-phase-3-close-report.md` § Observation 2 (where the discipline failure originated — physical-43% misread as imbalance)
- `agentic_orchestration/legolas/research/2026-06-09-arpg-physical-magical-ratio/synthesis.md` (the empirical baseline that surfaced the correct target-vs-watch-flag structure)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (where Discipline #18.2 lives if ratified)

---

## 0. TL;DR

**The recognition:** substrate-vs-genre-baseline questions require **target-vs-watch-flag structure**, NOT just min-max range.

**The discipline failure pattern observed:** during /forge Phase 3 close-routing 2026-06-09, the physical-43%-corpus observation iterated through 3 framings before landing on the correct disposition:

| Iteration | Framing | Failure mode |
|---|---|---|
| **1** | "43% physical is imbalance — corpus-rebalance to fix" | Treated substrate-imbalance generically without genre-baseline check |
| **2** | "43% is genre-correct (recall 40-55% range); may need to push UP toward 50-55%" | Treated the recalled genre range as FLAT (assumed mid-target was 47.5%); missed that the range has structure (central + target band + watch flags) |
| **3** | "43% is within spec at upper boundary; central is 37-40%; watch flag at 48%" — correct | Required Legolas Mode A empirical research to surface the target-vs-watch-flag structure |

**Candidate Discipline #18.2 amendment:** at substrate-vs-genre-baseline math hotspots, methodology consultation should produce target-vs-watch-flag structure (central + target band + watch flags), NOT just min-max range. The structure matters operationally — central guides aim; target band guides acceptance; watch flags guide drift-detection.

---

## 1. The recognition in detail

### 1.1 What happened

During /forge Phase 3 close-routing 2026-06-09, drax surfaced Observation 2: physical element comprises 428/1000 kits (43%) in the PROVISIONAL corpus. This was framed as YELLOW (potential imbalance worth Matt-direction).

**Iteration 1 (gandalf framing):** I treated the 43% as substrate-imbalance to fix via corpus-rebalance commission (engine-side workstream: gandalf design-spec → elrond/rocket execution; regenerate corpus with reduced physical share toward parity with 7 elementals).

**Matt correction:** "ARPG genre historical physical vs magical average... was somewhere between 40%-55% physical" — flagged that physical-43% is in-band for the recalled genre range, and that prior research on this baseline was lost.

**Iteration 2 (gandalf reframing):** I interpreted Matt's "40-55%" recall as a flat range, suggested the mid (~47.5%) might be the optimal target, and flagged that 43% sits BELOW that mid — "may need to push UP toward 50-55%."

**Legolas Mode A research (commissioned and completed same session):** empirical baseline surfaced from 8-ARPG survey is **physical-primary 37-40% central (range 32-47%); recommended Reincarnated target band 38-45%; watch flag >48% (warrior over-rep) / <32% (caster over-rep)**.

**Iteration 3 (correct):** 43% is within spec at the upper boundary of the recommended target band. Pushing UP past 48% would trigger the warrior-over-representation watch flag. The correct disposition is "no urgent action; monitor."

### 1.2 What the failure pattern looks like

Iteration 1's failure: didn't check substrate-imbalance against genre baseline at all. **Substrate-honesty without genre-context is just data-honesty.**

Iteration 2's failure: had the genre range (40-55% recall) but treated it as flat. Assumed mid-target was 47.5%. Missed that:
- Central estimate may NOT be mid-range (central can be near top or bottom of the band)
- Range may NOT be symmetrical (40-55% recall actually decomposed to 32-47% range with 37-40% central — left-skewed)
- Pushing toward "the middle of the range" can land in a watch-flag zone if the structure is asymmetric

Iteration 3's correctness: required EMPIRICAL methodology consultation (Legolas Mode A) to surface the target-vs-watch-flag structure. The structure couldn't be reasoned from min-max alone.

---

## 2. Discipline #18.2 amendment-candidate formulation

### 2.1 The proposed amendment

**Current Discipline #18.2 framing** (per gandalf OP § 4.2): methodology consultation fires AFTER baseline at extension hotspots.

**Proposed amendment:** at substrate-vs-genre-baseline math hotspots specifically, methodology consultation should produce **target-vs-watch-flag structure**, not just min-max range. The output structure must include:

1. **Central estimate** (most-likely value; the value to design around)
2. **Target band** (operational range for "in-spec"; tighter than the plausible range)
3. **Plausible range** (the absolute min-max bounds where data lives)
4. **Watch flags** (specific thresholds + signal interpretation when crossed)
5. **Current corpus position** (where the project sits in this structure NOW)

Each layer carries different operational meaning:
- Central = aim
- Target band = acceptance
- Plausible range = informational bounds
- Watch flags = drift-detection
- Corpus position = current-state diagnostic

### 2.2 When this discipline fires

The discipline applies when substrate-imbalance findings surface AND the imbalance is evaluated against external (genre / ARPG / cross-product) baselines. Triggers include:

- Corpus composition observations (element-family / weapon-family / archetype distribution)
- Build distribution observations (per-class / per-skill / per-T4 mix)
- Mechanical-output observations (DPS / KPM / TTK distribution vs genre cohort)
- Visual-content observations (sprite / VFX / asset distribution vs visual-register reference)
- Any "is X% imbalanced?" question where X is measured against external canon

### 2.3 What it does NOT change

This amendment does NOT change Discipline #18 (methodology consultation at math hotspots required) OR Discipline #18.2 (timing — consultation fires AFTER baseline at extension hotspots). It REFINES the OUTPUT STRUCTURE methodology consultations should produce at substrate-vs-genre-baseline hotspots specifically.

---

## 3. Composition with prior disciplines

| Discipline | Composition |
|---|---|
| **#18** (methodology consultation at math hotspots) | This is sub-discipline at the output-structure layer; #18 still governs WHEN consultation fires |
| **#18.2** (methodology consultation timing — post-baseline at extension hotspots) | This refines OUTPUT requirement; #18.2 governs TIMING |
| **#25** (semantic-layer rep-audit) | Composes — semantic ambiguity at substrate classification (e.g., bleed-as-physical-or-magical) requires per-game disposition documentation; target-vs-watch-flag structure absorbs Discipline #25 caveats at the classification layer |
| **#41** (pre-authored taxonomy interrogation) | Composes — target-vs-watch-flag structure naturally surfaces when substrate vs genre-baseline is measured; "what's the actual central?" question rejects pre-imposed assumption that mid-of-range is the target |
| **#59** (substrate-honesty at substrate vote layer) | Composes — substrate-honesty here means "honor the genre-empirical baseline structure"; just rendering substrate truth without checking against genre canon is incomplete substrate-honesty |

---

## 4. First-canonical-example (per gandalf OP § 4.5 pattern)

**The example:** /forge Phase 3 close-routing iteration 1 → 2 → 3 on the physical-43% question (2026-06-09).

**The cycle:**
- Drax Phase 3 close report surfaces Observation 2 (43% physical; YELLOW for Matt-direction)
- Gandalf iteration 1: misreads as imbalance; queues corpus-rebalance commission framework
- Matt correction surfaces lost prior research on 40-55% genre range
- Gandalf iteration 2: misreads recalled range as flat; suggests push toward 50-55%
- Matt commissions Legolas Mode A to re-establish empirical baseline
- Legolas synthesis surfaces target-vs-watch-flag structure (central 37-40% + target band 38-45% + watch flag >48% / <32%)
- Gandalf iteration 3: correctly disposes 43% as within-spec-at-upper-boundary; no action

**Total cost:** ~3 message-cycles + Legolas Mode A research (~30-45 min) to land correct disposition. Would have been ~1 cycle if iteration-1 had requested target-vs-watch-flag structure from the start.

**This is the FIRST CANONICAL EXAMPLE** of the discipline gap — observation of substrate-imbalance evaluated against external baseline WITHOUT requesting target-vs-watch-flag structure produced 2 sequential misreads before landing correct disposition.

**When to cite:** future substrate-vs-genre-baseline observations should cite this example as the canonical operational lesson — request target-vs-watch-flag structure at first iteration, not third.

---

## 5. Routing for jack-ryan ratification consideration

**This is a candidate, not a ratified discipline.** Jack-ryan owns canonical-write authority on `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` per ADR-002 + critique-pair role definition.

**Recommended jack-ryan disposition options:**
1. **Ratify as Discipline #18.3** — new sub-discipline under #18 at output-structure layer (target-vs-watch-flag structure for substrate-vs-genre-baseline hotspots)
2. **Amend Discipline #18.2 in-place** — extend #18.2 to cover BOTH timing (post-baseline at extension hotspots) AND output structure (target-vs-watch-flag at substrate-vs-genre-baseline hotspots)
3. **Defer** — observation captured; no immediate canonical ratification needed; future repeat-occurrence triggers re-evaluation
4. **Reject** — single-instance observation; not yet recurrent pattern warranting discipline-level capture

**Gandalf-side lean:** option (1) ratify as Discipline #18.3, OR option (2) amend #18.2 in-place. Both produce the same operational effect; (1) preserves clean separation of timing vs output-structure concerns; (2) keeps the discipline-count cleaner. Either is fine; jack-ryan's call.

**If jack-ryan defers (option 3) or rejects (option 4):** this sidecar remains as discipline-observation reference; future repeat-occurrence may trigger re-consideration.

---

## 6. Composition with prior canonical commitments

This sidecar is observational; preserves all prior canonical commitments without modification. No architectural-commitment changes.

---

## 7. Sign-off

**Authored:** gandalf 2026-06-09 at session close per Matt directive — "fire both, and we'll wind down" (optional sidecar named as cheap second authoring thread).

**Authority:** gandalf cross-cutting discipline-observation authority for surfacing empirical-observation patterns for jack-ryan ratification consideration.

**Routing:** jack-ryan reads at convenience (non-blocking); ratification consideration at future cycle; sidecar captured for cross-session reference regardless of ratification outcome.

**Empirical-evidence triggers for ratification re-evaluation:**
- Future substrate-vs-genre-baseline observation repeats the iteration pattern (failure mode recurs)
- Future engine-generation tuning workstream surfaces target-vs-watch-flag structure need
- Cycle 15+ Pattern B on substrate composition consumes this observation as discipline-anchor

**Composition with prior canonical commitments:** all preserved (observational sidecar; no architectural touch).

**End of discipline-recognition sidecar.**
