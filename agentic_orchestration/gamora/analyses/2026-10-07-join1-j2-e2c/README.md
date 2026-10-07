# JOIN-1 · J2-E2c evidence: rulebook forms, § 4.7 v3

gamora, 2026-10-07. **Engine `8f9546b3`, committed ALONE** (7 files: `src/join2_rulebook/{__init__,families,forms,operands,hooks,conversion}.py` and `tests/test_join2_rulebook_e2c_forms.py`).

## Tests

- **Fail-first:** run before the modules existed, the tests gave 1 failed and 24 errors. After: 34 passed. With the W1 and B′ tests added, 62 passed.
- **P-J2-3 (hit grid):** the frozen 440-row `join1-hitchance-grid-v1` was re-derived through `forms.resolve_hit` / `forms.probability_to_hit`. Every field is bit-exact. The ROWSET, recomputed under the grid manifest's own law, equals `eaf31884…` (the I-4 derivation).
- **P-J2-4:** 0 differing bit patterns across:
  - `mitigate`: every `RESIST_PCT` family × 11 damages × 2 caps × 2 bonus sets, with and without an `IntakeFold`, the fold telemetry compared too; the unmapped family raises with the sealed message.
  - `physical_applied`: every absorption limb × order × region × `global_flat`.
  - `resolve_hit`: 18 PTH values, including the `nextafter` edges of 55 and 70, × rolls 1–100.
  - the two boards (all offense keys, by identity; 2,000 summon keys).
  - `applied_damage`.
  - the summon adapter (sealed signature).
  - Soulfire and bleed, every w155 record plus one absent record.
  - `pth_for`.
  - 20,000 random intercepts.
  - `__post_init__` (GD is a no-op; kit AS 200 gives 200/196).

## § 4.7 (v3 script, `s47v3/s47v3_evidence.json`): **ORACLE BYTE-IDENTICAL**

- **HEAD:** start = end = `8f9546b3`; the kc2 tree is `7496a28a` at both ends.
- **Limb A:** canonical `f04ef6d0…` on both sides.
- **Limb B:** pass.
- **Limb B′:** pass.
  - Path hits: 0 sealed, 0 HEAD.
  - Census equal.
  - Witness: 2 of 2 children, no hits.

## Flagged for the conductor and J3

- **L-08 and L-17 defaults are PROVISIONAL.** The record names them as declared-invented instances but gives no value. I declared `yes` for L-08 and `off` for L-17, each with its reason, so J3 must ratify or replace them.
- **The referent's conversion row is UNSTAMPED under the dual-column law.** The reader is column-agnostic, so a caller that holds to `rdr_value` needs a stamping rule from elrond, or the reader refuses.
