# Synty Humanoid-Asset Inventory — E10 Leg 3 PREP (mob vessel-race = bestiary provenance)

**Date:** 2026-07-09
**Author:** drax (presentation seam)
**Status:** READ-ONLY inventory / prep artifact. NOT a build. NOT a curation memo.
**Authority:** Feeds the race-well curation memo that parks at `canonical/matt_decision_needed/`.
**Scope:** Enumerate Synty POLYGON humanoid/character assets present in `~/Games/reincarnated-godot/`, flag rig-conformance against the Q7 GeneralSkeleton retarget contract, report variant/material space per candidate.
**Source of truth:** `~/Games/reincarnated-godot/Assets/Synty/` (gitignored on disk; enumerated live), `~/Games/reincarnated-godot/catalogue/packs.json`, `~/Games/reincarnated-godot/AGENT_STATE.md`, `~/Games/reincarnated-godot/README.md`.

> Survey-mode discipline: this document reports what EXISTS. No "should" statements. Curation (which races Matt picks) is a downstream Matt decision; this inventory only tells Matt what is AVAILABLE and RIG-CONFORMANT to pick FROM.

---

## 1. The Q7 GeneralSkeleton retarget contract (cited, not invented)

Documented in `reincarnated-godot/README.md` §"gate item #2 detail" + `scripts/retarget_test.gd` + AGENT_STATE.md (2026-06-14 through 2026-06-20 entries). The contract, restated from those files:

- **Target skeleton:** Godot `GeneralSkeleton` (88-bone, built on Godot's `SkeletonProfileHumanoid`). A conformant character imports → its `Skeleton3D` is renamed `GeneralSkeleton` and exposes all **21 humanoid-profile bones** (Root, Hips, Spine, Chest, UpperChest, Neck, Head, both Shoulder/UpperArm/LowerArm/Hand, both UpperLeg/LowerLeg/Foot). Proven headless in `retarget_test.gd`.
- **The retarget mechanism:** the jgillich Sidekick Creator post-import plugin (`addons/sidekick_creator/import_plugin.gd`, an `EditorScenePostImportPlugin`) auto-applies a **bone map** + the GeneralSkeleton **renamer** to EVERY FBX imported under the configured "sidekick root". CRITICAL FILE-LEVEL FINDING: `import_plugin.gd` line 7 gates the auto-apply on `path.begins_with(sidekick_root)`, and `sidekick_root` defaults to `res://Assets/Synty/SidekickCharacters/`. So auto-retarget only fires INSIDE that root; every OTHER pack is retargeted MANUALLY via `scripts/apply_hero_retarget.py`, which injects the same retarget block into the target FBX's `.import` file.
- **Two proven SOURCE rig families** both retarget onto GeneralSkeleton via a bone map:
  1. **UE-mannequin / Sidekick lowercase** (`pelvis`, `spine_01`, `upperarm_l`, `thigh_l`, `hand_r`, `head`, …). Mapped by `addons/sidekick_creator/sidekick_bone_map.tres`. PROVEN on the Wizard (`SK_Chr_Male_Wizard`, fantasy-characters-pack) and the King (`SK_Chr_King_Male_01`, elven-realm). These are the `SK_Chr_*` FBX under each pack's `Unreal_Characters/` subdir.
  2. **Goblin PascalCase** (`Hips`, `Spine_01`, `Clavicle_L`). Mapped by `addons/sidekick_creator/goblin_bone_map.tres`. PROVEN on the goblin-war-camp roster + Troll (combined `Characters.fbx` / `CharactersBR.fbx`).
- **The load-bearing normalizer:** `retarget/rest_fixer/fix_silhouette/enable: true` on both the character AND any driving clip. Without it the retargeted rest bakes a T-pose (splayed arms); with it the arms hang and the clip's rotations apply correctly (AGENT_STATE 2026-06-20).
- **Conformance signal from files ALONE (what CAN be judged offline):** presence of an `SK_Chr_*` / `SK_Character_*` skeletal FBX (esp. under an `Unreal_Characters/` subdir) → almost certainly one of the two proven source families → retargetable. A COMBINED static `Characters.fbx` showcase (all bodies baked into one mesh, PascalCase-rigged) → the goblin-family path. **What CANNOT be judged offline:** whether a given creature's skeleton is HUMANOID-topology (bipedal, GeneralSkeleton-shaped) vs a bespoke rig (quadruped, tail-driven, serpent-tail, extra limbs) that the humanoid bone map cannot cover. That requires an in-Godot bone-dump probe (`scripts/dump_bones.gd` / `probe_anim_bind.gd`) per candidate — flagged per-candidate below, not guessed.

**Conformance verdict scale used below:**
- **CONFORMANT (proven):** a body from this pack has been render-verified retargeted onto GeneralSkeleton in this repo.
- **CONFORMANT (file-inferred):** ships `SK_Chr_*`/`SK_Character_*` skeletal FBX in a proven source rig family; humanoid-topology expected but NOT yet probed in-repo.
- **NEEDS-VERIFICATION:** ships character bodies, but either (a) the rig family / topology can't be inferred from filenames, or (b) the creature silhouette is plausibly non-humanoid (needs a bone-dump).
- **NON-CONFORMANT (offline flag):** creature is clearly NOT humanoid-topology (won't bind the 21 humanoid bones) — flagged for confirmation, not asserted as final.

---

## 2. Candidate roster (character-bearing Synty packs present on disk)

Derived from `catalogue/packs.json` `family` tags + live FBX enumeration. Packs that ship NO character bodies (pure environment/props: dark-fortress, dungeon-realms, dwarven-dungeon, ancient-egypt, ancient-empire, viking-realm env, etc.) are EXCLUDED. `adult-face-plates` and `simple-people-2/3` ship 0 standalone character FBX (face-plate attachments / prop-only splits) and are excluded as race candidates.

### 2a. FANTASY-RACE candidates (the bestiary-relevant set)

| # | Pack | Path (Assets/Synty/…) | Race-relevant bodies | Rig source family (file-inferred) | Conformance verdict | Variant / material space |
|---|---|---|---|---|---|---|
| 1 | **Fantasy Rivals** | `polygon-fantasy-rivals-pack/` | **20 distinct creatures**: Big_Ork, Dwarf, DarkElf, Troll, RedDemon, SpiritDemon, EvilGod, Medusa (+MedusaSnakes), ForestGuardian, ForestWitch, BarbarianGiant, MechanicalGolem, ElementalGolem, FortGolem, Ancient_Warrior, AncientQueen, Mystic, Slayer, MutantGuy, Pig_Butcher | Both: `SK_Character_*` (Sidekick lowercase) + `Unreal_Characters/` duplicates; combined `Characters.fbx`+`Characters_BR.fbx` (PascalCase) also present | **MIXED — see §3.** Bipedal humanoids (Ork/Dwarf/DarkElf/Troll/Barbarian/AncientQueen/Warrior/Mystic/Slayer/MutantGuy/RedDemon/SpiritDemon/Pig_Butcher/EvilGod/ForestWitch): CONFORMANT (file-inferred). **Medusa (serpent tail), the 3 Golems (bulk/proportion), ForestGuardian: NEEDS-VERIFICATION** (non-humanoid topology risk). | `MaterialList_PolygonFantasyRivals.txt`; 21 PNG; Synty A/B/C palette-swap atlas families (`FantasyRivals_Texture_01/03_{A,B,C}`). Per-creature 1 base body; skin/color variance = the A/B/C atlas swap, not per-body variants. |
| 2 | **Mini Fantasy Characters** | `polygon-mini-fantasy-characters/` | **120 `SK_*` skeletal bodies** incl. fantasy races: GoblinShaman, GoblinWarriorMale/Female, GoblinFemale, RockGolem, SkeletonSoldier ×2, SkeletonKnight, Wizard, Witch, Druid, Sorcerer, King, + Viking/Samurai/Pirate/Western human variants | `SK_*` skeletal, Sidekick-family naming | CONFORMANT (file-inferred) for the humanoid bodies; **RockGolem, Skeleton\* NEEDS-VERIFICATION** (skeleton/golem topology probe). NOTE: "MINI" = chibi/low-poly proportion — a proportion mismatch vs the full-scale Fantasy Rivals set, not a rig issue. | `MaterialList_PolygonMiniFantasyCharacters.txt`; 18 PNG; **named color-family atlases** (Green/Purple/… `_A/_B/_C`) — richer swap space than the single-atlas packs. |
| 3 | **Fantasy Characters Pack** | `polygon-fantasy-characters-pack/` | 12 human archetypes: King, Wizard (PROVEN), Sorcerer, Druid, Witch, Gypsy, Queen, Baird(bard), Rouge(rogue), Peasant ×3 | `SK_Character_*` + `Unreal_Characters/SK_Chr_*` (Sidekick lowercase) | **CONFORMANT (proven)** — the Wizard from this pack is the original render-verified retarget (AGENT_STATE 2026-06-20). All human-topology. | `MaterialList_PolygonFantasyCharacters.txt`; 16 PNG; A/B/C atlas variants (`_01/_05_{A,B,C}`) + an Emmision map. |
| 4 | **Modular Fantasy Hero Characters** | `polygon-modular-fantasy-hero-characters/` | Modular HUMAN wardrobe: 1496 part FBX (Torso/Head/Arms/Legs/attachments, Male+Female) via `SK_Chr_*` parts + combined `ModularCharacters.fbx` | `SK_Chr_*` (Sidekick lowercase modular parts, same family the SidekickCharacters retarget proof runs on) | **CONFORMANT (proven-adjacent)** — same modular Sidekick rig family the `retarget_test.gd` proof + the King's pauldron/cape attach work exercised. Human-topology only. | `MaterialList_PolygonFantasyHeroCharacters.txt`; 17 PNG; A/B/C atlas + a `Mask_01` (recolor mask). Enormous MODULAR variant space (mix-and-match parts), not fixed bodies. |
| 5 | **Modular Fantasy Heroes** (2nd copy) | `polygon-modular-fantasy-heroes/` | 1442 part FBX — near-duplicate of #4 | same as #4 | **CONFORMANT (proven-adjacent)** — DUPLICATE PACK of #4 (likely a re-download; near-identical FBX roster). Flag for de-dup at curation. | same atlas family as #4 |
| 6 | **Boss Zombies** | `polygon-boss-zombies/` | 4 zombie bosses: Slobber, Wretch, Brute, Blobber (each `SK_Chr_ZombieBoss_*`, + `Unreal_Characters/` duplicates) | `SK_Chr_*` (Sidekick lowercase), `Unreal_Characters/` present | **CONFORMANT (file-inferred)** for humanoid zombies; Brute/Blobber bulk = **NEEDS-VERIFICATION** (proportion/extra-mass rig probe). Undead-race candidate. | `MaterialList_PolygonBossZombies.txt`; 15 PNG; `_02/_04_{A,B,C}` atlas families. |
| 7 | **Werewolf** | `polygon-werewolf/` | 2 skeletal: `SK_Chr_Werewolf_01`, `SK_Chr_Werewolf_Undead_01` (+ static `SM_Werewolf_01`, `SM_Werewolf_Tail_01`) | `SK_Chr_*` naming BUT a WEREWOLF silhouette (digitigrade legs, tail — separate `SM_Werewolf_Tail_01` mesh exists) | **NEEDS-VERIFICATION, leaning NON-CONFORMANT.** Werewolf topology is plausibly NON-humanoid (digitigrade + tail). The `SK_Chr_` prefix does NOT guarantee the 21 humanoid bones bind. REQUIRES a bone-dump before any race-list inclusion. | `MaterialList_PolygonWerewolf.txt`; 8 PNG; `_01/_02/_03_{A,B}` atlas (2-variant, smaller space). |
| 8 | **Goblin War Camp** | `polygon-goblin-war-camp/` | Combined `Characters.fbx` / `CharactersBR.fbx` (grunts, elites, WarChief, Troll_01) + `Capes.fbx` + attachments | Goblin **PascalCase** (`Hips`/`Spine_01`/`Clavicle_L`) | **CONFORMANT (proven)** — this exact roster is render-verified retargeted via `goblin_bone_map.tres`; goblins + Troll stand in a bound idle in `ravine_atgrade.tscn` (AGENT_STATE 2026-06-20). Goblin + Troll race candidates. | `MaterialList` present; green-skin goblin atlas; combined-showcase distribution (bodies baked into one FBX — extract per-body). |

### 2b. NON-FANTASY / modern-setting character packs present (out of bestiary-genre, listed for completeness)

These ship rig-conformant human bodies but are MODERN/CITY themed (contemporary clothing) — genre-mismatched for a fantasy bestiary; noted so Matt knows they exist and can exclude them explicitly.

| Pack | Path | Bodies | Conformance | Notes |
|---|---|---|---|---|
| City Characters Pack | `polygon-city-characters-pack/` | ~19 `SK_Character_*` (Biker, Paramedic, FireFighter, Grandpa…) | CONFORMANT (file-inferred) | Modern-city theme. |
| Simple People | `polygon-simple-people/` | ~21 `SK_Character_*` (Sheriff, RiotCop, BusinessMan…) | CONFORMANT (file-inferred), SIMPLE-line low-detail | Modern; SIMPLE-line polys. |
| Mini City Characters | `polygon-mini-city-characters-pack/` | combined `Characters.fbx` + `Unreal_Characters/MiniCharacter_*` | CONFORMANT (file-inferred), chibi | Modern chibi. |

---

## 3. Rig-conformance summary (the number Matt needs)

### Fantasy-race candidate PACKS: 8 (§2a)
### Distinct fantasy-race candidate BODIES (de-duplicated across packs, bestiary-genre only):

Counting distinct creature TYPES suitable as bestiary "races" (collapsing the human-archetype flavors — King/Wizard/Druid/etc. — into "Human"; collapsing pack duplicates):

**CONFORMANT (proven or file-inferred humanoid-topology) — ~13 race-type candidates:**
1. Human (Fantasy Characters / Modular Hero / Mini) — PROVEN
2. Goblin (Goblin War Camp / Mini) — PROVEN
3. Troll (Goblin War Camp / Fantasy Rivals) — PROVEN (goblin PascalCase rig)
4. Ork (Fantasy Rivals) — file-inferred
5. Dwarf (Fantasy Rivals) — file-inferred
6. Dark Elf (Fantasy Rivals) — file-inferred
7. Barbarian Giant (Fantasy Rivals) — file-inferred (humanoid, just scaled)
8. Red Demon / Spirit Demon (Fantasy Rivals) — file-inferred (bipedal demon)
9. Zombie / Undead (Boss Zombies) — file-inferred
10. Skeleton (Mini Fantasy — SkeletonSoldier/Knight) — file-inferred (skeletal-humanoid)
11. Ancient Warrior / Queen (Fantasy Rivals) — file-inferred
12. Mystic / Slayer / MutantGuy (Fantasy Rivals) — file-inferred humanoid
13. Forest Witch / Gypsy / other human-topology casters — file-inferred

**NEEDS-VERIFICATION (topology probe required before inclusion) — ~7 candidates:**
- Medusa (serpent lower body — `SK_MedusaSnakes_01` is a separate mesh; near-certain non-humanoid tail)
- Mechanical Golem / Elemental Golem / Fort Golem (Fantasy Rivals) — bulk/proportion, possibly bespoke rig
- Rock Golem (Mini Fantasy)
- Forest Guardian (Fantasy Rivals) — tree/plant-form, likely non-humanoid
- Werewolf (digitigrade + tail — leans NON-CONFORMANT)
- Zombie Brute / Blobber (Boss Zombies) — extra-mass proportion
- Pig Butcher / Evil God (Fantasy Rivals) — verify bipedal-humanoid topology

**NON-CONFORMANT (offline flag, confirm before excluding):**
- None asserted as hard-non-conformant from files alone. Werewolf + Medusa are the strongest non-humanoid-topology candidates but require a bone-dump to confirm (flagged, not guessed).

### The clean count for the curation memo:
- **Character-bearing packs present:** 11 (8 fantasy-genre + 3 modern-genre).
- **Fantasy-race candidate packs:** 8.
- **Distinct fantasy-race-TYPE candidates:** ~20 (13 rig-conformant / ~7 needs-verification).
- **Matt's cardinality budget v1 lean:** 4–6 races. The conformant-13 set comfortably exceeds the budget → curation is a SELECTION problem, not a supply problem. The needs-verification set (golems, medusa, werewolf, forest guardian) is where the Synty-rig-conformance gate does real filtering work.

---

## 4. Material / variant space (per the retarget contract's "material/skin options")

Every Synty POLYGON character pack uses the same skin/color model: a small set of shared **texture atlases** (`Pack_Texture_NN_{A,B,C}.png`), where A/B/C are palette-swap color variants of the SAME UV layout. A single body FBX can be recolored by binding a different atlas variant — this is the "material/skin option" axis. It is NOT per-body geometry variants (those come from distinct FBX). Two shapes of variant space present in the roster:

- **Single-atlas packs** (Fantasy Characters, Fantasy Rivals, Modular Hero, Werewolf, Boss Zombies): 2–3 color variants (A/B/C) per texture family.
- **Named-color-family pack** (Mini Fantasy Characters): explicit Green/Purple/… atlas families → the widest recolor space, well-suited to per-race color coding.
- **Modular packs** (#4/#5): the variant space is combinatorial (mix-and-match part FBX), not a fixed atlas swap — orders of magnitude more visual variants, human-topology only.

Material gotcha carried from AGENT_STATE (2026-06-19/20, load-bearing for any build phase, NOT a curation input): Synty FBX ship broken embedded material refs; the working repo binds atlases via `Image.load()` on the `.png`, NOT the FBX's embedded material. Any Leg-3 BUILD that renders these bodies must bind atlases explicitly (this is a BUILD note, parked here so it's not lost — it does not affect curation).

---

## 5. Files / provenance cited

- `~/Games/reincarnated-godot/catalogue/packs.json` — pack config (48 pack entries; `family` tags; fbx_roots).
- `~/Games/reincarnated-godot/addons/sidekick_creator/import_plugin.gd` — auto-retarget scope gate (sidekick-root-only).
- `~/Games/reincarnated-godot/addons/sidekick_creator/plugin.gd` — `sidekick_root` default = `res://Assets/Synty/SidekickCharacters/`; `skeleton_name` = `GeneralSkeleton`; `bone_map` = `sidekick_bone_map.tres`.
- `~/Games/reincarnated-godot/addons/sidekick_creator/sidekick_bone_map.tres` — UE-mannequin→GeneralSkeleton map.
- `~/Games/reincarnated-godot/addons/sidekick_creator/goblin_bone_map.tres` — goblin PascalCase→GeneralSkeleton map.
- `~/Games/reincarnated-godot/scripts/retarget_test.gd` — the auto-retarget PROOF harness (21 humanoid bones resolved).
- `~/Games/reincarnated-godot/scripts/apply_hero_retarget.py` — manual retarget-block injector for non-sidekick-root FBX.
- `~/Games/reincarnated-godot/scripts/dump_bones.gd`, `scripts/probe_anim_bind.gd` — the per-candidate bone-dump probes needed to clear NEEDS-VERIFICATION items.
- `~/Games/reincarnated-godot/README.md` §"gate item #2 detail" — the retarget contract narrative.
- `~/Games/reincarnated-godot/AGENT_STATE.md` — Wizard/King/goblin retarget verifications (2026-06-14 → 2026-06-20).

## 6. What this inventory does NOT do (scope boundary)

- Does NOT curate the race list (Matt's decision; parks at `matt_decision_needed/`).
- Does NOT run the in-Godot bone-dump probes to clear the ~7 NEEDS-VERIFICATION creatures (that is a follow-on if Matt's curation lands any of them). Those verdicts are flagged, not guessed, per the read-only file-only mandate.
- Made ZERO changes to `reincarnated-godot/` (read-only seam). No FBX imported, no `.import` written, no probe run.
