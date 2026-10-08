# Finding — 2026-10-08 — BV2F P5 dense-texture PRE-RULING (before pilot 3 is gated)

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority)
**Severity:** WARN (ruling **(b) RE-INSTRUMENT**; 0 BLOCK now)
**Target:** R-C9-246 / R-C9-247 / R-C9-248 (conductor, ledger `astra_test_01/burst/runs/C-9/ledger.json`); PT root cause `6430c7bd8` (`fid/pt/r247/`); PH P5 calibration (`fid/ph/calibration.md` §§ 1–4, `harness/p5_seams.py`, `results/p5.json`)
**Developer:** galadriel (lane PH), drax (lane PT); conductor gandalf
**Principles applied:** REVIEW_PROCESS #1 (math before code), #2 (control before claim), #4 (charter + ledger as truth), #5 (severity matters)
**Governs:** charter `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` § 9 C-1, § 12 W-1 (*"re-instrumented or discarded; never threshold-tuned"*), § 12 W-4 (pilot is a proof), the P6′ pre-registration precedent

## Ruling

**(b) P5 is RE-INSTRUMENTED.** Raw overlap MAD stays on the sheet and is no longer binding. **The texture-normalised MAD offered as the example is REJECTED**: it cannot see a tone seam in dense texture, which is the case being relaxed. The replacement is a **band split on the raw canvases** plus a **new context-boundary step** on the stitched painting. P5(b) is unchanged. Every parameter is frozen in this finding, before any pilot-3 number exists.

**Read this before relying on the premise of the question.** One of PS3a's two "dense" joins over the bar has a **real, visible seam**. At 0_1/0_2 there is a straight horizontal tone step at **y = 1792**. The re-instrumented P5 still catches it, and I expect pilot 3 to **FAIL P5 on that join** (§ PASS/FAIL).

## What I found (descriptive)

All numbers here come from my read-only probe on the archived canvases and the dry stitches. They are **not binding**; PH's recomputation binds.

1. **Raw MAD mixes two different quantities.** The service redraws every pasted strip (PT Q2: high-pass correlation 0.51–0.79 in v1). Two renditions of dense texture therefore disagree pixel for pixel even when tone and grain match. That phase incoherence is what makes MAD track texture (PT: r 0.87 on v1). On v1's densest join (2_2|3_2, raw 13.09), a Gaussian σ 6 px removes it: the low-pass difference is 6.50.
2. **Raw MAD moves the wrong way for the observed mechanism.** If v1 3_2's strip high frequencies are scaled ×0.67 (PT mechanism 1, a soft redraw), raw MAD **falls**, 13.09 → 11.64. No form of overlap MAD can see a redraw that is softer than the new paint.
3. **The texture-normalised MAD is blind where it matters.** Adding a uniform +8 sRGB tone offset to v1 3_2's strip scores 0.576 against a v1 bar of 1.406, so it PASSES. The bar is set by smooth joins, where the denominator collapses. PS3b's known-bad joins (1_1|2_1, 2_0/2_1, which were stopped correctly under R-C9-247) score 0.69 and 0.97, also PASS.
4. **The MAD−f(Lv) residual (PT's "MAD~texture fit") is a threshold, not an instrument.** It fits two free parameters to v1 (n = 24) and then sets the bar at v1's maximum residual. That is a texture-dependent threshold on the same mixed scalar. In substance it is threshold-tuning. PS3a's margin is 3.27 against a bar of 3.425. **Rejected as binding.** PH may report it.
5. **P5(b) is aimed at the wrong line for this pipeline.** `seam_vis` measures at the band **centre**, x = 1280c + 128. Both PT mechanisms make their line at the **context boundary**, x = 1280c + 256 (likewise y = 768r + 256), where v1's ramp ends on the redraw. That line is 128 px from P5(b)'s line: outside its ±2 px window, and inside the 128–160 px gap before its baseline. This holds for v1 as well. P5(b) is a valid ghosting detector, but nothing binding measures the boundary.
6. **PS3a has a visible seam at y = 1792.** Probe on `fid/pt/ps3_dry/painting.png` (the PS3a dry stitch), mean luma over x 1250–1400: 233.4 at y 1790, then 210.8 at y 1792. At 3× it is a straight horizontal edge across the shore-ice bay (x ≈ 1240–1400). It is fainter across the snow at x ≈ 450–800 (+10 to +12 luma at y 1792, against neighbouring rows of −7 to 0). PT's own crop `fid/pt/ps3_dry/join_0_1-0_2_y1792_MAD13.81.jpg` shows the line at its row ≈ 258. **The premise "no visible seam at 1:1" holds for 1_1/1_2. It does not hold for 0_1/0_2.**
7. **The conductor's tone and texture controls have holes exactly there.** `join_steps.py` and `hf_steps.py` mask to ice/snow guide classes with ≥ 60 % coverage. The bay is painted ice over a guide class that is not ice. Result: **0 segments** on 1_2|y1792 and none at x ≥ 1088 on 0_2|y1792. The per-join median reading (0_2|y1792: 3.19 against control 3.35) hides a 15.44 dE segment at x 960–1024. These are PT diagnostics. They are not calibrated rows, and they are not a safety net for P5.
8. **Label drift.** `join_mad_survey.py`'s `src()` and PH's `canvases()` both prefer `-r1` directories. PT's "PS3" survey (r 0.71; 16.74 / 16.23 / 14.79 / 13.93) is therefore **PS3b-precedence**, not PS3a. PS3a's raw MAD is 14.38 at 1_1/1_2, 13.81 at 0_1/0_2 and ≤ 11.60 elsewhere. A P5 run on the build through `canvases("BV2F-PS3")` would measure the wrong canvases.
9. **INFO: v1 itself has a visible seam** at y = 2560 (x ≈ 380–1140). Heather is cut and there is a snow-brightness step. Any v1-max bar on a boundary measure therefore allows a seam that bad. That is what v1 parity means. The R-C9-248(4) eye stop is stricter than P5, and that is legitimate.

Probe summary (binding values come from PH):

| Set | raw MAD max (over 13.09) | a1 low-pass seg max (over v1 bar ≈ 9.57) | a2 grain seg (over ≈ 0.504, whole-join probe) | normalised MAD (over 1.406) |
|---|---|---|---|---|
| v1 T10BF | 13.09 (0) | 9.57 (0) | 0.504 (0) | 1.406 (0) |
| R-C9-158 BVSW | 15.29 (6) | 11.85 (**3**) | 0.722 (**1**) | 1.587 (1) |
| PS2 | 13.86 (1) | 6.56 (0) | 0.241 (0) | 0.475 (0) |
| **PS3a** (build base) | 14.38 (2) | **11.11 (1: 0_1/0_2, x 1408–1536)**; 1_1/1_2 = 5.30 | 0.354 (0) | 0.594 (0) |
| PS3b | 16.74 (4) | 18.08 (**4**) | 0.354 (0) | 0.974 (**0**: misses known-bad joins) |

R-C9-158's worst raw join (0_2|1_2, 15.29, Lv 2625) is itself dense texture: its low-pass value is 6.00. Part of raw MAD's calibrated "separation" of the negative control was texture density. That supports the re-instrumentation; it does not undermine it.

## The instrument: P5 v2 (parameters frozen here)

Grid law unchanged: 1536 × 1024 canvases, stride 1280 × 768, 256-px overlap. Bars are always **v1's own maximum** on the same measure (T10BF canvases and `barrow_full_painted.png`, flag-off).

- **P5(a1) overlap TONE disagreement, on RAW canvases (binding).** For each neighbouring pair, take each canvas's rendition of the shared 256-px strip. Apply a Gaussian, σ = 6 px, per sRGB channel (0–255). Take the mean over channels of |G(a) − G(b)|, trimmed 12 px on every strip edge. Split along the overlap's length into **128-px segments** (8 vertical, 12 horizontal). The score is the per-segment mean; the row value is the maximum segment.
- **P5(a2) overlap GRAIN disagreement, on RAW canvases (binding unless discarded, see C3).** H = luma − G_σ3(luma). For the same segments, score |log2((std H_b + 0.5) / (std H_a + 0.5))|.
- **P5(b) stitched seam visibility at band centre:** unchanged, ≤ 0.799.
- **P5(c) context-boundary STEP, on the STITCHED painting (new, binding).** Measure at x = 1280c + 256 (c ≥ 1, over that chunk's row span) and y = 768r + 256 (r ≥ 1, over its column span), per **64-px segment**, on Lab (D65) after a Gaussian, σ = 4 px. **All classes, with no class mask and no median-over-join.**
  - Tone: T(p) = ‖mean Lab[p−10, p−4) − mean Lab[p+4, p+10)‖.
  - Grain: G(p) = |log2((std H[p, p+24) + 0.05) / (std H[p−24, p) + 0.05))|, with H = L* − G_σ3(L*).
  - Excess = T(0) − median of T(±o) for o ∈ {32, 40, …, 96}. The same applies to G. A seam is straight; a content edge does not peak exactly on the boundary.
  - A segment counts only inside a run of **≥ 2 consecutive segments** on the same boundary. The run score is the minimum of the two.
  - Exclude any segment whose ±110 px window touches unpainted pixels.
- **Raw overlap MAD (the old (a)): reported, NOT binding.** Any join over 13.09 gets a 1:1 crop in the Gate-2 packet.

## What PH must compute

Pre-register P5 v2 in `calibration.md` and **commit the section and the harness before reading any pilot-3 P5 value**. This follows the P6′ precedent: stricter-than-pre-data.

- **C1 · v1 positive control.** v1 PASS on a1, a2, b and c, by construction. Also: v1 restitched with **DEV-23 + DEV-25 ON** must PASS (b) and (c), and flag-off must reproduce v1 byte-identical.
- **C2 · R-C9-158 negative control** (BVSW-* plus `section_sw_painted.png`). P5 v2 must FAIL as a row. Report each sub-measure's separation.
- **C3 · Constructed REDs, one per sub-measure:**
  - a1: (i) the existing 6 % hue/tone second hand on 1_1; (ii) **new, dense**: +6 sRGB uniform on v1 3_2's strip of 2_2|3_2 (probe: 11.05 against ≈ 9.57). Report the rejected normalised MAD beside it, for the record.
  - a2: **new**: v1 3_2's strip HF (σ 3) scaled ×0.67 (the PS2 2_0 mechanism-1 ratio). **If it reads GREEN, a2 is DISCARDED, not tuned**, and mechanism 1 then rests on (c).
  - c: **new**, on v1's stitched painting: (i) a +7.16 dE step (the PS3 2_2 rectangle) on the new-paint side over 256 px of one boundary; (ii) HF ×2.5 on the new-paint side over 256 px (the PS3b mound). Report RED or GREEN. Where GREEN, report the smallest magnitude that reads RED, as a disclosed detection floor. If neither reads RED at any magnitude ≤ 2× the stated value, (c) is DISCARDED.
  - **Masking control:** the PS3b canvases (the `-r1` set), stitched with DEV-23 + DEV-25 ON, must still FAIL P5.
- **C4 · Specificity**, which is the question asked. Report a1 and a2 for PS2 0_1/0_2 (raw 13.86) and PS3a 1_1/1_2 (raw 14.38). Expected PASS (probe 4.00 / 5.30). A FAIL is reported, not tuned.
- **C5 · Canvas pin.** Use an explicit manifest, with sha256, of the build's canvases: `BV2F-PS3A-*` with 2_2 replaced by the R-C9-248 repaint. **Do not use `canvases()`' highest-`rN` rule** for this prefix family (§ 8).

## PASS / FAIL for pilot 3

**PASS iff** on the pinned build set (flag-ON stitch for b and c), all of the following hold:

- every a1 segment ≤ v1 bar;
- every a2 segment ≤ v1 bar (if a2 survives C3);
- every P5(b) seam ≤ 0.799;
- every P5(c) run ≤ the v1 tone and grain bars.

**FAIL** if any of them is exceeded. Raw MAD above 13.09 alone never fails.

**Expected: FAIL on a1 at 0_1/0_2, x 1280–1536** (probe 11.11; 1280–1408 at 9.33). It sits on the real bay seam of § 6, and the join is unchanged by the 2_2 repaint. 1_1/1_2 and the other dense joins should clear. The repainted 2_2's joins (1_2|2_2, 2_1/2_2, x2816) are unmeasured and must be measured fresh.

**Disposition if it fails.** The cause is already diagnosed: the R-C9-248(6) bay, a content change across a paste boundary (R-C9-247's owned error).

- No repaint loop and no bar move.
- Gate-2 records **P5 FAIL, cause diagnosed, remedy assigned**. Under W-4 (the pilot is a proof, not a keeper) that does **not** BLOCK the build artifact.
- It **will BLOCK Phase 3′ firing if the both-sides blockout fix has not landed in the blockout by then.**

## DEV-23 / DEV-25 masking

- **M-1 (WARN).** DEV-23 (tone match) and DEV-25 (grain-amplitude match) correct exactly the statistics P5(c) measures. Report (c) **flag-OFF and flag-ON**. The binding read is flag-ON. Any segment that FAILS off and PASSES on reads **"PASS (stitch-corrected)"**, with a 1:1 crop in the packet. **a1 and a2 are measured on raw canvases, which DEV-23/25 never touch. That is why (a) stays raw and must not move to the stitched painting.**
- **M-2 (INFO).** DEV-25 matches HF *amplitude*, not grain *scale*. 0_2's redraw at the bay corner has visibly larger pebbles than 0_1's rendition. A coarse-against-fine seam can pass (c) after DEV-25; P11 and the conductor's 1:1 look are the remaining guard.
- **M-3 (WARN).** DEV-23 can feather a straight content edge (a pool or bay rectangle) into a soft but still straight band. C3's masking control (PS3b, flags ON, must FAIL) is the proof that it does not hide one from P5.
- **M-4 (WARN).** Do not cite `join_steps.py` or `hf_steps.py` medians as P5 evidence, or as the "tone/texture control" in R-C9-248(4)'s stop, without a coverage report. Their class mask and median reading missed § 6.

## Action

- [ ] PH (galadriel): implement P5 v2 exactly as specified. Run C1–C5, pre-register and commit, then measure pilot 3.
- [ ] PT (drax): no action for P5. For the build stop, inspect x 1180–1460 × y 1740–1840 of the pilot-3 stitch at 3× before reporting "no visible seam".
- [ ] Conductor (gandalf): record this pre-ruling as a ledger row. Rule on adopting P5 v2 on PH's calibration evidence, as for P6′. Decide the pilot-3 0_1/0_2 disposition: blockout fix before Phase 3′.
- [ ] Matt: none. This is a within-harness re-instrumentation under charter W-1; no cross-seam schema change and no row reclassification.

## References

- `astra_test_01/burst/runs/C-9/ledger.json` (R-C9-158, -246, -247, -248)
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/calibration.md` §§ 1–4; `calibration.json`; `harness/p5_seams.py`; `results/p5.json`
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/pt/r247/findings.json`, `join_mad_*.json`, `strip_trace_summary.json`
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/pt/tools/join_mad_survey.py`, `join_steps.py`, `hf_steps.py`
- `astra_test_01/burst/runs/C-9/barrow_v2/fid/pt/ps3_dry/painting.png`, `js/join_steps.json`, `join_0_1-0_2_y1792_MAD13.81.jpg`
- `astra_test_01/burst/runs/C-9/barrow_full/paint/barrow_full_painted.png` (v1; seam at y 2560)
- `astra_test_01/burst/runs/C-9/artifacts/BV2F-PS3A-*` (byte-identical to `BV2F-PS3-*` base, md5 checked on 0_0 and 2_2)
