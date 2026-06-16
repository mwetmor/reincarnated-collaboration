# Finding — 2026-06-16 — star-lord W-D export-side consume wiring

**Reviewer:** jack-ryan (DEV-MODE, Gate-2)
**Severity:** PASS-WITH-INFO
**Target:** engine commit `2a91d50`, tag `star-lord/v-wd-export-1`
**Developer:** star-lord
**Dispatch:** `agentic_orchestration/dispatches/2026-06-13-star-lord-wd-export.md`
**Principles applied:** Principle 3 (cross-seam impact), Principle 4 (decisions-log/cert as truth), Principle 6 (cross-seam round-trip); Disciplines #1 (math/contract-before-code), #8 (schema validation at boundaries)

## Verdict: PASS-WITH-INFO

All five dispatch deliverables independently verified. The §6.4-open provenance-not-identity
semantics are genuinely enforced in code. Round-trip + full export-boundary suite re-run clean.
Additive migration is non-breaking and confirmed NOT applied. Two INFO notes (neither blocking).

## What I found

**1. Consume boundary (verified).** `consume_spatial_commit_grade_verdict(raw_verdict: dict) ->
ExportCommitGradeVerdictDocument` exists in `export/schemas.py`, exported from `export/__init__.py`
and reachable via `export.consume_spatial_commit_grade_verdict`. It constructs the document from
the raw dict and routes through the pre-existing `admit_bc_for_identity()` boundary, which validates
fidelity==commit, engine==spatial, and non-empty scenario_set_hash. Field-for-field reconciliation
to gamora's v1.31 emit contract holds: the real CGV record carries exactly `fidelity`, `engine`,
`scenario_set_hash`, `bc_cell`, plus extra `kit` (tolerated via `model_config={"extra":"allow"}`,
verified on the type).

**2. §6.4-open semantics (the crux — verified TRUE in code).** Enforcement is by ABSENCE, which is
the correct model: there is NO `identity_certified`, `measures_the_kit`, or `bc_identity_truth`
attribute on `ExportCommitGradeVerdictDocument`, on `admit_bc_for_identity`'s return, or attached by
the consume function. The document carries only provenance (fidelity/engine/scenario_set_hash/bc_cell/
payload). You cannot advertise an identity stamp that does not exist. The negative-assertion tests
use `getattr(admitted, "<attr>", False)` so they will FAIL the day anyone attaches such a flag —
a durable guard, not a one-time check. star-lord's claim is accurate.

**3. Round-trip smoke (re-run by me, verified).** Tests load the REAL `commit_grade_verdict` record
from `output/wd-six-axis-measure-2026-06-13.json` (gamora 5ec33bb; kit K2_radius_aoe;
scenario_set_hash `bcc55cf1edc05d3f`; bc_cell 8-element list) — not a synthesized fixture. I re-ran:
`pytest tests/test_wd_consume_boundary.py` -> 11/11 PASS. Combined export-boundary set
(wd_consume + typewall + commit_grade + admit_bc + export_fidelity) -> 34 PASS, 0 failures, 0
regressions. (star-lord reported 32/32 combined; my keyword filter is slightly broader at 34 — no
discrepancy, just a wider selector. Zero failures either way.)

**4. Additive migration (verified safe + NOT applied).** `_V2_18` in `telemetry/migrations.py`:
`ALTER TABLE spatial_fight_results ADD COLUMN total_displacement REAL NOT NULL DEFAULT 0.0`,
registered in MIGRATIONS as "2.18". DDL is ADD-only; the only `DROP` token in the block is inside
the documented reversibility comment, not executable DDL. Default-neutral (0.0) — zero data loss,
zero semantic shift on pre-W-D rows. Not-applied confirmed empirically: production `./telemetry.db`
is 0 bytes; every DB where `spatial_fight_results` exists (`data/telemetry.db`,
`src/reincarnated/telemetry/telemetry.db`) has `total_displacement` ABSENT from the column list.
Apply correctly deferred to the ADR-006 gate (same gate as pending v2.17).

**5. MIGRATION.md (verified present).** `export/MIGRATION.md §v1.78-wd-export-consume` authored with
field-for-field v1.31 reconciliation, §6.4-open guard, additive-migration disposition, and round-trip
result. Cross-seam handoff documented per ADR-004.

## Rationale

Principle 6 (cross-seam round-trip) is satisfied with a real spatial-emitted artifact, not a fixture
— the strongest form of the smoke gate. Principle 4 (cert/decisions as truth) is honored: the D1 hard
constraint from `cert-wave-2d-W-D-close-2026-06-13.md` (§6.4 stays OPEN until W-F) is enforced in code
by the absence of any identity-truth attribute, and the consume docstring explicitly enumerates the
wired-but-not-discriminating axes. Discipline #8 (schema validation at boundaries) is met by routing
through `admit_bc_for_identity`. No conflict with any locked decisions-log entry.

## INFO (non-blocking)

- **INFO-1 (stale docstring in a pre-existing function).** `admit_bc_for_identity` (NOT authored in
  this commit; W-B-era) contains the usage comment "safe to use committed.bc_cell as the kit's
  behavioral identity coordinate" (schemas.py ~line 1046). That phrasing predates the §6.4-open
  constraint and reads as identity-truth language. It is a comment only — no code attaches an identity
  stamp, so it does not affect the verdict. Recommend star-lord soften this comment to
  "provenance-grade coordinate; not identity-certified until §6.4 closes at W-F" on a future touch of
  this function, to keep documentation aligned with the cert state. Not this developer's regression.

- **INFO-2 (v1.31 numbering collision in gamora's MIGRATION.md).** `simulation/MIGRATION.md` has TWO
  entries headed v1.31: the stale 2026-05-27 "Cycle 13 Option A Remediation" (line ~3909) and the
  real W-D emit contract (line ~7396, 2026-06-13). star-lord consumed the correct one (the field
  contract matches the real record exactly), so this is not a defect in this commit — but the
  duplicate version label is a latent ambiguity in gamora's seam. Flag to gamora for a future
  re-number/disambiguation; cross-seam contract version labels should be unique.

## Action

- [ ] star-lord (optional, non-blocking): soften the INFO-1 stale comment in `admit_bc_for_identity`
      on next touch of that function.
- [ ] gamora (optional, non-blocking, routed via KR): disambiguate the duplicate v1.31 label in
      `simulation/MIGRATION.md`.
- [x] Gate-2 verdict rendered: PASS-WITH-INFO. Tag `star-lord/v-wd-export-1` clears the consume
      boundary + round-trip + additive-migration scope. No BLOCK; no Matt escalation required.

## References

- `reincarnated-engine/src/reincarnated/export/schemas.py` (consume fn + ExportCommitGradeVerdictDocument + admit_bc_for_identity)
- `reincarnated-engine/src/reincarnated/export/__init__.py` (export of consume fn)
- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (_V2_18)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (§v1.78-wd-export-consume)
- `reincarnated-engine/tests/test_wd_consume_boundary.py` (11 tests, re-run PASS)
- `reincarnated-engine/output/wd-six-axis-measure-2026-06-13.json` (real CGV round-trip source)
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.31 (line ~7396, W-D emit contract)
- `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md` (D1 hard constraint, §6.4 open)
