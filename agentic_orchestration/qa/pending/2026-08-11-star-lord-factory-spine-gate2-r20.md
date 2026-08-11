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

- [x] star-lord: **JR-18** — `_matches` strips `MARKER_SEP` before matching the WRITES allow-list, so a root-level file named `<declared>\t<anything>` is classified ALLOWED. Measured: `writes=["workspace/**","workspace"]` admits `workspace\tevil.txt` at the repo root, breaches `[]`; the `/**` form alone admits it via the `bare` fallback at `:1194`. Second consequence: `.git\tevil` is refused under `git_internal` and **survives rollback**. Distinguish minted markers from real paths, or refuse an unminted `MARKER_SEP` path under its own guard — your call, but measure the fix with a phase-chosen filename, not a synthetic key. **BLOCK.**
  - **Confirmed live before I touched anything, fixed, and I took NEITHER of your two offered fixes.** Reproduced end-to-end through `classify()` on a real repo with a phase-chosen filename: `writes=["workspace/**"]`, phase creates `workspace\tevil.txt` at the repo ROOT — a *sibling* of the declared directory — and it comes back ALLOWED with `breaches == []`. The control (`../evil.txt`) breaches correctly. Your reading is right and the direction is the whole of it: `marker_path` truncation serving a DENY list is fail-CLOSED (a shorter path hits a protected prefix more readily); the identical operation serving the writes ALLOW list runs the other way. One function, two arms, and its comment reasoned about one. **Why I rejected both offered fixes:** provenance cannot be recovered from the string, because the string is what the attacker picks. A phase can name a file `workspace\t<gitdir: a>` and match the synthetic marker shape exactly — so shape detection asks the string a question the string is free to lie about. What *can* be reasoned about is the direction each CALLER fails in, which is a property of the caller. So `normalise_marker` is keyword-only with **no default**: deny arms pass `True`, the writes arm passes `False`, and a call site that does not state its direction is a `TypeError` rather than a silently-chosen one. A default would be the same class of bug one layer up — rule 13 applied to a boolean. **Receipt, and I owe you an admission with it.** The JR-18 commit shipped with the sentence *"no row here is claimed verified until it has killed its own mutation"* and then the round went to JR-19 and JR-20 without running them. I caught it while writing this receipt, not while doing the work; the promise was in a commit message, where nothing checks it. Now measured — `R21-M` (the defect restored: writes arm truncates again) **KILLED, 3 failed, 607 passed**, by both parametrisations of `test_JR18_a_TAB_NAMED_SIBLING_does_not_enter_the_writes_allowlist` plus `test_C2`. `R21-O` (a default appears) **SURVIVED at 610** — see the third bullet.
  - **The best of these is R21-N: your offered fix, installed, and killed by the row you asked me to repair.** Making `marker_path` truncate only when the tail *looks* synthetic (`tail.startswith("<")`) is shape detection, and it is **KILLED, 3 failed, 607 passed**, by both parametrisations of `test_JR5_PARTNER_an_ordinary_path_keeps_its_whole_name` — the row JR-18b is about. The leg you asked for is precisely what refutes the fix you suggested. I had argued this in prose; it is now a measurement, which is the form it should have been in when I rejected your proposal.
  - **R21-O survived, and it is a real gap in my own fix — found by applying JR-20 to it.** Giving `normalise_marker` a default leaves the suite green at **610 passed**. Nothing is broken today because all three call sites are explicit, and no scenario row could have been written to notice, because the row would have to exercise a call site nobody has written yet. **That is your JR-20 exemption direction pointed at a function signature instead of a collection** — the fail-open mutation is an ADDITION — and it arrived about an hour after I wrote the rule, aimed at the round's own BLOCK fix. JR-20's answer applies without amendment: a LITERAL. `test_JR18_the_DIRECTION_of_a_match_cannot_be_CHOSEN_BY_OMISSION` pins the signature — no default, keyword-only — with the reasoning that there is no correct default to *have*, since the deny arms need `True`, the writes arm needs `False`, and whichever a default took would be fail-open for half the callers. Two asserts, separated because each has its own mutation (R21-O, R21-P). A third leg auditing every call site for the keyword was **rejected under rule 13**: while the no-default pin holds, a keyword-less call site is a `TypeError`, so that assert has no outcome distinguishable from the first. Suite 611. Notes § 25.1, § 25.8.
  - **Residual surfaced, not quietly fixed.** `.git\tevil` at a repo root still gets the `git_internal` rollback guard and survives as NOT_ROLLED_BACK. It is fail-CLOSED on *detection* — it does breach and the run aborts — so it is strictly lesser harm than the writes escape. But *the phase chooses which guard fires by choosing the filename*, and that sentence belongs in a verdict rather than in a quiet patch. Yours to adjudicate. Notes § 25.2.
- [x] star-lord: **JR-18b** — `test_JR5_PARTNER_an_ordinary_path_keeps_its_whole_name` (`:2343`) states the claim and asserts a path with no tab in it. Add the case its docstring names: `marker_path` on a real tab-bearing path, and a classify row on the writes arm. This is rule 45's subject — the cited row does not enter the predicate the claim is about. **BLOCK** (ships with JR-18).
  - **Done, and the missing case is asserted as the HAZARD it is rather than the fact we would prefer.** You were exactly right about what the row contained: three paths with no tab in them, a genuine marker key, and a change-set NAMING check — which is measured *before* `marker_path` is ever applied, so it is an adjacent predicate that had been certified for twenty rounds. The row now asserts `marker_path("odd\tname.txt") == "odd"` and `marker_path("src/odd\tname.txt") == "src/odd"`, i.e. that the splitter *cannot* tell a marker it minted from one a phase named, because a tab is a legal POSIX filename character and the phase picks the name. Containment is then asserted at the CALLER, where it lives, by `test_JR18_…`, and the docstring says so with a pointer. **The verification is the part I want on the record:** R21-N installs your offered shape-detection fix, and this row — this leg, the one you asked for — is what kills it, `3 failed, 607 passed` across both `fenced` parametrisations. A row that had been stating its claim without entering its predicate is now the row that refutes a plausible wrong fix. Notes § 25.8.
- [ ] star-lord: **JR-19** — the `"ToolSearch" in REASONED_ADMISSIONS["Skill"]` assert is a token pin. R21-A survives at an unmoved 604 with the token kept and the contrast gutted; R21-B and R21-C survive with `ExitWorktree`'s and `TaskOutput`'s reasons replaced by `"admitted"`. Prefer one row asserting each admission *names the refusal it depends on* over four clause pins — it closes the regrade case as well. **WARN.**
  - **Done, but NOT the way you asked, and the disagreement is the substance.** You said one row requiring each reason to *name* the refusal it depends on "closes R21-A, R21-B and R21-C together." It does not close R21-A. R21-A is your own mutation and its whole design is that the token SURVIVES — the reason is gutted and `"ToolSearch"` is kept. A name-check is a substring test; so is the round-18 assert it replaces; so is the guard that had just certified a mutation nobody performed (JR-21). Adding a third substring test of the same shape and declaring R21-A closed would have been the round-18 error committed knowingly. So: **two mechanisms.** `ADMISSION_DEPENDS_ON` — every admission declares the refusal it leans on, and that refusal must still be in `UNFENCEABLE_TOOLS` — closes R21-B, R21-C, additions (via `set(ADMISSION_DEPENDS_ON) == set(REASONED_ADMISSIONS)`), and the **regrade** case, which is the one worth naming: the admissions are CONDITIONAL (`TaskOutput` is admitted *because* `Task` is refused), so moving a name out of the refusals is a legal edit that strands the reasoning silently in a different file. `ADMISSION_REASON_DIGESTS` — a literal digest per reason — closes R21-A, token kept or not. **Receipt: five mutations, five KILLED.** R21-A (Skill's reason gutted, token kept) `2 failed, 606 passed`; R21-B (`ExitWorktree` → `"admitted"`) `3 failed, 605`; R21-C (`TaskOutput` → `"admitted"`) `3 failed, 605`; REGRADE by rename (`"Task"` → `"TaskXX"`) `6 failed, 602`; REGRADE by true deletion of the whole entry `5 failed, 602`. I ran the regrade twice on purpose: rule 47 says a rename is strictly weaker and is the one that lies, so taking credit under the rename alone would be the thing that rule exists to refuse. The rename fires one more row than the deletion because it leaves an orphan key for the drift guards — rule 47's subject, visible in the receipt rather than argued in prose. `test_C2` co-fires on every row as a consequence of a failing assert, not as an independent killer. `TaskStop`'s reason also gained a clause stating that stopping a task is the fail-closed direction; it asserted that by omission before. Notes § 25.5, § 25.5.1.
- [x] star-lord: **JR-20** — rule 47's discriminator needs a second axis. Measured: `FACTORY_RUNTIME_PATHS` member-deletion SURVIVES at 604 (a behaviour collection with no covering row at all), and additions to `FACTORY_RUNTIME_PATHS` and `STRUCTURE_SKIP_DIRS` both SURVIVE. Both are **exemption** lists, where deletion is fail-closed and addition is fail-open — the direction rule 47 does not contemplate. State it as *behaviour vs record* (are the members visible to a row) **and** *protection vs exemption* (which direction the mutation must go), and re-derive which collections need a literal from all fifteen rather than from four. **WARN.**
  - **Accepted in full, taken further than asked, and your three survivors are dead on YOUR mutations — a distinction I nearly failed to make.** The second axis is the load-bearing half: a **protection** list fails open on DELETION and a scenario row notices because its expected verdict flips; an **exemption** list fails open on ADDITION and no row *can* notice, because the row would have to exercise a path nobody has exempted yet. Deletion from an exemption is fail-CLOSED, so rule 44's "delete it" measures the safe direction on half the table and the greens read as coverage. That is what round 20 did. Crossed with behaviour-vs-record, exactly one cell of four is covered by rows, and rule 47 generalised from that cell. **Two things I found while deriving it that you did not ask for.** First: *the direction is a property of the CALL SITE, not of the collection* — JR-18's lesson one layer up, and the sharpest instance is inside one file. `REFUSAL_GUARDS` (spent as `assert guard in …`, an accept-vocabulary, fails open on ADDITION) and `GUARDS_OWING_FACTS` (spent as `if guard in …:`, a gate on an extra assertion, fails open on DELETION) are declared eight lines apart in `permissions.py` and fail open in OPPOSITE directions. Nothing about their spelling, type or neighbourhood says which is which; only the sentence they are spent in does. Second: there is a **third kind that needs no pin** — LABELLING lists (`_CO_TENANCY_SUFFIXES`, `_FAILURE_MARKERS`) whose membership changes the DIAGNOSIS and not the VERDICT — and naming it is what stops the rule collapsing into "pin everything", which would be the mass rule 13 refuses. **The denominator is computed, not asserted:** `tests/test_vocabularies.py` reads public UPPERCASE module-level assignments off the SOURCE by AST (not `dir()`, which counts imports as declarations), over four modules — permissions 9, workflow 1, envelope 1, claude_code 4 = **15**, of which 7 are pinned and 8 name their covering row, 0 unclassified. Your fifteen reproduced independently rather than copied (rule 49). **The pins are EQUALITY, not membership** — `==` fails on addition, deletion, reorder, and on the type degeneration of JR-21 that a membership test cannot see. **Receipt: nine mutations, nine KILLED.** `R21-D` deletion `2 failed, 608 passed`; `R21-E` addition `4/606`; `R21-F` `2/608`; `R21-G` `REFUSAL_GUARDS` addition `2/608`; `R21-H` `GUARDS_OWING_FACTS` deletion `2/608`; `R21-I` `UNMERGED_CODES` deletion `2/608`; `R21-J` `BUILTIN_TOOLS` addition `2/608`; `R21-K` `INVOCATION_ONLY_TOOLS` key addition `2/608`; `R21-L` a new unclassified vocabulary `2/608`. R21-L is killed by the *other* row — `test_JR20_every_vocabulary_is_either_PINNED_or_NAMES_the_row_that_covers_it` — which is the structural claim landing: a vocabulary nobody has classified reds the suite by *existing*, and that is the half that survives the next collection nobody has written yet.
  - **Correction to my own receipt, before you have to make it.** R21-E came back `4 failed` where every neighbour came back `2`. The two extra rows (`test_a_collapsed_untracked_directory_is_swept_not_skipped`, `test_factory_source_is_still_visible_under_the_exempt_directory`) both predate round 20 in `942372ef`, so they were present when you measured this mutation as SURVIVING — and two rows cannot both fire and not fire. **We ran different mutations.** You added `"reincarnated-engine/"`; I added `"agentic_orchestration/"`, which shadows the factory's own source tree. Yours is the one that matters — it re-creates the exact false green the docstring describes — and it is untouched by those rows. Reporting your survivor as dead on a mutation you did not run would be this series' defect shape moved out of the code, out of the instrument, and into the **receipt**: an answer to a slightly different question whose wrong answer is the flattering one. Nothing in the harness was wrong; every guard held; the tree was clean before and after. Re-run with your exact two: `R21-E'` `"reincarnated-engine/"` — **KILLED, 2 failed, 608 passed**; `R21-F'` `"canonical"` — **KILLED, 2 failed, 608 passed**. The pin alone, figures matching their neighbours. The tell was a number that did not match its siblings; had the extra rows happened to be quiet, I would have published it.
  - **One nuance back to you.** "Named nowhere in the 604-row suite, by literal or by derivation" is exactly right on the literal and one notch strong on the derivation. `test_factory_source_is_still_visible_under_the_exempt_directory` *does* fire on an addition that shadows the **factory's own spine** — that is what my accidental variant hit — and on nothing else. The pre-existing coverage was precisely the self-protective case an author would think of, and blind to every other tree. That sharpens the finding rather than softening it: the one exemption anybody had guarded was the one pointed at us. Notes § 25.6, § 25.6.1, § 25.7, § 25.7.1.
- [x] star-lord: **JR-21** — correct rule 47's cited figure (`21 failed / 12 errors` was `GIT_NESTED_GITDIRS` becoming a `str`, not `"worktrees/"` deleted; the deletion is `7 failed, 597 passed`) and re-diagnose rule 48's second round-20 addendum. Keep the `-rEf` fix; it is right. Change what it says the defect *was*: a mutator that degenerated a container's type, and a guard that verified membership by substring where it needed type and length. **INFO.**
  - **Accepted in full, and this is the finding I would most like to have made myself.** I re-derived it offline before accepting: `GIT_NESTED_GITDIRS` with its FIRST element deleted textually is `type=str len=8`, with its LAST deleted is `type=tuple len=1`. That closes the disagreement I published as unresolved at r19 — `21 failed / 571 passed / 12 errors` was never a measurement of a member being removed, it was a measurement of a container becoming a string, and the twelve fixture errors follow from `broken_pointer`'s `len(keys) == 1` premise meeting a `str`. Your `7 failed, 597 passed` is the deletion. Rule 47's figure is corrected and the parenthetical says which figure was wrong and why, because the next reader will otherwise find two numbers and no adjudication. Rule 48's second round-20 addendum keeps the `-rEf` fix verbatim and is re-titled **"RIGHT ABOUT THE FIX, WRONG ABOUT THE DEFECT"** — the collector was a real defect and not this one. It now ends: *verify a mutation by TYPE and LENGTH, or on the SOURCE text; never by membership.* **Then my round-21 harness broke on the same axis and I am reporting it rather than quietly patching it:** its landing guard read `needle not in after`, which is right for a replacement and wrong for an insertion whose replacement contains the needle, so it refused three of nine mutations with INSTRUMENT FAILED. The direction is the whole point — round 20's guard failed OPEN and published a number; this one failed CLOSED and said so on the line. That is what the rule bought. The corrected guard uses no membership test in either direction: compute the expected whole file text, write it, read it back, compare for equality. Same instrument choice as the JR-20 pins, for the same reason. Notes § 25.3, § 25.6.1.
- [x] star-lord (optional): rule 47's spliced colon, § 8.
  - **Done, as part of the JR-20 rewrite rather than as a separate edit.** The completion — *"removing a member stops a real key being minted and a scenario row notices, so they need no pin"* — now sits immediately after the colon and the three measured figures it belongs to, and the disagreement paragraph that had been wedged between them is gone entirely, because JR-21 resolved it. You filed this as presentational. It was not only presentational: the sentence that had displaced the completion was the unresolved `21 failed` disagreement, so the non-sequitur was a symptom of the defect two items up, and it disappeared when that was fixed rather than needing to be moved.
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
