# Finding — 2026-08-10 — factory-spine-v1 (Gate 2, round six)

**Reviewer:** jack-ryan
**Severity:** **BLOCK** — K1 discharged; two new BLOCK-class defects (L1, L2), two WARN, three INFO.
**Target:** `agentic_orchestration/factory/` @ `463a620b` (diffed against `3a8ca231`)
**Developer:** star-lord (builder, ruling D4)
**Supersedes:** `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate-2-round-five.md`
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate / evidence), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** 8 (schema validation at boundaries), 11 (empirical inspection over assumption), 12 (semantic-shifting fixes need explicit framing)

---

## Verdict

**K1 is DISCHARGED**, against my own round-five criterion, reproduced live through the
shipped CLI on a sandbox I built myself.

**The agentic lane remains BLOCKED — on L1, which lives inside the K1 fix, and on L2,
which lives inside the K2 fix.**

> **L1 — BLOCK.** The module hands raw filesystem **paths** to git as **pathspecs**. A
> path is not a pathspec. Three call sites shipped this round rest on that confusion,
> and two of them are the guards built to close K1 and K3. Live, through the shipped
> CLI: a phase edits **one** file inside a fenced read-only tree; the rollback runs
> `git checkout -- ':(top)'`; git reads that as pathspec magic meaning *from the
> repository root*; **the entire repository is reverted**, every uncommitted in-flight
> change destroyed — and the receipt says `restored`. That is K1, outcome for outcome,
> through the guard written to prevent K1.

> **L2 — BLOCK.** `_kind_of_new_entry` — K2's new predicate — types a rename
> **destination** as `modified`, because `"A" not in "R "`. The rollback then runs
> `git checkout --` on it, which restores the file **from the index the phase had just
> staged**, so the artifact is left exactly as the phase wrote it and the receipt says
> `restored`. Pre-K2 the same artifact came back `NOT_ROLLED_BACK` with an honest
> refusal. **The K2 fix converted an honest refusal into a false restore.**

This is the **eighth** instance of the family and it is in the fix for the seventh,
for the fifth round running. The axis is new — **wrong LANGUAGE** — and it joins
CATEGORY, BASE, GRANULARITY, TARGET, CHANNEL, PARSE and K1's `restored`. L2 is not a
new axis: it is **K2's own axis, re-broken on the status codes K2 did not enumerate.**

---

## What I reproduced (verified, not accepted)

| Claim | Result |
|---|---|
| 262 tests green (was 247) | **REPRODUCED** — `262 passed in 19.99s` |
| Founding run PASS, 1m43s | **REPRODUCED** — PASS, 1m44.91s (within noise) |
| `DETERMINISM: EXACT — 14 gate verdicts identical across two laps` | **REPRODUCED**, verbatim (laps `…025459Z-3e00df` / `…025643Z-bd086b`, both PASS) |
| Engine 2789 / godot 233 dirty at baseline (plain `--porcelain`) | **CONFIRMED** — and identical after every probe |
| Engine 0 / godot 1 modified-tracked | **CONFIRMED** |
| K1 live probe inverted: `newdir (created)` → `deleted`, fenced work intact | **REPRODUCED** on my own sandbox (§ 1) |
| K5 — the accounting predicate exists once and is shared with its falsifier | **CONFIRMED** — `_unaccounted` defined once at `:255`, used by round four at `:432` and by its falsifier at `:869` |
| K7 / K8 / K9 closed | **CONFIRMED** (§ 6) |
| `permissions.py` + `tests/` byte-identical to `463a620b` after star-lord's mutations | **CONFIRMED** — `git diff HEAD` empty |

All destructive probes confined to `/tmp/jr6*`. Nothing was written to the engine,
godot, demo or loadout trees.

---

## 1. K1 — **DISCHARGED**, on my own criterion

My round-five discharge criterion, verbatim:

> *Discharges when the live probe reproduces with the tree intact: the empty directory
> is detected and fenced, the uncommitted work in the fenced tree survives, and the
> receipt says what was and was not undone.*

Built fresh at `/tmp/jr6` (two repos in the shipped shape: a `repos:` entry that is
also a `read_only_trees:` entry at its worktree root; the fenced repo carrying
uncommitted work on two tracked files). One phase: `mkdir -p …/fenced/newdir/deeper`.

```
   PERMISSIONS BREACH during gate execution — aborting the run
     newdir (created) — write inside a read-only tree (/private/tmp/jr6/fenced)
     rollback: newdir -> deleted
ABORTED: permissions breach during gate execution: 1 path(s) outside the allowlist

########## AFTERMATH — the fenced tree ##########
--- git status ---   M src/canon.md /  M src/other.md    <- both still dirty
--- src/canon.md --- PRECIOUS COMMITTED BASELINE
                     UNCOMMITTED WORK IN FLIGHT          <- INTACT
--- src/other.md --- another tracked file
                     more in-flight work                 <- INTACT
--- newdir ---       No such file or directory           <- artifact GONE
```

Three faces, each verified as the change star-lord describes:

- **the sweep NAMES the directory** — `newdir`, not `.`. `newdir/deeper` is correctly
  folded into the one row rather than emitted twice, and `rmtree` takes both.
- **the whole-tree pathspec guard REFUSES** `.` / `""` / `*` / `**` / a declared tree
  root — confirmed by direct call.
- **`.git` is out of the walk**, so a plain `git add` in a fenced tree no longer reads
  as a structural write.

All four K1 changes are real and each does what the commit message says. **K1 closed.**

---

## 2. L1 — **BLOCK (new)** — a path is not a pathspec

**Files:** `permissions.py:686-701` (`_tracks_content`), `:704-724`
(`_is_whole_tree_pathspec`), `:907` (`git checkout -- change.path`).

Git pathspecs are a *language*, not a list of filenames. A pathspec whose first
character is `:` is **magic**: `:(top)` and `:/` mean *the whole repository from its
root*; `:(glob)`, `:(icase)`, `:!` and friends change matching wholesale. The module
takes repo-relative paths straight off the fingerprint and passes them to git as
pathspecs at three sites. Every one of the three fails in the permissive direction.

### L1(a) — the K1 guard passes every magic form. Live.

```
_is_whole_tree_pathspec('.')          -> refused
_is_whole_tree_pathspec(':(top)')     -> None      <- means the whole repo to git
_is_whole_tree_pathspec(':/')         -> None      <- means the whole repo to git
_is_whole_tree_pathspec(':(glob)**')  -> None      <- means the whole repo to git
```

Through the shipped CLI, on a fenced read-only tree carrying uncommitted work, with
one phase appending a line to one file named `:(top)`:

```
     :(top) (modified) — write inside a read-only tree (/private/tmp/jr6magic2/fenced)
     rollback: :(top) -> restored

########## AFTERMATH — the fenced tree ##########
--- git status --porcelain ---  (empty — the tree is now CLEAN)
--- src/canon.md ---  COMMITTED BASELINE          <- the uncommitted line is GONE
--- src/other.md ---  another tracked file        <- the uncommitted line is GONE
```

One file touched; the whole repository reverted; every uncommitted in-flight change in
the fenced tree destroyed; receipt word `restored`. **This is K1's outcome, produced by
K1's own guard.** The guard answers *"is this string one of the four literals I
enumerated, or a declared tree root?"* The question asked is *"will `git checkout --`
treat this pathspec as the whole tree?"* — and the wrong answer, `None`/"proceed", is
the safe-looking one.

### L1(b) — the destroyer guard goes blind, and `rmtree` fires. Live.

```
tracked under ':magic' per git:  :magic/committed.md
  git ls-files  --  :magic                    -> rc=0  out=''   err=''
  git ls-tree -r --name-only HEAD -- :magic   -> rc=0  out=''   err=''
  _tracks_content(':magic') = 0    <-- 0 is the answer that authorises rmtree
```

Not an error path — **rc=0, empty output, silently wrong.** Through the shipped CLI, a
phase running `git mv src ':magic'` inside a fenced tree:

```
     :magic (created) — write inside a read-only tree
     rollback: :magic -> deleted
########## AFTERMATH ##########  ls -a: . .. .git      <- the tree is EMPTY
```

This falsifies **README rule 7** — *"Either question alone is answerable `no` while
work is present; both together are not."* Both together are answerable `no`. K3 added
the second question; it did not fix the language the questions are asked in.

**Mitigations, stated accurately.** The bytes *were* quarantined before deletion, so
rule 2 held and the evidence exists at `sessions/…/breach/fenced/:magic/`. The content
here was committed and recovers with `git checkout HEAD -- .`. What does **not**
recover is any untracked, ignored or uncommitted content inside the deleted directory.

### L1(c) — the same confusion at the restore verb

`git checkout -- change.path` at `:907` is the third site and is what L1(a) rides on.
`_matches` and `_read_only_hit` are purely lexical and are **not** affected.

### Reachability, bounded honestly

Magic is **positional** — only a leading `:` on the pathspec. Confirmed:
`ls-files -- 'sub/:magic'` resolves correctly. So the surface is *a top-level entry
whose name begins with `:` in a declared tree*. Both shipped `read_only_trees`
(`~/Games/reincarnated-engine`, `~/Games/reincarnated-godot`) are worktree roots **and**
`repos:` entries, so change paths inside them are unprefixed and reach the surface
directly. Neither tree carries such an entry today — that is a property of today's
working trees, not of the mechanism.

### The fix — one line, closes all three

`GIT_LITERAL_PATHSPECS=1` in `_git`'s environment. Verified at the git level:

```
GIT_LITERAL_PATHSPECS=1 git ls-files -- ':magic'   -> :magic/committed.md
GIT_LITERAL_PATHSPECS=1 git checkout -- ':(top)'   -> only ':(top)' restored;
                                                      src/canon.md still ' M'
```

It also retires the glob-character question round five probed with `v[1]`, because
literal pathspecs disable `*`, `?` and `[` as well. With magic off,
`_is_whole_tree_pathspec` becomes a *correct* model of the language rather than a
partial enumeration of it, which is the property that matters.

**Discharges when** the live probe reproduces with the tree intact: `:(top)` is
restored, `src/canon.md` and `src/other.md` keep their uncommitted work, and
`_tracks_content(':magic')` is non-zero. Reproduction:
`/tmp/jr6wall/test_jr6_shape.py` (red now), `/tmp/jr6magic2/magic2.yaml`,
`/tmp/jr6magic/magic.yaml`.

---

## 3. L2 — **BLOCK (new)** — the rename destination, and the receipt word flipped the wrong way

**File:** `permissions.py:497-521` (`_kind_of_new_entry`).

`git status --porcelain -z` emits a staged rename as `R <dest>\0<orig>\0` — verified.
The parser handles both ends correctly (J1 holds). But the **destination** carries code
`R ` (or `RM`), which contains no `A` and does not start with `D`, so it falls through
to `return "modified"`. The rollback then runs `git checkout --` on a path the phase
has just **staged**, git restores it *from the index*, and the file is left exactly as
the phase wrote it.

Live, through the shipped CLI — `git mv src/canon.md src/renamed.md` inside a fenced,
clean read-only tree:

```
     src/renamed.md (modified) — write inside a read-only tree
     src/canon.md (deleted) — write inside a read-only tree
     rollback: src/renamed.md -> restored
     rollback: src/canon.md -> NOT_ROLLED_BACK
########## AFTERMATH ##########
ls src/                 renamed.md
git status --porcelain  R  src/canon.md -> src/renamed.md
```

The fenced tree is left **fully mutated** — the original gone, the new file present,
the rename still staged — and the only positive verb in the receipt is `restored`.

### It is a regression, and I measured it rather than inferring it

Same artifact, same sandbox, the two kinds side by side:

| kind | receipt | reason | artifact on disk |
|---|---|---|---|
| `modified` — **shipped (K2)** | `restored` | `git checkout -- <path>` | **True** |
| `created` — **pre-K2** | `NOT_ROLLED_BACK` | `REFUSED: … git tracks 1 file(s) under it` | True |

The artifact survives either way. What K2 changed is that the receipt stopped saying
so. That is precisely the mutation I named in K1 — *the wrong answer is no longer
`clean`, it is `restored`* — reproduced inside the fix for K2, and reached by
`git mv`, which is the command round four's J1 was about.

**Fix.** An `R`/`C` destination is a path that did not exist before the phase: it is a
`created`. Typing it so restores the honest refusal immediately. The better end-state
pairs it with L3 so the refusal names the real reason (*the phase staged this rename;
unstaging is a human decision*) instead of asserting a misidentification.
`_kind_of_new_entry` should enumerate the porcelain code space explicitly and
`return "modified"` should not be the default that catches everything unlisted —
a default that catches the unenumerated is how this class recurs.

---

## 4. L3 — **WARN** — the guard returns a count, so the caller cannot tell which question said yes

`_tracks_content` unions the index and HEAD and returns `len(seen)`. The union is right;
collapsing it to an integer is not. A phase that creates a file inside a read-only tree
**and stages it** — a disciplined agent — produces:

```
     src/planted.md (created) — write inside a read-only tree
     rollback: src/planted.md -> NOT_ROLLED_BACK
   reason: REFUSED: reported as created by the phase, but git tracks 1 file(s) under
           it — the path identification is wrong and deleting it would destroy
           committed work

ls-files:      src/planted.md
ls-tree HEAD:  (empty)
```

Both clauses of the reason are false: the identification is exactly right, and there is
no committed work — HEAD has never heard of the path. The artifact survives inside the
fence. **This is K2's defect in a different branch**, and K4 fixed one instance of the
false-reason class rather than the class. The distinction the guard needs is the one it
already computes and throws away: *HEAD knows it* → refuse, deleting would destroy
committed work; *only the index knows it* → that is the phase's own staged write, so
delete it and unstage, or refuse **for that reason**.

Third round running in which the *more* disciplined git command is the one containment
handles worst.

---

## 5. L4 — **WARN** — the wall is load-bearing, and it is structurally blind to K1's damage class

Round three now checks contents (`_assert_contents_match`), round four's predicate
exists once and is shared with its falsifier, and fourteen kinds each carry an
allowed-where-declared partner. The mechanism is sound and I am not asking for a
different wall. Two structural properties of the **fixture**, though, make the entire
K1 family unobservable — which is why L1 and L2 shipped green under 262 tests.

**(i) The fixture is not the shipped shape, and its docstring says it is.** `fenced`
declares `protected/` — a *subdirectory* — as the read-only tree. Both shipped
`read_only_trees` are worktree **roots** that are also `repos:` entries. Every wall
change path therefore carries a `protected/` prefix, and that prefix is exactly what
neutralises leading-`:` magic and makes `_is_whole_tree_pathspec`'s tree-root branch
unreachable. Demonstrated: the identical row is **green** in the fixture's shape and
**red** in the shipped shape (`/tmp/jr6wall/test_jr6_extension.py::test_A` vs
`/tmp/jr6wall/test_jr6_shape.py`).

**(ii) No wall row has uncommitted work at phase start.** The fixture commits
everything, so the tree is clean when `_snapshot` takes the baseline. K1's damage —
*a rollback destroying uncommitted modifications to tracked files* — has nothing to
destroy in any of the fifty-six parametrized runs. Relatedly, rounds three and four
call `perm.rollback(breaches, {}, …)` with an **empty** `before` map, so
`was_dirty_before` is `False` in every one of them: the pre-existing-dirt guard —
landed twice this round, by K1(3) and K4 — is exercised only by the single dedicated
test at `:747`.

Both are one-line fixture changes. Three rows I wrote against the shipped module, two
red:

| row | verdict |
|---|---|
| a pathspec-magic name at a fenced worktree root does not revert the repo | **RED** |
| the destroyer guard sees committed content under a `:`-named directory | **RED** |
| a rename destination is not falsely reported `restored` | **RED** |

**On the honesty of the M13–M19 table.** Star-lord recorded that M18 and M19 were
GREEN on first attempt and why, and corrected both. That is the disclosure I want and
I am counting it in his favour, not against. The M13–M19 anchors all resolve against
the shipped file and each reverts the change it claims to. The table's residual weakness
is not dishonesty, it is **scope**: a mutation table can only falsify what the fixture
can express, and this fixture cannot express K1's damage class at all. That is the gap
to close, not the table.

---

## 6. K2–K5, K7–K9 — dispositions

- **K2 — CLOSED for the case it named, RE-OPENED as L2.** A clean tracked file that a
  phase modifies is now typed `modified` and restored correctly; verified. The predicate
  mis-answers `R`/`RM`.
- **K3 — CLOSED for the case it named, RE-OPENED as L1(b) and L3.** The union is
  present and correct; `git rm --cached` no longer blinds the guard. Pathspec magic
  blinds both halves at once, and the count discards the distinction.
- **K4 — CLOSED.** `_covers` is bidirectional and `:747` asserts the refusal *by that
  reason*; M17 reverts the exact anchor. The bidirectional widening is **conservative**
  in every direction I could find — it can only make `was_dirty_before` more true, and
  more true means refuse. Not a defect; see L6 for its cost.
- **K5 — CLOSED.** `_unaccounted` at `:255`, one definition, shared by round four
  (`:432`) and its falsifier (`:869`).
- **K7 — CLOSED.** The bad M10 row is gone with the round-five table.
- **K8 — CLOSED.** *"Eleven rules"* now sits above eleven rules. Rules **7 and 10 are
  false as written** for a new reason (L1) and rule **11 is incomplete** (L2).
- **K9 — CLOSED.** `test_K9_the_filesystem_refuses_a_non_UTF8_filename` pins the host
  property, as asked.

---

## 7. The lanes

**Agentic lane: BLOCKED on L1 and L2.** The lane's premise is a model choosing commands
inside a fenced tree. `git mv` is such a command, and it now produces a fully mutated
read-only tree with `restored` on the receipt. A model choosing a `:`-prefixed path at
a tree root reverts the repository or triggers an unrefused `rmtree`.

**Mechanical lane: approval STANDS, on the same narrow empirical grounds, re-verified
this round.**

> The three shipped phases of `kc2-baton-mechanical.yaml` are approved as written. They
> declare `writes: []`, produce **0-path change-sets** on every phase, and create no
> directories in either read-only tree — verified over three laps this round (one run
> plus a two-lap determinism pass), all PASS, engine and godot dirty counts at 2789 /
> 233 before and after. Neither declared tree carries a top-level `:`-named entry today.

**The approval remains void for any mechanical phase that runs a git write-operation in
a read-only tree, creates a directory in one, or introduces a path whose name begins
with `:` at a tree root.** That is a property of the phase list, not of the lane, and
it is re-checked whenever a phase is added.

---

## 8. The five questions, answered

**1. Does K1 discharge?** Yes — § 1, on my own criterion, my own sandbox.

**2. Is the fix itself the eighth instance?** **Yes.** Two of the four new predicates
carry it. `_is_whole_tree_pathspec` (the K1 guard) and `_tracks_content` (the K3 guard)
both model git's pathspec language as a list of strings; `_kind_of_new_entry` (the K2
guard) enumerates part of the porcelain code space and defaults the rest to `modified`.
Of the four, only `_covers` came through clean, and it did so because its failure
direction is refusal.

**3. The wall's honesty.** The corrected wall is load-bearing and is not
self-confirming — its rows failed for me when I mutated the module. It is **blind by
construction** to the K1 damage class, for the two fixture reasons in § 5. The kinds it
still does not cover: a name that is a git *pathspec* rather than a path; a staged
artifact (`A `, `R `, `RM`) of any sort; and any artifact planted while the tree carries
uncommitted work.

**4. Are the refusal semantics right?** **Yes, and it is not a fail-open** — for one
structural reason: the run **aborts**. A fail-open is a mechanism that lets a run
continue on a false clean; here the breach is detected, quarantined, recorded and the
run stops. Leaving the artifact is a cost paid to avoid destroying work that was never
the phase's, which is the strictly worse failure and the one you have now shipped twice.
Two conditions, neither currently met: the refusal must be **visible as coverage loss**
(L6), and it must **cite the reason that actually applies** (L3).

**5. K2–K5, K7–K9.** § 6 — three closed outright, two closed-and-partly-reopened, three
closed.

---

## 9. Smaller findings

- **L5 — INFO.** `command_succeeds` runs `shlex.split(command)` as argv with **no
  shell**, so `cd X && git mv …` becomes `/usr/bin/cd` with four extra arguments, exits
  0, and the gate reports **PASS** for a command that did nothing. I hit this on my
  first probe. The argv form is the right design; the silent degradation is not. A gate
  holding shell metacharacters (`&&`, `||`, `;`, `|`, `>`, `<`) in argv should come back
  `not_runnable`. A green that measures nothing is the shape the wall exists to end.
- **L6 — INFO.** Refusal coverage is unmeasured. The engine's baseline carries **53
  collapsed dirty directory entries** (`cache`, `foundation`, `logs`, `output/…`), and
  **358 of its 686 non-`.git` directories (52%)** sit under one. Any structure-sweep
  change in that region comes back `NOT_ROLLED_BACK` citing *"path was already dirty at
  phase start"* — false about the path itself, true about its ancestor. This is the
  right posture and a large silent region. Rule 3 emits a per-phase
  `containment_coarse` receipt naming its regions; refusal deserves the symmetric
  `containment_not_undone`.
- **L7 — INFO.** README: rule **7**'s closing sentence and rule **10** are falsified by
  L1; rule **11** is incomplete per L2. Minor: `_is_whole_tree_pathspec` refuses any
  `norm.startswith("..")`, which also refuses a legal filename beginning `..` — the safe
  direction, worth a comment so it is not later "fixed".
- **F3–F8 (round one), F4 in particular** — still open, still non-gating. Unchanged.
- **G5-family reason bug** (receipt says *"the phase committed this path"* when a
  co-tenant did) — confirmed as star-lord logged it; non-blocking, same class as L3.

---

## Action

- [ ] **star-lord — L1 (BLOCKING):** set `GIT_LITERAL_PATHSPECS=1` in `_git`'s
      environment, so every pathspec the module builds from a filesystem path is read as
      a path. Then re-state `_is_whole_tree_pathspec`'s comment to say what it now is —
      a complete model of the whole-tree forms *under literal pathspecs* — rather than a
      partial enumeration. Correct README rules 7 and 10. **Discharges when**
      `/tmp/jr6wall/test_jr6_shape.py` goes green against the shipped module and
      `_tracks_content(':magic')` is non-zero.
- [ ] **star-lord — L2 (BLOCKING):** type an `R`/`C` destination as `created`.
      Enumerate the porcelain code space explicitly; `modified` must not be the default
      that catches every code nobody listed. Correct README rule 11. **Discharges when**
      `git mv` inside a fenced tree leaves a receipt that does not say `restored` about
      a file the phase's own index is holding.
- [ ] **star-lord — L3 (WARN, land with L2):** have the destroyer guard report *which*
      question answered yes. HEAD → refuse, deleting would destroy committed work. Index
      only → that is the phase's own staged write; act on it, or refuse **for that
      reason**. No refusal may assert a misidentification that did not occur.
- [ ] **star-lord — the wall, four items (land with L1/L2):**
      (a) add a second `fenced` fixture in the **shipped shape** — the read-only tree
      IS a worktree root that is also a `repos:` entry — and run the four rounds against
      both; the docstring claiming shipped-shape must become true or go;
      (b) give the fixture **uncommitted work at phase start** on a tracked file no
      artifact touches, and assert it survives every rollback — that single assertion
      catches K1, L1(a) and any successor;
      (c) pass the real `before` map to `rollback` in rounds three and four, so the
      dirt guard is armed in all fifty-six runs instead of one;
      (d) add two kinds: `pathspec_magic_name` and `staged_artifact` (`git add` and
      `git mv`), each with its allowed-where-declared partner.
- [ ] **star-lord — L5/L6/L7:** non-gating. `not_runnable` on shell metacharacters in
      an argv gate; a `containment_not_undone` receipt symmetric with
      `containment_coarse`; the three README corrections.
- [ ] **knight-rider:** G3 (host-quiet window) still owed, unchanged. Star-lord's
      founding-run abort on gandalf's `9b3e7e2b` is the first observed instance rather
      than a theorised one; route it.
- [ ] **Matt — decision needed: none to hold the block.** L1 and L2 are
      developer-fixable, so they stay within my authority per ADR-002. Unchanged and
      still yours: **O4** (the dollars figure) and **D-10** (no HALT status).
      **Informational:** for the fifth round running the defect was not in the code
      under review but in the fix that closed the previous round's finding. I want to be
      precise about what that does and does not mean. It is **not** evidence that the
      fixes are bad — every one of round five's four K1 changes does exactly what it
      claims, K1 is genuinely dead, and the wall grew real teeth. It is evidence that
      **the review is descending a real gradient**: rounds one and two found defects in
      what the module measured, rounds three and four in how it parsed, rounds five and
      six in the language it speaks to git. Each round the surface is narrower and the
      trigger more exotic — K1 fired on `git add`, L1 needs a file named `:(top)` at a
      tree root. The single change I would make to the process is the one item that has
      now been owed twice: **a new predicate gets its wall row, in the shipped shape,
      before it ships.** Round five wrote that rule down for measurement surfaces and
      applied it; it was not applied to the four new *predicates*.
- [x] **jack-ryan:** K1 discharged. Agentic lane **BLOCKED on L1 + L2**. Mechanical
      lane approved **narrowly**, re-verified, for the three shipped phases as written.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py`
  (`:686-701` `_tracks_content` — L1(b), L3; `:704-724` `_is_whole_tree_pathspec` — L1(a);
  `:907` the destructive `git checkout` — L1(c); `:497-521` `_kind_of_new_entry` — L2;
  `:680-683` `_covers` — clean; `:352-395` `structure_dirs` — K1 closed;
  `:557-582` the structure diff — K1 closed)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_containment_wall.py`
  (`:204-223` the `fenced` fixture — L4(i)+(ii); `:255-259` `_unaccounted` — K5 closed;
  `:262-278` round three contents check; `:365`/`:424` `rollback(…, {}, …)` — L4(ii);
  `:747` the K4 row; `:882` the K9 row)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/README.md`
  (rules 7 and 10 falsified by L1; rule 11 incomplete per L2)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/gates/core.py`
  (`:276-318` `_exec_verdict` — L5)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/runner.py`
  (`:496-545` `_handle_breach`; `:514-519` the `declared_trees` wiring — correct)
- Round five: `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate-2-round-five.md`
- Probe sandboxes (all under `/tmp`, disposable): `/tmp/jr6` (K1 discharge),
  `/tmp/jr6mv` (L2 live), `/tmp/jr6add` (L3 live), `/tmp/jr6magic` (L1(b) live),
  `/tmp/jr6magic2` (L1(a) live), `/tmp/jr6top` + `/tmp/jr6tc` (git-level),
  `/tmp/jr6wall/test_jr6_extension.py` + `/tmp/jr6wall/test_jr6_shape.py` (the rows)
- Probe evidence (in-tree, gitignored) under `factory/sessions/`:
  `jr6-empty-directory-20260811T024302Z-88e52c` (**K1 discharged**),
  `jr6-git-mv-inside-fence-20260811T024456Z-2870ed` (**L2**),
  `jr6-pathspec-magic-20260811T024718Z-e31295` (**L1(b) — the tree emptied**),
  `jr6-pathspec-magic-checkout-20260811T024832Z-488c81` (**L1(a) — the repo reverted**),
  `kc2-baton-mechanical-20260811T024912Z-9227fe` + the two determinism laps

**Post-review state:** `permissions.py` and `tests/` byte-identical to `463a620b`;
suite **262 passed**. Engine dirty **2789** (0 modified-tracked), godot dirty **233**
(1 modified-tracked) — both at baseline before and after every probe. All destructive
probes were confined to `/tmp/jr6*`; nothing was written to any declared repo.
