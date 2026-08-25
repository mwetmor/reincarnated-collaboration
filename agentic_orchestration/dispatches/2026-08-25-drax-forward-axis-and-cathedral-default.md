# Dispatch — 2026-08-25 — drax — forward-axis fix + cathedral-as-default + re-capture

**Status:** PENDING
**From:** knight-rider (Step-2 VFX build wave, conductor)
**To:** drax (presentation seam — `reincarnated-godot/`)
**Pattern:** B (multi-step; capture passes are ~25 min each)
**Source:** Matt review of `harness_logs/mp4_review_2026-08-25/` — *"the character is still backwards in all of the MP4's"*; jack-ryan Gate-1 ruling `agentic_orchestration/qa/findings/2026-08-25-godot-forward-axis-convention.md`
**Push:** authorized for this session, all repos including `reincarnated-godot` (Matt, verbatim *"push as you go through this session"*)

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
