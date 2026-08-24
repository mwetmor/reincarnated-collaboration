# DRIFT-CRITIC verdict — KC2-MC · **B-4** (SPECIALS FIRING, facet (c))

**Agent:** gandalf (`DRIFT-CRITIC`, named sub-agent) · **Date:** 2026-08-24 · **Run:** KC2 MODEL-COMPLETION, ledger `L-55`, ruling `R-L55-1`
**Judged:** `simulation/kc2/pet_specials.py` · math note `kc2-mc-b4-specials-2026-08-24.md` + ADDENDA 1–6
· sibling `E-s09-cp150-b4-20260824_232229` `08255194…`
**Against:** the `R-L51-2` launch brief (the B-2app-era carries + the B-3 Gate-2 WARN cluster + `L-50`'s `magnitude_class` instruction), `L-50`'s carry-shape discipline **on its first outing**, `L-53`/`L-54`'s referent attestations, and the run's **intent sentence** (Matt: *"all aspects present"*).
**Parallel:** jack-ryan Gate 2 on the bytes. This verdict judges design-fit only — no hash re-verification.
⚠ **The carries this build answers are mine, and so is the SPIKE-LANE elevation ruled at `R-L55-2` before this verdict existed.** § 7 is pointed at both. It finds three, and one of them is in the brief that commissioned this verdict.

---

## 0 · TOP-LINE

**PASS — with design findings. Twelve, three baton-blocking, four of them the conductor's.**

B-4 is the most **self-correcting** build in the run and it is not close. Six standalone addenda, every one convicting a defect found by **the instrument the previous addendum built**, zero pass-fixes, two mutation proofs using the *actual historical defect* as payload, an untracked scratch probe disclosed rather than hidden, and a deletion declaration whose stated mechanism **is the absence** and is checkable in git. The three-arm design answered `L-50`'s anti-laundering instruction *structurally* — each sign on its own arm, so no cancellation claim is ever needed — and that structure then **bought a decomposition a single-arm run could not have produced**: `D2_FIRING_ONLY` is byte-identical to `ABSENT` on 5/5 salts, so the arm of record's entire measured effect belongs to the silent 51 and the 14-slot repair moves *nothing*.

And it found, before the fold was designed and by looking rather than reasoning, that **the sim's busiest pet body could not attack.** `livingplant_a01_summon`, 61 spawns, `slots == ()`. Every sealed cell in this run — b1, b2, b1r, b2app, b3 — and every PM1–PM4 grade before it, ran on that board.

My dissents are, as in B-3, **not with the modelling.** They are with (i) **what the published numbers can be read to mean** — and the B-3 `F-1` class is back, this time *inside a registered predicate*; (ii) **what the baton must carry so the Godot session does not build a model the sim refuses**; and (iii) **three sentences the conductor wrote that pre-commit answers to questions still open.**

---

## 1 · Q1 — THE WRONG-FIFTY-ONE AND THE INTENT SENTENCE

### (a) First, a correction to the question I was asked

**"118/152 spawns could not attack ⇒ the fight was missing most of its teeth"** is an over-read, and it is mine. The record cell rolls **312 roster placements** (60 of 169 records) **plus** 152 D-2-body spawns. The roster bodies were fully armed throughout. The inert set is **118 of ~464 bodies ≈ 25 %** — a quarter of the board, concentrated in the summoned-pet subpopulation. That is a large and material finding; it is not "most of its teeth," and the difference matters because the residual argument below turns on the magnitude.

**And "108 bodies wake" is the conflation `ADDENDUM 1` was written to repair.** 108 is **spawns**; **12** bodies wake, of 14 that gain a slot, of 15 that cannot swing. `D-B4-2` caught exactly that collapse; the brief re-committed it in the question. See § 7.

### (b) What the arm of record actually did — and the honest instrument

Read off the artifact's own per-salt cells:

| salt | ABSENT term / waves / landings | `D2_ALL` term / waves / landings |
|---|---|---|
| 0 | 155 / 5 / 260 | **151 / 1 / 22** |
| 1 | 156 / 6 / 330 | 156 / 6 / **359** |
| 2 | 152 / 2 / 50 | 152 / 2 / **78** |
| 3 | 151 / 1 / 20 | 151 / 1 / **33** |
| 4 | 151 / 1 / 23 | 151 / 1 / 18 |
| **Σ** | **15 waves / 683 landings / 2 control** | **11 waves / 510 landings / 1 control** |

**On the four salts whose ladder length is unchanged, landed attacks rise 423 → 488 (+15.4 %) and the terminal wave does not move on any of them.** The whole of the ensemble's `683 → 510` "reduction" is salt 0's ladder collapsing from 5 waves to 1. Waking a quarter of the board's bodies **increased incoming attack volume by ~15 % on a matched denominator** — the registered ↑-threat sign, confirmed, on the only instrument that can confirm it.

### (c) The residual's sign — three readings, and only one survives

| reading | verdict |
|---|---|
| *"the residual widened: mean terminal 153.0 → 152.2"* | **UNSAFE.** Driven entirely by one salt; the fold permutes the shared RNG stream **by construction** (`S-B4-4`), and salt 4's landings fell 23 → 18 on an *identical* ladder, which is pure stream noise. A 4-wave move on 1 of 5 salts is not separable from a re-roll at this ensemble size |
| *"the fold is inert on survival"* | **UNSAFE in the other direction** — it discards a measured +15 % attack volume |
| ⚑ *"attack VOLUME rose ~15 % on matched ladders; TERMINAL WAVE moved on 1 of 5 salts and that move is confounded with a stream permutation"* | **the honest statement**, and it is computable from the artifact and published nowhere |

**But the design consequence survives the caution, and it is the sharpest constraint the run has on the residual.** Set (c) beside `L-50`'s salt-1 finding from B-3:

> **B-3, salt 1:** landed attacks `330 → 93` (**−72 %**) — terminal wave `156 → 156`.
> **B-4, salts 1–4:** landed attacks `423 → 488` (**+15 %**) — terminal waves **unchanged, 4 for 4**.

**Two independent perturbations, opposite directions, one conclusion: the sim pilot's terminal wave is insensitive to attrition volume.** Removing three-quarters of incoming attacks buys nothing; adding a sixth costs nothing. That is not a weak result — it is a *two-sided* falsification of the attrition hypothesis, and it composes with `L-53`(c) (the deficit is not channel-uptime-shaped) and `L-54` (it is not energy-dry-out-shaped) into a genuine narrowing: **the sim pilot dies to spikes, and the 151–156-vs-160 residual lives in spike survival, not in sustain.** This evidence is currently **unassembled across two builds** and appears in neither fold. It is `F-2`.

### (d) *"Record-cell exposure NIL"* — over-read, and I can name where

`D2_FIRING_ONLY` ≡ `ABSENT` byte-identical on 5/5 with **0** pet special selections is *correct, measured, and well-evidenced* (`ADDENDUM 6` § 1). The mechanism is also measured: the one firing-arm slot on a rolled body is `wraith_b01_summon special3`, reach 6.0 m, 4 spawns, the body's **only** slot — so `choose_slot` offers nothing whenever it sits outside 6 m. **The reach was binding, not the gate**, exactly as § 0.3 registered before any of it ran. Excellent work.

**NIL is conditioned on three things, and the artifact names one.** `measurement_condition` reads *"a zero here is a ROLL, not a rule (L-50 trap T-c)."* The roll is the weakest of the three:

1. **the ROLL** — 4 spawns of one body across 5 salts (named);
2. **the PILOT** — the sim's continuous-spin kiter never closes to 6 m. `L-53` attests the referent ran **greedy-on-cooldown with a pack-proximity hold** — a policy whose *defining behaviour is closing to packs*. The pilot that produces this NIL is the pilot the run has already attested is wrong (unnamed);
3. **the PURSUIT MODEL** — **B-5** (alert-before-pursue) and **B-6** (state-machine expansion) both change monster approach, i.e. the *distance distribution* that made reach binding (unnamed).

⚑ **T-c was adopted at `L-50` as MEASUREMENT-CONDITIONED-ON-**PILOT** and lands in B-4 as conditioned-on-**ROLL**.** The condition axis narrowed in transit, at the one address where the pilot-condition is load-bearing. **NIL on the record arm is not NIL on PM5's re-graded arm**, and the ledger sentence *"the reach was the binding constraint, not the gate"* travels without any of the three. `F-4`.

---

## 2 · Q2 — `ManaBurnDrain` AS THE SPIKE LANE: THE CHAIN DOES NOT HOLD, AND THE COMMISSION IS STILL RIGHT

### (a) Grade the plausibility chain honestly

| link | status |
|---|---|
| a masked 2 s Disruption sits on the health-damage lane | **TRUE and decoded-adjacent.** `min` is a duration on control rows (`Stun min=0.6999…`, B-2 § 2); Grava'Thul's Disruption row carries `min = 2.0` under `kind='direct'`. The units error is real |
| a second armed row exists that no carry named (`ManaBurnDrain`, `min = 10.0`) | **TRUE, and it is the build's best find.** Found because the carry was briefed as a *mechanism*, not a name |
| both are gated and loaded (`special3` delay 15 s / chance 100 / reach 21 m; `special4` delay 6 s / chance 100 / reach 2.4 m) | **TRUE** |
| ⇒ **these are the residual's spike lane** | ⚑ **FALSE ON THIS CELL, and not marginally.** Grava'Thul has **0 placements** over the 5-salt ensemble. A body that is never instantiated contributes **exactly zero** to a residual measured on that ensemble. Not "small." Zero, by construction |

**So the reading is ahead of D-10's decode — and it is ahead of something more basic than the decode.** Even if D-10 returns *"`min` is a magnitude, the consumer is the health lane, it hits for 10"*, the row still cannot explain a residual on a cell where its body never spawns. The elevation's stated rationale (`R-L55-2`: *"the armed health-lane rows are the run's best spike-lane candidates and PM5's residual attribution needs them decoded, not parked"*) pre-commits **three** things D-10 must be free to falsify: that the rows are *health-lane* (that is literally MD-B4-1's question — if `min` is a duration they are not), that they are *spike candidates* (requires firing), and that *residual attribution needs them* (it cannot use them).

**D-10 is still correctly commissioned. Its reason must be replaced, and the replacement is stronger because it holds under either arm of the fork:**

- **STABILITY.** `mitigate()` raises `KeyError` on an unmapped family. Two gated slots on a rollable nemesis are **one roll from a halt** — carry (b)'s finding, and the run's most load-bearing operational fact.
- **UNITS-CORRECTNESS.** A duration sitting on the damage lane mis-prices *every future cell that rolls the body* and would corrupt any Layer-1 baton row derived from it.

Neither requires the row to fire, to be on the health lane, or to touch the residual. `C-2`.

### (b) What the PM5 prereg row must pre-commit to, so the answer cannot be retro-fitted

The retro-fit hazard is concrete: D-10 returns *after* the residual is known, the fold arrives, and the temptation is to grade the fold by whether it closes the gap. Four pre-commitments, filed **before D-10 returns**:

1. **PLACEMENT GATE, FIRST AND SEPARATELY.** The armed body's placement count on the graded cell is published **before any armed-row fold is graded**. If placements == 0, the row is graded **`NOT-INSTANTIATED — contributes zero by construction`** and is **FORBIDDEN from appearing in any residual-attribution sentence.** ⚑ This is the pre-commitment that cannot be retro-fitted, because the placement count is a property of the roll, not of the decode.
2. **BOTH ARMS' DIRECTIONS, REGISTERED NOW.** `min = magnitude` ⇒ ↑ health-lane threat, and *a correction owed to any prior figure that read 2.0/10.0 as damage*. `min = duration` ⇒ ↑ control-carrying landings, health contribution **zero**. Whichever returns, the model moves in a pre-named direction and neither reading gets to be a surprise.
3. **ATTRIBUTION IS A SEPARATE ROW FROM THE FOLD, AND IT RUNS FIRST.** The spike-vs-attrition classifier (`L-50`, now two-sided per `F-2`) classifies each death **before the armed rows exist in the model**, so the classification cannot be re-drawn to accommodate them.
4. ⚑ **REFERENT-SIDE EXISTENCE CHECK — nobody in this run has asked it.** *Did the referent's board contain bodies the sim's roll never produced?* If Grava'Thul (or any never-rolled body) appears in the referent footage, that is a **ROSTER-COMPOSITION divergence** and it belongs in the twin-test's distributional-fidelity frame (`L-49` ③), not in the specials frame at all. Routed to the video lap, **reported, graded by nothing.** This is the question that decides whether never-rolled bodies matter to the residual *at all*, and it is cheap.

---

## 3 · Q3 — FACET (c) COVERAGE HONESTY, AGAINST THE RATIFIED MATRIX

**`PARTIAL` at SIM is the honest cell, and the refusal band is nowhere near narrow enough to claim CLOSED-at-record. Three independent grounds, any one sufficient.**

**(1) Two of the four decoded gate fields are not consumed.** D-2 decoded `Chance · Delay · Timeout · Range`. B-4 models `Chance`, `Delay` and `skillCooldownTime`; it **loads `Timeout` unread** (`C-B4-3`) and **does not model `Range`** (`C-B4-1`). A facet whose decode has four fields and whose sim consumes two is `PARTIAL` on the plainest reading of the matrix. The 16/159 and 3/159 are *exposures*; the matrix cell asks about **coverage**, and coverage is 2-of-4.

**(2) The band is measured on 18 % of the decoded surface.** 53 of 65 slots (81 %) sit on bodies this ensemble never spawns; **12 slots on 6 bodies** are reachable at all. So *"16/159, 3/159, narrow"* is a statement about **the roll**, not about the refusal — `T-c` applied to the coverage claim itself. Under a different roll or the `L-53` pilot, `C-B4-1`'s annulus reaches 65 slots, and 16/159 is already **10 % of pet special selections firing at distances the decoded gate would refuse.** That is not a rounding error; it is one selection in ten at the wrong range.

**(3) An unresolved family is an active halt condition.** `C-B4-4`'s own honest class — *bounded at zero on this configuration, unbounded off it, and the failure mode is a halt rather than a magnitude* — **is** the definition of a PARTIAL cell. No facet raising `KeyError` on a rollable body is CLOSED at any layer.

**Credit where it is due, and it changes only the conductor's item:** the artifact ships **`lifted_by`** on every refusal (`C-B4-1 → MD-B4-4`, `C-B4-2 → MD-B4-3`, `C-B4-3 → MD-B4-2`). The closure path exists **per refusal**. It does not exist **per facet cell** — the `L-55` cell line reads *"facet (c) SIM = OPENS-PARTIAL"* full stop. Facet (f)'s PARTIAL had a named substrate (`MD-B3-1`); facet (c)'s does not, and the run's target state (§ 1.1) seals on facet coverage. **PARTIAL cells need a `CLOSURE_CONDITION` set on the cell line**, not just a stamp — here `{MD-B4-1 decode · MD-B4-2 ruling · MD-B4-4 build}`. Otherwise *"all aspects present"* seals with two PARTIALs whose paths live only in per-refusal fields three levels down. `F-12`.

---

## 4 · Q4 — `magnitude_class`'s FIRST OUTING: REAL AT THE REFUSALS, CEREMONIAL AT THE SHIFTS

**Real work, unambiguously, in three places:**

- **`C-B4-5` carries `unbounded-unmeasured` and NO price**, with the refusal to invent a decorative one stated in the artifact. That is precisely the laundering `L-50` struck, refused *in the build* rather than described.
- **`C-B4-4` was SPLIT INTO TWO CLAUSES BECAUSE IT HAD TWO MAGNITUDE CLASSES** — bounded-at-zero here, unbounded off-configuration, *"and the failure mode is a halt, not a magnitude."* The column forced a refusal to become two rows. That is a column doing structural work, not a column being filled in.
- **`C-B4-2`'s `0/159` flagged as *a roll not a rule*** with `measurement_condition` attached — `T-c` applied to a **price**, which is a genuinely new address for the trap. *"A refusal reported as free is the most expensive misreading a runtime builder could take from this artifact"* is the right sentence and it is on the artifact.
- And the **three-arm design** answered the instruction better than the instruction asked: no cancellation claim is possible because no cancellation claim is ever needed.

**Ceremonial in one place, and it is the place the column was invented for.** `shift_magnitude_classes` reads `S-B4-1: measured · S-B4-2: measured · S-B4-3: measured`. What is measured in each case is the **population size** — 51 slots, 12 bodies, 14 slots — read off `LoadReport` at emission time. **That is a count of the affected surface, not a measure of the shift's effect.**

⚑ **`magnitude_class` has two referents and this build conflated them.** `L-50` coined the column to separate *"I know how big this bias is"* from *"I do not"* — a statement about **effect**. B-4 filled it with **population**. Concretely: `S-B4-1`/`S-B4-2` are labelled `measured` while their effect on the graded quantity is *one salt's terminal moving 4 waves, confounded with a stream permutation* (§ 1c) — which is the exact over-claim the column exists to prevent. `S-B4-3` is labelled `measured` and its effect was later measured as **exactly zero by never being reached**; the label and the truth agree by luck, not by construction.

**Repair (one field, emission-only):** every `magnitude_class` carries **`magnitude_of ∈ {population · effect-on-record · effect-on-outcome}`.** `S-B4-1`/`S-B4-2` = `measured`/**population**, and `bounded`/**effect-on-outcome** at best. `C-B4-1..3` are already `measured`/**effect-on-record** and correctly so. Without the second field the column reads as an effect claim and is filled with a row count — `F-3`-of-B-3's laundering shape, one level in. `F-5`.

---

## 5 · Q5 — BATON CONSEQUENCES: FOUR LAYER-1 ROWS, TWO BUILD-GATES, ONE MISSING PROVENANCE CLASS

### (a) ⚑ **`T-d` — TWO-ROW SURFACE, ONE READ** *(new trap; sits beside D-8's `T-a`/`T-b` and `L-50`'s `T-c`)*

**Rule, provenance `decoded`:** a monster special's **gate fields** (`Chance · Delay · Timeout · Range`) live on the **caster's creature record**; its **damage** lives on the skill/damage row. Two rows, one skill.

**Trap, provenance `INFERRED-FROM-INCUMBENT-DEFECT` — and the evidence that it is reachable is that this sim fell into it:** a runtime that takes **admission** from one row and **construction** from the other loses the gate *silently*. `threat.py:850-853` admitted 14 slots *because they declare a `skill_cooldown_s`* and then built all 14 with `cd = delay = chance = 0.00`. Same family as `T-a` (the ACTION stops the skill, not the state transition) and `T-b` (`GetDefenseAttributes` gates on RANK, not is-active): **reading the wrong row of a two-row surface.**

**Player consequence, and this is why the row is high-value:** mis-implemented, elite and nemesis specials fire on *every* opportunity in reach with no cooldown and no chance roll. The fight does not become merely harder — it becomes **illegible**. The player cannot learn a telegraph that has no rhythm, and the encounter reads as arbitrary rather than difficult. That is the Diablo III pre-2.0 affix-soup failure exactly: monster abilities without cadence produce a fight the player experiences as *random*, and a player who cannot attribute their death to a readable cause stops improving and starts resenting. The Godot team is building this exact join. The row must ship with the trap named, not just the field locations.

### (b) Pet-special gating — the table, plus the field the baton does not yet have

§ 10's row shape is correct and the `capability_*` / `measurement_*` split is applied where 53 of 65 rows are exactly the shape it protects. **One field is missing and it is load-bearing.**

⚑ **The baton will carry DECODED rules the sim REFUSES.** `Range` annulus (`C-B4-1`, 39/39 pet + 164/164 roster bodies populated) and `Timeout` (`C-B4-3`, values decoded) are **decoded** — so by the run's own law they ship to Layer 1. But the sim does not consume them. A Godot team building faithfully from the baton therefore builds a **more complete model than the sim**, and the twin-test (target-state item 4: recorded-path drive → tolerance bands) will register that divergence as **Godot's error** when it is the **sim's incompleteness**. There is no field on the baton, and no clause in the twin-test spec, that can express this.

**Owed, and it is a Wave-4 schema item for S-1:**
- a **fourth provenance class — `DECODED-NOT-CONSUMED-BY-SIM`** — alongside decoded / inferred-with-evidence / declared-absent;
- a per-row **`consumed_by_sim: true|false`**;
- a **twin-test pre-registration of which side is authoritative per row.** For a `DECODED-NOT-CONSUMED-BY-SIM` row the **baton** is authoritative and the *sim* is the divergent party — which inverts the twin-test's default assumption and must be stated before the test runs, not after it disagrees.

`F-6`, **baton-blocking.**

### (c) The never-rolled stability property — the Godot runtime needs a **content** gate, not a code guard

The sim's `KeyError` is *correct* at the model layer (GL-12: fail loud rather than guess). **It is not a shippable runtime behaviour**, and neither of the obvious alternatives is acceptable: a silent default is the Law-3 invention, and a guessed resistance is an invention *in the damage-raising direction* — the exact failure `RESIST_PCT`'s own comment exists to prevent.

**Recommended shape (design call — I recommend, conductor/Matt rules):**
- **Baton row:** `UNRESOLVED_FAMILY: {Disruption, ManaBurnDrain} — no player-side consumer decoded; behaviour on encounter is UNDEFINED-IN-MODEL`, provenance **`DECODED-ROW-UNDECODED-CONSUMER`**.
- **Runtime guard:** an unresolved family resolves to **NO-OP with a telemetry flag** — the only option that is *transparently* wrong in a **known direction** (under-threat) rather than opaquely wrong. A crash is unshippable; a guess is unattributable.
- ⚑ **Content gate:** **do not place Grava'Thul (or any body carrying an unresolved family) in the playable build until `MD-B4-1` returns.** A nemesis whose signature ability no-ops is an anticlimax the player *feels* and cannot name — worse than his absence, for the same reason `F-4`-of-B-3 found that inert visible pets read worse than absent ones.

**This is the second build-gate the run has needed, and the pattern is now general enough to state:** *a facet carrying an unresolved family or an unmodelled lifecycle gets a **CONTENT** gate on the baton, not merely a schema note.* Wave-4 should carry the general rule and both instances. `F-7`, **baton-blocking.**

### (d) ⚑ A cross-build interaction nobody has flagged

**Every prior sealed cell in this run ran on a board where 118 of 152 pet-body spawns could not attack** — including B-3's. So `DIVERT_MAX`'s headline (*"removes ~85 % of incoming attack opportunities"*, roster-mean divertible fraction 0.854473) was computed against an **attack-opportunity population that was ~25 % short of the board B-4 now produces.** The band's endpoints move under B-4; the diversion *fraction* may not, but the *opportunities* it is a fraction of certainly do. Likewise the b1/b2/b1r/b2app figures and **every PM1–PM4 grade**.

None of this invalidates a sealed cell — each measured what it measured, on its own basis, correctly (K-7's whole content). But it is a **retrospective validity note owed to the run record and to the PM5 interpretive frame**, and it is not on any artifact or ledger row. `F-8`.

---

## 6 · Q1 (return) — THE `F-1` CLASS REPEATS, AND THIS TIME IT IS INSIDE A PREDICATE

**`F-8`-of-B-2app's re-derivation was carried, faithfully executed, and produced a pair of numbers nobody can read.**

Published: **2 in 683** on `ABSENT`, **1 in 510** on the arm of record. Read as a rate: 0.293 % → 0.196 %, i.e. *"control exposure fell under the arm that adds 51 attack slots"* — the inverse of the registered ↑-threat sign. It did not fall. Both the numerator's loss and the denominator's loss are **the same event**: salt 0's ladder collapsing 5 waves → 1 took its single control landing and its 260 landings with it.

**On the four ladder-matched salts the numerator is `1` on both arms. It did not move at all.**

⚑ **And `B4-P8`'s registered falsifier was *"identical values on `ABSENT` and `D2_ALL`"* ⇒ the predicate demanded that the figure MOVE. It moved — because the denominator collapsed.** A registered falsifier was satisfied by a ladder-length artifact. In B-3 this class lived in prose and in a fold; here it has reached a **predicate**, which is strictly worse, because a green predicate is the surface a Wave-4 emitter and a PM5 grader trust.

**Three repairs, in order:**

1. **Say it.** F-8 at this ensemble is **`UNMEASURABLE-AT-THIS-ENSEMBLE (n = 2 / n = 1)`**, published as a finding. Two consecutive builds have now carried it faithfully and produced an uninterpretable pair.
2. **Publish the matched-ladder normalisation**, which *is* computable from this artifact (unlike B-3's — `n_waves` per cell is emitted, and that is a real improvement worth crediting): landings **per wave** and control-carrying **per landing**, on the ladder-matched subset, with the subset named.
3. **`B4-P8`'s falsifier is re-registered against the matched subset**, so "the figure moved" cannot be satisfied by a ladder that ended early.

⚑ **The defect originates in the conductor's brief.** See § 7. `F-1`.

---

## 7 · ⚠ FRAMING AUDIT — POINTED AT THE CONDUCTOR, AND THIS BUILD IS A CONTROLLED EXPERIMENT

`R-L51-2` briefed the carries as *"MECHANISM + QUESTION only; B-4 derives its own instruments"* — `L-50`'s discipline candidate applied to my own hand on its first outing. **It did not fully hold, and the build is the cleanest evidence the discipline will ever get, because both arms ran side by side.**

| carry | shape as briefed | what it produced |
|---|---|---|
| **Disruption false-absence** | ✅ **mechanism + question** — *"is Disruption absent from this roster, or masked?"* | ⚑ **The mechanism generalised and found `ManaBurnDrain`, which no carry and no ledger row names.** The build says so explicitly: *"found because the carry was briefed as a mechanism rather than a name"* |
| **limb-B loaded-never-rolled** | ✅ **mechanism + question** | ⚑ Became a **STABILITY property** — *"the only thing standing between this configuration and a halt is a roll"* — a reframe no instrument-shaped ask would have reached |
| **`F-8` 2-in-562 re-derivation on B-4's own basis** | ❌ ⚑ **PRE-NAMES THE INSTRUMENT.** It names the QUANTITY (a 2-in-562 *count pair*), the OPERATION (re-derive), and the BASIS | **Produced `2/683 → 1/510` — uninterpretable, and it satisfied a registered falsifier by a denominator artifact** (§ 6). ⚑ **This is `K-5` again: a COUNT named where the mechanism is a RATE. B-3's `F-1` is unrepaired, and I re-committed it in the brief that followed the verdict which found it** |
| **`magnitude_class` column** | ⚠ **instrument named, referent unnamed** | Filled with **population-magnitude** where `L-50` meant **effect-magnitude** (§ 4). ⚑ The mirror of the law: *naming an instrument without naming the question it answers gets it filled with the wrong referent* |
| **W1 / W2 / W3-mechanism / W4 + F-10** | n/a — repair prescriptions | All landed, all with instruments better than prescribed (`B4-P11c`'s mutation proof, `B4-P17c`'s historical-defect payload) |
| **this verdict's own Q1** | ❌ *"missing most of its teeth"* (25 %, not most) and *"108 bodies wake"* (**12** bodies; 108 spawns) | ⚑ **The brief re-committed, in its question, the exact conflation `ADDENDUM 1`'s `D-B4-2` was written to repair** |

**Two things follow, and both belong in the run-close harvest.**

**(i) The discipline is now empirically supported, not merely argued.** Same build, same author, same seat: **two mechanism-shaped carries produced findings the conductor did not ask for; the one instrument-shaped carry produced a number nobody can read.** That is as close to a controlled comparison as this run can generate, and it is worth more than the argument that motivated the candidate.

**(ii) The discipline needs one clause before ratification, or it will be mis-applied.** `L-50`'s law governs **FORWARD CARRIES** (open questions). It must **NOT** govern **REPAIR PRESCRIPTIONS** (closed defects at a named address) — a Gate-2 WARN *necessarily* names an instrument, because that is what a repair is. Without the clause, the next build refuses a gate finding on carry-shape grounds. Proposed text, appended to the candidate:

> *A forward carry names the MECHANISM and the QUESTION; the build derives the INSTRUMENT. **A repair prescription against a closed defect at a named address is exempt — it names the instrument because the defect is already located.** And an instrument issued as a standing instruction must name **what it measures**, or it will be filled with the nearest measurable thing.*

The third clause is `magnitude_class`'s lesson and it is new.

**`R-L55-2`'s rationale is the fourth conductor item and the most urgent, because D-10 has not returned.** § 2(a): the SPIKE-LANE framing pre-commits health-lane, firing, and residual-relevance — on a body with **0 placements**. Replace with **STABILITY + UNITS-CORRECTNESS**, which hold under both arms of the fork. `F-9`.

---

## 8 · FINDINGS

| # | sev | finding | disposition |
|---|---|---|---|
| **`F-1`** | **WARN, design-critical** | The B-3 `F-1` class **repeats inside a registered predicate.** F-8's `2/683 → 1/510` is entirely salt 0's ladder collapse; on ladder-matched salts the numerator is `1` and `1`. `B4-P8`'s *"the figure MOVES"* falsifier was satisfied by a denominator artifact | Publish F-8 as **UNMEASURABLE-AT-THIS-ENSEMBLE**; publish the matched-ladder normalisation (computable from this artifact — `n_waves` per cell is emitted, credit); re-register `B4-P8`'s falsifier against the matched subset. ⚑ **Originates in the conductor's carry** (§ 7) |
| **`F-2`** | **WARN, design — the run's strongest attribution finding, and it is unassembled** | **B-3 salt 1: −72 % landings, terminal unmoved. B-4 salts 1–4: +15.4 % landings, terminals unmoved 4/4.** Two independent perturbations, opposite directions ⇒ **the sim pilot's terminal wave is insensitive to attrition volume.** Composes with `L-53`(c) and `L-54` into: the residual lives in **spike survival**, not sustain | Assemble both legs onto the **PM5 prereg spike-vs-attrition row** and onto the L-55 fold. It appears in neither fold today |
| **`F-3`** | **WARN** | Terminal deltas on the arm of record are **confounded with a stream permutation** — one salt moved, and `S-B4-4` registered that the fold permutes the shared RNG stream by construction (salt 4: landings 23→18 on an identical ladder). `S-B4-4`'s own caution is registered and **not applied to the artifact's headline quantities** | Label terminal deltas **`CONFOUNDED-BY-STREAM-SHIFT`** on the artifact and the fold. The defensible statement is the matched-ladder volume figure, not the terminal |
| **`F-4`** | **WARN, baton-bound** | *"Record-cell exposure NIL"* is conditioned on **roll · pilot · pursuit-model**; `measurement_condition` names only the **roll**. ⚑ `T-c` was adopted as **pilot**-conditioning and narrowed to **roll**-conditioning in transit — at the address where B-5, B-6 and `L-53`'s greedy pack-closing pilot all move the distance distribution that made reach binding | `measurement_condition` gains all three axes; the ledger sentence *"the reach was the binding constraint"* carries them. **NIL on the record arm ≠ NIL on PM5's arm** |
| **`F-5`** | **WARN, design** | `magnitude_class`'s first outing: **real at the refusals** (`C-B4-4` split into two clauses *because* two classes; `C-B4-5` honestly blank; `C-B4-2`'s roll-not-rule), **ceremonial at the shifts** — three `measured` labels that measure **population size**, not effect. `S-B4-1/2` are `measured` while their effect is one confounded salt | Add **`magnitude_of ∈ {population · effect-on-record · effect-on-outcome}`.** Without it the column reads as an effect claim and is filled with a row count — `F-3`-of-B-3's shape one level in |
| **`F-6`** | **WARN, baton-blocking** | **The baton will carry DECODED rules the sim REFUSES** (`Range` annulus, `Timeout` scope). A faithful Godot build is then *more complete than the sim*, and the twin-test reads the **sim's incompleteness as Godot's divergence.** No field expresses this | S-1 schema: fourth provenance class **`DECODED-NOT-CONSUMED-BY-SIM`** + per-row `consumed_by_sim` + **twin-test pre-registration of which side is authoritative per row** (for these rows it is the baton — inverting the test's default) |
| **`F-7`** | **WARN, baton-blocking** | The unresolved-family halt needs a **CONTENT gate**, not a code guard. The sim's `KeyError` is right at the model layer and unshippable at the runtime layer; a silent default is the Law-3 invention; a guess is damage-raising | Baton row `UNRESOLVED_FAMILY` (provenance `DECODED-ROW-UNDECODED-CONSUMER`) + runtime **NO-OP-with-telemetry** + ⚑ **do not place Grava'Thul in the playable build until `MD-B4-1` returns.** Second build-gate; generalise the pattern (with `F-4`-of-B-3) |
| **`F-8`** | **WARN, cross-build** | **Every prior sealed cell — and every PM1–PM4 grade — ran on a board where 118/152 pet spawns could not attack.** B-3's `DIVERT_MAX` (*"~85 % of attack opportunities"*) was computed against an opportunity population ~25 % short of the board B-4 produces | Retrospective validity note on the run record + the PM5 interpretive frame. No cell is invalidated (K-7); the note is owed anyway |
| **`F-9`** | **WARN, conductor — act before D-10 returns** | `R-L55-2`'s SPIKE-LANE rationale pre-commits **health-lane**, **firing**, and **residual-relevance** on a body with **0 placements**. `MD-B4-1`'s own first question is whether the rows are on the health lane at all | Replace the rationale with **STABILITY + UNITS-CORRECTNESS** (both hold under either arm). Commission unchanged, reason replaced, **in the ledger, this commit** |
| **`F-10`** | **WARN → baton** | ⚑ **`T-d` — TWO-ROW SURFACE, ONE READ.** Gate fields live on the **caster's creature record**, damage on the skill row; a runtime that admits from one and constructs from the other loses the gate silently — evidenced by this sim's own defect. **Player consequence: specials without cadence make the fight *illegible*, not merely harder** (D3 pre-2.0 affix-soup) | Baton row: rule `decoded`, trap `INFERRED-FROM-INCUMBENT-DEFECT`. Sits with D-8's `T-a`/`T-b` and `L-50`'s `T-c`. Inventory 19+ → **24+** |
| **`F-11`** | INFO, positive → discipline | ⚑ **The framing audit is a controlled experiment this time.** Two mechanism-shaped carries produced unasked-for findings (`ManaBurnDrain`; stability-as-a-property); the one instrument-shaped carry produced an unreadable number. **And the brief's own Q1 re-committed the `108-spawns / 12-bodies` conflation `D-B4-2` had just repaired** | Bank as the empirical support for candidate #2. ⚑ **Add the exemption clause** (*repair prescriptions name instruments legitimately*) **and the referent clause** (*an instrument issued as a standing instruction must name what it measures*) **before jack-ryan ratifies** |
| **`F-12`** | INFO | Facet (c) SIM = **PARTIAL, honestly** — 2 of 4 decoded gate fields unconsumed; band measured on 18 % of the surface; an active halt condition. Credit: `lifted_by` ships the closure path **per refusal**. It does not exist **per facet cell** | Cell lines gain a **`CLOSURE_CONDITION`** set: facet (c) = `{MD-B4-1 · MD-B4-2 · MD-B4-4}`. The target state seals on facet coverage; two PARTIALs must not seal with their paths three levels down |

**Also noted, no action.** Six standalone addenda, **every deviation caught by the instrument the previous addendum built**, and gamora's refusal to self-adopt the discipline the build earned six times over (*"ratifying my own discipline in the build that needed it is a gate's job"*) — correct routing, and the gate should adopt it. `B4-P16c` and `B4-P17c` use the **actual historical defect** as mutation payload rather than a synthetic one; that technique should outlive this run. `ADDENDUM 3` § 1's decision to **strike the vocabulary from the artifact rather than teach the scanner about negation** — *"every clause of fragility in a falsifier is a clause of licence"* — is the single best sentence of engineering judgement in the run. The untracked scratch probe disclosed pre-emptively (*"saying so is cheaper than being caught by it"*), and the deletion declaration whose mechanism **is the absence**, are `W3` discharged better than `W3` asked. And § 0.3's reach-vs-gate frame, **registered before any measurement**, landed on the one slot where it could be tested and was right — which is what pre-registration is for.

---

## 9 · DISPOSITION

**PASS — with design findings. No BLOCK.** Nothing on this artifact is wrong in a way that moves a figure. Every dissent concerns **what the figures may be read to mean**, **what the baton must carry so a Godot session does not build a model the sim refuses**, and **three conductor sentences that pre-commit open answers.**

Carried forward:

- **Baton-blocking before the Wave-4 emitter (three):** `F-6`'s `DECODED-NOT-CONSUMED-BY-SIM` provenance class + `consumed_by_sim` + twin-test authority pre-registration; `F-7`'s `UNRESOLVED_FAMILY` row + runtime NO-OP + **Grava'Thul content gate**; `F-10`'s `T-d` trap row.
- **Baton rows owed (facet c), five:** the 65-slot five-field gate table with `capability_*`/`measurement_*` (§ 10, correct as drafted) + `consumed_by_sim` · the decoded metre annulus flagged unconsumed · `T-d` · `UNRESOLVED_FAMILY` · the `S-B4-5` key-meaning change for consumers. Inventory 19+ → **24+**.
- **Rides the next gamora touch:** `magnitude_of` (`F-5`) · `measurement_condition`'s three axes (`F-4`) · matched-ladder normalisation + `B4-P8` falsifier re-registration (`F-1`) · `CONFOUNDED-BY-STREAM-SHIFT` labels (`F-3`).
- **PM5 prereg accumulation:** the **placement gate** and the **both-arms direction registration** for `MD-B4-1`, filed **before D-10 returns** · the attribution row running **before** any armed-row fold · the **referent-side existence check** for never-rolled bodies (reported, graded by nothing) · `F-2`'s two-sided attrition falsification as the spike-vs-attrition instrument's second leg · `F-8`'s retrospective validity note as interpretive frame.
- **Discipline candidates → jack-ryan:** candidate #2 with `F-11`'s **empirical support** plus its **two new clauses** (repair-prescription exemption; instruments must name their referent) · gamora's candidate #3 (*any count or name on a digested surface must be DERIVED*) — **six surfaces, one mechanism, one build**; the author correctly declined to self-adopt it · `ADDENDUM 2` § 4's disjointness candidate.
- **Conductor:** `C-1` amend the **L-55 fold** — it omits the arm-of-record terminal movement, the matched-ladder +15.4 %, and the `683→510` denominator artifact · `C-2` **replace `R-L55-2`'s rationale before D-10 returns** (`F-9`) · `C-3` file the four PM5 pre-commitments · `C-4` file `F-8`'s retrospective validity note · `C-5` add `CLOSURE_CONDITION` to PARTIAL cell lines (`F-12`).

---

*DRIFT-CRITIC verdict, gandalf, 2026-08-24. Judged out of the conductor's foreground per the `L-23` pattern. The build's best work is that its carry was briefed as a mechanism and the mechanism generalised — `ManaBurnDrain` exists on this record because nobody named it. Its most valuable find is that the fight's busiest pet body has been unable to attack in every sealed cell this run has produced. My sharpest dissent is that the run's own two builds have now measured, from opposite directions, that the sim pilot's death is not attrition-shaped — and that neither fold says so. My most uncomfortable is that the measurement class B-3's verdict convicted me of, I re-issued in the brief the same verdict launched. Committed, not pushed.*
