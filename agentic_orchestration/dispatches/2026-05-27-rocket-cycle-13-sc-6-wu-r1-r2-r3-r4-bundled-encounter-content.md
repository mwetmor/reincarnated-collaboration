# Dispatch — 2026-05-27 — rocket — Cycle 13 SC-6 WU-R1 + WU-R2 + WU-R3 + WU-R4 Bundled (Endgame Reference Encounter Content)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + gamora SC-6 audit recommendation + jack-ryan Gate-1 PASS-with-WARN verdict (commit `ae1a19a`) authorizing rocket implementation path
**Estimated effort:** 8-16 hrs bundled implementation (WU-R1 mob stat profile authoring ~3-4 hrs + WU-R2 18 encounter definitions ~4-8 hrs + WU-R3 archetype coverage verification ~1-2 hrs + WU-R4 deferred-cell scope record ~30 min)
**Acceptance:** L45-50+ endgame mob stat profile landed + 18 endgame-reference encounters authored against non-deferred BC-cell scope + archetype coverage verification for WR contract alignment + Cycle 14+ scope record for 7 proxy-deferred cells; integrates with `build_reference_gauntlet()` consumer

## Context

Gamora SC-6 GAP 2 audit (commit `3ced195`; memo at `gamora/notes/2026-05-27-sc-6-reference-encounter-audit.md`) returned BLOCKING-severity finding: **0 endgame-reference-encounters exist in current engine codebase**. Pre-existence gap, not partial coverage. ~22-25 NO-COVERAGE cells.

Jack-ryan Gate-1 critique (commit `ae1a19a`; finding at `qa/findings/2026-05-27-cycle-13-sc-6-gate-1-critique.md`) verdict: **PASS-with-WARN** (0 BLOCK / 3 WARN / 4 INFO). Audit substantively sound; gamora re-pass NOT required. 3 WARN amendments specified for fold-in to rocket dispatch authoring (this dispatch).

This dispatch bundles all 4 rocket work-unit specifications from gamora audit memo § Recommendation, with jack-ryan Gate-1 W1+W2+W3 amendments folded in. Bundling reduces context-load overhead + supports sequential WU-R1 → WU-R2 dependency (WU-R1 mob stat profile blocks WU-R2 encounter definitions).

## Required reading before starting

1. `agentic_orchestration/gamora/notes/2026-05-27-sc-6-reference-encounter-audit.md` (audit memo with full 18-encounter recommendation specifications + 4 WU specs; 24KB)
2. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-sc-6-gate-1-critique.md` (jack-ryan Gate-1 critique; 3 WARN amendments to fold in)
3. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 5.1 (GAP 2 architectural lock — 8-12 minimum / 15-22 optimal / ~30 max + each encounter exercises playability criterion D61 / #26)
4. `canonical/41-progression-framework-2026-05-27.md` § 3 (endgame node identity L45-50+ + Cycle 13 v1 endgame-only scope)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (just amended; reference for capability toolkit + T4 algorithm + multi-T4 architecture context for encounter difficulty calibration)
6. `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` § 1.4 (anchored intent for endgame: KPM ~75+ / HP endgame mob calibrated / defense uptime ≥80%) — encounter difficulty calibration target
7. `canonical/story/v1-bc-target-intent-2026-05-24.md` (Sketch A + ~22 v1 cells; verify per Gate-1 W1 amendment — 25-row 5-tuple vs 18-cell non-deferred 4-tuple key)
8. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes operational truth — encounter cell-mapping per axis)
9. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 code-citation + #11 empirical inspection + #18 methodology + #26 playability + #30 sim methodology naming)
10. `agentic_orchestration/operating-procedures/rocket.md` (your operating procedure — generation + engine canonical authority)
11. Existing simulation code paths: `reincarnated-engine/src/reincarnated/simulation/` for arena.py + balance_loop.py + sim fixtures + `build_reference_gauntlet()` consumer (per Gate-1 W2 amendment — cite specific line for `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` and specify implementation form: replace vs augment vs new per-tier profile)

## Math-before-code

Per Discipline #1 math-before-code, before implementing WU-R1 mob stat profile:
- [ ] Document the L45-50+ mob stat math against P_node anchor intent (per Block C scaffolding § 1.4): mob HP scaled to player endgame HP per defense_uptime ≥80% target; mob damage profile per KPM ~75+ target survivability; sustained vs burst damage distribution
- [ ] Document the per-cohort scaling formula (DPS-min-maxer 110-130% KPM / Balanced 100% / Defensive 70-85% KPM / Hybrid variable) — mob stats should produce in-band performance per cohort archetype per cohort_wr_modifier (Block C § 3.4)
- [ ] Document encounter difficulty multiplier formula (per Block C § 3.5 cell-difficulty-adjustment math hotspot; gamora seam consulted post-implementation per #18.2)

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required.** WU-R1 + WU-R2 produce new mob stat profile + 18 encounter definitions consumed by `build_reference_gauntlet()` (gauntlet sim seam owned by gamora). Round-trip smoke required:

- **Round-trip smoke: WU-R1 mob stat profile + WU-R2 first encounter definition** loaded via `build_reference_gauntlet()` producing a runnable sim fixture; verify field-presence + type-consistency at gamora-side consumer. Acceptance criterion: smoke test PASSes against 1 encounter (proof-of-integration); full 18-encounter integration verified in subsequent Wave 5 gauntlet sim test.

## Scope

### WU-R1 — L45-50+ endgame mob stat profile authoring (~3-4 hrs)

**Per Gate-1 W2 amendment:** cite specific code line for current `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` location + specify implementation form.

- [ ] Locate + cite current `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` definition (file + line per Discipline #1.2)
- [ ] Decide implementation form per Gate-1 W2:
  - **Option A:** Replace the 1.5 multiplier with L45-50+ calibrated value
  - **Option B:** Augment with new endgame-specific multiplier (preserving 1.5 for legacy)
  - **Option C:** Author new per-tier mob stat profile structure (cleanest separation; preferred per scaling-formula deferred-commitment per doc 41 § 4 #1)
- [ ] Document chosen option + rationale (math-before-code per § Math-before-code above)
- [ ] Implement per chosen option; integrate with `build_reference_gauntlet()` consumer signature
- [ ] Smoke test: load mob stat profile in isolation; verify field-presence + type-consistency

### WU-R2 — 18 endgame encounter definitions (~4-8 hrs)

**Per Gate-1 W1 amendment:** explicitly state encounter-definition-key choice — 25-row 5-tuple (full Sketch A enumeration) OR 18-cell non-deferred 4-tuple (proxy-collapsed). Verify the 25-row count includes proxy-density variants of base cells; if 18-cell is correct, document the proxy-collapse rationale.

- [ ] Lock encounter-definition-key choice per W1 amendment; document in this dispatch's completion record
- [ ] Author 18 endgame-reference encounter definitions per gamora audit memo § Recommendation:
  - 1 encounter per non-deferred cell per chosen key
  - Per encounter: target cell + intent + expected playability-criterion coverage (6 #26 sub-gates) + difficulty calibration intent (anchored to endgame per Block C § 1.4)
  - Per encounter: mob composition spec (count + types per WU-R1 mob stat profile) + arena interaction (use existing arena.py 6 scenarios as shells where applicable) + encounter sequence + termination conditions
- [ ] Round-trip smoke: load first encounter via `build_reference_gauntlet()`; verify successful loading + sim fixture instantiation
- [ ] Document each encounter against WU-R3 archetype coverage matrix

### WU-R3 — Archetype coverage verification (~1-2 hrs)

- [ ] For each of the 18 encounters, document which cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C § 2.2) can validly engage at WR ∈ [WR_lower, WR_upper] per W(cell, node, cohort) function (Block C § 3)
- [ ] Verify aggregate coverage: each cohort archetype has ≥N viable encounters (N = closeout-defined OR substrate-led; recommend ≥6 per cohort = 33% encounter coverage minimum)
- [ ] Flag any cohort-coverage gaps as INFO; WARN if a cohort has <6 viable encounters
- [ ] Output: archetype coverage matrix table in completion record

### WU-R4 — Cycle 14+ proxy-deferred 7-cell scope record (~30 min)

- [ ] Document the 7 proxy-deferred cells per gamora audit § Recommendation deferral list
- [ ] Update `canonical/02-roadmap.md` § 5 deferred-commitments with explicit Cycle 14+ work-unit entry: "Proxy-light / proxy-heavy 7-cell encounter content" with empirical-evidence trigger ("sim capability extension lands for proxy-density encounters")
- [ ] No implementation work for the 7 deferred cells in this dispatch

### Discipline compliance

- [ ] **#1.2 code-citation:** all references to existing code (arena.py, balance_loop.py, `build_reference_gauntlet()`) cite file + line per Gate-1 W2 amendment
- [ ] **#11 empirical inspection:** all numerical counts verified empirically; post-script empirical count assertions per WARN-pattern context (carried into Cycle 13)
- [ ] **#1 math-before-code:** mob stat math documented BEFORE WU-R1 implementation per § Math-before-code
- [ ] **#26 playability:** each of 18 encounters operationalized per 6 sub-gates
- [ ] **Round-trip per Principle 6:** WU-R1 + WU-R2 first encounter smoke test PASSes

## Acceptance criteria

- [ ] WU-R1 mob stat profile implemented per chosen option (A/B/C); code-cited; rationale documented
- [ ] WU-R2 18 endgame-reference encounters authored with per-encounter specifications complete
- [ ] WU-R3 archetype coverage matrix produced; flagged gaps if any
- [ ] WU-R4 Cycle 14+ proxy-deferred scope record updated in roadmap § 5
- [ ] Round-trip smoke: WU-R1 + first WU-R2 encounter loaded via `build_reference_gauntlet()` PASSes
- [ ] Discipline compliance per § Discipline compliance above
- [ ] Post-script empirical count assertions per WU dimension
- [ ] Tagged commit per rocket convention: `rocket: Cycle 13 SC-6 WU-R1+R2+R3+R4 — endgame reference encounter content (mob stat profile + 18 encounters + archetype coverage + Cycle 14+ scope record)`
- [ ] Round-trip smoke PASSes per Principle 6

## Out of scope (explicit non-goals)

- Pre-endgame encounter content (L1-15 / L15-30 / L30-45) — deferred per Cycle 13 v1 endgame-only scope (doc 41 § 4 #4)
- Full 22-encounter implementation (audit recommended 18 non-deferred + 3 optional; the 3 optional contested-cell + high-mobility swarm + spiky-add variants are deferred for separate dispatch IF substrate-vote-extends scope)
- 7 proxy-deferred cell content (WU-R4 records scope; no implementation in this dispatch)
- Wave 5 gauntlet sim execution against full 18-encounter set (separate Wave 5 dispatch)
- jack-ryan Gate-2 verification (separate dispatch post-rocket-implementation)
- Gamora SC-7 methodology consultation FULL execution (post-Wave-1 + post-baseline per #18.2)
- Modifying gandalf doc 42 partition intent (cross-seam; gandalf seam authority)
- Doc 40 / doc 41 / doc 42 modifications

## Open questions for the agent to resolve

- WU-R1 implementation form choice (A/B/C) — recommend Option C (cleanest separation) per scaling-formula deferred-commitment; your seam-owner call
- WU-R2 encounter-definition-key (25-row vs 18-cell) per Gate-1 W1 — verify against `v1-bc-target-intent-2026-05-24.md` content; pick the operationally correct key
- WU-R3 cohort coverage threshold — recommend ≥6 viable encounters per cohort (33% of 18-encounter total); adjust per substrate-led discipline if your seam analysis suggests different threshold

## References

- `agentic_orchestration/gamora/notes/2026-05-27-sc-6-reference-encounter-audit.md` (audit + recommendation specs)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-sc-6-gate-1-critique.md` (Gate-1 critique with W1+W2+W3 amendments)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` § 1.4 + § 2.2 + § 3 (Block C scaffolding)
- `canonical/41-progression-framework-2026-05-27.md` § 3 (endgame node identity)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (post-amendment foundation)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (BC-cell scope)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #26 + #30)

---

**Cycle:** 13
**Wave:** 0 / Sidecar SC-6 implementation
**Gates:** Wave 5 gauntlet sim execution preparation
**Priority:** P1 — Wave 5 prep critical-path; can fire in parallel with Wave 1 Gate-1 critique on doc 42
