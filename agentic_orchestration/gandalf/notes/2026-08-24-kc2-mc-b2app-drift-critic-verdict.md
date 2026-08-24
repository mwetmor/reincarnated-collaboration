# DRIFT-CRITIC verdict — KC2-MC · **B-2app** (control APPLICATION, facet (e))

**Agent:** gandalf (`DRIFT-CRITIC`) · **Date:** 2026-08-24 · **Run:** KC2 MODEL-COMPLETION, ledger `L-41`
**Judged:** `simulation/kc2/control_application.py` · math note `kc2-mc-b2app-control-application-2026-08-24.md`
+ ADDENDA 1–3 · sibling `E-s09-cp150-b2app` `43a6a48b…`
**Against:** the L-38/L-40 frozen brief (D-7 README + both CSVs + § 2.1 law + ladder + longest-wins +
Confusion/Convert zeros + `R-D7-1` + **J-1…J-10** + F-5 zero-count rows) and the run's intent sentence.
**Parallel:** jack-ryan Gate 2 on the bytes. This verdict judges design-fit, spec-drift and player-consequence only.

---

## 0 · TOP-LINE

**PASS — with one commission I am recommending at first priority, and it is not a defect in the build.**

B-2app is the strongest build of the run on the discipline axis. It answered J-1 in the *type system*
rather than in prose; it converted J-7 from a rule into a representation and showed why the two lanes
share a container; it **decoded** J-6 instead of refusing it and found the dichotomy false; it left
`B2app-P9` **failing as registered** and replaced it in a standalone addendum rather than rewriting it
to pass — which is BLOCK-1's lesson internalised one build after it was administered. Four defects
published alone above their repairs, three of them its own, one inherited. The honest count is the
headline. That is the shape this run asked for.

It also bought the run's biggest **player-experience** result: at the arm of record, a channelling EoR
Warlord sits at `r = 104/105/101` for Stun/Freeze/Trap and **50 of 69 slot-surface control rows deliver
zero buckets while the disc spins.** Effective CC-immunity, emergent from a duration scalar, with no
immunity flag anywhere in the substrate.

**And that finding rests on a load-bearing declared grain, priced in a way that reads as reassurance
and is actually circular.** That is `F-1`, it is the whole of my dissent, and the repair is one lap.

---

## 1 · Q1 — THE CHANNELLING CC-IMMUNITY FINDING

### (a) Does the sim model the gaps honestly?

**The latch is modelled and that is the important half.** `channelling` is implemented as exactly
`not suppresses_channel()` (l. 806/784), and `apply()` reads `chan` *before* inserting the new entry —
so the resist that governs a landing is the one the player held when it hit, and any landed control
drops him from `r = 104` to `r = 79` for whatever lands next. That is a **positive-feedback structure**:
break the channel once and the big three start landing at ×0.1785, which breaks it again. The sim has
the death-spiral shape without anyone naming it as a design intent. Good.

**The refusal is the right shape.** No substrate names re-acquisition latency; it is a player-INPUT
quantity, and inventing it puts a free parameter on the survival axis inside a quarantine that grades
none of it. `REACQUISITION_TICKS = 0` shipped as an explicit constant with "every published channel
cost is a LOWER BOUND" stated makes the refusal auditable. `C-B2app-1` is correct **at the sim layer**.
It does not hollow the finding, because the finding is about the immunity, not about its cost.

**What does risk hollowing it is narrower and sharper — see `F-1`.** With re-acquisition at zero, the
*only* entry into the vulnerable window is a control that lands **while channelling**. At the arm of
record that is **Petrify and nothing else** (`r = 59`, ×0.287; Confusion/Convert are decoded zeros).
Petrify is the fight's **can-opener** — the single mechanism by which control pressure exists at all on
this board. And whether Petrify suppresses the channel is the `STUN_PROXY` **declared** arm of
`D-B2app-G3`, not a decode.

The grain's price is published as *"on the record cell the arm moves NOTHING, because the only families
the record ensemble lands are Confusion and Convert."* True, and **circular**: it moves nothing because
nothing lands, and whether anything ever lands is the thing the grain decides. The pricing is honest
arithmetic in a frame that cannot see the quantity at issue.

Two arms, and they are not close:

| if `MD-B2app-1` resolves… | the fight is |
|---|---|
| Petrify **does** drive a controller state (STUN_PROXY-like) | a **latch fight**: immune while spinning, one Petrify opens the door, the big three pour in, and the player either potions/re-acquires out or spirals |
| Petrify calls no `SetState` (gamora's own named alternative — the `R-D7-3` pattern's second instance) | a fight with **no control dimension at all**: `r` never drops, nothing hard-controls a channelling Warlord, ever |

That is a **binary on the fight's identity**, resolvable by one lap on an existing harness against two
named RVAs with the method already written (`d7_step30/31/32`). Recommending **`D-8` COMMISSIONED**
(legolas, `MD-B2app-1` verbatim) at first priority — not because B-2app got it wrong, but because a
declared grain should not sit under the run's headline design truth when the decode costs one lap.

**Second, smaller gap: the synthetic set has no LATCH probe.** `P5` exercises the ladder (Stun+Petrify
co-live → expiry → fall-through). Nothing forces *one* Petrify landing onto a channelling player and
steps forward to measure re-entry into immunity and the width of the vulnerable window. That is the only
instrument that would show the spiral shape, and it is cheap (`F-6`).

### (b) What the BATON must carry — Layer-1 rows and runtime-choice entries owed

The immunity-plus-windows rhythm is arguably the fight's defining feel. Nine items; the first four are
the ones a Godot team cannot reconstruct and will otherwise get wrong:

1. **`channel_conditional_resistance`** (Layer 1, `decoded`). EoR's `defensiveCrowdControl = +25` applies
   **only while the channel is active**, expanding into exactly {Stun, Freeze, Petrify, Trap} by SUM.
   ⚑ This is a *state-conditional* stat row and the S-1 schema has no conditionality qualifier. Without
   one, a builder bakes +25 as a flat passive and **the fight loses its rhythm entirely** — permanently
   near-immune instead of immune-while-committed. Schema item, not prose.
2. **`control_duration_law` + a derived-consequence note** (Layer 1, `decoded` / `derived`). The law is
   `duration × (1 − r/100)`, clamp ≥ 0, `≤ 0` never inserted, `(int)(s·10)` buckets. The **immunity is
   emergent** — there is no immunity flag. A builder who implements a chance-gate or a clamped minimum
   duration gets a materially different fight while believing he implemented the same rule. Ship the law
   as the rule and `r ≥ 100 ⇒ nothing lands` as a *derived consequence*, explicitly labelled.
3. **`reacquisition_latency` — a NAMED FORK, not a constant** (runtime-choice ledger, `L-10`). See `F-5`.
4. **`control_concurrency_law`** (Layer 1, `decoded`). See Q3 — this is the row that prevents the single
   most likely Godot-side control bug.
5. **`resisted_to_zero` presentation flag** (runtime-choice ledger). 50/69 rows produce a landing with
   zero delivered duration. Does the game show a resist-flash? Grim Dawn does. **A telegraphed slam that
   produces no visible reaction reads as a broken game**, and this is the *most common* control event on
   this board. The baton cannot decide it; it must FLAG it.
6. **`items_and_instant_casts_permitted_through_control`** (Layer 1, `decoded`). Potions work through a
   stun. `S-5` names it as counter-intuitive; the baton must too, or intuition wins.
7. **`suppression_matrix` as a Layer-1 table with `IMPL` distinctness preserved.** gamora kept `IMPL`
   on the receipt (`n_requests_honoured_via_impl`); the emitter must not flatten it. "A trapped player
   casts through a *different state*" is a presentation fact a boolean destroys.
8. **`petrify_is_the_can_opener`** (Layer 1, `derived`, flagged `DECLARED-PROXY (MD-B2app-1)` until D-8).
9. **`blitz_knockdown`** — the player's own control, `UNREACHABLE_BY_PRIOR_REFUSAL`. Already routed at
   `L-32`; restated because it is a facet-(e) Layer-1 row and belongs in this list.

### (c) F-5's `pilot_divergence` row at PM5 — yes, and it is an attribution trap

If the recorded pilot's survival to wave 160 leans on channel uptime, then **`pilot_divergence` is not
purely a skill/behaviour residual — part of it is mechanical.** A sim whose EoR uptime is materially
lower than the pilot's eats controls the pilot never ate, and the resulting survival gap will be read
as a *sustain* shortfall when it is a *control-exposure* shortfall. Those two diagnoses point at
different repairs.

**PM5 prereg row owed (graded by nothing, reported always):** channel-uptime fraction, and
`n_control_landings_while_channelling` vs `while_not`, for sim and — where the video supports it —
pilot. Joins the `F-6` semantic-shift ledger at W3 prereg. `F-3`.

---

## 2 · Q2 — `RESISTED-TO-ZERO` AS A FIRST-CLASS DISPOSITION

**Right shape, and it is cleanly separated from both existing axes.** Checked against `L-34`/Q2's
`provenance` ÷ `sim_disposition` split, `EffectModel` is a **third** axis — a *per-event outcome class*,
not a knowledge grade and not a modelling status. A row carries all three plus the layer:
`provenance: decoded` · `layer: SIM` · `sim_disposition: IN_MODEL` · `effect_model: RESISTED-TO-ZERO`.
The build already ships `"layer": "SIM"` on every row (l. 911), which is `F-4`-of-B-1r anticipated
rather than deferred. Credit where due.

**Does the enum need the layer axis MORE urgently? Yes — and the reason has changed class.** At `L-37`
the layer qualifier was bookkeeping: `DECLARED-NOT-FOLDED` has no Layer-1 meaning. `RESISTED-TO-ZERO`
is the first disposition whose Layer-1 meaning is **the inverse of its SIM meaning**:

- **SIM:** nothing was inserted; no state; contributes nothing; safe to treat as absence.
- **Layer 1 (Godot runtime):** something *did* happen — the enemy telegraphed, cast, connected, and the
  correct presentation is impact + resist feedback + zero effect.

A Godot dev reading a SIM-flavoured `RESISTED-TO-ZERO` will implement it as an absence and delete the
run's biggest finding from the playable artifact. **The layer qualifier is now the field that prevents
the headline result from being mis-transcribed.** Escalating the S-1 item from schema-nicety to
**required-before-the-Wave-4-emitter**, joining B-2's `F-5` vocabulary harmonisation.

⚑ **And a second schema requirement falls out: the baton needs THREE distinguishable zeros, not one.**
`GATE-FAILED` (rolled and missed — no cast connection), `DECODED-ZERO` (the engine has no consumer —
the effect is real but inert by design), `RESISTED-TO-ZERO` (connected and resisted). Three different
presentations. A single "zero" bucket at Layer 1 collapses them and the fight reads flat. `F-2`.

---

## 3 · Q3 — J-6: PETRIFY BURNS THE STUN TIMER

**The decode is right and the consequence is correctly implemented.** `tick()` (l. 963–999) advances
every family's accumulator every tick and retires buckets regardless of which family is *acting*; only
`active_family` is exclusive. `Stop/StartInvoluntaryEffect` touch controller state only. So overlapping
controls **eat each other's wall-time**: 2 s of petrify inside a 3 s stun costs the attacker the whole
2 s. A player petrified during a stun is **not** stunned again afterward for the full remainder.

**Is it correctly carried into the shift ledger? No — one row is missing.** `S-1…S-7` cover suppression
(S-2/3/4, ↓), items (S-5, ↑), semantics (S-1/S-6), and the arm (S-7, ↑). Nothing names the
concurrency law. It is technically subsumed — the B-2 incumbent applied nothing, so *vs the incumbent*
it hides inside S-2/3/4 — but the ledger's stated standard is *"every shift with its direction and
mechanism,"* and this one's sign is **opposite** to S-2/3/4 (overlapping controls are cheaper than
sequential ones ⇒ ↑ survival vs a queueing model). The ledger's entire value is showing both
directions. **`S-8` owed as an addendum row.** WARN-class, no code, no digest. `F-4`.

**Baton row owed — and it is high-value.** Godot/ARPG implementations queue or refresh CC by default;
almost nobody implements concurrent independent timelines with an exclusive presentation state. A dev
who writes *"stun 1.2 s, then petrify 2.0 s, total 3.2 s locked out"* ships a fight roughly a third
more punishing than the real one, and it will feel unfair in exactly the way ARPG players notice.

> **Layer-1 row `control_concurrency_law`** (`decoded`, four clauses): (1) every family runs its own
> independent 100 ms-bucket timeline, all burning concurrently; (2) exactly one family *acts* at a time,
> chosen by the priority ladder Immobilize > Petrify > Freeze > Trap > Sleep > Stun > Knockdown > TakeHit,
> first-hit-wins; (3) the ladder is re-evaluated every update — nothing is discarded, nothing is
> suspended; (4) same-family landings are **longest-wins over REMAINING**, computed by list extension,
> with **no refresh**.

⚑ **Plus a runtime-choice entry:** when the acting family's list empties and a lower-priority family is
still live, the player transitions Petrify → Stun **with no incoming hit**. Godot's VFX layer must not
fire an impact effect on that transition. That is a presentation ruling the baton cannot make and must
surface.

---

## 4 · Q4 — REFUSAL AUDIT, `C-B2app-1..5`

| # | verdict | note |
|---|---|---|
| `C-B2app-1` re-acquisition = 0 | **correct at SIM, UNDER-refused at BATON** | `F-5` below |
| `C-B2app-2` `DefenseAttributeDefenseCap_All` unwalked | **correct** | closed by measurement (`P7`), price proven zero |
| `C-B2app-3` `R-D7-1` `n × cap` unresolved | **correct** | inert *at these values*, measured. Baton must say `assumption, inert on this board` — never `decoded` |
| `C-B2app-4` Blitz stays `UNREACHABLE_BY_PRIOR_REFUSAL` | **correct, and exemplary** | the sim can't reach it; the RULE still ships to Layer 1. This is the two-layer baton earning its keep |
| `C-B2app-5` WARN-2 Disruption → B-4 | **correct routing** | not over-refused; 2/133 named |

**No over-refusal starves the baton — with one exception of labelling, not modelling.**

**`F-5` — `C-B2app-1` is under-refused one layer up.** `REACQUISITION_TICKS = 0` is honest at the sim
layer and **misleading at Layer 1**, where a constant `0` reads as a decoded zero. The referent is
*client input*: Grim Dawn's actual EoR is a hold-to-channel skill, so a real player's re-acquisition may
genuinely be ~0 ticks (button still held) or a full re-press — and **the binary cannot see input**, which
is precisely why the refusal was right. The baton must inherit the refusal **as a named fork, not as
silence**:

> **Runtime-choice ledger entry `RC-reacquisition`.** Arm 1: hold-to-channel, the disc resumes the tick
> the control expires (≈ the sim's lower bound). Arm 2: explicit re-press, N ticks of dead time.
> **Consequence:** Arm 2 compounds with the Q1 latch — every landed control costs its duration *plus*
> the re-press window at `r = 79`, which is a second control landing at full length. Arm 1 is
> forgiving; Arm 2 is a spiral. **This is the highest-leverage feel fork in the whole facet and a
> Godot session will otherwise decide it by accident.** Matt-surface at Wave 4.

---

## 5 · Q5 — COVERAGE MATRIX (L-26 gate, honest counts per L-37's trimming)

**Facet (e) — control**

| cell | status | owner |
|---|---|---|
| SIM · delivery | **CLOSED** (B-2) | ✅ |
| SIM · application | **PARTIAL** — CLOSED for Stun/Knockdown/Sleep/Trap/Immobilize/Confusion/Convert; **Freeze + Petrify carry a DECLARED suppression grain** (`MD-B2app-1`, 59/131 roster rows) | B-2app ▲ · closes on `D-8` |
| BATON · Layer 1 | **OPEN** | Wave-4 emitter |
| BATON · Layer 2 | **OPEN** | Wave-4 emitter |

⚑ **1 of 4 CLOSED, 1 PARTIAL, 2 OPEN.** Not 2/4. `L-37` trimmed `L-36`'s optimism and the same
discipline applies to my own build's headline (`F-7`).

**Facet (d)** — unchanged at **1/4**. SIM·sustain closed; **SIM·offense/armour still OPEN with NO OWNER**
(Ascension ±38/39 %, FS +95 %, Tip-the-Scales leech, Ulzaad `+190` armour at the intake seam, Ulzaad
offensive/retaliation limbs). ⚑ **Third consecutive verdict in which I record an unowned cell and assign
nobody.** Conductor item, named in § 8.

**Facet (i)** — unchanged at **2/5**. B-2app does not touch it; the fleeing re-check rides B-3.

**What remains for Wave 4's emitter on facet (e), exactly ten items:** (1) the layer-qualified
disposition field (`F-4`-of-B-1r, now *required*); (2) three distinguishable zeros (`F-2`); (3) a
state-conditionality qualifier for EoR's `+25` (Q1b/1); (4) the `control_concurrency_law` row (Q3);
(5) the suppression matrix as a Layer-1 table with `IMPL` distinctness preserved; (6) `RC-reacquisition`
as a named fork (`F-5`); (7) the `RESISTED-TO-ZERO` presentation flag; (8) Blitz's rule row; (9) the
`DECLARED-PROXY` basis on Freeze/Petrify rows, or its retirement if `D-8` fires; (10) the derived-
consequence note on emergent immunity at `r ≥ 100`.

---

## 6 · Q6 — THE **K-MAP** FOR B-3 (SUMMONS)

Eleven hazards, priority order. Each names a *mechanism* and a *measurement*, per the standard that made
the J-map work.

**K-1 — ⚑ ACTOR-ID STABILITY IS WHAT MAKES A SUMMON A DISTINCT ATTACKER, AND IT IS UNVERIFIED.** B-1r
keyed DoT timelines on actor id with the silent fallback **removed** (H-1, LIVE). A summon spawned
mid-wave takes a fresh id ⇒ a fresh **additive** timeline. So a summoner spawning N adds is an N-fold
multiplier on distinct-source ADD. **Answer before building: are summon ids unique for the run's whole
life, and are they RECYCLED on death?** If recycled, a dead summon's timeline is fed by its successor —
MAXing where it should ADD, or ADDing into a stale key. Pre-register an id-uniqueness census over the
full ensemble. H-1 pointed forward; most likely defect.

**K-2 — ⚑ THE SUPPRESSION MATRIX IS `ControllerPlayer` AND A SUMMON IS NOT A PLAYER. B-2app's DECODED
ZEROS INVERT ON A NON-PLAYER TARGET.** D-7 § 3.4: Confusion/Fear/Taunt are `ret` stubs on
`ControllerPlayer` — but **Monster OVERRIDES them** (`CombatExertInfluenceConfusion@Monster 0x002d9670`
is a real body). So the families that are decoded zeros on the player are decoded **non-zeros** on a
monster, and possibly on a pet. **B-3 must decode which controller class a player pet uses and must NOT
inherit B-2app's zeros.** Highest-value K-row; it is F-7's "re-derive at call time" as code, and it
retro-lights B-2's Fleeing-inert verdict from the other side.

**K-3 — TAUNT / THREAT TRANSFER, THE HALF OF F-7 NOBODY HAS NAMED.** Taunt (`+0x3cc`) is a real body on
Monster. Summons pull threat and the sim has `threat.py`. If any summon emits taunt or threat-transfer,
monster target selection moves, which moves incoming player damage, which is survival-coupled and lands
inside `B1r-Q`. Search both kits; **publish the negative with the search recorded** if absent.

**K-4 — A SUMMON THAT DIES MID-TIMELINE IS A NEW RETIREMENT SHAPE.** B-1r's timelines retire
monotonically and drop in-flight at wave end (I-15 A3, inherited-not-re-argued). Does a summon's DoT on
a monster keep burning after the summoner dies? Genre-standard says yes; **genre-standard is not a
decode.** And symmetrically: **if B-3 models summons as damage SOURCES but not as damage SINKS it
manufactures free damage.** First-class on both sides, or the asymmetry is declared with its price.

**K-5 — ⚑ SUMMONS-AS-SINKS CHANGE THE PLAYER'S CONTROL EXPOSURE — Q1's finding one lane over.** Every
monster attacking a pet is not attacking the player; the channel breaks less; the CC-immunity latch
holds longer. This is a **live facet-(e) ↔ B-3 coupling** of exactly the `J-4` shape, except `J-4`
measured inert and this one will not. **B-3 publishes `n_control_landings_on_player` PRE and POST the
summon fold**, inside `B1r-Q`.

**K-6 — THE SPAWN SEAM: A SUMMON IS A SPAWN THAT IS NOT IN THE WAVE MANIFEST.** `spawn_structure.py`,
`arrival.py`, `arrival_order.py`, `deferred_arrival.py` all key off the manifest. Does wave-advance count
summons as roster? **If yes**, a summoner outspawning the player's clear rate extends the wave without
bound; **if no**, summons orphan across the wave boundary. Neither is safe to assume, and either can
silently move the **terminal wave** — which is PM5's graded row. Decode or declare.

**K-7 — THE DENOMINATOR MOVES A THIRD TIME (`J-9`'s shape).** Every price in this run is denominated
over "169 roster bodies" / "131 control rows" / "n landings in 562". Summons sit outside the roster
sweep. **Pre-register: B-3 re-derives every denominator it touches on its own basis and cites nothing
from B-2app's or B-2's.** Dated-claim discipline, third firing.

**K-8 — DOES A SUMMON INHERIT THE SUMMONER'S MODIFIER POOL?** `GetTotalDurationModifierType` sums entries
on **a** Character; a pet is its own Character. `offensiveStunModifier −40 %` (Gladiator) and `+25 %`
(Ultimate solo) are difficulty-globals. Giving a summon the player's pool by inheritance is an invention;
giving it nothing is a different invention. **Decode the pet's attribute-collection path, or run both
arms with one graded — the `D-B2app-G3` pattern, which worked.**

**K-9 — THE DIGESTED-SURFACE PROSE DEFECT AND THE `C-B1r-3` SCHEMA DECISION, RESTATED LOUDER.** I
recommended pulling `C-B1r-3` forward *before* B-2app at `J-10`; it was not done, and B-2app escaped only
because jack-ryan's BLOCK-1 ruling established docstrings are outside the digested surface. B-3 will want
`SUMMON_BASIS`, `PET_LADDER_BASIS`. **Pull the `_surface()` filter decision forward before B-3 or accept
the fifth instance.**

**K-10 — ⚑ PREDICATE INDEPENDENCE, AS A STANDING PREREG CLAUSE.** `D-B2app-4` is the run's most
transferable lesson: `B2app-P12` reported 60/60 against a matrix it was misreading, because its
expectation was built from *the same collapse the implementation performed.* B-3's predicates about
summon behaviour will be written against gamora's own summon abstraction. **Pre-register that every B-3
predicate derives its expectation from a PINNED ARTIFACT in that artifact's own vocabulary** — the decode
CSV, the roster CSV, the video — never from the implementation's abstraction. Routing this to jack-ryan
for discipline ratification alongside the `F-8`-of-B-1r prose rule (`F-8`, below).

**K-11 — ⚑ DOES RELEASING A PET BREAK THE CHANNEL? IF SO, THE PLAYER CAN DROP HIS OWN CC-IMMUNITY.**
`RequestReleasePet` is `PERMITTED` in all five *control* states — but the CSV is a diff against **Idle**,
and `ControllerPlayerStateUseSkill`'s `Request*` row is **not in it**. Per Q1, exiting the channel costs
the `+25` and puts the big three back in play at ×0.1785. So "should I summon?" may be a real
risk/reward decision the player makes mid-fight — **or it may be free.** The ask is one more column of
the census that already produced the CSV: diff `ControllerPlayerStateUseSkill`'s 83 slots against Idle.
Cheap, and it is a *player-agency* mechanic, which is exactly the class of thing the baton exists to
carry.

---

## 7 · FINDINGS

| # | sev | finding | disposition |
|---|---|---|---|
| **F-1** | **WARN, design-critical** | `MD-B2app-1`'s `STUN_PROXY` grain is **load-bearing**: Petrify is the only hard-control family reaching a channelling player, i.e. the sole causal entry into the fight's control dimension. Its price — *"moves nothing on the record cell"* — is **circular** (it moves nothing because nothing lands, and the grain decides whether anything lands). Binary on the fight's identity | ⚑ **`D-8` COMMISSIONED** (legolas; `MD-B2app-1` verbatim, RVAs `0x0005b020` / `0x0005b150`, method = `d7_step30/31/32`). Conductor call, veto-open. Facet (e) SIM·application closes on its return |
| **F-2** | **WARN, baton-bound** | `RESISTED-TO-ZERO` is right-shaped as a third axis (per-event outcome ⟂ provenance ⟂ sim_disposition) — but it is the first disposition whose **Layer-1 meaning inverts its SIM meaning**, and the baton needs **three distinguishable zeros** (`GATE-FAILED` / `DECODED-ZERO` / `RESISTED-TO-ZERO`), not one | S-1 layer-axis item **escalated from schema-nicety to required-before-Wave-4-emitter**; joins B-2 `F-5` vocabulary harmonisation |
| **F-3** | **WARN** | `pilot_divergence` at PM5 is partly **mechanical**, not purely behavioural: channel uptime governs control exposure. Mis-attribution risk — a control-exposure gap read as a sustain gap | PM5 prereg row (graded by nothing): channel-uptime fraction + `n_control_landings_while_channelling` vs `while_not`, sim and pilot. Joins the `F-6` semantic-shift ledger at W3 |
| **F-4** | WARN | The **J-6 concurrency consequence has no shift-ledger row.** Its sign is ↑ survival — *opposite* to S-2/3/4 — and the ledger's value is showing both directions | **`S-8` owed** as an addendum row. No code, no digest |
| **F-5** | **WARN, baton-bound** | `C-B2app-1` correct at SIM, **under-refused at Layer 1**: `REACQUISITION_TICKS = 0` reads as a decoded zero where the referent is *client input* the binary cannot see | Ship as **`RC-reacquisition` NAMED FORK** in the runtime-choice ledger, both arms with consequences; Matt-surface at Wave 4. Highest-leverage feel fork in the facet |
| **F-6** | INFO | The synthetic set has **no latch probe** — nothing forces one Petrify onto a channelling player and steps forward to measure the vulnerable window's width and re-entry into immunity | Cheap addition; recommend it ride `D-8`'s return build rather than a re-submission now |
| **F-7** | INFO | Facet (e) honest count is **1 CLOSED / 1 PARTIAL / 2 OPEN**, not 2/4 | Matrix corrected in § 5; ledger row must carry it (§ 8, C-1) |
| **F-8** | INFO, positive → discipline | `D-B2app-4` (a predicate acquitting incorrect code because its expectation came from the implementation's own collapse) is the run's most transferable lesson, and it was found by a test asserting the **decode's sentence**, not the matrix cell | **Route to jack-ryan for discipline ratification** alongside the B-1r `F-8` prose-in-digested-surfaces candidate: *predicate expectations derive from a pinned artifact in that artifact's own vocabulary.* Carried into B-3 as `K-10` |

**Also noted, no action:** the inherited `MD-B2app-1` errata against D-7 § 8 should ride the gate fold as
a correction to the decode README (evidence CSVs unaffected) — already routed at `L-41`, restated so it
is not lost. And `B2app-P9` left failing as registered, with P16/P17 pre-registered before the repair
ran, is the correct handling and the clearest evidence in the run that BLOCK-1's lesson took.

---

## 8 · ⚠ THE FRAMING AUDIT TURNS ON THE CONDUCTOR

**C-1 — the facet cell line is missing from `L-41`. Third instance, and it is now a pattern in my own
hand.** I recommended it at B-2/Q1(c), recorded the failure at B-1r/C-1 (*"every Wave-2 ledger row
carries its facet's cell line — three lines per row"*), and `L-41` again narrates a build without them.
The repair is mechanical and I keep not making it. **Amending `L-41` this commit to carry `facet (e) =
1 CLOSED / 1 PARTIAL / 2 OPEN`, and the convention binds every remaining Wave-2 row.**

**C-2 — `L-41` states the headline at full confidence and its dependency three clauses later at lower
confidence.** The row says *"design truth the run just bought: EoR channelling is effective CC-immunity
to the big three families on this board"* — true — and separately records `D-B2app-G3` as a declared
grain. **It does not say in the same sentence that the finding's causal complement (that control ever
lands at all) rests on that grain.** That is the laundering shape at the ledger layer, and it is the
third time I have named this failure in my own text. **Repair: the `L-41` amendment carries the
dependency in the same sentence as the finding, and `D-8` is commissioned in the same row.**

**C-3 — facet (d)'s SIM·offense/armour cell has now been recorded OPEN with NO OWNER in three
consecutive verdicts** (B-1r `Q5`, and again here). Recording an unowned cell three times is not
bookkeeping, it is deferral wearing bookkeeping's clothes. **Owner assignment owed at the next
sequencing decision, or the cell gets an explicit declared-out-of-scope ruling with its price.** I will
not record it a fourth time without one.

**C-4 — what worked, and why.** The J-map's standard (name a *mechanism* and a *measurement*, never a
concern) held: J-1 became a type-system separation, J-3 became a measured 50-of-69, J-6 became a decode
that falsified its own dichotomy, J-4 and J-7 were closed by measurement rather than argument. Two of
ten were LIVE and both would have shipped as plausible numbers. **K-1…K-11 are written to the same
standard**, and `K-2`, `K-5` and `K-11` are the forward-pointed ones — hazards this build *created* for
the next, rather than inherited from the surface.

---

## 9 · DISPOSITION

**PASS.** B-2app is clear on the design surface. Carried forward:

- **`D-8` commissioned** (legolas, `MD-B2app-1`) — first priority, one lap, binary on the fight's identity.
- **B-3's brief carries `K-1…K-11`**, with `K-2` (the player-side zeros do not transfer to a pet) and
  `K-10` (predicate independence) first-class.
- **Wave-4 emitter carries the ten facet-(e) baton items** (§ 5), of which `F-2`'s layer axis and
  `F-5`'s named fork are prerequisites, not deliverables.
- **`S-8` addendum row** and the D-7 § 8 errata ride the gate fold.
- **`F-8` → jack-ryan** for discipline ratification.
- **Conductor:** `L-41` amended per C-1/C-2 this commit; facet-(d) ownership ruled at the next
  sequencing decision per C-3.

---

*DRIFT-CRITIC verdict, gandalf, 2026-08-24. Judged out of the conductor's foreground per the `L-23`
pattern. The build's best work is the decode it did not have to do (J-6) and the predicate it left
failing (P9). My one dissent is not with the build — it is with letting the run's headline design truth
rest on a declared grain when the decode costs one lap. Committed, not pushed.*
