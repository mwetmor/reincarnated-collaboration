# PROVISION-CAL · Wave-1 cell PC-W1-A — werewolf A-PREP + menus glyph coverage

**Run:** PROVISION-CAL (`2026-07-28-provision-cal-run-charter.md`) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Cell:** PC-W1-A · **Executor:** drax (presentation seam, `reincarnated-godot`) · **Date:** 2026-07-28
**Riders:** charter §2 **T-3** (werewolf A-PREP a/b/c/d) + §2 **T-4** (menus glyph coverage)
**Boundary observed:** measurement + import only. No feature work. Findings beyond scope are logged in §5 for the
conductor, never acted on. **R-PC-1 honoured:** `SK_Chr_Werewolf_Undead_01.fbx` was never loaded, imported,
reimported, instantiated or read by this cell. See §6 for the one place the undead *mesh* is unavoidably co-resident.

**Stack:** Godot `4.6.3.stable.official.7d41c59c4`, Forward+, macOS arm64, project
`/Users/admin/Games/reincarnated-godot` (`config/features=("4.6","Forward Plus")`).

---

## §0 — Headline verdicts

| Rider | Verdict |
|---|---|
| **T-3(a)** import | **LOADS-DIRTY(missing-embedded-texture)** — scene, skeleton, skin and 2 materials all build; **zero albedo textures bind**. Two ERRORs + one WARNING, verbatim in §1.2. |
| **T-3(b)** bone census | **52 bones** on `SK_Chr_Werewolf_01.fbx` (Unreal_Characters, UE naming) — **not 51**. The 51-bone rig is a *different file*, `SM_Werewolf_01.fbx` (generic/Unity naming). Both enumerated in §2. |
| **T-3(c)** bone-map applicability | **RETARGET-READY.** Existing `sidekick_bone_map.tres` applies unmodified. 40/52 bones map to `SkeletonProfileHumanoid`; **mean AND max rest Δ over all 40 profile bones = 0.0000°** against the hero body, the boss body, and the base-locomotion clip character. Caveats (all non-blocking) in §3.3. |
| **T-3(d)** SM_ meshes + materials | **LOAD.** 2 meshes / 2 materials confirmed for the werewolf body, matching `MaterialList_PolygonWerewolf.txt`. All materials carry `albedo_texture = <null>` (same defect as T-3(a)). |
| **T-4** glyph coverage | **0 / 6 COVERED. All six STILL-MISSING.** The menus pack ships **no element family and no ailment family** — its 1,377 PNG are menu-functional icons, generic fantasy motifs, and 653 platform input prompts. The L8 arm-2 purchase-fork HALT **does not dissolve**. |

---

## §1 — T-3(a): does `SK_Chr_Werewolf_01.fbx` import clean?

### 1.1 Method (and why the first attempt did not count — L-N)

Asset: `/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/SK_Chr_Werewolf_01.fbx`
(686,944 bytes, mtime 2024-02-11).

The file arrived already `.import`-touched (charter §1.3), so a plain `--headless --import` is a **no-op** and would
have recorded a false CLEAN. Two instrument steps were needed:

1. Deleting only `.godot/imported/SK_Chr_Werewolf_01.fbx-71f7f93449e1539fd6fc6854bbf06205.md5` did **not** trigger
   reimport — the `.scn` kept its 2026-07-23 00:22 mtime and byte size 267718. **That pass proves nothing and is
   discarded.** (Log retained: `tmp/pcw1a/reimport.log`.)
2. Deleting the **dest artifact** `.scn` did trigger a true reimport: new `.md5` + new `.scn` written 20:31,
   267719 bytes, sha256 `33ef877f…689127` vs the prior `8b66c218…113fff`. The 1-byte delta is Godot's
   per-import sub-resource ID string (`StandardMaterial3D_ic5we` etc.), i.e. a genuinely fresh import.
   Command: `/Applications/Godot.app/Contents/MacOS/Godot --headless --import --path .` → **exit 0**.

Control for L-N: the pack's albedo texture loads standalone —
`res://Assets/Synty/polygon-werewolf/SourceFiles/Textures/PolygonWerewolf_Texture_01_A.png` → **OK 4096×4096**.
So the load path is verified good before any NO is recorded.

### 1.2 Verbatim import output (from `tmp/pcw1a/reimport2.log`, lines 44–52)

```
[   0% ] reimport | SK_Chr_Werewolf_01.fbx
[   0% ] import | Started Import Scene (104 steps)
[   0% ] import | Importing Scene...
ERROR: Resource file not found: res:// (expected type: Texture2D)
   at: _load (core/io/resource_loader.cpp:351)
ERROR: Can't open file from path 'res://Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/PolygonFantasyGothic_Texture_01.psd'.
   at: get_file_as_bytes (core/io/file_access.cpp:942)
WARNING: FBX: Image index '0' couldn't be loaded from path: res://Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/PolygonFantasyGothic_Texture_01.psd because there was no data to load. Skipping it.
     at: _parse_images (modules/fbx/fbx_document.cpp:1084)
```

Plus, at project-scan level (lines 332–335):

```
WARNING: Case mismatch opening requested file '/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-werewolf/SourceFiles/textures/PolygonWerewolf_Texture_01_A.png', stored as '/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-werewolf/SourceFiles/Textures/PolygonWerewolf_Texture_01_A.png' in the filesystem. This file will not open when exported to other case-sensitive platforms.
     at: open_internal (drivers/unix/file_access_unix.cpp:116)
```

Nothing else in the 334-line log is attributable to this asset. (The other WARN/ERROR lines in that log —
`another project.godot at res://Assets/Synty/polygon-starter`, four `UID duplicate` on
`polygon-dark-fantasy-01` capes, the `VFXLoot` parse error — are pre-existing project-wide conditions
present before this cell and unrelated to the werewolf. Logged in §5.)

### 1.3 What the errors mean, factually

The FBX embeds an image reference to **`PolygonFantasyGothic_Texture_01.psd`** — a texture from a *different*
Synty pack, in a format Godot cannot read, and **not present anywhere in this pack** (the pack ships 8 PNG,
`PolygonWerewolf_Texture_0{1..4}_{A,B}.png`). Godot skips it. Measured consequence
(`tmp/pcw1a/matprobe.gd`): **every werewolf material imports with `albedo_texture = <null>`.**

```
=== SK_Chr_Werewolf_01 ===
  MESH SM_Werewolf_Mesh_01 aabb=[P: (-1.525659, -0.017109, -0.30443), S: (3.051318, 1.821218, 0.688771)] surfaces=2
    surf[0] name=lambert1407 albedo_tex=<null> albedo_color=(0.9063, 0.9063, 0.9063, 0.8) verts=12816
    surf[1] name=lambert1408 albedo_tex=<null> albedo_color=(0.6652, 0.6652, 0.6652, 1.0) verts=48
```

Geometry, skin and skeleton are intact. Only the albedo binding is absent. **Verdict: `LOADS-DIRTY(missing-embedded-texture)`.**
The case-mismatch warning is a separate, export-portability-only concern (lowercase `textures/` requested,
`Textures/` on disk); it does not affect the Mac render path.

---

## §2 — T-3(b): bone census

Method: `tmp/pcw1a/census.gd`, run headless. To recover **raw source** bone names (the canonical `.import`
applies a bone renamer), a scratch copy of the FBX was imported with default options, censused, then deleted —
see §6.

### 2.1 `SK_Chr_Werewolf_01.fbx` — the R-PC-1/R-PC-4 body — **52 bones**

Node tree: `SK_Chr_Werewolf_01 <Node3D>` → `GeneralSkeleton <Skeleton3D>` → `SM_Werewolf_Mesh_01 <MeshInstance3D>`.
No AnimationPlayer.

Raw source bone names, in index order (parent in parentheses):

```
 0 root(-)              13 hand_l(12)          26 hand_r(25)          39 foot_l(38)
 1 pelvis(0)            14 thumb_01_l(13)      27 thumb_01_r(26)      40 ball_l(39)
 2 spine_01(1)          15 thumb_02_l(14)      28 thumb_02_r(27)      41 thigh_r(1)
 3 spine_02(2)          16 thumb_03_l(15)      29 thumb_03_r(28)      42 calf_r(41)
 4 spine_03(3)          17 index_01_l(13)      30 index_01_r(26)      43 foot_r(42)
 5 neck_01(4)           18 index_02_l(17)      31 index_02_r(30)      44 ball_r(43)
 6 head(5)              19 index_03_l(18)      32 index_03_r(31)      45 ik_foot_root(0)
 7 jaw(6)               20 middle_01_l(13)     33 middle_01_r(26)     46 ik_foot_l(45)
 8 eyebrows(6)          21 middle_02_l(20)     34 middle_02_r(33)     47 ik_foot_r(45)
 9 eyes(6)              22 middle_03_l(21)     35 middle_03_r(34)     48 ik_hand_root(0)
10 clavicle_l(4)        23 clavicle_r(4)       36 Belly_01(2)         49 ik_hand_gun(48)
11 upperarm_l(10)       24 upperarm_r(23)      37 thigh_l(1)          50 ik_hand_l(49)
12 lowerarm_l(11)       25 lowerarm_r(24)      38 calf_l(37)          51 ik_hand_r(49)
```

Post-retarget (as the project actually ships it), the same 52 in `GeneralSkeleton` space:

```
 0 Root                 13 LeftHand            26 RightHand           39 LeftFoot
 1 Hips                 14 LeftThumbMetacarpal 27 RightThumbMetacarpal 40 ball_l
 2 Spine                15 LeftThumbProximal   28 RightThumbProximal  41 RightUpperLeg
 3 Chest                16 LeftThumbDistal     29 RightThumbDistal    42 RightLowerLeg
 4 UpperChest           17 LeftIndexProximal   30 RightIndexProximal  43 RightFoot
 5 Neck                 18 LeftIndexIntermediate 31 RightIndexIntermediate 44 ball_r
 6 Head                 19 LeftIndexDistal     32 RightIndexDistal    45 ik_foot_root
 7 Jaw                  20 LeftMiddleProximal  33 RightMiddleProximal 46 ik_foot_l
 8 eyebrows             21 LeftMiddleIntermediate 34 RightMiddleIntermediate 47 ik_foot_r
 9 eyes                 22 LeftMiddleDistal    35 RightMiddleDistal   48 ik_hand_root
10 LeftShoulder         23 RightShoulder       36 Belly_01            49 ik_hand_gun
11 LeftUpperArm         24 RightUpperArm       37 LeftUpperLeg        50 ik_hand_l
12 LeftLowerArm         25 RightLowerArm       38 LeftLowerLeg        51 ik_hand_r
```

Hierarchy is preserved exactly under the rename; the 12 unmapped bones keep their source names.

### 2.2 Where the "51" is — a naming-collision finding

The 51-bone figure from Synty's product page corresponds to a **different file**:
`Assets/Synty/polygon-werewolf/SourceFiles/FBX/SM_Werewolf_01.fbx` — the generic-naming (Unity-lineage) rig,
**51 bones**, `Root / Hips / Spine_01..03 / Neck / Head / Eyebrows / Eyes / Jaw / Clavicle_L / Shoulder_L /
Elbow_L / Hand_L / Thumb_01..03 / IndexFinger_01..04 / Finger_01..04 / (mirror _R via `_2` suffixes) /
Belly_01 / UpperLeg_L / LowerLeg_L / Ankle_L / Ball_L / Toes_L / (mirror _R)`.

The two rigs differ in more than naming: the generic rig has **4-joint fingers and explicit Toes**; the UE rig
has **3-joint fingers, no Toes, and 7 `ik_*` helper bones**. 51 vs 52 is that trade, not a discrepancy in
the ruled body. **The R-PC-1/R-PC-4 body is the 52-bone `SK_Chr_Werewolf_01.fbx`.**

### 2.3 The tail is a separate skeleton

`SM_Werewolf_Tail_01.fbx` carries its own 5-bone chain `Tail_01 → Tail_02 → Tail_03 → Tail_04 → Tail_05`,
**root-parented, not attached to the body skeleton**. `SK_Chr_Werewolf_01.fbx` contains **no tail bones and no
tail mesh**. Attaching the tail is separate work, not covered by this rider. Logged in §5.

### 2.4 No animation content ships with the body

`tmp/pcw1a/animprobe.gd`:

```
SK_Chr_Werewolf_01 : AnimationPlayer x0
SM_Werewolf_01 : AnimationPlayer x1
    clip 'Take 001' len=5.417s tracks=5
SM_Werewolf_Tail_01 : AnimationPlayer x1
    clip 'Take 001' len=5.000s tracks=0
```

`Take 001` is the FBX default-take placeholder (5 tracks on a 51-bone rig; 0 tracks on the tail), not authored
motion. **The werewolf pack ships zero usable animation clips.** The L6 ladder must source motion from the
Synty animation packs and retarget — which §3 measures as clean.

---

## §3 — T-3(c): bone-map applicability

### 3.1 Lineage — the map is already applied, by my own R4/KT-2 pass

`Assets/Synty/polygon-werewolf/SourceFiles/FBX/Unreal_Characters/SK_Chr_Werewolf_01.fbx.import` already carries:

```
_subresources={
"nodes": {
"PATH:Skeleton3D": {
"retarget/bone_map": Resource("uid://wmbil1kpwowa", "res://addons/sidekick_creator/sidekick_bone_map.tres"),
"retarget/bone_renamer/rename_bones": true,
"retarget/bone_renamer/unique_node/make_unique": true,
"retarget/bone_renamer/unique_node/skeleton_name": "GeneralSkeleton",
"retarget/rest_fixer/apply_node_transforms": true,
"retarget/rest_fixer/fix_silhouette/enable": true,
"retarget/rest_fixer/keep_global_rest_on_leftovers": true,
"retarget/rest_fixer/normalize_position_tracks": true,
"retarget/rest_fixer/overwrite_axis": true,
"retarget/rest_fixer/reset_all_bone_poses_after_import": true
}
}
}
```

Provenance is **not** the `sidekick_creator` post-import plugin — that plugin gates on
`addons/sidekick_creator/sidekick_root` (default `res://Assets/Synty/SidekickCharacters/`), which the werewolf
path does not match. It is **`scripts/kt2_apply_retarget.py`** (drax KT-2, 2026-07-23), whose `MESHES` list
includes `polygon-werewolf/.../SK_Chr_Werewolf_01.fbx` at entry 12 of 22, and whose `RETARGET_BLOCK` is
byte-identical to the block above. `scripts/kt2_verify_retarget.gd` already asserts the werewolf as
`RT_PASS`. **The werewolf was provisioned into the retarget lineage before this run existed.**

### 3.2 The diff, measured

`SkeletonProfileHumanoid` membership over the imported werewolf skeleton (`tmp/pcw1a/restdelta2.gd`):

- **MAPPED (40)** — `Root, Hips, Spine, Chest, UpperChest, Neck, Head, Jaw, Left/RightShoulder,
  Left/RightUpperArm, Left/RightLowerArm, Left/RightHand, Left/Right {Thumb,Index,Middle} ×3,
  Left/RightUpperLeg, Left/RightLowerLeg, Left/RightFoot`
- **LEFTOVER (12, keep original names)** — `eyebrows, eyes, Belly_01, ball_l, ball_r, ik_foot_root,
  ik_foot_l, ik_foot_r, ik_hand_root, ik_hand_gun, ik_hand_l, ik_hand_r`
- **PROFILE SLOTS UNFILLED (16)** — `LeftEye, RightEye, Left/Right {Ring,Little} {Proximal,Intermediate,Distal}
  (12), LeftToes, RightToes`
  *(`LeftToes`/`RightToes` are already empty strings in `sidekick_bone_map.tres` — unfilled by design, not by
  the werewolf.)*

**No unmapped bone is load-bearing for animation.** The 12 leftovers are 7 UE IK helper bones (inert; no skin
weights drive them in a Godot render), 2 facial bones, 1 belly jiggle bone, and 2 foot-ball bones.

### 3.3 Rest-Δ, by the TCP-43 methodology

TCP-43 established that name-match ≠ rig-match and cost a render to see it (~28° mean / 180° max on unretargeted
pairs). Applying the same instrument — per-bone global-rest basis quaternion angle, over shared bone names —
between the retargeted werewolf and each reference body already running the same map
(`tmp/pcw1a/restdelta2.log`):

| Reference | class | n | mean Δ | max Δ |
|---|---|---:|---:|---:|
| `SK_Chr_Male_Wizard` (hero) | **profile** | **39** | **0.0000°** | **0.0000°** |
| `SK_Chr_Male_Wizard` (hero) | leftover | 11 | 64.3602° | 90.0000° |
| `SK_Chr_ZombieBoss_Wretch_01` (boss body) | **profile** | **40** | **0.0000°** | **0.0000°** |
| `SK_Chr_ZombieBoss_Wretch_01` (boss body) | leftover | 12 | 59.2985° | 90.0000° |
| `A_MOD_BL_Walk_F_Masc` (clip character, 121 bones) | **profile** | **40** | **0.0000°** | **0.0000°** |
| `A_MOD_BL_Walk_F_Masc` (clip character, 121 bones) | leftover | 9 | 92.9640° | 179.2870° |

**Every humanoid-profile bone sits at exactly 0.0000° against all three references** — the hero the game
already runs, the boss body TCP-43 measured, and the character the base-locomotion clips were authored on.
`rest_fixer/overwrite_axis` + `fix_silhouette` normalise the profile chain into a common rest, which is
precisely the condition TCP-43 found *absent* pre-retarget. Whole-skeleton means (all shared bones, no class
split — `tmp/pcw1a/restdelta.log`) are **14.16°** vs hero and **13.68°** vs boss; both figures are carried
entirely by the `ik_*` helpers (90.00° by construction) and `eyebrows`/`eyes` (34.88°), which no retargeted
clip drives.

Bone-name overlap with the boss body is **52/52, zero on either side unmatched**.

### 3.4 **VERDICT: RETARGET-READY**

`sidekick_bone_map.tres` applies unmodified. No new map is required. No bone is unmapped that a retargeted
humanoid clip would drive. Caveats, all recorded as facts rather than problems:

1. **Three fingers per hand, not five.** Ring and Little (12 profile slots) have no target. Clips authored on
   the 5-finger Sidekick rig will drop those 12 tracks. Irrelevant at ARPG camera distance; named so it is
   never re-discovered as a surprise.
2. **One `eyes` bone, not `eye_l`/`eye_r`.** `LeftEye`/`RightEye` unfilled — no eye-aim retarget.
3. **No Toes.** Matches the map, which already leaves Toes empty. `ball_l`/`ball_r` retain source names and
   `keep_global_rest_on_leftovers`.
4. **The `ik_*` bones read 90.00° Δ.** Expected: they are UE authoring helpers with no skin weights. They are
   not evidence against the retarget; excluding them is the correct read, and the profile figure is 0.0000°
   with or without that exclusion.
5. **The tail is not in this skeleton** (§2.3).

---

## §4 — T-4: menus glyph coverage

### 4.1 The six glyphs, sourced

From the L8 arm-2 record —
`agentic_orchestration/drax/notes/2026-07-25-tcp-l8u2-dark-fantasy-kit-report.md` §7(d), verbatim:

> `holy`, `shadow`, `physical` have **no glyph anywhere in the 3,573-PNG kit**; nor do the
> `knockback`, `consecrate`, `freeze` ailments.

Elements: **holy, shadow, physical.** Ailments: **knockback, consecrate, freeze.**
The fork options recorded there were (i) commission, (ii) **buy a second Synty interface pack**, (iii) re-scope
the display element set. This rider tests (ii) against the pack that has since landed.

### 4.2 What the pack actually contains

`/Users/admin/Games/reincarnated-godot/Assets/Synty/interface-dark-fantasy-menus/SourceFiles/`
— **2,784 files, 1,377 PNG.**

| Family | count | content |
|---|---:|---|
| `Core/Icons_Input/` (7 platform families) | **653 PNG** | Platform button prompts only: `GamepadGeneric` 50 · `MouseKeyboard` 38 · `PlayStation` 83 · `SteamController2026` 128 · `SteamDeck` 128 · `Switch` 136 · `Xbox` 90. Filenames are `ICON_Input_<Platform>_{Button,Dpad,Stick,Trackpad,…}_*_{Clean,Stroke,Underlay}.png`. |
| `Core/Icons_Social/` | 7 | Discord, Facebook, Instagram, Synty, TikTok, X, YouTube |
| `Core/Branding/` | 2 | Synty logo / interface branding |
| `Sprites/Icons_DarkFantasyMenus/` | 37 | Chest ×4(+Currency variants), Coin/Gem/Rune, Arrow, Book, **Cross**, Exit, Flag(s), Helmet, Key, Medal, Multiplayer, Plus, Scroll, Settings, Swords |
| `Sprites/Icons_DarkFantasyMenus_Flat/` | 93 (31 bases × Clean/Stroke/Underlay) | Chest, Currency, Eye ×3, Hand, Heart, Key, **Sigil ×6**, **Skull ×3**, **Spell ×3**, **Sword ×3** |
| `Sprites/Icons_Menu/` | 72 (24 bases) | Cancel, Delete, Display, Link, Load, Lock, Message, Music, Notification, Quit, Refresh, Save, Settings, Shop, Sound, Trophy, Warning |
| `Sprites/Icons_Settings/` | 24 (8 bases) | Camera, Color, Contrast, Controls, Filters, Frame, Headphones, Picture |
| `Sprites/DarkFantasyMenus/` | 371 | Frames, bars (H/V/scroll), boxes, arrow buttons — compositing rigs (`_Left`/`_Right`/`_TopLeft`…), not 9-slices |
| `Sprites/General/` | 58 | Boxes, parchment panels, gradients, vignettes, indicator lines, sigil rings/diamonds/triangles, `General_DemonicGlyphs` |
| `Sprites/{FX,Cursors,Fonts}/` | 10 / 9 / 2 | Glows, fire sheet, gem sheen · crosshairs + pointers · font sheets |
| `DarkFantasyMenus/` (top level) | 21 | Branding plates + example screenshots (ARPG, Soulslike, Shooter, 1st/3rd person, DarkShrine) and hero/scene art |
| `FBX/` + `Textures/` | 3D menu props | Chest/Coin/Gem/Key/Rune meshes + 2 atlas textures |

**There is no `Icons_Elements` folder and no ailment folder in this pack.** Exhaustive
case-insensitive filename search across all 2,784 files:

```
holy: 0   shadow: 0   physical: 0   knockback: 0   consecrate: 0   freeze: 0
frost: 0  ice: 0      light: 0      divine: 0      bleed: 0        poison: 0
burn: 0   stun: 0     element: 0
```

(`dark: 1398` is the `DarkFantasyMenus` filename prefix, not content.)

### 4.3 Eyes-on the plausible substitutes (L-A / TCP-30 — names are not the artifact)

Filename absence is not depiction absence, and one of L8 arm-2's own findings was that a Synty asset named
`Cross` was not what the name suggested. So the 24 closest candidates were rendered to a contact sheet
(`/Users/admin/Games/reincarnated-godot/tmp/pcw1a/glyph_candidates.png`) and **looked at**:

- `SPR_DarkFantasyMenus_Icon_Cross_01` — **not a religious cross.** Two dark crossed timbers, an X-brace /
  barricade motif. Not a `holy` glyph. (Confirms the arm-2 reading of this shape.)
- `Sigil_01..06` — abstract dark-fantasy sigils: an arrow-and-bar mark, a bordered eye-star, a triangle-and-blade,
  a four-point starburst, a dagger-flanked diamond, a dripping-blood mark. **None element-specific.**
- `Skull_02/03/04` — skulls (one wreathed in flame). Read as death/undead, not the `shadow` element.
- `Spell_01/02/03` — a swirling vortex, twin shards, a rising flame-claw. Generic magic, no element identity.
- `Sword_01/02/03`, `Swords_01`, `Helmet_01` — weapons and armour, not a damage-type glyph in the HUD register.
- `Eye_01` — radiant eye in a sunburst. Nearest thing to a divine mark in the pack; still an eye, not a
  `holy` element glyph, and it already reads as "vision/reveal" in menu context.
- `General_DemonicGlyphs` — a strip of decorative rune-marks (border ornament, not discrete icons).
- `Heart_01` (broken heart), `Warning_01`, `Medal_01` — unrelated.

**Nothing in the pack depicts ice, frost or freezing in any form. Nothing depicts displacement or knockback.
Nothing depicts consecration/ground-blessing.**

### 4.4 Per-glyph verdict

| # | glyph | class | verdict | evidence |
|---|---|---|---|---|
| 1 | `holy` | element | **STILL-MISSING** | 0 filename hits (`holy`/`divine`/`light`). Nearest depiction `…_Flat/ICON_DarkFantasyMenus_Eye_01_*.png` (radiant eye) and `…/SPR_DarkFantasyMenus_Icon_Cross_01.png` — the latter inspected and is a **timber X-brace, not a religious cross**. No holy symbol in the pack. |
| 2 | `shadow` | element | **STILL-MISSING** | 0 filename hits. Nearest are `Skull_02/03/04` (death/undead register) and `Sigil_01..06` (abstract). No shadow/darkness element glyph. |
| 3 | `physical` | element | **STILL-MISSING** | 0 filename hits. `Sword_01..03` / `Swords_01` are weapon icons in a menu register, not the HUD damage-type glyph the element row needs. |
| 4 | `knockback` | ailment | **STILL-MISSING** | 0 filename hits. No displacement/impact/prone depiction anywhere in the pack. The arm-2 §7(e) `Down_01` collision with `stun` is **unaffected** — this pack adds nothing to it. |
| 5 | `consecrate` | ailment | **STILL-MISSING** | 0 filename hits. No ground-rune, blessing-circle or sanctified-area depiction. `Sigil_Ring_*` in `Sprites/General/` are decorative UI rings, not ground-effect glyphs. |
| 6 | `freeze` | ailment | **STILL-MISSING** | 0 filename hits for `freeze`/`frost`/`ice`. **No cold imagery of any kind** in 1,377 PNG. |

**COVERED: 0 / 6. STILL-MISSING: 6 / 6.**

### 4.5 What this settles

Charter §2 T-4 asked: does `Core/Icons_Input` cover L8 arm-2's 6 missing glyphs? **No** — and the reason is
categorical rather than marginal: `Icons_Input` is a **platform-button-prompt** library (653 PNG across 7
controller families) and the pack as a whole ships **no element and no ailment icon family**. This is a
menus/shell pack; the L8 kit's `Icons_Elements` has no counterpart here.

**The purchase fork does NOT dissolve.** Arm-2 option (ii) — "buy a second Synty interface pack and accept a
register seam" — is **not satisfied by this particular pack**. Options (i) and (iii) remain untouched, and
whether (ii) survives as a route depends on a *different* pack existing, which is not a question this rider
was scoped to answer. Matt's fork stands as recorded.

*(Adjacent fact, offered as evidence not as a request: `Icons_Input`'s 7 platform families would cover a
different open surface — controller/keybind prompts — which the L8 laps have not yet needed. Logged in §5.)*

---

## §5 — Findings logged for the conductor (NOT acted on)

| # | finding | evidence |
|---|---|---|
| F1 | **The werewolf FBX references a foreign pack's texture.** `PolygonFantasyGothic_Texture_01.psd` is embedded as image index 0 and does not exist in this pack. Consequence: all albedo bindings null on every werewolf mesh. Fix would be manual material authoring against `Textures/PolygonWerewolf_Texture_01_A.png` (loads fine, 4096²) — **not done; out of rider scope.** | §1.2, §1.3 |
| F2 | **51 vs 52 is a two-rig fact, not an error.** Synty's product-page 51 is `SM_Werewolf_01.fbx` (generic naming, 4-joint fingers, Toes). The ruled body is `SK_Chr_Werewolf_01.fbx` at 52 (UE naming, 3-joint fingers, 7 `ik_*`). | §2.1, §2.2 |
| F3 | **No tail on the body rig.** The tail is a standalone 5-bone skeleton in `SM_Werewolf_Tail_01.fbx`, unparented to the body. A werewolf with a tail requires an attachment step nobody has scoped. | §2.3 |
| F4 | **The werewolf pack ships zero animation.** Only FBX default `Take 001` placeholders. L6's second body has no native motion; every clip must be retargeted in. | §2.4 |
| F5 | **The retarget was already provisioned by drax KT-2 (2026-07-23), not by this run.** `scripts/kt2_apply_retarget.py` applied the identical block to 22 bodies incl. the werewolf; `kt2_verify_retarget.gd` already lists it. This rider *measured* a pre-existing state rather than creating one. | §3.1 |
| F6 | **`SM_Werewolf_01.fbx` bundles the undead mesh in the same file** as the normal mesh (`SM_Werewolf_Mesh_01` + `SM_Werewolf_Undead_Mesh_01`, materials `lambert1407/1408` and `Gothicc2/lambert1409`). R-PC-1 forbids the undead *variant*; the SM_ census required by T-3(d) cannot open the file without the undead mesh being co-resident in the scene tree. **The undead SK_ rig was never touched.** If R-PC-1 is meant to extend to the co-resident mesh, that is the conductor's ruling, not mine. | §6 |
| F7 | **Pre-existing project-wide import noise, unrelated to this cell** (present before it, unchanged by it): a nested `project.godot` at `res://Assets/Synty/polygon-starter` (folder ignored); 4 × `UID duplicate` between `Assets/Synty/PolygonDarkFantasy/Models/extracted/` and `Assets/Synty/polygon-dark-fantasy-01/…` cape `.res` files; a `VFXLoot`/`VFXEffect` GDScript parse error in `res://assets/BinbunVFX/loot_effects/src/script/vfx_loot.gd`; and case-mismatch warnings on `textures/` vs `Textures/` across **8 Synty packs**, not just the werewolf. | `tmp/pcw1a/reimport2.log` |
| F8 | **`godot --headless --import` rewrites `project.godot` and prunes settings equal to engine defaults.** This run's pass silently deleted `[rendering] mesh_lod/lod_change/threshold_pixels=1.0`. **Restored by hand; `git diff project.godot` is empty.** Any future headless-import cell will do this again — worth knowing before it lands in a commit as an invisible diff. | §6 |
| F9 | **A deleted `.md5` does NOT force reimport on 4.6.3** — only deleting the dest `.scn` does. Any cell that "verified a clean import" by clearing `.md5` alone verified nothing (L-N). | §1.1 |
| F10 | `Core/Icons_Input`'s 653 PNG across 7 platform families would serve a **controller/keybind-prompt** surface the L8 laps have not yet opened. Offered as inventory, not as a proposal. | §4.2 |

---

## §6 — Exactly what changed in `reincarnated-godot` (nothing committed there)

**No commit was made in `reincarnated-godot`.** Changes, complete:

1. **`project.godot`** — modified by the headless import pass (dropped `[rendering]
   mesh_lod/lod_change/threshold_pixels=1.0`), then **restored by hand**. `git diff project.godot` → **empty**.
   Net change: **none**.
2. **`.godot/imported/SK_Chr_Werewolf_01.fbx-71f7f93449e1539fd6fc6854bbf06205.{scn,md5}`** — regenerated by the
   forced reimport (267718 → 267719 bytes; sha256 `8b66c218…` → `33ef877f…`; delta is per-import sub-resource ID
   strings). `.godot/` is **gitignored** (`.gitignore:52`). Derived cache only.
3. **No `.import` sidecar in `Assets/` was created, modified or deleted by this cell.**
   `git status --porcelain -- Assets` → **0 entries.** The werewolf and menus packs both arrived already
   `.import`-touched; the import pass found nothing new to write there.
4. **Scratch, created and then removed:** `tmp/pcw1a/WW_RAW.fbx` (a copy of the werewolf FBX imported with
   default options to recover pre-rename bone names) + its `.import` + its two `.godot/imported/WW_RAW.fbx-*`
   artifacts. **All four deleted.** No duplicate werewolf rig remains in the project.
5. **Scratch retained** under `/Users/admin/Games/reincarnated-godot/tmp/pcw1a/` as this note's evidence:
   `census.gd`, `matprobe.gd`, `restdelta.gd`, `restdelta2.gd`, `animprobe.gd`, `census.log`, `reimport.log`,
   `reimport2.log`, `restdelta.log`, `restdelta2.log`, `scn_before.sha`, `glyph_candidates.png`.
   `tmp/` was already untracked-and-uncommitted before this cell.
6. **`SK_Chr_Werewolf_Undead_01.fbx` — untouched.** Not loaded, not instantiated, not reimported; its
   `.import` and its `.godot/imported/` artifacts carry their 2026-07-23 timestamps. The one place the undead
   *mesh* appears is inside `SM_Werewolf_01.fbx`, which bundles both meshes — see F6.

---

## §7 — Rider exit

| charter target | status |
|---|---|
| T-3(a) FBX imports clean into the Godot project | ✅ measured — **LOADS-DIRTY(missing-embedded-texture)**, verbatim errors §1.2 |
| T-3(b) bone census captured | ✅ **52 bones** enumerated raw + post-retarget §2.1; the 51-bone rig located and named §2.2 |
| T-3(c) diffed against the bone-map lineage; applicability VERDICT | ✅ **RETARGET-READY** — 40/52 mapped, **0.0000° profile rest Δ** vs hero / boss / clip-character §3.3–3.4 |
| T-3(d) SM_ meshes + materials load (2 meshes / 2 materials) | ✅ **load**, 2 meshes / 2 materials confirmed against `MaterialList_PolygonWerewolf.txt`; all albedo null §1.3 |
| T-3(d′) werewolf registered as L6 second body in the ladder brief | ⬜ **not mine** — ladder brief is the conductor's document; this note supplies the facts it needs |
| T-4 glyph-coverage answer | ✅ **0/6 COVERED** — six per-glyph verdicts §4.4; **HALT does not dissolve** §4.5 |

**Boundary held:** LOADS?/REACHES?, never BETTER. No judgement offered on whether the werewolf is a *good*
caster body, whether the missing albedo *should* be authored, or which fork option Matt should take.

---

**Signed:** drax (presentation seam), 2026-07-28.
Evidence root: `/Users/admin/Games/reincarnated-godot/tmp/pcw1a/`
