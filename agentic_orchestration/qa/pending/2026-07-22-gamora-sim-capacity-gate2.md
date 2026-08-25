# Finding — 2026-07-22 — sim-capacity step-(b) build (Gate-2, DEV-MODE)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (no BLOCK)
**Target:** `gamora/v1.14-sim-capacity-1` @ `e51fbf5` · `-2` @ `a57ee1f` · `-3` @ `620f687` · AGENT_STATE @ `99aaf50`
**Developer:** gamora
**Principles applied:** Principle 1 (math-before-code), Principle 2 (smoke-gate), Principle 6 (cross-seam impact), Principle 4 (decisions-log as truth), Principle 5 (severity)
**Disciplines cited:** #1, #1.1, #2.1, #11, #12, #18, #19.1, #62

## What I found

The build lands the spec-frozen envelope exactly as I cleared it at Gate-1 (A1-enemy + A2/A6 horde + A3 formation; nothing design-gated built). I verified every load-bearing claim first-hand at HEAD (Disc #11), not from the commit prose:

- **Central call — the geometry-only band with deferred pilot cross-check is HONEST, not a masked failure. CLEAR.** (a) The `dense_cell` geometry-only-band precedent is REAL and correctly applied: I read `gauntlet_sim.py:520` — dense_cell ships GEOMETRY-ONLY ("NO dense_cell distribution exists on disk yet (new room); falsifier named in math note §4.3 ... measured at the pilot, NOT curve-fit now"). `scenario_overrun` follows the identical posture with the identical structure (density-anchored KPM = mob_count·60/clear_s, timeout floor, geometry ceiling, falsifier named in refit-note §3). (b) The overrun-30/30 diagnosis is SOUND and independently corroborated: the four-family build smoke ALREADY documents the same fact in tracked source (`_build_smoke_four_family.py:125,142` — "Kit survival ... is a LETHALITY OUTCOME (Lane-3/calibration), NOT a room-build signal"). This is a pre-existing project law, not a rationalization invented for this build. The baseline artifact (`output/sim-capacity-horde-band-baseline-71000301.json`) records the honest 30/30 monster-win with `admits_baseline:false` — the failure is captured, not greened. (c) This is honest substrate-voting-deferral: the band is not asserted as validated; it is declared geometry-anchored with the empirical cross-check explicitly routed to the Lane-3 pilot, seed + artifact cited.
- **Non-shift (Disc #12): CONFIRMED.** The gather-OR reduces to identity — I read the diff: `player_gather_primitive or bool(getattr(scenario, "gather_primitive_default", False))`, and every scenario except overrun is `False`, so the OR is `x or False == x`. `preferred_behavior_override=None` → mob_dict lookup byte-identical. Runtime check confirms 55 mobs, gather True, `all_mobs_killed`, in `ALL_SCENARIOS`, NOT in `FAMILY_SCENARIOS`. `_route_tier_1` predicate untouched (comment-only reference in diff); `_W5G_ELIGIBLE_PASS_FLOOR_EXPECTED == 9` unchanged; only structural assert count 7→8. 107 spatial/gauntlet tests pass == baseline.
- **Principle 6 / MIGRATION: NONE OWED — CONFIRMED.** `scenario_id` is a free-form unconstrained `str` column; `"scenario_overrun"` is a new value, not a new field. No `formation` telemetry field emitted (the one Principle-6-refiring contingency is fenced out by construction). Band constants are sim-side metrology, not fixture fields. No cross-seam field entered.
- **AM-1 provenance (Disc #18): SATISFIED.** The neutral-baseline composition is stated in refit-note §2 BEFORE the refit code; the measurement ran at N=55 (≥50, verified the scenario materializes 55 concurrent), seed 71_000_301, artifact committed. Genuinely a ≥50 measurement, demonstrably not scaled from the 8-concurrent bands (§0 argues the never-carry-a-bar-across-instruments law).
- **#2.1 resource rehearsal: CONFIRMED at ≥50.** Slice-1 smoke runs N=55 (verified mob_count), reports 26.9 ms/fight, 51.2 MB RSS, 0.13 s cohort — matches the #1.1 projection (memory non-binding, wall the constraint, 50 cleared with ~7× headroom; do-not-certify-at-150 respected).
- **Pre-existing-failure honesty: CONFIRMED.** `git diff 4ee8ccb..HEAD` on `season_generation_pipeline.py` is EMPTY — rocket's cell-grain contract (`:1905`, a halt-loud `AssertionError`) is byte-identical pre/post build. I ran the suite: 21 errors, ALL in `TestW5R3SeasonContentAuthoring` (rocket's authoring path), zero in gamora's sim seam. Not introduced by this build.
- **The two deferred follow-ons: LEGITIMATELY DEFERRED, not a scope gap.** (a) The horde-band pilot cross-check → Lane-3 calibration pilot: correct, because no survivable endgame kit distribution exists on disk for this new room (same as dense_cell). (b) The ≥50 defensive-axis re-fit that dispatch §III.3 *expected*: correctly deferred and coupled to the SAME real-kit pilot. gamora touched no incoming-damage constant this slice (verified: production changes are confined to `gauntlet_sim.py` band rows + arena/spatial_engine additive fields). The re-fit criterion is named: "survivable-pilot death-rate at SCENARIO_OVERRUN > 0 under the 2026-06-21 incoming constants." Deferring a defensive re-fit that cannot be run without a survivable pilot — the same pilot that is already deferred — is legitimate scoping, not a swept gap.

## Rationale

The Gate-2 bar is: does the build match the frozen spec, and are the load-bearing claims empirically true rather than asserted (Disc #11)? Both hold. The one item that keeps this from an unqualified PASS is an evidence-artifact gap on the central diagnosis (below), which is an AMENDMENT (a WARN-tier provenance completeness note), not a BLOCK — because the diagnosis is independently corroborated by a pre-existing tracked project law, so the missing artifact does not leave the conclusion unsupported.

**AMENDMENT (WARN — provenance completeness, Disc #19.1):** The load-bearing falsifier that converts "30/30 overrun" from a horde-regime failure into a bad-test-kit property is the viability probe — "vit-200 tanky kit, dm swept 6→20→60 dies at fixed ~3.6 s invariant to damage; count sweep dies at n=8 too." This probe is asserted in three places (refit-note §3, AGENT_STATE, commit `620f687`) but is NOT persisted in any tracked artifact or script. The committed baseline JSON contains only the 30-fight overrun run; no probe script is tracked; the invariance/n=8 numbers exist only in prose. Per Disc #19.1 (cheapest-refuting-test-per-claim must be reproducible), the "invariant-to-damage" and "dies-at-n=8" claims should be reproducible from a committed artifact, not narrated. This does not BLOCK because `_build_smoke_four_family.py:125,142` independently establishes the same lethality-is-calibration law in tracked source — the conclusion stands on that precedent even with the probe unpersisted. But the probe artifact should be committed (or the probe re-run and its output persisted) so the diagnosis is provenance-verifiable end-to-end, matching the AM-1 discipline gamora correctly applied to the band itself.

## Action

- [ ] Developer (gamora): commit the viability-probe artifact (the n=8 count-sweep + dm-sweep 6→20→60 output the diagnosis rests on) alongside the baseline JSON, OR add a one-line note in the refit math-note §3 pointing at where that probe output lives. Empirical criterion to clear: a tracked artifact reproducing "death ~3.6 s invariant to dm; WR 0.00 at n=8." Non-blocking; may land in the next slice/session.
- [ ] Matt: no decision required to clear this Gate-2. Two decisions-log entries are OWED as forward-item captures (below) — jack-ryan will draft; they record posture, they do not gate the tag.

## Decisions-log entries owed (jack-ryan to draft — capture, not gate)

1. **Geometry-only horde-band posture** — `scenario_overrun` band `(28.70, 110.00)` ships GEOMETRY-ONLY with pilot cross-check deferred to Lane-3, per the `dense_cell` precedent. Records that the band is declared-not-canonicalized; the Lane-3 pilot is the canonicalization gate; falsifier named (survivable-pilot win-KPM median must land in-band, ceiling ≥ p90, floor ≤ p10).
2. **≥50 defensive-axis re-fit as named forward item** — the 2026-06-21 ≤8-concurrent defensive close does NOT carry to ≥50 (~6.9× swarm incoming at N=55); re-fit is ROUTED to the same Lane-3 pilot; criterion: survivable-pilot death-rate at SCENARIO_OVERRUN > 0 under the 2026-06-21 incoming constants. No incoming-damage constant was touched this slice.

## References

- Spec: `src/reincarnated/simulation/spec/sim-capacity-extension-spec-2026-07-22.md`
- Math notes: `src/reincarnated/simulation/math/sim-capacity-{resource-bounds,overrun-scenario-gather,formation-topology,horde-kpm-band-refit}-2026-07-22.md`
- Baseline artifact: `output/sim-capacity-horde-band-baseline-71000301.json`
- Precedent (corroborating diagnosis): `src/reincarnated/simulation/spatial_gauntlet/_build_smoke_four_family.py:125,142`
- Precedent (geometry-only band): `src/reincarnated/simulation/gauntlet_sim.py:520` (dense_cell)
- Band + non-shift: `src/reincarnated/simulation/gauntlet_sim.py` (scenario_overrun row; W5G floor `:713`; structural assert `:712`)
- Pre-existing failures: `tests/test_cycle13_wave5_season_generation.py::TestW5R3SeasonContentAuthoring` (21 errors, rocket `season_generation_pipeline.py:1905`, byte-identical pre/post build)
- Completion record: `src/reincarnated/simulation/AGENT_STATE.md` @ `99aaf50`
