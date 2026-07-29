# Finding — 2026-07-29 — WR2-ENCGEO Cell A (aim-line supplementary emission)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2)
**Severity:** **CLEAR-with-notes** (1 WARN, 8 INFO; **zero BLOCK**)
**Target:** engine `607743a..9bfbdda` — `c8ef0ba` + `6b13b25` + `9bfbdda` (pushed, `origin/main` == `9bfbdda`)
**Developer:** gamora
**Run:** WR2-ENCGEO-2026-07-29, Cell A. Conductor: gandalf. Charter §1 mechanism A, §4 per-landing law.
**Principles applied:** #2 (smoke-gate), #3 (cross-seam impact / MIGRATION), #4 (decisions-log as truth), #5 (severity), #6 (cross-seam round-trip)
**Disciplines cited:** #2, #10, #11, #12, #62
**ADRs:** ADR-002 (tiered approval), ADR-004 (cross-seam handoff)

**Cell B is released to fire.**

---

## What I found

Cell A is a caller-side threading landing that does what it claims. All four scope obligations hold
under independent verification, and the two headline claims (R-WR2-2 non-perturbation, S-5 shape)
reproduce from the artifacts using a comparator I wrote from the charter predicate rather than
gamora's driver. The full engine regression name-set is **identical to the WR1 BATTERY-3 baseline in
both directions**. The single WARN is a forward hazard for Cell C, not a defect in what landed.

---

## 1. Full regression, name-diff law (Obligation 1) — **PASS, empty diff both directions**

Ran to completion in the foreground, not "adjacent suites" (WR1 §8.19 lesson):

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
60 failed, 6042 passed, 3 warnings, 21 errors in 1462.06s (0:24:22)   EXIT=1
```

| | baseline (WR1 BATTERY-3, gamora) | my run at `9bfbdda` |
|---|---|---|
| failed | 60 | **60** |
| passed | 6042 | **6042** |
| errors | 21 | **21** |
| distinct failure names | 81 | **81** |

**Name-set diff vs `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`:
`removed=0  added=0`.** T8 absent from both, as the baseline records. All 81 names sit in
`test_cycle12_layer4_convergence` (33) / `test_cycle13_wave5_season_generation` (21) /
`test_cycle12_layer6_t4_wireup` (12) / `test_kit_space_*` (5) / `test_foundation` (4) / 6 singletons —
**zero in the simulation seam, zero touching the G-5 harness.** The acceptance criterion is met on its
strict form (empty diff), so no delta needed judging.

## 2. Zero-kernel-change (Obligation 2) — **CONFIRMED**

Whole-range diff excluding `output/`:

```
src/reincarnated/simulation/AGENT_STATE.md                     |  99 +-
src/reincarnated/simulation/MIGRATION.md                       |  70 +
src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py |  43 +
src/reincarnated/simulation/wr2_cell_a_aim_2026_07_29.py       | 538 +
```

`git diff --name-only 607743a..9bfbdda -- src/reincarnated/simulation/spatial_gauntlet/` returns
**`kitcal_g5_harness.py` and nothing else** — the entire kernel package is untouched, not merely
`spatial_engine.py`. Last commit to touch `spatial_engine.py` is `3183efb`, and
`git merge-base --is-ancestor 3183efb 607743a` returns true, so it predates the landing range. The
`_trace_decisions` instrument and the `run_spatial_fight(trace_decisions=...)` parameter both
pre-exist at `spatial_gauntlet/spatial_engine.py:2854 / :6943 / :7169`. gamora's claim that the
capability existed since BW-1 and was merely unthreaded is **correct**. Charter §1's scope law holds.

## 3. Default-OFF (Obligation 3) — **CONFIRMED, and proven at the artifact level, not just the signature**

All four threading points declare `trace_decisions: bool = False` (`run_one_fight` :763, `drive`
:1611, `_drive_armed` :1703, CLI `store_true`). Signature-level proof is necessary but not
sufficient, so I fired my own paired battery **at HEAD** — same argv, one with `--trace-decisions`,
one without, 15 traces each:

- **Flag-OFF traces contain ZERO `decision` records.**
- With `decision` records dropped from the ON side: **zero differing fields across every record of
  every pair — not even `engine_git_hash`** (both runs on one tree). This is a *stronger* result than
  R-WR2-2 itself, because no exclusion was needed at all.
- Report: the only `wave_regime` delta is `trace_decisions_wr2_a: false → true`. In the `fights`
  block the **only** field that moves is `trace_path` (different `--out-dir`, by construction) —
  **zero fight metrics move**.
- `trace_summary` moves exactly as MIGRATION §3 warns and nowhere else: `record_counts["event"]`
  32→91 and `event_counts` gains `decision: 59`, while `damage: 18 / death: 8 / telegraph: 6` are
  byte-identical. The documented consumer hazard is accurate and complete.

## 4. SS-1 (Obligation 4) — **CONFIRMED**

`git diff --name-only 607743a..9bfbdda -- .../output/kitcal_g5/wr1_battery_2/` = **0 paths**, and 0
per-commit for each of `c8ef0ba`/`6b13b25`/`9bfbdda`, while the same query for `wr1_battery_2_aim/`
returns 454. `git status --porcelain` on the banked root is clean. The frozen BEFORE-evidence was not
written. Determinism scratch roots are neither tracked nor left on disk, as declared.

## 5. Independent falsification (Obligation 5) — **four claims falsified independently; all held**

I did not read gamora's driver before writing my comparator (Discipline #11).

**(a) R-WR2-2 digest — reproduced with NO a-priori exclusions.** Rather than a pass/fail digest, my
comparator does a recursive structural diff and *reports which JSON paths differ*, so an exclusion
list cannot hide a perturbation. 72 stratified pairs (3 legs × 4 tiers, seeded sample), `decision`
records dropped from both sides:

```
PAIRS COMPARED: 72   record-count mismatches after dropping decisions: 0
DIFFERING JSON PATHS (no exclusions applied):
   'engine_git_hash'   occurrences=72   e.g. boss__B__seed74000823.jsonl#0
```

72 occurrences over 72 traces = **exactly one per trace, on the header record only**. The sole
differing field is `header.engine_git_hash` and nothing else — gamora's declared exclusion set is
exactly right, and the `raw` 0/450 row is explained (the hash differs on every pair, so the
un-excluded digest could only ever say "different"). **R-WR2-2 PASS confirmed.**

**(b) S-5 with an independent denominator.** gamora's "decision count == tick count" is mildly
self-referential if the tick set is read from the aim trace (decision records carry `tick`). I
re-derived the denominator from the **banked** trace, which contains no `decision` records at all:
across 36 traces (3 legs × 4 tiers × 3 seeds), the **decision tick-set equals the banked tick-set in
36/36** — no gaps, no extras, exactly one decision per tick, every decision carrying a non-empty
`target_id`. Observed intents: `{advance, hold}` only, consistent with `evade` being unreachable
without `piloted_competence`. **S-5 shape confirmed on a denominator that cannot be self-fulfilling.**

**(c) Full-population census — reproduced to the digit.** Independent grep count over all 450 aim
traces: pre 40,046 / post 45,362 / pre_endpoint 32,499 (total **117,907**); `advance` **1,680 in every
leg**; `hold` 38,366 / 43,682 / 30,819 (total 112,867); **zero traces with zero decision events** in
any leg. Every number in gamora's §4 table matches.

**(d) The Cell-C datum is TRUE and STRONGER than reported.** Per-tier `advance` counts are not merely
regime-invariant — they are **seed- and arm-invariant**: the distinct per-fight `advance` count is a
single value in every tier, in every fight (trash 6, mixed_pack 7, champion 11, boss 16; 30/30/30/60
fights; 180+210+330+960 = 1,680 exactly). The approach phase is a **deterministic function of spawn
geometry alone**, with zero variance across 450 fights. This corroborates Cell-SPEC §0.2 harder than
the cell note claims and is materially useful to Cell C.

## 6. Process disciplines

- **Principle 2 / Discipline #2 — smoke-gate: SATISFIED.** `--smoke` armed-vs-unarmed pair at seed
  74000700 is present in the cell note, and the full regression is now on record for the landing.
- **Principle 3 / ADR-004 — cross-seam: SATISFIED, and well above the bar.** MIGRATION.md was filed
  *before* the run, names both consumers (star-lord for the report key, drax for the trace),
  distinguishes schema-unchanged from population-changed, states the absent-key read for old reports,
  and names the exact consumer anti-pattern (`record_counts["event"]`, file size) that my §3 check
  independently confirmed is the only thing that moves.
- **Discipline #62 — commit hygiene: CLEAN.** Three pathspec-precise commits (code → repair →
  artifacts), no `git add -A` residue; the substantial pre-existing untracked tree noise was not
  swept into any of them.
- **Principle 4 — decisions-log: NO CONFLICT.** Nothing in this landing contradicts a locked entry;
  the 2026-07-22 BW-1 semantic-shift entries are consistent with it.
- **Discipline #10 / #12 — the two self-caught instrument bugs are handled correctly.** Re-firing the
  cell from a clean tree rather than explaining away a `-dirty` straddle is the right call: a
  determinism check spanning a tree change measures the tree, not the RNG.

---

## Rationale

Verdict is **CLEAR-with-notes** rather than CLEAR because of WARN-1, and rather than BLOCK because no
review principle is violated and nothing that landed is wrong. Per Principle 5, severity is
proportionate: WARN-1 is a *forward* hazard whose remedy belongs to Cell C's MIGRATION, not a defect
in `607743a..9bfbdda`. Under ADR-002 this landing sits in jack-ryan tier — it is caller-side
threading behind a default-off flag plus artifacts, with no cross-seam *schema* change (the record
shape is unchanged since REPLICA-1 G2; only its population moved) and no architectural commitment. No
escalation to Matt is required by this finding.

---

## WARN

**WARN-1 — `trace_decisions_wr2_a: false` is not a trace-content guarantee: there is a SECOND,
UNGATED decision-emission site.** At `spatial_gauntlet/spatial_engine.py:4258` the frame sink's
`decision(...)` is called on the **evade branch under `if self._frame_sink is not None:` alone** — it
is *not* behind `if self._trace_decisions:`. The site gamora's note cites (`:5068`) is correctly
gated; this one is not. It is unreachable on this run's path (`piloted_competence` is not passed) and
I verified it empirically: **zero `decision` records in all 450 banked flag-OFF traces and zero in my
own flag-OFF run.** So nothing that landed is affected.

The forward problem is the declaration's scope. MIGRATION §1 and the report key are written as
though "armed" and "trace carries decisions" are the same proposition. On a piloted-competence path
they are not: a trace could carry `decision` records with `intent: "evade"` while its report says
`trace_decisions_wr2_a: false` — reintroducing exactly the measured-zero / unmeasured-zero confusion
(P-2) the key exists to prevent, in the opposite direction. **Cell C is the next thing to touch this
code** (R-WR2-9 explicitly retains EVADE as the uptime-costing motion), so the hazard becomes live
one cell from now.

*Action:* gamora, at Cell C — either gate `:4258` on `_trace_decisions` for symmetry with `:5068`, or
state in MIGRATION that the key declares the **battery arm** and not a trace-content invariant, and
name `:4258` as the exception. Either resolves it; the choice is gamora's (within-seam, ADR-002).
Not blocking for Cell B.

---

## INFO

- **INFO-1 — Cell B's byte-identity baseline must be taken at `9bfbdda`, not at the WR1 banked
  report.** `"trace_decisions_wr2_a": bool(trace_decisions)` is written into `wave_regime`
  *unconditionally*, so a **flag-OFF report is no longer byte-identical to a pre-landing report** — it
  gains one additive key valued `false` (I confirmed: banked reports lack the key entirely; my
  flag-OFF run at HEAD emits `false`). MIGRATION §1 documents the key, but the forward consequence is
  stated nowhere: **R-WR2-11 requires Cell B's Gate-2 to grade "flag-OFF byte-identical full
  regression"**, and that comparison will show a spurious one-key delta if its BEFORE snapshot is
  taken from `wr1_battery_2`. Behavior and trace content are unaffected; only the report artifact.
  *Action:* conductor — pin Cell B's byte-identity BEFORE-snapshot at `9bfbdda`+.

- **INFO-2 — S-4 is not closed by this cell, and §8.2 should not be read as closing it.** Charter §3
  S-4 is a *battery* predicate ("battery byte-reproducible at fixed seed, twice"); Cell A's evidence
  is **one leg, 150 traces, twice** (`determinism.leg: "pre"` in the statistics artifact). Charter §4
  item 5 assigns S-1..S-4 to Cell BAT, so Cell A **over-delivered** relative to its obligation — but
  the remaining 300 traces × 2 are still owed at Cell BAT. Charter §8.2's "determinism 150/150 twice"
  is accurate; it is not S-4 GREEN.

- **INFO-3 — the driver's own refusal guard has a disjunct that admits an inert exclusion.**
  `wr2_cell_a_aim_2026_07_29.py:258`: `"exclusion_gap_is_exactly_the_declared_set": gap_fields ==
  expected_gap or not gap_fields`. The `or not gap_fields` clause means an **empty** gap also passes,
  i.e. the guard cannot distinguish "the exclusion is exactly right" from "the exclusion did
  nothing". Benign in this run — the `raw` 0/450 row independently proves the exclusion live, and the
  cell note argues from that row — but the guard is weaker than its docstring claims. Worth tightening
  if the falsifier is reused in Cell BAT.

- **INFO-4 — path-precision in citations.** The cell note, MIGRATION §4 and AGENT_STATE all cite
  `spatial_engine.py:2854 / :5068 / :6943 / :7169` without the `spatial_gauntlet/` path segment; the
  file is at `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py`. All line numbers are
  correct. Same class as the line-drift note carried in the Wave-D Gate-2 finding; cosmetic, but a
  future reader grepping the stated path finds nothing.

- **INFO-5 — Principle 6 round-trip: substance present, declared form absent.** The report gained a
  key star-lord exports and the trace gained a record class drax consumes. No round-trip smoke was run
  at drax's loader boundary — legitimately, because that loader does not exist yet (charter §4 runs it
  in parallel). MIGRATION carries the substance of a (ii) justification (additive, default-false,
  absent-key semantics stated, consumer anti-pattern named). The literal
  `Round-trip: not applicable because <reason>` line is not present. INFO rather than WARN because the
  substance is unusually complete. *Owed at the drax handoff / AFTER baton.*

- **INFO-6 — 145 MB committed; repo trace artifacts now ~274 MB.** gamora flagged this explicitly to
  the conductor and matched the `wr1_battery_2` precedent (129 MB, tracked). Regenerable in ~9.7 s of
  battery wall time from the committed driver. This is a conductor/Matt-tier call, not
  jack-ryan-tier — ledgered here, not adjudicated.

- **INFO-7 — cell note and AGENT_STATE are stale relative to the final landing.** Both head with
  "Commits (engine, **NOT PUSHED**): `c8ef0ba`, `6b13b25`" — the landing is three commits and *is*
  pushed (`origin/main == 9bfbdda`). Charter §8.2 is correct. Documentation currency only; both were
  written before the banking commit.

- **INFO-8 — positive, and a Cell-C input.** See §5(d): the `advance` census is seed- and
  arm-invariant, not merely regime-invariant — zero variance across all 450 fights. Recommend the
  conductor carry the *invariance*, not just the totals, into the Cell C spec: it means the approach
  phase is fully determined by spawn geometry, so any post-C `advance` variance is attributable to C
  alone (Discipline #10, change one thing / measure one thing).

---

## Action

- [x] jack-ryan: full regression run to completion, name-diff vs baseline — **empty both directions**
- [x] jack-ryan: kernel-untouched, default-OFF, SS-1 verified independently
- [x] jack-ryan: R-WR2-2 and S-5 independently falsified from artifacts with own comparator — both hold
- [ ] gamora (at Cell C, non-blocking): resolve **WARN-1** — gate `spatial_engine.py:4258` or scope the
      MIGRATION claim to "battery arm, not trace-content invariant"
- [ ] gandalf (conductor): pin Cell B's flag-OFF byte-identity BEFORE-snapshot at `9bfbdda`+ (**INFO-1**)
- [ ] gandalf (conductor): record that S-4 remains open at Cell BAT (**INFO-2**); carry the
      `advance`-invariance into the Cell C spec (**INFO-8**)
- [ ] Matt: **no decision required by this finding.** INFO-6 (repo size) is the only item that could
      escalate, and gamora has already routed it to the conductor.

**Cell B is CLEARED to fire** per charter §4 per-landing law.

---

## References

- Charter: `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` (§1, §2 R-WR2-2, §3 S-4/S-5, §4, §6 SS-1, §7 R-WR2-11, §8.2)
- Cell note: `agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-a-aim-emission.md`
- Regression baseline: `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py` (:763, :827, :1611, :1703, :1747, :1808, :1991, :2043, :2120)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (:2854, **:4258 ungated — WARN-1**, :5068 gated, :6943, :7169) — **unmodified by this landing**
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wr2_cell_a_aim_2026_07_29.py` (:75, :208, :258)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — entry `[2026-07-29] WR2-ENCGEO Cell A`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — SESSION 91
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2_aim/wr2_cell_a_aim_statistics.json`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/` — FROZEN, verified untouched

*jack-ryan, 2026-07-29. Gate 2, DEV-MODE. Nothing rubber-stamped: every load-bearing number in this finding was recomputed from the artifacts or from runs I fired myself.*
