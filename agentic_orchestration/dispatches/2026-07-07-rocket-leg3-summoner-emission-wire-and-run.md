# Dispatch — 2026-07-07 — rocket — Leg-3: summoner emission wire + run (emit-assignment activation + pilot emission)

**From:** knight-rider
**To:** rocket (generation seam)
**Approved by:** Matt 2026-07-07 (arc-close batch, Item 1 lane: "rocket: gen-path legs 2–3 (summoner emission path)") for the LANE. **The emission RUN itself is a SEPARATE Matt authorization** (ADR-006 external/compute action + LLM-cost) — jack-ryan's coordinated-Gate-2 readiness call is explicit on this. This dispatch is staged so STEP 1 (design + projection + Gate-1) fires now; STEP 2 (wire + run) fires ONLY on Matt's run-authorization with the projection in hand.
**Estimated effort:** STEP 1 small (design note + resource projection + Gate-1). STEP 2 medium (emit-wiring code + emission run + Gate-2).
**Acceptance (whole leg):** the emit assignment (`season_generation_pipeline.py:404-412`, still the universal-DDA slot) is wired to call rocket's `route_primary_t4()` so proxy-bearing summoner kits emit a ratified proxy-family `primary_t4`; a pilot emission run produces pilot-ready summoner kits into the four-family instrument; the run's resource/LLM cost was projected + Matt-authorized BEFORE it fired; the pre-existing `test_w3_emission_driver` smoke is root-caused + re-cleared. **Leg-3 completion is the unblocking event for star-lord's Leg C re-fire + gamora's summoner proxy-T4 sim-eval** (Matt Item 1).

## Context — leg-2 is certified; leg-3 activates + runs it
Leg-2 (the three-seam machinery: route fn + emit-validator + sim consume-side) is certified — coordinated Gate-2 PASS-WITH-FOLLOWUPS (jack-ryan finding `3bae44a`, 2026-07-07; 378 tests green at HEAD). Leg-2 is **inert on the current all-non-summoner population** because the emit assignment still hard-codes DDA (`season_generation_pipeline.py:404-412`). Leg-3 is the activation: wire the emit path to `route_primary_t4()`, then run a pilot emission so real summoner kits (proxy-family `primary_t4`) enter the four-family instrument.

## STEP 1 — design + projection + Gate-1 (fires now; NO code, NO run)
**Math/design-before-code (Disc #1) + resource-bounds (Disc #1.1):**
1. **Emit-wiring design note:** the exact change at `season_generation_pipeline.py:404-412` — replace the universal-DDA assignment with `route_primary_t4(..., proxy_decls=build_proxies_surface(kit.skills))` so proxy-bearing kits draw a proxy-family member, empty-decl kits keep DDA (byte-identical). This is a certification-path behavior activation — the critique pair prices the role-split + emission-band (spec v3 §8-A1 ≥90%/≥60%) consequence NOW that it goes LIVE.
2. **Disc #1.1 resource/LLM-cost projection (THE artifact Matt needs to authorize the run):** the pilot emission run's peak concurrent entities, wall-time, AND LLM call count + token/$ cost projection (if the emission path invokes the LLM for flavor/naming). State the run's scope (how many summoner kits, which cells, seeded/deterministic?) and its bounded cost envelope.
3. **`test_w3_emission_driver` root-cause:** jack-ryan confirmed this pre-existing smoke fails on the clean baseline (NOT leg-2-caused; zero refs to route/C2). Leg-3 runs the emission driver — root-cause WHY the smoke fails and whether it touches the leg-3 emission path. If it gates the run, name the fix; if orthogonal, prove it.
4. **Refutation conditions (Disc #23).**
- **Submit STEP-1 to `agentic_orchestration/qa/pending/` for jack-ryan Gate-1 (DESIGN-MODE).** Then STOP. Report the projection to KR for Matt's run-authorization.

## STEP 2 — wire + run (fires ONLY on Matt run-authorization + Gate-1 PASS)
- Land the emit-wiring code (per the Gate-1-cleared design).
- Run the pilot emission (Matt-authorized; within the projected envelope).
- Verify pilot summoner kits carry proxy-family `primary_t4`; emission bands measured (spec v3 §8-A1) — REPORT the band outcome (it's a measured result, not a leg-3 pass/fail threshold per the Gate-1 framing).
- MIGRATION.md update (emit path now live); AGENT_STATE.md.
- Tag `rocket/v-batch2-leg3-summoner-emission-run-1`.
- **Submit to `qa/pending/` for jack-ryan Gate-2** (certification-path activation + run artifacts).

## Required reading before starting
- This dispatch's leg-2 predecessor: `dispatches/2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md` (the machinery leg-3 activates).
- jack-ryan coordinated Gate-2 finding `qa/findings/2026-07-07-leg2-summoner-emission-route-coordinated-gate2.md` (`3bae44a`) — the leg-3 followup boundary.
- rocket leg-2 producer: `route_primary_t4()` @ `mechanic_alteration.py:1962`; C2 constant @ `t4_catalog_v2.py:150`.
- `season_generation_pipeline.py:404-412` (the DDA slot to wire) + `:528` (`build_proxies_surface`).
- spec `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` v3 §4 (role-split), §8-A1 (emission bands).

## Out of scope
- **NO STEP-2 wiring/run until Matt authorizes the run** (ADR-006) AND Gate-1 clears STEP 1.
- Chassis FROZEN, bars/bands FIXED, no magnitude touch.
- NO star-lord validator or gamora sim-site changes (leg-2, done); NO F-f live-wiring (B4-scoped — the two leg-2 Gate-2 followups are B4, not leg-3).

## References
- Matt arc-close batch Item 1 (legs-2-3 lane); jack-ryan coordinated Gate-2 `3bae44a`
- ADR-002, ADR-004 (MIGRATION), ADR-006 (run = external action, Matt-gated), Principle 6, Disc #1, #1.1, #12, #23
- Run-state `batch2-run-state-2026-07-06.md`
