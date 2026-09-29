# T4 — the video route, closed with numbers

**Question.** Kling and Ludo animated the same input: the knight's east still
`fal_t4/knight_E_ref_1024.png`, driven by our Meshy carry-walk video
`fal_t4/knight_carrywalk_E_drive.mp4`. Which one holds the character's identity
frame to frame — especially the helm, which is what the knight's per-frame
Astra paint failed on ("his helmet/head morph once each second whenever he
turns his head").

**Instrument.** The T1/T2 low-pass drift measure (`meshy_t2/scripts/21_drift.py`),
with one forced substitution: video has no pos guide, so pos-space matching
becomes 2D rigid registration. Method, the defects found while building it, and
the validation are in `METHOD.md`. Every number below is in `drift.json`.

**How to read the tables.** Lower is better everywhere except *planted travel*
and *cadence*, where the target is the drive's own value. Drift is mean |ΔRGB|
in 0–255 over the shared silhouette. The two `_floor_` rows cannot drift by
construction — they are what this instrument costs on a sequence with no drift.

### Table 1 — identity: does the helm hold?

| route | frames · fps | helm px | helm drift, **phase-matched** (lag=1/12 stride) med / p90 / max | helm drift raw f2f med | shuffled control | helm vs the still (min / med) | whole figure vs the still (min / med) |
|---|---|---|---|---|---|---|---|
| **Kling v3 Pro** motion-control | 150 · 30.0 | 174 | **4.66** / 8.02 / 24.90 | 2.44 | 7.34 | 3.85 / 7.03 | 13.82 / 21.57 |
| **Ludo** transfer-motion, hydra | 64 · 21.9 | 91 | **1.83** / 2.55 / 4.81 | 1.62 | 2.91 | 4.93 / 5.69 | 7.49 / 12.70 |
| **Ludo** transfer-motion, forge | 42 · 14.4 | 96 | **0.39** / 0.44 / 6.31 | 0.38 | 0.55 | 6.23 / 6.46 | 8.23 / 12.28 |
| **Ludo** animate-sprite, text 'walking' | 36 · 12.5 | 122 | **1.56** / 2.14 / 2.62 | 1.39 | 3.37 | 3.63 / 5.16 | 4.30 / 11.90 |
| _floor_ · the Meshy drive render | 150 · 30.0 | 94 | **1.78** / 5.93 / 8.22 | 1.01 | 3.33 | n/a | n/a |
| _floor_ · raw 3D render, 12-frame cell | 12 · 20.7 | 25 | **8.20** / 26.19 / 26.88 | 8.20 | 11.77 | n/a | n/a |
| _benchmark_ · Astra per-frame paint | 12 · 20.7 | 31 | **12.18** / 26.13 / 26.92 | 12.18 | 9.25 | n/a | n/a |

### Table 2 — walk quality, loop, cost

| route | cadence (strides/s) | vs drive | foot slip RMS (% fig. h) med / p90 | planted travel (% fig. h) | pollaxe: haft len CV · straightness · dAngle p90 | loop seam (body, 1.0 = clean) | cost | wall time |
|---|---|---|---|---|---|---|---|---|
| **Kling v3 Pro** motion-control | 0.88 | 1.00x | 1.02 / 5.24 | 16.8 | 26.3% · 0.86% · 2.78° | 2.36 | $0.84 | 180 s |
| **Ludo** transfer-motion, hydra | 0.73 | 0.83x | 2.02 / 3.39 | 29.2 | 25.1% · 1.16% · 0.21° | 3.17 | 15 cr | 347 s |
| **Ludo** transfer-motion, forge | 0.57 | 0.65x | 3.21 / 4.72 | 30.4 | 22.3% · 0.97% · 0.06° | 2.37 | 10 cr | 293 s |
| **Ludo** animate-sprite, text 'walking' | 0.70 | 0.79x | 2.41 / 3.56 | 22.1 | 30.0% · 0.89% · 1.53° | 2.79 | 9 cr | 501 s |
| _floor_ · the Meshy drive render | 0.88 | 1.00x | 4.11 / 7.27 | 16.9 | no weapon | 3.29 | 3 cr* | 6 s |
| _floor_ · raw 3D render, 12-frame cell | 1.73 † | 1.96x | n/m ‡ | n/m ‡ | 12.6% · 0.83% · 4.76° | 0.62 | -- | -- |
| _benchmark_ · Astra per-frame paint | 1.73 † | 1.96x | n/m ‡ | n/m ‡ | 2.6% · 0.70% · 0.28° | 1.36 | Astra seat | ~1 h/cell |

† no repeat found in the clip; the clip is one stride and the period is its length.
‡ not measurable: fewer than 16 frames per stride, see drift.json.
\* the drive is our own Meshy text-to-motion carry walk (10 cr to generate + 3 cr to apply), not a per-clip cost of this test.

### Table 3 — is the 2D fallback the same instrument? (both run on the knight's 12-frame Astra walk E)

| sequence | pos-matched body | pos-matched **head** | 2D body | 2D **head** |
|---|---|---|---|---|
| paint | 14.46 | 8.13 | 18.94 | 9.11 |
| render(floor) | 4.40 | 1.32 | 13.14 | 8.20 |
| paint shuffled(control) | 20.95 | 12.98 | 29.42 | 12.00 |

### Table 4 — what a drift number means (a known break, injected into the drive's helm)

| injected per-frame change | helm drift med | p90 |
|---|---|---|
| none (the floor) | 1.93 | 6.03 |
| helm scale +-1% | 1.90 | 6.01 |
| helm scale +-2% | 2.07 | 6.03 |
| helm scale +-4% | 2.46 | 6.61 |
| helm rotate +-1 deg | 2.01 | 6.02 |
| helm rotate +-2 deg | 2.33 | 6.09 |
| helm rotate +-4 deg | 3.53 | 6.37 |
| helm tone +-4/255 | 3.93 | 6.99 |
| helm tone +-8/255 | 6.49 | 9.94 |

Table 4's floor is 1.93 rather than Table 1's 1.78 because it runs on the first
60 drive frames rather than all 150. Read it as a conversion: **Kling's 4.66
is about a ±5° per-frame helm rotation. Ludo hydra's 1.83 and forge's 0.39 are
below the floor — no detectable change at all.** A ±1 % size change or a ±1°
turn does not register; this instrument cannot see those, and says so.

### Reading of the numbers

**Ludo holds the character; Kling redraws it.** Phase-matched helm drift: forge
0.39, anim 1.56, hydra 1.83 — all at or below the drive's own 1.78 floor.
Kling is 4.66, 2.6× the floor, p90 8.02, max 24.90 in a cluster at frames
86–97. On the whole figure against the source still, Kling is 13.8 at its
*best* frame and 21.6 median; Ludo sits at 7.5–8.2 best and 11.9–12.7 median.
The strip shows it: Kling restages the pollaxe, loses it from the crop
entirely at f106, and changes the gorget between frames.

**But Kling is the only one that reproduced the motion.** Its cadence is 0.882
strides/s — the drive's value to three decimals — and its planted foot travels
16.8 % of figure height per contact against the drive's 16.9. Ludo's
transfer-motion came back at 0.73 (hydra) and 0.57 (forge) strides/s, 17 % and
35 % slow, with feet travelling ~30 %. Ludo did not transfer the gait it was
given; it produced *a* walk. (Playback fps is ours to set, so the strides/s can
be dialled back; the frames-per-stride and the stride *length* cannot.)

**Ludo's identity score is partly won by not animating.** The registration
shift needed to align consecutive helms is 0–1 px for all three Ludo routes and
16 px — the search edge — for Kling. Forge's helm does not move at all: drift
0.38, below the floor, eight visually identical frames in the strip, pollaxe
angle steady to 0.06°. A head that never bobs cannot morph. Kling's 16 px cap
also means some of its residuals are *lower* bounds on its true drift.

**Nothing loops.** Ludo's sheet is documented as trimmed to its best loop. The
absolute helm seam is 6.45 (forge), 6.51 (hydra), 7.81 (anim) — as large as
each route's own distance from the reference still (5.2–6.5). The last frame
differs from the first by as much as either differs from the source art. Body
seam ratios are 2.4–3.2 against a clean 1.0.

**Against the benchmark.** The Astra per-frame paint reads 12.18 against its
own resolution-matched floor of 8.20 — 1.49×. Ludo hydra reads 1.83 against
1.78 — 1.03×. So on the helm Ludo is genuinely steadier than the paint Matt
rejected. The comparison is *directional, not quantitative*: the Astra cell has
31 px of helm at 12 frames per stride, where the instrument has eight times
less headroom, and Table 3 shows the 2D fallback separating paint from floor by
only 1.11× on the head where the pos-matched instrument gets 6.16×.

### Cost for one character, 8 directions × 4 actions = 32 clips

| route | per clip | × 32 | serial wall | note |
|---|---|---|---|---|
| Kling v3 Pro motion-control | $0.84 | **$26.88** | 1.6 h | needs a drive video per direction × action |
| Ludo transfer-motion, hydra | 15 cr | **480 cr** | 3.1 h | 47 % of the charter's 1,030-credit balance |
| Ludo transfer-motion, forge | 10 cr | **320 cr** | 2.6 h | 31 % of the balance |
| Ludo animate-sprite, text | 9 cr | **288 cr** | 4.4 h | no motion control: 8 directions would not agree |

The Ludo credit-to-dollar rate is not recorded anywhere on disk; credits are
reported as charged by the API. **Neither route removes the 3D work**: both
consume a drive video per direction × action, which only the Meshy rig
produces, and a reference still per direction, which is an Astra paint. The
video branch replaces the per-frame paint step, not the backbone.

### Verdict

1. **Ludo transfer-motion (hydra) is the only route that holds identity well
   enough to consider** — helm drift at the instrument's floor, whole figure
   within 12.7 of the source still, pollaxe rigid to 0.21° — and it is the one
   to use if the video branch is used at all.
2. **Kling is disqualified on identity, not on motion**: it is the only route
   that reproduced the drive's cadence and foot contact exactly, and the only
   one that redesigns the character while doing it (21.6 against the still, a
   restaged pollaxe, a 24.9 helm excursion at frames 86–97).
3. **No route is good enough to be the video branch as a backbone**, because
   every one of them fails a different half of the job: Ludo holds the face and
   loses the gait, Kling holds the gait and loses the face, and none of the
   three Ludo sheets loops despite being trimmed for it.
4. **Ludo is worth keeping as a reference-motion and concept tool**, at 480
   credits per character — 2.1 characters on the current balance — which is too
   expensive to be a roster pipeline and cheap enough to be a look-development
   aid.
5. **The result that should change the plan is the Astra comparison**: the
   per-frame paint Matt rejected reads 1.49× its own floor where Ludo reads
   1.03×, so per-frame generation *is* the drift source, and the fix is a route
   where the helm is not regenerated per frame at all — the rig or the
   EbSynth-propagation path, not a different video model.

### Artefacts

| file | what |
|---|---|
| `drift.json` | every number above, per route, with per-frame worst cases |
| `fallback_check.json` | the two instruments side by side (Table 3) |
| `sensitivity.json` | the known-break calibration (Table 4) |
| `helm_strip.png` | 8 evenly spaced helms per route, fixed crop, scale-normalised |
| `helm_quad.mp4` | the four candidate helms at 2×, each at its own fps |
| `METHOD.md` | how the instrument works and the four defects found building it |

`helm_strip.png` (3.8 MB) and `helm_quad.mp4` (1.0 MB) are **not committed**
(binaries); they sit in `runs/C-9/t4_close/` on disk.
