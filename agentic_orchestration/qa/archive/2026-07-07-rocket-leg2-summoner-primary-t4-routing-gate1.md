# Gate-1 request (DESIGN-MODE) — rocket: leg-2 summoner `primary_t4` proxy-family routing (math-before-code)

**Filed by:** rocket, 2026-07-07 (arc-close batch, Item 1 — gen-path legs 2-3, rocket emit-route half).
**Critique pair:** jack-ryan (DESIGN-MODE technical/process) + gandalf (design — the emission-band consequence is a balance-surface pricing).
**Math note under review:** `reincarnated-engine/src/reincarnated/generation/math/leg2-summoner-primary-t4-routing-math-2026-07-07.md`.
**Co-dispatch (GOVERNS):** `agentic_orchestration/dispatches/2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md` (rocket emit-route ∥ star-lord validator-widen — coordinated MIGRATION lockstep).
**Governing spec:** `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` **v3** §1/§4/§4.5/§8.
**Producer-side handoff:** gamora `simulation/MIGRATION.md:8371` (the DDA-lock validator-widen flag).

## Why Gate-1 BEFORE routing code (not just Gate-2)

Leg-2 is a **cross-seam certification-path change** (ADR-002 / ADR-004): the emitted `primary_t4` value
for a whole kit class (summoners) changes DDA → a proxy-family constant, and star-lord's DDA-locked
emitter validator must widen to admit it in lockstep. The co-dispatch requires Gate-1 of this math note
BEFORE any routing code lands (math-before-code). **NO routing code has landed** — this note is the
before-code artifact. **NO star-lord validator touch, NO gamora sim-site edit** — I own only the route
side.

## What the note establishes (the two things the pair rules — note §7)

1. **The routing predicate P (note §1) + the accepted value-set contract (note §3):** proxy_decls
   non-empty → route through `select_proxy_t4` (`mechanic_alteration.py:1895`); empty → DDA as before
   (`select_primary_t4:1831`, byte-identical no-op off the summoner bin — S2). The accepted proxy
   `primary_t4.strategy_type` set the validator must admit is EXACTLY:
   `{PROXY_ASCENSION, PROXY_SOVEREIGNTY, PROXY_FISSION, PROXY_CONVERGENCE, DUAL_PROXY}`
   (`t4_catalog_v2.py:55-60`), with **`PROXY_INVERSION` and `ZONE_CONTROL` deliberately EXCLUDED**
   (INVERSION deferred wholly / not in `PROXY_T4_FAMILY`; ZONE_CONTROL is GEOMETRY-family, not
   proxy-gated). DDA stays admissible on both branches (summoner no-member-clears fallback). The widen
   is **conditional on `proxy_decls` non-empty** — a stray non-DDA on an empty-decl kit STILL rejects.
2. **Price the emission-band consequence (note §2.1):** confirm the spec §4.5 / §8 A1 ≥90% (heavy) /
   ≥60% (light) family-share bands are a **measured leg-3 outcome** of a deterministic argmax route
   (my framing), NOT a threshold leg-2 enforces; and confirm the self-cast-T4s-stay-in-`t4_candidates`
   disposition (spec §4.5 / R3 one-primary-per-kit) is a ratified rule, not a new design choice.

## Load-bearing seam fact for the pair (note §1.1)

`primary_t4` is derived at THREE sites: emit (`season_generation_pipeline.py:404-412`, **rocket** —
routes), and two sim re-derivations (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`,
**gamora**). If rocket routes site 1 but gamora's sites 2/3 keep re-deriving DDA, the emitted and
simulated capstones diverge. The note NAMES sites 2/3 as gamora consume obligations for the
MIGRATION-lockstep; rocket does not patch them. The pair should confirm this coordination is captured
(it is the cross-seam integrity condition of the whole leg).

## F-f disposition folded (co-dispatch out-of-scope item)

The note (§6) rules leg-2's route does NOT make the GEOMETRY co-draw reachable — `select_proxy_t4`
returns a SINGLE argmax member and ZONE_CONTROL is excluded from `PROXY_T4_FAMILY`. So `enforce_family_max_one`
stays structurally unreachable through the summoner route → **F-f re-surfaced to KR as still-B4-scoped**
(per the co-dispatch "else re-surface the F-f BLOCK to KR"). Confirm this disposition.

## Refutation conditions named (Disc #23 / #19.1 — note §4)

Cheapest refuting test per claim: S2 no-op-off-summoner → schema/byte diff ($0, deterministic); S1
drawn-member-matches-decl → unit assertion (existing 77-test surface + new S1 case); S3 lock-preserved
→ star-lord round-trip (his half); bands → leg-3 run (re-opens η-surface not the route on fail).

## Guards

Kit-side chassis FROZEN (2.3384× fossil); bars/bands FIXED; η surface untouched (route, not re-score);
NO magnitude touch (`_PROXY_SCAFFOLD_MAGNITUDES` unchanged). ZERO production code this session (math
note only). Auto-committed (CLAUDE.md in-scope work-product); NOT pushed (Matt-gated).

## On Gate-1 ratification

The leg-2 routing code (emit site 1) + the generation MIGRATION lockstep entry (cross-ref star-lord's
validator MIGRATION) fire from the co-dispatch; leg-3 (emission run) gates on leg-2 landing + the
four-family instrument. Tags per dispatch: `rocket/v-batch2-leg2-summoner-emission-route-1` (routing) +
`rocket/v-batch2-leg3-summoner-emission-run-1` (run).
