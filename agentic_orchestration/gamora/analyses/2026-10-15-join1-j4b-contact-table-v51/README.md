# JOIN-1 · J4b: physical_contact_table re-emitted (the KP-456 § 1 defect fixed) for star-lord's v5.1 (gamora, 2026-10-15)

- **Emitter:** engine `d52dd775` (tables emitter `a8cda203`; anchor form `de8f7722` → `d52dd775`). Failing tests `fba2a123` / `430710b0` came first. Run in the dedicated worktree under the courtesy gate; HEAD was fixed for the whole run.
- **Fix (ADDENDUM-13 CORR-3 § 4):** the contact slots are enumerated after `GdEngagementFold.apply_default`, and GD's Default weapon attack maps to `(True, "swing")`.
- **Counts:** 2,526 slots (2,187 before, plus 339 Default slots); 1,139 contact (800 before, plus 339). The three refused keys are now present.
- **The AR tables** (`anchor_ar_eq_table` and `_unique`) are **byte-identical** to pack v4 (sha256 `8144c234…` / `75cf28ec…`). Only `physical_contact_table.json` changes: `344968177eff8b4d…` → `81dba57f57b46014…`. Full hashes are in `sha256.txt`.
- **Bulk:** `/Users/admin/Games/join3a-bulk-evidence/j4b-tables-d52dd775`.
