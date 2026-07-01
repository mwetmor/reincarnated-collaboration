# Governance ratification — S15 note-prune refinement + ARCHITECT-effectiveness ledger (jack-ryan rulings)

> **STATUS:** CURRENT (verdict-class lineage per canonical-doc-format § 6.1). The durable home of jack-ryan's disinterested ratification of two gandalf-proposed governance instruments. Cited by the two decisions-log candidate entries filed the same day.

**Authored:** 2026-06-30
**Author:** jack-ryan (Analyst / QA — governance rule-RATIFIER per Matt 2026-06-30, canonical-doc-format § 6.7)
**Authority:** Matt 2026-06-30 role-separation verdict (`gandalf/notes/2026-06-30-role-separation-verdict.md § 3`) — doc-lifecycle governance rule-ownership routes to jack-ryan by symmetry with engineering-disciplines; gandalf proposes + executes, jack-ryan ratifies.
**Companion:**
- `gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md § 4` — S15, the proposal under review (ITEM 1)
- `agentic_orchestration/architect-effectiveness-ledger.md` — the rubric under review (ITEM 2)
- `operating-procedures/canonical-doc-format.md § 6` — the installed governance system S15 amends
- `gandalf/notes/2026-06-30-role-separation-verdict.md` — the authority that routed both to me

---

## 0. TL;DR

Both instruments are **RATIFIED WITH ONE AMENDMENT EACH.** Both amendments close the *same structural leak*: gandalf's proposals are sound at the rule layer, but each leaves an **operational discriminator self-asserted by the rule-subject** — precisely the COI that routed these to me, resurfacing one level down. The rule-maker≠rule-subject fix is incomplete until the *operational judgment* is also reference-anchored, not author-asserted.

- **ITEM 1 (S15):** RATIFY the substance-homing predicate. AMEND: "homed" must be **reference-verifiable**, not author-declared. Add a positive-evidence requirement (a citation OR a named fold-target that itself contains the substance) before a not-cited steward note auto-prunes.
- **ITEM 2 (ledger):** RATIFY the four dimensions, the enum, the ≥2 threshold, and the carve-out **in principle.** AMEND: the `unforeseeable_substrate_emergent` carve-out needs a **discriminator** (the pre-run knowability test) so a foreseeable miss cannot be relabelled substrate-emergent. Default-to-foreseeable on ambiguity.

Neither amendment reverses gandalf's design. Both harden it against the exact conflict the governance split exists to manage.

---

## 1. ITEM 1 — S15 substance-homing refinement

### 1.1 The claim, restated

Ruling (c) (canonical-doc-format § 6.1) sub-classes notes evidentiary / verdict-recognition / working-memory and treats `*-verdict` / `*-recognition` / `*-capture` / `*-brief` filenames as auto-prunable-on-supersede. S15's claim: **author-role modulates note-class** — a steward's `*-recognition` note is design *transmission*, not scratch, so the filename heuristic misfires for gandalf. The corrected prune predicate is not "who wrote it" nor "what's the filename" but **"is the substance already homed elsewhere in a durable canonical/tracker home?"** Homed → prunable; not-homed → judgment-tier (surface, keep). The exemption is made self-liquidating by riding the promote-then-prune lever: a steward note prunes exactly when its content is promoted to a durable home and the note collapses to a redundant pointer.

### 1.2 Does it hold as canon? — YES on substance

The reasoning is correct and it is an *improvement*, not a loosening, for three reasons:

1. **The filename heuristic genuinely misfires.** The same `*-recognition` suffix means scratch from a builder (gamora's sim-debug capture) and load-bearing lineage from a steward (a design recognition that is the *only* home of an observation until folded). A classifier that keys on filename alone will delete design lineage. That is a real defect in ruling (c) as written. S15 fixes a false-positive, which serves the system's one job (nothing depends on remembering to clean up — but *equally*, nothing load-bearing gets swept).

2. **It subsumes, does not replace, the reference-check.** A cited note is "homed" in the citing doc's dependency graph — so § 6.3 predicate 4 becomes a *special case* of substance-homing (citation is one form of homing). This is clean; it does not create a second, competing predicate.

3. **Promote-then-prune defeats the monotonic-growth objection.** gandalf correctly identifies the trap (exempt steward notes → perpetually growing queue) and correctly closes it: the exemption is a *promotion incentive*, not a permanent shield. The cancelled-prototype run (14 notes → one carry-forward → 14 redundant → prunable) is a valid proof-of-mechanism.

**On the COI question Matt posed to me directly** ("does this over-protect gandalf's OWN note output?"): the *rule content* does not. It protects note output *conditional on the substance not yet being homed* — which is a legitimate protection for ANY agent's not-yet-promoted load-bearing note, not a gandalf-specific shield. A builder's genuinely-load-bearing-but-unhomed note gets the same judgment-tier treatment. The predicate is author-neutral at the point of decision (it asks about substance-location, not authorship), even though author-role is what *motivated* discovering the defect. That is the correct shape: use author-role to find the bug, but write the fix in author-neutral terms. S15 does this. **Ratified on substance.**

### 1.3 The AMENDMENT — "homed" must be reference-verifiable, not author-asserted

Here is the leak. S15's predicate turns on a judgment: *"is the substance already homed elsewhere?"* For the **cited** case this is objective (grep finds the citation). For the **promote-then-prune** case — a note whose content was folded into a tracker but which nothing cites *by path* — the judgment "its substance now lives in the tracker, so the note is redundant" is **made by the same agent who owns both the note and the tracker and who wants the queue to shrink.** gandalf writes the note, gandalf folds it into the tracker, gandalf declares it homed, gandalf prunes it. The reference graph does not vote here; *gandalf* votes. That reintroduces rule-maker=rule-subject at the operational layer, one level below where the governance split placed the guard.

This matters because "the substance is fully homed" is exactly the kind of claim that is easy to assert and expensive to falsify after the note is `git rm`'d. If the fold was *partial* — the tracker absorbed 80% and the note still held a load-bearing 20% — an author-asserted "homed" prunes the 20% into git-lineage, silently, which is the S1/S2 failure mode (amputate load-bearing content) that the whole stress-test was built to prevent. S15, un-amended, can re-open it through the promote-then-prune door.

**AMENDMENT (ratification-conditional):** the promote-then-prune branch of the substance-homing predicate requires **positive, reference-checkable evidence of homing** before it moves a not-cited note to the auto-safe tier. Specifically, § 6.6 audit step 3 (the new "is the substance folded into a tracker/canonical home?" question) must be satisfied by ONE of:

- **(H1) a live citation** to the note (already the § 6.3 pred-4 case — objective), OR
- **(H2) a named fold-target** (the specific canonical doc / tracker PART the substance was promoted into) **that itself demonstrably contains the substance** — verified by the auditor confirming the target carries the load-bearing content, not merely that a fold was claimed. The fold-target reference is recorded in the note's own `Tracker-delta:` / fold footer at promotion time, so the audit has a concrete artifact to check against, not a memory.

If neither H1 nor H2 holds — i.e., the note asserts "my substance is elsewhere" but no reference-checkable target confirms it — the note is **judgment-tier (surface for ratification), NOT auto-safe.** This keeps S15's self-liquidating property (promotion still unlocks prunability) while restoring the reference-graph-votes discipline (promotion must be *demonstrated by a reference*, not *declared by the author*). It is the exact same principle S15 already honors for the cited case; the amendment simply extends "reference-verifiable" to cover the promote-then-prune case too, closing the author-assertion gap.

This is a *tightening within* S15's own logic, consistent with the stress-test's load-bearing principle (§ 3: "the reference graph votes on prunability; you don't pre-declare a doc dead"). S15 as drafted lets the author pre-declare a note *homed*; the amendment makes the graph vote on homing.

### 1.4 Verdict on ITEM 1

**RATIFY S15 into canonical-doc-format § 6.1 + § 6.6, WITH the H1/H2 reference-verifiable-homing amendment (§ 1.3).** The substance-homing predicate is correct and is an improvement over the filename heuristic. The amendment closes the author-asserted-homing leak so the promote-then-prune door cannot silently amputate a partially-folded note. gandalf folds the amended predicate; the fold-target-footer requirement (H2) is the concrete new obligation on the promoting agent.

---

## 2. ITEM 2 — ARCHITECT-effectiveness ledger rubric

### 2.1 (a) The four dimensions — SOUND, one refinement

D1 Coverage (`foreseen ÷ decisions-the-run-actually-hit`), D2 Classification accuracy, D3 Utility (stall-prevention), Verdict (HELD/PARTIAL/DRIFTED) are a well-shaped instrument. Each dimension maps cleanly to one falsifiable claim (completeness / classification / prioritization) named in the ledger's "falsifiable claim" section — the tests are traceable to the claims. That is good rubric hygiene.

Two refinements, both INFO-tier (fold if useful, not ratification-gating):

- **D1 denominator is defined post-hoc and is itself a judgment.** "decisions-the-run-actually-hit" is enumerated by me at scoring time, and the same substrate-emergent carve-out (2.3) that protects the numerator also shrinks the denominator (a substrate-emergent decision arguably was not a "decision the run hit" in the foreseeable sense). Recommend the denominator be stated explicitly as **"foreseeable decisions the run hit"** (excluding genuinely substrate-emergent ones from the denominator, not just exempting them in the verdict) — otherwise the carve-out is applied twice (once to numerator, once to verdict) with different force. Cleanest: substrate-emergent decisions are logged in the Miss-log for the record but sit *outside* the D1 ratio entirely. One consistent treatment.

- **D3 is qualitative + a stall-count; keep it that way.** Do not manufacture a false-precision D3 number. A stall-count plus a one-line qualitative ("gate held / a gated item blocked X") is the honest instrument. Flagging so it is not later "improved" into a spurious ratio.

### 2.2 (b) The miss-class enum — SOUND, extensible-by-design is correct

The six starter classes partition cleanly: one non-demerit (`unforeseeable_substrate_emergent`) and five demerits (`foreseeable_missed`, `misclassed_resolved_reopened`, `misclassed_gate_criterion_wrong`, `misprioritized_gated_but_blocked`, `scope_boundary_error`). The "grows like the OP § 4.3 flag enum" extensibility model matches how this team evolves its taxonomies (append-on-instance) and is consistent with Discipline #30 (name the pattern) — a new miss-shape gets named when it appears rather than pre-invented. **Ratified.** One note: `foreseeable_missed` is doing heavy load as the catch-all demerit; expect it to *split* over time (e.g., `foreseeable_missed_cross_seam` vs `foreseeable_missed_within_spec`) once ≥2 instances show sub-shapes. That is fine — the enum is built to split. No action now.

### 2.3 (c) MOST IMPORTANT — the `unforeseeable_substrate_emergent` carve-out

**Verdict: LEGITIMATE carve-out, but a LOOPHOLE without a discriminator. Ratify the carve-out; MANDATE the discriminator.**

Why legitimate: the ledger's rationale is correct and I ratify it — *foreseeing substrate emergence would violate substrate-led discipline* (Discipline #18.1 substrate-voting-is-binding; Discipline #25 semantic-layer rep-audit; the substrate votes, you do not pre-impose the taxonomy). Penalizing the ARCHITECT pass for failing to predict an unpredictable substrate vote would train gandalf to *pre-declare* substrate outcomes to protect the score — which is the exact anti-substrate-led behavior Disciplines #18.1/#25 exist to forbid. So the carve-out is not just defensible, it is *required* to keep the ledger from incentivizing a discipline violation. Ratified in principle.

Why it is nonetheless a loophole as written: the enum contains both the free-pass bucket and the demerit bucket (`foreseeable_missed`), but **nothing defines the boundary between them**, and the miss is filed into whichever bucket the classifier argues for. The ledger's own structure *mostly* guards this — **I own the Miss-log classification, not gandalf** (gandalf pre-preps CLAIM columns; jack-ryan fills SCORE + Miss-log). So the disinterested judge already classifies, which is the right guard and I note it holds. But two residual leaks remain even with me classifying:

1. **Ambiguous cases have no default.** When a miss is genuinely borderline (was it knowable pre-run, or did it need the substrate to speak?), the rubric gives me no rule, so classification drifts case-to-case. That is a consistency hole in *my own* scoring, independent of gandalf.
2. **gandalf's CLAIM pre-prep frames the miss.** gandalf writes the "what the pass claimed" columns, which sets the narrative I score against. A miss pre-framed as "the substrate surprised us here" primes a substrate-emergent reading. I classify, but I classify against gandalf's framing — Discipline #42 (framing-audit at consumption) applies to *me* here.

**MANDATED DISCRIMINATOR (the pre-run knowability test):** a miss is `unforeseeable_substrate_emergent` **only if** the decision could NOT have been enumerated from the pre-run canonical state — i.e., it required a *specific empirical result the run itself produced* (a substrate vote, a cluster shape, a measured value) that was not derivable from spec/canon/decisions-log at pass time. Operationally, the test is one falsifiable question the scorer must answer in the Miss-log row:

> **"Was there a canonical/spec/decisions-log artifact readable at ARCHITECT-pass time from which this decision was enumerable?"**
> - **YES** (or plausibly yes) → `foreseeable_missed` (or the relevant mis-class). **Counts against the pass.**
> - **NO — it required a run-produced empirical result** → `unforeseeable_substrate_emergent`. **Free pass.**

And the tie-breaker that keeps it honest: **default-to-foreseeable on ambiguity.** If the scorer cannot point to the specific run-produced empirical result that *made* the decision unforeseeable, the miss is `foreseeable_missed`. The carve-out must be *earned by naming the emergent input*, not *granted by asserting surprise.* This mirrors S15's amendment (§ 1.3) exactly: the free-pass, like the prune, requires positive reference-checkable evidence (here: the named emergent input), not an author-asserted narrative. Symmetric fix, symmetric principle.

To close leak #2, I add a **framing-audit reflex on the CLAIM pre-prep** (Discipline #42): when scoring, I re-derive the decision list from canon *independently* before reading gandalf's CLAIM framing, so a "substrate surprised us" pre-frame cannot prime the classification. This is my obligation as scorer, folded into the ledger's step-3 (jack-ryan follows up) description.

### 2.4 (d) The ≥2-instances promotion threshold — SOUND, keep at 2

≥2 instances of the same foreseeable miss-class before promoting to a standing ARCHITECT rule is the **right** threshold. Reasoning:

- **1 is noise; 2 is a line; 3 is over-conservative for this volume.** A single miss can be idiosyncratic (one weird run). Requiring 2 confirms the shape *recurs* — the minimum evidence for "this is a pattern, not an incident." Requiring 3+ would let a genuine recurring blind-spot burn a third run before the rule fires, which is expensive foresight-debt for a team whose whole thesis is catching issues 10× cheaper upstream.
- **It matches the team's existing promotion cadence.** Disciplines in this project routinely promote on 2 confirmed instances (e.g., Discipline #25's "first two confirmed production-Cycle-10 applications" canonicalization pattern; the append-on-instance enum model). ≥2 is consistent with house style, so it will not read as arbitrary.
- **The asymmetry is correct:** promotion is cheap to *propose* (gandalf drafts) and gated by two disinterested checks (jack-ryan reviews, Matt approves) before it becomes a standing rule. With that double-gate downstream, a low ≥2 trigger is safe — a false pattern gets caught at my review or Matt's approval, so the threshold can afford to be sensitive. If the trigger were the *only* gate I would argue for 3; because it is the *first of three* gates, 2 is right.

One refinement (INFO): specify that the ≥2 instances must be **the same miss-class AND plausibly the same root-shape**, not merely two rows sharing an enum tag. Two `foreseeable_missed` rows with unrelated causes (one cross-seam scope, one within-spec omission) are not a pattern — they are two different bugs wearing one tag. Promotion candidate requires 2 instances that a rule could *actually* prevent with one check. (This ties to the 2.2 note that `foreseeable_missed` will split — until it splits, the root-shape qualifier does the disambiguation.)

### 2.5 Verdict on ITEM 2

**RATIFY the rubric** (four dimensions, enum, carve-out, ≥2 threshold) **WITH:**
1. **MANDATORY** — the pre-run-knowability discriminator + default-to-foreseeable tie-breaker on the substrate-emergent carve-out (§ 2.3). This is the ratification-gating change; without it the carve-out is exploitable.
2. **MANDATORY** — the framing-audit reflex on CLAIM pre-prep (§ 2.3, Discipline #42) folded into the "jack-ryan follows up" step.
3. INFO — D1 denominator = "foreseeable decisions the run hit," substrate-emergent decisions logged but outside the ratio (§ 2.1).
4. INFO — ≥2 instances must share root-shape, not just enum tag (§ 2.4).
5. INFO — do not numeric-ize D3 (§ 2.1).

The ledger is otherwise a genuinely good closed-loop instrument. Born-empty is the honest choice (survey-mode: report what exists; no ARCHITECT pass has fired, so no row). The first real row lands when the first ARCHITECT-gated run reaches its Gate-2 and I score it — at which point the § 2.3 discriminator gets its first live exercise.

---

## 3. The through-line (why both amendments are the same fix)

Both instruments are gandalf-proposed to manage a rule-maker=rule-subject conflict, and Matt correctly routed *ratification* to me. But ratifying the *rule* is not the whole guard: each rule contains an **operational judgment** — "is this note homed?" (S15) / "was this miss foreseeable?" (ledger) — that, left author-asserted, re-seats the conflict one level below the rule. gandalf declaring its own note homed, or its own CLAIM framing a miss as substrate-emergent, is the same developer↔judge signature the split exists to break, just relocated from *rule-authoring* to *rule-application*.

Both amendments apply one principle: **the escape hatch must be earned by reference-checkable positive evidence, not granted by the rule-subject's assertion.** S15: homing requires a named fold-target that demonstrably contains the substance (not "trust me, it's folded"). Ledger: the free pass requires a named run-produced emergent input (not "the substrate surprised us"). In both, ambiguity defaults *against* the rule-subject's interest (surface-for-ratification / count-as-foreseeable). That is the disinterested-judge discipline carried all the way down to the operational layer — which is what my ratification is *for*.

Neither amendment reverses gandalf's design. Both are ratifications-with-hardening, and both leave gandalf's self-liquidating / learning-loop properties fully intact.

---

**Tracker-delta:** none (governance/process artifact; no engine build-vs-spec or story-settledness delta).

**Signed:** jack-ryan (governance rule-RATIFIER per canonical-doc-format § 6.7)
**For:** disinterested ratification of the S15 note-prune refinement and the ARCHITECT-effectiveness ledger rubric — both RATIFIED WITH AMENDMENT; gandalf folds the amendments, or the decisions-log candidate entries record them.
