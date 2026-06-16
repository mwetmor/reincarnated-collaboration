# Autonomous-run review + completion-frontier audit (gandalf, Pattern B for Matt)

**Date:** 2026-06-16
**Author:** gandalf
**Mode:** Pattern B — Matt-commissioned review of KR's 2026-06-16 autonomous run, verified against disk/code, with independent re-think of the engine docs.
**Commission (Matt, verbatim substance):** review everything KR did in the autonomous run; compare against the planned run AND against what's left toward (a) completed combat sim and (b) completed end-to-end engine pipeline; review per my notes; ultra-think the engine docs; **"do not take anything written as truth."**
**Discipline applied:** every load-bearing claim below was verified against git/disk/code, not against prose summaries. Where I report a status, I name the artifact I checked.

---

## 0. Headline — the inversion

KR's run was **disciplined and faithful**. No destructive deletion fired. No scope was invented. No design call was promoted to a decision. Every additive item with a reachable acceptance criterion cleared the two-witness gate; every Tier-2 deletion correctly parked.

**The artifact that most failed the "don't take it as truth" test was my own charter** (`canonical/story/2026-06-16-engine-state-and-autonomous-run-plan.md`), stale on three counts. KR's reconcile-against-disk discipline caught my staleness and corrected it mid-run. That inversion is the first thing Matt should hear: I sent KR in with a partly-wrong map, and he redrew it correctly rather than marching off the edge.

A second, compounding finding (mine, this review): the charter's blocker lists **also omitted** three engine-track items that live in ground-state §5.1. KR can't be faulted for not working items absent from the lists he was given — but it means the charter was both *stale* (wrong on 3) and *incomplete* (silent on 3). More below (§5).

---

## 1. Plan-vs-actual — VERIFIED

| Charter intent | Actual | Verified by |
|---|---|---|
| 4 waves, park-and-advance | All 4 processed; trunk never halted | RETURN-PACKAGE run-log + wave-close docs |
| Additive items clear full gates | Wave 1 (D6 loader, W-D export, i-frame dodge, telegraph-3); Wave 1.5 (M1.3.5 substrate); Wave 2 (keystone contract + gear materialization + node-wire); Wave 4 (companion-gen + D4 proxy-port) — all PASS/PASS-WITH-INFO + gandalf endorse | git log `eeacbec`/`a362953`/`0fa3c66`/`68af6b9` + per-wave close docs |
| Tier-2 deletions fire only on clean criterion | Both PARKED — 1D `search_estimator` + b6 both gated on real-loadout re-measurement | §2 below (disk check) |
| No Matt surface on gate grounds | None forced; open items are design calls + parked preconditions | RETURN-PACKAGE §2 |

The plan's *shape* held. What changed was the plan's *premises* — see §3-4.

---

## 2. Deletion-safety + scope-discipline — VERIFIED ON DISK

- `simulation/search_estimator.py` — **EXISTS.** 1D estimator not deleted. ✔
- `generation/b6_archetype_templates.py` + `b6_kit_builder.py` — **EXIST.** b6 not retired. ✔
- `generation/companion_generation.py` — **bounded/synthetic confirmed:** docstring "NOT a production corpus"; `MIN_COMPANION_SEASON=2`; `is_synthetic=True`; `_SYNTHETIC_HALL` pool; `ValueError` season-1 refusal guard. ✔
- M1.3.5 (`m1-3-5-reduced-substrate-build-2026-06-16.md`) — **flag-gated OFF** (`REDUCED_SUBSTRATE_TICK_SIZE=0.2` distinct from legacy `REDUCED_TICK_SIZE=0.5`); production byte-identical; 1D not deleted; halted at Gate-2; §8.2 ablation PASS (1D drift 1.0, reduced drift 0.0). ✔
- D5 reference-kit — commit `7fd8792` dated 2026-06-13, **pre-dates the run** → genuinely "already done," not run-work. ✔

Scope discipline was clean. The three Tier-2/Tier-3 boundaries the charter drew were all respected.

---

## 3. The three charter reconciliations — ALL TRUE (I was the stale one)

1. **W-E throughput "NOT started — critical path" (charter) → actually CLOSED pre-run.** Verified against my OWN note `2026-06-14-we-close-design-endorse-and-wf-search-substrate-precondition.md` (W-E CLOSED + Matt-ratified "Do all three" 2026-06-14) and jack-ryan's Gate-2 finding `2026-06-14-gamora-we-throughput-proof-gate2.md`. My charter contradicted my own work from two days prior.
2. **The genuine 1D-delete precondition was M1.3.5, which the charter omitted from the W-F trigger.** M1.3.5 (reduced-spatial search substrate) is the real precondition — deleting 1D strands the recompose loop unless a spatially-aware-reduced replacement exists (else doc-37 form-bias poison re-enters). Cert-wave doc line 151 confirms: "Does not delete 1D before W-F. Immediate deletion strands the pipeline." KR built it (substrate + Gate-2 PASS). **Not invented scope** — pre-authorized, load-bearing, doubly-confirmed.
3. **D5 "READY, not picked up" (charter) → already done** (`7fd8792`). Confirmed above.

All three reconciliations are correct. KR distrusted the prose (my charter) and trusted the disk. That is exactly the discipline the run was supposed to embody.

---

## 4. The optimism-compression correction (load-bearing dissent)

The RETURN-PACKAGE frames the frontier as **"ONE design call: §6 set-bonus magnitude"** with named execution dependencies (keystone integration, F1 fix). I want to be fair: KR did NOT claim §6 is literally the only thing left — he named the keystone-integration and F1-fix dependencies explicitly. The framing is "the design-DECISION frontier converges to §6."

**Where I push back:** "convergent" compresses two things it shouldn't.

1. **cond.5 is a genuine pass/fail, not a foregone pass.** After §6 → keystone integration → real loadouts exist → cond.5 (spatial defensive-bridge boss re-validation) runs. But it must **run AND PASS.** The keystone (kits measured at full power with real defensive set bonuses) makes a pass *more likely* — that's the design intent — but it is a prediction, not a certainty. If cond.5 fails on real loadouts, **1D deletion does not fire and W-F does not close.** That is a second decision point hiding behind §6, not a downstream formality.
2. **Option 1 / b6 may not resolve cleanly.** If the envelope does NOT hit b6-parity on real loadouts, the accept-vs-investigate fork is a live Matt decision — a third decision point.
3. **F1 geometry-blindness fix has its own Matt-gated dimension.** It's a production semantic shift (degraded keyword heuristic → correct geometry read) with a **balance-outcome** dimension. It's not downstream of §6 — it's a parallel W-F-adoption precondition that needs its own re-measure + ratification.

**Net:** §6 is the **next** gate, not the **last**. Behind it sit at least three more genuine decision points (cond.5 pass/fail → maybe reopen b6; b6 accept-vs-investigate fork; F1 production-shift ratification) plus real execution (keystone integration + its validating Gate-2 re-measure; F1 fix; D4 flag-flip; real-Hall population). The frontier is *near* but not *singular*.

---

## 5. The two completion bars — answering Matt's two-part question directly

Matt asked about two distinct things. They have two distinct completion bars, and conflating them is where the "we're almost done" feeling overshoots.

### Bar 1 — "Completed combat sim" (spatial commit-grade engine certified): **CLOSE**
Gated on: §6 ruling → keystone live-integration → cond.5 **PASS** + 1D deletion + §6.4 close; with F1 fix as a parallel precondition. This is the convergent frontier the RETURN-PACKAGE describes. Accurate that it's near. The genuine risk is cond.5 (could fail on real loadouts) and F1 (real production semantic shift needing balance ratification). Everything else here is built or one gate away.

### Bar 2 — "Completed end-to-end engine pipeline" (gen → balance → name → export → UE): **FURTHER OUT**
A real long tail beyond Bar 1, partly enumerated, partly omitted from the charter:

| Pipeline-tail item | Build state (disk-verified) | Bar |
|---|---|---|
| **Export → UE packet** (§7 UE-fit clause) | `export/` exists (`season_exporter.py`, `cycle14_wave5_emitter.py`, `kit_space_emitter.py`, `arena_scenario_emitter.py`) but **ZERO** `ue_packet`/`unreal` refs. UE-shaped packet NOT built; forward item gated on PC-seam-named requirements. | Bar 2 only |
| **Enemy elemental distribution** (gauntlet guarantees all 7 damage types so immunity-T4s testable) | **NOT built.** The damage_resolver.py hit is immunity-coverage *commentary* (line 334, "2/7 damage types ~29% coverage"), not a coverage-guarantee algorithm. Ground-state says "does not block Phase 3/4" — real gap, non-blocking for combat-sim cert. | Bar 2 (testability) |
| **T4-aware gear equipping** (kit construction reads T4 strategy → derives gear priorities) | **NOT built** as a named algorithm (zero grep hits). Partial overlap with keystone gear materialization's carry-forward note (b) T4-variant coherence, but the full feature is open. | Bar 2 (partial Bar 1 overlap) |
| **Real-Hall companion population** | companion-gen used SYNTHETIC Hall; real source needs cross-season persistence + my Hall-as-ally player-journey authoring (my seam). | Bar 2 |
| **D6's 13 unmasked test failures** | Family A b6-generator ×5; Family B element-naming ×8 — each a product-bug-vs-stale-test judgment. | Bar 1/2 hygiene |
| **Phase-5 LLM naming cost-scaling at 400 kits** | gamora-flagged; only LLM-scaling surface in the season pipeline; star-lord surface. | Bar 2 |

**Correction to ground-state §5.1 (stale at its 2026-06-12 refresh):** of its three "NOT STARTED" engine items, the **thin parallel runner is already built** — `BatchGauntletRunner` + `ProcessPoolExecutor` across kits exists in `gauntlet_modes.py` (W0.9.4 Mitigation 2, `MAX_PARALLEL_WORKERS=4`); and its surrogate-search half (M1.3.5) was just built by this run. So that item is substantially landed, not open. The other two (enemy elemental distribution, T4-aware gear) are genuinely open — and were absent from the charter's blocker lists. The parallel runner was always a throughput optimization, never a combat-sim correctness blocker.

---

## 6. My-seam parking-lot items (correctly mine, correctly parked)

- **Real-Hall companion population + Hall-as-ally player-journey authoring** — mine per companion-gen commitment §8. The **synthetic-Hall watch-flag holds the line at wire-in**: synthetic Hall must NEVER leak to production. The season-2 absence→arrival beat collapses if a companion reads as a roster-pick rather than *the* specific self the player lived. Module is explicit it won't (`is_synthetic` + JC-1 park); I hold the line at adoption.
- **D6 canon-placement** — the live-authority grouping-layer-vocabulary doc filed under `historical/` with `STATUS:HISTORICAL-INFORMATIVE` may be mis-filed; my canon seam.
- **Keystone integration carry-forward order** (mine): (a) Matt's §6 ruling FIRST; (b) T4-variant coherence (gear-attuned T4 == alteration-firing T4 at live measurement); (c) JC-3 (count all 11 slots even for 2H — resolved in-lane); (d) empirical re-measure as the gate validating JC-2 + contract §8 predictions.

---

## 7. Empirical criteria for the deferred work (per OP §3.4 — evidence, not time-passage)

- **§6 set-bonus magnitude:** Matt's design call. Content of the decision = the band-ceiling tradeoff (6a generated-kit-aligned vs 6b fixed-reference). My lean: 6b-for-keystone (a stable measurement reference), 6a-as-shipped (player-facing). Magnitude is Matt's.
- **1D deletion fires** iff cond.5 RUNS **and PASSES** on REAL loadouts (not stopgap). The pass is the gate, not the run.
- **b6 deletion fires** iff Option 1 envelope hits b6-parity on REAL loadouts; else the accept-vs-investigate fork is Matt's.
- **F1 fix ratifies** iff the re-measure shows geometry-correct spatial outcomes matching design intent (a balance ratification, not just a code fix).
- **Keystone integration ratifies** iff the Gate-2 re-measure validates JC-2 + contract §8 predictions.

---

## 8. Sign-off

KR's run earns a clean review: faithful to charter intent, disciplined on deletions and scope, correct to reconcile my stale charter against disk. The honest correction is mine to make twice over — my charter was both stale (wrong on 3) and incomplete (silent on 3 §5.1 items), and the "single convergent gate" reading undersells cond.5's pass/fail risk and conflates the combat-sim bar with the end-to-end-pipeline bar. The combat sim is genuinely close (gated on §6 → keystone → cond.5-PASS + F1). The end-to-end pipeline has a real tail beyond it — most notably the unbuilt UE export packet, which no one has been wrong about, just hasn't reached yet.

**Anchor docs:** charter `2026-06-16-engine-state-and-autonomous-run-plan.md`; RETURN-PACKAGE; wave-4-close; keystone contract `representative-loadout-measurement-contract-2026-06-16.md`; forward-architecture-contract `2026-06-11-...-wrap-and-extend.md` §9; gamora throughput note `2026-06-10-sim-throughput-profile-and-runner-architecture.md`; cert-wave `2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md`; ground-state §5.

**Author:** gandalf, 2026-06-16.
