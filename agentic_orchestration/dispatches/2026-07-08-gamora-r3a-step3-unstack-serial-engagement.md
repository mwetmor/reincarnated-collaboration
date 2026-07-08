# Dispatch — 2026-07-08 — gamora — R3a step 3: MOB_HP un-stack (Option A) + serial-engagement pass + winner-tally recording flip

**From:** knight-rider (chain-orchestrated; KR fires the sub-agent himself per the pre-ratified execution protocol)
**To:** gamora (simulation seam — sole seam; no cross-seam boundary expected, see Principle-6 gate below)
**Approved by:** Matt 2026-07-08 (§6 fork ruled **A / YES / YES**) — this dispatch EXECUTES that ruling. Pre-authorized; no fresh run-auth.
**Estimated effort:** gamora medium–large. Math-note-first (×2-3). Gate-2 (coordinated). Multi-step.
**Chain position:** R3a step 3 (of the batch2 pre-ratified chain). Precedes step 4 ($0 gauntlet re-run → §4 gradient check).

## Why this exists
R2 confirmed the endgame-BC gauntlet WR surface is floor-saturated at both rails (0/18, bands 17/1/0, all extremes exactly 0.000/1.000 — a step function, not a gradient). Matt ruled the §6 fix **A/YES/YES**. This dispatch implements it. The before-side §8-A1 band snapshot is already captured (R2, `leg3_pilot_section8a1_band_measurement.json`, seed 56M, committed `75637f5`).

## Required reading (session-start)
- `agentic_orchestration/gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md` — the full design read; esp. §3 (Levers 1-2, ruled), §4 (acceptance criterion), §5.2-AMEND (gandalf ruling (a): fold recording flip into this step; no dedicated before-side split re-run).
- `agentic_orchestration/gamora/notes/2026-07-08-spatial-floor-saturation-g1-g2-design-finding.md` — your own G1/G2 diagnosis.
- `agentic_orchestration/gamora/notes/2026-07-08-floor-termination-split.md` — your fail-loud telemetry-gap finding + winner-tally recording-flip recommendation.
- Run-state `agentic_orchestration/batch2-run-state-2026-07-06.md` — Matt ruling block (lines 817-841) + the last four KR DELTAs.
- Engineering disciplines #1 (math-before-code), #1.1 (resource-bounds projection), #2.1 (smoke-test resource-scaling), #11 (attribution — do NOT trust the log's `1.5→1.25` remedy as truth; it was DISPROVEN by your own G1), #23 (framing-audit at math hotspots).

## Deliverables (each math-note-first per Discipline #1; Gate-2 on the coordinated set)

### D1 — Option A: un-stack `MOB_HP_DIFFICULTY_MULTIPLIER` from the endgame-BC gauntlet path
- **What:** the endgame-BC gauntlet path stops applying `MOB_HP_DIFFICULTY_MULTIPLIER` (application site ~`spatial_engine.py:3441`, scenario-membership gated). The constant `1.5` STAYS in `arena.py:49` untouched — it remains ruled for the legacy convergence instrument (2026-05-19). This is **scope-retirement, NOT a constant move** (Goodhart guard: you refused to MOVE the constant to green the pilot — that refusal stands; this removes an un-re-ruled STACKING of it from a path the 2026-05-28 endgame profile explicitly said it "DOES NOT modify").
- **Math-note:** cite the 2026-05-28 endgame-profile "rather than applying a runtime multiplier" intent; show the budget effect (gandalf §3: open_arena/chokepoint kill-budget drops ~33%, 1.59M→1.06M). Confirm no other endgame path depends on the multiplier being applied.
- **Verify:** the legacy convergence-instrument path (the one the ×1.5 WAS ruled for) is UNAFFECTED — the un-stack is scoped to the endgame-BC gauntlet path only.

### D2 — Lever 2: serial-engagement / pack-local activation for `open_arena` + `magic_pack`
- **What:** pack-local activation so open rooms engage in proximity waves (~3-4 serial bites) instead of whole-field alpha-strike from tick 0. gandalf §3 Lever-2 suggests trash activation radii in the ~12-15m range as a starting point — **you math the actual radii** from room geometry (open_arena spawn tables: player at (18,30), nearest trash ~7-10m, farthest ~30m, ~40 mobs; magic_pack: 14m-deep room, ~24 mobs) + desired bite size. Also address the inherited-uncalibrated `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0` (gandalf §3: calibrated 2026-05-19 for the RETIRED 50×50 geometry, never re-checked against the 2026-07-07 36×36 re-base — a third inherited-uncalibrated constant).
- **Math-note (framing-audit, Disc #23):** show the wave-count arithmetic; state assumptions (activation radius → expected concurrent engagement → bite size); this is restoring the room's OWN stated certification intent ("repositioning cost" presumes engagements to reposition between) + genre open-field grammar (D2 pack-local aggro, D3 density pulls, PoE pack spacing). NOT instrument-softening — a total-aggro open field is bad GAME design the sim built by accident.
- **magic_pack note (gandalf §3 Lever-3):** do NOT add magic_pack to `MOB_HP_DIFFICULTY_SCENARIOS` (that would make it HARDER; the floors say it already over-kills). Same serial-engagement treatment and/or room-depth address.

### D3 — Winner-tally recording flip (gandalf §5.2-AMEND: fold into this step; within-seam)
- **What:** record the per-(class, scenario) `winner ∈ {player, monster, timeout}` tally (3 ints per row) into the gauntlet results JSON aggregate, so the step-4 $0 re-run yields the death-vs-timeout termination split NATIVELY. `winner` is already computed + passed to `write_fight_result` — no fight-loop change.
- **gandalf design lean:** keep it as an **in-JSON gamora-side aggregate → within-seam, NO MIGRATION, NO star-lord hand-off.** It would ONLY need MIGRATION + star-lord IF you land it as a persisted `spatial_fight_results` DB column. **YOUR final boundary call** (Principle-6 gate below) — if you choose the DB-column path, MIGRATION + star-lord coordination is REQUIRED.

## Acceptance criterion (the anti-Goodhart gate — gandalf §4; NOT "N/18 pass")
The ultimate validation is step 4 ($0 re-run, separate). The bar there: **the WR surface regains a gradient — meaningful per-scenario WR mass in (0.05, 0.95) across the 12-kit population; per-kit differentials (corridor vs open) persist as SPREAD, not RAILS.** Kits still floored on a CALIBRATED gradient are TRUE content findings — REPORT them, do NOT fix content to satisfy the instrument (rider 4). This dispatch's job is the levers + instrument; step 4 measures whether they worked.

## Smoke-test expectation (Disc #2.1)
- D1: smoke that the endgame-BC path no longer multiplies mob HP by 1.5 (assert a representative endgame mob's effective HP dropped by the expected factor) AND the legacy convergence path is unchanged.
- D2: smoke that pack-local activation produces staged engagement (not all mobs active at tick 0) in open_arena + magic_pack — a small deterministic fight showing <full-field concurrent activation early.
- D3: smoke that the winner-tally appears in the results JSON aggregate for a tiny run (3 ints per row, sums to fight count).
- **Resource projection (Disc #1.1):** state peak memory + expected wall-clock for the step-4 re-run (the R2 re-run was ~25 min / <5MB — confirm your changes don't blow that up; serial-engagement may change fight duration).

## Principle-6 cross-seam gate (knight-rider, at authoring)
- **D1 (un-stack):** application-site change, no boundary field moves. Round-trip: N/A. NO MIGRATION expected.
- **D2 (serial-engagement):** simulation-internal engagement model; no boundary field. NO MIGRATION expected.
- **D3 (winner-tally):** **CONDITIONAL.** In-JSON gamora-side aggregate (gandalf lean) = within-seam, NO MIGRATION. IF you choose the persisted DB-column path = boundary field crosses to star-lord telemetry → **MIGRATION.md + star-lord coordination REQUIRED** (ADR-004). You make the call; if it crosses, flag KR to fire star-lord.

## Tag + Gate-2
- Tag: `gamora/v-r3a-step3-unstack-serial-engagement-1` (seam-prefixed per convention).
- Submit the coordinated set to `agentic_orchestration/qa/pending/` for **jack-ryan Gate-2** (balance/difficulty-affecting engine change — un-stack + engagement-model + recording).
- Auto-commit (authorized cycle work). Push granted (R6 push-as-you-go). Report commit hash(es) to KR.

## Out of scope (explicit non-goals)
- **NO Lever-1 constant MOVE** — un-stack is scope-retirement; `arena.py:49` stays `1.5` for the legacy instrument.
- **NO content/kit re-tuning to pass the gate** (rider 4). Kits floored on a calibrated gradient = TRUE findings, reported not fixed.
- **NO Lever-4 certification-criterion change** — that is a CONDITIONAL Matt touchpoint later, ruled with step-4 data IF structural fails persist on a working gradient.
- **NO step-4 re-run in this dispatch** — this dispatch produces the levers + recording; the $0 re-run + gradient check is R3a step 4 (KR fires it separately after Gate-2).
- **NO leg-3 wire / chassis / bars / bands / kit-constant touches** (frozen).
- **NO extension of the multiplier to magic_pack** (would make it harder; wrong direction).

## Open questions for gamora to resolve
- D2: the actual activation radii + whether `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0` needs re-basing to the 36×36 geometry (your math).
- D3: in-JSON aggregate (gandalf lean, within-seam) vs persisted DB column (needs MIGRATION + star-lord) — your file-owner boundary call.
- Whether magic_pack needs room-depth address in addition to serial-engagement (gandalf §3 Lever-3 raised both).

## References
- gandalf design read + §5.2-AMEND (`1906598`); gamora G1/G2 (`03076c0`) + termination-split (`18dbba5`); R2 before-side artifact (`75637f5`); dispatch `2026-07-08-gamora-starlord-spatial-floor-diagnosis.md`; run-state `batch2-run-state-2026-07-06.md` (817-841 + recent deltas). ADR-004 (MIGRATION), Principle 6, Disciplines #1/#1.1/#2.1/#11/#23.

## Completion record
*(gamora appends on completion: math-notes, code changes, smoke results, resource projection, tag, Gate-2 path, boundary call on D3, commit hashes.)*
