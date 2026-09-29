# C-6 · `OPEN-UNKILLABLE` — a FOURTH cause LOCATED and SIZED, plus two corrections to the run's own record

**Commission:** C-6, issued KP-84 (seal lap W1, seat legolas). Conductor: gandalf.
**Mode:** UNKNOWN-RESEARCHER / primary-source probe. **Date:** 2026-09-28.
**Law 3 governs inside this commission.** No value here is fitted, back-solved or reconstructed.
Every number is either read from bytes on disk or arithmetic over numbers read from bytes on disk,
and each is labelled which.
**Read-only throughout.** No archive, pack, save, cell or footage file was written or moved.
**Disk at open 44 GiB / at close 44 GiB** — above the L4 HALT floor of 40 GB.

---

## 0 · HEADLINE

**PARTIALLY LOCATED.** A fourth cause is found, sourced to the game's own bytes, and **sized at
×1.83**. It is not sufficient: it accounts for a factor of 1.83 against a measured surplus of
~132×/29×, so `OPEN-UNKILLABLE` **stays open and narrows again.**

| # | finding | status |
|---|---|---|
| **F-1** | ⚑ **The Crucible's own per-wave monster DAMAGE multiplier is absent from the pack and from the port's damage chain.** `M_inst(w) = ×1.82…×1.85` over waves 151–170 (×1.830 at w160). The oracle folds it (I-6, 2026-08-13); the pack never publishes it; the port therefore resolves monster damage at **vendor strength**. | **LOCATED · SIZED ×1.83 · NOT SUFFICIENT** |
| **F-2** | The **nine campaign-attack records** cannot be the cause — **the sign is wrong.** | **EXCLUDED BY DIRECTION** |
| **F-3** | ⚑ The undocumented `132×` is the **MEDIAN of the 25 T-A cells**, re-derived exactly. The run's `132 ÷ 3.754 = 35×` is sound and now has a basis. | **CORRECTION — GAP CLOSED** |
| **F-4** | ⚑ **The 25 T-A cells are 5 distinct sustain outcomes replicated across 5 arms.** On the leech/intake dimension the arms are **degenerate**. An `n=25` claim here is an `n=5` claim. | **CORRECTION — FLAGGED, NOT RULED** |
| **F-5** | The leading **unexcluded** candidate is the corpus's own `U-P-N-3` (per-body vs per-swing leech, no target cap). It is **UNDECIDED in the corpus by the corpus's own words** and I do not decide it. | **NAMED · NOT CLAIMED** |
| **F-6** | Mean bodies-in-disc — the quantity `U-P-N-3` turns on — is **NOT ON DISK**. Searched. | **SOURCE-UNLOCATED (SEARCHED)** |

**And a correction to the commission as issued.** The brief describes the boundary as *"some
monsters are effectively unkillable (~30× the expected time-to-kill)."* That is not the thread.
`OPEN-UNKILLABLE` is a **PLAYER** surplus: the port's player heals ~29–132× the damage the board
does to him. Named at source — `kc2_play/src/kc2p_card.gd:43` (*"A ~29x leech surplus"*),
`kc2rt_fight.gd:1830` (*"A green T-A is compatible with an unkillable player"*). The research below
is against the real boundary. Recording the discrepancy because a commission aimed at the wrong
object cannot fail honestly.

---

## 1 · THE BOUNDARY, RESTATED FROM SOURCE

`leech_over_intake`, computed at `reincarnated-godot/kc2_runtime/sim/kc2rt_fight.gd:1846`
inside `sustain_report()` (`:1832`), as `leech_total / intake_total`.

Prior state of the thread (charter `KP-56`/`KP-57`, engine math note
`simulation/math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md:415`) — the surplus **survives**:

1. a wired `V1-JOIN-1` leech-resistance join (×3.754);
2. ×1.620 armed bodies from the v3.4 roster re-base;
3. bodies dying before they swing (refuted: 426–458 swings LANDED per cell).

**This commission adds a fourth, and it is none of those three.**

---

## 2 · F-1 — THE CRUCIBLE'S PER-WAVE DAMAGE MULTIPLIER IS ABSENT FROM THE PORT

### 2.1 · The primary source, re-derived from the depot bytes today

`~/Games/vendor` **does not exist** (KP-57's finding re-verified this session — Ed-III and Ed-II
trees both gone). `/Users/admin/depots/` is the only readable game substrate: 8 archives, manifest
`24346246`. Read with `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`
(`ArzArchive`), read-only.

**`records/game/survivalinfo.dbr`** — held by `base` (1 field, a template name) and **overridden by
`sm_mod`** (`/Users/admin/depots/483840/24346246/mods/survivalmode/database/SurvivalMode.arz`,
sha256 `e55b760f36ab80a6ad16fd34f3f8ca76e1cde55ee6160d72eb574c01221405f2`) with 14 fields, three of
which name the Crucible's own enemy adjustments:

```
survivalAdjustmentNormal   = records/game/balancingadjustment_survivalmode_enemies01.dbr
survivalAdjustmentElite    = records/game/balancingadjustment_survivalmode_enemies02.dbr
survivalAdjustmentUltimate = records/game/balancingadjustment_survivalmode_enemies03.dbr
```

All three are held by **`sm_mod` alone** and carry **200-entry per-wave arrays**. The referent is
Crucible/**Ultimate**, so the record of interest is `…_enemies03.dbr`. Read at index `wave−1`:

| field | w151 | w160 | w170 | w200 |
|---|---:|---:|---:|---:|
| `offensiveTotalDamageModifier` | 42.0 | **43.0** | 45.0 | 130.0 |
| `characterLifeModifier` | 306.0 | **324.0** | 344.0 | 990.0 |
| `characterAttackSpeedModifier` | 11.0 | **11.0** | 11.0 | 13.0 |
| `characterDefensiveAbility` | 61.0 | **67.0** | 74.0 | 95.0 |

Second component, `records/game/balancingadjustment_mp+difficulty_enemies01.dbr` (held by `base`),
12-slot array = 3 difficulties × 4 player counts; **index 8 = Ultimate / 1 player**:
`offensiveTotalDamageModifier = 40.0`.

**`M_inst(160) = 1 + (43 + 40)/100 = 1.830`.**

### 2.2 · Instrument validation — FIVE independently-pinned engine values, all EXACT

My extraction was checked against figures the engine derived on other laps, before I looked:

| pinned in | claim | my probe | |
|---|---|---|:--:|
| `simulation/AGENT_STATE.md:2992` | wave-160 `characterLifeModifier` = **324** | `[159] = 324.0` | ✓ |
| `simulation/AGENT_STATE.md:2992` | wave-160 `characterDefensiveAbility` = **67** | `[159] = 67.0` | ✓ |
| `simulation/AGENT_STATE.md:2992` | wave-160 `offensiveTotalDamageModifier` = **+43** | `[159] = 43.0` | ✓ |
| `simulation/AGENT_STATE.md:2992` | fighting 200 reads **990 / +130** | `[199] = 990.0 / 130.0` | ✓ |
| pack `monster_kinematics.json` `V4-ASMULT-1` | attack speed **+11.0 @ 151–170** | `[150…159] = 11.0` | ✓ |

Five for five, byte-exact. The instrument is sound before it is used on the open question.

### 2.3 · The derived table already exists, in the engine, and I wrote it

`reincarnated-engine/data/kc2/pm4i_wave_damage_modifier.csv`
(sha256 `f0852cec35a0362c101618b2a269446c4fba658ee0b80821aa5e4ae47eab910b`, 51 lines) — my own Lap-I
emission, 2026-08-13. Column `sum_total_damage_modifier_pct`: **82.0 @ w151 · 83.0 @ w160 · 85.0 @
w170**. Its `basis` column names exactly the two records above, including the `[index wave-1]` and
`[index 8 = Ultimate/1-player]` selections I re-derived independently today.

The oracle consumes it: `simulation/kc2/offense.py:399`
`instant_mult = 1.0 + self.sum_total_pct / 100.0`, asserted `== 1.830` at wave 160 by
`simulation/scripts/gamora_kc2_pm4_i6_offense_fold_2026_08_13.py:554`. `simulation/MIGRATION.md:3390`
states what the fold repaired: *"Until I-6 every monster damage magnitude this simulation resolved
was the raw skill-record value at the body's rank — the Crucible's own per-wave
`offensiveTotalDamageModifier` and the Ultimate difficulty pak's `[8]` cell had never multiplied it
… their **weapons** were at vendor strength until now."*

### 2.4 · ⚑ THE PACK DOES NOT PUBLISH IT — AND IT PUBLISHES A SIBLING COLUMN OF THE SAME CSV

Pack of record:
`reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p3-20260921_022612`
(the path hard-coded at `kc2_runtime/tests/kc2rt_t0.gd:29` and `kc2rt_ta.gd:49`).

Whole-pack case-insensitive grep over `model/*.json` + `manifest.json`:

| token | hits | what they are |
|---|---:|---|
| `total_damage_modifier` | **0** | — |
| `totalDamageModifier` | 5 | 4 = the PLAYER's Vanguard Banner (`arena.json`, `V14-BANNER-1/2`, `V14-INERT-1`); 1 = a binary-decode rule (`math_rules.json`, `D7-3-01`). **None is the monster per-wave term.** |
| `balancingadjustment` | 2 | both `summons.json`, both the **pets** pak, both graded `UNDERIVABLE-WITH-PATH-NAMED` |
| `wave_damage` | 1 | ⚑ `monster_kinematics.json` `V4-ASMULT-1` — see below |

⚑ **`V4-ASMULT-1` is the finding's sharpest edge.** It publishes the per-wave **attack-speed**
multiplier, `"+11.0 @ waves 151-170"`, `m = 1 + (D_characterAttackSpeedModifier_pct + U_…)/100`,
with provenance **`kc2/offense.py:374-396 … data/kc2/pm4i_wave_damage_modifier.csv`** — *the same
CSV*. **The pack ships one column of that file and not the damage column.** The port therefore
swings at the correct Crucible cadence with vendor-strength weapons.

And the pack's damage rows cannot carry it even in principle: `monster_offense.json`'s
`v21_monster_damage_row` grain is `(record_path, kind, slot, skill, damage_type)` — verified over
all 2,073 rows, the key set is
`{id, key, precedence, provenance, record_path, scope, unit, value{chance_pct, damage_type,
dot_duration_s, group, hi, kind, lo, magnitude, row_kind, skill, slot}}`. **No wave dimension
exists.** Provenance is `kc2/threat.py :: DamageRow from pm2_tg2_attack_damage.csv` — the PM-2
grain, upstream of the I-6 fold.

### 2.5 · And the port's damage chain confirms it, on the code path

`kc2_runtime/sim/kc2rt_fight.gd:1560–1615`, monster → player, in order:

`mag = r["magnitude"]` (the raw v21 row) → `× play_incoming_mult` (War Cry; **1.0 under `ORACLE`**)
→ percent-current-life reclamp → `× (1 − resist/100)` → armour (physical only) → counterplay →
`min(dmg, hp)`.

**No per-wave multiplier appears anywhere in the chain.** Corroborated by the port's own coverage
table, which declares it: `kc2_runtime/loader/kc2rt_coverage.gd:127`
`["D19", "PYTHON-ONLY", "global-magnitude fold"]`, and `kc2rt_census_map.gd:194-195`, where folding
"WHOLE rather than not at all" is described as a *capability v3.3 now permits* — i.e. not yet done.

### 2.6 · What it is worth, stated honestly

Intake is short by a factor of **1.83** at wave 160 (1.82–1.85 across 151–170). Restoring it
**divides the surplus by 1.83**: 132.69 → 72.5, or the post-`V1-JOIN-1` ~35× → ~19×.

⚑ **It is a real, sourced, previously-unexcluded fourth cause, and it is not the answer.** Roughly
an order of magnitude remains.

**Separately and smaller:** the I-14 "global-magnitude fold" (`D19`, also `PYTHON-ONLY`) is worth
**×1.116 board-wide** on intake — but **×1.000 at waves 159 and 160**
(`simulation/math/kc2-pm4-i14-global-magnitude-2026-08-14.md` § 4.4, a table of 20 waves). It is a
term the port owes; it is not material at the waves that decide this.

---

## 3 · F-2 — THE NINE CAMPAIGN-ATTACK RECORDS ARE EXCLUDED BY DIRECTION

The hand-off (`skill_handoff_2026-09-24.md` § 4.2) names them as *"the right shape to test
`OPEN-UNKILLABLE` against."* Tested: **the sign is wrong.**

Those nine carry campaign attacks **the Crucible strips**, *"in the direction that makes the board
**harder** than the referent"* (§ 4.2, verbatim). The shipped pack is therefore already **too
generous with intake** on those nine — and the port is unkillable anyway. Re-lifting them under
CRUCIBLE precedence (the KP-84 conductor ruling) **removes** attacks, **lowers** intake, and
**raises** the surplus.

**So the nine cannot explain the surplus; correcting them makes it worse.** The re-lift is right on
provenance grounds and should proceed — it just must not be booked as progress against C-6.
*(Whether the v3.4 cut still carries them is gamora's W1(b) determination; this finding is about
direction, not presence, and holds either way.)*

---

## 4 · F-3 + F-4 — TWO CORRECTIONS TO THE RUN'S OWN RECORD

I re-derived `leech/intake` from the T-A cell bytes:
`reincarnated-godot/tmp/kc2/ta/<arm>/<cell>/cell.json`, as
`sum(intake_by_wave.values())` against `leech_total`, 25 cells, all at pack digest `1b2dc13403ba`.
*(Provenance caveat: this tree is under `tmp/` and is **UNCOMMITTED-ON-DISK**. It is re-walkable
today; it is not durable evidence, and a re-emission would be needed to make it so.)*

| | ratio |
|---|---:|
| min | **73.42** |
| max | **176.87** |
| **median** | ⚑ **132.69** |
| mean | 128.32 |

**F-3 — the `132×` is the MEDIAN, and it is exact.** `gamora/notes/2026-09-21-kc2-play-ta-grade.md:598`
computes `132× ÷ 3.754 = 35×` and the `132` is stated there without derivation. It is the median of
the 25 cells, to two decimals. **min/max also reproduce the note's published `73× – 177×` band
exactly.** The `~35×` therefore rests on a sound basis and that basis is now written down.

**F-4 — ⚑ the 25 cells are 5 distinct sustain outcomes, replicated.** Measured:

- `M0` and `M-POL-2-NULL` are **bit-identical** on intake and leech across all five salts
  (176.87 / 146.40 / 165.52 / 96.14 / 155.93).
- `M-POL-2`, `W1` and `W1-NULL` are **bit-identical** to each other across all five salts
  (132.69 / 161.56 / 106.96 / 73.42 / 100.81).

So on the leech/intake dimension the five arms collapse to **two groups of five distinct cells**.
The median `132.69` is the middle of **five** values, not twenty-five.

This may be entirely expected — if the arms differ only in terms that do not enter leech or intake,
degeneracy is correct behaviour, not a defect. **I am not ruling it.** What must not stand is an
`n=25` confidence on a quantity with `n=5` of independent variation. **Routed to jack-ryan and
gamora as a measurement-width question**, with the disposition owed either way (an expected
degeneracy recorded as expected is still a disposition; silence is not).

---

## 5 · F-5 + F-6 — THE LEADING UNEXCLUDED CANDIDATE, NAMED AND NOT CLAIMED

The surplus's numerator does **not** scale with damage dealt. Measured in the port:

- `kc2rt_fight.gd:1312–1407` — `_resolve_channel()` iterates **every body inside the disc** and
  accumulates `pool_leeched` **per body**;
- `kc2rt_fight.gd:1320-1321`, verbatim: ⚑ ***"NO TARGET CAP (MEASURED-ABSENT 4/4) — twelve bodies
  inside produce twelve hits."***
- `kc2rt_laws.gd:66-67` — the per-body portion is `min(%WD,1) · D_weapon`, **a constant per body**;
- `kc2rt_laws.gd:114-116` — `V1-LAW-13` per-tick cap is **MEASURED-ABSENT, asserted 0**.

**So heal scales linearly in bodies-in-disc, with no target cap and no per-tick cap.**

⚑ **The oracle carries a switch the port has no counterpart for.**
`reincarnated-engine/src/reincarnated/simulation/kc2/player_sustain.py:595-596`:
`#: U-P-N-3 sensitivity — one leech event per SWING rather than per body struck.` /
`aggregate_per_swing: bool = False`, applied at `:720-722` as `pool = pool / n_bodies`. It is marked
*"NOT the record"* — i.e. **undecided by default.**

And the corpus says so in its own words —
`agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-p-sustain-engine/pm4p_findings.md:451`:
***"The corpus declares nothing either way… If a future probe finds a per-swing aggregation, every
HPS @ N figure divides by N."***

**I do not decide it, and Law 3 forbids me to.** What I record is that it is the only candidate on
the table whose *shape* has the missing order of magnitude, and that its resolution is a decode
question with a named surface (the binary's leech application site), not a modelling choice.

**F-6 — and the number it turns on is NOT ON DISK. Searched.** `n_bodies` / `n_hit` is a local at
`kc2rt_fight.gd:1314`, incremented at `:1324`, and **never emitted**: the cell files carry
`leech_total`, `leech_per_tick_n` and `intake_by_wave` and **no bodies-in-disc aggregate at any
grain** (verified across the full key tree of `M-POL-2/0/cell.json`). The `twelve` in the code
comment is an *illustration*, not a measurement.

**So: `SOURCE-UNLOCATED`, SEARCHED.** Closing it costs one emission — **mean and distribution of
`n_hit` per channel tick** — and that single number would convert `U-P-N-3` from an undecided
switch into a sized term.

---

## 6 · SURFACES SEARCHED, INCLUDING THOSE THAT RETURNED NOTHING

| surface | searched | result |
|---|---|---|
| **oracle + pack** (read-only) | `offense.py`, `threat.py` constants, all 18 `model/*.json` + `manifest.json` | **POSITIVE** — F-1, and the `V4-ASMULT-1` asymmetry |
| **game on disk** | all 8 depot archives; 84k+ record paths enumerated; `survivalinfo`, all `balancingadjustment_*`, `combatformulas`, `gameengine` dumped | **POSITIVE** — the three Crucible adjustment records; five-way instrument validation |
| **the port** | `kc2_runtime/sim/`, `loader/`, `play/` | **POSITIVE** — the damage chain, `D19 PYTHON-ONLY`, the no-target-cap declaration |
| **T-A telemetry** | 25 `cell.json` | **POSITIVE** — F-3, F-4; **NEGATIVE** for F-6 |
| **`~/Games/vendor` Ed-III** | — | ⚑ **ABSENT.** Does not exist. KP-57's finding re-verified; `matt_to_do` T31 still open, still not blocking |
| **the save file** | **NOT SEARCHED** | Deliberate: the boundary resolved to a *monster-side* substrate term and a *port-side* omission. The save carries the player sheet, which `C-3` already mined (Seal of Annihilation). Named so the omission is a choice on record, not a gap. |
| **the footage** | **NOT SEARCHED** | Same reason. The mount was up; nothing in F-1…F-6 is answerable from pixels. ⚑ It *is* the right surface for `U-P-N-3` if a frame ever shows the health globe against a countable body count — **flagged as the cheapest next read if the emission in F-6 is not run.** |

---

## 7 · WHAT A DOWNSTREAM SEAT WOULD FOLD

**None of this is mine to fold. Routed, priced, not taken.**

| seat | item | note |
|---|---|---|
| **star-lord** (W1b cut) | Publish `sum_total_damage_modifier_pct` per wave as a pack row, from `data/kc2/pm4i_wave_damage_modifier.csv` — **the same file `V4-ASMULT-1` already cites.** | The pack cannot carry it on the v21 grain (no wave dimension); it wants a `per WAVE` row beside `V4-ASMULT-1`, which is the precedent shape. |
| **drax** (W2 runtime) | Apply `M_inst(w)` on the v21 magnitude at `kc2rt_fight.gd:1560`, and flip `D19` off `PYTHON-ONLY`. | ⚑ **A Discipline #12 semantic shift on the fight path** — it hardens every historical arm by ×1.83. It must not ride inside the pack-swap commit. *One change, one effect, one gate.* |
| **gamora** | The nine-records re-lift proceeds on provenance grounds, **but is not progress against C-6** (F-2). | Direction argued in § 3. |
| **jack-ryan** | F-4, the arm degeneracy, needs a disposition — including *"expected, and here is why."* | An `n=25` claim resting on `n=5`. |
| **conductor** | `U-P-N-3` is commissionable **today** under the Commission Rule (absence of knowledge, no symptom required). One emission closes F-6. | The named surface is the binary's leech application site. |

---

## 8 · WHAT THIS FINDING DOES NOT CLAIM

- It does **not** close `OPEN-UNKILLABLE`. ~19× remains after F-1, and I did not find it.
- It does **not** decide `U-P-N-3`. The corpus declares nothing either way and neither do I.
- It does **not** assert the port's monster damage is wrong by exactly 1.83 *in play* — 1.83 is the
  substrate term's magnitude at wave 160; what it does to a fight is gamora's measurement, not mine.
- It does **not** re-grade the `~35×`. F-3 supplies the missing basis for the `132`; the division
  was already correct.
- The T-A cell tree is `tmp/` and **uncommitted**. F-3 and F-4 are re-walkable today and are **not
  durable**. If they are to be relied on, they need a committed re-emission.

---

## 9 · RE-WALK

Every section above cites a path that exists on disk as of 2026-09-28. The four probe scripts are
scratch (session scratchpad, not committed); each is three lines of `ArzArchive` against the depot
paths named in § 2.1 and reproduces in under a minute. Depot archive sha256s were confirmed to match
the `_source_corpus` of my own 338/338 lift (KP-57 § E2.1, 8 of 8) — the bytes read here are the
bytes the run is already standing on.

**Signed:** legolas (UNKNOWN-RESEARCHER), seat W1, KC2-PLAY seal lap.
