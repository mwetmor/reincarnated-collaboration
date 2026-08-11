# Finding — 2026-08-10 — factory-spine-v1 (Gate 2, round five)

**Reviewer:** jack-ryan
**Severity:** **BLOCK** — J1 discharged; one new BLOCK-class defect (K1), three WARN, five INFO.
**Target:** `agentic_orchestration/factory/` @ `3a8ca231` (diffed against `e22cc0cd`)
**Developer:** star-lord (builder, ruling D4)
**Supersedes:** `agentic_orchestration/jack-ryan/2026-08-10-factory-spine-gate-2-wall-audit.md`
**Remediation note reviewed:** `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` § 10
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate / evidence), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** 8 (schema validation at boundaries), 11 (empirical inspection over assumption), 12 (semantic-shifting fixes need explicit framing)

---

## Verdict

**J1 is DISCHARGED — all three faces, verified live through the shipped CLI, not
accepted on assertion. The wall's own defect is fixed and its round one now asserts
detection rather than non-emptiness.**

**The agentic lane remains BLOCKED, on K1 — which lives in the round-four fix itself.**

> **K1 — BLOCK.** The structure sweep added in round four reports its change at the
> **root path of the read-only tree** (`"."` when the tree is a repo root, as both
> shipped read-only trees are). `rollback` hands that string to `git checkout --` as a
> **pathspec**. So a phase that creates **one empty directory** inside a fenced tree
> induces a **repo-wide `git checkout -- .`**, destroying every uncommitted
> modification to every tracked file in that repo — while the artifact that caused the
> breach is **left standing**. Proven live through the shipped CLI. The receipt records
> it as `restored`.

This is the seventh instance of the family, and it is in the fix for the sixth. The
shape is unchanged — *a predicate answering a slightly different question than the one
asked* — with one mutation: the wrong answer is no longer `clean`, it is `restored`.
That is the same disease presenting as a cure.

**Mechanical lane: approval NARROWED, not withdrawn** (§ 6). My round-four grounds —
"every filename in it is human-authored" — no longer cover the lane, because **K1 does
not need a filename.**

---

## What I reproduced (verified, not accepted)

| Claim | Result |
|---|---|
| 247 tests green (was 207) | **REPRODUCED** — `247 passed in 15.82s` |
| `./factory run workflows/kc2-baton-mechanical.yaml` → PASS | **REPRODUCED**, 1m46s (claimed 1m42s; within noise) |
| `DETERMINISM: EXACT — 14 gate verdicts identical across two laps` | **REPRODUCED**, verbatim |
| M8 — drop the rename origin record → 1 red | **REPRODUCED** — 1 failed, `test_J1a_a_git_mv_OUT_of_the_fence_names_the_SOURCE` |
| M9 — remove the destroyer guard → 1 red | **REPRODUCED** — 1 failed, `test_J1c_the_rollback_never_deletes_tracked_content` |
| M10 — revert `-z` to porcelain v1, alone → 21 red | **NOT REPRODUCED — I measure 29 red** (K7; favourable direction, wrong record) |
| Engine / godot dirty at baseline 2789 / 233 | **CONFIRMED**, before and after every probe |
| Structure sweep cost 0.21 s engine / 1.69 s godot | **CONFIRMED** — 0.24 s / 1.55 s cold, and stable across two reads |
| J1(a)/(b)/(c) closed | **CONFIRMED** — see § 1 |

`permissions.py` is byte-identical to `3a8ca231` after all mutations; suite re-run green.

---

## 1. J1 — **DISCHARGED**, all three faces

`_parse_porcelain_z` is the right fix in the right place, and it removes
`.strip('"')` rather than trying to repair it. I checked it against every axis the
prompt named:

- **`R`/`C` origin consumption** — correct. The origin is emitted under `RENAME_SOURCE`
  and typed as a **deletion** in `diff_fingerprints`, which is the load-bearing half:
  `created` is the one kind the rollback deletes.
- **Copy detection (`C`)** — I set `status.renames=copies` and forced a byte-identical
  copy. `git status` emits `A `, not `C `; no `C` record is reachable from `status` at
  all, and the source is not mistyped as deleted. **Not a defect.**
- **Unmerged (`U`), submodule status, collapsed `--ignored=traditional` entries** —
  single-record forms, no origin consumed, trailing slash normalised at every consumer
  (`_matches`, `_read_only_hit`, `rel_norm`). **Not a defect.**
- **Non-UTF-8 filenames** — `_git` uses `text=True` with strict decoding, so a
  latin-1 byte in a filename would raise rather than fabricate. It is unreachable here:
  **APFS refuses the name outright** (`Errno 92: Illegal byte sequence`). K9.
- **`git ls-files` pathspec glob magic** — I planted a tracked directory literally named
  `v[1]`. git matched it correctly and both directions fail closed. **Not a defect.**

**There is no seventh defect in the parser.** It is in the other thing round four added.

---

## 2. K1 — **BLOCK (new)** — the structure sweep's path is a repo, and the rollback treats it as a pathspec

**Files:** `permissions.py:514-518` (the change is constructed at the tree root),
`permissions.py:631-634` (the guard that would have stopped it), `permissions.py:763`
(the destructive call).

### Live, through the shipped CLI

Two sandbox repos in the shipped shape — a `repos:` entry that is also a
`read_only_trees:` entry at its worktree root, exactly as `~/Games/reincarnated-engine`
is declared. The fenced repo carries uncommitted work on two tracked files, as the
engine does mid-session. The phase runs one command: `mkdir -p …/fenced/newdir`.

```
-- phase 1/1: make_one_empty_directory [mechanical]
   PERMISSIONS BREACH during gate execution — aborting the run
     . (modified) — write inside a read-only tree (/private/tmp/jr5/fenced)
     rollback: . -> restored
ABORTED: permissions breach during gate execution: 1 path(s) outside the allowlist

########## AFTERMATH — the fenced tree ##########
--- git status ---            (empty — the tree is now CLEAN)
--- src/canon.md ---
PRECIOUS COMMITTED BASELINE   <- the uncommitted line is GONE
--- src/other.md ---
another tracked file          <- the uncommitted line is GONE
--- does newdir survive? ---
/tmp/jr5/fenced/newdir        <- the artifact is STILL THERE
```

The rollback destroyed work it was built to protect and left the thing it was built to
remove. The receipt word is `restored`.

### Why the two guards that exist do not fire

1. **The destroyer guard is scoped to `kind == "created"`.** A structure change is
   typed `modified`, so it falls straight through to `git checkout -- <path>`. My
   round-four prescription said `created` is the one kind the rollback deletes; that
   was true then. `git checkout --` on a whole repo is equally destructive and the
   guard does not cover it.
2. **`was_dirty_before` is an exact-string membership test.**
   `any(e.rstrip("/") == rel_norm for e in before_fp.entries)` — the change path is `.`
   or `protected`, and the dirty entries are `src/canon.md`, `src/other.md`. **No
   ancestor match**, so the pre-existing-dirt protection — the one thing that exists to
   stop exactly this — is bypassed by the very change shape most likely to need it.

### The trigger is ordinary, and it is name-independent

`structure_signature` walks the whole read-only tree **including `.git`**: 281 of the
engine's 968 directories (29%) and 276 of godot's 5,240. So the sweep fires on
`.git/objects/<xx>/` fanout creation. Measured:

```
structure before `git add`: dirs:16:6e2b00db1525d7cd
structure after  `git add`: dirs:17:d71b6b76bc5a00af
-> structure sweep fires on a plain `git add`: True
```

An agent running `git add`, `git stash`, `git commit` or `git fetch` in a read-only
tree — or creating any directory anywhere in it — trips a repo-wide
`git checkout -- .`. **No filename is involved**, which is why my round-four
mechanical-lane reasoning does not reach it.

### Blast radius, stated precisely

`git checkout -- .` restores the worktree from the index. It does **not** touch
untracked files, so the engine's 2,789 untracked/ignored dirty paths are safe. What it
destroys is uncommitted modifications to **tracked** files. On this host **right now**
that is 0 files in the engine and 1 in godot — so today's exposure is small, and that
is a property of today's working tree, not of the mechanism. The factory exists to run
while agents have work in flight; the number is whatever is uncommitted at run time.

One operational note, not a finding: for a change at `.` the quarantine step first sums
`st_size` over `rglob("*")` of the whole tree — a 6.5 GB walk on the engine — before the
destructive checkout. Slow, not itself harmful. Established by inspection; not run.

### The fix

The narrow, correct fix is at the rollback boundary, and it does not depend on knowing
which measurement produced the coarse path:

- **Refuse `git checkout --` on a pathspec that is not a proper subpath.** `.`, the
  empty string, and any path equal to a declared repo or read-only tree root must be
  `NOT_ROLLED_BACK` with the reason stated. A rollback that cannot name a *file* has not
  identified an artifact — it has identified a tree, and acting on a tree is a human
  decision. This is the same principle as the destroyer guard, applied to the other
  destructive verb.
- **Make `was_dirty_before` ancestor-aware.** A change at `X` must count as dirty-before
  if any baseline entry is `X` **or under `X`**. This is the guard that should have
  caught it, and it is one predicate.
- **Report the structure delta at a path that names something.** The sweep knows which
  directories appeared; naming them (or, if that is too costly, emitting the change as a
  non-rollbackable observation) is what makes the receipt honest.
- **Exclude `.git` from the structure walk**, or state why it is in scope. Nothing in the
  blind spot the sweep was built to close (PEP-420 packages, Godot's `res://` scan) lives
  under `.git`, and including it converts ordinary git activity into a breach.

**Discharges when** the live probe reproduces with the tree intact: the empty directory
is detected and fenced, the uncommitted work in the fenced tree **survives**, and the
receipt says what was and was not undone. Reproduction is `/tmp/jr5/emptydir.yaml`
against the two-repo sandbox in § 8.

---

## 3. K2 — **WARN** — a clean tracked file, modified, is typed `created`, and the refusal reason is false

A clean tracked file is absent from `git status` output, so it is absent from the
baseline `entries`. When a phase modifies it, `before_code is None` and
`diff_fingerprints` types it **`created`**:

```
changes  : [('protected/movable.md', 'created', None, ' M')]
rollback : [('protected/movable.md', 'NOT_ROLLED_BACK')]
   reason: REFUSED: reported as created by the phase, but git tracks 1 file(s) under
           it — the path identification is wrong and deleting it would destroy
           committed work
file content after rollback: 'movable\nPHASE WROTE THIS\n'
```

Two things. First, **the destroyer guard is doing real work here** — pre-guard this
path deleted a committed file, and now it does not. That is the guard earning its keep
on a case nobody designed it for, which is the point of defence in depth.

Second, **the reason is false and the outcome is wrong.** The path identification is
exactly right; the *kind* is wrong. The correct action is `git checkout --` (restore),
which never runs, so the file stays modified inside a read-only tree after the abort.
This is the single most likely agentic breach there is — an agent edits a committed
engine source file — and containment does not undo it. It also violates my round-four
§ 5 ruling that a `NOT_ROLLED_BACK` reason must be derived from the failure that
actually occurred.

Fix: type it from existence, not from baseline-dirt membership — a path git tracks, or
that existed at phase start, is `modified`, not `created`. Then the existing
`git checkout --` branch restores it correctly.

---

## 4. K3 — **WARN** — `ls-files` is the index, and the index can be silenced

The prompt asked whether `ls-files` is the right question. It is not.

```
after `git rm --cached protected/committed.md`:
  on disk : True
  in HEAD : protected/committed.md
  ls-files (what the guard asks) : ''
  ls-tree HEAD (what it means)   : 'protected/committed.md\n'

rollback on a `created` change naming protected/ : [('protected', 'deleted')]
  committed.md still on disk? False
```

A staged deletion removes a path from the index while it remains **committed in HEAD
and present on disk**. The guard goes blind and deletes committed content — the exact
outcome it exists to refuse. `assume-unchanged` is a second route to the same silence.

This makes **README rule 7 — "Rollback never deletes tracked content" — false as
stated.** Fix is one line: union `git ls-files` with `git ls-tree -r --name-only HEAD`,
and refuse if either reports. Either question alone is answerable `no` while work is
present; both together are not.

---

## 5. K4 — **WARN** — round four's own dirt-guard fix has zero coverage

I ran a mutation of my own. **M11** reverts the trailing-slash normalisation in
`was_dirty_before` to the exact-string test it replaced — the fix that protects the
engine's 3.3 GB `seasons/` collapsed entry from deletion, prescribed as a J1 WARN and
landed in this round:

```
### M11_exact_string_dirty_check
   247 passed
```

**Nothing goes red.** A safety fix with no falsifying test is a comment. It needs a row:
a collapsed ignored directory that was dirty at phase start must come back
`NOT_ROLLED_BACK`, and the row must fail when the normalisation is removed.

For contrast, **M12** (make the structure sweep inert) turns exactly 1 red — correctly
sized for *detection*, and the reason K1 still shipped is that detection is all the
sweep is tested for.

---

## 6. The lanes

**Agentic lane: BLOCKED on K1.** The lane's whole premise is a model choosing commands
inside a fenced tree. `git add` is a command a disciplined agent runs, and it currently
triggers a repo-wide revert of the tree it was told not to touch. This is not an
adversary story; it is the second time in two rounds that the *more* disciplined git
command is the one that breaks containment.

**Mechanical lane: approval NARROWED.** My round-four grounds were that no filename in
it is model-chosen. K1 is name-independent, so those grounds no longer cover the lane.
The approval that stands is narrower and empirical:

> The three shipped phases of `kc2-baton-mechanical.yaml` are approved as written. They
> create no directories in either read-only tree — verified over four laps this round
> (one run plus a two-lap determinism pass), all PASS, engine and godot dirty counts at
> baseline before and after. `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`
> (`gates/core.py:269`) are load-bearing for that property, not tidiness.

**The approval is void for any mechanical phase that runs a git write-operation in a
read-only tree, or that creates a directory in one.** That is now a property of the
phase list, not of the lane, and it should be re-checked whenever a phase is added.

---

## 7. On the wall — it is still the right mechanism, and it has two gaps

The prompt asked whether round four adjudicates. Measured per kind, residue after
rollback:

| adjudicates (residue non-empty) | vacuous (rollback left nothing) |
|---|---|
| `mode_only_change`, `unreadable_subtree` | the other 11 kinds |

**So round four is live on 2 of 13 rows.** That is not fatal — it is doing exactly what
it should where residue exists, and the eleven vacuous rows are vacuous because the
rollback is clean, which is the good outcome. But two gaps are real:

**(i) The accounting predicate is satisfiable by an over-broad name.** `named` matches
in both directions, so an action naming `.` or `protected` accounts for **every** path
in the tree. K1 passes round four — I ran it:

```
round-4 residue unaccounted : [] -> PASS
round-3 verdict (restored ⇒ path exists) : True
```

A rollback that reverted the entire repo and left the artifact satisfies both rounds.
Round three's `restored` assertion checks only that the path still exists — which is
trivially true of a directory. **The rounds cannot currently distinguish "restored the
artifact" from "reverted the tree."**

**(ii) The structure sweep is not an `ARTIFACT_KIND`.** Its two tests
(`test_an_empty_directory_tree_in_a_READ_ONLY_tree_is_caught_by_the_structure_sweep`,
`…does_not_fire_on_an_unchanged_tree`) stop at `classify()`. It never reaches rounds
three or four. **That is precisely why K1 shipped** — the new measurement surface was
added to the module without being added to the wall. The rule from round three holds
and was not applied here: *a new containment question of this shape should be a new
row.*

The mechanism is not in question. It caught rule 5 unaided, it falsified on all seven
round-four mutations and all five of mine, and M10 falsifies harder than claimed. I am
asking for rows and for two assertions to be tightened, not for a different wall.

---

## 8. Smaller findings

- **K5 — INFO.** Round four adjudicates on 2/13 kinds and its `named` predicate accepts
  ancestors bidirectionally (§ 7i). Tighten: an action may only account for residue it
  names at or **below** itself, and a `restored` action on a directory must assert the
  directory's *contents* returned to the phase-start fingerprint.
- **K6 — INFO.** The structure sweep needs to be an `ARTIFACT_KIND` so it runs all four
  rounds, with the falsification partner planting the same empty tree in the writable
  subtree (§ 7ii).
- **K7 — INFO.** M10's evidence row is wrong: **29 red, not 21**, running it exactly as
  described (flag swap alone, not cumulative). The direction is favourable but a
  mutation table is evidence and must be right.
- **K8 — INFO.** README: *"Five rules keep the claim honest"* sits above **eight** rules.
  Also rule 7's sentence is falsified by K3 and needs the `ls-tree` clause.
- **K9 — INFO.** Non-UTF-8 filenames are refused by APFS, so the strict-decode path in
  `_git` is unreachable **on this host's filesystem**. That is a host property, not a
  code property. Pin it with a test that asserts the refusal, so a network mount or a
  case-sensitive volume does not silently change the answer.
- **F3–F8 (round one), F4 in particular** — still open, still non-gating. Unchanged.

---

## Action

- [ ] **star-lord — K1 (BLOCKING, holds the agentic lane):** refuse `git checkout --` on
      a pathspec that is not a proper subpath (`.`, empty, or any declared repo /
      read-only tree root → `NOT_ROLLED_BACK` with the reason stated); make
      `was_dirty_before` ancestor-aware; report the structure delta at a path that names
      the directories that actually moved; exclude `.git` from the structure walk or
      state why it is in scope. **Discharges when** `/tmp/jr5/emptydir.yaml` reproduces
      with the fenced tree's uncommitted work intact.
- [ ] **star-lord — the wall, four items (land with K1):**
      (a) add `empty_directory_tree` as an `ARTIFACT_KIND` so the structure sweep runs
      all four rounds with its falsification partner;
      (b) tighten round four — an action accounts only for residue at or **below** the
      path it names;
      (c) tighten round three — a `restored` directory must have its contents back at the
      phase-start fingerprint, not merely exist;
      (d) add the row K4 asks for: a collapsed ignored directory dirty at phase start
      comes back `NOT_ROLLED_BACK`, and the row must go red when the trailing-slash
      normalisation is reverted (M11 currently turns nothing red).
- [ ] **star-lord — K2 (WARN, land with K1):** type `created` from existence at phase
      start, not from baseline-dirt membership, so a modified tracked file is `modified`
      and gets restored. The refusal reason must stop asserting a misidentification that
      did not occur.
- [ ] **star-lord — K3 (WARN, land with K1):** union `ls-files` with
      `ls-tree -r --name-only HEAD` in the destroyer guard; correct README rule 7.
- [ ] **star-lord — K7/K8/K9:** non-gating. Correct the M10 row, the "five rules"
      preamble, and pin the filesystem's refusal of non-UTF-8 names.
- [ ] **knight-rider:** G3 (host-quiet window) still owed, unchanged, and now sharper —
      K1 means an unrelated process creating a directory in a read-only tree during a run
      does not merely abort the run, it reverts the tree.
- [ ] **Matt — decision needed: none to hold the block.** K1 is developer-fixable, so it
      stays within my authority per ADR-002. Unchanged and still yours: **O4** (the
      dollars figure) and **D-10** (no HALT status). **Informational:** for the fourth
      round running the defect was not in the code under review — it was in the fix that
      closed the previous round's finding. Round four closed a blind spot I ruled
      non-gating and told star-lord he could simply reword; he closed it instead, and
      closing it introduced the worst-consequence defect of the seven. **That is not an
      argument against closing blind spots.** It is the argument for the rule the module
      already has and did not follow here: every new measurement surface gets a wall row
      before it ships. The review is converging — the parser is now clean under direct
      attack, and the remaining defect is in code that is four hours old.
- [x] **jack-ryan:** J1 discharged, all three faces. Agentic lane **BLOCKED on K1**.
      Mechanical lane approved **narrowly**, for the three shipped phases as written.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py`
  (`:270-315` `_parse_porcelain_z` — J1 closed; `:340-370` `structure_signature` — K1 source;
  `:514-518` the structure Change at tree root — K1; `:631-634` `was_dirty_before` — K1, K4;
  `:707-729` the destroyer guard — K2, K3; `:763` the destructive `git checkout` — K1)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_containment_wall.py`
  (`:229-243` `_names`; `:293-337` round three; `:339-377` round four; `:496-554` the structure sweep, never rolled back)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/README.md`
  ("What 'the tree was clean' is worth" — rule 7 falsified by K3, preamble stale K8)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/runner.py` (`:185-199` structure_roots wiring)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` § 10
- Probe workflow: `/tmp/jr5/emptydir.yaml`; sandbox repos `/tmp/jr5/hub`, `/tmp/jr5/fenced`
- Probe scripts: `/tmp/jr5/probe_wall_gap.py` (K1/K2/K3 and the parser axes), `/tmp/jr5/mutate.py` (M8–M12)
- Probe evidence (in-tree, gitignored) under `factory/sessions/`:
  `jr5-emptydir-20260811T013652Z-05081a/` (**K1 — one empty directory, repo-wide revert, artifact standing**)
  `kc2-baton-mechanical-20260811T014221Z-aa4247/` + the two determinism laps (PASS, EXACT 14/14)

**Post-review state:** `permissions.py` byte-identical to `3a8ca231`; suite **247
passed**. Engine dirty **2789** (0 modified-tracked), godot dirty **233** (1
modified-tracked) — both at baseline. All destructive probes were confined to
`/tmp/jr5/`; the engine and godot blast-radius figures in § 2 were established by
inspection and **not** executed.
