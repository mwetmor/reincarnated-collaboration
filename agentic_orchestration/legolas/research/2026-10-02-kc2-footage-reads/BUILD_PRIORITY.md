# Build priority from the referent line-up — 2026-10-02

**Mode:** A (analytical), read-only except this file. **Agent:** legolas. **Commissioner:** gandalf (Run C-9). The arena fights Matt's actual per-wave line-up from his footage (Q101), not the roster-wide frequency, so the tier-2 build order follows the line-up.

**Inputs:**
- `referent_lineup_by_wave.csv` in this folder: 84 rows of wave × spawn point × record, with count and confidence. It includes the 17 summon identities from `README.md` § 1.
- The roster packet `../2026-10-02-crucible-enemy-roster-packet/roster.json`: record → rig (`type_id`), role, equipped items, the bind-pose box, the attack-kind mix, and the rig clips of the summoned bodies.

**Built set (given):** `aetherialcorruption`, `wraith`, `devourer`, `crabmonstrosity`, `golemswamp_phase01`, `hero01_unarmed`, `sandlizard`, `wendigo`, `aetherialimp`, `carnivorousplant01a_p1`, `basilisk`, `cannibal`, `thornedhorrora01`, `skeleton_01a`, `heroine01_unarmed`, `voidfiend`, `aetherialbloater`, `yeti`, plus `chthonianrylok` (3D).

**Naming rule:** rows are keyed by the roster's `type_id` and record names only. Descriptions are generic. No source display names appear here; don't put record names into an image, mesh or animation prompt.

## 0. Short answer

- **The built rigs already carry 80.6 % of the referent's on-screen bodies** (127.4 of 158.1 confidence-weighted).
- **Not built: 29.8 (18.8 %).**
- **Unmapped: 0.9 (0.6 %).** These are 5 unresolved HP fingerprints plus 1 summon with no rig in the packet.
- **One rig dominates what is left:** `chthonianservitor`, at **8.6 bodies**. That is 29 % of the not-built remainder: six trash bodies in w157, a boss in w159, and its summoned drones.
- **After that the tail is flat:** about 2 bodies each for the next six, then 1 for each single named boss.
- **`thornedhorrora01` is built but has 0 referent bodies.** The referent's w152 p03 rolled basilisk trash instead (README § Summary).

**Top 10 not-built rigs by referent on-screen bodies:**

| # | rig | exp. bodies | what it is (generic) |
|---|---|---|---|
| 1 | `chthonianservitor` | **8.6** | Very large multi-legged insectoid. 6 trash in w157 + 1 boss in w159 (MEDIUM, implied) + 2 summoned drones. |
| 2 | `possessedstatue` | **2.4** (raw 4) | Animated statue with a 2H spear. 4 bodies in w156, MEDIUM confidence. |
| 3 | `skeleton_01a_b` | **2.2** | Skeleton variant: the w160 nemesis + its revenant summon + a w153 bounty hero. **It probably reuses built `skeleton_01a`** (same clip directory and bone count). |
| 4 | `woollyrhino` | **2.0** | Heavy horned quadruped. 2 simultaneous heroes in w157. |
| 5 | `aetherialwisp` | **2.0** | Two stationary crystal summons of the w160 nemesis. VFX only. |
| 6 | `maggot01a`\* | **2.0** | Larva summons of the w159 boss. **No roster type.** |
| 7 | `aetherialworm`\* | **2.0** | Worm summons of the w157 boss. **No roster type.** |
| 8 | `aetherialcolossus` | **1.0** | Giant brute boss, w160 |
| 9 | `fleshhulk_unarmed` | **1.0** | Hulking brute boss, w159 |
| 10 | `golembone_phase01` | **1.0** | Bone-golem hero, w158 |

Ranks 11–15 are also 1.0 each: `chthonianherald`, `korvaaksascended01a`, `aetherialfleshshaper`, `sandbeetle01a`, `abomination`. The last two are `hellhound` (0.3; 0.9 if the unmapped hound summon shares it) and `slith01` (0.3).

## 1. Method

**Confidence weight.** HIGH = 1.0, MEDIUM = 0.6, LOW = 0.3, UNKNOWN = 0. This is a convention I chose [I]. The unweighted ("raw") column is shown beside it, so any other weighting can be applied.

**On-screen count.** I use the CSV's `count_min`: the most bodies of that fingerprint in one frame. It was validated exactly on w160, and it is a **lower bound** for bodies never engaged on screen (README § 1.1). `count_tracker_upper` over-counts and is not used.

**Alternatives.** A row naming several candidates ("X or Y", or a sibling class) splits its count equally across them, unless the CSV favours one:
- w157 `yetidire_c01` 0.7 / `aetherialbloater_c01` 0.3;
- w157 yeti siblings 0.4 / 0.4 / bloater 0.2.

A row naming two simultaneous bodies ("X + Y") splits its count between them.

**One row split in two.** The w159 row `beetle_maggot01 (+ chthonianservitor_lunalvalgoth?)` is split into the beetle boss (HIGH, 1) and the implied servitor boss (MEDIUM, 1). The drone summon is the evidence; the CSV note says the drones imply that boss at p01. That gives 85 entries, not 84.

**Rig of a record.** The rig is read from the roster's `members_detail` (all 80 named records resolve). Unnamed hero classes go to their family's rig: crab heroes → `crabmonstrosity`, corruption heroes → `aetherialcorruption`, imp heroes → `aetherialimp`, skeleton heroes → `skeleton_01a` (every `skeleton_h*` record is on that rig). Summons use the roster's `summoned_bodies[].rig_clip`.

**Two summons have no roster type.** Their rig is named after their clip prefix and **marked with \***:
- `aetherialworm_b0x_summon` → `aetherialworm`\* (rig key `aetherialworm_combatidle_a01`);
- `beetle_maggot01_maggotsummon` → `maggot01a`\* (rig key `maggot01a_run_a01`).

**Body plan.** Built rigs use `../2026-10-02-mixamo-library-probe/ENEMIES.md` § 1. For new rigs I used the roster's bind-pose box (H/D = height ÷ depth; ≥ 1.3 reads as biped) plus archetype knowledge, and marked *(inferred)* where no box exists.

**Weapon.** The animation prefix plus the equipped loot classes. All referent records animate `unarmed`, but several bosses equip a 1H weapon + shield or a caster weapon + focus.

**Own mesh?** **yes** means the record's mesh differs from its rig's lead mesh. The rig is built, but that boss or hero needs its own mesh or skin.

## 2. Ranked: not-built rigs

| rank | rig | exp. bodies | raw | waves | records (row keys) | body plan | generic description | suggested route |
|---|---|---|---|---|---|---|---|---|
| 1 | `chthonianservitor` | **8.60** | 9.00 | 157, 159 | `chthonianservitor_b01`, `chthonianservitor_b02`, `chthonianservitor_c01`, `chthonianservitor_a01`, `chthonianservitor_lunalvalgoth`, `chthonianservitor_a01_summon` | non-biped, insectoid | very large multi-legged insectoid (box H/D 0.87; family Chthonic + Insectoid; locomotion clip is a walk) | Blender |
| 2 | `possessedstatue` | **2.40** | 4.00 | 156 | `statue_a01`, `statue_a02`, `statue_b01`, `statue_b02` | biped humanoid | animated statue with a two-handed spear (equipped Spear2h; box H/D 3.7) | Mixamo |
| 3 | `skeleton_01a_b` | **2.20** | 2.33 | 153, 160 | `ro_bounty12`, `nemesis_orderdeathsvigil_01`, `nemesis_orderdeathsvigil_01_revenantsummon` | biped humanoid | skeleton; same clip directory and 39-bone count as built skeleton_01a (bone names not compared) | Mixamo |
| 4 | `woollyrhino` | **2.00** | 2.00 | 157 | `rhino_h02` | quadruped | heavy horned grazer-beast (box very long, H/D 0.56) | Blender |
| 5 | `aetherialwisp` | **2.00** | 2.00 | 160 | `aetherialvanguard_crystal` | stationary prop | crystal summon on the generic anomaly/trap rig; VFX pulse only | none (VFX only) |
| 6 | `maggot01a*` | **2.00** | 2.00 | 159 | `beetle_maggot01_maggotsummon` | serpentine crawler | larva summon; NO roster type | Blender |
| 7 | `aetherialworm*` | **2.00** | 2.00 | 157 | `aetherialworm_b0x_summon` | serpentine | burrowing worm summon; NO roster type (its rig key is a combat-idle clip, so it may not travel) | Blender |
| 8 | `aetherialcolossus` | **1.00** | 1.00 | 160 | `aetherialcolossus_galakros` | biped brute | giant crystal-studded brute (box H/D 2.5) | Mixamo |
| 9 | `fleshhulk_unarmed` | **1.00** | 1.00 | 159 | `aetherial_fleshhulk_mine` | biped brute | hulking flesh brute (box H/D 3.2) | Mixamo |
| 10 | `golembone_phase01` | **1.00** | 1.00 | 158 | `skeletalgolem_h03` | biped brute | bone golem (box H/D 2.3) | Mixamo |
| 11 | `chthonianherald` | **1.00** | 1.00 | 157 | `chthonianherald_h02` | biped humanoid | tall robed caster, 108 bones (cloth/tentacles); box H/D 5.8 | Mixamo |
| 12 | `korvaaksascended01a` | **1.00** | 1.00 | 154 | `fatherkymon` | biped humanoid (inferred) | ascended caster boss; may hover; no box | Mixamo |
| 13 | `aetherialfleshshaper` | **1.00** | 1.00 | 152 | `aetherialfleshshaper_haraxis` | biped humanoid (inferred) | aether caster boss; no mesh box in the packet | Mixamo |
| 14 | `sandbeetle01a` | **1.00** | 1.00 | 159 | `beetle_maggot01` | hexapod insect (inferred) | giant beetle; 19 bones; no box | Blender |
| 15 | `abomination` | **1.00** | 1.00 | 153 | `kc_bounty13` | large non-biped (inferred) | multi-limbed chthonic monster; 56 bones; locomotion clip is a walk; no box | Blender |
| 16 | `hellhound` | **0.30** | 0.50 | 156 | `direwolf_frozenwastes_01` | quadruped | large canine (the record is a giant-wolf boss) | Blender |
| 17 | `slith01` | **0.30** | 0.50 | 153 | `dc_bounty08` | serpentine-humanoid (inferred) | snake-bodied humanoid; no box | Blender |

**Notes on the ranking:**
- **Tie order:** pool bodies before summons, then bipeds before non-bipeds (bipeds are cheaper on the Mixamo route), then later wave first.
- **The suggested route** follows `ENEMIES.md`: bipeds → Mixamo clips on a humanoid auto-rig; non-bipeds → Blender. A stationary prop needs a VFX pulse only.
- **`possessedstatue`** equips a 2H spear. Mixamo has no spear pack, so the Great Sword Pack's 2H set (owned) is the nearest grip [I].
- **`skeleton_01a_b`** may need no new rig at all: same clip directory (`creatures/enemies/skeleton/anm`) and the same 39-bone count as built `skeleton_01a`. The roster flags equal bone count as *necessary, not sufficient*; bone names weren't compared. Its three records need meshes: a caster-robed nemesis, a heavy revenant summon, and a 1H blunt + shield bounty hero.

## 3. One rig, several named bosses

| Rig | Built | Named bosses / nemeses / bounty heroes it carries (row keys) | Implication |
|---|---|---|---|
| `hero01_unarmed` | yes | `witchgod_finalboss` (w159; equips 1H melee + shield), `nemesis_aetherialvanguard_01` (w160; caster weapon + focus) | Rig done. **Two own meshes needed.** |
| `heroine01_unarmed` | yes | `witch_janaxia` (w156), `witch_larria` (w156, MEDIUM), `humanascendant_mindthief_01` (w155), `ku_bounty_06` (w153, MEDIUM; 1H axe + shield) | Rig done. **Up to four own meshes.** The witches equip caster weapon + focus. |
| `chthonianrylok` | yes (3D) | `chthonianrylok_gabalthunn` (w154), `chthonianrylok_ekketzul` (w159) | Two boss meshes (winged and fire variants). |
| `yeti` | yes | `nemesis_beast_01_p1` (w154 **and** w160) | One nemesis mesh, used in two waves |
| `aetherialcorruption` | yes | `aetherialcorruption_intro` (w155) plus hero class (w152) | Boss mesh |
| `aetherialbloater` | yes | `aetherialbloater_malmouthdocks_01` (w157) | Boss mesh + its worm summons (`aetherialworm`\*, no rig) |
| `skeleton_01a_b` | **no** | `nemesis_orderdeathsvigil_01` (w160) + its revenant summon, `ro_bounty12` (w153, MEDIUM) | See § 2 notes |
| `chthonianservitor` | **no** | `chthonianservitor_lunalvalgoth` (w159, MEDIUM, implied) + six trash (w157) + drones | Builds trash, boss and summon in one rig |
| `hellhound` | **no** | `direwolf_frozenwastes_01` (w156, MEDIUM, 0.25 share) | Probably also the unmapped `hellhound_witchgod_b01_summon` (w159) [I] |

**`hero01_sword1h`, `hero01_sword2h` and `heroine01_sword1h` carry no referent body.** No record in the referent line-up resolves to them. They appear in the roster only through summon records (`ghost_b02_summon` … `ghost_b04_summon`) that the footage did not read. They can wait.

## 4. Unmapped and low-confidence rows

| Row | Wave | What | Weighted | Raw | Why unmapped / caveat |
|---|---|---|---|---|---|
| 27 | 153 | bounty hero, L107 HP class | 0.3 | 1 | HP class shared by about 33 bounty records |
| 28 | 153 | HP 447,994 | 0 | 1 | No record reproduces it (README) |
| 39 | 155 | boss-class L108 body | 0 | 1 | Only one w155-legal member, already counted; seam reading |
| 42 | 156 | 4th boss-class body L106 | 0 | 1 | All three boss points already filled; a clone or mis-levelled body |
| 47 | 156 | HP nearest `aetherialbloater_b01_summon` | 0 | 1 | −0.24 % residual; not counted on the bloater |
| 78 | 159 | `hellhound_witchgod_b01_summon` | 0.6 | 1 | **No rig in the roster packet** (not among its summoned bodies); owner inferred |

**Other caveats:**
- **MEDIUM rows that move the ranking:**
  - `possessedstatue`: both w156 rows MEDIUM; the HP isn't reproduced by the model, but the name was read.
  - `chthonianservitor_lunalvalgoth`: implied by its drones, not read.
  - The crab-hero and corruption-hero split in w152 row 9.
- **Summon counts depend on fight length** (roster § E). The 2-body counts for worms, maggots, crystals and drones are what the referent's fight produced, not a law.
- **The counts are lower bounds.** Off-screen bodies are missing everywhere, built and not-built alike.

## 5. Per-rig roll-up (built and not built)

| rig | built | exp. bodies | share | raw (unweighted) | waves | of which summons | named bosses/nemeses on it | body plan | attack mix (roster) |
|---|---|---|---|---|---|---|---|---|---|
| `wraith` | yes | **20.22** | 12.8% | 20.75 | 151, 155, 156 | 2.00 | — | floating | projectile 28% · melee 23% · aura 19% |
| `crabmonstrosity` | yes | **16.20** | 10.2% | 19.00 | 152, 158 | 7.00 | — | hexapod-crab | melee 41% · projectile 31% · aoe 22% |
| `aetherialcorruption` | yes | **15.20** | 9.6% | 16.00 | 152, 155, 156 | 2.00 | `aetherialcorruption_intro` | biped brute | projectile 53% · melee 31% · aura 8% |
| `skeleton_01a` | yes | **12.60** | 8.0% | 16.00 | 153, 158, 160 | 7.00 | — | biped humanoid | projectile 49% · aoe 30% · aura 9% |
| `chthonianservitor` | **no** | **8.60** | 5.4% | 9.00 | 157, 159 | 2.00 | `chthonianservitor_lunalvalgoth` | non-biped, insectoid | projectile 55% · melee 27% · aura 11% |
| `basilisk` | yes | **8.50** | 5.4% | 9.50 | 152, 156 | 0.00 | `basilisk_witchritual` | quadruped | aoe 66% · projectile 28% · aura 3% |
| `carnivorousplant01a_p1` | yes | **8.00** | 5.1% | 8.00 | 151, 153 | 2.00 | — | stationary plant | melee 50% · projectile 50% |
| `cannibal` | yes | **8.00** | 5.1% | 8.00 | 154 | 0.00 | — | biped humanoid | projectile 39% · melee 29% · buff 25% |
| `yeti` | yes | **7.38** | 4.7% | 8.30 | 154, 157, 160 | 0.00 | `nemesis_beast_01_p1` | biped brute | aoe 34% · projectile 26% · aura 21% |
| `sandlizard` | yes | **6.20** | 3.9% | 7.00 | 158 | 0.00 | — | long reptile | melee 75% · aoe 25% |
| `wendigo` | yes | **5.20** | 3.3% | 6.00 | 153 | 0.00 | — | biped brute | melee 47% · projectile 28% · aura 21% |
| `devourer` | yes | **4.40** | 2.8% | 6.00 | 158 | 0.00 | — | quadruped | aoe 37% · projectile 33% · melee 23% |
| `golemswamp_phase01` | yes | **4.28** | 2.7% | 5.25 | 151, 153 | 0.00 | — | biped brute | aoe 32% · projectile 32% · melee 27% |
| `heroine01_unarmed` | yes | **2.90** | 1.8% | 3.50 | 153, 155, 156 | 0.00 | `humanascendant_mindthief_01`, `witch_janaxia`, `witch_larria` | biped humanoid | projectile 65% · aura 12% · melee 12% |
| `possessedstatue` | **no** | **2.40** | 1.5% | 4.00 | 156 | 0.00 | — | biped humanoid | melee 50% · aoe 33% · projectile 17% |
| `aetherialimp` | yes | **2.20** | 1.4% | 3.00 | 157 | 0.00 | — | biped (small) | melee 58% · projectile 17% · aura 17% |
| `skeleton_01a_b` | **no** | **2.20** | 1.4% | 2.33 | 153, 160 | 1.00 | `nemesis_orderdeathsvigil_01` | biped humanoid | projectile 60% · aoe 20% · buff 10% |
| `chthonianrylok` | yes | **2.00** | 1.3% | 2.00 | 154, 159 | 0.00 | `chthonianrylok_ekketzul`, `chthonianrylok_gabalthunn` | biped brute | melee 37% · aoe 33% · projectile 28% |
| `woollyrhino` | **no** | **2.00** | 1.3% | 2.00 | 157 | 0.00 | — | quadruped | projectile 50% · melee 42% · aura 8% |
| `aetherialworm*` | **no** | **2.00** | 1.3% | 2.00 | 157 | 2.00 | — | serpentine | — |
| `hero01_unarmed` | yes | **2.00** | 1.3% | 2.00 | 159, 160 | 0.00 | `nemesis_aetherialvanguard_01`, `witchgod_finalboss` | biped humanoid | projectile 44% · aoe 24% · melee 24% |
| `maggot01a*` | **no** | **2.00** | 1.3% | 2.00 | 159 | 2.00 | — | serpentine crawler | — |
| `aetherialwisp` | **no** | **2.00** | 1.3% | 2.00 | 160 | 2.00 | — | stationary prop | projectile 64% · aoe 27% · aura 9% |
| `aetherialbloater` | yes | **1.72** | 1.1% | 2.70 | 157, 160 | 0.30 | `aetherialbloater_malmouthdocks_01` | biped (obese, uncertain) | projectile 46% · melee 28% · aoe 15% |
| `aetherialfleshshaper` | **no** | **1.00** | 0.6% | 1.00 | 152 | 0.00 | `aetherialfleshshaper_haraxis` | biped humanoid (inferred) | aoe 45% · projectile 39% · aura 14% |
| `abomination` | **no** | **1.00** | 0.6% | 1.00 | 153 | 0.00 | — | large non-biped (inferred) | aoe 43% · melee 29% · projectile 29% |
| `korvaaksascended01a` | **no** | **1.00** | 0.6% | 1.00 | 154 | 0.00 | `fatherkymon` | biped humanoid (inferred) | projectile 62% · aoe 25% · melee 12% |
| `chthonianherald` | **no** | **1.00** | 0.6% | 1.00 | 157 | 0.00 | — | biped humanoid | projectile 56% · aoe 36% · buff 7% |
| `golembone_phase01` | **no** | **1.00** | 0.6% | 1.00 | 158 | 0.00 | — | biped brute | aoe 36% · buff 32% · projectile 20% |
| `sandbeetle01a` | **no** | **1.00** | 0.6% | 1.00 | 159 | 0.00 | `beetle_maggot01` | hexapod insect (inferred) | projectile 60% · melee 40% |
| `fleshhulk_unarmed` | **no** | **1.00** | 0.6% | 1.00 | 159 | 0.00 | `aetherial_fleshhulk_mine` | biped brute | aoe 44% · melee 26% · projectile 22% |
| `aetherialcolossus` | **no** | **1.00** | 0.6% | 1.00 | 160 | 0.00 | `aetherialcolossus_galakros` | biped brute | projectile 56% · melee 18% · aoe 14% |
| `UNMAPPED` | **no** | **0.90** | 0.6% | 6.00 | 153, 155, 156, 159 | 0.60 | — | — | — |
| `voidfiend` | yes | **0.40** | 0.3% | 0.67 | 153 | 0.00 | — | non-biped (unknown) | projectile 39% · aoe 37% · aura 20% |
| `slith01` | **no** | **0.30** | 0.2% | 0.50 | 153 | 0.00 | — | serpentine-humanoid (inferred) | projectile 38% · aoe 28% · aura 19% |
| `hellhound` | **no** | **0.30** | 0.2% | 0.50 | 156 | 0.00 | `direwolf_frozenwastes_01` | quadruped | melee 50% · aoe 50% |

## 6. Per-record table (every referent identity and summon)

One line per candidate record: a CSV row that names alternatives expands into one line per alternative, each carrying its share. That gives 114 lines from 85 entries (84 CSV rows, with the w159 row split in two). "own mesh?" applies to pool records only. "—" means a summon, or that no lead mesh is recorded.

| row | wave | point | record | rig (`type_id`) | built | role | weapon | body plan | conf (w) | count_min × share | **exp. bodies** | own mesh? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 151 | p01/p04 | `wraith_a01` | `wraith` | yes | trash (Common) | unarmed | floating | HIGH (1.0) | 4 × 1.00 | **4.00** | same as rig lead |
| 2 | 151 | p01/p04 | `wraith_b01` | `wraith` | yes | trash (Champion) | unarmed | floating | HIGH (1.0) | 4 × 1.00 | **4.00** | same as rig lead |
| 3 | 151 | p01/p04 | `wraith_c01` | `wraith` | yes | trash (Champion) | unarmed | floating | HIGH (1.0) | 2 × 1.00 | **2.00** | **yes** |
| 4 | 151 | p02 | `wraith_h03` | `wraith` | yes | champion-hero (Hero) | unarmed | floating | HIGH (1.0) | 2 × 0.50 | **1.00** | **yes** |
| 4 | 151 | p02 | `wraith_h01` | `wraith` | yes | champion-hero (Hero) | unarmed | floating | HIGH (1.0) | 2 × 0.50 | **1.00** | **yes** |
| 5 | 151 | p02/p03 | `wraith_h02` | `wraith` | yes | champion-hero (Hero) | unarmed | floating | LOW (0.3) | 1 × 0.25 | **0.07** | **yes** |
| 5 | 151 | p02/p03 | `wraith_h04` | `wraith` | yes | champion-hero (Hero) | unarmed | floating | LOW (0.3) | 1 × 0.25 | **0.07** | **yes** |
| 5 | 151 | p02/p03 | `wraith_h05` | `wraith` | yes | champion-hero (Hero) | unarmed | floating | LOW (0.3) | 1 × 0.25 | **0.07** | **yes** |
| 5 | 151 | p02/p03 | `swampgolem_h02` | `golemswamp_phase01` | yes | champion-hero (Hero) | unarmed | biped brute | LOW (0.3) | 1 × 0.25 | **0.07** | **yes** |
| 6 | 151 | p03 | `swampgolem_h01` | `golemswamp_phase01` | yes | champion-hero (Hero) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.25 | **0.30** | **yes** |
| 6 | 151 | p03 | `swampgolem_h03` | `golemswamp_phase01` | yes | champion-hero (Hero) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.25 | **0.30** | **yes** |
| 6 | 151 | p03 | `swampgolem_h04` | `golemswamp_phase01` | yes | champion-hero (Hero) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.25 | **0.30** | **yes** |
| 6 | 151 | p03 | `swampgolem_h05` | `golemswamp_phase01` | yes | champion-hero (Hero) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.25 | **0.30** | **yes** |
| 7 | 151 | p05 | `livingplant_a01` | `carnivorousplant01a_p1` | yes | trash (Common) | unarmed | stationary plant | HIGH (1.0) | 4 × 1.00 | **4.00** | same as rig lead |
| 8 | 151 | summon | `livingplant_a01_summon` | `carnivorousplant01a_p1` | yes | summon | summon | stationary plant | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 9 | 152 | p01/p02/p05 | `basilisk_h05` | `basilisk` | yes | champion-hero (Hero) | unarmed | quadruped | MEDIUM (0.6) | 6 × 0.17 | **0.60** | **yes** |
| 9 | 152 | p01/p02/p05 | `basilisk_h02` | `basilisk` | yes | champion-hero (Hero) | unarmed | quadruped | MEDIUM (0.6) | 6 × 0.17 | **0.60** | **yes** |
| 9 | 152 | p01/p02/p05 | `swampcrab_h0x (crab hero class)` | `crabmonstrosity` | yes | hero | — | hexapod-crab | MEDIUM (0.6) | 6 × 0.33 | **1.20** | — |
| 9 | 152 | p01/p02/p05 | `aetherialcorruption_h0x (hero class)` | `aetherialcorruption` | yes | hero | — | biped brute | MEDIUM (0.6) | 6 × 0.33 | **1.20** | — |
| 10 | 152 | p03 | `basilisk_a01` | `basilisk` | yes | trash (Common) | unarmed | quadruped | HIGH (1.0) | 3 × 1.00 | **3.00** | same as rig lead |
| 11 | 152 | p03 | `basilisk_b01` | `basilisk` | yes | trash (Champion) | unarmed | quadruped | HIGH (1.0) | 3 × 1.00 | **3.00** | same as rig lead |
| 12 | 152 | p03 | `basilisk_c01` | `basilisk` | yes | trash (Champion) | unarmed | quadruped | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 13 | 152 | p04 | `aetherialfleshshaper_haraxis` | `aetherialfleshshaper` | **no** | boss (Quest) | unarmed | biped humanoid (inferred) | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 14 | 152 | summon | `aetherialcorruption_c01_summon` | `aetherialcorruption` | yes | summon | summon | biped brute | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 15 | 152 | summon | `swampcrab_a00_summon` | `crabmonstrosity` | yes | summon | summon | hexapod-crab | MEDIUM (0.6) | 5 × 0.50 | **1.50** | — |
| 15 | 152 | summon | `springscrab_a00_summon` | `crabmonstrosity` | yes | summon | summon | hexapod-crab | MEDIUM (0.6) | 5 × 0.50 | **1.50** | — |
| 16 | 153 | p01 | `wendigo_a01` | `wendigo` | yes | trash (Common) | unarmed | biped brute | HIGH (1.0) | 2 × 1.00 | **2.00** | same as rig lead |
| 17 | 153 | p01 | `wendigo_b01` | `wendigo` | yes | trash (Champion) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.50 | **0.60** | same as rig lead |
| 17 | 153 | p01 | `wendigo_b02` | `wendigo` | yes | trash (Champion) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.50 | **0.60** | **yes** |
| 18 | 153 | p01 | `wendigo_c01` | `wendigo` | yes | trash (Champion) | unarmed | biped brute | HIGH (1.0) | 2 × 1.00 | **2.00** | **yes** |
| 19 | 153 | p03 | `skeleton_c01` | `skeleton_01a` | yes | trash (Champion) | unarmed (equips shield) | biped humanoid | MEDIUM (0.6) | 5 × 0.33 | **1.00** | **yes** |
| 19 | 153 | p03 | `skeleton_c02` | `skeleton_01a` | yes | trash (Champion) | unarmed (equips shield) | biped humanoid | MEDIUM (0.6) | 5 × 0.33 | **1.00** | **yes** |
| 19 | 153 | p03 | `skeleton_c03` | `skeleton_01a` | yes | trash (Champion) | unarmed (equips shield) | biped humanoid | MEDIUM (0.6) | 5 × 0.33 | **1.00** | same as rig lead |
| 20 | 153 | p03 | `skeleton_d01` | `skeleton_01a` | yes | trash (Champion) | unarmed (equips 1H blunt + off-hand focus) | biped humanoid | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 21 | 153 | summon | `skeleton_a02_summon` | `skeleton_01a` | yes | summon | summon | biped humanoid | HIGH (1.0) | 4 × 1.00 | **4.00** | — |
| 22 | 153 | p05 | `livingplant_a01` | `carnivorousplant01a_p1` | yes | trash (Common) | unarmed | stationary plant | HIGH (1.0) | 2 × 1.00 | **2.00** | same as rig lead |
| 23 | 153 | p05 | `swampgolem_a01` | `golemswamp_phase01` | yes | trash (Champion) | unarmed | biped brute | HIGH (1.0) | 3 × 1.00 | **3.00** | same as rig lead |
| 24 | 153 | p02/p04 | `kc_bounty13` | `abomination` | **no** | champion-hero (Hero) | unarmed | large non-biped (inferred) | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 25 | 153 | p02/p04 | `dc_bounty08` | `slith01` | **no** | champion-hero (Hero) | unarmed | serpentine-humanoid (inferred) | MEDIUM (0.6) | 1 × 0.50 | **0.30** | same as rig lead |
| 25 | 153 | p02/p04 | `ku_bounty_06` | `heroine01_unarmed` | yes | champion-hero (Hero) | unarmed (equips 1H axe + shield) | biped humanoid | MEDIUM (0.6) | 1 × 0.50 | **0.30** | **yes** |
| 26 | 153 | p02/p04/p06 | `kc_bounty09` | `voidfiend` | yes | champion-hero (Hero) | unarmed | non-biped (unknown) | MEDIUM (0.6) | 1 × 0.33 | **0.20** | same as rig lead |
| 26 | 153 | p02/p04/p06 | `ro_bounty12` | `skeleton_01a_b` | **no** | champion-hero (Hero) | unarmed (equips 1H blunt + shield) | biped humanoid | MEDIUM (0.6) | 1 × 0.33 | **0.20** | **yes** |
| 26 | 153 | p02/p04/p06 | `chthonianfiend_h01` | `voidfiend` | yes | champion-hero (Hero) | unarmed | non-biped (unknown) | MEDIUM (0.6) | 1 × 0.33 | **0.20** | same as rig lead |
| 27 | 153 | p02/p04 | `UNRESOLVED bounty hero (L107 HP class, ~33 records)` | `UNMAPPED` | **no** | ? | — | — | LOW (0.3) | 1 × 1.00 | **0.30** | — |
| 28 | 153 | ? | `UNRESOLVED (HP 447,994)` | `UNMAPPED` | **no** | ? | — | — | UNKNOWN (0) | 1 × 1.00 | **0.00** | — |
| 29 | 154 | p01 | `fatherkymon` | `korvaaksascended01a` | **no** | boss (Quest) | unarmed | biped humanoid (inferred) | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 30 | 154 | p02 | `chthonianrylok_gabalthunn` | `chthonianrylok` | yes | boss (Quest) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 31 | 154 | p03 | `nemesis_beast_01_p1` | `yeti` | yes | nemesis (Boss) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 32 | 154 | p04 | `wendigocannibal_a01` | `cannibal` | yes | trash (Common) | unarmed | biped humanoid | HIGH (1.0) | 5 × 1.00 | **5.00** | same as rig lead |
| 33 | 154 | p04 | `wendigocannibal_b01` | `cannibal` | yes | trash (Common) | unarmed | biped humanoid | HIGH (1.0) | 3 × 1.00 | **3.00** | **yes** |
| 34 | 155 | p01+p02 | `aetherialcorruption_intro` | `aetherialcorruption` | yes | boss (Quest) | unarmed | biped brute | HIGH (1.0) | 2 × 0.50 | **1.00** | **yes** |
| 34 | 155 | p01+p02 | `humanascendant_mindthief_01` | `heroine01_unarmed` | yes | boss (Quest) | unarmed | biped humanoid | HIGH (1.0) | 2 × 0.50 | **1.00** | **yes** |
| 35 | 155 | p03/p04 | `eldritchwraith_a01` | `wraith` | yes | trash (Common) | unarmed | floating | HIGH (1.0) | 4 × 1.00 | **4.00** | **yes** |
| 36 | 155 | p03/p04 | `eldritchwraith_b01` | `wraith` | yes | trash (Champion) | unarmed | floating | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 37 | 155 | p03/p04 | `eldritchwraith_c01` | `wraith` | yes | trash (Champion) | unarmed | floating | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 38 | 155 | p03/p04 | `aetherialcorruption_c01` | `aetherialcorruption` | yes | trash (Champion) | unarmed | biped brute | HIGH (1.0) | 5 × 1.00 | **5.00** | same as rig lead |
| 39 | 155 | ? | `UNRESOLVED boss-class L108` | `UNMAPPED` | **no** | ? | — | — | UNKNOWN (0) | 1 × 1.00 | **0.00** | — |
| 40 | 156 | p01 | `witch_janaxia` | `heroine01_unarmed` | yes | boss (Quest) | unarmed (equips caster weapon + off-hand focus) | biped humanoid | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 41 | 156 | p02+p03 | `witch_larria` | `heroine01_unarmed` | yes | boss (Quest) | unarmed (equips caster weapon + off-hand focus) | biped humanoid | MEDIUM (0.6) | 2 × 0.50 | **0.60** | **yes** |
| 41 | 156 | p02+p03 | `basilisk_witchritual` | `basilisk` | yes | boss (Quest) | unarmed | quadruped | MEDIUM (0.6) | 2 × 0.25 | **0.30** | same as rig lead |
| 41 | 156 | p02+p03 | `direwolf_frozenwastes_01` | `hellhound` | **no** | boss (Quest) | unarmed | quadruped | MEDIUM (0.6) | 2 × 0.25 | **0.30** | same as rig lead |
| 42 | 156 | ? | `UNRESOLVED 4th boss-class body (L106)` | `UNMAPPED` | **no** | ? | — | — | UNKNOWN (0) | 1 × 1.00 | **0.00** | — |
| 43 | 156 | p05 | `aetherialcorruption_b01` | `aetherialcorruption` | yes | trash (Champion) | unarmed | biped brute | HIGH (1.0) | 6 × 1.00 | **6.00** | same as rig lead |
| 44 | 156 | p04 | `statue_a01` | `possessedstatue` | **no** | trash (Champion) | unarmed (equips 2H spear) | biped humanoid | MEDIUM (0.6) | 2 × 0.50 | **0.60** | **yes** |
| 44 | 156 | p04 | `statue_a02` | `possessedstatue` | **no** | trash (Champion) | unarmed (equips 2H spear) | biped humanoid | MEDIUM (0.6) | 2 × 0.50 | **0.60** | same as rig lead |
| 45 | 156 | p04 | `statue_b01` | `possessedstatue` | **no** | trash (Champion) | unarmed (equips 2H spear) | biped humanoid | MEDIUM (0.6) | 2 × 0.50 | **0.60** | **yes** |
| 45 | 156 | p04 | `statue_b02` | `possessedstatue` | **no** | trash (Champion) | unarmed (equips 2H spear) | biped humanoid | MEDIUM (0.6) | 2 × 0.50 | **0.60** | same as rig lead |
| 46 | 156 | summon | `wraith_b01_summon` | `wraith` | yes | summon | summon | floating | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 47 | 156 | ? | `UNRESOLVED (nearest aetherialbloater_b01_summon)` | `UNMAPPED` | **no** | ? | — | — | UNKNOWN (0) | 1 × 1.00 | **0.00** | — |
| 48 | 157 | p01 | `aetherialbloater_malmouthdocks_01` | `aetherialbloater` | yes | boss (Quest) | unarmed | biped (obese, uncertain) | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 49 | 157 | p02 | `rhino_h02` | `woollyrhino` | **no** | champion-hero (Hero) | unarmed | quadruped | HIGH (1.0) | 2 × 1.00 | **2.00** | same as rig lead |
| 50 | 157 | p02 | `chthonianherald_h02` | `chthonianherald` | **no** | champion-hero (Hero) | unarmed | biped humanoid | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 51 | 157 | p03 | `chthonianservitor_b01` | `chthonianservitor` | **no** | trash (Champion) | unarmed | non-biped, insectoid | HIGH (1.0) | 3 × 1.00 | **3.00** | same as rig lead |
| 52 | 157 | p03 | `chthonianservitor_b02` | `chthonianservitor` | **no** | trash (Champion) | unarmed | non-biped, insectoid | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 53 | 157 | p03 | `chthonianservitor_c01` | `chthonianservitor` | **no** | trash (Champion) | unarmed | non-biped, insectoid | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 54 | 157 | p03 | `chthonianservitor_a01` | `chthonianservitor` | **no** | trash (Champion) | unarmed | non-biped, insectoid | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 55 | 157 | p04 | `yetidire_a01` | `yeti` | yes | trash (Champion) | unarmed | biped brute | HIGH (1.0) | 4 × 1.00 | **4.00** | same as rig lead |
| 56 | 157 | p04 | `yetidire_b01` | `yeti` | yes | trash (Champion) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.40 | **0.48** | same as rig lead |
| 56 | 157 | p04 | `yetidire_b02` | `yeti` | yes | trash (Champion) | unarmed | biped brute | MEDIUM (0.6) | 2 × 0.40 | **0.48** | same as rig lead |
| 56 | 157 | p04 | `aetherialbloater_b01` | `aetherialbloater` | yes | trash (Champion) | unarmed | biped (obese, uncertain) | MEDIUM (0.6) | 2 × 0.20 | **0.24** | same as rig lead |
| 57 | 157 | p04 | `yetidire_c01` | `yeti` | yes | trash (Champion) | unarmed | biped brute | MEDIUM (0.6) | 1 × 0.70 | **0.42** | **yes** |
| 57 | 157 | p04 | `aetherialbloater_c01` | `aetherialbloater` | yes | trash (Champion) | unarmed | biped (obese, uncertain) | MEDIUM (0.6) | 1 × 0.30 | **0.18** | same as rig lead |
| 58 | 157 | p05 | `aetherialimp_h01` | `aetherialimp` | yes | champion-hero (Hero) | unarmed | biped (small) | HIGH (1.0) | 3 × 0.33 | **1.00** | **yes** |
| 58 | 157 | p05 | `aetherialimp_h0x (2 more imp heroes)` | `aetherialimp` | yes | hero | — | biped (small) | MEDIUM (0.6) | 3 × 0.67 | **1.20** | — |
| 59 | 157 | summon | `aetherialworm_b0x_summon` | `aetherialworm*` | **no** | summon | summon | serpentine | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 60 | 158 | p01 | `sandlizard_a01` | `sandlizard` | yes | trash (Common) | unarmed | long reptile | HIGH (1.0) | 3 × 1.00 | **3.00** | **yes** |
| 61 | 158 | p01 | `sandlizard_b01` | `sandlizard` | yes | trash (Champion) | unarmed | long reptile | HIGH (1.0) | 2 × 1.00 | **2.00** | **yes** |
| 62 | 158 | p01 | `sandlizard_c01` | `sandlizard` | yes | trash (Champion) | unarmed | long reptile | MEDIUM (0.6) | 2 × 1.00 | **1.20** | **yes** |
| 63 | 158 | p02+p05 | `skeleton_h04` | `skeleton_01a` | yes | champion-hero (Hero) | unarmed (equips 1H axe + shield) | biped humanoid | HIGH (1.0) | 3 × 0.33 | **1.00** | **yes** |
| 63 | 158 | p02+p05 | `skeleton_h0x (2 more, hero HP class)` | `skeleton_01a` | yes | hero | — | biped humanoid | LOW (0.3) | 3 × 0.67 | **0.60** | — |
| 64 | 158 | p02 | `skeletalgolem_h03` | `golembone_phase01` | **no** | champion-hero (Hero) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 65 | 158 | p03/p04 | `chthoniandevourer_a01` | `devourer` | yes | trash (Common) | unarmed | quadruped | HIGH (1.0) | 2 × 1.00 | **2.00** | same as rig lead |
| 66 | 158 | p03/p04 | `chthoniandevourer_b01` | `devourer` | yes | trash (Champion) | unarmed | quadruped | MEDIUM (0.6) | 4 × 0.50 | **1.20** | same as rig lead |
| 66 | 158 | p03/p04 | `chthoniandevourer_b02` | `devourer` | yes | trash (Champion) | unarmed | quadruped | MEDIUM (0.6) | 4 × 0.50 | **1.20** | same as rig lead |
| 67 | 158 | p03/p04 | `swampcrab_a01` | `crabmonstrosity` | yes | trash (Common) | unarmed | hexapod-crab | HIGH (1.0) | 4 × 1.00 | **4.00** | same as rig lead |
| 68 | 158 | p03/p04 | `swampcrab_b01` | `crabmonstrosity` | yes | trash (Common) | unarmed | hexapod-crab | HIGH (1.0) | 3 × 1.00 | **3.00** | **yes** |
| 69 | 158 | p03/p04 | `swampcrab_c01` | `crabmonstrosity` | yes | trash (Champion) | unarmed | hexapod-crab | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 70 | 158 | summon | `swampcrab_a00_summon` | `crabmonstrosity` | yes | summon | summon | hexapod-crab | HIGH (1.0) | 4 × 1.00 | **4.00** | — |
| 71 | 159 | p04 | `beetle_maggot01` | `sandbeetle01a` | **no** | boss (Quest) | unarmed | hexapod insect (inferred) | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 72 | 159 | p01 (implied) | `chthonianservitor_lunalvalgoth` | `chthonianservitor` | **no** | boss (Quest) | unarmed | non-biped, insectoid | MEDIUM (0.6) | 1 × 1.00 | **0.60** | **yes** |
| 73 | 159 | p02 | `aetherial_fleshhulk_mine` | `fleshhulk_unarmed` | **no** | boss (Quest) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 74 | 159 | p03 | `witchgod_finalboss` | `hero01_unarmed` | yes | boss (Quest) | unarmed (equips 1H melee + shield) | biped humanoid | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 75 | 159 | p05 | `chthonianrylok_ekketzul` | `chthonianrylok` | yes | boss (Quest) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 76 | 159 | summon | `beetle_maggot01_maggotsummon` | `maggot01a*` | **no** | summon | summon | serpentine crawler | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 77 | 159 | summon | `chthonianservitor_a01_summon` | `chthonianservitor` | **no** | summon | summon | non-biped, insectoid | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 78 | 159 | summon | `hellhound_witchgod_b01_summon` | `UNMAPPED` | **no** | summon | summon | — | MEDIUM (0.6) | 1 × 1.00 | **0.60** | — |
| 79 | 160 | p01+p03 | `nemesis_orderdeathsvigil_01` | `skeleton_01a_b` | **no** | nemesis (Boss) | unarmed (equips caster weapon + off-hand focus) | biped humanoid | HIGH (1.0) | 2 × 0.50 | **1.00** | same as rig lead |
| 79 | 160 | p01+p03 | `nemesis_aetherialvanguard_01` | `hero01_unarmed` | yes | nemesis (Boss) | unarmed (equips caster weapon + off-hand focus) | biped humanoid | HIGH (1.0) | 2 × 0.50 | **1.00** | **yes** |
| 80 | 160 | p02 | `nemesis_beast_01_p1` | `yeti` | yes | nemesis (Boss) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | **yes** |
| 81 | 160 | p04 | `aetherialcolossus_galakros` | `aetherialcolossus` | **no** | boss (Quest) | unarmed | biped brute | HIGH (1.0) | 1 × 1.00 | **1.00** | same as rig lead |
| 82 | 160 | summon | `aetherialvanguard_crystal` | `aetherialwisp` | **no** | summon | summon | stationary prop | HIGH (1.0) | 2 × 1.00 | **2.00** | — |
| 83 | 160 | summon | `nemesis_orderdeathsvigil_01_revenantsummon` | `skeleton_01a_b` | **no** | summon | summon | biped humanoid | HIGH (1.0) | 1 × 1.00 | **1.00** | — |
| 84 | 160 | summon | `skeleton_a02_summon` | `skeleton_01a` | yes | summon | summon | biped humanoid | HIGH (1.0) | 3 × 1.00 | **3.00** | — |
| 85 | 160 | summon? | `aetherialbloater_b01_summon (probable)` | `aetherialbloater` | yes | summon | summon | biped (obese, uncertain) | LOW (0.3) | 1 × 1.00 | **0.30** | — |

## 7. Sources

- `referent_lineup_by_wave.csv` and `README.md` (this folder; FOOTAGE + DATAMINED, graded per row).
- `../2026-10-02-crucible-enemy-roster-packet/roster.json` (`types[].members_detail`, `summoned_bodies`, `attack_style`, `size`).
- `../2026-10-02-mixamo-library-probe/ENEMIES.md` (body plans and routes for the built tier-1 rigs).
- Computation scripts are in the session scratchpad. They are reproducible from the two inputs and the stated weights.
