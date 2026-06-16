# Reduced-spatial inner-loop search substrate — discrimination-floor acceptance spec (design contract)

**Type:** design-spec-as-math / acceptance contract (gandalf seam). The search-layer sibling of the commit-grade golden oracle.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 ("do all three" — author the acceptance spec as the design front-end of the reduced-spatial-substrate milestone).
**Status:** forward-spec for an unbuilt, not-yet-sequenced Track-1 milestone. **Graduates to `canonical/story/` (mini-oracle status) when the milestone is ratified + sequenced.** Until then this is the contract gamora builds against — same family as the §4.C/§4.D density design contract.
**Companion docs:**
- `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — the **commit-grade** acceptance authority; this is its **search-grade** sibling.
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` §4.2 (the "reduced-spatial, not 1D" mandate) + §4.3 (the inner loop cannot be 2D).
- `agentic_orchestration/gandalf/notes/2026-06-14-we-close-design-endorse-and-wf-search-substrate-precondition.md` — the finding that named this milestone.
- W-D §6.4 discrimination law ("a measurement is only a measurement if it discriminates") — this spec is that law applied to the **search gradient**.

---

## 0. TL;DR

The W-F 1D-delete strands the balance/recompose inner loop, which runs on 1D today (`balance_loop.py::_primary_recompose_loop` → `search_estimator.simulate_fight`). §4.2 mandates the replacement be **spatially-aware-reduced, never 1D**, because a 1D inner loop hill-climbs every kit toward single-target optima — poison even as a non-gating substrate. §4.3 says the replacement cannot be full-2D (too expensive). The reduced substrate sits between, and this spec is its acceptance authority: **what must "reduced" preserve so the cheaper gradient does not reintroduce the 1D single-target bias in milder form.**

The answer in one line: **the substrate need not be ACCURATE (it is non-gating — commit-grade 2D mints the real verdict on survivors), but it must be DIRECTIONALLY HONEST on the convergence-critical axes — above all the AOE/geometry axis 1D is blind to.** The acceptance test is a discrimination test, not an accuracy test.

---

## 1. The proving question

The inner recompose-first loop adjusts a candidate kit's composition until its win-rate lands in the target band across the room cohort. It runs **639 kits × convergence-iterations × room-cohort** — far too many evaluations for commit-grade 2D (W-E: 6.31 ms/fight × that volume is hours; §4.3 #2 confirms the inner loop cannot be 2D). It therefore needs a cheap evaluator. The question this spec answers: **how cheap can that evaluator get before its search gradient lies about the axis that defines the build?**

## 2. The core principle — directional honesty, not accuracy (the floor)

The 1D engine's sin was **not** imprecision. It was **systematic bias**: blind to AOE, it reads a real pack-clearing AOE kit as an underperforming single-target kit, so the recompose loop "fixes" the underperformance by pushing the kit toward single-target DPS — biasing the whole archive away from AOE identity during convergence (the wave doc's Scenario-3/C1 analysis). The poison is a *gradient that points the wrong way for spatial archetypes.*

So the floor is **not** "match commit-grade win-rates." It is: **no systematic axis-blindness that creates a convergence bias.** The substrate may be noisy, may be absolutely off, may disagree with commit-grade on magnitude — as long as its *ranking gradient on the convergence-critical axes* preserves the kit's identity through convergence. A cheap, noisy, directionally-honest evaluator is sound. A cheap, precise-looking, directionally-biased one (1D) is poison.

This is the discrimination law (W-D §6.4) applied to the search layer: **a search is only a valid search if its gradient discriminates the axes the archetypes live on.**

## 3. Which axes must the reduced gradient preserve (and which may degrade)

Not all 8 axes are convergence-critical. Rank by "does blindness here bias the convergence direction":

| Axis | Convergence-critical? | Floor requirement |
|---|---|---|
| **Geometry (Axis-2)** | **YES — the load-bearing one** | MUST discriminate single-target vs AOE families in the density rooms. This is the axis 1D kills and the one whose blindness caused the bias. Non-negotiable. |
| **Engagement range / mobility (Axis-1)** | **YES** | MUST register kite-survival vs face-tank — convergence pushes melee/ranged composition, and a substrate blind to kiting mis-converges mobile archetypes (the K4-family signal). |
| Proxy (Axis-2A) | PARTIAL | the summoner identity (K5) must not collapse to "does nothing" — a standing population must still register as effective, or the loop strips proxies. Lower priority than geometry but cannot be zero. |
| Defensive (Axis-4) | NO (commit-grade concern) | may degrade — defensive separation is the commit-grade-of-survivors / W-F boss-room job, not a search-direction driver. |
| Resource / Control / Tempo / Variance | NO | may degrade — these refine identity at commit-grade; they do not set the convergence *direction*. |

**Design consequence:** the reduction is allowed to be aggressive on the bottom rows and must be conservative on the top two. The substrate is "cheap everywhere, honest where convergence turns."

## 4. The reduction levers and their discrimination risk (§4.2: "fewer ticks / fewer entities / same geometry")

| Lever | Cheapness gain | Discrimination risk | Floor constraint |
|---|---|---|---|
| **Fewer ticks (coarser `TICK_SIZE`)** | linear — fewer sim steps | coarse ticks smear fast movement → kiting separation and the M1 gather-then-cast repositioning blur → Axis-1 + AOE-setup degrade | tick coarseness must stay fine enough that kite-survival (K4) and gather-then-cast (M1 primitive) still register a signal |
| **Fewer entities (smaller packs)** | linear-ish | smaller packs **compress the AOE-vs-single-target gap** — pack size is exactly what AOE exploits; shrink it too far and K2 (AOE) ≈ K1 (single-target) → **Axis-2 stops discriminating → 1D poison returns** | pack size must stay **above the threshold where K2-radius-AOE's pack-clear advantage over K1 is measurable** in the density rooms |
| **Same geometry (PRESERVED)** | n/a — this is the lever §4.2 says to KEEP | none — geometry preservation is the whole point | non-negotiable: the substrate keeps true 2D geometry; it reduces *cost*, never *dimensionality* |

The trap to name loudly: **"fewer entities" is the lever most likely to silently re-create the 1D failure**, because shrinking packs is exactly how you make AOE and single-target indistinguishable. The reduction must shrink packs only down to the AOE-discrimination floor, not below.

## 5. The acceptance test (pre-registered discrimination floor — the judge of PASS)

The substrate PASSES iff, at its reduced-cost config, the reference kits still discriminate on the convergence-critical axes. Mirrors the oracle's vary-the-lever-confirm-the-bin-moves logic, at the reduced cost:

**(A) AOE floor — the load-bearing assertion.** Run K1 (single-target) and K2 (radius-AOE) through the reduced config in the **density rooms** (`magic_pack`, `elite_pack`). Assert **K2 out-ranks K1 by a margin that survives the reduction.** If the reduced config collapses K2 ≈ K1 in density, AOE-blindness has returned — the substrate has reduced too far. (This is the K2-vs-K1 separation the oracle §5 establishes at commit-grade; the floor is that the *direction* survives reduction, not the magnitude.)

**(B) Kite floor.** Run a K4-family (mobile-farmer) kit; assert its kite-survival signal (Axis-1) still registers vs a face-tank reference. If the reduction flattens the kiter, ticks are too coarse.

**(B.1) Practical-significance displacement floor (§2/§3 amendment — ratified 2026-06-16, post-legolas-consult).** The static resolvability test (|margin| > 2·SE) is NECESSARY BUT NOT SUFFICIENT for the kite floor, because the cells are deterministic (SE=0 at tick≥0.2) and a sub-meter margin passes the resolvability test while being practically dead. A directional-honesty floor on raw displacement is therefore a §2/§3 design requirement, not a statistical default. **The ratified floor: the signed K4−K6 displacement margin must be ≥ 20 m (raw meters) AND sign-correct (K4 > K6).** Anchor: ≈10% of commit-grade K4 absolute displacement (216.83 m) ≈ 12% of the commit-grade K4−K6 reference separation (171.98 m); any floor in the 10–20% band gives the identical classification (the gap between the passing and failing ticks is a cliff, not a slope — legolas consult §Q1). A margin below ~10% of the reference kiting extent is the sim registering navigation rounding, not kiting behavior. Under this floor: tick 0.1 (+172 m) PASS, tick 0.2 (+65 m) PASS, tick 0.3 (−43 m) FAIL on sign, tick≥0.5 (sub-meter) FAIL. **Kite-honest tick region = {0.1, 0.2}.**

**(B.2) tick=0.2 directional-honesty ruling (the load-bearing call — 2026-06-16).** The legolas consult flagged that at tick=0.2 K4's *absolute* displacement (315 m) EXCEEDS tick=0.1's (216.83 m) while the *margin* shrinks (65 m vs 172 m), raising whether the coarser grid measures a different physical quantity (longer total path under coarse navigation, not larger genuine kite separation). **Ruling: tick=0.2 is DIRECTIONALLY HONEST.** The reasoning is regime-identity, not magnitude: at BOTH tick 0.1 and tick 0.2, K4 AND K6 timeout at the full 240 s — the same fight regime (continuous kiting against one persistent hard target). The path-length inflation (315 m) is a coarse-navigation artifact that lifts BOTH kits' absolute path symmetrically (K6 also rises, 44.85 → 249.55 m); it does NOT corrupt the SIGN or the RANK. §2 requires the *ranking gradient on the convergence-critical axis to preserve kit identity through convergence* — explicitly NOT magnitude fidelity ("may be absolutely off … as long as its ranking gradient preserves the kit's identity"). At tick=0.2 the kite archetype still ranks above the face-tank with 3× headroom over the floor. The regime BREAK is at tick=0.3, where K4 stops kiting and wins in 51 s (a fight-character flip, confirmed deterministic SE=0 — not noise no N can fix). The kite-honest boundary is the regime boundary, which lies between 0.2 and 0.3. Therefore tick=0.2 is inside the honest region; gamora selects 0.1 vs 0.2 on cost (tick=0.2 is ~35% cheaper at 0.583 vs 0.887 ms/fight). **Guard for gamora's eventual report: this honesty holds for the SEARCH gradient (rank-correctness is all the non-gating substrate needs); the absolute displacement number at tick=0.2 must NOT be cited as a kite-separation magnitude downstream — it is path length, not separation. Commit-grade 2D mints any magnitude verdict on survivors.**

**(C) Proxy non-collapse.** Run K5 (summoner); assert the standing-population effectiveness does not read as zero. (Lower bar — "not zero," not "fully discriminated.")

**(D) Convergence-direction regression (the real proof).** The above are static probes; the decisive test is dynamic: **run the recompose loop on a known AOE archetype using the reduced substrate, and confirm convergence does NOT drift the kit toward single-target composition** (the 1D failure mode, reproduced as the negative control). If a 1D-substrate run drifts it and the reduced-substrate run holds it, the substrate has earned its purpose. This is the with/without ablation pattern (cf. the M1 gather ablation, oracle §5.2) — prove the *mechanism*, not just the *threshold*.

**Sweep to find the frontier (methodology hotspot — OP §4.2):** do NOT pre-guess the tick/pack reduction. Sweep tick-coarseness and pack-size DOWN from commit-grade until test (A)/(B) first fails; the **coarsest config that still passes** is the Pareto-optimal substrate. Set the reduction levers EMPIRICALLY from this frontier after the first sweep, the same discipline the density contract applies to the steady-state window. **Methodology consultation (legolas Mode A) fires AFTER the first sweep's signal-to-noise lands, per the Discipline #18 extension-hotspot refinement — not before.**

## 6. The cost target

- **Ceiling (must beat):** commit-grade 6.31 ms/fight (W-E datum) — the substrate exists *because* the inner loop can't pay this × 639 × iterations.
- **Floor (the thing it replaces):** the 1D `search_estimator` per-fight cost — the substrate should approach 1D's cheapness while being spatially honest. (gamora has the 1D per-fight cost and the convergence-iteration count from `balance_loop.py`; the cost target is "639 × iterations × rooms × reduced-cost ≤ tolerable inner-loop wall-clock" — gamora quantifies; this spec sets the *discrimination requirement*, not the cost number.)
- The reduced substrate's value is realized only if it lands materially below the ceiling **while passing §5** — cheapness bought by failing the discrimination floor is the 1D trap re-bought.

## 7. Genre/design anchor

Every ARPG balance pipeline faces this: you cannot run full-fidelity simulation on every candidate during search, so you use a cheaper proxy — but the proxy must not lie about the thing that defines the build. The 1D engine's specific sin was using the **range scalar** as the proxy, blind to the AOE axis that defines half the genre's archetypes (D2 Sorceress Frozen Orb vs single-target; PoE clear-speed AOE builds vs single-target bossers; the entire "mapper vs bosser" split). A search proxy that can't tell a pack-clearer from a single-target DPS will, over many candidates, homogenize the archive toward whichever it can see — exactly the form-bias failure mode (doc 37) in a new guise. The discrimination floor is the structural guard against re-importing it through the back door of the search loop.

## 8. Disposition

- This is the **design front-end** of the **reduced-spatial inner-loop search substrate** milestone (Track-1, slots between M1.3 axis-closures and M1.4 W-F; a hard W-F precondition per the W-E-close finding).
- **gamora builds against §5** (the acceptance test) and **§4** (the lever constraints); **gandalf owns §2/§3/§5** (the discrimination floor); the cost-target number (§6) is gamora-measured.
- **Sequencing:** KR sequences the milestone into a batch before W-F. When ratified + sequenced, this spec graduates to `canonical/story/` as the search-grade mini-oracle.
- **Not built here.** This is the contract; the build is the milestone.

---

**Signed:** gandalf, 2026-06-14 (§5 amended 2026-06-16: B.1 displacement floor ≥20 m ratified + B.2 tick=0.2 ruled directionally honest → kite-honest region {0.1, 0.2}, post-legolas-consult)
**For:** the discrimination-floor acceptance spec for the reduced-spatial inner-loop search substrate — the search-layer sibling of the commit oracle. The substrate must be directionally honest (not accurate) on the convergence-critical axes, above all geometry; "fewer entities" is the lever most apt to re-create the 1D single-target bias and must shrink packs only to the AOE-discrimination floor; the acceptance test is a with/without convergence-drift ablation, not an accuracy match.
