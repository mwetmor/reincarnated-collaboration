# Dispatch — 2026-08-25 — drax — CAMERA FRAMING (re-issued) + the WW-AB clean-room RENDER

**Status:** PENDING
**From:** knight-rider (Step-2 build wave, conductor)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Pattern:** B — two tasks, one serial godot session
**Sequencing:** fires now. Your lane is clear — the forward-axis dispatch closed with **Matt's verdict**: *"I confirmed that the _v3 mp4s from drax now have the character facing the correct way (forwards)."*
**Matt is away.** Both tasks are on his standing instructions. Do not wait on him; **surface, do not stall.**

---

## ⚑ 0. Why Task A is in front of you a second time, and why that is my failure

**Matt asked for this on 2026-08-25 and you never saw it.** I authored it as a *mid-flight addendum* to a dispatch you had already opened (`7d344a9b`), with `SendMessage` unavailable for the fifth confirmed time this session. **A dispatch amended after pickup is not a dispatch amended.** Verified against the tree rather than assumed: `s2a_stage.gd` still reads `CAM_PITCH := -55.0` / `CAM_DIST := 34.0`, and the only occurrence of "camera" in your completion record is in the out-of-scope list. Nothing about that is on you. It is re-issued here as its own file because that is the only channel that has ever reliably worked.

---

# TASK A — camera framing for the S2 review clips

**Matt, verbatim:** *"the zoom is too far out. please have it match our most recent completed godot rendering of camera angle/zoom from this mp4: `/Users/admin/Desktop/level-18-ice-golem-simulation.mp4`"*

## A.1 What the reference is — identified by two independent means, not assumed

`level-18-ice-golem-simulation.mp4` · 1600×900 · 30 fps · 40.4 s · 2026-08-02.

The only source in this repo that matches it is `scripts/wr2_playback.gd`. Its runner documents the invocation for that pick, by seed, at `scripts/run_wr2_playback.sh:25`:

```
CAM=arena_full FRAMES=1120 bash scripts/run_wr2_playback.sh wr3_acc acc boss FULL 74000909
```

Seed `74000909` is **on the frame**, in the HUD panel (`SIM · seed 74000909`) — I cropped at native resolution and read it rather than inferring from a filename. **So the reference camera is `arena_full`, NOT `player_lock`.** I state that I checked, because `player_lock` is the mode the source file itself calls *"THE GAME CAMERA"*, and assuming it would have been the natural error.

## A.2 The two cameras, from the constants

| | reference — `arena_full` (`wr2_playback.gd`) | current — S2 (`s2a_stage.gd:69-73`) |
|---|---|---|
| yaw | **47.0°** (`CAM_YAW_DEG:1669`) | **47.0°** — ✅ already identical |
| fov (vertical) | **40.0°** (`CAM_FOV:1671`) | **40.0°** — ✅ already identical |
| pitch | **−41.0°** (`CAM_PITCH_DEG:1670`) | **−55.0°** — ⚑ **14° steeper** |
| distance | **58.0 m** (`CAM_DIST_FULL:1710`) | **34.0 m** — ⚑ **24 m closer** |
| aim | datum + `(7, 1, 7)` NE bias (`CAM_AIM_NE_FULL:1717`) | focus + `(0, 1.2, 0)` |
| px/m @720p | **17.05** (their own published figure, `wr2_playback.gd:231`) | **29.09** = `360/(34·tan20°)` |

## A.3 ⚑ THE TRAP — DO NOT COPY `CAM_DIST_FULL`. TAKEN LITERALLY, MATT'S INSTRUCTION INVERTS ITSELF.

He asked for **less** zoom-out. Matching the reference literally means **34 m → 58 m**, world scale **29.09 → 17.05 px/m — a 41% reduction.** **The S2 camera is already 1.7× closer than the reference it is being asked to match.**

**Take the pitch. Do not take the distance.** −55° → −41° is the change that is unambiguously *toward* the reference and unambiguously *toward* what he asked for: a shallower camera shows more of the figure's front and less of its scalp, which reads as closer even at constant distance.

## A.4 ⚑ My model contradicts Matt's eye, so the MODEL is on trial — not his eye

Modelling apparent subject height as `h · (px/m) · cos(depression)`, ~1.8 m figure at 1080p:

| | reference `arena_full` | current S2 |
|---|---|---|
| px/m @1080 | `540/(58·tan20°)` = **25.58** | `540/(34·tan20°)` = **43.64** |
| foreshortening | `cos 41°` = **0.755** | `cos 55°` = **0.574** |
| figure height | **≈ 34.8 px** = **3.2%** of frame | **≈ 45.0 px** = **4.2%** of frame |

**By this model the S2 caster is already ~29% LARGER than the reference player.** That flatly contradicts what Matt sees. **One of my assumptions is wrong, and I am not relaying the model as a finding.** I shipped three untested mechanism claims earlier in this session and was refuted on all three, once by Matt himself — `#79` cl. 6 exists because of that. This is a hypothesis with its assumptions on the table.

**My leading hypothesis: the problem is COMPOSITION, not SCALE.** I pulled `harness_logs/s2c_rows12_2026-08-25/clip_bl_cathedral_03c-contact-far.png` at native 1920×1080. The caster and his skeletons occupy roughly a **360×280 px island**, and **well over half the frame is exterior rock and terrain with nothing in it.** The reference frame is *bounded* — a 36×36 m arena with walls, a minimap, a HUD, action centred. **A subject that is 4% of the frame reads "far away" when 60% of the frame is empty rock, and reads "correctly framed" when the rest of the frame is the room he is fighting in.** This also explains Matt's own earlier note that *"arena has a good wall height for the basic walls which we will want for the foreground"* — he was describing a framing property, not a set-dressing preference.

## A.5 What to do — settle it by measurement, not by my model and not by my eye

1. **Measure the actual apparent size on both sides.** Caster pixel-height as a fraction of frame height, in the reference MP4 and in a current cathedral clip. That is a direct measurement of the thing in dispute and it costs one crop each.
2. **If the measurement refutes § A.4, SAY SO PLAINLY** and treat the composition hypothesis as the live one. **If it refutes the composition hypothesis too, say that** — then the answer is neither of mine and I want to know that more than I want to be right.
3. **Apply the pitch change** (`CAM_PITCH := -55.0` → `-41.0`) regardless; it is toward the reference on every reading.
4. **Do not change `CAM_DIST` toward 58.** If measurement says the subject should be larger, move it **closer** than 34, not further. Report the number you chose and why.
5. **Re-cut the review MP4s** at the new framing, same `-g 15 -sc_threshold 0 -movflags +faststart` recipe, into `harness_logs/mp4_review_2026-08-25_v4/`.

## A.6 Out of scope for Task A

`--audience=measure` capture parameters (**the measurement corpus must not move** — every prior differential depends on it), the `bare` default, `vh_caster.gd:78`, `king_rig.gd` sword side (**Matt ruled: leave it**), and any forward-axis site (**sealed and Matt-verified — do not re-touch**).

---

# TASK B — render the clean-room whirlwind to MOTION, so the WW-AB comparison can actually happen

**Matt, verbatim, 2026-08-25:** *"let's prioritize the Whirlwind VFX generation with the WW AB test versus my prior HITL run. I think there is alot to be learned from that run."*

## B.1 The state of WW-AB, which is not what the wave record said

**The clean-room mint HAS run** — `drax/v0.1-s2-whirlwind-cleanroom-1` = `1692d6e`, 2026-08-24 18:52, 1,858 insertions across 12 `wwcr_*` files (your own work). **gandalf's DRIFT-CRITIC lineage audit returned LINEAGE CLEAN**: *"the datum is VALID… genuinely agent-built-from-spec against human-in-the-loop."* The wave record read `AUTHORED, un-run` for a day; I corrected it at `8033b487`.

**The comparison still cannot happen, and here is exactly why:**

| Arm | Object | Class |
|---|---|---|
| **HITL** (adopted SB-1 lineage) | `galadriel/captures/2026-08-16-sb1-gate2-clip/ww7-gate2-cadence-ab-plk0665-1920x1080.mp4` — 12,749,012 B, sha256 `7e9764e3fc53096128ef6b64d2a624962c1f3df599ae5e4aaf311347c0b828ca` | **MOTION** |
| **Clean-room** (`wwcr_*`) | `harness_logs/wwcr_2026-08-2*` — 10-pose PNG ladders | **STILLS ONLY** |

`find` for any `ww*.mp4` in this repo returns **zero**. **Only one arm has an object Matt's eye can judge, so the run's whole thesis is un-testable.**

⚑ **And the standard was written down nine days ago, about this exact comparison, then applied to one side.** The WW-7 v2 receipt (`.../2026-08-16-sb1-gate2-clip/receipt.txt`): *"GATE 2 (article FEEL — density, palette knee, cadence read, FX draw) is judged on **MOTION**, and a still cannot carry it."*

## B.2 What to render

**The clean-room build as it stands, under the HITL clip's camera and cadence grammar, so the ONLY variable between the two MP4s is the build.**

Camera, from `scripts/run_ww7_gate2_clip.sh`: **`--cam player_lock --plk 0.665`** — the gate-1-passed camera, a pure **dolly** (`--plk` scales the position offset vector and nothing else; rotation pitch `52.9535411256029` / yaw `47.0`, lens `fov_v 31.7861018306101` VERTICAL / KEEP_HEIGHT, and the anchor expectation `(0.501041450500488, 0.550925123426649)` frac are the ported values). **Note this is a DIFFERENT camera from Task A's** — Task A serves Matt's review clips; Task B serves a controlled A/B and must match its counterpart, not the review default. **Do not unify them.** The unscaled-offset pin fires first and must print `0.000000000000 m`; if it does not, HALT.

Match the counterpart on: shot id, tick window, cadence booleans, preroll, fps, encoder settings, seam, concat.

## B.3 ⚑ THE QUARANTINE — a conductor's ruling, because this is the exact edge it was written for

The clean-room quarantine bound you **during the mint**. The mint is complete, tagged, and lineage-audited. **A render cannot change a build.** So:

> **RULING: you MAY read the quarantined SB-1 clip machinery (`run_kc2_cpb_clip.sh`, `kc2_cpb_clip.gd`, the WW-7 runner, the `sb1-*` captures) FOR CAMERA AND CADENCE PARAMETERS ONLY. You MAY NOT modify any `wwcr_*` file, or any file the clean-room mint authored.**

**The line is: read anything, change nothing in the build.** The moment a `wwcr_*` file changes in this session, the artifact gandalf audited no longer exists and his LINEAGE CLEAN verdict describes something else — **the experiment would be destroyed by the act of preparing to run it.**

⚑ **If rendering genuinely requires a `wwcr_*` change — HALT AND ROUTE. Do not make it.** That includes changes that look purely mechanical (a camera hook, an export path, a signature). Route to me and to gandalf; he is the audit's author and only he can rule whether a given change voids it. **This is the one instruction in this dispatch I would rather you over-obey than under-obey.**

## B.4 Disk — Discipline #1.1, mandatory, and I am the reason it says so

**Measured now: `/System/Volumes/Data` — 60 GiB free, 87% used.** It sat at **2.7 GiB (0.6%)** earlier today and **halted your tranche-3A mid-capture**; Matt spent an afternoon freeing 64 GB. **I ran the pre-fire projection only *after* that failure.**

**Project frames × resolution × bytes-per-frame against `df -h`, write it down, and do not fire if it does not fit with margin.** Your own `SUFFIX` fix took the harness from 4 × 4.2 GB to 2 × 4.2 GB per row — hold that property.

## B.5 And the lesson you paid for, restated so it is not lost

**`bash` reads a running script lazily, by byte offset.** You edited a runner 90 seconds into a detached run of it. **Detachment alone is not enough** — and a detached run is *precisely* the one you are most likely to edit, because it is not holding your terminal. **Launch from a frozen copy.** I dispatched half that remedy last time; here is the other half, in writing.

---

## Acceptance criteria

1. **Task A** — apparent-size measured on both sides and reported as a number; pitch applied; a stated, reasoned decision on distance; `mp4_review_2026-08-25_v4/` cut and ffprobe-gated
2. **Task A** — an explicit verdict on § A.4: does the measurement support my model, the composition hypothesis, or neither
3. **Task B** — a clean-room whirlwind MP4 at 1920×1080 under `--cam player_lock --plk 0.665`, matching `ww7-gate2-cadence-ab-plk0665` on every listed parameter, with the differences that could not be matched **named**
4. **Task B** — a receipt asserting **zero `wwcr_*` bytes changed** (`git status` + `git diff --stat` against `1692d6e` over those paths). This is the receipt that keeps the experiment alive; it is worth more than the render.
5. Pre-fire disk projection recorded **before** any capture
6. Both MP4 paths handed over explicitly — they are gitignored under the Synty licence, so the path IS the deliverable

## Quality criterion

**Game-quality goal:** WW-AB is the wave's **calibration datum for every other row's expected quality** — its own dispatch says so. Matt's read that the VFX are *"basic representations… lacking ALOT of the depth of the originals"* is currently unanswerable, because the one comparison built to answer it has never been rendered in the medium the question lives in. **Twelve more rows are queued to mint against a standard nobody has yet been able to look at.**

**Refutation conditions** (surface if any apply):
- The clean-room build cannot render under `player_lock/--plk 0.665` without a `wwcr_*` change → **HALT and route** (§ B.3); do not work around it
- The two arms cannot be matched on some parameter that materially affects the read → name it; a comparison with an unnamed second variable is not a comparison
- Task A's measurement refutes both of my hypotheses → say so; that is a better outcome than confirming either
- The pitch change moves any *measurement-corpus* capture → it must not; review and measure audiences are separate by construction (`--audience`)
- Either task requires touching a forward-axis site → **HALT**; that landing is sealed and Matt-verified
- Acceptance criteria can pass while Matt still cannot tell the two whirlwind arms apart — in which case say so plainly, because that result *is* the datum
