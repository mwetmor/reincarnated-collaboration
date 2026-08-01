# BR-2 / RESOLVE-TRUTH-1 — landing note

**Cell:** 1d of run BR-2 (TRUE-SHAPE). **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Author:** gamora (simulation seam). **Date:** 2026-08-01.
**Authority:** BR-2 charter § ADDENDUM 4.
**Math note (BEFORE the code, Discipline #1):** `reincarnated-engine/src/reincarnated/simulation/math/br2-resolve-truth-1-2026-08-01.md`
**Commits:** `16fa7e8d` (code + schema + tests + MIGRATION), landing note follow-on.
**Pre-change HEAD:** `28eddef4`. **Battery of record:** `~/Games/reincarnated-godot/tmp/wr3acc/traces/`, 200 traces, 90,708 records, 1,556 telegraphs, stamped `16fa7e8d`.

---

## 0. THE ANSWER TO THE QUESTION THE CELL WAS CHARTERED TO ASK

**The nova is SIXTEEN CORRIDORS. It is not a disc, and it has never been one.**

`n_realized` (`gd_nova.py:666`), called at `spatial_engine.py:6548` and gated at `:6559`, counts how
many of the 16 prong corridors — each of half-width **0.42 m** — cover the target's bearing. If none
do, `delivered` is 0 and the crossing deals nothing.

Measured over the battery, and this is the number that should decide what the renderer draws:

> **226 of 466 resolved nova crossings — 48.5 % — dealt ZERO damage. Not one of them was out of
> range. Every single one passed through a prong gap.**

The ring is gapless only inside `0.42 / sin(π/16)` = **2.1528 m**, which is melee. At r = 9 m,
**76.2 % of bearings are safe.** Union lethal area out to 12.0 m is **147.06 m²** against a drawn
disc of **452.39 m²** — the disc is **3.076×** the lethal area.

Every frame this project has rendered has told the player *run out of the nova*. Half the time the
resolver's answer is *stand still*. That is the charter's hypothesis, confirmed, with a denominator.

---

## 1. THE PREDICATES, WITH CITATIONS

### 1.1 WAVE

`spatial_engine.py:8039` → `_gd_wave_resolve_tick` `:6770` → `WaveScheduler.resolve_tick`
`gd_boss_kit.py:836` → `wave_hits` `:648` → `wave_half_width_m` `:633`.

```
half_w(u) = (start_width_m + (width_m − start_width_m)·clamp(u,0,range_m)/range_m) · 0.5
HIT ⟺  −r_t ≤ u ≤ range_m + r_t                              (:678)
   ∧  |s| ≤ half_w(u) + r_t                                  (:680  THE TAPER)
   ∧  max(0, v·t − depth_m) ≤ u + r_t  ∧  u − r_t ≤ v·(t+dt) (:688  THE BAND)
```

Confirmed against the conductor's two open questions: **yes**, it also tests along-axis bounds
against `distance_m` (`:678`); **yes**, `target_radius_m` is added to the TARGET, not the lane — so
the shape to draw is the bare trapezoid.

### 1.2 NOVA

`spatial_engine.py:8032` → `_gd_nova_resolve_tick` `:6499` → `NovaScheduler.resolve_tick`
`gd_nova.py:1137` → `RingEvent.crossing_time` `:1026`; then `n_realized` `:666` at
`spatial_engine.py:6548`, gated `:6559`.

```
α(r) = 0  if r > radius_m ;  π  if r ≤ h ;  asin(h/r) otherwise      (coverage_half_angle :578)
HIT ⟺ r* ≤ radius_m ∧ #{ j : |wrap(φ* − spoke_offset − j·2π/N)| ≤ α(r*) } ≥ 1
```

`oracle_count_at` `:785` re-derives the identical predicate from segment distances as an independent
implementation, and a test asserts exact agreement.

**Disc or corridors: CORRIDORS.** Sixteen of them, 0.84 m wide.

**The 1.5 m splash is NOT in the predicate.** `hit_half_width` `:210` returns `explosion_radius_m`
**only when `threat_half_width_m is None`**, and the shipping star sets 0.42 (`:411`). The other
reference (`:776`) is inside `EXT_1_3_FALSIFIED_n`, the retired operator.
*Null-instrument control: the identical selector returns 3 live sites on `hit_half_width` (`:210`,
`:602`, `:792`) before it was allowed to report `explosion_radius_m` as predicate-dead.*

**The distance bands are magnitude, not hit-test** (`band_scale_at` `:222`). Only the beyond-12.0 arm
gates a hit, and `radius_m` already carries it. Emitted anyway, on the charter's instruction and
R-BR-28's ruling.

### 1.3 BLIZZARD

`BlizzardScheduler.resolve_tick` `gd_boss_kit.py:1159`, per-drop test at `:1181`:
`(x − d.x)² + (y − d.y)² ≤ hit_radius_m²`. No per-target dedupe.

**Cell 1b's fields do NOT close it.** Drop positions are drawn at cast (`:1141-1156`) — four RNG
draws each on a dedicated sub-stream — and no consumer without the engine's PCG64 state can produce
them. `hit_radius_m` made one disc honest; it could not say where the 24 discs are.

---

## 2. FIELDS SHIPPED — six, all additive and nullable

| field | nova (470) | wave (516) | blizzard (570) | required by |
|---|---|---|---|---|
| `start_width_m` | null | **3.0** | null | `wave_half_width_m` — the taper's other endpoint |
| `depth_m` | null | **1.0** | null | `back(t) = max(0, v·t − depth_m)` |
| `corridor_half_width_m` | **0.42** | null | null | `α(r)` — **the nova's entire hit test** |
| `band_bounds_m` | **[2.5, 9.0]** | null | null | `band_scale_at` (magnitude; R-BR-28) |
| `band_scales` | **[0.5, 1.0, 1.4]** | null | null | `band_scale_at` (magnitude; R-BR-28) |
| `impact_points_xy` | null | null | **24 [x,y] pairs** | the per-drop circle test |

`replica-frame/v1` and `g5-replay-trace/v1` both stay v1. No key removed, retyped or re-meant.

**`corridor_half_width_m` is a NEW field and deliberately not `hit_radius_m`.** Cell 1b refused to
put 0.42 there because a corridor half-width is not a disc radius. Doing so would have been the
**fifth** wrong-quantity field on this schema, committed by the cell chartered to stop that.

**`impact_points_xy` — the one field that could have been argued either way, so it was.**
R-WR3-23(6) refused per-prong positions (a closed form transports itself); R-WR3-25(10) admitted
`prong_count` (one record cannot determine it). Together: **derivable ⇒ refuse; not derivable ⇒
emit.** Drop positions are RNG draws, not per-frame (24 pairs once per cast, ~2.9 casts/fight).
Per-drop impact *time* is NOT emitted because it IS derivable from the volley-major ordering — which
is therefore **contractual**, and pinned by a test.

**NOT emitted, with reasons:** `explosion_radius_m` 1.5 (predicate-dead), `drop_variation_m`,
`wave_time_s` (= `range_m/v`), `dwell_s` (= `duration_s − range_m/v`).

---

## 3. ⚑ VERDICT ON `shape` — RULING EXECUTED, AND EXTENDED TO THE NOVA

**Ship `shape: "trapezoid"` for the wave: AGREED, no argument against.** The resolver evaluates a
linearly tapering lane; `rect` names a constant lateral extent. The error is front-loaded onto the
dodge band — 2.00× too wide at u = 0, 1.33× at u = 8, exact only at u = 16 where the player never
is. **Measured cost of the old reading: 18 false positives in 516 waves.**

**And the nova's `circle` is in the same position, so it ships `"star"` in the same breath.** It is
the bigger error of the two by the run's own measurement (48.5 % vs 3.5 %). `star` is the codebase's
own word and is fully determined by fields already present: `origin_*` + `radius_m` + `prong_count`
+ `spoke_offset_rad` + `corridor_half_width_m`.

**The blizzard KEEPS `circle`, and here is the argument rather than compliance.** Its `radius_m` 8.0
truthfully names the scatter disc — which genuinely is a disc, and genuinely is the support of the
danger — and its per-drop primitive genuinely is a circle test. It is the one family of the three
whose enum is not carrying the wrong primitive. Its remaining defect is that two circles live in one
record (`radius_m` 8.0 scatter vs `hit_radius_m` 1.32 lethal), which is a *naming* problem already
documented at the field, not a wrong-primitive problem. Whether `shape` should distinguish a
**multi-instance** primitive is a real question and is **routed to BR-3** rather than decided
unilaterally inside an emission-only cell.

**The rule this establishes:** `shape` names the geometry the resolver's predicate EVALUATES, not
the region the mechanic occupies.

`VALID_SHAPES` grows by two and **retains `rect` and `circle`** — removing a value from a frozenset
`validate()` consults would make the engine reject its own historical records on replay.

---

## 4. GATES

### G-1f — EMISSION PURITY: **PASS**, three limbs

**Limb 1 — control arm.** Battery regenerated at pre-change HEAD `28eddef4` and compared to the
banked cell-1b battery: **200 files, 90,708 records, the ONLY differing path is
`header.engine_git_hash`** (`5b8c724b` → `28eddef4`). Zero simulation paths. The intervening commit
`5b8c724b..28eddef4` is `AGENT_STATE.md` alone — 1 file, 0 code.

**Limb 2 — whole-battery path diff, post-change vs cell-1b.** 200 files, **90,708 records**:

| path | n | sample |
|---|---|---|
| `event[telegraph].start_width_m` | 1,556 | `<ABSENT>` → `None` / `3.0` |
| `event[telegraph].depth_m` | 1,556 | `<ABSENT>` → `None` / `1.0` |
| `event[telegraph].corridor_half_width_m` | 1,556 | `<ABSENT>` → `None` / `0.42` |
| `event[telegraph].band_bounds_m` | 1,556 | `<ABSENT>` → `None` / `[2.5, 9.0]` |
| `event[telegraph].band_scales` | 1,556 | `<ABSENT>` → `None` / `[0.5, 1.0, 1.4]` |
| `event[telegraph].impact_points_xy` | 1,556 | `<ABSENT>` → `None` / 24 pairs |
| **`event[telegraph].shape`** | **986** | `'rect'` → `'trapezoid'`, `'circle'` → `'star'` |
| `header.engine_git_hash` (provenance) | 200 | `'5b8c724b'` → `'16fa7e8d'` |

**No eighth simulation path in 90,708 records.** `unexpected_paths: []`. And
`expected_paths_that_did_NOT_move: []` — the instrument grades *missing* movement too, which is how
the `family` incident (dropped at the emitter, 0 of 13,573 records) would have shown.

⚑ **986 = 470 nova + 516 wave exactly. The blizzard's 570 `shape` values did not move** — the
argument in §3 is visible in the diff, not only in prose.

**Limb 3 — pick artifact.** `wr3_acc_pick.json` is **byte-identical** to the cell-1b artifact, and
the scan re-selects watch seed **74000909** (cornering 0.0000 | min-HP 0.6545 | intake/pool 0.5740 |
rule `PRIMARY_argmin_min_hp_among_uncornered`). **No RNG moved.**

### G-1g — COVERAGE AS COUNTS: **PASS**, 36/36 gates, 0 failing

Denominators: **nova 470 / wave 516 / blizzard 570 / 1,556 telegraphs / 90,708 records / 200 files.**

| gate | at value | null | `absent_key` | other values |
|---|---|---|---|---|
| `wave.start_width_m == 3.0` | 516/516 | 0 | **0** | {} |
| `wave.depth_m == 1.0` | 516/516 | 0 | **0** | {} |
| `nova.corridor_half_width_m == 0.42` | 470/470 | 0 | **0** | {} |
| `nova.band_bounds_m == [2.5, 9.0]` | 470/470 | 0 | **0** | {} |
| `nova.band_scales == [0.5, 1.0, 1.4]` | 470/470 | 0 | **0** | {} |
| `blizzard.impact_points_xy` len 24 | 570/570 | 0 | **0** | {} |
| `nova.shape == 'star'` | 470/470 | 0 | **0** | {} |
| `wave.shape == 'trapezoid'` | 516/516 | 0 | **0** | {} |
| `blizzard.shape == 'circle'` (unchanged) | 570/570 | 0 | **0** | {} |

**NULL ELSEWHERE, counted rather than inferred** (R-WR3-40(2) guard) — every cell `absent_key` **0**,
`non_null_values` empty:

| field | null on | null count |
|---|---|---|
| `start_width_m` | nova / blizzard | 470/470 · 570/570 |
| `depth_m` | nova / blizzard | 470/470 · 570/570 |
| `corridor_half_width_m` | wave / blizzard | 516/516 · 570/570 |
| `band_bounds_m` | wave / blizzard | 516/516 · 570/570 |
| `band_scales` | wave / blizzard | 516/516 · 570/570 |
| `impact_points_xy` | nova / wave | 470/470 · 516/516 |

**15 CARRIED controls from cells 1 and 1b all PASS** — `projectile_velocity_ms` (14.0 / 11.428571428571429 / 24.0), `prong_count` (16 / 6), `duration_s` (0.8571428571428571 / 1.4874999999999998 / 8.0), `stage_count` 4, `stage_interval_s` 2.0, `hit_radius_m` 1.32, `radius_m`, `range_m`, `width_m`. Nothing earlier moved.

### G-1h — PREDICATE RECONSTRUCTION: **PASS at 100 % on all four arms**

An independent function consuming **ONLY telegraph fields** — the module imports nothing from
`reincarnated`, asserted by a test that strips docstrings and comments before scanning, plus an
import-graph check — scored against the trace's own damage events:

| arm | TP | TN | FP | FN | unresolved | denominator | accuracy |
|---|---|---|---|---|---|---|---|
| **nova** | 240 | 226 | **0** | **0** | 4 | **470** | **100.000 %** |
| **wave** | 100 | 416 | **0** | **0** | 0 | **516** | **100.000 %** |
| **blizzard (telegraph)** | 156 | 414 | **0** | **0** | 0 | **570** | **100.000 %** |
| **blizzard (drop)** | 186 | 13,494 | **0** | **0** | 0 | **13,680** | **100.000 %** |

**FP 0 and FN 0 on every arm. No residual. The fallback was not needed and nothing is rounded up.**

The 4 nova `unresolved` are telegraphs whose ring never crossed — the boss died inside the window.
They are counted in the denominator and reported separately rather than dropped.

**Nova miss decomposition: 226 through a prong gap, 0 beyond `radius_m`.**

⚑ **The gate carries its own degenerate-predictor tripwire and it FIRED during development.** An
"always miss" predictor scores 48 % on the nova, 81 % on the wave and 98.6 % at drop level — all
three read like passes if you only look at accuracy. The instrument raises if TP or TN is zero on
any arm; on a 3-seed smoke it correctly refused to report (`wave TP=0`).

### G-9 — PUSH TRUTH

Verified on `origin/main` — see §7.

---

## 5. SMOKE + REGRESSION

- **20/20** new tests in `tests/test_br2_resolve_truth_1.py`, including reconstruction-vs-resolver
  agreement on **20,000 random wave configurations**, **50,000 random nova crossings** and 20,000
  blizzard drop tests, and **three ablations asserted as FAILURES** (uniform width, depth 0,
  disc-instead-of-corridors) so a non-load-bearing field could not pass unnoticed.
- **3,699 targeted tests PASS** across all 8 telegraph/simulation/WR modules.
- **Full suite, post-change (`16fa7e8d`): `63 failed, 10068 passed, 21 errors` in 21:08.**
  The pre-existing baseline is `63 failed, 10048 passed, 21 errors`. **Same 63, same 21 — and
  `+20` passed, which is exactly this cell's new module.** No test changed state from pass to fail.
- **The failures were controlled where it matters, not assumed away.** Of the 63, three modules sit
  in this change's blast radius. All were re-run at pre-change HEAD `28eddef4` in a clean worktree
  and fail **identically, test-ID for test-ID**:

  | module | failing IDs at `16fa7e8d` | at `28eddef4` |
  |---|---|---|
  | `test_wr2_d_nova_telegraph.py` | 2 (`..._DERIVED_duration_under_the_arm`, `..._MEASURED_0_750_off_the_arm_H_M2_f`) | **same 2** |
  | `test_wr1_m12_gd_mitigation_nova.py` | 1 (`..._nova_fires_telegraphs_and_lands_a_death2_class_blow`) | **same 1** |
  | `test_kit_space_emitter.py` | 4 (`TestMultiKitEmit::*`) | **same 4** |

  The remaining 56 are in rocket's generation seam (`test_cycle12_layer4_convergence` 33,
  `test_cycle12_layer6_t4_wireup` 12, `test_foundation` 4, and seven singletons) — the first of
  which was independently traced to `generation/skill_tree.py:422 NotImplementedError` on a stashed
  tree before any of this cell's edits existed.

⚑ **And the strongest non-regression evidence is not the suite at all — it is G-1f limb 2.** A
byte-level path diff over **90,708 records** proves that no simulation path moved. A test suite
samples behaviour; that diff enumerates it.

⚑ **Two scope guardrails from cells 1 and 1b fired on `start_width_m` and did exactly their job.**
Both were **inverted, not deleted**, citing charter § ADDENDUM 4 — a deleted assertion leaves no
record that the gap was ever fenced, and the fence is why the fill needed a ruling at all.

---

## 6. ⚑ SELF-CAUGHT, ON RECORD

**`PRIMORDIAN_FRIGIDRING` is the rank-4 PRE-stage-2 nova. Its `hit_half_width` is 1.5 — the splash.**
The shipping object is **`PRIMORDIAN_FRIGIDRING_STAR_R5`** (0.42). One suffix apart; the hit test
differs by **3.57×**. Emission was never affected — every site reads `p.hit_half_width` off whichever
params object the resolver holds — but my first test draft reached for the obvious name and would
have measured the retired mechanic while calling it the shipping one. Caught by this cell's own value
pins on their first run. Both objects are now pinned by an assertion, and MIGRATION §6 warns
consumers.

---

## 7. BR-3 FINDINGS (logged, not fixed — the run does not move its own goalposts)

1. **⚑ THE BODY-RADIUS ASYMMETRY.** Three families, two conventions, in one boss's kit. The wave adds
   the **live target's** `entity_radius` (`gd_boss_kit.py:680`, `:688`); the nova and the blizzard
   bake the **referent's** 0.32 m into their constants (0.42 = 0.10 + 0.32; 1.32 = 1.0 + 0.32). On
   this fixture the player's radius is **0.5**, so the nova and blizzard resolve against a body
   0.18 m smaller than the one the sim is simulating. Does not affect any gate here (the
   reconstruction replicates whatever the resolver does) and is **not touched** — changing it moves
   outcomes, and this cell is emission-only. Pinned by a test so a future reconciliation is deliberate.
2. **A stale derived constant.** `n_bounds`'s docstring (`gd_nova.py:629`) gives the gapless boundary
   as **7.6890 m**. That is `1.5/sin(π/16)` — the *pre-stage-2* blast. The shipping value is
   **2.1528 m**. Code correct, prose stale.
3. **Should `shape` distinguish a multi-instance primitive?** (§3). The blizzard's `circle` covers 24
   discs. Held deliberately; a conductor question.
4. **`damage_amount` is a single preview scalar** on a mechanic with three distance bands and a
   variable prong count. Hit/no-hit is now fully reconstructible; delivered **magnitude** is not.
   `band_bounds_m`/`band_scales` are the first half; the per-prong payload basis is the second.
5. **The nova's DAMAGE-event `geometry` still reads `"circle"`** (`spatial_engine.py`, `_rx(...)`),
   which is the same misnaming one vocabulary over. **Not changed here** — `wr3_cell_kc_2026_07_30.py:688`
   reads it and changing it would move a graded measurement.

---

## 8. WHAT THIS CHANGES FOR THE RENDERER

1. **Draw the nova as 16 lanes, not a disc.** `spoke_offset_rad` (already shipped) says exactly which
   16. The gaps are safe and they are ~2/3 of the footprint by area, ~48.5 % by outcome.
2. **Shade the nova's danger INVERTED from intuition** — ×0.50 inside 2.5 m, ×1.40 at the rim.
3. **Draw the wave as a trapezoid** 3.0 → 6.0 over 16.0 m, lethal only in a 1.0 m band behind the
   front. The sweep is `range_m / projectile_velocity_ms` = 1.4 s, **not** `duration_s` 1.4875.
4. **Draw the blizzard as 24 discs of 1.32 m at the emitted points**, not an 8 m circle. 98.6 % of
   the scatter disc is harmless at any instant.
5. **Match on `family`, never on `shape`.** Two `shape` values changed.
6. **Add the player's radius to `start_width_m`/`width_m`; do NOT add it to `hit_radius_m` or
   `corridor_half_width_m`.**

---

## 9. ARTIFACTS

- Battery of record: `~/Games/reincarnated-godot/tmp/wr3acc/traces/` (200 traces, stamped `16fa7e8d`)
- Preserved: `traces_CELL1B_5b8c724b/`, `traces_CELL1_bce46fd9/`, `traces_PREFILL_ddbdebc8/`
- Control arm: `~/Games/reincarnated-godot/tmp/wr3acc_CTRL_28eddef4/`
- As-generated: `~/Games/reincarnated-godot/tmp/wr3acc_br2resolve/`
- Pick artifacts: `wr3_acc_pick_BR2RESOLVE.json` (byte-identical to `wr3_acc_pick_BR2STAGE.json`)
- Gate instrument: `reincarnated-engine/src/reincarnated/simulation/notes/br2_resolve_truth_1_gates_2026_08_01.py` (`battery` / `cover` / `rebuild`)
- Generator: drax's `reincarnated-godot/scripts/wr3_acc_pick_scan.py --out <dir>`, **UNMODIFIED**
- No tracked file in `reincarnated-godot/` was touched (drax's ARSENAL-2 contention respected).
