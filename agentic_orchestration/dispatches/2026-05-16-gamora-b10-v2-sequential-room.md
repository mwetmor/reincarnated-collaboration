# Dispatch — 2026-05-16 — gamora — B10 V2: Sequential-room semantics with HP carryover

**From:** knight-rider
**To:** gamora
**Approved by:** Matt at 2026-05-16 Day 4 (per VS2a critical-path scope; B10 V2 promoted from deferred → in-scope per roadmap 2026-05-16)
**Status:** PENDING — ACTIVE
**Estimated effort:** 1-2 sessions (~7-12 hours engine work per roadmap §VS2a). Math-before-code per Discipline #1 — the convergence semantics change with sequential-room HP carryover, so the math note is load-bearing.
**Acceptance:** Sequential-room semantics implemented (Model A — class fights N mobs per room with HP carryover between encounters); convergence math re-derived for the new semantic; smoke season demonstrates the AOE differential the spec stated as the goal; intermediate tag `gamora/v1.3-b10-v2-sequential-room`; cross-seam impact documented in MIGRATION.md if telemetry consumers see new fields.

---

## Context — why now

**B10 V2 was promoted 2026-05-16 from deferred → in scope for VS2a** per `canonical/16-project-roadmap.md`:

> **B10 V2** Sequential-room semantics — **PROMOTED 2026-05-16 from deferred → IN SCOPE FOR DEMO VS2a.** Model A: class fights N mobs per room with HP carryover between encounters. Required for the spec's stated AOE differential goal ("balance loop sees AOE advantage"). V1 establishes the tier-diverse pool; V2 adds sequential-room mechanics + HP/resource carryover. ~3-4× regen cost increase vs V1. Cannot claim "full AOE differential achieved" until V2 ships. **Critical for VS2a — the "updated gauntlet" showcase undersells without sequential-room semantics.**

**You just closed two dispatches:**
- `2026-05-16-gamora-b10-4-option-2-implementation.md` — B10.4 Option 2 cut + pushed
- `2026-05-16-gamora-modifier-range-investigation.md` — calibration epoch declared (decisions-log entry committed `c000d7d`)

You're cleared to start B10 V2 immediately. This work is independent of rocket's B6 pre-work (which targets generation/, not simulation/). It also pairs cleanly with the calibration epoch — the new B10 V2 modifier output should be measured against the same `mean |mod-1.0|` metric.

## What B10 V2 changes — the semantic shift (Discipline #12)

**V1 (current):** Each (class × monster) encounter is independent. Class enters at full HP; fight ends at win/loss; next encounter starts at full HP.

**V2 (this dispatch):** Class fights N monsters in sequence per "room"; HP/energy/cooldowns/buffs carry over between encounters within the room. A new room resets to full state.

**Why this matters for AOE differential:**
- V1 cannot show the AOE advantage cleanly: an AOE class clearing 5 mobs in a single encounter looks similar in metrics to a single-target class clearing 5 mobs in 5 sequential 1v1s, because V1 collapses everything to per-fight outcomes.
- V2 surfaces the structural advantage: AOE class's HP/energy state after clearing 5 mobs in one encounter is far better than single-target's state after 5 fights (5× chip damage taken, 5× resource expenditure). The next encounter in the room is therefore much easier for AOE class. This is the genre-correct "AOE clears packs cheaply" advantage.

This is the spec's stated goal. V1 was the foundation; V2 makes the AOE advantage visible in metrics.

## Math-before-code requirements (Discipline #1)

**Math note required** at `src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` BEFORE any code changes. Cover:

### Section 1 — Model A specification

Define explicitly:
- What "room" means structurally: N consecutive encounters; class state persists; reset at room boundary.
- What state carries over: HP (yes), energy/mana/rage (yes), cooldowns (yes), buffs/debuffs (yes — but model decay if buff has duration), trial-room flags (no — those are per-fight).
- N value(s) — single fixed N, or distribution across rooms? Recommend with reasoning. Roadmap mentions "~3-4× regen cost increase vs V1" which suggests roughly N=3-4.
- Number of rooms per gauntlet — what does the gauntlet structure look like under V2? Is V2's "gauntlet" the same as V1's (one room per content-type slot, 7 slots = 7 rooms) or restructured?
- Monster sequencing within a room: same monster type N times? Different monster types from the same content-type pool? Recommend.

### Section 2 — Convergence math under V2

The convergence binary search currently operates on `convergence_winrate` (non-pack WR per B10.4 Option 2 lock). Under V2, "win rate per encounter" is no longer the right metric — a class winning encounter 1 then losing encounter 2 in the same room is qualitatively different from winning both. Derive:

- **What does "winning a room" mean under V2?** All N encounters cleared without death? Some lighter criterion (e.g., reached end of room with HP > 0%)?
- **What does the binary search converge on under V2?** Per-room win rate? Per-encounter win rate? Some weighted combination?
- **How does B10.4 Option 2's `convergence_winrate = non-pack WR` translate to V2?** Per-room non-pack room WR? Or does "non-pack" need redefinition (pack content fits more naturally inside a room; non-pack might span a separate room type)?
- **Cost-parity implications:** V1's experienced-cost-parity is "cost per encounter equal across classes." V2 adds room-internal cost: AOE class spends less per room because fewer total encounters needed to clear. This intersects with the engine-balance-stewardship entry's "experienced-cost-parity (deferred)" constraint — V2 makes the deferred metric observable.

### Section 3 — Calibration-epoch implications

Per the 2026-05-16 calibration-epoch decisions-log entry, the current operational baseline is **mean |mod-1.0| ≈ 0.82, range 0.09–0.52** under B10.4 Option 2 convergence semantics. Under V2:
- Expected direction of modifier range — does AOE differential surfacing push modifiers further apart (more compression on single-target) or compress them (room-internal balance is easier to hit)?
- Will the metric `mean |mod-1.0|` still be the right operational tracker, or does V2 demand a new metric?

If V2 demands a new metric, surface as a finding and let knight-rider author a follow-on decisions-log entry. **Do not unilaterally redefine the metric mid-dispatch.**

### Section 4 — Migration impact

- Does the `class_fight_loadouts` schema need new fields (room_id, encounter_index_within_room, hp_at_room_start, etc.)? If yes, MIGRATION.md entry required per ADR-004; star-lord cross-seam flag.
- Does the existing `validation_report.py` in-band check need to change? Probably yes — describe.
- Does B10.4 Option 2 binary search keep its semantic under V2, or does it need rework? Probably needs rework — describe.

### Section 5 — Test plan

How will you validate the implementation? Recommend:
- Unit tests on room state carryover (HP persistence, energy persistence, cooldown persistence).
- Math-driven smoke: hand-derive expected outcomes for 2-3 specific (class, room) combinations and verify the simulation matches.
- Smoke season for empirical comparison: same season seed pre/post V2 to see modifier range shift.

## Code change scope (after math note lands)

**Primary files (your seam):**
- `src/reincarnated/simulation/balance_loop.py` — binary search semantic update + room loop structure
- `src/reincarnated/simulation/fight_engine.py` — sequential-encounter execution within a room; state carryover
- `src/reincarnated/simulation/fight_result.py` — room-level result aggregation
- `src/reincarnated/simulation/damage_resolver.py` — likely unchanged but verify

**Cross-seam (star-lord territory — DO NOT MODIFY, file findings instead):**
- `src/reincarnated/telemetry/recorder.py` — if new fields needed for room context, file a finding; knight-rider authors star-lord follow-on
- `src/reincarnated/telemetry/migrations.py` — same; schema-level change requires MIGRATION.md per ADR-004
- `src/reincarnated/export/` — encounter_analytics.json schema; if room context is now part of the export, star-lord follow-on needed

**Read but don't modify:**
- `src/reincarnated/generation/*` — rocket's seam; generation produces classes that B10 V2 consumes
- `src/reincarnated/spirit_guide/*` — your seam but adjacent; check whether sequential-room semantics affect spirit_guide marginal-value calculations and surface as a flag if so

## Smoke discipline (Discipline #2)

**Two smokes required:**
1. **Unit smoke:** test_simulation suite passes; new unit tests for room state carryover pass.
2. **Season smoke:** generate a smoke season (not full regen) on a known seed (e.g., 001005); verify convergence works; capture modifier range; flag against calibration epoch.

**Star-lord regen interaction:** star-lord is running a fresh `season_001005` regen in the background as I write this. **Your B10 V2 code changes should NOT land on `main` until that regen completes** (race condition risk — fresh regen consumes current balance_loop semantics; B10 V2 changes those semantics). If the regen completes before you finish, no issue. If you finish first: hold your commit/push until the regen lands, then push. Knight-rider notifies when regen lands.

## Tag policy

- **Intermediate tag:** `gamora/v1.3-b10-v2-sequential-room` at the commit closing the implementation + smoke tests pass.
- **Milestone tag:** none from this dispatch. The milestone for B10 V2 (likely `v1.3-b10-v2-sequential-room` without prefix) cuts only after Matt approval AND a full regen confirms the AOE differential is observable in metrics. That's a separate confirmation step.
- Standard ADR-003 protocol: confirm with knight-rider before any milestone tag.

## Required reading

- `canonical/16-project-roadmap.md` §VS2a + §"Demo Vertical Slice 2" (the scope context)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 entries (engine-balance-stewardship + calibration-epoch) — the philosophical and metric anchors
- `agentic_orchestration/qa/findings/2026-05-16-gamora-modifier-range-rootcause.md` (your own findings — calibration epoch context)
- `reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md` (your own math note)
- `reincarnated-engine/src/reincarnated/simulation/math/b10-4-option-2-convergence.md` (your B10.4 math note — the convergence semantic you're now extending)
- `reincarnated-engine/design/b10-gauntlet-analysis.md` (full gauntlet analysis; §15 has B10.4 Option 2 full regen findings)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code), #2 (smoke-test), #11 (attribution), #12 (semantic-shifting — central to this dispatch)
- `agentic_orchestration/REVIEW_PROCESS.md` (seam discipline; MIGRATION.md per ADR-004)

## Acceptance criteria

- [ ] Math note `src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` filed with all 5 sections complete
- [ ] Convergence semantic under V2 explicitly defined (per-room WR vs per-encounter WR vs other)
- [ ] Schema impact analyzed; MIGRATION.md entry if new fields required (star-lord cross-seam flag if so)
- [ ] Code changes scoped to `simulation/` only; cross-seam findings filed instead of touching other seams
- [ ] Unit tests pass (existing + new room-state-carryover tests)
- [ ] Smoke season demonstrates B10 V2 convergence works
- [ ] Modifier range observed under V2; comparison against calibration epoch (mean |mod-1.0| ≈ 0.82) documented
- [ ] Intermediate tag `gamora/v1.3-b10-v2-sequential-room` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion with: tag hash, math note path, MIGRATION.md entry (if any), smoke results, cross-seam flags

## Out of scope (explicit)

- **B6 main (engine kit composition + balance re-tune)** — separate dispatch; waits on rocket's B6 pre-work landing first.
- **B14.5 V2 energy-type lever** — separate dispatch; closes calibration-epoch gap.
- **Stage A2 movement-speed-aware sim extension** — separate dispatch per engine-balance-stewardship Lock 3b.
- **Schema changes to telemetry or export seams** — file findings; star-lord follow-on if needed.
- **Generation-side changes** — rocket's seam; out of scope.
- **Demo/loadout viz changes** — drax follow-on once V2 is in main; out of scope here.

## Open questions for gamora to resolve in the math note

1. **N value per room:** fixed N (recommend value) or distribution (recommend distribution)?
2. **Room structure for the gauntlet:** 7 rooms (one per content-type slot) or restructured?
3. **Per-room win criterion:** all encounters cleared without death, or HP > 0% at room end?
4. **Binary search semantic under V2:** per-room WR, per-encounter WR weighted, or something else?
5. **"Non-pack" definition under V2:** does the boundary between pack-content (within-room) and non-pack-content (room-type) need rework, or does B10.4 Option 2's definition translate cleanly?

---

## Completion record

**Completed:** 2026-05-16
**Math note:** `src/reincarnated/simulation/math/b10-v2-sequential-room-convergence.md` — all 5 sections complete
**Intermediate tag:** `gamora/v1.3-b10-v2-sequential-room` at commit `9db2f5a` — pushed to origin
**Smoke status:** PASSED — 5/5 converged, 74.7s, mean |mod-1.0| = 0.3175 (vs V1 epoch 0.82; compresses toward 1.0 as predicted). 1320 tests pass.
**MIGRATION.md entry:** `src/reincarnated/simulation/MIGRATION.md` §v1.4 created — star-lord action required for telemetry schema changes
**Cross-seam flags:**
  1. Star-lord (HIGH): MIGRATION.md §v1.4 — new telemetry fields for room context (encounter_index_within_room, room_won, hp_fraction_at_encounter_start, use_room_evaluation, room_winrate, room_pack_winrate). Star-lord dispatch required.
  2. Star-lord (CARRIED): output/summary_formatter.py convergence_winrate display issue — still open from B10.4
  3. Spirit_guide (LOW, flagged): check whether spirit_guide marginal-value calculations use convergence_winrate or modifier values; V2 semantic shift may affect recommendations
**Notes for knight-rider:**
  - V2 modifier compression toward 1.0 confirmed empirically: V2 smoke mean |mod-1.0| = 0.3175 vs V1 epoch 0.82. This is the predicted consequence of the harder room-level convergence target (see math note §2.2 and §3).
  - V2 calibration epoch is not yet formally declared in decisions-log — that requires a full regen (seed 1005, 11 classes). Recommend a follow-on dispatch for milestone tag + decisions-log entry after full regen confirms the pattern.
  - Wall time smoke 74.7s is ~1.26× V1 (not 3×). This is because smoke uses 30 fights/matchup and binary search converges quickly; the 3× cost is at full regen scale (100 fights/matchup × N=3 encounters per slot).
  - V2 mode is opt-in (use_room_evaluation=False default). All V1 code paths unchanged; no risk to existing regen runs.
