# R3a step-4 gauntlet — coherence forensics (2 anomalies) — $0 read-only

**Author:** gamora (simulation seam)
**Date:** 2026-07-08
**Mode:** $0 read-only forensic diagnosis. NO gauntlet re-run, NO code change. Existing artifacts only.
**Artifacts read:** `cycle-13-gauntlet-sim-results-20260708_065352.json` (1197 encounter_results),
`leg3_pilot_section8a1_band_measurement.json`, `/tmp/leg3_r3a_step4_run.log` (87229 lines),
`t4_sim_cycling.py`, `gauntlet_sim.py`, `math/r3a-d3-winner-tally-recording-flip-2026-07-08.md`.

---

## Anomaly 1 — winner-tally ⟂ survival_rate — SEMANTIC DISTINCTION (not a D3 defect), but with a confound worth naming

**Root cause / code citation.** Within a single tier-2 batch, `survival_rate` and `winner_tally.player`
are BOTH pure functions of `fr.winner == "player"` and cannot disagree:
- `survival_rate = wins/n_fights`, `wins = Σ f.player_won` (`t4_sim_cycling.py:255-262`)
- `player_won = (fr.winner == "player")` (`t4_sim_cycling.py:1245`)
- `winner_tally["player"] = Σ (f.termination_reason == "b_dead")` (`t4_sim_cycling.py:304`)
- `termination_reason = _term_for[fr.winner]`, `_term_for = {"player":"b_dead", ...}` (`t4_sim_cycling.py:1241,1269`)

Empirically confirmed: over ALL 603 records that carry a tally, `abs(survival_rate − tally.player/n) < 1e-6`,
**0 mismatches**. The D3 flip is correct; the monster-win case IS incrementable (it's `a_dead`); nothing is
tallied on the wrong population. The apparent contradiction is a **pure aggregation artifact**:

The `magic_pack` aggregate (player=720/1.00, monster=0, timeout=0) is computed over ONLY the 36 magic_pack
records that ran tier-2 — and all 36 are ceiling (survival ≥ .95). The 153 floored magic_pack cells carry
`tier_2_winner_tally = None` and never enter the aggregate. So "floored surface + 100% player-wins" is two
DISJOINT cell sets being read as one. monster=0 in every scenario is likewise real-but-benign: the recorded
population is the ceiling cells, which by definition contain no deaths.

**Why the None cells exist (the confound).** `tier_2_winner_tally` defaults to `None` (`gauntlet_sim.py:616`),
assigned ONLY when tier-2 runs (`:1304`). `tier_2_survival_rate` is a dataclass field **defaulting to 0.0**
(`:609`), also assigned only when tier-2 runs (`:1301`). When a CLEAR shell REJECTs at tier-1, the loop
`continue`s (`gauntlet_sim.py:1278-1288`) — tier-2 never runs, so `survival_rate` keeps its **0.0 default
(reads as FLOOR) while the tally stays None**. Cross-tab of the 1197 cells: 603 measured (tally present),
**594 unrun** (tally None) — and every one of the 594 unrun cells reads survival 0.0/floor. This is a
default-value-vs-sentinel mismatch: the same "not-run" state renders as a genuine-looking FLOOR in one field
and as None in the other. **Not a D3 defect** (D3 only touched the tally, and touched it correctly) — it is a
pre-existing serialization semantic on `tier_2_survival_rate` that D3 makes newly visible.

## Anomaly 2 — calibration-warning ⟂ final-cell surface — DIFFERENT NAMESPACES; final `encounter_results` is contaminated

**Root cause / code citation.** The `[R2 calibration]` WARNINGs are emitted by
`reincarnated.simulation.spatial_gauntlet.spatial_engine` — the RAW spatial engine's own R2 calibration probe,
a separate loop from the tier-1/tier-2 gauntlet **gate**. Its scenario name and the gate's
`scenario_shell_id` are the same tokens but different measurement surfaces. Calibration WR (541 warns) by
scenario: CEILING — open_arena 225, chokepoint_corridor 189; FLOOR — magic_pack 116, open_arena 11. That
matches Matt's read: open_arena mostly ceiling, magic_pack floor, in the calibration namespace.

The final `encounter_results` surface for the SAME scenarios: open_arena 252/252 FLOOR,
chokepoint_corridor 189/189 FLOOR — because **open_arena and chokepoint_corridor NEVER run tier-2 in the
gate** (100% tally-None; all cells are the 0.0-default artifact from Anomaly 1). So the open_arena
"ceiling→floor inversion" is not a real flip in the fight math; the final field is simply the unrun 0.0
default for every open_arena/chokepoint cell.

**Which surface is authoritative for §4?** Neither the raw calibration warns nor the full 1197-cell field.
The calibration probe is an instrument-health signal, not the gate WR surface. The 1197-cell field is
contaminated by 594 unrun 0.0-default cells. The **only defensible gradient surface is the 603 MEASURED cells
(tally present = tier-2 actually ran)**.

## Corrected surface (measured-only, tier-2 actually ran)

| surface | floor ≤.05 | mid (.05,.95) | ceil ≥.95 | mid-fraction |
|---|---|---|---|---|
| ALL 1197 cells (Matt's read) | 714 | 1 | 482 | 0.001 |
| 594 unrun cells (0.0 default) | 594 | 0 | 0 | — |
| **603 MEASURED cells** | **120** | **1** | **482** | **0.0017** |

Per-scenario MEASURED-only: elite_pack 315/315 ceil; magic_pack 36/36 ceil; boss_with_adds 72 ceil / 117
floor; mini_boss 59 ceil / 3 floor / 1 mid. The single mid cell is in mini_boss.

## BOTTOM LINE

**The "mid-fraction 0.001 → still rails" §4 read is TRUE — and NOT confounded in the direction that would
rescue the surface.** The measurement artifact (594 unrun 0.0-default cells) inflates the floor count, but
removing every artifact cell leaves 603 genuinely-simulated cells that are STILL rails: 482 ceiling, 120
floor, exactly 1 mid → mid-fraction 0.0017. The WR surface did NOT regain a gradient; the levers moved cells
between the ceiling and floor rails, not into the (0.05, 0.95) interior. The design acceptance criterion
("mass in (0.05, 0.95), differentials as spread not rails") is **NOT met** on this run. Matt's headline read
stands; only the per-scenario winner-tally aggregates are artifact-driven and must not be read as a
death-vs-timeout split without restricting to the measured (tally-present) cells.
