# Research — M1.3.5 Methodology Consult: Displacement Practical-Significance Floor + Seed-Count

**Mode:** A (analytical methodology)
**Commissioner:** knight-rider (Discipline #18 extension-hotspot trigger, post-first-sweep)
**Date:** 2026-06-16
**Sources consulted:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/m1-3-5-reduced-spatial-frontier-sweep-2026-06-14.md` (gamora, sweep math note + §9 POST-RUN FINDINGS)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-14-reduced-spatial-search-substrate-discrimination-floor-acceptance-spec.md` (gandalf, discrimination-floor acceptance spec)
- `/Users/admin/Games/reincarnated-engine/output/m1-3-5-frontier-sweep-2026-06-14.json` (raw per-config sweep data, N=12/cell)

---

## Summary (4 sentences)

The displacement metric at tick≥0.5 is statistically resolvable (SE=0, perfectly deterministic) but represents physical collapse: K4 travels only 9–9.6m total in a 43–68s fight, compared to 216.83m in 240s at commit grade — a different fight regime entirely, not a noisier version of kiting. A raw-magnitude floor of **≥20m signed displacement** (approximately 10% of commit-grade K4 absolute displacement or ~12% of commit-grade reference separation) cleanly separates the two genuinely kite-honest ticks (0.1 and 0.2) from every failing tick, with no ambiguous middle cases. The tick=0.3 sign-flip is a **structural deterministic discontinuity**, not sampling noise: SE=0 at tick=0.3 (12 seeds all return identical values), so no increase in N can stabilize it — the fight regime itself flips (K4 kills the boss in 51s at tick=0.3 versus timing out at 240s at tick≤0.2), making the displacement value meaningless as a kite signal. The recommended action is to **exclude tick≥0.3 from the kite-honest region** and treat tick=0.2 as the coarsest viable kite-floor tick, requiring no additional seeds.

---

## Q1 — Practical-Significance Floor for Kite-Floor Displacement (Axis-1)

### The problem with Cohen's d here

The standard standardized-effect-size path (Cohen's d, Glass's Δ) is inapplicable to this dataset. Every cell at tick≥0.2 has within-cell displacement SE=0 (pstdev=0 across all 12 seeds): the simulation is deterministic — identical seed → identical displacement. Cohen's d with a pooled-SD denominator of zero is undefined; even at tick=0.1 where K4 has SD≈0.24m, Cohen's d = 1003, which is not informative. The entire tick range returns "infinite" or "undefined" standardized effect size regardless of whether the margin is 171.98m or 0.38m.

**Conclusion: a raw-magnitude floor anchored to a physical scale is the correct tool here, not a standardized effect size.**

### Physical scale anchor

Three candidate anchors:

| Anchor | Value | Floor at 10% | Floor at 20% |
|---|---|---|---|
| Commit-grade K4 absolute displacement (tick=0.1, 240s fight) | 216.83m | 21.7m | 43.4m |
| Commit-grade K4−K6 reference separation | 171.98m | 17.2m | 34.4m |
| Arena size | not in data | — | ROUTES TO GANDALF |

The arena-size anchor requires a value not in the sweep data or spec. The two in-data anchors converge: both place the floor in the 17–43m range, and any floor in that range produces identical classification outcomes across all six tick levels. This robustness means the exact percentage choice within that band is a design-judgment call, not a statistical one (see "Routes to Gandalf" below), but any defensible choice within the band gives the same answer.

### Recommended floor

**≥20m signed displacement margin** (absolute raw meters, must also be sign-correct: K4 > K6).

Rationale:
- ~10% of commit-grade K4 absolute displacement (216.83m). A margin below 10% of the reference kiting extent cannot be called directionally honest on the mobility axis — it is the sim registering rounding artifacts, not kiting behavior.
- Round number cleanly above the maximum failing-tick margin (tick=1.0: +1.0m) and well below the minimum passing-tick margin (tick=0.2: +65.45m). No ambiguous cases anywhere in the data.
- Robust to anchor choice: 10% of K4 absolute = 21.7m; 12% of reference separation = 20.6m. Both round to the same floor.

### Classification under the recommended floor

Criterion: margin ≥ +20m AND sign_ok = True AND statistically resolvable (|margin| > 2·pooled_SE).

| Tick | K4 disp (m) | K6 disp (m) | Margin (m) | sign_ok | stat_resolvable | pract_sig (≥20m) | KITE VERDICT |
|---|---|---|---|---|---|---|---|
| 0.1 | 216.83 | 44.85 | +171.98 | YES | YES | YES | **PASS** |
| 0.2 | 315.00 | 249.55 | +65.45 | YES | YES | YES | **PASS** |
| 0.3 | 10.80 | 53.48 | −42.68 | NO | YES | NO | **FAIL** |
| 0.5 | 9.00 | 8.62 | +0.38 | YES | YES | NO | **FAIL** |
| 0.8 | 9.60 | 9.20 | +0.40 | YES | YES | NO | **FAIL** |
| 1.0 | 9.00 | 8.00 | +1.00 | YES | YES | NO | **FAIL** |

The floor cleanly separates the regime where kiting behavior is real (240s fight, continuous movement, >65m separation) from the regime where it has collapsed (short win, both kits nearly static, sub-meter separation).

### Observation on the tick=0.2 data point

At tick=0.2, K4 displacement is *higher* than at tick=0.1 (315m vs 216.83m), with K6 also higher (249.55m vs 44.85m). Both timeout at 240s. The margin drops (65.45m vs 171.98m) but remains strongly above the floor. This is the legitimate kite zone: coarser sampling of a genuinely mobile kiter still records substantial movement at 240s. The proposed floor (20m) passes this with 3× headroom.

---

## Q2 — Seed Count / Power for the Tick=0.3 Zone and Adequate Power Generally

### The tick=0.3 zone is a structural discontinuity, not sampling noise

The critical finding is that tick=0.3 already has **displacement_se=0.0 and clear_time_se=0.0** across 12 seeds. This means the simulation is perfectly deterministic at this tick level: all 12 seeds return identical values. There is no sampling variance to reduce with additional seeds.

The sign-flip at tick=0.3 is caused by a regime transition, not noise:

| | tick=0.1 | tick=0.2 | tick=0.3 | tick=0.5 |
|---|---|---|---|---|
| K4 outcome | timeout (240s) | timeout (240s) | **WIN (51s)** | WIN (43s) |
| K6 outcome | WIN (114s) | timeout (240s) | **WIN (131s)** | WIN (103s) |
| K4 disp | 216.83m | 315.0m | 10.8m | 9.0m |
| K6 disp | 44.85m | 249.55m | 53.48m | 8.62m |

At tick=0.3, K4 kills the boss in 51s (a fast win, not a kiting fight). K4's displacement is 10.8m because the fight only lasts 51s — the kiter doesn't need to kite, it just kills. K6 fights for 131s and racks up 53.48m displacement, making it appear more "mobile" by the displacement metric purely because it fights longer. This is a coarse-navigation artifact that changes the fundamental character of the fight, not a measurement of kite behavior at all.

**More seeds cannot fix this.** The system produces identical results across 12 seeds (SE=0). The 13th seed would give the same values. The instability at tick=0.3 is not sampling variance — it is that the tick size changes the simulation's fight dynamics (navigation overshoots land hits that a finer grid misses, killing the boss before kiting saturates). No N resolves a deterministic structural discontinuity.

### Power at the candidate Pareto configs (tick=0.1, tick=0.2)

At both passing ticks, power is already effectively infinite:

- **tick=0.1:** margin=+171.98m, pooled_SE=0.07m, test-stat=171.98/0.07=2457. Power ≈ 1.0 at any reasonable alpha.
- **tick=0.2:** margin=+65.45m, pooled_SE=0.00m (deterministic). Test-stat = infinity. Power = 1.0.

N=12 is more than sufficient for both candidate Pareto configs. Increasing N provides no additional discrimination power.

### AOE floor power note (§9.2 secondary question, elite_pack adds1)

Elite_pack adds1 (1 add above the inversion): clear_time margin=+0.73s at tick=0.1 (pooled_SE not shown for this cell in the margin-to-noise summary; the §9.1 table reports it as "marginal, resolvable"). This is the thinnest AOE margin in the dataset. However, the spec §5(A) requires the margin survive the reduction in direction, not match commit-grade magnitude. Since clear_time margin is positive and resolvable even at 1 add (while inverting at 0 adds), the pack floor is already empirically located. This cell would benefit from a power check if gamora wants to tighten the margin estimate, but it does not block the Pareto config decision (the Pareto config uses ≥2 adds anyway per §9.1's stated floor).

### Recommendation

**Do not increase N. Exclude tick≥0.3 from the kite-honest region.**

The verdict rests on structural evidence, not statistical ambiguity. The correct action is to note in the Pareto config documentation that tick=0.3 is excluded because of a deterministic fight-regime transition (not noise), and that this transition is an expected consequence of coarse-step navigation altering damage-delivery timing in a single-target long-duration fight.

---

## Synthesis: How the Two Answers Compose

Combining Q1 and Q2:

- **Kite-honest tick range:** {0.1, 0.2}. The floor is set by the raw-magnitude practical-significance criterion (≥20m); the upper bound of this range is tick=0.2 (65.45m margin, 3× above floor). Tick=0.3 is excluded by structural discontinuity, not by insufficient N.
- **AOE-honest pack range:** ≥2 simultaneously-AOE-coverable targets (magic_pack ≥3 mobs, elite_pack ≥2 mobs). Tick-invariant; established independently of the kite analysis.
- **Provisional Pareto rectangle (confirmed by this consult):** tick ∈ {0.1, 0.2}, dense packs at/near full. Cost at tick=0.2, full packs ≈ 0.58 ms/fight (~11× under commit-grade ceiling).
- The Pareto-config *selection* within this rectangle (0.1 vs 0.2) is a cost/margin tradeoff that routes to gamora + gandalf/Matt (see below).

---

## Items that Route to Gandalf / Matt

**ROUTES TO GANDALF/MATT — Item 1:** The practical-significance floor percentage (10% vs 20% vs 25% of reference displacement) is a value judgment about "what counts as directionally honest enough on Axis-1." The analysis shows that any floor between ~17m and ~42m produces the same classification outcome, so the exact number is not statistically load-bearing — but the *floor's existence and minimum value* is a design-level discrimination requirement (§2/§3 territory). Gandalf should ratify the floor (or set a tighter one) as part of the §5 discrimination-floor review.

**ROUTES TO GANDALF/MATT — Item 2:** The tick=0.2 data shows a genuinely odd result — K4's absolute displacement at tick=0.2 (315m) *exceeds* tick=0.1 (216.83m), while the K4−K6 margin is lower (65.45m vs 171.98m). Both kits timeout and rack up displacement across the full 240s, but the coarser grid produces more cumulative path length for both kits. This is not a problem for the kite floor (both values pass the 20m floor with margin), but it means the displacement metric at tick=0.2 is measuring something slightly different from tick=0.1 — higher total path, not higher kite separation. Whether this constitutes a directional-honesty concern for the search gradient is a §2/§3 judgment call, not a statistical one. Flagged for gandalf review before Pareto lock.

**ROUTES TO GAMORA — Item 3:** The Pareto-config choice between tick=0.1 (margin=171.98m, cost=0.887 ms/fight) and tick=0.2 (margin=65.45m, cost=0.583 ms/fight) is a cost-vs-discrimination tradeoff. Both pass the kite floor; tick=0.2 is cheaper (~35% faster per fight). The cost-target quantification (§6: "639 × iterations × rooms × reduced-cost ≤ tolerable inner-loop wall-clock") is gamora's measurement. This consult recommends tick=0.2 is statistically sound for the Pareto candidate, but gamora should confirm the inner-loop wall-clock budget is met.

---

## Knowledge Gaps Not Resolved

- **Arena size** is not reported in the sweep data or spec. An arena-size anchor for the practical-significance floor would be more physically grounded than the commit-grade-reference anchor used here. If arena size is available in the spatial fight engine config, gamora could add it as a reported field in the next sweep for cleaner floor justification.
- **Cause of the tick=0.2 displacement increase** (K4: 315m vs 216.83m at tick=0.1) is not diagnosed from the JSON alone. It is likely that coarser tick steps cause slightly longer path trajectories due to overshoot correction, but this is a mechanistic hypothesis, not a measured fact.
- **elite_pack adds1 pooled_SE** is not reported in the frontier summary (the per-cell JSON has it but the margin-to-noise ratio table only covers magic_pack). This thin margin (+0.73s) should be confirmed resolvable with adequate power if gamora wants a tighter pack-floor bound (though it does not change the Pareto-config recommendation at ≥2 adds).

---

## Source List

1. Gamora sweep math note: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/m1-3-5-reduced-spatial-frontier-sweep-2026-06-14.md` (accessed 2026-06-16)
2. Gandalf acceptance spec: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-14-reduced-spatial-search-substrate-discrimination-floor-acceptance-spec.md` (accessed 2026-06-16)
3. Raw sweep data: `/Users/admin/Games/reincarnated-engine/output/m1-3-5-frontier-sweep-2026-06-14.json` (N=12/cell; accessed 2026-06-16; computed displacement SDs, Cohen's d applicability, regime-transition structural diagnosis from raw values)
