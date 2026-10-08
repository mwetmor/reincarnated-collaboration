# Finding — 2026-10-08 — JOIN-1 J3b AMENDMENT-1 + AMENDMENT-2 (per-kit-pulse energy charge, row 36), delta

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **GO**; fail-first may proceed)
**Target:** engine `a2a8099e` (AMENDMENT-1), `463342a2` (AMENDMENT-2); `src/reincarnated/simulation/math/join1-j3b-levers-prereg-2026-10-08-AMENDMENT-{1,2}.md`
**Developer:** gamora · conductor gandalf (KP-387/388/389)
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

## (1) The substitution claim: VERIFIED by reading the code

- `run.py:48` does `from .energy import … charge_per_tick`, a module global. `run.py:1260` (`per_tick_cost = charge_per_tick(tps, DrainUnit.PER_TICK)`) looks it up at call time, so rebinding `run.charge_per_tick` substitutes it without touching `simulate_wave` or `kc2/**`.
- **That is the only fight-path charge.** The only energy assignments in `run.py` are `:2303` (income, `(regen + leech_while_up) × period`, invariant per second) and `:2321` (`energy -= per_tick_cost`). `refuses_activation(energy, per_tick_cost)` at `:2316` reads the substituted value, which is consistent.
- Other readers (`micro_oracles.py:212/471`, `per_cast_energy.py`, and `EnergyModel.drain_per_s` internally) are off the fight path or report-only. The `drain_per_s` split is declared. No script rebinds the name. **Nothing disagrees on the fight path.**

## (2) The law: CORRECT and bit-identical at defaults

I computed these from the sealed functions in f64:

| AS | `charge_per_tick` | drain per second |
|---|---|---|
| 196 | 14.4 | 176.4 |
| 200 | 14.4 | 180.0 |
| 300 | 14.4 | 270.0 |

- `charge_per_tick(tps300) × (196/300)` = **9.408**, and × 18.75 = **176.39999999999998**, against the referent's 176.4: one ulp.
- At h == 1.0 the sealed value is returned unmultiplied, so it is bit-identical by construction.
- The law preserves L-22's measured meaning (drain ∝ the kit's attack rate; PER_SECOND was refuted). So it is a derived generalisation, not a free choice.
- **Proportional every tick vs impulse is an honest, declared choice.** **INFO-1:** also declare its one side effect. The dry-out threshold `refuses_activation(energy, cost)` drops from 14.4 to 14.4·h (9.408). The Warlord keeps channelling with energy in [9.408, 14.4), where an impulse law would refuse on pulse ticks. The effect is small, and its direction favours the kit. It belongs in the § 1 choices list.

## (3) L01-W at X = 200 with ORACLE-TWIN@200: SOUND

- At world = kit = 300 the oracle's own law drains 270/s, and the twin dries out at w151 too. So the 300 % dry-out belongs to the referent's economy, not to JOIN. Moving the reach control to 200, where the sealed run completes (180/s), is correct.
- Keeping the `9047b515` 300 % runs as finding evidence, marked INVALID as controls, is the right disposition.
- **INFO-2 (for J4a):** a kit at 300 % that inherits the Warlord's channel cost dries out by the referent's own law. J4a kits must bring their own resource law, or that is a balance finding, not a bug.

## (4) L01-P re-predictions: FALSIFIABLE

- New predictions: (c) `charge_bound` == {9.408: k}; (d) **25/25 sim terminals** (the substantive prediction the HALT motivates); (e) row-32 per world tick < J-S8 (structural).
- Survival, ticks and intake at X = 300 are reported, not predicted, which is correct for a reach control.

## (5) L04-1, L05-1 and L05-2 stand: VALID, on one check

- Row 36 is inert at h == 1.0. **INFO-3:** "differs only by row 36" is a claim about a commit not yet made.
- **The J3b close-out must print `git diff 9047b515 <record> -- src/join2_rulebook`** and show that it is row 36 + `charge_bound` + the census key only. If anything else moved, those runs are re-run.
- L04-2 being re-run (NO VERDICT) is correct.

## (6) WARN-1 (`60df9ee60`): DISCHARGED

- `acc_bound` counts every row-31 accumulator, GD included, with `row31_calls` as the anchor.
- `frame-breakpoint` → effective AS, then `hits_per_tick = eff/world`, refusing above the world.
- NC-J3-L01-P is added.
- INFO-1…4 are all folded in: the twin's conditions, the port refusal for `hits_per_tick` < 1 carried to J3c and MIGRATION, NC-J2-5b retired with the test updated, and the `holds` mislabel declared.

## Action
- [ ] gamora: add the INFO-1 clause to AMENDMENT-2 § 1 (append-only, may ride the fail-first commit's message or a one-line corrigendum). Print the INFO-3 diff at close-out.
- [ ] conductor: carry INFO-2 into J4a kit intake.
- [ ] Matt: none (KP-388 is under delegation; Matt informed).

## References
- engine `src/reincarnated/simulation/kc2/run.py` (48, 1257–1261, 2303, 2316–2321), `energy.py` (50–68), `micro_oracles.py` (212, 471). All read-only; f64 values computed by importing the sealed modules, with no writes.
