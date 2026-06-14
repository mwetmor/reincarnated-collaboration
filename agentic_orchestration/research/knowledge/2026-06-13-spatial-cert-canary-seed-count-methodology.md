# Research — RESOLVE Canary Seed-Count and Decision Rule for K1@Chokepoint — 2026-06-13

**Mode:** A (analytical)
**Commissioner:** knight-rider (routed from gandalf § 2-S.4 conditional trigger; pre-authorized by Matt)
**Sources consulted:**
- `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` (§ 5, §6.1, §7, §2-S.4)
- `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json` (per-fight, per-seed KPM data, 6 kits × 6 rooms × 5 seeds)
- Statistical methods: one-sample t-test (one-sided), binomial power analysis, likelihood ratio comparison

---

## Summary (4 sentences)

The spatial engine's K1@chokepoint variance is real but bounded: the per-seed KPM spread is CV=8.9% (SD=1.67 on mean=18.78), and the mean sits 1.03σ below the floor — close enough that a single seed crosses the floor with probability ~15%, explaining the 4/5 BELOW observation. The three open_arena canaries are in an entirely different regime (K1 open_arena is 4.06σ below its floor; K4 and K5 open_arena are >4.5σ above theirs) and are stable regardless of rule choice. For the K1@chokepoint canary, the strict every-seed rule (N=5) passes a correct engine only 44% of the time — a near-coin-flip — while a **7-of-9 majority rule** delivers 85.6% true-pass rate with only 0.5% false-pass risk against a marginal IN kit. A one-sided t-test at α=0.10 on the pooled N-seed mean is the cleanest alternative: it already passes the existing 4/5 baseline (t=−2.30, p=0.041) and at N=9 reaches 95.5% power with 0.2% false-pass rate.

---

## Findings

### 1. Variance characterization

**Per-seed KPM for all canary cells, from spike data:**

| Canary cell | Per-seed KPM (5 seeds) | Mean | SD | CV | Floor | Margin (σ) | Seeds BELOW |
|---|---|---|---|---|---|---|---|
| K1 @ open_arena | 16.27, 18.82, 16.49, 17.14, 17.78 | 17.30 | 1.04 | 6.0% | 21.5 | 4.06σ below | 5/5 |
| K1 @ chokepoint | 17.20, 20.87, 19.20, 19.67, 16.96 | 18.78 | 1.67 | 8.9% | 20.5 | 1.03σ below | 4/5 |
| K4 @ open_arena (IN) | 41.38, 45.71, 41.38, 45.71, 45.71 | 43.98 | 2.37 | 5.4% | 21.5 | 9.47σ IN | 5/5 IN |
| K5 @ open_arena (IN) | 34.04, 38.40, 34.04, 30.57, 36.36 | 34.68 | 2.93 | 8.4% | 21.5 | 4.50σ IN | 5/5 IN |

**Finding:** The engine's within-cell variance is structurally tight for cells far from the floor edge (CV ≈ 5–9%). The K1@chokepoint cell is the sole case where the mean is within ~1σ of the floor; this is a funnel-compression physics effect (queuing-boosted single-target rate) not a general engine instability. The three open_arena canaries are 4–9σ from their respective floors and are verdict-stable under any sensible rule.

**Context — K3@chokepoint variance is notably higher (CV=26.9%):** This is expected and non-problematic. The line kit's performance in the corridor is highly spawn-geometry-sensitive (whether the line aligns with the queue); seeds that land K3@chokepoint at 21–45 KPM all remain IN (above floor=20.5 at all seeds). This is high variance in absolute KPM but not a floor-crossing problem.

### 2. Seed-count recommendation

**Problem framing:**  
K1@chokepoint has a per-seed BELOW probability of p ≈ 0.849 (estimated from observed mean and SD via normal CDF). This is not a clean 95%+ per-seed probability, so any seed-count rule that requires unanimity or near-unanimity will fail frequently on a correct engine.

**Binomial power — P(true-BELOW kit passes canary) by rule:**

| Rule | N seeds | k threshold | P(correct engine passes) | P(IN kit @floor+0.5σ false-passes) |
|---|---|---|---|---|
| Strict every-seed | 5 | 5/5 | 0.44 | 0.003 |
| 4-of-5 (80% majority) | 5 | 4/5 | 0.83 | 0.034 |
| Strict every-seed | 9 | 9/9 | 0.23 | <0.001 |
| **7-of-9 (78% majority)** | **9** | **7/9** | **0.856** | **0.005** |
| 6-of-9 (67% majority) | 9 | 6/9 | 0.965 | 0.029 |
| 9-of-11 (82% majority) | 11 | 9/11 | 0.775 | 0.001 |
| One-sided t-test α=0.10 | 5 | mean — | 0.780 | 0.004 |
| **One-sided t-test α=0.10** | **9** | **mean —** | **0.955** | **0.002** |

**The 4-of-5 rule at N=5 is marginal:** 83% true-pass power, but 3.4% false-pass risk against a marginally-IN kit (floor+0.5σ). For a canary gate where a false-pass means a genre-fatally broken engine escapes cert, 3.4% is uncomfortably high. 

**Recommendation on N:** N=9 seeds for the chokepoint room specifically. The chokepoint corridor introduces compression physics that inflates single-target KPM relative to the open_arena floor regime. The 5-seed baseline is sufficient as a scale anchor (it already confirms the BELOW direction with p=0.041) but is underpowered for a strict majority canary rule. Adding 4 seeds brings any reasonable majority rule above 85% power.

### 3. Decision-rule recommendation

**The strict every-seed rule must not apply to variance-sensitive cells.** At p_per_seed=0.849, even with N=100 seeds the strict rule fails ~0.000001 of the time — fine — but the point is it fails 44% of the time at N=5 and 23% at N=9. That is unacceptable false-fail rate for a canary gate (a false-fail here means stalling W-C on a correct engine unnecessarily).

**Two viable rules:**

**Rule A — 7-of-9 majority (recommended for variance-sensitive cells):**
- Run 9 seeds for the chokepoint room. Canary passes if ≥7 of 9 per-seed verdicts are BELOW.
- Power: 85.6% (correct engine passes 5 of 6 times)
- False-pass rate: 0.5% (a genuinely IN kit at floor+0.5σ passes as BELOW in 1 of 200 cert runs)
- Clean to implement: same verdict-counting framework gamora already uses; just change threshold and N for this cell.
- Current 4/5 baseline: would need 4 additional seeds with ≥3 of the 4 new seeds BELOW to achieve the 7/9 gate.

**Rule B — one-sided t-test, α=0.10 on pooled mean (recommended if analytical cleanliness is prioritized):**
- Run N seeds; classify BELOW if the one-sided t-test (H₀: μ ≥ floor; H₁: μ < floor) rejects at α=0.10.
- At N=9: power = 95.5%, false-pass rate at floor+0.5σ = 0.2% — better on both dimensions than 7-of-9.
- The existing N=5 data already passes this test: t=−2.30, p=0.041 < 0.10.
- Interpretive advantage: expresses "the mean is reliably below the floor" rather than counting binary per-seed flips.
- Operational cost: gamora needs to compute sample mean and SE; slightly more code than count-based rule.

**Asymmetry clarification:**  
For a BELOW canary, the catastrophic error is **false-pass** (the engine is broken — K1 is genuinely IN-band — but the rule calls BELOW and cert passes). That would mean 1D's single-target-bias has leaked into 2D undetected. The **false-fail** error (correct engine stalls cert) is costly in time but not in correctness. Therefore, the false-pass rate is the binding constraint. Both Rule A and Rule B deliver false-pass rates below 1% against the worst credible IN kit (floor+0.5σ); the strict every-seed rule at N=5 delivers 3.4% on the 4-of-5 variant, which is borderline.

**Rule for stable cells (open_arena canaries K1/K4/K5):** the original "every seed" rule is fine for cells where the mean is ≥4σ from the floor. These cells are variance-immune at any N≥3. No change needed.

### 4. Specific call for K1@chokepoint

**Current 4/5-BELOW baseline under each rule:**

- **Strict every-seed (N=5):** FAILS. One seed (20.87 KPM) crosses the floor (20.5). The engine is correct; the rule fails it.
- **4-of-5 majority (N=5):** PASSES immediately. 4/5 ≥ threshold. Power 83%, false-pass 3.4%.
- **7-of-9 majority (N=9):** INCOMPLETE — needs 4 more seeds; passes if ≥3 of 4 new seeds are BELOW (expected: ~3.4 of 4 will be, so this is near-certain with the correct engine).
- **One-sided t-test α=0.10 (N=5 already):** PASSES immediately. t=−2.30, p=0.041 < 0.10. No additional seeds required.

**Legolas call:**  
The existing 4/5 BELOW baseline classifies K1@chokepoint as BELOW under the **one-sided t-test α=0.10 rule at N=5** and under the **4-of-5 majority rule**. If gandalf/gamora elect the 7-of-9 majority rule (stronger guarantee), the existing data is directionally consistent but 4 additional seeds are needed — which with the observed distribution will almost certainly produce ≥3 additional BELOW seeds and confirm the canary.

The t-test path is the most efficient: it passes the canary now from the existing baseline, with a 95.5% power guarantee if run again at N=9, and leaves the pack-size lever (oracle §4.A) available if the separation is judged insufficiently robust by the designers.

---

## Knowledge gaps not resolved

1. **Per-seed independence assumption.** The analysis assumes seeds produce independent KPM draws. If the engine's RNG has seed-correlation (e.g., seeds that share a spawn-position RNG stream), the effective N is smaller than the literal seed count. No per-seed RNG architecture information was available; gamora should confirm seeds are independently seeded at the fight level.
2. **Distributional shape.** The normal approximation is used for per-seed KPM (justified for KPM = kills/elapsed where elapsed is a sum over kill events — CLT applies). With N=5 seeds the normality assumption for the t-test is shaky; the actual distribution could be heavier-tailed due to collision-geometry outliers. This slightly inflates the true false-pass rate above the nominal t-test value. At N=9 the CLT is more reliable.
3. **Floor sensitivity.** The analysis is conditioned on the recalibrated floor of 20.5 for chokepoint. If W-C-full's pack-size tuning or gamora's W-C anchor re-derivation shifts the floor by ±1 KPM, all the above probabilities shift accordingly. The K1 mean at 18.78 is robust to a ±0.5 KPM floor adjustment; it would require the floor to drop to ≤17 to threaten the BELOW classification.

---

## Source list

- Oracle spec (v1.2): `/canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — accessed 2026-06-13
- Spike data: `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json` — accessed 2026-06-13; 6 reference kits × 6 rooms × 5 seeds
- Methods: binomial CDF (scipy.stats.binom), normal CDF (scipy.stats.norm), Student t-test (scipy.stats.t), one-sided formulation

---

**Filed by:** legolas, 2026-06-13
**For:** knight-rider → gandalf/gamora (RESOLVE cert methodology decision, W-C-full)
