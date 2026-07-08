# Floor Termination-Reason Split (death vs timeout) — R3a step 2

**Author:** gamora (simulation seam)
**Date:** 2026-07-08
**Chain:** batch-2 R3a step 2 (the $0 termination-split weighting Lever 1 vs Lever 2)
**Ruling operated under:** §6 fork **A / YES / YES** (Matt 2026-07-08, run-state lines 817-841). Both levers
  authorized regardless of this split's outcome; the split WEIGHTS magnitudes, it does not gate.
**Disciplines:** #11 (empirical inspection — do not infer from proxies), honesty/fail-loud (say
  "not captured" rather than fabricate a split).

---

## TL;DR — FAIL LOUD: the termination reason was NOT PERSISTED for the R2 run

**The instrument EXISTS but was not RECORDING.** The per-fight death-vs-timeout signal is a
first-class engine field (`SpatialFightResult.winner ∈ {"player","monster","timeout"}`), and it maps
exactly to the split the design needs:

- `winner == "monster"` → **death** (player HP→0, mobs still alive) → implicates the engagement model (Lever 2)
- `winner == "timeout"` → **timeout** (clock expired, player alive, mobs alive) → implicates the HP budget (Lever 1)
- `winner == "player"` → clear (not a floor)

**BUT the R2 run (seed 56M, 25,530 fights, 2026-07-08 01:55) persisted ZERO per-fight winner rows.**
I cannot produce the requested death-vs-timeout counts from R2 data because the data does not exist.
This is a missing-instrument finding — itself a legitimate result. **The correct next $0 step is a
telemetry-recording flip, not more analysis of what's on disk.**

I do NOT fabricate a split from HP/time proxies. One proxy signal is reported below, explicitly labeled
as a proxy, not as the split.

---

## What I checked (Discipline #11 — verified against source + data, not assumed)

### 1. The aggregate results JSON collapses the winner axis
`simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json` (898 KB, mtime Jul 8 01:55) IS the
fresh R2 run (metadata: `total_fights_run: 25530`, `wall_clock_seconds: 1507.6`, `node: endgame`,
`star_lord_integration_mode: stub_write`). Its `encounter_results` (1197 rows) carry only aggregated
axes — `tier_1_outcome`, `tier_1_kpm`, `tier_2_kpm`, **`tier_2_survival_rate`** — and NO
`termination_reason` / `winner` field. `tier_2_survival_rate` is a batch RATE (fraction of tier-2 fights
survived), which cannot be decomposed into monster-death vs clock-timeout after the fact.

R2 floor surface from this JSON (survival_rate == 0.0), for reference:
- **open_arena: 252 / 252 records floored** (survival 0.0 uniformly).
- **magic_pack: 180 / 189 records floored** (9 at survival 1.0).

(These exceed the v3 log's 212 / 111 counts cited in the design-finding note — the R2 endgame surface is
MORE saturated, consistent with gandalf §1's dial-drift arithmetic.)

### 2. The per-fight field exists in the schema and the engine distinguishes the two reasons
`simulation/spatial_gauntlet/spatial_telemetry.py:233` — `SpatialFightResult.winner: str  # "player" |
"monster" | "timeout"` (validated at :386-389). The fight loop actively separates the two: e.g.
`arena.py:923-928` records a prior diagnosis "caster mini_boss = 100% timeouts, 0% death." So the
mechanism to split is native; it is a recording gap, not a modeling gap.

### 3. The R2 run used the Null stub writer — winner was discarded
Metadata `star_lord_integration_mode: stub_write`. `NullSpatialTelemetryWriter.write_fight_result`
(spatial_telemetry.py:461-469) validates the winner then emits it **only at `log.debug`**. The R2 driver
ran at INFO, so even the debug line is absent: `grep -c "winner="` and `grep -c "R2 spatial telemetry"`
on `/tmp/leg3_r2_run2.log` (35 MB) both return **0**. The winner value was computed per fight and thrown away.

### 4. No DB rows for the R2 run anywhere
`spatial_fight_results` (with the `winner` column) exists in three DBs. Only
`src/reincarnated/telemetry/telemetry.db` has rows (7841), but they are STALE VS2a data:
- `MAX(created_at) = 2026-05-20` (49 days old); no rows `>= 2026-07-01`.
- Class IDs are `class_0001…` (heuristic cohort); `COUNT(class_id LIKE '%endgame%') = 0`.
- `COUNT(seed BETWEEN 56000000 AND 57000000) = 0` — none of our seed.

That stale corpus's own winner split (monster 160 / player 3130 / timeout 4551) is from a DIFFERENT
regime (pre-endgame-profile, pre-F1/F2 re-population) and is NOT usable as the before-side. Reporting it
as our split would be a fabrication.

---

## The one proxy signal (LABELED PROXY — not the split, not load-bearing)

In the R2 JSON, of the 252 open_arena floors, **30 have `tier_2_kpm > 0`** (player killed some mobs
before the encounter ended) and 222 have `tier_2_kpm == 0`. In magic_pack, **all 180 floors have
`tier_2_kpm == 0`**. This is a *kills-happened-or-not* proxy, aggregated over the tier-2 batch, NOT a
per-fight winner. It is directionally suggestive (magic_pack floors are near-total no-kill → more
alpha-strike/death-flavored; open_arena has a thin sliver of partial-clears) but it CANNOT distinguish a
0-KPM timeout (survived, killed nothing, clock ran out) from a 0-KPM death (died before killing anything).
KPM==0 is exactly the ambiguous case. **I do not weight the levers from this. Do not treat it as the split.**

---

## Lever implication (unchanged from the design read; not newly evidenced here)

Because the split is not measured, the empirical weighting gandalf §5.2 wanted is not available. The
levers remain authorized on the A/YES/YES ruling regardless (they do not gate on this). The prior
mechanism read stands on its own footing: gandalf §1's "magic_pack floors at the LOWEST HP budget"
argument already establishes HP is not the discriminant → engagement geometry (Lever 2) is the primary
suspect in magic_pack; open_arena is the total-aggro leash finding (Lever 2 again, gandalf §3 Lever 2).
**But this note does not add empirical death/timeout weight to either — it reports that the weight is
un-measured.**

---

## Recommended next $0 step (the telemetry add this finding surfaces)

A near-zero-cost recording flip makes the split available on the R3a step-4 re-run (which is already a
$0 gauntlet re-run — so no extra run cost):

1. **Inject a winner-tallying writer** (or extend the aggregation) so the per-fight `winner` is retained
   per (class, scenario) as `{player, monster, timeout}` counts, surfaced into the results JSON
   (a small aggregate: three ints per encounter row). This is the minimum; it needs NO new fight-loop
   code — `winner` is already computed and passed to `write_fight_result`.
2. **Cross-seam note:** adding a persisted winner-count column to the results-JSON schema (or writing the
   existing `spatial_fight_results` rows to the live DB for this run) touches the star-lord telemetry
   export boundary → **a MIGRATION + star-lord hand-off is required** if it lands as a schema field. If it
   lands purely as an in-JSON aggregate on the gamora side of the results file (no DB write, no export
   column), it is within-seam. I will make that determination when step 3/4 executes and math-note it then.
   **This note itself moves no constant, adds no field, and requires no MIGRATION.**
3. Then the step-4 re-run yields the death-vs-timeout split natively as the before/after diff — the exact
   number this task wanted, but sourced from a run that was actually recording.

---

## Scope discipline

- Moves NO constant. Executes NO lever (that is R3a step 3 — math-note-first + Gate-2 each).
- Touches no content/kit (rider 4).
- Fails loud on the missing instrument rather than inferring a split from proxies.
- No MIGRATION for THIS note (no boundary field moves in a measurement-only task).
