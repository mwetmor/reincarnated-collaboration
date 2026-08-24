# Finding — 2026-08-24 — gamora KC2-MC **B-2app** (control APPLICATION, facet (e) SIM·application cell)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **BLOCK** (one, narrowly scoped) + 4 WARN + 5 INFO
**Target:** engine `84832c42` · `8add2a3d` · `e2122c1a` · `dbfab508` · `ac9b4d20` · `d01506df` (NOT pushed)
**Sibling artifact:** `E-s09-cp150-b2app` sha `43a6a48b5e39c13976a46e21bd01dfb421cdbf158502b617c9eee947808dd79e`
**Developer:** gamora (simulation seam) · **Conductor:** gandalf (RUN-CONDUCTOR), charter ledger `L-40` / `L-41`
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** #1 (math before code), #3 (no parallel regens / sequential), #8 (schema validation at boundaries), #10 (empirical inspection over assumption), #12 (semantic shifts published)
**ADRs:** ADR-002 (tiered approval), ADR-004 (cross-seam MIGRATION), ADR-006 (read-only external systems)
**Standing run law:** `L-33` amendment / `D4` prereg fidelity, **BLOCK force since `L-38`**

> **Method note.** Every claim below was **re-derived, not read**. I re-ran the driver at HEAD,
> re-hashed all six predecessors, diffed my own emission against gamora's, re-parsed the D-7
> artifacts, re-derived the Lap-X census-exclusion premise from Lap X's own emitter source, widened
> gamora's cap-binding census beyond its registered population, and ran two **mutation probes**
> against the predicates the brief flagged hardest. Where I did not re-derive something, I say so.

---

## What I found

B-2app is, on the evidence, the most disciplined build this run has produced. Prereg immutability is
**perfect** — each of the four governing documents has exactly one commit and none was edited after
it; `B2app-P9` stands byte-untouched and stands failing, with `P16`/`P17` registered 19 minutes
before the repair that needed them landed. The byte-safety claims all verify exactly. The
screenshot-519 falsification verifies *more strongly than gamora claimed it*. The J-map discharges
verify per-row. There are no by-name discards anywhere, and `B2app-P10`'s non-vacuity probe
reproduces.

And in the middle of that, the one thing the build itself declared as its worst self-defect —
`B2app-P12` acquitting the `IMPL`-is-not-a-refusal bug because the predicate copied the bug's
collapse — **is not actually repaired.** The repair moved the collapse from an inline
`verdict == "PERMITTED"` to a shared `ca.verdict_honours()` call that *both sides of the comparison
now route through*. I reinstated `D-B2app-3` verbatim and P12 still reports `holds=True` with zero
disagreements while the trapped player is helpless again. The registered ADDENDUM-3 clause "every
`IMPL` cell is HONOURED" was never implemented, and the two constants that encode the mapping are
uncited and structurally unreachable by the citation predicate. That is `BLOCK-2`.

---

# BLOCK-2 — `B2app-P12` IS STILL NOT AN INSTRUMENT, AND THE `ADDENDUM-3` REPAIR HAS NO AUTOMATED GUARD

## (a) The registered clause is unimplemented

ADDENDUM 3 (`dbfab508`) registered, before the repair ran:

> …and the count of cells whose CSV verdict is `IMPL` is **EXACTLY 2** …, of which **EXACTLY 1**
> lies in the five decoded states; **every `IMPL` cell is HONOURED**; and every one of the four
> verdict strings in the CSV appears in `HONOURED ∪ REFUSED` — an unknown fifth RAISES.
> **Falsifier:** any count, any unmapped verdict, **or any `IMPL` cell reading as refused.**

The shipped instrument (`gamora_kc2_mc_b2app_control_2026_08_24.py:386`) is:

```python
if probe._permits(req) != ca.verdict_honours(verdict):
    bad.append(f"{st}/{req}={verdict}")
```

and its `holds` is `not bad and not unmapped and cells == 60 and items_ok and len(impl_all) == 2 and
len(impl_cells) == 1`. **Nothing in that expression tests whether an `IMPL` cell is honoured.** The
count clauses are implemented; the honoured clause is not. The falsifier "any `IMPL` cell reading as
refused" is therefore **disarmed** — which is the `BLOCK-1` class, one build later.

## (b) The mutation probe — the falsifier cannot fire

I reinstated `D-B2app-3` exactly as ADDENDUM 3 describes it (`IMPL` → refused) and re-ran P12's body:

```
BASELINE  holds= True
MUTATED   holds= True | disagreements= [] | unmapped= [] | impl_all= 2 | impl_in_five= 1
   trapped player may cast? _permits("RequestSkillAction") under Trap = False
```

`probe._permits(req)` computes `verdict_honours(cell)`; the predicate computes
`ca.verdict_honours(verdict)`. **Both sides move together.** ADDENDUM 3's own lesson —
*"a predicate that derives its expectation from the same collapse the implementation performs is not
an instrument. The expectation has to come from the artifact, in the artifact's own vocabulary"* —
was written correctly and then not applied to the repair. The expectation still does not come from
the artifact; it comes from the module's own classification tuples.

**Ruling on the brief's predicate-independence question: NO.** The repaired `B2app-P12` is *less*
vacuous than the original — it now catches an unmapped fifth verdict and pins the `IMPL` cell census
at 2 / 1, neither of which the original could do — but **on the one proposition it was repaired for
it remains exactly as vacuous as before.** Its 60/60 still means "the implementation agrees with
itself," not "the implementation agrees with the CSV."

## (c) And the constants that encode the defect are uncited

`HONOURED_VERDICTS` and `REFUSED_VERDICTS` (`control_application.py:344,346`) are new module-level
constants introduced by the ADDENDUM-3 repair. They are `tuple`s, so `B2app-P10`'s type guard
(`isinstance(live, (bool, int, float))`) **cannot see them**, and they appear in neither
`declared_constants()["constants_introduced"]` nor math note § 9 (§ 9 predates ADDENDUM 3 and was
correctly never edited). P10 is *faithful to its registration* — its registered form says "every
module-level **numeric** constant" — so this is a scope gap, not a dishonesty. But the consequence
is exact:

> **The two constants that encode the four-valued → boolean mapping whose miscoding WAS `D-B2app-3`
> are outside every citation guard the build has, and the predicate that grades that mapping cannot
> convict a change to them.** The ADDENDUM-3 repair's only guard is one unit test.

## (d) The mitigating fact, stated so the severity is calibrated

`tests/test_kc2_mc_b2app_control_application.py:170` **is** the independent instrument:

```python
def test_a_trapped_player_may_still_cast():
    f = ca.ControlApplicationFold(limb=L); f.land_buckets("Trap", 20)
    assert f.suppresses_motion() and f.suppresses_channel()
    assert f.refuses_actives() is False       # RequestSkillAction is IMPL under Trap.
```

It asserts the decode's **sentence**, routes through no classification tuple, and **does** fail under
my mutation. So the model on disk is CORRECT, no emitted artifact is wrong, and no published figure
moves. This is a **predicate-integrity** BLOCK, not a modelling BLOCK — which is why it is cheap.

## The path forward (three lines, one re-run)

1. In P12, add the registered clause as an assertion whose expectation does **not** route through
   `ca.verdict_honours`: for every cell whose CSV verdict is `IMPL`, assert `probe._permits(req) is
   True` **literally**, and assert `"IMPL" in ca.HONOURED_VERDICTS` as a standalone check. Publish
   the mutation probe's result beside it (patch `HONOURED_VERDICTS` → P12 reds) exactly as B-1r's
   non-vacuity probe was published after `BLOCK-1`.
2. Cite `HONOURED_VERDICTS` / `REFUSED_VERDICTS` in `constants_introduced` with the `D-B2app-3`
   provenance. Consider whether `B2app-P10`'s successor should widen from *numeric* to *decision
   constants* — a registered scope change, in an addendum, not a silent widening.
3. Re-run. Wall is **8.3 s**. The new emission is a legal second b2app sibling under the `L-40` D5
   ruling (multiplicity legal, ambiguity not) provided the seal names one sha of record.

**No deviation addendum is owed for this repair** — like the P12 repair itself, it moves *toward*
the registered form. It should nonetheless be published, for the reason gamora gave in ADDENDUM 3:
a predicate having been vacuous for a whole run is a fact about the run that a silent fix erases.
**This will be the second run in a row where that sentence is the load-bearing one.**

---

# WARN

### `WARN-1` — the honest count is published in four mutually inconsistent forms

The substance is intact everywhere: `B2app-P9` failed, is named on every surface, and was not
rewritten. The *arithmetic label* is not:

| surface | count |
|---|---|
| artifact `⚑ predicates_holding` / `⚑ predicates_registered` (machine-computed) | **18 / 19** |
| commit `ac9b4d20`, `d01506df`, charter `L-41`, driver comment `:859` | **16 / 17** |
| driver `preds["B2app-P9"]["⚑ FAILED_AND_NOT_REWRITTEN"]` | **14 / 16** |
| ADDENDUM 2, at its own moment | **14 / 15** |

`16/17` is the merged convention (`P1a`/`P1b`/`P1c` counted as one `P1`); `18/19` is the row
convention the artifact's own `len(preds)` produces. Both are defensible; **no surface states which
convention it is using**, and `14/16` matches neither. The artifact is the surface a third party
reads, and it publishes `19` while the headline says `17`. Pick one convention, state it once, make
the machine field and the prose agree.

### `WARN-2` — two governing surfaces are stale on the addenda and on the grading set

* `artifact["addenda"]` (driver `:772`) and `declared_constants()["addenda"]` (`:1098`) list **only
  ADDENDUM 1**. ADDENDA 2 and 3 — which changed the *model* (the duration roll) and the *code*
  (`IMPL`) — are absent from both. The MIGRATION.md entry correctly says "ADDENDA 1–3"; the machine
  receipt does not.
* Both `⚑ quarantine` strings (driver `:815`, module `:1162`) end *"The grading predicates are
  `B2app-P1…P15` and nothing else."* `P16`/`P17` are grading predicates and `P16` gates on the
  record ensemble. The sentence that defines the quarantine's own scope is wrong.

### `WARN-3` — math note § 9's completeness claim does not re-derive

§ 9 states: *"Every one is cited in `control_application.declared_constants()["constants_introduced"]`,
and `B2app-P10` walks the module's AST to prove none is missing."* Re-derived at HEAD:

```
⚑ in § 9 but NOT in receipt: ['SURVIVAL_DIFFICULTY']
⚑ in receipt but NOT in § 9: ['TRUNCATE_BUCKETS']
```

`SURVIVAL_DIFFICULTY = "gladiator"` is load-bearing — it selects the halt9 difficulty column that
supplies the −40 scalars in the modifier pool. It is cited in the module docstring and in § 9; it is
**not** in the receipt, and P10's numeric-only scope cannot reach it. This is the **third instance
this run** of the `F-B1r-1` / `D-B2app-1` shape — a summary that names a member its own table does
not carry — and it is the first one that is gamora's own rather than inherited.

### `WARN-4` — `B2app-P14`'s holds clause is a tautology, and `gate_rolled` carries two meanings

`preds["B2app-P14"]["holds"] = n_land > 0 and n_ctrl >= 0`. **`n_ctrl >= 0` cannot be false for a
count.** The registered falsifier was "absence of either figure"; a tautology is not a presence
check. Separately, the artifact publishes `"gate_rolled": True` as a **hardcoded literal** at
`:725`, while the measured `n_gate_rolled` is **`0` on all five salts** (my re-run: `gate rolled
0/failed 0` on every leg). The same key name means *measured* on ledger rows and *capable* in the
predicate, inside one artifact — the `S-1` failure mode at a second address. The J-9 price itself is
sound and re-derives: **2 control-carrying landings in 683 landed monster attacks**, on B-2app's own
basis, with B-2's 2-in-562 appearing nowhere as an input.

---

# INFO

### `INFO-1` — `J-4` / `R-D7-1` are inert with **zero headroom**, and D-7 flagged the exact entry

I widened the census past its registered population — from the roster's 5 families (20 cells) to the
full 15-family enum (60 cells): **0 clamped entries / 60 cells.** The negative is *stronger* than
gamora measured. But the margin is one point:

```
Freeze  un-channelled  r = 80.0   cap = 80.0
```

`resistance_total` clamps on strict `>`, so 80.0 is correctly not clamped (`min(80,80) == 80`, no
movement) — but the falsifier gamora named (`max_entry > cap`) **needs 81 to fire**. D-7 § 2.3 says
so in its own words: *"`freeze_resist = 80` sitting exactly on the cap is now explained rather than
suggestive."* The measurement is right; "inert by measurement" is doing more work than the one-point
margin advertises, and § 4.1's table displays the 80 without saying it is *on* the line.

### `INFO-2` — two non-families are enumerated as families on the wire

`control_type_enum()` admits `CrowdControl` (64) and `CrowdControlCap` (65) — the **aggregate defence
stats**, not applicable control families. They zero-fill `application_counts`,
`player_control_resists` and `duration_modifier_pool`. A Layer-1 consumer reading
`application_counts` sees fifteen "families", two of which cannot be applied. `F-5`'s explicit-zero
convention applied to a mis-scoped key set. Harmless in-sim (`is_involuntary` keys on the ladder,
which carries the correct eight) — a presentation-surface item.

### `INFO-3` — 10 pet-sourced control rows are out of population and not declared

The pinned CSV carries 141 rows at `kind == 'control'`. Gamora's filter
(`actor_kind == 'roster' AND status == 'OK' AND rank_grade == 'MEASURED'`) yields 131. The 10
excluded are all `actor_kind == 'pet'` — **8 Stun + 2 Freeze**, from
`trap_lightningspike_hero_a01` / `trap_icespike_hero_a01`, all `OK` / `MEASURED`. The
roster-scope is **inherited from B-2's census** (`control_states.py:88,737`, where pets are
explicitly discussed) so this is a scoped decision, not a new silent exclusion — and **none of the 10
carries `max > min`**, so `P9`'s 12 and `P16`'s "EXACTLY 12" are unaffected. But § 0.1 enumerates
`F-5` explicit zeros for six absent families and says nothing about ten present-but-out-of-population
rows. B-2 could leave that alone because B-2 applied nothing; **B-2app is the build where "who can
control the player" stops being a census question**, and monster-summoned trap pets are a real
control source. One declared line, or a `C-B2app-6` naming it.

### `INFO-4` — a second inherited D-7 prose defect, same shape as `MD-B2app-1`

D-7 § 2.2 opens: *"The pinned `data/kc2/pm2_tg2_attack_damage.csv` carries **143 control rows**
(Stun 68, Freeze 35, Petrify 26, Confusion 8, Convert 4, Disruption 2 — all `MEASURED`)."* Re-derived
at HEAD: `kind == 'control'` yields **141**, and the 2 Disruption rows are **`kind == 'direct'`** —
which gamora's own § 0.1 already identifies as the structural blindness behind `WARN-2`. So § 2.2's
143 is composed across two `kind` values **without saying so**. Identical failure shape to
`MD-B2app-1`: a D-7 summary figure that does not re-derive against its own artifact. Cheap errata
candidate to ride alongside `MD-B2app-1`; the evidence CSVs are unaffected.

### `INFO-5` — `MD-B2app-1` has an independent corroborator gamora did not cite

ADDENDUM 1 grounds the Freeze/Petrify gap on § 3.3's vtable-census method and § 3.1's routing table.
There is a second, blunter witness in § 3.1 itself: its list of the **literal state-name strings**
passed to `ControllerAI::SetState` is

> `Immobilized · Trapped · Stunned · KnockedDown · TakeHit · Sleeping`

— **no `Frozen`, no `Petrified`.** D-7's own enumeration of reachable player states omits both
families, independent of the vtable diff. Worth adding to the named ask: it narrows the "IF NEITHER
CALLS `SetState`" branch toward the likely answer, which ADDENDUM 1 already flags as *"itself the
answer and a large one."* (The same list contains `TakeHit`, which § 3.3's table also lacks — the
`R-D7-3` watch item, consistent.)

---

## Verified — the claims that re-derive exactly

**1 · Prereg integrity (the `BLOCK-1` class) — CLEAN, and better than claimed.**

`git log --follow` on all four governing documents returns **exactly one commit each**. Nothing was
edited after its ALONE commit. Timestamps:

| commit | | time |
|---|---|---|
| `84832c42` | math note ALONE | 13:10:36 |
| `8add2a3d` | ADDENDUM 1 ALONE | 13:12:38 |
| `e2122c1a` | **ADDENDUM 2 ALONE — P16/P17 registered** | **13:37:26** |
| `dbfab508` | **ADDENDUM 3 ALONE** | **13:42:06** |
| `ac9b4d20` | **the code the addenda change** | **13:56:35** |
| `d01506df` | AGENT_STATE | 13:58:45 |

`P16`/`P17` precede the repair by **19 minutes**; ADDENDUM 3 precedes it by 14. Discipline #1 held on
all four. `B2app-P9`'s `registered_form` is byte-identical to the parent note's § 6 row and reports
`holds: False` with the 12 rows enumerated in full. **No by-name discards anywhere**: the only
`continue`s in the driver are structural (AST scope/type in `_b2app_p10_ast`) or *recorded* (the
`unmapped` list, which feeds `holds`). P10 non-vacuity probe reproduces —
patch the salt's citation away → `holds=False, uncited=['CONTROL_GATE_RNG_SALT']`.

**3 · The screenshot-519 falsification — VERIFIED, and the premise is stronger than gamora argued.**

Gamora's premise is a *class-membership* argument: Lap X admits player-class skills whose `Class ∈
ALWAYS_ON` and EoR is not one. Both halves check out —
`pm4l_emit_2026_08_14.py:164` is exactly `ALWAYS_ON = {"Skill_Passive", "Skill_Mastery",
"Skill_BuffSelfToggled", "Skill_BuffRadiusToggled"}` (the cited line number is exact), applied at
`:237`; and the pinned EoR note gives `Class = 'Skill_AttackRadiusSpin'`, in none of them. But there
is a **stronger, simpler verification gamora did not use**: the string `CrowdControl` appears
**zero times in the entire Lap-X emitter**. There is no expansion path, so the +25 is not merely
class-filtered out — it is *structurally absent* from the reconstruction. The census also carries
**11** keys with **no `defensivePetrify`, no `defensiveTrap`**, confirming inherit-by-construction.

Arithmetic, re-derived: Arm A requires `sheet ≥ recon + 25` = **78+25 = 103** (Stun) and
**75+25 = 100** (Freeze). Observed **79 / 80**; residuals **+1 / +5**; both an order of magnitude
below 25; two different values defeat any single display clamp; `playerDefenseCap = 80 ≠ 79`.
**Arm A falsified. Arm B is the arm of record.** Channelling `r` re-derived through the module:
**Stun 104 · Freeze 105 · Trap 101 · Petrify 59** — matching the claim character for character.

And the consequential count reproduced in **my own run**, not read from gamora's artifact:

```
arm-b-sheet-unchannelled | channelling=True : 50/69 rows deliver ZERO buckets {Freeze: 17, Stun: 33}
arm-b-sheet-unchannelled | channelling=False:  4/69                          {Stun: 4}
arm-a-sheet-mid-channel  | channelling=True :  4/69                          {Stun: 4}
arm-a-sheet-mid-channel  | channelling=False:  0/69                          {}
```

**50 of 69 confirmed** (33 + 17), against 4 under the dead arm. The design consequence the run bought
— *EoR channelling is effective CC-immunity to Stun/Freeze/Trap on this board, and Petrify is the one
hard-control family that reaches a channelling player* — is **carried by measurement, not by
assertion**, and it is baton-consequential exactly as the charter says. Both arms are run and both
counts published.

**4 · J-hazard discharges — verified per row.**

* **`J-1` — dodged in the type system.** `grep` over `control_application.py` returns exactly one
  crossing: `from .dot_timeline import BUCKET_MS`. No `_Entry`, `_Instance`, `PendingDot`,
  `source_key`, `ordinal_weight`. `B2app-P3` measures both laws **in one process**: control
  longest-wins **10 buckets** from two different attackers, against the DoT lane's ADD
  (**200.0 > 100.0**). The rule "share the clock, never the aggregation" is executable, not narrated.
* **`J-3` — LIVE and first-class.** `RESISTED-TO-ZERO` is a closed-vocabulary `EffectModel` member,
  zero-filled in `counts_by_effect_model`, documented in `export/MIGRATION.md` § 3 as *"a landing,
  not a silence"*, and covered end-to-end by
  `test_a_fully_resisted_control_is_a_landing_not_a_silence`. B-1r's zero-truncation proof correctly
  **does not transfer** — § 1.3's reasoning (the truncation follows the resistance scalar, so
  non-tenth-multiples are the norm) re-derives.
* **`J-4` — inert by measurement.** Reproduced (0 clamped / 20 cells) and **widened** by me to the
  full enum (0 clamped / **60** cells). `R-D7-1` falls the same way. See `INFO-1` on the margin.
* **`J-6` — DECODED, dichotomy false, and grounded in D-7's own text.** D-7 § 3.2: *"Only one
  involuntary effect is ever active, **regardless of how many control timelines are running**"* —
  the word *running* is the affirmative evidence — plus § 3.3: *"no self-timer … **The clock is the
  `DurationDamageManager` bucket list, and only that.**"* `Stop`/`StartInvoluntaryEffect` touch the
  controller state; the manager's lists are untouched; timelines burn concurrently. The ladder parses
  to `Immobilize > Petrify > Freeze > Trap > Sleep > Stun > Knockdown > TakeHit`, matching § 3.2
  exactly. **Being petrified burns the stun timer** is measured twice — by `B2app-P5` (Petrify→Stun
  in 19 ticks, Stun still live, **zero further landings**) and by
  `test_being_petrified_burns_the_stun_timer`.

**5 · Application counts and the survival delta — VERIFIED.** Confusion **2** across the 5-salt
ensemble (1 on salt 0, 1 on salt 1), each `applied: True` / `effect_model: DECODED-ZERO` /
`effect_inserted: False` / `suppression_basis: DECODED-ZERO (D-7 § 3.4)`. Every other family
presents as explicit `0`; `counts_by_effect_model` presents all four members; `state_ticks` presents
all five decoded states as `0`. Seven shifts signed, S-2/3/4 down and S-5/7 up. **The no-survival-delta
assertion is MEASURED, and I re-derived it**: `B2app-P1c` — stripped digest identical to `P1a`'s
fold-absent digest, un-stripped digest differing — holds in my own run, with `P1a` bound by digest to
B-1r's sealed record cell **read out of the b1r artifact** (`a17951a83365…`), that artifact **found
by hashing candidates, not by filename**.

**6 · Byte-safety — EXACT.** I re-hashed independently:

```
43a6a48b…  b2app        ← sibling sha, EXACT as claimed
30ef0031…  b1r-of-record        6ac7c4e0…  b1r-retained
0957daaf…  b1            a49ef783…  b2            20b05cb4…  mech
verify_frozen()  20/20   PRE and POST
```

All six unchanged PRE **and** POST. **Unrequested probe:** I re-ran the driver at HEAD and diffed my
emission against gamora's, key by key over the whole tree — **exactly 2 differences**, both volatile:

```
/wall_s      8.94 → 8.26
/started_utc 2026-08-24T17:57:08 → 2026-08-24T18:13:22
```

`43a6a48b…` **is** the emission HEAD produces. (My probe artifact has been deleted so no sibling
ambiguity is introduced under the `L-40` D5 condition.)

**7 · `MD-B2app-1` — CONFIRMED, and the overstatement is exactly this:** D-7 § 8 item 5 asserts a
decoded suppression verdict *"for Stun/Freeze/Petrify/Sleep/Knockdown/Immobilize"* — **six families**.
§ 3.3's table and `d7_md_b2_2_player_suppression.csv` carry **five states**: `Stunned`,
`KnockedDown`, `Sleeping`/`Sleep`, `Trapped`, `Immobilized`. **§ 8 names `Freeze` and `Petrify`,
neither of which has a column in either; and § 8 omits `Trapped`, which has a column in both and is
the subject of § 3.3's most-discussed row (the `IMPL` exception).** The gap is structural, not
clerical — § 3.3 is a `ControllerPlayerState` vtable census and § 3.1 routes Freeze (`0x0005b020`)
and Petrify (`0x0005b150`) through `Character::Begin<X>` with no exported state class. **The
conductor's errata note is owed on my confirmation**, and I recommend folding `INFO-4` and `INFO-5`
into it. The evidence CSVs are unaffected; this is a prose defect in the decode artifact.

**8 · Refusals and smoke.** `C-B2app-1…5` each carry a price in math note § 8 and in the artifact's
`⚑ refusals` — including `REACQUISITION_TICKS = 0` shipped as an explicit zero, which correctly
makes every published channel cost a **lower bound** rather than an estimate, with the price named
as 0 on the record cell. Smoke, re-run by me:

* `tests/test_kc2_mc_b2app_control_application.py` — **42 passed**, 0.12 s.
* kc2 blast radius — **452 passed / 1 failed**, the failure being
  `test_kc2_locomotion.py::test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface`.
  **Pre-existing, verified structurally**: neither that test file nor its subject
  (`secondary_streams.py`) appears anywhere in the `ec843589..HEAD` diff.
* engine-wide — **10,643 passed / 59 failed / 21 errors**, of which **exactly one is a kc2 test**.
  ⚑ **Scope disclosure: I did NOT re-derive a pre-build engine-wide baseline** (22 min/run). I
  bounded the claim by blast radius instead: the diff touches only `simulation/kc2/`, the driver,
  docs and tests; 58 of 59 failures are outside that surface. The "identical failure set" claim is
  **supported, not independently re-derived**, and I record it that way rather than adopting it.

**Cross-seam (ADR-004).** `export/MIGRATION.md` leads with the breaking `S-1` shift in a two-column
before/after table, gives the mechanical migration (`applied` → `effect_inserted`), documents the
full row schema and the four-member `effect_model` vocabulary, flags the
`tracks.circle_channel_active` change, and explicitly declines to pre-empt star-lord's `S-1` /
`F-5` / `C-B1r-3` decisions. This is the correct shape. Note that B-2's own `REQUEST 1` block higher
on the page still reads *"`applied` — `False` on every row"* as a mandatory field; the new entry
supersedes it, but the two now sit on one page saying opposite things — worth a one-line pointer at
the old block. Filed as part of `WARN-2`'s family, not separately.

---

## Action

- [ ] **gamora — BLOCK-2 (required before seal).** Implement `B2app-P12`'s registered ADDENDUM-3
      clause "every `IMPL` cell is HONOURED" with an expectation that does **not** route through
      `ca.verdict_honours`; publish a mutation probe showing P12 reds when `HONOURED_VERDICTS` is
      patched; cite `HONOURED_VERDICTS` / `REFUSED_VERDICTS` in `constants_introduced`. Re-run
      (8.3 s). No deviation addendum owed (the move is *toward* the registration) — publish anyway.
- [ ] **gamora — WARN-1.** Choose one predicate-counting convention, state it once on the artifact,
      make `⚑ predicates_registered` and the prose headline agree. Correct the `14/16`.
- [ ] **gamora — WARN-2.** Add ADDENDA 2 and 3 to both `addenda` arrays; correct both
      `⚑ quarantine` strings from `P1…P15` to the full grading set; add a supersession pointer on
      B-2's `REQUEST 1` `applied` block in `export/MIGRATION.md`.
- [ ] **gamora — WARN-3.** Reconcile math note § 9 against the receipt (`SURVIVAL_DIFFICULTY` /
      `TRUNCATE_BUCKETS`) in an addendum — **do not edit § 9**, which is correctly immutable.
- [ ] **gamora — WARN-4.** Replace `n_ctrl >= 0` with a real presence check; disambiguate
      `gate_rolled` (capability vs measurement) or rename the predicate's field.
- [ ] **gamora — INFO-1/2/3.** Note the zero-margin on Freeze's cap entry; drop or mark
      `CrowdControl`/`CrowdControlCap` in the family-keyed emissions; declare the 10 pet-sourced
      control rows as out-of-population.
- [ ] **gandalf (RUN-CONDUCTOR).** Errata note on `MD-B2app-1` is **owed and confirmed** — fold in
      `INFO-4` (D-7 § 2.2's 143 vs the artifact's 141 + 2 `kind='direct'`) and `INFO-5` (§ 3.1's
      state-name list omits Frozen/Petrified) as same-shape items. Record `BLOCK-2` at `L-42` and
      re-open the B-2app seal gate.
- [ ] **Matt — no decision required.** `BLOCK-2` is a within-seam predicate repair; ADR-002 puts it
      in gamora's lane with my clearance on the re-submission. Escalate to Matt only if gamora
      contests the ruling in (b).

---

## Verdicts

### Does B-2app SEAL?

> **NO — B-2app does NOT seal at `43a6a48b…`.** One BLOCK stands. The seal is held on `BLOCK-2`
> alone; **every other claim in the submission verifies**, and several verify more strongly than
> claimed. This is a *predicate-integrity* hold, not a modelling hold — the model on disk is
> correct, the artifact is internally consistent, no published figure moves, and the discharge is a
> three-line predicate amendment plus an 8-second re-run. On clearance of `BLOCK-2` (and the WARN
> items folded into the same re-run), **B-2app seals on the re-emitted sibling**, with
> `43a6a48b…` retained as evidence per the `L-40` D5 ruling.

### May the star-lord discharge proceed against HEAD?

> **YES — with one boundary.** The `C-B1r-3` + `B-1f § 9.5` discharge, **as scoped** (replacement
> text into `src/reincarnated/export/MIGRATION.md`), is disjoint from `BLOCK-2`'s repair surface
> (`simulation/kc2/control_application.py` + the driver), touches no digested surface, no member of
> `threat.SUBSTRATE` and no `FROZEN` artifact, and therefore cannot move `B2app-P1a`'s config bind
> or any predecessor pin. My Gate-2 review is **complete**, so the "no writer moves HEAD under a
> review" hold releases. It may fire now.
>
> ⚑ **The boundary, and it is load-bearing:** `C-B1r-3`'s *request* is a schema shape — *"either
> `_surface()` excludes provenance prose by construction, or provenance strings carry a version
> marker."* **If the discharge extends to touching `_surface()`, it moves every digest in the
> family** — B-1r's sealed `B1r-P1c` record digest, `B2app-P1a`'s bind to it, and every artifact
> that cites either. That is not a doc discharge; it is a new dispatch with a cross-seam blast
> radius, and it must re-gate before a line of it lands. **Doc discharge: proceed. `_surface()`
> change: STOP and re-dispatch.**

---

## References

**Reviewed (engine, `~/Games/reincarnated-engine/`):**
- `src/reincarnated/simulation/kc2/control_application.py` (1,164 lines)
- `src/reincarnated/simulation/scripts/gamora_kc2_mc_b2app_control_2026_08_24.py` (885 lines)
- `src/reincarnated/simulation/math/kc2-mc-b2app-control-application-2026-08-24.md` + `-ADDENDUM-`, `-ADDENDUM-2-`, `-ADDENDUM-3-`
- `src/reincarnated/export/MIGRATION.md` (the 2026-08-24 B-2app entry)
- `src/reincarnated/simulation/kc2/control_states.py`, `dot_timeline.py`, `threat.py`
- `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b2app-20260824_175717.json`
- `tests/test_kc2_mc_b2app_control_application.py`
- `data/kc2/d7_control_application_decode_README.md`, `d7_control_application_parameters.csv`,
  `d7_md_b2_2_player_suppression.csv`, `pe1_eor_spin_parameters.md`, `pm2_tg2_attack_damage.csv`

**Reviewed (meta-repo, `~/Games/reincarnated-collaboration/`):**
- `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` (`L-40`, `L-41`)
- `agentic_orchestration/gandalf/notes/2026-08-24-kc2-mc-b1r-drift-critic-verdict.md` (§ 6 J-map, § Q6)
- `agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-x-mitigation-decode/pm4x_player_defense.json`
- `agentic_orchestration/research/scripts/pm4l_emit_2026_08_14.py` (`:164` `ALWAYS_ON`, `:237` the filter site)

**Prior findings in this run:** `2026-08-24-gamora-kc2-mc-b1-gate2.md` · `…-b2-gate2.md` ·
`…-b1r-gate2.md` (`BLOCK-1` and its `L-40` clearance)

---
---

# CLEARANCE — 2026-08-24 — `BLOCK-2` DISCHARGED · **B-2app SEALS**

**Reviewer:** jack-ryan (DEV-MODE, Gate 2 · clearance re-derivation)
**Severity:** **CLEAR** — `BLOCK-2` discharged · 1 new WARN · 3 new INFO · none seal-holding
**Target:** engine `f7382122` (ADDENDUM 4) → `1208ae12` (ADDENDUM 5) → `15ffccc5` (build), NOT pushed
**Sha of record:** `a4b84ed5da98d306ceb3111e4aa940a1c4a6d629b58113d45530b90b9f599a12`
**Developer:** gamora · **Conductor:** gandalf (RUN-CONDUCTOR), charter ledger `L-46`
**Precedent:** the `B-1r` clearance appended at `d1e9495e` — same shape, same method.

> **Method note.** As with the parent finding: **re-derived, not read.** I re-ran the driver at HEAD
> and diffed my emission against gamora's key-by-key; I ran M1 and M2 myself rather than reading the
> artifact's probe block, **and I added a third mutation gamora did not run**; I mutation-tested all
> three registered-form changes (`P10`, `P7`, `P19`) on every falsifier limb; I re-hashed all six
> retained artifacts; and I re-derived the digest and numeric-leaf censuses independently rather than
> adopting `P18`/`P19`'s counts. My probe emission has been deleted — exactly two `b2app` artifacts
> remain on disk.

## What I found

`BLOCK-2` is **discharged, and the discharge is stronger than the ask.** I asked for one clause whose
expectation does not route through `ca.verdict_honours`; gamora shipped **two mutually independent**
ones — the literal `is True` on the `IMPL` cell and the standalone `"IMPL" in ca.HONOURED_VERDICTS` —
and my own third mutation proves they are independent in the direction gamora did not test. Every
registered-form change in the build is covered by an addendum whose commit precedes the build, and
each one convicts under mutation. The label-only delta re-derives exactly on my own census. And the
build's own self-disclosure sweep found and repaired a second instance of the `BLOCK-2` class
(`P7`) that I had not caught, then ADDENDUM 5 found a third (`P18`'s digest blindness) by reading its
own emission rather than its own `holds` field. **That is the behaviour the run law was written to
produce.** One new WARN — and it is, once more, `WARN-2`'s exact shape.

---

## 1 · Driver re-run — REPRODUCES, 3 volatile leaves

Re-ran `gamora_kc2_mc_b2app_control_2026_08_24.py` at HEAD. **20/21 holding, `B2app-P9` failing**,
wall **8.21 s** (gamora 8.33 s). Key-by-key diff of my whole emission tree against `a4b84ed5…`:

```
n_diff = 3
  /wall_s                                                       8.33 -> 8.21
  /started_utc                                                  19:22:34.922599 -> 19:30:10.448115
  /predicates/B2app-P18/class_2_differing_leaves//started_utc/new   (the same volatile, once more)
```

**Two distinct volatile quantities, nothing else.** `a4b84ed5…` **is** the emission HEAD produces.

## 2 · Mutations — I ran M1 and M2 myself, and added M3

```
BASELINE   holds=True   impl_asserted=['Trapped/RequestSkillAction'] impl_bad=[] IMPL_in_HON=True  trapped_may_cast=True
M1  D-B2app-3 reinstated      holds=False  disagreements=[]  impl_bad=['Trapped/RequestSkillAction=IMPL']  IMPL_in_HON=False  trapped_may_cast=False
M2  IMPL dropped              holds=False  unmapped=['Trapped/RequestSkillAction=IMPL']                    IMPL_in_HON=False
M3  ⚑ MINE — tuples UNTOUCHED, _permits() broken on the IMPL cell
                              holds=False  disagreements=[...]  impl_bad=['Trapped/RequestSkillAction=IMPL']  IMPL_in_HON=True
RESTORE    holds=True   tuples byte-equal: True
```

`M1` — my own `BLOCK-2` mutation verbatim — now reds, and note **`disagreements` is still empty under
it**: the old collapse is *still silent*, exactly as the commit subject claims, and the two new
clauses are what convict. `M3` is the test gamora did not run and the one that matters most for
durability: with `HONOURED_VERDICTS` left correct and the *implementation* broken, `IMPL_in_HON`
stays `True` and the literal `is True` clause is the sole conviction. **The two clauses cover the two
different failure directions.** The repair is an instrument, not a mirror.

> **Ruling on predicate-independence, reversed from the parent finding: YES.** `B2app-P12`'s
> expectation now comes from the artifact, in the artifact's own vocabulary. `BLOCK-2` is discharged.

## 3 · The three registered-form changes — all addendum-covered, all non-vacuous

Commit times (`git log`, not read from prose):

| doc / commit | time | precedes build? |
|---|---|---|
| ADDENDUM 4 `f7382122` — `P12` § 1.2, `P10` § 2, `P7` § 10.1, `P14` § 6.1, `P15` § 9.3, `P18` § 9.4 | 15:08:39 | ✅ |
| ADDENDUM 5 `1208ae12` — `P19` § 4 | 15:21:26 | ✅ |
| the emission itself | 15:22:43 | (77 s after ADDENDUM 5) |
| build `15ffccc5` | 15:27:20 | — |

**Prereg immutability: PERFECT for the second time.** `git log --follow` on all **six** governing
documents returns **exactly one commit each** — nothing edited after its ALONE commit, including the
parent math note § 9, which was correctly reconciled in ADDENDUM 4 § 5 rather than amended.

**No silent registered-form change.** I diffed every `registered_form` string across the two
siblings: `P10`, `P14`, `P15` changed and each carries its `D-B2app-N` tag and addendum section
inline; `P18`/`P19` are added; **all fifteen others are byte-identical, `B2app-P9` included.**

My mutations on each of the three:

```
P10  baseline holds=True (n_walked=34)
     drop HONOURED_VERDICTS from receipt  -> holds=False  uncited_decision_tables=['HONOURED_VERDICTS']
     drop SURVIVAL_DIFFICULTY (WARN-3)    -> holds=False  uncited_scalars=['SURVIVAL_DIFFICULTY']
     add a NEW module-level re.Pattern    -> holds=False  excluded_unregistered=['JR_NEW_PATTERN']
P7   baseline holds=True  n_over=0  min_headroom=0.0
     one entry +1 over cap, module clamp flag STILL 0 -> holds=False  (the OLD form would have said True)
P19  P1a/digest (the config bind) moved   -> holds=False   P1c/digest_stripped moved -> holds=False
     a P11 predecessor pin moved          -> holds=False   stale may-move path       -> holds=False
     P1c inequality collapsed             -> holds=False   wrong candidate file      -> HALTS (found by hash)
```

`P10`'s widening **closes the class, not the instance** — my third mutation adds a constant of an
unregistered *type* and it reds. `P7`'s new clause convicts while the module's own clamp flag reads
`0`, which is precisely the `BLOCK-2` shape it was repaired for. `P19` is armed on all four limbs.

## 4 · RULING — the `985067cb…` deletion is **LEGAL**

Under my own `L-40` D5 ruling (sibling **multiplicity** legal, sibling **ambiguity** not), a declared
deletion of a superseded intermediate is legal **when three conditions hold, all three of which hold
here:**

1. **It is not the seal candidate and no sealed surface cites it.** `985067cb…` was a FIX2
   intermediate emitted before ADDENDUM 5 registered `P19`. Nothing grades against it — `P18` and
   `P19` both diff against `43a6a48b…`.
2. **The deletion is DECLARED, by sha, with a reason, in an immutable prereg document, before the
   seal.** ADDENDUM 5 § 5 item 2 does exactly this. ⚑ This condition carries more weight here than
   it looks: **`b2app` artifacts are untracked in git**, so the deletion is irreversible and the
   declaration is the *only* record. "Git history is the archive" does not apply to this run's
   emissions. Gamora met the higher bar without being told it existed.
3. **The fact it witnessed is independently reproducible from a retained artifact.** The digest
   movement `848e102c… → db73e052…` that motivated `P19` is reproduced on the sealed emission's own
   `P19` block against `43a6a48b…`. The deleted file was not the sole witness.

**Fail any of the three and the deletion is illegal** — in particular, deleting a *cited* or
*sole-witness* emission would be evidence destruction regardless of declaration. Retaining
`985067cb…` would itself have created the D5 hazard: three `b2app` files, one of which carries a
**different predicate set** (20 rows, no `P19`), which is ambiguity of exactly the forbidden kind.
**The deletion improved the record.** Disk state verified: exactly two `b2app` artifacts, both
gamora's, my probe removed.

## 5 · Label-only delta — RE-DERIVED INDEPENDENTLY, verified

I ran my own census over the two **finished** files rather than adopting `P18`/`P19`'s numbers:

```
digest leaves  OLD=27  NEW=35  IN BOTH=27  moved=1  -> ['/predicates/B2app-P1c/digest_full']
NUMERIC leaves moved over the whole tree = 3:
   /wall_s                 8.94 -> 8.33    (registered volatile)
   /⚑ predicates_holding     18 -> 20      (excluded by PATH, declared, values printed)
   /⚑ predicates_registered  19 -> 21      (excluded by PATH, declared, values printed)
/predicates/B2app-P1a/digest            a17951a83365…  SAME  ← ⚑ the config bind to B-1r's sealed cell
/predicates/B2app-P1c/digest_stripped   a17951a83365…  SAME  ← ⚑ the survival claim
/predicates/B2app-P1c/digest_full       848e102c… -> db73e052…  MOVED (the one registered path)
/predicates/B2app-P1c/digest_full_of_incumbent  538e5178…  SAME
```

**Not one number moved outside the two declared count fields and the volatile.** The `D-8` re-grade
is label-only **by my measurement, not by gamora's.** `P1a`'s bind and `digest_stripped` are
byte-identical, so the survival claim and the B-1r seal binding both survive the re-grade intact.

## 6 · Predecessor bytes + the pre-existing fail — EXACT

```
43a6a48b…  b2app candidate (retained evidence)      a4b84ed5…  b2app OF RECORD
30ef0031…  b1r-of-record      6ac7c4e0…  b1r-retained
0957daaf…  b1                 a49ef783…  b2          20b05cb4…  mech
```

All re-hashed by me. All match the artifact's `B2app-P11` **PRE and POST** blocks exactly, and all
match the parent finding's record. `43a6a48b…` verified byte-unchanged and is declared on the sealed
artifact's `⚑ b2app_candidate_retained` block — **which is the disambiguation `L-40` D5 requires.**

Smoke, re-run by me: `tests/test_kc2_mc_b2app_control_application.py` — **44 passed** (was 42; two
added by the repair), 0.11 s. KC2 blast radius — **454 passed / 1 failed**, the failure being
`test_kc2_locomotion.py::test_AC_10_10…` at `secondary_streams.py:136`. **Pre-existing, verified
structurally again**: `git diff --name-only d01506df..HEAD` returns seven files, and neither
`secondary_streams.py` nor `test_kc2_locomotion.py` is among them.

## 7 · Star-lord `5764f89c` — CANNOT have moved anything I graded

Doc-only: **one file, `src/reincarnated/export/MIGRATION.md`, 274 insertions, zero deletions.**
`MIGRATION.md` appears in **no** `pins` entry, is read by no predicate, and is in no digested surface.
The boundary I set in the parent finding **held exactly**: star-lord's own § 1 records
*"`_surface()` is UNTOUCHED and no digest moved"*, and the commit stat confirms it. Landed 15:06:07,
before ADDENDUM 4, so it also sits inside this build's own `B2app-P11` PRE bracket. ⚑ Checked
unprompted: gamora's `15ffccc5` also writes `MIGRATION.md` — it is a **pure append**, star-lord's
`C-B1r-3` text survives at HEAD intact. No clobber.

---

# `WARN-5` (NEW) — ⚑ `WARN-2` RECURS AT FOUR ADDRESSES, IN THE BUILD THAT REPAIRED `WARN-2`

ADDENDUM 4 § 4 correctly repaired both `addenda` arrays and both `⚑ quarantine` scope sentences.
Then **ADDENDUM 5 added `B2app-P19`, and the repaired text went stale by one — undeclared.**

| surface | says | truth |
|---|---|---|
| `artifact["addenda"]` | ADDENDA **1–4** | ADDENDUM 5 exists and registers a grading predicate |
| `declared_constants()["addenda"]` | ADDENDA **1–4** | same |
| `artifact["⚑ quarantine"]` | *"The grading predicates are `B2app-P1…P18` and nothing else."* | `P19` grades, and holds |
| `declared_constants()["⚑ quarantine"]` | same sentence | same |

The string `ADDENDUM-5-2026-08-24.md` **appears nowhere in the sealed artifact.** This is the
identical failure shape to `WARN-2` — *the sentence that defines the quarantine's own scope is
wrong*, and the machine receipt does not carry a governing document — one build later, on the
repair. ADDENDUM 5 § 5 declared **two** consequences of adding a predicate (the row count, the
deleted intermediate); **the third — that it invalidates ADDENDUM 4's just-shipped scope text — was
not among them.**

**Severity: WARN, not BLOCK, and it does NOT hold the seal.** No falsifier is disarmed; `P19` is
armed on all four limbs and I proved it. No number moves. `P19`'s own `registered_form` on the
artifact names *"ADDENDUM 5 § 4"*, so the registration is traceable at one remove, and
`⚑ predicates_registered = 21` is correct. Principle #5: an 8-second re-run to fix two strings and
one array entry would emit a **third** `b2app` sibling — a worse outcome under `L-40` D5 than a
carried WARN.

**Durable fix, and it is the standard gamora set for herself in ADDENDUM 4 § 2 — close the class, not
the instance.** Both defects are hand-maintained literals (`control_application.py:1179,1355`;
driver `:1337,1386`). Derive the `addenda` array from a glob of `simulation/math/kc2-mc-b2app-*` and
derive the quarantine's predicate range from `sorted(preds)` at emission time. Then no future
addendum can strand either sentence. **Rides to B-3.**

# INFO

### `INFO-6` — the deletion is declared in the addendum but not on the artifact

`985067cb…` appears **nowhere** in the sealed artifact. The artifact carries
`⚑ b2app_candidate_retained` for the *retained* sibling and nothing for the *deleted* one. The
declaration in ADDENDUM 5 § 5 is what makes the deletion legal (§ 4 above) and it is sufficient —
but by `WARN-1`'s own lesson, *the artifact is the surface a third party reads*, and a reader of the
artifact alone cannot learn that a third emission existed. A `⚑ b2app_intermediate_deleted` block
with the sha and the reason costs one key.

### `INFO-7` — `P18`'s promised side-by-side prints `null`, and its reason text pre-dates ADDENDUM 5

ADDENDUM 4 § 9.4 promised the excluded paths' *"old and new values … printed side by side so the
reader sees `18 → 19` and `19 → 20` explicitly rather than being told they were skipped."* The
artifact publishes `{"old": 18, "new": null}` and `{"old": 19, "new": null}` — the *new* side is
absent, a consequence of the diff timing that ADDENDUM 4 itself pre-declared, so the mechanism is
honest but the promise is half-kept. The `reason` string also states the movement as `19 -> 20` /
`18 -> 19`; the true movement is `19 -> 21` / `18 -> 20`. **Disclosed** — ADDENDUM 5 § 5 item 1
corrected it in writing and deliberately did not edit `P18`, which is the correct immutability call.
Recorded so the artifact and the addendum are read together.

### `INFO-8` — ADDENDUM 5's digest census does not re-derive; `P19` holds anyway

ADDENDUM 5 § 2 says it re-derived *"all **33** digest-shaped leaves"* and § 4 registers the
expectation *"exactly one moved … and **32** unmoved."* My independent count over the candidate:

```
digest leaves in the candidate = 27   (in both = 27, moved = 1, unmoved = 26)
```

§ 2's own table enumerates **26** — it counts *"the five substrate pins"* when `/pins` carries
**six** (`b1r_record_digest_read_from_artifact` is the sixth). So the prose says 33, the table
implies 26, and the artifact measures 27. **`P19` holds legitimately** — its three registered clauses
are about *illegal moves*, *stale registrations* and the `P1c` inequality, none of which references
the census size, and all three re-derive. This is the **fourth instance this run** of the
`F-B1r-1` / `D-B2app-1` / `WARN-3` shape: a summary that names a count its own table does not carry.
At four instances it has stopped being an errata item and started being a **discipline candidate** —
*a registered expectation stated as a number must be computed, not counted by hand.* Recommend
gandalf consider it for the disciplines file.

---

## Action

- [x] **gamora — `BLOCK-2`: DISCHARGED.** Verified by independent re-run, independent M1/M2, and a
      third mutation of my own. No further action.
- [x] **gamora — `WARN-1` / `WARN-3` / `WARN-4`: DISCHARGED.** Row convention stated once
      (`⚑ predicate_count_convention`, `20/21`, merged counts published beside); § 9 reconciled in
      ADDENDUM 4 § 5 with § 9 correctly unedited and both `SURVIVAL_DIFFICULTY` and
      `TRUNCATE_BUCKETS` now in the receipt **and enforced** by the widened `P10`; `P14`'s tautology
      replaced with a real presence check and `gate_rolled` split into
      `⚑ gate_is_ROLLED_by_this_build` (capability) vs `⚑ n_gate_rolled_MEASURED = 0` (measurement).
- [ ] **gamora — `WARN-2`: PARTIAL → carried as `WARN-5`.** Four addresses stale by one. **Do not
      re-run B-2app for it.** Fix in B-3 by *deriving* the addenda array and the quarantine's
      predicate range instead of hardcoding them.
- [ ] **gamora — `INFO-6/7/8`.** Publish the deleted intermediate on the artifact; note `INFO-7`
      when B-3 re-uses the excluded-by-path construction; recompute registered census figures rather
      than hand-counting them.
- [ ] **gandalf (RUN-CONDUCTOR).** Record the clearance and **seal B-2app at `a4b84ed5…`** (§ below).
      `MD-B2app-1` errata note remains owed from the parent finding, with `INFO-4` / `INFO-5` folded
      in. Consider `INFO-8` as a new engineering-discipline candidate — four instances this run.
- [ ] **Matt — no decision required.** Within-seam predicate repair cleared under ADR-002.

---

## Verdicts

### Does B-2app SEAL?

> ## **YES.**
>
> **B-2app SEALS on `a4b84ed5da98d306ceb3111e4aa940a1c4a6d629b58113d45530b90b9f599a12`**
> — `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b2app-20260824_192243.json`,
> at engine commit **`15ffccc5`**. **That is the single sha of record.**
>
> `43a6a48b…` is **retained as evidence and is explicitly NOT of record**; the sealed artifact names
> it in `⚑ b2app_candidate_retained` with its status, which discharges the `L-40` D5 ambiguity
> condition on the artifact itself rather than by convention. `985067cb…` is **legally deleted**
> (§ 4). Exactly two `b2app` artifacts exist on disk and only one claims the seal.
>
> `BLOCK-2` is discharged on my own measurements. Every registered-form change is addendum-covered
> with a commit time preceding the build, and every one convicts under mutation. Prereg immutability
> is perfect across all six governing documents. `B2app-P9` stands **byte-untouched and failing**, as
> registered, at 20/21. `WARN-5` and `INFO-6/7/8` ride to B-3 and **do not hold the seal**: none
> disarms a falsifier, none moves a number, and a re-run to discharge them would emit a third sibling
> — which `L-40` D5 disfavours more than it disfavours a carried WARN.

### The thing I looked hardest for, and did not find

> The parent `BLOCK-2` was *a repair that routed both sides of the comparison through a shared
> collapse.* I swept the whole repair for a recurrence and **there is none.** `P12`'s two new clauses
> are independent of each other and of the classifier — proven by my `M3`, which breaks the
> implementation while leaving the tuples correct and is still convicted. `P7`'s new clause is
> literal arithmetic that fires while the module's own clamp flag reads `0`. `P10`'s widening is
> type-complete with a both-directions exclusion register. `P18` and `P19` take their expectations
> from a re-hashed file on disk, and `P19` re-checks `P1c`'s inequality rather than inheriting its
> `holds`. The single shared `_b2app_p12_body()` between the graded run and the probe is **not** the
> same-collapse hazard — it is the opposite one closed, since a probe that re-implements the
> predicate is a second copy that can drift.
>
> The one thing I did find, `WARN-5`, is not the `BLOCK-2` class at all. It is `WARN-2`'s class:
> **a hand-maintained string that a later, correctly-immutable document made stale.** The fix is to
> stop hand-maintaining it.

---

## References — clearance

**Re-derived (engine, `~/Games/reincarnated-engine/`):**
- `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b2app-20260824_192243.json` (**of record**)
- `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b2app-20260824_175717.json` (retained evidence)
- `src/reincarnated/simulation/scripts/gamora_kc2_mc_b2app_control_2026_08_24.py`
  (`_b2app_p12_body` `:411`, `_b2app_p12_mutation_probe` `:471`, `_b2app_p10_ast` `:544`,
  `_b2app_p18_label_only` `:250`, `_b2app_p19_digests` `:330`, `P19_MAY_MOVE` `:326`, `P7` `:802`)
- `src/reincarnated/simulation/kc2/control_application.py` (`:1179` addenda array, `:1355` quarantine)
- `src/reincarnated/simulation/math/kc2-mc-b2app-control-application-ADDENDUM-4-2026-08-24.md`
- `src/reincarnated/simulation/math/kc2-mc-b2app-control-application-ADDENDUM-5-2026-08-24.md`
- `src/reincarnated/export/MIGRATION.md` (star-lord `5764f89c` + gamora's append)
- `tests/test_kc2_mc_b2app_control_application.py` (44 passed)

*Clearance appended by jack-ryan, 2026-08-24. Not pushed.*
