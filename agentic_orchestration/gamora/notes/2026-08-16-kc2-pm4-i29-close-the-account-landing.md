# KC2-PM4 · I-29 — **CLOSE THE ACCOUNT** · SEAM LANDING NOTE

**Iteration:** I-29 (RUN KC2-PM4)
**Commission:** R-PM4-76 part 3
**Date:** 2026-08-16
**Author:** gamora (simulation seam)
**Conductor:** gandalf (RUN-CONDUCTOR)
**Status:** LANDED — verdict banked, conductor verification complete (CL-10), charter rows L-67 / R-PM4-77

---

## ⚑ PROVENANCE BANNER — **AUTHORED POST-HOC FROM COMMITTED ARTIFACTS**

This note was **not** written by the session that executed I-29. It is authored after the fact, from artifacts already committed to `~/Games/reincarnated-engine`, and it re-derives **nothing**.

What happened:

1. The **executing** session ran I-29 to completion and **committed every engine work-product** — math note, both defect addenda, instrument, findings — before it died to a stream timeout.
2. Two **subsequent** sessions were opened to write this seam-convention landing note. **Both died to stream timeouts** as well, each having spent its budget re-verifying work the conductor had already verified (re-hashing the findings, re-reading the instrument, re-walking the decomposition).
3. This third session is deliberately **lean**: it reads the committed artifacts only as far as needed to point at them, quotes the conductor-verified digest rather than recomputing it, and runs **no instrument**.

Consequence for the reader: **the engine record is authoritative, this note is a pointer.** Where this note and the committed artifacts disagree, the artifacts win. Nothing here is new evidence; every number below is transcribed from artifacts the conductor has already checked.

The absence of this note was banked as a **seam debt**. This note repays it (R-PM4-77 part 4).

---

## 1 — VERDICT

**F-I29 HOLDS.** `BELOW ×10/10`, `failing=[]`.

The pre-registered criterion had **three limbs**, all of which had to hold:

| Limb | Requirement | Result |
|---|---|---|
| **BELOW** | ρ below the ×10 band at the **sim-favourable** end of the band | held, 10/10 arms |
| **Closure** | identity closure residual ≤ `1e-9` | achieved ≤ `2.2e-16` (machine-epsilon class) |
| **Q-DOMINANT** | `s_Q > 0.5` — the Q-leg must carry the majority of log-magnitude | held on every row |

No arm failed. `failing=[]` is the literal empty set, not a rounding of "near-zero".

---

## 2 — THE DECOMPOSITION HEADLINE

The account closes on the identity

```
ρ = L_ref / L_sim = Q_leg × N_leg × T_leg
```

Three things are worth carrying forward, and only three:

- **The N-leg is exactly unity by construction.** That is a *property of the construction*, not a finding. It does not get to be cited as evidence of agreement.
- **The Q-leg carries ~85% of log-magnitude on every row.** `s_Q` ranges **0.720 – 0.893**, median **0.8478**. The discrepancy is overwhelmingly a Q-side quantity, on every arm, without exception.
- **The T-leg is NOT one-signed.** Range **0.384 – 1.863**; **6 rows > 1, 4 rows < 1**. The time leg does not push consistently in either direction, so it cannot be characterised as a bias — it is dispersion. This is the single most consequential structural statement I-29 produced, and it is the reason the account can be *closed* rather than *corrected*.

---

## 3 — RECORD POPULATION AND COVERAGE

- **10 pairs** graded: **7 COMPLETE + 3 DEATH-TRUNCATED**.
- **6 arms outside the criterion** were **published beside** the graded set — visible, not folded in, not silently dropped.
- **54 UNREACHED rows** carried forward from I-28, still unreached. Carried, not swallowed.

The window-completeness partition was named in the math note **before** grading, so the death-truncated rows were classified by a rule written in advance rather than by a rule chosen after seeing them.

---

## 4 — GATE_S AND THE AGGREGATE

- **`GATE_S` EXACT ×7.**
- Aggregate, ω-weighted: **3.352406** against pinned **3.3519** → **rel_dev +1.51e-4**, ruled **functional** (agreement at the level the aggregation rule can support).
- The deflated comparator sits at **−6.0e-2** — three orders of magnitude away, which is what makes the +1.51e-4 ruling meaningful rather than an artefact of a loose tolerance.

---

## 5 — PREDICTIONS

**9 PASS / 1 FAIL / 0 UNREACHED**, graded **wording-unchanged** from pre-registration.

The single **FAIL is informative, not embarrassing**: **P-3**, on `salt1 w155`, `D = 0.8012 < 1` — one COMPLETE pair runs **short**. The prediction asserted no COMPLETE pair would; one does. That is a real, small, located counter-example, and it is better banked as a FAIL than rescued by re-wording.

---

## 6 — DEFECTS: TWO, BOTH SELF-CAUGHT, BOTH FAILED CLOSED

Both defects were caught by my own guards **before any claim was published**, and in both cases the iteration **HALTed itself** and committed the addendum **ALONE, before the repair**, so the defect record cannot be read as retro-fitted around a fix.

**D-I29-1 — numeric identity decided by string manipulation.**
An equality between numeric quantities was being decided through a `rstrip("0")` on the string rendering. That is a rung guard: the comparison was operating one representational rung below where it belonged. Caught by the guard, HALT, addendum `14990a82` committed **alone**, then repaired.

**D-I29-2 — `1e-9` tolerance applied against a 6-dp presentation field.**
A machine-precision tolerance was being tested against a field carrying only six decimal places of presentation precision — a tolerance the field is structurally incapable of satisfying. Surfaced at **1.22e-5**. HALT, addendum `9729b807` committed **alone**, then repaired. **The repair reads the full-float ⚑ SIM block** rather than the presentation field.

Disposition on both: **guards failed CLOSED; nothing downstream was contaminated.** The published verdict rests on the post-repair pass, and the pre-repair state is on the record in its own commit.

---

## 7 — POINTER BLOCK (the controlling record)

**Engine commits** — `~/Games/reincarnated-engine`, all four pushed:

| Commit | What it is |
|---|---|
| `130e137c` | I-29 math note / pre-registration — CLOSE THE ACCOUNT. Committed **ALONE, ZERO CODE, ZERO GRADES** (math-before-code, Discipline #1). |
| `14990a82` | Addendum #1 — **D-I29-1**, committed **ALONE, BEFORE ITS REPAIR**. |
| `9729b807` | Addendum #2 — **D-I29-2**, committed **ALONE, BEFORE ITS REPAIR**. |
| `d0297ace` | Instrument + findings — F-I29 HOLDS; the Q-leg carries ~85% and the T-leg is not one-signed. |

**Math note:**
`~/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i29-close-the-account-2026-08-16.md`

**Findings:**
`~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-pm4-i29-findings-20260816_124601.json` (112,429 bytes)

**sha256** — *conductor-verified digest, quoted not re-hashed*:

```
8c493c4c5565e084c76a698c4094f4257780c4987ebaf7bb38c2ceec422ca9ac
```

Quoting rather than recomputing is deliberate: the truncated-pin law (run **DO-NOT 8**) is honoured here **by declaration**. The digest above is the conductor's, transcribed in full and unabbreviated; this session did not run a hash and does not claim to have independently confirmed it.

**Charter rows — the controlling record:** **L-67** and **R-PM4-77**. Where this note is thinner than the charter, the charter governs.

---

## 8 — LAW 3

**No tuning.** No simulation parameter moved in I-29. The frozen **E-s09-cp150** state was **untouched** — read from, never written to. I-29 measures and closes an account; it does not adjust the thing it measures. Any future change to a modifier formula, threshold, or convergence criterion arising from these findings is a **separate** iteration with its own math note, per Discipline #1.
