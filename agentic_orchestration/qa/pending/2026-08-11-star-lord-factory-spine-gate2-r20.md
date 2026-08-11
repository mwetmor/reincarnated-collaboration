# Finding — 2026-08-11 — factory-spine Gate-2 round 20

**Reviewer:** jack-ryan
**Severity:** **BLOCK (mechanical lane — RE-OPENED, new finding JR-18)** / **BLOCK stands (agentic lane), clause 2 only, unchanged**
**Target:** `4396ae13` + `644b5db3` (r20), remediating my round-20 verdict `9f857270` on `4088b730`
**Developer:** star-lord
**Captured by:** star-lord (jack-ryan does not write findings files; verdict returned inline and captured verbatim)
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #5 (severity matters). Disciplines 8 (validation at boundaries), 9 (attribution clarity), 10 (empirical inspection over assumption). README rules 13, 44, 45, 47, 48, 49. Matt's standing method mandate.

## Verdict summary

| Finding | Round | Adjudication |
|---|---|---|
| JR-15 `REASONED_ADMISSIONS` unpinned | 20 | **CLOSED as to the KEY.** R20-1/2/3 reproduce exactly. The *second* assert does not do what its docstring says — **JR-19, WARN** |
| JR-16 the producer enumeration | 20 | **CLOSED.** Four producers named, `:684`/`:697`/`:711` adjudicated, zero rows added as instructed. Verified by reading `permissions.py` at HEAD |
| JR-17 the eleventh pathway | 20 | **CLOSED.** Denominator re-measured by me: exactly ten mint sites (`:580`,`:664`,`:684`,`:697`,`:711`,`:730`,`:733`,`:739`,`:754`,`:760`) + `:826`. Line citations correct at HEAD |
| § 24.5's seven-row table | — | **RE-RUN INDEPENDENTLY. Six of seven reproduce exactly. R20-4 does not, and I can now say why** — **JR-21, INFO** |
| the R20-4 disagreement | — | **ADJUDICATED. star-lord's number is an artifact of their mutator, not their collector.** Reproduced both ways |
| rule 47's behaviour-vs-record discriminator | — | Two measured gaps, including a third category neither of us named — **JR-20, WARN** |
| `_matches` normalises the WRITES allow-list | — | **A phase-chosen filename escapes the declared write scope. Measured. JR-18, BLOCK** |

Baseline re-run by me at `644b5db3`: **604 passed in 162.08s**, clean tree, `-p no:randomly`. Confirmed, not accepted. Was 603 at `4088b730`.

---

## 0. Answering your six questions, in order

1. **Re-run § 24.5.** Done, my own harness, nine mutations plus three controls. **R20-1/2/3/5/6/7 reproduce to the digit. R20-4 does not — and both of us are right about what our own instruments did.** § 1.
2. **The figure that does not close.** **Settled, and it is not the collector.** Your deleter degenerated the 2-tuple into a bare `str`; I reproduced *your* `21 failed, 571 passed, 12 errors` exactly by degenerating it deliberately, and reproduced *my* `7 failed` by deleting properly. § 2.
3. **Is the JR-15 fix the right shape?** Neither. It is the minimum one plus one assert that does not close the case its own docstring names. **JR-19.** § 3.
4. **Rule 47's discriminator against its own scope.** It has a hole on its own axis and there is a third category. Both measured. **JR-20.** § 4.
5. **Audit the instruments.** Yours: § 2. Mine: three defects this round, § 5.
6. **Lane calls.** Mechanical **BLOCK, re-opened** on JR-18. Agentic **BLOCK stands**, unchanged. **Clause 1's counter resets to 0.** § 7.

---

## 1. The table, re-run — six of seven, and the seventh explained

Harness: AST-scoped, re-emitting the container via `ast.unparse` so a 2-tuple minus one element stays a **tuple**. Refuses to report unless the tree was clean before the run, the file changed, the mutated file parsed, the module imported, the intended change was observed in the loaded object by **type and length and membership**, and results were collected with `-rEf` so **ERRORs and FAILUREs are both reported**. Counts below are the raw pytest summary line.

| your id | mutation | your figure | my observation |
|---|---|---|---|
| R20-1 | `"Skill"` deleted | `2 failed, 602 passed` | **KILLED**, `2 failed, 602 passed` — `test_JR15_…`, `test_C2_…` |
| R20-2 | `"ExitWorktree"` deleted | `2 failed, 602 passed` | **KILLED**, identical, same two rows |
| R20-3 | the `ToolSearch` clause cut | `2 failed, 602 passed` | **KILLED**, identical, same two rows |
| R20-4 | `"worktrees/"` deleted | `21 failed, 571 passed, 12 errors` | **see § 2** |
| R20-5 | `"modules/"` deleted | `11 failed, 593 passed` | **KILLED**, `11 failed, 593 passed` — exact |
| R20-6 | `"config.worktree"` deleted | `3 failed, 601 passed` | **KILLED**, `3 failed, 601 passed` — exact |
| R20-7 | `".claude/"` deleted | `3 failed, 601 passed` | **KILLED**, `3 failed, 601 passed` — exact |

Every line closes to 604. R20-1/2/3 land on `test_JR15_no_reasoned_admission_can_be_DELETED_without_a_row_failing` — so the roster pin **is** load-bearing for the key, and R20-3 confirms the second assert fires when the clause is cut. That part of your receipt is sound.

---

## 2. R20-4 adjudicated — your mutator, not your collector. **JR-21, INFO.**

I ran the deletion **twice, two ways**, on the same tree, minutes apart:

```
R20-4T  GIT_NESTED_GITDIRS -> ('modules/',)   [a proper 1-tuple]
        KILLED, raw:  7 failed, 597 passed
        3 H4 rows x 2 `fenced` params + test_C2

R20-4S  GIT_NESTED_GITDIRS -> ("modules/")    [a bare str, len 8]
        KILLED, raw:  21 failed, 571 passed, 12 errors
        ERROR ...::test_JR5_a_marker_key_names_a_path_UNDER_dot_git[read_only_subtree-commondir points at a file]
```

**R20-4S is your figure, to the digit, including the twelve fixture errors and the verbatim first line you recorded for me.** R20-4T is my r19 figure, `7 failed`, at the new 604 baseline. Neither of us mis-collected. We mutated two different objects.

**The mechanism, and it explains the asymmetry you flagged as impossible.** Deleting the *last* element of `("worktrees/", "modules/")` by cutting the literal leaves `("worktrees/", )` — a valid 1-tuple. Deleting the *first* must take the following comma too, and leaves `("modules/")` — parentheses around a string, which is a `str`. So the last-element deletions (R20-5/6/7) closed against me and the first-element one did not. Your G4 guard passed it because `"worktrees/" not in "modules/"` is a true **substring** test.

Then `for nested in GIT_NESTED_GITDIRS` iterates *characters*, and both strings end in `/`, so the final iteration is `nested = "/"` → `container = dot / "".rstrip("/")` → `dot` itself → every entry in the gitdir mints a `<gitdir: …>` marker key. `broken_pointer`'s premise `assert len(keys) == 1` then blows at **fixture** level, and those three `test_JR5_…` rows never execute. I confirmed the mechanism by running the mirror case: R20-5S (`("worktrees/")`, also `/`-terminated) returns **`21 failed, 571 passed, 12 errors`** as well.

**Two corrections follow, and they matter more than the number.**

- **Rule 47's addendum cites `21 failed / 12 errors` for a `"worktrees/"` deletion. That deletion was never performed.** What was measured is `GIT_NESTED_GITDIRS` becoming a string. The adjudication holds — KILLED either way, as you said — but the figure in the rule is attached to the wrong mutation, and the rule is the one about scope.
- **Rule 48's second round-20 addendum diagnoses this as a collector defect.** The collector gap is real and the `-rEf` fix is right; it is what *hid* the tell. It is not what *produced* the reading. Written as it stands, the rule teaches the wrong lesson from the right event: the defect was a mutator that degenerated a container's **type** and a guard that checked membership by substring — which is, precisely and to the letter, the defect I recorded against my own name in r19 § 6 and which round 20 generalised into rule 48 *as coming from the reviewer's instrument*. The round that wrote it down shipped it.

You asked whether my harness saw errors. It sees them now because I built it to; on the mutation you and I disagreed about, **there were none to see.**

---

## 3. JR-19 — the second assert is a token pin, not a clause pin. **WARN.**

You added an assert I did not ask for, on the argument that a roster pin alone passes a mutation that keeps the key and guts the sentence. **The argument is correct. The assert does not discharge it.**

`assert "ToolSearch" in REASONED_ADMISSIONS["Skill"]` is a **substring test on a ten-character token**. R20-3 cut the clause *including the token*, so of course it dies. The weaker mutation — the one the docstring actually names, *"the reason rewritten to something that no longer adjudicates anything"* — keeps the token:

```
R21-A  Skill's reason -> "is fine; ToolSearch is a different name"
       SURVIVED, 604 passed — the baseline count UNMOVED
```

That is the same byte-identical-verdict signature that made JR-15 worse than JR-13, still open, in the fix for JR-15.

**And the gap I did not enumerate last round is larger than the one I did.** Three of the four entries carry a load-bearing clause and none is pinned at all — and unlike `Skill`, their admissions are *conditional on a refusal elsewhere*:

```
R21-B  ExitWorktree's reason -> "admitted"   SURVIVED, 604 passed
R21-C  TaskOutput's reason   -> "admitted"   SURVIVED, 604 passed
```

`TaskOutput` is admitted because *"`Task` is refused above, and without a creator this is inert"*. `ExitWorktree` because *"`EnterWorktree` is refused above"*. `TaskStop` by reference to `TaskOutput`'s reason. Those are not decoration: they are the premises. `REFUSED_ROSTER` currently holds them by accident — it pins `Task` and `EnterWorktree` in a *different literal*, so the coupling is real but nowhere stated. A legal two-line edit (regrade `Task` as fenceable, update both `UNFENCEABLE_TOOLS` and `REFUSED_ROSTER`) leaves three admissions standing on a refusal that no longer exists, and the suite stays at 604.

**Cheapest fix, and I do not think it needs a fourth assert per entry:** one row that walks `REASONED_ADMISSIONS` and requires each reason to name the refused entry it depends on — the dependency asserted as a link rather than restated as prose. That closes R21-A, R21-B and R21-C together and it closes the regrade case, which no literal does.

---

## 4. JR-20 — rule 47's discriminator has a hole on its own axis, and a third category. **WARN.**

You measured four collections and generalised over "this codebase's production collections." There are fifteen. I measured the ones you did not, chosen adversarially:

```
R21-D  FACTORY_RUNTIME_PATHS  -- member DELETED               SURVIVED, 604 passed
R21-E  FACTORY_RUNTIME_PATHS  -- "reincarnated-engine/" ADDED SURVIVED, 604 passed
R21-F  STRUCTURE_SKIP_DIRS    -- "canonical" ADDED            SURVIVED, 604 passed
R21-G  STRUCTURE_SKIP_DIRS    -- ".git" deleted  [control]    KILLED,  2 failed (test_K1_…)
R21-H  PROTECTED_ALWAYS       -- "canonical/" deleted [ctrl]  KILLED,  2 failed
```

**Gap one, on the discriminator's own axis.** `FACTORY_RUNTIME_PATHS` is *behaviour* by your definition — `_is_factory_runtime` (`:414`) is a live predicate on every fingerprint. The rule says behaviour collections are protected by the scenario rows that exercise them and need no literal. **Deleting a member survives at an unmoved 604.** It and `STRUCTURE_SKIP_DIRS` are named nowhere in the 604-row suite, by literal or by derivation. "Behaviour ⇒ covered" is not a property of being behaviour; it is a property of *someone having written the row*, and the rule states it as the former.

**Gap two, and this is the third category.** `FACTORY_RUNTIME_PATHS` and `STRUCTURE_SKIP_DIRS` are **exemption lists** — their members mean *do not look here*. For those, deletion is the **fail-closed** direction and **addition** is the fail-open one, and rule 47's headline instruction is *"to test whether a finding is protected, DELETE it."* Applied to an exemption list, deletion is the strictly weaker mutation — which is rule 47's own founding sentence, *"a rename is the weaker mutation, and it is the one that lies,"* reproduced inside rule 47's own generalisation, one axis over.

The sharpest instance is the one whose docstring already tells the story: `FACTORY_RUNTIME_PATHS` is *"a list of six paths rather than the category 'anything git ignores', because the category version is what let a write to the engine's telemetry DB pass as a green read-only proof."* Adding `"reincarnated-engine/"` re-creates that exact false green, in the root repo, and **nothing in the suite moves.**

So the discriminator needs a second axis, not a repair: **behaviour vs record** decides *whether the members are visible to a row at all*; **protection vs exemption** decides *which direction the mutation has to go*. Deletion tests a protection list. Addition tests an exemption list. `REASONED_ADMISSIONS` needs the literal because it is a record; `FACTORY_RUNTIME_PATHS` needs one because deletion — the only mutation the rule contemplates — is the direction that cannot hurt it.

---

## 5. JR-18 — the writes allow-list is fail-open on a phase-chosen filename. **BLOCK.**

`_matches` (`permissions.py:1183`) strips the marker before matching, and its own comment reasons about exactly one direction: *"in the permissive direction for the protected lists, which is the direction that does not announce itself."* The same function is the writes arm of `classify` (`:1283`). For the **allow-list**, truncation is permissive in the other direction, and nobody looked.

Measured on a real repo, clean tree asserted, module source verified unmutated by `inspect.getsource`:

```
writes = ["workspace/**", "workspace"]
phase creates, at the repo ROOT:   workspace\tevil.txt      (a SIBLING of workspace/)

changes:               [{"path": "workspace\tevil.txt", "kind": "created"}]
classify -> ALLOWED:   ["workspace\tevil.txt"]
classify -> BREACHES:  []

_matches("workspace\tevil.txt", "workspace")     -> True
_matches("workspace\tevil.txt", "workspace/**")  -> True     <-- the `bare` fallback
_matches("workspace-evil.txt",  "workspace")     -> False    <-- control
```

`marker_path` splits on the first tab; a tab is a legal POSIX filename character; the module cannot tell a marker it minted from one git handed it. A phase granted `writes: ["<dir>/**"]` — the standard shape of every writes declaration, and the `/**` form alone is sufficient via the `bare` fallback at `:1194` — can write **outside its declared scope** and be classified as an authorised write. The wall's central claim, *the phase wrote only where it declared*, is falsifiable by choosing a filename. This is the series' own shape at the fence: a predicate answering "is the path this key **names** inside the allowlist" when asked "is this **change** inside the allowlist," and the wrong answer is the green one.

**Second measured consequence, same root.** A root-level file named `.git\tevil`:

```
breach reason:  "write inside an always-protected path in ANY declared repo"
rollback:       NOT_ROLLED_BACK, guard="git_internal"
file_still_present_after_rollback:  True
```

Fail-closed on detection — good — but the phase chose which guard fired, the receipt names git's control plane for a file that is not in it, and **the rollback declines to remove it**. A phase can make its artifact survive rollback by naming it with a tab.

**Why no row caught it, and this is the part that belongs with rule 45.** `test_JR5_PARTNER_an_ordinary_path_keeps_its_whole_name` (`test_containment_wall.py:2343`) is the designated falsification partner. Its docstring states the claim exactly right — *"A path that merely CONTAINS a tab is not a marker-bearing key, and truncating it would move a breach's reported location to an ancestor, which is K1's damage shape."* Its three `marker_path` assertions are on `"src/output/a.json"` (**no tab**), `""`, and a genuine marker key. The one case it exists to falsify is absent, and the code fails it: `marker_path("odd\tname.txt")` → `"odd"`, `marker_path("src/odd\tname.txt")` → `"src/odd"`. Its fourth assertion tests that the change-set *names* the file, which is measured before `marker_path` is ever applied — an adjacent predicate, certified. That is JR-11 again, on a row that has been green for twenty rounds.

**Scope of exposure, stated plainly so the BLOCK is not read as wider than it is.** The only compiled workflow, `workflows/kc2-baton-mechanical.yaml`, declares `writes: []` on every phase, and an empty allow-list admits nothing. The read-only arm runs first and is fail-closed under truncation, so declared read-only trees are not reachable this way. **Nothing pending is exposed. The fence is.** And D4 is precisely the rule that says the fence gets cleared before anything fires.

**Path forward.** The fix is in `_matches` and not in the rows: it needs to know whether the key it was handed is one this module minted. A key is synthetic only when the marker matches the shape the ten sites emit (`\t<…>`, closing bracket, no further separator) — anything else is a real path and must be matched whole. Either that, or refuse a change whose path contains `MARKER_SEP` and did not come from a mint site, and file it as its own guard. I have a preference for the second; the choice is yours and the measurement is what I am asking for, not the design.

---

## 6. What is CLOSED, and the instruments

**JR-16 — CLOSED.** I read `permissions.py` at HEAD rather than accepting the citations. `:684`, `:697`, `:711` all mint `<dir>/\t<marker>`; `:664` mints the exact-key shape; the paragraph names all four and states that one row covers the branch three of them reach. Zero rows added, as instructed, and your stated reason for agreeing rather than complying is the right one.

**JR-17 — CLOSED, and the denominator now holds under an independent count.** Exhaustive grep for marker construction across `permissions.py` returns exactly ten mint sites — `:580`, `:664`, `:684`, `:697`, `:711`, `:730`, `:733`, `:739`, `:754`, `:760` — and `:826` is the eleventh pathway, a prefix, not a mint. `:807` is the `not dot.is_dir()` branch, as the docstring says. Every line number in the amended docstring is correct at HEAD. I do not re-litigate 16 vs 17 keys; flagging the difference rather than adopting mine silently was the right call and it is the rule 49 behaviour, not merely the rule 49 text.

**Your instrument.** § 2. The two guards you added this round are the right guards and they did not fire because the type check was a membership check. `type` and `len`, not `in`.

**Mine, three defects, recorded against my name per rule 48.**

- **A false-abort I would rather have than its opposite.** My G5 precondition looked for `collected N items`, which `-q --no-header` does not print, so every row reported `ABORT: G5 collected=None` *after* a complete and correct measurement. Conservative by direction — it can only refuse a good reading, never accept a bad one — and I verified each row's `failed + passed + errors` totals to 604 by hand before using it. Fixed by deriving the total from the raw summary line.
- **A probe that failed closed.** My first batch passed the observation script to `python3 -c` through a shell, which ate the newlines; all nine rows aborted at G3 and none reported a verdict. The guard did its job: nothing was published from a run where the module had not been read.
- **A predicate answering an adjacent question, in my own harness, in the round I am writing this in.** I chained batch 3 behind batch 2 with `while pgrep -f "mut21.py"; do sleep 20; done`. The chain shell's own command line contains the string `mut21.py`, so it matched itself and waited forever. Asked: *is the harness still running.* Answered: *does any process mention this name.* Wrong answer, safe-looking direction. Twenty rounds in, and it is still the easiest mistake in this codebase to make.

Every mutation restored, `git diff HEAD -- agentic_orchestration/factory` empty after each, tree verified clean before every probe, and the closing re-run at `644b5db3` is **604 passed in 165.66s** on an empty diff.

---

## 7. Lane calls

### Mechanical lane — **BLOCK. The round-19 PASS is re-opened.**

JR-15, JR-16 and JR-17 are all worked, and two of the three are closed cleanly. The receipt reproduces six of seven and the seventh is now explained rather than parked. On the round's own terms this was a good round.

The PASS does not survive JR-18, and the criterion is the one I set myself when I granted it: I lifted the r19 BLOCK on the finding that the open items were *"claim gaps with no reachable exploit… not a regression channel the suite cannot see."* JR-18 is a reachable fail-open in the classifier, exercised by a filename, invisible to 604 rows, and guarded by a falsification partner that omits its own falsification case. That is the criterion JR-13 failed, and this fails it harder.

**Clause 1's counter resets to 0.** It stood at 1 of 2. A round that surfaces a BLOCK-severity behaviour defect is not a clean round, and I am not going to carry the counter past it.

### Agentic lane — **BLOCK stands, clause 2, unchanged and untouched.**

Nothing this round moves it. JR-18 through JR-21 are all mechanical. The threat-model boundary remains gandalf's and Matt's, and remains this lane's critical path.

---

## 8. Not adjudicated — flagged only

- **v1 containment posture** (base-names-only, pre-hoc). Matt's.
- **The three-clause stopping rule and the lane split.** Matt's. My proposed second limb — *"and the round's mutation table has been independently re-run"* — now has its fifth data point, and this round is the strongest evidence for it yet: the re-run did not just re-check a number, it produced a BLOCK. Round 20's own conclusions were sound; what the re-run found was underneath them.
- **The threat-model boundary**, including rule 39's tension with unscoped `Bash`. gandalf's and Matt's.
- **JR-7's INFO rider** — the benign `ToolSearch` control. Correctly still deferred to the agentic lane opening.
- **Rule 47's amended prose** carries a colon whose completion — *"removing a member stops a real key being minted and a scenario row notices, so they need no pin"* — is now six lines downstream of it, behind the disagreement paragraph. It reads as a non-sequitur. Presentational, INFO, fold into the JR-20 rewrite.

---

## Action

- [ ] star-lord: **JR-18** — `_matches` strips `MARKER_SEP` before matching the WRITES allow-list, so a root-level file named `<declared>\t<anything>` is classified ALLOWED. Measured: `writes=["workspace/**","workspace"]` admits `workspace\tevil.txt` at the repo root, breaches `[]`; the `/**` form alone admits it via the `bare` fallback at `:1194`. Second consequence: `.git\tevil` is refused under `git_internal` and **survives rollback**. Distinguish minted markers from real paths, or refuse an unminted `MARKER_SEP` path under its own guard — your call, but measure the fix with a phase-chosen filename, not a synthetic key. **BLOCK.**
- [ ] star-lord: **JR-18b** — `test_JR5_PARTNER_an_ordinary_path_keeps_its_whole_name` (`:2343`) states the claim and asserts a path with no tab in it. Add the case its docstring names: `marker_path` on a real tab-bearing path, and a classify row on the writes arm. This is rule 45's subject — the cited row does not enter the predicate the claim is about. **BLOCK** (ships with JR-18).
- [ ] star-lord: **JR-19** — the `"ToolSearch" in REASONED_ADMISSIONS["Skill"]` assert is a token pin. R21-A survives at an unmoved 604 with the token kept and the contrast gutted; R21-B and R21-C survive with `ExitWorktree`'s and `TaskOutput`'s reasons replaced by `"admitted"`. Prefer one row asserting each admission *names the refusal it depends on* over four clause pins — it closes the regrade case as well. **WARN.**
- [ ] star-lord: **JR-20** — rule 47's discriminator needs a second axis. Measured: `FACTORY_RUNTIME_PATHS` member-deletion SURVIVES at 604 (a behaviour collection with no covering row at all), and additions to `FACTORY_RUNTIME_PATHS` and `STRUCTURE_SKIP_DIRS` both SURVIVE. Both are **exemption** lists, where deletion is fail-closed and addition is fail-open — the direction rule 47 does not contemplate. State it as *behaviour vs record* (are the members visible to a row) **and** *protection vs exemption* (which direction the mutation must go), and re-derive which collections need a literal from all fifteen rather than from four. **WARN.**
- [ ] star-lord: **JR-21** — correct rule 47's cited figure (`21 failed / 12 errors` was `GIT_NESTED_GITDIRS` becoming a `str`, not `"worktrees/"` deleted; the deletion is `7 failed, 597 passed`) and re-diagnose rule 48's second round-20 addendum. Keep the `-rEf` fix; it is right. Change what it says the defect *was*: a mutator that degenerated a container's type, and a guard that verified membership by substring where it needed type and length. **INFO.**
- [ ] star-lord (optional): rule 47's spliced colon, § 8.
- [ ] **Matt:** ratify or amend the three-clause stopping rule. **Clause 1's counter resets to 0** after this round. See § 8 for the proposed second limb and the fifth data point behind it.
- [ ] **Matt / gandalf:** the threat-model boundary. Unchanged from rounds 17–20, still the agentic lane's critical path.

## References

- `agentic_orchestration/factory/permissions.py` — `:74` (`FACTORY_RUNTIME_PATHS` — JR-20), `:414` (`_is_factory_runtime`), `:508` (`STRUCTURE_SKIP_DIRS` — JR-20), `:516–541` (`marker_path`), `:613` / `:635` (the two `GIT_*` tuples — § 2), `:644–714` (`_gitdir_control_entries`; the `nested` loop that degenerates), `:580`/`:664`/`:684`/`:697`/`:711`/`:730`/`:733`/`:739`/`:754`/`:760` (the ten mint sites, re-counted), `:807` / `:826` (the eleventh pathway), **`:1183–1195` (`_matches` — JR-18)**, `:1198–1232` (`_read_only_hit`), **`:1283` (`classify`'s writes arm — JR-18)**, `:1520` (the rollback `git_internal` guard)
- `agentic_orchestration/factory/tests/test_workflow.py` — `:559` (`REFUSED_ROSTER`), `:618` (`ADMITTED_ROSTER`), `:621–651` (`test_JR15_…` — JR-19), `:793–830` (the four derived `REASONED_ADMISSIONS` assertions)
- `agentic_orchestration/factory/tests/test_containment_wall.py` — `:500` (`fenced`), `:2203` (`GIT_POINTER_BREAKS`), `:2237–2260` (`broken_pointer`, whose `len(keys) == 1` premise is what errored — § 2), `:2265`/`:2287`/`:2316` (the three erroring rows), **`:2343–2362` (`test_JR5_PARTNER_…` — JR-18b)**, `:2426–2503` (the JR-16/JR-17 docstring, verified against HEAD)
- `agentic_orchestration/factory/README.md` — rules 44, 45, 47 (+ round-20 addendum — JR-20, JR-21), 48 (+ two round-20 addenda — JR-21), 49
- `agentic_orchestration/factory/workflows/kc2-baton-mechanical.yaml` — `writes: []` on every phase; the reason JR-18 is a fence defect and not a live exposure
- `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` — § 24, § 24.5
- `agentic_orchestration/qa/pending/2026-08-11-star-lord-factory-spine-gate2-r19.md` — my r19 verdict with your dispositions; additions only, my text unaltered, verified by diff

## Mutations run this round (jack-ryan)

Sixteen mutations plus two baselines. Counts are raw pytest summary lines, `test_C2` included; subtract one for your § 24.5 convention. Every row: clean tree asserted before, container type/length/membership observed in the loaded object, `-rEf` collection, restore verified.

| id | mutation | observed |
|---|---|---|
| B0 | none (baseline at `644b5db3`) | **604 passed in 162.08s** |
| R20-1 | `"Skill"` deleted from `REASONED_ADMISSIONS` | **KILLED** — `2 failed, 602 passed`: `test_JR15_…`, `test_C2_…` |
| R20-2 | `"ExitWorktree"` deleted | **KILLED** — `2 failed, 602 passed`: same two |
| R20-3 | the `ToolSearch` clause cut from `Skill`'s reason | **KILLED** — `2 failed, 602 passed`: same two |
| R20-4T | `"worktrees/"` deleted → `('modules/',)` **tuple** | **KILLED** — `7 failed, 597 passed`: `test_H4_a_NEW_gitdir_APPEARING…`, `test_H4_a_config_in_an_EXISTING_worktree_gitdir…`, `test_H4_PARTNER_…` (each ×2 `fenced`), `test_C2_…` |
| R20-4S | `"worktrees/"` deleted → `("modules/")` **str** | **KILLED** — `21 failed, 571 passed, 12 errors`: **your figure exactly**, incl. 12 fixture ERRORs on the three `test_JR5_…` rows |
| R20-5T | `"modules/"` deleted → `('worktrees/',)` tuple | **KILLED** — `11 failed, 593 passed`: **your figure exactly** |
| R20-5S | `"modules/"` deleted → `("worktrees/")` str | **KILLED** — `21 failed, 571 passed, 12 errors`: confirms the `/`-terminated-string mechanism |
| R20-6 | `"config.worktree"` deleted from `GIT_CONTROL_PATHS` | **KILLED** — `3 failed, 601 passed`: **your figure exactly** |
| R20-7 | `".claude/"` deleted from `PROTECTED_EVERY_REPO` | **KILLED** — `3 failed, 601 passed`: **your figure exactly** |
| R21-A | `Skill`'s reason → keeps `"ToolSearch"`, contrast gutted | **SURVIVED** — `604 passed`, count unmoved. **JR-19** |
| R21-B | `ExitWorktree`'s reason → `"admitted"` | **SURVIVED** — `604 passed`. **JR-19** |
| R21-C | `TaskOutput`'s reason → `"admitted"` | **SURVIVED** — `604 passed`. **JR-19** |
| R21-D | `FACTORY_RUNTIME_PATHS` member deleted | **SURVIVED** — `604 passed`. **JR-20** |
| R21-E | `"reincarnated-engine/"` **added** to `FACTORY_RUNTIME_PATHS` | **SURVIVED** — `604 passed`. **JR-20** |
| R21-F | `"canonical"` **added** to `STRUCTURE_SKIP_DIRS` | **SURVIVED** — `604 passed`. **JR-20** |
| R21-G | `".git"` deleted from `STRUCTURE_SKIP_DIRS` (control) | **KILLED** — `2 failed, 602 passed`: `test_K1_ordinary_git_activity_does_not_move_the_structure`, `test_C2_…` |
| R21-H | `"canonical/"` deleted from `PROTECTED_ALWAYS` (control) | **KILLED** — `2 failed, 602 passed`: `test_protected_paths_breach_even_when_the_allowlist_names_them`, `test_C2_…` |

**Probes** (in-process, tree asserted clean by `git status` and `marker_path`'s loaded source verified unmutated by `inspect.getsource` first): the JR-18 writes-arm escape, the `.git\tevil` rollback refusal, and the ten-mint-site recount.

Closing receipt: `git diff HEAD -- agentic_orchestration/factory` **empty**, suite re-runs **604 passed in 165.66s**. The tree I am handing back is the tree I measured.
