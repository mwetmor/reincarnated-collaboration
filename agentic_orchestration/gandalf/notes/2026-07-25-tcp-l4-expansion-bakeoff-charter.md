# TCP-L4 — T2 EXPANSION, THREE-WAY BAKE-OFF (run charter)

**Program:** `2026-07-24-tool-capability-program-charter.md` — lap **L4**, class **T2 EXPANSION** × mode **(i) held-constant spec**
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executors:** drax ×3, sequential · **Status:** CHARTERED 2026-07-25
**Matt gate:** none. Q45/Q46 do not block (Q46 is a standing-exposure question, mitigated in-lap by the env block).

---

## §0 — Intent, in one sentence

**Given the same existing scene and the same frozen expansion spec, which of W-PRO, W-MUR and H
produces the addition — without breaking what was already there — and how many author→look→fix cycles
does each one need?**

**Rubric diff against §0 (law L-I).** What falls out: this lap says nothing about *design* quality
(mode (i) freezes the spec), nothing about new-scene authoring (that is L6), nothing about UI or VFX.
It answers **execution fidelity + non-destruction + iteration count** on an expansion task. Do not let
a win here be read as "best tool overall."

**Why this lap is running at all.** The conductor proposed cancelling it on the grounds that the
outcome was predictable. **Matt overruled, and was right to:** the program's founding discipline is
that predictions are pre-registered and then *measured*, and the conductor's prediction record in this
program is five wrong generalizations. **A confident forecast is not a substitute for a lap.** That is
the charter's first sentence for a reason.

## §1 — Why expansion is a different test from replica

Replica (L1/L2) tests: can you build a thing from constants. **Expansion tests something replica
structurally cannot — can you add to a scene you did not author without damaging it.**

L2 found that **a Pro-authored scene does not round-trip through Pro**: `add_scene_instance` calls
`set_owner_recursive`, so internal nodes save owned *and* re-instance on reload, colliding and
renaming. Expansion **requires** loading a scene the instrument did not write. Whether that failure
generalizes to foreign scenes is **untested and is the sharpest question in this lap.**

## §2 — The substrate: one scene-before, one frozen spec, three outputs

**Everything happens in the lab .NET project** (`~/Games/mcp-lab/project/`). It can host all three:
Murzak is a C# addon, Pro is a GDScript addon, H needs neither. `reincarnated-godot` is **not touched**
(TCP-17/18 stand; blast-radius verification per **TCP-20** — file-count + fingerprint of the ignored
tree, because `git status` is structurally blind there).

**`scene_before.tscn`** — the L2 room (17.5 m, 4th pack), rebuilt by the established H pipeline and
**frozen before any instrument runs.** Hash it. Every instrument starts from a pristine copy at its own
output path and **never writes to the frozen original.**

**THE EXPANSION SPEC — identical for all three, held constant (mode (i)):**

A raised dais against the **far (−Z)** wall of the existing room.

1. **Platform** — 6.0 m (X) × 4.0 m (Z) × 0.6 m high, centred on X=0, back edge flush to the existing
   far wall's inner face.
2. **Flanking stairs** — one at each of the dais's +X and −X ends, 4 steps, each 0.15 m rise × 0.40 m
   run, 1.2 m wide, ascending toward −Z.
3. **Two pillars** from the pack, standing **on** the dais, one at each front (+Z) corner, inset 0.5 m
   from each edge.
4. **Two dressing props** from the pack at the dais front edge, symmetric about X=0. Declare which
   props and verify **measured texture presence**, not merely a valid material slot (TCP-16).
5. **NON-DESTRUCTION** — the existing floor, walls, dressing and lighting are **unmodified**: nothing
   moved, deleted, renamed or re-parented. This is a spec clause, not a courtesy.
6. **Camera** — the `__box` standing framing (TCP-12), identical parameters for every cell.

**Kit constants are HANDED TO ALL THREE, deliberately.** We already know Pro cannot derive them (L2
P-B, decisive). Re-testing that here would burn a lap re-answering a settled question and would
confound the thing we *are* measuring. Publish the measured wall/floor/pillar/prop dimensions in the
brief so every instrument builds from the same numbers. **What is being measured is the expansion act,
not the measurement act.**

## §3 — Pre-registered predictions (pinned before results)

- **P-1 — all three produce the dais geometry.** *High confidence.* A FAIL here is a large finding.
- **P-2 — DECISIVE. Non-destruction.** Pixel diff of the region **outside** the addition against
  `scene_before`'s frame must be ~zero for a passing method. **Prediction: W-PRO FAILS** on the L2
  `set_owner_recursive` mechanism, now applied to a foreign scene. **If Pro passes, that is the single
  most interesting result of the lap** and it reverses a standing program belief.
- **P-3 — W-MUR routes through W→H** (authors a builder script via `script-create`) rather than
  placing nodes one at a time, because that is what its 39 tools are shaped like. **If it instead goes
  node-by-node, record that** — it means the W→H path needs deliberate prompting rather than being the
  natural groove.
- **P-4 — H wins wall-clock, but by a NARROWER margin than L2's** — expansion requires *reading* the
  existing scene, which the wire does natively and a script must be told to do.
- **P-5 — ITERATION COUNT, and no lap has ever measured this.** Count author→look→fix cycles to land
  the spec, per instrument. **This is the real axis of "best at building" and the program has been
  proxying it with wall-clock.** Report the count, and what each cycle was spent fixing.

- **P-6 — THE SAVE-DUPLICATION HAZARD ON ADDED GEOMETRY.** *Added 2026-07-25 after L4-PREP, before
  any instrument ran — legitimate preregistration: no results exist.* **TCP-24** found that Godot's
  `PackedScene.pack()` duplicates instanced FBX sub-scenes on save (808 nodes in → **1320 out**), and
  that **no route gives both correct node count and surviving materials** (own-all → duplicates;
  own-root-only → every material silently dropped). PREP flattened that confound out of the
  *substrate*. **It is NOT removed from the addition** — pillars and props are FBX, so any instrument
  that instances them and saves duplicates them. **The question this makes measurable: can the
  instrument place geometry WITHOUT going through scene-instancing?** *Forecast (and per TCP-22 a
  forecast is measured, not obeyed): at least one instrument ships duplicated pillars and does not
  notice, because every call returned `ok` — L-K, sixth instance.* **No known-good route is being
  handed over.** Each instrument finds a non-lossy path or **names its ceiling, and a named ceiling
  is a PASS (L-G).** Every cell reports node-count-in vs node-count-out across a save/reload.

**Every prediction resolves to a recorded fact. A FAIL is a finding (L-G).** **Report medians with n
and exclusions for any timing claim (TCP-19)** — a mean containing retry timeouts is not a measurement.

## §3b — AMENDMENT at dispatch: L4-PREP, and the two charter defects that forced it

**Amended 2026-07-25 by the conductor, before any instrument ran.** Reviewing §2/§5 for dispatch I
found two defects in my own charter. Both are recorded here rather than quietly fixed, because the
program's value is in its error trail.

1. **§2 had the first instrument build `scene_before`. That confounds P-3.** P-3 asks whether Murzak
   *naturally* routes through W→H. An operator who has just hand-written a GDScript room builder will
   reach for W→H reflexively — the measurement would be reading the operator's fresh habit, not the
   tool's groove. **The substrate must be built by a party that then runs no instrument.**
2. **§5 had the diff instrument judging before anyone calibrated it.** P-2 is the decisive prediction
   and it resolves through a masked pixel diff — an instrument nobody had shown to work. **That is
   textbook L-K wearing our own uniform:** `custom_aabb` returned a field shaped exactly like the
   answer, identically zero, `ok=true`. A differ that silently returns a plausible number is the same
   trap. **Two-point calibration is now mandatory: self-diff must be EXACTLY zero, and a diff against
   a deliberately-nudged copy must be non-zero with the bright pixels on the nudged node.** An
   instrument not shown to detect a change it was handed is not evidence about a change it was not.

**L4-PREP therefore runs first, as a control, and runs no instrument.** It copies + imports
`polygon-dark-fortress`, builds and **freezes** `scene_before.tscn` (SHA-256 published), **relocates
its builder out of the project directory** (L1 §4c contamination guard — a worked room-builder on
disk lets a wire agent read the method instead of solving the task), pins the two dais props with
**measured texture presence** (TCP-16) so a held-constant spec does not resolve three different ways,
renders the `__box` reference frame, and calibrates the differ.

**The line PREP draws, and it is deliberate — it is what keeps P-4 alive:**

| | |
|---|---|
| **HANDED to all three** (`L4_KIT_CONSTANTS.md`) | module **natives** + asset/texture paths + exact camera parameters. L2 P-B settled decisively that Pro cannot derive these; re-testing it would burn a lap re-answering a closed question and confound what we *are* measuring |
| **NOT handed — must be read out of `scene_before.tscn`** | where the far (−Z) wall sits, its inner-face Z, the floor extent, the node names |

Hand over the placements too and P-4 is gutted — nobody would need to read the scene at all, and
*"expansion requires reading a scene you did not author"* is the entire structural difference between
this lap and a replica lap. **Instruments may read `scene_before.tscn` by any means; no instrument may
read the builder that produced it.**

## §4 — Sequence, and why it is forced

**L4-PREP → W-MUR → W-PRO → H.** Prep, then three sequential dispatches, one instrument each.

- **Murzak first** — already installed; saves a full swap cycle.
- **Pro second** — swap in, run, **restore verified by file inventory, never a version string** (L-J /
  TCP-9). L-J's three known residues apply: `[autoload]` rewrite, class-name cache emptying, and
  **opening a project in an editor is itself a write.**
- **H last, with no wire installed** — the L1 §4c contamination guard: if H's builder script is on disk
  first, a wire agent can **read the answer instead of solving the task.**
- **No instrument reads another's output.** Separate output paths, and it is a HALT to peek.

**Three dispatches, not one.** L3b burned **217K tokens / 85 tool calls** on a single instrument; a
three-instrument run risks exhausting context mid-lap, which is its own silent failure. Each report
must stand alone.

## §5 — Exit predicate

1. **A four-cell contact sheet** at the `__box` framing: `scene_before` | W-MUR | W-PRO | H — plus a
   **`|diff| ×4` strip against `scene_before` for each**, so non-destruction is visible to the eye and
   not only in a table (**L-A**). Assembled by the H dispatch, **running the differ PREP already
   calibrated** (§3b) — the H dispatch does not build the instrument that judges its own cell.
2. **P-2 resolved numerically** — masked pixel diff of the non-addition region, per instrument,
   **against a differ with both calibration points published** (§3b).
2b. **A DETAIL CROP per cell, tightly framed on the dais.** *Added 2026-07-25 by the conductor after
   looking at PREP's reference frame.* At `__box` (CAM_DIST 50) the 6×4 m dais is roughly a ninth of
   the floor and lands in a few hundred pixels — **the six spec clauses (4 steps, 0.15 m rise, 0.5 m
   pillar inset, symmetric props) are not judgeable at that size.** L-A requires a *judgeable* frame,
   and a frame in which the thing under test occupies 100 px does not satisfy it. Same camera
   parameters for every cell's crop, declared once. **The wide shot proves non-destruction; the crop
   proves conformance. Both are required.**
3. **P-1, P-3, P-4, P-5, P-6 each resolved** to a recorded fact with its evidence.
4. **Spec conformance checklist** — the six spec clauses, per instrument, PASS/FAIL with the measurement.
5. **The Pro swap restored and verified by inventory** (§4), plus the class-name-cache rescan.
6. **Blast radius verified per TCP-20** — fingerprint of `reincarnated-godot`'s ignored tree, before
   and after. `git status` alone does not satisfy this.
7. **No Godot or `gamedev-mcp-server` processes left running** — L3's exit-state discipline, standing.

**Honorable fallback (L-F/L-G):** any instrument that fails ships **the attributed failure point with
the exact blocking artifact**, and **its cell still appears on the contact sheet** — showing the
failure. A named ceiling is a PASS. **An unattributed failure is the only real failure.**

## §5b — OPEN FINDING carried out of L4a: the rainbow pillar, and the gap in its own control

**Ratified:** drax's attribution is sound and L4a is **not** at fault. Same mesh, same UVs to five
decimals, same texture, same scale as the room's own pillar; the side-by-side control shows the two
are indistinguishable. P-5's cycle count is not penalized, and TCP-27 ③ propagates the note so L4b
and L4c do not burn cycles on it.

**But the control answers a narrower question than the picture asks, and the difference matters.**
The control proves ***"L4a did not break it."*** It does **not** prove ***"it is not broken."*** If
the fault predates the cell — in the pack, in `kit_replica_level.gd`, or in **PREP's flattening** —
then two equally-broken pillars compare equal and the control passes anyway. **This is the rubric
law (`desirable-run-pattern.md` §6.3) firing on us: a VERIFIED claim must name its rubric AND show
that rubric is the owner's question.** The owner's question at the picture is *"do these read as
stone?"* They do not — they read as **atlas swatch bands with a green glyph**, which is the exact
signature of **L-K instance #3**, the void-cap rainbow (*"sampled a tiling texture the pack does not
ship; returned a palette swatch strip instead of stone, without complaint"*).

**The live hypothesis, and it points at prep rather than the pack.** Flattening extracts the mesh
from the FBX instead of instancing it — and that path is **already known to lose things**: prep
itself found the pillar FBX's internal mesh node carries a **+0.004478 m Y offset that instancing
applies for you and extraction does not.** Material/UV binding is the same class of loss. Against
that: L2 picked `polygon-dark-fortress` *because* it ships genuine tiling stone, and Synty pillars
are atlas-mapped **by design** — so the pack answer is live too.

**Decidable by one cheap probe, and it is NOT run inside this lap:** render the pillar module in
the **production** room and look. Production stone → prep's substrate is unfaithful and TCP-24's
*"the fix is a fix and not a workaround"* needs qualifying. Production rainbow → a standing
`reincarnated-godot` defect that L4 surfaced for free, hidden all this time because the room's
corner pillars are ~89% buried in the walls.

**Why it does not block:** all three cells inherit the identical substrate, so the comparison is
unaffected — and running a second Godot process against the lab project concurrently with a live
cell is precisely L3's orphan-editor hazard. **Queued for after the lap. Named on the contact
sheet, so Matt is not asked to wonder why every cell looks broken.**

## §6 — Conductor interface

- **In-run rulings (drax, logged, veto-open):** prop selection and declared substitutions; how to read
  the existing scene; dais placement arithmetic if the kit forces it; whether to use W→H or direct
  placement **provided the choice is recorded as P-3 evidence**.
- **HALT to gandalf:** any need to write into `reincarnated-godot`; swap restore failure; an instrument
  requiring the frozen `scene_before` to be modified; Murzak launched without the full self-hosted env
  block (**Q46** — the compiled-in default is Cloud and it transmits before any tool call; the launcher
  hard-fails or it does not launch).
- **HALT to Matt:** nothing anticipated.

**Reports:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l4{a,b,c}-<instrument>-run-report.md`

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). **This charter exists because its conductor was
overruled.** I argued the outcome was known well enough to skip the measurement — which is precisely
the reasoning that produced five wrong generalizations in this program's short life. Every prior lap
found a charter defect; assume this one has them too, and report rather than work around.
