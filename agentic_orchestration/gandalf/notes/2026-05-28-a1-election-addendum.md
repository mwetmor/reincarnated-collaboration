# A1 Election Addendum — T1 Measurement-Context Decision

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward)
**Mode:** Pattern B Matt-elected decision; addendum to prior adjudication record
**Status:** LOCKED — Matt 2026-05-28 sign-off; KR election prompt drafted
**Authority:** Matt 2026-05-28 (this Pattern B session — A1 elected following gandalf design-lead recommendation + ARPG-genre lineage analysis)

**Anchor docs:**
- `agentic_orchestration/gandalf/notes/2026-05-28-phase-4-rerun-3-adjudication.md` (parent adjudication record; R1/R2/R3/R4 disposition)
- `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` (Discipline #42 architectural case; this session)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 (two-layer T4 architecture; Q6 DDA 1.75× scope)
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.8.9 (Primary EXEMPT discipline)
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` § 4.4 (BVV calibration anchor / W-α3 lineage)
- `canonical/story/c-hybrid-cell-and-curation-architecture-2026-05-28.md` (load-bearing architecture; § 1.1 amended this session per BC axis expansion)

---

## 1. Election

**A1 LOCKED:** T1 close-criterion measured at base-context (DDA off). Original measurement semantics restored. Cross-path equity measured at the layer where equity belongs (raw cohort DPS before context-specific amplification at the in-game Primary T4 Capstone layer).

## 2. Layer separation locked

Two architectural layers, previously tangled by T1-T5 vs in-game-T1-T4 naming overlap, now canonically separated:

| Layer | Measurement / production | Disposition |
|---|---|---|
| In-game Primary T4 Capstone (DIRECT_DAMAGE_AMPLIFICATION 1.75× at preferred_encounter_type) | Production layer; design intent | UNCHANGED — universal-EXEMPT from T4 close-criterion; canonically scaffold-Cycle-15-RETIREMENT per Discipline #40 |
| In-game Secondary T4 Capstone (per-kit cohort-relative peak variants) | Production layer; design intent | UNCHANGED — canonically deferred to Cycle 16+ BC axis expansion per c-hybrid § 1.1 |
| Close-criterion T1 (cross-path DPS equity) | Measurement layer | A1 ELECTED — measured at base context (DDA off); semantic stability restored |
| Close-criterion T2 (zero-KPM at any encounter type) | Measurement layer | UNCHANGED — must pass at all profiles (gamora R3-prime hotfix Component B addresses profile-asymmetric band lower-bound) |
| Close-criterion T3 (saturation / structural) | Measurement layer | UNCHANGED — universally passes |
| Close-criterion T4 (Secondary T4 specialization peaks) | Measurement layer | UNCHANGED — DROPPED as Cycle 14 close-gate; canonically deferred to Cycle 16+ measurement framework |
| Close-criterion T5 (floor violations) | Measurement layer | UNCHANGED — universally passes |

**Effective Cycle 14 v1 MVP close-criterion (locked):** T1-base-context + T2-all-profiles + T3 + T5 = 4/4 required. T4 explicitly deferred.

## 3. Naming-amendment candidate (canonical close-criterion capture work)

The T1-T5 close-criterion naming overlaps visually with in-game T1-T4 skill-tier vocabulary. While the engine currently only uses in-game T4 Capstone explicitly, future cycles may introduce in-game T1-T3 skill-tier vocabulary, at which point the overlap becomes load-bearing confusion.

**Proposal:** rename close-criterion to C1-C5 (or Target-1 through Target-5) at canonical close-criterion capture. Disambiguates measurement vocabulary from in-game vocabulary. Bounded scope; mechanical rename across doc 47 + doc 51 amendment notes + future close-criterion records.

**Disposition:** raised for KR sequencing consideration at canonical close-criterion capture step. Low-priority but cheap. Defer to KR judgment whether to fold into Cycle 14 close-criterion capture or schedule as Cycle 15 entry housekeeping.

## 4. Sequence dependencies

A1 election unblocks the following dispatch sequence:

| # | Dispatch | Owner | Cost estimate | Dependency |
|---|---|---|---|---|
| 1 | T1 measurement-context amendment to BVV harness (T1 explicitly base-context per restored semantics) | gamora (harness seam) | ~30 min | A1 elected |
| 2 | R3-prime hotfix Component B — band lower-bound recalibration for low/mid/mixed_v1/mixed_v3 profile-asymmetry | gamora | ~30-60 min | Sequenced after #1 (avoids T1 amendment interaction with band-calibration changes) |
| 3 | Phase 4 RE-RUN-5 — verify amended close-criterion (T1-base + T2-all-profiles + T3 + T5 = 4/4) | gamora (sweep execution) | ~80s + result analysis | #1 + #2 complete |
| 4 | Canonical close-criterion capture (doc 47 § 4.6 + doc 51 § 10.8 amendment notes; layer separation + T1 base-context semantics + naming-amendment consideration) | gandalf (sub-agent at KR invocation) | ~half-day | #3 PASS |
| 5 | jack-ryan Gate-2 wave-close review + Discipline #42 canonical ratification with gandalf pushback memo as input | jack-ryan | ~half-day | #4 complete |
| 6 | Cycle 14 v1 MVP closure record | KR (state-file + closure record) | ~1-2 hours | #5 PASS |

## 5. Discipline #42 framing-audit ratification — load-bearing now

Three same-cycle empirical instances + one prior canonical precedent constitute the empirical evidence for Discipline #42 canonical ratification. Gandalf pushback memo at `gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` provides the architectural argument. jack-ryan canonical-write authority at Gate-2 (dispatch #5 above).

**Gandalf-side commitment:** OP § 4.1 framing-audit checklist will reference Discipline #42 as canonical anchor post-ratification.

## 6. Operational constraints continuing

Discipline #47 candidate (host-RAM-aware operational concurrency) remains active. R47.1-R47.5 per gandalf incident note § 6. Single-seam sub-agent at a time; no parallel fan-out while sweep is resident. Pre-flight vm_stat confirmation before each sweep fire.

---

## 7. Design-lead conviction record

A1 election preserves the architectural layer separation that Reincarnated's design depends on. The genre lineage (D2 / D3 / D4 / PoE / Last Epoch / Grim Dawn + isekai analog) consistently treats path-shines-at-content asymmetry as the design pattern, not aggregate cross-path equity at endgame-amplified measurement. T1 in base context measures equity at the layer where equity belongs; in-game Primary T4 Capstone delivers asymmetry at the layer where the genre's appeal lives; in-game Secondary T4 Capstone (Cycle 16+ scope) will deliver cohort-relative peak identity.

A2 (normalize T1 in DDA context) would have re-litigated T4's axis with different math — methodology bloat without solving the design question. A3 (drop T1 entirely or replace with DDA-aware variance metric) would have lost the base-layer regression catcher T1 was designed to provide. A1 is the honest call — fastest path to v1 MVP close, cleanest layer separation, genre-aligned design conviction.

**Signed:** gandalf (story-and-design steward)
**For:** the A1 election addendum locking T1 base-context measurement semantics, the canonical layer separation, the naming-amendment candidate, the dispatch sequence dependencies, and the Discipline #42 ratification readiness for jack-ryan Gate-2.
