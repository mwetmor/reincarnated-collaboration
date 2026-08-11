# Finding — 2026-08-10 — factory-spine-v1 (Gate 2, VERDICT RESTATEMENT / round three)

**Reviewer:** jack-ryan
**Severity:** **CONDITION DISCHARGED · LANE RE-CONDITIONED** — one new BLOCK-class defect (H1), two WARN, two INFO
**Target:** `agentic_orchestration/factory/` @ `801b7cea` (diffed against `d68a4072`)
**Developer:** star-lord (builder, ruling D4)
**Supersedes:** `2026-08-10-factory-spine-gate-2-rereview.md` (BLOCK LIFTED, CONDITIONALLY)
**Remediation note reviewed:** `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` § 8
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate / evidence), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** 8 (schema validation at boundaries), 11 (empirical inspection over assumption), 12 (semantic-shifting fixes need explicit framing)

---

## Verdict

**The round-two condition is DISCHARGED. The lane is re-conditioned on a different,
narrower condition.**

> **Round-two condition (`whole git repositories`) — DISCHARGED.** G1's fix enforces
> it mechanically, at two independent layers, and it survived every bypass I could
> construct including a symlink indirection. star-lord was right not to assume this;
> he is right to now have it.

> **New condition (H1).** **No phase may declare a `writes` pattern that matches
> paths inside a declared `read_only_trees` entry.** In practice: `writes: ["**"]`
> is forbidden for any phase in a workflow that declares a read-only tree. Outside
> that shape the agentic lane is authorized.

The condition changed rather than lifted because I found a third defect of the
module's recurring shape, and I found it in the *shipped* configuration. That is a
finding about the module, not about a line, and I say so in § H1 and § "The pattern."

**Mechanical lane: remains approved, unchanged.**

---

## What I reproduced (verified, not accepted)

| Claim | Result |
|---|---|
| 170 tests green | **REPRODUCED** — `170 passed in 3.60s` |
| `./factory run` PASS ~1m15s | **REPRODUCED** — 3 phases, 14 verdicts, all green |
| `DETERMINISM: EXACT — 14 verdicts identical across two laps` | **REPRODUCED** — 14/14, on a quiet tree, 2m27s for the pair |
| Three `containment: coarse` declarations for godot `.godot/` + `Assets/Synty/` | **CONFIRMED** — and the engine tree still fingerprints with **zero** coarse regions |
| Engine dirty 2789 / godot dirty 233 unchanged | **CONFIRMED** — before and after every probe below |
| No `__pycache__` written into the engine tree | **CONFIRMED** |

---

## 1. G1 — DISCHARGED. I attacked it three ways; it held all three.

**(a) The load refusal, with nothing planted.** My own round-two probe, re-run:

```
workflow rejected at load: declared repo …/src/reincarnated/telemetry is a SUBDIRECTORY
of the git worktree at /Users/admin/Games/reincarnated-engine. … Declare
`/Users/admin/Games/reincarnated-engine` and scope the phase with `writes:` instead.
=== ARTIFACT SURVIVE? === No such file or directory
```

The phase never executed. Nothing to delete by hand this time. The error names the
worktree root to declare instead, as required.

**(b) Symlink bypass of the load refusal — REFUSED.** I built
`/tmp/jr3/link_subdir -> engine/src/reincarnated/telemetry` and declared the link.
`workflow.py:231-232` resolves `repos:`/`read_only_trees:` before validation, so the
loader saw through it and refused with the *real* path named. This is the bypass I
most expected to work.

**(c) Defense-in-depth, called directly — FAILS CLOSED.** The loader is not the only
caller, so I called the lower layer myself:

```
engine/src/reincarnated/telemetry -> usable=False | entries=0 | err=… is not a git worktree root …
/tmp/jr3/link_subdir              -> usable=False | entries=0 | err=… (same, resolved)
/Users/admin/Games/reincarnated-engine -> usable=True | entries=2907
diff_fingerprints(subdir, subdir) -> ContainmentError
```

`usable` is `is_git and error is None`, and the G1 branch populates `error`, so the
F2 guard now actually fires on this path. The round-two defect — *"F2's fail-open
wearing a passing guard"* — is closed at the source, not only at the loader.

## 2. G2 — DISCHARGED for the direct case, and the rollback is real this time

Nested read-only tree, whole repos declared, `writes: ["**"]`:

```
PERMISSIONS BREACH during gate execution — aborting the run (a breach is evidence, not a retry)
  src/reincarnated/telemetry/jr3_g2.txt (created) — write inside a read-only tree (…/telemetry)
  rollback: src/reincarnated/telemetry/jr3_g2.txt -> deleted
ABORTED: permissions breach during gate execution: 1 path(s) outside the allowlist
=== DID jr3_g2.txt SURVIVE? === No such file or directory
```

Compare round two, where the identical probe printed `-> deleted` and the file was
still on disk. The receipt and the world now agree. **This is what discharges the
round-two "narrower read-only tree" fallback as safe** — with the H1 exception below.

## 3. H1 — **BLOCK-class (new)** — a symlink into a read-only tree escapes the read-only fence, and the run greens

**File:** `permissions.py:393-412` (`_read_only_hit`)
**Pinned by:** nothing. `grep -rn "symlink\|symbolic" tests/` returns **zero hits**.

`_read_only_hit` computes `full = (change_root / rel).resolve()` and asks whether
`full` lands in a read-only tree. `.resolve()` follows symlinks. So for a symlink
whose *target* is outside the read-only tree, the function answers a question about
the target's location instead of about the link's location — and returns `None`.

**Proven live, on the shipped whole-repo shape** (`read_only_trees: [engine]`):

```
-- phase 1/1: symlink_out_of_readonly_tree [mechanical]
   OK   command_succeeds: PASS -- `ln -sfn /tmp/jr3 …/reincarnated-engine/jr3_h1_link` exited 0
   OK   diff_matches_claims: PASS -- change-set (0 path(s)) is a subset of the 0 claimed
   OK   verdict_consistent: PASS -- envelope claims PASS and all 2 prior gate(s) are green
run jr3-h1-symlink-escape -> PASS
=== DID THE SYMLINK SURVIVE INSIDE THE READ-ONLY TREE? ===
lrwxr-xr-x 1 admin staff 8 Aug 10 20:28 …/reincarnated-engine/jr3_h1_link -> /tmp/jr3
=== engine dirty count (baseline 2789) === 2790
```

**Control, identical workflow, `ln -sfn` replaced by `touch`:**

```
PERMISSIONS BREACH — jr3_h1_regular.txt (created) — write inside a read-only tree (…/reincarnated-engine)
  rollback: jr3_h1_regular.txt -> deleted
ABORTED
```

One is a symlink, the other is a regular file. Same workflow, same allowlist, same
tree, opposite verdicts. The cause is isolated: **`.resolve()`, and nothing else.**

**Scope of exposure — why the condition and not a re-BLOCK.** The read-only check runs
*first* in `classify`; when it misses, the `writes` allowlist is the only remaining
fence. With the shipped `writes: []` the symlink still breaches (see H3), so **the
shipped mechanical workflow is not exposed**. The exposure is exactly: a phase whose
`writes` pattern covers the path. That is a describable, avoidable configuration,
which is why it becomes a condition rather than a fresh BLOCK on the whole lane.

**But do not read the exposure as exotic.** `read_only_trees` is the *only*
repo-scoped fence the spine has (H4), the godot tree already ships **132 symlinks**
as its established asset layout, and `ln -s` is ordinary work for an agent holding
Bash. I checked the 132: all resolve *inside* the godot worktree, so no pre-existing
escape hatch exists on this host today. The hazard is a link an agent creates, not
one already there.

**Path forward — two lines, mirroring the bidirectional matching star-lord already
wrote for G2.** Test **lexical** containment as well as resolved containment, and
breach if *either* lands in a read-only tree. Verified against the live case:

```
lexical path : /Users/admin/Games/reincarnated-engine/jr3_h1_link
lexical in RO tree? True     <-- proposed check catches it
```

Keep the resolved check too — it catches a symlinked ancestor pointing *into* a
read-only tree. Then add the falsification partner the suite has never had: **a
symlink created inside a read-only tree must breach.**

## 4. H2 — WARN (new) — a nonexistent `read_only_trees` entry loads clean and enforces nothing

**File:** `workflow.py:302-315` (`_validate_containment`)

F2's load fix validates that every `repos:` entry exists, is a directory, and is a
worktree root. `read_only_trees:` entries get only the coverage check — and coverage
is decided by pure path arithmetic (`ro == r or r in ro.parents`), which a
nonexistent path satisfies perfectly:

```
path exists? False
LOAD: ACCEPTED  <-- read-only claim on a path that does not exist, enforces nothing
```

A typo (`.../telemetrry`) yields a workflow that *declares* a read-only tree, passes
every load check, prints no diagnostic, and fences nothing. This is F2's own sentence
— *"a read-only tree that nothing fingerprints is a promise nobody checks"* — applied
to the half of the check that did not get the existence test. Cheap fix: require
`ro.exists()` and `ro.is_dir()` at load, same as `repos:`.

## 5. H3 — WARN (new) — `rollback` cannot remove a symlink, and the artifact survives the abort

Same probe with the shipped `writes: []`. The breach **is** caught (by the allowlist,
with the read-only reason missing per H1) and the run aborts — but:

```
rollback: jr3_h1_link -> NOT_ROLLED_BACK
BREACH.json: "reason": "delete failed: Cannot call rmtree on a symbolic link"
```

`shutil.rmtree` refuses symlinks, so the link stays on disk. **The receipt is honest**
— it says NOT_ROLLED_BACK and gives the reason, which is the opposite of round-two
G1's lying `deleted` — so this is WARN and not BLOCK. But a surviving symlink is the
single worst artifact to leave behind, because it is a durable escape hatch that
outlives the aborted run and is invisible to H1's fence on the next one. Fix:
`Path.unlink()` when `is_symlink()`, before the `is_dir()` branch.

## 6. H4 — INFO (new) — `writes` patterns are repo-agnostic, which concentrates all cross-repo containment on the mechanism H1 holes

`classify` matches `writes` against `change.path` with no repo qualification (proven
incidentally by the H1 probe: `writes: ["**"]` declared in a meta-repo phase permitted
a change whose `change.root` was the engine). `protected` is root-repo-only by
design. So `read_only_trees` is the **only** fence that distinguishes one repo from
another — which is why a hole in it is worth more than its narrow trigger suggests.
Not a defect on its own; worth one sentence in the README so an author does not read
`writes:` as repo-scoped.

## 7. H5 — INFO (new) — the co-tenancy label is name-based and can excuse a real phase write

I planted `jr3_evil.db-wal` deliberately, from the phase, with `writes: ["**"]`:

```
PERMISSIONS BREACH … jr3_evil.db-wal (created) — write inside a read-only tree
  rollback: jr3_evil.db-wal -> deleted
  NOTE: 1 breaching path(s) look like another process on this host, not this phase
ABORTED … — 1 of them look like host co-tenancy, not this phase
```

**The label is verdict-inert** — I checked this specifically, because a label that
softens a verdict would be an exemption wearing a diagnosis. It is not: still FAILED,
still rolled back, still ABORTED, still exit 1. Correct construction. The residual
INFO is that the diagnosis itself can be wrong in the excusing direction, and an
operator who trusts it may re-run instead of investigating. One hedging word
("may be host co-tenancy — verify") costs nothing.

---

## Rulings on the three questions asked

### G3 — is diagnose-don't-exempt the right call for a Gate-2 pass? **Yes. And no, it does not block.**

star-lord's reasoning is correct and I endorse it without reservation. Exempting
`-wal`/`-shm` would have been F1's defect in its third costume: a *category*
exemption bought to make a red go away. He named the tell himself in § 3 and then
declined to trip it when it was his own run's convenience at stake. That is the
discipline working.

**It does not block, and the reason is directional.** G3 fails **closed**. A gate
exists to prevent a green over a broken world; it does not exist to guarantee
uptime. An abort that should not have happened costs a re-run. A green that should
not have happened costs the founding run's credibility. G3 is entirely of the first
kind.

**But it is not free, and it is not a code item.** `DETERMINISM: EXACT` is presently
a property of **host quiescence** as much as of the instrument — I demonstrated that
in round two by killing both laps with a read-only query from my own session. This
belongs in the founding run's operating plan, not in the module:

- **Route to knight-rider:** the founding run needs a host-quiet window on the
  engine and godot trees — no other agent session reading an engine DB, no editor or
  language server indexing those trees — for the duration.
- **Route to Matt (informational, not a decision):** the founding run can die from
  another agent merely *reading* a database. That is the accepted cost of D5
  sandboxes being deferred, and the honest v1 statement of it.

### G5 — does it block? **No.**

INFO, unchanged from round two. A collapsed-directory breach is **detected** and the
run **aborts** — the load-bearing half — and rollback declines for a safe reason that
is merely imprecisely worded. Nothing greens. Not a gating item; fix it when the
receipt text is next touched.

### Is the round-two condition discharged? **Yes — see § 1. It is replaced, not removed.**

---

## The pattern — this is now a finding about the module

You asked me to say plainly if I found a third instance. I did, and this is the
fourth if you count F1 as the first of the family:

| # | Where | The shape |
|---|---|---|
| F1 | `fingerprint` via `git status` | measured a *category* it never looked inside → reported clean |
| G1 | `_is_git_worktree` via returncode | measured against the *wrong base* → reported clean |
| G2 | `classify` via `change.root` | measured at the *wrong granularity* → reported clean |
| **H1** | `_read_only_hit` via `.resolve()` | measures the *wrong target* → reports clean |

Every one is a containment predicate that answers a slightly different question than
the one it was asked, and whose wrong answer is **"clean."** Four times in one
module, and **three of the four were pinned by a passing test that asserted the
reduced behaviour was the requirement** — which is why 136, then 164, then 170 green
did not surface any of them.

**Discipline #12 recommendation, and it is the durable fix here — not another patch.**
`permissions.py` needs one stated invariant it can be tested against as a class
rather than instance by instance:

> *Every containment predicate must be falsifiable by a planted artifact, and its
> failure mode must be "breach," never "clean."*

Concretely: a single parametrised falsification wall that plants one artifact of each
kind — regular file, symlink, nested directory, collapsed-ignored-directory member,
gitignored file, subdirectory-declared repo, unreadable subtree — inside a declared
read-only tree, and asserts each one breaches. Seven cases, one table. Three of the
four defects above would have been caught by that wall on the day it was written, and
H1 is the proof that reviewing instance-by-instance is not converging: I have now
found one per round, in three consecutive rounds, in the same file.

This is my recommendation, not a BLOCK condition. **H1 alone discharges the new
condition; the wall is what stops a round four.**

---

## Action

- [ ] **star-lord — H1 (discharges the new condition):** make `_read_only_hit` test
      lexical containment as well as resolved containment; breach on either. Add the
      falsification partner: *a symlink created inside a read-only tree must breach.*
      **Discharges when** my H1 probe aborts and the link does not survive, proven by
      a live run.
- [ ] **star-lord — H3 (fix with H1; same probe proves both):** `unlink()` symlinks in
      `rollback` before the `is_dir()` branch, so the abort path leaves nothing behind.
- [ ] **star-lord — H2:** require `read_only_trees:` entries to exist and be
      directories at LOAD, as `repos:` entries already must.
- [ ] **star-lord — the falsification wall (recommended, non-gating):** one
      parametrised table over the seven artifact kinds. This is the item I would
      prioritise over any individual INFO below.
- [ ] **star-lord — H4/H5, G4 residual, G5:** non-gating. (G4 is substantively closed —
      `_note_coarse` now fires at all three snapshots; the dedup key is the caveat text,
      so a receipt still reads `phase start:` only when the regions are unchanged. A
      region crossing the cap mid-phase *is* declared, which was the point.)
- [ ] **star-lord — F3/F4/F5/F6/F7/F8 (round one):** still open, still non-gating. **F4
      (`permission_denials` dropped before the receipts) should land with H1** — it is
      the record of an agent attempting a tool use it was not permitted, on the lane
      this verdict opens.
- [ ] **knight-rider:** the founding run needs a declared host-quiet window on the
      engine and godot trees (G3). This is a scheduling precondition, not a patch.
- [ ] **Matt — decision needed:** **none to authorize the lane.** H1–H3 are
      developer-fixable defects, so this stays within my authority per ADR-002. Two
      items already correctly routed to you and unchanged: **O4** (drop vs. keep the
      dollars figure — gandalf and I ruled opposite ways) and **D-10** (no HALT
      status), still the largest remaining gap for the founding run, and still wanting
      a dispatch rather than a patch. **Informational:** G3 means the founding run can
      be killed by another agent reading an engine DB; that is the honest cost of D5
      deferral.
- [x] **jack-ryan:** round-two condition discharged. Mechanical lane approved,
      unchanged. Agentic lane authorized for workflows declaring whole git
      repositories, **excluding any phase whose `writes` pattern covers a declared
      read-only tree** — that exclusion lifts on H1.

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflow.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/runner.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_permissions.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_workflow.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflows/kc2-baton-mechanical.yaml`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md`
- Probe workflows: `/tmp/jr3/g1_subdir.yaml`, `/tmp/jr3/g1_symlink.yaml`,
  `/tmp/jr3/g2_nested.yaml`, `/tmp/jr3/h1_symlink_escape.yaml`, `/tmp/jr3/h1_control.yaml`,
  `/tmp/jr3/h1_narrow.yaml`, `/tmp/jr3/g3_cotenancy.yaml`
- Probe evidence (in-tree, gitignored) under `factory/sessions/`:
  `jr3-g2-nested-20260811T002614Z-8dbcaf/` (G2 closed — breach, real rollback)
  `jr3-h1-symlink-escape-20260811T002754Z-a083ac/` (**H1 — run PASS, symlink survived**)
  `jr3-h1-control-regularfile-20260811T002815Z-3b0bb5/` (H1 control — regular file breaches)
  `jr3-h1-narrowwrites-20260811T002821Z-d34a8a/` (H3 — `NOT_ROLLED_BACK`, link survived)
  `jr3-g3-cotenancy-20260811T002940Z-aaed39/` (G3 label is verdict-inert)
  `kc2-baton-mechanical-20260811T0031…` ×2 (determinism EXACT, 14/14)

**Post-review state:** all probe artifacts removed by hand where the factory did not
remove them. Engine dirty **2789**, godot dirty **233** — both at baseline.
