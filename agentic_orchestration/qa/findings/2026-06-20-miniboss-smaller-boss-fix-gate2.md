# Finding — 2026-06-20 — mini_boss "smaller boss" fix (re-banks HELD production-gate column)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (re-cleared 2026-06-20 — BLOCK resolved; 3 prior non-gating INFO items carried forward)
**Target (re-cleared):** `gamora/v-miniboss-smaller-boss-fix-2` — engine commit `fb3e702` (test-only correction) atop the originally-reviewed `gamora/v-miniboss-smaller-boss-fix-1` (`c2a8392` fix+math-note, `82ae9b9` driver; collab `da40542` data)
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** #1 (math-before-code), #2 (smoke-test / suite-green at tag), #3 (seed hygiene), #12 (semantic-shift declaration)
**ADRs:** ADR-002 (in-seam test correction — direct-approve authority), ADR-004 (MIGRATION: none required), ADR-006 (read-only verify; did NOT push)

## Verdict

**PASS-WITH-INFO** (re-cleared) — the single narrow BLOCK defect is resolved. Carries the 3 prior non-gating INFO items (INFO-1/2/3 below) for the record; none gate.

### Re-clear (2026-06-20) — BLOCK → PASS, verified first-hand

The original BLOCK was a single in-seam defect: the fix flipped `SCENARIO_MINI_BOSS.soft_timeout_s 150.0 → None` but left the pinning test asserting the pre-fix value
(`test_soft_timeout_is_150s`, :171-173 → `assert None == 150.0`, red suite). gamora corrected it in `gamora/v-miniboss-smaller-boss-fix-2` (`fb3e702`). I verified all three
re-clear conditions FIRST-HAND (did not take the claim):

1. **Assertion is a clean re-point, not invented logic / not gate-masking.** `tests/test_spatial_gauntlet_scenarios.py:184` now reads `assert SCENARIO_MINI_BOSS.soft_timeout_s
   is None`; test renamed `test_soft_timeout_is_150s → test_soft_timeout_is_none_smaller_boss` with a docstring documenting the boss/240s alignment + the Discipline #12 semantic
   shift. `git show fb3e702` confirms it is a single assertion flip + rename + docstring — no try/except, no `pytest.skip`, no broadened/loosened assertion. It pins the NEW
   truth, mirroring the boss-gate stale-floor correction pattern.
2. **Suite re-run GREEN first-hand:** `pytest tests/test_spatial_gauntlet_scenarios.py` → **27 passed in 0.30s** (was 1 failed, 26 passed). Discipline #2 "suite green at tag"
   now satisfied.
3. **Fix mechanism unchanged.** `git show --stat fb3e702` shows the correction touches ONLY `tests/test_spatial_gauntlet_scenarios.py` (1 file, +14/-3). `arena.py`
   (soft_timeout→None) and `t4_sim_cycling.py` (`_boss_midpoint_hp` + `_floor_miniboss_hp` HP floor) are NOT in the commit — the production mechanism I PASSed on all 8 focus
   items below is byte-for-byte intact. The correction was test-only.

Re-clear is mine under ADR-002 (within-seam test correction reflecting an already-Matt-ratified semantic shift) — no Matt escalation. The 8 original focus-item PASSes stand
unchanged (mechanism untouched).

### Original verdict (2026-06-20, pre-correction) — BLOCK

**BLOCK** — on a single, narrow, in-seam defect: the fix flipped `SCENARIO_MINI_BOSS.soft_timeout_s 150.0 → None`, but the test that pins that exact value
(`tests/test_spatial_gauntlet_scenarios.py::TestMiniBossScenario::test_soft_timeout_is_150s`, :171-173) was NOT updated and now FAILS against post-fix HEAD
(`assert None == 150.0`). A production-gate-affecting tag (same gate-rigor tier as the boss-gate build) must not ship with a red suite (Discipline #2). This is a
stale-assertion-not-tracking-the-deliberate-change condition, NOT a masking condition — the fix is correct; the test asserts the OLD intended value. Resolution is a
one-assertion edit in gamora's own seam (no architectural decision), so this BLOCK clears the moment the test is re-pointed and the suite is re-run green. **→ RESOLVED in
`gamora/v-miniboss-smaller-boss-fix-2` (`fb3e702`); see Re-clear above.**

**Everything else PASSES first-hand.** The mechanism is sound on all 8 focus items, the banked boss_with_adds column is mechanically and empirically unmoved, clear shells
are byte-identical, seed hygiene is clean, recompose-first held, the semantic shift is declared and coherent, the seam call is correct, and the dex sub-finding is
correctly attributed to pre-existing geometry + the known V5 metric artifact (not created by this fix).

## What I found

**FOCUS 1 — Mechanism correctness (soft_timeout=None routes through existing guard; HP clamp DOWN-only off live profile) — CONFIRMED.**
- soft_timeout: `_mini_boss_soft_timeout` is sourced at `spatial_engine.py:1648-1652` directly from `self.scenario.soft_timeout_s` (now None). The guillotine at
  `:1685-1696` is gated `if _mini_boss_soft_timeout is not None and ...` — with None it is inert. NO new branch, NO logic deleted (recompose-first); the guard already
  existed and was designed for exactly this. Verified by reading both sites first-hand.
- HP clamp: `_floor_miniboss_hp` (`t4_sim_cycling.py:1056-1077`) clamps ONLY `if threat_tier == "mini-boss"` AND ONLY `if mob_hp > ceiling` (downward-only). Ceiling is read
  live via `_boss_midpoint_hp()` importing `ENDGAME_MOB_PROFILES["boss"]` — no hard-coded 231k; it tracks any future boss re-base. Armor re-derived off the clamped HP using
  the unchanged `armor_frac` (no new armor model). Applied at both consumption sites (`:1240` t1, `:1315` t2). Smoke-tested directly:
  `_boss_midpoint_hp()=231000.0`; `_floor_miniboss_hp('mini-boss',240000,0.115) -> (231000.0, 26565.0)` (clamps + re-derives); `('mini-boss',200000,...)` -> no-op.

**FOCUS 2 — No regression on the banked boss_with_adds column — CONFIRMED (mechanical AND empirical).**
- Mechanical: boss_with_adds `win_condition="boss_killed"` (`arena.py:523`), so it never enters the `if win_condition == "mini_boss_killed"` block where the soft-timeout
  guillotine lives — the soft-timeout change cannot reach it. Its boss spawn `threat_tier="boss"` (`:493`), so the HP clamp (`== "mini-boss"`) is a no-op; smoke-confirmed:
  `_floor_miniboss_hp('boss',240000,0.165) -> (240000.0, 39600.0)` byte-identical. boss_with_adds already ran `soft_timeout_s=None` (default, `:243`) — unchanged.
- Empirical: re-measure table (seed 711000) shows boss_with_adds UNMOVED — int 1.000, wis 0.956, str 1.000, dex 1.000, ALL with timeout=0.000. The "banked column stays
  put" HARD criterion holds.

**FOCUS 3 — No clear-shell regression — CONFIRMED.** The HP clamp is guarded on `threat_tier == "mini-boss"`. Smoke-confirmed no-op for swarm/magic/elite even above the
ceiling: `_floor_miniboss_hp('swarm'|'magic'|'elite', 240000, 0.165) -> (240000.0, 39600.0)`. The soft-timeout change is scoped inside the mini_boss_killed win-condition
block. Clear shells are byte-identical.

**FOCUS 4 — Seed hygiene (Discipline #3) — CONFIRMED.** Base `711000` appears ONLY in this fix's own driver + math-note (`grep -rln 711000` across engine src + collab
artifacts). Disjoint from all declared used bases (820000, 619000, 14001, and the diagnosis's 8.5M/16M/24M/32M/40M namespaces). 700k namespace is clean.

**FOCUS 5 — Recompose-first held — CONFIRMED.** Two constant re-scales, zero new mechanics: (a) one field value `150.0 → None`; (b) a downward clamp of an EXISTING computed
HP value to an EXISTING boss-profile-derived ceiling, with armor re-derived off the EXISTING armor_frac. No new HP model, no armor model change, no hand-tuning to a target
(the clamp is to the boss midpoint, a principled config-derived value, not a number chosen to make a cell pass). The generation range is read, not edited.

**FOCUS 6 — Semantic-shift declaration (Discipline #12) — CONFIRMED + coherent.** Declared in math-note §4, in the commit message, AND inline in `arena.py:768-779`. The
shift is real: mini_boss survive-and-kill moves from "burst within 150s vs HP ≥ boss" to "kill within the 240s boss window vs HP ≤ boss"; historical mini_boss numbers are
declared not comparable. Coherent with the "smaller boss" ratification.

**FOCUS 7 — Seam boundary (consumption-site clamp, generation range untouched) — CONFIRMED correct.** The kill-target HP is computed deterministically in gamora's seam at
the t1/t2 consumption sites (`20_000 × midpoint(hp_factor_range)`); the clamp is applied there, on gamora's own value. rocket's `generation/endgame_mob_stat_profile.py:101`
range `(9.50, 14.50)` is NOT edited and is correctly flagged for rocket's post-workstream absolute-magnitude-constant sweep. This is the right seam call: no field crosses
the gamora→star-lord boundary newly; `termination_reason` values are unchanged (only `timeout` frequency shifts — a data shift, not schema). **MIGRATION: NONE required —
correctly declared.** (ADR-004.)

**FOCUS 8 — dex sub-finding (`endgame_bc_melee_high_flat_dex_none` clears boss_with_adds, times out 100% on mini_boss) — CONFIRMED gamora's read.** The re-measure
corroborates the mechanism: dex|mini_boss bossHP%_p90 = **13.80** (>>1.0) — the V5 attribution-accumulation metric artifact (dex sinks damage into adds; boss_HP_removed
accumulates past the kill target). dex|boss_with_adds is 1.000 / bossHP%_p90 1.0; dex|mini_boss drops to 0.667 / timeout 0.333. The fix only RELAXED time (150s→240s) and HP
(240k→231k) — both strictly easier — so it is mechanically incapable of CREATING a dex timeout. The residual is a pre-existing melee-dex × mini_boss geometry shortfall
(closer-flanking elite adds + larger mini-boss body) surfaced, not introduced. I challenge nothing here; it is correctly routed as a pre-existing item, not a flag against
this fix.

## The defect (BLOCK basis)

`tests/test_spatial_gauntlet_scenarios.py:171-173`:
```python
def test_soft_timeout_is_150s(self):
    """Soft timeout at 150s (A8 spec § 5.3)."""
    assert SCENARIO_MINI_BOSS.soft_timeout_s == pytest.approx(150.0)
```
Re-run first-hand: `1 failed, 26 passed` — `assert None == 150.0 ± 1.5e-04`. The fix deliberately set `soft_timeout_s=None`; this assertion pins the pre-fix value and was not
updated in commit `c2a8392` (which touched only arena.py, t4_sim_cycling.py, and the math-note). A production-gate-affecting tag at boss-gate rigor must present a green
suite (Discipline #2). This is distinct from the boss-gate build, where the 7 test edits were INCLUDED in the gate commit and verified green (49/49) at Gate-2; here the
parallel edit is MISSING.

This is a stale-floor-style correction (the same benign category as the boss-gate build's `2 of 4 → 9 of 18` fixes), NOT gate-masking — the test asserts the OLD intended
value. It is in-seam (gamora owns `tests/test_spatial_gauntlet_scenarios.py` for simulation scenarios) and architecturally trivial.

## Rationale

REVIEW_PROCESS #2 / Discipline #2: a tagged state that changes a production-gate-affecting constant must carry its test suite green; a constant pinned by a test was changed
without re-pointing the test, leaving the suite red. Severity is BLOCK because (a) this is a production-gate-affecting change at boss-gate rigor tier, where "suite green at
tag" is non-negotiable, and (b) a red suite at a tag is the precise condition Discipline #2 exists to catch. It is NOT escalated to Matt: the resolution is a single
in-seam assertion edit reflecting an already-Matt-ratified semantic shift (mini_boss = "a smaller boss"), so it is gamora's to fix directly and mine to re-clear under
ADR-002 (test-addition / within-seam correction is my direct-approve authority once green).

## Action

- [x] Developer (gamora): re-point the assertion to `is None`, retitle `test_soft_timeout_is_none_smaller_boss`, docstring the semantic shift, re-run green, re-tag.
  **DONE** — `gamora/v-miniboss-smaller-boss-fix-2` (`fb3e702`); suite 27 passed.
- [x] jack-ryan: re-clear to PASS on confirmation the suite is green (in-seam test correction; ADR-002 direct-approve — no Matt escalation). **DONE** — verified first-hand
  (assertion re-point, 27 passed green re-run, mechanism byte-for-byte unchanged); verdict BLOCK → PASS-WITH-INFO.

## INFO (non-blocking; do not gate)

- **INFO-1 (stale harness banner string):** the re-measure table header (`miniboss-smaller-boss-remeasure-2026-06-20.txt:9`) still text-labels "mini-boss 150s soft" in
  the termination-vocabulary legend, while the live config dump on line 11 correctly shows `mini_boss ... soft_timeout_s: null, max_duration_s: 240.0`. The MEASUREMENT used
  None (the config was live-read); only the legend prose is stale. Cosmetic; fix opportunistically. Cite: Discipline #12 (keep declared semantics consistent in artifacts).
- **INFO-2 (caster mini_boss lands GRADED, not full clear):** int 0.681 / wis 0.563 with residual timeouts 31.9% / 43.7% and a_dead=0 — these are honest 240s-window
  near-kill shortfalls, not guillotine artifacts (math-note §3 pre-registered graded-OR-full as both criterion-passing). This is the now-correct disposition input, NOT a
  defect. Whether casters SHOULD clear mini_boss more fully than ~0.6 is a design-fit question for gandalf/Matt, not a Gate-2 item. Routing as design input, mirroring the
  boss-gate finding's halt pattern.
- **INFO-3 (generation-range inversion still live upstream):** the root config inversion (mini-boss hp_factor midpoint 240k > boss 231k) remains in rocket's
  `generation/endgame_mob_stat_profile.py:101`; the consumption-side clamp masks it for the simulation gate but the generation range still rolls mini-boss HP above boss for
  any other consumer. Correctly flagged by gamora for rocket's absolute-magnitude-constant sweep. Noting so a future reader does not assume the generation inversion is
  resolved. Cite: REVIEW_PROCESS #3 (cross-seam impact).

## References

- Math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/miniboss-smaller-boss-fix-2026-06-20.md`
- Code (re-traced first-hand): `spatial_gauntlet/arena.py:768-780` (soft_timeout→None), `:472-523` (boss_with_adds: boss_killed / threat_tier=boss / soft_timeout=None),
  `:713-767` (mini_boss: 240s hard cap, threat_tier=mini-boss); `spatial_engine.py:1648-1652` (soft_timeout sourcing) + `:1685-1696` (guillotine guard, inert when None);
  `t4_sim_cycling.py:1056-1077` (_boss_midpoint_hp + _floor_miniboss_hp) + `:1240` (t1 apply) + `:1315` (t2 apply); `generation/endgame_mob_stat_profile.py:101,103` (ranges,
  read not edited)
- Re-measure: `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/miniboss-smaller-boss-remeasure-2026-06-20.{json,txt}` (960 cells, seed
  711000; inversion gone, boss_with_adds unmoved)
- DEFECT (RESOLVED): `~/Games/reincarnated-engine/tests/test_spatial_gauntlet_scenarios.py:171-184` — assertion re-pointed to `is None`, test renamed
  `test_soft_timeout_is_none_smaller_boss`; suite re-run **27 passed in 0.30s** (was 1 failed, 26 passed). Correction commit `fb3e702` (test-only, +14/-3).
- Prior gate-rigor reference: `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-06-20-boss-gate-gate2.md`
- Commits: engine `c2a8392` (fix+note), `82ae9b9` (driver), `fb3e702` (test correction); collab `da40542` (data)
- Re-cleared tag: `gamora/v-miniboss-smaller-boss-fix-2` → `fb3e702`
