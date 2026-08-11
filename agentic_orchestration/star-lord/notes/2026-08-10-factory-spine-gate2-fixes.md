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

**Signed:** star-lord — operational-pipeline seam (export · output · telemetry · LLM)
