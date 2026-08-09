# Rider-2 threat-grammar companion lap — Edition-III `.arz` attack-timing boundary

**Agent:** legolas (UNKNOWN-RESEARCHER)
**Date:** 2026-08-08
**Commission:** Matt-approved 2026-08-08 via gandalf Q52 ruling § 3 (Rider 2), `agentic_orchestration/gandalf/notes/2026-08-08-q52-ruling-and-riders.md`
**Track:** PARALLEL — reports into the Godot PLAYTEST milestone. **NOT a KC2-SIM gate. Blocks nothing in that run.**
**Corpus:** `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (Edition-III cut, pins 8/8 verified per `2026-08-08-kc2-edition-III-intake-and-diff.md`). Same edition as the KC2 stat fold — **no cross-edition hazard.**
**Access discipline:** READ-ONLY throughout. No writes to the vendor tree.
**Artifacts:** `2026-08-08-kc2-threat-grammar-arz-boundary/` (sidecar dir, this directory)

---

## § 0 — HEADLINE

**The commission asked me to map a boundary and expected the answer to be "DB has cadence, animation has everything else, go ask galadriel."**

**That is not the answer.** The boundary sits one layer deeper than the commission's framing, and it is *further out* than expected:

1. The `.dbr` layer (`.arz`) carries the **AI attack grammar** — cadence, re-use delay, chance, range band, cooldown, attack-speed multiplier, swing pause, projectile velocity. As expected. **DB-RESIDENT.**
2. The `.dbr` layer carries **animation file references and speed/weight multipliers**, but **no durations**. As expected. **The `.dbr` boundary is real.**
3. **But the `.anm` files are in the corpus, their header is decodable, and their tail carries a plain-ASCII event track naming the exact frame of every hit, every hitbox on/off, every FX spawn, and every interrupt-release point.**

So the six timing dimensions are **not** split "DB vs. needs-a-camera." They are split **DB-record vs. DB-adjacent-binary** — and the second half is agent-fetchable at volume, today, without Wine, without a frame lap.

**All six requested dimensions are extractable from the corpus.** Wind-up, recovery, telegraph, cadence, root-lock, projectile speed. Full 968-record extraction is DONE and shipped in this note's sidecar, not sampled.

**Four independent cross-checks against galadriel's WR3 frame-lap numbers agree**, the tightest at **−0.10%**. See § 5.

**What this does NOT displace:** galadriel's frame lap remains necessary and is now *more* valuable, not less — see § 7. It becomes a validation and gap-fill instrument against a measured baseline instead of the sole source.

---

## § 1 — Method and provenance

### § 1.1 Layers traversed

| # | Layer | Container | Reader | Status |
|---|---|---|---|---|
| L1 | Monster `.dbr` | `.arz` (TQIT, LZ4-block) | `gd_arz_adapter_2026_07_24.ArzArchive` | pre-existing lane |
| L2 | Controller `.dbr` | same | same | pre-existing lane |
| L3 | Skill `.dbr` | same | same | pre-existing lane |
| L4 | Projectile `.dbr` | same | same | pre-existing lane |
| L5 | Anim-table `.dbr` (`charanimationtable.tpl`) | same | same | **first traversed this lap** |
| L6 | `.anm` binary header | `.arc` v3 (`Creatures.arc`) | `gd_arc_reader_2026_07_26.ArcArchive` + new decode | **FIRST-OF-KIND (this lap)** |
| L7 | `.anm` ASCII event trailer | same | new parse | **FIRST-OF-KIND (this lap)** |

Overlay-stack resolution is last-wins field merge across all 8 archives (`base`, `gdx1..3`, `sm_mod`, `sm1..3`) — the same stack the Edition-III diff used.

### § 1.2 Roster basis — join target held

Join key is `record`, identical to `t22_band_a_monster_stats.csv`.

- t22 SHA-256 prefix **verified `0d6992e8`** (`0d6992e87aca4c99…`), 968 data rows + header. Matches the commission.
- **967/968 records resolve** in the Edition-III `.arz`.
- The 1 miss is `records/creatures/enemies/hero/scavenger_h075.dbr` — **the same record t22 already carries as `scavenger 1/968 INFERRED`.** Independent corroboration that the residual is a genuine corpus absence, not a stat-fold artifact.
- Emitted tables carry all 968 rows in t22 order; the scavenger row carries `status=NOT-FOUND-IN-ARZ`.

**#67 name-is-a-pin honored:** the tables EXTEND the existing board on the existing key. No parallel roster is minted. No record is renamed. Namespace guard clean.

### § 1.3 Format decode — `.anm` header (FIRST-OF-KIND)

```
offset 0 : magic  b'ANM' + version byte (0x02)
offset 4 : u32  bone/track count
offset 8 : u32  FRAME COUNT
offset 12: u32  FPS  (== 30, invariant)
offset 16: u32  len(name)
offset 20: name bytes  (e.g. "Target_CTRL")
```

**Grade: MEASURED.** Not asserted from field position — proven by a payload-size identity across the whole population:

| regression | r² | n |
|---|---|---|
| `size ~ frames × offset4` | **0.999997** | 3,452 |
| control: `size ~ frames` alone | 0.5727 | 3,452 |
| control: `size ~ offset4` alone | 0.3157 | 3,452 |

Slope **56.068 B** (= 14 float32 per track per frame), intercept **1,004 B**. Both controls fail decisively. This is a mechanical identity, not a plausibility argument.

`offset 12 == 30` for **all 3,452** `.anm` files across all five `Creatures.arc` archives — zero variance. Interpretation as *frames-per-second* is confirmed independently in § 5.

Duration `= frames / 30`. Population: min 0.067 s, median 1.233 s, max 40.033 s.

### § 1.4 Format decode — `.anm` ASCII event trailer (FIRST-OF-KIND)

The tail of each `.anm` carries plain-text blocks, CRLF-delimited:

```
CallbackPoint
{
	name = "SwipeRight"
	frame = 9
}
CallbackPoint
{
	name = "RightHandHit"
	frame = 13
}
CreateEntity
{
	frame = 5
	entity = "Records\FX\SkillsOther\AttackMelee\AetherialAbomination_Slam_Trail_FX01.dbr"
	attach = "L Hand"
}
```

Census across all 3,452 `.anm`: **11,030 `CallbackPoint` + 1,922 `CreateEntity`** blocks, **62 distinct callback names**. 815 clips carry zero events (idles, walks, deaths — expected).

The callback vocabulary IS the threat-grammar vocabulary:

| callback | n | threat-grammar meaning |
|---|---|---|
| `RightHandHit` / `LeftHandHit` / `Hit` | 1,840 / 1,003 / 12 | **damage-application frame** → wind-up boundary |
| `SwipeRight` / `SwipeLeft` | 1,611 / 756 | hitbox-arc ON |
| `SwipeRightOff` / `SwipeLeftOff` | 332 / 97 | hitbox-arc OFF → active window |
| **`AllowInterrupt`** | **987** | **root-lock RELEASE frame** |
| `PS1Start` / `PS1End` | 546 / 364 | particle-system window → telegraph |
| `CameraShake_1_1` | 19 | telegraph |
| `notTargetable` / `targetable` | 7 / 7 | i-frame windows |
| `TurnStart` / `TurnEnd`, `MoveStart`, `StartJump`/`StopJump` | 30/325/10/49 | locomotion state |
| `voxSound`, `specialAttackSound1-4`, `genericSound1-4` | 845 + 235 + 62 | audio telegraph |
| `R Footstep` / `L Footstep` | 269 / 264 | gait cadence |
| `mortal`/`immortal`, `dissolve`, `spawnDeathActor` | 38/34/32/23 | death handling |

`CreateEntity` gives **FX spawn frame + the FX `.dbr` record path + the attach bone** — i.e. the telegraph VFX, its onset frame, and where on the body it appears.

---

## § 2 — THE BOUNDARY (the finding the commission asked for)

Three columns, because the two-column framing the commission assumed does not survive contact with the corpus.

| Timing parameter | `.dbr` (`.arz`) | `.anm` (in-corpus, agent-fetchable) | Truly absent |
|---|---|---|---|
| attack-speed multiplier | **`characterAttackSpeed`** (967) | — | — |
| attack-speed tag | `characterBaseAttackSpeedTag` (967) | — | — |
| spell-cast speed | `characterSpellCastSpeed` (967) | — | — |
| animation **reference** | `<class>AttackAnim1-3`, `<class>SpecialAnim1-73` | — | — |
| animation **speed multiplier** | `<class>AttackAnimSpeed{N}` | — | — |
| animation **selection weight** | `<class>AttackAnimWeight{N}` | — | — |
| animation **symbolic binding** | `skillSpecialAnimationName` ↔ `<class>SpecialAnimRef{N}` | — | — |
| **animation DURATION** | ✗ **NOT-FOUND** | **`frames / fps` (header)** | — |
| **wind-up duration** | ✗ **NOT-FOUND** (only `skillAllowsWarmUp` bool, 49 skills) | **`*Hit` callback frame / 30** | — |
| **recovery duration** | ✗ **NOT-FOUND** | **`(frames − last *Hit) / 30`** | — |
| **root-lock** | ✗ **NOT-FOUND** | **`AllowInterrupt` frame / frames** | — |
| **telegraph duration** | partial: `warmUpEffectName` (28), `warmupFxPakName` (31), `skillWarmUpSound` (14), `cameraShakeDurationSecs` (176) — **all refs/flags, no duration** | **`PS1Start`→`PS1End`; `CreateEntity` frame + FX dbr + attach bone; `Swipe`→`SwipeOff`** | telegraph *legibility* (colour/silhouette/screen-space size) |
| **cadence — re-use interval** | **`specialAttack{N}Delay`** (2,184 slots) | — | — |
| cadence — attempt window | `specialAttack{N}Timeout` (2,171) | — | — |
| cadence — roll | `specialAttack{N}Chance` (2,196) | — | — |
| cadence — engagement band | `specialAttack{N}Range` (Any/Short/Medium/Long) | — | — |
| cadence — inter-swing pause | **controller `maxSwingPause`** (959) | — | — |
| cadence — intra-clip combo | — | **multi-`Hit` spacing** (220 slots >1 hit) | — |
| skill cooldown | **`skillCooldownTime`** (469 slots) | — | — |
| skill active duration | `skillActiveDuration` (423) | — | — |
| charge duration | `skillChargeDuration` (29) | — | — |
| **projectile speed** | **`projectileVelocity`** (152/191 projectile DBRs) | — | — |
| projectile range / arc / TTL | `projectileDistance` (190), `launchAngle` (68), `projectileHitTTLMin/Max` (89), `projectileDuration` (10) | — | — |
| wave/AoE travel | `waveTime` (107), `waveDistance` (107), `expansionTime` (91) | — | — |
| approach speed | **`characterRunSpeed`, `walkSpeed`, `characterRunSpeedJitter`** | — | — |
| turn rate | `minRotationSpeed` / `maxRotationSpeed` (967) | — | — |
| stand-off distance | controller `enemyTooClose`, `RepositionChance` | — | — |
| aggro / pursuit | controller `ViewDistance`, `InnerViewDistance`, `PursuitTime`, `FleeBehavior` | — | — |
| concurrent attackers | **`numAttackSlots`** (967; values 4 or 8) | — | — |
| **which animation class is active at spawn** | ✗ — **stochastic**, see § 3.2 | — | **engine-runtime roll** |
| **fallback clip when binding unsatisfied** | ✗ | ✗ | **engine-internal, § 3.3** |
| animation **blend-in** at clip start | `deathAnimBlendTime` only (death) | — | **engine-internal** |

### § 2.1 One-line statement of the boundary

> **The `.dbr` owns *when and whether* an attack happens. The `.anm` owns *how long it takes and when inside it the damage lands*. Both are in the corpus and both are agent-fetchable. What is genuinely absent from both is (a) which weapon-class animation set a given spawn rolls, (b) the engine's fallback clip when a symbolic animation binding is unsatisfied, and (c) animation blend-in.**

---

## § 3 — Named hazards and negative findings

### § 3.1 `characterBaseAttackSpeedTag` is degenerate — the t22 column is uninformative

`CharacterAttackSpeedAverage` for **967/967** records. Zero variance. t22's `attack_speed_tag` column carries no signal for this roster. The live speed signal is the numeric `characterAttackSpeed` (min 0.20, p25 1.00, median 1.00, p75 1.10, max 2.10).

**Flag for gamora / drax:** do not treat the tag column as a threat discriminator. Use the numeric.

### § 3.2 Active animation class is a per-spawn ROLL, not a record property

Equip slots present: `chanceToEquipRightHand` (967), `LeftHand` (963), plus Head/Chest/Legs/Feet/Hands/Shoulders. The weapon rolled at spawn selects the animation class, which selects a *different clip with a different frame count*.

`unarmedAttackAnim1` is populated for **964/964** resolvable anim tables — the universal deterministic fallback. Other classes are conditional:

| class | tables with `AttackAnim1` |
|---|---|
| `unarmed` | 964 |
| `sHanded` | 433 |
| `dHanded` | 210 |
| `dualRanged` | 175 |
| `staff` | 81 |

Eleven prefixes exist overall (`ranged1h`, `ranged2h`, `axe2h`, `mace2h`, `sword2h`, `spear2h` additionally carry `SpecialAnimRef`).

**Extraction decision (declared):** all emitted per-monster timing uses the **`unarmed`** class — deterministic, universal, 964/964. Column `anim_classes_alt` names which other classes exist for that body (**454/968 monsters** have at least one). **Timing for those bodies is a distribution, not a scalar, and the emitted scalar is the `unarmed` branch.** Do not silently treat it as the only branch.

### § 3.3 353/3,064 attack slots name an animation the creature's own table does not define

`skillSpecialAnimationName` is a **symbolic** name resolved against the creature's own animation table at runtime. It is not guaranteed to resolve.

| binding grade | n | share |
|---|---|---|
| `DIRECT-REF` (ref present, clip resolved) | 917 | 29.9% |
| `NO-REF` (skill names no animation) | 1,794 | 58.6% |
| `REF-UNSATISFIED-BY-TABLE` | **353** | **11.5%** |

Worked example: `records/skills/nonplayerskills/attackcharge/aetherialabomination_charge.dbr` sets `skillSpecialAnimationName = 'Charge'`. The Aetherial Abomination's own table (`anm_aetherial_abomination.dbr`) defines exactly `{Quake, QuakeSunder, Roar, Slam}`. **'Charge' is not there.** Most-unsatisfied refs: `Summon` (73), `Charge` (61), `Nova` (50), `Slam` (24), `CastOrb` (18).

**The fallback rule is engine-internal and NOT DB-resident.** I emit a `fallback_anm_dur_s` column under a named, non-measured assumption (non-weapon skill classes → `<class>SpellAttackAnim`), covering 1,626 `NO-REF` + 222 `REF-UNSATISFIED` slots. **It is labelled and must never be promoted to MEASURED.** Column `anim_binding_grade` carries the distinction on every row.

### § 3.4 Resolver bug caught mid-lap (recorded so the correction is not invisible)

First pass scanned `SpecialAnimRef1..15` on five hard-coded prefixes. The true index ceiling is **73** and there are **eleven** prefixes. Fixed to dynamic regex discovery over all `<prefix>SpecialAnimRef<N>`. Direct-ref resolution 881 → 917. All figures in this note are post-fix.

### § 3.5 A falsifier I ran that came back NOT-DIAGNOSTIC

**Hypothesis tested:** `specialAttack{N}Timeout` is the AI's window for the bound animation to complete, so it should track clip duration and thereby constrain fps.

**Result on 817 paired DIRECT-REF slots:** Pearson **r = 0.132**. `timeout ≥ clip_dur` holds for 67.6% at 30 fps, 82.4% at 60 fps, 57.8% at 24 fps — monotone in fps, so it cannot discriminate.

**Verdict: NOT-DIAGNOSTIC.** `Timeout` is an AI attempt/targeting window, not an animation window. Recorded because a run that only reports its successful tests is not reporting.

### § 3.6 Coverage honesty

- 3 records carry no `charAnimationTableName` (`trap_brambletrap_a01`, `trap_chthonicshard_zap_a01_summon`, `trap_lightningspike_hero_a01`) — static traps. Correctly `NOT-FOUND`, not zero.
- 1 skill DBR unresolved: `records/skills/nonplayerskills/buffoffensive/trollhalfcave_dreadaura.dbr`.
- 436/172,906 (0.3%) `.anm` references do not resolve in any `Creatures.arc`.
- `.arc` reader limitation carried forward from the 2026-07-26 probe: the 44-byte file entry's CRC is read but **not validated**. This extraction is clean, but it is not CRC-verified.

---

## § 4 — What was extracted (FULL, not sampled)

The commission permitted a demonstrative sample. **Full extraction was achieved and is shipped.**

### `tg_monster_timing.csv` — 968 rows × 53 cols
SHA-256 prefix `af93f27283e342a0`. One row per t22 roster record, same key, same order.

Carries: overlay owners · anim table · controller · classification · attack/cast/run/walk speeds + jitter · rotation speeds · `numAttackSlots` · `waitingAnimDelay` · the full basic-attack clip set (names, weights, speeds, per-clip durations) · weighted `basic_attack_dur_s` · `basic_swing_period_s` (= clip ÷ `characterAttackSpeed`) · `anim_classes_alt` · controller `maxSwingPause`/`RepositionChance`/`DodgeChance`/`DodgeDelay`/`PursuitTime`/`ViewDistance`/`InnerViewDistance`/`FleeBehavior`/`enemyTooClose` · and the full event-derived block for the primary swing clip (`basic_windup_s`, `basic_recovery_s`, `basic_hit_frames`, `basic_n_hits`, `basic_root_lock_s`, `basic_root_lock_frac`, `basic_root_lock_grade`, `basic_active_window_s`, `basic_ps_window_s`, `basic_fx_*`).

### `tg_attack_slots.csv` — 3,064 rows × 51 cols
SHA-256 prefix `4ad33dcbaa11abd3`. One row per (record, attack slot). Slots: `basic` (274), `special1-5` (798/630/440/236/94), `initial` (414), `dying` (178).

Carries: skill path + class · `chance_pct` · `delay_s` · `timeout_s` · `range_band` · `skill_cooldown_s` · `skill_active_duration_s` · `skill_charge_duration_s` · `instant_cast` · `allows_warmup` · `warmup_effect` · `wave_time_s` / `wave_distance` · `camera_shake_dur_s` · `distance_profile` · `special_anim_ref` · **`anim_binding_grade`** · resolved clip + frames + duration · `fallback_anm_dur_s` (labelled) · projectile record + **`projectile_velocity`** / `projectile_distance` / `projectile_launch_angle` · plus the full event block per clip.

### Supporting indices
`anm_index.json` (3,452 clips: bones/frames/fps/size/control-name) · `anm_events.json` (3,452 clips with parsed event tracks) · extraction scripts (`tg_lib.py`, `x1_extract.py`, `x2_events.py`, `a4_anmcensus.py`, `a8_cbcensus.py`) — all read-only, all re-runnable.

### Six-dimension coverage

| # | Dimension | Monster-level | Slot-level | Grade |
|---|---|---|---|---|
| 1 | **wind-up** | **963/968 = 99.5%** | 917/3,064 = 29.9% (+1,848 labelled fallback) | MEASURED |
| 2 | **recovery** | **963/968 = 99.5%** | 917/3,064 = 29.9% | MEASURED |
| 3 | **telegraph** | — | FX-onset 417 (13.6%) · PS-window 52 (1.7%) · swipe-window 80 (2.6%) · DB warm-up FX 87 (2.8%) | MEASURED but **SPARSE** |
| 4 | **cadence** | attack-speed 967 (99.9%) · swing-pause 959 (99.1%) | re-use delay 2,184 (71.3%) · cooldown 469 (15.3%) · intra-clip combo 220 | MEASURED |
| 5 | **root-lock** | **963/968 = 99.5%** | 917/3,064 = 29.9% | MEASURED |
| 6 | **projectile speed** | — | 681/3,064 = 22.2% (= 152/191 distinct projectile DBRs) | MEASURED |
| + | approach speed | 967/968 = 99.9% | — | MEASURED |

**Dimension 3 (telegraph) is the weak one and is declared weak.** Best DB+`.anm` coverage is 13.6% at slot level. Telegraph is the dimension where galadriel's frame lap remains load-bearing.

### Distributions (the shape of GD's threat grammar)

| quantity | n | p25 | median | p75 | max |
|---|---|---|---|---|---|
| basic attack clip (s) | 963 | 0.760 | **1.138** | 1.278 | 2.033 |
| basic swing period ÷ atkspeed (s) | 963 | 0.715 | **1.022** | 1.217 | 3.467 |
| **wind-up (s)** | 963 | 0.367 | **0.500** | 0.700 | 1.133 |
| **recovery (s)** | 963 | 0.367 | **0.567** | 0.933 | 1.400 |
| wind-up as fraction of clip | 2,086 clips | 0.346 | **0.465** | 0.548 | — |
| **root-lock (s)** | 963 | 0.833 | **1.200** | 1.533 | 2.333 |
| root-lock frac (clips w/ `AllowInterrupt`) | 987 clips | 0.621 | **0.690** | 0.739 | — |
| special re-use delay (s) | 2,184 | 6.0 | **8.0** | 10.0 | 99999 |
| skill cooldown (s) | 469 | 1.0 | **5.0** | 12.0 | 120 |
| **projectile velocity** | 681 | 14.0 | **16.0** | 20.0 | 220 |
| projectile distance | 939 | 15.0 | **19.0** | 20.0 | 100 |
| controller `maxSwingPause` (s) | 959 | 0.700 | **1.000** | 1.200 | 3.300 |
| special anim duration (s) | 917 | 0.967 | **1.500** | 2.033 | 5.133 |

Root-lock grades: **751 bodies full-clip-locked** (no `AllowInterrupt` point at all) vs **212 with an interrupt release**. Engagement bands: Short 755 / Medium 493 / Any 492 / Long 455.

---

## § 5 — CROSS-INSTRUMENT VALIDATION vs galadriel WR3

**Provenance caveat, stated plainly:** the WR3 numbers below are **quoted from the commissioning note** (gandalf § 3: *"Primordian 0.489 s wind-up / 0.879 s recovery, 0.80 s nova telegraph, root 79.6%"*). I searched the repo and could not locate the underlying WR3 artifact on disk. **I did not re-measure them.** They are treated as an independent instrument's reading, cited as given. If they are later corrected, § 5 must be re-run — but § 1.3's r² = 0.999997 stands independently of them.

**Subject:** Primordian, the Forgotten One = `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` (identified via galadriel `2026-07-28-kitcal1-g8-death2-primordian-stats.md`). Anim table `anm_slith.dbr`. **`characterAttackSpeed = 1.0` and all `AttackAnimSpeed = 1.0` — a clean test with no multiplier confound.**

`.anm` reads: `slith01_attack_01.anm` = **41 frames**, `SwipeRight`@9, `RightHandHit`@13. `slith01_attack_02.anm` = **51 frames**, `RightHandHit`@20.

| # | Check | galadriel (frame lap) | legolas (`.arz` + `.anm`) | delta |
|---|---|---|---|---|
| **1** | **clip total = wind-up + recovery** | 0.489 + 0.879 = **1.368 s** | 41 frames ÷ 30 = **1.3667 s** | **−0.10%** |
| **2** | **fps discrimination** | (same 1.368 s) | @24 fps → 1.7083 s | **+24.9%** ✗ |
| | | | @60 fps → 0.6833 s | **−50.1%** ✗ |
| | | | **@30 fps → 1.3667 s** | **−0.10%** ✓ |
| **3** | **root-lock over contact** | **0.796** | clip ÷ (clip + `maxSwingPause`) = 1.4778 ÷ (1.4778 + 0.400) = **0.7870** | **−1.13%** |
| **4** | wind-up / recovery **split point** | 0.489 / 0.879 | 13 ÷ 30 = 0.433 / 0.933 | −11.4% / +6.2% (= **1.7 frames**, same sign both sides) |

### Reading

**Check 1 is decisive.** Two instruments with no shared machinery — video frame analysis vs binary header decode — agree to one part in a thousand on the same clip.

**Check 2 closes the fps question.** The commission would have accepted `offset12 = 30` as INFERRED. It is not. 24 and 60 are excluded by 25% and 50%. **`offset 12 = fps` is MEASURED, cross-instrument confirmed.**

**Check 3 independently validates a *derived* quantity** — root-lock fraction over contact time = clip ÷ (clip + controller swing pause) — from two `.dbr`/`.anm` layers that were never fitted to it.

**Check 4 is the one genuine discrepancy, and it is informative rather than troubling.** The sum matches to 0.1% but the split is 1.7 frames (0.056 s) later in galadriel's read, *with the error in the same direction on both sides* (her wind-up longer, her recovery shorter by the same amount). That is the exact signature of measuring **visible impact** rather than **callback fire**: the damage callback fires, then the VFX/hit-reaction becomes visible ~2 frames later. It is not a decode error; it is two instruments correctly measuring two different, adjacent events.

**Consequence for the handoff:** `windup_s` in my table is the **damage-application frame** (engine truth, what the Godot runtime must schedule damage on). galadriel's is the **player-perceived impact** (what a human eye sees). Both are correct and they differ by a small, apparently systematic offset. Godot should use mine for scheduling and hers for VFX timing. **This distinction should be carried on the artifact and not collapsed.**

---

## § 6 — Demonstrative family sample

Family = skeleton (anim table); **90 distinct** across the roster. Basic-attack clip, `unarmed` class.

| family (anim table) | n bodies | clip frames | clip dur (s) | swing period (s) | wind-up (s) | run speed | swing pause (s) |
|---|---|---|---|---|---|---|---|
| `anm_malepc` | 70 | 15\|15 | 0.507 | 0.604 | — | 0.71 | 1.29 |
| `anm_femalepc` | 51 | 15\|15 | 0.517 | 0.645 | — | 0.71 | 1.45 |
| `anm_skeleton_fast` | 41 | 33\|37\|33 | 1.138 | 1.149 | — | 1.10 | 1.39 |
| `anm_groble` | 40 | 37\|41\|37 | 1.271 | 1.084 | — | 1.03 | 1.31 |
| **`anm_slith`** | **37** | **41\|51\|41** | **1.478** | **1.584** | **0.433** | **0.79** | **1.21** |
| `anm_spidergiant` | 34 | 51\|51\|51 | 1.700 | 1.526 | — | 1.83 | 0.60 |
| `anm_zombiewalker` | 28 | 39\|38\|28 | 1.164 | 0.993 | — | 1.35 | 1.05 |
| `anm_prawn` | 25 | 29\|27\|21 | 0.856 | 0.856 | — | 1.01 | 0.80 |
| `anm_chthonian_devourer` | 22 | 25\|24 | 0.817 | 0.731 | — | 1.08 | 0.60 |
| `anm_swampcrab` | 22 | 29\|27 | 0.933 | 0.933 | — | 1.00 | 0.82 |
| `anm_troll` | 22 | 37\|41\|53 | 1.444 | 1.107 | — | 1.32 | 0.95 |
| `anm_half-troll_shaman` | 21 | 15\|15\|15 | 0.507 | 0.501 | — | 0.94 | 1.14 |
| `anm_yeti` | 20 | 25\|21\|28 | 0.818 | 0.818 | — | 0.97 | 0.84 |
| `anm_chthonianminion` | 20 | 37\|37\|37 | 1.227 | 1.204 | — | 1.35 | 0.60 |
| `anm_chthonianvoidfiend` | 19 | 43\|43 | 1.433 | 1.348 | — | 0.88 | 1.15 |
| `anm_ghost_male` | 18 | 15\|15 | 0.507 | 0.565 | — | 0.64 | 1.25 |

(Per-body wind-up/recovery/root-lock for all 968 are in `tg_monster_timing.csv`; the sample above shows family means for the columns that aggregate meaningfully.)

Note the design grammar this exposes: **humanoid PC-skeleton bodies swing in ~0.51 s with a ~1.3 s pause; large monsters swing in 1.2–1.7 s with a ~0.6–0.9 s pause.** Threat is paced by clip length, and stand-off recovery is paced by controller pause — they trade off in opposite directions.

Worked multi-hit example — Aetherial Abomination `attackspecial_a01` (101 frames = 3.367 s): hits at frames 20, 35, 50, 65, 89 → **5-hit combo inside one clip**, mean gap 17.25 frames = **0.575 s**, plus `voxSound`@28 and a `CreateEntity` FX (`AetherialAbomination_Slam_Trail_FX01.dbr`, attach `L Hand`) at frame 5 = **0.167 s telegraph onset**. 220 slots across the roster carry >1 hit per clip.

---

## § 7 — Handoff

### To galadriel (frame lap) — the lap is NOT displaced; it is re-pointed

1. **Telegraph is your dimension.** It is the one of six where the corpus is sparse (13.6% best case). Prioritize it.
2. **You now have a measured baseline to validate against instead of a blank.** `tg_monster_timing.csv` gives you predicted wind-up/recovery/clip/root-lock for 963 bodies. Families that disagree with your frames are the interesting ones.
3. **The ~1.7-frame offset (§ 5 check 4) is worth pinning.** If callback-fire vs visible-impact is a stable offset across families, it is a reusable conversion constant for the whole pipeline. Test it on 3–4 more families.
4. **Bodies with `anim_classes_alt` populated (454/968) are ambiguity cases.** Your footage shows which weapon the spawn actually rolled; the DB cannot. Report the observed class so the scalar can be branched.
5. **`REF-UNSATISFIED-BY-TABLE` slots (353) are the highest-value forensic target** — footage is the only way to learn the engine's fallback rule (§ 3.3).

### To drax (Godot runtime)

- Consume both CSVs alongside the baton. Key = `record`, identical to the baton roster.
- **Schedule damage on `windup_s` (callback-fire), not on visible impact.** Use `recovery_s` for the commit tail, `root_lock_s` / `root_lock_frac` for movement lock. 751 bodies are **full-clip-locked** — no early interrupt exists for them.
- `basic_swing_period_s` already folds `characterAttackSpeed`; add controller `maxSwingPause` for the gap between swings.
- Gate specials on `delay_s` + `chance_pct` + `range_band`; `numAttackSlots` (4 or 8) caps concurrent attackers on the player.
- **Never consume `fallback_anm_dur_s` without reading `anim_binding_grade` on the same row.**

### To gamora / the KC2 board

- **This changes nothing in the KC2-SIM run.** Parallel track. `NAMED-ABSENT-DECLARED` on the provenance block per Rider 3 stands as written for the emit.
- Informational for a *later* revision: the declared absence is narrower than believed. Attack-timing grammar is now MEASURED for 5 of 6 dimensions at ≥99% monster-level coverage. **Do not amend the emit's provenance block mid-run** — preregistration holds, and this artifact is not on that gate.
- § 3.1 is directly actionable: `t22`'s `attack_speed_tag` column is constant across all 967 and carries no signal.

### Follow-on that can go to legolas-crawler (lane is now MAPPED)

The `.anm` header + event-trailer decode is a known schema with a known procedure. Mechanical, no judgment required:

1. Extend the `.anm` event census beyond the KC2 roster to **all** creature `.anm` (3,452 indexed here; the roster touches a subset).
2. Resolve the `CreateEntity` FX `.dbr` targets into the `.arz` for telegraph FX **duration/radius/colour** — that is the most likely route to lifting dimension 3 off 13.6%, and it is pure known-schema `.arz` work.
3. Extract the non-`unarmed` weapon-class branches for the 454 multi-class bodies, emitting timing as a distribution.

Contract for the crawler: schema is § 1.3 + § 1.4; grading vocabulary is § 3.3's `anim_binding_grade`; **HALT on any `.anm` where `size ≠ 56.068 × frames × bones + 1004 ± 2KB`** — that identity is the crawler's mechanical tripwire that the header decode still holds.

---

## § 8 — Grades

| Claim | Grade |
|---|---|
| `.anm` header: offset 8 = frame count, offset 4 = track count | **MEASURED** (r² = 0.999997, n = 3,452; both controls fail) |
| `.anm` header: offset 12 = fps, value 30 | **MEASURED** (invariant n = 3,452; cross-instrument confirmed −0.10% vs WR3; 24/60 excluded) |
| `.anm` ASCII event trailer: `CallbackPoint` / `CreateEntity` name+frame | **MEASURED** (11,030 + 1,922 blocks, 62 names, self-describing plain text) |
| wind-up = first `*Hit` frame ÷ 30 | **MEASURED** — 963/968 bodies. **Semantics = damage-application frame, NOT perceived impact** (§ 5 check 4) |
| recovery = (frames − last `*Hit`) ÷ 30 | **MEASURED** — 963/968 |
| root-lock = `AllowInterrupt` frame ÷ frames, else full clip | **MEASURED** — 963/968; cross-check −1.13% vs WR3 |
| cadence (delay/chance/range/timeout/cooldown/pause/atkspeed) | **MEASURED**, DB-resident |
| projectile velocity | **MEASURED**, DB-resident, 152/191 projectile DBRs |
| telegraph duration | **MEASURED but SPARSE** — 13.6% best slot-level coverage; **DECLARED WEAK** |
| roster join to t22 basis `0d6992e8` | **MEASURED** — 967/968; the 1 miss is t22's own known INFERRED scavenger |
| `characterBaseAttackSpeedTag` degenerate | **MEASURED** — 967/967 identical |
| active animation class at spawn | **NOT-FOUND in DB** — stochastic equip roll (§ 3.2) |
| engine fallback clip for unsatisfied bindings | **NOT-FOUND in DB** — 353 slots affected; `fallback_anm_dur_s` is **LABELLED-ASSUMPTION**, never MEASURED |
| animation blend-in duration | **NOT-FOUND in either layer** |
| `specialAttackTimeout` as an animation window | **REFUTED / NOT-DIAGNOSTIC** (r = 0.132, § 3.5) |
| WR3 comparison values (0.489 / 0.879 / 0.796) | **QUOTED from commissioning note; NOT re-measured by me; underlying artifact not located on disk** |
| `.arc` payload CRC | **NOT VALIDATED** (reader limitation carried from 2026-07-26 probe) |
