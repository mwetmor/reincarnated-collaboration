# Research — WR3 stage-2 referent extraction (Evade · boss attack timings · speeds) — 2026-07-30

**Mode:** A (analytical / primary-source probe — new format lane established)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR), per **R-WR3-17 (b)(c)(d)**
**Access mode:** read-only throughout. Writes confined to this note and
`legolas/scratch/2026-07-30-wr3-stage2/`. No game file modified; the game was never launched.

**Grading key:** **M** = MEASURED (read verbatim from a pinned binary) · **C** = COMPUTED (from M
inputs under a named operator) · **D** = DOCUMENTED (from in-game text / patch-note-tier source) ·
**U** = UNRESOLVED.

**Companions:** `legolas/research/2026-07-30-gd-l13-reference-envelope.md` (§3a U-1 is closed here) ·
`legolas/notes/2026-07-28-wr1-mechanism-extraction.md` (gaps **G-1** and **G-3** are closed here) ·
`legolas/notes/2026-07-28-kitcal1-g7-gdc-save-findings.md` (the save fixture).

---

## Summary

**The ledgered `.anm` question is discharged.** The `.anm` container was reverse-engineered end to
end (§0). It is not opaque: it carries an explicit **fps field, an explicit keyframe count, per-bone
root motion, and a plain-text `CallbackPoint` trailer naming the contact frame of every attack**.
Everything R-WR3-17(d) asked for is now MEASURED rather than inferred. Four things follow, in order
of how much they should change stage 2.

1. **The referent boss commits far harder than our sim's boss, and the commit is a full root-lock.**
   Primordian's melee swing is **0.489 s wind-up to contact / 0.879 s recovery / 1.369 s total**
   (weighted over its three swing variants, Normal 1-player), against our sim's 0.30 / 0.20 / 0.60.
   The attack animations carry **zero root translation** (M) — the boss cannot move for the entire
   swing. GD's boss is **rooted ~79.6 % of its melee cycle**; ours is rooted 28.6–40 % (R-WR3-13).
   **If GD governs, CAL-C1/CAL-C2 roughly triple and quadruple respectively.**
2. **The nova's telegraph is 0.80 s, not 0.5 s.** `primordian_frigidring` casts through the `Roar`
   animation; the projectile ring releases on the `RightHandHit` callback at **0.800 s** after cast
   start (0.87–0.89 s if the difficulty pak's speed penalty applies — see §2.3), out of a 1.600 s
   total cast during which the boss is likewise rooted.
3. **The speed row in charter §3 is measuring the wrong boss, and the sign flips when it measures
   the right one.** The `0.99 / 0.81` pair is **Warden Krieg** ph.1/ph.2. Against **Primordian** —
   the boss the fixture is actually built on — the player is **1.29–1.33× FASTER** under *both*
   competing composition models. Our fixture's **1.43×** is therefore only 7–11 % more
   player-favoured than the referent, i.e. **materially in band, not "generous."** This is a
   HALT-and-escalate item: R-WR3-17(b) directs speed *parity*, which would make our boss
   **more** boss-favoured than anything Matt actually fought. See §4.
4. **GD's Evade carries no i-frames.** It is a pure positional dash: 3.0 s cooldown, 1 charge,
   10.0 u maximum range, ~0.28 s of travel inside a 0.33 s action-lock. No immunity, absorption,
   avoidance or damage-nullification field exists on the record, on its template, or on any of the
   nine GDX3 runes that modify it (M). **Evade was present and enabled in Matt's L13 save** (M,
   `character_skills[7]`, level 1, `enabled=1`) — with no rune modifiers equipped. This is
   fence-friendly: the referent's dodge is *movement*, exactly the object §7.2 does not protect.

**One acquisition gap blocks full fidelity** (§5, U-1): Matt fought the boss in **werewolf form**,
whose animation set is GDX3-only, and the local asset pin has no GDX3 `Creatures.arc`. Every
player-side timing below is the **human-form** figure. Routed as a `matt_to_do` candidate.

---

## 0. The `.anm` format — first-of-kind documentation (this closes the ledgered question)

Container located at `/Users/admin/Games/vendor/grim-dawn/resources/Creatures.arc`
(SHA-256 `bdafb010…de07c`), read with the existing `gd_arc_reader_2026_07_26.py` ARC v3 reader.
**Provenance note:** this asset pin's `database/database.arz` is byte-identical (SHA-256
`8cdeff12…ae3f`) to the Edition-II DB pin used by all prior GD notes, so the asset and record
corpora are the same game build.

**Format (little-endian, byte-packed, no alignment padding) — all M:**

```
header (16 B):  magic b'ANM' | u8 version (=2) | u32 nBones | u32 nKeys | u32 fps
per bone:       u32 nameLen | char name[nameLen] | nKeys x 56-byte key (14 float32)
trailer:        plain UTF-8 text, CRLF, zero or more blocks:
                  CallbackPoint\r\n{\r\n\tname = "<EventName>"\r\n\tframe = <int>\r\n}\r\n
```

Validation performed (all pass):
- `fps` reads **30** on every one of the 25 clips parsed, across four different rigs with bone
  counts 26–56 — a constant that tracks nothing else in the file. It is frames-per-second.
- The declared bone/key counts reproduce the exact byte offset of every subsequent bone name string,
  and consume the file to within the trailer length. Zero residue.
- **Clip duration = `(nKeys − 1) / fps`**, not `nKeys / fps`. Decided by measurement, not
  convention: for looping/complete clips the final key is a **byte-level duplicate** of the first
  (`|f0 − f_{N-1}| = 0.00005` vs `|f0 − f1| = 2.169` on the PC run cycle; same result on slith run,
  slith walk, slith attack_01). The last key is the loop-closing duplicate, so the clip spans
  `N − 1` intervals.
- Bone 0 (`Target_CTRL` / `Bip001`) carries **root motion** in key floats [0:3]; it is monotonic
  along one axis for locomotion clips and identically zero for attack clips.

**Why this matters beyond the numbers:** the envelope's U-1, WR1's G-1 and WR1's G-3 all said the
same thing — "the duration lives in the `.anm` binaries, which this corpus does not ship." Both
halves were wrong: the corpus ships them one directory over, and the binary is trivially legible.
No in-client observation and no Matt-only measurement was needed for any figure below.

Parser: `legolas/scratch/2026-07-30-wr3-stage2/a4_parse.py` (+ `a5`–`a10` probes). Arithmetic:
`z1_compute.py`.

---

## 1. TARGET 1 — GD Evade as it existed in Matt's session

### 1.1 Availability in the session — **M, decisive**

| datum | value | grade | source |
|---|---|---|---|
| Evade present in the L13 save | **yes** — `character_skills[7]` = `records/skills/default/defaultevade.dbr`, `level = 1`, `enabled = 1` | **M** | `legolas/scratch/2026-07-28-gdc-parse-g7/parsed.json` (save SHA-256 `0be3a99f…ee91`) |
| Evade modified by gear | **no** — the nine `rune_*_evade.dbr` skill-modifiers are the only records in the entire corpus that touch Evade; none of the 10 equipped items is a rune | **M** | `s8_refs.py` corpus-wide reference sweep + `gear_named.json` |
| Mod present | **no evidence of one.** The boss record resolves out of stock `database.arz`; the mastery (`playerclass10`, Berserker) is stock GDX3; difficulty `128 / 0` = Normal, 1 player | **M** | G-7 §1.12; `s3_arzgrep.py` |

So Evade in Matt's session was **stock, rank 1, unmodified**. (The commission's phrase "the mod's
`boss&quest/slith_wightmirecave01`" appears to be path shorthand — that record is base-campaign.)

### 1.2 Parameters — **M from `records/skills/default/defaultevade.dbr`**

| parameter | value | unit | grade | note |
|---|---|---|---|---|
| `Class` | `Skill_Evade` | — | M | template `skill_evade.tpl` |
| `skillCooldownTime` | **3.0** | s | M | template desc: "Seconds" |
| `cooldownCharges` | **1** | — | M | template desc: "Amount of times skill can be used in a row" |
| `waveDistance` | **10.0** | game units | M | template desc: **"Maximum range"** |
| `maxMoveRatio` | **1.1** | ratio | M | template desc: "Ratio between absolute and walkable distances" — a pathing constraint |
| `characterRunSpeedModifier` | **+250.0** | % | M | see §1.4 caveat |
| `distanceProfile` / `targetingMode` | `Long` / `Point` | — | M | |
| `skillMaxLevel` | 1 | — | M | not rankable |
| **damage immunity / i-frames** | **ABSENT** | — | **M (negative)** | see §1.3 |
| in-game description | *"Dash quickly in the target direction to evade attacks."* | — | **D** | `tags_skills.txt` → `tagSkillDefaultEvadeDescription01` |

### 1.3 The i-frame question — **M-negative, and it is a strong negative**

Three independent reads, all empty:
1. The record's 476 fields contain **no** non-zero defensive, absorption, avoidance, dodge-chance,
   invulnerability or damage-nullification value. Every `defensive*` / `retaliation*` field is 0.
2. `skill_evade.tpl` declares exactly **two** variables of its own — `maxMoveRatio` and
   `waveDistance` — over `Skill_Base` + `Skill_Activated` + `Skill_WarmUp`. There is no field an
   i-frame *could* live in.
3. All nine GDX3 `rune_*_evade` skill-modifiers touch **only** `skillCooldownTime` (−0.5 to +1.0)
   and `cooldownCharges` (+1). Crate's own designed lever set for Evade is cooldown and charges —
   not invulnerability.

**Reading (C, but tight):** GD's Evade avoids damage *geometrically* — by leaving the hitbox before
resolution — not statistically. That is Mechanism-K-shaped, not dodge-skill-shaped, and it does not
disturb the R-WR3-12 (8.1) fence.

### 1.4 Timing and distance — **M inputs, C composition** (human form; see §5 U-1)

Matt's L13 human form wields a 1h blunt ⇒ animation slot `sHanded`.
`anm_malepc.dbr`: `sHandedEvadeAnim = creatures/pc/anm/hero01_unarmed_dodge01.anm`,
`sHandedEvadeAnimSpeed = **1.30**` (M). All six PC dodge clips are the same 29-key length (M).

Clip `hero01_unarmed_dodge01.anm`: **29 keys @ 30 fps**; callbacks
`StartJump@f2`, `voxSound@f2`, `StopJump@f13`, `Hit@f13`, `AllowInterrupt@f13` (M).
Root-motion profile on `Target_CTRL`: zero through f2, then a decelerating slide reaching
**11.000 u at f13**, then flat to the end (M).

| quantity | raw (1.0×) | **at 1.30×** | grade | operator |
|---|---|---|---|---|
| total clip | 0.9333 s | **0.7179 s** | C | `(29−1)/30 ÷ 1.30` |
| dash start (`StartJump` f2) | 0.0667 s | **0.0513 s** | C | `2/30 ÷ 1.30` |
| dash end / action-lock end (`StopJump`+`AllowInterrupt` f13) | 0.4333 s | **0.3333 s** | C | `13/30 ÷ 1.30` |
| **traversal window** (f2→f13) | 0.3667 s | **0.2821 s** | C | `11/30 ÷ 1.30` |
| **displacement** | 11.000 u (anim) · **10.0 u** (skill max range) | — | M | root motion vs `waveDistance` |
| implied dash rate | — | 35.5 u/s (at the 10 u cap) · 39.0 u/s (uncapped anim) | C | |
| **committed window** | — | **0.333 s** | C | interruptible from f13 |

**Named caveat (U):** how `characterRunSpeedModifier = +250` composes with the root-motion slide is
**not resolved from source**. The animation alone accounts for the full 10–11 u displacement, so the
+250 % is more plausibly the engine's means of realising it (or a brief post-dash carry) than an
additional 3.5× on top. **Do not stack them.** The decision-grade numbers are the animation-derived
ones: **10 u in ~0.28 s, on a 3 s cooldown, single charge, no immunity.**

### 1.5 Reconciliation to our sim

| row | GD referent | our sim today | delta |
|---|---|---|---|
| dodge exists in player toolkit | yes, stock, enabled | **none** (F-WR2-5: intents {reposition/advance/hold}) | the R-WR3-17(c) build |
| cooldown | 3.0 s | — | new CAL row |
| distance | 10.0 u ≈ **1.74× the fixture's 5.75 m/s × 1 s** | — | large relative to the 2.000 m pinned separation |
| commit cost | 0.333 s locked | — | K's action must carry a lock, not be free |
| i-frames | none | none proposed | §7.2 fence intact |

---

## 2. TARGET 2 — the boss's real attack timings

Boss = `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ("Primorian the Forgotten
One", per its own `FileDescription` — note the game's internal spelling omits the *d*).
`charAnimationTableName = records/creatures/enemies/anm/anm_slith.dbr`;
`characterAttackSpeed = 1.0`; `controller = controller_boss_viloth.dbr` (all M).

### 2.1 What each number IS vs what it is COMPUTED from

Every timing below is `frame ÷ 30 fps ÷ (animSpeed × characterAttackSpeed × pakModifier)`.
The frame numbers and the animation-speed multipliers are **M**; the composition is **C**.

### 2.2 Melee swing — **M frames, C durations**

`anm_slith.dbr` melee slots (M): three weighted variants.

| slot | clip | weight | `AnimSpeed` | keys | `SwipeRight` | **`RightHandHit` (contact)** |
|---|---|---|---|---|---|---|
| `unarmedAttackAnim1` | `slith01_attack_01.anm` | 40 % | 1.20 | 41 | f9 | **f13** |
| `unarmedAttackAnim2` | `slith01_attack_02.anm` | 40 % | 1.25 | 51 | f17 | **f20** |
| `unarmedAttackAnim3` | `slith01_attack_01.anm` | 20 % | 1.05 | 41 | f9 | **f13** |

Difficulty pak `records/game/balancingadjustment_mp+difficulty_enemies01.dbr`, Normal/1-player slice:
`characterAttackSpeedModifier = **−10 %**`, `characterRunSpeedModifier = −18 %`,
`characterSpellCastSpeedModifier = −8 %` (all M).

**With the pak (Matt's actual conditions):**

| variant | eff. rate | wind-up→contact | total | post-contact recovery |
|---|---|---|---|---|
| attack_01 @1.20 (40 %) | 1.080 | 0.4012 s | 1.2346 s | 0.8333 s |
| attack_02 @1.25 (40 %) | 1.125 | 0.5926 s | 1.4815 s | 0.8889 s |
| attack_01 @1.05 (20 %) | 0.945 | 0.4586 s | 1.4109 s | 0.9524 s |
| **weighted** | — | **0.4892 s** | **1.3686 s** | **0.8794 s** |

*(Without the pak the weighted trio is 0.4403 / 1.2317 / 0.7914 s. The pak-applied row is the one
that governs; the no-pak row is shown so the operator is auditable.)*

**Root motion during the swing = 0.0000 u** on `slith01_attack_01`, and ≤0.15 u of incidental jitter
on `slith01_attack_02` (M). **The commit is a hard root-lock, both sides of the contact frame.**

Inter-swing idle: `controller_boss_viloth` `minSwingPause = 0.30`, `maxSwingPause = 0.40` (M) —
the tightest bounded pause in the L13 roster.

**Derived cycle (C):** 1.3686 + U(0.30,0.40) → mean **1.7186 s** per swing, of which
**1.3686 s (79.6 %) is rooted**.

### 2.3 Nova cast time — **M frames, C duration**

`specialAttack2SkillName = records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr`
(`Skill_AttackProjectileRing`, 16 projectiles, 360°). Its `skillSpecialAnimationName = **'Roar'**`
resolves through `anm_slith.dbr` `unarmedSpecialAnimRef3 = 'Roar'` →
`unarmedSpecialAnim3 = slith01_cast_buff_01.anm` at `unarmedSpecialAnimSpeed3 = **1.25**` (all M).

Clip: **61 keys @ 30 fps**; `SwipeRight@f25`, `RightHandHit@f30` (M). Root motion 0 (M).

| rate model | **release (`RightHandHit`)** | `SwipeRight` | total cast |
|---|---|---|---|
| anim-table only (1.250) | **0.8000 s** | 0.6667 s | 1.6000 s |
| + pak attack −10 % (1.125) | 0.8889 s | 0.7407 s | 1.7778 s |
| + pak cast −8 % (1.150) | 0.8696 s | 0.7246 s | 1.7391 s |

**U (minor):** which pak modifier applies to a monster *attack-class skill* animation is not
resolvable from source. Band **0.80–0.89 s**; recommend **0.80 s** as the anchor with the band
carried. Cadence gates (M): `specialAttack2Chance 80 %`, `Delay 6.0 s`, `Timeout 3.0 s`,
`Range MediumRange`.

Two further boss abilities, for completeness (M): `primordian_wave` (`specialAttackSkillName`,
`Skill_AttackWave`, `waveTime 1.4 s` over `waveDistance 16`, anim ref `TailLashSunder` →
`slith01_attack_special_sunder.anm`, 79 keys, contact f23 @0.90× ⇒ release **0.852 s**, total
**2.889 s**); `chillbane_blizzard` (`specialAttack3`, ground-drop, `skillActiveDuration 8.0`).

### 2.4 Reconciliation to our sim (**this is the R-WR3-17(d) answer**)

| row | GD referent (Primordian, Normal 1p) | our sim (R-WR3-13) | verdict |
|---|---|---|---|
| melee wind-up (CAL-C1) | **0.489 s** (variant range 0.401–0.593) | **0.30 s** | **GD is 1.63× longer** |
| melee recovery (CAL-C2) | **0.879 s** (0.833–0.952) | **0.20 s** | **GD is 4.40× longer** |
| total lock `T_lock` | **1.369 s** | 0.60 s | GD is 2.28× longer |
| full swing cycle | **1.719 s** | 1.500 s (metronome, {1.5 s 89.7 %, 1.6 s 10.3 %}) | **in band, ~15 %** |
| **rooted fraction of cycle** | **79.6 %** | 28.6 % spec-literal / 40.0 % cooldown-absorbing | **GD is 2.0–2.8× more committed** |
| nova telegraph | **0.80 s** (band to 0.89) | 0.5 s advertised (R-WR3-13 F3 writes `wind_up_s = 0.30`) | **GD is 1.6–2.7× longer** |
| commit is a movement root-lock | **yes, 0.000 u root motion** | modelled as a lock | agrees |

**The headline for the conductor:** our *cycle length* is right (1.50 vs 1.72 s) but our *duty cycle
is inverted*. GD's boss buys its cadence almost entirely with committed, rooted animation; ours buys
it almost entirely with free idle. That is precisely the mechanism R-WR3-5 named as load-bearing,
and the referent now gives it a number: **T_lock ≈ 1.37 s inside a 1.72 s cycle.** Note this sits
well above the `T_lock ≲ 0.75` "safe ceiling on this fixture" that gamora's duty-cycle read
established — a real tension the stage-2 grill must resolve, not a number to adopt silently.

---

## 3. TARGET 3 — exact speed values

### 3.1 The measured inputs (all **M**)

| datum | value | source |
|---|---|---|
| player `characterRunSpeed` | **0.93** | `records/creatures/pc/malepc01.dbr` (base `.arz` carries 0.92; expansion override 0.93) |
| movement-speed affixes on Matt's 10 equipped items | **none** | all 30 affix/base records swept, zero `characterRunSpeed*` |
| Primordian `characterRunSpeed` | **0.85** | `slith_wightmirecave01.dbr` |
| Warden ph.1 / ph.2 `characterRunSpeed` | 1.15 / 1.40 | `warden01.dbr` / `warden02.dbr` |
| difficulty-pak monster run modifier (Normal) | **−18 %** | `balancingadjustment_mp+difficulty_enemies01.dbr` |
| PC run clip root motion ÷ duration | 6.858 u ÷ 0.8000 s = **8.5725 u/s** | `hero01_sword1h_run.anm` (identical on `sworddw` and both `_floating` variants) |
| slith run clip | 10.0839 u ÷ 1.1333 s = **8.8976 u/s** | `slith01_run_01.anm` |
| warden run clip | 5.000 u ÷ 0.9667 s = **5.1724 u/s** | `warden_run_01.anm` / `wardenphase02_run_01.anm` |

### 3.2 What the charter's two ratios actually measured

`0.99 / 0.81` = **`characterRunSpeed`-multiplier ratios, for Warden Krieg phase 1 and phase 2**,
player 0.93 vs 0.943 and 1.148 after the pak. They are **not Primordian**, and they are not
absolute speeds. Since the fixture's HP anchor (15,822), its nova and its controller all come from
**Primordian**, §3's speed row and the referent's boss row are describing two different monsters.

### 3.3 Absolute values — and why the model fork does not matter here

`characterRunSpeed` is a multiplier; the base it multiplies is not stated in the `.arz`. Two
composition models remain open:

- **Model A (animation-driven base):** speed = `rootMotion ÷ clipDuration × characterRunSpeed`.
- **Model B (global constant base):** speed = `characterRunSpeed × k`, with playback time-warped to
  match. This is what the `0.99/0.81` row implicitly assumed.

I could not close the fork from source: `gameengine.dbr` carries only percentage caps
(`playerRunSpeedCapMax 135`, `monsterRunSpeedCapMax 500`), no absolute constant; and a 27-creature
census of `animBase × characterRunSpeed` (`a9_speedcensus.py`) produces a 6× spread of "bases"
(skeleton 1.91 u/s → rifthound 11.43 u/s) that is suggestive under either reading. **Reported as
U-2, not adjudicated.** Fortunately the fork does not change the answer that matters:

| pairing | **Model A** (player : boss, u/s) | ratio | **Model B** (multipliers) | ratio |
|---|---|---|---|---|
| **player : Primordian** | 7.9724 : 6.2016 | **1.286×** | 0.930 : 0.697 | **1.334×** |
| player : Warden ph.1 | 7.9724 : 4.8776 | 1.635× | 0.930 : 0.943 | 0.986× |
| player : Warden ph.2 | 7.9724 : 5.9379 | 1.343× | 0.930 : 1.148 | 0.810× |
| **our fixture** | 5.75 : 4.025 m/s | **1.429×** | — | — |

**Both models agree the player was faster than Primordian, by 1.29–1.33×.** The models disagree only
about Warden — which is not the fixture's boss.

Unit note (**C, unproven**): several root-motion values are exact foot multiples in metres
(6.858 = 22.5 ft, 3.810 = 12.5 ft, 7.620 = 25 ft, 1.906 = 6.25 ft), suggesting 1 game unit ≈ 1 m.
Not all rigs fit, and `actorHeight = 3.0` for a human PC argues against a clean metre reading.
**Compare ratios; treat u ≈ m as a plausible scale only.**

### 3.4 Reconciliation to our sim

| row | GD referent | our sim | verdict |
|---|---|---|---|
| player : boss speed | **1.29–1.33×** player-favoured (vs Primordian) | **1.43×** player-favoured | **IN BAND, 7–11 % over** |
| charter §3's stated referent | 0.99 / 0.81 boss-favoured | — | **wrong boss** — Warden, not Primordian |
| absolute player speed | 7.97 u/s (Model A) | 5.75 m/s | same order; unit scale unproven |

---

## 4. HALT-AND-ESCALATE — one directive is aimed at a falsified premise

**R-WR3-17(b) directs speed parity** (player = boss) on the strength of R-WR3-5's "sharpest fact":
*the GD referent boss was FASTER than the player (0.99/0.81) and Matt still kited it.*

That fact is **Warden-specific and model-specific**. Against the boss the fixture models, the
referent player was **1.29–1.33× faster**. Setting our sim to 1.00× would therefore push the fixture
**past the referent, to the boss-favoured side of anything Matt actually fought** — and it would do
so while stage 2 is simultaneously trying to *raise* the win rate from 100 % into 40–60 %.

I am not ruling on this; I am flagging that the premise moved. Three readings the conductor may want
on the table, offered as options and not as a recommendation:

1. **Parity as a deliberate over-correction** — accept it as a calibration knob that intentionally
   exceeds the referent, with the referent row restated so the ledger does not later read as fidelity.
2. **Referent-matched ratio 1.30×** — a 9 % trim from 1.43×, which is a much smaller lever than
   parity and may not move the win rate at all.
3. **Spend the correction on commit instead** — §2.4 shows the fixture's real fidelity gap is the
   duty cycle (79.6 % vs 28.6–40 %), not the speed ratio. Speed parity and a 2–2.8× longer lock are
   *both* boss-favouring; doing both at once risks overshooting the 40–60 % band from above.

**No `matt_to_do` is generated by this item** — it is a conductor ruling, not a host action.

---

## 5. Gaps — flagged, not guessed

| # | Item | Why it is open | What would close it |
|---|---|---|---|
| **U-1** | **Werewolf-form player timings** (Evade clip length, run-anim base, attack cadence). Matt fought the boss in werewolf form; `anm_werewolf.dbr` routes to `creatures/pc/werewolf/anm/*` with `unarmedEvadeAnim = hero_werewolf_dodge_a01.anm` at `unarmedEvadeAnimSpeed = 1.0` (M) — a **different clip at a different rate** from the human 1.30×. `anm_werewolf.dbr` is **GDX3-only**, and the local asset pin (`vendor/grim-dawn/`, base+GDX1+GDX2, 2026-07-23) ships **no GDX3 `Creatures.arc`**. Confirmed by exhaustive `rglob("*.arc")` sweep: zero `werewolf` asset entries anywhere. | **`matt_to_do` CANDIDATE — Steam-authenticated depot pull.** `DepotDownloader` is already resident at `vendor/depotdownloader/`, and the Edition-II pull precedent exists; but it needs Steam credentials, which is a Matt-only action. Scope: the GDX3 asset depot's `Creatures.arc` only (~0.5 GB). Once present, every figure in §1.4 re-derives in minutes with the parser already written. **Confirmed NOT needed for §2 or §3** — Primordian, Warden and the human PC are all base-game assets, fully measured. |
| **U-2** | **`characterRunSpeed` composition model** (§3.3). Blocks *absolute* m/s claims; does **not** block the player:Primordian ratio, on which both models agree. | An engine-side constant (not in `gameengine.dbr`), or one timed in-client traversal over a known distance. Low value — the ratio is what stage 2 uses. |
| **U-3** | **Which pak speed modifier applies to a monster attack-class skill animation** (§2.3). Moves the nova telegraph within 0.80–0.89 s. | Not closable from source; the stage-2 spec should name which reading it adopts. |
| **U-4** | **Whether GD blends out of the post-contact recovery on player interrupt.** Slith attack clips carry no `AllowInterrupt` callback (the PC dodge does) — read as "the full clip plays" — but absence of a callback is weaker evidence than presence. | Frame-count off a capture; or accept the 0.879 s recovery as an upper bound and name it. |
| **U-5** | Carried forward unchanged from the envelope: `lastHitBy` 273.704 > `greatestDamageReceived` 260.498. Untouched by this note. | — |

---

## 6. Corrections owed to already-banked artifacts

1. **`2026-07-30-gd-l13-reference-envelope.md` §6 U-1 is CLOSED** — "base attack interval is in the
   `.anm` binaries, not the `.arz`" was half right; the binaries are legible and were one directory
   away. The envelope's "**the envelope's weakest number**" attack-cadence row (1.0–2.0 /s, grade E)
   and the 310–620 HP/s DPS band that rests on it are now closable by the same method for the
   *player* side — **pending U-1's GDX3 assets**, since Matt's cadence was werewolf-form.
2. **`2026-07-28-wr1-mechanism-extraction.md` G-1 and G-3 are CLOSED** for every base-game creature.
   Their stated remedy — "(a) re-pin the depot with the asset `.arc`s and write an `.anm` header
   parser… or (b) measure it off Matt's play-test capture" — resolves to **(a), and the re-pin was
   already on disk.** The recommendation for (b) as "cheaper" should be struck.
3. **Charter §3's speed row** names a ratio measured on Warden Krieg while every other cell in the
   table is measured on Primordian. Recommend the row be split, or relabelled.

---

## 7. Source list

**Primary — datamined record corpus** (read-only,
`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`, `database.arz` SHA-256 `8cdeff12…ae3f`):
`records/skills/default/defaultevade.dbr` · `records/skills/itemskillsgdx3/skillmodifiers/rune_{b301,b302,b303,c301,c302,c303,d301,d302,d303}_evade.dbr` ·
`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/creatures/enemies/anm/{anm_slith,anm_warden_phase1,anm_warden_phase2}.dbr` ·
`records/creatures/enemies/boss&quest/{warden01,warden02}.dbr` ·
`records/controllers/enemy/controller_boss_viloth.dbr` ·
`records/skills/nonplayerskills/bossskills/{primordian_frigidring,primordian_wave}.dbr` ·
`records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr` ·
`records/creatures/pc/{malepc01,anm_malepc,anm_werewolf}.dbr` ·
`records/skills/playerclass10/werewolf1.dbr` ·
`records/game/{gameengine,balancingadjustment_mp+difficulty_enemies01}.dbr` ·
27-record roster sweep from `legolas/scratch/2026-07-28-kitcal1-g5a/roster.txt`.

**Primary — asset corpus** (read-only, `/Users/admin/Games/vendor/grim-dawn/`):
`resources/Creatures.arc` (SHA-256 `bdafb010…de07c`) — 25 `.anm` clips parsed across the slith,
warden, PC and werewolf-adjacent rigs; `database/templates.arc` (SHA-256 `d6d381a5…13e72`) —
`skill_evade.tpl`, `templatebase/skill_activated.tpl`, `templatebase/skill_warmup.tpl`.

**Primary — localisation:** `resources/Text_EN.arc` → `tags_skills.txt`
(`tagSkillDefaultEvade01`, `tagSkillDefaultEvadeDescription01`).

**Primary — fixture save:** `player.gdc` SHA-256 `0be3a99f…ee91`, via G-7 parse artifacts
(`parsed.json`, `gear_named.json`).

**Tertiary — consulted, none used as a basis for any figure.** No web source was needed: every
number in this note is read out of a locally pinned binary. The Steam-forum "100 % attack speed =
2 attacks/s" bound the envelope had carried as its only external anchor is now **superseded by
measurement** and should not be cited again.

**Scratch:** `agentic_orchestration/legolas/scratch/2026-07-30-wr3-stage2/`
(`a4_parse.py` — the `.anm` parser; `a6_all.py` — callback dump; `a8_rootprofile.py` — root motion;
`a10_loopcheck.py` — the duration-convention test; `a9_speedcensus.py`; `z1_compute.py` — all
arithmetic above; `s1`–`s8` corpus probes).

---

## 8. Handoff

**To gandalf (RUN-CONDUCTOR).** Four items, in priority order:

1. **§4 — the R-WR3-17(b) premise moved.** The referent boss was slower than the player, not faster.
   Speed parity now over-corrects past the referent. Conductor ruling owed before the stage-2 CAL
   register is written.
2. **§2.4 — R-WR3-17(d) is answered, and GD disagrees with 0.30/0.20.** Under R-WR3-17(d)'s own
   clause ("if GD disagrees, the referent governs"), CAL-C1 → 0.489 s and CAL-C2 → 0.879 s. But
   T_lock 1.369 s sits far above gamora's measured `T_lock ≲ 0.75` safe ceiling on this fixture —
   so "the referent governs" and "the fixture tolerates it" collide. Needs a ruling, not an adoption.
3. **§1 — Evade parameters are complete and fence-safe** (3.0 s / 1 charge / 10.0 u / 0.33 s lock /
   no i-frames), for the human form. The werewolf-form variant is U-1.
4. **§5 U-1 — one `matt_to_do` candidate**: Steam-authenticated GDX3 asset-depot pull, to close
   werewolf-form player timings. Blocks §1.4 fidelity only; §2 and §3 are unaffected.

**To jack-ryan**, if any of this is ratified: the `.anm` parser (§0) is scratch-grade and
unvalidated against a second implementation; the duration convention rests on the loop-duplicate
test, which is strong but is one test. U-2 and U-3 are unclosed composition ambiguities that any
adopting spec must name a reading for.

**No canonical doc amended by this note.**

---

**Signed:** legolas (UNKNOWN-RESEARCHER), 2026-07-30.
