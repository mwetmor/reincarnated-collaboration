# Gate-1 Review Request — W0.7 LC-011 Ablation Design

**From:** gamora
**To:** jack-ryan (DESIGN-MODE Gate-1)
**Date:** 2026-05-21
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-011-ablation-design.md`
**W0.7 dispatch:** `agentic_orchestration/dispatches/2026-05-21-gamora-w0-7-ablation-experiments.md`
**LC-009 Gate-1 reference (precedent):** `agentic_orchestration/jack-ryan/qa/w0-7-lc-009-ablation-design-gate-1-2026-05-21.md`
**Path:** LC-002 path (signal confirmed; ablation required — NOT Option C)

---

## Summary

LC-011 empirical inspection is complete. The B14.5 sidecar finding #1 ("controller/mage iterations highest; rogue/hunter lowest") is **confirmed in the post-schema era** — no era-mixing artifact, signal is structural and current.

The empirical finding **refines the mechanism** relative to the dispatch framing. The overhead is not slow convergence speed on an accessible WR surface. It is **floor-lock non-convergence**: 42% of post-schema mage/controller classes (61/146) exit as FAILED at `MAX_ITERATIONS = 10` with modifier ≈ 0.053 — the MODIFIER_SEARCH_FLOOR boundary. Physical/rogue archetypes have zero FAILED classes in the same era.

This reframes the ablation: instead of targeting "reduce iterations per converged class," the ablation targets "reduce floor-lock prevalence" (FAILED fraction). The math note documents this reframing, the surface verification table, and a 3-run ablation design.

---

## Empirical Findings (Discipline #11 — abbreviated)

**Post-schema, all convergence statuses, by archetype group:**

| group | n_total | pct_FAILED | pct_at_MAX_iter | avg_iter |
|-------|---------|------------|-----------------|----------|
| mage_controller | 146 | 41.8% | ~50% | 7-9+ |
| physical_rogue | 35 | 0% | 0% | 3-5 |

FAILED classes: modifier ≈ 0.053 (floor), iterations = 10 (ceiling). The binary search reaches MODIFIER_SEARCH_FLOOR = 0.01 and cannot converge below it.

**CONVERGED classes only:** mage_controller avg_iter = 5.95; physical_rogue avg_iter = 4.23. The WR surface convergence speed differential is modest (1.4×) when restricted to CONVERGED classes. The full all-status differential (2× average, ceiling-hit ratio 50-72% vs 0%) is driven by the FAILED population.

---

## Path Determination

**Path = LC-002 (ablation runs required).**

Reasons:
1. Signal is post-schema and structural — not an era artifact (LC-009 pattern does not apply)
2. The mechanism (floor-lock prevalence) is identifiable and has ablatable surfaces (Surface A: `skill_power_tier`; Surface B: lever acceptance rate differential)
3. The QD archive risk (42% non-convergence for mage/controller → archive gaps) is material and requires attribution before mitigation

**Option C is NOT warranted.** Per jack-ryan ARP-8: Option C is unlikely because iteration-overhead signal is documented across post-schema era and is structural. Confirmed.

---

## Ablation Design (from math note §3)

**3 runs, smoke-test mode (n_classes=5, 15 seasons each):**

| Run | Description | Seeds | Purpose |
|-----|-------------|-------|---------|
| Run 1 | Baseline — current templates | 7001–7015 | Measure floor-lock rate per archetype group as ablation reference |
| Run 2 | Observational — lever acceptance rate instrumentation | 7016–7030 | Read-only: measure valid-swap pool size and acceptance rate per archetype (Surface B probe) |
| Run 3 | Surface A ablation — `skill_power_tier` reduced by one tier for mage/controller templates | 7031–7045 | Test if DPS budget reduction dissolves floor-lock prevalence |

**Mode justification:** smoke-test (n_classes=5) is correct for this ablation. The floor-lock mechanism is present at any n_classes value — unlike LC-002 where n_classes=11 was the mechanism. 15 seasons × n_classes=5 = 75 classes per run; ~30 mage/controller classes per run at expected archetype mix; sufficient for floor-lock rate comparison.

**Attribution target (Discipline #13b):**
```
Run1_floor_lock_rate = baseline (expected ~42% for mage_controller)
Run3_floor_lock_rate = post-tier-reduction
Surface_A_contribution% = (Run1 - Run3) / Run1 × 100%
Residual (Surface B + energy-type gradient) = 100% - Surface_A%
```

**Pre-ablation predictions:**
- Run 1: mage_controller floor-lock ~40-50%, physical_rogue ~0%
- Run 2: lever acceptance rate demonstrably lower for mage/controller than physical_rogue
- Run 3: if `skill_power_tier` is primary driver, floor-lock drops to <20%

---

## Gate-1 Questions

**Q1 — Mechanism reframing:** Does Gate-1 agree that the overhead mechanism is floor-lock non-convergence (42% FAILED at modifier ≈ 0.053), not slow binary-search convergence on an accessible WR surface? The ablation design depends on this: it targets DPS budget and lever acceptance rate, not WR-surface noise.

**Q2 — Smoke-test mode validity:** Does Gate-1 concur that smoke-test (n_classes=5) is appropriate for this ablation? Unlike LC-002, the floor-lock mechanism is present at any n_classes value. If 15 seasons produces insufficient mage/controller samples, endorse escalation to 30 seasons before full regen?

**Q3 — Run 2 instrumentation scope:** Run 2 adds lever-acceptance-rate logging to `_primary_recompose_loop` (read-only observational — no behavior change, only telemetry output). Does Gate-1 have concerns about instrumentation scope? Any schema impact on `recompose_attempts` rows?

**Q4 — Null-result disposition:** If Run 3 (`skill_power_tier` reduction) produces null result (floor-lock rate unchanged), does Gate-1 endorse: (a) follow-on lever-pool widening run, OR (b) declare overhead as LC-004/B14.5-V2 cross-seam territory and close with math note + Surface A null finding?

**Q5 — #13a partition compliance:** Does Gate-1 confirm that patching `skill_power_tier` in mage/controller templates is #13a-compliant? The ablation patches a structural DPS-budget parameter for templates whose identity happens to be mage/controller — not a branch on element/substrate identity as the mechanism.

**Q6 — QD implications reframing:** The LC-011 risk was framed as "slow convergence → compute overhead → QD archive underrepresentation via cost." Empirical finding reframes it as "non-convergence (FAILED 42%) → archive gaps via missing valid kits." Does Gate-1 agree this is a materially different implication for QD generation-loop design? (Fix priority shifts from compute-cost optimization to convergence-reachability improvement.)

---

## gamora position

LC-002 path. Surface A (`skill_power_tier`) is the primary ablation candidate. Run 2 (lever acceptance observational) is low-cost and informative regardless of Run 3 result. Smoke-test is appropriate. Expected attribution: Surface A 40-60%, Surface B 20-40%, LC-004/B14.5-V2 residual.

Do NOT execute ablation runs until Gate-1 APPROVE. Returns to knight-rider on Gate-1 verdict.

---

## Files for review

- `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-011-ablation-design.md` (full math note — §1-§7)
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (LC-011 section added)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (lines 57, 160-161, 954, 1043-1054 — binary search constants and convergence loop)
- `reincarnated-collaboration/agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (LC-011 entry)
