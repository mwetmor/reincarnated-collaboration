# Gate-1 Re-Review — W0.7 LC-002 Ablation Experiment Design (Post-BLOCK Amendment)

**Date:** 2026-05-21
**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE Gate-1 re-review (amendment fold-in verification)
**Author under review:** gamora
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md`
**Re-submit dispatch:** `agentic_orchestration/dispatches/2026-05-21-jack-ryan-gate1-resubmit-w0-7-lc-002-ablation-design.md`
**Prior verdict:** `agentic_orchestration/jack-ryan/qa/w0-7-lc-002-ablation-design-gate-1-2026-05-21.md`
**Principles applied:** Discipline #2, #3, #10, #11, #13a-partition, #13b

---

## Top-line verdict: APPROVE

All four amendments resolve their respective findings. BLOCK-1 is lifted. The three non-blocking amendments (AMEND-1/2/3) are adequately addressed. gamora has a green light to proceed to LC-002 ablation execution.

---

## Per-amendment findings

### BLOCK-1 — Measurement mode resolution: PASS

**Code verification:** Lines 296-297 of `season_orchestrator.py` read:

```python
if smoke_test:
    n_classes = 5
```

This is an unconditional assignment inside the `smoke_test` branch, executed at line 297 before the `rng` initialization at line 300 and before line 475's `n_classes = n_classes or int(rng.integers(*CLASS_COUNT_RANGE))`. The `or` guard at line 475 only substitutes if `n_classes` is falsy — but line 297 has already set it to the integer `5`, which is truthy. gamora's observation is correct: any caller-supplied `n_classes` override is silently overwritten when `smoke_test=True`. The n_classes=11 override path jack-ryan suggested in the prior verdict is not viable without modifying the orchestrator.

**Amendment verification:**
- §4 final paragraph documents the mode decision explicitly, names Discipline #10 as the override rationale, and explains why smoke-test eliminates the mechanism under study. Adequate.
- §5.1 run command updated to `generate-season --seed <N>` with no `--smoke` flag. Wall-time estimate (10-15 min/run, ~30-45 min total) is stated. Adequate.
- §9 measurement protocol steps reference "full regen" at each run step (steps 2, 7, 10). No smoke-test language remains. Adequate.
- §10 amendment log accurately summarizes the resolution.

**Cost-benefit against Discipline #3:** Discipline #3 prohibits parallel regens of the same seed; it does not mandate smoke-test preference over correctness. Discipline #2 (smoke-test for rapid iteration) is correctly subordinated here per Discipline #10 — the mechanism under study (modulo-index bias at n_classes=11) does not exist under smoke-test conditions. 30-45 minutes of wall time is proportionate to the signal being measured. No concern.

**Verdict: PASS. BLOCK-1 lifted.**

---

### AMEND-1 — Element order: PASS

**Config verification:** `config/elements.yaml` lists elements in declaration order: fire, water, earth, wind, physical. This matches the corrected §2 claim in the math note: `fire(0), water(1), earth(2), wind(3), physical(4)`.

**Prediction table (§5.4) verification:**
- Under the correct ordering, all non-fire elements sit at indices 1-4. For n_classes=11, each non-fire element receives exactly 2 assignments (laps: 2 full laps of 5 = indices 0-9, plus one extra at index 10 which is index 0 again = fire). Non-fire elements are therefore symmetric at 2/11 = 18.2% per element per n=11 season.
- Blended across a 50/50 n=10/n=11 mix: non-fire elements land at ~19.1-19.5%, matching the revised table. Prior erroneous predictions (wind ~17.6%, earth ~19.7%) are removed.
- Run 2 rotation derivation: with 15 seasons and offset `season_index % 5`, each element starts exactly 3 seasons. Over 15 seasons × n=11: each element gets 3 starts × 3/11 + 12 non-starts × 2/11 = 9/11 + 24/11 = 33/165 = 20.0%. This derivation is independent of which specific element occupies which index — it holds under the corrected order identically.
- The attribution claim (fire at index 0 → 27.3% for n=11) is unaffected by the element order correction, as stated.

**Verdict: PASS.**

---

### AMEND-2 — n_classes stability caveat: PASS

**§7 text verified.** The added caveat reads:

> "The round-robin attribution (3/11 = 27.3% fire for n=11) and the proposed fix's effectiveness are contingent on n_classes remaining in the 10-12 range. `CLASS_COUNT_RANGE = (10, 12)` currently produces n=10 or n=11. If n_classes shifts outside this range in the QD-rebuild context (e.g., archive insertion overrides to a fixed count, or P3 cohort sizing changes), the modulo arithmetic changes and the over-representation magnitude changes accordingly. If n_classes=5 is ever fixed uniformly (smoke-test scenario or a future override), the bias disappears without any fix because 5 % 5 = 0 (all elements equal). The fix's effectiveness should be re-verified whenever CLASS_COUNT_RANGE changes."

**Adequacy check:**
- P3 archive-insertion risk: explicitly named ("P3 cohort sizing changes"). Adequate.
- Smoke-test scenario preserved: explicitly named ("smoke-test scenario or a future override"). Adequate.
- Machine-readable form: the caveat is a prose paragraph, not a structured assertion. This is acceptable for a math note; the conditions are stated precisely enough to be actioned by a future reader.
- The caveat does not claim P3 changes are imminent — it correctly frames them as a future verification trigger.

**Verdict: PASS.**

---

### AMEND-3 — Telemetry isolation (seed change): PASS with one observation

**Seed/season_id logic verified.** Line 301: `season_id = season_id or f"season_{seed:06d}"`. Seeds 9001/9002/9003 produce season_id prefixes `season_009001`, `season_009002`, `season_009003`. These are distinct; no row-overwrite risk across runs. §5.3 correctly documents the rationale.

**Observation (non-blocking, for gamora's awareness):** The re-submit dispatch raises whether seeds 9001/9002/9003 (sequential) are adequate vs. more independent seeds like 9001/4441/7771. The question is whether sequential seeds produce correlated n_classes draws. Since `rng = np.random.default_rng(seed)` initializes independent RNG state per seed, sequential integer seeds (9001, 9002, 9003) produce uncorrelated draws — numpy's PCG-64 generator does not exhibit sequential-seed correlation at this scale. The concern is not founded. The sequential seeds are acceptable.

**Additionally:** gamora's documentation in §5.3 of the cross-seed n_classes variance as an accepted secondary variable is appropriately transparent. The prediction is formula-based and accounts for whatever n=10/n=11 mix the seed produces; the attribution question remains the assignment method. No issue.

**Verdict: PASS.**

---

## Carry-forward attestation

Prior PASS findings from the initial Gate-1 verdict carry forward without re-examination:

- **Q1 (surface disambiguation — round-robin correctly targeted):** CARRY FORWARD PASS. Nothing in the amendments touches §2 or §3 analytical attribution. Surface B (D1 pool) and Surface C (ELEMENT_AFFINITY) remain ruled out by code audit.
- **Q2 (sidecar finding #4 — classes.canonical_element column identity):** CARRY FORWARD PASS. No change to §1 or the empirical telemetry framing.
- **Q4 (#13a-partition compliance of seed-derived rotation offset):** CARRY FORWARD PASS. §5.4 Run 2 derivation is unchanged in structure; the amended element order does not alter the partition-compliance assessment. The offset derives from `season_index`, a structural scheduling property, not from element identity.

---

## Run-readiness statement

**Green light to execute.**

gamora may proceed with the following execution plan as documented in the revised math note:

- Run 1: full regen, seed 9001, baseline round-robin measurement
- Run 2: full regen, seed 9002, modulo-rotation patch (season_index % 5 start offset)
- Run 3: full regen, seed 9003, random element assignment
- Post-run: attribution write-up per §9 protocol, then tag `qd-rebuild/v0.7-ablation-lc-002`

Precondition: gamora records the `classes` table row count before each run and isolates new rows by season_id prefix post-run, as specified in §9. This precondition was already in the protocol and is confirmed by the amended §5.3.

---

## Process recommendation refresh

The prior verdict recommended: gamora applies Discipline #11 empirical surface inspection to LC-009 and LC-011 before authoring their math notes, using LC-002 as the template. knight-rider does NOT pre-amend the W0.7 dispatch for those LCs.

**This recommendation stands unchanged.** Nothing in the amendment fold-in alters the underlying reasoning:

1. The LC-002 amendment log shows that AMEND-1 (element order) was caught only because gamora performed a code-level config read against `config/elements.yaml`. The same pattern of verifying surfaces against actual source before populating prediction tables is the correct prior for LC-009 and LC-011.
2. The BLOCK-1 resolution reinforces that the dispatch's surface hypotheses can be wrong in ways that only code inspection reveals. This is exactly the risk Discipline #11 is designed to mitigate.
3. No new evidence from this fold-in suggests LC-009 or LC-011 surfaces are clean without inspection. The prior recommendation to treat the dispatch as a starting hypothesis, not a verified surface map, holds.

**The gamora-applies-Discipline-#11-per-LC pattern is the right process for the next two LCs.** Gate-1 for LC-009 and LC-011 will review the surface verification table (§2 of each math note) before assessing experiment design.

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` lines 296-297, 301, 475
- `/Users/admin/Games/reincarnated-engine/config/elements.yaml` lines 1-4 (fire, water, earth, wind declaration order)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md` §4, §5.1, §5.3, §5.4, §7, §9, §10
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/jack-ryan/qa/w0-7-lc-002-ablation-design-gate-1-2026-05-21.md` (prior verdict)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-21-jack-ryan-gate1-resubmit-w0-7-lc-002-ablation-design.md`
