# KC2-SIM Phase C — G-B1 fix report

**Author:** gamora (simulation seam)
**Date:** 2026-08-08
**Commission:** conductor (gandalf, RUN-CONDUCTOR), Phase C fix cycle — **G-B1 ONLY**
**Verdict fixed:** `jack-ryan/notes/2026-08-08-kc2-gate2-phase-c.md` § 2, G-B1 (BLOCK)
**Repo / branch:** `~/Games/reincarnated-engine`, `main`
**Base:** `874302d5` → **commit `bae60ce6`** (not pushed)

---

## 1 — Reproduction at HEAD, before any edit

Verified first, per commission step (1). `PYTHONPATH=src python3 -m pytest`.

```
tests/test_wr3_kite_commit_stage2b.py::test_rect_is_a_valid_shape_and_the_enum_grew_deliberately
  @ 874302d5 → FAILED
  AssertionError: assert frozenset({'c...'rect',...}) == frozenset({'c...'star',...})
    Extra items in the left set:
    'disc'
  tests/test_wr3_kite_commit_stage2b.py:357
```

Reproduces exactly as the verdict describes.

I also re-derived the census independently rather than taking the verdict's list, using the
grep the verdict says was owed — `grep -rn "VALID_SHAPES\|VALID_FAMILIES" tests/`. It returns
**5 files**, confirming jack-ryan's count. His § 2 table names four; the fifth is my own
`tests/test_kc2_channel_disc.py`, which uses membership (`<=`, `in`), not equality, and was
already green.

Source of truth, `src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py`:

```
:451  VALID_FAMILIES = frozenset({"nova", "blizzard", "wave", "melee", "eor_spin"})
:512  VALID_SHAPES   = frozenset({"circle","cone","line","point","rect","trapezoid","star","disc"})
```

---

## 2 — Diff summary

Two files. Nothing else in the repo touched.

| File | Change |
|---|---|
| `tests/test_wr3_kite_commit_stage2b.py` | **M** — +12 / −2. The one assertion at `:357`, on the prescribed pattern. |
| `tests/test_telegraph_value_set_census.py` | **A** — new, 88 lines. The mechanical census. |

### 2.1 The `:357` amendment

Exactly jack-ryan's prescribed pattern: the exact-equality limb becomes a retention limb plus a
named-additions limb, carrying the same in-diff reason comment the other four amendments carry
(INVERT-DON'T-DELETE attribution, the ruling that admitted the value, the math-note pointer).
The pre-existing BR-2 comment block above it was left intact — the new comment stacks below it,
so the cell now reads as two successive recorded crossings rather than one rewritten claim.

```python
assert frozenset(
    {"circle", "cone", "line", "point", "rect", "trapezoid", "star"}) <= TelegraphSpec.VALID_SHAPES
assert TelegraphSpec.VALID_SHAPES - frozenset(
    {"circle", "cone", "line", "point", "rect", "trapezoid", "star"}) == frozenset({"disc"})
```

### 2.2 Root cause, stated as a method defect

The growth was ratified and correct; what failed was the **derivation of the blast radius**. Lap 1
chose its radius as a *file list* (7 files) where the question was "who fences this value-set" — a
question only a grep on the value-set **name** answers. The grep returns 5 files / 15 assertions;
the file list returned 4 of them. Discipline #2 names the blast radius but does not say how to
derive it. On a value-set, the derivation is the grep. That is the transferable lesson and it is
written into the new file's docstring as step 2 of the protocol, stated as authoritative over any
remembered file list.

---

## 3 — The census test (jack-ryan's recommended addition, adopted)

**Placement:** a **new dedicated file**, `tests/test_telegraph_value_set_census.py`, rather than
appending to an existing wave-scoped file. Reasoning: the whole failure mode is that the census
lived scattered across wave files, each of which is discoverable only if you already know it
exists. A census that lives inside `test_kc2_channel_disc.py` would be invisible to the next
grower, who will not be doing KC2. A file named for the job is greppable, wave-neutral, and
outlives any one wave's test file.

**Contents — three cells:**

1. `test_the_shape_value_set_has_EXACTLY_this_membership` — exact equality against
   `EXPECTED_SHAPES` (8 values).
2. `test_the_family_value_set_has_EXACTLY_this_membership` — exact equality against
   `EXPECTED_FAMILIES` (5 values).
3. `test_a_value_is_never_REMOVED_from_either_set` — superset check against every value **ever**
   admitted. Removal is the one direction that is not mere bookkeeping: `validate()` consults
   these sets, so deleting a value makes the engine reject its own historical records on replay.
   This cell is permanent and must never be relaxed, only extended.

Both equality cells carry a failure message naming `added=` / `removed=` explicitly, so a future
red states the delta rather than making the reader diff two frozenset reprs.

**Provenance on the values, not just in the log.** Each value carries an inline block naming the
ruling that admitted it — the original five (WR3), `trapezoid`/`star` (BR-2 / RESOLVE-TRUTH-1,
math note `br2-resolve-truth-1-2026-08-01.md` §3), `disc` (D-6 / L-16, spec §2.3, math note
`kc2-mechanism-stack-2026-08-08.md` §C), `eor_spin` (L-16, one new mechanism = one new family).

**The three-step protocol** is in the module docstring: (1) update the expected membership and
say which ruling admitted the value; (2) run the grep — that grep, not a remembered file list, is
the blast radius; (3) amend every hit on INVERT-DON'T-DELETE. The current 5-file census is listed
with line numbers, explicitly flagged as courtesy — line numbers drift, the grep does not.

**Non-vacuity verified.** A tripwire nobody has seen fire is a tripwire nobody knows is armed. I
injected a synthetic growth (`hexring` into `VALID_SHAPES`) and a synthetic removal (`melee` from
`VALID_FAMILIES`), in memory only, no file edited:

```
growth caught:  VALID_SHAPES moved. added=['hexring'] removed=[] — see this module's docstring §PROTOCOL
removal caught: a family was REMOVED: ['melee'] — replay of historical records will now fail validate()
```

Both fired, and both named the offending value.

---

## 4 — `:351` disposition — INSPECTED, NOT AMENDED

```python
:351    assert "rect" in TelegraphSpec.VALID_SHAPES
```

**Shape:** a single-value **membership** assertion, not an equality-pin. It is monotone under
growth — adding `disc` cannot make it red. It can only fail on a **removal** of `rect`, which is
precisely the behaviour worth keeping (the docstring above it says so: `rect` is retained on
purpose because removing a value would make `validate()` reject historical records on replay).

**Disposition:** left as-is, per the commission's stated condition — amend only if it equality-pins
a grown frozenset. It does not. Amending it would have added diff noise to a cell that is already
correct, and its removal-guard intent is now additionally backstopped by census cell 3.

---

## 5 — Test counts, before and after

Blast radius = all 5 census files, plus the new census file, plus the full
`test_wr3_kite_commit_stage2b.py` standalone.

| Scope | Before (`874302d5`) | After (`bae60ce6`) |
|---|---|---|
| 5 census files | **1 failed / 138 passed** | — |
| 5 census files + new census file | — | **0 failed / 142 passed** |
| `test_wr3_kite_commit_stage2b.py` alone | **1 failed / 37 passed** | **0 failed / 38 passed** |
| Tree-wide collection | — | **10,268 tests collected, 0 collection errors** |

The arithmetic closes: 139 tests across the 5 files before, plus 3 new census cells = 142 after,
all green. The single before-failure was G-B1 and nothing else; no other red existed in the
radius.

Files in the radius: `test_br2_resolve_truth_1.py`, `test_br2_trace_stage_1.py`,
`test_wr3_stage2c.py`, `test_wr3_kite_commit_stage2b.py`, `test_kc2_channel_disc.py`,
`test_telegraph_value_set_census.py`.

---

## 6 — Anomalous: the verdict's own baseline count for this file

Reported, not silently corrected — it is the verdict's evidence line, so the conductor should
decide what to do with it.

§ 2 records:

```
@ ebf13240 (PYTHONPATH-isolated):  1 failed*, 37 passed  → this test PASSES
* the one failure at ebf13240 in that file is a different test; this assertion was green.
```

I re-ran the file at `ebf13240` in a detached worktree (`git worktree add ... --detach`, removed
afterwards). Result:

```
tests/test_wr3_kite_commit_stage2b.py @ ebf13240 → 38 passed, 0 failed
```

**Zero failures in that file at the baseline**, not one. The 2 known pre-existing failures live in
a *different file*, `tests/test_wr2_d_nova_telegraph.py`
(`::test_the_minted_telegraph_carries_the_DERIVED_duration_under_the_arm` and
`::test_the_minted_telegraph_carries_the_MEASURED_0_750_off_the_arm_H_M2_f`) — the same two my
lap-1 commit message declared as pre-existing. I confirmed they are still failing at HEAD,
test-ID for test-ID, identical at both ends and untouched by this fix.

**The finding is unaffected and correct.** I verified the load-bearing half directly: `:357` was
**green at `ebf13240`** and **red at `874302d5`**, which is the entire basis of G-B1. Only the
parenthetical baseline count mis-attributed another file's failures into this file's tally. It
changes nothing about the BLOCK.

Two live reds remain in the wider KC2 blast radius (`test_wr2_d_nova_telegraph.py`, both
pre-existing at `ebf13240`, declared in the lap-1 and lap-4 commit messages). They are **not**
G-B1 and are **not** touched here.

---

## 7 — Discipline notes

- **Discipline #1 (math-before-code): not triggered.** This amends test guardrails to *record* an
  already-ratified growth. No balance constant, modifier formula, threshold, convergence criterion
  or gate rule moves. No new math note; the governing note is the existing
  `simulation/math/kc2-mechanism-stack-2026-08-08.md` §C.
- **Discipline #2 (smoke / blast radius): the finding, and the fix, both live here.** Radius
  re-derived by grep on the value-set name, not by file list. Counts in § 5.
- **Discipline #12 (semantic-shifting): not triggered.** No behaviour's interpretation changes.
  `VALID_SHAPES` already contained `disc` at HEAD; this only makes the guardrails say so.
- **Schema / MIGRATION:** unchanged. The value-set growth and its D-F4 consumer obligation were
  already carried in the lap-4 `MIGRATION.md`; this touches tests only, so nothing new is owed to
  star-lord.
- **Push posture:** COMMIT-NEVER-PUSH honoured. Not pushed. Re-verdict is the conductor's to
  commission; not self-cleared.

---

## 8 — Scope statement

**G-B1 only.** Two files, both tests. The G-D wiring re-lap (kubacabra re-scope, AC-6.x tests,
Cited-graded exemption entries, array-lookup-law flip) is pre-registered separately and did **not**
fire in this commission. The four gamora WARNs (G-W1..G-W4) are untouched — the verdict states they
do not gate G-C on jack-ryan's authority.

This meta-repo note is deliberately **not committed**; it rides the conductor's gate-close unit.
