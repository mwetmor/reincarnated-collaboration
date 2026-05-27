# Dispatch — 2026-05-27 — gandalf — Cycle 13 Wave 3 T4 Algorithm Phase 3 Design INTENT Canonical Authoring (Doc 44)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 2 Gate-2 PASS verdict (commit `0783860`) UNBLOCKS Wave 3 dispatch authoring + Wave 2 CLOSED + WARN-pattern REMEDIATED milestone
**Estimated effort:** 2-4 hrs canonical authoring (mirror doc 43 Wave 2 pattern but smaller scope; ~8-15KB; ~200-350 lines; Wave 3 is single Phase 3 not multi-phase like Wave 2)
**Acceptance:** NEW canonical doc 44 authored at `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` with character-wide vs chain-wide scope dimension operationalization + biggest-design-risk handling per doc 40 D81 Phase 3 framing + sub-wave structure W3.0-W3.X + composition with Wave 2 outputs + Wave 3 implementation guidance for rocket

## Context

Cycle 13 Wave 2 CLOSED 2026-05-27 (jack-ryan Wave 2 Gate-2 PASS verdict commit `0783860`; WARN-pattern FULL CLOSURE achieved). Wave 3 dispatch authoring is now UNBLOCKED.

Wave 3 = T4 algorithm Phase 3 implementation per framing brief § 3 Wave 3 + doc 40 D81 Phase 3 + closeout § 1.4 variable 3-or-4 chain architecture context. Per framing brief § 3 Wave 3 framing:

> **Phase 3 (character-wide vs chain-wide dimension) — doc 40 D81 Phase 3 framing as "biggest design risk" — dual-effect scope dimension is the variance generator**

Wave 3 introduces the SCOPE dimension to T4 architecture: each T4 capstone effect can target CHARACTER-WIDE scope (e.g., resource conversion across all chains) OR CHAIN-WIDE scope (e.g., chain-specific effect within one chain). This dimension was acknowledged in Wave 2 (3-category taxonomy + Wave 2 doc 43 § 2 references) but Phase 3 operationalizes the FULL implementation with both scope dimensions exposed.

This dispatch asks gandalf to author Wave 3 design INTENT canonical doc 44 operationalizing Phase 3 per framing brief + closeout + doc 40 + doc 43. Mirrors Wave 2 doc 43 pattern (gandalf design-spec → jack-ryan Gate-1 → rocket implementation → jack-ryan Gate-2).

**Per jack-ryan Wave 2 Gate-1 I5 routing (carryover):** SC-2 ratification (#31+#32) queue before Wave 3 — already CLOSED via jack-ryan commit `13e18a8` earlier this session. No carryover action needed; ratifications complete.

## Required reading before starting

1. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 precedent; design intent + sub-wave structure pattern; Wave 3 builds on top)
2. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (D81 Phase 3 architectural foundation; "biggest design risk" framing)
3. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition substrate)
4. `canonical/41-progression-framework-2026-05-27.md` (cell × node × cohort + L50 hybrid framework)
5. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.4 + § 2.4 (variable 3-or-4 chain architecture + 3-category T4 taxonomy substrate)
6. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` (Wave 2 close + WARN-pattern REMEDIATED milestone; verify any Wave-3-routing INFO from Gate-2)
7. Rocket Wave 2 implementation files (engine commit `2445bad`):
   - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (3-category taxonomy + chain config — Wave 3 builds on)
   - `reincarnated-engine/src/reincarnated/generation/t4_algorithm_wave2.py` (Wave 2 orchestrator — Wave 3 extends scope dimension)
   - `reincarnated-engine/src/reincarnated/generation/t4_option_f.py` (Option F retry orchestrator — Wave 3 inherits)
8. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 — all relevant for Wave 3)
9. `agentic_orchestration/operating-procedures/gandalf.md` (canonical-doc-format authority)
10. `agentic_orchestration/operating-procedures/canonical-doc-format.md` (canonical doc spec)

## Math-before-code (canonical authoring; no code)

NOT applicable — design intent authoring; no implementation code.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 44 is canonical design-intent artifact. (Wave 3 rocket implementation downstream WILL introduce cross-seam contracts via T4 scope dimension; downstream of THIS dispatch.)

## Scope

Author NEW canonical doc at: `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md`

Mirror doc 43 structure but smaller scope (Wave 3 is single Phase 3 not multi-phase):

### Required sections (proposed; gandalf seam-owner adjusts as needed)

- [ ] **§ 0 TL;DR + § 1 architectural foundation cross-references** — doc 38 + 39 + 40 amended + 41 + 42 + 43 amended + closeout doc + Wave 2 implementation as authority basis
- [ ] **§ 2 — Character-wide vs chain-wide scope dimension operationalization** (per doc 40 D81 Phase 3 + closeout § 1.4):
  - Character-wide scope: T4 capstone effect applies to ALL chains in kit (e.g., resource conversion affecting all skills); composes with Category A (class mechanical/energy alteration)
  - Chain-wide scope: T4 capstone effect applies to single chain (own-chain or parallel-chain per Wave 2 parallel-chain reach); composes with Categories B/C
  - Dimension is variance generator — most T4 capstones can be EITHER scope; specific scope decision per generation step
- [ ] **§ 3 — Per-category scope-dimension applicability** — Category A (class mechanical/energy) inherently character-wide; Categories B (chain multiplicative) + C (chain element conversion/addition) chain-wide by default but parallel-chain reach extends; cross-reference Wave 2 doc 43 § 2/§ 3/§ 4 + Wave 2 t4_category_schema.py implementation
- [ ] **§ 4 — Scope-dimension selection algorithm** — when generating T4 for chain:
  - For Category A: scope is inherently character-wide (fixed)
  - For Categories B/C: scope is chain-wide; parallel-chain reach (own-chain vs parallel-chain) is sub-dimension already implemented Wave 2 W2.3
  - Phase 3 introduces: additional scope variation cases / scope-conflict resolution / scope-interaction with one-T4-at-a-time gating per closeout § 1.3
- [ ] **§ 5 — Biggest-design-risk handling** (per doc 40 D81 Phase 3 framing) — surface what makes Phase 3 the biggest design risk:
  - Scope-dimension interaction with parallel-chain reach (Wave 2) — potential combinatorial explosion
  - Scope-dimension interaction with cohort archetypes (Block C) — different cohorts prefer different scopes
  - Scope-dimension interaction with one-T4-active gating (closeout § 1.3) — only one T4 active → scope-dimension selection has higher consequence per kit
  - Risk mitigation: spec how Phase 3 algorithm bounds the design space (e.g., per-archetype scope-dimension defaults; cohort-archetype-driven scope-preference)
- [ ] **§ 6 — Composition with Wave 2 outputs** — Phase 3 builds on Wave 2:
  - Uses t4_category_schema.py 3-category taxonomy
  - Uses t4_synergy_scan.py compositional synergy scan (Pass 1 resolve + Pass 2 preserve; 5-category framework)
  - Uses t4_option_f.py Option F retry mechanism
  - Uses t4_algorithm_wave2.py orchestrator extended with scope-dimension
  - Inherits all Wave 2 critical fold-ins (legendary_t0_5 round-trip; Pattern 9+10 stubs; etc.)
- [ ] **§ 7 — Sub-wave structure W3.0-W3.X for rocket implementation** (mirror Wave 2 W2.0-W2.9 pattern but smaller; ~5-7 sub-waves):
  - **W3.0** — Substrate prep + repo-scaffold (review Wave 2 outputs)
  - **W3.1** — Scope-dimension schema extension (Category A inherently character-wide; Categories B/C chain-wide; field on T4CandidateV2 or new T4CandidateV3)
  - **W3.2** — Per-category scope-dimension applicability implementation
  - **W3.3** — Scope-dimension selection algorithm + biggest-design-risk mitigation (per-archetype defaults; cohort-archetype-driven preference)
  - **W3.4** — Cross-cohesion validation per #26 + Block C scaffolding (extend Wave 2 W2.8 to include scope-dimension variance)
  - **W3.5** — Round-trip smoke per Principle 6 (including any new scope-dimension-driven rarity surface; preserve legendary_t0_5 coverage from Wave 2)
- [ ] **§ 8 — Wave 3 implementation guidance for rocket** — concrete next-steps; integration with Wave 2 schema; Wave 4 spec-driven gear gen will consume scope-dimension at gear-attunement time
- [ ] **§ 9 — Wave 3 close criterion** — jack-ryan Gate-2 PASS on rocket Wave 3 implementation; ready to feed Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling
- [ ] **§ 10 — Composition with locked architecture** — full composition table
- [ ] **§ 11 — Discipline #23 framing-audit section** (per doc 42 § 11 + doc 43 § 11.9 precedent — INCLUDE FROM START; jack-ryan flagged its absence as W1 amendment in Wave 2 Gate-1)
- [ ] **§ 12 — Sign-off** — gandalf authored; jack-ryan Gate-1 critique fires post-authoring; rocket Wave 3 implementation per Wave 3 dispatch

### Discipline compose-check

- [ ] #1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 — all relevant; compose throughout
- [ ] **#23 framing-audit INCLUDED FROM START** (don't repeat W1 amendment pattern from Wave 2 Gate-1)
- [ ] **WARN-pattern REMEDIATED status** — Wave 2 closed the pattern; maintain Wave 3 implementation expectation: 100% accurate post-script empirical count assertions

## Acceptance criteria

- [ ] NEW canonical doc 44 authored at `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md`
- [ ] All 12 sections complete per § Required sections itemization (gandalf seam-owner may adjust count + structure as needed)
- [ ] § 11 Discipline #23 framing-audit section INCLUDED FROM START (no W1 pattern repeat)
- [ ] Cross-validate against doc 43 amended (no contradiction; doc 44 builds on Wave 2 outputs)
- [ ] Tag intent: `gandalf: Cycle 13 Wave 3 T4 algorithm Phase 3 design intent canonical (doc 44)`
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Rocket Wave 3 implementation (separate dispatch post-Gate-1)
- Jack-ryan Gate-1 critique on doc 44 (separate dispatch post-authoring)
- Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling (separate)
- Wave 5 gauntlet sim + season gen + close (separate)
- Gamora SC-7 methodology consultation FULL (post-Wave-3-baseline per #18.2 — fires AFTER Wave 3 close, not before)
- Doc 40 / 41 / 42 / 43 modifications (cross-seam gandalf authority)
- Production code modifications
- decisions-log entries (separate jack-ryan work if architectural drift surfaces)

## Open questions for the agent to resolve

- Doc numbering: 44 next available; confirm or pick alternate
- Section count: 12 proposed; adjust per Wave 3 scope (smaller than Wave 2 doc 43 14-section)
- Sub-wave structure granularity: W3.0-W3.5 proposed (6 sub-waves; smaller than Wave 2 W2.0-W2.9 10-sub-wave); adjust per scope-dimension scope
- Biggest-design-risk handling spec depth: full risk-mitigation algorithm vs design-intent-only + delegation to gamora SC-7 (post-Wave-3-baseline per #18.2); your seam-owner call
- T4CandidateV3 vs T4CandidateV2 extension: full new schema vs field addition to V2; your call

## References

- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 precedent)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` (Wave 1 precedent)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (D81 Phase 3 + biggest design risk)
- `canonical/41-progression-framework-2026-05-27.md`
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.3 + § 1.4 + § 2.4
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` (Wave 2 close + WARN-pattern REMEDIATED)
- Rocket Wave 2 implementation files (engine commit `2445bad`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (all relevant disciplines)

---

**Cycle:** 13
**Wave:** 3 design intent
**Gates:** jack-ryan Wave 3 Gate-1 critique on doc 44 → rocket Wave 3 implementation dispatch authoring (post-Gate-1 PASS) → Wave 3 close (post-rocket-implementation Gate-2) → unlocks Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling + gamora SC-7 methodology consultation FULL per #18.2
**Priority:** P1 — critical-path Wave 3 start

---

## Completion record — 2026-05-27

**Completed by:** gandalf (story-and-design steward)
**Status:** COMPLETE
**Output:** `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` (557 lines; 13 § headings § 0-12 inclusive)

### Acceptance verification

- [x] NEW canonical doc 44 authored at `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md`
- [x] 13 sections complete (§ 0 TL;DR + § 1 architectural foundation + § 2 scope dimension operationalization + § 3 per-category applicability + § 4 selection algorithm + § 5 biggest-design-risk handling + § 6 composition with Wave 2 + § 7 sub-wave structure W3.0-W3.5 + § 8 implementation guidance + § 9 close criterion + § 10 composition with locked architecture + § 11 framing-audit + § 12 sign-off) — adjusted from dispatch's proposed 12 to 13 (added § 0 TL;DR as standalone section per Wave 2 doc 43 precedent)
- [x] **§ 11 Discipline #23 framing-audit INCLUDED FROM START** (no W1 amendment pattern; doc 44 establishes the from-start expectation as Wave 3+ baseline per § 11 first-canonical-example anchor)
- [x] Cross-validated against doc 43 amended (no contradiction; doc 44 builds on Wave 2 outputs via § 6 composition table + § 8.1 substrate consumption + § 8.5 schema-coherence guidance)
- [x] Tag intent: `gandalf: Cycle 13 Wave 3 T4 algorithm Phase 3 design intent canonical (doc 44)`
- [x] Round-trip: not applicable — no cross-seam contract change in canonical authoring; Wave 3 rocket implementation downstream WILL introduce additive cross-seam contracts (acknowledged in doc 44 § 8.4)
- [x] Ground-state oracle § 1 updated with new CURRENT entry for doc 44

### Empirical count verification (Discipline #11; maintain WARN-pattern REMEDIATED milestone)

| Asserted item | Asserted | Empirical (verified via `grep -cE` / `grep -E ... | wc -l`) | Status |
|---|---|---|---|
| § headings (§ 0-12) | 13 | `grep -cE "^## "` = 13 | PASS |
| Sub-waves (W3.0-W3.5) | 6 | `grep -E "^\| \*\*W3\." \| wc -l` = 6 | PASS |
| Total line count | (informational) | `wc -l` = 557 | PASS |

### Open-questions resolution (dispatch § Open questions)

| Question | Resolution |
|---|---|
| Doc numbering | Doc 44 (next available; confirmed) |
| Section count | 13 (dispatch proposed 12; gandalf adjusted to 13 by treating § 0 TL;DR as standalone section per Wave 2 doc 43 14-section precedent of § 0 + § 1-13) |
| Sub-wave structure granularity | W3.0-W3.5 (6 sub-waves; matches dispatch proposal; smaller than Wave 2 W2.0-W2.9 10-sub-wave per smaller Phase 3 scope) |
| **Biggest-design-risk handling spec depth** | **FULL design-intent + 4-mitigation bundle (architectural bounding + Pattern 9+10 scope-amplification detection extension + one-T4-active gating composition + gamora SC-7 calibration delegation per #18.2).** Threshold tuning delegated to gamora SC-7 post-baseline per #18.2; Wave 3 ships starting estimates. Rationale: Wave 3 IS Phase 3 ("biggest design risk" per D81); half-spec'd would defeat the purpose AND would push design-intent decisions out of gandalf scope onto rocket implementation where they don't belong |
| **Scope-dimension selection algorithm spec depth** | **FULL 6-step algorithm spec (§ 4: applicability bound + cohort prior + per-scope synergy scan + cohort-weighted score selection + magnitude downscaling + Option F Retry 4 scope-flip).** Calibration parameters (cohort priors numerics + magnitude downscaling formula + Pattern 9+10 thresholds + tie-breaker tolerance) ANCHORED with starting estimates per Verdict-B.4-pattern; gamora SC-7 iterates post-baseline per #18.2 |
| T4CandidateV2 vs T4CandidateV3 extension | **Field addition to V2** (per § 2.4 + § 8.5; mirrors Wave 2 W2.3 `parallel_chain_mode` precedent; preserves Wave 2 contracts; schema-coherence guidance per § 8.5 Option A vs Option B with Option A recommended) |

### Discipline composition verification

- #1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 — all composed throughout (per § 10 composition table)
- #23 framing-audit INCLUDED FROM START per § 11 (NO W1 amendment pattern repeat)
- WARN-pattern REMEDIATED milestone PRESERVATION expectation embedded in § 8.3 + § 9 close criterion (Wave 3 implementation: 100% accurate post-script empirical count assertions; module-load `assert len(X) == N` pattern preserved from Wave 2 rocket discipline)

### Hand-off

- **jack-ryan Wave 3 Gate-1 critique on doc 44** is the next gate (separate dispatch fires from knight-rider)
- After Gate-1 PASS: rocket Wave 3 implementation dispatch authoring (per § 7 sub-wave structure + § 8 implementation guidance)
- After Wave 3 close: Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling + gamora SC-7 methodology consultation FULL per #18.2

**Commit:** see `gandalf: Cycle 13 Wave 3 T4 algorithm Phase 3 design intent canonical (doc 44)` per tag intent
