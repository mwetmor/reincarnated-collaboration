# Finding — 2026-06-22 — proxy realized-damage telemetry (v1.82 OBSERVER)

**Reviewer:** jack-ryan
**Severity:** PASS (one INFO carry-forward to W3)
**Target:** engine commits `4dd8fd5` + `d798246`, tag `star-lord/v-proxy-realized-damage-telemetry-1`; collab completion record `8f67a0e`
**Developer:** star-lord
**Mode:** DEV-MODE Gate-2 (no Gate-1 — operational pipeline, not a sim wave)
**Principles applied:** Review Principle #1 (math-before-code), #2 (smoke/empirical), #3 (cross-seam impact), #5 (severity); Disciplines #11 (empirical inspection), #12 (semantic-shift), #19.1 (cheapest refuting test); ADR-004 (MIGRATION), ADR-006 (DB read-only / apply gate)

## What I found

star-lord added `SpatialFightResult.proxy_realized_damage_dealt: float = 0.0` (spatial_telemetry.py:347) as a brownfield-safe additive observer on gamora's W2 producer path, wired in `spatial_engine.py` result construction (line 2666) as `sum(a.delivered_damage_dealt for a in self._positioned_allies)`. I verified all seven reported results against the tree, not against the completion record. The three load-bearing verifications: (i) **producer-contract exactness** — gamora's contract (simulation/MIGRATION.md §v1.82 §(a) line 35: `Σ over engine._positioned_allies of ally.delivered_damage_dealt`) is read byte-for-byte by the summation expression; same set (`_positioned_allies`, the W1 ally-proxy set, `[]` in solo per engine line 1791/1866), same measure (`delivered_damage_dealt`, the V2 overkill-clamped per-attacker DELIVERED field, accumulated line 1527 for any attacker — ally is just another attacker). (ii) **`player_damage_total` genuinely unchanged** — the writer at spatial_engine.py:2632 (`player_damage_total=self.player.delivered_damage_dealt`) is NOT in the diff; the new lines append after `player_death_element`. Every `player_damage_total` match in the commit is in MIGRATION.md, comments, or tests — never the assignment. Option (a) preserved, no proxy bleed; the `test_player_damage_total_unchanged_option_a` test pins it. (iii) **ADR-006 DB-apply gate genuinely not triggered** — no `ALTER TABLE`, no `_INSERT_SQL` change, no `.sql` or migration `.py` touched; the only "migration"-named file is `export/MIGRATION.md` (ADR-004 cross-seam doc, not a DB migration). `validate()` (line 353) does not reference the field. Export schema `ExportProxyRealizedDamageTelemetry` + `build_proxy_realized_damage_telemetry()` added to schemas.py as a validation-artifact boundary mirroring the v1.81 `ExportTypedDeathTelemetry` pattern exactly (getattr-default brownfield-safe, fight-identity required-field guards, no DB write). I ran the suite: **70/70 PASS in 0.78s** (verified, not asserted). Push held — engine main is 6 ahead of origin, none pushed. MIGRATION.md §v1.82 records both the option-a and internal-to-seam decisions with consumer-obligations and explicit "ADR-006 gate NOT triggered." G-COUNT≠CONTRIBUTION upheld (distinct from cancelled `mean_proxy_contribution_pct`); no content emitted (`_DEFERRED_PROXY_BINS` untouched).

## Rationale

Every dispatch acceptance criterion and NON-NEGOTIABLE GUARD is satisfied and independently refutation-tested. The producer contract reads exactly (Principle #1 / Discipline #11). `player_damage_total` is byte-stable — the highest-risk existing-consumer claim — and I refuted the bleed hypothesis by confirming the writer line is absent from the diff (Discipline #12, option (a) endorsed at W2 Gate-2 `2026-06-22-proxy-W2-gate2.md`). The ADR-006 DB-apply gate is genuinely not triggered: internal-to-seam matches the Wave A2 precedent (`mean_active_proxy_count`/`mean_proxy_contribution_pct` never in `_INSERT_SQL`). This is a clean additive observer that reads 0.0 on every production row today.

### INFO carry-forward (W3, not blocking)

The 6 `TestProxyRealizedDamageV182` tests inject `proxy_realized_damage_dealt` directly into `SpatialFightResult` via the `_make_result()` constructor — they prove field-level dataclass behavior (default 0.0, no-bleed, validate non-enforcement) but do NOT drive `SpatialFightEngine.run()` with a fighting `_positioned_allies` to exercise the summation wiring at line 2666. The wiring correctness is established by my code-read against gamora's contract (cheapest refuting test, Discipline #19.1 — the expression is provably correct), and is acceptable for a brownfield-safe observer (production reads 0.0 regardless; the producer path was Gate-2'd at W2). But W3 calibration is the first wave that drives a real fighting army through the engine — the engine-level integration assertion (one `run()` fixture with a non-empty `_positioned_allies`, asserting the summed result is non-zero and matches per-ally `delivered_damage_dealt`) should land there as the first calibration-harness check, before any magnitude band is read off the instrument. This is the natural place for it, not a gap to backfill here.

## Action

- [x] Developer (star-lord): no remediation required — PASS.
- [ ] W3 (gamora + gandalf): land the engine-level integration assertion (one `SpatialFightEngine.run()` fixture with a fighting `_positioned_allies`, assert summed `proxy_realized_damage_dealt` matches Σ of per-ally `delivered_damage_dealt`) as the first calibration-harness check before reading any magnitude band. The W2 fixture numbers (WR=1.000 / delivered=60000.0) are a proof, NOT a calibration baseline.
- [ ] Push remains HELD (Mac per-cycle Matt-ask) — flag at the cycle's authorized push moment.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py:347,353`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:2632,2666` (and `_positioned_allies` 1791/1866, `delivered_damage_dealt` 644/1527)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` §v1.82 §(a) (gamora producer contract)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` (ExportProxyRealizedDamageTelemetry + builder)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v1.82 (consumer decisions)
- `~/Games/reincarnated-engine/tests/round_trip_spatial_telemetry.py` (70/70 PASS verified)
- `agentic_orchestration/dispatches/2026-06-22-star-lord-proxy-realized-damage-telemetry.md`
- `agentic_orchestration/qa/findings/2026-06-22-proxy-W2-gate2.md` (W2 Gate-2, option-a endorsement)
