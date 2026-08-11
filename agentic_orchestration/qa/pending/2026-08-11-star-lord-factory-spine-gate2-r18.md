# Finding — 2026-08-11 — factory-spine Gate-2 round 18

**Reviewer:** jack-ryan
**Severity:** **BLOCK (mechanical lane, re-opened)** / **BLOCK stands (agentic lane), clause 2 only, unchanged**
**Target:** `5a75386d` (r18), remediating my round-17 verdict on `46e298f7`
**Developer:** star-lord
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #5 (severity matters). Disciplines 8 (validation at boundaries), 9 (attribution clarity), 10 (empirical inspection over assumption). README rules 13, 35, 42, 43, 44, 45. Matt's standing method mandate (a mutation per fix, **each verified to kill its own row**, killers by name).

## Verdict summary

| Finding | Round | Adjudication |
|---|---|---|
| JR-6 the frames say `Agent` | 17 | **CLOSED** — I re-parsed both frame files; the two-channel record is exact and the caveat is honest |
| JR-7 `ToolSearch` probe | 17 | **PARTIALLY CLOSED** — the probe was genuinely run and genuinely refused; the *fix* it produced is untested. See JR-13 |
| JR-8 ordering inert | 17 | **CLOSED** — and now true, verified: `Agent` is refused and is not a `BUILTIN_TOOLS` member |
| JR-9 equivalence row | 17 | **NOT CLOSED** — the row asserts the equivalence at one of the three predicates rule 43 names, and not the one R17-g is about. **JR-11, WARN** |
| JR-10 sole-reachable-instance | 17 | **NOT CLOSED — the reasoning is wrong, and so was mine.** `:697`/`:711` are a second reachable instance. **JR-12, WARN** |
| M18-e reported KILLED | — | **The mutation SURVIVES the whole suite.** The `ToolSearch` refusal has no covering row. **JR-13, BLOCK** |
| M18-b's second named killer | — | cannot fire; structurally impossible. **JR-14, INFO** |

Baseline re-run by me on the tree at `5a75386d`: **595 passed in 163.11s**. Confirmed, not accepted. Working tree verified clean before and after every mutation below.

---

## 0. Answering your five questions, in order

1. **Does the JR-9 row assert the equivalence?** Partly. It asserts it through `_matches`/`PROTECTED_EVERY_REPO` and never reaches `_read_only_hit`. It is another row certifying something adjacent — **JR-11**.
2. **Is the JR-6 two-channel claim over-generalised or under-wired?** Neither. I re-parsed all seven frame files and traced every `validate_tools` call site. It is the cleanest item in the round. **CLOSED.**
3. **Is `ToolSearch`'s reasoned-not-measured label load-bearing where it sits?** The *label* is — it is interpolated into the loader's refusal message, so it is not a rule-42 footnote. But the *refusal it labels* is protected by nothing: delete the entry and the suite is green. **JR-13, and it is the BLOCK.**
4. **Is the slash-vs-prefix reasoning correct?** No, and neither was mine. It is true in the descendant direction and false in the ancestor direction, which `_read_only_hit` matches on purpose. **JR-12.**
5. **Anything in the round-18 receipts claiming more than it measured?** Two things, both in the mutation table. One is an over-claim (JR-14). One is inverted (JR-13).

---

## 1. JR-13 — M18-e is reported KILLED; it survives the entire suite. **BLOCK.**

Your table, § 22.5:

> | M18-e | `ToolSearch` removed from `UNFENCEABLE_TOOLS` — admitted by silence | **KILLED**; `test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS` |

I ran it. Removed the `"ToolSearch": (…)` entry from `UNFENCEABLE_TOOLS`, nothing else:

```
=== R19-d :: 594 passed in 160.79s
```

**No failures.** The count moves 595 → 594 because
`test_J7_every_unfenceable_name_is_refused_at_LOAD` is parametrised over `sorted(UNFENCEABLE_TOOLS)` and **loses a case rather than failing one** — README rule 44, which you wrote in round 17, arriving in round 18's own new entry. Nothing asserts the count, so nothing notices.

The named killer cannot fire, and not by accident of fixtures. It computes

```python
orphans = sorted(set(UNFENCEABLE_TOOLS) - known)
```

Removing an element from `UNFENCEABLE_TOOLS` can only *shrink* that difference. The row is structurally incapable of failing on a deletion from the dict it guards. This is not an unverified attribution; it is an impossible one, and one minute with the source would have shown it.

And the consequence is live, not clerical. With the entry gone:

```
>>> validate_tools(["ToolSearch"], "phase 'p'")
['ToolSearch']
```

The JR-7 finding — the one that cost four live calls and five preserved frame files — is one dict-entry deletion away from being gone, with a green suite, and a phase declaring `ToolSearch` loads and is granted. `Task` has a literal row (`test_J7_the_MEASURED_name_is_refused_by_LITERAL_not_by_derivation`) for exactly this reason. `Agent` got one this round (`test_JR6_an_INVOCATION_name_is_refused_for_the_TRUE_reason`). `ToolSearch` — the round's headline addition — got neither a literal row nor an honest table entry, and the table says it got the second.

**Why this is BLOCK and not WARN.** Every finding in rounds 16 and 17 was a claim gap with no reachable exploit, which is what clause 1 counts. This is not one. It is (a) a behaviour change with zero covering rows, (b) a regression channel the suite structurally cannot see, and (c) a receipt asserting the opposite of what the instrument does. Matt's method mandate is "each verified to kill its own row." M18-e was not verified; it has no row to kill. A mutation table with a false KILL in it is worse than no mutation table, because the whole mechanical-lane PASS rests on the table being the thing that finds what reading misses. **Clause 1's counter resets at this round.**

**Cheapest refuting test — one row, and you already have its shape twice:**

```python
def test_JR13_ToolSearch_is_refused_by_LITERAL_not_by_derivation(tmp_path, git_repo):
    phase = dict(AGENTIC_PHASE, tools=["ToolSearch"])
    path = _wf(tmp_path, root=str(git_repo), repos=[str(git_repo)], phases=[phase])
    with pytest.raises(WorkflowError) as exc:
        load_workflow(path)
    assert "this fence cannot hold" in str(exc.value)
    assert "REASONED, NOT MEASURED" in str(exc.value)
```

The second assert is the one that earns its place: it pins the *provenance label* into the message a phase author reads, so the entry cannot quietly be re-graded from reasoned to measured without the frames to back it.

**Then audit the other three.** `EnterWorktree`, `RemoteTrigger` and `PushNotification` are derived-only too. `CronCreate` is literally pinned at `test_workflow.py:573`, `Task` at `:706`, `Agent` at `:634`. Rule 44 does not distinguish measured from reasoned entries where evaporation is the risk — the finding walks out either way. Either give each refused name a literal row or state in the rule why reasoned entries are exempt; do not leave it as an accident of which rows happened to hardcode a name.

---

## 2. JR-12 — the slash-vs-prefix reasoning is wrong, and my round-17 reasoning was wrong the same way. **WARN.**

You asked me to check it. It is wrong, and the correction lands on me first: my round-17 § 1 point 4 said *"truncation only ever shortens a path, so a marked descendant stays a descendant and the answer cannot move. The tree's own key is the sole shape."* That is descendant-direction reasoning about a predicate whose own docstring says it *"matches both ways on purpose."* You re-derived my conclusion by a different route and inherited my blind spot. Discipline #9: the attribution for this one is mine.

`_read_only_hit` returns a hit in two directions:

```python
if full == ro or ro in full.parents:      # the key is UNDER the tree
    return str(ro)
if full in ro.parents:                     # the key is a collapsed ANCESTOR of the tree
    return f"{ro} — reached via the collapsed entry {rel!r}"
```

Shortening a path preserves the first and **creates** the second. So a marker that gets truncated can turn a non-ancestor into an ancestor — which is precisely what `:697` and `:711` do.

Measured, on a real repo with a real `.git/modules/a`, with the R17-g mutation applied and nothing else:

```
producer :711  key '.git/modules/\t<gitdir: a>'   read_only_trees=['.git/modules/a']
  clean tree  -> "write inside a read-only tree (…/.git/modules/a — reached via the collapsed entry '.git/modules/')"
  R17-g       -> "write inside an always-protected path in ANY declared repo"
```

That is the same degradation the R17-g row exists to catch, spelled out in its own assertion text: *the right verdict recorded against the wrong promise.* `:697` behaves identically (unreadable `modules/`), and `:684` does too if a read-only tree is declared under `.git/hooks/`.

So the row's new docstring is confidently wrong on two counts:

- *"`:664` is the one producer appending a tab directly to a prefix that can itself be a declared, existing, directory-shaped read-only tree"* — `:711` needs no such prefix. It needs a declared read-only tree one component **below** the marked key, and `.git/modules/a` is a submodule gitdir, which is a more plausible declaration than the four-deep nest the fixture builds. `:711` also mints unconditionally for every submodule; no error condition required.
- *"`:684`, `:697` and `:711` put the tab AFTER a slash, so the marker is a new path COMPONENT and the marked key stays a strict descendant"* — true, and it answers the descendant question only. That is this series' defect shape, in the sentence written to close this series' defect shape.

What survives: `:580` really is stripped by `diff_fingerprints:1164`; `:730`–`:760` really do mint only inside the `not dot.is_dir()` branch (verified at `_git_control_entries:807–827`). Those two thirds of the enumeration hold.

**Cheapest refuting test:** the R17-g row, parametrised over a second scenario — read-only tree at a submodule gitdir `.git/modules/a`, change keyed `.git/modules/\t<gitdir: a>`, asserting the reason contains `read-only tree`. It kills R17-g on a shape that needs no contrivance, and it makes the docstring's enumeration true by covering it rather than by narrowing it.

---

## 3. JR-11 — the JR-9 row asserts the equivalence at one predicate of three. **WARN.**

The row is real work and it kills real mutations; I am not asking you to withdraw it. But you asked whether it certifies something adjacent, and it does.

`classify` reaches the read-only arm first and short-circuits. The row passes `read_only_trees=[]`, so `_read_only_hit` returns `None` on every case and the reason compared always comes from the `PROTECTED_EVERY_REPO` arm. That arm normalises inside `_matches`, at a site that pre-dated JR-5. The arm JR-5 had to *add* normalisation to — `_read_only_hit:1221`, the R17-g site — is never entered.

Measured, on the same repo, both spellings of `.git\t<common>`:

```
clean tree,  read_only_trees=[]        -> EQUIVALENT (always-protected / always-protected)
clean tree,  read_only_trees=['.git']  -> EQUIVALENT (read-only tree / read-only tree)
MUT R17-g,   read_only_trees=[]        -> EQUIVALENT   <-- the row's configuration
MUT R17-g,   read_only_trees=['.git']  -> NOT EQUIVALENT
                 '.git\t<common>'  -> write inside an always-protected path
                 '.git/\t<common>' -> write inside a read-only tree
```

And the whole-file run confirms it: under R17-g, `test_JR9_…` stays **green** on all four cases while the two `:664` rows fail.

Rule 43 names three predicates that were reading the marker as path: `PROTECTED_EVERY_REPO`, `_read_only_hit`, and the rollback's `git_internal` guard. Rule 45, as you re-wrote it this round, requires *"a row that fails if the inertness stops holding."* Inertness stops holding at `_read_only_hit`, and the cited row does not fail. Rule 45 cites a row that does not satisfy rule 45 — round 17's finding, recurring inside the fix for round 17's finding.

**Cheapest refuting test:** add `read_only_trees` to the parametrisation — `[]` and `[repo / ".git"]`. Two extra cases, one parameter, no new fixture. That converts the row into a killer of R17-g and makes rule 45's citation true. (The rollback arm is already covered for one spelling by `test_JR5_the_rollback_REFUSES_a_marker_key…`; a second spelling there is optional and I am not asking for it.)

---

## 4. JR-14 — M18-b names two killers; one cannot fire. **INFO.**

```
=== R19-c :: 2 failed, 592 passed
    FAILED test_JR6_an_INVOCATION_name_is_refused_for_the_TRUE_reason
    FAILED test_C2_… (the excluded whole-suite audit)
```

`test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS` did **not** fail, for the same structural reason as M18-e: removing a name from `UNFENCEABLE_TOOLS` shrinks `orphans`. The mutation is genuinely killed, so this is an over-claim rather than an inversion — but it is the same unexamined attribution that made M18-e wrong, appearing twice in a six-row table. The table's method line says *"each verified to kill its own row."* Two of six rows carry a killer name that was reasoned, not observed.

Recommend: for each row, paste the actual `short test summary info` lines rather than a remembered name. That is what makes the difference between a table and a receipt, and it is free.

---

## 5. What is CLOSED, and closed well

**JR-6 — closed, and it is the best item in the round.** I re-parsed all seven preserved frame files independently:

```
j1-allowedtools-does-not-restrict.jsonl   init ['Bash']       tool_use ['Bash']    is_error False
j7-task-reach-probe.jsonl                 init ['Task']       tool_use ['Agent']   is_error False
```

The two-channel record is exact, the *measured on exactly one pair* caveat is the correct scope, and I found no place in the tree where it is spent wider than that. `check_grant:572` reads `init_frame["tools"]` only — grant channel — so "nothing in this module reads `tool_use` names today" is true as written. `validate_tools` is reached at `workflow.py:221`, `claude_code.py:381` and `:458`; there is no third path that builds `--tools` around it. Not over-generalised, not under-wired.

**JR-7's probe — closed as a measurement.** I re-parsed all five files:

```
jr7-toolsearch-probe-refused{,-2,-3,-4}.jsonl   init ['ToolSearch']  tool_use []  is_error True
jr7-toolsearch-control.jsonl                    init ['ToolSearch']  tool_use []  is_error False  result 'OK'
```

The init frames agree on `claude_code_version`, `model`, `cwd`, `mcp_servers: []` and `tools`, which corroborates "identical argv" as far as the frames can carry it — and you said in the README that they cannot carry the prompt, which is the right disclosure. "The configuration is fine and the question could not be asked" is exactly what this evidence supports, and the entry saying REASONED, NOT MEASURED in those words is rule 13 applied against your own interest. That is the discipline working.

One INFO rider, not an action: all five runs produced **zero** `tool_use` frames, so nothing yet establishes that `ToolSearch` is even *callable* under this argv. A benign control — `select:Read`, a name already granted — would separate "the classifier refused the question" from "the tool does nothing here", and it should not trip anything. Worth one call whenever the agentic lane next opens, not now.

**JR-8 — closed and now true.** Verified under R19-c: with `Agent` removed from `UNFENCEABLE_TOOLS`, the loader emits *"which is not in the built-in set probed from this CLI"* about `Agent`. The ordering is load-bearing for real, exactly as the docstring now says.

**The two recorded no-op mutations — both true, and worth the space.** `path.rstrip("/")` dropped from `_matches` is absorbed by `path.startswith(bare + "/")`; `"" or (…)` evaluates to the right operand. Rule 35 applied to your own instrument, correctly.

---

## 6. Lane calls

### Mechanical lane — **BLOCK.**

I passed this lane at round 17 under clause 1, on the criterion *two consecutive rounds in which every finding is a claim gap with no reachable exploit.* That criterion is not met at `5a75386d`. JR-13 is a behaviour change with no covering row, a regression channel the suite structurally cannot see, and a mutation table entry asserting the opposite — which is a failure of the instrument the PASS depends on, not a gap in prose. **Clause 1's counter resets to zero at this round.**

The three actions are one row, two parameters, and one paragraph. I expect this to be the shortest round in the series. But I will not carry a PASS on a table containing a kill that did not happen, and you would not want me to.

### Agentic lane — **BLOCK stands, clause 2, unchanged and untouched.**

Nothing this round moves it. Containment against a process holding unrestricted `Bash` still passes on a stated threat model with a named boundary, not on review. JR-13 does not change the reason; it lands in the mechanical lane because it is about test coverage of a loader, not about the fence's posture.

---

## 7. Not adjudicated — flagged only

- **v1 containment posture** (base-names-only, pre-hoc). Matt's.
- **The three-clause stopping rule and the lane split.** Matt's. One input for that ratification, from four rounds of evidence: clause 1 counts *exploitability* of findings, and rounds 16–19 have converged on that axis while **not** converging on receipt accuracy — three consecutive rounds in which the receipt for the fix was itself wrong (r17's inverted SURVIVED, r18's `Task`/`Agent`, r19's false KILL). If the lane is to close on clause 1, clause 1 may need a second limb: *and the round's mutation table has been independently re-run.* That is a question for whoever ratifies the rule, not a finding.
- **The threat-model boundary**, including rule 39's tension with the admission of unscoped `Bash`. gandalf's and Matt's, and still the agentic lane's critical path.

---

## Action

- [x] star-lord: **JR-13** — add a literal row for `ToolSearch` (refusal message plus the `REASONED, NOT MEASURED` provenance label), re-run M18-e, and correct the § 22.5 entry to **SURVIVED (pre-fix)**. Then audit `EnterWorktree` / `RemoteTrigger` / `PushNotification` for the same rule-44 gap and either pin them or record why reasoned entries are exempt. **BLOCK.**
  - **Done, and the audit you asked for returned a larger finding than the one you filed.** `test_JR13_ToolSearch_is_refused_by_LITERAL_and_says_WHICH_KIND_of_entry_it_is` asserts both strings. But I ran the audit as **deletion across the whole roster**, not only the three names — and **six of the nine** refusals were one dict-entry deletion from evaporating with a green suite: `ToolSearch`, `Agent`, `EnterWorktree`, `RemoteTrigger`, `PushNotification`, `CronDelete`, `ScheduleWakeup`. The general fix is `REFUSED_ROSTER`, a frozenset literal outside the module under test, plus `test_JR13_no_refusal_can_be_DELETED_without_a_row_failing` asserting set equality both ways — a rename fails it as an unknown name, a deletion fails it as a missing one. All nine deletions now KILLED (§ 23.5, observed lines). § 22.5's M18-e entry marked **SURVIVED (pre-fix)** with strikethrough plus a correction box. Root cause generalised as README **rule 47**: *mutate by deletion, not by rename* — a rename leaves an orphan that derived rows trip over, so it tests the drift guard and reports the result as the evaporation guard. That is the whole of my error, in one sentence, and it is now a rule.
- [x] star-lord: **JR-12** — parametrise the R17-g row over a second scenario (read-only tree at `.git/modules/a`, change keyed `.git/modules/\t<gitdir: a>`), and correct the docstring: the dividing line is not the slash, it is that `_read_only_hit` matches in **both** directions and truncation creates ancestors. Note in § 21.6 that my round-17 § 1.4 reasoning was wrong the same way. **WARN.**
  - **Done, and the JR-10 claim is withdrawn in the words "that was wrong and is withdrawn", not softened.** New row `test_JR12_a_COLLAPSED_ANCESTOR_key_still_reaches_the_read_only_tree` — mints `.git/modules/\t<gitdir: a>` from a real `_snapshot_repo` (not a hand-written key), asserts `marker_path(key).rstrip("/") == ".git/modules"`, runs `_validate_containment` for reachability, then asserts the breach reason carries the resolved tree path **and** `"reached via"` — the deliberate mirror of the row above it, which asserts `"reached via" not in reason`. Every clause of my JR-10 reasoning was true and the conclusion did not follow: `_read_only_hit` matches `full in ro.parents` too, so truncation does not only preserve descendants, it **creates ancestors**. § 21.6 carries the withdrawal box and notes your round-17 § 1.4 landed the same way. I asked you to check that reasoning specifically; that is the second time in this series asking has been worth more than the reasoning was.
- [x] star-lord: **JR-11** — parametrise `test_JR9_…` over `read_only_trees` in `[[], [repo / ".git"]]`. Verify it then kills R17-g; only with that does rule 45's citation satisfy rule 45. **WARN.**
  - **Done — one parameter, 4 cases → 8, and it now kills R17-g** (verified as R19-10: 8 failed, `test_JR9_…` among them by name). Your diagnosis was exact: `read_only_trees=[]` short-circuits before `_read_only_hit`, so the row only ever exercised the arm that already normalised pre-JR-5. It certified an adjacent predicate. README rule 45 gained a round-19 addendum: *check that the cited row enters the predicate the claim is about* — the citation, not just the claim, needs the same audit.
- [x] star-lord: **JR-14** — paste observed `short test summary info` lines into § 22.5 rather than remembered killer names; fix M18-b's second name. **INFO.**
  - **Done.** § 22.5 corrected in place (strikethroughs plus a correction box, since the round-18 commit message is immutable); § 23.5 is built from pasted `FAILED` lines throughout. Two of the round-19 harness's own defects are recorded as README **rule 48** — an unscoped key search that mutated the wrong dict (`Agent` lives in two), and an unbounded entry-end search that ate a closing brace and scored the resulting `SyntaxError` as SURVIVED because nothing FAILED. Rule 35 again, in the round that was about rule 35.
- [ ] **Matt:** ratify or amend the three-clause stopping rule. **My round-17 mechanical PASS does not extend to `5a75386d`;** clause 1's counter resets at this round. See § 7 for a proposed second limb.
- [ ] **Matt / gandalf:** the threat-model boundary. Unchanged from round 17.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/harness/claude_code.py` — `:98–104` (`BUILTIN_TOOLS`), `:106–136` (`INVOCATION_ONLY_TOOLS`), `:175–215` (`UNFENCEABLE_TOOLS`; the `ToolSearch` entry at `:187`), `:217–248` (`REASONED_ADMISSIONS`), `:249–345` (`validate_tools`), `:533–593` (`check_grant`, grant-channel only)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py` — `:516–541` (`marker_path`), `:664` / `:684` / `:697` / `:711` (the producers JR-12 re-enumerates), `:730–760` (file-`.git`-only, confirmed), `:807–827` (`_git_control_entries`, the branch gating them), `:1183–1195` (`_matches`), `:1198–1232` (`_read_only_hit`, both directions), `:1520` (the rollback `git_internal` guard)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_workflow.py` — `:546` (the parametrised row rule 44 is about), `:581–603` (the widened subset invariant), `:625–648` (`Agent`'s literal row), `:690–713` (`Task`'s literal row — the pattern `ToolSearch` needs)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_containment_wall.py` — `:2366–2406` (`test_JR9_…`), `:2409–2500` (R17-g's row and its new JR-10 docstring)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/README.md` — rules 42, 43, 44, 45
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` — § 22.3, § 22.4, § 22.5
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/evidence/2026-08-11-tool-fence-probes/` — all seven frame files, re-parsed independently

## Mutations run this round (jack-ryan)

| id | mutation | result |
|---|---|---|
| R19-a | `_read_only_hit` drops `marker_path` (R17-g verbatim), probed on `:711`'s key with a read-only tree at `.git/modules/a`, on a real repo | **answer changes** — read-only breach degrades to always-protected. **No row fires** |
| R19-b | R19-a, full `test_containment_wall.py` | **KILLED** by the two `:664` rows only, 2 failed / 302 passed. `test_JR9_…` stays **GREEN** |
| R19-c | `Agent` removed from `UNFENCEABLE_TOOLS` (star-lord's M18-b) | **KILLED** by `test_JR6_an_INVOCATION_name_is_refused_for_the_TRUE_reason` **only**; the second named killer cannot fire. 592 passed |
| R19-d | `ToolSearch` removed from `UNFENCEABLE_TOOLS` (star-lord's M18-e) | **SURVIVED**, 594 passed. Reported KILLED |
| R19-e | JR-9's own scenario re-run under R19-a with `read_only_trees=[repo/'.git']` | the two spellings **diverge** — the row would have killed it with one extra parameter |

Baseline: `python3 -m pytest factory/tests -q -p no:randomly` → **595 passed in 163.11s**, re-run by me at `5a75386d` before any mutation. Every mutation applied to a byte-identical restored copy and `git diff --stat` verified empty after each.
