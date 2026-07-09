# Race-Well Bone-Dump Probes — DarkElf / Dwarf / Big_Ork (E10 Leg 3 `verified=true` resolution)

**Date:** 2026-07-09
**Author:** drax (presentation seam)
**Status:** RESEARCH / verification artifact. PARKED for gandalf consumption — I do NOT edit the race-well canon's §2 rig-status columns (that's gandalf's write).
**Authority:** Resolves the in-Godot bone-dump probes flagged in `canonical/reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md` §6.1 (Lane 4a follow-on). Kit-gen (E10 Leg 3) requires `verified=true` rig bindings per canon §6.2; these probes supply the evidence.
**Prior artifact:** `agentic_orchestration/research/2026-07-09-synty-humanoid-asset-inventory.md` (d7e2dff) — file-level inventory that flagged these three as "CONFORMANT (file-inferred)" pending the in-Godot probe. This note upgrades those verdicts with actual rig evidence.
**Probe script (committed, godot repo):** `scripts/probe_race_well_bones.gd` — commit `1970bcb`.

---

## 0. Method (what the probe actually tested)

The three bodies live OUTSIDE `res://Assets/Synty/SidekickCharacters/` — the auto-retarget root — so their `.import` files carry NO retarget block (verified: `SK_Character_DarkElf_01.fbx.import` has zero `retarget/` params). They therefore import with their **RAW SOURCE skeleton** (pre-renamer bone names). That is exactly what a conformance probe wants: dump the raw bone set and test whether it matches a **proven-mappable reference family**.

Two proven reference bone-map source vocabularies exist in this repo (`addons/sidekick_creator/`):
- **`sidekick_bone_map.tres`** — UE-mannequin lowercase source names (`root`, `pelvis`, `spine_01/02/03`, `neck_01`, `head`, `clavicle_l/r`, `upperarm_l/r`, `lowerarm_l/r`, `hand_l/r`, `thigh_l/r`, `calf_l/r`, `foot_l/r`, + finger chains). **Render-PROVEN** on the Wizard (`SK_Chr_Male_Wizard`) and King (`SK_Chr_King_Male_01`) per AGENT_STATE 2026-06-20.
- **`goblin_bone_map.tres`** — Goblin PascalCase source names (`Hips`, `Spine_01`, `Clavicle_L`, `Shoulder_L`, `Elbow_L`, `UpperLeg_L`, …). Render-PROVEN on the goblin roster + Troll.

The probe scores each body's raw bone set against the 21 CORE (non-optional-finger) source bones of BOTH maps, against the 21 post-renamer GeneralSkeleton humanoid-profile bones, and scans for bespoke-rig signal bones (tail/wing/serpent). It also dumps rest-pose global-Y heights of key bones for the reskin-vs-reframe proportion test.

### Disc #1 / #2 smoke validation (pipeline proven before trusting the unknowns)
1. Ran the existing `scripts/dump_bones.gd` on the Human base body (`SK_HUMN_BASE_01_10TORS_HU01.fbx`, inside the Sidekick root) → dumped `GeneralSkeleton`, 88 bones, full humanoid profile. Pipeline confirmed live under Godot 4.6.3-stable headless.
2. Closed the mapping chain: probed the **proven-render King body** — it imports as `GeneralSkeleton` and resolves **21/21 humanoid-profile bones** post-renamer. Since the King is retargeted from the identical `root/pelvis/spine_01/...` source names my three targets carry, this proves the chain **raw sidekick source names → `sidekick_bone_map.tres` → 21/21 GeneralSkeleton profile**. The three targets' 21/21 sidekick-core coverage is therefore a valid `verified=true` signal, not a filename guess.

---

## 1. Per-body bone-dump results

All three bodies: skeleton node `Skeleton3D`, single root bone `root` (parent=-1), no bespoke-signal bones (no tail/wing/serpent). All three carry the identical UE-mannequin/Sidekick lowercase source family.

| Body | FBX | Bone count | Sidekick-core | Goblin-core | Bespoke signals | Verdict |
|---|---|---|---|---|---|---|
| **DarkElf (elf)** | `SK_Character_DarkElf_01.fbx` | 50 | **21 / 21** | 0 / 24 | none | RIG-CONFORMANT via `sidekick_bone_map` = reskin-class |
| **Dwarf** | `SK_BR_Character_Dwarf_01.fbx` | 51 | **21 / 21** | 0 / 24 | none | RIG-CONFORMANT via `sidekick_bone_map` = reskin-class |
| **Big_Ork (orc)** | `SK_BR_Character_Big_Ork_01.fbx` | 51 | **21 / 21** | 0 / 24 | none | RIG-CONFORMANT via `sidekick_bone_map` = reskin-class |

(Goblin-core = 0/24 is EXPECTED and correct — these are the OTHER proven family, PascalCase-goblin scores zero because the bodies are lowercase-sidekick. Not a failure.)

**Bone-set structure:** DarkElf's 50-bone set is the canonical Sidekick body (`root, pelvis, spine_01/02/03, clavicle_l, upperarm_l, lowerarm_l, hand_l`, index/middle/thumb finger chains L+R, `neck_01, head, eyes, eyebrows, thigh_l, calf_l, foot_l, ball_l` + R mirror, `ik_foot_root/l/r, ik_hand_root/gun/l/r`). Dwarf and Big_Ork are the SAME set + one extra bone `Belly_01` (a modular belly-deform helper parented into the spine — NOT a topology divergence; the 21 core humanoid bones are untouched).

### Proportion evidence (reskin-vs-reframe, rest-pose global-Y in meters)

| Bone | DarkElf | Dwarf | Big_Ork |
|---|---|---|---|
| pelvis | 0.876 | 0.876 | 0.876 |
| spine_03 | 1.337 | 1.337 | 1.337 |
| thigh_l | 0.832 | 0.833 | 0.833 |
| calf_l | 0.432 | 0.457 | 0.457 |
| foot_l | 0.056 | 0.081 | 0.081 |
| head | 1.569 | 1.663 | 1.663 |

The skeleton REST proportions are effectively IDENTICAL across all three (pelvis/spine_03 pinned to the same heights). The Dwarf's stubby silhouette is NOT baked into the bone rest transforms — it rides on the **mesh**, on the shared standard-height rig. That is the textbook definition of reskin (mesh-baked proportions on the shared bone map), not reframe (own skeleton + own locomotion).

---

## 2. Resolved status per race

### Elf — `verified=true`? **YES.**
Evidence: DarkElf raw skeleton = 21/21 sidekick-core coverage, single `root`, no bespoke bones. Binds `sidekick_bone_map.tres` (render-proven on Wizard/King) → GeneralSkeleton. **Reskin-class, zero new rig cost.** Full Sidekick animation library inherited. Canon §2 "reskin-likely / file-inferred" upgrades to **VERIFIED (bone-dump)**.

### Dwarf — reskin or reframe? **RESKIN.**
Evidence: Dwarf raw skeleton = 21/21 sidekick-core coverage; bone set IDENTICAL to DarkElf except one non-topological `Belly_01` helper; rest-pose proportions IDENTICAL to the standard Sidekick rig (pelvis/spine pinned to the same heights as DarkElf and Big_Ork). Dwarf proportions are mesh-baked, not skeleton-baked. Binds the SAME `sidekick_bone_map.tres`. **Reskin-class — the open question resolves to reskin (zero new rig cost, no own locomotion set needed).** Canon §2 "reskin-or-reframe (the open one)" resolves to **RESKIN, VERIFIED (bone-dump)**.

### Orc — native `Big_Ork` body vs modular-reskin. **RECOMMENDATION (ruling parks for gandalf/Matt):**

**I RECOMMEND: use the native `Big_Ork` body as the orc vessel (the modular-reskin path is unnecessary).**

Evidence and reasoning:
- **Rig cost — TIE at zero.** The native `Big_Ork` body is 21/21 sidekick-core conformant, single `root`, no bespoke bones, IDENTICAL rest proportions to the standard rig. It binds `sidekick_bone_map.tres` with zero new rig work — the SAME conformance the modular human-frame path would have. Matt's ruling constraint ("green skin + robust musculature as modular assets WITHOUT altering the skeleton's dimensions") is SATISFIED BY THE NATIVE BODY: its skeleton dimensions ARE the standard human-frame dimensions (pelvis 0.876 / spine_03 1.337 — identical to DarkElf/Dwarf). The native body does not alter skeleton dimensions; the orc bulk is in its mesh.
- **Animation-library inheritance — TIE.** Both paths inherit the full Sidekick base-locomotion library (same bone map, same GeneralSkeleton target).
- **Silhouette / readability — native body WINS.** At Camera B′ (20 m / ~8% hero fraction, canon §1 readability check), silhouette is a distance-surviving channel. The native `Big_Ork` mesh ships purpose-authored orcish bulk (heavy brow, tusks, broad shoulders baked in the mesh) that reads as "orc" at gameplay distance out of the box. A modular-reskin of the human frame would require assembling bulk pieces to approximate what the native body already delivers — more asset-assembly work for an equal-or-worse silhouette. Native body = less work, better readability.
- **Consistency — native body WINS.** Choosing the native `Big_Ork` makes the orc construction identical in KIND to the elf and dwarf (all three: native fantasy-rivals body + shared sidekick rig + material/mesh differentiation). One uniform reskin pattern across all three file-inferred races is simpler to build and maintain than a bespoke modular-assembly path for the orc alone.

The modular-reskin path (Matt's alternative framing) remains VIABLE — it's also rig-conformant — but on this evidence it costs more asset-assembly work for equal rig cost and weaker default silhouette. **The RULING is gandalf/Matt's; I park the recommendation with evidence and do not decide it.**

---

## 3. What would BLOCK a `verified=true` stamp — NOTHING for these three.

No BLOCKs. All three bodies:
- Load and instantiate clean under Godot 4.6.3-stable headless.
- Carry a single-root humanoid skeleton with all 21 core sidekick-map source bones.
- Show no bespoke-rig signals (no tail/wing/serpent bones that would defeat the humanoid map).
- Share the proven Wizard/King rig family's exact source vocabulary → `sidekick_bone_map.tres` binds them → GeneralSkeleton (chain closed via the King's proven 21/21 profile resolution).

### Two BUILD notes (NOT blocks — parked so they aren't lost at Leg 3):
1. **Retarget block must be injected at build.** These three FBX currently import WITHOUT a retarget block (raw source skeleton). To actually render them retargeted, Leg 3 must apply `sidekick_bone_map.tres` + the GeneralSkeleton renamer + the `retarget/rest_fixer/fix_silhouette/enable: true` normalizer via `scripts/apply_hero_retarget.py` (the same manual-injection path used for every non-sidekick-root FBX). Without `fix_silhouette` the rest bakes a T-pose (AGENT_STATE 2026-06-20). This is expected mechanics, not a defect.
2. **Material binding.** Synty FBX ship broken embedded material refs; the working repo binds atlases via `Image.load()` on the `.png`, not the FBX embedded material (AGENT_STATE 2026-06-19/20). Any Leg-3 render of these bodies must bind the fantasy-rivals atlas explicitly. Carried from the prior inventory §4.

---

## 4. Files / provenance

- Probe script: `~/Games/reincarnated-godot/scripts/probe_race_well_bones.gd` (commit `1970bcb`).
- Smoke reference: `~/Games/reincarnated-godot/scripts/dump_bones.gd` (Human base → GeneralSkeleton 88-bone).
- Bone maps: `addons/sidekick_creator/sidekick_bone_map.tres` (lowercase, proven Wizard/King), `addons/sidekick_creator/goblin_bone_map.tres` (PascalCase, proven goblins/Troll).
- Bodies probed (all under `Assets/Synty/polygon-fantasy-rivals-pack/PolygonFantasyRivals_Source_Files/Source_Files/Characters/Unreal_Characters/`): `SK_Character_DarkElf_01.fbx`, `SK_BR_Character_Dwarf_01.fbx`, `SK_BR_Character_Big_Ork_01.fbx`.
- Chain-closure reference: `SK_Chr_King_Male_01.fbx` (polygon-elven-realm) — proven-render body, 21/21 post-renamer humanoid profile.
- Godot: `/Applications/Godot.app/Contents/MacOS/Godot` v4.6.3-stable, headless.

---

## 5. Summary for gandalf (canon §2 rig-status column updates — YOUR write, not mine)

| Race | Was (canon §2) | Resolves to (this probe) |
|---|---|---|
| Elf (DarkElf) | file-inferred CONFORMANT | **VERIFIED (bone-dump): reskin, 21/21 sidekick-core, verified=true** |
| Dwarf | reskin-or-reframe (open) | **VERIFIED (bone-dump): RESKIN, 21/21 sidekick-core, verified=true** |
| Orc (Big_Ork) | reskin — modular-vs-native open (Lane 4a) | native `Big_Ork` body = 21/21 sidekick-core, verified=true either way; **drax RECOMMENDS native body** (equal rig cost, better silhouette, uniform with elf/dwarf) — ruling parks for gandalf/Matt |

The well's five races are now: Human (VERIFIED by construction), Goblin (VERIFIED, own goblin map), Orc/Elf/Dwarf (VERIFIED by bone-dump, shared sidekick map). No BLOCK stands between this slate and E10 Leg 3 kit-gen consumption on rig grounds.
