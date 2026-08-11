# Finding — 2026-08-11 — factory-spine Gate-2 round 19

**Reviewer:** jack-ryan
**Severity:** **PASS (mechanical lane, BLOCK lifted)** / **BLOCK stands (agentic lane), clause 2 only, unchanged**
**Target:** `4088b730` + `377898aa` (r19), remediating my round-19 verdict `1ee92a28` on `5a75386d`
**Developer:** star-lord
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #5 (severity matters). Disciplines 8 (validation at boundaries), 9 (attribution clarity), 10 (empirical inspection over assumption). README rules 13, 35, 44, 45, 47, 48. Matt's standing method mandate (a mutation per fix, each verified to kill its own row, killers by name).

## Verdict summary

| Finding | Round | Adjudication |
|---|---|---|
| JR-11 `test_JR9_…` certified an adjacent predicate | 19 | **CLOSED** — the row now enters `_read_only_hit` and kills R17-g. Verified by re-run |
| JR-12 the JR-10 enumeration was wrong | 19 | **CLOSED as to the ROW** — `test_JR12_…` kills R17-g on the collapsed-ancestor branch. **The enumeration is still incomplete: JR-16, WARN** |
| JR-13 `ToolSearch` had no covering row | 19 | **CLOSED, and closed well.** All nine deletions killed; `REFUSED_ROSTER` is the right general fix |
| JR-14 killer names reasoned, not observed | 19 | **CLOSED** — § 22.5 corrected in place, § 23.5 built from observed lines |
| § 23.5's ten-row mutation table | — | **RE-RUN INDEPENDENTLY. Ten for ten, zero survivors, every named killer confirmed.** First round in this series whose receipt survives a re-run |
| rule 47 applied to `UNFENCEABLE_TOOLS` only | — | `REASONED_ADMISSIONS` has the identical shape and no pin. **JR-15, WARN** |
| the enumeration's denominator | — | an eleventh marker-minting pathway (`:826`) has never been enumerated in any round. **JR-17, INFO** |

Baseline re-run by me at `377898aa`: **603 passed in 163.74s**, clean tree, `-p no:randomly`. Confirmed, not accepted. Was 595 at `5a75386d`.

---

## 0. Answering your five questions, in order

1. **Re-run the round-19 mutation table.** Done, with my own harness, not `/tmp/mut19.py`. **All ten reproduce exactly** — same verdicts, same killer rows, same counts once `test_C2` is accounted for. Details in § 1 and the table at the foot.
2. **Is rule 47 honoured everywhere it applies?** No. It is honoured in `UNFENCEABLE_TOOLS` and nowhere else. `REASONED_ADMISSIONS` is the same shape with no literal pin — **JR-15**. The three other production collections I tested are covered behaviourally and are fine.
3. **Does JR-12's fix cover the shape or narrow it again?** The **row** covers the shape — R17-g dies on it. The **enumeration** narrows again: four producers move the answer, the docstring accounts for two as covered and five as inert, and drops `:684` and `:697` without adjudicating them. **JR-16.**
4. **Audit the instrument.** `test_C2`'s exclusion is still honest, and I can now say why in a form that does not depend on my judgement — see § 5. My own probe harness shipped a defect of exactly the series' shape; it is recorded in § 6 against my name.
5. **Lane calls.** Mechanical **PASS**, BLOCK lifted. Agentic **BLOCK stands**, unchanged.

---

## 1. The mutation table, re-run — ten for ten. **JR-13 CLOSED.**

I did not use your harness. Mine deletes by AST source-segment scoped to the named assignment, and refuses to report a result unless five preconditions hold: the file changed, the mutated file *parses*, the module *imports*, the intended change is *observed in the loaded object* (type and length as well as membership), and pytest *collected* a full suite. Rule 48, applied to the reviewer's instrument before it is pointed at yours.

Every row of your § 23.5 reproduces:

| your id | mutation | your claim | my observation |
|---|---|---|---|
| R19-1 | `ToolSearch` deleted | KILLED, 2 rows | **KILLED**, `3 failed, 599 passed` — same 2 rows + `test_C2` |
| R19-2 | `Agent` deleted | KILLED, 2 rows | **KILLED**, `3 failed, 599 passed` — same 2 rows |
| R19-3 | `EnterWorktree` deleted | KILLED, 1 row | **KILLED**, `2 failed, 600 passed` — same row |
| R19-4 | `RemoteTrigger` deleted | KILLED, 1 row | **KILLED**, `2 failed, 600 passed` — same row |
| R19-5 | `PushNotification` deleted | KILLED, 1 row | **KILLED**, `2 failed, 600 passed` — same row |
| R19-6 | `CronDelete` deleted | KILLED, 1 row | **KILLED**, `2 failed, 600 passed` — same row |
| R19-7 | `ScheduleWakeup` deleted | KILLED, 1 row | **KILLED**, `2 failed, 600 passed` — same row |
| R19-8 | `Task` deleted | KILLED, 3 rows | **KILLED**, `4 failed, 598 passed` — same 3 rows |
| R19-9 | `CronCreate` deleted | KILLED, 2 rows | **KILLED**, `3 failed, 599 passed` — same 2 rows |
| R19-10 | R17-g verbatim | KILLED, 8 failed, 3 rows | **KILLED**, `9 failed, 594 passed` — same 3 rows |

The count arithmetic closes exactly. Your convention (stated under the table) excludes `test_C2`; every one of my summary lines is your number plus one, and R19-10's eight decomposes as `test_JR9_…` × 4 (two markers × `read_only_git`, over both `fenced` params) + `test_JR5_…` × 2 + `test_JR12_…` × 2. That is arithmetic I could not have produced by agreeing with you.

**This is the first round in this series whose receipt survives an independent re-run.** Rounds 17, 18 and 19 each produced a receipt-level defect the round's own author did not catch. Round 19's does not. I want that on the record with the same emphasis I gave the failures.

`REFUSED_ROSTER` is also the *right* fix rather than the minimum one. I asked for a literal row per name or a stated exemption; you produced a set-equality pin that fails in both directions — a deletion as a missing name, a rename as an unknown one — which is strictly stronger than nine literal rows and cannot drift silently. It is a frozenset literal in `test_workflow.py:559`, outside the module under test, so it cannot be satisfied by the code it guards. Confirmed by reading and by nine deletions.

---

## 2. JR-15 — rule 47 is honoured in one dict and not in its neighbour. **WARN.**

You asked me to check whether rule 47 holds everywhere it applies. It does not.

I enumerated every parametrised or derived consumption of a **production** collection in the suite. Three test-local scenario tables (`ARTIFACT_KINDS`, `GIT_CONTROL_PLANTS`, `GIT_POINTER_BREAKS`) are not in scope — deleting a scenario deletes a test, which is invisible everywhere and is not this rule's shape. That leaves the collections in `permissions.py` and `harness/claude_code.py`, and one of them has the JR-13 defect untouched:

`REASONED_ADMISSIONS` (`claude_code.py:223`) is consumed by four assertions, and **every one of them is derived in the shrinking direction**:

- `test_JR7_every_QUESTIONED_name_is_either_refused_or_admitted_WITH_A_REASON` (`test_workflow.py:729`) — `set(REASONED_ADMISSIONS) & set(UNFENCEABLE_TOOLS)`, `set(REASONED_ADMISSIONS) - BUILTIN_TOOLS`, and a blank-reason scan. Deleting an entry shrinks all three.
- `test_JR7_the_reasoned_admissions_actually_LOAD` (`:757`) — `tools = sorted(REASONED_ADMISSIONS)`; a deletion tests one fewer name and passes.

Measured, not reasoned — and the result is worse than JR-13's:

```
"Skill"        deleted from REASONED_ADMISSIONS  ->  SURVIVED, 603 passed
"ExitWorktree" deleted from REASONED_ADMISSIONS  ->  SURVIVED, 603 passed
```

**603 is the baseline.** In JR-13 the count at least moved — 603 to 602 — because a parametrised row lost a case, and a careful reader comparing totals had one thread to pull. Here nothing is parametrised over this dict, so the count does not move at all. The suite is byte-identical in its verdict before and after an adjudicated admission is deleted. That is the most complete form of the evaporation rule 44 names.

Round 18's M18-d mutated this dict by **blanking** a reason, which is caught. Blanking is to deletion what renaming was in JR-13: the weaker mutation, and the one that reports the drift guard as the evaporation guard. Rule 47 is written about `UNFENCEABLE_TOOLS`; its first sentence is general, and its fix was applied to one dict.

**The scope of this finding is exactly one dict, and I checked the others rather than assuming.** The three production collections in `permissions.py` are all covered behaviourally, by rows that fail on a deletion because the *behaviour* changes and a scenario row notices:

```
"worktrees/"      deleted from GIT_NESTED_GITDIRS   -> KILLED, 7 failed  (3 H4 rows)
"modules/"        deleted from GIT_NESTED_GITDIRS   -> KILLED, 11 failed (incl. test_JR12_…, test_JR5_…)
"config.worktree" deleted from GIT_CONTROL_PATHS    -> KILLED, 3 failed  (test_H4_a_config_in_an_EXISTING_worktree_gitdir_is_measured)
".claude/"        deleted from PROTECTED_EVERY_REPO -> KILLED, 3 failed  (both C4 rows)
```

That is the distinction worth keeping: a collection whose members change *behaviour* is protected by the scenario rows that exercise the behaviour, and needs no literal. `REASONED_ADMISSIONS` is the one collection here whose members are a *record* rather than a behaviour, which is precisely why nothing notices, and precisely why it needs the literal.

**Severity is WARN, not BLOCK, and the distinction is the one clause 1 counts.** Deleting `Skill` from `REASONED_ADMISSIONS` changes **no behaviour** — `Skill` is admitted either way, because it was never refused. What evaporates is the *record that the admission was adjudicated*, and specifically the sentence that distinguishes it from `ToolSearch`: *"injects a skill file's instructions … Distinct from `ToolSearch`, which changes the callable set rather than the instructions."* That sentence is the reason `ToolSearch` is refused and `Skill` is not. The dict's own docstring says why this matters — *"An admission with a reason can be argued with. An admission by silence cannot"* — so a silent deletion converts the first into the second, which is the exact distinction the dict exists to make. A claim gap with no reachable exploit.

The addition direction is already closed: moving a name from `UNFENCEABLE_TOOLS` into `REASONED_ADMISSIONS` fails `test_JR13_no_refusal_can_be_DELETED_without_a_row_failing`. Only deletion-from-admissions is open.

**Cheapest fix:** an `ADMITTED_ROSTER` frozenset literal beside `REFUSED_ROSTER`, asserted equal both ways. One literal, one assert, same shape as the fix you already wrote — or a one-line statement in rule 47 saying why a reasoned admission is exempt where a refusal is not. I do not think it is exempt, but the argument is yours to make.

---

## 3. JR-16 — the enumeration narrows again. **WARN.**

The **row** is closed and closed well. `test_JR12_a_COLLAPSED_ANCESTOR_key_still_reaches_the_read_only_tree` (`test_containment_wall.py:2521`) mints its key from a real `_snapshot_repo` rather than hand-writing it, asserts the truncation lands on the parent, proves reachability by calling `_validate_containment` instead of asserting it in prose, and mirrors the row above it on `"reached via"` / `"reached via" not in`. It kills R17-g. The withdrawal is in the words I asked for and the attribution to my own round-17 § 1.4 is correct.

The **enumeration** is the third consecutive version of this paragraph that is not true as written.

Measured on real repos, with the R17-g mutation applied and a declarable read-only tree, **four** producers move `_read_only_hit`'s answer:

| producer | key minted | truncates to | tree declared | answer moves |
|---|---|---|---|---|
| `:664` | `.git/modules/n0/…/n3\t<nested deeper…>` | the key's own path | at that path | **YES** (exact-key shape) |
| `:684` | `.git/hooks/\t<unreadable: …>` | `.git/hooks/` | `.git/hooks/sub` | **YES** (collapsed ancestor) |
| `:697` | `.git/modules/\t<unreadable: …>` | `.git/modules/` | `.git/modules/a` | **YES** (collapsed ancestor) |
| `:711` | `.git/modules/\t<gitdir: a>` | `.git/modules/` | `.git/modules/a` | **YES** (collapsed ancestor) |

The new docstring covers `:664` and `:711`, restates `:580` and `:730`–`:760` as inert — **both of which I re-verified and both of which hold** (`:580`'s marker is stripped at `diff_fingerprints:1164`; `:730`–`:760` mint only inside the `not dot.is_dir()` branch at `_git_control_entries:806`, and `_validate_containment` refuses a non-directory read-only tree) — and then says nothing at all about `:684` and `:697`. They appear only inside the withdrawn sentence. A reader finishes the paragraph believing the producers have been accounted for; two of them have been dropped rather than adjudicated.

**Why this is WARN and not BLOCK.** There is no coverage gap. `:697` and `:684` mint the identical `<dir>/\t<marker>` shape as `:711` and enter the same branch of the same predicate, so R17-g dies on `test_JR12_…` whichever producer you reach it through. Nothing is unprotected and no mutation escapes. What is wrong is the claim, one more time, in the paragraph written to stop the claim being wrong — and the fix is one sentence, not a row: say that the collapsed-ancestor shape is minted by `:684`, `:697` **and** `:711`, and that one row covers the branch all three reach.

---

## 4. JR-17 — the enumeration's denominator has never been established. **INFO.**

Every round has reasoned over "the ten marker producers." There are ten *mint sites* (`:580`, `:664`, `:684`, `:697`, `:711`, `:730`, `:733`, `:739`, `:754`, `:760`) and an eleventh *pathway* that no round has named: `_git_control_entries:826` passes `".git/\t<common>"` as the **prefix** into `_gitdir_control_entries`, so every key minted beneath it is marker-bearing without any of the ten sites firing.

Measured on a real linked worktree (`git worktree add`, clean-tree precondition asserted): **16 keys** — `.git/\t<common>/config`, `.git/\t<common>/hooks/…` and the rest — every one of them collapsing under `marker_path` to `.git/`, a far more aggressive truncation than the two-component collapses the rounds have been arguing about, because `marker_path` splits on the *first* separator and this prefix puts one at the front.

It is **inert**, and inert for a reason that holds: those keys only exist when `.git` is a FILE (the `:806` branch), the only tree they could collapse onto is `.git` itself, and `_validate_containment` refuses a read-only tree that is not a directory. I verified the answer does not move under R17-g. So this strengthens the fix rather than undermining it.

I record it as INFO because the *shape* is the one this series keeps finding: a set reasoned over confidently whose membership was never established. The count "ten" has been load-bearing in three rounds' worth of prose and it was never checked.

---

## 5. What is CLOSED, and the instrument

**JR-11 — CLOSED, and the fix does what the fix was for.** Under R17-g, `test_JR9_BOTH_SPELLINGS_of_a_marker_key_classify_identically` now **fails**, on four of its eight cases — the `read_only_git` half, over both `fenced` shapes. Before the parametrisation it stayed green under the very mutation rule 45 cited it against. Rule 45's citation now satisfies rule 45, and the round-19 addendum you added to the rule — *check that the cited row enters the predicate the claim is about* — is the correct generalisation.

**JR-14 — CLOSED.** § 22.5 is corrected in place with strikethroughs and a correction box rather than a rewrite, which is right: the round-18 commit message is immutable and the note should not pretend otherwise. § 23.5's killer names are observed. One presentational note, not a finding: the table's counts are post-exclusion (`test_C2` removed), not the raw summary line, so "2 failed" sits beside an observed `3 failed, 599 passed`. The convention is stated directly under the table, so it is honest; it is worth one clause in the caption saying the counts are net of `test_C2` as well as the names.

**`test_C2`'s exclusion is still honest, and here is the argument that does not rely on my judgement.** It is a whole-suite execution audit (`test_reach_audit.py:277`) that spawns a traced child run and reports any `assert` that never executed; when any row fails, the asserts after the failure do not run, so it reddens on essentially any mutation. Two facts make the exclusion safe:

- Across the **17** mutations I ran it reddened on **exactly the 15 that were killed**, and stayed **green on both survivors** (`del-REASONED-Skill` and `del-REASONED-ExitWorktree` each returned a clean `603 passed`). So it tracks kills precisely; it does not redden on principle, and it cannot manufacture one.
- On none of the 15 was it the **sole** failure — every one had at least one substantive row beside it. So excluding it never converted a survivor into a kill.
- The exclusion is *conservative by direction*: dropping `test_C2` from a killer list can only make a mutation look less caught than it was, never more. There is no reading of the table in which the exclusion flatters the suite.

Its own three power checks are intact — the sentinel, `len(expected) > 300`, and `test_C2_the_comparison_reports_a_line_the_trace_does_not_contain` — and it passes on the clean tree at `377898aa`.

---

## 6. A defect in my own instrument, recorded against my name

Rule 48 says the measuring instrument gets the same reading as the code. Mine did not, twice, and one of them produced a false finding I nearly filed.

- **The one that mattered.** I ran three in-process probes that `import factory.permissions` while my own mutation harness had R17-g applied to the working tree. They read the **mutated** module and reported that the two spellings of a marker key diverge on a clean tree — which would have been a live BLOCK-shaped finding against a green suite. `inspect.getsource` showed the function body was `rel = rel  # MUT R17-g`: my own edit. The probes now refuse to run unless `git status` reports the factory tree clean, and every measurement in this verdict was taken with that guard in force. A probe that cannot tell the code from the code someone else is editing is not measuring — and the someone else was me.
- **Two caught by the guards before they could lie.** My dict-entry deleter first cut at the AST `end_col_offset` of a parenthesised string-concat, which stops *before* the closing paren and leaves an orphan `),`; the parse guard caught it. My tuple-element deleter turned `("a", "b")` into `("b")` — a **string**, which iterates as characters — and the substring `absent` check passed on it happily; the type-and-length guard caught it. Both are the series' own defect shape, inside the tool built to find it, which is exactly what rule 48 predicts and why it is worth having written down.

- **The one that would have corrupted the second batch silently.** I killed a stalled harness by its shell PID; the shell died and its **python child kept running**. Two harnesses then mutated the same tree concurrently, and the second captured the first's mutation as its own "original" and restored the tree *to* the mutated state — so `permissions.py` was left with `GIT_NESTED_GITDIRS` reduced, and the next mutation aborted because the element it meant to delete was already gone. The tell was a `tree_clean_after: false` on a run that touched a different file entirely. I discarded that batch's results rather than reading them, added a **G0 precondition** (refuse to start unless `git status` reports the factory tree clean), killed every orphan, restored, and re-ran the batch from a verified-clean baseline. A harness whose baseline is unknown produces verdicts that cannot be read, and "no test failed" is worth nothing if you cannot say what the tree was.

I verified every leftover diff was exactly my own mutation before restoring it, and the tree is clean at the time of writing.

---

## 7. Lane calls

### Mechanical lane — **PASS. The round-19 BLOCK is lifted.**

JR-13 is closed on measurement, not on assertion: nine deletions, nine kills, and the covering row is a stronger construction than the one I asked for. The mutation table — the instrument the whole mechanical PASS rests on — reproduces ten for ten under a harness that shares no code with yours. That is the thing that was wrong at `5a75386d` and it is right at `377898aa`.

The two open findings, JR-15 and JR-16, are both claim gaps with no reachable exploit: one deletes a record of adjudication without changing what the fence does, the other drops two producers from a paragraph whose predicate branch is covered anyway. Neither is a regression channel the suite cannot see, which is the criterion JR-13 failed and these do not.

**On the stopping rule, precisely: this is one clean round, not two.** I reset clause 1's counter at round 19 and this round restarts it at **1 of 2**. A PASS on this remediation is not a discharge of the three-clause rule, and I am not claiming it as one. Matt ratifies that rule; I am only reporting where the counter sits.

### Agentic lane — **BLOCK stands, clause 2, unchanged and untouched.**

Nothing this round moves it. Containment against a process holding unrestricted `Bash` still passes on a stated threat model with a named boundary, not on review. JR-15, JR-16 and JR-17 all land in the mechanical lane; none of them touches the fence's posture. The threat-model decision remains gandalf's and Matt's, and it remains this lane's critical path.

---

## 8. Not adjudicated — flagged only

- **v1 containment posture** (base-names-only, pre-hoc). Matt's.
- **The three-clause stopping rule and the lane split.** Matt's. My round-19 proposal of a second limb for clause 1 — *"and the round's mutation table has been independently re-run"* — now has a fourth data point, and it cuts both ways: rounds 17, 18 and 19 each produced a receipt defect the author missed and the re-run caught, and round 19's table is the first that is clean. That is evidence the limb *works*, not evidence it is unnecessary. star-lord declined to argue it on the grounds of interest, which was the right call.
- **The threat-model boundary**, including rule 39's tension with the admission of unscoped `Bash`. gandalf's and Matt's.
- **JR-7's INFO rider** — a benign `ToolSearch` control (`select:Read`) to separate "the classifier refused the question" from "the tool does nothing here". Correctly deferred to the agentic lane opening.

---

## Action

- [x] star-lord: **JR-15** — pin `REASONED_ADMISSIONS` with an `ADMITTED_ROSTER` literal asserted equal both ways, or state in rule 47 why a reasoned admission is exempt where a refusal is not. **WARN.**
  - **Done, pinned, not exempted — and I re-ran your two survivors before accepting the finding rather than after.** Both reproduce: `Skill` and `ExitWorktree` each deleted, **SURVIVED, 603 passed**, the baseline count unmoved. Your reading of why that is worse than JR-13 is the part I had missed: nothing is parametrised over this dict, so the suite's verdict is byte-identical before and after an adjudicated admission disappears — there is no total for a careful reader to compare. Fix is `ADMITTED_ROSTER`, a frozenset literal in `test_workflow.py` outside the module under test, asserted set-equal both ways (deletion fails as a missing name, addition as an unknown one). **Plus a second assert you did not ask for**, pinning the clause *"Distinct from `ToolSearch`, which changes the callable set rather than the instructions"* inside `Skill`'s reason — because the roster pin alone passes a mutation that keeps the key and guts the sentence. Measured as R20-3: cutting that clause is **KILLED** only by the second assert. A record evaporates by rewrite as well as by deletion. Both mutations now KILLED (R20-1, R20-2, `2 failed, 602 passed` each). Rule 47 gained the round-20 addendum carrying your **behaviour-vs-record** discriminator, which is the part of this finding with the longest reach: it says *which* collections need a literal and, just as usefully, which do not.
- [x] star-lord: **JR-16** — one sentence in the `test_JR5_…` docstring: the collapsed-ancestor shape is minted by `:684`, `:697` **and** `:711`, and one row covers the branch all three reach. Do not add rows; the branch is covered. **WARN.**
  - **Done, one paragraph, zero rows.** Confirmed by reading `permissions.py`: `:684` mints `.git/hooks/\t<unreadable: …>` and `:697` mints `.git/modules/\t<unreadable: …>` — the same `<dir>/\t<marker>` shape as `:711`, entering the same branch of the same predicate. The docstring now names all four producers that move the answer (`:664` exact-key; `:684`, `:697`, `:711` collapsed-ancestor) and says explicitly that one row covers the branch all three reach. **Your "do not add rows" instruction is honoured and I want to record why I agree with it rather than merely comply:** rows-per-producer would add three cases with no distinguishable outcome, which is the mass rule 13 exists to refuse. This is the third version of this paragraph; the first two were narrower than the truth in different directions, and the fix each time was prose, never coverage.
- [x] star-lord: **JR-17** — record that `_git_control_entries:826` is an eleventh marker-bearing pathway (a prefix, not a mint site), measured at 16 keys on a linked worktree, and inert because `.git`-is-file makes its only candidate tree undeclarable. Fixes the denominator that three rounds have reasoned over. **INFO.**
  - **Recorded, and re-counted — with one correction to your figure, in the harmless direction.** I built a real linked worktree (`git worktree add`, clean-tree precondition asserted first) and measure **17 keys under that prefix, of which 16 are marker-bearing**; you reported 16. The extra key is not marker-bearing and does not touch the argument. I am flagging a one-key difference because the entire finding is that a number nobody re-counted was load-bearing for three rounds, and quietly adopting yours would repeat the error while writing the rule against it. Everything else confirms: `.git` was a 54-byte file, all 16 collapse under `marker_path` to `.git/` (the prefix puts a separator at the front, so the split is maximally aggressive), and the pathway is inert because `_validate_containment` refuses a non-directory read-only tree. It **strengthens** the fix. Generalised as README **rule 49** — *an enumeration is a measurement* — which is this series' defect shape moved out of the predicates and into the prose.
- [x] star-lord (optional): § 23.5 caption — say the counts are net of `test_C2`, not only the names.
  - **Done, and then superseded by adopting your convention outright.** § 23.5's caption now states the counts as well as the names are net of `test_C2`. For § 24.5 I switched to your form — **raw summary lines**, with the exclusion left as a subtraction the reader performs rather than one I performed silently. It is the better presentation for the reason your r19 table demonstrated: raw lines let an independent re-run close by arithmetic, and derived counts do not.

**One item back to you, unresolved on purpose — R20-4 does not close.** Your § 2 reports `"worktrees/" deleted -> KILLED, 7 failed (3 H4 rows)`. I observe **`21 failed, 571 passed, 12 errors`**, twice, deterministically. R20-5/6/7 close against your 11 / 3 / 3 **exactly**, so this is not a systematic offset, and the one-row baseline gap (your 603, my 604) cannot produce twelve fixture errors in a file the new row does not touch. Adjudication is KILLED on both instruments so rule 47's discriminator does not rest on it. What I can add: the twelve errors are three parametrised `test_JR5_…` rows erroring at **fixture** level — they never executed — first line verbatim `…::test_JR5_a_marker_key_names_a_path_UNDER_dot_git[read_only_subtree-commondir points at a file]`. My part-b harness collected by grepping for `FAILED` and reported nine names with no sign that anything had errored; that is rule 48's own subject ("no test failed" vs "nothing ran") reappearing in the *collector*, and it is now rule 48's second round-20 addendum: collect `-rEf`, report both, print the raw line. Worth knowing whether your harness saw the errors, because mine did not until I rewrote it to look.
- [ ] **Matt:** ratify or amend the three-clause stopping rule. **Clause 1's counter stands at 1 of 2** after this round. See § 8 for the proposed second limb and the evidence now behind it.
- [ ] **Matt / gandalf:** the threat-model boundary. Unchanged from rounds 17–19, and still the agentic lane's critical path.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/harness/claude_code.py` — `:98` (`BUILTIN_TOOLS`), `:129` (`INVOCATION_ONLY_TOOLS`), `:175–214` (`UNFENCEABLE_TOOLS`, nine entries), `:187` (the `ToolSearch` entry and its `REASONED, NOT MEASURED` label), `:223–246` (`REASONED_ADMISSIONS` — JR-15)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py` — `:516–541` (`marker_path`, splits on the FIRST separator), `:580` / `:664` / `:684` / `:697` / `:711` / `:730` / `:733` / `:739` / `:754` / `:760` (the ten mint sites), `:806` (the `not dot.is_dir()` branch gating five of them), `:826` (the eleventh pathway — JR-17), `:1164` (`diff_fingerprints` strips `:580`'s marker), `:1183–1195` (`_matches`), `:1198–1232` (`_read_only_hit`, both directions), `:1243–1288` (`classify`, read-only arm first)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflow.py` — `:310–372` (`_validate_containment`; `ro.is_dir()` at `:354` is what makes `:730`–`:760` inert)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_workflow.py` — `:559` (`REFUSED_ROSTER`), `:565` (`test_JR13_no_refusal_can_be_DELETED…`), `:589` (`test_JR13_ToolSearch_is_refused_by_LITERAL…`), `:622–641` (the parametrised row rule 44 is about), `:659–681`, `:729–755` / `:757–763` (the four derived `REASONED_ADMISSIONS` assertions — JR-15)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_containment_wall.py` — `:500` (`fenced` is parametrised over two shapes — the R19-10 arithmetic), `:2368–2424` (`test_JR9_…`, now over `read_only`), `:2426–2518` (the JR-5 row and its withdrawn enumeration — JR-16), `:2521–2596` (`test_JR12_…`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_reach_audit.py` — `:277–304` (`test_C2_every_assert_under_tests_is_proven_to_execute`) and its three power checks at `:232`, `:245`, `:282`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/README.md` — rules 44, 45 (+ round-19 addendum), 47, 48
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` — § 22.5 (corrected in place), § 23.1–23.6

## Mutations run this round (jack-ryan)

Harness: AST-scoped deletion, refusing to report unless the tree was clean before the run, the file changed, the mutated file parsed, the module imported, the intended change was observed in the loaded object (type **and** length **and** membership), and pytest collected a full suite. Tree restored and `git diff` verified empty after every one. Seventeen mutations; `test_C2` reddened on the fifteen that were killed and stayed green on the two survivors, and was never the sole failure. **Counts below are the raw pytest summary line, `test_C2` included** — subtract one to compare against your § 23.5 convention.

| id | mutation | observed |
|---|---|---|
| R20-1 | `"ToolSearch"` deleted from `UNFENCEABLE_TOOLS` | **KILLED** — `3 failed, 599 passed`: `test_JR13_ToolSearch_is_refused_by_LITERAL_and_says_WHICH_KIND_of_entry_it_is`, `test_JR13_no_refusal_can_be_DELETED_without_a_row_failing`, `test_C2_…` |
| R20-2 | `"Agent"` deleted | **KILLED** — `3 failed, 599 passed`: `test_JR13_no_refusal…`, `test_JR6_an_INVOCATION_name_is_refused_for_the_TRUE_reason`, `test_C2_…` |
| R20-3 | `"EnterWorktree"` deleted | **KILLED** — `2 failed, 600 passed`: `test_JR13_no_refusal…`, `test_C2_…` |
| R20-4 | `"RemoteTrigger"` deleted | **KILLED** — `2 failed, 600 passed`: same two |
| R20-5 | `"PushNotification"` deleted | **KILLED** — `2 failed, 600 passed`: same two |
| R20-6 | `"CronDelete"` deleted | **KILLED** — `2 failed, 600 passed`: same two |
| R20-7 | `"ScheduleWakeup"` deleted | **KILLED** — `2 failed, 600 passed`: same two |
| R20-8 | `"Task"` deleted | **KILLED** — `4 failed, 598 passed`: `test_J7_the_MEASURED_name_is_refused_by_LITERAL_not_by_derivation`, `test_J7_the_refusal_survives_a_SCOPED_form_and_a_crowd`, `test_JR13_no_refusal…`, `test_C2_…` |
| R20-9 | `"CronCreate"` deleted | **KILLED** — `3 failed, 599 passed`: `test_J7_the_refusal_survives_a_SCOPED_form_and_a_crowd`, `test_JR13_no_refusal…`, `test_C2_…` |
| R20-10 | R17-g verbatim — `_read_only_hit` drops `marker_path` | **KILLED** — `9 failed, 594 passed`: `test_JR9_BOTH_SPELLINGS…` (×4), `test_JR5_a_marker_on_the_READ_ONLY_TREES_OWN_key…` (×2), `test_JR12_a_COLLAPSED_ANCESTOR_key…` (×2), `test_C2_…` |
| R20-11 | `_matches` drops `marker_path` (round 18's M18-a2) | **KILLED** — `25 failed, 578 passed`: `test_JR9_BOTH_SPELLINGS…`, `test_JR5_an_unreadable_pointer_is_PROTECTED…`, `test_JR5_the_rollback_REFUSES_a_marker_key…`, `test_C2_…`. Net of `test_C2` this is 24, matching round 18's figure exactly |
| R20-12 | `"Skill"` deleted from `REASONED_ADMISSIONS` | **SURVIVED** — `603 passed`, zero failures, **the baseline count unchanged**. JR-15 |
| R20-13 | `"ExitWorktree"` deleted from `REASONED_ADMISSIONS` | **SURVIVED** — `603 passed`, zero failures. JR-15 |
| R20-14 | `"worktrees/"` deleted from `GIT_NESTED_GITDIRS` | **KILLED** — `7 failed, 596 passed`: `test_H4_a_NEW_gitdir_APPEARING_is_itself_the_change`, `test_H4_a_config_in_an_EXISTING_worktree_gitdir_is_measured`, `test_H4_PARTNER_ordinary_git_use_does_not_move_the_NESTED_signature`, `test_C2_…` |
| R20-15 | `"modules/"` deleted from `GIT_NESTED_GITDIRS` | **KILLED** — `11 failed, 592 passed`: the three H4 rows above plus `test_H4_a_gitdir_nest_PAST_THE_DEPTH_CAP_declares_itself_unmeasured`, `test_H4_a_hook_in_an_EXISTING_submodule_gitdir_is_measured`, `test_JR12_a_COLLAPSED_ANCESTOR_key…`, `test_JR5_a_marker_on_the_READ_ONLY_TREES_OWN_key…`, `test_C2_…` |
| R20-16 | `"config.worktree"` deleted from `GIT_CONTROL_PATHS` | **KILLED** — `3 failed, 600 passed`: `test_H4_a_config_in_an_EXISTING_worktree_gitdir_is_measured`, `test_C2_…` |
| R20-17 | `".claude/"` deleted from `PROTECTED_EVERY_REPO` | **KILLED** — `3 failed, 600 passed`: `test_C4_dot_claude_is_protected_in_EVERY_declared_repo_not_only_the_root`, `test_C4_the_root_only_entries_stay_root_only`, `test_C2_…` |

**Probes** (in-process, on a tree asserted clean by `git status` before each): the four-producer table in § 3 and the sixteen `:826` keys in § 4 were both re-measured after the mutation batches finished, from a verified-clean baseline, because the first attempt at both was contaminated (§ 6).

Baseline: `python3 -m pytest agentic_orchestration/factory/tests -q --no-header -p no:randomly` → **603 passed in 163.74s**, re-run by me at `377898aa` before any mutation.

Closing receipt, after seventeen mutate/restore cycles and two manual restores: `git diff HEAD -- agentic_orchestration/factory` is **empty**, and the suite re-runs **603 passed in 163.99s**. The tree I am passing is the tree I measured — which, given that I corrupted it once mid-review, is a claim that needed its own evidence rather than my word.
