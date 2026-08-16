# KC2-PM4 · LAP AC — **THE REFERENT SIDE OF THE RESIDENCE** — PRE-REGISTRATION

**Lap:** AC · **Agent:** legolas (`UNKNOWN-RESEARCHER`) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Commission:** `R-PM4-72 part 6` (charter ledger row after `L-62`)
**Written:** 2026-08-16, **BEFORE** any Lap-AC instrument existed or ran.
**Commit discipline:** this file lands **ALONE**, in its own commit, before one line of instrument
is written. Its sha256 is asserted at instrument start; a mismatch is a HALT.

---

## 0 — WHAT THIS LAP IS, AND WHAT IT IS NOT

`R-PM4-72 part 5` escalated the run's **denominator** to the referent side, and `part 3` established
that the fourteenth name (**THE RESIDENCE**) **has no referent comparator today**. Three pins are
missing (`UNREACHED-I27-1`): a per-body referent ring-**entry** time, a per-body referent ring-**exit**
time, and the referent body **population** at the ring. This lap goes and gets whichever of the three
the pins can reach, and publishes the rest as holes with obstacles named.

**THIS LAP IS REFERENT-SIDE ONLY.** No simulation cell, code, telemetry, record or artifact is opened
by any leg. No number produced here elects, ranks, recommends or grades anything for the simulation
(`R-PM4-27 part 3`). **No sim grade is computed anywhere.** The only "audit" performed against a
pinned instrument is the audit of **our own referent-side video pipeline** commissioned in fork (a).

**GL-12 binds absolutely: decode-never-estimate.** Where a quantity is measurable it is measured;
where it is not, `UNREACHED` is published with the obstacle named. No estimate stands anywhere in
place of a decode. If any fork is reachable only by invention, I HALT and say so.

---

## 1 — PINNED INPUTS (sha256 asserted at instrument start; ANY mismatch is a HALT, never a warning)

| # | artifact | sha256 | class |
|---|---|---|---|
| 1 | `…/lap-r-locomotion-contact/pm4r_contact_occupancy.csv` | `913a57a34e58d5e2d9b29def163303ea680189234180986ba43e4f59f7bb20e6` | **the bracket** |
| 2 | `…/lap-r-locomotion-contact/method/plates60_lapH2.npy` | `28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df` | the census |
| 3 | `…/research/scripts/pm4r_contact_2026_08_14.py` | `8994b96a8da280e031fd6d795e8db7b5894910c4b8a233b4b064e1010068f2a7` | the instrument under audit |
| 4 | `…/research/scripts/pm4r_lib_2026_08_14.py` | `630bede0bbc10389dca79d04601d319d37a02f266d406c0aad837480b110762b` | its constants |
| 5 | `…/lap-h2-video-match/method/bars.py` | `2ecfc75543d9498aa81f8d7b733d5f7eca2b7009a2ca7bbd834dffd10258e7e0` | the **detector** |
| 6 | `…/lap-h2-video-match/method/extract.py` | `36f7f923501a7ddd4dccfad7e8fd2e688f8ee53e0647989a68e67ba6dea6b36d` | the **producer** of (2) |
| 7 | `…/lap-h2-video-match/method/d1b.py` | `c26388071e127a0fb8e8420bb4ae151a6a678d444848c67d84cbd445034b876f` | the **tracker** |
| 8 | `…/lap-h2-video-match/method/d1run.py` | `2cebdc5df62979d0d7d208c1aaf7274c02ff2540ea8e7b44efcff9f61dbdf8c5` | its driver constants |
| 9 | `…/lap-h2-video-match/method/d1final.py` | `d9e296eee4e4324b210332b76fe978cf36f5ccc5e657f0ade327e1f940078519` | track-CSV driver |
| 10 | `…/lap-h2-video-match/method/d2.py` | `0366a39faf9586b11278118ba19c50e7d89c2bd49b03643b21ec6ef8a0fc0cd2` | ring-density ancestor |
| 11 | `…/lap-h2-video-match/method/camera_translation_60fps_683-866.npy` | `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33` | world frame |
| 12 | `…/lap-h2-video-match/pm4h2_tracks.csv` | `13bb3033cb35012846343dcb077902304eb163a92cb8f7423ba8cf8074563818` | prior tracks |
| 13 | `…/lap-h2-video-match/pm4h2_ring_density.csv` | `a675367c9f46cedcb3413b3c43dfa0ac2aa0591c8ae120dcef05ce9a2f903eb5` | prior ring counts |
| 14 | `…/lap-ab-march-dispersion/pm4ab_findings.md` | `a0279b1122c4de476e540a0bc34425c68e519a16d667a06abc2964a1675f07ba` | DO-NOT block source |
| 15 | referent MP4 `eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` | **RECORD-class, pinned here for the first time** |

Prior-lap numbers enter **only** through these emitted artifacts with digests asserted — never from
prose (`R-PM4-67 part 2` / `D-CON-6`).

---

## 2 — CONSTANTS, ALL IMPORTED BY IDENTITY, NONE INVENTED HERE

| symbol | value | source, cited by file:line |
|---|---|---|
| `K_GROUND` | `0.537` | `pm4r_lib_2026_08_14.py:60` (Lap H-2 `OBS-H2-8`) |
| `FPS` | `60.0` | `d1b.py:26`; census `t` grid is `1/60 s` |
| `dt` | `1/60 s = 0.016667 s` | ⇒ **every duration in this lap carries ±1 frame = ±0.0167 s** |
| `FIGHT_T0`, `FIGHT_T1` | `683.0`, `864.0` | `pm4r_lib_2026_08_14.py:55` |
| `WAVE_START` | 151:683.0 · 152:698.6 · 153:714.9 · 154:729.8 · 155:744.0 · 156:760.2 · 157:780.4 · 158:799.7 · 159:812.7 · 160:839.0 | `pm4r_lib_2026_08_14.py:48-51` |
| `WAVE_END` | `WAVE_START[w+1]`, 160 closes at `864.0` | `pm4r_lib_2026_08_14.py:56` |
| player-plate gate | `abs(x-960) < 50` **and** `abs(y-429) < 16` | `pm4r_contact_2026_08_14.py:51` |
| ring predicate | `hypot(x - pl_x, (y - pl_y)/K_GROUND) <= RC` | `pm4r_contact_2026_08_14.py:74-75` and `:250-252` |
| gap-join rule | consecutive instants joined while `t[j+1]-t[j] < 0.05` | `pm4r_contact_2026_08_14.py:112` and `:136` |
| tracker gate / maxgap | `gate=30.0` gpx, `maxgap=12` frames, growth `gate*max(1,Δi)**0.6` | `d1b.py:track` (defaults, unchanged) |
| smoother | 15-frame moving average, 7 frames trimmed each end | `d1b.py:kinematics` (`smooth=15`) |

### 2.1 THE RING RADIUS — THE BRACKET, NOT A SCALAR (`R-PM4-70`: brackets stay brackets)

The run's standing occupancy residual is quoted against the `at_sim_D_ENGAGE_M_2.400` rows of pinned
artifact (1). Those three rows are the **only** like-for-like rungs for a 2.400 m ring on referent
pixels, and this lap uses **all three, never one**:

| rung | `R_gpx` | gpx/m anchor | pinned `mean_occupancy` |
|---|---:|---:|---:|
| LO | `285.7` | 119.05 | 3.2423 |
| **MID (primary)** | **`293.6`** | 122.32 | 3.3519 |
| HI | `300.0` | 125.0 | 3.4251 |

**Declared before any measurement:** `293.6` is the **primary** rung solely because it is the middle
of the three; the choice is registered here so it cannot be made after seeing a result. The
metre-anchor conversion is Lap H-2's **DECLARED GAP `OBS-H2-9`**, carried unruled (`pm4r_contact…py:94`,
`:196`). A fourth rung, **`150.0` gpx** (Lap H-2's visually-calibrated melee-abutment radius,
`d1run.py:R_CONTACT`), is reported **separately and never pooled** with the 2.400 m bracket: it is a
different ring, not a sensitivity on the same one.

---

## 3 — FORK (a) — **THE LAP R OCCUPANCY INSTRUMENT'S POPULATION AUDIT**

### 3.1 What fork (a) must answer

*"What did the contact-occupancy bracket's segmentation actually count as a body?"* — as a **decoded
fact with file+line citations**, and then: **is the bracket like-for-like with a movers-only count, a
pet-inclusive count, or neither?**

### 3.2 Leg `A-1` — THE COUNTING CHAIN, DECODED FROM CODE (no measurement; pure decode)

Walk the chain byte-cited, artifact (3) → artifact (6) → artifact (5), and publish the counting
population as a **predicate**, not a paraphrase. Every clause carries `file:line`.

### 3.3 Leg `A-2` — THE GREEN-PLATE CENSUS *(the decisive empirical leg)*

`bars.py` classifies by **colour**: `red_mask` for the counted population, `green_mask2` for the
player. Whether the referent's **four purchased Crucible defence emplacements** (Deathchill Beacon,
Stormcaller Beacon, Inferno Beacon, Vanguard Banner — Lap AB § 3.4, artifact (14), imported by
identity) would have been *counted* therefore reduces to a single decodable question: **does this
footage draw any non-player plate in green?**

- **Method.** Re-extract frames from artifact (15) and run `bars.find_bars` with
  `mask_fn=bars.green_mask2`, **imported unchanged** from artifact (5), with **the position gate
  removed** (`extract.py:pbar` restricts `x_left ∈ [890,960]`; that restriction is precisely what
  would hide an off-centre friendly plate). The four `extract.py:HUD` rectangles are excluded
  unchanged.
- **Window (declared now):** `t ∈ [683.0, 864.0]` sampled at **2.0 fps** on the same 60 fps grid
  (`t = 683.0 + k/2`, `k = 0…362`), **363 frames**, chosen before running.
- **Functional:** per sampled frame, `n_green_offcentre` = number of green-bar detections passing the
  full `find_bars` pipeline (3–6 row persistence, ≥70 white text pixels in `dy ∈ [-34,-18]`, dedupe)
  whose `x_left ∉ [890,960]`.
- **Population non-emptiness (`R-PM4-72 part 4`):** the leg is only evaluable if the detector
  demonstrably fires on this footage — **the player's own green plate must be detected in ≥ 50 % of
  the 363 sampled frames**. Below that the leg publishes **INCONCLUSIVE**, not a negative. A green
  census that finds nothing because the detector found nothing is a caption, not a measurement
  (`D-I26-6` / `D-I27-2`).
- **Evidence:** up to 8 crops around off-centre green detections (or, if none, around the 4 frames
  with the largest count of world-stationary red tracks from leg `A-3`) are written to `evidence/`.

### 3.4 Leg `A-3` — THE EMPLACEMENT SIGNATURE IN THE **RED** POPULATION

An emplacement is **world-stationary for its whole lifetime**. Using fork (b)'s world-frame tracks
(§ 4), census tracks whose lifetime world displacement is small and whose duration is long.

- **Functional:** for each track, `net_world_disp_gpx` = `hypot(Δwx, Δwy/K_GROUND)` between first and
  last observed plate anchor in the **world** frame, and `path_world_gpx` = summed per-frame world
  step. Declared thresholds, chosen now: **`STATIONARY_NET_GPX = 40.0`** (≈ ⅓ of the melee-abutment
  radius) and **`STATIONARY_MIN_S = 8.0`**.
- ⚑ **This leg is CORROBORATIVE, never dispositive.** A world-stationary red track is consistent with
  an emplacement AND with a monster that does not move; and the world frame is a **cumulative sum**
  of per-frame camera estimates whose drift is validated only locally by Lap H-2. The leg is scoped
  to **within-wave** displacement for that reason, and its verdict language is bounded to
  *"consistent with"* / *"no candidate found"*. It may not, alone, decide fork (a).

### 3.5 Leg `A-4` — DECOY ENUMERATION (`D-Z-1` / `D-AA-1`, the standing law)

The findings will enumerate, by name, every population **not** counted and why — including at minimum:
corpses, ground loot / beams, floating combat text, HUD elements, red VFX runs, plate-IoU blobs vs
body identity, off-screen bodies, plate-suppressed bodies, large-bodied monsters' radial displacement,
and the player. The list is written **before** the verdict, not to decorate it.

### 3.6 Fork (a) verdict grammar (fixed now, so it cannot be softened later)

Exactly one of:
1. **PET-EXCLUSIVE** — the counted population is red-plated bodies and the referent's allied
   emplacements are drawn green ⇒ the bracket is **like-for-like with a movers-only count** on the
   summon axis.
2. **PET-INCLUSIVE** — allied emplacements are drawn red and are therefore inside the bracket.
3. **UNDECIDABLE** — the artifacts cannot resolve it; the obstacle is named and the bracket's
   population is published as **carrying an undecided summon term**.

The verdict statement must name its **quantity, population and clock** (`R-PM4-72 part 3`).

---

## 4 — FORK (b) — **REFERENT MONSTER RING-RESIDENCE FROM THE PINNED TRACKS**

### 4.1 Population and identity

The tracked population is **exactly the population the occupancy bracket counts** — `kind == 0` rows
of artifact (2) — so fork (b) is like-for-like with the bracket **by construction**. `d1b.world` and
`d1b.track` are imported **unchanged** from artifact (7); nothing is re-implemented. Tracking runs
**per contiguous wave window** (`WAVE_START[w] … WAVE_END[w]`, § 2) — the same windowing shape as
`d1final.py` — which bounds the association cost and makes wave-boundary truncation **countable**.

**No minimum-track-length filter is applied.** `d1final.py:8` drops tracks under 1.0 s; that filter is
appropriate for a locomotion taxonomy and **wrong for a residence census**, because short residences
are the quantity of interest. The divergence from the ancestor is declared here, in advance.

### 4.2 The ring predicate — imported by identity, in form, from the instrument under audit

For a track's plate anchor `(x, y)` at instant `t` and the player's plate anchor `pl = P[t]`
(gate `pm4r_contact…py:51`):

```
in_ring(t, RC)  ==  hypot(x - pl[0], (y - pl[1]) / K_GROUND) <= RC
```

This is `pm4r_contact_2026_08_14.py:74-75` verbatim in form. **Instants with no detected player plate
are UNOBSERVED, not out-of-ring** — the occupancy instrument excludes them (`:58-61`, "EXCLUDED, not
imputed") and so does this lap.

### 4.3 Intervals

A **ring interval** is a maximal run of consecutive **observed** instants of one track with
`in_ring == True`, joined across gaps of `< 0.05 s` (`pm4r_contact…py:112`). Emitted per interval:
`track_id, wave, RC, t_entry, t_exit, residence_s, n_frames, n_obs_gaps, censor_left, censor_right,
censor_reason, r_at_entry, r_at_exit, r_min`.

**Residence** `= t_exit − t_entry`, **±0.0167 s**, published with that stamp on every quantile.
A second functional, `body_time_s = n_frames · dt`, is published alongside it — the two differ by
exactly one frame per interval and both are named rather than averaged.

### 4.4 TRUNCATION HONESTY — mandatory, published per interval and in aggregate

Every interval is flagged **left-censored** if its first instant is the track's first observed instant,
or the wave-window's first instant, or is preceded by an unobserved gap ≥ 0.05 s; **right-censored**
symmetrically. Aggregate quantiles are published **twice**: over **all** intervals (an under-estimate
of true residence, direction declared) and over **uncensored-only** intervals (a survivorship-selected
sub-population, direction declared). Neither is presented as *the* answer. Additional named limits,
all published whether or not they bite:

- **identity-continuity** — the tracker's `gate`/`maxgap` can split one body into two tracks
  (inflating interval count, deflating durations) or merge two bodies into one (the converse);
- **occlusion / VFX saturation / plate suppression** — plate absence never proves body absence
  (`bars.py:12-15`, NOTE-9), so every count remains a **LOWER BOUND** and every residence a
  **left-truncated** observation;
- **large-bodied monsters** — plate sits high above the head, so their radial distance is
  systematically over-stated ⇒ their residence is systematically **under**-counted (Lap R § 200);
- **wave-window boundaries** — 9 internal cuts; the count of intervals touching one is published;
- **player-plate coverage** — 10,216 of 11,039 frames carry a player plate; the shortfall is
  unobserved time, reported as a fraction per wave.

### 4.5 `UNREACHED-I27-1`'s three pins — what fork (b) claims and what it does not

| pin | disposition |
|---|---|
| per-body referent ring-**entry** time | fork (b) **fills** it, at the declared resolution, truncation-flagged |
| per-body referent ring-**exit** time | fork (b) **fills** it, at the declared resolution, truncation-flagged |
| referent body **population** at the ring | fork (a) **rules** it; fork (b) publishes the per-wave in-ring body count from its own intervals |

⚑ **Fork (b) does NOT re-derive occupancy.** The bracket is pinned and stays pinned; the reconstruction
in `F-AC-1` below exists **solely as a fidelity gate on my own tracker** and is never published as a
competing occupancy figure.

⚑ **Fork (b) computes NO sim comparison.** `W` still has no referent-vs-sim grade and this lap does not
manufacture one — `R-PM4-72 part 3` (i) stands until the conductor rules otherwise. Per-body referent
residence and gamora's `W` are the **same quantity on different clocks and different populations**;
stating both side by side would be `D-CON-9`'s twin and is forbidden here.

---

## 5 — FORK (c) — **THE REFERENT'S EXIT-CHANNEL SPLIT, WHERE RESOLVABLE**

### 5.1 Alive-vs-dead at exit

For each ring interval with an **observed** (non-right-censored) exit:

- **`EXIT_ALIVE`** — the same track has ≥ 1 further observed plate instant after `t_exit` within its
  wave window. A plate **proves** a living body (`bars.py:14-15`), so this classification is a
  **decoded positive**.
- **`EXIT_TRACK_ENDS`** — no further plate instant for that track. Corpses carry no nameplate
  (Lap H-2 `OBS-H2-1`, confirmed), so this is **consistent with death** — and equally with occlusion,
  plate suppression, screen exit or a tracker identity break. It is therefore published as
  **`DEATH-CANDIDATE`, never as `DEATH`.** Two named sub-flags are emitted to bound it:
  `near_screen_edge` (plate anchor within 120 px of any frame edge at exit) and `re_detect_within_1s`
  (any unassociated plate within `gate` gpx of the last position inside 1.0 s).

⚑ If the ratio of `EXIT_TRACK_ENDS` that carry `re_detect_within_1s` exceeds **0.35**, the alive/dead
split is declared **UNREACHED** for want of a death discriminator, and only the counterfactual
partition (§ 5.2) is published. Threshold fixed now.

### 5.2 The counterfactual partition — *who moved?*

Let `t_i` be the last in-ring instant and `t_e` the first out-of-ring instant of an observed exit, and
let `m_w(·)`, `p_w(·)` be monster and player **world** positions (screen minus cumulative camera
translation, `d1b.world`, artifact (11)). Ground-plane distances throughout (`y/K_GROUND`). Define:

```
r_actual            = |m_w(t_e) − p_w(t_e)|          (> RC by construction)
r_player_frozen     = |m_w(t_e) − p_w(t_i)|          player held at its last in-ring position
r_monster_frozen    = |m_w(t_i) − p_w(t_e)|          monster held at its last in-ring position
```

Four-bucket, exhaustive, mutually exclusive:

| bucket | condition |
|---|---|
| **`MONSTER_SUFFICIENT`** | `r_monster_frozen <= RC` and `r_player_frozen > RC` |
| **`PLAYER_SUFFICIENT`** | `r_player_frozen <= RC` and `r_monster_frozen > RC` |
| **`EITHER_SUFFICIENT`** | both `> RC` (each motion alone would have carried the exit) |
| **`NEITHER_SUFFICIENT`** | both `<= RC` (only the joint motion crosses the boundary) |

*(Naming note, fixed now so it cannot drift: the bucket is named for the mover whose motion, **alone**,
suffices to explain the crossing. `MONSTER_SUFFICIENT` therefore requires the **player**-frozen
counterfactual to still be out of ring.)*

Additionally reported, never substituted for the partition: the player's smoothed ground speed
(`pm4r_lib.rolling_median`, `SMOOTH_FRAMES = 9`, imported by identity) in `[t_e − 0.125, t_e + 0.125]`
at exits, against its fight-wide distribution over the same observed instants.

⚑ **Small-N is acceptable and is declared as such** (commission: *"even a small-N answer with declared
resolution beats none"*). What is **not** acceptable is a partition computed on an empty or
near-empty population; see `F-AC-2`'s non-emptiness clause.

---

## 6 — FALSIFIERS AND CRITERIA
### (each declares **WINDOW**, **FUNCTIONAL** and **POPULATION NON-EMPTINESS** — `R-PM4-72 part 4`)

### `F-AC-1` — **TRACKER FIDELITY**: my per-body decomposition must reconstruct the pinned occupancy

- **WINDOW.** `t ∈ [683.0, 864.0]`, restricted to the **10,216 instants carrying a detected player
  plate** — the occupancy instrument's own population (`pm4r_contact…py:58`), not a superset.
- **FUNCTIONAL.** `L_recon(RC) = Σ_intervals n_frames · dt / (N_obs · dt) = Σ n_frames / N_obs`,
  compared against the pinned `mean_occupancy` for the same `RC` in artifact (1), rows
  `at_sim_D_ENGAGE_M_2.400`. Same units (bodies), same truncation regime (identical instant set),
  same population (`kind == 0` plates).
- **POPULATION NON-EMPTINESS.** Evaluable only if `N_obs >= 10000` **and** the interval count at the
  primary rung `RC = 293.6` is `>= 50`. Otherwise `F-AC-1` is **UNREACHED**, published as a hole.
- **CRITERION.** PASS iff `|L_recon(RC)/L_pinned(RC) − 1| <= 0.05` at **all three** rungs
  (285.7 / 293.6 / 300.0).
- **WHY IT IS WORTH REGISTERING.** It can fail: if the tracker drops, splits or mis-associates plate
  instants, body-time leaks and `L_recon` under-shoots. A failure invalidates fork (b)'s quantiles and
  I would publish them as UNREACHED rather than repair the threshold. ⚑ **This grades MY instrument
  against MY OWN lap's pinned artifact. It is not a sim comparison and issues no sim verdict.**

### `F-AC-2` — **THE REFERENT'S EXIT CHANNEL IS NOT PREDOMINANTLY MONSTER-DRIVEN**

- **WINDOW.** All ring intervals at the **primary** rung `RC = 293.6`, whole fight `[683.0, 864.0]`,
  **observed exits only** (not right-censored), one bucket per exit.
- **FUNCTIONAL.** `share_player = (PLAYER_SUFFICIENT) / (PLAYER_SUFFICIENT + MONSTER_SUFFICIENT)` —
  a share over the two **decidable** buckets, with `EITHER_` and `NEITHER_` published separately and
  never folded in to move the number.
- **POPULATION NON-EMPTINESS.** Evaluable only if `PLAYER_SUFFICIENT + MONSTER_SUFFICIENT >= 30`.
  Below 30 the criterion is **UNREACHED** and the raw four-bucket counts are published unGRADED.
- **CRITERION.** `F-AC-2` **PASSES** (the referent's exit channel is materially player-displacement-fed)
  iff `share_player >= 0.20`. It **FAILS** below 0.20.
- ⚑ **What a PASS does and does not license.** It licenses the sentence *"displacement is a materially
  present ring-exit channel in the referent, at this resolution."* It does **not** license any
  comparison to I-27's sim-side displacement shares — different instrument, different clock, different
  predicate, and `R-PM4-72 part 4` forbids the comparison outright.

### `F-AC-3` — **THE GREEN-PLATE CENSUS IS DECISIVE**

- **WINDOW.** The 363 frames of § 3.3, `t ∈ [683.0, 864.0]` at 2.0 fps.
- **FUNCTIONAL.** `n_frames_with_offcentre_green` = number of sampled frames with
  `n_green_offcentre >= 1`.
- **POPULATION NON-EMPTINESS.** Evaluable only if the player's own green plate is detected in
  `>= 182` of the 363 frames (≥ 50 %). Otherwise **INCONCLUSIVE**, published as such.
- **CRITERION.** `n_frames_with_offcentre_green >= 1` ⇒ fork (a) verdict **PET-EXCLUSIVE** is
  supported by measurement; `== 0` over a non-empty, detector-live population ⇒ the green channel
  carries nothing but the player, and fork (a) must fall to **PET-INCLUSIVE** or **UNDECIDABLE** on
  legs `A-1`/`A-3` alone. **`F-AC-3` grades the census's decisiveness, not the verdict.**

---

## 7 — PRE-REGISTERED PREDICTIONS (graded **wording-unchanged**)

| # | prediction |
|---|---|
| **P-1** | The Lap R occupancy instrument's counted population is decodable **entirely from artifacts (2)–(6)**, with no undisassembled consumer in the chain. |
| **P-2** | The counted population is **red-masked nameplate bars carrying a white text token**, and colour is the **sole** hostile/friendly discriminator in the chain — no faction, name, HP or template field enters. |
| **P-3** | At least one green bar detection occurs **outside** the player's `x_left ∈ [890,960]` gate in the 363-frame sample. |
| **P-4** | The player's own green plate is detected in **≥ 50 %** of the 363 sampled frames (`F-AC-3`'s non-emptiness clause holds). |
| **P-5** | `F-AC-1` **PASSES** at all three rungs: my per-body decomposition reconstructs the pinned `mean_occupancy` to within 5 %. |
| **P-6** | The number of ring intervals at `RC = 293.6` over the whole fight is **≥ 300**. |
| **P-7** | Median referent ring residence at `RC = 293.6` over **all** intervals is **≥ 0.20 s**. |
| **P-8** | **More than 25 %** of ring intervals at `RC = 293.6` are censored on at least one side. |
| **P-9** | `F-AC-2`'s decidable population is **non-empty and ≥ 30**, i.e. the criterion is evaluable rather than UNREACHED. |
| **P-10** | `PLAYER_SUFFICIENT` exits are **present** (count ≥ 1) at the primary rung. |
| **P-11** | At least one leg of this lap returns **UNREACHED** with an obstacle named — this lap does not close every question it opens. |
| **P-12** | Leg `A-3` finds **at least one** world-stationary red track meeting `STATIONARY_NET_GPX = 40.0` / `STATIONARY_MIN_S = 8.0` within a single wave. |

Predictions are graded verbatim. A prediction that fails is reported as failing; none is re-worded,
re-scoped or dropped after the numbers (`D-AB-3`'s lesson, one lap on).

---

## 8 — DEFECT DISCIPLINE, DETERMINISM, AND DIGESTS

- **Defects self-disclosed in a defect table BEFORE any claim rests on them.** Every defect found in my
  own instrument is published whether or not it changed a number, with its disposition.
- **Determinism ×2.** Every instrument runs **twice**; all emitted artifacts must be **byte-identical**
  across the two legs. Any stochastic element uses a fixed seed declared in code. A non-identical leg
  is a HALT.
- **Digests computed AFTER the final write** (`D-AA-5`), full 64-hex sha256, and the committed blob is
  verified equal to the working tree before the lap is reported.
- **New mechanisms encountered are NAMED, not decoded** (`R-PM4-56 part 4`).
- **HALT rather than estimate.** If a fork is reachable only by invention, I stop and report the HALT
  with the obstacle named, rather than publish a number-shaped hole as a number.

### 8.1 Declared method risks (named now, before they can be discovered later)

1. **The `.05 s` gap-join can bridge a genuine exit-and-re-entry** into one interval, inflating
   residence. The count of intervals containing an internal unobserved gap is emitted so the reader
   can bound it.
2. **`d1b.track` retains dead tracks in its candidate list** (they are skipped by the `maxgap` test but
   never pruned). Per-wave windowing bounds the cost; the behaviour is unchanged from the ancestor.
3. **The world frame is a cumulative sum** of per-frame camera estimates. Fork (c)'s counterfactuals
   use it only over a **single frame step** `t_i → t_e`, where drift is negligible by construction;
   leg `A-3` uses it only **within** a wave. No claim in this lap rests on cross-wave world positions.
4. **`pm4r_lib.PLAYER_SCREEN = (958, 544)` and `d1b.PX_S/PY_S = (960, 544)` disagree by 2 px.** The
   ring predicate (§ 4.2) uses **neither** — it uses the per-instant **detected player plate anchor**,
   exactly as the audited instrument does. The discrepancy is recorded and does not enter.
5. **The occupancy instrument's whole-fight loop includes `t = 864.0`; its per-wave loop excludes it**
   (`(ta >= a) & (ta < b)`). Fork (b) follows the whole-fight convention and states the one-instant
   difference rather than silently choosing.

---

## 9 — DO-NOT BLOCKS CARRIED, ENTIRE

Lap V § 7.2 · Lap V-2 § 11.2 · Lap W § 7.2 · Lap X § 12.2 · Lap Y § 11.6 · Lap Z § 5 · Lap AA § 6 ·
**Lap AB § 9 (all ten)** — carried unchanged and binding on this lap. In particular:

- **Lap AB DO-NOT 9** — `pm4u_arrivals.csv` is a **strict upper bound** (`D-U-3`), **not** an arrival
  rate. ⚑ **This lap does not open it, does not cite it, and computes no referent `λ` from it.**
- **Lap AA DO-NOT 5** — arena identity is UNREACHED at 3/10; the candidate-restricted bound governs any
  distance claim.
- **Lap AB DO-NOT 4** — `F-AB-1`'s failure is **not** evidence that the referent compresses its march
  and is not cited here as anything.
- **Lap H-2 NOTE-9** — plate presence proves a living body; **absence never proves absence**. Every
  count in this lap is a LOWER BOUND and every residence a truncated observation. Non-negotiable.

---

## 10 — WHAT THIS LAP WILL NOT DO (the firewall, stated in advance)

1. No simulation cell, code, telemetry, record, config or artifact is opened by any leg.
2. No sim grade, ratio, deficit, convergence or comparison is computed anywhere.
3. No number here elects, ranks, designates or recommends anything (`R-PM4-27 part 3`).
4. The standing occupancy residual is **not re-quoted, re-based or amended**; the definition of record
   stays exactly where `R-PM4-72 part 5` left it.
5. No metre quantity is published on a single anchor; the bracket governs.
6. `W` acquires **no** referent comparator by side-by-side placement in this lap's prose.

---

*Pre-registered by legolas (`UNKNOWN-RESEARCHER`), 2026-08-16, before any Lap-AC instrument existed.*
