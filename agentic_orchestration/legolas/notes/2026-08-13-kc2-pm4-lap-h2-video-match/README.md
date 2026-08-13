# RUN KC2-PM4 — Lap H-2 — deep video-match decode

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR) · **Fired under:** R-PM4-11
(Matt verbatim: *"Please review the fight video from my grim dawn fight and match what occurs there."*)
**Date:** 2026-08-13 · **Discipline:** GL-12 decode-never-estimate · NOTE-9 basis on every number ·
read-only on `/Volumes/reincarnated/` · observer firewalled from the sim's outcome numbers.

---

## VERDICT — D1 contact response: **R2-MEASURED** (lateral resolution), R1 measured-ABSENT

Lap H returned UNDECIDABLE on 6/6 episodes against a strict binary eyeball rubric. Matt widened the
instrument. It is now decided, and it is decided by a *measurement*, not a judgement call:

| clause | result |
|---|---|
| **R1 "block-and-dwell"** — body holds station behind a blocker ≥1.5 s while not attacking | **MEASURED ABSENT.** Median blocked dwell **0.18 s**; p90 0.43 s; longest in the entire fight **1.77 s**. Of 333 blocked dwell spans, **2** reach 1.5 s and **0** reach 2.5 s. The unblocked control is statistically identical (median 0.17 s, max 1.30 s) — *blocking is not what makes bodies stop.* |
| **R2 "lateral resolution"** — path resolves around the clump toward an open arc | **MEASURED PRESENT** as a monotone eight-band gradient: median **closing** speed collapses **108.5 → 0.6 ground px/s** from far field to contact ring, while median **tangential** speed *rises* **58.8 → 86.7**. Bodies arriving at the ring stop closing and keep moving — laterally, at undiminished speed. |

n = 48,956 track-frames across **339 tracks**, **10 waves** (151–160), 60 fps. Evidence figure:
`evidence/D1-radial-tangential-vs-range.png`. Full band table: `pm4h2_d1_range_profile.csv`.

**Honest shape of the verdict.** The behaviour is *graded, not binary*. Bodies do not switch state at a
radius; the tangential fraction of motion rises continuously as range falls (median |v_t|/|v| 0.388 far
field → 0.739 at the ring, against an isotropic-motion null of 0.707). And blocking *per se* is a weak
term: blocked-vs-unblocked frames differ by only ~1.4 pp in stationary fraction. What is strong is
**range**. The measured law is *"closing velocity is extinguished at the ring while tangential velocity
is not"* — which is what a push-apart/lateral-resolution model produces and what block-and-dwell cannot.

### Why this lap could decide what Lap H could not

Lap H's four named confounds are dissolved by one find (§ "the enabling find") plus one instrument:

| Lap H confound | status here |
|---|---|
| **C1 corpse carpet** — a motionless clump reads as blocked rear rank but is corpses | **DISSOLVED.** Corpses carry **no nameplate**. Every body in this lap's census is plate-proven living. |
| **C2 VFX saturating the contact annulus** | **DISSOLVED.** Nameplates are drawn in the **UI layer, over all world VFX**. The instrument reads through the bloom. |
| **C3 terrain inside the melee zone** | **PARTLY STANDING.** Terrain is not measured. It would add stalls, not tangential motion — so it can only weaken R2, never manufacture it. The verdict is conservative against C3. |
| **C4 multi-point spawn geometry manufactures a surround** | **DISSOLVED.** The classification is a **per-body velocity decomposition against the current player position**, not a configuration read. Where bodies *come from* does not enter. |

---

## The enabling find — the camera is rigidly player-locked

The player's own nameplate bar sits at a **fixed screen anchor**: left edge x = **921–924 px** (p5–p75)
and bar row y = **421–433** (p5–p95), across **1,742/1,840 (94.7 %)** detections at 10 fps and **10,444/11,040 (94.6 %)**
at 60 fps. (The bar depletes *rightward from a fixed left edge* — its width ranged 14–74 px over the
same detections — so the **left edge is the anchor** and `x_left + 36` recovers screen x = **960**.)

Two consequences carry this whole lap:

1. **Screen coordinates ARE player-relative coordinates.** No stabilisation is required for any
   player-relative measurement, and no camera-registration error enters it.
2. **Camera translation IS the player's world displacement, exactly, in screen pixels.**

The player's ground point is pinned at screen **(958, 544)** — 115 px below the plate bar — by the
player's own circular ground decal at t = 683.500, measured **80 × 43 px** centred (957.5, 544.4).
That ellipse also gives the isometric ground-plane compression **K = minor/major = 0.537**. Every
distance in this lap is a **ground pixel** = screen x-pixel with screen dy divided by 0.537.

---

## Instrument — the nameplate tracker

Monster nameplates are the tracking primitive, replacing Lap H's silhouette reading:

- **red 3-scanline bar, ~72 px at full width**, with a white `(cur/max)` string at a *measured* offset
  of dy = −31…−21 from the bar's top scanline (profiled on five bars in frame 783.000; all five peak
  in that band and are empty outside it). The text co-occurrence gate is what kills red-VFX false
  positives — without it a saturated frame reports 103 "bars"; with it, 15.
- **green bar = the player** (RGB ≈ 120/240/35, measured at frame 700.000 rows 428–431). Monsters are
  red; therefore green is unambiguous.
- **corpses carry no bar** → the C1 discriminator.

Extraction: **98,794 monster plates + 10,316 player rows over 11,039 frames at 60 fps** (whole fight
683–866 s). Linking: greedy nearest-neighbour in ground-plane world coordinates, gate 30 ground px,
max gap 12 frames.

**Camera trace.** 60 fps, phase correlation on the *gradient magnitude* of the terrain band (terrain is
high-frequency, VFX glow is low-frequency, so the correlation peak stops being pulled by moving light),
sub = 2, parabolic sub-pixel, running-median outlier rejection. **Validated at two points against
independent normalised-cross-correlation terrain-patch matching**:

| interval | 60 fps trace | independent NCC | agreement |
|---|---|---|---|
| 700.00 → 700.25 (quiet) | 88.4 px | 82.1 / 92.4 / 93.4 / 108.3 px across four terrain patches | within spread |
| 805.55 → 805.85 (fastest event) | 244.8 px | 236.0 px (best-confidence patch, ncc 0.684) | **3.7 %** |

**Velocity decomposition (the classifier).** Per track per frame, the monster's *own* world velocity is
resolved against the *current* player world position: `v_radial` (positive = closing) and
`v_tangential`. Both are properties of the monster's motion alone — **player movement does not enter**,
which is what makes this classification legal on footage where the player is moving 88 % of the time.
Track-level plate height is constant, so it cancels out of every derivative; only absolute range carries
the plate-height bias.

**BLOCKED predicate:** another living plate sits in the corridor between the body and the player
(closer to the player, perpendicular offset < corridor, projection strictly between). Results are
reported at corridor = 50 / 70 / 100 ground px and are **stable across all three**.

---

## D1 — results

### Blocked vs unblocked, per frame (outside contact, r > 150 ground px)

| population | n frames | stationary | tangential-dominant | closing | median speed |
|---|---|---|---|---|---|
| BLOCKED (corridor 70) | 23,312 | 0.296 | 0.399 | 0.376 | 134.0 |
| UNBLOCKED (control) | 17,537 | 0.282 | 0.418 | 0.400 | 145.2 |
| ≥2 blockers | 12,350 | 0.310 | 0.383 | 0.350 | 123.0 |
| ≥3 blockers | 6,305 | **0.337** | 0.385 | 0.319 | **104.9** |

Blocking produces a **graded mild slowdown** (145 → 105 median ground px/s, −28 %; stationary fraction
0.28 → 0.34) — and **no stall regime**. Identical picture at corridor 50 and 100.

### Range profile — the decisive statistic

| range band (ground px) | n frames | median v_radial | median v_tangential | median \|v_t\|/\|v\| (moving) |
|---|---|---|---|---|
| 900–1400 | 2,562 | **108.5** | 58.8 | 0.388 |
| 600–900 | 16,050 | 33.6 | 61.1 | 0.529 |
| 400–600 | 10,689 | 15.6 | 48.6 | 0.549 |
| 300–400 | 5,111 | 14.2 | 52.3 | 0.569 |
| 220–300 | 4,548 | 7.3 | 65.3 | 0.611 |
| 150–220 | 4,451 | 4.3 | 66.2 | 0.660 |
| **100–150 (the ring)** | 2,774 | **0.6** | **86.7** | **0.739** |
| 0–100 | 2,771 | 2.3 | 89.2 | 0.672 |

Monotone in seven of eight bands. Track-linking noise would push every ratio *toward* the isotropic null
0.707 — it cannot create a monotone gradient from 0.388 to 0.739, so the measurement is conservative.

### Track census — every track attempted

`pm4h2_tracks.csv`, **339 rows**, one per track ≥1.0 s, waves 151–160, with id / window / frame count /
classification / range endpoints / blocked fraction / max blocked dwell / radial + tangential medians.
Per-track labels (the strict per-track rubric, which is much coarser than the per-frame census):

| label | n |
|---|---|
| INDETERMINATE | 166 |
| APPROACH-DIRECT | 114 |
| IN-CONTACT | 30 |
| UNBLOCKED-NO-TEST | 26 |
| **R1-STALLED-BEHIND** | **2** |
| **R2-LATERAL-RESOLVED** | **1** |

The 2-vs-1 split at track level is **not the verdict** and must not be read as one — the per-track
rubric requires ≥1.5 s of *uninterrupted* stall or ≥1.0 s of *uninterrupted* blocked tangential
dominance, and real bodies switch regime faster than that. It is reported because the charter asked for
every attempt. **The verdict rests on the 48,956-frame census and the range profile**, where the
question is asked at the timescale the behaviour actually operates on.

**Named exemplars** (all far → ring, > 2.5 s; plotted in `evidence/D1-exemplar-tracks.png`):

| track | wave | window (s) | frames | r start → min | blocked | max blocked dwell | median v_t / v_r | tang ratio |
|---|---|---|---|---|---|---|---|---|
| W151-T03 | 151 | 690.97–697.00 | 359 | 1137 → 126 | 0.68 | 0.57 s | 95 / 96 | 0.64 |
| W152-T02 | 152 | 704.37–710.93 | 361 | 998 → 106 | 0.38 | 0.23 s | 76 / 69 | 0.39 |
| W153-T10 | 153 | 720.32–723.00 | 176 | 909 → 114 | 0.57 | 0.13 s | 99 / 77 | 0.74 |
| W153-T11 | 153 | 719.50–722.33 | 168 | 926 → 123 | 0.82 | 0.00 s | 81 / 88 | 0.52 |
| W156-T01 | 156 | 768.98–778.02 | 549 | 999 → 55 | 0.68 | **1.03 s** | 14 / 0 | 0.31 |
| W157-T01 | 157 | 784.32–797.93 | 826 | 981 → 51 | 0.45 | 0.40 s | 82 / **0** | 0.79 |
| W157-T04 | 157 | 787.82–798.73 | 655 | 1037 → 3 | 0.38 | 0.27 s | 63 / 8 | 0.64 |
| W157-T14 | 157 | 787.67–791.62 | 181 | 885 → 32 | 0.44 | 0.00 s | **259 / 42** | **0.89** |
| W159-T16 | 159 | 816.45–819.70 | 166 | 892 → 9 | 0.31 | 0.12 s | 100 / **417** | 0.21 |
| W160-T01 | 160 | 841.87–858.40 | 885 | 1098 → 21 | 0.53 | 0.32 s | 27 / 4 | 0.39 |
| W160-T03 | 160 | 850.47–859.87 | 505 | 1059 → 200 | 0.57 | 0.42 s | 22 / 4 | 0.66 |

W159-T16 is the pure straight-in charger (v_r = 417, tang ratio 0.21). W157-T14 is the pure lateral
resolver (v_t = 259 vs v_r = 42, tang ratio 0.89). **Both shapes are in the corpus** — the population
statistic is what decides, and it is the range profile above. **The single longest blocked dwell across
all 339 tracks is 1.03 s in this exemplar set, 1.77 s across the whole census.**

---

## D2 — ring density (the match target)

`pm4h2_ring_density.csv`. Contact criterion: plate anchor within **150 ground px** of the player's plate
anchor, ground plane de-projected by K = 0.537; calibrated by direct visual inspection with rings drawn
at 100/150/200/300 ground px on frames 783.000 and 824.400 (bodies whose sprites abut the player fall
inside 150; the next rank sits at 200–270). Reported at 120 and 180 as sensitivity.

| window | wave | n instants | **max contact** | typical (mode) | median | p90 | mean |
|---|---|---|---|---|---|---|---|
| **WHOLE FIGHT 683–864** | 151–160 | **10,036** | **10** (9 at R120, 12 at R180) | 0 | 1 | 3 | 1.31 |
| W151-early 688.0–698.5 | 151 | 553 | 8 | 0 | 1 | 3 | — |
| PM4H-E1 689.0–694.0 | 151 | 273 | 4 | 0 | 0 | 1 | — |
| PM4H-E2 770.0–774.0 | 156 | 241 | 8 | 1 | 2 | 5 | — |
| PM4H-E3 810.5–813.25 | 158 | 132 | 5 | 0 | 1 | 2 | — |
| PM4H-E4 779.0–784.0 | 157 | 220 | 5 | 0 | 0 | 1 | — |
| PM4H-E5 813.0–817.0 | 158–159 | 227 | 3 | 0 | 0 | 1 | — |
| PM4H-E6 838.0–846.0 | 159–160 | 349 | 5 | 0 | 1 | 2 | — |
| per-wave 151…160 | — | 553–1,452 each | **4 / 7 / 4 / 8 / 8 / 9 / 10 / 8 / 9 / 8** | 0–1 | 0–2 | 2–4 | — |

**The match target, stated plainly: median 1, p90 3, whole-fight maximum 8–12 simultaneous nameplated
monsters in melee contact.** Peak per wave never exceeds 10 at the calibrated radius.

**Occlusion / basis caveats (NOTE-9), all of which make these LOWER BOUNDS:**
- counts nameplated monsters only — a plate proves a living monster; absence does not prove absence;
- **large-bodied monsters are systematically under-counted**: their plate sits high above the head, far
  from the ground contact point, so a giant whose body overlaps the player can score outside 150;
- the mode of 0 is real and is *not* an artefact of the instrument — it is the signature of a player who
  is repositioning 88 % of the time (see D3). It says the reference fight is not a standing brawl.

---

## D3 — player movement cadence (I-4 policy substrate)

`pm4h2_movement_cadence.csv`. Basis: the 60 fps camera trace (= player world displacement exactly,
per the enabling find), NCC-validated at two points, converted to ground px via K = 0.537.

**Threshold basis.** The player speed histogram is cleanly bimodal: a stationary spike at 0–40 ground
px/s, a valley at 40–80, and a broad **run mode at ~440 ground px/s**. The motion threshold is set at
the measured valley, **60 ground px/s**; 200 and 400 are reported as sensitivity.

| (a) fraction of fight time in significant motion | **0.883** at 60 ground px/s · 0.757 at 200 · 0.494 at 400 |
|---|---|
| **(b) dash-class events** | **34** at ≥950 ground px/s (≈2.2× the run mode) · **19** at ≥1800 ground px/s. Per wave (≥950): 2/2/4/3/4/2/3/4/6/4 for waves 151→160. |
| **(c) median displacement per movement bout** | **226.9 ground px net**, **472.4 ground px path**, over **107 bouts**; median bout duration **1.03 s**. Total path over the fight **71,960 ground px** (mean 397.6 ground px/s). |
| **(d) longest stationary window during combat** | **1.40 s** (t = 810.58–811.98). Only **two** stationary runs in the whole 181 s fight reach 1.0 s; **none** reaches 2.0 s. Total stationary time 22.8 s = 12.5 % (the 0.883 moving fraction and this figure differ by the 0.15 s minimum-span filter on runs). |

> **The headline for I-4.** The reference player is *never* stationary for as long as two seconds across
> the entire fight, moves for 88 % of it, and fires a dash-class traversal roughly every 5 s. Lap H's
> "the reference player is NOT pinned" is now quantified. This is the measured constant set for the
> sim's movement policy — decoded from what Matt actually did.

Largest short high-peak traversals (candidate dash-skill firings), net ground px:
489 @690.57 · 455 @797.68 · 448 @825.95 · 423 @805.67 · 367 @844.40 · 340 @858.18 · 331 @847.97 ·
313 @789.58 · 299 @732.45 · 237 @785.30 · 223 @831.63.

---

## D4 — contact-adjacent observables (logged, not ruled)

`pm4h2_observables.csv`, nine rows. Headlines:

- **OBS-H2-1 corpses carry no footprint — CONFIRMED.** Plate-free prone bodies carpet the floor from
  ~wave 155 and living bodies and the player stand on them. Three evidence frames. The nameplate
  discriminator is what makes it *assertable* rather than merely visible.
- **OBS-H2-2 the Lap H interpenetration candidate (E4-782.00) is RETIRED.** At t = 782.000 the nearest
  nameplated monster sat at **226.6 ground px** (dx +84, dy +113); next nearest 335. Nothing was inside
  200. Lap H's uncertain flag is closed negative.
- **OBS-H2-3 interpenetration in general — NOT ASSERTABLE, declared.** Small plate separations cannot be
  read as overlap: a taller-than-player monster standing *down-screen* has its extra plate height cancel
  its ground offset, aliasing to near-zero plate separation at real separation. Per-record plate height
  is unmeasured, so the alias cannot be removed. Declared, not estimated.
- **OBS-H2-4 the player channels while traversing — CONFIRMED.** Across the fastest single traversal in
  the fight (244.8 raw px in 0.30 s), the player-centred channel VFX ring is continuously present and
  player crit numbers keep spawning in every frame while the terrain visibly translates. NOTE-9: pixels
  cannot name *which* skill draws the ring; the measured claim is that a channel VFX **and** player
  damage output both persist through traversal. Corroborates Lap G's `canUseWhileMoving=1` on camera.
- **OBS-H2-5 player HP trace — MEASURED** (method validated against read plate text to 1 %). Mean HP
  fraction **0.932**; below 0.75 for 8.5 % of the fight, below 0.55 for 4.4 %, below 0.40 for 1.3 %.
  **Seven** sustained excursions below 0.70: t = 735.8 (0.35 s, min 0.38) · 742.0 (0.62, 0.49) · 749.1
  (0.43, 0.41) · 832.4 (1.40, 0.35) · 844.3 (1.87, 0.23) · 847.8 (1.00, 0.38) · **856.1 (6.55 s, min
  0.28 — the terminal collapse)**. Bears on I-3 and on T4b's terminal clause; **not interpreted here**.
- **OBS-H2-6 wave boundaries re-measured to ±0.25 s** from the wave-counter digit crop:
  152@698.6 · 153@714.9 · 154@729.8 · 155@744.0 · 156@760.2 · 157@780.4 · 158@799.7 · 159@812.7 ·
  160@839.0. Supersedes Lap H's 4 s-granularity map (which put 159@816, 160@840). Offered as
  corroboration only — **this lap rules nothing about T3.**
- **OBS-H2-9 ground px → metres: DECLARED GAP, NOT RULED.** Two candidate anchors disagree and neither
  is decisive: Lap G's decoded 10/12/16-unit dash layers against the largest observed traversal (489
  ground px ⇒ ≥30.6 px/unit) versus the measured ~440 ground px/s run mode (which at that scale implies
  an implausible ~14 units/s, and at any plausible walk scale would make a 12-unit dash ≈1,500 ground px
  — four times the largest displacement ever observed). The conflict is real. **Every distance in this
  lap is therefore reported in ground pixels and the metre conversion is declined.** Resolving it needs
  one in-frame anchor of known DB length. This is the named blocker on comparing this lap's radii
  directly with `D_ENGAGE_M = 2.4` or Lap F's `actorRadius`.

---

## Self-corrections recorded (GL-12)

- **IS-H2-1 — Lap H's dash landmark was not a camera measurement, and this lap's own first trace was
  wrong too.** Lap H hand-tracked the `94,059/94,059` **nameplate** across 732.50→732.75 and got 236 px,
  concluding phase correlation ran "~30 % high". A nameplate belongs to a *monster*, which carries its
  own motion — it is not a camera landmark. Independent NCC terrain matching gives **176.2 px** and the
  60 fps gradient trace **175.4 px** (0.5 % apart). Separately, this lap's own first 20 fps trace summed
  only **54 px** over the same interval — phase correlation *fails* during fast motion at coarse
  sampling (correlation peak 0.05, i.e. registration failure defaulting toward zero). Both errors are
  fixed by the same change: 60 fps sampling + gradient registration + NCC validation at two points.
  **All Lap H translation figures should be treated as superseded by `method/camera_translation_60fps_683-866.npy`.**
- **IS-H2-2 — this lap's first HP instrument was an artefact, caught and retracted before it entered any
  finding.** Raw per-frame player-bar width produced a spectacular-looking result: HP oscillating to
  20–35 % and snapping back to full **54 times** in 183 s. It is false. VFX overdraw *truncates* the
  green run, manufacturing spurious dips. Caught by reading the plate text at the deepest dips —
  t = 688.2 reads `(20,005/20,005)`, i.e. **full**, where the instrument said 0.20. Replaced by a rolling
  **max** over ±0.10 s (occlusion can only shorten the run, so max-over-burst converges to truth from
  below), which validates against read text to 1 % (t = 858.2: method 0.405 vs `(8,179/20,005)` = 0.409).
  Nothing from the falsified pass survives anywhere in this file.
- **IS-H2-3 — the min-projection de-VFX instrument was built, validated, and then superseded.** Sliding
  per-pixel minimum over 60 fps bursts genuinely does suppress additive VFX and floating damage numbers
  (`method/burst.py`, kept for reuse), but it smears moving bodies and cannot beat the nameplate layer.
  Recorded so the next lap does not rebuild it.
- **IS-H2-4 — a nameplate detector without the text gate is not a detector.** Bar-only detection reported
  103 "plates" in a saturated frame at t = 820; with the measured white-text co-occurrence gate the same
  frame reports 15. Any red-run heuristic without that gate should be distrusted.

---

## Pins

| item | value |
|---|---|
| reference footage | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` |
| sha256 | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` — **re-verified EXACT at lap start** |
| format | 1920×1080, h264, 60 fps, 1034.10 s, 479,438,089 B |
| fight window used | 683.0 – 866.0 s (Lap H's in-frame bracket, unchanged) |
| `pm4h2_tracks.csv` | `13bb3033cb35012846343dcb077902304eb163a92cb8f7423ba8cf8074563818` (339 rows) |
| `pm4h2_ring_density.csv` | `a675367c9f46cedcb3413b3c43dfa0ac2aa0591c8ae120dcef05ce9a2f903eb5` (18 rows) |
| `pm4h2_movement_cadence.csv` | `1bfefb36926ed9a21faa175fb2d8cd2784cdce216abb547571c89f4220956156` (11 rows) |
| `pm4h2_observables.csv` | `61c25fab2f22c91fc8ee9260517a1e1e4fbdc8b09b1427f5f7551d9c4209c042` (9 rows) |
| `pm4h2_d1_range_profile.csv` | `63f2fc2c9beeeabe411accfadd4d3ea44726a1a277bf8a9e74c4b98272adada8` (8 rows) |

`eor-test-1` was **not** drawn from, consistent with Lap H's ruling that mining a second sitting after a
result on the reference footage is selecting substrate against an outcome.

---

## Layout

```
2026-08-13-kc2-pm4-lap-h2-video-match/
├── README.md                        ← this file
├── pm4h2_tracks.csv                 ← D1: every track attempted (339)
├── pm4h2_d1_range_profile.csv       ← D1: the decisive 8-band velocity decomposition
├── pm4h2_ring_density.csv           ← D2: the match target
├── pm4h2_movement_cadence.csv       ← D3: measured movement constants
├── pm4h2_observables.csv            ← D4: nine observables incl. two declared gaps
├── evidence/
│   ├── D1-radial-tangential-vs-range.png     ← the verdict, in one figure
│   ├── D1-exemplar-tracks.png                ← 6 named tracks, path + velocity
│   ├── D4a-corpse-carpet-748.00.jpg
│   ├── D4a-corpses-stood-upon-814.00.jpg
│   ├── D4a-corpse-carpet-836.00.jpg
│   └── D4c-eor-during-traversal-805.45-806.05.jpg
└── method/                          ← every script, reproducible from the pinned video
    ├── bars.py                      ← nameplate detector (bar + measured text gate)
    ├── extract.py                   ← whole-fight plate extraction
    ├── pbar.py                      ← player-plate pass (camera-lock proof + HP trace)
    ├── cammo2.py                    ← 60 fps gradient camera trace
    ├── ncc.py                       ← independent NCC validation of the trace
    ├── d1b.py / d1run.py / d1frames.py / d1dwell.py / d1final.py
    ├── d2.py                        ← ring density
    ├── burst.py                     ← min-projection de-VFX (built, superseded, kept)
    ├── camera_translation_60fps_683-866.npy
    ├── player_hp_frac_60fps.npy
    └── d1_profile_frames.npy        ← the 48,956-frame decomposition
```

Scratch extraction (several GB of intermediate frames) was written under `/tmp` and deleted; every
artefact here is regenerable from the pinned video with the scripts in `method/`.
