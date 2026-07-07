# Gate-2 SUBMISSION — 2026-07-07 — gamora leg-2 CONSUME half (sim `primary_t4` re-derive sites route via shared `route_primary_t4`)

**Submitter:** gamora (simulation seam — CONSUME/re-derive side, sites 2/3)
**For:** jack-ryan DEV-MODE Gate-2 (BLOCK authority)
**Tag:** `gamora/v-batch2-primary-t4-consume-widen-1` @ engine `8d8e76b` (verified: tag == the commit)
**Gate:** DEV-MODE Gate-2, cross-seam certification path (ADR-002 / ADR-004) — sim-consume of a changed emit contract
**Governs:** dispatch `2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md` (Gate-1 C1, gamora scope block)
**Design of record:** math note `simulation/math/leg2-primary-t4-consume-widen-2026-07-07.md`, Gate-1 C1 (jack-ryan finding `a5ebd17`)

---

## ⚑ THIS IS THE CONSUME HALF OF THE THREE-SEAM LEG — coordinated Gate-2 requested

Per Gate-1 C1, leg-2 is a THREE-seam lockstep. This is the **CONSUME/re-derive side** — it closes the emitted-vs-simulated divergence C1 names. It builds against rocket's LANDED route + C2 constant (does NOT touch them) and is co-reviewed with star-lord's validator-widen half.

- **rocket (PRODUCE, LANDED):** `route_primary_t4()` `mechanic_alteration.py:1972`, C2 `ACCEPTED_PROXY_PRIMARY_T4` `t4_catalog_v2.py:150-171` (tag `rocket/v-batch2-leg2-summoner-emission-route-1` @ `996f77d`). Submission `2026-07-07-rocket-leg2-summoner-emission-route-gate2.md`.
- **star-lord (VALIDATE):** DDA-lock validator widen (tag `star-lord/v-batch2-dda-lock-validator-widen-1`). IMPORTs the same C2 constant.
- **gamora (CONSUME — THIS):** routes sites 2/3 through the SAME `route_primary_t4`.

**Requested:** coordinated Gate-2 across the three once star-lord's half lands. This CONSUME half may be reviewed on its own merits now — it is self-contained (routes through rocket's landed function; S2 + C1 self-proving).

## The divergence this CLOSES (C1 — the integrity condition rocket's interim window flagged)

Rocket's producer submission (item C1) captured an INTERIM DIVERGENCE WINDOW: the producer route is inert w.r.t. the emitted population until leg-3, and the CONSUME side (sites 2/3) still re-derived DDA. **This submission closes the consume side of that window.** Without it, a summoner kit would EMIT a proxy-family capstone but be SIMULATED as dead-weight DDA. Both sim sites now route through the SAME `route_primary_t4` the emit path calls, so sim's `primary_t4` derivation is **provably identical to emit's** (shared derivation site, not a mirror). The `simulation/MIGRATION.md:8371` v1.83 producer flag — the original NAMED obligation — is now CLOSED (a named obligation made captured).

## What landed (6 files, additive/routing-only — NO star-lord/rocket seam touch)

| Condition | Where | Result |
|---|---|---|
| **C1 route — site 2** | `gauntlet_sim.py:2279` (`build_variant_enumeration_configs`) | `select_primary_t4(...)` → `route_primary_t4(..., proxy_decls=build_proxies_surface(kit.skills))`. |
| **C1 route — site 3** | `unified_calibration_loop.py:3592` (UCL two-layer `primary_dda`) | same route + same `proxy_decls` source. Docstring + failure-log tag updated to `route_primary_t4`. |
| **C2 — imported, not copied** | smoke imports `t4_catalog_v2.ACCEPTED_PROXY_PRIMARY_T4` | membership assert on the summoner branch; INVERSION + ZONE_CONTROL excluded. |
| **Byte-faithful `proxy_decls`** | `build_proxies_surface(kit.skills)` | the emit source VERBATIM (`season_generation_pipeline.py:528`), so sim-site decls == emit-side decls byte-for-byte. |
| **Math-before-code (Disc #1)** | `simulation/math/leg2-primary-t4-consume-widen-2026-07-07.md` | equivalence proof (§1) + byte-faithful sourcing (§1.2) + S2 invariance proof (§2) + refutation/framing-audit (§3). |
| **C3 / MIGRATION lockstep** | `simulation/MIGRATION.md [2026-07-07] LEG-2 CONSUME-side` | cross-refs C2 + rocket's `[2026-07-07] LEG-2` + star-lord's half; CLOSES the v1.83:8371 window. |

## Smoke (Disc #2) — GREEN

`simulation/notes/leg2_primary_t4_consume_smoke_2026_07_07.py` (deterministic, no fights, no full regen, no LLM):

- **S2 non-summoner byte-identity (C3): 8/8** — for an 8-kit non-summoner corpus, `route_primary_t4(proxy_decls=[])` returns a primary_t4 BYTE-IDENTICAL (strategy_type + preferred_encounter_type) to the pre-leg-2 `select_primary_t4` path; all still `DIRECT_DAMAGE_AMPLIFICATION`. The no-op-off-summoner-bin proof, sim-side.
- **C1 summoner route** — demo necromancers under DoF-A `focus`: bone→`PROXY_FISSION`, crypt→`PROXY_SOVEREIGNTY`, gravecaller→`PROXY_SOVEREIGNTY`; all ∈ `ACCEPTED_PROXY_PRIMARY_T4`. Source-fidelity: sim-site `build_proxies_surface([summon_skill])` == the fixture's own proxies surface.
- **C2 anchor** — `ACCEPTED_PROXY_PRIMARY_T4` imported (not copied); len==5; INVERSION + ZONE_CONTROL excluded.

Both sim modules AST-parse + import clean post-edit.

## Cert-baseline byte-intact — this is a DERIVE-SITE ROUTING FIX, not a balance change

The current certified population is entirely non-summoner (no summon skills emitted) → every certified kit hits `build_proxies_surface → []` → `route_primary_t4` falls back to `select_primary_t4` with identical args → byte-identical. **No certified band moves; no magnitude/bar/band/chassis touch.** Disc #12: NO semantic shift on live behavior — the DDA fallback is byte-preserved; the only behavior change is on proxy-bearing kits, which do not reach the certified population until leg-3 (rocket's separate fire). Chassis FROZEN, bars/bands FIXED assertion holds by construction.

## Out of scope (honored)

NO change to rocket's route/constant or star-lord's validator. NO leg-3 emission run. NO magnitude touch. NO new fight-result field / telemetry schema change (consume-side derive routing only).

## Regression / dependency note

The S2 non-summoner-`None`→DDA invariance leans on the existing passing pin `w0_prereqs_smoke_2026_07_03.py:207` (`select_proxy_t4(..., proxy_decls=[]) is None`) — rocket's landed surface, unchanged. My smoke re-proves the fallback end-to-end (8/8). No new production fight-path regression surface introduced (routing at two config-build sites; the downstream `strategy_params` read is unchanged).
