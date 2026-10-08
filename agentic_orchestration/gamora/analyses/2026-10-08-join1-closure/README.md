# JOIN-1: certification of rulebook `15611d0a` (the step-2b closure tally; KP-381)

**gamora, 2026-10-08.** The fail-first test is engine `8b7471ea`; the rulebook is `15611d0a`.

**What `15611d0a` adds:** `crit.lookups`, which counts every player-offense lookup at:
- row 32 `damage_against` (counted before the guard refuses);
- `soulfire_applied`;
- `bleed_dps_against`.

Any (record, wave) outside the guard's sourced set is counted in `n_outside`. The counter is observational. PACK_PIN was v2 at this commit.

| | Result |
|---|---|
| `pj29.json` | P-J2-9 30/30 |
| `golden-master/` | 7/7 FILE-equal (sha256 per grain); 0 JOIN draws. **Closure self-check at GD: `n_outside` = 0 over 829,625 lookups in 26/26 records** (damage_against 201,029 · soulfire_applied 264,598 · bleed_dps_against 363,998). Bulk at `/Users/admin/Games/join3a-bulk-evidence/closure-golden-master-15611d0a` |
| `s47v4/` | § 4.7 v4 ORACLE BYTE-IDENTICAL |

**INFO-2 (KP-382):** I re-ran census cell M0|0 from the committed `604a5d2f`. Its output is byte-identical to the census of record (sha256 `7f5783c3…`).

Superseded as the rulebook of record by `06b9bdb3` (PACK_PIN v3).
