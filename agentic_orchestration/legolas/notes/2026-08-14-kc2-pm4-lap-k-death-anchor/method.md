# KC2-PM4 — Lap K — death-anchor decode (method + basis)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Run:** KC2-PM4, Lap K · **Date:** 2026-08-14
**Class:** primary-source probe — first-of-kind measurement of a player-death event from raw video.

---

## Headline finding

**The death is an instant full-to-zero one-shot.** At `t = 864.7333 s` the player is at
`20005 / 20005` HP — exactly full. `0.0834 s` later (5 frames at 60 fps) the readout is `0`.
The player had been at or above `0.9926` health fraction for the preceding **1.6166 s**, having
completed a *full* recovery from the last damage excursion at `t = 863.1167 s`.

**Lap H-2's tail-claim — "a 6.55 s collapse, then death" — is SUPERSEDED.** That event measures,
at exact-readout resolution, as a **recovery**: HP falls from full at `855.7000`, floors at
`0.291877` (`5839 / 20005`) at `859.9500`, and climbs back to `1.0000` at `863.1167`. The player
survives it completely. Death is a **separate, later, unrelated-in-shape event** 1.62 s afterwards.
Any downstream reading of "the character was ground down and expired" is wrong: the character was
at full health and was deleted in a single 83-millisecond window.

**Corroborating instrument-defect finding.** L-18 (commit `f951bf30`) recorded that the evidence
file's trace "ends `t=864.833` hp=`0.9595` **ALIVE** after full recovery". Put that beside the exact
readout: at `t = 864.8333` this instrument reads **`0 / 18065`** — the frame *after* death, with
buffs already shed. The Lap H-2 nameplate-bar instrument reported 95.95 % health at the exact frame
the game itself printed zero. The bar sprite lags the underlying value (or the instrument tracked
the wrong element); either way the ≈1 %-resolution bar instrument is not merely imprecise near
death, it is **qualitatively wrong** there — it reported *alive at near-full* at a frame where the
character was dead. This is an independent reason to treat every H-2-derived terminal claim as
unsafe, and it is why I-1 (which reads the game's own printed integers) supersedes it outright.

Corroborating detail: the `max` field drops `20005 → 18065` on the **frame after** zero
(`864.8333`), i.e. buffs shed on death. The 1940-HP delta is buff-granted maximum, present at the
moment of the killing blow. The one-shot therefore removed **20,005 HP**, not 18,065.

---

## Substrate

| Field | Value |
|---|---|
| File | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` |
| sha256 | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` — **verified in full this session**; matches the charter-recorded prefix `4c60960d98e9d729` |
| Geometry | 1920 × 1080, 60 fps, 1034.10 s |
| Content | Grim Dawn Crucible, Warlord, displayed waves 151 → 160 |

---

## Instrument stack

All four instruments are **MEASURED** (they read the game's own rendered output). None is inferred,
modelled, or carried over from a prior lap's estimate.

**I-1 — HP-orb OCR (exact instrument).**
Fixed screen ROI `x 578..696, y 1009..1021`; white-ink mask (`R>140 ∧ G>140 ∧ B>128`);
column-gap glyph segmentation; per-glyph nearest-template NCC against templates built from
cluster medoids of 14,583 harvested glyph bitmaps (`glab.npy` / `gbmp.pkl`), **labelled by reading
the rendered medoids**, not by assumption. Reader is the hardened `read_hard2` variant with four
rejection gates:
- **G1** per-glyph NCC ≥ 0.78
- **G2** glyph box width within ±2 px of the matched template's modal width — kills the
  merged-glyph / dropped-digit failure mode
- **G3** no box touching the ROI edge (no clipping)
- **G4** strip up to one leading and one trailing *junk* box (best NCC < 0.55) — transient VFX ink
  abutting the string. Self-correction **D-K-2**: without G4, 289 fight frames (2.6 %) were lost to
  a single spurious trailing glyph, all inside `861.2–862.1`.

This instrument reads the game's own printed integers `cur/max`. It **supersedes** Lap H-2's
nameplate-bar-width instrument (≈1 % resolution). Coverage: `675.0000 → 884.9833` at 60 fps,
12,600 samples, **363 rejected (2.88 %)**, emitted as empty fields in `pm4k_full_trace.csv`.
Rejection is *conservative by design*: a rejected frame is a frame the gates would not certify, not
a frame with no HUD. The largest rejection block (`867.6500 → 870.2667`, 158 frames) is the
death-fade + respawn, where the orb genuinely is not rendered.

**I-2 — wave-counter reader (exact instrument).**
Crucible HUD red wave numeral, fixed ROI `x 1580..1650, y 138..168`.
Feature = "redness" `R − max(G,B)`, clipped at 0. Greedy NCC clustering (threshold 0.90) over all
2,068 frames of a 2 fps full-video pass; ink < 2000 ⇒ blank. Cluster→value labels read from the
rendered medoids. **Re-derived in this session at 60 fps** (see § Resumed vs re-derived).

**I-3 — nameplate census + contact ring (lower-bound instrument).**
`bars.find_bars` (Lap H-2 instrument, text-gated). Nameplate count is a **LOWER BOUND** on living
monsters — corpses carry no plate, and off-screen or occluded monsters are invisible to it.
Contact ring = plates within `R = 150` ground px of the player anchor `(960, 429)`, ground plane
de-projected by `K = 0.537` (Lap H-2 D2 calibration).

**I-4 — colour-class VFX ink + combat-text runs (descriptive instrument).**
Six saturated colour classes as *fractions of screen pixels*. **These are COLOUR classes, not
damage-type claims** — `fire_red` means red-dominant saturated ink, not fire damage. Boss/hero
banner = red run detection in `x 700..1220, y 0..40`. Combat text = bright text-run count in the
world layer `y 120..900, x 200..1500`.

---

## GL-12 basis grades (NOTE-9 — every quantity asserts its basis)

| Quantity | Basis | Grade | Resolution |
|---|---|---|---|
| `death_t_s = 864.8167` | I-1, exact printed integer | **MEASURED** | ±1 frame (0.0167 s) |
| `hp_cur`, `hp_max` (all rows) | I-1, exact printed integer | **MEASURED** | exact (integer readout) |
| `instant_kill_span_s = 0.0834` | I-1, frame difference | **MEASURED** | ±1 frame |
| Wave spans (all 10) | I-2 at 60 fps | **MEASURED** | ±1 frame |
| `tod_s = 182.7167` | arithmetic on two MEASURED times | **DERIVED-from-MEASURED** | ±2 frames |
| Collapse start / floor / end | I-1 + a stated threshold | **MEASURED (threshold-defined)** | ±1 frame |
| `post-death-fade` bounds | I-1 (start) + I-2 (end) at 60 fps | **MEASURED** | ±1 frame |
| Fade *brightness* profile | 2 fps global pass | **MEASURED, coarse** | ±0.5 s |
| `black-tail` start `1029.0000` | 2 fps global pass | **MEASURED, coarse** | ±0.5 s; true transition ∈ (1028.5, 1029.0] |
| `pre-fight` sub-structure | 2 fps global pass | **MEASURED, coarse** | ±0.5 s |
| `plates_*` (deep-burst rows) | I-3 | **MEASURED LOWER BOUND** | — |
| `ring_*` (deep-burst rows) | I-3 + K=0.537 de-projection | **MEASURED LOWER BOUND, calibrated** | — |
| Colour-class fractions | I-4 | **MEASURED, descriptive** — *not* damage-type | — |
| Anything about *what killed the player* | — | **NOT MEASURED. Absent.** | — |

The last row is load-bearing. This lap anchors *when* and *how fast*. It does **not** identify the
damage source. `pm4k_deep_bursts.csv` describes what was on screen; it does not attribute.

---

## Wave-span table (I-2, 60 fps, MEASURED)

Method: 60 fps ROI extraction over `678.0000 → 874.9833` (11,820 frames). For each of the ten
displayed values, a template was formed as the mean normalised redness feature over the 2 fps
frames falling inside that wave's *core* interval (boundaries excluded). Each 60 fps frame was
assigned by max NCC, accepted at NCC ≥ 0.90 ∧ ink ≥ 2000, else blank.

| Wave | first frame reading it | last frame reading it | duration (s) | gap to next flip (s) |
|---|---|---|---|---|
| 151 | 682.1000 | 698.3667 | 16.2667 | 0.0166 |
| 152 | 698.3833 | 714.6333 | 16.2500 | 0.2167 |
| 153 | 714.8500 | 729.6000 | 14.7500 | 0.0167 |
| 154 | 729.6167 | 743.7333 | 14.1166 | 0.0167 |
| 155 | 743.7500 | 760.0667 | 16.3167 | 0.0166 |
| 156 | 760.0833 | 780.2833 | 20.2000 | 0.2834 |
| 157 | 780.5667 | 799.4167 | 18.8500 | 0.0166 |
| 158 | 799.4333 | 812.5333 | 13.1000 | 0.0167 |
| 159 | 812.5500 | 838.8500 | 26.3000 | 0.0167 |
| 160 | 838.8667 | **868.3167** | 29.4500 | — |

**Death at `864.8167` falls inside wave 160**, 25.9500 s after that wave's counter appeared and
3.5000 s before the counter vanishes into the death fade.

Sub-second blanks at each flip are the numeral's own re-render, not measurement dropout. The spans
are therefore *first-visible → last-visible*, not a forced contiguous partition; that is the honest
form and it is why `pm4k_segments.csv` carries ≤0.28 s gaps between consecutive wave rows.

**Post-death note (previously unrecorded):** the wave-160 numeral **returns** at `869.8667` and is
readable through `874.9833` (end of the 60 fps window), and the 2 fps pass shows the counter ROI
occupied until `943.0`. The Crucible run does not end at the player's death — the counter persists
across the respawn. Any "run ended at wave 160" claim should be phrased as "player died during
wave 160", which is a different statement.

---

## The terminal sequence — verbatim, frame by frame

I-1 readout, `864.5833 → 864.9167`. Blank cells are gate rejections (there are none in this span).

| t_s | hp_cur | hp_max | hp_frac |
|---|---|---|---|
| 864.5833 | 20005 | 20005 | 1.000000 |
| 864.6000 | 20005 | 20005 | 1.000000 |
| 864.6167 | 20005 | 20005 | 1.000000 |
| 864.6333 | 20005 | 20005 | 1.000000 |
| 864.6500 | 20005 | 20005 | 1.000000 |
| 864.6667 | 20005 | 20005 | 1.000000 |
| 864.6833 | 20005 | 20005 | 1.000000 |
| 864.7000 | 20005 | 20005 | 1.000000 |
| 864.7167 | 20005 | 20005 | 1.000000 |
| **864.7333** | **20005** | **20005** | **1.000000** ← last full-health frame |
| 864.7500 | 2118 | 20005 | 0.105874 |
| 864.7667 | 2222 | 20005 | 0.111072 |
| 864.7833 | 703 | 20005 | 0.035141 |
| 864.8000 | 703 | 20005 | 0.035141 |
| **864.8167** | **0** | **20005** | **0.000000** ← DEATH |
| 864.8333 | 0 | **18065** | 0.000000 ← buffs shed (max drops 20005 → 18065) |
| 864.8500 | 0 | 18065 | 0.000000 |
| 864.8667 | 0 | 18065 | 0.000000 |
| 864.8833 | 0 | 18065 | 0.000000 |
| 864.9000 | 0 | 18065 | 0.000000 |
| 864.9167 | 0 | 18065 | 0.000000 |

Read this literally. In **one frame** (`864.7333 → 864.7500`) the player loses **17,887 HP —
89.4 % of maximum**. The remaining four frames are the tail. The `2118 → 2222` uptick at
`864.7667` is a real +104 HP (regen or a leech tick landing between damage instances), not an OCR
artefact — both readings pass all four gates.

**`instant_kill_span_s = 864.8167 − 864.7333 = 0.0834 s`** (5 frames at 60 fps).

---

## The final pre-death excursion — the event Lap H-2 mislabelled

Threshold, stated: an *excursion* **starts** at the first frame with `hp_frac < 0.95` and **ends**
at the first subsequent frame with `hp_frac ≥ 0.99`. Both thresholds are on the exact printed
readout, so they are hard, not fitted.

| Quantity | Value | Note |
|---|---|---|
| `collapse_start_t_s` | **855.7000** | first frame `< 0.95`; last frame `≥ 0.99` before it was `855.1333` |
| `collapse_floor` | **0.291877** | `5839 / 20005` |
| `collapse_floor_t_s` | **859.9500** | |
| `collapse_end_t_s` | **863.1167** | first frame `≥ 0.99`; it reads exactly `1.0000` |
| `collapse_duration_s` | **7.4167** | `863.1167 − 855.7000` |
| `hp_max` throughout | `20005`, unchanged | no buff shed during the excursion |
| Full-health dwell before the one-shot | **1.6166 s** | `863.1167 → 864.7333`; `hp_frac ≥ 0.992602` for every one of the 96 frames, zero gate rejections |

The player recovers **completely** — `20005 / 20005` — and holds it for 1.62 s. The one-shot then
lands out of a full bar.

**Context:** 26 excursions of ≥ 0.5 s duration occur across waves 151–160. The `855.70` excursion
is the *deepest survived* one at `0.2919`; the next deepest is `843.4000 → 846.5000` floor `0.2679`,
also survived, also in wave 160. Deep excursions are routine in this fight and are routinely
survived. That is precisely why the death does not read as attrition.

---

## Post-death sequence

| t_s | event | basis |
|---|---|---|
| 864.8167 | HP reads `0 / 20005` — death | I-1 |
| 864.8333 | `max` drops to `18065` — buffs shed | I-1 |
| 864.8333 → 867.6333 | HP held at `0 / 18065`, world still rendered, wave counter still reads 160 | I-1, I-2 |
| 867.6500 | HP orb readout no longer certifiable — fade begins | I-1 (gate rejection block start) |
| 868.3167 | last frame the wave numeral `160` is readable | I-2, 60 fps |
| 868.0 → 869.5 | screen fade: 2 fps frame brightness `25.5 (867.0) → 4.05 (868.0) → 0.24 (869.0)`; orb-ink exactly `0` across the span | 2 fps global pass, ±0.5 s |
| 869.8667 | wave numeral `160` returns — respawn readout up | I-2, 60 fps |
| 870.2833 | HP readout returns **`18065 / 18065`** — respawned at full, un-buffed | I-1 |
| → 1028.5 | content continues (2 fps pass); wave-counter ROI occupied to `943.0` | 2 fps global pass |
| 1029.0000 | frame brightness exactly `0.000` — black tail to EOF `1034.10` | 2 fps global pass, ±0.5 s |

Note the respawn maximum equals the post-death maximum (`18065`), confirming the `20005` figure was
buffed and the buffs did not survive death. **The killing blow therefore had to overcome 20,005 HP.**

---

## Time-on-death arithmetic

```
tod_s = death_t_s − wave-151 start
      = 864.8167 − 682.1000
      = 182.7167 s
```

Stated so the like-for-like comparison is unambiguous: `182.7167 s` is elapsed time **from the
first frame the wave-151 counter is readable**, not from video start (which includes 682 s of
pre-fight), and not from wave-150 (not shown in this capture despite the filename). Time from
wave-160's counter appearing to death is `864.8167 − 838.8667 = 25.9500 s`.

---

## Deep-burst composition (K3)

`pm4k_deep_bursts.csv` is the 35 deepest single-window HP falls across waves 151–160, ranked by
`d_frac`. Rank 1 is the death one-shot itself (`d_frac = −1.0000`, `d_hp = −20005`).

Distribution by wave: **160 → 10 bursts, 159 → 9, 154 → 6, 156 → 4, 153 → 3, 151/152/155 → 1 each,
157/158 → 0.** Waves 159 and 160 hold 19 of the 35 deepest bursts — the fight's damage intensity is
strongly back-loaded, which is consistent with Crucible wave scaling and is worth carrying forward.

Per-row caveats, restated because they will otherwise be lost downstream:
- `plates_*` and `ring_*` are **LOWER BOUNDS**. Corpses carry no nameplate; occluded and off-screen
  monsters are not counted. Do not read `plates_med` as "monsters present".
- The six colour columns are **fractions of screen pixels in a saturated colour class**. They are
  not damage types, not element attributions, and not intensity-normalised.
- `boss_banner` is a binary presence flag on the top-centre banner region, `0` for every row
  including the death burst — no named boss banner was up at the killing blow.

Evidence stills for all 35 windows exist at `/tmp/pm4k/ev/burstNN_TTT.TTT.jpg` (not committed —
they are 1920×1080 and belong in the capture store, not the repo).

---

## Resumed vs re-derived — and the prior-launch crash

A prior launch of this cell **completed the decode** and then died, after 90 tool uses, on an
infrastructure failure: *"image exceeds the dimension limit for many-image requests (2000px)"* —
full-resolution 1920-px frames read into context. It died **before writing any output file and
before committing**. Root cause is instrument discipline, not analysis: high-resolution visual
verification was used where numeric verification was sufficient.

**This session read zero images.** Every quantity above came from arrays and from one new numeric
extraction. That is the correct standing posture for this class of work and should be treated as the
lane rule: *decode to arrays, verify in arrays; downscale below 1500 px and cap at 3 images if a
frame must be seen at all.*

**Resumed unchanged from the prior launch's on-disk state:**
- `hp60_final.npy` — the 12,600-sample 60 fps HP trace (I-1 output)
- `k3.json` — the 35-entry deep-burst composition (I-3 + I-4 output)
- `segfeat.npz` — the 2,068-sample 2 fps full-video brightness / diff / orb-ink features
- `glab.npy` / `gbmp.pkl` — the labelled glyph templates underpinning I-1

**Re-derived from scratch in this session:**
- **The 60 fps wave-span table.** The prior launch printed it but did not persist the 60 fps
  intermediate; only the 2 fps cluster labels survived (0.5 s resolution). Rather than adopt the
  charter's numbers, the ROI was re-extracted at 60 fps (`ffmpeg`, 197 s, 11,820 frames) and
  re-matched. **All ten spans reproduce the charter to the frame**, which independently validates
  the prior launch's refinement and confirms there is no `-ss` seek offset between the two passes.
- **The excursion analysis**, from `hp60_final.npy` under an explicitly stated threshold.
- **The post-death sequence and NaN accounting.**

### Discrepancies against the charter (GL-12: measurement wins)

| Charter stated | Measured here | Δ | Assessment |
|---|---|---|---|
| collapse start `855.75` | **`855.7000`** | 0.05 s | charter rounded; threshold now stated explicitly |
| collapse floor `0.2922` at `t = 860.0` | **`0.291877` at `t = 859.9500`** | 3 frames | `0.2922` is the value at `860.0000` exactly (`5845/20005`); the true minimum is 3 frames earlier |
| "full recovery by `863.5`" | **`863.1167`** | 0.38 s | recovery to `1.0000` is earlier than stated |
| collapse end implied `~863.5` ⇒ dwell `1.3 s` | **dwell `1.6166 s`** | +0.32 s | the full-health window before the one-shot is *longer* than charted — the finding is stronger, not weaker |
| wave-160 end `868.367` | **`868.3167`** | 3 frames | `868.3167` is the last readable `160`; the numeral is gone by `868.3333` |
| terminal sequence `864.7333 → 864.7500 → 864.7833 → 864.8167` | same, **plus `864.7667 = 2222` and `864.8000 = 703`** | — | the charter's abbreviation omitted two intermediate frames; both pass all gates. The `2118 → 2222` uptick is real |
| `instant_kill_span ≈ 0.083` | **`0.0834`** | — | confirms |
| `tod_s = 182.717` | **`182.7167`** | — | confirms |
| death `864.8167`, wave 160, w160 start `838.867` | **identical** | — | confirms |

No discrepancy alters the headline. Two of them (`863.1167` recovery, `1.6166 s` dwell) **strengthen**
it: the player was at full health for longer before the one-shot than the charter supposed.

---

## Outputs and digests

| File | Rows (excl. header) | sha256 |
|---|---|---|
| `pm4k_full_trace.csv` | 12,600 | `bbe31eed7ed13e2f8223cdf13bb5f747b15b7fbee3da5708068276d058b786ee` |
| `pm4k_segments.csv` | 15 | `a1b03c319db32d81cbcbae6efe5b584f01a8069b4af3514b8a886d1ac0b80785` |
| `pm4k_death_anchor.csv` | 1 | `999347db3e1b5caa69809abf8d56d1c7212d67321ae8c80e87abd2e71d584a6e` |
| `pm4k_deep_bursts.csv` | 35 | `044742102ffa845ea05c8c2bade32e8d8ca29d36983f0f6a99b897e3f591a93f` |

`pm4k_full_trace.csv` NaN convention: 363 of 12,600 rows (2.88 %) carry empty `hp_cur` / `hp_max` /
`hp_frac`. These are **gate rejections**, not zero values. Never coalesce them to 0 — doing so would
manufacture 363 spurious deaths. The `867.6500 → 870.2667` block (158 rows) is the death fade and
respawn, where no orb is rendered at all.

---

## What this lap does NOT establish

- **What killed the player.** No damage source, no monster identity, no ability attribution. The
  instruments here read HP and the wave counter; nothing reads the combat log.
- **Whether 20,005 in 83 ms is one hit or several.** Five frames elapse; the intra-frame structure is
  below this instrument's resolution. `17,887 HP in a single 16.7 ms frame` is the measured floor on
  burst concentration; whether that frame contained one instance or five is not resolved.
- **Whether the death was avoidable.** Out of scope, and not inferable from HP alone.
- **Monster counts.** `plates_*` are lower bounds and should never be quoted as census figures.

Suggested next probe if the source question matters: Grim Dawn writes a combat log; the on-screen
floating combat text at `864.7333–864.8167` is captured in the rank-1 evidence still and is legible
at native resolution. That is a bounded, mapped follow-on — a crawler-shaped job once the text ROI
is characterised, not a researcher-shaped one.
