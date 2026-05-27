# Dispatch — 2026-05-26 — gamora — Cycle 13 Wave 0 Methodology Consultation Prep

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-05-26 — Cycle 13 framing brief § 4.1 KR autonomous (sidecar dispatching) + Q6 ratification (gamora consultation gates Wave 4) + hive-mind decision-routing directive (seam-owner decides in-scope work)
**Estimated effort:** 4-8 hrs methodology prep (review + framework draft + gates enumeration)
**Acceptance:** methodology framework draft for Cycle 13 Phase 3 sim cycling + Phase 4 archive insertion that addresses doc 40 D84 hybrid cohort + edge-case sampling + per-legendary cohort anchoring; explicit "PRE-BASELINE-RESOLVABLE" vs "REQUIRES-WAVE-3-BASELINE" classification per Discipline #18.2

## Context

Cycle 13 Wave 4 = spec-driven gear gen + T4 algorithm Phase 4 (full sim cycling). Wave 4 is a math hotspot per Discipline #18 — methodology-before-execution requires gamora consultation BEFORE specialist execution. Per framing brief § 7 + doc 40 D84 + D85, the sim cycling is compute-heavy combinatorially (N kits × M T4 configurations × K stat-sheet partition compositions × L cohort archetypes × 4 progression nodes) and methodology choice is load-bearing for compute budget management.

**Discipline #18.2 amendment timing:** at extension hotspots (Wave 4 extends multi-T4 architecture), methodology consultation FULL execution fires AFTER baseline (Wave 3 close). This dispatch is the PREP — reviewing the math hotspot landscape NOW so the post-Wave-3 consultation closure is fast.

**Substantive design inputs already landed:**
- doc 40 D84 (hybrid cohort + edge-case sampling with per-legendary cohort anchoring; Sub-option A primary; Sub-option B fallback)
- doc 40 D62 (compute discipline — stratified sampling / tiered validation / quick-estimate hybrid / caching)
- doc 40 D85 (Cycle 13 all 4 phases of T4 algorithm wrap; Phase 4 = full sim cycling)
- doc 40 D27 (4 progression nodes — early game / mid game / endgame start / endgame [85% target])
- doc 40 D61 (playability gate — PLAYABLE-AND-IN-BAND validation; now Discipline #26)
- **gandalf Pattern A-deep verdicts (commit `c983173`, 2026-05-26):**
  - C.1 RATIFIED — power-level targets per progression node: **DELEGATE-TO-GAMORA-METHODOLOGY** per substrate-led + D1 + #18.2 (you decide; design-intent anchors gandalf authored as starting position)
  - C.2 RATIFIED — WR-bracket definition per cell + node: **DELEGATE-TO-GAMORA-METHODOLOGY** per same (you decide; design-intent anchors gandalf authored)
  - C.3 RATIFIED — cohort archetype definitions: **DELEGATE-TO-GAMORA-METHODOLOGY** + composes with new Discipline #30 (sim methodology naming)

**Disciplines in play:**
- **#18 methodology-before-execution** (foundational for this dispatch)
- **#18.2 methodology-consultation timing at extension hotspots** (PREP NOW; FULL consultation post-baseline)
- **#26 Playability** (PLAYABLE-AND-IN-BAND criterion; just landed)
- **#30 sim methodology naming** (NEW; methodology pattern must be named explicitly — composes with consultation output)
- **#19 Agent-tool-not-for-waiting** (parallel sub-agent invocation if needed)
- **#11 empirical inspection over assumption** (cite empirical evidence)

## Required reading before starting

1. `canonical/00-ground-state.md` (current epoch)
2. `canonical/02-roadmap.md` (engine build visual-flow tracker; § 4.3 Cycle 13 status)
3. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 4 (acquisition curve + multi-node calibration) + § 6 (T4 algorithm canonical form) + § 8 (D60-D86 incl. D84 hybrid cohort + D85 Phase 4 sim cycling + D62 compute discipline)
4. `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.5 (content lifecycle dependency chain — sim CONSUMES, doesn't generate) + § 3 (Phase 3 convergence)
5. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes operational truth)
6. `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (substrate-vector convergence math)
7. `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 7 (compute budget) + § 3 Wave 4 sequencing
8. `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` Blocks C.1/C.2/C.3 (your delegation inputs from gandalf)
9. `agentic_orchestration/cycles/cycle-13-mechanical-engine-build-scope.md` (full Cycle 13 scope-doc; § 12 fill-in checklist post-gandalf-verdicts)
10. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (current 30 disciplines incl. #26-#30 just landed)
11. `agentic_orchestration/operating-procedures/gamora.md` (your operating procedure — fight-engine + balance-loop + spirit-guide; methodology consultation pattern)
12. Existing simulation code reference paths (review your own seam): `reincarnated-engine/src/reincarnated/simulation/` for B14.5 V1 primary loop pattern + balance loop architecture + existing sim methodology
13. Existing convergence math: `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (W1.13 multi-dim convergence per Cycle 12 Layer 4)

## Math-before-code (methodology prep; no code)

NOT applicable — methodology framework prep + canonical-relevant documentation only. NO simulation runs at scale.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Methodology framework draft is design-intent output consumed at Wave 4 by you (gamora) + rocket (sim integration) + jack-ryan (Gate-1/Gate-2 review); no schema / fixture / boundary change.

## Scope

Produce methodology framework draft addressing:

### A. Sub-option selection (D84 framework choice)

- [ ] **A.1 — Sub-option A vs B vs Hybrid:** doc 40 D84 lays out Sub-option A primary (per-weapon cohort coverage) + Sub-option B fallback (per-legendary cohort selection) + hybrid framing. Your recommendation: which sub-option (or hybrid composition) for Wave 4 sim cycling?
- [ ] **A.2 — Naming per Discipline #30:** name the methodology pattern explicitly. Per #30 four-axis naming: node-population + edge-case + cohort + compute-burden. E.g., "hybrid-cohort-edge-case-anchored-per-legendary-with-stratified-sampling."
- [ ] **A.3 — Per-legendary cohort anchoring specifics:** how cohort coverage attaches to specific legendary items per D84

### B. Cohort archetype definitions (C.3 delegation input)

- [ ] **B.1 — DPS-min-maxer cohort:** investment patterns; gear preferences; KPM expectations; per-progression-node distribution
- [ ] **B.2 — Balanced cohort:** same dimensions
- [ ] **B.3 — Defensive cohort:** same dimensions
- [ ] **B.4 — Hybrid cohort:** same dimensions; explicit handling for hybrid-within-hybrid ambiguity per D84
- [ ] **B.5 — Cross-cohort overlap:** how cohorts interact with multi-T4 attunement (a kit with 3 T4 paths can be valid for multiple cohorts depending on attunement choice)
- [ ] **B.6 — Cohort granularity vs compute budget:** 4 cohort archetypes — is this right? Should some collapse? Should others split (e.g., DPS-glass-cannon vs DPS-survivor)?

### C. Power-level targets per progression node (C.1 delegation input)

- [ ] **C.1 — Per-node "in-band" definition:** numerical band per progression node (early game / mid game / endgame start / endgame [85% target]); reference existing balance bands from Cycle 12+ or propose new
- [ ] **C.2 — Banding shape:** flat-band-per-node vs gradient vs curve
- [ ] **C.3 — Cross-node validation:** how a single kit validates across all 4 nodes (does it need to fall in-band at ALL nodes, or only its target node?)
- [ ] **C.4 — Calibration anchoring vs empirical iteration:** does this dispatch ANCHOR initial numerical targets OR delegate to first-cycle empirical iteration per D1 substrate-led + balance-as-property?

### D. WR-bracket definition per cell + node (C.2 delegation input)

- [ ] **D.1 — Bracket math:** ±X% WR around target per cell × node; X depends on cell type / cell rarity / progression node
- [ ] **D.2 — Cross-cell consistency:** how WR-brackets interact across the 5-tuple BC-target subspace
- [ ] **D.3 — Failure mode:** what does WR-bracket FAIL look like in sim output (per gandalf Q10 amendment: "all characters within WR bracket" = those that pass form the season)

### E. Compute discipline (doc 40 D62)

- [ ] **E.1 — Stratified sampling design:** strata definition (per cell × per cohort × per node); sample size per stratum; statistical floor for confidence
- [ ] **E.2 — Tiered validation:** quick-estimate first; full-sim only on candidates that pass quick-estimate
- [ ] **E.3 — Caching strategy:** which intermediate computations cache; invalidation rules
- [ ] **E.4 — Compute budget projection:** N kits × M T4 × K cohort × 4 nodes — estimate compute hours given current single-fight runtime + parallelism budget; flag if budget exceeds available compute resource (per Discipline #1.1 pre-fire resource-bounds projection)

### F. Playability gate operationalization (Discipline #26 PLAYABLE-AND-IN-BAND)

- [ ] **F.1 — 6 sub-gate definitions per #26:** KPM in band + coherent rotation + resource flow + defensive uptime + no-degenerate-states + cognitive load manageable. Operationalize each: what does sim measure? What threshold passes/fails?
- [ ] **F.2 — Composition with WR-bracket:** playability gate operates per-kit; WR-bracket operates per-cell; how they compose at archive insertion (Phase 4)
- [ ] **F.3 — Degenerate-state detection:** per gandalf D.4 verdict (hybrid KPM-proxy + 3 validators) — specify the 3 validators

### G. Discipline #18.2 timing classification

For each item A-F:
- [ ] **PRE-BASELINE-RESOLVABLE:** can be designed NOW based on existing canonical + doc 40 + gandalf verdicts; goes into Wave 4 methodology framework
- [ ] **REQUIRES-WAVE-3-BASELINE:** needs Wave 3 T4 algorithm Phase 3 outputs (character-wide vs chain-wide variance) before methodology can close; flagged for post-Wave-3 finalization

### H. Output canonical doc

- [ ] Author methodology framework doc at `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` per gamora canonical-relevant notes pattern
- [ ] Structure: § 1 TL;DR + § 2 Sub-option choice (A) + § 3 Cohort definitions (B) + § 4 Power-level + WR-bracket (C+D) + § 5 Compute discipline (E) + § 6 Playability gate operationalization (F) + § 7 Pre-baseline vs post-baseline classification (G) + § 8 Open questions surfaced
- [ ] Tagged commit

## Acceptance criteria

- [ ] Methodology framework draft authored per H above
- [ ] All 6 sections A-F addressed; G classification applied
- [ ] D84 Sub-option choice + named methodology pattern per #30
- [ ] 4 cohort archetypes defined per C.3 delegation
- [ ] Compute budget projection per #1.1 (peak memory + estimated compute hours flagged against available resource)
- [ ] Playability gate per #26 operationalized into specific sim measurements + thresholds
- [ ] Pre-baseline vs post-baseline classification explicit per item
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- Running simulations at scale (this is methodology PREP; full Wave 4 sim execution is post-prep + post-Wave-3-baseline)
- Modifying simulation code (NO code changes in this dispatch)
- Modifying balance_loop.py or fight engine (audit + propose only)
- Phase 3 architecture decisions (Phase 3 is gandalf design intent + your methodology; this dispatch is methodology-only)
- Implementing playability gate code (operationalize design only)
- Anchoring numerical balance targets where empirical iteration is more appropriate (per substrate-led + balance-as-property D1 — flag where anchoring vs delegation is appropriate)

## Open questions for the agent to resolve

- D84 Sub-option choice: A primary, B fallback, hybrid per legendary — your call as seam owner
- Cohort granularity: 4 archetypes is gandalf's starting position; expand/collapse/split as your methodology requires
- Compute budget: if projected compute exceeds available, flag as REQUIRES-MATT-CREATIVE-RATIFICATION-ON-SCOPE (e.g., reduce season N OR reduce cohort granularity OR accept longer wall-clock)
- Power-level targets: anchor specific numbers (gandalf's design-intent anchors) OR empirical-iterate from first cycle (substrate-led); your call per #18.2
- #26 playability sub-gates: 6 are listed; you can operationalize as-is OR amend (your seam authority per #26 operationalization)

## References

- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 4 + § 6 + § 8 (D60-D86)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 3 + § 0.5
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` Blocks C.1/C.2/C.3 (your delegations)
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 7 (compute budget framing)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #18 + #18.2 + #19 + #26 + #30 + #11 + #1.1

---

**Cycle:** 13
**Wave:** 0 / Methodology consultation prep
**Gates:** Wave 4 sim cycling (full methodology execution post-Wave-3-baseline per #18.2)
**Priority:** P1 — last Wave 0 KR-autonomous parallel work-unit

---

## Completion record

**Completed:** 2026-05-26
**Author:** gamora
**Commit:** `115f2a6`

**Methodology pattern name (Discipline #30 — four-axis):**
> "Per-weapon-cohort-exhaustive with sub-option-B fallback for cohort-clear legendaries; stratified by progression node; tiered quick-estimate first validation"

Four axes: (1) node-population = per-weapon cohort coverage (Sub-option A primary) with per-legendary cohort selection (Sub-option B fallback for cohort-clear); (2) edge-case = per-legendary anchoring on tier-2 legendaries/sets + adversarial hybrid cohort inclusion; (3) cohort definition = 4 archetypes (DPS-min-maxer / balanced / defensive / hybrid) by investment-pattern + gear-preference + KPM-expectation-band; (4) compute-burden = quick-estimate filter first, full-sim on passers only, stratified sampling with statistical floor, intermediate caching.

**D84 sub-option choice:** Hybrid-within-hybrid. Sub-option A for legendaries where cohort attunement is mechanically ambiguous (generic damage modifier + triggered passive). Sub-option B for cohort-clear legendaries (T4-attunement strategy archetype forces single dominant cohort, OR modifier surface is exclusively single-cohort, OR capability toolkit is self-contained for one archetype). Discrimination heuristic designed as PRE-BASELINE-RESOLVABLE.

**Compute budget projection (Discipline #1.1):**
- Estimated tier-2 legendaries first season: 15-30
- Fights per kit: ~48-100 (quick-estimate pass filter + full-sim stratum)
- Total fight range: ~11,000-20,000
- Wall-clock at 0.34s/fight sequential: ~1-2 hours
- Peak memory: <5MB (fight-result accumulation only; no large in-memory matrices)
- Host RAM check: M2 8GB host; 5.0GB threshold per Discipline #1.1 (62.5%); <5MB WELL WITHIN threshold
- Status: WITHIN AVAILABLE RESOURCE — no scope reduction required

**Classification counts:**
- PRE-BASELINE-RESOLVABLE: 22 items (discrimination heuristic, cohort definitions, compute discipline structure, playability sub-gates 1/2/4/5, degenerate-state validators, WR bracket math structure, tiered validation approach, caching strategy)
- REQUIRES-WAVE-3-BASELINE: 12 items (numerical WR band thresholds, DPS-min-maxer bimodal split decision, power-level calibration anchors, playability sub-gates 3+6 hard thresholds, cross-cohort collapse candidates)

**Output artifact:** `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md`

**Acceptance criteria status:** All met. Methodology framework complete; all 6 sections A-F addressed; G classification applied; Discipline #18.2 constraint honored (full closure deferred to post-Wave-3-baseline).
