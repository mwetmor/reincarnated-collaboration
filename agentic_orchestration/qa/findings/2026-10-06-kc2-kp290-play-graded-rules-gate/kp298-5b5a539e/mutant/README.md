# Mutation check of BLOCK-1's closure (scratch only)

Two scratch kc2_play projects (`git archive 534febc kc2_play`, `vendor/kc2_runtime` = `git archive adb3f55 kc2_runtime`
(tree 5b5a539e), `data/` = the arena geometry of record, sha256 68d895d7…). In `play_mut` one line of the vendored
`kc2rt_fight.gd` `_loop_layer_open` was changed: `cp_warcry_auto = play_driver == null` -> `cp_warcry_auto = true`
(the automatic War Cry re-armed in PLAY). Then `tools/kc2p_config_audit.gd -- seed=0 n=1` and
`tools/kc2p_s47_harness.gd -- seeds=0 ablate=arena` ran in each, under the heavy lock.

play_ok: CONFIG-AUDIT GREEN (exit 0); §4.7 GREEN (PLAY cast NEITHER without keys; divergences DR-15).
play_mut: CONFIG-AUDIT RED (exit 1; `cp_warcry_auto` RED); §4.7 RED (exit 1; "PLAY CAST WITHOUT A KEY"; PLAY [47, 0]).
No repository was touched.
