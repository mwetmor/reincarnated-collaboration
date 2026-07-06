# Light read — 2026-07-06 — leg4 calibration + attribution derivations

**Reviewer:** jack-ryan
**Type:** LIGHT READ (confirm-or-flag; no Gate, no BLOCK authority) — notes/analysis only, no production code.
**Target:** commit `dddd569` (engine); edits confined to `simulation/notes/` + `AGENT_STATE.md`.
**Developer:** gamora
**Scope authority:** Matt-approved unit; gandalf ruled light read; KR's call on formality.
**Principles applied:** #1 (math-before-code), #11 (empirical inspection), #1.2 (code citations).

## Job
Confirm the two load-bearing derivations that propagate to batch-2. NOT a re-litigation of the C2 ruling (Matt ruled it); NOT a fault for absent re-emit/re-fight (deferred to batch-2 by design).

## Claim 1 — C2 plain-caster floor: CONFIRMED
`bar_lo` = 9.90 KPM (open_arena) / 11.65 KPM (chokepoint).

- Byte-verified against `gauntlet_sim.py:393-394`: `open_arena` lo=9.90, `chokepoint_corridor` lo=11.65, Balanced/Hybrid columns identical (band cohort-invariant per `:389`).
- Baseline 0.0/0.0 was Gate-2-verified (caster reads 0.0 both shells). `gap = bar_lo − 0.0 = bar_lo` is arithmetically correct.
- The 0.0 is a hard timeout (below-floor, not near-miss), so `required_summon_KPM_contribution = max(0, bar_lo − 0.0) = bar_lo` holds under the degenerate-case guard.
- **"Predominantly structural / band-re-tune-alone-may-be-insufficient" is a DEFENSIBLE read, not overreach.** A full timeout-to-floor jump (zero kills → 9.90/11.65) is qualitatively distinct from a marginal miss, and it is corroborated by the independent AGENT_STATE Session-48 W3 autopsy (4/10 pure structural + 6/10 ST-sustain/resource-economy collapse). Correctly framed as a measurement OUTPUT with the fix deferred to batch-2 config.

## Claim 2 — magic_pack 600.0 metric-domain artifact: CONFIRMED
Verdict "1/tick-floor quantization artifact, NOT a min=max clamp; report as `≥`-ceiling."

- `observed_kpm = total_kills / (total_duration_s / 60.0)` verified at `t4_sim_cycling.py:277`.
- `TICK_SIZE=0.1s` quantization + `1/(0.1/60)=600` = 1/tick-floor verified at `:108-113`.
- `CLEAR_SHELL_DOMAIN_TMIN_S=1.0` verified at `:117`; sub-`T_min` completion-gate routing (`term=b_dead`, no timeout; KPM not consulted) verified at `:729-739`. Engine already routes sub-tick clears on completion — the artifact mechanism is recognized in-code.
- Mechanism is a metric-domain quantization floor, NOT a clamp — verdict correct.
- Reporting 600.0 as a `≥`-ceiling and treating **elite_pack 426.9 (genuine spread 163.6–450.0)** as the real pack-overperformance signal of record is the RIGHT call. magic_pack is ABOVE_CEILING either way, so the calibration verdict on that shell is unaffected by the true (unresolvable, sub-tick) value.

## Action
- [x] Both derivations confirmed trustworthy to anchor batch-2. No flags, no caveats material to propagation.
- No developer action required. No Matt escalation (no BLOCK, no conflict with locked decisions-log entry).

## References
- `reincarnated-engine/src/reincarnated/simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` (§2.2, §2.3)
- `reincarnated-engine/src/reincarnated/simulation/notes/leg4-attribution-report-2026-07-06.md` (§2)
- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:393-394`
- `reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py:108-117,273-277,729-739`
- Companion: `agentic_orchestration/qa/pending/2026-07-06-pilot-measurement-report-gate2.md` (the sealed Gate-2 measurement-report review this light read builds on)
