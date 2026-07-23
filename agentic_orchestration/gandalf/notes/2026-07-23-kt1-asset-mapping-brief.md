# KT-1 Asset-Mapping Brief — KING-TWIN run (SCENEWRIGHT + SPEC-AUTHOR)

**Author:** gandalf (`SCENEWRIGHT`+`SPEC-AUTHOR`), 2026-07-23. **Run:** KING-TWIN (Matt-ratified
autonomous run dressing the KIT-FIDELITY auto-battle in Synty assets to the king-exemplar's
fidelity). **Purpose:** the ruling brief for KT-2/KT-4 — one row per entity, exact asset names,
king-grammar per row. **These are LEANS — Matt rules every row + every fork.**

**Substrate:** census `…/gandalf/notes/2026-07-23-synty-census-evidence.md`; harvests
`…/legolas/notes/2026-07-23-kf23-harvest-{d2,poe1,poe2,gd}.md`. All exact mesh/scene names below
verified on-disk 2026-07-23 (read-only recon of `/Users/admin/Games/reincarnated-godot`).

**KING-SINGULARITY CONSTRAINT (honored throughout):** `SK_Chr_Male_King`, the crown attachment,
and `SF_Wep_Elven_Greatsword_01` are the exemplar's signature — assigned to NO pilot fighter and
NO mob. The twin criteria copy the king's GRAMMAR (mesh + hand-socket prop + element-keyed aura +
retargeted locomotion + camera/light register), never his identity.

**King-grammar recipe (per §7 census, applied to every player row):** body SK (GeneralSkeleton
retarget, scale to ~1.85m) · hand_r BoneAttachment3D prop · element-keyed Binbun aura via
`aura_clip` interior-scissor shader + OmniLight (~0.55 energy) · retargeted idle/walk locomotion.
Mobs get body + optional aura only (no hand-socket prop unless armed identity demands it).

---

## TABLE A — PLAYER-5 PILOT KITS (aura + prop REQUIRED)

| Entity | Proposed mesh (exact Synty) | Hand prop (exact) | Aura (Binbun family + tint) | Named ALTERNATE mesh | Rationale (one line) |
|---|---|---|---|---|---|
| `d2-firewall-sorc` | `SK_Chr_Male_Sorcerer` | `SM_Prop_WizardStaff_01` (hand_r) | `fire_area_03.tscn` + **deep-orange/ember tint** `#FF6A1A` | `SK_Chr_Male_Wizard` | Robed male caster reads "sorceress-class fire mage"; ground fire-area aura literally IS Fire Wall's floor-fire idiom. |
| `d2-fire-sorc` | `SK_Chr_Female_Witch` | `SM_Prop_Wand_01` (hand_r) | `fire_area_06.tscn` + **hot-yellow/white-core tint** `#FFD23A` | `SK_Chr_Female_Druid` | The census-named ×2-distinct fire read: female-witch silhouette + wand + brighter yellow core distinguishes her from the male ember-sorc at a glance in the same arena. |
| `gd-flames-of-ignaffar-purifier` | `SK_Chr_Hunter_Male_01` | `SM_Wep_Crossbow_01_Rigged` (hand_r; the rigged variant) | `beam_vfx_04.tscn` (channel cone) + **fire-orange tint** `#FF7A24` | `SK_Chr_Male_Rouge_01` | Purifier = gunner; census names the rigged crossbow as the gunner candidate; FoI is a channeled fire CONE → beam_vfx is the channel-cone family. |
| `poe2-bonestorm` | `SK_Chr_Witch_Female_01` (dark-fantasy) | `SM_Prop_Druid_Staff_01` (hand_r) | `magic_orb_basic_vfx_01.tscn` orbit (magic_orbs family, assets-14) + **bone-white/pale-violet tint** `#D9D2E8` | `SK_Chr_Priest_Female_01` | Dark-fantasy witch = the bone-witch class; physical/bone-tinted orb-orbit (NOT fire) marks her as the non-elemental caster; pale-violet bone tint per §6 magic/projectile family. |
| `poe1-cyclone` | `SK_Chr_DarkLord_Male_01` (dark-fantasy) | `SF_Wep_GreatAxe_01` (hand_r, 2H) | `pulse_area_vfx_03.tscn` (spin-pulse) + **steel-gray/dust tint** `#9AA0A6` | `SK_Chr_Hunter_Male_01` + `SF_Wep_Human_Greatsword_01` | Heavy armored melee silhouette; 2H greataxe from the axe pool (deliberately NOT the elven greatsword); pulse-area aura reads as the physical whirl of Cyclone, no element color. |

**Prop/aura notes for the pilot rows:**
- Every aura instantiates through the king's `aura_clip` interior-scissor shader + OmniLight recipe
  (§7) — same rig, different Binbun scene + tint. Tints are hex leans; galadriel/drax may nudge for
  bloom-washout parity per the king's 2026-06-22 tuning.
- `poe2-bonestorm` is the ONLY non-fire pilot — deliberate: three of five kits are fire-family
  (firewall/fire-sorc/FoI), so bonestorm's bone-white and cyclone's steel-gray are the read-apart
  anchors. If all five glowed orange the arena would be unreadable (the D2-screen-of-fire problem).

---

## TABLE B — MOB STARTER SETS (prop/aura MAY read "none"; default = NO aura per Fork 2)

### D2 — Act-1 Normal (harvest-confirmed 5 identities; see Fork 1 re: quill-rat)

| Entity | Proposed mesh (exact Synty) | Hand prop | Aura | Named ALTERNATE mesh | Rationale |
|---|---|---|---|---|---|
| D2 Fallen | `SK_Chr_Goblin_Male` (dungeon-pack) | none — unarmed | none | `SK_Chr_Goblin_Warrior_Male` | Fallen = small cackling imp-goblin; the goblin family IS the corrupted-humanoid proxy. |
| D2 Zombie | `SK_Chr_ZombieBoss_Wretch_01` (downscaled ~0.8) | none — unarmed | none | `SK_Chr_ZombieBoss_Slobber_01` | Only zombie skins on disk are the ZombieBoss set; Wretch is the leanest → downscale for trash-mob. |
| D2 Skeleton | `SK_Chr_Skeleton_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_Skeleton_Soldier_01` (dungeon-pack) | Basic skeleton, the genre-anchor undead. |
| D2 Corrupt Rogue | `SK_Chr_Hunter_Female_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_Hunter_Male_01` | Dark Hunter/Vile Hunter = corrupted female archer → Hunter_Female class per census anchor. |
| D2 Spike Fiend / Quill Rat | **SEE FORK 1** — lean = OMIT (starter-set substitution) | — | — | (proxy capsule if Option B) | No `*rat*`/`*quill*` mesh exists (census-named gap). |

### PoE1 — zone-68 white-map set (harvest-confirmed identities)

| Entity | Proposed mesh (exact Synty) | Hand prop | Aura | Named ALTERNATE mesh | Rationale |
|---|---|---|---|---|---|
| PoE1 Cannibal | `SK_Chr_Goblin_Warrior_Male` (dungeon-pack) | none — unarmed | none | `SK_Chr_Goblin_Male` | Feral cannibal-humanoid → goblin-warrior body reads savage. |
| PoE1 Goatman | `SK_Chr_Demon_Male_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_Demon_01` | Horned bipedal beast-man → demon-kin is the closest horned silhouette. |
| PoE1 Corrupted Rhoa | `SK_Chr_Werewolf_01` (rescale) | none — unarmed | none | `SK_Chr_Werewolf_Undead_01` | No bird mesh; large fast charging beast → werewolf is the beast-charger proxy (flag mismatch, Fork 4). |
| PoE1 Skeleton (Rhoa-skeleton variant) | `SK_Chr_Skeleton_LightArmor_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_Skeleton_Ranger_01` | The RhoaSkeletonBlackMap variant is a skeletal reanimate → skeleton family. |
| PoE1 Goatman (2nd, ranged) | `SK_Chr_Goblin_Shaman` (dungeon-pack) | `SM_Prop_Wand_01` (hand_r) | none | `SK_Chr_Demon_01` | The CannibalFemaleThrowFire / caster-goatman → shaman with wand marks the ranged-caster mob. |

### PoE2 — Act-1 early (identities INFORMAL per harvest — SEE FORK 4 for Matt confirmation)

| Entity | Proposed mesh (exact Synty) | Hand prop | Aura | Named ALTERNATE mesh | Rationale |
|---|---|---|---|---|---|
| PoE2 Skeleton (SkeletonMelee) | `SK_Chr_Skeleton_HeavyArmor_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_Skeleton_Knight` (dungeon-pack) | PoE2 undead-heavy Act-1 → armored skeleton. |
| PoE2 Zombie (ZombieRibbed) | `SK_Chr_ZombieBoss_Brute_01` (downscale) | none — unarmed | none | `SK_Chr_ZombieBoss_Blobber_01` | Ribbed-zombie → brute skin downscaled. |
| PoE2 Bone Deacon (caster undead) | `SK_Chr_Skeleton_Flesh_01` (dark-fantasy) | `SM_Prop_Wand_01` (hand_r) | none | `SK_Chr_Gravedigger_Male_01` | Fleshy bone-caster → flesh-skeleton + wand. |
| PoE2 Cannibal | `SK_Chr_Goblin_Female` (dungeon-pack) | none — unarmed | none | `SK_Chr_Goblin_Warrior_Female` | Same cannibal idiom as PoE1, female variant for roster variety. |

### GD — Act-1 Normal (identities KNOWN, stats FULL GAP per harvest — SEE FORK 4)

| Entity | Proposed mesh (exact Synty) | Hand prop | Aura | Named ALTERNATE mesh | Rationale |
|---|---|---|---|---|---|
| GD Rotting Corpse / Undead | `SK_Chr_ZombieBoss_Slobber_01` (downscale) | none — unarmed | none | `SK_Chr_Skeleton_Flesh_01` | Rotting-undead → slobber zombie skin. |
| GD Ghoul / Corpse-eater | `SK_Chr_Demon_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_Gargoyle_01` | Chthonic ghoul → demon-kin small variant. |
| GD Chthonic Hound | `SK_Chr_Werewolf_Undead_01` | none — unarmed | none | `SK_Chr_Werewolf_01` | Hound → the census-named hound-proxy werewolf (undead variant for the Chthonic register). |
| GD Crazed Villager | `SK_Chr_Gravedigger_Male_01` (dark-fantasy) | none — unarmed | none | `SK_Chr_PlagueDoctor_01` | Deranged human → gravedigger reads as a broken commoner. |
| GD Crazed Thornback (boar/wildlife) | `SK_Chr_Werewolf_01` (rescale, quadruped-ish) | none — unarmed | none | `SK_Chr_Gargoyle_01` | No boar mesh; low beast → werewolf rescaled (flag mismatch, Fork 4). |

**Mob-side coverage read:** every mob resolves to a real on-disk skin via the census creature
families (skeletons ×8–9, zombies ×4 boss-tier downscaled, goblins ×6, demon-kin ×3, werewolves ×2,
ghosts ×2). Recolor/rescale/retarget is the licensed transform per census §3. Two named
proxy-mismatches (Rhoa→werewolf, Thornback→werewolf) are flagged, not silent.

---

## FORK 1 — Quill-rat (D2 Spike Fiend; NO Synty mesh, census-named gap)

- **Option A — starter-set substitution (OMIT):** harvest carried 5 D2 mobs; drop the quill-rat,
  ship the 4 that have honest meshes (Fallen/Zombie/Skeleton/Corrupt Rogue). *Consequence:* the D2
  set loses its only pure-ranged trash — the auto-battle's D2 lane becomes all-melee-approach, which
  slightly narrows the encounter-geometry read but keeps every on-screen entity a HONEST asset.
- **Option B — proxy-with-log:** one visibly-flagged capsule (or `SK_Chr_Skeleton_Ranger_01` as a
  stand-in ranged skirmisher) tagged `PROXY:quill-rat` in the scene. *Consequence:* preserves the
  ranged-trash encounter shape but puts a non-representative body on screen in a FIDELITY run whose
  whole point is asset honesty.
- **LEAN → Option A (OMIT).** This is a fidelity run; a flagged capsule undercuts the exemplar
  standard the run exists to prove. Four honest D2 mobs beat five with one lie. The ranged-geometry
  gap is recoverable in a later lap when a rodent/quill mesh is sourced (Meshy gap-fill or a Synty
  critter pack). Matt rules.

## FORK 2 — Mob-aura default policy

- **Options:** (a) every mob carries a faint element aura; (b) NO aura on starter-set trash — aura
  is RESERVED as an elite/boss/unique marking (the D2 champion/unique idiom).
- **Consequence of (b):** the king reads as singular BECAUSE the room does not glow with him — if
  trash mobs glow, the aura stops meaning "special" and the king's golden aura loses its semantic
  weight. Aura-as-rarity-signal is load-bearing genre grammar (D2 unique/champion auras, PoE rare
  beams).
- **LEAN → (b): none for starter-set trash; aura reserved for elite/boss.** The whole twin-criteria
  thesis is that the king is legible as EXCEPTIONAL; a glowing mob-floor destroys that legibility.
  Matt rules.

## FORK 3 — Arena piece-family (ONE arena)

- **Proposal (polygon-dungeon-pack family mix, per census §5):**
  - **Floor:** `SM_Env_Tiles_01`–`SM_Env_Tiles_07` tile family (the ×7 dungeon floor set) laid as
    the arena deck; `SM_Env_Tile_Simple_01` for plain fill.
  - **Wall / archway:** `SM_Env_Wall_01` + `SM_Env_Wall_02` perimeter; `SM_Env_Ceiling_Arch_01` for
    the entry threshold; `SM_Env_Pillar_Round_01` / `SM_Env_Pillar_Broken_01` corner accents.
  - **Deco register (bone/macabre density, LOW):** sparse `SM_Env_Bone_Skull_01`,
    `SM_Env_Bone_Ribcage_01`, `SM_Env_Bone_Pile`-adjacent (`SM_Env_Pillar_Broken_Pile_01`) at the
    arena edges only — enough to read "crypt" without clutter that fights entity readability.
  - **Swap window:** reuse existing `scenes/boss_arena_30x30.tscn` as the KT-4 proxy→rig swap host
    (census §8 — KT-4 is a proxy swap inside a working window, not a scene from scratch).
  - **King register applied:** the king's camera (FOV 30° @ (0.85,1.95,1.7)→(0,1.66,0)), key
    DirectionalLight (−22°,28°,0°) E2.4, ambient (0.45,0.47,0.52) E0.8, glow ON (§7).
- **LEAN → dungeon-pack floor+wall+pillar as the spine; bone deco kept SPARSE (edges only).** The
  macabre density must stay a garnish — a bone-choked floor competes with the fighters for the
  camera's attention and the run is about entity fidelity, not set-dressing. Matt rules density.

## FORK 4 — Starter-set membership confirmation (informal sets → explicit lists)

The harvests fixed D2 (5 verbatim) and PoE1 (zone-68, well-anchored). **PoE2 mob identities were
unfetchable per-mob (SPA 404s — harvest §KF-3) and GD stats are a FULL GAP though identities are
known.** Proposed explicit 3–5 identity lists per game, flagged for Matt's same-pass confirmation:

- **D2 (confirmed):** Fallen · Zombie · Skeleton · Corrupt Rogue · [Spike Fiend → Fork 1 OMIT].
  → ship **4**.
- **PoE1 (well-anchored):** Cannibal · Goatman · Corrupted Rhoa · Rhoa-Skeleton · caster-Goatman.
  → **5**. (Rhoa→werewolf proxy flagged — no avian mesh on disk.)
- **PoE2 (INFORMAL — Matt confirm identities):** proposed = Skeleton (melee) · Ribbed-Zombie ·
  Bone Deacon (caster) · Cannibal. → **4**. These are gandalf-proposed from the PoE2 undead-heavy
  Act-1 archetype since the harvest could not fetch named mobs; Matt confirms or substitutes.
- **GD (identities KNOWN, stats GAP — Matt confirm the SET):** proposed = Rotting Corpse · Ghoul ·
  Chthonic Hound · Crazed Villager · Crazed Thornback. → **5**. (Thornback→werewolf proxy flagged.)
  Note: GD stats are a full gap (harvest §GD) — mesh mapping proceeds; NUMERIC fidelity for GD is a
  separate KF-2 unblock (Matt/team screenshot path or datamined CSV).

**LEAN:** confirm D2+PoE1 as-is; treat PoE2+GD identity lists above as gandalf-proposed drafts
requiring Matt's explicit yes/substitute in the same ruling pass. Do not let an informal set ship
unconfirmed — the fidelity standard applies to WHICH mobs as much as to how they look.

---

## KT-2 readiness

All 5 pilot rows + ~18 mob rows + arena + VFX resolve to exact on-disk assets at king-grammar
quality. NO BLOCKER (census §9 concurred). Named open items for Matt's ruling pass: Fork 1 (quill
OMIT), Fork 2 (no-trash-aura), Fork 3 (arena family + deco density), Fork 4 (PoE2+GD set
confirmation + 2 flagged beast proxies). King singularity preserved — no King mesh / crown / elven
greatsword assigned anywhere.

**Signed:** gandalf (`SCENEWRIGHT`+`SPEC-AUTHOR`), 2026-07-23.
