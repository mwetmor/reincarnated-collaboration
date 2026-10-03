# Mutant check of BLOCK-1's probe (M), scratch only

`git archive 66605a1` into scratch, then lines `kc2rt_fight.gd:3834` and `:3854` were reverted to the pre-fix fresh read:
`d = d * mut_fold.player_factor(run_tick - _wave_start_tick)` and `dps = dps * mut_fold.player_factor(run_tick - _wave_start_tick)`.
Then `tests/kc2rt_v3p11_probes.gd` was run under the heavy lock. Result: (M2) FAIL (got 1091.52, want 1186.43) and the (M3) control
fails to go RED. v3.11 PROBES RED, 81 checks, 2 failures, 27/28 controls. The probe discriminates the defect on the bleed path.
The repository was not touched.
