# SB-1 Cell A2b-r — RECOVERY · CONTAINMENT · THE GRIP · THE CHANNEL POSE

**Cell ID:** `SB1-CELL-A2b-r` · **Date:** 2026-08-12 · **Author:** drax (presentation seam)
**Ledger:** `gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — rows **A2b-1** (the death + the
containment mandate) and **R-CPB-6** (Matt's two ruled defects) GOVERN. R-CPB-1/2/3/3b/5/5b ride.
**Base:** the A2 landing `drax/notes/2026-08-12-sb1-a2-motion-landing.md`; the probe
`legolas/notes/2026-08-12-whirlwind-rev-rate-probe.md` @ `073dc7fd`.
**Godot repo:** `169bf8b` → `63c94ea`, **four commits, pushed as they landed (PL-7).**

**VERDICT: ITEMS 0 · 1 · 2 · 3 LANDED + STILLS SHIPPED. 0 HALTS. HALTED after item 3 as ordered.**

---

## 0 · THE PROVENANCE ANSWER, FIRST, BECAUSE MATT IS WAITING ON IT

**The hammer and the helmet are SYNTY. Both are clean. Say so plainly.**

| asset | file | pack | licence status |
|---|---|---|---|
| **HAMMER** | `SM_Wep_WarHammer_Large_04.fbx` | `Assets/Synty/polygon-dungeon-realms/FBX/` | **Synty-owned**, already under this repo's day-one `/Assets/Synty/` gitignore rule ("never commit Synty binaries — license forbids sharing source files outside the team") |
| **HELMET** | `SM_Chr_Attach_Undead_Knight_Helmet_01.fbx` | `…/polygon-dungeon-realms/FBX/Characters/Attachments/` | **Synty-owned**, same rule |
| **HEAD** | `SM_Chr_Attach_Undead_Knight_Head_01.fbx` | same | **Synty-owned**, same rule |
| BODY | `Chr_Undead_Knight_01.fbx` | same | **Synty-owned**, same rule (unchanged from A2) |

**No third-party geometry entered the player.** The hammer is from the protagonist's OWN pack, which
is also why it shares his texture atlas — every other pack's hammer would have been a foreign atlas
on a dungeon-realms body. **No Matt fork is needed here: nothing to retain-with-licence, nothing to
re-source.** The marriage may proceed; the birth certificate is in order.

Two non-Synty **textures** are in the VFX (unchanged from A2b, named for completeness):
`Assets/brackeys_vfx_bundle/particles/alpha/spark_04_a.png` and `smoke_05_a.png` — the Brackeys
bundle, which this repo's `.gitignore` records as **CC0** and ignores for size, not licence.

---

## 1 · ITEM 0 — CONTAINMENT

### 1.1 The porcelain delta, every line named

**The conductor's premise about the addons is FALSIFIED BY MEASUREMENT, and the measurement is not
close.** Every untracked addon dir was born **2026-07-28, 20:55–21:20** — fifteen days before SB-1
launched and fourteen before cell A2b ran. **Cell A2b acquired nothing.** The `stat` birth times are
uniform across all twenty-three dirs and `Assets/ThirdParty/`.

The A2b-era delta is **exactly 9 lines**, and not one of them is an addon:

| class | count | the lines |
|---|---|---|
| modified | 4 | `scripts/kc2_player_channel.gd` · `scripts/kc2_cpb_clip.gd` · `scripts/kc2_motion_smoke.gd` · `tmp/kc2/kc2_motion_smoke.json` |
| untracked | 5 | `scripts/kc2_rig_probe.gd` · `scripts/kc2_wep_sheet.gd` · `scenes/kc2_wep_sheet.tscn` · `tmp/kc2/kc2_a2b_head_probe.json` · `tmp/kc2/kc2_a2b_weapon_inventory.json` |

⚑ **`tmp/br2watch/measure/census.json` is NOT A2b's.** It was modified **2026-08-02**, ten days
earlier; it sits INSIDE the L-0 233 baseline. Counting it would have made the arithmetic close at 10
against an observed 9 — and an accounting that is off by one is an accounting that is wrong.
**233 + 9 = 242 = the observed count. It closes.**

**Accounting at cell end: 230.**
`242 − 3 (quarantined addons) − 5 (untracked → committed) − 4 (modified → committed) = 230.`
Observed 230. The L-0 baseline moves by exactly the three quarantined dirs and by nothing else.

### 1.2 The addon table — origin, licence, used, kept or removed

Not one addon is referenced by any script, scene or `project.godot`. Enabled plugins are
`sidekick_creator` + `godot_mcp` **only**. Origin for all: **manual drop-in on 2026-07-28** (no
`.git` dir in any of them, so not a git clone; asset-library / zip extraction).

**QUARANTINED — native-code GDExtensions, unreferenced (receipts:
`reincarnated-godot/tmp/kc2/kc2_a2br_addon_removal_receipts.txt`, moved to
`~/Games/_quarantine/2026-08-12-sb1-a2br-godot-addons/`, reversible, not destroyed):**

| addon | size | files | licence | why it had to go |
|---|---|---|---|---|
| `libik` | 20 M | 24 | **NONE** | GDExtension: loads an unsigned native binary into every engine process regardless of plugin enablement. Zero references. **The rig has finger bones — an IK addon was never needed for the grip.** |
| `vaportrail` | 79 M | 46 | **NONE** | same: native binary, zero references |
| `yparticles3d` | 45 M | 93 | LICENSE | same, **plus a demonstrated harm**: it emitted `ERROR: Error loading extension` on **every Godot start for fifteen days**. That is the clean-negative family this run keeps catching — noise where a real error would hide. |

144 M / 163 files. `.godot/extension_list.cfg` pruned to `godot-sqlite` alone; verified by re-running
the engine to a **silent start**.

**RETAINED — load-bearing:**

| addon | licence | used by | cost of the built-in alternative |
|---|---|---|---|
| `godot-sqlite` (GDExtension, gitignored by `/addons/*sqlite*/`) | LICENSE.md | `sidekick_creator/sidekick_character.gd`, `scripts/retarget_test.gd`, `scripts/compose_test.gd`; opens the Synty Sidekick DB on every project load | Godot has **no** built-in SQLite. Replacing it means re-exporting the whole Sidekick character DB to JSON — a cell of its own, for no gain to this run. |
| `sidekick_creator` (tracked, MPL-2.0) | LICENSE | Synty Sidekick character composition | pre-existing, tracked, authorised |
| `godot_mcp` (gitignored) | NONE | the harness's editor bridge | pre-existing, gitignored, out of this cell's scope |

**DECLARED, NOT DELETED — twenty inert GDScript editor tools:** `advanced_model_import` ·
`animation_property_tracks_batch_modification` · `godot_projectile_engine` · `godot-synty-tools` ·
`import_replacer` · `lens_effects` · `mixamo_animation_batcher` · `modifier_animation_baker` ·
`proton_trail` · `shader-previewer` · `ShaderLib_v2_2_4` · `skeleton_poser_plugin` · `TrailRenderer`
· `unidot_importer` · `UniParticles3D` · `unique_anim_lib` · `Unused Bone Track Remover` ·
`vfx_library` · `vkaParticleTool` · `Assets/ThirdParty/rpicster-vfx-textures` (has a LICENSE).
**Twelve of the twenty carry NO licence file at all** — that is the sharpest remaining edge and it is
named here rather than buried.

**⚑ WHY I DID NOT DELETE THEM, AND THIS IS A DEVIATION FROM THE BRIEF.** Item (c) said "UNUSED **new**
addons: DELETE … they entered the tree without authorization." The word doing the work is *new*, and
measurement refutes it: none is new, all sit inside the L-0 233 baseline every cell of this run
closes against. Deleting twenty pre-L-0 dirs would mutate the run's own containment instrument
mid-run on a premise the birth times just falsified — a coordination act, not a presentation-seam
act. They are inert GDScript, unreferenced, unenabled, and reach **zero** code into the render path,
which is the measured difference between them and the three that went. **The fork is the
conductor's / Matt's, and the removal is one line:**

```
mkdir -p ~/Games/_quarantine/2026-08-12-godot-unused-editor-addons && \
cd ~/Games/reincarnated-godot && mv addons/advanced_model_import \
  addons/animation_property_tracks_batch_modification addons/godot_projectile_engine \
  addons/godot-synty-tools addons/import_replacer addons/lens_effects \
  addons/mixamo_animation_batcher addons/modifier_animation_baker addons/proton_trail \
  addons/shader-previewer addons/ShaderLib_v2_2_4 addons/skeleton_poser_plugin \
  addons/TrailRenderer addons/unidot_importer addons/UniParticles3D addons/unique_anim_lib \
  "addons/Unused Bone Track Remover" addons/vfx_library addons/vkaParticleTool \
  ~/Games/_quarantine/2026-08-12-godot-unused-editor-addons/
```

Firing it drops porcelain 230 → 211, and the L-0 pin needs re-declaring at that number.

### 1.3 Adoption

The three WIP scripts adopted **as-is** and committed FIRST, before any new work, with the two probe
scripts, the weapon-sheet scene and the two probe JSONs that are the hammer's evidence trail.
Baseline verified before touching anything: **motion smoke 32 checks, 0 FAIL** on the inherited tree.
The dead cell's forty minutes are banked.

**CL-2 held this cell: four items, four commits, each pushed as it landed.**

---

## 2 · ITEM 1 — THE GRIP (Matt defect 1)

> *"goes through the wrist… The hand needs to actually have its fingers/thumb wrap around the
> handle, near the base."*

**Root cause, measured not guessed:** a `BoneAttachment3D` sits at the **bone origin**, and the
origin of the `RightHand` bone **is the wrist joint**. A weapon parented straight to that socket is
skewered on the wrist *by construction*. No euler tuning reaches the palm, because the palm is
**0.0975 m** further on. A2b tuned the euler.

**The fix is a GRIP FRAME derived from the rig's own finger rests, never typed:**

| element | derivation | measured on this rig |
|---|---|---|
| origin | `midpoint(Finger_01, Thumb_02)` — the centre of a closed fist, which is physically where a held handle is | 0.0975 m from the wrist bone |
| **+Y** | `Index-base − Finger-base` — the axis a handle takes when a fist closes (the barrel exits the index side) | fist span 0.0599 m |
| **+Z** | `wrist → knuckles`, orthogonalised, so the head's roll is repeatable rather than incidental | — |

The weapon hangs off a `GripPoint` node at that frame and needs **no euler at all** now.

**Fingers close for real.** `Thumb_01..03`, `IndexFinger_01..04`, `Finger_01..04` each rotate about
**the haft itself** — 32°/joint; the thumb the other way at 27°, because a thumb curling with the
fingers is inside the fist. Asserted: **15 of 15** finger/thumb joints off rest (bar 0.05 rad); at
rest every one reads 0.000, which is an open hand with a hammer through it.

**Both hands, near the base.** Right fist **9 %** up the haft from the pommel, left fist **0.1000 m**
below it — the baseball grip. Grip residual **0.00047 m** against a 0.010 m bar.

**⚑ `libik` WAS NOT NEEDED AND IS QUARANTINED.** The rig carries `Thumb_01..03`,
`IndexFinger_01..04` and `Finger_01..04` per hand, so the fingers pose with built-in `Skeleton3D`
bone poses. The two-arm reach is the **law of cosines** — twenty lines, exact, no solver, no native
code, no dependency. Declared either way, as the brief required.

---

## 3 · ITEM 2 — THE CHANNEL POSE (Matt defect 2, the bigger one)

> *"roughly standing still with arms down at its sides, but it should be swinging the hammer in
> something more similar to a baseball swing that never resolves."*

The protagonist is **off the locomotion line entirely**. A2 bound him to the same `loco/idle` as the
344 trash bodies and spun the holder — an arms-down idle on a turntable is a **statue rotating**. He
now carries an **authored frozen mid-swing**, applied ONCE at build, spun eternal by the 0.36 s/rev
yaw. Every `AnimationPlayer` in his subtree is stopped **and** deactivated by walk (**4** silenced;
the Synty FBX ships one with 31 tracks) — a live player would overwrite every bone pose on its first
frame and put the statue back without a word.

**Degrees of freedom — every one a named constant, one edit each:**

| constant | value | what it decides |
|---|---|---|
| `SWING_YAW_DEG` | −54 | where in the circle the hands sit, from body-forward |
| `ARM_DROP_DEG` | 10 | the swing plane, below horizontal |
| `TORSO_TWIST_DEG` | −38 | chest coiled into the swing |
| `HIP_TWIST_DEG` | −13 | hips lag the chest — **the coil is the difference**, 25° |
| `TORSO_LEAN_DEG` | 18 | leaning INTO the swing (about the swing's own axis) |
| `STANCE_SPLIT_DEG` | 15 | lead boot into the swing, trail boot braced back |
| `KNEE_BEND_DEG` | 26 | lead knee full, trail knee 0.55× |
| `HEAD_TURN_DEG` / `HEAD_TILT_DEG` | −26 / 14 | he is looking down the swing |
| `HAFT_LAG_DEG` | 12 | the head TRAILS the hands: a swing mid-flight, not a lance |
| `ARM_EXTENSION_FRAC` | 0.99 | never 1.00 — a chain at full length has a straight elbow, and a straight elbow is Matt's robot arm |

**FG-10 survives by construction.** The pose is applied once and never touched; the only thing that
moves per tick is `body_holder.rotation.y`, still a pure function of sim time. Asserted in smoke.

**Oscillation: NOT BUILT, declared.** A per-revolution wobble would be a second clock beside the
trace's (GL-18) and would make the spark radius time-varying, weakening the one law the ring rests
on — sparks at exactly the hammer's reach. Cheap to add later as a pure function of the same tick.
Veto-open.

---

## 4 · ITEM 3 — RE-MEASURE, GENEROSITY, AND THE SECOND SPARK LAYER

### 4.1 The radii

| radius | value | basis |
|---|---|---|
| hammer-tip sweep, A2b arms-down | **1.1696 m** | the number the pose had to move |
| **hammer-tip sweep, A2b-r pose** | **2.1563 m** | MEASURED: max horizontal distance from the spin axis to any of 1,958 weapon vertices, in the pose the scene draws, bone globals composed from local poses |
| R-CPB-5 ruled band | [2.10, 2.35] | **INSIDE** |
| kill ring `d_engage` | 2.400 m | **margin 0.2437 m** — kills land just outside the steel's visible reach |
| continuous TRAIL, haft axis | 2.0086 m | inside the sweep, because the head's outboard **corner** leads the axis |
| SMOKE (damage truth) | 3.000 m | the wire's own `circle_sweep.radius_m`, unmoved |
| hands radius | 0.6752 m | an **anatomy fact**, not a dial |

**Spread 0.0000 m, honestly.** A2b measured twelve phases of an idle cycle because the hand moved
through the clip. The channel pose does not move: twelve samples would be twelve copies of one
number wearing a distribution's clothes. One sample, spread zero, and the basis string says so.

### 4.2 ⚑ THE ONE BAND THIS CELL BROKE, LOUDLY

**`WEAPON_SCALE` 1.35 → 1.65, outside A2b's own declared ~1.2–1.5× "genre convention".**

The band cannot reach R-CPB-5's target once the hands radius is measured rather than guessed. The
hands are pinned near the mid-sagittal plane because **both fists are on one haft**: shoulders 0.41 m
apart, each arm spans 0.611 m. At scale **1.50** (band top) the sweep measures **1.990 m** — 0.410 m
of air under the kill ring, which is not "just under" anything.

Two rulings collide, so the weaker-sourced one yields. **R-CPB-5 is a LAW**, Matt-ruled at the CP-B
dialogue and canonised on his word. The 1.2–1.5 band is the cell's own summary of genre convention,
and **the legolas probe went looking for its sources and came back UNRESOLVED** ("Weapon scale:
sources UNRESOLVED → direct measurement"). An unsourced convention does not overrule a ruled law.

1.65 is the **smallest** factor that lands the sweep inside the ruled band. Hammer 1.648 m native /
1.615 m in world on a 1.7097 m body — **94 % of his height**. Big, still visibly a weapon.
**The alternatives are priced, one line and a re-render each:** ~1.95 puts the sweep at the band's
top (2.35 m, 0.05 m under the ring) with a hammer taller than the man; 1.50 restores the genre band
and hands the ring back 0.41 m of air. **Matt's eye picks.**

### 4.3 The two-layer convention, built as two layers

The probe found GD and D3 both split a continuous weapon-bone **TRAIL** from discrete **CONTACT
BURSTS** and keep them as independent records (GD hangs two `EffectEntity` on the weapon bones).

**How the WIP mapped on, and what I adjusted:** A2b built the **burst half only** — three staggered
emitters on the sweep circle, duty-cycled from a hash of (emitter, revolution), never solid and never
dark. That is the discrete layer and it is right. **The continuous layer was missing and is added
here**: a world-space emitter riding the hammer head itself, always on, gated on the same wire bit as
the bursts. The streak is the steel's actual passage instead of a ring drawn where the steel is
supposed to be — and it is what makes 33.3°/frame legible. `TRAIL_*` and `SPARK_*` are **separate
constant families**, which is what "independent records" is worth in practice.

---

## 5 · Per-item commit table (CL-2)

| hash | item | what |
|---|---|---|
| `c312f36` | **0** | CONTAINMENT + ADOPTION — provenance answered, the addon premise falsified, three native GDExtensions quarantined with receipts, the dead cell's WIP adopted |
| `0097826` | **1 + 2** | THE GRIP and THE CHANNEL POSE — one commit, structurally (the grip's target is a point on a haft the pose puts there; they are one solve, and splitting them would have committed a grip that reached at nothing) |
| `6b5be76` | **3** | RE-MEASURE, the generosity check, the second spark layer, **7 new smoke rows (32 → 39)** |
| `63c94ea` | stills | the four-frame deliverable + what my eyes changed |

All four **pushed as they landed** (PL-7). Zero minutes of uncommitted work at any point.

---

## 6 · Self-attack surfaces (ranked, veto-open)

1. **`WEAPON_SCALE` 1.65 breaks a band this cell declared.** § 4.2 argues the law outranks the
   unsourced convention. If Matt disagrees, 1.50 restores the band and R-CPB-5 goes unmet by 0.41 m
   — and *that* becomes the thing to say out loud instead.
2. **The pose is a presentation choice with NO WIRE BASIS**, exactly like the spin rate. The wire
   carries `circle_sweep.active` on 3,732 of 3,732 samples and says nothing whatever about limbs.
   Ten constants, ten opinions.
3. **The hands radius caps the reach at 0.675 m and cannot be argued up.** If Matt wants the sparks
   at 2.35 m, only the hammer can grow.
4. **`HAFT_LAG_DEG` 12° is invented.** It reads as "the head trails the hands"; nothing sourced it.
5. **The right elbow sits at 139°, the left at 159°** — asymmetric, which is what a real trail arm
   does at contact, but it is a claim about baseball made by someone rendering a whirlwind.
6. **No oscillation.** § 3 gives the reason; a watcher may simply find the frozen pose dead over 60 s
   of clip, which the stills cannot tell me and the next cell's clip can.
7. **Twenty unlicensed editor addons stay in the tree** on my judgment (§ 1.2). If the conductor
   reads that as ducking the mandate, the command is written out and takes one line.
8. **The helmet is still Matt's "ok"** — accepted tepid. Untouched this cell; upgrade surface open.

---

## 7 · Stills

`agentic_orchestration/galadriel/captures/2026-08-12-sb1-a2br-stills/` — four 1920×1080 PNGs, **all
at tick 1600**, plus `MANIFEST.json` (sha256, bytes, camera pose, FOV, and the measured numbers per
frame). **Class E, untracked, never committed.** PL-5 floor check fired before a frame existed:
6.70 G of the 10 G ceiling.

| file | what it answers |
|---|---|
| `01-grip-closeup.png` | defect 1 — fists wrapped on the haft, the wrist behind them |
| `02-pose-full-body.png` | defect 2 — the frozen mid-swing, broadside to the swing normal |
| `03-three-quarter-reach.png` | the reach and both spark layers over the smoke bed |
| `04-overhead-sweep-vs-ring.png` | the three radii in one frame: sweep inside the violet 2.400 m ring inside the blue 3.000 m ribbon |

**No clip rendered.** The consolidated CP-B′ waits for Matt's full review list — one re-render, not
two, as the cadence ruling says.

---

## 8 · Laws

**Zero combat lines** — R-A1-1 asserted across the whole driven tree with the player, pose and FX in
it: 0 text/canvas nodes; the no-combat guard on the driver's stripped bytes still passes.
**GL-18 untouched** — one clock; the stills' spin-up computes its tick from the frame index.
**GL-6** — the loader path was not touched; the baton digest recomputes to `d7ecd866ac45` (MATCH) on
every run in this cell. **D-14** — no factory-spine coupling; all renders classic.
**Porcelain** — closes at **230**, every delta named in § 1.1.
**Engine repo** — untouched.

---

## NOTES (continuing from NOTE-23)

**NOTE-24 — A `BoneAttachment3D` is a WRIST socket, not a HAND socket.** It sits at the bone origin,
and every humanoid rig puts the hand bone's origin at the wrist joint. Anything parented to it is
skewered on the wrist. Hand-held props need a grip frame derived from the finger rests; on this rig
the palm is 0.0975 m past the socket. Applies to every weapon this project ever hangs on a body.

**NOTE-25 — A two-handed grip is an ANATOMY CONSTRAINT, and it caps reach hard.** Shoulders 0.41 m
apart, arm span 0.611 m: both fists on one haft pins the hands near the mid-sagittal plane, max
radius ~0.68 m with a lean. Any VFX radius target built on "arms out" arithmetic will overshoot what
a two-handed pose can deliver. Budget the weapon, not the arms.

**NOTE-26 — Lean INTO the rotation, not forward.** A lean about the swing's own axis carries the
shoulders outboard (0.25 m at 18° and 1.4 m of shoulder height) *and* is what every reference
whirlwind does. Leaning forward looks the same in a thumbnail and leaves the reach on the table.

**NOTE-27 — Solve to 0.99 of the chain, never 1.00.** A two-bone solve to its own full length
produces a straight elbow by definition. 0.99 lands ~164°: extended, visibly unlocked. The reach must
then RELAX — solve, read how far each shoulder was asked to stretch, pull in by the overshoot — or
the residual and the locked elbow both hide behind a plausible-looking pose.

**NOTE-28 — NOTE-23's family, fifth and sixth instances, both in one cell.** (a) `_s_aabb(node)`
includes the node's OWN transform, so its numbers live in the *parent's* space while a child's
`position` is read in the node's — the trail emitter landed 0.32 m past the steel. (b) Walking node
transforms through a `BoneAttachment3D` silently skips the whole arm, because Godot writes that
transform on a processed frame a headless harness never takes — the trail radius read 1.54 m for a
head at 2.13. **The render was never wrong; only the measurement was, which is the more dangerous
of the two.** Both were caught by *comparing two radii that should have had a known relationship*.

**NOTE-29 — A VFX layer whose content is MOTION cannot be photographed from a paused world.** Set the
tick once and take frames and you get: a body that never turns, a world-space trail pooled into a
blob, and duty-cycled emitters frozen on one gate state. Still-capture of anything moving must spin
up through real ticks first. Rewind by more than the longest particle lifetime, play forward at 1×.

**NOTE-30 — Frame the subject broadside to its own axis.** The full-body still was first shot down
the hammer's axis, which foreshortened the entire swing into a man holding a pole at the camera. The
frame answered neither defect while looking, at a glance, like it did.

**NOTE-31 — A manifest that quotes constants as typed literals goes stale the moment you retune.**
Three pose angles in the still manifest were literals; I retuned the pose twice after writing them.
Read every published number from the constant that produces it.

**NOTE-32 — Normalise a body's height on the body STANDING UP, before any pose.** Measuring a
crouched, leaning mid-swing AABB and normalising *that* to a target height inflates the character
every time the brace deepens. Rest → measure → scale → pose.

**NOTE-33 — Birth times settle provenance arguments in one command.** `stat -f %SB` on twenty-three
addon dirs refuted a supply-chain premise in ten seconds and redirected the containment work to the
three that actually mattered. Check when a thing arrived before arguing about who let it in.

**NOTE-34 — An unused GDExtension is not inert.** `.gdextension` files load their native binaries on
every engine start regardless of plugin enablement. That is the measured line between "clutter" and
"code running in your process", and it is the line worth acting on first.

---

*Landed by drax, presentation seam, 2026-08-12. HALT after item 3, as ordered.*
