# EN-E4 resume note (R-C9-137, coilseer + gloamwing) — HALTED at the disk gate

**Written:** 2026-10-03 ~01:10Z by drax (EN-E4 resumed lane). **Why halted:** free disk read 19 GiB (`df -h /System/Volumes/Data`), below the 20 GiB gate (R-C9-88). Nothing heavy is running or queued from this lane; the two final chains were stopped while still waiting on the heavy lock (no output written).

## Next step (exactly)
When free disk is back above 20 GiB, launch both final chains (each runs the whole rest of its pack under one heavy-lock hold):

```
cd ~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
nohup python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- zsh work/chain_final_cs.sh > work/chain_final_cs.log 2>&1 < /dev/null &!
nohup python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- zsh work/chain_final_gw.sh > work/chain_final_gw.log 2>&1 < /dev/null &!
```

`work/chain_final.sh` does: 06a/06b bake of the chosen paint (EN4-SLPG_b / EN4-GRPG_b) → n08 blend → rig export to `export/<n>/<n>.glb` (texture embedded via cfg `texture`) → n17 fit → n12 manifest → mk_states → n14 kit → `work/patch_kit_en4.py` (true_size + radii + breath bursts + aura note) → Godot JOIN-1 cells into `join1_pack/en-<n>` → index_cells (+ contact sheet) → validate_sockets → runtime resample → manifest lint with 2 negative controls → stills8 → Godot import check. Read the log end to end; then commit, ledger milestone, hand-back.

## Gloamwing: check after the final chain
- `cfg_gloamwing.json` now has `emerge.wing_open 0.85` (e11 reads it; added in this lane's copy). v3 n17: s_fit 1.0094, with 5 % margin 0.961, binding emerge f0 heading 6 (the spread drop-in wings, NOT the rise -- rise 0.95 changed nothing and is back to 1.2). If the final export's n17 `s_with_margin` is still < 1.0, narrow `wing_open` further (0.75) and re-run the final chain; the raw fit (no margin) is already >= 1.0.
- Known, accepted unless the conductor says otherwise: walk min_z -0.096 m over 3 frames and run -0.093 m over 4 frames (the fore-foot hind talon in swing), run footlock slide 0.10 m.

## State of each creature
| | coilseer | gloamwing |
|---|---|---|
| prep | `builds/coilseer_prep.glb` 2.2 m --height --flip, tail compressed to 2.3 m; s_fit 1.079 (no rescale) | `builds/gloamwing_prep.glb` re-prepped at 3.808 m (5.6 x 0.68 max-fit), --flip |
| rig of record | e10 v3 (`builds/coilseer_rig_v3.glb`): hand gate 0.24 (v2 left palm shards), walk/run amp 0.13/0.16 | e11 v3 + wing_open (to be built by the final chain); leg gate 0.52, motion_scale 0.68, run duty 0.30 |
| canvas | `work/canvas_coilseer_G.png` (layout coilseer_G) | `work/canvas_gloamwing_G.png` (layout gloamwing_G) |
| paint | EN4-SLPG, kept **b** (registration 0.915) | EN4-GRPG, kept **b** (marker fixed; a has an extra band) |

## Path-slip judgement (coilseer)
Lint now splits the slip: `path_slip_body_m` (joints past the 35 % amplitude ramp) and `path_slip_ramp_m`. v2 walk 0.169 / 0.101; v3 (amp 0.13/0.16) walk 0.137 / 0.090, run 0.099 / 0.131. So the 0.26 m in v1 was NOT mainly the ramp: the fixed-length segment chain shortens axially on a steep sine, so joints fall off the path. Judged ACCEPTABLE for v3: at 151 px/m the worst is ~20 px of lateral smear spread over a 1.3-2.1 m wavelength, under the belly and largely hidden by the torso at the 53 deg camera; a true no-slip fix needs arc-length re-parameterisation of the wave (a rig-script rewrite), noted, not done.

## Spend (R-C9-137)
Astra 16/30 (EN4-SL 4, EN4-GR 4, EN4-SLPG 4, EN4-GRPG 4; no usage-limit message). fal $0.80/$1.50. Meshy 0/60.

## Scratch to list for Matt (no deletions by the lane)
- `/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad/` (~1 GB, EN3_TMP render temp)
- intermediate rigs `builds/coilseer_rig_v1.glb`, `_v2`, `_v3`, `builds/gloamwing_rig_v1.glb`, `_v2`, `_v3` (keep the Tripo GLBs)
