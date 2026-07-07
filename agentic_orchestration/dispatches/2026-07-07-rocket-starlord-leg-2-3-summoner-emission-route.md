# Dispatch — 2026-07-07 — rocket ∥ star-lord — Gen-path legs 2-3: summoner emission-route (primary_t4 proxy-family routing + DDA-lock validator widen)

**From:** knight-rider
**To:** rocket (generation seam — emit route) ∥ star-lord (export/telemetry seam — validator widen) ∥ **gamora (simulation seam — consume-side re-derive sites, added at Gate-1 C1)**. **CO-DISPATCH — coordinated THREE-SEAM MIGRATION lockstep required.**

> **⚑ GATE-1 STATUS: PASS-WITH-CONDITIONS (jack-ryan, finding `a5ebd17`, 2026-07-07).** Routing code proceeds once C1–C3 (below) are folded. The verdict UPGRADED this from a two-seam to a THREE-seam lockstep — see "Gate-1 conditions" section.
**Approved by:** Matt 2026-07-07 (arc-close batch, Item 1 lane: "rocket: gen-path legs 2–3 (summoner emission path)"). This dispatch is the KR-owed scoping brief rocket's Phase-1 note (§5a) correctly refused to fire blind.
**Estimated effort:** medium (rocket: routing change + math note + Gate-1; star-lord: validator widen + round-trip). Multi-hour, cross-seam certification path.
**Acceptance:** a summoner kit (non-empty `proxy_decls`) emits a `primary_t4` carrying the highest-η **ratified proxy-family** member (ASCENSION / SOVEREIGNTY / FISSION per decl shape) instead of the hard-coded universal DDA; the DDA-locked emitter validator is widened to admit proxy-family `primary_t4` values without regressing the non-summoner DDA lock; both sides land in coordinated MIGRATION lockstep; leg-3 emission run produces pilot-ready summoner kits into the four-family instrument. **Leg-3 completion is the unblocking event for star-lord's Leg C re-fire + gamora's summoner proxy-T4 sim-eval** (Matt's Item 1).

## Context — the deferred cross-seam obligation now going live

rocket's B1-REBASE Phase-1 v3 note (`generation/math/proxy-t4-b1-rebase-phase1-v3-refire-2026-07-07.md`, `a5adcf1`) §1 + §5a establishes the exact scope:

- **Leg 1 (LANDED):** summon gen-path wire-in — a summoner cell emits a non-empty `proxies` decl with all sim-consumable fields. Magnitudes are SCAFFOLD (gamora's lane).
- **Leg 2 (THIS DISPATCH — the primary-T4 routing gap):** `select_primary_t4` (`mechanic_alteration.py:1831`) is hard-coded **ALWAYS-DDA** (`eta=1.0`, universal) and never consults `select_proxy_t4` (which exists at `:1876`) or `proxy_decls`. So a summoner today emits `primary_t4 = DirectDamageAmplification` — the exact v1 bug spec v3 §1 names ("a summon-bearing kit receives a capstone that multiplies its smallest contribution surface — mechanically dead weight"). Leg 2 routes proxy-bearing kits through `select_proxy_t4` so `primary_t4` carries the highest-η ratified proxy-family member; self-cast T4s stay in `t4_candidates` (spec v3 §4.5 bands).
- **Leg 3 (THIS DISPATCH — the emission run):** produce pilot-ready summoner kits (real proxy-family `primary_t4` + varied kits) into the four-family instrument.

**The cross-seam block (gamora's `simulation/MIGRATION.md:8371`, VERBATIM):** *"When B4 wires `select_proxy_t4` … into the emission pipeline, a proxy-bin kit's `primary_t4` will carry a ratified catalog constant … the DDA-locked emitter validator must widen."* That validator lives on star-lord's emit surface. rocket does not patch it (AGENTS.md seam boundary) — hence the co-dispatch. A coordinated MIGRATION lockstep (rocket emit + star-lord validator + gamora consume) is owed.

## Coordination — who owns what

- **rocket (PRODUCE/route side):** the `select_primary_t4` → `select_proxy_t4` routing at `mechanic_alteration.py:1831`; the leg-2 math note; the leg-3 emission run. Do NOT touch star-lord's validator.
- **star-lord (VALIDATE/emit side):** widen the DDA-locked emitter validator to admit proxy-family `primary_t4` values for proxy-bearing kits, WITHOUT loosening the DDA lock for non-summoner kits (the lock must still catch a stray non-DDA `primary_t4` on a kit with empty `proxy_decls`). Round-trip smoke required. Do NOT touch rocket's routing.
- **gamora (CONSUME/re-derive side — added at Gate-1 C1):** two sim sites re-derive `primary_t4` via the old always-DDA `select_primary_t4` today — `gauntlet_sim.py:2267` + `unified_calibration_loop.py:3577`. Without a matching consume-side patch, a summoner kit would **emit** a proxy member but be **simulated** as DDA (emitted-vs-simulated divergence — the leg's integrity failure). gamora routes these two sites through the same predicate P (or consumes the emitted `primary_t4` directly rather than re-deriving), so sim reflects the emitted kit. Do NOT touch rocket's emit route or star-lord's validator.
- **Serialize the landing:** rocket's routing change is the PRODUCER; star-lord's validator-widen must admit what rocket emits; gamora's sim must simulate what rocket emits. Coordinate the exact accepted value-set via a shared MIGRATION entry (C2 constant) BEFORE any side tags. If rocket's math note reshapes the accepted set, star-lord's widen AND gamora's re-derive track it in lockstep.

## Gate-1 conditions (jack-ryan PASS-WITH-CONDITIONS, `a5ebd17`) — FOLD before routing code lands

- **C1 (load-bearing — the leg's integrity condition):** THREE-seam MIGRATION lockstep, not two. The MIGRATION must cross-ref gamora's consume-side patch of sites 2/3 (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`) — OR explicitly state a known-transient divergence window if gamora's patch is separately sequenced. A NAMED obligation is not a CAPTURED one; the divergence must be closed or documented, not just cited.
- **C2:** freeze `ACCEPTED_PROXY_PRIMARY_T4` = `{PROXY_ASCENSION, PROXY_SOVEREIGNTY, PROXY_FISSION, PROXY_CONVERGENCE, DUAL_PROXY}` as a SINGLE shared MIGRATION constant all three seams build against (rather than three independent copies of the set).
- **C3:** the `$0` S2 byte-diff (non-summoner population byte-identical off the route) must be GREEN and CITED at Gate-2 — not merely named as available.
- **C4 (INFO):** add the S1 route-correctness unit case (bone→FISSION, crypt→SOVEREIGNTY under DoF-A `focus`) and cite at Gate-2.
- **Confirmed at Gate-1 (no action):** F-f GEOMETRY max-1 stays structurally unreachable through the summoner route (ZONE_CONTROL isolated in `GEOMETRY_ZONE_STRATEGIES`) — rocket's "re-surface to KR as still-B4-scoped" disposition is correct. No decisions-log conflict (governed by the 2026-07-06 Matt Option-1/batch-2 authorization).

## Required reading before starting
**rocket:**
- your own `generation/math/proxy-t4-b1-rebase-phase1-v3-refire-2026-07-07.md` §1, §2, §5a (the scope you already captured).
- `mechanic_alteration.py:1831` (`select_primary_t4` — the ALWAYS-DDA site) + `:1876` (`select_proxy_t4` — the existing selector to route into).
- `season_generation_pipeline.py:404-409` (the "DDA universal; all kits" emission assignment).
- spec `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` v3 §1 (the v1 bug), §4 (role-split), §4.5 (self-cast band).

**star-lord:**
- `simulation/MIGRATION.md:8371` (gamora's producer-side flag — the authoritative handoff for the validator-widen).
- your DDA-locked emitter validator (locate the exact site that asserts `primary_t4 == DirectDamageAmplification` on emit).
- rocket's Phase-1 note §5a (the routing change your validator must admit).

## Math/design-before-code (Discipline #1 — rocket authors BEFORE routing code)
rocket authors a leg-2 math note covering:
- The exact routing predicate (proxy_decls non-empty → route through `select_proxy_t4`; empty → DDA as before).
- The η/band consequence: which proxy member a summoner draws given decl shape, and the spec v3 §4 role-split + ≥90%/≥60% (§8 A1) emission-band consequence. **This is a balance/emission-routing change — the critique pair prices the role-split consequence.**
- The accepted `primary_t4` value-set star-lord's validator must admit (the shared contract).
- Refutation conditions (Disc #23 framing audit) + resource-bounds if the leg-3 run is compute-heavy (Disc #1.1).
- **Gate-1 (jack-ryan DESIGN-MODE) reviews the leg-2 math note BEFORE routing code lands.**

## Cross-seam contract change? (Principle 6 gate — YES)
**YES — emit-surface contract change.** The emitted `primary_t4` value for a whole kit class (summoners) changes from DDA → a proxy-family constant.
- **MIGRATION.md REQUIRED on BOTH seams in lockstep:** rocket's generation MIGRATION (producer) + star-lord's export/telemetry MIGRATION (validator/consume), cross-referencing the shared accepted value-set.
- **Round-trip smoke (star-lord):** a summoner kit with proxy-family `primary_t4` → emit → validator admits → persist/read-back intact; AND a non-summoner kit with empty `proxy_decls` and a stray non-DDA `primary_t4` → validator STILL rejects (lock preserved where it should hold).

## Scope
**rocket:**
- [ ] Leg-2 math note first (all bullets above), committed before routing code. → **Gate-1 (jack-ryan DESIGN-MODE).**
- [ ] Route proxy-bearing kits (`proxy_decls` non-empty) through `select_proxy_t4` so `primary_t4` carries the highest-η ratified proxy-family member; empty-decl kits keep DDA.
- [ ] Self-cast T4s remain in `t4_candidates` (spec v3 §4.5).
- [ ] generation MIGRATION.md entry (the accepted value-set contract; cross-ref star-lord's).
- [ ] Leg-3 emission run: pilot-ready summoner kits into the four-family instrument.
- [ ] AGENT_STATE.md updated. Tag: `rocket/v-batch2-leg2-summoner-emission-route-1` (routing) + `rocket/v-batch2-leg3-summoner-emission-run-1` (run).
- [ ] Submit tagged commit(s) to `qa/pending/` for jack-ryan Gate-2 (certification/cross-seam path).

**star-lord:**
- [ ] Widen the DDA-locked emitter validator to admit proxy-family `primary_t4` for proxy-bearing kits (per the shared MIGRATION contract).
- [ ] Preserve the DDA lock for non-summoner (empty-decl) kits — round-trip smoke BOTH cases GREEN.
- [ ] export/telemetry MIGRATION.md entry in lockstep with rocket's.
- [ ] AGENT_STATE.md updated. Tag: `star-lord/v-batch2-dda-lock-validator-widen-1`.
- [ ] Submit tagged commit to `qa/pending/` for jack-ryan Gate-2 (emit-boundary change).

**gamora (consume-side, Gate-1 C1):**
- [ ] Route sites 2/3 (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`) through predicate P (or consume the emitted `primary_t4` directly) so sim simulates what rocket emits — close the emitted-vs-simulated divergence.
- [ ] Build against the shared `ACCEPTED_PROXY_PRIMARY_T4` constant (C2).
- [ ] simulation MIGRATION.md entry in lockstep with rocket + star-lord.
- [ ] AGENT_STATE.md updated. Tag: `gamora/v-batch2-primary-t4-consume-widen-1`.
- [ ] Submit tagged commit to `qa/pending/` for jack-ryan Gate-2 (sim-consume of a changed emit contract).

## Out of scope (FROZEN / deferred / separate)
- **NO kit-side chassis constant changes** (2.3384× fossil FROZEN).
- **NO bar / band moves** (fit-direction law — FIXED inputs).
- **DoF-A (A3 energy-designation)** — being resolved IN PARALLEL by gandalf (summoner energy designation design call). It affects which member a SPECIFIC demo fixture selects (SOVEREIGNTY gate), NOT the routing mechanism. Leg 2 builds the route independent of DoF-A; the demo-fixture energy value lands separately once gandalf/Matt rules. **Do not block leg 2 on DoF-A.**
- **DoF-B (F-f GEOMETRY max-1 live call site)** — rocket's §3: the live call site rides THIS wiring (`select_proxy_t4` → emission makes the GEOMETRY co-draw reachable). Once leg-2 routing lands, the `enforce_family_max_one` consumer (`t4_catalog_v2.py:159-215`, function-complete/W0-tested) SHOULD be wired into the selection path so the F-f invariant becomes a live-consumer assertion (gamora ext §3 branch 1). rocket names this obligation in the leg-2 MIGRATION; wire it if the routing makes GEOMETRY co-draw reachable, else re-surface the F-f BLOCK to KR.
- **NO magnitude touch** (`_PROXY_SCAFFOLD_MAGNITUDES` unchanged — gamora's lane).

## References
- rocket Phase-1 v3 note `a5adcf1` §1/§2/§5a; gamora `simulation/MIGRATION.md:8371`; spec v3 §1/§4/§4.5/§8
- ADR-002 (tiered approval), ADR-004 (MIGRATION), Principle 6 (round-trip), Disciplines #1, #1.1, #3, #11, #12, #23
- Run-state `batch2-run-state-2026-07-06.md` (Item-1 gen-path lane; leg-3 = unblocking event for star-lord Leg C + gamora summoner proxy-T4)
