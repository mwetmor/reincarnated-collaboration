# Engine-Rebuild Scope of Work — Hive Mode (Second Activation)

**Authored:** 2026-05-19 by knight-rider at engine-rebuild hive activation.
**Authority:** Matt directive 2026-05-19 (autonomous-operation); launch dispatch `agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md`; operating under `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`.
**Status:** **Live executable plan.** Updated by knight-rider as workstreams advance. All seams consult this doc; specialists execute against the per-workstream dispatch + this doc.
**Estimated duration:** ~8 weeks parallel for the seven workstreams + class-retuning sprint following R1.
**Companion artifacts:** `coordination-matrix-engine-rebuild.md` (per-workstream seam mapping); `engine-rebuild-log.md` (append-only hive log); `state-of-hive-YYYY-MM-DD-engine-rebuild.md` (daily digests).
**Mission canonical:** `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`.

---

## § 0 — TL;DR

The hive closes the six gauntlet-simulator gaps diagnosed 2026-05-18 + runs the season-as-emergent-output A/B test gandalf + Matt co-surfaced. **Seven workstreams** (R1, R2, R3, R4, R5, R7, R8) across the engine simulation seam + generation seam + telemetry/export seam + demo seam. R6 (Host-Calibration) is parked behind Pattern-B and explicitly out-of-scope.

**First-fire batch (parallel):** R1 + R3 + R7 + R8. **Queued behind R3:** R5 + R2 + R4.

**Ship gate per workstream:** hypothesis test passes per criteria in solutions doc §§ 2–8. **Batch ship gate:** all seven workstreams' hypothesis tests pass → tag `hive-rebuild/v1.0-engine-rebuild-complete` → continue forward to VS2a per Matt roadmap-continuation directive (no wind-down).

**Wind-down trigger:** Matt's explicit declaration only. Engine-rebuild completion is a milestone, not an endpoint.

---

## § 1 — The seven workstreams

### § 1.1 — R1 — Per-tier balance targets ⭐ *fire first*

- **Owner:** gamora (engine-sim seam)
- **Inputs:** solutions doc § 2; current `balance_loop.py:1907-1936` (aggregate-only convergence)
- **Deliverables:**
  - Per-tier WR target table operationalized (swarm 0.72 / magic 0.62 / elite 0.52 / mini-boss 0.45 / boss 0.38; floors 0.65 / 0.55 / 0.45 / 0.35 / 0.30; ceilings 0.80 / 0.70 / 0.60 / 0.55 / 0.45)
  - `balance_loop.py` modified: convergence requires all 5 tiers to pass within tolerance; not just aggregate mean
  - Telemetry: per-tier WR distribution emitted per fight + per convergence iteration
  - Baseline measurement: 5 shipped seasons' classes under aggregate-only convergence (captured before R1 ships)
- **Math-before-code (Discipline #1):** per-tier math doc authored before convergence loop modification; jack-ryan reviews
- **Hypothesis tests:**
  - Test 1 — Initial failure rate ≥ 60% on shipped class set under new criteria (without re-tune)
  - Test 2 — Post-retune pass-rate ≥ 70% with named structural failures documented
  - Test 3 — Playtest validation: Matt + son beat boss with ≥ 2 of 3 selected classes within 5 attempts each
- **Effort:** 1–2 weeks for R1 itself + multi-week class-retuning sprint (in-scope; not separately tracked)
- **Pattern P7 risk:** convergence-loop early-exit on aggregate mean must explicitly fail-loud on per-tier miss — no silent-pass

### § 1.2 — R3 — Per-skill range + AI behavior schema migration (foundation)

- **Owner:** rocket (schema + catalogue) + star-lord (export + telemetry) + elrond (backfill tooling)
- **Inputs:** solutions doc § 4; current `fight_engine.py:155, 161` (1D scalar distance + binary `at_melee_range` gate)
- **Deliverables:**
  - Per-skill range field: `range_m` (or `range_band: short/medium/long/extreme`) added to skill schema in catalogue
  - Per-mob AI behavior fields: `preferred_behavior` (melee_aggressive / ranged_kite / cast_at_range / charge_then_melee / etc.), `telegraph_window_seconds`, `aggro_radius_m`, `leash_distance_m`, `skill_rotation_priority`, `range_profile_redistribution`
  - Backfill across 5 shipped seasons: re-derive per-skill range from geometry-type defaults; populate AI fields from archetype priority
  - Disengage as valid balance-loop action: player-sim AI and monster-sim AI can choose "retreat to leash" / "kite to optimal range" — not just fight-to-death
- **Cross-seam contract:** MIGRATION.md REQUIRED (concurrently authored by rocket) — affects R2, R4, R5, R7 consumers
- **Hypothesis tests:**
  - Test 1 — Out-ranging viability: long-range class WR ≥ 20pp higher than melee class on same monster
  - Test 2 — Disengage viability: controller class WR on hard-counter boss improves from 0% to ≥ 20% via disengage-and-reset
  - Test 3 — Range-profile redistribution: post-R3 distribution ≈ 30% long / 40% medium / 30% close (within 5pp)
- **Effort:** 2–4 weeks together
- **Discipline #13 watchpoint:** schema field naming + semantic shape must match across rocket emitter + star-lord telemetry + elrond migration + downstream consumers (R2/R4/R5/R7)

### § 1.3 — R7 — AI catalogue source of truth (parallel with R3)

- **Owner:** rocket (schema + sim consumption) + star-lord (catalogue + parity-test infrastructure)
- **Inputs:** solutions doc § 7; 3 decoupled AI implementations diagnosis (engine-sim AI Python; demo runtime AI TS; balance-loop implicit AI assumption)
- **Deliverables:**
  - Catalogue (monster JSON) is single source of truth for AI behavior fields
  - Engine-sim AI reads monster JSON at convergence
  - Demo runtime AI reads monster JSON at spawn (consumed by R5 + R4)
  - Balance loop reads monster JSON when computing expected behavior
  - **Parity-test infrastructure:** automated test that asserts engine-sim AI and demo runtime AI for same monster produce equivalent behavior within tolerance
- **Hypothesis tests:**
  - Test 1 — Parity test passes: change `aggro_radius` in monster JSON from 8m to 12m → both engine sim AND demo reflect new behavior identically within ±10%
  - Test 2 — Parity test fails loudly on intentional break: hardcoded TS constant override in demo reported with file:line
  - Test 3 — Cross-surface consistency: 3 monsters with distinct `preferred_behavior` produce matching observed behavior on both surfaces (100% match)
- **Effort:** 2–3 weeks; parallel with R3 (shares schema)
- **Pattern P7 watchpoint:** consumers MUST iterate registry / read from JSON; no silent fallback to TS constants or Python defaults

### § 1.4 — R8 — Season-as-emergent-output A/B (parallel; independent surface)

- **Owner:** rocket (generation pipeline + CLI flags) + star-lord (LLM call orchestration + cost telemetry) + gandalf (theme-coalescence prompt + cohesion judging)
- **Inputs:** solutions doc § 8; current generation pipeline (~317 LLM calls/season; theme-as-input gates all downstream content)
- **Deliverables:**
  - Generation pipeline modified: default mode is mechanical convergence with no theme-as-input
  - One LLM call after convergence coalesces theme + anchor + cosmological vocabulary + naming
  - CLI surface extended: `--theme-input PATH | --theme-name SLUG` (opt-in, invokes legacy input-driven mode); `--no-coalesce` (opt-out, raw mechanics output)
  - Post-convergence theme-coalescence prompt drafted by gandalf
  - Cohesion judging protocol drafted by gandalf (human + LLM judge, 1–5 scale)
  - A/B run: 3 inverted + 3 baseline seasons at seed parity
- **Hypothesis tests:**
  - Test 1 (must-pass) — Cohesion: inverted within 0.5 of baseline on cohesion score
  - Test 2 (interesting) — Mechanical variety: inverted ≥ baseline on skill-diversity entropy / role-distribution variance / gear-set coherence
  - Test 3 (operational) — LLM cost: ≥ 75% reduction in calls AND ≥ 75% reduction in $
  - Test 4 (discovery) — Substrate-identity invariance: examine theme-coalescence output for whether substrate identity is preserved or whether emergent groupings replace it
  - Test 5 (stability) — Multi-shot: 3 runs of theme-coalescence on same converged content converge on same anchor + dominant element within ≥ 70% Jaccard overlap
- **Effort:** 1–2 weeks for prototype + A/B run + measurement
- **Disposition routing:** gandalf authors final disposition decision (commit-to-emergent-default OR revert-to-input-driven OR partial) — no Matt-wait

### § 1.5 — R5 — Demo AI parity audit (queued behind R3)

- **Owner:** drax (player-presentation seam)
- **Inputs:** solutions doc § 6; current `world/movement.ts:74-81` (hardcoded `PREFERRED_RANGE`, `KITE_TRIGGER`)
- **Deliverables:**
  - Audit current TS constants vs monster archetype range_profile fractions
  - Read range_profile from monster JSON at demo spawn (replaces TS constants)
  - Redistribute range_profile across approach / engage / kite (per R3's monster JSON spec)
- **Hypothesis tests:**
  - Test 1 — Distribution post-audit: range_profile assignments visible in `world/aggro.ts` match R3 JSON spec
  - Test 2 — Kite-default frames drop by ≥ 70% across same-class playtest comparison
- **Effort:** 1 week; best AFTER R3 (so JSON has fields) but before R4 (so R4 builds on corrected baseline); could overlap with end of R3
- **Activation gate:** R3 shipping the AI behavior fields (at minimum)

### § 1.6 — R2 — 2D spatial sub-gauntlet (queued behind R3)

- **Owner:** gamora (combat model) + star-lord (telemetry emission for spatial events)
- **Inputs:** solutions doc § 3; current 1D scalar distance + 3-band state machine
- **Deliverables:**
  - 2D spatial sub-gauntlet alongside 1D gauntlet
  - 3–5 spatial scenarios per class: open arena (50m × 50m), choke-point corridor (10m × 50m with bottleneck), boss-with-adds composition (one boss + 2–4 adds at varying spawn positions)
  - Soft entity collision (push-apart force at small radius)
  - Hard collision body for boss-tier
  - Real per-skill range checks (R3 dependency)
  - Real AOE coverage queries against mob positions
  - 1D gauntlet retained for damage-number ballparking
- **Math-before-code (Discipline #1):** spatial combat math doc authored before sub-gauntlet build; jack-ryan reviews
- **Hypothesis tests:**
  - Test 1 — Geometry-type WR variance within role increases from ~0.05 to ≥ 0.10
  - Test 2 — Boss-with-adds detection: ≥ 30% of shipped classes show ≥ 10pp WR delta between 1D boss fight and spatial boss-with-adds
  - Test 3 — Chokepoint testability: chokepoint-vs-arena WR delta correlates with class's spatial-aware skill set
- **Effort:** 3–5 weeks
- **Activation gate:** R3 shipped (per-skill range available)
- **Sim cost increase:** ~3–4× (acceptable)

### § 1.7 — R4 — Demo collision + leash + range (queued behind R3)

- **Owner:** drax (player-presentation seam)
- **Inputs:** solutions doc § 5; current `world/movement.ts:197-199` (entity collision deferred)
- **Deliverables:**
  - Soft separation via push-apart force at `r < 0.8 × entity_radius`
  - Aggro + leash per monster (read from R3 JSON)
  - Per-skill range as real check (out-of-range skills don't fire or visibly miss)
  - Range_profile distribution rebalance (R3 dependency)
  - AI behavior FSM: `idle → approach → attack → reposition`
- **Hypothesis tests:**
  - Test 1 — Pack-spread visible: galadriel-capture pipeline screenshot at swarm-engagement shows no entity-overlap at center-pixel
  - Test 2 — Leash + reset: monster HP returns to 100% within 5 seconds of leash break
  - Test 3 — Skill out-of-range visibly fails: visible feedback + no damage + skill on cooldown
  - Test 4 — Constant-flee artifact fixed: < 2 of 10 playtest fights show "monster flees indefinitely"
- **Effort:** 2–3 weeks
- **Activation gate:** R3 shipped (per-skill range + aggro/leash fields available)

---

## § 2 — Sequencing summary

```
Week 0 (now, 2026-05-19):
  Engine-rebuild hive activated by knight-rider per Matt directive

Week 1-2 (parallel):
  R1 — per-tier balance targets (gamora) — triggers class-retuning sprint
  R8 — season-as-emergent-output A/B (rocket + star-lord + gandalf) — 6-season A/B + measurement; disposition at end

Week 1-4 (parallel with R1 + R8):
  R3 — schema migration (rocket + star-lord + elrond)
  R7 — AI catalogue source of truth (rocket + star-lord, partial-parallel with R3)

Week 3-5 (after R3 partial):
  R5 — demo AI parity audit (drax) — fast cleanup once R3 schema lands

Week 5-8 (after R3 ships):
  R2 — 2D spatial sub-gauntlet (gamora + star-lord) — primary fight-integrity payoff
  R4 — demo collision + leash + range (drax) — player-surface payoff

Week 8+ — hypothesis-test validation gates:
  R1 test, R2 test, R3 test, R4 test, R5 test, R7 test, R8 test
  → if all pass: tag hive-rebuild/v1.0-engine-rebuild-complete
  → continue forward to VS2a per Matt roadmap-continuation directive
  → no wind-down (Matt declares wind-down explicitly when ready)
```

---

## § 3 — Roadmap continuation (post-engine-rebuild)

Per Matt directive 2026-05-19 (launch dispatch § 6.5) and protocol § 10:

### § 3.1 — Stage 1: VS2a project list

- Source: `canonical/16-project-roadmap.md` § "VS2a — Gauntlet + Geometry + First Catalogue Integration" (gandalf-stewarded)
- Knight-rider authors VS2a `scope-of-work-vs2a.md` + `coordination-matrix-vs2a.md` at engine-rebuild completion checkpoint
- Specialists execute under SME authority per same operating mode
- Tag milestones per VS2a roadmap-named gates
- Move to Stage 2 only after every VS2a item shipped + tagged + state-of-hive captures completion

### § 3.2 — Stage 2: VS2b project list

- Source: `canonical/16-project-roadmap.md` § "VS2b — Substrate Realignment + Full Catalogue" (gandalf-stewarded)
- Begin only after VS2a closed out
- Same operating pattern
- Move to Stage 3 only after VS2b closed out

### § 3.3 — Stage 3: Stage A2 phases

- Source: `canonical/16-project-roadmap.md` Stage A2 references + `canonical/28-engine-arpg-rebalance-design.md` queue
- Begin only after VS2a AND VS2b both closed out
- Items in flight or queued per current roadmap state: B6, B7, B12, B13, B14, B16 (subject to roadmap refresh)
- Same operating pattern
- After Stage A2 closes, surface to gandalf for next-priority direction

---

## § 4 — Mission discipline

**Scope is FIXED at seven workstreams.** Scope-creep protocol per protocol § 2.3 (engine-rebuild protocol):

| Pressure | Default |
|---|---|
| Add new substrate during rebuild | REJECT (Phase-1 P1 substrate set is fixed) |
| R1 surfaces structurally-unfixable class | If rare, surface to gandalf; if tuning gap, retune in sprint |
| R8 emergent theme is unexpectedly compelling | If hypothesis criteria met, gandalf authors design-doc amendment; no Matt-wait |
| R3 schema migration touches substrate identity declarations | ESCALATE to gandalf for design judgment; gandalf decides |
| Galadriel finishes Track-C and wants follow-up captures during R4 | ACCEPT if scoped; galadriel observes, does NOT spawn sub-agents per § 7 |
| Pattern-B research arrives | FILE in PARKED thread; do NOT pull focus |

**Canonical-doc revisions** (substrate identity declarations, engine-rebuild solutions doc, etc.) → gandalf authors mid-flight amendment per protocol § 4 routing; knight-rider broadcasts.

---

## § 5 — Cross-references

- Engine-rebuild protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`
- Engine-rebuild mission canonical: `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`
- Diagnosis canonical: `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`
- Mechanics inheritance: `canonical/story/archived/hive-mind-protocol-2026-05-17.md`
- Pattern-B parked: `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`
- Launch dispatch: `agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md`
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Decisions log: `reincarnated-engine/design/decisions/decisions-log.md`
- Roadmap: `canonical/16-project-roadmap.md`
