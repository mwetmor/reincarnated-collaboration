# Finding — 2026-08-10 — factory-spine-v1 (Gate 2, RE-REVIEW)

**Reviewer:** jack-ryan
**Severity:** **UNBLOCK — CONDITIONAL** (see § Verdict) · one new BLOCK-class defect (G1)
**Target:** `agentic_orchestration/factory/` @ `942372ef`
**Developer:** star-lord (builder, ruling D4)
**Supersedes:** `2026-08-10-factory-spine-gate-2.md` (BLOCK agentic · APPROVE mechanical)
**Remediation note reviewed:** `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md`
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate / evidence), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** 8 (schema validation at boundaries), 9 (assertions from spec sources), 11 (empirical inspection over assumption), 12 (semantic-shifting fixes need explicit framing)

---

## Verdict

**The BLOCK is LIFTED. The agentic lane unblocks, conditionally.**

- **F1 — CLOSED.** Proven live, four independent ways, against the real engine tree.
- **F2 — CLOSED for the trigger I named.** A neighbouring trigger in the same
  family is still open: **G1**, below, which I proved live.
- **D-3, D-4, D-6, D-7 — genuinely closed.** Each verified behaviourally, not by
  reading the note. All four branches of D-4 and all three of D-7 exercised.

**The condition.** The agentic lane is authorized for workflows that declare
**whole git repositories** in both `repos:` and `read_only_trees:` — the shape the
shipped workflow already uses and the shape I re-proved sound today. **G1 is a
BLOCK on any workflow that names a subdirectory in either list**, and the fix is a
loader refusal small enough that it should land before the first agentic workflow
is authored, because authoring is where the hazard enters.

This is not the same split as last time. Last time the mechanical lane was proven
and the agentic lane was not. This time the containment layer is sound for the
configuration in use; what remains is a config shape the loader currently blesses
and cannot enforce.

---

## What I verified independently (every claim reproduced, none accepted)

| Claim | Result |
|---|---|
| 164 tests green | **REPRODUCED** — `164 passed in 3.47s` |
| `./factory run` PASS in ~1m26s | **REPRODUCED** — run `…T235710Z-82624d`, 3 phases, 14 verdicts, 86 s wall |
| `DETERMINISM: EXACT — 14 verdicts identical` | **REPRODUCED on a quiet tree** — 14 vs 14, byte-identical verdict tuples, recomputed from `gate_results` rather than trusting the CLI's own summary |
| Gate env suppresses bytecode writes | **CONFIRMED** — zero `__pycache__` / `.pytest_cache` in the engine tree newer than 18:00 today |
| Exemption is the named six, root repo only, recorded | **CONFIRMED** — live fingerprint records exactly `['…/.pytest_cache/', '…/__pycache__/', '…/receipts.db', '…/sessions/']` (the two absent are `-wal`/`-shm`, which did not exist at snapshot time) |
| `containment_coarse` emitted per phase | **CONFIRMED** — 3 receipts on a 3-phase run |

### F1 — closed, and closed against the thing that actually motivated it

I re-ran my original probe verbatim. Same workflow shape, opposite result:

```
-- phase 1/1: plant_ignored_write_in_readonly_tree [mechanical]
   PERMISSIONS BREACH during gate execution — aborting the run
     jr_probe_f1.log (created) — write inside a read-only tree (reincarnated-engine)
     rollback: jr_probe_f1.log -> deleted
ABORTED: permissions breach during gate execution: 1 path(s) outside the allowlist
=== DID THE FILE SURVIVE? ===  GONE (rolled back)
```

Three harder variants, all caught:

1. **A write inside a pre-existing collapsed ignored directory** — the shape
   `seasons/` and `cache/` actually report in. Detected as
   `('cache/', 'modified')` → `write inside a read-only tree`.
2. **A same-content, new-mtime rewrite of an existing ignored file** — the weakest
   possible edit signal. Detected.
3. **Measurement tier of the assets that produced the BLOCK.** I fingerprinted all
   three real repos. **The engine tree has ZERO coarse regions** (2,907 entries,
   all EXACT). The only coarse regions on this host are godot's `.godot/` and
   `Assets/Synty/`. `seasons/` (3.3 GB) and `telemetry.db` (450 MB) are
   **exactly** measured.

### F2 — closed for the named trigger, both halves, live

```
workflow rejected at load: declared repo /private/tmp/jr_f2_tree is not a git worktree.
```

```
CONTAINMENT FAILURE during gate execution — after fingerprint of /private/tmp/jr_f2_tree
is unusable (not a git worktree) — containment cannot be proved for this tree, so the run stops
ABORTED: containment failure during gate execution
```

Both discharge conditions from my action list are met: a workflow naming a non-git
repo refuses to start, and a mid-run git failure aborts rather than greening.

### D-3 / D-4 / D-6 / D-7 — closed, verified behaviourally

- **D-3.** `verdict_consistent` at position 2 of 3 → `REJECTED` at LOAD with the
  position named. Last → loads.
- **D-4.** All four branches exercised against `_dollars_line`: registered source →
  subscription caveat; **unregistered** source → `source \`x\` (no gloss registered)`;
  **empty** sources with a non-null figure → `**provenance unrecorded**; this figure
  cannot be read as money spent`; two sources → both labels travel. The renderer no
  longer supplies a meaning the receipt did not record.
- **D-6.** `harness: codex` → `REJECTED` at LOAD: *"runs on the 'codex' lane, which
  is not open — blocked on T16 — Matt action: ChatGPT subscription + Codex CLI
  install + login."* Names T16 as required.
- **D-7.** PASS → notes pass through unlabelled. FAILED → prefixed with phase name,
  status, and the lead-not-result caveat, notes still present (label, not filter).
  Whitespace-only notes stay empty. Wired into `_build_prompt` via `run()`.

---

## G1 — BLOCK-class — a `repos:` entry naming a SUBDIRECTORY of a git repo fails open, and the rollback receipt lies

**Files:** `workflow.py:248-258` (`_is_git_worktree`) · `permissions.py:243-294` ·
`permissions.py:393-490` (`rollback`)
**Pinned by:** `tests/test_workflow.py::test_a_read_only_tree_nested_inside_a_declared_repo_is_accepted`

`_is_git_worktree` runs `git rev-parse --show-toplevel` and checks only the return
code. That succeeds from **any** subdirectory of a repo. Its own docstring asserts
the opposite:

> *"Not `.git` existence — a worktree or submodule keeps a `.git` file, and a
> subdirectory of a repo has neither."*

The intent is right; the implementation does not achieve it. Measured:

```
_is_git_worktree(engine/src/reincarnated/telemetry) = True
LOAD accepts it as a repo: ACCEPTED
fingerprint usable = True   entries = 2907
sample entries = ['.claude/', 'data/emission_registry.db-shm', 'data/emission_registry.db-wal']
do those resolve under the declared root? [('.claude/', False), (..., False), (..., False)]
signatures for them: ['dir:0:e3b0c44298fc1c14', '', '']
```

`git status` returns **repo-root-relative** paths; `root` is the subdirectory;
every `root / rel` join therefore misses. Consequences, in order of severity:

1. **`usable` is `True`, so the new `ContainmentError` guard never fires.** This is
   F2's exact failure mode wearing the badge the F2 fix installed.
2. **Content changes inside the declared tree are invisible** — every signature is
   `''` or the empty-directory hash, identically before and after.
3. **The rollback records an action it did not perform.** Live probe: a gate command
   wrote into a subdirectory declared as both a repo and a read-only tree.

```
PERMISSIONS BREACH during gate execution — aborting the run
  src/reincarnated/telemetry/jr_probe_g1.txt (created) — write inside a read-only tree (telemetry)
  rollback: src/reincarnated/telemetry/jr_probe_g1.txt -> deleted
=== DID THE FILE SURVIVE? ===
-rw-r--r--@ 1 admin staff 7 Aug 10 19:58 …/src/reincarnated/telemetry/jr_probe_g1.txt
```

The durable receipt says the same thing:

```
rollback :: src/reincarnated/telemetry/jr_probe_g1.txt: deleted — created by the phase
```

`rollback()` joined the wrong root, found nothing at the target, skipped both the
quarantine and the delete branch, and appended a `deleted` action anyway. **The
bytes survived; I removed them by hand.** A receipt that records a remediation
that did not occur is worse than no receipt — it is the "green phase over a broken
world" pattern relocated onto the abort path. Discipline #8: this boundary has no
validation.

**Reachability is not theoretical.** The F2 fix's own error message routes an
author here: *"Declare it in `repos` as well."* An author who wants a narrower
read-only tree — which is the fallback § 4 of the remediation note recommends —
follows that instruction and lands exactly on this.

**Path forward:** compare `--show-toplevel` output to the declared path and refuse
a mismatch, with a message naming the enclosing repo. One condition, one test:
*a subdirectory of a git repo is not a repo.* That closes G1 and G2 together.

---

## G2 — WARN — `read_only_trees` at sub-repo granularity is accepted at LOAD and unenforced at CLASSIFY

**File:** `permissions.py:361-390` (`classify`) · `workflow.py:283-290`

`classify()` decides read-only by comparing `change.root` — which is always a
**repo root** — against the read-only paths. A read-only tree that is a
*subdirectory* of a declared repo can never match:

```
1. LOAD accepts read_only_trees=[engine/seasons] with repos=[meta, engine]:  ACCEPTED
2. read_only=[engine/seasons]:  allowed=['seasons/anything.json']   breaches=[]
3. read_only=[engine]        :  allowed=[]  breaches=['write inside a read-only tree']
```

The new load rule *certifies* a read-only claim the classifier does not enforce.
And the new test that pins it —
`test_a_read_only_tree_nested_inside_a_declared_repo_is_accepted`, docstring
*"a subdirectory of a fingerprinted repo is fingerprinted with it"* — asserts
acceptance without ever checking that acceptance means anything. That is the same
construction I flagged under **Discipline #12** last round at
`test_permissions.py:220`: a test encoding the reduced scope as the requirement.
Worth naming, because it is the second instance of the pattern in this module.

**Consequence for § 4:** the fourth option star-lord names but did not take —
*"declare a narrower read-only tree"* — is **currently unsafe**. Do not take it
until G1/G2 close.

---

## G3 — WARN — the read-only trees are not write-quiet, and the factory cannot make them so

**File:** `gates/core.py:252-272` (`_gate_env`) · `harness/claude_code.py:79-86`

**star-lord's reasoning on `PYTHONDONTWRITEBYTECODE` is correct and I endorse it.**
Exempting `__pycache__` would have been the F1 defect one layer down: a category
exemption bought to make a red go away. Suppressing the write is right.

The suppression is incomplete in a way that matters for the lane being opened.

**(a) It reaches gate subprocesses only.** `_gate_env()` is passed to
`_exec_verdict`'s `subprocess.run`. The **harness** subprocess —
`claude_code.py:79`, the one that runs the agent — takes no `env=` at all and
inherits the ambient environment. Any python the agent runs writes `__pycache__`
where it runs: inside the read-only engine tree (breach), or under
`agentic_orchestration/factory/` (a `PROTECTED_ALWAYS` breach). Nested caches such
as `agentic_orchestration/factory/gates/__pycache__/` are not in the six-path
exemption either.

**(b) A whole class of writers is outside the factory's reach entirely.** Measured
on the real tree:

```
src/reincarnated/telemetry/telemetry.db: journal_mode=wal
  sidecars_created=['…/telemetry.db-shm', '…/telemetry.db-wal']
during connection:      [db-shm, db-wal]
after close, same process: [db-shm, db-wal]
after process exit:        db-shm  db-wal      <-- PERSIST
```

A **read-only** SQLite open on the engine's production telemetry DB creates two
files inside the declared read-only tree and they survive process exit, because a
read-only connection cannot checkpoint. Under post-F1 containment those are
measured, classified `write inside a read-only tree`, and abort the run — and
`rollback` will `unlink` a `-wal`, which is a destructive act if any process holds
that database open.

**This is not hypothetical. It happened during this review, and it flipped the
acceptance claim.** An out-of-band read-only query from my own session — a process
the factory did not launch — aborted *both* determinism laps of the shipped
workflow:

```
PERMISSIONS BREACH during phase execution — aborting the run
  src/reincarnated/telemetry/telemetry.db-shm (modified) — write inside a read-only tree
  src/reincarnated/telemetry/telemetry.db-wal (modified) — write inside a read-only tree
DETERMINISM: DIFFERS — the instrument is not asserting the same thing twice
```

With the tree quiet, the re-run reproduced `PASS` and 14 identical verdicts. So the
acceptance evidence is real — **and it is conditional on nothing else on this host
touching an engine database during the run.** On a Mac-resident 10-agent team that
is not a safe standing assumption, and Spec A § 11 item 2 (determinism) is
currently a property of host quiescence as much as of the instrument.

This is fail-**closed**, not fail-open, which is why it is WARN and not BLOCK. But
it is the most likely way the founding agentic run dies, and it will look like a
containment defect when it is a co-tenancy problem.

**Path forward (developer's choice, all three are legitimate):** pass `_gate_env()`
to the harness subprocess as well; and either (i) treat a known-transient sidecar
set as an explicitly *named* class — the same discipline as `FACTORY_RUNTIME_PATHS`,
never a category — or (ii) declare the read-only claim as *"no write the factory
made"* rather than *"no write occurred"*, and say so in the receipt. What must not
happen is a silent category exemption for `*-wal`/`*-shm`.

---

## G4 — INFO — the coarse caveat is emitted from the `before` snapshot only

`runner.py:227` is the sole call site of `_note_coarse`, and it passes `before`
with `when="phase start"`. The post-execution and post-gate snapshots' measurement
strength is never declared. Confirmed in receipts: 3 of 3 events read
`phase start:`. If a region crosses the 50 k threshold *during* a phase, the
receipt describes the strength of a claim about the pre-state while the verdict is
about the post-state. Cheap fix; call it on `after` and `post_gate` too.

## G5 — INFO — breach granularity for collapsed ignored directories

A write inside a pre-existing ignored directory reports the **directory** as the
breach (`('cache/', 'modified')`). Detection is correct and the run aborts —
that is the load-bearing half. But rollback then declines with *"path was already
dirty at phase start; restoring would destroy pre-existing uncommitted work"*,
which is the safe behaviour and a **misleading reason**: what remains on disk is a
new file the phase created, not pre-existing dirt. Quarantine will also `copytree`
up to 64 MB (`cache/` is 56 MB) or `rglob` a 3.3 GB tree to build a manifest.
Worth one sentence in the receipt distinguishing *"not rolled back"* from *"the
containing directory was not restored; the write remains."*

## G6 — INFO — `os.walk(..., onerror=lambda _: None)` swallows unreadable subtrees

Both `_coarse_signature` and `_exact_signature` silently skip a subtree they cannot
read, identically before and after — so an unreadable region reads as unchanged.
This is F2's family in miniature, and it sits under a module docstring that now
claims *"nothing is ever assumed clean."* Record the skipped paths on the
fingerprint, as `coarse` and `exempted` already are.

## G7 — INFO — dead parameter, live cost

`_signature(root, rel, untracked_files)` never reads `untracked_files`, but
`fingerprint()` spends a `git ls-files --others --exclude-standard` subprocess per
tree per snapshot to compute it — 27 calls on a 3-phase, 3-repo run. Drop both.

---

## Direct answers to the three questions in § 4

**1. Is the COARSE tier acceptable at Gate-2, or does it reopen F1 in a quieter
register?** **Acceptable. It does not reopen F1** — and the reason is measurable,
not rhetorical. I fingerprinted all three real repos: the engine tree has **zero**
coarse regions. `seasons/` and `telemetry.db`, the two assets whose exposure earned
the BLOCK, are EXACT-measured. The only coarse regions on this host are godot's
`.godot/` (regenerable build cache) and `Assets/Synty/` (vendored third-party
assets nothing in this project authors). F1 was *"measured nothing and reported
clean."* This is *"measured less, said so, on data that is regenerable or
vendored."* Those are different failures, and **Discipline #12 is satisfied
because the semantic shift is framed explicitly** — in the constant's docstring, in
the README, in a per-phase receipt, and in a falsification test that reds if the
caveat ever becomes too strong. A declared-weaker claim is acceptable when all four
of {declared, labelled, pinned by falsification, residual risk scoped} hold. All
four hold. Fix G4 so the label covers the snapshot the verdict is about — and note
that the fourth option you did not take is currently the unsafe one (G2).

**2. `PYTHONDONTWRITEBYTECODE` — check the reasoning, and check for other
side-effect writes of the same family.** The reasoning is **correct** — see G3
opening. You were right that exempting would be the same defect one layer down,
and the tell you named (*"an exemption proposed to make a red go away rather than
to describe something true"*) is the right tell. But you did miss members of the
family, and one of them is not suppressible: the harness subprocess gets no env
override, nested `__pycache__` under the factory is outside the six-path exemption,
and WAL sidecars are created by **processes the factory does not launch**. G3 has
the evidence, including the live determinism flip.

**3. Is `read_only_trees` ⊆ `repos` scope creep, or the actual shape of F2?**
**The actual shape of F2, and the better statement of it.** F2 was *"a containment
promise that nothing measures."* An unfingerprinted read-only tree is that promise
in its purest form — my finding named the non-git repo because that is the instance
I could reach, and you generalised correctly to the class. Approve the rule. Two
caveats: it is under-enforced in the subtree direction (G2), and its error message
routes authors into G1.

---

## Action

- [ ] **star-lord — G1 (blocking on subtree-declaring workflows):** make
      `_is_git_worktree` compare `--show-toplevel` to the declared path and refuse a
      mismatch. **Discharges when** a workflow naming a subdirectory in `repos:`
      refuses to load, proven live.
- [ ] **star-lord — G2:** either enforce sub-repo read-only paths in `classify()`
      (match on `change_root / change.path`, not on `change_root`), or refuse them at
      LOAD. Then make
      `test_a_read_only_tree_nested_inside_a_declared_repo_is_accepted` assert that
      acceptance *enforces something*, or delete it.
- [ ] **star-lord — G3 (before the first agentic workflow runs):** pass a hardened
      env to the harness subprocess; decide and *declare* how transient DB sidecars
      are handled — named class or narrowed claim, never a category exemption. Note
      in the founding-run plan that `DETERMINISM: EXACT` presently requires host
      quiescence on the engine and godot trees.
- [ ] **star-lord — G4/G5/G6/G7:** non-gating.
- [ ] **star-lord — F3/F5/F6/F7/F8 from the first review:** still open, still
      non-gating. F5 (`usage_absent_reason` overloaded) is the one with a deadline —
      before `SCHEMA_VERSION` 1 gains a consumer. F4 (`permission_denials` dropped
      before the receipts) becomes materially more important the moment an agentic
      phase runs, since it is the record of an agent attempting a tool use it was
      not permitted; recommend pulling it forward with the G3 work.
- [ ] **Matt — decision needed:** **none to unblock.** G1–G3 are developer-fixable
      defects, not architectural calls, so lifting the BLOCK stays within my
      authority per ADR-002. Two items already correctly routed to you by star-lord
      and unchanged by this review: **O4** (drop vs. keep the dollars figure —
      gandalf and I ruled opposite ways) and **D-10** (no HALT status), which I
      agree is the largest remaining gap for the founding run and wants a dispatch,
      not a patch.
- [x] **jack-ryan:** BLOCK lifted. Mechanical lane remains approved. Agentic lane
      authorized for whole-repository workflows.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflow.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/runner.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/report.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/gates/core.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/harness/claude_code.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_permissions.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_workflow.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflows/kc2-baton-mechanical.yaml`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md`
- Probe evidence (in-tree, gitignored):
  `factory/sessions/jr-re-f1-ignored-20260810T235023Z-6b8a30/` (F1 contained, aborted)
  `factory/sessions/jr-re-f2-midrun-20260810T235812Z-16b2d1/` (F2 mid-run abort)
  `factory/sessions/jr-re-g1-subdir-20260810T235828Z-3d418d/` (G1 — rollback receipt says `deleted`; the file survived)
  `factory/sessions/kc2-baton-mechanical-20260810T235428Z-158abb/` + `…T235539Z-eacd0c/` (G3 — both laps aborted on WAL sidecars)
  `factory/sessions/kc2-baton-mechanical-20260810T235710Z-82624d/` + `…T235836Z-af6a69/` (quiet-tree determinism, 14 identical verdicts)
  Probe workflows: `/tmp/jr_re_f1_ignored.yaml`, `/tmp/jr_re_f2_midrun.yaml`, `/tmp/jr_re_f2_load.yaml`, `/tmp/jr_re_g1_subdir.yaml`
