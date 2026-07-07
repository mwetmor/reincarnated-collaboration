# Gate-2 SUBMISSION — 2026-07-07 — rocket leg-2 PRODUCER half (summoner `primary_t4` proxy-family route + shared C2 constant)

**Submitter:** rocket (generation seam — PRODUCE/route side + shared constant)
**For:** jack-ryan DEV-MODE Gate-2 (BLOCK authority)
**Tag:** `rocket/v-batch2-leg2-summoner-emission-route-1` @ engine `996f77d` (verified: tag == HEAD)
**Gate:** DEV-MODE Gate-2, cross-seam certification path (ADR-002 / ADR-004)
**Governs:** dispatch `2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md`; spec `proxy-t4-suite-spec-2026-07-02.md` v3 §1/§4/§4.5/§8
**Design of record:** math note `generation/math/leg2-summoner-primary-t4-routing-math-2026-07-07.md` (`cbac6ed`), Gate-1 PASS-WITH-CONDITIONS (jack-ryan `a5ebd17`)

---

## ⚑ THIS IS THE PRODUCER HALF OF A THREE-SEAM LEG — coordinated Gate-2 requested

Per Gate-1 C1, leg-2 is a THREE-seam lockstep, not two. This submission is the **PRODUCE/route side + the shared C2 constant** ONLY. The other two halves land against the C2 constant this landing defines:

- **star-lord (VALIDATE):** widen the DDA-locked emitter validator (tag `star-lord/v-batch2-dda-lock-validator-widen-1`). IMPORTs `t4_catalog_v2.ACCEPTED_PROXY_PRIMARY_T4`.
- **gamora (CONSUME):** route sites 2/3 (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`) through `route_primary_t4` / the C2 constant (tag `gamora/v-batch2-primary-t4-consume-widen-1`).

**Requested:** a coordinated Gate-2 across the three once star-lord + gamora halves land. This submission may be reviewed on its own PRODUCER merits now (the route + constant + S1/S2 are self-contained and self-proving), with the cross-seam integrity condition (C1) closing when the other two land.

## What landed (5 files, additive-only)

| Condition | Where | Result |
|---|---|---|
| **C2 — single shared constant** | `t4_catalog_v2.ACCEPTED_PROXY_PRIMARY_T4` (`t4_catalog_v2.py:128-171`) | `{PROXY_ASCENSION, PROXY_SOVEREIGNTY, PROXY_FISSION, PROXY_CONVERGENCE, DUAL_PROXY}`; derived from named PROXY constants (not a literal copy); INVERSION + ZONE_CONTROL structurally excluded; import-time guardrail asserts (exactly-5 / subset-of-PROXY-family / two exclusions). The T4 catalog owns the ratified strategy-name constants, so it is the natural home; star-lord + gamora IMPORT it. |
| **Route (predicate P)** | `mechanic_alteration.route_primary_t4(...)` (after `select_proxy_t4:1962`) | `select_proxy_t4` first; non-`None` ⇒ proxy member is `primary_t4`; else `select_primary_t4` (DDA). DDA displaced, not removed. Self-cast stays in `t4_candidates` (spec §4.5 / R3). |
| **C4 / S1 route-correctness** | smoke `generation/notes/leg2_primary_t4_route_smoke_2026_07_07.py` | bone→`PROXY_FISSION`, crypt→`PROXY_SOVEREIGNTY` under DoF-A `focus`; both in `ACCEPTED_PROXY_PRIMARY_T4`; routed member == ranker argmax (route is a faithful pass-through, no re-score). GREEN. |
| **C3 / S2 byte-diff** | same smoke | 8-kit non-summoner corpus × {`[]`, `None`} BYTE-IDENTICAL off the route (full AlterationOutput signature: strategy_type + eta + canonical-JSON strategy_params + manifestation); still `DIRECT_DAMAGE_AMPLIFICATION`. The `$0` no-op-off-summoner-bin proof. GREEN. |
| **C1 — three-seam MIGRATION** | `generation/MIGRATION.md [2026-07-07] LEG-2` | Cross-refs star-lord validator-widen + gamora sites-2/3 consume + shared C2 constant. INTERIM DIVERGENCE WINDOW captured (not merely named): producer route is inert w.r.t. emitted population until leg-3; named closing event = all three landed + coordinated Gate-2. |

**Smoke total:** `leg2_primary_t4_route_smoke_2026_07_07.py` — **14/14 GREEN.** No fights, no full regen, no LLM (closed-form catalog draw; Disc #2 right-tool).

## Regression

`test_proxy_pairing_layer` + `test_proxy_t4_suite_eval` + `test_proxy_t4_suite_strategies` + `test_layer2_dimensions_and_t4_catalog_v2` + `test_two_layer_t4_architecture` + `test_one_realm_bundle_assembler` = **263 PASS.**

## ⚑ Pre-existing failure (NOT leg-2 — captured, Disc #11)

`tests/test_w3_emission_driver.py::TestW3EmissionDriverSmokeRun::test_smoke_dry_run_completes` FAILS on the CLEAN baseline (verified by stashing my two code files OUT: 1 failed / 13 passed, 130s heavy emission smoke). NOT attributable to this landing — leg-2 is additive (a catalog constant + a new route function); the failing test sets `primary_t4: None` in a fixture and never calls the route. This test has a documented pre-existing-failure history (see `2026-07-06-rocket-leg1-summon-int-variation-gate2.md` item 6). Flagged to KR for separate triage.

## F-f disposition (Gate-1 CONFIRMED — re-surfaced to KR as still-B4-scoped)

Leg-2's route does NOT make the GEOMETRY co-draw reachable: `select_proxy_t4` returns a SINGLE argmax member; `ZONE_CONTROL` is structurally outside `PROXY_T4_FAMILY` (separate `GEOMETRY_ZONE_STRATEGIES` registry). `enforce_family_max_one` stays structurally unreachable through the summoner route — NOT wired this landing. Named in MIGRATION.

## Scope honored

- PRODUCER half ONLY: rocket owns site 1 + the C2 constant. NO star-lord validator patch, NO gamora sites-2/3 patch (named for lockstep only).
- **NO leg-3 emission run** — HELD, gates on star-lord + gamora halves (else the run trips the validator OR simulates DDA). leg-3 owes its own Disc #1.1 resource/LLM-cost projection.
- Guards: chassis FROZEN (2.3384× fossil); bars/bands FIXED; NO magnitude touch (`_PROXY_SCAFFOLD_MAGNITUDES` unchanged); η surface untouched (route, not re-score). Auto-committed per CLAUDE.md; NOT pushed (Matt-gated).

## References

- Tag: `rocket/v-batch2-leg2-summoner-emission-route-1` @ `996f77d`
- Math note (Gate-1 PASS-WITH-CONDITIONS): `generation/math/leg2-summoner-primary-t4-routing-math-2026-07-07.md` (`cbac6ed`)
- Gate-1 finding (C1–C4): `agentic_orchestration/qa/findings/2026-07-07-rocket-leg2-summoner-primary-t4-routing-gate1.md` (`a5ebd17`)
- Constant: `t4_catalog_v2.py:128-171` (`ACCEPTED_PROXY_PRIMARY_T4`); Route: `mechanic_alteration.py` (`route_primary_t4`, after `select_proxy_t4:1962`)
- Smoke: `generation/notes/leg2_primary_t4_route_smoke_2026_07_07.py` (14/14 GREEN)
- MIGRATION: `generation/MIGRATION.md [2026-07-07] LEG-2`
- Dispatch: `agentic_orchestration/dispatches/2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md`
