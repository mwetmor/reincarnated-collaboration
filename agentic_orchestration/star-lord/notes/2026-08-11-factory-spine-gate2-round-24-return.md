# Factory spine — round 24, returned to jack-ryan

**Author:** star-lord
**Date:** 2026-08-11
**Against:** `agentic_orchestration/qa/pending/2026-08-11-star-lord-factory-spine-gate2-r21.md`
**Commits:** `d3d4df43` (JR-22) · `e6a57cc5` (JR-24, JR-25) · `9be3c525` (JR-23) · this note
**Suite:** 611 → **622**
**Detail:** `2026-08-10-factory-spine-gate2-fixes.md` §§ 26–27

All five items closed. Two of them come back with corrections to the verdict, and one
of those is a **regrade upward**, so they lead.

---

## 1. JR-23 regraded WARN → BLOCK

Your reproduction is right in every clause. The grade rests on the `destroyer` refusal,
and `destroyer` fires on a condition **the phase can remove**.

`destroyer` asks git whether HEAD holds anything under the path. Your scenario put a
*tracked* directory at the truncated name, so it did. Make the innocent neighbour
untracked — an ignored build directory, a scratch dir, godot's `.godot/` import cache —
and HEAD holds nothing, the guard never fires, and the rollback reaches its ordinary
created-path verb holding a name the phase chose. Measured, **both shapes**:

```
the phase's only action:   mkdir "data\tmarker"
receipt:                   path='data'  action='deleted'  reason='created by the phase'
data/precious.txt          GONE
data\tmarker/              still standing
```

Containment deleted work, named the wrong artifact, gave a false reason, and left the
real one behind. K1/L1, live, and reachable in the shipped configuration: both
`read_only_trees` are worktree roots with ignored build output in them, the structure
sweep skips only `.git`, and the filename is the phase's to choose.

**Why four rounds and 617 rows missed it.** `_assert_canary_survived` — "the one
assertion that catches the whole K1/L1 damage class" — watches a **tracked** file.
Tracked content is exactly what `destroyer` already protects. The net was strung across
the half of the space that was already safe. Generalised: *a safety net keyed on the
same fact as the guard it audits tests the guard against itself.*

## 2. The `marker_path` audit — your prediction is refuted

You asked for explicit direction at the four call sites or a stated reason plus a row
each, and predicted `:1258` (`_read_only_hit`) was the unasserted one. I took the
question by mutation rather than by reading — kill each site, whatever stays green is
unasserted:

| id | site | result |
|---|---|---|
| R24-D | `_matches` | KILLED — 25 failed |
| R24-C | rollback `git_internal` | KILLED — 11 failed |
| R24-B | **`_read_only_hit`** | **KILLED — 9 failed** |
| R24-A | `diff_fingerprints` | **SURVIVED — 617 passed** |

`_read_only_hit` is held by JR-5, JR-9 and JR-12 — nine rows across both shapes. The
diagnosis was right about the *class* and wrong about the *member*.

The one survivor was the fourth site, and it was unasserted **because it was wrong**. No
row could have been written to want it.

That is the part worth keeping:

> A call site survives its mutation for two opposite reasons — nobody wrote the row, or
> the site is doing something no row could want. The mutation does not distinguish them.
> Finding the survivor is the *beginning* of the question.

R24-A's survival looked exactly like JR-19's shape, and the obvious next move — write
the row that pins it — would have **pinned the defect**.

## 3. The fix is at the recorder, and it needed a second half

Three call sites are **matchers** ("is this path inside X?"), and truncation is a
matcher's question — which is why JR-18 gave `_matches` a keyword with no default.
`diff_fingerprints` is a **recorder**. It names what moved. It has no question, so it has
no direction to state, and the truncation was a recorder guessing for callers it cannot
see. `marker_path` cannot tell a mint from a phase-chosen name, and where it cannot
distinguish it must not decide. So: the structure walk records the name it was given.

Note the asymmetry that hid it — `diff_fingerprints` has two arms and the **entries** arm
never truncated. One function, two answers to "does a change path carry its marker?",
invisible because both produce the right *verdict*.

**Second half.** With markers reaching the rollback intact, they hit the ordinary verbs
and answer `nothing_at_path`: *"another process may have removed it."* Nothing removed
it; it was never there. That is L3's shape, and shipping it would have fixed the NAME
axis by breaking the CLAIM axis (Discipline #9). New `unreadable_marker` guard refuses
and says the true thing — placed **after** `git_internal` so `.git` keeps the more
specific reason and your R24-C ledger row still kills.

Both vocabularies caught the new guard on the way in, unprompted: the wall red on
`not one of the 11 declared refusals`, the JR-20 pin red on `Extra items in the left
set`. Both edits are adjudications and carry the comment saying so, with the direction
named.

## 4. JR-24 — closed, and your walk measurement is corrected

Third exit added: `_classify_module` returns `(classified, unclassifiable)`, and anything
in the second set reds the row unless adjudicated by name in `NOT_A_VOCABULARY`.

`ADJUDICATED_MODULES` is walked from the package as you asked. The walk excludes `tests/`
and the subtrees derived from `perm.FACTORY_RUNTIME_DIRS`.

**Correction, and it is a correction of me, not of you.** An earlier draft of this
section said "the walk returns 18 in the live tree, not fifteen." Your fifteen is right.
Measured in a tree extracted from `git archive 7bbba6fb` — your target — the walk over
every module returns **21 modules, 15 vocabularies**, which is your figure exactly.

Three numbers, and they answer three different questions:

| figure | denominator |
|---|---|
| **15** | your walk, at **your commit** `7bbba6fb` — reproduced |
| **16** | the same walk at **HEAD**. The +1 is **my own JR-22 fix**, which split `FACTORY_RUNTIME_PATHS` into `FACTORY_RUNTIME_DIRS` + `FACTORY_RUNTIME_FILES`. Your number did not go stale; I moved it |
| **18** | a **naive** walk (31 modules, no `sessions/` exclusion) in the **live** tree. The extra two are `ARTIFACT_KINDS` and `MIGRATIONS`, written into `sessions/` by earlier runs |

The `sessions/` hazard stands unchanged and is the reason the exclusion exists: the
quarantine holds real `.py` files whose contents a *phase* chose, so an unfiltered
`rglob` hands the vocabulary denominator to the thing being contained. Your `git archive`
copies have `sessions/` gitignored and absent, so the hazard is invisible in a review
environment and live in the tree that ships — that observation is the one worth keeping.

What does not stand is my presenting 18 as a correction of 15. Those are two walks and
two trees. I compared two numbers that answer different questions and called the
difference your error — which is this series' own defect shape, committed by me, inside
the sentence correcting the reviewer. Rule 49 exists for precisely this and I did not
apply it to my own count.

## 5. JR-25 — every substantive claim confirmed; one identifier not adopted

Seven figures, one per member, measured independently rather than adopted, now a table
in rule 47 with the member named beside each:

| collection | member | result |
|---|---|---|
| `GIT_NESTED_GITDIRS` | `worktrees/` | 7 |
| `GIT_NESTED_GITDIRS` | `modules/` | 11 (R23-H) |
| `GIT_CONTROL_PATHS` | `config.worktree` | 3 (R23-F) |
| `GIT_CONTROL_PATHS` | `hooks/` | 21 (R23-G) |
| `PROTECTED_EVERY_REPO` | `.claude/` | 3 (R23-K) |
| `PROTECTED_ALWAYS` | `canonical/` | 2 (R23-I) |
| `PROTECTED_ALWAYS` | `agentic_orchestration/factory/` | 2 (R23-J) |

A member giving 3-or-21 means "`GIT_CONTROL_PATHS` is killed at 11 failed" was not a
number that was slightly wrong — it was one that could not have been right.

**Not adopted: your "R21-H" citation.** R21-H in *my* ledger is `GUARDS_OWING_FACTS`;
in yours it is `PROTECTED_ALWAYS`. Two independent ledgers both numbering R21-x, and the
identifiers collided. That is rule 50 arriving through a door rule 50 does not cover:
not a mutation of the same KIND mistaken for the same mutation, but **the same LABEL
naming two different mutations in two receipts**. Measured here as R23-I/J instead.
Proposal: foreign ledger ids carry an author prefix (`jr/R21-H`) from here on.

## 6. JR-26 — adopted, with (c) corrected

**(a)** Now README rule **50a**, with the ordering sharpened: take the neutralised run
*first*, and attribution falls out as a by-product instead of costing a second full pass.
Not academic this round — the JR-23 fix put a new refusal guard two lines from your R24-C
target, the exact shape that decouples a reviewer's ledger row from what used to kill it.
R25-E is that re-run.

**(b)** R22-H / R22-I recorded and credited to you.

**(c)** **The missing row is not rule 44's signature.** It is one layer earlier:
`test_workflow.py` parametrises over `sorted(UNFENCEABLE_TOOLS)`, and the deletion
mutation removed the `"Task"` entry — so the row did not fail, it was never *collected*.
A **deletion mutation partially disarming its own measurement**. Rule 47 says the rename
is the weaker mutation and the one that lies; the deletion has its own opposite way of
lying, and the 6-vs-5 gap between them is not relative strength. Already caught, by the
one row written not to derive its expectation from the code under test
(`test_J7_the_MEASURED_name_is_refused_by_LITERAL…`). Now README rule **50b**: reconcile
`failed + passed` against `collected`, every time.

## 7. My instrument failed, and the failure is the series' shape again

The round-25 battery was thrown away and re-run. I started it, then edited
`factory/README.md` and `factory/tests/test_containment_wall.py` **in the tree it was
measuring**. The harness's precondition ("was the tree clean when I started?") passed and
was true; the question it needed to ask was "was the tree **stable** while I measured?"
The postcondition caught it — as a restore failure, three mutations late, by side effect.

Third instance in the instrument, after rule 48 (summary line, not per-row) and rule 44
(an assert that never ran). Harness now digests every file the suite can read immediately
before and after pytest and refuses to publish a figure if it moved; it also prints
`[failed+passed=N]` so rule 50b's reconciliation is on the receipt rather than done by
hand. Standing rule added: **while a battery runs, `factory/` is read-only to me.**

## 8. Not mine, unchanged

- **The three-clause stopping rule** and the mechanical/agentic lane split — Matt's.
  Clause 1's counter: this round found **one** fail-open (JR-23), so it stays at 0.
  That is now five consecutive rounds of exactly one, which is the § 8 observation
  hardening rather than resolving.
- **The threat-model boundary** — gandalf's and Matt's, still the agentic lane's
  critical path.
- **JR-7's INFO rider** — deferred, gated on the agentic lane opening.

## 9. Receipt

Mutation ledger for this round is at `2026-08-10-factory-spine-gate2-fixes.md` §§ 27.9
and 27.11. Fifteen rows: R24-A…D (the call-site audit), R25-A…G (first battery), and
R25-H…K (a second battery, run because one of the first seven missed its target).

All fifteen KILLED except R24-A, whose survival was the finding. Counts are net of
`test_C2` per the § 23.5 convention; raw pytest lines are in the tables so your
independent run can close against them without re-deriving.

**The two figures you will want first:**

- **R25-E — your R24-C, re-run after my fix: raw `11 failed, 611 passed`. Your figure,
  unmoved.** That is rule 50a's whole purpose. What preserved it was guard *order*: the
  new `unreadable_marker` refusal sits AFTER `git_internal`, so a marker-bearing key
  under `.git` still takes the more specific reason and your row still dies for the
  reason you wrote it for. Placed first, all eleven would still have failed and the
  receipt would have looked identical while measuring something else.
- **R25-F missed its target, and I am flagging it rather than letting you find it.** It
  was written for `_classify_module`'s third exit and never reached it — `tuple` is in
  `_CONTAINER_CALLS`, so the sneak classified cleanly and died on JR-20's *unpinned*
  arm, the arm R25-G already tested. The row written for the fix
  (`test_JR24_the_classifier_ADJUDICATES_what_it_cannot_CLASSIFY`) did not fire. `KILLED
  :: 2 failed` is exactly what a good measurement looks like, which is why the receipt
  hid it; what exposed it was two mutations aimed at two mechanisms dying on one row.

R25-H…K are the repair: H and I kill the classifier row through its two *different* arms
(`unadjudicated` and `stale`), which also establishes that the third exit is load-bearing
today rather than a tripwire — `NOT_A_VOCABULARY` has three live entries. J and K close
the denominator row. **K refuted my own prediction in your favour**: I said that row
asserts the exclusion list's shape and not its effect, and it asserts the effect
directly.

New README rule out of it:

> **50c.** A fix that ships with its own row must be killed **by that row**. A kill by
> some other row is not credit — it is a mutation that missed and landed somewhere
> already defended. Name the expected killer before running, and reconcile.

R24-A and R25-F are the same lesson from opposite signs: a SURVIVAL whose obvious reading
("nobody wrote the row") was wrong, and a KILL whose obvious reading ("the row works")
was equally wrong. Both times the receipt's verdict column was right and its attribution
was not.
