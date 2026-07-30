# WR3-KITE-COMMIT — STAGE-1 BUILD REPORT (Mechanism K + Mechanism C2 + the env contract)

**Date:** 2026-07-30 · **Author:** gamora (simulation seam) · **Class:** verdict note
**Commission:** gandalf (RUN-CONDUCTOR), run WR3-KITE-COMMIT, mandate R-WR3-1 (Matt-signed)
**Built against:** `gandalf/notes/2026-07-30-wr3-stage1-mechanism-spec.md`, as AMENDED by charter
`…/2026-07-30-wr3-kite-commit-run-charter.md` §2 **R-WR3-12** + **R-WR3-13**
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr3-kite-commit-stage1-2026-07-30.md`
**Engine commit:** `6de80aab` (branch `main`, NOT pushed — the conductor pushes)
**Computing cell:** `simulation/wr3_cell_kc_2026_07_30.py` · artifact
`simulation/output/kitcal_g5/wr3_cell_kc_statistics.json`

---

## §0 — GATE VERDICT TABLE

> ⚠ **READ THE ARM BANNER FIRST.** The gate numbers below are measured on **11 of 30 seeds
> (74000800–74000810)**, in **both** arms, because **the full 30-seed AFTER battery HALTS** — see
> §F-1. That halt is the one item needing a conductor ruling. Both arms are restricted to the same
> seed window, so every BEFORE/AFTER comparison is like-for-like; but this is a **DIAGNOSTIC ARM,
> NOT the battery of record**, and no row below may be cited as one.

| gate | predicate | BEFORE (n=66 boss) | AFTER (n=66 boss) | verdict |
|---|---|---|---|---|
| **G1(a)** | `median_of(per-fight median sep) ≥ 2.000 + 0.25` | **2.0000** | **2.4709** | **PASS** (+0.471 m) |
| **G1(b)** | `count(per-fight median == 2.000 ± 1e-6) ≤ 90/180` (33/66 here) | **66 / 66** | **0 / 66** | **PASS** — the degenerate signature is GONE |
| **G2** | ≥1 **conceded** kite window in ≥ 90 % of boss fights | **0 / 66 = 0.000** | **60 / 66 = 0.9091** | **PASS** — at the threshold, +0.0091 |
| **G3(a)** | ≥1 firing with `player_max_r_from_origin > 12.0 m` | **0 / 60** | **60 / 114** | **PASS** |
| **G4 · S-1** | `violations == 0` AND `worst_slack ≥ −0.01 m` | 0 / **−0.000989** | 0 / **−0.001091** | **PASS** |
| **G4 · S-7 cl.1** | `assessable == firings` AND `worst_ratio ≤ 1.0` AND the margin identity holds | 60/60 · **0.1493** · 5.55e-17 | 114/114 · **0.7854** · 5.55e-17 | **PASS** |
| **G4 · S-2 (damage substrate)** | anchor grain 207.40 / worst drop unchanged | `{207.4, 235.4, 414.8, 470.8}` | **`{}` — 0 crossings** | **PASS, vacuously** — see §F-2 |
| **G5** | two full batteries, byte-identical | — | **165 / 165 matched, 0 differed** | **PASS** |

**Reported, ungraded (charter R-WR3-12(8.2) + R-WR3-13 F5):**

| column | BEFORE | AFTER | note |
|---|---|---|---|
| `escape_rate` = escaped / firings | **0.000** (0/60) | **0.5263** (60/114) | the two-sided question §8.2 defers to the stage boundary |
| `crossings / firings` (G3b) | **1.000** (60/60) | **0.000** (0/114) | **the nova is now fully NON-DELIVERING** |
| **F5 cadence invariance** | {1.5: 1266, 1.6: 184}, **0 off-grid** | {1.5: 2664, 1.6: 314}, **0 off-grid** | **PASS — no build defect.** 54 nova-spanning intervals classified out (§F-3) |
| S-2 wall-share (spec-conflict row) | 0.0223, corner 0 | 0.0158, corner 18 | K did **not** corner the player; it un-cornered it |
| boss win rate `boss/A` · `boss/B` | 0.333 · 0.364 | **1.000 · 1.000** | **§8.3's prediction is FALSIFIED — see §F-4** |
| mean boss fight duration | 36.2 s · 44.6 s | **82.2 s · 82.2 s** | GD referent band is 59–118 s |

**HALT RULES:** **G4 PASS, G5 PASS** — no build defect, no HALT. G1/G2/G3 all PASS, so the
pre-registered [CAL] sweep does not arise. **The pre-registered CAL sweep was NOT fired.**

**Five findings need a conductor ruling or a stage-2 hand-off: §F-1 … §F-5.**

---

## §1 — WHAT WAS BUILT

### 1.1 Mechanism K — `kite_policy_v1`, default OFF

- **K-T1 is an ARMING change, and no new evade math was written.** The flag constructs
  `PilotedCompetence()` at its declared defaults (`reaction_latency_s = CAL-K1 = 0.30`) when the
  caller passed none; an explicitly-passed instance still wins, so the R-WR2-21 paired M-3 arms keep
  their own sweep values. Rewriting the M-3 payload scorer would have been a second implementation
  of a payload law — the exact defect R-M3-1 exists to prevent.
- **K-T2 is new.** `KiteInput` (frozen, pure values, no engine handle) + `kite_claims_tick` in
  `policy/seam.py`; the step vector in `policy/kite.py` (3 headings × 8 deterministic samples + the
  `C_reach + ε` shelf point, pack filter, clamp-then-re-verify, argmax with ties keeping the
  incumbent). Zero RNG.
- **The delayed-observation buffer applies latency EXACTLY ONCE.** K-T1 keeps its internal
  `− reaction_latency_s` and reads the LIVE ring; K-T2 and the §4 observation contract read the
  buffer and subtract nothing. `REACTION_LATENCY_S = 0.0` reproduces the clairvoyant ceiling arm.
- **Evade costs the action slot** (`_m3_evaded_this_tick`), exactly as K-T1's does.

### 1.2 Mechanism C2 — `boss_commit_v1`, default OFF

- A mob-side consumer of the existing E4 commitment pattern. **Boss tier only, melee packet only**
  (R-WR3-13 F4 — the nova cast stays UNCOMMITTED).
- **T_lock realizes as exactly 6 locked ticks with the strike inside:** windup 3 (0.30 s) → strike 1
  (0.10 s) → recovery 2 (0.20 s). The state machine is tick-counted, not float-deadlined; the math
  note §1.2 derives the timeline from the transition rule and the engine reproduces it. Measured
  post-build: `c2_telegraph_lead_mismatch == 0` over every fight run in this build.
- **C2-L1 (live-geometry whiff) and C2-L2 (no re-aim)** both land. The lock is a per-tick scalar at
  the `_navigate_entity` read site; **`entity.movement_speed` is never written**, and G4's S-7 row
  confirms the consequence: `distinct_movement_speed_ms == [5.75]` in both arms.
- **F3:** the fixture packet writes `wind_up_s = 0.30`, and the telegraph is minted at **windup
  entry** with `fire_tick` = the realized strike tick. Because C2-L2 freezes position *and* heading,
  the mint's origin equals the origin at the strike by construction.
- **C2 adds no RNG draw.** The single `gd_swing_pause` draw per swing moves to initiation, so a
  whiffed swing still pays its cadence. F5 confirms.

### 1.3 The env contract

`spatial_gauntlet/env_contract.py`: frozen 23-slot `OBS_INDEX`, `build_obs` (the engine's ONLY Obs
producer — one implementation), `DelayedObservationBuffer`, the frozen `Discrete(4)` table
unit-tested against `list(MovementIntent)`, `reward_stub() == 0.0`, exact `reset`/`step` signatures.
**Zero RL imports at module scope** — asserted by an AST test, not promised. The battery hot path
never imports the module.

### 1.4 Measured mechanism evidence (66 boss fights, 11 seeds × 3 legs × 2 arms)

| counter | value |
|---|---|
| C2 initiations | **3,098** |
| C2 strikes that LANDED | **136** |
| C2 strikes that WHIFFED (C2-L1) | **2,960** — **95.55 %** |
| `c2_telegraph_lead_mismatch` (H-6 falsifier) | **0** |
| K evade ticks | **20,376** |
| K kite bouts | **3,168** |
| boss committed-tick share | **0.399** — the predicted `duty_ABS = 0.400` |

The duty-cycle pre-build measurement predicted 40.0 % cooldown-absorbing duty at T_lock 0.60. The
realized boss committed-tick share is **0.3992**. The arithmetic survived contact.

---

## §2 — SEMANTIC SHIFTS LANDED (Discipline #12)

| id | shift | disposition |
|---|---|---|
| **SS-K-1** | `MovementIntent.EVADE` acquires a SECOND producer. The decision record now carries a limb discriminator: `evade:tg` (K-T1) / `evade:commit` (K-T2a) / `evade:pressure` (K-T2b). **The bare `"evade"` is emitted ONLY when the arm is OFF**, so every WR2 instrument reading the frozen BEFORE root — including the S-7 clause-2 crossing instrument, whose comment says *"`evade` is UNIQUE to the M-3 limb"* — sees exactly the string it has always seen. **Consumer obligation:** a reader of a WR3-armed trace must match the `evade:` PREFIX. `env_contract.action_of_intent_str` already does. | LANDED, tested both directions |
| **SS-C2-1** | `Commitment` gains `recovery_s`, parsed with the same `.get` read every other field uses. A packet without it parses to `0.0` — byte-identical for every existing player-side consumer. | LANDED, additive + default-inert. **The emitter-side MIGRATION question is rocket's/knight-rider's per R-WR3-12(8.5) and is still OPEN — it must be dispositioned before jack-ryan's Gate 2.** |
| **SC-K-1** | `KiteInput` gains `bout_limb ∈ {"", "commit", "pressure"}`. Spec §2.6's field list omits it, but spec §2.4's yield condition 3 is explicitly *"(K-T2a only)"* — and a level-triggered pure predicate cannot tell a pressure bout under an idle boss from an ended commit bout without it. **Without the field K-T2b is deleted** (a 2-tick valve). Pinned by a test in both directions. | LANDED as a **spec completion**, reported not ruled — §F-5 |
| **BS-1** | Stage-1 `SpatialFightEnv.step` is **REPLAY-BACKED**: signatures, frozen Obs order, frozen action mapping, termination semantics and the reward stub are exact and live; the action is validated and recorded but does not steer the sim (`info["action_steers"] is False`). | LANDED as a **build-scope declaration**, reported not ruled — §F-5 |

**No `MIGRATION.md` entry is owed for stage 1**: the replica-frame schema is untouched (G2's
commit-attribution join reads `commit_state`, which the emitter already writes on every per-frame
entity block), and `SpatialFightResult` gains no field. The `run_spatial_fight` result dict gains
WR3 keys **only when the arms are set** — the same conditional shape B/C/D already use.

---

## §3 — TESTS AND SUITE STATE

| item | value |
|---|---|
| New unit tests | **3,523** in `tests/test_wr3_kite_commit_stage1.py`, all passing (1.3 s) |
| §2.6 grid-equivalence | **3,456 cells** — the full cross product `{commit_state} × {telegraph_live} × {in_bout} × {pressure} × {bout_elapsed} × {move_scale 0,>0} × {separation} × {bout_limb}` — declared law vs an **independently written** transcription of the spec prose, **and** vs the classifier's own EVADE claim |
| §4.3 action-mapping pin | `list(ACTION_TO_INTENT) == list(MovementIntent)`, plus per-index literals and decode round-trip |
| Full regression BEFORE build | 81 pre-existing failures (banked baseline) |
| Full regression AFTER build | **82** — 81 baseline + `test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported` |
| That 82nd | **The guard doing its job**, on this build's own new modules. It PASSES once they are tracked (verified). **ZERO NEW FAILURES.** |

Cheap-suite-first was honoured: the suite ran before the battery and the two never ran concurrently.

---

## §4 — BATTERY STATS

| arm | root | legs | traces | wall |
|---|---|---|---|---|
| BEFORE (frozen, **never regenerated**) | `output/kitcal_g5/wr2_battery_after/` | 3 | 450 (180 boss) | — |
| identity assertion | I1 rolled digest over all 180 boss traces | — | — | **`b5ce25e6…4345e3e` — MATCHES the banked value**, per-leg `e8dc6336…` / `b4a6766d…` / `935adfc3…` |
| AFTER, full 30-seed | `output/kitcal_g5/wr3_battery_after_HALTED_EVIDENCE/` | **1 partial** | 113 (23 boss) | 2.4 s → **HALT** |
| AFTER, 11-seed diagnostic | `output/kitcal_g5/wr3_battery_after_s11/` | 3 | 165 (66 boss) | 1.9 s/leg |
| G5 replicate | `output/kitcal_g5/wr3_battery_after_s11_det/` | 3 | 165 | 1.9 s/leg |

Argv is Cell BAT's ARMED argv character for character, plus `--kite-policy-v1 --boss-commit-v1`.
The two batteries differ in exactly the two mechanism flags. Legs ran sequentially (Discipline #3).

---

## §5 — FINDINGS

### F-1 — **THE FULL BATTERY HALTS. THIS IS THE RULING THE RUN NEEDS.**

The 30-seed AFTER battery refuses at **seed 74000811, arms A and B, in all three legs — 6 of 180
boss fights**, deterministically:

> `A-DMG-1: a single received event of 290.36 PER PROJECTILE exceeds the measured post-mitigation
> ceiling 260.5 … The boss damage regime is HELD; this falsifies it.`

**Mechanism, measured not inferred.** At that seed the nova crossing moves:

| | BEFORE | AFTER |
|---|---|---|
| crossing radius `r*` | **4.687 m** | **11.178 m** |
| realized spoke count | 2 | 1 |
| delivered per projectile | **207.40** (≤ 260.5 ✓) | **290.36** (> 260.5 ✗) |

The nova's per-spoke delivered payload **steps from 207.40 to 290.36 at r ≈ 10 m** (verified
directly against `gd_nova.nova_delivered` at the R2_proxy armour): fewer spokes cover a point at
larger radius, each spoke's RAW is larger, and M-1's piecewise armour operator
`taken = d − 0.70·min(d, A)` absorbs a smaller FRACTION of a larger hit. The M-3 limb minimises
EXPECTED TOTAL delivered and is therefore correct to go there — total falls, per-projectile rises.

**This is not a K or C2 build defect.** K's step is bounded by one tick's budget, there is no
teleport, and no nova number was touched. It is the fixture's own HELD boss-damage regime (HALT-1)
being falsified at a coordinate the pinned player could never reach, by a falsification pin doing
exactly what it was written to do. It **corroborates charter §3's already-known out-of-band row**
(*"nova up to 55 % of pool — 1.6–3.4× OVER — the outlier"*) from a new direction.

**Every available disposition lies outside my authority**, so I have taken none:
(a) rule that A-DMG-1's per-projectile ceiling does not govern the WR3 arm and re-fire the 30-seed
battery; (b) fire stage-2's CAL-1 nova reduction early — but spec §7 says **DO NOT TOUCH ANY NOVA
NUMBER IN STAGE 1**; (c) accept the 11-seed diagnostic as the stage-1 evidence.
**Routed to the conductor.**

### F-2 — **THE NOVA IS NOW INERT: 0 of 114 rings deliver.** (The §8.2 two-sided worry, FIRING.)

`crossings / firings` goes **1.00 → 0.00**. `escape_rate` goes **0.00 → 0.526**; the other 54
firings neither escaped the 12 m footprint nor delivered — the conflation the S-7 clause-2 caveat
names, carried verbatim. Consequence: the G4 S-2 damage-substrate row passes **vacuously** —
`{207.4, 235.4, 414.8, 470.8}` → `{}` — because no crossing exists to carry a grain, not because
the payload law moved. (The law is provably untouched: no nova constant is read or written by this
build, and the frozen BEFORE arm reproduces its banked grains exactly.)

Spec §8.2 predicted this precisely: *"a player who escapes 132/132 has made the nova inert, which
collides directly with stage 2's CAL-1 nova calibration — you cannot calibrate a heavy the player
never eats."* **The two-sided band the conductor deferred to the stage boundary is now the live
question.** Note the direction is not uniform: the nova is inert on 11 of 12 seeds and
*over*-lethal on the twelfth (F-1). Both facts are about the same outer-band payload step.

### F-3 — F5's off-grid intervals were the NOVA'S ACTION GATE, not a cadence change

The first F5 pass showed off-grid intervals at **7.5 s (42) and 7.7 s (12)** = `1.5/1.7 + 6.0`, the
nova's action-gate blackhole. On the frozen BEFORE arm this class is **empty** — the single nova is
cast at t = 0.700 and the first swing lands at t = 6.800, so the blackhole falls entirely before the
swing train (σ = 0 over 180 fights, duty-cycle note §3.3). Under K+C2 the fights run long enough for
the boss to **re-cast**, so the class becomes non-empty for the first time. Classifying it out is
the duty-cycle instrument's own convention (assumption A3), not a tune-around: an interval in which
the boss spent its action on the ring does not measure the swing cadence. With 54 such intervals
classified out, **{1.5: 2664, 1.6: 314}, zero off-grid — F5 PASSES and C2 changed no cadence.**

### F-4 — **§8.3's PREDICTION IS FALSIFIED. The boss win rate goes 0.33/0.36 → 1.00/1.00.**

R-WR3-12(8.3) CONFIRMED the reading that *"stage-1 boss win rate is predicted to FALL or hold at
0.00 — K costs uptime."* Measured on the 11-seed arm, the player wins **66 of 66** boss fights
(BEFORE: 22 of 66). Mean boss fight duration 36–45 s → **82.2 s**, which lands inside the GD
referent's 59–118 s band.

The mechanism is legible: the boss lands **4.45 %** of its melee swings (136 of 3,098) and **0 %**
of its novas. K's uptime cost is real and is simply dominated. **This is the "broken-easy" direction
§8.6 named as *"the more expensive failure, because it is the one that does not announce itself"* —
except it announced itself loudly.** It does not fail a stage-1 gate (the stage-1 gates are geometry
gates, correctly), but **the owner-eye checkpoint brief carries §8.3's sentence ABOVE the render
link**, and that sentence is now wrong in the opposite direction. It needs correcting before Matt
watches, or the watch is read against a prediction the build refutes.

Two sub-facts the conductor should hold together with it: the 95.55 % whiff rate sits far above the
"prove the geometry exists" band a stage-1 initial value is supposed to produce, and **`bout_max` /
`release_m` / `pressure_threshold` are all stage-2-owned [CAL] rows** whose current values were
chosen for defensibility, not for correctness. This is a calibration question, not a build defect —
routed as such.

### F-5 — Two named deviations from the spec text, both reported rather than ruled

- **SC-K-1** (`KiteInput.bout_limb`): spec §2.6's field list cannot implement spec §2.4's yield
  condition 3. Added as one pure string field; without it K-T2b is a 2-tick valve.
- **BS-1** (replay-backed `step`): the engine's `run()` has no per-tick entry point, and extracting
  one is a hot-path refactor that G4/G5 — the two BLOCK gates — are the worst place to attempt, for
  an adapter spec §7 fences out. The contract half is exact and live; the steering half is the
  declared stage-2 prerequisite.
- **Spec-internal conflict, reported:** spec §5's G4 row gives the S-2 *predicate* as *"anchor grain
  207.40 / worst_drop_abs 414.80 unchanged"* while naming `CC.s2_scan_battery` as its *computing
  cell* — but that function computes the WR2 Cell-C **wall-share**, a different statistic. The cell
  computes **both**, grades the predicate column's one, and reports the wall-share beside it. (For
  the record, the wall-share **improved**: 0.0223 → 0.0158.)

---

## §6 — DEFECT FOUND BY A SMOKE RATHER THAN ASSUMED (Discipline #11)

**`SpatialEntity` carries no `is_boss` field.** C2's tier scope was first written as
`getattr(mob, "is_boss", False)` — an entity-side read that returns `False` forever. The mechanism
would have armed, run, and initiated **zero** commits, with every counter reading a clean `0`, no
exception anywhere, and a battery that looked like it had measured something. The first ablation
smoke caught it (`c2_initiations: 0` against `k_evade_ticks: 127`). The boss declaration lives on
`SpawnSpec.is_boss` / `.threat_tier`, and `mobs` is index-aligned with `scenario.mob_spawns` at the
single construction site, so C2's scope now resolves once, at construction, into a frozen id set —
which also keeps the value-compared `SpatialEntity` dataclass free of a new field.

**A second, same-family catch:** the cell's I1 identity assertion failed at first because the
duty-cycle instrument rolls its digest in `sorted(LEGS)` **key** order (post, pre, pre_endpoint),
not `LEGS`-tuple order. A rolled digest is order-sensitive, so the wrong order is a total mismatch
that *accuses the evidence*. Reproduced from the instrument's source, not reasoned about.

---

## §7 — REPRODUCTION

```bash
cd ~/Games/reincarnated-engine
python3 -m pytest tests/test_wr3_kite_commit_stage1.py -q -p no:randomly     # 3,523 pass
python3 -c "from reincarnated.simulation import wr3_cell_kc_2026_07_30 as KC; KC.main()" --run-after
```

The cell asserts the frozen BEFORE root's identity before reading a single number and refuses on
mismatch. It writes only to `wr3_battery_after*` roots; `_assert_not_banked` refuses any path inside
a frozen evidence root. Nothing in this build wrote to `wr2_battery_after/`.

---

*WR3-KITE-COMMIT stage-1 build report — gamora, simulation seam, 2026-07-30. Engine committed at
`6de80aab`; neither repo pushed.*
