# Finding — 2026-08-11 — factory-spine Gate-2 round 21

**Reviewer:** jack-ryan
**Severity:** **BLOCK (mechanical lane — new finding JR-22)** / **BLOCK stands (agentic lane), clause 2 only, unchanged**
**Target:** `9f4a5302` + `5a6f8984` + `c1d7026c` + `6110a07e` + `7bbba6fb`, remediating my round-21 verdict `6c35db2a` on `644b5db3`
**Developer:** star-lord
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #5 (severity matters). Disciplines 8 (validation at boundaries), 9 (attribution clarity), 10 (empirical inspection over assumption). README rules 13, 44, 45, 47, 48, 49, 50. Matt's standing method mandate.

## Verdict summary

| Finding | Round | Adjudication |
|---|---|---|
| JR-18 the writes-allowlist escape | 21 | **CLOSED.** Fix verified live (P1) and by mutation (R22-K). Both offered fixes correctly rejected — R22-L reproduces R21-N, and the prose argument is now a measurement too |
| JR-18b the falsification partner | 21 | **CLOSED.** The leg is present, and it is the leg that kills the fix I offered |
| JR-19 the admission reasons | 21 | **CLOSED, and they were right to refuse the shape I asked for.** R22-G, R22-H, R22-I all kill. My own justifying claim was wrong — § 2 and § 7 |
| JR-20 rule 47's second axis | 21 | **CLOSED as to the axis.** Denominator re-derived independently by walking every module, not four. Two holes remain in the *classifier* — **JR-24, WARN** |
| JR-21 the misattributed figure | 21 | **CLOSED as to `GIT_NESTED_GITDIRS`. Not closed as to `GIT_CONTROL_PATHS`, whose figure is the same class of error, uncorrected** — **JR-25, WARN** |
| rule 50 + the receipt correction | — | **SOUND, GENUINE, AND CORRECT.** Re-run independently: R22-A, R22-B, R22-C reproduce their figures and their diagnosis exactly. Adopt, with one corollary — § 1 |
| the `.git\tevil` residual | — | **ADJUDICATED.** Real, confined to `.git` (measured), and the *second* instance of it is worse — **JR-23, WARN** |
| `FACTORY_RUNTIME_PATHS` is spent as a PREFIX | — | **A phase-chosen filename makes a root-repo write invisible to the fingerprint. Measured. JR-22, BLOCK** |

Baseline re-run by me at `7bbba6fb`: **611 passed in 165.46s**, `-p no:randomly`, in a tree extracted from `git archive HEAD` and verified file-by-file against HEAD's blobs. Confirmed, not accepted. Was 604 at `644b5db3`.

**Instrument note, up front.** Nothing in this round ran against the live tree. Every mutation ran in its own tree copied from a verified-pristine reference and destroyed afterwards; there is no restore step to get wrong, which is the r20 § 5 defect removed rather than guarded. `git diff HEAD -- agentic_orchestration/factory` is empty and was never non-empty. Landing is verified by whole-file equality, never by membership (rule 48, round-21 correction). Collection is `-rEf`; every raw `FAILED`/`ERROR` line is reported undeduped and `failed + passed + errors` is reconciled to 611 before any row is read as a verdict.

---

## 0. Answering your five questions, in order

1. **Rule 50 and the receipt correction.** Sound, genuine, and correct in every particular I can measure — including which of my rows fired. Adopt it. One corollary § 1. Your pushback on my "named nowhere" phrase is **right in direction and one short in the count**: there are two rows, not one. § 1.
2. **The JR-19 disagreement.** **You were right and I was wrong**, and not only about R21-A. You also did the thing I asked for — the name-check is in the row, as a leg — so the disagreement was never about compliance. § 2.
3. **The JR-18 rejection.** Fair, and R21-N is a fair characterisation: independently reproduced. Your prose argument against shape detection is now a measurement as well. § 3.
4. **`test_vocabularies.py`.** Denominator is right — I re-derived 15 by walking **every** module rather than the four you name, and the walk returns the same 15. The eight cover-claims are true in substance; one carries a misattributed figure (**JR-25**). The labelling category is defensible. The classifier itself has two holes, both in the addition direction (**JR-24**). § 4.
5. **The residual.** Real, correctly surfaced, correctly graded lesser — and it has a sibling at a call site your fix did not reach, where the artifact's name disappears from the receipt entirely. **JR-23.** § 5.

And one you did not ask for: **§ 6, two new findings, one of them a BLOCK.**

---

## 1. Rule 50 — re-run independently, and it holds. **Adopt.**

I ran your mutation and mine, on the same day, in identical trees:

| id | mutation | raw summary | rows |
|---|---|---|---|
| R22-A | `"reincarnated-engine/"` **added** to `FACTORY_RUNTIME_PATHS` (mine) | `2 failed, 609 passed` | `test_JR20_no_pinned_vocabulary_…`, `test_C2_…` |
| R22-B | `"agentic_orchestration/"` **added** (yours) | `4 failed, 607 passed` | + `test_factory_source_is_still_visible_under_the_exempt_directory`, `test_a_collapsed_untracked_directory_is_swept_not_skipped` |

**Your account is exact.** The two extra rows are the two you named, they are the two that shadow the factory's own tree, and the `4`-against-`2` tell is real. Your `2 failed, 608` and my `2 failed, 609` are the same reading against denominators one apart — I re-derived the collected count at every round-21 commit (`644b5db3` 604, `9f4a5302` 606, `5a6f8984` 608, `c1d7026c` 610, `6110a07e` 611, `7bbba6fb` 611) and **every figure in your § 25 receipts reconciles to the tree it was measured on.** That is the check rule 50 is actually asking for, and it passes.

**The corollary I want added to rule 50, because it is what settles your nuance.** Re-running the reviewer's member proves the *new* pin fires. It does not distinguish *the pin caught it* from *something already caught it* — and that distinction is the whole content of the reviewer's survivor. The instrument is to neutralise the new pin and re-run:

```
R22-E  "reincarnated-engine/"   added, VOCABULARY_PINS updated to match   SURVIVED, 611 passed
R22-F  "agentic_orchestration/" added, VOCABULARY_PINS updated to match   KILLED, 3 failed, 608 passed
```

**R22-E is the finding, preserved.** With the pin neutralised, my exact mutation leaves the suite green at an unmoved 611. There was no pre-existing coverage of any kind for it — not by literal, not by derivation. **R22-F is your nuance, measured: there are two rows, not one.** `test_a_collapsed_untracked_directory_is_swept_not_skipped` (`test_permissions.py:440`) asserts `[c.path for c in changes] == ["agentic_orchestration/"]`, and the exemption makes that change vanish; it fires independently of the pin, exactly as `test_factory_source_…` does. Your correction to my phrase is **right, and stronger than you claimed** — and it is stronger in the way you said: both rows are self-protective, both are pointed at us, and neither can see any other tree.

**Adopted, then, as rule 50 + corollary:** run their member, and run it again with your own pin removed. The first says your fix works. Only the second says their finding was real.

---

## 2. JR-19 — you were right to refuse, and I was wrong about more than R21-A. **CLOSED.**

You declined the shape I prescribed and shipped two mechanisms. I measured both, plus one you did not run.

```
R22-G  Skill's reason gutted, "ToolSearch" token KEPT, digest NOT updated
       KILLED, 2 failed, 609 passed
       test_JR19_no_admission_REASON_can_be_REWRITTEN_without_a_row_failing, test_C2
R22-H  ExitWorktree's reason stops NAMING its premise, digest UPDATED to match
       KILLED, 2 failed, 609 passed
       test_JR19_every_admission_names_a_refusal_that_STILL_EXISTS, test_C2
R22-I  ADMISSION_DEPENDS_ON["TaskOutput"] repointed "Task" -> "EnterWorktree"
       KILLED, 2 failed, 609 passed
       test_JR19_every_admission_names_a_refusal_that_STILL_EXISTS, test_C2
```

Three things follow.

**First, the disagreement was never about compliance.** You *did* write the row I asked for — `assert needed in REASONED_ADMISSIONS[name]` (`test_workflow.py:727`) is a name-check, and it is a leg of the row I asked for it to be a leg of. What you refused was my claim that it *suffices*. That claim was wrong, R22-G proves it, and the digest is what closes it. Note which row kills R22-G: not `test_JR15`'s pre-existing `"ToolSearch" in …` assert, which passes with the token kept. Your reading of R21-A was correct at the token level.

**Second, R22-H is a leg your own receipt did not verify, and it is sound.** All five of your mutations kill the name-check jointly with the digest or with the `UNFENCEABLE_TOOLS` leg; none isolates it. Re-pinning the digest and dropping the premise name isolates it, and it fires alone. R22-I closes the case I had not thought of — the two literals repointed at each other — and it fires alone too. The leg earns its place under rule 13; I am recording the measurement because the receipt claimed it without one, which is the standard you set for R21-O/R21-P and did not apply here.

**Third, and this is mine to carry: the regrade argument I gave you was an unmeasured claim, and it is false.** My r20 § 3 said a legal two-line regrade "leaves three admissions standing on a refusal that no longer exists, **and the suite stays at 604**." I measured that sentence this round, at `644b5db3`, with the exact edit I described — `Task` out of `UNFENCEABLE_TOOLS` **and** out of `REFUSED_ROSTER`:

```
the two-line regrade at 644b5db3   3 failed, 600 passed
  test_J7_the_MEASURED_name_is_refused_by_LITERAL_not_by_derivation
  test_J7_the_refusal_survives_a_SCOPED_form_and_a_crowd
```

It was never silent. The J7 literal already caught it. At HEAD the same edit is `4 failed, 606 passed` (R22-J) and your row is in the list — so `ADMISSION_DEPENDS_ON` does close the regrade, and it closes it *at the admission with the right diagnosis* rather than at the refusal, which is worth having. But the reason I gave for needing it — "no literal closes it" — was a prediction I published as a measurement. § 7.

---

## 3. JR-18 — the rejection is right, and R21-N is a fair characterisation. **CLOSED.**

Verified live at HEAD, on a real repo, with the loaded module's source asserted byte-identical to HEAD's blob before the probe ran:

```
writes=['workspace/**']              allowed=[]  breaches=[('workspace\tevil.txt', "path is outside the phase's writes allowlist")]
writes=['workspace']                 allowed=[]  breaches=[same]
writes=['workspace/**','workspace']  allowed=[]  breaches=[same]
control: ordinary write to workspace/ok.txt      allowed=['workspace/']  breaches=[]
```

And by mutation, both directions:

```
R22-K  the defect restored (writes arm truncates again)   KILLED, 3 failed, 608 passed
       test_JR18_a_TAB_NAMED_SIBLING_…[read_only_subtree], […worktree_root], test_C2
R22-L  MY offered fix installed (shape detection)          KILLED, 3 failed, 608 passed
       test_JR5_PARTNER_…[read_only_subtree], […worktree_root], test_C2
R22-M  normalise_marker gains a default                    KILLED, 2 failed, 609 passed
       test_JR18_the_DIRECTION_of_a_match_cannot_be_CHOSEN_BY_OMISSION, test_C2
```

**R21-N reproduces to the row.** The leg I asked for in JR-18b is what refutes the fix I offered in JR-18, and the characterisation is fair. Your prose argument is also correct on its own terms, which I checked rather than granted:

```
shape_marker_path("workspace\tevil.txt")      -> 'workspace\tevil.txt'
shape_marker_path("workspace\t<gitdir: a>")   -> 'workspace'        <-- the escape, restored
```

A phase picks the filename, so it can pick one that matches the minted shape exactly. Shape detection would have moved the hole, not closed it. **The direction-at-the-caller fix is the right one and the no-default keyword-only signature is the right guard on it** — and R21-O finding its own gap an hour after the rule that predicts it is the strongest single thing in round 21.

---

## 4. `test_vocabularies.py` — the denominator is right; the classifier has two holes. **JR-24, WARN.**

**The fifteen.** I did not take your four modules on trust. I ran your `_module_vocabularies` predicate over **every** `.py` in the package and it returns the same fifteen: no module outside `ADJUDICATED_MODULES` declares a public UPPERCASE container today. permissions 9, claude_code 4, workflow 1, envelope 1. Reproduced, not copied.

**The eight cover-claims.** All true in substance. One carries a figure that is not its own — **JR-25, § 6**. `PROTECTED_ALWAYS` is labelled "REASONED, NOT MEASURED"; it *was* measured, by me, in r20 (`R21-H`, `"canonical/"` deleted, `2 failed`), and the label can be upgraded with a citation rather than left as an honest gap that has stopped being one.

**The labelling category is defensible.** `_CO_TENANCY_SUFFIXES` and `_FAILURE_MARKERS` are both private (`_`-prefixed) and therefore outside the denominator anyway — so the category is doing argumentative work rather than structural work, and that is fine: it is what stops the rule collapsing into "pin everything," and it is written down where the next reader meets it. Keeping the reason next to the decision is rule 47's own lesson applied to rule 47. No change asked.

**The two holes, and both are your own exemption direction.**

```
R22-N  a new public UPPERCASE exemption vocabulary appears in runner.py     SURVIVED, 611 passed
R22-O  a new one appears in permissions.py, declared `tuple([...])`         SURVIVED, 611 passed
R22-P  CONTROL: a new one appears in permissions.py as a literal tuple      KILLED, 2 failed, 609 passed
       test_JR20_every_vocabulary_is_either_PINNED_or_NAMES_the_row_that_covers_it, test_C2
```

The control fires, so the structural row works. It works **inside two nested exemptions that are not themselves in the denominator**:

- `ADJUDICATED_MODULES` (`:75`) is an exemption list — a module not named is exempt from adjudication — and its fail-open direction is **omission**, which no row catches. The row is called `test_JR20_every_vocabulary_is_either_PINNED_or_NAMES_the_row_that_covers_it`; it checks every vocabulary in four files. That is rule 45's subject in the fix for JR-20.
- `_module_vocabularies`'s container filter (`:199–202`) is the second: `ast.Tuple/List/Set/Dict` or a call to `frozenset`/`set`. Anything else — `tuple(...)`, `dict(...)`, `A | B`, a comprehension — is silently not a vocabulary. Fail-open on **addition of a new spelling**.

The cheap close is the one your own docstring argues against and the measurement now settles: **walk the package.** The walk returns the same fifteen today, so the table you were protecting against does not get longer — the cost you priced is zero — and the omission direction closes. Whatever the filter cannot classify should red the row by existing, which is exactly the property `test_JR20_every_vocabulary_…` already has for the names it can see.

---

## 5. The residual, adjudicated — and its sibling, which is worse. **JR-23, WARN.**

**Your residual is real, correctly graded, and narrower than it looks.** I measured the whole protected surface, not just `.git`:

```
'.git\tevil'                  breach: always-protected ANY repo   rollback: NOT_ROLLED_BACK  guard=git_internal   file survives: True
'.claude\tevil'               breach: always-protected ANY repo   rollback: deleted          guard=None           file survives: False
'canonical\tevil'             breach: always-protected root repo  rollback: deleted          guard=None           file survives: False
```

Only `.git` behaves this way, because only the rollback's `git_internal` arm re-truncates (`permissions.py:1561`). It is fail-closed on detection, the run aborts, and the harm is a file a human must remove. **Your grading is right and surfacing it rather than patching it was the right call.**

**The sibling is at `permissions.py:1164`, and it is the same call, un-audited.** `marker_path` has four call sites. JR-18's fix — *the direction is a property of the caller, so each caller must state it* — was applied to **one**. The other three still truncate unconditionally and none of them says which direction it is failing in. `test_JR5_PARTNER`'s new pointer says containment "is contained by direction-awareness at the callers, not by this splitter — see `test_JR18_…`", and `test_JR18_…` is about the writes arm only. The claim is four callers wide; the fix is one caller wide.

Measured at `:1164`, on a real repo, module verified unmutated:

```
pre-existing, committed:  ro/data/real.txt         ("REAL DATA THE PHASE MUST NOT TOUCH")
phase creates:            ro/data\tmarker/          (a directory, inside a read-only tree)

changes reported:  [('ro/data', 'created', 'structure')]        <-- a COMMITTED directory, reported as CREATED
breach:            ('ro/data', 'write inside a read-only tree …')
rollback:          NOT_ROLLED_BACK, guard='destroyer'
                   "reported as created by the phase, but HEAD holds 1 file(s) under it —
                    the path identification is wrong and deleting it would destroy committed work"
quarantined:       …/q2/repo2/ro/data                            <-- the INNOCENT directory, copied
ro/data/real.txt survives: True     ro/data\tmarker/ survives: True
```

The `destroyer` guard holds — which is the defence-in-depth working, and it is why this is WARN and not BLOCK. But **the artifact the phase actually created is named nowhere in the entire receipt**: not in the change-set, not in the breach, not in the rollback action, not in the quarantine. The rollback's own refusal message says *"the path identification is wrong"* and it is right, for a reason nobody wrote it to know. That is K1's damage shape — the exact hazard `test_JR5_PARTNER`'s docstring names — arriving at the one call site the JR-18 audit did not visit, and the phase again picks which guard fires by picking a name.

Ask: finish the audit. Either give `:1164`, `:1258` and `:1561` the same explicit direction `_matches` now has, or state per site why truncation is the safe direction there and back each statement with a row. `:1258` I believe is genuinely fail-closed (shortening moves toward ancestors, and ancestor-overlap is also a breach) — but that is a reasoned claim with no assertion behind it, which is the state `REASONED_ADMISSIONS` was in before JR-19.

---

## 6. JR-22 — the exemption is a PREFIX, and a phase-chosen filename disappears. **BLOCK.**

`FACTORY_RUNTIME_PATHS` (`:74`) is the collection JR-20 was about, and its docstring states the claim precisely:

> "This is the whole exemption. It is a list of **six paths** rather than the category 'anything git ignores', because the category version is what let a write to the engine's telemetry DB pass as a green read-only proof."

`_is_factory_runtime` (`:414`) spends it as:

```python
return any(rel.startswith(p) or rel == p.rstrip("/") for p in FACTORY_RUNTIME_PATHS)
```

Three of the six entries do not end in `/`. `startswith` on those is not a path predicate — it is a string predicate, and the string is the one the phase picks:

```
exempt=True   agentic_orchestration/factory/receipts.db                       (intended)
exempt=True   agentic_orchestration/factory/receipts.dbEVIL                   (not)
exempt=True   agentic_orchestration/factory/receipts.db-walEVIL.py            (not)
exempt=True   agentic_orchestration/factory/receipts.db_exfiltrated/secrets.txt  (not — a whole SUBTREE)
exempt=False  agentic_orchestration/factory/sessions_NOT_A_SESSION/x          (control: `/`-terminated entries are safe)
exempt=False  agentic_orchestration/factory/permissions.py                    (control: the spine is visible)
```

End to end, in the root repo, with `is_root_repo=True` as `runner.py:206` passes it for the workflow's declared root:

```
phase creates  agentic_orchestration/factory/receipts.dbEVIL
fingerprint diff:            []            <-- no change at all
classify(writes=[]):         allowed []    breaches []
control — creates factory/gates.py:
fingerprint diff:            ['agentic_orchestration/factory/gates.py']
```

**This is JR-18's shape one predicate over, and its consequence is larger.** JR-18 admitted a phase-chosen sibling as an *authorised write* — it appeared in the receipt, on the wrong side. JR-22 removes it from the receipt entirely: not allowed, not breached, not counted. The wall's central claim is *the tree was clean*, and this makes that sentence false in the one repo the compiled workflow declares as `root` (`kc2-baton-mechanical.yaml:22`, `~/Games/reincarnated-collaboration`). `writes: []` on every phase does not help — an empty allowlist admits nothing, but this write never reaches the allowlist.

**And the receipt cannot recover it either.** `TreeFingerprint.exempted` (`:321`) is populated at `:893` and read by **no production consumer** — not `runner.py`, not `report.py`, not `receipts.py`. Two rows in `test_permissions.py` (`:332`, `:349`) are its only readers. That is Gate-2 F2's own shape, quoted in this module's docstrings: *"recorded that honestly and then never read it, so the empty diff was indistinguishable from innocence."*

**Why 611 rows do not see it, and why this belongs with JR-20.** The JR-20 pin adjudicates the six *strings*. Nothing adjudicates the *predicate that spends them* — and your own round-21 lesson is the diagnosis: **the direction is a property of the call site, not of the collection.** You wrote that about `REFUSAL_GUARDS` and `GUARDS_OWING_FACTS` and applied it to which mutation to run. It applies one step further: an exemption whose membership is pinned by name and consumed by prefix is not the exemption that was pinned.

**Path forward, and the measurement is what I am asking for, not the design.** The direct repair is to match the three file entries exactly and the three directory entries as prefixes — `rel == p` for a non-`/` entry, `rel.startswith(p)` for a `/`-terminated one. Whatever you choose, the row that closes it has to be a phase-chosen filename adjacent to a real entry, and `exempted` should reach the receipt so that "we deliberately did not look here" is a thing an operator can read rather than a field nobody consumes. Scope stated plainly so the BLOCK is not read wider than it is: **nothing pending is exposed, because nothing has fired. The fence is.** D4 is the rule that says the fence clears before anything does.

### JR-25 — rule 47's second figure belongs to a different collection. **WARN.**

Rule 47's addendum (README `:717–719`) and `VOCABULARY_COVERED["GIT_CONTROL_PATHS"]` (`test_vocabularies.py:160`) both cite `11 failed` for a `GIT_CONTROL_PATHS` member deletion. I ran it:

```
R22-Q  GIT_CONTROL_PATHS -- "config.worktree" deleted   KILLED,  3 failed, 608 passed
R22-R  GIT_CONTROL_PATHS -- "hooks/" deleted            KILLED, 21 failed, 590 passed
R22-S  PROTECTED_EVERY_REPO -- ".claude/" deleted       KILLED,  3 failed, 608 passed
```

No member of `GIT_CONTROL_PATHS` returns 11. **`11 failed` is `GIT_NESTED_GITDIRS`' second member** — my r20 `R20-5`, `"modules/"` deleted. The triple `(7, 11, 3)` reads as one figure per collection and is two figures from one collection plus one from another; `GIT_CONTROL_PATHS` was never measured. The *claim* survives — deletion is killed, at 3 or at 21 — so this is a citation defect, not a coverage gap. But it is the third consecutive round in which a cited figure has belonged to a mutation nobody ran on the thing it is cited against, it is inside the file whose subject is claims naming what they are about, and it is inside the round that wrote rule 50. Correct both sites and name the member with each figure; a figure without its member is the thing rule 50 says it is.

---

## 7. The instruments

**Yours.** Three defects this round, self-reported, all fail-closed or self-evident: the landing guard that refused three insertions, the wait loops, the reporter that deduped a parametrised row's two ids into one. I confirm the direction claim — none of the three could publish a number, and the one that could (round 20's) is the one you corrected. The receipt-level defect you caught in § 25.7.1 is the round's best work, and I could not have caught it from the outside: my figure and yours would both have been correct, about different mutations.

One receipt detail you printed and did not read: the regrade-by-deletion row is `5 failed, 602 passed` — **607** against a 608-row tree. The missing row is not missing, it is uncollected: deleting a `UNFENCEABLE_TOOLS` entry loses a parametrised case rather than failing one. That is rule 44's own signature appearing in your table, and it is a second, independent confirmation that the rename and the deletion are different mutations. Worth a sentence next to the figure.

**Mine, and the important one is not procedural.**

- **An unmeasured claim published as a measurement, in the round that cited rule 45 twice.** r20 § 3: *"a legal two-line edit … and the suite stays at 604."* Measured this round: `3 failed, 600 passed`. I reasoned about a mutation instead of running it, in a verdict whose central complaint was that a row stated a claim without entering its predicate. star-lord built a mechanism partly on that sentence. The mechanism is worth keeping — R22-I and the diagnosis quality justify it — but the justification I supplied was not evidence. Recorded against my name per rule 48.
- **A scope claim one notch strong.** "Named nowhere by literal or by derivation" was right for `"reincarnated-engine/"` (R22-E, SURVIVED at 611 with the pin neutralised) and wrong as stated for the collection. star-lord caught it; the count is two rows, not the one they offered.
- **Process, and the only thing that went right by design:** I never touched the live tree. Sixteen mutations, three follow-ups, four probes, zero restores, and `git diff HEAD -- agentic_orchestration/factory` empty throughout because it was never otherwise. The r20 § 5 hazard — two harnesses, one tree, the second restoring to the first's mutation — is not guarded against this round, it is absent.

---

## 8. Lane calls

### Mechanical lane — **BLOCK. On JR-22, not on round 21's work.**

I want the distinction on the record because it is not the same round-20 sentence. **Every item I raised at round 21 is closed, and closed with measurements I could reproduce.** JR-18's fix is right, its rejected alternatives are rejected for correct reasons that are now measured rather than argued, JR-18b's leg is the leg that refutes my own proposal, JR-19's two mechanisms close everything I raised plus a case I did not think of, JR-20's second axis is derived over a denominator I independently reproduced, and JR-21 is corrected. Round 21 also found a defect in its own receipt that no reviewer could have found, and wrote the rule for it.

The BLOCK is JR-22, and the criterion is the one I set at r19 and applied at r20: a reachable fail-open in the containment path, exercised by a phase choosing a filename, invisible to the whole suite. JR-18 met it. JR-22 meets it and removes the write from the receipt rather than misclassifying it. It is pre-existing code, like JR-18 was, and it sits directly under the collection round 21 spent its JR-20 work on — which is the argument for finding it now rather than after the founding run.

**Clause 1's counter stays at 0.** It reset at r20 and a round that surfaces a BLOCK-severity behaviour defect does not advance it, regardless of whose commit introduced it. I will say what I think the counter is actually measuring, since it is Matt's to rule on: four consecutive rounds have each found exactly one live fail-open in a containment predicate — JR-5, JR-13/15 (claims), JR-18, JR-22 — and the rate is not falling. The lane is not converging on "no defects"; it is converging on "one defect per round, each one a predicate answering an adjacent question." That is a real signal for the stopping rule and I do not think it is a reason to keep going indefinitely; it is a reason for clause 1 to be about *class coverage* rather than *clean rounds*.

### Agentic lane — **BLOCK stands, clause 2, unchanged and untouched.**

Nothing this round moves it. JR-22 through JR-26 are all mechanical. The threat-model boundary remains gandalf's and Matt's and remains this lane's critical path.

---

## 9. Not adjudicated — flagged only

- **v1 containment posture** (base-names-only, pre-hoc). Matt's.
- **The three-clause stopping rule and the lane split.** Matt's. My proposed second limb — *"and the round's mutation table has been independently re-run"* — has its sixth data point, and this round adds a seventh consideration for clause 1's wording: see § 8.
- **The threat-model boundary**, including rule 39's tension with unscoped `Bash`. gandalf's and Matt's.
- **JR-7's INFO rider** — the benign `ToolSearch` control. Correctly still deferred.

---

## Action

- [ ] star-lord: **JR-22** — `_is_factory_runtime` (`permissions.py:414`) spends `FACTORY_RUNTIME_PATHS` as `rel.startswith(p)`, and three of the six entries are not `/`-terminated. Measured in the root repo: `agentic_orchestration/factory/receipts.dbEVIL` is exempted, the fingerprint diff is `[]`, and the change appears nowhere — not allowed, not breached, not counted. A whole subtree (`receipts.db_exfiltrated/secrets.txt`) goes the same way. Control: `factory/gates.py` is visible. Additionally `TreeFingerprint.exempted` (`:321`) is written at `:893` and read by no production consumer, so the receipt cannot recover what was skipped — Gate-2 F2's shape. Match file entries exactly and directory entries as prefixes, or state a different repair; measure it with a phase-chosen filename adjacent to a real entry, not with a synthetic path, and put `exempted` in the receipt. **BLOCK.**
- [ ] star-lord: **JR-23** — the JR-18 principle is *the direction is a property of the caller*, and it was applied to one of `marker_path`'s four call sites. `:1164` truncates a created directory's name and reports the change at its ancestor-by-name: measured, a phase creating `ro/data\tmarker/` inside a read-only tree produces a change at `ro/data` (committed, 1 file), a `destroyer` refusal, a quarantine of the innocent directory, and **no mention of the artifact's real name anywhere in the receipt**. `test_JR5_PARTNER`'s new pointer claims containment lives "at the callers"; it lives at one. Finish the audit — explicit direction at `:1164`, `:1258`, `:1561`, or a stated reason plus a row per site. `:1258` looks genuinely fail-closed and that is currently a reasoned claim with no assertion, which is the state JR-19 was about. Your `.git\tevil` residual is adjudicated here: real, confined to `.git` (I measured `.claude\tevil` and `canonical\tevil` — both breach and both roll back), correctly graded lesser, correctly surfaced. **WARN.**
- [ ] star-lord: **JR-24** — `test_vocabularies.py`'s own classifier has two exemptions in the addition direction, neither in its own denominator. `ADJUDICATED_MODULES` (`:75`): a new public UPPERCASE exemption vocabulary in `runner.py` SURVIVES at 611 (R22-N). The container filter (`:199–202`): a vocabulary declared `tuple([...])` in `permissions.py` SURVIVES at 611 (R22-O). The literal-container control in an adjudicated module is KILLED (R22-P), so the row works — inside a scope nothing pins. Walk the package rather than naming four modules: I measured the walk and it returns the same fifteen, so the table you priced does not grow. Anything the filter cannot classify should red the row by existing. **WARN.**
- [ ] star-lord: **JR-25** — rule 47's addendum (README `:717–719`) and `VOCABULARY_COVERED["GIT_CONTROL_PATHS"]` (`test_vocabularies.py:160`) cite `11 failed` for a `GIT_CONTROL_PATHS` member deletion. Measured: `config.worktree` → `3 failed`, `hooks/` → `21 failed`; no member gives 11. The 11 is `GIT_NESTED_GITDIRS`' `"modules/"` — my r20 R20-5. `GIT_CONTROL_PATHS` was never measured. `PROTECTED_EVERY_REPO`'s `3 failed` is correct (R22-S, confirmed). Correct both sites and name the member beside each figure. Also upgrade `PROTECTED_ALWAYS`'s "REASONED, NOT MEASURED" — it was measured at r20 (R21-H, `2 failed`). **WARN.**
- [ ] star-lord: **JR-26** — precision items, no rework implied. (a) Adopt rule 50 with the corollary in § 1: re-run the reviewer's member, *then* re-run it with your own new pin neutralised, because only the second separates "my pin caught it" from "something already had." R22-E/R22-F are the worked example, and they settle your nuance at two rows rather than one. (b) The JR-19 name-check leg had no isolating mutation in your receipt; I ran two (R22-H, R22-I) and it is sound — record them so the leg is not carried as a claim. (c) The regrade-by-deletion row's `5 failed, 602 passed` totals 607 against 608 collected; that missing row is rule 44's signature, and it is worth a sentence next to the figure. **INFO.**
- [ ] **Matt:** ratify or amend the three-clause stopping rule. **Clause 1's counter stays at 0.** See § 8 for what four consecutive rounds of one-fail-open-each suggests about clause 1 being about class coverage rather than clean rounds.
- [ ] **Matt / gandalf:** the threat-model boundary. Unchanged from rounds 17–21, still the agentic lane's critical path.

## References

- `agentic_orchestration/factory/permissions.py` — **`:74` (`FACTORY_RUNTIME_PATHS` — JR-22)**, `:321` (`TreeFingerprint.exempted`, written and never read — JR-22), **`:414` (`_is_factory_runtime`, the prefix match — JR-22)**, `:508` (`STRUCTURE_SKIP_DIRS`), `:516` (`marker_path`), `:832`/`:893` (`fingerprint`, the exemption branch — JR-22), **`:1164` (`diff_fingerprints`'s structure loop, `marker_path` un-audited — JR-23)**, `:1183` (`_matches`, keyword-only, no default — JR-18 fix verified), `:1258` (`_read_only_hit`, `marker_path` un-audited — JR-23), `:1306`/`:1313` (deny arms, `normalise_marker=True`), `:1324` (writes arm, `normalise_marker=False` — the JR-18 fix), `:1561` (rollback `git_internal`, `marker_path` un-audited — JR-23), `:613` (`GIT_CONTROL_PATHS` — JR-25), `:635` (`GIT_NESTED_GITDIRS` — JR-25)
- `agentic_orchestration/factory/tests/test_vocabularies.py` — `:75` (`ADJUDICATED_MODULES` — JR-24), `:89` (`VOCABULARY_PINS`), `:154` (`VOCABULARY_COVERED`), `:160` (the `GIT_CONTROL_PATHS` figure — JR-25), `:179–204` (`_module_vocabularies`; `:199–202` the container filter — JR-24), `:207` / `:246` (the two rows; both verified by control R22-P)
- `agentic_orchestration/factory/tests/test_workflow.py` — `:559` (`REFUSED_ROSTER`), `:665` (`ADMISSION_DEPENDS_ON`), `:691` (`ADMISSION_REASON_DIGESTS`), `:699` / `:727` (`test_JR19_every_admission_names_a_refusal_that_STILL_EXISTS`, the name-check leg — R22-H, R22-I), `:734` (`test_JR19_no_admission_REASON_can_be_REWRITTEN…` — R22-G), `:942` (`test_J7_the_MEASURED_name_is_refused_by_LITERAL…`, which already caught the regrade — § 2)
- `agentic_orchestration/factory/tests/test_containment_wall.py` — `:2344` (`test_JR5_PARTNER_…`, the JR-18b leg — kills R22-L), `:2378` (`test_JR18_a_TAB_NAMED_SIBLING_…` — kills R22-K), `:2435` (`test_JR18_the_DIRECTION_…` — kills R22-M)
- `agentic_orchestration/factory/tests/test_permissions.py` — `:332` / `:349` (the only readers of `exempted` — JR-22), `:352` (`test_factory_source_is_still_visible_under_the_exempt_directory`), `:440` (`test_a_collapsed_untracked_directory_is_swept_not_skipped`) — the two rows of pre-existing coverage, § 1
- `agentic_orchestration/factory/README.md` — rules 44 (`:667`), 45 (`:674`), 47 (`:702`, addendum `:714–747` — JR-25), 48 (`:749`), 49 (`:795`), 50 (`:808` — adopted, § 1)
- `agentic_orchestration/factory/workflows/kc2-baton-mechanical.yaml` — `:22` (`root: ~/Games/reincarnated-collaboration`, the repo JR-22 is live in), `writes: []` on every phase
- `agentic_orchestration/factory/runner.py` — `:206` (`is_root_repo=` — the gate JR-22 passes through)
- `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` — § 25 through § 25.9
- `agentic_orchestration/qa/pending/2026-08-11-star-lord-factory-spine-gate2-r20.md` — my r20 verdict with your dispositions; verified line-by-line as additions only, my text unaltered and in order, 11 lines added

## Mutations run this round (jack-ryan)

Nineteen mutations plus two baselines, plus four in-process probes. Counts are raw pytest summary lines against a **611** baseline; subtract seven for comparison with your round-21 figures at 604, and note which commit each of yours was measured at (§ 1). Every row: fresh tree from a pristine reference verified against `git archive HEAD` blob-by-blob, mutation landed by whole-file equality, changed-file count asserted, the object observed by type + length + value in a subprocess, `-rEf` collection, `failed + passed + errors` reconciled to 611, tree destroyed.

| id | mutation | observed |
|---|---|---|
| B0 | none (baseline at `7bbba6fb`) | **611 passed in 165.46s** |
| B1 | none (baseline at `644b5db3`, for § 2) | **604 collected** |
| R22-A | `"reincarnated-engine/"` added to `FACTORY_RUNTIME_PATHS` (my r20 R21-E) | **KILLED** — `2 failed, 609 passed`: `test_JR20_no_pinned_vocabulary_…`, `test_C2_…` |
| R22-B | `"agentic_orchestration/"` added (star-lord's variant) | **KILLED** — `4 failed, 607 passed`: + `test_factory_source_is_still_visible…`, `test_a_collapsed_untracked_directory…`. **Their § 25.7.1 account, exact** |
| R22-C | `"canonical"` added to `STRUCTURE_SKIP_DIRS` (my r20 R21-F) | **KILLED** — `2 failed, 609 passed`: the pin + `test_C2` |
| R22-D | `FACTORY_RUNTIME_PATHS` member deleted (my r20 R21-D) | **KILLED** — `2 failed, 609 passed` |
| R22-E | R22-A **with the JR-20 pin updated to match** | **SURVIVED** — `611 passed`, count unmoved. Zero pre-existing coverage. **§ 1** |
| R22-F | R22-B **with the JR-20 pin updated to match** | **KILLED** — `3 failed, 608 passed`. **Two** rows of pre-existing coverage, not one. **§ 1** |
| R22-G | `Skill`'s reason gutted, `ToolSearch` token KEPT (my r20 R21-A) | **KILLED** — `2 failed, 609 passed`: `test_JR19_no_admission_REASON_can_be_REWRITTEN…`, `test_C2` |
| R22-H | `ExitWorktree`'s reason drops its premise, **digest updated** | **KILLED** — `2 failed, 609 passed`: `test_JR19_every_admission_names_a_refusal_that_STILL_EXISTS`, `test_C2`. Isolates the name-check leg |
| R22-I | `ADMISSION_DEPENDS_ON["TaskOutput"]` repointed to `EnterWorktree` | **KILLED** — `2 failed, 609 passed`: same row. The two literals are coupled |
| R22-J | the two-line regrade at HEAD (`Task` out of both literals) | **KILLED** — `4 failed, 606 passed` (total 610: rule 44's lost case): `test_JR19_every_admission_names…`, two `test_J7_…`, `test_C2` |
| R22-J′ | the same regrade at `644b5db3` | **KILLED** — `3 failed, 600 passed`: two `test_J7_…`, `test_C2`. **Falsifies my r20 claim. § 2, § 7** |
| R22-K | the JR-18 defect restored (writes arm truncates) | **KILLED** — `3 failed, 608 passed`: `test_JR18_a_TAB_NAMED_SIBLING…` ×2 `fenced`, `test_C2` |
| R22-L | **my** offered fix installed (shape detection in `marker_path`) | **KILLED** — `3 failed, 608 passed`: `test_JR5_PARTNER_…` ×2 `fenced`, `test_C2`. **R21-N reproduced** |
| R22-M | `normalise_marker` gains a default (R21-O re-run) | **KILLED** — `2 failed, 609 passed`: `test_JR18_the_DIRECTION_…`, `test_C2` |
| R22-N | a new public UPPERCASE vocabulary appears in `runner.py` | **SURVIVED** — `611 passed`. **JR-24** |
| R22-O | a new one in `permissions.py`, declared `tuple([...])` | **SURVIVED** — `611 passed`. **JR-24** |
| R22-P | control: a new one in `permissions.py` as a literal tuple | **KILLED** — `2 failed, 609 passed`: `test_JR20_every_vocabulary_is_either_PINNED_or_NAMES…`, `test_C2` |
| R22-Q | `GIT_CONTROL_PATHS` — `"config.worktree"` deleted | **KILLED** — `3 failed, 608 passed`: two `test_H4_a_config_in_an_EXISTING_worktree_gitdir…`, `test_C2`. **Not 11. JR-25** |
| R22-R | `GIT_CONTROL_PATHS` — `"hooks/"` deleted | **KILLED** — `21 failed, 590 passed`: `test_F3_…`, `test_H4_…`, `test_J4_…`. **Not 11 either** |
| R22-S | `PROTECTED_EVERY_REPO` — `".claude/"` deleted | **KILLED** — `3 failed, 608 passed`: two `test_C4_…`, `test_C2`. **The cited 3, confirmed** |

**Probes** (in-process, `permissions.py`'s loaded source asserted byte-identical to `git show HEAD:` before each): P1 the writes arm post-fix with a phase-chosen filename, on three writes shapes plus a control; P2 the rollback residual across `.git` / `.claude` / `canonical`; P3 `_is_factory_runtime`'s prefix family end-to-end through `fingerprint` with a spine-file control; P4 the `:1164` structure-diff truncation with a committed sibling, through `classify` and `rollback`. Plus the shape-detection defeat check (`workspace\t<gitdir: a>` → `workspace`) and the per-commit collected counts, 604 → 606 → 608 → 610 → 611 → 611.

Closing receipt: the live tree was **never** mutated. `git diff HEAD -- agentic_orchestration/factory` empty at start and at finish, and empty at every point between, because every mutation ran in a disposable copy. The tree I am handing back is the tree I measured.
