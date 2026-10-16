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

## Batch 3: the body-off arms (rows 11–14), graded on the cells that ran; refusals named (KP-500 reruns to follow)
**Added label:** **INSTRUMENT ADDED AFTER RUN.** My replay's `--body-off` binding (engine `640fdc76`; fail-first `acdc1d9b` / `40e2235c`) was added after these arms ran.
- The binding: the off body's rows carry offered = d = applied = 0 with the roll still the tape's. For splash, at most one damaging row per explosion.
- **Every cell's zeroed count equals the lane's own `t2_body_off_packets`** (e.g. M0|1 in body-fire_ball: 911). The label must be `J4B-T2-body-<x>`.

**Common to all four arms:**
- pins 75 / 75, committed == bulk;
- replay PASS on every graded cell, every class, 0 provenance mismatches;
- leech HP-chain identity holds, 0 off-ledger falls;
- effect gates, dot conservation and POST-HOC completeness PASS. Every orphan is TERMINAL.
- **Three of the four arms carry ONE refusal each**, `ControlFamilyUnmapped: Confusion` (diagnosis collab `739da26ae`; KP-500 ruled option A). Each is a **named result, not a drop.** The arm is graded on the other 24 cells.

**Registered (base § 9; prereg § 2 rows 11–14):** *"the body off, … her Σ damage dealt falls (paired totals)"*. Here Σ damage dealt = Σ `applied` over the whole cell (HP-capped), paired; FALSE only on a strict reversal.

| Row / arm | godot | Cells graded | Refusal (named) | Registered → result | Not graded: M-c per tick (off vs on) |
|---|---|---|---|---|---|
| **11 Fire Ball** (`body-fire_ball`) | `e868512` | **24** | **W1\|2**, tick 1929, Confusion (Blugrug, w157) | **FALSE.** Σ applied **rises**: 3,286,841,331 vs 2,716,394,572, **24 / 0** | 1,245,927 vs 1,913,833, **0 / 24** |
| **12 Meteor** (`body-meteor`) | `a61d1df` | **24** | **M0\|3**, tick 1151, Confusion | **FALSE.** Rises: 2,855,913,349 vs 2,712,397,374, 21 / 3 | 1,772,786 vs 1,910,947, 2 / 22 |
| **13 splash** (`body-splash`; FB secondaries 0) | `6e018aa` | **25** | none | **FALSE.** Rises: 3,153,829,939 vs 2,823,389,414, **25 / 0**. Signature: 4,770 explosions, 0 with more than one damaging row, 11,464 zeroed secondaries | 1,813,091 vs 1,991,085, 1 / 24 |
| **14 burning ground** (`body-pyre`) | `df4a2dc` | **24** | **M-POL-2-NULL\|3**, tick 956, Confusion | **TRUE**, barely: 2,711,870,491 vs 2,713,789,852 (−0.07 %), 9 / 10 / 5 ties, p = 1.0 | 1,903,104 vs 1,913,957, 8 / 11 |

**⚑ Why Σ applied rises when a body is removed (diagnostic, printed, not a re-grade):**
- Every arm clears every wave (her M-a is 24 / 24 or 25 / 25), so Σ applied is the **board's HP removed**: the roster's HP, plus monster leech healing, plus the pets and summons that spawn while a wave lasts.
- Taking a body away **lengthens the board**:
  - body-fire_ball: 63,464 vs 34,088 ticks;
  - kills 8,931 vs 7,600, because more summons spawn;
  - monster leech heal 275 M vs 18 M.
- So the HP-capped total **grows** while her output per tick **falls** (last column).
- **The registered metric cannot fall under kill-to-clear with an HP cap.** That is why it is FALSE as registered. Nothing is re-graded.
- ⚑ **Row 14's TRUE is within noise** (the pyre is a small share of damage; 5 cells are unchanged). **The KP-500 rerun of M-POL-2-NULL|3 can flip it.** The 25-cell grade decides.
- **(Third refusal, not in the relay: body-pyre M-POL-2-NULL|3, tick 956.)**

## Fraction (b), updated after all four body arms (24-cell body grades; rows 23 / 24 await drax's trace arms)
Format: "N demonstrated ACTIVE + M REACHED-INSENSITIVE (named) / 23". ACTIVE requires reach > 0 **and** the row's NC passing.

| Status | Rows |
|---|---|
| **ACTIVE** (NC passed, reach > 0) | 8, 10, **14**, 15, 16, 17, 20, **21**, 22, 25 (non-magic families), 26, **28**, 31 |
| **FAILED NC** (listed, never folded in) | **11, 12, 13** (body off: Σ applied rose), **19** (block off: Σ intake did not rise) |
| PARTIAL (NC not fully demonstrable on the contract) | 9 (her displacement during CAST), 32 (per-hit identity needs the S17 packet id) |
| **OPEN** | **23, 24** (pending the `--rb-row2324-trace` arms, quantities fixed at engine `6587ffe8`); 29 (forced-landing fixture not run); 30 (destinations not in the contract; binomial 5 / 43 printed, no α) |

- **Line:** **13 demonstrated ACTIVE + 0 REACHED-INSENSITIVE / 23**, with 4 failed NCs (11, 12, 13, 19), 2 partial (9, 32) and 4 open (23, 24, 29, 30).
- **The registered prediction "22 ACTIVE + 1 RI (row 22) / 23" is FALSE AS PRE-STATED.**
- Row 14's ACTIVE is provisional on the KP-500 rerun.

## Batch 3b: rows 11, 12, 14 on 25 cells — **CELL RERUN UNDER KP-500** (beside the 24-cell grades, which stay of record)
**The reruns:** godot `fb4d5a9` (fix `12d4eff`, runner `d6cf39b`). The pin file `89d42aa1…` verifies **55 / 55**. Labels are `J4B-T2-body-<x>-rerun-<cell>`; my replay accepts them (engine `84fd698e`, fail-first `1f4e2c21`).

**Checks on each rerun cell** (`kp500-reruns-25cell.json`):

| Rerun | Bound replay | Identity | Gates | Same construction route as the filed 24? |
|---|---|---|---|---|
| Fire Ball **W1\|2** | **PASS** every class; 909 zeroed == the lane's counter; 0 mismatches | 1.8e-16, 0 off-ledger | all PASS | **Yes.** Settings readback (anchor, r_HP, r_DMG, L-21, kit, pack digest) equal. Runtime tag, rulebook commit / tree, operand pack and dump equal. **Every row before the refusal tick 1929 is byte-identical** (G1, G2, G4, GO, GH, GR, GM; G3 waves 151–156; 185 GB spans closed before 1929). The only provenance differences are the KP-500 fix itself: `kc2rb_d2lane.gd`, `kc2rb_d2_laws.gd` and the JOIN tool sha. `control_dropped:Confusion` 1. Survived to 160 |
| Meteor **M0\|3** | **PASS**; 66 zeroed | 3.1e-17, 0 | all PASS | **Yes**, the same checks. Prefix before tick 1151 identical. Confusion dropped 1. Survived |
| pyre **M-POL-2-NULL\|3** | **PASS**; 535 zeroed | 2.4e-17, 0 | all PASS (3 TERMINAL orphans) | **Yes**, the same checks. Prefix before tick 956 identical. Confusion dropped 1. Survived |

**Registered "Σ damage dealt falls", graded once on 25 cells:**

| Row | 24-cell (of record) | **25-cell, CELL RERUN UNDER KP-500** |
|---|---|---|
| **11 Fire Ball** | FALSE (24 / 0) | **FALSE.** 3,433,234,496 vs 2,823,389,414, **25 / 0**, p = 5.96e-8 |
| **12 Meteor** | FALSE (21 / 3) | **FALSE.** 2,975,958,450 vs 2,823,389,414, 22 / 3, p = 1.6e-4 |
| **14 burning ground** | TRUE (−0.07 %) | **TRUE, unchanged.** 2,822,735,473 vs 2,823,389,414 (**−653,941, −0.02 %**), 10 / 10 / 5 ties, p = 1.0. Within noise; the rerun cell itself rose (110.9 M vs 109.6 M) |

- **Not graded:** M-c per tick, off vs on: Fire Ball 0 / 25, Meteor 2 / 23, pyre 8 / 12. M-a 25 / 25 in all three.
- **Row 14 did not flip, so fraction (b) is unchanged:** **13 ACTIVE + 0 RI / 23**. Failed NC: 11, 12, 13, 19. Partial: 9, 32. Open: 23, 24 (trace arms), 29, 30.
