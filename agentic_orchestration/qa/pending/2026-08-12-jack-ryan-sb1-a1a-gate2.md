# Gate-2 — SB-1 Cell A1a — the KC2 baton LOADER LANDING

**Reviewer:** jack-ryan (DEV-MODE, charter § 7)
**Date:** 2026-08-12
**Target:** `reincarnated-godot` `4c6dcc5..28ea1ba` (HEAD `28ea1ba1a2a6035549bd237c9e101a6106abf4fb`), local only
**Developer:** drax (presentation seam)
**Landing report:** `agentic_orchestration/drax/notes/2026-08-12-sb1-a1a-loader-landing.md`
**Predicates gated:** charter §§ 1–2 (G-COV, G-SEM) · run-minted-law GL-6…GL-12, GL-19, FG-13, FL-3, CL-2/CL-3/CL-10 · ledger A-0/A-1, R-A1-LAW, PL-4

## VERDICT: **PASS-WITH-FINDINGS**

**No G-COV clause fails. No G-SEM clause fails.** Every load-bearing number in the landing
report reproduced from my own seat, at HEAD, from the primary sources. **Act 1b (statics +
dress) is UNBLOCKED.** Nine findings, none BLOCKING: six DEBT, three INFO. All are
framing-and-coverage debt, not defects in the loader.

The ladder's closing sentence — *a predicate that answers a slightly different question than
the one asked will always look green from where you stand* — was applied to all four harnesses.
It caught one row (JR-A1a-2) whose green is structurally guaranteed, and it cleared everything
else.

---

## 1 · What I re-ran, and what came back

All four harnesses executed by me at HEAD. Godot `4.6.3.stable.official.7d41c59c4`.
**No harness attempts a viewport read, a frame write, a camera, a light, a mesh or a `.tscn`** —
grepped across all five authored scripts; the only match is a comment saying so. Nothing to abort.

| harness | claimed | **measured by me** |
|---|---|---|
| `kc2_loader_smoke.gd` | 26 checks, 0 FAIL | **26 checks, 0 FAIL, exit 0** |
| `kc2_placement_smoke.gd` | 10 assertions, 0 FAIL | **10 assertions, 0 FAIL, exit 0** |
| `kc2_fg13_falsify.gd` | 3 checks, 0 FAIL, mutants pruned | **3 checks, 0 FAIL, 2 mutants pruned, dir empty** |
| `kc2_loader_diff.py` | 22/22 EXACT-MATCH, 0 DELTA | **22/22 EXACT-MATCH, 0 DELTA, exit 0**; stub's own run 23/23 MUST · 33/33 total GREEN |

**Byte-identity (the determinism claim, verified as an artifact-layer property — not a G-DET claim):**
all six regenerated artifacts came back **byte-identical**, including the 2,698,325-byte gitignored
position sweep. `diff` of the before/after digest lists is empty.

**Containment, measured by me before and after my own runs (not read from the harness's own report):**

| tree | before | after |
|---|---|---|
| engine porcelain | 2,789 lines, sha `66338cf697b5…` | **identical text, full `diff` empty** |
| engine `__pycache__` dirs under `src/` | 18 | **18**; zero `.pyc` newer than session start |
| godot porcelain | 233 lines (= L-0 pin) | **identical text**; HEAD unchanged |

**Primary-source recount (CL-10, my own probe, neither loader in the path).** Baton sha256
recomputed from bytes = `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa`,
matching the § 1 pin. `events.rows[].event_type` recounted directly:

```
channel_release 20 · channel_start 20 · damage_dealt 1132 · death 344
spawn 344 · wave_end 20 · wave_start 20   →  7 types, 1,900 rows
```

Reconciled against `tmp/kc2/kc2_event_census.json`: **vocabulary and every count EXACT**, no type
in the baton absent from the artifact and none in the artifact absent from the baton. Dispositions
resolve **1,556 CONSUMED + 344 BINNED = 1,900**, `uncovered_needs: []`, `closes: true`, and no row
carries a disposition outside {CONSUMED, BINNED}. The artifact's own field
`vocabulary_derived_from` reads *"events.rows[].event_type (the artifact's own column)"* and the
code path confirms it: `_consume_events()` builds `event_vocabulary` by first-seen order from the
column, with `EVENT_REGISTRY` used only as a lookup — a type present with no registry row lands in
`uncovered_needs` and refuses. **The vocabulary is derived, not recited.**

**Also verified from primary sources, independent of the report:** 344/344 spawn rows resolve to
the actor table · `channel_start`/`channel_release` strictly alternate across all 40 rows (so the
loader's single-slot `open_channel` cannot orphan a segment on this baton) · 17 dwell pairs split
12 at ≥44 ticks / 5 at Δtick = 1 / 0 other · drip max +306 ticks · NOTE-7's substrate exactly
(1,132 `damage_dealt`; 332 with `applied == 0.0 ∧ hp_after == 0.0`, **all 332** coinciding with a
`death` row at the same (target, tick); 12 killing blows with `applied > 0`;
`sum(applied) == hp_max` on 344/344, **zero discrepancies**) — R-A1-1 rests on solid ground ·
32,375 = Σ(hi − lo + 1) against Cell 0's 32,031 = Σ(hi − lo), so the sample count and the
lifetime-coverage figure are the same measurement at two inclusivities, not a discrepancy.

## 2 · Differential independence (assignment clause b) — **CLEARS**

The two columns come from genuinely different code paths. Left: `build_scene(payload)` +
`consume(payload)` from `reincarnated-engine/src/reincarnated/export/baton_v1_stub_consumer.py`
(Python, star-lord's seam). Right: `tmp/kc2/kc2_loader_derived.json` +
`kc2_loader_positions.json`, written by `kc2_baton.gd` under Godot (GDScript, drax's seam).
**No shared parsing library exists between them** — only the baton bytes and the law.

The load-bearing row is the position function: `Scene.actor_position()` at
`baton_v1_stub_consumer.py:97–118` versus `Kc2Baton.actor_position()` at `kc2_baton.gd:486–502`.
Two independent transliterations of GL-7's rule, 32,375 samples, **max |Δ| 4.974e-13 m against a
1e-9 m bar**, consistent with the 12-dp string round-trip the report names at § 8(a). That is
verification, not self-agreement.

Both rows the report labels at § 2 are correctly labelled **in the harness output itself**:
- `[stub self-audit] suppressed path[0] tests` → note reads *"BOTH COLUMNS ARE STUB-SIDE. A
  DIFFERENT QUANTITY from the row above…"* ✓
- `a DISC would misplace (counterfactual)` → note reads *"the godot side REPORTS this number and
  draws no circle for scatter anywhere"* ✓

A third non-stub row, `board entry == path[0].run_tick + 1`, is labelled inline (*"the stub has no
such field — this row diffs godot against the WIRE"*) ✓. See JR-A1a-3 for the rows that are not.

## 3 · Falsification genuineness (assignment clause d) — **GENUINE**

Both mutants reach and exercise the refusal path they name, and each asserts the *specific* error
string, so a refusal for the wrong reason reads FAIL:

- **FG-13** — `telegraph_cast` planted; asserts `not ok ∧ load_error contains "UNCOVERED NEEDS"
  ∧ contains "telegraph_cast" ∧ uncovered_needs == ["telegraph_cast"]`. Observed:
  `loaded=false uncovered=["telegraph_cast"]`.
- **GL-12** — `actors[0].path = []` planted; asserts `not ok ∧ load_error begins_with
  "PATHLESS-ACTOR" ∧ contains victim`. Observed: `PATHLESS-ACTOR w151_a000`. PL-4's empty domain
  (0 of 344 pathless — I reproduced this) is correctly *given* a domain rather than declared
  untestable.
- **CONTROL** loads GREEN, so the mutant verdicts mean something.
- Mutants written to the godot repo's own `tmp/kc2/_falsify/`, loaded under their **own recomputed**
  sha256 (so the digest gate passes and the gate under test is the one that fires), and deleted —
  **directory verified empty after my run**. **The pinned baton was never touched: its digest
  recomputes to `d7ecd866ac45…` after all four of my runs.**

The report's mechanism claim at § 5 — *"the mutant's `_integrity` row count is bumped so the census
is the only thing that can fail"* — is **true but not operative**: see JR-A1a-9.

---

## 4 · Findings

### JR-A1a-1 — **DEBT** — the change-set is 12 paths, not the 11 the report and the ledger state

`git diff --name-only 978a423 28ea1ba | wc -l` = **12**. The report § 1 enumerates *"the five
scripts, `.gitignore`, `AGENT_STATE.md`, and four `tmp/kc2/` artifacts"* = 11; there are **five**
`tmp/kc2/` artifacts committed (`kc2_differential.json`, `kc2_event_census.json`,
`kc2_falsification.txt`, `kc2_loader_derived.json`, `kc2_placement_smoke.txt`). Ledger row A1-1
carries the same 11. Every path falls inside a claimed class, so **FG-4 (`diff_matches_claims`)
holds on the subset property** — but the count does not reproduce, which is the exact failure mode
CL-3 exists to catch (*"reproduce the number from the artifact, not from the report"*).
**Everything else in the hygiene claim reproduces:** `project.godot` 0 paths, WR2 stack
(`wr2_playback.gd`, `wr2_actor_rig.gd`, `replica_trace.gd`) 0 paths, 6 commits, commit-per-item.

### JR-A1a-2 — **DEBT** — the GL-7 UNDEFINED row is a tautology on the godot column

`kc2_loader_diff.py:183–195`, row *"UNDEFINED outside the closed span (GL-7)"*. The stub column is
a real test: it asks `scene.actor_position(aid, lo-1)` and `(aid, hi+1)` and requires `None`. The
godot column asks only whether the emitted rows start at `lo` and end at `hi`:

```python
g = positions["positions"][aid]
if g and (g[0][0] != lo or g[-1][0] != hi):
```

Those rows were produced by `kc2_loader_smoke.gd:337` — `for t in range(lo, hi + 1)`. **Measured:
344/344 actors emit exactly `range(lo, hi+1)`, 0 samples outside the span, 0 null entries.** The
condition is therefore a property of the *emitter loop*, not of `actor_position()`, and cannot fail
for any loader using that loop — including one that clamps or fabricates outside the span. The
loader is in fact correct (`kc2_baton.gd:491–492` returns `null` outside the closed span, read
directly), and the endpoint agreement is already covered by the terminal-tick and board-entry rows.
**The behaviour is right; the row does not test it.** This is the ladder's closing sentence in
miniature.
**Fix (A1b or a follow-on):** have the smoke emit two probe samples per actor at `lo-1` and `hi+1`
and assert `actor_position()` returns null there, then diff that against the stub's `None`.

### JR-A1a-3 — **DEBT** — "22 rows, stub → godot" overstates the independent count

Of the 22 rows, **8 are genuinely stub-object vs godot-loader** (actor count, knot count, wave
count, per-actor terminal tick, spawn positions, the position function, GL-7 UNDEFINED, track
sample counts). The rest are not, and only three say so:

- **raw-wire left column, unlabelled** — event row count, `tick_period_s`, event census by type,
  census closure, scatter shape word (the diff script re-parses `scatter_model.split()[1]`, the
  same rule the loader applies, so this row is a same-rule re-implementation, not an oracle);
- **diff-script predicate over stub-parsed data** — inside/outside BOX, disc counterfactual,
  `path[0]`-inside-active-disc, dwell pairs;
- **a hard-coded literal on the left** — `kc2_loader_diff.py:272–273`,
  `row("actors hit-testable at their own path[0] (GL-8)", 0, derived["hit_testable_at_path0"])`.
  The stub column is the integer `0`, not a measurement from either loader. The assertion is
  correct and valuable; the presentation as a stub↔godot match is not;
- **not a loader comparison at all** — `FG-17 engine tree unchanged` is a containment fingerprint
  counted inside the differential's 22.

Nothing here is wrong; the framing invites a reader to count 22 independent confirmations where
the independent count is 8 plus one literal. **Action:** carry a `basis` field per row in
`kc2_differential.json` (`STUB-VS-GODOT` / `WIRE-VS-GODOT` / `STUB-VS-STUB` / `GODOT-ASSERTION` /
`CONTAINMENT`) and report the sub-counts in the headline.

### JR-A1a-4 — **DEBT** — FL-3 coverage: 19 refusal paths in the loader, 4 falsified

`kc2_baton.gd` carries **19** distinct `load_error` refusal paths. Four are proven able to go red
(digest-not-declared, digest-mismatch, PATHLESS-ACTOR, FG-13 uncovered-needs). Five of the
**semantic** refusals — as opposed to I/O plumbing — have no falsification test:

| refusal path | line | law |
|---|---|---|
| `SCATTER-SHAPE-UNDECLARED` | 306 | **GL-9** |
| `placement_extents_m absent` | 309 | GL-9 |
| `TICK-PERIOD-DISAGREEMENT` | 285 | GL-10 |
| `FG-13 census does not close` | 808 | FG-13 |
| `INTEGRITY-MISMATCH` | 259 | **CL-10** |

FL-3 reads *"Every gate ships a falsification test that puts it back to RED."* § 5's header —
*"the gates proven able to go red, not merely green"* — reads as all of them. The GL-9 pair is
the highest-value gap, because **A1b is the BOX-placement cell** and a silently degraded shape
word costs 72 of 344 bodies. **Action:** add three mutants in A1b's cell — shape token replaced
with a non-`{BOX, DISC}` word, `config.kit.tick_period_s` perturbed in the last digit, and an
`_integrity` count bumped without a matching row — each asserting its own error string.
*(FG-13's own census-closure arm and the spawn-roster arm are lower value; note them, do not
gate on them.)*

### JR-A1a-5 — **DEBT** — NOTE-9 softness: four assertions carry a basis the predicate does not test

The cross-leg-speed check is the model to copy — `multi == 283 ∧ vary_2dp == 12 ∧ vary_4dp == 23 ∧
vary_raw == 282`, all three bases asserted, and the report's § 7 self-correction is exactly right.
Four others fall short:

| assertion | predicate | the basis in its name |
|---|---|---|
| `GL-12 absences declared` | `absences.size() >= 6` | **7 exist**; a `>=` bar below the measurement — dropping one absence still passes |
| `GL-7 2-knot straight walks (p05 set) = 61` | `path.size() == 2` | never checks the bodies are the p05 set |
| `NOTE-2 p05 drip … = 61` | `spawn_tick − spawn_event_tick != 0` | never checks the bodies are p05 |
| `GL-11 one global clock, no wave offset` | `tick[0] == 1 ∧ tick[-1] == 3732` | endpoints only; NOTE-4's claim rests on **contiguity + monotonicity**, which is not asserted — a track with a hole in the middle passes |

All four are **true on this baton** — I measured each (p05 set, 2-knot set and drip set are the
identical 61 bodies; `player_path.tick == range(1, 3733)` exactly). The debt is that the assertion
would not catch the day one stops being true. **Action:** assert `absences.size() == 7` with the
ids listed; assert set-identity for the two 61s; assert contiguity for the clock.

### JR-A1a-6 — **DEBT** — the census artifact does not carry the evidence for its own bin

`BIN-ROSTER-CROSSCHECK` is justified in report § 3 by *"roster identity is cross-checked against
the actor table (344/344 resolve)"*. The loader computes it —
`event_census["spawn"]["crosschecked_against_actor_table"] = spawn_rows_crosschecked`
(`kc2_baton.gd:811`) — but `census_report()` (`:815–837`) builds `by_type` from five named keys
only, so the number **never reaches `kc2_event_census.json`**. Measured keys on the committed
spawn row: `count, disposition, event_type, note, sink`. The claim is true (I verified 344/344
resolve from the baton), but the committed artifact carries an assertion whose evidence is only
implicit in the fact that the load did not refuse. **FG-16** gates the presence of a citation.
**Action:** add the crosscheck count to the emitted row.

### JR-A1a-7 — **INFO** — the largest check-count claim is the one without a committed receipt

Placement (10) and falsification (3) ship committed transcripts. The loader smoke — the **26**-check
headline, and the only harness asserting GL-10, GL-11, NOTE-1, NOTE-2 and the three-basis cross-leg
check — ships none. § 5 discloses this honestly (*"committed transcript for the placement run"*),
and I regenerated the 26 checks myself, so nothing is unverified. Recorded because A1b builds on
those 26 and a future reader will look for the receipt.

### JR-A1a-8 — **INFO** — the three 61s are one population, and that is worth saying

The landing prints three different 61s (61 two-knot straight walks · 61 drip bodies · 61 stub-side
suppressed `path[0]` tests) and correctly insists the last is a different quantity from the 6-body
would-be-hit class. **Measured: all three sets are the identical 61 bodies — and they are exactly
the p05 spawn-point population.** The 6 would-be-hits are a strict subset. So the coincidence is
structural, not accidental, and the NOTE-9 hazard the report guards against does not exist here.
Recorded as a positive: the deeper application of NOTE-9 came out clean.

### JR-A1a-9 — **INFO** — the FG-13 mutant's stated mechanism is not the operative one

Report § 5: *"The mutant's `_integrity` row count is bumped so the census is the only thing that
can fail."* The bump does make `_integrity` self-consistent, but it is **not** what isolates the
census: `load_file()` runs **GATE 5 (`_consume_events`, FG-13) before GATE 7 (`_verify_integrity`,
CL-10)** — `kc2_baton.gd:247–260`. Without the bump the census would still be the first and only
refusal. The conclusion is right and the mutant is honest; the rationale attributes the isolation
to the wrong mechanism, and a future reader porting the pattern to a loader with the opposite gate
order would carry the wrong lesson.

*Cleared while I was there:* the loader's `_integrity` check skips `path_knots` with
`declared: null`. This is **not** a dropped check — I confirmed the wire's `_integrity` block
carries `actor_count`, `event_row_count`, `events_columns_len`, `track_sample_counts`, `wave_count`
and **no knot count at all**. Declaring the absence rather than defaulting to a comparison against
nothing is GL-12 applied to the loader's own self-audit. Correct as written.

---

## 5 · Action

- [ ] **drax** — JR-A1a-1: correct the path count to 12 in `AGENT_STATE.md`; JR-A1a-2 and JR-A1a-5
      fold into A1b's harness pass; JR-A1a-4 add the three named mutants in A1b; JR-A1a-3 and
      JR-A1a-6 are one-line emitter changes, take them whenever convenient.
- [ ] **gandalf (`RUN-CONDUCTOR`)** — correct ledger row A1-1's "11 paths" to 12; bank JR-A1a-2 and
      JR-A1a-4 as the two A1b riders. **A1b is unblocked by this verdict — do not hold it for the
      debt items.**
- [ ] **Matt** — nothing. No BLOCK, no escalation, no locked-decision conflict. Per **ADR-002**
      this is within-seam work in drax's lane with no cross-seam schema change, so the verdict is
      mine to issue directly.

## 6 · References

Reviewed / executed / measured:
- `/Users/admin/Games/reincarnated-godot/scripts/kc2_baton.gd` (1,011 lines, read in full)
- `/Users/admin/Games/reincarnated-godot/scripts/kc2_loader_smoke.gd`
- `/Users/admin/Games/reincarnated-godot/scripts/kc2_placement_smoke.gd`
- `/Users/admin/Games/reincarnated-godot/scripts/kc2_fg13_falsify.gd`
- `/Users/admin/Games/reincarnated-godot/scripts/kc2_loader_diff.py`
- `/Users/admin/Games/reincarnated-godot/tmp/kc2/` (all five committed artifacts + the gitignored sweep)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/baton_v1_stub_consumer.py` (read-only)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` (read-only, digest re-verified)
- `agentic_orchestration/drax/notes/2026-08-12-sb1-a1a-loader-landing.md`
- `agentic_orchestration/drax/notes/2026-08-12-sb1-cell0-countersign.md`
- `agentic_orchestration/gandalf/notes/2026-08-10-sb1-kc2-scene-run-charter.md`
- `agentic_orchestration/gandalf/notes/2026-08-10-sb1-scene-run-ledger.md`
- `agentic_orchestration/operating-procedures/run-minted-law.md`

**Laws applied:** GL-6, GL-7, GL-8, GL-9, GL-10, GL-11, GL-12 · FG-4, FG-7, FG-13, FG-16, FG-17 ·
FL-1, FL-3, FL-8 · CL-2, CL-3, CL-4, CL-10, CL-12 · charter § 2 G-COV / G-SEM · ledger PL-4,
A0-2, R-A1-LAW · ADR-002.

— jack-ryan, 2026-08-12. *Every number in the landing report reproduced. The four findings that
matter are about what the harnesses claim to prove, not about what the loader does.*
