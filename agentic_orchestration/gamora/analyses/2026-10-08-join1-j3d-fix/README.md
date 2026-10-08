# JOIN-1 · J3d fix (jack-ryan J3d close-out WARN-1, collab `62a516076`; KP-404): the NEW J3c pin `3eefaa2eab7d50e94ff9b547b2aa5e67db6473ed`

**The defect.** `pct-resist-only` computed `raw − raw·dr/100`. At dr = 100 this leaves a ±ulp residue on about 13 % of f64 raws (e.g. 3968.871 gives −4.5e-13). A negative residue passes `min(pa, hp)` in `hit_with_proportional` and **heals** an immune body.

**Fix, engine order:**
- fail-first `tests/test_join3d_forms.py::test_pct_resist_only_immune_is_exactly_zero_and_never_negative_on_non_exact_raws`, RED at its commit;
- the rulebook **`3eefaa2e`**: `if dr >= 100: return 0.0`, else `max(0.0, raw − raw·dr/100)`. The diff vs `a8e11af6` is exactly those lines (`rulebook_diff_a8e11af6_3eefaa2e.patch`);
- the grid group `G-L08-immune-residue`.

**Re-certification of `3eefaa2e`:**
- P-J2-9 30/30;
- GM 7/7 FILE-equal (bulk `j3d-fix-golden-master-3eefaa2e`), 0 draws, `n_outside` 0;
- § 4.7 v4 ORACLE BYTE-IDENTICAL.

**Grids (`grids.json`, re-generated at `3eefaa2e`): ALL PASS,** now including `G-L08-immune-residue`:
- 5 non-exact raws × {100, 94 + 6, 130} give exactly 0.0;
- an immune body's HP is unchanged after a 100 % CB.

`pct-resist-only` is ratified (decisions-log `88819d4d`), conditional on this fix.

**The NEW J3c pin: `3eefaa2eab7d50e94ff9b547b2aa5e67db6473ed`** (supersedes `a8e11af6`).
