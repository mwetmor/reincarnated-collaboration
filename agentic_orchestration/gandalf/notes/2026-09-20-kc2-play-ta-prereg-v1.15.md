# KC2-PLAY · T-A PREREGISTRATION **v1.15**: Q104 RULED (Matt, KP-240) · `TA-X-30` RESTATED ON THE ORACLE's OWN PER-STEP HALT OPERAND · `TA-X-29(b)` RESTATED TO `CompositionFold` · LAW (a) ON BOTH: PASS 25/25 · EVERYTHING ELSE FROZEN AS v1.14

> ⚑ **STATUS: IMMUTABLE ON COMMIT. v1.15, authored 2026-10-02. Q104's SUCCESSOR. SUPERSEDES v1.14 ONLY IN THE TWO ROWS BELOW.**
> *(The filename carries the series' `2026-09-20` prefix.)*
>
> ⚑ **CARRIES v1.14 BY FILE: `5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92`** (`agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.14.md`,
> collab `4d64316d`). **Every row, value, tolerance, pin, precondition, the budget and every rule of v1.14 is carried
> unchanged, except `TA-X-29` clause (b) and `TA-X-30`, which this file restates by Matt's ruling.** A grader holds v1.14
> for everything else and this file for those two rows.
>
> ⚑ **MATT, Q104 (KP-240), both of gamora's option (i):** *(1) TA-X-30: restate (a) on the oracle's own per-step halt operand,
> read from the pack's `gd_engagement` / `gd_reposition` rows; the travel law's FORM `travel = min(v·dt, max(0, dist − op))` is
> unchanged and only its operand moved; grade (b) under the R-G4-V311 reading, with its vacuity outside W1 printed on the face.
> (2) TA-X-29: restate (b) to `CompositionFold` (its LO physical limb and the declared SlowChaos/SlowAether divisor); carry
> (a), (c), (d); carry (e) at the v1.14 re-derived values (w159 3.197066, w160 4.935649), its definition stated as the
> loader-built static supply.*
>
> ⚑ **LAW (a) (KP-178) ON THE TWO RESTATED ROWS: BOTH PASS ON THE ORACLE OF RECORD, 25/25** (`V311-FULL` + `graded_arm`, five
> arms × five salts, leg A, the OBS-1 completeness guard holding on 25/25; § K′). With v1.14 § K's 26 passing rows, **the
> oracle passes all 28 EXACT rows of v1.14 + v1.15.** **No tolerance moved. No expected value was set from port output.**
>
> ⚑ **THE BUDGET IS v1.14's, UNSPENT: a fresh 2.** The next graded run is **attempt 1 of 2 (overall 4)**, under v1.15 (carrying
> v1.14). § G.1a's 28-row pre-attempt read is a precondition (Matt Q96.3, carried).
>
> **Authority:** Matt Q104 (KP-240); everything v1.14 cites. **Author:** gamora, Run KC2-PLAY; conductor gandalf. Instruments:
> `agentic_orchestration/gamora/analyses/2026-10-02-kc2-play-prereg-v1.15/`, committed first and separately (D4).
> v1.14 and every earlier version are NOT edited.

---

## § 0 · THE v1.14 → v1.15 DELTA

| id | v1.14 | **v1.15** | Δ | authority |
|---|---|---|---|---|
| `TA-X-30` | ⛔ HALTED (Q104): (a) halts at 2.4; (b) halted beyond 2.4 == 0 | ⚑ **RESTATED** (§ F.2i′): (a′) the travel law with **the step's own operand**; (b′) the R-G4-V311 count == 0, vacuity printed | operand only; FORM unchanged; tolerance exact, unchanged | Matt Q104(1) |
| `TA-X-29` | ⛔ HALTED (Q104): (b) `Z5-LAW` verbatim | ⚑ **(b′) RESTATED to `CompositionFold`** (§ F.2h′); (a), (c), (d) CARRIED; (e) CARRIED at **3.197066 / 4.935649**, definition stated | (b) law; (e) values as v1.14 re-derived; tolerances unchanged (exact / `|Δ| ≤ 5e-4`) | Matt Q104(2) |
| every other row, precondition, pin, the cap, § G.1a, § F.5 rules 1–15, § C.9 incl. C.9.8 / C.9.9 | as v1.14 | **CARRIED** | none | — |

**Discipline #12, named twice:** `TA-X-30`'s operand moves from a constant (`arena.json :: d_engage_m`) to a per-step quantity
the oracle computes from pack rows; `TA-X-29(b)`'s composition law moves from `Z5-LAW` to GD's additive form. Both are
semantic restatements by Matt's ruling, derived from the oracle's code and checked on the oracle before commit.

---

## ⚑ § F.2i′ · `TA-X-30` RESTATED: THE TRAVEL LAW ON THE ORACLE's OWN PER-STEP OPERAND

### F.2i′.1 · The law (every arm, every salt, leg A; exact)

**(a′) Every body's pursuit step obeys `travel = min(v·dt, max(0, dist − op))`**, centre to centre, with `op` the operand
**that step** carries, `dist` the distance from the body to the step's target, and **halt ⇔ `dist − op ≤ 0`** (inclusive, exact,
no epsilon). The applied travel equals the law **unless** the non-penetration clip shortens it (then strictly shorter, on the
same ray) or a hold zeroes it (emergence, the stationary plant, the mech/latency hold, AlertBeforePursue: then 0). The
post-step position is `pre + unit(target − pre)·travel`. **NaN is tested explicitly** (a NaN operand or distance is a RED).

**The operand, per body class, as the v3.11 oracle computes it** (`gd_engagement.halt_for`, `gd_reposition.waypoint` /
`pet_target`, `run.py` at `969fbd8d`) — **and where each input comes from in the pack:**

| body / step | target | `op` | inputs, from the pack |
|---|---|---|---|
| roster, GD state **Attack** | the player | the current centre distance (the body stands: travel 0) | — |
| roster, GD state **Pursue**, no reposition waypoint | the player | `reach(S) × (1 − 1e-9)`, `S` the chosen slot | `reach(S)` below |
| roster, **reposition waypoint** (slot / RFA / WaitToAttack roam / move-to point) | the waypoint | **0** | a Pursue waypoint stops where CloseEnoughToUseSkill(S) first holds: `reach(S)` below |
| roster, no GD state or no skill | the player | the ring halt radius **2.4** (`arena.json :: d_engage_m`) | `arena.json` |
| pet, **melee** (`pet_target` returns a point) | that point | **0** | the pet's Normal slot reach enters through the stop point (as above) |
| pet, otherwise (`pet_target` returns `None`, the incumbent walk) | the player | **2.4** (`D_ENGAGE_M`) | `arena.json` |

`reach(S)` = `monster_offense.json :: ⚑ v3p8_rows.gr2_gd_fire_range` **`gd_use_range_m_HI`** for `(record, slot, skill)`; for
GD's Default attack (`defaultweaponattack.dbr`) `= ladder Melee 1.25 (math_rules ⚑ v3p8_rows.gr1 V38-GR1-LADDER-MELEE) + r_body
+ 0.336 + tolerance 0.5 (V38-GR1-TOLERANCE)`, `r_body` = the record's `monster_actor_radius_m × monster_scale` from its `gr2`
rows (0.5 where it has none, the fold's counted fallback); for a slot with no `gr2` row, its packed `reach_m` (the v3.7.1
base row, unchanged). **The halt's 2.4 survives only where the oracle still uses it** (no GD state; the incumbent pet walk).

**(b′) R-G4-V311** (the conductor's KP-191 R-G4 law bound to the v3.11 mechanics): `n_bodies_halted_beyond_d_engage` = the number
of distinct roster bodies with at least one **player-targeted, non-waypoint, non-hold, non-emerging** step that
`ArenaFold.clamp_body` stopped with pre-step distance **> that step's own `op`**. **Expected `0`, every cell.**
⚑ **VACUITY, PRINTED ON THE FACE (Matt Q104(1)):** only an armed `ArenaFold` can clamp. **(b′) is vacuous on every cell of
`M0`, `M-POL-2`, `M-POL-2-NULL` and `W1-NULL` (20 of 25) and tested only on `W1` (5 of 25).** The face prints, per cell,
`arena_armed` and *"(b′) vacuous: no armed wall"* where it is.

### F.2i′.2 · ⚑ THE EMISSION (the operands drax's harness emits, § Q104.4 item 11 of v1.14, by name)

Per cell, `cell.json :: pursuit` (replacing v1.13's block; `n_bodies_halted_beyond_d_engage` keeps its name, under (b′)):

```
pursuit.n_bodies_halted_beyond_d_engage   int   (b′) R-G4-V311, distinct roster bodies
pursuit.arena_armed                       bool  an armed ArenaFold exists on this cell
pursuit.r_g4_vacuous                      bool  == not arena_armed
pursuit.travel_law.n_player_arg_steps     int   roster steps whose target is the step's player_xy argument (incl. waypoints)
pursuit.travel_law.n_unclipped            int   ... neither clipped nor held
pursuit.travel_law.n_unclipped_law_exact  int   ... whose applied travel == min(v·dt, max(0, dist − op)) bit for bit
pursuit.travel_law.n_clipped              int   ... shortened by the non-penetration clip
pursuit.travel_law.n_clipped_shorter      int   ... strictly shorter than the law, on the ray
pursuit.travel_law.n_held                 int   ... zeroed by a hold
pursuit.travel_law.n_held_zero            int   ... with applied travel exactly 0
pursuit.travel_law.n_halt_flag_mismatch   int   halt flag != (dist − op <= 0)
pursuit.travel_law.n_position_mismatch    int   post-step position != pre + unit·travel
pursuit.travel_law.n_nan                  int   NaN operand or distance
pursuit.operand.n_attack_stand            int   op == current distance (Attack)
pursuit.operand.n_pursue_reach            int   op == reach(S)·(1 − 1e-9)
pursuit.operand.n_default_ring_halt       int   op == 2.4 (no state / no skill)
pursuit.operand.n_waypoint_op0            int   waypoint steps, op == 0
pursuit.operand.n_waypoint_reach_gr2 / n_waypoint_reach_default / n_waypoint_reach_packed   int
pursuit.operand.n_reach_ne_pack           int   reach(S) != the pack value of the table above
pursuit.operand.n_op_ne_rule              int   op != the table's rule for its class
pursuit.pets.n_steps                      int
pursuit.pets.n_no_travel_by_law           int   dist <= op or speed <= 0
pursuit.pets.n_moved_law_exact            int   applied == law, bit for bit
pursuit.pets.n_moved_clipped_shorter      int
pursuit.pets.n_moved_against_law          int   moved where the law says no travel
pursuit.pets.n_op_incumbent_2.4 / n_op_pet_target_0   int
pursuit.pets.n_reach_ne_pack              int   pet Normal-slot reach != its gr2 value (where a row exists)
manifest pursuit.ring_halt_m              2.4, read from arena.json :: d_engage_m ; manifest pursuit.nan_test (carried)
```

**GREEN iff, on every cell:** `n_unclipped_law_exact == n_unclipped`; `n_clipped_shorter == n_clipped`; `n_held_zero ==
n_held`; `n_halt_flag_mismatch`, `n_position_mismatch`, `n_nan`, `n_reach_ne_pack`, `n_op_ne_rule`, `pets.n_moved_against_law`,
`pets.n_reach_ne_pack` all `0`; `pets.n_moved_law_exact + pets.n_moved_clipped_shorter + pets.n_no_travel_by_law == pets.n_steps`
(a ghost pet's move read at the next tick's occupancy build counts in `n_moved_law_exact`); `n_player_arg_steps > 0`; **and**
`n_bodies_halted_beyond_d_engage == 0`. The counts themselves are realisation-dependent and are **printed, not expected**;
the oracle's are below for reference only (§ K′). A missing field is a RED on presence (the v1.8 § F.2f rule), not an
UNGRADEABLE.

⚑ **What the row now proves, and what it does not:** that every step the port takes obeys the travel law against **the
operand it computed**, and that operand obeys the table. **Whether the port's GD state (Attack/Pursue), chosen slot and waypoint
equal the oracle's** is G3's (`alive_set`, `body_xy`, `drive_target`, on the oracle's draws), not this row's.

---

## ⚑ § F.2h′ · `TA-X-29` RESTATED IN CLAUSE (b); (a), (c), (d), (e) CARRIED

| clause | v1.15 | class | tolerance |
|---|---|---|---|
| (a) | **CARRIED** (v1.8 § F.2h): `PRED-GMAG-WHOLE` TRUE: attribute limb 193 records (154 Lap O), own limb 527 (104); grain label 193 / 344 | integer counts | exact |
| ⚑ **(b′)** | **THE COMPOSITION LAW IS `CompositionFold`** (`gd_composition.py` at `969fbd8d`; Matt Q98; pack `V311-CG1-09`), with `P = om − 1` (`om` from the global-magnitude fold, which stays armed): **instant rows** (`direct`, `leech`), non-physical: `m · max(0, a + P)`; **physical, clamped** (`t = 0`): `m · max(0, a + P + (f − 1))`, `f` = the body's Lap-M physical factor (`pm4m_candidate_table.csv`, keyed by record, then the gmag terms' record, then the bio-bridge) re-based by `(pm4i(w) − pm4i(160))/100`, ⚑ **LO limb: an unmapped body takes `f_unmapped = min(measured) = -0.44`**; **physical, unclamped**: `m · max(0, a + P + pm4i(w)/100)`; **DoT rows**, non-leech types: `lo · max(0, a_dur + P + (M_inst − 1) + own)`, `a_dur` = `c11a_corrections.duration_attr_mult` when the body folds the attribute limb, ⚑ **SlowChaos / SlowAether: the divisor the pack DECLARES for `V311-FULL`: `CompositionFold(chaos_aether_dot_divisor=True)` (`a8`), i.e. `a_dur = int/200 + 1` (`dc1` `V39-DC1-2`, decoded A−)**, else 1.0; **DoT leech types** (`SlowLifeLeach`, `SlowManaLeach`): `lo · om` (the oracle form); **`percent_current_life` rows untouched.** `pm4i(w)` = `D_ + U_offensivePhysicalModifier_pct` of `pm4i_wave_damage_modifier.csv` (pack `f1` `IC7-F-V311-05`); `LAPM_WAVE` = 160 (`IC7-K-V311-0006`); `DOT_LEECH_TYPES` (`IC7-K-V311-0003`) | declared-precision → **exact: each composed row equals the law bit for bit** | exact |
| (c) | **CARRIED**: `z3` is a CHECK asserted before `own_add` (`M_inst` per wave = the pack's `z3`; re-measured on the oracle in v1.14: 10/10) | declared-precision | as v1.8 |
| (d) | **CARRIED**: the 29 inert records take the identity path; "unexercised: 0 of 29" | structural | — |
| (e) | **CARRIED at the v1.14 re-derived values: w159 `3.197066`, w160 `4.935649`, and the per-record ratios below.** ⚑ **Definition, stated (Matt Q104(2)): the supply-weighted pre-mitigation ratio of the LOADER-BUILT STATIC SUPPLY** — the profiles `load_profiles` builds under the v3.11 graded loader (inside `v3p10_oracle(Folds311('V311-FULL').v310)` + `v3p11_oracle`; the pack's `WALK` job), priced by the U-P-N-5 walk's own arithmetic `Σ mag·a·(M_inst + own)·t ÷ Σ mag·M_inst` over `direct` and `leech` rows (leech in the denominator only), candidates `pools_for(w, True)`. **It is a static-supply statistic, not the fight's row law** (which is (b′)); runtime grants and the composition are outside it | declared-precision | **`\|Δ\| ≤ 5e-4`** per wave ratio and per record ratio (carried) |

**(e)'s per-record tables (v1.14's walk, `derive_v1p14.json`; computed, not typed):**

| w159 (`M_inst` 1.83) | ratio | on | off |
|---|---:|---:|---:|
| `aetherial_fleshhulk_mine` | 3.514042 | 105739.935 | 30090.69 |
| `beetle_maggot01` | 3.301094 | 69254.047 | 20979.12 |
| `chthonianrylok_ekketzul` | 3.59875 | 100550.672 | 27940.44 |
| `chthonianservitor_lunalvalgoth` | 2.546547 | 48845.693 | 19181.145 |
| `humanwendigo_darkwood_01` | 3.75048 | 46595.48 | 12423.87 |
| `korvaakmessenger_02` | 3.033476 | 86335.987 | 28461.075 |
| `korvaakmessenger_02b` | 3.034357 | 89742.771 | 29575.545 |
| `manticore_jaggedwaste_01` | 2.956584 | 45188.897 | 15284.16 |
| `rokwind_01` | 3.362895 | 39355.455 | 11702.85 |
| `skeletalgolem_stepsoftorment_01` | 3.120862 | 31822.677 | 10196.76 |
| `statue_templeguardian_02` | 1.960798 | 25216.503 | 12860.325 |
| `statue_templeguardian_03` | 1.960798 | 25216.503 | 12860.325 |
| `stonegryphon_templeguardian_01` | 2.762796 | 56697.046 | 20521.62 |
| `wendigo_ancient_namadea` | 4.077782 | 97779.057 | 23978.49 |
| `witchgod_finalboss` | 3.978465 | 80028.246 | 20115.36 |
| `yeti_rimehorn_01` | 3.080011 | 39159.032 | 12713.925 |
| *unpriced (no profile): 5* | | | |
| **w159 supply-weighted** | **3.197066** | | |

| w160 (`M_inst` 1.83) | ratio | on | off |
|---|---:|---:|---:|
| `aetherialcolossus_galakros` | 3.80807 | 86437.112 | 22698.405 |
| `nemesis_aetherial_01` | 8.165613 | 235450.515 | 28834.395 |
| `nemesis_aetherialvanguard_01` | 6.466635 | 155338.25 | 24021.495 |
| `nemesis_beast_01_p1` | 3.829365 | 48791.371 | 12741.375 |
| `nemesis_beast_02` | 2.689026 | 34626.031 | 12876.795 |
| `nemesis_chthonian_02` | 5.55761 | 73832.204 | 13284.885 |
| `nemesis_chthonianvoidborn_01` | 4.517305 | 120614.819 | 26700.615 |
| `nemesis_kymon_01` | 3.474869 | 167919.204 | 48323.895 |
| `nemesis_kymon_02` | 1.075958 | 13506.377 | 12552.885 |
| `nemesis_orderdeathsvigil_01` | 6.921402 | 177547.981 | 25652.025 |
| `nemesis_orderdeathsvigil_02` | 3.658935 | 22012.61 | 6016.125 |
| `nemesis_outlaw_01` | 5.837726 | 88354.076 | 15135.015 |
| `nemesis_outlaw_02` | 5.07033 | 79884.996 | 15755.385 |
| `nemesis_undead_01` | 3.822594 | 75665.167 | 19794.195 |
| `nemesis_undead_02b` | 5.470426 | 124770.592 | 22808.205 |
| `nemesis_wendigo_01` | 6.06632 | 135475.515 | 22332.405 |
| `nemesis_wendigo_02` | 4.391011 | 85550.484 | 19483.095 |
| `statue_korvaaktombguardian` | 4.102804 | 111664.686 | 27216.675 |
| `wendigocannibal_h01` | 5.916297 | 39301.37 | 6642.9 |
| `wendigocannibal_h02` | 5.946459 | 47652.363 | 8013.57 |
| `wendigocannibal_h03` | 5.476449 | 18881.261 | 3447.72 |
| `wendigocannibal_h04` | 5.429514 | 16533.522 | 3045.12 |
| `wendigocannibal_h05` | 5.429514 | 16533.522 | 3045.12 |
| *unpriced (no profile): 5* | | | |
| **w160 supply-weighted** | **4.935649** | | |


### F.2h′.1 · ⚑ THE EMISSION (by name)

`ta_manifest.json :: ta_x_29_b_c_d["(b)"]` (replacing the Z5 block):

```
law                          "CompositionFold"          (string, exact)
phys_limb                    "LO"
f_unmapped                   -0.44                  (the minimum measured factor, from pm4m_candidate_table.csv)
chaos_aether_dot_divisor     true
lapm_wave                    160
exercised.instant_nonphys        {n, n_equal_to_law}
exercised.phys_clamped           {n, n_equal_to_law}
exercised.phys_clamped_unmapped  {n, n_equal_to_law}
exercised.phys_unclamped         {n, n_equal_to_law}
exercised.dot                    {n, n_equal_to_law}
exercised.dot_leech_type         {n, n_equal_to_law}
exercised.dot_chaos_aether       {n, n_equal_to_law}
exercised.pcl_rows_untouched     bool
```

**GREEN iff** the four constants equal the values above; every family's `n_equal_to_law == n` (per cell and summed; the
per-cell blocks under `cell.json :: ta_x_29_b`), with the total `n > 0`; `pcl_rows_untouched` true. (a), (c), (d) graded as in
v1.8 / v1.13; (e) on `gmag_conformance.terminal_multiplier` and `per_record` against § F.2h′'s values. ⚑ **Disclosed: no
SlowChaos / SlowAether DoT row was composed on any of the 25 oracle cells, so the divisor clause is UNEXERCISED by the
reference realisation** (both `1.0` and `int/200 + 1` would pass it there). The value bound here is the pack's `a8`
declaration for `V311-FULL`; if the port's realisation composes such a row, the row grades it.

---

## § K′ · ⚑ LAW (a) ON THE TWO RESTATED ROWS (KP-178): THE ORACLE PASSES BOTH

**Instrument:** `audit_v1p15.py` runs `run_one("V311-FULL", salts 0–4, period, arm)` under `graded_arm(arm)` for each arm, with
read-only hooks on `Mover.step`, `GdEngagementFold.halt_for`, `GdRepositionFold.waypoint` / `pet_target`, `ArenaFold.clamp_body`,
the per-tick occupancy map (where a moved pet's new position is written) and `CompositionFold.instant` / `.dot`, each forwarding
unchanged. **OBS-1 guard: 25/25 cells complete** (w151…w160 banked; every wave `cleared/board_empty` or
`player_death/player_died`; no exception escaped `simulate_wave`; `raised` None; leg A = the first death or the w160 clear).
STOP cells: none. `check_v1p15.py` evaluates the verdict.

| cell | complete | terminal | (a′) roster steps / law-exact unclipped / held | (a′) pet steps / moved exact / no travel | (a′) fails | (b′) beyond | armed wall | (b′) vacuous | (b′) | (b′) composed rows / fails | TA-X-29 (b′) |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| M-POL-2-NULL_s0 | ✓ | clear | 31,340 / 29,104 / 2,236 | 18,843 / 13,180 / 5,663 | 0 | 0 | no | **vacuous** | **PASS** | 3,636 / 0 | **PASS** |
| M-POL-2-NULL_s1 | ✓ | clear | 30,518 / 29,429 / 1,089 | 23,344 / 17,962 / 5,382 | 0 | 0 | no | **vacuous** | **PASS** | 4,112 / 0 | **PASS** |
| M-POL-2-NULL_s2 | ✓ | clear | 33,212 / 30,068 / 3,144 | 22,918 / 17,501 / 5,417 | 0 | 0 | no | **vacuous** | **PASS** | 4,085 / 0 | **PASS** |
| M-POL-2-NULL_s3 | ✓ | w160 | 35,199 / 32,358 / 2,841 | 32,404 / 26,845 / 5,559 | 0 | 0 | no | **vacuous** | **PASS** | 3,761 / 0 | **PASS** |
| M-POL-2-NULL_s4 | ✓ | clear | 34,280 / 32,831 / 1,449 | 29,906 / 22,730 / 7,176 | 0 | 0 | no | **vacuous** | **PASS** | 4,663 / 0 | **PASS** |
| M-POL-2_s0 | ✓ | clear | 31,773 / 29,927 / 1,846 | 21,629 / 16,076 / 5,553 | 0 | 0 | no | **vacuous** | **PASS** | 3,774 / 0 | **PASS** |
| M-POL-2_s1 | ✓ | clear | 32,739 / 31,383 / 1,356 | 32,274 / 26,256 / 6,018 | 0 | 0 | no | **vacuous** | **PASS** | 5,525 / 0 | **PASS** |
| M-POL-2_s2 | ✓ | w160 | 34,741 / 32,215 / 2,526 | 30,173 / 25,103 / 5,070 | 0 | 0 | no | **vacuous** | **PASS** | 3,640 / 0 | **PASS** |
| M-POL-2_s3 | ✓ | clear | 36,905 / 34,033 / 2,872 | 32,702 / 27,104 / 5,598 | 0 | 0 | no | **vacuous** | **PASS** | 4,954 / 0 | **PASS** |
| M-POL-2_s4 | ✓ | clear | 31,154 / 28,964 / 2,190 | 23,606 / 17,220 / 6,386 | 0 | 0 | no | **vacuous** | **PASS** | 3,735 / 0 | **PASS** |
| M0_s0 | ✓ | clear | 31,340 / 29,104 / 2,236 | 18,843 / 13,180 / 5,663 | 0 | 0 | no | **vacuous** | **PASS** | 3,636 / 0 | **PASS** |
| M0_s1 | ✓ | clear | 30,518 / 29,429 / 1,089 | 23,344 / 17,962 / 5,382 | 0 | 0 | no | **vacuous** | **PASS** | 4,112 / 0 | **PASS** |
| M0_s2 | ✓ | clear | 33,212 / 30,068 / 3,144 | 22,918 / 17,501 / 5,417 | 0 | 0 | no | **vacuous** | **PASS** | 4,085 / 0 | **PASS** |
| M0_s3 | ✓ | w160 | 35,199 / 32,358 / 2,841 | 32,404 / 26,845 / 5,559 | 0 | 0 | no | **vacuous** | **PASS** | 3,761 / 0 | **PASS** |
| M0_s4 | ✓ | clear | 34,280 / 32,831 / 1,449 | 29,906 / 22,730 / 7,176 | 0 | 0 | no | **vacuous** | **PASS** | 4,663 / 0 | **PASS** |
| W1-NULL_s0 | ✓ | clear | 31,773 / 29,927 / 1,846 | 21,629 / 16,076 / 5,553 | 0 | 0 | no | **vacuous** | **PASS** | 3,774 / 0 | **PASS** |
| W1-NULL_s1 | ✓ | clear | 32,739 / 31,383 / 1,356 | 32,274 / 26,256 / 6,018 | 0 | 0 | no | **vacuous** | **PASS** | 5,525 / 0 | **PASS** |
| W1-NULL_s2 | ✓ | w160 | 34,741 / 32,215 / 2,526 | 30,173 / 25,103 / 5,070 | 0 | 0 | no | **vacuous** | **PASS** | 3,640 / 0 | **PASS** |
| W1-NULL_s3 | ✓ | clear | 36,905 / 34,033 / 2,872 | 32,702 / 27,104 / 5,598 | 0 | 0 | no | **vacuous** | **PASS** | 4,954 / 0 | **PASS** |
| W1-NULL_s4 | ✓ | clear | 31,154 / 28,964 / 2,190 | 23,606 / 17,220 / 6,386 | 0 | 0 | no | **vacuous** | **PASS** | 3,735 / 0 | **PASS** |
| W1_s0 | ✓ | clear | 31,773 / 29,927 / 1,846 | 21,629 / 16,076 / 5,553 | 0 | 0 | yes | tested | **PASS** | 3,774 / 0 | **PASS** |
| W1_s1 | ✓ | clear | 32,739 / 31,383 / 1,356 | 32,274 / 26,256 / 6,018 | 0 | 0 | yes | tested | **PASS** | 5,525 / 0 | **PASS** |
| W1_s2 | ✓ | w160 | 34,821 / 32,295 / 2,526 | 26,352 / 21,656 / 4,696 | 0 | 0 | yes | tested | **PASS** | 3,402 / 0 | **PASS** |
| W1_s3 | ✓ | clear | 35,860 / 32,988 / 2,872 | 33,472 / 27,534 / 5,938 | 0 | 0 | yes | tested | **PASS** | 4,839 / 0 | **PASS** |
| W1_s4 | ✓ | clear | 31,154 / 28,964 / 2,190 | 23,606 / 17,220 / 6,386 | 0 | 0 | yes | tested | **PASS** | 3,735 / 0 | **PASS** |

**`TA-X-30(a′)`: PASS 25/25.** Roster steps checked 830,069 (unclipped 776,181, all law-exact; clipped 0; held
53,888, all zero; waypoint steps 572,104); operand classes `ATTACK` 253,753; `DEFAULT(no state)` 4,212; `PET:incumbent_walk(op=2.4)` 203,859; `PET:pet_target(op=0.0)` 469,072; `PET:reach=gr2_row` 132,680; `PET:reach=no_gr2_row(packed)` 336,392; `WAYPOINT(op=0)` 572,104; `WAYPOINT:pursue_reach=default_attack` 111,429; `WAYPOINT:pursue_reach=gr2_row` 156,909; pursue-waypoint reaches verified against the pack
on every Pursue waypoint step. Pet steps 672,931: moved law-exact 528,696 (incl. ghost pets read at the next tick),
clipped 0, no travel by law 144,235, moved against the law 0, unobserved 0.
**`TA-X-30(b′)`: PASS 25/25**; vacuous on 20 cells (no armed wall); on `W1`, 171,478 clamp calls and 0 bodies
stopped beyond their step operand.
**`TA-X-29(b′)`: PASS 25/25.** Rows recomputed and bit-equal: `dot:dot` 14,084; `dot:dot_leech_type` 134; `instant:instant_nonphys` 66,538; `instant:phys_clamped` 3,097; `instant:phys_clamped_unmapped(LO)` 1,895; `instant:phys_unclamped` 19,297; every composing instance `LO` with the divisor
`True`: `dot|limb=LO|divisor=True` 14,218; `instant|limb=LO|divisor=True` 90,827. Rows on which the Z5 form would differ from the oracle's value: 43,819 (why v1.14 halted it).

⚑ **Instrument defect, found and fixed BEFORE the verdict (disclosed):** the first full run counted 18 pet steps on 6 cells as
"moved against the law". The hook resolved a pet's pending step at ANY write into the tick's occupancy map; the contact solver
writes displaced pets into that same map after the motion loop (and a spawn writes a new pet). The fix resolves a pending step
only at the motion loop's own write, located in `run.py` by its source text (line 2023 at `969fbd8d`). **No
criterion, operand or expected value changed**; the oracle was not touched; the defect was the observation point.

**Result: with v1.14 § K (26 rows), the v3.11 oracle passes all 28 EXACT rows.** Law (b) for the two rows: v1.14 § L.11 and
§ L.12 are discharged by this restatement (the slots / WaitToAttack / RFA / stationary / pet-slot states are now read by
(a′)'s operand table; the composition by (b′)).

---

## § G · THE CAP, THE PRE-READ, THE VERDICT FILE

**§ G carried from v1.14:** a fresh 2; the next graded run is **"attempt 1 of 2 (overall 4)"**; § G.1a's 28-row pre-attempt read
is a precondition and applies the values of v1.14 + v1.15; KP-185's launch-sheet rules carry. **§ G.3, the changes:**
`prereg_version: "v1.15"`, `prereg_sha256` (this file), `prereg_carried_from: {"version": "v1.14", "sha256": "5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92"}`;
`ta_x_30` per cell = the § F.2i′.2 block with `holds`; `ta_x_29_b` = the § F.2h′.1 block; the face prints (b′)'s vacuity per
cell (§ F.2i′.1).

## § H · OWED BEFORE ATTEMPT 1 (v1.14 § H, updated)

H-0 **DONE** (Matt Q104, KP-240; this file). H-1 … H-8 as v1.14, with H-4 now pointing at v1.15 + v1.14 and emitting
§ F.2i′.2 and § F.2h′.1 by those names. ⚑ **At godot HEAD `a07f7f5` the harness emits only v1.13's
`pursuit.n_bodies_halted_beyond_d_engage` for `TA-X-30` and the Z5 block for `TA-X-29(b)`; the fields above are owed (H-4)
before the § G.1a read.**

---

## § Z · HOW THIS FILE WAS MADE

`audit_v1p15.py` (five arms) → `check_v1p15.py` (verdict) → `fill_v1p15.py` (every computed block, from their JSON and from
`derive_v1p14.json` / v1.14's committed instruments). All exit 0. Instruments committed first (D4); this file ALONE.

| file | sha256 |
|---|---|
| `audit_v1p15.py` | `67331626754b6ad2f62d6457a11c9ad73ca717e8d946457c3e3b31833d818ab1` |
| `check_v1p15.py` | `67750e035adc006af9dddc7d7b6e508cda19c6f7f2ad09c5a34111164bd92044` |
| `results_v1p15.json` | `111a209080d47b80f33c5af47e089d819f77fb3c9d9abf67bdf13a67a73347ab` |
| `fill_v1p15.py` | `27848e787a1d450c344db6962c7dc1e00f92d803e400ba85c9e73aad222dc8b5` |
| `v1.15.template.md` | `d92dfd68f9038f15085d3bbbb8ac171d886c60b612ae7cc31d94982847f54d5b` |
| `audit_out/audit_M-POL-2-NULL.json.gz` | `932739efc0014c25ac3e536a037eb34f54415b8ac67f13329bac40419c302a90` |
| `audit_out/audit_M-POL-2.json.gz` | `86d918e0576cbc130b2b90ec52b8a3c6d3a96a1159c55f19ef25eac405242bd4` |
| `audit_out/audit_M0.json.gz` | `f911d8dd5216e8fcedacfaa5c22e26256caec718393070e3536b4106583384ae` |
| `audit_out/audit_W1-NULL.json.gz` | `64cccd6b86c55fa8c8677035098f3c53f3b696d9c7ef441e40ff5462894e1c6f` |
| `audit_out/audit_W1.json.gz` | `5fe3f1166f1ee21d04aaeaced2480a37c5813ed65575cfbc07e23f70c32abb4b` |
| v1.14 `derive_v1p14.json` (read for (e)) | `7e9c28bd25b1406b7dd5f879f3ae9f5ed7cfc24c3b4cb7a670d1dd58ba2f7a1b` |

---

*Filed 2026-10-02 by **gamora**, Run KC2-PLAY; conductor gandalf.* **What v1.15 does:** writes Matt's Q104 ruling into the two
halted rows, derives each from the oracle's code and the pack's rows, and shows the oracle passes both 25/25 under the OBS-1
guard. **Nothing else moves.** No tolerance moved; NO BAND WIDTH MINTED; the declared set stays exactly `["TA-X-06"]`; no port
output read; the oracle not edited; godot not touched. **IMMUTABLE. D4 held: committed ALONE. No push.**
