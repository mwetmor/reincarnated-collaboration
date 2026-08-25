# Dispatch — 2026-08-25 — drax — forward-axis fix + cathedral-as-default + re-capture

**Status:** DONE (drax, 2026-08-25) — see § Completion record
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


---

# Completion record — drax, 2026-08-25

**Commits (all pushed, `reincarnated-godot` main at `689116c`):**
`612c1e3` Commit A (the fix) · `1c4f90f` Commit B (`face_toward()`, byte-verified) ·
`689116c` Commit C (review path + reference wiring)

**Deliverable:** `/Users/admin/Games/reincarnated-godot/harness_logs/mp4_review_2026-08-25_v3/`
— 7 MP4s, cathedral, gitignored under the Synty licence so the absolute path is the handover.

## ⚑ REFUTATION CONDITION 1 FIRED. Two of the five ordered sites were not defects.

Matt is right and jack-ryan's root cause is right — every rig fronts on local **+Z**. But the
180° error is **not uniform across rows**:

1. **`s2a_stage.gd:303` (the MOB yaw) was already correct and was NOT changed.**
   `atan2(-p.x, -p.z)` looks like the -Z formula and is not — it aligns local +Z with the
   direction *from p toward the origin*, so on a +Z-fronted body it points the mob **at** the
   caster. `scripts/s2_forward_axis_probe.gd` (new, Commit A) evaluates it at six bearings
   including one BEHIND the caster: **AT CASTER (dot = +1.000) at every one**; the flip reads
   AWAY at every one. Flipping it would have turned every staged body around.
2. **`melee` / `meleearc` / `aura` must NOT be rotated**, though Gate-1 scoped `melee` in.
   ⚑ **The repo holds TWO independent facts, not one: the RIG's forward axis, and THE FRAME
   EACH ROW AUTHORS ITS PAYLOAD IN.** Those rows author in the *rig's own frame*
   (`_rig.global_transform.basis * Vector3(sin b, 0, cos b)` — bearing 0 IS local +Z) and
   stage their bodies on +Z bearings to match. **Receipt: a full 79-frame `clip_ms_cathedral`
   arm re-rendered post-fix is byte-identical to the sealed pre-fix capture, 79/79**, with
   `hits_fired=3 / hits_off_body=0 / hit_body_err_max_m=0.0` unmoved.

So the ruled rule generalizes: *the right formula is a function of the RIG* — **and of the
ROW** — *and nothing at a call site tells you either.* Commit A therefore fixes the four
movers plus the caster's **rest yaw, which was never set at all** (`_caster_rest_yaw()`, a
per-row table). "Never set" is not neutral: it asserts yaw 0, i.e. the caster fronts on world
+Z while every world-framed row authors its payload along world -Z.

## Acceptance criteria

| # | Criterion | Result |
|---|---|---|
| 1 | Caster faces travel on all six rows, confirmed against a render | **MET.** Emitted yaw -3.14159 on dash/blink/teleport/leap/slam, -2.531 (= -145°, exactly aim 35) on the off-default arm, 0.0 on melee. Visual plates at 5x show cape-and-back on the five turned rows and the King's FRONT on melee, strokes toward his own staged bodies. |
| 2 | Commit B introduced; re-render byte-identical | **MET, and stronger than one comparison.** 472-frame pass at Commit A vs Commit B2: **472/472 byte-identical.** |
| 3 | Measurement keeps `bare`; review defaults `cathedral` | **MET.** `--audience=review\|measure`; global default untouched; explicit `--stage=` wins in either argument order (six-case table verified). |
| 4 | Six re-cut MP4s at an absolute path, dense keyframes + faststart | **MET (7 delivered).** 15-28 keyframes/file, faststart, ffprobe-gated promotion. |
| 5 | Reference URLs at each archetype definition site | **MET.** 18 files wired; the repo-wide `grep -rIn "youtube\|dossier"` goes from **1 hit** (a third-party addon's comment) to **51**. |
| 6 | Foreground wall-height note parked, not actioned | **MET.** `reincarnated-godot/AGENT_STATE.md`. |

## Refutation conditions

- **1 — the 180° error is not uniform: ⚑ FIRED.** Above. The dispatch was aimed at five sites;
  three were defects.
- **2 — Commit B cannot be made byte-identical: did not fire.** 472/472.
- **3 — the audience split requires touching the measurement path: did not fire.** Every
  measurement runner passes `--stage=` explicitly on every arm, so the flag cannot move them.
- **4 — the black-frame report reproduces against v2: NOT REPRODUCIBLE BY ME; OPEN ON MATT'S
  EYE.** KR's keyframe diagnosis is structurally confirmed (v1 = **6** keyframes / 366 frames,
  v2 = 25). On v3 I ran `blackdetect` (0 black runs on all 7) **and a cold-keyframe-seek scrub
  test at 12 timestamps per file** — the actual failure mode — with minimum decoded luma
  35.6-37.5 everywhere. If Matt still sees black on v3, the cause is upstream of the encode and
  I want to know rather than work around it.
- **5 — reference wiring needs a schema change: did not fire.** Comments only.

## Two findings surfaced, neither repaired

- **F-9 — the determinism receipt has counterexamples, and md5 is a knife-edge here.**
  `clip_tp_cathedral_f0032` differs between two runs of **identical code**; three further
  re-runs reproduced the other value. `clip_tp_cathedral_f0030` differs across identical-code
  runs by **exactly one pixel at maxdiff 2/255**. The sealed two-pass receipts (874/874,
  2106/2106) are not wrong — those two passes agreed — but **a single differing frame in an A/B
  comparison is not evidence of a behaviour change**, and I was one step from reporting one as
  if it were. The A/B differing frame measured 18 px at maxdiff 10, against the fix's own
  11,813 px at maxdiff 251 on that same frame. **Any future byte-identity claim on this corpus
  needs a same-code repeat to establish the flake set first.** Owners: drax, jack-ryan.
- **F-10 — `project.godot` carries an uncommitted rendering-setting deletion.** The working
  tree has dropped `[rendering] mesh_lod/lod_change/threshold_pixels=1.0` (committed at
  `aa8b0ae`). Mtime **12:09 on 2026-08-25, i.e. BEFORE the 14:12 sealed tranche-3A captures** —
  so the sealed corpus and everything captured today ran without it, consistently.
  **Deliberately not touched**: restoring it mid-dispatch would change pixels and break
  comparability with the sealed corpus. Owner: knight-rider (scope) — it wants a decision.

## Narrowing of the Gate-1 ruling, made on evidence

jack-ryan asked Commit B to adopt the helper at the already-correct **player-facing** sites,
receipted by byte-identical re-render. **Those sites cannot carry that receipt**:
`render_arena_room.gd` (9 GPUParticles3D refs), `render_boss_arena.gd` (10),
`render_descent_scene.gd` (40 refs + 63 `rand()` call sites) are non-byte-reproducible by
construction, and `playshell.gd` is the interactive played surface with no deterministic
capture at all. **The S2 harness is the only byte-reproducible surface in this repo** —
deliberately, because it was built that way. So those five files get a pointer comment naming
the convention and no code change: the convention reaches every yaw site, only the receiptable
ones were rewired. Routing back to jack-ryan for ratification or correction.

## Out of scope, honoured

`vh_caster.gd:78` MODEL_FORWARD_YAW (body-corrected rig; flipping re-opens WR1) ·
`king_rig.gd` sword side (Matt: leave it) · `s2c_cone:339`, `s2b_melee_arc:359/450`,
`s2b_line:425`, all camera/shader azimuths and sim-heading conversions (not rig yaws).

---

## ✅ MATT'S VERDICT — 2026-08-25, on the v3 deliverable. ACCEPTANCE CRITERION 1 DISCHARGED BY THE ONLY INSTRUMENT THAT COULD DISCHARGE IT.

**Matt, verbatim:** *"I confirmed that the _v3 mp4s from drax now have the character facing the correct way (forwards)."*

**Recorded here, immediately, because a verdict that lives only in a conversation is not a verdict the wave has** — the § conflict-rule corollary in `CLAUDE.md`, and the fourth instance in this wave of *the work is right and the record does not carry it*. The conductor owns this file and had no excuse for a fifth.

**What this closes, precisely.** The defect was **player-visible and eye-adjudicable**, so Matt's eye is the instrument of record — not `blackdetect`, not md5, not a byte-identity receipt. Those verified that *nothing else moved*; only Matt could verify that *the intended thing moved*. Both halves were required and both are now in.

⚑ **The finding that outranks the fix, and it is drax's not mine.** The four movers the dispatch named were real, but the defect Matt has been seeing since the first render was upstream of all four: **the caster's rest yaw was never set at all.** *Never set* is not neutral — it asserts yaw 0, so the caster fronted world **+Z** while every world-framed row authors its payload along world **−Z**. **He had his back to his own effect from frame 0, at rest, on every row, including rows with no aim at all.** No amount of fixing the aim formulae would have touched it. It was found by probing rather than by reading the dispatch's list, which is the only way it could have been found.

**What does NOT close with this verdict — carried forward, not lost in the acceptance:**

1. ⚑ **THE CAMERA FRAMING WAS NEVER DONE, AND THAT IS THE CONDUCTOR'S FAILURE, NOT THE BUILDER'S.** Matt asked for the zoom to match the ice-golem reference. I authored that as a **Task-5 addendum after drax had already read this file** (`7d344a9b`), with `SendMessage` unavailable for the fifth confirmed time this session. He never saw it. Verified against the tree rather than inferred: `s2a_stage.gd` still reads `CAM_PITCH := -55.0` / `CAM_DIST := 34.0`, and his completion record's only occurrence of the word "camera" is in the out-of-scope list. **A dispatch amended mid-flight is not a dispatch amended.** Re-issued as its own file.
2. **F-9 — the determinism receipt has counterexamples.** `clip_tp_cathedral_f0030` differs across runs of *identical code* by one pixel at maxdiff 2/255. So **md5 inequality on a single frame is not evidence of a behaviour change on this corpus.** This constrains every byte-identity seal already taken in this wave and is routed to jack-ryan, not resolved here.
3. **F-10 — `project.godot` carries an uncommitted deletion** of `[rendering] mesh_lod/lod_change/threshold_pixels=1.0`, verified live in `git diff`. mtime 12:09, i.e. **before** the 14:12 sealed captures, so those captures were taken under the deleted setting. drax deliberately left it dirty rather than break comparability mid-dispatch — the right call. Still open; wants a ruling.
4. **The Gate-1 narrowing** (the five player-facing sites cannot carry a byte-identity receipt because they are non-deterministic by construction) is routed to jack-ryan and unanswered.

⚑ **And the part that should survive longest: refutation condition 1 FIRED, and it fired against ME.** This dispatch ordered five sites fixed. **Two were not defects, and one of those would have broken the build.** `s2a_stage.gd:303`'s `atan2(-p.x, -p.z)` *looks* like the −Z formula and is not — it aligns local +Z toward the origin, so on a +Z-fronted rig it points every staged mob **at** the caster, correctly. drax measured it at six bearings including one behind the caster (dot = +1.000, every one) and **refused the ordered edit**. Flipping it would have turned every staged body around, in a commit whose stated purpose was fixing facing.

**The reusable lesson is not "check your dispatches."** It is that the repo holds **two independent facts** where I assumed one: the rig's forward axis, *and the frame each row authors its payload in*. `melee` / `melee_arc` / `aura` author about the caster's own bearing-0 and stage their bodies to match; they must not be rotated, though Gate-1 scoped `melee` in. Receipt: 79/79 byte-identical to the sealed pre-fix capture. **jack-ryan's own ruling — *"the right formula is a function of the RIG, not of the repo"* — was one axis short. It is a function of the rig AND the authoring frame.**
