# Dispatch — 2026-06-13 — star-lord — W-B export-side: type-wall + fidelity re-type

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-13 — cert-wave sequence approved; W-B is the Matt-pre-authorized TODAY drift-proofing move (wave doc § 3).
**Status:** GATE-1 PASS-WITH-INFO (jack-ryan, 2026-06-13). One WARN folded: scope SPLIT into a parallel-safe half and a D1-gated half (see Scope). FIRES on Matt go; the commit-grade-type half waits on D1's MIGRATION landing.
**Estimated effort:** ~hours (export-type minting + one artifact re-type).
**Acceptance:** `bc_measured_bins.json` as emitted from the 1D path advertises **search-grade** (a `fidelity:"search"` field the consumer asserts on, or a rename to `bc_search_estimate_bins.json` — your call, documented). The export-side identity-consumer accepts only commit-grade provenance. A consume-path check confirms a search-grade artifact cannot be admitted as behavioral identity.

## Context

This is the **export-side half** of the cert wave's chokepoint type-wall (wave doc § 3.1). gamora owns the simulation-side type (`CommitGradeVerdict` / `SearchGradeEstimate` + provenance markers) in the parallel dispatch `2026-06-13-gamora-wb-typewall-rename.md`; you own the export-side type and the re-typing of the 1D-fed artifact so it cannot masquerade as commit-grade behavioral identity. The drift being closed: `bc_measured_bins.json` is **1D-fed** but its name *invites* an agent to read it as the kit's measured identity — exactly the § 5 violation. The type-wall makes that mis-read a type error rather than a silently-wrong architecture three weeks later.

You already landed the consume-side schema `ExportKitBCMeasuredBin` + telemetry v2.17 this session (tag `star-lord/v-bc-measure-consume-1`). This dispatch fidelity-types that boundary: the *1D-fed* `bc_measured_bins.json` is search-grade; the **commit-grade** BC file is a *different* artifact minted by the spatial path (it does not exist yet — that emission is W-D, gamora+star-lord).

## Required reading before starting

- `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` § 3.1 (type-wall — your export-side bullet), § 3.2 (the artifact table)
- gamora's emit-side type contract: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (the `CommitGradeVerdict`/`SearchGradeEstimate` provenance fields — reconcile your export types to these; if not yet landed when you start, coordinate via KR — your re-type work can proceed on the artifact-naming half in parallel)
- Your own consume schema: `ExportKitBCMeasuredBin` (`star-lord/v-bc-measure-consume-1`)
- `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md` (wave state; arity = 8 — the eventual commit-grade file carries an 8-tuple)

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**YES.** export-side fidelity typing of the gamora→star-lord BC boundary:
- The 1D-fed `bc_measured_bins.json` is re-typed/renamed to advertise `fidelity:"search"`.
- The export-side identity consumer (whatever admits a BC record as behavioral identity) asserts commit-grade provenance and rejects search-grade.

**Round-trip smoke (Principle 6):** Round-trip smoke: take a real 1D-path `bc_measured_bins.json` record through the export consume boundary and assert it is admitted ONLY as search-grade (the identity-admission path rejects it). Use the existing season `kse_20260613_002` BC output as the production-path fixture.

## Scope

> **Gate-1 WARN — dependency split (jack-ryan).** The commit-grade export type MUST match gamora's provenance fields exactly; guessing the shape before D1's MIGRATION lands risks two contracts that *look* reconciled but drift on field names. So:
> - **PARALLEL-SAFE half (start anytime):** the search-grade re-type/rename of `bc_measured_bins.json`.
> - **D1-GATED half (do NOT start until D1's `simulation/MIGRATION.md` provenance section is on disk):** the commit-grade export type + admission rule, reconciled field-for-field to gamora's contract.

- [ ] **[parallel-safe]** Re-type the 1D-fed `bc_measured_bins.json` to advertise search-grade (`fidelity:"search"` field consumer asserts on, OR rename to `bc_search_estimate_bins.json`) — document the choice
- [ ] **[D1-gated]** Mint the export-side commit-grade type matching gamora's `CommitGradeVerdict` provenance contract field-for-field (the artifact it types — the spatial-emitted commit-grade BC file — is produced in W-D; here you define the export type + admission rule). **Do NOT start until D1's MIGRATION provenance section exists.**
- [ ] **[D1-gated]** Export-side identity consumer accepts only commit-grade provenance (search-grade → rejected at the consume boundary)
- [ ] MIGRATION.md consume-side section reconciling to gamora's emit contract
- [ ] Round-trip smoke per Principle 6 (above)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `star-lord/v-wb-typewall-export-1`

## Out of scope (explicit non-goals)

- **Emitting the commit-grade BC file from spatial telemetry** — that is W-D (after the spatial engine works). Here you only define the export TYPE + admission rule.
- **The simulation-side type + rename** — gamora's parallel dispatch.
- **Generation seam** — untouched.
- **Production telemetry.db apply** — remains Matt's ADR-006 gate; do not apply.
- **Pushing to remote** — Matt's keystone/wave-close gate; accumulate commits.

## Open questions for the agent to resolve (document at Gate-2)

- `fidelity` field vs file-rename for the search-grade artifact — pick the one that makes the mis-read hardest; document.
- Whether any existing consumer of `bc_measured_bins.json` needs a shim during the rename — enumerate callsites, document the migration.

## References

- Wave doc § 3.1 (export-side bullet), § 3.2 (artifact table)
- gamora emit contract: `simulation/MIGRATION.md`
- W-C.5 close: `agentic_orchestration/cert-wave-2d-W-C5-close-2026-06-13.md`
- Gate-2: jack-ryan gates the admission rule + round-trip per seam protocol.

---

**Author:** knight-rider, 2026-06-13. The export-side half of the chokepoint type-wall — makes the 1D-fed BC artifact structurally un-admittable as commit-grade behavioral identity.

---

## Completion record

**Completed by:** star-lord
**Date:** 2026-06-13
**Engine commit:** `a89f21a` — star-lord: W-B export-side type-wall — fidelity stamp + ExportCommitGradeVerdictDocument + admit_bc_for_identity
**Tag:** `star-lord/v-wb-typewall-export-1`

### Scope checklist

- [x] **[parallel-safe]** Re-type the 1D-fed `bc_measured_bins.json` to advertise search-grade — DONE. Added `fidelity:"search"` to the document dict emitted by `run_bc_measurement_over_corpus`. On-disk production files (`bc_measured_bins.json`, `bc_measured_bins_smoke_2026_06_13.json`) updated with the stamp. File NOT renamed (see open-question resolution below).
- [x] **[D1-gated]** Mint the export-side commit-grade type matching gamora's `CommitGradeVerdict` provenance contract field-for-field — DONE. `ExportCommitGradeVerdictDocument` in `export/schemas.py`. All four fields reconciled (fidelity/engine/scenario_set_hash/bc_cell). No production mint in W-B; W-D is the production site.
- [x] **[D1-gated]** Export-side identity consumer accepts only commit-grade provenance — DONE. `admit_bc_for_identity()` rejects search-grade (class identity check first, fidelity/engine marker check, non-empty hash check) with `ExportFidelityError` (a `TypeError`).
- [x] MIGRATION.md consume-side section reconciling to gamora's emit contract — DONE. `export/MIGRATION.md §v1.76-wb-typewall-export` includes field-for-field reconciliation table and callsite enumeration.
- [x] Round-trip smoke per Principle 6 — DONE. `test_round_trip_real_1d_bc_file_rejected_at_identity_admission`: real kse_20260613_002 bc_measured_bins.json (96 kits) → `ExportSearchGradeDocument` → `admit_bc_for_identity` → `ExportFidelityError`. PASS.
- [x] AGENT_STATE.md updated at session end — DONE.
- [x] Tag `star-lord/v-wb-typewall-export-1` — FIRED.

### Open questions resolved

**Q1: `fidelity` field vs file rename** — FIELD chosen (both layers: in-file `fidelity:"search"` stamp + class-identity boundary guard). Rename deferred. Rationale: the `fidelity` field is universally readable in any JSON viewer without Python type machinery; all existing callsites read `doc["bc_measured_bins"]` (the list key), not the top-level `fidelity` field — zero breakage from adding the stamp. The boundary guard (`admit_bc_for_identity`) provides structural enforcement by class identity: an `ExportSearchGradeDocument` with forged `fidelity="commit"` fields is still rejected because it is not an `ExportCommitGradeVerdictDocument` instance. MIGRATION.md §v1.76 documents the future rename cleanup path.

**Q2: Existing consumers of `bc_measured_bins.json` needing shim** — None required. Enumerated callsites: `scripts/gamora_bc_adapter_driver_smoke_2026_06_13.py`, `scripts/gamora_bc_measurement_full_corpus_2026_06_13.py`, `scripts/run_items_7_8_measured.py`, `scripts/rocket_defensive_bridge_measure_2026_06_13.py`, and two output artifact metadata strings. All are one-off scripts reading `doc["bc_measured_bins"]`; none inspect `doc["fidelity"]`. No shim needed.

### Test results

- **12/12 new tests PASS** (`tests/test_wb_typewall_export.py`)
- **215/215 combined PASS**, 0 regressions (W-B export + W-B rename + v2.17 BC signals + faction + w093/094/095)

### Gate-2 notes for jack-ryan

1. **Admission rule correctness**: `admit_bc_for_identity` rejects by class identity FIRST (not just fidelity-field inspection). A forged `ExportSearchGradeDocument` with `fidelity="commit"` is rejected. Test `test_search_grade_with_forged_fidelity_still_rejected` verifies this.
2. **Round-trip PASS with production data**: the Principle 6 smoke used the real `kse_20260613_002` on-disk file (96 kits, not a synthetic fixture). `test_round_trip_real_1d_bc_file_rejected_at_identity_admission`.
3. **Field-for-field reconciliation verified dynamically**: `test_provenance_constants_match_gamora_contract` imports from `simulation.verdict_types` at test-time and asserts the four export-side constants match exactly. Drift between export and simulation seam is caught by a live import.
4. **W-D production mint**: `ExportCommitGradeVerdictDocument` has no production mint site in W-B. The positive canary is TEST-ONLY construction. W-D is the spatial mint site.
5. **No drax consumer migration**: `ExportSeason` unchanged. Per ADR-004.
6. **Production DB apply**: telemetry v2.17 still PENDING Matt ADR-006 gate (carry-forward from prior session).
