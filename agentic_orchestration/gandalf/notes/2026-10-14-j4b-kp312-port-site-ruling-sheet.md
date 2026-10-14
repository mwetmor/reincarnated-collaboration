# J4b (D2 Fire Sorceress): KP-312 port-site ruling sheet for Matt (2026-10-14)

**Status:** PROPOSED. Put to Matt. His ruling, recorded as a KC2 ledger row, is the consent of record (KP-312 condition 1).
**Runtime base:** sealed runtime `a0e75469` (godot `d419666`, tag `kc2/referent-v1-sealed-r2-runtime-j3c-s12`).
**Design of record:** gamora's J4b design `f72316b7` and ADDENDA 1–8 (engine `4cabc43d` … `d785f334`).
**Placement of record:** drax's inventory, godot `a207180` (`kc2_play/join/J4B-SITE-INVENTORY-a0e75469.md`).
**Gates:** jack-ryan, collab `2c5413335` → `5ad04470f` → `1a4bee308` → `ae25b2f5f`/`9c1d54cce` → `146a3a84f` → `4a8b31678` → `926932a9f`. The last gate is GO-WITH-AMENDMENTS; its three WARNs are ruled in § 3 below.

## 1. What is being consented to

There are **19 port sites** (S01–S15, S16b, S17–S19) in the sealed Godot runtime.
- **Size:** about 120–200 lines in 25–35 hunks, across `kc2rt_fight.gd`, `kc2rt_control.gd` (plus one new rulebook member, M-5) and `kc2rt_gd_engage.gd`.
- **Untouched files:** `kc2rt_movement.gd`, `kc2rt_mutators.gd` and `kc2rt_pack.gd`.
- **Out of tree, not sealed:** the bulk of the kit, about 1,500–2,500 lines in `kc2_play/join/rulebook/`. This covers the spell lane, D2 mana, the three built bodies, D2-frame placement, locks, potions, the DoT receiver, the control registry and the AR-table read.

**Guard on every site:** `if rulebook == null or lever == gd value: existing lines`.
- In ORACLE and PLAY the rulebook is null, so every site is inert.
- **Predicted:** ORACLE G3 25/25 and the T-A digests are byte-identical, and JOIN[Warlord] stays bit-equal to the J-S8 golden master.

| Site | What it does | Sealed touch point (d419666) | Guard key |
|---|---|---|---|
| S01 | Turns off the six Warlord-kit systems under a D2 kit: channel verdict, player summons, War Cry and Ascension, cp_absorb on all 3 intake paths, R8 Resilience, dash layers | fight 1988–2000 and 1829, 2001–2020, 4532/4537, 4772/4817/5408, 2027/2053/5861/6322ff, movement call 2566 | `kit_is_gd()` |
| S02 | Spell-lane call-out (her casts) | fight 2037, after intake | lever |
| S03 | D2 mana replaces the EoR channel cost | fight 1806–1816 | lever |
| S04–S06 | The three built damage bodies (Fire Ball, Meteor, pyre) | out of tree, plus one sealed apply-damage-to-body function | new tagged function |
| S07 | Monster hit recovery | `_resolve_threat` 3269ff (3360/3518/3817); gd_engage `choose_slot` 447 and its motion step | lever |
| S08 | Cast and hit-recovery movement lock | `_pmove_pilot` 8154, `_pmove_propose` 8185; kmill 2544; movement call 2566 | lever |
| S09 | Shield block (full negate plus BL lock) | `_apply_slot`, right after 5962, before control 5966 and Cruel 5970 | L-23 |
| S10 | D2 belt potions | `_cp_begin_tick` 4524, `_cp_drink_potion` 4562, `_cp_heals` 4660 | **L-S7 `player_potion_model`** (§ 3 R-1) |
| S11 | Locks and D2-frame placement | out of tree, plus one chill call at `_land` 6267 | lever |
| S12 | GD control families received, D2 durations | `kc2rt_control.gd` 89/324/364/408, plus member M-5 | lever |
| S13 | DoTs received, D2 stacking | `bind_dot_timeline` 5184, 5229, 5261, 5335 | lever |
| S14 | Intake family map | existing consented H-8/H-7/H-10 routes; possibly one guard at 6369 | existing |
| S15 | Stamina and locomotion | fight call site 2566 | lever |
| S16b | Drain per-family export (observation only) | 6163/6173 (totals already public) | JOIN only |
| S17 | D2 intake hit law (AR vs Defence, 5–95 %) | H-1/H-2/H-3 (5860/5865/5894), plus a slot-context guard in `_apply_slot`; the 5881 draw is consumed and ignored | L-24 |
| S18 | Her D2 sheet at load | end of `_bind_player_raw` 982 | L-22 |
| S19 | Banner and mutator placement in the D2 damage pool | `_banner_factor_now` 5686, plus H-7 | lever |

## 2. Also in this consent (the KP-360 precedent)

- **(a) Booking-census rows:** every booking line added in J4b branches, enumerated by `census_grep` at the build commit with a MATCH result. That is the 4–8 rows for S04–S06 conservation bookings and S10 heals, plus any the S13 `d2` branch adds.
- **(b) Hunk audit:** a new J4b hunk audit at base `d419666`, collapsing J4b tags only, with a nested-guard drift control (S01 and S03 enclose existing D2/J3c guards).
- **(c) S16b emitter:** NO emitter unfreeze. The out-of-tree JOIN tool reads the per-family split through the KP-402 `_new_fight(hooked)` route and writes it into its own report. The frozen `kc2p_join1_gm_emit.gd` output is unchanged.
- **(d) The standing KP-312 conditions:**
  1. this ruling;
  2. fail-first for every site;
  3. ORACLE byte-identity (G3 25/25 + T-A pre_read 25/25) and J-S8 bit-equality for JOIN[Warlord];
  4. a jack-ryan delta Gate-2 before anything depends on the new digest;
  5. Matt's windowed `.app` self-test before the runtime ships.

## 3. Conductor rulings on the last gate's WARNs (`926932a9f`), already reflected in § 1

- **R-1 (WARN-1):** S10 keys on the potion lever L-S7 (`player_potion_model == gd`), not on `kit_is_gd()`. Potions are a world/boundary lever (census row 21, WIDEN), so a D2 kit must be able to run with GD potions or none.
- **R-2 (WARN-2):** a DEATH-at-entry test, `player_hp ≤ 0` means no frames run, so she cannot act after lethal intake in the same tick. It is mirror-side with no sealed change, and has a fail-first control.
- **R-3 (WARN-3):** option (a). Block and the BL lock for deferred projectiles are decided at the resolve tick, where the oracle resolves the hit, and the latency is printed. No extra S09 touch point.
- **Printed asymmetry (INFO-1):** her offense runs after intake while the Warlord's runs before it. This slightly disfavours her and goes on the fidelity table.
- **Wording fix:** R8 Resilience is the Warlord's class passive (`playerclass09/passive02.dbr`), not a devotion.
