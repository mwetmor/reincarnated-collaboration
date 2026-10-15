# J4b (D2 Fire Sorceress): KP-312 port-site ruling sheet for Matt (v2, 2026-10-14)

**Status:** PROPOSED v2 (23 sites). v1 (19 sites, collab `c14285481`) was put to Matt and HELD by his ruling (KP-435) until her build-file sheet was pinned and gated.
- The sheet is now pinned: C-14, collab `0ac88e6ef`.
- It is gated: census Gate-2 `8281adb67` and ADDENDUM-9 delta `d202525b8`.

Matt's ruling, recorded as a KC2 ledger row, is the consent of record (KP-312 condition 1).

**Runtime base:** sealed runtime `a0e75469` (godot `d419666`, tag `kc2/referent-v1-sealed-r2-runtime-j3c-s12`).

**Design of record:** gamora's J4b design `f72316b7` and ADDENDA 1–9 (engine `4cabc43d` … `1ae57713`).

**Placement of record:** drax's inventory, godot `a207180` plus ADDENDUM A `7ab66a3` (`kc2_play/join/J4B-SITE-INVENTORY-a0e75469.md`).

**Gates (jack-ryan, collab):** `2c5413335` → `5ad04470f` → `1a4bee308` → `ae25b2f5f`/`9c1d54cce` → `146a3a84f` → `4a8b31678` → `926932a9f` → `8281adb67` → `d202525b8`.

## 1. What is being consented to

**23 port sites** in the sealed Godot runtime: S01–S15, S16b, S17–S23. S16a is an engine-side read and needs no consent.

**Size and shape of the change:**
- About 140–230 sealed lines.
- Files touched: `kc2rt_fight.gd`, `kc2rt_control.gd` (plus one new rulebook member, M-5) and `kc2rt_gd_engage.gd`.
- Files untouched: `kc2rt_movement.gd`, `kc2rt_mutators.gd` and `kc2rt_pack.gd`.
- One new JOIN draw stream (`oculus:<kit>`), out of tree like `block:<kit>`.
- The bulk of the kit is out of tree: about 1,500–2,500 lines in `kc2_play/join/rulebook/`.

**Guard on every site:** `if rulebook == null or lever == gd value: existing lines`. In ORACLE and PLAY the rulebook is null, so every site is inert there.

**Predicted:** ORACLE G3 25/25 and the T-A digests are byte-identical, and JOIN[Warlord] stays bit-equal to the J-S8 golden master.

| Site | What it does | Sealed touch point (d419666) | Guard key |
|---|---|---|---|
| S01 | Turns off the six Warlord-kit systems under a D2 kit: channel verdict, player summons, War Cry and Ascension, cp_absorb on all 3 intake paths, R8 Resilience (class passive), dash layers | fight 1829, 1988–2000, 2001–2020, 4532/4537, 4772/4817/5408, 2027/2053/5861/6322ff, movement call 2566 | `kit_is_gd()` |
| S02 | Spell-lane call-out: Fire Ball, Meteor, Static Field | fight 2037, after intake | lever |
| S03 | D2 mana replaces the EoR channel cost | fight 1806–1816 | lever |
| S04–S06 | Built damage bodies (Fire Ball, Meteor, pyre; Static resolved here too), booked only through the existing `_ss_hit` 4021 | out of tree, plus `_ss_hit` | new tagged function |
| S07 | Monster hit recovery, and the Frozen Armor FREEZE on normal monsters (attack and motion gates) | `_resolve_threat` 3269ff (3324/3360/3403/3518/3817); gd_engage `choose_slot` 447, busy_until 421/945, reposition 787/951; march 2898 | lever |
| S08 | Cast and hit-recovery movement lock | `_pmove_pilot` 8154, `_pmove_propose` 8185; kmill 2544; movement call 2566 | lever |
| S09 | Shield block (full negate plus BL lock) | `_apply_slot`, right after 5962, before control 5966 and Cruel 5970 | L-23 |
| S10 | D2 belt potions | `_cp_begin_tick` 4524, `_cp_drink_potion` 4562, `_cp_heals` 4660 | L-S7 `player_potion_model` |
| S11 | Locks and D2-frame placement | out of tree, plus one chill call at `_land` 6267 | lever |
| S12 | GD control families received, D2 durations | `kc2rt_control.gd` 89/324/364/408, plus member M-5 | lever |
| S13 | DoTs received, D2 stacking (it also marks DoT calls so absorb skips them) | `bind_dot_timeline` 5184, `_dot_register` 5229/5231, 5261, 5335 | lever |
| S14 | Intake family map (and the per-hit flat magic absorb, direct rows only) | existing consented H-8/H-7/H-10 routes; possibly one guard at 6369 | existing |
| S15 | Stamina and locomotion | fight call site 2566 | lever |
| S16b | Drain per-family export (observation only) | 6163/6173 (totals already public) | JOIN only |
| S17 | D2 intake hit law (AR vs Defence by attack kind, 5–95 %) | H-1/H-2/H-3 (5860/5865/5894), plus a slot-context guard in `_apply_slot`; the 5881 draw is consumed and ignored | L-24 |
| S18 | Her build-file sheet at load | end of `_bind_player_raw` 982 | L-22 |
| S19 | Banner and mutator placement in the D2 damage pool | `_banner_factor_now` 5686, plus H-7 | lever |
| **S20** | Frozen Armor CHILL on champion, boss and nemesis (speed and cadence factor) | march 2898, ge_speed 8118–8121 (pets 4213); cadence 3324/3403; gd_engage 460/905, swing pause 344/351 | `rulebook.chilled(b)` |
| **S21** | ONE `on_struck` hook on a landed, unblocked hit, in declared order: Frozen Armor trigger → Oculus 25 % draw → thorns | `_apply_slot` 5936, after S09 | lever (G-A) |
| **S22** | Oculus teleport: player_x/player_y written once per tick | at the S02 call-out 2037 | rides S02 |
| **S23** | Thorns booked to a melee attacker via `_ss_hit` | `_apply_slot`, shares S21's guard | shares S21 |

## 2. Also in this consent (the KP-360 precedent)

- **(a) Census:** NO booking-census rows by design, because every new damage books through the existing `_ss_hit`. Conditional consent (jack-ryan INFO-2): if the build adds any `_cons_add` line in a J4b branch, it is enumerated by `census_grep` at the commit with a MATCH result and reported as a named finding, with no second ruling needed.
- **(b) Hunk audit:** a new J4b hunk audit at base `d419666`, collapsing J4b tags only, with a nested-guard drift control (S01 and S03 enclose existing D2/J3c guards).
- **(c) S16b emitter:** NO emitter unfreeze. The out-of-tree JOIN tool reads the per-family split through the KP-402 `_new_fight(hooked)` route. The frozen `kc2p_join1_gm_emit.gd` output is unchanged.
- **(d) The standing KP-312 conditions:**
  1. this ruling;
  2. fail-first for every site;
  3. ORACLE byte-identity (G3 25/25 + T-A pre_read 25/25) and J-S8 bit-equality for JOIN[Warlord];
  4. a jack-ryan delta Gate-2 before anything depends on the new digest;
  5. Matt's windowed `.app` self-test before the runtime ships.

## 3. Conductor rulings carried onto the sheet (gates `926932a9f`, `d202525b8`)

- **R-1:** S10 keys on the potion lever L-S7, not on `kit_is_gd()`.
- **R-2: DEATH-at-entry.** `player_hp ≤ 0` means neither her lane (S02) nor the teleport (S22) runs. The order at 2037 is teleport, then lane. This is mirror-side, with no sealed change, and has a fail-first control.
- **R-3: launch-time decision.** Block (S09), on-struck effects (S21) and thorns (S23) for deferred projectiles are decided at the resolve tick, where the oracle resolves the hit. The latency is printed.
- **R-4:** the flat magic absorb applies to DIRECT damage rows only. DoT rates registered through `_dot_register` are marked by S13 and skipped, with one grid row.
- **R-5:** the Frozen Armor trigger, the Oculus draw and thorns share ONE `on_struck` hook (S21), in the declared order above.
- **Printed asymmetry:** her offense runs after intake while the Warlord's runs before it. This slightly disfavours her.
