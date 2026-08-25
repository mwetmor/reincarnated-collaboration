# Dispatch — 2026-08-25 — drax — forward-axis fix + cathedral-as-default + re-capture

**Status:** PENDING
**From:** knight-rider (Step-2 VFX build wave, conductor)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Pattern:** B (multi-step; capture passes are ~25 min each)
**Source:** Matt review of `harness_logs/mp4_review_2026-08-25/` — *"the character is still backwards in all of the MP4's"*; jack-ryan Gate-1 ruling `agentic_orchestration/qa/findings/2026-08-25-godot-forward-axis-convention.md`
**Push:** authorized for this session, all repos including `reincarnated-godot` (Matt, verbatim *"push as you go through this session"*)

---

# ⚑⚑ ADDENDUM — TASK 5, ADDED MID-FLIGHT. CAMERA FRAMING. READ THIS BEFORE YOU RE-CAPTURE.

**Matt, verbatim:** *"dash attack is fixed. Also, the zoom is too far out. please have it match our most
recent completed godot rendering of camera angle/zoom from this mp4:
`/Users/admin/Desktop/level-18-ice-golem-simulation.mp4`"*

**Item 2 of the prior round is CLOSED** — the black dash-attack MP4 was the `-c copy` single-keyframe
encode; the dense-keyframe re-encode fixed it. Keep the `-g 15 -sc_threshold 0 -movflags +faststart`
recipe. My keyframe diagnosis held.

## What the reference actually is — identified, not assumed

`/Users/admin/Desktop/level-18-ice-golem-simulation.mp4` · 1600×900 · 30 fps · 40.4 s · 2026-08-02.

The only source in this repo matching it is `scripts/wr2_playback.gd` (the WR2/BR-2 watch). Its runner
`scripts/run_wr2_playback.sh:25` documents the invocation for that pick by seed:

```
CAM=arena_full FRAMES=1120 bash scripts/run_wr2_playback.sh wr3_acc acc boss FULL 74000909
```

Seed `74000909` is on the frame in the HUD panel (`SIM · seed 74000909`) — I cropped it at native
resolution and read it rather than inferring from the filename. **So the reference camera is
`--cam arena_full`, NOT `player_lock`.** I checked because `player_lock` is the one the source calls
"THE GAME CAMERA" and assuming it would have been the natural error.

## The two cameras, side by side, from the constants

| | reference — `arena_full` (`wr2_playback.gd`) | current — S2C (`s2a_stage.gd:65-69`) |
|---|---|---|
| yaw | **47.0°** (`CAM_YAW_DEG:1669`) | **47.0°** (`CAM_YAW`) — ✅ already identical |
| fov (vertical) | **40.0°** (`CAM_FOV:1671`) | **40.0°** (`CAM_FOV`) — ✅ already identical |
| pitch | **−41.0°** (`CAM_PITCH_DEG:1670`) | **−55.0°** (`CAM_PITCH`) — ⚑ **14° steeper** |
| distance | **58.0 m** (`CAM_DIST_FULL:1710`) | **34.0 m** (`CAM_DIST`) — ⚑ **24 m closer** |
| aim | datum + `(7, 1, 7)` NE bias (`CAM_AIM_NE_FULL:1717`) | focus + `(0, 1.2, 0)` |
| px/m @720p | **17.05** (their own published figure, `:231`) | **29.09** (`360/(34·tan20°)`) |

## ⚑ THE TRAP — DO NOT COPY `CAM_DIST_FULL`. IT WOULD MOVE THE CAMERA FURTHER OUT.

Matt asked for **less** zoom-out. Matching the reference literally means **34 m → 58 m** and world
scale **29.09 → 17.05 px/m, a 41% reduction.** The instruction as written, executed literally,
delivers the opposite of the instruction's intent. **The S2C camera is already 1.7× closer than the
reference.**

## ⚑ And my model contradicts Matt's eye — so the model is the thing on trial, not his eye

Modelling apparent subject height as `h · (px/m) · cos(depression)`, for a ~1.8 m figure at 1080p:

| | reference `arena_full` | current S2C |
|---|---|---|
| px/m @1080 | 540/(58·tan20°) = **25.58** | 540/(34·tan20°) = **43.64** |
| foreshortening | cos 41° = **0.755** | cos 55° = **0.574** |
| figure height | **≈ 34.8 px** = **3.2%** of frame | **≈ 45.0 px** = **4.2%** of frame |

**By this model the S2C caster is already ~29% LARGER than the reference player.** That flatly
contradicts what Matt sees, so **one of my assumptions is wrong and I am not going to relay the model
as a finding.** I have shipped three untested mechanism claims in this session and been refuted on all
three; this one is declared as a hypothesis with its assumptions on the table.

**My leading hypothesis is that the problem is COMPOSITION, not SCALE.** I pulled
`harness_logs/s2c_rows12_2026-08-25/clip_bl_cathedral_03c-contact-far.png` at native 1920×1080: the
caster and his skeletons occupy roughly a **360×280 px island**, and **well over half the frame is
exterior rock and terrain with nothing in it.** The reference frame is bounded — a 36×36 m arena with
walls, a minimap and a HUD, action centred — so the same subject size reads completely differently.
A subject that is 4% of the frame reads "far away" when 60% of the frame is empty rock, and reads
"correctly framed" when the rest of the frame is the room he is fighting in.

## What to actually do — and settle it by measurement, not by my model or my eye

1. **Take the pitch. `−55° → −41°`.** This one is unambiguous, it is what Matt means by "camera
   angle," and it is the change that most restores the body silhouette — at −55° you are looking at
   the top of the caster's head.
2. **Do NOT take the distance.** Hold 34 m, or come closer. Justify whatever you pick with a measured
   number, not a preference.
3. **Fix the framing.** Aim so the subject and the cathedral geometry fill the frame the way the
   reference's arena does. The NE-diagonal aim bias exists in the reference for exactly this reason
   and its value was *swept against `_audit_framing()`*, not chosen by eye — do the same here.
4. ⚑ **MEASURE, and let the measurement rule.** Render one frame per candidate pose and measure the
   **caster's pixel height as a fraction of frame height**, against the same measurement taken on the
   reference MP4. That is the number Matt is reacting to, and it is the cheapest test that can refute
   my composition hypothesis. **If the measured fractions come out roughly equal, my hypothesis is
   right and the fix is framing. If the S2C fraction is genuinely smaller, my model is wrong — say so
   plainly and fix the scale.**
5. Port whichever pose wins into the **review** capture path only. **The measurement path's camera is
   not in scope** — changing it would invalidate every prior differential the same way changing the
   `bare` default would.

**Refutation conditions specific to this task:**
- The reference MP4 was not rendered with `arena_full` after all (my identification rests on the
  runner's documented invocation plus the on-frame seed — if you find a different run record, yours wins)
- Matching pitch −41° pushes the caster or the effect out of frame, which `_audit_framing()` would catch
- The cathedral recipe's camera is not `s2a_stage.gd`'s at all for the review path
- The measured caster-height fractions come out equal, proving the complaint is composition — in which
  case **say so to Matt explicitly**, because he will otherwise reasonably expect a zoom change

---

## Required reading before you touch anything

1. `agentic_orchestration/qa/findings/2026-08-25-godot-forward-axis-convention.md` — jack-ryan's adjudication
2. `agentic_orchestration/galadriel/findings/2026-08-25-dash-attack-facing.md` — the measurement
3. `agentic_orchestration/galadriel/notes/2026-08-24-vfx-p3-selection-gate.md` § 3 — the reference table (see task 4)
4. `scripts/s2_stage_env.gd` — the stage-recipe contract you authored

---

## Task 1 — the forward-axis fix. TWO COMMITS, and the isolation is the whole point.

**The defect:** `s2a_stage.gd:303` computes yaw as `atan2(-x, -z)`. Every shipped rig in this repo
faces local **+Z**. The caster is therefore rotated 180° from travel **on every row, including at
rest** — it is not a dash-specific bug, it only reads worst on dash.

⚑ **The rule jack-ryan ruled, and it is the docstring of the helper you are about to write:**

> **The right formula is a function of the RIG, not of the repo — and nothing at a call site tells you which.**

**COMMIT A — the fix.** `s2a_stage.gd:303` plus the four `s2c_*` movers. Correct the yaw convention
to +Z-forward.

**COMMIT B — the helper.** Introduce `face_toward()` and route the *already-correct* sites through it.
**Commit B must be verified byte-identical on re-render** — that is what makes it a refactor and not a
second change. If any frame differs, B is not a refactor; HALT and route.

### Out of scope — explicitly, and each for a stated reason

- **`vh_caster.gd:78` — `MODEL_FORWARD_YAW := 180.0`.** That rig family faces `-Z` **deliberately**.
  It is not a defect. Flipping it re-opens WR1.
- **`king_rig.gd` sword side.** Retired unfired by Matt (`2026-08-25-drax-king-rig-sword-side.md`).
  The residual ~24° blade-aim error is recorded there and Matt ruled *leave it*.
- **`s2c_cone:339`, `s2b_melee_arc:359/450`, camera/shader azimuths, sim-heading conversions.**
  Not rig yaws. Do not sweep them.

---

## Task 2 — cathedral becomes the default presentation stage. Matt ruled it.

**Matt, verbatim:** *"The cathedral scene is perfect for what we are doing."* and
*"_CATHEDRAL mp4 files have amazing scenery (not arena)."*

`s2a_stage.gd:115` currently defaults E-0 to `bare`, with `cathedral` opt-in. That default was
correct for measurement — a constant background makes effect-vs-control isolation exact — and it is
now wrong for anything Matt reviews.

**Do NOT globally flip the default.** Split the two audiences instead:

- **Measurement captures keep `bare`.** Differential isolation is why `bare` exists; the C-3 albedo
  0.085 anchor is measured on it. Changing this silently invalidates every prior differential.
- **Review/demo captures default to `cathedral`.** Add an explicit review-capture path or flag so a
  human-facing cut lands on cathedral geometry without a per-run argument.

⚑ **Matt's second observation, which is a real design note and not a passing remark:**
*"arena has a good wall height for the basic walls which we will want for the foreground."*
**He explicitly deferred it** — *"Let's not worry about this for now."* Record it in `AGENT_STATE.md`
as a parked foreground-composition note. Do not action it in this dispatch.

---

## Task 3 — re-capture, then re-cut the review MP4s

All twelve current MP4s are **pre-fix** and show the backwards caster. After Commit A lands:

1. Re-capture the six skill rows
2. Re-cut MP4s to `harness_logs/mp4_review_<date>_v3/`
3. ⚑ **Encode with `-g 15 -sc_threshold 0 -movflags +faststart`.** The prior cut used
   `-stream_loop N -c copy`, which yields **one keyframe per loop iteration** (6 keyframes in 366
   frames). Matt reported the dash-attack arena file rendering black; `blackdetect` found **zero
   black runs** and frame-0 luma was within 0.5/255 of its neighbours, so the file content is not
   black — but a single-keyframe segment is a known black-on-scrub trigger in QuickTime. The dense-
   keyframe re-encode is at `mp4_review_2026-08-25_v2/` as the working recipe.
4. **`harness_logs/**/*.mp4` is gitignored** under the Synty licence. A deliverable that exists only
   in a gitignored directory is not delivered — give Matt the absolute path explicitly.

---

## Task 4 — wire the reference corpus into the build seam

⚑ **`grep -rIn "youtube\|dossier"` across all of `reincarnated-godot` returns exactly one hit** — a
third-party shader addon's own comment. **Nothing in the build seam points at the references the
minted effects are scored against.**

galadriel's P3 selection gate names a canonical + runner-up per archetype with R/P/S scores. Add the
canonical URL as a comment or metadata field at each `s2c_*` archetype's definition site so a future
reader can reach the reference from the code. Cheap, and it closes the loop.

**Two flags from that table that bear on rows you have already built:**
- **`teleport` R=3** — *"restrained arrival flash"* sits near your § 7.5 0.03% coverage floor. If the
  arrival burst is invisible at our camera, that is the predicted failure, not a new one.
- **`dash_attack`** was selected because contact response is *distributed along the path*, not merely
  terminal. Worth checking your mint against that specifically.

---

## Acceptance criteria

1. Commit A: caster faces travel direction on all six rows, confirmed against a render
2. Commit B: `face_toward()` introduced; re-render **byte-identical** at already-correct sites
3. Measurement captures still default `bare`; review captures default `cathedral`
4. Six re-cut MP4s at an absolute path given to Matt, encoded with dense keyframes + faststart
5. Reference URLs present at each archetype definition site
6. Foreground wall-height note parked in `AGENT_STATE.md`, not actioned

## Sequencing and safety

⚑ **`bash` reads a running script lazily, by byte offset.** You proved this the hard way earlier
today — a runner edited 90 seconds into a detached run. **Detachment alone is not enough, and a
detached run is precisely the one you are most likely to edit.** Launch every capture from a
**frozen copy** of the runner.

⚑ **Pre-fire resource projection (Discipline #1.1) is mandatory.** Host is at 66 GiB free after
Matt's reclaim; a pass is ~4.2 GB. Project before you fire, not after.

⚑ **`#80` cl. 5(b) ordering trap.** `s2b_e1_gate.py:324` builds
`vals = [v for k, v in det.items() if k != "note"]` — a **complement of exceptions**, so it silently
adopts any key added later. If you add numeric siblings, they get recruited into `vals` and
`all(v == 0 ...)` flips PASS to false on genuinely passing rows. **If you go red after such an edit,
that is the trap — do not revert the receipt.**

## Quality criterion

**Game-quality goal this dispatch serves:** the caster is the player's own body. A body that faces
backwards while moving forwards is the single most legible "this is broken" signal a viewer can
receive, and it invalidates every silhouette and readability judgement made about these six
archetypes. Matt has now seen it in twelve consecutive files.

**Refutation conditions** (surface if any apply):
- The 180° error is not uniform across rows — some rows are correct — which would mean the cause is
  not `s2a_stage:303` and this dispatch is aimed wrong
- Commit B cannot be made byte-identical, meaning `face_toward()` is a behaviour change not a refactor
- Splitting the stage default by audience requires touching the measurement path, which would put
  prior differential results at risk
- The dash-attack black-frame report reproduces against `mp4_review_2026-08-25_v2/`, meaning my
  keyframe diagnosis is wrong and the cause is upstream in the capture
- The reference-URL wiring would require a schema change rather than a comment
