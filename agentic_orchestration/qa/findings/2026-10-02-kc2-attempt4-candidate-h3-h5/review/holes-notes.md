# H-5 holes re-assessment at fd799b63 under V311-FULL (HOLES fork notes; read-only, no Godot run)

Source: archive of godot 96fc0cc (`kc2_runtime/`, digest fd799b63, 107 members). G3 evidence was read through git objects at ef5c04a: `evidence/kc2-play/2026-10-02-g3-25cell-kp261-V311FULL-96fc0cc/`.
Classes: **L** = live on the graded path; **S** = superseded by a v3.8–v3.11 fold; **P** = partial.

## Fold branch points (kc2rt_fight.gd unless noted)

- **GD engagement, roster.** At `:3163-3203`, when `ge_roster` holds, a roster body's opportunity comes from `ge_fold.is_opportunity` and its slot from `ge_fold.choose_slot`. `_choose_slot` is bypassed. Pets still take `_choose_slot` (`:3204-3218`).
  - GD `_choose` is at `kc2rt_gd_engage.gd:364-392`: SPECIAL_ORDER (special1-5, tree_attack), then NORMAL_ORDER. Its chance gate is `> chance → skip` on rg1 V311-RG-005, and its cooldown/delay uses half-to-even ticks.
- **Pursuit.** At `:2719-2754`, `halt_for` and the waypoint replace the 2.4 m halt.
- **Pilot.** At `:2491-2493`, P-MOVE (`pmove_fold`) returns before `_oracle_drive_step`, K_MILL and MovementPolicy.
- **Crowd.** At `:7350`, `ge_fold.crowd` replaces the symmetric converging solver with GD `separate`.
- **Damage.** Composition `:5858-5862` and mutators `:3826, 3846, 5479-5483, 5729-5748, 5852, 6040, 6083` sit on top of `_apply_slot`.
- **Line-up.** At `kc2rt_board.gd:641-650`.
- **dc1.** Scan at `:7585-7600`, initial self-cast at `:7602-7609` and `aura_slots :3253`.
- **Wave open.** `_v3p11_wave_open` (`:7695`) is called from `run()` `:1569` and from `_play_enter_wave` `:1689`.

## Item table

| item | class | graded pin at fd799b63 |
|---|---|---|
| H1 PCL | L | `pcl_rows_untouched` (composition does not touch PCL); hole probe at V38-RS reaches the same code; G3 HP |
| H2 death after heal | L | death order is independent of the folds; HOLE 2 probe; G3 death wave+tick on 5 dying cells (was 25) |
| H3 damage-row grouping | L (+ GD Default rows for u5 HONEST-FAIL, `:7756`) | G3 dmg_sources; v3p11 B4-3 covers the Default slot shape only. **No probe pins the HONEST-FAIL arming** |
| H4 tree_attack | **P**: roster S (GD `_choose`, tree_attack in SPECIAL_ORDER); pets L | roster: G3 only (draws at V311-RG-005, dmg_sources). No probe/control on GD `_choose` |
| H5 dying · 5b | L | `_fire_dying` unchanged; probe re-derived 14→26 (v3.8 reach, oracle count); G3 |
| H6 chance/cooldown/delay | **P**: roster S (`gd_engage.gd:376-386`, `choose_slot :455-458`); pets L | roster: G3 only |
| chance gate | **P** (two implementations: legacy for pets, GD `_choose` for roster) | same `>` convention in both; boundary U-3 un-exercised in both; no GD-half probe |
| H7 march base | L (`ge_speed` = run_speed × monster_speed_base) | G3 positions bit-exact |
| H8 to-hit | L (refactored into `Kc2RtLaws.resolve_hit`, 751b92d) | hit grid ROWSET; G3 |
| H9 mitigation order | L (mutator `resist_kw` added on top) | G3 HP |
| H10 DoT bucket | L (composition `dot` on top) | G3 |
| H11 crit tier | L | hit grid; G3 |
| H12a motion order | L | G3 positions |
| H12b contact fold | **S** (crowd `:7350`) | v3p11 B4-6 (bit-equal to CPython) + B4-7 control; G3 positions bit-exact. Native contact shadow compares 0 ticks |
| H13 Soulfire/bleed | L (Cruel factor on top) | G3 |
| H14 pets | **P** (GD `pet_target`/slots/RFA in `_pet_motion` `:4102`) | G3 pet_set; petpath shadow |
| H15 resist cap | L | G3 |
| H16 S1/O1 | L (GD `busy_until` uses `swing_ticks_of` → `_swing_ticks` with the mult `:3349`; the swing pause sits on top) | G3 |
| H17 monster life LO | L (C-11b scales on top) | G3 |
| C-11a grant law | L | G3; v3.6 probes at V38-RS reach the same code |
| KP-144 (a) board seed | **P** (line-up fold picks the keys) | G3 board class; v3p11 C1 |
| energy · wave poll · deferred · counterplay · tps · float64 | L | G3 |
| pilot DrivePolicy + ChannelPolicyFold | **P**: drive S (P-MOVE `:2491`), channel L | v3p11 B5; G3 drive_target (P-MOVE target) + channel |
| player summons | L (casts 3 per cell) | G3 |
| player raw | **P** (mutator player factor `:5479-5483`) | G3; v3p11 C2 |
| KP-147 count-law Adj · alert · control · kvec · banner · W1 · zero injections | L | G3 native-fold line: count_adj 79-80 · alert 71-76 evals · control inserted Σ20 · kvec · banner on 25/25 |
| KP-147 K_MILL + MovementPolicy | **S** (P-MOVE) | v3p11 B5; G3 player position. "K_MILL true" in the G3 log means bound, not stepped |
| patrol leg (U-5) | unported | 0 gate-closed body-ticks on 25/25 V311-FULL G3 cells (logs) |
| KP-150/152 closure items | L except `PX-LO` (K_MILL driver literal: S) | v3.7.1 probes now load the **v3.7.1 pack** (`MODEL_DIR_V3P7P1_SUPERSEDED`), not the graded pack; the graded pack's closure is the v3.11 loader section (L) |
| KP-167 leak | L | TA-X-07 (EXACT) |
| KP-177 TA-X-08 lethal tick | L | **the attempt-2 T8 real-cell pin is RED by population** (cell M-POL-2 s0 w151-153 no longer dies); pinned instead by H-4 constructed cells (dying + cleared) + G3 census EQUAL on 5 dying cells |
| KP-177 PRE_FIGHT · P-2 · KP-180 counters | L | H-4 cleared-cell check (PRE_FIGHT 10); G3 |

## Legacy probe diffs ff6b267..96fc0cc

- hole / v3.6 / completion / loop / v3.7: each adds `fight.set("oracle_level","V38-RS")`, and the completion/v3.6/v3.7 revision lists gain v3.8/v3.11 (this keeps the WIRED branches running).
- hole: `EXPECT_DYING_REACH_DOMINATES` 14→26, re-derived off the oracle; the old value is kept as `_SUPERSEDED`. Not a narrowing.
- v3.7.1: pins re-pointed to `*_V3P7P1_SUPERSEDED`. The probes still load and test the v3.7.1 directory, so they no longer touch the graded pack. Scope changed; no assertion weakened.
- No assertion text was removed from these six files.
- H-4 probe: 39→38 labels (re-point to v1.14/v1.15). Removed or merged:
  - the KP-158 setup tick-probe-row exclusion (superseded by the v3.11 setup partition check);
  - the separate TA-X-18 repr check (folded into H-4 (7) bits);
  - `read_pinned` refusal-controls presence;
  - "exact β agrees with float β to 1e-9".
  - `g3_block` still conjoins census, control term, shadow, oracle_complete, POST and death (`kc2rt_h4.gd:598-601`).
- `shadow_ok` does not require any comparison to have happened. Contact ticks compared are 0 under V311-FULL, and placements and petpath calls have no `> 0` floor. `native_shadow.mismatches_all_zero` reuses `all_ok` (mislabelled; conservative).

## U-list at V311-FULL

- **U-1:** `play_step` runs the same `_tick()` and wave-open hook. No suite probe runs it at V311-FULL (the HOLE 2 both-loops probe is at V38-RS). The kc2_play .app is not re-vendored. H-8 is still the only exerciser.
- **U-2:** unchanged. G3 now has 5 dying cells, not 25.
- **U-3:** now two implementations; the GD half has no probe.
- **U-4:** unchanged.
- **U-5:** 0/25. The `_pursue_one` comment ("43.8 m wall keeps every body inside") is stale: M0/M-POL-2 have no wall in the oracle (KP-252). Under reposition the 80 m test is against the step target (waypoint).
- **U-6, U-7:** unchanged.
- **New:** the GD sub-states (WaitToAttack, RFA, stuck/goal pathfail, roam, D8 whiff, pet_target) have no probe and no telemetry in the G3 summaries (`v3p11` carries composition/rows only). Only drax's commit text shows that petpath goal hits are reached.

## R-6 WARN-1 and INFO-1 (my d03ca891 actions for "the next runtime change")

- `r6_invariants` (ii) is unchanged at `tests/kc2rt_ta_emit.gd:2037-2043`, so it is still blind.
- Stale labels are still present: `kc2rt_fight.gd:7112` ("NOT MODELLED") and `:510-511` ("HALTED").
- **Not discharged** at this runtime change.

## Declared reds

- **attempt-2 T8** (`kc2rt_attempt2_probes.gd:126-175`): the population precondition (the cell must die in w151-153) is ill-posed under V311-FULL (waves about 2.3× longer; 20/25 clear w160). The lethal-tick assertions depend on it. This is a fixture defect, not a port regression; G3 census on the dying cells covers the property.
- **runtime_header ×2:** not just environment. `kc2rt_ta.gd:216-232` appends an emission failure (exit 1, `:282`) unless the .app is RE-VENDORED at fd799b63 with pack v3.11. The .app is not rebuilt (7eda88d message; KP-252 item 2). This is a pre-attempt build step.
