# Finding — 2026-10-08 — JOIN-1 J3a `crit_model` prereg delta check + a glance at the P-J2-5 step-2 prereg

**Reviewer:** jack-ryan (delta check before code; KP-364; doc-only, no heavy lock)

**Severity:**
- **J3a prereg (engine `6e412839`): GO-WITH-AMENDMENTS.** 1 WARN (a prediction that is false as written) · 4 INFO.
- **Code may start once WARN-P1 is fixed in the prereg** (a one-line amendment, committed ALONE before the first J3a build commit).
- **P-J2-5 step-2 prereg (engine `756f1098`): nothing stops the run.**
  - 1 WARN: the guard must not land on the default path while § 3 shows anything other than all-CERTAIN.
  - 2 INFO, to be added as reported columns. They do not change the registered verdict classes.

**Checked against:** the sealed `threat.resolve_hit` (`threat.py:388-405`); the fixture G1 (`join1-gm-fixture-v1/oracle/G1.jsonl`, FILE `eb335eba…`); charter v0.7 (line 2).

---

## § 1 · The J3a prereg

### 1.1 The `m2_band` law and its input provenance: correct

- For p ≥ 100 the sealed miss test (`roll > p`) never fires. With a d100, only thr₁ = 70 and thr₂ = 90 can be cleared. The tier loop takes the highest threshold both p and the roll clear, so rolls 90…100 give tier 2 (×1.1), and every other landed hit is ×1.0.
- So **P(×1.1) = 11/100**, which is f64 `3fbc28f5c28f5c29` and equals the literal 0.11. **m = `PTH_MULTIPLIERS[1]`**, f64 `3ff199999999999a`. The mean is 1.011.
- Provenance is complete: the PACK operands `pth_thresholds` / `pth_multipliers` (LAW), the sealed roll convention, and p from the sealed equation over the table's OA and DA (or step 2's sourced DA).
- **p < 100 refuses** (`JudgedCritUndecided`). That is right, because the band law conditions on a certain hit.
- **INFO-P1.** The implementation draws `u = rng.random()` with a proc iff `u < 0.11`, which is a Bernoulli(0.11) **re-parameterisation** of the d100 band, not a d100. It is equal in distribution, but it is not the same draw sequence that a `randint(1, 100)` would give. State it once as such, so nobody later "corrects" it into a d100 and moves the stream.

### 1.2 J-1…J-3: stated as judgments ✓

- **J-1** chooses M2 by law, not by direction (R-PM4-27 part 3).
- **J-2** does not apply +57 %, because it is M3's premise. That is the right call: mixing two candidate rules would be the worse judgment. It is stated as a judgment.
- **J-3** prints the M1 / M2 / M3 / D-L5 bracket beside the value.

My C-2 is discharged.

### 1.3 The `JudgedCritUndecided` refusal before step 2 ✓

`gd-judged` refuses at the first player packet on a body without DA, and that refusal is control **G-J2**, predicted 25/25. Its emission controls (G-J3/J4) wait on step 2. This discharges C-2's "refuses until then".

### 1.4 The JOIN stream seeding law: acceptable

`random.Random(int.from_bytes(sha256(f"{arm}|{salt}|{stream_id}").digest()[:8], "big"))`, `u = rng.random()`.

**INFO-P2 (for the port mirror, before any cross-mirror stream claim):**
- State the hash input's encoding (UTF-8).
- State that the seed is a Python `int`, so CPython seeds MT19937 via `init_by_array` over its 32-bit words.
- State that `random()` is the 53-bit two-output construction.
- Add a **cross-mirror stream test**: the first 10,000 `random()` values of each stream id at (M-POL-2, 0) bit-equal on both mirrors. The port's `kc2rt_rng.gd` is CPython-exact for the oracle's streams, but arbitrary-int seeding is a separate path.

### 1.5 The 4σ binomial bounds

- The two-sided normal tail at 4σ is 6.33e-5 per test, so about 1.6e-3 over 25 cells, as declared. ✓
- **INFO-P3:** declare the **family-wise** rate. About six stream-bearing controls × 1–2 streams × 25 cells gives roughly 1e-2 per J3a sitting.
- **INFO-P3:** state the mean-stash bound's σ exactly: `σ_mean = (m − 1)·sqrt(c(1 − c)/N)`. The text's "4σ/N" is ambiguous.
- **INFO-P3:** say that limbs (b) and (c) of L06-4 / G-J3 are **the same statistic** (mean = 1 + K(m − 1)/N). They are one test, not two.
- **INFO-P3:** where N·c < 30 in any cell, use the exact binomial interval instead of the normal.

### 1.6 The controls: discriminating? Yes, with one prediction false as written

- **GM-0:** ✓, both mirrors, with 0 JOIN draws.
- **nc8k:** ✓. The property class has its own control.
- **LANE-0:** ✓.
- **LANE-1 on the port** is valid. Port monster G1 is observed from H-3's return. The summon rows are re-evaluated with the sealed law, which is exactly the law an intake-only setting leaves in force. **LANE-2 engine-only (ADJ-J6): ✓.**
- **NC-J3-L06-1:** ✓. I checked the fixture: **every one of the 25 cells has ≥ 2 monster ×1.1 rows** (minimum 2), so "first divergence per cell is a monster ×1.1 row" is structurally available in every cell.
- **NC-J3-L06-2:** ✓ (2,347 summon ×1.1 rows).
- **G-J1…G-J4** are well-posed. G-J3 prints the judgment's cost without predicting a direction, which is honest, since +1.1 % is below cell noise. C-3 is discharged by G-J4 plus the cost line.
- **WARN-P1 · NC-J3-L06-3's "the multiplier on every proc row is 1.5" is FALSE as written.**
  - The fixture has **98 monster hit rows below p = 70**, across all 25 cells. On those rows the sealed law returns the **sub-70 damage scalar** p/70, not ×1.0.
  - The design (§ 3.1) says that scalar "is unchanged by every value".
  - At c = 0.10, about 10 of those rows will proc. **The prereg never states what a proc does on a scalar row:**
    - (a) `scalar × m`;
    - (b) `m`, replacing the scalar;
    - (c) no proc below 70, as under the sealed tier law.
  - **Required, before code:**
    - choose one of (a)/(b)/(c), stated as a judgment, for both `independent-proc` and `gd-judged` (whose player lane has p ≥ 100, so it is unaffected on this board, but the law must be total);
    - rewrite the prediction as "every proc row's multiplier = m × the row's base (1.0, or p/70 below 70)" under (a), or the analog;
    - say whether a scalar-row hit draws from `crit:intake`. That affects limb (a)'s draw count.
- **NC-J3-L06-4 (a)–(e):** ✓, including the port draw-count form `sf_n_rows + skips` (INFO-1), and engine-only at J3a.

### 1.7 The KIT-layer rows for star-lord's pack v1: acceptable

- Four rows (model, chance, multiplier, bracket), labelled JUDGED, never DATAMINED.
- Not `_FIELDS` at GD.
- The existing rows' bits unchanged, so P-J2-9 stays 30/30 plus the new rows' self-consistency.
- **INFO-P4:** pack v1 changes the pack digest. So the rulebook's `PACK_PIN` moves in **its own rulebook commit**, the E5 pattern, with a P-J2-9 re-run and the golden master FILE-equal at the new pin. It is not folded into the J3a build commit.
- **INFO-P4:** the chance/multiplier rows are valid **only for p ≥ 100**. The provenance strings already say "M2 band on p >= 100", so keep that wording.

### 1.8 Already discharged in the prereg

- **C-1:** `gd-judged` touches the player stream only; decoded lanes are refused at bind; the registry prints per-lane status.
- **C-4:** charter **v0.7** sanctions `gd-judged` as a non-kit profile (confirmed at charter line 2), and the L-06 registry row cites it.
- **INFO-Δ4:** the `crit_tier` relabel is declared under #12.

**J3a may build once WARN-P1's amendment lands ALONE.** I do not need to re-gate it, since the rest is unchanged; I will check it at J3a's Gate-2.

---

## § 2 · The P-J2-5 step-2 prereg (a glance; the run proceeds)

**Sound:**
- **S2-CAL-1** (the library reproduces its own 74 rows, else HALT) is the right first gate. A drifted source would otherwise pass silently.
- **S2-CAL-2** measures the level rule's error before applying it.
- **The verdict classes** (CERTAIN / UNDECIDED / BELOW / UNSOURCEABLE), with counts **reported, not predicted**, are the honest form.
- **"BELOW or UNDECIDED on the J-S8 path = a finding for Matt, not a lever"** is correct: it would falsify the referent's `HIT_CHANCE = 1.0` on a body the referent fights.
- No corpus writes; missing records are routed to elrond/legolas; HALT rather than substitute.

**WARN-S2 · The guard must not land on the default path unless § 3 is all-CERTAIN.**
- § 4 says that if § 3 finds BELOW, UNDECIDED or UNSOURCEABLE bodies, "the golden master would refuse … a finding for Matt".
- If the guard **commit** lands in that state, `JOIN[warlord, GD]` goes RED. That is a golden-master RED, which charter § 6 makes a HALT.
- **Required:** if § 3 is not all-CERTAIN, the guard lands **only behind a non-default profile flag**, or does not land, until Matt rules. The golden master at GD stays 7/7.
- This is a landing rule, not a run rule. **It does not stop the run.**

**INFO-S2a · E_L is calibrated on the wrong population for the hazard it bounds.**
- The 74 are roster-band bodies. The 112 are bosses, nemeses, bounties, summons and line-up bodies, whose **level rules may differ by class** (boss offsets; pets inherit the owner's level, Lap B R-P4).
- E_L measured on the 74 can be 0 even where the 112 carry a systematic level error.
- **The registered classes stand.** Add two **reported** columns per row, before the results are read:
  - the body class, and whether that class is represented among the 74;
  - **the level margin**, `(DA* − DA) / (12·(1 + mod/100))`, i.e. how many levels of error it takes to flip the verdict.
- A CERTAIN on a class absent from the 74 is reported to Matt as "**CERTAIN under L-RULE-B; class uncalibrated**", with its level margin.

**INFO-S2b.** Report the nearest-to-DA\* body per class, alongside P-S2-3's whole-path minimum. A single minimum hides which class carries the risk.

## § 3 · Owed

| Before | Item | Owner |
|---|---|---|
| the J3a build | WARN-P1 (the scalar-row proc law + the corrected prediction), ALONE | gamora |
| any cross-mirror stream claim | INFO-P2's stream test | gamora / drax |
| the J3a controls' reports | INFO-P3 (family-wise rate, σ_mean, one-test note, exact binomial at small N·c) | gamora |
| pack v1 | INFO-P4 (the pin moves in its own rulebook commit) | star-lord / gamora |
| the guard landing | WARN-S2 | gamora / conductor |
| the step-2 report | INFO-S2a/b reported columns | gamora |

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/join1-j3a-crit-model-prereg-2026-10-08.md` (engine `6e412839`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/join1-pj25-step2-da-sourcing-prereg-2026-10-08.md` (engine `756f1098`)
- sealed `kc2/threat.py` :388-405, :1874 · fixture `…/join1-gm-fixture-v1/oracle/G1.jsonl`
- charter `gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.7, line 2; § 6)
- prior: `…/qa/findings/2026-10-08-join1-j3-site-list-review.md` (C-1…C-4, ADJ-J6, INFO-1) · `…/2026-10-08-join1-j3-design-gate1.md` § 7
