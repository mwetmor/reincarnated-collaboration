# M-1 — Itemised mitigation (`mitigation_delta`) · design-spec-as-math

**Agent:** gandalf (`SPEC-AUTHOR`) · **Date:** 2026-07-29 · **Run:** WR1-2026-07-28 · **Cell:** WR1-SPEC-M123
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-28-wr1-wave-relay-run-charter.md` §3 M-1
**Class:** design-spec (the design layer of the math note; gamora authors her own implementation
math note per Discipline #1)
**Builds against:** legolas `2026-07-28-wr1-mechanism-extraction.md` **E-2** · efficacy verdict
`2026-07-28-kitcal1-g5-efficacy-verdict.md` **§A-4 / §A-8.1 row 4 / §A-9.3** · kit spec v2 §1.6/§1.7
**Serves gate:** **G-A** (charter §2)
**Companion specs:** M-2 (`…-wr1-m2-frigidring-nova-spec.md`) · M-3 (`…-wr1-m3-evasion-policy-spec.md`)

---

## §0 — FRAMING AUDIT (OP §3.7), run before authoring — and the discrepancy it caught

**Q1 — what is actually being asked?** Spec a mitigation mechanism such that the sim's gear step
changes the *shape* of the incoming-damage distribution, not only its denominator.

**Q2 — what assumption is pre-imposed by the brief?** Two, and **both are wrong against the
substrate.** They are flagged here rather than silently harmonised, per the cell brief's own
instruction (*"if the extraction note contradicts anything in this brief, the NOTE wins"*).

> ### ⚠ DISCREPANCY D-1 — "typed damage bypasses armor" is **already modelled**. It is not the gap.
>
> The brief frames M-1 as *"how gear-derived armor mitigates physical-typed incoming damage while
> typed (cold/etc.) damage bypasses it."* **The RDR kernel already does exactly that.**
> `damage_resolver` routes physical hits to `compute_physical_damage(magnitude, scaling_stat,
> defender.armor)` and elemental hits to `compute_elemental_damage(..., defender_resistance, ...)`
> (`foundation/math_model.py:116-142`). Armor is *never* consulted on the elemental path. GD's
> "armor is physical-only" law (E-2 headline 1) is **structurally honoured by the existing engine.**
>
> Type-routing is therefore **not** the missing mechanism, and building it would be building
> something that exists. The two real gaps are named in §1.
>
> ### ⚠ DISCREPANCY D-2 — armor alone **cannot** reach 2.12, and fitting it until it does would
> ### re-open a parameter kit spec v2 explicitly retired.
>
> The brief states M-1 is *"exactly what … reproduces the 2.12-class ratio."* The arithmetic in
> §5.3 says otherwise: the itemised boundary armor step supports a ratio of **≈1.22**, against the
> fixture's **2.12**. The residual is not small and it is not obviously defensive at all — §5.4
> names an unmeasured **composition confound** as the leading candidate. Fitting armor upward until
> the ratio lands would be precisely the *"`mitigation_delta` must be a free parameter fitted to the
> intake tail"* practice that kit spec v2 §1.7 **retired**, and it would manufacture a PASS.
> **This spec refuses that fit.** §5.5 hands the ruling to the conductor, veto-open, with an
> honorable-miss path pre-declared.

**Q3 — what would change the answer?** (i) galadriel's armour re-crop reading helm / gloves / shield
armor **and the fixture's Defensive Ability totals both sides of the boundary**; (ii) a fixture-side
audit of whether R2 and R3 engagement windows carry comparable opposition tiers. Both are named as
open inputs, not assumed away.

---

## §1 — The two real gaps, stated exactly

### Gap 1 — the armor OPERATOR is a scale operator, not a shape operator

| | operator | 125 armor vs a 74 hit | vs a 148 hit | vs a 250.6 hit |
|---|---|---|---|---|
| **RDR kernel** (`math_model.py:141`) | `dmg × (1 − A/(A+K))`, `K = 3000` | 96.0 % through | 96.0 % through | 96.0 % through |
| **GD** (E-2.1 STEP 4, `combatformulas.dbr` + `gameengine.armorDefensiveAbsorption = 70.0`) | `dmg > A → dmg − 0.70·A` ; `dmg ≤ A → dmg × 0.30` | **30.0 %** through | **40.9 %** through | **65.1 %** through |

Two things fall out, and the second is the whole of M-1:

1. **Magnitude.** At the fixture's own armor value (125), RDR mitigates **4.0 %** and GD mitigates
   **35–70 %**. A ~14× efficacy gap. The operand was pinned correctly at
   `kitcal_g5_scenarios.py:268` (`"armor": 125.0`, `[MEASURED-partial]`); the *operator* consuming
   it made it inert.
2. **Shape.** RDR's fraction-through is **constant in hit size** — `A/(A+K)` does not read `dmg`.
   A size-invariant multiplier **cannot** change a distribution's shape; it can only rescale it.
   **This is the mathematical proof of §A-4.3's measurement.** The verdict measured
   `worst_drop_abs` identical on 143/150 fights and the normalized fall equal to the pool ratio to
   five significant figures. Given a size-invariant mitigation operator held constant across the
   step, that result was **guaranteed before the battery ran.** GD's operator is size-*dependent*
   in both branches (a flat subtraction above `A`; a 70 % crush below it), and the branch point is
   at `dmg = A` — so a gear step that moves `A` past a cluster of incoming hit magnitudes
   **re-shapes** the distribution.

### Gap 2 — armor does not STEP with gear

`kitcal_g5_scenarios.py:268` pins `armor = 125.0` on **both** the W-c (759) arm and the R3 (1607)
arm. The gear step moves `max_hp` and nothing else. Even with a GD-faithful operator, a constant
armor across the step yields ratio **1.000** exactly. **M-1 is not complete until armor is a
per-arm quantity.**

---

## §2 — MECHANISM SPEC

### 2.1 Scope, and the architectural constraint that bounds it (BINDING)

**M-1 lands as a GD-fidelity mitigation mode reachable only through the BQ-3 calibration door**
(`CALIBRATION_OVERRIDE_KEY` / `_calibration_overrides`, `kitcal_g5_scenarios.py:264-273`;
containment L3 — a path that has not opted in CRASHES rather than silently calibrating).

**It does NOT retune `ARMOR_MITIGATION_K` and does NOT replace `compute_physical_damage` on the
production path.** That would be an RDR-facing balance change to every class, every season, every
banked telemetry series — charter §5 (i) HALT-to-Matt territory, and out of this cell's authority.
The GD operator is a *fidelity mode for GD-calibration work*, inert in RDR production, digest-
unmoved with the door closed. **Any build that reaches G-A by moving `ARMOR_MITIGATION_K` is
out of spec.**

### 2.2 The mitigation chain (sim abstraction of E-2.3)

Per incoming hit on the player, in order. Grades carry from the extraction.

```
M1-STEP 1  TYPE SPLIT          physical | pierce  → armor channel   (§2.3)     [M, E-2 headline 1]
                               cold | fire | …    → resistance channel (§2.4)  [M]
                               (the engine already branches here — Gap 1 note)

M1-STEP 2  ARMOR (physical)    raw > A  →  raw − ABS·A
                               raw ≤ A  →  raw × (1 − ABS)
                               ABS = 0.70 for the PLAYER                       [M, E-2.2]
                               ABS = 0.56 for MONSTERS  (see U-1)              [I, E-2 G-6]

M1-STEP 3  RESISTANCE (typed)  out × (1 − min(res, cap))
                               cap = 0.80 player / 1.00 monster                [I, E-2 G-4]
                               Normal-difficulty player res penalty = 0        [M, E-2.3]

M1-STEP 4  TAIL CHANNEL (DA)   ladder multiplier from PTH                      [M, E-2.1] — §2.5
```

### 2.3 Armor channel — the operator

```
def gd_armor_through(raw: float, armor: float, absorption: float = 0.70) -> float:
    if raw > armor:
        return raw - absorption * armor          #  DGP branch  (E-2.1)
    return raw * (1.0 - absorption)              #  DLEP branch (E-2.1)
```

Both branches are verbatim from `combatformulas.dbr`
(`physicalDamageDefenseEquationDGP` / `physcialDamageDefenseEquationDLEP` — the source's own typo
preserved in the extraction). The DGP branch simplifies from
`(P·(1−abs)) + (raw − P)` to `raw − abs·P` (E-2.1, graded **D**, arithmetic shown there).

**`sumAbsorptionDV` is the global 70 % and nothing else** — E-2.3 swept all 93,190 records and found
exactly one non-zero `defensiveAbsorption` (a sandbox record). Gear absorption is dead content.
**This is a clean simplification the spec relies on and names.**

**Continuity note (design, not source):** the operator is discontinuous in the *derivative* at
`raw = armor` but continuous in value (`armor − 0.7·armor = 0.3·armor`). No clamp is needed; output
is non-negative on both branches for `armor ≥ 0`. Assert it.

### 2.4 Resistance channel — and why it is the nova's door

Typed damage never touches armor. Player resistances on Normal difficulty carry **zero** difficulty
penalty (E-2.3, `balancingadjustment_mp+difficulty_players01.dbr`, Normal indices 0–3 all `0`), so
the player's cold resistance at the fixture band is **whatever gear gave him and nothing else.**

**Player cold resistance at the fixture band is UNKNOWN (U-2).** Kit spec v2 §1.6 records
*"+% cold res"* on head and *"+cold/+frostburn"* on legs without rolled magnitudes. M-1 exposes
`player_resistances["cold"]` as a **named unknown with a declared default of 0.20** and a sensitivity
sweep at {0.00, 0.20, 0.40}. The default is a **calibration constant, not a GD value** — labelled
as such in the artifact, per the extraction's G-3 instruction.

**This channel is the structural reason the nova is dangerous.** At r5 the nova is ~85 % cold
(247 of 395, E-1.2). Armor is inert against 247 of it. **That is G-A's "shape not scale" mechanism
sourced, and it is also G-B's killing mechanism** — one law, two gates. See M-2 §3.

### 2.5 The TAIL channel — Defensive Ability → PTH ladder (the shape operator that actually bites)

This channel is **not in the cell brief.** It is in the substrate (E-2.1) and the design arithmetic
(§5.3) says it carries more of the fixture's fall than armor does. Recording it is the point of
this section.

```
PTH   = probabilityToHitEquation(OA_attacker, DA_defender)     [M, E-2.1 verbatim]
        floored at pthMinimum = 55.0                            [M]
mult  = ladder(PTH):  70→1.0  90→1.1  105→1.2  120→1.3  130→1.4  135→1.5   [M]
```

A gear step that raises player **DA** lowers monster PTH, which **demotes the ladder tier**. The
ladder multiplies the hit — so this channel acts **selectively on the tail** (it removes the 1.4×
and 1.5× hits, which *are* the worst-drop statistic) while leaving the body near-untouched. That is
a shape operator in the strictest sense: it changes the distribution's upper quantiles by more than
its median.

Armor does the opposite. Re-read the §1 table: at a 125 armor step, a 74-raw hit loses 70 % but a
250.6-raw hit loses only 35 %. **Flat-subtraction armor compresses the BODY harder than the TAIL —
it makes the distribution relatively MORE tail-heavy.** Armor alone therefore pushes the G-A
statistic in the *wrong direction* relative to the median, and the worst-drop fall it can deliver is
bounded by `0.70 · ΔA` in absolute HP (§5.3).

> **Design headline, and the sentence to carry out of this spec:**
> **armor cuts the body; defensive ability cuts the tail.** G-A's statistic is a tail statistic.
> A mitigation model that is armor-only is fighting the gate with the wrong instrument.

**Build disposition:** the DA/PTH channel is spec'd as **DEFAULT-OFF behind its own flag**
(`WIRE_GD_PTH_LADDER`), because (a) the fixture's DA totals both sides of the boundary are
**UNMEASURED (U-3)** — kit spec v2 §1.6 records `+13 DA` (torso), `+20 DA` (aura, pre-step),
`+OA/+DA` (head, unrolled), `+DA mod` (gloves, unrolled) — and (b) turning it on without those
values is fitting. It is spec'd now so the build has the seam and galadriel has the target.

---

## §3 — THE GEAR STEP: what moves, and what is measured

| Quantity | W-c arm (pool 759) | R3 arm (pool 1607) | Grade |
|---|---|---|---|
| `max_hp` | 759.0 | 1607.0 | **M** (kit spec v2 §2, G-8-corrected) |
| `armor` | **`armor_r2` — UNKNOWN (U-4)** | ≥ 125.0 | post: **M-partial**; pre: **U** |
| itemised boundary armor step | — | **+65** = torso 58 + belt 7 | **M** (kit spec v2 §1.7/§1.6) |
| Amatok's Pact +16 armor | **on both sides** (switches on **mid-R2**) | on both sides | **M** (kit spec v2 §1.4/§1.7) |
| helm / gloves / shield armor | UNREAD | UNREAD | **U — the galadriel re-crop residual (§A-9.3)** |
| `DA` | UNKNOWN (U-3) | UNKNOWN (U-3) | **U** |
| `player_resistances["cold"]` | UNKNOWN (U-2) | UNKNOWN (U-2) | **U** |

**A correction the itemisation forces, recorded because it moves the arithmetic:** the Amatok's Pact
aura's **+16 armor arrives mid-R2, not at the boundary** (kit spec v2 §1.4: *"it switches on **mid-R2**"*;
§1.7: *"the aura's contribution arrives **mid-R2, not at the boundary**"*). It is therefore
**not part of the step** — it is on both sides. The `125.0` currently pinned in the harness is
`≥109 gear + 16 aura`; the *step* component of it is **65**, not 125. Any build that treats the whole
125 as the step over-states ΔA by ~1.9×.

**M-1 exposes `armor_r2` and `armor_r3` as separate declared inputs**, each carrying its grade, with
the assertion `armor_r3 − armor_r2 == armor_step` and `armor_step` defaulting to the **itemised 65**
[M]. Any other value must be supplied explicitly with a grade — the door does not accept an
un-graded armor step.

---

## §4 — ACCEPTANCE CRITERION (G-A), restated as one number

### 4.1 The gate simplifies to the absolute worst-drop ratio

Let `P` = pool, `D` = worst drop in absolute HP, subscripts `1` = pre-step, `2` = post-step.

```
normalized fall  =  (D₁/P₁) ÷ (D₂/P₂)  =  (D₁/D₂) · (P₂/P₁)
EHP ratio        =  P₂/P₁
G-A statistic    =  normalized fall ÷ EHP ratio  =  D₁ / D₂
```

> **G-A is exactly the ratio of the absolute worst drop across the gear step.**
> Fixture: 0.3302 × 759 = **250.6 HP** → 0.0738 × 1607 = **118.6 HP** → **2.113**. This reproduces
> §A-4's quoted **2.12** to three figures from the fixture's own p99 and pools — an independent
> arithmetic check on the gate's own statement, not a recomputation of a fixture goalpost.
> Sim: `worst_drop_abs` **identical on 143/150** → **1.000**.

This restatement is worth the ink: it converts a composite three-term gate into a single
directly-testable quantity, and it tells the builder exactly what to instrument —
`intake.worst_drop_abs`, which the harness **already emits** (`kitcal_g5_harness.py:272`). **No new
instrument is needed for G-A.**

### 4.2 The pre-registered predicate

**PRIMARY (composition-controlled, boss-free):** on the trash / champion / mixed_pack tiers — where
the sim's ratio today is **exactly 1.0000** on all three (§A-4.3) — the post-M-1 median
`worst_drop_abs` ratio must read **> 1.15**, i.e. the step must remove a measurable absolute bite.
Rationale for the floor: 1.15 is above the 0.26 % boss-tier numerical noise §A-4.3 measured by ~50×,
and below the §5.3 armor-only prediction of 1.22 — so a *correctly built* armor-only M-1 passes the
directional predicate and a *no-op* fails it. It is a discrimination threshold, not a target.

**SECONDARY (reference, NON-BINDING pending §5.5):** distance of the same statistic from the
fixture's **2.12**, reported per tier with the §5.4 confound named in the same table.

**FALSIFICATION:** if `worst_drop_abs` ratio still reads 1.000 ± 0.01 after M-1 lands, M-1 has not
changed shape and the mechanism is not built, whatever the normalized numbers say. This is the
§A-4.2 lesson applied forward — a predicate that a no-op satisfies is not a predicate.

---

## §5 — THE ARITHMETIC, run before the build (Discipline #1: math before code)

### 5.1 Setup

Take `D_raw` = the raw physical magnitude of the fixture's p99 hit; unchanged across the step (the
opposition did not get weaker because the player got a belt). Under §2.3's DGP branch:

```
D₁ = D_raw − 0.70·A₁          D₂ = D_raw − 0.70·A₂          ΔA = A₂ − A₁
D₁ − D₂ = 0.70·ΔA
```

### 5.2 What 2.12 requires

`D₁ = 250.6` and `D₁/D₂ = 2.113` ⟹ `D₂ = 118.6` ⟹ `D₁ − D₂ = 132.0` ⟹ **`ΔA = 188.6`.**

### 5.3 What the substrate supplies

Itemised boundary armor step = **65** (torso 58 + belt 7; §3). ⟹ `D₁ − D₂ = 0.70 × 65 = 45.5`
⟹ `D₂ = 205.1` ⟹ **ratio = 1.221.**

> **Armor as measured delivers 1.22 of the required 2.12.** Even attributing the entire pinned 125 —
> including the aura that sits on both sides — gives `0.7 × 125 = 87.5` ⟹ ratio **1.54**. Even
> adding a generous 55 armor of unread helm + gloves + shield to the *step* (which the +Health
> attestation does not support — those three slots are not part of the four attested step items)
> gives ΔA = 120 ⟹ ratio **1.51**. **No defensible reading of the armor evidence reaches 2.12.**

### 5.4 Where the remaining factor of ~1.7 lives — four candidates, ranked, none fitted

1. **COMPOSITION CONFOUND (leading candidate; the one that would make G-A partly unreachable).**
   The fixture's R2 max drop **is death 2** — `play_time` 5447–5450, drop 541 on a 747 pool,
   72.42 %, floor-censored (kit spec v2 §C-6). The R2 window contains the Primordian. The R3 window's
   max drop is **8.50 %**. If R3 carries no boss- or hero-tier opposition, then a large part of the
   fixture's fall is *"he stopped fighting the thing that hit hard,"* not *"his gear absorbed more."*
   **The sim's two arms run the identical battery** — composition is *designed* and controlled. A
   composition-driven component of the fixture's 2.12 is therefore **structurally unreachable by any
   sim-side mitigation model**, and pursuing it with mitigation parameters is fitting a confound.
   This is §A-8.3's own general rule — *"a fixture-side statistic does not keep its meaning when
   carried onto a designed battery"* — arriving for the third time in this run's history.
   **STATUS: unmeasured. Closable by a fixture-side opposition-tier audit of the R3 window
   (elrond/galadriel, ~1 query against `fixtures.db`). Named, not assumed.**
2. **DA / PTH ladder demotion (§2.5).** A 1.5× → 1.2× ladder demotion is a factor **1.25** on the
   tail alone. Combined with armor's 1.22 this reaches **1.53**. Plausible, sizeable, and **U-3**.
3. **Cold / typed resistance step.** Head, shoulders, gloves and legs all carry `+%` typed
   resistance (kit spec v2 §1.6) with magnitudes unrolled. **U-2.**
4. **Level-up base defense** between the windows (levels 11→13 in the same bracket; kit spec v2 §1.7
   attributes +104 of the HP residual to exactly this). **Small; U.**

### 5.5 ⚠ RULING REQUEST TO THE CONDUCTOR (veto-open; this spec does not decide it)

**M-1 as specified will, on the measured armor evidence, land ≈1.22 and MISS 2.12.** Three
dispositions; the spec states its lean and does not act on it.

- **(a) Hold 2.12 binding.** M-1 reports ≈1.22, G-A grades **MISS**, honorable-fallback §2 fires,
  residue named (composition confound + U-2/U-3/U-4). Nothing is bent. **Cost:** a gate miss that
  is arguably an instrument defect rather than a build defect.
- **(b) SPLIT the gate — CONDUCTOR'S LEAN.** G-A grades on the §4.2 **primary directional predicate**
  (composition-controlled tiers, ratio > 1.15 against today's exact 1.0000) and carries **2.12 as a
  NON-BINDING reference** until (i) the R3 composition audit and (ii) galadriel's armour + DA re-crop
  return. Both are cheap and both are already owed (§A-9.3). **This is not a weakened gate — it is
  the same gate on an instrument the sim can actually be graded against**, plus a named open
  attribution. The directional predicate is *stronger* than 2.12 in one respect: 2.12 is satisfiable
  by a confound, while a move off exactly-1.0000 on a controlled battery is satisfiable only by
  mitigation shape.
- **(c) Fit `armor_step` to 188.6.** **REJECTED by this spec.** It re-opens the free parameter
  kit spec v2 §1.7 retired, contradicts the itemised 65 with no evidence, and manufactures a PASS.
  Recorded so the option is visibly refused rather than silently unavailable.

---

## §6 — SIMPLIFICATION LEDGER (GD truth → sim abstraction; every divergence named)

| # | GD truth (grade, source) | Sim abstraction | Why | Risk |
|---|---|---|---|---|
| SL-1 | Six-region hit-location roll selects **which armour piece** supplies `sumProtection` (M, E-2.1) | **Single scalar `armor`**; no region roll | Player armor is a compiled total in the kit spec; per-slot values are partly UNREAD | Understates per-hit variance. GD's regions are 26/20/15/15/12/12 — a roughly flat draw over pieces of similar magnitude, so the mean is well-approximated. **Named; low.** |
| SL-2 | `combatRegion*Chance` applicability to monsters is **I** (E-2 G-8) | No-op on the monster side (`sumProtection` slot-invariant) | E-2's own reading | None inbound |
| SL-3 | Resistance **application operator** (hard clamp vs soft) is **I** (E-2 G-4) | **Hard clamp** at `playerDefenseCap = 80` | Field naming is unambiguous; operator is not | Only bites above 80 % res. Fixture is nowhere near. **Low.** |
| SL-4 | Monster absorption after `defensiveAbsorptionModifier = −20` is **56 % (convention) or 50 % (literal)** — E-2 G-6, source states neither | **0.56**, exposed as `monster_absorption` | Convention-consistent reading, named per E-2's instruction | ±6 pp on player→mob damage. **Does not touch G-A** (G-A is an incoming-damage statistic). **Named; inert for this gate.** |
| SL-5 | `damageAbsorptionPercent` / `offensiveTotalDamageModifier` / `defensiveTotalDamageModifier` stacking is **U** (E-2 G-5; unchanged from KC1) | **DO NOT COMPOSE.** Not modelled | The extraction's explicit instruction | A whole mitigation family absent. Carried unchanged from KC1. **Named.** |
| SL-6 | Block: `dmg > shieldDefense → dmg − shieldDefense·(shieldAbs/100)` else `dmg × ((100−shieldAbs)/100)` (M, E-2.1) | Block **out of M-1 scope**; existing door values (`block_chance 0.18`, `block_value 0.0`) untouched | KC1 §11.2 falsified block as *the* mitigation mechanism; re-opening it here would widen the cell | `block_value = 0.0` makes blocks damage-neutral — a known door literal (D-3). **Named; unchanged.** |
| SL-7 | PTH ladder + `pthMinimum = 55` (M) | **Flagged default-OFF** (`WIRE_GD_PTH_LADDER`) | DA inputs are U-3 | The channel §5.4 ranks #2. **Named as the largest deliberate omission in M-1.** |
| SL-8 | Attribute scaling `physical × ((dex/245)+1)` / `magical × ((int/215)+1)` (M, E-2.1 STEP 3) | **Not adopted**; RDR's `compute_damage_scaling` retained | Changing attacker-side scaling reaches RDR production math | Divergence is on the *attacker* side, common to both arms → cancels in the G-A ratio. **Named; inert for this gate.** |
| SL-9 | Fixture "drop" = a fall over an **engagement-sample interval** (death-2: 541 HP over `play_time` 5447–5450, ~3 s); sim "drop" = **one received hit** (`kitcal_g5_harness.py:271`) | Grain asymmetry accepted | Both G-A operands are computed **sim-side on the same instrument**, so the *ratio* is grain-invariant even though the *levels* are not | Affects the 2.12 comparison, not the >1.15 predicate. **Named — and it is a second, independent reason §5.5(b) is the sounder grading.** |

---

## §7 — NAMED UNKNOWNS carried into the build

| # | Unknown | Source | Disposition |
|---|---|---|---|
| **U-1** | Monster absorption after −20 % modifier: 56 % vs 50 % | extraction G-6 | `monster_absorption = 0.56` [I], exposed, swept at {0.50, 0.56} |
| **U-2** | Player cold / typed resistance at the fixture band | kit spec v2 §1.6 (unrolled) | `player_resistances["cold"] = 0.20` **calibration constant, not a GD value**; swept {0.00, 0.20, 0.40} |
| **U-3** | Player Defensive Ability, both sides of the boundary | kit spec v2 §1.6 (unrolled) | DA/PTH channel **default-OFF**. Galadriel re-crop target |
| **U-4** | Player armor on the W-c side (`armor_r2`) | never itemised | Declared input; `armor_r3 − armor_r2 == armor_step` asserted; `armor_step = 65` [M] default |
| **U-5** | Resistance-cap operator (hard vs soft) | extraction G-4 | Hard clamp [I], SL-3 |
| **U-6** | TDM stacking | extraction G-5, unchanged from KC1 | **Not composed** |
| **U-7** | Whether the fixture's R3 window carries boss/hero-tier opposition | this spec, §5.4 | **NEW — the highest-value cheap close in this document.** Routed to the conductor |

Extraction gaps **G-1 (windup)** and **G-3 (base attack interval)** do not touch M-1; they are M-2 /
M-4 items.

---

## §8 — BUILD NOTE FOR GAMORA

**You own:** the implementation math note (Discipline #1, before code), the tests, and jack-ryan
Gate-2 on the landing (kernel-touching — charter §3 makes this MANDATORY, not optional).

**Landing shape (recommendation, not prescription — the seam is yours):**

1. **Door-scoped, production-inert.** New behaviour reachable only via `_calibration_overrides`.
   Door-closed combat digest **byte-unmoved** — the O-d/R-KC1-17 precedent at
   `spatial_engine.py:2564+` is the pattern, including its no-new-RNG-draw property. **Do not add an
   RNG stream.** Every §2 operator is deterministic.
2. **Two flags, independently testable:** `WIRE_GD_ARMOR_OPERATOR` (§2.3) and `WIRE_GD_PTH_LADDER`
   (§2.5, default OFF). Grade G-A with the second OFF first — that is the honest armor-only reading
   and it is what §5.3 predicts at 1.22.
3. **Per-arm armor.** `armor_r2` / `armor_r3` in the door, with the `armor_step` assertion (§3).
   An un-graded armor step must raise.
4. **Assertions worth having** (the A-* pattern from the G-5 harness): `A-M1-1` door-closed digest
   unmoved · `A-M1-2` `armor_r3 − armor_r2 == armor_step` · `A-M1-3` armor is **never** consulted on
   a typed-element hit (the D-1 law, asserted so it cannot silently regress) · `A-M1-4` DGP/DLEP
   branch coverage — both branches exercised in the battery, reported with counts (a battery that
   never crosses `raw = armor` has not tested the shape operator, and §5.3's whole claim is about
   which branch the hits land in).
5. **Report `worst_drop_abs` ratio per tier explicitly** in the battery report, alongside the
   existing normalized fields. G-A reads it directly (§4.1). Do not make the grader re-derive it.
6. **`A-M1-4` is the one I most expect to be surprising.** If the battery's incoming hits are
   mostly *below* the armor value, they take the DLEP `×0.30` branch — a 70 % cut on nearly
   everything — and the ratio will overshoot 1.22 substantially. That is not a bug and it is not a
   pass; it is a **finding about the sim's damage magnitudes** relative to the fixture's, and it
   should be reported as one. §A-4.3's *"narrow band of constant chip"* (median worst drop 45.9–59.2
   HP absolute) sits **below** a 125 armor value — so on the current battery I predict the **DLEP
   branch dominates.** Measure it; do not assume my prediction.

**You do not own:** the §5.5 ruling (conductor's), the R3 composition audit (U-7, conductor routes),
the armour/DA re-crop (galadriel).

---

## §9 — WHAT THIS SPEC DELIBERATELY DOES NOT DO

- Does not touch `ARMOR_MITIGATION_K` or production `compute_physical_damage` (§2.1).
- Does not fit `armor_step` to the gate (§5.5 c, refused on the record).
- Does not compose TDM (SL-5), re-open block (SL-6), or adopt GD attacker-side attribute scaling
  (SL-8).
- Does not model the six-region hit-location roll (SL-1).
- Does not claim the nova's cold bypass is an M-1 deliverable — it is shared law, and it *fires* in
  M-2 (§2.4).

**Signed:** gandalf (`SPEC-AUTHOR`), 2026-07-29. Veto-open per the WR1 ruling ledger.
