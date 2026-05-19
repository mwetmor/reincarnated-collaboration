# Dispatch — 2026-05-19 — star-lord + gamora — VS2a L1 demo regen on single season (VS2a SHIP GATE)

**From:** knight-rider
**To:** star-lord (orchestration seam — regen pipeline OWNER) + gamora (sim seam — convergence validation OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when all upstream VS2a items land (F1, F4, S1, S2, S3, C1, C2, C3, F5; M1 not hard-gating per scope-of-work-vs2a § 2.10)
**Estimated effort:** ~1 week (regen orchestration + sim validation + visual smoke + ship-readiness review)
**Acceptance:** Single regenerated season demonstrates VS2a's full integrated stack WITHOUT override compensation. Tag fires: `vs2a/v1.0-vs2a-ship` (VS2a CLOSED).
**Hive context:** VS2a hive ACTIVE; L1 is the **VS2a SHIP GATE**. Everything that gates VS2a converges here.

---

## TL;DR

Regenerate one season demonstrating:
- Updated gauntlet (B6 kits + B10 V2 sequential rooms) ✓ via S1 + S2
- New geometry palette (B11 16→25 active types) ✓ shipped earlier
- 11 GREEN-list element VFX (Pimen integration) ✓ via C2 in-flight
- End-game-anchored movement-speed baseline ✓ via S3 + C1
- First Pimen integration ✓ via C2 + C4
- chierit character rendering ✓ via C3
- All WITHOUT override compensation

Plus post-pool-cull state: F5 Drift-14 pool × VFX-catalogue mapping closure landed; per-season vocabulary surface is canonical-bias clean.

---

## Context

Per `canonical/16-project-roadmap.md` § VS2a "Ship trigger":

> Single regenerated season demonstrates: updated gauntlet (B6 kits + B10 V2 sequential rooms) + new geometry palette (B11 + 11 GREEN-list element VFX) + end-game-anchored movement-speed baseline + first Pimen integration + chierit character rendering — all without override compensation.

Per scope-of-work-vs2a § 2.10:
- All of F1, F4, S1, S2, S3, C1, C2, C3, F5 must land
- Post-pool-cull state achieved (F5 Drift-14 closure)
- **Drift-15 Matt-selection step (M1) NOT a hard gate for L1** — L1 can ship with environment tileset deferred to follow-on (drax can ship season regen with current tilesets or geometric placeholders; Matt-selected pack lands as separate visual update post-wind-down via F6-D Track D)

This is the VS2a SHIP GATE. After L1 ships, VS2a CLOSES. VS2b begins per dispatch § 6.5 stage 2.

---

## Required reading

In order:
1. `canonical/16-project-roadmap.md` § VS2a "Ship trigger"
2. `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.10 (L1) + § 5 roadmap continuation
3. `canonical/story/movement-speed-baseline.md` § "Verdict Reversal" + Option-B values
4. All upstream VS2a dispatch completion records:
   - F1 (`geometry_type` schema)
   - F4 (B6 skill-tree UI) + drax F4 design dispatch
   - S1 (kit-redesign sprint per F2 branch)
   - S2 (B6 main work — tree structure)
   - S3 (Gate-3b sim MS extension)
   - C1 (movement-speed cascade)
   - C2 (B11 GREEN-list VFX)
   - C3 (chierit character rendering)
   - F5 (Drift-14 pool × VFX-catalogue audit + culled-pool summary)
5. R2 H1 re-validation result (R2-RT dispatch; either H1 PASS confirming spatial signal load-bearing OR gandalf re-disposition)
6. `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` (star-lord checkpoint)
7. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (gamora checkpoint)
8. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9 + § 6.5 stage 2 forward routing
9. `canonical/16-project-roadmap.md` § VS2b (forward routing target; VS2a close hands off)

---

## Scope

### Star-lord scope (regen orchestration)

- [ ] Pre-flight inventory verification: all upstream VS2a items landed; AGENT_STATE.md across all seams reflects readiness
- [ ] Select season for regen: typically the post-F2 reconverged canonical season OR a fresh season seeded freshly — L1 star-lord + gandalf consult if seed selection has cohesion implications
- [ ] Orchestrate full regen: catalogue (per S1 path) → tree-structured kits (per S2) → R1 sprint convergence (per S1 validation) → telemetry capture → manifest emission → export packet → loadout consumer
- [ ] All upstream features exercised: `geometry_type` per-skill (F1) populated; tree structure (S2) honored; engine-emitted MS JSON (S3) emitted + consumed; Drift-14 culled-pool (F5) selector behavior validated (no canonical-bias residue in selected season vocabulary)
- [ ] Cost telemetry: full season regen cost captured (LLM call count + $) per R8 disposition § 4 operating envelope
- [ ] Ship-readiness audit: no override compensation in fixture path (Discipline #13 drift watch; jack-ryan observes)
- [ ] AGENT_STATE.md updated

### Gamora scope (sim validation)

- [ ] R1 sprint executed on regenerated season (51-class × 5-tier × N-fight cardinality matching production sprint)
- [ ] Per-tier pass rate target: 70–85% per kit-redesign queue § 5.1 (or revised threshold per F2 disposition)
- [ ] Per-class geometry-type distribution + WR profile validated against F2 expectations
- [ ] R2 sub-gauntlet smoke pass (sanity check on 2D spatial substrate; expected GREEN per v0.13 + R2-RT)
- [ ] Sim + demo MS agreement validated (S3 gate; smoke fixture confirms)
- [ ] Telemetry full capture: `class_balance_results` + `class_fight_loadouts` + `spatial_fight_results` + `fight_log` per-fight
- [ ] AGENT_STATE.md updated

### Drax scope (visual ship readiness; consumer review)

- [ ] B6 skill-tree UI surface (F4 prototype) renders regenerated season's tree-structured catalogue
- [ ] chierit character rendering (C3) on player + opponents
- [ ] Pimen VFX integration (C2) per GREEN-list elements
- [ ] Movement-speed end-game-anchored (C1) operational
- [ ] Visual smoke captured (drax direct capture; galadriel sub-agent restriction in effect per protocol § 7)
- [ ] If F6-D Track D drax integration has landed (post-M1 wind-down), environment tiles render; if NOT (L1 ships before M1), geometric placeholders persist per scope-of-work § 2.10 NOT-hard-gating rationale

### Joint scope (ship-readiness review + tag fire)

- [ ] Ship-readiness review surface in hive log: gandalf judges cohesion (per R8 cohesion-judging protocol); jack-ryan observes Discipline #13 drift + Pattern P7 silent-default; knight-rider compiles state-of-hive L1 summary
- [ ] Gandalf cohesion sanity-check on the regenerated season: cohesion within 0.5 of baseline (per R8 disposition); player-facing vocabulary canonical-bias clean (per F5 closure)
- [ ] State-of-hive L1 ship doc authored at `agentic_orchestration/hive-mind/state-of-hive-<YYYY-MM-DD>-vs2a-l1-ship.md`
- [ ] Decisions-log entry authored by jack-ryan (or routed via jack-ryan) capturing VS2a arc + L1 ship + key outcomes (path through F2 / R1 sprint result / R2 H1 re-test result / cohesion sanity-check)
- [ ] Tag fire request: `vs2a/v1.0-vs2a-ship` (VS2a CLOSED)
- [ ] Hive log: STATE on regen start + STATE on R1 sprint re-run + STATE on ship-readiness review + COMPLETION on tag fire
- [ ] VS2a hive WIND-DOWN ACTIVATION: knight-rider authors VS2a closeout state-of-hive + CHANGELOG event entry + handoff to VS2b kickoff (per scope-of-work § 5.1)

---

## Cross-seam contract change? (Principle 6 gate)

**No new schema contracts in L1.** All upstream dispatches carried their own contract changes; L1 is the integrated end-to-end demonstration.

**Round-trip smoke REQUIRED at scale.** L1 IS the round-trip smoke for VS2a — every upstream contract is exercised end-to-end. Field-presence + integrity checks at every boundary (generator → schema validator → simulator → telemetry → export → loadout → demo render).

---

## Acceptance criteria

- [ ] All upstream VS2a items landed + verified (F1, F4, S1, S2, S3, C1, C2, C3, F5)
- [ ] Single season regenerated through full pipeline; no override compensation
- [ ] R1 sprint achieves 70–85% pass rate threshold
- [ ] B6 tree-structured catalogue rendered in demo skill-tree UI
- [ ] Sim + demo MS agreement validated
- [ ] Pimen VFX + chierit characters operational in demo
- [ ] Drift-14 culled-pool: no canonical-bias residue in season vocabulary
- [ ] Gandalf cohesion sanity-check passes (within 0.5 of baseline)
- [ ] Cost telemetry captured
- [ ] State-of-hive L1 ship doc authored
- [ ] Decisions-log entry authored
- [ ] Tag fired: `vs2a/v1.0-vs2a-ship`
- [ ] VS2a hive CLOSED + handoff to VS2b kickoff

---

## Out of scope

- VS2b roadmap items (Substrate Realignment + full catalogue; per `canonical/16-project-roadmap.md` § VS2b; separate hive after VS2a closes)
- Stage A2 closeout (B7 / B12 / B13 / B14 / B16; per scope-of-work § 5.2; post-VS2b territory)
- Playtest Cycle 1 (post-Stage-A2)
- Drift-15 Track D environment integration (F6-D; HELD post-M1; not gating L1 ship per scope-of-work § 2.10)
- M2 engine-rebuild playtest tag firings (separately held for wind-down)
- New catalogue features beyond VS2a scope

---

## Open questions for the agents

- **Season selection** — L1 star-lord + gandalf consult. Recommendation: pick the season that best demonstrates the integrated stack; if F2 path (b) regenerated specific seasons, select from that set
- **Override compensation watch** — L1 jack-ryan continuous observation; surface any hardcoded value or special-case that bypasses the integrated pipeline as Discipline #13 drift
- **Cohesion gate threshold** — L1 gandalf per R8 protocol; if cohesion regresses below baseline by > 0.5, surface for re-disposition (don't fire L1 tag)
- **R1 sprint threshold edge cases** — same as S1 (65–69% is PARTIAL; gandalf re-disposition)
- **Environment-tile placeholders for L1 ship** — L1 drax decision. If F6-D Track D has NOT landed (M1 still HELD), ship with geometric placeholders per F3 framework "What environmental theming is NOT". Surface in state-of-hive L1.
- **VS2b kickoff sequencing** — knight-rider authors scope-of-work-vs2b + coordination-matrix-vs2b at L1 completion checkpoint per scope-of-work-vs2a § 5.1. Pre-approval rationale: same Matt pre-approval pattern applies to VS2b batch authoring if Matt opts (this is a future decision)

---

## References

- `canonical/16-project-roadmap.md` § VS2a Ship trigger + § VS2b forward routing
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 2.10 (L1) + § 5 (continuation)
- All upstream VS2a dispatch docs (sibling files)
- `canonical/story/movement-speed-baseline.md` § "Verdict Reversal"
- `canonical/story/r8-disposition-2026-05-19.md` (cohesion-judging protocol reference)
- `reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` + `simulation/AGENT_STATE.md`
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9 + § 6.5 stage 2

---

## Autonomous-operation authority + activation gate

**Activation gate:** all upstream VS2a items landed (F1, F4, S1, S2, S3, C1, C2, C3, F5). M1 NOT hard-gating per scope-of-work § 2.10.

**Post-activation:** star-lord + gamora L1 orchestration; gandalf cohesion-gate at L2-equivalent; jack-ryan continuous observation. Knight-rider compiles state-of-hive L1 ship + VS2a closeout. No Matt-wait through ship; Matt re-enters at wind-down (M1 + M2 + retrospective).

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. L1 ships VS2a. Every upstream gate converges; the player gets a single season demonstrating end-game balance + tree-structured kits + integrated visual catalogue + canonical-bias-clean vocabulary. VS2a closes; VS2b begins.*
