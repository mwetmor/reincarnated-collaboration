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
  tests/           428 tests, all green (~110 s: the reach audit runs the suite twice)
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
`gates` is a load error); this one failed open, and was proven only to RESTRICT when
declared, never to REFUSE when absent (C3). An agentic phase with no `tools` allowlist is
now refused at **both** entry points — the loader and the adapter — because a guard
present in only one of two entry points is a guard with a route around it. Both flags are
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
