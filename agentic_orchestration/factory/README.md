# factory — the spine

**Built by:** star-lord (ruling D4)
**Against:** `agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md` (Spec A)
**Strategy of record:** `agentic_orchestration/operating-procedures/software-factory.md`
**Status:** v1 landed 2026-08-10. Spec A § 11 acceptance items 1–4 mechanically proven
(item 5, jack-ryan Gate-2, is queued — no compiled *agentic* workflow runs before it).

This is the SPINE layer of CHARTER / SPINE / LABOR. It does not decide what work is
worth doing (charter) and it does not do the work (labor). It runs phases, adjudicates
their claims against the disk, and writes receipts.

---

## The five compiled laws

Everything in this package exists to make one of these mechanical rather than
aspirational. Each has a test that reds when the law is broken.

| Law | Where it lives | Where it is proven |
|---|---|---|
| A phase is FAILED until exactly one `finish()` collapses it — **no override exists** | `phase.py` | `tests/test_phase.py` |
| Dataclass, JSON schema and prompt block are **one field table** | `envelope.py` | `tests/test_envelope_triad.py` |
| Gates adjudicate the world, never the envelope's word; **NOT_RUNNABLE is red**; **zero stubs** | `gates/` | `tests/test_gates.py`, `tests/test_no_stub_gates.py` |
| A write outside the allowlist is **quarantine + rollback + ABORT**, never a retry | `permissions.py` | `tests/test_permissions.py` |
| **Only failures travel**; reasoning tokens are a share of output, **never a fifth addend** | `gates/core.py`, `usage.py` | `tests/test_gates.py`, `tests/test_usage.py` |

## Layout

```
factory/
  phase.py         default-fail phase primitive
  envelope.py      the synced triad (one _FIELDS table -> dataclass + schema + prompt)
  gates/           base.py (registry, GateReport, RunContext)
                   core.py (the v1 six + command_succeeds)
                   digest.py (sha256_matches)  media.py (ffprobe_verifies)
  permissions.py   before/after tree fingerprinting, classify, quarantine, rollback
  harness/         claude_code.py (LIVE)   codex.py (HONEST STUB, blocked on T16)
  receipts.py      SQLite/WAL, 7 tables + schema_meta, SCHEMA_VERSION = 1
  runner.py        phases in order; fingerprint -> execute -> fingerprint -> permissions
                   -> gates -> fingerprint again -> phase verdict
  workflow.py      YAML/JSON loader; every refusal happens at LOAD
  report.py        renders from receipts only (one data path)
  cli.py           run · status · report · gates · determinism · probe-agent
  workflows/       kc2-baton-mechanical.yaml (the founding run's mechanical cells)
  pytest.ini       states the suite's subject; keeps the walk out of sessions/ (rule 23)
  sessions/        per-run session dirs, incl. the durable breach QUARANTINE
  tests/           471 tests, all green (~110 s: the reach audit runs the suite twice)
                   _reach_tracer.py  sys.settrace line collector, loaded in the child
```

## Use

```bash
cd agentic_orchestration/factory

./factory gates                                   # what can adjudicate a claim
./factory run workflows/kc2-baton-mechanical.yaml # run it
./factory status                                  # recent runs, from receipts
./factory report <run_id>                         # the full receipt, rendered
./factory determinism workflows/<wf>.yaml         # two laps, compare gate verdicts
./factory probe-agent <seam>                      # smoke the live harness lane
```

Nothing here writes to a remote, and nothing here runs `--dangerously-skip-permissions`.

## Why the runner fingerprints twice

Mechanical cells do their work *inside* a gate command (`tests_pass` /
`command_succeeds`), so a write made by the command itself lands after the
post-execution snapshot. A single check would let a gate's own writes escape
containment. The second pass aborts with `during="gate execution"` so the receipt
says which side of the boundary the breach came from.

## What "the tree was clean" is worth

Containment is a git change-set diff, so it is only as good as what git will
describe. **Seventeen rules** keep the claim honest, each one added closing a Gate-2
finding that had the *same shape*: a predicate answering a slightly different question
than the one asked, whose wrong answer is always `clean` — or, once, `restored`.

1. **Gitignored is not exempt.** `git status --porcelain` never reports ignored
   paths, so the v1 build was blind to the engine's `seasons/` and `telemetry.db`
   — inside a tree the workflow declares read-only. Status is now read with
   `--ignored=traditional` and the collapsed entries are swept. The only exemption
   is `FACTORY_RUNTIME_PATHS`: six named paths, root repo only, recorded on the
   fingerprint whenever one is taken.
2. **Unmeasurable is not clean.** A declared repo that is not a git worktree used
   to produce an empty diff, and an empty diff reads like innocence. Such a repo
   now fails at LOAD; a snapshot that fails mid-run raises `ContainmentError`.
3. **Coarse is declared as coarse.** A region over 50,000 files (the godot tree's
   `.godot/` + `Assets/Synty/` = 259k) falls back to directory mtimes: catches
   creation, deletion, rename; **misses in-place content edits**. Every phase emits
   a `containment_coarse` receipt naming the regions and the caveat. A test asserts
   the blind spot exists, so the caveat can only be weakened on evidence. **On the
   agentic lane the caveat is not enough** (C5): a caveat is a claim to a reader, and
   the agentic lane is defined by a model choosing its own paths — the case the caveat
   does not cover, made worse because these regions are gitignored, so an in-place edit
   there is neither detected *nor* recoverable. A workflow with an agentic phase is
   refused at LOAD unless it names each coarse region under `coarse_acknowledged:`.
   Naming a region that is *not* coarse is refused too: an acknowledgement drifted from
   the tree reads as diligence and certifies nothing. Measured here: the meta-repo and
   the engine have zero coarse regions; godot has exactly two.
4. **A fence is judged where the artifact IS.** `read_only_trees` is matched on the
   path's lexical *and* resolved form, breaching on either. `.resolve()` alone
   follows symlinks, so a link planted inside a fenced tree was judged by where it
   *pointed* — a link to `/tmp` walked straight out of the fence (H1).
5. **Unreadable is not clean.** `git status` reports a directory it cannot descend
   into on **stderr**, with exit code 0 and nothing on stdout, so a `chmod 000`
   subtree measured as untouched. Warned paths are folded into the fingerprint:
   unreadable at both ends is unchanged, unreadable at one end is a change.
6. **The status output is parsed with `-z`, and both ends of a rename are fenced.**
   Porcelain v1 C-quotes special paths and uses ` -> ` as its rename separator — a
   delimiter a filename can legally contain. Keeping only the last field dropped the
   rename SOURCE, so `git mv` out of a fenced tree named only a legal destination and
   passed; and a file named `junk -> src` parsed to `src`, a real path the rollback
   then deleted. `-z` is NUL-separated, never quoted, and emits the rename origin as
   its own record.
7. **Rollback never deletes content git knows about — asking BOTH questions.** A
   `created` path cannot contain anything git already has; if it does, the path
   identification is wrong and the deletion is refused with a reason. `git ls-files`
   alone is the index, and the index can be silenced while the content is still
   committed and still on disk (`git rm --cached`, `assume-unchanged`), so the guard
   unions it with `git ls-tree -r HEAD`. Either question alone is answerable `no`
   while work is present; both together are not. This does not depend on knowing
   which bug produced the bad path. Containment must never be the thing that destroys
   work.
8. **Empty directories are swept on the read-only trees.** git tracks content, so a
   wholly-empty directory tree is invisible at every porcelain setting. This was
   declared as a bounded blind spot and then closed: it is not inert (a bare directory
   is a PEP-420 namespace package; a new `res://` directory enters Godot's import
   scan) and a structure-only walk — no stats — costs 0.21 s for the engine and
   1.69 s for godot. `.git` is excluded: 281 of the engine's 968 directories live
   under it and its object fanout gains one on a plain `git add`, so including it
   made *disciplined* git use inside a fenced tree read as a structural write.
9. **A measurement that cannot NAME what moved is not wired to a verb that acts.**
   The sweep first returned `dirs:<n>:<hash>`. A hash can only say that something
   moved, so the diff reported the change at the read-only TREE — which the rollback
   handed to `git checkout --` as a pathspec, reverting every uncommitted change in
   the repository over one empty directory, while the directory itself survived. The
   receipt word was `restored`. The sweep now returns the directory set and the diff
   names the directory (K1).
10. **The rollback refuses a whole-tree pathspec.** `.`, the empty string, and any
   declared repo or read-only tree root come back `NOT_ROLLED_BACK` with the reason
   stated. A rollback that cannot name an artifact has identified a *tree*, and
   undoing a tree is a human decision. This is rule 7's principle applied to the
   other destructive verb, and it does not depend on knowing which measurement
   produced the coarse path.
11. **Absent from the baseline means clean, not new.** A tracked file nobody has
   touched is not in `git status` output, so reading absence as newness typed the
   most likely agentic breach there is — an agent edits a committed source file — as
   `created`. It hit rule 7's guard, came back refused with a reason that asserted a
   misidentification which had not occurred, and the edit survived inside the fence.
   The kind is now read from git's own status code — but see rules 13 and 14, which
   are the two halves of that fix that the first version got wrong (K2, L2).
12. **A path is not a pathspec.** Every path this module hands to git is read off a
   fingerprint, but git reads pathspecs as a *language*: a leading `:` is magic, so
   `:(top)` and `:/` mean the whole repository, and `*` `?` `[` glob. A file legally
   named `:(top)` at a tree root therefore turned `git checkout -- <that path>` into a
   repo-wide revert reported as `restored`, and turned `ls-files -- <that dir>` into
   rc=0 with empty output — and empty is what authorises `rmtree`. Every git call now
   runs under `GIT_LITERAL_PATHSPECS=1`. No call site wants globbing, so this removes
   an interpretation nobody asked for. **Rules 7 and 10 hold only because of this
   one**: both enumerate paths, and an enumeration is worthless if git re-reads the
   entries as patterns (L1).
13. **The status-code classifier is a closed table, and `unknown` is refused by
   name.** The first fix enumerated part of the code space and defaulted the rest to
   `modified`; the second wrote character-class tests under a docstring claiming
   closure, which handed a confident answer to 29 codes nobody had listed. Closure is
   now a property of a dict. A default that catches every code nobody thought about is
   how this class recurs — default-fail has to reach the classifier, not just its
   callers (L2).
14. **Containment does not restore staged work — it refuses and names the index.**
   `git checkout -- <path>` restores from the *index*, so it is a restore only while
   the index still holds the baseline. The moment a phase runs `git add`, the index
   holds the phase's content and the same command rewrites the file with exactly the
   bytes being removed, then reports `restored`. Found on a rename destination and
   first closed by re-typing that one code; the property is the whole `X≠' '` column,
   including `M ` — a staged edit of a tracked file, the most ordinary thing a
   disciplined agent does. Staged creations, modifications, renames and deletions all
   now come back refused, naming the index and printing the recovery command. Editing
   the index of a fenced tree is a human decision (L2, general).
15. **A refusal the operator never sees did not happen.** The paths the rollback
   deliberately declines to undo were returned in a list and dropped, so an abort
   report could say the run was contained while the tree was not clean. Each one now
   emits a `containment_not_undone` receipt naming the path and the reason (L6).
16. **Ask git about the tree, never a label this module wrote.** Rule 14's guard read
   the porcelain status *string* — so it was correct for every change git named, and
   blind to the one kind of change git does not. The structure sweep emits its rows
   with `after_status="structure"`, a label invented here; the guard measured it, found
   it was not two characters, answered "not staged", and handed a **directory** to
   `git checkout --`, which restored it from the index. Staging a fenced file and then
   removing its directory put the phase's own bytes back inside the tree under a
   receipt reading `restored` — on the row beside an honest refusal for the same file.
   The question is now asked of the repository (`git diff --cached HEAD -- <path>`),
   which is a property of the tree rather than of a string, and is therefore immune to
   a status being synthetic, absent, or added later. The rename pair needs no
   hand-placed exemption any more; git reports it. Note the destroyer guard was never
   fooled, because it had always asked git — only the guard that trusted a string was
   fooled by a string (L8).
17. **A negative claim is a claim, and it travels as a number.** The refusal for a
   staged removal told the operator "the index no longer holds it" without ever reading
   the index, one line above a command that reads the index — and for `MD` the index was
   holding the phase's content. Every clause in every refusal is now derived from a
   measurement. The first version of that fix wrote the measurements into English and
   the wall checked the English, so a refusal whose numbers were all flatly wrong passed
   410 tests as long as the sentence still read the way it used to. The measurements now
   travel on the action as `facts` — `(name, value)` pairs — the prose is *rendered* from
   them by `render_containment_facts()`, and the wall compares the pairs to git and then
   asserts the rendering appears in the reason. An operator reads numbers off an abort
   report and acts on them; a claim checked only as prose is a claim nobody checked
   (L9, B1).
18. **A refusal says WHICH guard fired, from a closed vocabulary.** Rule 17's own fix
   then had to decide *when* a refusal owes numbers, and asked a number it was
   certifying (`if expected["staged_paths"]:`) — so a guard could switch off its own
   certification by reporting zero. Every refusal now carries `guard=`, one of ten
   names in `REFUSAL_GUARDS`; the two that make counted claims are listed in
   `GUARDS_OWING_FACTS`, and the wall refuses a name outside the set. Whether a claim
   must be checked is decided by *which* claim was made, never by *what it said* (C1).
19. **Some paths are protected in every declared repo, not just the root.** The
   always-protected list was matched only against the root repo, so a phase declaring
   a sibling repo as a write target could write `.claude/` there — the next-session
   hijack the protection exists to prevent, at a path the workflow itself named.
   `PROTECTED_EVERY_REPO` is matched in **any** declared repo and is not
   config-overridable; the root-only entries stay root-only, and a row asserts that too,
   so the fix cannot quietly become a blanket fence (C4).
20. **An allowlist must RESTRICT, not merely be present.** C3 made an absent `tools`
   a refusal at both entry points and stopped there — a test of *declaration*. The
   state it exists to prevent, the full built-in tool set chosen by nobody, was still
   reachable by writing one word, `default`, and it read as diligence. `tools` is now
   checked against a **closed vocabulary** (`BUILTIN_TOOLS`, read off the `init` frame
   of a live run, not copied from documentation): `default` refused by name, a non-list
   refused (YAML `tools: Read` is a string, and `list("Read")` is four tools that do not
   exist — an allowlist that restricts by *accident*), an unenumerated name refused, an
   MCP name refused because its availability is per-machine. The vocabulary lives on the
   **harness**, and the loader refuses any harness that does not publish one, so a second
   lane cannot become the route around it (F4).
21. **Git's own control surfaces are measured, and refused rather than rolled back.**
   `.claude/` was protected in every repo (rule 19) while `.git/hooks/pre-commit` — the
   same hijack aimed at the next thing a *human* does in that repo — was not merely
   unprotected but **unmeasurable**: `git status` does not report paths under `.git/` at
   any porcelain setting, so the write produced an empty change-set and containment
   reported a clean tree. Every other path in `permissions.py` arrives through git; these
   three (`hooks/`, `config`, `info/exclude` — the surfaces that change only when
   somebody decides to change them, never on ordinary `git add`/`commit`/`gc`, which is
   K1's lesson) are measured directly, are in `PROTECTED_EVERY_REPO`, and hit a dedicated
   `git_internal` refusal: git tracks nothing there, so the destroyer guard would find
   nothing and authorise `rmtree` on `.git/config`, and `git checkout --` cannot restore
   a path git has never heard of. Both verbs are wrong, so the guard quarantines, names
   it, and stops (F3).
22. **A containment waiver is re-asserted while the run is happening, and keyed on
   something unique.** C5's `coarse_acknowledged` check ran at LOAD, which is right and
   is not sufficient: a region can cross the scan cap *during* a phase — including
   because the phase wrote enough files to push it over, the case where the waiver
   matters most — and nobody re-asked. It is now re-asserted at every snapshot on the
   agentic lane, off the fingerprint that was already computed (F5). And the key was
   `repo.name`, so two declared repos at `~/a/engine` and `~/b/engine` shared it and one
   waiver silently cleared a region in a tree nobody looked at; `coarse_key()` is the one
   spelling, on the resolved path, called by both the loader and the runner (F6).
23. **The suite states its own subject; the quarantine is not part of it.** What
   `rollback` refuses to undo it quarantines, durably, *inside this tree* at
   `sessions/<run>/breach/…` — and the wall's fenced trees contain test files, so the
   quarantine holds copies of `test_*.py`. Containment was working; the walk was not:
   `pytest` typed at this directory collected the quarantine and reported 33 errors on
   artifacts that are inert by intention. `pytest.ini` pins `testpaths` and excludes
   `sessions`, and a row plants an unparseable file where quarantine puts things and
   requires a root-cwd collection to stay clean — over both the bare invocation and the
   explicit `.`, which is how the ablation showed `norecursedirs` doing the work and
   `testpaths` merely saying so out loud (F7).
24. **The argv is not the grant.** Every permissions row on the agentic lane certified
   what the harness *sends*. The `claude` CLI takes its permission mode from
   `~/.claude/settings.json` when no flag pins it, and on this host that file carries
   `defaultMode: bypassPermissions` — under which `permission_denials` cannot fire at
   all. So the row named "no permission-skipping flag appears anywhere" was passing on
   a lane that skipped every permission, and the denial adjudicator was reading a list
   structurally incapable of being non-empty. The mode is now pinned on the argv *and*
   adjudicated against the `init` frame, which is the CLI reporting what it actually
   did; a disagreement fails the phase, and so does an absent init frame — no evidence
   about the grant must not read as no problem (H1). The same frame showed two MCP
   tools granted under an explicit allowlist and a scoped form dropped silently by
   `--tools`, so the grant is compared to the declaration by base name,
   `--strict-mcp-config` is passed, and the two tool flags now receive different
   strings because they accept different ones (H2).
25. **A trigger reaching a predicate is not the same as a predicate being called with
   it.** The round-thirteen mutation set had sixteen rows and every one mutated a
   predicate some test called directly; none mutated a *call site*. `_note_coarse`'s
   post-gate caller passed no `agentic` argument at all, and every row on the function
   stayed green. The argument is now required — omitting it is a `TypeError` rather
   than a default — each of the three call sites has a row that never names `agentic`
   itself, and the rows assert on the `when` label so one site's abort cannot be
   mistaken for another's. Wiring is a mutation *category* here now (H3). The first
   draft of the post-gate row asserted `status == "ABORTED"`, which the breach
   classifier satisfies independently: it passed with the gate under test disarmed.
   *And a signature is a rule that needs its own row.* Giving `agentic` a default of
   `True` survived the round-fourteen set — correctly, since all three call sites pass
   it explicitly — but the survivor showed that nothing tested the requirement itself,
   so the next call site could inherit a silent default. A parameter deliberately left
   without one is refuted only by a call that omits it.
26. **Unknown cost is not zero cost.** `Phase.usage` defaulted to
   `"mechanical phase — no model invoked"`, and the only path that ever read that
   default was the one where an agentic phase's harness died mid-flight — so the
   durable `phases.usage_absent_reason` column asserted that no model ran, for a phase
   that named an agent and launched a harness, at exactly the moment spend was least
   accounted for. `usage.py`'s own law is that absent is absent and never invented;
   inventing the *reason* breaks it as surely as inventing a token count, and worse,
   because the invented reason is the reassuring one. Three states, three reasons, each
   refutable on its own path: no attempt, attempt in flight (cost UNKNOWN), no model
   invoked — the last reserved for the one lane where it is structurally true (H8).
27. **A repo has as many gitdirs as it has submodules and worktrees.** F3 closed the
   `.git/hooks/pre-commit` vector and measured a single gitdir, so the same write one
   directory deeper — `.git/modules/<sub>/hooks/pre-commit` — stayed invisible. The
   closed control list now recurses into `.git/modules/` and `.git/worktrees/`, and the
   entry names of those directories are measured so a gitdir *appearing* is itself the
   change. The entry is a synthetic key: keying it on the real directory path made
   `_signature` stat-sweep the gitdir's index, refs and object store, which would have
   breached on every ordinary commit — K1 verbatim, on the axis added to fix it. The
   partner control (`add`/`commit`/`gc`, plus churn written inside the nested gitdir)
   is what caught that during authoring (H4).
28. **A control row must be RUN against the regression it controls for, not aimed at
   it.** That partner control, as first written, compared `_git_control_entries()`
   before and after — a map of names to a constant. The K1 false-breach lives one
   function downstream, where `fingerprint` computes `content[p] = _signature(root, p)`
   for each of those keys: the synthetic key resolves to nothing, the real key resolves
   to a directory and gets stat-swept. Both keyings yield the *same key set*. So the
   mutation that re-introduces K1 left the anti-K1 row green, and the row's docstring
   claimed it had caught the defect. It had — once, by hand, before it was narrowed to
   the cheaper comparison. The row now compares `perm.fingerprint(...).content` across
   the git-control keys, which is the thing that actually carries the failure. Review
   read this row several times and saw nothing; the mutation found it on the first pass.

**The wall.** `tests/test_containment_wall.py` is the standing answer to that
repeated shape — twenty artifact kinds (regular file, symlink out of the tree,
broken symlink, nested dir, collapsed untracked member, gitignored file, nested git
repo, unreadable subtree, a quoted path containing the rename delimiter, a path with
a newline, a hard link, a mode-only change, a directory replacing a file, an empty
directory tree, a file whose name is pathspec magic, and the five staging shapes: a
staged creation, a staged modification, a staged rename, a staged edit whose whole
directory is then removed — the one that arrives carrying a status git did not write
— and the unstaged modification that keeps the staging guard honest) each run through
four rounds, **in both fixture shapes**:

1. the change-set must **name** the artifact — not merely be non-empty. The first
   draft asserted only non-emptiness, which was the module's own disease in the one
   assertion meant to cure it;
2. it must be **fenced** under `writes: ["**"]`;
3. the rollback must **report the undo honestly** — a `deleted` path must be gone, a
   `restored` path must be back at its *phase-start fingerprint* (mere existence is
   what `git checkout -- .` scored while reverting a repository), and a
   `NOT_ROLLED_BACK` must carry a reason **whose factual claims are re-derived from
   git and checked**. "Has a reason" was the weaker question: L3 was a refusal with a
   perfectly good non-empty reason whose every clause was false;
4. every **residue** left on disk must be named by an action **at or above it**.
   Reading that relation both ways let a receipt naming something enormous account
   for everything inside it.

Every round also asserts an **uncommitted-work canary** survives: one tracked file,
dirty before the phase runs, that no artifact touches. For four rounds every fixture
committed everything, so "a rollback destroys uncommitted work" — the K1 damage class
— was unobservable, and L1 shipped green under 262 tests.

**Two shapes, not one.** The wall ran for four rounds against a read-only
*subdirectory* under a docstring calling it the shipped shape. It is not: both shipped
read-only trees are worktree roots that are also `repos:` entries, so their change
paths carry no directory prefix. Pathspec magic is positional, so that missing prefix
is the whole of rule 12's reachability — an identical row is green in the subtree
shape and red in the shipped one. Every round now runs in both.

Each round has a falsification partner requiring the same artifact to be *allowed*
where it is declared. The wall found rule 5 on its first run. A new containment
question of this shape should be a new row, not a new reviewer finding — and **a new
measurement surface gets its row before it ships**: the structure sweep was added with
detection tests only, never reached rounds three and four, and that is exactly where
its defect lived (K1).

**Where the wall structurally cannot reach.** It plants artifacts, so it only reaches
status codes git actually emits — and rule 13's defect lives in the branch taken by
codes nobody enumerated. A mutation restoring that default changes the answer for 41
codes while leaving every wall row green, because no artifact can produce any of them.
A default-fail is a claim about inputs that have not happened yet; it is tested by the
alphabet (`test_permissions.py`), not by an artifact. The wall is the right tool for
artifacts and the wrong one for total functions, and knowing which is which is the
point.

**The wall is checked by mutation, not by its own greenness.** Each fix is reverted in
the shipped module, the suite is run, and the fix is restored; a fix whose reversion
leaves the suite green is a comment, not a safety measure. The first pass over round
six's fixes found **all seven survived** — including rule 12's, whose row planted the
right filename in the wrong state (a *created* `:(top)` is rolled back with `unlink`
and never reaches git at all). That table is what produced rules 13, 14 and 15.

**The wall is a product, and it has the same disease.** After eight rounds the defect
shape stopped appearing in `permissions.py` and started appearing in the thing that
certifies it — same shape, one layer up: *a check that answers a slightly different
question than the one asked, whose wrong answer is green*. Three instances, all live:

* an assertion **gated on a literal phrase the module no longer emits** never runs, and
  reports as a pass. Three of them were sitting in the wall. The first fix was a regex
  that scanned the wall for `if "<phrase>" in reason` and required every phrase to still
  exist in `permissions.py` (B2). It shipped with a sentinel proving the regex could
  recognise a phrase-gate — the right instinct, aimed at the wrong thing: the sentinel
  never showed the scanner could see the *suite*. Round ten replaced it with measurement
  (C2), and the measurement's first act was to report that **the scanner's own assertion
  had never executed, in any run** — it collected zero phrases from the wall. The check
  written to catch dead assertions was one. `tests/test_reach_audit.py` now runs the
  whole suite in a child process under `sys.settrace` and requires **every `assert`
  statement under `tests/` to have executed at least once**, which subsumes the regex
  and covers the shapes it could not see: another file, single quotes, an aliased
  subject. Three power checks stand behind it, because it can go quiet three ways — a
  sentinel (tracer can tell reached from unreached), an enumerator floor (it still finds
  the suite), and a comparison test (it is still looking);
* a check written against **prose** rather than the values the prose describes — see
  rule 17. Its own first fix then read `if action.facts:`, which the product switches
  off by sending nothing; whether a refusal *owes* the operator numbers is a property
  of the tree, so git decides it. Sourcing the expectation from git instead of from the
  object under test failed four rows within one run and exposed a **second refusal
  site** — the destroyer guard — still writing its counts into English. Both sites now
  carry structured facts. A fix applied where the reviewer pointed is not a fix applied
  to the class (B1);
* a predicate proven to REFUSE where it must, with **no partner proving it ACTS where it
  must not refuse**. `_staged_against_head` was reached only by rows where staging was
  present at the artifact path, so dropping its `-- <path>` pathspec — making "is
  anything staged *anywhere*" the question — left every row green while turning any
  unrelated `git add` in the repository into a blanket refusal to contain. The partner
  now stages a *different* file and requires the rollback to act (B3).

So the reachability clause is amended: **a new predicate ships with both branches
exercised** — a row where it must answer YES and the verb must REFUSE, and a row where
it must answer NO and the verb must ACT — and **its scope arguments and every factual
clause it justifies must each be independently falsifiable**: reverting any one of them
turns a row red. Three axes, because a predicate can be unreached by its arrival route,
by its arguments, or by the claim its output is used to justify.

Round nine added the fourth, by finding the shape in the *fix* for the certification:
**the condition that decides whether a check runs must be independent of every value
that check certifies, and must itself be falsifiable — inverting the trigger has to
turn a row red. A check that can be switched off by anything it is measuring is a
comment.** The wall's first fix triggered on `if action.facts:`, which the product
switches off by sending nothing; the second triggered on `if expected["staged_paths"]:`
— one of the three numbers the check exists to certify. The third sources the trigger
from a **closed vocabulary of guard identities** (`REFUSAL_GUARDS`), so a refusal that
owes numbers is decided by which guard fired, not by what the numbers say. The same
clause is why C5's lane condition ships with a mechanical row proving the loader still
says yes to the same tree, and why the C2 audit carries a comparison test: without them
"nothing to report" and "stopped looking" are the same green.

**Why the mechanical lane is easier than it looks — and where that stops.** Every path
a mechanical workflow touches is authored by a human in a YAML file under review, so
the adversarial-filename class (rule 6) is unreachable there. That is a property of its
*inputs*, not of its code — the moment a phase's paths come from a model's output the
immunity is gone. The limit of the argument is worth stating too: it covers only
defects that need a filename. **K1 needed none** — an ordinary `mkdir` or `git add`
inside a fenced tree was enough — so no lane is exempt from the containment rules by
virtue of who chose its strings.

**What the rollback promises.** Not that the artifact is always removed — nothing is
deleted unquarantined, so evidence that cannot be safely quarantined is deliberately
left in place and named. Three promises, in order of how much they cost to keep:

* the receipt and the disk **agree** — an artifact never survives while the receipt
  says `deleted`, and a `restored` path is back at its phase-start contents;
* the rollback **never destroys work** — it will not delete what git has (rule 7),
  will not act on a tree (rule 10), will not let git re-read a path as a pattern
  (rule 12), and will not restore over the phase's own index (rule 14). Where it
  cannot act safely it says so;
* what it leaves behind is **named**. Evidence left deliberately is fine; evidence
  left silently is not.

Gate commands run with `PYTHONDONTWRITEBYTECODE=1` and
`PYTEST_ADDOPTS=-p no:cacheprovider`. Running pytest inside a read-only tree writes
`__pycache__` there, which is a real breach; the fix is to stop the write, not to
exempt the path.

**A gate command is argv, not a shell.** Gates exec directly with no shell, so
`cd tests && pytest` execs `/usr/bin/cd` with three extra arguments — which `cd`
ignores, exiting 0. The gate reports **PASS for a command that ran nothing**: the
containment defect shape, in the gate layer, where the wrong answer is green. A
command holding an unquoted `&& || ; | > < $( \`` is now `NOT_RUNNABLE` with the
`cwd:` argument named as the fix. The check strips quoted spans first, because the
version that did not rejected `grep -c ";" file` — a command that is completely
fine — while its docstring claimed quoted forms were excluded. A guard whose
documentation is false about its own behaviour is the class under review.

## Session-local state (gitignored)

`sessions/` and `receipts.db` are runtime artifacts, not source. They are ignored
at the meta-repo root so that the factory's own writes never read as tree changes
during its own fingerprinting — `tests/test_permissions.py` pins that behavior.

## The open items, as resolved

Spec A § 13 asked four questions. All four were probed live before any code was
written (claude 2.1.119, Python 3.12.0, this host, 2026-08-10):

- **O1 — flag co-support:** CONFIRMED. `--agent` + `-p` + `--output-format stream-json`
  work together. **`--verbose` is mandatory** alongside stream-json in print mode; without
  it the CLI exits 1 *before any API call*. The adapter passes it unconditionally.
- **O2 — usage fields:** `input_tokens`, `output_tokens`, `cache_read_input_tokens`,
  `cache_creation_input_tokens`, `total_cost_usd`, `modelUsage{}`. No `reasoning_tokens`
  key was present → reasoning is NULL with a reason, never folded into output.
- **O3 — PyYAML:** present (6.0.3). `.json` workflows load through the same validator
  if it ever goes missing.
- **O4 — dollars: SPEC DELTA.** The spec expected `total_cost_usd` to be NULL on a
  subscription lane. It is **populated** ($0.0672 for a 4-output-token call). It is a
  harness-computed **list-price imputation**, not money billed — the Max subscription
  is flat. The schema therefore records the figure *and* `dollars_source`, so no
  downstream surface can report it as spend. Flagged to gandalf as DRIFT-CRITIC input.

A fifth flag was never on the § 13 list and shipped on this lane anyway: **`--tools` and
`--allowedTools` exist** (probed 2026-08-11, claude 2.1.119). `claude --help`: *`--tools
... Use "" to disable all tools, "default" to use all tools`*. So **omitting the flag is
not a neutral default** — it is the full built-in set, chosen by nobody. Every sibling
allowlist in this spine fails closed (an empty `writes` breaches everything, an empty
`gates` is a load error); this one failed open. An agentic phase with no `tools` allowlist
is refused at **both** entry points — the loader and the adapter — because a guard present
in only one of two entry points is a guard with a route around it (C3).

That fix was then **the class it was fixing**: it proved the guard REFUSES when the
allowlist is ABSENT and stopped, which is a test of declaration rather than of
restriction. `tools: [default]` is the exact state it exists to prevent, reached by
writing one word, and it reads as diligence. So `tools` is now adjudicated against a
**closed vocabulary** — `BUILTIN_TOOLS`, enumerated off the `init` frame of a live
stream-json run rather than copied from documentation, since the CLI is the only
authority on what tools it has. `default`, a non-list, an unenumerated name and an
`mcp__` name are each refused **by name** with a row apiece, scoped forms like
`Bash(git *)` are kept because they are strictly narrower, and the vocabulary lives on
the harness so the loader has no second opinion about what a tool name is — a workflow
naming a harness that publishes no `validate_tools` is refused rather than passed
through (F4). Both flags are
passed: `--tools` selects what exists, `--allowedTools` selects what may run without a
prompt, and a headless run has nobody to prompt. `permission_denials` in the result frame
now **fails the phase**: a phase reaching outside its declared tools is the pre-hoc
analogue of a breach, and this spine does not treat a breach as noise. That adjudication
was lifted out of `run()` into `ClaudeCodeHarness.adjudicate()` so it can be exercised
without spending money — a verdict that can only be checked by invoking a model is a
verdict nobody checks.

## What is deliberately not here (Spec A § 12)

No dashboard, no scheduler, no queue, no sandbox, no model pinning in workflow files,
no cost optimizer, no auto-merge. Tier-0 is a terminal surface reading receipts.
UI does not advance a tier before receipts exist to render.

## Custody

Receipts schema custody is star-lord's (strategy § 8). A schema change gets a
MIGRATION note before it ships, because gate consumers and any future Tier-2 surface
read these tables. `schema_meta.schema_version` exists so a consumer can refuse an
unknown version rather than guess at it.

29. **Detecting a write and refusing it are two different claims.** A row that asserts
   on `fingerprint().content` has tested the first one only. J4 added control surfaces
   for a worktree's real gitdir and keyed them `.git\t<common>/…`; `_matches` protects
   by literal `.git/` prefix, so they were protected in no repo at all — while the
   docstring said they classified "as the protected surface it is." Both rows checking
   them compared fingerprint content, which moves whether or not the key is protected,
   so both stayed green. Found by reading `_matches` to check the sentence, by no test.
   Every "…and therefore it is protected / blocked / refused" claim owes an assertion
   on `classify`, under a permissive `writes` — because a protection that only holds
   when the allowlist would have refused anyway is not doing the work it claims.

30. **A row that goes red for the wrong reason has told you nothing.** Both J3 rows came
   up red on first run — for a missing import in the test module, which made the harness
   raise on attempt 1 so the retry path under test never executed. Green needs a
   mutation to mean anything; red needs to be read, because "the row failed" and "the
   row failed for its own reason" are the same colour on the terminal.

31. **A version stamp its own writer overwrites can never disagree, so it can never
   refuse.** `receipts.py` stamped `schema_version` from the code's constant,
   unconditionally, after `CREATE TABLE IF NOT EXISTS` — which cannot add a column. So
   opening a v1 DB with v2 code kept the v1 table shape and relabelled it "2", while
   the module docstring said the stamp existed "so a Tier-2 consumer can refuse an
   unknown version rather than guess at it." The refusal it promised was structurally
   unreachable. Generalises past schemas: any field whose purpose is to let a later
   reader detect a mismatch must be READ before it is written, or it is decoration.
   Same shape as `--allowedTools` (J1) — a fence whose falsifying condition cannot
   arise — but on the mechanism whose whole job was detecting drift.

32. **Migrating evidence is additive or it is not unattended.** `ADD COLUMN` cannot
   destroy a row. Anything that rewrites or drops is a Matt-authorized operation
   (ADR-006), not something a constructor does on open. And a refusal must not restamp:
   relabelling the DB on the way out of an error destroys the fact that caused the
   error, so the retry succeeds and is wrong. Pre-existing rows are never backfilled —
   a value nobody measured must read as unmeasured.

33. **A signature whose inputs the subject controls is not a signature.** `size+mtime`
   is the right cost for thousands of dirty paths and the wrong measurement for the
   handful of surfaces an adversary aims at, because matching a size is choosing the
   payload's length and restoring an mtime is `touch -t` — both free to any phase with
   `Bash`, which J1 measured the agentic lane as granting unrestricted. Control
   surfaces are content-hashed (H7). Where a hash is unaffordable, say so in the value
   rather than degrading quietly: `oversize:{n}:…` is a measurement, a bare stat sig
   presented as a hash is not.

34. **Hash what makes it DANGEROUS, not just what makes it DIFFERENT.** `chmod +x` on
   an inert `pre-commit` writes zero bytes and arms the hook. Content, size and mtime
   are all unchanged; only the mode moved, and git runs the hooks that are executable.
   H7-b — dropping mode from the signature — survived a full-suite mutation run. The
   mode was in the code; nothing would have noticed its removal, which is the same
   thing as it not being there. Ask what the file's *effect* depends on, then measure
   that.

35. **The instrument gets audited too.** Three rounds running, the defect was in the
   measuring apparatus rather than the subject: a mutation harness with a red baseline
   (round 14), a flat glob that made the suite's subject "whatever pytest reached"
   (F7/F2), and a killer-name parser that printed every name as the literal string
   `FAILED` — counts usable, attribution destroyed, which is the whole point of
   recording a first killer. Evidence that cannot name itself is not evidence.

36. **Record what you could NOT measure, next to what you could.** A receipt that
   reports the fence and omits the ground it stands on has recorded the less
   important half. Every containment verdict this factory issues was issued
   underneath a host `permissions.defaultMode` the factory does not set (H1's root
   cause, `bypassPermissions` on this host) and inside a bounded set of fingerprinted
   trees. Both facts now live on the session row (H6, schema v3). Neither is a defect
   in the wall; both are limits on what the wall's silence proves.

37. **A caveat that only prints on the red path is a caveat nobody reads.** Green is
   where the over-claim happens — "0 breaches" invites "nothing was written" — so the
   measurement-limit block renders on EVERY run report, not inside `if breaches:`. The
   reader who most needs the boundary is the one who has stopped asking for it.

38. **Never fill an unstated setting with the system's own default.** Claude Code
   falls back to `default` when `permissions.defaultMode` is unstated, so recording
   `"default"` would be right on every host that never changed it and unfalsifiable on
   every host that did. That is `usage.py`'s zero-filled token, moved from cost to
   containment. NULL, with a source sentence saying which kind of nothing it was.

39. **A vocabulary is closed against names it does not know; it is not closed against
   names whose GRANT IS NOT THEIR REACH.** `BUILTIN_TOOLS` was probed off a live init
   frame, so it answers "does this CLI have that tool?" correctly — and that is a
   membership question, not a containment question. A phase declaring `tools: ["Task"]`
   passed the fence, was granted exactly what it declared, and spawned a child holding
   `Bash`, `Edit` and `Write` (measured 2026-08-11, no denial, no error). The fence was
   satisfied and bypassed in one call. So `UNFENCEABLE_TOOLS` refuses those names at
   load and records WHY next to each — refused, not deleted, because deleting them
   would make the loader say "this CLI does not have that", which is false.

40. **Assert on the SECTION, not the document.** H6's certifying row checked three
   substrings against the whole report, and the repo path it looked for was also
   printed by the unrelated `**Root:**` line — so the entire trees block could be
   deleted with the suite green. Rule 28 with a longer fuse: the proxy was not a
   different measurement, it was the same string arriving from somewhere else. Slice
   the block the claim lives in, then assert inside it.

41. **A fixture with one element cannot tell a list from its first element.** Every H6
   row declared exactly one repo, so `measured_trees=wf.repos[:1]` survived the whole
   mutation pass. A run under-reporting its own scope is the worst kind of receipt: the
   second tree is fingerprinted, enforced, and invisible — measured but not admitted,
   which leaves the reader no cue to ask. Any row about a COLLECTION gets at least two.

42. **A caveat must say which WAY the unmeasured thing can move.** Naming the five
   permission layers this factory does not resolve was necessary and not sufficient: a
   reader still assumes the recorded mode is roughly the answer, and it is wrong in the
   direction that matters. An unresolved layer can be MORE permissive, so a
   restrictive-looking mode is not evidence of a restricted run. Direction, or it reads
   as a footnote instead of a limit.

43. **A synthetic marker is not part of the path.** When git's own pointer chain cannot
   be read, the fingerprint mints `.git\t<gitdir pointer unreadable: …>` so that
   unreadable never renders as unchanged. Five such keys put the tab BEFORE the slash,
   so they began `.git` and not `.git/` — and `PROTECTED_EVERY_REPO`, `_read_only_hit`
   and the rollback's `git_internal` guard all read the marker as path. The sibling key
   `.git/\t<common>` put the tab after and was fine, so the class was half-covered by
   an accident of string order. One normalisation (`marker_path`), shared by every
   predicate that reasons about the key.

44. **A row parametrised over the thing it guards cannot notice a deletion from it.**
   Every J7 row derived its names from `UNFENCEABLE_TOOLS`, so removing `Task` — the one
   name that was actually MEASURED — loses a parametrised case rather than failing one,
   and the suite stays green while the finding walks back out. Anything established by
   measurement gets one row that hardcodes it and cites the frames. Derivation keeps the
   lists from drifting; a literal keeps the finding from evaporating. Both, not either.

45. **"Inert" is a claim like any other — it needs its own assertion, or the table is
   reading a silence as a receipt.** jack-ryan's JR-5 mutation moved a tab across a slash
   and survived pre-fix, because nothing in the suite could tell protected keying from
   unprotected. Re-run post-fix it survived again, and round 17's table called that the
   fix working: after one shared normalisation the two spellings name the same path, so
   no answer changes. But the one row that could have disagreed had been widened to
   `.rstrip("/")` in the same commit (rule 46), so post-fix survival was a consequence of
   the relaxation, not evidence for the equivalence. Same word, `SURVIVED`, two different
   facts, and the receipt claimed the second. The equivalence is now asserted directly —
   both spellings minted, same verdict AND same reason (`test_JR9_…`) — and only with that
   row present does "inert" mean anything. A survivor whose inertness IS the claim must be
   labelled in the table AND backed by a row that fails if the inertness stops holding.
   *Round 19 addendum:* the row this rule first cited did not satisfy it. `classify`
   short-circuits at `_read_only_hit`, so with `read_only_trees=[]` the row only ever
   compared reasons from the arm that already normalised before JR-5 — the arm JR-5 had
   to FIX was never entered, and the row stayed green under the very mutation it was
   cited against. Check that the cited row enters the predicate the claim is about;
   "it asserts the right sentence" and "it reaches the right code" are two claims
   (rule 29, one level up).

46. **Do not assert the producer's string order when the fix exists to stop it
   mattering.** The premise row for rule 43 checked `marker_path(key) == ".git"`, which
   fails on `.git/` — so it would have reported a provably equivalent rewrite as a
   regression, and pinned in place the coupling the normalisation removes. Three of the
   four defects the wall opens with were held there by a passing test asserting the
   reduced behaviour was the requirement. Compare on the claim (`.rstrip("/")`), not on
   the spelling.

47. **To test whether a finding is protected, DELETE it — do not rename it. A rename is
   a strictly weaker mutation, and it is the one that lies.** Round 18 "verified" that
   removing `ToolSearch` from `UNFENCEABLE_TOOLS` was caught, by renaming the key to
   `ToolSearch_DISABLED`. A row computing `set(UNFENCEABLE_TOOLS) - known` fires on the
   orphan the rename leaves behind, so the table recorded KILLED. jack-ryan ran the
   DELETION: 594 passed, no failures, and `validate_tools(["ToolSearch"])` returns
   `['ToolSearch']`. The named killer could not possibly have fired — removing an element
   can only SHRINK a set difference — so the attribution was not merely unverified, it was
   unverifiable. Deletion is the mutation rule 44 is about; a rename tests the drift guard
   and reports it as the evaporation guard. Under deletion, SIX of nine refused names left
   the whole suite green. Fix (both halves, per rule 44): the parametrised row keeps the
   lists from drifting, and a hardcoded `REFUSED_ROSTER` literal fails on any removal.
   *Round 20 addendum, corrected and widened at round 21 — WHICH collections need the
   literal, because the answer is not "all of them" and a rule that said so would be
   noise.* The FIRST axis is whether a member is **behaviour** or a **record**.
   `GIT_NESTED_GITDIRS`, `GIT_CONTROL_PATHS`, `PROTECTED_EVERY_REPO` and
   `PROTECTED_ALWAYS` are all KILLED by member-deletion: removing a member stops a real
   key being minted and a scenario row notices, so they need no pin. *Corrected at round
   23 (JR-25).* The figures this addendum first published were `7 / 11 / 3` against three
   collections with **no member named beside any of them**, and the `11` did not belong to
   the collection it was printed under — it is `GIT_NESTED_GITDIRS`' `"modules/"`, and
   `GIT_CONTROL_PATHS` had never been measured at all. A figure is a claim about ONE
   member (rule 50), so each is now stated as one:

   | collection | member deleted | result |
   |---|---|---|
   | `GIT_NESTED_GITDIRS` | `"worktrees/"` | `7 failed` |
   | `GIT_NESTED_GITDIRS` | `"modules/"` | `11 failed` |
   | `GIT_CONTROL_PATHS` | `"config.worktree"` | `3 failed` |
   | `GIT_CONTROL_PATHS` | `"hooks/"` | `21 failed` |
   | `PROTECTED_EVERY_REPO` | `".claude/"` | `3 failed` |
   | `PROTECTED_ALWAYS` | `"canonical/"` | `2 failed` |
   | `PROTECTED_ALWAYS` | `"agentic_orchestration/factory/"` | `2 failed` |

   The spread within one collection is the point: `GIT_CONTROL_PATHS` gives `3` or `21`
   depending on the member, so "`GIT_CONTROL_PATHS` is killed at `11 failed`" was not a
   number that was slightly wrong, it was a number that could not have been right.
   `REASONED_ADMISSIONS`
   is a record — deleting `Skill` from it changes no behaviour at all, because `Skill` was
   never refused — and it SURVIVED at **603 passed, the baseline count unmoved**, which is
   worse than the JR-13 case where the count at least dropped to 602 and a reader
   comparing totals had one thread to pull. What evaporates is the sentence that
   adjudicated the admission. *(The `21 failed / 12 errors` figure this addendum first
   published for `GIT_NESTED_GITDIRS` was not a measurement of that deletion at all — see
   rule 48.)*
   The SECOND axis is **which direction is fail-open**, and round 20 did not have it
   because every mutation it ran went the same way. A **protection** list fails open when
   a member is DELETED. An **exemption** list fails open when a member is ADDED — and no
   scenario row can catch that, because the row would have to exercise a path nobody has
   exempted yet, so it could not have been written in advance. Deletion from an exemption
   is fail-CLOSED: the run gets noisier, not blinder. So rule 44's "delete it" measures
   the SAFE direction on half the table and the reading reads as reassurance. Measured
   (jack-ryan, round 21): `FACTORY_RUNTIME_PATHS` member-deletion SURVIVES, and additions
   to `FACTORY_RUNTIME_PATHS` and to `STRUCTURE_SKIP_DIRS` both SURVIVE. Crossed, exactly
   one cell of four is covered by rows — and the direction is a property of the CALL SITE,
   not of the collection: `REFUSAL_GUARDS` and `GUARDS_OWING_FACTS` are two frozensets of
   guard names declared eight lines apart in one file, failing open in OPPOSITE
   directions, because one is spent as `assert guard in …` and the other as
   `if guard in …:`. A THIRD kind needs no pin at all — **labelling** lists like
   `_CO_TENANCY_SUFFIXES` and `_FAILURE_MARKERS`, whose membership changes the DIAGNOSIS
   and not the VERDICT — and naming it is what stops this collapsing into "pin
   everything". The derivation over all **fifteen** public vocabularies, the seven pins
   and the eight cover-claims each naming its row, live in `tests/test_vocabularies.py`,
   which recomputes the denominator from source rather than trusting the number (rule 49).
   Rule 47 was written about one dict and applied to one dict; a rule's own scope is a
   claim like any other.

48. **The measuring instrument gets the same reading you would give the code (rule 35,
   sharpened by two failures in one round).** Round 19's own mutation harness shipped two
   defects of the shape it was hunting. Its "delete this dict entry" helper searched for
   the key name **unscoped**, and `Agent` lives in two dicts — so it silently mutated the
   wrong one and reported SURVIVED. Its "find where this entry ends" search was
   **unbounded**, so for the LAST entry in a dict it ran past the closing brace into the
   next dict and produced a syntax error, which the harness classified as SURVIVED because
   no test had FAILED. Both are predicates answering an adjacent question with a
   safe-looking wrong answer, inside the tool built to find predicates that do that. A
   harness that cannot distinguish "no row failed" from "nothing ran" is not measuring.
   *Round 20 addendum, from the reviewer's instrument rather than mine:* jack-ryan's
   probes imported `factory.permissions` while their own harness had a mutation applied
   to the working tree, read the mutated module, and produced a BLOCK-shaped finding
   against a green suite — caught by `inspect.getsource` showing their own edit. Separately
   they killed a harness by its shell PID, the Python child survived, two harnesses
   mutated one tree, and the second restored the tree *to* the first's mutation. The
   generalisation is a precondition, not a warning: **a measurement must assert the tree
   was clean before it ran**, because "no test failed" is worth nothing if you cannot say
   what the tree was. Both round-20 harnesses refuse to report without it, and both also
   verify the intended change is observable in the LOADED object — a mutation that did
   not land reads exactly like a mutation nothing caught.
   *Second round-20 addendum, mine — RIGHT ABOUT THE FIX, WRONG ABOUT THE DEFECT, and the
   correction is the more valuable half (jack-ryan, round 21).* Those same harnesses
   collected results by filtering pytest output for lines beginning `FAILED`. One control
   mutation returned `21 failed, 571 passed, **12 errors**`, and the harness printed nine
   names and no indication that three parametrised rows had **errored at fixture level and
   never executed at all**. An ERROR is not a FAILURE: a failing row ran and disagreed, an
   erroring row never ran and therefore certified nothing. A harness that greps for one of
   them silently reports the other as absent — which is this rule's own subject, "no test
   failed" versus "nothing ran", reappearing in the collector instead of the mutator.
   **Collect `-rEf`, report both, and print the raw summary line rather than a count
   derived from the lines you chose to match.** That fix stands. The DIAGNOSIS attached to
   it did not. I published that reading as a measurement of `"worktrees/"` deleted from
   `GIT_NESTED_GITDIRS`, could not close it against jack-ryan's `7 failed`, and named the
   collector as the suspect. The real cause is one line up: `GIT_NESTED_GITDIRS =
   ("worktrees/", "modules/")` is a single-line 2-tuple, and deleting its first element
   TEXTUALLY leaves `("modules/")` — not a 1-tuple, the bare string `"modules/"`. The run
   measured a container that had changed TYPE, and twelve fixture-level errors is exactly
   what that produces. Worse, the harness's own "did the mutation land?" guard asked
   `member not in container`, and `in` on a `str` is a **substring** test, so it certified
   the landing of a mutation nobody had performed — the series' defect shape inside the
   guard written to prevent it, one rule after the rule about that. **Verify a mutation by
   TYPE and LENGTH, or on the SOURCE text; never by membership.** Membership cannot tell a
   shorter tuple from a string, which is also why the pins in `tests/test_vocabularies.py`
   are equalities and carry an explicit `type(observed) is type(expected)` leg.

49. **Establish the denominator before reasoning over the set.** Three rounds argued about
   "the ten marker producers" and the count was never checked. There is an eleventh
   pathway (`_git_control_entries:826`), which mints nothing itself — it passes a
   marker-bearing string as the *prefix* into `_gitdir_control_entries`, so on a real
   linked worktree **17 keys sit under that prefix and 16 of them are marker-bearing**
   without any of the ten sites firing (jack-ryan reported 16; the extra key is not
   marker-bearing and does not move the argument, and the difference is recorded because
   an uncounted number is how this finding came to exist). They
   collapse to `.git/` rather than to the two-component paths the rounds were arguing
   about. It is inert, and inert for a reason that holds, so nothing was unprotected. The
   defect is the same one this series keeps finding, moved up a level: a set reasoned over
   confidently whose membership was never established. An enumeration is a measurement.

50. **When you re-run a reviewer's mutation, run THEIR mutation. A mutation of the same
   KIND is not the same mutation, and no guard a harness can carry will tell you.** Round
   21's JR-20 receipt reported jack-ryan's measured survivor as killed. They had added
   `"reincarnated-engine/"` to `FACTORY_RUNTIME_PATHS`; the re-run added
   `"agentic_orchestration/"`, which shadows the factory's own source tree and so trips two
   rows in `test_permissions.py` that have nothing to do with the pin under test. The
   harness was clean by every check it had — precondition tree clean, needle unique,
   substitution verified against the whole source text, tree restored, postcondition clean
   — because **not one of those guards is about which member you chose.** A harness
   verifies that the edit landed; it cannot verify that it was the right edit. The claim
   the receipt would have carried was false, and false in the flattering direction. This is
   the series' defect shape in its third location: the CODE (rounds 18–21), the INSTRUMENT
   (rules 44, 48), and now the RECEIPT. The only tell available in practice was a **count
   that did not match its siblings** — eight mutations at `2 failed` and one at `4` — which
   is a tell only because rule 48's `-rEf` correction makes the receipt print raw per-row
   lines. Re-run with the reviewer's exact members: `KILLED, 2 failed, 608 passed`, figures
   back in line. Corollary: *a reviewer's number is a claim about their mutation, not about
   the collection.* "SURVIVED, 604" was correct and remains correct; it was simply never a
   claim about a mutation nobody had run.

   **50a. Re-running their mutation is half of it. Then re-run it with your own new row
   neutralised** (jack-ryan, JR-26(a)) — only the second run separates *"my new row caught
   it"* from *"something already had."* A kill against a fixed tree with your rows in place
   is consistent with your rows doing nothing. In practice, take the neutralised run
   **first**: measure the site before you write the row, and attribution falls out as a
   by-product instead of costing a second full pass. Worked example at JR-23 — R24-A killed
   `diff_fingerprints`' `marker_path` call *before* any JR-23 row existed and SURVIVED at
   617, so every kill R25-A later recorded is attributable to the new rows and to nothing
   already standing. And the corollary is not academic: the JR-23 fix added a refusal guard
   two lines from jack-ryan's R24-C target, which is exactly the shape that decouples a
   reviewer's ledger row from the thing that used to kill it.

   **50b. Reconcile `failed + passed` against `collected`, every time.** They come apart for
   two unrelated reasons and only the arithmetic tells you to look: an assert that did not
   execute (rule 44), or **a mutation that deleted a parametrised case**. jack-ryan flagged
   round 21's `5 failed, 602 passed` = 607 against 608 collected as rule 44's signature
   (JR-26(c)); it is the second kind. `test_workflow.py` parametrises over
   `sorted(UNFENCEABLE_TOOLS)`, and the deletion mutation removed the `"Task"` entry, so the
   row did not fail — it was never collected. That is a **deletion mutation partially
   disarming its own measurement**: rule 47 says the rename is the weaker mutation and the
   one that lies, and here the deletion has its own opposite way of lying. It is caught, by
   the one row written not to derive its expectation from the code under test
   (`test_J7_the_MEASURED_name_is_refused_by_LITERAL_not_by_derivation`) — which is the
   general defence, not a special case.
