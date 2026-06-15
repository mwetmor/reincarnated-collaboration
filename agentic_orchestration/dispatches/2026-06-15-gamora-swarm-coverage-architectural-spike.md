# Dispatch — 2026-06-15 — gamora — swarm-coverage architectural spike (single-global-modifier hypothesis test)

**Status:** PENDING — Matt authorized 2026-06-15 ("Architectural hypothesis re-opens; swarm-coverage spike next"). Pre-fire gate: jack-ryan Gate-1 (DESIGN-MODE) on this dispatch + on the spike's mechanic+criterion math-note BEFORE the build fires.
**From:** knight-rider
**To:** gamora
**Estimated effort:** multi-day (Pattern B) — but it is a SPIKE, not a production feature build. Time-box to the smallest mechanic that answers the question.
**Acceptance:** a clean PASS or HONEST_FAIL on the question "does a swarm-side coverage/spatial-pressure mechanic bring the rogue cell's swarm tier **into the `[TIER_FLOORS["swarm"]=0.65, TIER_CEILINGS["swarm"]=0.80]` band** (NOT merely off the 1.0 ceiling) AND let a global modifier converged off its search floor clear the upper tiers?"

> **Gate-1 amendments folded (jack-ryan finding `f96fad4`, 2026-06-15):** A1 — PASS prong (b) pinned to real `balance_loop.py` constants (`MODIFIER_FLOOR_NEAR` does not exist). A2 — anti-AoE-proxy guard made concrete against the existing spatial arena + a stated falsification test. A3 — swarm prong is the full `[0.65, 0.80]` band, both bounds (a crater-everything outcome is an HONEST_FAIL). A4 — Principle-6 not-applicable qualified with the `NullSpatialTelemetryWriter` reason + a MIGRATION.md HALT trigger.

## Context

The weapon-as-envelope rogue-degeneracy chain just closed with a load-bearing result. rocket's coordinate-derived role-floor (`rocket/v2.2-envelope-role-floor`, commit `52703c9`; Gate-1 + Gate-2 passed) FIRED correctly in your G7 re-fire (`gamora/v1.x-...-rogue-refire`, `d003f8f`) — the composed kit carried `{defensive:1, mobility:2, area:4, burst:1}` — yet the envelope rogue arm **still craters upper tiers**. The mechanism you surfaced: **swarm stays pinned at 1.0**, so the single global modifier floors to **0.0719** to suppress it, and at that modifier the reserved burst does nothing. The fix is **necessary-but-insufficient on rogue.**

gandalf's disposition (`agentic_orchestration/gandalf/notes/2026-06-15-rogue-refire-necessary-but-insufficient-disposition.md`, § 6-octies): his diagnosis is **half-confirmed** (the composer gap was real, now closed) and **half-falsified** (his "the entire delta is the role floor" canary claim is wrong). A floor-intact kit cratering boss under a hot swarm is the **branch-2 architectural shape** — the single-global-modifier hypothesis now re-opens **on positive evidence**, not on silence. gandalf located the real lever as **swarm-side encounter design** (a spatial/coverage pressure mechanic) — NOT the composer, and NOT per-tier modifiers (which he flags as the band-aid that passes the sim while leaving the player experience — a single-target striker trivializing swarm — exactly as broken: the D3-pre-RoS symptom-patch anti-pattern).

**This spike answers the architectural question on evidence.** The hypothesis under test: *raw single-target throughput over-clears swarm because the sim models no spatial/coverage cost for a pure-ST kit facing many low-HP mobs. If swarm encounters apply a coverage pressure that a pure-ST kit cannot fully mitigate (you can't be everywhere; uncovered mobs cost you HP/time), the rogue swarm WR drops off the 1.0 ceiling, the global modifier comes off the floor, and the reserved burst can then carry the upper tiers.* This is a SPIKE — prove or disprove the lever; do not ship a production feature.

## Required reading before starting

- Your own refire result + math-note §8: `reincarnated-engine/output/g7-hold-sim-b6-prereq-B-rogue-refire-20260615.json` + `reincarnated-engine/src/reincarnated/simulation/math/b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md`.
- gandalf disposition: `agentic_orchestration/gandalf/notes/2026-06-15-rogue-refire-necessary-but-insufficient-disposition.md` (§3 the real lever; the per-tier-modifier anti-pattern).
- gandalf original diagnosis §1 (the swarm-over-clear mechanism): `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` — *"a fast single-target striker deletes low-HP swarm mobs one-by-one faster than they mob you — raw ST throughput over-clears swarm without any AoE."*
- `balance_loop.py` — the single-global-modifier search: `MODIFIER_SEARCH_FLOOR=0.01` (`:318`, the literal search floor), `MODIFIER_LOW_THRESHOLD=0.30` (`:92`, the "too-DPS-heavy" diagnostic); the observed floored modifier was `0.0719` (BETWEEN them — so "off the floor" must be pinned to a real cited constant, NOT the nonexistent `MODIFIER_FLOOR_NEAR`). Also `TIER_FLOORS`/`TIER_CEILINGS` (`:532-545`; `swarm` band `[0.65, 0.80]`).
- **THE SPATIAL ARENA — where the mechanic lives (A2).** The swarm tier ALREADY runs through a multi-mob spatial arena: `SCENARIO_OPEN_ARENA` (8-mob spatial engagement), `_run_spatial_slot` (`balance_loop.py:2742`) / `run_spatial_fight`, with entity positions, aggro/leash radii, and an explicit **"coverage gap" concept already in `spatial_gauntlet/spatial_engine.py:81-82`** (+ `SPATIAL_DAMAGE_SCALE`). You do NOT invent a coverage mechanic from scratch — you derive pressure from the EXISTING spatial state (mob position/spread vs. the kit's reach-per-tick). This is the encounter-side substrate; building a kit-side abstraction instead is the AoE-proxy trap.
- `spatial_gauntlet/spatial_telemetry.py` — `SpatialFightResult` / `FightEvent` (star-lord schema 2.12/2.14) + the `NullSpatialTelemetryWriter` convergence-path fallback (`balance_loop.py:2774`). Relevant to the Principle-6 boundary below.
- Disciplines #1 (math-before-code — the mechanic definition + measurable criterion are the load-bearing decisions; define BEFORE building), #2 / #2.1 (smoke-test + resource-scaling), #11 (empirical honesty), #1.2 (math-note code-citation).

## Math-before-code (MANDATORY — this is the load-bearing decision; HALT for Gate-1)

Author a math-note FIRST that defines:

1. **The coverage/spatial-pressure mechanic, derived from the EXISTING spatial arena + code-cited (A2 — the decisive guard).** gandalf's framing: a pure-ST kit cannot cover many simultaneous low-HP mobs, so some fraction of swarm mobs remain "uncovered" each tick and apply pressure the kit cannot prevent. **The mechanic MUST be derived from spatial state** — mob position/spread vs. the kit's reach-per-tick in `SCENARIO_OPEN_ARENA` (build on the `spatial_engine.py:81-82` coverage-gap concept) — **NOT from the kit's AoE-share count.** The AoE-share lever (role-floor Rule A, 4 area skills) was ALREADY proven insufficient because it acts on kit COMPOSITION; a position-derived coverage cost acts on the encounter GEOMETRY, which ST throughput cannot increase by adding skills.
   - **MANDATORY falsification test for the guard (jack-ryan will check this at the math-note Gate-1):** state explicitly — *"if this mechanic's pressure can be driven to zero by a kit adding AoE skills WITHOUT moving/repositioning, it IS the dead lever — name why it cannot."* If you cannot state why repositioning (not skill-count) is the only buy-out, the mechanic is the AoE proxy and must be redesigned before any build.
2. **The measurable PASS criterion (A1 + A3 — pin to real constants, full band).** Reuse your locked Prereq-B 3a/3b/3c vocabulary. The spike PASSES iff, on the rogue cell with the coverage mechanic active:
   - **(a) swarm WR ∈ `[TIER_FLOORS["swarm"]=0.65, TIER_CEILINGS["swarm"]=0.80]`** (BOTH bounds, `balance_loop.py:533/540`) — i.e. swarm comes INTO band, not merely off the 1.0 ceiling. A crater-everything outcome (swarm driven SUB-floor) is an **HONEST_FAIL**, not a pass.
   - **(b) the global modifier converges OFF the floor** — pin this to a REAL cited constant: `MODIFIER_SEARCH_FLOOR=0.01` (`:318`) is the literal search floor; the observed floored value was `0.0719`. Resolve in the math-note which threshold is operative (the search floor itself, or a margin above it) and state the numeric PASS bound. (`MODIFIER_FLOOR_NEAR` does NOT exist — do not cite it.)
   - **(c) the upper tiers (elite/mini_boss/boss) clear their `TIER_FLOORS`.**
   All three prongs conjunctive. Define each numerically against `balance_loop.py`.
3. **The HONEST_FAIL meaning.** If the coverage mechanic does NOT bring swarm into band, OR brings swarm down but the upper tiers still don't clear, that is a VALID, load-bearing outcome — it means the architectural limitation is deeper than swarm-coverage and needs a different rework. Report clearly; do NOT force a pass.

**HALT for jack-ryan Gate-1 on the mechanic + criterion math-note — MANDATORY.** The mechanic design is the decisive act (a coverage mechanic that's secretly an AoE proxy would re-test the falsified lever and waste the spike). Do not build before Gate-1 clears.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

The spike is a SIMULATION-INTERNAL mechanic (fight engine / balance loop / spatial arena). It does NOT add/modify/rename/remove any telemetry schema field, fight_log key, loadout key, or export packet structure. **Round-trip: not applicable BECAUSE (i) the convergence swarm slot writes through the `NullSpatialTelemetryWriter` (`balance_loop.py:2774` — no DB write on the convergence path) AND (ii) the spike adds NO field to `SpatialFightResult` / `FightEvent` (star-lord schema 2.12/2.14).** Both conditions must hold for the not-applicable claim to stand. **HALT TRIGGER (A4):** if measuring coverage requires emitting a NEW spatial-telemetry field on `SpatialFightResult` / `FightEvent`, that touches star-lord's schema 2.12/2.14 contract — HALT and flag a MIGRATION.md before proceeding. Verify-don't-assume the boundary (per your own Prereq-B math-note §4 discipline).

## Scope

- [ ] **Math-note FIRST** (mechanic + measurable criterion + anti-AoE-proxy guard), code-cited. HALT for jack-ryan Gate-1.
- [ ] Build the coverage mechanic as a **SPIKE** — flag-gated / harness-local, NOT a default `balance_loop.py` behavior change. The default sim must be unaffected when the flag is off.
- [ ] Run the spike on the rogue cell FOREGROUND-BLOCKING; compare swarm WR + converged modifier + upper-tier WRs with the mechanic ON vs OFF (the OFF arm reproduces your `d003f8f` refire baseline as the control).
- [ ] Report PASS or HONEST_FAIL against the criterion, with the numbers.
- [ ] Smoke slice is sufficient if decisive (as it was for the refire); no full regen required to record a PASS/FAIL on the rogue cell.
- [ ] AGENT_STATE.md updated; tag `gamora/v1.x-swarm-coverage-spike` (seam-prefixed).

## Out of scope (explicit non-goals)

- **NO production wiring.** This is a spike to answer the architectural question. A PASS authorizes a FUTURE production-design conversation (gandalf + Matt), not an immediate feature ship.
- **NO per-tier-modifier implementation as the primary lever** (gandalf's anti-pattern). You MAY run a per-tier-modifier arm as a COMPARISON baseline if it sharpens the read (it demonstrates the band-aid passes the sim while the experience stays broken) — but the coverage mechanic is the lever under test.
- **NO composer / generation changes** (rocket's seam — the role floor stays as built).
- **NO b6 deletion / no touching `balance_loop.py` ARCHETYPE_TEMPLATES imports.**
- **NO caster / L1 / L2 work.**
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)

- What is the cleanest fight-engine expression of "coverage cost a pure-ST kit can't buy out"? (mob-count-scaled uncovered-mob pressure is the gandalf framing — but you own the sim; pick the expression that is genuinely encounter-side, not kit-clear-rate-side.)
- Does the mechanic need to scale with mob count / mob density, and is the swarm matchup's mob model rich enough to express it, or does the swarm encounter itself need a (spike-local) enrichment?
- What's the control arm — your `d003f8f` refire numbers, re-run with the flag OFF, same seed? (INFO-1: the OFF arm must reproduce `d003f8f`'s converged numbers on the GENUINE close/single-target coordinates — `def_bin=glass`, `eng_bin=close-fast`, `geo_bin=single-target` per §8 — i.e. swarm 1.0, modifier 0.0719, upper tiers ~0.0; NOT the earlier medium-range b6 framing. Record the OFF-arm numbers and confirm they match `d003f8f` before trusting the ON-arm delta.)

## Sequence

jack-ryan Gate-1 on this dispatch → gamora mechanic+criterion math-note → **HALT, jack-ryan Gate-1 on the math-note (MANDATORY)** → gamora build (flag-gated spike) → gamora run (foreground-blocking, ON vs OFF) → **jack-ryan Gate-2 on the result** → KR carries the result + gandalf design-read to Matt. A PASS re-frames the architectural hypothesis as RESOLVED-WITH-A-LEVER (production-design conversation follows); a HONEST_FAIL deepens the architectural finding and feeds the next probe.

## References

- gandalf disposition note + § 6-octies (recognition record): the lever location + per-tier anti-pattern.
- gamora refire result `d003f8f` + math-note §8: the baseline this spike's control arm reproduces.
- rocket role-floor `52703c9` (`rocket/v2.2-envelope-role-floor`): the composer fix that stays as built (necessary, not sufficient).
- Recognition record `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quater (Decision 2, HELD) / § 6-septies / § 6-octies.
