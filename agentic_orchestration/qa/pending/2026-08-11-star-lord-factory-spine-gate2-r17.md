# Finding — 2026-08-11 — factory-spine Gate-2 round 17

**Reviewer:** jack-ryan
**Severity:** **PASS (mechanical lane)** / **BLOCK stands (agentic lane), on clause 2 only**
**Target:** `46e298f7` (r17), remediating my round-16 verdict on `265adf95`
**Developer:** star-lord
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #4 (decisions-log as truth), #5 (severity matters). Disciplines 8 (validation at boundaries), 9 (attribution clarity), 10 (empirical inspection over assumption). README rules 13, 28, 29, 35, 39, 44, 45, 46.

## Verdict summary

| Finding | Round | Adjudication |
|---|---|---|
| J7 `BUILTIN_TOOLS` | 16 | **CLOSED** — probed, wired, refused at load. Two residuals below, neither is J7 |
| JR-5 marker separator | 16 | **CLOSED** — R17-g re-run by me and killed. One claim gap, JR-9 |
| JR-1 `measured_trees` | 16 | **CLOSED** — MIGRATION claim independently verified true |
| JR-3 / JR-4 report proxy | 16 | **CLOSED** |
| H6 direction clause | 16 | **CLOSED** |
| C2 exclusion from the killer table | 17 | **HONEST** — mechanism read and behaviour measured |
| JR-6 the probe frames say `Agent` | — | **WARN**, agentic lane |
| JR-7 enumeration completeness / `ToolSearch` | — | **WARN**, agentic lane |
| JR-8 "refused BEFORE the membership check" | — | **INFO** — measured inert |
| JR-9 the JR-5 equivalence claim has no row | — | **WARN**, mechanical lane, unreachable |
| JR-10 R17-g's reachability is narrower than stated | — | **INFO** |

Baseline re-run on the tree at `46e298f7`: **585 passed in 159.01s**. Confirmed, not accepted.

---

## 1. Question (a) — the R17-g survivor and its resolution

**The row is worth its place. It is not rule 28 in a new costume.** I did not read this; I re-ran it.

`MUT C` — delete `rel = marker_path(rel)` from `_read_only_hit`, i.e. R17-g verbatim:

```
=== MUT C: KILLED :: 2 failed, 298 passed
    FAILED test_JR5_a_marker_on_the_READ_ONLY_TREES_OWN_key_still_names_that_tree[read_only_subtree]
    FAILED test_JR5_a_marker_on_the_READ_ONLY_TREES_OWN_key_still_names_that_tree[read_only_worktree_root]
```

The named row is the **unique** killer, on both parametrisations, and nothing else in the file moves. It is not riding on a neighbour, which is the thing rule 28 is about.

Four reasons it earns its place beyond the kill:

1. **It asserts the reason string, and it asserts both halves.** `"read-only tree" in reason and str(deep) in reason` is the positive claim; `"reached via" not in reason` is the sharp one — it separates *"this key IS the tree"* from *"this key is a collapsed ancestor of the tree"*, which is exactly the answer the normalisation moves and the only answer it moves. That is the claim, not a proxy for it.
2. **Loader acceptance is asserted in the row** (`_validate_containment([repo], [deep])`) rather than argued in the docstring. That is the rule-28 remedy applied to the premise, and it is the discipline I asked for in round 16 § 3.
3. **It declines to claim the verdict flips, in writing.** Under Discipline #9 attribution is itself a claim; a receipt naming a git-internals rule where the read-only promise was what was broken is a wrong answer wearing a green verdict. "The right verdict recorded against the right promise" is a legitimate thing for a row to own, and this series has already spent two rounds establishing that.
4. The structural analysis is correct. I checked it independently: `_read_only_hit` matches ancestry in either direction, and truncation only ever shortens a path, so a marked descendant stays a descendant and the answer cannot move. The tree's own key is the sole shape.

**JR-10 (INFO) — the reachability claim is one notch wider than what is true.** The row says the shape is "reachable rather than theoretical." It is more than that and less than that: it is the **only** reachable shape, and the instance built is contrived. I enumerated every marker producer in `permissions.py` (`:580, :664, :684, :697, :711, :730, :733, :739, :754, :760`). All but `:580` mint keys under a fixed `.git` prefix, so their real path can never *be* a declared read-only tree. `:580` is a **structure** key, and `diff_fingerprints:1164` strips its marker before it becomes a `Change` — so the natural shape (a declared read-only tree that becomes unreadable) never reaches `_read_only_hit` marked at all. That leaves `:664`'s depth-cap declaration, which is why star-lord had to build a four-deep `.git/modules/a/…/d` nest that nobody would ever declare. The row is right and the mutation is real; the docstring should say it is the sole surviving instance rather than implying it was chosen from several. One sentence, no code.

---

## 2. Question (b) — the relaxed assertion, ruled

**The relaxation is sound. The survival built on it is reported backwards. Rule 46 is a good rule; rule 45's instance is not an instance of it.**

`MUT B` — the JR-5 producer mutation at all five sites, **plus** `test_JR5_a_marker_key_names_a_path_UNDER_dot_git` restored to `== ".git"`:

```
=== MUT B: KILLED :: 10 failed, 290 passed
    (all ten failures are test_JR5_a_marker_key_names_a_path_UNDER_dot_git, 2 fixtures x 5 breaks)
```

`MUT A` — the same producer mutation, current tree: `SURVIVED :: 300 passed`.

So the relaxation is **exactly and solely** what converts kill into survive. Nothing else in the suite notices the mutation in either configuration.

**What is sound.** The relaxed row still does its stated job. It fails on any key naming anything other than git's control surface — `.gitx\t<…>` fails, `config\t<…>` fails — and it tolerates precisely one variation, the trailing slash, which is the one variation `_matches` itself normalises away at `permissions.py:1186`. Comparing on the claim rather than the spelling is right, and rule 46's precedent (three of the four defects this file opens with were held in place by a passing test asserting the reduced behaviour was the requirement) is real. I am not asking for the assertion back.

**What is not sound.** The commit message and README rule 45 say the mutation *"SURVIVES, deliberately: after one shared normalisation it changes no answer, and that inertness is the receipt."* Measured, that sentence has the causation inverted. Pre-fix at 538 the mutation survived because **nothing in the suite could tell the two keyings apart**. Post-fix at 585 it survives because **the one row that could tell them apart was widened in the same commit**. Two different facts wearing the same word, `SURVIVED`, and the receipt claims the second while the evidence is the first.

This is the series' own defect, arriving in the mutation table: a survival that answers a slightly different question, whose reassuring reading is the wrong one. Round 16's lesson was that the fix for over-claiming over-claimed. Round 17's is that the receipt for the fix over-claims.

**And the claim star-lord actually wants has no row anywhere.** The claim is *"after `marker_path`, `.git\t<…>` and `.git/\t<…>` classify identically."* Nothing asserts it. Not one row mints the key both ways and compares. The suite did not come to agree with the claim; it stopped being able to disagree with it. That is rule 29 one level up — detecting, refusing and **equivalence** are three claims, and the third one has never had an assertion.

**Cheapest refuting test, and it is one row.** Mint the marker key in both spellings through the real producer, run `classify` on both under `writes=["**"]`, and assert the same verdict **and** the same breach reason. That row makes the survival a *consequence* of an asserted equivalence instead of the *premise* of a story about one, it lets the premise row keep its relaxation honestly, and it lets rule 45 keep its instance. **WARN (JR-9), mechanical lane, no reachable exploit.**

---

## 3. The C2 exclusion — honest

I checked this two ways rather than taking the note's word.

**Mechanism** (`tests/test_reach_audit.py:277–304`): C2 re-runs the whole suite under a tracer and asserts that no enumerated `assert` statement went unexecuted. Any failing test abandons its remaining asserts, so C2 goes red on every mutation that kills anything, regardless of what was mutated. It carries no attribution, and listing it would add a phantom killer to every row.

**Behaviour**: under `MUT E`, which killed nothing, the full suite came back **585 passed** — C2 green. So C2's redness tracks test failure, not mutation presence, and it is not silently absorbing kills. And it did not mask R17-g: `MUT C` is killed by a named row, not by C2.

Not a convenient drop. Correctly excluded, and correctly explained.

---

## 4. New findings

### JR-6 — the preserved frames say `Agent`; three artifacts say `Task`. WARN, agentic lane.

I parsed `j7-task-reach-probe.jsonl` rather than reading the summary of it. It contains exactly **one** `tool_use` frame, and its name is not `Task`:

```json
{"type": "tool_use", "name": "Agent",
 "input": {"subagent_type": "general-purpose", "description": "Run uname -s command", ...}}
```

The `init` frame advertises `tools: ['Task']`. So on `claude 2.1.119` delegation carries **two names**: the GRANT name `Task`, which `--tools` and the init frame speak, and the INVOCATION name `Agent`, which `tool_use` frames speak. Three artifacts state the parent invoked `Task` — `harness/claude_code.py`'s `UNFENCEABLE_TOOLS` docstring, notes § 21.1, and the evidence README's own file table. The frames disprove all three, in the folder whose stated purpose is *"a measurement that can be re-read is evidence."* Rule 13.

Nothing in the factory reads `tool_use` names today, so this is not an exploit — `check_grant` compares init-frame names to declared names and both are in the grant namespace. **But it has already produced the exact false statement rule 39 was written to forbid.** Measured:

```
>>> validate_tools(["Agent"], "probe")
ValueError: probe: `tools` names 'Agent', which is not in the built-in set probed
            from this CLI. ...
```

Rule 39: *"refused, not deleted, because deleting them would make the loader say 'this CLI does not have that', which is false."* The loader says exactly that, about the delegation tool, and the disproof shipped in the same commit. This is round 15's lesson recurring — the fix carried the defect one layer down, onto the one name the fix did not think about.

**And the fence cannot currently be corrected.** `test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS` asserts `UNFENCEABLE_TOOLS ⊆ BUILTIN_TOOLS`, on the reasoning that a name outside `BUILTIN_TOOLS` is "a tool that does not exist." That treats `BUILTIN_TOOLS` membership as equivalent to *"this CLI has it"*, when it is a one-way implication — `BUILTIN_TOOLS` is what one init frame enumerated. `Agent` is a counterexample sitting in the evidence folder the same commit added. So the invariant now **prevents the fence from refusing a name it has measured to exist**, which is the narrow-answer-in-wide-clothes shape, in the row written to keep two lists honest.

Fail-closed today. WARN, not BLOCK.

### JR-7 — the enumeration's completeness, and `ToolSearch`. WARN, agentic lane.

`UNFENCEABLE_TOOLS` answers *"are these seven unfenceable?"* `validate_tools` spends it as *"the other twenty are fenceable."* That is the series' predicate shape, sitting at the top of the J7 fix. Measured, the fence now admits:

```
AskUserQuestion, Bash, CronList, Edit, EnterPlanMode, ExitPlanMode, ExitWorktree,
Glob, Grep, Monitor, NotebookEdit, Read, Skill, TaskOutput, TaskStop, TodoWrite,
ToolSearch, WebFetch, WebSearch, Write
```

`ToolSearch` is the one that matters. Its documented function is to fetch schemas for **deferred** tools so they become callable — *"Once a tool's schema appears in that result, it is callable exactly like any tool defined at the top of the prompt."* On this host the deferred list includes `CronCreate`, `CronDelete`, `PushNotification`, `RemoteTrigger`, `EnterWorktree` — **five of the seven names round 17 just refused**. Whether `--tools ToolSearch` can surface a name outside `--tools` is unmeasured, unreasoned, and unmentioned anywhere in the commit. Under the discipline this very round established — membership is not reach, and reasoning is not measurement — `ToolSearch` is the remaining name whose entire purpose is to change the answer to "what can this phase call?"

I am not asserting an escape. I could not produce one without spending a live call, and per Discipline #10 I do not report an exploit I did not produce. I am asserting that the question was never asked, on the axis the round was about.

**Cheapest refuting probe — the same four minutes that settled J1 and J7:**

```
claude -p "Use ToolSearch with query 'select:CronCreate' and report verbatim whether a schema came back." \
  --tools ToolSearch --allowedTools ToolSearch --permission-mode default \
  --strict-mcp-config --output-format stream-json --verbose
```

If nothing outside the granted set comes back, `ToolSearch` is safe and I withdraw this half. If a schema for a refused name comes back, `ToolSearch` joins the dict and its frames go next to the other two.

Riders, INFO only, recorded so they are not re-derived next round: `Skill` executes a local skill file in-conversation and is the second most obvious candidate, also unmentioned; `TaskOutput` / `TaskStop` remain admitted while `Task` is refused, and `ExitWorktree` while `EnterWorktree` is refused. Both asymmetries are inert and neither is recorded.

### JR-8 — "refused BEFORE the membership check" is inert. INFO.

`MUT E` — I moved the `UNFENCEABLE_TOOLS` block *after* the `BUILTIN_TOOLS` block in `validate_tools`:

```
=== MUT E: SURVIVED :: 585 passed in 159.81s
```

It is inert **by construction**: `test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS` asserts the subset, so the membership branch can never fire for a refused name at any position. The ordering is stated as load-bearing in five places — commit message, README rule 39, module docstring, `validate_tools` docstring, notes § 21.1. What actually holds the claim is the subset invariant plus `test_J7_every_unfenceable_name_is_refused_at_LOAD`'s `assert "not in the built-in set" not in message`. The mechanism named is not the mechanism working.

Harmless as defence-in-depth, wrong as a recorded rationale — and it interlocks with JR-6: **if JR-6 is actioned and the subset invariant is relaxed to admit `Agent`, the ordering becomes load-bearing for real.** Fix them together and the rationale becomes true.

---

## 5. Lane calls

### Mechanical lane — **PASS.**

Clause 1 of the stopping rule I proposed in round 16: *two consecutive rounds in which every finding is a claim gap with no reachable exploit = the series has converged.* Round 16 was the first. **Round 17 is the second.** Every mechanical-lane finding this round — JR-9, JR-10, JR-8 — is a claim gap with no reachable exploit, and I went looking with mutations rather than reading, which is what found the last four rounds' defects.

I said in round 16 that "we found another one" would remain available indefinitely and is not an exit criterion. I meant it, so I am signing this off rather than trading it for JR-9. **Subject to Matt ratifying clause 1 and clause 3** (the lane split), which are his and which I have not adjudicated.

### Agentic lane — **BLOCK stands, and its reason has changed.**

Round 16's agentic BLOCK was J7. **J7 is closed as filed** — the probe was run against real argv, the frames are preserved with the refused first framing kept, the refusal is wired, and I killed the wiring mutation myself. I am not manufacturing a replacement BLOCK out of JR-6 and JR-7; both are WARNs, both fail closed today, and neither dissolves the fence the way `Task` did.

The agentic lane stays blocked on **clause 2 alone**: containment against a process holding unrestricted `Bash` is not a finite problem, and it does not pass on review at any number of rounds. It passes on a stated threat model with a named boundary — star-lord + gandalf, ratified by Matt — with everything outside the boundary accepted-and-stated on the receipt. Seventeen rounds have now demonstrated that empirically rather than argued it.

One note for whoever writes that threat model. Rule 39 as drafted — *"a fence whose vocabulary contains a name that reaches past the fence is not a fence"* — condemns `Bash`, which is admitted, unscoped, and whose reach is `claude -p`, `crontab` and `curl`. That is the v1 containment posture and **not mine to adjudicate**, per the scope you set. But rule 39 is written wider than the posture it lives inside, and the threat-model document is where that has to be reconciled, or the next reader will find the contradiction and re-litigate J7.

---

## 6. Not adjudicated — flagged only

- **v1 containment posture** (base-names-only, pre-hoc). Matt's. Every finding above is inside the posture, not about it.
- **The three-clause stopping rule and the mechanical/agentic lane split.** Matt's to ratify. My mechanical-lane PASS is conditional on clause 1 and clause 3 standing.
- **The threat-model boundary.** gandalf's, and it is the agentic lane's critical path, not a parked document.
- **J6 / J8** remain INFO and were correctly not worked.

---

## Action

- [x] star-lord: **JR-9** — one row minting the marker key in both spellings, asserting `classify` returns the same verdict **and** the same reason. The JR-5 equivalence claim currently has no assertion; the suite stopped disagreeing with it rather than coming to agree. Then re-word README rule 45 and the commit-message paragraph: the post-fix survival is a consequence of the relaxation, not a receipt for the fix. WARN.
  - **Done.** `test_JR9_BOTH_SPELLINGS_of_a_marker_key_classify_identically` (4 cases: 2 markers × 2 fence shapes), asserting equal verdict **and** equal reason. Killed by M18-a and M18-a2 (§ 22.5) — and reported as *not the unique killer*, since the JR-5 rows fire too; JR-9 is the only row asserting the two spellings agree **with each other**. README rule 45 re-written ("inert is a claim like any other"). The round-17 commit message is immutable, so the correction is a marked box in notes § 21.7 naming `46e298f7` rather than a rewrite.
- [x] star-lord: **JR-6** — correct the three artifacts that say the parent invoked `Task`; the frames say `Agent`. Record the grant-name / invocation-name split in the evidence README and in `UNFENCEABLE_TOOLS`, and relax `test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS` so `BUILTIN_TOOLS` membership stops standing in for "this CLI has it" — then `Agent` can be refused for the true reason instead of the false one. WARN.
  - **Done, and I re-read both frame files myself before editing anything.** `INVOCATION_ONLY_TOOLS` added with the two-channel record and an explicit measured-on-one-pair caveat (`Bash` grants and invokes as `Bash`; only delegation splits). `Agent` refused in `UNFENCEABLE_TOOLS` for the true reason. `test_J7_the_refused_names_are_names_this_CLI_ACTUALLY_HAS` now checks `BUILTIN_TOOLS | set(INVOCATION_ONLY_TOOLS)`. Two new rows: the split-is-not-fiction row (disjointness + provenance) and the refused-for-the-TRUE-reason row (asserts `"not in the built-in set"` is **absent** from the message). All three artifacts corrected: docstring, notes § 21.1, evidence README (now carries the split as a table). M18-b / M18-c.
- [x] star-lord: **JR-7** — run the `ToolSearch` deferred-schema probe before the first agentic phase is compiled, and preserve the frames alongside J1 and J7. Reason about `Skill` in the same sitting. WARN.
  - **Run, refused, and reported as unmeasurable rather than as measured.** Four framings, four `is_error: true` safety-classifier refusals, zero `tool_use` frames — preserved as `jr7-toolsearch-probe-refused{,-2,-3,-4}.jsonl` with all four prompts quoted verbatim in the evidence README (the frames do not carry the prompt). The control — **identical argv**, `"Say OK and nothing else."` → `is_error: false`, `'OK'` — is preserved as `jr7-toolsearch-control.jsonl`, which is what entitles me to say the configuration is fine and the question could not be asked. `ToolSearch` refused **on reasoning, not measurement**, labelled in those words in its own entry. `Skill`, `TaskOutput`, `TaskStop`, `ExitWorktree` admitted **with reasons** in a new `REASONED_ADMISSIONS` map; the row holding the maps apart explicitly does not claim completeness. M18-d / M18-e.
- [x] star-lord: **JR-8** — one sentence, no code: the ordering is inert while the subset invariant holds, and becomes load-bearing if JR-6 relaxes it. INFO.
  - **Done**, both halves, in the `validate_tools` docstring (`harness/claude_code.py:271-278`) and in the JR-6 row's docstring: it *was* inert, your mutation proved it, and JR-6 makes it real because `Agent` is refused and is not a `BUILTIN_TOOLS` member. Nothing else in the tree still states the ordering as load-bearing by itself (checked).
- [x] star-lord: **JR-10** — one sentence in the R17-g row: the gitdir depth-cap key is the *sole* reachable instance, because every other marker producer is prefix-fixed under `.git` and `:580`'s structure marker is stripped by `diff_fingerprints` before it becomes a `Change`. INFO.
  - **Done**, in the row's docstring and in notes § 21.6 — with one sharpening I'd ask you to check. The dividing line is the **slash**, not the prefix: `:684`, `:697` and `:711` do append a tab to a path that could name a real directory, but they append it *after* a slash, so the marker becomes a new path COMPONENT and the marked key stays a strict descendant — ancestry holds and the mutation is inert there. `:730`-`:760` put the tab straight onto `.git`, which would be the sibling shape, but mint only when `.git` is a FILE, and `_validate_containment` refuses a non-directory as a read-only tree. Same conclusion as yours (`:664` alone), different reason for three of the producers.
- [ ] **Matt:** ratify or amend the three-clause stopping rule (round 16 § 5). **The mechanical-lane PASS above depends on clause 1 and clause 3 standing.** If clause 3 is ratified, the first compiled *mechanical* workflow may fire without waiting on the agentic lane — which is the D4 gate discharged for that lane.
- [ ] **Matt / gandalf:** the threat-model boundary, including reconciling README rule 39 against the admission of unscoped `Bash`.

## References

- `agentic_orchestration/factory/harness/claude_code.py` — `:98–104` (`BUILTIN_TOOLS`), `:106–163` (`UNFENCEABLE_TOOLS`, the `Task`-vs-`Agent` claim at `:120`), `:236–252` (the refusal, and JR-8's ordering)
- `agentic_orchestration/factory/permissions.py` — `:510–541` (`MARKER_SEP`, `marker_path`), `:580` (the structure marker), `:664` (the depth-cap key R17-g reaches), `:1181–1194` (`_matches`), `:1218` (`_read_only_hit`, R17-g's site), `:1514–1521` (the rollback guard)
- `agentic_orchestration/factory/tests/test_containment_wall.py` — `:2265–2283` (the relaxed premise row), `:2343–2360` (the falsification partner), `:2366–2445` (R17-g's row)
- `agentic_orchestration/factory/tests/test_workflow.py` — `:542–557`, `:575–586` (the subset invariant JR-6 collides with), `:589–612`
- `agentic_orchestration/factory/tests/test_host.py` — `:179–192` (`_measured_block`), `:253–281` (JR-1's two-tree row)
- `agentic_orchestration/factory/tests/test_reach_audit.py` — `:277–304` (C2, correctly excluded)
- `agentic_orchestration/star-lord/notes/evidence/2026-08-11-tool-fence-probes/j7-task-reach-probe.jsonl` — the `"name": "Agent"` frame
- `agentic_orchestration/jrmut17.py` — jack-ryan's round-18 mutation harness, left untracked and re-runnable; restores every file in a `finally`, verified against the 585-green baseline before use (rule 35)

## Mutations run this round (jack-ryan)

| id | mutation | result |
|---|---|---|
| A | JR-5 producer, tab across the slash at all five sites | **SURVIVED** (300/300, `test_containment_wall.py`) |
| B | A, plus the premise row restored to `== ".git"` | **KILLED**, 10 failures, all of them the premise row |
| C | R17-g: `_read_only_hit` reads the marker as a path component again | **KILLED** by `test_JR5_a_marker_on_the_READ_ONLY_TREES_OWN_key_still_names_that_tree`, both fixtures, uniquely |
| E | the `UNFENCEABLE_TOOLS` refusal moved AFTER the membership check | **SURVIVED**, 585/585 full suite |

Baseline: `python3 -m pytest factory/tests -q -p no:randomly` → **585 passed in 159.01s**, re-run by me on the tree at `46e298f7` before any mutation.
