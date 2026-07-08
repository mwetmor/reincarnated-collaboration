# Dispatch — 2026-07-07 — rocket + star-lord CO-DISPATCH — Leg-3 STEP-2: emission wire + pilot run

**From:** knight-rider
**To:** star-lord (export seam — touch-points 1-3) + rocket (generation seam — touch-point 4). **CO-DISPATCH — must co-fire.**
**Approved by:** Matt 2026-07-07 (arc-close batch, Item 1 lane: "rocket: gen-path legs 2–3"). **The pilot RUN itself is a SEPARATE Matt run-authorization (ADR-006 external/compute action).** Gate-1 on the STEP-1 design/projection is CLEARED — jack-ryan `PASS-WITH-CONDITIONS`, finding `qa/findings/2026-07-07-rocket-leg3-summoner-emission-wire-projection-gate1.md` (`bdca4a7`).
**Estimated effort:** star-lord medium (emit-wire + net-new adapter + driver drive + assertion fix + round-trip). rocket small (composer un-gate). Then the two-tier RUN (below).

## Why this is a CO-DISPATCH (the STEP-1 routing correction)
rocket's STEP-1 grep-proved — and jack-ryan Gate-1-ratified vs source — that the leg-3 dispatch's originally-cited wire site `season_generation_pipeline.py:404-412` is **field-def + comment only** (`primary_t4: Optional[dict] = None`, never assigned; grep zero hits). The **REAL DDA emission stamp is `cycle14_wave5_emitter.py:546`** (`primary_t4 = PRIMARY_T4`) — **star-lord's export seam.** 3 of 4 touch-points land in star-lord's `export/`; rocket owns only the composer un-gate. Per role rules (do not patch across seams), STEP-2 co-fires.

## Touch-point inventory (Gate-1 CONFIRMED + seam-attributed vs source)

| # | Touch-point | Seam / owner | File:site (verified) |
|---|---|---|---|
| 1 | Emit-assignment wire + **net-new adapter** `_primary_t4_to_emit_dict` | **star-lord** (export) | `cycle14_wave5_emitter.py:546` |
| 2 | Driver proxy-inclusive drive | **star-lord** (export) | `w3_emission_driver.py` |
| 3 | Identity-glyph assertion → population-aware | **star-lord** (export) | `w3_emission_driver.py:688` |
| 4 | Proxy-bin un-gate (`_DEFERRED_PROXY_BINS` lift for pilot) | **rocket** (generation) | `bc_target_composer.py:97` (gate at `:318`) |

## STEP-2A — WIRE (lands now on this dispatch; NO run until Matt run-auth)

### star-lord (touch-points 1-3)
1. **Emit-wire + net-new adapter @ `cycle14_wave5_emitter.py:546`.** Replace the universal `primary_t4 = PRIMARY_T4` (DDA) stamp with a call to rocket's `route_primary_t4(...)` → then adapt its `AlterationOutput` dataclass return into the emit dict via a **net-new** `_primary_t4_to_emit_dict` adapter (the route fn returns a dataclass, NOT the emit dict — the adapter is genuinely new code, Gate-1-confirmed).
   - **Solo/empty-decl kits:** adapter Clause D = `dict(PRIMARY_T4)` — Gate-1 proved **byte-identical** to today's stamp (the validator `:795-841` does full field-by-field DDA match, so this is provably a no-op for non-proxy kits — Disc #12 preserved).
   - **Proxy-bearing kits:** proxy branch carries member + scope + anchor.
2. **Driver proxy-inclusive drive @ `w3_emission_driver.py`** — drive the emission over the proxy-inclusive pilot population.
3. **Identity-glyph assertion → population-aware @ `w3_emission_driver.py:688`** — the pre-existing smoke failure. `:688` hard-codes `identity_glyph == 300 (BRUISER) and == 400 (GLASS_CANNON)`, a batch-1 population invariant the leg-3 pilot re-populates. **Fix per Gate-1 C4 = option (b): assert non-empty + all-glyphs-valid, do NOT pin an exact split.** This stops encoding a batch-1 invariant into a driver leg-3 re-populates. (Final call is star-lord's as file-owner; (b) is jack-ryan's recommended disposition.)

### rocket (touch-point 4)
4. **Proxy-bin un-gate @ `bc_target_composer.py:97`** (gate enforced at `:318`) — lift `_DEFERRED_PROXY_BINS` for the pilot so proxy-bearing bins compose into the pilot population.
   - **Fold Gate-1 C1 (doc-only):** correct the STEP-1 note's line-ref — `chain_wide_own`/`CHAIN_WIDE_OWN` t4_scope vocab is documented at `cycle14_wave5_emitter.py:67-68` (module docstring valid-values), **NOT `:451`** (that line is `MULTI_ACTIVE`). Substantive claim (existing label, not a new magnitude) is unaffected.

### Acceptance for STEP-2A (wire, pre-run)
- Adapter Clause D byte-identical for solo/empty-decl (cite the validator DDA-match); proxy branch member+scope+anchor correct.
- **Round-trip smoke** (Principle 6): proxy-bearing summoner kit → route → adapter → emit dict → validator ADMITS (proxy-family member) AND read-back intact; non-proxy kit → emit dict byte-identical to `dict(PRIMARY_T4)` → validator ADMITS (DDA lock preserved).
- `w3_emission_driver.py:688` assertion now population-aware (option b); the pre-existing W3 smoke is re-cleared and shown to gate ONLY on the assertion, not the emit path.
- **Carry as explicit STEP-2 acceptance lines (Gate-1 C2, C3 — do NOT let them silently drop):**
  - **C2 (rehearsal-confirm):** measure peak concurrent proxy entities/fight in the dry-run; the ≤7 bound (max_active 3 + FISSION cap 4) is directionally sound but NOT proven until the rehearsal measures it. Report the measured peak.
  - **C3 (A1-coverage measurement):** resolve whether the phase-2 scan already emits a family member into `t4_candidates` (§2.5), or whether leg-3 owes it. Report the answer from the dry-run.
- Regression clean; six non-proxy rooms/populations byte-behavior unchanged.
- **MIGRATION.md lockstep** — star-lord export MIGRATION (emit path now LIVE) + rocket generation MIGRATION (composer un-gate); cross-ref.
- AGENT_STATE.md both seams.
- Tags: `star-lord/v-batch2-leg3-emission-wire-1`, `rocket/v-batch2-leg3-composer-ungate-1`.

## STEP-2B — RUN (fires ONLY on Matt run-auth; TWO-TIER per Gate-1)

**Tier 1 — $0 dry-run pilot (Matt authorizes; ZERO LLM spend, no ADR-006 spend risk):**
- `dry_run_flavor=True` (skips all flavor passes → 0 LLM calls). ≤200-candidate deterministic pilot, **seed 56M**, ~23 min expected / ≤36 min worst-case, 50–80 MB RSS.
- Produces: wire-proof, emission-band measurement (spec v3 §8-A1 — **MEASURED, not a pass/fail threshold**), the C2 peak-entity measurement, the C3 A1-coverage answer.
- **REPORT the band outcome + C2/C3 measurements to KR.** This is the artifact Matt reviews before deciding Tier 2.

**Tier 2 — ≤$10 flavor ceiling (SEPARATE Matt rule; deferred until dry-run bands seen):**
- Fired ONLY if Matt wants named pilot-ready kits. `dry_run_flavor=False`. Expected ~$6.50 (~130 survivors × ~$0.05; monster/gear flavor shared + resumable-skip from prior W3 runs drops actual calls well below the 2,800 ceiling). Key ~$50 → $10 is 20%, no exhaustion risk.
- Stay within the projected envelope; resumable-skip on.

### Acceptance for STEP-2B (run)
- Pilot summoner kits carry proxy-family `primary_t4` (member ∈ `ACCEPTED_PROXY_PRIMARY_T4`).
- §8-A1 bands MEASURED + reported; C2 peak-entity + C3 A1-coverage reported.
- MIGRATION note: emit path exercised on live population.
- Tag `rocket-starlord/v-batch2-leg3-emission-run-1` (co-tag or per-seam run tag).
- **Submit to `qa/pending/` for jack-ryan Gate-2** (certification-path activation + run artifacts).

## Required reading before starting
- **Gate-1 finding** `qa/findings/2026-07-07-rocket-leg3-summoner-emission-wire-projection-gate1.md` (`bdca4a7`) — the touch-point inventory + 4 fold conditions + two-tier posture.
- rocket STEP-1 math note `generation/math/leg3-summoner-emission-wire-and-projection-2026-07-07.md` (`0384dbb`) — the design + projection (fold C1 line-ref).
- Leg-2 coordinated Gate-2 finding `qa/findings/2026-07-07-leg2-summoner-emission-route-coordinated-gate2.md` (`3bae44a`) — the certified machinery STEP-2 activates.
- rocket producer: `route_primary_t4()` @ `mechanic_alteration.py:1962`; C2 constant `ACCEPTED_PROXY_PRIMARY_T4` @ `t4_catalog_v2.py:150`.
- star-lord validator: `validate_class_data()` @ `cycle14_wave5_emitter.py:795-841` (the DDA field-by-field match adapter Clause D must satisfy).
- spec `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` v3 §4 (role-split), §8-A1 (emission bands), §2.5 (`t4_candidates`).

## Out of scope
- **NO RUN (Tier 1 or Tier 2) until Matt run-authorizes** (ADR-006). STEP-2A wire may land on this dispatch; STEP-2B run is Matt-gated.
- **NO Tier-2 flavor spend until Matt separately rules** on it AFTER seeing Tier-1 dry-run bands.
- Chassis FROZEN, bars/bands FIXED, no magnitude touch. Kits vote BARE.
- NO leg-2 machinery changes (certified). NO F-f live-wiring (B4-scoped, not leg-3). NO gamora sim-site changes (leg-2, done).

## References
- Matt arc-close batch Item 1 (legs-2-3 lane); Gate-1 `bdca4a7`; leg-2 coordinated Gate-2 `3bae44a`
- ADR-002, ADR-004 (MIGRATION), ADR-006 (run = external action, Matt-gated), Principle 6 (round-trip), Disc #1, #1.1, #12, #23
- Run-state `batch2-run-state-2026-07-06.md`

## Completion record
*(appended by the executing agents on completion)*

### rocket — touch-point 4 (generation seam) — STOP-and-FLAG (Disc #11) + C1 folded — 2026-07-07

**Verdict on TP4 (composer un-gate): STOP-and-FLAG. The named un-gate site is INERT for the leg-3 pilot path.** I did NOT edit `_DEFERRED_PROXY_BINS`.

- **Disc #11 source-trace:** the leg-3 pilot generation path is `w3_emission_driver.run_w3_emission` → STEP-2 (`w3_emission_driver.py:435`) → `w5r1_generate_kit_candidates` (`season_generation_pipeline.py:784`) → iterates `ENDGAME_ENCOUNTER_CATALOG`. It does **NOT** flow through `bc_target_composer.check_infeasibility` or `_DEFERRED_PROXY_BINS`. `bc_target_composer` is imported only by `bc_target_source.py` (itself an orphan on the pilot path) + one smoke note — never by pipeline/driver/catalog. **Lifting the frozenset @ `:97`/`:318` adds ZERO proxy cells to the pilot** (n_proxy_cells 1→1) while silently changing a different (8-step composer) path's deferral — a duct-tape edit faking an "un-gate landed" signal. This also **corrects my own STEP-1 §3.1 causal claim** (composer gate → 0 proxy kits), which was wrong (Disc #19.1).
- **Real pilot proxy gate = `ENDGAME_ENCOUNTER_CATALOG` curation:** 17 `none` / 1 `light` / 0 `heavy`. The 1 proxy-light cell (`endgame_bc_ranged_medium_variable_int_light`) emits a non-empty `proxies` decl (probe: n_skills=13, n_proxies=1) via the live leg-1 summon path. **So the pilot measures proxy-LIGHT (one cell) with ZERO proxy-HEAVY coverage** — it does NOT "measure nothing." Deferred proxy-heavy cells are absent (never authored), so un-gating them = net-new `EndgameReferenceEncounter` authoring (own math-note + Gate-1) — out of scope for "wire only / chassis FROZEN / kits vote BARE."
- **C1 (doc-only) FOLDED:** STEP-1 math-note §2.3 `chain_wide_own`/`CHAIN_WIDE_OWN` cite corrected `:451` (=`MULTI_ACTIVE`) → `:67-68` (docstring valid-values). Verified against source.
- **⚠ SEQUENCING FLAG:** star-lord's TP1-3 emit-wire IS fully exercisable on the catalog as-is (proxy-light cell present) — the Tier-1 $0 dry-run can prove the wire + emit path end-to-end. BUT it will have **zero proxy-heavy coverage**; the §8-A1 heavy-share band is NOT measurable this pilot. **KR/Matt must rule scope** (routed): (1) run pilot as-is (proxy-light band only; report proxy-heavy NOT-EXERCISED); (2) author deferred proxy cells (separate content wave); (3) re-point driver at `bc_target_cell_sampler.CELL_DEFINITIONS` (has proxy-heavy; star-lord driver-source swap, cross-seam). My read: Option 1 for THIS pilot + Option 2 as named follow-up. NOT self-selected (re-touches §8-A1 band-coverage acceptance).
- **Guards:** ZERO `export/` touch (star-lord's TP1-3 untouched); ZERO composition-behavior change; ZERO chassis/bar/band/magnitude; NO leg-2 machinery change. **NO tag** (`rocket/v-batch2-leg3-composer-ungate-1` not applied — the un-gate it names is inert). **NO MIGRATION entry** (no contract shifted). Committed `db1bbe1` (engine: math-note C1 + AGENT_STATE) + `f9ec4e6` (collab: STOP-flag note) — both **pushed**. STOP-flag note: `agentic_orchestration/rocket/notes/2026-07-07-leg3-composer-ungate-inert-STOP-flag.md`.
- **Star-lord ordering:** star-lord's TP1-3 wire may land independently of TP4 (there is no un-gate for it to sequence after). The Tier-1 $0 dry-run should run on the catalog as-is pending the scope ruling above.
