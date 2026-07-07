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
- [ ] **(Gate-1 condition 1) Clearing definition FROZEN as an explicit output artifact** — emit the exact clearing/kill definition used (fraction-of-wall vs absolute-kills-in-window, window seconds, metric) as a named field in the report so **step 3's re-pilot cites it VERBATIM**. Do not leave it implicit — an un-emitted definition is a soft loop that lets step 3 drift.
- [ ] **(Gate-1 condition 2) Q1 metric normalization PINNED** — report RAW mobs-killed per fight AND any normalization applied; explicitly flag if a metric OTHER than absolute-kills-in-window is needed for caster-vs-martial comparability. (The original failure was a mob-count normalization mismatch — this prevents an accidental "YES" dressed over a "NO".)
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

**gamora — 2026-07-07 — COMPLETE**

**Metrology fire executed. Q1 = NO on both shells; the 9.90/11.65 bars were NEVER valid for the caster's instrument.**

### Reproducibility
- **Run ID:** `8e98a01d-84a7-4c80-afa8-356c34454e70`
- **Seed base:** `63_000_000` (disjoint from pilot's 62M block)
- **Engine SHA at run:** `6811239`
- **Config:** 8 STR/DEX (martial) cells × 5 role-split templates × 2 shells × 10 fights = 80 records; DEFAULT economy; production `from_player_class` → bounded pool
- **Wall time:** 14.8 s in-session (below the Discipline #19 detached threshold; canonical checkpoint written pre-gauntlet regardless)
- **Driver:** `reincarnated-engine/src/reincarnated/simulation/martial_bar_rederivation_driver.py` (reuses `economy_pilot_driver._build_mob_dicts_calibrated` + the same kit-build/production fight path → BYTE-IDENTICAL wall to the pilot)
- **Math note (Discipline #1, written BEFORE the fire):** `reincarnated-engine/src/reincarnated/simulation/math/caster-bar-rederivation-instrument-match-2026-07-07.md`
- **Report note:** `reincarnated-engine/src/reincarnated/simulation/notes/caster-bar-rederivation-2026-07-07.md`
- **Report JSON:** `reincarnated-engine/src/reincarnated/output/martial_bar_rederivation/martial_bar_rederivation_report.json`
- **Tag:** `gamora/v-batch2-caster-bar-rederivation-1`

### Q1 — pre-registered validity check ANSWERED (with numbers)

| Shell | Bar under test | Martial MAX (mean-mobs-killed) | Metric ceiling | Q1 |
|---|---|---|---|---|
| open_arena | 9.90 | **8.0** | 8.0 | **NO** |
| chokepoint_corridor | 11.65 | **8.0** | 8.0 | **NO** |

The metric `mean_mobs_killed` is hard-capped at the spawn count 8 (`spatial_engine.py:2527,3262`; 8 spawns `arena.py:366-378,435-443`; no respawn). `8.0 < 9.90 < 11.65`. No martial, at any power, can reach the bars on an 8-mob no-respawn wall. Pre-registered arithmetic (math note §2-3) confirmed empirically. **The bars were never valid for this shell — that is the finding.**

### Q2 — martial per-shell DISTRIBUTION (matched instrument, 40 kits/shell)

| Shell | min | median | mean | max | spread |
|---|---|---|---|---|---|
| open_arena | 1.0 | **8.0** | 7.125 | **8.0** | 7.0 |
| chokepoint_corridor | 2.2 | **8.0** | 7.288 | **8.0** | 5.8 |

Distribution is **ceiling-saturated + bimodal**: 7/8 cells saturate the 8.0 ceiling (kill all 8) across ALL 5 role-split templates; 1 cell (`endgame_bc_melee_high_flat_dex_none`) floors at ~1 (open) / ~2-3 (choke) — a per-cell engagement stall vs the dispersed high-HP wall (the path-symmetric single-target throughput regime, ledger §2), not template/noise. Because the healthy martial mass is PINNED at the ceiling, this instrument cannot represent 9.90/11.65 at all.

### Gate-1 conditions honored
- **Condition 1 (clearing definition FROZEN):** emitted as the named `frozen_clearing_definition` field in the report JSON + report note §3 — metric = ABSOLUTE mean-mobs-killed, kind = absolute-kills-in-window, window = 120.0 s, ceiling = 8, no respawn, open 300k/choke 500k HP, dmod 0.3, production path. Includes a `NOTE_FOR_STEP3` directing the re-pilot to cite it verbatim and NOT compare against 9.90/11.65 as if reachable on 8 mobs.
- **Condition 2 (Q1 normalization PINNED):** emitted as the named `q1_normalization_pin` field — RAW mean-mobs-killed, NO normalization; comparability flag states no metric other than absolute-kills-in-window is needed for caster-vs-martial comparability ON THIS SHELL, and explicitly guards against an accidental "YES" dressed over a "NO."

### Were the bars valid for this shell?
**NO.** Bar/instrument mismatch (metrology), not a caster-power defect, not a reason to move the C2 principle. **Corrected calibration target named = the two-shell structure** (open_arena + chokepoint as separate gates; NEVER boss_with_adds — finding §7.1). Flagged for step 4 (not actioned): because the martial mass saturates the 8.0 ceiling, a distribution-shaped sizing target with martial HEADROOM above the caster requires a higher-ceiling instrument (more spawns / respawn / a kills-per-minute RATE metric — a DIFFERENT metric) — a step-3/4 instrument-design decision, out of scope here.

### Scope honored (HARD out-of-scope)
NO constant change, NO bar edit, NO C2 principle change (NOT F-d), NO caster re-pilot (step 3), NO nesting-bug fix (parallel step-2 rocket — pilot/gauntlet path uses the un-nested builder, measurement valid as-is), NO boss_with_adds target, NO Axis-5 back-door. Round-trip: not applicable (measurement fire; no cross-seam contract change; the driver imports two read-only helper functions from `economy_pilot_driver.py` — a read, not a modification; no MIGRATION.md required).

Auto-committed; NO push (Matt-gated).

<!-- gamora appends on completion -->
