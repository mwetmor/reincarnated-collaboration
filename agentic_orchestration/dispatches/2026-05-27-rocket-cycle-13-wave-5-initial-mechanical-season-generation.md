# Dispatch — 2026-05-27 — rocket — Cycle 13 Wave 5 Initial Mechanical Season Generation (Cycle 13 Close Milestone)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 + Cycle 13 framing brief § 3 Wave 5 + Q8 close criterion + Q10 amendment + jack-ryan Wave 4 BUNDLED Gate-2 PASS verdict (commit `888ffca`) — Wave 4 CLOSED + WARN-pattern MAINTAINED + Wave 5 dispatch authoring UNBLOCKED
**Estimated effort:** ~4-12 hrs season generation pipeline + result authoring (consumes Wave 4 architecture; integrates with gamora Wave 5 gauntlet sim outputs)
**Acceptance:** initial mechanical season generation produces all WR-bracket-validated characters per framing brief Q10 amendment; season content authored at `reincarnated-engine/output/cycle-13-mechanical-season-001/` (or equivalent path); kit count + per-cohort distribution + WR-bracket pass rate per quality report; Wave 5 close artifact ready for gandalf validation + jack-ryan Cycle 13 close Gate-2

## Context

Cycle 13 Wave 5 = gauntlet battle sim + initial mechanical season generation per framing brief § 3 Wave 5 + Q8 close criterion:

> **Cycle 13 close = gauntlet sim PASS + initial mechanical season generation + jack-ryan Gate-2 PASS. Output mechanically-validated content; hand off to Cycle 14 (Phase 5 cohesion) per Pattern A.**

This dispatch is **Wave 5 Track B — rocket initial mechanical season generation**. Gamora Wave 5 gauntlet sim execution fires in parallel (separate dispatch). Both tracks coordinate to produce the season's WR-bracket-validated content.

**Per framing brief Q10 amendment** (LOCKED): "all characters which are produced within WR bracket. No pre-imposed N; substrate-led — the engine generates against the spec; whatever passes WR-bracket validation IS the season's content. 'Let's see what comes out.'"

**Cycle 13 v1 scope:** endgame node only per Block C § 1.5 + doc 41 § 4 #4.

**Wave 4 architecture now consumable** (per Wave 4 Gate-2 PASS):
- Wave 1 partition schema (rocket consumes for gear gen rolling)
- Wave 2+3 T4 algorithm (rocket integrates 3-category + scope-dimension into season kit gen)
- Wave 4 Track A spec-driven gear gen (rocket extends for season-scale generation)
- Wave 4 Track B gamora sim cycling (rocket coordinates with gamora gauntlet for WR-bracket validation)
- Wave 4 Track C star-lord export schema (rocket exports season content via established schema)

## Required reading before starting

1. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-2-track-a-rocket.md` (Wave 4 Track A Gate-2 PASS; WARN-pattern MAINTAINED status)
2. `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-13-wave-4-track-a-spec-driven-gear-gen-implementation.md` (Wave 4 Track A implementation + your `gear_instance_generator.py` location)
3. `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 3 Wave 5 + Q8 close criterion + Q10 amendment
4. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` (substantive design locks)
5. `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` amended (your Wave 4 Track A intent)
6. `canonical/44+43+42+41+40+39+38` (full Cycle 13 canonical architecture)
7. `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (P_node + C_archetype for cohort × scope kit generation)
8. `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9 (SC-7 FULL — gauntlet sim integration spec)
9. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #26 + #27 + #29 + #30 + #31 + #32 + Principle 6)
10. `agentic_orchestration/operating-procedures/rocket.md`
11. Wave 4 implementation files (engine commits):
    - `reincarnated-engine/src/reincarnated/generation/gear_instance_generator.py` (Wave 4 Track A primary)
    - `reincarnated-engine/src/reincarnated/generation/partition_schema.py` (Wave 1+4)
    - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` + `t4_scope_selector.py` (Wave 2+3)
    - `reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` (Wave 4 Track B; gamora; rocket coordinates)

## Math-before-code (#1 — REQUIRED)

Per Discipline #1 math-before-code, before Wave 5 season generation:

- [ ] Document the season generation pipeline math: kit candidate enumeration per BC-target subspace + cohort archetype mapping per Block C; integration with Wave 4 Track A gear instance generation
- [ ] Document the WR-bracket validation integration math (Q10): season-content emission = kits PASSing gamora gauntlet sim WR-bracket gate per SC-7 W function
- [ ] Document the season-content output format: per-character (kit + gear instances + T4 selections + scope-dimension + chain composition + cohort assignment); season metadata (kit count; cohort distribution; WR-bracket pass rate; quality report cross-reference)
- [ ] Document the compute budget per #1.1: kit generation count; per-cohort sweep; integration with gamora gauntlet sim; M2 8GB threshold preserved
- [ ] Document the Cycle 13 v1 scope: endgame node only; multi-node deferred per doc 41 § 4 #2

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required.** Wave 5 season generation produces NEW season content artifact consumed by gandalf validation + jack-ryan Cycle 13 close Gate-2 + future Cycle 14+ Phase 5 cohesion coalescence + drax loadout app (Wave 4+ planning).

**Round-trip smoke:** sample season-content output → load via star-lord export schema → verify field-presence + type-consistency.

**MIGRATION.md** if cross-seam contract change beyond Wave 4 Track A.

## Scope

### W5R.0 — Season generation setup + math-note

- [ ] Math-note per Discipline #1 BEFORE execution
- [ ] Verify Wave 4 architecture composability (gear instance generation + T4 algorithm + scope-dimension end-to-end)
- [ ] Initialize season generation configuration: BC-target subspace coverage; cohort archetypes (4 per Block C); endgame node v1 scope

### W5R.1 — Kit candidate generation

- [ ] Generate kit candidates spanning BC-target subspace per Wave 1+2+3 architecture
- [ ] Per-kit gear instance set across rarity tiers per Wave 4 Track A
- [ ] Per-kit T4 selections + scope-dimension per Wave 2+3
- [ ] Per-kit cohort archetype mapping per Block C

### W5R.2 — Gauntlet sim integration (coordinates with gamora Wave 5 Track A)

- [ ] Submit kit candidates to gamora gauntlet sim
- [ ] Receive WR-bracket validation results per SC-7 W function
- [ ] Filter season content per Q10 amendment: ALL kits PASSing WR-bracket = season's content
- [ ] Substrate-led emission: no pre-imposed N

### W5R.3 — Season content authoring

- [ ] Author season content output at `reincarnated-engine/output/cycle-13-mechanical-season-001/` (or equivalent per rocket seam canonical structure)
- [ ] Per-character output (kit + gear + T4 + scope + chain + cohort)
- [ ] Season metadata: kit count; cohort distribution; WR-bracket pass rate; quality report cross-reference (gamora SC-7)
- [ ] Round-trip smoke per Principle 6: sample season-content → star-lord export → re-load
- [ ] MIGRATION.md if cross-seam contract change

### Discipline compose-check

- [ ] #1 math-before-code: math-note per § Math-before-code
- [ ] #1.2 code-citation: existing-code references (Wave 4 Track A integration cites `gear_instance_generator.py`; gamora gauntlet integration cites `t4_sim_cycling.py`)
- [ ] **#11 empirical inspection** — POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE (MAINTAIN WARN-pattern MAINTAINED status per Wave 4 Gate-2 milestone — Wave 2 REMEDIATED → Wave 3 PRESERVED → Wave 4 MAINTAINED → Wave 5 must MAINTAIN)
- [ ] #18 + #18.2 consumed from Wave 4 architecture
- [ ] #26 playability: WR-bracket validation operationalizes per SC-7 § 9 + Block C
- [ ] #27 + #31 + #32: T4 architecture preserved per Wave 2+3
- [ ] #29 commitment-to-consequence: season content lands with consequence (substrate-led emission)
- [ ] #30 sim methodology naming: gamora SC-7 pattern applied
- [ ] Principle 6 round-trip: W5R.3 smoke PASSes

## Acceptance criteria

- [ ] Season content generation pipeline executes against Wave 4 architecture
- [ ] Gauntlet sim integration (gamora coordination) produces WR-bracket-validated kits
- [ ] Season content authored per § W5R.3
- [ ] Per Q10 amendment: substrate-led emission ("all characters within WR bracket")
- [ ] Quality report cross-reference (gamora SC-7)
- [ ] Round-trip smoke per Principle 6 PASSes
- [ ] MIGRATION.md if cross-seam contract change
- [ ] **POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE** (WARN-pattern MAINTAINED status PRESERVED)
- [ ] Tagged commit per rocket convention: `rocket: Cycle 13 Wave 5 initial mechanical season generation — Cycle 13 close milestone (consumes Wave 4 architecture; integrates gamora gauntlet sim)`

## Out of scope (explicit non-goals)

- Gamora Wave 5 gauntlet sim execution (separate dispatch in parallel; rocket integrates via existing Wave 4 t4_sim_cycling.py interfaces)
- Gandalf Cycle 13 validation against doc 40 commitments (post-implementation; separate)
- Jack-ryan Cycle 13 close Gate-2 (post-validation; separate)
- KR Cycle 13 wind-down summary (post-Gate-2; separate)
- Cycle 14+ Phase 5 cohesion coalescence (post-Cycle-13)
- Multi-node season generation (Cycle 13 v1 endgame-only; deferred per doc 41 § 4 #2)
- Phase 5 LLM naming + cohesion (Cycle 14 scope; structure-only season output per Wave 2+3 I3 carryover)
- Modifying canonical docs
- Production telemetry DB migration

## Open questions for the agent to resolve

- Kit candidate count: substrate-led per BC-target subspace × cohort sweep; emission post-WR-bracket filter; no pre-imposed N per Q10
- Per-character output format: extend Wave 4 Track A `PartitionGearInstance` + Wave 2+3 `T4CandidateV2` schemas OR new season-content composite; recommend composite for season-level metadata
- MIGRATION.md scope: incremental per ADR-004; document new season-content path + metadata structure

## References

- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-2-track-a-rocket.md`
- `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-13-wave-4-track-a-spec-driven-gear-gen-implementation.md`
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` § 3 Wave 5 + Q8 + Q10
- `canonical/45+44+43+42+41+40+39+38` (full Cycle 13 architecture)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md`
- `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9
- Wave 4 implementation files (engine commits)
- `agentic_orchestration/operating-procedures/rocket.md`

---

**Cycle:** 13
**Wave:** 5 Track B (rocket initial mechanical season generation; Cycle 13 close milestone)
**Gates:** gandalf validation + jack-ryan Cycle 13 close Gate-2 → CYCLE 13 CLOSE
**Priority:** P1 — CRITICAL-PATH FINAL CYCLE 13 WAVE
