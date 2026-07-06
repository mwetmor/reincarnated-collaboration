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
<!-- star-lord appends on completion -->
