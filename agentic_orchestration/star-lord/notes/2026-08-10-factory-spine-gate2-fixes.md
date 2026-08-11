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
