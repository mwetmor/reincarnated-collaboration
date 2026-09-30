# Research — Weapon holds and attacks in our 3D pipeline — 2026-09-29

**Mode:** A (analytical + primary-source probe)
**Commissioner:** gandalf (conductor, Run C-9 Phase 2), on Matt's question
**Author:** legolas (UNKNOWN-RESEARCHER)
**Status:** findings; no repo code touched. Probes ran read-only against shipped files; all probe
artefacts were written to the session scratchpad, not the repo.

Matt's question, verbatim: *"PLEASE research how to get the weapon holds and attacks right within
our 3D pipeline. ultra think through how others are doing it that may work here. We must get this
right!"*

Every claim is tagged **VERIFIED** (with source or probe), **MEASURED** (I ran it, numbers below),
or **INFERENCE**. Nothing here is reported from memory.

---

## Summary

1. **The conductor's hypothesis is correct, and the evidence is stronger than the hypothesis.** It is
   not merely that there is no weapon bone to author against — the axe is a **skinned mesh with all
   7,506 of its vertices weighted 1.0 to `RightHand`** (MEASURED). Its orientation is frozen into
   vertex positions at bind time, so there is *no transform channel of any kind* between the hand and
   the weapon. Our own code says so in its docstring: *"getting the REST pose right is the whole job:
   the bone then carries it through every clip."* One rest pose, every clip, forever.
2. **The fix is verified end-to-end and is close to free.** I inserted a `weapon_r` bone as a child of
   `RightHand`, coincident with it, moved all 7,506 weights to it, and round-tripped through glTF into
   Godot 4.6.3. Result: **rest-pose displacement 4.02 × 10⁻⁷ m** (a visual no-op), **25 bones imported,
   `weapon_r` parented to `RightHand`, and a rotation track with 37 keys surviving into Godot**. The
   weapon's grip point does not move when `weapon_r` rotates — so the hold is preserved while the
   angle becomes free. This is the single highest-value change available.
3. **There are three separate defects, not one, and they need three different fixes.** (a) *Orientation*
   — the current complaint; fixed by the weapon bone. (b) *Edge alignment* — **the cutting edge is
   never within 45° of the character's forward direction in any clip** (MEASURED across 13 clips);
   fixed by fitting the mount roll, which the manifest itself admits was never done
   (`"status": "PLACED, ORIENTATION NOT FITTED"`). (c) *Arc noise* — the axe head travels **239–285 px
   over one armed-idle loop on a 140 px figure**; this is driven by the shoulder and elbow, **so neither
   the wrist lock nor a weapon bone can fix it**. It needs a quieter source clip or weapon-first
   authoring.
4. **The camera has a law and it should drive the choreography.** At pitch 52.9535° / yaw 47°, a
   vertical lift and a step away from camera are **0.00° apart on screen** — geometrically
   indistinguishable. A 0.9 m sweep reads as **42 px** if vertical, **70 px** if screen-lateral.
   Author cuts as **diagonals with a dominant horizontal component**; reserve vertical gestures for
   casts, where the FX carries the read.
5. **Sourcing is mostly already solved.** The Meshy library we already query holds 678 actions, 174 of
   them `Fighting`, including `Double_Blade_Spin`, `Axe_Spin_Attack`, `Double_Combo_Attack`,
   `Weapon_Combo` 0–2, `Left_Slash`, `Right_Hand_Sword_Slash`, `Combat_Stance`, `Sword_Shout`, and
   **nine `Mage Spell Cast` clips** plus two `Charged Spell Cast`. We do not need video mocap or
   text-to-motion for the barbarian or the sorceress core set.
6. **`Combat_Stance` (action_id 89) is the direct answer to Matt's words.** The wrist lock's target
   angle is currently taken from the *idle*, by the authoring script's own comment. An idle is a carry
   pose. Matt is asking for a guard pose. The library has one.

---

## Part 1 — What our pipeline actually does (read from the shipped files)

Everything in this part was read out of the repo or measured from the shipped GLBs. No inference.

### 1.1 The weapon is skinned, not socketed

`runs/C-9/nb_d2/scripts/gearlib.py :: socket_weapon2()` docstring, verbatim:

> "Binding is by vertex group and an armature modifier, not by a parent transform, so getting the
> REST pose right is the whole job: the bone then carries it through every clip."

**MEASURED** (probe 1, below): `nb_d2/export/axe.glb` contains a 24-bone skeleton whose vertex groups
are exactly the body's 24 bones, and the axe mesh's **7,506 vertices are weighted to `RightHand`**.

`attack_lab/godot/scripts/gear.gd` confirms the runtime side, verbatim:

> "THE MANIFEST DECLARES THREE BIND MODES AND THE FILES CARRY ONE. It lists `bone` for the helmet and
> bracers, `skin` for the byrnie and mantle, and `socket` for the axe and shield — which is a faithful
> description of how they were AUTHORED. What was exported is another matter […] every piece,
> including both sockets, arrives as a SKINNED mesh."

So: the manifest *says* socket; the file *is* skin. The runtime takes the file's word, correctly.

**Consequence.** The weapon's world orientation equals `RightHand`'s world orientation times a single
constant baked at bind time. The only authoring knobs are `axis_world` and `face_world` (the rest
direction of the haft and of the edge) plus `length`, `grip`, `offset_world` — **all global, all
one-shot, all shared by every clip.** The conductor's hypothesis is confirmed: there is no channel in
which to author the weapon's own motion.

### 1.2 The manifest already admits the orientation was never fitted

`nb_d2/artifacts/D2-manifest.json`, verbatim, for both weapons:

```
{"name": "axe",    "bind": "socket", "bone": "RightHand",    "length_m": 0.82, "grip_frac": 0.28,
 "status": "PLACED, ORIENTATION NOT FITTED"}
{"name": "shield", "bind": "socket", "bone": "LeftForeArm",  "length_m": 0.78, "grip_frac": 0.5,
 "status": "PLACED, ORIENTATION NOT FITTED"}
```

That is our own record saying the thing Matt is complaining about was never done.

### 1.3 The wrist lock's target is a carry pose, by design

`nb_d2/scripts/27_armed_carry.py` header, verbatim:

> "Build walk_armed / run_armed: the same locomotion with the wrists locked to a weapon carry angle,
> so the axe and shield stop waffling. […] **The target angle comes from the IDLE, because the idle is
> the clip Matt said looks right: 'the axe is better when idling.'**"

This is a sound decision that has now been outgrown. Matt's earlier note (*"better when idling"*) was
about *stability*; his current note (*"held tilted towards the character instead of at a battle
stance"*) is about *pose*. The lock propagates the idle's pose into locomotion faithfully — which is
why the tilt is now *consistent* and still *wrong*. **Nothing is broken here; the target is.**

### 1.4 Probe: how the axe is actually held, per clip

**MEASURED.** I recovered the axe's haft and edge directions as constants in `RightHand`'s frame from
`export/axe.glb`'s bind pose, then carried them through every clip of `work/nb-body-final.glb` using
`RightHand`'s pose. Character frame derived from the rig itself — up = Hips→Spine02, his-right = the
shoulder line, forward = up × right with the **sign independently checked against the ankle→toe
direction** (the check passed without flipping). Medians over each clip:

| clip | frames | tilt from vertical | haft forward | haft outboard | edge heading |
|---|---:|---:|---:|---:|---:|
| `idle` | 97 | **12.2°** | +0.16 | +0.14 | 129° |
| `idle_armed` | 148 | 40.1° | +0.29 | +0.25 | 61° |
| `walk_armed` | 43 | — | — | — | — |
| `run_armed` | 17 | 29.2° | +0.19 | +0.28 | 68° |
| `run_armed_L` | 16 | 38.9° | **−0.62** | +0.06 | **−160°** |
| `run_armed_R` | 16 | 44.8° | +0.24 | +0.66 | 151° |
| `attack` | 37 | **68.4°** | **−0.43** | **−0.26** | 115° |
| `attack_chop` | 185 | 66.8° | +0.19 | +0.69 | 88° |
| `block` | 85 | **159.9°** | +0.25 | +0.21 | −116° |
| `shield_bash` | 59 | 42.7° | +0.16 | +0.52 | — |

Read this table against the acceptance predicate our own `axe_diag2.gd` already encodes — tilt in
30–60°, haft forward > 0, haft outboard > 0, head outboard > 0, |edge heading| ≤ 45°:

- **No clip passes.** Every one fails on edge heading; the closest is `idle_armed` at 61°.
- **`attack` has haft forward = −0.43 and haft outboard = −0.26** — at the median frame of the strike
  the haft points *backward and across the body, toward the character*. That is Matt's sentence, in
  numbers.
- **`block` sits at 159.9° from vertical** — the axe is all but inverted through the block.
- **The frame-independent finding, immune to any error in my axis derivation:** `haft forward`
  **changes sign between clips** (−0.62, −0.43 … +0.29) and tilt ranges over **147.7°** (12.2 → 159.9)
  — under a *single baked mount*. A constant cannot be correct for a set that varies this much. This
  is the structural argument, and it does not depend on my choice of forward axis.

`attack_lab/godot/tools/axe_probe.gd` already measures these exact quantities in the character's
declared skeleton frame (forward +Z, up +Y, right −X) and should be the instrument of record for
re-confirming the table above. Its header states the same question in Matt's own words. **It exists
and appears never to have been run to an archived result** — there is no `[diag]`/`[probe]` output
anywhere under `runs/C-9`.

### 1.5 Probe: the axe head's on-screen arc, per direction cell

**MEASURED.** Same recovered head point, projected through the combat-lane camera (pitch
52.9535411256029° down, yaw 47° + k·45°, orthographic) at **77.8 px/m** (140 px for a 1.8 m figure).
Per-frame step and total path length of the axe head, min/max across the 8 cells:

| clip | frames | arc (px), min–max across cells | worst single-frame step |
|---|---:|---:|---:|
| `attack` | 37 | 435 – 518 | **79.3 px** |
| `attack_chop` | 185 | 304 – 377 | 18.8 px |
| `idle_armed` | 148 | **239 – 285** | 19.8 px |
| `idle` | 97 | 184 – 205 | 6.2 px |
| `block` | 85 | 133 – 170 | 7.4 px |
| `run_armed` | 17 | 83 – 107 | 15.4 px |
| `run_armed_L` / `_R` | 16 | 32 – 56 | 9.3 px |
| `walk_armed` | 43 | **25 – 46** | **2.3 px** |
| `walk` (unarmed src) | 26 | 60 – 106 | 13.2 px |

Three things fall out:

- **`walk_armed` is the well-behaved clip: 25–46 px of total axe travel, 2.3 px peak step.** That is
  what a correct armed locomotion cycle looks like at this register.
- **`idle_armed` is not: 239–285 px of axe-head path over one loop, on a 140 px figure — the head
  wanders roughly twice the character's height while he stands still.** This is the "waffle," still
  present *after* the wrist lock, and it is the clip the lock's alpha sweep tuned hardest (α = 0.75 for
  `idle_armed` vs 0.45 for `walk_armed`, per `work/retune.json`). **The stronger lock produced the
  worse arc.** That is diagnostic: *the wrist is not the source.* The grip point is carried by the
  shoulder and elbow, and the axe head sits ~0.6 m beyond the fist, so shoulder motion is amplified
  along a longer lever than the hand's. **A wrist lock cannot bound the weapon's arc, and neither can
  a weapon bone** — a weapon bone re-aims the weapon about the grip; it does not move the grip.
- **`attack` steps up to 79.3 px in one frame** — more than half the figure height between consecutive
  frames. Whatever output rate the attack cell is sampled at, this needs a trail or smear, or the
  strike will read as a teleport. (Q5 sources on smears and trails, below.)

### 1.6 What already exists that the fix should reuse

- `axe.glb` already carries an **`axe_edge` marker** `Node3D` under a `RightHand` `BoneAttachment3D`,
  and `gear.gd` explicitly re-creates that attachment on the body's skeleton so the marker survives
  (**VERIFIED**, `gear.gd` comment: *"axe.glb carries a Node3D named `axe_edge` under a RightHand
  BoneAttachment3D — the edge marker the last report asked for"*). The edge instrument is built.
- `21_lint_export.py` is a standing export lint with FAIL/WARN rules on joint scale tracks and root
  drift. **It contains no bone-count assertion** (MEASURED — grep for `24`/`bone_count` returns
  nothing), so adding bones will not trip it. It will need a new rule (§ 6.6).
- `TwoBoneIK3D` is present in Godot 4.6.3 and supports **multiple settings per node** with
  `settings/N/{root_bone,middle_bone,end_bone,target_node,pole_node,pole_direction}` (**VERIFIED** by
  instantiating the class and enumerating its property list on 4.6.3). The off-hand-on-staff problem is
  solvable with machinery drax already uses for feet.
- `BoneAttachment3D` can also write *back* to the skeleton via `override_pose`, but the Godot docs warn
  it *"operates interruptively in the skeleton update process using signals"* and *"may cause unintended
  behavior when used at the same time with SkeletonModifier3D"* (**VERIFIED**, class reference). Since
  we use `TwoBoneIK3D`, which *is* a `SkeletonModifier3D`, **do not build the weapon channel on
  `override_pose`.** Use a real bone.

---

## Part 2 — Probe: the weapon bone, verified end to end

This is the load-bearing feasibility result. Script: scratchpad
`probe/weapon_bone_probe.py`; run with Blender 5.2.0 LTS and Godot 4.6.3.stable against the **shipped**
`nb_d2/export/axe.glb`.

**Procedure.** Import the shipped axe → add `weapon_r` in edit mode with head/tail/roll copied from
`RightHand`, parented to it, `use_connect = False`, `use_deform = True` → move every vertex from the
`RightHand` group to a new `weapon_r` group at weight 1.0 → keyframe a 35° rotation on `weapon_r` →
export GLB → re-import → measure.

**Results (MEASURED):**

| check | result |
|---|---|
| source skeleton | 24 bones; axe mesh 7,506 verts; groups = the body's 24 bone names |
| weights moved `RightHand` → `weapon_r` | 7,506 / 7,506 |
| **rest-pose displacement of the axe after rebind** | **4.02 × 10⁻⁷ m** |
| axe extremity displacement for a 35° `weapon_r` rotation | 0.119 m |
| glTF round trip, bones | 25; `weapon_r` present; parent `RightHand`; weights present |
| glTF round trip, channels | 10 f-curves on `weapon_r`, incl. all 4 quaternion components × 30 keys |
| **Godot 4.6.3 import** | **25 bones; `weapon_r` idx 24, parent `RightHand`; rotation track, 37 keys** |
| `weapon_r` origin under its own rotation | unchanged, d = 0.0 — **the grip does not move** |

Four things this establishes:

1. **The migration is a visual no-op.** 0.4 µm. There is no "before/after" to re-approve; the fix is
   additive.
2. **The channel survives the whole chain** — Blender → glTF → Godot 4.6.3 — as a first-class rotation
   track that the existing `AnimationPlayer` plays without any new runtime code.
3. **Rotating the weapon bone pivots the weapon about the fist.** The grip stays welded to the hand —
   which is exactly what the grip morphs were built to sell, and it is preserved for free.
4. **The bone is a *deform* bone**, because the axe is skinned to it. That matters: Blender's glTF
   exporter has an `Export Deformation Bones Only` option, and there are open upstream bugs when that
   option meets *non*-deforming bones — [glTF-Blender-IO #2394](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2394),
   [#2697](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2697) (skins silently not exported),
   [#2115](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2115). Weighting the weapon to
   `weapon_r` sidesteps that class of bug entirely. **Set `use_deform = True` explicitly anyway.**

**One hard integration requirement.** `gear.gd` binds every piece by reparenting it under the body's
`Skeleton3D` and reports `bones_match_body = (piece_bone_names == body_bone_names)` — an
**order-sensitive** list comparison. So `weapon_r` and `weapon_l` must be added to the **base rig**,
before any piece is exported, so that body, byrnie, mantle, bracers, helmet, axe and shield all carry
the identical 26-bone skeleton in the identical order. Adding the bone to the axe alone would split the
skeletons.

---

## Part 3 — The camera's law: which arcs read at 140 px

Computed from the camera of record (pitch **52.9535411256029°** down, yaw **47.0°**, orthographic;
`canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md` and the
`player_lock` operand set in gandalf's SB-1 handoff). Figure register **140 px / 1080** ≈ 12.96 %
(double-sourced in the SB-1 ledger: harness geometry 12.990 % vs galadriel's independent vision
measurement 12.963 %, agreeing within 0.3 px). **77.8 px per metre.**

**MEASURED** (scratchpad `camwork/cam.py`), screen projection of a unit world motion:

| unit world motion | screen x | screen y | visible length | px for a 0.9 m sweep |
|---|---:|---:|---:|---:|
| world **up** (a vertical chop) | 0.000 | +0.603 | **0.603** | **42.2** |
| ground, **along** the camera azimuth | 0.000 | +0.798 | 0.798 | 55.9 |
| ground, **perpendicular** to azimuth | +1.000 | 0.000 | **1.000** | **70.0** |
| ground, 45° between | +0.707 | +0.564 | 0.905 | 63.3 |

And the consequence that matters more than the foreshortening:

> **The screen angle between "lift the weapon vertically" and "step away from the camera" is 0.00°.**

They are the *same screen direction*. A vertical chop's downstroke and a forward lunge are
indistinguishable in direction, and the lunge is the *stronger* of the two on screen (0.798 vs 0.603).
At this camera, vertical is both the shortest read and the ambiguous one.

A ground-plane sweep, by contrast, is robust across all eight cells — I computed the projected length
of a character-local forward and lateral unit vector for each 45° facing and the range is **55.9 to
70.0 px per 0.9 m**, never below 55.9 in any cell. **INFERENCE (from the above):** author melee cuts as
**diagonals with a dominant horizontal component** — the horizontal buys the read, the vertical
component buys the weight. Reserve near-vertical gestures (overhead Meteor call-down, a raised war-cry)
for moments where **FX carries the read**, not the silhouette.

**One free production win. INFERENCE (geometric, derivable, please verify before relying on it):** the
eight direction cells are eight cameras at a common pitch and 45° yaw steps (confirmed in
`runs/C-9/meshy_t2/work/bonedump.json`, whose eight camera matrices share an identical elevation row).
Rotating the camera 45° is identical to rotating the character −45°. So for a **Whirlwind authored as a
constant local pose plus a uniform single-revolution root yaw**, cell *k* at frame *i* equals cell 0 at
frame *i + kN/8* exactly. **Pick N divisible by 8 (16 or 24) and all eight cells come out of one
render, automatically consistent.** The precondition is real and binding: the identity holds only while
the pose is constant in the character's local frame. Put any independent arm cycle in the spin and it
breaks.

**A registered counter-risk, from our own record.** The SB-1 ledger already carries a Gate-2
readability flag on exactly this move (galadriel, `cannot_answer #1`): at canon register a spinning
figure read as *"wheel/rim + radial-spoke mass, not unambiguous humanoid."* The note continues: *"D3
whirlwind keeps the barb's silhouette with blur additive; if our body dissolves into FX at register,
that is a finding."* **The Whirlwind's risk at 140 px is silhouette dissolution, and it is already
logged.** Whatever we author, the acceptance test is *does a humanoid still read*, not *does the spin
look fast*.

---

## Part 4 — Sourcing: what the Meshy library already holds

**MEASURED** from `runs/C-9/nb_t8/work/motions.json`: **678 actions** — `WalkAndRun` 176, `BodyMovements`
158, `DailyActions` 157, **`Fighting` 174**, `Dancing` 33.

Against the two characters the commission names, the library covers most of it:

**Barbarian, sword (right) + axe (left)**

| need | library candidates (`action_id`) |
|---|---|
| **battle-stance idle** | **89 `Combat Idel` / `Combat_Stance`** ← the direct answer to Matt's note; 85 `Axe Stance`; 335 `Axe Breathe and Look Around` (current source) |
| walk / run | 21 `Walk Fight Forward`, 20 `Walk Fight Back`, 9/10 `ForwardLeft/Right Run Fight` (630/631) |
| alternating strikes | 92 `Double Combo Attack`, 105 `Triple Combo Attack`, 199/202/241 `Weapon Combo` 0–2, 97 `Left Slash`, 219 `Right-hand Sword Slash`, 240 `Thrust Slash`, 242 `Charged Slash`, 221 `Charged Upward Slash`, 99 `Reaping Swing`, 237 `Charged Axe Chop` |
| **Whirlwind** | **91 `Double Blade Spin`** ← dual-wield spin, the closest source; **238 `Axe Spin Attack`**; 100 `Rightward_Spin` |
| war-cry | **101 `Sword Shout`**; 51 `Shouting Angrily`; 26 `Angry Stomp` |
| hit-react | 178/179 `Hit Reaction`, 171 `Hit Reaction to Waist`, 174–176 `Face Punch Reaction`, 187/190 `Knock Down` |
| death | 8 `Dead`, 188 `Fall Dead from Abdominal Injury`, 189 `Dying Backwards` |

**Fire sorceress, staff**

| need | library candidates |
|---|---|
| casts | **129–137 `Mage Soell Cast` 0–8** (nine clips, spelling as shipped); 125/126 `Charged Spell Cast` 0–1 |
| Meteor call-down | 125/126 `Charged Spell Cast` are the charged-gesture candidates; a call-down wants an *upward* reach, which is the camera's weakest direction (§ 3) — **the FX carries it** |
| Fire Ball throw | 239 `Crouch Pull and Throw`, 280 `Female Crouch Pick Throw Forward` as throw references; the mage casts are the primary |
| locomotion / hit / death | as the barbarian |

**INFERENCE:** the barbarian and sorceress core sets are reachable from the library plus our existing
retarget and clip tooling. Text-to-motion (SMPL-H) and video mocap are **not on the critical path** and
should be held as gap-fill for anything the library genuinely lacks — which, on this list, is close to
nothing. Note the sourcing caveat the library carries: these are clips authored for *unarmed or
other-weapon* hands, which is precisely why the weapon's angle needs its own channel (Part 2).

---

## Part 5 — Industry practice

### Q1 — Weapon attachment: prop/weapon/IK bones vs hand sockets

**The pattern we are missing has a name in Epic's own documentation, and Epic defines the bone class
exactly as the thing we need.** VERIFIED — [Skeletons in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletons-in-unreal-engine):

> "A Bone in the current Skeleton that doesn't influence vertices on the Skeletal Mesh. These Bones are
> typically used in an auxiliary manner, **such as for attaching weapons or props, while still being
> animatable as a Bone**."

That last clause is the whole argument. A socket is *"a static point that acts as an offset attachment
point for Bones"* (same page) — **static**. A bone is animatable. Our problem is that the weapon's angle
must vary per clip; therefore we need a bone, not a socket. Epic's taxonomy says so in one sentence.

Confirmed Epic bone names and their documented purpose:

- **`weapon_r` — Epic's words: the *"right-hand auxiliary weapon bone."*** VERIFIED —
  [Copy Bone](https://dev.epicgames.com/documentation/unreal-engine/animation-blueprint-copy-bone-in-unreal-engine).
  The doc's example is *moving the weapon bone at runtime from the character's right hand to their left
  hand* — i.e. the weapon bone is exactly the handle by which weapon-vs-hand relationships are
  reconfigured without touching the hands.
- **`ik_hand_weapon` + "Pin Bones"** — the most on-point official sentence in the corpus. VERIFIED —
  [Retargeting Operation Stack, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/retargeting-operation-stack-in-unreal-engine-5-8?lang=en-US):
  > "**Pin Bones** is a post processing feature used within the IK Retargeter to lock a specific bone
  > (for example, `ik_hand_weapon`) to another bone (for example, `hand_r`). This operation ensures that
  > special bones follow the animated character, **preventing issues like the weapon snapping and
  > maintaining proper hand placement during animations**."
- **`ik_hand_gun`** — VERIFIED as a shipped Epic bone name, appearing in the default mirror table's
  central/non-mirrored regex alongside root/pelvis/spine/neck/head
  ([Mirroring Animation](https://dev.epicgames.com/documentation/unreal-engine/mirroring-animation-in-unreal-engine)).
  It is a *single* central bone, not a left/right pair.
- **`ik_hand_l`, `ik_hand_r`, `ik_hand_root`, `ik_foot_root`, `weapon_l`** — **NOT FOUND** as literal
  strings on any official Epic page, across ~18 pages checked. **Epic does not publish an enumerated
  mannequin bone list.** The names in common circulation are verifiable only by opening the asset. Worth
  recording because it means "the UE mannequin has `weapon_r` and `weapon_l`" is a *community* claim, not
  a documented one — and our own naming decision is therefore ours to make, not a convention to copy
  precisely.

**Epic's instruction that bears directly on our SMPL-H retarget tool.** VERIFIED —
[Using Retargeted Animations](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-retargeted-animations-in-unreal-engine):

> "Find the **Root** bone, any **IK** bones, any **Weapon** bones you may be using or other marker-style
> bones and set them to **Animation**." … "By using **Animation** as the Bone Translation Retargeting
> Mode, the bone's translation comes from the animation data itself and is unchanged."

**Our retarget tool transports each bone in its rest frame. A weapon bone must be excluded from that
transport** — its transform is authored data, not something to be re-derived from a source skeleton that
has no equivalent joint. This is a concrete change to the tool, and Epic states the rule plainly.

**Two hands on one weapon.** Epic's documented mechanism is **Two Bone IK per arm plus a Hand IK
Retargeting node**, not a magic parent. VERIFIED —
[Hand IK Retargeting](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-hand-ik-retargeting-in-unreal-engine):
> "In the example, the characters arms are being attached to the weapon, using a combination of the Two
> Bone IK nodes. The Hand IK Retargeting node is then being used to correct for the over extension of
> the character's left arm." … "0 would favor the left hand, 1 would favor the right hand and 0.5 would
> be equal weight."

Kubold — author of the most widely used UE weapon animation sets — states the practical form. VERIFIED —
[Kubold Unreal FAQ](https://www.kubold.com/unreal-faq-2): *"You need to turn on the IK on the left hand
and snap the effector to the barrel of the gun. This way, the left hand will always be where the IK
effector is – on the barrel."* **This is the sorceress's staff, verbatim, with "barrel" swapped for
"shaft."**

**And Epic names the cost of that approach, which we should plan for.** VERIFIED —
[Virtual Bones](https://dev.epicgames.com/documentation/unreal-engine/virtual-bones-in-unreal-engine):
> "if you were to set up a system where the hands were IK-attached to a weapon, you would have to
> perform extra steps to disable IK in certain situations, such as reloading."

For us "reloading" is any gesture where the off-hand *leaves* the staff — a Fire Ball thrown from the
free hand, a pointing cast. The off-hand IK needs a per-clip enable, not a global one.

**Sockets and how offsets are calibrated.** Unreal sockets are *"dedicated attach points… which can be
transformed relative to the Bone it is parented to"*, and the docs' stated motivation is ours exactly:
*"Instead of using math operations to estimate the offset transform, you can create Sockets"*
(VERIFIED — [Skeletal Mesh Sockets](https://dev.epicgames.com/documentation/unreal-engine/skeletal-mesh-sockets-in-unreal-engine?lang=en-US)).
The calibration affordances are: **Add Preview Asset** (*"Opens a menu of all eligible assets that can be
temporarily attached to a bone for previewing purposes"*) and **Customize Socket / Mesh Socket**, which
copies a skeleton socket onto one mesh so a single weapon can override the shared offset
(VERIFIED — [Skeleton Tree](https://dev.epicgames.com/documentation/en-us/unreal-engine/skeleton-tree?application_version=4.27)).
Unity's analogue is the **Parent Constraint**, whose documented example is literally a sword in a hand,
with an **Activate** button that captures the offset you have posed by hand
(VERIFIED — [Parent Constraint](https://docs.unity3d.com/Manual/class-ParentConstraint.html)); Animation
Rigging adds **Maintain Target Offset** / **Maintain Offset**
(VERIFIED — [TwoBoneIKConstraint](https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/TwoBoneIKConstraint.html),
[MultiParentConstraint](https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/MultiParentConstraint.html)),
and **MultiReferentialConstraint** is the one Unity page that names a prop: *"you could configure a
character's hand to sometimes control the motion of a prop, and the prop to sometimes control the motion
of the hand"*
(VERIFIED — [MultiReferentialConstraint](https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/MultiReferentialConstraint.html)).
That last sentence is *weapon-first authoring*, named by Unity.

**The most useful negative result in the whole commission.** Every system documents a *knob* for
capturing a grip offset — UE socket transform + Mesh Socket override + Add Preview Asset; UE Pin Bones +
Pin Bones Offset; UE Hand FKWeight; Unity Parent Constraint `Activate`; Unity Maintain Target Offset;
OptiTrack Rotation/Translation Offset; CC4's None / Position / Position-and-Rotation enum. **Nobody
documents a procedure for keeping those offsets correct across many weapons and many animation sets.**
Searched Epic, Unity, Reallusion, and GDC Vault abstracts (including *Tools-Based Rigging in Bungie's
Destiny*, GDC 2015, which mentions weapons only in an asset-category list). **The calibration-drift
problem is undocumented rather than solved.** That is the gap our QA instruments (§ 6.6) should fill,
and it means we should not expect to find a best practice to copy — we have to measure.

**Asset-pack conventions.** Synty is the most useful data point because drax already has Synty assets
on disk:

- Synty *character* packs have **no weapon bone** — the store page says only *"Fixed scale enables
  weapons and attachmenst [sic] to be easily parent to skeleton joints without any additional scaling"*
  (VERIFIED — [POLYGON Modular Fantasy Hero](https://syntystore.com/products/polygon-modular-fantasy-hero-characters)).
- Synty *animation* packs **add one**: *"ANIMATION - Swords Combat animations make use of a prop bone, an
  extra bone added to the hand"*, with the warning *"You may need to retarget the animations using
  third-party tools to get the prop bone to animate correctly on other character rigs"*
  (VERIFIED — [Animation: Sword Combat](https://syntystore.com/products/animation-sword-combat)).
  **A commercial sword-animation vendor ships exactly the bone this report recommends, and ships it
  because the animations need it.**
- LOCAL PRIMARY, read out of the shipped FBX binaries in `~/Games/reincarnated-godot/Assets/Synty/polygon-explorer-kit/SourceFiles/Characters/`:
  the Explorer Kit character rig has **no `weapon_*`, `prop_*` or `ik_*` bone of any kind**, and **only
  three finger chains per hand** (thumb, index, and one merged `finger_0N` for the rest). Casing is
  inconsistent (`Hand_L` but `lowerarm_l`) — a name-matching hazard. So the Synty characters drax has are
  in the same position as our Meshy rig, one step better on fingers.
- `Prop_R` / `Prop_L` / `ItemR` as published bone names: **NOT FOUND** in any vendor documentation. The
  only *documented* commercial prop-bone conventions are Epic's `weapon_r` / `ik_hand_weapon` /
  `ik_hand_gun` and Synty's unnamed prop bone.
- Mixamo's bone list: **NOT FOUND** — every Adobe/Mixamo doc URL returned 403 or 404 and the Internet
  Archive is blocked in this environment. **We cannot confirm from a primary source whether the Mixamo
  rig has finger or prop bones**, and this report will not assert it from memory.

**How mocap captures a prop — and it is a single bone, by definition.**

- **Vicon Shogun**, VERIFIED — [Create props](https://vicon-help.atlassian.net/wiki/spaces/Shogun111/pages/13207098/Create+props):
  *"In Shogun, a prop is a rigid object, such as a single bone system. Whereas a multi-segment prop is
  not a rigid object and would have more than a single bone, so it is defined as a subject."* Minimum
  **four markers**; *"Place the markers across the prop object to reach the extremities as far as
  possible"*; *"Avoid placing them in a straight line and/or on the same plane"*; *"Avoid placing markers
  symmetrically"*; and *"Prevent marker swaps by avoiding placing prop markers too close to the hands."*
  Crucially, **marker selection order defines the prop's axes**: *"The main axis (X) is defined by the
  first and second selected markers… The Y-axis pointing direction… tries to match the vector running
  from the first selection to the third selected marker"*
  (VERIFIED — [Shogun Post `rigidBody`](https://help.vicon.com/space/ShogunPost119/850468105)).
  Shogun Live adds: *"Props held by a subject (for example, an actor holding a sword) are better tracked
  using this pipeline"*
  ([object tracking](https://vicon-help.atlassian.net/wiki/spaces/Shogun113/pages/84218813/Understand+object+tracking+in+Shogun+Live)).
- **OptiTrack Motive**, VERIFIED — [Rigid Body Tracking](https://docs.optitrack.com/motive/rigid-body-tracking)
  and [Rigid Body properties](https://docs.optitrack.com/motive-ui-panes/properties-pane/properties-pane-rigid-body):
  *"At least three markers are required"*, *"recommended… 4 ~ 12"*, *"markers should be placed
  asymmetrically"*, *"The pivot point or bone of a Rigid Body is used to define both its position and
  orientation"*, and *"Unlike Skeletons or Trained Markersets, Rigid Bodies are comprised of a single
  bone"* — with **Rotation Offset** and **Translation Offset** as the calibration knobs.
- **Xsens / Movella MVN**, VERIFIED — [MVN User Manual](https://www.xsens.com/hubfs/Downloads/usermanual/MVN_User_Manual.pdf)
  § 7.2.10: prop types are *"crutch, sword, gun, golf club, generic"*; one tracker per prop, four props
  max. **And the manual states the edge-alignment calibration directly**: *"mount the prop tracker on the
  flat side of a sword with one axis aligned with the blade of the sword. Then, the orientation of the
  motion tracker can be set according to the natural orientation of the physical prop when holding it
  while in an N-pose."* **The industry solves edge alignment at capture time, by physically aligning an
  axis to the blade and calibrating against a known pose.** That is the analogue of fitting our mount's
  roll against a known guard pose (§ 6.2).
- **Important negative, and it matters if we ever buy prop mocap:** MVN exports props to **C3D only**, as
  three labelled points (`origin`, `tip`, `extra`); its FBX/MVNX exports are the 23-segment body model
  with **no prop segment**. And OptiTrack's FBX doc describes rigid bodies as 6-DoF data at their origin,
  **not** as bones inside the skeleton hierarchy. So *"prop mocap hands you a weapon joint in the FBX"*
  is true in Vicon/OptiTrack *terminology* but **not established for either vendor's FBX export**. NOT
  FOUND. Anyone sourcing prop mocap must verify the export path, not the marketing.

### Q2 — Authoring melee attacks: who does which, and what works for a small team

**This is the thinnest section in the report, and I want that stated plainly rather than padded.** The
session's WebSearch budget (200 calls, shared across all four research passes) was exhausted before the
tool survey completed, so the following is what I can stand behind. **Cascadeur's prop/weapon support and
the SMPL-family research's handling of held objects are NOT CONFIRMED here** — see § Part 7 gaps 11–12, and
treat them as open.

**What the record does establish, and it is the part that matters most for us:**

**Weapon-first authoring is a named professional practice, not an exotic idea.** Eben Bradstreet, game
animator, in a *Game Developer* feature co-authored with a HEMA instructor (VERIFIED —
[Art of War](https://www.gamedeveloper.com/art/art-of-war-animating-realistic-sword-combat)):

> "**the weapon leads the motions, just like your IK target leads your animation.**"

And Unity names the mechanism in its own docs (VERIFIED —
[MultiReferentialConstraint](https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/MultiReferentialConstraint.html)):

> "you could configure a character's hand to sometimes control the motion of a prop, and **the prop to
> sometimes control the motion of the hand**." … "The movement of the **Driving** object influences all of
> the other Reference Objects as if it were their parent."

That is weapon-first authoring as a shipped engine feature: designate the *weapon* as the driving object
and the hands follow. Epic's equivalent is Two Bone IK per arm with a hand-IK weight
(§ Q1), and Kubold's practical form is *"snap the effector to the barrel."*

**What that means for a small team, and for us specifically.** The two halves compose:
- The *arm* motion is cheap to source — the Meshy library has 174 `Fighting` clips (§ Part 4), and mocap
  retargeting is a solved part of our pipeline.
- The *weapon* motion is what nobody can give us, because no source clip was authored holding our axe. So
  the weapon channel is the part we must author ourselves — which is precisely the channel rank 1 creates.

**INFERENCE (mine):** the small-team answer is therefore **hybrid, not either/or** — library mocap for the
body, hand-authored keys for the weapon bone. That is far cheaper than full keyframe authoring and far more
controllable than pure retargeting, and it is the only split that puts authoring effort exactly where the
information is missing. It is also what rank 3 describes.

**Prop capture, for completeness:** if we ever did capture with a physical prop, the mocap vendors treat the
prop as a single rigid bone and give you explicit rotation/translation offsets to calibrate it (§ Q1 —
Vicon, OptiTrack, Xsens). Xsens even documents aligning a tracker axis to a sword's blade and calibrating
in an N-pose — the physical analogue of rank 2a. **But the FBX export path is not established for any
vendor** (§ Part 7 gap 7), so this is not a near-term option.

**Not established in this pass** (honest NOT FOUNDs): Cascadeur's AI feature set, prop support, and custom-
skeleton FBX round trip; Move.ai / DeepMotion / Rokoko Vision prop and finger support; whether WHAM, GVHMR,
TRAM or any 2025–26 successor recovers a held object; and any published source on authoring for a rig with
no finger bones (§ Q4 reaches the same conclusion from the LOD-budget side instead).

### Q3 — Dual-wield, spin attacks, and keeping the edge leading

**The closest documented analogue to our entire pipeline is Diablo II, and it is a primary source.**
Erich Schaefer (Blizzard North co-founder, D2 art director), *Game Developer*, Oct 2000 —
VERIFIED, [Postmortem: Blizzard's Diablo II](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-):

> "Almost all of *Diablo II*'s in-game and cinematic art was constructed and rendered in 3D Studio Max"
> … "An in-house tool would render the files from many different angles (**eight for all monsters, 16 for
> player characters**), and export them in the file formats used in the game."
> … "**Each part of a character's armor (the head, the torso, the legs, each arm, a weapon, and a shield)
> was rendered separately** with in-house tools."
> … "While the player characters are only seen in the game as **75 pixels tall**, all were modeled and
> rendered in high resolution."
> … "Monsters have 14 possible classifications of animation, from basics such as Walk, Attack 1, and
> Death, to the seldom-used Block, Run, and four Special modes."

Four things we should take from this and one we should argue with:

1. **We are at nearly twice D2's on-screen register.** D2 player characters were **75 px**; ours are
   **140 px**. Every readability budget below is more generous than D2's, not less. This is the single
   most reassuring number in the report.
2. **D2 rendered the weapon as its own layer, composited per frame** — VERIFIED above. Community
   reverse-engineering of the `.cof` format shows the draw order is resolved per
   `[direction][frame][layer]`, not once per animation
   ([OpenDiablo2 `cof.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2fileformats/d2cof/cof.go)),
   with 16 layer slots `HD TR LG RA LA RH LH SH S1–S8`
   ([`composite_type.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2enum/composite_type.go)).
   Paul Siramy's *Extracting Diablo II Animations* gives the reason, and it is a warning for us
   (COMMUNITY — [archive.org](https://archive.org/stream/ExtractingDiabloIIAnimations/Extracting%20Diablo%20II%20Animations_djvu.txt)):
   > "When the Player is facing West, you first see his Shield, and the rest of the body is behind. But
   > when facing East, the Shield is now the one that is behind."
   **We render from 3D with a real depth buffer, so we get this for free** — but it names the class of
   defect to watch for in any cell where we composite rather than render.
3. **D2 did NOT mirror for dual-wield. It minted a weapon class per hand-action pairing.** Four of
   fifteen `WeaponClass.txt` codes exist only to say what each hand is doing: **`1js` Left Jab Right
   Swing, `1jt` Left Jab Right Thrust, `1ss` Left Swing Right Swing, `1st` Left Swing Right Thrust**
   (COMMUNITY, two independent sources — Siramy above and
   [OpenDiablo2 `weapon_class.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2enum/weapon_class.go)).
   And the left-hand attack got **its own animation mode** (`S3` = *"a Swinging attack with the weapon in
   the Left hand"*), not a mirrored right. Siramy: *"the Dual-Weapon ability is an exception among the
   Player Characters animations."* **The reference implementation of our exact genre treated dual-wield
   as a distinct authored set, and the cost was real** — the Barbarian alone has **149 `.cof` files**.
4. **Release frames were data, not code.** Each `AnimData.d2` record carries a per-frame event map whose
   values are exactly `None | Attack | Missile | Sound | Skill`
   ([`events.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2fileformats/d2animdata/events.go)).
   `Attack` is melee contact; `Missile` is projectile release. **Our RELEASE marker is the same idea,
   independently arrived at.** D2 ran at **25 fps** (`speedDivisor = 256`, `speedBaseFPS = 25` —
   [`animdata.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2fileformats/d2animdata/animdata.go)).

**Modern engines take the opposite position on mirroring, and ship it as first-class.** VERIFIED —
[Mirroring Animation in UE](https://dev.epicgames.com/documentation/en-us/unreal-engine/mirroring-animation-in-unreal-engine):
*"mirroring within Unreal Engine provides a way to create mirrored animations without needing to manage a
second copy"*, and it mirrors *"not only your Animation Sequences, but also curves, sync markers, and
Notifies."* Two documented pitfalls that bear on us:

- *"In order to have a fully mirrored character, it is necessary that the table contains **most skinned
  bones, including central bones** like pelvis, spine, neck, and head"* — mirroring is not free, and a
  partial table produces a partially mirrored character.
- Epic ships an explicit escape hatch: **`Is Triggered By Mirrored Animation`** in the Notify Blueprint.
  **The engine concedes that a mirrored clip needs different downstream behaviour** — which is exactly
  our asymmetric-weapon problem: a mirrored sword clip driving an axe needs the axe's own edge and mount.

**INFERENCE (mine, from the two above):** for our barbarian, mirror the *body motion* to get the
left-hand strike cheaply, but **do not mirror the weapon channel** — author `weapon_l`'s rotation
separately, because the axe is not a mirrored sword. The mirror buys the arm; the weapon bone pays for
the blade. This is the synthesis of D2's "author per pairing" and Epic's "mirror plus a branch."

**Whirlwind — and a finding that challenges our 8-direction plan.** COMMUNITY, Phrozen Keep (Nefarius),
[Character Graphics Conversion Tutorial](https://d2mods.info/forum/kb/viewarticle?a=174):

> "Characters use 16 directions, however we dont need 16 directions for the paladin, as he uses no skills
> that require 16 directions in their sequences." … "in case you convert the barbarian you would need to
> do so, as **whirlwind uses 16 directions in its attack sequence**."

**The one D2 skill that forced the full 16-direction ladder is the Barbarian's Whirlwind** — the exact
move we are about to build at 8.

**But the contradiction resolves, and in our favour. INFERENCE, and I want it challenged:** D2 baked
*facing* into the direction index, so a spinning character had to step through direction slots and needed
16 of them to look smooth. **Our spin's rotation lives inside the frame sequence, not in the direction
index** — the root yaw is animated, and the cell's facing only sets where the spin starts. So our
angular resolution during the spin is *frames per cycle*, not *cells*, and 8 cells at N frames gives us
8N distinguishable orientations, not 8. **If anything, a pure single-revolution spin needs only ONE
rendered cell** (§ 3's phase-shift identity). The D2 constraint is an artefact of sprite-indexed facing
and does not transfer. **This should be verified with a render before it is relied on.**

Whirlwind's other documented properties, all COMMUNITY but consistent across sources:

- It is a **stitched sequence, not a clip** — `anim = SQ`, `seqnum = 10`; Double Swing is `seqnum = 11`
  ([Skills.txt guide](https://d2mods.info/forum/kb/viewarticle?a=350)). Looping is a data field
  (`seqinput` = *"the interval to wait before looping the sequence"*).
- It is flagged either-or-both-weapons at the data level: `weapsel = 2` means *"it can either use the
  Right or the Left or Both weapons (used by Whirlwind)."*
- **Hit cadence is decoupled from the visual revolution rate.** *"the game checks for a hit on a target in
  range at the 4th and 8th animation frames"*, then subsequent intervals depend on weapon speed —
  1-handed 12/10/8/6/4 frames, 2-handed 14/12/10/8/6/4
  ([fextralife](https://diablo2.wiki.fextralife.com/Whirlwind), [diablo2.io](https://diablo2.io/skills/whirlwind-t4197.html)).
  And when dual-wielding, *"both weapons try to score a hit… the game does a hit-check for each weapon."*
  **This is the design lesson for our Whirlwind: author one clean revolution for the eye, and drive hits
  from an independent schedule.** It matches our existing "rates applied at playback" architecture.
- The exact frame count of D2's Whirlwind animation, and any developer statement that it is one
  revolution looped: **NOT FOUND**. Also **NOT FOUND**: any developer commentary anywhere on making a
  continuous spin *read* — searched Diablo II/III/IV, PoE Cyclone, Warframe, Dark Souls/Elden Ring, GDC
  Vault, and Blizzard news. The nearest official statement is generic (Luis Barriga, D4 game director:
  *"Combat only feels visceral thanks to carefully crafted animations and visual effects"* —
  [D4 Quarterly Update, June 2021](https://news.blizzard.com/en-us/article/23665024/diablo-iv-quarterly-updatejune-2021)).
  **The spin-readability question is genuinely unanswered in the public record.** Our own SB-1 rotor flag
  (§ 3) may be the best evidence anyone has.

**Edge alignment — how it is actually done.** There is **no GDC talk and no engine doc** that exposes an
"edge normal" on a weapon socket (NOT FOUND, both). What the record does contain is better, because it is
a concrete technique:

- **Blade edge is defined by locators placed along the edge, ordered tip→base.** VERIFIED — Kiel Figgins
  (professional animation TD), [`kfSwordSwipe`](https://www.3dfiggins.com/Store/Support/SwordSwipe/):
  *"Create two or more locators and align them to the edge of the your sword's blade. If the blade is
  straight two should be fine, if it's curved you can create more locators… select them in order from tip
  to base."* **The edge is a marked curve on the mesh, not an axis of the weapon's transform.** We already
  have the marker (`axe_edge`, § 1.6); this says use two or more.
- **Engines consume a base/tip socket *pair*, and the pair's separation defines the trail's width.**
  VERIFIED — [Animation Notifies](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine):
  *"You can specify a separate bone or Socket here for each property, which are used to define the attach
  points for the AnimTrail. This also defines the trail's default width, based on the distance between
  these two attach points."* The same pair is used for hit tracing along the blade, sampling the arc
  *between* frames (COMMUNITY — [Remy Jaspers, melee tracing in UE5](https://www.remyjaspers.com/blog/melee_tracing_ue5/):
  ten traces *"spread over the length of the character's sword"*, from each previous-tick position to the
  current one). **Given our 79 px single-frame step on `attack` (§ 1.5), inter-frame arc sampling is not
  optional if we ever do 3D hit detection.**
- **The craft source, from an article co-authored by a HEMA instructor.** VERIFIED — Eben Bradstreet
  (animator) + John Clements (ARMA), *Game Developer*, Dec 2012,
  [Art of War: Animating Realistic Sword Combat](https://www.gamedeveloper.com/art/art-of-war-animating-realistic-sword-combat):
  - Clements: *"there are **16 possible lines of striking** for the typical double-edged European
    longsword."* (Games typically use a handful.)
  - Bradstreet on chaining: *"Despite the change in vector for every strike, John always returns to Vom
    Tag before striking again"* — which lets a sequence end *"without popping into an idle pose."*
    **This is the guard-pose argument, from craft: strikes should begin and end at a named stance.** It is
    also precisely what `Combat_Stance` gives us.
  - **Bradstreet, and this is the single most important sentence in the commission for our purposes:**
    > "**the weapon leads the motions, just like your IK target leads your animation.**"
    A working professional animator describing melee authoring states weapon-first as the natural frame.
  - On the trailing hand: *"The right hand (or the leading hand) indeed goes just below the cross-guard.
    The left hand should grip the weapon by the pommel… The sword is a lever, and your leading wrist is
    the fulcrum."* And the rig payoff: *"If a video game character grips the pommel with its trailing
    hand, the resulting animation will have **fewer problems with deformation around the wrist, less
    clipping** between the sword's mesh and the character's mesh."* **Directly transferable to the
    sorceress's staff: put the trailing hand at the extreme end of the shaft, not mid-way.**
- Mordhau, Chivalry 2, Kingdom Come, Hellish Quart official animation write-ups: **NOT FOUND**. A GDC
  talk specifically on dual-wield authoring or edge alignment: **NOT FOUND**.

### Q4 — Hand poses on a rig with no finger bones

**Recommendation up front: keep the grip morphs. Do not re-rig for fingers.** The evidence says fingers
are the first thing that stops mattering at our register, and our current solution is the right one.

**The industry's own LOD ordering settles it.** *"LOD bone reduction typically removes fingers first, then
twist bones, then toe bones, and simplifies the spine"* (VENDOR —
[MoCap Online, skeleton hierarchy guide](https://mocaponline.com/blogs/mocap-news/skeleton-hierarchy-animation-guide);
same page's bone budgets: 30–50 *"fast to evaluate, low memory, but limited deformation quality"*, 60–100
*"the sweet spot… includes twist bones and basic fingers"*). **When studios need to cheapen a character at
distance, fingers go first.** Our figure is 140 px. At 77.8 px/m a finger is under 1 px wide. **INFERENCE:
a finger bone cannot produce a visible difference at our register; a closed-fist silhouette can, and the
grip morphs already deliver it.**

What the tools would give us if we did re-rig, for the record:

| tool | finger bones? | prop/weapon bones? |
|---|---|---|
| **AccuRIG** (Reallusion, free) | **yes**, count configurable | deliberately **excluded** |
| **Auto-Rig Pro** (Blender, paid) | **yes**, 5 fingers, 2–3 phalanges, + a fist controller | **yes, explicitly** |
| **Meshy** (ours) | not stated in docs | **no** |
| **Tripo** (ours) | not stated in docs | not stated |
| Mixamo | not confirmable — all Adobe doc URLs 403/404 | not stated |
| Rigify | not confirmable — Blender docs 403 | — |

- AccuRIG, VERIFIED — [AccuRIG](https://www.reallusion.com/auto-rig/accurig/): *"Finger Count can be
  designated prior to the character rigging process"*, and notably *"**AccuRIG differentiates the hand
  from the props being held so auto-generated bones don't extend into inanimate objects**"* — i.e. the
  free auto-rigger that best handles fingers explicitly *refuses* to rig the prop. It would not solve our
  actual problem.
- **Auto-Rig Pro is the one tool that does both**, VERIFIED — [Auto-Rig Pro docs](https://lucky3d.fr/auto-rig-pro/doc/auto_rig.html):
  *"Add fingers (thumb, index, middle, ring, pinky)"*; *"Optionally, a fist controller can be added to
  hands. This controller is meant to blend the fingers into a predefined fist pose"*; and — the line that
  matters — ***"Adding your own new bones (custom bones) for props, clothes, hair or anything required is
  fairly simple and straightforward."*** If we ever want a fingered rig *and* prop bones in Blender, ARP
  is the documented route. It is not needed for the weapon-bone fix, which our own scripts can do (Part 2).
- Meshy's own docs confirm the constraint we already live with, VERIFIED —
  [Meshy rigging](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging): *"Humanoid and quadruped
  characters. **Props, buildings, and vehicles cannot be rigged**."* The docs page does **not** enumerate
  bones or promise finger bones; the "spine, limbs, fingers" claim lives only on marketing pages. **So
  "newer Meshy rigs may have fingers" is unverified — do not plan on it.**
- **The blend-shape route has an official Blender Studio tool, and its documented example is a fist.**
  VERIFIED — [Pose Shape Keys](https://studio.blender.org/tools/addons/pose_shape_keys): *"Author finger
  correctives 24-at-a-time"*, with the workflow benefit that it *"enables a workflow where you can
  continue iterating on your vertex weights and bone constraints after you've already created your shape
  keys, without having to re-sculpt those shape keys."* **Caveat, and it is real:** the documented
  workflow assumes finger bones exist to *drive* the shapes. Our grip morphs are driven by an equip state
  instead — a sensible adaptation, but **NOT FOUND** as a documented variant. We are ahead of the
  documentation here, not behind it.
- The orthodox answer to "no weapon bone" in the absence of one is a socket — but as § Q1 establishes, a
  socket is static and our problem is dynamic.

### Q5 — Readability of melee at a top-down / isometric ARPG camera

**Blizzard's own answer to this exact question, from the Diablo IV dev blog, is VFX that tracks the
weapon.** Daniel Briggs, Lead VFX Artist, VERIFIED —
[D4 Quarterly Update, December 2021](https://news.blizzard.com/en-us/article/23746639/diablo-iv-quarterly-updatedecember-2021):

> "gameplay readability is muddied, particularly in dark environments where **a weapon swing would
> naturally be hard to see**." … "AOEs expand outward with time, and **melee swings match the motion of
> your weapon**." … "we have revamped the way we apply hit effects to monsters, so impacts flow with the
> direction of a spell or melee attack." … "we can now **animate target areas (what we call payloads) over
> multiple frames**, which allows us to line up the animated target areas with the animated VFX."

Three things: Blizzard states plainly that a melee swing at this camera *is naturally hard to see*; their
remedy is an effect that follows the weapon's own motion; and their hit-response direction is derived from
the attack's direction. **All three are things we should copy, and the second one is the weapon trail.**

**Diablo III's art direction treats the fixed camera as an asset, not a constraint.** Christian Lichtner,
GDC 2012, session abstract VERIFIED — [The Art of Diablo 3](https://gdcvault.com/play/1015306/The-Art-of-Diablo):
*"Our aim for Diablo3 was to create a painterly stylized world that **takes full advantage of its fixed
camera**."* Press coverage of the same talk (VERIFIED — PRESS,
[gameranx](https://gameranx.com/features/id/5666/article/gdc-2012-the-art-of-diablo-iii/)): *"Important
gameplay elements need to be conveyed as quickly as possible, allowing players to understand and react
without unnecessary confusion"*; *"Characters and enemies need distinctive silhouettes"*; and the
pipeline consequence — *"Since the camera angle remains the same throughout the entire game, Blizzard was
able to develop special 2.5D models that look amazing with very few polygons."* **We are running the same
trade, one step further: our camera is fixed enough to bake to sprites.**

**Riot has published more on fixed-top-down readability than anyone, and one line is directly about our
8-direction problem.** VERIFIED — [Clarity in League](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/):

> "Silhouettes are the single most important thing for champion recognition in League." … "**It should be
> clear which direction a champion is facing from their silhouette alone.**"

**That is the acceptance test for our 8 direction cells**, stated by a studio that ships at this camera:
*can you tell which way he is facing from the silhouette?* It is also a test we can automate — we already
compute silhouettes (`19_silhouette.py`, `25_clip_sil.py`).

**And Riot's senior animator gives the craft answer to the foreshortening I measured in § 3.** Rory
Alderton, Senior Animator, Riot Games, VERIFIED —
[interview](https://www.animationcareerreview.com/articles/riot-games-senior-animator-rory-alderton-discusses-league-legends-animation-process):

> "**We push all our up and down motions a lot** especially during run cycles to show more weight from the
> top-down perspective." … "We also try to angle everything slightly upwards like champion heads so you
> can see a bit more of the face from the game view." … "it's crucial to get some super broad exaggerated
> posing into these moments so it feels satisfying for the player."

**Synthesis, and this is the most actionable number in the report. INFERENCE from Alderton's stated
practice plus my § 3 measurement:** vertical motion loses exactly `cos(52.9535°) = 0.603` of its length on
screen. Alderton's remedy is to *push up-and-down motion*. The principled amount is the reciprocal:
**exaggerate vertical amplitude by ≈ 1/0.603 ≈ 1.66× to restore apparent vertical travel to its true
magnitude.** Use that as the starting dial, not a law — but it turns "push it a lot" into a number we can
set and then measure.

Alderton also supplies a timing budget from a shipped top-down game: *"Our animations have to be very
snappy and responsive since **the cast times range from .25 to 1.0 seconds** on most abilities."*

**The anticipation/strike/recovery structure, from the most authoritative possible source.** Capcom's own
Street Fighter V column, VERIFIED — [Shadaloo C.R.I.](https://game.capcom.com/cfn/sfv/column/131432?lang=en):
*"There are 3 parts to an attack. 1 Startup 2 Attack Active Frames 3 Recovery Period"*, with worked
examples *"1 Startup 2/Active 4/Recovery 5"* and *"2 Startup 3/Active 4/Recovery 5"*. The 12 principles
are Johnston & Thomas, *The Illusion of Life* (1981); anticipation *"is used to prepare the audience for
an action"*, and exaggeration exists because *"animated motions that strive for a perfect imitation of
reality can look static and dull"*
(VERIFIED — [12 principles](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)).
Richard Williams' *Animator's Survival Kit* and Swink's *Game Feel* could not be fetched — **NOT FOUND**,
and deliberately not paraphrased from memory.

**The anticipation trap, stated twice by two independent sources — worth heeding given our RELEASE marker
architecture:**
- *"Be careful with anticipation! While it adds weight to your attacks, it also introduces a slight delay
  before the attack lands."* (VERIFIED — [GDQuest, juicy attack](https://www.gdquest.com/library/juicy_attack/))
- *"Anticipation and recovery frames add realism but can make sluggish gameplay. Too much anticipation
  will give a nasty feeling of input lag… Too much recovery will make your character feel sticky and
  vulnerable."* (VERIFIED — [SLYNYRD, Pixelblog 9: Melee Attacks](https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks))

**Our 79 px single-frame step has a name in the literature, and the literature names the fix.** Christoph
Lendenfeld, *Smearframes in Video Games* (master's thesis, FH Hagenberg, 2018), VERIFIED —
[PDF](https://theses.fh-hagenberg.at/system/files/pdf/Lendenfeld18.pdf):

> "It is especially common in **sword swings**, because the sword would usually swing in a big arc to
> create clearly readable poses. **Without motion trails however, that leads to strobing as the attack is
> usually very fast and the sword in comparison very thin.**" … "**If the distance on screen is too big
> between frames, the object needs to be stretched to prevent strobing.**"

That is our `attack` clip described from the outside. The thesis then gives us the implementation, and it
is cheap for a 3D-to-sprite pipeline:

- *"a motion trail is **not very view dependent**. Since the original object is not deformed and the newly
  spawned motion trail **can just be a 2D plane**, any ugly deformations can be avoided."* — **a trail
  plane works in all eight cells without per-cell authoring.**
- Scope discipline: *"when a fast movement of an arm occurs it is usually enough to smear only the hand as
  opposed to the whole arm. The hand alone creates enough guidance for the eye."*
- Duration: a smear is *"designed to be felt rather than seen. That is achieved by holding the smear for
  only one or two frames in a 24 frames per second movie."*
- Lead-in: *"it is often not enough to indicate the arc only with a smearframe. **Usually it is best to
  start the arc in the frames preceding the smear** to improve readability."*
- Edge craft: *"the edges need to have their own spacing cycle. That means that they should accelerate and
  decelerate steadily."*
- The honest limit: *"**If those poses do not read** or do not tell the intended story **a smearframe will
  not help.** So smearframes are not a magical solution to every animation problem."*
- Contrast, which pairs with Briggs' "dark environments": *"In low contrast, movement is just generally
  harder to register, so having a smearframe that blends into the background will not help."*
- And a Blizzard animator conceding the difficulty, David Gibson (Overwatch), GDC 2016, quoted with
  timestamp by the thesis: *"We tried to do this with ingame assets as well […] smearframes are kind of
  tricky to pull off in game-space […]"*

**The best modern precedent for "3D authored to read as few-frame 2D" is Guilty Gear Xrd**, and it is a
primary GDC handout. Junya C. Motomura, Arc System Works, GDC 2015, VERIFIED —
[official handout PDF](https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf):

> "we took a style called 'Limited Animation' … it focuses more on tricking the eyes with less frames."
> … "**Having the poses interpolate between key frames, makes it look smoother, but at the same time,
> makes it look more 3D. So we just stopped using interpolations between key frames.**" … "Every frame now
> is a key frame, and the animator poses the character in the best way possible." … "Because we were going
> to have less frames per animation, we knew we had to **add more information to each frame**." … "Limbs,
> hands, and feet get a lot of **scale animation to exaggerate the perspective**." … "**Expressiveness
> over accuracy.**"

**This is a direct challenge to one of our assumptions, and I want it on the record.** Our pipeline
authors *one clean cycle per state* and applies rates at playback — i.e. we are producing smooth
interpolated motion and then sampling it. GGXrd's finding is that at low frame counts, **interpolation is
what makes it read as 3D**, and they removed it. **INFERENCE:** we should test whether our attack cells
read better with per-frame hand-chosen poses (and exaggerated scale on the weapon at the extremes) than
with a uniformly sampled smooth cycle. Not a recommendation yet — a hypothesis with a strong source, and a
cheap A/B.

**Cost anchor for a sprite ARPG, so nobody is surprised.** COMMUNITY —
[Lilura1, Baldur's Gate retrospective](https://lilura1.blogspot.com/2019/10/Baldurs-Gate-Retrospective-Review-Graphics-Backgrounds-Sprites-and-Animation.html):
*"about 50 frames need to be drawn for Sarevok's attack swing alone"*, covering front, rear and one side
(mirrored for the other); *"there are 616 frames of animation just for Sarevok"*; *"There are over 100,000
frames of sprite animation in Baldur's Gate."* And the consequence at small size: *"most of the sprites in
Baldur's Gate lack detail because they are quite small."*

**Hit-stop — and a citation discrepancy I am flagging rather than averaging.** The only concrete sourced
figure is **1–4 frames**: *"Hit stop: a 1–4 frame game pause (zero time) on successful hit. Even 1–2
frames of hit stop dramatically improves the sensation of impact"* (VENDOR —
[MoCap Online, sword/melee guide](https://mocaponline.com/blogs/mocap-news/sword-melee-animation-guide)).
The widely repeated *"≈0.2 s"* attributed to Jan Willem Nijman's *The Art of Screenshake* traces only to a
student blog, **not to any transcript**. These differ by an order of magnitude (≈17–67 ms vs 200 ms).
**Do not specify a hit-stop value off this research — measure it.** Two corrections worth carrying:
*The Art of Screenshake* was **INDIGO Classes 2013, not GDC** (VERIFIED —
[archive.org](https://archive.org/details/the-art-of-screenshake)), and the 0.2 s number is unverified.
A named developer-educator's implementation is on the record, though: *"I very briefly slow down the
entire game when the sword hits the enemy to make the hit feel harder"*, via `Engine.time_scale`, layered
with *"a blink animation that briefly turns the sprite white"* and *"Smearing, creating a trail that
follows the attack"* (VERIFIED — [GDQuest](https://www.gdquest.com/library/juicy_attack/)).

**Gaps worth naming:** no developer anywhere states an on-screen character height in pixels for an ARPG
camera — **NOT FOUND**, so our 140 px has no external benchmark except D2's 75 px. Path of Exile, Hades,
Last Epoch, Torchlight, Wolcen and Battle Chasers yielded **no** primary dev statements on melee
readability. The aphorism *"if it doesn't read in silhouette it doesn't read"* is **NOT FOUND** in any
primary source; Riot's *"silhouettes are the single most important thing"* is its nearest verified
equivalent.

### Q6 — How weapon motion is verified, and what we should build

**The headline is a negative result, and it justifies building our own instruments rather than shopping
for them.** **NOT FOUND**: any published studio animation-QA checklist with explicit clipping /
interpenetration / arc pass items; any engine or tool that ships an automated weapon-interpenetration
check; any primary-source account of turntable or contact-sheet review practice. What the record gives us
is *where you would write such a check*, plus one academic paper naming the defect classes.

**Where studios write these checks: Unreal's Animation Modifiers, and the shipped example is exactly the
shape of check we need.** VERIFIED —
[Animation Modifiers](https://dev.epicgames.com/documentation/unreal-engine/animation-modifiers-in-unreal-engine):
*"a type of native or Blueprint Class that enable users to apply a sequence of actions to an Animation
Sequence or Skeleton asset"*; batch scope is set-wide — *"When applying an Anim Modifier to a Skeleton,
the modifier is applied to all Animation Sequences that are based on the Skeleton"*; and the documented
example is a **per-frame geometric detector**: *"creating automatic foot sync markers by pin-pointing on
which frames the right or left foot is place on the ground… Animation Sync Markers can be added to frames
where a bone is at its lowest point."* **Swap "foot at its lowest point" for "edge at its most forward
point" and that is our strike-frame detector — which `14_axe_assert.py` already implements.** We are on
the documented path; we just need to make it standing rather than ad hoc.

**Golden-image comparison, with perceptual tolerance as a first-class control.** VERIFIED —
[Screenshot Comparison Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine):
a **Ground Truth** baseline is *"the version that you know is correct"*; tolerances are configurable as
*"RGBA Channels, Min Brightness, and Max Brightness"* plus **Maximum Global Error** and **Maximum Local
Error**, explicitly to absorb anti-aliasing and rendering-technique variation; and the triage policy is
stated: teams *"review the failures and make the correct decision, which might be to update the
screenshot if a feature change has necessitated the updated screenshot or enter a bug report."*
**Our 8-direction cells are already images. A golden-image gate with a local-error tolerance is the
cheapest possible regression net for weapon motion, and it needs no new rendering.**

**Rule validation in CI.** VERIFIED —
[Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine):
validators derive from `UEditorValidatorBase` (C++, Blueprint, **or Python**) implementing
`CanValidateAsset` / `ValidateLoadedAsset`, and *"Both types of validation are run by CIS, on asset save
(enabled by default), and through menu options"*, plus a headless
`-run=DataValidation` mode. **This is what `21_lint_export.py` already is.** The pattern is right; the
rule set needs extending (§ 6.6).

**The defect classes have names and metrics in the literature.** VERIFIED — Rekik, Wuhrer, Hoyet, Zibrek,
Olivier, *Quality assessment of 3D human animation: Subjective and objective evaluation*
([arXiv 2505.23301](https://arxiv.org/html/2505.23301v1)):
- Interpenetration is *"one of the most common errors in VH animation, where different body parts
  inappropriately overlap or penetrate each other, compromising the physical plausibility of the 3D
  model."*
- Foot-skate is decomposed: *"either foot 'sliding', where the foot slides along the floor while
  maintaining contact, or 'moonwalking', where the foot slides backwards."* (We already measure
  `foot_slide_mean_m` / `foot_slide_max_m`.)
- Objective toolkit: **Chamfer** and **Hausdorff** distance, plus a foot-contact-difference feature.
- **And the caveat that should govern how we use any of this:** the paper finds human perception studies
  more reliable than individual objective metrics. **An automated metric is a triage filter, not a
  verdict.** Matt's eye stays the gate; the instruments decide what reaches it.

**Studio talks confirming automated validation is the norm at scale** (abstracts verified, videos behind
membership): Ubisoft Montreal, *Assassin's Creed Origins: Monitoring and Validation of World Design Data*
(GDC 2018) — *"it is practically impossible to validate the integrity and functionality of world data on a
timely basis using traditional methods"*
([GDC Vault](https://gdcvault.com/play/1025452/-Assassin-s-Creed-Origins)); Ubisoft Reflections,
*Automated Testing: Using AI Controlled Players to Test 'The Division'* (GDC 2019)
([GDC Vault](https://gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled)); Massive,
*Building a DCC and Project Agnostic Animation Pipeline* (GDC 2023)
([GDC Vault](https://www.gdcvault.com/play/1029332/Technical-Artist-Summit-Building-a)).

---

## Part 6 — Ranked recommendation

### 6.0 On the conductor's hypothesis: right, and incomplete in one specific way

The hypothesis — *"the weapon's angle is whatever the wrist does in clips authored for other weapons or
none, and there's no weapon bone to author the weapon's own motion"* — is **confirmed, and understated**.
It is worse than no weapon bone: the weapon is *skinned*, so there is no transform between hand and
weapon at all, and our own `socket_weapon2` docstring says the rest pose *"is the whole job."*

**But the hypothesis would, if taken as the complete diagnosis, leave one of the three defects unfixed.**
A weapon bone rotates the weapon *about the grip*. It cannot move the grip. And the grip is carried by the
shoulder and elbow — which is why `idle_armed` still shows a **239–285 px axe-head path** after the wrist
lock was tuned to its strongest setting (§ 1.5). **Defect (c), arc noise, is a source-clip and
arm-authoring problem, not an attachment problem.** Anyone who ships the weapon bone and expects the
waffle to be gone will be disappointed. Ranks 1–2 fix what Matt is complaining about *today*; rank 5 fixes
what he complained about *last time* and which is not actually fixed.

### Rank 1 — Add `weapon_r` and `weapon_l` to the base rig and rebind the weapons. **Do this first.**

**Why first:** verified end-to-end (Part 2), visually a no-op (4.02 × 10⁻⁷ m), and it is the precondition
for every other weapon-motion fix. Epic's own taxonomy describes this exact bone class as existing *"for
attaching weapons or props, while still being animatable as a Bone"*; a commercial sword-animation vendor
(Synty) ships one for the same reason.

**Steps:**
1. In the base-rig build step, insert `weapon_r` as a child of `RightHand` and `weapon_l` as a child of
   `LeftHand`, each **coincident with its parent** (copy head/tail/roll), `use_connect = False`,
   **`use_deform = True`**.
2. Add them to **the base rig, before any piece is exported**, so body, byrnie, mantle, bracers, helmet
   and both weapons all carry the identical 26-bone skeleton **in identical order** — `gear.gd` compares
   bone-name lists for equality (§ Part 2, integration requirement).
3. In `gearlib.socket_weapon2()`, change the final bind from `vertex_groups.new(name=bone)` to the
   weapon bone, and keep everything else — the rest-pose fit still does the placement, the weapon bone
   just makes it adjustable afterwards.
4. Exclude `weapon_r` / `weapon_l` from the SMPL-H retarget transport. Epic states the rule: *"Find the
   Root bone, any IK bones, any Weapon bones… and set them to Animation"* — the weapon bone's transform is
   authored data, not something to re-derive from a source skeleton that has no such joint.

**Cost:** low — hours, not days. Our scripts already do every operation involved.
**Risk:** low, and measured. The one real risk is the skeleton-order requirement in step 2; mitigate with
a lint rule (§ 6.6, check 1).
**Measure:** bone count 26 on every exported piece; `bones_match_body = true` in `gear.gd`'s report; the
rest-pose displacement of both weapons under 1 µm.

### Rank 2 — Fit the mount orientation, and retarget the wrist lock at a GUARD pose, not the idle. **This is the answer to Matt's sentence.**

Two changes, both cheap, both directly on the complaint.

**2a. Fit the mount's roll so the edge leads.** The manifest says `"ORIENTATION NOT FITTED"`; § 1.4 shows
**no clip has its edge within 45° of forward**. Solve for the single constant roll about the haft that
minimises |edge heading| across the *strike* clips (`attack`, `attack_chop`), which is where edge alignment
is load-bearing. From the measured medians (115° and 88°), a roll of roughly **−90° to −100°** brings both
inside ±45°. Fit it, don't guess it — and fit it against the strikes, not the idle. The industry does the
same thing at capture time: Xsens tells you to *"mount the prop tracker on the flat side of a sword with
one axis aligned with the blade"* and calibrate *"while in an N-pose."*

**2b. Change the wrist-lock target from the idle's angle to a guard angle, and take the guard from
`Combat_Stance`.** `27_armed_carry.py` says its target *"comes from the IDLE."* An idle is a carry pose.
Matt asked for a battle stance. **The Meshy library has `Combat Idel` / `Combat_Stance`, action_id 89**
(§ Part 4). Define the guard numerically by the predicate `axe_diag2.gd` already encodes — tilt 30–60° from
vertical, haft forward > 0, haft outboard > 0, head outboard > 0, |edge| ≤ 45° — and pick the target frame
from `Combat_Stance` by *lowest arm-travel into the strike starts*, which `axe_diag2.gd` also already
computes. The craft source agrees that strikes should start and end at a named stance: *"John always
returns to Vom Tag before striking again"*, which lets a sequence end *"without popping into an idle
pose."*

**Cost:** low. **Risk:** low; both changes are re-runs of existing scripts with different constants.
**Measure:** the acceptance predicate, per clip, as a table. **Target: every armed clip passes.** Today
none do.

### Rank 3 — Author the weapon channel per state. This is where rank 1 pays off.

With `weapon_r` / `weapon_l` in place, add a rotation track per clip:

- **idle / walk / run:** hold the guard angle from rank 2b. Because the weapon bone is authored and the
  wrist is not overridden, the arm keeps its natural motion while the weapon stays at guard — which is the
  thing a wrist slerp was approximating and could not achieve.
- **strikes:** author the weapon's angle through the swing so the **edge leads** — |edge| small and falling
  through the active frames, with the edge's most-forward frame as the strike. `14_axe_assert.py` already
  encodes the right definition, and its header already records why: *"THE STRIKE OF A CUT IS NOT A
  THRUST'S… The strike of a cut is where the EDGE reaches furthest forward."*
- **block:** the axe currently sits at **159.9° from vertical** (near-inverted). Author it upright.
- **Whirlwind:** author as **a constant local pose plus a uniform single-revolution root yaw**, with the
  weapons held out. This buys three things at once: the silhouette stays a humanoid with two arms out
  (answering the SB-1 rotor flag); the edge orientation is a *constant* in the local frame, so edge
  alignment is trivially correct for the whole revolution; and the § 3 phase-shift identity holds, so
  **all 8 cells come from one render** if N is divisible by 8 (use **16 or 24 frames**).
  **Hit cadence should not be tied to the revolution** — D2 ran WW's hit checks on an independent schedule
  (4th and 8th frames free, then weapon-speed intervals) and that composes cleanly with our
  rates-at-playback design.
- **Dual-wield alternation:** mirror the *body* to get the left-hand strike cheaply (Epic ships mirroring
  precisely so you avoid *"a second copy"*), but **author `weapon_l` separately** — the axe is not a
  mirrored sword. Epic's own `Is Triggered By Mirrored Animation` escape hatch is the engine conceding
  that mirrored clips need differentiated downstream handling; our differentiation is the weapon channel.
  Note the alternative D2 actually chose: distinct authored sets per hand pairing (`1ss` "Left Swing Right
  Swing" etc.) and a separate left-hand mode `S3`. **That is more faithful and much more expensive — 149
  `.cof` files for the Barbarian alone.** Mirror-plus-weapon-channel is the small-team version.
- **Sorceress staff:** bind the staff to `weapon_r`, and hold the **off-hand on the shaft with
  `TwoBoneIK3D`** (root `LeftArm`, middle `LeftForeArm`, end `LeftHand`, `target_node` = a `Node3D` under a
  `BoneAttachment3D` on `weapon_r` at the lower grip, with `pole_node`/`pole_direction` set so the elbow
  cannot flip). This is Epic's documented pattern (Two Bone IK per arm + hand-IK weighting) and Kubold's
  practical form (*"turn on the IK on the left hand and snap the effector to the barrel"*). Put the
  trailing hand at the **extreme end of the shaft**, not mid-way — the craft source gives the reason and
  the rig payoff: *"fewer problems with deformation around the wrist, less clipping."*
  **And plan the off-switch:** Epic warns that an IK-to-weapon setup needs *"extra steps to disable IK in
  certain situations."* Fire Ball thrown from the free hand is exactly that situation, so the off-hand IK
  needs a **per-clip enable**, not a global one.
- **Casts:** Meteor's call-down wants a raised staff, which is the camera's weakest direction (42 px per
  0.9 m, and directionally ambiguous with a step away — § 3). **Let the FX carry it**; that is Blizzard's
  own answer (*"melee swings match the motion of your weapon"*). Mark the RELEASE frame as data, which is
  what D2 did (`AnimData.d2` events `Attack` / `Missile`) and what both modern engines do.

**Cost:** medium — this is the real authoring work, per clip. **Risk:** medium, and it is *craft* risk, not
technical risk. **Measure:** the § 6.6 checks plus Matt's eye.

### Rank 4 — Put a trail on every strike. Not cosmetic — required by the measurement.

`attack` steps **up to 79.3 px in one frame on a 140 px figure** (§ 1.5). The literature names this exact
failure for exactly this weapon: *"without motion trails… that leads to strobing as the attack is usually
very fast and the sword in comparison very thin"*, and *"if the distance on screen is too big between
frames, the object needs to be stretched to prevent strobing."* Blizzard's stated remedy at an isometric
camera is an effect that *"match[es] the motion of your weapon."*

Cheap, because a trail *"can just be a 2D plane"* and is *"not very view dependent"* — **one trail works
across all eight cells.** Build it from the **edge**, tip→base, per Figgins' locator method and Unreal's
base/tip socket pair — we already ship an `axe_edge` marker; add a second so we have a span. Start the arc
*in the frames preceding* the fastest frame. Hold any smear one or two frames only. And smear the weapon,
not the whole arm — *"the hand alone creates enough guidance for the eye."*

### Rank 5 — Bound the grip's arc. The waffle is not fixed, and more wrist lock will not fix it.

`idle_armed`: **239–285 px of axe-head path per loop**, at the strongest lock alpha (0.75), versus
`walk_armed`'s **25–46 px at alpha 0.45.** The stronger lock has the worse arc, which localises the cause
away from the wrist. Order of attack, cheapest first:

1. **Re-source the armed idle from `Combat_Stance` (id 89)** instead of `Axe_Breathe_and_Look_Around`
   (id 335). A combat stance is a quieter clip by construction. Measure the arc; this alone may close it.
2. If not, damp the **shoulder and elbow** channels, not the wrist — that is where the lever is.
3. Set an explicit budget and lint against it (§ 6.6, check 4).

**Measure:** axe-head screen-path per loop. **Proposed budget: ≤ 60 px for any idle or locomotion cycle**
(derived from `walk_armed`'s measured 25–46 px, which Matt has not objected to). This is a *proposal from
our own best-behaved clip*, not an external standard — none exists.

### Rank 6 — QA instruments to build (six checks, all extensions of things we already have)

The record is clear that **nobody publishes a procedure for this** — not for grip-offset calibration across
weapons and clip sets (§ Q1's negative result), not as an animation-QA checklist, and no engine ships a
weapon-interpenetration check (§ Q6). We build it. The documented *pattern* to follow is Unreal's
Animation Modifiers (set-wide, per-frame geometric detection) and Data Validation (rules in CI) — which is
what `21_lint_export.py` already is.

1. **Skeleton-identity check** (new lint rule): every exported piece has the same bone names *in the same
   order* as the base rig. This is the one thing rank 1 can break, and `gear.gd` already computes the
   comparison — promote it from a report field to a FAIL.
2. **Hold predicate, per clip, as a standing table** — tilt / haft-forward / haft-outboard / head-outboard
   / edge-heading, against the rank-2b guard definition. `axe_probe.gd` and `axe_diag2.gd` already compute
   all of it. **They have never been run to an archived result** (§ 1.4). Run them, commit the JSON, and
   make it a gate.
3. **Edge-leads assertion on every strike** — `14_axe_assert.py`, promoted from one-off to standing, run
   for both hands and both weapons.
4. **Screen-arc budget** — axe-head path length and peak per-frame step, per clip, per direction cell
   (the § 1.5 instrument). Two numbers per clip: total arc (the waffle metric) and peak step (the strobe
   metric). Fail a locomotion/idle clip over the arc budget; flag any clip whose peak step exceeds a
   fraction of figure height as *requires a trail*.
5. **Golden-image gate on the cells** — our cells are already images. Use a Ground-Truth baseline with a
   **local**-error tolerance, per Unreal's model, so anti-aliasing noise does not fail a cell. Cheapest
   possible regression net for weapon motion, needing no new rendering.
6. **Penetration**, extending `sc_tilt.json`'s existing capsule/mesh depth measurement to both weapons in
   both hands across all clips. Interpenetration is a named, measured defect class in the literature.

**Governing caveat, from the academic source:** human perception outperformed individual objective metrics
in quality assessment. **These instruments are triage, not verdict.** They decide what reaches Matt's eye;
they do not replace it.

### Rank 7 — Weapon-first authoring: the ambitious option, and the one with the best craft pedigree

Author the *weapon's* path first and solve the arms by IK. A professional game animator states this as the
natural frame — *"the weapon leads the motions, just like your IK target leads your animation"* — and Unity
names the mechanism outright: *"you could configure a character's hand to sometimes control the motion of a
prop, and the prop to sometimes control the motion of the hand"* (MultiReferentialConstraint).

**It is the only approach that bounds the weapon's screen arc directly**, because the arc becomes the
authored quantity rather than an emergent consequence of shoulder motion — i.e. it is the principled fix
for defect (c), where ranks 1–5 are mitigations. **Hold it as a follow-on, not now:** it needs an authoring
surface we do not have, and ranks 1–5 should be measured first. Revisit if rank 5's budget cannot be met
by re-sourcing.

### Rank 8 — Explicit non-recommendations

- **Do not re-rig for finger bones.** The industry's own LOD ordering removes fingers first; a finger is
  under 1 px at our register; the grip morphs already work and Matt has accepted them. AccuRIG would give
  fingers but *deliberately refuses to rig the prop*, which is our actual problem.
- **Do not build the weapon channel on `BoneAttachment3D.override_pose`.** Godot's own docs warn it
  *"may cause unintended behavior when used at the same time with SkeletonModifier3D"* — and
  `TwoBoneIK3D`, which we rely on, is a `SkeletonModifier3D`.
- **Do not reach for video mocap or text-to-motion for this work.** The Meshy library already holds
  `Double_Blade_Spin`, `Axe_Spin_Attack`, `Combat_Stance`, `Sword_Shout`, the `Weapon_Combo` set and nine
  mage casts (§ Part 4). Sourcing is not the bottleneck; the weapon channel is.
- **Do not raise the wrist-lock alpha further.** Measured: the strongest alpha produced the worst arc.

### 6.9 Suggested order of work

| # | Work | Fixes | Cost |
|---|---|---|---|
| 1 | `weapon_r` / `weapon_l` on the base rig; rebind; exclude from retarget | precondition | hours |
| 2 | Fit mount roll; retarget wrist lock to `Combat_Stance` | **Matt's current complaint** | hours |
| 3 | Run the existing probes to an archived result; add the 4 lint rules | visibility | hours |
| 4 | Author the weapon channel per state (guard, strikes, block) | hold + edge | days |
| 5 | Whirlwind as constant pose + uniform yaw, N = 16 or 24 | the spin | days |
| 6 | Trail from the edge span on every strike | the 79 px strobe | days |
| 7 | Re-source armed idle from `Combat_Stance`; measure arc | the waffle | hours |
| 8 | Sorceress: staff on `weapon_r`, off-hand `TwoBoneIK3D` with per-clip enable | the staff | days |

Steps 1–3 are cheap, verified, and answer the live complaint. **They should not wait on the rest.**

---

## Part 7 — Knowledge gaps not resolved

1. **No developer anywhere states an on-screen character height in pixels for an ARPG camera.** Our 140 px
   has exactly one external anchor: D2's *"75 pixels tall"*. Everything else in the readability literature
   is qualitative.
2. **The spin-readability question is unanswered in the public record.** No developer commentary was found
   on making a continuous spin read — across Diablo II/III/IV, PoE Cyclone, Warframe, Dark Souls/Elden
   Ring, GDC Vault and Blizzard news. Our own SB-1 rotor flag may genuinely be the best evidence anyone
   has. **Treat the Whirlwind as unexplored territory and gate it on Matt's eye early.**
3. **D2's Whirlwind frame count is not published**, nor any statement that it is one revolution looped.
   Recoverable only by reading `AnimData.d2` directly.
4. **The phase-shift identity for the 8 spin cells is my inference, not a verified result.** It is
   geometrically sound given a constant local pose and uniform yaw, and the 8 cameras' shared elevation is
   confirmed in `bonedump.json` — but **render two cells and diff them before relying on it.**
5. **Hit-stop magnitude is unresolved and the two available figures differ by 10×** (1–4 frames, vendor
   source, vs an unverifiable ≈0.2 s). Do not specify it from citation; measure it.
6. **Mixamo's rig cannot be confirmed from a primary source** — every Adobe/Mixamo doc URL returned 403 or
   404 and the Internet Archive is blocked here. Whether it has finger or prop bones is genuinely unknown
   to this report.
7. **"Prop mocap yields a weapon joint in the FBX" is not established for any vendor's FBX export.**
   Vicon and OptiTrack both *describe* a prop as a single bone, but Xsens exports props only to C3D as
   three labelled points, and OptiTrack's FBX doc describes rigid bodies as 6-DoF data at their origin
   rather than bones in the skeleton hierarchy. Anyone buying prop mocap must verify the export path.
8. **`weapon_l`, `ik_hand_l/r`, `ik_hand_root`, `ik_foot_root` are not documented by Epic** anywhere I
   could reach (~18 pages checked). "The UE mannequin has `weapon_r` and `weapon_l`" is a community claim.
   Our naming is therefore our own choice, not a convention to match precisely.
9. **GGXrd's no-interpolation finding is a live challenge to our "one clean cycle, rates at playback"
   design** and I could not resolve it from sources. It needs an A/B, not more reading.
10. **The grip-offset calibration procedure is undocumented industry-wide**, against an abundance of
    documented *knobs*. We are not behind a best practice; there isn't one. That is why § 6.6 exists.
11. **The authoring-tool survey did not complete** (§ Q2). The session's 200-call WebSearch budget was
    exhausted across four parallel research passes. **Unresolved and worth one focused follow-up:** does
    **Cascadeur** support animating a held prop/weapon, and does it round-trip FBX with an arbitrary custom
    skeleton? If yes, it is the obvious place to author the weapon channel and would change rank 3's
    tooling. This is the single highest-value unclosed question in the commission.
12. **Whether any monocular video-mocap method recovers a HELD OBJECT is unresolved** — WHAM, GVHMR, TRAM
    and any 2025–26 successor were not reached. A clean negative would usefully close the door; an
    affirmative would open a sourcing option we have not considered. Likewise unconfirmed: Move.ai,
    DeepMotion and Rokoko Vision prop and finger support.
13. **Not verified in this pass:** whether Blender's glTF exporter drops our new bones under any export
    setting we actually use. Making them deform bones should make this moot (upstream bugs cluster on the
    *non*-deform case), and the round trip passed at default settings — but confirm against the real export
    configuration in `15_export_scene.py`.

---

## Source list

All accessed 2026-09-29.

**Our own repo (primary, read-only)**
- `astra_test_01/burst/runs/C-9/nb_d2/scripts/gearlib.py` — `socket_weapon2()` docstring (the rest-pose-is-everything statement)
- `.../nb_d2/scripts/11_weapon.py`, `14_axe_assert.py`, `18_grip.py`, `21_lint_export.py`, `26_wrist.py`, `27_armed_carry.py`
- `.../nb_d2/artifacts/D2-manifest.json` — `"PLACED, ORIENTATION NOT FITTED"`
- `.../nb_d2/work/retune.json` (wrist-lock alpha sweep), `wrist_final.json`, `sc_tilt.json`, `qa_final.json`
- `.../nb_d2/export/axe.glb`, `.../work/nb-body-final.glb` — the measured files
- `.../nb_t8/work/motions.json` — the 678-action Meshy library index
- `.../attack_lab/godot/scripts/gear.gd` (bind-mode reconciliation, `axe_edge` marker), `tools/axe_probe.gd`, `tools/axe_diag2.gd`
- `.../meshy_t2/work/bonedump.json` — the 8 direction-cell camera matrices
- `canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md` — camera of record
- `agentic_orchestration/gandalf/notes/2026-08-10-sb1-scene-run-ledger.md` — `player_lock` operands; the 140 px double-sourced register; **the whirlwind rotor readability flag**
- `agentic_orchestration/gandalf/notes/2026-08-16-sb1-session-handoff.md` — projection convention

**Probes run for this report** (scratchpad only, no repo writes): weapon-bone insertion + glTF round trip
(Blender 5.2.0 LTS → Godot 4.6.3.stable); hold-angle measurement per clip; axe-head screen-arc per
direction cell; camera projection geometry; Godot `TwoBoneIK3D` / `SkeletonModifier3D` class enumeration.

**Epic / Unreal**
- https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletons-in-unreal-engine
- https://dev.epicgames.com/documentation/unreal-engine/animation-blueprint-copy-bone-in-unreal-engine
- https://dev.epicgames.com/documentation/unreal-engine/retargeting-operation-stack-in-unreal-engine-5-8?lang=en-US
- https://dev.epicgames.com/documentation/en-us/unreal-engine/mirroring-animation-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-hand-ik-retargeting-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/hand-ik-retargeting?application_version=4.27
- https://dev.epicgames.com/documentation/en-us/unreal-engine/using-retargeted-animations-in-unreal-engine
- https://dev.epicgames.com/documentation/unreal-engine/skeletal-mesh-sockets-in-unreal-engine?lang=en-US
- https://dev.epicgames.com/documentation/en-us/unreal-engine/skeleton-tree?application_version=4.27
- https://dev.epicgames.com/documentation/unreal-engine/virtual-bones-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine
- https://dev.epicgames.com/documentation/unreal-engine/animation-modifiers-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine

**Godot / Blender / glTF**
- https://docs.godotengine.org/en/stable/classes/class_boneattachment3d.html
- glTF-Blender-IO issues on `Export Deformation Bones Only` + non-deform bones: [#2394](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2394) · [#2697](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2697) · [#2115](https://github.com/KhronosGroup/glTF-Blender-IO/issues/2115)
- https://studio.blender.org/tools/addons/pose_shape_keys

**Unity**
- https://docs.unity3d.com/Manual/class-ParentConstraint.html
- https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/MultiReferentialConstraint.html
- https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/TwoBoneIKConstraint.html
- https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/MultiParentConstraint.html
- https://docs.unity3d.com/Manual/InverseKinematics.html
- https://docs.unity3d.com/Manual/script-AnimationWindowEvent.html

**Diablo II (primary)**
- https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i- — Erich Schaefer, *Game Developer*, Oct 2000
- https://www.gdcvault.com/play/1028028/Resurrecting-a-Classic-Bringing-Diablo — Todisco, GDC 2022 (free; **highest-value unwatched lead**)
- https://gdcvault.com/play/1023469/Classic-Game-Postmortem — Brevik, GDC 2016 (Diablo 1)

**Diablo II (community reverse-engineering)**
- https://archive.org/stream/ExtractingDiabloIIAnimations/Extracting%20Diablo%20II%20Animations_djvu.txt — Siramy
- https://d2mods.info/forum/kb/viewarticle?a=174 · https://d2mods.info/forum/kb/viewarticle?a=350
- OpenDiablo2 format code: [`cof.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2fileformats/d2cof/cof.go) · [`composite_type.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2enum/composite_type.go) · [`weapon_class.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2enum/weapon_class.go) · [`animdata.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2fileformats/d2animdata/animdata.go) · [`events.go`](https://raw.githubusercontent.com/OpenDiablo2/OpenDiablo2/master/d2common/d2fileformats/d2animdata/events.go)
- https://diablo2.wiki.fextralife.com/Whirlwind · https://diablo2.io/skills/whirlwind-t4197.html · https://www.mannm.org/d2library/faqtoids/ias_eng.html

**Readability, timing and craft**
- https://news.blizzard.com/en-us/article/23746639/diablo-iv-quarterly-updatedecember-2021 — Briggs on melee readability
- https://news.blizzard.com/en-us/article/23665024/diablo-iv-quarterly-updatejune-2021 — Kotelnikoff, Chilano, Mueller, Barriga
- https://gdcvault.com/play/1015306/The-Art-of-Diablo — Lichtner, GDC 2012
- https://gameranx.com/features/id/5666/article/gdc-2012-the-art-of-diablo-iii/ (press coverage of the above)
- https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/ · https://www.leagueoflegends.com/en-us/news/dev/ask-riot-let-s-talk-clarity/
- https://www.animationcareerreview.com/articles/riot-games-senior-animator-rory-alderton-discusses-league-legends-animation-process
- https://www.animotionx.com/en/post/interview-jonathan-colin-readability-silhouette-and-gameplay-animation-secrets
- https://www.gamedeveloper.com/art/art-of-war-animating-realistic-sword-combat — Bradstreet + Clements, *Game Developer*, Dec 2012
- https://theses.fh-hagenberg.at/system/files/pdf/Lendenfeld18.pdf — Lendenfeld, *Smearframes in Video Games*, 2018
- https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf — Motomura, Arc System Works, GDC 2015 handout
- https://game.capcom.com/cfn/sfv/column/131432?lang=en — Capcom, startup/active/recovery
- https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation — Johnston & Thomas, 1981
- https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks · https://www.gdquest.com/library/juicy_attack/ · https://blog.cg-wire.com/smear-frames/
- https://archive.org/details/the-art-of-screenshake — Nijman, **INDIGO Classes 2013** (commonly miscited as GDC)
- https://www.3dfiggins.com/Store/Support/SwordSwipe/ — Figgins, edge locators
- https://www.remyjaspers.com/blog/melee_tracing_ue5/ — inter-frame arc sampling
- https://lilura1.blogspot.com/2019/10/Baldurs-Gate-Retrospective-Review-Graphics-Backgrounds-Sprites-and-Animation.html (community)

**Rigs, tools, mocap**
- https://syntystore.com/products/animation-sword-combat — *"make use of a prop bone"*
- https://syntystore.com/products/polygon-modular-fantasy-hero-characters
- `~/Games/reincarnated-godot/Assets/Synty/polygon-explorer-kit/SourceFiles/Characters/SK_Chr_Explorer_{Male,Female}_01.fbx` (local primary)
- https://www.kubold.com/unreal-faq-2 · https://www.reallusion.com/auto-rig/accurig/ · https://magazine.reallusion.com/2022/12/12/cutting-edge-auto-rigging-with-accurig/
- https://lucky3d.fr/auto-rig-pro/doc/auto_rig.html · https://www.lucky3d.fr/auto-rig-pro/doc/rig_behaviour_doc.html
- https://docs.meshy.ai/en/webapp/guides/3d-model/rigging · https://developers.tripo3d.ai/en/models/rig
- https://manual.reallusion.com/Character-Creator-4/Content/ENU/4.4/11-Set/Prop/Attaching-Props.htm
- https://vicon-help.atlassian.net/wiki/spaces/Shogun111/pages/13207098/Create+props · https://help.vicon.com/space/ShogunPost119/850468105
- https://docs.optitrack.com/motive/rigid-body-tracking · https://docs.optitrack.com/motive-ui-panes/properties-pane/properties-pane-rigid-body · https://docs.optitrack.com/motive/data-export/data-export-fbx
- https://www.xsens.com/hubfs/Downloads/usermanual/MVN_User_Manual.pdf
- https://mocaponline.com/blogs/mocap-news/skeleton-hierarchy-animation-guide · .../sword-melee-animation-guide (both VENDOR — treat as convention, not authority)

**QA**
- https://arxiv.org/html/2505.23301v1 — Rekik et al., quality assessment of 3D human animation
- https://gdcvault.com/play/1025452/-Assassin-s-Creed-Origins · https://gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled · https://www.gdcvault.com/play/1029332/Technical-Artist-Summit-Building-a

**Blocked this session** (recorded so nobody re-spends the budget): all `helpx.adobe.com` Mixamo pages
(403) and `mixamo.com/faq` (404); `docs.blender.org` (403 to WebFetch); Blender Rigify docs (403);
`diablowiki.net` (403); `streetfighter.fandom.com` frame data (402); Rokoko support (403);
`web.archive.org` blocked in this environment.
