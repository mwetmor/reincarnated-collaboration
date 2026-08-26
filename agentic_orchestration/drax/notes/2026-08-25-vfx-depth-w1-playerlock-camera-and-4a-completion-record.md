# VFX-DEPTH RUN — WAVE 1 (drax) — COMPLETION RECORD

**Date:** 2026-08-25 · **Agent:** drax (presentation seam, `reincarnated-godot/`)
**Conductor:** gandalf (RUN-CONDUCTOR) · **Charter:** `gandalf/notes/2026-08-25-vfx-depth-run-charter.md`
**Class:** evidentiary note · **Status:** CURRENT
**Wave:** W1 — `player_lock` k=0.665 camera hook + 4a spin-following scuffs + the two CP#1 clips
**Commits:** `9923b6a` (camera) · `fde563c` (4a) in `reincarnated-godot`
**Status: COMPLETE.** No HALT. Four findings routed (§ 7), none of them blocking.

---

## 0. THE THREE CP#1 CLIPS — the deliverable, because the media is gitignored

Charter R-4: *"Matt's first look lands on the true datum, not the combat-camera or magnified
approximations."* All three are at the same camera language. **The paths ARE the deliverable.**

| # | Arm | Path | Verified |
|---|---|---|---|
| 1 | **HITL** — Matt's own hand, SB-1 `ww7-gate2` ratified-camera reference | `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-16-sb1-gate2-clip/ww7-gate2-cadence-ab-plk0665-1920x1080.mp4` | 12,749,012 B · sha256 `7e9764e3…c828ca` — **byte-intact, matches the dispatch's pin.** h264 1920×1080, 30/1 fps, 658 frames, 21.933 s. NOT re-rendered. |
| 2 | **twin AS-IS** — the clean-room build untouched, at the ratified camera | `/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w1-twin-asis-plk0665/plk06650_fxon.mp4` | h264 yuv420p 1920×1080, 60/1 fps, 210 frames, 3.500 s, 574,246 B · sha256 `0ea4a36fa68bef65…` |
| 3 | **twin + 4a** — spin-following scuffs, nothing else | `/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w1-twin-4a-plk0665/plk06650_fxon.mp4` | h264 yuv420p 1920×1080, 60/1 fps, 210 frames, 3.500 s, 574,571 B · sha256 `9662298acd598f88…` |

**Controls, rendered with each arm** (VFX layers hidden, pose + rotation identical — the only valid
occlusion baseline):
`…/wwcr_2026-08-25-w1-twin-asis-plk0665/plk06650_fxctl.mp4` and
`…/wwcr_2026-08-25-w1-twin-4a-plk0665/plk06650_fxctl.mp4`.

⚑ **The two control clips are sha256-IDENTICAL — `046ff09d853e6ed9188adabf7feac46ff9319e4da70b4208ac6c11bf12cb5f85`
— across the two builds.** That is the single strongest receipt in this record and it was not
designed for: it proves in one number that 4a moved **nothing** outside the VFX (pose, rotation,
translation, camera, stage, lights, animation clocks all byte-stable) **and** that the stage's
determinism pin still holds across a source change. Clips 2 and 3 differ from each other in exactly
one respect, and the control says so mechanically rather than on my word.

### ⚑ Clip 1's LABEL, corrected in the record

> ⚑ **RETRACTED IN PART, 2026-08-25 (W2b, drax). The struck sentence below is MY OWN OVER-CORRECTION
> AND IT IS FALSE.** Authority: charter **R-18(b)** (conductor accepted W2 F-2). The original text is
> struck rather than rewritten, because a note that silently changes its mind teaches nothing.

It is **the SB-1 `ww7-gate2` ratified-camera reference — Matt's own HITL treatment footage.** ~~It is
**NOT a whirlwind** and it is **NOT "the HITL arm"** of a whirlwind A/B;~~ `WW-7` is an SB-1 run-ledger
cell id. See `qa/pending/2026-08-25-my-ww7-miscitation-propagated-into-a-measurement-and-the-number-survives-under-a-different-name.md`.
My own prior completion record called it "the HITL object" of WW-AB. **That was wrong and I am
carrying the correction rather than leaving it to be re-derived.**

#### ⚑ THE RETRACTION, and what the source actually says

**The clip's subject IS a whirlwind cast.** `scripts/kc2_cpb_clip.gd:111-112`, verbatim:

> *"It exists to answer ONE question — does the **whirlwind** read, now that the man has a head, a
> hammer, and a rate Matt chose?"*

The Undead Knight spins a warhammer and throws cut/spark arcs at `CUT_PER_REV 17`. I read my own note
instead of the source, and the source settles it.

**BOTH THINGS ARE TRUE, AND CONFLATING THEM IS WHAT WENT WRONG TWICE:**

| claim | standing |
|---|---|
| `WW-7` is an SB-1 run-ledger **cell id**, not a whirlwind label | **TRUE — stands.** knight-rider's retraction of that mis-citation is correct and is not disturbed. |
| Therefore *"the clip is not a whirlwind"* | ⛔ **FALSE — retracted here.** A correct NARROW correction was generalised into a BROAD claim the source refutes. |

⚑ **The shape worth carrying out of this, and it is the whole reason the strike is visible rather than
edited away: the wrong claim arrived dressed as a CORRECTION, so it carried more authority than the
error it replaced.** A note that says *"actually, no"* is read as the settled version. Mine was read
that way, by me, in the very next wave — which is how it reached a dispatch.

⚑ **NOT THIS WAVE'S WRITE, and named so it is not mistaken for an omission:** the adjacent
knight-rider seal (collab `950f6656`, *"WW-7 was never a whirlwind"*) may need a reconciliation line
of its own. **R-18(b) flags that to jack-ryan — record-truth is his territory.** I have not touched
it and will not.

---

## 1. TASK 1 — the `player_lock` hook. THE PIN PRINTS `0.000000000000 m`.

`9923b6a` · `scripts/wwcr_stage.gd` + `scripts/run_wwcr_stage.sh`.

**I HALTED on this exact edit yesterday** (§ B.3 forbade any `wwcr_*` change and named a camera hook
as its example). Charter **R-1** discharges that HALT by ruling. It is discharged, not worked around.

**First run, both arms, verbatim from `render.txt`:**

```
[wwcr] PL-PIN unscaled offset (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       vs pl_audit.json (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       — |delta| 0.000000000000 m, z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
[wwcr] PL-CAM k=0.665000 — DOLLY only. pitch 52.9535411256029 deg  yaw 47.0 deg
       fov_v 31.7861018306101 deg VERTICAL/KEEP_HEIGHT  z_player 34.8165340347471 m
[wwcr] PL-CAM offset k=1 (the PORT, pinned above) = (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       stand-off 34.8311882019043 m  height 28.3970108032227 m
[wwcr] PL-CAM offset k=0.665000 (THIS RUN) = (9.7929267883301, 18.8840122222900, 9.1654367446899) m
       stand-off 23.1627407073975 m  height 18.8840122222900 m
[wwcr] PL-AUDIT anchor: subject ground projects to frac (0.501041571299, 0.550925191243);
       expected (0.501041450500, 0.550925123427);
       delta (0.000000120799, 0.000000067817) frac = (0.0002, 0.0001) px at 1920 x 1080
```

Every parameter I was given is met exactly: stand-off **23.1627407073975 m** · pitch
**52.9535411256029°** · yaw **47.0°** · fov_v **31.7861018306101° VERTICAL/KEEP_HEIGHT** · anchor frac
**(0.501041450500488, 0.550925123426649)** · **k = 0.665**.

**The anchor audit is a real test here, not a formality.** The offset solves the subject's ground
point onto the measured anchor ray at depth `zp`; scaling by k slides the camera *along that same
ray*, so the projection must not move at any rung. A moved anchor would convict the port. It moved by
**two ten-thousandths of a pixel** — single-precision residue.

**The 0.979-octave gap is closed, and I measured it rather than trusting the arithmetic.** Subject
bounding box, same effect, same build, mid-sustain: **206 × 242 px at `combat`** → **399 × 466 px at
`player_lock` k=0.665**. Linear ratios **1.937×** and **1.926×** against a predicted **1.971×** —
within 2 %. The comparison that had a second, silent variable in it no longer does.

**Design choices I made and am flagging rather than burying:**
- `_playerlock_aim` **ignores its `focus` argument and re-reads the caster.** The two call sites pass
  different things (`Vector3.ZERO` at build, `_king.position` per frame) and agree only because the
  king starts at the origin. *Happens to agree* is not a property.
- `cam` + `plk` were added to the C8 `key_axes` **in the same commit as the axis they describe.** That
  list IS the Gate-2 WARN-1 property — an fx arm must not file under the same declaration key as its
  own control — and it holds only while it names every axis the stage varies.
- `scripts/run_wwcr_stage.sh` gained `REPO` as an env override with a `project.godot` guard, so a
  **frozen-copy launch is a one-liner instead of an edit to a running script** (§ B.5's lesson made
  mechanical). `CAM` defaults to `combat`, so an unset invocation renders byte-identically to every
  stage-4 run before this.
- **The Tier-1 element sweep keeps its `inspect` camera.** It has no motion question and no AB
  counterpart; nothing is served by moving it, and moving it would break comparability with the
  landed element corpus for free.

---

## 2. TASK 2 — twin-AS-IS rendered FIRST, before 4a existed

Charter R-4 ordering, honoured literally: **`9923b6a` was committed, the AS-IS clip was rendered and
verified, and only then did `wwcr_whirlwind.gd` change.** At the moment clip 2 was captured, 4a was
not written.

- Mint's **own unmodified `CAPTURE=seq` path** (`ARMS=gate CAPTURE=seq`), both parameters authored by
  the mint for exactly this question.
- **Frozen-copy launch**: `/tmp/frozen_run_wwcr_w1_asis.sh`, sha256
  `4f46122caaf5c043d59ad3c73f39387d0f05c73c6f40d2f9378515f10324623c` — **re-verified identical to the
  in-tree runner after the run completed.**
- **Fresh stamp** `wwcr_2026-08-25-w1-twin-asis-plk0665`. The runner opens with `: > "$LOG"`; reusing a
  landed stamp would truncate an audited `render.txt`.
- `FRAME_CENSUS rendered=420 delivered=420`. `non_authored_emitter_count: 0` on both arms.

**Pre-fire disk projection, recorded BEFORE the capture** (Discipline #1.1): mean PNG **66,559 B
measured on this exact stage+camera** (not assumed) × 422 frames × 2 copies + a 28 MB MP4 budget =
**84.2 MB per render, 168.4 MB for both**, against **46 GiB** available. Actual consumption by my
directories: **~30 MB.**

---

## 3. TASK 3 — 4a spin-following scuffs. MOTION ONLY.

`fde563c` · `scripts/wwcr_whirlwind.gd`.

**The defect:** a scuff was spawned on the engagement ring and then sat perfectly still for its whole
0.22 s life. A blade at 900 °/s throws air; air that does not move is not evidence of a sweep, it is a
decal that blinks. The outer radius was being spent in quanta — correct — but the quanta carried no
information about the rotation that caused them.

**The mechanism, sign-locked to the rotation by construction:**

```
bearing(s) = ( sin s, 0,  cos s )     <- where the blade pass threw it
d/ds       = ( cos s, 0, -sin s )     <- where the sweep was HEADING
v0 = deg_to_rad(OMEGA_DEG) * _w * R_ENGAGE * SCUFF_ENTRAIN_FRAC
```

The direction is the **derivative of the bearing the spawn already used**, so its sign follows `_spin`
/ `OMEGA_DEG` and *cannot* be set to disagree with the rotation it is supposed to agree with. Rate is
`_w`-scaled: a scuff thrown during spin-up drifts slower than one at full song, because *"consistent
with the rotation"* is a claim about the **current** rotation, not about `OMEGA_DEG`.

**Predicted, then measured, and the 11 % gap reconciles exactly:**

| quantity | value |
|---|---|
| `v0` at full weight | 5.5213 m/s |
| continuous integral `v0·τ·(1−e^(−L/τ))` | **0.453801 m** |
| discrete left Riemann sum, dt = 1/60, N = 14 | **0.503620381752 m** |
| `selfcheck()`'s runtime measurement | **0.503620386123657 m** |

Nine significant figures; the residue is single-precision. **The gap is the quadrature term, not
drift** — the loop integrates at the pre-decay velocity, which necessarily overshoots a decaying
exponential. It is stated in the file so that no later reader convicts two correct integrals of
disagreeing. On screen at the judging camera: **41 px of travel over 14 frames for an 18 px quad;
8.2° of the ring.**

### R-9 compliance — receipts, not assurances

- `SCUFF_COLOR` is **byte-untouched**. `selfcheck()` now emits `scuff_color_rgb`
  `[0.620000004768372, 0.600000023841858, 0.560000002384186]` and `scuff_is_tinted: false` so this is
  checkable rather than asserted.
- **The `_tinted_nodes` assert passes, on both arms of the delivered run:**
  `"tinted_surfaces":["TrailRibbon","ContactSpark"]` · `"tinted_count_is_2":true`. No assertion
  failure in either log. As the charter reads it at source, the assert counts tinted *surfaces* and
  the scuffs are structurally outside it — but it was run, not reasoned about.
- ⚑ **AND R-9 IS CONFIRMED AT THE PIXEL LEVEL.** I diffed clip 2 against clip 3 frame-for-frame and
  sampled the 1,428 pixels 4a actually changed: mean RGB **[78.9, 79.3, 81.8]** — near-neutral, with
  **blue** marginally dominant (the stage's own ambient), where the wind element tint is
  `(0.72, 0.95, 0.82)` with **green** dominant. **The pixels 4a moved are dust, not tint.**
- 4a is a MOTION landing; colour is 4b/4c and Matt's eye at CP#1 against a **moving** reference (R-3).
  Landing both together would reach him as one undifferentiated *"better"*, which is a verdict on
  neither.

### Where the change actually is, localized rather than claimed

| frame | control-arm changed px | fx-on changed px | fx-on bbox |
|---|---|---|---|
| 60 | **0** | 131 | x[1102..1133] y[403..416] |
| 90 | **0** | 416 | x[757..1139] y[399..797] |
| 120 | **0** | 349 | x[757..798] y[781..812] |
| 150 | **0** | 532 | x[780..1163] y[430..840] |
| 180 | **0** | **0** | (none — post-release, `_w < 0.55`, no scuffs firing) |
| 205 | **0** | **0** | (none) |

The lock holds the caster's ground point at a **fixed** (962, 595) px by construction, so the
engagement ring projects to a fixed ellipse: predicted bbox **x[674..1250] y[365..825]**. Every
changed pixel falls inside it (the 15 px overshoot at y=840 is the 0.5 m tangential travel carrying
puffs off the ring, which is the landing). **Frames after release show zero change** — the effect
being off is the control that came free.

### The pre-registered falsifier, written before Matt looks

If the dust reads as **SLIDING** — skating outward on ice, detached from the ground —
`SCUFF_ENTRAIN_FRAC` is too high. If it still reads as **blinking decals**, too low. One constant
either way, and it is his eye's call at CP#1, not mine.

---

## 4. DEFEAT-CONDITION RECEIPTS — pasted mechanically, no eye-curation (#72)

`HEAD = fde563c`. Audited commit `1692d6e`.

### [1] The published command, VERBATIM (lineage-audit note lines 18–19)

```
$ git diff 1692d6e..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'run_wwcr_stage.sh' | grep '^+' \
    | grep -Ei 'vfxbo|cpb|kc2|a337d30|sb1|etch|claw|cut_|rig_poe1|cyclone|run_ww[0-9]|PAL_|decay_gamma|sheath'

+#   character-for-character from `scripts/kc2_cpb_clip.gd:304-317`, which itself
+#   READ-ONLY, PARAMETERS ONLY. `kc2_cpb_clip.gd` is quarantined-adjacent SB-1
+const PL_PITCH_DEG := 52.95354112560294       # kc2_cpb_clip.gd:304 <- wr2_playback.gd:1806
+	#   Same guard kc2_cpb_clip.gd:509 carries, and for the same reason.

[4 matching lines]
```

**Non-empty. Adjudicated below, and I do not read it as a defeat — but the ruling on that is
gandalf's, as the audit's author, not mine.** All four hits are **prose citing provenance**, plus one
constant whose comment names its source. Three of the four are comment lines whose entire purpose is
to declare where the camera came from.

### [2] The same command with the path corrected

```
$ git diff 1692d6e..HEAD -- 'scripts/wwcr_*' 'scenes/wwcr_*' 'scripts/run_wwcr_stage.sh' | grep '^+' | grep -Ei '…'
  -> the SAME 4 lines. The runner's 146 added lines contain ZERO hits.
```

### [3] Float-literal intersection (method § Q2) — 24 non-trivial shared values

Adjudicated one by one. Rows already adjudicated in the note's own POST-AUDIT DRIFT section
(`0.4912`, `0.20`, `2.6`, `5.6`, `7.0`) are unchanged and not re-litigated here.

| Value | Clean-room role (mine) | Adopted role | Adjudication |
|---|---|---|---|
| `52.95354112560294` `31.78610183061007` `1896.5577238618157` `54.47290422329346` `0.5010416666666667` `0.5509259259259259` `47.0` | the 8 `player_lock` **operands** | `kc2_cpb_clip.gd` const block | **ACQUITTED — and by ULTIMATE PROVENANCE, not by argument.** All eight are present verbatim in `scripts/wr2_playback.gd` (**not quarantined**), which is where `kc2_cpb_clip.gd` itself transplanted them from. Verified by grep, one occurrence each. |
| `14.7262048721313` `28.3970108032227` `13.7826108932495` `0.501041450500488` `0.550925123426649` `34.8165340347471` | the 4 **pins** | same | **ACQUITTED by ultimate provenance.** All present in `tmp/br2watch/m6/pl_audit.json` (**not quarantined**) — read and pasted into this record above. |
| `0.665` | the dolly rung `--plk` | the same rung | **ACQUITTED — it is the charter's own instruction.** R-4 mandates rendering at *this* camera; a differing k would be the defect. |
| `34.0` | pre-existing `CAM_DIST`, in a moved comment | camera const | **ACQUITTED** by the note's original § Q2 (`camera_floor1_ratification.md`). |
| `0.09` | `SCUFF_DRAG_TAU` — **seconds**, a drag time-constant | `TRAIL_SPREAD_M := 0.09` — **metres**, a trail half-width | different domains, different **units** |
| `0.10` | `SCUFF_ENTRAIN_FRAC` — dimensionless fraction of blade-tip speed | `CUT_EPOCH_GAP_LO_REVS` (revolutions) · `GRIP_SEAT_M` / `HAND_GAP_M` (metres) | different domains |
| `0.22` | `SCUFF_LIFE`, a **pre-existing mint constant**, appearing in a new comment | `ETCH_CORE_FRAC` · `ETCH_SHEATH_ENERGY_FRAC` · `SMOKE_EDGE_SOFT_FRAC` — dimensionless | different domains, and mine **predates the audit** |
| `8.2` | prose: "8.2 deg of the ring" | `kc2_cpb_clip.gd:1493` **`"tick %8.2f"` — a printf field width** | **not a numeric literal at all.** Same class as the note's own `7.0` (`%7.0f`) and `5.6` (a clause number) acquittals |

**Result: not one clean-room occurrence occupies the adopted role.** Zero floats crossed from
`kc2_player_channel.gd` or `kc2_etch.gdshader` — the two **effect-authoring** quarantined files — into
this landing. Every value taken from `kc2_cpb_clip.gd` is a **camera** value with a verified
non-quarantined origin.

### [4] The certified artifact

```
$ git diff --stat 1692d6e..HEAD -- scenes/wwcr_stage.tscn
    -> EMPTY. Byte-identical to the audited mint.
$ git diff --stat 1692d6e..HEAD -- scripts/wwcr_whirlwind.gd
    -> 124 insertions(+), 3 deletions(-)   [4a — by design, under R-3]
```

⚑ **`wwcr_whirlwind.gd` is the file the POST-AUDIT DRIFT section named as "the certified artifact —
the authored effect, the thing in the bake-off," and 4a moves it.** That is the charter's instruction
(R-3 fires 4a first) and it is why the defeat-condition test is now the operative protection rather
than a hash. **I am naming it explicitly rather than letting it be discovered**: the previous
disposition ("the certified artifact did not move") is no longer available, and the verdict now rests
entirely on the provenance test above.

---

## 5. Smoke gates run

| Gate | Result |
|---|---|
| Camera hook, marks mode, both arms | `FRAME_CENSUS rendered=20 delivered=20 expected=20` · PIN MATCH · no `ERROR`/`SCRIPT ERROR` |
| 4a, marks mode, both arms | `FRAME_CENSUS rendered=20 delivered=20 expected=20` · `tinted_count_is_2: true` · no assertion failure |
| AS-IS clip render | `FRAME_CENSUS rendered=420 delivered=420` · both MP4s ffprobed |
| 4a clip render | `FRAME_CENSUS rendered=420 delivered=420` · both MP4s ffprobed |
| Frozen runners vs in-tree, **after** each run | sha256 identical, both runs |
| Default path unmoved | `CAM` unset ⇒ `--cam=combat`, prefix literal `combat` — byte-identical invocation to every stage-4 run |

---

## 6. Two clips vs the HITL clip — the mismatches that remain, NAMED

A comparison with an unnamed second variable is not a comparison. **The camera is now matched. These
are not:**

| Axis | HITL clip 1 | twin clips 2 & 3 |
|---|---|---|
| fps | 30 | 60 |
| duration / frames | 21.933 s / 658 | 3.500 s / 210 |
| grammar | A/B cadence clip **with a seam and a concat** | one continuous window of one cast |
| subject | Undead Knight + large warhammer, **spins in place** | King showcase rig + greatsword, **translates at 3.5 m/s** during the channel (`ww-native-eor1` semantics — the lock dollies with him) |
| colour model | fixed white-hot→orange→red heat ramp, no element parameter | element-parameterized (wind here) |

**Matching § B.2's full list is not a camera hook, it is a second harness** — that remains true and
unbuilt. What changed is that **the dominant variable, the one that decides a density/palette/cadence
read, is gone.** The rest are named so Matt's eye is not asked to discount something silently.

---

## 7. FINDINGS ROUTED — four, none blocking

**F-1 — ⚑ THE PUBLISHED DEFEAT-CONDITION COMMAND HAS A BLIND SPOT, AND IT IS THE HARNESS.**
Route: **gandalf** (the audit's author).
The path list reads `'run_wwcr_stage.sh'`. The file is at **`scripts/run_wwcr_stage.sh`**, and the
published glob matches it **zero times**:

```
published glob :  3 files, 776 insertions
corrected glob :  4 files, 922 insertions   (+ scripts/run_wwcr_stage.sh, 159 lines)
```

**146 added lines are invisible to the test as written, and it exits 0 while missing them.** The
harness is precisely one of the files the POST-AUDIT DRIFT section itself listed as having moved — so
that section's own re-test never saw it either. This is the session's dominant failure shape one more
time: *an instrument that keeps returning cleanly after it stopped answering the question.* One-line
fix; I have not edited the note, because it is gandalf's artifact.

**F-2 — `mi.scale` HAS NEVER RENDERED ON THE SPARKS OR THE SCUFFS.** Route: **gandalf** (design call),
tracked in `AGENT_STATE.md`.
Measured, not recalled from a doc string — two identical `QuadMesh` quads at scale 1.0 and 3.0, same
`BILLBOARD_ENABLED` material, rendered through a `SubViewport` in this Godot (4.6.3.stable):
**156 lit px each, ratio 1.0000**, where a kept scale gives 9.0. `billboard_keep_scale` defaults
false and is not set. So `_age_pools`' spark **shrink** and scuff **growth** animations have never
been on screen, and **position is the only channel a quantum has** — which is why 4a's mechanism is
unaffected and why 4a is the first thing that makes the scuffs animate at all. **I left both lines
byte-untouched**: enabling `keep_scale` changes apparent puff and spark size, which is a second
variable inside a landing whose entire purpose is to isolate motion. It belongs to the 4b/4c
conversation or to a named landing of its own.

**F-3 — 26 GB of stale capture scratch in the Godot user dir.** Route: **knight-rider**.
`~/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike/` holds **27 GB**, of which
`s2c38`, `s2c38b`, `s2c38v3`, `s2c38v3b` are **4.2 GB each** and the `s2c12*` trio 1.7 GB each — S2C
intermediate PNG ladders already copied into `harness_logs/`. Free space moved **46 → 41 GiB** during
this wave against a **30 MB** footprint of mine; the pressure is entirely this. **Not deleted**: it is
another dispatch's scratch and deleting evidence someone has not copied out is a worse failure than a
disk warning. `harness_logs/` itself is **10 GB** and `.godot/` is **17 GB**.

**F-4 — my own near-miss, recorded because it is the third instance of one shape this session.**
I ran `ls` on the output directory **while the background encode was still running**, read a
**48-byte** `plk06650_fxon.mp4`, and formed the hypothesis "the fxon encode died." It had not — I had
read a file mid-write. The completed file is 574,246 B and ffprobes clean. **The correct first move
when a result surprises you is to establish the state you are observing** (is the job finished?) —
*before* forming any hypothesis about what the observation means. Cost: two tool calls. Cost had I
"fixed" it: a re-render of a correct artifact.

---

## 8. What I did NOT do, and why

- **Did not touch `SCUFF_COLOR`** — R-9's HUE/VALUE ruling makes it permissible, and R-3's ordering
  makes it wrong to land here.
- **Did not fire the 3A recapture or A1–A3** — serial godot lane, charter § 6; Wave 1 held it.
- **Did not re-render clip 1.** Instructed not to, and it is byte-verified where it stands.
- **Did not unify the `player_lock` and `combat` cameras.** They answer different questions; the
  measurement corpus depends on `combat` staying exactly where it is.
- **Did not touch `tmp/br2watch/measure/census.json`** — dirty, 23 days old, another workstream's,
  under review at `qa/pending/2026-08-25-a-23-day-old-uncommitted-ocr-regression-nobody-owns.md`.
  Left exactly as found, for the third time. (The charter's inheritance board assigns me the
  `census.json` quarantine write; **that is a separate landing and it has not been fired.**)
- **Did not enable `billboard_keep_scale`** — see F-2.

---

## 9. Push

Charter § 5 push posture (Matt, this run: *"push as you go"*, all repos the run writes). Instruments
per landing: `git status --porcelain -- <paths>` before, `git show --stat HEAD` after, `git -C <path>`
on every cross-repo operation.
