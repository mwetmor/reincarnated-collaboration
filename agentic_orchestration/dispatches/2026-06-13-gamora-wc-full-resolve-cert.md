# Dispatch — 2026-06-13 — gamora — W-C-full: the RESOLVE certification (oracle §6.1)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-13 — K3 §5 row ratified (LOW-EDGE→BELOW @ open_arena, genre-forced), t-test canary rule affirmed, "W-C-full authoring is unblocked now." Sequence: this dispatch → jack-ryan Gate-1 → fire.
**Status:** GATE-1 PASS-WITH-WARN (jack-ryan DESIGN-MODE, 2026-06-13). Two folds applied: WARN-1 (t-test was over-generalized to all three KPM canaries; corrected to per-cell rule — strict-every-seed for the two open_arena canaries + K1@open_arena, one-sided t-test α=0.10 for **K1@chokepoint only**, the sole variance-sensitive cell per legolas §3) + WARN-2 (t-test wiring pinned to legolas §3 Rule B: pooled-mean vs floor, H₀ μ≥floor, one-sided, NOT a per-seed count). Two INFO folded: anchor-protection on K2@open_arena (the `A=43` scale anchor), and the two legolas seed-independence/CLT open questions. FIRES.
**Estimated effort:** multi-hour (band wire + spawn-spread fixture + pre-registered cert run + module validate-then-extend).
**Acceptance:** The spatial engine **passes the RESOLVE cert (oracle §6.1)** against the recalibrated **§2-S** band: (1) all six reference kits reproduce their §5 row within tolerance; (2) the **three KPM canaries** produce their required direction under the **per-cell decision rule** (legolas-scoped, NOT a single rule across all three): the two open_arena canaries (**K5 proxy IN**, **K4 mobile ≥ K2 stationary**) under the **strict every-seed rule** (≥4σ from floor → variance-immune per legolas §3); the **K1 single-target BELOW** canary under the rule appropriate to each density room — strict-every-seed at open_arena (5/5, 4.06σ), **one-sided t-test α=0.10 at chokepoint only** (the sole variance-sensitive cell, 1.03σ; passes now at N=5, t=−2.30, p=0.041 per legolas §4); (3) the **shape-flip** manifests (K2 radius-AOE and K3 line-AOE swap ranking between open_arena and chokepoint). Cert is **pre-registered (Discipline #2)** before the run. The **K4≠K6 boss-survival canary is OUT of scope** (deferred to W-F commit-grade per oracle §3.6).

## Context

This is the **formal RESOLVE cert — W-C exit** (oracle §6.1). The de-risk spike (`gamora/v-wc-derisk-spike-1`, engine `275e7a3`) produced the engine's first verified run and returned **GO validate-then-extend** (module triage M1–M4 KEEP, M5 KEEP-WITH-RECALIBRATE, M6 REBUILD-CANDIDATE). Two prerequisites the spike surfaced are now resolved:

1. **The band was recalibrated to the spatial instrument** (gandalf, oracle v1.2 **§2-S**, commit `aafb2c1`): the 1D-duel-unit band (floor 137–836) was re-expressed in spatial pack-clear units. Ships as a **parallel sibling constant `SPATIAL_ENCOUNTER_KPM_BAND`** (same shape as the 1D `ENCOUNTER_COHORT_KPM_BAND`), Balanced-key only, with the 1D band left intact until W-F deletes it. The circularity guard held (ratio invariant `R_expected=4`/`R_floor=2.5` asserted before the spike JSON was opened; spike supplied only the per-room scale anchor). A parallel gandalf hardening is folding the **TMPM 30-50 genre anchor** into §2-S as the external absolute-scale cross-check (~43 KPM ≈ 43 TMPM, in-band) — confirmatory, no numbers change, not a gate on this dispatch.

2. **The canary decision rule was settled** (legolas Mode-A consult, `agentic_orchestration/research/knowledge/2026-06-13-spatial-cert-canary-seed-count-methodology.md`): the strict "every-seed" canary rule is statistically broken for the variance-sensitive chokepoint cell (it passes a *correct* engine only 44% of the time at N=5). **Adopt the one-sided t-test at α=0.10** (95.5% power, <0.2% false-pass; aggregates all seeds). K1@chokepoint already passes it at N=5 (t=−2.30, p=0.041). The asymmetry to honor: a canary **false-PASS** (a broken engine slipping a genre-fatal direction through) is catastrophic and stays <1% under this rule; the old 4/5-BELOW situation was only a false-FAIL risk.

W-C-full formalizes the spike into a certified RESOLVE pass against the recalibrated band with the affirmed rule. **It runs in-seam** — the reference kits are the validated gamora-in-spike fixtures (rocket §5-hardening is W-D/W-F MEASURE-instrument prep per Matt's fixtures directive, NOT a W-C-full gate); the only fixture change here is the open_arena spawn-spread, which is your `arena.py` seam.

## Required reading before starting

- **The oracle, recalibrated:** `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md` — **§2-S** (the band you wire), §3 (room golden assertions), **§4.A** (pack-tuning — stays a live lever) + **§4.B** (spawn-spread — you implement this), **§5** (reference-kit verdict table + the ⚠ canaries; note the Matt-ratified K3@open_arena = BELOW), **§6.1** (the RESOLVE conditions you certify against), §7 (tolerance hypothesis + seed-count)
- **The band-recalibration dispatch + completion** `agentic_orchestration/dispatches/2026-06-13-gandalf-wc-kpm-band-recalibration.md` — the `SPATIAL_ENCOUNTER_KPM_BAND` interface name/shape you consume, the R invariant, the per-cohort=Balanced reduction
- **The canary-rule consult** `agentic_orchestration/research/knowledge/2026-06-13-spatial-cert-canary-seed-count-methodology.md` — the t-test α=0.10 rule + the K1@chokepoint N=5 result + the false-pass/false-fail asymmetry
- **Your own spike note** `reincarnated-engine/src/reincarnated/simulation/math/wc-derisk-spike-oracle-first-run-2026-06-13.md` — the module triage (M1–M6), the KPM-mismatch finding, the K4≠K6 + K4≥K2 fixture findings; and the spike baseline `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json`
- **W-C.5 close** `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md` — arity = 8 (do not re-open); the six-axis measurement gap is W-D scope, NOT W-C-full (RESOLVE is orthogonal to the orphan/coverage question per oracle §6.1)

## Cross-seam contract change? (Principle 6 gate — KR pre-assessment)

**YES — you consume gandalf's §2-S spec into code.** The `SPATIAL_ENCOUNTER_KPM_BAND` constant is your seam (it lives in `gauntlet_sim.py` alongside the 1D `ENCOUNTER_COHORT_KPM_BAND`). gandalf authored the *spec* (oracle §2-S); you implement the *constant* + the cert harness that reads it. Write a `simulation/MIGRATION.md` section documenting: the new sibling constant, the t-test canary rule contract, and the spawn-spread arena change. **Do NOT touch or overwrite `ENCOUNTER_COHORT_KPM_BAND`** — the 1D path still uses it; W-F deletes it.

## Scope

- [ ] **Wire `SPATIAL_ENCOUNTER_KPM_BAND`** (Balanced key) into the RESOLVE cert path per gandalf's §2-S spec — new sibling constant, 1D band untouched. Edges (Balanced): open_arena 21.5–107.5 · chokepoint 20.5–81.0 · magic 8.8–87.5 · elite 3.8–37.5 · mini_boss 0.6–10.0 · boss 0.6–8.8 (confirm against §2-S as authored; gandalf's TMPM hardening may add a note but not change these).
- [ ] **Implement the per-cell canary decision rule** in the cert harness (per the legolas note — the t-test is scoped to ONE cell, not all three canaries). The two open_arena canaries (K5 IN, K4 ≥ K2) use the **strict every-seed rule** (they are ≥4σ from floor → variance-immune; legolas §3 explicitly leaves these on the strict rule). The K1 BELOW canary uses strict-every-seed at open_arena and the **one-sided t-test α=0.10 at chokepoint only**. Implement the t-test per **legolas §3 Rule B**: a one-sided one-sample t-test on the **pooled-seed mean** against the room **floor** (H₀: μ ≥ floor; H₁: μ < floor), reject at α=0.10 → classify BELOW. (Tested edge = the floor; the genre-fatal direction is K1 reading IN, so the one-sided form binds the catastrophic false-PASS per legolas §3 asymmetry.) Confirm against the N=5 baseline (t=−2.30, p=0.041) before any wider run. NOTE: this is a t-test on the pooled mean / SE, **not** a per-seed count rule.
- [ ] **Implement §4.B spawn-spread** in `arena.py` open_arena: widen the 8-swarmer spawn spread so a single *stationary* nova cannot cover all 8 without repositioning — so K4 (mobile-AOE) reliably out-clears K2 (stationary radius-AOE) at open_arena (Risk-B; the spike showed K4≥K2 weak at 2/5 seeds, a fixture issue, not a band issue). Re-verify K4≥K2 holds under the decision rule after the spread change. **Re-check the full §5 table after the change** — confirm the spread perturbs no other reference-kit row. **Anchor protection (critical):** K2@open_arena is the `A=43` scale anchor the entire §2-S floor (21.5) is derived from (oracle §2-S.0(b)). The spread is designed to *lower* K2's clear (stationary nova can no longer cover all 8). After the change, re-confirm K2@open_arena not only stays IN but stays **near the `A=43` anchor** — a material K2 drop re-opens the floor derivation. Do NOT silently re-derive the band; surface any material anchor shift to gandalf.
- [ ] **Pre-register the cert (Discipline #2)** BEFORE the run: write down the §5 expected verdicts (incl. K3@open_arena = BELOW per Matt ratification), the three canary directions, the shape-flip prediction, the seed count, and the t-test rule — as a pre-registration artifact, so the cert is judged against a fixed prediction, not a post-hoc read.
- [ ] **Run the RESOLVE cert:** 6 reference kits × 6 rooms against §2-S, t-test rule. **Seed count:** N=5 is the legolas-validated baseline for the chokepoint canary; you set the final count empirically against spatial variance per §7 — raise it if any *other* cell proves edge-adjacent (the open_arena canaries are 4–9σ from floor → stable at N=5; chokepoint is the only tight one and N=5 already passes the t-test).
- [ ] **Module validate-then-extend** (the spike's GO): confirm M1–M4 KEEP reproduce under the formal cert; confirm M5 (the recalibrate item — band now recalibrated) KEEPs; for **M6 (REBUILD-CANDIDATE)** — its rebuild is the boss-survival/tank mechanism, which is W-F's commit-grade defensive-bridge re-validation. In W-C-full, **confirm M6 does not block the RESOLVE clear-rate cert** and **defer its boss-survival rebuild to W-F** (consistent with the K4≠K6 deferral below). Document the M6 boundary.
- [ ] **K4≠K6 boss-survival canary — document the W-F deferral explicitly.** Per oracle §3.6, the tank/mitigator/dodger/glass survival-mechanism distinction is the commit-grade defensive-bridge re-validation, owned by W-F. It is fixture-blocked in the spike (throwaway-tank DPS limit) and is **not** a RESOLVE gate. RESOLVE certifies clear-rate *resolution* (the 3 KPM canaries + shape-flip); survival-*mechanism* identity is MEASURE/W-F. Record this so RESOLVE does not gate on a fixture-blocked cell.
- [ ] **Smoke-test before the full cert run** (Discipline #2.1) — a subset cell run confirming the band wire + t-test harness + spawn-spread before the full 6×6×N sweep; declare resource-scaling (Disc #1.1) for the full run.
- [ ] `simulation/MIGRATION.md` section (the band constant + canary rule + arena change contract).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `gamora/v-wc-full-resolve-1`.

## Out of scope (explicit non-goals)

- **rocket §5 reference-kit hardening** — deferred to W-D/W-F MEASURE-instrument prep per Matt's fixtures directive ("hardening happens after the spike passes and they graduate to the standing MEASURE-cert instrument"). RESOLVE runs on the validated spike fixtures + your in-seam spawn-spread fix. **No rocket dependency.**
- **The MEASURE cert (axis-tuple computation from spatial telemetry)** — W-D. RESOLVE is orthogonal to the orphan/coverage question (oracle §6.1).
- **K4≠K6 commit-grade defensive-bridge re-validation** — W-F.
- **Editing/overwriting `ENCOUNTER_COHORT_KPM_BAND` or deleting any 1D path** — W-F.
- **Per-cohort band columns beyond Balanced** — W-D/W-F (all 6 ref kits are Balanced; the other 3 columns are deferred-not-invented).
- **Pushing to remote** — Matt's wave-close gate; accumulate commits.

## Open questions for the agent to resolve (document at Gate-2)

- **Final seed count** — N=5 is legolas-validated for the chokepoint canary; confirm empirically whether any other cell needs more under spatial variance (§7). Document the count + the per-cell variance basis. Also resolve the two legolas knowledge gaps bearing on N=5 sufficiency: (gap 1) **confirm fight-level seed independence** — your spike note §1.1 uses `base_seed ^ (fight_idx * 0x1337BEEF)`, so this is likely confirmable in-seam; (gap 2) **whether N=5 CLT-normality is adequate at chokepoint or it should go to N=9** (legolas recommends N=9 as the robust count: 95.5% power vs 78% at N=5). N=5 passes today; N=9 is the robustness fallback.
- **M6 rebuild boundary** — the minimal confirmation RESOLVE needs that M6 doesn't block clear-rate, vs what defers to W-F. Document the line you drew.
- **Spawn-spread side-effects** — confirm the §4.B widening perturbs no other §5 row (especially K2 at open_arena, which must stay IN).

## References

- Oracle §2-S/§3/§4.A/§4.B/§5/§6.1/§7: `canonical/story/2026-06-13-2d-spatial-golden-oracle-spec.md`
- Band recalibration dispatch + completion: `agentic_orchestration/dispatches/2026-06-13-gandalf-wc-kpm-band-recalibration.md`
- Canary-rule consult: `agentic_orchestration/research/knowledge/2026-06-13-spatial-cert-canary-seed-count-methodology.md`
- Spike note + baseline: `reincarnated-engine/src/reincarnated/simulation/math/wc-derisk-spike-oracle-first-run-2026-06-13.md`, `reincarnated-engine/output/wc-derisk-spike-2026-06-13.json`
- W-C.5 close: `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md`
- Gate-2: jack-ryan gates the RESOLVE pass — the pre-registration, the three canaries under the t-test rule, the shape-flip, and the M6/K4≠K6 deferral boundaries.

---

**Author:** knight-rider, 2026-06-13. The W-C exit — turns the de-risk spike's GO into a certified RESOLVE pass: the engine resolves combat correctly against the spatial-instrument band, with the three KPM canaries and the shape-flip proven under the t-test rule, and the survival-mechanism canary cleanly deferred to W-F's commit-grade boss room.

---

## Completion record

**Agent:** gamora. **Date:** 2026-06-13. **Tag:** `gamora/v-wc-full-resolve-1` (engine). **Status:** EXECUTED — RESOLVE cert run; one canary sub-clause SURFACED to KR for a disposition call (see below). NOT pushed (Matt wave-close gate).

**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/wc-full-resolve-cert-2026-06-13.md` (authored BEFORE code, Discipline #1).
**Cert harness:** `reincarnated-engine/scripts/gamora_wc_full_resolve_cert_2026_06_13.py`.
**Cert output:** `reincarnated-engine/output/wc-full-resolve-n9-2026-06-13.json`.
**MIGRATION:** `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.30.

### (a) RESOLVE PASS/FAIL — pre-registration vs result

**36/36 reference-kit §5 rows reproduce their pre-registered side** (N=9, spike-validated layout). Every kit×room cell matches expectation, including the Matt-ratified **K3@open_arena = BELOW** (19.5 < 21.5 floor). The shape-flip manifests, the anchor held, K1/K5 canaries pass cleanly.

**The ONE non-pass: the K4≥K2 ≥-margin sub-clause (6/9 seeds).** K4 IN @open (the actual canary *direction*) is 9/9 IN; K4 ≥ K2 holds on the MEAN (45.2 ≥ 41.1) but not every seed. Diagnosed (Discipline #11) as the **M1 movement-credit gap**: the player AI is "close to the NEAREST mob until in attack range" (`spatial_engine.py:1166-1193`) — there is NO "reposition to GATHER mobs into the AOE" primitive. K4's higher movement_speed only speeds *closing*, not *gathering* → the ≥K2 margin is closing-time noise, NOT spawn-spread-tunable. Four spawn geometries were smoke-tested at N=9 (clump / two-wing / arc / scatter); NONE satisfies K4≥K2-margin AND K3=BELOW AND K5=IN AND anchor simultaneously — the tension is structural (margin wants spread; the other three want clump). Math note §4.5.

### (b) The three KPM canaries under the per-cell rule

| Canary | Rule | Result | Verdict |
|---|---|---|---|
| K1 BELOW @ open_arena | strict every-seed | 9/9 below floor 21.5 | **PASS** |
| K1 BELOW @ chokepoint | one-sided t-test α=0.10 | mean 18.86, **t=−3.75, p=0.0028** (df=8); N=5 baseline reproduced t=−2.30/p=0.041 | **PASS** |
| K5 IN @ open_arena | strict every-seed | 9/9 in (30.6–38.7) | **PASS** |
| K4 ≥ K2 @ open_arena | strict every-seed | K4 IN 9/9; **≥K2 margin 6/9** (mean K4 45.2 ≥ K2 41.1) | **DIRECTION PASS / ≥-MARGIN SURFACED** |

K1@chokepoint t-test statistic: **t = −3.75, p = 0.0028** at N=9 (stronger than the N=5 baseline t=−2.30 as legolas predicted; rejects H₀ μ≥floor at α=0.10 → BELOW).

### (c) Shape-flip

**MANIFESTS.** open_arena: K2 41.1 > K3 19.5. chokepoint: K3 33.1 > K2 25.2. Ranking swaps → geometry × room genuinely simulated (M2 real). Stable across all 9 seeds.

### (d) Final seed count + the two legolas open questions

**N=9** (legolas robust count: 95.5% power, CLT-reliable at chokepoint; resource cost trivial — 324 fights ~5s).
- **Gap 1 (fight-level seed independence) — RESOLVED in-seam:** `seed = base_seed ^ (fight_idx * 0x1337BEEF)`; all RNG streams reseeded per fight (`random.Random(seed)`, `np.random.default_rng(seed)`, `…^0x5F3759DF`); entities rebuilt fresh per fight. No shared spawn-position RNG across fights → effective N = literal N. (Math note §7.1.)
- **Gap 2 (N=5 CLT-normality vs N=9) — RESOLVED: go to N=9.** The only variance-sensitive cell (K1@chokepoint, 1.03σ) is exactly where CLT matters; N=9 is where legolas says CLT is reliable. The 3 open_arena canaries are 4–9σ from floor → variance-immune at any N≥3, over-covered at N=9 at no risk. (Math note §7.2.)

### (e) K2@open anchor status after the spawn-spread

**A=43 HELD.** The shipped layout is the spike-validated clump; K2@open = **41.06** KPM, within the ±20% anchor gate [34.4, 51.6] and well above the 21.5 floor. **No material anchor shift → the §2-S floor derivation does NOT re-open.** (Note: the rejected arc/scatter geometries DID drop K2 off-anchor — a reason they were not shipped.)

### (f) The M6 boundary + K4≠K6 deferral

**M6 boundary drawn (math note §6):** RESOLVE requires M6 (flanking/survival) to be *non-corrupting of clear-rate* — confirmed, since the canaries + shape-flip live in density/mid rooms where M2/M4/M5 govern KPM, not M6's flanking/eHP path. RESOLVE does NOT require M6 to *correctly distinguish survival mechanisms* (that is W-F). **K4≠K6 boss-survival ⚠C4 cleanly deferred to W-F** — fixture-blocked (throwaway K6 tank str=50 can't out-DPS the 60k boss in 240s; fails a DPS check, is NOT dying), SURV-judged, survival-mechanism identity is commit-grade defensive-bridge re-validation (oracle §3.6). RESOLVE did not gate on it.

### (g) What needs Matt / gandalf before W-D

**THE DISPOSITION CALL (above gamora seam authority — surfaced per dispatch "STOP and surface"):** Does RESOLVE **PASS** with the K4≥K2 ≥-margin recorded as the surfaced M1 movement-credit finding (consistent with oracle §2-S.5 finding 3's edge-placement tier-a disposition + the dispatch two-tier rule: "the IN direction reproduces; the ≥-margin does not robustly reproduce and is surfaced for W-C-full tuning"), or does it **hard-gate** on the literal K4≥K2 canary (→ FAIL until an M1 gather primitive is added)? This is a gandalf design-authority read of the oracle's canary definition (Matt ratified the canary rules). gamora's recommendation: **PASS-WITH-SURFACED-FINDING** — 36/36 §5 rows + 3 clean canaries + shape-flip + held anchor is a robust RESOLVE; the K4≥K2 margin is a *known* M1 gap (pre-flagged twice: oracle §2-S.5 finding 3 + spike note §7), not a new engine fault, and the *fix is outside the spawn-spread lever* (an M1 player-gather primitive, engine-movement seam, W-D/W-F). Routing the M1 gather-primitive item to KR/rocket for W-D/W-F is the design response if the ≥-margin must hard-pass.

**Author:** gamora, 2026-06-13.
