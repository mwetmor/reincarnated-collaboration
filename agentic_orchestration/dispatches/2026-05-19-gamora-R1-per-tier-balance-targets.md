# Dispatch — 2026-05-19 — gamora — R1 per-tier balance targets

**From:** knight-rider
**To:** gamora (engine simulation + spirit guide seam)
**Approved by:** AUTONOMOUS — engine-rebuild hive activation under Matt directive 2026-05-19 (no per-dispatch Matt approval; per-tier targets pre-confirmed by gandalf per solutions doc § 10 Q1)
**Estimated effort:** 1–2 weeks for R1 itself + multi-week class-retuning sprint (in-scope; not separately tracked)
**Acceptance:** R1 Tests 1+2+3 pass per solutions doc § 2 (failure rate ≥ 60% on first run, post-retune pass-rate ≥ 70%, Matt-playtest boss-tier beatable for ≥ 2 of 3 selected classes)
**Hive context:** Engine-rebuild hive ACTIVE (second activation). This is the **first-fire, no-regret start** workstream. R1 is the cheapest gap and the one that explains Matt's empirical playtest finding directly.

---

## Context

The balance loop currently converges on the **mean win-rate across the 12-fight gauntlet** (`balance_loop.py:1907-1936`). No per-tier WR thresholds exist. **A class with boss WR 0.15, miniboss 0.30, elite 0.55, magic 0.65, swarm 0.80 passes convergence at mean 0.622** while being boss-unwinnable.

This is the **explanation for Matt's playtest report** ("highest WR ~45% miniboss, sub-20% boss, only beat miniboss with one class"). The metric was wrong; convergence pass rate hid the boss-tier failure for shipped classes.

R1 surfaces that failure mode and forces class-retuning. **Expect a balance-regression cascade** — most currently-shipped classes will fail the new criteria. That is **correct behavior** — the metric exists to do this.

## Required reading before starting

In order:

1. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` — operating protocol (§ 4.0 autonomous-operation amendment particularly load-bearing; § 4.5 jack-ryan continuous-observation; § 4.7 tagged-checkpoint principle; § 5.1 R1 activation requirements; § 9 engineering disciplines load-bearing for this rebuild)
2. `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` — mission canonical (§ 2 R1 in particular; § 10 gandalf's pre-confirmations)
3. `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — the diagnosis the rebuild closes (Axis 2 specifically — "convergence-target mismatch")
4. `agentic_orchestration/hive-mind/engine-rebuild-log.md` — hive log; acknowledge activation in your seam's first entry
5. `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md` § 1.1 — R1 deliverables summary
6. `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md` — seam mapping; concurrent-edit hot-spots (`balance_loop.py` is shared with future R3 consumer)
7. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #1 (math-before-code) is LOAD-BEARING for R1
8. `reincarnated-engine/src/reincarnated/simulation/balance_loop.py:1907-1936` — the convergence call site you're modifying
9. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — your last checkpoint

## Math-before-code (Discipline #1)

**Required:** author a per-tier math note BEFORE modifying `balance_loop.py`. Path suggestion: `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md`.

The math note must capture:

1. **Per-tier target table (pre-confirmed by gandalf per solutions doc § 10 Q1):**
   | Tier | Slots | Target | Floor | Ceiling |
   |---|---|---|---|---|
   | Swarm | 6 | 0.72 | 0.65 | 0.80 |
   | Magic | 2 | 0.62 | 0.55 | 0.70 |
   | Elite | 2 | 0.52 | 0.45 | 0.60 |
   | Mini-boss | 1 | 0.45 | 0.35 | 0.55 |
   | Boss | 1 | 0.38 | 0.30 | 0.45 |

2. **Per-tier tolerance bands** — the proposed targets above use ±span as the tolerance; document the exact band semantics (target ±tolerance vs floor/ceiling) and which is operative in the convergence loop. Cite Diablo II / PoE / Grim Dawn precedent for the boss-0.30 floor.

3. **Convergence pass criterion** — all 5 tiers must pass within tolerance, not just aggregate mean. Document the per-tier evaluation order + the early-exit semantics (fail on first tier-miss → reject and re-tune; aggregate-mean is no longer the gate).

4. **Per-tier weighting** — if any tier (e.g., boss with 1 slot) is statistically noisier than swarm (6 slots), document the proposed n-shot strategy or variance handling (e.g., 30 boss simulations vs 30 swarm-batch simulations). Don't silently average 1-slot-into-12-slot mean.

5. **Pattern P7 risk callout** — the current aggregate convergence does silent-default-pass on per-tier failure. R1 must explicitly fail-loud on per-tier miss. Document the telemetry surface that captures per-tier failure cause.

6. **Per-tier WR telemetry emission** — what fields are added to fight log / class_balance_results telemetry? Coordinate with star-lord if new telemetry schema fields are introduced (MIGRATION.md authoring becomes required).

Jack-ryan reviews the math note before you commit `balance_loop.py` modifications.

## Cross-seam contract change? (Principle 6 gate)

**Likely YES** for the per-tier WR telemetry emission. If you add a `per_tier_win_rate` column / field / dict-key to:
- `class_balance_results` (engine → telemetry)
- fight_log dict (gamora → star-lord boundary)
- season JSON `manifest.json` (engine → catalogue boundary)

…then MIGRATION.md is REQUIRED at the simulation seam, and star-lord must be coordinated with for the telemetry consumer side. Author MIGRATION.md concurrently per ADR-004.

**If NO** (e.g., the per-tier breakdown is computed locally in `balance_loop.py` without emitting a new field): state `Round-trip: not applicable — no cross-seam contract change` explicitly.

The Acceptance criteria below must include either:
- `Round-trip smoke: <fixture + boundary + check>` if any new telemetry/schema field is added
- `Round-trip: not applicable because <reason>` if no cross-seam impact

## Scope

- [ ] Per-tier math note authored at `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md` (Discipline #1)
- [ ] Baseline measurement: capture current per-tier WR distribution across 5 shipped seasons under aggregate-only convergence. Store at `reincarnated-engine/output/R1-baseline-measurement-2026-05-19/baseline-per-tier-distribution.json` (or similar discoverable path)
- [ ] Tag baseline measurement: `hive-rebuild/v0.1-r1-baseline-measurement-captured` (push under § 6.6 commit-push authority on milestone)
- [ ] `balance_loop.py:1907-1936` modified: convergence requires all 5 tiers to pass within tolerance, not just aggregate mean. Per-tier failure cause is logged.
- [ ] Per-tier WR telemetry emission (if introduced) — schema change coordinated with star-lord via MIGRATION.md
- [ ] Tag: `hive-rebuild/v0.2-r1-per-tier-convergence-operational`
- [ ] Test 1 execution: run R1 against 5 shipped seasons' classes under new criteria WITHOUT re-tune. Capture per-class pass/fail under per-tier criteria. **Success criterion: ≥ 60% failure rate** on shipped class set. Hypothesis-test result stored at `reincarnated-engine/output/R1-test1-failure-rate.md`.
- [ ] Class-retuning sprint (in-scope; iterate per failing class; gandalf consult on design intent for structurally-difficult classes per solutions doc § 2.3 scope-creep table — "DEPENDS" row)
- [ ] Test 2 execution: post-retune convergence pass-rate. **Success criterion: ≥ 70% pass-rate post-retune** with named structural failures documented. Result stored at `reincarnated-engine/output/R1-test2-post-retune-pass-rate.md`.
- [ ] Test 3 execution: package 3 classes that pass new criteria for Matt + son playtest. **Success criterion: Matt beats boss with ≥ 2 of 3 selected classes within 5 attempts each.** Document playtest packet at `reincarnated-engine/output/R1-test3-playtest-packet.md` (Matt executes the playtest when he reads state-of-hive; result captured later).
- [ ] Smoke-test passes (standard engine smoke per Discipline #2)
- [ ] MIGRATION.md if cross-seam impact (telemetry schema field addition triggers this)
- [ ] Round-trip smoke (or not-applicable justification) per Principle 6
- [ ] AGENT_STATE.md updated at session end per existing convention
- [ ] Tag on hypothesis-test passage: `hive-rebuild/v0.3-r1-hypothesis-test-passed`

## Acceptance criteria

- [ ] Per-tier math note committed before `balance_loop.py` modification
- [ ] Baseline per-tier WR distribution captured + tagged
- [ ] `balance_loop.py` per-tier convergence operational
- [ ] R1 Test 1 (failure rate ≥ 60%) executed + result documented
- [ ] Class-retuning sprint converges most failing classes back to per-tier criteria
- [ ] R1 Test 2 (post-retune pass-rate ≥ 70%) executed + result documented
- [ ] R1 Test 3 playtest packet prepared for Matt
- [ ] Smoke-test GREEN throughout (per Discipline #2; protocol § 4.5 inheritance)
- [ ] Round-trip smoke: if per-tier WR telemetry field added → fixture exercising `class_balance_results` insert + telemetry read; field-presence check. OR `Round-trip: not applicable because <reason>`.
- [ ] Hive log updated continuously per protocol § 4.2 (STATE entries on milestone; HANDOFF on test result; OBSERVATION on structurally-difficult classes for jack-ryan + gandalf surface)
- [ ] AGENT_STATE.md updated
- [ ] All three hypothesis-test results captured in hive log → knight-rider tags `hive-rebuild/v0.3-r1-hypothesis-test-passed` and commits/pushes per § 6.6

## Out of scope (explicit non-goals)

- 2D spatial sub-gauntlet build (R2 — separate workstream; depends on R3)
- Per-skill range additions to balance loop (R3 — separate workstream; rocket leads schema)
- Demo runtime AI parity (R5 — separate workstream; drax)
- Substrate identity declaration revisions (Phase-1 P1 commitment; out-of-scope unless gandalf-surfaced)
- New tier additions (per-tier table is fixed at 5 tiers: swarm/magic/elite/mini-boss/boss)
- Boss-tier composition changes (boss-with-adds is R2 sub-gauntlet scope, not R1)
- Pattern-B-conditional work (R6 host-calibration; parked)

## Open questions for the agent to resolve (in-seam L1 authority)

- **Per-tier statistical strategy** — single-slot tiers (mini-boss, boss) are noisier than multi-slot tiers; how do you handle n-shot variance? L1 gamora decision; document in math note. If proposed approach materially changes solutions-doc § 2 design intent (e.g., proposing different per-tier table than gandalf-confirmed), surface to gandalf via hive log QUESTION.
- **Convergence early-exit semantics** — fail on first tier-miss vs evaluate all tiers and report all failures? L1 decision; document in math note.
- **Class-retuning loop architecture** — per-class iterate vs batch-retune-and-validate? L1 decision; documented in implementation notes.
- **Class structural-fail surface** — when a class is structurally unable to pass per-tier under retune (rare per solutions doc § 2.3 "DEPENDS" row), surface to gandalf via hive log REQUEST entry; gandalf decides whether to redesign class concept vs flag as known-limitation.

## References

- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2 (R1 specification)
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 10 Q1 (per-tier targets pre-confirmed)
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (Axis 2 diagnosis)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 5.1 (R1 activation requirements)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py:1907-1936` (current aggregate convergence call site)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #1 math-before-code; Discipline #2 smoke-test)
- Prior B14.5 work patterns (per `project_b14_5_sidecar_analyses.md` for convergence iteration distributions; B14.5 V1 primary loop architecture is the canonical balance-loop pattern to extend)
- Hive log: `agentic_orchestration/hive-mind/engine-rebuild-log.md` — acknowledge activation in your seam's first entry

---

## Autonomous-operation authority (no Matt-wait)

Per launch dispatch § 3 + protocol § 4.0:

- **In-seam implementation decisions** — gamora L1 authority; no escalation
- **Cross-seam impact (telemetry schema)** — coordinate with star-lord via MIGRATION.md; knight-rider monitors
- **Design-direction question on per-tier targets** — surface to gandalf via hive log; gandalf decides + responds in-session
- **Structural-fail class disposition** — surface to gandalf via hive log REQUEST; gandalf decides

**No Matt-wait at any point during R1.** Matt re-enters only at wind-down per protocol § 4.9.

---

*Authored 2026-05-19 by knight-rider under autonomous-operation authority. R1 fires first. The metric is wrong; the per-tier truth surfaces; the boss-tier becomes a real gate. The gauntlet teaches us what the playtest already showed.*
