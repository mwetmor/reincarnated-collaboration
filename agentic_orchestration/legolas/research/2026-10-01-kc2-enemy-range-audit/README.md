# Research: KC2 enemy attack-range audit against Grim Dawn (2026-10-01)

**Seat:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (RUN-CONDUCTOR, Run KC2-PLAY), ledger **KP-194**
**Matt's finding (verbatim):** *"some of the enemies' range is too far and kill me from outside of the screen."* He ruled it a **range** problem, not a camera problem.
**Mode:** A (analytical). Read-only throughout. No engine, pack, godot or vendor file was modified. The only writes are in this directory.
**Labels used on every number:** **DATAMINED** (GD `.arz` record or `Game.dll`/`Engine.dll` disassembly) · **PACK** (pack row id or pack-substrate CSV) · **INFERRED** (arithmetic or classification by me, with the basis stated) · **FOOTAGE** (none used in this note).

---

## 0 · Summary

1. **The pack's `reach_m` is not GD's attack range. It is a projectile's flight distance or an effect radius.** The oracle (and the port, which copies it) lets a monster attack from distance *d* iff `d <= reach_m`, where `reach_m` = the first non-empty of `projectile_distance` → `skill_radius` → `skill_target_radius`/`projectile_explosion_radius` → 2.4 m (`threat.py:740-759`; `kc2rt_fight.gd:3283-3292`). In GD, `projectileDistance` is a field on the **projectile entity** (`projectilebase.tpl`): how far the projectile flies before it expires. It is not what the AI reads.
2. **GD's AI fire range is decoded, from the binary (DATAMINED).** A monster may start a skill iff
   `centre_distance <= ladder[distanceProfile(skill)] + r_monster + r_player + 0.5`,
   where the ladder is `gameengine.dbr`: **Melee 1.25 · Short 4.75 · Moderate 9.0 · Long 15.0 · Maximum 18.0 · Boss 32.0 m**. Special slots must also pass a per-creature metre annulus, `{short,medium,long}Range{Min,Max}`, measured edge to edge.
3. **873 of 1,816 AI-initiated attacks in the pack have a range that exceeds GD's** (896 under the smaller-radius limb). **801** of them belong to monsters in the waves 151–160 pool. **376** exceed GD by more than 5 m and **194** by more than 10 m. The worst offenders are orbiting and inverse-nova projectiles carrying `projectileDistance = 90 m` or `40–45 m`, where GD fires them from 4.6–17 m.
4. **The root cause is systematic and single: wrong field, not wrong units.** GD's length unit is the metre, and the pack copies GD's numbers byte for byte, so there is no units error (×1.0). The pack took the projectile's **flight cap** (and, for novas and auras, the **effect radius**) as the **fire range**, and ignored `distanceProfile`, the band annulus and the body radii. That substitution accounts for **869 of the 873** over-range rows. The remaining **4** (3 sub-0.1 m melee-fallback cases on tiny pets, 1 `projectile_explosion_radius` row) are noise.
5. **The spawn timer: GD does the opposite of the port.** GD holds the p05 ambush bodies **out of the world** for 4.0 s (`minDelayTime`). It then spawns them **with a spawn animation**, decoded unconditional in `ProxyAmbush::PlaceNextObject`. During that animation an attack request is **PENDING**, and death is **permitted**. The oracle and the port release the bodies at 4.0 s and let them **swing on the first tick** they are in reach. On top of that, the port **draws** the bodies during the 4-s pre-spawn window and makes them un-hittable. That un-hittable window is the "timer" Matt sees.

---

## 1 · Which value decides "the monster can attack the player from distance d": oracle and port

| step | oracle | port | label |
|---|---|---|---|
| distance | `dist = hypot(ax-px, ay-py)`, centre to centre, no radii (`run.py:3611`) | `_dist_to_player(b)` | PACK-code |
| per-slot reach | `choose_slot`: `if dist_m > s.reach_m: continue` (`threat.py:1664`) | `_choose_slot`: `if d > _slot_reach(s): continue` (`kc2rt_fight.gd:3213`) | PACK-code |
| reach value | `_reach_for`: `projectile_distance` (slot meta, then damage rows, **including nested `autoCastSkill`/`buffSkillName` children**) → `skill_radius` → `skill_target_radius`/`projectile_explosion_radius` → `MELEE_REACH_M = D_ENGAGE_M = 2.4` (`threat.py:740-759`) | reads the wire's `reach_m` (pack `monster_offense.json` rowsets `v20` / `y1` / `u1`), then `extent_m`, then 2.4 (`kc2rt_fight.gd:3283-3292`) | PACK |
| swing clock start | `PhaseModel.ENGAGE` (driver of record): φ = first tick with `dist <= max_reach_m` = max over slots; the first swing fires **on that tick** (`threat.py:1585-1645`) | same (`kc2rt_fight.gd:2998-3010`, `3064-3074`) | PACK-code |
| band annulus | exists as `gate_model.SpecialGateFold.annulus_admits` but **disarmed** (`input_closure_v3p7p1.json` constant `C-B4-1`: *"the Range metre annulus is NOT enabled"*; `special_gate_fold = null`) | absent | PACK |

**I reproduced the pack's `reach_m` for all 2,181 loaded rows** by replaying `_reach_for` over the pinned CSVs (`pm2_tg2_attack_*`, `q91_pool338_attack_*`). Every row is attributed, with no residue. The source column is `pack_reach_source` in the table.

---

## 2 · GD's law, decoded (Edition IV `Game.dll` 32-bit, sha `e75925d1…`; listings in `evidence/`)

| # | element | finding | evidence | label |
|---|---|---|---|---|
| L1 | the gate | `ControllerAIStateT<ControllerMonster>::CloseEnoughToUseSkill(target, skill)` returns `GetTargetDistance(owner,target,skill) + GetSkillUseTolerance(skill) >= centre_distance` | `evidence/01` @ `0xd18a0` | DATAMINED [bin] |
| L2 | target distance | `Character::GetTargetDistance` = `skill->GetRange()` + `owner->GetRadius()` + `target->GetRadius()` (the target radius is dropped if the target is not a Character) | `evidence/02` @ `0x491f0` | DATAMINED [bin] |
| L3 | tolerance | `GetSkillUseTolerance` = **0.5**, one shared body for every ControllerAIStateT, and it is vslot `+0x12c` of `ControllerMonsterStateAttack` | `evidence/03` @ `0x62230` | DATAMINED [bin] |
| L4 | skill range | `Skill::GetRange` = `gGameEngine` float selected by `[skill+0x8c]` ∈ 0..5; default 1.0. It sits at vslot `+0x120` on 126 `Skill_*` vtables. **`Skill_AttackSpellBeam/Cone/Drain` override it: 100 m while already running (channel continuation), otherwise the ladder.** None of those three classes appears in this roster | `evidence/04`, `09` | DATAMINED [bin] |
| L5 | ladder | `GameEngine::LoadFromDatabase`: meleeRange→`+0xc48`, shortRange→`+0xc4c`, moderateRange→`+0xc50`, longRange→`+0xc54`, maximumRange→`+0xc58`, bossRange→`+0xc5c`. `records/game/gameengine.dbr` (single carrier, `base`, **identical in Ed IV and Ed II**): **1.25 / 4.75 / 9.0 / 15.0 / 18.0 / 32.0 m** | `evidence/05`; record | DATAMINED |
| L6 | profile parse | `Skill::LoadResources`: `distanceProfile` Melee→0, Short→1, Moderate→2, Long→3, Maximum→4, Boss→5. **An absent or unrecognised value leaves the constructor's 0 = Melee** (`??0Skill` @ `0x3b2fe7`) | `evidence/06` | DATAMINED [bin] |
| L7 | special annulus | `ControllerMonster::IsSkillInProperRange(target, band)`: band 0 (**AnyRange**) ⇒ **TRUE, no limit**. For bands 1/2/3: `d_edge = max(0.5, centre − (r_target + r_self))`, admitted iff `min < d_edge < max`. Min/max come off the creature record (`{short,medium,long}Range{Min,Max}`); the binary defaults are 0/4, 4/8, 8/16. Band strings: ShortRange=1, MediumRange=2, LongRange=3 | `evidence/07`, `08` | DATAMINED [bin] |
| L8 | radius | Engine `Actor::GetRadius` (Object vslot `+0xe4`) = `actorRadius × |transform axis|`. That the transform scale equals the record `scale` is **INFERRED**. So I carry two limbs: **HI** = `actorRadius × scale`, LO = `actorRadius`. Player: `actorRadius 0.32`, `scale 1.05` (Lap F, `pc01`) | `evidence/10` | DATAMINED [bin]; scale link INFERRED |
| L9 | composition | `ChooseBestSkill` tests the annulus (predicate 6) and `CloseEnoughToUseSkill` (predicate 8), both after the chance roll | legolas **D-11** README § 4 | DATAMINED [bin] (prior lap) |

**So the GD fire range, centre to centre, as used for every comparison here (INFERRED arithmetic over DATAMINED terms):**
- basic, chain and tree attacks: `R = ladder[dp] + r_m + r_p + 0.5`
- special slots: `R = min(ladder[dp] + r_m + r_p + 0.5, bandMax + r_m + r_p)`. There is also a **minimum**, `bandMin + r_m + r_p`. For AnyRange, only the first term applies.
- `dp` is read off the **slot's root skill**, the one the AI tests. 295 pack rows carry a nested `*_buff` child instead of the root, and the table carries both.

**Units:** the GD DB length unit is the metre (Lap F: `SkillDistanceFormat={%.1f0 {^E}Meter %s1}`; `meleeTargetDistance = 2.4000000953674316` = the pack's `D_ENGAGE_M`). The pack copies GD values verbatim: 837 rows equal a GD `projectileDistance` exactly. **Conversion: ×1.0. There is no units error.** DATAMINED.

**Edition IV vs II:** 1,557 records compared on every range field. **2 differ:** `giant_a01` `specialAttackRange` (IV LongRange / II MediumRange) and `nemesis_beast_02` `specialAttack2Range` (IV LongRange / II AnyRange). `distanceProfile`, the ladder, `projectileDistance`, `skillTargetRadius` and the radii are identical. See `ed_diff.json`.

---

## 3 · Results

Scope: **2,181 attack rows** the oracle loads. These are the `v20` + `y1` + `u1` rowsets, less the 54 `v20` rows superseded by `y1`. They span 533 records: the waves 151–160 pool (466 members), their pets (57 rows), and 144 rows of roster records outside the 151–160 pool. Every row is in `range_audit_per_attack.csv`, and the column grades are in `range_audit_per_attack.grades.json`.

| class | rows | pack > GD | notes |
|---|---|---|---|
| AI-initiated: basic / chain / tree | 400 | — | gate L1 |
| AI-initiated: special1–5 | 1,416 | — | gates L1 + L7 |
| **AI-initiated, total** | **1,816** | **873** (HI) · 896 (LO) | 801 in the 151–160 pool; 803 by more than 1 m, 376 by more than 5 m, 194 by more than 10 m |
| aura / initial (radius around the caster) | 225 | 15 | all 15 are an aura's reach set to a **nested auto-cast projectile's** 15–20 m flight cap, against an aura radius of 3–5 m |
| dying | 140 | 1 | `bl_bounty10` `gilisten_firestorm`: 24 vs 8 |

**By pack source, AI rows over GD (INFERRED attribution, see § 1):**

| pack source | over GD | of rows |
|---|---|---|
| `projectile_distance` (slot meta) | **547** | 626 |
| `projectile_distance` (damage row) | 71 | 85 |
| `projectile_distance` via a nested `autoCastSkill` | 74 | 102 |
| `projectile_distance` via `buffSkillName` | 1 | 1 |
| `skill_radius` (slot meta) | 107 | 215 |
| `skill_target_radius` (damage row / via buff / via autocast) | 9 / 56 / 4 | 30 / 66 / 4 |
| `projectile_explosion_radius` | 1 | 18 |
| `MELEE_REACH_M` 2.4 fallback | 3 (sub-0.1 m, tiny pets) | 669 |

**The pack is too SHORT just as often.** 943 AI rows are below GD (496 by more than 1 m, 266 by more than 5 m). There are **0 exact matches**, which is expected because GD adds the radii and 0.5. The largest short group is the 2.4 m fallback applied to attacks GD fires at Moderate or Long range (151 Moderate, 64 Long). **The pack's reach is decorrelated from GD's.** It is not a uniform overestimate.

**Worst offenders, waves 151–160 pool, unique root skill:**

| pack row | monster (record) | slot | root skill (class) | pack m | GD dp / band | GD m | diff |
|---|---|---|---|---|---|---|---|
| U1-349 | chthonianservitor_c01 | special2 | bleedspiral (ProjectileOrbiting) | 90.0 | Long / Short 0–4 | 5.24 | +84.8 |
| U1-282 | ku_bounty_10 | special2 | avian_channeldestruction (ProjectileRing) | 90.0 | Moderate / Medium 0–6 | 7.00 | +83.0 |
| U1-1403 | nemesis_eldritch_01 | tree | eldritch_lightningorbital_secondary | 90.0 | Long / – | 17.04 | +73.0 |
| Y1-48 | nemesis_wendigo_01 (Reaper of the Lost) | special3 | wendigo_necroticnovainverse (ProjectileRing) | 40.0 | Boss / Short 0–4 | 5.32 | +34.7 |
| V20-175 | witch_janaxia (Janaxia) | special2 | witch_necroticprojectilenova | 40.0 | Short / Medium 0–12 | 6.05 | +34.0 |
| U1-1416 | nemesis_outlaw_02 | basic | outlaw2_aetherspineslam (ProjectileFan) | 40.0 | Short / – | 6.18 | +33.8 |
| V20-51 | aetherialbloater_malmouthdocks_01 (Blugrug) | special2 | avris_bloodorbnova | 40.0 | Long / Medium 0–9 | 10.48 | +29.5 |
| U1-1429 | nemesis_wendigo_02 | basic | wendigo2_homingrotpool (ProjectileBurst) | 45.0 | Long / – | 16.30 | +28.7 |
| V20-245 | chthonianherald_b01 (Chthonian Portent) | basic | chthonianherald_chaosblast (Projectile) | 45.0 | Long / – | 16.80 | +28.2 |

**Most widespread off-screen offenders**, where the pack exceeds the 12.69 m half-width but GD does not. There are 263 rows over 197 roster records, among them:
- **19 records** — `electrified_lightningnova`: 20 vs ~9.5
- **10** — `aldanar_vitalitynova`: 15 vs ~9.1
- **10** — `swampcrab_waterspout`: 20 vs ~6.5
- **9** — `basilisk_acidbarf`: 20 vs ~3.1 (a Melee wave; the 20 is a nested poison cloud's flight cap)
- **9** — `aetherialcolossus_burningnova`: 15 vs ~9.5
- **8** — `baldim_chaoswave`: 21 vs ~9.9
- **6** — `aetherialimp_aetherfirestrike`: 19 vs ~2.8, a **weapon** strike

**Screen context (INFERRED, for context only; Matt ruled ranges).** The port's camera at `ZOOM-GD` is `ppm = 75.668 px/m`, pitch 52.95°, on a 1920×1080 frame centred on the player (`kc2play_projection.gd`; `kc2p_main.gd:492`). That gives a visible half-width of **12.69 m** and a half-height of **8.94 m**. Pack reach exceeds the half-width on **713** AI rows. **GD's own fire range exceeds it on 563.** Long (15 m), Maximum (18) and Boss (32) profiles reach off-screen by GD's data too: 329 of 533 records have at least one such attack. Correcting the pack removes the 90/45/40/24/20 m outliers. It does **not** make every attacker visible.

---

## 4 · Root cause

The three hypotheses the commission named, tested:

| hypothesis | verdict | basis |
|---|---|---|
| a units mix-up | **FALSIFIED** | m→m, ×1.0. 837 pack values equal GD `projectileDistance` byte for byte (DATAMINED) |
| projectile reach = speed × lifetime | **FALSIFIED** | the pack never multiplies. GD's projectile carries `projectileDistance` directly. `projectilebase.tpl` has no lifetime field besides hit/miss residue TTLs (DATAMINED) |
| a default range where data was missing | **MINOR, AND IT ERRS SHORT** | `MELEE_REACH_M = 2.4` on 669 rows. GD melee is 1.25 + radii + 0.5 = 2.31–4.x m. It goes over GD on only 3 rows, all under 0.1 m |
| **wrong field** | **CONFIRMED: this is the cause** | `_reach_for` reads the **projectile entity's flight cap** (`projectileDistance`), the **effect radius** (`skillTargetRadius`), or a **nested child skill's** projectile distance. GD's AI reads none of these. It reads `distanceProfile` → ladder, plus radii and tolerance (L1–L6), and for specials the band annulus (L7) |

The comment at `threat.py:433-435`, *"`range_band` is a LABEL with no metres anywhere in the corpus"*, and its repetition at `:2227` were already falsified by D-2 (2026-08-24): the metres sit on the creature record. `gate_model.py:38` (`C-B4app-1`, *"the ROSTER's annulus has no decoded metres"*) is falsified the same way. **`distanceProfile` was extracted into the substrate from the start** (`pm2_tg2_attack_slots.csv` column `distance_profile`) and never consumed.

The error **multiplies through the engage clock.** `max_reach_m` (the maximum over slots) anchors φ. One 90 m orbital slot therefore starts a body's swing clock the moment it spawns. From then on, any slot in reach fires on schedule.

---

## 5 · The spawn timer (Matt: *"spawning enemies at the center which I have to wait to kill but which shoot me as soon as their timers start"*)

| question | GD | oracle | port |
|---|---|---|---|
| pre-spawn hold | p05 is `ProxyAmbush`. On all 13 rows for waves 151, 152, 153 and 156–159 (`proxy_w0{1,2,3,6,7,8,9}_p05a`, Ed IV = Ed II, `sm3`): `minDelayTime = maxDelayTime = 4.0`, `minSpawnTime = maxSpawnTime = 3.0`, group 30, `spawnThreshold 15` (DATAMINED, `proxyambush.json`). The body **does not exist** during the hold. Whether the delay is counted from the wave start is the oracle's reading, not decoded here | `spawn_t_s = P05_FIRST_ARRIVAL_S = 4.0`; not on the board before then (`wave_engine.py:543`) | **draws** the bodies during the 4 s with an "ARRIVING" countdown; they **cannot be hit** (`kc2p_token.gd:50-57`; `kc2p_card.gd:51-52`). The card itself says *"Whether the real client draws them before release is undecoded"* |
| invulnerability | **none found.** `invincible = 0` on 466/466 pool records (DATAMINED). The card's *"Character+0x1844 … on your summons only"* stands. **`DieAction` during `SpawnAction` = REPLACE**, so a spawning body *can* be killed (`evidence/13`, matrix pinned by RESID-D1-2) | n/a (absent) | un-hittable during the hold |
| activation delay at spawn | **YES.** `ProxyAmbush::PlaceNextObject` calls `EnableSpawnAnimation` (vslot `+0x318`) **unconditionally** before `FastSpawnEntity` (`evidence/11`). On the controller's first update, `JustSpawnedWithAnimation()` ⇒ a **`SpawnAction`** (type 19) (`evidence/12`). **While it runs, a new `AttackAction` is PENDING and `MoveTo`/`Walk` are PENDING** (`evidence/13`). Duration = the record's `*SpawnAnim`: **31/31 p05 members have one, 0.87–4.90 s, median 1.67 s**; 394/466 pool records have one, 0.40–5.33 s (DATAMINED Ed III `.anm` headers, Lap 08-08 index, `(frames−1)/30`; anim speed 1.0 INFERRED) | **none.** φ = the first tick in reach, and the first swing is **on that tick** | **none** (identical) |
| first special cast | each special is armed by its **`Timeout`**, which counts only after acquisition (D-11). p05 members: 84 special slots, `Timeout` 0.0–8.0 s, median 2.0 (DATAMINED) | first-cast gate = `delay_s` against the **wave** clock (R-PM2-1, falsified by D-11); the decoded `Timeout` arm is disarmed (`special_gate_fold = null`). **16 of the 84 p05 slots have `Delay ≤ 4.0` and are already open at release** | same as the oracle |
| reach from p05 | p05 sits **7.16 m** from the player spawn (PACK `arena.json`, graded ESTIMATED-FOOTAGE ±15° there). **20/31** p05 members have a GD fire range ≥ 7.16 m | **28/31** have pack reach ≥ 7.16 m | same as the oracle |

**Verdict:** the oracle and the port **do not match GD at spawn**. GD has an un-drawn 4-s hold, then a 0.9–4.9 s spawn animation during which the body can be hit and killed but cannot attack or move, then per-special `Timeout` arming. The model has an un-hittable but drawn 4-s hold (port only), then an attack on tick 1. Matt's report matches that inversion exactly. Per-member rows are in `p05_spawn_activation.csv`.

---

## 6 · What star-lord should change for pack v3.8 (each with its source)

1. **Replace every AI-initiated row's `reach_m`** (`v20`/`y1`/`u1`, slots basic, special1–5, chain_initial/next, tree_attack) with `gd_use_range_centre_m_HI` from `range_audit_per_attack.csv`. That value is `ladder[distanceProfile(root skill)] + actorRadius·scale + 0.336 + 0.5`. Sources: L1–L6, L8, and the pack row's own creature record. **This changes reach in both directions** (873 down, 943 up), so the conductor should see both counts before ruling. Emit the LO limb alongside, as Lap F did; L8 is binary evidence for HI, but the scale link is INFERRED.
2. **Publish the special-slot annulus per row:** `gd_range_band`, `gd_band_min_m`, `gd_band_max_m`, measured edge to edge with a 0.5 m floor and strict bounds (L7). Arming it (`gate_model` `annulus`) is a conductor/gamora ruling. **The "no roster metres" premise behind `C-B4-1` and `C-B4app-1` is falsified:** the roster's metres are on its creature records and are now in the table. AnyRange means no limit; it does **not** mean "0 to longRangeMax" (L7 corrects D-2 § 1 on this point).
3. **Keep the damage geometry separate from the fire range.** `projectileDistance`, `skillTargetRadius` and `extent_m` stay in the pack as effect geometry (telegraphs, ring co-landing), but must not feed `reach_m`. Aura and initial rows keep the aura radius. **Correct the 15 aura rows** whose reach came from a nested auto-cast projectile (§ 3).
4. **Name the ladder in the pack as constants:** `meleeRange 1.25`, `shortRange 4.75`, `moderateRange 9.0`, `longRange 15.0`, `maximumRange 18.0`, `bossRange 32.0`, tolerance 0.5, and the absent-profile ⇒ Melee rule. Source: `gameengine.dbr` (Ed IV = Ed II) plus `evidence/03-06`.
5. **Spawn (for the conductor; it touches gamora's and drax's seams):** publish per record `gd_spawn_anim_s` and the decoded rules: ProxyAmbush ⇒ SpawnAction; Attack/Move PENDING; Die REPLACE; no invincibility. Publish the `Timeout` first-cast values too. The port's drawn-but-un-hittable hold has no GD basis in this audit.
6. **Edition note:** `giant_a01` special1 and `nemesis_beast_02` special2 change band between Ed II and Ed IV (§ 2). The pack carries MediumRange and AnyRange (the II values).

---

## 7 · Knowledge gaps not resolved

- **`Actor::GetRadius`'s transform scale versus the record `scale`.** That is why both limbs are given. The HI and LO counts differ by only 23 rows (873 vs 896).
- **Whether `tree_attack` skills are AI-initiated at all.** They sit outside the 8 `ChooseBestSkill` slots, and many are `*secondary`/`*retaliation` procs. I apply L1 as an upper bound. 45 of the 873 over-range rows are tree rows.
- **Whether the `Character` class overrides vslot `+0xe4`.** I decoded the Engine `Actor` body only.
- **Spawn-animation speed and the `+0x12c < 30` limb** of `JustSpawnedWithAnimation`. I did not decode what `+0x12c` counts. Durations assume speed 1.0.
- **Whether the referent's camera equals the port's `ZOOM-GD`** (FOOTAGE-derived register, not re-measured here).
- **Pursuit:** GD's ranged monsters stop at their `CloseEnoughToUseSkill` distance, while the oracle halts every body at 2.4 m. Adjacent, out of scope, not audited.

---

## 8 · Files and provenance

| file | what |
|---|---|
| `range_audit_per_attack.csv` | 2,181 rows: pack value (row id) · GD fields · conversion · GD reference · diff · flags |
| `range_audit_per_attack.grades.json` | DATAMINED / PACK / INFERRED grade for every column |
| `range_audit_per_monster.csv` | 533 records: pack `max_reach_m` vs GD maximum fire range |
| `p05_spawn_activation.csv` | 31 p05 members: reach, spawn animation, `Timeout`/`Delay`/`Range` per special |
| `summary.json` · `ed_diff.json` · `proxyambush.json` · `digests_vendor.json` | counts · IV/II diffs · p05 proxy records · vendor sha256 |
| `evidence/01-13` | disassembly listings (`Game.dll`/`Engine.dll` IV 32-bit) plus the permission-matrix cells |
| `scripts/` | `gdlib.py` (arz reader) → `pack_slots.py` → `gd_ranges.py` → `compare.py` → `carrier.py` → `summary.py` → `build_outputs.py`; `d4b_*`/`e_dis`/`strx`/`dump_evidence` (disassembly). Run from a scratch cwd with `PYTHONDONTWRITEBYTECODE=1` |

**Inputs (sha256):**
- `monster_offense.json` `fad592f5…`
- `waves.json` `38c43a9c…`
- `arena.json` `15078b58…`
- `pm2_tg2_attack_slots.csv` `eb950649…`
- `pm2_tg2_attack_damage.csv` `e250089e…`
- `q91_pool338_attack_slots.csv` `8cccfb20…`
- `q91_pool338_attack_damage.csv` `a6a6a0cf…`
- `threat.py` `4ce434f9…`
- `kc2rt_fight.gd` (vendored copy) `1e60eb15…`
- `kc2play_projection.gd` `9b74f150…`
- `Game.dll` IV `e75925d1…`
- `Engine.dll` IV `f18e8658…`
- the arz set: `digests_vendor.json`

Prior laps relied on: **D-2** (band fields), **D-11** (`ChooseBestSkill` order, `Timeout`), **Lap F** (radii, metre unit), **RESID-D1-2** (permission matrix).

*legolas · KC2-PLAY · KP-194 range audit · 2026-10-01*
