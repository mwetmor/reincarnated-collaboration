# The 2D Spatial Golden Oracle — Certification Spec

> **STATUS:** CURRENT (load-bearing as of 2026-06-13) — see `canonical/00-ground-state.md`

**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward; design authority for the oracle)
**Status:** v1.1 — design-spec-as-math; Matt-authorized 2026-06-13 ("and then the golden oracle for 2D"). gamora executes the validation; this doc is the acceptance authority. **v1.1 amendment (same day, per Matt challenge):** § 6 cert gate split into RESOLVE (W-C; orthogonal to orphans) + MEASURE (W-D/W-F; downstream of the BC coverage audit); MEASURE arity consumes the Bucket-B ruling, no longer presumes 8 axes.
**Authority:** Matt 2026-06-13 — authored from the Pattern-B combat-sim-architecture dialogue (this session).
**Companion docs:**
- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` — the wave (§ 5) this oracle gates; the cert wave's W-A authors this, W-C validates against it
- `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md` — § 5 commit-grade-is-the-2D-playspace; this is how commit-grade gets *proven* rather than asserted
- `canonical/story/gauntlet-arena-scenarios-magic-elite-miniboss-2026-05-21.md` — prior gandalf scenario-design authority (the 6 rooms' implementation spec)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the 8 axes the commit-grade BC computes from spatial telemetry (W-D)

---

## 0. TL;DR

1. **The oracle is the ground truth the 2D engine has never been measured against.** The spatial engine is ~1900 lines of built scaffolding that has **never produced a single successful, verified run.** Until we can say "for THIS known kit in THIS known room, the engine produces THIS result, and we hand-verified that result is correct from genre knowledge," every kit it characterizes is unprovable. This doc *is* that ground truth: hand-authored known-correct answers for the six existing rooms and a set of reference kits.
2. **The rooms already exist; the bands already encode the skew.** `arena.py` defines the six `ArenaScenario` objects; `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206–311) already sets per-room KPM targets that *encode the AOE-skew in hard numbers* — open_arena/chokepoint demand **137–836 KPM** (unreachable by single-target against 8 mobs in 120 s); boss/mini_boss expect **18–225** (single-target range). The oracle does not invent targets; it verifies the engine *realizes* the targets that are already designed.
3. **The oracle bakes in the three risks Matt named** (this session's A/B/C): pack count tuned so the high-KPM rooms are **AOE-only-reachable** (A); at least one room that rewards **movement-as-AOE-setup** (B); the **mob AI pinned** so AOE is rewarded-but-not-free (C4). Each becomes a concrete acceptance test via a reference kit whose golden result *requires* the engine to credit that dimension.
4. **The reference-kit set is the genre's diversity, used as a test instrument.** Six known-correct kits (single-target, radius-AOE, line/cone-AOE, mobile-AOE-farmer, proxy/summoner, tank). Each has an *expected per-room verdict*. The engine is certified when it reproduces all of them within tolerance — which proves it teaches the genre rather than flattening it. Two of them (single-target, proxy) are **canaries**: the engine must *reject* single-target at the density rooms and *reward* proxy at them. If it doesn't, it's lying in the genre-fatal direction.

---

## 1. What the oracle IS and IS NOT

**IS:** a hand-authored set of `(reference_kit, room) → expected_verdict` cells, derived from genre design knowledge, that the spatial engine must reproduce to be trusted as the **sole** behavioral-identity authority (per the companion doc, 1D no longer mints identity). It is the keep-vs-rewrite judge for the W-C module pass: a module is kept if the cells it touches reproduce; rebuilt if they don't.

**IS NOT:** a from-scratch room build (the rooms exist), a balance pass (it certifies the *instrument*, not the kits the instrument will later judge), or a 1D artifact (it runs exclusively on the spatial engine).

**Why now is the right point** (Matt's timing claim, affirmed): the golden answers *require* knowing what we measure. You cannot author "the correct verdict for a nova in the open arena" without the locked axes (so the verdict populates the right dimensions) and the KPM bands (so "correct clear-rate" has a number). Both are now done. The axes/labels/hypotheses work that was completed *instead of* the simulator last cycle is precisely the prerequisite that makes this oracle authorable. The detour built the ruler.

---

## 2. The anchor — the bands already encode the skew

Verified `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:206–311), `(lo, hi)` KPM per (room, cohort):

| Room | DPS-min-maxer | Balanced | Defensive | Hybrid | Reading |
|---|---|---|---|---|---|
| **open_arena** | 193–836 | 150–664 | 368–560 | 137–728 | **HIGH — AOE-only.** 8 mobs, 120 s, all-killed. To clear at 150+ KPM you must hit many at once. |
| **chokepoint_corridor** | 182–836 | 150–664 | 368–560 | 137–728 | **HIGH — line/cone-favoring.** Funnel concentrates mobs into a line. |
| **magic_pack** | 52–614 | 47–555 | 34–380 | 44–453 | Mid. Champion + retinue. |
| **elite_pack** | 51–699 | 47–660 | 37–447 | 47–573 | Mid-high. Few tanky + adds. |
| **mini_boss** | 46–204 | 29–180 | 29–136 | 29–166 | **LOW — single-target.** |
| **boss_with_adds** | 29–225 | 22–180 | 18–151 | 21–197 | **LOW — single-target + flanking.** |

The skew is *in the bands*: the two density rooms demand a clear-rate that single-target cannot physically produce, and the two boss rooms expect single-target rates. This is the genre teaching mechanism, already designed. **The oracle's core job is to verify the engine produces KPM inside these bands for the cohort the kit belongs to — and, critically, produces KPM *outside* the band when a kit is the wrong archetype for the room** (a single-target kit must fall *below* the open_arena floor; an AOE kit must fall *below* the boss... no — an AOE kit at boss simply produces low single-target KPM, which is *in* the low boss band; the canary is the single-target kit *failing the high density floor*).

---

## 3. The six rooms — golden assertions

Each room's golden behavior, stated as what a *correct* engine must produce. Room facts verified in `arena.py`.

### 3.1 open_arena (50×50, 8 swarmers, 120 s, all-killed) — the AOE god-room
- A **radius-AOE** kit clears all 8 within the band (≥150 KPM Balanced).
- A **single-target** kit **cannot reach the floor** (falls below 137–193 KPM) — it kills one at a time while the pack applies pressure. **If the engine puts single-target in-band here, it is broken (over-crediting single-target) — fail certification.**
- The room rewards **repositioning** (B): the 8 spawns are spread (x∈[18,32], y∈[8,18]); a stationary nova may not cover all 8 — a kit that *moves to gather then AOEs* should out-clear a stationary one of equal AOE. (See § 4.B.)

### 3.2 chokepoint_corridor (10×50, 5 m bottleneck at y=23–27, 8 swarmers, kills-only) — the geometry room
- A **line/cone-AOE** kit is **best here** — the funnel queues mobs into its shape.
- A **radius-AOE** kit is **worse here than in open_arena** — the corridor denies the spread it wants. **The ranking of radius-AOE vs line-AOE must FLIP between open_arena and chokepoint.** This flip is the diversity-generator (it makes AOE *shape* a build axis). **If the two rooms rank the two AOE shapes identically, the geometry isn't being simulated — fail certification.**

### 3.3 magic_pack (32.7×14, 1 magic + 3 swarm, kills-only) — champion + retinue
- Blended: AOE clears the retinue; some focus finishes the champion. In-band for AOE and proxy cohorts.

### 3.4 elite_pack (few tanky + adds) — the transition
- Rewards *some* single-target priority alongside clear. A pure-nova with no focus should sit at the *low* edge; a hybrid should sit center-band.

### 3.5 mini_boss (single-target survival) — LOW band
- Single-target and mobile-survivor kits in-band; pure-density kits at the low edge (they can still chip a lone target).

### 3.6 boss_with_adds (30×30, 1 boss r=1.5 + 2 flanking elite brutes, 240 s, boss-killed) — the climax
- **This room is the commit-grade home of the defensive bridge.** The 1D boss-duel panel (`boss/brute/physical` + `boss/brute/fire`) that produced the bridge's 25/22/23/26 was a *search-grade proxy for this room.* Certification re-validates the tank/mitigator/dodger/glass separation **here, commit-grade** (companion doc W-F).
- A **mobile** kit survives via kiting/dodging the flank pressure; a **tank** survives via eHP. Both in-band; **if the engine cannot distinguish their survival mechanism, the AI/positioning model is too coarse (C4)** — diagnostic.

---

## 4. The three risks, baked in as acceptance parameters

### A — monster count → KPM AOE-only-reachable
**Parameter:** the density rooms' pack size must make the high KPM bands **physically unreachable by single-target.**
**Acceptance test:** reference kit **K1 (single-target)** must score **below** the open_arena/chokepoint floor; reference kit **K2 (radius-AOE)** must score **in-band**. If K1 reaches the floor at pack = 8, **the pack is too small** — raise the swarmer count (8 → 10/12…) until single-target falls below the floor *and* AOE stays in-band. The current `arena.py` pack of 8 is the *starting* hypothesis; the oracle's first job is to confirm-or-raise it. This is the literal mechanism by which "not enough corpses" (Matt's original question) becomes a tuned parameter rather than a vibe.

### B — movement-as-AOE-setup
**Parameter:** at least one room must reward *moving into position to land AOE*, not just standing and firing.
**Acceptance test:** reference kit **K4 (mobile-AOE farmer)** must **out-clear** an equal-AOE *stationary* kit in open_arena, by using movement to gather/reposition against the spread spawn. If the mobile kit does not beat the stationary one despite equal AOE, the engine is modeling movement only as flee, not as setup — **fail B; rebuild the movement/positioning credit.** (If needed, open_arena's spawn spread widens so a single stationary nova *cannot* cover all 8 without repositioning.)

### C4 — mob AI pinned
**Parameter:** the golden answers assume a **specified** mob behavior (the existing aggro-radius 8 m, swarm leash override 35 m, pursuit-to-player). This behavior is **pinned as part of the oracle** — if the AI changes, the golden master re-derives.
**Acceptance test:** the pinned AI must produce **realistic spread + pursuit** such that AOE is *rewarded but not free.* Specifically: mobs must **not** all collapse to a single point (which would make any AOE trivially clear every room and destroy differentiation), and must **not** scatter so widely that AOE never multi-hits. The diagnostic: if K2 (radius-AOE) trivially aces *every* room including the boss rooms, the AI is over-clumping (AOE-blob bias — the opposite failure from 1D's single-target bias). Pin the AI to the regime where § 3.1/§ 3.2's shape-flip actually manifests.

---

## 5. The reference-kit set — genre diversity as the test instrument

Six known-correct kits. Each cell is the **expected verdict** the engine must reproduce. `IN` = KPM in the room's cohort band; `BELOW` = below floor (correct rejection); `LOW-EDGE` = in-band but near floor; `SURV` = survives (boss/mini rooms judged on kill + survival).

| Ref kit | open_arena | chokepoint | magic_pack | elite_pack | mini_boss | boss_with_adds | Genre anchor |
|---|---|---|---|---|---|---|---|
| **K1 single-target** | **BELOW** ⚠ | **BELOW** ⚠ | LOW-EDGE | IN | IN | IN | D3 single-target dummy-DPS / the harness-not-playspace canary |
| **K2 radius-AOE (nova)** | IN | LOW-EDGE | IN | IN | LOW-EDGE | LOW-EDGE | PoE nova/Cyclone screen-clear |
| **K3 line/cone-AOE** | LOW-EDGE | **IN (best)** | IN | IN | LOW-EDGE | LOW-EDGE | Glacial Cascade / corridor-hold |
| **K4 mobile-AOE farmer** | **IN (≥K2 via setup)** ⚠B | IN | IN | IN | IN | **SURV (via kite)** ⚠C4 | D3 zoom-DH / PoE deadeye-mapper — the chase fantasy |
| **K5 proxy/summoner** | **IN** ⚠ | IN | IN | IN | LOW-EDGE | LOW-EDGE | D2 skeleton-army — the 100%-1D-fail archetype, S-tier in density |
| **K6 tank** | LOW-EDGE (Def) | LOW-EDGE | LOW-EDGE | LOW-EDGE | SURV | **SURV (eHP, ≠K4 mechanism)** ⚠C4 | the defensive-bridge tank, commit-grade |

⚠ = **canary cell** (engine must produce this *exact* direction or it is lying genre-fatally):
- **K1 BELOW at the density rooms** — single-target *must* fail to clear; if it passes, 1D's lie has leaked into 2D.
- **K5 IN at open_arena** — the summoner that fails 100 % of 1D duels *must* be density-S-tier; if it fails, proxy density isn't credited (the BC coverage-audit blind spot, made fatal).
- **K4 IN at open_arena (≥ K2)** — proves B (movement-as-setup).
- **K4 vs K6 distinct survival at boss** — proves C4 (the AI distinguishes kite-survival from eHP-survival).

---

## 6. The certification gate — TWO certs, sequenced

> **Amendment 2026-06-13 (v1.1, per Matt challenge):** v1 bundled both certs into one 5-condition gate and hard-coded "the 8-axis bin" in condition 4 — which presumed the BC measurement-coverage audit's answer. It does not. The gate is now split into **RESOLVE** (gates W-C; *not* downstream of orphans) and **MEASURE** (gates W-D/W-F; downstream of the coverage audit), and MEASURE's arity consumes the Bucket-B ruling rather than presuming 8 (§ 6.3).

The oracle certifies two distinct engine responsibilities, and they gate **different wave phases** because one is downstream of the coverage audit and one is not.

### 6.1 RESOLVE cert — gates W-C (orthogonal to orphans)

The spatial engine **resolves combat correctly** when **all** hold:

1. **All six reference kits reproduce their § 5 row** within tolerance (tolerance per § 7).
2. **All four canary cells** (⚠) produce their required direction — non-negotiable; a near-miss on a canary is a fail.
3. **The shape-flip manifests** — K2 and K3 swap ranking between open_arena and chokepoint (§ 3.2).

This cert is **independent of the orphan/coverage question.** The reference kits are *hand-authored* known-correct, so they bypass generation's allocator orphans entirely (the built-lever-no-allocator failure that bit the defensive bridge cannot bite a kit constructed by hand). RESOLVE is the **deepest prerequisite in the whole architecture**: the engine has never produced a verified run, and the MEASURE cert below (condition 5, the defensive-bridge commit-grade re-validation) *cannot run until RESOLVE passes* — re-validating anything in the boss room needs a working spatial engine. RESOLVE is therefore **upstream of the orphan work's own final step**, not after it.

### 6.2 MEASURE cert — gates W-D / W-F (downstream of the coverage audit)

The spatial engine **measures kit identity correctly** when **both** hold:

4. **The complete axis surface is computed from spatial telemetry** — every axis *per the Bucket-B coverage ruling (§ 6.3)* is assigned from the spatial run (replacing the placeholder `bc_cell`) and **wired, not default-valued** (the Bucket-A check, on the spatial seam); the result is minted as a `CommitGradeVerdict` (companion § 3.1).
5. **The defensive bridge re-validates commit-grade** in boss_with_adds — tank/mitigator/dodger/glass separation holds on the spatial boss room, not just the 1D duel panel.

### 6.3 The arity is NOT settled at 8 — it consumes the coverage audit

v1 said "the 8-axis bin." That presumed the May-20 lock's 8 axes still **cover** the current kit surface. They may not: generation has built proxy-density, charge-stack, T4 mechanics, and companion-binding *since* the lock (`agentic_orchestration/gandalf/notes/2026-06-13-bc-measurement-coverage-audit-query.md` — Bucket A re-opened deferrals + Bucket B unaxised features). That audit's own § 7: certifying the archive kit-complete before it runs *"would repeat the keystone's mistake one architectural layer up."* So MEASURE's arity is whatever the **Bucket-B design ruling** (routed to gandalf) determines — 8, or 8+N. If Bucket B promotes (e.g.) proxy-density to a real axis, then condition 4 wires a 9-tuple **and this oracle's reference-kit set (§ 5) grows a 7th kit that varies on the new axis** — without it, the engine would measure two kits that differ only on proxy-density as identical and cull one (the genre-flattening this whole architecture exists to prevent). The **Axis-4 defensive orphan is already handled** — sized + ruled ONE-OFF (`agentic_orchestration/gandalf/notes/2026-06-13-bc-orphan-sizing-ruling.md`), sitting in condition 5; § 6.3 is about the *broader* coverage question the second audit, still in flight, owns.

### 6.4 Wave exit

- **RESOLVE (§ 6.1)** = W-C exit.
- **MEASURE (§ 6.2)** = W-D exit (condition 4) + W-F exit (condition 5).
- Only when RESOLVE **and** MEASURE pass does "the archive measures the current kit" stop being a claim and become a measured fact — and only then does the 1D engine delete (companion § 4).

---

## 7. Methodology-hotspot flag (Discipline #18)

The pack-size calibration (§ 4.A), the movement-credit threshold (§ 4.B), and the verdict tolerances (§ 6) are **design-math calibration choices.** Per the OP § 4.2 refinement (methodology-consultation fires AFTER a baseline exists, not before): the **first** golden master is **genre-design-authored** (this doc, gandalf seam) and validated empirically by the first spatial runs. If, after the baseline runs land, the tolerance/pack-size calibration touches a statistical-methodology question (e.g., how many seeds to call a KPM "in-band" under spatial variance, given the collision/aggro stochasticity), **that** is the point to route a legolas Mode-A methodology consult — not before. The empirical criterion that gates "oracle calibrated" is the reference kits reproducing with stable verdicts across seeds — substrate evidence, not assertion.

**Tolerance starting hypothesis (subject to the above):** a verdict is reproduced if the kit's median KPM across the commit-grade fight count lands on the correct side of the band edge (IN/BELOW/LOW-EDGE) for ≥ the seed-majority; canary cells require the correct side at *every* seed. gamora sets the seed count against the spatial variance once baseline runs exist.

---

## 8. Cross-references

- Drift-proofing + cert wave (companion; the wave this gates): `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md`
- Forward-architecture contract § 5 (commit-grade = 2D playspace): `canonical/story/2026-06-11-forward-architecture-contract-wrap-and-extend.md`
- Prior scenario-design authority (the 6 rooms): `canonical/story/gauntlet-arena-scenarios-magic-elite-miniboss-2026-05-21.md`
- BC axes lock (the 8 axes commit-grade BC computes): `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- Verified code anchors (2026-06-13): scenarios `spatial_gauntlet/arena.py:283-712`; KPM bands `gauntlet_sim.py:206-311`; throughput `gauntlet_sim.py:318-322`; archive insert `gauntlet_archive.py:208`; placeholder cell `balance_loop.py:2827`
- ground-state oracle registration: `canonical/00-ground-state.md` § 1

---

**Signed:** gandalf, 2026-06-13
**For:** the hand-authored ground truth that turns the 2D spatial engine from unvalidated scaffolding into a certified, sole behavioral-identity authority — six rooms anchored on the already-designed KPM bands, with Matt's three risks (AOE-only pack count, movement-as-AOE-setup, pinned mob AI) baked in as canary acceptance tests, and a reference-kit set that uses the genre's own diversity (single-target / radius-AOE / line-AOE / mobile-farmer / summoner / tank) as the instrument that proves the engine teaches the genre rather than flattening it.
