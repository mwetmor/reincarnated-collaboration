# JOIN-1 · J3 · INFO-Δ2 + INFO-Δ3: retiring `intake_order_override` and the ≥ 3.11 binder guard (KP-357)

gamora, 2026-10-08.

**Matt's ruling (KP-356):** the intake order is FIXED at `ARMOUR_THEN_RESIST`, "declared by lineage; GD's order undecoded".

## Engine commits (each ALONE)

| Commit | What |
|---|---|
| `228feeef` | **Instrument + fail-first tests.** The P-J2-9 script counts the fields itself (N = len(`_FIELDS`)) and checks that the pack has exactly one pack-only row. NC-J2-2 / NC-J2-2-sealed are RETIRED in the runner (`run_e4` refuses them; their lineage is recorded at collab `a36062ae6`). Tests: P-J2-9 30/30, NC-E5-1 29/30, retirement checked in `_FIELDS`, the A-2 JSON and `with_`, and the binder refuses Python < 3.11. **5 FAILED against `0dda17bd`.** |
| **`547ac177`** (tree `3b2e04dc…`) | **The rulebook commit (Δ2 and Δ3 together, by order: the instrument came first and was fail-first).** `intake_order_override` is removed from `_FIELDS` (31 → 30), from the `from_oracle` values and from row 4's form (no override branch; the form takes the caller's order, the sealed `IntakeFold.order`, so the order has one home). In the A-2 JSON, `control_only_operands` becomes `retired_operands` and row 4's `control_only_operand` is dropped. `CONTROL_ONLY` becomes `RETIRED_OPERANDS`. A control spec that names the operand now refuses (`with_` raises `KeyError`). INFO-Δ3: `install()` refuses CPython < 3.11. **129/129 J2 tests pass.** |

**Rulebook worktree:** `0dda17bd` → **`547ac177`**, clean.

**drax re-pins once, later, to `547ac17734a75c0cdec39f257b186e36a9f3a6b3`.**

## Results at `547ac177`

**P-J2-9** (`pj29.json`):
- **30/30 bit-equal.** Sources are ORACLE-CONST vs PACK; layers and provenance strings are 30/30.
- `pack_only_operands == ["intake_order_override"]`: the pack still carries the row, and it is not read.
- NC-E5-1…4 all pass (NC-E5-1 reads 29/30).

**JOIN[warlord, GD] golden master** (`golden-master/`; run under drax's C-9 courtesy gate, lock acquired after 0 s):
- J-S8 7/7 ROWSET-equal, and **all 7 grain FILEs are byte-equal to the fixture**.
- TA-X equal; 26 records; tree ok; 0 hits.
- Operand source is PACK; `operand_pack_at_bind` reads clean, tracked.
- A-2 digest `b15e0155…`.

**§ 4.7 v4 at engine HEAD `547ac177`** (`s47v4/`, `s47v4.stdout.txt`, under the courtesy gate): **ORACLE BYTE-IDENTICAL**. HEAD is fixed, and limbs A, B and B′ pass.

**At GD nothing moved.** The removed branch was never taken while the operand was `None`. The FILE-equal golden master shows it.

## Bulk evidence

The golden master's `emission` and `records` were moved to `/Users/admin/Games/join2-j3-delta2-bulk-evidence/golden-master/`. The manifests stay here.
