# Finding — 2026-09-21 — Run KC2-PLAY, discipline ratification 2

**Reviewer:** jack-ryan
**Mode:** RATIFICATION (not a gate) — Run KC2-PLAY is in a deliberate hold; graded run #2 withheld pending two oracle reads and a Matt ruling
**Severity:** WARN (two implementation defects in candidate C's reference enforcement; no BLOCK, nothing graded touched)
**Target:** godot `de3c279` + `699e38d` · engine `10705dda` (prior landing) · `gamora/notes/2026-09-21-kc2-play-ta-grade.md` (`df2dc1188`)
**Proposers:** drax (C) · gandalf `RUN-CONDUCTOR` (D) · gamora + drax (E)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #4 (decisions-log as truth), #5 (severity matters) · ADR-002 process-tier, Matt-veto open
**Canonical write:** LANDED in the same pass — see § 5

---

## 1. Rulings

| cand. | proposition | ruling | number |
|---|---|---|---|
| **C** | *a choice registered against the wrong absence is camouflage* | ⚑ **ADOPT**, minted in derived-class form; **one of three proposed clauses REJECTED as already existing** | **#84** |
| **D** | *a pin is an audit instrument, not a gate* | ⚑ **AMEND** — the proposition is already in the corpus; the **remedy** is new and lands as a clause | **#75 cl. 1(a)** |
| **E** | *a band whose numerator counts per-wave events over a per-tick denominator is confounded with survival* | ⚑ **ADOPT**, generalised to the invariance form; family enumeration **named OPEN** | **#85** |

Corpus state **derived, not recalled**, per **#79** cl. 1, before any number was assigned: highest existing `#83`; `#77` vacant-by-contamination; `#84` and `#85` free. **#72** citation sweep across all three repos: **1 hit, 0 premature first-party citations** — `decisions-log.md:6793`, the row recording `#84` as *declined* for the empty-fixture candidate. Benign historical prose, left unedited per **#64** NAME FORM cl. 4, with a disambiguation stated in the new log entry.

---

## 2. Candidate C — ADOPT as #84

**Minted as:** *A declared absence is a LICENCE WITH A SCOPE — a choice registered against it NAMES the behaviour it authors, and if the wire declares that behaviour the choice is camouflage.* drax's headline sentence is carried verbatim inside the entry.

### 2.1 The corpus answer the conductor asked for

**The core proposition is NOT in the corpus, and drax identified the gap correctly.** The corpus governs absences three ways and all three sit on the **declaring** side:

| number | what it governs | reaches candidate C? |
|---|---|---|
| **#63** + **#63(c)** | how an absence is **read and emitted** — no zero default, no prose attestation | **no** — nothing was collapsed into a measured zero |
| **#70** | whether a **source's population boundary** was established | **no** — different actor, different direction |
| **#49** | what substrate **silence** may be disposed as | **no** |
| **#64** | a **name** must declare its referent | ⚑ **the near miss, and it fails**: `ABS-TARGET-SELECTION` declared its referent honestly and correctly |

⚑ **None governs the LICENCE an absence grants a CONSUMER** — the authority to author a value the wire does not carry, and the scope of that authority. An absence-registry architecture carrying only #63/#70/#49 is complete on the declaring side and unguarded on the consuming side, which is the side that writes behaviour. That is a real hole and it takes a number.

### 2.2 ⚑ But ONE proposed clause IS in the corpus — and it is the proposer's own

The positive control — ***"a guard that only ever refuses is indistinguishable from a broken registry"*** — was routed as a novel clause and flagged as discipline-grade in itself.

**It is `#78` cl. 3, and `#78` is drax's, proposed by him on 2026-08-24 from his own `totem` gate:**

> *"Specificity is proven on known-positives, exactly as sensitivity is proven on known-negatives (#75 cl. 2). Before a gate's conviction is acted on, run it against an artifact known to be correct and require it to acquit. **A gate that has only ever been shown to convict has demonstrated that it fires, not that it discriminates.**"*

`#78`'s headline is *a gate is not safe merely because it is strict*. drax re-derived his own rule one month later and did not cite it — **#79** cl. 1, fired at a builder's seat this time, and the **#80** cl. 6 precedent applies exactly: *independent re-invention is evidence the corpus HAS a rule and nobody derived it before proposing.*

⚑ **The conduct is a CREDIT and is recorded as one.** #78's own Gate-2 question asks whether the gate was *shown to acquit a known-correct artifact*. drax's answer is not a validation run someone remembers — it is an assertion in the suite (`tests/kc2rt_rules_smoke.gd:246-268`) that **re-proves itself on every execution.** That is better than #78 requires. **Only the citation was missing.** Landed as **#78 founding instance 4** — the first on a *refusal* gate rather than a threshold gate, and the first where the specificity proof ships as a permanent assertion. **Not duplicated into #84.**

### 2.3 ⚑ Two defects in the enforcement — derived by inspection, not taken from summary

Both **WARN**. Neither touches a graded artifact: `699e38d` ran no T-A and emitted nothing graded.

**Defect 1 — `authors` is documented REQUIRED and is optional in code, with a green test asserting the opposite.**

The claim appears in the commit body, in the source comment at `kc2_runtime/loader/kc2rt_absence_ledger.gd:80-82`, and in the candidate's own headline: *"a guard evadable by leaving a field blank is a naming convention."* The code:

```gdscript
func register_choice(absent_ref: String, choice: Variant, chooser: String,
		rationale: String, authors: String = "") -> bool:      # :113 — optional, defaults ""
	...
	if authors.strip_edges() != "" and _guarded.has(authors):  # :123 — fires only when NON-empty
```

There is no emptiness branch. And `tests/kc2rt_rules_smoke.gd:234-235` **asserts that a four-argument call SUCCEEDS**:

```gdscript
_ck("a well-formed runtime choice is accepted",
    l.register_choice("ABS-X", 0.285, "drax", "registered u, ledger KP-6"))
```

So the requirement is not merely unimplemented — **a green test asserts its negation.** Governing rules: **#80 cl. 3** (*a fix ported in prose is a fix that reads as adopted; an asserted parity does not get checked*) and **#63(c)** (*a prose attestation is `get(k, 0)` written in English*).

**Defect 2 — the guard's population is opt-in; 7 of 13 production registration sites are invisible to it.**

Derived mechanically over every `ledger.register_choice(` in `kc2_runtime/` excluding tests. Population **13**:

- **WITH `authors` (6):** `sim/kc2rt_fight.gd:438` · `:489` · `:519` · `:535` · `:544` · `:554`
- ⚑ **WITHOUT (7):** `sim/kc2rt_fight.gd:506` · `sim/kc2rt_register.gd:468` · `:485` · `sim/kc2rt_vectors.gd:105` · `sim/kc2rt_oracle_config.gd:175` · `:216` · `kc2rt_pack.gd:221`

The guard is armed over 6 of 13 registrations, **structurally blind to 7, and reports nothing about them.** **#80** (a guard not shown to reach its population) · **#82 cl. 1** (the population is part of the claim).

⚑ **And the correct pattern is in the SAME commit pass, applied to a different object.** Defects 1+3 of the repair pass were one defect: `configure_arm` consumed a hand-picked tuple of scalars, so any limb outside it was structurally invisible — the dropped one was `movement_policy_wrap`, and **one un-consumed limb produced both the three-way arm collapse and all four red motion bands.** drax fixed it by *making the class impossible rather than the instance*: `limb_consumption_audit()` requires every declared limb to be **consumed or declared-unconsumed BY NAME, and refuses the cell otherwise.** **He then built the camouflage guard with an optional field — a hand-picked set of registrations, the identical shape one object over.**

**Why this is load-bearing and not cosmetic, and why it shaped #84 cl. 2:** the founding defect was **not** an author hiding an excess. It was an author who **did not realise the behaviour he was writing was declared on the wire.** The check that catches him is the one that forces him to *say what he is authoring*. ⚑ **An optional field does not force articulation — and the author least aware of what he is authoring is precisely the author who leaves it blank.** That is the entire population the guard exists to reach. **#80** cl. 6's asymmetry, at the registry layer: *the honest registration names its behaviour and gets checked; the camouflaged one names nothing and sails.*

---

## 3. Candidate D — AMEND, not a new number

⚑ **The proposition is already in the corpus, at `#75` cl. 1:**

> *"Bind the shipping instance, not the authored object. A probe reads the artifact at the layer that produces the outcome under test — the instance that draws, the pixels that render, **the file the consumer opens**."*

And #75's one-line summary is *"inspect the artifact that ships, not the one you authored"*; its own cross-references already claim the pinning case as generalised into it from **#67**. A revision pin binds an authored object; the artifact that ships is the working file the builder opens. **That is cl. 1, exactly.**

**So the honest answer to *"am I over-reading one miss?"* is: over-reading it as a NEW DISCIPLINE — yes. Over-reading the DEFECT — no.** And the proposer's own hedge was the correct call: *"the candidate may be narrowing what a pin claims rather than adding a rule."* Ratified as stated.

**What IS new is the remedy**, and the corpus does not mint numbers for remedies to rules it already holds. Landed as **#75 cl. 1(a)**: *nobody reads a pinned revision; they read the file — so the builder declares the revision he built against, and the pin is checked against that statement.* A pin left to itself is one-sided by construction: it records what the reviewer examined and is silent on what the builder opened, **and the two diverge with neither party doing anything wrong.**

**Bounding case carried into the clause, because it matters:** the pins in this run **did** work — three moves were caught by re-deriving them. cl. 1(a) **narrows what a pin CLAIMS**; it retires nothing.

**The conductor's not-a-HALT ruling is upheld** (nothing in those commits moved a row). The exposure is recorded per **#81** cl. 6 — name the backwards set even where every member discharges: a builder obeying the `P-e` pin would have measured every band on a board **216–273 bodies/arm lighter**, and it did not happen **only because drax read the current file, which is normal practice and not a compliance act.** The pin's stale coverage annotation is a **separate** defect, already correctly ruled **#82 cl. 2**, and is now recorded there as **cl. 2 instance 4** per **#72** — the first instance on a pin's own annotation.

---

## 4. Candidate E — ADOPT as #85

**Minted as:** *A cross-implementation acceptance band is a claim about INVARIANCE — enumerate what the two implementations may differ on, and show the statistic does not move with it.* One-line summary is gamora's own, verbatim: *a band pinned without its construction specified tightly enough to bind a second implementation.*

**The mint argument is this corpus's own merge doctrine** — two halves are one number only when satisfying one cannot be mistaken for satisfying the other. Run the nearest neighbours against `TA-B-07`:

| neighbour | its demand | met at the founding instance? |
|---|---|---|
| **#80 cl. 2** | don't calibrate against one denominator; don't pool across scales | **met** — single-row, unpooled, `D` printed |
| **#82 cl. 1** | state the set at the site of the number | **met** — and gamora **re-derived it correctly** |
| **#64** FRAME FORM | operator, instrument, scene, geometry on the same line | **met** — every physical condition travelled |

⚑ **What did not travel is the CONSTRUCTION, and that is a third detection method** — neither re-derivation (blind to it) nor labelling (#82 cl. 2's method), but *asking what the statistic is invariant to*. By the doctrine above, a third detection method is a third rule.

**Three founding instances + one:** `TA-B-07` and `TA-B-02` (gamora's, against her own width file — and they are **one row with a sign flip**, `released/D ≡ 1 − uptime` exactly); ⚑ `TA-B-03` (drax's, **unflagged by anyone at the grade** — reaching the oracle's ~14.6 % stationary would need ~650 ticks where 10 transitions × 16 ticks caps it at 160). Plus `TA-B-06` as cl. 2's instance: the window was never specified; the seal uses one 5 s window per wave, the port tiles the run, **and neither party is wrong.**

⚑ **The enumeration is NAMED OPEN, not back-filled** (**#79** cl. 1). Three instances plus one establish the class; they do not establish its extent. **If it returns most of the counted bands, the finding is that T-A's band half is measuring survival with extra steps — and that lands as a fourth instance class UNDER #85, not as a new rule.** Until it returns, no coverage claim is made.

⚑ **The do-not-tune-toward-the-band limb is NOT minted here — it is `#78` cl. 1–2 and already binding**, whose founding instance is *a correct effect detuned until a broken instrument approved of it*. drax was correctly told not to tune `frac_moving` toward `TA-B-03`'s band; that instruction is already law. Carried as a cross-reference per **#58-DECLINED**. **A band is not a law: where a declared law and a measured band disagree, the law governs and the band is the finding.**

---

## 5. Canonical write — LANDED IN THIS PASS

The ratify-then-land gap is closed here rather than deferred.

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
  - **#84** minted (3 clauses, founding instance, enforcement inventory, both WARN defects carried **in the mint**)
  - **#85** minted (3 clauses, 3+1 founding instances, open-enumeration declaration)
  - **#75 cl. 1(a)** added
  - **#78** founding instance **4** added; instance-count header amended 1–3 → 1–4
  - **#82 cl. 2** instance **4** added (per #72)
  - anatomy bullet added
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — trigger entry per that file's extend protocol step 5, including the ⚑ **#84 disambiguation** (the `#84` *declined* in the earlier entry today is the empty-fixture candidate, which became `#80` cl. 6; the `#84` minted here is drax's absence-licence rule — the number was free at both writings, only the first candidate for it was refused)

---

## 6. Action

- [ ] **drax — before graded run #2 (WARN, not a gate on this commit):** make `authors` mandatory in `register_choice` and refuse the blank; pass `authors` at the **7** named sites or declare each unnamed by explicit exception. **The pattern is your own** — `limb_consumption_audit()`'s *consumed or declared-unconsumed BY NAME, else refuse the cell.* A graded run under a guard blind to 7 of 13 sites banks the guard's green as evidence (**#80**).
- [ ] **drax — citation only:** your positive control is **#78 cl. 3**, your own discipline. Nothing to change in the code; it is now recorded there as founding instance 4.
- [ ] **gamora:** the `#85` family enumeration is **open and routed to you**. It may sharpen cl. 1's scope; it will not change the number.
- [ ] **gandalf `RUN-CONDUCTOR`:** `#84`, `#85` and `#75 cl. 1(a)` are **citable now**. The `C1` candidate is an amendment, not a number — cite `#75 cl. 1(a)`, never `#86`.
- [ ] **Matt — no decision required; veto open** on all three per ADR-002 process-tier.

## 7. References

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #84, #85, #75 cl. 1(a), #78 inst. 4, #82 cl. 2 inst. 4
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — 2026-09-21 trigger entry
- `~/Games/reincarnated-godot/kc2_runtime/loader/kc2rt_absence_ledger.gd` :77-141 · `sim/kc2rt_oracle_config.gd` :430-466 · `tests/kc2rt_rules_smoke.gd` :230-268 · `sim/kc2rt_fight.gd` :438-561
- `~/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-09-21-kc2-play-ta-grade.md` — `TA-B-02/03/06/07`, `C1`
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` — ledger KP-41…KP-45
