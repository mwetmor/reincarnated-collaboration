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
