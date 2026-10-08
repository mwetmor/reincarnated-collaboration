# JOIN-1 · J3a AMENDMENT-4: certification of rulebook `ea28195a`

**gamora, 2026-10-08.** The doc is engine `06d6db42`, the instrument + tests are `baec5c0d`, and the rulebook is `ea28195a`.

**What the rulebook adds (observational counters only):**
- `lane_landed`;
- `stash_hist`;
- the row-33 read-back counters;
- the id-reuse-safe Soulfire anchor `crit.note_sf_rows`.

PACK_PIN stays on v2.

| | Result |
|---|---|
| `pj29.json` | P-J2-9 30/30 |
| `golden-master/` | 7/7 FILE-equal (sha256 per grain), 25 cells, HEAD fixed, instrument pinned; 0 JOIN draws, empty `decoded` / `stash_hist`, `row33_stash_mismatch` 0 in 26/26 records. Bulk at `/Users/admin/Games/join3a-bulk-evidence/amd4-golden-master-ea28195a` |
| `s47v4/` | § 4.7 v4 ORACLE BYTE-IDENTICAL |

**Not run:** the four deferred controls (C-INTAKE-NC, C-SUMMON-NC, C-L06-3, C-L06-4). See AMENDMENT-4 § 5 HOLD and `../2026-10-08-join1-gd3/README.md` (the guard-coverage finding). NC-J3-L06-RT runs after them, at whatever rulebook is then of record.

**INFO-V2-3:** the sealed referent's `fixture.CRIT_DAMAGE_PCT` is **12** (the Visor alone), not 57 or 69.
