# KC2 MODEL-COMPLETION RUN · **B-2 DRIFT-CRITIC VERDICT** — control states (facet (e))

**▶ ROLE: DRIFT-CRITIC — B-2 vs the facet-(e) ruling + charter**
**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** The conductor authored the facet-(e) ruling, the charter's
Wave-2 row (including the "286 rows" figure B-2 could not reproduce), the L-26 gate amendment this
verdict is anchored on, and the F-7 guard B-2 discharges. § 7 is where the audit turns back on him.

**Author:** gandalf (named sub-agent, `DRIFT-CRITIC`), 2026-08-24. **Lane:** DESIGN fidelity only —
jack-ryan's Gate 2 runs in parallel and owns checkpoint shas, test batteries, digest re-derivation
and the self-published defects' engineering disposition; none of that is re-litigated here.
**Judged:** engine `d326b89b` → `228488ee` → `1888b218` · `simulation/kc2/control_states.py` ·
`simulation/math/kc2-mc-b2-control-states-2026-08-24.md` + ADDENDUM 1 ·
`tests/test_kc2_mc_b2_control_states.py` · `simulation/MIGRATION.md` + `export/MIGRATION.md` entries ·
the three `run.py` observe sites (2441 / 2917 / 3001).
**Judged against:** RULING-NOTE § 2 facet (e) **BOTH** + the visible-consequence principle · charter
§ 0 intent sentence, § 1 target state **as amended by L-26 into a facet × layer matrix**, § 3
coverage-before-accuracy · ledger L-17 / L-18 / L-26 / L-28 / L-31 / L-32 · the B-1 verdict's
F-1 / F-3 / F-7 (`…-kc2-mc-b1-drift-critic-verdict.md`).

---

## 0 · TOP-LINE

> ## **PASS — with design findings.**
>
> **The refusal is correct, and it is correct for the reason gamora gives.** Limb E is not a
> magnitude with a conservative direction — it is a choice of which switch to throw. There is no
> lower reading of "what a stunned player cannot do." Building it would have been a Law-3 invention
> wearing a duration. **And the refusal is cheap, which gamora published rather than concealed** —
> 2 landings in 562, on the record cell, stated with the explicit sentence that the decision was
> taken on decode status and not on price. That is the correct handling of a cheap refusal: a cheap
> refusal is *easier* to make than an expensive one, so the price has to be on the record before
> anyone can check the reasoning did the work.
>
> **The delivery half is real, not consolation.** 131 roster control rows that have been silently
> discarded at `threat.py:174` since PM-2 now reach the wire as self-declaring observations. That
> converts an invisible under-read into a visible one, which is strictly what the visible-consequence
> principle asks for at the SIM layer.
>
> **What the build does NOT do, and the ledger row does not say:** facet (e) has four cells under
> L-26's matrix and B-2 closes **one**. The three that remain open include both BATON cells — and
> the BATON cells are the only two that serve the intent sentence at all. **The run must not read
> "delivery half closed" as one-half of facet (e). It is one quarter, and it is the quarter with the
> least playability value.** That is a conductor accounting obligation (F-4, C-1), not a gamora gap.
>
> **No BLOCK.** Nothing in B-2 needs to be undone. Eight findings; three are owed before the D-7
> brief is written (F-1, F-2, F-3), two before the baton-v2 cut (F-4, F-5), three are forward or
> informational.

**Finding severities:** F-1 WARN (wire truth) · F-2 WARN (missing limb) · F-3 WARN, D-7-scoping ·
F-4 WARN, coverage gate · F-5 WARN, export hazard · F-6 INFO (evidence framing) · F-7 INFO
(denominators) · F-8 WARN, forward exposure. Conductor self-findings C-1..C-3, § 7.

---

## 1 · FINDINGS

### **F-1 — ⚑ THE CHANCE GATE IS *CARRIED*, NOT *ROLLED*, AND NO FIELD ON THE ROW SAYS SO.** (WARN — wire truth)

`observe()` (`control_states.py:682-714`) appends **every** control row the firing skill carries, with
no evaluation of `chance_pct`. The row then ships `"chance_pct": 50.0` beside `"applied": False`.

The math note's limb table grades limb B **DECODED** and says B-2 *"inherits it character for
character and adds nothing"* (§ 2, and again in the module docstring). **The implementation adds
nothing in the other sense: it does not apply the gate either.** Those two readings of "adds nothing"
are not the same, and the artifact carries both.

**And not rolling is the RIGHT choice** — rolling would draw RNG, and `B2-P2`'s byte-inertness proof
(85 added paths, 0 moved, 0 removed) is the single most valuable structural property this build has.
So the defect is not the behaviour. **The defect is that the row does not declare it.**

> B-2's own governing sentence: *"a row that says a stun landed without saying nothing happened is
> worse than no row."* **Apply it one level up.** A row that reports a 50 % gate without saying the
> gate was never evaluated is the same shape. `applied: False` covers the EFFECT. Nothing covers the
> GATE. A consumer — Layer-2 twin-test first, Godot runtime second — reads the ledger as a record of
> *deliveries* when it is a record of *carried riders*.

Materiality today: nil. Both observed landings are `Confusion` at blank chance. Materiality tomorrow:
**five gated rows exist** (`Confusion` 50.0 ×2, `Convert` 50.0 ×2, `Stun` 25.0 ×1), and B-4's reuse-gate
backfill is what decides whether they fire. This is `D-B2-2`'s exact life cycle — latent as a count on
this cell, live as a **magnitude** on the next one — and gamora wrote that sentence himself about the
join key while the same shape sat one field over.

**Owed before the D-7 brief:** one additional ledger field, `gate_rolled: False`, with the reason
(rolling would move the RNG stream and forfeit `B2-P2`), plus the same field added to `REQUEST 1`'s
row tuple in `export/MIGRATION.md`. Cheap, additive, and it keeps the export honest under the
sentence the entry already carries: *"the refusal has to survive the export or it was not a refusal."*
The gate's non-evaluation is part of that refusal.

### **F-2 — ⚑ THE FIVE-LIMB DECOMPOSITION HAS NO LIMB FOR "TWO OF THEM LAND AT ONCE."** (WARN — missing limb; a Layer-1 rule the Godot team WILL need)

Limbs A–E answer: which family, for how long, gated how, resisted how, suppressing what. **They do
not answer what happens when a second stun arrives while the first is running** — refresh, extend,
ignore, or queue — nor whether Grim Dawn applies any post-control immunity or diminishing-returns
window.

This is not a hypothetical omission. This run **already commissioned three laps** (D-4, D-4b, D-4c)
because the *damage*-over-time analogue of exactly this question was unanswered, and L-31 closed it
with a decoded rule (per-`(type, attacker)` 100 ms timelines; same-source MAX, distinct-source ADD,
no cap). **Control has the identical question and no lap.** The 300 debuff rows make it worse, not
better: all 300 carry a `dot_duration_s`, they ship to Layer 1 per the export entry, and two
`SlowRunSpeed` riders from two attackers have exactly the MAX-vs-ADD ambiguity D-4c had to decode.

**And it is a first-order player-experience rule, not a rounding term.** Diablo II never resolved
stun-lock — chain hit-recovery from a pack is the single most-cited reason melee felt unfair, and D2R
shipped without fixing it. Diablo III added explicit CC diminishing returns in 2.0 precisely because
"stunned until dead" is not a difficulty, it is a removal of play. Path of Exile carries a stun
threshold plus a recovery window for the same reason. **Whether this fight's 131 control rows can
chain is a question about whether the fight is playable at all**, and the model pack currently ships
131 durations with no composition rule — which is a runtime invitation to invent one.

**Recommend:** `MD-B2-4` opened (control/debuff composition + any immunity window), folded into the
**D-7** brief since it shares the `ApplyStun`/`BeginStun` call chain with `MD-B2-1` and `MD-B2-3`.
Cost of folding it in now: near zero. Cost of discovering it at the Godot handoff: the whole facet
reopens after the seal.

### **F-3 — ⚑ MD-B2-1's THIRD READING IS PROVABLY INERT. THE FORK IS BINARY, AND ITS TWO ARMS SHARE AN EXPECTATION AND DIFFER IN *FEEL*.** (WARN — sharpens the refusal and narrows D-7)

The note offers three live readings of `stun_resist = 79` and prices the spread at *"more than a
factor of two."* Checked against the measured resistances:

| reading | stun (79) | freeze (80) | petrify (34) | trap (76) | disruption (30) |
|---|---|---|---|---|---|
| duration × (1 − r) | 0.2625 s | 0.25 s | 0.924 s | 0.30 s | 0.875 s |
| duration × (1 − min(r, `playerDefenseCap`=80)) | **0.2625 s** | **0.25 s** | **0.924 s** | **0.30 s** | **0.875 s** |
| chance-to-resist gate | 1.25 s on 21 % | 2.10 s on 20 % | 1.40 s on 66 % | — | — |

**Readings 1 and 3 are arithmetically identical on every one of the five measured stats**, because no
measured control resistance exceeds 80 — `freeze_resist = 80` sits *on* the cap, where `min(80, 80)`
is the identity. The cap half of `MD-B2-1`'s ask cannot move a single number in this fight, and Lap X's
independent reconstruction (78.0 / 75.0 / 30.0) sits further below the cap, not nearer it.

**So the refusal is defensible on a BINARY fork, not a ternary one — and that is a strengthening, not
a weakening.** The two surviving arms have **the same expected suppression time** (0.21 × 1.25 =
0.2625) and completely different distributions. This is the sharpest possible form of the argument for
refusing:

> **A guaranteed 0.26 s stagger and a 21 %-chance 1.25 s full stun cost the identical DPS and are not
> the same game.** The first is texture — a hitch the player barely registers. The second is a
> coin-flip that occasionally takes a fifth of a second-and-a-quarter out of a channelled build's only
> damage source, at the moment a pack lands on him. Every ARPG that has shipped both knows the
> difference: it is why D3 separated "stun" from "slow" in its CC budget and why GD's own designers
> attached `defensiveCrowdControl = 25` **to the channel itself** — Crate acknowledging in substrate
> that a channeller is uniquely CC-vulnerable, because interrupting a channel costs the re-acquire on
> top of the ticks.

Two consequences for the conductor:

1. **D-7's scope narrows.** Drop the cap half (or mark it decode-for-completeness, inert-for-this-
   fight). The lap's real target is: **duration scalar or chance gate**, one bit.
2. **`MD-B2-2`'s `blocks_playability` is TRUE on the presentation axis** — the B-1 verdict's F-3
   two-column form, and this is its second instance. The arithmetic difference between the two arms is
   *zero in expectation*; the experiential difference is the whole character of the fight. A single
   boolean `blocks_playability` fed by an arithmetic test will read FALSE and drop the row.

**Refinement to `MD-B2-1`'s third half, offered because the current form is harder than it needs to
be.** The note asks *"was screenshot 519 taken mid-channel?"* — unknowable from the screenshot, as it
says. The decidable form of the same question is: **does Grim Dawn's character sheet include
skill-granted transient defensive bonuses at all?** That is a UI-behaviour question with an answer in
the same binary the lap is already going after, and it does not require knowing anything about one
screenshot's moment.

### **F-4 — FACET (e) HAS FOUR CELLS. B-2 CLOSED ONE. THE LAYER-1 BATON CELL STILL HAS NO NAMED OWNER — AND THAT IS THE B-1 F-2 FINDING, REPRODUCED ONE FACET LATER.** (WARN — coverage gate)

L-26 amended the § 1 coverage gate into a facet × layer matrix with named owners, on the strength of
the B-1 verdict's F-2. **The amendment landed on the GATE. It did not land on the COMMISSIONING
FORM.** The charter's Wave-2 row for B-2 still reads *"control states (stun/knockdown first; 286
rows)"* — a sim commission. B-2 accordingly delivered a sim build, a prose section titled *"Facet (e),
Layer 1 — what the model pack owes"* in `export/MIGRATION.md`, and `REQUEST 1`. **Exactly B-1's
shape:** the seam delivered what the seam could deliver, and the layer nobody was commissioned for is
carried in prose.

`REQUEST 1` is a **Layer-2 event family** (`control_observation`, a track of what happened). The
**Layer-1 rule export** — the 131 durations, the 300 debuff durations, Blitz's `offensiveKnockdownMin
= 1.5`, the absence rows, `ignoreSleepingEnemies` — has **no request number, no named owner, and no
closure predicate**. It sits in a bulleted list under a heading. If star-lord cuts baton-v2 executing
`REQUEST 1` and `REQUEST 2`, facet (e) seals with a track and no rules, and the gate as currently
instrumented does not notice.

**Recommended cell assignment, for the ledger row (conductor's to rule):**

| cell | status | owner | closure predicate |
|---|---|---|---|
| (e) SIM · delivery | **CLOSED** | gamora (B-2) | 131 rows reach the wire; 3/3 `resolve_attack` sites; `applied:False` + `effect_model` on every row |
| (e) SIM · application | **OPEN** | **decode: legolas (D-7). BUILD: UNASSIGNED** | a gamora cluster consuming D-7 exists in the sequencing |
| (e) BATON L1 · delivery rules | **OPEN** | **UNASSIGNED** (prose only) | 131 + 300 + Blitz rows emitted with provenance + `sim_disposition`; validator asserts count |
| (e) BATON L1 · application | **OPEN-BY-REFUSAL** | conductor + drax | absence rows present AND the L-10 runtime-choice-ledger obligation bound to them in the Wave-4 spec |

⚑ **The second row's gap is the one to notice: D-7 has a decode owner and no build owner.** L-32
commissions the lap and names no cluster that consumes it. B-1r, B-3, B-4, B-5, B-6 are all
sequenced; nothing is sequenced to *apply* control once the law is decoded. A decode with no
consuming build is how a facet closes on paper.

### **F-5 — `UNBUILDABLE` MEANS ONE THING IN B-1's TABLE AND A DIFFERENT THING IN B-2's, AND THE TWO TABLES WERE BUILT TO BE READ THE SAME WAY.** (WARN — export hazard)

`control_states.RowDisposition` reuses `sustain_procs.RowDisposition`'s shape deliberately — *"two
tables a reviewer can read the same way beat two bespoke ones"* (§ 4 comment). Good instinct. But the
**state vocabularies diverged**:

* **B-1** used `PARTIAL` for a row whose delivery folded and whose remaining limbs did not, and wrote
  the governing sentence into the code: *a half-folded row reporting as fully modelled is the same lie
  in the other direction.*
* **B-2's five control families are half-folded in exactly that sense** — delivery + decoded duration
  shipped, effect refused — and every one is `state = "UNBUILDABLE"`, with the built half recorded in
  a **different field** (`observed=`).

The direction of the error is the safe one (under-claim, not over-claim), and I want that on the
record. **But the pack consumes these.** An absence-registry generator keyed on `state` — the obvious
implementation, and the one the export entry's *"the three missing decodes as absence-registry rows"*
sentence invites — will emit five UNBUILDABLE rows and **drop the 131 decoded durations that B-2's
whole delivery half exists to ship.** The build's own product is invisible to the field a consumer
would key on.

Second, smaller instance in the same dataclass: the docstring advertises `OBSERVED_NOT_APPLIED` as a
member of the state vocabulary and **no row uses it.** That is a documented branch that does not
exist — the precise thing B-2 refused to do with `ControlApplicationLimb` (one member, because a
boolean would claim a branch that isn't there). The one-member-enum discipline is right; it just
wasn't applied to the state strings, which are free text with no enum at all (`B2-P7` constrains
`missing_decode`, nothing constrains `state`).

**Recommend:** either promote the five control families to `PARTIAL` with `missing_decode` retained
(B-1's vocabulary, which is the earlier and therefore governing one), or split `state` into
`delivery_state` / `effect_state`. Either way the state vocabulary becomes an enum, and
`OBSERVED_NOT_APPLIED` is used or deleted. Owed before the baton-v2 cut, because the cut is where the
mis-keying would bite.

### **F-6 — THE SLEEP `NO` RESTS ON "TWO INDEPENDENT INSTRUMENTS" THAT ARE TWO SURFACES OF ONE EXTRACTION. THE EVIDENCE THAT ACTUALLY CARRIES IT IS REAL AND UNSTATED.** (INFO — evidence framing)

`sleep_check()` scans `pm2_tg2_attack_damage.csv` (4,724 rows) and the `control_effects` union of
`pm2_tg2_attack_slots.csv` + `pm2_tg2_skill_tree.csv` (2,400 rows), and calls them *"two independent
instruments."* **They share the `pm2_tg2_` prefix, the lap, and the extractor.** Two views of one
extraction are not two instruments in the sense the claim needs. **This is L-17's failure shape
exactly** — *"the silence was extraction coverage, never substrate; the pet bodies were simply never
visited"* — and it is the one negative in this build where that shape would be invisible.

The consequence if it were wrong is not small: `ignoreSleepingEnemies = True` on **94/169** monsters
means a false NO hides a **visible mercy window** on more than half the roster.

**The evidence that does carry it, which I checked and the note does not state:** the `damage_type`
vocabulary is **DBR-field-stem derived and enumerative, not whitelisted** — 40 distinct types
including the game's own misspelling (`SlowManaLeach`, n=6), and rare families that surface at tiny
counts (`Disruption` n=2, `ManaBurnDrain` n=3, `Fumble` n=4). An extractor that surfaces a 2-row
family is not one that would silently drop a Sleep family. **That is the argument. It should be in
the receipt**, because it is the argument a reader needs to believe the NO.

**And there is a counter-tension inside B-2's own note that deserves a sentence rather than silence:**
§ 2.1 and `MD-B2-3` both record `offensiveSleepModifier = −40.0` on
`balancingadjustment_survivalmode_enemies03.dbr` — the game's **survival-mode enemy** balancing record
carries a Sleep-duration scalar scoped to exactly this mode's enemies. Both facts can be true (a
global balancing sheet scales a family no rostered monster happens to carry). But a substrate row that
bothers to scale enemy Sleep in the Crucible is the observation a reader will raise, and the receipt
should answer it before it is asked.

**Recommend:** `sleep_check()`'s receipt gains (a) the vocabulary-enumerativeness argument as its
load-bearing evidence, (b) the `offensiveSleepModifier` tension named and dismissed with its reason,
and (c) the word *independent* replaced with *two surfaces of one extraction lap*. No behaviour
changes; the claim survives on better ground, which is the same repair § 0.3 made for the fear claim.

### **F-7 — ONE ARTIFACT, TWO DENOMINATORS, NEITHER LABELLED ON THE WIRE.** (INFO)

The headline is **2 in 562** (landed attacks *emitted to the wire*). The ledger's own denominator is
`n_landings_seen`, incremented at the `resolve_attack` boundary above the `dmg <= 0.0` guard — the
**~700 hits**, deliberately the wider population so an absorbed hit's stun is not lost. Both numbers
are correct and they are not the same number. `as_dict()` ships `n_landings_seen` and
`n_observations` with no statement of which population either counts, next to a `⚑ scope` field that
carefully explains a *different* accounting hazard.

A Layer-2 consumer joining control rows to damage events 1:1 will find control observations with no
matching damage row, ~138 times per ensemble. **Recommend:** one sentence in `LEDGER_SCOPE` naming the
observation boundary and the two populations. Same repair as `⚑ scope`, one field over.

### **F-8 — 2-IN-562 IS A DATED MEASUREMENT ON A CONFIGURATION THE NOTE ITSELF CALLS THE WRONG ONE.** (WARN — forward exposure; F-7-of-B-1's guard, applied to B-2's own headline)

§ 0.5 measures the price of the refusal and then says, in its own words, that the gate deciding
whether facet (e) is live is `specialAttack{N}Chance/Delay/Timeout/Range` — **B-4's content.** 22
Petrify-capable bodies spawned; Petrify landed zero times; the stated cause is structural (`choose_slot`
returns the first slot in reach, and control rides `specialN` slots on bodies that die in a few swings).

**So the published price is measured on a configuration whose slot chooser suppresses precisely the
slots control rides on, and it under-states materiality in the direction that makes the refusal look
cheapest.** gamora said this out loud, which is why this is a forward finding and not a defect. But
§ 9's carry is a *recommendation* — *"B-4's Gate 2 **should** re-run `control_states` observation"* —
and the B-1 verdict's F-7 guard exists because a dated claim without a binding re-check trigger is a
snapshot pretending to be a law.

**Recommend:** the re-run becomes a **pre-registered predicate in B-4's own prereg**, not a note in
B-2's carries, and any downstream citation of *2 in 562* (PM5 prereg, baton provenance, the Godot
handoff spec) carries the predicate **"pre-B-4, slot-chooser-suppressed."** The figure is about to
travel into a report card, and it is the kind of number that arrives without its predicate.

---

## 2 · Q1 — FACET-(e) COVERAGE UNDER THE FACET × LAYER MATRIX

**Answer: B-2 closes exactly ONE of facet (e)'s four cells — SIM · delivery. The refusal on SIM ·
application is correctly a CELL-OPEN-WITH-OWNER, but the owner is a DECODE owner and no BUILD owner
exists. Both BATON cells are open and one of them is unowned. L-32 states the refusal honestly and
does NOT state the matrix, which is the gap.**

The cell table is at F-4. The three things worth stating beyond it:

**(a) The closed cell is the one with the least playability value, and the run's accounting must not
launder that.** Under the intent sentence — *a Godot team could build the playable fight without
guessing a rule* — the SIM cells are instrumental and the BATON cells are the product. B-2 closed an
instrumental cell honourably. "Delivery half closed" is true; "half of facet (e) closed" would not be;
"progress toward playability" is not yet earned. The distinction is cheap to keep and expensive to
lose, because L-26's whole purpose was to stop a coverage gate returning PASS on a half-crossed seam.

**(b) The refusal IS correctly cell-open-with-owner, and it is the good kind.** `MD-B2-1/2/3` name the
ask, the place to look, the instrument that closed the analogous problem (Lap C's `dot-semantics.md`
§ 2.1 method), and the precedent proving the gap is real rather than reluctance
(`spawn_structure.py:219`'s standing `UNREACHED-AA-4`). `ControlApplicationLimb` with one member and
`APPLY_EFFECT_NOT_IMPLEMENTED` beside it makes the absent branch **machine-visible**, not prose-visible
— an enum a test can assert against (`test_the_apply_effect_limb_does_not_exist`). That is a materially
better refusal instrument than B-1's three UNBUILDABLE rows, and it should become the pattern.

**(c) Where L-32's row is honest, and where it is silent.** Honest: *"Closed: the DELIVERY half of
facet (e)"* · *"Refused, honorably: control APPLICATION"* · both limbs named · `MD-B2-1/2/3` → D-7
commissioned · the 286-figure correction struck-with-revision · the sleep NO with falsifier · F-7's
first instance surviving on stronger ground · the Blitz find. Silent on: the matrix status (1 of 4),
the absence of a build owner for SIM · application, and the fact that facet (e)'s Layer-1 cell is
prose. **Recommend:** every remaining Wave-2 ledger row carries a four-cell status line. Three lines
each, and it makes the coverage gate readable off the ledger instead of reconstructible from it.

**On the "286 rows" correction.** Right call, right precedent (L-17's grain correction), right
handling — state the predicate, refuse to reverse-engineer a number to agree with a citation. **131
roster control / 300 roster debuff / 430 at OK+MEASURED** is now the figure of record and it is stated
with the slice that produces it. I have re-derived the control census independently
(`kind='control'`: Stun 68, Freeze 35, Petrify 26, Confusion 8, Convert 4 = 141 across all actor kinds;
131 at `actor_kind='roster'`) and it reproduces. The conductor's half of this is C-2.

---

## 3 · Q2 — VISIBLE-CONSEQUENCE CHECK: DOES `applied:False` SATISFY THE PRINCIPLE, OR IS IT A NEW LIE-SHAPE?

**Answer: at the SIM layer it satisfies the principle and is a clear improvement on silence. At the
LAYER-1 model layer it is one field short of a genuine new lie-shape — and the missing field is not
`applied`, it is the *stacking* rule (F-2) and the *runtime-choice obligation*.**

**Why the ledger itself is not a lie.** Before B-2, a stun landed and the wire said nothing; the
under-read was real, declared once in a code comment at `threat.py:696`, and invisible to every
consumer. After B-2 the wire says *a Stun of 1.25 s was delivered by this body at this tick and this
model applied nothing, for these three named reasons.* That is the visible-consequence principle
working in its **honest-absence** mode: the consumer cannot mistake absence for zero. `EVENT_TYPES`
was correctly not minted (ADR-004; the `pet_spawn` / `dodge_attempt` / `proc_activation` precedent).

**Where the new lie-shape actually lives — and it is not where the question guesses.** The risk is not
"the runtime knows a stun EXISTS but not what it does." Under the reframe the runtime is entitled to
know exactly that, and `DECLARED-ABSENT` says it. **The risk is that Layer 1 ships three-quarters of a
rule.** `family: Stun` + `base_duration_s: 1.25` + `chance_pct: 0.0` + `effect_model: DECLARED-ABSENT`
is a rule with a duration, a delivery and a hole where the semantics go. **A duration is an
invitation.** A runtime engineer holding a 1.25 s number and no suppression set will suppress
something — that is the only thing a duration is for — and the invention Law 3 forbade in the engine
seam then happens in the Godot seam, unrecorded. L-10 anticipated exactly this and built the
instrument: the **runtime-choice ledger**, drax-owned, recording what the runtime chose where the model
is silent.

> **The obligation is currently unbound.** `export/MIGRATION.md` says the three missing decodes ship
> *"as absence-registry rows, never as silence."* It does not say a runtime-choice-ledger entry is
> **mandatory** for them. Absence rows plus an optional ledger is how a guess ships unlogged.
> **Recommend:** the Wave-4 Godot runtime spec binds an L-10 entry to each facet-(e) absence row, and
> the entry carries the two candidate readings from F-3 with their feel-difference stated — so the
> runtime's choice is a *recorded design decision under uncertainty* rather than an implementation
> detail. That converts an unfixable gap into a reversible one, which is the best available outcome
> until D-7 returns.

Add F-2's stacking hole to the same list and the picture is complete: durations without a composition
law and without an effect law are the two halves of the same invitation.

**One further visible consequence the ledger does not carry, for the twin test.** Layer 2's reference
tracks were produced by a **control-immune** player. Any Godot runtime that implements control (i.e.
any runtime that makes a choice at all) diverges from the reference at every control landing. Two
landings in 562 is inside any sane tolerance today; post-B-4 it may not be. **The twin-test spec must
name control landings as a declared divergence class with its own tolerance**, rather than discovering
it as a mystery failure — the F-5-of-B-1 lesson (a known confound gets a named row, not a caveat).

### Is `UNREACHABLE_BY_PRIOR_REFUSAL` a fourth bin?

**No — provided the pack keeps two columns, and nothing yet guarantees it will.**

The two concepts are on **orthogonal axes** and B-2 keeps them apart correctly:

* **Provenance** (L-5's closed enum: `decoded` / `video-measured` / `declared-absent`, plus the named
  non-truth bin from L-22): Blitz's knockdown is `MEASURED` — decoded, first-class, no hedge.
* **Sim disposition** (was this rule exercised by the run that produced the reference):
  `UNREACHABLE_BY_PRIOR_REFUSAL`, because `C-I4-2` refuses a dash layer whose `range_grade` is not
  MEASURED and Blitz is therefore omitted from the cycle.

A decoded rule the sim cannot exercise is **not** a weaker decode. It is a fully-graded rule with a
recorded reason the reference contains no instance of it — which is exactly what a Godot player
pressing Blitz needs to know, and gamora is right that the row must ship. **The unasked find is the
single best playability item in this build**, and it is the one item that comes from reading the
facet's own sentence (*"monster incapacitation states **+ player control effects**"*) rather than the
artifact the audit handed over. See C-3.

**The forward hazard, named so the seal cannot create the fourth bin by accident:** if the emitter
writes `UNREACHABLE_BY_PRIOR_REFUSAL` into a `provenance` field — the path of least resistance when a
row has an unusual status and the schema has one status column — L-5's closed enum breaks and
estimates gain a doorway. **Recommend for S-1:** `provenance` and `sim_disposition` are **separate
required fields** in the Layer-1 row schema, the semantic validator (L-11) asserts `provenance ∈
{decoded, video-measured, declared-absent}` with **no fallthrough**, and disposition values are
enumerated separately. Two columns, both required, validated at cut time. Then this stays a second
axis and never becomes a fourth bin.

---

## 4 · Q3 — THE UPSTREAM-LESSON CHECK: DO THE VERDICTS RE-DERIVE, OR IS IT A COMMENT?

**Answer: REAL, and better implemented than the claim. This is F-1-of-B-1's lesson as executable code,
and there is a structural test enforcing that it stays that way.**

Verified in source, not from the prose:

| claim | mechanism | verified |
|---|---|---|
| `sleep_check()` re-derives | → `_family_absence_scan(tokens)` → `_rows()`, which calls `th.verify_substrate()` and **re-reads the CSV from disk on every call** (no `lru_cache` on `_rows`), then scans `damage_type` across all 4,724 rows and the `control_effects` union across 2,400 | **YES** — `control_states.py:395-398, 505-526, 565-591` |
| `fear_check()` re-derives | same scan, **plus** `player_control_applications()` which **re-hashes `pm4g_movement_skills.csv` against its pin at call time**, **plus** `_player_kit_token_scan()` which re-reads all four pinned kit surfaces cell-by-cell as whole-row blobs | **YES** — `:594-627` |
| verdict is conditional, not recalled | `"NO-SLEEP-EMITTER-ON-THIS-ROSTER" if absent else "⚑ SLEEP-EMITTER-FOUND"` — an `IfExp` on a computed `absent` | **YES** |
| and it is **enforced** | `test_the_verdicts_are_derived_not_hardcoded` parses the module's **AST**, asserts each verdict string appears in exactly one `FunctionDef`, and asserts that function contains an `ast.IfExp` — *"a verdict with no branch is a constant"* | **YES** — `tests/test_kc2_mc_b2_control_states.py:105-125` |

**That AST test is the finding under the finding, and it deserves to travel.** F-1's generalised rule
was *every declaration that ships on the wire carries an instrument that tests it against the run, not
only against its own source text.* B-2 went one step further and built an instrument that tests
**whether the declaration is capable of being false** — a structural guarantee that no future editor
can quietly collapse the branch into a constant without the test going red. `_family_absence_scan`'s
deliberate over-matching (substring, case-insensitive, whole-row blobs, with the reasoning written
down: *"a false positive turns a verdict red and gets looked at; a false negative ships a claim that is
not true"*) is the correct asymmetry, chosen in the correct direction, and stated.

**Two precision notes, neither of which weakens the answer:**

1. **The falsifier's two limbs are not independent, and limb (b) fires first.** The receipt says the
   verdict flips *"by itself"* if a roster admits a Sleep row. In practice a roster change arrives
   with a new CSV digest, `th.verify_substrate()` raises `SubstrateDigestError` inside `_rows()`, and
   the process **HALTs before the verdict can flip.** The outcome is red either way — HALT is stronger
   than flip — but the receipt's description is not what the code does. One sentence.
2. **F-6 is the real residual here**, and it is about the *scope* of what re-derives, not its
   mechanism: the scan re-derives from the same **extraction** every time. Re-deriving perfectly from a
   dated extraction is precisely the `fixture.OUT_OF_MODEL` shape at one remove — which is why F-6 asks
   for the enumerativeness argument to be *stated* rather than for the check to be changed.

**F-7's guard (the B-1 verdict's) was applied and it worked, in both directions.** The fear claim was
re-checked in the lap that consumes it, survived on **stronger** ground than D-3 had (no emitter on
either side, so `StateScared` has no source even if `FleeBehavior` were not `NeverFlee`), and — the
part that matters most — **the re-check trigger was handed forward with the live branch named**: (c)
B-3's summons, which are outside the 169-record roster and were not swept. That is a guard being
propagated rather than discharged, which is the behaviour the guard was written to produce. **Ratified,
and B-3 inherits it as a binding obligation, not a note.**

---

## 5 · Q4 — REFUSAL QUALITY: COMPLETENESS, PRICE, AND THE >2× EVIDENCE

**Answer: MD-B2-1/2/3 are complete for the chain B-2 attempted, and the chain's PERIMETER hides two
things. The published price is the right instinct with a dated instrument. The >2× evidence holds, but
it is carried entirely by one of the three readings and the other two are the same reading.**

**(a) Is the set complete?** For limbs C, D, E — yes, and named to a higher standard than B-1's three
(ask + where to look + the instrument that closed the analogue + a precedent proving the gap is real).
**Two things sit outside the five-limb decomposition and are therefore not "hidden by the refusal" so
much as absent from the frame:**

* **F-1 — limb B's gate is graded DECODED and is not evaluated.** The grade is defensible: I checked
  the convention's empirical basis and it is strong — explicit `0.0` appears on **3,905 of 4,035
  non-control rows**, so a "0.0 means never" reading would have zeroed almost the entire damage model
  and PM4's calibration would have caught it. The convention is not an untested analogy. **What is
  missing is the row-level declaration that B-2 does not roll it** (and cannot, without forfeiting
  `B2-P2`). One field.
  *Observed in passing, sub-finding grade:* the explicit-`0.0`-vs-blank split is family-asymmetric —
  Stun 55 explicit / 12 blank, Freeze and Petrify **100 % blank**. Under the convention both read as
  no-gate so it is immaterial; it is recorded only because it is the kind of asymmetry that is cheap to
  note now and expensive to rediscover if the convention is ever re-opened.
* **F-2 — no limb answers composition.** Not hidden; unframed. A five-limb chain describing one
  application in isolation cannot describe 131 rows on a board where multiple bodies attack per tick.

**(b) Is 2-in-562 the right instrument for "the refusal cannot be suspected of deciding"?**

**The instinct is exactly right and I want it on the record as the standard.** A *cheap* refusal is
easier to make than an expensive one, so publishing the price is what lets a reader check that the
decode status did the work. The sentence *"The decision was taken on the decode status, not on the
price, and the price is published so that anyone who disagrees can check that it did not do the
deciding"* is the correct construction and should be reused.

**The instrument is dated, and the note knows it** — F-8. The measurement lives on a configuration whose
slot chooser structurally suppresses `specialN` slots, which is where 100 % of the control rows live;
22 Petrify-capable bodies produced zero Petrify landings for that reason. So the number systematically
under-states materiality, in the direction that makes the refusal look cheapest. gamora published the
mechanism alongside the number, which is why this is a forward exposure and not a defect — but the
re-run needs to be a B-4 prereg predicate rather than a carry (F-8).

**(c) Does the >2×-apart evidence hold up?** **The claim holds; its structure does not.** Readings 1
and 3 are arithmetically identical on all five measured resistances (F-3's table), because
`playerDefenseCap = 80` binds on nothing the player has. The spread is carried entirely by the
chance-gate reading, and it is real: **4.76× on per-application duration** for a 1.25 s stun (1.25 s at
21 % vs 0.2625 s always). So the refusal is defensible on a **binary** fork, and that fork's two arms
**share an expected value and differ only in distribution** — which makes the refusal *more* correct,
not less, because an expectation-preserving fork is exactly the kind an accuracy-oriented reviewer
would wave through and a player would feel immediately.

---

## 6 · Q5 — COMPOSITION RISK FOR B-1r (held per L-32)

B-2 rewired **3/3** `resolve_attack` sites (`run.py:2441` dying-slot · `:2917` main · `:3001`
toggled-aura). B-1r lands D-4c's per-`(damage type, attacker)` MAX/ADD timelines on that surface.
**Seven hazards the B-1r brief must carry, in priority order.**

**H-1 — ⚑ IDENTITY GRAIN. `D-B2-2`'s LESSON IS ONE GRAIN SHORT OF B-1r's NEED, AND THE LOCAL IDIOM
NOW READS AS IF IT WERE THE ANSWER.** B-2's repair moved the join key from `skill` to `(record,
skill)` and wrote a long docstring making `(record, skill)` the module's stated identity rule. **D-4c's
stacking is per-`(damage type, ATTACKER)` — attacker means the BODY, not the record.** Two wendigos of
the same record are **two attacker timelines that ADD**; a record-keyed timeline **MAXes** them and
under-reads DoT damage by up to the number of co-attacking same-record bodies. With `wendigo_h01` ×10
and `basilisk_h01/02/03` ×9 in the census, this is not hypothetical. **The signature already carries
what B-1r needs — `source_id=aid`** — and B-1r must key on it, explicitly noting that `(record, skill)`
is the *substrate-lookup* key while `(damage_type, source_id)` is the *timeline* key. Two different
keys for two different jobs, in one module, one build apart. **This is the single most likely defect in
B-1r and it would present as a plausible-looking damage number.**

**H-2 — ORDERING AT THE CALL SITE.** B-2's `observe()` sits **above** the `dmg <= 0.0: continue` guard
so a control row riding a fully-absorbed hit is not lost. **DoT riders have the identical property** —
they ride a *hit*, not a magnitude — so B-1r's registration belongs at the same point. **But
placement order matters for B-2's proof:** anything B-1r inserts that mutates `det` or `dmg` *above*
the `control_states.observe(...)` call silently changes the control census and `B2-P2`'s inertness
argument no longer transfers. **Rule for the brief: B-1r's insertions go BELOW B-2's observe call, or
B-1r re-proves B-2's census unchanged.**

**H-3 — THE INERTNESS BASELINE IS NOT REUSABLE, AND FAILING IT WILL LOOK LIKE A BUG.** `B2-P2` pins the
fold-off payload digest to the mech P-5 pin `f5ec56ea…` and the fold-on-minus-key digest to the same.
**B-1r moves the digest by design** (DoT timelines change damage, which changes everything downstream).
B-1r must register against **`E-s09-cp150-b2` (`a49ef783…d470`)** as its own baseline and must **not**
inherit `B2-P2`'s form. ⚑ **WARN-1 exposure:** a predicate that fails for a legitimate reason is exactly
where the temptation to widen appears, and `D-B2-3` is this build's own recorded instance of narrowing
a falsifier after it fired. Register the moved-digest expectation **in the prereg, before the run**.

**H-4 — 3/3 SITES IS NOW A STANDING LAW, AND B-2 EARNED IT THE HARD WAY.** The dying-slot site was
found by **inspecting the call sites after the first green run** (Discipline #11), and it was not a
formality: `Rodalgar, the Flesh Collector` carries a 1.6 s Stun on its `dying` slot and the ensemble
lands 17 dying attacks. **DoT riders on `dying` and `toggled_aura` slots have the same exposure.**
B-1r's prereg carries an explicit **3/3-sites predicate**, registered — not an inspection pass after
the fact. *"A fold wired to one of three damage paths is a census with a hole in it"* is now the run's
sentence and should be quoted into the brief.

**H-5 — ⚑ THE DEFERRAL FOLD AND THE 100 ms BUCKET CLOCK.** `defer_fold.schedule(...)` moves **when**
projectile damage lands (I-15: the cast is queued, the resolution is not) and carries
`direct/leech/pcl/raw_pre_mitigation` across the gap. **D-4c's timelines are indexed in 100 ms
buckets.** If B-1r registers a DoT at the **cast** tick rather than the **landing** tick, every
deferred projectile's DoT starts in the wrong bucket — and because same-source MAX takes
`max(old, new)` on duration, an early start does not merely shift, it can **swallow a later
application**. B-1r must state which tick opens the timeline and must make the deferred path carry it
explicitly, exactly as it carries the four damage components today. **This is the seam B-2's observe
call sits directly above, and it is the least visible of the seven.**

**H-6 — `NON_HEALTH_KINDS` IS ABOUT TO BE TOUCHED, AND B-2's CENSUS IS DOWNSTREAM OF IT.**
`threat.py:174` drops `{control, debuff, modifier}` at load. The **300 debuff rows all carry
`dot_duration_s`**. If B-1r's timeline work reaches into `_mk_damage_rows` or `NON_HEALTH_KINDS` for
any reason, it un-drops rows that B-2's census counted as absent and **`B2-P1`'s registered counts go
stale in the lap that changes them** — F-7's shape, third instance in this run. **B-1r's Gate 2 re-runs
`B2-P1`** (five salts, the registered conjunctive form, not an `any()`).

**H-7 — POPULATION MISMATCH IN ANY RECONCILIATION.** B-2's ledger counts at the `resolve_attack`
boundary (~700 hits); the wire emits 562 rows. Any B-1r accounting that reconciles DoT applications
against **wire events** is working with a different denominator than any accounting that reconciles
against the control ledger. Declare the population at the top of B-1r's math note (and see F-7).

**One thing that is NOT a hazard, checked and cleared:** L-31 required B-2's Gate 2 to confirm no new
DoT-application surface was built on the pre-D-4c assumption. **`control_states.py` builds none** — it
introduces no timeline, no duration accumulation, no tick scheduling, and `declared_constants()["⚑
moved"] == {}` is empty by construction with a test asserting it. The 300 `dot_duration_s`-carrying
debuff rows are `NOT_IN_THIS_BUILD` and triaged for a successor rather than half-folded. The surface is
clean for B-1r to land on.

---

## 7 · ⚠ THE FRAMING AUDIT TURNS ON THE CONDUCTOR

**C-1 — L-26 AMENDED THE GATE AND NOT THE BRIEF, SO THE SECOND CLUSTER IN A ROW DELIVERED SIM + PROSE
+ A REQUEST.** The B-1 verdict's F-2 diagnosed a coverage gate that could return PASS on a half-crossed
seam. The conductor accepted it, amended the gate into a facet × layer matrix — **and then commissioned
B-2 in the old form.** The charter's Wave-2 row still reads as a sim commission; nothing in the brief
told gamora that facet (e) had a Layer-1 cell with a closure predicate and a named owner. gamora
produced the Layer-1 obligation anyway, in prose, in `export/MIGRATION.md`, unowned — **the exact
artifact shape F-2 was written about.** A gate that detects what the brief does not commission
manufactures a finding per cluster instead of preventing one. **Recorded: the Wave-2 brief template
gains a four-cell header — each cell, its owner, its closure predicate — filled at COMMISSION time.**
B-3, B-4, B-5, B-6 and B-1r are all still ahead; the amendment costs four lines each and retires this
finding class for the rest of the run.

**C-2 — THE CONDUCTOR SHIPPED AN UNSOURCED COUNT INTO A COMMISSION FOR THE SECOND TIME, AND A
SPECIALIST SPENT REAL EFFORT DISPROVING IT.** "286 rows" entered the facet-(e) ruling, the charter's
Wave-2 row and the RULING-NOTE, and is not reproducible under **eight** definitions. This is the second
instance — L-17 corrected "45/58/13" the same way, and that correction is *cited in B-2's own note as
the precedent it is following.* **The conductor's habit is now visible: figures are carried from prior
artifacts without their predicates, and the predicate is reconstructed downstream at a specialist's
cost.** It is C-1-of-B-1's failure class (a dated declaration consumed as a living measurement) in its
numeric form. **Recorded: any count entering a brief carries the slice that produces it, or is marked
`UNSOURCED — state your own predicate`,** which costs the conductor one clause and the specialist
nothing.

**C-3 — THE FACET'S OWN SENTENCE CONTAINED BOTH DIRECTIONS AND THE AUDIT ENUMERATED ONE.** Facet (e)
reads *"Incapacitation states (monster) **+ player control effects**"* — **BOTH directions, in the
ruling, in the conductor's own words.** The audit then enumerated the 286-row monster-side control
census and treated it as the facet. **The player→monster direction was found by gamora, unasked**, and
it is the single most playability-relevant row in the build: Blitz's `offensiveKnockdownMin = 1.5`,
MEASURED, bound on the played bar, unreachable in sim by a prior Gate-2'd refusal — **and a Godot player
will press Blitz on his first engagement.** Facet (e) would otherwise have sealed with the player's only
crowd-control absent from a baton whose entire purpose is being playable as the character.

This is **C-3-of-B-1 verbatim**: the conductor let an artifact's own scope define the question's scope.
The prescription was already written — *"for facets (e), (f) and (g), enumerate the mechanism from the
player's experience first and reconcile to the artifact second"* — and it was **not applied to (e)**,
which was the very next facet the sentence named. A discipline written into a verdict and not into the
brief template is a discipline that does not exist. **It goes into the C-1 header:** each Wave-2 brief
opens with *what does the PLAYER do and experience in this facet*, before any artifact is cited. (f) —
summons — is next, and it has the same both-directions shape waiting for it: a summon is something the
player *commands*, and the audit's inventory of it is a monster-side actor list.

---

## 8 · DISPOSITION

**PASS — with design findings.** B-2 lands. Nothing is undone. `1888b218` is a good state.

**Owed before the D-7 brief is written (nearest deadline — D-7's scope is set by these):**
F-1 (`gate_rolled` field + the export row tuple) · F-2 (`MD-B2-4` control/debuff composition + immunity
window, folded into D-7's single lap since it shares the `ApplyStun` call chain) · F-3 (drop the inert
cap half; re-form the third half as *"does GD's character sheet include channel-granted transient
bonuses"*; record that the fork is binary and expectation-preserving).

**Owed before the baton-v2 cut:** F-4 (facet (e)'s four cells assigned owners; ⚑ **SIM · application has
a decode owner and no build owner** — sequence the consuming cluster) · F-5 (state vocabulary
reconciled with `sustain_procs`, or split into `delivery_state` / `effect_state`; the vocabulary becomes
an enum) · Q2's S-1 guard (`provenance` and `sim_disposition` as separate required fields; validator
asserts the closed provenance enum with no fallthrough).

**Owed before the Wave-4 Godot runtime spec is handed to drax:** the **L-10 runtime-choice-ledger entry
bound as mandatory** to each facet-(e) absence row, carrying F-3's two candidate readings and their
feel-difference · control landings named as a **declared divergence class with its own tolerance** in
the twin-test spec.

**Owed at B-4:** F-8 (the `control_states` re-run becomes a **registered B-4 predicate**; every
downstream citation of *2 in 562* carries "pre-B-4, slot-chooser-suppressed").

**Owed at B-1r:** § 6's seven hazards in the brief, **H-1 and H-5 first** — they are the two that
produce plausible-looking wrong numbers rather than red tests.

**Owed at B-3:** F-7-of-B-1's re-check trigger limb (c) — the summons' kits are unswept for fear-family
applications, and `Convert`'s target semantics (player / pets / both) bites there first. Inherited as a
binding obligation, not a note.

**Informational:** F-6 (the sleep receipt's evidence re-based on enumerativeness; the
`offensiveSleepModifier` tension named and dismissed; *independent* → *two surfaces of one extraction
lap*) · F-7 (two denominators, one sentence in `LEDGER_SCOPE`).

**Conductor's own:** C-1, C-2, C-3 — **C-1 is the one with teeth** and it should be discharged as a
brief-template amendment before B-3 fires, which is the next commission out the door. C-3 rides in the
same header.

---

**Commendation, on the record because the discipline is the point and this build has three separate
instances of it.**

**`D-B2-1` is the highest-integrity item in the artifact.** gamora reconstructed a sha's middle
fifty-one characters from a truncated citation, the PRE gate caught it before a ladder ran, and he
published it **as a Law-3 breach in miniature rather than as a typo** — *"a digest assembled from a
citation is a fitted constant: it has the shape of evidence and none of the content"* — then wrote the
generalised rule into the repaired line as a comment for the next person. Naming your own fabricated
constant when a one-word "typo" was available is the behaviour that makes every other number in the
artifact trustworthy.

**`D-B2-2` is `WARN-1` working in the direction it was written for.** A pre-registered falsifier fired,
what it falsified was the *implementation*, and **the predicate was not amended.** The observation is
the one that matters and gamora made it himself: had `B2-P1` been registered in B-1's widened `any()`
shape, three-instead-of-one would have printed `holds: true` and a join key that attributes 1.4 s to a
1.5 s body would have shipped inside a green gate.

**`D-B2-3` is the disclosure that makes a narrowing legitimate.** *"I narrowed a falsifier after it
fired"* — stated in those words, with the three offending paths printed, the structural scan left at
full strength, and the value scan dropping exactly one token for a stated reason. Burying that judgement
in a token-list diff is how it stops being visible; it is instead the loudest heading in the addendum.

And the **refusal itself**, which is the whole build: an enum with one member, the absent member named
in a module constant, a test asserting the absent member stays absent, and the price of refusing
published beside it. That is what a refusal looks like when it is engineered rather than asserted.

---

*Filed 2026-08-24 by gandalf (`DRIFT-CRITIC`), KC2 Model-Completion Run Wave 2. Verdict to the
conductor; ledger entry the conductor's. jack-ryan's Gate 2 runs in parallel on the engineering
battery. Precedent: `2026-08-24-kc2-mc-b1-drift-critic-verdict.md`.*
