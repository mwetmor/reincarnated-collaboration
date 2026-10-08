# Finding — 2026-10-08 — JOIN-1 J3d port-lever forms prereg (L-02 / L-03 / L-07 / L-08), DESIGN-MODE delta

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: one prereg amendment, alone, before fail-first)
**Target:** engine `dfdb6a9f`, `src/reincarnated/simulation/math/join1-j3d-port-lever-forms-prereg-2026-10-08.md`; against design `d97e1fc0` §§ 3.4–3.6, 4.5–4.6
**Developer:** gamora · conductor gandalf (KP-399)
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

## WARN-1 — The L-02 form is not the sealed per-body expression, so G-L02-1's claim that n = 1 equals the sealed loop is false as written

**What the sealed packet actually is.** `PlayerOffense.damage_against` (`player_offense.py:516–541`) returns:

```
applied_damage(raw · banner_factor(dmg_mult), armor, absorption, res_physical + res_bonus_pct, crit) × vector_fold.k(record)
```

with k applied only when `out > 0`. The C-11a aura `res_bonus_pct` is added to resist. The loop at `run.py:3066–3150` uses `applied = min(tick_damage_b, hp)` and `heal_basis_against(…, raw_damage=tick_damage_b)`, where `tick_damage_b` **includes k**.

**What the prereg's form does.** `packets_applied(raws, armor, absorption_pct, res_physical_pct, hp, crit_mult)` carries **no k, no banner and no `res_bonus`**. So:
- G-L02-1 tests against `min(applied_damage(raw), hp)`, which is not the loop's expression whenever k ≠ 1 (I-23's vector fold is live on the board), the banner is up, or an aura covers the body;
- G-L02-6's `frac_k = applied_k / a_k` uses the wrong denominator.

**Action:**
- Define `a_k` as the sealed per-packet `damage_against` expression: banner-applied raw, `res + res_bonus`, × k when > 0. The form takes k and `res_bonus` as operands, or calls a raw-override of `damage_against`.
- Restate G-L02-1 as **n = 1 ≡ `min(PlayerOffense.damage_against(record, dmg_mult, res_bonus), hp)`**, bit-exact.
- Add grid rows with k ≠ 1 (and k on an immune body: still 0.0) and `res_bonus` > 0.
- **`proportional_applied` (L-08 `yes`):** declare whether k and `res_bonus` apply. I suggest `res_bonus` yes (it is physical resist), and k no (k is the weapon's damage-type composition, not the proportional packet's), as JUDGED pending legolas Q-3.

## INFO-1 — "Installed on no A-2 row": HOLDS by construction

The forms are pure. `PortOnlyLever` and `L08Unset` refuse at the profile, and certification at defaults is unchanged. The close-out diff check (`d5384b4b` → J3d, forms and refusals only) is the right proof.

## INFO-2 — A port-only lever (engine grid, no engine emission) is ACCEPTABLE for J4, labelled and with one cheap strengthening

- The grid proves **arithmetic** parity (P-J3-4). It does **not** prove **integration**: where in the per-body loop the form is called, its order against leech, sustain and death bookkeeping, and event counts. With no engine emission there is no cross-mirror emission parity.
- Acceptable as a **declared limit**. J4's fidelity table should label L-02/L-03/L-07/L-08 rows **"PORT-EMITTED · ENGINE-GRID (arithmetic only)"**.
- **Recommended, not required:** a **row-level replay** at J3c. An out-of-tree Python checker reads the port's per-packet G1/G2 records (raw, armour, absorption, res, k, hp_before) and recomputes each through the engine form, bit-exact. That gives cross-mirror evidence at the row level with no oracle edit and no hot-loop transcription.

## INFO-3 — The other forms: SOUND

- **`packets_applied` semantics:**
  - per-packet sealed chain, min with remaining HP, after-death packets apply 0.0 and are counted;
  - the leech pool is aggregated (linear, so equal to the per-packet sum);
  - the sustain basis is one record per packet (proration is nonlinear across the kill);
  - correct once WARN-1 fixes `a_k`.
- **`hp_after_max_change`:** the domain is right, and `min(…, M2)` on `preserve-fraction` correctly absorbs the possible ulp overshoot at h = M.
- **`proportional_raw`** and **`killable_under`:** correct as stated.
- **The ADJ-J4 JUDGED defaults behind operands** (post-weapon HP, no leech) are the right shape. legolas's Q-1…3 can upgrade them with a value change only.

## INFO-4 — Port controls restated as paired totals: CORRECT, one wording fix

NC-J3-L07-1 says "L-08 at its default `yes`". Under R-5 / `L08Unset` that profile **refuses**, so it must state `l08 = yes` explicitly.

## INFO-5 — Carry into J3c's MIGRATION

- The new pin (the J3d commit).
- My J3b close-out WARN-1 (`bb6a86230`) is **still open**: the row-36 port site and the KP-360 scope cross-reference.

## L-08 ratification (§ 5)

It is already **Active** in the decisions-log (2026-10-08, J3 Gate-1). It stated it does not wait on NC-J3-L08-1. I have added a J3d entry that **binds the implementation** to it and records the WARN-1 `yes`-chain operands. No re-ratification was needed.

## Action
- [ ] gamora: AMENDMENT-1 (alone) folding WARN-1 and INFO-4; then fail-first.
- [ ] drax / conductor: INFO-2 labelling (and, optionally, the row replay) at J3c; INFO-5 into MIGRATION.
- [ ] Matt: none.

## References
- engine `src/reincarnated/simulation/kc2/player_offense.py:516–541`, `run.py:3066–3150` (read-only)
- engine `design/decisions/decisions-log.md`, entries "JOIN-1 lever L-08 … RATIFIED" and the J3d entry of this date
