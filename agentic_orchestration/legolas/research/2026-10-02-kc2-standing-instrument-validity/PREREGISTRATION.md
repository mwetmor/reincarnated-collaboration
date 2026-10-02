# PRE-REGISTRATION: is the KC2 standing gap an instrument artefact? (like-for-like projection of the v3.10 oracle through the referent's Lap H-2 pipeline)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (RUN-CONDUCTOR), after KP-220 · **Written:** 2026-10-02
**Committed ALONE before any like-for-like number exists.** Read-only everywhere: the oracle runs from a `git archive` snapshot of engine `a329a544`; no engine, pack or footage file is touched. The Pi share is unmounted; everything below uses committed data only.
**Labels:** FOOTAGE (computed from the committed referent plate/camera arrays) · SIM (oracle) · INFERRED.

## 0 · What I ran before writing this, and what I saw (disclosed)

**Referent side (FOOTAGE; commission item 1, all computed from committed arrays: `lap-r/method/plates60_lapH2.npy`, `lap-h2/method/camera_translation_60fps_683-866.npy`, the Lap H-2 scripts unchanged except for paths):**

- **R0 reproduction:** the Lap H-2 range profile is reproduced exactly (48,956 frames; still fractions 0.201 / 0.229 / 0.283 / 0.279 / 0.336 / 0.346 / 0.243 / 0.145 by band 0–100 … 900–1400 gpx).
- **R1 what "range" means in the referent:** `d1b.kinematics` measures r from the monster's **plate anchor** to the player's **ground point** (960, 544). The plate sits about 115 screen px (≈ 214 gpx ≈ 1.75 m) above its own body's ground point (player's measured offset), so r is not the oracle's centre-to-centre distance. The "0–0.82 m" band contains no east, west or north contact bodies at all.
- **R2 camera compensation is sound:** per-frame plate screen steps follow the camera content step with slope 1.000 (x) and 1.054 (y); the camera's high-frequency jitter is real content motion (screen slope 1.09 on it), not trace error. Residual y excess 5.4 %.
- **R3 plate width:** inside 150 gpx, 35 % of census frames are narrow detections (w < 21 px); they read still 0.08 (150–300: 23 %, 0.10). Wide detections (w ≥ 40) read still 0.39 (0–150), 0.35 (150–300), 0.34 (300–600). Narrow detections cluster in a column over the player's sprite. They are not screen-locked artefacts (< 0.5 % screen-fixed while the camera moves).
- **R4 per-frame anchor noise:** inside 150 gpx, 35 % of linked raw steps exceed 12 gpx in one frame (≈ 1.8× the fastest walk), 76 % of those are vertical jumps ≥ 10 gpx (≥ 5 screen px); 29 % of links bridge missing frames. 300–600 gpx: 13 %, 7 %.
- **R5 glitch noise floor:** a body that never moves, carrying the referent's own transient residuals (raw − 9-frame median) through the identical 0.25 s boxcar + gradient + 50 gpx/s rule, reads still 0.634 / 0.726 / 0.756 / 0.812 (bands 0–300) and 0.895 / 0.940 (300–600). Persistent jumps are NOT in this floor.
- **R6 known-stationary proxy:** 21 referent segments where the robust (0.5 s median) position stays in a 20 gpx disc for ≥ 2.5 s; the instrument reads still 0.755 (0–150), 0.753 (150–300), 0.813 (300–600), 0.843 (600–1400) on them. No Carnivorous Plant can be bound to a plate track from committed data (its reads are hover-name reads with no screen position).

**Oracle side (SIM): trajectory capture only.** V310-FULL, salts 0–19, with an inert `Mover.step` wrapper recording pre-step positions, the player position, HP fraction and radius. **Replica exact:** the captured instrument leg reproduces gamora's step instrument to the third decimal (bands 0.91 / 0.888 / 0.87 / 0.851 / 0.64 / 0.467 / 0.512 / 0.51; inside 2.46 m 0.8674; 2.46–4.92 m 0.530; ratio ×1.847). One count was printed: visible-window bodies per tick mean 2.4 (the referent shows 8.9 plates per frame), and 5.1 % of visible body-ticks have HP < 19.4 % (the referent detector's 14-px minimum). **No like-for-like still fraction has been computed, printed or seen.**

## 1 · The like-for-like pipeline (fixed here; nothing is tuned after this file)

Positions: each body's pre-step position at tick k and the player's position at the same instant (instrument leg: the last invocation of each wave per salt, waves 151–160, salts 0–19). Linear interpolation to 60 fps.

Projection (Lap H-2's camera): player ground point fixed at screen (960, 544); body ground point X = 960 + S·(bx − px), Yg = 544 + S·K·(by − py), S = 122 gpx/m, K = 0.537, oracle +y = screen down. Plate anchor (x_left + 36) = X; plate `y` = Yg − 115. Visible window: x in [0, 1920), y in [60, 975), outside the Lap H-2 HUD rectangles. Population: roster bodies only (pets are not stepped by `Mover.step`; the referent's red plates are hostiles). Bar width w = round(72 · HP fraction).

Synthetic camera content shift = −S·Δplayer (x), −S·K·Δplayer (y). Then **the referent's exact code**: `d1b.world`, `d1b.track` (30 gpx gate, 12-frame gap), `d1b.kinematics` (15-frame boxcar, gradient), tracks ≥ 1.0 s (`d1frames.collect`), still = speed < 50 gpx/s, bands 0/100/150/220/300/400/600/900/1400 gpx. **Headline quantities: still fraction inside 300 gpx ("inside 2.46 m") and at 300–600 gpx ("2.46–4.92 m"), frame-weighted.**

Layers (each adds one difference, so the gap can be attributed):

| layer | what changes |
|---|---|
| N0 | the oracle's own step instrument (published; replica above) |
| N1 | true positions, centre-to-centre bands in metres, **referent velocity rule** (60 fps interpolation, 0.25 s boxcar, < 0.41 m/s); every body-frame, no tracking |
| N2 | N1 with the **referent's range definition** (plate anchor to player ground point, in gpx) |
| L0 | ideal detector: every visible plate at its rounded projected pixel, full referent tracking (≥ 1 s tracks) |
| L1 | L0 + the 14-px minimum bar width (HP < 19.4 % undetected) |
| L1g | L1 + the referent's own transient anchor residuals (R5), sampled from referent tracks of the same band (screen units) |
| L2 | rendered occlusion: plates painted in screen-y order (lower on top) as a dark frame + red fill + white text glyph columns 21–31 rows above, then the **exact `bars.find_bars`** (red mask, ≥ 3-row persistence, 14–90 px runs, text gate, dedupe) and the HUD filter |
| L3 | L2 + R5 residuals |

Sensitivity (reported, not graded): S = 119 / 125; plate offset 80 / 160 px; mirrored y; draw order reversed (L2).

## 2 · Predictions (V310-FULL, salts 0–19)

| # | quantity | prediction |
|---|---|---|
| Q1 | N1 inside 2.46 m / 2.46–4.92 m | 0.78–0.90 / 0.44–0.56 |
| Q2 | N2 inside 300 gpx / 300–600 gpx | 0.68–0.88 / 0.42–0.58 |
| Q3 | L1 inside / 300–600 | 0.65–0.88 / 0.40–0.57 |
| Q4 | L1g inside / 300–600 | 0.40–0.70 / 0.36–0.54 |
| Q5 | L2 inside / 300–600 | 0.45–0.78 / 0.38–0.56 |
| Q6 | L3 inside / 300–600 | 0.30–0.62 / 0.34–0.52 |
| Q7 | **Verdict:** under the most referent-like layer (L3; L1g as its bracket) the inside-2.46 m gap **SHRINKS by at least half but SURVIVES** (oracle still ≥ 0.33 vs the referent's 0.20–0.28) | — |
| Q8 | 2.46–4.92 m: the gap (0.530 vs 0.34) shrinks to ≤ +0.15 under L3 | — |
| Q9 | the oracle shows FEWER plate-visible bodies per frame than the referent (by ≥ 2×) | — |

## 3 · Pass / fail

Each row is HIT or MISS on its interval (a two-part row hits only if both parts do). The verdict is read from the numbers, not from the predictions. **No oracle rule is changed by this check.** If the gap does not survive, the corrected comparison is the like-for-like table, and mechanism work waits for it.
