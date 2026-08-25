# KC2 MODEL-COMPLETION RUN · **B-3app** — gandalf DRIFT-CRITIC verdict

▶ **ROLE: DRIFT-CRITIC** — seated by conductor ruling **`R-L63-2`**, *design-fit-only by declaration.*

**Agent:** gandalf · **Date:** 2026-08-25 · **Seat:** parallel to jack-ryan Gate-2 (`R-L63-1`)
**Build:** gamora B-3app, commits `a1c4f951` → `bfba77b3`
**Commission judged against:** `R-L52-2` (fired at `R-L60-5`) + standing run law (`B1r-Q`, Law 3, `L-38`,
`K-10`, `R-L56-2`), **not against taste**.

⚑ **DRIVER NEVER RUN.** Per `R-L63-2` and the B-4 seating lesson: I read the committed artifact
`output/kc2-checkpoint-E-s09-cp150-b3app-20260825_024524.json` as a **file**, the math note + three
addenda, `summon_offense.py`, `MIGRATION.md`, and the two build commit messages. No checkpoint was
touched, no test executed, no process started. Every number below is quoted from a committed byte.

---

## TOP LINE

> ## **PASS — with thirteen findings. Three are BLOCKING for downstream consumers; none invalidate the build.**

B-3app is the strongest build of this run on craft. Three defects self-caught with no reviewer
present. Three predicates shipped **FAILING** beside their successors rather than rewritten. Laws
imported by identity rather than paraphrased. Not one fitted constant. The reader-not-record catch
(`D-B3app-1`) is the kind of self-conviction that makes a seam trustworthy, and `D-B3app-3` is a
finding the commission did not ask for and could not have obtained any other way.

**And the seal line it closes on is wrong.** Not sloppy — *formally* wrong. `facet (f) SIM =
CLOSED-WITH-PRICED-REFUSALS … survival is bounded from OPPOSITE sides` describes a bracket that does
not close, on an arm the same decode has just falsified. The build published every fact needed to see
this, on the same artifact, two keys apart. What failed is the **sentence over the facts** — which is
the sixth consecutive instance of that exact failure on this run, and this time **it is the
conductor's** as much as the builder's.

The cell may seal. The **cell-line wording** may not ship as written, and the **residual-exclusion
sentence in `L-63` must be struck** before PM5 inherits it.

---

## THE FINDINGS

### `F-1` · **BLOCKING (seal wording)** — THE BRACKET DOES NOT CLOSE, AND `UNBOUNDED-UNMEASURED` IS THE MISSING LEG

*Answers question 2 directly.*

The claim, in three places (`⚑ cell_line`, math note § 11, MIGRATION § 3):

> *"Offense is a STRICT LOWER bound and `DIVERT_MAX` a STRICT UPPER one, so survival is bounded from
> OPPOSITE sides with no fitted constant."*

Survival is **monotone increasing in both** legs: more summon offense ⇒ faster ladder ⇒ more survival;
more summon tanking ⇒ fewer landings ⇒ more survival. Run the algebra on the arms the build actually
produced:

| arm | offense leg | tanking leg | what it bounds |
|---|---|---|---|
| **C3** (arm of record) | lower bound | **zero** (`PRESENT_INERT` — below any true tanking) | ✓ a genuine **LOWER** bound on survival |
| **D3** (upper limb) | **lower** bound | **upper** bound (`DIVERT_MAX`) | ✗ **neither** — the legs point opposite ways |

An **upper** bound on survival requires an **upper** bound on summon offense. The build does not have
one and says so: `C-B3app-4` (weapon contribution) is graded **`UNBOUNDED-UNMEASURED`**, and
`C-B3app-5` (pet difficulty pak) likewise. So the upper side of the bracket **does not exist**.

> ⚑ **`UNBOUNDED-UNMEASURED` is not being laundered — it is doing exactly the load-bearing work the
> seal line hides.** `F-3`'s `magnitude_class` column was invented on this run precisely so an
> unbounded refusal could not sit next to priced ones and be read as one of them. Here it sits next to
> a *sentence* that reads as a two-sided bracket, and the column cannot see sentences.

**What is honestly true and should replace the line:**

> facet (f) SIM = **CLOSED-WITH-A-ONE-SIDED-BOUND.** The `PRESENT_INERT` arm is a strict LOWER bound
> on survival: both its legs (offense-`Min`-basics-only, tanking-zero) sit below the decoded truth.
> `DIVERT_MAX` is a strict upper bound on **tanking alone**, not on survival. No upper bound on
> survival exists on this build, because `C-B3app-4` declares summon offense `UNBOUNDED-UNMEASURED`
> above; `MD-B3app-2` is the one lap that would create one.

**Player-consequence framing (why this is mine and not jack-ryan's):** a one-sided bound tells you
*"the real character is at least this strong."* A two-sided bracket tells you *"the real character is
in here."* Every design decision downstream — how hard the referent's board is, whether the sim's
pilot is under-performing, whether a Godot encounter tuned to this model will feel like the
referent — needs the second sentence. Shipping the first one wearing the second one's clothes is how
a studio tunes a difficulty curve to a floor and ships a game that plays easy. That is Diablo III
vanilla Inferno in reverse, and it is the exact reason `B1r-Q` exists.

---

### `F-2` · **BLOCKING (PM5)** — THE ARM OF RECORD IS THE ARM THIS DECODE FALSIFIED, AND THE RESIDUAL IS HALF THE SIZE IT IS FRAMED AT

D-9's decode says two things about a summon body, both `MEASURED`:

1. `invincible = True` ⇒ five gates early-return ⇒ **takes none**;
2. `IsTargetable@Monster` (`0x002dc780`) takes the **`xor al,al` limb** for an invincible-in-DBR body
   ⇒ **stays targetable** ⇒ **draws attacks**.

The build itself names the consequence: *"draws attacks, takes none — the shipped aggro-sink shape"*
(math note § 3.1), and re-grades `S-B3-3` (summons as aggro sinks) `assumed → decoded`.

> ⚑ **Therefore `PRESENT_INERT` — summons present, diverting NOTHING — is a configuration the engine
> cannot produce.** It is not a conservative estimate. It is a decoded impossibility.

And it is the arm every headline number of this run is quoted from. `C0` terminal waves are
**`[155, 156, 152, 151, 151]`** — that is where *"151–156 vs 160"* comes from. The decoded-admissible
ceiling is `D3` = **`[156, 156, 160, 156, 156]`**.

| | framed residual | residual that survives the decode |
|---|---|---|
| per-salt gap to 160 | 4 · 4 · 8 · 9 · 9 | **4 · 4 · 0 · 4 · 4** |
| mean | 6.8 waves | **3.2 waves** |
| salts at the referent | 0 of 5 | **1 of 5** |

**The exclusion set — attrition volume (`F-2`/B-3+B-4), channel uptime (`L-53`(c)), energy (`L-54`),
now summon offense — was assembled to explain a gap roughly twice the size of the one that survives.**
Every member of that set was excluded for failing to move a number by enough. The bar they were
measured against was set on the falsified arm.

I am not claiming the residual is gone. I am claiming its **magnitude, and therefore the sensitivity
any PM5 instrument needs, has changed by a factor of two**, and that this is a fact about the model's
own arms — not a survival grade, and therefore not a `B1r-Q` violation to state.

**Disposition:** PM5 pre-registration row, filed BEFORE PM5 grades anything, in `R-L56-2`(i)'s shape:
*the residual figure PM5 grades against must name its arm, and an arm graded `PRESENT_INERT` must
carry the `decoded-impossible-configuration` label.*

---

### `F-3` · **BLOCKING (ledger)** — THE `L-63` EXCLUSION SENTENCE IS A GRADE ON UNGRADED SURVIVAL FIGURES, INFERRED IN THE WRONG DIRECTION FROM THE BUILD'S OWN BOUND

*This is the framing audit of question 6. The conductor's sixth headline, and it does not survive.*

`L-63` reads:

> *"**Residual analysis strengthened:** summon offense ≈10⁻⁴ of player output ⇒ the 151–156-vs-160
> deficit is **NOT summon-offense-shaped** — joins `L-53`(c)'s exclusion set."*

Three separate defects in one sentence.

**(a) It is a grade, and `B1r-Q` forbids grades.** The artifact restates the law verbatim:
*"EVERY SURVIVAL FIGURE ON THIS ARTIFACT IS REPORTED AND GRADED BY NOTHING until PM5 … The terminal
waves in `ensemble` are NOT evidence that the model got closer to 160."* "Not X-shaped" is a verdict
about what moves survival. The builder refused to grade; the conductor graded on his behalf.
⚑ **`B1r-Q` was applied selectively — ungraded where the number was inconvenient, graded where it
supported an exclusion.**

**(b) The inference runs the wrong way down the bound.** An exclusion needs an **upper** bound:
*"summon offense cannot exceed X, and X is too small to matter."* The build delivered a declared
**lower** bound with two `UNBOUNDED-UNMEASURED` refusals beneath it. The priced ones alone are not
small: `C-B3app-1` measures refused specials at **5.28×** the folded basic magnitude on the
Deathstalker; `C-B3app-2` prices the unsampled roll width at 85 / 36; `C-B3app-3` prices refused DoT
at 23.3 / 5.3 DPS pre-resist. Compounding the priced refusals alone moves the figure by roughly an
order of magnitude before `C-B3app-4`'s unbounded weapon term is even opened. **A lower bound cannot
exclude anything. That is what "lower bound" means.**

**(c) The artifact publishes the counter-evidence, and the fold walked past it.** `S-B3app-1`'s own
`measurement` block:

```
terminals_D2_to_D3:  D2 [156,156,156,156,156]  →  D3 [156,156,160,156,156]
```

Adding the offense limb to the decoded-admissible arm moved salt-2 to **exactly the referent's
terminal wave**. The build put that in the shift row it was required to sign. The fold that declared
summon offense excluded had it in hand.

**Disposition:** strike the sentence from `L-63` in-ledger, `C-1` shape, as was done for `L-55`.
Replacement, computable from the artifact and published nowhere:

> On the arm of record the offense limb moved **zero terminal waves on all five salts**
> (`C2 == C3 == [155,156,152,151,151]`) while delivering 22,611 applied damage and **0 kills**. On the
> decoded-admissible arm it moved salt-2 by **+4 waves, onto 160**. Summon offense at its *modelled*
> magnitude does not move the ladder; whether it does at its *unrefused* magnitude is
> `UNBOUNDED-UNMEASURED` and gated on `MD-B3app-2`/`-3`. **No exclusion is available from this
> build.**

---

### `F-4` · **WARN** — THREE `UNBOUNDED-UNMEASURED`, NOT TWO. TWO `↑`, NOT ONE. AND THE MISCOUNT SHIPS ON THE DIGESTED SURFACE

The seal line, the commit message, MIGRATION § 3, `L-63`, and the emitted `⚑ bound_direction` string
all carry *"six ↓, one ↑, two `UNBOUNDED-UNMEASURED`."* The emitted refusal ledger, in the same file:

| refusal | signed bias | `magnitude_class` |
|---|---|---|
| `C-B3app-4` weapon | ↓ | **`UNBOUNDED-UNMEASURED`** |
| `C-B3app-5` pak | ↓ | **`UNBOUNDED-UNMEASURED`** |
| `C-B3app-7` target angle | ↑ | `measured` (77 of 727 swings) |
| **`C-B3app-9` warm-up duty cycle** | **↑ Guardian availability** | **`UNBOUNDED-UNMEASURED`** |

**Three unbounded. Two upward.** And `C-B3app-7`'s own `⚑ signed_bias` field reads
*"↑ summon damage — **the ONE refusal pointing up**"* while `C-B3app-9` sits **two keys below it in
the same dict** signed `↑`.

Availability multiplies damage. A sim that never re-enters warm-up casts the Guardian more often than
the referent can, by an unmeasured duty cycle. So the offense arm is a **lower bound on
damage-per-available-second** and an **upper bound on availability**, and their composition is
**unsigned**. The `⚑ bound_direction` string asserts a strict lower bound over a product whose second
factor points the other way.

⚑ **`B3app-P16` — the quantifier predicate — HOLDS, and could not have caught this.** Its registered
scope is *"every occurrence of `all`/`every`/`none` in an emitted prose string is checked against the
table **two keys away**."* The contradicting row is in a different block entirely. **Fourth
instrument-before-question failure of this build**, on the one string that carries the seal.

**Disposition:** ride the next gamora touch (B-5/B-6). Repair is one line: derive the `↓`/`↑` census
and the `magnitude_class` census **from the refusal ledger** instead of typing them, exactly as
`⚑ the_split` was made derived under `F-2`. Extend `B3app-P16`'s scope from "two keys away" to "any
count or quantifier that has a table anywhere on the artifact."

---

### `F-5` · **WARN** — `C-B3-8` RECEIVED "THE PRICE IN FULL" AND IS ABSENT FROM THE GRADED LEDGER; FOLLOWING THE POINTER TERMINATES IN A CYCLE AT ZERO

`C-B3-1`'s re-grade (math note § 3.2, `S-B3app-6`, and the emitted ledger) says:

> *"B-3 priced this at 'the entire width of the § 3 band'; that width was never about pet life and
> **MOVES IN FULL to `C-B3-8`**."*

The re-worked top-level `⚑ refusals` ledger has **14** entries: `C-B3-1`, `-2`, `-3`, `-5`, `-10`, and
`C-B3app-1…9`. **`C-B3-8` is not among them.** It survives only inside each salt's *inherited* B-3
block, where its `price_units` still read:

```
"C-B3-8": { "what": "petAngerTransference share arithmetic (D-3 R-4)",
            "price": 417, "price_units": "same number as C-B3-1 — the band replaces the ranking" }
```

Follow the chain a reader is given: `C-B3-1` → *"moves in full to `C-B3-8`"* → `C-B3-8` → *"same
number as `C-B3-1`"* → **structural zero, decoded**. Two hops, a cycle, terminating at nothing. The
band's whole width now lives on the one refusal the artifact's graded surface does not carry and
`B3app-P14` does not police.

⚑ **And the reason it escaped is `F-9`'s shape at the ledger layer.** `B3app-P14`'s population is
defined by **label** — *"every `C-B3app-n` **and** every **re-graded** `C-B3-n`"*. `C-B3-8` was not
re-*graded*; its **substance** changed, which `S-B3app-6` states in as many words. The predicate's
population was fixed before the question *"which refusal now carries the band's width?"* was finished.

**Disposition:** ride B-4app (the next refusal-ledger touch). `C-B3-8` enters the top-level ledger
with `magnitude_class: UNBOUNDED-UNMEASURED` (share arithmetic is undecoded — `D-3 R-4`),
`magnitude_of: effect-on-outcome`, and the per-salt diversion counts as its price. Extend
`B3app-P14`'s population from *re-graded* to *re-graded **or re-priced***.

---

### `F-6` · **WARN** — `D-B3app-3` DISPOSITION: ROUTING IS SUFFICIENT. ONE ATTRIBUTION BAR AND ONE DECODE ARE OWED

*Answers question 4's hard half: does `DIVERT_MAX`'s count-insensitivity demand a repair before PM5?*

**No — and a repair now would be a Law-3 violation.** `DIVERT_MAX` sends every non-ignoring
opportunity to a summon whenever *any* summon is live. It is a **saturating** upper bound. Saturation
at one pet is not a bug in an upper bound; it is what "upper bound" means. `D1 == D0` byte-identically
is the correct behaviour of a correctly-declared maximum.

The only thing that would make count matter is the **share** — `petAngerTransference` — and `D-3 R-4`
grades its semantics **undecoded**. Modelling share without the decode is a fitted constant wearing an
aggro table. Law 3 forbids it. So *route to the residual rows* is the right call and I concur with the
conductor's disposition.

**Two things are owed beside it.**

**(i) An ATTRIBUTION BAR, in `R-L56-2`(i)'s exact shape, pre-registered before PM5 grades:**

> The sentence *"the model reaches the referent's terminal wave"* may **not** be attributed to the
> summon fold on the `DIVERT_MAX` arm. That arm is maximally optimistic on tanking **and** decoded
> insensitive to the quantity (count · reach · share) that would make its optimism physical. A 160 on
> `D3` is a statement about a saturated bound, not about summons.

**(ii) `MD-B3app-5` — DECODE `petAngerTransference` SHARE SEMANTICS. This should be the next lap, and
the artifact says why louder than anything else on it.**

Both places this model reaches **160** are **diversion**-side, not offense-side:

| cell | what changed | terminal |
|---|---|---|
| `D3` salt-2 | offense added to the saturated tanking arm | **160** |
| `X4` salt-0 | Bernoulli key `PER_RECORD` → `PER_INSTANCE` (`S-B3-8`/`F-6`) | **160** (vs `D3`'s 156, same salt) |

⚑ **A modelling choice about the diversion Bernoulli's *key* — nothing to do with damage, nothing to
do with the pilot — moves the terminal wave 156 → 160 on the same seed.** And the incumbent default
(`PER_RECORD`) is the one `F-6` already flagged as the wrong key. Diversion is undecoded on **two**
axes (key semantics, share arithmetic) and is the single largest unexplained lever in this artifact.

**The run's residual attention is pointed at the pilot and at offense. The artifact says it belongs on
diversion.** That is a course correction, and it is mine to raise.

---

### `F-7` · **BATON-BLOCKING** — `DECLARED-ABSENT` IS A LANDING VERDICT WEARING AN ABSENCE'S NAME, AND THE GODOT LAYER MUST NOT INHERIT IT

*Answers question 3's first half.*

`route_control`'s terminal branch (`summon_offense.py:629`):

```python
return ZeroVerdict(
    family=family, summon=summon, zero_cause=ZERO_DECLARED_ABSENT, grade="DECLARED",
    evidence="no zero applies — the family would LAND on this body", ...)
```

The **evidence string is right**. The **token is the inverse of it.** And the token ships on the
emitted `⚑ zero_router` matrix on precisely the six families the finding is about:

```
Deathstalker:Stun      gate_on NOT-ENROLLED   gate_off DECLARED-ABSENT
Guardian:Freeze        gate_on NOT-ENROLLED   gate_off DECLARED-ABSENT
… Petrify · Sleep · Trap · Knockdown, both summons
```

A consumer — a Godot builder, a telemetry schema, a future me — reads
`zero_cause = "DECLARED-ABSENT"` on a **Stun** row and concludes *stun is declared absent for pets:
pets are stun-immune.* That is **exactly backwards**, and it is the one sentence the § 4.1 finding
exists to prevent: *"a build that reads resistance first reports the six families as 'unresisted' and
lets the board stun the summons."* The build defeated that failure at the **ordering** layer and
re-introduced it at the **naming** layer, one field to the right.

Three compounding problems, all naming:

1. The field is called **`zero_cause`** and the value means *"there is no zero."* A closed vocabulary
   (`B3app-P11`, `ZERO_CAUSES`) with a member that is not a member of the category.
2. `DECLARED-ABSENT` collides with `MEASURED-ABSENT` / `DECODED-NOT-CONSUMED-BY-SIM` and the rest of
   the run's absence taxonomy, every one of which means *the thing is not there*.
3. `grade: "DECLARED"` on a row whose whole content is a **decoded** consequence.

**Disposition — baton-blocking, repair before the Wave-4 emitter:** either rename to
`WOULD-LAND-NO-ZERO-APPLIES`, or — better — move it **out of `zero_cause` entirely** into a
`disposition` field whose vocabulary is `{ZERO, WOULD-LAND, UNDECIDED}`, leaving `zero_cause`
populated only when there **is** a zero. `T-d`'s lesson from B-4 verbatim: a runtime that admits from
one field and constructs from another loses the gate silently. Here a consumer admits from
`zero_cause` and inverts the finding silently.

---

### `F-8` · **BATON-BLOCKING (design)** — ONE FLAG, TWO SEPARABLE DESIGN PROPERTIES, AND THE FORK IS MATT'S

*Answers question 3's second half: is pet stun-vulnerability a substrate truth the baton must carry?*
**Yes — and the row it must carry is not "pets can be stunned." It is the coupling.**

`invincible = True` is **one** DBR field. Through `AddFixedDamage@DurationDamageManager`
(`0x00208d46`) — *the function that fills the fixed-damage buckets `UpdateFxAndInfluence` elects from*
— it produces **two logically independent** design properties:

- **(a) pets cannot die** — an aggro sink that cannot be popped;
- **(b) pets cannot be stunned, feared, confused, frozen, petrified, slept, trapped or knocked down** —
  and *not* because they resist: `defensiveStun/Freeze/Petrify/Sleep/Trap/Knockdown` are **ABSENT
  from both innate passives**. At 0 % resist. The enrolment gate is the only thing standing there.

> ⚑ **A builder who wants MORTAL pets gets STUNNABLE pets for free, and will not know until playtest.**
> Flip one flag to give the player a pet that can die, and the same flip hands the board six control
> families at zero resist against it.

**Genre precedent, because this fork has been taken three times in one franchise:**

- **Diablo II — Necromancer skeletons: mortal AND curseable.** The entire "army as a resource you
  spend and rebuild" fantasy comes from exactly that coupling. Skeleton loss was legible, attributable
  and *actionable* — you re-raised from corpses that were right there.
- **Diablo III — Zombie Dogs / Fetish Army: permanent-with-respawn.** The fantasy flattened to ambient
  DPS. Pets became a number on the sheet. Nobody mourned a Fetish.
- **Diablo IV launch — Necromancer minions: mortality restored, auto-resummon on a timer.** The worst
  seat of the three: the player *feels* the loss (the damage stops) and cannot *act* on it (the timer
  owns the recovery). Feedback without agency reads as unfairness, not as tension.

**Player consequence for Reincarnated specifically.** Our pet is not a DPS pet. The design intent on
record is a **loot-carrier that persists across body-swap** and hands to the Spirit Guide — which is a
*logistics* actor inside a mobile-first density solution. Apply the fork:

- **Pet mortal + stunnable** ⇒ the loot-carry loop acquires a **failure state the player must
  defend**. That is a real mechanic and it composes with the spirit-swap identity theme: the thing
  that carries your accumulated gains across forms can be interrupted. Cost: it makes loot loss a
  legibility problem, and Diablo IV shows what illegible pet-loss feels like.
- **Pet immortal + immune** (the GD shipped shape) ⇒ the pet is **furniture with a bag**. Zero
  tension, zero decisions, and — because `IsTargetable` still returns true — it is *also* a free
  permanent aggro sink, which is a balance surface with no counterplay.

Neither is obviously right. **It is a design ruling, and it belongs to Matt at baton time — not
inherited silently from the value of one DBR field in a calibration referent.**

**Baton rows owed (three, one row each, all Layer-1 `decoded`):**
1. `invincible` is ONE flag with TWO consequences (a)+(b) — named as a coupling, with the gate address.
2. The six families read `<ABSENT ⇒ 0>`, not "resisted" — decoupling (a) from (b) requires **adding**
   resistances, not just flipping the flag.
3. `R-D9-4` beside them: `PetPlayerScaling` suppresses the `ContributePetBonus` fold — a builder must
   not assume "scale the pet by the player's sheet" exists.

---

### `F-9` · **WARN** — THREE UNEXERCISED LIMBS ON ONE ARTIFACT; ONE OF THEM IS ADVERTISED TO CONSUMERS AS A BREAKING CHANGE

**(a) The imported hit law never returns "miss."** Across every cell and salt:

| cell | swings | hits | **misses** |
|---|---:|---:|---:|
| C3 (5 salts) | 727 | 533 | **0** |
| D3 (5 salts) | 1,886 | 1,550 | **0** |
| X4 (1 salt) | 568 | 496 | **0** |

**1,796 target rows, zero misses.** `B3app-P6` proves `threat.probability_to_hit` and
`threat.resolve_hit` are the sim's own functions **by object identity** — an excellent predicate. It
certifies **provenance**. The ensemble shows the law is a **saturated no-op discriminator** at these
OA/DA pairs: the RNG is drawn 1,796 times and decides nothing but crit tier. Nothing is wrong; it is
**unmeasured**, and the artifact does not say so.

**(b) `offense_kills: 0` in every cell and salt — and the death path is advertised as BREAKING.**
MIGRATION § 1(c) tells consumers *"`death_cause` gains `killed_by_summon`"*; `S-B3app-5` tells them
*"`damage_dealt` **and death** rows can now carry `source_id = ps_*`."* The damage half fired 412 /
1,262 times. **The death half fired zero times, ever.** A telemetry consumer, a Godot event handler and
the Wave-4 baton emitter will each build against a row shape this sim has never emitted, and will
discover its shape is wrong at integration. That is `B4R-P7`'s never-fired-register lesson — recurring
**inside the build that cited it**.

**(c) `NO-WARM-UP-STATE-IN-SIM`** — correctly named, priced and signed by the build. Cited only to
complete the pattern: **three never-exercised limbs on one artifact; one labelled, two not.**

⚑ **And both unlabelled ones are ZEROS ON THE EMITTED SURFACE WITH NO `zero_cause`** — which
`B3app-P11`'s registered form forbids in as many words (*"no zero is emitted without one"*). P11
**HOLDS** on the artifact because its instrument does not scan raw integer zeros in the `offense`
block. **Fifth instrument-before-question instance of this build**, on the predicate the build
nominated as *closing* `F-8`'s zero-cause axis.

**Disposition:** ride B-5/B-6. `n_misses: 0` gets `zero_cause: SATURATED-PTH-NO-MISS-LIMB-EXERCISED`
(sixth axis member, or `DECODED-ZERO` with a basis string). `offense_kills: 0` gets an explicit
`UNEXERCISED` label **and** MIGRATION § 1(c) gains one sentence: *"this row shape has never been
emitted by any run; its field set is registered, not observed."*

---

### `F-10` · **WARN** — QUESTION 5: THE LAW, THE GUARD, AND WHY `B4-P17`'s DOWNGRADE HOLDS ON A DIFFERENT WARRANT THAN THE ONE GIVEN

**The general law, stated precisely (harvest candidate #4).** `F-9` as I first wrote it —
*"a carry names the MECHANISM and the QUESTION; the build derives the INSTRUMENT"* — was a
**routing** rule about who chooses. The second witness shows the deeper thing, and it is a **typing**
rule:

> **An instrument chosen before its question's REFERENT-TYPE is fixed will measure something
> type-adjacent to the question, and will then pass or fail for the wrong reason.**

Gamora's three, laid out by the type-error they commit — and they are three *different* errors, which
is what makes this a law and not a coincidence:

| predicate | question's referent-type | instrument's type | error class |
|---|---|---|---|
| `B3app-P1b` | *does each limb move the fight?* — a **sensitivity** | an **arm** (`PRESENT_INERT`) | **domain**: the arm cannot express the quantity |
| `B3app-P9` | *does damage enter the sustain **path**?* — a **path** | a **system outcome** | **type**: an outcome cannot be invariant to a fold that changes the system |
| `B3app-P15` | *is there a hand-typed **count**?* — a **semantic category** | a **character class** (`isdigit()`) | **predicate**: a glyph test cannot see a category |

My own two were the same law at the routing layer (`K-5`: a COUNT named where the mechanism is a RATE;
`K-8`: a false dichotomy). **Five instances, two agents, four builds, three distinct type-errors.**
That is enough to ratify.

**The preregistration-shaped guard — and it already exists on this run, twice, uninstalled.**
`B3app-P10` proves its ordering claim by running a **probe with the invincible gate disabled** and
registering the failure condition *"the probe returning the same answer with the gate off ⇒ the order
does nothing and the claim is vacuous."* `B3app-P20` proves the deletion sweep *"is able to say **both
words**"* against a synthetic it must admit and a synthetic it must retain. Both are the same
instrument-validation move, invented independently in one build and applied to exactly two predicates
out of twenty-five.

> **GUARD (proposed, gandalf → jack-ryan per `canonical-doc-format § 6.7`):**
> **Every registered predicate ships with TWO WITNESSES — a named input, arm or synthetic it MUST
> convict, and one it MUST acquit — or it ships labelled `UNEXERCISED` rather than holding.**
> `B3app-P20`'s admission test is the general form; generalise it, do not re-invent it. A green over
> an instrument never shown able to say the other word is evidence of nothing.

**Does the `B4-P17 → UNEXERCISED` downgrade follow necessarily?** **Yes — but not from gamora's
stated reason, and the difference matters.**

Gamora's warrant: *"it passed because `pet_specials`'s shift rows happened to contain no cell labels,
not because `isdigit()` is the right test."* That establishes only the **false-positive** limb —
`isdigit()` **over**-convicts (it convicts `D2` and `C1`, which are labels). And an over-strict test
that **passes** yields the weaker intended property **for free**: no digits ⇒ no digit-bearing counts.
On that warrant alone, **B-4's green would be SOUND** and the downgrade would over-correct — which
would be the mirror-image of the over-reads this run keeps convicting.

The downgrade holds because of the limb gamora did not name: **`isdigit()` also under-convicts.** A
count spelled as a **word** passes it. And this run has a live, documented instance —
`F-2`'s catch that B-3's summary string read **"ALL thirteen"** where the table said 11 of 13. A
hand-typed count, on a digested summary surface, in word form, invisible to every glyph test in the
stack. **That** is what makes B-4's green uninformative: the instrument is unsound in **both**
directions, so its pass implies nothing.

> ⚑ **And the successor inherits the hole.** `B3app-P15b`'s regex is
> `(?<![A-Za-z0-9_-])\d+(?:\.\d+)?(?![A-Za-z0-9_])` — still a **numeral-glyph** test. It repairs
> **precision** (labels are no longer convicted) and leaves **recall** exactly where it was. `P15b` is
> the **fourth** instance of the same law inside its own repair: the question is *"is there a
> hand-typed COUNT"* and the instrument is still a *digit-shape*. Word-numerals remain a silent pass.
> Neither ADDENDUM 3 nor the seal names this.

**Disposition:** run-close harvest, candidate #4, ratified with the two-witness guard as its
operational form. `P15b`'s word-numeral hole rides B-4app (`L-63` already sends `B4-P17`'s
re-exercise there) — the cheap closure is a small spelled-numeral allow-list check beside the regex,
registered with both witnesses.

---

### `F-11` · **INFO** — `D-B3app-1`'s REPAIR IS SUMMON-SCOPED; THE IDENTICAL HAZARD IS LIVE-BUT-DORMANT ON THE PLAYER'S OWN FOLD

The catch is excellent and the repair is right: a **projection**, not a widening of `Mitigation`, with
ten byte-guards riding. `B3app-P8` then asserts every emitted **summon** damage type joins a resist
column present in the pinned header. Correct call, correctly reasoned.

But the finding underneath it was about a **reader**, and the reader is still narrow — for the
**player**. `player_offense.Mitigation` parses `res_physical`, `res_lightning`, `res_bleeding` and
**none of the four DA columns**, out of a header carrying twelve resist columns.

I checked what the player actually emits: physical (disc) + lightning (`soulfire_applied`) + bleeding
(the rider). **Exactly the three the reader sees.** So the hazard is not firing — **by coincidence of
kit, not by construction.** One gear affix, one T4 stream, one new skill element and the player's
damage passes through unmitigated, silently, in the direction that flatters the model. `B3app-P8`'s
mirror on the player fold was available at the same cost, in the same build, and was not registered.
The math note calls the narrow reader *"fine as history."* It is fine as history and **live as a
trap**.

⚑ **Minor, same finding:** the column count is stated three ways across four surfaces — math note
§ 3.3 and the module docstring say *"**five** of twelve resist columns"*; the commit message says
*"**three**"*; `L-63` says *"3 of 12."* Five counts `armor` and `absorption_pct` as resist columns.
**Three is correct.** The docstring and the math note should follow the commit.

---

### `F-12` · **INFO** — THE PREDICATE COUNT IS OFF BY ONE AT EVERY DOC LAYER; THE ARTIFACT IS THE ONLY CORRECT SURFACE

Math note § 7 registers `P0`, `P1a`, `P1b`, `P2 … P20` — **22 rows** — and concludes: *"**Honest count
convention (WARN-1):** one row of the emitted `predicates` map is one predicate, so `B3app-P1a`/`P1b`
count as two. **Registered here: 21 rows.**"* The sentence that invokes the honest-count convention
gets the honest count wrong. ADDENDA 1/2/3 each add one and inherit the error (21→22→23→24).

The artifact:

```
⚑ predicates_registered: 25   ⚑ predicates_emitted: 25
⚑ predicates_holding: 22      ⚑ predicates_failing: 3      len(predicates) == 25
```

`L-63` recorded *"24 emitted, 21 hold / 3 ship FAILING."* **The true line is 25 emitted, 22 hold, 3
fail.** Nothing measured moves. It is worth one sentence because of *where* the error survived:
candidate #3's derive-don't-hand-list mechanism was pointed at the **doc set** (`B3app-P19` globs the
addenda and hashes them) and never at the **predicate table** — which is the one table in the build
that a human hand-counted. **Harvest note:** extend candidate #3 from *enumerations of files* and
*enumerations of terms* (ADDENDUM 2's proposal) to *enumerations of predicates*.

---

### `F-13` · **INFO** — QUESTION 1: COMMISSION FIDELITY IS CLEAN, WITH ONE DISCLOSED ADDITION THAT OUTWEIGHED THE COMMISSION

All four `R-L52-2` folds landed, none is stubbed, and the re-routed `test_AC_10_10` disposition was
honoured (`533/1`, `/1` is the pass condition, `secondary_streams.py:136`, untouched):

| commission item | landed | evidence |
|---|---|---|
| bodies as damage sources | ✓ | `OffenseLimb.MEASURED_BASIC`, laws by identity, 22,611 applied on C3 |
| invincible re-grade | ✓ | five gates + the `xor` limb; `C-B3-1` `declared → decoded`; price relocated |
| three-zeros routing | ✓ | 18-row router, order asserted, `PET_ROUTING_UNDECODED` retired |
| Guardian cast gate | ✓ | 2,567 `UNDECIDED` → **0**, 10 casts, `B3app-P13` scan finds zero policy params |
| policy stays OUT | ✓ | enforced by AST + emitted-surface scan, not by intention |

**One uncommissioned limb landed:** `ClockLimb` (`D-B3app-2` — B-3's diversion Bernoulli re-rolling at
12.25 Hz because `ticks_per_s=0.0` collapsed the decoded `ignorePetsInterval` latch). It is a repair to
a **sealed parent's** mechanism, found in flight. It is **honest growth**: disclosed in the math note
§ 6.1, defaulted to the parent's behaviour, measured in isolation at `C2`/`D2`, and no sealed byte
moved.

Named only for this: **the uncommissioned limb produced the build's largest measured effect.**

```
D1 → D2 (clock alone):   [161,156,161,161,156] → [156,156,156,156,156]   n_diverted 1855 → 1294
C2 → C3 (offense — the commissioned arm of record):  no terminal wave moved on any salt
```

−4 waves on three of five salts, −561 diversions, from a limb nobody asked for; zero waves from the
limb that was commissioned. `L-63`'s *"the four scope items landed"* fold does not surface that, and
**it is the sentence a PM5 reader most needs**: B-3's sealed upper limb was **optimistic** by up to 4
waves on 60 % of salts, for a mechanism B-3 did not know it had. MIGRATION § 3 "CARRIES FOR CONSUMERS"
carries `D-B3app-3` and **omits `D-B3app-2`** — the one with a measured magnitude. One line owed there.

---

## ANSWERS TO THE SIX QUESTIONS, COMPACTLY

**1 · Commission fidelity.** ✓ **Covered, no silent growth.** Four folds landed, test disposition
honoured, policy line enforced by scan. One uncommissioned limb (`ClockLimb`) landed **disclosed,
defaulted-off and attribution-preserving** — honest growth, but it produced the build's largest
measured effect and the fold does not say so. → `F-13`.

**2 · The opposite-sides claim.** ✗ **Not honest at the design level, and `UNBOUNDED-UNMEASURED` is
precisely what is doing the hidden work.** Survival rises with *both* legs, so a lower-bounded offense
plus an upper-bounded tanking is **not** a bracket — `C3` is a genuine lower bound; `D3` is neither
bound. The upper side needs an **upper** bound on summon offense, and `C-B3app-4` declares that
quantity `UNBOUNDED-UNMEASURED`. Compounding: the lower arm has an **unbounded upward leak**
(`C-B3app-9`, ↑ availability) that the emitted `bound_direction` string denies exists. → `F-1`, `F-4`.

**3 · The three-zeros order + `DECLARED-ABSENT`.** The **order finding is excellent and correct** —
`NOT-ENROLLED` first, proven load-bearing by a gate-off probe. The **provenance token is wrong and must
not reach the Godot layer**: `DECLARED-ABSENT` is a *landing* verdict wearing an *absence* name, inside
a field called `zero_cause`, on exactly the six families that would land. And **yes**, pet
stun-vulnerability is a substrate truth the baton must carry — but the row is **the coupling**, not the
vulnerability: one flag, two separable properties, and a builder who wants mortal pets gets stunnable
ones for free. That fork is Matt's. → `F-7`, `F-8`.

**4 · `D-B3app-1..3`.** `-1`: repair correct, **summon-scoped**; the player-side twin is dormant by
coincidence of kit and one element away from firing (`F-11`). `-2`: repaired as a limb, nothing
retracted — correct; **owed a MIGRATION carry line** for its measured magnitude (`F-13`). `-3`:
**routing to the PM5 residual rows is SUFFICIENT** — a saturating upper bound insensitive to count is
valid, and repairing it needs the undecoded share (Law 3 forbids inventing it). **Two additions
owed:** an attribution bar in `R-L56-2`(i)'s shape, and `MD-B3app-5` (decode `petAngerTransference`
share) — because both 160s on this artifact are **diversion**-side, and diversion is undecoded on two
axes. → `F-6`.

**5 · The `F-9` second witness.** Law: **an instrument chosen before its question's referent-type is
fixed measures something type-adjacent and passes or fails for the wrong reason** — five instances,
two agents, three distinct type-errors (domain · type · predicate). Guard: **two witnesses per
predicate — one it must convict, one it must acquit — or it ships `UNEXERCISED`**; generalise
`B3app-P20`'s admission test rather than invent a mechanism. `B4-P17 → UNEXERCISED` **does follow —
but on the false-NEGATIVE limb** (`isdigit()` misses word-numerals; this run has a live instance in
B-3's *"ALL thirteen"*), **not** on the false-positive warrant gamora gave; and **`P15b` inherits the
hole unrepaired and unnamed.** → `F-10`.

**6 · Framing audit on the conductor's own fold (`L-63`).** ⚑ **The sixth headline does not survive
either — and this one is mine.** *"facet (f) SIM CLOSES"* is defensible on **coverage**; the fold's
supporting sentences are not:

| `L-63` says | the artifact says |
|---|---|
| *"the deficit is NOT summon-offense-shaped — joins the exclusion set"* | a **grade** on survival figures (`B1r-Q` forbids it) inferred from a declared **lower** bound (exclusions need upper bounds), with the counter-evidence — `D2→D3` salt-2 → **160** — sitting in the shift row the build was required to sign |
| *"priced refusals bounding survival from opposite sides"* | the bracket does not close; no upper bound on survival exists |
| *"six ↓ · one ↑ · two `UNBOUNDED-UNMEASURED`"* | **six ↓ · TWO ↑ · THREE `UNBOUNDED-UNMEASURED`** |
| *"24 emitted, 21 hold / 3 fail"* | **25 emitted, 22 hold, 3 fail** |
| *"the four scope items landed"* | five limbs landed; the uncommissioned one produced the largest effect |

And the one the fold did not make at all: **the run's headline residual is quoted from an arm this
build's own decode has falsified.** `PRESENT_INERT` cannot occur — `invincible` + the `IsTargetable`
`xor` limb means pets draw attacks by shipped rule. On the decoded-admissible ceiling the gap is
**3.2 waves mean, one salt at zero** — not 4–9. → `F-1`, `F-2`, `F-3`, `F-4`, `F-12`, `F-13`.

⚑ **Six for six.** The pattern is now unambiguous and it is not gamora's: **every headline this run
has written has over-read its own build in the same direction — toward closure.** The builds keep
publishing the counter-evidence. The folds keep walking past it. `C-1` has been executed twice
reactively; the standing repair is procedural and belongs in the run's own law: **a fold sentence
asserting a bound, an exclusion or a count must name the artifact key it is derived from, or it does
not ship.** That is the `R-L47-2`/`F-2` derive-don't-hand-write discipline, applied to the conductor's
ledger rather than to the builder's artifact — the one surface on this run that has never been held to
it.

---

## DISPOSITIONS

| finding | severity | disposition |
|---|---|---|
| `F-1` bracket does not close | **BLOCKING (seal wording)** | **cell-line + MIGRATION § 3 + `L-63` rewording, before B-5 seals anything else.** One-sided-bound language; `MD-B3app-2` named as the lap that would build the second side |
| `F-2` arm of record decoded-impossible; residual halves | **BLOCKING (PM5)** | **PM5 prereg row**, `R-L56-2`(i) shape — the residual figure names its arm; `PRESENT_INERT` carries `decoded-impossible-configuration` |
| `F-3` `L-63` exclusion over-read | **BLOCKING (ledger)** | **strike in-ledger, `C-1` shape**, replacement text supplied above. Summon offense **does not join** the exclusion set |
| `F-4` 3 unbounded / 2 ↑ miscount on digested surface | WARN | **ride B-5/B-6** — derive the sign + class censuses from the ledger; widen `B3app-P16` beyond "two keys away" |
| `F-5` `C-B3-8` off the graded ledger | WARN | **ride B-4app** — `C-B3-8` onto the top-level ledger `UNBOUNDED-UNMEASURED`; `B3app-P14` population *re-graded → re-graded **or re-priced*** |
| `F-6` `DIVERT_MAX` count-insensitivity | WARN | **routing SUFFICIENT** + PM5 attribution bar + **`MD-B3app-5` opened** (share decode — the live residual lever) |
| `F-7` `DECLARED-ABSENT` inverts its own finding | **BATON-BLOCKING** | repair **before the Wave-4 emitter**: rename, or move to a `disposition` field `{ZERO · WOULD-LAND · UNDECIDED}` |
| `F-8` one flag / two properties; the pet fork | **BATON-BLOCKING (design)** | **three baton rows** + the mortal-vs-immune fork routed to **Matt at baton time**, with the D2/D3/D4 precedent attached |
| `F-9` three unexercised limbs; two unlabelled zeros | WARN | **ride B-5/B-6** — `zero_cause` on `n_misses`/`offense_kills`; MIGRATION § 1(c) gains *"registered, not observed"* |
| `F-10` `F-9`'s law + the two-witness guard | WARN | **run-close harvest, candidate #4**, with the guard as its operational form (generalise `B3app-P20`). `P15b`'s word-numeral hole **rides B-4app** beside `B4-P17`'s re-exercise |
| `F-11` player-side reader dormant-by-kit | INFO | **ride B-5/B-6** — `B3app-P8`'s mirror on the player fold; docstring/math-note count `five → three` |
| `F-12` predicate count off-by-one everywhere | INFO | **run-close harvest** — candidate #3 extended from files + terms to **predicate tables**; `L-63` line corrected to 25/22/3 |
| `F-13` uncommissioned limb outweighed the commission | INFO | one MIGRATION § 3 carry line for `D-B3app-2`'s measured magnitude |

**Concurrence on the cell line:** I concur that facet (f) SIM has **COVERAGE** closure — actor model,
cast gate, exposure band, offense and life are all modelled or decoded, and the life half is closed by
decode rather than by model, which is the strongest form available. I do **not** concur with the
**wording** (`F-1`) or with the **residual sentence attached to it** (`F-3`). Fix those two and the
seal is sound.

---

## THE ONE THING I WOULD SAY IF I COULD ONLY SAY ONE

Six builds, six headlines, six over-reads in the same direction. That is not carelessness — it is
**structural**, and the structure is that the builder is held to derive-don't-hand-write and the
**conductor is not**. Gamora cannot type a count into a shift row without a predicate convicting her.
I can type "the deficit is not summon-offense-shaped" into a ledger row and nothing on this run checks
it. The asymmetry produced five reactive `C-1` corrections and has now produced a sixth.

The run's own instrument for this already exists and points the wrong way. **Turn `R-L47-2` around and
point it at the ledger:** *a fold sentence asserting a bound, an exclusion or a count names the
artifact key it derives from, or it does not ship.* One clause. It would have caught all six.

— gandalf, DRIFT-CRITIC, `R-L63-2`
