# RIVAL-CAST — the pack has no large rig, and the boss stands on the player's own skeleton

> **Cell:** RIVAL-CAST (BR-1 BATON-RENDER §3 cell #3) — pack import at the R-PC-2 asset home,
> rig-compat + retarget on the conductor's lean, cold-emissive tint, scale call, casting verdict.
> **Agent:** drax (presentation seam). **Conductor:** gandalf (`RUN-CONDUCTOR`).
> **Date:** 2026-07-31. **Gate:** G-2.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` — **Scope 22**
> (casting rulings, delegation, temperature grammar) · Scope 14 (cold pools) · Scope 17 (gap law)
> · Scopes 21/23 (cone + reversed gradient) · the **BEAM-CONE LANDING**.
> Charter: `gandalf/notes/2026-07-31-baton-render-run-charter.md` (R-BR-5, G-2).
> **Inherited:** godot `811c320` LOCAL (ahead 11). **Shipped:** godot `b80d7d9` LOCAL
> (ahead 12, **NOT pushed**).

---

## §0 — The cell in five sentences

**The conductor's lean survives its own gate, and it survives it on the strongest possible
evidence: the ElementalGolem is not merely *compatible* with the werewolf's rig — it IS the
werewolf's rig**, sharing the Matt-locked player body's rest skeleton to four decimals (head
1.6940 m / hips 0.8763 m / foot 0.0811 m on both), which is why its profile rest-Δ against the
player, against the clip character and against the scene-proven DarkLord is **0.0000° mean AND
max** — the werewolf's own certificate, reproduced. **The import step turned out to be a
verification rather than a copy**: the pack has been in the R-PC-2 asset home since the
2026-06-21 catalogue ingest, so what this cell actually added was the retarget. **⚑ The scale
question has an answer Matt will not like, and it is about the pack rather than the cast: NO
Fantasy Rivals rig is natively boss-large** — all nine large-rig candidates measure 1.79–2.05 m
and the lean is 1.8239 m, i.e. **1.0015× the werewolf** — so "one of the larger skeletons/rigs"
cannot be satisfied by *selection*, only by a declared uniform scale (shipped: **2.75 m, ×1.5077,
1.528× the player**). **The cold tint is not a picked colour**: it is `SKY_COLOR` read out of the
level, so the boss and the floor pools are one temperature by construction, and the energy was
solved on a five-rung ladder rather than eyeballed (**0.50** — 0.00 % saturated, and **102.6
points of blue-minus-red away from the warm floor beside it**). **Two of my own instruments
failed and are written down**: a G-2 PASS scored on a clip that was binding 10 of 93 tracks, and
a tint selector that called 96.6 % of its own bounding box "the boss".

---

## §1 — CASTING VERDICT

**CAST: `SK_BR_Character_ElementalGolem_01`** (the conductor's Scope-22 lean). **No fallback
walked.** FortGolem, SpiritDemon and the DarkLord floor were all measured anyway — a fallback
chain nobody measures is a chain nobody can walk in a hurry — and the results are in §2.

The lean's three stated reasons, checked rather than accepted:

| Scope-22 rationale | verdict from this cell |
|---|---|
| (i) large mass sells the 12.0 m nova + 2.32 s wind-up | **HELD, but not for free.** The mass reads; the SIZE does not come with the asset (§4). |
| (ii) the Elemental emissive channel lets it glow cold pale-blue | **HELD, and stronger than expected.** The mask is white-on-black and the golem samples it on **49.11 %** of its vertices — half this body is crystal. The pack's own intent is a luminous golem. |
| (iii) golem gait tolerates trace-driven locomotion | **UNTESTED HERE — declared.** This cell shows authored clips, not trace-driven motion. Foot-slide under kinematic drive is LAP-1 WATCH's to see (R-BR-2 already declares it as named debt). |

---

## §2 — GATE G-2: rig-compat + retarget

### 2.1 Import (R-PC-2) — a verification, reported as one

`Assets/Synty/polygon-fantasy-rivals-pack/PolygonFantasyRivals_Source_Files/Source_Files/` was
**already on disk**, 63 MB against the 62 MB handoff source, placed by the 2026-06-21 catalogue
ingest. Contents confirmed against the conductor's recon: `Characters/` (23 FBX) +
`Characters/Unreal_Characters/` (20 FBX) + `Textures/` (families 01–04 × A/B/C/D, **each with its
`_Emissive`**, plus `FantasyRivals_Texture_Elemental_Emissive.png`, `Mystic_Arms.tga`,
`Runes.tga`) + `FBX/` + `OBJ/` + `MaterialList_PolygonFantasyRivals.txt`. Gitignored by the Synty
licence rule (`/Assets/Synty/`), so **nothing about the asset tree is recoverable from a commit** —
which is why the retarget recipe was promoted to a tracked script (§2.2).

**⚑ Two asset-home conventions coexist in this tree, and the brief cited the minority one.** The
brief said "same layout as `Assets/Synty/PolygonDarkFantasy/`". That home holds only `Models/` and
is a legacy stub; the **57 other packs** — including `polygon-dark-fantasy`, and including the
werewolf pipeline this cast has to match — use the lowercase-dash form
`polygon-<pack>/…SourceFiles/`. The rivals pack already sits in the majority form. **Followed the
live convention, flagged the divergence** rather than creating a third layout.

**Only what the cast needs was retargeted** (charter: "not all 20 rigs") — the lean + its two
named fallbacks. The other 17 rigs remain imported-but-unretargeted, exactly as the catalogue
ingest left them.

### 2.2 The retarget applied — and the L6 law deliberately NOT applied

The block is **byte-identical** to the one the 22 in-tree bodies (including the Matt-locked
werewolf) already carry: `sidekick_bone_map.tres` → `GeneralSkeleton`, `rename_bones`,
`apply_node_transforms`, `fix_silhouette`, `keep_global_rest_on_leftovers`,
`normalize_position_tracks`, `overwrite_axis`, `reset_all_bone_poses_after_import`. Applier:
`reincarnated-godot/scripts/rivalcast_apply_retarget.py` (tracked; the `.import` files it edits
are not).

**The L6 law (`retarget/remove_tracks/unmapped_bones: true`) is available and was not used.**
That is a decision with a reason: the werewolf's own `.import` does not carry it, and L6 §7.3
established *what the law does* — it starves the **`.glb` exporter** of dangling tracks, because
the live `AnimationPlayer` already skips unresolvable tracks while the exporter redirects them
onto bone 0. **This pipeline binds clips in memory through an `AnimationPlayer` and emits no
`.glb`**, so the mechanism the law defends against is not in the path. Measured, not assumed:
zero inversion without it (§2.5). The flag is one word away (`--l6`) if a later cell moves to a
`.glb` emit path, and the applier rewrites the block in place when it flips.

### 2.3 Bone census — RAW (before) and RETARGETED (after)

Raw (`tmp/rivalcast/logs/census_raw.log`) — every Fantasy Rivals `Unreal_Characters` rig arrives
as a plain `Skeleton3D` with **0** humanoid-profile bones and the UE naming
(`root/pelvis/spine_01…/ik_hand_gun`) that `sidekick_bone_map` targets. **The POLYGON (non-Unreal)
mirror uses a different naming entirely** (`Pelvis`, `UpperArm_L`, `indexFinger_01_l`, 55 bones)
which the map does **not** target — confirming the Unreal mirror is the correct convention, the
same one the werewolf pipeline uses.

After (`tmp/rivalcast/logs/g2_r2.log`):

| rig | skeleton | bones | profile | leftover | mesh h | rest head / hips / foot (m) |
|---|---|---:|---:|---:|---:|---|
| **LEAN ElementalGolem** | GeneralSkeleton | 51 | **39** | 12 | 1.8239 | **1.6940 / 0.8763 / 0.0811** |
| FB1 FortGolem | GeneralSkeleton | 51 | 39 | 12 | 1.8827 | 1.6940 / 0.8763 / 0.0811 |
| FB2 SpiritDemon | GeneralSkeleton | 50 | 39 | 11 | 1.9414 | 1.5641 / 0.8763 / 0.0557 |
| FLOOR DarkLord | GeneralSkeleton | 51 | 40 | 11 | 1.8431 | 1.5641 / 0.8763 / 0.0557 |
| **CONTROL werewolf (locked)** | GeneralSkeleton | 52 | 40 | 12 | 1.8212 | **1.6940 / 0.8763 / 0.0811** |

**39 profile bones and not 40, because the golem has no `jaw`.** Named so it is never
re-discovered as a surprise; nothing in the clip set drives it.

### 2.4 ⚑ The rest columns are identical, and that is a finding rather than a bug

Run 1 of the animation probe returned **byte-identical posed head heights** for the golem and the
werewolf (+1.6844 on both). That is either a shared skeleton or an instrument reading a rig it
does not think it is reading, and the difference matters, so the probe was extended to report the
**REST pose alone — no animation anywhere near it**. The rest columns above answer it: **the
ElementalGolem, the FortGolem and the Matt-locked werewolf share one rest skeleton to four
decimals; SpiritDemon and DarkLord share a second.** Two rig families in this tree, and **the cast
boss is in the player's own family**. This is the single strongest G-2 result available and it
came from distrusting a coincidence.

### 2.5 Rest-Δ — the TCP-43 / PC-W1-A instrument, verbatim

Per-bone global-rest basis quaternion angle over shared bone names, split profile / leftover.

| ElementalGolem vs | class | n | mean Δ | max Δ |
|---|---|---:|---:|---:|
| **WEREWOLF (Matt-locked)** | **profile** | **39** | **0.0000°** | **0.0000°** |
| WEREWOLF | leftover | 12 | 53.7047° | 90.0000° |
| **`A_MOD_BL_Walk_F_Masc` (clip character, 121 bones)** | **profile** | **39** | **0.0000°** | **0.0000°** |
| clip character | leftover | 9 | 68.9050° | 177.5116° |
| **DarkLord (scene-proven)** | **profile** | **39** | **0.0000°** | **0.0000°** |
| DarkLord | leftover | 11 | 6.5822° | 36.2024° |

**The werewolf standard, reproduced exactly.** The leftover figures are carried entirely by the
`ik_*` UE authoring helpers (90° by construction, no skin weights) and `eyes`/`eyebrows` — the
same family, at the same magnitudes, that the werewolf's own PC-W1-A certificate reports. Both
fallbacks return the identical profile figures.

### 2.6 Animation — locomotion + one attack, on the posed skeleton

24 phases per clip; `Hips`/`Head`/`LeftFoot` read from `get_bone_global_pose`.

| clip | track bind | head_y min | as × rig h | min(head−hips) | min spread | non-finite | verdict |
|---|---|---:|---:|---:|---:|---:|---|
| walk (`A_MOD_BL_Walk_F_Masc`) | 45/122 | **+1.6844** | 0.924× | **+0.8081** | 1.6033 | 0 | **UPRIGHT + ALIVE** |
| idle (`A_MOD_BL_Idle_Standing_Masc`) | 49/124 | +1.6874 | 0.925× | +0.8111 | 1.6063 | 0 | **UPRIGHT + ALIVE** |
| swipe (`A_MOD_GBL_Idle_Fidget_Swipe_Neut`) | 51/95 | +1.4472 | 0.793× | +0.5709 | 1.2095 | 0 | **UPRIGHT + ALIVE** |

**Nothing inverts. Nothing collapses. Nothing goes non-finite.** The 52 unbound track subnames
are exactly the proc/IK helper family (`hipAttachFront`, `ik_shoulder_l`, `ik_knee_r`, …) that
TCP-43 §8.1 identified as the 121-minus-88 difference between Synty's animation rigs and its
character rigs. Not a defect; the count is reported so it stays a known number.

**The "attack" is named as what it is:** this tree vendors **no combat pack**. The only
attack-shaped clip on disk is a goblin-locomotion *idle-fidget swipe*. It moves the boss
genuinely (the head drops 1.6940 → 1.4472 m, a real crouch-and-swing) and it is enough to answer
"animates without inversion". **It is not a boss slam, and TELL-DRESS owns the real wind-up.**

### 2.7 **G-2 VERDICT: PASS** on the conductor's lean, without the L6 law and without a fallback.

---

## §3 — ⚑ INSTRUMENT FAILURE #1 (mine): a PASS scored on a rig that was barely animating

G-2 run 1 reported:

```
G2_C LEAN_ElementalGolem  swipe  bind=10/93  head_y_min=+1.6940 (0.929× rig h) ... ⇒ UPRIGHT+ALIVE
```

**10 of 93 tracks bound.** The verdict was green because almost nothing was moving — the swipe
clip's `.import` carried **no bone map** while the base-locomotion walk/idle clips carried one, so
its track paths were raw Synty names against a `GeneralSkeleton` target and matched only by
accident. **A green verdict on 10 bound tracks is a null measurement wearing a PASS**, and it is
precisely TCP-43's lesson arriving again in a new costume.

Fixed by retargeting the clip with the same block and re-running: **51/95**, and the pose changes
(head 1.6940 → 1.4472 m). The failing row is kept above the fixed one in the log, and the applier
carries the clip in its list with the reason written into the source.

---

## §4 — SCALE: the answer is about the pack, not the cast

**Matt asked for "one of the larger skeletons/rigs". Measured, at import scale, mesh AABB Y:**

| candidate | native height | × the 1.8212 m werewolf |
|---|---:|---:|
| RedDemon | 2.0527 m | 1.127× |
| AncientQueen | 1.9839 m | 1.089× |
| SpiritDemon | 1.9414 m | 1.066× |
| EvilGod | 1.8982 m | 1.042× |
| FortGolem | 1.8827 m | 1.034× |
| BarbarianGiant | 1.8344 m | 1.007× |
| **ElementalGolem (lean)** | **1.8239 m** | **1.0015×** |
| Troll | 1.8175 m | 0.998× |
| MechanicalGolem | 1.7909 m | 0.983× |

**There is no boss-large rig in this pack.** Synty authors the whole roster on the ~1.8 m
mannequin (which §2.4 shows is *literally the same skeleton*); the "giants" are giants by
silhouette, not by stature. **The request cannot be met by casting — only by a declared scale.**

**SHIPPED (veto-open): boss target height 2.75 m, uniform scale ×1.5077.** Three measured
constraints, no taste:

1. **≥ 1.5× the player** (conductor's lean): 2.75 / 1.80 = **1.528×** ✓
2. **< `WALL_H` = 3.005743 m**, the room's own masonry course — so the boss fits the room and its
   3-bay doorway: **0.915×** the course ✓
3. **⚑ > `SKY_BEAM_BASE_Y` = 2.40 m — THIS ONE BREAKS, and it is at Matt's eye.** The Scope-17
   gap law lifted the beam base to 2.40 m explicitly to clear *a 1.8 m person*. **A boss-scale
   body does not clear it: the top 0.35 m of the boss enters the beam-base plane.** The fork is
   one word: cap the boss at ≤ 2.40 m and lose the ≥1.5× lean, or accept a boss whose head
   passes through the shafts. Judge it in the orbit.

**Measured on screen at CAM-LOCK (1280×720):** player **39.5 px** / 1.80 m · boss **61.7 px** /
2.75 m → **1.5633× in pixels** against 1.5278× in metres. The pixel ratio is the larger of the two
because the boss stands 3 m nearer the camera along the camera-right axis; both numbers are
reported so the discrepancy is a stated property of the staging rather than a rounding mystery.

---

## §5 — COLD-EMISSIVE TINT PASS

### 5.1 The constants, and why the hue is read rather than typed

| constant | value | source |
|---|---|---|
| emissive mask | `FantasyRivals_Texture_Elemental_Emissive.png` | pack; 2048², **pure white over 0.07 % of the atlas**, peak mask luma 1.000 |
| tint | **`Color(0.620, 0.740, 1.000)`** | **`kit_replica_level.gd::SKY_COLOR`, READ AT RUNTIME** |
| energy | **0.50** | ladder, §5.2 |
| emission operator | `ADD`, UV1 | — |
| coverage on the cast body | **4,394 of 8,948 vertices (49.11 %)** | measured by `RivalBossRig.emissive_uv_coverage()` |

The hue is **not re-typed into the boss rig**. `shoot_rivalcast_orbit.gd` assigns
`_boss.emission_color = KRLS.SKY_COLOR`, so the boss, the cold floor pools and the cone beams are
one temperature *by construction* and cannot drift apart in a later tune. The pack's **other**
emissive (`FantasyRivals_Texture_01_Emissive.png`) is **warm** — mean non-black RGB (183, 110, 89)
— and is deliberately unused: warm is the player's carried light in this grammar, and a warm boss
would collapse the readability axis the cast exists to create.

The coverage number is measured rather than trusted, because a 0.07 %-white mask can be assigned
to a mesh that never samples any of it while the material looks perfectly correct. It samples
**half the body** — the golem's crystal — which is the pack's own design intent and is exactly
why this rig was the right lean.

### 5.2 The energy ladder — measured on a fixed 1,576 px core mask

Acceptance named **before** the ladder ran, from the cell brief ("must read in the dark room at
the CAM-LOCK camera without blowing out"): **READS** (clearly above the unlit body), **NOT BLOWN**
(saturated pixels ≤ 5 %), **TINT KEPT** (mean B > mean R — a white boss has lost the entire point).

| energy | mean luma | p95 luma | saturated % | mean R | mean B | **B − R** | verdict |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.00 | 61.9 | 143.0 | 0.00 | 93.8 | 32.3 | **−61.5** | no glow (control) |
| 0.20 | 121.5 | 183.2 | 0.00 | 129.1 | 137.8 | +8.7 | reads; **tint thin** |
| **0.50** | **164.4** | **222.2** | **0.00** | **160.6** | **193.8** | **+33.2** | **SHIPPED** |
| 1.00 | 202.6 | 251.4 | **5.96** | 192.3 | 233.7 | +41.4 | **FAIL — blown** |
| 4.00 | 254.9 | 255.0 | **98.29** | 254.5 | 255.0 | +0.5 | **FAIL — white, tint destroyed** |

**Room floor immediately beside the boss: B − R = −69.4.** So the shipped boss sits **102.6 points
of blue-minus-red away from its own room**, with **zero saturated pixels**. The temperature
grammar is not a claim about intent; it is a measured 102.6-point separation.

The failing rungs are kept in the table. E = 1.00 buys +8.2 more separation and costs the
"without blowing out" clause by 0.96 points — a one-constant move if Matt's eye wants it hotter.

---

## §6 — ⚑ INSTRUMENT FAILURE #2 (mine): a selector that measured its own bounding box

The first tint instrument defined "boss pixels" as *pixels inside the boss's screen bbox brighter
than a far-corner floor sample*. It selected **18,568 of the bbox's 19,220 pixels — 96.6 %** — i.e.
the torch-lit floor around the boss, and duly reported the boss **red-dominant at every energy,
including 4.00, which renders him pure white**. A selector that returns 96.6 % of its own box is
measuring the box.

Replaced with the peel this lineage uses everywhere else: **render the identical frame with the
emissive at energy 0 and diff.** The difference IS the emissive, on exactly the pixels it touches.
A second refinement was needed after that — the "touched" set *grows* with energy (bloom spill),
which made the mean B−R non-monotonic — so the final instrument fixes one **core mask** (pixels
where E = 1.00 adds ≥ 60 luma; 1,576 px) and evaluates every rung on that same set. The
non-monotonic intermediate is recorded because it is what forced the fix.

---

## §7 — Deliverable

**`~/Games/reincarnated-godot/tmp/rivalcast/clips/RIVALCAST_orbit_watch.mp4`** — 14.0 s, 1280×720,
420 frames at 30 fps, 8.1 MB.

- One full revolution around the pair, **ending on the CAM-LOCK framing and holding 60 frames
  there**. The orbit is built by the **same derivation** as `wr2_playback.gd::_pl_build_lock`,
  parameterised on yaw alone, so the tail is not *near* the game camera — it is asserted identical:
  **|Δpos| = 0.000000000 m, max |Δbasis column| = 1.03 × 10⁻⁷**, stand-off **34.8312 m**, height
  **28.3970 m**, offset (14.7262, 28.3970, 13.7826) — matching the published CAM-LOCK surface.
- **Camera identity printed on every frame** (Scope-20 ruling 1), including the live yaw and its
  signed delta from the locked bearing, plus the boss's current clip and the emissive constants.
- **The boss cycles idle → walk → swipe during the orbit**, so G-2's animation clause is judged in
  motion rather than in a log (M-EYE law: a headless number cannot answer "without inversion" —
  TCP-43 proved a broken rig passes every numeric check).
- Room: `WR1Level`, 4 rooms, boss room (room 3, dark-fantasy kit), **flag-for-flag what
  `wr2_playback.gd` hands the level on its own defaults** at `811c320` — beauty shadows/fog/
  skylight/sheen ON, walltop daylight 0.685, cones + cold pools + warm carried light.
- Plate: `tmp/rivalcast/plates/PLATE_RIVALCAST_orbit_watch_CAMLOCK.png` · ladder strip:
  `plates/LADDER_strip.png` · logs: `tmp/rivalcast/logs/{census_raw,g2,g2_r2}.log`.

---

## §8 — At Matt's eye (outside this gate)

1. **The beam-base clash (§4 constraint 3).** The 2.75 m boss's top 0.35 m enters the 2.40 m
   beam-base plane the gap law lifted for a 1.8 m person. One-word fork, veto-open.
2. **The player body reads as a dark silhouette at the game camera.** This is not a golem problem
   and not a texture problem — the werewolf atlas means **(106.4, 104.8, 102.9)**, neutral, not
   dark. The **carried lamp sits INSIDE the torso at 1.55 m**, so it lights the floor around the
   player and not the surface facing the lens; at **39.5 px tall** the result is a dark shape in a
   bright warm pool. Lighting is SHADOW-UNIFY's seam; recorded here because the cast clip is the
   first frame in which both bodies stand together, and the temperature grammar's *warm* half is
   currently reading as a hole rather than a body.
3. **The cast is veto-open by construction** — the orbit exists so the veto can be exercised on
   the record. Fallback chain is measured and one CLI word away
   (`bash scripts/run_rivalcast_orbit.sh <prefix> SK_BR_Character_FortGolem_01 420 0.50`).

---

## §9 — Guards

| guard | result |
|---|---|
| collision check at cell start (`git status`, tracked) | **clean**, HEAD `811c320` as expected |
| traces / engine tree | **never opened for write** |
| `kit_replica_level.gd` / `wr1_level.gd` / `wr2_playback.gd` / shaders | **NOT TOUCHED** — this cell adds bodies, it does not move the lighting cosmology |
| `SKY_COLOR` and every BEAM-CONE constant | **read-only**; the boss reads the level's value, the level does not read the boss's |
| declared authorised surfaces | `scripts/rival_boss_rig.gd` · `scripts/shoot_rivalcast_orbit.gd` · `scripts/run_rivalcast_orbit.sh` · `scripts/rivalcast_apply_retarget.py` · `scenes/rivalcast_orbit.tscn` — **5 files, all NEW, +808/−0** |
| staged-file guard (BEAM-CONE's lesson: the guard is a list) | 5 `A ` lines, 5 expected; no `.uid`, no `__pycache__`, no unrelated probes |
| godot commit | **LOCAL, `b80d7d9`, ahead 12, NOT pushed** |
| prior cells' clips / plates | `tmp/beamcone` + `tmp/beamfix` **untouched** |
| disk | `tmp/rivalcast` = **26 MB** total; every PNG sequence encoded then deleted in the same command; free space 15 GB, unchanged across the cell |
| smoke | level builds + renders, no `SCRIPT ERROR` / `Parse Error`, on every run |

**Open, honestly:** rig-quality was judged at the GD camera, where the boss is 62 px tall. A
close-up beauty pass on the golem's silhouette has **not** been done; if the cast survives Matt's
eye, ROOM-DRESS or the watch is where it would live.

---

## §10 — Routing

**RIVAL-CAST lands. SHADOW-UNIFY (BR-1 §3 cell #4) is next** — and it inherits two things from
here: the temperature grammar now has **both** bodies to validate on (cold emissive boss ×
warm-carried-light player), and the §8.2 finding that the *warm* half currently reads as a
silhouette is squarely in its scope.
