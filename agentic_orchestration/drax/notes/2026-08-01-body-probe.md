# BODY-PROBE — BR-1 (BATON-RENDER), drax, 2026-08-01

**Cell question (Scope 37 + amendments, Scope 38 R1/R3):** which body does the player
wear in the final watch, and what does it swing?

**Single-writer:** opened at godot `4f1a3ca` (BEAM-SLITS), the named head. No foreign
commits. Landed at `136ff81`.

**No aesthetic self-verdict is taken anywhere in this note.** What binds, what connects,
what reads — measured. Which body *looks* right is the conductor's under Scope 38, and
Matt's on return.

---

## 0. The headline, in one paragraph

The tree does ship authored melee motion. It is in exactly one file, it was never
missing, and it was unreachable for a reason no earlier search could have found by
looking at filenames: its bone names share **zero** entries with every candidate body.
Scope 37's second-amendment hypothesis (the knight's 48 bones are the generation
`Animations_Melee.fbx` targets) is **FALSE — measured 0/21**. But the same measurement
found the bridge the hypothesis was reaching for, and a better one: knight and werewolf
are the **same rig family to the bone (49/49)**, so one retarget serves both and the
clip set does not depend on which body wins. Bridged through
`SkeletonProfileHumanoid`, the melee take now binds **16/18 tracks on every candidate
body**, out-reaches the fidget incumbent by **×1.51** on the knight, and **connects** —
crossing the target hull by −0.5652 m against the incumbent's −0.4539 m.

---

## 1. PART 1 — the clip census

### 1.1 Method, and why it is not a filename search

The standing lesson of this run is that name-driven searches miss things: a `*attack*`
glob missed `Animations_Melee.fbx` for the entire VFX bake-off. So the census was driven
by **content**:

1. Binary sweep of **all 24,576 FBX** under `Assets/Synty` counting `AnimationCurveNode`
   occurrences. (`AnimationStack` is useless as a discriminator — FBX writes one into
   almost every file, including static props. Curve-node count is not.)
2. Every animation-bearing character/animation-shaped file with ≥ 60 curve nodes — **317
   files** — opened in-engine, every clip enumerated, every clip's **track count, length
   and track paths** printed.
3. Discriminator, measured per file rather than assumed: a bind-pose-only FBX writes
   ~3 curve nodes per bone and yields a take of ≲1 frame. Real authored motion yields a
   multi-second take.

Instruments: `scripts/bp_clip_census.gd`, `scripts/bp_census_bulk.gd`.
Artifacts: `tmp/bodyprobe/stats/clip_census.json`, `census_bulk.json`.

### 1.2 What exists — the census result

**263 of 316 clips clear the real-motion bar.** Deduplicated by signature they collapse
to 20 distinct takes. The ones that matter:

| take | len s | tracks | bones | rig root | what it actually is |
|---|---|---|---|---|---|
| `Animations_Melee.fbx` "Take 001" | **11.333** | **20** | 21 | `Root_jnt` | **the only authored melee in the tree** |
| `Animations.fbx` (simple-fantasy) | 44.633 | 21 | 21 | `Root_jnt` | locomotion/idle omnibus, same rig |
| `Chr_Undead_Knight_01.fbx` (embedded) | 8.333 | 31 | 50 | `Root` | showcase turntable |
| Fantasy Rivals `SK_Character_*` (embedded) | 5.967 | 51 | 55 | `Pelvis` | showcase turntable |
| `polygon-dark-fantasy/Characters.fbx` | 5.000 | 52 | 50 | `Root` | showcase turntable |
| `polygon-dark-fortress/Characters.fbx` | 9.115 | 53 | 50 | `Root` | showcase turntable |
| modular-fantasy-heroes parts ×154 | 2.633 | 27 | 48 | `Pelvis` | one shared part-showcase |

**Attack-worded clip names in the whole tree: ZERO.** Not one clip anywhere is called
attack/strike/slash/claw/swipe/melee. The melee bundle's single take is named
`Take 001`. Name-driven search could never have found it; that is the finding.

**Corrections to two standing claims, both partial:**

- *"The MOD_GBL library is locomotion+idles only — censused, zero attack clips."*
  **CONFIRMED, and extended.** There are **two** goblin-locomotion packs on disk, not
  one: `anim-goblin-locomotion` (417 clips, censused before) and
  `polygon-animation-goblin-locomotion`, which additionally carries a whole `Polygon/`
  subtree of `A_POLY_GBL_*` clips nobody had listed. Enumerated this cell: identical
  action set — Crouch / Walk / Run / Sprint / Jump / Land / Turn / Transitions /
  Additives / Idles. **Zero attacks in either.** The claim holds on a bigger corpus.
- *"Fantasy Rivals + the werewolf pack ship ZERO animation FBX between them."* **True
  about FILES, false about the tree.** Synty writes the pack's showcase motion *inside*
  the character FBX as an unnamed take. Every Fantasy Rivals character carries a
  5.967 s / 51-track take; `Chr_Undead_Knight_01` carries an 8.333 s / 31-track take.
  They are not strikes (§1.3), but they are not nothing, and the earlier claim would
  have hidden them permanently.

### 1.3 Which takes are strikes — measured, not assumed

Each take was played and its right hand measured against its hips over the whole clip
(`scripts/bp_take_dissect.gd`). Separation is unambiguous:

| take | hand-reach span m | peak m | verdict |
|---|---|---|---|
| **`Animations_Melee`** | **1.3671** | **1.7141** | authored action set |
| `rivals_ancient_warrior` | 0.5975 | 0.8200 | turntable |
| `darkfantasy_chars` | 0.5773 | 0.8899 | turntable |
| `darkfortress_chars` | 0.4583 | 0.8006 | turntable |
| **`undead_knight` (own take)** | 0.4505 | 0.8369 | **turntable — not a strike** |
| `dr_hero_male` | 0.4505 | 0.8369 | turntable (identical — one shared take) |

The melee take's span is **2.3–3.0× every other take in the tree.** The knight's own
embedded 8.333 s take is *not* an attack; it is the same showcase motion every
dungeon-realms character carries.

> **Instrument defect caught before it produced a verdict.** Run 1 of the dissection
> reported reach span **0.0000 m on every take** — the stale-global-pose hazard banked
> in the VFX-BAKEOFF landing, hit again. `Skeleton3D.get_bone_global_pose()` reads a
> cache that only refills during the skeleton's process step, which never runs in a
> headless `SceneTree` script, so it silently returns the rest pose. Fixed by composing
> forward kinematics by hand from `get_bone_pose()`, which the AnimationPlayer writes
> directly. Every metre in this note is post-fix.

### 1.4 The melee take is unsegmented, and the cut list was recovered

`Animations_Melee.fbx` arrives as one unnamed 11.333 s `Take 001`. There is **no Unity
`.meta` beside it** (checked: zero `.meta` files anywhere under `Assets/Synty`) and **no
clip names inside the FBX** (checked: `strings` over the whole 608 KB shows only Maya
authoring paths). The clip boundaries are recorded nowhere.

Recovered from the motion instead (`scripts/bp_segment_melee.gd`): a Synty showcase take
concatenates individually-authored actions, each starting and ending on the same neutral
pose, so whole-skeleton kinetic energy dips to a floor at every seam and only at a seam.
The check that it worked is that the recovered segments are **action-length**, not
noise-length. Ten segments recovered on the knight; the seven with motion are frozen into
`data/bp_melee_lib.res`:

| slice | window s | dur | peak hand speed m/s | reading |
|---|---|---|---|---|
| `attack_1` | 0.000–1.667 | 1.667 | 13.33 | combo hit 1 |
| `attack_2` | 1.667–3.167 | 1.500 | 13.30 | combo hit 2 |
| `attack_3` | 3.167–4.567 | 1.400 | 11.87 | combo hit 3 (longest reach) |
| `hit_react` | 4.567–5.533 | 0.967 | 18.50 | flinch (sharpest, shortest reach) |
| `guard` | 6.333–7.600 | 1.267 | 5.94 | block/guard |
| `guard_hit` | 7.600–8.700 | 1.100 | 2.46 | guarded impact |
| `knockback` | 8.700–10.233 | 1.533 | 5.94 | knockback |

The tail (10.233–11.333 s) is a held pose: hand travel 0.0002 m. Correctly excluded.

### 1.5 The claw-vs-sword fork **dissolves at the skeleton**

Scope 37 tier 1 asks for "a claw/unarmed strike clip"; tier 2 fires on "sword/humanoid
strikes only". **Measured, that distinction has no referent in this asset.** The
simple-fantasy melee rig has **21 bones and no finger bones at all** — the full list is
root, hips, two 3-joint legs, a 2-joint spine, head, two hat attach points, and two
3-joint arms ending at `Hand_*_jnt`. The take is pure arm-arc rotation. Nothing in it
specifies, or could specify, what the hand holds.

Corroborating: the pack ships `SF_Wep_Claws_01.fbx` — a **claw weapon mesh** — in the
same folder as `SF_Wep_BlackSword_01`, `SF_Wep_Doublesword_01` and the rest, all
authored against this one melee set. The set is weapon-agnostic by construction. It is
neither sword-only nor claw-only; it reads as whatever is in the hand, including nothing.

**Consequence for the chain:** tier 1's gate ("a claw/unarmed strike clip exists AND
retargets cleanly to the werewolf") is satisfiable on the second half and *undecidable*
on the first, because the asset does not carry the distinction. Reported, not ruled.

---

## 2. PART 2 — the body chain

### 2.1 Bone-name-set comparison (Scope 37 2nd amendment, tested not assumed)

`scripts/bp_rig_compare.gd`. Two rigs are the same family iff a clip authored against one
addresses bone paths the other owns — so name-set intersection is the whole test.

**Pre-retarget, against the melee source (21 bones, `Hips_jnt` convention):**

| target | bones | shared / 21 | naming |
|---|---|---|---|
| `Chr_Undead_Knight_01` | 50 | **0 (0.0 %)** | `Root/Hips/Spine_01/Clavicle_L` (POLYGON) |
| `SK_Chr_Werewolf_01` | 52 | **0** | Sidekick→GeneralSkeleton |
| `SK_Knights_Dark_01` | 44 | 0 | `root/pelvis/spine_01` (Unreal) |
| `SK_Chr_DarkLord_Male_01` | 51 | 0 | GeneralSkeleton |
| `SK_Character_Human_Knight` | 48 | 0 | `Pelvis/spine_01` mixed-case |
| `SK_Character_Samurai_Warrior_01` | 48 | 0 | `Pelvis/spine_01` mixed-case |

**Scope 37's second-amendment hypothesis is FALSE: 0/21, not "possibly zero-retarget".**

**But the same matrix found what the hypothesis wanted.** Against
`polygon-adventure-pack/Unity_Version_Mechanim/Characters.fbx` (49 bones, the raw POLYGON
humanoid):

- `Chr_Undead_Knight_01` → **49/49 = 100 %**
- `SM_Werewolf_01` (raw variant) → **49/49 = 100 %**

Knight and werewolf are the **same rig family, exactly.** One retarget serves both; the
clip set is invariant to which body wins the chain.

**Post-retarget, all on `SkeletonProfileHumanoid`:** melee source ↔ knight **19/21
(90.5 %)**; ↔ werewolf and dark lord **17/21 (81.0 %)**.

> **Self-caught error, kept on the record.** The first version of this table named
> `polygon-werewolf/SourceFiles/FBX/SM_Werewolf_01.fbx` for "the werewolf". That is the
> static-mesh variant with raw POLYGON names. The body the watch actually ships is
> `wr2_playback.gd::WEREWOLF_FBX` — the `Unreal_Characters/SK_Chr_Werewolf_01.fbx`
> variant, sidekick-mapped to GeneralSkeleton. The two disagree about every bone name,
> so the original row described a file no scene loads. Both rows are now in the table,
> labelled. Read the path from the shipping constant, never from a guess.

### 2.2 The bridge, and the retarget

Godot's retarget importer renames a rig's bones onto `SkeletonProfileHumanoid`; two rigs
renamed onto the same profile bind each other's tracks regardless of authoring names. So
the bridge is the **profile**, not the family.

- `addons/sidekick_creator/goblin_bone_map.tres` — already in the tree, maps the POLYGON
  convention. Exact fit for knight and werewolf on the whole load-bearing chain
  (Root/Hips/Spine/Chest/UpperChest/Neck/Head/Clavicle/Shoulder/Elbow/Hand/UpperLeg/
  LowerLeg/Ankle/Ball/Toes). Only the finger suffixes differ, which no strike uses.
- `addons/sidekick_creator/sf_melee_bone_map.tres` — **authored this cell** for the
  21-bone simple-fantasy rig. **13 profile slots are left empty rather than guessed**:
  this rig has no clavicles, no neck, no toes, no fingers. `Foot_*_jnt1` is the toe joint
  (child of `Foot_*_jnt`) and maps to `Toes`, not to a second `Foot`.

Applier: `scripts/bp_apply_retarget.py`. The retarget block is copied **byte-for-byte**
from `vfxbo_apply_retarget.py` (→ mobcast → lap1 → rivalcast → kt2). Six cells, one
recipe; the only permitted deviation is the `retarget/bone_map` line.

> **Second self-caught error, and the most dangerous kind.** The lineage block hard-codes
> `"PATH:Skeleton3D"`. That key is the skeleton's **scene path inside that particular
> FBX**, not a literal. The melee bundle's skeleton lives at `Character/Skeleton3D`, so
> the key matched no node and the entire `_subresources` entry was **ignored with no
> warning**: the import succeeded, the reimport logged fine, and the clip came out still
> addressing `Hips_jnt`. A wrong key here fails *exactly* like a successful no-op. Now
> measured per rig from `bp_rig_compare.gd`'s `skeleton_path` output and passed in.

**Retarget angles.** No rest-delta is introduced by this cell: the shipped block carries
`rest_fixer/reset_all_bone_poses_after_import` + `fix_silhouette` + `overwrite_axis`,
byte-identical to the block holding RIVAL-CAST's **0.0000°** certificate. Since the block
is unchanged the certificate transfers; the cell did not re-derive it. Inversion is
excluded empirically instead — all six bodies stand upright and swing in
`PROBE_BEAT_bodies` (§4), which is the failure mode inversion produces.

### 2.3 Measured bind (`scripts/bp_bind_test.gd`)

The standing §4.2 law: a clip that binds zero tracks is not a clip. Nothing below is
inferred from the retarget "having worked" — every body is loaded, every clip attached,
and tracks that **resolve to a real bone index** counted. Unmapped tracks are parked on a
path that resolves to nothing, per the L6 `remove_tracks/unmapped_bones` law.

| body | clip | bound / total | reach span m | verdict |
|---|---|---|---|---|
| **undead_knight** | **MELEE** | **16/18 (88.9 %)** | 0.8620 | MOTION |
| undead_knight | LOCO_sf | 17/19 | 1.0700 | MOTION |
| undead_knight | INC fidget-swipe | **21/95 (22.1 %)** | 0.5886 | MOTION |
| undead_knight | INC land-hard | 22/94 | 0.2563 | weak |
| **werewolf** | **MELEE** | **16/18** | 1.1619 | MOTION |
| werewolf | INC fidget-swipe | 51/95 | 0.8381 | MOTION |
| dark lord | MELEE | 16/18 | 0.8620 | MOTION |
| dr_skeleton_01 | MELEE | 16/18 | 0.8620 | MOTION |

The melee take binds **16/18 on every body tried** — the 2 misses are `Hat_jnt`/`Hat_jnt1`,
headgear attach points correctly unmapped. The incumbent binds **21/95 on the knight**:
74 of its tracks address Sidekick attach/twist/IK bones (`hipAttach_*`, `thigh_twist_*`,
`ik_hand_*`) the POLYGON profile does not carry. **The melee clip is the cleaner bind on
the knight by 4×.**

### 2.4 Strike reach, in the incumbent's own metric

Reporting a new number in a new metric would be unfalsifiable against the 1.7671 m fidget
figure, so `scripts/bp_strike_reach.gd` reuses `vfxbo_reach_probe.gd`'s definition
exactly — **peak forward (+Z) bone-cloud extent, net of the same body's idle-pose extent,
at applied scale** — including its corrections (manual FK, one fresh body per clip,
`free()` not `queue_free()`). Applied scale = `RIG_PLAYER_H` 1.80 m.

**Undead Knight** (native rest 1.7097 m → ×1.0528):

| clip | fwd_net m | lat_net m | bound |
|---|---|---|---|
| **MELEE attack_3** | **+1.7543** | −0.5555 | 16/18 |
| MELEE attack_1 | +1.5024 | −0.5571 | 16/18 |
| MELEE attack_2 | +1.3725 | −0.0371 | 16/18 |
| *INC fidget-swipe (incumbent)* | *+1.1587* | −0.2610 | 21/95 |
| INC land-hard | +0.4753 | −0.3901 | 22/94 |

**Knight on the real strike out-reaches the fidget incumbent ×1.51.**

**Werewolf** (native rest 1.8469 m → ×0.9746):

| clip | fwd_net m | bound |
|---|---|---|
| *INC land-hard (the pounce)* | *+2.0230* | 52/94 |
| **MELEE attack_3** | **+1.3231** | 16/18 |
| *INC fidget-swipe* | *+1.1154* | 51/95 |

On the werewolf the melee strike beats the fidget incumbent **×1.19** but does **not**
beat `land_hard` at +2.0230 m. **`land_hard` is the defect, not a rival** — it is a
landing clip, and its extra 0.70 m is the forward *lunge* that produced Matt's "mildly
jumping forwards" reading. Reach and strike-reading are different quantities here, and
the larger number is the worse clip.

**Honest baseline caveat.** The idle baseline is the Sidekick standing idle, which binds
**0/88 on the knight** and 6/88 on the werewolf — so on both bodies the baseline is
effectively the *rest pose*, not an animated idle. It is the same baseline for every row
on a given body, so within-body comparisons are sound; cross-body absolute comparison
carries that caveat.

### 2.5 Chain step reached, and why each earlier step did not close

- **Step 1 — werewolf keeps the body if a claw/unarmed strike exists and retargets
  cleanly.** *Retarget half: SATISFIED* — the melee set binds 16/18 on the werewolf and
  animates. *Claw/unarmed half: UNDECIDABLE FROM THE ASSET* — §1.5, the 21-bone rig has
  no fingers and the set is weapon-agnostic by construction; the pack ships a claw mesh
  authored against it. No purchase can resolve this (Scope 38 R3) and no measurement can
  either. **Not closed by the probe; routed to the conductor.**
- **Step 2 — Undead Knight.** *Rig-family hypothesis FALSE (0/21)* but **the body works
  anyway**: binds 16/18, animates upright, out-reaches the incumbent ×1.51, and connects
  (§3). Its own embedded 8.333 s take is a turntable, not a strike (§1.3) — that part of
  the lead did not pay off. Nothing about the knight failed.
- **Steps 3/4 — not required.** `SK_Chr_DarkLord_Male_01` was carried through anyway as a
  measured comparator (binds 16/18 identically) and is in the render. `SK_Knights_Dark_01`
  (Unreal `root/pelvis` naming, 0 shared with everything), `SK_Character_Human_Knight` and
  `SK_Character_Samurai_Warrior_01` are **unretargeted and would each need their own bone
  map** — not built, because the chain closed above them. Recorded so the next cell knows
  the cost. Also recorded: the samurai FBX reports a **308.90 m** mesh AABB, a unit-scale
  defect that would need handling before it could ship.

**Both surviving bodies are on the identical clip set.** The werewolf is not a downgrade
path — it is the same 16/18 bind and the same seven slices. The choice is aesthetic, and
this cell does not make it.

---

## 3. Strike-connect (Scope 24/25 law: measured, not eyeballed)

`shoot_bp_probe.gd --mode connect`. Both pairs held at the **identical** separation —
1.267 m, the boss-surface figure the bake-off measured. Hand-to-target-surface computed
live per frame; **negative = inside the target hull = connected.**

| arm | min contact m | reading |
|---|---|---|
| **knight × MELEE attack_3** | **−0.5652** | connects, crosses 0.5652 m into the hull |
| knight × INC fidget-swipe | −0.4539 | connects, crosses 0.4539 m |

**The melee strike crosses 24.5 % deeper** at identical separation. Both cross — the
incumbent's failure was never that it misses geometrically; it is that a fidget-menace
clip *reads* as a fidget. That distinction is the clip's to answer, not the number's.

> **Third self-caught error.** Run 1 yawed both bodies to face the camera and then placed
> the target at `−hb × gap` — **behind** the attacker's own forward axis. Every strike
> swung into empty room and the probe reported a clean, precise, meaningless *"neither
> connects"* (MELEE +0.5542, INCUMBENT +0.3985) that would have read as evidence against
> the melee clip. Run 2 also had `rig.global_transform * (skel.global_transform * pose)`
> — the rig transform applied twice, since `Skeleton3D.global_transform` is already
> world-space — reporting a minimum contact of **+155.66 m**. That one was only caught
> because 155 m is absurd; a 1.5 m version would have shipped.

---

## 4. Parity grades (Scope 29 as amended) — collisions shown, not argued

`shoot_bp_probe.gd --mode parity`, three renders. **Camera untouched** — GD-PARITY proved
it metre-identical to GD's, so the only lever is body scale, and this harness never loads
the CAM-LOCK camera. Base uplift 7.04 / 5.47 = **×1.2871**.

| grade | player m | elite m | boss m | boss ÷ player |
|---|---|---|---|---|
| ×1.00 | 1.800 | 2.000 | 2.750 | 1.5278 |
| ×1.15 | 2.070 | 2.300 | 3.163 | 1.5278 |
| **×1.29** | **2.322** | 2.580 | **3.548** | 1.5278 |

**Collisions, named and in-frame** (drawn as coloured datum sticks + a ground annulus so
the eye checks against a marked reference rather than a number in a note):

- **Boss vs 3.00 m wall course (red datum).** At ×1.00 the boss clears it by 0.25 m. At
  ×1.15 he clears by 0.16 m. **At ×1.29 the boss stands 3.548 m — he is 0.55 m TALLER
  than the wall course.** This is the collision Scope 29 asked to be shown, and it is
  real at the ruled grade.
- **Boss vs 2.40 m beam base (blue datum).** Exceeded at **every** grade, including
  ×1.00 (2.75 > 2.40). The scaling worsens it from +0.35 m to +1.15 m.
- **Player vs 1.80 m GD datum (yellow).** At ×1.29 the player is 2.322 m — the datum is
  a floor marker for how far the whole cast has moved.
- **Frigidring, r = 10.0 m (blue ground annulus).** Legible at all three grades; the ring
  is 20 m across and the cast spans ~6 m even at ×1.29. **No legibility loss found.**
- **Threat-inversion guard.** boss ÷ player is **1.5278 at every grade** — the ratio is
  scale-invariant by construction, so no grade inverts the silhouette. Noted for the
  record: 1.5278 is **not** the GD-correct **1.46** Scope 29 names as the target. Closing
  that would need the boss at 2.628 m (×1.00) or 3.390 m (×1.29) — a *separate* change to
  `RIG_BOSS_H`, not a grade. **Not made here**; flagged as an open ruling.
- **Lycanthropy.** If the knight ships, the 2.10× question dissolves and the grading
  collapses to the clean ×1.29, exactly as Scope 37's amendment predicted. The werewolf
  arm is preserved in `PROBE_BEAT_bodies`.

---

## 5. Deliverables

All under `/Users/admin/Games/reincarnated-godot/tmp/bodyprobe/clips/`. All decode-clean
(`ffmpeg -f null`, zero errors); 1920×970 h264 after the banked even-dimension guard.
Frames pruned after encode: **1.1 GB → 11 MB.**

| clip | frames | sha256 |
|---|---|---|
| `PROBE_BEAT_bodies.mp4` — **the body-verdict surface** | 210 | `6faed2e44bc789a8ecf9c8fa532fb18664fac1378ee9815f3914f3f25bdd3b9d` |
| `STRIKE_CONNECT.mp4` | 170 | `bb30bb13d4dfa6ebdb8a9279d835d326dced190e8bb4a99fc8c121e1a1c8f86a` |
| `PARITY_GRADES.mp4` (all three, in sequence) | 420 | `d88ae4df31089dd30895088b8fda570af17c5925c282908ec8079cb8c9d8e65e` |
| `PARITY_GRADE_100.mp4` | 140 | `d8963e7dbcb074f8da893db212ff49337dece16b788f5cce38357bb803921aac` |
| `PARITY_GRADE_115.mp4` | 140 | `781a195ce56e01620a464371fe2cd28a078c1dfc6db53ac9dbb33566a0b45d69` |
| `PARITY_GRADE_129.mp4` | 140 | `3c7cff246498b636782acd4cd11968d14f5afcd5c318f23b7c916b773c146497` |

**WATCH FIRST: `PROBE_BEAT_bodies.mp4`.** Front row = werewolf / **Undead Knight** / dark
lord on the real melee strike. Back row = the *same three bodies* on the fidget
incumbent, same light, same stage, same frame. That is the whole question in one frame.

Lighting is the watch's lighting flag for flag (WR1 4 rooms, beauty on, walltop 0.685),
off `shoot_mobcast_parade.gd`. Camera geometry is the parade's — the CAM-LOCK camera is
never loaded.

**Committed** (godot `136ff81`, opened at `4f1a3ca`): `scripts/bp_clip_census.gd`,
`bp_census_bulk.gd`, `bp_rig_compare.gd`, `bp_take_dissect.gd`, `bp_bind_test.gd`,
`bp_segment_melee.gd`, `bp_strike_reach.gd`, `bp_apply_retarget.py`,
`scripts/shoot_bp_probe.gd`, `scenes/bp_probe.tscn`,
`addons/sidekick_creator/sf_melee_bone_map.tres`, **`data/bp_melee_lib.res`** (the seven
sliced clips), and all of `tmp/bodyprobe/`.

---

## 6. Gates, honest

- **Single-writer: PASS.** Opened `4f1a3ca`, no foreign commits, landed `136ff81`.
- **F-AH-3 (project.godot `[rendering]` guard): FIRED TWICE, HANDLED.** `--import` stripped
  `[rendering]` + `mesh_lod/lod_change/threshold_pixels=1.0` on both reimports, exactly as
  banked. Snapshot taken before the first import; restored after each. Final hash
  `6bef17eb6dd5e44aa8444cc40cd8b518329c9b688a390e16d03abd688aface8a` — **identical to the
  pre-cell hash.** Snapshot + hash committed at `tmp/bodyprobe/stats/`.
- **F-AH-6 (decode-verify every clip): PASS.** All six, zero decode errors.
- **F-BR-4 (SIMPLE-asset gate): RED at 900 — UNCHANGED.** Identical to the count banked at
  VFX-BAKEOFF (simple-dungeons 516 + simple-town 384). **This cell added zero violations
  by the gate's own reckoning.** Still not this cell's to fix; the queue row stands.
- **F-BR-5 (SIMPLE-line animation fork): STANDS, and this cell consumed it under orders.**
  `polygon-simple-fantasy` is SIMPLE-line and the gate's rule (path components starting
  `simple-`/`simple_`) still does not catch a pack root starting `polygon-`. What is
  consumed is **animation only** — rotation curves. No SIMPLE mesh, material or texture
  enters any scene; the SIMPLE rig is never instantiated. Scope 37 explicitly ordered the
  bundle probed and Scope 38 R3 dissolved the purchase alternative, so the cell executed
  and flags it. **Matt's ruling on the principle is still owed.**
- **Retarget persistence: a real constraint, handled per lineage.** `Assets/Synty/` is
  gitignored, so the `.import` retarget blocks **cannot be committed** and live on this
  Mac's disk only. That is why `bp_apply_retarget.py` is the durable artifact and is
  idempotent (`ALREADY_RETARGETED` / `--revert`), exactly as the five prior cells' appliers
  are. Stock originals snapshotted to `tmp/bodyprobe/stats/ORIG_*.import` (force-added past
  the `*.import` ignore).
- **Scope boundaries honoured.** Beams at A3, WARMTH, HUD grade C, pools and camera all
  inherited untouched — this cell writes no scene the watch loads. No VFX/SFX/JUICE built.
  `UNIFIED_KEY_ENERGY` not flipped. `wr2_playback.gd` **not modified**; wiring the melee
  slices into the watch is the restage's job and `data/bp_melee_lib.res` is the handoff.

## 7. Open, for the conductor

1. **Tier-1's claw question is undecidable from the asset** (§1.5). Both bodies bind the
   identical clip set at 16/18. Needs a ruling, not a measurement.
2. **boss ÷ player is 1.5278, not the GD-correct 1.46** (§4). Scale-invariant, so no grade
   fixes it; needs a `RIG_BOSS_H` change. Not made.
3. **At ×1.29 the boss (3.548 m) exceeds the 3.00 m wall course by 0.55 m** and every grade
   exceeds the 2.40 m beam base. Shown in `PARITY_GRADES.mp4`, not argued.
4. **F-BR-5 principle** still owed from Matt.
5. **Steps 3/4 bodies each need their own bone map** if ever wanted; the samurai also
   carries a 308.90 m unit-scale defect.
