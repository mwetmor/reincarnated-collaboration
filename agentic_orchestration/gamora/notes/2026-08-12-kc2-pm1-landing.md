# KC2-PM1 — landing note: the player moves while channeling

> **Cell:** KC2-PM1 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Author:** gamora (simulation seam)
> **Date:** 2026-08-12 · **Ledger:** `agentic_orchestration/gandalf/notes/2026-08-12-kc2-pm1-run-ledger.md`
> **Math note (Discipline #1, written BEFORE the code):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm1-player-movement-policy-2026-08-12.md`
> **Status:** COMPLETE — sibling baton emitted, gate wall 66/66 at FULL, determinism ×2 EXACT.

---

## 0 — The one-paragraph answer

The player moves now. `PlayerPolicy.DRIVE_TO_PACK` drives the channeling player at full base speed
(5.4 m/s) at the boss-weighted densest live cluster, straight **through** it, re-targeting about
once a second under a hysteresis that blocked **64 of 80** candidate switches. A sibling baton
exists — `kc2-baton-v1-E-s09-cp150-pm1-20260812_230313.json` @ `4585eeb8…` — through the **same**
66-gate wall at **FULL** grade, from a committed tree. The frozen baseline was verified from bytes
and never opened for writing. **And my own pre-registered prediction is falsified:** the run got
*longer*, not shorter (+2.3% ticks), and the per-wave sign tracks board density at r = −0.575.
That mechanism is § 5.

---

## 1 — What landed

| # | artifact | where | digest |
|---|---|---|---|
| 1 | **movement policy** | `simulation/kc2/player_drive.py` | commit `aa9bd263` |
| 2 | **new policy limb** | `simulation/kc2/locomotion.py` — `PlayerPolicy.DRIVE_TO_PACK` | `aa9bd263` |
| 3 | **tick-loop wiring + `player_start_xy`** | `simulation/kc2/run.py` | `aa9bd263` |
| 4 | **math note** (+ § I, added before the code that discharges it) | `simulation/math/kc2-pm1-player-movement-policy-2026-08-12.md` | `aa9bd263` |
| 5 | **drive replay + assert wall** | `simulation/scripts/gamora_kc2_pm1_drive_2026_08_12.py` | `aa9bd263` |
| 6 | **F5-E knots supply** | `simulation/output/kc2-pm1-actor-paths-E-s09-cp150-pm1-20260812_225655.json` | `bf87afd476df03e811f63aef2131e2d0c33d4ad91925b3a7bd80ca8931c48c23` |
| 7 | **export amendment + 2 MIGRATION entries** | `export/kc2_run_adapter.py`, `export/kc2_baton_emit.py`, `export/MIGRATION.md`, `simulation/MIGRATION.md` | `306fec08` |
| 8 | **★ THE SIBLING BATON** | `output/kc2-baton-v1-E-s09-cp150-pm1-20260812_230313.json` | `4585eeb8f98966e4511690060fadc3b7cea772b3b6438ac69e9cb042f9fec971` |
| 9 | **findings instrument** | `simulation/scripts/gamora_kc2_pm1_findings_2026_08_12.py` | `edaf44de` |
| 10 | **findings artifact** | `simulation/output/kc2-pm1-findings-2026-08-12.json` | `652b9ea5fdefeb4e02b12fb7cdee8605c52b8f0b7b3d0c8ad1eb3613c821cc15` |

**The frozen baseline** `kc2-baton-v1-E-s09-cp150-20260809_052836.json` @
`d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` was **verified from bytes** at
the top of the drive driver and again at the top of the findings instrument (GL-6), read
read-only, and **never written**. Its emission path is byte-identical: `E_S09_CP150` is literally
unchanged in the adapter and `test_kc2_run_adapter.py` (40 tests) passes unmodified.

---

## 2 — EMISSION RECEIPT (deliverable C)

### 2.1 Declared constants — every policy parameter, named

| constant | value | basis |
|---|---|---|
| `move_speed_fraction` | **1.0** | **R-PM1-1**, the ruling, as one named module constant |
| `player_speed_m_per_s` | **5.4** | `v_ref 4.0 × playerRunSpeedCapMax 1.35 × 1.0`. ⚑ **NOT no-wire-basis** — both factors are the sim's existing DB-cited constants (`fixture.V_REF_M_PER_S`, `locomotion.PLAYER_RUN_SPEED_MULTIPLIER`) and are the **same pair** the retired `CAMP_THEN_COLLECT` collect-branch already used. This lap introduces **no new speed number**, only a fraction pinned at unity |
| per-tick step | **0.440816 m** | `5.4 × 0.081633` (the run's own 12.25 ticks/s clock) |
| `cluster_radius_m` (R) | **8.0** | **IMPORTED** from `wave_engine.PLACEMENT_EXTENTS_M` — the half-width of the box the sim itself scatters each body into. "One spawn point's worth of bodies" by construction; a future change to the scatter moves the cluster with it |
| `boss_weight_beta` (β) | **3.0** | anchored to a **census, not an outcome**: this run rolls 70 boss-class / 274 other bodies; `70(1+β) = 274 ⇒ β = 2.914…`, declared 3.0. One boss = four trash bodies, so Matt's two clauses carry comparable mass |
| boss-class definition | `pool_kind == "BOSS"` **OR** record contains `/enemies/nemesis/` | ⚑ **NOT `is_champion`** — measured on the frozen baseline, `is_champion` is TRUE on exactly the 63 `hero`-tier bodies and FALSE on all 59 `boss` + 11 `nemesis`. It would have weighted the wrong population |
| objective | `S(i) = Σ_{‖x_j−x_i‖ ≤ R} (1 + β·boss(j))`, argmax over anchors, ties → **lowest `actor_id`** | R-PM1-3 rider (a): Matt's sentence, in one sum |
| aim point | member **centroid** of the chosen cluster | the anchor selects; the centroid aims |
| `retarget_cadence_ticks` | **12** (0.9796 s) | largest integer tick count strictly under one second on this run's clock — *the player re-reads the board about once a second*. One window = 5.29 m < R, so a leg never crosses a cluster-width unread |
| forced re-target | incumbent anchor dead **or** cluster empty | driving at a ghost is not a policy |
| `hysteresis_margin` (m) | **0.25** | a switch must buy ≥ 1 whole body at the small end: `m = 0.25` clears one body whenever `S_inc ≤ 4` |
| `hysteresis_cooldown_ticks` (C) | **24** (1.959 s = **10.58 m** of committed travel) | `C = 2N`, and 10.58 m **exceeds** the 8.0 m cluster radius — every switch carries the player a full cluster-width before it can be reconsidered. **This is what makes a switch cost something** (R-PM1-3 rider (b)) |
| switch rule | `S_best > (1+m)·S_inc` **AND** `ticks_since_switch ≥ C`; an **invalid** incumbent bypasses both | |
| `pass_through_lock_m` (L) | **3.0** | **IMPORTED** from the EoR disc radius. Inside it the centroid is already inside the damage predicate, so homing precision buys nothing — and unlocked homing with an unclamped step produces a **0.44 m / 2-tick (6 Hz) tremor** parked on the centroid, which is the drunk-walk jitter rider (b) forbids, arriving through the *steering* term instead of through flapping |
| step clamp | **NONE** — never `min(step, dist)` | clamping is stop-at-target; **R-PM1-2 forbids it** |
| `empty_target_policy` | **HOLD** — no move, heading lock cleared, incumbent cleared | **R-PM1-5**. The live set is `alive ∧ spawn_t_s ≤ t` — exactly what the sim already computes as `on_board`. **No spawn schedule is readable from this module** |
| `player_sane_bound_m` | **80.0** | DERIVED: max measured spawn radius 45.06 m + lock 3.0 m + one step, far below the DB pursuit leash 125 m. A firing bound means the policy ran away, not that the bound was tight |
| RNG draws / clock reads | **0 / 0** | the policy's whole input is `(tick, player_xy, live set)` |
| iteration order | caller supplies live bodies **sorted by `actor_id`**; argmax tie-break lowest `actor_id` | a dict-iteration dependence here is a determinism defect that only appears on someone else's Python |
| policy state scope | **PER WAVE** — incumbent, heading lock, cooldown all reset at a wave boundary | position is a property of the **body**; target loyalty is a property of the **board**, and only one survives a dead cluster |

### 2.2 Schema delta — NAMED

**Naming family retained: `kc2-baton-v1`.** No field was added, removed or retyped; no schema
version moved. The structure is unchanged, so the family is correct.

**But the delta is a SEMANTIC SHIFT (Discipline #12), and that is a different sentence.**
`tracks.player_path.x/y` — and `tracks.circle_sweep.centre_x/centre_y`, which are the *same pair of
numbers* by AC-11.7c — were the constant **(0, 0) on all 3,732 baseline ticks** and now **vary**. A
structural diff sees **nothing at all**. A consumer that cached *"the player is at the origin"*, or
that read `config.arena.player_spawn` as a **standing** position rather than a **start** position,
holds a stale **BELIEF** rather than a stale number.

It is declared **on the wire**, not only in a doc — `provenance.informative_rows` carries three
`class: DECLARATION` rows, on PM1 batons only:

| id | says |
|---|---|
| `PM1-PLAYER-PATH-IS-A-TRAJECTORY` | the constant became a trajectory; `player_spawn` is now a START position; **`heading_rad` stays DECLARED-NON-SEMANTIC** (F5-F := ZERO, Law 4 honoured — the body performs the channel, travel direction is derivable from consecutive path samples, and deriving it on the wire would emit a convention that reads as a measurement) |
| `PM1-ACTOR-PATH-KNOT-DENSITY` | **1,003 → 15,793 knots (×15.7)**. The knot PREDICATE is unchanged (R-L82-1, every velocity vertex); the **path** changed, because a pursuing body now chases a moving point and bends on essentially every pursuit tick. A **size** consequence of an honest recorder — buffer sizing off the baseline is the thing to re-check |
| `PM1-WAVE-BOUNDARY-POSITION-CARRY` | the path is **continuous across all twenty waves**; a consumer may interpolate straight through a boundary |

Also filed: `export/MIGRATION.md [2026-08-12]` (ADR-004, **flagged for star-lord**) and
`simulation/MIGRATION.md [2026-08-12]`.

### 2.3 Determinism ×2 — digests and mask

Two **FULL-grade** emissions from one committed tree, back to back, neither landing in the repo:

```
raw bytes      A  f7f973faef5fccdd67f5553bca5a61c6c4ba0aea1a809bb7fedd5bf3cc19614a
               B  0e6acbc3ffb1424296d146e6be385c3a26556ca4b7f452be0d526c89767db73a
unmasked diffs 2  ._emitted_at            '2026-08-12T23:08:44Z' vs '…:45Z'
                  .baton_run_id           two UUIDs
MASK           ['_emitted_at', 'baton_run_id']
                  = baton_v1_emitter.PROVENANCE_VOLATILE_KEYS, the emitter's OWN declared
                    carve-out — IMPORTED by the instrument, not restated
masked digest  A == B == 967b039ab78cf1f3486cbde31c5fae2744719ecf8314ae83f48129898cf4522c
VERDICT        EXACT — 0 differences
```

**Sim-layer determinism** (the replay itself, run twice, full emitted surface deep-compared):
**EXACT**, 116,315 leaves, 0 differences; knots digest `747d1a48…` both runs.

**And the baton of record is tied to that pair.** `4585eeb8…` is payload-**identical** to both,
differing in exactly `sim_pin.engine_version_sha` (`306fec08` vs `edaf44d` — a **true provenance
difference**: the record was emitted from the commit that produced it, the pair from a later commit
that added the findings instrument) and the untracked-file count. Under a mask covering those
provenance stamps, **all three digest `e0a76b0dc2549d49083c725a023b0ef4` identically.**

> ### ⚑ A third volatile field, found by running the ×2 — declared, not masked quietly
> `sim_pin.tree_state_untracked_entries_excluded` is a count of **untracked files on the host** at
> emission time, not a simulated quantity. An emission that lands in `output/` — which is *exactly*
> the `code-surface-v2` exclusion set — **increments it by one**, so emission A can move a field
> emission B reads simply by existing. My first ×2 attempt failed on it. Rather than widen the mask
> and move on, the instrument reports **two** masks and the pair was re-run without perturbing the
> tree: the **tight** mask (the emitter's own two keys, nothing added) then suffices at 0
> differences — which *proves* the extended mask hides nothing instead of asserting it.
> **Flagged for star-lord:** a host-filesystem count on a provenance surface is a real, if small,
> reproducibility hazard for anyone diffing two batons.

---

## 3 — Assert wall (math note § F, deliverable A)

All six green, measured on the **emitted surface** rather than on the policy's own bookkeeping —
checking the policy's counters would be asking the accused to testify.

| check | result |
|---|---|
| 1 · `move_speed_fraction == 1.0` | PASS (5.4 m/s) |
| 2 · every player position finite | PASS — 3,817 samples, 0 non-finite |
| 3 · inside the declared sane bound | PASS — max 27.004 m vs the 80.0 m bound |
| 4 · per-tick travel is **exactly** 0 or one full step (1e-12) | PASS — 3,259 full / 558 zero / **0 partial**. A partial step is how a clamp creeps back in |
| 5 · `channel_active` TRUE on every sample | PASS — 3,817/3,817 (R-PM1-4 fold rider: no stop-spin-to-run) |
| 5b · `circle_sweep` centre == `player_path` | PASS — 0 mismatches (AC-11.7c asserted at the **source**, where it can be attributed) |
| 6 · knot machinery consistency | PASS — 344 actors, 0 structural violations, 0 actors without knots, worst polyline-vs-sim length error 0.0 m |

Plus the emitter's own wall on the moving player: **66/66 green**, including
`AC-2.1-RECHECK` (1,132 damage rows re-tested against a *moving* `circle_sweep`, **0 outside the
disc**) and `R-LOCO-1-HITTEST` (**28,454** `(actor, tick)` pairs re-decided from path × sweep, **0**
inside-without-a-row and **0** row-outside). The trajectory and the damage are one object.

`tests/test_kc2_{locomotion,run_surfaces,actor_path_knots,channel_disc,s1_ramp}`: **141 passed**.
`tests/test_kc2_run_adapter`: **40 passed, unmodified**. (Engine full-suite red tree is the known
non-gating baseline per cell law 7; nothing here touches it.)

---

## 4 — COMPARATIVE FINDINGS, run-level (deliverable D)

R-PM1-4: comparison is **run-level, never tick-by-tick**. The board is rolled identically (the RNG
is consumed entirely before the tick loop), then the first body that dies on a different tick makes
every later tick a different question.

### 4.1 Run level

| | BASELINE (camp) | PM1 (drive) | Δ | Δ% |
|---|---:|---:|---:|---:|
| total ticks | 3,732 | **3,817** | +85 | **+2.3%** |
| run duration (s) | 304.653 | 311.592 | +6.939 | +2.3% |
| event rows | 1,900 | 1,900 | 0 | 0.0% |
| damage rows | 1,132 | 1,132 | 0 | 0.0% |
| actors killed / waves cleared | 344 / 20 | 344 / 20 | 0 | 0.0% |
| channel-active ticks | 3,732 | 3,817 | +85 | +2.3% |
| **path knots** | 1,003 | **15,793** | +14,790 | **+1,474%** |
| end reason | `arena_tier_exhausted` | `arena_tier_exhausted` | — | — |

*(Event and damage row counts are identical because the kill term one-shots most bodies on disc
entry — the player still lands the same 1,132 hits on the same 344 bodies; only **when and where**
moved.)*

### 4.2 Kill curve (ticks from run start)

| quartile | BASELINE | PM1 | Δ | Δ% |
|---|---:|---:|---:|---:|
| 25 % of kills | 813 | 833 | +20 | +2.5% |
| 50 % | 1,373 | 1,405 | +32 | +2.3% |
| 75 % | 2,520 | 2,551 | +31 | +1.2% |
| 100 % | 3,732 | 3,817 | +85 | +2.3% |

The curve is displaced **uniformly**, not bent — the drive policy does not front-load or back-load
the clear, it shifts the whole schedule.

### 4.3 Player path

| | BASELINE | PM1 |
|---|---:|---:|
| path length (m) | **0.000** | **1,436.192** |
| bounding box | x[0, 0] y[0, 0] | **x[−26.243, 20.082] y[−19.853, 17.438]** |
| bbox w × h (m) | 0 × 0 | **46.325 × 37.291** |
| max distance from camp (m) | 0.000 | **27.004** |
| distinct positions | **1** | **3,093** |

1,436 m over 311.6 s = **4.61 m/s average** against a 5.4 m/s cap — the player is moving on
**3,259 of 3,817** ticks (85.4%) and holding on 558 (14.6%), *all* of which are R-PM1-5
empty-board holds between a clear and the next spawn drip. `n_hold_no_heading` = **0**: the policy
never once failed to find a direction it was entitled to.

### 4.4 Wave pacing — and the mechanism

| wave | bodies | BASE | PM1 | Δ | Δ% |
|---:|---:|---:|---:|---:|---:|
| 170 | 4 | 174 | 227 | **+53** | **+30.5%** |
| 160 | 5 | 189 | 235 | +46 | +24.3% |
| 165 | 6 | 200 | 229 | +29 | +14.5% |
| 159 | 9 | 108 | 107 | −1 | −0.9% |
| 169 | 9 | 131 | 120 | −11 | −8.4% |
| 154 | 13 | 169 | 214 | +45 | +26.6% |
| 162 | 15 | 203 | 203 | 0 | 0.0% |
| 164 | 15 | 119 | 119 | 0 | 0.0% |
| 152 | 18 | 143 | 140 | −3 | −2.1% |
| 155 | 18 | 114 | 114 | 0 | 0.0% |
| 163 | 18 | 189 | 166 | −23 | −12.2% |
| 156 | 19 | 279 | 273 | −6 | −2.2% |
| 166 | 19 | 283 | 276 | −7 | −2.5% |
| 161 | 20 | 241 | 243 | +2 | +0.8% |
| 157 | 21 | 129 | 133 | +4 | +3.1% |
| 153 | 24 | 195 | 198 | +3 | +1.5% |
| 167 | 24 | 309 | 306 | −3 | −1.0% |
| 168 | 26 | 187 | 152 | **−35** | **−18.7%** |
| 151 | 28 | 225 | 213 | −12 | −5.3% |
| 158 | 33 | 125 | 129 | +4 | +3.2% |

**Sorted by body count, the sign is a signal, not noise.**

| cohort | n waves | mean Δ ticks | mean Δ% |
|---|---:|---:|---:|
| **SPARSE** (≤ 15 bodies) | 8 | **+20.1** | **+10.8%** |
| **DENSE** (> 15 bodies) | 12 | **−6.3** | **−2.9%** |

**Pearson r(body count, Δ%) = −0.575** over 20 waves.

### 4.5 Peak concurrency

**33 live bodies** in both runs — identical, as the single-variable design requires (baseline peak
at run_tick 1,261; PM1 at 1,292, displaced by the pacing shift). The board is the same board.

### 4.6 Kill distance — BOTH batons (also owed downstream to R-CPB-5)

Distance from the player's position at the kill tick to the body that died, read from the wire's own
columns (the body's last `damage_dealt` row against `tracks.player_path` at that tick), never
re-simulated. 344/344 kills measured on both sides; 0 excluded.

| | BASELINE | PM1 |
|---|---:|---:|
| min | 0.7881 | 1.0778 |
| p25 | 2.7253 | 2.4654 |
| **median** | **2.8119** | **2.6793** |
| p75 | 2.9072 | 2.8651 |
| p90 | 2.9709 | 2.9305 |
| p99 | 2.9966 | 2.9931 |
| **max** | **2.9982** | **2.9999** |
| mean | 2.7950 | 2.6406 |

Histogram (0.25 m bins, count · cumulative %):

| bin (m) | BASELINE | cum | PM1 | cum |
|---|---:|---:|---:|---:|
| [0.75, 1.00) | 1 | 0.29% | 0 | — |
| [1.00, 1.25) | 0 | — | 2 | 0.58% |
| [1.50, 1.75) | 0 | — | 2 | 1.16% |
| [1.75, 2.00) | 2 | 0.87% | 3 | 2.03% |
| [2.00, 2.25) | 0 | — | 8 | 4.36% |
| [2.25, 2.50) | 15 | 5.23% | **84** | 28.78% |
| [2.50, 2.75) | 95 | 32.85% | 99 | 57.56% |
| [2.75, 3.00) | **231** | 100% | **146** | 100% |

---

## 5 — What the numbers MEAN (and where I was wrong)

### 5.1 ⚑ My pre-registered prediction is FALSIFIED, and here is the mechanism

Math note § G.1, written before the run: *"Total ticks fall… closing speed rises from `v_mob` to
`v_mob + v_player`. Predicted direction: **fewer** total ticks."* **Wrong: +2.3%.**

The prediction was right about **half** the board and silent about the other half. Two measured
facts explain it:

1. **The player outruns almost everything.** Player 5.4 m/s; monster speeds min 2.4 / **median 4.0**
   / max 5.8 m/s — only **5 of 344** bodies are faster than the player.
2. **DRIVE-THROUGH has no stop clause, by ruling.** R-PM1-2 forbids stop-at-target-edge.

So closing speed is `v_mob + v_player` only while the player is **inbound**. Once it drives
*through* a cluster it is **outbound**, and for 339 of 344 bodies the gap now *opens* at up to
+1.4 m/s until the policy turns around. On a **dense** board that costs nothing — there is always
another cluster in front, the player is nearly always inbound at *something*, and the wave clears
faster (−2.9% mean). On a **sparse** board the last few stragglers spend real time chasing a
receding target, and the wave clears slower (+10.8% mean, worst +30.5% on wave 170's four bodies).

**This is a property of the ruled policy, not a defect, and it is NOT tuned away (Law 3).** It is
also the natural home of the first veto question in § 7.

### 5.2 The hysteresis was load-bearing — measured, not assumed

| | count |
|---|---:|
| re-target evaluations | 398 |
| forced re-targets (incumbent invalid) | 151 |
| **switches taken** | **16** |
| blocked by **margin** | 48 |
| blocked by **cooldown** | 16 |
| pass-through lock ticks | 653 |

**64 of 80 discretionary switches were refused** (80%). Without either term the target would have
flapped 5× more often, and R-PM1-3 rider (b) names exactly what that renders as.

### 5.3 ⚑ The margin's own declaration is partly falsified — reported, not retuned

The math note declared `m = 0.25` because it "clears one whole body whenever `S_inc ≤ 4`", and
committed to reporting the measured cluster-score distribution against that. Measured: per-wave
**median** cluster score at selection ranges 1–8 with a median-of-medians of **5**, and per-wave
maxima reach 16. At the typical `S_inc ≈ 5`, `m = 0.25` demands **+1.25** — i.e. **two** whole
bodies, not one. **The margin buys one body only on the smaller half of the distribution and two on
the larger half.** It is still monotone, still deterministic, still blocking flapping — but the
stated justification was sized against a distribution slightly smaller than the one that turned up.
Named here rather than quietly re-fitted; `m` is untouched.

### 5.4 ⚑ For R-CPB-5: the kill ring is 3.0 m, not 2.400 m

The SB-1 ledger's presentation law is framed against *"the 2.400 m kill ring"*. Measured off both
batons, **2.400 m is the ENGAGE ring (`d_engage_m`) — the radius at which a monster stops to
attack. It is not where anything dies.** Kills are bounded by the **EoR disc radius, 3.0 m**
(`config.kit.radius_m`), and **no kill in either run exceeds it**: baseline max 2.9982 m, PM1 max
2.9999 m.

If a VFX sweep extent is sized to read *under* the kill reach, the number to sit under is **3.0 m**,
and the empirical distribution to be honest about is:

* **BASELINE (the camping player the frozen baton describes):** kills pile hard at the rim —
  **67.2 % in [2.75, 3.00)**, median **2.812 m**, and only 5.2 % inside 2.50 m. The camping player
  kills things **as they arrive at the edge of the disc**.
* **PM1 (a moving player):** the pile-up relaxes — [2.75, 3.00) falls to **42.4 %**, [2.25, 2.50)
  rises from 15 to **84** kills, median drops to **2.679 m**. Because the player is moving, bodies
  cross the disc boundary at varied relative velocities instead of all walking into a stationary rim.

**Handed to the conductor as a correction of the frame, not a challenge to the law.** The
asymmetric-generosity direction (player VFX under-reads kill reach) is unaffected; only the number
it is measured against moves, 2.400 → 3.000, and the distribution under it is now measured on both
runs.

### 5.5 The knot explosion was predicted and is a size fact

1,003 → 15,793 (×15.7), predicted in math note § G.2 before the run. The predicate did not move
(R-L82-1, every velocity vertex); the **path** moved, because a pursuing body chasing a moving
point bends its bearing on nearly every pursuit tick. `G-LOCO-ONE-TRAJECTORY` is what would catch a
knot list that is *not* vertex-complete, and it is green. Declared on the wire for buffer sizing.

---

## 6 — SELF-ATTACK SURFACES (what in my own work is most inventable / fragile)

Ordered by how much I would want a second pair of eyes on it.

1. **β = 3.0 is census-anchored, and a census is still a choice of denominator.** I anchored it so
   the boss-class population carries the same total objective mass as everything else *on this
   roster*. A different roster moves β. Nothing downstream validates β; it is a taste-shaped number
   wearing an arithmetic derivation, and it is the parameter I would most expect Matt to have an
   opinion about. **Most inventable thing in the lap.**
2. **The pass-through lock (L = 3.0 m) is a second steering rule I introduced, not a ruled one.**
   R-PM1-2 ruled drive-through; the lock is *my* answer to the 6 Hz tremor that unclamped homing
   produces at the centroid. It is imported from the disc radius rather than picked, and the
   failure it prevents is written down — but it is still a mechanism the ledger did not ask for,
   and it fired on **653 ticks** (17% of the run). If it is wrong, the motion reads as gliding past
   targets rather than turning on them.
3. **The § I wave-boundary carry is a semantic change to run assembly, made mid-lap.** I judged the
   teleport a rendering defect and the carry the faithful model. It is defensible and it is
   **veto-open** — but it is the one place I changed something the cell did not scope, on my own
   judgement, and it is one unpassed parameter from being reverted.
4. **The margin justification is now known to be half-right** (§ 5.3). I left the value alone
   because moving it after seeing the data is fitting. Someone could reasonably say the honest move
   is to re-derive `m` from the measured distribution *once*, in public, and re-run.
5. **The cluster objective is anchor-centred, which is O(n²) per evaluation and slightly
   arbitrary.** Every live body anchors a candidate cluster; a true density estimate (e.g. a grid or
   a mean-shift) would give a different, arguably better, "densest pack". The anchor form was chosen
   because it is exactly expressible from Matt's sentence and needs no bandwidth parameter — but
   "the cluster centred on some body" is not identical to "the largest group".
6. **The findings instrument re-derives kill positions from `damage_dealt` rows** because `death`
   rows carry no position. It relies on the killing blow and the death sharing a tick — true in this
   engine (the death is emitted inside the same hit loop) and asserted nowhere. If that ever
   separates, the kill-distance histogram silently measures the wrong tick.
7. **I wrote in star-lord's seam.** Chartered, minimal, MIGRATION-filed — but four export files
   moved under a sim agent's hand, and the guard I added (baseline spec raises if it resolves to a
   non-record policy) is my own idea of what star-lord would want protected.

---

## 7 — Questions for the conductor / Matt (all veto-open, none blocking)

1. **Does the sparse-wave penalty want a policy answer?** § 5.1 is a clean, ruled consequence:
   drive-through + a player faster than 98.5% of the board means stragglers chase a receding target.
   A "close on the residual when the board is nearly clear" clause (the camp policy's own
   `CAMP_THEN_COLLECT` logic, which exists and is retired under this limb) would remove it — but it
   is exactly the stop-at-target R-PM1-2 rejected. **Not implemented; not tuned around. Matt's call.**
2. **§ I wave-boundary carry — keep or revert?** Adopted with reasons, one parameter from reverting.
3. **§ 5.4 — does R-CPB-5 want re-basing from 2.400 m to 3.000 m?** The engage ring and the kill
   ring are different rings and I think the presentation law is currently reading the wrong one.
4. **§ 5.3 — leave `m = 0.25`, or re-derive once from the measured distribution?** I left it.

**No HALT was hit.** Nothing required modifying the frozen baseline or its lineage; nothing smelled
like balance tuning; no structural surprise contradicted the ledger's premises. The § I boundary
carry is the only decision I took beyond the ruling set, and it is declared in three places
(math note, wire, both MIGRATION files) rather than buried.

---

## 8 — Cross-seam flags

* **star-lord** — `export/MIGRATION.md [2026-08-12]`. Five defaulted fields on `KC2RunSpec` + a
  `SPECS` table; `build_wire`/`emit` take `spec=`; output name keyed on `run_id`; per-spec knots
  supply. `E_S09_CP150` literally unchanged, 40 adapter tests pass unmodified. Plus the § 2.3
  host-filesystem-count-on-a-provenance-surface hazard.
* **drax / any scene consumer** — the three `PM1-*` wire declarations in § 2.2 are the read-this
  list. The knot-density row is the one that costs money if ignored.
* **rocket** — nothing. No generation primitive was needed or touched.
* **jack-ryan** — Discipline #12 semantic shift declared in commit messages, both MIGRATION files,
  the math note and on the wire. Discipline #1 satisfied (math note precedes both the policy module
  and the § I change). Discipline #2 smoke-then-full. Discipline #11: § 5.1 and § 5.4 are both
  cases where empirical inspection overturned a written assumption — mine in the first, the
  ledger's frame in the second.
