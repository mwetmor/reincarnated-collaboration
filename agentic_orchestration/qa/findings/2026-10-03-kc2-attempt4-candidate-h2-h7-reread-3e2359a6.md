# Finding — 2026-10-03 — Run KC2-PLAY · H-2 + H-7 RE-READ at the KP-275 repair candidate `3e2359a6`

**Reviewer:** jack-ryan (DEV-MODE; H-2 and H-7 seat). **The pre-read is a gate document: not a verdict of record, not the attempt, and it consumes nothing.**
**Severity:** **INFO.** H-2 **PASS**. H-7 **28/28 GREEN** ⇒ **FIRE**.
**Target:** runtime tree FILE **`3e2359a6d46c78029f7994a0f600434894dc8916d580b81732c20278257d3057`** (MANIFEST godot `66605a1`; main `c64c192`). Native lib `74360ffa…`, unchanged.
**Supersedes:** my BLOCK at `fd799b63` (collab `ac3342161`, `2026-10-02-kc2-attempt4-candidate-h2-h7.md`) for this candidate.
**Developer:** drax · conductor gandalf · gamora grades the attempt.
**Prereg set of record:** v1.14 `5bbe7ae5…`, v1.15 `d1c4a75a…`, notes `7797ff17…` (all re-hashed equal).
**Principles applied:** REVIEW_PROCESS #1, #4, #5. Disciplines #10, #11, #12. v1.14 § G.1a; KP-185; KP-275.

## Method (the same as the first read)

- **Candidate verified.** I took a `git archive c64c192` into scratch and recomputed the tree independently: **107 members, 0 mismatches, `3e2359a6…`**. The H-3 Gate-2 at this digest belongs to the other session.
- **Emission.** I ran drax's harness `kc2rt_ta.gd` in scratch under the heavy lock, with `run_kind=pre_read`, `expect_runtime=3e2359a6…` and `g3=` the KP-274 summaries (`2026-10-03-g3-25cell-kp274-V311FULL-66605a1`).
  - The boot check passed. H-4 is green. G3 passed on all 25 cells. The runtime digest did not change during the run.
  - `run_kind` is `pre_read` and `verdict` is `null`.
  - **The only emission failure is `runtime_header`, because there is no `.app` in scratch** (see INFO-2 below).
  - The emission is filed at `…-h2-h7/reread-3e2359a6/PRE-READ-NOT-A-GRADED-RUN-emission/`: tree digest `15870c45…`, `ta_manifest.json` `4df67ba8…`, `ta_verdict.json` `d05adce4…`.
- **P-2 control (c).** I ran the committed `kc2rt_attempt2_probes.gd` at this tree. Control (c) REDs as required, and 16 of 16 controls are RED. The probe's only failures are the two `.app` checks, which fail because scratch has no `.app`.
- **Grader.** I used **r3** (`grader_h7-r3.py`, FILE `457587e2…`), committed alone at collab **`3b246e3b2`** before the emission was opened.
  - r3 is r2 with **one change**: `PIN["runtime_tree"]` now holds the new candidate digest.
  - That pin is the candidate's identity, not an expected value. The P-2 control-(c) evidence is keyed to it.
  - Every expected value, tolerance, rule and field read is r2's. The `diff` shows exactly that one line plus the docstring.

## H-2 · (L2) of `TA-X-07(c)` — PASS

- **(L2) holds on 25/25 cells**, evaluated in exact rationals.
  - Worst β = **5.3644e-14** at `W1|4`; margin **×18.64**.
  - Λ max 483.18; f_max ∈ {100, 160, 240}.
  - Clause (a): max ρ̂ = 2.2115e-16.
- **Census.** My independent re-check gives 47 rows, 35 sites, 35 call sites found, T 22 / S 11 / F 14, green.
  - The row content is identical to `fd799b63`'s and `d03ca891`'s once line numbers are stripped. KP-274 relocated lines only.
- **(N1)–(N8).** `_offer`, `_cons_add`, `_neu` and `conservation_residual` are **byte-identical** to `d03ca891`.
- The harness's `r11_bound` agrees with my evaluation on every cell, and the Neumaier probe is bitwise-equal.
- The Cruel fix moves one tick's operands on `M0|1` ≡ `M-POL-2-NULL|1` (INFO-1). The worst cell and the worst β are unchanged.

## H-7 · the 28-row read — 28/28 GREEN

| | read |
|---|---|
| P-1 … P-5 | **GREEN** (P-2 with control (c) at this tree; P-4: packs `99711727…` / `af58ef40…` re-derived from disk) |
| C1 | **CONFORMING** (v1.14 § B.1a ROWSETs; G3 25/25 incl. census, control term, deaths, native shadow) |
| `TA-X-01` … `TA-X-30` (28 EXACT) | **28 GREEN** (`TA-X-19` GREEN-BY-CONSTRUCTION), 0 RED, 0 UNGRADEABLE |
| `TA-X-06` | UNGRADEABLE-declared (W1 vs M-POL-2 identical 2/5) |
| **§ G verdict the emission would take** | **`PASS`** @ 89/89, 28/28 EXACT green, `TA-X-06` declared, epoch v3.11 / `99711727…` / `af58ef40…`, prereg v1.15 (+ v1.14, notes) |

**The rows my BLOCK named, now:**

- **`TA-X-25` is GREEN.**
  - SWING = POOL-466 (`33c886a1…`), NONSWING = ∅ (`e3b0c442…`).
  - All 2,119 record-cells are `measured_offense`; 0 are `measured_inert`.
  - Clauses (a), (b), (c2) and (c4) pass on 25/25. (c3) is satisfied over an empty set.
- **WARN-3 is fixed.** `ta_manifest.json :: ta_x_29_b_c_d["(b)"]` now holds `law = "CompositionFold"`, `holds = true`.
- **`TA-X-29(b′)`, summed by me:**
  - The constants are exact.
  - Every family has n = n_equal: instant_nonphys 66,766 · phys_clamped 2,453 · phys_clamped_unmapped 2,121 · phys_unclamped 21,209 · dot 14,958 · dot_leech_type 162 · dot_chaos_aether 0.
  - Clause (e) reads 3.197066 / 4.935649, with max per-record deviation 0.0.

Every other row prints the same operands as in my first read (`grader_r3_stdout.txt`).

## Face items (notes § 3, plus the KP-275 contact face)

1. **`TA-X-30(b′)`:** vacuous on **25/25** cells — *"(b′) vacuous: no clamp stopped a body"*. W1 had clamp calls on every salt and 0 stops.
2. **Trajectories:** the **port realisation** has 25 cells / **13** distinct trajectories (4 clear, 9 die). The **reference** has 25 / 12 (9 clear, 3 die). The two are not draw-comparable (§ C.7), so the face must label each figure.
3. **UNEXERCISED-ON-REFERENT:** the non-waypoint Pursue operand has 0 port steps, and the non-penetration clip has 0 port steps.
4. **Clip flag:** none (0 clipped steps on 25/25).
5. **`TA-X-08` lethal tick:** exercised on **9 distinct dying port trajectories** (reference: 3). Inapplicable on the clearing cells.
6. **`TA-X-13`:** counted from player rows — 9,035–16,458 per cell, 0 crit (structural, as before).
7. **`TA-X-21`:** all 14 notes § 2 live sites cited, plus the 3 dead ones.
8. **Divisor clause:** UNREACHABLE-IN-PACK. The port composed 0 rows. The `a8` rows taken are the explicit-`True` ones.
9. **Contact solver (KP-275): the face shows the comparisons.**
   - `modes: ["shadow"]`, library `74360ffa…`.
   - **Placements: 10,806 compared, 0 mismatches.**
   - **Blocker scans: 942,161 compared, 0 mismatches.**
   - Contact ticks: *"not reached at this level"*. Under V311-FULL the crowd step is GD `separate`, as declared at KP-272.
   - `zero_mismatches_with_comparisons: true`. Every cell carries `contact_solver: shadow` and the build id.

**§ F.5 rule 13 as it would read:** *"`TA-X-08` identity 2 carries `n_control_suppressed_channelling`. On this run it was 122 (max 12 on one cell); in G3 it was 80 and equal to the oracle's on every cell."*

## INFO

- **INFO-1 · The repair moved two cells' run-determined values, as the Cruel fix should.** That is why no cell digest equals the `fd799b63` read's.
  - On `M0|1` ≡ `M-POL-2-NULL|1`, one tick of 5,378 (tick 201) differs.
    - Leech on that tick: 5366.895 → 5364.701.
    - `offered`: 345,081,494.02 → 345,081,505.64.
    - `hp_trace`, terminal and census are equal. ρ̂ = 0.0 in both runs.
  - The other 23 cells are equal on every behaviour field. They differ only in emitted labels (`nodata`/`board` classes, `contact_solver`, a new c11a field).
  - G3 V311-FULL is 25/25 at `66605a1`, so the moved tick matches the oracle.
  - The attempt should reproduce **this** read, not the first one.
- **INFO-2 · WARN-2 (the `.app`).** I did not run the real `.app`: running it would write into a user-data directory that is not mine, and scratch has no `.app`.
  - The `.app` was rebuilt on 2026-10-03 at 02:06.
  - drax's probe at this tree (`tmp/kc2/kc2rt_attempt2_probes.json`, 02:19) shows 0 failures, which includes both header checks.
  - The attempt's harness will check `runtime_header_vendored_runtime_equals_runtime_digest` itself. **gamora: confirm it is `true` on the graded face.**
- **INFO-3 · Carried from the first read, unchanged:**
  - TA-X-12 and TA-X-13 are structural zeros (§ F.5 cl. 6).
  - TA-X-10's port bound prints at 15 digits.
  - Summon hits sit outside TA-X-07's identity.
  - INFO-4 there: the oracle-only streams are labelled by their construction lines, not their draw lines.

## Ruling

**FIRE.** Attempt 1 of 2 (overall 4) may run **at `3e2359a6d46c78029f7994a0f600434894dc8916d580b81732c20278257d3057`**, with these arguments:
- `run_kind=attempt`
- `expect_runtime=` that digest
- `pre_read_finding=` this file
- `g3=` the KP-274 summaries

This read predicts the graded emission byte for byte (`TA-X-01`). Any per-cell difference goes on the face. **The graded emission governs.**

This read is not a verdict of record. H-5 (hole closure) and H-8 (Matt's T-C replay) remain seal conditions.

## Action

- [ ] **gandalf:** record H-2 PASS and H-7 28/28 → FIRE at `3e2359a6` (once H-3 at this digest is PASS). Budget: 2 of 2 unspent until the attempt runs.
- [ ] **drax:** run the attempt as above, from the real repo with the rebuilt `.app`. File it with the committed tool.
- [ ] **gamora:** grade independently. Reconcile with this read row by row. Print INFO-1's two moved cells, the trajectory labelling (face item 2) and the `.app` header booleans.

## References

- Instruments: `agentic_orchestration/qa/findings/2026-10-02-kc2-attempt4-candidate-h2-h7/grader_h7-r3.py` and `…/reread-3e2359a6/` (`MANIFEST.json` FILE `c8b4fc32…`).
  - Those hold the emission tar, harness stdout, r3 stdout, results JSON, `p2c.json` and the probe stdout.
- G3: godot `evidence/kc2-play/2026-10-03-g3-25cell-kp274-V311FULL-66605a1/`.
- Ledger KP-272 … KP-275. First read: `2026-10-02-kc2-attempt4-candidate-h2-h7.md`.
