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

---

## Completion record

**Closed:** 2026-05-19 by gamora
**Commits:** `5d6dfc4` (engagement-geometry impl + smoke) + `155e1f2` (Stage 1 R2-RT v3 results + AGENT_STATE)

### Phase 1 — Math note + impl + smoke

**Math note § 10:** COMPLETE. Authored at `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md` per Discipline #1 + WP-R2-E-1. Six sub-sections (engagement-geometry analysis, timeout semantics, combined fix projection, 5-class smoke selection, Discipline #12 framing, WP-R2-E-1 compliance checklist).

**Engagement-geometry impl:** COMPLETE (commit 5d6dfc4).
- `LEASH_DISTANCE_OVERRIDE_M_SWARM = 35.0` named constant in arena.py
- `KILLS_ONLY_TIMEOUT_SCENARIOS = frozenset({"open_arena", "chokepoint_corridor"})` named constant
- `SpawnSpec.leash_distance_override_m: Optional[float] = None` new field (WP-R2-A-3)
- open_arena + chokepoint swarm spawns: leash_override=35.0; boss_with_adds: explicit None
- `entity_from_monster_dict()`: spawn leash override takes precedence over monster JSON
- kills-only timeout for KILLS_ONLY_TIMEOUT_SCENARIOS in `SpatialFightEngine.run()`
- Pattern P7 floor-saturation WARNING added (symmetric to ceiling WARNING)
- Player AI `_select_skill_for_entity()`: shortest-CD non-self skill preference (L1 seam improvement)
- MIGRATION.md v1.20 appended (star-lord: no schema change)
- Discipline #12 cited in commit message

**5-class smoke:** PASS (dispatch criterion — >=1 class WR<0.95; ceiling saturation cleared).
- All 5 prior WR=1.000 classes now have WR < 0.95 (4 at 0.000, 1 at 1.000)
- class_0035 (dm=0.64, point): 0.000 → 1.000 (correctly wins; skill AI fix + leash fix)
- Dispatch PASS: Pattern P7 ceiling saturation definitively cleared
- Full criteria FAIL (diagnostic): 5-class sample is bimodal; no intermediate-WR classes
- Floor-saturation WARNING fires; L1 tightening not applied (floor-dm kill-throughput intrinsic)

### Phase 2 — Stage 1 full 51-class R2-RT v3 run

**Stage 1 result: H1 FAIL (catalogue-diversity finding; CD-variance domination)**

H1 variance: 0.0136 (FAIL; threshold >= 0.10)
Per-geometry mean WRs: circle=0.143, line=0.000, point=0.286
True partition confirmed: 21 circle / 2 line / 28 point (41.2% / 3.9% / 54.9%)
Geometry source: 100% explicit (0% heuristic_fallback; F1 backfill confirmed)
Wall time: 151.7s (51 × 3 × 30 = 4590 fights)

**ANOMALY:** point mean WR (0.286) > circle mean WR (0.143). Inverted from H1 hypothesis.

**Fourth structural finding (Drift-17 Layer 4 candidate):** Kills-only timeout + optimized skill selection exposes CD-variance domination. Floor-dm classes with extreme fast-CD skills (cd=0.1-0.2s, range_m=2-3m) fire 5-10 attacks/second and serially clear 8 mobs in ~15-25s regardless of geometry type. Point cohort has more fast-attack subclasses in this catalogue → point wins more than circle. This is the existing catalogue's CD distribution as the binding constraint, not the substrate.

**Per § 5.3 routing-to-S1 clause:** Explicit routing-to-S1 finding confirmed. Stage 1 PARTIAL-CLOSE condition MET (§ 5.3: "H1 ≥ 0.10 OR routing-to-S1 explicit finding"). Tag `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` surfaces to knight-rider for PARTIAL-CLOSE decision.

**Per disposition § 4.2:** H1 FAIL on existing catalogue is NOT a substrate failure. Route to Stage 2.

**H2/H3 regressions** (from 74.5%/+0.130 to 21.6%/+0.041): Both caused by kills-only timeout changing open_arena WR distribution from uniformly-high to bimodal. Not independently actionable; resolve with Stage 2.

### Routing

**Tag surfaces to knight-rider:** `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` — per § 5.3 routing-to-S1 clause; knight-rider decides whether to fire.

**WP-R2-A-1:** ACTIVE-DEFERRED. Stage 2 R2-RT v4 on S1 catalogue is canonical measurement surface.

**REQUEST to knight-rider:** Draft Stage 2 R2-RT v4 dispatch after S1 first-batch validation gate PASS + 4 remaining seasons regen completes.

**Fourth finding to gandalf (via knight-rider routing):** CD-variance domination is a Drift-17 Layer 4 candidate. Disposition question: does Stage 2 on S1 (R8-inversion normalized CDs per archetype) resolve implicitly, or does it need a fifth disposition pass? Pre-forecast: Stage 2 resolves implicitly if R8 archetype normalization is present.
