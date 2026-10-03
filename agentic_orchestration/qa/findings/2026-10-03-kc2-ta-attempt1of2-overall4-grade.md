# Finding — 2026-10-03 — Run KC2-PLAY · T-A GRADE · "attempt 1 of 2, overall 4" (REFERENT-v1 at v3.11)

**Reviewer:** jack-ryan (grading seat per conductor KP-279).
**Severity:** INFO (verdict PASS; there are no WARN or BLOCK findings).
**Target:** the graded emission at godot `9756c31`, `evidence/kc2-play/2026-10-03-ta-attempt1of2-overall4-v1.15-cells/`.
- `ta_verdict.json` FILE `03f20be4694e01218141086f6e0c94046d3ccfb05fd65be941e39208f5dc3e16`
- `ta_manifest.json` FILE `4ec6fdc35ae39026f291686c1761275d2227c7f4d4693815107d3fe88faa6b87`
- evidence MANIFEST tree `51dc9d6815030ac56917d7ddab90bf58cfda79b40f88b9e6f2faa67333ebf597` (28 members)

**Runtime:** `3e2359a6d46c78029f7994a0f600434894dc8916d580b81732c20278257d3057`. Godot HEAD at the run was `c64c192`, clean.
**Developer:** drax (port + emission) · conductor gandalf
**Prereg set of record:** v1.15 FILE `d1c4a75a…` (restates `TA-X-29(b)` and `TA-X-30`), carrying v1.14 FILE `5bbe7ae5…`, plus the v1.15 notes FILE `7797ff17…`.
**Principles applied:** REVIEW_PROCESS #1, #4, #5. Disciplines #10, #11, #12. v1.14 § G (taxonomy carried from v1.13), § G.1, § G.3, § F.5; v1.15 § G.

---

## ⇒ T-A VERDICT: **`PASS`**

> **`PASS @ coverage 89/89, 28/28 EXACT rows GREEN, TA-X-06 UNGRADEABLE-declared (Q83(b)), substrate_epoch v3.11 / model 99711727… / reference af58ef40…, prereg v1.15 (carrying v1.14 5bbe7ae5…; notes 7797ff17…), runtime 3e2359a6…`**

**Budget.**
- This attempt ran once and consumed **1 of the fresh 2** (KP-194 / KP-227).
- **The budget now reads 1 of 2 remaining** under the re-opened REFERENT-v1.
- A `PASS` does not need it.

**Not quotable yet.**
- The verdict file itself carries `hole_closure: "PENDING (H-5)"`.
- § F.5 cl. 11 says a PASS is not quotable without jack-ryan's hole-closure finding at the same runtime digest (H-5, owed by the other session).
- The seal also needs Matt's T-C replay on this digest (H-8).

---

## 1 · Is this the emission at those digests, and is it the read's?

**Digests match.**
- I extracted the folder from git objects at `9756c31`.
- `ta_verdict.json`, `ta_manifest.json` and the MANIFEST tree all re-hash to the cited values.
- All 28 members verify, and the only file outside the member list is `MANIFEST.json` itself.

**Identity.**

| field | value |
|---|---|
| `run_kind` | `attempt` |
| `attempt` | `"attempt 1 of 2, overall 4"` |
| `attempt_overall` | 4 |
| `verdict` (the harness computes none) | `null` |
| prereg sha | v1.15; set of record = {v1.14, v1.15, notes}, all equal to the pins |
| `runtime_digest` | `3e2359a6…`, unchanged through the run |
| `pre_attempt_read.expected_runtime_digest` | `3e2359a6…` (boot-checked) |
| `pre_attempt_read.finding_sha256` | `76667f56…` = **my re-read file** (`2026-10-03-kc2-attempt4-candidate-h2-h7-reread-3e2359a6.md`, re-hashed) |
| `runtime_header` | read by running the rebuilt `.app` (exit 0); `equals_P4: true`; `vendored_runtime_equals_runtime_digest: true` |
| emission failures | 0 |
| conditions raised to the grader | 0 |
| `godot_head_graded` | `c64c192`; `kc2_runtime` not dirty |

**Reproduction of the § G.1a read.**
- **All 25 `cell.json` files are byte-equal to my `3e2359a6` re-read emission** (collab `531cbfc1d`), and all 25 `cell_digest`s are equal.
- In the verdict file, every graded block is identical: `ta_x_16`, `ta_x_08`, `r11_bound`, `ta_x_30`, `ta_x_29_b`, `ta_x_25`, `terminal` and `face`.
- The verdict-file keys that differ are only the run's identity fields:
  - `run_kind`, `attempt*`, `pre_attempt_read`;
  - `runtime_header*` (the real `.app` versus none in scratch);
  - `godot_head_graded`, `ta_manifest_sha256`;
  - `g3.source_dir` (a path).
- The manifest differs only in `failures`, `runtime_header` and `g3.source_dir`.
- **So the graded-versus-read difference that the face must print is empty.** The record is in `…-grade/reproduction_vs_reread.json`.

## 2 · The grade

**Instrument.**
- I used my committed r3 grader **unchanged**: `grader_h7-r3.py`, FILE `457587e2…`, collab `3b246e3b2`.
- It ran with the P-2 control-(c) evidence from my run of the committed probe at the same runtime tree.
- No change was needed, so nothing new was committed before grading.
- **One read of its output, stated so it isn't mistaken for a red:** its last line, `FIRE (R8) == False`, is the pre-read's fire rule. That rule requires `run_kind == "pre_read"`, and this emission is the attempt. The attempt's grade is the § G verdict line, **`PASS`**.

**The grader's output on the attempt is line-identical to its output on my re-read, except P-4's printed `runtime_header` (now `true` / `true`).** The output is filed in `…-grade/grader_r3_on_attempt_stdout.txt`.

| row | grade | operands (attempt emission) |
|---|---|---|
| **P-1** | GREEN | 89/89 (IMPLEMENTED 65 · DIVERGENCE 8 · RUNTIME-CHOICE 13 · OUT-OF-SCOPE 3) |
| **P-2** | GREEN | § B.3a (1)–(5): fold forked once, 4,706 invocations = 4,706 ticks; own-stream draws measured 0; one digest function; controls (a)/(a0)/(b) not GREEN; control (c) RED at this tree |
| **P-3** | GREEN | POOL-466 (466), WEIGHTED/UNIFORM. This is the incumbent roll's law (v1.14 § L.2). |
| **P-4** | GREEN | 26 P4 blocks verified; packs re-derived from disk (model `99711727…`, reference `af58ef40…`, cross-pin equal); `.app` header true/true |
| **P-5** | GREEN | settings (2)–(11) by value; v3.8–v3.11 folds read off `a8` (H-4 green) |
| **C1** | CONFORMING | five arms' ROWSETs = v1.14 § B.1a; G3 25/25 against `V311-FULL` incl. census, control term (Σ 80 = the oracle's), deaths, native shadow 0; `declared_ungradeable` = `["TA-X-06"]` |
| `TA-X-01` | GREEN | M0 salt 2 run twice: identical, and equal to the graded M0\|2 cell |
| `TA-X-02` | GREEN | 89/89 (v1.14 § L.1: this says the census is mapped, not that v3.11 is covered; G3 is that evidence) |
| `TA-X-03` | GREEN | M-POL-2-NULL ≡ M0, 5/5 |
| `TA-X-04` | GREEN | W1-NULL ≡ M-POL-2, 5/5 |
| `TA-X-05` | GREEN | M-POL-2 ≢ M0, 0/5 identical |
| `TA-X-07` | GREEN | (a) max ρ̂ 2.2115e-16 ≤ 1e-12; (b) reported; (c) **(L2) 25/25** exact; worst β 5.3644e-14 (W1\|4), margin ×18.64; census 47 rows / 35 sites / T22 S11 F14, independently verified |
| `TA-X-08` | GREEN | identity (1), (2) restated, (2p) and the § F.2o convention on 25/25; M0 `n_ticks_released` 0 |
| `TA-X-09` | GREEN | 9/9 replayed; ROWSET `0e826ee0…` |
| `TA-X-10` | GREEN | W1 armed; max body radius 43.0183–43.0707 m ≤ **43.71638147965161** |
| `TA-X-11` | GREEN | (0, 0) clamps on 10/10 W1 and W1-NULL cells ("the port never needed to clamp", § F.5 cl. 6) |
| `TA-X-12` | GREEN | pool damage 0.0 on 25/25 (structural) |
| `TA-X-13` | GREEN | 0 crit rows with `source == player`; 9,035–16,458 player rows per cell (notes § 1 scope; structural) |
| `TA-X-14` | GREEN | release causes ⊆ {type_a, type_b}; 0 energy dry-outs |
| `TA-X-15` | GREEN | (a) p01–p04 at tick 0, p05 at tick 49, on every (wave, point); (b) by construction |
| `TA-X-16` | GREEN | § F.2m′ (a)–(d) at key grain, 25/25; LU-KEYS `[5,5,5,4,4,5,5,5,5,4]` / P06-KEY re-derived from the pack and the line-up: equal |
| `TA-X-17` | GREEN | emitted max ‖spawn − anchor‖ 7.95483 m ≤ 8.0; anchor = the v3.8 GD `emitter_xy` |
| `TA-X-18` | GREEN | lossless emission; bits `c00fffffffffffde` / `be9777a5cf72cec6` |
| `TA-X-19` | GREEN (by construction) | `_defer_arrivals`; the packet carries no position |
| `TA-X-20` | GREEN | r = 3.0: 2.99 HIT · 3.01 MISS · behind HIT · side HIT · 12 → 12 |
| `TA-X-21` | GREEN | 12/12 quantisation rows; all 14 notes-§ 2 live sites cited, plus the 3 dead; 0 bare `round(` over 90 files |
| `TA-X-22` | GREEN | `interrupts_channel_flag` cause 0 |
| `TA-X-24` | GREEN | `PhaseModel.ENGAGE` |
| `TA-X-25` | GREEN | SWING = POOL-466 (`33c886a1…`), NONSWING = ∅ (`e3b0c442…`); clauses (a), (b), (c2), (c4) on 25/25, with all bodies `measured_offense`; (c3) satisfied over an empty set |
| `TA-X-26` | GREEN | (a)–(e); ARMED-464 mean 0.2468965517, median 0.25, max 0.35, min 0, 17 zero; P-i `cb6a008b…` |
| `TA-X-27` | GREEN | (a) 0/0; (b) 16 seeds equal; (c) registry **41** (29 V9 + 12 rg1) and G3 draw rules 25/25; (d) 139 / 97 |
| `TA-X-28` | GREEN | caps 0/0, ALL_BODIES_IN_DISC, 0.57 |
| `TA-X-29` | GREEN | (a) 193/154, 527/104, 344. **(b′) CompositionFold**: constants exact (LO, −0.44, divisor `true`, LAPM 160); every family has n = n_equal (instant_nonphys 66,766 · phys_clamped 2,453 · phys_clamped_unmapped 2,121 · phys_unclamped 21,209 · dot 14,958 · dot_leech_type 162 · dot_chaos_aether 0); PCL rows untouched. (c) z3 10/10. (d) 29 inert, "unexercised: 0 of 29". (e) **3.197066 / 4.935649**, 16 + 23 records, max deviation 0.0 |
| `TA-X-30` | GREEN | (a′) the travel law on 25/25: 814,944 roster steps (55,994 held, all exactly zero; 0 clipped), 666,392 pet steps; 0 halt / position / NaN / reach / operand mismatches. (b′) 0 bodies halted beyond their operand; ring halt 2.4 m with the NaN test |
| *`TA-X-06`* | *UNGRADEABLE-declared* | *printed: W1 vs M-POL-2 identical on 2/5 salts* |

**Counts: 28 GREEN · 0 RED · 0 UNGRADEABLE. Taxonomy (`STRUCTURAL → INDETERMINATE → PASS`): no RED, so not STRUCTURAL; no UNGRADEABLE, no non-GREEN precondition and C1 conforming, so not INDETERMINATE. ⇒ `PASS`.**

## 3 · The report face (§ F.5 rules + notes § 3)

- **Rule 11 (port holes).** The emission's sentence still reads *"A v1.12 PASS is not quotable…"*. That label is carried from v1.12's text, and it should be printed as **"A v1.15 PASS"** (INFO-1). The 17 holes plus the KP-144 / 147 / 150 / 152 defects are invisible to every EXACT row.
- **Rule 13.** *"`TA-X-08` identity 2 carries `n_control_suppressed_channelling`. On this run it was 122 (max 12 on one cell); in G3 it was 80 and equal to the oracle's on every cell."* G3 exercises the control-suppressed branch only; doubly-suppressed and PRE_FIGHT-suppressed ticks are 0 in both.
- **Rule 14, the declared residuals (verbatim from the verdict file).** *"The oracle of record is v3.11 (`V311-FULL`), sealed with five residuals carried to REFERENT-v2: (1) waves last ≈ 2.3× the referent's (oracle mean w151–159 ≈ 39.4 s vs the referent's 17.3 s, KP-226; on the 25 graded cells 37.812 s); (2) the oracle survives w160 more often than the referent did (graded cells: 20/25 clear w160; seat M-POL-2 over 20 salts: 16/20; the referent died in w160 at 25 s); (3) summons are over-produced (≈ 492 monster summons per graded cell) and 3 of the referent's 13 summon identities are absent (Haraxis's Aberrations, Skeletal Archers, Margul's Maggots); (4) the referent's max-HP dip (16,368 = ⌊20,005 × 9/11⌋, w153) is unidentified and not modelled; (5) the six mutators' flat-array level-index law is INFERRED, not decoded. A T-A PASS says port ≡ oracle; it says nothing about these."* Notes § 3.2 reading of (2): *"20/25 cells clear w160 (9 distinct clearing trajectories)"*.
- **Rule 15, cleared terminals.**
  - **Port realisation: 8 cells clear w160 and 17 die** (counted off `terminal`).
    - M0 ≡ M-POL-2-NULL: D w160 · C · C · D w160 · D w160
    - M-POL-2 ≡ W1-NULL: D w160 · D w160 · C · **D w157** · D w160
    - W1: D w160 · C · C · **D w157** · D w160
  - On the clearing cells the § F.2o lethal-tick clause is *inapplicable: no lethal tick (terminal_reason cleared)*.
- **Notes § 3 items:**
  1. `TA-X-30(b′)`: *"(b′) vacuous: no clamp stopped a body"* on **25/25** cells. W1 had clamp calls on every salt and 0 stops.
  2. **Trajectories, labelled.** **Port:** 25 cells / **13** distinct trajectories (4 clear, 9 die). **Reference (oracle):** 25 / 12 (9 clear, 3 die). The port's T-A cells run on its own generator, so they are **not draw-comparable** with the oracle's (§ C.7). Port ≡ oracle on the oracle's draws is G3's 25/25 (deaths equal to the oracle's at the same tick). The emission's harness block prints both strings, each labelled (`port` / `reference`).
  3. **UNEXERCISED-ON-REFERENT:** the non-waypoint Pursue operand class has **0** port steps; the non-penetration clip has **0** port steps.
  4. **Clip flag:** none (0 clipped steps on 25/25 cells).
  5. **`TA-X-08` lethal tick:** exercised on **9 distinct dying port trajectories** (reference: 3); inapplicable on the clearing cells.
  - *(also)* `TA-X-13` is counted from player rows; ps_ rows are out of scope. `TA-X-21` prints the 14-site list. The `TA-X-29(b′)` divisor clause is **UNREACHABLE-IN-PACK**: 0 port rows; the `a8` rows taken are the explicit-`True` ones.
- **§ C.9.8 / contact face.**
  - Native library `74360ffa…`, mode `shadow` on every cell.
  - **Placements: 10,806 compared, 0 mismatches. Blocker scans: 942,161 compared, 0 mismatches.**
  - Contact ticks: *"not reached at this level"* (the crowd step is GD `separate` under `V311-FULL`; KP-272).
  - G3 evidence: godot `evidence/kc2-play/2026-10-03-g3-25cell-kp274-V311FULL-66605a1/`.
- **R-6 invariants:** (i) 0 · (ii) 0 · (iii) 0.

## INFO

- **INFO-1 · Rule 11's label.** The harness reads the holes sentence from v1.12's carried text, so it prints "A v1.12 PASS". The face must print "v1.15" (as at v1.13, H-3 INFO-A). This is a label, not a grade input.
- **INFO-2 · Structural rows, disclosed per § F.5 cl. 6.**
  - `TA-X-11` (the wall never bound).
  - `TA-X-12` (constant 0.0 under ORACLE).
  - `TA-X-13` (the player row's `crit` field is the literal `false`; the port has no player crit roll, as in V0 · CritLimb LO).
  - `TA-X-19` (by source).
  - `TA-X-30(b′)` (vacuous on 25/25 cells).
  - `TA-X-25(c3)` (an empty set).
  - Each is GREEN by its row's law. **None is a measurement of the behaviour it names.**
- **INFO-3 · What this PASS covers.** "Port ≡ v3.11 oracle" on the 28 EXACT rows plus G3. It says nothing about the five declared residuals (oracle ≠ referent) or the holes in rule 11.
- **INFO-4 · Seat.** I authored both the § G.1a read and this grade, from one instrument family. The v1.13 practice had gamora grade independently.
  - The byte-equal reproduction makes the grade mechanical given the read.
  - **The conductor may still want gamora's independent read of the same emission** before the seal, so that the attempt is not graded by its own pre-reader.
  - That is a process note, not a finding against the emission.

## Action

- [ ] **gandalf:** record **T-A `PASS`** for attempt 1 of 2 (overall 4) at `3e2359a6`. The budget reads 1 of 2 remaining. Hold the seal for H-5 (hole closure, other jack-ryan session) and H-8 (Matt's T-C replay). Decide whether to take INFO-4.
- [ ] **drax / gamora (face):** print rule 11 with "v1.15" (INFO-1), and print the trajectory figures labelled as above.
- [ ] **Matt:** H-8 on this digest (seal condition).

## References

- Emission: godot `9756c31`, `evidence/kc2-play/2026-10-03-ta-attempt1of2-overall4-v1.15-cells/` (+ `ta_attempt4_stdout.log`).
- Instruments: `agentic_orchestration/qa/findings/2026-10-03-kc2-ta-attempt1of2-overall4-grade/`:
  - `grader_r3_on_attempt_stdout.txt`
  - `grade_results_r3.json.gz`
  - `reproduction_vs_reread.json`
- Grader: `…/2026-10-02-kc2-attempt4-candidate-h2-h7/grader_h7-r3.py` (FILE `457587e2…`, collab `3b246e3b2`). Control-(c) evidence: `…/reread-3e2359a6/p2c.json`.
- The § G.1a read: `2026-10-03-kc2-attempt4-candidate-h2-h7-reread-3e2359a6.md` (FILE `76667f56…`). First read: `2026-10-02-kc2-attempt4-candidate-h2-h7.md`.
- Prereg v1.14 § 0.2, § C.9, § F.5, § G, § G.1, § G.3; v1.15 § F.2h′, § F.2i′, § G; notes §§ 1–5; v1.12 § F.2k.
