# Finding — 2026-06-16 — Wave-4 additive pair: companion-generation pass + D4 proxy-port (Axis-2A)

**Reviewer:** jack-ryan (DEV-MODE / Gate-2)
**Severity:** PASS-WITH-INFO (both items) — no BLOCK, no WARN
**Targets:**
- Item 1 — `rocket/v-companion-gen-1` (code `52c773d`, math-note `e5d9c6a`, AGENT_STATE `5578b71`)
- Item 2 — `gamora/v-d4-proxy-port-axis2a-1` (code `fea7e55`, AGENT_STATE `4a28f3b`)
**Developers:** rocket (Item 1), gamora (Item 2)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** #1 (math-before-code), #2/#2.1 (smoke pre-registration), #11 (empirical inspection / mechanism diagnosis), #12 (semantic-shift discipline)
**Run context:** AUTHORIZED AUTONOMOUS RUN; KR coordinating; Matt not in loop. gandalf reviews design-conformance in parallel — this is an independent technical verdict.

---

## VERDICTS

| Item | Verdict | Surfaces to Matt? |
|---|---|---|
| 1 — rocket companion-generation pass | **PASS-WITH-INFO** | No (PASS is terminal) |
| 2 — gamora D4 proxy-port (Axis-2A) | **PASS-WITH-INFO** | No (PASS is terminal). Decisions-log entry AUTHORED for the WIRED-DEFERRED→BUILD shift. |

**Nothing in this review surfaces to Matt as a BLOCK or FAILED gate.** Two scope-PARKs are flagged for KR awareness (production flag-flip; real-Hall population) — both are correctly-parked design/scope questions, NOT correctness gaps.

---

## Item 1 — rocket companion-generation pass — PASS-WITH-INFO

### What I found
A bounded, LLM-free, additive companion-record generator (`companion_generation.py`) that makes the Q8 "Hall-of-Heroes ally" path runnable + measurable. I verified rocket's claims against the source rather than trusting the smoke. The Q8 68-cell table is transcribed **verbatim and faithfully** from the FINAL matrix: I confirmed 22 player rows, 68 total cells (20 rows × 3 + 2 bond rows × 4 = 68, matching FINAL §6's 7×3+4×3+3×3+6×3+2×4 budget exactly), all 23 referenced strategy strings resolve to real `t4_catalog_v2` constants (zero typo-masked phantom strategies), the full diagonal is rejected by an import-time assert, the RETRIBUTION_ENGINE/MONSTER_PACT anti-synergy CUT (FINAL §5 #3) is honored (RETRIBUTION row excludes MONSTER_PACT; PERSISTENCE row keeps it — the precise directional pair holds), and PROXY_INVERSION carries the sanctioned summoner-damage exception (FINAL §5 #1). The season-1 refusal is a real hard guard (`generate_companion_record` raises `ValueError` for `season_index < MIN_COMPANION_SEASON=2`), not a comment — verified live. The §6.2 NPC caps in `NPC_CAPS` match the Session-2 §6.2 table value-for-value (damage_amp 1.15, cc_duration_mult 1.25, survivability_mod 0.10, resource_gen_mod 0.10, aoe_radius_mod 0.15, enemy_cc_mult 1.0); every emitted modifier sits at-or-below its cap and `_assert_caps` enforces it at generation. Determinism is seed-real (keyed on `(player_strategy, season_index, seed)`). Smoke: 12/12 checks PASS including the negative asserts (invalid-cell + season-1 refusal). The four PARKED JCs (JC-1 real-Hall population; JC-2 measured-BC §6.3 mapping = gamora downstream; JC-3 curated naming; JC-4 corpus size) are all genuine design/scope handoffs, correctly parked — none is a correctness gap.

### Rationale
Math-note precedes code and pre-registers the schema, draw rule, cap derivation, and acceptance asserts (Discipline #1, Principle #1). Smoke pre-registers per-role bins and exercises every role-class deterministically rather than depending on a random draw landing on rare roles (Discipline #2.1, Principle #2). The transcription is the single-source-of-truth import the FINAL matrix specifies (no re-derivation; strategy strings imported from `t4_catalog_v2`). Additivity holds: a new module, no consumer rewired, no §6.2-cap or Q8-matrix change, no LLM, no sim/balance_loop wire. JC-2 is correctly a generation↔measurement handoff — §6.3 keys on MEASURED BC bins which exist only downstream of gamora; the role-class projection is a sound, cap-bounded, deterministic generation-time substitute, not a new balance lever (every magnitude is a fraction of an already-ratified cap).

### INFO (non-blocking, actionable; record for later)
- **INFO-1 (synthetic Hall provenance is honestly flagged):** records carry `hall_form.is_synthetic=True` and `provenance` strings. This is the correct honest marker for the JC-1 bounded-synthetic posture. **Action (rocket, when JC-1 resolves):** ensure the real-Hall wire-in flips `is_synthetic=False` and that any downstream consumer (gamora Session-5 gauntlet) gates on this flag so synthetic records never leak into a balance verdict. No action now.
- **INFO-2 (3 of 25 player rows have no Q8 row — by design):** 22 rows, not 25. The 3 absent rows match FINAL §2 (which enumerates 22 valid-cell rows; the diagonal note covers all 25). `valid_companions` raises for a player strategy with no row — correct fail-loud. **Action:** none; noting for the record that "22 rows" is the expected, FINAL-faithful count, not a transcription omission.
- **INFO-3 (MIGRATION deferred — correctly):** no MIGRATION.md yet because no downstream consumer exists (the wire-in is gamora's Session-5 seam). **Action (rocket/gamora):** author the record-schema MIGRATION when the first consumer is wired. No action now.

### Action
- [x] Developer (rocket): none required — PASS. INFO items are forward-notes for the JC-1/Session-5 wire-in.
- [ ] Matt: none (PASS is terminal per run charter).

---

## Item 2 — gamora D4 proxy-port (Axis-2A discrimination, arity=8) — PASS-WITH-INFO

### What I found
A flag-gated, additive population-tracking port that makes Axis-2A (Proxy Density) discriminate (solo / proxy-light / proxy-heavy) where W-D left it inert. I verified the three load-bearing Discipline-#12 claims at the code level, not the smoke level. **(a) Production-unchanged-with-flag-OFF:** I re-read the code path — `track_proxy_population` defaults False; with it off, `_build_player_proxies` is never called, the per-tick block is gated `if self._track_proxy_population and self._proxies`, the accumulators stay 0, `mean_active_proxy_count` resolves to 0.0, and `measure_axis2a_proxy` bins `solo`. The OFF path executes ZERO proxy code — genuinely byte-identical, not merely smoke-asserted. The D4 changeset touches exactly 3 production files (`spatial_engine.py` +106, `spatial_telemetry.py` +10, `spatial_bc_measurement.py` +38) and 1 test file; `proxy_combatant.py`, `fight_engine.py`, and `balance_loop` are NOT in the changeset, so the 1D kernel is structurally untouched. **(b) Test supersession is legitimate:** `test_axis2a_proxy_is_wired_deferred_not_fabricated` was renamed to `test_axis2a_proxy_no_proxies_is_honest_measured_zero` using the SAME K5 no-proxy fixture — the assertion changed (`measurable=False`/WIRED-DEFERRED → `solo`/`measurable=True`/BUILD/value=0.0) because the MECHANISM changed, and two NEW discrimination tests were ADDED. This is a contract upgrade matching a deliberate semantic shift, not a weakening to make a regression pass; the frozen pre-D4 consume-boundary fixture still asserts `cell[2] == "none"` and passes (export contract untouched). **(c) measurable=False→True with flag ON is a sound, flag-gated semantic shift:** `measurable=False` meant "the engine cannot count proxies"; the mechanism now exists, so a no-proxy kit's honest reading is a measured-zero (`solo`/measurable=True), not a deferral. The port is correctly scoped as a COUNT instrument (the COUNT≠CONTRIBUTION cut): proxies apply no damage to mobs and take no spatial position — verified in `_step_proxy_population` (attrition is the reused balance-neutral 1D lifetime model only; no DPS term). arity=8 holds (`AXIS_ORDER` unchanged length 8; K5 the existing canary discriminates; no new reference kit). Smoke 6/6 PASS; W-D BC + consume-boundary 20/20 PASS; spatial scenario suite 27/27 PASS.

### Rationale
Discipline #12 (Principle #5 severity / Principle #4 decisions-log-as-truth) requires a meaning-changing measurement to be flag-gated byte-identical-by-default AND recorded as a gated disposition change — both satisfied (off-path inert; decisions-log entry authored). Discipline #11 (mechanism diagnosis): the COUNT≠CONTRIBUTION reframe is the correct diagnosis — the lock §3.3 coordinate is a population count, position/DPS-independent, so the port shrinks from a movement-AI-scale combat-participant rework to a contained per-tick accumulator; the relief-valve cut (W-D §1.2) is applied honestly, not as a half-build. Math-before-code holds (Discipline #1; math note `d4-proxy-port-axis2a-2026-06-16.md` precedes the code with the scope cut, flag-gated build plan, resource-bounds, and the explicit #12 PARK). Cross-seam impact (Principle #3): the exported 8-tuple schema is unchanged; the new `mean_active_proxy_count` is internal-to-seam (not in the star-lord export), so no MIGRATION is required and star-lord's contract is untouched — verified by the passing consume-boundary fixture.

### INFO (non-blocking, actionable; record for later)
- **INFO-1 (the production flag-flip is a real future #12 gate — correctly PARKED):** flipping `track_proxy_population` ON for the production balance-loop / archive re-measurement WOULD shift the production 2A-slot value for proxy-bearing kits — a production-measurement #12 shift. This commit keeps it off-default and PARKS the flip. **Action (KR/Matt, when adoption is wanted):** the flip + archive re-measurement is a separate gated call that must author its own supersession note. Logged in the decisions-log "Decisions to revisit." No action now.
- **INFO-2 (proxy declarations are harness-injected, not yet stamped by production generation):** the discrimination is proven via harness-injected `proxies` fixtures; real generation does not yet stamp `proxies` on kits. This is correctly a rocket reference-kit/generation follow-on, not a D4 gap (D4 only needs the mechanism + a harness-injected proof). **Action (rocket, if/when a proxy-differentiated reference kit is added):** stamp `proxies` on the relevant kit(s). No action now. *(Note the natural seam-pairing with Item 1's JC-1/Session-5 wire-in — both items leave the real-data population to the same downstream handoff.)*
- **INFO-3 (F1 geometry-blindness untouched — correctly out of scope):** D4 sidesteps F1 via explicit `geometry_type` fixtures, as W-D did. F1 remains a separate production #12 shift for Matt. **Action:** none here; F1 is its own workstream.

### Action
- [x] Developer (gamora): none required — PASS.
- [x] jack-ryan: decisions-log entry AUTHORED — "2026-06-16 (measurement semantic shift): Axis-2A WIRED-DEFERRED → BUILD" in `reincarnated-engine/design/decisions/decisions-log.md`, citing the flag-gating that keeps production inert. "Decisions to revisit" updated with the production-promotion park.
- [ ] Matt: none (PASS is terminal). The decisions-log entry records the gated shift for the record; the production flag-flip is the only Matt-gated future step and it is PARKED, not requested here.

---

## References
- `~/Games/reincarnated-engine/src/reincarnated/generation/companion_generation.py` (Item 1 code, `52c773d`)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/companion-generation-pass-2026-06-16.md` (Item 1 math note)
- `~/Games/reincarnated-engine/scripts/rocket_companion_generation_smoke_2026_06_16.py` (Item 1 smoke — 12/12 PASS)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (Item 2 — flag, `_build_player_proxies`, `_step_proxy_population`, per-tick gate L1687, result thread L1827)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_bc_measurement.py` (Item 2 — `measure_axis2a_proxy` L182, BUILD/measurable=True)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py` (Item 2 — `mean_active_proxy_count` field)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/d4-proxy-port-axis2a-2026-06-16.md` (Item 2 math note)
- `~/Games/reincarnated-engine/scripts/gamora_d4_proxy_port_smoke_2026_06_16.py` (Item 2 smoke — 6/6 PASS)
- `~/Games/reincarnated-engine/tests/test_wd_spatial_bc_measurement.py`, `tests/test_wd_consume_boundary.py` (20/20 PASS), `tests/test_spatial_gauntlet_scenarios.py` (27/27 PASS)
- Governing: `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md`; `agentic_orchestration/gandalf/notes/2026-06-13-q8-companion-convergence-matrix-FINAL.md`; `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` §§4-6; `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` §3.3; `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md` §D4 (`8974209`)
- Decisions-log entry authored: `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (2026-06-16 Axis-2A WIRED-DEFERRED→BUILD)

---

**Signed:** jack-ryan, 2026-06-16 — Gate-2 DEV-MODE. Both Wave-4 additive items PASS. Verification was source-level (transcription cross-check, code-path re-read, changeset audit, test-supersession diff), not smoke-trust. No BLOCK; no WARN; INFO items are forward-notes for downstream wire-ins.
