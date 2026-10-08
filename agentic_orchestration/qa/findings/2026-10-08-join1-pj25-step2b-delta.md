# Finding — 2026-10-08 — JOIN-1 P-J2-5 step 2b (population A + B + pet closure), delta check

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **GO**; star-lord may cut pack v3 `offense_da` at 248 rows)
**Target:** engine `7a8fc0f3` (prereg), `604a5d2f` (census), `d7561387` (run instrument), `8c6c2f3e` (AMENDMENT-4 corrigendum); collab `910048891` (evidence), `af7535540` (G-D3 README amendment)
**Developer:** gamora · conductor gandalf (KP-379/380/381)
**Principles applied:** 1, 3, 5 · Disciplines #10, #12

## (1) Spawn paths: COMPLETE, and the reason is structural

I read `run.simulate_wave`. A cell's bodies come from exactly three places:
- **`roll_wave`.** `rng = random.Random(seed)` at `run.py:1214`, with `roll_wave(wave, rng, …)` at `:1234` **before any fight draw**. The pre-pass calls it with `seed = engine_seed(CONDUCTOR_SEED, w)` per wave (`i26` :483–484).
- **`ReferentLineupFold.roll`.** It has its own `Random("kc2-referent-lineup|salt|wave")`.
- **Pet contracts**, firing only from `on_board` line-up and roll actors (`run.py` ≈3485–3500).

Two things show nothing else spawns bodies:
- `_perturb_regular_count` only re-uses records already in the roll, and nothing in the emitter path sets it.
- The pet contracts the fight uses are `th.load_pet_contracts()[0]`, both by default and through the `i26` substrate (`:1150`). That is the same object the closure uses.

**Consequence: every non-pet spawn is trajectory-invariant.** It is fixed by the wave's seed, salt and fold, and not by the fight. That holds under any crit profile, because the JOIN streams are separate RNGs. So B read from the census is exact, the static A is a superset, the 19 capped-out pairs cannot spawn under any trajectory, and only *which pets* spawn can vary, which the closure covers.

C-0 (the struck union equals the 196 exactly) validates the probe. **HOLDS.**

## (2) The counts: CONSISTENT; label them as re-derivations, not predictions (INFO-1)

- The arithmetic is consistent: 173 + 62 − 26 = 209; 209 + 34 + 5 = 248; 248 − 196 = 52 = 5 + 47. `counts_ok` is true, and `path_subset_of_P` is true.
- But the census ran before the prereg, and its output produced § 0, so these figures were known when they were "predicted".
- They are **determinism and re-derivation checks** (with a HALT on mismatch), which is worth having, but not risky predictions. The genuinely unknown measurement was S2b-CLASS. Say so in one line at the next touch.

## (3) Census before commit: ACCEPTABLE AS DECLARED (INFO-2)

- The census is descriptive and read-only on the oracle.
- Its 25 outputs are sha-recorded in `s2b_report.json` (`census_shas`), and C-0 validates it.
- The rule it grounds is a sourcing **scope**, not a hypothesis. The real falsifier is the § 3 closure test on the re-emit.
- *Optional, cheap:* re-run one cell of `604a5d2f` as committed and compare its sha against `census_shas`. That would turn "committed unchanged" into a checked claim.

## (4) S2b checks: HOLD

From `s2b_report.json`:
- S2b-CAL-1 74/74, max Δ 0.0.
- E_L 130.36799999999994, bit-equal.
- REPRO 122/122 bit-equal.
- MEAS 5/5, Δ 0.0.
- CLASS **47/47 CERTAIN**, min p 107.131, min level margin 20.91.
- The 5 depth-2 pets are included and labelled. `ghost_a01_summon|153` is at p 123.24.
- Edition IV; buildid 24825149 checked; record shas OK.

## (5) No carry-over: HOLDS

- Actors and `pet_state` are locals of `simulate_wave(w)`, and `PlayerOffense` and `SecondaryStreams` are built per wave.
- Empirically, 0 cases occur in 25 cells.
- Every G-D3 terminal row ends at wave 160.

## (6) Closure test: WELL-POSED; tighten the instrument (INFO-3)

Before the re-emit, commit fail-first a **named** rulebook counter, for example `guard_lookups_outside_P` per cell, plus a `looked_up` set. It should:
- tally **all three** PATH_Q lookups (EoR damage, Soulfire, bleed) against pack v3 `offense_da` keys;
- be predicted 0 in 25/25 cells.

Because the guard raises at the first miss, the count per cell is 0 or 1. Also report coverage, |looked_up| / |P|.

## (7) WARN-1 (`13cc43bd8`) and INFO-3: CLOSED

- **WARN-1:** the population is now the roster plus B plus the transitive pet closure, with a closure test and a carry-over check.
- **INFO-3:** `af7535540` restates the survival reading as low power with an adverse direction, discloses the non-random exclusion, and makes D-1 a fresh prediction. `8c6c2f3e` corrects the direction of the AMENDMENT-4 statement.

## INFO-4 (new, one line for gamora)

The pre-pass runs inside `c11a._period()`, which is the period calibration. Under `gd-decoded`, confirm whether the pre-pass fights draw on the JOIN crit streams. If they do, the calibrated **period** may differ from J-S8's, and that would confound the G-D3/G-D4 comparison through the world clock. Report period(`gd-decoded`) against period(J-S8) per cell on the re-emit; equality is the expected answer.

## Action
- [ ] star-lord: pack v3 `offense_da` (248 rows) may proceed.
- [ ] gamora: INFO-3 counter, fail-first, before the re-emit; INFO-4 period check on the re-emit; INFO-1 wording. INFO-2 is optional.
- [ ] Matt: none.

## References
- engine `src/reincarnated/simulation/kc2/run.py` (1214, 1234, 1705–1717, ≈3485–3500, 5180); `scripts/gamora_kc2_pm4_i26_spawn_structure_fold_2026_08_16.py` (483–484, 1150); step-2b scripts `604a5d2f` and `d7561387` (`population()` lines 45–92). All read-only.
- collab `agentic_orchestration/gamora/analyses/2026-10-08-join1-pj25-step2b/run-edition-IV/s2b_report.json`
