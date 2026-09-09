# ASTRA TEST 01 — execution report

**Run disposition: STOPPED AT FAILED TURNAROUND CHECKPOINT.** The complete eight-view attempt failed; a targeted SW repair also failed. Generation stopped under §§2 and 6 of the brief. Eight checkpoint frames and one rejected repair exist. No animation or VFX sequence is represented as complete.

## 1. Toolchain declaration

Declared before the first generation call:

- Built-in `image_gen.imagegen` (`tools.image_gen__imagegen`) accepts prompts and local reference images. The interface exposes neither its backend model identifier nor hard resolution limits, seed locking, a mask argument, or an explicit alpha-output setting. The run therefore does not claim a selectable model or guaranteed output size. All nine returned sources were **1254×1254**. S was RGBA; all eight subsequent reference-conditioned results were RGB.
- System Python 3: **Pillow 10.3.0, numpy 2.4.6**, verified by import. The adjacent project virtual environment lacks Pillow; no installation was needed.
- Brief: [ASTRA TEST 01 painted character vfx.md](../codex-3d-modeling/ASTRA%20TEST%2001%20painted%20character%20vfx.md). The adjacent README, references, Blender scripts, and Godot scene describe a different purple-and-gold 3D wizard. They supply no matching painted battle-mage or animation frames and were not reused.
- Output is repo-root `./astra_test_01/`, following the brief. Serial open Codex lane; authenticated using ChatGPT; no subagents, API-key fallback, or model switch.
- Original generated PNGs are kept locally; source images and packed PNGs remain git-ignored under this repository's binary policy. Versioned scripts, prompts, annotations and reports alone cannot reproduce the stochastic art without the preserved PNGs.

## 2. Consistency method used

S idle frame 00 was generated first and then supplied directly as the reference for seven individual direction calls. Every direction was generated uniquely. No mirroring, programmatic character shapes, duplicated animation frames, synthetic motion, relighting, or background-keying was used. Exact prompts are in [prompts/](prompts/). Original bytes are in [source/](source/); SHA-256 hashes are recorded in both check result files.

The repair used the original SW output as its edit target, explicitly requesting genuine alpha, preserved identity/pose/light, smaller framing and fixed feet placement. It returned RGB again, altered the pose, and introduced brighter, smoother gold-brown edge accents. The first SW is retained in the main package; the repaired SW is evidence only.

Packing uniformly downsamples the entire 1254×1254 source to 512×512 using Lanczos. It never upscales, crops, repositions, normalizes individual silhouette heights, or removes the baked background. Converting RGB to RGBA for packing leaves every pixel opaque; that conversion is not counted as recovered transparency.

## 3. Turnaround checkpoint results (gates 1–4, 7)

**Attempt 1: FAIL**, recorded before the repair and before any other animation frames. **Repair checkpoint: FAIL**, checked with the SW replacement and the original seven remaining views. This is one full turnaround plus one targeted repair, not two independently regenerated eight-view sets. The failed repair was sufficient to stop; the other six opaque directions were not regenerated.

Evidence:

- [First eight-view turnaround](character/turnaround.png), [64 px canvas-height read](character/turnaround_64px.png).
- [First numeric results](evidence/turnaround_1/checks.json), [first measurement overlay](evidence/turnaround_1/measurement_overlay.png).
- [Repair numeric results](evidence/turnaround_2/checks.json), [repair comparison sheet](evidence/turnaround_2/turnaround.png), [repair overlay](evidence/turnaround_2/measurement_overlay.png).

| Gate | Result | Evidence / interpretation |
|---|---|---|
| 1. Height parity ±3% | FAIL to certify | Only S has usable alpha: bbox `[146,108,332,446]`, height **338 px**, reference deviation 0%. Seven silhouettes are unavailable because their backgrounds are opaque. Their heights and deviations are reported as null, not fictitious 512 px silhouettes. Visual scale varies substantially. |
| 2. Pivot within ±4 px | FAIL | All eight first-attempt foot midpoints fail. Worst-axis errors **21.36–60.76 px**; table below. |
| 3. Fixed upper-left light centroid | FAIL to certify | S alone passes: brightest-5% centroid **(214.64,187.93)** versus silhouette center **(238.5,276.5)**, using 1,558 pixels. Seven opaque backgrounds prevent valid character-only sampling. Visual highlights are generally upper-left, but that does not certify the numeric gate. |
| 4. Staff in right hand | PASS, visual | S/front views: staff in viewer-left arm; N/back views: viewer-right arm; W far arm and E near arm. Opposite hip carries satchel. Individual images and the turnaround were inspected. No mirrored asset was generated or packed. |
| 7. Hood + staff downscale read | PASS, visual | Pointed hood and separate tall staff remain identifiable in the actual 512×64 strip, even with character heights below 64 px. Background transparency still fails independently. |

Contact annotations mark two visible sole endpoints in the 1254×1254 source; their midpoint defines the measured stance contact. These are approximate manual observations, ±6 source pixels (±2.45 output pixels), not automatic landmark ground truth. The failure margins comfortably exceed that uncertainty. The overlay shows sole points/links in turquoise, required pivot in pink, and valid silhouette/light measurements in amber. No feet pass is claimed from canvas metadata.

| Direction | Measured midpoint, px | Worst-axis error, px | Fully transparent output pixels |
|---|---:|---:|---:|
| S | (259.88,421.36) | 21.36 | 227,041 / 262,144 (86.6093%) |
| SW | (258.65,453.21) | 53.21 | 0 |
| W | (249.06,460.76) | 60.76 | 0 |
| NW | (248.24,434.42) | 34.42 | 0 |
| N | (254.37,442.39) | 42.39 | 0 |
| NE | (250.08,425.03) | 25.03 | 0 |
| E | (277.23,445.04) | 45.04 | 0 |
| SE | (280.50,445.45) | 45.45 | 0 |
| SW repair | (264.57,442.59) | 42.59 | 0 |

Measurement rules were set before generation: alpha ≥128 defines the silhouette; height includes the staff; Rec.709 RGB luminance selects exactly ceil(5%) of silhouette pixels with stable tie ordering; centroid must be left of and above bounding-box center. No right-side lighting pass is inferred for frames that cannot be segmented using their actual alpha.

The S hood-to-boots body is also visibly larger than the approximately 240 px register; 338 px above is the entire staff-inclusive silhouette, not a mislabeled body-height measurement. Camera foreshortening and projected stance vary across views. These are additional register concerns, not silently corrected art.

## 4. Animation results (gates 5–6)

| Animation | Required | Delivered | Drift / loop seam |
|---|---:|---:|---|
| idle | 64 frames | 8 initial checkpoint poses only | NOT TESTED; no temporal pairs exist |
| walk | 64 frames | 0 | NOT TESTED |
| cast | 96 frames | 0 | NOT TESTED; no cast-pass prerequisite for sprint |
| sprint, optional | 64 frames | 0 | Not attempted |

The idle sheet is **512×4096**, one column and eight direction rows. Its atlas explicitly states one available frame per direction versus eight required, `production_ready: false`, and `REJECTED_CHECKPOINT`. It is an evidence atlas, not a complete loop. No frame repetition was used to inflate counts.

## 5. VFX results (gates 8–10)

- **8. Style match: NOT TESTED.** No character cast frame or VFX cast frame exists. No side-by-side comparison is invented.
- **9. Alpha cleanliness: NOT TESTED for VFX.** There are zero VFX frames and no VFX edge samples; no mean edge value can be reported. The opaque character checkerboard defect is not substituted for a VFX measurement.
- **10. Combined cast → travel → impact: NOT TESTED.** No sequences were generated. The local viewer labels this and disables combined playback. Metadata preserves the intended zero-based character spawn index **5** (the sixth frame), but metadata is not timing evidence.

[VFX atlas](vfx/atlas.json) has an empty `modules` object and records all 24 required frames as absent. Character failure supplies no evidence about the quality of a separately generated frost spell.

## 6. Scope reductions

The mandatory failed-turnaround stop overrides downstream generation. Required production deliverables therefore remain incomplete: **216 of 224 character frames absent**, 24 of 24 VFX frames absent, all emissive masks absent, temporal playback absent. Eight delivered checkpoint frames are themselves rejected. Optional sprint and Godot resources were not attempted.

[preview/index.html](preview/index.html) is a dependency-free local **evidence viewer**, with direction, attempt and background selectors, the packed turnaround, and measurement links. Its FPS and animation/combined controls are disabled honestly. It does not satisfy the requested animation player or composite gate. Open it directly with its adjacent folders intact; it makes no external requests.

Browser verification was attempted through the installed browser skill; setup reported “No browser is available” and discovery returned an empty list. Interactive behavior could therefore not be browser-verified. JavaScript syntax and packaged file/atlas integrity are checked separately; generated contact sheets were visually inspected with the image viewer.

## 7. CHARACTER verdict: FAIL

The tool produced a recognizable, detailed original battle-mage and preserved the right-hand staff arrangement across eight separately generated views. It did not meet the test's production contract: seven views and the attempted repair have baked checkerboards, the stance pivot is outside tolerance in every view, scale varies, and alpha-dependent height/light consistency cannot be certified. No animations were generated on top of this failed prerequisite. This is a measured failure of this run and tool workflow, not a claim that all painted-image workflows must fail.

## 8. VFX verdict: PARTIAL — NOT TESTED

No VFX generation was reached. PARTIAL records incomplete execution within the brief's allowed PASS/PARTIAL/FAIL vocabulary; it does not assert partial visual quality or a VFX failure. There is no evidence for style match, edge cleanliness, emissive masks, or S/E composite timing. The VFX question remains unanswered independently of the character verdict because the brief also requires stopping at the failed turnaround.

## 9. Time and generation-call count

All dates below are UTC; local session date is September 8, 2026 (EDT).

| Section | Calls | Timing |
|---|---:|---|
| S master | 1 | 2026-09-08 23:51:17 start; reported tool wait 38.4 s |
| Remaining seven directions | 7 | Complete by 2026-09-09 00:00:02; cumulative reported waits 309.3 s |
| SW repair | 1 | Complete and measured by 2026-09-09 00:03:46; reported tool wait 40.0 s |
| Character animations | 0 | Not started |
| VFX | 0 | Not started |
| Packing, checker, report, preview | 0 | Local processing; see verification record for completion timestamp |

**Total: 9 generation calls, all returned images; 8 outputs failed transparency.** Reported waits total 387.7 s (about 6.46 minutes), including small orchestration overhead in some calls. Elapsed generation/checkpoint window was approximately 12.5 minutes, including prompt authoring, copying, inspection, and checker development. Session-start reading preceded that window. There was no API fault or named-Claude fallback; this was an output-quality failure.

## 10. Second-run process changes

1. Validate **one reference-conditioned transparent edit** before commissioning a full turnaround. The first new image had genuine alpha; that did not predict the edit path's behavior. A painted checkerboard must fail immediately on actual mode/alpha inspection.
2. Use verified alpha output plus explicitly recorded source foot anchors, then apply a documented uniform scale/translation registration stage. Check geometry before/after that stage; do not confuse an atlas pivot declaration with actual contact. This would address spatial placement but would not recover missing transparency or prove identity consistency.
3. Lock a common master size before directional generation, and establish a consistent camera/stance reference. The master in this run already missed the requested standing height; the direction calls then drifted in framing.
4. Clarify the test's gate precedence before a future run: allow standalone VFX work after a character stop if independent VFX evidence is required regardless of character outcome. Under this run's literal stop rule, it remains untested.
5. Clarify the one-based frame wording and the 8 VFX cast frames at 20 fps (0.40 s) versus character frames 3–8 at 16 fps (0.375 s). Also distinguish material brightness from key-light direction, and define how frost emission is excluded from the character light-lock measurement. These are proposed next-run methodology clarifications; this run's register and gates were not changed.

### Reproduce the evidence checks

From the repository root:

```sh
python3 astra_test_01/check.py --attempt 1
python3 astra_test_01/check.py --attempt 2
python3 astra_test_01/package.py
```

Both checker commands intentionally return exit code **1** for the measured asset failure; this is not a Python crash. Each writes detailed JSON and comparison images before returning. Visual gate judgments are stored in `visual_judgments.json`; they are human-style observations recorded by the assistant, not automated hand detection. Source byte hashes make the measured inputs auditable. See [verification.json](verification.json) for final packaging checks.
