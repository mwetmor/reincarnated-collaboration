# Finding — 2026-07-06 — pilot-measurement-report (Gate 2, cross-seam)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-FOLLOWUPS (no BLOCK)
**Target:** tag `star-lord/v-pilot-join-contract-measurement-report-1`, engine commit `2a9c31b`
**Developer:** star-lord
**Principles applied:** #3 (cross-seam impact), #4 (decisions-log/contract as truth), #6 (cross-seam round-trip)
**Disciplines applied:** #1 (math/context-before-code), #2 (smoke-test), #8 (schema validation at boundaries), #11 (empirical inspection)

## Verdict: PASS-WITH-FOLLOWUPS

All five in-scope charges verified. Baseline numbers are trustworthy for gamora to build calibration on. No BLOCK.

## What I found (descriptive)

**Charge 1 — right fix, not wrong fix (VERIFIED).** The gauntlet↔kit-identity join was left structurally correct. The driver recovery path (`variation_pilot_driver.py:658-664`) still derives `legendary_id` via `_build_legendary_config` and looks up in a `legendary_id`-keyed map — matching `gauntlet_sim.py:1437`. Diff scan for any added `character_id` rekey returns NONE. Matt's forbidden ad-hoc rekey was NOT introduced. The fix is confined to the demo-bundle coupling (measurement runs no longer route through `one_realm_bundle_assembler.validate_bundle()`).

**Charge 2 — clean, permanent decoupling (VERIFIED).** `measurement_report_writer.py` imports only stdlib (`json`, `logging`, `datetime`, `pathlib`, `typing`). Zero import of `one_realm_bundle_assembler` or any demo module. Every occurrence of "monsters/gear/bundle_assembler" in the file is docstring/prose, not code. Produced report has no `monsters`/`gear_pool`/`factions` keys (confirmed programmatically). Module is importable by the gamora seam for SPRT-calibration without dragging demo dependencies. Design-as-module (not a flag) is correct given SPRT direct-import need.

**Charge 3 — MIGRATION.md §v2.10 (VERIFIED accurate).** Describes the new module, the published join contract (with file:line citations), the schema table, the SPRT-reuse contract (additive `sprt_state`, `report_type` discriminator), and the solo-caster baseline table. Consumer-impact line is correct: gamora acts (SPRT + baseline read); drax/loadout/demo-bundle consumers unaffected. The baseline table in the doc matches the emitted JSON exactly.

**Charge 4 — round-trip smoke exercises the real boundary (VERIFIED).** Re-ran the actual path (`extract_pilot_measurement_report` → `validate_measurement_report` → `write_measurement_report` → `smoke_validate_measurement_report`) against the on-disk source. Result: `pass=True`, `errors=[]`, `melee_emit_count=2`, `caster_plain_emit=0`, `shell_cohort_pairs=8`. This reads the real 3.4 MB results file and serializes a real zero-monster report — not a mock.

**Charge 5 — baseline derivation (VERIFIED, independently recomputed).** I recomputed `tier_2_kpm` mean/min/max/n per clear-shell × cohort directly from the source `encounter_results` (filter: `caster_cell_id in lid`, `'light' not in lid`, shell ∈ CLEAR_SHELLS, cohort ∈ {Balanced,Hybrid}). Every value matches the emitted report to 4 decimals including sample counts:
- open_arena B/H: 0.0 (n=124); chokepoint B/H: 0.0 (n=93)
- magic_pack B/H: 600.0 (n=93); elite_pack B: 426.8909 (n=124), H: 425.3575 (n=124)

Numbers are genuinely derived from disk, not fabricated. gamora can build calibration on them.

## Follow-ups (non-blocking, INFO)

- [ ] **gamora:** The report is extracted from `cycle-13-gauntlet-sim-results-2026-05-27.json`, which contains only 4 distinct kit_results lids (2 melee + 2 caster_plain) and NO `int_light` proxy-dominant lids. So `caster_proxy` is legitimately EMPTY — this is correct data for this results file, not a silent extraction miss. If the calibration expects proxy-dominant baseline rows, note they are absent from this source and will require a proxy-cell-bearing results file. (Not a defect in this commit.)
- [ ] **gamora:** `magic_pack` KPM=600.0 is a flat min=max=600.0 across all 93 samples — likely a ceiling/clamp artifact in the source sim, not a natural distribution. Confirm the clamp semantics before treating 600.0 as a real DPS reading in calibration. (Source-data property, out of star-lord's scope; flagged so it isn't mistaken for signal.)

## Rationale

Principle #6 (cross-seam round-trip) satisfied: the boundary was exercised end-to-end, not asserted. Principle #4 (contract as truth): the join contract was verified against the published sources (`MIGRATION.md §v1.88`, `gauntlet_sim.py:1437`) rather than re-derived. Principle #3 (cross-seam impact): consumer-impact is correctly scoped to gamora only. Discipline #8 satisfied: `validate_measurement_report` gates the write with HALT-LOUD.

## Out of scope (not faulted per charge)

Tiered-shell scoping (Matt-reserved batch-2), balance re-tuning, the calibration itself.

## References

- `reincarnated-engine/src/reincarnated/export/measurement_report_writer.py`
- `reincarnated-engine/src/reincarnated/export/variation_pilot_driver.py` (recovery path 640-690; new `run_measurement_report` + flags)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v2.10
- `reincarnated-engine/src/reincarnated/output/variation_pilot_measurement_report.json`
- source: `reincarnated-engine/src/reincarnated/simulation/output/pilot/cycle-13-gauntlet-sim-results-2026-05-27.json`
