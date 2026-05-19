# Dispatch — 2026-05-19 — gamora — VS2a R2 recalibration impl + R2-RT v3

**From:** knight-rider
**To:** gamora (sim seam — spatial calibration constants + R2-RT v3 OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires on gandalf R2 recalibration disposition lands (✓ `vs2a/v0.13-r2-spatial-calibration-disposed`)
**Estimated effort:** ~2–3 days (math note + impl + 5-class smoke + 51-class re-run)
**Acceptance:** Per § Acceptance. Tag fires: `vs2a/v0.2-r2-h1-revalidated` on R2-RT v3 H1 PASS.
**Hive context:** VS2a hive ACTIVE; R2-RT v1 (gamora 2026-05-19) returned H1 FAIL via calibration saturation. Gandalf disposition (HYBRID Option C; `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md`) prescribes 2-knob recalibration. R2-RT v3 fires on EXISTING 5-shipped-season catalogue BEFORE S1 ships (avoids conflating recalibration causes).

---

## Context

Gandalf's R2 recalibration disposition (HYBRID Option C):

| Constant | Old | New | File |
|---|---|---|---|
| `SPATIAL_DAMAGE_SCALE` | 8.0 | **4.0** | `simulation/spatial_gauntlet/spatial_engine.py` line 125 |
| `MOB_HP_DIFFICULTY_MULTIPLIER` (NEW; open_arena + chokepoint swarm only) | implicit 1.0 | **1.5** | `simulation/spatial_gauntlet/arena.py` (new constants block) |
| `PLAYER_ARMOR_FACTOR_VS_STANDARD` | 0.85 | **unchanged** | preserved survivability |
| Boss-with-adds calibration | — | **unchanged** | § 3.4 forward-flag preserved for VS2b |

Pattern: R1 Blocker 3 inverted (test-fixture calibration tuned against under-classified instrument; F1 corrected instrument; calibration over-rewarded catalogue).

R2-RT v1 result that motivated this dispatch:
- Re-run produced WR = 1.000 for all 51 classes in open_arena + chokepoint at current calibration
- H1 variance = 0.000 (saturation; no discriminating WR surface)
- True geometry partition correct: 41.2% circle / 3.9% line / 54.9% point

---

## Required reading

In order:
1. `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` (gandalf disposition; full)
2. `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.4 + § 4 (sub-claims + amendment paragraph)
3. `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/` (R2-RT v1 results; geometry_audit.md; summary.md)
4. `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` (encounter recalibration precedent + Discipline #1 math note pattern)
5. `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP-R2-A-1 partially-closed; WP-R2-A-2 + WP-R2-D-1 new)
6. `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (line 125 `SPATIAL_DAMAGE_SCALE`)
7. `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (new constants block target)
8. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (your checkpoint)

---

## Math-before-code (Discipline #1) — REQUIRED

**Path:** `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md`

Capture:

1. **Saturation math** — current calibration → WR=1.000 surface; show derivation
2. **Recalibration math** — `SPATIAL_DAMAGE_SCALE 8.0 → 4.0` halves DPS; `MOB_HP_DIFFICULTY_MULTIPLIER 1.5` × adds 50% mob HP (open_arena + chokepoint swarm only); combined: ~3× tougher than saturated state, ~0.5× tougher than original instrument-limited state
3. **Variance projection** — expected H1 variance under recalibration on TRUE 41.2/3.9/54.9 partition (point vs circle vs line)
4. **Discipline #12 citation** — telemetry capture conventions for v3 metrics
5. **5-class smoke selection** — pick 5 classes spanning geometry types (e.g., 1 line + 2 circle + 2 point) for smoke validation before full 51-class re-run

Jack-ryan reviews math before commit per continuous-observation rhythm.

---

## Scope

### Implementation

- [ ] Math note authored at `reincarnated-engine/design/working-agreement/R2-recalibration-math-2026-05-19.md`
- [ ] `SPATIAL_DAMAGE_SCALE` updated 8.0 → 4.0 in `simulation/spatial_gauntlet/spatial_engine.py`
- [ ] `MOB_HP_DIFFICULTY_MULTIPLIER` new constants block in `simulation/spatial_gauntlet/arena.py`; 1.5 multiplier on open_arena + chokepoint swarm only; boss_with_adds preserved unchanged
- [ ] `PLAYER_ARMOR_FACTOR_VS_STANDARD` preserved at 0.85
- [ ] Boss-with-adds calibration preserved (§ 3.4 forward-flag for VS2b)
- [ ] MIGRATION.md appended at `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`

### Validation

- [ ] **5-class smoke** (selected per math note; Discipline #17 semantic-shifting check)
- [ ] Smoke PASS → full 51-class R2-RT v3 run (51 × 3 × 30 fights; same seeds as R2-RT v1 for direct comparison)
- [ ] H1 metric: variance across geometry-type means
- [ ] H2 + H3 sanity-check
- [ ] Apply ORIGINAL H1 variance ≥ 0.10 threshold

### Outputs

- [ ] `reincarnated-engine/output/R2-h1-revalidation-v3-2026-05-19/`:
  - `R2-test1.md` — H1 re-test under recalibration
  - `R2-test2.md` — H2 sanity-check
  - `R2-test3.md` — H3 sanity-check
  - `summary.md` — comparison to R2-RT v1 + production sprint
  - `geometry_audit.md` — true partition confirmed unchanged

### Result routing

- [ ] **If H1 PASS:** STATE entry in hive log; tag-fire request `vs2a/v0.2-r2-h1-revalidated`; WP-R2-A-1 fully CLOSES
- [ ] **If H1 still FAIL:** STATE entry + REQUEST entry to gandalf for further disposition (deeper finding worth surfacing — calibration would still need iteration)
- [ ] **If H2/H3 regression:** surface as anomaly; do NOT roll back disposition tags

---

## Cross-seam contract change? (Principle 6 gate)

**Sim seam only; constants change.** MIGRATION.md at sim seam covers the contract.

**Round-trip: not applicable for this dispatch — calibration constants are sim-internal; F1 round-trip already validated; this dispatch consumes that.**

---

## Acceptance criteria

- [ ] Math note authored BEFORE production code change
- [ ] Constants updated per disposition table
- [ ] MIGRATION.md appended
- [ ] 5-class smoke PASSES before full re-run
- [ ] 51-class R2-RT v3 run executed; result docs filed
- [ ] H1/H2/H3 metrics recomputed; original thresholds applied
- [ ] If H1 PASS: WP-R2-A-1 CLOSES; tag-fire `vs2a/v0.2-r2-h1-revalidated`
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on math-before-code phase + STATE on impl phase + STATE on smoke phase + STATE on full re-run + REQUEST if FAIL

---

## Out of scope

- S1 first-batch regen (rocket; running in parallel; different catalogue + different files)
- Boss-with-adds recalibration (§ 3.4 forward-flag for VS2b)
- New R2 hypothesis tests beyond H1/H2/H3 (out)
- F1 schema/backfill (rocket; upstream)
- Per-class kit redesign (S1 territory)
- Substrate-identity revisions (already-stable per R8 disposition)

---

## Open questions for gamora

- **5-class smoke selection** — L1 gamora per math note (1 line + 2 circle + 2 point recommended for geometry-axis coverage)
- **Same-seeds vs new seeds for v3** — recommendation: same as R2-RT v1 + production sprint for direct variance comparison; L1 gamora
- **MOB_HP_DIFFICULTY_MULTIPLIER scope** — open_arena + chokepoint swarm only; boss_with_adds preserved unchanged. Document in math note.
- **What constitutes "PASS" vs "PARTIAL"** — strict threshold: H1 ≥ 0.10 PASS; 0.08-0.099 PARTIAL surface to gandalf; below 0.08 FAIL
- **R2-RT v3 substrate** — gandalf prescribed EXISTING 5-shipped-season catalogue (F1 partition correct at 41.2/3.9/54.9); fires BEFORE S1 ships to avoid conflating recalibration causes. L1 gamora confirms sequencing.

---

## References

- `canonical/story/r2-h1-recalibration-disposition-2026-05-19.md` (gandalf disposition; upstream)
- `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.4 + § 4
- R2-RT v1 result docs at `reincarnated-engine/output/R2-h1-revalidation-2026-05-19/`
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` (precedent pattern)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #12 telemetry; #17 semantic-shifting)
- `agentic_orchestration/hive-mind/watchpoints-engine-rebuild-2026-05-19.md` (WP-R2-A-1 + A-2 + D-1)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.1 re-test plan
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** gandalf R2 recalibration disposition landed (✓ `vs2a/v0.13-r2-spatial-calibration-disposed`).

**Post-activation:** gamora L1 within seam; jack-ryan reviews math; gandalf L2 if FAIL surfaces. No Matt-wait.

**Sequencing relative to S1:** PARALLEL — S1 first-batch regen (rocket) operates on a NEW season; R2-RT v3 (this dispatch) operates on EXISTING 5 shipped seasons. Different files + different catalogues. No conflict.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. The instrument was corrected; the calibration follows. Two knobs across two files; the spatial substrate becomes measurable under its original threshold.*

---

## Completion record

**Completed by:** gamora
**Date:** 2026-05-19
**Commit:** `24cdc7e` (reincarnated-engine main)
**Dispatch scope status:** PARTIAL — implementation complete; smoke FAIL (structural finding); full R2-RT v3 BLOCKED pending gandalf re-disposition.

### Phase 1: Math note + impl + 5-class smoke

**Math note:** `design/working-agreement/R2-recalibration-math-2026-05-19.md` — authored before implementation per Discipline #1. §§ 1-8 cover saturation derivation, recalibration math, variance projection, application boundary, Discipline #12 citation, 5-class smoke selection. § 9 added post-smoke with structural finding documentation.

**Implementation:**
- `SPATIAL_DAMAGE_SCALE` updated 8.0 → 4.0 (`spatial_engine.py`) ✓
- `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` (NEW) in `arena.py` constants block ✓
- `MOB_HP_DIFFICULTY_TIERS` + `MOB_HP_DIFFICULTY_SCENARIOS` added (application boundary) ✓
- `run_spatial_fight()` applies multiplier per scenario+tier ✓
- Pattern P7 ceiling-saturation WARNING at WR ≥ 0.95 ✓
- `MOB_DAMAGE_SCALE` 0.25 → 0.40 (L1 second-pass combination tightening, disposition § 2.4 option 3) ✓
- `PLAYER_ARMOR_FACTOR_VS_STANDARD = 0.85` PRESERVED ✓
- Boss-with-adds calibration UNCHANGED (§ 3.4 forward-flag) ✓
- MIGRATION.md v1.19 entry ✓
- Discipline #12 cited in commit message ✓
- WP-R2-D-1 CLOSED ✓

**5-class smoke: FAIL — structural finding**

Pass 1 (HYBRID Option C as disposed, MOB_DAMAGE_SCALE=0.25): all 5 classes WR=1.000. Root cause: mob DPS=45/s, player TTD=336s >> 120s fight cap. Timeout win condition universally met.

Pass 2 (+ MOB_DAMAGE_SCALE=0.40): partial signal. class_0035 (point, dm=0.64) WR=0.000. Signal direction correct. 4/5 floor-dm classes still WR=1.000.

**Structural finding (exceeds L1 calibration tightening scope):**
Mob `leash_distance_m = 18m` (monster JSON default) vs spawn-to-player distance 20-32m (SCENARIO_OPEN_ARENA, 50×50 arena). Mobs oscillate; empirically 11 mob hits total in 120s fight (expected ~686). Player HP 98.8% at fight end. This is a scenario spawn/leash geometry issue, not a calibration constant issue.

See:
- `output/R2-recalibration-smoke-2026-05-19/smoke_report.md` — full structural analysis
- `design/working-agreement/R2-recalibration-math-2026-05-19.md` § 9 — second-pass addendum

### Phase 2: Full R2-RT v3

**Status: BLOCKED** — smoke FAIL prevents execution per dispatch acceptance criteria.

### Routing

**Dispatch routing clause invoked:** "If H1 still FAIL: STATE entry + REQUEST entry to gandalf for further disposition."

STATE + REQUEST entries filed in `agentic_orchestration/hive-mind/engine-rebuild-log.md`.

REQUEST to gandalf: spawn/leash/timeout architecture re-disposition required. Options surfaced:
- A: Reduce player spawn y (40→25) in SCENARIO_OPEN_ARENA
- B: Override leash_distance_m per scenario (18→35m)
- C: Kills-only timeout for open_arena + chokepoint (semantic change)
- D: Combination A+C (recommended)

**Tag status:** `vs2a/v0.2-r2-h1-revalidated` HELD. `vs2a/v0.2-r2-h1-revalidated` will fire after re-disposition + smoke PASS + R2-RT v3 PASS.

**WP-R2-A-1:** ACTIVE-DEFERRED — H1 measurement still blocked; routing re-opened to gandalf.
**WP-R2-A-2:** ACTIVE-MONITORING — Pattern P7 WARNING operational.
**WP-R2-D-1:** CLOSED.
