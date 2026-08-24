# KC2-MC · **B-1r** — DRIFT-CRITIC verdict

**Author:** gandalf (`DRIFT-CRITIC`, named sub-agent) · 2026-08-24
**Build:** `7e8b02ad` + ADDENDA 1–3 (`a010c4ba` / `34839d3d` / `b7152552`); math note `84d507cb` ALONE.
**Sibling:** `E-s09-cp150-b1r` `6ac7c4e0…9786b11` · **Commission:** charter § 8 **L-30 / L-31 / L-34**.
**Rubric anchor (Matt verbatim):** *"the goal is to provide the baton which will allow the godot team
to immediately create a version of it that is playable as the character. This is why I want all
aspects present."*

⚠ **SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** The conductor authored the facet rulings, the hazard map
B-1r answers, and the L-34 launch text. This judging is seated OUT of the conductor's foreground and
the framing audit turns on the conductor in § 9.

---

## 0 · TOP-LINE

**PASS — with design findings. Eight (F-1…F-8), two of them live on a baton-bound value.**

B-1r is the best-instrumented cluster this run has produced. Every claim I re-derived, re-derived:
the `damageMagnitude` table is genuinely **parsed** from the D-4c README behind a digest pin with
both pulls required to agree and a HALT on disagreement (`dot_timeline.damage_magnitude_table`, not
a literal anywhere in engine source); the 6.2 s refire gate ships with 5.0 beside it labelled
`DECODED-BUT-INERT`; `gate_rolled: False` is on the wire at `control_states.py:803`; all thirteen
predicates hold; all four predecessors hash byte-identical. Four defects were caught by gamora's own
falsifiers and published ALONE above their repairs, and one of the four (`D-B1r-3`) is gamora
reproducing `WARN-3` on itself and saying so in a standalone commit. **That is what a build that can
be trusted looks like, and I want it on the record before the findings.**

**The findings are not about what B-1r built. They are about what B-1r's headline finding did NOT
finish.** `F-B1r-1` is correct and load-bearing, and its conclusion-survives claim is **true for the
two conclusions gamora tested**. But the sweep stopped one site short of the site that matters, and
the falsified clause turns out to be the **licence for the `CritLimb` HI limb** — a value the sim
runs at both ends and the baton will ship to Godot. At the pinned board the top two crit tiers are
reachable on **0 of 95 bodies**. Detail in F-1/F-2.

**Nothing here blocks B-2app.** Two items should be dispositioned before it launches (F-8, and the
MD-B1r-1 arm), and one is owed at the conductor's own desk (F-3's re-scope).

---

## 1 · Q1 — `F-B1r-1`: is "the conclusion survives on different ground" design-sound, and is a sweep owed?

**Answer: the claim is TRUE and I verified both surviving conclusions independently. The SWEEP IS
NOT COMPLETE, a fourth site exists, and it is the load-bearing one. A struck-with-revision sweep IS
owed at the conductor level — and it is WIDER than the three texts gamora repaired.**

**What I re-derived and confirms.** `data/kc2/pm4o_oa_da.csv`, 95 monster rows, `p2m_attacker_OA`
uniformly 3259.0: `p2m_pth_effective` runs **103.5368 – 124.8879 over waves 151–160** (the CSV
carries no wave above 160). `min(1, 103.5368/70) = 1.0`, so `HIT_CHANCE = 1.0` survives on its own
arithmetic. `player_offense.CritLimb` has exactly two members and the player damage path reads no
PTH-derived tier, so the +108 OA is inert **in this sim**. Both survivals hold.

### F-1 — ⚑ A FOURTH SITE CARRIES 149.2, AND IT IS THE ONE THAT LICENSES A MODEL VALUE. (WARN — Discipline #72 sweep miss)

gamora named three texts (`sustain_procs.ROW_DISPOSITIONS["fighting_spirit"]`, `CRIT_BASIS`,
`HIT_BASIS`). There is a fourth, at `player_offense.py:146-148` — the `CritLimb` **class docstring**:

> *"Against this board the player's PTH is 149.2-182.2 versus a top threshold of 135, so the top tier
> is REACHABLE on every body at every wave and the only open question is how often it is TAKEN."*

It was not swept, and it is not a provenance string like the other three — **it is the stated
justification for the shape of a live model value.** This is the run's fourth recorded value-set
sweep miss (L-28 INFO-4 noted the third). The sweep instrument keeps being *the three places I
remembered*, and the fix is mechanical: sweep on the FIGURE across the repo pair, not on the list of
sites the finding was found at.

### F-2 — ⚑ THE FALSIFIED CLAUSE IS THE `CritLimb` HI LIMB's LICENCE, AND THE LICENCE DOES NOT SURVIVE. (WARN — live fidelity defect on a baton-bound value)

`combatformulas` gives `pthThreshold1..6 = 70/90/105/120/130/135` and `pthDamageModifier1..6 =
1.0/1.1/1.2/1.3/1.4/1.5`. Measured across the 95 pinned monster rows:

| tier | reachable on |
|---|---|
| ×1.1 | 95/95 rows, max mass 15.00 pp |
| ×1.2 | 94/95 rows, max mass 15.00 pp |
| ×1.3 | **15/95 rows, max mass 4.89 pp** |
| ×1.4 | **0 / 95** |
| ×1.5 | **0 / 95** |

`p2m_expected_mult_given_hit` runs **1.0135 – 1.0597** across the whole board. Lap O's own findings
state it plainly (§ table, `×1.4 / ×1.5 tiers — 0.00 %`).

**The sim runs a bracket of 1.0 / 1.5.** The HI end is a tier the board cannot roll, and it was
licensed by the sentence F-1 found. `F-B1r-1` struck the clause and left the limb. Under the run's
own law that is not a survivable conclusion — the +108 OA's inertness survives, but the *bracket's
width* was resting on the same false figure and nobody has re-based it.

**Player consequence, which is the whole point of this run.** The terminal waves are 151/151/152/155/156
against Matt's 160. A crit bracket ~10× wider than the substrate permits is a large share of the
sim's own uncertainty on exactly the quantity the gap is about — and a Godot team reading Layer 1
would build a character whose crit ceiling is ×1.5 in a fight whose expected crit contribution is
**≈4.6 %**. That is not a bracket; it is a different character.

**Recommend (conductor disposition, not mine to rule):** re-base `CritLimb` against the pinned Lap O
tier-mass columns and collapse it toward `[1.0135, 1.0597]` per-body, OR keep 1.0/1.5 and record
*explicitly* that the HI end is known-unreachable and is retained only as a stress arm. Either is
defensible; silence is not. Rides the PM5 prereg as a named sensitivity, `report_only: true`.

**And note what this does to `D-L5`.** D-L5 declares *"no corpus field discriminates M1/M2/M3."* Lap
O — **pinned in `data/kc2/` since 2026-08-14** — implements the threshold-banded roll (M2):
`P(tier ≥ k) = clamp((P − T_k)/100, 0, 1)`, k=2 DOCUMENTED, k=3..6 DERIVED-BY-PARALLEL, mass
conserving to **0.000e+00 on all 190 direction-rows**. The premise "no field discriminates" is not
what is true; what is true is **"the discriminating evidence is documentation-grade, not
binary-grade"** — and given the standing display-layer guard, that distinction is exactly the kind
this run has learned to state rather than blur. Two different declarations, two different
dispositions. D-L5's text is owed a restatement.

### F-3 — ⚑ THE ROOT CAUSE IS NOT "A WEAKER BOARD." TWO PINNED ARTIFACTS DISAGREE ~2× ON MONSTER DA. (WARN — `C-B1r-2` is correctly filed and incorrectly scoped)

gamora's diagnostic reads: *"149.2 corresponds to DA ≈ 1168 against a board whose DA range is
2011–2770 — a substantially weaker board, carried forward without its predicate."* I re-derived it
and it is **not a different board**:

| artifact | monster DA, waves 151–160 |
|---|---|
| `data/kc2/pm4l_applied_damage_by_body.csv` (Lap L, 31,600 rows in window) | **64.0 – 1169.2** |
| `data/kc2/pm4o_oa_da.csv` (Lap O, 95 monster rows) | **2011 – 2770** |

Lap L's `defense_of()` (`research/scripts/pm4l_emit_2026_08_14.py`) composes DA as
`bio.characterDefensiveAbility` plus per-skill flats. Lap O decodes it as `da_level_term` (1236.0)
+ `da_attr_term` (344.6) + `da_flat_bio` (467.9) + flats, with a percent modifier — a sample row
resolves to 2174.875. **Lap L's composition omits the level term and the attribute term.** That is
why 149.2 exists. It is a *composition defect in a pinned artifact*, not a stale citation from a
different population — and the difference matters because a citation is repaired by re-quoting and a
composition defect is repaired by re-deriving a column.

**Blast radius, measured, so the finding is bounded rather than alarming:**

* **The sim is insulated.** `player_offense.chain_positive_control` reads `crit_multiplier` from the
  Lap L row on *both* sides of its comparison, so it cancels; the control tests the armour/resist
  chain and is unaffected. Live player damage uses `CritLimb`, not the CSV column.
* **The baton is not.** Every Lap L column downstream of DA — `PTH`, `hit_chance`, `crit_tier_max`,
  `crit_multiplier`, `expected_applied_per_rev`, `revs_to_kill` — inherits it, and
  `pm4l_applied_damage_by_body.csv` is a live Layer-1 candidate.

**`C-B1r-2` re-scope owed (conductor):** from *"re-derive Lap L's `L4-player-cannot-miss-this-board`
check"* to *"reconcile Lap L's DA composition against Lap O's decoded terms, and decide whether
`pm4l_applied_damage_by_body.csv` is baton-bound."* gamora was right to refuse to do it inside a
stacking build; the refusal is correct and the routing needs a wider target.

**Sweep verdict: YES, owed at conductor level.** Four items: (1) F-1's fourth site; (2) F-2's
`CritLimb` re-base + D-L5 restatement; (3) F-3's `C-B1r-2` re-scope; (4) the baton-bound decision on
the Lap L table. Items (1) and (2) touch a digested surface — see F-8.

---

## 2 · Q2 — `MD-B1r-1` grain fork: **DISPOSITION RECOMMENDED**

**Recommendation: RATIFY `PER_ROW` as the record limb. Keep `PER_SKILL` as the registered,
runnable, ungraded sensitivity. Do NOT commission a lap. Ship the fork as a baton-visible declared
open with the L-10 runtime-choice-ledger obligation attached.** Conductor's reasoning-boundary call;
this is my lean, stated as a lean.

**Does the substrate vote? Partially — and it votes PER_ROW.** D-4c's object trace puts the key's
second dword at `thisDamageAttribute->field_0x54`, where `thisDamageAttribute` is the **per-rider**
`DamageAttributeDur` object. A key read off a per-rider object is prima facie per-rider. D-4c was
right to refuse to *claim* it (the field could be a back-pointer to the owning skill), but a
refusal-to-claim is not a null vote — the pointer chain leans, and it leans one way.

**Materiality, measured on the frozen roster roll, so the fork is priced not argued.** Of the 16
records carrying multi-row keys:

| window | bodies | multi-row-record bodies | `(wave, record)` cells with >1 co-live body |
|---|---:|---:|---|
| 151–156 (sim's terminal range) | 120 | 11 (9.2 %) | 2 |
| **151–160 (the referent window)** | **188** | **13 (6.9 %)** | **3** |
| 151–170 (full roll) | 344 | 26 (7.6 %) | 6 |

Against gamora's worked divergence of **4.87 % per application** (`basilisk_acidbarf`), the fork's
whole reach is ≈7 % of bodies × ≈5 % of their DoT delivery — a fraction of a percent of DoT intake,
which is itself a fraction of total intake, **inside a quarantine that grades none of it.** A
legolas seat spent here while B-2app is the critical path is a seat spent on a rounding term.

**What each arm does to the fidelity claim.** `PER_SKILL` introduces NEW semantics on 18 undecoded
keys (MAXing rows that currently ADD). `PER_ROW` introduces none — it is the incumbent grain, so new
semantics land only where the decode is complete. **Under decode-before-declare the arm that changes
behaviour on an undecoded question is the arm that needs a licence, and neither arm has one.**
PER_ROW is therefore the arm that costs the model nothing it hasn't already spent.

**What each feels like at the Godot layer — my lane, and it is not a tiebreak, it is a third
independent vote.** Take gamora's own case: `basilisk_acidbarf` is `SlowPoison` **631.5 hp/s × 2.0 s
AND 35.0 hp/s × 5.0 s** — a designed **spike-plus-tail**. Under `PER_ROW` the player sees the spike
land and then a low tail that keeps ticking for three more seconds: *you are still burning; break
off.* Under `PER_SKILL` the tail is swallowed by the MAX for its first two seconds and the burn ends
abruptly at t=2.0 — the readable signal that the author of that record wrote is **deleted by the
grain choice.** DoT tails are how an ARPG tells a player that disengaging is a decision (Diablo II's
Poison Nova taught this by having a tail long enough to matter; Diablo III's damage-over-time
rebuild lost it and never got the read back). `PER_ROW` preserves the authored shape. `PER_SKILL`
flattens it.

**Three independent votes, all PER_ROW, none of them the direction of effect** — and I note for the
record that PER_ROW is the arm that moves the sim *away* from wave 160, which is what makes the
designation credible.

**Do not close the ask.** `MD-B1r-1`'s named question is well-written and cheap to carry. It ships as
a Layer-1 declared open with `source_key_grain` stated, the arm named, and the L-10 obligation that
the Godot runtime record its own choice if it diverges. That converts a decode gap into a
runtime-ledger row instead of a lap — which is precisely the disposition class the run built the
ledger for.

---

## 3 · Q3 — `B1r-Q`: is quarantining survival until PM5 the right shape?

**Answer: YES, and it is a stronger instrument than B-1's `B1-P7` because the two shifts push
opposite ways. One refinement is owed at the W3 prereg, and it is owed NOW rather than at Wave 3.**

**Why publishing partial estimates would be wrong.** The DoT repair's direction is knowable a
priori (same-source ADD → per-bucket MAX ⇒ intake falls, survival rises). Publishing a number with a
knowable sign into the run's one live open question — *why 151–156 and not 160* — is how a run
acquires a preferred answer without anyone choosing it. The graded-not-gated ruling exists so the
terminal wave can be *read* rather than *passed*; a quarantined delta with both directions published
and neither netted holds that ruling's shape exactly. Netting them would be worse than either.

### F-6 — WAVE 2 IS PRODUCING SEMANTIC SHIFTS FASTER THAN THE PREREG IS TRACKING THEM. (INFO — prereg item, generalises B-1's F-5)

Four Discipline-#12 shifts have landed in Wave 2 (B-1's circuit-breaker evaluation-point repair ·
B-2's control delivery · B-1r's DoT MAX · B-1r's Resilience window), each with an a-priori direction,
and **the W3 prereg carries none of them.** L-26 accepted a named `pilot_divergence` row for the θ
caveat; the general form is owed: a **`semantic_shift_ledger` row set** in the PM5 prereg,
`report_only: true` per L-9, one row per Wave-2 shift with its a-priori direction and its build.
Otherwise PM5 grades a terminal wave with four known-sign contributors and a prereg that names one.

---

## 4 · Q4 — Refusal audit: `C-B1r-1`, the inert cooldown, and one under-labelled refusal

**`C-B1r-1` (Ulzaad `+190` flat armour → intake seam): CORRECT refusal, correctly priced, and it does
NOT starve the baton.** The mechanism argument is real — `intake.armour_table(global_flat)` is a
pinned per-region MEASURED table whose fold-off byte identity is what I-23/I-24's inertness proofs
rest on, and threading a dynamic duty-cycled addend into it inside a stacking lap is how a proof
breaks where nobody is looking. The uptime is published so the deferral is priced, not asserted.
**And the +190 still ships to Layer 1 as a decoded row with its composition named** — the *aspect is
present*; only the sim-side fold is deferred. That is the L-26 layer distinction working as designed.

**The inert 5.0 s cooldown: not merely correct — this is the pattern the run should adopt.**
Shipping a real record value labelled `DECODED-BUT-INERT` **with its governing gate beside it** is
the precise shape of Matt's "all aspects present." Omitting 5.0 would have let a Godot team re-read
the record, find the cooldown, and build the ~24 %-over-firing proc — the model's silence would have
been the bug. Same class: refusing to normalise `uniform_int(0,100) <= 30` to 30 % when the binary
delivers 30.693 %. **Recommend `DECODED-BUT-INERT` join the S-1 `sim_disposition` vocabulary** — my
B-2 Q2 answer already established `sim_disposition` as an axis orthogonal to `provenance`, and this
is its second inhabitant after `UNREACHABLE_BY_PRIOR_REFUSAL`.

### F-4 — ⚑ `DECLARED-NOT-FOLDED` IS A **SIM** DISPOSITION WEARING NO LAYER QUALIFIER, AND FACET (d) IS NOT CLOSED. (WARN — coverage + export)

Two things, one root.

**(a) The E.4 argument must not be inherited by Layer 1.** Ascension's `+38 %`, Fighting Spirit's
`+95 %`, Tip the Scales' leech, Ulzaad's offensive/retaliation limbs all ship
`DECLARED-NOT-FOLDED` on I-4 § E.4 — *"the player-damage limb of record is a character-SHEET reading
whose buff composition is undecidable."* **That premise is a property of the SIM's damage limb and
it evaporates at Layer 1**, because a Godot runtime computes damage from the kit, not from a sheet
number. These are aspects, and Matt asked for all aspects present. The rows must carry a Layer-1
disposition distinct from their sim disposition; as shipped, a Wave-4 emitter reading
`DECLARED-NOT-FOLDED` will reasonably read *absent*.

**(b) `UNBUILDABLE`-empty is not facet-(d)-closed, and the ledger headline risks laundering it.**
The checkpoint's own `⚑ unbuildable_after_d6` is `{}` — true. But `row_dispositions` shows
`ascension: PARTIAL` with two named unfolded limbs, and `fighting_spirit` / `ulzaads_decree` likewise
moved `UNBUILDABLE → PARTIAL`, not `→ IN_MODEL`. **This is B-2's F-5 vocabulary hazard arriving
exactly where predicted**, and it is the B-1 F-2 lesson's third recurrence. *"The UNBUILDABLE table
is now EMPTY"* is true; *"facet (d) closes"* is not.

**Coverage-matrix answer (Q5) follows from this — see § 5.**

### F-5 — A ZERO-COUNT SITE IS ABSENT FROM THE LEDGER RATHER THAN PRESENT AS A ZERO. (WARN — wire truth; third instance of one class)

`B1r-P3` holds and H-4 is literally satisfied (all three `resolve_attack` sites exercised at least
once across the ensemble — `toggled_aura` fires on salt 1 only, 9 registrations). But the shipped
`registrations_by_site` **omits the key** on the salts where a site registered nothing:

```
salt 3  sites {'main': 6}          # dying and toggled_aura are ABSENT, not 0
```

The math note registered *"or is reported as an exercised-zero with its own count."* A consumer
reading salt 3 cannot distinguish *"toggled_aura registered zero DoTs"* from *"toggled_aura was not
instrumented on this salt."* **This is B-2's F-1 exactly — carried-not-rolled with no field that says
so — reproduced in B-1r's own ledger, and it is the third instance of the missing-field-that-declares
class in this run.** Cheap repair: emit all three keys always, zeros included. Rides B-2app's brief.

### F-7 — THE ORDINAL LADDER IS GENUINELY LIVE, WHICH VALIDATES SHIPPING THE TABLE. (INFO — positive)

`max_instances_in_a_bucket` reaches **5**, and `n_ordinal_ge_1_seen` reaches **1,495** on salt 1.
Shipping `damageMagnitude` as a table + `min(i, N−1)` + descending sort + `/100` is not a
principled gesture at a value that happens to be neutral — the ladder is walked five deep on real
buckets. If Crate ever ships a non-neutral table (or a mod does), this model reads it correctly
without a rebuild. **This is the single most baton-valuable thing in B-1r** and it deserves to be
said in the Layer-1 row's own prose, not just in the math note.

---

## 5 · Q5 — Coverage matrix (facet × layer), L-26 gate

**Facet (d) — Menhir's Will + devotion procs**

| cell | status | owner |
|---|---|---|
| SIM · sustain half | **CLOSED** — Menhir IN_MODEL, Resilience IN_MODEL (full rank-3 payload on the decoded 5 s/15 s window), Fighting Spirit schedule IN_MODEL, Ulzaad schedule IN_MODEL | B-1 + B-1r ✅ |
| SIM · offense/armour half | **OPEN** — Ascension ±38/39 %, FS +95 %, Tip-the-Scales leech (E.4) · Ulzaad `+190` armour (`C-B1r-1`, intake seam) · Ulzaad offensive/retaliation limbs | intake cluster + a named E.4 disposition — **no owner assigned** |
| BATON · Layer 1 | **OPEN** — and needs F-4(a)'s layer-qualified disposition field before it can be emitted truthfully | Wave-4 emitter |
| BATON · Layer 2 | OPEN | Wave-4 emitter |

**1 of 4 closed.** `UNBUILDABLE`-empty closed the *decode* gap; it did not close the facet.

**Facet (i) — fleeing · dodging · distress · swing-pause · emotes · DoT stacking**

| cell | status | owner |
|---|---|---|
| SIM · DoT stacking | **CLOSED** — decoded rule implemented, `MD-B1r-1` a declared open with a runnable sensitivity | B-1r ✅ |
| SIM · swing-pause | **CLOSED** by decode at D-3 (`IGenerate(min,max)` ms re-rolled per swing) — *carry the F-7 standing guard: re-derive at the build that consumes it* | D-3 → B-6 |
| SIM · fleeing / dodging / distress / emotes | **OPEN** — D-3 decoded them; B-2 confirmed Fleeing-inert on stronger ground; dodging (42/169, projectile-reaction) and distress have no build owner | **B-6, unassigned** |
| BATON · Layer 1 (rules + parameters) | **OPEN** — this is the facet Matt re-ruled *specifically* so a live runtime gets the rules; the 100 ms bucket clock, MAX/ADD, the `damageMagnitude` hook (F-7), the truncation rule, `rand()%101` (D-3), the swing-pause re-roll all land here | Wave-4 emitter |
| BATON · Layer 2 | OPEN | Wave-4 emitter |

**2 of 5 closed** (with a third resting on a D-3 declaration that owes an F-7 re-derivation).

**What remains owed on the BATON side for Wave 4 — the short list, both facets:** a layer-qualified
`sim_disposition` field so `DECLARED-NOT-FOLDED` / `DECODED-BUT-INERT` / `UNREACHABLE_BY_PRIOR_REFUSAL`
read correctly at Layer 1 (F-4a) · the `UNBUILDABLE` / `PARTIAL` vocabulary harmonisation (B-2 F-5,
still open) · the `source_key_grain` declared-open row + its runtime-choice obligation (§ 2) · the
`CritLimb` re-base or explicit known-unreachable annotation (F-2) · the baton-bound decision on
`pm4l_applied_damage_by_body.csv` (F-3).

---

## 6 · Q6 — Composition hazards for **B-2app**

B-2app lands control APPLICATION beside `dot_timeline.py`. D-7 decoded that the fixed lane and the
DoT lane are the **same `DurationDamageManager` at `Character+0x3e4`, sharing the same 100 ms bucket
container** — and that the fixed lane's aggregation law is the **opposite convention**. **Ten
hazards, in priority order.**

**J-1 — ⚑ ONE CONTAINER, TWO LAWS, AND THE SOURCE ENGINE'S OWN SHARING IS THE TRAP.** DoT lane:
key `(damage_type, ATTACKER)`, same-source **MAX**, distinct-source **ADD**, all timelines live
concurrently. Fixed lane: key is the **FAMILY on the target**, same-family **LONGEST-WINS**, never
additive, and **exactly one involuntary effect at a time** by the priority ladder. Two stuns from two
bodies must **not** ADD. A builder who reads D-7's "same manager" sentence will reach for
`dot_timeline._Entry` / `_Instance`, and will inherit per-attacker keying and additive aggregation —
**both wrong, and both would present as a plausible-looking control duration.** *Rule for the brief:
SHARE the bucket-clock primitive; DO NOT share the entry/instance aggregation. The engine shares a
container, not a law.* This is B-1r's H-1 one lane over, and it is the single most likely defect.

**J-2 — THE PER-ENTRY ACCUMULATOR PHASE, AND WHETHER Stop-old/Start-new RESETS IT.** B-1r decoded
(`AddDamage`, `+0x1c` zero-init) that each DoT entry carries its **own** 100 ms phase, and refused a
global clock because it would manufacture coincidences. Does a control entry allocate the same way —
and does the ladder's Stop-old/Start-new **re-allocate**, resetting phase on every family swap? The
difference is whether a 0.2 s stun is 2 buckets or 1 bucket plus a partial. Decodable from functions
D-7 already read. State it with the RVA or declare it; do not inherit B-1r's answer.

**J-3 — TRUNCATION IS THE NORM IN THIS LANE, AND ZERO-DURATION IS A LANDING, NOT A SILENCE.** B-1r
proved truncation is *exactly zero* on its corpus (all `dot_duration_s` tenth-multiples). **That
proof does not transfer.** D-7's control path truncates **after** the resistance scalar —
`duration × (1 − r/100)` then `(int)(s·10)` — so non-tenth-multiples are the norm (gamora's worked
1.25 s @ r=79 → 0.2625 → **0.2**). And `duration ≤ 0` is never inserted: a sufficiently-resisted
control **silently does not land**. That must reach the wire as a *landing with zero delivered
duration*, not as absence — B-2's own `applied:False` self-declaration principle applied to a new
zero-shape. Pre-register a truncation census; do not assert a zero term.

**J-4 — ⚑ B-1r JUST MADE THE PLAYER'S RESIST WINDOW INTERMITTENT, AND CONTROL DURATION IS A
FUNCTION OF RESIST.** This is the composition nobody has named yet. B-1r folded
`defensiveAllMaxResist +2 %` and `defensivePhysical +4 %` **gated on a 5 s window / 15 s cooldown**.
D-7's duration scalar reads `defensive<X>` + the `defensiveCrowdControl = 25` SUM, clamped at
`playerDefenseCap` (seat `+0x3690`). **Question B-2app must answer BEFORE it builds: does
`defensiveAllMaxResist` raise the cap the control family clamps against?** If YES, stun duration
becomes a function of a devotion proc's duty cycle — a live facet-(d)↔facet-(e) coupling created one
build earlier. If NO, publish the negative with its RVA. This is the F-7 guard pointed *forward*
instead of backward, and it is the first time the run has needed that.

**J-5 — CHANNEL-OFF IS BY STATE REPLACEMENT, AND THE PLAYER'S ENTIRE DAMAGE MODEL IS A CHANNEL.**
D-7: a landing control `SetState`s out of `UseSkill` and **does not resume**. The sim's EoR is a
channelled spin whose damage model is the *one-hit-per-tick identity*. So every landed control costs
**the remainder of the channel plus re-acquisition** — a cost that is **not proportional to the
control's duration**. A 0.2 s truncated stun can cost far more than 0.2 s of output. **B-2app must
publish channel re-acquisition cost as its own quantity, separate from control duration**, or the
model under-reads the cost of control by construction. *At the playability layer this is the whole
difference between "stuns are an annoyance" and "stuns are why you died"* — and it is the row a Godot
team most needs to feel the fight correctly.

**J-6 — THE LADDER NEEDS A STOP; `pop_front`-ONLY RETIREMENT HAS NONE.** B-1r's timeline retires
monotonically and drops in-flight at wave end (I-15 A3, inherited not re-argued). The fixed lane
needs an active family's timeline to be **stoppable mid-burn** by a higher-priority family
(Immobilize > Petrify > Freeze > Trap > Sleep > Stun > Knockdown > TakeHit, first-hit-wins,
Stop-old/Start-new). D-7 does **not** state whether the stopped family's remaining buckets are
**discarded or suspended-and-resumable**. "First-hit-wins" hints discard; a hint is not a decode.
**If it stays undecoded, refuse and declare — do not pick.** B-2's own limb-E refusal is the
precedent and the standard.

**J-7 — LONGEST-WINS NEEDS A COMPARISON THE DoT LANE NEVER MAKES, AND `no refresh` MAKES IT
ORDER-DEPENDENT.** Same-family LONGEST-WINS with **no refresh**: a 3.0 s stun at t=0, then a 1.0 s
stun at t=2.0 — is the comparison against **remaining** (1.0 vs 1.0) or **nominal** (3.0 vs 1.0)?
D-4c's per-bucket MAX is remaining-agnostic and gives no guidance. ⚑ **The bucket-list representation
probably answers it for free** — a longer new duration simply extends the bucket list and a shorter
one adds nothing, which *is* longest-wins, computed rather than branched. **If that identity holds,
state it: it converts a rule into a representation and is very likely why the two lanes share a
container.** The hazard is implementing it as a scalar `if new > old: old = new`, which silently
diverges on partial overlap.

**J-8 — THE DECODED ZEROES MAKE B-2app's OWN PREDICATES VACUOUS ON THE RECORD CELL.** Confusion,
Fear and Taunt are **player no-ops** (shared `ret` stubs); Convert has no player-side consumer. And
**Confusion is the only family B-2 ever observed landing (2/2).** So on the record ensemble B-2app's
application path will be exercised by nothing, and every application predicate will pass by
emptiness. **Pre-register that the application lane is exercised on a SYNTHETIC probe** — a forced
Stun landing with a known duration and a known resist — or B-2app ships an untested lane wearing a
green. This is `D-B1r-5` inverted: not a predicate that convicts correct code, but a predicate that
acquits absent code. Compose with F-7: the Confusion no-op re-derives at B-3 (summons sit outside
the 169-roster sweep).

**J-9 — POPULATION, AND NOW THE DENOMINATOR ITSELF MOVES.** B-1r declared P-A/P-B/P-C. B-2app adds a
fourth: control **applications**, which is B-2's delivered observations filtered by a gate that
B-2app is the build that finally **rolls**. ⚑ **The moment `gate_rolled` becomes `True`, B-2's
131-row census and its 2-in-562 price stop being the same measurement.** F-8-of-B-2's dated-claim
discipline fires: B-2app re-derives the price on its own basis and **cites nothing from B-2's**.

**J-10 — THE DIGESTED-SURFACE PROSE DEFECT IS NOW THE RUN'S MOST-REPEATED, AND B-2app IS THE NEXT
BUILD THAT WILL ADD BASIS STRINGS.** Three instances: B-1's `devotion_envelope_disclosure` (F-1),
B-2's scope label (WARN-3), B-1r's `CRIT_BASIS`/`HIT_BASIS` (`D-B1r-3`). B-2app will want
`SUPPRESSION_BASIS`, `LADDER_BASIS`, `TRUNCATION_BASIS` — and F-1/F-2 of *this* verdict now owe
edits to that same surface. **Recommend the `C-B1r-3` schema decision (a `_surface()` filter
excluding provenance prose, or version-marked additive keys) be pulled FORWARD from Wave 4 to
BEFORE B-2app.** It is a small S-1 ruling and it is currently generating one defect per build.

---

## 7 · DISPOSITION

**PASS.** B-2app is clear to launch on the technical surface. Carried into its brief: **J-1…J-10**,
plus the F-5 zero-count-key repair. Two conductor items owed alongside, neither blocking: the F-1/F-2/F-3
sweep (which needs J-10's ruling first, or it reproduces `D-B1r-3` a fourth time), and the F-6 prereg
row set. `MD-B1r-1`: my recommendation is `PER_ROW` ratified, no lap, declared open with the runtime
obligation — conductor rules.

## 8 · ⚠ THE FRAMING AUDIT TURNS ON THE CONDUCTOR

**C-1 — the L-34 launch text says *"the `UNBUILDABLE` table is now EMPTY"* and does not say what is
still `PARTIAL`.** That is the conductor's own sentence, written from gamora's headline, and it is
the exact laundering F-4(b) names. L-26 amended the coverage gate into a facet × layer matrix and
L-34 reported a build against the *old* vocabulary — **the second time this run the conductor has
amended a gate and then narrated against the pre-amendment frame.** The B-2 verdict's C-1 said
*"L-26 amended the gate and not the brief"*; this is the same failure one turn later, in the ledger
rather than the brief. Repair, and it is mechanical: **every Wave-2 ledger row carries its facet's
cell line.** Three lines per row. I recommended this at B-2 Q1(c) and did not do it in L-34.

**C-2 — the hazard map worked, and the conductor should notice why.** H-1 and H-5 were both LIVE and
both would have shipped as plausible numbers. What made the map work was that it named a *mechanism*
and a *measurement* per hazard rather than a concern. J-1…J-10 are written to the same standard, and
J-4 is the first forward-pointed instance — a hazard created by the build two clusters back rather
than inherited from the surface. That is the shape the remaining Wave-2 briefs should take.

---

*DRIFT-CRITIC verdict, gandalf, 2026-08-24. Judging seated out of the conductor's foreground per the
L-23 pattern. Committed, not pushed.*
