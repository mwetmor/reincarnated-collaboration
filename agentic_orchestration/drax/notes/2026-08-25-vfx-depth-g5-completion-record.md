# VFX-DEPTH G-5 — COMPLETION RECORD

**Cell:** instrument gap **G-5**, queued to drax at charter **R-17(e)**, lane-clearing for the BUILD wave per **R-21(c)**.
**Author:** drax (presentation seam) · **Date:** 2026-08-25 (rendered 2026-08-26T04:24Z UTC)
**Start commit (godot):** `fc26b80793cce58660aba37ae957e366d15c0216`
**Authority:** VFX-DEPTH autonomous run, gandalf RUN-CONDUCTOR. Push-as-you-go, Matt-authorized.

---

## 1. What G-5 required

galadriel's definition, § instrument gaps, row **G-5** — the diagnosis and the remedy, verbatim:

> **Cannot report:** F7 on any moving-camera clip.
> **Why:** "My pan-null is a **rigid** pan. A camera following a character through a 3-D scene manufactures high-frequency translation from parallax that the null does not model, so authored shake and tracking noise are not separable by amplitude alone. The impact-enrichment term narrows this but does not close it."
> **Remedy:** "**A 3-D tracking-camera null** — a synthetic scene with depth, panned by a follow-cam, no shake authored. Buildable in the godot harness in an hour **by drax**, and it would convert every reference F7 `?` into a real call. ⚑ *This is the one gap that needs another seam.*"

**What the existing null actually is, read rather than assumed.** `frame_forensics_depth.py::synth_controls()` builds `synth_pan.mp4` as `np.roll(base, int(round(6.0 * i)), 1)` — a flat image slid sideways. One image-space translation, exactly representable by the global affine fit, residual zero **by construction**. It is a correct null for *"does a pan read as shake"* and the wrong null for *"does a FOLLOW-CAM read as shake"*, because a follow-cam through geometry **has no single true translation to fit**. G-5 asks for that second null. That is what was built.

**Scope call — where the seam boundary falls.** G-5's remedy sentence is entirely a *render* deliverable; there is no CV-pipeline change inside its wording. I therefore did the whole of G-5 and touched none of `galadriel/pipeline/`. What is NOT in G-5 but is adjacent is named in § 7.

---

## 2. What was built

Three new files in `~/Games/reincarnated-godot`, all new, none pre-existing:

| Path | Role |
|---|---|
| `/Users/admin/Games/reincarnated-godot/scripts/g5_camnull.gd` | scene builder, follow-cam, shake authoring, ground-truth emitter |
| `/Users/admin/Games/reincarnated-godot/scenes/g5_camnull.tscn` | 6-line scene binding the script |
| `/Users/admin/Games/reincarnated-godot/scripts/run_g5_camnull.sh` | ladder runner: render → dim gate → prune → count gate → encode → R-18c prune → ffprobe promotion |

### 2.1 The ladder, and why it is a ladder and not a clip

**A single null clip yields a single number, and a single number is not a floor** — it is one sample of a floor that varies with its driver. The residual scales with (a) depth relief in frame and (b) how the camera is coupled to the subject. The ladder sweeps exactly those two, holding path, clock, lens and seed fixed:

| leg | relief | follow-cam | authored shake |
|---|---|---|---|
| `N0-flat` | ground only, zero relief | lockstep | **none** |
| `N1-low` | 0.3 – 1.5 m | lockstep | **none** |
| `N2-mid` | 0.5 – 4.0 m | lockstep | **none** |
| `N3-high` | 1.0 – 10.0 m | lockstep | **none** |
| `N4-high-spring` | 1.0 – 10.0 m | **spring** (lagging, eased) | **none** |
| `P1-shake` | 1.0 – 10.0 m | spring | **3.0 analysis-px peak** |

**`N0-flat` is not a trivial leg and not a re-run of `synth_pan.mp4`.** A perspective camera pitched 52.95° at a flat plane sees depth varying down the frame, so a camera translating parallel to that plane induces a **non-uniform image flow with zero relief in the scene**. N0 isolates the parallax a follow-cam cannot avoid even in an empty room. `np.roll` has none of it.

**`P1-shake` is a matched positive control and G-5 did not ask for it.** A null alone cannot show the instrument would have *seen* a shake had one been there — the *"instrument returns cleanly after it stopped answering the question"* shape this run has now hit repeatedly. Its amplitude is specified in **the operator's own units** (analysis pixels on the 1280×720 raster `analyse_depth` resamples to) and converted to metres through the camera's focal term at the subject's stand-off: 3.0 px = **0.054959 m** of camera displacement at 23.1627 m. That is **6× the operator's hardcoded 0.5 px absolute floor**.

### 2.2 The camera — ratified, transplanted, pinned, and not edited

The pose is `player_lock` at **k = 0.665**, the Matt-ratified camera (R-CPB-18). The construction is copied line-for-line from `kc2_cpb_clip.gd::_playerlock_pose()` into the new file and **pinned against the same `pl_audit.json`**, so a mistyped digit fails at the pose rather than in a floor three steps on. Every leg printed:

```
[g5] player_lock PIN vs tmp/br2watch/m6/pl_audit.json: offset delta 0.000000000000 m,
     z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
```

**No ratified-camera code path was edited.** This is the WW-8a pattern: a fresh file that re-derives the vector and checks it. `--pitch` / `--fov` / `--plk` are exposed so a later cell can approximate a reference clip's cam geometry; the **pin only fires on the ratified operands** and prints NOT-APPLICABLE otherwise, rather than failing an assertion it was never meant to satisfy.

### 2.3 What is deliberately absent from the scene, and why it is a measurement decision

Fog, glow, SSAO and **shadow maps** are all off. Every one of them is a **temporal** term, and a temporal term in a null clip is authored high-frequency image content **with no camera motion behind it** — it would inflate the very floor the clip exists to establish. A moving camera re-rasterising a shadow map every frame is the worst offender. The null reports the parallax term alone, and says so in its own manifest under `scene_terms_deliberately_absent`.

Albedo is multi-octave value noise, **world-triplanar**. Flat albedo would give an 8×8 grid of ill-conditioned tiles and the camera fit would be measuring the operator's failure mode instead of the scene's parallax; per-instance UVs would put a scale-dependent spatial frequency into the flow and **confound the relief sweep with a texture sweep**.

### 2.4 The ground truth — the part that is not just a clip

Each leg ships a manifest with, **per frame**, the camera transform, the subject position, and this:

> Take the **previous** frame's six world probe points (a vertical stack at heights 0/1/2/4/8/16 m above the screen-centre ground point) and re-project them through **this** frame's camera. The six displacements are the true image motion at six depths — the six answers the operator's single `tx` has to average into one. Their **spread** is the disagreement the global fit must absorb.

A rigid pan has spread **0.000 by construction**. `synth_pan.mp4` has spread 0.000. This ladder has **4.44 – 4.58 px per frame**, against a true ground-level image motion of ~3.78 px/frame. **That is the quantity G-5 says is missing, stated as a number, per frame, in the operator's own raster.**

⚑ **The probes are analytic and camera-only, so the ground truth is IDENTICAL across the four relief legs — and that is the design, not a bug.** It separates *"how much parallax this camera and path COULD produce"* (constant, mine) from *"how much of it the global fit actually inherits"* (varies, galadriel's). A relief-dependent probe would have confounded the two and neither number would have meant anything.

---

## 3. Evidence

### 3.1 The clips (promotion receipt)

`/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-25-vfx-depth-g5-camnull/g5-camnull-receipt.txt`

Six clips, each **150 frames counted off the decoded stream** (not read from the header), 1920×1080 @ 30/1, libx264 crf 12 preset slow (near-lossless, so the floor is not an h264 artefact), sha256-pinned. Manifests + shas in `evidence/`.

Per Class-E convention the **mp4s live on disk and their shas live in text** — the clips are not committed; the receipt, manifests and check script are.

### 3.2 Consumability check — the operator loads them unmodified

`evidence/g5-consumability-check.py` → `evidence/g5-consumability-check.json`. Ran `frame_forensics_depth.analyse_depth()` **unmodified** on all six legs:

| leg | relief | cam | authored | gt spread | `hf_p99` | `shake_bar` | spike frames | `hf_to_pan_ratio` |
|---|---|---|---|---|---|---|---|---|
| N0-flat | flat | lockstep | 0.00 | 4.583 | **0.0967** | 0.5000 | **0** | 0.026 |
| N1-low | low | lockstep | 0.00 | 4.583 | **0.1260** | 0.5000 | **0** | 0.034 |
| N2-mid | mid | lockstep | 0.00 | 4.583 | **0.2316** | 0.5000 | **0** | 0.060 |
| N3-high | high | lockstep | 0.00 | 4.583 | **0.4225** | 0.5000 | **0** | 0.093 |
| N4-high-spring | high | spring | 0.00 | 4.441 | **0.3401** | 0.5000 | **0** | 0.076 |
| **P1-shake** | high | spring | **3.00** | 4.482 | **4.5838** | 0.5000 | **18** | **1.034** |

**Three things this shows, none of which is the floor:**

1. **The clips are consumable.** `F7_shake` comes back fully populated on every leg with no change to her pipeline, and the fitted `pan_mean_px` (3.75 – 4.55) lands between the ground truth's near-depth (3.78) and far-depth motion, which is what a global fit over mixed depths *should* do.
2. **The residual is monotonic in relief** — 0.097 → 0.126 → 0.232 → 0.423 px across flat/low/mid/high, at a fixed camera, path and speed. **That relationship is the thing G-5 said could not be measured**, and it is now a curve rather than an assumption.
3. **The pair separates by ~13.5×** (P1 4.584 vs its matched null N4 0.340), 18 spike frames against 0. The detector sees an authored 3 px quake cleanly.

⚑ **AND ONE THING I AM FLAGGING RATHER THAN RULING ON, because it is hers.** On every one of these six legs `shake_bar_px` came back **exactly 0.5000** — the derived term (`median + 6·MAD`) never once exceeded the hardcoded absolute floor, so on this ladder the detector is **entirely floor-governed**. `N3-high`'s worst frame (`hf_max` **0.4419**) sits at **88 % of that bar with zero margin to spare**, at a pan rate of ~3.8 px/frame and a relief ceiling of 10 m. **I am not saying the bar is wrong.** I am saying the null now exists to test whether a faster pan or deeper relief crosses it, and that test is one `SPEED=` re-run away.

`hf_to_pan_ratio` may travel better than `hf_p99` for that purpose: it separates the pair 11–40× and is scale-free, so it does not need the reference clip and the null to share a pan speed. **Offered as an observation from the builder's chair, not a recommendation for her operator.**

### 3.3 x2 determinism

Everything that moves is a pure function of the frame index — subject path, spring-cam lag (precomputed over the whole clip at `_ready`, so it is a table lookup and not an accumulator), shake envelope, and scene layout (one seeded RNG drained in one fixed order, **including for unfilled cells**, so two relief legs are the same world at two heights rather than two different worlds). Nothing reads `delta`.

**That is the design; the receipt is the measurement.** `N0-flat` re-rendered end-to-end into a separate OUT/TMP and compared: see § 3.4.

### 3.4 x2 result — **GREEN, byte-identical, on both artifacts**

`N0-flat` re-rendered end to end into `OUT=/tmp/g5_x2_out TMP=/tmp/g5_x2_tmp` and compared against the promoted deliverable:

```
d1ee0ef3e60a67d48adaab3fc65dce642bd59c5d83b2fbe45cdc5c92cd2b4bda  .../g5-camnull-N0-flat-1920x1080.mp4   (pass 1, promoted)
d1ee0ef3e60a67d48adaab3fc65dce642bd59c5d83b2fbe45cdc5c92cd2b4bda  /tmp/g5_x2_out/g5-camnull-N0-flat-1920x1080.mp4  (pass 2)
                                                                  cmp -s -> GREEN, byte-identical

bfd1f23a08228282b33755b0ef3d31826079094d1093cecabe336d9e3a5a967d  .../evidence/g5-manifest-N0-flat.json  (pass 1)
bfd1f23a08228282b33755b0ef3d31826079094d1093cecabe336d9e3a5a967d  /tmp/g5_x2_out/evidence/g5-manifest-N0-flat.json  (pass 2)
```

**Byte-identical at the container level** — no fallback to per-frame decoded hashes was needed, and **the manifest matched too**, which is the stronger of the two claims: it says the camera, the path and the ground truth walked the identical sequence, not merely that the encoder was reproducible. The CLK-1 tick-frozen preroll is doing its job.

⚑ **One leg, not six.** A determinism claim measured on `N0-flat` and asserted for `P1-shake` would be an extrapolation; the shake envelope is `exp`/`sin` of a frame index and has no new nondeterminism available to it, but **that is an argument, not a receipt**, and it is labelled as one here.

---

## 4. Guarded-files check

Required output, `git -C ~/Games/reincarnated-godot diff --name-only fc26b80..HEAD`:

```
scenes/g5_camnull.tscn
scripts/g5_camnull.gd
scripts/run_g5_camnull.sh
```

Three paths, all new files. The two greps run over that same diff:

```
$ git diff --name-only fc26b80..HEAD | grep -E "wwcr_|run_wwcr_stage"
ZERO guarded-path hits

$ git diff --name-only fc26b80..HEAD | grep -E "kc2_cpb_clip|wr2_playback|kc2_arena"
ZERO ratified-camera hits
```

Landing commit: **`f0e8d6dc5d6512821cb1e9da3411fddae466e0c3`**. Post-commit contents verified with `git show --stat HEAD` (**not** `git diff HEAD~1`, which on a shared working tree names other sessions' uncommitted files): 3 files changed, 1238 insertions.

**Zero hits on `scripts/wwcr_*`, `scenes/wwcr_*`, `scripts/run_wwcr_stage.sh`.** Zero hits on any ratified-camera code path (`kc2_cpb_clip.gd`, `wr2_playback.gd`, `kc2_arena.gd` are all untouched — read only, for the transplant).

---

## 5. Two defects the build's own ground truth caught, before either reached a deliverable

Both are the same shape, and it is the shape this run keeps meeting: **the instrument ran, returned cleanly, and had stopped answering the question.** Recording them because the near-miss is the finding.

**(a) The path was walking down the view axis, not across it.** First cut moved the subject along world **+X**. The pose's yaw is 47°, so world +X is **73 % *along* the camera's view direction** — the camera was **dollying backward**, not panning across. A dolly is a *scale* change; the affine fit puts it in the scale term, **not `tx/ty`** — so the null would have been a null for a feature F7 does not read. It would have rendered, encoded, promoted, and answered the wrong question. **The manifest's own `true_motion_px` numbers are what caught it**: 0.21 px against an intended ~3.6, on a 6-frame headless probe, before anything was rendered at length. The path is now defined in the camera's frame — lateral carries the pan, a ±3 m weave along the view axis keeps the subject's depth changing.

**(b) `Camera3D.unproject_position()` was reporting against a 64×64 viewport.** It maps to the **live viewport rect**, which under `--headless` is 64×64. The screen-centre ground point came back at (32, 32) and every true-motion figure was **~17× too small**. No error, no warning, and the numbers were plausible enough to write down. ⚑ **And the sting is that the smoke path — headless, cheap, the one you probe with — is exactly the path where it lies.** A full 1920×1080 render would have been right, so the bug was reachable **only by the tool used to check for bugs.** The ground truth is now projected analytically from the camera's own transform and fov against the **declared** render size, and `_projection_selfcheck()` prints the disagreement against `unproject_position` rather than assuming it away.

**(c) A trailing duplicate frame, which in a shake null is not harmless.** `get_tree().quit()` requests a quit at the *end* of the frame, so Movie Maker writes one more PNG after the scene stops advancing — measured, `raw = preroll + frames + 1`, every leg, every time. That frame is content-identical to its predecessor, so the frame **pair** it forms has **zero camera motion** — a spike in the high-frequency component of precisely the series being floored. It would have made the null read **louder than the truth**, in the direction that matters. `prune_tail()` removes everything at index ≥ `PREROLL + FRAMES`, by index rather than by count.

---

## 6. Handed to the harness, not to G-5 — a fact worth someone's attention

⚑ **The windowed Godot viewport on this host is 1920×971 while Movie Maker writes PNGs at 1920×1080.** Measured, printed by the self-check on every deliverable leg:

```
[g5] projection self-check: viewport 1920x971 · declared render 1920x1080 ·
     analytic (960.000, 540.000) px vs unproject_position (960.000, 485.500) px · |delta| 54.5000 px
```

The window is clipped by the Mac menu bar; the encoder is not. **So `unproject_position` is wrong by a vertical factor of 1080/971 ≈ 1.112 in ANY Movie-Maker render on this host, not only in headless.** I have not audited whether any other harness file measures screen position that way — that is a survey, not G-5, and I am naming it rather than doing it. Routed to **galadriel** (measurement) and **jack-ryan** (whether it touches anything already ruled on).

---

## 7. Remainder for galadriel

**G-5 itself is discharged** — the render deliverable its remedy names exists, is consumable, and separates its matched pair. What remains is hers, and none of it was in G-5's wording:

1. **Read the floor and write it.** Six legs, her operator, her note. I have deliberately named no F7 bar; a builder stating the floor his own clips produce is marking his own homework (WW-8a discipline). The consumability table in § 3.2 exists so she knows the instrument is worth pointing at something — not so she can skip pointing it.
2. **The pose-transfer assumption, which is live and named.** Every leg is at the ratified `player_lock` pose. A reference clip has its own cam geometry, so **transferring this floor to a reference leg is an assumption until the null is re-rendered near that reference's pose.** `--pitch` / `--fov` / `--plk` exist for exactly that and cost one re-run per pose (~2.5 min/leg). **The gap is closed for our legs; for reference legs it is closed conditionally.**
3. **The speed axis is unswept.** One `SPEED=` value (2.0 m/s → ~3.8 px/frame). Given `N3-high` sits at 88 % of the 0.5 px bar, the residual's behaviour above this pan rate is the obvious next rung and I did not climb it.
4. **G-4 is adjacent and was not touched.** Sub-pixel motion compensation is her named remedy there; this ladder would serve as its control too, since it has known per-depth true motion — but that is her build, not mine.

**Also still open, out of scope here, named so it does not get lost:** R-21(b) left drax a `kc2_cpb_clip.gd:111` → `:119` line-number correction in my own W1 note. Not touched by this cell; it is record-truth hygiene on a prior artifact and belongs to my next touch of that file.

---

## 8. Disk

R-18c honoured per leg: PNG ladders pruned **only after** the encoder's exit status, a nonzero output, a dims-from-bytes gate and a **count** gate — six receipts in the promotion file, ~0.23 G reclaimed each, peak PNG on disk **one leg, never six**. Free space at close: **48 GiB** — unchanged from the 48 GiB at open, across seven full 211-frame renders (six legs + the x2 pass). The six promoted mp4s total **~24 MB**.

**One untidiness, named rather than left:** `/tmp/g5_camnull/frames-SMOKE-12f-N2-mid/` holds ~96 MB of black PNGs from the very first smoke — the run where the script failed to parse and Godot rendered an empty scene until `--quit-after` fired. It is dead intermediate from a HALT, outside `captures/`, and safe to `rm -rf` at any time. `/tmp/g5_x2_tmp/` and `/tmp/g5_x2_out/` are likewise disposable once § 3.4 is read.

---

## 9. Reproduce

```bash
cd ~/Games/reincarnated-godot
bash scripts/run_g5_camnull.sh                          # whole ladder, ~18 min
LEGS="N3-high" bash scripts/run_g5_camnull.sh           # one leg, ~2.7 min
FRAMES=12 PREROLL=3 LEGS="N2-mid" bash scripts/run_g5_camnull.sh   # smoke; CANNOT promote
SPEED=4.0 LEGS="N3-high" bash scripts/run_g5_camnull.sh # the unswept axis in § 7.3
```

The smoke knob renames every artifact `-SMOKE-` and the promotion gate refuses a smoke name, so a short clip has **no path to `captures/`**.
