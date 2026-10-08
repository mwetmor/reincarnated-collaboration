# Research: Grim Dawn crit roll rule (DECLARED-GAP D-L5), 2026-10-08

**Mode:** A (analytical; primary-source probe)
**Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf (JOIN-1 conductor)
**Scope:** read-only. The Grim Dawn binary was disassembled read-only from the vendored copy. No engine code was touched.
**Sources consulted:** the GD `x64/Game.dll` binary, build 24825149 (disassembled); `combatformulas.dbr` (already extracted); Crate's official combat guide; the Fandom wiki; Crate forum and Steam threads; prior legolas Lap B and Lap N notes. Full list in § 8.

**⚑ ERRATA, 2026-10-08:** jack-ryan's Gate-1 corrected five points, E-1 to E-5 (see § ERRATA). The roll rule stands. The intake PTH range is corrected (E-1). The § 4 worked example is a **lower-side** estimate against the referent footage (E-2).

---

## 0 · Verdict

**The roll is not any of M1, M2 or M3 as registered. It is M2's banded form with a wider roll range, and the crit-damage stat is added to the tier multiplier. There is no separate crit roll.**

```
ROLL = max(100, PTH) × u          u ~ U(0,1)   (continuous; Park–Miller 31-bit RNG, float32)
PTH  = max(probabilityToHitEquation(OA, DA), pthMinimum=55)      no upper clamp
if PTH < 100 and ROLL > PTH      -> MISS
elif PTH <= 70                   -> hit × (PTH/70)                  (no crit possible)
else multiplier = pthDamageModifier_i for the HIGHEST i with ROLL > pthThreshold_i, else ×1.0
crit  ⇔ multiplier > 1.0          (i.e. ROLL > 90)
on a crit: shown/applied multiplier = tier multiplier + Crit Damage%   (ADDITIVE)
```

For the player at PTH above 100, the roll runs over **(0, PTH)**, not (0, 100). So PTH above 100 does keep buying higher tiers and a higher crit share. The sealed M2 caps the roll at 100, and that cap is wrong for PTH above 100. With it, our board's player is stuck at "11 % at ×1.1". The decoded rule gives **13.1 % crit at DA 2770** and **27.9 % crit with tiers up to ×1.3 at DA 2011** (§ 4).

| Part of the rule | Confidence | Basis |
|---|---|---|
| Roll range `max(100, PTH)`, tier = highest threshold the roll exceeds | **HIGH** | Two independent PRIMARY sources agree exactly: the decompiled `Game.dll` and Crate's official guide. Community references match, and so does Lap N's footage tier shape. |
| One roll decides both hit and tier (no separate crit roll) | **HIGH** | PRIMARY (binary): a single draw `u` feeds a single function. |
| Same rule for players and monsters | **HIGH** for the roll function | PRIMARY (binary): there is no actor-type branch. The inputs can differ. |
| Crit Damage % is **added** to the tier multiplier, and only on tiers above ×1.0 | **MEDIUM-HIGH** | SECONDARY (several community sources) plus our own measured footage (Lap N lattice). **Not traced in the binary.** |

---

## 1 · Q1: How a crit is decided

### 1.1 PRIMARY: the shipping binary (build 24825149)

`/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/x64/Game.dll`. The appmanifest `buildid` is 24825149. sha256 `07775a29…529387` matches `MAC_SIDE_SHA256.tsv`. It was disassembled with capstone 5.0.7. The annotated listing is in `captures/game-dll-x64-disasm-excerpts.txt`, and the tooling is in `captures/re/`. The function names below are mine; the binary is stripped. Its own debug-log strings label each step.

1. **Loader** (func `0x109080`). This reads `records/game/combatformulas.dbr` into the CombatManager. `pthMinimum` goes to `+0x278`. Thresholds 1–6 go to `+0x280, +0x288 … +0x2a8`, and modifiers 1–6 go to `+0x284 … +0x2ac`.
2. **Constructor** (func `0x1087c0`) writes **`+0x27c = 100.0f`**. That is a hard-coded constant, not a DBR field. It is the roll-span floor. (It also writes `+0x278 = 66.0f`, the pre-DBR default for `pthMinimum`.)
3. **PTH** (func `0x10e490`; debug strings `PTH Offensive Ability %f / PTH Defensive Ability %f / PTH %f`). This evaluates `probabilityToHitEquation(OA, DA)` and clamps from below to `pthMinimum`. **There is no upper clamp.**
4. **Draw** (attack resolver `0x10a650`; melee site `0x10af5e`, plus ranged `0x10b3fa` and direct `0x10b716`). The seed step is `seed ← 16807·seed mod (2³¹−1)` (Park–Miller, Schrage form). Then `u = seed × 4.656613e-10`, ~~which is 1/(2³¹−1)~~ *(→ ERRATUM E-5)*. `u` is passed as the second float argument.
5. **Roll and tier** (func `0x10d810`; debug strings `PTH %f, Rand Value %f`, `PTH Random Number %f`, `PTH Missed Hit`, `PTH Uber Hit`, `PTH Modifier value %f`):
   - `ROLL = max([+0x27c]=100, PTH) * u`
   - if `PTH < 100` and `ROLL > PTH`: return 0.0 (**miss**)
   - if `PTH <= pthThreshold1 (70)`: return `normalPTHEquation` = PTH/70. (There is a 0.75 fallback constant if no equation is loaded; this is a pre-patch relic.)
   - otherwise compare `ROLL > thr6 (135)` → `mod6`, `> thr5` → `mod5`, … `> thr2 (90)` → `mod2`, else `mod1 (1.0)`. The tier index 0–5 is written to an out-pointer.
6. **Crit flag** (`0x10bfdd`). Crit counters increment iff the returned multiplier is greater than 1.0 (`xmm12` = 1.0f, verified). The value is logged as `criticalStrike = %f`.

The tier test does **not** check `PTH ≥ threshold` separately, and it does not need to. When PTH is below 100, a hit already means ROLL ≤ PTH. When PTH is 100 or more, ROLL < PTH by construction. Either way, the roll can only exceed thresholds the PTH also exceeds.

### 1.2 PRIMARY: Crate Entertainment's official guide

<https://www.grimdawn.com/guide/gameplay/combat/>, captured 2026-10-08 (`captures/crate-guide-combat.{html,txt}`), lines 226–241, verbatim:

> *Example: PTH = 97, 1-89 hits, 90-97 critically hits for 1.1x damage, 98-100 misses*
> *At PTH 100 and above, you cannot miss your target. At PTH 105+, you will begin to see the second tier of critical hits.*
> *Example: PTH = 107, 1-89 hits, 90-104 critically hits for 1.1x damage, 105-107 critically hits for 1.2x damage*
> *Example: PTH = 124, 1-89 hits, 90-104 … 1.1x, 105-119 … 1.2x, 120-124 critically hits for 1.3x damage*
> *Beyond the 6th threshold, you will no longer see higher critical hit values, but you will see critical hits more reliably.*

At PTH 107 and 124 the enumerated outcomes run from 1 to PTH, not 1 to 100. That is the same `max(100, PTH)` span the binary computes. The last sentence ("more reliably") is only possible if the span keeps growing past 135. Under a d100 roll nothing would change above PTH 100, and under M1 every crit would already be ×1.5.

The guide uses whole numbers for readability. The binary's roll is continuous, so the difference is under 1 percentage point (§ 5.2).

### 1.3 SECONDARY: the community agrees

- tqFan, *"Critical Hit / Resistance Calculators – DPS multipliers"*, Crate forum, 2020-02-06 (<https://forums.crateentertainment.com/t/critical-hit-resistance-calculators-dps-multipliers/95882>): *"possible results are 1 - 100 for PTH < 100 and 1 - PTH for PTH ≥ 100"*; *"Chance to critically hit is … (PTH − 89) / PTH"*.
- Raiyaz, *"Advanced Mechanics"*, Crate forum, 2015-07-21 (<https://forums.crateentertainment.com/t/advanced-mechanics/29059>): `CC = 1 − 90/max(100, PTH)`. This is the binary's formula exactly. **Caveat:** the same post uses obsolete 2015 thresholds (90/110/130/150/170 → ×1.25…×2.5), so cite it only for the span rule.

### 1.4 Corroboration from our own measurement (Lap N, 2026-08-14)

The Lap N footage decode (`legolas/notes/2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_findings.md`) read 148 crit floating-text events from the referent EoR Warlord run (waves 150–160):

| Tier | Share of crits |
|---|---|
| ×1.1 | 50.7 % |
| ×1.2 | 41.2 % |
| ×1.3 | 6.8 % |
| ×1.4 | 1.4 % |
| ×1.5 | 0 % |

- **Sealed d100 M2** predicts **100 % ×1.1**. Contradicted.
- **M1** predicts all ×1.5. Contradicted.
- **The decoded rule** predicts multiple tiers, falling off with height. Lap N read the tier densities as a PTH survival curve with median PTH ≈ 112. Our board's `p2m_pth_effective` median is **111.83** (95 monster rows, `data/kc2/pm4o_oa_da.csv`). ~~**INFERRED, but it is a strong independent match.**~~ *(→ ERRATUM E-2: the medians agree, the distributions do not)*

At the time, Lap N could not reconcile this with the old PTH figure of 149–182. `F-B1r-1` has since shown that figure was wrong, which removes Lap N's reading (i).

---

## 2 · Q2: How Crit Damage % combines with the tier multiplier

**Additive, and applied only to crits (multiplier above 1.0):** `crit multiplier = pthDamageModifier_tier + CritDamage%/100`.

| Evidence | Grade |
|---|---|
| Lap N footage: GD prints `(x1.67) (x1.77) (x1.87) (x1.97)`. That is exactly 1.1/1.2/1.3/1.4 **+ 0.57**, the sheet's "+57 %". There is a second family at +0.69. **No `x1.57`** (1.0 + 0.57) appears, and no multiplicative value like `x1.727` (1.1 × 1.57). | MEASURED game output (our decode). Splitting the total into tier + stat is INFERRED, but well corroborated. |
| Fandom wiki: *"Equipment and Skills granting +% Critical damage will be added to PTH Threshold multipliers … 1.25x damage (1.1 + 0.15)"* | SECONDARY (the page is stale elsewhere, see § 6) |
| Steam, 2018-02-04, *"Max crit multiplier has changed?"*: *"Crit damage bonuses are additive, so 1.5(1+.11+.15) = 1.89"* (DarkestLight); *"simply adds onto the base 1.10 - 1.50 crit multiplier"* (jbridso) | SECONDARY / tertiary |
| Crate forum, 2022-06-10, thread 114846: *"minimum pth crit 1.1+71 = 1.81"* (Gnomish_Inquisition). It also observes that a skill-specific crit-damage modifier did not apply to that skill's DoT ticks. | SECONDARY |
| Binary: the attribute class `DamageAttributeAbsMod_CritDamageModifier` and fields `offensiveCritDamageModifier` / `offensiveCritDamageGlobal` exist, and the resolver passes the tier multiplier into the damage-attribute loop. **I did not trace the addition itself.** | PRIMARY that the class exists; **the combination rule is NOT binary-verified** |

There are also **per-skill** crit-damage modifiers ("+15 % Crit Damage to Forcewave", per Crate's item-skills guide). These add only to that skill's hits. That fits Lap N's two families, +0.57 and +0.69: two damage sources with different crit-damage totals.

---

## 3 · Q3: Players versus monsters

**The roll function is the same for both.** There is one CombatManager with one set of thresholds and modifiers, and `0x10d810` and `0x10e490` contain no branch on actor type (PRIMARY, binary). Crate's guide also applies the 55 PTH floor to *"you or your enemies"* (PRIMARY).

Any asymmetry comes from the **inputs**: OA/DA, and crit-damage stats such as the per-wave `wave_crit_damage_modifier_pct` column already in `pm4o_oa_da.csv`.

~~On our board, monster PTH runs from 66 to 85, which is below 100, so the span question does not affect the intake lane (§ 5.2).~~ *(→ ERRATUM E-1)*

---

## 4 · Q4: Worked example, OA 3259 against the board

PTH is computed with the stored equation. Reproduce with `captures/worked_example.py`.

| | DA 2011.53 (lowest board DA) | DA 2770.09 (highest board DA) |
|---|---|---|
| PTH | **124.888** | **103.537** |
| Roll span | (0, 124.888) | (0, 103.537) |
| Miss | 0 | 0 |
| ×1.0 (ROLL ≤ 90) | 90/124.888 = **72.06 %** | 90/103.537 = **86.93 %** |
| ×1.1 (90–105) | 15/124.888 = **12.01 %** | 13.537/103.537 = **13.07 %** |
| ×1.2 (105–120) | **12.01 %** | 0 |
| ×1.3 (120–124.9) | 4.888/124.888 = **3.91 %** | 0 |
| ×1.4 / ×1.5 | 0 / 0 (PTH below 130) | 0 / 0 |
| **Crit chance** | **27.94 %** | **13.07 %** |
| E[tier ∣ crit] | **1.1710** | **1.1000** |
| E[crit multiplier ∣ crit], +57 % added | **1.7410** | **1.6700** |
| E[multiplier per hit], no crit damage | 1.04777 | 1.01307 |
| **E[multiplier per hit], +57 % crit damage** | **1.20701** | **1.08760** |

For comparison, the sealed M2 / J3a `gd-judged` value on this board is a flat 11 % at ×1.1, which gives E = 1.011 (or 1.0737 if +57 % were added). **The decoded rule is higher at every DA on the board.** At the low-DA end the per-hit expectation is about 19 % above the J3a judged value (1.207 against 1.011).

The pinned "damage per hit 43,691–59,761 non-crit" is a non-crit figure. The expected per-hit damage is that figure multiplied by the last row: **×1.088 to ×1.207 across the board**, if the global crit damage of +57 % is the right one for the hit source. Some sources carry +69 % (§ 2).

---

## 5 · What this means for the sealed laws (factual notes; the decisions belong to gamora, gandalf and jack-ryan)

### 5.1 Player lane (D-L5)
- The `CritLimb` bracket LO 1.0 / HI 1.5 does contain the decoded per-hit expectation, which is 1.013–1.048 for the tier alone and 1.088–1.207 including +57 %. Neither end of the bracket equals it.
- The J3a `gd-judged` value ("M2, 11 % at ×1.1") **is contradicted by both PRIMARY sources** for PTH above 100.

### 5.2 Intake lane (`threat.resolve_hit`, "Crate's published loop")
The docstring's label is accurate in form. Its d100 parameterisation differs from the binary in three ways:
- **Range when PTH ≥ 100.** The roll is capped at 100. ~~This does not bind on the current board, where monster PTH is 66–85.~~ *(→ ERRATUM E-1: the range is 77.15–99.98 and the cap misses binding by 0.02 PTH)*
- **Integer roll with `≥` instead of continuous roll with `>`.** The sealed hit chance is `floor(p)/100`, against the binary's `p/100`. Crit chance for p between 90 and 100 is `(floor(p)−89)/100`, against `(p−90)/100`. **Each difference is ≤ 1 percentage point.** Example: at p = 77.8 the sealed hit chance is 0.77 and the binary's is 0.778.
- **The sub-threshold boundary.** The binary applies PTH/70 when p ≤ 70; the sealed code uses p < 70. This makes no difference to any value.

Whether that ≤ 1 pp matters is not my call.

---

## 6 · Conflicts, kept separate

| Source | Says | Disposition |
|---|---|---|
| Fandom wiki *Game Mechanics* (`captures/fandom-game-mechanics.wikitext`) | Crit chance = PTH − 90 (out of 100); threshold-1 = 75; floor 60; *"x3.5"* max; tiers 4–6 marked "UNCONFIRMED" | **Stale.** It conflicts with the `.arz` (70/55) and the binary on every point it can be checked against. Lap B § 5 already flagged it. Its crit-damage additivity statement is the only part I use, and it is graded SECONDARY. |
| Raiyaz 2015 thread | Thresholds 90/110/130/150/170 → ×1.25…×2.5 | Pre-release constants. Its span formula matches the binary; its thresholds do not. |
| Sealed M2 (`threat.py:390–405`, J3a § 3.1) | Roll is d100 (1–100) | Contradicted by the binary and the guide when PTH > 100. |
| **Lap N apparent crit share** | Non-crit 87 against crit 57, so a crit share of at least 39.6 % (graded INDICATIVE) | **Unresolved tension.** Under the decoded rule, a single PTH of 135 or less gives at most 33.3 % crits. The 0 % at ×1.5 rules out higher PTH. So either the share is biased upward by OCR or attribution ~~(Lap N argued the bias runs downward)~~ *(→ ERRATUM E-3: that is an unverified assumption)*, or some sources print crits by another route. **I do not resolve this.** It does not affect the tier-shape agreement in § 1.4. |

---

## 7 · Knowledge gaps not resolved

1. **Crit-damage addition is not binary-verified.** Tracing it means following the tier multiplier (`[attack+0x9c]`) into the `DamageAttributeAbsMod_CritDamageModifier` virtual methods. That needs vtable/RTTI reconstruction. Next step if wanted: rebuild the class vtables from RTTI in `.rdata` and decompile the attribute's apply method.
2. **Whether DoT and bleed damage gets the multiplier**, and whether crit damage applies to the over-time component. The resolver logs `Absolute` and `Over Time` totals separately. A community report says skill crit damage did not reach DoT ticks. Not checked.
3. **Other paths that call the roll:** `0x48dd10` (a dispel skill) and `0x5135c0` call the same roll function with their own Park–Miller draw. The Retaliation and Reflection attack types never call it *(→ ERRATUM E-4: nor does Debuff Attack)*, which suggests they cannot crit. **INFERRED, not verified.**
4. **The Lap N crit-share tension** (§ 6).
5. **The RNG seed and stream**: the seed source and per-actor sharing are not examined. It does not matter for a distribution-level model.

---

## ERRATA — 2026-10-08 (after jack-ryan Gate-1, collab 7215b9bb3)

Source: jack-ryan, `agentic_orchestration/qa/findings/2026-10-08-join1-dl5-decode-gate1.md`, verdict GO-WITH-AMENDMENTS. He re-derived every PRIMARY claim independently, and the roll rule is unchanged. These errata fix the README's statements about **inputs** and **corroboration**. The original lines are struck through above and point here.

**E-1 · Intake monster PTH range (Gate-1 WARN-2). "66–85" was wrong.**
- The sealed intake lane at waves 151–160 reads `m2p_pth_effective` from `pm4o_oa_da.csv` (through `measured_board.pth_for`).
- That column runs **77.15–99.98**, with **55 of 95 rows in the crit band [90, 100)**. I re-checked this against the CSV: min 77.1484, max 99.9799, 55 rows.
- "66–85" is the sim's own dex-absent `effective_oa` fallback PTH, not the lane's input.

What still holds, per jack-ryan:
- The d100 range cap does not bind on this board. **The margin is 0.02 PTH, not about 15.**
- The difference between the sealed law and the binary stays within the "≤ 1 pp" stated in § 5.2. The maximum change is 0.984 pp in hit chance and 0.990 pp in crit chance.

What § 5.2 should have said:
- **The bias is one-signed.** Per swing, the sealed intake expectation averages **−0.58 %** against the binary (range −1.08 % to +0.10 %). That direction flatters the Warlord.
- **JOIN predicate:** `m2p` is keyed to the Warlord's DA of 2591. A joined kit with lower DA pushes these rows to PTH ≥ 100, where the d100 cap **does** bind. (The conductor records this.)

**E-2 · The Lap N tier-shape corroboration was overstated (Gate-1 WARN-1).**
- The two medians agree (about 112 against 111.83), but the distributions do not.
- Applied to the board's 95 player-PTH rows (103.54–124.89), the decoded rule predicts these shares among crits:

  | Tier | Board prediction | Footage |
  |---|---|---|
  | ×1.1 | about 0.59–0.64 | 0.507 |
  | ×1.2 | about 0.35–0.39 | 0.412 |
  | ×1.3 | about 0.014 | 0.068 |
  | ×1.4 | 0 | 0.014 |

- ×1.3 and ×1.4 together: **12 observed against about 2.1 expected**, Poisson P ≈ 2×10⁻⁶.
- ×1.4 requires PTH > 130, but the board's maximum is 124.89.

This does not threaten the rule; d100 M2 predicts 100 % ×1.1 and is falsified either way. It does show that **the realised in-run PTH sits above the board's static PTH**. Candidate causes are DA shred, temporary OA, or a higher-OA damage source (family B is one candidate).

jack-ryan's best two-point fit to the footage is 80 % at PTH 116.5 and 20 % at PTH 132. That implies a crit share of **22–27 %**, against **20.8–21.9 %** for the board-fed profile.

**⚑ So a board-fed decoded profile, including the § 4 worked example, is the LOWER-SIDE estimate relative to the referent footage.** AMENDMENT-2 (gamora) carries either the footage-implied PTH lift as a sensitivity, or a named input gap.

**E-3 · The Lap N crit-share bias direction is an assumption, not a measurement (Gate-1 INFO-4).**
- Lap N's claim that the 39.6 % share is biased only **downward** was never verified. FCT lifetime was measured only on crit strings.
- If crit text persists longer than non-crit text, snapshot sampling over-counts crits (length bias). There are other upward routes too: small-number filtering, and how confidence-1.0 OCR treats bare numbers against suffixed ones.
- **Re-grade: ASSUMPTION.** 39.6 % must not enter any calibration. The binary is direct evidence, and the footage share cannot override it.

**E-4 · § 7.3 missed one path (Gate-1 INFO-5).**
- **Debuff Attack** also never calls the roll. It reuses the stored multiplier.
- Separately, the resolver has **miss channels that run before the PTH roll**: `Fumble Chance … caused a miss`, `Defender Dodged Attack`, and `Defender Deflected Attack` (ranged). HIT_CHANCE = 1.0 at PTH ≥ 100 covers only PTH misses. Fumble debuffs or dodge reaching the Warlord would be a separate route.

**E-5 · RNG scale constant (Gate-1 INFO-6).**
- The float32 constant 4.656613e-10 is exactly **2⁻³¹**, not 1/(2³¹−1).
- So `u` lies in (0, 1], with P(u = 1) ≈ 3×10⁻⁸ and float32 granularity near 1.
- This has no effect at the distribution level.

---

## 8 · Sources (accessed 2026-10-08 unless stated)

**PRIMARY**
- Grim Dawn `x64/Game.dll`, Steam buildid 24825149, sha256 `07775a297050e84a846af1182731700614fb8b7bb41cca46b37fd24c90529387`. Functions `0x1087c0`, `0x109080`, `0x10e490`, `0x10a650`, `0x10d810`. Listing: `captures/game-dll-x64-disasm-excerpts.txt`.
- `records/game/combatformulas.dbr`, base archive, as extracted at `reincarnated-engine/data/kc2/pm2_hit_math_constants.json` (Lap B).
- Crate Entertainment, *Grim Dawn Game Guide: Combat*, <https://www.grimdawn.com/guide/gameplay/combat/> (`captures/crate-guide-combat.*`); also the `character-basics`, `item-skills`, `crucible` and `monsters` guide pages (`captures/crate-guide-*`).

**MEASURED (our own decode of game output)**
- legolas Lap N, `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_findings.md` + `pm4n_crit_multipliers.csv`.

**SECONDARY / tertiary**
- tqFan, Crate forum t/95882 (2020-02-06).
- Raiyaz, Crate forum t/29059 (2015-07-21). Zantai posts in the thread, but not on the crit formula.
- Gnomish_Inquisition and wizcacha, Crate forum t/114846 (2022-06-10). No developer post.
- DarkestLight, jbridso and Geek, Steam discussion 1699415798772378312 (2018-02-04). No developer post.
- Grim Dawn Fandom wiki, *Game Mechanics*, via the MediaWiki API (`captures/fandom-game-mechanics.wikitext`).

**Not captured:** the Crate forum's JSON endpoint rate-limited anonymous requests (*"performed this action too many times"*). The forum threads were read through WebFetch summaries, so the quotes above are as returned by that fetch, not byte captures. No developer statement on crit-damage additivity was found.
