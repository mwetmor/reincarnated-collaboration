# KC2-SIM — F-13: count-model discrimination against the fourth extraction

**Date:** 2026-08-08
**Author:** named-gandalf sub-agent, role-tag **DRIFT-CRITIC** (judging a model of record — my own § 10.5 —
against independent evidence)
**Status:** WORKING — evidentiary/verdict note, conductor commission at ledger **L-44**
**Commit state:** UNCOMMITTED by instruction. Rides the conductor's G-D gate-close unit.
**Scope guard:** analysis only. No spec edit, no ledger edit, no other agent's note touched, nothing committed.
**Evidence in:** `galadriel/notes/2026-08-08-kc2-fourth-extraction.md` (blind census) ·
`galadriel/notes/2026-08-08-kc2-third-extraction.md` · `galadriel/notes/2026-08-08-kc2-board-closure.md` ·
`jack-ryan/notes/2026-08-08-kc2-gate2-phase-d.md` § 2.3 · `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`
§ 10.4 / § 10.5 / F-9 / F-10
**Substrate:** `legolas/scratch/2026-08-08-kc2-e2-exemption/pe6_crucible_wave_pools_v2.csv` (1,998 rows,
200 waves, per-wave-per-spawn-point, full rosters + record paths)

---

## 0. Instrument calibration — before any claim

Every number below was recomputed from the v2 CSV by an instrument written for this note. Before using it
I reproduced the model of record end to end:

```
§ 10.5 CITED-exemption + no-op-on-empty, waves 151-170, p06 OFF   ->  271.50 regulars / 63.00 champions
                                              same, empty = "+1"  ->  292.50 / 63.00
                                              p06 ON,  no-op      ->  290.17 / 81.00
                                              p06 ON,  "+1"       ->  317.17 / 81.00
```

All four land **exactly** on F-10's and jack-ryan § 2.2's published cells. jack-ryan's CONJURE−NO_OP
w-lattice also reproduces exactly (`w151 2 · w152 3 · w153 2 · w157 2 · w158 2`, band 21.00) — it is the
count of *spawn points whose selected alternative has an empty regular roster*, one conjured body each.
The instrument is calibrated. Everything after this is measured on it.

**One methodological pin that governs every verdict below.** galadriel observed **one realization** of each
wave, censored from below. A model is therefore falsified **only when the observed lower bound exceeds the
model's support maximum** — not its expectation. Exceeding the expectation is a sampling event; exceeding
the *maximum achievable draw* is a contradiction. Every FALSIFIED grade in this note is support-based.
Undershoots are graded UNINFORMATIVE without exception.

---

## 1. Q1 — IDENTITY JOIN. Verdict: **31 of 33 plates ROSTERED; exactly ONE body is un-rostered corpus-wide.**

### 1.1 The join

33 plate reads (galadriel § 5's 30, plus the three w151 second-stream reads she carries forward at § 8.2)
joined against `roster_names` + `champ_names` for their own wave, p06 excluded, exact match then
Levenshtein-close fallback at 0.80.

| # | wave | +off | name | colour | grade | roster location |
|--:|--:|--:|:--|:--|:--|:--|
| 1 | 151 | 4.00 | Spiteful Wraith | yellow | ROSTERED | p1/p4 trash **REG** `wraith_t3` |
| 2 | 151 | 4.40 | Ancient Wraith | yellow | ROSTERED | p1/p4 trash **REG** `wraith_t3` |
| 3 | 151 | 5.60 | Tildoom ~ Timewarped | orange | ROSTERED | p2 HERO **CHP** `wraith_hero` |
| 4 | 151 | 7.20 | Arcanom the Soulthief | orange | ROSTERED | p2 HERO **CHP** `wraith_hero` |
| 5 | 151 | 8.80 | Wraith | white | ROSTERED | p1/p4 trash **REG** `wraith_t3` |
| 6 | 151 | 10.10 | Carnivorous Plant | white | ROSTERED | p5 trash **REG** `livingplant_t3` |
| 7 | 151 | 12.70 | Carnivorous Plant | white | ROSTERED | p5 trash **REG** `livingplant_t3` |
| 8 | 151 | 13.50 | Ferrosius ~ Swift | orange | ROSTERED | p3 HERO **CHP** `swampgolem_hero` |
| **9** | **152** | **0.40** | **Carnivorous Plant** | white | **UN-ROSTERED (this wave)** | absent from w152; present w151 p5 · w153 p5 `livingplant_t3` |
| 10 | 152 | 3.00 | Mudflinger ~ Reflective | orange | ROSTERED | p1 HERO **CHP** `swampcrab_hero` |
| **11** | **152** | **3.40** | **Ugdenbog Crabling** | white | **UN-ROSTERED (corpus)** | **matches nothing in 1,492 names / 1,617 records** |
| 12 | 152 | 3.80 | Chaosshell ~ Voidtouched | orange | ROSTERED | p1 HERO **CHP** `swampcrab_hero` |
| 13 | 152 | 5.00 | Chillslither ~ Arctic | orange | ROSTERED | p2 HERO **CHP** `basilisk_hero` |
| 14 | 152 | 7.40 | Stonegaze Basilisk | white | ROSTERED | p3 trash **REG** `basilisk_t3` |
| 15 | 152 | 8.40 | Fleshweaver Haraxis | violet | ROSTERED | p4 BOSS **REG** `aetherialfleshshaper_haraxis` |
| 16 | 152 | 8.80 | Juvenile Basilisk | white | ROSTERED | p3 trash **REG** `basilisk_t3` |
| 17 | 153 | 3.80 | Wendigo ~ Ancient | **orange** | ROSTERED | p1 trash **REG** `wendigo_t3` |
| 18 | 153 | 4.20 | Wendigo | white | ROSTERED | p1 trash **REG** `wendigo_t3` |
| 19 | 153 | 6.80 | Storm Revenant | yellow | ROSTERED | p3 trash **REG** `skeletonrevenant_t3` |
| 20 | 153 | 7.40 | Frost Revenant | yellow | ROSTERED | p3 trash **REG** `skeletonrevenant_t3` |
| 21 | 153 | 7.60 | Ugdenbog Golem | yellow | ROSTERED | p5 trash **REG** `livingplant_t3` |
| 22 | 153 | 8.00 | Carnivorous Plant | white | ROSTERED | p5 trash **REG** `livingplant_t3` |
| 23 | 157 | 2.80 | Diremane Brute | yellow | ROSTERED | p4 trash **REG** `yetidire_t3` |
| 24 | 157 | 6.80 | Starhorn ~ Celestial | orange | ROSTERED | p2 DEVOTION **CHP** `devotion_heroes01/03` |
| 25 | 157 | 7.60 | Blugrug the Living Plague | violet | ROSTERED | p1 BOSS **REG** `aetherialbloater_malmouthdocks` |
| 26 | 157 | 8.80 | Chthonian Bloodkeeper | yellow | ROSTERED | p3 trash **REG** `chthonianservitor_t3` |
| 27 | 158 | 1.80 | Chthonian Devourer | yellow | ROSTERED | p1/p3/p4 trash **REG** `chthoniandevourer_t3` |
| 28 | 158 | 3.80 | Ugdenbog Spikeshell | white | ROSTERED | p1/p3/p4 trash **REG** `swampcrab_t3` |
| 29 | 158 | 4.20 | Ugdenbog Crab | white | ROSTERED | p1/p3/p4 trash **REG** `swampcrab_t3` |
| 30 | 158 | 5.80 | Culldar Endbringer ~ Celestial | orange | ROSTERED (fuzzy, 1 char) | p5 HERO **CHP** `wraith_hero` = *Tulldar* Endbringer ~ Celestial |
| 31 | 158 | 6.20 | Arcanom the Soulthief | orange | ROSTERED | p5 HERO **CHP** `wraith_hero` |
| 32 | 158 | 6.60 | Sandclaw ~ Matriarch | **orange** | ROSTERED | p1 trash **REG** `sandlizard_t3` |
| 33 | 158 | 7.80 | Sandclaw | white | ROSTERED | p1 trash **REG** `sandlizard_t3` |

**Tally: 30 exact ROSTERED · 1 fuzzy ROSTERED · 2 UN-ROSTERED. Zero ROSTER-OTHER-POINT** (every hit is at a
point that exists for that wave). **Zero UNIDENTIFIABLE** among plated bodies; the 69 max-HP fingerprints
carry no independent identity channel (level is drawn per body — her § 2.6 — so HP cannot be inverted to a
record), so **91 of ~113 bodies are UNIDENTIFIED, not un-rostered.** That asymmetry is load-bearing and is
carried into every verdict below.

### 1.2 The two un-rostered candidates, adjudicated separately

**(A) w152 +0.40 s "Carnivorous Plant" — grade UNDECIDABLE, lean CARRYOVER.**
`livingplant_t3` is w151's **p05 ambush pool** and w153's p05 pool. It is not in w152 at any point:
w152's full 6-point roster space is 117 distinct names and contains **zero** Plant/Golem entries.
Competing readings:
- *Carryover.* +0.40 s is the smallest offset in the corpus; the badge flipped at 698.38; galadriel reports
  three w152 fingerprints present pre-flip (§ 1.3); w151's own second stream was Carnivorous Plants as
  recently as t = 694.8. The plate instrument (cursor hover) is **not** the readout instrument, so her
  "no body persists ≥ 3 frames past its flip" — a statement about readouts — does not close it.
- *Conjure.* Fails on family: a CONJURE_FROM_TEMPLATE body at w152 would inherit its pool's own creature
  family (crab at p1, basilisk/thorned-horror at p2, aetherial-corruption at p5). **No w152 pool is
  Plant·Eldritch.** The conjure hypothesis does not predict this body.
- **UNDECIDABLE** by galadriel's censoring; but the conjure branch is the *worse* fit of the two.

**(B) w152 +3.40 s "Ugdenbog Crabling" — grade UN-ROSTERED, MEASURED. This is the loudest single output.**

Exhaustive negative search on the substrate:
```
'Crabling' as literal in the 1,250,890-byte CSV ..................... ABSENT
'crabling' in any of the 1,617 monster record paths ................. ABSENT
corpus names containing 'crab'/'shell' (12 total) ... Chaosshell~Voidtouched, Corrupshell~Corrupted,
   Foll the Burningshell, Goll the Stormshell, Haunted Crab, Haunted Spikeshell, Haunted Stoneshell,
   Thornshell~Bramble, Ugdenbog Crab, Ugdenbog Spikeshell, Ugdenbog Stoneshell, Voidshell~Voidtouched
'Ugdenbog Crab' appears at waves ......... 62, 106, 158, 167, 191   -- NOT 151, NOT 152, NOT 153
```
So the un-rostered verdict is **robust to the obvious eye-read failure**: even if "Crabling" is a misread of
"Ugdenbog Crab", that name is *also* absent from w152 and from both neighbouring waves, so no carryover
route exists. Either way, w152 carried a swampcrab-family **common** body that no w152 pool can produce.

**Where it sits is the interesting part.** The two plates bracketing it — *Mudflinger ~ Reflective* (+3.00)
and *Chaosshell ~ Voidtouched* (+3.80) — are both `swampcrab_hero` champion entries, which uniquely
identifies w152 **p01's selected alternative as `swampcrab_hero`**. That pool is **non-exempt with
`roster_n = 0`** — i.e. it is precisely one of the three empty-roster alternatives that jack-ryan's CONJURE
lattice says w152 should conjure from. An un-rostered, common-rank, swampcrab-family body appeared at the
right point, in the right family, inside a 0.8 s window bracketed by that pool's own champions.

**And yet this does not settle CONJURE — because of the control.**

### 1.3 The control that keeps the un-rostered class ambiguous

`"Aleksander's Shard"` — camera-read at wave 160, three frames, fingerprint 103,912 ×2, plain furniture,
level 109, graded **SUMMON** by galadriel (third extraction § 2.1) — is **also absent from the 1,492-name
corpus**. So is the un-rostered class's magnitude at w160: the fully-closed w160 board is 4 skull bodies
(Aleksander, Zantarin, Kubacabra, Galakros) plus **seven plain bodies** (Aetherial Bileeater, Death
Revenant, Aleksander's Shard ×2, Skeletal Archer ×3) against a count model that predicts **zero** regulars
on that wave.

> **UN-ROSTERED ≠ CONJURED. The class has at least two mechanisms and one of them — monster summoning — is
> already MEASURED in this footage, at a volume (7 un-rostered plains against 4 rostered bodies, 175 %)
> that dwarfs the conjure branch's +1-per-point.**

The wave-160 summons were detectable only because their level inherited the *nemesis* value 109, outside the
102–108 regular band. **On waves 151–158 every plausible summoner is inside the band** (bosses read 108,
heroes 106–108), so galadriel's level-inheritance test — her strongest summon discriminator, 22/22 clean —
**has no power on these five waves.** Her "zero SUMMON" grading is a true statement about the *signature*,
not about the *population*.

### 1.4 A structural correction the join forces, and it is not small

The join shows the **regular limb carries champion- and hero-rank monsters**:

| plate | colour galadriel read | DB limb it is drawn from |
|:--|:--|:--|
| Spiteful Wraith · Ancient Wraith (w151) | yellow → champion | `wraith_t3` **REGULAR** roster |
| Storm Revenant · Frost Revenant (w153) | yellow → champion | `skeletonrevenant_t3` **REGULAR** |
| Ugdenbog Golem (w153) | yellow → champion | `livingplant_t3` **REGULAR** |
| Diremane Brute · Chthonian Bloodkeeper (w157) | yellow → champion | `yetidire_t3` / `chthonianservitor_t3` **REGULAR** |
| Chthonian Devourer (w158) | yellow → champion | `chthoniandevourer_t3` **REGULAR** |
| **Wendigo ~ Ancient (w153)** | **orange → hero** | `wendigo_t3` **REGULAR** |
| **Sandclaw ~ Matriarch (w158)** | **orange → hero** | `sandlizard_t3` **REGULAR** |

Rank is a property of the **monster record**, not of the proxypool limb that drew it. Therefore:

> **AC-10.4's "63.00 expected champions" counts `nameChampion{j}` DRAWS. galadriel's "23 star-pair bodies"
> counts RANK FURNITURE. These are different populations and the second is a superset of the first
> whenever a regular roster contains a champion- or hero-classified record — which it demonstrably does, on
> 4 of the 5 waves.** Scoring one against the other is a category error.

This retires the commissioning brief's premise that "champion star-pairs exceed selection champs on
151/153/158." Reproduced, the champion limb **never** overshoots (§ 2.2), and the star/champion comparison
is not the right comparison in the first place.

---

## 2. Q2 — MODEL DISCRIMINATION

### 2.1 The furniture ↔ limb mapping used (declared)

`PLAIN` ← regular limb of **trash** pools · `SKULL` ← regular limb of **BOSS** pools · `STAR` ← champion
limb, any pool. Per § 1.4 this mapping is **known incomplete on the STAR side** (rank-carrying regular
records get furniture the model books as PLAIN). Consequence: STAR is scored **one-sided only** — a STAR
undershoot is uninformative twice over.

### 2.2 The three limbs, model of record (M1 = § 10.5 CITED + no-op, p06-OFF)

p05 policy: **EXCLUDED for w151, INCLUDED for the other four** — and that is measured, not chosen.
w151's cohort closes at +3.97, nothing arrives until **+8.47**, and the bodies that then arrive are
`livingplant_t3` (Carnivorous Plant ×2, plated +10.1/+12.7) which is **w151's p05 pool and nothing else's**.
p05 fires at t+4.0 (DB) ⇒ a measured spawn→render lag of **4.47 s**, inside galadriel's 3.5–6.1 s band.
Two instruments, one conclusion: **w151's census window contains p01–p04 only.** For 152/153/157/158 the
p05 render lands at ≈ +8.5 s and the windows close at 10.23 / 8.60 / 8.63 / 8.33 — straddling. Including
p05 there is the **generous-to-M1** choice and is what is tabled.

| wave | PLAIN E / sup | obs | verdict | STAR E / sup | obs | verdict | SKULL E / sup | obs | verdict |
|--:|--:|--:|:--|--:|--:|:--|--:|--:|:--|
| 151 | 16.00 / 18 | 9 | uninformative | 6.00 / 6 | 3 | uninformative | 0 / 0 | 0 | — |
| **152** | **7.00 / 7** | **17** | **FALSIFIED +10** | 9.00 / 9 | 6 | uninformative | 1.75 / 2 | 1 | uninformative |
| **153** | **17.50 / 18** | **23** | **FALSIFIED +5** | 6.00 / 6 | 4 | uninformative | 0 / 0 | 0 | — |
| **157** | **12.38 / 14** | **15** | **FALSIFIED +1** | 6.00 / 6 | **6** | **EXACT** | 2.00 / 2 | 1 | uninformative |
| 158 | 27.00 / 36 | 24 | uninformative | 6.00 / 6 | 4 | uninformative | 0 / 0 | 0 | — |

Derivations, shown:
```
w152 PLAIN, p3 only:  basilisk_t3      (5,6) -> nmin=floor((5+1)*1.2)=7 , nmax=6+1=7  -> 7 DETERMINISTIC
                      thornedhorror_t3 (5,6) -> 7 , 7                                 -> 7 DETERMINISTIC
                      p1/p2/p5 are HERO pools, roster_n=0, no-op -> 0
                      => support = {7}. ZERO WIDTH. Observed 17.
w153 PLAIN:  p1 wendigo_t3       (4,5) -> floor(5*1.2)=6 , 6            -> 6 det
             p3 skeletonrevenant (6,6) -> floor(7*1.2)=8 > 7 -> clamp 7 , 7 -> 7 det
                giant_t3         (5,6) -> 7 , 7                          -> 7 det
             p5 livingplant_t3   (3,4) -> floor(4*1.2)=4 , 5             -> {4,5}
             => support = {17,18}. Observed 23.
w157 PLAIN:  p3 max over {leech 7, rylok 6, servitor 6, gargoyle 5} = 7
             p4 max over {skeletalgolem 7, aetherialbloater 7, swampgolem 6, yetidire 7} = 7
             => support max = 14. Observed 15.
```

> **The model of record's regular limb is FALSIFIED on three of five waves, at the support maximum, with
> zero sampling defence on w152 (the limb is deterministic there). This is the run's first hard COUNT
> contact and it is not a tolerance question — T-2's 1.9 % has nothing to say about 17 against a
> deterministic 7.**

The **STAR limb is unfalsified on all five waves**, and w157's 6/6 is a positive control: the instrument
*can* reach the champion expectation, so the undershoots at 151/152/153/158 are engagement censoring, not
model error. **AC-10.4's 63.00 survives this pass untouched.**

The **SKULL limb** is unfalsified (all undershoots) but see § 2.5.

### 2.3 The formal lattice — 64 configurations, 12 survivors

Axes: `trash_rule ∈ {SELECT, ALL}` × `champ_rule ∈ {SELECT, ALL}` × `boss_rule ∈ {SELECT, ALL}` ×
`empty ∈ {NO_OP, CONJURE}` × `champ_additive ∈ {ADD(+2→3), RAW(1)}` × `boss_additive ∈ {ON, OFF}`.
Scored against 5 waves × 3 furniture classes on support.

```
SURVIVORS: 12 / 64
marginals:  trash_rule  ALL 12 / 12      <- SELECTION ON TRASH POINTS IS FALSIFIED
            empty       CONJ 12 / 12     <- NO_OP IS FALSIFIED
            champ_rule  SEL 4  ALL 8     <- UNDECIDED
            boss_rule   SEL 6  ALL 6     <- UNDECIDED
            champ_add   ADD 8  RAW 4     <- UNDECIDED
            boss_add    ON 6   OFF 6     <- UNDECIDED
```
Named cells:
```
trash=SEL champ=SEL boss=SEL empty=NO_OP  (= M1, MODEL OF RECORD) -> FAILS w152(17>7) w153(23>18) w157(15>14)
trash=SEL champ=SEL boss=SEL empty=CONJ   (= M1 + F-9's +1)       -> FAILS w152(17>10) w153(23>20)
trash=SEL champ=ALL boss=SEL empty=NO_OP  (the brief's mixture)   -> FAILS w152(17>7)  w153(23>18) w157(15>14)
trash=ALL champ=SEL boss=SEL empty=NO_OP                          -> FAILS w152(17>14)
trash=ALL champ=SEL boss=SEL empty=CONJ                           -> SURVIVES
trash=ALL champ=ALL boss=ALL empty=NO_OP  (naive all-pools)       -> FAILS w152(17>14)
```

Three things follow immediately.

1. **F-9's `+1` alone does not rescue the count.** Machine-confirmed: jack-ryan's lattice magnitude
   (+2/+3/+2/+2/+2, band 21.00) is the wrong size *and the wrong shape* for the measured overshoot
   (+0/+10/+5/+1/+0). The correlation between his per-wave prediction and the measured overshoot is
   effectively nil.
2. **Naive all-pools is also falsified** — by w152, which has only two trash alternatives (7+7=14 < 17).
   The brief's expectation that all-pools would be falsified "on BOSS points" is not where it dies;
   it dies on the trash limb of the single sparsest wave.
3. **The lattice's only survivors require BOTH `trash=ALL` AND `CONJURE`.** Neither alone survives.

### 2.4 …and why I do **not** endorse the lattice's answer

`trash=ALL` multiplies the band by **2.33×–2.84×** (§ 4). It also implies w158 carries **81 regular bodies**
and w157 **51**, against a minimap eye-read that peaks at ≈ 14 and ≈ 11 icons respectively. Icon merging
and minimap radius blunt that objection but do not remove a 5.8× gap. Before endorsing a 2.8× band
correction I ran the decomposition the lattice cannot see.

**The HP decomposition — the finding that reframes the whole question.** Largest-ratio gap located by an
unsupervised rule (max consecutive ratio in the sorted plain-body fingerprint set), then the population
split counted:

| wave | plains | M1 sup | over | largest gap in the plain set | below gap | **above gap** | M1 support |
|--:|--:|--:|--:|:--|--:|--:|:--|
| 151 | 9 | 18 | −9 | 1.62× (139,400 → 225,874) | 3 | 6 | {16..18} — censored, no test |
| **152** | **17** | **7** | **+10** | **2.53× (93,599 → 237,258)** | **10** | **7** | **{7} — EXACT, deterministic** |
| **153** | **23** | **18** | **+5** | **5.37× (37,840 → 203,039)** | **5** | **18** | **{17,18} — EXACT, at the top** |
| 157 | 15 | 14 | +1 | 1.31× (304,994 → 398,226) — **no break** | 7 | 8 | — |
| 158 | 24 | 36 | −12 | 2.23× (42,446 → 94,715) | 6 | 18 | {…36} — censored, no test |

> **On both waves that falsify the model, the plain bodies *above* a clean HP break number EXACTLY the
> model of record's support — 7 (zero-width) and 18 (top of a two-point support). The entire overshoot is a
> second population, separated by 2.5× and 5.4× in max HP, that the count model does not represent at all.
> The two waves with no clean break (151, 157) show no such structure.**

Two independent exact landings, from an unsupervised split rule. That is not proof — but it is a far
better-behaved hypothesis than a 2.8× global multiplier, and it says something different:

**The count model's trash limb is not WRONG. It is INCOMPLETE.** It reproduces the rostered trash
population exactly and is silent about a second, low-HP population.

Candidate mechanisms for that second population, all NAMED, none fitted:
- **(i) Summoned minions.** Precedent MEASURED in this footage (w160: 7 un-rostered plains, incl.
  41,237 ×3 and 103,912 ×2 — the same 40 k–104 k band as w152's 42,798 ×4 / 43,548 ×3 / 91,696 / 93,599 ×2
  and w153's 37,840 ×4 / 16,368). Undetectable on 151–158 because the level test has no power (§ 1.3).
- **(ii) p05 replenishment.** `minGroupSize = maxGroupSize = 30`, `spawnThreshold = 15`,
  `min/maxSpawnTime = 3.0 s`, `min/maxDelayTime = 4.0 s` (§ 10.6). The adopted model emits the pool budget
  **once**; a replenishing reading emits every 3 s while live count < 15. Sensitivity, w153:
  `p01–p04 sup 13 + n × p05 sup 5` → n=1 → 18 **FAILS** · **n=2 → 23 — EXACTLY the observation** ·
  n=3 → 28 clears. And w153's p05 pool is `livingplant_t3`, whose two members galadriel **plated in-window**
  (Ugdenbog Golem +7.60, Carnivorous Plant +8.00). This limb is § 10.6's own declared-undetermined flag
  (*"whether maxGroupSize caps concurrency independently of the pool budget is not determinable"*).
  It does **not** explain w152, whose p05 is a hero pool with an empty regular roster.
- **(iii) CONJURE on empty rosters.** Explains at most +3 on w152, +2 elsewhere. Alone: insufficient.
  Supported on w152 by the identity leg (§ 1.2 B), which none of the other candidates predicts as cleanly.

**GRADE: the falsification of M1's regular limb is DECIDED. The replacement mechanism is UNDECIDABLE**
between (i), (ii), (iii) and trash-point multiplicity. galadriel's censoring blocks the call; the note below
names what would decide it.

### 2.5 The BOSS limb — a quiet, opposite-direction finding

Not falsifiable here (all undershoots) but the fit is one-sided and worth the conductor's eye:

| wave | boss E / sup, `boss_add=ON` (record) | boss E / sup, `boss_add=OFF` | camera |
|--:|--:|--:|--:|
| 152 | 1.75 / 2 | **1.00 / 1** | **1** |
| 157 | 2.00 / 2 | **1.00 / 1** | **1** |
| 160 | 5.00 / 5 | **4.00 / 4** | **4** (minimap, arena-level; census closed 8/8) |

Under § 10.5 a *non-exempt* BOSS pool with `spawnMin=spawnMax=1` receives the `+1` and becomes
`floor(2×1.2)=2 , 2` — **two bosses per boss point**. The camera reads one, three times, including once on
the non-censored instrument. `boss_add=OFF` matches 3/3 exactly. Band effect: **271.50 → 248.83
(−22.67, −8.35 %)** — a correction pointing the *opposite* way to everything else in this note.
**GRADE: STRONG CIRCUMSTANTIAL, NOT DECIDED** (three undershoots cannot falsify; the w160 leg is the only
near-arena-level one and its minimap icons "converge and merge" by galadriel's own caveat).

### 2.6 p05 handling — explicit, per the commission

- DB cadence: start **t + 4.0 s**, interval **3.0 s**. Windows → in-window emission events:
  w151 **1** (t+4 only; t+7 > 5.97) · w152 **3** (4, 7, 10) · w153 **2** (4, 7) · w157 **2** · w158 **2**.
- **Engagement-lag assumption, stated:** the readout instrument renders only on engagement. The one
  measured lag in this corpus is **4.47 s** (w151: p05 fires t+4.0, first post-gap render +8.47, identity
  confirmed as `livingplant_t3`). galadriel's stated spawn→engagement band is 3.5–6.1 s. Therefore a
  t+4 emission renders in **[+7.5, +10.1] s** and a t+7 emission in **[+10.5, +13.1] s**.
- **Consequence:** w151 sees **zero** p05 renders (window 5.97) — MEASURED, two instruments.
  152/153/157/158 see **at most the first emission**, and only marginally (windows 10.23/8.60/8.63/8.33
  against a [+7.5,+10.1] render band). The second emission is **outside every window**.
- **This is why § 2.4's mechanism (ii) is scored as a hypothesis about *spawning*, not about *rendering*:**
  a second p05 emission cannot itself appear in these windows, so if it explains w153 it does so by making
  the *first* emission larger, not by adding a visible second drip. That distinction is not resolvable here
  and is graded **UNDECIDABLE**.

### 2.7 One instrument measured and rejected (recorded so it is not re-tried)

Correlation of model expectation with observed plain count across the five waves:
`M1 E = [16.00, 7.00, 17.50, 12.38, 27.00]` vs `obs = [9, 17, 23, 15, 24]` → **r = +0.515**;
all-pools E → **r = +0.370**. Both weak, neither discriminating, and both dominated by censoring (her § 6:
readouts see 0–5 bodies while the minimap carries 10–14). **NON-PROBATIVE. Do not re-run it.**

---

## 3. Q3 — THE CONJURE QUESTION, ANSWERED PRECISELY

**Is any body un-rostered? YES — exactly one, corpus-wide: `Ugdenbog Crabling`, w152 +3.40 s.**
(Plus one cross-wave candidate, `Carnivorous Plant` w152 +0.40 s, graded UNDECIDABLE / lean carryover.)

So the count-pass re-open leg found **contact on BOTH channels — but they do not agree with each other**:

| channel | contact | does it support the `+1`-on-empty branch? |
|:--|:--|:--|
| **IDENTITY** | 1 un-rostered common, at a point whose selected alternative (`swampcrab_hero`) is non-exempt with `roster_n = 0`, in that pool's own creature family, bracketed by that pool's own champions | **YES — this is exactly the CONJURE_FROM_TEMPLATE signature.** But see the Aleksander's-Shard control: un-rostered ≠ conjured, and the rival mechanism is measured in the same footage. |
| **COUNT** | +10 / +5 / +1 over support on w152 / w153 / w157 | **NO — wrong magnitude and wrong shape.** CONJURE predicts +2/+3/+2/+2/+2. It over-predicts where nothing is seen (151, 158) and under-predicts by 7× where the overshoot is largest (152). Adding it still leaves w152 at 17 > 10 and w153 at 23 > 20. |

**Disposition on F-9's no-op — my recommendation to the conductor:**

> **F-9 NO-OP: dispositionally UNCHANGED, but its evidentiary status changes from *undischarged* to
> *contested*. Re-grade the L-40(b) status line from "NOT DISCRIMINATED ON CAMERA — the discriminating
> waves are unread" to "DISCRIMINATING WAVES READ; the count leg REJECTS the CONJURE magnitude; the
> identity leg produces ONE un-rostered body consistent with CONJURE at a predicted point; the two legs
> disagree and the un-rostered class is known to be non-unique in mechanism (w160 summon precedent).
> No-op stands on the L-35(e) pre-registration, now with a named contradiction on the record."**

Rationale, and I want to be plain about it: **the honest reading is that the count-pass found something
LARGER than F-9, not F-9.** The `+1`-on-empty question is a ±21-body question over the band; what the
camera actually surfaced is a **+18 to +45-body question over three waves**, of unknown mechanism.
Adopting the `+1` now because a crabling appeared would be fitting one free parameter to a residual that is
demonstrably not that parameter's shape — the exact move charter § 4.2 forbids, and the exact move F-10
already caught the pin-era model making. **F-9's `+1` stays un-adopted. F-13 is a new finding, not a
resolution of F-9.**

**What is genuinely NEW and belongs on the record regardless of F-9:** the model of record's regular limb is
falsified at its own support on three of five discriminating waves, and the residual has structure
(a clean HP break, above-gap counts landing exactly on the model's support twice).

---

## 4. Q4 — BLAST RADIUS

### 4.1 Band 151–170 under every candidate

| model | regulars | champions | × record |
|:--|--:|--:|--:|
| **M1 — model of record** (trash=SEL, champ=SEL, boss=SEL, no-op, p06 OFF) | **271.50** | **63.00** | 1.000 |
| M1 + F-9 `+1` (the un-adopted parameter) | 292.50 | 63.00 | 1.077 |
| M1 with `boss_add=OFF` (§ 2.5) | **248.83** | 63.00 | **0.917** |
| **MEASURED FLOOR** — M1 with the three falsified waves raised to their measured lower bounds | **289.62** | 63.00 | **1.067** |
| lattice survivor: trash=ALL, champ=SEL, boss=SEL, CONJ, boss_add=OFF | 632.00 | 63.00 | 2.328 |
| lattice survivor: trash=ALL, champ=SEL, boss=SEL, CONJ, boss_add=ON | 654.67 | 63.00 | 2.411 |
| lattice survivor: trash=ALL, champ=ALL, boss=SEL, CONJ | 708.67 | 225.00 / 75.00 | 2.610 |
| lattice survivor: trash=ALL, champ=ALL, boss=ALL, CONJ | 772.00 | 225.00 / 75.00 | 2.843 |

Measured-floor derivation (E-form; the only sampling-defence-free figures are the support deficits):
```
w152  PLAIN E = 7.00 (deterministic)  measured >= 17  ->  E-delta >= +10.00   support deficit +10
w153  PLAIN E = 17.50                 measured >= 23  ->  E-delta >=  +5.50   support deficit  +5
w157  PLAIN E = 12.38                 measured >= 15  ->  E-delta >=  +2.62   support deficit  +1
                                                          -------------------------------------
                            over 3 of 20 band waves:            +18.12                     +16
   band floor = 271.50 + 18.12 = 289.62  (1.067x)   [support form: 287.50, 1.059x]
```

**GRADE on the band: the best-fit model is NOT DETERMINED, so the band is a RANGE, not a number.**
`248.83` (boss_add OFF, no second population) … `271.50` (record) … `289.62` (measured floor) …
`632–772` (lattice survivors). The measured floor is the only figure that is both **above the record** and
**free of any mechanism assumption** — it is arithmetic on her lower bounds. **I recommend the conductor
carry 289.62 as a FLOOR and refuse a point estimate.**

### 4.2 Per-consumer

| consumer | verdict | why |
|:--|:--|:--|
| **T-3** (`counts run the p06-OFF model of record 271.50 / 63.00`) | **MOVES — regular limb only. Champion limb 63.00 UNTOUCHED.** | The 271.50 is falsified below at ≥ 289.62; the 63.00 is unfalsified on all five waves and hit **exactly** on w157. Recommend the row be re-annotated to carry the regular figure as a **floor with a named finding**, exactly as F-10 handled the superseded pins — *not* re-pinned inside this run. |
| **AC-10.4** | **MOVES — second annotation.** | Its regular limbs were already re-graded SUPERSEDED-PROVENANCE at F-10 against a *documentary* argument. F-13 adds the first **empirical** falsification of the *replacement*: 271.50's per-wave components are falsified at support on w152/w153/w157. The champion pin's "63.0 EXACT" claim is now **empirically corroborated** for the first time (w157, 6/6). |
| **F-12 / locomotion lap N inputs** (sim clear time r = +0.737 vs N) | **MOVES, and this is the one that hurts.** | The locomotion amendment will be calibrated against s1/s2 clear times using per-wave N from the count model. On w152 that N is **7 against a measured ≥ 17** — a 2.4× error on a body-count-coupled timing model. Calibrating locomotion on a falsified N would bake the count error into `v_mob`/radius. **Recommend: the locomotion lap runs on waves where N is UNFALSIFIED (151, 158 and the 15 unmeasured band waves), and 152/153/157 are excluded from calibration and reported as findings.** Alternatively the lap waits for the mechanism call — but that is a real schedule cost and it is the conductor's ruling, not mine. |
| **baton `count_model` provenance** | **MOVES — additive, no schema change.** | The provenance block already carries F-10 + the superseded pins by name. It should now also carry **F-13**, the per-wave falsification table (§ 2.2), the measured floor 289.62, and the un-adopted-parameter list extended from `empty_roster_plus_one` to include `trash_pool_multiplicity`, `p05_replenishment`, `boss_spawn_additive`, `summoned_bodies`. **All four NAMED, none fitted.** |
| **MO-5** (cycle floor ~7.0 s) | **DOES NOT MOVE.** | MO-5 is a one-sided floor for a *trivially-dying* wave; it emerges from spawn + traversal geometry (AC-10.7), not from N. A larger N can only push clear time up, never below the floor. Its already-flagged provisional-on-geometry status (F-12a, the uncited 30.0 m radius) is untouched by this note. |
| **AC-10.3** (w160: one nemesis on each of p01/p02/p03, zero trash) | **NEEDS-DATA.** | "Zero trash" is contradicted by the board-closure's **seven plain bodies** at w160 — but those are graded SUMMON, which AC-10.3 does not model and does not claim to. The AC is defensible as written *about spawns*; it should say so. Recommend a one-line scoping annotation, not a re-pin. |
| **§ 10.6 p05 arrival model** | **NEEDS-DATA.** | The replenishment fork (§ 2.4 (ii)) is § 10.6's own declared-undetermined flag and it is now load-bearing on w153. It was safe to declare when nothing depended on it; it is no longer. |
| **T-2** (1.9 % count-model residual) | **DOES NOT MOVE — but is now visibly the wrong size of question.** | T-2 bounds intra-order/rounding/clamp at 5.5 on 292. The measured miss on w152 alone is +10 on a **deterministic** 7. Recommend the row carry a pointer to F-13 so nobody reads 1.9 % as the count model's total error bar. |

---

## 5. What would decide the open calls — named, cheap, and in priority order

1. **The mechanism split (i) vs (ii) vs (iii) — a per-body IDENTITY pass on WAVE 153.** It is the only
   falsifying wave with **no boss and no skull on any instrument**, so the summon branch (i) must run
   through trash/hero summoners there or not at all. Ask: *what are the 5 sub-50 k bodies
   (16,368 ×1 and 37,840 ×4)?* If they plate as `livingplant_t3` members (Carnivorous Plant / Ugdenbog
   Golem) → **p05 (ii)**. If they plate as `giant_t3` members (Asterkarn / Groble) → **trash multiplicity**.
   If they plate un-rostered → **(i) or (iii)**. **Deterministic three-way separation on five bodies.**
2. **The `Ugdenbog Crabling` binding.** Bind that plate to a max-HP fingerprint and a spawn bearing.
   If it binds to the low cluster (42,798 ×4 / 43,548 ×3) the un-rostered population on w152 is **seven
   bodies from one point**, which kills CONJURE (predicts 1) and points hard at hero-entourage or summon.
3. **The w152 +0.40 s carryover question.** Whether GD's Crucible advances the badge on wave-clear or on a
   residual condition. One citation (`survivalevent.lua`) closes it and also closes whether 302,934
   (arr +0.00, last +0.77) is a w151 body — which is worth exactly 1 of w152's 17 plains and would move the
   above-gap count off its exact landing on 7.
4. **`boss_add` (§ 2.5).** The `proxypool`/`adj03` template fine-print on whether `spawnMinAdj` applies to
   `ignoreGameBalance = False` **boss** pools. Rides the legolas r3 template rider that is already open for
   F-9. Worth −22.67 on the band, opposite direction to everything else here.

---

## 6. Verdicts, one line each

| Q | verdict |
|:--|:--|
| **Q1 identity** | **31 / 33 plates ROSTERED (30 exact + 1 one-char fuzzy). Exactly ONE body is un-rostered corpus-wide: `Ugdenbog Crabling`, w152 +3.40 s** — absent from 1,492 names and 1,617 record paths, sitting at a point whose selected pool (`swampcrab_hero`) is non-exempt with an empty regular roster. One further cross-wave candidate (`Carnivorous Plant`, w152 +0.40 s) is **UNDECIDABLE**, lean carryover. Zero ROSTER-OTHER-POINT. 91 of ~113 bodies are **UNIDENTIFIED, not un-rostered** — the join has no power over them. |
| **Q2 discrimination** | **M1 (model of record) FALSIFIED at its own support on the PLAIN limb: w152 17 > 7 (deterministic), w153 23 > 18, w157 15 > 14.** STAR limb **unfalsified everywhere and EXACT at w157 (6/6)** — AC-10.4's 63.00 survives. SKULL limb unfalsified. Of 64 lattice cells, 12 survive, all requiring `trash=ALL` **and** `CONJURE` — but that is a 2.3–2.8× band correction I do **not** endorse, because the HP decomposition shows the above-gap plains land **exactly** on M1's support on both falsifying waves (7 and 18). **The trash limb is INCOMPLETE, not WRONG.** Replacement mechanism **UNDECIDABLE** among four named candidates. |
| **Q3 conjure** | **Contact made on BOTH channels, and they disagree.** IDENTITY gives one un-rostered body with the right signature; COUNT rejects CONJURE's magnitude and shape (+2/+3/+2/+2/+2 predicted vs +0/+10/+5/+1/+0 measured; adding it still leaves w152 17 > 10). The un-rostered class is **known non-unique in mechanism** — `Aleksander's Shard` (w160, SUMMON) is equally un-rostered. **F-9's no-op disposition stands UNCHANGED and un-adopted; its status line changes from *undischarged* to *contested*. F-13 is a new and larger finding, not a resolution of F-9.** |
| **Q4 blast radius** | Band is a **RANGE, not a number**: 248.83 (boss_add OFF) … **271.50 (record)** … **289.62 (measured floor, assumption-free)** … 632–772 (lattice survivors). **MOVES:** T-3 (regular limb only), AC-10.4 (second annotation; champion pin now empirically corroborated), **F-12 locomotion N inputs (the painful one — exclude 152/153/157 from calibration)**, baton `count_model` provenance (four new named-never-fitted parameters). **DOES NOT MOVE:** MO-5, T-2 (but annotate). **NEEDS-DATA:** AC-10.3's "zero trash" scoping, § 10.6's p05 replenishment fork. |

---

## 7. Mirror voice

I wrote the count model, so let me say the uncomfortable thing first. On wave one-fifty-two my model does
not have a distribution — it has a **number**. Seven. Two alternatives, both deterministic, both seven; there
is no roll to lose. The camera counted seventeen, and ten of those seventeen sit in a band of health values
two and a half times below everything else on the board, as though a second and smaller kind of thing had
walked in through a door the model does not know about. On wave one-fifty-three the same door opens and
five walk through it, and the ones **above** the gap number eighteen, which is my model's ceiling, hit
precisely, on the nose, with nothing to spare.

That is the shape of a spec that is right about what it describes and silent about something standing next
to it. It would have been easy — and it was very nearly the arithmetic's own suggestion — to conclude that
every pool at every point spawns at once and to multiply the band by two and eight tenths. Twelve
configurations out of sixty-four say exactly that, and all twelve are wrong for the same reason the pin-era
model was wrong: they are the only shape left when you refuse to admit the model might be **incomplete**
rather than **mis-parameterised**.

And there is one crab. One small crab with a name that exists nowhere in one thousand four hundred and
ninety-two names, standing between two heroes from the pool it should have been drawn from and was not.
It is exactly the body F-9 said it would be. It is also exactly the body that Aleksander's Shard was at
wave one-sixty, and that one was summoned. **One un-rostered body is not a mechanism. It is a door, and we
have now seen two different things come through it.**

---

**Filed:** named-gandalf `DRIFT-CRITIC`, 2026-08-08, KC2-SIM Phase D, conductor commission L-44.
Uncommitted per instruction. Every figure recomputed from `pe6_crucible_wave_pools_v2.csv` on an
instrument calibrated against F-10's published cells; no figure quoted without reproduction.

---

## 8. L-50 ADDENDUM — the § 5 deciders fired (conductor, corrigenda-forward; this note's body above is unedited record)

The fifth extraction (`galadriel/notes/2026-08-08-kc2-fifth-extraction-w153-identity.md`) executed
decider (1) and closed decider (2). Dispositions against this note's own claims:

- **Decider (1) — EXECUTED.** The five sub-50k bodies resolve: **16,368 ×1 = NOT A HOSTILE BODY**
  (green bar 92/93 frames, zero nameplates, fraction-excluded on all 22 plate-valid frames) — struck
  from the w153 monster census. One 37,840 = **`Skeletal Archer` L105 Undead common**
  (FRACTION-UNIQUE 5/5, Δ = 1.1 px, runner-up 17× out); three 37,840 UNIDENTIFIED
  (degenerate / no-plate — the ×4 independently reproduced by damage-state banding).
- **The separation landed in the branch this note called "(i) or (iii)":** `Skeletal Archer` is
  **absent from every rostered pool on waves 151–158** (all pool kinds; conductor grep on the pinned
  CSV at the L-50 fold). ×4 bodies > CONJURE's +2 → **(iii) insufficient; (i) SUMMON indicated.**
  § 5's plate-class map under-enumerated w153's trash pools (four, not two: + `wendigo_t3` p01,
  `skeletonrevenant_t3` p03); neither silent case occurred, and **`skeletonrevenant_t3` (Flame /
  Frost / Storm / Death Revenant class) is the named summoner-candidate** — the citation question
  is concrete: do those records carry a summon skill referencing `skeleton_a02_archer.dbr`?
- **§ 6 Q1's "exactly ONE un-rostered body corpus-wide" is now THREE:** Crabling (w152) ·
  Aleksander's Shard (w160, SUMMON) · **Skeletal Archer (w153, ×4)**. The mirror's door has been
  used a third time, and this time the thing that came through has a name and a level.
- **Decider (2) — CLOSED-UNBINDABLE.** The Crabling hover's plate is saturated FULL on all 4
  frames; ≥ 5 parsed bodies ≥ 0.988. The low-cluster question is neither confirmed nor excluded.
- **The falsification triple re-grades:** w152 **STANDS** (margin 10; the 20,005 green entity was
  never in its 17) · w153 **STANDS** (16,368 struck → 22-or-23 > 18; count-pass and
  fourth-extraction census accountings differ by one and both exceed support) · w157 **SUSPENDED at
  margin-1** (bar_hue never ran there; one green contaminant collapses 15 > 14 to 14 = 14). M1's
  PLAIN falsification **survives on w152 + w153 alone**. The **289.62 floor → CONTINGENT** (its
  18.12 E-form consumed w153/w157 excesses now under census correction); endpoints
  248.83 / 271.50 untouched. Champion 63.00 unmoved; the w157 6/6 positive control gains a
  glyph-colour rank-audit caveat (fifth § 9.2/9.3: `~ Affix` ≠ rank; stars bind HERO only).
- **Green-class identification (candidate, not ruled):** 20,005 ≡ MO-4's pinned player max health
  EXACT — the green class contains the player's own readout; 16,368's profile (static box, never
  damaged, survives badge flips) + the save regime's **+4 purchased defenses** name Crucible
  defense structures as the candidate class. Mechanism-adjudication piece QUEUED at the bar_hue
  fold.

*Addendum by the conductor at the L-50 fold, 2026-08-08. The body of this note above § 8 is
unedited record; where § 5/§ 6 claims are superseded, this addendum governs.*

## 9. L-52 ADDENDUM — the commissioned bar_hue cohort pass returned (conductor, corrigenda-forward; §§ 0–8 above are unedited record)

The bar_hue cohort correction (`galadriel/notes/2026-08-08-kc2-barhue-cohort-correction.md`;
8,781 readouts re-classified, 121 tiles eye-read, five cohorts) executed the § 8 queued items.
Dispositions against this note's own claims:

- **w157 — RE-CONFIRMED STANDS, 15 > 14.** The margin-1 suspension lifts: 11/11 plain-cohort
  bodies return zero green votes (9 with mean g exactly 0.0), 11/11 eye-read RED. The one
  collapse scenario (a green contaminant inside the 15) is excluded by direct measurement, not
  by argument. w157 re-enters the falsification triple.
- **w153 — single accounting, 22 > 18.** The § 8 "22-or-23" resolves to **22** (−1 = the struck
  16,368; count-pass and census accountings converge). Margin +4.
- **w151 9 · w158 24 — EXACT, no green contamination.** The strike does not spread: all 50
  remaining flagged-window readouts eye-read RED.
- **The green class is ONE entity — the player's own readout.** 16,368 ≡ 20,005: identical
  modal box [882,399]–[1039,413], x-centre 960.5 = frame centre, zero co-occurrence across
  1,073 frames, value handover 713.347 → 713.380 coinciding with a buff expiry — the only
  STATIC entity in all five cohorts. The § 8 "Crucible defense structures" candidate RETIRES —
  defense structures are NAMED-ABSENT from all five cohorts (caveat: engagement censoring —
  readouts render only for engaged bodies, so this is absence-from-instrument, not
  absence-from-arena). **The exclusion rule matures: key on the BOX, not the value.**
- **The champion 6/6 corroboration is STRUCK — derivation-invalid.** All six w157 star bodies
  (457,975 ×3 · 447,590 ×2 · 588,905 ×1) are STAR-DERIVED — none was ever glyph-read. The
  30 Hz plate re-scan (13 spans / 168 plate-valid frames) binds zero plates to star bodies;
  the two bindings it does produce are both champion-on-PLAIN-bar — **Diremane Brute →
  238,068** (FRACTION-TRACK, RMS 0.78 px, r² 0.9996 — fourth independent calibration
  agreement) and **Aetherial Stormdrinker → 304,994** (PROBABLE). Star-pairs bind HERO (fifth
  § 9.3, reproduced in-wave). Consequences, graded:
  - Champion limb **63.00 → UNCORROBORATED** — NOT falsified. The star instrument is one-sided
    and no champion-census instrument exists; in-cohort hover names put ≥ 2 champions in w157.
  - § 2.1's mapping gains its named contingency: PLAIN furniture carries commons AND
    champion-flagged bodies, so PLAIN falsifications are in-principle mixtures. Two branches:
    **slot-conserved** (champions occupy roster slots; PLAIN excess still counts against
    support) vs **additive-champion** (champions ride above roster; excess partially
    explained). w151 (obs 9, under E) and w158 (obs 24, under support 36) land where
    regular-only accounting puts them — evidence for slot-conserved. **Branch ruling routed to
    the mechanism-adjudication piece**, which now holds the corrected cohorts + the green
    census + the save regime; it folds with the summon-citation return.
- **The floor re-derives.** E-form: 271.50 + 10.00 (w152) + 4.50 (w153: 22 − 17.50) + 2.62
  (w157) = **288.62** (1.063×). Support form: 271.50 + 10 + 4 + 1 = **286.50** (1.055×). Both
  above the 271.50 record — the § 8 CONTINGENT grade clears; the § 4.1 verdict shape is
  unchanged (floor-with-named-finding carried; point estimate refused). Superseded figures,
  named: 289.62 → 288.62 · 287.50 → 286.50 · +18.12/+16 → +17.12/+15.
- **Per-consumer (§ 4.2 updates):** T-3 row — L-52 annotation landed. AC-10.4 — fourth
  annotation; "63.0 corroborated" WITHDRAWN. F-12 calibration — exclusion set **{w152, w153,
  w157} UNCHANGED** (w157 re-confirmed, not de-falsified; no re-entry fires). Baton
  `count_model` provenance — carries F-13 + the corrected floor + the UNCORROBORATED champion
  grade.
- **Instrument findings (registered):** (i) a new false-plate class — in-world readouts
  drifting into plate rows 17–34 pass `is_plate`; the contrast gate caught 1 of 2; **plates
  must be eye-read**; (ii) bar_hue purity is a scene-brightness statistic erring BOTH
  directions (0.54 measured on a red body; 0.75–0.87 on the green entity) — classification
  stands on the green-vote census + eye-read, never on purity alone.

*Addendum by the conductor at the L-52 fold, 2026-08-08. Where § 5/§ 6/§ 8 claims are
superseded, this addendum governs.*

## 10. L-53 MARKER — the summon-citation returned (conductor, corrigenda-forward; §§ 0–9 above are unedited record)

The § 9 line "it folds with the summon-citation return" discharges here. The legolas
summon+maploader micro-probe (`legolas/notes/2026-08-08-kc2-summon-maploader-microprobe.md`)
returned T1 **CLOSED-DB-CITED**:

- **w153's mechanism limb is SOLVED — SUMMON-CITED.** Chain: w153 p03 `skeletonrevenant_t3`
  slot 4 rosters **Death Revenant** (`skeleton_d01.dbr`, Champion, `limit4 = 2` per point);
  its `skillName7` = Skill_MonsterGenerator; `spawnObjects` = `skeleton_a02_summon.dbr` =
  **"Skeletal Archer"** (Common; `_summon` vs `_archer` differ 1 field/938, eHP-neutral).
  **petLimit = 4** (sm_mod overlay 6 → 4; Crate template verbatim: "max number of pets alive
  at any given time"; burst 2, period 6.0 s, TTL 30 s → cap reached t ≈ 6 s and held).
  **Observed ×4 = the declared cap EXACTLY.** Ceiling 8 under two limit-2 Revenants. Pet
  LEVEL is NAMED-ABSENT in the DB; two corroborations put archers AT wave level (L104–105
  band; the w160 archer L109 eHP 41,237 EXACT, L-33) — which is why the level-inheritance
  discriminator had no power on 151–158: identity, not level, closed it.
- **w152's limb stays OPEN.** The probe's exhaustive BFS (7/429 monsters reach a Skeletal
  Archer) was ARCHER-specific; non-archer generators are un-enumerated, and w152's
  archer-reaching summoners sit in p06 hero pools — RULED OFF (L-37(b)). Candidates for the
  +10: non-archer generators (a cheap legolas extension if the adjudication wants it) · p05
  replenishment · trash multiplicity.
- **w157 candidate named:** `skeletalgolem_b01` rostered at p04 carries a golem generator
  (petLimit 4; probe § 2.3) — plausibly its +1/+2.62.
- **Structural point (probe § 2.4):** `skeleton_a02_summon` is rostered in NO pool. Summons
  are a **second body source orthogonal to rosters**, gated by per-summoner `petLimit`, not
  per-pool `spawnMin/Max` — one Death Revenant licenses up to 12 un-rostered bodies (archer +
  warrior + knight generators, petLimit 4 each). § 2.1's count-model taxonomy gains its
  citation.
- **Disposition this run:** summoned bodies stay **OUT-OF-MODEL**, DECLARED in baton
  `count_model` provenance — adding a summon model mid-run is re-pinning (standing safety #1);
  modelling is a next-lap pre-registration item.
- **The § 9 champion-composition branch ruling** (slot-conserved vs additive-champion) and
  mechanism (ii) p05-replenishment both ride the **mechanism adjudication, now COURSE work,
  firing AFTER the L-54 locomotion-lap fold** (the lap's p05-cadence localisation bears on
  (ii)).

*Marker by the conductor at the L-53 fold, 2026-08-08. The adjudication itself is deferred,
not this citation: where § 5 decider (1)'s "summon-or-conjure" branch read SUMMON *indicated*,
it is now SUMMON **CITED**.*
