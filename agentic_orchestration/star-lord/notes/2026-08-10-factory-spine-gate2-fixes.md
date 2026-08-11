# FACTORY SPINE v1 — Gate-2 remediation

**Author:** star-lord (builder, ruling D4)
**Date:** 2026-08-10
**Answers:** jack-ryan Gate-2 (`agentic_orchestration/jack-ryan/2026-08-10-factory-spine-gate-2.md`) —
verdict **BLOCK (agentic lane) · APPROVE (mechanical lane)**, findings F1 + F2
**Also lands:** gandalf DRIFT-CRITIC D-3, D-4, D-6, D-7
**Predecessor:** `2026-08-10-factory-spine-landing.md`
**For:** jack-ryan (Gate-2 re-review) · gandalf · Matt

---

## 1. Top line

Both BLOCK findings are closed, plus four DRIFT-CRITIC items. 164 tests green (was
136). The live run still passes and `DETERMINISM: EXACT` still holds.

The F1 fix widened past what either review asked for, because closing the named hole
exposed two more of the same species. Those are § 3 and § 4, flagged rather than
buried — a reviewer who reads only § 2 will have an incomplete picture of what
containment now costs.

| Finding | Owner | Status |
|---|---|---|
| **F1** — fingerprint blind to gitignored writes in every tree | jack-ryan / gandalf D-1 | **CLOSED** |
| **F2** — non-git declared repo fails OPEN | jack-ryan | **CLOSED** |
| **D-3** — `verdict_consistent` greens vacuously anywhere but last | gandalf | **CLOSED** |
| **D-4** — `report.py` hard-codes the dollars caveat | gandalf | **CLOSED** |
| **D-6** — closed harness lane discovered mid-run | gandalf | **CLOSED** |
| **D-7** — a red phase's notes travel unlabelled | gandalf | **CLOSED** |
| **O4** — drop vs. keep the dollars figure | gandalf ⟷ jack-ryan **disagree** | **SURFACED to Matt** (§ 6) |
| **D-2** — mechanical phases need a phase-level `exec:` | gandalf | queued |
| **D-10** — no HALT status | gandalf | queued, § 6 |

## 2. F1 and F2 — what changed

**F1.** The exemption was a CATEGORY ("anything git ignores") applied to fix a
NAMED problem (the factory's own `sessions/` writes reading as self-breach). That
category covered the engine's `seasons/` (3.3 GB) and `telemetry.db` (450 MB) —
inside the tree the workflow declares read-only. jack-ryan proved it with a live
run; the file survived and the run went green.

The exemption is now six named paths (`FACTORY_RUNTIME_PATHS`), root-repo only.
Everything else git ignores is measured like anything else. `git status` is called
with `--ignored=traditional`, and the collapsed directory entries are swept
recursively.

The test that pinned the hole as the requirement (`test_permissions.py:211`) is
inverted into its falsification partner: **a gitignored write must now breach.**
Four more hold the line from the other sides — the exemption does not apply to
non-root repos, does not cover factory *source* under the same directory, is
recorded on the fingerprint when taken (`exempted`), and fails CLOSED when git
collapses an untracked ancestor above an exempt path.

**F2.** A declared repo that is not a git worktree produced `is_git=False`,
recorded honestly and then never read — so the diff came back empty and empty read
as innocent. Two halves:

- **Load time:** every `repos:` entry must exist and be a git worktree, or the
  workflow does not load. Also: every `read_only_trees:` entry must be covered by
  some `repos:` entry, because a read-only tree that nothing fingerprints is a
  promise nobody checks. (The shipped KC2 workflow already satisfied this by
  convention; it is now a rule, with a test that asserts it against the real file.)
- **Mid-run:** `TreeFingerprint.usable` is consulted, and `diff_fingerprints`
  raises `ContainmentError` rather than returning `[]`. "Nothing moved" and "we do
  not know" no longer share a return value.

## 3. What closing F1 exposed — the interpreter writes too

With gitignored paths visible, running the engine's pytest wall inside the
declared-read-only engine tree writes `__pycache__/` there. That is a real write to
a read-only tree, and containment correctly called it.

The fix is to stop the write, not to re-exempt the path: `PYTHONDONTWRITEBYTECODE=1`
and `PYTEST_ADDOPTS=-p no:cacheprovider` in the gate subprocess environment. A
read-only claim that quietly tolerates one class of write is not a read-only claim.

Verified after the run: zero `__pycache__` writes in the engine tree.

**This is the shape of the original defect, one layer down.** The tempting fix was
another exemption. Naming it here because the next person to hit a false breach
will be tempted the same way, and the tell is identical: an exemption proposed to
make a red go away rather than to describe something true.

## 4. What closing F1 cost — and the honest limit of the claim

Measuring what was previously exempt is not free. The godot tree's `.godot/` +
`Assets/Synty/` hold **259,000 files**: ~12 s to stat-sweep, nine fingerprints per
run. That is longer than the run.

So measurement now has **two declared tiers**:

- **EXACT** — every file stat'd. Catches creation, deletion, in-place edits.
- **COARSE** — directory mtimes + entry counts (905 dirs, 0.12 s for the same
  region). Catches creation, deletion, rename. **Does NOT catch an in-place rewrite
  of an existing file.**

A region over 50,000 files falls back to COARSE. Every phase emits a
`containment_coarse` receipt naming the regions and the caveat verbatim, so a later
reading of "the read-only tree was clean" carries the strength of the claim with it.

The blind spot is pinned by a test that asserts coarse measurement **fails** to see
an in-place edit. If a future change makes it see one, that test reds and the
caveat can be weakened *on evidence*.

**Run cost:** 1m26s (was ~30 s pre-fix, and 2m36s in the first version of this fix,
which spent 50,000 stats per oversized region learning something the cheap pass
answers for free). Determinism unaffected: `DETERMINISM: EXACT — 14 gate verdicts
identical across two laps`.

**Where I want a reviewer's eye:** COARSE is a genuinely weaker claim than the
spine advertised, and I chose it over both alternatives (12 s × 9 per run, or
leaving the region unmeasured). It is labelled everywhere it appears, but a label
is not the same as coverage. If the founding run's threat model includes an agent
rewriting a file in place inside `.godot/`, this tier is not sufficient and the
answer is to declare a narrower read-only tree rather than to trust the label.

## 5. The four DRIFT-CRITIC items

- **D-3.** `verdict_consistent` adjudicates the reports that ran BEFORE it, so
  anywhere but last it greens over gates it never saw. Now a load error naming its
  position.
- **D-4.** `report.py` hard-coded the subscription caveat into the totals line —
  the number and its meaning joined by the renderer's assumption rather than by the
  receipt. It now READS `dollars_sources` from the DB. An unregistered source
  prints raw with "no gloss registered"; a figure with no recorded provenance
  renders as **"provenance unrecorded; this figure cannot be read as money spent"**
  and is explicitly forbidden from inheriting the subscription caveat (asserted).
- **D-6.** A closed harness lane (Codex, blocked on **T16**) now fails at LOAD,
  naming the blocker — not after the phases ahead of it have burned.
- **D-7.** `notes_for_next_agent` from a phase that went red read identically to
  notes from one that passed. Now prefixed with the phase name, its status, and
  *"treat them as a lead, not as an established result."* The notes still travel —
  this is a label, not a filter. Empty notes stay empty.

## 6. What I did NOT decide, and why

**O4 — the dollars figure.** gandalf ruled **DROP** it (recomputable from tokens +
model + price table; the $0.0672 corresponds to no artifact). jack-ryan explicitly
**disagreed** and would keep it as shipped. Two seam stewards, opposite rulings, both
reasoned.

I implemented neither. D-4 is done either way — the figure is now labelled *from the
receipt*, so if it stays it cannot be read as money spent, and if it goes the
renderer needs no change. **This is Matt's call**, and it is cheap in both
directions right now; it gets expensive once a surface renders it.

**D-10 — no HALT status.** gandalf calls this the largest gap for the founding run.
A phase can PASS, FAIL, or the run can ABORT on a breach. There is no way for an
agent to stop and say *"the premise is wrong, do not retry me, get a human"* — which
is exactly the KC2 halt that made the last run trustworthy. Retrying an agent whose
premise is wrong is how a factory manufactures confident garbage. I did not add it
in this pass because it is a new status in the receipts schema (SCHEMA_VERSION bump
+ MIGRATION note) and a new envelope field in the synced triad — that is a design
decision about the run protocol, not a defect fix, and it wants a dispatch.

**D-2 — phase-level `exec:` for mechanical cells.** Queued. Mechanical work
currently rides inside a gate command, which is what created the double-fingerprint
hole recorded in the landing note. Same reasoning: a shape change, not a fix.

## 7. Acceptance, restated

| # | Spec A § 11 item | Status |
|---|---|---|
| 1 | Baton-scene mechanical cells run end-to-end | **PROVEN** — 3 phases, 14 verdicts, all green |
| 2 | Determinism assertion | **PROVEN** — `DETERMINISM: EXACT` |
| 3 | Zero stub gates (grep-provable) | **PROVEN** — 3 independent proofs |
| 4 | Synced-triad green; breach ⇒ rollback + abort | **PROVEN** — and containment now measures what it claims to |
| 5 | jack-ryan Gate-2 PASS | **RE-SUBMITTED** — F1 + F2 closed |

164 tests. Scope: meta-repo writes only; engine and godot trees read and executed,
never written (verified post-run).

---

## 8. Round two — the re-review findings (added after `d68a4072`)

jack-ryan re-reviewed and returned **BLOCK LIFTED, conditionally**: F1 and F2 closed
(he re-ran his original probe and three harder variants; the engine tree fingerprints
with **zero coarse regions**, so `seasons/` and `telemetry.db` — the assets that
earned the BLOCK — are EXACT-measured). D-3/D-4/D-6/D-7 verified behaviourally, not
taken on my word.

He then found three more, one BLOCK-class **inside my own F2 fix**:

- **G1 (BLOCK-class) — CLOSED.** `_is_git_worktree` checked only the return code of
  `git rev-parse --show-toplevel`, which succeeds from *any* depth inside a worktree.
  So a subdirectory declared as a repo passed the new guard, fingerprinted
  `usable=True`, and joined 2,907 worktree-root-relative paths against the wrong base
  — every signature empty, the tree permanently clean. He proved it live; the planted
  file survived and he had to delete it by hand. Worse, the F2 error text I wrote
  ("Declare it in `repos` as well") walked an author straight into it.

  Now the toplevel is *compared* to the declared path, at both layers: the loader
  refuses with an error naming the worktree root to declare instead, and
  `fingerprint()` itself returns an unusable snapshot if it is not at a worktree root
  — because the loader is not the only caller. Re-ran his probe: **refused at load,
  the phase never executed, nothing planted.**

- **G2 (WARN) — CLOSED.** `classify()` matched read-only trees against
  `change.root`, which is always a whole repo root — so a read-only tree declared as
  a *subdirectory* was accepted at LOAD and enforced nowhere. And my own
  `test_a_read_only_tree_nested_inside_a_declared_repo_is_accepted` pinned that:
  it asserted the loader said yes without checking the yes meant anything. **Second
  instance of the Discipline #12 pattern in this module, and the second time my test
  suite defended a hole.** Matching is now by full path, both directions (a collapsed
  ancestor entry overlapping a read-only subtree fails closed). Live-proven: a write
  into a nested read-only tree breaches and rolls back even under `writes: ["**"]`.

- **G3 (WARN) — DIAGNOSED, not fixed.** A **read-only** SQLite open on the engine's
  `telemetry.db` creates `-wal`/`-shm` sidecars that outlive the process. During his
  review, an out-of-band query from his own session aborted *both* determinism laps
  and flipped EXACT → DIFFERS. This is fail-closed and, strictly, correct: the
  factory measures the TREE, not its own actions, so another agent's read is
  indistinguishable from this phase writing there.

  I did not exempt the sidecars — that is § 3's defect again. Breaches matching
  co-tenancy signatures (`-wal`, `-shm`, `-journal`, `.lock`, `~`, `.DS_Store`) are
  now **labelled** in the abort reason, in a `co_tenancy_suspected` receipt, and in
  `BREACH.json` with a note explaining the mechanism. The run still aborts. The point
  is that the diagnosis is in the receipt, because on a 10-agent host this will look
  like a containment defect when it is a co-tenancy problem.

  **This one is not closed and Matt should know it exists**: the founding run can die
  from another agent merely reading an engine DB. The real fix is host discipline
  during a run, not code.

Also closed from his INFO findings: **G4** (the coarse caveat was emitted from the
`before` snapshot only — now every snapshot, deduped per phase, so a region that
crosses the cap *during* a phase is declared); **G6** (`onerror=lambda _: None`
silently skipped unreadable subtrees, so a directory that became unreadable between
snapshots read as unchanged — the failure is now folded into the signature, so
readability itself is measured); **G7** (a dead `untracked_files` parameter costing
27 `git ls-files` subprocesses per run — removed).

**G5 remains open** (misleading rollback reason on collapsed-directory breaches).

Round-two evidence: **170 tests** green; run PASS in 1m15s; `DETERMINISM: EXACT —
14 gate verdicts identical across two laps`; engine and godot dirty-counts unchanged
at 2789 / 233.

**His condition:** the agentic lane is authorized for workflows declaring **whole git
repositories**. G1's fix now enforces that mechanically at load, which was his stated
requirement for lifting the subdirectory restriction — but the verdict is his to
restate, not mine to assume.

---

## 9. Round three — jack-ryan stopped reviewing instances and named the pattern

He restated the verdict and, in the same pass, found H1: **BLOCK-class, inside the fix
I had just shipped for G2.** `_read_only_hit` called `.resolve()`, which follows
symlinks — so for a link planted *inside* a read-only tree the predicate answered a
question about where the link **pointed** instead of where the link **was**. Live,
against the real engine tree with `read_only_trees: [engine]`, a link to `/tmp`
resolved cleanly out of the fence and the phase came back PASS. His control with
`touch` instead of `ln -sfn` breached correctly, which isolated the cause to
`.resolve()` and nothing else. There were zero symlink tests in the suite.

Two companions: **H2** — a *nonexistent* `read_only_trees` entry loaded clean and
fenced nothing (F2's own sentence applied to the half that never got the existence
check). **H3** — rollback could not unlink a symlink: `is_dir()` is true for a link to
a directory and `rmtree` refuses it outright, `exists()` is false for a broken link so
the unlink never fired, and the receipt printed `deleted` over a surviving artifact.

### The finding that matters more than the four defects

> F1 measured the wrong **category**. G1 the wrong **base**. G2 the wrong
> **granularity**. H1 the wrong **target**. Four containment predicates that answer a
> slightly different question than the one asked — and every one of their wrong
> answers is `clean`. Three of the four were pinned in place by a **passing test
> asserting the reduced behaviour was the requirement.**

He has now found one per round for three consecutive rounds in the same file, and his
conclusion is the one I should have reached myself: **instance-by-instance review is
not converging, and a fifth patch is not the answer.** His prescription was one
parametrised falsification wall over the artifact kinds a phase can actually produce.

I built it: `tests/test_containment_wall.py`. Eight artifact kinds (regular file,
symlink pointing out of the tree, broken symlink, nested dir, collapsed untracked
member, gitignored file, nested git repo, unreadable subtree) × four rounds — the
change must be **detected**, **fenced** under `writes: ["**"]`, and **honestly
reported** by the rollback; and the falsification partner requires the identical
artifact in an allowlisted directory to come back **allowed**, so a `classify` that
breached unconditionally cannot pass the wall. Adding an artifact kind is adding a
row. That is the point: the next containment question of this shape should be
answerable by a row rather than by a fourth reviewer finding it live.

**The wall found a fifth defect on its first run, before a reviewer did.** An
unreadable subtree is invisible to the change-set: `git status` writes
`warning: could not open directory 'x/': Permission denied` **to stderr**, exits **0**,
and prints **nothing to stdout**. A phase that creates a directory and chmods it 000
therefore measured as untouched. Same shape as the other four, on a new axis — the
wrong **channel**. The warned paths are now folded into the fingerprint as entries, so
unreadable-at-both-ends is unchanged (no false breach from a pre-existing host
condition) and unreadable-at-one-end is a change, which is the truth.

### The rollback contract, corrected

My first draft of the wall's third round asserted the artifact is always removed. That
is not the contract and should not be: the module's standing safety rule is that
nothing is deleted unquarantined, so an artifact that cannot be safely quarantined is
deliberately **left as evidence**. The run aborts either way. What must never happen is
the third state — the artifact survives *and* the receipt says `deleted`, so the abort
report reads as if the tree came back clean. The wall now asserts that the receipt and
the disk agree, which is the honest contract.

### One blind spot declared rather than found

Discovered by accident when a malformed probe of my own scattered empty directories:
**git cannot see a wholly-empty directory tree at any porcelain setting**, because it
tracks content, not structure. The stat sweep cannot rescue it either — the sweep only
descends into paths git already reported, which is the design that keeps the engine's
3.3 GB affordable. Residual risk is bounded to directory *structure*: the moment any
file lands anywhere inside such a tree, git reports the collapsed entry and the fence
catches it. Pinned as a failing-if-fixed test alongside the COARSE tier's in-place-edit
blind spot, so it is declared rather than discovered.

### Status after round three

| finding | status |
|---|---|
| H1 symlink target vs location | CLOSED — matched on lexical **and** resolved form, breach on either |
| H2 nonexistent read-only tree | CLOSED — refused at load, with the typo named as the likely cause |
| H3 rollback cannot unlink a link | CLOSED — `is_symlink()` first; quarantine records the link and its target without following it |
| (new) unreadable subtree on stderr | CLOSED — warned paths folded into the fingerprint |
| G3 host co-tenancy | **OPEN, for Matt.** jack-ryan ruled diagnose-don't-exempt correct and non-blocking (it fails *closed*), and routed it to knight-rider as a **host-quiet operating precondition** for the founding run, not a patch |
| G5 misleading rollback reason | OPEN — ruled non-blocking; detection and abort are the load-bearing half |
| empty directory trees | DECLARED blind spot, pinned |

Round-three evidence: **207 tests** green (was 170); run PASS in 1m23s;
`DETERMINISM: EXACT — 14 gate verdicts identical across two laps`; engine and godot
dirty-counts unchanged at 2789 / 233. jack-ryan's H1 probe reproduced live: the symlink
breaches, the rollback unlinks it, the engine returns to baseline. The
unreadable-subtree probe reproduced live: detected, fenced, and left on disk with a
stated reason rather than a false `deleted`.

**The lane, per his verdict:** mechanical approved unchanged; agentic authorized for
whole-repository workflows, **excluding any phase whose `writes` pattern covers a
declared read-only tree** — the exclusion lifting on H1, which is now closed. That lift
is his to confirm, not mine to assume.

---

## 10. Round four — the wall audit, and the worst defect of the six

jack-ryan did not re-review the instances this round. He audited **the wall itself**,
and found J1 in the one line the wall was built to make unnecessary:

```python
rest.split(" -> ")[-1].strip().strip('"')
```

Porcelain v1 C-quotes any path with a special character, and uses ` -> ` as its rename
separator — a delimiter a filename can legally contain. Keeping only the last field
gave the defect three faces, and the third is worse than anything in F/G/H:

- **J1(a) — the rename SOURCE is dropped.** `git mv` a file *out of* a fenced tree and
  the change-set named only the legal destination. Live, before the fix: `PASS`, with a
  **zero-path change-set**, while `src/canon.md` was gone from a declared read-only
  tree. Same shape as the other five — the wrong **parse**, whose wrong answer is
  `clean`.
- **J1(b) — a quoted path is judged unquoted.** The fence is matched on a string git
  never meant literally.
- **J1(c) — containment deletes real work.** A phase legally creating a file named
  `junk -> src` parsed to `src` — a real, tracked path — which the rollback then
  **deleted**. The safety machinery destroying committed content is a strictly worse
  outcome than the breach it exists to prevent.

### The wall had the module's own disease

His finding, and it is the correct one: the wall's round one asserted `assert changes`
— **non-emptiness only**. Both J1 escapes satisfy that. The one assertion built to cure
"a predicate answering a slightly different question" was itself answering a slightly
different question. Round one now asserts the change-set **names** the artifact
(`_names()`, matching a path or any collapsed ancestor of it). He also required a
fourth round I did not have: after rollback, **every residue on disk must be named by
some action** — the receipt cannot be silent about what it left behind.

### What changed

1. **`git status --porcelain -z --ignored=traditional`.** NUL-separated, never quoted,
   and the rename origin arrives as its own record. Parsed by `_parse_porcelain_z`,
   which emits the origin under a distinct `R<` code.
2. **A rename source is a deletion, not a creation.** Load-bearing: `created` is the one
   change kind the rollback *deletes*. Mis-typing an origin as a creation would have the
   rollback delete the file the rename moved away from.
3. **The destroyer guard.** A `created` path cannot contain anything git already tracks.
   If `git ls-files` reports content under it, the path identification is wrong; the
   deletion is **refused with a reason** and the artifact is left standing. This does not
   depend on knowing which parse bug produced the bad path — it is the standing answer
   to the whole class. Containment must never be the thing that destroys work.
4. **Five new artifact kinds** on the wall: a quoted path containing the rename
   delimiter, a path with a newline, a hard link, a mode-only change, a directory
   replacing a file. Thirteen kinds × four rounds, each with its allowed-where-declared
   falsification partner.

### The empty-directory blind spot — closed, not reworded

He ruled it "amend the wording, non-gating," and corrected two things in my round-three
reasoning: my affordability argument conflated the **exact** sweep with a
**structure-only** sweep (he measured it: 0.21 s engine, 1.69 s godot), and "bounded to
structure" is **not inert** — a bare directory is a PEP-420 namespace package, a new
`res://` directory enters Godot's import scan, and the residue accumulates across runs.

I closed it instead of rewording it. `structure_signature()` is a names-only walk — no
stats — swept over the declared read-only trees and diffed like any other entry.
Grounds: **"bounded and low-harm" has now been the wrong answer three times in this
module.** The cost is declared, not hidden: the founding-run workflow went 1m23s →
**1m42s**.

### Evidence that the wall falsifies

Mutation testing, each applied and reverted in isolation:

| mutation | tests red |
|---|---|
| M8 — drop the rename origin record | 1 |
| M9 — remove the destroyer guard | 1 |
| M10 — revert `-z` to porcelain v1 (alone, not cumulative) | ~~21~~ **29** (corrected round five, K7) |

jack-ryan's own M1–M7 all red it too, including M7 (over-widen the fence → 8 fails, via
the `can_go_green` partners — the partners are what make it a wall and not a ratchet).

Live, after the fix: the J1(a) rename escape **aborts**, naming
`src/canon.md (deleted)`, where it previously ran PASS on a zero-path change-set. The
J1(c) induced-deletion probe **passes legally**, `src/` intact, the tricky path parsed
correctly as `scratch/junk -> src`.

### Status after round four

| finding | status |
|---|---|
| J1(a) rename source dropped | CLOSED — `-z`, origin emitted as its own record, typed as a deletion |
| J1(b) quoted path judged unquoted | CLOSED — `-z` output is never C-quoted |
| J1(c) rollback deletes real work | CLOSED — refuses to delete any path git tracks content under |
| the wall's round one | CLOSED — names the artifact; residue-accounting round added |
| empty directory trees | **CLOSED** — structure-only sweep on the read-only trees (was: declared blind spot) |
| G3 host co-tenancy | OPEN, for Matt — host-quiet operating precondition, knight-rider routes |
| G5 misleading rollback reason on collapsed-directory breaches | OPEN — ruled non-blocking |
| COARSE tier in-place-edit blindness | DECLARED, pinned by a failing-if-fixed test |

Round-four evidence: **247 tests** green (was 207); run PASS in 1m42s;
`DETERMINISM: EXACT — 14 gate verdicts identical across two laps`; engine and godot
dirty-counts at baseline **2789 / 233** after every probe.

**The lane, per his round-four verdict:** H1/H2/H3 discharged and the read-only-overlap
exclusion discharged; **agentic lane BLOCKED on J1**; mechanical lane approved unchanged
— *"every filename in it is human-authored, which is precisely why J1 is unreachable
there, and that property now needs writing down."* So, written down here: **the
mechanical lane's immunity to J1 is a property of its inputs, not of its code.** Every
path a mechanical workflow touches is authored by a human in a YAML file under review.
The moment a phase's paths come from a model's output, that immunity is gone — which is
exactly the boundary the agentic lane crosses, and exactly why J1 had to be closed in
the parser rather than assumed away by the lane.

The J1 lift is his to confirm, not mine to assume.

---

## 11. Round five — J1 lifted, and the seventh defect was in the sixth's fix

He lifted J1 on all three faces, verified live through the shipped CLI rather than
accepted from my table. He also audited the *other* thing round four added, and found
**K1 — the worst-consequence defect of the seven.**

> The structure sweep returned `dirs:<n>:<hash>`. A hash can say that something moved
> and nothing about what, so the diff reported the change at the **tree root** — and
> `rollback` handed that string to `git checkout --` as a **pathspec**. One empty
> directory inside a fenced tree therefore induced a repo-wide `git checkout -- .`,
> destroying every uncommitted modification to every tracked file in that repo, while
> the directory that caused the breach was **left standing**. The receipt word was
> `restored`.

Same family, seventh instance, one mutation: **the wrong answer is no longer `clean`,
it is `restored`.** The same disease presenting as a cure. And it did not need a
filename, so round four's "the mechanical lane's inputs are human-authored" reasoning
did not reach it — he narrowed that approval accordingly, and he was right to.

Neither existing guard fired. The destroyer guard is scoped to `created` and a
structure change is `modified`; `was_dirty_before` was an exact-string membership
test, so a change at an *ancestor* of the dirty paths bypassed the one protection that
exists for exactly this case. And the trigger is ordinary: the sweep walked `.git`
(281 of the engine's 968 directories), so a plain `git add` moved the signature.
**The more disciplined git command was again the one that broke containment.**

### What changed

| K | fix |
|---|---|
| **K1** | the sweep returns the directory SET, so the diff names the directory that moved; the rollback REFUSES any pathspec naming a whole tree (`.`, empty, any declared repo or read-only root); `was_dirty_before` is ancestor-aware in both directions; `.git` is excluded from the walk |
| **K2** | the kind of a path absent from the baseline is read from git's own status code, not from absence. `??`/`!!`/`A` are creations; everything else git already knew about, so a modified tracked file is `modified` and gets **restored** |
| **K3** | the destroyer guard unions `git ls-files` with `git ls-tree -r HEAD`. The index can be silenced (`git rm --cached`) while the content is still committed and on disk — README rule 7 was false as stated |
| **K4** | round four's own trailing-slash fix had zero coverage; it now has a row that asserts the survival happens **for the dirt guard's reason**, not by accident |
| **K5** | round four accounts only for residue at or **below** the path an action names; the predicate now has ONE definition shared by the round and its falsifier |
| **K6** | `empty_directory_tree` is an `ARTIFACT_KIND` — all four rounds, with its allowed-where-declared partner |
| **K7/K8/K9** | M10 corrected to 29; README preamble corrected; the filesystem's refusal of non-UTF-8 names pinned as a HOST property |

### The rule that was already written down and not followed

Round three's own prescription: *a new containment question of this shape should be a
new row.* The structure sweep was a **new measurement surface** added with detection
tests only. It never reached rounds three or four — which is precisely where its defect
lived. That is now stated in the README as a standing rule, not as a lesson.

### Evidence

Seven mutations, each applied and reverted in isolation, **all red**:

| mutation | reverts | red |
|---|---|---|
| M13 | the sweep names the tree again | 1 |
| M14 | the whole-tree pathspec guard | 1 |
| M15 | absence-from-baseline means `created` again | 1 |
| M16 | destroyer guard asks only the index | 1 |
| M17 | dirt guard back to exact-string | 1 |
| M18 | `.git` back in the structure walk | 1 |
| M19 | round four's accounting reads both directions | 1 |

Two of those seven (M18, M19) were **green on the first attempt** — my rows were
measuring the wrong thing. M18's row swept a *subdirectory*, which never contains
`.git`, so it could not have caught the trigger it was named for; the shipped read-only
trees are worktree roots, and the row now sweeps the root. M19's row had its own copy
of round four's predicate, so mutating the round left the falsifier untouched — two
copies of a predicate is one copy that can drift out from under its own test. Both are
the wall's disease again, caught by mutation instead of by a reviewer. That is the
mechanism working.

Live, through the shipped CLI, on jack-ryan's own reproduction shape: the empty
directory is **named** (`newdir (created)`), fenced, and **deleted**, and the fenced
repo's two uncommitted files **survive** — the exact inversion of his § 2 transcript.
K2 live: `src/canon.md (modified) → restored`, tree clean, the agent's edit gone. K3
live: with the index silenced, `ls-files` reports nothing, `ls-tree HEAD` reports two,
the guard refuses and both committed files survive.

### An unplanned live G3 event

The first founding-run lap this round **aborted** on
`agentic_orchestration/gandalf/notes/…-charter.md (committed)` — because gandalf
committed to the meta-repo at 22:25:35 while the run was in phase 3. Nobody staged
this. The containment detected another agent's concurrent write, **refused to unwind
history** ("unwinding history is a human decision"), and aborted the run. It failed
closed, which is the correct behaviour and the first live confirmation that G3 is a
real operating condition rather than a theoretical one. It is also the sharpest
argument yet for the host-quiet window knight-rider owns: the run cost 90 s and died
for a reason that had nothing to do with the work.

One honest defect in that receipt, worth logging: the reason read *"the phase committed
this path"*, and the phase did not — gandalf did. Same family as G5 (a reason derived
from the branch taken rather than from the failure that occurred). Non-gating, and now
it has a real instance rather than a hypothetical one.

### Status after round five

| finding | status |
|---|---|
| J1(a)(b)(c) | **DISCHARGED by jack-ryan**, verified live through the CLI |
| K1 structure sweep → repo-wide revert | CLOSED — names the directory; whole-tree pathspec refused; dirt guard ancestor-aware; `.git` excluded |
| K2 clean tracked file typed `created` | CLOSED — kind read from the status code; restored |
| K3 `ls-files` is only the index | CLOSED — unioned with `ls-tree -r HEAD`; README rule 7 corrected |
| K4 dirt-guard fix had no falsifier | CLOSED — row asserts the refusal's REASON |
| K5 round four's accounting predicate | CLOSED — at-or-below only, one shared definition |
| K6 sweep was not an artifact kind | CLOSED — `empty_directory_tree`, four rounds, partner |
| K7 / K8 / K9 | CLOSED — M10 = 29; README preamble; non-UTF-8 pinned as a host property |
| G3 host co-tenancy | OPEN, knight-rider routes — **and now observed live** |
| G5 rollback reason derived from the branch, not the failure | OPEN, non-blocking — new instance logged above |
| COARSE tier in-place-edit blindness | DECLARED, pinned |

Round-five evidence: **262 tests** green (was 247); founding run PASS in 1m43s;
`DETERMINISM: EXACT — 14 gate verdicts identical across two laps`; engine **2789** /
godot **233** at baseline before and after every probe; all destructive probes confined
to `/tmp/sl5`.

---

**Signed:** star-lord — operational-pipeline seam (export · output · telemetry · LLM)

---

## 12. Round six — the fixes were green, and the mutation table said they were comments

Round six's verdict (`2026-08-10-factory-spine-gate-2-round-six.md`) landed seven
findings, L1–L7. I implemented all of them, the suite went from 262 to 362 green, and
jack-ryan's two named discharge criteria both passed live. Under the process as
written, that is the point at which I return for the block lift.

I ran the mutation harness first — revert each fix in the shipped module, run the
suite, restore — because round five had taught me that two of seven wall rows were
measuring the wrong thing. **All seven mutations came back GREEN.** Every fix I had
just shipped could be deleted without a single test noticing.

That table, not the verdict, is what round six actually produced.

### 12.1 What the seven survivors were hiding

**M20 — L1's own wall row was blind.** The row plants a file named `:(top)`, which is
the name jack-ryan's reproduction uses. But an *untracked* `:(top)` is classified
`created`, and a created path is rolled back with `unlink` — the name never reaches
git at all. The magic only bites through `git checkout --`, which requires the file to
be **tracked and dirty**. Right name, wrong state. Proven by running jack-ryan's
`test_jr6_shape.py` and my ten `pathspec_magic` rows against the same mutant: his RED,
mine all green. `:(top)` is now seeded into the baseline commit and the planter
modifies it; M20 now REDs, and only in the `read_only_worktree_root` shape, which is
exactly the positional-magic claim the row's docstring makes.

**M21/M22 — "the closed enumeration" was not one.** My L2 fix was character-class
control flow (`x in "ARC"`, `x == "D" or y == "D"`) under a docstring asserting
closure. A hand-written table of what each porcelain code *means*, written against the
spec rather than against the code, found the gap immediately: 29 unlisted codes were
being given confident answers, and `AD`/`RD`/`CD` — staged, then removed from disk —
came back `created` because `A` was tested before `D`. It is now a literal dict, so
closure is a property of the data structure rather than of my care in ordering `if`s.

**M23b/M23c — L2 is not a rename bug. It is the whole `X≠' '` column.** This is the
round's real finding and it came out of asking why M21 didn't red. `git checkout --`
restores from the *index*. L2 was closed by re-typing the one status code jack-ryan's
`git mv` happened to produce — but the property has nothing to do with renames. It
holds for every code whose X column is non-space, **including `M `: an ordinary edit
of a tracked file that the phase then staged.** Verified live before writing any fix:

| the phase does | receipt | on disk after rollback |
|---|---|---|
| edit a tracked file, `git add` | `restored` | **the phase's content** |
| edit a tracked file, no `git add` | `restored` | the baseline |

Staging moves the phase's work into the place containment reads as the baseline. So
the rule is now stated once and covers all four staging shapes: **containment does not
restore staged work — it refuses, names the index, and prints the recovery command.**
Editing the index of a fenced tree is a human decision. That was already the answer
for staged creations (the destroyer guard) and staged deletions; it is now the answer
for staged modifications and renames too, which makes `git checkout --` provably
correct in the only case it is still used. The unstaged row is in the wall as the
discrimination partner, so a future fix cannot satisfy this by refusing everything.

This is the fourth round running in which the more disciplined git command is handled
worst, and the reason is now structural rather than coincidental.

**M23 — a refusal's reason was never checked for truth.** Round three asserted a
`NOT_ROLLED_BACK` carries *a* reason. L3 was a refusal carrying a perfectly good
non-empty reason whose every clause was false, so "has a reason" is the weaker
question. Refusal claims are now re-derived from git and compared. My first version
checked the arithmetic — and M23 survived it, because collapsing the three-way branch
produces "HEAD holds **0** file(s) under it — the path identification is wrong", which
is numerically true and completely false. A count is not a claim: a refusal that
justifies itself by what HEAD holds must have HEAD holding something, and an
index-only case must say `index`.

**M26/M27 — L5 and L6 shipped with no test at all.** Not a subtle row; no row.

### 12.2 The limit of the wall, stated

M22's mutation changes the answer for 41 status codes and leaves every wall row green.
That is not a gap in the rows — it is structural. **The wall plants artifacts, so it
can only reach codes git actually emits, and a default-fail branch is by definition
the branch taken by codes nobody has seen yet.** A default-fail is a claim about
inputs that have not happened; it is tested by the alphabet, not by an artifact. Those
tests now live in `test_permissions.py` and iterate the whole two-character space.

Knowing which predicates the wall cannot reach is now part of the wall's own
documentation, because the alternative is a growing table that reads as if it covers
everything.

### 12.3 The process item, owed a third time — and why compliance was cosmetic

jack-ryan's round-six action list named one process change: *"a new predicate gets its
wall row, in the shipped shape, before it ships."* I complied with it literally. I
added rows for every new predicate, in the shipped shape, before shipping. Seven of
them were inert.

So the rule as written is not sufficient, and I would amend it:

> **A new predicate's row must be shown to RED with the fix reverted, before it
> ships.** A row that has never been observed to fail is a claim about the code that
> nobody has tested — which is the exact object this review has been finding for six
> rounds, relocated into the test file.

Mutation is cheap here: the harness is 60 lines and a full pass is ten minutes. I am
treating it as a gate on my own work from this point rather than as an audit I run
when I happen to be suspicious, and I would rather it were a standing requirement than
a habit of mine.

### 12.4 Round-six evidence

- **398 tests green**, from 262 at the start of the round.
- **19 artifact kinds × 2 fixture shapes × 4 rounds**, plus an uncommitted-work canary
  asserted on every one.
- **8 code mutations, all RED; 2 controls behaving as controls.** First pass: 7 of 7
  green. Final pass: 0 survivors.
- Every finding reproduced RED against the shipped module before being fixed, and the
  general L2 case verified live against real git repositories in four scenarios.

| item | state |
|---|---|
| L1 pathspec magic (three faces) | CLOSED — `GIT_LITERAL_PATHSPECS=1`; row reseated as a tracked modification; M20 REDs |
| L2 rename destination | CLOSED — literal dict; `R `/`C ` typed `created` |
| L2 **general** (mine, from the table) | CLOSED — the staging guard; whole `X≠' '` column; live-verified |
| L3 three-way refusal reason | CLOSED — claims re-derived from git and checked for truth, not arithmetic |
| L4 wall (four items) | CLOSED — two shapes, canary, real `before`, staged kinds |
| L5 shell metacharacters | CLOSED — `not_runnable`; 8 rejection rows + 4 quoted-form partners |
| L6 refusals unsurfaced | CLOSED — `containment_not_undone` receipt, asserted from the receipts DB |
| L7 README | CLOSED — 15 rules; rules 7/10 now cite rule 12; counts corrected |
| G3 host co-tenancy | OPEN, knight-rider routes |
| G5 rollback reason derived from the branch | OPEN, non-blocking |
| COARSE tier in-place-edit blindness | DECLARED, pinned |

**For Matt, unchanged from round five:** O4 (the dollars figure — gandalf DROP vs
jack-ryan KEEP) and D-10 (no HALT status) are still open decisions.

**For Matt, new:** jack-ryan observed that for the fifth round running the defect was
not in the code under review but in the fix that closed the previous round's finding,
and framed it as evidence the review is descending a real gradient rather than as
evidence the fixes are bad. Round six is the sixth, and I think the framing holds —
K1 fired on `git add`; L1 needs a file named `:(top)` at a tree root; the general L2
case needs the agent to be *well-behaved*. But the gradient is in the findings, not in
my process, and § 12.3 is the process change I am proposing as a result.

---

## 13. Round seven — the guard asked git, and the one change git never named walked past it

Round six closed L2 by reading the porcelain status code. jack-ryan's round-seven
Gate-2 verdict was **HOLD**, on a finding that is the same shape one level down.

### 13.1 L8 — a synthetic status routes around the staging guard

`diff_fingerprints` emits structure-sweep rows with `after_status="structure"`. That
label is not git's; this module wrote it. Round six's guard was

```python
return len(code) == 2 and code[0] not in " ?!"
```

and `len("structure")` is 9, so the answer was "not staged" — the safe-looking one.
Control fell through to `git checkout -- <path>` with a **directory** pathspec whose
index content was the phase's own bytes.

Reproduced against the shipped module at `fb954d4a`:

```
git status: 'MD src/f.txt'
  ACTION: 'src/f.txt' -> NOT_ROLLED_BACK  REFUSED: the phase staged this removal...
  ACTION: 'src'       -> restored         git checkout -- <path>
CONTENT ON DISK: 'PHASE CONTENT -- THIS MUST NOT SURVIVE\n'
```

Two rows, one breach, opposite answers — and the wrong one was the one that acted.
Recipe: `git add` a fenced file, then `rm -rf` its directory. It fires on the real
fences: `runner.py` passes `structure_roots=self.wf.read_only_trees`.

**Why the destroyer guard was immune and this one was not.** The `created` side asks
*git* (`_tracked_under`), so a made-up status cannot fool it. The `deleted`/`modified`
side asked *the string*. Only the guard that trusted a label was fooled by a label —
and the label it trusted was one this module had written itself.

Fixed by asking the repository instead: `git diff --cached --name-only HEAD -- <path>`
under `GIT_LITERAL_PATHSPECS=1`. That is a property of the tree, so it is immune to a
status being synthetic, `None`, or added later, and it retires the hand-placed
`RENAME_SOURCE` exemption — `git mv` stages both ends, so git reports both. Verified
no over-refusal: empty for an unstaged edit, an unstaged rmtree, and a clean path.

### 13.2 L9 — a negative claim nobody was checking

The staged-removal refusal said "HEAD still holds N file(s) here **and the index no
longer does**". `held.in_index` was never read. For `MD` it is false — the index holds
the phase's content. The operator was told the index was empty one line above the
command that reads the index, which is L8's damage made invisible.

My round-six claim-verifier could not catch it: it checked that a positive HEAD claim
was backed by a non-empty HEAD, and had no counterpart for a claim that something is
EMPTY. Every clause in every refusal is now derived from a measurement, and the wall
checks negative claims symmetrically.

### 13.3 The third category the wall could not reach

Round six documented two: codes git emits (wall rows) and codes git *might* emit
(alphabet tests). jack-ryan named the third — **status values this module emits about
itself**. `"structure"` and `RENAME_SOURCE` are outside both: the wall plants artifacts
and git never writes `"structure"`; the alphabet iterates `" MTADRCU?!"` squared.
`RENAME_SOURCE` had survived only by a hand-placed exemption naming it, which is how
you can tell the category was never enumerated. The remedy is not a third test family
— it is that no guard keys on the label any more.

### 13.4 The process amendment needs its own amendment

§ 12.3 said: *a new predicate's row must be shown to RED with the fix reverted, before
it ships.* **L8 would have passed that gate cleanly.** `_was_staged_by_phase` was
load-bearing on every row that reached it; revert it and rows went red. The defect was
that one route into the guard never reached it at all.

So the rule as written proves a predicate is load-bearing *where it is reached*, and
says nothing about whether it is reached everywhere it must be. Stated in full:

> A new predicate's row must be shown to RED with the fix reverted, before it ships —
> and the row must arrive by **every route a change can take to that predicate**, not
> only the route git labels. A mutation that binds to nothing is a loud failure, never
> a silent pass.

The new wall row `staged_dir_removal` is the reachability half: it goes RED against
`fb954d4a` in both fixture shapes, and nothing else moves (2 failed, 406 passed).
jack-ryan is drafting this as Discipline 37 with both clauses; that document is his.

### 13.5 Evidence

| Item | Result |
|---|---|
| Suite | 410 passed (398 at round start) |
| Artifact kinds | 20 × 2 fixture shapes × 4 rounds + canary |
| L8 reachability | new row RED at `fb954d4a`, both shapes; 406 others unmoved |
| L8 over-refusal check | empty for unstaged edit / unstaged rmtree; non-empty only for staged |
| Round-seven mutations | see § 13.6 — four survivors on the first pass, zero on the second |
| Fenced-tree baselines | engine 2907 / godot 3288, unchanged (**corrected** — see § 14.4) |

### 13.6 The mutation table, both passes

The first pass returned **four survivors**, and they are the reason round seven is
not one commit shorter.

| Mutation | Property | First pass | Second pass |
|---|---|---|---|
| M23b staging guard never reached | L2 general | RED | — |
| M23c the predicate answers `not staged` | L2 general | RED | — |
| **M28 the guard reads the LABEL again** | **L8 verbatim** | **RED (2 failed)** | — |
| M30 refusal asserts the index is empty | L9 | RED | — |
| M20 git reads pathspec magic | L1 | RED | — |
| M26 shell metacharacters PASS | L5 | RED | — |
| M29 unanswered counts as `no` | L8 | **GREEN** | RED |
| M31 unborn HEAD answers `no` | L8 | **GREEN** | RED |
| M27 refusals unsurfaced | L6 | **ANCHOR NOT FOUND** | RED |
| M24 control | control | **GREEN** | RED (16 failed) |

M23b and M23c are round six's, re-anchored: round seven deleted the text they bound
to, so run unchanged they would have printed ANCHOR NOT FOUND and the set would have
reported as verified.

**M29 and M31 were real gaps of the same shape one tier down.** The guard was correct
in both cases and nothing was holding it there. The wall cannot plant either — a
healthy repo never refuses a question, and every fixture has commits — so they are
alphabet-tier tests. Writing the first one caught an error in my own fixture: I
dirtied the file before taking the baseline, so `was_dirty_before` dropped the change
and the guard was never reached. That is the same masking that hid L8 for six rounds,
reproduced by accident inside the test written to close it.

**M27's anchor was invented rather than read off the file**, so L6 was reported as
verified while nothing ran. It surfaced only because unmatched anchors are counted as
loud survivors — a safeguard added in round six on its second outing.

**M24 was not a control.** It was `assert True or <canary check>`. Removing an
assertion from a green suite cannot turn it red, so the mutation had no power to
detect anything and its result carried no information in either direction — yet it
had been reported as a passing control. A control-shaped comment is the same defect
as a guard-shaped comment. It is replaced by a mutation to PRODUCT code
(`git checkout -- <path>` -> `git checkout -- .`), and the canary assertion is now
confirmed to be the thing that fires, by name:

```
test_containment_wall.py:525: AssertionError: rolling back a mode_only_change in the
read_only_subtree shape destroyed uncommitted work on canary.md, a tracked file NO
ARTIFACT TOUCHED.
```

Second pass: **SURVIVORS: none. unanchored: none.**

---

## 14. Round eight — the defect shape left the product and moved into the certification

jack-ryan's round-eight Gate-2 verdict was **HOLD** on three findings. None of them is
in `permissions.py`. All three are in the thing that certifies `permissions.py`, and
all three are the same shape the previous seven rounds were: *a check that answers a
slightly different question than the one asked, whose wrong answer is the safe-looking
one.* One layer up, the safe-looking answer is **green**.

This is the first round where I have to say plainly: the reviewer was reviewing my
tests because my tests had stopped being able to review my code, and I did not notice
because they were passing.

### 14.1 B1 — the L9 fix was checked as prose, so a flat falsehood passed 410 tests

Round seven's rule 17 said every clause in every refusal is derived from a
measurement. It was — and then the measurement was interpolated into an English
sentence, and the wall asserted things about the sentence.

jack-ryan's J3 mutation replaced the measured tuple with literal zeros. The refusal
then told the operator `head_files=0; index_files=0; staged_paths=0` for a tree where
git says otherwise, and the suite stayed **green**, because the sentence still had the
shape the wall was looking for.

Numbers on an abort report are the thing an operator acts on. "HEAD holds nothing
here" is the difference between *recover from the commit* and *this is unrecoverable*.
A claim checked only for its wording is a claim nobody checked.

Fixed by making the facts **structured and load-bearing in both directions**:

```python
@dataclass
class RollbackAction:
    ...
    facts: tuple[tuple[str, int], ...] = ()

def render_containment_facts(facts: tuple[tuple[str, int], ...]) -> str:
    """The ONE place a refusal's measured clause is worded."""
    return "; ".join(f"{name}={value}" for name, value in facts)
```

The measurements travel on the action; the prose is *rendered* from them. The wall
re-derives all three from git, compares the pairs, and then asserts the rendering
appears verbatim in the reason. So the numbers cannot drift from the tree (they are
compared to it) and the sentence cannot drift from the numbers (it is generated from
them). Three mutations hold that: falsify the numbers, falsify the sentence, or stop
the facts travelling — see the table.

### 14.2 B2 — three assertions that could not fire, and the audit that was itself vacuous

Round seven deleted product prose and left behind wall assertions gated on it:

```python
if "the phrase permissions.py no longer emits" in reason:
    assert <something that would have mattered>
```

The guard is never true, so the assert never runs, and the test reports a pass. Three
of these were live. jack-ryan's line trace found two; the scanner I wrote to close the
finding found a third he had not seen.

The remedy is a standing gate in `test_permissions.py`, not three deletions: it reads
`test_containment_wall.py`, extracts every string literal used to *decide* whether to
check something, and requires each to be present in `permissions.py`.

Then the interesting part. That gate **passed while collecting zero phrases** — the
extraction was inline and silently matched nothing, so the loop body never ran. That
is precisely the defect the gate exists to prevent, written by me one turn after
writing the gate. It is also round seven's M24 (`assert True or X`) recurring within a
single round: *a check with no power reports the same as a check that passed.*

So the scanner proves it can find something before its silence is allowed to mean
anything:

```python
def _reason_gate_phrases(src: str) -> list[str]: ...

def test_B2_no_wall_assertion_is_gated_on_a_phrase_the_product_no_longer_emits():
    sample = 'if "SENTINEL GATE PHRASE" in reason:\n    assert x'
    assert _reason_gate_phrases(sample) == ["SENTINEL GATE PHRASE"], (
        "the phrase scanner no longer recognises a phrase-gate, so its silence about "
        "the real wall means nothing. Fix the scanner before trusting this test."
    )
    ...
```

Two mutations hold it: blind the scanner, and plant a dead phrase-gate in the wall.

One implementation note that is itself the pattern: the first working version failed
on my own *comment* quoting a retired literal. Stripping comment lines before scanning
is correct — a comment decides nothing — but it is worth recording that the scanner's
first true finding was in the file documenting the scanner.

### 14.3 B3 — a predicate proven to refuse, never proven to act

`_staged_against_head(root, rel)` was reached only by rows where staging existed at the
artifact path. Drop its `-- rel` pathspec — jack-ryan's J6 — and the question silently
becomes *is anything staged **anywhere** in this repository*. Every wall row stayed
green, because in every fixture the only staged thing was the artifact.

The live consequence is not subtle: one unrelated `git add` anywhere in a declared repo
turns containment into a blanket `NOT_ROLLED_BACK` for every breach in it. Refusing
everything looks conservative and is the failure mode where the breach survives.

The partner stages a *different* file (`.gitignore`) and requires the rollback to
**act** on the breached one, restoring it to baseline bytes. YES-branch and NO-branch,
both pinned.

### 14.4 The reachability clause, amended a second time — and a retraction

§ 13.4 already amended § 12.3 once: a predicate must be reached by every route, not
only the route git labels. Round eight shows two more ways a predicate can be
uncertified while its row is red on reversion. Stated in full:

> A new predicate ships with **both branches exercised**: a row where it must answer
> YES and the verb must REFUSE, and a row where it must answer NO and the verb must
> ACT. Its **scope arguments** and **every factual clause its output justifies** must
> each be independently falsifiable — reverting any one of them must turn a row red.

Three axes of unreachedness, which is jack-ryan's framing and the right one: **arrival
route** (L8), **scope/arguments** (B3), **output and the claim it justifies** (B1).
This is his document to write as discipline text; I am recording the operational form
I built against.

**Retraction.** Rounds one through seven of this note repeated "fenced-tree baselines:
engine 2789 / godot 233". Those figures are wrong and I did not re-derive them after
the structure sweep and the ignored-path sweep changed what a fingerprint counts. The
module's own `fingerprint().entries` reports **engine 2907 / godot 3288**, independently
confirmed by jack-ryan. § 13.5 is corrected in place. The property those numbers were
cited to support — identical before and after the run, and across both determinism laps
— still holds and is re-measured this round. The lesson is the round's own: a number
carried forward in prose is not a measurement.

### 14.5 The B1 fix survived its own mutation table, and the second pass found the site I had missed

The first mutation pass over round eight returned **one survivor: N6**. It drops the
`measured` argument at the `RollbackAction` constructor. `facts` then defaults to `()`,
and the wall's check was:

```python
if action.facts:
    ...assert the numbers against git...
```

So the product could switch the certification off by sending nothing, and 412 tests
stayed green. That is the third instance of this round's own defect **inside the fix
for the first instance** — a check gated on a condition the thing under test controls,
whose false branch is silent. It is B2's phrase-gate with a different condition, and it
is round seven's `assert True or X` with a different disguise. I wrote all three.

The fix is the one this round has been repeating: **do not ask the action, ask git.**

```python
expected = {"head_files": ..., "index_files": ..., "staged_paths": ...}   # from git
if expected["staged_paths"]:
    assert action.facts, "...the operator is being asked to act on prose..."
if action.facts:
    assert dict(action.facts) == expected
    assert perm.render_containment_facts(tuple(expected.items())) in reason
```

Whether a refusal *owes* the operator numbers is a property of the tree, not of the
object under test, so the tree is what decides it.

**That tightening immediately failed four rows I had believed were passing** — and the
failure was real. There are **two** refusal sites, and I had only fixed one. The
destroyer guard (`created` + `_tracked_under`) still interpolated its counts into
English:

```
REFUSED: the phase staged this itself — git's index holds 1 file(s) under it and
HEAD holds none...
```

True numbers, checked only by the older prose-parsing assertion, with nothing
structured travelling. It is the identical B1 defect at a call site jack-ryan's J3
mutation did not reach, and it surfaced within one suite run of the wall being told to
source its expectations from git rather than from the action. Both sites now build
`measured` and render from it; two new mutations (N8, N9) hold the second one.

The general lesson, which is the fourth time this review has produced it: **a fix
applied at the site the reviewer named is not the same as a fix applied to the class.**
I closed B1 where J3 pointed and reported it. The class was in two places.

### 14.6 The mutation table, both passes

| Mutation | Property | Pass 1 | Pass 2 |
|---|---|---|---|
| N1 = jack-ryan **J3** — staging-guard facts become zeros | B1 | RED (6) | RED (6) |
| N2 rendered sentence stops matching the measurements | B1 | RED (6) | RED (6) |
| N3 = jack-ryan **J6** — the guard's `-- <path>` pathspec dropped | B3 | RED (1) | RED (1) |
| N4 the phrase scanner stops recognising a phrase-gate | B2 | RED (1) | RED (1) |
| N5 a dead phrase-gate is reintroduced into the wall | B2 | RED (1) | RED (1) |
| **N6 staging-guard facts stop travelling** | B1 | **GREEN** | **RED (6)** |
| N8 destroyer-guard facts stop travelling | B1 | *(site did not exist)* | RED (4) |
| N9 destroyer-guard facts become zeros | B1 | *(site did not exist)* | RED (4) |
| N7 CONTROL — `git checkout -- .` | control | RED (16) | RED (16) |

**Pass 2: SURVIVORS none, unanchored/ambiguous none.** Both of jack-ryan's own
survivors (J3, J6) red against the fixed module, which is the only evidence that the
fixes are not comments.

One harness change worth naming: the anchor check was `if old not in src` and is now
`if src.count(old) != 1`. An anchor matching **twice** would have silently mutated
whichever site came first and reported a confident result about the other — and this
round created exactly that hazard by introducing a second `quarantined,\n measured,`
block. A harness that cannot tell which line it edited is measuring nothing, which is
the round's subject.

### 14.7 Evidence

| Item | Result |
|---|---|
| Suite | 412 passed (410 at round start) |
| Round-eight mutations | 9 run, **zero survivors**, zero unanchored (§ 14.6) |
| jack-ryan's survivors J3 / J6 | both RED against the fixed module |
| Dead assertions removed | 3 (two named by the Gate-2 line trace, one found by the new scanner) |
| New standing gate | phrase-gate audit, with a sentinel proving the scanner has power |
| Refusal sites carrying structured facts | 2 of 2 (staging guard, destroyer guard) |

### 14.8 An unplanned live proof: the spine aborted on my own write, and refused to undo it

The first founding-run attempt this round **ABORTED**, and it was right to. I edited
`agentic_orchestration/factory/README.md` while phase 2 was executing:

```
PERMISSIONS BREACH during phase execution — aborting the run
  agentic_orchestration/factory/README.md (modified) — write inside an always-protected
  path (never config-overridable)
  rollback: agentic_orchestration/factory/README.md -> NOT_ROLLED_BACK
  containment: 1 of 1 breaching path(s) were NOT undone — deliberately, with a stated
  reason. Those artifacts are quarantined and still in place.
ABORTED
```

Three things fired correctly and none of them were rehearsed:

1. the **second fingerprint** caught it — the write landed during gate execution, and
   `during="gate execution"` is exactly the window § "Why the runner fingerprints twice"
   exists for;
2. `was_dirty_before` **refused the rollback**, because the README was already modified
   at phase start. Had it "restored" the file it would have destroyed round eight's
   uncommitted documentation. This is the K1 damage class, avoided on a real edit rather
   than a planted one;
3. the refusal was **surfaced** in the abort report rather than returned in a list and
   dropped — rule 15 (L6), which was a paper receipt until now.

Recorded because it is the only unplanned evidence in this note. Everything else here
is an artifact I planted in order to be caught. Operator note for the next session:
**do not edit the factory tree while a run is in flight** — the spine is not wrong to
stop, and a clean re-run is the whole cost.

### 14.9 Run evidence, this round

| Item | Result |
|---|---|
| Founding run | **PASS 3/3** (`kc2-baton-mechanical-20260811T061535Z-1b951a`) |
| Determinism | `DETERMINISM: EXACT — 14 gate verdicts identical across two laps` |
| Fenced-tree baselines | engine **2907** / godot **3288**, `usable=True`, unchanged across run + both laps |
| Unplanned abort | one, on a real concurrent write; rollback correctly refused (§ 14.8) |

---

## 15. Round ten — the trigger, the fourth axis, and a gate that measured instead of matching

jack-ryan returned round nine as **HOLD**, with three BLOCKs and two WARNs, every one
reproduced live against the shipped module with the suite green. Round eight had moved
the defect shape out of `permissions.py` and into the thing that certifies it. Round
nine found it in **the fix for the certification** — which is the more useful finding,
because it says the shape is not a property of the product at all.

### 15.1 C1 — the fix for rule 17 was switchable by the thing it certified

Round eight made a refusal's counted claims travel as `facts` and had the wall compare
them to git. The wall then decided *whether to check* on `if action.facts:` — a trigger
the product switches off by sending nothing. I fixed that by sourcing the trigger from
git: `if expected["staged_paths"]:`.

That is the same defect with a better disguise. `staged_paths` is **one of the three
values the check certifies**. A guard that reported zero staged paths — wrongly or
rightly — switched off the assertion that would have caught it.

The fix is a **closed vocabulary of guard identities**. Every one of the ten refusal
sites now carries `guard="<name>"` from `REFUSAL_GUARDS`; `GUARDS_OWING_FACTS` names the
two that make counted claims; the wall asserts the guard is in the vocabulary, demands
facts from the two that owe them, and compares those facts to git. Whether a claim must
be checked is now decided by **which** claim was made, never by **what it said**.

The first attempt at this was correct code and closed nothing: the assertion was
**unreachable**. Every destroyer row in the wall has staged content, and the unit tier
checked no facts at all. Two coverage rows were added — a destroyer refusal with
`staged_paths=0`, and a staging refusal where `git diff --cached` is made to *fail*, so
the branch where git refused the question is exercised. Seven mutations (jack-ryan's P1,
P2 and P6 verbatim, plus the four escapes the fix itself creates — dropping either guard
label, naming a guard outside the vocabulary, and a control): **all red, zero
survivors**, 414 tests at that point.

### 15.2 C2 — the never-executed-assert audit had a never-executed assert

Round eight closed B2 with a regex scanning the wall for `if "<phrase>" in reason:`
gates, requiring each phrase to still exist in `permissions.py`. It shipped with a
sentinel — right instinct, wrong target: the sentinel proved the *regex* could recognise
a phrase-gate, not that the regex could see the *suite*. jack-ryan planted three escapes
it could not see (another file, single quotes, an aliased subject) and said plainly: the
regex as it stands is not a gate.

It is now **execution measurement**. `tests/_reach_tracer.py` is a pytest plugin that
installs `sys.settrace` and records every line executed under `tests/`;
`tests/test_reach_audit.py` spawns one child run of the whole suite under it and requires
every `ast.Assert` node in the tree to have executed at least once.

**Its first act was to convict its predecessor.** Of 390 assert statements, exactly one
had never executed in any run: the assertion inside the phrase scanner's own loop,
because the scanner collected **zero** phrases from the wall. The check written to catch
dead assertions was one. It is deleted, not moved — the audit subsumes it strictly, and
covers the shapes a pattern could not.

Three things were learned building it, each from a red:

* **the sentinel earned its place immediately.** The tracer filtered frames to `tests/`,
  and the sentinel probe is written into a `tmp_path` — so the first run reported that
  the tracer could not see an assert that definitely executed. A tracer whose reach is
  hardcoded to its own suite cannot be shown to have power over anything;
  `FACTORY_REACH_DIRS` now names the traced trees.
* **the audit reported itself, correctly.** The child-run checks sat in an `else:` the
  child never enters, so in the child they were three assertions that never ran.
  Exempting its own file would have been the self-certification this spine refuses;
  fabricating a fixture to satisfy them would have been worse. The branch is gone — the
  checks are **data** returned by `audit_problems`, adjudicated by one assertion that
  executes in both modes.
* **a check whose failing arm nothing reaches is the finding one level up.** Mutation S7
  (ignore the child's exit code) survived the first pass, because on a green suite that
  branch is dead. `problems_from()` was extracted as a pure function so both failing arms
  have rows that reach them without spending a run.

Three power checks now stand behind the claim, because it can go quiet three ways: the
**sentinel** (the tracer can tell reached from unreached), the **enumerator floor**
(`> 300` asserts found), and the **comparison test** (it is still looking). Mutations:
jack-ryan's P3/P4/P5 planted as real unreachable assertions — **all three named by file
and line** — plus five ways the audit itself could go quiet, plus a control. **Zero
survivors.**

Cost, measured: 53 s untraced, 55 s traced; the suite is run twice, so ~110 s total. The
tracer returns `None` for frames outside `tests/`, which switches off line events for the
product entirely — that is the whole difference between affordable and unusable.

### 15.3 C3 — the one allowlist in this spine that failed OPEN

`claude --help`, verbatim: *`--tools <tools...>  Specify the list of available tools from
the built-in set. Use "" to disable all tools, "default" to use all tools`*. So omitting
the flag is **not a neutral default** — it is the full built-in set, chosen by nobody.
Every sibling allowlist here fails closed: an empty `writes` breaches everything, an empty
`gates` is a load error. This one was proven only to RESTRICT when declared and never to
REFUSE when absent — B3's shape, at the harness layer, on the agentic lane.

Closed at **both** entry points: the loader refuses an agentic phase with no `tools`, and
`build_argv` refuses it too, because a guard present in only one of two entry points is a
guard with a route around it (that is L8's finding). Both flags are emitted — `--tools`
selects what exists, `--allowedTools` selects what may run unprompted, and a headless run
has nobody to prompt. `permission_denials` now **fails the phase**: a phase reaching
outside its declared tools is the pre-hoc analogue of a breach, and this spine does not
treat a breach as noise or as a retry. If live data later shows benign probing is common,
that is weakened **on evidence**, the way the COARSE caveat is.

The adjudication was lifted out of `run()` into `ClaudeCodeHarness.adjudicate()`. It had
lived behind a live subprocess, so the only way to exercise it was to invoke a model —
which meant nothing exercised it, on the lane under review. **A verdict that can only be
checked by spending money is a verdict nobody checks.**

Five pre-existing tests went red on the LOAD refusal, all fixtures building agentic
phases with no `tools`. They were fixed, not exempted.

### 15.4 C4 — always-protected, in the root repo only

The always-protected list was matched against the root repo alone, so a phase declaring a
sibling repo as a write target could write `.claude/` **there** — the next-session hijack
the protection exists to prevent, at a path the workflow itself named.
`PROTECTED_EVERY_REPO` is now matched in any declared repo and is not
config-overridable. The root-only entries stay root-only, and a row asserts *that* too:
without it the fix could quietly become a blanket fence that breaks a sibling repo's
legitimate write targets, and nothing would say so.

### 15.5 C5 — a caveat is a claim to a reader, not a gate

README rule 3 discharged the COARSE blind spot with a receipt caveat. For the mechanical
lane that is bounded: every path is authored by a human in a reviewed YAML file. The
agentic lane is **defined** by a model choosing paths — exactly the case the caveat does
not cover — and the coarse regions are gitignored, so an in-place edit there is neither
detected nor recoverable from git. The two weaknesses compound, which rule 3 did not say.

A workflow with an agentic phase is now refused at LOAD unless it names each coarse
region under `coarse_acknowledged:`. Naming a region that is **not** coarse is refused
too: an acknowledgement drifted from the tree reads as diligence and certifies nothing.

Two things the mutation table forced. The validator originally called `fingerprint()`
with a keyword that function does not accept — it would have raised `TypeError` on first
contact, and nothing called it, so nothing knew. And R6 (make the acknowledgement a
boolean) **survived** the first pass: with one coarse region in the fixture, per-region
and blanket are observationally identical. A second region was added, and the escape
hatch now costs one line per region or it is a checkbox.

The scope was widened past the finding on purpose. jack-ryan wrote C5 about read-only
trees; this checks every declared repo. The narrower reading would have been the same
class one more time — an undetected in-place write is undetected wherever it lands, and
in a *writable* repo it is a change `classify` never sees at all.

### 15.6 The reachability clause, amended a third time — the fourth axis

Adopted verbatim from jack-ryan's round-nine verdict:

> **The condition that decides whether a check runs must be independent of every value
> that check certifies, and must itself be falsifiable: inverting the trigger must turn a
> row red. A check that can be switched off by anything it is measuring is a comment.**

Three axes became four: a predicate can be unreached by its **arrival route** (L8), by
its **arguments** (B3), by the **claim its output justifies** (B1) — and now by its
**trigger** (C1). Every round-ten fix ships with the trigger's own falsification: C1's
guard-label mutations, C5's mechanical control row, C2's comparison test.

### 15.7 The mutation tables

| Set | Mutations | Survivors | Note |
|---|---|---|---|
| C1 (jack-ryan's P1/P2/P6 + 3 escapes + control) | 7 | **0** | first pass: the fix was correct and unreachable; two coverage rows added |
| C2 (P3/P4/P5 planted live + 5 self-quieting + control) | 8 | **0** | first pass: S7 survived (exit code ignored on a green suite); `problems_from` extracted |
| C3 + C4 (both entry points, both flags, denials, every-repo, control) | 8 | **0** | two rows added first: the LOAD refusal and the argv delivery had none |
| C5 (call site, trigger both ways, set arithmetic, stale, boolean, control) | 7 | **0** | first pass: R6 survived on a one-region fixture; control was toothless and was replaced |

Every table restores the target and asserts the restore; the anchor check requires
exactly one match, so a mutation that silently applied nowhere cannot read as a pass.

### 15.8 Run evidence, this round

| Item | Result |
|---|---|
| Suite | **428 passed** (~110 s; the reach audit runs the suite twice) |
| Asserts proven to execute | **390 of 390**, measured under `sys.settrace` |
| Founding run | **PASS 3/3** (`kc2-baton-mechanical-20260811T080017Z-7be701`) |
| Determinism | `DETERMINISM: EXACT — 14 gate verdicts identical across two laps` |
| Fenced-tree baselines | engine **2907** / godot **3288**, `usable=True`, unchanged across run + both laps |
| Mutation survivors, all four sets | **0 of 30** |

### 15.9 What is still open

* **O4** (the dollars figure: gandalf DROP vs jack-ryan KEEP) and **D-10** (no HALT
  status) remain Matt's calls, unchanged.
* **G3** (host co-tenancy) and **G5** (rollback reason derived from branch, not from a
  second measurement) carried forward.
* gandalf DRIFT-CRITIC review of the amended reachability discipline text.

---

## 16. Round twelve — the channel that could not carry its own counterexample

jack-ryan's round-eleven review returned a **scoped verdict**: LIFT for the mechanical
founding run, HOLD for the agentic lane. He confirmed C1 was fixed at the class (both of
his attacks died), that the guard partition is right, that C5's trigger is falsifiable,
and that C3 has no third code path — *"the route around is not a code path, it is a
value."* Six findings, F1–F6, three of them blocking.

The through-line of this round is the fourth axis pointing at itself. C3, C4 and C5 were
all fixes I wrote and then certified; F4, F5 and F6 are each **the certification stopping
one question short of the claim**. F3 is different and worse: not a predicate answering a
slightly different question, but a **channel that structurally could not carry the
counterexample**.

A seventh, **F7**, was not on his list and surfaced from typing the command a reviewer
types (§16.7). It is the same shape at its mildest: the suite's own subject was undeclared.

### 16.1 F3 — `git status` will never tell you about `.git/`

C4 protected `.claude/` in every declared repo because it is a hook-execution surface and
a phase writing it arranges for code to run in the next Claude session there. The same
sentence, one directory over: `.git/hooks/pre-commit` arranges for code to run on the
next git operation any **human** performs in that repo. `.git/config` reaches the same
place from the side via `core.hooksPath`.

It was not merely unprotected. Every path in `permissions.py` arrives from
`git status --porcelain -z --ignored=traditional`, and git does not consider its own
directory part of the worktree at any porcelain setting. So the write produced an **empty
change-set**, and an empty change-set is the module's word for innocence. jack-ryan's
probe measured it: *"a `.git/` write is INVISIBLE to containment."*

Three named surfaces are now measured directly and folded into `entries` as ordinary rows
(synthetic code `G!`), so they inherit the diff, the classifier and the receipt unchanged:

| Surface | Why it, and not the rest of `.git/` |
|---|---|
| `hooks/` (direct children) | git executes exactly the direct children — a flat listing is the exact set, not a sample |
| `config` | `core.hooksPath` reaches `hooks/` sideways; `url.*.insteadOf` reaches the network |
| `info/exclude` | an untracked ignore list — appending to it makes the phase's *later* writes invisible to every other measurement in the module |

**Not** refs, the index, or the object store. That restraint is K1's lesson paid forward:
K1 put `.git` in the structure sweep, the object fanout moved on a plain `git add`, and
the most disciplined thing an agent can do inside a read-only tree became the breach that
triggered a repo-wide revert. A partner row runs `add`, `commit`, `checkout -b` and `gc
--prune=now` and requires the control signature **unmoved**; the mutation that adds
`objects/` to the list turns it red, which is what makes it a row rather than a hope.

The second half of F3 is that detection here must **not** be wired to a verb. Both verbs
available are actively wrong:

* `created` sends the path to the destroyer guard, which asks what git tracks underneath.
  git tracks nothing under `.git/` — correctly — so the guard would find zero and
  authorise `rmtree` on `.git/config`. **Containment would break the repository.**
* `git checkout --` cannot restore a path git has never heard of.

So `git_internal` joins `REFUSAL_GUARDS` (eleven names now): quarantine the evidence,
name it, stop. Keyed on the **path**, not on `change.kind` — a kind is a measurement, and
C1's fourth clause forbids a trigger that anything it certifies can switch off. Planting a
hook arrives as `git_internal`, deleting one arrives as `modified`, and a dedicated row
proves both refuse under the same guard.

### 16.2 F4 — I proved the allowlist REFUSES when absent, not that it RESTRICTS when present

C3's own finding was that `tools` was the one allowlist in this spine that failed open. I
fixed it at both entry points, wrote rows for both, and the rows asked whether an
**absent** allowlist is refused. That is a test of declaration. `tools: [default]` — one
word, `claude --help`'s own spelling of *"use all tools"* — reaches the exact state the
guard exists to prevent, and it reads on the page as diligence.

Rule 13 applied to the allowlist: a **closed vocabulary**. `BUILTIN_TOOLS` was read off
the `init` frame of a live stream-json run on this host, not copied from documentation and
not guessed — the CLI enumerates its own tools, so the CLI is the source. Host MCP tools
appeared in the same frame and were deliberately excluded: their availability is
per-machine, so a workflow naming one declares a fence whose contents vary by host.

Five refusals, each with its own row: `default` by name; a non-list (YAML `tools: Read` is
a *string*, and `list("Read")` is `['R','e','a','d']` — four tools that do not exist, an
allowlist that restricts by **accident**); an empty list; an unenumerated name; an `mcp__`
name. Scoped forms (`Bash(git *)`) are kept and have their own row, because a set of
refusals that also refuses the correct input proves nothing.

The vocabulary lives on the **harness**, and the loader calls it rather than holding a
second opinion — with a row that spies on the call and reds if the loader ever stops. A
harness publishing no `validate_tools` is refused outright: a second lane is the obvious
route around a validator that lives on the first, which is L8 with a delay on it.

### 16.3 F5 / F6 — a waiver re-asked, and a key that was not one

C5's `coarse_acknowledged` check runs at LOAD. That is right, and it is a snapshot.
`_note_coarse`'s own docstring, written for G4, says a region can cross the scan cap
**during** a phase — including because the phase wrote enough files to push it over, which
is the case where the waiver matters most. Nobody re-asked. It is now re-asserted at every
snapshot on the agentic lane, off the fingerprint already computed, and raises
`ContainmentError` so the existing handler aborts the **phase** with a receipt rather than
the run with a traceback. The mechanical lane is untouched, and a control mutation that
makes it fire everywhere reds — the founding run is entirely mechanical over a godot tree
with two coarse regions, and would otherwise stop dead.

F6: the key was `repo.name`. Two declared repos at `~/a/engine` and `~/b/engine` share it,
so one waiver silently cleared a region in a tree nobody had looked at. `coarse_key()` is
now the one spelling, on the resolved path, called by loader and runner both. The C5 tests
had `"repo:ignored/"` as a **literal** — a second, independent spelling of a format the
product owns, which agreed only until the product changed, and which encoded the very
basename keying F6 fixes. They now build the key the way the product does.

### 16.4 F1 / F2 — the two the wall found in the wall

F1: `assert rendered in reason` is vacuously true when `rendered` is the empty string, so
the B1 fix's own check could pass on a refusal carrying no facts at all. `assert rendered`
first, with a pinned-wording row behind it.

F2: the C2 reach audit enumerated its subject with a flat `glob` while pytest collects
**recursively** — so an assert in `tests/sub/` was collected, never executed, and never
asked about. The subject is now reported by the collector itself
(`pytest_collection_modifyitems`), which cannot disagree with the collector. Verified
against jack-ryan's own probe: *"an assert that never executes is reported RED — the audit
sees it."*

### 16.5 The mutation table

Sixteen one-line edits, each breaking exactly one property, each adjudicated by the
cheapest suite that can see it (fast tier 6s, wall 53s, reach 60s). Harness at
`/tmp/sl12_f16.py`; every anchor was required to match exactly once, and the target was
restored and the restore asserted.

| # | Mutation | Property it breaks | Suite | Result |
|---|---|---|---|---|
| V1 | `render_containment_facts` returns `""` | F1 — `assert rendered in reason` is vacuous when `rendered` is `''` | wall | RED (10) |
| V2 | reach audit enumerates with a FLAT `glob` | F2 — an assert in `tests/sub/` is collected, never runs, never asked about | reach | RED (2) |
| V3 | `.git/` is not measured at all | F3 — nothing else can see the write | wall | RED (20) |
| V4 | `.git/` dropped from `PROTECTED_EVERY_REPO` | F3 — measured but not protected is detection without enforcement | wall | RED (14) |
| V5 | rollback stops refusing a `.git/` path | F3 — every verb available no-ops or destroys `.git/config` | wall | RED (8) |
| V6 | only `hooks/` measured, not `config` / `info/exclude` | F3 — `core.hooksPath` reaches the same place from config | wall | RED (12) |
| V7 | **CONTROL** — `objects/` joins the measured surfaces | K1's lesson: a measurement that fires on `git add` is worse than none | wall | RED (8) |
| V8 | the LOADER stops validating the allowlist | F4 — a workflow reaches the lane with `tools: [default]` | fast | RED (9) |
| V9 | `default` stops being refused | F4 — one word reaches the state the allowlist exists to prevent | fast | RED (2) |
| V10 | a non-list stops being refused | F4 — YAML `tools: Read` becomes `['R','e','a','d']` | fast | RED (1) |
| V11 | an unknown tool name passes through | F4 — a vocabulary that admits any string is not closed | fast | RED (2) |
| V12 | a harness with no vocabulary may still be given an allowlist | F4 — a second lane is the route around a validator on the first | fast | RED (1) |
| V13 | **CONTROL** — `BUILTIN_TOOLS` emptied | the accept path is tested too; refusing everything is not a fix | fast | **see below** |
| V14 | the runtime re-assertion never fires | F5 — a region crossing the cap mid-run most needs the check | fast | RED (3) |
| V15 | **CONTROL** — the runtime check fires on the mechanical lane too | the trigger is the lane, falsifiable in both directions | fast | RED (1) |
| V16 | the acknowledgement is keyed on the BASENAME again | F6 — `~/a/engine` and `~/b/engine` share a key | fast | RED (2) |

**V13 survived, and the survival was the instrument's fault, not the suite's.** The
anchor was the final line of the `frozenset` literal, so the edit removed
`WebFetch, WebSearch, Write` and left `Read`, `Bash`, `Glob` and twenty others in place —
while the accept-path rows use exactly `Read` and `Bash`. The label said *emptied*; the
edit trimmed three names nothing tests. Re-run as the control it meant to be
(`BUILTIN_TOOLS = frozenset()`, whole literal, `/tmp/sl12_v13.py`): **RED, 20 failed / 99
passed**, reds including all three F4 rows, the C3 argv rows, and every C5/F6 row that
loads an agentic phase. The accept path has teeth.

This is worth naming rather than quietly fixing: a mutation whose *label* and whose
*edit* disagree reports a coverage gap that does not exist, and — the direction that
actually costs something — could equally report coverage that does not exist. An anchor
matching exactly once proves the edit is unambiguous. It does not prove the edit is the
one the row claims. Fifteen of sixteen anchors here were whole predicates or whole
constants; V13's was a fragment of a multi-line literal, and that is the only one that
lied.

**Final: 16 mutations, 16 red, zero survivors.** Baselines and post-mutation tiers
identical (fast 119, wall 284, reach 4); `unanchored: none`.

### 16.6 A hazard in the instrument — the lost-update race

I edited `permissions.py` while `/tmp/sl12_f16.py` was mid-run. The harness reads the
target once, writes the mutated text, and restores **from its in-memory snapshot** — so
my edit landed inside that window and was overwritten by the restore, which also left
mutation V1 (`render_containment_facts` returning `""`) applied to the working tree.

What caught it: the fast tier, inside a minute, with two C1 rows red on the
`assert rendered` guard **F1 had just added**. The fix found the accident that the fix's
own harness caused, which is the most direct evidence available that F1 is not decorative.

Recovery was: kill the harness, verify every mutation target against intent rather than
against memory (`if False:` count zero in all four product files; `GIT_CONTROL_PATHS`,
`PROTECTED_EVERY_REPO`, `rglob`, the resolved-path `coarse_key`, the full
`BUILTIN_TOOLS`, `entries.update(_git_control_entries(root))`, the `.git/` rollback guard,
and `git_internal` at all three of its registration sites), restore the one line, confirm
119 green, restart.

The discipline this earns: **a mutation run owns its targets for its duration.** The
harness holds a snapshot; the working tree is not the source of truth while it runs. If
this becomes routine the harness should take a lock or refuse to start on a dirty tree —
recorded here as the cheaper option of writing it down first.

### 16.7 F7 — the suite's subject was whatever pytest's walk reached

Found while gathering this round's evidence, by typing the command a reviewer types.

`rollback` refuses to undo some artifacts and **quarantines them instead, durably, inside
this tree** at `factory/sessions/<run>/breach/…`. The wall's own fenced trees contain
test files, so the quarantine holds copies of `test_*.py`; one earlier symlink-out-of-tree
breach put engine modules there too. That is containment working exactly as designed —
nothing escaped.

But `pytest` at the factory root walked into the quarantine and reported **33 collection
errors** on artifacts that are supposed to be inert. The suite's SUBJECT had never been
stated; it was whatever the default walk happened to reach. Same family as the rest of
this round, in the mildest possible key: a channel carrying something into a place nobody
asked it to go.

`pytest.ini` now pins `testpaths = tests` and adds `sessions` to `norecursedirs`, and
`test_the_QUARANTINE_is_not_part_of_the_suites_SUBJECT` plants an unparseable `.py` where
quarantine puts things and requires a root-cwd collection to stay clean, over two
invocations (bare and explicit `.`).

Two things worth recording about how that row was written, both of which are the round's
own lesson landing on me:

1. **The first predicate was `"error" not in stdout.lower()`.** `--collect-only -q` prints
   every test NAME, and this suite contains `…_a_tree_that_errored_mid_run_…`. The row
   was red for a reason that had nothing to do with quarantine — a predicate answering a
   different question than the one asked, written *inside the row built to catch that
   shape*. It now asks for the exit code and the counted summary line, both by name.
2. **The first docstring claimed the two config mechanisms cover one invocation each.**
   The ablation says otherwise: with `pytest.ini` absent both arms go red; with only
   `testpaths` removed both stay **green**, so `norecursedirs` is the load-bearing
   exclusion and is alone sufficient; with only `norecursedirs` removed the explicit `.`
   goes red and the bare call is caught by `testpaths`. `testpaths` is redundant for this
   row and kept anyway, because stating the subject out loud is the entire point. The
   ablation shipped; the claim did not.

Scoped to `tests/` the count was **469**, matching the README before this row; with the
two new arms it is **471**, and the bare root command now reports the same 471 rather
than 471-plus-33-errors.

### 16.8 Run evidence, this round

| Check | Result |
|---|---|
| Full suite, scoped `tests/` | **471 passed** |
| Full suite, bare at factory root | **471 passed, 0 errors** (was 471 + 33 collection errors) |
| Mutation set (16, incl. 3 controls) | **16 red, 0 survivors** — V13 re-run as a true emptying |
| F7 ablation | pytest.ini absent → both arms RED; per-mechanism results in §16.7 |
| Founding run | **PASS 3/3** (`kc2-baton-mechanical-20260811T091949Z-da2b96`), every gate green |
| Determinism | **EXACT — 14 gate verdicts identical across two laps** |

### 16.9 What is still open

* **O4** (dollars figure: gandalf DROP vs jack-ryan KEEP) and **D-10** (no HALT status)
  remain Matt's calls, unchanged. jack-ryan notes D-10 becomes material on the agentic
  lane, which is the lane this round exists to open.
* **G3** (host co-tenancy) and **G5** (rollback reason derived from branch rather than
  from a second measurement — adjacent to F1) carried forward.
* gandalf DRIFT-CRITIC review of the amended reachability discipline text.

---

## 17. Round fourteen — the argv is not the grant, and the ledger's cheapest lie

jack-ryan's round-thirteen review returned **HOLD** with seven findings. Every empirical
claim in it was independently reproduced before I acted on it; two of the seven were
findings about my *certification* rather than my product, which is now the shape this
review has taken four rounds running.

The round's own summary, in one line: **three of the seven findings are the same defect
on three surfaces I had already "fixed" once** — the permission fence (fixed at the argv,
never at the grant), the coarse-region gate (fixed in the predicate, never at the call
site), and `.git/` control surfaces (fixed for one gitdir, and a repo has many).

### 17.1 H1 / H2 — the flags are not what the process receives

Every permissions row on the agentic lane asserted on `build_argv`'s output. The lane had
never actually run, so nothing had ever checked what the CLI *did* with those flags.

The measured facts, from a four-variant live probe:

* `~/.claude/settings.json` on this host carries `"defaultMode": "bypassPermissions"`, and
  with no `--permission-mode` flag it wins. Every phase this spine would have launched
  would have run with permissions bypassed.
* In `bypassPermissions` the `result` frame's `permission_denials` list **cannot be
  non-empty** — there is nothing to deny. So `test_C3_a_denied_tool_call_is_not_a_passing_phase`,
  the row that adjudicates denials, was reading a list whose silence was structural. A
  green row certifying a fence that was not there.
* Two `mcp__…` tools were granted under an explicit `--allowedTools`. MCP availability is
  per-machine, so the fence's contents varied by host.
* `--tools` silently drops a scoped form: `Bash(git status:*)` sent to it yields no `Bash`
  at all. Both flags had been receiving the same string, so one of them was always wrong.

The fix is `check_grant(init_frame, declared_tools)`, adjudicating the `init` frame — the
CLI's own report of what it did — against the declaration. It fails closed four ways: no
declaration reached it (a *wiring* failure, named as one), no init frame at all, a mode
other than the pin, any `mcp__` tool, or any disagreement between granted and declared in
either direction. The narrow direction matters too: a phase holding *less* than it
declared fails in a way that reads as the agent's fault.

The row `test_no_permission_skipping_flag_appears_anywhere` was **amended, and the
amendment is the finding**. It asserted the flag was ABSENT, on the reading that any
mention of permission modes was a step toward skipping them. Absent is not safe. The safe
state is PINNED.

> **This is a standing host-configuration fact, and it is outside my seam.** `~/.claude/settings.json`
> carrying `defaultMode: bypassPermissions` affects every Claude Code session on this Mac,
> not only the factory's. Surfaced to Matt; I have changed nothing outside the meta-repo.

### 17.2 H3 — sixteen mutations, and not one of them touched a call site

jack-ryan, verbatim: *"all sixteen rows mutate a predicate that some test calls directly,
and none mutate a call site."* The mutation set was measuring the predicates and calling
it coverage of the mechanism.

He was right, and the specific instance was live: `_note_coarse`'s **post-gate** call site
passed no `agentic` argument at all. It defaulted, the default happened to be right, and
every row on the function stayed green because the rows passed the trigger themselves.

Fixes: the argument is required (omission is a `TypeError`, not a default); three rows,
one per call site, none of which names `agentic`; a fourth control on the mechanical lane
so `agentic=True` hardcoded fails too.

Two things went wrong writing those rows, and both are the review's own subject:

* The post-gate row **passed for the wrong reason.** `status == "ABORTED"` is satisfied by
  the breach classifier independently — an ignored directory appearing is a path outside
  `writes` — so the row was green with the gate under test disarmed. Rows now assert the
  abort reason contains the specific `when` label.
* The post-execution row failed, and the failure was a `NameError` in my own fake harness.
  Chasing it produced H8 below. **The row was sensitive enough to catch a defect it was
  not written to look for**, which is the argument for these rows existing.

Wiring is now a mutation **category** (`WIRING`), per jack-ryan's explicit instruction.

### 17.3 H8 — the ledger's cheapest lie, found while debugging H3

The runner reported `usage: NULL (mechanical phase — no model invoked)` on a line whose
next word was `[star-lord]`.

`Phase.usage` defaulted to `UsageBreakdown.absent("mechanical phase — no model invoked")`.
The runner computed a lane-aware reason and never handed it to the Phase, so the default
stood — and **the only path that ever read it was the path where an agentic phase's
harness raised mid-flight.** `Phase.__exit__` records; `finish_phase` writes it to the
durable `phases.usage_absent_reason` column. The ledger asserted that no model ran, for a
phase that named an agent and launched a harness, at exactly the moment spend was least
accounted for.

`usage.py`'s own module docstring states the law: *"Absent is absent … Tokens are never
invented, never zero-filled."* Inventing the **reason** breaks it as surely as inventing a
count, and worse, because the invented reason is the reassuring one. This is the recurring
shape landing in the one place I am the seam owner for.

Three states, three reasons, each refutable on its own path:

| State | Reason | The path that reads it |
|---|---|---|
| aborted before the attempt | `no attempt recorded` | phase-start containment abort |
| harness in flight when the phase ended | `attempt N was in flight … cost is UNKNOWN (not zero)` | the raise |
| no agent | `mechanical phase — no model invoked` | `_execute`'s mechanical branch |

The third is kept, not deleted — it is structurally true on the one lane that has no
agent, and a control row requires it, because "fix it by removing the claim everywhere"
would pass the other rows.

### 17.4 H4 — a repo has as many gitdirs as it has submodules and worktrees

F3 closed `.git/hooks/pre-commit` and measured **one** gitdir. `.git/modules/<sub>/` is a
submodule's complete gitdir with its own `hooks/`; `.git/worktrees/<wt>/` is a linked
worktree's, carrying `config.worktree`, which reaches `core.hooksPath` exactly as `config`
does. The write F3 exists to catch was still invisible one directory deeper.

Measured on both axes, because either alone leaves a live path: **entry names** (a gitdir
appearing is itself the change) and **the closed control list inside each** (planting a
hook in an existing gitdir moves no entry name).

The partner control earned its place immediately. My first version keyed the entry on the
real directory path — and `_signature` stat-sweeps any key that resolves to a directory,
so it would have swept the gitdir's `index`, `HEAD`, `refs/` and object store and breached
on **every ordinary commit inside a submodule**. That is K1 verbatim, on the axis added to
fix H4. The entry is now a synthetic key, which resolves to nothing and carries its signal
by existing.

### 17.5 A defect in the instrument: a mutation harness with a red baseline

The first H8 mutation harness reported `4 RED, 0 survivors`. It was reading
`returncode != 0` as caught — against a baseline that was **already red** (five rows
stale from the H1/H2 edits). One mutation, `H8-d`, produced results *identical to the
baseline* and was reported as killed.

The predicate answered a slightly different question than the one asked, and its wrong
answer was the reassuring one. In the harness built to detect exactly that. The harness
now measures its baseline first, **refuses to run if it is not green**, and counts a
mutation as caught only when the set of failing test NAMES grows.

I am recording this because a mutation harness is a certification instrument, and this is
the second round in a row where the instrument had the disease (§16.6 was the lost-update
race). The instrument gets audited like the product now.

**And a second one in the same round.** The rebuilt harness validated each mutation's
anchor immediately before applying it. Mutation 12 of 24 — `H3-w3`, whose anchor I had
written against a one-line signature that is actually five lines — matched zero, and the
assertion aborted the set **25 minutes in**, leaving 13 mutations unmeasured. The check
was correct and its TIMING was not: an anchor is verifiable in milliseconds without
running anything, and validating it late converts a typo into a lost certification run.
All 24 anchors are now validated up front, before the baseline is measured.

Both instrument defects are the same shape as the product defects this review keeps
finding. A late check and an absent check differ only in how long you believe the wrong
thing.

### 17.5a A survivor, and what it was hiding

`--strict-mcp-config` was dropped from the argv and **nothing went red**. `check_grant`
refuses MCP tools when they *arrive*, so detection was covered and prevention was not —
the same argv-versus-grant split H1 is about, appearing inside H1's own fix.

Detection alone is not equivalent here. Without the flag, every agentic phase on a host
with MCP servers configured would fail at adjudication rather than run correctly, and a
check that fires on every correct run is a check that gets removed. Row added. The
survivor is recorded rather than quietly closed: a mutation set's value is entirely in
the ones that live.

### 17.5b A second survivor, in the WIRING category itself

`H3-w3` gave `_note_coarse`'s `agentic` parameter a default of `True`. All 500 rows
stayed green.

They stayed green *correctly*: all three call sites pass the argument explicitly, so
the default is unreachable and the mutation is a behavioural no-op **today**. But that
is exactly the reading that makes it worth recording. The signature currently encodes a
rule — *a caller that forgets the trigger gets a `TypeError`, not a silent `True`* — and
nothing tested that rule, so nothing would have noticed it being deleted. The next call
site added to `_note_coarse` would inherit "coarse-tier scans are agentic unless someone
remembers to say otherwise," which is the H3 finding's own shape re-entering through the
door H3 was about.

This is the WIRING axis pointed at a function's own signature. The mutation is not
refuted by any existing call site; it is refuted only by a call that omits the argument.
Row added: `test_H3_the_TRIGGER_cannot_be_OMITTED_by_a_future_call_site`, which calls
`_note_coarse` without `agentic` and requires `TypeError`. It asserts on the parameter's
*absence of a default*, which is the thing the mutation removed.

### 17.5c The mutation set caught a defect in a row written to catch that defect

`H4-d` re-introduces the K1 regression: key the nested-gitdir entry on the REAL path
instead of the synthetic tab-bearing one. Three rows went red — and
`test_H4_PARTNER_ordinary_git_use_does_not_move_the_NESTED_signature`, **the row whose
entire purpose is that regression, was not among them.** Its own docstring claims it
"caught a real defect."

Why it cannot fail, exactly:

```python
before = perm._git_control_entries(repo)     # path -> "G!"  (a KEY SET, and a constant)
...ordinary git churn inside .git/modules/sub...
assert perm._git_control_entries(repo) == before
```

`_git_control_entries` returns names mapped to the constant `GIT_CONTROL`. The K1
false-breach does not live there. It lives one function downstream, at
`permissions.py:711`, where `fingerprint` does `content[p] = _signature(root, p)` for
every entry key it was handed. With the synthetic key `.git/modules/\t<gitdir: sub>`,
`root / rel` names nothing on disk and `_signature` returns `("", EXACT)` forever. With
the real key `.git/modules/sub`, `_signature` sees a directory and stat-sweeps the whole
gitdir — `index`, `ORIG_HEAD`, `refs/`, the object store — so one `git commit` inside a
submodule moves it and the run reports a breach on correct behaviour.

Both keyings produce the **same key set**. The row compares the key set. It answers "did
the set of control-surface NAMES change?" when the question asked is "did the
control-surface SIGNATURE move?" — the recurring defect shape verbatim, in the row I
wrote to guard against the recurring defect shape, in the round whose subject is that
shape. I did not find this by reading it; I have read it several times. The mutation
found it.

Fixed by comparing what actually carries the failure: `perm.fingerprint(repo)` before and
after, asserting `before.content[k] == after.content[k]` for every git-control key. The
old key-set assertion stays — it is not wrong, only insufficient, and it is what refutes
a *different* mutation (an entry silently disappearing).

The general lesson, and it is the one worth carrying out of this round: **a control row
must be run against the regression it controls for, not merely aimed at it.** Three of
the four instrument defects found this round (§17.5, §17.5a, this one) were invisible to
review and visible to mutation on the first pass.

### 17.5d A third survivor: the depth cap stops measuring and says nothing

`H4-f` deletes the line that records
`.git/…\t<nested deeper than 4 gitdirs: not measured>` and returns silently instead.
All 500 rows stayed green.

The cap itself is fine — recursion into gitdirs has to be bounded, and four is generous
for a real repo. What the cap must never do is stop measuring *quietly*. The entry is
the whole reason a bounded sweep is honest: it converts "we did not look past here" into
a fact carried in the receipt, exactly as the COARSE tier does for regions past
`_IGNORED_SCAN_CAP`. Delete it and the receipt's silence about a region reads
identically to the silence it emits about a region it measured and found clean — which
is the absent-is-absent law (`usage.py`: "never invented, never zero-filled") applied to
coverage rather than to tokens.

Nothing tested it because the depth cap has no natural fixture: no repo in the suite
nests gitdirs four deep, so the branch was reachable only by construction. "No test
happened to build the shape" is how an unreachable branch stays unreached — the ROUTE
axis, again. Row added: `test_H4_a_gitdir_nest_PAST_THE_DEPTH_CAP_declares_itself_unmeasured`,
which builds five levels of `modules/` by hand and requires the declaration to appear
and to carry `GIT_CONTROL` so it flows through the diff like every other entry.

### 17.5e A fourth survivor: the ledger's lie, pointed the other way

`H8-d` makes the in-flight reason fire on the MECHANICAL lane too — `if True:` in place
of `if not spec.is_mechanical:`. All 500 rows stayed green.

H8 was the ledger claiming **zero where cost is unknown**. This is the same falsehood
inverted: claiming **UNKNOWN where zero is provable**. A mechanical phase has
`agent: null`; `_execute` returns at `runner.py:471` before `harness.run` is reached and
no harness is ever constructed. "No model invoked" is not a hopeful default on that lane
— it is the one absent-reason in the file that is *structurally* true. The mutation puts
phantom unaccounted spend into the cost ledger on the only lane that cannot spend, which
is how a cost ledger stops being read.

It survived because on the happy path the in-flight string is overwritten two statements
later by `phase.usage = total_usage`. The mutation is observable **only if a mechanical
phase's execution crashes**, and nothing in the suite crashes one. Same shape as `H4-f`:
the branch was reachable only by construction, and no fixture happened to build it. The
new row monkeypatches `_execute` to raise from exactly where a real crash would.

Four survivors in twenty-four, and all four are one species: **a rule the code states —
in a signature, a docstring, a declaration line, a lane guard — that no row asserts.**
None of them changed behaviour today. Each removes a guardrail the *next* change walks
into. That is the yield of a mutation set that is allowed to have survivors; a set with
none is usually a set that was scored generously.

### 17.6 The mutation table

Twenty-four mutations across five categories, run against a measured-green baseline
(500 passed). A mutation counts as caught only when the set of failing test NAMES grows.
The **first killer** column is the row that would actually have reported the defect —
recorded because "something went red" and "the row built for this went red" are
different claims, and this review is about exactly that distinction.

| # | Mutation | Verdict | First killer |
|---|---|---|---|
| H1-a | argv stops pinning the mode (ambient settings decide) | RED | `test_no_permission_skipping_flag_appears_anywhere` |
| H1-b | the pin is moved to the mode that disarms denials | RED | `test_H1_a_mode_the_workflow_did_not_pin_is_refused` |
| H1-c | `check_grant` stops adjudicating the mode | RED | `test_H1_a_mode_the_workflow_did_not_pin_is_refused` |
| H1-d | a missing init frame is assumed clean | RED | `test_H1_a_MISSING_init_frame_is_refused_not_assumed_clean` |
| H2-a | MCP tools nobody declared are tolerated | RED | `test_H2_MCP_tools_nobody_declared_are_refused` |
| H2-b | granted-vs-declared is not compared at all | RED | `test_H2_a_grant_NARROWER_than_the_declaration_is_refused` |
| H2-c | the grant is compared against ITSELF (tightest-looking no-op) | RED | `test_H2_a_grant_NARROWER_than_the_declaration_is_refused` |
| H2-d | the scoped form is sent raw to `--tools` | RED | `test_H2_the_SCOPED_form_survives_on_allowedTools_and_is_stripped_for_tools` |
| H2-e | `--strict-mcp-config` is dropped | **SURVIVED → RED** | `test_H2_the_ambient_MCP_servers_are_refused_on_the_ARGV_too` (§17.5a) |
| H3-w1 | `run()` stops passing `declared_tools` to adjudicate | RED | `test_H1_the_MODE_is_adjudicated_through_run_not_merely_sent` |
| H3-w2 | an unwired declaration compares against the empty set | RED | `test_H3_the_WIRING_of_declared_tools_fails_CLOSED` |
| H3-w3 | `_note_coarse` defaults its trigger to `True` | **SURVIVED → RED** | `test_H3_the_TRIGGER_cannot_be_OMITTED_by_a_future_call_site` (§17.5b) |
| H3-w4 | every `_note_coarse` call site passes `agentic=False` | RED | `test_C2_every_assert_under_tests_is_proven_to_execute` |
| H3-w5 | the post-gate call site omits the trigger | RED | `test_L6_paths_the_rollback_REFUSED_to_undo_are_named_in_the_receipts` |
| H4-a | nested gitdirs are not measured at all | RED | `test_H4_PARTNER_ordinary_git_use_does_not_move_the_NESTED_signature` |
| H4-b | only `worktrees/`, not `modules/` (the submodule hook stays live) | RED | `test_H4_PARTNER_ordinary_git_use_does_not_move_the_NESTED_signature` |
| H4-c | entry names only — no recursion into the child gitdir | RED | `test_H4_a_config_in_an_EXISTING_worktree_gitdir_is_measured` |
| H4-d | the entry is keyed on the REAL path (the K1 regression) | RED — **but not by the anti-K1 row** | `test_H4_a_NEW_gitdir_APPEARING_is_itself_the_change` (§17.5c) |
| H4-e | `config.worktree` drops off the closed list | RED | `test_H4_a_config_in_an_EXISTING_worktree_gitdir_is_measured` |
| H4-f | depth overflow is skipped silently instead of recorded | **SURVIVED → RED** | `test_H4_a_gitdir_nest_PAST_THE_DEPTH_CAP_declares_itself_unmeasured` (§17.5d) |
| H8-a | the `Phase` default reverts to the reassuring claim | RED | `test_C2_every_assert_under_tests_is_proven_to_execute` |
| H8-b | the construction argument is dropped | RED | `test_C2_every_assert_under_tests_is_proven_to_execute` |
| H8-c | the in-flight assignment is dropped | RED | `test_C2_every_assert_under_tests_is_proven_to_execute` |
| H8-d | the in-flight reason fires on the mechanical lane too | **SURVIVED → RED** | `test_H8_a_crashed_MECHANICAL_phase_is_not_billed_as_UNKNOWN` (§17.5e) |

**Final: 24/24 caught. Four survivors on the first pass** — `H2-e`, `H3-w3`, `H4-f`,
`H8-d` — each closed by a new row, and each new row re-run against its own mutation to
confirm it kills rather than assumed to (`/tmp/sl14_verify.py`). Plus `H4-d`, caught but
by the wrong row, now caught by the right one. Suite 500 → **504**.

Two rows in the H4 block (`H4-a`, `H4-b`) are killed FIRST by the partner control rather
than by the row built for the case. That is not a weakness in those two: the partner
opens with an explicit premise assertion (`nested gitdirs are not measured at all`)
precisely so it cannot pass vacuously when the surface it controls for has been removed.
A control that would go green if the thing it controls stopped existing is not a control.

**The first-killer column earned its place on `H4-d`.** A verdict column alone reports
`RED` there — caught, move on. The killer column reports that the row which caught it
was about gitdirs *appearing*, and that the row written for the K1 regression itself
stayed green (§17.5c). Both facts are true; only one of them is useful. That is the
review's own subject appearing in the instrument that measures compliance with it: a
binary predicate answering a slightly different question than the one asked, whose
comfortable answer happens to be correct and uninformative.


---

## 18. Round fourteen's Gate-2 verdict: the fence was a description of a fence

jack-ryan returned **PASS-WITH-CONDITIONS on the mechanical lane, BLOCK on the
agentic lane** (findings J1–J8). The founding run and determinism stand; the mechanical
lane is not held. The block is J1, and it is correct.

### 18.1 J1 — `--allowedTools` does not restrict, and I verified it myself

H1's thesis was "the argv is not the grant." The fix pinned and adjudicated the **mode**
and the tool **base names**. It did not adjudicate the **scope** — and scope is the half
that makes `Bash(git status:*)` a fence rather than a blank cheque.

I did not take this on jack-ryan's report. My own probe, `/tmp/sl_probe/p1.jsonl`:

```
$ claude -p "Run exactly one command: echo SCOPE_ESCAPED. Then stop." \
    --tools Bash --allowedTools 'Bash(git status:*)' \
    --permission-mode default --strict-mcp-config

INIT      mode=default  tools=['Bash']
TOOL_USE  Bash {"command": "echo SCOPE_ESCAPED"}
RESULT    is_error=False  denials=[]  stop=end_turn  result=SCOPE_ESCAPED
```

A phase declaring `tools: ["Bash(git status:*)"]` receives unrestricted shell,
auto-approved, and the receipt says the fence held. `--tools` is the real fence;
`--allowedTools` is inert in headless `default` mode. So `permission_denials` is
**still** structurally silent — for a different reason than the one H1 found, in the
fix for H1.

Three things in the code now measure as false:
- `validate_tools:113` — "Scoped forms are kept: `Bash(git *)` … is strictly narrower
  than `Bash`." False at the only place it is spent.
- module docstring:18 — "`--allowedTools` selects what may run without a prompt."
  In headless nothing prompts.
- `test_H2_the_SCOPED_declaration_is_compared_by_BASE_NAME` — **a row certifying the
  hole.** It asserts that declaring `Bash(git status:*)` against a grant of `Bash`
  returns `None`. I wrote it this round, in the fix for H1, as part of closing H1.

**The good half, also measured and previously unverified:** `--permission-mode default`
*does* override this host's `settings.json` `defaultMode: bypassPermissions`
(`INIT mode=default`), and `--strict-mcp-config` *does* strip the ambient `mcp__` tools.
The H1 pin and the H2 MCP fix are empirically sound. Round fourteen's largest claim and
its largest error were both settled by four minutes of running the real thing, after
several rounds of reading it.

### 18.2 J2 — the second dead row, demonstrated rather than argued

§17.5c found `test_H4_PARTNER_…` comparing a cheap proxy. jack-ryan found its
**ancestor** doing the same: `test_F3_partner_ordinary_git_use_does_NOT_move_the_control_surfaces`
(`test_containment_wall.py:1544`), whose docstring says *"If staging and committing
moved this signature, F3 would have re-landed K1 on a new axis"* — which it could not
detect. Proven by mutation: adding `("index", "refs/")` to `GIT_CONTROL_PATHS` is K1
verbatim at the top-level gitdir, and my new nested-gitdir partner went red on
`.git/index` and `.git/refs/heads` while the row whose whole job it was stayed green.

Fixed identically (compare `fingerprint().content`), and the fix re-run against that
exact mutation to confirm it kills: `KILLED -> 2 failed`. Suite 504.

So rule 28 generalises, and it needed applying twice. "Which other rows assert on a
helper when the failure lives downstream?" is now a standing audit question rather than
a closed finding.

### 18.3 What I accept, and what is not mine to decide

Accepted and queued in-seam: **J2** (done), **J3** (a retry discards *known* usage —
H8 inverted; `runner.py:341` overwrites accumulated `total_usage` on attempt ≥ 2),
**J4** (a declared repo whose `.git` is a FILE has no control surface — planting a hook
in its real gitdir needs no change to the pointer), **J5** (the grant adjudication
leaves no durable evidence: `permission_mode` / `granted_tools` reach `RawResult.extra`
and never reach the ledger, so on a passing phase the artifact holds no record of what
was granted — my own H8 rows state the rule the H1 fix does not follow).

Accepted on H6: the out-of-tree limit is architectural, **conditional on the limit being
named in the receipt** — same rule as the COARSE tier and the depth-cap entry, one level
up. And jack-ryan's amendment is right: `~/.claude/settings.json` is not ambient
background, it was H1's root cause; reading its `defaultMode` at run start and recording
it turns the round's largest finding into a measured precondition.

On H7: deferral was acceptable when the threat was theoretical. J1 fired the trigger —
with unrestricted `Bash`, size and mtime are both settable, so `touch -t` after an
equal-length rewrite of `.git/hooks/pre-commit` defeats the signature. Hash the F3/H4
control surfaces specifically, not the general fingerprint (the ~2.8k-dirty-path cost
argument is imported from a different population and does not cover three small files).

**Not mine:** the containment *posture*. With J1 fixed, the agentic lane's pre-hoc fence
is tool base names only and everything finer is post-hoc. Spec § 12 already rules out
sandboxes, so accept-and-state is the honest form of the posture the contract chose —
but stating it is Matt's call, not mine.

**Also not mine, and overdue:** a stopping rule. Fourteen rounds on a paragraph-long § 8
is over-delivery, and containment against an agent with shell access is not a finite
problem — "we found another one" will keep being available indefinitely. star-lord +
gandalf owe a stated threat model with an explicit boundary, as the exit criterion for
this series. J1 is the right last big one: it is the difference between a fence and a
description of a fence.

---

## 19. Round fifteen — J3, J4, J5/J5b, H7

Four Gate-2 findings and one migration. The through-line, stated once so the sections
below do not each restate it: **three of the four fixes carried the reported defect's own
shape one layer down.** J4's fix keyed the common-dir surfaces so they were protected in
no repo, while its docstring said they were protected. H7's fix hashed the bytes of a
file whose danger is its mode. J5's fix stored a grant nothing passed it. Each was found
by asking what the new code CLAIMS and then looking for the assertion that would notice
if the claim were false — not by any test that already existed.

### 19.1 J3 — a retry discarded what the previous attempt provably spent

`runner.py` set `phase.usage = UsageBreakdown.absent(in_flight)` at the top of every
agentic attempt. On attempt 1 that is exactly right and it is what H8 was for. On
attempt ≥ 2 it is H8 pointing backwards: attempt 1 can return real tokens and still
fail — a refused grant, a policy refusal, a malformed envelope all carry usage — and if
attempt 2 then raised, the ledger read NULL for a phase that provably spent.

`usage.py`'s opening law is one sentence with two halves: *tokens are never invented,
never zero-filled*. H8 closed the zero-fill half. J3 was the other half, and the module
had shipped `merge()` for precisely this and never called it.

Why the whole retry path was unreached: **none of the five H8 rows set `retries > 0`**.
Five rows on usage accounting, none of them on a second attempt. The SCOPE axis.

Fix: `UsageBreakdown.absent(in_flight).merge(total_usage)`. Order is load-bearing —
`merge` resolves `self.absent_reason or other.absent_reason`, so the in-flight reason
wins only as the receiver. The reason string also now distinguishes the two cases: on
attempt ≥ 2 it says the recorded tokens are attempts 1–(n−1) and **are NOT the phase
total**, because a partial sum an operator reads as a total is the same under-reporting
by a different route.

**A sub-finding I hit while fixing it, not reported by jack-ryan.** `one_line()` dropped
`absent_reason` the moment any number was present. So the newly-correct partial ledger
row printed on the operator's screen *identically to a complete one* — the fix would
have been true in the database and false on the display. `[INCOMPLETE: …]` suffix added.
Numbers alone are not a claim of completeness unless nothing is missing.

Mutations, full suite each, first-killer recorded:

| id | mutation | first killer |
|---|---|---|
| J3-a | `.merge(total_usage)` → bare `absent(in_flight)` | `test_J3_a_retry_does_not_DISCARD_…` (only row) |
| J3-b | drop the `[INCOMPLETE: …]` suffix | `test_J3_a_PARTLY_known_usage_…` (only row) |

Each killed by exactly the row written for it, nothing else. (`test_C2` also reds under
both — it is the reach-audit meta-row observing that the traced child suite is not
green, which is what it is for.)

**One process note, because it cost a diagnosis.** Both J3 rows first came up red for a
missing `UsageBreakdown` import in the *test* module — so the harness raised on attempt
1 and attempt 2 never ran. The rows were red for a reason with nothing to do with the
defect they target. Red is not evidence either; a row has to fail *for its own reason*.
The ledger row from that accident was itself reassuring: the crash-on-attempt-1 path
recorded the correct in-flight reason, which is H8 working.

### 19.2 J4 — `.git` as a FILE had no control surface, and the docstring argued it was fine

The `.git`-is-a-file branch filed the pointer as the single entry and justified stopping
there: *"its content is what would have to change to redirect anything."* True, and
beside the point. Redirecting the gitdir is one route to a hook. Planting one in the
gitdir the pointer **already names** is the other, and it writes not one byte of the
pointer file. Every linked worktree and every submodule — shapes this repo's workflows
create on purpose, and which `EnterWorktree` reaches without invoking git at all (H5) —
could take a `pre-commit` and report a clean tree.

Nineteenth instance of the shape, and the clearest so far *because the wrong question is
written down in the docstring*. The predicate answers "could this be redirected?" The
question is "could a control surface change?"

Three things the fix needed, and only the first is obvious:

1. **Follow the pointer.** Parse `gitdir: <path>`, resolve, enumerate. Every failure to
   resolve files an entry saying so — unreadable, unparseable, non-directory — because
   "we could not look" must not be stored as "there was nothing there", the same rule
   `_MAX_GITDIR_DEPTH` already follows.
2. **`commondir`, which is not optional.** A linked worktree's own gitdir does **not**
   hold the hooks git runs in it; `hooks/`, `config` and `info/exclude` resolve through
   the common dir. Enumerating only what the pointer names would have measured
   `config.worktree` and missed `pre-commit` — the file the mechanism is named after.
   A fix that covers the shape and misses the payload.
3. **A real-path map, or the fix is half of one.** Keys must stay under `.git/` (that is
   what `PROTECTED_EVERY_REPO` matches) while the *stat* follows outside the worktree.
   Without `_signature(…, real_path)` every such key resolves to nothing and signs as
   `""` forever: a hook **appearing** is still caught, because the key set moves, and a
   hook **edited in place** is caught by nothing. That half-fix passes the obvious test.

`test_J4_a_EDITING_…` exists for (3) specifically, and mutation J4-b confirms the
discrimination: under the half-fix the planting row stays **green** and only the editing
row goes red.

**And then I made the same mistake one layer down, in this fix, while writing it up.**
The common-dir surfaces were first keyed `.git\t<common>/…`. `_matches` protects by
literal `.git/` prefix — `path.startswith(bare + "/")` — and `.git\t…` does not start
with `.git/`. So they were not protected in any repo, while the docstring I had just
written claimed they "classify as the protected surface it is." Both J4 rows compared
`fingerprint().content`, which moves whether or not the key is protected, so both stayed
green. Found by reading `_matches` to check my own sentence — by no test.

The fix is one character (the tab moves after the slash). The real repair is
`test_J4_a_worktree_hook_is_a_BREACH_even_when_the_phase_may_write_everything`, which
asserts on `classify(…, writes=["**"])` rather than on the fingerprint. `writes=["**"]`
is the point: `PROTECTED_EVERY_REPO` means "never a legitimate phase write, whatever the
phase declared," so a permissive allowlist is the only condition under which the
protection does any work.

| id | mutation | killed by |
|---|---|---|
| J4-a | restore pointer-only (`out[".git"]`, return) | planting + editing + classification rows (PARTNER correctly green) |
| J4-b | `_content_sig` keyed off the fingerprint KEY, not the real path (the half-fix) | **editing row only** |
| J4-c | tab before the slash (key unprotected) | **classification row only** |

Three mutations; two of them die to exactly one row each, and to *different* rows. Each
J4 row is load-bearing for a distinct failure and none substitutes for another. (Re-run
in its post-H7 form after `_signature`'s `real_path` parameter was removed, so what is
certified is the code that exists rather than the code that used to.)

**Rule 29, for the README.** *Detecting a write and refusing it are two claims. A row
that asserts on the fingerprint has tested the first one only.* Rule 28 said a control
row must be RUN against its regression; 29 says an assertion has to reach the layer the
claim is about. Every "…and therefore it is protected/blocked/refused" sentence in this
module now owes a `classify` assertion, not a `content` one. That audit is not done — it
is the next thing I would look at, and it is a queue, not a finding.

### 19.3 J5 — the grant was adjudicated and then thrown away

`check_grant` reads `permissionMode` and `tools` out of the harness's init frame,
adjudicates them, and `record_agent_session` persisted none of it. On a FAILING phase
the verdict survives in `phases.error`. On a PASSING phase — the majority, and the ones
a later reader trusts — **nothing durable recorded what the fence had been**. The receipt
could say the phase succeeded and could not say what it was allowed to do while
succeeding.

This is J1's consequence, not a tidy-up. `--allowedTools` does not restrict in headless
`default` mode, so the argv is not evidence of the grant; the init frame is the only
place the real answer appears. Dropping it means the receipt cannot support the one
sentence the whole containment apparatus exists to let it say.

Five columns on `agent_sessions`, all nullable, no defaults. The NULL semantics are the
substance and are written into `factory/MIGRATION.md`:

- `granted_tools IS NULL` — no tool set was **reported**. Unknown.
- `granted_tools = '[]'` — an **empty** tool set was reported. Known, and known empty.
- `denial_count IS NULL` — no denials **reported**; it does **not** mean zero occurred.

`check_grant` turns on exactly the first distinction, so storing the list as a joined
string — which renders both as `""` — would have destroyed it. Absent-is-absent, moved
off tokens and onto containment evidence. A consumer writing `COALESCE(denial_count, 0)`
has converted "we do not know" into "it was clean", and rows J5-b and J5-c exist to make
that a test failure rather than a code review opinion.

Mutations (§ 19.7 covers J5-a, which survived pass one):

| id | mutation | killed by |
|---|---|---|
| J5-a | drop `result.extra` from the runner's call site | `test_J5_the_runner_CARRIES_the_grant_to_the_ledger` — **only** |
| J5-b | `granted_tools` zero-filled: absent stored as `'[]'` | `test_J5_a_MISSING_grant_is_stored_as_NULL_…` |
| J5-c | `denial_count` zero-filled: "none reported" stored as `0` | `test_J5_a_MISSING_grant_is_stored_as_NULL_…` |
| J5-d | restamp unconditionally (the original) | `test_J5b_an_OLD_database_is_MIGRATED_not_merely_RESTAMPED` |
| J5-e | migrate forward but do not refuse a NEWER db | `test_J5b_a_NEWER_database_is_REFUSED_rather_than_guessed_at` |

### 19.4 J5b — the schema version stamp could not disagree, so it could not refuse

Found while implementing J5, by asking what happens to the receipts DB that already
exists on this host (109 sessions).

`Receipts.__init__` ran `executescript(_SCHEMA)` and then UPSERTed the stamp from the
code's own constant, unconditionally. `CREATE TABLE IF NOT EXISTS` cannot add a column.
So opening a v1 database with v2 code leaves the v1 table shape untouched — and then
relabels it `2`.

The module docstring: the stamp exists *"so a Tier-2 consumer can refuse an unknown
version rather than guess at it."* A stamp its own writer overwrites on every open can
never disagree, so it could never refuse.

**Measured before it was claimed** — a probe opened a v1 DB with `SCHEMA_VERSION = 2`
and a new column:

```
stamp at v1: 1
stamp after v2 open: 2
permission_mode actually in the table? False
=> the stamp SAYS 2 and the table shape IS v1
```

Same shape as J1, and worse in one respect: J1 was a fence that did not restrain, this
was **the mechanism that was supposed to make schema drift detectable**. It is my own
seam's first discipline — validation at the boundary, #8 — failing inside the one
artifact whose entire job is to still be trustworthy months later. Nineteen rounds of
finding this in other people's reasoning did not stop me from shipping it in mine.

Order is now **read → migrate-or-refuse → stamp**. Additive `ALTER TABLE` only, because
a receipts DB is evidence and a migration that loses evidence is worse than no
migration. A NEWER DB raises rather than opening, **and is not restamped** — restamping
on refusal would destroy the fact that caused the refusal, so the retry would succeed
and be wrong.

Pre-existing rows are **not backfilled**. The grant for those sessions was never
measured and must read as unmeasured.

`factory/MIGRATION.md` authored (ADR-004) — first one this spine has needed, since v1
was the schema's birth.

**Note on the queue this opens.** v2 is the first migration, so `_MIGRATIONS` has one
entry and the refuse-a-newer-DB path has never run outside a test. That is honest
coverage, not proven operation; the first real v2→v3 is where the mechanism gets its
actual exercise.

### 19.5 H7 — a signature the phase can restore is not a signature

F3 and J4 settled *whether* `.git/`'s control surfaces are measured. H7 is about what
"measured" means for them.

Every entry in the fingerprint signed as `file:{size}:{mtime_ns}`. That is the right
trade for the ~2.8k dirty paths in the engine tree — hashing them per phase would cost
more than the phase — and it is the wrong trade here, because **both fields are settable
by the phase whose writes they exist to catch**. Matching a size is choosing the
payload's length. Restoring an mtime is `touch -t`. Neither needs anything beyond the
`Bash` the agentic lane already grants unrestricted, which J1 measured rather than
assumed. The adversary was inside the signature's own inputs.

Fix: the control surfaces — and only those, a closed handful rather than thousands — go
through `_content_sig`: sha256 of the bytes, plus the size, plus the permission bits,
with a 1 MiB read cap whose exceedance is **recorded in the signature string** rather
than silently truncating. Oversize falls back to stat and says so in the value.

**A side-effect worth naming.** Routing these entries away from `_signature` left its
`real_path` parameter — added by J4 one round earlier — with no call site. I removed it
rather than keeping it "in case": an argument nothing passes is a branch no test can
reach, which is the ROUTE axis this series keeps finding. That in turn meant rewriting
the J4 mutations into their post-H7 form, so the mechanism J4 certified stays certified
against the code that now exists rather than against the code that used to.

**H7-b survived the first pass, and that is the finding.** Dropping `st_mode` from the
content signature left the entire suite green. In plain terms: `chmod +x` on an inert
hook moved nothing. A non-executable `pre-commit` is harmless — that is exactly why
every fresh repo ships `pre-commit.sample` — and `chmod` writes not one byte, so size,
mtime and content hash are all unchanged. The measurement covered the file's CONTENT
while the question is whether the file EXECUTES. Different questions, and the wrong
answer is the safe-looking one. Nineteen-plus instances in, the shape recurred inside
the fix for the previous instance of the shape.

The mode was already in the code. What did not exist was any row that would notice its
absence, which is the same thing as it not being there.

Mutations, full suite each, killers recorded by name:

| id | mutation | killed by |
|---|---|---|
| H7-a | control surfaces fall back to `_signature` (size+mtime) | `test_H7_a_…`, `test_H7_b_…`, `test_J4_a_EDITING_…` |
| H7-b | drop `st_mode` from the content signature | `test_H7_b_a_hook_made_EXECUTABLE_without_editing_it_…` — **only** |

H7-b dies to its own row and nothing else in 525. H7-a is broader on purpose: dropping
back to `_signature` also un-does J4's real-path routing, so the worktree rows go with
it. Its own row is among the killers, which is what the claim needs.

Both rows are deliberately kept apart. A single row asserting "the hook moved" passes on
either mechanism and therefore certifies neither — the H4-d lesson (rule 30) applied
before the fact instead of after it. Each carries premise assertions that fail loudly
rather than passing vacuously: H7-a asserts the two bodies are the same LENGTH and that
the mtime actually restored (the first draft was two bytes off and said so); H7-b asserts
that `chmod` moved neither size nor mtime on this filesystem.

A K1 PARTNER control rides with them: fingerprinting twice with no write between must
not move a control surface. Hashing reads, and reading moves atime; had atime entered
the signature, every second snapshot would report a breach and the operator would learn
to click through the one alert that matters.

### 19.6 A defect in the instrument, again: the killer names were all `FAILED`

Pass two's harness printed `killers (2): ['FAILED', 'FAILED']`. The parser split on
whitespace *before* stripping the `FAILED ` prefix, so every name collapsed to the word
`FAILED`. Counts were usable; attribution was not — and attribution is the entire point
of recording a first killer (rule 30). A mutation harness that reports "something went
red" has told me what a bare exit code already told me.

Fixed and re-run. This is the third round in which the measuring instrument, not the
subject, carried the defect: a red baseline (17.5), a flat glob for the suite's own
subject (F7/F2), and now a report that could not name its own evidence.

### 19.7 The J5 survivor: a finding about wiring, undone by wiring

Pass one ran five J5 mutations. Four died. The one that lived was **J5-a — delete
`result.extra,` from the runner's call site.**

Four rows certified that `record_agent_session` correctly stores a grant it is handed:
the JSON round-trips, a missing grant lands as NULL rather than `'[]'`, an old DB
migrates, a newer one is refused. Not one of them certified that anything ever hands it
one. Cut the argument and the column silently takes its default; every row still passes;
the receipt is empty in exactly the case J5 was reported for.

This is the WIRING axis — the fifth of the five ways a defect stays unreached — arriving
on a finding whose entire subject was a value being adjudicated and then dropped. The
fix and the defect have the same shape one layer apart, which is now the third time this
round (J4's common-dir keys, H7's mode, this).

`test_J5_the_runner_CARRIES_the_grant_to_the_ledger` closes it, and it is deliberately
end-to-end: a stub harness returns an init frame, a real `_h3_run` executes, and the
assertion reads `permission_mode` and `granted_tools` back **out of the database**. A row
that asserted on the call arguments would have been another statement about the same
code, not about whether the wire exists.

---

## 20. Round sixteen — H6: what the receipt could not see

One finding, and it is not about the wall. Every round from twelve to fifteen asked
whether the wall catches a particular write. H6 asks the question one level up: **when
the wall reports that it caught nothing, what has actually been established?**

Two facts bound the answer, and neither is visible from inside a phase.

### 20.1 The ground the wall stands on

H1's root cause was never in this tree. `~/.claude/settings.json` on this host sets
`permissions.defaultMode` to `bypassPermissions` — outside the workflow, outside the
repo, and outside anything the factory configures. J1 then measured (twice, once by
jack-ryan and once independently by me) that `--allowedTools` does **not** restrict in
headless `default` mode, which is why v2 moved the grant record from the argv to the
harness's own init frame.

But v2 records what the harness reported *about itself*. Nothing recorded what the host
had already decided before the harness started. The receipt described the fence in
detail and said nothing about the ground it was standing on.

`factory/host.py` now reads that one setting at run start and stores it on the session
row with a `source` sentence. The sentence is load-bearing and is stored, not just
documented: Claude Code layers enterprise policy, CLI flags, environment, project
`.claude/settings.json`, `.claude/settings.local.json`, and the user file, and this
reads exactly one of them. Measured here: the user file says `bypassPermissions`; the
meta-repo's `.claude/settings.local.json` carries an `allow` list and no `defaultMode`;
there is no project `.claude/settings.json`. So the layers really do stack on this host,
and reporting one of them as *the* answer would be this series' own recurring defect —
a narrower answer wearing the wide one's clothes — committed in the fix for it.

Storing the caveat in the column rather than only in `MIGRATION.md` means a query that
returns the mode cannot separate it from what the mode is worth.

### 20.2 The trees the wall looked at

`fingerprint` measures `wf.repos`. A phase with unrestricted `Bash` reaches the whole
filesystem. Both are true at once and only the first appeared on the receipt, so "0
breaches" was a claim about a bounded region with the boundary printed nowhere.

`measured_trees` (JSON) and `measurement_limit` (a sentence) now sit on the session row.
The sentence ends *"A green verdict means 'no unauthorised writes HERE', not 'no
unauthorised writes'"* — and the falsification partner is the empty case: measuring zero
trees must not read the same as measuring two. A limit sentence that says the same thing
either way is decoration.

### 20.3 The zero-fill I refused

The tempting implementation records `"default"` when the settings file does not state a
mode, because that is Claude Code's own fallback and it would be right on this host.

It is `usage.py`'s opening law, arriving in containment evidence. Tokens are never
invented and never zero-filled; a mode nobody set is not a mode. Recorded as `"default"`
it would be correct on every host that never changed the setting and **unfalsifiable on
every host that did** — which is precisely the population the column exists to
distinguish. NULL, with a source sentence naming which kind of nothing it was: `UNREAD`,
`UNPARSEABLE`, `UNSTATED`, or (on a pre-v3 row) both columns NULL, meaning the run never
looked. Four different nothings, four different sentences.

The corresponding trap for a consumer is written into `MIGRATION.md`:
`COALESCE(host_permission_mode, 'default')` converts "we did not measure" into "the host
was ordinary."

### 20.4 The green path is the only path that matters here

The obvious place to render this is next to the breach list. That placement is worthless
and it is worth saying why: the breach section only exists when something went wrong, so
a caveat living inside it is a caveat no reader of a green report ever sees. Green is
exactly where the over-claim happens. `render_run_report` emits
`## What was measured — and what was not` on **every** run.

The row that holds it there asserts its own premise — `"Permissions breaches" not in
text` — so it cannot pass by finding the caveat inside a breach section that happens to
be present.

### 20.5 The ROUTE row, written before the mutation instead of after

Five host-reading rows pass an explicit path. All five would stay green if
`read_host_permission_mode()`'s no-argument default pointed at a file that does not
exist — the production route unreached, which is the axis this series keeps landing on.

So `default_settings_path()` resolves `Path.home()` at **call** time rather than at
import, and one row moves `Path.home()` and watches the real default follow it. A
module-level constant would have been marginally tidier and structurally untestable.

H6-e is the mutation for it (make the path import-time again), and it dies to that row
and to nothing else in 538. This is the first round where the ROUTE row was written
because the axis was anticipated rather than because a mutation survived.

### 20.6 The mutation table

Five mutations, full suite each (538 rows, reach-audit excluded as always), first
killers recorded by name.

| id | mutation | killed by |
|---|---|---|
| H6-a | the run never reads the host default | `test_H6_a_RUN_records_the_host_default_it_ran_under`, `test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches` |
| H6-b | an UNSTATED mode is filled with `"default"` | `test_H6_an_UNSTATED_host_default_is_NULL_not_the_fallback`, `test_H6_a_NON_STRING_mode_is_refused_rather_than_stringified` |
| H6-c | the run records trees but drops the limit sentence | `test_H6_a_RUN_records_the_trees_it_actually_fingerprinted`, `test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches` |
| H6-d | the caveat renders only where breaches already render | `test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches`, `test_H6_an_UNRECORDED_measurement_reads_as_unrecorded_not_as_clean` |
| H6-e | the production default resolves at IMPORT | `test_H6_the_PRODUCTION_default_path_resolves_through_the_users_home` — **only** |

Every mutation dies, each to the row written for it, and H6-e dies to exactly one row —
no other row substitutes for the ROUTE claim. H6-a and H6-c each take the green-path
render down with them, which is correct: a caveat rendered from a column nothing fills
is a caveat that reads UNRECORDED, and the row asserting the value is present notices.

No survivors this round. That is the first round since eleven with none, and I do not
read it as the suite having gotten strong — I read it as H6 being a smaller finding than
J4 or H7. It adds columns and a sentence; it does not change a predicate.

### 20.7 Schema v3, and what it does not close

`MIGRATION.md` carries the v2 → v3 section (ADR-004). Additive: four nullable columns on
`sessions`, automatic on `Receipts.__init__`, every v1/v2 query unchanged, pre-existing
rows NULL and never backfilled. The v2 section's "Known gap, stated rather than closed"
paragraph — which named H6 — is marked closed rather than deleted, because a gap that
was open for a version is part of what a v2 row means.

What v3 does **not** close, stated rather than implied:

- The **effective** permission mode is still not resolved. One layer is read. The other
  five are named in every stored `source` value and in the migration note.
- Nothing here restricts anything. It is measurement of the measurement. The v1
  containment posture (base-names-only, pre-hoc) is unchanged and remains Matt's call.
