# The three-goal end state, and whether a digital twin exists between here and there

**Author:** gandalf (`ARCHITECT`), 2026-07-25 — commissioned by Matt same session
(*"ultra think through our 3-part goal in terms of exactly what specs we would need as an end
state and let me know if a digital twin exists between our current state and the end state
where all 3 goals are met to which an autonomous run can potentially be drafted in the future"*).
**Companion ruling, same session:** Q47 → DEFERRED-EMPIRICAL (tolerance is an output of unit
measurement, not an input — `canonical/matt_decision_needed/README.md`).
**Prior frame:** `agentic_orchestration/skill_handoff_2026-07-25.md` §§ 0–2.

---

## 0. The verdict up front

**Yes — a digital twin exists in potential, and it has a precise, honest boundary.**
The twin is not a fourth artifact we would build alongside the three goals. **The twin IS the
three goals met:** frozen GD parameters (goal 2's domain) + complete mechanism vocabulary
(goal 1) + a measured-correct key (goal 3) *is* a computable replica of a GD fight that no
longer needs the live game to run. The live game's irreplaceable role collapses to one thing —
**a finite, bankable validation oracle** (Matt's controlled trials, captured once per ladder
rung, reusable forever). Everything else is agent-side and autonomous-runnable.

An autonomous run **cannot be chartered today** — eight named gaps below, two of them
elicitation-shaped, one of them newly surfaced by this derivation. But every gap is bounded,
none is open-ended research, and the sequence from here to a charterable run is short and
mostly already in motion.

---

## 1. Method note

The § 8.4 corrective applies to this document's own reasoning: every spec claim below was
checked against **each of the three goals separately**. Where a requirement serves one goal
and not the others, it says so. Where this derivation found a surface no goal's current
program covers, it is flagged as NEW rather than silently folded in.

---

## 2. End-state spec, per goal — in decidable form

A spec is only run-charterable if its "done" is **decidable** (desirable-run-pattern § 3:
bounded substrate in, decidable target-state out). Each goal below is stated as the artifact
set + the decision procedure that closes it.

### 2.1 Goal 1 — "all of GD's combat mechanisms exist in our battle sim"

**End-state artifacts:**

| Artifact | Content | Owner |
|---|---|---|
| **G1-A — Mechanism coverage matrix** | All 40 `ControllerMonster` states → the 7 mechanism families (+ 2 loose items) → per state: `MODELLED` / `PARTIAL` / `ABSENT` / `OUT-OF-SCOPE`, with our sim's equivalent construct **named** (not asserted) | gamora (audit), gandalf (family design) |
| **G1-B — Scope declaration** | Which states are declared out. Matt said *combat* mechanisms — the ~7 quest/cosmetic states (`QuestWalk`…`Emote`, `Sleeping`, `Patrol`) are presumptively OUT, but that is a **ruling, not a default** — one line from Matt closes it | Matt (ruling) |
| **G1-C — Per-family behavior specs + implementations + tests** | For each `ABSENT`/`PARTIAL` family (telegraph, combat spacing, fear granularity, pack hierarchy, idle tri-state, ranged modelling, monster support skills, pathing-recovery): a spec of the state's *transition semantics* (entry trigger, exit trigger, parameter bindings — e.g. `AlertBeforePursue` bound to `SightAngerRate`/`InnerSightAngerRate`), then sim code + a behavioral test per state | gandalf (spec) → gamora (build) |

**Decision procedure:** goal 1 is DONE when every in-scope state's row in G1-A reads
`MODELLED` and its behavioral test passes — *the sim's controller, given the GD parameters,
enters and exits the state under the trigger conditions the binary defines.* Fully decidable,
fully agent-side, with one caveat: some trigger semantics are **inferences** from binary +
observation (the D-b telegraph join is the type specimen), and each inference needs one live
confirmation before its test is written against it. Those confirmations are single
observations, foldable into any Matt trial.

### 2.2 Goal 2 — "a conversion key for their player and monster characters"

**End-state artifacts:**

| Artifact | Content | Owner |
|---|---|---|
| **G2-A — Key domain declaration** | WHAT converts. "Player and monster characters" needs unpacking: monster = creature records (proven at width 1). Player = class/mastery? skills? **devotion constellations? gear?** Each inclusion multiplies the field-mapping surface. **UNRULED — the largest open elicitation** | Matt (grill session) |
| **G2-B — Field-mapping tables** | Per in-domain record type: GD field → sim field, with per-field fidelity class: `EXACT` / `DERIVED` (formula stated) / `APPROXIMATED` (loss stated) / `UNMAPPED-DECLARED`. Versioned; pinned to the frozen Edition-II manifest | rocket/gamora build, gandalf spec, elrond substrate |
| **G2-C — Unit reconciliation constants** | DBR distance units ↔ GD world-space ↔ sim units; GD ms ↔ sim ticks; damage/HP scale. **MEASURED, not assumed** — the WarpCursor calibration experiment (T9 item 2) is the instrument | Matt (one trial) + gamora |

**Decision procedure:** goal 2 is DONE at declared width when every field of every in-domain
record type carries a fidelity class with provenance, and the unit constants have empirical
error bars. Decidable. **Note the key is a pure function between two frozen digital spaces**
— once G2-A is ruled and G2-C is measured, building it out to full width requires zero live
game and zero Matt hours. It is the most autonomous-runnable object in the program.

### 2.3 Goal 3 — "measure the comparative correctness of the key and tune it"

**End-state artifacts:**

| Artifact | Content | Owner |
|---|---|---|
| **G3-A — Fixture bank** | Banked GD reference fights, one set per ladder rung (hand-off § 2.3). Per fixture: *setup* (character record + monster record(s) + distance + procedure, all by DBR identity if `game.Spawn` works) + *outcome* (TTK, damage dealt/taken, HP curve; state timeline at higher rungs). Versioned, frozen, schema by elrond | Matt (plays) + capture instrument |
| **G3-B — Differential harness** | Replays each fixture's setup through the key into our sim; emits the same outcome metrics; computes raw deltas. Exists "in principle" per the hand-off; not written | gamora |
| **G3-C — Fidelity report + tolerance verdict** | Raw deltas per unit block (per Q47-DEFERRED-EMPIRICAL: **no pass/fail until Matt rules the bar against real numbers**), then per-rung verdicts once ruled; tuning loop iterates G2-B until the bar holds | gamora runs, gandalf verdicts, Matt rules the bar |

**Decision procedure:** goal 3 is DONE when the ruled bar holds at the highest rung whose
gating mechanisms (goal 1) are closed. Decidable — *after* two inputs exist that don't yet:
fixtures, and the empirically-ruled bar.

---

## 3. ★ NEW GAP — the second completeness surface

This derivation surfaced a hole in the current program frame, and it is exactly the
partial-view shape the week kept producing: **the 40-state table is the complete vocabulary of
monster *behavior*. It is NOT the vocabulary of combat *resolution*.**

A GD fight's outcome is behavior × resolution: damage types (physical/pierce/elemental/vitality/
aether/chaos + DoTs), armor absorption mechanics, resistances + reduction, **OA/DA hit
mechanics** (probability-to-hit, the crit-tier ladder), attack/cast speed, life steal,
retaliation, racial bonuses. These formulas live in **code, not in the `.arz`** — the `.arz`
carries their *parameters*. Goal 1 as currently instrumented (AI states) covers behavior only;
goal 3's differential will diverge on resolution formulas and the divergence would be
**unattributable** — the same confound the constraint ladder was built to kill, one layer down.

**The mitigation is cheap and digital:** GD's resolution formulas are extensively
community-documented (a decade of wiki/grimtools/forum derivation). A legolas Mode-A lane can
enumerate the resolution vocabulary into a **G1-A′ resolution coverage matrix** (the twin of
the state matrix), with each formula *validated against L0 fixtures* rather than trusted.
L0 was already the right first rung for the key; it is ALSO the right first rung for formula
validation — one melee monster, fight to death, is nearly pure resolution with minimal
behavior. **L0 does double duty and nothing about the ladder changes.**

---

## 4. The twin boundary — what is digital, what is not

| Side | Contents | Twin status |
|---|---|---|
| **DIGITAL (agent-side, frozen, bankable)** | Edition-II `.arz` corpus (hashed, byte-verified) · 40-state table + RTTI (exhaustive) · community-documented resolution formulas (§ 3, to be enumerated + fixture-validated) · the key (pure function) · our sim (fully controlled) · the differential harness · **banked fixtures once captured** | **IN the twin** |
| **LIVE-GAME (Matt-gated, finite)** | Fixture capture (the trials themselves) · inference confirmations (telegraph join, re-aggro semantics, spawn-impoverishment) · unit calibration (one WarpCursor trial) · rig determination (T9 items 1–3 answers) | **The oracle** — consumed in bounded sessions, each session's output banked into the digital side permanently |

**The load-bearing property:** Matt-hours are **front-loaded and finite per rung**, not
resident in the loop. Once a rung's fixtures are banked, an autonomous run can iterate
key + mechanisms against them indefinitely at zero owner cost. The twin *grows* rung by rung;
it is never blocked open-endedly on the live game. This is also why Q47's deferral composes
perfectly: L0 fixtures are the first oracle deposit, and they are simultaneously (a) the key's
first unit judgment, (b) the resolution formulas' first validation, and (c) the evidence base
for ruling the bar. **One small set of Matt trials feeds all three goals at once.**

**What the twin is NOT:** it does not replicate GD's *feel* (L5's "play feel" rung stays
human), it does not capture engine-side stochasticity beyond what fixtures sample (fixture
schema must record N-trial spreads, not single outcomes — elrond schema requirement), and its
behavior semantics are only as good as the confirmed inferences behind them (unbanked
inferences stay flagged, per this week's five-case record).

---

## 5. Desirable-run-pattern fit test — can a run be chartered?

Against `operating-procedures/desirable-run-pattern.md`:

| Requirement | Status |
|---|---|
| Bounded substrate | ✓ available: frozen corpus + state table + (future) fixture bank — all versioned, all hashed |
| Decidable target-state | ✓ derivable per § 2 — but **only after** G1-B, G2-A, and the Q47 bar are ruled |
| Elicited charter (intent residency) | ✗ not yet — the grill session (§ 6 items 6–7) has not run |
| Pre-registered gates + honorable fallback | ✓ pattern exists: ladder rungs ARE the gates; fallback = report raw deltas + halt at last closed rung |
| Veto-open ruling ledger | ✓ standing machinery |
| Matt interface declared | ✓ derivable: HALT at fixture exhaustion (new rung needs a PC session) and at bar-commitment; everything else in-run |

**Verdict: the twin supports a charterable run FAMILY — one run per ladder rung — after the
gap register below closes.** Likely first charter: **"L0-CLOSE"** — substrate = L0 fixture
set + frozen corpus; target = key at G2-A-ruled width reproduces L0 fixtures, raw deltas
reported, resolution formulas validated-or-flagged; conductor per pattern § 3 fit test.

---

## 6. Gap register — what must close before any charter (the elicitation/architecture list)

| # | Gap | Type | Owner | Status |
|---|---|---|---|---|
| 1 | **T9 items 1–3** — `game.Spawn` / `WarpCursor` / `PlayStats`: determines the entire rig shape (spawn-identity vs world-monster fallback; readout instrument) | Matt hands | Matt | SIMPLE sheet on the pi share now |
| 2 | **gamora 40-state audit** — converts G1-A from provisional to ground truth | agent | gamora | owed, dispatchable now |
| 3 | **★ Resolution-vocabulary enumeration** (§ 3 — NEW) | agent | legolas Mode A | needs commission |
| 4 | **Unit calibration** (G2-C) | Matt hands (one trial) | Matt + gamora | folded into T9 item 2 |
| 5 | **L0 fixture schema** — incl. N-trial spread capture | agent | elrond + gandalf | needs drafting |
| 6 | **G2-A key-domain grill** — gear? devotion? skill width? | elicitation | ELICITOR ↔ Matt | not scheduled |
| 7 | **G1-B combat-scope ruling** — the 7 non-combat states declared out | ruling (one line) | Matt | can ride the grill |
| 8 | **Q47 bar** — DEFERRED-EMPIRICAL; rules itself against L0 deltas | ruling, post-evidence | Matt | re-surfaces at first fixture bank |

**Sequence:** T9 probe → L0 trials + calibration (one PC sitting) → fixtures banked (schema
ready by then) → Q47 ruled on real deltas → grill session (G2-A + G1-B) → ARCHITECT
completeness pass → **charter L0-CLOSE**. In parallel, gaps 2 + 3 run agent-side now and
gate nothing.

---

*The twin and the deliverable are the same object; the live game shrinks to an oracle we
visit, not a dependency we carry. — gandalf*
