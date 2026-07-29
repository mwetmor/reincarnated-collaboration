# KIT-CAL-1 hand-off queue — items that outlive the run

**Run:** KC1-2026-07-27 · **Conductor:** gandalf (RUN-CONDUCTOR) · **Authored:** 2026-07-28, post-G-5
**Status of the run at authoring:** G-5 executed clean (NO FLIP → Arm A canonical, charter §14.26);
T-5 band-verdict lap in flight (named gandalf sub-agent); Gate-2 doc conditions C-1..C-5 closure in
flight (gamora). This note is the queue of cross-seam consequences that need routing AFTER the run
terminates — knight-rider sequences; nothing here is a dispatch.

---

## HQ-1 → drax — REPLICA-1 repair changes what your Godot lane has been consuming

**What happened:** at G-5 harness smoke, gamora found `ReplicaFrameSink.on_hit`'s mob→player branch
had **never been called since KF-5** — every replica trace ever emitted showed the player taking zero
damage. Repaired + tested at engine `bef1f55` (charter §14.25).

**Why drax cares:** the Godot auto-battle depiction is the other consumer of `replica-frame/v1`.
Every replica trace drax has rendered to date carried a player HP series that never dropped. Any
Godot-side tuning done against those traces (HP-bar pacing, damage-flash cadence, hit-react timing,
"is this fight legible" judgments) was tuned against a vacuum on the received side.

**Action:** re-emit any replica traces drax's scenes currently reference from engine ≥ `bef1f55`;
re-check hit-react/HP-bar presentation against a trace that actually contains incoming damage.
Bonus: the G-5 traces (`g5-replay-trace/v1`, strict superset of `replica-frame/v1`, paths in
`src/reincarnated/simulation/output/kitcal_g5/g5/kitcal_g5_g5_report.json` per-fight `trace_path`)
are the first traces ever emitted with a real received-side — and per R-KC1-19a the base schema
already carries everything the depiction needs (per-frame `alive/x_m/y_m/heading_rad/hp`, `decision`
aim-line events, `telegraph` events with `damage_amount` for tell-rendering). No live AI ships;
Godot renders, sim thinks.

## HQ-2 → star-lord — `leg3_pilot_section8a1_band_measurement.json` mutates under foreign test runs

**What happened:** `src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json` (star-lord's
seam) was rewritten AGAIN by the G-5 harness test session **despite** `test_w3_emission_driver` being
deselected. Second observed occurrence this run. The file is currently uncommitted-dirty in the
engine working tree — left untouched deliberately so the trigger can be diagnosed from a live
reproduction.

**Action:** find which import-time or fixture-time path writes that file (suspicion: a module-level
or conftest side effect that fires on collection, not on the deselected test itself), and make the
write opt-in. A measurement artifact that rewrites itself when unrelated tests COLLECT is a
provenance leak in an emission seam. Until fixed, no one should trust that file's mtime as evidence.

## HQ-3 → knight-rider — Q-KC1-1 wave charter inputs (the build-class wave)

The run's class line (R-KC1-21): *known-wrong operands get fixed before validation; not-yet-built
mechanics get built in their wave.* This is the wave. Inputs banked and ready:

| Input | Where it lives |
|---|---|
| BQ-1 / BQ-2 / BQ-4 build questions (BQ-4 = crit un-glued seam, ex-P-6) | charter §14.12, §14.14 |
| Leech build-carriers F-1..F-7 (F-2 HoT `tick_effects` scalar conflation; F-4 kernel out-carry would stack with door; F-7 HALTED) | gamora wake note + charter §14.22 |
| Hero-slot scaling finding (A-HP-3: measured 4,702 vs pool semantics) | charter §14.25 |
| Dodge-on-tell / evasion mechanic — **Matt's Primordian WIN is the pre-banked acceptance fixture** (R-KC1-22; observer-effect caveat on death-1 recorded) | charter §14.24 |
| Frigidring / telegraph-burst modeling — **Matt's death-2 is the pre-banked acceptance fixture** on the other side; fidelity-law: model the GD mechanic (CC nova), do NOT reuse RDR `freeze` shatter (Gate-2 H-1) | charter §14.23, §14.26 |
| Freeze-shatter + execute operators: woken but corpus-dormant (nothing emits `freeze`; execute 0 fires) — the wave decides whether content should emit them | wake census, charter §14.22 |
| **Before-baseline dataset:** the full G-5 battery (150 fights, 30 seeds, engine `bef1f55`, Arm A canonical) — any wave build must re-run this battery and diff | `output/kitcal_g5/g5/` |
| Acceptance symmetry (the wave's exit shape): with the nova modeled, the no-evasion sim player must become killable at the fixture's death-2 band; with evasion modeled, the win must become reachable | charter §14.26 |
| T-5 band verdict's join-forward section (which MISSes are wave-inheritance vs current-class calibration deltas) | `2026-07-28-kitcal1-g5-efficacy-verdict.md` (in flight) |

**Non-blocking carried flags:** `arm_a_jitter=false` deviation (flat 5%, measured band 3.25–6.75%);
1.61-vs-1.10 regen-floor UNRESOLVED; galadriel armour re-crop residual (`mitigation_delta` pin);
M10 elrond rider; N-12 NOT-RECUT non-stationarity caveat travels with any future use of that band.

---

*Filed by the conductor as a queue, not a dispatch. KR sequences HQ-1..HQ-3 post-wind-down; HQ-2 is
the only item with an active hazard (a self-rewriting artifact) and should sequence first.*
