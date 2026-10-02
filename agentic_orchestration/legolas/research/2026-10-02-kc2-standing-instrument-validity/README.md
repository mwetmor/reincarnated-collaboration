# Research: is the KC2 standing gap an instrument artefact? (2026-10-02)

**Mode:** A (analytical: an instrument-validity check, with the referent's pipeline reproduced from committed data and the oracle projected through it like for like)
**Commissioner:** gandalf (RUN-CONDUCTOR), after KP-220. **Agent:** legolas (UNKNOWN-RESEARCHER).
**Read-only everywhere.** The oracle ran from a `git archive` snapshot of engine `a329a544`, with an inert `Mover.step` capture. The capture reproduces gamora's numbers exactly (ratio ×1.847; step standing by band to the third decimal). No engine, pack or footage file was touched. The Pi share is unmounted, so only committed arrays were used.
**Labels:** FOOTAGE · SIM · INFERRED.
**Pre-registration:** `PREREGISTRATION.md`, committed ALONE at collab `1865b7a92` before any like-for-like number existed. Its § 0 discloses everything computed beforehand: the referent diagnostics R0–R6 and the capture replica.

**Sources:**
- Lap H-2 method scripts, unchanged apart from paths (`legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/method/`: `bars.py`, `extract.py`, `d1b.py`, `d1run.py`, `d1frames.py`).
- The Lap H-2 camera trace `camera_translation_60fps_683-866.npy`.
- The raw 60 fps plate detections `legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/method/plates60_lapH2.npy` (98,794 monster plates).
- Lap R scale bracket (119–125 gpx/m).
- The roster packet (`2026-10-02-crucible-enemy-roster-packet`).
- The v3.10 composition script (`gamora_kc2_play_v3p10_oracle_2026_10_02.py`) and gamora's pass-3 results.

---

## Verdict

**The gap survives a like-for-like instrument, but it is about 40 % of its published size. Its "concentrated inside 2.46 m" shape is largely an instrument artefact.**

| | inside 2.46 m (300 gpx) | 2.46–4.92 m (300–600 gpx) |
|---|---|---|
| referent (FOOTAGE; 95 % wave-bootstrap) | **0.256** [0.211, 0.291] | **0.343** [0.285, 0.413] |
| oracle, published step instrument (N0) | 0.867 (gap +0.61) | 0.530 (gap +0.19) |
| **oracle through the referent's pipeline, most referent-like layer (L3)** | **0.487** (chunk range 0.452–0.517) | **0.455** (0.427–0.479) |
| ↳ bracket layer L1g (per-salt mean ± sd) | 0.490 ± 0.055 | 0.459 ± 0.031 |
| **like-for-like gap** | **+0.23** (≈ +0.17 … +0.29) | **+0.11** (≈ +0.04 … +0.17) |

The instrument accounts for about 62 % of the inside-2.46 m gap and about 40 % of the 2.46–4.92 m gap. **What survives is about +0.2 in every band.** It is smallest at 2.46–4.92 m (+0.11) and larger both inside (+0.19 … +0.33) and beyond 4.92 m (+0.22 … +0.37). It is **not** a contact-only deficit.

## 1. How the referent's standing fraction is measured (FOOTAGE; commission item 1)

**The pipeline (reproduced exactly, R0).**
- Each monster's plate is detected per frame at 60 fps: a red 3-row bar, 14–90 px wide, with the white `(cur/max)` text gate. The anchor x is `x_left + 36`; the anchor y is the bar row.
- Plates are moved to world coordinates by subtracting the cumulative camera content shift. Ground px = (x, y/0.537).
- Plates are linked by greedy nearest neighbour (gate 30 gpx, gaps up to 12 frames). Only tracks ≥ 1.0 s are kept.
- Velocity is a 15-frame (0.25 s) boxcar on position, then `np.gradient`. A frame is "still" if speed is below 50 gpx/s (0.41 m/s at 122 gpx/m).
- Bands use r in gpx, converted to metres at 122.

**Findings:**

1. **Range is measured from the plate to the player's GROUND point (R1).** `d1b.kinematics` measures r from the monster's plate anchor to the player's ground point at (960, 544). It does not measure ground to ground.
   - The plate sits about 115 screen px above its own body's ground point (the player's measured plate-to-ground offset). That is about 214 gpx, or 1.75 m.
   - So the referent's "0–0.82 m" band holds no east, west or north contact bodies. It holds bodies about 1.75 m due south.
   - The referent's "inside 2.46 m" includes bodies up to about 4.2 m away to the south.
   - Lap H-2 noted the bias ("only absolute range carries the plate-height bias") but did not correct it. The residual hunt later read the gpx bands as metres against the oracle's centre-to-centre distance.
   - **This single definitional difference is the largest instrument term: −0.20 inside 2.46 m on the oracle (N1 → N2).**
   - Re-banded to centre-to-centre (offset 115 px), the referent itself reads **0.355 inside / 0.294 at 2.46–4.92 m**. The ordering flips: inside-contact bodies stand *more* than mid-band ones (`results/reband.json`; offset 80 / 160 px gives 0.311–0.389 / 0.277–0.326).
2. **Camera compensation is sound (R2).** Plate screen steps follow the camera content step with slope 1.000 in x and 1.054 in y. The trace's large high-frequency jitter (sd about 3 px per frame) is real content motion that the plates share, not trace error. Camera shake and the player's own motion cancel. A residual 5 % y-parallax remains (≤ 25 gpx/s during runs). It is not decisive.
3. **Plates at contact are noisy, fragmented and partly truncated (R3–R5).**
   - Inside 150 gpx, 35 % of linked raw steps exceed 12 gpx in one frame (about 1.8× the fastest walk). Three quarters of these are vertical jumps of ≥ 5 screen px. 29 % of links bridge missing frames. At 300–600 gpx the figures are 13 % and 7 %.
   - The plate anchor does move when the body does not. The jumps are mostly vertical and concentrated where plates crowd. **INFERRED:** they are re-linking between stacked plates, or GD offsetting overlapping plates. Telling these apart needs frames.
   - Narrow detections (w < 21 px) are 35 % of census frames inside 150 gpx and read still 0.08. Wide plates there read 0.39.
   - **Noise floor:** a body that never moves, carrying the referent's own transient anchor residuals, reads still only **0.63 / 0.73 / 0.76 / 0.81** in the four bands inside 300 gpx and 0.90 / 0.94 at 300–600 gpx (`results/noisefloor.json`). Persistent jumps are excluded, so this is optimistic.
4. **Known-stationary calibration (R6).**
   - **The Carnivorous Plant cannot be bound to a plate track from committed data.** Its four referent reads (692.2, 694.8, 698.4 and 722.5–722.9 s) are hover-name reads with no screen position.
   - Proxy used instead: 21 segments where a track's robust (0.5 s median) position stays within 20 gpx for ≥ 2.5 s. On these the instrument reads still **0.755 / 0.753 / 0.813 / 0.843** (0–150 / 150–300 / 300–600 / 600–1400 gpx), so even a held body loses about 20 %. Selection favours clean tracks, so this is an upper bound on fidelity.
   - **The plant calibration proper needs raw frames (T33):** the plant's screen position at 692–698 s and 719–729 s.
5. **Population (commission item 3).**
   - The referent counts plate-visible hostiles: red plates, with HP ≥ 19.4 % (the 14-px minimum run).
   - Plates appear for trash too. Only 5–22 % of plate detections are full-width, and w159/w160 show 10.4 / 8.9 plates per frame against rosters of 5.5 / 4, so **summoned bodies carry plates**. The oracle does not have summoned bodies as movers: every captured mover is a roster `wNNN_aNNN`.
   - **Pets** are not in either census. The referent detector is red-only, and in the oracle pets are not stepped by `Mover.step`, so gamora's step instrument already excludes them.
   - **The oracle puts far fewer bodies on screen:** 2.1 plate-visible bodies per frame against the referent's 8.95. 7 % of the oracle's body-steps fall inside 2.46 m, against 30 % of the referent's census frames.

## 2. The like-for-like projection (SIM; commission item 2; V310-FULL, salts 0–19)

**Setup:**
- Oracle body positions and the player position are captured per tick and interpolated to 60 fps.
- They are projected into Lap H-2's screen geometry: player ground point fixed at (960, 544), S = 122 gpx/m, K = 0.537, plates 115 px above the ground point, bar width 72 × HP.
- Then they run through the **referent's own code**: `d1b.world`/`track`/`kinematics`, tracks ≥ 1 s, the < 50 gpx/s rule, the same bands. Each layer adds one difference (`tools/lfl.py`).

| layer | adds | inside 2.46 m | 2.46–4.92 m | Δ inside |
|---|---|---|---|---|
| N0 | the oracle's step instrument (published) | 0.867 | 0.530 | |
| N1 | the referent's velocity rule (60 fps, 0.25 s boxcar, < 0.41 m/s) | 0.858 | 0.496 | −0.009 |
| N2 | **the referent's range definition (plate → player ground)** | 0.661 | 0.511 | **−0.197** |
| L0 | ideal plate detection + the referent's tracking (≥ 1 s tracks) | 0.651 | 0.510 | −0.010 |
| L1 | the 14-px minimum bar (HP < 19.4 % undetected) | 0.618 | 0.489 | −0.033 |
| L2 | rendered occlusion (painted plates and text, then the exact `bars.find_bars`) | 0.616 | 0.486 | −0.002 |
| L1g | L1 + the referent's transient anchor residuals by band | 0.488 | 0.458 | −0.130 vs L1 |
| **L3** | **L2 + the referent's transient residuals** | **0.487** | **0.455** | **−0.129** |
| referent | | **0.256** | **0.343** | |

Per band, L3 against the referent (gpx bands 0–100 … 900–1400):

| | 0–100 | 100–150 | 150–220 | 220–300 | 300–400 | 400–600 | 600–900 | 900–1400 |
|---|---|---|---|---|---|---|---|---|
| L3 | 0.53 | 0.54 | 0.49 | 0.47 | 0.45 | 0.46 | 0.46 | 0.51 |
| referent | 0.20 | 0.23 | 0.28 | 0.28 | 0.34 | 0.35 | 0.24 | 0.15 |
| gap | +0.33 | +0.31 | +0.21 | +0.19 | +0.12 | +0.11 | +0.22 | +0.37 |

**Sensitivity** (`results/sensitivity/`):
- On L1g, inside 2.46 m reads 0.43–0.55 across S = 119/125, plate offset 80/160 and mirrored orientation. 2.46–4.92 m reads 0.45–0.51.
- On L2 (salts 0–4), reversed draw order gives 0.648 inside (base chunk 0.649).
- Every variant stays above the referent's 95 % upper bound in both bands (0.291 inside, 0.413 at 2.46–4.92 m). The closest are L1g OFF160 inside (0.431) and L1g OFF0/OFF80 at 2.46–4.92 m (0.447).
- Mirroring raises the oracle by about 0.05, because the plate offset interacts with the arena's geometry.

**Scorecard (pre-registration `1865b7a92`): 7 HIT, 2 MISS.**
- **Q2 and Q3 missed (0.661 and 0.618 against floors of 0.68 and 0.65).** The range-definition term was larger than I expected.
- Q7 hit (the inside gap shrinks from 0.61 to 0.23 and survives) and Q8 hit (the mid-band gap is +0.11).
- Q9 hit: the oracle shows 4× fewer plate-visible bodies per frame.

## 3. What the like-for-like does NOT emulate (each makes the oracle read too HIGH, so the surviving gap is an upper estimate)

1. **Persistent jumps and dropouts at the referent's crowd density.** The oracle's crowd is sparse (2.1 plates per frame), so rendered occlusion barely bites (L1 → L2 −0.002). The referent's anchor relocations (steps > 12 gpx on 11–19 % of contact frames) come from crowding the oracle does not reach. Injecting only *transient* residuals leaves these out.
   - **To close the inside gap fully,** the missing terms would have to flip a further 47 % of the oracle's still-readings to moving. That would mean a held body reads still only about a third of the time. The known-stationary proxy (0.75) does not support so large a term (INFERRED; that proxy is itself favourably selected).
2. **Summoned bodies** are in the referent's population and absent from the oracle's.
3. **Per-record plate height.** One 115 px offset is used for all bodies. Big bodies sit higher, which strengthens the range-definition term (offset 160: L1g inside 0.43).

## 4. Corrected comparison and the bearing on mechanism work

- **Stop comparing the step instrument with the referent's 0.34 / 0.20–0.28.** The like-for-like statement is **0.49 vs 0.26 inside 2.46 m and 0.46 vs 0.34 at 2.46–4.92 m (plate-to-ground bands)**. Equivalently, on centre-to-centre bands: the referent re-banded reads 0.36 / 0.29, and the oracle under referent noise (L1g, offset 0) reads 0.66 / 0.45.
- **Mechanism work is still warranted, but on a different target** (INFERRED):
  - The residual is about +0.2 at every range, smallest at 2.5–5 m. It is not a contact-jostle deficit.
  - The largest single disagreement is now **crowd geometry**: the referent has 4× more bodies within the screen window (about 8 m). The oracle's bodies stand at range (still 0.46–0.51 beyond 4.9 m, against the referent's 0.15–0.24, where referent bodies are mostly approaching).
  - The candidate leads are ones that put bodies close and keep them moving: the referent's own line-up and summons (T33; seed 9 is declared extreme), and the undecoded knockback/stun recovery. More contact-only rules are less likely to help.
- **Any future standing comparison should use `tools/lfl.py` (layer L3, or L1g as its fast bracket),** not the step instrument.

**What raw frames would settle (waits for T33):**
1. Frame reads at contact: does GD offset or stack overlapping nameplates? This would explain the 76 % vertical share of the jumps.
2. The Carnivorous Plant's screen position at 692–698 s and 719–729 s, for a true known-stationary calibration.
3. Plate heights per family (the offset term).

## Files

| file | contents |
|---|---|
| `PREREGISTRATION.md` | predictions and pipeline; committed alone at `1865b7a92` |
| `results/results_table.json` | every layer, per-salt spread, chunk values, sensitivity, grading |
| `results/lfl_*.json` | per-layer counts by band and per wave (N1, N2, L0, L1, L1g, L2, L3) |
| `results/sensitivity/*.json` | S, plate offset, mirror and draw-order variants |
| `results/noisefloor.json` · `stationary.json` · `reband.json` | referent instrument diagnostics R5, R6 and the centre-to-centre re-banding |
| `results/resid_pools.npz` | the referent's transient anchor residuals by band (the L1g/L3 noise) |
| `results/oracle_capture_replica_summary.json` | the capture's oracle summary (replica of gamora's V310-FULL) |
| `tools/capture_oracle.py` · `select_legB.py` | inert trajectory capture; selection of the instrument leg (last invocation per wave, salts ≥ 0) |
| `tools/lfl.py` · `merge.py` | the like-for-like layers |
| `tools/repro.py` · `collect2.py` · `camhf2.py` · `screenlock.py` · `jitter.py` · `jumps.py` · `noisefloor.py` · `stationary.py` · `pools.py` · `reband.py` | referent diagnostics |

**Reproducing.** The tools expect the Lap H-2 method scripts beside them in a `ref/` directory, with `plates60.npy` (= Lap R `plates60_lapH2.npy`) and `cam60g.npy` (= the Lap H-2 camera trace). They also expect `cap/legB_rows.npy` from `capture_oracle.py V310-FULL 0-19` (run from a snapshot of engine `a329a544`, then `select_legB.py`). The capture arrays (about 30 MB) are regenerable and not committed.

*legolas · KC2-PLAY · KP-220 instrument-validity check · 2026-10-02*
