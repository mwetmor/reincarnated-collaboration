# RUN KC2-PM4 — LAP S — THE ARENA-AND-ADVANCE DECODE

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Fired under:** R-PM4-44 part 3 (ledger rows L-34, L-35) · **Date:** 2026-08-14
**Discipline:** GL-12 DECODE-NEVER-ESTIMATE · outcome-firewalled · NOTE-9 basis on every number ·
FULL 64-hex sha256 on every input and output · read-only on every external source.

**Pre-registration:** `PREREGISTRATION.md`, sha256
`68f4e3a35ca7fdf4a2808f2bf3af16b3f1a2c13c6fbd7b6be65cf2115522af59`, written and hashed
**2026-08-14T15:23:39Z — before any instrument ran.** Every threshold and every verdict rule used
below appears there. Reconnaissance that preceded the hash is declared in its § 0. Two departures
are declared in § 7 of this file, both self-caught.

---

## 0. HEADLINE — the run's geometry residual is NOT the radius

| # | finding | number |
|---|---|---|
| **1** | **⚑ THE SIM'S 45.06 m SPAWN RADIUS IS NOT WRONG IN MAGNITUDE.** Decoded from the Crucible's own world assets: the six tier-16 spawn points sit a **median 37.03 m** (range **3.56 – 51.42 m**, n = 114 over 20 arenas) from their arena's patrol-point centroid. A uniform disc of radius 45.06 m has mean radius **30.04 m**. **The two agree to ~20 %.** The run's working story — *"the sim's arena is bigger and emptier than the one Matt played"* — **is not supported by the game's own geometry.** | game median **37.03 m** vs sim-disc mean **30.04 m** |
| **2** | **⚑ WHAT IS WRONG IS THE SHAPE.** The game dispenses each wave from **6 FIXED points**, each scattering its pack within **`placementExtents = 8.0` m** (uniform on all 54 tier-16 proxies), and then **links every non-ambush pack to `PatrolPoint_Attack`** so it *converges on a named attack-point group* (8–11 patrol points per arena). The sim scatters bodies **independently and uniformly over a disc**. Same mean distance; completely different arrival structure. | **6 packs × 8.0 m**, converging — not a 45 m disc |
| **3** | **⚑ THE WAVE-ADVANCE RULE, DECODED VERBATIM FROM SHIPPED LUA SOURCE.** A wave advances when **every spawn point's PROXY reports `AllKilled()`**, evaluated on a **1000 ms poll**, and a spawn point whose wave entry is `nil` is marked killed **immediately, without spawning**. The gate is **six proxy booleans over proxy-DISPENSED bodies** — traps are created outside any proxy and do not gate; runtime summons were never placed by a proxy and cannot be in its placed-ID list. **The sim's gate on ALL deaths, including 12 unkillable-by-design summons, has no counterpart in the shipped rule.** | 6 booleans, **1000 ms poll** |
| **4** | **⚑ WAVE 154 IS THE ONLY WAVE IN THE TIER WITH FOUR ACTIVE SPAWN POINTS.** `tier16waves.lua` has `{nil}` on both p05 and p06 for wave index 04. **The referent's 14.20 s w154 is a smaller wave by authorship, not a behavioural anomaly.** | **4 of 6** gating proxies |
| **5** | **⚑ `characterRunSpeedJitter` IS AUTHORED AND UNCONSUMED.** The transform is fully decoded (one-shot, load-time, two-sided multiplicative uniform `v·(1 + (J/100)(2u−1))`, MINSTD/Schrage). But **no shipped module contains the field's name literal**, while its own sibling `characterRunSpeed`, both other `*Jitter` fields, and five positive controls all do — and there is **no standalone `"Jitter\0"`** literal for runtime name construction either. **DO NOT FOLD IT.** | literal present in **NONE** |
| **6** | **THE REFERENT'S CAMERA CANNOT SEE 45 m.** The farthest a nameplate ever appears is **1385.5 gpx = 11.08 – 11.64 m**; the frustum's tightest geometric limit is **798.9 gpx = 6.39 – 6.71 m**. First-appearance radius is therefore **RIGHT-CENSORED** and can never *refute* a spawn radius — which is exactly why limb (a)'s world-asset decode, not limb (b), carries finding 1. | max ever seen **11.6 m** |

**The shape, in one sentence.** Lap R found the referent's dryness differs from the sim's in
*granularity* rather than amount; **Lap S finds the same thing one level down — the spawn geometry
differs in STRUCTURE rather than SCALE.** Six converging packs at a correct mean distance is not
the same fight as a uniform disc at a correct mean distance, and the run has been pricing the
wrong quantity.

---

## 1. Inputs — every one re-hashed before use (GL-6)

| input | sha256 (FULL 64-hex) | verdict |
|---|---|---|
| `…/lap-r-locomotion-contact/method/plates60_lapH2.npy` | `28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df` | **EXACT** |
| `…/lap-h2-video-match/method/camera_translation_60fps_683-866.npy` | `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33` | **EXACT** |
| `PREREGISTRATION.md` | `68f4e3a35ca7fdf4a2808f2bf3af16b3f1a2c13c6fbd7b6be65cf2115522af59` | **EXACT** |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` | recorded |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` | recorded |
| `vendor/grim-dawn/Grim Dawn.exe` | `1a71e188ea3d7f83bec296e22acecf7cac71686c9c0c117d0eb03c9d7ada1ff4` | recorded |
| `…/survivalmode1/resources/Maps.arc` | `2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237` | recorded |
| `…/survivalmode2/resources/Maps.arc` | `cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec` | recorded |
| `…/survivalmode3/resources/Maps.arc` | `94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911` | recorded |

Referent video (read-only, never modified):
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`
Record + world corpus (read-only): `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/`
Shipped binaries (read-only): `/Users/admin/Games/vendor/grim-dawn/`

**Carried constants, each with its emitting lap named (NOTE-9):** `K = 0.537` (`OBS-H2-8`) ·
player plate anchor `(960, 429)` (Lap R) · px→m **bracket `[119.0, 125.0]` gpx/m**, both edges
always (`U-R-1` / R-PM4-43 part 2) · wave boundaries ±0.25 s (`OBS-H2-6`) · fight 683.0–864.0 s.

---

## 2. LIMB (a) — CRUCIBLE SPAWN GEOMETRY. Lap R's `UNREACHED-1`, **CLOSED.**

### 2.1 The format, mapped from the bytes

Lap R probed five `.arz` record paths and correctly found none; the geometry is in `.map` world
assets. Those assets ship in ARC containers the run had not opened:
`survivalmode{1,2,3}/resources/Maps.arc → survivalworld_{a..j}.map`.

Format decoded first-of-kind for this project, from the bytes alone (no public spec used):

```
magic       b'MAP\t'
…           head section (inline `Patrol Points` group), LVL region blocks
STRING TABLE  contiguous run of  u32 len | printable-ASCII `.dbr` path
u32           placement_count
PLACEMENT[]   9 × f32 row-major 3×3 ROTATION | 3 × f32 WORLD POSITION (x, y, z)
              | u32 | u32 string-table INDEX                        = 56 bytes
```

Records are accepted **only** where the nine leading floats form an orthonormal-row matrix (row
norms ∈ [0.98, 1.02]) and the index is in range; unrecognised bytes advance by 4 and retry. The
reader therefore **under-reports rather than inventing placements**, and the parsed/declared ratio
is emitted per map so any shortfall is visible: **11 of 20 maps parse 100 %**, and the worst is
`survivalmode1:survivalworld_g` at **97.67 %** — no map falls below it.

**Validation, declared in the pre-registration and passed on all 20 maps:** the `y` component is
the vertical axis (`y-span ≪ x-span` and `y-span ≪ z-span` — e.g. `survivalworld_c`: y 32.4 vs
x 127.2, z 126.9). Ground distances are computed in the (x, z) plane.

**Units.** GD world units are metres on Lap F's scale (`actorRadius = 0.32` on the player;
`eyeofreckoning1 :: skillTargetRadius = 3.0`). **This is the only limb of Lap S that carries no
px→m bracket — it is already metric.**

### 2.2 The spawn set for waves 151–160

`eventcontrol.lua` routes `rewardTier = floor(wave/10) = 15 → tier16Waves` (§ `pm4s_wave_advance.md`
§ 1). `tier16waves.lua` binds spawn point 1 via `SurvivalEvent_OnAddToWorld`; the world assets carry
one **tier-specific** primary spawn point per tier plus five shared secondaries:

`records/scriptentities/tier16spawnpoint01.dbr` (+ `tier01..tier17` siblings) ·
`spawnpoint02` · `spawnpoint03` · `spawnpoint04` · `spawnpoint05` · `spawnpoint06`

All positions are in `pm4s_arena_placements.csv` (1,079 rows over 20 arenas).

### 2.3 ⚑ The decidable comparison

| arena (survivalmode : map) | spawn pts | patrol pts | spawn→patrol-centroid min / med / max (m) | spawn→NEAREST patrol, med (m) | spawn pairwise max (m) |
|---|---:|---:|---|---:|---:|
| sm1 : survivalworld_a | 6 | 11 | 9.78 / 30.49 / 38.34 | 14.48 | 65.72 |
| sm1 : survivalworld_b | 6 | 11 | 12.43 / 36.09 / 42.14 | 19.64 | 77.24 |
| sm1 : survivalworld_c | 5 | 10 | 29.58 / 39.64 / 48.89 | 10.28 | 76.66 |
| sm1 : survivalworld_d | 4 | 11 | 35.54 / 39.05 / 44.14 | 19.07 | 69.79 |
| sm1 : survivalworld_e | 5 | 10 | 27.79 / 36.82 / 43.43 | 17.32 | 81.30 |
| sm1 : survivalworld_f | 6 | 11 | 13.10 / 35.75 / 43.04 | 12.18 | 79.82 |
| sm1 : survivalworld_g | 6 | 10 | 6.27 / 37.22 / 43.96 | 18.56 | 74.29 |
| sm1 : survivalworld_j | 6 | 9 | 13.13 / 43.87 / 48.01 | 17.07 | 84.92 |
| sm2 : survivalworld_h | 6 | 9 | 20.59 / 43.07 / 50.04 | 18.31 | 77.39 |
| sm2 : survivalworld_i | 6 | 9 | 3.56 / 38.30 / 39.77 | 17.89 | 76.07 |
| sm3 : survivalworld_a | 6 | 9 | 13.97 / 33.36 / 37.04 | 12.63 | 65.02 |
| sm3 : survivalworld_b | 6 | 9 | 10.30 / 35.27 / 40.04 | 16.99 | 73.86 |
| sm3 : survivalworld_c | 6 | 11 | 12.13 / 29.72 / 39.33 | 10.51 | 59.21 |
| sm3 : survivalworld_d | 6 | 11 | 10.49 / 35.70 / 41.03 | 11.37 | 69.79 |
| sm3 : survivalworld_e | 5 | 11 | 32.84 / 37.55 / 41.39 | 19.65 | 76.33 |
| sm3 : survivalworld_f | 5 | 10 | 14.24 / 42.64 / 44.11 | 6.57 | 85.37 |
| sm3 : survivalworld_g | 6 | 8 | 13.69 / 35.88 / 51.42 | 22.82 | 77.92 |
| sm3 : survivalworld_h | 6 | 9 | 16.50 / 40.72 / 47.91 | 18.31 | 77.39 |
| sm3 : survivalworld_i | 6 | 9 | 4.11 / 37.56 / 41.23 | 18.61 | 77.97 |
| sm3 : survivalworld_j | 6 | 8 | 20.66 / 44.07 / 49.35 | 16.99 | 84.86 |

**Pooled, n = 114 spawn points over 20 arenas:**

| quantity | min | median | mean | max |
|---|---:|---:|---:|---:|
| spawn point → patrol-point **centroid** | 3.56 | **37.03** | **34.36** | 51.42 |
| spawn point → **nearest** patrol point | 0.65 | **17.07** | 16.09 | 37.51 |

**Against the sim.** A uniform disc of radius **45.06 m** has mean radius **30.04 m** and median
radius **31.86 m**.

> **⚑ THE SIM'S SPAWN DISTANCE IS RIGHT AND ITS SPAWN STRUCTURE IS WRONG.** 34.36 m measured mean
> vs 30.04 m modelled mean is a **14 % gap** — and the sim's is the *smaller* one, so the sim is not
> even scattering bodies too far. **Every metre of the run's geometry residual has to come from
> structure, because the scale has now been measured and it agrees.**

### 2.4 The scatter constant, and the convergence policy

| term | value | basis |
|---|---|---|
| **`placementExtents`** | **8.0** on **all 54** tier-16 selector proxies (47 `Proxy` + 7 `ProxyAmbush`) | `records/proxies/tier16waves/proxy_wNN_pMMa.dbr`, `.arz`, whole-record replacement |
| corpus-wide mode | **8.0 (1254 / 2349 proxies)** | corpus census, all `records/proxies/**` |
| **patrol-point group** | **`PatrolPoint_Attack`** | `tier16waves.lua :: survivalModeEventParameters.patrolPoint` |
| linkage | `proxy:LinkPatrolPointGroup(waveEvent.patrolPoint)` on every non-ambush proxy | `survivalevent.lua :: SurvivalEvent_SpawnNext` |
| patrol points per arena | **8 – 11** | `.map` placements |
| patrol-ring radius about its own centroid | **1.3 – 45.0 m** (per-arena max 19.1 – 45.0) | `pm4s_arena_geometry.json` |

**So the referent's per-wave spatial process is:** 4–6 packs, each dispensed inside an **8.0 m**
disc about a fixed point ~37 m from the arena's attack ring, each pack then **pathing as a group to
a named attack-point set**. The sim's is: N bodies, independent, uniform on a 45.06 m disc, each
seeking. **Those are different processes with the same first moment.**

---

## 3. LIMB (b) — THE VIDEO-GEOMETRY LIMB

10,216 instants carry a detected player plate in 683.0–864.0 s; they contain **91,165 living
monster plates**. Instants without a player plate are EXCLUDED, never imputed (Lap R's rule).

### 3.1 ⚑ Frustum limit — why this limb cannot carry the headline

| limit | ground px | metres @125 (HI) | metres @119 (LO) |
|---|---:|---:|---:|
| geometric, left / right | 960.0 | 7.68 | 8.07 |
| geometric, **up (tightest)** | **798.9** | **6.39** | **6.71** |
| geometric, down | 1212.3 | 9.70 | 10.19 |
| **empirical, farthest plate EVER observed** | **1385.5** | **11.08** | **11.64** |
| empirical, p99 of all plate radii | 1144.7 | 9.16 | 9.62 |

**Pre-registered verdict `V-B1`: the frustum limit is < 45.06 m at BOTH bracket edges. MEASURED.**
The referent's camera **cannot contain a body at the sim's spawn radius** — the farthest body ever
rendered is **3.9× closer** than 45.06 m. The first-appearance distribution is therefore
**RIGHT-CENSORED**, and I pre-committed to never quoting a percentile from it without that
attached. **This is why finding 1 rests on limb (a) and not on this limb.**

### 3.2 First-appearance radius

PRIMARY tracker (`G_MAX = 60`, `N_MIN = 6`, `H_GAP = 6`): **3,324 tracks**.

| statistic | ground px | metres @125 | metres @119 |
|---|---:|---:|---:|
| median birth radius | 306.1 | 2.449 | 2.572 |
| **p95 (pre-registered comparator `V-B3`)** | 1058.0 | 8.464 | **8.891** |
| max | 1382.0 | 11.056 | 11.614 |
| fraction of births at ≥95 % of the frustum limit | — | **0.1273** | — |

**Full 27-cell sweep published** (`pm4s_video.json → first_appearance_sweep`). The headline is
**stable across it**: p95 runs 7.87 – 9.28 m over all 27 parameter combinations — a **±8 %** band
against a **5.07×** gap to 45.06 m. **No verdict here is sweep-dependent.**

**Read honestly:** 87 % of nameplate births occur *inside* the frustum rather than at its edge, so
most bodies become visible near the player rather than walking in from the screen edge. That is
**consistent with** the decoded 8.0 m pack scatter plus patrol convergence — but it is
**confounded** by occlusion and VFX blink (a plate can be born mid-screen because the plate
reappeared, not because the body did). **It is offered as consistent, not as proof.**

### 3.3 Arena bounds — **INDICATIVE, and a self-caught retraction**

| quantity | ground px | metres @125 | metres @119 |
|---|---:|---:|---:|
| player trajectory bbox | 1250 × 2581 | — | — |
| player trajectory **diagonal** | 2867 | 22.94 | 24.09 |
| entity-cloud diagonal (conservative sign convention) | 4692 | 37.54 | **39.43** |
| entity-cloud diagonal (other sign convention) | 5154 | 41.23 | 43.31 |

**⚑ `D-S-1` — I am retracting my own pre-registered bound-direction claim.** PREREGISTRATION § 3.0
asserted that "the hull of observed positions is a strict LOWER bound on arena extent." That is
true of *exactly measured* positions. The player trajectory here is **not measured — it is
INTEGRATED**, by cumulative sum of 11,024 per-frame phase-correlation displacements. Integration
error accumulates as a random walk, and added noise **inflates** a max-minus-min extent in
expectation. **So the hull is an over-estimate, not a lower bound.** No number changed; the claim
about the numbers did. Graded **INDICATIVE**.

The retraction does not cost the finding, because the bias is **signed and in the useful
direction**: the true entity-cloud diameter is **≤ 39.43 m**, i.e. *the sim's spawn RADIUS alone
(45.06 m) exceeds the referent's entire drift-INFLATED entity-cloud DIAMETER.* That is the exact
strong form pre-registered at `V-B2`, and it holds at both bracket edges.

**But note the tension with § 2.3, and I am not hiding it.** The world assets say spawn points are
~37 m from the attack ring and up to 85 m apart; the video's entity cloud spans ≤ 39 m. **Both can
be true only if the player never traverses the full arena** — which Lap H-2/R support (the camera
is player-locked, the player fights where the packs converge, and bodies are only ever visible
within ~11.6 m). **The video measures the fight's footprint; the world assets measure the arena.
They are different quantities and this lap keeps them apart.**

### 3.4 Per-wave arrival curves

| wave | span (s) | peak plates | t(peak) | t→50 % peak | t→90 % peak | plates at increment | min |
|---|---:|---:|---:|---:|---:|---:|---:|
| 151 | 15.60 | 24 | 3.950 | 3.050 | 3.950 | 6 | 0 |
| 152 | 16.30 | 20 | 4.317 | 0.283 | 4.317 | 2 | 1 |
| 153 | 14.90 | 25 | 5.817 | 3.850 | 5.417 | 1 | 0 |
| **154** | **14.20** | 28 | 7.650 | 3.417 | 4.067 | 1 | 0 |
| 155 | 16.20 | 19 | 4.567 | 3.883 | 4.517 | 3 | 0 |
| 156 | 20.20 | 25 | 6.383 | 2.767 | 5.883 | 2 | 0 |
| 157 | 19.30 | 36 | 7.550 | 5.033 | 7.417 | 1 | 0 |
| 158 | 13.00 | 26 | 4.117 | 1.717 | 4.117 | 3 | 0 |
| 159 | 26.30 | 29 | 9.550 | 6.200 | 9.050 | 3 | 0 |
| 160 | 25.00 | 25 | 12.033 | 3.117 | 12.033 | 2 | 0 |

**⚑ The board BUILDS, it does not appear.** Median time to 90 % of a wave's peak plate count is
**4.97 s**; median time to 50 % is **3.27 s**. A wave is not instantly present and it is not a
steady trickle — it **ramps over ~4–6 s and then drains**, which is the signature of packs
marching from fixed points, and it is a directly foldable curve.

---

## 4. LIMB (c) — THE WAVE-ADVANCE RULE

**Full decode, verbatim source, and the five consequences: `pm4s_wave_advance.md`.** Summary:

- **MEASURED:** advance requires **all spawn-point proxies `AllKilled()`**, polled every **1000 ms**;
  `nil` wave entries never gate; spawn point 6 is bonus-gated; the wave counter increments **inside**
  `SpawnNext`, i.e. it is a **spawn** event.
- **MEASURED:** **wave 154 has only 4 active spawn points** — the only such wave in tier 16.
- **INFERRED-WITH-EVIDENCE:** runtime summons are not proxy-placed and therefore cannot gate.
  Traps are `Character.Create`'d outside any proxy and demonstrably do not gate (**MEASURED**).
- **UNREACHED:** the body of `Proxy::AllKilled()` — its Lua binding lives in `Grim Dawn.exe`, which
  ships a **`.bind` section (Steam DRM)** with encrypted `.text`. `Game.dll`/`Engine.dll` are
  unprotected and were disassembled freely. **Recorded, not estimated.**
- **Video arm, pre-registered `V-C1`: NOT FALSIFIED at every Δ ∈ {1, 3, 5} s** — 6 of 9 increments
  show a demonstrably empty board in the preceding 3 s, which is what an all-proxies-killed gate
  predicts. Globally the board is empty for only **3.00 s of 181 s (1.76 %)**. **Two independent
  instruments, one answer.**

---

## 5. LIMB (d) — `characterRunSpeedJitter`

**Full decode: `pm4s_jitter_law.md`.** Summary: the law is
`v' = max(0, v·(1 + (J/100)(2u−1)))`, `u = seed·2⁻³¹`, MINSTD/Schrage — **one-shot at load, two-sided,
multiplicative percentage, clamped at zero, and `J = 0` does not even advance the RNG.** All of
d3/d4/d5 are **MEASURED** (disassembled), which satisfies my PREREGISTRATION § 5 pre-commitment.

**And it does not matter, because `d6` is a MEASURED-NEGATIVE:** no shipped module carries the
field's name literal, while its own sibling `characterRunSpeed`, both other corpus `*Jitter`
fields, and five positive controls all do; and there are **zero standalone `"Jitter\0"` literals**
in any module, closing the runtime-name-construction escape.

> **⚑ `C-I18-1`: DO NOT FOLD. Gamora's refusal stands — now decoded rather than undecoded.**

---

## 6. What I am handing the conductor for I-19

| # | foldable term | value | grade |
|---|---|---|---|
| **F-1** | spawn points per wave, tier 16 | **6 declared; 4–6 active per wave; wave 154 = 4** | MEASURED |
| **F-2** | per-pack spawn scatter | **`placementExtents = 8.0` m**, uniform on all 54 tier-16 proxies | MEASURED |
| **F-3** | spawn-point → attack-ring distance | **median 37.03 m** (min 3.56, mean 34.36, max 51.42; n = 114) | MEASURED |
| **F-4** | spawn-point → **nearest** patrol point | **median 17.07 m** (min 0.65, max 37.51) | MEASURED |
| **F-5** | spawn-point pairwise max separation | **59.2 – 85.4 m** per arena | MEASURED |
| **F-6** | movement policy of spawned packs | **converge on `PatrolPoint_Attack` group** (8–11 points/arena), NOT per-body player-seek | MEASURED |
| **F-7** | wave-advance rule | **all spawn-point proxies `AllKilled()`, polled at 1000 ms**; `nil` entries never gate | MEASURED |
| **F-8** | advance latency floor | **U(0, 1] s** poll quantisation on top of the last kill | MEASURED |
| **F-9** | summons in the advance gate | **excluded** (not proxy-placed) | INFERRED-WITH-EVIDENCE |
| **F-10** | wave arrival ramp | median **t→50 % peak 3.27 s**, **t→90 % peak 4.97 s** | MEASURED (plate counts = lower bounds) |
| **F-11** | `characterRunSpeedJitter` | **DO NOT FOLD** — authored, unconsumed | MEASURED-NEGATIVE |
| **F-12** | spawn beacons | exist, 5 per arena, sit **0.36 m** from spawn points, shipped comment: *"accelerate monster movement in their spawn areas"* — **magnitude UNREACHED** | NAMED, NOT QUANTIFIED |

---

## 7. Departures from the pre-registration — both self-caught, both reported

**⚑ `D-S-1` — the arena-hull bound direction was WRONG and I retract it.** See § 3.3. The
pre-registration called the observed-position hull "a strict LOWER bound on arena extent"; the
trajectory is integrated, not measured, and integration drift **inflates** extent. The quantity is
regraded **INDICATIVE** and the `V-B2` refutation is stated only in its pre-registered strong form,
which survives because the bias is signed in the useful direction. **No number changed.**

**⚑ `D-S-2` — one instrument bug and one test bug, both caught by my own hand before any finding
was drawn, both repaired, both reported.**
(1) The PE32 export-directory header was unpacked with **10 fields instead of 11** — the `Name RVA`
at +12 was dropped, which silently produced 12,033 "exports" whose names were raw x86 byte strings.
Caught because the "export names" were obviously machine code. Repaired ⇒ **25,091** real exports;
the corrected reader carries a comment saying why.
(2) The `d6` runtime-name-construction test `b"Jitter\0" in blob` is a **false positive** — it
matches the tail of `lootRandomizerJitter\0` and returned TRUE on all three modules. The corrected
test requires the preceding byte to be a non-identifier character, and returns **0 on all three**.
**The MEASURED-NEGATIVE in § 5 rests on the corrected test only.**

**Out-of-pre-registration addition, declared:** PREREGISTRATION § 2 anticipated the `.map` decode
might fail and named UNREACHED as the honest landing. It did not fail, and the placement-array
format decode (§ 2.1) is consequently work the pre-registration did not specify in detail. It is
reported with its validation criteria (orthonormality gate, parsed/declared ratio, vertical-axis
check) stated **as constraints the reader enforces**, not as post-hoc justification.

---

## 8. UNREACHED census

| # | term | status |
|---|---|---|
| **UNREACHED-S1** | **the body of `Proxy::AllKilled()`** | **UNREACHED.** Lua binding lives in `Grim Dawn.exe`; that module ships a `.bind` section (Steam DRM) and its `.text` is encrypted at rest. The binding NAME table is readable in plaintext `.rdata`; the implementation is not. Not estimated. |
| **UNREACHED-S2** | **the spawn beacon's speed magnitude** | **UNREACHED.** `records/creatures/traps/spawnbeacon.dbr` exists and is placed 5× per arena; its effect is documented only by a shipped Lua comment. The record's aura/skill chain was not walked this lap. |
| **UNREACHED-S3** | **which arena Matt actually played** | **UNREACHED.** 20 arena variants carry a tier-16 spawn set; the referent's frames were not matched to a specific `survivalworld_*`. All limb-(a) numbers are therefore reported as **distributions over all 20**, never as a single arena's value. |
| **UNREACHED-S4** | **whether a nameplate birth is a genuine spawn or a re-appearance** | **UNREACHED and structural.** Occlusion and VFX saturation both extinguish and restore plates. § 3.2's "87 % born inside the frustum" is consistent-with, not proof-of. |
| **UNREACHED-S5** | **true spawn distance from video** | **UNREACHED by construction** — right-censored at the frustum limit (§ 3.1). Closed instead by limb (a) from world assets. |
| **UNREACHED-S6** | **whether a body present at a wave increment is new-wave or straggler** | **UNREACHED.** Carried unchanged from Lap R `UNREACHED-5`; the plate census has no wave identity per body. |
| **UNREACHED-S7** | **`bonusSpawnStatus` at each wave in the referent** | **UNREACHED.** Spawn point 6 is gated on `gd.survival.rewards.checkBonusStatus()`, whose per-wave state in Matt's run is not observable from the frames. Active-spawn-point counts are therefore given as **ranges** (4–6) in `pm4s_wave_advance.md` § 3. |
| **UNREACHED-S8** | **`.lvl` region contents** | **UNREACHED.** `Maps/Region_Survival_*.lvl` are referenced by the `.map` but were not opened; terrain walls and pathing blockers are therefore not measured, so no arena *boundary* (as opposed to entity extent) is claimed anywhere in this lap. |

---

## 9. UNDECIDED / uncertain terms — for the conductor's bracket accounting

| # | term | why undecided | what would decide it |
|---|---|---|---|
| **U-S-1** | **which arena's geometry to fold.** Spawn→centroid median ranges 29.7 – 44.1 m across the 20 arenas. | `UNREACHED-S3`. I publish all 20 and impose none. | matching a referent frame to an arena's terrain, or Matt naming the arena |
| **U-S-2** | **whether "spawn → patrol centroid" or "spawn → nearest patrol point" is the right comparator to the sim's spawn radius.** They differ by **2.2×** (37.03 vs 17.07 m median). | The sim's radius is measured from the *player*; the game's packs march to an attack *ring*, and the player is somewhere on or inside it. Neither is the player. **Both published; neither ruled.** | a decoded relation between `PatrolPoint_Attack` occupancy and player position, which pixels cannot give |
| **U-S-3** | **the entity-hull / world-asset tension** (§ 3.3): video footprint ≤ 39.4 m vs arena spawn separation up to 85.4 m. | Most plausibly the player never traverses the arena, but drift makes the video number an over-estimate and `UNREACHED-S8` means the arena boundary is unmeasured. **Named, not resolved.** | a drift-corrected trajectory (loop-closure on a landmark), or the `.lvl` decode |
| **U-S-4** | **whether patrol-point convergence is a per-pack group path or a per-body destination.** | `LinkPatrolPointGroup` is decoded; the pathing semantics of a linked group are in the DRM'd exe. | `UNREACHED-S1`'s blocker, same cause |
| **U-S-5** | **px→m bracket `[119.0, 125.0]`** | carried unchanged from `U-R-1` / R-PM4-43 part 2; **not re-opened and not narrowed here.** Note limb (a) does not use it at all — the world assets are already metric, so **finding 1 is bracket-free.** | Lap R's `U-R-1` conditions, unchanged |

**Carried unchanged from prior laps:** `U-R-1` … `U-R-6` · `OBS-H2-3` · `OBS-H2-9` ·
Lap N § A.6 · Lap R `UNREACHED-5` (= `UNREACHED-S6`).

---

## 10. What this lap did NOT do — the firewall, stated

No simulation output, no engine telemetry, no I-18 emission set, and no gamora note was opened at
any point. The only sim-side quantities that entered are the three comparators handed down in the
commission itself — **45.06 m**, **`D_ENGAGE_M` = 2.400 m**, **w154 46.12 s vs 14.20 s** — and they
were used only in the direction *referent → compared against sim*. **No threshold in this lap was
chosen after seeing a result, and the one bound-direction claim that turned out wrong is retracted
in § 7 under my own name rather than quietly restated.**

I also did not rule `U-S-1` or `U-S-2`, and I decline to hand the run a single spawn-distance
constant: **the measurement is a distribution over 20 arenas and two defensible comparators, and
collapsing it would be exactly the kind of point value the bracket-not-point ruling exists to
prevent.**

---

## 11. Emitted artifacts

| file | content |
|---|---|
| `PREREGISTRATION.md` | hashed 2026-08-14T15:23:39Z, before any instrument ran |
| `pm4s_first_appearance.csv` | 3,324 tracks × 16 cols — birth radius in gpx and at both bracket edges |
| `pm4s_arena_bounds.csv` | 36 rows — trajectory/entity hulls (INDICATIVE) + frustum limits (MEASURED) |
| `pm4s_arena_placements.csv` | 1,079 rows — every spawn/patrol/beacon/trap/defense placement, 20 arenas, metric |
| `pm4s_arena_geometry.json` | per-arena spawn geometry summary |
| `pm4s_jitter_records.csv` | 169 rows — per-record jitter values over Lap D's frozen baton |
| `pm4s_jitter.json` | declaration, literal-in-binary census, module digests, symbols |
| `pm4s_video.json` | frustum, first-appearance sweep (27 cells), arena, arrival, wave-advance |
| `pm4s_wave_advance.md` | the advance rule, verbatim source + five consequences + two unmodelled mechanisms |
| `pm4s_jitter_law.md` | the jitter law, disassembled, + the MEASURED-NEGATIVE |
| `pm4s_findings.md` | this file |
| `pm4s_digests.json` | FULL 64-hex sha256 of every input and output |
| `evidence/survivalevent.lua` · `tier16waves.lua` · `eventcontrol.lua` | shipped source, banked verbatim |
| `evidence/addjitter_charattributevalspeed.asm` | the disassembled jitter transform |

**Instruments** (`agentic_orchestration/research/scripts/`):
`pm4s_pe_2026_08_14.py` (durable PE32 reader + objdump bridge — Lap J's `/tmp` scratch, made
reproducible) · `pm4s_map_2026_08_14.py` (`.map` world-asset decoder) ·
`pm4s_video_2026_08_14.py` (limb b + limb c video arm) · `pm4s_jitter_2026_08_14.py` (limb d).
They **re-implement nothing**: the ARC reader, the `.arz` reader and Lap D's roster baton are all
imported.
