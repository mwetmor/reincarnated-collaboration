# Dispatch — 2026-07-07 — gamora — caster-viability bar re-derivation (instrument-matched)

**From:** knight-rider
**To:** gamora (lead — simulation/metrology)
**Approved by:** Matt 2026-07-06/07 (relayed the critique-pair-aligned 5-step sequencing; this is step 1)
**Estimated effort:** ~2–4h — measurement + report; a fire (batch-1 martial kits on the Leg-B shells) + analysis
**Acceptance:** per-shell martial DISTRIBUTIONS (not just floors) re-derived on the IDENTICAL instrument as the Leg-B pilot (same shells, same mob count/HP/dmod, same window, same clearing definition), with the pre-registered validity check answered: **can batch-1 martial kits reach the current 9.90 / 11.65 bars on THIS 8-mob dispersed wall?** If they cannot, the bars were never valid for this shell — that is itself the finding.

## Context

The Leg-B economy pilot HALTed (0/25 caster configs clear). gandalf's structural finding + gamora's per-cast ledger spike converged through a critique-pair pass (finding §8 CORRECTION, commit `9fb3467`):

- The 2.3384× fossilized seed ratio is **net-cancelled** by the caster-only weapon spell pool (SC-6b: INT avg 88.4% spell_damage_modifier, live in the pilot via the un-nested gauntlet builder). Net per-cast the caster is within **~1.07–1.25× of the martial** — NOT the "43% per cast" gandalf §2 originally claimed (retracted).
- The dominant single-target deficit (~3–6×) is **spatial/geometry throughput** (single_target rotation vs a dispersed 8-mob wall; pack-multiply never fires) and is **PATH-SYMMETRIC** — a martial single_target kit eats the same de-rating.
- **Rank-1 defect (reconciled stack, finding §8.3) is a bar/instrument MISMATCH:** the 9.90 martial bar EXCEEDS the 8-mob wall's throughput cap (`spatial_engine.py:2527`, `mobs_killed = sum(...)` with NO respawn; open_arena spawns 8, `arena.py:366-378`). A per-fight mobs-killed metric on an 8-mob wall cannot reach 9.90. So the 9.90/11.65 bars were derived on a DIFFERENT (martial-native) shell, not the caster's shell. Part of the nominal "4× residual" is a **units mismatch**, not mechanism.

**This step is metrology, NOT F-d bar-lowering.** The C2 principle (a caster must meaningfully kill lone targets) survives untouched. What is contested is whether the NUMBER (9.90) was derived on the same instrument the caster was measured on. We re-derive the number on the matched instrument; we do not move the principle.

## Required reading before starting
- `agentic_orchestration/gandalf/notes/2026-07-06-caster-single-target-structural-finding.md` — **§8 CORRECTION (reconciled defect stack §8.3) + §7 (fix-build constraints: instrument-shape calibration; distribution sizing — NOT floor-scraping).**
- `reincarnated-engine/src/reincarnated/simulation/notes/caster-single-target-ledger-spike-2026-07-06.md` — your own ledger, esp. §7 (the 9.90-exceeds-8-mob-cap finding) + §2 (the spatial residual).
- `agentic_orchestration/dispatches/2026-07-06-star-lord-batch2-legB-fire-economy-pilot.md` — the pilot's exact shell construction (`economy_pilot_driver.py:249-269,288`, the 8×300k open_arena + 500k chokepoint, dmod=0.3).
- `agentic_orchestration/batch2-run-state-2026-07-06.md` — the C2 floor provenance (9.90/11.65 byte-verified `db2df69`) and where those bars originally came from (the batch-1 martial floor).

## Math-before-code (Discipline #1)
Before firing, document:
- The EXACT instrument the pilot used (shell mob count, HP, dmod, window seconds, clearing/kill definition) — cite `economy_pilot_driver.py` lines.
- The instrument the 9.90/11.65 bars were ORIGINALLY derived on (batch-1) — cite the source. Name every axis on which the two instruments differ (mob count, HP, respawn, window, metric normalization).
- The pre-registered validity check (below), written down BEFORE the fire so it cannot be back-fit.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)
**NO.** This is a measurement fire + report. No telemetry schema field, no fight_log key, no loadout key, no export shape, no inter-seam fixture is added/modified/renamed/removed. Reading batch-1 martial kits and running them on the existing Leg-B shells uses the already-Gate-2-verified production path. `Round-trip: not applicable — no cross-seam contract change; instrument-matched measurement fire consuming existing shells + existing kits.`

## Scope
- [ ] **Re-run batch-1 martial kits on the IDENTICAL Leg-B shells** — open_arena (8×300k dispersed, dmod=0.3) AND chokepoint_corridor (500k, dmod=0.3), same 120s window, same clearing/kill definition, production (`from_player_class` → bounded pool) path.
- [ ] **Report per-shell martial DISTRIBUTIONS** (min / median / spread / max), not just a floor — finding §7.2: sizing target is the martial distribution shape, so the eventual re-pilot GO criterion can be yield-rate comparability, not bare floor-clearance.
- [ ] **Answer the pre-registered validity check** (below) explicitly.
- [ ] Sequential, ONE registered run; seed+SHA+config reproducibility; detached per Discipline #19 if the run exceeds a few minutes; canonical-JSON checkpoint before the gauntlet.
- [ ] Measurement report via the measurement-report path (no demo-bundle coupling).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-batch2-caster-bar-rederivation-1`

## PRE-REGISTERED validity check (write it down BEFORE the fire — do NOT back-fit)
- **Q1:** Can batch-1 martial kits reach 9.90 (open_arena) and 11.65 (chokepoint) on THIS instrument (8-mob dispersed wall, matched window/metric)?
  - **If YES** → the bars are valid for this shell; the caster deficit is real on the matched instrument and step-3 re-pilot proceeds against these (confirmed) bars.
  - **If NO** (martials also cannot reach 9.90 on the dispersed wall) → the bars were NEVER valid for this shell. Report the re-derived per-shell martial distribution as the corrected calibration target. This is a finding, not a failure.
- **Q2:** What is the martial per-shell DISTRIBUTION on the matched instrument (so step-4 F-b sizing, if any, is distribution-shaped, not floor-scraping)?

## Acceptance criteria
- [ ] Per-shell martial distributions on the matched instrument, both shells.
- [ ] Q1 answered YES/NO with the measured numbers.
- [ ] Q2 distribution reported.
- [ ] Calibration target for the eventual re-pilot named = the two-shell structure (open_arena + chokepoint as separate gates — the C2 band shape), NEVER a whole-encounter median (finding §7.1 — don't re-fossilize).
- [ ] Round-trip: not applicable because no cross-seam contract change (measurement fire only).

## Out of scope (explicit non-goals)
- **NO constant changes** — no BASE_SPELL, no multiplier, no bar edit. This step establishes the *correct number*; whether the caster gap survives it, and any F-b, are steps 3–4.
- **NO C2 principle change** — this is NOT F-d. The principle (casters meaningfully kill lone targets) stands; only its instrument is being matched.
- **NO caster re-pilot in this step** — step 3. This step measures MARTIALS on the matched instrument to establish the target.
- **NO nesting-bug fix** — that is the parallel step-2 dispatch (rocket+gamora). Pilot/gauntlet path is unaffected by the nesting bug (different builder), so this measurement is valid as-is.
- **NO whole-encounter (boss_with_adds) calibration target** — the pack channel hides the per-cast asymmetry; the two-shell structure is the target (finding §7.1).
- **NO Axis-5 back-door.**

## Open questions for the agent to resolve
- Whether the batch-1 martial kits need role-split stratification even for the bar re-derivation, or whether a representative attack-composition martial is the right bar-setter (document the choice; the caster re-pilot in step 3 WILL stratify).
- Detached vs in-session per Discipline #19 based on measured run time (checkpoint first either way).
- The exact clearing definition to freeze (fraction-of-wall vs absolute-kills-in-window) so step-3 uses the identical one.

## References
- gandalf finding §7/§8 (`9fb3467`); gamora ledger `79796e2`; pilot fire dispatch + run `617409b8`
- C2 floor provenance `db2df69`; run-state `batch2-run-state-2026-07-06.md`
- Discipline #1 (math-before-code), #11 (attribution), #18.1 (substrate-voting/measurement is a gate), #19 (detached run), #24 (per-cohort measurement)

---

## Completion record
<!-- gamora appends on completion -->
