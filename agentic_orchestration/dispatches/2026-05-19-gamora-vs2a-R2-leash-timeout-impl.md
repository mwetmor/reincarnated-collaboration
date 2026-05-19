# Dispatch — 2026-05-19 — gamora — VS2a R2 leash/timeout impl + Stage 1 R2-RT v3

**From:** knight-rider
**To:** gamora (sim seam — engagement-geometry impl + Stage 1 R2-RT v3 OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires on gandalf 3rd disposition lands (✓ `vs2a/v0.14-r2-leash-timeout-disposed`)
**Estimated effort:** ~2–3 days (math note extension + impl + 5-class smoke + Stage 1 51-class re-run)
**Acceptance:** Per § Acceptance. Tag fires: `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` on Stage 1 H1 PASS.
**Hive context:** VS2a hive ACTIVE; this is the THIRD R2 impl pass following gandalf's Path γ disposition. Two-stage validation gate: Stage 1 (this dispatch; existing catalogue) + Stage 2 (post-S1 regen; future dispatch).

---

## Context

Gandalf's R2 leash/timeout disposition (`canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md`) — Path γ Hybrid B+C:

**Engagement-geometry fix (B + C):**

| Change | Old | New | File |
|---|---|---|---|
| `leash_distance_m` per-scenario override (swarm, open_arena + chokepoint) | 18m (monster JSON default) | **35m** | `simulation/spatial_gauntlet/arena.py` |
| Timeout semantics (open_arena + chokepoint) | HP>50% timeout-survival win | **kills-only timeout** | `simulation/spatial_gauntlet/spatial_engine.py` |
| Boss-with-adds | unchanged | unchanged | § 3.4 forward-flag preserved |

**Two-stage validation gate:**
- **Stage 1 (this dispatch):** R2-RT v3 on EXISTING 5-shipped-season catalogue (diagnostic confirmation). Tag: `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue`.
- **Stage 2 (future dispatch post-S1):** R2-RT v4 on S1 regenerated catalogue (gold-standard threshold validation). Tag: `vs2a/v0.4-r2-h1-validated-on-S1-catalogue`.

Original `vs2a/v0.2-r2-h1-revalidated` REPLACED by two-tag schema. Original H1 ≥ 0.10 threshold preserved end-to-end.

R2-RT v3 smoke (your prior session) demonstrated:
- Recalibration constants (SPATIAL_DAMAGE_SCALE=4.0 + MOB_HP × 1.5 + MOB_DAMAGE_SCALE=0.40) implemented
- Leash mechanic blocks engagement at current scenario geometry
- 4/5 smoke classes still WR=1.000 due to leash + HP>50% timeout-survival win

This dispatch closes the engagement-geometry surface gandalf has now formally dispositioned.

---

## Required reading

In order:
1. `canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md` (gandalf disposition; FULL; § 2.1 impl + § 4 two-stage validation gate)
2. `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` (prior disposition; constants implemented)
3. `canonical/story/drift-audit.md` § Drift-16 + § Drift-17 (newly named patterns)
4. `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP-R2-A-1/A-2/A-3 + E-1/E-2 + D-1 CLOSED)
5. Your prior R2-RT smoke report: `reincarnated-engine/output/R2-recalibration-smoke-2026-05-19/smoke_report.md`
6. Your prior math note: `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` — § 10 EXTENSION (this dispatch authors § 10)
7. `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (leash override target)
8. `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (timeout semantics target)

---

## Math-before-code (Discipline #1) — § 10 extension

**Extend existing math note** at `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` with § 10:

1. **Engagement-geometry analysis** — leash 18m → 35m enables mob approach within open_arena 50×50 and chokepoint 10×50 spatial dynamics; D2 Bloody Foothills / PoE Twilight Strand semantic preserved
2. **Timeout semantics correction** — kills-only timeout for open_arena + chokepoint (boss_with_adds retains HP-based timeout); rationale: HP>50% timeout-survival was development-phase scaffolding, not what H1 measures (geometry-type kill efficiency discrimination)
3. **Combined fix projection** — engagement-geometry + recalibration constants → expected discriminating WR surface on true 41.2/3.9/54.9 partition
4. **5-class smoke selection** — same 5 classes as R2-RT v3 smoke (class_0016, class_0020, class_0006, class_0019, class_0035) for direct A/B comparison; Discipline #17 semantic-shifting check
5. **WP-E-1 compliance** — math note + MIGRATION.md concurrent commit pattern

Jack-ryan reviews § 10 before commit per continuous-observation rhythm + WP-R2-E-1 obligation.

---

## Scope

### Implementation

- [ ] Math note § 10 authored (extends `R2-recalibration-math-2026-05-19.md`)
- [ ] Per-scenario `leash_distance_m` override field in `simulation/spatial_gauntlet/arena.py` (swarm spawns; open_arena + chokepoint → 35m; boss_with_adds preserved at monster JSON default)
- [ ] Kills-only timeout for open_arena + chokepoint in `simulation/spatial_gauntlet/spatial_engine.py` (boss_with_adds retains HP>50% timeout)
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (engagement-geometry impl entry)
- [ ] Per WP-R2-E-1: math note + MIGRATION.md concurrent with impl

### Validation

- [ ] **5-class smoke** (same 5 classes as recalibration smoke for direct A/B comparison)
- [ ] Smoke PASS criterion: at least 1 class WR < 0.95 in eligible scenarios (Pattern P7 ceiling-saturation cleared); discriminating surface visible
- [ ] Smoke PASS → full 51-class Stage 1 R2-RT v3 (51 × 3 × 30 fights; same seeds as R2-RT v1 + v3 smoke for direct comparison)
- [ ] H1 metric: variance across geometry-type means (open_arena + chokepoint)
- [ ] H2 + H3 sanity-check
- [ ] Apply ORIGINAL H1 variance ≥ 0.10 threshold (preserved through three findings)

### Outputs

- [ ] `reincarnated-engine/output/R2-leash-timeout-smoke-2026-05-19/smoke_report.md`
- [ ] If smoke PASS: `reincarnated-engine/output/R2-h1-revalidation-stage1-2026-05-19/`:
  - `R2-test1.md` — Stage 1 H1 re-test under Path γ
  - `R2-test2.md` — H2 sanity-check
  - `R2-test3.md` — H3 sanity-check
  - `summary.md` — comparison to R2-RT v1 (heuristic) + v3 (saturation) + v3-smoke (leash); three-layer findings arc
  - `geometry_audit.md` — true partition confirmed 41.2/3.9/54.9

### Result routing (Stage 1)

- [ ] **If H1 PASS Stage 1:** STATE entry; tag-fire `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue`; WP-R2-A-1 PARTIAL-CLOSE; Stage 2 R2-RT v4 dispatch authored post-S1 regen
- [ ] **If H1 FAIL Stage 1:** STATE entry + REQUEST entry to gandalf for fourth disposition pass (would need consideration of substrate-architectural surgery; Stage 2 may pre-empt as the cleaner test bed)
- [ ] **If H2/H3 regression:** surface anomaly; do NOT roll back v0.13 or v0.14 disposition tags

---

## Cross-seam contract change? (Principle 6 gate)

**Sim seam only; engagement-geometry + timeout semantics change.** MIGRATION.md at sim seam covers the contract.

**Round-trip: not applicable for this dispatch — engagement-geometry is sim-internal; F1 round-trip already validated; this dispatch consumes that.**

---

## Acceptance criteria

- [ ] Math note § 10 authored BEFORE production code change
- [ ] Engagement-geometry impl per disposition § 2.1
- [ ] MIGRATION.md appended (WP-R2-E-1)
- [ ] 5-class smoke PASSES (discriminating WR surface visible)
- [ ] 51-class Stage 1 R2-RT v3 executed; result docs filed
- [ ] H1/H2/H3 metrics recomputed; original threshold applied
- [ ] If H1 PASS: WP-R2-A-1 PARTIAL-CLOSE; tag-fire `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue`; Stage 2 R2-RT v4 dispatch surface readiness signal
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on math-before-code phase + STATE on impl phase + STATE on smoke + STATE on full re-run + REQUEST if FAIL

---

## Out of scope

- S1 first-batch regen (rocket; in parallel; different catalogue + different files)
- Stage 2 R2-RT v4 (post-S1 regen; separate future dispatch)
- Boss-with-adds recalibration (§ 3.4 forward-flag preserved for VS2b)
- Per-class kit redesign (S1 territory)
- Substrate identity revisions (already-stable per R8 disposition)
- Fourth R2 disposition pass (only if Stage 1 H1 FAIL)

---

## Open questions for gamora

- **5-class smoke selection** — same as v3 smoke for direct comparison (class_0016/0020/0006/0019/0035); document choice
- **Same-seeds vs new seeds for Stage 1** — same as R2-RT v1 + v3 smoke for direct three-finding-arc variance comparison
- **Per-scenario leash override mechanism** — L1 gamora; recommendation: scenario-aware monster spawn pipeline reads override map; document choice in math note § 10
- **Kills-only timeout semantics for chokepoint** — chokepoint geometry may have different kill expectations than open_arena; document if differentiation needed in math note
- **PASS / PARTIAL / FAIL thresholds** — strict: H1 ≥ 0.10 PASS; 0.08-0.099 PARTIAL → gandalf re-disposition; below 0.08 FAIL
- **Stage 2 R2-RT v4 timing signal** — post-S1 first-batch PASS + 4 more season regen + Stage 1 PASS together; surface readiness in completion record

---

## References

- `canonical/story/r2-h1-leash-timeout-disposition-2026-05-19.md` (gandalf Path γ; upstream)
- `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` (prior disposition)
- `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.4 (original spatial-recalibration forward-flag)
- `canonical/story/drift-audit.md` § Drift-16 + § Drift-17 (meta-patterns named)
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP suite refined)
- `reincarnated-engine/output/R2-recalibration-smoke-2026-05-19/smoke_report.md` (your prior smoke FAIL)
- `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` § 1-9 (existing math; § 10 to be appended)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1, #12, #17)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** gandalf 3rd R2 disposition landed (✓ `vs2a/v0.14-r2-leash-timeout-disposed`).

**Post-activation:** gamora L1 within seam; jack-ryan reviews math § 10; gandalf L2 if Stage 1 FAIL. No Matt-wait.

**Sequencing relative to S1:** PARALLEL — S1 first-batch regen operates on a NEW season; Stage 1 R2-RT v3 operates on EXISTING 5 shipped seasons. Different catalogues + different files. No conflict.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. The leash and timeout finalize the spatial substrate's instrumentation. Stage 1 confirms diagnostically; Stage 2 validates on the cleaner regen test bed. The three findings become a coherent arc.*
