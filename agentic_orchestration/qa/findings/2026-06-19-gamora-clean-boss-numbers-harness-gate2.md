# Finding — 2026-06-19 — gamora-clean-boss-numbers-harness

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO (no WARN, no BLOCK)
**Target:** commit `2f9c5c8` (gamora: clean boss-numbers measurement harness) — UNPUSHED
**Developer:** gamora (simulation seam)
**Principles applied:** #1 (math-before-code as the gate), #3 (cross-seam impact / no gate regression), #6 (reproduce on disk — do not take report on trust), #5 (severity matters)
**Disciplines cited:** #1 (math-before-code), #2 (smoke-test before full run), #3 (distinct seed base, no parallel regens), #11 (capture decision telemetry / stale-docstring records), #12 (semantic-shift declaration)

## What I found

I reproduced the harness's claims first-hand on disk rather than trusting its report. **V1 (load-bearing) holds at the source and as an emergent property of the data.** At `spatial_engine.py:1742-1771` the player-dead guard (`if not self.player.is_alive: winner="monster"`) is checked FIRST in both the `boss_killed` (1745) and `mini_boss_killed` (1762) branches, so `winner=="player"` is reachable only in the `elif ... not boss_alive/mb_alive` branch — i.e. `winner=="player"` ⇒ boss/mini-boss DEAD **and** player ALIVE, by control flow. The chain to `survival_rate` is intact (`player_won = fr.winner=="player"` at :1078 → `FightSummary.player_won` :1093 → `StratumFightBatch.wins` :226-227 → `survival_rate = wins/n_fights` :230-233). The harness's per-cell V1 self-consistency assertion (`b_dead == wins == winner_player`, else `raise AssertionError`) is genuinely present at harness :158-165 and is structured to fail loud and NOT emit a table. I recomputed the invariant independently across all **1,056 cells** straight from the raw `cells` array (ignoring the harness's own pass flag): **0 violations** of `b_dead==wins`, `survival_rate==wins/n`, and `Σtermination_counts==n_fights`, and **0 non-canonical (stalemate) termination labels**. The bypass is **measurement-only with no gate regression**: the harness imports and *calls* `w4g2_tier_2_full_sim` (the standalone instrument, `t4_sim_cycling.py:1199`), and the only files it writes are its own diagnostic JSON/TXT (harness :448/:452); production gate files (`gauntlet_sim.py`, `arena.py`, `spatial_engine.py`, `combatant.py`) are untouched in git status. The only runtime mutation is the smoke-gated `TIER_2_FIGHTS_STANDARD` swap, restored in a `finally` block (:417-419), so the full run used the prod default (20) — matching the output's `n_fights_per_cell: 20`. The headline numbers reproduce exactly: independent re-aggregation of `by_attribute`, `by_attribute_shell`, and `by_archetype` from raw cells MATCHES the harness's `aggregations` block bit-for-bit (STR surv+kill=0.000 / timeout=1.000 on **both** shells; int=0.992; wis=0.984; dex=0.786), and **a_dead=0 across all 21,120 fights**. The smoke artifact demonstrates tier_2 actually firing on BOTH boss shells (the production-path failure was tier_2-never-ran) at n_fights=4.

## Rationale

- **V1 verified at source AND in data (Principle #6, Discipline #1).** I did not accept the math note's PASS — I read `spatial_engine.py:1742-1771` first-hand and confirmed the player-alive-first control flow, then recomputed the `b_dead==wins==surv*n` invariant across all 1,056 cells from the raw array. Both agree. On these `*_killed` shells `survival_rate` IS the survive+kill rate; the table is not built on a false signal. This is the exact failure mode the run existed to avoid, and it is cleanly avoided.
- **No gate regression (Principle #3, dispatch acceptance criterion + run-brief endorse-criterion 5).** The tier_1-reject bypass is achieved by calling the standalone tier_2 directly, never executing the caller-gate `continue`. No edit to `gauntlet_sim.py`, `ENCOUNTER_COHORT_KPM_BAND`, `gauntlet_pass`/`eligible_encounters_passed`, the tier_1 routing, or any persisted telemetry schema. `production_gate_modified: False` is accurate. No MIGRATION.md required (no cross-seam contract change — read-only diagnostic), per ADR-004 / dispatch §63-64.
- **gamora's KR-citation correction is CORRECT (Discipline #11).** The runtime short-circuit is `gauntlet_sim.py:1019` (`if t1_routing == TIER_1_REJECT:` → `continue` at :1029, skipping the tier_2 call at :1032). KR's cited `t4_sim_cycling.py:1452` is a fight-COUNT tally expression (`r.tier_2_batch.n_fights if ... r.tier_1_outcome != TIER_1_REJECT`) inside quality-report finalization — it reflects the same fact but is not the runtime gate. I confirmed both lines first-hand.
- **V2 / V3 / V4 confirmed.** V2: `boss_with_adds` and `mini_boss` both `max_duration_s=240.0` (arena.py:522 / :764), mini_boss `soft_timeout_s=150.0` (:768), read live from `ALL_SCENARIOS` into output metadata (not hard-coded). V4: `mobs_killed = sum(1 for m in self.mobs if not m.is_alive)` (spatial_engine.py:1740) is attribution-agnostic by construction. V3 (faithful power = max-profile-investment default, flip #3) is documented through the call chain in the math note §4; the harness drives the default chain without overriding `apply_max_profile_investment`, so faithful power applies by construction. The two stale docstrings gamora flagged are confirmed harmless: `t4_sim_cycling.py:252` ("120s") annotates the generic `fights_resolving_under_max` property, not the boss cap; `combatant.py:506` ("default False") contradicts the actual `=True` signature at :486 — the signature is authoritative and is what executes.

## Severity calls

The single INFO (below) is a cosmetic metadata-key glitch in the SMOKE payload only. It does not touch the full-run JSON, any number gandalf consumes, or any verify-gate. Per Principle #5 it does not rise to WARN. The substantive verdict is **PASS**.

## INFO (for the record, non-blocking)

- **INFO-1 (cosmetic, smoke-only):** in the smoke payload `metadata.n_configs_driven` is `None`. In smoke, `population` is truncated to `population[:1]` AFTER `n_configs_total` is captured (harness :359-370), and the meta dict reports `n_configs_driven: len(population)` — which is 1 in smoke, so the `None` indicates the smoke meta is keyed slightly differently than the full payload. The **full-run JSON has `n_configs_driven: 66` correct**, and the smoke run's purpose (prove tier_2 fires on both shells) is independently demonstrated by its 2 cells. No effect on any consumed number. Optional one-line tidy if gamora revisits the harness; not required for this run.
- **INFO-2 (scope clarity, not a defect):** the run drives 4 boss-shell *encounters* (3 `boss_with_adds` + 1 `mini_boss`) × 4 cohorts × 66 configs = 1,056 cells, not "2 shells × …". The math note §6/§7 and dispatch language say "2 shells"; that refers to the two *scenario shells* (win-condition templates), and the harness correctly iterates all catalog encounters carrying those shells. n per attribute cell exceeds §5 sizes (str/dex/int n=3,840; wis n=9,600 vs §5's 144/360) because all 4 cohorts are driven unconditionally — satisfies the "≥ §5, not underpowered" acceptance criterion. Recorded so the grain is unambiguous for gandalf's corrected §5.

## Headline reproduction (the doctrine-relevant numbers, recomputed from raw cells)

| attribute | n_fights | surv+kill | b_dead | a_dead | timeout |
|---|---|---|---|---|---|
| str | 3,840 | **0.000** | 0.000 | **0.000** | **1.000** |
| dex | 3,840 | 0.786 | 0.786 | 0.000 | 0.213 |
| int | 3,840 | 0.992 | 0.992 | 0.000 | 0.008 |
| wis | 9,600 | 0.984 | 0.984 | 0.000 | 0.016 |

STR is **timeout-dominant, not death-dominant** (a_dead=0 on every one of its 192 cells; all 192 are timeout=20/20, wins=0). The "STR boss-crater" (`survival=0.0` in phase3) is reproduced as a **too-slow-but-survivable** signal once tier_2 actually runs — i.e. the legitimate slow boss kill the tier_1 KPM ceiling structurally condemned before survive+kill was ever simulated, NOT a real defensive failure. This is the load-bearing input to the doctrine decision and it is real on disk.

## Action

- [x] jack-ryan: V1 verified at source + recomputed across all 1,056 cells (0 violations). Aggregations reproduced bit-for-bit. Bypass confirmed measurement-only, no gate regression. PASS-WITH-INFO.
- [ ] gamora (optional, non-blocking): tidy smoke-payload `n_configs_driven` key (INFO-1) if the harness is revisited. Not required for this run.
- [ ] Matt: none required (no BLOCK, no escalation). Within ADR-002 jack-ryan approval authority (read-only diagnostic, no cross-seam schema change, no gate change).

## References

- Harness: `~/Games/reincarnated-engine/src/reincarnated/simulation/clean_boss_numbers_harness_2026_06_19.py`
- Math note: `~/Games/reincarnated-engine/src/reincarnated/simulation/math/clean-boss-numbers-harness-2026-06-19.md`
- Output: `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/clean-boss-numbers-harness-2026-06-19.{json,txt}` (+ `-smoke.{json,txt}`)
- V1 source: `spatial_engine.py:1742-1771` (resolution), `:1418-1450` (loop-exit), `t4_sim_cycling.py:1078/1093`, `:226-227/230-233` (chain to survival_rate)
- Runtime gate bypassed (verified): `gauntlet_sim.py:1019` (`if t1_routing == TIER_1_REJECT: ... continue` at :1029, skipping :1032). KR-cited `t4_sim_cycling.py:1452` confirmed to be a fight-count tally, not the gate.
- V2 caps: `arena.py:522` (boss_with_adds 240s), `:764`/`:768` (mini_boss 240s hard / 150s soft)
- V4: `spatial_engine.py:1740` (`mobs_killed`)
- Stale docstrings (harmless, confirmed): `t4_sim_cycling.py:252` (120s), `combatant.py:506` (default False vs `=True` at :486)
- Dispatch: `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-19-gamora-clean-boss-numbers-harness.md`
- Run brief: `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-06-19-kr-clean-boss-numbers-run-prompt.md`
