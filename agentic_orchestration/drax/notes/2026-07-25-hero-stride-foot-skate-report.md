# hero walk foot-skate — the constant was wrong, but not by 11 %, and the real defect is elsewhere

**From:** drax (presentation seam) · **To:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-hero-stride-foot-skate.md`
**Stack:** Godot **4.6.3.stable.official.7d41c59c4** · Metal · Apple M2 · macOS 24.6.0

---

## Verdict in one line

**The hypothesis is half right, and the half that is wrong is mine.** The constant *was*
too large and it *is* now fixed — but by **+4.0 %**, not ~11 %. The ~11 % figure came from
my own L6-PREP §8, which compared the clip's stride **in the source rig's space** against a
constant that lives in **the hero's post-scale travel space**. Two different frames. The
missing term is `hero_walker.gd`'s own `TARGET_HEIGHT` scale, 0.877497.

And the constant is the small half. **The retarget destroys the source clip's foot lock**,
and that accounts for **~75 % of the measured skate**, which no scalar can reach.

| # | question | answer |
|---|---|---|
| 1 | Is the mismatch real **at the frame**? | **YES** — rendered and counted: **0.0366 m** mean planted-foot slide per stance, 19 stances. Real, but **not conspicuous** on this character (see §1.3). |
| 2 | Which number governs? | **The hero's own planted-foot travel in TRAVEL-NODE space: 1.297 ± 0.003 m/cycle.** Not the clip's 1.500 — wrong frame. |
| 3 | Does the retarget rescale? | **The pose: NO (×1.00003). The root track: YES, ×1.13280.** And binding to the hero **breaks the foot lock outright.** |

**Fixed:** `reincarnated-godot/scripts/hero_walker.gd:69` — `STRIDE_PER_CYCLE` **1.35 → 1.30**.
**HALT to gandalf:** §5. The retarget-fidelity finding re-scopes L6.

---

## §0 — The hypothesis, re-verified line by line

The dispatch asked me to treat its §0 as a hypothesis **including the line number**. Checked:

| claim | verdict |
|---|---|
| `hero_walker.gd:44` declares `STRIDE_PER_CYCLE := 1.35` | **TRUE at the time of the dispatch.** Line 44 exactly, value 1.35. (Now line 69 after the fix's comment block.) |
| "the clip it drives" | **PARTLY.** Line 38 names `A_MOD_BL_Walk_F_Masc` — the **in-place** twin, which has **no root position track at all**. The `_RM_` twin is not vendored in `reincarnated-godot` (0 hits under `Assets/`); it lives only in Matt's pack and in `mcp-lab/l6prep`. Reading the `_RM_` twin as this clip's declared stride is nonetheless **legitimate and I confirmed it independently** — see §2. |
| "measures 1.500 m/cycle" | **TRUE, in the source rig's own space.** Independently re-confirmed two ways in §2. |
| "~11 % mismatch" | **FALSE, and the error is mine.** 1.500 and 1.35 are not in the same frame. In the same frame the gap is **+4.0 %**. |
| "foot-skate, visible in the register an ARPG camera looks at" | **Half true.** It is real and measurable at that register. It is **not conspicuous** there, because the shipped hero is a floor-length-robed wizard whose feet are largely occluded. §1.3. |

---

## §1 — Is it real at the frame?

### 1.1 The pictures

`~/Games/mcp-lab/harness/out/`

| artifact | what |
|---|---|
| `hero_stride_before/` | STRIDE = **1.35** (as shipped), 160 f @ 40 fps = **4.0 s**, 1280×720, ARPG framing at 7.0 m |
| `hero_stride_after/` | STRIDE = **1.30** (measured), same everything |
| `hero_stride_detail_before/`, `hero_stride_detail_after/` | same pair at 2.9 m, aim-height 0.38 — the feet and the ground trace |
| `hero_stride_AB/AB_gameplay_f140.png` | **the before/after plate at the gameplay register** |
| `hero_stride_AB/AB_marks_f100.png` | one stance, magnified 6× |
| `hero_stride_AB/AB_detail_f100.png` | detail framing, 3× crop inset |
| `DETERMINISM_hero_stride.json` | re-render identity |

Each folder carries `.mp4`, `.gif`, a 12-thumb timestamped `_strip.png`, the numbered
frames, and `render.log` with the full invocation.

```bash
cd ~/Games/mcp-lab/harness
bash bin/shoot_clip.sh hero_stride_before res://clips/hero_stride_before.gd \
     --fps 40 --duration 4.0 --width 1280 --height 720 --settle 30 \
     --dist 7.0 --fov 30 --aim-h 0.90
```

### 1.2 The diagnostic, and why it is this one

A numeric mismatch is not a defect until a frame shows it, and a **still** cannot show
foot-skate at all. So the clip drops a **dot at each ball (toe) joint's world position on
every frame it is in contact**, plus a **white anchor** where the foot landed and a **live
tether** from that anchor to where the foot is now. **The tether's length is the slide, in
metres, live.** A planted foot leaves a point; a skating foot leaves a dash. The ground
carries 0.5 m stripes as the ruler.

**Purity held (motion_clip's seek contract).** The dots are not accumulated at runtime: the
whole contact schedule is a function of *t*, computed in `build()`, every node created up
front, and `set_time(t)` only toggles visibility and rescales the tethers.

**Counted by the render itself**, independently of the analytic estimator:

| run | stances | mean slide / stance | max slide / stance |
|---|---|---|---|
| **BEFORE, STRIDE = 1.35** | 19 | **0.0366 m** | 0.0438 m |
| **AFTER, STRIDE = 1.30** | 19 | **0.0129 m** | 0.0220 m |

**−65 % mean, −50 % worst-case.** The analytic prediction was 0.032 m per stance; the render
counted 0.0366. Two independent paths, 14 % apart, same conclusion.

### 1.3 The honest reading of the picture

At the ARPG register the **ground trace shows it plainly** — the before dashes are visibly
longer than the after dashes in `AB_gameplay_f140.png`. **The character does not.** The
shipped hero is `SK_Chr_Male_Wizard`, a floor-length robe; his feet are occluded for most
of the gait, and 3.7 cm of slide on a 1.8 m figure at 7 m is at the edge of perceptibility.

I am not going to claim the frame screams. It does not. **The defect is real, it is
measurable at the frame, and on this particular character it is quiet.** It would be louder
on a bare-legged mob — which is exactly the content L6 is about to add.

### 1.4 Accumulator lockout

**Held — no tolerance declared, none needed.** The clip uses `deterministic_env()`
unmodified. Separate-process re-render of `hero_stride_after`:

```
framediff: rerun_identity
  pairs           : 160
  byte-identical  : 160 / 160
  pixel-identical : 160 / 160
  scale bar (adjacent frames of the motion): 63,582..66,582 px changed, max channel delta 229
```

Both MP4s share sha256 `3d68920ff2f47443b6189b3082fb22265ac6f4a293456049b6ba0ad9d5dae95c`.

---

## §2 — Which number governs

**Four candidates, and only one of them is in the frame the constant operates in.**

`set_walk_speed` sets `speed_scale = (mps / STRIDE) · clip_len`, so the clip completes one
cycle in `T_eff = STRIDE / mps`. A planted foot is world-stationary iff
`mps = S / T_eff` where `S = −d(foot)/d(phase)` during stance. Substituting gives
**`STRIDE == S` exactly** — the constant must equal the planted foot's backward travel per
unit clip phase, **measured in travel-node space, i.e. after the `TARGET_HEIGHT` scale.**
That derivation is the whole subtlety and it is what my §8 got wrong.

| # | candidate | value | governs? |
|---|---|---|---|
| a | clip's authored stride, **on its own 121-bone authoring rig** | **1.49696** | **No — wrong frame** |
| b | (a) × the hero scale 0.877497 | **1.3136** | Close; the geometric prediction |
| c | **measured planted-foot travel on the shipped hero, travel-node space** | **1.2980** | **YES** |
| d | the declared constant | 1.3500 | — |

**(a) is confirmed twice over and is not in doubt.** On the clip's own rig the walk is
**perfectly foot-locked**: the ball's height holds constant to **0.3 mm** and its backward
rate to **±0.6 %** for the entire stance, on **both** feet — and that rate, 1.49696, matches
the `_RM_` twin's authored root translation of **1.500 m** to **0.20 %**. Synty's root
motion and Synty's feet agree. It is simply not the hero's number.

**(c) is the answer, and it is stable.** `scripts/tcp_stride_sens.gd` sweeps the contact
threshold from 0.10 to 0.50 of the ball's own vertical range:

| threshold | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|---|---|
| **D\*** | 1.2970 | 1.2970 | 1.2960 | 1.2980 | 1.2990 | 1.2970 | 1.2960 | 1.2940 |

**Spread 0.005 m = 0.4 %.** Every threshold puts D\* **3.9–4.3 % below** the declared 1.35.
The 1 %-of-minimum basin is 1.29–1.31 at every setting.

**Shipped value: 1.30.** It is inside the measured basin at every threshold and within 1.0 %
of the criterion-free geometric route (b). Rounding to three significant figures is
deliberate — a criterion spread of ±0.005 does not support a fourth digit.

**One coincidence worth killing.** 1.35 = 0.90 × 1.50 exactly. The hero scale is **0.8775**,
not 0.90. So the old constant was **not** a scale correction someone got slightly wrong; it
reads as eyeballed. Nothing was compensating for anything, which is why replacing it is safe.

---

## §3 — Does the retarget change the stride?

Measured in `mcp-lab/l6prep` on the clip's **own** skeleton — no character, no cross-rig
binding — with raw and retargeted imports of the same two files side by side
(`tools/stride_source.gd`).

| case | bones | hips rest y | root NET | foot rate |
|---|---|---|---|---|
| RAW in-place | 121 | 0.88276 | — (none) | **1.49696** |
| RAW root-motion | 121 | 0.88276 | **1.50000** | 0.0023 (≈0 — the root carries it) |
| RTG in-place | 121 | 0.88276 | — (none) | **1.49701** |
| RTG root-motion | 121 | 0.88276 | **1.69921** | 0.0022 |

**Three findings, in ascending order of how much they matter.**

### 3.1 The pose is untouched — ×1.00003

`1.49696 → 1.49701`. `rest_fixer` with `fix_silhouette` + `overwrite_axis` +
`normalize_position_tracks` leaves the bone-**rotation** motion, and therefore the foot
trajectory, bit-for-bit where it was. Good news, and it means the retarget is not the
suspect for the constant.

### 3.2 The ROOT TRANSLATION TRACK is rescaled by ×1.13280 — **a live trap for L6**

`1.500000 → 1.699207`. That factor is exactly `1 / 0.882765` = 1 / the rig's hips rest
height. `retarget/rest_fixer/normalize_position_tracks` divides position tracks by the
skeleton's **motion_scale**; Godot expects the consumer to multiply it back.

> **Anyone who reads a retargeted `_RM_` clip's root track as metres gets 13.3 % too much
> travel.** It is silent, it looks like a plain number, and every one of the 3,386 clips my
> L6-PREP report proposed to retarget will carry it.

This is not the hero-walk defect — `hero_walker` drives the in-place twin and never reads a
root track. It is a defect the *next* consumer walks into.

### 3.3 Binding to the hero DESTROYS the foot lock — and this is the real defect

Same clip, applied to `SK_Chr_Male_Wizard` through the same bone map:

| | ball height during stance | backward rate during stance | L vs R plant height |
|---|---|---|---|
| **source authoring rig** | constant to **0.3 mm** (0.0224 ± 0.0003) | constant to **±0.6 %** (−1.489…−1.506) | matched |
| **shipped hero** | wanders **2.2 cm** | wanders **1.15 … 1.39** (±9 %) | **3.5 cm apart** |

And it is **not** an asymmetric rest. The hero's rest is mirror-exact — leg chains
L/R = 0.886946 / 0.886946, **ratio 1.000000**; ball rest y identical at −0.002980 on both
sides. The asymmetry is entirely in **the animation as retargeted onto different
proportions.** Retargeting maps rotations; a foot lock is a property of the exact limb
lengths it was authored against, and it does not survive re-proportioning without IK.

**The size of it:** total planted-foot slip is **0.0884 m/cycle at 1.35** and
**0.0664 m/cycle at the best possible constant.** The constant fix removes **25 %**.
The remaining **75 % is the broken foot lock, and no scalar can reach it.**

---

## §4 — The fix, and what else reads the constant

`reincarnated-godot/scripts/hero_walker.gd` — `STRIDE_PER_CYCLE` **1.35 → 1.30**, with the
derivation, the frame-error correction, and the pointer to this report in the comment.

**Blast radius, enumerated in 13 passes and treated as a ceiling per the dispatch:**

| layer | searched | found |
|---|---|---|
| 1 | `STRIDE_PER_CYCLE`, all four repos | **1 reader**: `hero_walker.gd:132` (`set_walk_speed`) |
| 2 | callers of `set_walk_speed` | **2**: `walkthrough_ravine.gd:102`, `walkthrough_carved.gd:145` — both `WALK_SPEED = 1.5` |
| 3 | writers of `speed_scale` | **1**: `hero_walker.gd:134`, no other |
| 4 | files mentioning `hero_walker` | 10, of which 8 instantiate `HeroRig` |
| 5 | which of those 8 drive the walk | **2** (above). 2 use `set_paused_at_phase` (explicit phase → unaffected). 4 use no API at all (`shoot_hero_pose`, `probe_connector_cam`) or only cite it as a pattern in comments (`king_rig`, `mob_rig`) |
| 6 | re-implementations of the phase-match formula | **0** |
| 7 | literal `1.35` in `scripts/` + `scenes/` | 9 hits, **all unrelated** (sky energy, light energy, aim heights, transforms) |
| 8 | files using the `HeroRig` alias that the `hero_walker` grep missed | **0** (set difference empty) |
| 9 | `.tscn` attaching `hero_walker.gd` | **0** |
| 10–11 | `kit_replica_level` / `shoot_kit_replica` / `replica_playback` / `playshell` | **0** — `AGENT_STATE.md:818`'s claim that the kit replica preloads `HeroRig` describes a **superseded** state |
| 12 | every `.gd` naming `SK_Chr_Male_Wizard` | 10; only `hero_walker` couples travel to cadence. `spike_hero_walk.gd` is a static-pose spike with no travel |
| 13 | shell runners of the affected scripts | **1**: `run_ravine_walkthrough.sh`. `walkthrough_carved.gd` has no runner |

**Net effect on the two affected renders:** `speed_scale` 1.14815 → 1.19231 (**+3.8 %** leg
cadence). Travel path, video length and camera path are **unchanged** — both walkthroughs
advance by `_dist += WALK_SPEED/FPS`, which does not read the constant.

**Smoke gate — `scripts/tcp_stride_smoke.gd`, 11/11 PASS, exit 0.** Exercises the whole
public API the way both live callers do, and specifically asserts the new `speed_scale` is
the **unclamped** value with headroom on both sides of `clamp(0.4, 2.5)` — a constant change
that silently saturates the clamp would look fine and animate wrong.

---

## §5 — HALT to gandalf: the real fix is bigger than a constant

Per the dispatch's honorable fallback, **both** outcomes apply here: the constant was wrong
and is fixed, **and** the fix that matters is larger.

1. **The retarget does not preserve foot locks** (§3.3). A perfectly locked source becomes a
   2.2 cm-wandering, ±9 %-varying contact on the hero. The remedy is **foot IK** — a
   two-bone `SkeletonModifier3D` pinning the stance foot to its touchdown point — or a
   proportion-matched rig per character. Either is L6 scope and neither is a constant.
2. **Any per-character stride constant is now a per-character measurement**, because the
   number is a function of the character's limb lengths, not of the clip. L6 adding N
   monsters means N measurements — or foot IK, which makes the constant stop mattering.
   `scripts/tcp_stride_measure.gd` is the instrument; it runs headless in ~30 s.
3. **`normalize_position_tracks` silently inflates retargeted root tracks by 1/motion_scale**
   (§3.2, ×1.1328 here). This lands on all 3,386 clips the L6-PREP report proposed to patch.

Items 1 and 2 re-scope L6. Item 3 is a correctness trap in the pipeline L6-PREP recommended.

---

## §6 — Instrument bugs, all mine, all recorded

Four estimators returned four answers for the same rig, and the first three were wrong in
ways that each produced a **confident, plausible, false** statement about the asset.

| # | estimator | answer | why it was wrong |
|---|---|---|---|
| 1 | "the lower foot is the planted foot" | **0.641** | `ball_l` skims to **y = +0.001** at phase 0.625 while travelling **forward at +3.17 m/cycle**. It is low and swinging. **Height alone cannot detect contact.** |
| 2 | rigid-foot: \|v_ball − v_ankle\| < ε | **1.245**, per-foot **1.299 / 1.179** | The test is right for flat-foot and **rejects toe-off**, during which the foot pivots **on the ball** and the ball is still the contact point. The window closes early, on the low-rate half. |
| 3 | longest contiguous rigid run, middle 60 % | **1.229**, "**10.69 % L/R asymmetry**" | Same flaw; each foot's window landed in a different half of its stance. |
| 4 | **ball in the lowest N % of its own vertical range, moving backward** | **1.294–1.299 for every N from 0.10 to 0.50** | Stable. This is the answer. |

**Estimators 2 and 3 would have been filed as "the hero's right leg strides 10 % short" — a
rig defect that does not exist in that form.** It dissolved the moment I stopped letting a
heuristic pick the window and printed the raw velocity curves (`scripts/tcp_stride_dump.gd`).
Both feet show the *same* shape: rate starts ≈1.31 at heel strike and drifts to ≈1.15 by
mid-stance. That drift is the §3.3 defect; it is not asymmetry.

**Fifth bug, caught before it reached a frame.** The first attempt shipped the hero to the
harness as a `.glb` **with its animation**. glTF mangled it: the skeleton lost its `Root`
bone (50 → 49), 122 tracks → 36, **the feet flew** (`ball_l` y 0.023…0.395 against a native
0.004…0.090), and D\* off that glb read **1.126 — 13 % out**. A render from it would have
been a picture of the exporter. Caught by a **numeric clean-room verify**
(`l6prep/verify_clean/stride_glb_verify.gd`) *before* any frame was judged, and replaced by
a **baked pose table** — per-sample bone global poses relative to the skeleton node, which is
parent-chain independent and therefore survives the re-parenting. That bake verifies at
**0.000000 m worst-case ball error over 64 phases**, asserted inside every render's own log.

This is the same lesson as L6-PREP's headline, one turn further in: **98.7 % name-match with
a head below the floor** then; **all-green export with the feet in the air** now.

---

## §7 — Hygiene

- **`mcp-lab/project/` and `mcp-lab/evidence/l5/` — NOT TOUCHED.** Both show recent mtimes;
  both are the **concurrent gandalf L5 cell**, demonstrably: `project/l5a_measure.gd`
  changed at **18:18:09** while I was running the hygiene check itself, and my last write
  anywhere was 18:13. `prep/l5d_residue/` — no changes at all.
- **`reincarnated-godot/project.godot` — untouched.** Its uncommitted diff is still exactly
  the pre-existing `mesh_lod/lod_change/threshold_pixels` removal the dispatch flagged as not
  mine. Not staged.
- **`mcp-lab/harness/` — still has no `.godot/`.** Its no-import-cache property is intact.
- **`user://` clean.** `reincarnated-godot/project.godot` sets no `file_logging` keys, so the
  desktop default (true) applies and my headless runs left 5 rotated engine logs in a
  `logs/` directory that did not previously exist. **Removed, directory removed.** I did not
  change the setting — `project.godot` is not mine this dispatch. `tcp-l6prep`,
  `tcp-l6prep-verify` and `tcp-motion-harness` hold zero non-cache files.
- **Probe scratch consolidated.** Five superseded probe scripts and their JSON/CSV deleted
  rather than committed; the record of their wrong answers is §6, which is where it belongs.
- **`l6prep` grew 16 MB → 19 MB** (two raw-import walk clips + the emitted artifacts).
  `emitted/` is `.gdignore`'d and cannot re-enter the import cache.

---

## §8 — Rulings

| # | ruling |
|---|---|
| **R1** | **`STRIDE_PER_CYCLE` was +4.0 % high, not ~11 %.** The 11 % figure was my own frame error: the clip's stride lives in the source rig's space, the constant lives in the hero's post-`TARGET_HEIGHT` travel space. **A restated measurement is only as good as the frame it was measured in, and mine did not carry one.** |
| **R2** | **The governing number is the hero's planted-foot travel per cycle in travel-node space: 1.297 ± 0.003**, stable across every contact threshold from 0.10 to 0.50. Shipped as **1.30**. Not the clip's 1.500, not 1.500 × scale. |
| **R3** | **Synty's `_RM_` root motion is trustworthy.** On its own rig the in-place clip is perfectly foot-locked at 1.49696 and its `_RM_` twin's root track reads 1.500 — **0.20 % agreement**, independently derived. Root motion and feet were authored consistently. |
| **R4** | **The retarget leaves the pose alone (×1.00003) and rescales the root position track by 1/motion_scale (×1.1328).** A consumer reading a retargeted `_RM_` root track as metres is 13.3 % wrong, silently. **Applies to every one of the 3,386 clips L6-PREP proposed to patch.** |
| **R5** | **Retargeting does not preserve foot locks.** A source locked to 0.3 mm becomes a 2.2 cm-wandering contact on a hero whose rest is mirror-exact. **75 % of the residual skate is this, and no constant can reach it.** Foot IK or proportion-matched rigs. **HALT-worthy: it re-scopes L6.** |
| **R6** | **Height alone cannot detect foot contact, and neither can a rigid-foot test.** A skimming swing foot passes the first; toe-off fails the second. Three estimators, three wrong answers, one invented rig defect. **Print the curve before trusting the statistic.** |
| **R7** | **Do not round-trip an animation through glTF and then judge frames from it.** It silently dropped a root bone and put the feet in the air while every structural check passed. **Bake the pose and verify it numerically against the native rig** — the pattern here verifies at 0.000000 m and L6 can reuse it (`scripts/tcp_stride_emit_glb.gd` + `clips/hero_stride_base.gd`). |
| **R8** | **The harness rendered a rigged, retargeted production character with no modification** — `bin/ab_compare.py` is the only addition, and that is a compositor, not a rig change. Determinism held: **160/160 byte-identical**, matching MP4 sha256, with a skinned 49-bone skeleton and 331 live trace nodes. |

---

## §9 — Read list

**Governing**
- `agentic_orchestration/dispatches/2026-07-25-drax-hero-stride-foot-skate.md`
- `agentic_orchestration/drax/notes/2026-07-25-tcp-l6prep-animation-probe-report.md` (§4, §8 — the finding this corrects)

**Changed (production)**
- `reincarnated-godot/scripts/hero_walker.gd` — the constant, 1.35 → 1.30, plus derivation

**Added (instruments, `reincarnated-godot/scripts/`)**
- `tcp_stride_measure.gd` — the answer + its 1 % basin
- `tcp_stride_sens.gd` — D\* vs contact threshold (the sensitivity that makes the answer trustworthy)
- `tcp_stride_dump.gd` — the raw velocity curves + rest geometry (the evidence behind §3.3 and §6)
- `tcp_stride_emit_glb.gd` — static glb + baked pose table for the harness (reusable by L6)
- `tcp_stride_smoke.gd` — the API smoke gate

**Added (`mcp-lab`, not a git repo)**
- `l6prep/tools/stride_source.gd`, `l6prep/tools/stride_dump_source.gd` — the raw-vs-retargeted bench
- `l6prep/verify_clean/stride_glb_verify.gd` — the clean-room check that caught the glTF mangling
- `l6prep/assets/anim_raw/` — raw (non-retargeted) twins of both walk clips
- `l6prep/emitted/hero_static.glb`, `l6prep/emitted/hero_walk_pose_table.json`
- `harness/clips/hero_stride_base.gd` + `hero_stride_before.gd` + `hero_stride_after.gd`
- `harness/bin/ab_compare.py`

**Read, not written**
- `reincarnated-godot/scripts/walkthrough_ravine.gd`, `walkthrough_carved.gd`, `spike_hero_walk.gd`, `probe_hero_rig.gd`
- `.../anim-base-locomotion/.../A_MOD_BL_Walk_F_Masc.fbx.import`
- `.../polygon-fantasy-characters/.../SK_Chr_Male_Wizard.fbx.import`
- `mcp-lab/harness/README.md`, `motion_clip.gd`, `bin/shoot_clip.sh`
- `mcp-lab/l6prep/README.md`, `tools/emit_final.gd`

---

## §10 — Wall clock (TCP-32: authoring separate from execution)

**Session: 17:37 → 18:22 EDT, 2026-07-25 — 45 minutes.**

| band | ≈ | notes |
|---|---|---|
| **Execution** (machine) | **~12 min** | 13 headless script runs (2–35 s each; the N=960 solves ~30 s); 1 headless import (2.6 s); **6 harness renders** (~55–70 s each); 1 framediff; 3 composites |
| **Authoring + analysis** (me) | **~33 min** | the math derivation before the code; 9 probe scripts written and 5 deleted; **4 estimator diagnoses**; the glTF failure diagnosis and the pose-table replacement; the 13-layer blast-radius enumeration; the fix + smoke gate; this report |

Execution was again not the constraint. **The single largest authoring cost was disproving
my own estimators** — three of them agreed the answer was "about 1.24" and one of them had
invented a 10 % left/right rig defect, and the only thing that settled it was printing the
curve and looking. The second largest was the glTF export, which passed every structural
check and put the feet in the air.

---

## Answer to the dispatch's question

**"Does the hero visibly skate?"** — Yes, by 0.0366 m per stance, and now by 0.0129 m. The
constant was 4 % wrong, not 11 %; the 11 % was my arithmetic across two coordinate frames
and gandalf restated it faithfully, which is exactly the failure mode TCP-35 exists to catch.
**The dispatch caught it because it refused to enforce my own number back at me.**

And the constant was never the main event. **The retarget breaks the clip's foot lock**, that
is three quarters of the skate, and it is a problem that gets worse the moment L6 puts a
bare-legged monster on screen.
