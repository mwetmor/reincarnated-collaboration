# Finding — 2026-07-31 — WR3 W-2 ENCOUNTER AI (phase 0 debt discharge + phase 2 build)

**Reviewer:** jack-ryan
**Severity:** **PASS with 4 WARN, 0 BLOCK**
**Target:** engine `f808b46d` (pushed). Prior consolidated Gate-2 covered through `dbb2d6a9`.
**Developer:** gamora (simulation seam). **Conductor:** gandalf (RUN-CONDUCTOR).
**Commission:** R-WR3-42(7) — Gate-2 on the W-2 landing
**Acceptance:** charter R-WR3-42 · rulings R-WR3-41(3) D3–D7 · R-WR3-12(W-2) · R-WR3-40(8)
**Principles applied:** 1 (math-before-code), 2 (smoke/full-regen gate), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity matters), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #8, #9, #10, #11, #12, #19/§19.2, #53, #63, #64, #65, #66, **#67 (minted here)**, Pattern P7, Pattern P8, ADR-002, ADR-004

> ### THE R-WR3-2 FULL-MIX ACCEPTANCE LAP IS **NOT GATED** BY THIS VERDICT.
> No WARN below blocks it. **One precondition attaches to its commission, not to this landing:**
> the stagger instrument (WARN-2) must exist before R-WR3-2 win rates are graded with W-2 armed,
> because without it the lap measures an outcome it cannot attribute to the mechanism it just
> armed. That is a scope line on the next commission, not a hold on this one.

---

## 0. Verdict summary

| Review item (commission) | Verdict |
|---|---|
| **1** — my own dispositions implemented faithfully | **PASS** — all three verified, two exceed the disposition |
| **2** — pin-scope discipline candidate | **RATIFIED as Discipline #67** — with a third founding instance I found in this landing |
| **3** — AI-D2-R1 tripwire actually trips | **PASS-with-WARN** — 0 violations measured across 1,024 flag combinations; the tripwire is arm-scoped, which is #67's own third instance |
| **4** — the four honest gaps | **2 WARN · 1 INFO-carry · 1 INFO** (dispositioned in §4) |
| **5** — G-I1 annotated-not-re-based | **PASS** — proven byte-reversible, not asserted |
| **6** — sweep integrity | **ATTESTED** — +1/−0 reconciles exactly; the +1 self-clears, verified post-commit |

**Landing quality, for the record.** Phase 0 discharged six debts and *upgraded two of them past what I
asked for*. The containment guard ships three protections I did not prescribe (stale-exemption expiry,
non-vacuity, artifact-annotation pin). The cell's own docstring declares its ablation gap in the first
thirty lines with the correct boundary drawn around it. G-W2-7 was reported as **NOT SAMPLED** with an
out-of-band probe distinguishing it from a dark mechanism — that is Pattern P8's remedy applied
unprompted, and it is the single best instance of the pattern I have reviewed.

**The four WARNs are all one shape: a number or a label that outran its basis.** None touches a
mechanism, a measurement, or a shipped behaviour.

---

## 1. Item 1 — were my dispositions implemented faithfully? **PASS**

### 1.1 §4.1(a) artifact annotation — **verbatim, verified by string equality**

Not accepted on report. Executed: parsed the `_DEFECT_worst_received_event_hp` value out of the
artifact, parsed the prescribed text out of my own finding doc, un-escaped the JSON quote, compared.
**`EXACT MATCH: True`.**

**Additive-and-reversible PROVEN for both artifacts, independently:**

| artifact | new top-level keys | pre-existing keys whose value changed | strip-new-key vs pre-edit |
|---|---|---|---|
| `wr3_stage2c.json` | `_DEFECT_worst_received_event_hp` | **none** | **byte-identical**, 11,484 = 11,484 |
| `wr3_anchor_refit.json` | `_INSTRUMENT_G_I1_reads_fight_length` | **none** | **byte-identical**, 16,345 = 16,345 |

Within seam-owner authority per **Discipline #53**; no re-base occurred.

### 1.2 §4.1(b) named allow-list entry — **PASS, and it exceeds the disposition**

`tests/test_measured_zero_containment.py` promotes `test_F2`'s sweep to all of `src/`, AST not grep,
with `wr3_cell_s2c_2026_07_30.py:88` as a named entry carrying a 5-sentence reason. **Three
protections I did not prescribe:**

- **`test_MZ2`** — every allow-list entry must still name a live site. A stale exemption fails. This
  is the self-executing form of my §E-10(c) expiry clause: when line 88 is struck at the next re-run,
  MZ2 fails and forces the entry's removal in the same landing. I wrote (c) as a hope; gamora made it
  a mechanism.
- **`test_MZ5`** — non-vacuity. The known live instance must be *found* by the sweep, not merely
  tolerated by the allow-list.
- **`test_MZ6`** — pins that the artifact annotation survives re-serialization.

**The scope measurement is the finding, and I am ratifying the narrowness.** Three predicates were run
against the live tree and the rejected two are recorded *in the file*: any-zero-default-getattr =
105 sites (a rewrite, not a rule); phantom-name = **0 sites**, because `worst_received_event_hp` is a
live grain-dict key at `kitcal_g5_harness.py:641` — *the detector is blind to its own founding
instance*; dict-key-as-attribute = 35 sites at ~3 % precision. A detector at 3 % precision gets
suppressed, not obeyed. Rejecting it was correct.

**INFO-1 (no action):** the result is a **watched-name** guard, not a general "unmeasured is not zero"
linter. The class can recur under a *new* field name until that name is added to
`_WATCHED_ABSENT_RESULT_FIELDS`. gamora states this plainly in the docstring. Recorded so a later
reader does not over-read the guard's reach.

### 1.3 WARN-1 MIGRATION paragraph — **landed; the magnitude is wrong. See WARN-1 (§2.1).**

The paragraph itself is *better than I asked for*: it names flag-OFF as a known-wrong default retained
for comparability, enumerates the affected consumers, points at the chartered ruling, and closes with
the consumer instruction. The **magnitude** is the problem, and it is a new finding.

### 1.4 An error of my own, recorded

Phase 0 item (2)+(5) also **corrected a false claim in MIGRATION §2(1)** — *"per-swing damage-event
count doubles"*, true only of the mob packet's effect list and **false at the trace boundary**, where
drax measured one damage event per swing on both arms (91 armed / 77 flag-OFF). A consumer correcting
for a doubling that does not occur **would have halved the boss's melee on screen.**

My prior verdict's §5 table records *"MIGRATION.md anchor-refit entry §§0–6 — READ IN FULL."* I read
it and did not catch this. Owner-eye #4 (drax) caught it by measuring the stream. **Discipline #11
cuts against the reviewer too:** reading a document is not inspecting the thing it describes.

---

## 2. The four WARNs

### 2.1 WARN-1 — the `1.64–1.89×` magnitude rests on a factor the seam itself retired

**This is the most consequential finding in the review, and it is on the ADR-004 surface.**

The new MIGRATION debt paragraph states the flag-OFF overshoot at **1.64–1.89×**, framed as a
measurement superseding my rounded "~2×". The table is internally consistent — but it is computed from
**×0.7517**, and `0.7517 / 0.86 = 0.8741` is precisely the factor the **anchor-refit note §3.3
explicitly retired**:

> *"That factor is **not** a mitigation term: `0.86` is already the whole cold-channel operator and
> `S = 1.0`. §4's figure is `0.86 × 0.874`, and **0.874 is a sample mean of `U(0.80, 1.20)`** — a low
> draw, not a model. §4 is corrected in §4 below with the measurement."*

Anchor-refit §4 then measures the shipped 100 %-cold row at **×0.8508** against a **×0.86** model
(−1.07 % agreement, uniform) and concludes *"OUR MITIGATION IS AT PARITY WITH THE REFERENT'S MODEL,
not 0.87× of it."* The correction repaired the **attribution** and did not restate the **magnitude**,
so the stale magnitude propagated forward into the W-2 MIGRATION entry.

**Computed this session across every consistent basis:**

| basis | T=43.1 | T=50.0 | T=60.8 |
|---|---|---|---|
| model / model (`0.86T` ÷ ref model) | 2.164× | 2.016× | **1.874×** |
| measured / model (anchor-refit `0.8508T`) | 2.141× | 1.995× | 1.854× |
| measured / measured (÷ `..._OWN_CELL`) | 2.210× | — | 1.911× |
| **shipped: retired `0.7517T` ÷ model** | **1.891×** | **1.762×** | **1.638×** |

**Every consistent basis gives 1.85–2.21×. Only the mixed basis — a superseded measurement over a
model — gives 1.64–1.89×.** The rounded "~2×" was right; the "precision upgrade" moved the number
away from the answer while telling the reader the opposite.

**Severity WARN, not BLOCK:** no code, no graded gate and no measurement consumes this figure; the
paragraph's *purpose* is fully discharged. But it is quotable, it sits on the cross-seam surface
ADR-004 exists to make sufficient, and its framing actively directs a reader to trust the wrong number.

**Remediation (one-line, gamora's next seam session):** restate the overshoot on a declared basis —
**model/model 1.87–2.16×**, citing anchor-refit §4's `×0.86` parity measurement — and strike the
`×0.7517` row. Also correct the framing sentence: the Gate-2 rounding was not superseded.
**Cited: Discipline #64** (basis form) **+ ADR-004 + Principle 3.**

### 2.2 WARN-2 — two of ten pre-registered gates are ungraded; one is ungradeable as built

Math note §5 pre-registers **ten** gates. The commit roll-up grades **eight**. The artifact's `gates`
block carries **eight**. Missing: **G-W2-5** (stagger exists) and **G-W2-10** (`ai_state` vocabulary
closed).

- **G-W2-10** is partly covered — `test_G1` pins that `AI_STATES` grew additively and that
  `W2_AI_STATES` is its tail. The gate's **emission-side** limb (*"every emitted `ai_state` ∈
  `AI_STATES ∪ {None}`"*) is not checked anywhere. Cheap to close.
- **G-W2-5 cannot be graded from what the cell emits.** The counter block is
  `[boss_dormant_at_t0, commit_beat_return, distress_calls_emitted, distress_calls_no_eligible_target,
  distress_responses_accepted, distress_responses_declined, dormant_at_t0, emotes_played,
  heal_on_return_hp, n_mobs, proximity_activations, pursuit_distance_exceeded, pursuit_timeouts,
  returns_completed, returns_started, social_activations]` — **there is no per-body engagement time.**
  `max(t_engage) − min(t_engage) > 0.5 s` is not computable from the artifact.

**Why this one matters more than its severity suggests.** G-W2-5 is the gate that would have verified,
*in the live simulation*, the thing the lap exists to build. The 2.15 s stagger width lives in the math
note's 200,000-trial static model (§2.3), which **declares its own limits** — it holds mob positions
fixed and therefore bounds the distress path from below. The live measurement was pre-registered, and
it was not taken. It is also the gate most exposed to gap 4: 403 of 463 calls reach nobody.

**Not BLOCK:** no false PASS was claimed — the gates were omitted, not graded green. Every
load-bearing claim of the lap (M1 fires, boss starts dormant, no heal, AI-D2 disjoint, flag-OFF
identity) is separately gated and passing. And the compliant shape was available and *used* elsewhere
in this same landing — G-W2-7's explicit **NOT SAMPLED**. This reads as an instrument oversight, not a
goalpost move.

**Remediation:** emit per-body `t_engage`; grade G-W2-5 and G-W2-10 explicitly, or declare them NOT
SAMPLED in G-W2-7's style. **This is the precondition on the acceptance-lap commission** named in the
banner. **Cited: Discipline #1 + #10 + #11 + Principle 1.**

### 2.3 WARN-3 — G-W2-4 is labelled PASS; on its own criterion it is NOT MET

Pre-registered criterion: *"accepted / (accepted + declined) within ±0.10 of the tier's B11 value
**over ≥200 rolls**."* Measured: **0.500 exactly** vs B11 0.50 — the value limb passes cleanly — at
**n = 60**. The power limb is not met.

**And it is narrower than "under-powered".** Rolls occur on **one tier of four**: trash 30/30;
boss, champion and mixed_pack each **0 accepted / 0 declined**. The artifact labels the gate
**(POOLED)**, which is honest but reads as *aggregated across tiers* when it is in fact *the only tier
that produced a roll*. The criterion names "the tier's B11 value" — three tiers' B11 (75 %, 75 %,
50 %) are unverified at any n.

gamora declared the n in the commit message ("UNDER the 200 pre-registered — PASS, under-powered, said
so"). **The honesty held; the label is what is wrong.** Pre-registration exists so a threshold cannot
be renegotiated after the data is seen, and "PASS, under-powered" renegotiates it.

**Remediation:** re-label to **CRITERION NOT MET ON n (point estimate on target: 0.500 vs 0.50,
n = 60, 1 of 4 tiers)**; carry the n-extension into the acceptance lap, which the conductor has
already scoped. **Cited: Discipline #10 + #11 + Principle 5.**

### 2.4 WARN-4 — the pre-registered per-mechanism arms do not exist, and two surfaces still say they do

Math note §5's table assigns every gate an **arm**: `M1-only`, `M2-only`, `M3-only`, `M1+M2`,
`M1+M2+M3`. **Those arms were not built.** `ARMS` in the cell defines two:

```python
#: The four arms. **`before` is the arm G-W2-1 grades against** and it is the ONLY arm that must
#: reproduce a banked figure; the other three are new measurements with no history to preserve.
ARMS: dict[str, dict] = {
    "before":      dict(wr3_encounter_ai_v1=False),
    "w2_armed":    dict(wr3_encounter_ai_v1=True),
}
```

The comment says **four arms** and **"the other three"**; the dict has **two**.

**The gap itself is declared excellently** — cell docstring lines 7–31 state it in bold, refuse to
paper it over ("*a real gap against Discipline #10's `change one thing`*"), substitute attribution by
measured non-participation, and — the part that makes it acceptable — **draw the boundary**:
*"WHAT WOULD STILL NEED REAL ARMS: any claim about M2's or M3's effect size, and any claim about
interaction between the three. This cell makes neither."* Verified: it makes neither.

**The defect is that the pre-registration document was not annotated to match.** A later reader
opening §5 sees an `arm` column naming single-mechanism ablations and will reasonably believe they
were run. **Cited: Discipline #12** (a plan that changes under execution is re-declared, not silently
diverged from) **+ #10.**

**Remediation:** annotate §5's arm column (*"NOT BUILT — attribution by measured non-participation;
see cell docstring"*) and fix the `ARMS` comment to say two.

---

## 3. Item 3 — does the AI-D2 tripwire actually trip? **PASS-with-WARN, and it is #67's third instance**

The commission asked exactly the right question: *is the repair for the pin-scope lesson itself
subject to the pin-scope lesson?* **Partly yes — and I measured it rather than reasoning about it.**

`test_F3` sweeps `S.build_scenarios(**_ARMED)` for any committing skill with `range_m >
VIEW_DISTANCE_M`. `_ARMED` is a **frozen 5-key literal** — `with_nova`, `gd_cadence`,
`boss_commit_v1`, `wr3_stage2_v1`, `wr3_stage2b_v1` — against a **12-parameter** `build_scenarios`
surface (also `r3_arm`, `s1_control`, `nova_tdm_arm_c`, `wr3_icearmor_enabled`,
`wr3_melee_split_v1`, `wr3_outgoing_stage_id`, `boss_dmg_per_hit`).

**The good news, and it is the decisive half.** `_ARMED` **does** include `wr3_stage2_v1` — the exact
arm whose calibration the W-1 fencepost was blind to. gamora pointed the new tripwire at the arm that
moved. That is the lesson correctly applied.

**Measured, all 1,024 boolean flag combinations swept against the F3 predicate:**

```
combos swept: 1024 | combos violating F3: 0
union of ALL committing-skill ranges across every combination: [2.0]
under _ARMED: committing ranges = [2.0] | all ranges = [2.0, 9.0, 10.0, 15.0, 18.0, 40.0]
```

**No live defect exists under any configuration.** `commit_beat_return = 0` on all four tiers is
corroborated structurally.

**The residual is future-coverage, and it is exactly #67.** `_ARMED` is a test-local literal. A future
`wr3_stage2d_v1` that arms a commitment on the shaman (18 m) or the nova (40 m) is **invisible to
`test_F3`**, because adding a flag to `build_scenarios` does not touch `_ARMED`. The same applies to
`test_E1` (the arena tripwire — a new arena behind a new flag is unseen) and to seven sibling tests.

**Cheap repair, and the pattern is already in-tree** — the `_door_opening_sites` /
`_MEASURED_ZERO_ALLOW_LIST` shape gamora just used: derive the arm set from the source's own surface
and assert coverage, so that widening `build_scenarios` **fails by name** until someone decides whether
the new flag belongs in the arm:

```python
_SCENARIO_FLAGS = {n for n, p in inspect.signature(S.build_scenarios).parameters.items()
                   if isinstance(p.default, bool)}
assert _SCENARIO_FLAGS - set(_ARMED) == _DECLARED_OUT_OF_ARM   # named, with reasons
```

Folded into the WARN-2 remediation. **This is the third founding instance of Discipline #67**, and it
is the one that carried ratification over the bar — *the repair for the defect reproduced the defect.*

---

## 4. Item 4 — dispositions on the four honest gaps

| gap | disposition | reasoning |
|---|---|---|
| **G-W2-4 under-powered** (n=60 vs 200) | **WARN** (§2.3) | criterion's power limb not met **and** single-tier; declared honestly, mislabelled |
| **G-W2-7 regime unreachable** | **INFO — carry, ride the acceptance lap** | see below |
| **No per-mechanism sub-flags** | **WARN** (§2.4) | the *gap* is declared correctly; the **pre-registration document** was not annotated |
| **Social aggro near-inert** (403/463) | **INFO** | design-lap observation, correctly framed |

### 4.1 G-W2-7 — *"is a mechanism that cannot be sampled in-battery acceptably 'built'?"*

**YES, in this instance — and the reason is a rule, not a concession.** The three things that would
have made this a WARN are all already discharged:

1. **It was not claimed as PASS.** Reported **NOT SAMPLED**. `pursuit_timeouts = 0` is the *exact*
   shape Pattern P8 says cannot be trusted, and gamora treated it that way.
2. **Dark-vs-unsampled was measured, not argued.** An out-of-band probe instrumented the accumulator
   across 10 fights/tier: peak continuous disengagement **0.50 s (boss) / 2.60 s (trash) / 0.50 s
   (mixed_pack)** against a 10.0 s threshold. **The timer runs, resets, and peaks at 26 %.** That is
   P8's founding pair — two mechanisms measuring nothing while their counters stayed plausible —
   discriminated by instrumenting the accumulator rather than reading the counter.
3. **Non-vacuity and the tripwire both exist.** `test_E4` fires the distance limb at 76 m, proving it
   inert by *geometry* rather than by being unimplemented; `test_E3` fires the timeout at exactly
   `PursuitTime`; `test_E1` asserts every arena diagonal < 75 m and **fails when an arena grows**,
   at which point assumption A-1 (home- vs target-relative pursuit) becomes load-bearing and must be
   resolved.

**The general rule, stated so this disposition is reusable:** a mechanism unsampled in-battery is
acceptably built when (a) its zero is reported as *unsampled* rather than *passing*, (b) the
distinction from a dark mechanism is **measured**, (c) non-vacuity is proven by construction, and
(d) a tripwire exists for the condition under which the regime becomes reachable. All four hold.
Absent any one, the same facts would be a WARN.

**Residual, recorded:** E3/E4 are unit-level on synthetic inputs. The *integration* path remains
unsampled and is the acceptance lap's kiting policy to sample. `test_E1` is arm-scoped (§3).

### 4.2 Social aggro near-inert — **INFO**

403 of 463 calls (**87.0 %**) reach an empty eligible set; boss/champion/mixed_pack are `emitted ==
no_eligible_target` exactly. **This is a confirmed prediction, not a defect** — math note §2.3 regime
A pre-registered *"the distress call is very nearly REDUNDANT"* for a closing player, and proximity
latches the reachable bodies before the 2 s call lands.

**The counter is the point.** Without `distress_calls_no_eligible_target` this would have read as a
healthy `emitted: 77`. gamora's own first smoke forced that counter into existence — **Discipline #63
clause (b)** working prospectively. Note the interaction with G-W2-3: its tri-state is satisfied on
**trash only**; the gate is labelled POOLED, which is honest but reads broader than it is (same note
as §2.3).

---

## 5. Item 5 — G-I1 annotation: **PASS, annotated not re-based**

Verified byte-reversible (§1.1): one new key, **zero existing values touched**. Arithmetic
re-derived independently: `12.1 / 36.007 = 0.33605` against the artifact's `3630 / 10802 = 0.33605`;
band `[0.30, 0.42]` ⇒ duration band `[12.1/0.42, 12.1/0.30] = [28.81 s, 40.33 s]`. Confirmed.

The strongest part is the **in-file self-refutation**: `B_anchor` and its `seed_matched_before_leg`
carry `icearmor_up_ticks = 3630` *identically* while `icearmor_total_ticks` moves 10395 → 10802 — so
uptime "changed" with the numerator provably untouched. The annotation closes with *"the gate's PASS
history STANDS as recorded; do not quote G-I1 as evidence the ward is behaving,"* which is the right
disposition: the reading is corrected without moving a graded number. **Moving it needs a ruling, and
that ruling is chartered to the RDR design lap.** Upheld.

**INFO-3:** §5's G-W2-10 row says *"the two new members appear"*; **three** were added
(`dormant`/`alert`/`return`). Cosmetic, in the pre-registration document.

---

## 6. Item 6 — sweep integrity: **ATTESTED, and the +1 independently re-verified**

Reported: 61F / 9973P / 21E in 22:09; name-diff **+1 / −0** vs the 81-name `dbb2d6a9` baseline.

**Reconciled arithmetically:** baseline 60F + 21E = 81 names → now 61F + 21E = 82 = 81 + 1. ✔
**Pass delta reconciled exactly:** 9973 − 9927 = **46** = +37 (W-2) + 6 (containment) + 3 (stage-2
fencepost arm) + 1 (vocabulary prefix) − 1 (the tracked-ness test). ✔

**Independently verified this session (not accepted on report):**

| check | result |
|---|---|
| `test_wr3_w2_encounter_ai.py` collected | **37** — matches the claimed +37 |
| `test_measured_zero_containment.py` collected | **6** — matches the claimed +6 |
| the +1 name (untracked-source detector) post-commit | **1 passed** — self-clears, as claimed |
| W-2 + containment + W-1 schema + BQ-3 door + anchor-refit | **147 passed in 11.85 s** |

**ATTESTED under Discipline #65.** The full 22-minute sweep was not re-run — that exceeds this
review's budget — but it is the compliant shape: run to completion without `-x`, diffed against a
**named** baseline commit with the artifact path recorded, and **independently reproduced by the
conductor**, who additionally verified the detector clears post-commit (44/44). Two independent
readers reaching the same name-diff is stronger than one re-run by me. The **+1 is not a regression**:
it is a detector correctly reporting the commission's own pre-commit unstaged state, which is the
detector doing its job. **No contest.**

---

## 7. Discipline ratification (ADR-002 direct authority)

### 7.1 **Discipline #67 — Pin scope: a pin must bind the surface that moves** — RATIFIED

Submitted by the conductor as the pin-scope rule. **Ratified as a new number**, on three instances.

**Why a number and not a merge.** The nearest neighbour is **#65** (full-sweep run law), and the two
are complementary rather than overlapping: **#65 catches a test that starts failing; #67 catches a
test that keeps passing for the wrong reason.** A full sweep would not have caught
`TestDF1Fencepost` — the test *passed*. #65's instrument is the name-diff, and a name-diff is blind by
construction to a green test that guards nothing. Nothing in #63, #64, #10 or #11 covers the *binding
surface* of a pin. Consistent with the six-numbers-not-minted record, I checked for a merge home first
and there is none.

**Three founding instances, one of which is the repair of another:**
1. `TestDF1Fencepost` — fixture-arm-scoped pin; durations moved under `wr3_stage2_v1`, an arm
   `_armed_boss_fight` never runs. **Did not fire**, though its own docstring promised it would.
2. `TestW1Vocabulary` — **the counter-example, in the same commit.** Fired **by name** when
   `AI_STATES` grew, because it pins a module-level constant in the source. Not diligence — surface.
3. **`test_F3` / `test_E1` + 7 siblings (found this Gate-2)** — the repair for instance 1, scoped to
   `_ARMED`, a frozen 5-of-12 flag literal. 1,024-combination sweep: **0 live violations**, so no
   defect — but the tripwire cannot see an arm added tomorrow.

Instance 3 is what carries it: **the repair reproduced the defect**, which is the property that makes
a rule necessary rather than a note sufficient.

### 7.2 **Discipline #64 extended — the `basis` form gains its second instance** — NO NEW NUMBER

WARN-1 is #64's existing basis clause recurring one level down: my prior §C caught pre- vs
post-mitigation units at the *constant* layer, and this is the same failure at the *derived-magnitude*
layer. Ratifying a new number for it would split one proposition across two.

**The extension states the propagation half, which #64 did not carry:** *when a correction retires an
operand or a factor, every magnitude derived from it is re-stated in the same landing.* Anchor-refit
§4 repaired the attribution (*"our mitigation is at PARITY"*) and left the magnitude computed with the
retired 0.874 standing in §3.3 and in AGENT_STATE — from where it propagated into a cross-seam
MIGRATION entry a lap later. **#58-DECLINED precedent applies.**

---

## 8. Independent verification performed (Discipline #11)

| check | result |
|---|---|
| `_DEFECT_` wording vs my §4.1(a) | **EXACT MATCH** by string equality |
| both artifact edits additive-only | **PROVEN** — 0 values changed; strip-new-key byte-identical both files |
| allow-list entry named + reasoned + live | **CONFIRMED** — MZ2/MZ3/MZ5 enforce all three |
| F3 predicate across the full flag surface | **1,024 combos swept — 0 violations**; committing ranges = {2.0} |
| `_ARMED` coverage of `build_scenarios` | **5 of 12 parameters** — the #67 residual |
| dormant R2 full-heal at `spatial_engine.py:1957` | **NEITHER ARMED NOR REMOVED** — `test_B3` pins the branch exists **and** `suppress_leash_hp_reset is False` |
| D1/D2 — anything built presuming full-heal? | **NO** — `HEAL_ON_RETURN_FRACTION = 0.0`; `test_B1`/`B2`; `test_B5` keeps `leash-return` ≠ `return` (avoiding a #66 conflation) |
| 1.64–1.89× arithmetic | **internally consistent with ×0.7517; ×0.7517 is retired** — WARN-1 |
| overshoot across 4 consistent bases | **1.85–2.21×** |
| G-I1 decomposition | **VERIFIED** to 5 decimals; band ≡ [28.81 s, 40.33 s] |
| W-2 counter block vs G-W2-5 | **no `t_engage` counter** — gate ungradeable as built (WARN-2) |
| §5 gates vs roll-up vs artifact | **10 pre-registered / 8 graded / 8 in artifact** (WARN-2) |
| G-W2-4 per-tier rolls | **trash 30/30; boss, champion, mixed_pack 0/0** (WARN-3) |
| `ARMS` dict vs its own comment | **2 arms, comment says "four"** (WARN-4) |
| test suites | **147 passed in 11.85 s** |
| sweep name-diff reconciliation | **arithmetically exact**; +1 self-clears post-commit |

**INFO-2:** `wr3_cell_w2_2026_07_31.py` docstring duplicates the *"NO `getattr(x, "name", 0.0)` IN
THIS FILE"* line at 33 and 35.
**INFO-4:** `test_F4`'s docstring claims it *"survives a referent-driven duration change"*; it asserts
`pytest.approx(1.368, abs=0.01)` and will fail on one. Failing is the *desired* tripwire behaviour —
the docstring is what is inaccurate.

---

## 9. Action

- [x] **jack-ryan:** ratify **Discipline #67** into `engineering-disciplines.md` — **DONE**
- [x] **jack-ryan:** extend **#64** with the basis-propagation clause + instance — **DONE**
- [x] **jack-ryan:** update the document-anatomy record — **DONE**
- [x] **jack-ryan:** decisions-log entry — **DONE**
- [ ] **gamora (WARN-1):** restate the MIGRATION overshoot on a declared basis (**1.87–2.16×**,
      model/model, citing anchor-refit §4's ×0.86 parity measurement); strike the ×0.7517 row; correct
      the "supersedes the Gate-2's ~2×" framing
- [ ] **gamora (WARN-2):** emit per-body `t_engage`; grade **G-W2-5** and **G-W2-10**, or declare them
      NOT SAMPLED in G-W2-7's style — **precondition on the acceptance-lap commission**
- [ ] **gamora (WARN-3):** re-label G-W2-4 to CRITERION NOT MET ON n (point estimate on target; n=60;
      1 of 4 tiers); carry the n-extension into the acceptance lap
- [ ] **gamora (WARN-4):** annotate math-note §5's `arm` column as NOT BUILT; fix the `ARMS` comment
- [ ] **gamora (#67, cheap):** derive `_ARMED` coverage from `build_scenarios`' signature with a named
      out-of-arm list, so a new flag fails by name
- [ ] **gamora (INFO-2/3/4):** docstring duplicate; "two new members" → three; `test_F4` docstring
- [ ] **gandalf:** carry the three sub-flags + G-W2-4 power extension + the **stagger instrument** into
      the R-WR3-2 acceptance-lap commission
- **Matt:** **no decision required by this verdict.** D1/D2 remain correctly queued at
  `canonical/matt_decision_needed/2026-07-31-wr3-w2-leash-departure.md`; **verified nothing built
  presumes them.**

---

## 10. References

**Reviewed:**
- `agentic_orchestration/gandalf/notes/2026-07-30-wr3-kite-commit-run-charter.md` — R-WR3-41 (1382–1438), R-WR3-42 (1439–1500)
- `agentic_orchestration/qa/findings/2026-07-31-gate2-wr3-kite-commit-consolidated.md` — my prior verdict
- `agentic_orchestration/legolas/research/2026-07-31-wr3-w2-aggro-leash-referent.md` — B1–B18

**Engine inspected (`f808b46d`):**
- `src/reincarnated/simulation/math/wr3-w2-encounter-ai-2026-07-31.md` (§§0–7)
- `src/reincarnated/simulation/math/wr3-anchor-refit-2026-07-30.md` (§3.3, §4 — the WARN-1 basis)
- `src/reincarnated/simulation/spatial_gauntlet/wr3_encounter_ai.py`
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (:1957 dormant R2 full-heal)
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py` (140–149; `build_scenarios`)
- `src/reincarnated/simulation/wr3_cell_w2_2026_07_31.py` (1–66)
- `src/reincarnated/simulation/MIGRATION.md` (W-2 entry §§0–4; anchor-refit debt paragraph)
- `tests/test_wr3_w2_encounter_ai.py` (37) · `tests/test_measured_zero_containment.py` (6)
- `src/reincarnated/simulation/output/kitcal_g5/wr3_w2/wr3_w2.json`
- `src/reincarnated/simulation/output/kitcal_g5/wr3_stage2c/wr3_stage2c.json`
- `src/reincarnated/simulation/output/kitcal_g5/wr3_anchor_refit/wr3_anchor_refit.json`

**Written this session:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #67, #64 extension, anatomy record
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — ratification entry
