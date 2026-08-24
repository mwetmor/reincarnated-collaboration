# KC2 MODEL-COMPLETION RUN · **B-1 DRIFT-CRITIC VERDICT** — the player sustain layer (facet (d))

**▶ ROLE: DRIFT-CRITIC — B-1 vs the facet-(d) ruling + charter**
**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** The conductor authored the facet rulings, the charter's
Wave-2 row and the RULING-NOTE § 3 reading that B-1 answers. The framing audit below points at those
as hard as it points at the build; § 6 is where it lands.

**Author:** gandalf (named sub-agent, `DRIFT-CRITIC`), 2026-08-24. **Lane:** DESIGN fidelity only —
jack-ryan's Gate 2 runs in parallel and owns checkpoint shas, test evidence and quarantine greps;
none of that is re-litigated here.
**Judged:** `baf120d8` → `5acf6c92` → `0bdd7704` (engine) · `simulation/kc2/sustain_procs.py` ·
`simulation/math/kc2-mc-b1-player-sustain-2026-08-24.md` + ADDENDUM 1.
**Judged against:** RULING-NOTE (`2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md`) § 1 reframe,
§ 2 facet (d) **BOTH** + the visible-consequence principle, § 3 (as REVISED at L-21) · charter § 0
intent sentence, § 1 target state, § 3 Wave-2 coverage-before-accuracy, ledger L-5 / L-9 / L-21 / L-22.

---

## 0 · TOP-LINE

> ## **PASS — with design findings.**
>
> **Facet (d)'s SIM half is closed and closed honourably.** The premise correction is the most
> valuable thing in the build: a commissioned agent read the commission's own premise sentence, found
> it false, published the correction *above* the code it invalidated, and then published two further
> defects of its own instruments (`D-B1-1` double-count, `D-B1-2` a predicate that was two predicates)
> including one that FAILED as registered. The refusal to re-designate `MONITOR_ON_FLOOR` after seeing
> it shorten survival is the single most important judgement in the artifact — an outcome-selected limb
> would have been undetectable in the record and would have poisoned every downstream grade.
>
> **Facet (d)'s BATON half is NOT closed, and no one owns it.** That is a conductor gap, not a gamora
> gap (F-2). Combined with F-1 — the same function that B-1 repaired ships a *contradicting* stale
> declaration three keys away, test-enforced — the run's coverage gate as written cannot detect either.
>
> **No BLOCK.** Nothing in B-1 needs to be undone. Three findings (F-1, F-2, F-3) are **owed before the
> Wave-4 seal**; two (F-5, F-6) are **owed before the Wave-3 prereg is pinned**, which is the nearer
> deadline.

**Finding severities:** F-1 WARN (wire truth) · F-2 WARN, gate amendment · F-3 WARN, coverage gate ·
F-4 INFO→WARN · F-5 WARN, prereg-blocking · F-6 WARN, prereg-blocking · F-7 WARN, forward exposure.
Conductor self-findings C-1..C-3, § 6.

---

## 1 · FINDINGS

### **F-1 — ⚑ THE SAME `return` DICT SHIPS THE REPAIR AND ITS CONTRADICTION. THE STALE ONE IS TEST-ENFORCED.** (WARN — wire truth; NEW, not a restatement of gamora's)

`run.out_of_model_manifest()` now correctly reports, under `⚑ reclassified_in_model`, that Menhir's
Will, Turtle Shell, Arcane Barrier and the potion are IN MODEL and firing.

Three keys later, **the same return dict** (`run.py:4042`) ships:

```
"devotion_envelope_disclosure": dv.ENVELOPE_DISCLOSURE
```

whose first line reads, verbatim on the wire:

> `ruling: R-KC2-1(d) — no proc mechanism modelled this lap; baton damage is kit-native`

That sentence has been **false as written since I-4** and B-1 has now proved it. The block also carries
`error_bar_classes: piloting_parameters: War Cry cadence, Vire's Might cadence, Ascension usage` — the
*exact three strings* B-1 just amended in `piloting_parameters` to say "MODELLED as greedy on-cooldown,
zero-free-parameter bound." **After B-1 the baton carries two statements about the same three rows, on
the same wire, from the same function, that disagree.**

**Why this is worse than the manifest defect gamora found, not equivalent to it.** `fixture.OUT_OF_MODEL`
was merely stale. This block is stale **and architecturally protected against being noticed**:
`baton_v1_schema.py:405-461` builds a four-link chain — spec § 9.5 → checked-in golden → module constant
→ wire — with a cross-repo byte-compare, an in-repo golden pin, a sha sidecar, and a validator assertion
(`baton_v1_validator.py:369`). Every link works. **Every link tests the text against its own source. Not
one link tests the text against the run.**

> **The generalised drift mechanism, stated for the record:
> a pin proves a text has not drifted. It does not prove the text is still true.**

The apparatus that was supposed to make this class of lie impossible is the apparatus that makes it
invisible. Under the visible-consequence principle a Godot team reading `no proc mechanism modelled this
lap` next to `⚑ reclassified_in_model: menhirs_will IN_MODEL` will not build a runtime; it will file a
ticket. **Owed before the Wave-4 seal:** the § 9.5 block is re-derived or explicitly superseded at the
baton-v2 cut, and the golden's provenance sidecar gains a *run-truth* link, not only a source-text link.
Routing: the block's ownership is star-lord's wire + the spec note's author; the conductor files the ask
with the baton-v2 cut. Discipline candidate (jack-ryan ratifies, gandalf proposes, per
`canonical-doc-format.md` § 6.7): **every declaration that ships on the wire carries an instrument that
tests it against the run, not only against its own source text.**

### **F-2 — FACET (d) WAS RULED *BOTH*. B-1 DELIVERED *SIM* + A SIDECAR + A REQUEST. NOBODY OWNS *BATON*.** (WARN — gate amendment, owed before Wave-4 seal)

What the wire carries about the player's entire sustain layer today is one boolean:
`kc2_run_adapter.py:735` — `counterplay_fold: bool = False`. A Godot **runtime** (not a playback head —
that is the whole reframe) cannot execute a boolean. To play Turtle Shell it needs `triggerType=LowHealth`,
`triggerParam=50.0`, `damageAbsorption=6100`, `cooldown 8.0 s`, **replaces-never-stacks (C-I4-4)**, and the
declared **≤ 1-tick (0.0816 s) actuation latency**. Every one of those exists, pinned and digest-verified,
in `counterplay.Kit` / `pm4g_defensive_actives.csv` sha `0cdfd3af…`. **None of them is exported.**

B-1 delivered exactly what its seam could deliver — the sim repair, a `waves[].counterplay["⚑ B1_sustain_procs"]`
ledger, and REQUEST 1/REQUEST 2 filed to star-lord in `export/MIGRATION.md`. That is correct seam
discipline (ADR-004; `EVENT_TYPES` is a closed countersigned enum and minting a member is not gamora's
call). **The gap is upstream of gamora.** Charter § 1(1) says coverage is "checkable against the facet
table, row by row" — but the facet table has one column, and Wave 4's row says *"baton-v2 cut"*, which is
a **cut obligation, not a content obligation**. If star-lord cuts baton-v2 without landing REQUEST 1,
facet (d) seals with its sim half closed and its baton half open, and the gate as written returns PASS.

**Recommended gate amendment (conductor's, mine to propose):** the coverage gate becomes a **facet × layer
matrix** — for each of (a)–(i), two cells (SIM / LAYER-1-RULE-EXPORT), each with a named owner and a
decidable closure predicate. Facet (d)'s Layer-1 cell owes: the six-layer parameter table, the
replaces-not-stacks semantics, `ACTUATION_LATENCY_TICKS`, the `proc_activation` event family, and the
F-B1-1 pilot-model label. This is the instrument the charter's own coverage-before-accuracy law (§ 3
Wave 2) currently lacks; without it, "coverage closed" means "gamora shipped," which is the KIT-FIDELITY
failure mode the charter names as its own anti-pattern, relocated one seam downstream.

### **F-3 — THE THREE UNBUILDABLE ROWS ARE D-2-CLASS, NOT D-5-CLASS. THEY OWE A LAP, NOT AN ABSENCE ROW.** (WARN — coverage gate)

Two decode outcomes are now precedent in this run, and they are **not** the same shape:

* **D-5 (L-19):** the arena boundary **is not an authored object anywhere in shipped data.** Even success
  is derived geometry. That is a genuine substrate absence — and the conductor still refused to declare it,
  commissioning **D-5b** because a bounded derivation path remained.
* **D-2 (L-17):** 45/58 specials were silent, and the cause was **"the pet bodies were simply never
  visited."** 65/65 slots decoded, **0 UNDECODABLE**. The silence was extraction coverage, never substrate.

**All three of B-1's refusals are the D-2 shape, and gamora priced each one to a single unvisited record:**

| row | named ask | shape |
|---|---|---|
| `ulzaads_decree` | the `…_buff` companion payload record's `defensiveProtection` / `defensiveProtectionModifier` @ dev 20 | **one record**; the artifact's own Maul pair (`tier2_05f_skill.dbr` + `tier2_05f_skill_buff.dbr`) shows exactly where it lives — "the payload record was never visited" |
| `resilience` (non-heal limbs) | full magnitude set of `playerclass09/passive02.dbr` @ rank 3 + its `thresholdDuration` | **one record**, already known present in `pm4g_played_kit.csv` row 319, absent from `pm4g_defensive_actives.csv` entirely |
| `fighting_spirit` | `triggerType`-equivalent field on `Skill_PassiveOnHitBuffSelf` — `HitByEnemy`-class vs `AttackEnemy`-class; second, weaker: the field home of the 30 % | a **template-field** decode, same class as D-2's owner-record catch |

Declaring these absent in the playable baton now would put three rows into the absence registry that
one bounded lap — the direct analogue of D-5b — plausibly closes. Under coverage-before-accuracy that is
premature. **Recommend: commission `D-6` (legolas, player-kit residual decode lap; three named records +
one template field; scope logged in the ledger, not silent growth).** Honorable fallback identical to
Wave 1: UNDECODABLE is a finding, and *then* the absence rows are earned.

**`blocks_playability` judgement — and it is not the obvious one.** gamora measured that
`fighting_spirit`'s decode "buys **the visible activation** — the buff flash a Godot runtime must render,
and the baton row a live player is entitled to — and nothing arithmetic" (`characterOffensiveAbility +108`
is **provably inert**: minimum PTH 149.2 already clears `pthThreshold6=135`, `HIT_CHANCE` already 1.0,
monotone in OA). That pricing is exactly right and the conductor must not misread it as "cheap."

> **Under the visible-consequence principle, `blocks_playability` is TRUE for a row that is
> arithmetically inert but visibly present.** A player whose Fighting Spirit never flashes is playing a
> different character from the one in the reference footage — the arithmetic is identical and the
> *character* is not. Diablo II shipped exactly this failure in reverse with Battle Orders: the number
> was the whole mechanic and the visual was an afterthought, and the skill read as a chore for a decade
> until D2R gave the aura a body. The absence registry therefore needs a **two-column**
> `blocks_playability`: `arithmetic` and `presentation`. A single boolean will collapse
> `fighting_spirit` to FALSE and quietly drop a visible player power out of the playable baton.

### **F-4 — THE LARGEST HP RECOVERIES IN THE FIGHT ARE STILL UNCAUSED ON THE WIRE.** (INFO→WARN — *not* a B-1 defect; a facet-(d) coverage row the conductor's audit never listed)

B-1 made the **discrete** sustain visible: the activation ledger now records every drain site, including
the two that discarded (`run.py` 2701 / 3132), 39 previously-invisible firings per ladder on salt 0. Good,
and it is the right fix at the right seam.

The **continuous** sustain remains a silent scalar. `run.py:3084`:

```python
hp_player = min(hp_player_max, hp_player + regen + adcth)
```

No event row. And by gamora's own § 2.1 this is the *dominant* term — the lift that censored both circuit-
breakers in the first place: **21 % ADCtH plus 129.38 hp/s regen.** The attribution exists inside the sim
(`leech_pool` accumulates against the player's own `damage_dealt` events, `run.py:2303`/`3054`) and is
collapsed to one per-tick number before it reaches the wire.

For Layer 2 (twin test) this is harmless — the `player_hp` track carries it. For Layer 1 it is a rule-export
obligation identical to F-2's: ship the regen rate, the ADCtH percentage, and **the attribution rule that
ADCtH rides the player's own damage-dealt events.**

**And it is a feel finding, not only a data finding.** Regen and leech are two different animals to a
player's hand. Regen is a bar creeping up; leech is HP *snapping* in time with your swings — in D2 that
snap on a Whirlwind barbarian, and in GD on exactly this kind of two-hander build, IS the sustain fantasy,
the thing that makes standing in the pack feel earned rather than granted. A runtime handed one fused
scalar will render a smoothly-rising bar, be arithmetically perfect, and feel like a different build.
**The visible-consequence principle covers this: the consequence is visible, so the rule must reach the
baton.** Scope note: pre-existing, not introduced by B-1 — its presence in this verdict is a **coverage
row the facet-(d) audit should have enumerated and did not** (see C-3).

### **F-5 — F-B1-1's CAVEAT IS PROSE, AND THE THING IT DESCRIBES IS NOW A NAMED CANDIDATE CAUSE OF THE HEADLINE GRADED ROW.** (WARN — owed before the Wave-3 prereg is pinned)

L-22's disposition is correct in all three limbs and I ratify it: Layer 1 carries effect rules only
(the human pilots the potion); Layer 2 replays cast events; sim-side θ is kept and labelled PILOT-MODEL /
NOT-MODEL-TRUTH in the L-5 non-truth bin. **The refusal to invent a piloting policy was the correct
Law-3-adjacent line** and gamora held it.

The hole is in limb (3)'s *form*. L-22 carries the sensitivity "into the PM5 prereg as an interpretive
caveat." B-1's own measurement says a caveat is too weak a container:

> `MONITOR_ON_FLOOR` fires K-3 on the shallow wave-151/153 excursions → holds HP above θ → **the potion
> fires 0 times instead of 2** → K-3 buys ~8,200, K-4 never spent costs ~16,900 → terminal wave **155 → 154**.

**A faithfulness improvement to a decoded rule produced a survival regression that ran entirely through
the pilot model.** That is not noise around the grade; it is a confound **coupled to every remaining
Wave-2 build**. B-2 (control states: stuns change the HP trajectory), B-3 (summons: damage-share changes
it), B-4/B-4r (specials firing: more incoming damage changes it) — each will move potion firings *as a
side effect of the identification*, not as a modelled consequence. And L-21 has already promoted
pilot-model divergence to a **named live candidate** for the 151-156-vs-160 gap the run's headline row
reports.

> A live candidate cause of the headline graded row cannot ship as prose. Under a narrative caveat the
> report card reads *"terminal wave 154; caveat: pilot-model sensitivity"* — from which no reader can
> separate model incompleteness from pilot divergence, which is precisely the question the graded row
> exists to leave open honestly.

**Recommendation (conductor rules; this is a design recommendation, not a ruling):** promote the caveat to
a **named `pilot_divergence` row in the L-9 shared row schema**, `report_only: true` alongside wave-160,
carrying (i) potion firing count, sim vs the recorded referent, and (ii) a **pre-registered θ band** —
sweep θ across the interval its own PREDICATE-F census (17/74) supports and report terminal wave as a
*range under pilot uncertainty* rather than a point. Discipline #72 (value-set sweeps on any in-run value
change) is the existing instrument and arguably already binds: θ is not changing, but its *effective*
operating point is being moved by every build, which is the same exposure.
**Guard on that recommendation, stated so it cannot be misused:** the band is pre-registered before any
cell runs (D4) and it **grades nothing and selects nothing**. A sweep that reports a width is the opposite
of a fit; a sweep that picks a limb is `R-PM4-27 part 3`'s violation wearing a lab coat.

### **F-6 — DOES THE REFERENCE ACTUALLY CARRY POTION *CASTS*, OR ONLY THE *BAR* THEY WERE INFERRED FROM?** (WARN — verification item, owed before the Wave-3 prereg is pinned)

L-22 limb (2) rests the twin test's independence from θ on this sentence: *"Layer 2 twin-test replays
recorded potion CAST EVENTS (facet (g)) directly — θ never enters the acceptance instrument."*

That holds **iff** the reference records potion casts as *observed* events. But θ was **identified against
`pm4h2_player_hp_frac_60fps.npy` — the HP-bar trace** (OBS-H2-5, PREDICATE F 17/74). If the reference's
potion cast times are **inferred from bar discontinuities** rather than observed as casts (icon flash,
animation, count decrement), then "replay the recorded cast events" replays an inference *derived from the
same instrument θ was fitted to*, and Layer 2's independence is asserted, not established.

I do not have evidence either way and I am not asserting the circularity — **I am asserting that the
ruling currently depends on an unverified premise.** One bounded check answers it: are potion casts in the
reference **observed** or **bar-inferred**? If observed, L-22(2) stands as written and this finding closes.
If inferred, L-22(2) needs an amendment before it can carry the acceptance instrument's weight, and the
honest form is a declared tolerance on potion-timing in the twin test rather than an exactness claim.

### **F-7 — D-3's INERTNESS MAP IS A DATED CLAIM ABOUT *THIS CONFIGURATION*, AND WAVE 2 IS ABOUT TO CHANGE THE CONFIGURATION.** (WARN — forward exposure; the Q3 guard)

Q3 asks whether the drift mechanism has other live instances. Triaged across the remaining Wave-2 inputs:

| input | dated-snapshot exposure | verdict |
|---|---|---|
| `pm4g_defensive_actives.csv` (Lap G) | sha-pinned and re-verified at load by `counterplay.verify_substrate()` | **guarded** — a live pin, not a snapshot |
| D-1 / D-2 decode tables | claims about **substrate**, which is frozen game data | **low** — cannot go stale against the sim |
| **D-3 inertness map** | claims about **this fight** — "provably inert in the recording" | **⚑ LIVE EXPOSURE** |
| `pm4g_field_evidence.csv` **negative** results ("field not on this template") | a dated record of a *search*, and B-1 leans on one (`onHitActivationChance`) to declare its second gap | **moderate** — a negative search result is dated by construction; D-5b is the standing precedent |
| C-1 / D-5 | already reclassified in the open, L-14 / L-19 | **handled** |

The D-3 instance is concrete and named in D-3's own return: Fleeing is triple-locked (`NeverFlee` 169/169)
**but `fleeDistance` feeds `StateScared`, so fear stays alive.** B-2 is the control-states build. If B-2
lands player-side fear/terror, **D-3's "Fleeing provably inert" becomes false in the same lap that
consumes it** — a dated inertness claim treated as a standing fact, which is `fixture.OUT_OF_MODEL`'s
mechanism exactly, one wave later.

**Recommended guard (cheap, and it is the general form of what B-1 learned the hard way):**

> **Every claim of the form "X is provably inert in this fight" carries (a) the sim configuration it was
> measured on, by checkpoint sha, and (b) a named re-check trigger — the future build that would falsify
> it.** An inertness claim without a falsifying-build name is a snapshot pretending to be a law.

Applied now, that is three lines on D-3's return and it makes B-2's obligation self-announcing.

---

## 2 · Q1 — FACET-(d) COVERAGE vs THE RULING

**Answer: the SIM half of facet (d) is satisfied. The BATON half is not, and the coverage gate still has
open sustain rows — three of them wrongly shaped as absences (F-3) and one whole layer unowned (F-2).**

The 13-row `fixture.OUT_OF_MODEL` manifest (`fixture.py:234-248`), enumerated against
`sustain_procs.ROW_DISPOSITIONS` (14 entries — the 13 manifest rows plus `ulzaads_decree`, correctly
surfaced as a sub-row of `devotion_procs`):

**(a) Modelled + emitting — 4 rows** (all four are rows the pre-B-1 baton declared ABSENT)

| row | state | emitting? |
|---|---|---|
| `menhirs_will` | **IN_MODEL** — trigger + instant heal + regen + duration + cooldown, evaluation point repaired | heal → `heal_tick` ✓; activation → ledger ✓; **wire event ✗** (REQUEST 1) |
| `devotion_procs` | **PARTIAL** — Turtle Shell ✓, Arcane Barrier ✓, Tip the Scales energy limb ✓; `offensiveLifeLeechMin=132` DECLARED-NOT-FOLDED; Ulzaad's UNBUILDABLE; Maul / Assassin's Mark / Shifting Sands offensive, outside facet (d) | ledger ✓; **wire event ✗** |
| `ascension` | **PARTIAL** — absorb clause ✓; `offensiveTotalDamageModifier +38 %` / `retaliationTotalDamageModifier +39 %` DECLARED-NOT-FOLDED (HALT-4, undecidable buff composition) | ledger ✓; **wire event ✗** |
| `resilience` | **PARTIAL** — healing-increase limb (+24 % below `lifeMonitorPercent=66`) ✓; remainder not decoded | via heal path ✓ |

Every PARTIAL names the limb that did **not** fold. That is the right discipline and it is the half of
manifest truthfulness that is easiest to skip: *a half-folded row reporting as fully modelled is the same
lie in the other direction* — gamora wrote that sentence into the code and then obeyed it.

**(b) Proved inert / dissolved with evidence — 5 rows + 1 limb**
`block` (two-hander; three measured zeroes) · `righteous_fervor` (dissolves — no such skill on the
fixture) · `blessings` (measured zero, both sittings) · `retaliation` (build rule, Physical 1008) ·
`m2_death_rewind` (declared simplification, single life) · **plus `fighting_spirit`'s
`characterOffensiveAbility +108`, proved inert by a real monotonicity argument** (min PTH 149.2 >
`pthThreshold6` 135; `HIT_CHANCE` already 1.0; holds on both crit limbs). These are honest absence-registry
rows and they are earned.

**(c) UNBUILDABLE pending decode — 3** — `fighting_spirit` (trigger DIRECTION) · `ulzaads_decree` (payload
magnitudes) · `resilience` non-heal limbs (full magnitude set + `thresholdDuration`). **Not yet honest
absences — see F-3.** All three are D-2-shaped (unvisited records), not D-5-shaped (nothing authored
anywhere); each is priced at one record or one template field; **D-6 is recommended before any of them
enters the baton's absence registry.** `blocks_playability` needs the two-column form (arithmetic /
presentation) or `fighting_spirit` will be dropped on a false FALSE.

**(d) Charter-excluded, no decode owed — 3** — `defense_structures` (charter § 10) · `mutators` (declared
live confound) · `tributes_score_rewards`.

**On the premise correction itself.** The delivered state — pre-existing layers + one genuine mechanism
repair + activation visibility + manifest truthfulness + three refusals — is a **better** answer to the
facet-(d) ruling than the commissioned one, because the commissioned one was false. The one genuine
mechanism gap it found is the *most* load-bearing one available: the RULING-NOTE § 3 named Menhir's Will
"the build's actual circuit-breaker," and the census shows that in waves 151 and 153 the censored tick was
**the only sub-33 % tick in the wave** — the circuit-breaker was not under-firing, it was **switched off**.
Substrate basis (`lifeMonitorPercent` beside `thresholdDuration` — *"Wait for life to be above threshold
before starting duration timer?"*) is a decode, not a genre inference, and the split rule that keeps the
potion on `H_end` partitions all six layers without leaving anything to taste. I ratify the split rule as
the facet-(d) evaluation-point law.

## 3 · Q2 — VISIBLE-CONSEQUENCE CHECK

**Answer: partially. B-1 made the discrete procs *recorded*; it did not make them *renderable*, and the
largest HP recoveries in the fight remain uncaused on the wire.**

| would a Godot runtime see it? | verdict |
|---|---|
| Menhir's Will heal | **yes** — `heal_tick` (already on the wire) |
| Potion instant + over-time | **yes** — `heal_tick` |
| Turtle Shell / Arcane Barrier / Ascension **activation** | **recorded, not renderable** — `waves[].counterplay["⚑ B1_sustain_procs"]` is a wave-scoped sidecar; `EVENT_TYPES` (`baton_v1_schema.py:76`) has no `proc_activation` member. 39 firings/ladder are now *counted with a timestamp* and still **absent from the event vocabulary** |
| War Cry damage removal | same — sidecar only |
| **regen + ADCtH** | **NO — uncaused HP recovery, `run.py:3084`, no event row at all** (F-4) |

So: would a runtime show the player surviving lethal hits **with cause**? For heals, yes. For **absorbs,
no** — an absorb moves no HP, so on the wire the visible consequence is a damage row that is quietly
*smaller than the model's roll*, with nothing saying "6,100 absorbed by Turtle Shell." And for the
continuous term, no: HP simply rises. **Uncaused HP recovery remains in the record, and it is the dominant
term** — the same 21 % ADCtH + 129.38 hp/s that censored the circuit-breakers.

Two qualifications, both in B-1's favour. (i) gamora's **refusal to mint an `EVENT_TYPES` member** was
correct — ADR-004, the enum is countersigned and star-lord's — and the `pet_spawn` / `dodge_attempt`
precedent (withheld, counted, declared) is the right one to have followed. (ii) The **explicit instruction
that `proc_activation` must NOT join `HP_AFTER_EVENT_TYPES`** is a genuinely good catch carried forward
from `D-I5-2`: an absorb moves no HP and a synthetic `hp_after` on it is a row no consumer can reconcile.

The residual is therefore **not a fidelity lie** — it is an **unowed Layer-1 rule export plus an unlanded
event family**, which is precisely F-2. Under the reframe the Godot side executes the model; it can compute
its own absorb-pool draw *if* the pool rules ship. They do not ship today.

## 4 · Q3 — THE PREMISE CORRECTION'S UPSTREAM LESSON

**The drift mechanism, named:** *a dated DECLARATION was consumed as a living MEASUREMENT.*
`fixture.OUT_OF_MODEL` was written 2026-08-08 as a statement about a **document** (spec § 5.3) and was read
by three downstream consumers as a statement about a **run**: the baton provenance (unconditionally, since
I-4 — four rows declared absent while present and firing), the conductor's own gap audit (RULING-NOTE § 3),
and the charter's Wave-2 commission (§ 3, which cited the 13-row manifest as a *work list*). The declaration
never lied; **it was asked a question it was never built to answer, by three readers who did not check its
date.**

**Forward exposure across the remaining waves: F-7's table.** The critical instance is **D-3's inertness
map**, whose "provably inert in the recording" claims are configuration-scoped and about to meet B-2 (the
`fleeDistance` → `StateScared` limb is the named collision). Second instance: `pm4g_field_evidence.csv`'s
**negative** search results, one of which B-1 already leans on — and D-5b exists precisely because this run
already learned that a negative search result is dated by construction. Substrate decode tables (D-1, D-2)
are **not** exposed: substrate is frozen. `pm4g_defensive_actives.csv` is **not** exposed: it is sha-verified
at load, which is the pattern the rest should copy.

**The guard, recommended:** F-7's two-part rule for inertness claims (checkpoint sha + named falsifying
build). Plus F-1's wire-level companion, which is the deeper one: **a pin proves a text has not drifted; it
does not prove the text is still true.** Both proposed as discipline candidates; jack-ryan ratifies.

## 5 · Q4 — F-B1-1 DISPOSITION FIT

**Answer: L-22 is right in substance and under-specified in form. PM5's grading of a θ-piloted player
against a human-piloted referent is NOT interpretable under a prose caveat — the caveat needs the sharper
form the question proposes.**

Ratified as ruled: (1) Layer 1 carries the potion's decoded effect rules and **no use-policy row** — in a
playable baton the human pilots the potion, and the L-5 `presentation_defaults` / NOT-MODEL-TRUTH bin is
the right home for a pilot stand-in; (2) the twin test replays cast events; (3) sim-side θ kept for grading,
labelled. The `presentation_defaults` generalisation to a named non-truth bin is a good structural move —
it keeps the model layer's provenance enum closed at decoded / video-measured / declared-absent, which is
what keeps Law 3 structural rather than aspirational.

**Where it is under-specified:** F-5. B-1 measured the pilot model as the **dominant explanatory term** in
a terminal-wave shift, every remaining Wave-2 build perturbs the HP trajectory that θ was identified
against, and L-21 has already named pilot divergence a live candidate cause of the run's headline graded
row. Recommendation: a named `pilot_divergence` row in the L-9 shared row schema, `report_only: true`,
plus a pre-registered θ band reported as a width and grading nothing.
**Second hole:** F-6 — limb (2)'s independence from θ rests on the unverified premise that the reference's
potion casts are *observed* rather than *bar-inferred*. One bounded check settles it; it is owed before the
Wave-3 prereg is pinned, because the prereg is where the caveat's form gets frozen.

## 6 · ⚠ THE FRAMING AUDIT TURNS ON THE CONDUCTOR

Three of the seven findings are the conductor's, and the ⚠ SWITCH exists so they get named as loudly as
gamora's.

**C-1 — The conductor consumed a dated declaration as an audit fact, and shipped it into a Matt-ruled
record.** RULING-NOTE § 3 asserted the sustain-asymmetry reading ("every missing player-side layer extends
survival") on the strength of a manifest written sixteen days earlier. The charter's Wave-2 row commissioned
B-1 against that manifest as a work list. The § 3 revision is appended (L-21) and the specific instance is
closed — **but only the instance.** The *habit* is not recorded. Recorded now: **an audit fact that is a
DECLARATION rather than a MEASUREMENT gets a date and a freshness check before it enters a ruling.** The
sub-agent inventories cited `fixture.py:234-248` faithfully; the foreground synthesis never asked *when was
this written, and about what.* That question is one line and it would have caught this before it reached
Matt's eye.

**C-2 — The facet-(d) ruling said BOTH and never said what the BATON half of a sustain rule looks like.**
The visible-consequence principle is stated at the level of *"must reach the baton"* and stops there. B-1
proved that "reach the baton" decomposes into at least three obligations — the **rule parameters** (still
unowed), the **activation event** (requested, unlanded), and the **provenance label** on identified stand-ins
(F-B1-1). Ruling the facets without the layer decomposition is what let a coverage gate return PASS on a
half-crossed seam. F-2's facet × layer matrix is the correction, and it should be applied to (a)–(i) at once,
not to (d) alone — (e), (f) and (g) have the same shape waiting for them.

**C-3 — The facet-(d) audit enumerated the *manifest* and mistook it for the *sustain layer*.** ADCtH and
regen are the two largest sustain terms in the fight and appear nowhere in the 13 rows, because the manifest
is a list of *exclusions*, not a list of *sustain*. The audit inherited the manifest's frame and inherited
its blind spot with it — which is F-4, and it is the same failure as C-1 wearing different clothes: the
conductor let an artifact's own scope define the question's scope. **For facets (e), (f) and (g), enumerate
the mechanism from the player's experience first and reconcile to the artifact second** — not the reverse.
That ordering is the whole reason the visible-consequence principle exists, and the conductor did not apply
it to his own audit.

---

## 7 · DISPOSITION

**PASS — with design findings.** B-1 lands. Nothing is undone.

**Owed before the Wave-3 prereg is pinned (nearer deadline):** F-5 (`pilot_divergence` row + pre-registered
θ band) · F-6 (observed-vs-inferred potion casts).
**Owed before the Wave-4 seal:** F-1 (§ 9.5 block re-derived or superseded; golden gains a run-truth link) ·
F-2 (facet × layer coverage matrix with named owners; facet (d)'s Layer-1 cell filled) · F-3 (D-6 lap, or an
earned declaration of absence with the two-column `blocks_playability`).
**Owed before B-2 opens:** F-7's inertness guard applied to D-3's return (three lines).
**Carried:** F-4 into F-2's Layer-1 cell, with the leech-vs-regen feel note attached.
**Conductor's own:** C-1, C-2, C-3 — C-2 is the one with teeth, and it should be discharged as a charter
amendment (commitment boundary if it changes the target state; a reasoning-boundary ledger entry if it only
adds an instrument to an existing gate).

**Commendation, on the record because the discipline is the point.** gamora corrected a commission's premise
rather than executing it; published `D-B1-1` and `D-B1-2` **above** the code they invalidated, including a
pre-registered predicate recorded FAILED and decomposed into three *narrower* claims rather than widened to
pass; and — the one that matters most — **refused to re-designate `MONITOR_ON_FLOOR` after seeing it shorten
survival**, on the grounds that the limb was designated in a commit containing zero grades. That refusal is
invisible in the artifact if you do not go looking for it, and it is the difference between a model and a
fit.

---

*Filed 2026-08-24 by gandalf (`DRIFT-CRITIC`), KC2 Model-Completion Run Wave 2. Verdict to the conductor;
ledger entry the conductor's. jack-ryan's Gate 2 runs in parallel on the engineering battery.*
