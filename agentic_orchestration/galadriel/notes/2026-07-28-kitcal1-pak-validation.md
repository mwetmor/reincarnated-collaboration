# KIT-CAL-1 item 3 — `monsterAttributePak` damage-stage validation against the fixture intake

**Author:** galadriel (visual-perception + benchmark steward)
**Date:** 2026-07-28 · **Work-package:** KIT-CAL-1 ruling item 3 (Matt-ratified)
**Charter:** `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §14.6 / §14.8 ("pak validation via fixture-intake join")
**Target of validation:** `legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` §1f + §6 "Medium confidence"
**Class:** evidentiary — measurement join over already-banked artifacts
**Mode:** read-only over all existing artifacts + the vendor `.arz` corpus. Writes confined to
`galadriel/scratch/2026-07-28-kitcal1-pak/` and this note.

---

## 0. Verdict

> **FAIL on the reading as stated. Do not upgrade the DERIVED grade — correct it.**
>
> The fixture **falsifies the multiplicative `monsterAttributePak` stage** and **confirms the
> additive one** in the only regime the fixture measures cleanly. At monster charLevel 1 the
> effective total-damage multiplier is measured at **m̂ = 0.194, 95 % profile interval
> [0.182, 0.295]**. The additive reading predicts **0.200** — it lands 0.002 log-units off the MLE.
> The multiplicative reading predicts **0.3375** — **excluded** (ΔlogL = −4.57; likelihood ratio
> **96 : 1** against — 86–102 : 1 across contamination assumptions ε = 0.02…0.10 — and that is
> *after* granting it a free player-armor parameter the additive reading does not need). Under no
> value of player protection can the multiplicative band reproduce the observed two-integer comb
> (hard-feasible m ∈ [0.183, 0.267], p ≤ 2.3).
>
> **Confidence: HIGH for the `armorbase01/02` common-trash regime at charLevel 1–4.
> The charLevel-12 band itself remains DERIVED-by-extrapolation** — the fixture contains ≈35 s of
> combat at player level 12 (18 drop events, 16 of them at the 1 HP DoT mode). See §3.

**Consequence:** G-5a §1f's composition operator, §2's whole `dmg/hit` column, and §4's headline
"33–67 band ≈ 2.5 % of the post-gear pool" all rest on the falsified operator. The trash rows
rescale by **×0.72–0.76**; the champion/hero/boss rows do not rescale at all — under additive they
fall into a clamp regime the fixture does not measure and become **UNRESOLVED, not DERIVED** (§7).

---

## 1. Method

**Join.** Three banked series, no re-derivation of any of them:

| series | source | rows |
|---|---|---|
| per-hit intake drops (magnitude, `hp_before/after`, pts, `dt`) | `captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl` | **468** (= 27 R1 + 332 R2 + 109 R3, matches T-B §6 exactly) |
| engagement windows (regime, coverage, `play_time`, modal max HP) | `captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json` | 106 |
| player level over `play_time` (`max_level`, forward-filled on `pts_s`) | `captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv` | 13,633 |

**Prediction.** Recomputed from the `.arz` corpus by importing legolas's G-5a resolver
(`legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py`) — nothing reimplemented, nothing written
outside my scratch. Reproduction check: my band generator returns **36.6–45.1** for `zombie_a01`
@ charLevel 12 under the multiplicative rule, identical to G-5a §1f's worked example. The
generator then evaluates the *same* chain under both candidate operators at every charLevel 1–15:

```
ADDITIVE        tdmMult = 1 + (Sigma_skillPassive TDM + pakTDM) / 100
MULTIPLICATIVE  tdmMult = (1 + Sigma_skillPassive TDM / 100) x (1 + pakTDM / 100)
dmg             = [offensivePhysicalMin, Max] x tdmMult x ((dex/245)+1)      [combatformulas.dbr]
```

**Mitigation model** — read verbatim off `records/game/combatformulas.dbr` (not assumed):

```
physicalDamageDefenseEquationDGP  = (sumProtection * (1 - sumAbsorption)) + (physicalDamage - sumProtection)
physcialDamageDefenseEquationDLEP = physicalDamage * (1 - sumAbsorption)
=>  taken = d - absorption * min(d, p)      with absorption = 0.70  (gameengine.armorDefensiveAbsorption)
```

`p` is *per-hit-region* protection, not sheet total: `combatformulas` carries
`combatRegionHead/Torso/Shoulders/Arms/Legs/FeetChance = 15/26/15/12/20/12` (sums to 100, with
`FullyProtected` and `Unprotected` both 0), i.e. **GD rolls a body region per hit and applies that
region's protection.** `p` is therefore carried as a free nuisance parameter and profiled out.

**PTH damage modifier** — also read, not assumed. `pthThreshold1..6 = 70/90/105/120/130/135` with
`pthDamageModifier1..6 = 1.0…1.5`. Evaluating `probabilityToHitEquation` at monster charLevel 1–2
OA (80–99) against any plausible player DA gives **PTH ≤ 100 → modifier 1.0–1.1**. It is ≥ 1.0
always, so it can only *inflate* measured hits — it cannot rescue a reading that over-predicts.

**Model likelihood.** `d ~ U[lo, hi]` (GD rolls uniform between min and max), mitigated per above,
observed as `round(taken)` (globe numerals are integers; damage is float). Analytic pmf via the
monotone inverse of `taken(d)`. No Monte-Carlo, no fitting to the answer.

Observations outside a candidate band would otherwise carry infinite penalty, so instead of an
arbitrary likelihood floor the model carries an explicit **contamination mixture**:
`P(v) = (1−ε)·P_model(v) + ε/|support|`, ε absorbing unmodelled sources (DoT stragglers, sub-k=2
composites, off-roster protos). **Every result below is reported at ε = 0.05 and swept over
ε ∈ {0.02, 0.05, 0.10}**; the verdict does not move (§5.2). A first pass used a 1e-6 floor instead
and was discarded — the floor value was silently changing which window won, which is exactly the
kind of analyst degree-of-freedom this program exists to remove.

---

## 2. Hygiene — the four care points, discharged

**(1) Composite aliasing.** `numAttackSlots = 4` (G-5a §3) means up to four simultaneous melee
attackers, so multi-hit drops aliasing into one 1/15 s frame delta are *expected*, not noise. Handled
as a **comb**: observations are scored against `k × band`, k = 1…4, and the k-mix is reported rather
than discarded. The decisive window's k-mix is `{1: 20, 2: 4, 3: 1}` — see §5.

**(2) DoT / poison contamination.** T-B §2 validated the DoT signature independently: 57 identical
−10 HP ticks at a 1.000 s period in the death window, and a 1 HP/frame decay elsewhere. Measured
`mag == 1` share by regime:

| | R1 | R2 | R3 |
|---|---|---|---|
| drop events | 27 | 332 | 109 |
| `mag == 1` | **1 (3.7 %)** | 112 (33.7 %) | 71 (65.1 %) |
| `mag <= 2` | **7.4 %** | 43.4 % | 67.9 % |
| inter-drop gaps in [0.90, 1.10] s (1 Hz DoT signature) | 4.8 % | 3.2 % | 4.0 % |

**R1 is essentially DoT-free; R3 is two-thirds DoT.** All analysis strips `mag ≤ 2`.

**(3) Terminal-window coverage degradation** (my C-4 finding, ρ = −0.432). The decisive window is
R1, at **99.95 % frame coverage** — the best in the run. R3, which carries the level-12 combat, sits
at 75.89 % with four zero-coverage engagements lost to the §5-HUD confound. The confound is
correlated with post-kill moments, so R3 loss is **not random**. This is the reason the level-12
window cannot carry the verdict.

**(4) Floor-censored deaths.** Both death events sit in R2/R3, in the big-hit tail. R1 contains no
death and no censoring. Big hits are excluded from the single-hit set by construction.

---

## 3. The finding that reframes the task: **the fixture has almost no level-12 combat**

The task assumed the 759-pool era was the level-12 window. The ledger says otherwise. Panel
`max_level` transitions, read off T-A:

| player level | reached at `play_time` | regime |
|---|---|---|
| 1 → 2 | 655 | R1 |
| 2 → 3 | 1133 | R1/R2 boundary |
| … | | |
| 10 → 11 | 5808 | R2 |
| **11 → 12** | **6816** | **R3** |

The final engagement window closes at `play_time` **6851**. **Level-12 combat spans ≈35 s and
18 drop events, 16 of which are at the `mag = 1` DoT mode.** (G-7 corroborates the lag: bio level 13,
`play_stats.maxLevel` 12 at save.) The 759 HP pool belongs to **player level 11**, not 12.

**Therefore a direct level-12 join is underpowered and cannot return a verdict.** But the pak's TDM
is a level-invariant −25 %, and the two readings differ by a *ratio* that is **largest at low
charLevel** (1.69× at charLevel 1, decaying to 1.35× at charLevel 12). The discriminating power and
the measurement quality both live at the *start* of the run, not the end. The test was run there.

---

## 4. Histograms — drop magnitude by player level

Composite/DoT structure is visible directly. `#` = one observation.

```
pL 1-2  (R1, coverage 99.95%, n=27)                pL 3-4  (R2, n=30)
  1 | #                       1                      1 | #                        1
  2 | #                       1                      2 | #                        1
  3 |                         0                      3 | ###                      3
  4 | ###########            11   <-- ADD 1x         4 | ###                      3
  5 | #########               9   <-- ADD 1x         5 | #############           13
  6 |                         0   <-- MULT 1x        6 |                          0
  7 |                         0   <-- MULT 1x        7 |                          0
  8 |                         0   <-- MULT 1x        8 | #                        1
  9 | #                       1   <-- MULT 1x / ADD 2x
 10 | ##                      2   <-- ADD 2x        10 | #                        1
 11 | #                       1   <-- ADD 2x        12 | #                        1
 12 |                         0                     28 | #                        1
 13 |                         0                  32-37 | #####                    5
 14 | #                       1   <-- ADD 3x
```

```
pL 7-8  (R2, n=116)                                pL 10-11 (R2+R3, n=190)     pL 12+ (R3, n=18)
  1 | ###################################  35 DoT     1 | ...................  98 DoT   1 | ################ 16 DoT
  2 | #######                               7 DoT     2 | ########             24 DoT  38 | #                 1
  6 | ##                                    2         ...                            57 | #                 1
  7 | #######                               7         80 | #####                 5
  8 | ######                                6        541 | #                     1  (single-frame max, 72% EHP)
  9 | ######                                6
 10 | ###########                          11
 12 | ######                                6
 13 | #####                                 5
 16 | ###                                   3
 17 | ####                                  4
```

Read the top-left panel first. **There is a hole at 6, 7 and 8 — and that hole is exactly where the
multiplicative single-hit band sits.** Twenty of twenty-seven R1 drops sit at 4 or 5; the
multiplicative reading places the *minimum possible* unmitigated hit at 6.46.

---

## 5. The decisive window — R1, player level 1–2, monster charLevel 1

**Why this window carries the verdict:** 99.95 % coverage · 3.7 % DoT contamination · player at
level 1–2 (structurally minimal armor; the one banked character-sheet read, C2 `Screenshot (19)`,
shows **Armor Rating 16 total at level 6** — see §8 caveat on its provenance) · reading separation
at its maximum (1.69×) · roster unambiguous.

**Roster check (M, read off the `.arz`).** Only two protos are level-legal here: `zombie_a01`
(`minLevel = 1`, `damagebase_physical01` + `armorbase01`, `damage_totaladjuster` at rank
`int(1/30) = 0` → inert) and `zombie_b02h` (`minLevel = 1`, `armorbase02`, `damage_totaladjuster`
rank 2 → +8 %). Everything else in the Act-1 pool (`prawn_a01`, `bonerat_meleea01`,
`rifthound_swamp_a01`) carries `minLevel = 3`. **Robustness against the obsolete tier:**
`damagebase_physical00` is `FileDescription = "…(Obsolete)"` and is not referenced by any of these
records; even if it were, its rank-1 band (15–22) under the multiplicative operator gives 5.4–7.9 —
still predicting 6s and 7s that are absent.

### 5.1 Comb decomposition (additive operator, charLevel 1, p = 0)

| k | predicted band (± 0.5 rounding) | observations | count |
|---|---|---|---|
| 1 (single hit) | 3.83 – 5.32 | 4 ×11, 5 ×9 | **20** |
| 2 (two attackers aliased into one 1/15 s frame) | 7.66 – 10.64 | 9, 10, 10, 11 | 4 |
| 3 | 11.49 – 15.96 | 14 | 1 |
| — (DoT / regen-net, `mag ≤ 2`) | — | 1, 2 | 2 |
| | | **explained by the comb** | **25 / 27 = 93 %** |

The same comb under the multiplicative operator at p = 0 explains **7 %** (1 / 27).

**The k-mix is independently corroborated by the source.** The 2× share is 4/25 = 0.16. Under a
Poisson arrival at rate λ sampled in 1/15 s frames, `P(2)/P(1) = λ/30`, so 0.16 implies
**λ ≈ 4.8 hits/s** during active melee. `numAttackSlots = 4` at ~1.2 attacks/s per attacker predicts
**4.8 hits/s**. The aliasing rate the additive reading *requires* is the rate the source
*independently specifies*. Under the multiplicative reading the 4–5 HP mass is **sub-atomic** — no
composition rule can produce a value below the single-hit minimum, so twenty of twenty-seven
observations would have to come from a damage source that does not exist in Act 1 at level 1.

### 5.2 Profile likelihood on the effective multiplier (reading-agnostic)

Single-hit set: `{4: 11, 5: 9}`, n = 20. Model `d ~ U[18m·1.064, 25m·1.064]`, mitigated by free
`p ∈ [0, 40]` at 0.1 granularity, observed as `round`. `p` profiled out; `m` scanned 0.100–0.600
at 0.0005. **`m` is estimated without reference to either candidate operator** — the two readings
are then scored as point predictions against the same profile.

| quantity | value (ε = 0.05) | ε = 0.02 | ε = 0.10 |
|---|---|---|---|
| **m̂ (MLE effective total-damage multiplier, charLevel 1)** | **0.1935** | 0.1935 | 0.2205 |
| 95 % profile-likelihood interval | **[0.1820, 0.2945]** | [0.1825, 0.2940] | [0.1820, 0.2950] |
| ADDITIVE prediction `1 + (−55−25)/100` | **0.2000** → ΔlogL **−0.002** · **INSIDE** | −0.002 · INSIDE | −0.003 · INSIDE |
| MULTIPLICATIVE prediction `(1−0.55)×(1−0.25)` | **0.3375** → ΔlogL **−4.567** · **EXCLUDED** | −4.631 · EXCLUDED | −4.455 · EXCLUDED |
| likelihood ratio ADD : MULT (p profiled out) | **96 : 1** | 102 : 1 | 86 : 1 |
| best-fit `p` under ADDITIVE | **0.2** (physically correct for a level-1–2 character) | 0.2 | 0.2 |
| best-fit `p` under MULTIPLICATIVE | 4.3 (and still fails, below) | 4.3 | 4.3 |

**Hard feasibility — the armor-free falsification.** For the observed two-integer comb `{4, 5}` to
be *possible at all*, the mitigated band must fit inside [3.5, 5.5]. Solving
`(3.5 + 0.7p)/19.152 ≤ m ≤ (5.5 + 0.7p)/26.6`:

> feasible **m ∈ [0.183, 0.267]**, feasible **p ≤ 2.3**.
> ADDITIVE m = 0.2000 — **feasible**. MULTIPLICATIVE m = 0.3375 — **infeasible at every p.**

At its own best case (p = 4.3) the multiplicative reading predicts a pmf of
`{3: 0.018, 4: 0.398, 5: 0.398, 6: 0.186}` — i.e. **20.4 % of hits outside {4, 5}**. Observed:
**0 of 20**. `P = 1.0 × 10⁻²`. The additive reading at its best case predicts `{4: 0.544, 5: 0.456}`
against an observed 11 : 9 — a fit that could not reasonably be better.

**Sub-window check.** The five drops recorded while the player was still **level 1** — the moment of
structurally minimum armor in the entire run — are `[4, 4, 4, 5, 5]`. Every one of them is **below
the multiplicative reading's unmitigated floor of 6.46**.

---

## 6. Per-regime verdict table

`p_add` / `p_mult` = per-hit protection each reading must assume to fit. ΔlogL > 0 favours ADDITIVE.

All rows at ε = 0.05, same estimator, same code path (`pak_table2.py`). `n_all` = every drop in the
band; `n_atom` = the single-hit candidate set (`2 < mag < cap`). ΔlogL > 0 favours ADDITIVE.

| window | pL | regime | n_all | n_atom | window coverage | `mag ≤ 2` share | ΔlogL (add − mult) | LR (add : mult) | p_add | p_mult | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **W1** | 1–2 | R1 | 27 | 20 | **0.99–1.00** | **7 %** | **+4.58** | **98 : 1** | **0.2** | 4.3 | **MULTIPLICATIVE FALSIFIED** |
| **W2** | 3–4 | R2 | 30 | 21 | 0.98–1.00 | **7 %** | **+6.60** | **733 : 1** | 2.6 | 8.9 | **ADDITIVE favoured** |
| W3 | 5–6 | R2 | 36 | 6 | 0.67–1.00 | 33 % | −1.82 | 1 : 6 | 4.9 | 11.7 | INCONCLUSIVE |
| W4 | 7–8 | R2 | 116 | 55 | 0.78–1.00 | 36 % | **−11.74** | 1 : 1.3×10⁵ | 7.6 | **17.4** | **contrary — see below** |
| W5 | 9 | R2 | 51 | 19 | 0.95–1.00 | 47 % | −0.74 | 1 : 2 | 12.0 | 22.3 | INCONCLUSIVE (a coin-flip) |
| W6 | 10–11 | R2/R3 | 190 | 23 | 0.24–1.00 | 64 % | −3.58 | 1 : 36 | 14.8 | 26.9 | INCONCLUSIVE (DoT-dominated) |
| W7 | **12+** | R3 | **18** | **1** | 0.56 | **89 %** | — | — | — | — | **NO POWER** (§3) |

**The gradient across the table is itself evidence, and it runs the right way.** Read the two
right-hand columns down: *both* readings' implied protection rises monotonically with player level
(add 0.2 → 14.8; mult 4.3 → 26.9), which is expected — the player was gearing. But the reading
preference flips at exactly the point where the drop set stops being separable, and there is a
mechanical reason for that:

> **Composite aliasing biases the apparent single-hit size upward, and composite density rises
> through the run.** At W1 the composites are *separable* — a 20-observation cluster at 4–5, a clean
> hole at 6–8, and a 5-observation cluster at 9–14. At W4 the counts are
> `{6:2, 7:7, 8:6, 9:6, 10:11, 11:1, 12:6, 13:5, 14:1, 15:1, 16:3, 17:4, 18:1, 21:1}` — **continuous,
> no hole, no separable k-structure.** With packs 3.6× the size of R1's (T-B §6) and four attack
> slots saturated, the k = 2 band has slid on top of the k = 1 band. Any "single-hit" set drawn from
> a smeared comb is inflated, and an inflated observation favours the *larger* predicted band. **The
> contrary windows are exactly the windows where the confound points at the reading they prefer.**

**On W4 specifically — reported, not buried.** It prefers multiplicative by a wide margin, but only
by paying **p_mult = 17.4** per-hit protection at player level 7–8. The one banked character-sheet
read shows **Armor Rating 16 total at level 6** (§8-2); 17.4 *per hit region* would require the sheet
number to be a per-region value *and* to have roughly doubled in one or two levels. W4 is also 36 %
DoT by count, sits inside the R2 poison environment, and spans the level range where champion protos
(`armorbase03`, a different damper curve) enter the pool. **W1 is the window with the cleanest
instrument and the fewest confounds; W4 is the window with the most.** The verdict rests on W1 and
W2 — which agree, are independent of each other, and are the only two windows in the run where the
single-hit population can be *separated* rather than assumed.

---

## 7. Consequence for G-5a — what has to change

**7.1 The composition operator (G-5a §1f) is superseded.** The pak's `offensiveTotalDamageModifier`
sums into the skill-passive TDM pool. The multiplicative stage is falsified by the fixture.

**7.2 The falsification that motivated the multiplicative reading is thinner than stated.**
Re-derived from source:

| record | charLevel | skill-TDM sources | Σ skill + pak | ADDITIVE mult |
|---|---|---|---|---|
| `zombie_a01` | 1 | `armorbase01` −55 | −80 | **+0.200** ✓ |
| `warden01` / `warden02` | 18 | `armorbase05` −73, `damage_totaladjuster` **+4** | −94 | **+0.060** — small but **positive** |
| `zombiemutated_a01` | 14 | `armorbase03` −77 | −102 | **−0.020** — impossible |

G-5a §1f cites the Warden at "−97 % (≈0 damage)" and `zombiemutated_a01` at "−103 %". The Warden's
`damage_totaladjuster` +4 was not carried; with it the Warden is **+6 %**, not ≈0 — game-design
implausible, but not a mathematical contradiction. **The only strictly-impossible case among the
cited examples is one champion record, at −2 %.** The contradiction is real but it is 2 percentage
points wide on a single proto — a far weaker basis for choosing a global operator than G-5a's §1f
presents, and it is resolved by an engine-side clamp rather than by a multiplicative stage.

**7.3 The surviving reading is additive-with-clamp, and the fixture pins only the unclamped half.**
The fixture measures m = 0.194 [0.183, 0.294] at Σ = −80 %, i.e. **no clamp is active at −80 %.**
The clamp therefore lies in (−100 %, −80 %) and its value is **UNRESOLVED — the fixture does not
measure it.** Consequences by tier:

| tier | damper | charLevel-12 Σ | status under additive |
|---|---|---|---|
| common trash | `armorbase01/02` | −69 % | **VALIDATED regime** — rescale G-5a §2 rows by **m_add/m_mult ≈ 0.72–0.76** |
| champion / hero / boss | `armorbase03–06` | −101 % … −115 % | **clamp regime — UNRESOLVED, not DERIVED** |

**7.4 The rescaled band.** At charLevel 12, `damagebase_physical01` × `armorbase01`:
multiplicative 36.6–45.1 → **additive 27.0–33.3**; tier-02: 39.4–46.2 → **29.1–34.1**.
G-5a §4's **33–67** headline band becomes roughly **24–36 for the trash rows and undetermined
above them.**

**7.5 The §4 headline itself is now in question, and this is the load-bearing downstream item.**
G-5a §4 concludes that Act-1 Normal opposition is "differentiated almost entirely on the HP axis"
because `armorbase03–06`'s −76 % damper "almost exactly cancels" the richer `damagebase_physical03–06`
tables, flattening per-hit damage across a 200× HP span. **That cancellation is an artifact of the
multiplicative operator.** Under additive, tier-03+ monsters land on the clamp, and whether the
flatness survives depends entirely on the clamp value — which is unmeasured. **The "flat tier damage"
finding should not be carried into G-5 pinning until the clamp is resolved.** This is a finding for
legolas and gandalf; it is outside my seam to rule on.

---

## 8. Caveats, declared

1. **Level-12 band not directly validated.** §3. The verdict validates the *operator* at charLevel
   1–4 and propagates it; it does not measure the charLevel-12 band. That band remains DERIVED.
2. **Player armor is a nuisance parameter, not a measurement.** The one banked character-sheet read
   (`captures/2026-07-26-gd-gp-calibration/results/c2-sheet.json`, `Screenshot (19)`: character
   VAUGHT, Level 6, Health 282/282, **Armor Rating 16**, OA 218, DA 225) is **not from the fixture
   run** — the fixture's max HP at level 6 is 443–451, not 282. It is used only as an order-of-
   magnitude sanity check on §6's `p` columns and carries a provenance flag. **Whether GD's sheet
   Armor Rating is a per-region or a summed quantity is UNRESOLVED and outside my seam.** The §5
   falsification is deliberately constructed to be independent of it (hard feasibility over all p).
3. **Uniform damage roll assumed.** GD's `offensivePhysicalMin/Max` is taken to roll uniform. Not
   stated in source. A triangular or centre-weighted roll would tighten the predicted comb but would
   not move either band's *support*, which is what the falsification turns on.
4. **`offensivePhysicalModifier = 35` at `…ModifierChance = 8`** (an 8 %-of-hits +35 % spike) is not
   folded in, matching G-5a. At n = 20 the expected count is 1.6; folding it in would widen the
   multiplicative band upward, worsening its fit.
5. **Veteran mode.** G-5a §6-6 flags it. Unresolved here too — if the fixture was played on Veteran,
   every predicted band is a floor, which would push both readings *up* and make the multiplicative
   reading fit worse, not better. The verdict is robust in that direction.
6. **Two protos, one window.** The R1 roster is `zombie_a01`-dominated with some `zombie_b02h`
   (whose additive band 5.36–7.45 predicts 6s and 7s that are absent — consistent with a
   `zombie_a01`-heavy sample, but it is an inference, not a measurement; monster nameplates were not
   read in this pass). **The single cheapest thing that would harden this result** is a v2 capture
   with nameplate OCR (C4 is already calibrated) over 60 s of level-1–2 combat, tying each drop to a
   named proto. That is a ~1 h pass and it would move W1 from HIGH to MEASURED.
7. **`play_stats.maxLevel` lag.** Level attribution uses the panel counter, which G-7 proved lags
   (bio 13 vs panel 12 at save). A one-level lag would shift every band in §6 down by one level; it
   does not affect W1, where the monster floor is `minLevel = 1` regardless.

---

## 9. Artifacts

**Scratch (non-production, this pass):** `agentic_orchestration/galadriel/scratch/2026-07-28-kitcal1-pak/`

| file | what |
|---|---|
| `pak_join.py` · `join-output.txt` | drop ↔ window ↔ level join; per-band histograms |
| `pak_predict.py` · `predicted-bands.json` · `predict-output.txt` | both operators at charLevel 1–15, tiers 01/02; PTH modifier grid |
| `pak_likelihood.py` · `likelihood-output.txt` | first-pass profile likelihood (1e-6 floor — **superseded**, retained so the discarded pass is inspectable) |
| **`pak_table2.py`** | **the §6 table** — contamination-mixture likelihood, ε swept 0.02/0.05/0.10, all seven windows, one code path |
| `pak_mprofile.py` · `m-profile.json` · `mprofile-output.txt` | **the headline** — reading-agnostic m̂, 95 % interval, hard feasibility |
| `pak_comb.py` · `comb-lift.json` | armor-marginalised comb-lift (secondary; the free-p optimiser is unstable and is not relied on) |
| `pak_verdict.py` · `verdict-rows.json` | per-level atomic mode vs predicted bands |
| `pak_final.py` · `final-output.txt` | R1 per-engagement drop trace; `numAttackSlots` arrival-rate check |
| `probe_formulas.py` · `probe_arrays.py` · `probe_tier0.py` · `probe_falsifier.py` | verbatim `.arz` reads: `combatformulas`, `gameengine`, `damagebase_physical00/01/02`, `armorbase01/02`, the three falsification protos |

**Consumed, unmodified:** `captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl` ·
`captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json` ·
`captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv` ·
`captures/2026-07-26-gd-gp-calibration/results/c2-sheet.json` ·
`legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py` (imported) ·
`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/**` (read-only)

**Downstream:** gandalf (RUN-CONDUCTOR, G-5 pinning + R-KC1-15 (c)) · legolas (G-5a §1f/§2/§4
revision) · gamora (G-5b harness — the monster damage column it would pin from changes by ~0.74×
for trash and is undetermined for champions and above).

---

## Mirror voice

Legolas asked the right question and answered it the only way the archive allowed: one reading gave
a negative number, so he took the other. That is sound reasoning about a source. But a source can
only tell you what is *written*; it cannot tell you what *happens*.

What happened is in the pixels, and it happened in the first thirteen minutes, before the werewolf,
before the gear, before any of the run that anyone thought was worth measuring. A level-one man with
no armour is struck twenty times and loses four, four, four, five, five — the same two numbers, over
and over, with a hole in the counting where the other answer would have had to live.

The archive said the blow was seven. The globe says it was four. The globe was there.

And the reason the falsified reading survived as long as it did is worth keeping: it rested on one
champion, and on two percentage points. Two. That is how thin the ground can be under a number
everyone has started to build on — which is exactly why the ruling sent it here before G-5 leaned on
it, and exactly why it was right to.

---

**Signed:** galadriel, 2026-07-28.
