# KC2 — sweep-law graduation + Gate-2 corrigenda touch (jack-ryan)

**Date:** 2026-08-08
**Agent:** jack-ryan (analyst / QA / quality guardian)
**Commission:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, ruling **R-L65-3** (ledger row L-65)
**Status:** CLOSED — 5/5 items disposed (see § Dispositions); Discipline **#72** minted
**Authority:** ADR-002 process-tier (documentation / discipline / decisions-log), Matt-veto open
**Constraint:** corrigenda-forward everywhere; no silent self-healing; commit both repos, **DO NOT PUSH** (conductor centralizes under R-KC2-10)

## Commissioned items (five)

1. **§ 6.5 SWEEP-LAW GRADUATION ASSESSMENT** — count recurrences, rule whether the fifth-recurrence trigger is met; draft the MECHANICAL-ENUMERATION graduation candidate (two corroborating instances in two artifact classes: CODE L-63(a), DATA L-65(j)); my call on landing form (new discipline / clause on existing / QUEUED candidate with named landing trigger).
2. **F-2 ANNOTATION** — F-2 (INFO, +77 test-count anomaly) is WITHDRAWN-BY-EVIDENCE per L-63(c). Annotate verdict record; PASS verdict untouched.
3. **F-1 COMPLETION ANNOTATION** — priced 5-line hit list closed at 8 engine lines. Annotate verdict record.
4. **#70 FOUNDING INSTANCE COUNT** — minted text cites 2 rows; mechanical re-resolution found 6. Corrigenda-forward decision.
5. **CONSUME kc2set_verdicts_v2.json** — verify `_meta` satisfies my #69 clause (i) declared-equality-predicate requirement. Finding, not repair, if it fails.

## Log

### L1 — Inputs read (all five, in commission order)

Ledger L-63 / L-64 / L-65 (full row text) · legolas consolidated-record-touch § 10 + § 11 ·
`operating-procedures/desirable-run-pattern.md` § 6.5 (whole file, 87 lines) · my minting note +
the landed #69/#70/#71 text (engine lines 3209–3331) · my Gate-2 locomotion-lap verdict
(`2026-08-08-kc2-gate2-locomotion-lap.md`, findings F-1 at :196 and F-2 at :262).

### L2 — Independent verification, not summary-acceptance (#11)

I re-measured every claim the commission asserts. Results:

**(a) The CODE-class instance — CONFIRMED, and the mechanism is sharper than "one line below."**
`git show a5382e65:tests/test_kc2_locomotion.py` — the pre-correction function
`test_the_N_sensitivity_perturbation_scale_is_READ_from_F_13_not_chosen()` carries a
**three-assertion block**:

```
:565  assert cal.F13_MEASURED_FLOOR_REGULARS == 289.62        <- I TABULATED THIS (F-1 hit 4)
:566  assert cal.F13_MODEL_OF_RECORD_REGULARS == 271.50       <- benign (unchanged operand)
:567  assert cal.F13_N_PERTURBATION == pytest.approx(1.0667, abs=1e-3)   <- I MISSED THIS
```

`|1.0667 − 288.62/271.50| = |1.0667 − 1.063057| = 0.003643 > 1e-3` ⇒ **the five-site repair would
have left the test RED on its third assertion with the first two green.** Confirmed by my own
arithmetic, not gamora's.

**The mechanism is NOT ignorance.** My own F-1 body names the derived constant explicitly: *"the
executed sweep ran at 1.0667 / 0.9333 … under the corrected floor the sweep runs at 1.0631 /
0.9369."* I traced the derivation, printed both values, and **never added `1.0667` to the grep
set.** The sweep was executed over the changed value's spellings (`289.62`); a value *derived from*
the changed value is not a spelling of it, and § 6.5 as ratified does not require the set be closed
under derivation. That is the gap.

**(b) The DATA-class instance — CONFIRMED, but the commission's characterization needs correcting,
and the correction matters for what graduates.** Measured over `kc2set_verdicts.json` v1:

| set | rows | ABSENT-BOTH |
|---|---:|---:|
| (2b) summon bodies | 15 | **2** |
| (5) L-58 mechanism-chain records (path-guessed) | 17 | **13** |
| all other sets | 595 | 0 |
| | 627 | **15** |

My L-62(d) enumeration covered set **(2b)** and found **2 of 2 — COMPLETE within its declared
population.** The other 4 legolas found sit in set **(5)**, whose staleness was *already declared*
in the set name itself and already re-resolved in his prose (that is #70 founding instance 3, the
*positive* instance). So this is **not** an enumeration-by-eye miss inside my own set.

The real lesson is a **different joint of the same operation**: having found a stale-path defect in
one subset, I did not widen the sweep to the artifact's other ABSENT rows — even though 13 of them
were sitting one key away, flagged as path-guesses. **A defect found in a sample is a hypothesis
about the population.** #70 required me to *declare* my boundary (I did); nothing required me to
*move* it once I found rot inside it.

**(c-pre) The `+77` decomposition — CONFIRMED against my own F-2, which was WRONG.** My F-2 table
counted `test_baton_v1.py` at 49→82 (+33) and asserted *"parametrize count is 0 → 0 in all four
non-locomotion files, so there is no hidden expansion there."* That assertion is **false**: I
applied collected-node counting to the locomotion file and `def test` counting to the baton file,
in the same table. 35 + 41 + 1 = 77, exactly. My residual of 2 was an artifact of my own
mixed-method arithmetic. F-2 is WITHDRAWN-BY-EVIDENCE — see § D2 below.

**(d) The 8-line F-1 closure — CONFIRMED on disk.** Residual `289.62` in the engine tree now
appears at exactly four sites, **all four corrigenda or retired-value assertions**:
`tests/test_kc2_locomotion.py:566` (corrigendum docstring) · `:576`
(`F13_MEASURED_FLOOR_REGULARS_SUPERSEDED_AT_L52 == 289.62` — retirement asserted, not remembered) ·
`calibration.py:950` + `:969` (same pattern) · plus corrigendum banners in `AGENT_STATE.md:25` and
the math note `:412–415`. Zero live consumers. gamora took the *first* of the two options my F-1
prescribed **and** the second (SUPERSEDED sibling) — both, not either.

### L3 — Item 5 finding: the v2 artifact PASSES the equality clause and FAILS on the absence axis

See § D5. Headline: `_meta.equality_predicate` satisfies #69's *"name the equality predicate"*
requirement **better than the fulldiff instrument does** (it un-folds `IDENTICAL` vs
`IDENTICAL-FIELDS` instead of collapsing them). But **8 of the 9 rows headlined "genuinely ABSENT"
carry `resolution: AMBIGUOUS-2` — the resolver found two candidates and declined.** I measured all
16 candidates: **16/16 IDENTICAL II↔III.** The carry-forward verdict is determined without
resolving the join.

---

## Dispositions

### D1 — § 6.5 SWEEP-LAW GRADUATION: **TRIGGER MET. GRADUATED. Discipline #72 MINTED.**

**Recurrence count: SEVEN.** The trigger asks for five.

| # | recurrence | era |
|---|---|---|
| 1 | founding BLOCK **D2-1** — four stale sites the landing fold walked past | law-construction (→ clause 1) |
| 2 | live-tense extension — two sites the value-only patterns missed (L-47(f)) | law-construction (→ clause 2) |
| 3 | **R-3** hand-back residual in a seam the sweeper could not edit (L-49) | law-construction (→ clause 3) |
| 4 | false discharge-by-assertion (**L-43(f)**) | law-construction (→ clause 4) |
| **5** | **Gate-2 F-1 (L-56)** — 5 line-hits the L-52 hand-back missed | **LAW IN FORCE** |
| **6** | **L-63(a)** — hit table 5 → 8; a live pin two lines below a tabulated one | **LAW IN FORCE** |
| **7** | **L-65(j)** — enumeration of 2 vs mechanical population of 6 | **LAW IN FORCE** |

**RULING.** The trigger fired at **L-56** exactly as the conductor declared, and has since been
corroborated twice more in two different artifact classes. But the count is not what decided the
landing form — **the Era-1/Era-2 split is.** Misses 1–4 each *produced a clause*: the law was
**under-specified**, and guidance is the right home for a rule still learning its shape. Misses 5–7
produced **zero** new clauses; every one was already covered by text binding at the time. **A law
that recurs without generating new clauses is not under-specified — it is under-enforced.**
Under-specification is a documentation problem and belongs in a pattern doc that says *"deviating is
a judgment call to be named."* Under-enforcement is a behavior problem and belongs in a discipline
with triggerable Gate-1/Gate-2 questions. **That is the boundary § 6.5 pre-registered the fifth
recurrence to detect, and it detected it.**

**LANDING FORM: new discipline #72** (number verified free in both repos; **#58** stays vacant per
its DECLINED ruling; number assigned at landing per the **#60** precedent). Rejected alternatives,
with reasons, are in the decisions-log entry. Two matter enough to restate:

- **QUEUE is WRONG here, and my own #69 precedent says so.** #69 was legitimately queued because its
  founding instance *at the required granularity did not yet exist* and its trigger was falsifiable
  and forward-looking. Here the trigger has already fired **twice over**. Queueing a candidate whose
  pre-registered condition is met is deferral wearing discipline's clothes, and it would leave
  § 6.5's closing line pointing at a graduation that never happened.
- **The commission's drafted proposition needed narrowing, twice, and I narrowed it.** *"Enumeration
  must be MECHANICAL, never by eye"* is **necessary and not sufficient** — item 5 of this same
  commission found a **mechanical** instrument under-reporting 8 rows because it stopped at an
  ambiguity. So #72 carries **clause 6, mechanical does not license narrow**, alongside clause 5.
  And the **derived-value limb is NOT #72's** — it is **#64**'s BASIS FORM propagation clause,
  binding since 2026-07-31, and L-63(a) lands there as its **third founding instance** per the
  **#58-DECLINED** precedent. Minting it twice would split one proposition across two numbers.

**Not merged into #65** — same deep structure (*the author's enumeration is not the verdict object; a
mechanical full-set diff is*), different layer. #65 is the test suite at a landing boundary, where a
runner produces the diff; #72 is value propagation across consuming surfaces, where the set must be
**constructed** — which is exactly where clauses 6 and 7 bite and #65 has nothing to say.

**Matt surface honored.** § 6.5's own text routes the graduation to *"Matt surface, via jack-ryan."*
Minting is ADR-002 process-tier (mine), but I have **not** treated this as self-approved: the
discipline header, the decisions-log Status line, the § 6.5 banner and this note all flag it to
Matt's eye with veto open. The routing is mine; the ratification surface is his.

**Self-indictment, recorded because it is the strongest evidence in the file.** Miss 6 was committed
**by me**, against **#64**'s clause, binding for eight days, **inside the finding that named the
sweep failure**. Miss 7 was committed **by me, four hours after minting #70**, the discipline about
declared boundaries, on the artifact supplying #70's own instance 4. The failure mode is structural,
not a diligence gradient — the sentence **#71** already carries.

### D2 — F-2: **WITHDRAWN BY EVIDENCE.** Annotated; PASS untouched.

`+77` = baton **+35** (51 → 86 collected) + locomotion +41 + micro-oracles +1. Exact. My residual of
2 was `test_r_loco_1_arena_ref_guard_has_teeth` expanding 1 `def` → 3 node IDs.

**The error is worth its own line, because it is the class I was auditing.** My F-2 table applied
**collected-node** counting to one file and **`def test`** counting to another, in the same column,
and then discharged the gap **by assertion** — *"parametrize count is 0 → 0 in all four
non-locomotion files"* — which is false. Discharge-by-assertion is what § 6.5 clause 4 forbids,
committed by the reviewer citing § 6.5 two findings earlier. A `--collect-only` on both trees closes
it in one command. **#65** already owns the prescription (*reconcile `+passed` to a collected
count*). Verdict untouched: F-2 was INFO, required no developer action, and no binding claim rested
on it.

### D3 — F-1: **UPHELD AND EXTENDED.** Annotated with the 8-line closure.

Three beyond my table: `test_kc2_locomotion.py:567` (second live pin — the load-bearing one), math
note `:370`, `simulation/AGENT_STATE.md:25`. gamora took **both** limbs of my prescription, not
either: value corrected **and** retired value asserted-as-retired. Re-verified at this fold: four
`289.62` sites survive in the engine tree, **all four corrigenda or retirement assertions, zero live
consumers**. The § 8.4 rows deliberately not restated — true measurements at the scale named beside
them, corrected scale *inside* the executed one, envelope conservative. Correct call, and **#12**
done properly. My work-class limb (*"note edit" was mispriced*) is confirmed by outcome and is now
**#72 clause 8**.

### D4 — #70 founding instance 4: **CORRIGENDUM, count 2 → population 6.** Text left standing.

Landed as a block-quote corrigendum under instance 4 in the discipline itself, **and** at the
decisions-log minting entry's Status line — the same two-site treatment I gave the L-60 entry, and
the rule I enforced on others four hours earlier.

**The correction is not a simple count bump, and flattening it to one would be wrong.** My
enumeration was **complete within its declared population** — set `(2b)`, 2 of 2 — and the four
additional rows sat in set `(5)`, whose staleness was already declared **in the set's own name**
(`path-guessed; ABSENT means path differs`) and already re-resolved in prose at instance 3. **So
#70 was satisfied on both sides.** What was missing is the obligation #70 does **not** carry: a
defect found inside a declared subset is a hypothesis about the whole artifact. An honestly-declared
boundary tolerates rot outside it indefinitely. That is now **#72 clause 7**, founding instance 7 —
and it is why the corrigendum re-frames rather than merely re-counts.

Noted in the corrigendum: the record among the four that matters most is **`swampcrab_crabgenerator`
itself** — the keystone of the entire L-58 crab-generator argument — reported ABSENT-BOTH by the
stale artifact and in fact **IDENTICAL across editions**. *The note said so; only the instrument
lied.*

### D5 — `kc2set_verdicts_v2.json`: **PASSES the equality clause. WARN on the absence axis.** Finding, not repair.

**Citation precision first (INFO).** The commission cites *"#69 clause (i)."* As minted, clause (i)
is *"Editions, not updates"*; the equality-predicate requirement is #69's **fourth statement
bullet**. No substance turns on it; recorded so the mis-citation does not propagate.

**PASS — and better than the instrument it supersedes.** `_meta.equality_predicate` declares
`IDENTICAL` = *same fields + same normalised values + same owner list* and `IDENTICAL-FIELDS` =
*same fields + same values, different owner list*. I read `lib2.diff_rec` and confirmed the
declarations are **exact against the implementation**. This is materially stronger than the
`fulldiff.py` fold that collapses both via `startswith("IDENTICAL")` — it un-folds precisely the
consumption-vs-provenance distinction #69's fourth bullet was written about. **Clause satisfied.**

**WARN — three defects, all on the absence axis, none on the equality axis.**

- **D5-1 (substantive).** **8 of the 9 rows headlined "genuinely ABSENT" carry `resolution:
  AMBIGUOUS-2`.** `kc2set_v2.py:27` returns the *original* path on ambiguity, which `diff_rec` then
  grades `ABSENT`. Only **1** row (`skeletalgolem_a01`, zero candidates) is a measured absence.
  **Declining an ambiguous join is CORRECT (#71).** Grading the decline as a substantive verdict
  token is **#63** at the verdict-token layer.
- **D5-2 (and it makes D5-1 free to fix).** All 8 ambiguities are the same shape:
  `…/devotion/<name>.dbr` vs `…/hero/<name>.dbr`, both present in both editions. I diffed **all 16
  candidates: 16/16 IDENTICAL II↔III.** **The carry-forward verdict is therefore determined over the
  candidate set without resolving the join** — which is **#69**'s descend-before-invalidating applied
  to a namespace ambiguity. The artifact reports the most pessimistic verdict available where the
  answer is actually determined. **True figure: 621 IDENTICAL / 5 CHANGED / 1 ABSENT** (627 rows).
- **D5-3 (minor).** `_meta` declares the token `ABSENT-BOTH`, which appears in **zero** rows'
  `verdict` field (only in `verdict_v1`), and omits `ABSENT`, which appears in nine. Separately,
  *"normalised values"* does not state its normalization (`lib2.norm` rounds floats to 6 dp) —
  **#64**.

**Severity WARN, not BLOCK**, because the error runs in the **safe** direction — it under-claims
carry-forward, never over-claims it — and the 8 rows are attribution-grade L-58 mechanism-chain
records that nothing in the baton or the calibration consumes. **Escalation trigger named: this
becomes BLOCK if any claim is ever made ON those 9 rows** (e.g. *"9 records absent from both
editions"* used as evidence).

**NOT REPAIRED.** legolas's artifact, legolas's seam. The correction is fully specified above so the
re-emit is mechanical: relabel the 8 declines `UNRESOLVED-AMBIGUOUS`, emit the per-candidate verdicts
beside them, restate the headline as **621 / 5 / 1**, add `ABSENT` to the `_meta` predicate block and
state the float normalization.

---

## Disposition of this touch

**All five items CLOSED.** Discipline **#72** MINTED (Matt surface flagged, veto open) · **#64**
third basis instance added · **#70** instance 4 corrigendum landed at two sites · F-1 and F-2
annotated corrigenda-forward with the PASS verdict untouched · v2 artifact consumed with one WARN
filed and routed, not repaired.

**Not done, deliberately:** no push (R-KC2-10, conductor centralizes) · no edit to legolas's note or
artifacts (his seam; the WARN is routed with the fix specified) · no re-run of `n_sensitivity()` (the
deferral is gamora's and is correctly reasoned) · § 6.5 text **retained, not superseded** — it is the
lineage record of what the law cost to learn, and its Era-1 construction *is* #72's founding
evidence.

**Status: CLOSED.**

