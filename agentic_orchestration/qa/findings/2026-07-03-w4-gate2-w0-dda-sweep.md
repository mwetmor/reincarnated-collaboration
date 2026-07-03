# Finding — 2026-07-03 — W4 Gate-2 — W0 DDA-propagation sweep

**Reviewer:** jack-ryan (DEV-MODE)
**Severity:** PASS (INFO-only)
**Target:** `gamora/v-demo-run-w0-dda-sweep-1` @ `87c47a6`
**Developer:** gamora (simulation seam)
**Principles applied:** #1 (math-before-code), #2 (smoke-vs-full scope), #4 (decisions-log as truth), #5 (severity)

## What I found
The math note (`src/reincarnated/simulation/math/dda-propagation-live-floor-2026-07-03.md`) was authored before the sweep harness and derives the propagation-ON killing-blow arithmetic to a clean closed form: `max_army_boss_dps_NEW = max_army_boss_dps_OLD × dm_player_sp`, factor 0.6 at cert-fixture player power. This correctly recognizes the Gate-1 #1 catch — the flip establishes a NEW (lower) floor rather than re-earning the 1.0-hard-coded one. The two-arm OFF/ON structure is a genuine single-parameter isolation (#24): Arm-OFF reproduces the D3 cert byte-for-byte as a regression-equivalence proof before the flip, and the harness asserts per (kit,shell) that only `ally.damage_modifier` differs OFF→ON. Both melee summoners re-cert WR 1.0 both shells with 136s margin; empirical clear-time (103.7s) matches the analytic linear prediction (100.17s) within noise, corroborating the no-double-dip claim by construction AND empirically. Anchor held by construction (swept var disjoint from boss/swarm mob-dict fields). Disc #12 semantic-shift declared explicitly (interpretation change, not bug fix; routed to decisions-log G5 `a10a695`). All refutation conditions pre-checked and none fired.

## Rationale
Discipline #1 satisfied to the letter (math first, code-cited: `:1428/:1491/:1510/:1730/:1757/:1773/:2757/:3050`). Discipline #24 isolation is not merely asserted — it is structurally proven (Arm-OFF regression-equivalence) plus per-cell asserted. Discipline #3 seed hygiene clean (base 53,000,017, disjoint, sequential, no parallel regen). This is exemplary balance-loop discipline; no findings rise above INFO.

## INFO (for the record, non-blocking)
- The certification is a floor DECREASE (0.6×) at base gear — mathematically honest and conservative, but it means the demo summoners are certified at the *bottom* of the propagation curve. The gear-as-power UPSIDE (proxy DPS rising above 300 as player dm exceeds 1.0) is asserted but not measured this run — correctly deferred to the launch inheritance study (§6). No action; noting the certified envelope is base-only.
- Harness ranged player-kit delivers f_army=0 (D3 finding-2 artifact carried forward). The record correctly flags this as a harness artifact, not D2-dominance. Carried, not a defect.

## Action
- [x] Developer: none required — PASS.

## References
- `reincarnated-engine/src/reincarnated/simulation/math/dda-propagation-live-floor-2026-07-03.md`
- `reincarnated-collaboration/agentic_orchestration/dispatches/2026-07-03-gamora-w0-dda-propagation-sweep.md`
- Tag `gamora/v-demo-run-w0-dda-sweep-1` @ `87c47a6`
