# JOIN-1 · J4b: the registered items that need no arena arm, computed on the gb-fix grains (conductor KP-473 (4)) (gamora, 2026-10-15)

**Labels:** completeness POST-HOC; CORR-4 FALSE AS PRE-STATED (carried).

**Inputs:**
- the gb-fix grains (pin file `1a17de52…`, 105 / 105; G1–G7 pinned `b77414ef…`);
- her J4B-ROWS, G1, G2 and GO;
- the engine row replay (`7f611592`, PASS on every class, collab `33eddbc97`).

**Engine HEAD:** `0ab979a7`.

**Labels:** completeness POST-HOC; CORR-4 FALSE AS PRE-STATED; probe limbs by reference; Meteor-delay semantics OPEN (KP-476), replay check absent at grading, no pair flips.

## 1 · Fraction (a): rows mapped / 32, from the CENSUS and the PACK (jack-ryan INFO-1; no grains)

**Inputs:**
- census: elrond, Sorceress census § 13 (32 rows; § 14 classes);
- pack: v5.1 (`kc2-rulebook-pack-v5.1-20261015_134952`): `kit_d2_fire_sorc.json`, `hooks.json`, `hooks_j4b.json`, `world_l21.json` and `anchor_d2_gd.json`.

**The test:** a row is **mapped** iff the pack carries its JOIN setting, either a lever row or the KIT / WORLD operand rows the setting reads.

| Row | Pack evidence | Mapped? |
|---|---|---|
| 1 mana spend | `RB-K-fire_ball` / `RB-K-meteor` / `RB-K-static_field` `mana_cost`; `RB-K-resource_law` | yes |
| 2 regen | `RB-K-warmth_pct`, `RB-K-manarecoverybonus_items`, `RB-K-mana_regen_class` | yes |
| 3 damage lines | `RB-K-fire_ball`, `RB-K-meteor`, `RB-K-meteor_pyre` | yes |
| 4 synergy | `synergy_pct` in the same rows; `RB-K-blvl.*` | yes |
| 5 mastery | `RB-K-fire_mastery_pct`, `RB-K-mastery_item_pct` | yes |
| 6 +skills | `RB-K-slvl.*` | yes |
| 7 Meteor cooldown | `RB-K-meteor.delay_frames` | yes |
| 8 cadence | `RB-HOOK-L-01`; `RB-K-sheet.fcr_frames` | yes |
| 9 cast root | `RB-HOOK-L-17` | yes |
| 10 no hit roll | `RB-HOOK-L-06`; `RB-K-crit_model_spell` | yes |
| 11 projectile | `RB-HOOK-L-14`; `RB-K-fire_ball.missile` | yes |
| 12 remote impact | `RB-HOOK-L-19`; `RB-K-meteor` | yes |
| 13 splash footprint | `explosion_radius_subtiles` / `impact_radius_subtiles` | yes |
| 14 burning zone | `RB-HOOK-L-20`; `RB-K-meteor_pyre` (+ offsets) | yes |
| 15 fire family | `RB-K-spell_lane_vocab`; `families.json` | yes |
| 16 monster hit recovery | `RB-HOOK-L-21`; `RB-W-l21_*` | yes |
| 17 her hit recovery | `RB-HOOK-L-18`; `RB-K-sheet.fhr_frames`; `RB-K-hr_threshold_frac` | yes |
| **18** build legality (OUT-OF-ARENA) | prerequisite operands present (`RB-K-blvl.fire_wall`, `RB-K-blvl.blaze`), but **no legality-check row** | **operands only** |
| 19 block | `RB-HOOK-L-23`; `RB-K-sheet.block_pct(_running)` | yes |
| 20 intake hit law | `RB-HOOK-L-24`; `RB-K-sheet.defence_*`; `RB-A-anchor_ar_eq_table(_unique)`; `RB-A-physical_contact_table` | yes |
| 21 potions | `RB-HOOK-L-S7`; `RB-K-belt.*`; `RB-A-d2_potions_*` | yes |
| 22 control received | `RB-HOOK-L-12` | yes |
| **23** DoTs received | **no pack row** for `dot_receiver_law`. The port reads it as a design-text operand (provenance `design_text_operands`) | **no pack row** |
| **24** chill on her | **no pack row.** The port uses design-text `CHILL_ON_HER_FRAMES` 100 | **no pack row** |
| 25 family map | `RB-K-res_map`, `RB-K-res_uncapped`, `RB-K-sheet.res.*` | yes |
| 26 world / arena | AS-IS world rules (banner, mutators) need no lever row; Resilient via `RB-K-res_uncapped` | yes (AS-IS) |
| 27 stamina | `RB-K-stamina_max`, `RB-K-stamina_drain_256`, `RB-K-velocity_walk_run` | yes |
| 28 Static | `RB-HOOK-L-07`; `RB-K-static_field`; `RB-K-static_rule` | yes |
| 29 FA freeze / chill | `RB-K-frozen_armor`; `RB-K-on_struck_order`; `RB-HOOK-monster_freeze_receiver` / `_chill_receiver` | yes |
| 30 Oculus | `RB-K-oculus_teleport_on_struck`; `RB-HOOK-player_reposition_on_struck` | yes |
| 31 thorns | `RB-K-thorns`; `RB-HOOK-player_retaliation` | yes |
| 32 flat absorb | `RB-K-sheet.absorb_magic_flat`; `RB-HOOK-flat_family_absorb` | yes |

**Result:**
- **29 / 32 rows have their setting in the pack.**
- Rows **23** and **24** are implemented from **design-text operands**, not pack rows.
- Row **18** has its prerequisite operands but no legality-check row.
- **Against the prediction of 32 / 32** (31 / 32 if row 18 is ruled unmappable), the pack criterion gives 29 / 32. Whether design-text operands count as mapped is jack-ryan's grading call, and it is printed both ways: **29 / 32 (pack rows only)** or **31 / 32 (counting design-text operands; row 18 open)**.


**⚑ drax's confirmation, folded (relayed by the conductor):**
- **Row 18 (build legality): the port has NO legality check.** Only `RB-K-blvl.inferno` is read, so row 18 is **not implemented**, either in the pack or in the port.
- **Row 27 (stamina): wiring shown.**
  - sealed hook `kc2rt_fight.gd:8232`;
  - adapter `kc2rb_port.gd:651`;
  - lane `:333` / `:1213`;
  - S15 reach 1,421;
  - forms 0 / 22,700 bit-unequal.
- **Fraction (a), all three readings side by side:**
  - **pack rows:** 29 / 32 (rows 18, 23 and 24 missing);
  - **implementation:** **31 / 32.** Rows 23 / 24 are implemented from design-text operands, and row 18 is not implemented.
- **The registered prediction was 32 / 32, or 31 / 32 if row 18 is ruled unmappable.** The implementation count matches only the second form. **jack-ryan grades it.**

## 2 · The row-identity negative controls on the existing grains (prereg § 2)

| Row | Registered NC (row identity) | Result |
|---|---|---|
| 8 cadence | cast starts and action frames | **PASS**: 8,673 casts; action == start + 5; spacing ≥ 8 on the rebased timeline |
| 9 cast root | row identity | **PARTIAL.** The lock law passes (CAST length 8 in 8,871 lock checks; `move_refused_cast` 28,765). Her own motion trace is not in the grains, so "no displacement during CAST" is unverifiable |
| 10 no hit roll | row identity | **PASS**: her packets carry no roll or crit; every G1 row is a monster attack on her |
| 15 offense family | packets by family | **PASS**: fire_ball / meteor / meteorfire → Fire (20,862); static_field → Lightning (3,103); thorns → Physical (330) |
| 17 interruptible casts | row identity | **PASS**: 0 lock-precedence violations; 79 preempts before the action, 44 after |
| 20 intake hit law | multiplier 1.0, tier 0, CtH ∈ [5, 95] on rolled rows | **PASS**: 1,426 G1 rows (849 rolled, 577 auto-hit), 0 violations |
| 24 chill | row identity on chilled ticks (displacement == 0.5 × proposed) | **NO VERDICT.** No chill-tick or motion trace is in the contract, and the control rows carry only 10 Stun landings |
| 25 family map | every G2 row's applied resist == her entry | **PASS** for every non-magic family: 2,367 rows exact (Physical / Pierce 18, Fire / Cold / Lightning 75, Poison 83 under Resilient, Bleeding 18). Aether / Chaos / Life (entry 0) are reduced further by row 32's flat absorb. See row 32 |
| 26 world / arena | banner and Ascended in her pool; Cruel; Resilient | **PASS**: pool ∈ {353, 453} = FM 345 + Ascended 8 (+ banner 100); Cruel ∈ {1.0 (12,516), 0.92 (8,346)}; poison PR 83 on 179 / 179 DoT replaces |
| 28 Static | row identity per packet | **PASS**: 3,103 packets. 695 below the 50 % floor and 227 on lightning-immune bodies are zero, as the form says |
| 31 thorns | row identity per packet | **PASS**: 330 packets (row replay, with `res`) |
| 32 flat magic absorb | row identity; G-ABS-DOT | **PARTIAL.** Over Aether / Chaos / Life rows grouped per (tick, attacker), absorbed == min(8 · r_DMG = 628.67, Σ pre) in **617 / 618** groups. The one exception is two hits by one attacker in the same tick (two budgets). Exact per-hit identity needs the S17 packet id, which G2 does not carry |

## 3 · Row 30 (Oculus), from the existing grains
- **Exact binomial proc rate:** 5 procs / 43 eligible draws, against p = 0.25. **Two-sided p = 0.051. No α was pre-stated, so there is no pass / fail** (KP-476 (4)).
- **Draw count:** 53 `oculus:` draws = 43 proc draws + 2 × 5 one-try searches. Consistent.
- **Destinations inside the square and walkable: NO VERDICT.** No destination rows are in the contract.

## 4 · ⚑ FINDING: the engine row replay does not check the Meteor cooldown, and the grains show short gaps
- **The gap:** ADDENDUM-1 § E said *"The row replay checks every cast against the rule."* My replay's cast class checks cost, action frame and spacing ≥ 8, but **not the Meteor delay** (30 frames from the action, i.e. 35 frames from the cast start). **The replay was incomplete on this point.**
- **What the grains show** (on the rebased timeline): of 1,755 Meteor cast rows, **39 start fewer than 35 frames after the previous Meteor** (18 after preempts, 21 at wave starts). ⚑ **Count correction:** this file and my messages first said 45. **The cause was my own transcription error:** every computation (the gap histogram, the preempt split 21 + 14 + 4, and the by-wave and by-cell sums) gives **39**, which equals jack-ryan's independent walk (`4959e1100`). The waves 159 / 160 set (9 casts, 7 cells) is unchanged.
  - 18 follow a preempted Meteor (14 preempted before its action, 4 after).
  - 21 are the first Meteor of a new wave.
  - Everything is consistent with the port setting `meteor_ready` only when an action **resolves with a target** (`kc2rb_d2lane.gd:571–579`; 141 actions had no target, typically when the board empties at wave end).
  - **The contract carries no per-action row, so this cannot be confirmed row by row. That is a contract gap.**
- **Registered meaning:** base § 2 says *"Meteor's delay is 30 frames from its action"*. Whether a cast with no missile (a preempt before the action, or no target at the action) starts the delay is **UNDEFINED IN REGISTRATION.**
- **Bound on the primary result** (a disclosure, not a re-grade):
  - In waves 159 / 160 there are **9** such Meteors, in 7 cells.
  - Removing, for each of them, the **maximum** applied damage of any single Meteor impact in that cell's waves 159 / 160 leaves her M-c ≥ his in **every** affected cell. The closest is M-POL-2-NULL s2: 98,614 vs 90,504.
  - **No pair of the 25 / 0 sign test can flip.**
- **To close:**
  - the contract gains a per-action row (cast id, action frame, target or none, missile created);
  - the conductor rules the delay semantics;
  - the replay then adds the Meteor-delay check, fail-first.

## 5 · The 16a recorder (WARN-1): scope for separate authorisation
- **What it is:** an additive engine sidecar on **his flinch-off arm** (`JOIN[warlord, gd-decoded @ 196]`, the 25 J-S8 cells). It follows the CORR-1 sidecar pattern: a per-cell child in the JOIN profile, through the J-S8 emitter's `--cell` path.
- **What it reads:** inside the graded window, the oracle's own run attributes `run.non_health_rows` (SlowManaLeach) and `run.non_health_by_type` (ManaBurnDrain / Disruption / PierceRatio), per wave (`run.py:4452–4457`). It changes nothing and draws nothing.
- **What it writes:**
  - per (cell, wave) landing counts by type;
  - `B_hi = n_SML · 1,032`, which is her mana max;
  - `B_eq = Σ (drain_GD / energy_max_Warlord) · 1,032`;
  - the Disruption lost-cast bound `Σ lockout_s · 3.125`.
- **Its gates:**
  - G1–G7 are 7 / 7 vs `4c30b0d64`, as the GO sidecar was;
  - its own G1–G7 equal the instrument's row for row.
- **Who builds it:** **gamora** (engine, simulation seam): failing tests, then code, each commit alone, run in the dedicated worktree under the courtesy gate. About 30 minutes of compute.
- **Her side is already measured:** 0 landings on 25 / 25 cells (16b), so the bias on her margin is 0 whatever 16a shows.

*Read-only computation over the released grains. No new run.* gamora, 2026-10-15.
