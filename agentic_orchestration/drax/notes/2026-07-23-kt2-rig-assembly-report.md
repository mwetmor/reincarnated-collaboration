# KT-2 Rig-Assembly Report — KING-TWIN run

**Author:** drax (presentation seam), 2026-07-23. **Gate:** KT-2 (assemble the 23 fighter
RIG SCENES that KT-4 will swap in for the capsule proxies inside `replica_playback.tscn`).
**Scope:** `/Users/admin/Games/reincarnated-godot` (rig scenes + scripts) + this report.
**Substrate:** KT-1 mapping brief (Tables A+B, four forks — all Matt-ruled) + census §7 king
recipe. All work is DISPLAY-SHELL only (zero-derivation): body + prop + aura + locomotion,
nothing computed. No King mesh / crown / elven greatsword used anywhere (KING SINGULARITY held).

---

## Headline

- **23 rig scenes assembled** (5 pilots + 18 mobs), each a self-contained `.tscn`
  instantiable by the playback scene at KT-4.
- **Headless load: 23/23 PASS.** Every rig loads clean via `godot --headless`, node-tree
  sane: body mesh under a GeneralSkeleton on all 23; hand-prop socket populated on all 7
  ruled-armed rows (5 pilots + 2 caster mobs); aura node present on all 5 pilots; NO aura
  on any mob (Fork 2 held).
- **Alternate-mesh fallbacks: NONE.** All 22 unique primary meshes retargeted to
  GeneralSkeleton and built on the first real attempt. No named-alternate was needed.
- **One substrate deviation (aura scene), logged below** — forced by an on-disk asset gap,
  not a mapping change. Not improvised around; flagged for the conductor.

---

## The retarget substrate work (the load-bearing enabler)

The king imports through the `sidekick_creator` plugin's `sidekick_bone_map.tres` →
GeneralSkeleton humanoid retarget (`fix_silhouette` ON), so `king_rig.gd` can address bones
by profile name (`RightHand`, `Head`, `UpperChest`). **Recon finding:** of every mesh in
Tables A+B, only `SK_Chr_Male_Wizard` (used by the pre-existing `hero_walker.gd`) was already
retargeted. Every other candidate imported with native Unreal bone names as a plain
`Skeleton3D` (empty `_subresources={}` in its `.fbx.import`).

**Fix (king-parallel, per the brief's "GeneralSkeleton retarget via the existing import
plugin"):** injected the identical retarget subresource block (same bone map, `fix_silhouette`
ON) into each of the 22 unique meshes' `.fbx.import`, cleared each cached
`.godot/imported/*.scn`+`.md5`, and reran `--headless --import`. Verified all 22 reimported as
`GeneralSkeleton` with `RightHand`/`Head`/`UpperChest` present (`kt2_verify_retarget.gd`,
`RT_SUMMARY ok=22 bad=0`). Discipline note: `--import` alone will NOT reprocess a changed
`.import` — the cached artifact must be deleted first, then reimported. (Tools:
`scripts/kt2_apply_retarget.py`, `scripts/kt2_verify_retarget.gd`.)

---

## TABLE A — PILOT RIGS (5) — full king grammar

Scenes in `scenes/rigs/pilots/`. Script `scripts/pilot_rig.gd` (body + hand_r prop + aura +
idle/walk crossfade). `scale` = runtime factor to hit `target_height=1.85m` (king register);
factor logged from the build print. All PASS.

| rig id | mesh used (primary) | scale factor | prop (ruled) | aura node (ruled hex) | headless |
|---|---|---|---|---|---|
| `rig_d2_firewall_sorc` | `SK_Chr_Male_Sorcerer` (primary) | 1.0063 | `SM_Prop_WizardStaff_01` @ hand_r ✔ | present, tint `#FF6A1A` | PASS |
| `rig_d2_fire_sorc` | `SK_Chr_Female_Witch` (primary) | 0.9387 | `SM_Prop_Wand_01` @ hand_r ✔ | present, tint `#FFD23A` | PASS |
| `rig_gd_flames_of_ignaffar_purifier` | `SK_Chr_Hunter_Male_01` (primary) | 1.0329 | `SM_Wep_Crossbow_01_Rigged` @ hand_r ✔ | present, tint `#FF7A24` | PASS |
| `rig_poe2_bonestorm` | `SK_Chr_Witch_Female_01` (primary) | 1.0327 | `SM_Prop_Druid_Staff_01` @ hand_r ✔ | present, tint `#D9D2E8` | PASS |
| `rig_poe1_cyclone` | `SK_Chr_DarkLord_Male_01` (primary) | 1.0037 | `SF_Wep_GreatAxe_01` @ hand_r ✔ | present, tint `#9AA0A6` | PASS |

All five props are the EXACT ruled mesh at `hand_r` (GeneralSkeleton `RightHand` socket, prop
pose in the hand-bone local frame — king pattern). All five auras instantiate the Binbun scene
through the king recipe: parented under the rig at the feet, OmniLight softened to energy 0.55
+ color-keyed to the ruled hex, lifted 0.08m, glow-mesh surfaces tinted to the hex; the
`aura_clip` interior-scissor shader is wired-available for KT-4's room clip (applied by the
playback host per the king `apply_interior_clip` pattern — not clipped at KT-2 since the rig is
standalone with no room bounds yet). Locomotion: retargeted `A_MOD_BL_Idle_Standing_Masc` /
`A_MOD_BL_Walk_F_Masc`, 0.18s crossfade.

---

## TABLE B — MOB RIGS (18) — body + optional prop, NO aura (Fork 2)

Scenes in `scenes/rigs/mobs/`. Script `scripts/mob_rig.gd`. `scale` = runtime factor to hit
the per-row `target_height` (my reasoning-boundary call, logged). Only the two ruled-armed
caster rows carry a hand prop; all others ruled unarmed. NO aura on any mob. All PASS.

| rig id | mesh used (primary) | target_h (m) | scale factor | prop (ruled) | headless |
|---|---|---|---|---|---|
| `rig_mob_d2_fallen` | `SK_Chr_Goblin_Male` | 1.40 | 0.7817 | none (unarmed) | PASS |
| `rig_mob_d2_zombie` | `SK_Chr_ZombieBoss_Wretch_01` | 1.48 | 1.2719 | none (unarmed) | PASS |
| `rig_mob_d2_skeleton` | `SK_Chr_Skeleton_01` | 1.70 | 0.9469 | none (unarmed) | PASS |
| `rig_mob_d2_corrupt_rogue` | `SK_Chr_Hunter_Female_01` | 1.70 | 0.9489 | none (unarmed) | PASS |
| `rig_mob_poe1_cannibal` | `SK_Chr_Goblin_Warrior_Male` | 1.55 | 0.8433 | none (unarmed) | PASS |
| `rig_mob_poe1_goatman` | `SK_Chr_Demon_Male_01` | 1.85 | 0.8623 | none (unarmed) | PASS |
| `rig_mob_poe1_corrupted_rhoa` | `SK_Chr_Werewolf_01` | 1.90 | 1.0433 | none (unarmed) | PASS |
| `rig_mob_poe1_rhoa_skeleton` | `SK_Chr_Skeleton_LightArmor_01` | 1.70 | 0.9469 | none (unarmed) | PASS |
| `rig_mob_poe1_caster_goatman` | `SK_Chr_Goblin_Shaman` | 1.50 | 0.7977 | `SM_Prop_Wand_01` @ hand_r ✔ | PASS |
| `rig_mob_poe2_skeleton` | `SK_Chr_Skeleton_HeavyArmor_01` | 1.75 | 0.9747 | none (unarmed) | PASS |
| `rig_mob_poe2_zombie` | `SK_Chr_ZombieBoss_Brute_01` | 1.55 | 0.8401 | none (unarmed) | PASS |
| `rig_mob_poe2_bone_deacon` | `SK_Chr_Skeleton_Flesh_01` | 1.72 | 0.9539 | `SM_Prop_Wand_01` @ hand_r ✔ | PASS |
| `rig_mob_poe2_cannibal` | `SK_Chr_Goblin_Female` | 1.45 | 0.7792 | none (unarmed) | PASS |
| `rig_mob_gd_rotting_corpse` | `SK_Chr_ZombieBoss_Slobber_01` | 1.50 | 0.8191 | none (unarmed) | PASS |
| `rig_mob_gd_ghoul` | `SK_Chr_Demon_01` | 1.65 | 0.8643 | none (unarmed) | PASS |
| `rig_mob_gd_chthonic_hound` | `SK_Chr_Werewolf_Undead_01` | 1.55 | 0.8511 | none (unarmed) | PASS |
| `rig_mob_gd_crazed_villager` | `SK_Chr_Gravedigger_Male_01` | 1.75 | 0.9740 | none (unarmed) | PASS |
| `rig_mob_gd_crazed_thornback` | `SK_Chr_Werewolf_01` | 1.35 | 0.7413 | none (unarmed) | PASS |

Quill-rat OMITTED (Fork 1 — D2 set = 4 mobs). Rhoa→werewolf and Thornback→werewolf are the
two brief-flagged beast proxies (Fork 4), carried faithfully as ruled.

---

## Reasoning-boundary calls (all logged, none silent)

1. **Scale = target-height, not raw multiplier.** The king scales to a target metric height
   by AABB.y; I reused that. My per-row `target_height` encodes the brief's size intent
   (goblins short ~1.40–1.55m; skeletons/humans ~1.70–1.75m; demon-goatman tall 1.85m; the
   fast-charger Rhoa 1.90m; hound/thornback low 1.35–1.55m). The runtime `scale factor`
   (logged above) is derived per mesh from its raw height.
2. **ZombieBoss "downscale ~0.8" interpretation.** The brief says downscale the boss skins for
   trash mobs. Because the ZombieBoss meshes vary in raw height (Wretch is short, ~1.16m), a
   flat 0.8× would land them at inconsistent heights. I instead targeted trash-mob heights
   directly (~1.48–1.55m ≈ 0.8×1.85m boss-presentation), which is the downscale INTENT — a
   uniformly trash-sized zombie. Consequence: the Wretch's factor is >1 (1.27) because its raw
   mesh is small; the OTHER zombie skins (Brute 0.84, Slobber 0.82) scale down as expected.
   The visual outcome (a ~1.5m trash zombie) is correct in all three cases.
3. **Werewolf rescale (Rhoa / Thornback).** Both are ruled werewolf proxies with "rescale".
   Rhoa (large fast charger) → 1.90m; Thornback ("quadruped-ish", low beast) → 1.35m. The
   werewolf mesh stands humanoid-upright; a true quadruped pose is out of scope for a
   display-shell retarget and was not attempted (flagged, not improvised).
4. **Locomotion clip gender.** Only the MASCULINE base-locomotion idle/walk clips exist on
   disk (no feminine set at the Sidekick path). All rigs — including female-bodied ones
   (Witch, Hunter_Female, Goblin_Female) — bind the masculine clips, which are retargeted to
   GeneralSkeleton and bind by humanoid bone name regardless of body gender. Acceptable for a
   display shell; noted.

## Deviation (flagged for the conductor — NOT improvised around)

**Aura Binbun scene substitution (pilots).** The brief's Table A names a distinct per-kit
Binbun aura scene (`fire_area_03`, `fire_area_06`, `beam_vfx_04`, `magic_orb_basic_vfx_01`,
`pulse_area_vfx_03`). On-disk recon 2026-07-23 found ONLY `magic_areas/.../basic_area_vfx_01.tscn`
present in `Assets/BinbunVFX/` — the `fire_effects/` and `magic_orbs/` directories are empty
stub folders, and no `beam`/`pulse` families are on disk (census §6 listed 25 sets, but only 5
family dirs exist and just 1 holds a `.tscn`). **Resolution:** every pilot instantiates the ONE
real Binbun aura scene (`basic_area_vfx_01`), TINTED to its ruled hex (OmniLight color-keyed +
glow-mesh modulate). This preserves the king GRAMMAR faithfully (real Binbun scene + tint +
softened OmniLight + 0.08m lift + `aura_clip` wired); only the specific Binbun VARIANT differs,
forced by the gap. `pilot_rig.gd` carries `// TODO(drax): replace basic_area with the ruled
per-kit Binbun scene when the fire_effects / magic_orbs / beam / pulse asset sets are on disk` —
a clean one-line swap of the `AURA_VFX` const (or per-scene export) when the assets land. This
is an asset-availability gap for the conductor to route (likely to whoever owns BinbunVFX
provisioning), not a mapping-brief change.

---

## Verification

Exit predicate met via `scripts/kt2_rig_harness.gd` (headless; instances every rig .tscn, adds
to tree so `_ready()`→build fires, inspects on frame 2): **`RIG_SUMMARY passed=23 failed=0
total=23`**. Body-mesh-under-GeneralSkeleton on all 23; prop socket populated on all 7 ruled
rows; aura node on all 5 pilots; zero mob auras. Retarget verified separately:
`kt2_verify_retarget.gd` → `RT_SUMMARY ok=22 bad=0`.

## Files

- Rig scripts: `scripts/pilot_rig.gd`, `scripts/mob_rig.gd`
- Rig scenes: `scenes/rigs/pilots/*.tscn` (5), `scenes/rigs/mobs/*.tscn` (18)
- Tooling (seam): `scripts/kt2_apply_retarget.py`, `scripts/kt2_verify_retarget.gd`,
  `scripts/kt2_rig_harness.gd`, `scripts/kt2_write_mob_scenes.py`
- Import surgery: 21 `SK_Chr_*.fbx.import` gained the GeneralSkeleton retarget block
  (`SK_Chr_Male_Sorcerer` gained it first as the de-risk probe; total 22 meshes retargeted).

## Handoff note — retarget `.import` edits do NOT travel via git (reproduce step)

The 22 retargeted `SK_Chr_*.fbx.import` files live under `/Assets/Synty/`, which is
**gitignored** (Synty license + size — the repo's established convention; the King's own
`.import` is ignored the same way). So the retarget config does NOT ship in the commit. The
tracked AUTHORITY is the BUILDER: `scripts/kt2_apply_retarget.py` (idempotent — skips
already-retargeted meshes) + `scripts/mob_rig.gd` / `scripts/pilot_rig.gd` + the rig scenes.

**To reproduce on any fresh checkout (conductor/KT-4 host), before the rigs will build:**
```
cd /Users/admin/Games/reincarnated-godot
python3 scripts/kt2_apply_retarget.py                       # inject retarget block + clear caches
/Applications/Godot.app/Contents/MacOS/Godot --headless --import   # reprocess -> GeneralSkeleton
/Applications/Godot.app/Contents/MacOS/Godot --headless --script scripts/kt2_rig_harness.gd  # verify 23/23
```
(The Sorcerer's `.import` was retargeted via a one-off Edit during de-risk; the script covers
the other 21 — re-running it on a fresh machine where none are retargeted picks up all 22 via
the `_subresources={}` anchor. If a machine already has the Wizard-style block on some, the
script's idempotent SKIP handles it.)

**Signed:** drax, 2026-07-23. COMMIT, NEVER PUSH — conductor verifies + pushes.
