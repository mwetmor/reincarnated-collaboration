# Finding — 2026-08-10 — factory-spine-v1 (Gate 2, WALL AUDIT / round four)

**Reviewer:** jack-ryan
**Severity:** **BLOCK** — one new defect (J1), BLOCK-class, three faces, one line. Four INFO/WARN.
**Target:** `agentic_orchestration/factory/` @ `e22cc0cd` (diffed against `be186953`)
**Developer:** star-lord (builder, ruling D4)
**Supersedes:** `2026-08-10-factory-spine-gate-2-verdict.md`
**Remediation note reviewed:** `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` § 9
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate / evidence), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** 8 (schema validation at boundaries), 11 (empirical inspection over assumption), 12 (semantic-shifting fixes need explicit framing)

---

## Verdict

**H1/H2/H3 are DISCHARGED. The read-only-overlap exclusion is DISCHARGED. The wall
works — I could not make it green with broken containment, and it falsified on all
seven mutations I threw at it.**

**And the agentic lane is BLOCKED again, on a defect worse than any of the previous
five, which I found by attacking the wall rather than the module.**

> **J1 — BLOCK.** `permissions.py:339` parses `git status --porcelain` with
> `rest.split(" -> ")[-1].strip().strip('"')`. That one line has three consequences,
> and the third is that **the factory's own rollback can be induced to delete the
> read-only tree it is fencing, from a file a phase was allowed to write.**
> Proven live through the shipped CLI. Quarantine-before-delete is the only thing
> that keeps it recoverable — and above 64 MB even that stops being true.

**Mechanical lane: remains approved** (see § 7 for why J1 is not reachable there in
practice, and what would make it reachable).

---

## What I reproduced (verified, not accepted)

| Claim | Result |
|---|---|
| 207 tests green (was 170) | **REPRODUCED** — `207 passed in 9.08s`, `python3` |
| `./factory run workflows/kc2-baton-mechanical.yaml` → PASS | **REPRODUCED**, ~1m25s per lap |
| `DETERMINISM: EXACT — 14 gate verdicts identical across two laps` | **REPRODUCED**, verbatim |
| Three `containment: coarse` declarations on godot | **CONFIRMED** — `['.godot/', 'Assets/Synty/']`, engine still zero coarse regions |
| Engine dirty 2789 / godot dirty 233, at baseline after every probe | **CONFIRMED**, before and after |
| H1 symlink escape closed | **CONFIRMED** by mutation test M1 (§ 1) |
| H2 nonexistent / file read-only tree refused at load | **CONFIRMED**, two tests, both raise |
| H3 symlink rollback + honest `NOT_ROLLED_BACK` | **CONFIRMED** by mutation test M5 (§ 1) |

One incidental confirmation worth recording: my first `./factory run` **aborted**
because a probe file I had just created under `factory/tests/` tripped
`PROTECTED_ALWAYS`. The no-self-modification fence works, and G3's host-quiescence
warning is now demonstrated twice by two different reviewers' own sessions.

---

## 1. The wall itself — does it falsify? **Yes. This is the strongest thing in the module.**

You asked me to attack the wall, not just the fixes. The test that matters is not
"does it pass" but "can I make it pass while containment is broken." I reverted each
fix in turn and re-ran the wall alone:

| Mutation | Wall result |
|---|---|
| M1 — revert H1 (`_read_only_hit` resolved-only) | **3 failed**, 32 passed |
| M2 — revert the stderr fold (unreadable subtree invisible) | **4 failed**, 31 passed |
| M3 — revert F1 (drop `--ignored=traditional`) | **4 failed**, 31 passed |
| M4 — revert G2 (read-only matched on repo root only) | **8 failed**, 27 passed |
| M5 — revert H3 (no `is_symlink()` branch in rollback) | **1 failed**, 34 passed |
| M6 — gut the fence entirely (`_read_only_hit` → `None`) | **18 failed**, 17 passed |
| M7 — over-widen the fence (breach everything) | **8 failed**, 27 passed |

**M7 is the one that matters most.** A `classify` that breaches unconditionally —
the cheapest possible way to make a containment wall green — is caught by the
`test_the_wall_can_go_green` partner in eight places. The wall is bidirectional, and
that is the difference between a wall and a ratchet. I asked for the partner in round
three; star-lord built it and it earns its keep.

**M5 returning only 1 failure is worth a sentence, not a finding.** H3's fix is
narrow by nature — one artifact kind exercises it. That is a correctly-sized row, not
thin coverage.

**Conclusion: the prescription worked.** The wall found the fifth defect (the stderr
channel) before any reviewer did, it resists both directions of tampering, and adding
a kind is genuinely one row — I verified this by adding three (§ 3). I am not asking
for a different mechanism. I am asking for rows, and for one assertion to be
tightened.

---

## 2. J1 — **BLOCK (new)** — the porcelain parse fabricates paths, and the rollback acts on them

**File:** `permissions.py:339`

```python
path = rest.split(" -> ")[-1].strip().strip('"')
```

`git status --porcelain` (v1) is not a whitespace-delimited format. It **C-quotes**
any path containing a character it considers special, and it uses ` -> ` as the
separator in rename records. That line handles neither correctly, and the wrong
answer is a path that **does not exist** — which is then treated as a real change,
classified, and **acted on by the rollback.**

Three faces. All three reproduced; the first two are containment escapes, the third
is destruction.

### (a) A staged rename OUT of a read-only tree is invisible. The run greens.

`split(" -> ")[-1]` keeps the rename destination and **discards the source**. So the
half of the rename that *removes bytes from the fenced tree* is never a change at all.

Live, through the shipped CLI, on the read-only-subtree shape my round-two verdict
explicitly discharged as safe:

```
-- phase 1/1: rename_out_of_readonly_subtree [mechanical]
   OK   command_succeeds: PASS -- `git mv src/canon.md scratch/canon.md` exited 0
   OK   diff_matches_claims: PASS -- change-set (0 path(s)) is a subset of the 0 claimed
   OK   verdict_consistent: PASS
run jr4-rename-escape -> PASS
=== DOES src/canon.md SURVIVE IN THE READ-ONLY TREE? ===
total 0
```

A tracked file left a declared read-only tree and **the change-set measured zero
paths.** The control is unambiguous: the identical move done with `mv` instead of
`git mv` breaches correctly. The difference between caught and clean is whether the
agent used the *more* disciplined command.

Under the shipped `writes: []` it is not better, only differently wrong: the breach is
recorded on the destination, the rollback deletes the destination, and the source
stays deleted. I reproduced that too — the fenced repo ends in state
`RD protected/tracked.txt -> workspace/moved.txt`. **The rollback completed the
destruction and reported `deleted` truthfully about the wrong path.**

### (b) Any path git quotes becomes a fabricated path

`strip('"')` removes the quote characters but does not C-unquote the escapes.

```
git:      ?? "protected/café.txt"
parsed:   protected/caf\303\251.txt      <- a path that does not exist
```

For a quoted name the *directory* component survives, so the read-only fence still
catches it — but the rollback then targets a path that was never on disk:

```
BREACH   : protected/caf\303\251.txt — write inside a read-only tree
ROLLBACK : NOT_ROLLED_BACK — "nothing at this path by rollback time; another
                             process may have removed it"
SURVIVED?: True
```

The artifact permanently survives inside the fenced tree, and the stated reason is
false — nothing removed it; the path was never real. Note what H3's fix did here: it
converted a *lying* `deleted` into an *honest-shaped but misdiagnosed*
`NOT_ROLLED_BACK`. That is an improvement and it is not enough (§ 5).

**Worse: a name containing ` -> ` escapes the fence entirely.** git quotes such names,
so the ` -> ` split fires *inside the quoted filename*:

```
planted : protected/'a -> b.txt'     (inside the read-only tree)
parsed  : b.txt                      (at the repo root)
writes  : ["**"]
result  : ALLOWED. Zero breaches.
```

Under `writes: ["**"]` — the agentic-lane shape — a file written into a read-only tree
is classified as an allowed write. Under narrow writes it breaches for the wrong
reason, names a path that never existed, and is not rolled back.

### (c) The rollback then deletes whatever the fabricated path happens to name

This is the part that makes J1 BLOCK rather than a third fence hole. The fabricated
path is not garbage — it is `<repo-root>/<whatever followed the last " -> ">`, which
is a **real, existing path**. `rollback` receives it as `kind="created"`,
`was_dirty_before=False` (a clean file is not in the baseline entries), and deletes it.

Live, through the shipped CLI. The phase writes **one empty file, inside its own
allowed `scratch/`**:

```
-- phase 1/1: write_only_inside_my_own_scratch [mechanical]
   PERMISSIONS BREACH during gate execution — aborting the run
     src (created) — write inside a read-only tree (/private/tmp/jr4/fe3/src)
     rollback: src -> deleted
ABORTED: permissions breach during gate execution: 1 path(s) outside the allowlist
=== THE READ-ONLY TREE /tmp/jr4/fe3/src ===
ls: /tmp/jr4/fe3/src: No such file or directory
*** THE READ-ONLY TREE IS GONE ***
=== the file the phase actually wrote ===
-rw-r--r--  0 Aug 10 21:06 junk -> src
```

The filename was `junk -> src`. The phase never touched `src/`. The factory reported a
breach that did not happen, and its rollback **`shutil.rmtree`'d the read-only tree it
was built to protect.** The file the phase actually wrote is still sitting there.

**Scope on this host, stated precisely, and not demonstrated live.** The fabricated
path is always a single component at the root of the repo the change was measured in.
On the engine that includes:

| Fabricated by a file named | Target | Size | Baseline guard? |
|---|---|---|---|
| `x -> src` | `~/Games/reincarnated-engine/src` | **6.5 GB** | no entry → guard misses |
| `x -> seasons` | `~/Games/reincarnated-engine/seasons` | **3.3 GB** | baseline key is `seasons/`, change path is `seasons` → **guard misses on the trailing slash** |

Both are above `_QUARANTINE_MAX_BYTES` (64 MB), so the quarantine writes a **manifest
of filenames only** and the `rmtree` proceeds. That is unrecoverable deletion of
3.3–6.5 GB, triggered by a filename. I verified the porcelain key forms and the
`was_dirty_before` miss by inspection; I did not and will not run it.

**On reachability — this is not an adversary story.** `git mv` is ordinary disciplined
agent behaviour and produces face (a) with no ill intent at all. `mapping -> out.json`,
`old -> new`, `a -> b` are ordinary artifact names and produce faces (b) and (c). An
agent holding Bash and a `writes` allowlist reaches all three without trying.

### The fix, verified before prescribing it

`git status --porcelain -z` is unambiguous: NUL-separated records, **no quoting**, and
renames emitted as two adjacent records — destination first, then origin. I confirmed
on this host against the exact inputs above:

```
porcelain    : R  protected/tracked.txt -> workspace/moved.txt
porcelain -z : R  workspace/moved.txt \0 protected/tracked.txt \0 ?? protected/ \0
```

So: switch to `-z`, split on NUL, and for `R`/`C` status codes consume the **next**
record as the origin and emit it as a change of its own. That closes all three faces
at the source, and it removes `.strip('"')` rather than trying to make it correct.

---

## 3. Should the wall have caught J1? **Partly mine, partly a real gap in the wall.**

You asked me to say plainly whether the prescription worked. It did — and I have to
own half of this.

**What is mine.** Round three named seven artifact kinds. Renames and quoted paths
were not among them. star-lord built eight and found a ninth himself. The wall is the
size I specified.

**What is the wall's.** I added three candidate rows to a scratch copy and ran it. The
rows are cheap and they work — but the pattern of *which* rounds go red is diagnostic:

| Candidate row | detects (r1) | fences (r2) | undo honest (r3) | can go green (r4) |
|---|---|---|---|---|
| `staged_rename_out_of_the_tree` | pass | **FAIL** | pass | **FAIL** |
| `path_containing_an_arrow` | pass | **FAIL** | **FAIL** | pass |
| `path_with_non_ascii` | pass | pass | pass | pass |

Two things fall out of that table, and both are wall defects, not missing rows.

**(i) Round one does not assert detection.** `assert changes` requires only that the
change-set be *non-empty*. Both escapes satisfy it — the rename with the destination
while the source vanishes, the arrow file with a **fabricated** path at the repo root.
The planter comment justifies the looseness ("what git reports may be that path, an
ancestor, or a collapsed entry") and the justification is correct; the assertion drawn
from it is too weak. The honest form is available and still covers all three shapes:
**the change-set must name the planted path, an ancestor of it, or a descendant of
it.** `b.txt` at the repo root is none of the three.

This is worth naming for what it is. Round one is *a predicate that answers a slightly
different question than the one asked, and whose wrong answer is green.* The wall has
the module's own disease, in the one assertion that is supposed to cure it.

**(ii) `path_with_non_ascii` passes all four rounds while the artifact permanently
survives inside the fenced tree under a false reason.** That is not a missing row. That
is the round-three contract being satisfiable by a consistent falsehood — § 5.

**So: the prescription worked, the mechanism is sound, and the wall needs one
assertion tightened and three rows added.** I would not trade this wall for anything
else. It is the reason round four found a *class* defect at the parse layer instead of
a sixth instance at the predicate layer.

---

## 4. Ruling on the empty-directory blind spot — **declared-and-bounded. Accepted. One clause of the bound overstates.**

**The declaration is correct and the pattern is right.** git tracks content, not
structure; there is genuinely no signal in the porcelain channel at any setting. This
is the first time this module has *declared a limit* instead of shipping a wrong
answer, and the failing-if-fixed test is exactly the right instrument. It is **not** a
sixth instance of the family: the family is "signal was available and the predicate
did not consult it." Here there is no signal to consult. I endorse it.

**I verified the bound holds for bytes.** Empty tree → invisible. Any file landing
anywhere inside it → git reports the collapsed entry → the fence catches it. Ignored
file inside it → `--ignored=traditional` reports it → caught. star-lord's argument is
sound on its own terms.

**Two corrections, neither of which changes the ruling.**

*The affordability reason is not the real reason.* The note says the stat sweep cannot
rescue it because descending only into git-reported paths "is the design that keeps the
engine's 3.3 GB affordable." That conflates the *exact* sweep (one stat per file —
genuinely expensive) with a *structure-only* sweep (no stats at all). I measured a
full `os.walk` of both read-only trees on this host:

```
engine: 968 dirs,  34,072 files, 0.21 s
godot : 5,240 dirs, 321,273 files, 1.69 s
```

~1.9 s per fingerprint, ~11 s per run if taken at phase boundaries on read-only trees
only, against an 83 s run. That is affordable. The blind spot is *closeable*; it is
being kept for cost/benefit reasons, which is a fine reason, but it should be stated
as the reason it is.

*"Bounded to directory structure" is true; the harmlessness it implies is not.* On the
two trees actually being fenced, an empty directory is not inert:
- **Python** — a bare directory is a PEP-420 namespace package. An empty
  `src/reincarnated/<name>/` turns an `ImportError` into a successful import of
  nothing. The engine is the read-only tree.
- **Godot** — a new directory under `res://` is picked up by the import scan. The
  godot tree is the other read-only tree.
- It is invisible to the rollback as well, so it is never cleaned and accumulates
  across runs.

**Ruling: accept the declaration; amend the wording.** Replace "bounded to directory
structure" with the two mechanisms named above and the measured cost of closing it, so
that a future author is choosing rather than reassured. Non-gating.

---

## 5. Ruling on the corrected rollback contract — **right floor, insufficient promise. Two clauses missing.**

**"The receipt and the disk agree" is the correct correction and star-lord's reasoning
for it is right.** Asserting "the artifact is always removed" would have forced the
rollback to become destructive to satisfy a test — the exact shape of F1, and he
declined it. Leaving evidence that cannot be safely quarantined is the right behaviour,
and **no**, leaving evidence in a read-only tree after an abort is not itself
unacceptable: the run has aborted, a human is now in the loop, and destroying evidence
to make a tree look tidy is the worse failure. The module says so in its own docstring
and it is correct.

**But the contract as phrased is satisfiable by a false-but-consistent narrative, and I
have three demonstrations.**

1. **`path_with_non_ascii` (§ 3).** Survives + `NOT_ROLLED_BACK` + a stated reason →
   contract satisfied. The reason — *"another process may have removed it"* — is
   fabricated. Nothing removed it. The receipt agrees with the disk about a fiction.
2. **The staged rename (§ 2a).** The destination was deleted, the receipt says
   `deleted`, the disk agrees — while the source stays destroyed inside the fenced
   tree. Every statement is true and the tree is materially damaged.
3. **The oversized branch (§ 6, J2).** Deleted + `deleted` → contract satisfied, while
   the artifact's only record is a note that says *"left in place, not copied"*.

The common shape: the contract is scoped to *paths that were classified as breaches*.
Everything J1 does happens to paths that were not.

**Ruling — the promise needs a second clause, and it is cheap.** Add to the contract:

> **After rollback, the fenced tree is back at its phase-start fingerprint — or every
> path that is not is named in the receipt.**

One extra fingerprint, on the abort path only, when the run is already over. It is a
whole-tree assertion rather than a per-breach one, so it catches damage the classifier
never attributed to a breach — including all three demonstrations above, and including
J1 face (a), which no per-path contract can reach. This is the durable answer, the same
way the wall was the durable answer to instance-by-instance predicate review.

*(Caveat worth stating: with J1 unfixed, the re-fingerprint would itself mis-name the
path. The parse fix has to land first. That is an ordering note, not an objection.)*

**And one clause on honesty:** a `NOT_ROLLED_BACK` reason must be derived from the
failure that actually occurred. "Nothing at this path by rollback time" is a correct
observation and an incorrect explanation. It should not speculate about other
processes when the module cannot distinguish that from its own bad path.

---

## 6. Smaller findings

### J2 — WARN — the oversized-artifact branch deletes unquarantined, and its note says the opposite

`permissions.py:549-553`. Above 64 MB the rollback writes a note and then, for
`kind="created"`, deletes the artifact anyway. Exercised faithfully (cap lowered to 8 B):

```
rollback : ('protected/big.tar.gz', 'deleted', '.../big.tar.toolarge.txt')
on disk  : False
note text: "... was 1024 B -- left in place, not copied"
```

Three things at once: (i) the module docstring's stated safety rule — *"Nothing is
deleted unquarantined"* — is violated for exactly the artifacts most expensive to
recreate; (ii) the note asserts the artifact survives while the action deleted it, so
the only surviving record is wrong; (iii) `dest.with_suffix()` mangles multi-dotted
names (`big.tar.gz` → `big.tar.toolarge.txt`), so two artifacts can collide in
quarantine. **Zero tests reference this branch** — `grep -rn "toolarge\|manifest" tests/`
returns nothing. This is the branch that turns J1 face (c) from recoverable into
unrecoverable, which is why it is WARN and not INFO.

### J3 — INFO — a mode-only change to an ignored file inside a fenced tree is invisible

`_stat_sig` is `size:mtime_ns`; `chmod` moves ctime only. Verified: `chmod +x` on an
ignored file inside a read-only tree → empty change-set. The tracked-file equivalent is
caught (git reports the mode). No bytes cross the fence. Candidate row, not a defect.

### J4 — INFO — an mtime-preserving rewrite of an ignored file is invisible

Verified: rewrote an ignored file's contents inside the fenced tree while restoring
`st_mtime_ns`; change-set empty, content changed. This is the documented consequence of
`_signature` being stat-based rather than content-based, and that tradeoff is correctly
reasoned in the docstring — but it is reachable *without* adversarial intent by
`cp -p`, `rsync -a`, and `tar -x`, which is not stated. One sentence in the same place
the COARSE caveat lives.

### J5 — INFO — `_unreadable_paths` will mis-key a quoted directory name

Same root cause as J1(b): git quotes the path inside the `could not open directory '…'`
warning too, and `_unreadable_paths` does not unquote. Folds into the J1 fix.

---

## 7. The verdict on the lanes

**Was the read-only-overlap exclusion discharged? Yes.** H1 is genuinely closed:
lexical *and* resolved matching, both directions preserved for the G2 collapsed-entry
case, four symlink tests where there were zero, and mutation-verified (M1). `writes: ["**"]`
alongside a read-only tree is no longer the specific hazard my round-three verdict
named. H2 and H3 are closed on the same standard.

**Is the agentic lane authorized? No — BLOCKED on J1.**

The exclusion that lifted has been replaced by a defect with a wider trigger and a
worse consequence. The previous five were fence *escapes*: something got in and was
reported clean. J1 face (c) is the fence *firing on a path that does not exist and
destroying it*. A containment mechanism that can be induced to delete the tree it
protects, by an allowed write, is not a containment mechanism yet.

**Is the mechanical lane still approved? Yes, unchanged, and here is the reasoning
rather than the assertion.** J1 needs a filename, and in a mechanical workflow every
filename is authored by a human in the YAML. The shipped phases run `sha256`,
`ffprobe`, and `pytest -p no:cacheprovider` under `PYTHONDONTWRITEBYTECODE=1`; they
create no files at all, which is why `diff_matches_claims` reports 0 paths on all three
and why determinism is EXACT. The lane is safe because nothing in it chooses a name.
**That property should be written down**, because it is the whole reason the two lanes
diverge here — and it stops being true the moment a mechanical phase runs a command
that emits generated filenames.

**Nothing about this is a reversal of the wall.** The wall is why round four is a
*class* finding at the parse layer rather than a sixth instance at the predicate layer,
and the fix is one function plus four rows rather than a fifth patch. That is the
prescription doing exactly what it was for.

---

## Action

- [ ] **star-lord — J1 (BLOCKING, discharges the lane):** replace the porcelain parse
      with `git status --porcelain --ignored=traditional -z`; split on NUL; for `R`/`C`
      codes consume the next record as the rename **origin** and emit it as a change of
      its own. Delete `.strip('"')` rather than repairing it. **Discharges when** all
      three of my probes come back correct on a live run: the `git mv` out of a fenced
      subtree breaches on the *source*; `protected/'a -> b.txt'` breaches on its real
      path under `writes: ["**"]`; and `scratch/'junk -> src'` leaves `src/` standing.
- [ ] **star-lord — the wall, four items (land with J1):**
      (a) **tighten round one** — assert the change-set names the planted path, an
      ancestor, or a descendant, not merely that it is non-empty;
      (b) add rows `staged_rename_out_of_the_tree`, `path_containing_an_arrow`,
      `path_with_non_ascii` — I have verified all three fail today, at the diagnostic
      rounds in § 3;
      (c) add rows for `mode_only_change_to_an_ignored_file` (J3) and
      `oversized_artifact` (J2, with the cap monkeypatched — the branch has no coverage
      at all);
      (d) keep the empty-directory pin; amend its wording per § 4.
- [ ] **star-lord — J2 (WARN, land with J1):** decide explicitly whether an oversized
      created artifact is deleted or left. Either is defensible; the note must say what
      was actually done, and the docstring's "nothing is deleted unquarantined" must
      match the code. Fix `with_suffix` → append.
- [ ] **star-lord — the rollback contract (§ 5, land with J1):** add the second clause —
      after rollback the fenced tree is back at its phase-start fingerprint, or every
      path that is not is named. Derive `NOT_ROLLED_BACK` reasons from the failure that
      occurred; stop speculating about other processes.
- [ ] **star-lord — document the mechanical lane's safety property** (§ 7): mechanical
      phases are safe from name-driven defects because a human authors every filename,
      and that stops being true if a mechanical phase emits generated names.
- [ ] **star-lord — J3/J4/J5:** non-gating, fold into the above.
- [ ] **star-lord — F3–F8 (round one):** still open, still non-gating. **F4
      (`permission_denials` dropped before the receipts) should land with J1**, as in
      round three.
- [ ] **knight-rider:** the founding-run host-quiet window (G3) is still owed and is now
      demonstrated twice — my own probe file aborted a lap of this review's own run.
- [ ] **Matt — decision needed: none to hold the block.** J1 is a developer-fixable
      defect, so this stays within my authority per ADR-002. Unchanged and still yours:
      **O4** (the dollars figure) and **D-10** (no HALT status). **Informational, and it
      is the one thing I would want you to see even if you read nothing else:** for the
      third round running, the defect was not in the code that was under review. Round
      two found it in round one's fix, round three in round two's fix, and round four
      found it in a line nobody had touched since the founding commit — reachable only
      because the wall pushed the search up a layer. That is the review converging, not
      failing.
- [x] **jack-ryan:** H1/H2/H3 discharged; read-only-overlap exclusion discharged; the
      wall audited and endorsed as the mechanism. **Agentic lane BLOCKED on J1.**
      Mechanical lane approved, unchanged.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py`
  (`:339` the parse — J1; `:426-459` `_read_only_hit` — H1 closed; `:501-633` `rollback` — H3 closed, J1(c), J2)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflow.py` (`:300-320` — H2 closed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_containment_wall.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_workflow.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/README.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` § 9
- Probe workflows: `/tmp/jr4/rename_escape.yaml`, `/tmp/jr4/collateral.yaml`
- Probe evidence (in-tree, gitignored) under `factory/sessions/`:
  `jr4-rename-escape-20260811T010153Z-840eda/` (**J1(a) — run PASS, fenced file gone**)
  `jr4-collateral-destruction-20260811T010655Z-0333fa/` (**J1(c) — read-only tree deleted by the rollback**; the quarantined `breach/…/fe3/src/{a,b}.md` are what made it recoverable)
  `kc2-baton-mechanical-20260811T010303Z-b8c8f4/` + `…T010428Z-7d02e3/` (determinism EXACT, 14/14)

**Post-review state:** probe file removed from `factory/tests/`; `permissions.py`
byte-identical to `e22cc0cd`; suite **207 passed**. Engine dirty **2789**, godot dirty
**233** — both at baseline. All probes were confined to `/tmp/jr4/`; the 6.5 GB and
3.3 GB engine cases in § 2(c) were established by inspection and **not** executed.
