# C-11c — the referent's PLAYER-SIDE defensive stack: what the oracle already folds, what it does not, and what that is worth

**Date:** 2026-09-30 · **Author:** legolas (UNKNOWN-RESEARCHER) · **Commission:** C-11c (KP-132),
issued by the KC2-PLAY conductor (gandalf) on the **REFERENT-v2** track after Matt ruled
*"Seal v1 with the gap declared."*
**Boundary:** after every sourced MONSTER-side correction the oracle takes **×3.17** the referent's
landed intake (w151–159; referent 1,605.6 hp/s, dies w160 at 29.0 s). Four monster-side
investigations (C-10, C-11, C-11a, C-11b) failed to close it and three pointed the wrong way. The
hypothesis under test: **is the surplus in the oracle's declared PLAYER-side absences?**
**Mode:** read-only. No sealed cell opened, re-run or moved. Nothing fitted (Law 3).
**Surfaces:** the oracle's own committed substrate (`simulation/kc2/`, the v3.6 pack's
`config_of_record.json`) · the Lap-C/Lap-X/PM4g measured sheets in `data/kc2/` · the Mac Edition-II
depot `.arz` (CRUCIBLE precedence KP-79, mods included) · the decompiled `survivalevent.lua` ·
galadriel's committed HUD extractions · the save parse.
**Tooling:** `legolas/scratch/2026-09-30-c11b-attrlineage/arz.py` (carried from C-11b, unchanged).

---

## 0 · VERDICT IN ONE PARAGRAPH

⚑ **The commission's premise is substantially FALSE, and correcting it is the first finding. The
oracle does NOT omit the referent's defensive procs — it folds nearly all of them.** The
`kc2/__init__.py` L18–22 declaration that motivated this commission is a **2026-08-08 spec-era
docstring that PM-3 (2026-08-12), I-4, D-6 and B-1/B-1r superseded and nobody amended.** Turtle
Shell (6,100 absorb / 8 s), Arcane Barrier (2,900 / 3 s), Menhir's Will, Resilience, Ascension's
30 % absorption clause, Fighting Spirit's schedule, Ulzaad's schedule and **War Cry's −29 % enemy
damage at its MAXIMUM 100 % uptime** are all live on the cell of record. ⚑ **Blessings are a
MEASURED ZERO** — Matt bought none in either sitting, and the sheet carries all four counterfactuals
stamped `[NOT PURCHASED - measured]`. **Tributes are the purchase CURRENCY, not a combat mechanic.**
What IS genuinely absent is narrower and I priced it: **(A)** the circuit-breaker poll repair, a
LIVE known-bad worth at most **×3.17 → ×2.67**; **(B)** the three Crucible beacons' enemy-facing
output, unfired because its PERIOD was never read, worth at most **×2.73** on its own and **×2.29**
composed with (A); **(C)** four allied 65,000-HP decoy bodies the oracle's board does not contain,
existence grade A and **diversion share UNLOCATED**; **(D)** two player mutators drawn from a pool
whose largest defensive entry is +20 % Armour. ⚑ **No single term is large enough, and all sourced
terms AT THEIR CEILINGS reach ×2.29, not ×1 — closing the gap needs ×0.315. C-11c is the FIFTH
sourced investigation to fail to close ×3, and the first on the player side.** ⚑ **And the mutator
layer points the WRONG WAY: of the fight's six mutators, four were MONSTER mutators, and the oracle
models none of them.**

| # | player-side mechanic | oracle state | direction | priced |
|---|---|---|---|---|
| — | Turtle Shell · Arcane Barrier · Menhir's Will · Resilience · Ascension absorb · Fighting Spirit · Ulzaad schedule | ⚑ **ALREADY FOLDED** | — | n/a |
| — | **War Cry −29 % enemy damage** | ⚑ **FOLDED at MAXIMUM uptime** (`WarCryLimb.COOLDOWN`, 7.5 s ≡ its own cooldown) | — | n/a |
| — | **Celestial blessings** | ⚑ **MEASURED ZERO — none purchased, both sittings** | none | **nil** |
| — | **Tributes / score rewards** | purchase currency only (5 tributes + 10,000 ironbits per defence) | none | **nil** |
| **A** | circuit-breaker poll point (`LifeMonitorLimb.MONITOR_ON_FLOOR` NOT installed) | ⚑ **LIVE KNOWN-BAD** (V0-KB-53) | DOWN | **≤ ×2.67** |
| **B** | 3 beacons' enemy-facing output (Inferno −14 % dmg · Deathchill freeze/slow · Stormcaller −10 res) | magnitudes MEASURED, **period UNREAD ⇒ does not fire** | DOWN | **≤ ×2.73** alone; **≤ ×2.29** with A |
| **C** | 4 defence bodies as decoys (65,000 life each, `defensiveTaunt 500`) | oracle board has **no allied bodies** | DOWN | existence **A**; share **UNLOCATED** |
| **D** | 2 player mutators (of 6; the other 4 are MONSTER) | OUT-OF-MODEL | DOWN (small) / **UP** for the 4 | **identities UNLOCATED** |

---

## 1 · WHAT THE ORACLE ALREADY FOLDS — the premise correction

The commission cites `reincarnated-engine/src/reincarnated/simulation/kc2/__init__.py` L18–22:

```
- **Devotion procs** (R-KC2-1(d) — envelope only; `devotion.py` models the ABSENCE and proves it)
- **Defense structures, blessings, mutators, tributes** (charter-excluded / OUT-OF-MODEL)
```

⚑ **That block is stale.** It is the 2026-08-08 KC2-SIM spec's declaration. Since then PM-3
built `defenses.py`, I-4 built `counterplay.py`, D-6 closed the Fighting Spirit and Ulzaad decodes,
and B-1/B-1r folded the sustain layer. The authoritative statement of what is and is not in the
model is **`sustain_procs.ROW_DISPOSITIONS`** (13 rows) plus the v3.6 pack's
`model/config_of_record.json`, and they disagree with the docstring.

**Folded, from `ROW_DISPOSITIONS` and `counterplay.load_kit()`:**

| row | state | what is folded |
|---|---|---|
| `menhirs_will` | IN_MODEL | LowHealth ≤ 33 %, 35 % instant heal, 120 hp/s for 10 s, cd 21 s |
| `resilience` | IN_MODEL | full rank-3 payload on a decoded schedule |
| `devotion_procs` | PARTIAL | **Turtle Shell 6,100 absorb / 8 s · Arcane Barrier 2,900 / 3 s · Tip the Scales' energy limb** |
| `ascension` | PARTIAL | **`damageAbsorption` 30 %**, 10 s / 24 s, greedy on-cooldown |
| `fighting_spirit` | PARTIAL | the full decoded schedule |
| `ulzaads_decree` | PARTIAL | the full decoded schedule |

**War Cry is the one I most expected to find missing, and it is the most completely folded thing in
the kit.** `counterplay.py:744-750` applies `offensiveTotalDamageReductionPercentMin = 29.0` to
every incoming event, and the v3.6 `config_of_record.json` row `counterplay.kit.warcry_limb` reads
`WarCryLimb.COOLDOWN (duration 7.5 s)` — duration exactly equal to the cooldown, i.e. **100 %
uptime, the upper limb.** The mitigation order is asserted verbatim
(`counterplay.py:811`): `raw → ×(1 − warcry) → K-1 turtle → K-2 barrier → applied`.
⚑ **There is no headroom here at all.** C-11's own FINDINGS confirm it from the other side: the
biggest killing burst is described as *"about 7 k landed after 80 % chaos resist **and warcry**"*.

**Correctly absent, unchanged:** Block (two-hander, three measured zeroes), Righteous Fervor
(dissolves), Retaliation (build rule — and C-11a's byte-decode then showed it has **zero
population** anyway).

**Defensive limbs genuinely NOT folded, all small:** Ulzaad's `defensiveProtection = +190` flat
Armour (`DECLARED-NOT-FOLDED` with mechanism named and price MEASURED by B-1r, routed C-B1r-1) and
Tip the Scales' `offensiveLifeLeechMin = 132` (a HEAL, not a landed-intake term, and it rides
outgoing damage against a model already running a 21 % ADCtH from a different decode).

---

## 2 · THE CRUCIBLE STATE OF THE REFERENT FIGHT

### 2.1 Blessings — MEASURED ZERO, and this is a searched negative already in hand

`data/kc2/pm3_measured_defence_sheet.csv` carries **four** blessings — Blessing of Ulo,
Empyrion's Guidance, Might of Amatok, Ulzuin's Pact — and every row of all four is stamped
`[NOT PURCHASED - measured]`. `defenses.py`'s own headline says it in one line:

> *"Matt bought **ZERO celestial blessings**."*

Corroborated independently on camera by the save parse
(`legolas/notes/2026-08-05-eorwarlguts-save-parse.md`: `survival-powerups-activated +0` in both
sittings) and by `legolas/notes/2026-08-07-pe6-crucible-wave-composition.md` G-6
(`survival-defense-built +4`, `powerups-activated +0`). ⚑ **There is nothing here to model.** Had
Ulo been bought it would have been worth +25 physical/pierce/chaos resist and +10 defensivePhysical
— materially large — but it was not bought, and inventing it would be exactly the fit Law 3 forbids.

### 2.2 Structures — four purchased, and the gap is a PERIOD, not a magnitude

Purchased (sheet, with video timestamps, all well before wave 151):

| # | purchase | record | t (s) | cost |
|---|---|---|---|---|
| 1 | Deathchill Beacon | `records/creatures/defenses/turret_ice.dbr` | 477 | 5 tributes + 10,000 ironbits |
| 2 | Stormcaller Beacon | `…/turret_lightning.dbr` | 484 | " |
| 3 | Inferno Beacon | `…/turret_fire.dbr` | 502 | " |
| 4 | Vanguard Banner | `…/banner_offense.dbr` | 510 | " |

**`defences = True` is armed on the cell of record** (V0-05, `DRIVER-OF-RECORD`). But of the sheet's
259 rows only **6 touch the player**, all on the Vanguard Banner's 8 m aura, and **all six are
OFFENSIVE**: `characterOffensiveAbility 80` · `…Modifier 4 %` · `offensiveTotalDamageModifier 100 %`
· `retaliationTotalDamageModifier 100 %` · `skillMaxLevel 2` · `skillTargetRadius 8`.
⚑ **Not one player-facing structure row reduces intake.** (Under `player_offense.banner_additive`
the live one is worth ×1.0319, not ×2.0, because the sheet already carries +3036 % physical.)

**The 28 enemy-facing rows are where the intake reduction lives, and they do not fire.**
`defenses.py:202-209` names this as *"THE LAP'S LARGEST DECLARED GAP, COUNTED"* and counts it on the
wire as `defence_output_slots_ungated`: the enemy-facing output is fully MEASURED but **the firing
cadence is UNREAD**, and GL-12 forbids borrowing a period, so *"a defence with no measured reuse
gate DOES NOT FIRE."* The refusal is correct. What is buyable is the period.

Magnitudes, verbatim from the sheet (`rank_used = 26`), all riders on the beacons' own attack skills:

| beacon | skill | enemy-facing effect |
|---|---|---|
| Inferno | `turretfire_fireblast.dbr` | ⚑ **`offensiveTotalDamageReductionPercentMin = 14.0` for 5.0 s**, `skillTargetRadius 5.0`; `offensiveFireMin 2340`; `offensiveSlowDefensiveReductionMin 381` / 3 s |
| Deathchill | `turretice_icebolt.dbr` | ⚑ **`offensiveFreezeChance = 50.0`, `offensiveFreezeMin 2.0–3.2 s`**; `offensiveSlowRunSpeedMin 35` / 5 s; `offensiveSlowOffensiveAbilityMin 145` / 5 s; `offensiveColdMin 1876`; explosion radius 2.0, 3 fragments |
| Stormcaller | `turretlightning_chainlightning.dbr` | `offensiveTotalResistanceReductionAbsoluteMin 10` / 3 s (OFFENSIVE — helps the player kill); `offensiveLightningMin/Max 1604/4284` |

⚑ **I read the three skill records and the three creature records from the depot. THE PERIOD IS NOT
A MISSING DATUM — IT IS A DIFFERENT DATUM, AND THE ORACLE ALREADY OWNS THE ROUTE TO IT.**

- The three skill records carry **no `skillCooldownTime`** (verified field-by-field,
  `SurvivalMode.arz`; classes `Skill_AttackRadius` / `Skill_AttackProjectile` / `Skill_AttackChain`).
- The three creature records carry **no `skillControllerName`** — no autocast controller exists.
- What they DO carry: `monsterClassification = Common`, `characterAttackSpeed = 1.0`,
  `characterBaseAttackSpeedTag = CharacterAttackSpeedAverage`, and the skill in **tree slot 3**
  (`skillName3`, `skillLevel3 = charLevel/4+1`) beside `passiveproperties_defense.dbr` (slot 1) and
  `armorbase03.dbr` (slot 2).

⚑ **That is structurally identical to every one of the 466 board records the oracle already times.**
The cadence of a `Monster` record's tree-slot-3 skill under the default attack loop is exactly what
`pm2_tg2_monster_timing.csv` / `pm2_tg2_attack_slots.csv` decode for the pool
(`character_attack_speed`, `basic_swing_period_s`, `num_attack_slots`, `time_between_attacks_ms`,
the `or_zero_fields` slot model). **The Lap-C sheet's grain was granted STAT effects from
`parameters_offensive.tpl`, which is why the period was not in it. The DBR corpus is not the
sheet.** So the largest declared gap in `defenses.py` is closable **by the oracle's own existing
machinery, with no borrowed constant and no invented period** — the beacons can be admitted to the
timing decode as four more records.

**Two caveats that must travel with any fold, and neither is adjudicable from what I read:**
1. **Position.** `defenses.py:253-264` seats the four defences on arena anchors by a D-1 rule
   (banner nearest the centroid, beacons taking the rest in purchase order, separation floor = the
   banner's own 8 m radius) — a **placement CONVENTION, not a measurement.** Inferno's 5 m and
   Deathchill's 2 m radii are small against the arena, so coverage is position-sensitive in a way
   the banner's tether was not. The real placement is in the footage and is **SOURCE-UNLOCATED**.
2. **Survival.** Each defence has `characterLife = 65,000`. Whether all four were still standing
   through w151–160 is a **footage** question I did not answer.

### 2.3 Structures as BODIES — the term I did not expect and cannot price

The four purchases are `Monster` records with **65,000 `characterLife` each** and
`passiveproperties_defense.dbr` granting `defensiveTaunt = 500` and 300–500 in every CC resistance.
**They are attackable bodies standing in the arena.** ⚑ **The oracle's board contains no allied
bodies at all; every monster's threat resolves to the player.** 4 × 65,000 = 260,000 HP of decoy is,
at the oracle's 5,098 hp/s, **51 seconds of intake** — set against a fight whose terminal is a 6.7 s
spike. **Existence is grade A. The diversion SHARE is SOURCE-UNLOCATED** and I will not estimate it:
it depends on GD's threat-target selection between a player and a taunt-resistant structure, which
I did not decode, and on the placement caveat above. ⚑ **I flag it as the largest UNPRICED
player-side term found by this commission, and as the one most likely to be worth a commission of
its own.** It is not in `ROW_DISPOSITIONS` in this form — `defense_structures` is listed as
`EXCLUDED — excluded by charter`, which reads as a statement about their OUTPUT, not about their
existence as bodies on the board.

### 2.4 Mutators — six were live, TWO were the player's, and the identities are unrecorded

Verified verbatim from the decompiled `survivalevent.lua`
(`legolas/scratch/2026-08-08-kc2-citation/lua/sm_mod/game/events/survivalevent.lua`):

```lua
-- SurvivalEvent_SelectMutators(), L325-356
if checkpointWave > 0 then rewardTier = math.floor(checkpointWave / 10) end
...
elseif rewardTier >= 15 then  mutatorCount = 6
-- SurvivalEvent_MutatorRandomizer(), L238-252
if mutatorCount >= 6 then  playerMutatorCount = 2
...
monsterMutatorCount = mutatorCount - playerMutatorCount
```

The referent ran **checkpoint 150** ⇒ `rewardTier = 15` ⇒ **`mutatorCount = 6`**, split
**2 player + 4 monster**. This matches galadriel's committed HUD extraction
(`galadriel/notes/2026-08-08-eor-followup-extraction.md` § 5): a **six-icon mutator row** at t = 684
(wave 151, sitting 2), geometry-measured at 55.4 px pitch, x = 1271…1549 — with the explicit note
that *"no hover text anywhere … the six are described by glyph, not named."* ⚑ **The identities are
NOT recoverable from any committed artifact, and selection is `math.randomseed(Time.Now())` per
run, so they are not reconstructible from the records either.** This is a **SEARCHED
SOURCE-UNLOCATED**, and the only surface that could close it is a frame of the MP4 with a hover
tooltip, which does not exist in the recording.

**What CAN be bounded is the pool.** I read all ten player mutators from the depot; the magnitudes
are **tier-invariant** (base ≡ `_e` ≡ `_u`, verified), so there is no Ultimate-tier ambiguity:

| player mutator | defensive payload | intake-relevant? |
|---|---|---|
| `armored` | `defensiveProtectionModifier +20` (a **percent** Armour modifier) | ⚑ **largest** |
| `blessed` | `defensiveAllMaxResist +2` | yes, tiny |
| `voidmarked` | `defensiveChaos +8`, `defensiveChaosMaxResist +8` | ⚑ **conditionally large — see below** |
| `aethermarked` | `defensiveAether +8`, `…MaxResist +8` | yes, narrow |
| `resilient` | `defensiveBleeding/Poison +8` and their MaxResists | yes, narrow |
| `vigorous` | `characterLifeMultModifier +12` | survivability, not intake |
| `mighty` · `ascended` · `accelerated` · `sprinting` | offence / utility only | **no** |

⚑ **Two draws from that list cannot produce ×0.315.** The best defensive pair available is
+20 % Armour and +2 max resist, against a kill mechanism C-11 characterises as a **12,278–35,944 HP
one-second spike** on a 20,005 HP player.

⚑ **ONE CONDITIONAL EXCEPTION, and it is the highest-value follow-up in this finding.**
C-11's FINDINGS names `chthonianherald_chaosblast` as the largest killing-burst mass —
*"35 k raw per blast, about 7 k landed after 80 % chaos resist and warcry."* If `voidmarked` was one
of the two drawn, chaos resist and its cap both rise 80 → 88, and landed chaos goes from 0.20× to
**0.12× of raw — a ×0.60 on all chaos intake.** ⚑ **I am NOT applying this**: whether `voidmarked`
was drawn is unknown (1-in-45 for a specific unordered pair from 10, uniform draw unverified), and
the chaos share of pooled landed intake is a number I did not read. **gamora can read that share
off her committed by-source column in one query**, and it would convert this from a named
possibility into a bracket.

### 2.5 Tributes — a clean negative

Tributes are the Crucible's **purchase currency** (5 tributes + 10,000 ironbits per defence, per the
sheet's own `tribute_cost` / `ironbits_cost` columns). They buy the structures and blessings priced
above; they have **no combat effect of their own**, and the save's tribute ledger is fully
reconciled (`legolas/notes/2026-08-05-eorwarlguts-save-parse.md`: sitting 1 flat 150 / zero debits;
sitting 2 held 125 / zero upgrades / zero blessings). ⚑ **There is no tribute mechanic to model. The
`tributes_score_rewards` row can be reclassified from `EXCLUDED — excluded` to `SEARCHED-ABSENT`.**

---

## 3 · THE ONE LIVE KNOWN-BAD ON THE PLAYER SIDE

`config_of_record.json` V0-KB-53, verbatim, and it is the only one of three census claims that
survives:

> **`known_bad.life_monitor_POLL_AT_SLOT`** — *"circuit breakers poll a POST-LIFT hp value, not the
> tick minimum, and measurably miss floor ticks (Turtle 51 vs 41 seen; Menhir 13 vs 10; in waves
> 151/153 the censored tick was the only sub-threshold tick, so the breaker was OFF entirely
> there)"* — status: **⚑ LIVE ON THE CELL OF RECORD.**

The repair limb `LifeMonitorLimb.MONITOR_ON_FLOOR` exists and is **NOT INSTALLED**
(`sustain_procs_fold = None`, V0-44). Its basis is the record field's own name —
`lifeMonitorPercent` on `skill_passiveonlifebuffself.tpl`, beside `thresholdDuration`
(*"Wait for life to be above threshold before starting duration timer?"*): **a field that must ask
whether life is above the threshold is a field on a MONITOR OF THE LIFE VALUE**, not a poll of a
post-heal sample. ⚑ **This is a sourced, decoded, already-built, direction-DOWN player-side
correction that the sealed cell does not run.** Of the three known-bads, the other two
(`warcry_I8_LEGACY`, `potion_I4_EXCURSION_MAX`) are `NOT-IN-CELL-OF-RECORD` — the driver overrides
both — so this one is the whole of it.

---

## 4 · PRICING, WITHOUT FITTING

**Basis:** gamora's committed C-11a-fold decomposition, ×3.175 pooled landed over w151–159 against
the referent's 1,605.6 hp/s ⇒ **oracle ≈ 5,097.8 hp/s**. Target ×1. **Required factor: ×0.315.**
Every figure below is a **CEILING** — the largest value the sourced magnitude can take — because a
ceiling that fails to close the gap is a stronger negative than a point estimate.

**Term A — install `MONITOR_ON_FLOOR`.** Only the absorb limb is a landed-intake term (Menhir's
heal is not). MEASURED: **10 missed Turtle Shell firings** over 917 ticks (× 0.0816 s = **74.83 s**),
salt 0 of the mech record cell. Ceiling 10 × 6,100 = 61,000 HP ⇒ **815.2 hp/s**.

> **×3.175 → ×2.667**

*Ceiling, because a 6,100 absorb pool only removes damage that actually arrives while it is up.
Measured on the mech record cell, not the C-11 pooled cell — same fixture, different arm.*

**Term B — fire the Inferno Beacon's debuff.** `offensiveTotalDamageReductionPercentMin = 14.0`.
Ceiling assumes it covers the entire attacking population continuously — which the 5 m radius makes
**certainly false**, and which is why this is a ceiling and not a fold.

> alone: **×3.175 → ×2.731**  ·  composed with A: **→ ×2.294**

Deathchill's 50 % freeze / 2.0–3.2 s and −35 % run speed / 5 s are **not priced**: both need the
period and the placement, and both are ceilings I would have to invent. They point DOWN.
Stormcaller's −10 resist is OFFENSIVE and does not touch intake.

**Term C — the four decoy bodies.** **UNPRICED.** Existence A; diversion share UNLOCATED.

**Term D — the two player mutators.** **UNPRICED** (identities UNLOCATED). Pool ceiling is +20 %
Armour + 2 max resist unless `voidmarked` was drawn, in which case a ×0.60 on chaos intake alone.
⚑ **The four MONSTER mutators point UP and the oracle models none of them, so the mutator layer's
NET direction is not even established as favourable.**

### The arithmetic that matters

| | landed hp/s | ratio |
|---|---|---|
| oracle, C-11a-corrected (committed) | 5,097.8 | **×3.175** |
| − Term A at ceiling | 4,282.6 | ×2.667 |
| − Term A + Term B, both at ceiling | 3,683.0 | **×2.294** |
| **referent (target)** | **1,605.6** | **×1** |

⚑ **Both sourced terms at their simultaneous maxima leave ×2.29. The gap does not close, and it does
not come close to closing.** Answering the commission's sub-question directly: **is any single one
of them large enough to matter?** Yes — A (×0.84) and B (×0.86) each individually exceed the ~5 %
threshold at which a term is worth folding, and C may be larger than both. **Is any large enough to
CLOSE the gap? No, and neither is their product.**

---

## 5 · WHAT gamora WOULD MODEL FOR REFERENT-v2

Ordered by (sourced × priced) and with the fold's grade attached:

1. ⚑ **Install `LifeMonitorLimb.MONITOR_ON_FLOOR`** (`sustain_procs_fold`). Already built, already
   decoded, already MEASURED-falsified in its incumbent form. **Grade A. ≤ ×2.67.** This is the
   cheapest correct move on the board.
2. ⚑ **Admit the three beacons to the timing decode** as four more `Monster` records and fire their
   tree-slot-3 skills on the oracle's OWN cadence model. **No borrowed period.** Carries two named
   caveats on every row: the D-1 placement is a CONVENTION, and beacon survival through w151–160 is
   unverified. **Magnitudes grade A; cadence derived by the oracle's own route; coverage declared.**
   **≤ ×2.73 alone, ≤ ×2.29 with (1).**
3. **Reclassify, don't model:** `blessings` → `SEARCHED-ABSENT (MEASURED ZERO, both sittings)`;
   `tributes_score_rewards` → `SEARCHED-ABSENT (purchase currency; no combat effect)`. Both are
   currently `EXCLUDED`, which understates what we now know.
4. ⚑ **Amend `kc2/__init__.py` L18–22.** It declares absent seven mechanics the package folds. A
   stale declaration that survives four laps of repair is Discipline #73 in its purest form — the
   state changed and the record did not follow — and **this commission was issued on the strength of
   it.** The docstring should point at `sustain_procs.ROW_DISPOSITIONS` rather than restate it.
5. **Route as new commissions, not folds:** **C-11d** the decoy-body diversion share (threat-target
   selection between player and structure; needs a `Game.dll` decode and the footage placement);
   **C-11e** the chaos share of pooled landed intake, which brackets the `voidmarked` conditional in
   one query against gamora's committed by-source column.
6. **Do NOT model:** the two player mutators (identities SEARCHED SOURCE-UNLOCATED, and
   reconstructing them would be exactly the fit Law 3 forbids); Ulzaad's +190 flat Armour beyond
   what B-1r already priced; Tip the Scales' leech (a heal, and it collides with the ADCtH decode).

---

## 6 · THE STANDING READ

⚑ **Four monster-side investigations and now one player-side investigation have failed to close
×3.** C-11b found the monster attributes were ~9 % LOW and its sourced fixes made the oracle MORE
lethal. C-11c finds the player's defensive stack was **already folded**, its two real absences are
worth at most ×2.29 between them at ceilings neither can actually reach, and the one layer that
remains genuinely unknown (mutators) was **two-thirds MONSTER-side** and therefore points the wrong
way as well.

**The honest conclusion this finding supports: the surplus is not a missing defensive mechanic.**
It is more likely in a term that is *present but composed wrongly* — the attribute limb's ρ 0.177
still dominates every ablation, and its scope and equation are byte-decoded while its **composition
with M_inst and the own-modifier at the total layer** remains the one place three separate
investigations have each declined to rule (C-11a's C3 HALTED; R3 and R4 routed, both direction UP).
⚑ **That is a composition question, not an acquisition question, and no further research commission
on my surfaces will answer it.** I record that plainly so the REFERENT-v2 track does not spend a
sixth commission on the same shape.

**Matt's seal ruling is unaffected and is, on this evidence, correct:** the declared gap
*"~×3 too lethal; player-side absences suspected"* should now read **"~×3 too lethal; player-side
absences SEARCHED and priced at ≤ ×2.29 combined ceiling; not the cause."**

---

## 7 · SOURCE LIST

**Primary — game data (Mac Edition-II depot, `~/depots/…/24346246/`, CRUCIBLE precedence KP-79):**
`SurvivalMode.arz` :: `records/creatures/defenses/turret_{fire,ice,lightning}.dbr`,
`banner_offense.dbr`, `records/skills/defenses/{turretfire_fireblast, turretice_icebolt,
turretlightning_chainlightning, passiveproperties_defense}.dbr` ·
`database.arz` :: `records/game/mutators/mutator_player_*.dbr` (10 × 3 tiers, read),
`mutator_monster_*.dbr` (17, enumerated only).

**Primary — decompiled script:**
`legolas/scratch/2026-08-08-kc2-citation/lua/sm_mod/game/events/survivalevent.lua`
L238-252, L325-356 (quoted verbatim, § 2.4).

**Primary — the save:** `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` (blessings,
tributes) · `legolas/notes/2026-08-07-pe6-crucible-wave-composition.md` G-6.

**Primary — the footage:** `galadriel/notes/2026-08-08-eor-followup-extraction.md` § 5, § 7.2
(six-icon mutator row, t = 684) · `galadriel/notes/2026-08-07-eor-sittings-extraction.md` L400-404.

**Oracle substrate (committed):** `simulation/kc2/{__init__,devotion,counterplay,defenses,
sustain_procs}.py` · `data/kc2/{pm3_measured_defence_sheet, pm4g_defensive_actives,
pm4g_consumables, pm2_tg2_monster_timing, pm2_tg2_attack_slots}.csv` ·
`legolas/notes/2026-08-15-kc2-pm4-lap-x-mitigation-decode/pm4x_defensive_procs.csv` ·
`output/kc2-model-pack-v3-E-s09-cp150-mech-v3p6-20260930_045353/model/config_of_record.json`
(V0-05, V0-44, V0-KB-51/52/53).

**Pricing basis:** `simulation/math/kc2-play-c11-oracle-lethality-decomposition-FINDINGS-2026-09-29.md`
§ 3, § 4 · `…-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md` (×3.175) ·
charter KP-124 → KP-132.

**Nothing in this finding was fitted, reconstructed, or taken from community description.**
Where a value was not recoverable it is marked SOURCE-UNLOCATED and left unpriced.
