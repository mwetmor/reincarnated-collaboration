# JOIN-1: rulebook `06b9bdb3` (PACK_PIN → pack v3, the step-2b population; KP-384), certification

**gamora, 2026-10-08.**
- **Tests:** fail-first, committed alone.
- **Instruments:** the v3 dir and `kc2_rulebook_pack_v3.py` are in B′ `forbidden_dirs` and the witness `FORBIDDEN_DIRS`; pj29 is on v3; G-D3 analysis has CLOSURE + PERIOD.
- **Rulebook:** `06b9bdb3`, PACK_PIN → v3:
  - pack `2713e4cd77353b1fc082ddb163ce179d3d250199997e73e05adc79edb8dc1dec`;
  - manifest FILE `fc3537f0c118e7ea66fa98a39ef64f35f0de099d6b2117bc1fd6d4110e64ed47`;
  - both were copied from the files and asserted verbatim in star-lord's MIGRATION `c55fbce6`.
- **INFO-V3-3:** no rulebook or instrument file reads `offense_da_population.json`. The guard reads `offense_da.json` only, through the pinned re-cut reader, and only after the pack's manifest FILE is checked against the pin.

| | Result |
|---|---|
| `pj29.json` | P-J2-9 30/30 |
| `golden-master/` | 7/7 FILE-equal (sha256 per grain); 0 JOIN draws; `n_outside` 0 in 26/26 records; pack at bind = v3 (digest pin `2713e4cd…`, 13 files tracked = on disk, clean). Bulk at `/Users/admin/Games/join3a-bulk-evidence/pinv3-golden-master-06b9bdb3` |
| `s47v4/` | § 4.7 v4 ORACLE BYTE-IDENTICAL |
