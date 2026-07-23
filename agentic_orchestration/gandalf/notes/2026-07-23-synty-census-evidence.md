# Synty Asset Census — Evidence Capture (KING-TWIN F1 substrate)

**Captured by:** gandalf `RUN-CONDUCTOR`, 2026-07-23, from a read-only Explore-agent reconnaissance
of `/Users/admin/Games/reincarnated-godot` (52 tool-uses, evidence-only mandate). Purpose: F1
enumerability evidence for the PROPOSED KING-TWIN run + raw material for the KT-1 asset-mapping
brief. **Evidence, not decisions** — mapping rulings are Matt's at KT-1.

## §1 Scale

- **54 Synty POLYGON pack directories** · 24,560+ FBX/GLTF · 707 Synty `.tscn`.
- **25 Binbun VFX asset sets** · 389 `.tscn` VFX scenes · shared-shader forks already in-repo.
- ~70 project scenes in `/scenes/` (playback, arenas, ravine/crypt levels, render harnesses).

## §2 Character mesh pool (player-kit candidates)

- `polygon-fantasy-characters` (12 SKs): **King, Wizard, Sorcerer, Baird, Female Witch, Female
  Druid, Male Rouge[sic], Female Queen** + peasants.
- `polygon-dark-fantasy` (20 skeletons + attachments): **DarkLord_Male, Witch_Female,
  Priest_Female, Hunter_Male/Female, PlagueDoctor, Gravedigger** + skeleton/demon kin (below).
- `polygon-modular-fantasy-hero-characters`: modular torso/head/arm/leg composition system,
  retargetable on GeneralSkeleton via the existing import plugin.
- Coverage read: caster archetypes (×2 distinct fire sorc identities possible), gunner/rogue,
  heavy melee, bone-witch all have multiple candidates. ~60–80 humanoid meshes total.

## §3 Creature/bestiary pool (starter-set candidates)

| Family | Meshes | Count |
|---|---|---|
| Skeletons | basic / LightArmor / HeavyArmor / Ranger / Flesh (dark-fantasy) + Knight / Slave / Soldier ×2 (dungeon-pack) | 8–9 |
| Zombies | ZombieBoss Blobber / Slobber / Wretch / Brute (boss-tier; downscale for mobs) | 4 |
| Goblins (corrupted-humanoid proxies) | Male / Female / Shaman / Warrior ×2 / WarChief | 6 |
| Ghosts | Ghost_01 / Ghost_02 | 2 |
| Beasts | Werewolf / Werewolf_Undead (hound-proxy) | 2 |
| Demon-kin | Demon ×2 / Gargoyle | 3 |

- **GAP (named):** no `*rat*` / `*quill*` mesh; farm animals static-only (non-skeletal). D2
  starter mob **Spike Fiend/Quill Rat has no direct mesh** → KT fallback: starter-set
  substitution (harvest carried 5 D2 mobs; 4 suffice) or proxy, logged — never silent.
- Total ~25–30 creature skins; recolor/rescale/retarget covers a 15–20 mob roster.

## §4 Weapons + props

250+ meshes: staves/wands (`SM_Wep_Staff_01`, `SM_Prop_WizardStaff_01`, `SM_Prop_Wand_01`,
`SM_Prop_Druid_Staff_01`), swords incl. the king's `SF_Wep_Elven_Greatsword_01`, axes, maces,
bows/crossbows (`SM_Wep_Crossbow_01` + rigged variant — purifier-gunner candidate), halberds,
90+ shields. All five pilot-kit hand-props coverable.

## §5 Environments

- `polygon-dungeon-pack`: **463 modular pieces** — tile floors ×7 families, wall/archway/trim
  sets, pillars, platforms, bone/macabre deco (skulls, ribcages, spines, bone piles), rubble.
- Plus `polygon-dark-fortress`, `polygon-dwarven-dungeon(±map)`, `polygon-simple-dungeons`,
  `polygon-elven-realm` (king's architecture), 200+ further pieces.
- **Existing arena scenes:** `arena_room / open_arena / chokepoint_corridor / descent /
  mini_boss / boss_with_adds / magic_pack / elite_pack`, `boss_arena_30x30`, ravine family
  (`ravine_assembly_1x4(±baked) / carved / atgrade`), `crypt_vault_node(±baked)`.

## §6 VFX families (element-keyed aura/skill candidates)

Binbun: **fire_effects** (assets-19) · **beam_vfx** (12, 25 — channel-cone candidate) ·
**magic_projectiles** (20, 22) · **impact_explosions** (21) · **poison_effects** (18) ·
**ice_effects** (9) · **muzzle_flash** (13, 24) · **magic_areas** incl.
`basic_area_vfx_01` (the king's golden aura) · loot/portal/smoke. Custom juiced shaders ×4
(`loot_*_juiced.gdshader`) + `aura_clip` / `king_clip` interior-scissor shaders in `/scripts/`.

## §7 The king exemplar — decomposed grammar (E4 twin-criteria substrate)

**Scene:** `scenes/probe_king_mcp.tscn` · **rig:** `scripts/king_rig.gd` (`KingRig`).

```
KingRig ─ Body (SK_Chr_King_Male_01, elven-realm; scale→1.85m; GeneralSkeleton retarget)
  ├─ HeadSocket(BoneAttachment3D "head") ─ Crown · Elf ears · Hair
  ├─ HandSocket("hand_r") ─ Greatsword (simple-fantasy, cross-pack) + teal emissive blade
  │     (#3DE3E8, energy 0.7) + sword_loot_vfx.tscn (juiced, 0.28 scale, +0.55m)
  ├─ Cape ─ UNSKINNED static extract from Capes.fbx on spine_03 socket (bind-pose-leak fix)
  ├─ HolyAura ─ Binbun basic_area_vfx_01 + aura_clip shader + OmniLight energy 0.55
  │     (bloom-washout tuning, Matt 2026-06-22) + 0.08m lift
  └─ KingAnim ─ anim-base-locomotion idle/walk retargeted; 0.18s crossfade
Camera FOV 30° @ (0.85,1.95,1.7)→(0,1.66,0) · Key DirectionalLight (−22°,28°,0°) E2.4 ·
ambient (0.45,0.47,0.52) E0.8 · glow ON
```

**Critical findings (agent-verified):** armor/cape BAKED into body mesh (no dress-up slots);
exactly FOUR attachments (crown/ears/hair/sword); sword pose lives in hand_r LOCAL frame
(re-solves per animation frame); cape must be unskinned-extracted; interior-clip shaders
scissor body+aura to room bounds. **This is the reusable rig recipe** — per-kit instantiation =
body mesh + hand prop + element-keyed aura + retargeted locomotion.

## §8 Playback substrate

`scenes/replica_playback.tscn` + `scripts/replica_playback.gd` already build PROCEDURALLY:
arena, camera, lights, entity proxies, HP bars, floaters, telegraphs, aim-line, scrubber;
interactive + headless smoke modes; frames external via `--frames-dir`. **KING-TWIN's KT-4 is a
proxy→rig swap inside an existing working window, not a scene from scratch.**

## §9 Census verdict (agent, conductor-concurred)

**NO BLOCKER** for 5 player rigs + 15–20 mob roster + arena + VFX at king-grammar quality from
on-disk assets. Named gap: quill-rat (§3). Retarget pipeline + clip-shader system pre-exist.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
