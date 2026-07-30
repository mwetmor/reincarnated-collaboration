# WR2-ENCGEO Cell D — the nova cast-gate parity fix + Mechanism D, telegraph escape-speed law

**Cell:** WR2-ENCGEO Cell D (charter §8.21 / §8.22 disposition (i) / §8.23 R-WR2-20) · **Agent:** gamora
**Date:** 2026-07-29 → 2026-07-30 · **Class:** BUILD, in seam (`simulation/`).
**Authority:** **R-WR2-19 (MATT-SIGNED)** for Mechanism D + gate S-7; **R-WR2-20** (conductor) for the
flag topology; **R-WR2-8/-17/-18** for the range law item 1 completes.
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md`
**Spec:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` §D / §E / §G
**Diagnostic of record:** `agentic_orchestration/gamora/notes/2026-07-29-wr2-f3-nova-diagnostic.md`
**Gate-2 riding obligations:** `agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr2-cell-c.md`
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr2-d-nova-telegraph-2026-07-29.md`
**Baseline:** engine `main` at `ecea69f` (charter §8.23 INFO-5 adoption). Tree tracked-clean at start.

---

## 1 — VERDICT

| # | obligation | result |
|---|---|---|
| 1 | **Build item 1** — nova cast-gate parity (rides `body_separation_v2`, R-WR2-20) | **PASS.** Gate 6/6 at `d = 10.2085905239 ≤ 10.5`; ring minted 5/6 (the miss is 74000800's 80 % `Chance` draw, the same seed that misses flag-OFF). `n_nova_crossings` **0 → 1** on five seeds Cell C measured at 0. **F-WR2-3 CLOSED.** |
| 2 | **The range-predicate sweep** (§8.22 disposition (ii)) | **PASS — 19 sites enumerated + a conclusive NEGATIVE finding.** Exactly ONE REACH predicate was out of law. Both attack phases read end to end: the nova was the *only* skill in the tree with a private reach gate downstream of the shared selector. |
| 3 | **Build item 2** — Mechanism D escape law (`nova_telegraph_v2`, default OFF) | **PASS.** `T = 12.0/(0.90 × 5.75) = 2.318840579710145 s` vs the measured 0.750 (3.0918×). Zero RNG, per-fight-constant, derived at cast. |
| 4 | **Ring reconciliation** (R-WR2-19 clause) | **PASS — resolved NAME-AND-PIN.** Drawn ring already == damage ring (one constant, four readers). `range_m` 10.0 is cast eligibility: the WR1 flag is a naming collision across two record blocks, not a lie in either direction. |
| 5 | **S-7 trace prep + field names** | **PASS, with one field ADDED** (`header.entities[].movement_speed_ms`, conditional). Without it S-7 was **provably vacuous** (§4.1). |
| 6 | **S-7 scratch spot-check** | **PASS 5/5, zero fail.** Worst ratio to bound **0.14928412301085175** — matching the math note's *a-priori* table to **15 s.f.** |
| 7 | **Flag-OFF byte-identity vs `ecea69f`** | **PASS, STRONGER than the law requires** — `diff -r` returns ZERO differing lines; SHA-256 identical on all 6 traces. |
| 8 | **Full regression name-diff** | **PASS — EMPTY both directions, 81/81.** |
| 9 | **Unit tests** | **PASS 69/69** new; 223/223 across the B + C + D + nova suites. |
| 10 | **Riding obligations** (WARN-1/-2/-3/-5, INFO-1/-4) | **ALL SIX DISCHARGED**, zero behaviour change. WARN-1 pinned by a new engine-level test. |
| 11 | **Residual counters (§B-6) re-reported** | **PASS — UNCHANGED by D on every tier.** Trash 2.000/fight (Cell C's `180 = 2 × 90` signature), 0 elsewhere. Not repaired. |
| 12 | **Predictions P-1..P-6** | **6 HIT.** P-6's *wording* scored as a miss (see §7.8). |

**Two things I got wrong and corrected before handing over — both found by measurement, not by
re-reading prose:** the S-7 onset-tick convention (§4.2, and it would have LOOSENED the gate Cell BAT
computes) and an unconditional trace field that would have broken flag-OFF byte-identity on all 450
traces (§4.1).

**One ⚑ for the conductor** (§7.9): `ACTIONABLE_WINDOW_S = 0.70` caps the M-3 evade budget
identically in both arms, so Mechanism D reaches R-WR2-19's *second* clause through telegraph TICK
COUNT (8 → 24), not through budget. **Reported, not repaired** — the constant is M-graded, outside
spec §E, and M-3 is dark on the battery.

---

## 2 — WHAT CHANGED, BY FILE:LINE

### 2.1 Item 1 — the nova cast-gate parity fix (rides `body_separation_v2`; NO new flag)

| file | line (post-landing) | change |
|---|---|---|
| `spatial_gauntlet/spatial_engine.py` | `:4485-4533` | The gate. `_eff_fire_range = p.fire_range_m + (target.entity_radius if self._body_separation_v2 else 0.0)`, then `if mob.distance_to(target) > _eff_fire_range: return False`. The bare `> p.fire_range_m` comparison is GONE. |
| `spatial_gauntlet/spatial_engine.py` | `:4470-4474` | `_gd_nova_cast` docstring's FIRE CONDITION clause names the surface measure and points at the selector by line. |

The fix is **one term**, and the invariant it restores is stated in-code as a rule rather than as a
symptom: *the range predicate the SELECTOR applies to skill i must be the predicate skill i's own
cast gate applies.* Flag OFF the added term is literally `0.0`, so the legacy expression is
byte-identical **by construction**.

**Why not a third flag** (R-WR2-20, and I would have made the same call): a separate flag lets the
two predicates disagree BY FLAG STATE, which is the bug's own shape.

### 2.2 Item 2 — Mechanism D (new flag `nova_telegraph_v2`, default OFF)

| file | line | change |
|---|---|---|
| `simulation/gd_nova.py` | `:259-323` (new §1b) | `NOVA_ESCAPE_FRAC = 0.90` (the one dial) + `telegraph_escape_duration_s(v, p, *, escape_frac)` — the LAW. Includes the declared `v <= 0` fallback to `p.wind_up_s`. |
| `simulation/gd_nova.py` | `:59-66` | `__all__` gains the two names. |
| `simulation/gd_nova.py` | `NovaScheduler.cast` | New keyword `wind_up_override_s: Optional[float] = None`. `None` → `params.wind_up_s`, the untouched path. |
| `spatial_gauntlet/spatial_engine.py` | `:562-565` | Import `telegraph_escape_duration_s as _gd_telegraph_escape_duration_s`. |
| `spatial_gauntlet/spatial_engine.py` | ctor | New param `nova_telegraph_v2: bool = False` → `self._nova_telegraph_v2`. Carries NO other state. |
| `spatial_gauntlet/spatial_engine.py` | `:4545-4580` | `_tg_wind_up_s` derived at cast; passed to `cast(wind_up_override_s=...)`. |
| `spatial_gauntlet/spatial_engine.py` | `:4621` | `TelegraphSpec(wind_up_s=float(_tg_wind_up_s))` — **ONE DURATION, TWO READERS.** |
| `spatial_gauntlet/spatial_engine.py` | `:5729-5735` | Crossing-phase ordering comment updated; names the consequence that a fight ending inside the window leaves a tell with no crossing. |
| `spatial_gauntlet/spatial_engine.py` | `run_spatial_fight` | Param threaded; conditional result key `nova_telegraph_v2=True` when armed. |
| `spatial_gauntlet/replica_frame_emitter.py` | `header` | **CONDITIONAL** `movement_speed_ms` per entity block when `engine._nova_telegraph_v2`. |
| `spatial_gauntlet/kitcal_g5_harness.py` | import block | `NOVA_ESCAPE_FRAC as _NOVA_ESCAPE_FRAC` — read from the module, never transcribed (the C-4 lesson). |
| `spatial_gauntlet/kitcal_g5_harness.py` | `run_one_fight` / `drive` / `_drive_armed` | Threaded, including the INS-1 probe (third instance of the matched-physics asymmetry). |
| `spatial_gauntlet/kitcal_g5_harness.py` | `wave_regime` | **UNCONDITIONAL** `nova_telegraph_v2_wr2_d` + `nova_escape_frac_wr2_d`. |
| `spatial_gauntlet/kitcal_g5_harness.py` | CLI | `--nova-telegraph-v2`, `_ntv2` artifact suffix, armed banner. |

**ONE DURATION, TWO READERS** is the design point worth naming: the ring's `t_launch` and the
telegraph's `wind_up_s` take the *same float*. `fire_time_s` / `fire_tick` derive from
`ring.t_launch`, so all three are one number by construction. If they could differ, the depicted
tell would be a lie about the fight — which is the exact failure class the ring-reconciliation clause
exists to prevent.

### 2.3 ⚠ SS-D-1 — the semantic shift, named (Discipline #12)

Under the flag, an **M-GRADED** constant stops governing the telegraph window: `NovaParams.wind_up_s`
= 0.750 s (45 frames @ 60.000 fps CFR, two reads, honest bracket 0.717–0.750) is replaced by the
**derived** 2.318840579710145 s. This is a fidelity-to-the-fixture LOSS traded for a
fidelity-to-playability GAIN, and the trade is Matt-signed, not a build decision.

Three safeguards so the trade stays inspectable rather than laundered:

1. **`NovaParams` is NOT mutated.** The override is a `cast()` PARAMETER. The frozen dataclass keeps
   its M value and its bracket, so a derived duration can never be misread as a measurement, and
   H-M2-f ("a default must never silently fill this slot") is untouched — the slot is replaced by a
   LAW under a named flag, not filled by a default.
2. **The trace declares the regime** (`wave_regime.nova_telegraph_v2_wr2_d` + the conditional
   `movement_speed_ms`).
3. **The existing M-pin tests stay green UNMODIFIED** — they run flag-OFF and assert 0.750. That is
   exactly the guard that should keep working, and I did not touch it.

### 2.4 Ring reconciliation — resolved NAME-AND-PIN, not repair

R-WR2-19's required clause. The WR1 flag reads `range_m: 10.0` vs `radius_m: 12.0`. **Measured
disposition: the drawn ring ALREADY equals the damage ring**, because those are two *quantities*, not
two values of one:

* `radius_m = projectile_distance_m = 12.0` is the DAMAGE radius — the cutoff `band_scale_at` returns
  `0.0` beyond, the radius `resolve_tick` culls at, the radius the telegraph DRAWS, and now the
  radius the escape law binds on. **One constant, four readers.**
* `range_m = fire_range_m = 10.0` (header `skills` block) is **CAST ELIGIBILITY**. It never described
  the footprint, and the telegraph event's own `range_m` is `None` (a ring has no forward extent).

So the WR1 flag is a **naming collision across two record blocks**, not an outward or inward lie.
Nothing moves; the identity is pinned by test and stated by field name in MIGRATION. One property the
fixed gate now guarantees, and it is what makes the reconciliation safe: `d ≤ 10.5 < 12.0`, so **the
player is always strictly inside the drawn ring at telegraph onset.**

---

## 3 — THE RANGE-PREDICATE SWEEP (charter §8.22 disposition (ii))

Enumerated by grep over `spatial_gauntlet/` + `gd_nova.py` (`distance_to`,
`_dist_point_to_segment`, and every `*range*` / `*radius*` / `*reach*` comparison). **19 sites.**
Classification is the load-bearing part: **REACH** predicates (may I hit / fire at that BODY?) take
the surface measure; **FOOTPRINT**, **AI-STATE**, **SELECTION** and **INSTRUMENT** predicates do not.
Full table with per-row reasons: math note §1.3. Summary:

| class | sites | disposition |
|---|---|---|
| **REACH** | `:2641` selector · `:4485` nova gate | selector ✅ already S2S (SS-B-1); **nova gate ⛔ WAS THE DEFECT → fixed, same flag** |
| **REACH-adjacent (movement)** | `:5570`/`:5475` `min_attack_range` · `policy/reposition.py` band | band ✅ already surface-aware under `_bsep`; the advance threshold stays centre-to-centre **by design** — moving it would shift the band a second time from underneath itself |
| **FOOTPRINT** | `:1541` circle · `:1553` cone · `:1590` line · `gd_nova.py:165/290/835` | ⬛ centre-to-centre. A blast extent is not a reach to a body. **⚑ site `:1541` is the select-but-WHIFF half of the same pattern** (see §3.1) |
| **AI-STATE** | `:1977` + `:5961` serial activation · `:1990` leash · `:2081`/`:2104`/`:2114` kite/cast/hit-and-run · `:6214` proximity trigger | ⬛ aggro / standoff / latch, not reach. Four of the six are structurally unreachable on this battery (`serial_activation_radius_m` is `None`; `_positioned_allies` is empty; the melee roster never enters the kite branches) |
| **SELECTION** | `:2554` nearest pick · `:1613` point branch · `:1871` taunt weight | ⬛ argmins and weights, no threshold to move. Radius-invariant where radii are equal, and where they differ the surface-nearest body IS the one a reach law would prefer |
| **INSTRUMENT** | `:1780` coverage pressure · `policy/exposure_map.py` density kernels · `policy/telegraph_response.py:264` shelf | ⬛ metrics and the player's own reachability sampling; no hit, no cast |

**Exactly ONE REACH predicate was out of law, and it is this cell's fix.**

### 3.1 The negative finding that makes the sweep CONCLUSIVE rather than merely long

A table of hits cannot prove absence, so I read both attack phases end to end looking for a **second
reach gate** — the defect's shape, one layer downstream of the selector:

* **Player attack phase** (`:5783`–`:5940`): `_select_skill_for_entity` → `skill_geometries[idx]` →
  `_compute_aoe_hits`. **No distance comparison of any kind between them.**
* **Mob/boss attack phase** (`:5950`–`:6060`): `_select_skill_for_entity` → the three-way `_gd_nova`
  / `self`-`none` / generic-AOE `elif` chain. **The only distance comparison in the entire chain was
  the nova's gate.**

So the nova was the **only skill in the tree carrying a private reach gate downstream of the shared
selector.** That is why the defect existed at all, and why fixing one site closes the *class* rather
than one instance. A second-pass grep over `(<=|>) *[a-z_.]*(range|radius|reach|dist)` returned nine
hits, all already in the table.

### 3.2 ⚑ The pattern behind both halves, and the half I did NOT repair

| | selector admits at | effect layer measures | outcome |
|---|---|---|---|
| **nova** (fixed here) | 10.5 (surface) | 10.0 (centre) | **REFUSE** — and bills 6.0 s of action budget |
| **circle AoE** (jack-ryan's Cell-B INFO-2) | 3.5 (surface) | 3.0 (centre) | **WHIFF** — the cast lands on nothing |

One mechanism: *the selector and the effect layer measuring reach differently.* The nova half is a
REACH predicate and is fixed. The AoE half is a **FOOTPRINT** predicate — a different class — so it
is **reported, not repaired.** It is currently unreachable on this battery (this kit carries **no
circle skill at all**: `feral_claws_r16` cone, `rip_and_tear_r16` line), and Cell C's `band_outer`
2.70 sits **0.30 m** clear of its binding edge (WARN-2, §6.2). **Conductor's call, not mine** — the
fix would change footprint semantics on every circle AoE in the corpus, which is far outside Cell D.

---

## 4 — S-7 TRACE FIELDS, BY EXACT NAME (charter §8.21 prep)

| quantity | exact field name | status |
|---|---|---|
| telegraph ONSET tick / instant | `<telegraph event>.tick` / `.t_s` | ✅ existed. `_frame_sink.telegraph(...)` fires AT CAST, so these are onset, not launch. |
| `telegraph_duration` | `<telegraph event>.wind_up_s` | ✅ existed; carries `T` under the arm (SS-D-1). |
| launch instant | `<telegraph event>.fire_t_s` / `.fire_tick` | ✅ existed. `fire_t_s == t_s + wind_up_s` — **use it as a cross-check on the duration.** |
| damage radius | `<telegraph event>.radius_m` | ✅ existed; `= projectile_distance_m`. |
| ring origin | `<telegraph event>.origin_x_m` / `.origin_y_m` | ✅ existed. |
| player position at onset | `<tick record where tick == onset_tick>.entities[is_player].x_m` / `.y_m` | ✅ recoverable — **the SAME index, NOT `tick - 1`. See §4.2 — this is a correction.** |
| **player move speed** | **`<header>.entities[is_player].movement_speed_ms`** | ⚠ **DID NOT EXIST — ADDED THIS CELL, conditional on the D arm.** |

**The exact predicate Cell BAT should compute:**

```
onset_tick = telegraph.tick                       # nova rings: shape == "circle"
d_onset    = hypot(player.x_m@[onset_tick] - telegraph.origin_x_m,
                   player.y_m@[onset_tick] - telegraph.origin_y_m)
S-7 holds iff (telegraph.radius_m - d_onset) / telegraph.wind_up_s
                  <= NOVA_ESCAPE_FRAC * header.entities[player].movement_speed_ms
```

### 4.2 ⚠ THE ONSET TICK IS `tick`, NOT `tick - 1` — I had this wrong, and it LOOSENED the gate

**This note's first draft, the math note's first draft and MIGRATION's first draft all said
`tick - 1`.** Cell BAT computes the gate of record from this contract and would have inherited it.
Recorded rather than silently edited.

**Mechanism.** Loop order within tick *k*: player movement (`:5518`) → soft collision (`:5712`) →
nova crossing resolve (`:5724`) → player action (`:5776`) → **MOB ACTION, where the cast and
`telegraph(tick=k)` happen** (`:5949`) → `tick` record (`:6691`). The tick-*k* record therefore holds
the position AFTER tick *k*'s movement — **exactly the position the caster measured.**

**Falsifier, `boss__B__seed74000802`, all three arms armed:**

| read | `d_onset` | `≤ 10.5` (the fixed gate's own ceiling)? | `v_req` | ratio to bound |
|---|---|---|---|---|
| `tick - 1` (the wrong draft) | 10.7835905239 | **NO** | 0.524577 | 0.101367 |
| **`tick` (correct)** | **10.2085905239** | **YES** | **0.772545** | **0.149284** |
| `tick + 1` | 9.6335905239 | yes | 1.020514 | 0.197201 |

Two confirmations, the first decisive:

1. **`tick - 1` is IMPOSSIBLE.** At 10.7836 the fixed cast gate would have REFUSED the cast, so the
   telegraph could not exist. A convention that contradicts the predicate which produced the record
   cannot be that record's convention.
2. **`tick` reproduces the F-WR2-3 diagnostic's independently measured cast distance to 10 decimal
   places** (10.2085905239), and its ratio-to-bound `0.14928412301085175` matches the math note's
   *a-priori* §2.2 table row to **15 significant figures**.

**Why the direction is the point.** `v_req = (R − d)/T` DECREASES in `d`, so reading one tick early
(further away) UNDERSTATES required escape speed — here by **32 %** (0.5246 vs 0.7725 m/s). It would
have made S-7 easier to pass than the mechanic actually is. **An error that loosens a gate is worse
than one that tightens it**, which is why this is in the verdict table and not a footnote.

How it was caught: not by re-reading the prose, but because the measured `d_onset` **exceeded the cast
gate's own ceiling** — an internal contradiction only a number could surface (Discipline #11).

### 4.1 ⚠ Why the added field is load-bearing, and why S-7 would otherwise be VACUOUS

This is the one thing in the cell I want the conductor to read closely. Without an **independent**
move speed, the only way to obtain `FRAC · v` from a trace is `radius_m / wind_up_s` — **which is the
law itself.** The predicate then reduces to

```
(radius_m - d) / wind_up_s  <=  radius_m / wind_up_s     ⟺     d >= 0
```

**i.e. vacuously true, and S-7 would have graded nothing.** With `movement_speed_ms` in the header,
S-7 becomes the real check: *was the shipped duration derived from the shipped speed by the shipped
law?* That is falsifiable, and it is what a gate is for.

The field is **CONDITIONAL on the D arm**, not unconditional, and that was forced rather than chosen:
the charter pins Cell D's flag-OFF traces byte-identical to `ecea69f`, and an unconditional header
key breaks that on all 450 traces including the ones with no nova. Conditional is also the better P-2
shape (Cell B's ruling, reused): key ABSENT = the escape law did not govern this trace; key PRESENT =
it did, and here is the input it read.

---

## 5 — THE LAW, AND WHY S-7 CANNOT FAIL BY ARITHMETIC

Derivation (math note §2.1): the damage area is the disc of radius `R` about the origin; a target at
`d` must cover `R − d`, so `v_req(d) = (R − d)/T` is **monotonically decreasing in d** and the worst
point inside the area is the **CENTRE**. Pinning `v_req(0) = FRAC·v` gives the law, and it is the only
`T` that does:

```
T = R / (FRAC · v)                                                    [FROZEN — R-WR2-19]
v_req(d) / (FRAC · v) = 1 − d/R                                       [THE MARGIN IDENTITY]
```

This fixture: `R = 12.0`, `v = 5.75` m/s (**measured, not assumed** — the player kit declares no
`movement_speed`, so the engine default at `:7182` supplies it), `FRAC = 0.90`:

```
FRAC · v = 5.175 m/s        T = 12.0 / 5.175 = 2.318840579710145 s   (23.1884 ticks)
vs the measured 0.750 s → 3.0917874396135265x LONGER
```

| `d` | `v_req` | ratio to bound | ratio to move speed |
|---|---|---|---|
| 0.0 — unreachable (B holds 2.0) | 5.175 | **1.0000** (exact, no epsilon needed) | 0.900 |
| **2.0 — B's floor, the WORST REACHABLE** | **4.3125** | **0.8333** | **0.750** |
| 10.2086 — the measured cast distance | 0.77255 | 0.1493 | 0.1343 |
| 10.5 — the fixed gate's ceiling | 0.646875 | 0.1250 | 0.1125 |

**So S-7 holds with ≥ 16.67 % margin for every geometrically possible firing in this fixture,
independent of seed** — closed form, not a sample. Registered as prediction P-2 so the battery can
falsify it. Float note: `12.0 / (12.0 / 5.175) == 5.175` **exactly** in IEEE-754 double, verified, so
Cell BAT needs no tolerance even at the degenerate centre.

**Read the margin identity for what it means about the gate:** S-7 holds *by construction*, so what
it actually falsifies is **whether the shipped duration equals the law's duration.** That is the only
falsifiable content, and §4.1 is why it is falsifiable at all.

---

## 6 — RIDING OBLIGATIONS DISCHARGED (charter §8.23) — ZERO behaviour change

| item | discharge | where |
|---|---|---|
| **WARN-1** | Named IN CODE as a REPOSITION-tick clock + in math note §5.1 + **pinned by a new engine-level test** | `spatial_engine.py:5654-5675`; `test_the_flip_clock_is_a_REPOSITION_tick_clock_not_a_sim_tick_clock` |
| **WARN-2** | 0.80 → **0.30 m** corrected, with an explicit ERRATUM block naming the two-different-0.80s confusion | Cell C note §(S-3) erratum; math note §5.2; `test_WARN_2_...` |
| **WARN-3** | MIGRATION §5 restated by field name with the measured `heading_rad` counter-table | `MIGRATION.md` Cell-C entry §5 erratum; math note §5.3 |
| **WARN-5** | HOLD annulus `d ∈ (1.70, 2.00]` named beside SS-C-3 with its `BAND_WIDTH` coupling; **name-and-pin, NOT repair** | Cell C math note §2.3; math note §5.4; `test_WARN_5_...` |
| **INFO-1 / INFO-4** | Stall convention (3.84 vs 7.43) + `azimuth_reversals` deadband (1/3/21 vs 9/23/22) in the driver docstring | `wr2_cell_c_move_2026_07_29.py::trajectory`; math note §5.5; `test_INFO_1_and_INFO_4_...` |

### 6.1 WARN-1 — the pin is the part that was missing, and it is the part I care about

jack-ryan's finding was precise: Cell C's flip tests all pass `ticks_since_flip` in **as a parameter
to the pure helper**, so *nothing pinned the engine's clock SOURCE.* That is the same
declaration-vs-transcription gap that produced Cell B's HALT, here with a trivial consequence rather
than a gate-breaking one — but the same shape. The new test closes it two ways:

* **Source:** asserts the single increment site sits INSIDE the REPOSITION limb, so moving it to the
  tick loop (a defensible change — spec §C-2 says "elapsed") fails the test and forces the §E
  TUNABLE periods to be re-read as seconds.
* **Behavioural:** drives a real armed boss fight, counts reposition vs non-reposition decision
  ticks, and asserts `clock ≤ n_reposition < n_decision_ticks`. It **refuses to pass vacuously** —
  it asserts both branch counts are non-zero first, so a fight that exercised only one branch fails
  rather than silently proving nothing.

**Named, not changed**, because both periods are §E **TUNABLE**: a lap is licensed to move exactly
these two numbers, and a lap that moves a period does so believing it is moving seconds. Converting
the clock would be a mechanism change no gate is asking for.

### 6.2 WARN-2 — a correction, plus the confusion that made it worth filing

The clearance is **0.30 m** (`3.0 − 2.70`), not 0.80 m. The window is `d ∈ (3.0, 3.5]` and its
**binding edge is 3.0** — 0.80 m is the distance to the FAR edge, which nothing has to cross to get
in. It overstated available `BAND_WIDTH` headroom by **2.7×**. The test was always right.

**The trap I walked into while fixing it, recorded because a future reader will hit the same thing:**
the Cell C math note ALSO contains a correct 0.80 m at §2.2 — the slack of the *reach* term
(`3.50 − 2.70` boss, `2.50 − 1.70` mob). **Two 0.80s, two different measurements, one of them
wrong.** I nearly "corrected" the right one. Both are now labelled at both sites.

---

## 7 — MEASURED

Sample: boss tier, arm B, `R2_proxy_resists_low`, `--gd-cadence --with-nova --emit-telegraphs`,
seeds 74000800–74000805 — **the same six the F-WR2-3 diagnostic used**, so its numbers compare
directly. Raw: `agentic_orchestration/gamora/notes/2026-07-30-wr2-cell-d-s7-spotcheck.json`
(committed); scratch traces at `/tmp/wr2d/` (regenerable, not committed).

### 7.1 Item 1 — the mechanic is back

Range gate passes at `d = 10.2085905239 ≤ 10.5` in **6/6**; the ring is minted **5/6**, and the miss
is **74000800** — the same seed that loses the 80 % `Chance` draw flag-OFF, on the nova's dedicated
sub-stream. `n_nova_crossings` per seed under `_bsep_mv2`: **0, 1, 1, 1, 1, 1**, where Cell C's
landing measured **0 on all six.**

### 7.2 Gate S-7 — 5/5 HOLD, zero fail

| quantity | value |
|---|---|
| firings assessed / hold / fail | **5 / 5 / 0** |
| unassessable (no speed field) | **0** — the header field is present on every armed trace |
| `d_onset` | **10.2085905239** on all five (seed-invariant: the approach carries no RNG) |
| `wind_up_s` | **2.318840579710145** on all five |
| worst `v_req` | **0.7725453365811579** m/s |
| bound (`0.90 × 5.75`) | **5.175** m/s |
| **worst ratio to bound** | **0.14928412301085175** |

**The cross-check I care about more than the pass:** the math note's §2.2 table — written before any
code existed — predicts `0.14928412301085192` at `d = 10.2086`. The trace-derived value agrees to
**15 significant figures.** A derivation and a measurement meeting is what makes P-2's `≤ 0.8333`
bound a prediction rather than a restatement.

### 7.3 The conditional trace field, verified at artifact level

`movement_speed_ms` **present** on every armed trace (`5.75` on the player block), **absent** on every
unarmed trace (grepped across all six byte-identity traces). Both halves measured, neither assumed.

### 7.4 Flag-OFF byte-identity vs `ecea69f` — PASS, and stronger than the law requires

Method: `git archive ecea69f | tar -x` to a scratch tree (read-only plumbing — writes nothing to
`.git`, creates no worktree), then the SAME unarmed slice emitted from each tree with `git_hash`
pinned to one literal so even the header field is comparable.

* Slice: boss + trash × seeds 74000800/-01/-02 = **6 traces**, all three v2 flags OFF.
* `diff -r base head` → **IDENTICAL, zero differing lines.** Not "modulo `engine_git_hash`" —
  literally zero.
* Per-file **SHA-256 identical on all 6.**
* The unarmed nova telegraph still carries the **MEASURED** values — onset `tick 8`, `t_s 0.80`,
  `wind_up_s 0.75`, `radius_m 12.0`, `fire_t_s 1.55` — the WR1 banked figures exactly (baton §5), and
  seed 74000800 still has no ring. **SS-D-1's flag-OFF half is verified against the fixture's own
  numbers, not merely against itself.**

### 7.5 Full regression — name-diff EMPTY, both directions, 81/81

`60 failed, 6197 passed, 21 errors in 1205.00s (0:20:05)`. 60 + 21 = **81** against the banked
81-name baseline; `comm -13` and `comm -23` both return nothing. Sequential, single process (the WR2
wave-tail law: no parallel pytest against the shared editable install).

Cell D's own suite **69/69**; B + C + D + the two nova suites together **223/223**.

**Process catch, self-ledgered.** I started the regression, then landed a comment-only source edit
mid-run — the exact hazard Cell B-FIX recorded (a mid-run edit tripping `inspect.getsource` tests).
I **killed and restarted against the final tree** rather than reason about whether the edit was
harmless. Cost ~7 minutes; the alternative was a regression of record against a tree that no longer
existed.

### 7.6 Residual counters (§B-6) — re-reported across ALL FOUR tiers, in BOTH D arms

| tier | fights | ticks D-OFF | ticks D-ON | per fight | worst gap (counter, PRE-correction) |
|---|---|---|---|---|---|
| **trash** | 6 | **12** | **12** | **2.000** | 1.3506 mm |
| champion | 6 | 0 | 0 | 0.000 | 0 |
| mixed_pack | 6 | 0 | 0 | 0.000 | 0 |
| boss | 6 | 0 | 0 | 0.000 | 0 |

**Mechanism D moves them by exactly zero on every tier** — the required answer, since D changes timing
and not geometry. The trash figure reproduces Cell C's signature exactly: **2.000 ticks/fight**, which
is where the battery-wide `180 = 2 × 90` came from. **Not repaired** (charter instruction).

Two quantities that must not be conflated: **1.3506 mm** is the counter's deliberate PRE-correction
over-report (§B-6); Cell C's and jack-ryan's **0.98 mm** is the measured POST-solver overlap in
emitted frames. Different measurements, both intact. **WARN-2's evidence boundary is still not
reached.**

### 7.7 S-6 line items (REPORTED, not gated)

`elapsed_s`, boss tier, `_bsep_mv2` → `_bsep_mv2_ntv2`:

| seed | crossings | elapsed OFF → ON | Δ |
|---|---|---|---|
| 74000800 | 0 → 0 | 61.600 → 61.600 | **0.000** |
| 74000801 | 1 → 1 | 17.600 → 40.200 | +22.600 |
| 74000802 | 1 → 1 | 35.500 → 20.400 | −15.100 |
| 74000803 | 1 → 1 | 37.300 → 20.800 | −16.500 |
| 74000804 | 1 → 1 | 17.500 → 37.000 | +19.500 |
| 74000805 | 1 → 1 | 37.100 → 22.000 | −15.100 |

Three shorter, two longer, **one exactly unchanged — and it is the seed with no ring.** That is the
cleanest available demonstration that the arm acts *through the nova and nowhere else*: an arm with a
side channel would have moved 74000800 too. `winner` is `monster` on all six in both arms, so the S-3
predicates are undisturbed on this slice. **Crossing COUNT is unchanged (5/5 rings still cross); what
moved is WHEN, therefore at what radius, therefore how much.**

### 7.8 Prediction scoreboard (Discipline #11)

| # | prediction | result |
|---|---|---|
| P-1 | gate 6/6, ring 5/6, 74000800 the `Chance` miss | **HIT**, exactly |
| P-2 | S-7 100 %, worst ratio ≤ 0.8333 | **HIT** — 5/5, worst 0.14928 |
| P-3 | flag-OFF byte-identical + name-diff EMPTY | **HIT** — byte-identity came back *stronger* than predicted |
| P-4 | flag-OFF report gains keys ⇒ Cell BAT's report baseline pins at Cell D | **HIT** — and it is TWO keys, not one |
| P-5 | outcomes move in both directions; no direction predicted | **HIT** |
| P-6 | residuals stay at Cell C's signature | **HIT on content; WORDING scored as a miss** — I wrote "180 ticks", but 180 is an all-tier battery total that a 6-seed boss slice cannot produce. The falsifiable content (2/fight trash, 0 elsewhere, invariant to D) held. |

### 7.9 ⚑ FINDING — Mechanism D does NOT reach R-WR2-19's second clause on its own. REPORTED, NOT REPAIRED.

R-WR2-19 carries a second sentence beside S-7: *"the M-3 evade-armed player's realized nova-crossing
rate must DROP vs BEFORE."* Arithmetic, unchanged by this cell:

```
t_eff  = min(t_remaining_s, ACTIONABLE_WINDOW_S) - reaction_latency_s
ACTIONABLE_WINDOW_S = 0.70  (M — same footage as the windup)   reaction_latency_s = 0.30 (default)
```

| arm | `t_remaining` at cast | `min(·, 0.70)` | `t_eff` | per-tick budget |
|---|---|---|---|---|
| D OFF | 0.750 | 0.70 | 0.40 | 5.75 × 0.40 = **2.300 m** |
| D ON | 2.3188 | **0.70** | 0.40 | **2.300 m — IDENTICAL** |

**The `min` binds in both arms, so D changes the per-tick evade budget by exactly nothing.** What it
does change is the NUMBER of telegraph ticks the policy acts on — `ceil(0.750/0.1) = 8` →
`ceil(2.3188/0.1) = 24`, a 3.0× increase in cumulative repositioning reach (≈ 4.3 m → ≈ 13.3 m at
≤ 0.575 m executed per tick). So the second clause is plausibly reachable **through tick count, not
through budget** — and if it fails, the suspect is `ACTIONABLE_WINDOW_S`, not the escape law.

**Why I did not touch it, and this is a boundary rather than a preference:** `ACTIONABLE_WINDOW_S` is
**M-graded**; spec §E's frozen wall and R-WR2-19's own scope ("the one dial is `NOVA_ESCAPE_FRAC`")
put it out of reach; re-deriving an actionable window from a DERIVED telegraph would be circular; and
**M-3 is dark on the battery of record** (`wave_regime.piloted_competence_m3: null`), so the clause
cannot be measured on the AFTER battery without a new arm. **Conductor's ruling, not mine.**

### 7.10 ⚑ FINDING — the AoE select-but-WHIFF window stays open. REPORTED, NOT REPAIRED.

The other half of §3.2's pattern (jack-ryan's Cell-B INFO-2): a circle AoE may be SELECTED to 3.5 m
under SS-B-1 while `_compute_circle_hits` still measures `aoe_radius` 3.0 centre-to-centre. **Not
fixed here on a classification argument, not on convenience:** the nova's gate was a **REACH**
predicate (may I fire at that body?) and belongs to the surface measure; a blast radius is a
**FOOTPRINT** — an extent in the world — and changing it would alter footprint semantics for every
circle AoE in the corpus. Far outside Cell D, and outside R-WR2-8's own wording. Currently
unreachable on this battery (this kit has **no circle skill**: cone + line), with Cell C's
`band_outer` 2.70 sitting **0.30 m** clear of the binding edge.

---

## 8 — WHAT NEEDS A CONDUCTOR RULING

1. **§7.9 — `ACTIONABLE_WINDOW_S` and R-WR2-19's second clause.** Whether the M-3 realized-crossing
   clause is (a) deferred as unmeasurable on a M-3-dark battery, (b) measured by arming M-3 in a
   supplementary set, or (c) answered by an M-constant amendment. **Not a Cell D decision.**
2. **§7.10 — the circle-AoE whiff window.** A FOOTPRINT-class question that the nova fix does not
   reach. Currently harmless on this fixture; a ledger item, not a blocker.
3. **Cell BAT's flag-OFF REPORT baseline must pin at `796a6f6d`** (this cell's landing), not
   `ecea69f`: `wave_regime` gains two keys unconditionally, by the arm-declaration precedent. **Trace
   byte-identity against `ecea69f` is UNAFFECTED and verified** (§7.4). Same class as Cell C's INFO-5,
   declared here rather than discovered at the gate.
4. **The S-7 onset-tick convention is `tick`, not `tick - 1`** (§4.2). If any downstream note or
   grading script already transcribed `tick - 1` from an earlier draft of this cell, it must be
   corrected — the wrong read **loosens** the gate by 32 %.

---

## 9 — COMMITS

| hash | content |
|---|---|
| `28386b26` | Math note — written BEFORE the code (Discipline #1). The law, the derivation, the 19-site sweep, SS-D-1, the §E-D table, the riding obligations, and the six registered predictions. |
| `b35695c0` | The build. Item 1 (parity fix, rides `_bsep`) + item 2 (Mechanism D, `nova_telegraph_v2`), the conditional trace field, the harness/CLI/report wiring, and the six riding-obligation doc/pin edits. |
| `796a6f6d` | Tests (69/69) + all measured evidence + the onset-tick correction propagated to the math note and MIGRATION. |

MIGRATION entry: `simulation/MIGRATION.md` → `[2026-07-30] WR2-ENCGEO Cell D` (nine sections;
consumers are star-lord for the two report keys and drax for the 3.09× telegraph-duration change plus
the conditional header field).

**Not pushed** — the conductor pushes at banking.
