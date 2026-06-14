# W-E close — gandalf design-endorse + the W-F search-substrate precondition (the inner-loop gap)

**Type:** critique-pair deliverable (gandalf design half of the W-E close) + a design-coherence finding that gates W-F.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 ("Yes, open the W-E close").
**Critique pair:** jack-ryan Gate-2 (sub-agent finding, this session) + **this** gandalf design-endorse + Matt ratify.
**Artifact under review:** gamora W-E throughput proof, engine commit `02e2a6f` (`simulation/math/we-throughput-proof-2026-06-13.md` + `output/we-throughput-proof-2026-06-13.json` + `scripts/gamora_we_throughput_proof_2026_06_13.py`).
**Acceptance authority:** `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` + `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` §4.2/§4.3/§5.

---

## 0. TL;DR

1. **W-E close: ENDORSE (design half).** The build is a clean, honest measurement that banks the §4.3 #2 datum the W-F 1D-delete decision needs. The arithmetic reproduces from the JSON; the acceptance criterion + FAIL branch were pre-registered; scope is measurement-only (no engine-behavior change). Design significance below.
2. **jack-ryan Gate-2: WARN→PASS, two doc-only fixes** (within his ADR-002 doc-only authority; neither gates the close). WARN-1: the "boss-weighted 6.31 ms/fight" headline is actually the flat per-room mean (the boss tail IS correctly weighted in the unit/batch sums, which are the numbers that gate). WARN-2: the harness times the *fight* (`run_spatial_fight`) but not the 8-axis *reduction* (`measure_kit_spatial`→`mint_commit_grade_verdict`) that mints the verdict — so the commit-grade bound is a lower bound (sim half only). Large headroom (~440×) makes the gate robust regardless.
3. **The design-coherence finding (this note's load-bearing content) — a W-F precondition W-E did NOT discharge:** W-E measured the **commit** path. The W-F 1D-delete strands the **search** path. The balance/recompose inner loop runs on 1D **today** (`balance_loop.py::_primary_recompose_loop` → `simulate_fight` from `search_estimator`); the spatially-aware-reduced replacement §4.2 mandates **does not exist** (grep-confirmed — only forward-references); and §4.3 #2 establishes the inner loop **cannot** be full-2D. So **W-F's delete is gated on building + throughput-proving the reduced-spatial inner-loop substrate** — otherwise the delete strands the recompose loop with no evaluator, the exact "zero working combat engines" failure §4.2 was written to prevent.

This finding does **NOT** block the W-E close. W-E's scope was the commit-grade-of-survivors datum; it nailed it. The finding reshapes **W-F**.

---

## 1. The design-endorse (why W-E matters beyond a budget gate)

The 2D spatial engine exists because the 1D range-scalar engine **cannot discriminate the spatial axes the class fantasies live on** — a kiting hunter, a blood-mage controller, a face-tank are spatially-defined archetypes the 1D engine flattens to a single range scalar. That is the design case for making the spatial engine the sole COMMIT-grade authority (oracle §6.2; the discrimination law "a measurement is only a measurement if it discriminates," W-D §6.4).

Until W-E, the 1D engine retained **one** justification the fidelity argument couldn't touch: it was cheap. W-E removes it. The commit-grade-of-survivors batch is **~11 s** (34 survivors × 54 fights), **0.07 %** of the 1D ~5-hr reference, **~54×** cheaper per fight than the 1D basis the budget projection was built on (`gauntlet_sim.py:1388`). The blind authority is now **slower-per-decision AND blind**, vs the discriminating authority being **decisive AND affordable**. The design case for retiring 1D (archetype-fidelity + cost) is, at the commit layer, **complete**. That is what W-E earns. Endorse.

## 2. Why 1D must DIE in every branch, not demote to search-only (the discrimination law at the search layer)

§4.2's load-bearing design point, in my register: the reason 1D cannot survive even as a *non-gating* search substrate is the discrimination law applied to the **search gradient**. A cheap evaluator blind to AOE does not merely lose precision — it **hill-climbs every kit toward single-target optima during convergence** (the wave doc's Scenario-3/C1 analysis). The gradient points the *wrong way* for spatial archetypes. "A measurement is only a measurement if it discriminates" has a search-layer twin: **a search is only a valid search if its gradient discriminates the axes the archetypes live on.** A 1D inner loop would silently re-bias the whole archive toward single-target builds — poison even when it never mints a verdict. So the §4.2 mandate (replace 1D with reduced-*spatial*, never keep 1D) is not fastidiousness; it is the same law that justifies the whole wave. I amplify it, I do not dissent from it.

## 3. The finding in full — the inner-loop gap (empirically grounded, Disc #11)

**Verified, not assumed:**

| Claim | Evidence |
|---|---|
| Inner recompose loop evaluates on 1D today | `simulation/__init__.py:5` `from .search_estimator import simulate_fight`; `balance_loop.py:1680` `_primary_recompose_loop`, `:908` `_make_recompose_gauntlet` |
| Spatial engine is NOT wired into the balance inner loop | grep `spatial_engine|run_spatial_fight|measure_kit_spatial` in `balance*.py`/`*recompose*` → **empty**; spatial appears only in the gauntlet/commit path |
| Reduced-spatial substrate does NOT exist | grep `reduced.spatial|spatial.reduced|spatial.search|fast_spatial` across `simulation/` → only gamora's own forward-reference ("1D-now / spatial-reduced-**future** per §4.2"); no implementation |
| Inner loop cannot be full-2D | wave doc §4.3 #2: "this datum already *confirms* the inner loop cannot be 2D — hence a non-gating search substrate survives per §4.2" |
| Deletion surface | 16 `search_estimator` callsites across `src/reincarnated/` |

**The internal tension this surfaces in the wave doc (named, for the W-F gate):** §4.2 branch-1 says "if commit-grade affordable [W-E ✓] → 1D has zero remaining function → delete it." But §4.3 #2 says the same datum *confirms the inner loop cannot be 2D*. Both true ⇒ even in the affordable branch, the inner loop still needs a **non-1D** search substrate — which §4.2 itself says must be reduced-spatial. So **"1D has zero remaining function" is aspirational, not current**: it becomes true only *after* the reduced-spatial inner-loop substrate replaces 1D in `balance_loop.py`. Today, 1D has a very active function — it is the only inner-loop evaluator that exists.

**Therefore the W-F row needs a precondition it does not currently carry.** The wave doc §5 W-F row reads: *"Delete the 1D engine + callsites; re-validate the defensive bridge commit-grade in the boss room."* It is silent on the inner-loop replacement. **Recommendation (recommend, do not unilaterally rescope):** W-F (or a W-E.5 inserted before it) must additionally **build + throughput-prove the spatially-aware-reduced inner-loop search substrate**, because deleting 1D removes the current `_primary_recompose_loop` evaluator and §4.2 forbids 1D as its substitute. Route to KR (sequencing) + Matt (ratify the W-F scope expansion).

**Why this matters / the player-and-project consequence:** the entire wave was authored to stop the team from "wasting weeks or months AGAIN" by pairing canonical docs the wrong way (Matt, §0 verbatim). Deleting 1D before its reduced-spatial replacement is built would strand `balance_loop.py` with zero inner-loop engines — the *exact* failure mode the wave exists to prevent, re-introduced by its own final step if the clean 54× commit-path headline is allowed to carry W-F past the unmeasured search path. This is implicit-pillar drift (Discipline #13) caught one gate early.

## 4. How the two critique-pair halves compose

jack-ryan caught that the **commit** path's *reduction* cost is untimed (a gap *within* the commit path; small; doc-deferrable, likely folded into W-F's commit-grade re-validation). gandalf caught that the entire **search** path is *unbuilt* (a structural gap; a hard W-F precondition). Two independent witnesses, two layers, one convergent conclusion: **W-E measured a subset of what the post-1D-delete architecture runs; the W-F gate's full throughput story is not yet told.** Neither blocks the W-E close (its scope was exactly the subset it measured, measured cleanly). Both are W-F preconditions.

## 5. Disposition

- **W-E close design half: ENDORSE.** Pairs with jack-ryan Gate-2 WARN→PASS. Ready for Matt ratify.
- **Two jack-ryan doc-lines → gamora** (rename the per-fight headline off "boss-weighted"; scope the proof as fight-execution-cost-only + note the reduction is unmeasured-but-sub-dominant). Within jack-ryan's doc-only authority; async; do not gate the close.
- **W-F precondition (this note §3) → KR + Matt.** Add to the W-F gate (or insert W-E.5): build + throughput-prove the reduced-spatial inner-loop substrate before the 1D-delete. Track explicitly so the 54× headline does not carry the delete past it.
- **W-F unchanged otherwise:** still owes cond.5 (defensive-bridge boss-room re-validation) + §6.4 final discrimination-accounting close.

---

**Signed:** gandalf, 2026-06-14
**For:** the design half of the W-E close (ENDORSE — W-E removes the cost justification for the blind 1D authority, completing the retirement case at the commit layer) + the load-bearing W-F precondition the commit-path proof did not discharge: the reduced-spatial inner-loop search substrate that 1D's deletion strands is unbuilt today, and W-F cannot cross the 1D-delete until it is built + throughput-proven.
