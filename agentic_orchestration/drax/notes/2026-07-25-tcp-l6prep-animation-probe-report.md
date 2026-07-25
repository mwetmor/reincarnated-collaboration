# TCP-L6-PREP — does Matt's Synty animation corpus reach a rendered swing?

**From:** drax (presentation seam) · **To:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l6prep-animation-probe.md`
**Stack:** Godot **4.6.3.stable.official.7d41c59c4** · Metal · Apple M2 · macOS 24.6.0

---

## Verdict in one line

**Yes, they work — and they dissolve TCP-38 ③.** All three questions resolved to
recorded facts, none `UNRECOVERABLE`. The clip exists: a real Sidekick character
driven by a real Synty animation, sword in hand, **0.000000000 m of weapon drift
across 101 measured frames.**

| # | question | answer | evidence |
|---|---|---|---|
| 1 | Does a Synty animation FBX import cleanly via built-in ufbx on 4.6.3? | **YES** | `Skeleton3D` + `AnimationPlayer` + correctly-named clip of correct length, 11/11 files |
| 2 | **Can it be done without a human at the GUI?** | **YES** | `godot --headless --import` → exit 0, **2.78 s**, cold/absent cache, 7 FBX |
| 3 | **Does the `.glb` round-trip carry the animation?** | **YES** | channels, lengths, **and root translation** survive; proven in a project that has never imported anything |

**Consequence for TCP-38 ③.** The capability fork softens from *"H cannot reach
rigged content"* to *"H pays a one-time conversion pass."* Headless GDScript does
not need an editor-resident MCP wire for animated content. It needs one CLI
invocation, after which the content is plain `.glb` that anything can load. The
wires do not own rigged content.

---

## §1 — The command lines, and what each returned

### 1.1 Import (the fork-decider)

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --import \
    --path /Users/admin/Games/mcp-lab/l6prep
```

`--import` is flagged **editor-only** in `--help` ("Starts the editor, waits for
any resources to be imported, and then quits"). Combined with `--headless` it runs
unattended and **works**.

- **Exit 0.** `2.07s user 0.31s system 85% cpu 2.778 total` — 7 FBX, from a
  directory with **no `.godot/` at all** (verified absent immediately prior).
- Produced `.godot/imported/*.scn` + `.md5` for every file, and a `.import`
  sidecar next to each source.
- **2 errors, both benign and identical in kind:** Synty FBX embed references to
  `.psd` texture files that do not ship alongside; Godot cannot load PSD and skips
  the image. Geometry, skeleton and animation are unaffected.
- Incremental re-imports later in the session: **2.58 s**, **2.6 s**, ~2 s. The
  cache is warm-reusable; only changed files re-import.

### 1.2 Inspection — what the import actually made

```bash
Godot --headless --path <proj> --script res://tools/inspect_import.gd
```

Every animation FBX produced `Node3D → Skeleton3D + AnimationPlayer`, one clip,
named after the file. Track types are only `TYPE_POSITION_3D` (1) and
`TYPE_ROTATION_3D` (2) — **no scale tracks anywhere.**

| file | rig bones | clip length | tracks (pos/rot) | bones addressed |
|---|---|---|---|---|
| `SidekickSyntyCharacter` (base-loco pack) | 88 | — | — | mesh `SK_DMMY_BASE_01_00BODY`, skinned |
| `ModularSyntyCharacter` (sword pack) | 88 | — | — | same rest as above |
| `SM_Wep_Sword_01` | — | 5.0000 s | 0 / 0 | phantom empty `Take 001`, strip it |
| `A_MOD_SWD_Idle_Base_Neut` | 91 | 1.7667 s | 10 / 66 | 66 |
| `A_MOD_SWD_Attack_HeavyCombo01A_Neut` | 91 | 2.0333 s | 12 / 79 | 79 |
| `A_MOD_SWD_Attack_HeavyCombo01A_RM_Neut` | 91 | 2.0333 s | 13 / 79 | 80 |
| `A_MOD_BL_Walk_F_Masc` | 121 | 1.0333 s | 31 / 72 | 72 |
| `A_MOD_BL_Walk_F_RM_Masc` | 121 | 1.0333 s | 32 / 72 | 73 |
| `A_MOD_GBL_Walk_F_Neut` | 91 | 1.0333 s | 11 / 64 | 64 |

### 1.3 Round-trip — emit, then verify in a clean room

```bash
# emit
Godot --headless --path <proj> --script res://tools/emit_final.gd
# verify: a project that has NEVER imported anything, loading by absolute OS path
Godot --headless --path <proj>/verify_clean --script res://verify.gd
```

`GLTFDocument.append_from_scene()` → `write_to_filesystem()` returned **OK** for
every artifact. Re-loaded through `append_from_file()` + `generate_scene()` — the
same call `motion_clip.load_glb()` makes — in `tcp-l6prep-verify`, a project that
holds **zero assets**:

- `sidekick_swing.glb` — 91 tracks, `{pos:12, rot:79}`, **identical to source**.
  Hand bone travels **1.4298 m** across the arc. Pose moves.
- `sidekick_walk_rm.glb` — 65 tracks (the 40 unresolved IK/proc tracks were
  correctly dropped on the way out). Pose moves.
- `sidekick_swing_armed.glb` — the `BoneAttachment3D` round-tripped **as a
  `BoneAttachment3D`**, name `hand_r`, `bone_name='hand_r'`, `bone_idx=62`. glTF
  has no bone-attachment concept; Godot re-expresses it as a child of the joint
  and rebuilds it on import.

**Root translation survives.** Control experiment (`emit_control.gd`): export a
clip scene *unmodified* and read the root track back —

```
SOURCE root pos track: keys=2  k[0]=(0,0,0)  k[1]=(0,0,1.500000)
ROUND-TRIPPED:         keys=32 k[0]=(0,0,0)  k[last]=(0,0,1.500000)  NET=1.5000 m
=> root translation SURVIVES the unmodified round-trip
```

---

## §2 — The picture

`/Users/admin/Games/mcp-lab/harness/out/l6prep_sidekick_swing/`

| file | what |
|---|---|
| `l6prep_sidekick_swing.mp4` | **100 frames @ 40 fps = 2.500 s**, 1280×720 |
| `l6prep_sidekick_swing.gif` | same, 640 px |
| `l6prep_sidekick_swing_strip.png` | 12-thumb timestamped film-strip |
| `frames/frame_00000..00099.png` | the sequence |
| `render.log` | invocation + full per-frame arc trace |

```bash
cd ~/Games/mcp-lab/harness
bash bin/shoot_clip.sh l6prep_sidekick_swing res://clips/l6prep_sidekick_swing.gd \
     --fps 40 --duration 2.5 --width 1280 --height 720 \
     --dist 4.4 --fov 30 --target -0.55,1.05,0.0 --settle 30
```

Subject: `ModularSyntyCharacter` (Sidekick rig, 88 bones) driven by
`A_MOD_SWD_Attack_HeavyCombo01A_Neut` (2.0333 s), `SM_Wep_Sword_01` mounted on
`prop_r`, at the seam's standing ARPG combat framing (yaw 47°, pitch −50°). The
character reaches the harness **only as an emitted `.glb`** — which is §1.3's
answer arriving as a picture.

### Weapon-in-hand, measured across the arc, not at one frame

Per-frame trace in `render.log` (`[arc]` lines), 101 samples:

| quantity | value |
|---|---|
| `prop_r` socket travel | bbox (0.731, 1.176, 1.123), **diag 1.7830 m** |
| blade-tip travel | bbox (2.186, 1.698, 1.881), **diag 3.3470 m** |
| **grip-to-socket separation** | min **0.000000000**, max **0.000000000**, **DRIFT 0.000000000 m** |
| fastest blade-tip step | **1.1682 m** between adjacent frames at t=1.200 s (**46.7 m/s**) |

The sword does not detach, at any point, to nine decimal places. It cannot: the
mount is computed inside `set_time` rather than delegated (see §5).

### Accumulator lockout

**Held — no tolerance declared, none needed.** The clip uses
`deterministic_env()` unmodified; glow/SSAO/SSIL/SDFGI/volumetric-fog/auto-exposure
all off.

**New fact:** the harness's determinism property, previously only proven for
scripted motion, **holds for a rigged `AnimationPlayer`-driven Synty skeleton.**
Separate-process re-render:

```
framediff: rerun_identity
  pairs           : 100
  byte-identical  : 100 / 100
  pixel-identical : 100 / 100
  scale bar (adjacent frames of the motion): 26,435..37,611 px changed, max channel delta 228
```

Both MP4s share sha256 `10007ba4a1707deb2ec56d5a093e64b94e631f3b3c86ed0d21f92dc8b68c0267`.

---

## §3 — Bone / rig report: **NAME-MATCH IS NOT RIG-MATCH**

> The dispatch asked me to *name* this gap, not fix it. Naming it took a
> measurement, because the first name I had for it was wrong.

### 3.1 Within the packs, the names line up almost perfectly

Bones addressed by each clip that exist on the 88-bone pack character:

| clip | rig | present on target | missing |
|---|---|---|---|
| `A_MOD_SWD_Idle_Base_Neut` | 91 | **98.5%** | `fchr_dyn_01_01_r` |
| `A_MOD_SWD_Attack_HeavyCombo01A_Neut` | 91 | **98.7%** | `fchr_dyn_01_01_r` |
| `A_MOD_GBL_Walk_F_Neut` | 91 | **98.4%** | `fchr_dyn_01_01_r` |
| `A_MOD_BL_Walk_F_Masc` | 121 | 70.8% | 21 bones, **all** `ik_*` / `*Proc_*` / `upperarm_proportion_*` |

The base-locomotion pack ships a **fatter rig** (121 bones, carrying Unreal-style
control-rig helpers that drive nothing on a Godot skeleton). Every *deformation*
bone matches. On names alone, this looks solved.

### 3.2 It is not solved. The rests disagree.

Godot's imported bone tracks are **local transforms**, meaningful only against the
rest pose they were authored on. Per-bone rest deltas over shared-by-name bones
(`tools/rest_compare.gd`):

| character | clip rig | shared | mean Δrot | max Δrot |
|---|---|---|---|---|
| any pack character (all three share one rest) | sword pack (91) | 88 | **27.69°** | **179.97°** |
| " | base-loco (121) | 88 | 19.94° | 180.00° |
| " | goblin pack (91) | 88 | 33.93° | 180.00° |
| `SK_Chr_Male_Wizard` (our hero, raw import) | sword pack | 48 | **67.72°** | 179.60° |

Driving a raw clip onto a raw character across that gap produces a character whose
**head sits at y = −0.69** mid-clip, with a **perfectly intact skin** (88/88 binds
resolving, no bad bone names, no scale anomaly). That failure is invisible to
every name-based check and it cost a render to see — which is the argument for the
harness in one sentence.

### 3.3 **A bone map / `SkeletonProfileHumanoid` retarget IS required — on BOTH sides**

Our hero, the same FBX imported two ways, measured side by side
(`tools/hero_compare.gd`):

| import | skeleton node | bones | first names |
|---|---|---|---|
| default | `Skeleton3D` | 50 | `root, pelvis, spine_01, spine_02, spine_03, clavicle_l, upperarm_l, …` |
| via `sidekick_bone_map.tres` | **`GeneralSkeleton`** | 50 | `Root, Hips, Spine, Chest, UpperChest, LeftShoulder, LeftUpperArm, …` |

Name overlap between the two imports of the *same file*: **11 of 50** (the
"leftover" bones the humanoid profile has no slot for).

How well a **raw-imported pack clip** binds to each:

| clip | → hero RAW | → hero RETARGETED |
|---|---|---|
| `A_MOD_SWD_Attack_HeavyCombo01A_Neut` | 54.4% | **6.3%** |
| `A_MOD_SWD_Attack_HeavyCombo01A_RM_Neut` | 55.0% | **6.2%** |
| `A_MOD_BL_Walk_F_RM_Masc` | 39.7% | **9.6%** |
| `A_MOD_GBL_Walk_F_Neut` | 54.7% | **9.4%** |

**The two name spaces do not mix.** Our hero as shipped in `reincarnated-godot` is
in the retargeted space; a raw pack clip binds to it at ~6–10%, i.e. not at all
(→ T-pose). Both sides must go through the same map. `reincarnated-godot` already
does exactly this for the one base-locomotion walk it uses — its
`SK_Chr_Male_Wizard.fbx.import` carries the `_subresources` block with
`retarget/bone_map`, `rename_bones`, `skeleton_name: "GeneralSkeleton"`,
`rest_fixer/fix_silhouette: true`, `normalize_position_tracks`, `overwrite_axis`.

**Does `rest_fixer` / `fix_silhouette` come into it? Yes, load-bearing.**
`hero_walker.gd`'s own header records why: `fix_silhouette` rotates the retargeted
rest so the arms hang at the sides matching the source A-pose instead of the
humanoid profile's T-pose, and *that* is what let the native clip replace an
earlier `ArmSwingMod` procedural hack.

I applied that same block to both the character and the clips in the probe. Result
(`verify_clean/pose_gate.gd`, 24 samples per clip, head-above-hips checked every
frame):

| clip | head y | hips y | R-hand travel | upright every frame |
|---|---|---|---|---|
| `swing` | 0.904 … 1.254 | 0.513 … 0.775 | **1.521 m** | yes |
| `swing_rm` | 0.905 … 1.254 | 0.514 … 0.775 | 1.685 m | yes |
| `idle` | 1.227 … 1.235 | 0.735 … 0.740 | 0.023 m | yes |
| `goblin_walk` | 0.998 … 1.138 | 0.677 … 0.844 | 0.323 m | yes |
| `walk` (base-loco, 121-bone) | **−1.628 … −1.315** | −0.988 … −0.792 | 0.770 m | **NO** |

**Named gap, for L6 to scope — I have not fixed it:**

1. **The retarget must be applied to every pack clip's `.import`.** It is a
   mechanical `_subresources` patch, one block per file, and `--headless --import`
   applies it unattended. 3,386 files.
2. **The 91-bone packs (sword, goblin, and by inference bow/idles/emotes) retarget
   cleanly onto an 88-bone pack character. The 121-bone base-locomotion pack does
   not** — it inverts the character. It *does* work against
   `reincarnated-godot`'s 50-bone hero, which carries far fewer un-mapped leftover
   bones for the fat rig's extra tracks to land on. **Which character a clip is
   bound to changes whether the retarget succeeds.** That is L6's decision, not
   this probe's.
3. **`fix_silhouette` is not optional** and must match on both sides.

### 3.4 Two §0 hypotheses corrected

- **"`goblin-locomotion` is a monster rig" — FALSE.** Its tree is
  `Animations/{Sidekick,Polygon}/Neutral/…` and its characters are
  `SidekickSyntyCharacter.fbx` / `PolygonSyntyCharacter.fbx`. It is
  goblin-*flavoured* locomotion authored for the same humanoid Sidekick rig —
  98.4% name-bind to the pack character. (`reincarnated-godot` does carry a
  separate `goblin_bone_map.tres`, so a distinct goblin *character* rig exists
  elsewhere; it is not in this pack.)
- **"our hero already uses the Sidekick rig" — TRUE, and confirmed from the
  build, not the guess.** `hero_walker.gd` states it and its `.import` proves it.
  But the hero is **50 bones**, not 88/91/121, and lives in the *renamed*
  `GeneralSkeleton` space.
- **§0's `sword-combat/Models/` list was incomplete** — it also carries
  `POLYGONRig_01.fbx`, `PolygonSyntyCharacter.fbx`, `SM_Generic_SkyDome.fbx`.
- **Two of the six packs are already vendored** in `reincarnated-godot/Assets`:
  `anim-base-locomotion` and `anim-goblin-locomotion` (plus
  `polygon-animation-goblin-locomotion`). The genuinely new material is
  **bow-combat, idles, emotes-taunts, sword-combat**.

### 3.5 The rig ships weapon sockets — use them

The Sidekick rig carries **`prop_l` / `prop_r`**, children of the hand bones. They
are **animated by the sword-combat clips** (`'prop_r' driven by the swing clip:
true`). Their rest basis is axis-aligned (`X=(-1,0,0) Y=(0,0,-1) Z=(0,-1,0)`),
which makes the grip transform *derivable* rather than dialled in by eye. The
clip's `GRIP` constant is a single −90° roll about Z, read off that geometry.
**Mount weapons on `prop_*`, not on `hand_*`.**

---

## §4 — Root motion, in one sentence

**Synty ships every locomotion and attack clip twice — the plain name is authored
in place with no `root` position track at all, and the `_RM_` twin carries a real
root translation track — so L6 chooses its regime per clip rather than having to
author one.**

Measured, source side:

| clip | rig | length | root position track |
|---|---|---|---|
| `A_MOD_BL_Walk_F_Masc` | 121 | 1.0333 s | **none** — in place |
| `A_MOD_BL_Walk_F_RM_Masc` | 121 | 1.0333 s | 2 keys, **+1.500 m** in Z (= **1.452 m/s**) |
| `A_MOD_SWD_Attack_HeavyCombo01A_Neut` | 91 | 2.0333 s | **none** — in place |
| `A_MOD_SWD_Attack_HeavyCombo01A_RM_Neut` | 91 | 2.0333 s | 19 keys, **+0.500 m** in Z (a lunging attack) |
| `A_MOD_GBL_Walk_F_Neut` | 91 | 1.0333 s | **none** — in place |

In-place clips still move the *pelvis* (the walk's pelvis bobs with `max|step|`
0.0052 m and returns to its start exactly; the attack's pelvis drops 0.135 m into
the crouch) — that is body mechanics, not travel.

**Caveat for L6, measured here:** root translation survives an *unmodified* glTF
round-trip (§1.3) but was **flattened to 0.009 m when I re-bound a 121-bone clip
onto an 88-bone character before export**. Whether that survives the retargeted
pipeline is not established by this probe. If L6 wants root motion, test it after
the retarget, on the exact character it will ship.

---

## §5 — A harness finding that changes how L6 writes clips

**`BoneAttachment3D` is incompatible with `motion_clip.set_time()`'s purity
contract, and must not be used in a harness clip.**

It refreshes **once per frame**, off the skeleton's update notification. That makes
frame *k* depend on frame *k−1* — exactly what the seek-mode contract forbids, and
exactly what the accumulator lockout exists to prevent elsewhere. Measured: reading
an attachment 24 times inside a single frame reports up to **0.54 m of phantom
weapon drift** on a weapon that is correctly attached.

The clip therefore computes the mount itself:

```gdscript
seek_all_players(_char, t, CLIP_NAME, true)
_skel.force_update_all_bone_transforms()
var bone_world := _skel.global_transform * _skel.get_bone_global_pose(_socket_idx)
_sword.global_transform = bone_world * grip
```

Both reads happen inside `set_time`, so the weapon can never be a frame behind the
hand. That is why the drift figure is **0.000000000 m** rather than "small".

`seek_all_players(node, t)` — the one-line bridge — needed **no change**. The
harness required no modification of any kind to render a rigged character.

---

## §6 — Instrument bugs found, all mine

Recorded because each produced a **confident, wrong answer about the assets**, and
TCP-30's whole point is that the frame has to be trustworthy before its output is.

1. **Work run in `_initialize()`.** `SceneTree.root` is not yet in the tree there,
   so every `Node3D.get_global_transform()` returns identity with an error. Rig
   reported ***"POSE IS DEAD — samplers did not survive"*** for three `.glb` files
   whose animation was completely intact. → run on the first `_process` tick.
2. **`position_track_interpolate(track, anim.length)` on a `LOOP_LINEAR` clip**
   wraps to the `t=0` value. Reported **0.0 m** of root travel for a clip that
   moves **1.5 m**, i.e. "root motion does not survive glTF" — the opposite of the
   truth. → read first/last **key values**, which no loop mode can rewrite.
3. **Sampling `BoneAttachment3D` many times per frame** → §5.
4. **A pose-sanity gate that also ran in `_initialize()`**, so it measured the rest
   pose while looking exactly like a gate (`head y 1.544..1.544` for five different
   clips, including a violent sword combo).

Bug 2 is the one worth flagging upward: it would have shipped a *false negative* on
the single most valuable property in the whole probe.

---

## §7 — Hygiene

- **`mcp-lab/project/` — UNTOUCHED.** `find -newermt "2026-07-25 16:45"` returns
  the directory itself and nothing within it. The concurrent L5-D cell's floor was
  never entered.
- **`mcp-lab/harness/` — no `.godot/` acquired.** Its no-import-cache property is
  intact; the new clip loads `.glb` from absolute OS paths like every other clip.
  One file added: `clips/l6prep_sidekick_swing.gd`.
- **`reincarnated-godot/` — READ-ONLY, honoured.** Four files *copied out*
  (`SK_Chr_Male_Wizard.fbx`, its texture, `addons/sidekick_creator/`), nothing
  written. `git status` shows the pre-existing uncommitted `M project.godot` the
  dispatch warned about and nothing else new from me.
- **`user://` clean.** File logging off via **both** keys.
  `app_userdata/tcp-l6prep/` and `tcp-l6prep-verify/` contain no logs (one empty
  `objectdb_snapshots/`). The harness dir holds only its regenerable
  `shader_cache/`.
- **Corpus not imported.** 11 FBX in the probe, not 3,386. `l6prep` totals **16 MB**,
  of which `.godot/` is **1.5 MB**.

---

## §8 — Rulings

| # | ruling |
|---|---|
| **R1** | `godot --headless --import` **works** on 4.6.3: exit 0, 2.78 s for 7 FBX, no GUI, no operator. **TCP-38 ③'s fork softens to a one-time import pass.** Either answer was first-rank; this is the one the machine gave. |
| **R2** | The FBX→`.glb` round-trip **carries animation channels, clip lengths and root translation**, verified in a project with no import cache. **The animated corpus is now first-class for the headless route.** |
| **R3** | **A bare animation FBX cannot round-trip alone** — glTF has no skeleton without a skinned mesh. Clips must be bound to a character before export. This forces **one `.glb` per character carrying its whole clip library**, which collapses 3,386 files to a handful of artifacts rather than expanding them. |
| **R4** | **Name-match is not rig-match.** 98.7% bone-name agreement coexists with ~28° mean / 180° max rest-rotation disagreement, and the failure mode (head at y = −0.69, skin perfectly intact) is invisible to every name-based check. **A `sidekick_bone_map` → `SkeletonProfileHumanoid` retarget with `rest_fixer/fix_silhouette` is mandatory, on both sides.** Named, not fixed — L6's scope. |
| **R5** | **Root motion is a per-clip choice Synty already made for us**: every clip ships in-place and as an `_RM_` twin with a real root track. |
| **R6** | **`BoneAttachment3D` must not be used inside a harness clip** — its once-per-frame deferred refresh violates `set_time()` purity. Compute the mount from `get_bone_global_pose()` inside `set_time`. Mount on **`prop_r`**, the rig's own animated weapon socket. |
| **R7** | The harness's **determinism property extends to rigged content**: 100/100 byte-identical across processes, matching MP4 sha256, with a skinned 88-bone skeleton and a 46.7 m/s blade. `seek_all_players` needed no change. |
| **R8** | **`l6prep` STAYS** (dispatch §4.6) — §1.3 works, so it is the corpus's front door. `README.md` documents the three commands. |

### Raised, not acted on

- **`reincarnated-godot/scripts/hero_walker.gd` line 44** declares
  `STRIDE_PER_CYCLE := 1.35`. The measured stride of the clip it drives
  (`A_MOD_BL_Walk_F_RM_Masc`) is **1.500 m/cycle** — an ~11% foot-skate error in
  the shipped hero walk. Read-only repo; flagged for L6, not touched.
- **Four `.controller` files** in the packs are Unity `AnimatorController` assets —
  unusable by Godot, but readable as Synty's intended state machine. Not parsed
  this lap.

---

## §9 — Read list

**Governing**
- `agentic_orchestration/dispatches/2026-07-25-drax-l6prep-animation-probe.md`

**Read (not written)**
- `reincarnated-godot/scripts/hero_walker.gd`
- `reincarnated-godot/Assets/Synty/polygon-fantasy-characters/Source_Files/Characters/Unreal_Characters/SK_Chr_Male_Wizard.fbx.import`
- `reincarnated-godot/addons/sidekick_creator/sidekick_bone_map.tres`
- `mcp-lab/harness/README.md`, `motion_clip.gd`, `project.godot`, `bin/shoot_clip.sh`, `clips/demo_sword_arc.gd`
- `matt_notes_handoff_docs/recent-synty-packs/synty-animations/` — full tree survey

**Written**
- `mcp-lab/l6prep/` — new project (README, `project.godot`, 7 tools, `verify_clean/` with 5 scripts)
- `mcp-lab/harness/clips/l6prep_sidekick_swing.gd` — one new clip
- this report

---

## §10 — Wall clock (TCP-32: authoring separate from execution)

**Session: 16:51 → 17:28 EDT, 2026-07-25 — 37 minutes.**

| band | ≈ | notes |
|---|---|---|
| **Execution** (machine) | **~7 min** | 4 headless imports (2.78 + 2.58 + 2.6 + ~2 s); 13 headless script runs (~2–5 s each); 4 renders (2 probes + final + determinism re-render, ~60–90 s each); 1 framediff |
| **Authoring + analysis** (me) | **~30 min** | terrain survey; 7 tools + 5 clean-room scripts + 1 harness clip; 4 instrument-bug diagnoses; `.import` patching; README + this report |

Execution was never the constraint. **Roughly a third of the authoring time went to
finding and fixing my own instrument** — four bugs, each of which had already
produced a confident wrong answer about Matt's assets. Two of those wrong answers
("the pose is dead", "root motion does not survive glTF") would have been reported
as corpus defects and would have argued for keeping TCP-38 ③'s fork open.

---

## Answer to Matt's question

**"Will these work?" — Yes.** They import headlessly, they convert to `.glb` with
their animation intact, and a Sidekick character swings a sword with the weapon
welded to its hand for the full 2.5 seconds. The one thing standing between the
probe and the corpus is a mechanical retarget patch applied to each clip's
`.import` — the same one the hero already uses — and scoping that is L6's job.
