# KC2 — Consolidated record-arithmetic touch (nine items, one web)

**Status:** COMPLETE — 9 / 9 closed, 0 dead-ends
**Date:** 2026-08-08
**Author:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (`RUN-CONDUCTOR`), KC2-SIM autonomous run, fold L-64, ruling **R-L64-3**
**Ledger:** `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` rows L-61 → L-64
**Grade tags (R-KC2-7):** MEASURED (read from records / read from footage) · DERIVED (arithmetic on
MEASURED inputs, no free parameter) · INFERRED (structural argument) · No silent estimation anywhere.

---

## 0. Headline

> **The ×2.7181 residual does not exist.** It was the artefact of dividing by a `×4.08` that never
> multiplied. The w152 enemy-life stack is **additive-within-field**, and its missing term is a
> **level-indexed passive** — `armorbase0N.dbr` carries `characterLifeModifier` as a 200-element
> array indexed by *skill rank = charLevel*. At charLevel 108:
>
> ```
> Σ = 580  (balancingadjustment_mp+difficulty_enemies01 · Ultimate · players 1)
>   + 308  (balancingadjustment_survivalmode_enemies03  · characterLifeModifier[wave-1] @ w152)
>   + 121  (armorbase03/05.dbr · characterLifeModifier[charLevel-1] = [107])
>   = 1009 %   ⇒   ×11.0900
> ```
>
> **maxHP = characterLife_eq(charLevel) × (1 + Σ/100)** reproduces **11 of the 12** wave-152 census
> fingerprints EXACTLY (worst residual **+0.0021 %**), including both members of the low pair.
>
> **B-KC2-C1 is CLOSED, not merely unblocked.** The pair-seat is SEATED: `42,798 ×4` and
> `43,548 ×3` are `swampcrab_a00_summon` — **Ugdenbog Crablings at charLevel 107 and 108** — exactly
> as galadriel's plate read and exactly as her monotone within-set inference proposed.

Second-order, and it is the one that cost the run two folds: **the record `charLevel` additive
offset (`charLevel*1+5`) does NOT enter the spawn level.** Rotmouth's 109/110 prediction failed on
that link, `averagePlayerLevel = 100` fell with it (it is **[103.0, 103.92)**), and the old ratio
bands were too *narrow*, not too wide.

---

## 1. Substrate, instruments, provenance

**Corpora.** Every record read this touch was read from **GD-Edition-II**
`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (the fixture substrate — both KC2 sittings
predate the patch). Every path used was additionally confirmed present and **IDENTICAL** in
**GD-Edition-III** `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` by the L-61 diff and
re-confirmed by this touch's `kc2set_verdicts_v2.json` (613 IDENTICAL / 5 CHANGED / 9 ABSENT).
Localization tags (§ 8) were read from **both** trees and agree 8/8.

**Prior notes (mine).** `2026-08-08-kc2-edition-III-intake-and-diff.md` (§ c.0 self-flag; corrigenda
banner added this touch) · `2026-08-08-kc2-w152-w157-generator-join.md` (§ 3.3/3.4 re-run target;
corrigenda banner added this touch).

**New measured input.** `galadriel/notes/2026-08-08-kc2-crabling-rotmouth-touch.md` — read in full.
Not edited.

**Instruments** (all new this touch, in `legolas/scratch/2026-08-08-kc2-ed3-diff/`, all READ-ONLY):

| script | what it does |
|---|---|
| `d1_crab.py` | crab-summon body inventory |
| `d2_tags.py` | display-string → localization tag → record, both trees (→ `tags_all.json`) |
| `d3_levelchain.py` | lv-proxy formulas · hero/boss pool records · per-record `charLevel` |
| `d4_wavelevel.py` | hunt for a Crucible level term in the survival arrays — **none exists** |
| `d5_summoners.py` | who can spawn the crabling; every pool carrying each hero record |
| `d6_c1.py` | B-KC2-C1 first pass (two-anchor residual comparison) |
| `d7_join.py` | census → record join at a trial multiplier |
| `d8_pin.py` | multiplier pinned from exact hits; corpus-wide exact join |
| `d9_exact.py` | **charLevel-108 uniqueness solve**; exact join for all 12 fingerprints |
| `d10_armorbase.py` | **the +121 % term** — level-indexed passive `characterLifeModifier` |
| `d11_solve.py` | the solved life model, verified against six bindings |
| `d12_census.py` | full w152 census join + hero-offset falsification (→ `w152_fingerprint_levels.json`) |
| `d13_apl.py` | `averagePlayerLevel` solved from the resolved level structure |
| `d14_bands.py` | **item 1** — corrected ratio bands + § 3.4 re-verdict |
| `kc2set_v2.py` | **item 7** — verdict artefact re-emit (→ `kc2set_verdicts_v2.json`) |

---

## 2. ITEM 1 — § 3.3 / § 3.4 re-run — **COMPLETE. The dead gap does not exist.**

Two errors compounded in the original derivation, and the one I self-flagged was the *smaller* one.

| # | error | direction |
|---|---|---|
| **E-1** | § 3.2 censused the `charLevel` **multiplier** and missed the **additive** term (1,132 / ~3,115 records carry offsets −1…+6). My own flag, intake note § c.0. | narrows the bands |
| **E-2** | The multiplier stack was modelled as **level-independent**. It is not. Every monster carries `skillName3 = armorbase0N.dbr`, whose `characterLifeModifier` is a **200-array indexed by skill rank**, and `skillLevel3 = charLevel*1`. A same-record ΔL = 1 step therefore moves the **multiplier** as well as the base. | **widens** the bands — and dominates |

**E-2 dominates**, so the published bands are not "overstated" (as § c.0 predicted) — they are **too
narrow**. MEASURED array excerpt (`records/skills/nonplayerskills/passive/`, Edition-II):

| index | 100 | 101 | 102 | 103 | 104 | 105 | 106 | **107** | 108 | 109 | 110 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `armorbase01/02` | 56 | 61 | 69 | 74 | 82 | 88 | 96 | **102** | 110 | 110 | 114 |
| `armorbase03/04/05/06` | 63 | 70 | 78 | 86 | 94 | 103 | 111 | **121** | 125 | 125 | 129 |

### 2.1 Corrected bands — **DERIVED**

w152 roster + one-hop summon bodies, level-scaling records only, charLevel 102–108
(the DERIVED admissible band, § 5.3):

| ΔL | published § 3.3 Branch A | **CORRECTED** (w152) | **CORRECTED** (w157) |
|---:|---|---|---|
| 1 | 1.181 % … 1.519 % | **1.595 % … 2.329 %** | 1.595 % … 2.321 % |
| 2 | 2.364 % … 3.046 % | **2.833 % … 4.543 %** | 2.833 % … 4.527 % |
| 3 | 3.550 % … 4.580 % | **4.449 % … 6.923 %** | 4.449 % … 6.899 % |

*(Including constant-life records — traps, some proxies — drops the floor to 0.000 % on all three
rows. Reported separately rather than folded in: a constant-life record has no level step, so its
0 % is a true value of a different question.)*

### 2.2 § 3.4 re-verdict — **all seven deltas are ONE RECORD at ΔL = 1**

| wave | delta | Δ | published verdict | **CORRECTED verdict** |
|---:|---|---:|---|---|
| 152 | **42,798 → 43,548 (LOW PAIR)** | **1.752 %** | NOT one record (dead gap) | **ONE RECORD, ΔL = 1** — and § 3 identifies it exactly |
| 152 | 91,696 → 93,599 | 2.075 % | NOT one record | **ONE RECORD, ΔL = 1** — `basilisk_a01` @ 102 → 103 |
| 152 | 237,258 → 242,124 | 2.051 % | NOT one record | **ONE RECORD, ΔL = 1** — `basilisk_b01` @ 103 → 104 |
| 157 | 233,250 → 238,068 | 2.066 % | NOT one record | ONE RECORD, ΔL = 1 admissible |
| 157 | 398,226 → 406,243 | 2.013 % | NOT one record | ONE RECORD, ΔL = 1 admissible |
| 157 | 411,440 → 414,837 | 0.826 % | NOT one record (below floor) | **still NOT one record** — below the corrected 1.595 % floor. The one surviving negative verdict. |
| 157 | 414,837 → 419,839 | 1.206 % | CONSISTENT, ΔL = 1 | **REVERSED — now BELOW the ΔL = 1 floor.** Not one record. |

> **The "systematic 2.01–2.08 % signature"** flagged in § 3.4 as *"a signature, not noise"* was read
> correctly and diagnosed backwards. It is not evidence of an exotic producer; it is the **ordinary
> ΔL = 1 step of this level band**, once the passive-rank term is in. Two of the four are now
> resolved to a named record and a named level pair (`basilisk_a01`, `basilisk_b01`).

> **Corrigenda-forward banner placed on the join note.** No measured row retro-edited.

---

## 3. ITEM 2 — B-KC2-C1 decomposition — **CLOSED** (the touch's primary)

### 3.1 The first pass gave the commissioned answer, and it was the wrong question

Commissioned rule: *crabling residual == Haraxis residual ⇒ mode-wide; different ⇒ tier-scoped.*
Run as specified (`d6_c1.py`), Edition-II:

| body | tier | life eq | plate L | implied ×  | ÷ 4.08 "residual" |
|---|---|---|--:|--:|--:|
| `aetherialfleshshaper_haraxis` | Quest | `((charLevel*30)^1.5)+500` | 108 | 11.0900 | **2.7181** |
| `swampcrab_a00_summon` @ 42,798 | Common | `((charLevel*6)^1.28)+25` | 107 | 10.8398 | 2.6568 |
| `swampcrab_a00_summon` @ 43,548 | Common | same | 108 | 10.9000 | 2.6716 |

Residuals within **2.3 %** across a Quest boss and a Common pet ⇒ *not tier-scoped* — the
commissioned verdict, and it is right as far as it goes. But the 2.3 % scatter is **larger than the
measurement precision**, which means the "residual" was still hiding structure. It was.

### 3.2 The multiplier is not a multiplier — it is an additive Σ, and its third term is level-indexed

Three census fingerprints turned out to be reproducible **EXACTLY** by *one* multiplier at *one*
level, across *three different* `characterLife` equations (`d8_pin.py`, Edition-II):

| fingerprint | record class | life eq | implied × at charLevel 108 |
|---:|---|---|--:|
| 2,050,807 | Quest | `((charLevel*30)^1.5)+500` | **11.08999715** |
| 453,883 | Hero (standard bio) | `((charLevel*11)^1.50)-20` | **11.08999707** |
| 472,732 | Champion | `((charLevel*28)^1.33)+50` | **11.08999913** |

Agreement to **1 part in 10⁷** across exponents 1.5 / 1.5 / 1.33. **MEASURED.**

**charLevel 108 is uniquely determined by that agreement** (`d9_exact.py`) — the three-equation
disagreement is 0.1604 % at 107, **0.0000 %** at 108, 0.1589 % at 109. So *both* M and charLevel fall
out of HP alone, with no plate input. **This is a third independent confirmation of the calibration
law "nameplate = the charLevel the attribute equations are evaluated at"** — Haraxis's plate reads
108; the HP-only joint solve says 108.

×11.0900 ⇒ **Σ = 1008.9997 % ≈ 1009 %** under additive-within-field stacking. Declared terms account
for 580 + 308 = 888. **Missing: exactly +121 %.** A corpus scan for a `characterLifeModifier` of ≈121
returned `armorbase03/04/05/06.dbr` **at array index 107** — i.e. at *skill rank 108*. Every monster
record carries one of these as `skillName3` with `skillLevel3 = charLevel*1`.

### 3.3 The solved model — **DERIVED, and it closes the block**

```
maxHP(record, charLevel, wave)
    = characterLife_eq(charLevel)
      × ( 1 + [ 580                                             # mp+difficulty, Ultimate, players 1
              + survivalmode_enemies03.characterLifeModifier[wave-1]      # 308 @ w152
              + Σ_i  skillName_i.characterLifeModifier[ skillLevel_i(charLevel) - 1 ]
              ] / 100 )
```

Verified EXACT on six independent bindings (`d11_solve.py`):

| body | charLevel | Σ | × | modelled | MEASURED (galadriel census) | Δ |
|---|--:|--:|--:|--:|--:|--:|
| `swampcrab_a00_summon` (Ugdenbog Crabling) | 107 | 984 | 10.84 | 42,798.92 | **42,798** | **+0.0021 %** |
| `swampcrab_a00_summon` | 108 | 990 | 10.90 | 43,548.04 | **43,548** | **+0.0001 %** |
| `bio_hero_standard_01` bodies | 107 | 999 | 10.99 | 443,554.74 | **443,554** | **+0.0002 %** |
| `bio_hero_standard_01` bodies | 108 | 1009 | 11.09 | 453,883.12 | **453,883** | **+0.0000 %** |
| `aetherialcorruption_c01_summon` | 108 | 1009 | 11.09 | 472,732.04 | **472,732** | **+0.0000 %** |
| `aetherialfleshshaper_haraxis` | 108 | 1009 | 11.09 | 2,050,807.53 | **2,050,807** | **+0.0000 %** |

The crabling's Σ differs from the boss's **not by tier** but because it carries `armorbase01`
(+96 @ 107, +102 @ 108) where heroes and bosses carry `armorbase03/05` (+111 @ 107, +121 @ 108).

> ### VERDICT — B-KC2-C1: **CLOSED.**
> - **There is no residual.** `×2.7181` was `11.0900 / 4.08` — a quotient by a factor that never
>   multiplied. The stack is **additive-within-field**, MEASURED.
> - **Answering the commissioned binary:** the non-record part of Σ (**580 + 308 = 888 %**) is
>   **MODE-WIDE** — same for Quest, Hero, Champion and Common. The record part is **not tier-scoped
>   either**; it is *passive-scoped and level-indexed*, and the tiers correlate with it only because
>   trash bodies happen to carry `armorbase01` and heroes/bosses `armorbase03+`.
> - **Record home, as commissioned:** `records/game/balancingadjustment_mp+difficulty_enemies01.dbr`
>   [`characterLifeModifier`, index 8] · `records/game/balancingadjustment_survivalmode_enemies03.dbr`
>   [`characterLifeModifier`, index wave−1] · `records/skills/nonplayerskills/passive/armorbase0N.dbr`
>   [`characterLifeModifier`, index charLevel−1]. All three IDENTICAL across Editions II and III.
> - **Collateral closure:** join-note Part-C **open item 1** ("the stacking rule is undeclared;
>   additive gives ×9.88, multiplicative ×27.74, nothing states which") is **ANSWERED: ADDITIVE.**
>   Neither of my two published candidates was right, because a third term was missing from both.

---

## 4. ITEM 3 — within-set assignment — **CONFIRMED, and upgraded INFERRED → DERIVED**

galadriel offered `L107 ↔ 42,798 · L108 ↔ 43,548` as monotone inference, explicitly *"a lead, not a
measurement."* Arithmetic confirms it and leaves no alternative:

| assignment | Σ(107) / Σ(108) | modelled HP | vs measured |
|---|---|--:|---|
| **107 ↔ 42,798** | 984 % → ×10.84 | 42,798.92 | **+0.0021 %** ✔ |
| **108 ↔ 43,548** | 990 % → ×10.90 | 43,548.04 | **+0.0001 %** ✔ |
| inverted 107 ↔ 43,548 | ×10.84 | 42,798.92 | −1.72 % ✘ |
| inverted 108 ↔ 42,798 | ×10.90 | 43,548.04 | +1.75 % ✘ |

The inverted pairing misses by ~800 HP on a value read to the unit. **Monotone assignment CONFIRMED.**
Multiplicity `×4 @ 107` and `×3 @ 108` is consistent with two `swampcrab_hero` placements
(`spawnChampionMinAdj/MaxAdj = +1`, L-61(f)), one at each level, each carrying
`swampcrab_crabgenerator` (`petLimit 8`, `petBurstSpawn 4`).

---

## 5. ITEMS 4 + 5 — the dead gap and the Rotmouth-107 discrimination (one mechanism, two symptoms)

### 5.1 Item 4 — Δ1.752 % at ΔL = 1 is **EXPLAINED**, not overturned

The commission offered two exits: explain it, or overturn the two-bodies-at-adjacent-levels reading.
**It is explained, and the interpretation stands.** The decomposition is exact:

```
43,548 / 42,798  =  1.017524   (MEASURED, +1.7524 %)

  base part      ((108*6)^1.28+25) / ((107*6)^1.28+25)   = 1.011902   (+1.1902 %)
  passive part   (1 + 990/100) / (1 + 984/100)           = 1.005535   (+0.5535 %)
  product                                                  1.017503   (+1.7503 %)
```

Residual **0.0021 %** — the integer-rounding of the two displayed HP values. Of the three candidate
mechanisms the commission named, the answer is the third: **per-body level-indexed cross-terms**. It
is not the additive `charLevel` term (which is 0 on this record and, § 5.2, does not apply anyway)
and not the 200-array wave scalar (which is shared within a wave and cancels).

> **The L-58 arc closes coherent, and closes *inward*:** too-narrow band → phantom Carraxus
> requirement → seat falsified by plate → band corrected by direct measurement → **the pair reseats
> on the crabling after all, at the very levels the plate read.** The mechanism class L-58 named was
> right the whole way through; only the arithmetic that priced it was wrong.

### 5.2 Item 5 — the failed link is the **OFFSET**. Identity and band both survive.

Commission: discriminate among {identity join · spawn-level band · offset}.

**(a) Identity join — CONFIRMED, three ways.**
- Tag join is **unique in both trees**: `tagGDX1HeroBasilisk_H02 = Rotmouth`, one hit in 20,394
  (Ed-II) / 20,471 (Ed-III) tags → `records/creatures/enemies/hero/basilisk_h02.dbr`.
- Only one w152-reachable pool carries it: `poolsherogdx1/basilisk_hero.dbr` at sp = 2 (the other six
  pools containing `basilisk_h02` are world/endless-dungeon/totem pools, none on a tier-16 wave).
- `monsterClassification = Hero` matches the MEASURED orange glyph; family Beast matches.

**(b) Spawn-level band — CONFIRMED.** `basilisk_hero` uses `levelVarianceEquationChampion1..5 =
lv6_hero.dbr`, whose floor set at the DERIVED `averagePlayerLevel` is exactly **{107, 108}** (§ 5.3).
The plate's 107 sits **inside** the band. The band was never the problem.

**(c) The offset — FALSIFIED, and by HP as well as by plate.**

The plate-side argument is apl-free and wave-internal: `swampcrab_h03/h04` (`charLevel*1`) and
`basilisk_h02/h03` + `aetherialcorruption_h02` (`charLevel*1+5`) draw from the **same** `lv6_hero`
equation on the **same** wave. If the offset entered the spawn level, the basilisk/corruption heroes
would stand exactly **5 levels above** the crab heroes. MEASURED: Rotmouth **107**, crablings (pets,
`charLevel*1`, at their summoners' level) **107 and 108**. Δ ∈ {−1, 0}, not +5.

The HP-side argument is independent of the plate entirely (`d12_census.py`). All six w152 hero names
share `bio_hero_standard_01` + `armorbase03`, so their HP is a pure function of level:

| hero (MEASURED name, galadriel) | record | `charLevel` | HP @ 107 | HP @ 108 |
|---|---|---|--:|--:|
| Mudflinger ~ Reflective | `hero/swampcrab_h03.dbr` | `charLevel*1` | 443,555 | 453,883 |
| Chaosshell ~ Voidtouched | `hero/swampcrab_h04.dbr` | `charLevel*1` | 443,555 | 453,883 |
| **Rotmouth** | `hero/basilisk_h02.dbr` | **`charLevel*1+5`** | 443,555 | 453,883 |
| Aregos ~ Corrupted | `hero/basilisk_h03.dbr` | **`charLevel*1+5`** | 443,555 | 453,883 |
| Chillslither ~ Arctic | `hero/basilisk_h05.dbr` | **`charLevel*1+5`** | 443,555 | 453,883 |
| Vanallius the Voracious | `hero/aetherialcorruption_h02.dbr` | **`charLevel*1+5`** | 443,555 | 453,883 |

*(Join hazard worth recording: `Chillslither ~ Arctic` is `tagGDX3HeroBasilisk_H01` — a **gdx3** tag
carried by a **gdx1-named** record, `hero/basilisk_h05.dbr`. Resolving that name by path-guess from
the tag string would have missed it; only the reverse `description` → record scan finds it.)*

The census contains **exactly two** hero-class fingerprints — `443,554 ×4` and `453,883 ×2`, six
star-flanked bodies — and they are **one level apart**. If the +5 applied, a board carrying both
offset-0 and offset-5 hero records would show hero fingerprints at four levels spanning ≥ 5, i.e. a
≥ 7.5 % HP spread. Measured spread: **2.33 %, exactly ΔL = 1.**

> ### VERDICT — item 5
> **The record's additive `charLevel` term does not enter the Crucible spawn level.** The failed link
> is the **offset**; identity and band are exonerated. The calibration law survives, restated
> precisely: **nameplate level = the level the attribute equations are evaluated at = the pool's
> level draw (floored)** — and the record `charLevel` expression is *not* in that chain.
> **MEASURED** (twice, independently: plate-side and HP-side).
>
> **Corollary I owe the run:** my L-61(h) prediction "the plate must read 109 or 110" was
> falsifiable, registered before the looking, and **wrong for a nameable reason**. The mechanism that
> made it wrong is the same one that made the L-58 bands too narrow. One error, two folds.
>
> **Corollary that pays galadriel back:** her item-2b honest NOT-READABLE is now answerable by
> arithmetic. Rotmouth's plate reads **107** ⇒ **Rotmouth max HP = 443,554** (DERIVED). She was right
> to refuse the 3-way-degenerate bar read; the number was recoverable from the level, not the bar.
> *(Grade note: 443,554 identifies the LEVEL, not the individual — all six hero names share the bio,
> so this is "Rotmouth is one of the four 443,554 bodies", which is exactly what was asked.)*
>
> **What is NOT resolved:** *why* the offset is inert here. The corpus declares no rule. Candidates
> (unranked, none measured): the proxy assigns the level directly and `charLevel` is consumed only by
> non-proxy spawn paths; or `charLevel` is legacy where a `levelVarianceEquation` is present.
> **NAMED-BLOCKED — B-KC2-C2 (offset semantics).** It does not gate anything in this run: the *effect*
> is MEASURED and the level model works without knowing the cause.

### 5.3 `averagePlayerLevel` — **DERIVED to [103.0, 103.92)**, and it is not 100

With offsets out, apl is over-determined by the resolved level structure (`d13_apl.py`).
`records/proxies/poolsbasicgdx1/basilisk_t3.dbr` assigns a *different* lv proxy per roster slot,
which makes w152 a natural four-point calibration:

| pool slot | lv proxy | interval at apl = A | floors MEASURED via HP (§ 6) |
|---|---|---|---|
| `basilisk_a01` | `lv2_normal` | [A−1, A] | **102, 103** |
| `basilisk_b01` | `lv3_strong` | [A, A+A/75] | **103, 104** |
| `basilisk_c01` | `lv4_champion+` | [A+1, A+1+A/50] | **106** |
| hero pools (`swampcrab_hero`, `basilisk_hero`, `aetherialcorruption_hero`) | `lv6_hero` | [A+2+A/50, A+3+A/50] | **107, 108** |
| boss pool (`aetherialfleshshaper_haraxis`) | `lv7_uber hero` | [A+3, A+3+A/50] | **108** |

Intersecting: **A ∈ [103.0, 103.92)**. (`lv2_normal ⊇ {102,103}` gives A ∈ [103, 104);
`lv6_hero ⊇ {107,108}` gives A ∈ [102.94, 103.92).) At A = 100 the same structure would sit at
99–106 and no hero could reach 108 — **falsified**.

> **CORRIGENDUM to my intake note § c.1 — `averagePlayerLevel = 100 CONFIRMED` is SUPERSEDED.** The
> `108 = 103 + 5` arithmetic was valid; its premise (the offset) was not, and apl was the free
> parameter that absorbed the error. Banner placed on that note.
>
> **NEW open question, filed not answered:** the *source* of apl ≈ 103.4 for a level-100 character
> in a tier-16 Crucible run is **NAMED-ABSENT in the corpus** — no level term exists anywhere in
> `survivalinfo.dbr`, in any `balancingadjustment_survivalmode_*` array (627 fields censused,
> `d4_wavelevel.py`), in the tier-16 wave proxies, or in `mp+difficulty`. **B-KC2-C3.**

---

## 6. ITEM 9 — the 52-read level sweep, consumed as a constraint dataset — **CONSISTENT**

galadriel's sweep was sampled without regard to any prediction, which makes it a clean test set. Model
prediction = the floor sets of every lv proxy at A ∈ [103.0, 103.92), offsets OFF:

| lv proxy | interval @ A = 103.4 | predicted floors |
|---|---|---|
| `lv1_weak` / `lv2_normal` | [102.40, 103.40] | 102 · 103 |
| `lv3_strong` | [103.40, 104.78] | 103 · 104 |
| `lv4_champion(+)` | [104.40, 105.78] | 104 · 105 |
| `lv5_elitechampion` | [105.40, 106.47] | 105 · 106 |
| `lv6_hero` | [107.47, 108.47] | **107 · 108** |
| `lv7_uber hero` | [106.40, 108.47] | 106 · 107 · 108 |
| `lv8_boss` / `lv8_boss+` | [108.47, 109.47] | 108 · **109** |

| observed (52 reads) | span | levels | model |
|---|---|---|---|
| w151 / w157 / w158 | 14 | 103 · 104 · 105 · 106 · 107 · 108 | ✔ all predicted |
| w153 | 10 | 103 · 104 · 106 · 107 · 108 | ✔ |
| w152 | 12 | 107 · 108 | ✔ (hero + pet-of-hero plates: `lv6_hero`) |
| s2 t = 811–838 | 12 | 106 · 107 · 108 | ✔ |
| w160 | 4 | **109** | ✔ — **109 is reachable ONLY from an lv8 pool**, and w160 is the nemesis wave |

> **The ceiling of 108 across w151–w158, and 109 appearing only at w160, is a PREDICTION of the model,
> not an input to it.** Under offsets-ON at apl = 100 the same corpus would span 96–112 and heroes
> would sit at 109/110 inside the band — contradicted 52/52.
>
> One prediction unobserved: **level 102** (`lv1/lv2` low end). Not a mismatch — it needs a hover on a
> `lv2_normal` trash body. It *is* MEASURED indirectly via `basilisk_a01 → 91,696` (§ 7), which is why
> the level model has a 102 anchor even though the plate sweep has none. **Free falsification test for
> galadriel, registered: any w152 plate hover on a `Stonegaze Basilisk` must read 102 or 103.**

---

## 7. The w152 census, fully joined — **11 / 12 fingerprints resolved EXACTLY**

Every row: modelled HP within **0.05 %** of the measured fingerprint, at an integer charLevel, on a
record reachable on wave 152. Artefact: `w152_fingerprint_levels.json`.

| max HP | × | record | charLevel | class | furniture (galadriel) |
|---:|:--|---|--:|---|---|
| 42,798 | ×4 | `swampcrab_a00_summon` — **Ugdenbog Crabling** | **107** | Common | plain |
| 43,548 | ×3 | `swampcrab_a00_summon` — **Ugdenbog Crabling** | **108** | Common | plain |
| 91,696 | ×1 | `basilisk_a01` — Stonegaze Basilisk | 102 | Common | plain |
| 93,599 | ×2 | `basilisk_a01` | 103 | Common | plain |
| 237,258 | ×1 | `basilisk_b01` | 103 | Champion | plain |
| 242,124 | ×2 | `basilisk_b01` | 104 | Champion | plain |
| 369,770 | ×1 | `basilisk_c01` | 106 | Champion | plain |
| 443,554 | ×4 | hero-standard bio (Rotmouth · Aregos · Mudflinger · Chaosshell · Chillslither · Vanallius) | **107** | Hero | ★ ★ |
| 453,883 | ×2 | same bio, one level up | **108** | Hero | ★ ★ |
| 472,732 | ×2 | `aetherialcorruption_c01_summon` | 108 | Champion | plain |
| 2,050,807 | ×1 | `aetherialfleshshaper_haraxis` | 108 | Quest | 💀💀 |
| **302,934** | ×1 | **UNRESOLVED** — no w152-reachable record within 0.05 % | — | — | plain |

Three things fall out that the composition model should have:

1. **Six star bodies ↔ six hero-RECORD names.** `443,554 ×4` + `453,883 ×2` = 6 star bodies, against
   six w152 plate names whose records are `monsterClassification = Hero`: five that galadriel measured
   **orange → hero** by glyph (Mudflinger · Chaosshell · Aregos · Chillslither · Rotmouth) plus
   **Vanallius**, which she measured **yellow → champion** by glyph while its record is Hero. Her F1
   ("the star is sufficient for hero, not necessary") is *strengthened*, and the five-names-vs-two-
   fingerprints tension dissolves: **the fingerprints are levels, not identities.** Vanallius is a
   registered single-body test of the render-vs-record axis (§ 8).
2. **The plain-tier surplus is crablings.** 7 crabling bodies (4 + 3), from two `swampcrab_hero`
   placements at adjacent levels — the `spawnChampionMinAdj = +1` mechanism of L-61(f) doing exactly
   what it was predicted to do, now with the bodies counted and priced.
3. **`472,732 ×2` is a Champion SUMMON** (`aetherialcorruption_c01_summon` @ 108), not a spawn.
   galadriel graded it **UNDECIDED** on arrival timing (+8.23 s, late). Record says summon.
   *Attribution-grade; routes to the composition model.*

`302,934` is the one open row. Nearest w152-reachable candidates at ±0.2 %: `swampcrab_c01_summon`
@ 108 (−0.147 %) and `aetherialcorruption_b02_summon` @ 108 (−0.183 %) — both **outside** the 0.05 %
envelope every other row met, so I decline both. **NAMED, not estimated.** Most likely a body reached
by a two-hop summon chain my one-hop expansion did not walk.

### 7.1 By-product finding — **three basilisk-branch hero names against two seats. MEASURED tension.**

`poolsherogdx1/basilisk_hero` has `championMin/Max = 1/1`; with `spawnChampionMinAdj/MaxAdj = +1` at
w152 that is **exactly two** champion seats. galadriel's plate scan names **three** of that pool's
five alternatives on the w152 board: **Rotmouth (h02) · Aregos ~ Corrupted (h03) · Chillslither ~
Arctic (h05)**. I checked the only other hero source at w152 — the six sp = 6 devotion pools — and
**none of them carries any basilisk hero** (all six are `lv6_hero`, `championMin/Max = 1/1`, rosters
of 13–14 non-basilisk devotion bodies).

Three named bodies, two seats, no third source in the corpus. I am not resolving this — it is a
composition-model question and the candidate explanations are not mine to rank. Recording it with the
two leads I can see: (i) galadriel's w152 scan spans t = 697.8 → 715.2 s and may cross a wave
boundary, so one name may belong to w151 or w153; (ii) `p02`'s pool draw with `championChance = 100`
across five alternatives at two seats should yield two distinct names, so a third implies either a
second p02-class placement the wave table does not declare, or a scan-window artefact. **Attribution-
grade; routes to the composition model. Nothing in §§ 2–6 depends on it** — the level and life
arithmetic is per-body and indifferent to how many heroes the wave seats.

---

## 8. ITEM 8 — the two absent plate names — **RESOLVED, with a registered prediction**

Same method as Rotmouth: display string → tag → record, run over all 7 `Text_EN.arc` in **both**
trees (`d2_tags.py`; 20,394 Ed-II / 20,471 Ed-III tags). One hit each, identical in both trees.

| plate string (MEASURED, galadriel § 5 F2) | tag | record | class | `charLevel` | seat on w152 |
|---|---|---|---|---|---|
| **`Aregos ~ Corrupted`** | `tagGDX1HeroBasilisk_H03` | `records/creatures/enemies/hero/basilisk_h03.dbr` | Hero | `charLevel*1+5` | **sp = 2**, `poolsherogdx1/basilisk_hero` `nameChampion3` |
| **`Vanallius the Voracious`** | `tagGDX1HeroAetherialCorruption_H02` | `records/creatures/enemies/hero/aetherialcorruption_h02.dbr` | Hero | `charLevel*1+5` | **sp = 5** (ProxyAmbush), `poolsherogdx1/aetherialcorruption_hero` `nameChampion2` |

Both are `bio_hero_standard_01` + `armorbase03`, both `lv6_hero`. **Neither is a roster gap** — same
verdict shape as Rotmouth: a name-coverage gap in our plate tables, not a composition gap.

**Two corroborations at no cost.** (i) `basilisk_hero` seats **two** champions at w152
(`championMin/Max = 1/1` plus `spawnChampionMinAdj = +1`) and the two names measured on camera are
**h02 + h03** — the pool's own roster, both slots filled, consistent. (ii) `Vanallius` sits on the
sp = 5 **ProxyAmbush** (`minGroupSize = maxGroupSize = 30`, `spawnThreshold = 15`) — which is why
galadriel found it at t = 709.8, *outside* the census window: the ambush fires late by construction.

> **REGISTERED PREDICTIONS (before the looking, per the Rotmouth pattern):**
> 1. **`Aregos ~ Corrupted` plate level = 107 or 108**, and its max HP is **443,554** (if 107) or
>    **453,883** (if 108).
> 2. **`Vanallius the Voracious` plate level = 107 or 108**, same two HP values.
> 3. galadriel measured Vanallius as **yellow → champion** by glyph, while the record is
>    `monsterClassification = Hero`. Under the R-L58-1 two-axis reading these need not agree — but if
>    the *level* reads 107/108 while the glyph reads champion, that is a **direct measurement of the
>    render-vs-record axis on a single body**, which the corpus has not yet produced.
>
> Any of the three failing falsifies the § 5 level model on the same terms my 109/110 prediction was
> falsified. That is the point of registering them.

---

## 9. ITEM 6 — a.7 corrigendum, BOTH sites — **DONE**

Per jack-ryan L-62(e). Corrigenda-forward: nothing struck, nothing rewritten, both wrong sites left
standing with a corrigendum attached, and a banner at the head of the note.

| site | file : line (pre-edit) | wrong | right |
|---|---|---|---|
| header | `2026-08-08-kc2-edition-III-intake-and-diff.md` § a.7 | "8 CHANGED / 8 IDENTICAL (of the 16 shared)" | **9 DIFFER / 7 IDENTICAL** |
| closing prose | same file, ex-line 214 | "It is 8 of 16." | **It is 7 of 16.** |

Authority: a.7's own table (9 = 7 `.arz` + base/gdx3 `Text_EN`; 7 = `sm2.arz` + 6 `Text_EN`),
jack-ryan's independent L-60(b) diff, and his L-62(c) re-hash. **Majority of independent
measurement, 3 : 1 against the header.** Downstream propagation: none (his grep, incl. the ledger,
which quotes the TABLE). Banner also carries corrigenda C-3…C-6 from this touch.

---

## 10. ITEM 7 — `kc2set_verdicts.json` re-emit — **DONE, and it found 4 more**

jack-ryan (L-62(d), Discipline #70 founding instance 4) found **2** rows marked `ABSENT-BOTH` that
were stale path-guesses, not absences. A mechanical basename re-resolution over **every**
`ABSENT-BOTH` row found **6** — the enumeration-by-eye missed four, which is the same sweep-law
lesson gamora banked at L-63(a), here on my own artefact.

| path as given (v1) | resolved to | v1 | **v2** |
|---|---|---|---|
| `records/creatures/enemies/fleshshaper_spirit_01.dbr` | `records/skills/nonplayerskillsgdx1/bossskills/pets/…` | ABSENT-BOTH | **IDENTICAL** |
| `records/creatures/enemies/krieg_aethertrap.dbr` | `records/skills/nonplayerskillsgdx1/bossskills/pets/…` | ABSENT-BOTH | **IDENTICAL** |
| `records/creatures/enemies/swampcrab_h05.dbr` | `records/creatures/enemies/hero/swampcrab_h05.dbr` | ABSENT-BOTH | **IDENTICAL** |
| `records/creatures/enemies/aetherialcorruption_h05.dbr` | `records/creatures/enemies/hero/aetherialcorruption_h05.dbr` | ABSENT-BOTH | **IDENTICAL** |
| `…/nonplayerskillsgdx1/monsterskills/swampcrab_crabgenerator.dbr` | `…/nonplayerskillsgdx1/summoning/swampcrab_crabgenerator.dbr` | ABSENT-BOTH | **IDENTICAL** |
| `…/nonplayerskillsgdx3/monsterskills/springscrab_crabgenerator.dbr` | `…/nonplayerskillsgdx3/summoning/springscrab_crabgenerator.dbr` | ABSENT-BOTH | **IDENTICAL** |

**New artefact: `kc2set_verdicts_v2.json`** — **613 IDENTICAL / 5 CHANGED / 9 genuinely ABSENT**
(v1: 607 / 5 / 15). Every row now carries `path_as_given`, `path_resolved`, `resolution`,
`verdict_v1`, `verdict`, and the file declares its **equality predicate in a `_meta` block** per
Discipline #69 clause (i). **`(2b) summon bodies: 15 / 15 IDENTICAL` — the note's claim REPRODUCED
by instrument.**

**Git lineage:** v1 is **retained unedited**; v2 is a new file naming what it supersedes. The
intake note carries corrigendum C-3 pointing at it. Nothing self-healed in place.

> The L-58 mechanism chain is *strengthened* by this: `swampcrab_crabgenerator` — the single record
> the whole crab-generator argument rests on — was reported ABSENT-BOTH by the stale artefact and is
> **IDENTICAL across editions**. The note said so; only the instrument lied.

---

## 11. What this touch owes back, and to whom

| # | item | status |
|---|---|---|
| 1 | § 3.3 / § 3.4 re-run | **CLOSED** — bands corrected (wider, not narrower); dead gap retired; 5 of 7 verdicts reversed |
| 2 | B-KC2-C1 decomposition | **CLOSED** — no residual; additive stack; +121 % term named to its record |
| 3 | within-set assignment | **CLOSED** — monotone CONFIRMED, INFERRED → DERIVED |
| 4 | dead-gap re-derivation | **CLOSED** — Δ1.752 % decomposes exactly (1.1902 % base + 0.5535 % passive-rank) |
| 5 | Rotmouth-107 discrimination | **CLOSED** — the OFFSET; identity + band exonerated; Rotmouth max HP DERIVED = 443,554 |
| 6 | a.7 corrigendum, both sites | **CLOSED** |
| 7 | `kc2set_verdicts.json` re-emit | **CLOSED** — 6 repairs (4 beyond the commission), v2 emitted |
| 8 | Aregos / Vanallius | **CLOSED** — both resolved; 3 predictions registered |
| 9 | 52-read sweep as constraint | **CLOSED** — 52/52 consistent; the 108-ceiling and the w160-only-109 are model *predictions* |

**Named-blocked, deliberately (nothing gates on them):**
- **B-KC2-C2 — offset semantics.** *Why* the record `charLevel` additive term is inert under a proxy
  pool. Effect MEASURED; cause undeclared in the corpus.
- **B-KC2-C3 — the apl source.** `averagePlayerLevel` ∈ [103.0, 103.92) for a level-100 character at
  tier 16. No level term exists anywhere in the survival, difficulty, wave-proxy or survivalinfo
  records (627 fields censused). Band DERIVED; generator absent.
- **`302,934 ×1`** — the one unresolved w152 fingerprint. Two candidates at −0.15 % / −0.18 %, both
  outside the 0.05 % envelope the other eleven met. Declined rather than estimated.
- **Three basilisk hero names against two seats** (§ 7.1) — MEASURED tension, two leads named, not
  ranked. Composition-model seam.

**Routes (not mine to decide):**
- **gamora / composition model** — the § 7 join table is a complete w152 body-and-level manifest:
  7 crablings at 107/108 from two hero placements; 6 hero bodies; `472,732 ×2` is a *summon* the
  arrival grading left UNDECIDED.
- **galadriel** — three registered predictions (§ 8) and one free falsification test (§ 6, the
  `Stonegaze Basilisk` 102/103 hover). Her item-2b NOT-READABLE is answered (§ 5.2). No note of hers
  was edited.
- **conductor** — B-KC2-C1 closure is a pair-seat *unblock and reseat* in one move; the C-1 closure
  lap's blocking input is now a solved equation rather than a residual.
- **jack-ryan** — Discipline #70's founding instance 4 grew 2 → 6 under mechanical re-resolution;
  another corroboration for the "enumeration must be mechanical, never by eye" graduation candidate,
  this time on a *data artefact* rather than a code hit-table.

---

## 12. Scout's report

I was sent to price a residual and found there was nothing to price.

The ×2.7181 was never a factor in the world; it was a factor in my arithmetic — what is left when you
divide by something that never multiplied. The thing I had modelled as a fixed multiplier turns out to
carry a term that moves with the monster's own level, hidden in a passive skill whose name is about
armour. That is why two crablings one level apart came out 1.752 % apart instead of 1.190 %: they were
not being multiplied by the same number. The Mirror read the bar right, read the numeral right, and
handed me a gap that only existed because my ruler was wrong.

And the ruler was wrong twice, in the same place. The `+5` I used to reproduce Haraxis's plate exactly
is inert; it reproduced the plate by accident, and it took the average-player-level with it when it
went. A prediction of 109 or 110 was registered against that arithmetic, and it fell to a seven-frame
read of a single digit. The digit was right. The prediction did its job by being wrong out loud.

What is standing now is one equation that reproduces eleven of twelve numbers on a wave to four
decimal places, and a band of levels that predicts a ceiling of 108 across eight waves and a 109 only
at the nemesis. Those were not fitted; they were checked afterwards, against fifty-two reads taken
before anyone knew what to look for.

The scout does not bring back the map he expected. He brings back the ground.

---

*Filed 2026-08-08 by legolas under KC2-SIM ruling R-L64-3 (gandalf, RUN-CONDUCTOR). Read-only
throughout; zero external fetches. Committed in the meta repo per the touch's standing authorisation;
**not pushed** — the conductor centralises under R-KC2-10.*
