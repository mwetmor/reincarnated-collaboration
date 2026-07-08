# Finding — 2026-07-08 — F4 escape_lane band registration (Gate-2 + Lane-3 ratification)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-CONDITIONS (no BLOCK)
**Target:** `gamora/v-batch2-f4-escape-lane-registration-1` (engine `84ad40d`)
**Developer:** gamora (simulation seam)
**Principles applied:** #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log as truth), #5 (severity), plus review-principle cross-seam-round-trip
**Disciplines cited:** #1 (math-before-code), #11 (empirical inspection over assumption), #12 (semantic-shift framing), #13 (inherited-uncalibrated drift check), #23 (framing-audit)

---

## Verdict

**PASS-WITH-CONDITIONS.** The wiring is correct at source, the smoke is a genuine gate (not a rubber-stamp), F1/F2/F3/T1-pilot are byte-identical, the field-identity is exact, and gamora's density derivation reaches the inherited bars from INDEPENDENT premises (Pressure-1 resolved in her favor). The single carried condition is a MANDATORY re-check of the never-observed band against the first live escape_lane distribution the R4 sweep produces (Pressure-2). **R4 cert sweep is CLEARED to fire.**

---

## PRESSURE 1 — "CONFIRMED by construction": independent verification, NOT a circular rubber-stamp

**Finding: the derivation is independent. The CONFIRM stands.**

The test I applied: could gamora have reached exit≈0.95-1.0 / KPM-ceiling-headroom / KPM-floor-as-arrival-rail WITHOUT reading the spec's stated "60-150" and "80-90%+" numbers? Yes — and she did. Every premise in math-note §3 is a spawner/geometry parameter I verified independently at `arena.py:1058-1097`:

- 55m travel = `escape_threshold_m=58.0` − player `y=3.0` (not a bar).
- ~3 fodder/s = `ContinuousSpawnSpec(interval_s=1.0, group_size=3)`; ~180 streamed + 12 initial (`_build_escape_lane_initial_spawns`) = ~192 supply (not a bar).
- `engaged_cap=50`, `escape_elevation_multiplier=2.0`, `max_duration_s=60.0` (all room params, not bars).

From these she DERIVES a demand — exit≈0.95-1.0 (from the ~5× travel-budget ratio: 55m at ~5 m/s ≈ 11s inside a 60s window), a KPM supply ceiling ~192, a KPM arrival-tempo floor ~180/min raw — and THEN compares the inherited 0.80 / 150 / 60 against that demand. The comparison direction is honest: the exit floor (0.80) lands ~0.15-0.20 BELOW the geometry-implied 0.95-1.0 (correct anti-curve-fit direction for a floor — the floor does not over-demand); the KPM ceiling (150) lands BELOW the ~192 supply ceiling with ×1.28 headroom (reachable-but-flagging, not inert). Neither derivation back-reads the spec bar it is checking.

**Why this is NOT the tautology KR flagged.** A circular rubber-stamp would compute "the room streams 150/min because the spec says the KPM ceiling is 150." gamora computes the supply ceiling as ~192 from `interval×group×window` and observes 150 sits *below* it — a different number, reached from spawner arithmetic, that the bar must sit under. Same for exit: geometry says ~0.95-1.0, the bar is 0.80 — the derived demand and the bar are DIFFERENT numbers, and their relationship (bar-below-demand) is the honest signature, not their equality.

**The honest caveat I record (does not change the verdict):** a CONFIRM is inherently *weaker corroboration* than an ADJUST would have been informative, precisely because the room was tuned to the genre spec — so agreement was the expected prior. gamora states this openly (math-note §4: "consistent by construction of the room"). That candor is the right posture: the CONFIRM is real but low-information, which is exactly why Pressure-2's re-check condition matters. The rider (verify, don't rubber-stamp) is HONORED — she density-verified and could have returned ADJUST; the arithmetic simply landed CONFIRM. Contrast step-5/step-6, where the room had drifted under a stale band → ADJUST; here the room and bars are the same Q11 generation → CONFIRM. Both are legitimate rider outcomes.

## PRESSURE 2 — registering a never-observed band: ACCEPTABLE to ship, but CONDITION-GATED

**Finding: acceptable as geometry-only registration, on a MANDATORY re-check condition.**

The band is registered with the anti-curve-fit cross-check `HONESTLY UNAVAILABLE` — there is no observed escape_lane exit/KPM distribution on disk because the F4 branch was dead (I confirmed: F4 constants did not exist at parent `b30c4ae`, grep count 0). So the band is geometry-only, unvalidated against any real escape_lane result. The R4 cert sweep (KR fires next) will be the FIRST live escape_lane data.

Registering it geometry-only is acceptable HERE because: (a) the dispatch explicitly instructed geometry-only derivation + flag-cross-check-unavailable + do-not-invent-a-distribution — she followed that exactly; (b) the fail-safe direction is correct — `getattr(r, "tier_2_survival_rate", None) or 0.0` means a missing/zero exit fraction fails PRIMARY, so an un-exercised path cannot manufacture a pass; (c) she named the falsifier (math-note §4).

But a geometry-only band is a HYPOTHESIS about the distribution, not a measurement of it. It must not silently harden into a trusted VALUE. Hence:

**CONDITION 1 (MANDATORY, re-check):** After R4 produces the first scored escape_lane distribution, the F4 band gets re-validated against it — the geometry-vs-p90 anti-curve-fit cross-check that was UNAVAILABLE here MUST be run then. The named falsifiers stand: if the viable-kit exit MODE lands <0.80, or the KPM mode is pinned at 150, the CONFIRM is falsified and the bars revisit. **This re-check must complete before R5 band-sheet VALUES are trusted** (R5 is a Matt touchpoint per the chain; the band feeding it cannot be a never-observed number treated as final).

**CONDITION 2 (records-only):** the CONFIRM is registered as PROVISIONAL-PENDING-FIRST-OBSERVATION in the decisions-log entry (done below), so the log reflects that the band is geometry-anchored-only until R4 corroborates.

---

## Standard Gate-2 verifications

- **Disc #1 (math-before-code): PASS.** Math-note `f4-escape-lane-band-registration-2026-07-08.md` precedes the code; density-anchored method matches the step-5/step-6 template (`r3a-step5/step6` notes cited). Framing-audit §0, provenance §1, derivation §3, verdict §4, wiring §5, semantic-shift §6, boundary §7, HALT-check §8 — structurally complete.
- **Field-identity (Disc #11): PASS, verified at source.** `spatial_engine.py:2874-2888` (in `spatial_gauntlet/`): for `win_condition=="escape_reached"`, `winner=="player"` IFF `self._escape_reached` (dead→"monster", window-elapsed→"timeout"). Therefore `tier_2_survival_rate` (= player-wins/n) IS the exit-within-window fraction for an escape room. The whole F4 gate rests on this and it holds exactly. No new field, no schema.
- **Wiring correctness: PASS.** The new F4 branch sits BEFORE the clear-shell KPM lookup, so escape_lane returns a real verdict rather than falling through to a no-band `return False`. Constants `_F4_ESCAPE_SHELL_GATE_TYPES / _F4_EXIT_WITHIN_WINDOW_FLOOR=0.80 / _F4_KPM_BAND=(60.0,150.0)` match math-note §5 exactly. PRIMARY (exit) evaluated before SECONDARY (KPM); fail-safe on missing fields.
- **Smoke re-run by me: PASS.** `gamora_f4_escape_lane_registration_smoke_2026_07_08.py` exit 0. It is a GENUINE gate test, not a rubber-stamp: exit-at-floor 0.80 inclusive passes / 0.79 fails PRIMARY; KPM 59 and 151 both fail SECONDARY; boss survival-bit with KPM ignored; a failing escape_lane cohort does NOT certify (no manufactured pass). `family_certification_pass` + `season_emit` reachable-True for an all-four-passing cohort AND False for a walled kit — both limbs proven.
- **F1/F2/F3 byte-identical: PASS.** Boss branch (survival validity bit, KPM ignored) untouched; clear-shell KPM branch untouched; four-family conjunction untouched. `escape_lane` is NOT in `ENCOUNTER_COHORT_KPM_BAND` (smoke asserts this — the F4 exit branch does not leak into clear shells). T1 6-shell pilot bands (step-5/step-6) untouched.
- **Regression re-run by me: PASS.** `test_cycle13_wave5_gauntlet_sim.py` 52/52 (retired the dead-code test, added 3 live-gate tests). The one pre-existing fail `test_run_phase5_cohesion_judge_accepts_path_x_pm1_result_in_smoke` (LLM/P5 seam, PCA-clustering path) is confirmably NOT this seam: the test file imports zero F4/gauntlet_sim symbols (grep count 0), and the F4 constants did not exist at parent `b30c4ae` — gamora's git-stash-verified claim stands.
- **MIGRATION / cross-seam boundary: PASS.** MIGRATION v1.86 is a WITHIN-SEAM discharge of the v1.85 "zero emit until Lane-3 registers F4" contract — it reuses `tier_2_survival_rate` + `tier_2_kpm` (already serialized), no new star-lord schema, `season_emit` stays a bool (only its truth-condition becomes reachable-True). rocket's `season_generation_pipeline.py` reads that bool unchanged (output set can now be non-empty; no break). Correctly NOT an ADR-004 cross-seam schema MIGRATION.
- **KPM-ceiling disposition choice (gamora flagged for Gate-2): ACCEPTED.** The in-line hard upper (`t2_kpm <= hi` → False above) matches the pre-existing clear-shell gate convention; the Rider-3 flag-vs-fail overlay correctly lives in the report-only metrology `_bar_disposition`, not in the gating predicate. Deliberate consistency with the clear shells F4 sits beside, not an omission. No finding.

---

## Action

- [x] Developer (gamora): none required to clear this gate — wiring is correct.
- [ ] Developer (gamora / whoever scores R4): **CONDITION 1** — after R4 produces the first escape_lane distribution, run the geometry-vs-p90 anti-curve-fit cross-check that was UNAVAILABLE here; re-validate 0.80 / [60,150] against it BEFORE R5 band-sheet VALUES are trusted. Falsifiers: viable-kit exit mode <0.80, or KPM mode pinned at 150.
- [x] jack-ryan: decisions-log entries authored (below), F4 registration entry carries the PROVISIONAL-PENDING-FIRST-OBSERVATION stamp.
- [ ] Matt: no decision needed to clear (no BLOCK). The re-check condition is a jack-ryan gate call under ADR-002 (within-seam re-validation), NOT a Matt escalation — flagged here for R5-touchpoint awareness.

## R4 cert sweep

**CLEARED to fire.** The gate that made F4 dead-code (season_emit=0 by construction) is correctly lifted; the certification contract now gates on a real, fail-safe criterion. R4 is the intended first-observation event and its data is what CONDITION 1 re-validates against.

## Decisions-log entries authored (this pass)

Batched, cross-linked, all Status: Active (Matt ruled the substance in this chain; his ruling is the approval basis per the decision-log-format skill):

1. **2026-07-08 — F4 escape_lane cert criterion REGISTERED** (this step; PROVISIONAL-PENDING-FIRST-OBSERVATION on the band).
2. **2026-07-08 — R4 cert-contract shift** (STR boss-shell carve-out RETIRE → four-family conjunction) + **open_arena re-base** + **mobs_killed range relaxation (F4 continuous)** — the three deferred Disc-#12 semantic shifts (run-state :357), authored as one entry (single ratified instrument-build event).
3. **2026-07-08 — §4 acceptance-layer REFRAME** (tier-1 KPM = measurement / tier-2 WR = validity bit; Matt-ruled A) — SEPARATE entry per my prior advice (run-state :1087), with the residual KPM-spread-collapse falsifier captured.
4. **2026-07-08 — Endgame-BC gauntlet un-stacks MOB_HP_DIFFICULTY_MULTIPLIER (Option A) + serial-engagement authorized** — folded in the pending §6 proposal (`qa/pending/2026-07-08-kr-decisions-log-proposal-s6-spatial-difficulty-ruling.md`), with the two parked-workstream Status edits (log 4240 + 5223 → SCOPE-RETIRED reference).

## References

- Math-note: `reincarnated-engine/src/reincarnated/simulation/math/f4-escape-lane-band-registration-2026-07-08.md`
- Code: `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (F4 branch + 3 constants); `spatial_gauntlet/arena.py:1058-1097` (SCENARIO_ESCAPE_LANE); `spatial_gauntlet/spatial_engine.py:2874-2888` (escape win-condition identity)
- Smoke: `reincarnated-engine/src/reincarnated/simulation/scripts/gamora_f4_escape_lane_registration_smoke_2026_07_08.py`
- gamora completion note: `agentic_orchestration/gamora/notes/2026-07-08-f4-escape-lane-band-registration.md`
- Spec: `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` §3-F4
- Decisions-log: `reincarnated-engine/design/decisions/decisions-log.md`
