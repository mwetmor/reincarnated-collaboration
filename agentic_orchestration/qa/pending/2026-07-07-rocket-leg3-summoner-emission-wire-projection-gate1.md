# Gate-1 submission (DESIGN-MODE) — 2026-07-07 — rocket — Leg-3 STEP 1: summoner emission-wire design + resource/LLM-cost projection

**Submitter:** rocket (generation seam)
**Reviewer:** jack-ryan (Gate-1, DESIGN-MODE — pre-fire peer collaborator)
**Mode:** DESIGN + PROJECTION only. NO production code landed. NO run fired. This is STEP 1 of a 2-step leg.
**Artifact under review:** `reincarnated-engine/src/reincarnated/generation/math/leg3-summoner-emission-wire-and-projection-2026-07-07.md`
**Governing dispatch:** `dispatches/2026-07-07-rocket-leg3-summoner-emission-wire-and-run.md` STEP 1
**Predecessor (certified):** leg-2 coordinated Gate-2 PASS-WITH-FOLLOWUPS — your finding `qa/findings/2026-07-07-leg2-summoner-emission-route-coordinated-gate2.md` (`3bae44a`, 378 tests green)
**Spec:** `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` v3 §4 (role-split / bands), §8-A1 (emission acceptance)
**Principles engaged:** 1 (math-before-code), 3 (cross-seam impact / MIGRATION), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #1.1, #8, #11, #12, #23
**Commit (math note):** landed on `main` as a leg-3 math note (in-scope work-product, auto-commit); NOT pushed (Matt-gated).

---

## What STEP 1 delivers (all in the artifact)

1. **Emit-wire design** (artifact §2) with a **load-bearing site correction** (§1): the dispatch + leg-2 MIGRATION
   name `season_generation_pipeline.py:404-412` as the wire site, but that is the dataclass FIELD DEFINITION —
   `KitCandidate.primary_t4` is NEVER assigned in the pipeline (grep-proven zero hits). The true DDA stamp is
   **`cycle14_wave5_emitter.py:546`** (`primary_t4 = PRIMARY_T4`), consistent with your leg-2 finding ref line 66.
2. **Adapter design** (§2.3): `route_primary_t4()` returns an `AlterationOutput` OBJECT (`strategy_type`, …), the
   emit slot needs a validator-shaped DICT (`strategy`, `scope`, `discipline_anchor`). No existing adapter — this
   is the one net-new code artifact STEP 2 writes. Clause D emits the EXACT frozen `PRIMARY_T4` dict on the DDA
   fallback → solo population byte-identical.
3. **Disc #1.1 resource/LLM-cost projection** (§3 — THE artifact for Matt's run-auth): pilot scope ≤ 200 proxy
   candidates, seed 56M, deterministic; ≤ 36 min wall-time; ≤ 80 MB peak; ≤ 7 proxy entities/fight; **LLM: $0 on
   a dry-run pilot (recommended first), ≤ $10 with flavor** (anchored on W3's empirical $0.025–0.050/survivor).
4. **`test_w3_emission_driver` root-cause** (§4): the failing smoke is a **hard-coded full-run 300/400
   identity-glyph-split assertion** (`w3_emission_driver.py:688`) with no smoke guard. Reads
   `identity_glyph`/`bc_target_cell.range` — **ORTHOGONAL to the emit path** (zero `primary_t4`/proxy refs) — but
   WILL gate the pilot because a proxy-inclusive run also breaks the 300/400 invariant. Fix named (§4.4).
5. **Refutation conditions** (§7, Disc #23) — cheapest refuting test per claim; the site-correction, adapter-need,
   and orthogonality claims are already empirically confirmed (grep + read + reproduced failure).

## The Gate-1 asks (specific)

- **A. Ratify the wire-site correction** (§1): is `cycle14_wave5_emitter.py:546` the correct wire target, and do
  you concur the dispatch's `season_generation_pipeline.py:404-412` reference is a field-def / populate-site
  conflation (not a populate site)?
- **B. Ratify the freeze proof** (§2.2 + §6): does the adapter Clause D (emit exact `PRIMARY_T4` on DDA fallback)
  preserve the byte-identical solo path, and is `scope="chain_wide_own"` (a new slot LABEL on a never-populated
  proxy slot) correctly NOT a magnitude/bar/band touch?
- **C. Ratify the cost envelope** (§3.4) for KR→Matt relay: is ≤ $10 (or $0 dry-run-first) a sound bounded
  authorization number, and is the dry-run-first recommendation the right run-auth framing?
- **D. Ratify the cross-seam finding** (§5): STEP 2 has 4 touch-points, 3 in star-lord's `export/`
  (emit-wire, driver-drive, glyph-assertion-fix) + 1 in rocket's `bc_target_composer.py` (proxy-bin un-gate).
  Do you concur STEP 2 must be a **rocket+star-lord co-dispatch**, not a solo rocket landing? This is the routing
  consequence KR needs.
- **E. W3-smoke verdict** (§4): concur ORTHOGONAL-to-emit-path but GATES-the-pilot, and the §4.4 fix (population-
  aware assertion, star-lord's file) is the right disposition?

## What STEP 1 explicitly does NOT do

- NO emit-wiring code. NO adapter code. NO composer un-gate code. NO run. NO push.
- Does NOT resolve the §2.5 A1 `t4_candidates`-family-membership coverage question (a STEP-2 measurement item; flagged).
- Does NOT pick between §4.4 fix options (a) vs (b) — that is star-lord's file-owner call at STEP 2.

## STEP-2 gating (for the record)

STEP 2 (wire + un-gate + run + Gate-2) fires ONLY on: (1) this Gate-1 PASS, AND (2) Matt run-authorization against
the §3 envelope (ADR-006 external/compute + LLM-cost). Chassis FROZEN, bars/bands FIXED throughout.
