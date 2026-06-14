# M1.3.5 discrimination-floor methodology ruling — the Pareto-config lock settings

**Type:** methodology ruling (gandalf seam) — the grounded §5 methodology for the reduced-spatial search-substrate, synthesizing the Discipline-#18 extension-hotspot consult that fired on gamora's first-sweep signal.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 (the M1.3.5 milestone + its acceptance spec, "do all three").
**Empirical grounding:** gamora's M1.3.5 first frontier sweep (engine `42e40e4`) + the legolas Mode A methodology consult (`agentic_orchestration/legolas/research/2026-06-14-m135-discrimination-floor-methodology.md`, fired per the Disc #18 timing refinement once the first sweep's signal-to-noise landed).
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-14-reduced-spatial-search-substrate-discrimination-floor-acceptance-spec.md` — the acceptance contract this grounds (§5 the discrimination floor). When M1.3.5 graduates to `canonical/story/`, this ruling folds into §5.
- `agentic_orchestration/legolas/research/2026-06-14-m135-discrimination-floor-methodology.md` — the consult memo (all three priors confirmed).

---

## 0. TL;DR — three Pareto-lock settings ruled (all three priors confirmed by external practice)

1. **Kite floor (Q1):** PASS requires **two separate gates** — `(margin > MDE) AND (margin > 2·SE)`. The MDE is a **design call I own, not a statistics output**: it is the displacement that converts ≥1 attack from **hit → miss** against the reference monster. Sub-MDE margins FAIL even when statistically real. In the noisy tick=0.3 zone: Common Random Numbers + CI-width ≤ MDE/2 stopping.
2. **AOE floor (Q2):** lock the dense-room floor at **≥2 coverable targets**, not 1. Verify the 2-add AOE margin satisfies `margin ≥ 2·SE` *at 2-add specifically* (SNR≥3 ideal) before locking — not just the overall clear-time SNR.
3. **Discrimination coordinate (Q3):** clear-time primary + aoe-hits witness — confirmed. **Name + control the DPS confound:** K1/K2 must be **DPS-matched at the single-target level** so the density-room clear-time delta isolates geometry, not raw DPS. This is the discrimination law applied to the instrument itself.

The substrate is **affordable at the discrimination-safe config** (gamora: ~0.58 ms/fight at tick=0.2/full-packs, ~11× under the commit-grade ceiling), so cost is not the binding constraint — the only open question is test (D), the convergence-drift ablation.

---

## 1. The consult disposition

The legolas Mode A consult confirmed **all three of my stated design-priors** against established discrete-event-simulation / Monte-Carlo / A-B-testing / game-balance practice. This is the Disc #18 refinement working exactly as intended: the consult fired *after* the first sweep's signal-to-noise landed (not before), so it grounded the *extension* methodology against real signal rather than in the dark. The memo's precision-additions (below) sharpen each ruling; none overturn a prior. I hold the design calls; legolas grounded the statistical methodology.

## 2. Ruling Q1 — the kite floor (MDE is a design call, not a noise threshold)

**Confirmed practice:** practical significance and statistical significance are *orthogonal* gates. The minimum-detectable-effect (MDE) is set *before* data collection, anchored to the minimum decision-relevant effect — **never derived from the noise level**. Statistical significance says the effect is real; MDE says it is large enough to matter.

**The ruling.** The kite floor's gate structure is, verbatim:
```
PASS if (margin > MDE_kite) AND (margin > 2·SE)
```
both gates emitted separately so it is visible which is binding. **The MDE is mine to set, and I set it on player-perceptible physics, not on an abstract meter value:**

> **MDE_kite = the displacement margin that converts at least one attack from a HIT into a MISS against the reference monster** — computed from the engine's monster attack-range + the relative (kiter − monster) move-speed over one attack windup.

A +0.4–1.0 m displacement edge that clears 2·SE but does not move the kiter out of the monster's reach is "statistically real, practically dead" — it is not kiting, it is jitter. Kiting *is* the act of moving out of reach to turn a hit into a miss; the floor must measure that, not sub-reach wobble. gamora computes the exact meter value from the engine params (she has monster attack-range + move-speeds); the **design principle** is the hit→miss conversion, not the number.

**Threshold-zone stabilization (tick=0.3):** Common Random Numbers (same seed sequence across the compared configs) to strip between-seed variance from the comparison — standard for *all* archetype comparisons in this substrate, not just the kite floor. Target CI-width ≤ MDE/2 as the seed-count stopping criterion (~5–10× the stable-zone baseline seeds in the noisy zone). Antithetic variates if the fight RNG is accessible.

## 3. Ruling Q2 — the AOE floor (≥2 adds, with the 2·SE-at-2-add verification)

**Confirmed practice:** operating at/near a crossover is noise-dominated; require the observed margin ≥ 2× the noise amplitude (SE of the margin) *above* crossover before treating a config as a reliable discriminator; game-balance practice cites SNR ≥ 3 on the discrimination coordinate as the "robust" floor.

**The ruling.** Lock the dense-room AOE floor at **≥2 coverable targets**, not the 1-add thin pass. My design reason (confirmed): a +0.7 s margin "passing only thinly" at 1 add is the razor's-edge that load drift — machine variance, pack-spawn variance, tick order-of-operations — pushes below zero, **silently reinstating the single-target bias the substrate exists to prevent.** Operating at the crossover reintroduces the 1D poison *probabilistically*. **Verification gate before lock (legolas's refinement, adopted):** confirm the 2-add AOE-comparison margin satisfies `margin ≥ 2·SE` *at 2-add specifically* (ideally SNR≥3) — do not borrow the 24.85 overall clear-time SNR as a proxy for the AOE margin at 2-add.

## 4. Ruling Q3 — clear-time primary + the DPS confound (the discrimination law at the instrument)

**Confirmed practice:** "discriminate on the non-saturating continuous coordinate" is the correct formalization — a saturated output has zero d′ (signal-detection theory). clear-time is the standard discrimination coordinate precisely when win-rate / kill-fraction saturate (both kits fully clear). The two-coordinate structure (clear-time primary + AOE-hit-count *witness*) is standard: the witness confirms the *mechanism*, it does not replace the *signal*.

**The load-bearing pitfall — and the design ruling it forces.** clear-time = *f*(raw DPS, geometry efficiency). If K1 (single-target) and K2 (radius-AOE) differ in raw DPS, then "K2 clears the pack faster" is *partially* a DPS win, not a geometry win — **and a clear-time coordinate confounded with DPS is the flat-scalar trap in a new costume.** This is the same lesson as the whole cert wave and form-bias (doc 37): the measurement coordinate must discriminate the *target axis* (geometry), not a *confound* (DPS). The discrimination law applies to the reference *instrument*, not only to the engine under test.

**The ruling:** the K1/K2 reference pair must be **DPS-matched at the single-target level** — equal expected single-target DPS *before* the AOE multiplier — so the density-room clear-time delta is attributable to geometry alone. gamora verifies K1/K2 are DPS-matched; if they are not, hold them within a ±tolerance band and lean on the aoe-hits witness to deconfound (the reduced-cost-appropriate mitigation legolas confirms). **Document the DPS confound explicitly** in the substrate's methodology notes — it is a permanent property of a clear-time coordinate, not a one-time check.

## 5. What gamora does next (unblocked)

With §2–§4 locked:
1. **Lock the Pareto config** at the discrimination-safe corner (tick ∈ [0.1, 0.2], dense packs ≥2), applying the Q1 two-gate kite test, the Q2 ≥2-add AOE floor + 2·SE-at-2-add verification, and the Q3 DPS-matched K1/K2 + clear-time/aoe-hits coordinates.
2. **Run the §5(D) convergence-drift ablation** — the decisive proof: the recompose loop on a known-AOE archetype using the locked reduced substrate must **NOT** drift the kit toward single-target composition (the 1D failure, run as the negative control: a 1D-substrate run *should* drift it; the reduced-substrate run *should* hold it). Prove the mechanism, not just the threshold.
3. **Route:** jack-ryan Gate-2 + gandalf §2/§3/§5 review on the locked config + the ablation result.

## 6. Disposition

- **Three Pareto-lock settings RULED** (§2 kite MDE = hit→miss displacement + two-gate; §3 ≥2-add AOE floor + 2·SE verification; §4 clear-time + DPS-matched K1/K2 + confound named). All three confirm the priors; the consult sharpened, did not overturn.
- **gamora unblocked** for Pareto-config lock → test (D) ablation. Cost is non-binding (~11× headroom); test (D) is the open question.
- **This ruling folds into the acceptance spec §5** when M1.3.5 graduates to `canonical/story/`.
- The §2 CRN discipline applies substrate-wide (all archetype comparisons), not only to the kite floor.

---

**Signed:** gandalf, 2026-06-14
**For:** the M1.3.5 discrimination-floor methodology ruling — the three Pareto-config-lock settings grounded by the Disc-#18 extension-hotspot consult: the kite floor's MDE is the player-perceptible hit→miss displacement (a design call, gated separately from statistical significance); the dense-room AOE floor locks at ≥2 coverable targets with a 2·SE-at-2-add verification (a thin pass is the razor's-edge that reinstates the 1D single-target poison); and the clear-time discrimination coordinate must be deconfounded from raw DPS by DPS-matching the K1/K2 reference pair — the discrimination law applied to the instrument, the same flat-scalar lesson the cert wave exists to retire.
