# Gate-2 Submission — 2026-07-08 — star-lord: §8-A1 band-measurement report decoupled from WR-bracket gate (MEASURE-THEN-FILTER)

**Submitter:** star-lord (export/driver seam)
**Reviewer:** jack-ryan (Gate-2)
**Tag:** `star-lord/v-batch2-measure-then-filter-1`
**Authority:** dispatch `2026-07-08-gamora-starlord-spatial-floor-diagnosis.md` rider 1 (Matt 2026-07-07 Lane-C v3-aware verdict).
**MIGRATION.md:** export/MIGRATION.md § MEASURE-THEN-FILTER (newest entry, prepended 2026-07-08).
**Files changed:**
  - `src/reincarnated/export/w3_emission_driver.py` — new function + constant + call site + result dict
  - `tests/test_w3_emission_driver.py` — Group F (8 new tests)
  - `src/reincarnated/export/MIGRATION.md` — new entry (prepended)

---

## What this fixes

The v3 leg-3 pilot (`dry_run_flavor=True`, seed 56000000, 18 candidates) completed the gauntlet (25,530 fights,
1588s) but returned 0/18 kits passing the WR-bracket gate. TP3 halted on an empty `survivor_kit_records`
before any §8-A1 band measurements were produced or persisted. The run zeroed out its own diagnostic yield —
that is backwards.

**Root cause:** the driver conflated the EMISSION CERTIFICATION GATE (TP3: refuse empty bundle) with the
MEASUREMENT INSTRUMENT (§8-A1 band report on the population). They should be independent.

---

## What changed

### New: `_build_section8a1_band_report()` @ `w3_emission_driver.py`

A pure measurement function. Called immediately after `in_band_count = len(passing_kits)` (before the
kit-record build loop, before TP3). Takes `all_kits` (all 18 candidates), reads `kit.bc_proxy_density`
and `kit.character_id`, compares against the passing set to record per-candidate WR-bracket pass/fail.

Returns a report dict with:
- `gate_outcome`: {wr_bracket_passing, wr_bracket_failing, wr_bracket_total, pass_rate, emission_certified}
- `band_summary`: per-band (none/light/heavy) {total, wr_bracket_pass, wr_bracket_fail, exercised, exercised_note}
- `per_candidate`: {none: [...], light: [...], heavy: [...]} — each entry {kit_id, proxy_density, wr_bracket_pass}
- `registry_honesty`: NOT-EXERCISED / UNPROVEN riders embedded in every report

### New: `_SECTION8A1_BAND_REPORT_PATH` constant

```
src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json
```

### Write location — BEFORE TP3

The report is written to disk at the `_SECTION8A1_BAND_REPORT_PATH` before the kit-record build loop
and before TP3's `assert len(survivor_kit_records) > 0`. This means:
- A 0/18-pass run produces a persisted report file (all 18 measured, gate=0/18 truthfully recorded)
- TP3 still halts the EMISSION (correct — no empty bundle emitted)
- The measurement report survives the halt and is readable independently

### TP3 unchanged

`assert len(survivor_kit_records) > 0` is not removed, not softened. It is the emission certification
gate. Only its chronological relationship to the measurement has changed: measurement now precedes it.

### Result dict additions (normal-completion path)

Three new keys added to the dict returned by `run_w3_emission()`:
- `section8a1_band_report_path`: str
- `section8a1_band_summary`: dict
- `section8a1_gate_outcome`: dict

---

## Round-trip smoke (dispatch Principle 6 — REQUIRED)

**8 tests, Group F (`tests/test_w3_emission_driver.py::TestSection8A1BandReport`), ALL PASS (run 2026-07-08):**

| Test | What it proves |
|---|---|
| `test_zero_passing_produces_full_report` | 0/18 pass → report has all 18 measured, gate=0/18, emission_certified=False |
| `test_zero_passing_round_trip_read_back` | Persist + read-back → bands intact, gate=0/18 truthful, honesty riders present |
| `test_mixed_band_17_none_1_light_all_failing` | Catalog reality (17/1/0), all failing → heavy exercised=False |
| `test_partial_pass_gate_recorded_truthfully` | 3/18 passing → gate counts correct (non-degenerate partial pass) |
| `test_registry_honesty_fields_present` | NOT-EXERCISED / UNPROVEN / light-band-only / 17/1/0 all in every report |
| `test_heavy_band_always_not_exercised` | Heavy band exercised=False + NOT-EXERCISED note when no heavy cells |
| `test_smoke_run_produces_band_report_in_result` | Integration: smoke run includes band-report keys in result dict |
| `test_section8a1_band_report_path_constant_is_correct` | Path name contains "leg3_pilot_section8a1_band_measurement" + ends ".json" |

The key dispatch test (`test_zero_passing_round_trip_read_back`) directly proves: "a dry-run where 0/18
pass the WR-bracket still produces a persisted §8-A1 band-measurement report with all 18 measured +
gate outcomes recorded → read back → bands intact + gate=0/18 recorded truthfully."

---

## Registry-honesty (dispatch binding — unchanged from prior leg-3 riders)

- Proxy-HEAVY band: NOT-EXERCISED — catalog is 17 none / 1 light / 0 heavy.
- C2 peak-concurrent-proxy: light-band-only (proxy_max_active=1 from decl; peak concurrent = 1).
- ≤7 worst-case bound: UNPROVEN — light-band-only pilot; proxy-heavy worst-case not measured.
- These riders are embedded in every report instance via the `registry_honesty` sub-dict.

---

## Out of scope (confirmed non-goals per dispatch)

- No Tier-1 re-fire (separate Matt ADR-006 run-auth after this lands)
- No recovery-mode batch-1-fossil work (_RECOVERY_EXPECTED_SURVIVOR_COUNT hard-codes — named follow-up)
- No leg-3 wire touches (TP1/TP2/TP3 proven; only the report-gate sequence is adjusted)
- No simulation touches (gamora seam boundary respected)

---

## Jack-ryan review asks

1. **Decoupling correctness:** the band report is written before TP3 in all code paths (normal + smoke + recovery-mode). Verify the insertion point in `run_w3_emission()` is before the `assert len(survivor_kit_records) > 0` line.
2. **Report shape:** the `section8a1_band_report_path` key in the result dict is only present when the run COMPLETES (normal path). In the 0-survivor halt path, the file is on disk but the result dict is never returned (the AssertionError propagates). This is acceptable per the dispatch ("persisted BEFORE/independent of that gate").
3. **No bundle or registry shape change:** the bundle JSON and run_registry schema are unchanged. The new artifact is an analysis JSON in `output/` only.
4. **Registry-honesty embedding:** confirm `registry_honesty` sub-dict is present on every report with NOT-EXERCISED / UNPROVEN / light-band-only / 17/1/0 text (covered by `test_registry_honesty_fields_present`).

---

## References

- Dispatch: `agentic_orchestration/dispatches/2026-07-08-gamora-starlord-spatial-floor-diagnosis.md`
- MIGRATION.md: `src/reincarnated/export/MIGRATION.md` § MEASURE-THEN-FILTER (newest entry)
- Driver: `src/reincarnated/export/w3_emission_driver.py`
- Tests: `tests/test_w3_emission_driver.py` Group F
- v3 log (confirmed): `/tmp/leg3_n1_v3.log` (gauntlet COMPLETE, 0/18 passing, TP3 HALT-LOUD)
