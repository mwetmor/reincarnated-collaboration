# JOIN-1 · J4b · DIAGNOSIS: `ControlFamilyUnmapped: Confusion` on the body-off arms (read-only; nothing changed) (gamora, 2026-10-16)

**The refusals:**
- **body-fire_ball** (godot `e868512`): cell **W1|2**, tick 1929, wave 157. G5 `terminal_reason: raised:KeyError`.
- ⚑ **Also body-meteor:** cell **M0|3**, tick 1151, `ControlFamilyUnmapped: Confusion`. **This is the same mechanism.**
- Evidence files: `confusion_scan.txt` (every filed run) and `lineup_control.txt` (the w151–160 lineup census).

## (1) Where Confusion comes from, and why only with a body off
- **The source:** **Blugrug the Living Plague** (`boss&quest/aetherialbloater_malmouthdocks_01.dbr`), slot `special1`, skill `aetherialbloater_violentbarf`.
  - It is a roster monster. No affix and no mutator is involved.
  - G1 row: tick 1929, attacker `w157_a000`, `special1`, hit. The struck row names the record.
  - Census (`pm2_tg2_attack_damage.csv`): Confusion, min 2.0 s, **chance empty**. The port's gate runs only when chance > 0 (`kc2rb_d2lane.gd:1602`), so **every landed `special1` hit is a Confusion delivery.**
- **Its wave:** Blugrug is in the w151–160 pools on **wave 157** (`wave_engine.pools_for`). In the struck rows it appears on wave 157 in M0, M-POL-2, M-POL-2-NULL and W1.
- **Why only with a body off: her kill rate.** In car2 and in every tier-1 and other tier-2 arm, Blugrug **never struck her once** (0 struck rows from its record), so it died before closing.
  - Fire Ball off: 4 struck rows from Blugrug (3 basic, 1 `special1` landed, which is the refusal).
  - Meteor off: 1 `special1` landed, which is the refusal.
  - Both arms run slower boards (body-fire_ball: 65,393 ticks vs 35,473), so the wave-157 boss lives long enough to reach her.
  - **Your guess holds:** she survives longer because the board takes longer, and the boss gets to her.

## (2) Elsewhere, and the full family list
- **Confusion or Convert in any other filed run** (car2; tier 1: use-weighted, worst-case, raw, flinch-off; tier 2: r2, nonladder, block-gd, potion-gd, potion-none, dot-gd, chill-off, resist-referent, static-off): **never delivered.**
  - 0 control rows and 0 refusals.
  - 0 landed hits from any Confusion- or Convert-carrying slot.
  - The only Sentinel struck row is one `basic` hit in use-weighted.
- **Every control family the w151–160 lineup can deliver**, against S12's `CONTROL_FAMILIES` (`kc2rb_d2_laws.gd:262`: Stun, Freeze, Knockdown, TakeHit, Sleep, Trap, Petrify, Immobilize):

| Family | Lineup sources (waves) | In S12? |
|---|---|---|
| Stun | 15 roster records + 1 pet (LightningSpike) (151–160) | yes |
| Freeze | 7 roster records (152, 153, 155, 157, 158, 160) | yes |
| Petrify | 12 roster records (151–153, 155–157, 159) | yes |
| **Confusion** | **Blugrug (157); Aetherial Regurgitator, trash (156, 157); Vanoxxis Bile, bounty (153, 155)** — all `violentbarf`, chance none (always lands on a hit) | **NO** |
| **Convert** | **The Sentinel (159)**, `special5` / tree, chance 0.0 (no gate) | **NO** |

- The census's control families, over all rows, are exactly these five. **Two are unmapped: Confusion and Convert.**
- **Convert has never landed in any filed run**, but nothing stops it. A landed Sentinel `special5` on wave 159 would refuse the same way.
- S12's Knockdown, TakeHit, Sleep, Trap and Immobilize have **no source in this lineup.**

## (3) The design of record
- **Never enumerated.** ADDENDUM-4 § 4.2 (P-2, row 22) lists **8 GD families** (Stun, Freeze, Knockdown, TakeHit, Sleep, Trap, Petrify, Immobilize). **Confusion and Convert appear nowhere** in the base note `f72316b7`, its ADDENDA, or the grading prereg.
  - The table was drawn from GD family names, not from this lineup's census. Three of the five families the lineup actually delivers are in it; two are not.
- ⚑ **A design-vs-port gap, named:** A4 § 4.2 says *"An unmapped family REFUSES at **bind** (checked against every family appearing in the loaded profiles), never mid-run."* The port refuses **mid-run, on landing.**
  - A bind-time check against the loaded profiles would have refused **every** run whose roster contains Blugrug, the Regurgitator, Vanoxxis or the Sentinel. That is all 25 cells, before any tier.
- **The gd semantics, as received, are no effect on a player.**
  - The sealed oracle decodes Confusion and Convert on a player as **ZERO**: D-7 § 3.4, `CombatExertInfluenceConfusion@ControllerPlayer` is a `ret` stub, and `Monster` overrides it.
  - `control_application.py:913` books them `EffectModel.DECODED_ZERO`; `control_states.py:287–293` marks them UNBUILDABLE.
  - **The skill's damage still lands.**
- **D2 has no player confusion or convert state.** D2's Confuse is a curse on monsters.

**Options for the ruling:**
- **(A) Recommended:** add Confusion and Convert to the S12 registry as **"no D2 player state ⇒ no effect; counted `control_dropped:<family>`"** under `d2-strict`, the same as Sleep / Trap / Petrify.
  - This equals gd's decoded zero and the D2 fact, so it is native under KP-420 and the GD-default boundary rule, with no invention.
  - `d2-nearest`: none, or the Stun form (DECLARED-INVENTED), as a sensitivity only.
- **(B)** Map them to the Stun form under the default. This is an invention against both games.
- **(C)** Restore A4's bind-time refusal as written. Every cell with these bodies in its roster refuses, so no arm can run until (A) or (B) is chosen.

Under (A), only the two refused cells change (W1|2 Fire Ball off; M0|3 Meteor off). They rerun; every other filed cell is untouched, because no Confusion or Convert landed in them.

*Read-only diagnosis.* gamora, 2026-10-16.
