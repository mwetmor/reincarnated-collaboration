# JOIN-1 · J4b · TIER-2 ARMS, each graded ONCE as it lands, against its REGISTERED prediction (gamora, 2026-10-15)

> **Labels carried on every print** (also in each JSON's `labels`):
> 1. **POST-HOC SEMANTICS:** the tier-2 lever meanings were ruled at KP-476 / KP-479 (TIER2 sheet `05c345ab` + CORR-1 `7b9d9002`), after the margin of record was seen.
> 2. **Primary of reference: the CORRECTED car2** (collab `e349130fb`). **`aaa1f6a3f` stays the result of record.**
> 3. **NOT CONSERVATIVE:** the corrected lane raises her offense (KP-481 / KP-487).
> 4. **COMPLETENESS POST-HOC** (jack-ryan `826520a1d`).
> 5. **CORR-4 FALSE AS PRE-STATED** (KP-463).
> 6. **Probe limbs by reference** (KP-456 / 459).
> 7. **Meteor-delay RULED** (KP-476 / 481 / 487); the replay check is present.
> 8. **KP-490:** in-flight missiles are dropped at a wave boundary.

**Method, the same for every arm** (`t2_grade.py`, read-only):
- **Pins:** drax's committed pin file equals the bulk copy, and every file is verified on size and sha256.
- **My row replay** at engine `98e22f2f`, each arm bound to its own r_DMG and r_HP by hex. R2 and non-ladder are bound from legolas's operand file, sha `e245b4a8…`, which is checked. Per-cell readback must match bit for bit.
- **Leech HP-chain identity**, the runs gate, OBS-1, effect gates, dot conservation and POST-HOC completeness.
- **Then the registered item.** Grader functions `0ab979a7`, H = 40,000.

## Batch 1: the r_HP arms (registered: ADDENDUM-A § C, offered damage per tick, RAW sense, her arms only, **R2 ≤ R1 ≤ non-ladder**, paired totals; M-c printed un-ordered)
| Arm | godot | Pins | Replay (own r_HP bound) | Identity | Gates | Registered → result |
|---|---|---|---|---|---|---|
| **R2** (r_HP 29.152836858187047, hex `403d272050fb8969`) | `e33d377` | `dfdd0dcd…` 75 / 75 | **PASS 25 / 25 every class**, 0 provenance mismatches | 25 / 25, 7.3e-17, 0 off-ledger | all PASS (6 orphans, all TERMINAL) | **R2 ≤ R1: TRUE.** Offered per tick 5,670,849 vs 7,222,531 (×0.785). **0 / 25**, p = 5.96e-8. M-c printed only: 1,914,829 vs 1,991,085 |
| **non-ladder** (r_HP 54.059548939006774, hex `404b079f4cb4c5d6`) | `fe93638` | `44d860dd…` 75 / 75 | **PASS 25 / 25 every class**, 0 provenance mismatches | 25 / 25, 6.7e-17, 0 off-ledger | all PASS (9 orphans, all TERMINAL) | **R1 ≤ non-ladder: TRUE.** 7,222,531 vs 9,467,914 (×1.311). **25 / 0**, p = 5.96e-8. M-c printed only: 2,091,026 vs 1,991,085 |

- **The full registered chain R2 ≤ R1 ≤ non-ladder holds**, with every cell in order.
- M-a, printed: 25 / 25 in both arms.
- drax's own report HALTs on these arms because it uses the replay at `90e12d52`, which binds R1. My replay binds the arm's own r_HP and PASSes.

## Batch 2: the receivers and Static (one lever each; POST-HOC SEMANTICS per KP-476)
**Common to every arm in this batch:**
- pins 75 / 75, drax's committed pin file == the bulk copy;
- my replay PASS 25 / 25 in every class, primary binding, 0 provenance mismatches;
- leech HP-chain identity 25 / 25, worst ≤ 1.3e-16, 0 off-ledger falls;
- runs, OBS-1, effect gates, dot conservation and POST-HOC completeness all PASS. Every orphan is TERMINAL.

| Arm (row) | godot | Pins | Registered prediction | Result |
|---|---|---|---|---|
| **block-gd** (19; L-23 `gd` = no block, draws consumed) | `ffff26c` | `47b3d694…` | NC-J4b-BLOCK / NC-ROW19: **Σ intake higher with block off**, paired totals (A1 § C) | **FALSE.** Strict reversal: block-off 6,305,422 vs d2 6,338,689 (−33,267, −0.5 %). 9 / 10 / **6 ties**, p = 1.0. **Diagnostic:** the 6 cells with no block in the primary are byte-equal in intake (Δ 0). The whole Δ is in the 19 cells where 1–5 blocks fired, and there it has both signs (−121,540 … +203,405): one changed block shifts the rest of the cell's trajectory. Blocks 41 in the primary; 0 in the arm. Draws in the arm 504 (consumed) |
| **potion-gd** (21; the oracle's K-4 law on her sheet) | `89292c8` | `eb656d55…` | NC-ROW21: d2-belt **≥ gd** on survival and on realised casts/s in the mana-bound phase | **TRUE on both.** Survival **25 vs 14**. Casts/s 74.80 vs 57.12 (Σ over cells), **25 / 0**, p = 5.96e-8. The mana-bound phase is not delimited in registration, so whole-cell casts/s is used (POST-HOC operationalisation) |
| **potion-none** (21; empty belt) | `eb165bf` | `3543b55e…` | NC-ROW21: d2-belt **≥ no-potion** on survival and casts/s | **TRUE on both.** Survival **25 vs 0**. Casts/s 74.80 vs 57.43, **25 / 0**, p = 5.96e-8 (same operationalisation) |
| **dot-gd** (23; the sealed `dot_timeline`) | `eca3e23` | `ea7d1d2c…` | NC-J4b-ROW23: per **landed DoT application**, intake d2 ≤ gd, paired over cells; totals NOT graded | **NO VERDICT.** Under `gd` the receiver is the sealed timeline, and its registrations are not exported: 0 per-application rows, GC 0. The per-application form cannot be formed. (d2: 462 applications.) A provenance counter of gd applications per cell would close it |
| **chill-off** (24) | `e2d99c5` | `1ce7f525…` | NC-J4b-ROW24: row identity on chilled ticks; per-moving-tick displacement **d2 ≤ off**, sign test | **NO VERDICT.** The contract carries no per-tick player displacement trace and no chill-on-her count (NO-ARM-ITEMS § 2). ⚑ The `fa_chill` counter is row 29 (monsters chilled by her Frozen Armor), **not** row 24 |
| **resist-referent** (25; the sealed `RESIST_PCT`, git blob `05227445`, armour leg off) | `d43fd22` | `bb8319df…` | A4 § 5: paired Σ intake per landed hit, **hers ≥ the Warlord's map** | **TRUE.** Per cell: Σ G3 intake / landed G1 hits. 157,064 vs 117,429 (Σ of per-cell means), **24 / 1**, p = 1.55e-6 |
| **static-off** (28; Static removed from her castables) | `f25086a` | `e481518c…` | row 28: **`off` gives zero Static packets** (plus row identity per packet on the primary) | **TRUE.** 0 Static packets over 25 cells (primary 3,103), and no `static_casts` counter fired |

M-a under each lever, printed only: block-gd 25, potion-gd 14, potion-none 0, dot-gd 25, chill-off 25, resist-referent 25, static-off 25.
