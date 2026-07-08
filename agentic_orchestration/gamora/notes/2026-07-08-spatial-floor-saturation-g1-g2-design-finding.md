# Spatial-Gauntlet Floor-Saturation — G1 Disposition + G2 Bimodality Design-Finding

**Author:** gamora (simulation seam — PRIMARY on the co-diagnosis)
**Date:** 2026-07-08
**Dispatch:** `agentic_orchestration/dispatches/2026-07-08-gamora-starlord-spatial-floor-diagnosis.md`
**Routing:** Matt / gandalf (G1 is a design finding, not a unilateral gamora calibration change)
**Disciplines:** #11 (empirical inspection — the log's remedy note is NOT trusted as truth), #12
  (semantic-shift honesty), #23 (framing-audit), Goodhart-guard (rider 5).

---

## TL;DR

- **G1 (the load-bearing fork):** `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` is a **KNOWN-PARKED-UNCALIBRATED
  state relative to the endgame-BC regime** — AND its re-calibration is an **explicitly
  Matt-scheduling-pending workstream** (decisions-log, twice). It is NOT ruled-final endgame
  difficulty; it was ruled for a *different* regime (2019-HP swarm, 51-class heuristic cohort,
  2026-05-19) and **never re-ruled** against the endgame regime that landed 9 days later.
  **BUT** the log's `1.5→1.25` remedy is WRONG and I do NOT apply it. The floor is not an HP-wall
  the multiplier can fix. **No constant moves. This is the design finding.**
- **G2 (bimodality):** of the 12 endgame-BC classes that reach the gauntlet surface, **10 are
  bimodal-by-design (positional identity), 2 are ceiling-only (clear everything), ZERO are
  uniformly-floored.** Every one of the 12 walls `chokepoint_corridor` at WR=1.000. The floor is
  **scenario-specific (open_arena + magic_pack), not class-specific.** The instrument's difficulty
  state is the suspect — exactly the Leg-B caster-vindication shape. 11 classes are NOT broken.

---

## G1 — Difficulty-state disposition (cited, verified against source)

### The question
Is `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` a KNOWN-UNCALIBRATED state the leg-3 pilot inherited, or the
RULED endgame difficulty?

### The three source citations (Discipline #11 — verified, not assumed)

**Source 1 — arena.py:49 provenance + git-blame.** The constant `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5`
was authored 2026-05-19 (commit `24cdc7e`, "VS2a R2 recalibration impl — HYBRID Option C"). Its
docstring (arena.py:30-48) cites: disposition `r2-h1-recalibration-disposition-2026-05-19.md §2.1`,
math note `R2-recalibration-math-2026-05-19.md §4`, "L1 gamora authority." `git log -L 49,49` shows
**exactly ONE commit in the line's entire history** — it was never touched again.

**Source 2 — the math note's calibration regime (`R2-recalibration-math-2026-05-19.md §2.2`).** The
1.5× was derived against **~2019 HP per swarm mob** ("2019 × 1.5 = 3028.5 HP per swarm mob"). That is
the OLD generic mob-stat regime. It was calibrated to de-saturate the **51-class heuristic cohort**
for the **H1-variance / convergence instrument** — NOT the endgame-BC corpus.

**Source 3 — the endgame regime explicitly declares itself DISTINCT (endgame_mob_stat_profile.py:8-16).**
The endgame mob profile (W-α7+ Phase 3c, 2026-05-28 — **9 days AFTER** the 1.5× was ruled) states
verbatim: *"OPTION C (new per-tier stat profile structure; **distinct from MOB_HP_DIFFICULTY_MULTIPLIER
= 1.5 at arena.py:49, which is preserved for the existing convergence path recalibration**). This
profile bakes L45-50+ durability into the monster stat specification rather than applying a runtime
multiplier."* and *"Cross-seam note: **DOES NOT modify arena.py**."* The endgame swarm-tier HP is now
**26,500 mid** (`ENDGAME_TIER_HP_FACTOR_RANGE["swarm"] = (1.05, 1.60)` × 20,000; confirmed live by
`arena.py:_compute_swarm_tier_hp_ref() → 26,500`). That is a **~13× increase** over the 2019 HP the
1.5× was tuned against.

**Source 4 — the decisions-log names it a SEPARATE, MATT-SCHEDULING-PENDING workstream (decisive).**
Two entries in `design/decisions/decisions-log.md`:
- Line 4240 (2026-06-16 KPM-band recalibration CLOSE): *"bands are re-fit candidates IF
  `MOB_HP_DIFFICULTY_MULTIPLIER` changes … that multiplier workstream is **separate,
  Matt-scheduling-pending**."*
- Line 5223: *"the separate `MOB_HP_DIFFICULTY_MULTIPLIER` workstream **(Matt-scheduling-pending)** …
  the bimodal-shell p25-lo cut is anchored to it."*

### Disposition (the fork resolved)

`1.5` is **NOT the ruled endgame difficulty.** It is a constant *properly ruled for its original
context* (2019-HP regime, convergence instrument) that is now **stacking, un-re-calibrated, on top of
a ~13×-heavier endgame mob regime it was never evaluated against.** In the fork's terms it is the
"inherited-uncalibrated" branch — but with a critical qualifier the dispatch's binary did not
anticipate: **its re-calibration is an explicitly Matt-scheduling-pending workstream** (Source 4).
gamora does NOT have standing to unilaterally move a Matt-scheduling-pending constant.

### Why the log's `1.5→1.25` remedy is WRONG (Discipline #11 — do not trust the log)

The floor-saturation warning (spatial_engine.py:3432) prints *"reduce MOB_HP 1.5→1.25 per L1
authority."* **I verified this remedy against source and it is structurally incapable of fixing the
observed floor:**

1. **The 1.5× multiplier does NOT apply to `magic_pack` at all.** `MOB_HP_DIFFICULTY_SCENARIOS =
   {open_arena, chokepoint_corridor}` (arena.py:55). Verified live:
   `'magic_pack' in MOB_HP_DIFFICULTY_SCENARIOS → False`. Yet **magic_pack accounts for 111 of the
   323 floor events (34%)** and floors WR=0.000 for 7 of the 12 classes. `1.5→1.25` **cannot touch a
   single magic_pack floor** — they are outside its scope entirely.
2. **The floor is bimodal against a hard ceiling, not a uniform HP-wall.** Every class that floors in
   open_arena/magic_pack **ceilings at WR=1.000 in chokepoint_corridor** (see G2). A 17% HP reduction
   shifts both modes slightly; it does not collapse a 0.000/1.000 positional split. The mechanism is
   positional/leash + magic_pack-scope, not mob durability.
3. **Applying `1.5→1.25` to make the pilot pass would be textbook Goodhart drift (rider 5)** — softening
   a mis-scoped instrument to green a gate, on a constant Matt has parked for scheduled re-calibration.

### G1 verdict

**NO CONSTANT MOVES.** The correct disposition is: surface to Matt/gandalf that (a) the endgame-BC
spatial difficulty state is uncalibrated-for-endgame (1.5× stacking un-re-ruled on the 26,500-HP
regime), (b) the parked `MOB_HP_DIFFICULTY_MULTIPLIER` re-calibration workstream is now on Leg-C's
critical path and needs Matt scheduling, and (c) the `1.5→1.25` note in the code is mis-scoped and
should NOT be the fix — the real levers are leash/positional geometry (open_arena) and the
magic_pack HP-multiplier SCOPE question (magic_pack is currently outside the multiplier). This is a
DESIGN FINDING routed up, not a gamora calibration edit. Per ADR-004/Gate-2: since no boundary field
moves on the gamora half, **no MIGRATION is required for G1.**

---

## G2 — Bimodality characterization (12 endgame-BC classes)

### Method (Discipline #11)
Extracted per-class-per-scenario extreme WRs from `/tmp/leg3_n1_v3.log` (the completed run). The log
emits floor (WR≤0.05) and ceiling (WR≥0.95) warnings naming class+scenario; mid-band WRs are not
logged, but floor+ceiling extremes are exactly what characterizes bimodality (mass at 0.0 vs mass at
1.0). 18 candidates were generated; **6 dropped at character-generation** (`Phase 3 FAIL: 0 in-band
T4s`) and never reached the gauntlet; **12 reach the surface** — these are the analysis population.

### The per-class matrix (extreme WR by scenario)

| Class (endgame_bc_*) | chokepoint | open_arena | magic_pack | shape |
|---|---|---|---|---|
| melee_high_flat_dex | 1.000 | 1.000 | — | ceiling-only |
| ranged_high_flat_dex | 1.000 | 1.000 | — | ceiling-only |
| melee_high_flat_str | 1.000 | **0.000** | — | **BIMODAL** |
| melee_medium_variable_str | 1.000 | **0.000** | — | **BIMODAL** (dispatch exemplar) |
| mid_high_flat_dex | 1.000 | **0.000** | — | **BIMODAL** |
| melee_high_variable_wis | 1.000 | **0.000** | **0.000** | **BIMODAL** |
| melee_medium_variable_wis | 1.000 | **0.000** | **0.000** | **BIMODAL** |
| mid_medium_variable_wis | 1.000 | **0.000** | **0.000** | **BIMODAL** |
| ranged_low_spiky_int | 1.000 | **0.000** | **0.000** | **BIMODAL** |
| ranged_low_spiky_wis | 1.000 | **0.000** | **0.000** | **BIMODAL** |
| ranged_medium_variable_int_light | 1.000 | **0.000** | **0.000** | **BIMODAL** |
| ranged_medium_variable_wis | 1.000 | **0.000** | **0.000** | **BIMODAL** |

### Count

- **Bimodal-by-design (positional identity — BOTH a WR=1.000 ceiling AND a WR=0.000 floor): 10 of 12.**
- **Ceiling-only (clear everything, no floor): 2 of 12** (`melee_high_flat_dex`, `ranged_high_flat_dex`
  — the strongest kits; no design concern).
- **Uniformly-floored (floors with NO ceiling anywhere): 0 of 12.**

### Interpretation (rider 4 — bimodality is a LIVE HYPOTHESIS, confirmed)

The dispatch's exemplar `melee_medium_variable_str` (open_arena 0.000 / chokepoint 1.000) is **not an
outlier — it is the population pattern.** ALL 12 classes wall chokepoint_corridor at WR=1.000. The
scenario-level floor breakdown is decisive:
- **open_arena: 212 floor events** (kited-to-death across open ground — the melee/short-range identity
  cost; leash-geometry sensitive).
- **magic_pack: 111 floor events** (ranged-caster-pack full-clear pressure — and, per G1, entirely
  OUTSIDE the HP-multiplier scope).
- **chokepoint_corridor: 242 ceiling events** (the corridor funnels mobs into the kit's engagement
  geometry — every kit walls it).

This is **positional identity, the design signal the engine exists to emit** — a melee kit kited to
death in the open that walls a corridor is a working class, not a broken one. **A calibrator that
demanded unimodal per-class convergence would be fighting the kit diversity, exactly rider 4's
warning.** The instrument's difficulty state (open_arena leash/positioning + magic_pack scope) is the
suspect, not 10-11 broken classes. **Do NOT fix the content to satisfy the instrument (rider 4).**

### Consequence for Leg-C (rider 3)
Because the floor is scenario-structural (open_arena + magic_pack) and population-wide, the full Leg-C
summoner campaign hits the same wall. The G1 Matt-scheduling-pending re-calibration workstream — NOT
a `1.5→1.25` tweak — is on Leg-C's critical path. Leg-C should not re-fire until Matt schedules that
re-calibration (correct levers: open_arena leash/positional geometry + the magic_pack HP-multiplier
scope decision).

---

## What this finding does NOT do (scope discipline)

- Does NOT move `MOB_HP_DIFFICULTY_MULTIPLIER` or any bar/band/chassis/kit constant (all frozen; the
  multiplier is Matt-scheduling-pending).
- Does NOT re-roll or re-tune the 18 candidates (rider 4 — no fixing content to satisfy the instrument).
- Does NOT touch the leg-3 wire, export/, or the driver (star-lord's half).
- The G3 fail-loud convergence guard (separate, unconditional deliverable) ships regardless of this
  finding — see `simulation/math/r2-calibration-fail-loud-convergence-guard-2026-07-08.md`.
