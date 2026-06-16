# Finding — 2026-06-16 — telegraph-combat-model (Gate-2, dispatch 3 Phase 2)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO
**Target:** engine commit `ffafd4e`, tag `gamora/v1.4-telegraph-combat-model`
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 2 (smoke-gate vs full-regen), 3 (cross-seam impact), 5 (severity matters); Disciplines #1, #2, #12; ADR-004 (MIGRATION); parent ruling §7.1/§7.2/§7.4
**Gate-1 antecedent:** finding `ba95624` (CLEAR-WITH-AMENDMENTS, A3-1 + CL-3)

## Verdict
**PASS-WITH-INFO.** All six dispatch deliverables independently verified. The load-bearing §7.2 invariant holds on my own re-run. Two INFO-tier doc-vs-reality notes (below); neither blocks tag or dispatch-4 fire.

## What I found
I re-ran the §7.2 regression smoke (`scripts/gamora_telegraph_regression_smoke_2026_06_16.py`) and the full spatial test slice independently — did not take gamora's report on faith.

1. **§7.2 bit-identical (the crux) — CONFIRMED.** My re-run: `boss_with_adds` ON≡OFF identical PASS (600 telegraphs ON / 0 OFF); `open_arena` ON≡OFF identical PASS (203 ON / 0 OFF); `is_dodge_gated_coordinate(glass-close-ST) = True` PRESERVED; OFF path emits 0 telegraphs (byte-identical-when-off). The identity assertion is a per-fight 7-tuple (`winner, elapsed_s, player_kill, mobs_killed, total_aoe_hits, total_flanking_ticks, max_flanking_count`), compared exactly per fight, exit-nonzero on any divergence. No divergence. Telegraphs move no sim outcome.

2. **Mint correctness — CONFIRMED minted-from-kernels, no 1D path.** `_mint_telegraph_spec` (`spatial_engine.py:620`) reads the SAME footprint constants the resolver kernels read (`_aoe_radius_for_skill`, `CONE_RANGE_M`/`CONE_HALF_ANGLE_RAD`, `LINE_RANGE_M`/`LINE_WIDTH_M`) plus dynamic `attacker.heading_rad` at fire-instant — no re-computation. `grep` confirms ZERO `SearchGradeEstimate`/1D-estimator references in the file (§7.4 spatial-minted by construction). The call-site (`:1548-1569`) is DOWNSTREAM of HP/damage/cooldown updates, gated entirely on `self._emit_telegraphs`, and append-only to `telegraph_buffer` — no avoidance branch, no sim-state mutation. `_tg_dmg` is recomputed locally for telegraph metadata only; the real damage application (gated on `hits`) is untouched.

3. **TelegraphSpec dataclass — CONFIRMED, no drift.** Reflection shows the contract object; round-trip key `attack_id == f"{attacker_id}:{skill_idx}"`; carried-in-contract unit fields (`spatial_unit=m`, `time_unit=s`, `angle_unit=rad`, `frame_origin=bottom_left`); `validate()` Pattern-P7 guard present.

4. **Fixture — CONFIRMED real emit.** `output/telegraph-fixture-2026-06-16.json`: 200 specs, shape histogram `{circle:188, line:2, point:10}`, round-trip key holds for ALL 200, per-shape extents correctly populated (circle→radius, line→range+width+orientation, point→all-None), units carried. Real production-path fight, not a stub.

5. **MIGRATION v1.71 — CONFIRMED sufficient for dispatch 4.** Field-for-field table covers all 19 fields with types + units, matching the dataclass exactly; coordinate-frame + edge-disposition semantics documented; star-lord can serialize without drift. Exactly one `v1.31`, one `v1.71`, one `v1.69b` header (collision resolved).

6. **Gate-1 amendments — ALL THREE CONFIRMED.** (a) `TELEGRAPH_WIND_UP_DEFAULTS_S` pinned (`:98`) with derived rationale (reaction-floor + escape-distance/v_ref, §8.3); (b) duplicate `v1.31` disambiguated, W-D re-labeled `v1.69b`; (c) §7.2 smoke produced + re-run PASS.

**Test suite:** `302 passed, 0 failed` across the spatial/telegraph/dodge-gated/round-trip slice (254s).

## Rationale
The dispatch's BLOCK condition was "§7.2 ON/OFF outcome NOT bit-identical." My independent re-run shows bit-identical per-fight signatures on both scenarios → no BLOCK. Mint draws from certified-kernel constants with no 1D-estimator path → §7.1/§7.4 satisfied at the source. MIGRATION field-for-field → ADR-004 cross-seam contract clean for dispatch 4.

## INFO notes (non-blocking, for the record)
- **INFO-1 (field count):** commit message + MIGRATION prose say "18 fields"; the dataclass has **19** (the extra is `damage_amount` vs the 4 unit declarations being counted ambiguously). The MIGRATION TABLE itself lists all 19 correctly, so star-lord inherits the right surface — the "18" is prose-only drift. Suggest gamora correct the prose to 19 at next touch; not a contract defect.
- **INFO-2 (HP-identity granularity):** the §7.2 identity tuple uses `player_kill`/`mobs_killed` (binary/count) rather than a raw residual-HP float. Any HP perturbation would still surface via `elapsed_s` or `total_aoe_hits` divergence, so the guard is sound — but a future tightening could add exact final-HP to the signature for a stricter wall. Note for dispatch-4 round-trip design, not a Phase-2 defect.

## Action
- [x] jack-ryan: Gate-2 PASS-WITH-INFO; tag `gamora/v1.4-telegraph-combat-model` clears Gate-2.
- [ ] gamora (optional, next-touch): correct "18 fields" → "19" in commit-adjacent prose / MIGRATION header line.
- [ ] star-lord (dispatch 4): consume MIGRATION v1.71 + fixture; round-trip on `attack_id`. Contract is drift-free as authored.
- [ ] No Matt escalation required (no BLOCK; PASS within ADR-002 within-seam-emission authority routed through the Gate-2 gate).

## References
- `src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py` (TelegraphSpec `:103-187`)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (`_mint_telegraph_spec` `:620`, wiring `:1548-1569`, wind-up table `:98`, flag/buffer `:1207-1208`)
- `scripts/gamora_telegraph_regression_smoke_2026_06_16.py` (identity `:123-152`)
- `output/telegraph-fixture-2026-06-16.json` (200 specs)
- `src/reincarnated/simulation/MIGRATION.md` (v1.71 `:11`, v1.69b re-label `:7478`)
- `design/math/telegraph-combat-model-2026-06-16.md`
- Gate-1 finding `ba95624`; parent ruling `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` §7.1/§7.2/§7.4
