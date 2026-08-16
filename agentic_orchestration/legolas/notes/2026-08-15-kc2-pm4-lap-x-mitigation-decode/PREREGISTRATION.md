# KC2-PM4 · LAP X — THE MITIGATION-PIPELINE DECODE (both directions) — **PREREGISTRATION**

> **Run:** KC2-PM4 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Commission:** `R-PM4-61 part 5`
> **Seat:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-15
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> **Laws carried:** READ-ONLY on every source · **Law 3 NO tuning** (the referent's numbers are
> GRADES, never inputs) · **GL-12 decode-never-estimate** · **NOTE-9** every quantity asserts its own
> basis · **R-PM4-25** (LO/HI brackets for monotone scalars only; structural unknowns get
> pre-registered candidates + a discriminator, or route) · **R-PM4-27 part 3** (publish both limbs at
> a fork; never pick by grade) · **R-PM4-29** (corrections carry their basis) · **R-PM4-55**
> (this file committed ALONE, FIRST, in its own commit; full-64-hex digests everywhere) ·
> **R-PM4-56 part 4** (any NEW mechanism outside the targets: NAME it, do not decode it, do not fold it).
>
> **This file is committed ALONE and FIRST. No Lap-X instrument has run at the moment of its commit.**

---

## § 0 — THE FIREWALL, AND AN HONEST SCOPING DISCLOSURE

### 0.1 The firewall

This lap will read **no** sim outcome as an input: no findings JSON's grades, no baton, no wave
duration, no time-of-death, no HP track. Every referent-derived number appears in § 5 as a **GRADE**
and is quarantined there.

### 0.2 ⚑ SCOPING DISCLOSURE — what I had already read before writing this file

A preregistration that pretends to more blindness than it has is worse than no preregistration.
Before writing this file I performed read-only *scoping* reads to establish that the targets are
reachable at all. Exhaustively, these were:

| read | what it established (already known to me at prereg time) |
|---|---|
| `records/game/combatformulas.dbr` (44 fields) | the armour / block / PTH equation set exists verbatim in-record |
| `records/game/gameengine.dbr` (367 fields) | `armorDefensiveAbsorption`, `playerDefenseCap`, `monsterDefenseCap`, `monsterLevelGapFixer` exist |
| `templates.arc` field declarations for 9 named fields | field classes/descriptions only |
| `ascension1.dbr`, `tier1_29e_skill.dbr` field dumps | `damageAbsorption` is an **array**, ranked |
| Lap A `measured-player-sheet.csv` | including the block rows and the resistance grid |
| Lap G `pm4g_defensive_actives.csv`, `pm4g_played_kit.csv` | the allocated Soldier/Oathkeeper list |
| Lap L `method.md` § 6–7 | the monster-side armour chain, already decoded at Lap L |
| Lap I `method.md` § 0–1, `pm4i_dot_riders.csv` header | the DoT-rider limb, already decoded at Lap I |
| gamora I-22 landing note; `R-PM4-61` ledger row | the commission |

**Consequences that must be honoured downstream, and are honoured in § 2 and § 4:**

* **`T-C` (shield block) and the `Overguard` clause of `T-D` are NOT blind targets.** I already knew,
  from the Lap A sheet and the Lap G kit census, that this build carries a two-handed weapon and that
  `Overguard` is not in its allocation. Those findings are therefore reported in the findings note as
  **prereg-sighted**, never as discoveries, and § 2's `P-X-3` is written as a *falsifiable
  confirmation with a named falsifier*, not as a blind bet.
* Everything in `P-X-1`, `P-X-2`, `P-X-4`, `P-X-5` is genuinely uncomputed at this moment: no census
  of monster attack magnitudes has been run, no per-piece player armour has been read, no intake or
  TTK arithmetic has been performed.

---

## § 1 — PINNED INPUTS (HALT on any mismatch; full 64 hex, `R-PM4-55 part 2`)

Every instrument re-hashes this table as its first action and **exits non-zero on the first
mismatch**. No instrument proceeds past a mismatch.

### 1.1 Game corpus (edition-III cut)

| input | sha256 |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `edition-III/mods/survivalmode/resources/Scripts.arc` | `47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |

Both binary digests are byte-identical to the values Laps U, V and V-2 pinned.

### 1.2 The played save and the camera-measured sheet

| input | sha256 |
|---|---|
| `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc` | `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5` |
| Lap A `measured-player-sheet.csv` | `6852794382b9bf608f13433ea18be7a52d1f2f0942801e5bb7c4e1be8899badd` |

### 1.3 Prior-lap emissions consumed as substrate

| input | sha256 |
|---|---|
| Lap G `pm4g_played_kit.csv` | `2fd5a34792b96125bd55a40891dfd65cdeb43c385c6ef06607486342d53ce0b3` |
| Lap G `pm4g_defensive_actives.csv` | `0cdfd3af9a22e2d6d7de59ca0b8238f0e2c04c64192a16dee894ef71ae0be306` |
| Lap D `pm4d_band_b_ehp_by_wave.csv` | `3e82e72b5f35f98f9b30ac46c0aa062c42b804a38ac08791e25d74320ded5024` |
| Lap I `pm4i_dot_riders.csv` | `2dc3e380a3800b3afd14f1923d1e2a32efe9263f4ee2eaec7c69c753ed7f6ce1` |
| Lap I `pm4i_wave_damage_modifier.csv` | `f0852cec35a0362c101618b2a269446c4fba658ee0b80821aa5e4ae47eab910b` |
| Lap I `pm4i_survival_wave_arrays_full.csv` | `eab2d141cb41ad83c89b02c9da2a9c7b75ba49d6cb38b27a988a2a172dbd1ce9` |
| Lap L `pm4l_mitigation_by_body.csv` | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` |
| Lap L `pm4l_eor_per_hit.csv` | `120990d998ac23a4b2dadc134e0f5cf3e51a3f7f6eb34ee400d5e2531b26d5a8` |
| Lap L `method.md` | `d33f396d5d47950b9a13a35f1fbeb6ca5c28adaf92346deaae0b10dd8aa0db32` |

### 1.4 The GRADE surface (quarantined; never an input to a decoded value)

| input | sha256 |
|---|---|
| Lap C `measured-reference-truth.csv` | `4546046efd0d01eaceefe5548b46d14c829b8975474f162a007c586b7dcf5642` |

---

## § 2 — THE PRE-REGISTERED PREDICTIONS

All predictions below are **committed before any Lap-X instrument runs**. They are graded in
`pm4x_findings.md` § "graded predictions" against the § 5 observables. A prediction that turns out
wrong is reported wrong and **its wording is not rewritten** (the `S-3` precedent, I-22 § 6).

### `P-X-1` — INTAKE. The implied per-second player intake on the wave-151 28-body board

**Claim, three clauses, all numeric:**

* **`P-X-1a`** The decoded **gross** post-mitigation intake `I_gross` with all 28 wave-151 bodies in
  contact lands in **[300, 1500] HP/s**.
* **`P-X-1b`** `I_gross` **exceeds** the player's bare health regeneration of **129.38 HP/s**
  (sheet, Lap A) — i.e. regeneration alone does not hold the board.
* **`P-X-1c`** `I_gross` is **below 20,005 / 16.0 = 1,250.3 HP/s** — the rate that would empty the
  declared pool inside the referent's own wave-151 duration. If the decode returns above that, the
  decode **over-reads the intake** and I say so.

`I_gross` is defined precisely as: Σ over the 28 wave-151 bodies of (that body's decoded per-second
direct-attack output, post-armour, post-resist, post-declared-caps), evaluated at each body's own
wave-151 level and the wave-151 survival modifiers, with **no** uptime modelling of any player
defensive proc (uptime is I-23's, per the commission) and **no** avoidance term other than those the
records declare.

### `P-X-2` — KILL RATE. Implied player TTK per band-A archetype

* **`P-X-2a`** Folding the **full player damage-type vector** (physical + internal trauma + bleeding
  + pierce + the weapon's chaos→physical 55 % and lightning→physical 46 % and EoR's fire→physical
  100 % conversions) against the **full monster resist vector** moves the median ticks-to-kill by
  **less than ±25 %** from Lap L's physical-only **7.62 ticks**, because after conversion the kit is
  overwhelmingly physical.
* **`P-X-2b`** The decoded band-average player kill rate, at the Lap-L disc geometry, is **≥ 1.0
  bodies/s** — i.e. the decoded kill rate is **fast enough to explain a small standing crowd**, and
  the crowd gap (sim peak living 10 vs referent 19–36) is therefore **not** repaired by any TTK
  correction inside this decode. Stated the other way: I predict this lap **will not** find a
  kill-rate error large enough to close the crowd gap on its own.

### `P-X-3` — BLOCK. **PREREG-SIGHTED** (see § 0.2), stated as a falsifiable confirmation

* **`P-X-3a`** Shield block is **DECODED-ABSENT** for this referent build: block chance 0, block
  amount 0, block recovery 0 — and the record-side reason is that the equipped weapon occupies both
  hands, so no shield record contributes `defensiveBlock`.
* **`P-X-3b`** **Falsifier, named in advance:** if any equipped item record, any allocated skill, or
  any devotion in the played save carries a non-zero `defensiveBlock` / `defensiveBlockChance` /
  `blockAbsorption` / `blockRecoveryTime`, `P-X-3a` is **FAILED** and the sheet's zeros are the thing
  that needs explaining.

### `P-X-4` — THE ARMOUR-SEMANTICS FORK

* **`P-X-4a`** `combatRegion*Chance` (head 15 / shoulders 15 / arms 12 / torso 26 / legs 20 / feet 12)
  is a **hit-location roll**, and therefore player armour applies **per covering piece**, not as the
  sheet aggregate.
* **`P-X-4b`** The sheet's `armor_rating = 3557` is the **SUM** of the six pieces' post-modifier
  armour, **not** their hit-weighted average. **I bet on SUM.** If the reconstruction matches the
  weighted average instead, `P-X-4b` is FAILED and the average limb is the decode.
* **`P-X-4c`** Whichever limb wins, both are published at full size and the fold is handed **both**
  (`R-PM4-27 part 3`). The distinction is worth roughly a factor of six on the effective per-hit
  armour and is therefore load-bearing, not cosmetic.

### `P-X-5` — THE RESISTANCE PIPELINE

* **`P-X-5a`** `playerDefenseCap = 80` is the **player resistance cap**, the sheet's row of 80s is
  the player sitting **exactly at cap** on nine of ten types, and physical 16 is the one type far
  below it.
* **`P-X-5b`** Armour applies to **physical only** and applies **before** resistance; no record field
  expresses a different order, so if the binary does not discriminate the order I will publish
  **both** orders with their numeric consequence rather than pick one.
* **`P-X-5c`** At least one band-A roster record on waves 151–160 carries a non-zero
  `offensive*ResistanceReduction*` field — i.e. the monsters do carry resist reduction and the
  player's 80s are not the whole story. **Directional bet; may lose.**

### What I will NOT predict

Uptime of any player defensive proc. The commission assigns uptime modelling to I-23 and this lap
decodes **record-truth only**. Any number in the findings that would require an uptime assumption is
emitted as a **per-activation** quantity with its declared duration and cooldown beside it, never as
an effective average.

---

## § 3 — DECODE TARGETS AND THEIR METHOD

| id | target | method | grade if the method runs out |
|---|---|---|---|
| **T-A** | armour absorption: formula, %, which types, per-piece vs aggregate, level interaction | `combatformulas.dbr` + `gameengine.dbr` verbatim; per-piece reconstruction from the played save's equipment array (Lap L § 0 recovery, imported not re-implemented); `templates.arc` for field semantics; `Game.dll` string/xref corroboration | DECLARED-GAP with the field named |
| **T-B** | resistance pipeline: order, caps, monster-side reduction/penetration | `gameengine.dbr` caps; full field census of the 151–160 roster for every `offensive*ResistanceReduction*` and `offensive*ReductionPercent*` family | both orders published if undiscriminated |
| **T-C** | shield block: chance, amount, recovery, what it applies to, `Menhir's Will` | `combatformulas.dbr` block equations; equipment array; `willtolive1.dbr` at its own rank | DECODED-ABSENT is a legitimate outcome and is reported as one |
| **T-D** | defensive procs as RECORD-TRUTH: `Ascension`, constellation procs, everything in Lap G's defensive-actives census | each record at its own decoded rank; `damageAbsorption` flat-vs-percent settled by the shipped UI format string; **no uptime** | per-activation quantities only |
| **T-E1** | intake operand: damage-type composition + magnitudes of the 151–160 roster's attack skills | `skillName{i}` walk at `skillLevel{i}` (the Lap D/I/L ratified walk), all `offensive*Min/Max` families, wave-array modifiers at index `w−1` | per-record declared gap, counted |
| **T-E2** | kill-rate operand: monster HP / armour / resists vs the player's damage types | Lap D eHP + Lap L mitigation table, extended from physical-only to the full ten-type vector | per-record declared gap, counted |

**Reader law:** `E3.winner()` — whole-record replacement (`L-33` / `C-9` overlay law), never `merged()`.
**Wave-array law:** fighting wave `w` reads the cell **labelled** `w`, index `w−1`.
**Rank law:** over-range array indexing clamps to the last authored cell and the row says so.

---

## § 4 — STANDING DO-NOTs INHERITED, AND THE ONES THIS LAP ADDS TO ITSELF

Lap V § 7.2, Lap V-2 § 11.2 and Lap W § 7.2 DO-NOT blocks **remain binding in full** and are carried
forward unchanged. `NOTE D-V2-1` is honoured: the Lap-S PE reader's export map collides
vtable-symbol RVAs, so **no vtable base from it is trusted**; any binary corroboration in this lap
is by string/immediate/xref evidence, is labelled CORROBORATION and never CARRIES a magnitude alone.

This lap binds itself additionally:

* **DO NOT let any referent number enter a decoded value.** § 5 is a grading surface. If a decoded
  quantity would need a referent number to be computed, it is UNREACHED, not estimated.
* **DO NOT model proc uptime.** Not here. I-23's.
* **DO NOT report `P-X-3` as a discovery.** It is prereg-sighted (§ 0.2).
* **DO NOT collapse the § 2 `P-X-4` fork by grade.**

---

## § 5 — THE GRADE SURFACE (referent-derived observables; quarantined)

| id | observable | value | source |
|---|---|---|---|
| **`G-1`** | wave 151 duration, terminal | **16.0 s**, CLEARED | Lap C `measured-reference-truth.csv` |
| **`G-2`** | the referent survived the band at high health | mean HP **0.932**, full-health dwell **1.6166 s** | charter T4a / T4b(b) bands |
| **`G-3`** | referent concurrent living bodies at w151 | **19–36, median 25** (a LOWER bound) | charter / I-22 § 4 |
| **`G-4`** | implied referent kill rate at w151, from the decoded 28-body roster and `G-1` | **28 / 16.0 = 1.75 bodies/s** | derived from `G-1` + the decoded roster; **derived, not measured** |
| **`G-5`** | player declared pool / regen | **20,005 HP** / **129.38 HP/s** | Lap A sheet |

`G-4` is arithmetic on `G-1` and a decoded roster count. It is labelled DERIVED and it grades
`P-X-2b` only.

---

## § 6 — DELIVERABLES

`pm4x_findings.md` · `pm4x_prediction.json` (hashed **before** the grade is computed) ·
`pm4x_grade.json` · `pm4x_player_defense.json` · `pm4x_player_armor_pieces.csv` ·
`pm4x_monster_offense.csv` · `pm4x_monster_resist_reduction.csv` ·
`pm4x_intake_w151.csv` · `pm4x_ttk_by_body.csv` · `pm4x_formulas.json` · `pm4x_digests.json`.

Instruments under `agentic_orchestration/research/scripts/`:
`pm4x_decode_2026_08_15.py` (pins, formulas, player side, monster census) and
`pm4x_grade_2026_08_15.py` (predictions → grade, gated on re-hashing `pm4x_prediction.json`).

---

*Preregistered by legolas (UNKNOWN-RESEARCHER), 2026-08-15, before any Lap-X instrument existed.*
