# Oracle-derived testing suite — SPEC MEMO (T1 pre-contract)

> **STATUS:** DRAFT v0.1 (2026-09-12) — gandalf (SPEC-AUTHOR). Folds into `astra_test_01/burst/SPEC.md` § 6 T1 next HITL session, after legolas R10c's clip table lands and a first measurement pass fixes the bands. **Matt's boundary (2026-09-12), binding:** extracted reference frames (Hades et al., class E; Muybridge, public domain) are a MEASUREMENT SUBSTRATE — **frames in, numbers out, never pixels forward.** No reference frame is ever a burst input: not a generation reference, not a judge anchor (a judge seeing Hades is Hades as an input). Judge calibration uses Muybridge (PD) or our own frames only.
> **Principle:** the SAME instrument measures the reference and the candidate. A gate is "oracle-calibrated" when its band was fixed on reference curves BEFORE our loop was measured (pre-registration, as the lane already runs it).

## 0. The chain

`reference clip → frames (outside the repo, class-E sidecar) → masks → landmarks → phase-normalised curves → bands.json (numbers, in the repo) → gates + judge questions + prompt guidance + pose guides (first-party) → our candidate measured by the same code → comparison view for Matt`

## 1. Segment — `oracle/segment_reference.py`
- Static-camera clips: **median background** over the clip → |frame − background| threshold (Lab distance) → morphological open/close → largest component → mask. Shadow rejection by a low-lightness/low-chroma test under the figure.
- Camera-motion guard: phase-correlation shift between consecutive frames > 1 px ⇒ frame VOID (`passed: null`). Mask-health metric = fraction of the figure bbox that is unclassified border (as O6).
- Muybridge: rectify against the printed grid (Legolas § 5.1.3), then threshold on the lit-skin band; head-top from the crown is unreliable (dark hair on dark backdrop) → use the **ear/eye row + a fixed crown offset** measured once, and say so.
- Output per frame: mask PNG (outside the repo), `mask_health`, `camera_shift_px`.

## 2. Landmarks — `oracle/landmarks.py` (mask → numbers; identical for reference and candidate)
| quantity | how (mask-only) |
|---|---|
| `H` | head-top row − sole line (topmost / bottommost mask rows, alpha ≥ 128 equivalent) |
| `head_top_y`, `head_cx` | topmost row; centroid x of the top 12 %H of the mask |
| `sole_line_y` | bottommost mask row |
| `foot_L_x / foot_R_x`, `planted[]` | the two lowest connected components below the knee line (0.25 H above the sole); left/right by x-order with temporal continuity; planted = sole within 2 px of the ground line **and** x-velocity ≈ the expected scroll (in-place) |
| `shoulder_y`, `chest_w` | topmost row of the torso column (mask width ≥ 0.6 × max width); mask width at 0.72 H |
| `wrist_ext_L/R` | mask horizontal extent at 0.45 H beyond the torso column, per side |
| `root_cx` | figure centroid x |
All in px and ÷ H. Null when the mask health fails.

## 3. Curves — `oracle/cycle_curves.py`
- Cycle detection: autocorrelation of `sole_line_y`/`head_top_y` → period; phase φ ∈ [0,1) per frame; resample every series to 24 phases (Muybridge 12, Hades native, ours 8 all map).
- Derived: bob amplitude %H + phase of min/max; lateral head sway %H + sign-changes per cycle (W-3c); arm swing amplitude per side; planted-sole scroll %H/frame and slip; the contact/down/passing/up table; idle: breath amplitude %H, period s, maxima per loop; **lock** statistics (sole, head, root, grip drift).

## 4. Bands — `oracle/oracle_bands.py` → `oracle/bands.json`
- For each gate ID in legolas § 5.4 (W-1…W-12, I-1…I-8, G6c): `floor` = Muybridge value, `target` = painted-ARPG value(s), `ceiling` = target × k (k stated per gate), with the reference provenance (clip id, class, fps) recorded beside the number.
- **Pre-registration rule:** `bands.json` is committed and hashed into the bible (`gait_bands_sha256`) BEFORE the first candidate loop is measured against it. Re-banding = a new TOOLING burst + a ledger ruling.

## 5. Gates — `gates/gait_oracle.py` (T1b) + `G6c` in `gates/g6_seam.py`
- Applies `bands.json` to our registered frames through `landmarks.py` + `cycle_curves.py`; every result an envelope (value, band, evidence strip); sub-pixel quantities (toe clearance, veridical bob) REPORT-ONLY by design (Legolas § 0.4).
- G6c: seam vs half-cycle homologue ≤ 1.25×; walks only; idles fall back to G6b.

## 6. Guidance — `gates/pose_guide.py` + prompt phase text (first-party by construction)
- `pose_guide.py` renders numbered-foot silhouette guides per phase from the *table* (our H, our canvas): two sole outlines at the measured x/y per phase, a ground line, phase labels — line art we draw, no reference pixels.
- Prompt phase text generated from the same table ("frame 3 — PASSING: left leg swings past the planted right; body at its highest; arms at the crossing") → BURST_RULES data, not hand-kept prose.
- Idle spec generated from the idle bands: breath amplitude/period; the LOCK list (feet, head, gaze, grip, root) as explicit assertions — ~5 lock to 2 motion (Legolas § 0.5).

## 7. Judge — question generator + motion-transcriber calibration (X0-M)
- DSG-shaped questions from the phase table (planted foot per frame; lead alternation; frame-7→0 continuity; idle: does the head move? do the feet?). Calibrated on **Muybridge** (PD) frames with known answers, exactly as X0-T calibrated the part transcriber — pass bar pre-registered. Hades frames never reach a burst.

## 8. Matt's comparison view — `review/oracle_compare.py`
- Oracle vs candidate: curves overlaid per quantity (head y, sole x per foot, arm extent, chest width) on the phase axis, with the two frame strips aligned by phase beneath; bands drawn as shaded floors/ceilings. Static HTML + PNG; MP4s side by side at their native fps.

## 9. Where things live
- Reference frames + masks: `~/Desktop/Astra Burst Review - …/06 Oracle - painted ARPG clips (class E)/` (never the repo; `SOURCE_and_CLASS.txt` sidecar per clip). Muybridge plates: legolas `refs/` (PD).
- Numbers: `astra_test_01/burst/oracle/bands.json` + per-reference landmark CSVs — in the repo, hashed into the bible.
- `lane/ref_provenance.py` keeps refusing class-E paths as burst references — that is the enforcement, not a convention.

## 10. Sequence
R10c clips → extract (conductor, `clip_to_oracle.sh`) → **T1a** (segment, landmarks, curves, bands; serial TOOLING) → first measurement pass on Muybridge + Hades → `bands.json` committed → **T1b** gates + pose guides + G6c → **T1c** question generator + X0-M calibration on Muybridge → re-run idle-S / walk-E with generated guidance → compare → Matt rules L5 and the loops.

Open for Matt: (a) the a/b/c sourcing class; (b) whether PD (Muybridge) frames may be judge anchors (Q73 e); (c) k per gate ceiling — proposed 1.5× target unless Legolas' § 5.4 states otherwise.

Tracker-delta: game tracker (oracle-first sequence already logged); charter § 11 row 26 criterion unchanged.
— gandalf, 2026-09-12
