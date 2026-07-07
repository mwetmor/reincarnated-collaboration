# Gate-2 submission — star-lord leg-2 VALIDATOR-WIDEN (DDA-lock conditional widen)

**Submitted by:** star-lord
**Date:** 2026-07-07
**Tag:** `star-lord/v-batch2-dda-lock-validator-widen-1`
**Seam:** export/telemetry (star-lord)
**Gate-2 context:** EMIT-BOUNDARY CHANGE — part of THREE-SEAM leg-2 lockstep.
  Coordinated Gate-2 covers rocket + star-lord + gamora (all three must land before leg-3 fires).

## What this submission is

The VALIDATE half of the three-seam leg-2 co-dispatch
(`agentic_orchestration/dispatches/2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md`).

**Rocket's PRODUCE half** (`rocket/v-batch2-leg2-summoner-emission-route-1`) already landed —
it added `route_primary_t4()` in `mechanic_alteration.py` and the C2 shared constant
`ACCEPTED_PROXY_PRIMARY_T4` in `t4_catalog_v2.py`.

**This VALIDATE half** widens the DDA-locked emitter validator in `validate_class_data()`
(`export/cycle14_wave5_emitter.py`) so it admits proxy-family `primary_t4` values for
proxy-bearing kits, WITHOUT loosening the DDA lock for empty-decl (non-summoner) kits.

**Gamora's CONSUME half** (`gamora/v-batch2-primary-t4-consume-widen-1`) is PENDING — see
`agentic_orchestration/qa/pending/2026-07-07-gamora-leg2-primary-t4-consume-gate2.md`.

## Gate-1 conditions satisfied by this submission

- **C1 (three-seam lockstep):** star-lord's MIGRATION.md names the C1 interim divergence window
  explicitly — the window is OPEN until gamora's consume-side lands. The closing event is
  explicit: all three seams tagged + coordinated Gate-2.
- **C2 (shared constant):** `ACCEPTED_PROXY_PRIMARY_T4` IMPORTED from `t4_catalog_v2`, NOT
  copied. `_PROXY_FAMILY_PRIMARY_T4_STRATEGIES` is now an alias pointing at the imported constant
  (backward compat). ZONE_CONTROL excluded from the accepted set per C2 structural exclusion.
- **C3 (S2 byte-diff):** non-summoner kits are BYTE-IDENTICAL off the validator — the
  conditional `is_proxy_bearing = bool(proxy_decls)` gates the proxy-family path; empty-decl
  kits still resolve through the DDA branch unchanged. This is CITED here (Gate-2 condition).
- **C4 (S1 route-correctness):** the 5 ACCEPTED_PROXY_PRIMARY_T4 members correspond exactly
  to the values rocket's route may emit. Smoke confirms bone→FISSION, crypt→SOVEREIGNTY via
  rocket's CITED smoke (`generation/notes/leg2_primary_t4_route_smoke_2026_07_07.py`).

## Validator site

**File:** `src/reincarnated/export/cycle14_wave5_emitter.py`
**Function:** `validate_class_data(class_data: dict, season_id_str: str) -> None`
**Docstring section added:** `§ leg-2 VALIDATOR-WIDEN (2026-07-07)`
**Predicate:** `proxy_decls = class_data.get("proxies") or []` → `is_proxy_bearing = bool(proxy_decls)`

## Conditional logic summary

| Kit type | primary_t4.strategy | Validator result |
|---|---|---|
| Non-summoner (proxies=[]) | DIRECT_DAMAGE_AMPLIFICATION | ADMIT (DDA lock) |
| Non-summoner (proxies=[]) | any ACCEPTED_PROXY_PRIMARY_T4 member | **REJECT** (lock preserved) |
| Non-summoner (proxies=[]) | ZONE_CONTROL | REJECT |
| Non-summoner (proxies=[]) | unknown string | REJECT |
| Summoner (proxies non-empty) | DIRECT_DAMAGE_AMPLIFICATION | ADMIT (ETA_FLOOR fallback) |
| Summoner (proxies non-empty) | any ACCEPTED_PROXY_PRIMARY_T4 member | **ADMIT** (widen) |
| Summoner (proxies non-empty) | ZONE_CONTROL | REJECT (excluded from C2 constant) |
| Summoner (proxies non-empty) | unknown string | REJECT |

## Round-trip smoke (Principle 6 — both cases GREEN)

**CASE 1 (summoner kit + proxy-family primary_t4 → admit → persist/read-back intact):**
- Kit: `smoke_kit_001`, `proxies=[{proxy_type: skeletal, count: 3, ...}]` (non-empty)
- `primary_t4.strategy = "PROXY_FISSION"`, scope and discipline_anchor set
- `validate_class_data()` → no exception
- `json.dumps/loads` round-trip → strategy reads back as `"PROXY_FISSION"`, proxies intact
- All 5 ACCEPTED_PROXY_PRIMARY_T4 members: GREEN

**CASE 2 (empty-decl kit + stray non-DDA primary_t4 → validator REJECTS):**
- Kit: `smoke_kit_001`, `proxies=[]` (empty, non-summoner)
- `primary_t4.strategy = "PROXY_ASCENSION"` (stray non-DDA)
- `validate_class_data()` → ValueError: "proxy_decls (proxies) is empty — DDA lock holds"
- All 5 ACCEPTED_PROXY_PRIMARY_T4 members reject on empty-decl kits: GREEN

## Test results

**File:** `tests/test_cycle14_wave5_loadout_emission.py`
**Total:** 115 PASS (zero failures; 6 tests renamed/expanded from W0 era; 10 new tests added)
**Validator-specific (16 tests):**
- `test_validate_class_data_accepts_dda_primary_t4` — DDA on non-summoner → ADMIT
- `test_validate_class_data_accepts_dda_primary_t4_on_summoner_kit` — DDA on summoner → ADMIT
- `test_validate_class_data_accepts_proxy_family_primary_t4_on_summoner_kit[×5]` — all 5 C2 members
- `test_validate_class_data_rejects_proxy_family_primary_t4_on_empty_decl_kit[×5]` — CASE 2
- `test_validate_class_data_rejects_zone_control_as_primary_t4` — C2 structural exclusion
- `test_validate_class_data_rejects_unknown_primary_t4_strategy`
- `test_validate_class_data_rejects_proxy_family_t4_missing_scope`
- `test_validate_class_data_proxy_accepted_set_matches_c2_constant` — C2 pin

**Broader regression:** 188 PASS (test_one_realm_bundle_assembler + test_layer2_dimensions_and_t4_catalog_v2 +
test_proxy_t4_suite_strategies + test_proxy_pairing_layer). Zero regressions.

## Files changed

- `src/reincarnated/export/cycle14_wave5_emitter.py` — import + validator widen
- `src/reincarnated/export/MIGRATION.md` — § leg-2 VALIDATOR-WIDEN (newest entry)
- `src/reincarnated/export/AGENT_STATE.md` — checkpoint updated
- `tests/test_cycle14_wave5_loadout_emission.py` — validator tests updated (6 renamed + 10 new)
- `agentic_orchestration/qa/pending/2026-07-07-star-lord-dda-lock-validator-widen-gate2.md` — this file

## Consumer action required

**None for drax/loadout** on existing bundles. This is a validation-predicate change only —
no new export field, no renamed field, no removed field. drax's bundle loader is unaffected.

Summoner kits will carry proxy-family `primary_t4.strategy` strings in the leg-3 bundle
(once rocket leg-3 emission run fires), but drax's loader already treats `primary_t4` as an
opaque dict — the W0-DDA-widen pre-established schema tolerance for proxy-family strings.

## Cross-seam status

- **Rocket PRODUCE:** LANDED (`rocket/v-batch2-leg2-summoner-emission-route-1`)
- **Star-lord VALIDATE:** LANDED (this tag — `star-lord/v-batch2-dda-lock-validator-widen-1`)
- **Gamora CONSUME:** PENDING (`gamora/v-batch2-primary-t4-consume-widen-1`) — see
  `agentic_orchestration/qa/pending/2026-07-07-gamora-leg2-primary-t4-consume-gate2.md`
- **Leg-3 emission run:** HELD until gamora consume-side lands + coordinated Gate-2

## Integrity ledger

- 1 code file changed (`cycle14_wave5_emitter.py`: import + validator widen)
- 1 test file updated (`test_cycle14_wave5_loadout_emission.py`: 6 renamed + 10 new)
- 1 MIGRATION.md entry (export seam)
- 1 AGENT_STATE.md update
- 0 telemetry schema changes (validation-predicate only; no new column)
- 0 chassis/bar/band/magnitude touch
- 0 LLM call-site changes
