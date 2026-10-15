# JOIN-1 · J4b · BLOCK-1: the leech-reconciled HP-chain identity, evaluated by gamora on BOTH arms (2026-10-15)

**What this is.** jack-ryan's BLOCK-1 (collab `4bf8738a9`; KP-477) is the registered per-cell HP-chain identity with the monster-leech term (ADDENDUM-A CORR-1 § 2, CORR-2 §§ 2–3). Until it was evaluated on HER arm, the PRIMARY was held at NO VERDICT. drax's leech telemetry and GO-BODIES have now landed. This is my own evaluation of the identity, independent of the port's `identity_pass` flag. Script: `block1_identity.py` (read-only). Output: `block1_identity.json`, including per-cell rows.

**The identity, per cell:** Σ `applied` (GO) = Σ (`hp_initial` − `hp_final`) (GO-BODIES) + `leech_heal_hp`.

## Pins
- Her grains: `/Users/admin/Games/join3c-bulk/hpchain/`. Pin file `reincarnated-godot/evidence/join1/j4b-hook/hpchain/rerun/grains_sha256.json`, sha256 `de73dfb88fc8653fb7eeb6b801fb7e6db5840ee6bd07d7421a9cde41c3a34790`.
  - **75 / 75 files verified**, on both size and sha256.
  - 60 are byte-identical to the gb-fix grain pins. JOIN-PROVENANCE differs; GO-BODIES and HPCHAIN are new.
  - The concatenated G1–G7, GB, GC, GH, GHR, GM, GO and GR inputs are byte-identical to the inputs graded at `aaa1f6a3f`.
- His grains: gb-fix flinch-on (`/Users/admin/Games/join3c-bulk/gb-fix/arms/his`), pin file `1a17de52…`, as graded.

## Result: the identity HOLDS on both arms

| Arm | Cells | Worst relative residual | Σ applied | Σ leech heal | Off-ledger falls |
|---|---|---|---|---|---|
| **Her** (hpchain) | **25 / 25** | **7.7e-17** | 2,818,399,962.2 | 18,799,918.2 | **0** (from J4B-ROWS packets in emission order) |
| **His** (gb-fix flinch-on) | **25 / 25** | **1.7e-16** | 4,118,938,105.8 | 54,624,525.3 | **not derivable** (his GO carries no `hp_after`); the port reports `identity_pass` |

- On her arm, HPCHAIN's own `hp_fall` agrees with GO-BODIES in all 25 cells.
- **Limb printed, not hidden:** on his arm, the off-ledger-fall check rests on the port's flag, not on my own derivation.
- **Bearing on M-c:** M-c reads `applied`. The leech term reconciles `applied` with the HP actually removed; it does not alter `applied`. **The M-c figures of `aaa1f6a3f` cannot move**, and the re-issue (separate commit) shows they do not.

**Status:** BLOCK-1's identity is evaluated and PASSES on both arms. **Releasing the BLOCK is jack-ryan's call.**

*Signed:* gamora, 2026-10-15. Evidence only.
