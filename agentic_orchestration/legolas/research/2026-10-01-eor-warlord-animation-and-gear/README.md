# EoR Warlord: gear, animations, timing, VFX

**Date:** 2026-10-01 · **Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf, for the C-9 animation session
**Referent:** `EoRWarlGuts`, grimtools `b28gD0KN`, the KC2 oracle fixture (`player_kit.fixture`)
**Machine-readable:** `packet.json` (41 animation/FX entries, plus `gear_of_record`, `speed_inputs` and `channel_eye_of_reckoning` blocks)
**Access:** read-only throughout. No pack, oracle, C-8, C-9, save or host file was modified. No sealed cell was opened.

**Grades.** DATAMINED: read from GD `.arz`/`.arc` here or in a cited legolas decode. PACK: kc2 pack `v3-E-s09-cp150-mech-v3p7p1-20261001_021247`, with the row id. PACK-SOURCE: the pinned source CSV behind a pack provenance id, but not lifted as a row. SAVE: decoded `player.gdc`. COMMUNITY-VERIFIED: grimtools, confirmed on camera. INFERRED: derived, with the reasoning given. UNKNOWN: not established, with what would settle it.

---

## Summary

1. **He wields a two-handed mace and no shield.** The weapon is Gutsmasher (`melee2h/d107_blunt2h`, Class `WeaponMelee_Mace2h`, a hammer mesh), so his GD animation style is **`mace2h`**. That style uses the **2H-sword clip set** (`hero01_sword2h_*`).
2. **Both existing Warlord renders show the wrong weapon style:** a one-handed spiked mace plus a kite shield. That is a sword-and-board silhouette. Every pose they contain is wrong for the referent.
3. **Eye of Reckoning plays the Spin clips** (`hero01_sword2h_skill_whirlwind_a01start` / `…loop`), a whirlwind. It is not the "channel" clips. The loop is 10 keys at 30 fps, which is **0.300 s per loop**.
4. **The oracle's channel ticks every 1/12.25 s = 0.0816 s.** That is 0.16 s × 100/196 % attack speed. Soulfire orbits on its own 0.2 s clock.
5. **His EoR effect is the RED variant (`pfx_eyeofreckoning_spinredfx_01.pfx`), not the default gold one.** Gutsmasher's EoR modifier swaps it.

---

## A. Gear of record

### Three sources, one answer

| Source | What it says | Status |
|---|---|---|
| **Oracle (pack)** | The pack carries **no per-slot gear list**. `provenance.json` lists `ABS-NOT-RECOVERED-GEAR` (*"the item-by-item basis of those totals is not [recovered]"*). The oracle runs on the aggregate sheet (`PRV-PLAYER-SHEET`). Where a constant needed an item, it cites the item record: `mace2h_d107_eyeofreckoning` (Gutsmasher), `hands_d206_eyeofreckoning` (Sandreaver), `compb_sealannihilation`, `compb_chainsofoleron`, `d007_feet`, `d114_relic`, `d203_rune` (in `input_closure.json` and `player_kit.json`). | Silent per slot, but **consistent with the save everywhere it cites an item** |
| **Save** | `player.gdc`, sha256 `b8e6f510…bfa5`. The file is byte-identical in `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/`, in `/Volumes/reincarnated/GD-matt-test/eor-test-2/save/_EoRWarlGuts/` and in `legolas/scratch/2026-08-05-eorwarlguts-parse/`. It was decoded 2026-08-05 and re-read here. | SAVE |
| **grimtools `b28gD0KN`** | I did not fetch it: grimtools' `robots.txt` blocks ClaudeBot. gandalf compared it on camera (`gandalf/notes/2026-08-05-eor-ceremony-cross-verification.md` §A): **13/13 slots name-identical**. | COMMUNITY-VERIFIED |

**There is no conflict to rule on.** All three agree on every item name. The oracle governs, and the oracle simply does not enumerate the gear. The gaming PC was not reachable read-only from this Mac (no SSH host is configured), and it was not needed: the Mac copies are the PC save.

### By slot (records from Edition IV `.arz`, build 24825149)

| Slot | Item | Record | Armour class / type | Visual mesh |
|---|---|---|---|---|
| **Weapon set 1, main** | **Gutsmasher** (Legendary) | `items/gearweapons/melee2h/d107_blunt2h.dbr` [GDX2] | **WeaponMelee_Mace2h**, `tagAttackSpeedVerySlow` | `items/gearweapons/melee2h/hammer2h_013a_02.msh` |
| Weapon set 1, off-hand | *(empty: two-hander)* | — | — | — |
| Weapon set 2 | *(both slots empty; the swap key is armed)* | — | — | — |
| Head | Warborn Visor + craft `ad201_slowresist` | `items/upgraded/gearhead/d028_head.dbr` | **Heavy** helm, Warborn set | `items/gearhead/head_004a_05.msh` |
| Shoulders | Warborn Pauldrons + craft `ao14_oa` | `items/upgraded/gearshoulders/d026_shoulder.dbr` | **Heavy**, Warborn set | `items/gearshoulders/shoulders_022c_01.msh` |
| Chest | Warborn Chestguard | `items/upgraded/geartorso/d026_torso.dbr` | **Heavy**, Warborn set | `items/geartorso/torso_heavy_002-01b_m.msh` |
| Hands | Sandreaver Bracers | `items/gearhands/d206_hands.dbr` [GDX3] | Light | `items/gearhands/hands_020a_01.msh` |
| Legs | Devastating Solael-Sect Legguards of the Eagle (MI) | `items/gearlegs/b002e_legs.dbr` | Light | `items/gearlegs/legs_001b_03.msh` |
| Feet | Windshear Greaves + craft `ad201_slowresist` | `items/upgraded/gearfeet/d007_feet.dbr` | Light | `items/gearfeet/feet_009a_04.msh` |
| Belt | Gladiator's Distinction | `items/gearaccessories/waist/d108_waist.dbr` | belt | `…/waist/belt.msh` |
| Amulet | Imposing Kaisan's Burning Eye of Alacrity (MI) | `items/gearaccessories/necklaces/b201e_necklace.dbr` | jewellery | — |
| Ring 1 | Combustion Band | `items/gearaccessories/rings/d110_ring.dbr` | jewellery | — |
| Ring 2 | Aggressive Gargabol's Ring of Oleron's Wrath (MI) | `items/gearaccessories/rings/b103e_ring.dbr` | jewellery | — |
| Medal | Imposing Mark of Harvoul of Ruin (MI), augment **Rune of Violent Delights** | `items/gearaccessories/medals/b016e_medal.dbr` + `enchants/runes/d203_rune.dbr` | medal | — |
| Relic | Deathstalker | `items/gearrelic/d114_relic.dbr` | relic | — |

The component and augment for every slot are in `packet.json → gear_of_record.slots`.

**Visual set:** 3-piece Warborn (helm, pauldrons, chest) in heavy plate. The arms and legs are light pieces. So the readable silhouette is a heavy-plate upper body over a lighter lower body, carrying a big two-handed hammer.

**Weapon style:** `mace2h`. Evidence: the item Class is `WeaponMelee_Mace2h` (DATAMINED); the save has the off-hand empty (SAVE); the sheet shows Chance to Block 0 % (ceremony #519); and EoR's `Mace2h=1` makes the skill legal with it. In the PC animation table (`records/creatures/pc/anm_malepc.dbr`; the save header reads `male=1`), every `mace2h*` slot points to the **sword2h** clips. The `mace2h` slots are byte-identical between Edition II and Edition IV.

---

## B. Animations

Clip data comes from the `.anm` census of the Edition III `Creatures.arc` (`legolas/scratch/2026-08-08-kc2-threat-grammar/anm_events.json`; every clip is 30 fps). **The Edition IV pin carries no `.arc` files, and no `Creatures.arc` exists on the Mac today.** So the clip figures are Edition III, and asset parity with Edition IV is UNVERIFIED. The animation *table* is unchanged II → IV.

Duration = (nKeys − 1)/30. That rule is measured: the last key is a loop-closing duplicate (wr3-stage2 §0). nKeys/30 is in the packet as an alternative. **Action** = the `RightHandHit` (or `Hit`) callback frame. "Table speed" = the `…AnimSpeed` field. All three of those are DATAMINED.

| State | `.anm` (all `creatures/pc/anm/…`) | Keys | Native s | Table speed | Action frame → s at table speed | Other callbacks | Existing render |
|---|---|---|---|---|---|---|---|
| Combat idle | `hero01_sword2h_idlecombat_a01` | 61 | 2.000 | 1.0 | — | — | wrong style |
| Long idle | `hero01_sword2h_idle_a01` | 101 | 3.333 | 1.0 | — | — | wrong style |
| Idle fidget | `hero01_sword2h_idle_fidget_a01` | 181 | 6.000 | 1.0 | — | — | **missing** |
| Combat → idle | `hero01_sword2h_idlecombat_trans2idle_a01` | 48 | 1.567 | 1.0 | — | — | **missing** |
| Walk | `hero01_walk_a01` (shared by all styles) | 31 | 1.000 | 1.0 | — | R foot 10, L foot 25 | wrong style |
| Run | `hero01_sword2h_run_a01` | 25 | 0.800 | 1.0 | — | L foot 2, R foot 14 | wrong style |
| Attack A (45 %) | `hero01_sword2h_attack_a01` | 21 | 0.667 | 1.0 | f7 → 0.233 | swipe 4–11, AllowInterrupt 13 | **missing** |
| Attack B (30 %) | `hero01_sword2h_attack_b01` | 21 | 0.667 | 1.0 | f10 → 0.333 | swipe 8–14, AllowInterrupt 16 | **missing** |
| Attack C (25 %) | `hero01_sword2h_attack_c01` | 21 | 0.667 | 1.0 | f7 → 0.233 | swipe 4–11, AllowInterrupt 16 | **missing** |
| Attack, turn L/R 90° | `hero01_sword2h_attackleft90_a01` / `…right90_a01` | 21 | 0.667 | 1.0 | f9 → 0.300 | turn 1–8 | **missing** |
| Get hit | `hero01_sword2h_gethit_a01` | 21 | 0.667 | 1.0 | — | — | **missing** |
| Stun / crit react | `hero01_stunned` | 91 | 3.000 | 1.0 | — | — | **missing** |
| Death | `hero01_death_a` | 91 | 3.000 | 1.0 | — | — | **missing** |
| Respawn | `hero01_getup_faceup` | 91 | 3.000 | 1.0 | — | — | missing (optional) |
| **EoR spin start** | `hero01_sword2h_skill_whirlwind_a01start` [GDX2] | 7 | 0.200 | 1.0 | f6 → 0.200 | — | **missing** (render has only a loop) |
| **EoR spin loop** | `hero01_sword2h_skill_whirlwind_a01loop` [GDX2] | 10 | **0.300** | 1.0 | f8 → 0.267 | MoveStart f0 | ≈ render `attack` (16 frames/direction, 0.40 s, wrong weapon) |
| **War Cry** | `hero01_sword2h_spell_warcry_a01` | 19 | 0.600 | 1.0 | **f11 → 0.367** (shout sound also f11) | swipe 5, AllowInterrupt 14 | **missing** (render `cast` is generic) |
| **Blitz** | `hero01_sword2h_skill_blitz_a01` | 19 | 0.600 | 1.0 | **f4 → 0.133**; the clip spawns `Blitz1_Impact_FX` at f4 | AllowInterrupt 13 | **missing** |
| **Vire's Might** | `hero01_sword2h_skill_rush_a01` [GDX2] | 19 | 0.600 | **1.3** | **f4 → 0.103** | AllowInterrupt 13 | **missing** |
| **Rune of Violent Delights** | same clip as Vire's Might (`Rush`) | 19 | 0.600 | 1.3 | f4 → 0.103 | — | **missing** |
| **Ascension** | `hero01_sword2h_spellbuffself_a01` | 19 | 0.600 | 1.0 | f11 → 0.367 | AllowInterrupt 14 | **missing** |
| Summon Guardian of Empyrion | `hero01_sword2h_skill_summon_a01` [GDX1] | 23 | 0.733 | 1.0 | f15 → 0.500 | AllowInterrupt 20 | **missing** |
| Summon Deathstalker (relic) | **UNKNOWN** slot | — | — | — | — | — | missing |
| Evade (not bound in the kit) | `hero01_sword2h_dodge01` | 29 | 0.933 | 1.3 | Hit f13 → 0.333 | jump 2–13 | missing (optional) |
| Potion | **no body animation** (the table has no potion slot) | — | — | — | — | — | n/a |
| Procs and toggled auras (Menhir's Will, Turtle Shell, Arcane Barrier, Resilience, Fighting Spirit, Divine Mandate, Presence of Virtue, Field Command, the 7 devotion procs) | **FX only**, no body clip (INFERRED: auto-triggered or toggled, no `skillSpecialAnimationName`) | — | — | — | — | — | n/a |

**How each skill's clip was resolved.** For War Cry, Blitz, Vire's Might, the Rune and Summon Guardian, the skill record names a clip (`skillSpecialAnimationName` = Warcry / Blitz / Rush / RaiseDead), which resolves through `mace2hSpecialAnimRef{21,6,39,31}`. That chain is DATAMINED. Three mappings are INFERRED:

- **EoR → Spin**, strong inference. The record has no clip name. Its class `Skill_AttackRadiusSpin` exports `StopSpinning` in Game.dll. The Spin clips are GDX2-tagged, which is EoR's expansion. EoR is the only player Spin skill besides one relic. The skill text reads *"a whirlwind of fire and light"*.
- **Ascension → BuffSelf**, by its class name.
- The `Channel*` slots (`hero01_sword1h_spellattackchanneled_*`) are listed in the packet **only so that nobody uses them for EoR**. They belong to beam channels.

**The existing render covers:** idle, walk, run, attack (an EoR stand-in), cast (generic) and jump. All of them use the wrong weapon style.

**It lacks:** combat idle as a separate state, the idle transition, fidget, the 3-swing attack chain plus the turn-attacks, get-hit, stun, death, the EoR spin-start, and dedicated War Cry, Blitz, Vire's Might/Rune, Ascension and Summon clips. The generic `cast` stands in for four different GD clips with different release frames (f4, f4, f11, f11, f15).

**It has one state the referent never uses:** `jump`. The player has no jump in this kit.

### Speed laws

Speed inputs:

| Input | Value | Grade |
|---|---|---|
| Attack speed | 196 % | PACK, `player_kit.channel.attack_speed_pct` |
| Cast speed | 184 % | PACK-SOURCE, `pm2_measured_player_sheet.csv` |
| Attacks per second | 2.66 | PACK-SOURCE |
| Weapon attacks per second | 1.46 | PACK-SOURCE |
| Run speed | 135 % | PACK-SOURCE; at the cap `playerRunSpeedCapMax` 135, DATAMINED |
| Attack-speed cap | 200 | DATAMINED |
| PC base attack and cast speed | 1.25 | DATAMINED, `malepc01.dbr` |
| Gutsmasher base attack speed | −0.18 (VerySlow) | DATAMINED |

1. **EoR damage and drain tick, which the oracle governs.** `tick = 0.16 s × 100/AS% = 0.0816327 s` (12.25 Hz).
   - PACK: `rng_contract.tick.tick_period_s`, `PRV-MPOL2-SEAL`; `math_rules` RULE-RELEASE-TYPE-A/B test vectors; `V15-1` (16.0 × 12.25 × 0.90 = 176.4); KP-68 (first post-tick sample at t = 0.0816 s).
   - DB: `timeBetweenAttacks = 200`, and the in-game text says *"every 0.16s at 100% Attack Speed"*.
   - The ×0.8 conversion holds on 9 channel skills (PE-1 §1.3); why it holds is UNKNOWN.
   - The inverse-proportional form is INFERRED (strong), and it reproduces the pack value exactly.
   - *Contradiction on file:* `2026-08-12-whirlwind-rev-rate-probe.md` treated 200 ms as the 100 % period. The pack does not. **The oracle uses 0.16-based 12.25 Hz.**
2. **Weapon swings: INFERRED, two candidate laws that disagree by about 10 %.**
   - Law A stretches the clip to the attack period 1/APS: **0.376 s per swing**, with the hit at 0.132 s (A, C) or 0.188 s (B).
   - Law B plays the clip ×1.96: 0.340 s, with the hit at 0.119 / 0.170 s.
   - Settle by frame-counting one referent swing.
3. **Skills tagged with attack speed** (`characterBaseAttackSpeedTag`: Blitz, Vire's Might, Rune, Ascension): INFERRED playback ×1.96 on top of the table speed.
   - Blitz: 0.306 s, strike at 0.068 s.
   - Vire's Might / Rune: 0.235 s, strike at 0.052 s.
   - Ascension: 0.306 s, release at 0.187 s.
4. **Skills without the tag** (War Cry, Summon Guardian): INFERRED playback ×1.84 cast speed.
   - War Cry: 0.326 s, shout at 0.199 s.
   - Summon: 0.399 s, release at 0.272 s.
5. **Run:** INFERRED playback ×1.35, giving a 0.593 s cycle.
6. **Spin clip vs attack speed: UNKNOWN.**
   - Unscaled, the loop is 0.300 s, which is 3.675 damage ticks per loop.
   - At ×1.96 it is 0.153 s, which is 1.875 ticks per loop.
   - Damage is not driven by the clip's `RightHandHit` (INFERRED from the class).
7. Idle, get-hit, stun and death: unscaled (INFERRED).

### The channel: Eye of Reckoning

| Item | Value | Grade / row |
|---|---|---|
| Body clips | spin start 0.200 s (once), then spin loop 0.300 s (repeating). There is **no spin-end clip** in the table. | DATAMINED; slot mapping INFERRED (strong) |
| Tick cadence | 0.0816327 s (12.25 Hz); 176.4 energy/s drained per tick | PACK, `rng_contract.tick`, V15-1 |
| Release tail | ≤ 0.25 s | PACK `channel.channel_tail_s` + DATAMINED `duration=0.25`, `useResetsDuration=1` |
| Radius | 3.0 m true disc, no target cap | PACK `channel.radius_m`, V17-HITTEST-1 |
| Turn rate | ×0.35 while channelling | PACK + DATAMINED |
| Movement | **allowed** while channelling (`canUseWhileMoving=1`, `delayMovement=1`; MoveStart callback at loop f0) | DATAMINED |
| Rank | 15 allocated / 26 total | PACK `channel.rank`, `fixture.eor_rank_total` |
| Soulfire | orbiting projectile, period 0.2 s, CCW, starts at the front, 0.2 m burst, 100 % pierce, projectile duration 2.6 s | DATAMINED + PACK `channel.soulfire`, V15-8 |
| Effect | **`pfx_eyeofreckoning_spinredfx_01.pfx`** (red), via `fxChanges` on Gutsmasher's `mace2h_d107_eyeofreckoning` modifier. The base skill's default would be `pfx_eyeofreckoning_spinfx_01.pfx`. | DATAMINED; the replacement behaviour is INFERRED |
| Sound | `spak_eyeofreckoning_loop` (loop), `spak_eyeofreckoning_hit` (per hit) | DATAMINED |

The particle timing inside each `.pfx` lives in `FX.arc`, which is not on the Mac: UNKNOWN.

### VFX hooks per skill (record → particle file)

| Skill | FX records → `.pfx` (all `fx/particlesystems/…`) |
|---|---|
| EoR | `skillclass09/eyeofreckoning_spinredfx01` → `skillsclass09/pfx_eyeofreckoning_spinredfx_01.pfx` (cast aura, of record) |
| Soulfire | `eyeofreckoning_projectileorbitalfx01` → `pfx_eyeofreckoning_flight.pfx`, impact `pfx_eyeofreckoning_impact.pfx` |
| War Cry | `warcry4_radius_fxpak01` → `skillsclass01/pfx_warcry04.pfx` (rank-indexed; total rank 16; camera shake 0.1 s; disturbance radius 14). On-target: `weaponpool01_fxpak` → `pfx_brutalimpact01.pfx` |
| Blitz | warm-up loop `blitz1_warmuploop.pfx` (Upper Body); impact `blitz1_impact.pfx`, spawned by the clip at f4; on-target `pfx_brutalimpact01.pfx` (camera shake 0.5 s) |
| Vire's Might | warm-up `pfx_viremight_warmup_01.pfx` (Upper Body); impact `pfx_viremight_impact_01.pfx` (shake 0.2 s); hit `pfx_viremight_hit_02.pfx`; Volcanic Stride trail `pfx_viremight_firetrail_01.pfx` (4 s) |
| Rune of Violent Delights | `itemrunes/pfx_rush_warmup_vitality_01.pfx`, `pfx_rush_impact_vitality_01.pfx`, `pfx_rush_hit_vitality_01.pfx` |
| Ascension | `pfx_ascension_selfloop_01.pfx` (FXUnParentedCenter, 10 s) |
| Summon Deathstalker | `pfx_summon_generic_01.pfx` |
| Menhir's Will | `pfx_willtolive1_loop.pfx` (10 s) |
| Turtle Shell / Arcane Barrier | `turtle_shield_loop02.pfx` / `crab_shield_loop03.pfx` |
| Resilience / Fighting Spirit | `pfx_resilience_01.pfx` / `pfx_fightingspirit02.pfx` |
| Divine Mandate / Presence of Virtue / Field Command (persistent) | `pfx_divinemandate_01.pfx` / `pfx_presenceofvirtue_selfloop_01.pfx` + `…otherloop_01.pfx` / `pfx_fieldcommand1_loop.pfx` |
| Assassin's Mark / Maul / Tip the Scales / Shifting Sands (devotion procs) | `assassinmark_loop01.pfx` / `direbear_maul01.pfx` / `scalesofulcama_cast01.pfx` / `pfx_azrakaasands01_projectile.pfx` |

---

## C. Render mismatches

C-8 is `runs/C-8/cliffside_v40-warlord5`. C-6 is `runs/C-6/cliffside_v40-warlord8`, which has idle and walk only and an empty `exporter.json`.

| # | Mismatch | Severity |
|---|---|---|
| M1 | **Weapon style.** Both renders show a **one-handed spiked mace in the right hand and a large kite shield in the left**. The referent wields a **two-handed hammer** (Gutsmasher) with **no shield**: block is 0 % on the sheet and the off-hand is empty in the save. Every pose is a sword-and-board pose, not the `sword2h` stance GD uses for `mace2h`. | **Blocking** for "to spec" |
| M2 | **Armour read.** The render is full heavy plate head to toe. The referent's heavy pieces are only the 3-piece Warborn set (helm, pauldrons, chest); bracers, legguards and greaves are light. | Minor / art-direction |
| M3 | **EoR loop.** The render `attack` loops in 0.40 s (`whirlwind_fit.json loop_seconds`). GD's spin loop is 0.300 s unscaled. There is no start clip. | Moderate |
| M4 | **EoR movement.** C-8's proof requires *"the figure does not move while attacking."* GD's EoR is channel-while-moving: `canUseWhileMoving=1`, plus a MoveStart callback. | Moderate (behaviour) |
| M5 | **EoR colour.** The of-record effect is the **red** spin (`spinredfx`), via Gutsmasher. | Moderate (VFX) |
| M6 | **Generic `cast`.** It stands in for War Cry, Ascension, Summon and the charge skills, which have distinct clips and release frames. Its release model is a staff tip; the referent has no staff. | Moderate |
| M7 | **`jump`** is not in the referent kit. | Minor |
| M8 | **Missing states:** the attack chain, get-hit, death, Blitz/Vire's Might dash-strikes, and spin-start (table in B). | Coverage |

---

## Open questions

1. **Spin vs attack speed.** Does the whirlwind clip play faster with attack speed (0.300 vs 0.153 s per loop)? How many degrees does one loop turn: one revolution? The root-bone yaw is in the `.anm`, but the clip is not on the Mac. *Settle:* re-pin `Creatures.arc` (a Matt-only Steam depot pull; the parser exists at `legolas/scratch/2026-07-30-wr3-stage2/a4_parse.py`), or frame-count the referent footage.
2. **Weapon-swing law A vs B** (0.376 vs 0.340 s). The APS arithmetic does not close either: 2.66/1.96 = 1.357 base, against 1.46 on the weapon tooltip and 1.25 − 0.18 in the DB. *Settle:* one footage swing.
3. **Summon Deathstalker's clip slot.** `Skill_SpawnPet` names none. *Settle:* footage, or the Game.dll class-to-slot code.
4. **Edition IV asset parity.** The clip figures are Edition III `Creatures.arc`. The census also keeps base over expansion for same-named clips. *Settle:* the same depot pull.
5. **War Cry radius (presentation only).** The pack's `V13-WARCRY-1` has `skill_target_radius_m 16.0` (= rank 12, index 11) next to `reduction_pct 29.0` (= rank 16, index 15). At total rank 16 the DB radius is 16.8 m. That is not mine to rule; it is flagged for the ring's VFX scale.
6. **Coincidence, not adjudicated.** The pack's cast-linked channel release (`RULE-RELEASE-TYPE-B`, median 0.6 s / 0.59375 s) equals the unscaled length of the Blitz, War Cry and Rush clips (18 intervals / 30 = 0.600 s). If it is causal, those clips play **unscaled**, and laws 3 and 4 above would be wrong.
7. **When GD plays the walk clip** for the player is not in data.

---

## Sources

- **Pack:** `reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/{player_kit,provenance,config_of_record,math_rules,rng_contract,input_closure,input_closure_v3p7p1}.json`
- **GD DB:** `~/Games/vendor/grim-dawn-edition-IV-20260929/` (build 24825149): `anm_malepc.dbr`, `malepc01.dbr`, `gameengine.dbr`, the skill, item and FX records named above. Edition II `~/depots/*/24346246/` was used for the drift check and Text_EN.
- **Clip census:** `agentic_orchestration/legolas/scratch/2026-08-08-kc2-threat-grammar/anm_events.json`. Format: `legolas/research/2026-07-30-wr3-stage2-referent-extraction.md` §0.
- **Prior decodes:**
  - `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` (§3 gear, C-2 rank attribution)
  - `legolas/notes/2026-08-07-pe1-eor-spin-parameters.md`
  - `legolas/notes/2026-08-12-whirlwind-rev-rate-probe.md`
  - `legolas/notes/2026-08-01-eor-endgame-build-of-record.md`
  - `research/knowledge/gd/2026-08-23-eorwarlguts-save-decode.md` (hotbar)
  - `gandalf/notes/2026-08-05-eor-ceremony-cross-verification.md`
  - `reincarnated-engine/data/kc2/pm2_measured_player_sheet.csv`
- **Renders:** `astra_test_01/burst/runs/C-8/cliffside_v40-warlord5/godot/{sprites,exporter.json,whirlwind_fit.json,probe_attack_c8.gd}` and `runs/C-6/cliffside_v40-warlord8/godot/sprites`. Viewed, not modified.
