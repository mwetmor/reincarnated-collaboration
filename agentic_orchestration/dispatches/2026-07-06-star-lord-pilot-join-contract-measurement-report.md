# Dispatch — 2026-07-06 — star-lord — pilot join-contract fix + measurement-report decoupling + re-extract

**From:** knight-rider
**To:** star-lord (with gamora consult on the gauntlet-results contract)
**Approved by:** Matt 2026-07-06 (triage ruling, 4 items)
**Estimated effort:** ~2–4h
**Acceptance:** join fixed via published contract; measurement runs no longer require demo-bundle validity; Leg-4 attribution + solo-caster baseline re-extracted from the ON-DISK results (no re-fight).

## Context

The pruned variation pilot (`--n-per-cell 25`) generated 50 kits and ran the full gauntlet to completion — `GAUNTLET_SIM_PASS=True`, 118,350 fights, 903s, results on disk at `reincarnated-engine/src/reincarnated/simulation/output/pilot/cycle-13-gauntlet-sim-results-2026-05-27.json` (3.4 MB, 81 configs, **40 with `season_emit: True` including melee configs**). But `variation_pilot_driver` reported `0/50 in-band → 0 survivors → empty bundle → HALT-LOUD (Discipline #8: no kits / no monsters)`.

**Leading root-cause hypothesis (confirm before fixing):** the gauntlet keys `kit_results` by **`legendary_id`** (e.g. `endgame_bc_melee_medium_variable_str_none_t4_chain_1`); the driver's survivor join-back keys by **`character_id`** (e.g. `S1_endgame_bc_melee_medium_variable_str_none_s0`). Namespace mismatch → zero join hits even though 40 configs emitted. This is a seam-boundary defect, NOT a balance failure — the kits pass the gate.

Nothing is lost: the fight data (and the solo-caster baseline gamora's calibration needs) is on disk; only the extraction/report layer broke.

## Required reading before starting
- `agentic_orchestration/variation-pilot-run-state-2026-07-06.md` — full run-2 record + Matt's 4-item triage ruling (authoritative).
- `reincarnated-engine/src/reincarnated/export/variation_pilot_driver.py` — the survivor join-back + Step-5 bundle-assembly path.
- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — how `kit_results` are keyed/emitted (the published contract source; **gamora is the authority here — consult, do not guess**).
- The gauntlet-results↔kit-identity contract wherever it is PUBLISHED (MIGRATION.md / schema doc / results-contract). Matt: **fix via the published contract, not an ad-hoc rekey.**
- `reincarnated-engine/src/reincarnated/export/one_realm_bundle_assembler.py` — the demo-bundle validation being (wrongly) reused for a measurement run.
- gamora's calibration note: `simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` — what the solo baseline must feed (the open slot: `solo_caster_baseline_KPM` per clear shell × cohort).

## Scope
- [ ] **Item 1 — Join fix via published contract.** Confirm the root-cause hypothesis against the results file. Locate the PUBLISHED gauntlet-results↔kit contract (gamora consult). Fix the driver's survivor join-back to key on the contracted identity the gauntlet actually emits — NOT an ad-hoc character_id→legendary_id rekey hack. If the contract itself is ambiguous/underspecified, that is a finding: document it and raise to knight-rider rather than papering over.
- [ ] **Item 2 — Measurement-report decoupling (PERMANENT).** A measurement/pilot/SPRT-calibration run's deliverable is a REPORT, not a demo bundle. Uncouple the measurement path from `one_realm_bundle_assembler` demo-validity (monsters/gear) entirely. Measurement runs must produce a valid report with zero monsters/gear. This path is reused by future SPRT-calibration runs — design it as a first-class measurement-emit path, not a pilot special-case.
- [ ] **Item 3 — Re-extract from on-disk results (NO re-fight).** From the existing `cycle-13-gauntlet-sim-results-2026-05-27.json`: (a) Leg-4 attribution data (melee-cell + caster-cell survivor sets, distinctness carried through to fights, per-cohort pass); (b) the **solo-caster baseline** in the shape gamora's calibration note needs (`solo_caster_baseline_KPM` per clear shell × cohort), sourced from the ~21 plain-caster (non-proxy) kits. Emit as the measurement report from Item 2.
- [ ] Smoke-test passes
- [ ] MIGRATION.md if the join fix or measurement-emit path changes any cross-seam contract field
- [ ] Round-trip smoke (or not-applicable justification) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `star-lord/v-pilot-join-contract-measurement-report-1`

## Cross-seam contract change? (Principle 6 gate)
**YES — this dispatch is ABOUT a cross-seam contract (gauntlet `kit_results` identity → export survivor extraction).** Acceptance MUST include:
- **Round-trip smoke:** generate a tiny fixture (or reuse a slice of the on-disk 81-config results), run the survivor join-back, assert non-zero survivors map back to their generated kits by the contracted identity, and assert the measurement report serializes with zero monsters/gear. Field-presence check on the joined identity key.

## Acceptance criteria
- [ ] Root-cause confirmed against the results file and stated with file:line for both the gauntlet emit-key and the driver join-key.
- [ ] Join fixed via the published contract; the fix references the contract's published location.
- [ ] Measurement report emits successfully for THIS run's on-disk results with zero monsters/gear — no Discipline-#8 HALT.
- [ ] Solo-caster baseline extracted in gamora's calibration-note input shape; report path handed to knight-rider so calibration can queue.
- [ ] Round-trip smoke: on-disk results slice → join-back → non-zero mapped survivors + zero-monster report serialization. OR not-applicable justification (not expected — this IS a contract change).

## Out of scope (explicit non-goals)
- **Full-18-shell → tiered-shells scoping. DO NOT TOUCH.** Matt: this is the tiered-shells lever already on the batch-2 books, not a triage fix. Preserved in the run-state note. Leave the gauntlet running whatever shell set it runs; only fix the identity join + report path.
- Any re-fight / re-run of the gauntlet. Re-extract only.
- Proxy-magnitude calibration itself (gamora's gated task; this dispatch only unblocks its input).
- Any balance re-tuning of melee (over-ceiling) or caster (under-floor) — that's downstream of Leg-4 analysis, not triage.

## Open questions for the agent to resolve (document your answers)
- Where is the gauntlet-results↔kit-identity contract actually published? If it is NOT published anywhere, that absence is the real defect — flag it to knight-rider (a contract can't be "fixed via the published contract" if none exists; it may need to be authored, which is a Gate-1 item, not a silent triage decision).
- Does the measurement-emit path warrant its own module/entrypoint (given SPRT-calibration reuse) or a flag on the existing driver? Choose and justify.

## References
- `agentic_orchestration/variation-pilot-run-state-2026-07-06.md` (Matt's triage ruling + run-2 record)
- decisions-log `2c0d357` (Option 1 ruling), calibration Gate-1 disposition (in run-state)
- Gate-2 review of the tagged fix returns to jack-ryan (cross-seam boundary → mandatory Gate-2).

---

## Completion record

**Completed:** 2026-07-06 by star-lord
**Tag:** `star-lord/v-pilot-join-contract-measurement-report-1`
**Engine commit:** (tagged at session end)

### Item 1 — Root cause confirmed

**Confirmed file:line (both keys):**
- Gauntlet emit-key: `gauntlet_sim.py:1437` — `legendary_id = f"{kit.bc_cell_id}_{chain_id}"` in `_build_legendary_config` (cell-level, keyed by BC cell + T4 chain, NOT per-sample `character_id`)
- Driver join-key: `variation_pilot_driver.py:661` — recovery path correctly calls `_build_legendary_config(kit, enc_idx2)` and joins via `config_to_kits[legendary_id]`. The join logic itself IS structurally correct.

**Actual root cause:** The HALT-LOUD was NOT a join/namespace bug. It was demo-bundle coupling: `validate_bundle()` at `one_realm_bundle_assembler.py:1237` fired "Bundle has no monsters — demo requires monster content" (a demo constraint, irrelevant for a measurement run). Simultaneously "Bundle has no kits" — because 0 survivors (caster `season_emit=False` was valid measurement data, not a balance failure). Run log confirms at lines 8106-8111 of `variation_pilot_run.log`.

**Published contract location:** The gauntlet-results↔kit-identity contract IS published in:
1. `AGENT_STATE.md §W3-Batch-1-Post-Run-Defect-Record` (lines 189-199)
2. `MIGRATION.md §v1.88` (Assert-B documentation)
3. `season_generation_pipeline.py:_build_legendary_config():1437,1385` (code-citation in comments)
4. NOW ALSO: `measurement_report_writer.py` (module docstring) + `MIGRATION.md §v2.10`

### Item 2 — Measurement-report decoupling (PERMANENT)

**New module:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/measurement_report_writer.py`
- `extract_pilot_measurement_report()`, `validate_measurement_report()`, `write_measurement_report()`, `smoke_validate_measurement_report()`
- Zero coupling to `one_realm_bundle_assembler`. No monsters/gear required.
- SPRT-calibration reuse: gamora imports from this module. Additive SPRT fields supported.

**Design choice: own module (not a flag).** Rationale: separate contracts (demo-bundle vs measurement), separate consumers (drax vs gamora). A flag on the assembler would preserve the wrong coupling at the type level.

**Driver changes:** `variation_pilot_driver.py` — `--emit-measurement-report` flag + `run_measurement_report()` + `PILOT_MEASUREMENT_REPORT_PATH` constant. `MIGRATION.md §v2.10` documents all changes.

### Item 3 — Re-extraction (no re-fight)

**Report path:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/variation_pilot_measurement_report.json`

**Solo-caster baseline (gamora §2 open slot — FILLED):**

| Shell | Cohort | solo_caster_baseline_KPM | Required summon contribution |
|---|---|---|---|
| open_arena | Balanced | 0.0 | 9.90 (bar lo) |
| open_arena | Hybrid | 0.0 | 9.90 |
| chokepoint_corridor | Balanced | 0.0 | 11.65 |
| chokepoint_corridor | Hybrid | 0.0 | 11.65 |
| magic_pack | Balanced | 600.0 | 0.0 (above ceiling — survivability only) |
| magic_pack | Hybrid | 600.0 | 0.0 |
| elite_pack | Balanced | 426.89 | 0.0 |
| elite_pack | Hybrid | 425.36 | 0.0 |

**Leg-4 attribution:** MELEE cell — 2 legendary_ids, both `season_emit=True`, passes Balanced/Hybrid/DPS-min-maxer. CASTER plain — 2 legendary_ids, both `season_emit=False` (caster times out on clear shells without summon). CASTER proxy — 0 entries in results (the "light" proxy kits' legendary_id suffix `_int_light_*` is absent from this results file; 4/25 proxy-dominant kits confirmed in generation checkpoint).

### Round-trip smoke (Principle 6) — ALL PASS

```
PASS: melee season_emit_count = 2 (non-zero legendary_ids mapped)
PASS: validate_measurement_report returns no errors (zero monsters/gear required)
PASS: solo_caster_baseline populated for 4 shells × 2 cohorts (8 pairs)
PASS: round-trip smoke from disk (schema_version=pilot-v1)
PASS: report has no monsters or gear_pool (decoupled from demo-bundle)
```

### MIGRATION.md

`MIGRATION.md §v2.10` authored. Documents: new `measurement_report_writer.py`, schema `pilot-v1`, solo-caster baseline table, contract publication, round-trip smoke result, driver CLI changes.

### Gamora calibration queue

gamora's §2 open slot is now filled. Solo-caster baseline confirms the calibration note prediction exactly (open_arena/chokepoint: 0.0 KPM timeout → summon must carry full clear; magic_pack/elite_pack: 600.0/426 KPM → summon adds survivability only, not DPS). gamora can now proceed with the calibrated re-emit + caster-cell re-fight under Gate-1 conditions 1-5.
