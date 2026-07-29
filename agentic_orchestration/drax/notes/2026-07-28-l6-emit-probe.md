# L6-EMIT-PROBE — naming the MECHANISM of the 121-bone glTF round-trip inversion

> **STATUS: COMPLETE** — mechanism CONFIRMED (§7, §9). Written incrementally, one section per probe step.

**Cell:** L6-EMIT-PROBE · **Executor:** drax (presentation seam) · **Date:** 2026-07-28
**Authorization:** Matt, parallel thread · **Boundary: DIAGNOSTIC ONLY.** No production-code fix is
implemented anywhere. `/Users/admin/Games/reincarnated-godot` is **not touched** (a race cell may be
running there concurrently). All work in `/Users/admin/Games/mcp-lab/` scratch.

**Question:** PC-T3 §3.6 / §4bis established *that* the 121-bone inversion is a glTF **round-trip**
failure and *that* `retarget/remove_tracks/unmapped_bones = true` on the emitting project's import
config dissolves it. **The workaround is known; the mechanism is not.** This cell names the mechanism.

**Corpus (read-only, PC-T3's own emits — the exact pair):**
- **FAILING:** `/Users/admin/Games/mcp-lab/pct3/proj/emitted/lib_control.glb` — head y **−1.628 … −1.315**, inverted
- **FIXED:** `/Users/admin/Games/mcp-lab/pct3/proj/emitted/lib_c.glb` — head y **+1.612 … 1.649**, upright

Same character, same clips, same bone map, same `fix_silhouette`. **One `.import` boolean apart.**

**Instruments:** Layer-3 chain from PC-L3-INSTALL — `gltf-transform` 4.4.2, Khronos `gltf_validator`
2.0.0-dev.3.10 (Rosetta), Blender 5.2.0 headless, FBX2glTF 0.13.1 (Rosetta), Godot 4.6.3 headless in a
clean lab project at `/Users/admin/Games/mcp-lab/l6probe/` (M-T4 #4).

**Scratch root:** `/Users/admin/Games/mcp-lab/l6probe/`

---
## §1 — Probe step 1: the pair already exists, and it is a clean single-variable pair

PC-T3 emitted the failing/fixed pair on 2026-07-28 and left it intact. **No re-emit was needed for
steps 2–4**, and re-emitting would have been the worse instrument: these two files are the exact
artefacts the −1.628 / +1.612 numbers of record were measured on. They were used read-only.

| | FAILING | FIXED |
|---|---|---|
| file | `emitted/lib_control.glb` (1,350,504 B) | `emitted/lib_c.glb` (1,259,708 B) |
| `.import` config | drax R4 recipe, **no** `remove_tracks/unmapped_bones` | same **+ `retarget/remove_tracks/unmapped_bones: true`** |
| gate (glb-side) | head y **−1.628 … −1.315**, `upright=false` | head y **+1.612 … 1.649**, `upright=true` |

`gltf-transform inspect` on both (`l6probe/scratch/inspect_{control,c}.txt`): same generator
(Godot 4.6.3), same single `GODOT_single_root` extension, same mesh, same material, same bbox
(`-0.948,-0.003,-0.186 → 0.948,1.785,0.180` — **the bind-pose bbox is upright in BOTH**). The only
inspect-visible difference is channel counts:

| animation | FAILING channels | FIXED channels |
|---|---:|---:|
| `Take 001` | 22 | 15 |
| `swing` | 91 | 52 |
| `walk` | **84** | **42** |

---

## §2 — Probe step 2: the node graph. **The parent-transform hypothesis is REFUTED.**

The brief's leading hypothesis was a flip (180° X-rotation or −1 scale) parked on a **parent of the
skinned-mesh node** — the transform the validator's `NODE_SKINNED_MESH_NON_ROOT` warning says viewers
must ignore. Measured (`scratch/nodegraph.py`, outputs `scratch/graph_{control,c}.txt`):

```
== lib_control.glb (FAILING)          == lib_c.glb (FIXED)
nodes: 90  roots: [0]                 nodes: 90  roots: [0]
skinnedMeshNodes: [89]                skinnedMeshNodes: [89]
skins: [{joints: 88, skeleton: None}] skins: [{joints: 88, skeleton: None}]

-- skinned mesh node 89 'SK_DMMY_BASE_01_00BODY'
   own trs: IDENTITY                     own trs: IDENTITY
   parent 0 'SidekickChar' IDENTITY      parent 0 'SidekickChar' IDENTITY
```

**There is exactly one non-joint parent, `SidekickChar`, and its transform is IDENTITY in both files.**
There is no 180° rotation, no −1 scale, no `matrix` anywhere in the non-joint chain. The
`NODE_SKINNED_MESH_NON_ROOT` warning is real and universal across the emit corpus, but **it is not this
defect** — the transform it warns about is the identity, so honouring or ignoring it changes nothing.
The warning is a red herring for this inversion. Refuted on measurement, not on argument.

### 2.1 — And the two files are IDENTICAL everywhere except the animation channels

`scratch/jointdiff.py` compared, element by element, across the whole 88-joint skin:

```
joint order identical: True
parenting identical:   True
total differing joints: 0 of 88     (rest translation/rotation/scale AND inverseBindMatrices)
```

**Zero.** Same node hierarchy, same joint list, same joint order, same rest transforms, same 88
inverse-bind matrices to 1e-6. The bind pose of the failing file is the bind pose of the fixed file.
So the inversion is **not** in the hierarchy, **not** in the rest pose, **not** in the skin. It is
100 % in the animation data.

---

## §3 — ★ THE MECHANISM: an animated `Root` joint carrying a ~168° flip

`scratch/animdiff.py` diffed the `walk` animation channel-by-channel, matching on
`(target node name, path)`:

```
== animation 'walk': FAILING channels=84   FIXED channels=42
only in FAILING: 42        only in FIXED: 0        shared: 42
shared channels differing:  0
```

**The fixed file's animation is a strict SUBSET of the failing file's, and every one of the 42 shared
channels is value-identical.** `remove_tracks/unmapped_bones` is purely subtractive at the emit — it
adds nothing and it alters nothing. The whole 3.24 m head-y swing is produced by the *presence* of 42
extra channels.

The 42 extra channels, in full — and the first two are the whole story:

```
('Root', 'rotation')      ('Root', 'translation')        <-- the parent of the entire skeleton
('backAttach','rotation') ('ball_l','rotation') ('ball_r','rotation')
('calf_twist_01_l'…) ('calf_twist_01_r'…) ('elbowAttach_l'…×2) ('elbowAttach_r'…×2)
('eyeLight_l'…) ('eyeLight_r'…) ('hipAttachBack'…) ('hipAttachFront'…)
('hipAttach_l'…) ('hipAttach_r'…) ('ik_foot_l'…×2) ('ik_foot_r'…×2)
('ik_hand_gun'…×2) ('ik_hand_l'…×2) ('ik_hand_r'…×2) ('kneeAttach_l'…×2) ('kneeAttach_r'…×2)
('lowerarm_twist_01_l'…) ('lowerarm_twist_01_r'…) ('prop_r'…)
('shoulderAttach_l'…×2) ('shoulderAttach_r'…×2) ('thigh_twist_01_l'…) ('thigh_twist_01_r'…)
('upperarm_twist_01_l'…) ('upperarm_twist_01_r'…)
```

Forty of those are leaf/helper bones — `*Attach*`, `ik_*`, `*_twist_01_*`, `eyeLight_*`, `prop_r`,
`ball_*` — none of which is an ancestor of `Head`. **Two are not: `Root`.** `Root` is node 1, the
direct child of the scene root and the parent of `Hips`, which is the parent of `Spine → … → Head`.
**Everything the gate measures hangs off `Root`.**

And here is what `Root` is animated to (`scratch/rootdump.py`):

| file | `Root` REST | `walk` `Root.rotation` | angle |
|---|---|---|---|
| **FAILING** `lib_control` | **IDENTITY** | `(0.6217, 0.0979, 0.7708, 0.0992)` @ t=0 | **168.62°** |
| | | `(0.8604, 0.0121, 0.5028, 0.0823)` @ t=0.5 | **170.56°** |
| **FIXED** `lib_c` | **IDENTITY** | *channel does not exist* | — (stays identity) |

**A ~168–170° rotation about a near-horizontal axis (≈0.62, 0.10, 0.77 — the XZ plane), applied to the
parent of the whole skeleton.** That is an upside-down character. It is the inversion, in one number.

`Root` also carries a `translation` channel in the failing file (`≈ ±0.003, 0.002, 0.009` — small),
which is why the gate's head-y band is `−1.628 … −1.315` rather than an exact negation of
`+1.612 … 1.649`: the flip axis is tilted ~11° off horizontal and the hips drift.

### 3.1 — The `swing` clip corroborates it independently, at a different angle

`swing`'s `Root.rotation` is a **single keyframe** at `(0.1329, −0.1696, −0.3219, −0.9219)` =
**314.42°**, i.e. **−45.58°**. It is not a flip; it is a tilt. And PC-T3's control-config gate reads
`swing` at head y **0.904 … 1.254** — *positive but short*. A 1.6 m head tilted 45.6° off vertical
lands at `1.63 × cos(45.58°) = 1.14 m`, dead centre of the measured 0.904–1.254 band.

**Two clips, two different `Root` rotations, two different gate readings, and the gate readings are
predicted by the `Root` angle in both cases.** The `Root` channel is not correlated with the
inversion; it *is* the inversion, and it is quantitatively so.

---
## §4 — Probe step 3: surgery. **Double dissociation — `Root` is necessary AND sufficient.**

### 4.1 — L-N: the instrument was cleared before it was used to record anything

A clean lab project was built at `/Users/admin/Games/mcp-lab/l6probe/proj/` (M-T4 #4): **no assets, no
import step at all** — it loads the `.glb` from an absolute OS path at runtime via
`GLTFDocument.append_from_file`, so no import cache can contaminate a reading. The gate is PC-T3's own
`verify_clean/pose_gate.gd`, unmodified except that the path argument is generalised. Run on the two
files of record first:

```
lib_control  walk  -1.628..-1.315   -0.988..-0.792   0.7702 m  upright=false
lib_c        walk   1.612.. 1.649    0.970.. 1.006   0.4084 m  upright=true
```

**Character-for-character identical to PC-T3 and to the charter.** The instrument reproduces both poles
before it is trusted with anything new.

### 4.2 — Two surgical variants, cut from the SAME failing file

`scratch/surgery.py` rewrites only the GLB's JSON chunk (BIN left byte-identical; orphaned samplers
pruned and indices remapped so the result stays spec-legal — both variants re-validate at **0 errors**
under the Khronos validator, carrying only the same universal `NODE_SKINNED_MESH_NON_ROOT` warning).

| variant | what was cut from `lib_control.glb` | walk channels |
|---|---|---:|
| **V-NOROOT** | **only** the 2 `Root` channels. All 40 other extras KEPT. | 82 |
| **V-ROOTONLY** | the 40 non-`Root` extras. `Root` KEPT. | 44 |

### 4.3 — The result

```
V-NOROOT     swing 1.360..1.633   walk  1.612.. 1.649  upright=true    OK
             ^^^ character-for-character IDENTICAL to lib_c, the FIXED file (incl. R-hand 0.4084 m)

V-ROOTONLY   swing 0.904..1.254   walk -1.628..-1.315  upright=false
             ^^^ character-for-character IDENTICAL to lib_control, the FAILING file (incl. 0.7702 m)
```

**A clean double dissociation, to four decimal places on every column.**

- Remove `Root` alone → the file becomes the fixed file. **`Root` is necessary.**
- Keep `Root` alone → the file stays the failing file. **`Root` is sufficient.**
- The other 40 unmapped-bone channels contribute **exactly zero** — 0.000 m on every measurement.

**This narrows PC-T3's own §3.6/T3-F6 statement.** PC-T3 wrote *"the 121-bone inversion is caused by
the 80 unmapped leftover tracks landing on the target's bones."* Measured: it is **not** the leftover
tracks landing on the target's bones. Forty of them land harmlessly. It is **two channels on one
bone**, and that bone is the skeleton root. I am correcting a claim my own cell made yesterday, on my
own evidence.

---

## §5 — Probe step 4: cross-viewer read. **There is NO Blender-vs-Godot disagreement.**

Blender 5.2.0 headless (`scratch/blender_read.py`), glTF import, armature pose evaluated over 24
samples, world-space `Head` vs `Hips` on Blender's Z-up axis:

| file | Godot (`pose_gate.gd`) | Blender 5.2 headless | agree? |
|---|---|---|:---:|
| `lib_control.glb` (FAILING) | head y **−1.628 … −1.315**, upright=false | head Z **−1.6256 … −1.4112**, upright=False | **YES** |
| `lib_c.glb` (FIXED) | head y **+1.612 … 1.649**, upright=true | head Z **+1.6240 … 1.6474**, upright=True | **YES** |
| `v_noroot.glb` | **+1.612 … 1.649**, upright=true | **+1.6240 … 1.6474**, upright=True | **YES** |
| `v_rootonly.glb` | **−1.628 … −1.315**, upright=false | **−1.6256 … −1.4112**, upright=False | **YES** |

Blender independently reproduces **the whole double dissociation**, and it reports the `Root` pose
quaternion as `(w=0.0991, x=0.6217, y=0.0979, z=0.7708)` on the failing files and exactly
`(w=1.0, x=0, y=0, z=0)` on the fixed ones — **the same quaternion I read out of the binary by hand.**

**The disagreement pattern names the guilty side by its absence.** Two independent, spec-compliant
glTF readers, on different engines, in different languages, agree the file describes an upside-down
character. **The file is faithfully inverted.** No viewer is mis-honouring or over-honouring a
transform; the `NODE_SKINNED_MESH_NON_ROOT` ambiguity is not in play (§2). **The defect is in the
WRITER, unambiguously — Godot's `GLTFDocument` export.** That is as clean a localisation as this class
of question admits.

*(Instrument noise, named not hidden: every Blender run also lists a mesh object `Icosphere` that is
not in any `.glb` — the corpus has exactly one mesh, `SK_DMMY_BASE_01_00BODY`. It appears identically
in all four reads, never joins the armature, and separates no contestant. A control run with
`--factory-startup` + `read_factory_settings(use_empty=True)` and no import returns `[]`, so it is a
session artefact of my invocation, not of the files.)*

---
## §6 — Going upstream: the live scene has NO `Root` track, and its `Root` pose is IDENTITY

`Root` had to come from somewhere. PC-T3's two instruments — `pct3_gate.gd` (scene-side) and
`pct3_emit.gd` (glb-side) — turn out to **build the identical in-memory scene**: load the character
FBX, load each clip FBX, `duplicate(true)` the clip's `Animation`, add it to an `AnimationLibrary` on
an `AnimationPlayer` parented to the character. The scene gate then measures that scene; the emit then
`append_from_scene()`s that scene. **Same object. Different reading.** So the whole delta lives inside
`append_from_scene`.

A faithful copy of PC-T3's project was taken to `/Users/admin/Games/mcp-lab/l6probe/pct3copy/`
(assets + `.import` files + addons; `.godot/`, `emitted/`, `logs/`, `out/` excluded so the import is
cold). **PC-T3's evidence root was not modified** — its current `.import` state already *is* the
control config (`_subresources` carries `bone_map`, `rename_bones`, `skeleton_name: GeneralSkeleton`,
`fix_silhouette`, `keep_global_rest_on_leftovers`, and **no** `remove_tracks/unmapped_bones`).

`pct3copy/tools/l6_scene_probe.gd` builds that exact scene and interrogates it **before** any export:

```
CHAR skeleton node name = 'GeneralSkeleton'  bones=88
CHAR bone 'Root' idx=0  REST=[X:(1,0,0) Y:(0,1,0) Z:(0,0,1) O:(0,0,0)]   rest quat=(0,0,0,1)  parent=-1
--- CLIP swing : source skeleton 'GeneralSkeleton' bones=91   CLIP 'Root' rest quat=(0,0,0,1)
--- CLIP walk  : source skeleton 'GeneralSkeleton' bones=121  CLIP 'Root' rest quat=(0,0,0,1)

=== LIVE SCENE gate (the artifact append_from_scene will export) ===
  swing  head y  1.290..1.544    LIVE Root bone POSE rot@0=(0, 0, 0, 1) angle=0.000 deg
  walk   head y  1.525..1.559    LIVE Root bone POSE rot@0=(0, 0, 0, 1) angle=0.000 deg
```

Three facts, each load-bearing:

1. **The probe found no animation track whose path ends in `:Root` — in either clip.** It printed every
   such track and printed none. **The source animations contain no `Root` track at all.**
2. **The live `Root` bone pose is exactly identity** through the whole clip, and its rest is identity
   on the character AND on both clip rigs. Nothing in the scene rotates the skeleton root.
3. The live scene is **upright** — reproducing PC-T3 §4bis's scene-side numbers exactly
   (`walk 1.525..1.559`, `swing 1.290..1.544`).

`bone_map/Root = &"root"` is present in `sidekick_bone_map.tres`, so `Root` is a mapped, renamed,
ordinary bone — **and it is bone index 0**, the skeleton's first bone and the ancestor of everything.

**So `GLTFDocument.append_from_scene()` did not mis-transform a `Root` track. There was no `Root`
track. It MANUFACTURED one.**

---

## §7 — ★★ THE MECHANISM, NAMED: dangling bone tracks collapse onto bone index 0

`pct3copy/tools/l6_emit_probe.gd` builds the same scene twice and exports both, changing exactly one
thing: whether tracks whose bone name is absent from the target skeleton are removed **in memory,
before `append_from_scene`**.

The character rig is **88 bones**. The `walk` clip's rig is **121 bones** (§8.1). So 40 of `walk`'s 122
tracks name bones the character does not have:

```
walk   tracks=122  NON-RESOLVING=40
  ik_shoulder_l ×2, ik_elbow_l ×2, ik_shoulder_r ×2, ik_elbow_r ×2, ik_thigh_l ×2, ik_knee_l ×2,
  ik_thigh_r ×2, ik_knee_r ×2, ik_head_aim ×2, ik_eyes_aim ×2, ik_head_orient ×2, gluteProc_l ×2,
  gluteProc_r ×2, kneeProc_l ×2, kneeProc_r ×2, clavLiftProc_r ×2, clavLiftProc_l ×2,
  upperarm_proportion_l, upperarm_proportion_r, elbowProc_l ×2, elbowProc_r ×2
swing  tracks=91   NON-RESOLVING=1     [ fchr_dyn_01_01_r ]
```

**Result:**

| emit | walk gate | `Root` channels in the .glb |
|---|---|---|
| `probe_raw` (nothing stripped) | **−1.628 … −1.315, upright=false** — reproduces the failing baseline exactly | `Root.rotation` 29 kf @168.62°, `Root.translation` 14 kf |
| `probe_stripped` (40+1 dangling tracks removed pre-export) | **+1.612 … 1.649, upright=true, OK** — reproduces the fixed baseline exactly | **none. Zero `Root` channels.** |

### 7.1 — And the manufactured values are byte-identical to the LAST dangling track

`pct3copy/tools/l6_dangle.gd` reports the **last** non-resolving track of each type in each clip:

```
--- swing : dangling rotation tracks=1  position tracks=0
    LAST dangling ROT: '%GeneralSkeleton:fchr_dyn_01_01_r'  keys=1
        q@0 = (0.132869, -0.169637, -0.321857, -0.921942)   angle = 45.577 deg
--- walk  : dangling rotation tracks=21  position tracks=19
    LAST dangling ROT: '%GeneralSkeleton:elbowProc_r'  keys=29
        q@0 = (0.621714, 0.097892, 0.770751, 0.099148)      angle = 168.620 deg
    LAST dangling POS: '%GeneralSkeleton:elbowProc_r'  keys=14
        v@0 = (-0.002018, 0.002123, 0.00914)
```

Set against what the emitted `.glb` writes onto the `Root` **joint**:

| | last dangling track (in the scene) | `Root` channel (in the .glb) |
|---|---|---|
| swing rotation | `fchr_dyn_01_01_r`, **1 key**, `(0.132869, −0.169637, −0.321857, −0.921942)` | **1 keyframe**, `(0.13287, −0.16964, −0.32186, −0.92194)` |
| walk rotation | `elbowProc_r`, **29 keys**, `(0.621714, 0.097892, 0.770751, 0.099148)` | **29 keyframes**, `(0.6217, 0.0979, 0.7708, 0.0992)` |
| walk translation | `elbowProc_r`, **14 keys**, `(−0.002018, 0.002123, 0.00914)` | **14 keyframes**, `(−0.00202, 0.00212, 0.00914)` |

**Identical. Same keyframe count, same values, to every printed digit.** Not similar — the same data.

### 7.2 — The mechanism, in one paragraph

> **`GLTFDocument.append_from_scene()` resolves each skeleton animation track by bone NAME. When the
> name is absent from the target `Skeleton3D`, the lookup yields the failure sentinel and the track is
> written onto bone index 0 instead of being skipped. On a humanoid-retargeted Synty rig, bone 0 is
> `Root` — the parent of the entire skeleton. Every dangling track collapses onto that one joint,
> last-writer-wins per path type, and the winner's rotation becomes the character's world orientation.
> For `walk` the winner is `elbowProc_r` — a proc-helper bone that exists only on the 121-bone clip rig
> — carrying a 168.62° rotation. The character is exported upside-down.**

The live `AnimationPlayer` **skips** unresolvable tracks — which is why the same scene measures upright
in memory and inverted after a round-trip. The exporter does not skip them; it redirects them to the
root. That single divergence between the two consumers of the same `Animation` resource is the entire
121-bone inversion.

### 7.3 — What this says about the known workaround

`retarget/remove_tracks/unmapped_bones = true` deletes those dangling tracks **at import**, so the
exporter never meets one. **It does not fix the exporter — it starves it.** PC-T3's T3-F6 ("the missing
key in my own R4 recipe") is correct as an operational remedy and should stay in the recipe; it is now
also *understood*, which is what makes it safe to rely on. And it explains PC-T3 §4.5's puzzle exactly:
stripping the tracks from the *finished* Animation is the same operation as `remove_tracks`, **provided
it happens before `append_from_scene`** — §7's `probe_stripped` does it at that moment, in memory, with
no import setting at all, and it works.

### 7.4 — One loose end, measured and left open (honest narrowing)

PC-T3 §4.5 stripped 46 unmapped-bone tracks from **row 22's** fixer output and the result stayed
inverted (`walkstrip`, head y −1.568 … −1.530). My mechanism predicts that should have worked. Checked
directly against the artefact: in `lib_check6c.glb`, **`walkstrip` carries NO `Root` channel at all**
(`walkbase` and `walksynty` both do). So `walkstrip`'s residual inversion is **a second, different
defect**, specific to row 22's `rest_pose/load_pose = 2` + external-T-Pose recipe — its tracks are
composed in a rest basis the character does not share, which is a per-bone data problem, not a
root-collapse problem. **§7's mechanism explains the charter's −1.628 baseline completely and does not
explain `walkstrip`.** Row 22 is already `REACHES-NOT`; its separate defect is logged, not chased.

---
## §8 — The two side-answers

### 8.1 — Why 88 joints, not 121: **they are two different rigs, and nothing was lost**

Both source FBX were converted independently with FBX2glTF 0.13.1 (row 42) and their skins counted —
an instrument that has never seen Godot's importer:

| source FBX | role | nodes | skins | **joints** | has `elbowProc_r`? |
|---|---|---:|---:|---:|:---:|
| `assets/char/ModularSyntyCharacter.fbx` | **the character** | 90 | 2 | **88, 88** | **no** |
| `assets/anim/A_MOD_BL_Walk_F_Masc.fbx` | **the animation clip** | 122 | 1 | **121** | **yes** |

**The character rig has 88 bones; the animation rig has 121.** The emitted library is built on the
character, so it carries 88 joints — and Godot's own count agrees (`char skeleton='GeneralSkeleton'
bones=88`; the emitted skin's `joints` = 88; `Skeleton3D.get_bone_count()` on reimport = 88). Skeleton
bone count and skin joint count are **equal in every emit**; there is no drop, no truncation, and no
discrepancy to explain. The emit is not "losing 33 joints" — **the 121 was never the character's.**

The 33-bone difference is exactly the proc/IK helper family (`*Proc_*`, `ik_*`,
`upperarm_proportion_*`, `fchr_dyn_*`) that Synty ships on its animation rigs and not on its modular
character. **That difference is also the whole supply of dangling tracks in §7** — the two "oddities"
are one fact. "The 121-bone inversion" is more precisely *the 121-onto-88 transplant inversion*.

### 8.2 — Why `lib_a.glb` has animationCount 0: **the exporter omits empty animations entirely**

`lib_a.glb` has **no `animations` key in its glTF JSON at all** — not an empty array, absent. Its node
names are the raw Synty ones (`root`, `pelvis`, `hipAttachFront`, `thigh_l`, …), which identifies it as
PC-T3 **config a** — the stock Mixamo-Batcher bone map that matched 0/34 Synty bone names, so the
retarget bound nothing and the addon's own `remove_tracks/unmapped_bones` then deleted every track
(`swing` 91 → 0, `walk` 122 → 0). Those zero-track `Animation`s were still added to the library and
still handed to `append_from_scene`.

**Godot's `GLTFDocument` drops an animation that produces no channels rather than writing a named empty
one.** So `animationCount: 0` is not a Layer-3 anomaly and not an emit bug — it is config a's known
total track loss, faithfully reported one layer downstream. The validator saw the consequence of
PC-T3 §3.1, not a new defect.

---

## §9 — VERDICT

### MECHANISM: **CONFIRMED**, and it is a Godot glTF-**exporter** defect, not a spec violation and not a viewer disagreement

> Animation tracks addressing a bone that does not exist on the target `Skeleton3D` are **not skipped**
> by `GLTFDocument.append_from_scene()`. They are written onto **bone index 0** — `Root`, the ancestor
> of the entire skeleton — last-writer-wins per path type. On the L6 corpus the winner is the 121-bone
> clip rig's `elbowProc_r`, and its 168.62° rotation becomes the character's world orientation.

### The evidence chain, in order

1. The two files differ in **nothing** but animation channels — same hierarchy, same 88 joints, same
   joint order, same rest transforms, same 88 inverse-bind matrices (0 differing of 88). §2.1
2. The fixed file's channels are a **strict subset** of the failing file's, and all 42 shared channels
   are **value-identical**. The setting is purely subtractive. §3
3. Among the 42 extra channels, only `Root` is an ancestor of `Head`; the other 40 are leaf/helper
   bones. `Root` carries **168.62°** on walk and **45.577°** on swing — and `1.63 × cos(45.58°) = 1.14 m`
   predicts swing's measured 0.904–1.254 band. §3, §3.1
4. **Surgical double dissociation:** cutting only `Root` from the failing file makes it read exactly as
   the fixed file; keeping only `Root` makes it read exactly as the failing file — to four decimals on
   every column. Necessary and sufficient. §4
5. **Blender 5.2 reproduces all four readings and the same `Root` quaternion.** No viewer disagreement;
   the writer is guilty. §5
6. The **live scene has no `Root` track** and its `Root` pose is identity throughout, while measuring
   upright. The exporter manufactured the channel. §6
7. Stripping the 40+1 **non-resolving** tracks in memory before `append_from_scene` removes the `Root`
   channel entirely and yields an upright emit — from the identical scene. §7
8. The manufactured `Root` values are **byte-identical** to the last dangling track of each type
   (`elbowProc_r` on walk: 29 rotation keys and 14 position keys, same numbers; `fchr_dyn_01_01_r` on
   swing: exactly 1 key, same numbers). §7.1

### REFUTED along the way

- **The parent-transform hypothesis.** There is no flip, no −1 scale, no non-identity matrix anywhere in
  the non-joint chain; the only non-joint parent is the identity. §2
- **`NODE_SKINNED_MESH_NON_ROOT` as the culprit.** Real, universal across the emit corpus, and
  irrelevant here — the transform it warns about is the identity. §2
- **A glTF spec violation.** PC-L3-INSTALL §5.1 already measured 0 errors across all eight emits; both
  surgical variants also validate at 0 errors. **A perfectly conformant file can describe an
  upside-down character.** The validator is the wrong instrument for this class and always was.
- **PC-T3's own "80 leftover tracks landing on the target's bones" framing** — 40 of them land
  harmlessly; it is 2 channels on 1 bone. Corrected on my own cell's evidence. §4.3

### NARROWED

- Row 22's `walkstrip` residual is a **second, separate** inversion path (no `Root` channel present) and
  is not explained by this mechanism. §7.4

---

## §10 — What an emit-side FIX would look like (DESCRIBED, NOT IMPLEMENTED)

Boundary: this cell implements nothing. Ranked by where the defect actually is.

**(a) Upstream — the real fix, in Godot's `GLTFDocument`.** Make the exporter's bone-name lookup treat
"not found" as *skip this track*, matching what `AnimationPlayer` already does, instead of falling
through to bone 0. One-line class of change; the correct home for it; upstream-reportable with this
note's reproduction as-is (`probe_raw` vs `probe_stripped` from one script differing in one filter).
Not ours to land, and not ours to wait on.

**(b) Our side — a pre-export filter in the emit tool.** Exactly what `probe_stripped` does: before
`append_from_scene()`, walk each `Animation` and remove every track whose
`track_get_path().split(":")[-1]` is not found by `Skeleton3D.find_bone()`. Measured to work, produces
a `.glb` identical in gate output to the `remove_tracks` route, and it is **robust in a way the import
setting is not**: it is enforced at the emit — the one place every L6 artefact passes through — rather
than depending on ~3,386 per-clip `.import` blocks each carrying the right boolean. It also fails loud:
the filter can report a count, so a rig mismatch becomes a logged number instead of a silent flip.

**(c) Keep the import setting too.** `retarget/remove_tracks/unmapped_bones = true` stays in the
recipe (PC-T3 T3-F6). It is now known to be *starvation, not repair* — so it should be carried as
belt-and-braces alongside (b), not instead of it. Note it is also lossy in a way (b) is not: it deletes
the tracks from the imported clip permanently, where (b) filters per-emit against a specific target rig.

**(d) A gate, not a hope.** The single cheapest permanent guard is the one that already exists: run
`pose_gate.gd` on **every emitted `.glb`**, not on the scene. The scene-side reading is upright in
every config measured and would have passed this defect through silently (PC-T3's T3-F4, now fully
explained). **The glb-side gate is the instrument of record precisely because the `.glb` is the
front door.**

**Not recommended:** post-hoc surgery on finished `.glb` files (my `surgery.py`). It works — V-NOROOT
proves it — but it repairs a symptom downstream of a known, cheap, upstream filter. It exists here as a
diagnostic, and that is all it should ever be.

---

## §11 — Cell exit

**Nothing outside scratch was modified.** `/Users/admin/Games/reincarnated-godot` was **not touched**
(a race cell may be running there). `/Users/admin/Games/mcp-lab/pct3/` — PC-T3's evidence root — was
read only; `git status` in `reincarnated-collaboration` shows only this note.

**Created (all under `/Users/admin/Games/mcp-lab/l6probe/`):**
- `proj/` — clean lab Godot project (no assets, imports nothing) + `pose_gate.gd`
- `pct3copy/` — faithful copy of PC-T3's project (assets/`.import`/addons; `.godot` excluded for a cold
  import) + three new probe scripts: `tools/l6_scene_probe.gd`, `tools/l6_emit_probe.gd`,
  `tools/l6_dangle.gd`; emits `emitted/probe_{raw,stripped}.glb`
- `scratch/` — `glbjson.py`, `nodegraph.py`, `jointdiff.py`, `animdiff.py`, `rootdump.py`,
  `rootspread.py`, `surgery.py`, `blender_read.py`; `v_noroot.glb`, `v_rootonly.glb`;
  `src_{ModularSyntyCharacter,A_MOD_BL_Walk_F_Masc}.glb`; inspect + graph dumps
- `logs/` — `lncontrol.log`, `surgery_gate.log`, `blender_matrix.log`, `copy_import.log`,
  `scene_probe_control.log`, `emit_probe.log`, `probe_gate.log`, `dangle.log`

**Method notes carried and honoured:** M-T4 #4 (clean lab project, never `reincarnated-godot`) · L-N
(both poles reproduced character-for-character before any new reading was recorded; the copied project
independently re-reproduced the −1.628 baseline before its stripped variant was believed) · F8 (no
`project.godot` was read for a verdict) · boundary DIAGNOSTIC-ONLY (§10 describes; it does not build).

**Signed:** drax (presentation seam), 2026-07-28. The L6 front door has a named mechanism.
