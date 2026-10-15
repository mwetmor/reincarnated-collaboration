# Finding — 2026-10-15 — JOIN-1 J4b ADDENDUM-A CORRIGENDUM-1 + CORRIGENDUM-2 (leech-reconciled HP-chain identity), narrow delta

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **PASS-WITH-NOTES**; the comparator re-emission may proceed under the restated identity)
**Target:** engine `d7f916a8` (CORRIGENDUM-1), `7741e4b6` (CORRIGENDUM-2, a #12 semantic shift), `9b98db4e` (the GO sidecar); against my delta `eb9ec1a10`
**Developer:** gamora · conductor gandalf
**Principles applied:** 1, 2, 5 · Disciplines #10, #12

## CORRIGENDUM-1: my `eb9ec1a10` is DISCHARGED
- **WARN-1:** the capacity-vs-realised M-c registration is withdrawn. M-c is now registered only on **KILL-LIMITED waves**:
  - the median `tail_share = (wave_end − last_arrival)/n_ticks ≥ 0.25`, pre-stated;
  - also requiring the capacity ratio ≥ 1.67;
  - otherwise UN-PREDICTED;
  - computed from **his** re-emitted grains only, as PREREG-ADDENDUM-B, alone, before any graded run.
- **WARN-2:** "unmodified" is withdrawn. The offense grain comes from an additive sidecar (GO + GS) that reads `run.events` (no wrapping, no draw). The instrument's G1–G7 must be byte-identical to `4c30b0d64`, and the sidecar's own G1–G7 must equal the instrument's row for row; either failure is NO VERDICT.
- **One M-c definition for both emitters** (HP-capped, roster + enemy pets per world tick), with his sources named. His summons are **included**, and no-summons is a sensitivity. The GO row contract is given.

## CORRIGENDUM-2: restating the HP-chain identity after a smoke failure is LEGITIMATE here

Four tests, all met:
1. **Whose data?** The failure was observed on **the comparator's own data** (one Warlord cell, M-POL-2 s0, scratchpad), **not her kit's**. No graded run was made, the re-emission had not started, and the smoke's digests are used nowhere. No registered prediction about her could have been informed by it.
2. **What kind of check?** It is an **instrument-validity** identity (I asked for it in `eb9ec1a10` as WARN-2(c)), not a directional prediction. A validity check whose premise is false **by the oracle's design** must be corrected, or every cell becomes NO VERDICT for a reason unrelated to validity.
3. **Is the correction mechanism-derived, not gap-fitted?**
   - The added term is the Crucible **Leeching** heal (`mutators.MutatorFold.leech_heal`, via `run.py` `_mut_leech`), named at its four call sites.
   - It is read from **independent telemetry** (`tel["leech_heal_hp"]`) that the oracle already keeps, not back-solved from the gap.
   - The gap equals that telemetry to **1.26e-6 absolute (7e-15 relative)**, **zero** off-ledger HP falls were seen, and the heal visible in the chain equals the same figure.
4. **Can the restated check still fail?** Yes, in three ways:
   - (1) **any** off-ledger HP fall breaks it (`n_chain_breaks = 0` required);
   - (2) the reconciled sum must close;
   - (3) the visible heal must not exceed the telemetry.
   
   The old form is still **reported** per cell. Framed as #12 before the run it gates, that is the right discipline.

**M-c is correctly UNCHANGED.** HP removed through a leech heal is real offense her kit (or his) had to spend, so `applied` stays in M-c.

## The tolerance: the observed residual is excellent; the registered bound is looser than it needs to be (INFO-1)
- **The observed residual is 1.26e-6 HP on Σ applied ≈ 1.7e8, i.e. 7e-15 relative. Acceptable**: double-precision accumulation over the cell's rows.
- **The registered gate is |Δ| ≤ 1e-6 × Σ applied, about 172 HP per cell.** That cannot hurt M-c (a 1e-6 relative effect). But it would let an unknown **off-ledger mechanism of up to about 170 HP per cell** pass unseen, and the identity exists precisely to expose such mechanisms; Leeching was found this way.
- *Recommended (non-blocking):* tighten to **1e-9 × Σ applied** (≈ 0.17 HP per cell). That is still about 10⁵ × the observed residual, so it is safe for the port's different accumulation order in IEEE-754 doubles.

## Her port must report the leech heal: YES. It needs NO new sealed site
- Leeching rides the **waves**, not the kit, so her cells see it too. Without the heal term, her identity cannot close, and her cells would be NO VERDICT.
- **The port already keeps the counter:** `kc2rt_mutators.gd:52` initialises `tel` with `"leech_heal_hp"` (and `"leech_overheal_hp"`), and `leech_heal(applied, b)` (`:233`) is called after each applied monster hit (`kc2rt_fight.gd:6334`).
- **So the JOIN tool reads `mut_fold.tel` through the KP-402 RecFight route.** It is a member read; it needs **no sealed edit and no new J4b site**.
- *INFO-2:* bind the **meaning**: the oracle's `leech_heal_hp` is the heal **applied** (the identity closed against it to 1.26e-6, so it is net of any cap). The port's `leech_heal_hp` must be the same applied quantity, with `leech_overheal_hp` separate. State it in the GO contract that goes to drax.
- *INFO-3: scope.* Read the telemetry **before and after each GRADED `simulate_wave` call only**. The c11a pre-pass also runs `simulate_wave`, and its leech heals must be excluded on **both** sides, matching the events the chain walks. State it in the contract, for the engine sidecar and the port alike.

## Action
- [ ] gamora: optionally tighten the tolerance to 1e-9 relative (INFO-1); add INFO-2 (applied-heal meaning) and INFO-3 (graded-calls scope) to the GO contract. None of this blocks the re-emission.
- [ ] drax (via the GO contract): emit the leech heal from `mut_fold.tel["leech_heal_hp"]` per graded wave, read-only.
- [ ] conductor: the KP-386 comparator emit may proceed when heavy_lock allows; then PREREG-ADDENDUM-B (alone) and my narrow delta on it.
- [ ] Matt: none.

## References
- engine `d7f916a8`, `7741e4b6`, `9b98db4e`; godot `kc2_runtime/sim/kc2rt_mutators.gd` (`:52`, `:233`), `kc2rt_fight.gd:6334` (read-only)
