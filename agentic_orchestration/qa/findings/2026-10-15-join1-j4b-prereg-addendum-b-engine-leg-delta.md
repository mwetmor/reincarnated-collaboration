# Finding — 2026-10-15 — JOIN-1 J4b PREREG-ADDENDUM-B and the comparator ENGINE leg, delta gate

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **PASS-WITH-NOTES**. The engine leg is valid, the sidecar fix is a measurement fix, and **the narrowing to waves {159, 160} is right**. The comparator's **port leg is still owed** before any graded run.)
**Target:** engine `a4d77ae2` (ADDENDUM-B), `d5a217ba` (its instrument), the sidecar `9b98db4e` → `2bd18836` (1e-9 gate) → `da29f39b` (real final HP); collab `0636752ba` (engine-leg evidence, `prereg_b.json` sha256 `cd73f50e…`)
**Developer:** gamora · conductor gandalf
**Principles applied:** 1, 2, 5 · Disciplines #10, #12

## The engine leg: VALID
- **`compare_vs_4c30b0d64.json`** (read here): **G1–G7 FILE-equal 7/7 and ROWSET-equal 7/7** against `4c30b0d64`. For example, G1 has 50,767 rows, with FILE `67b4f336…` and ROWSET `8a8acaed…` equal to the reference. The KP-386 instrument ran as committed, with the rulebook `3eefaa2e` unmoved.
- **The sidecar** (`da29f39b`): its G1–G7 equal the instrument's row for row on **25/25** cells. The leech-reconciled identity holds on **25/25**, with a maximum relative residual of **5.3e-14** against the 1e-9 gate and 0 off-ledger falls. My INFO-1 tightening (1e-9), INFO-2 (the applied-heal meaning, with overheal separate and never added) and INFO-3 (graded calls only, with `n_graded_runs` = the G7 rows) are folded in `2bd18836`.
- **His M-c is 37,966.8 per tick** (37,961.7 without summons). GO's sources are EoR disc, Soulfire, the bleed rider, and his two pet skills; the summons are included per CORRIGENDUM-1.

## `da29f39b` is a MEASUREMENT fix, not a meaning change: CONFIRMED
- The identity CORRIGENDUM-2 registered, `Σ applied = Σ (initial − final) + Σ leech_heal_hp`, is **unchanged**.
- `2bd18836` measured "final HP" as **the last `hp_after` in the chain**. That is the wrong instrument for a body that **survives the wave and keeps leeching after its last player hit**: its post-hit heal is in the telemetry but not in the chain. Hence W1-NULL s0 / s2 failed (relative −6.9e-5 / −2.7e-4), with 0 chain breaks.
- `da29f39b` reads the body's **real final HP** from the oracle's own state, through a **pass-through observer** on `MutatorFold.leech_heal` (graded window only; it returns the oracle's value unchanged).
- That is the quantity the identity always named. **The observer effect is bounded by evidence:** the sidecar's G1–G7 still equal the instrument's 25/25.
- **The two added gates are sound:** observed heal equals fold telemetry (1e-9), and the heal on never-hit bodies is 0.
- **Keeping the superseded `2bd18836` run on file** is the right record.

## ADDENDUM-B: registering the CONJUNCTION (waves {159, 160}) rather than all 10 is RIGHT

**The registered reading measured release, not arrival.** The `spawn` rows all carry the wave-start tick, and `Mover.spawn_t_s` releases every body within the first seconds, after which they march. Under it every wave is "kill-limited" (0.82–1.00), but that is a property of the release schedule. **It does not answer WARN-1's question** (is the wave's length set by his kill rate, or by bodies reaching him?).

⚑ **The imprecision is mine.** My `eb9ec1a10` asked for "the last-arrival tick from the trajectory-invariant spawn schedule", conflating *release* with *arrival at the player*. Arrival is trajectory-dependent, because the bodies march.

**The measured-arrival reading answers the question.** It takes the latest first-hit tick on a roster body from **his** GO; his disc hits whatever reaches it, so first-hit ≈ arrival within his reach. On it, 8 of 10 waves are **arrival-limited** (tail 0.026–0.235). Only 159 (0.298) and 160 (0.375) clear the pre-stated 0.25, and both also clear the capacity ratio ≥ 1.67 (2.33, 2.79).

**Registering on all 10** would put a direction on waves where both kits' realised M-c converge on the spawn flow. That is the near-tie WARN-1 existed to avoid, reached through an instrument that returned cleanly after it stopped answering the question.

**The narrowing is legitimate:**
- it was decided from **his** data only, with no emission of hers read (the provenance holds; the instrument `d5a217ba` reads his G7, the sidecar's GS / GO and `prereg_a.json`);
- it **narrows** the claim rather than widening it;
- the broader set is left to this gate, which declines it.

**The pairing rule is pre-stated and right.** Only cells where both kits reached wave 159 are paired, so survival is not double-counted through M-c. The dropped cells are listed.

*INFO-1:* the **"< 6 pairs → NO VERDICT"** floor is an extra rule beyond the grading law's strict-reversal criterion. It is accepted as a pre-stated minimum sample: with n ≤ 5 the exact two-sided sign test cannot reach 0.05.

## Notes
- *INFO-2:* the grader needs **fail-first tests** for:
  - (a) the wave restriction {159, 160};
  - (b) the pairing rule (both reached 159; dropped cells listed);
  - (c) the < 6-pair NO VERDICT;
  
  then the code. That is the conductor's next step.
- *INFO-3:* **the port leg is still mandatory** (ADDENDUM-A § E / WARN-2): `JOIN[warlord, gd-decoded @ 196]` on the J4b port digest, 7/7 against `4c30b0d64`. The port's GO / leech emission is under the same contract (applied heal; graded calls only). **Until it passes, the comparator is engine-valid only, and the J4b margin is NO VERDICT.**
- *INFO-4:* the measured-arrival proxy depends on his reach geometry (the disc radius) and on bodies he actually hits (roster only; pets excluded). That is acceptable for a registration rule, and both caveats should be printed beside the tail-share table.

## Action
- [ ] gamora: the grader's fail-first tests plus code for INFO-2; print INFO-4's caveats with the tail-share table.
- [ ] drax: the comparator port leg (INFO-3) under the GO and leech contract.
- [ ] jack-ryan: a narrow delta on the grader increment and on the port-leg evidence; then the first graded run may proceed.
- [ ] Matt: none.

## References
- collab `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-comparator-engine-leg/` (`compare_vs_4c30b0d64.json`, `sidecar/sidecar_report.json`, `prereg_b.json`, read here)
- engine `a4d77ae2`, `d5a217ba`, `2bd18836`, `da29f39b`
