# Finding — 2026-10-01 — Run KC2-PLAY · H-6: PRE-READ OF PREREG v1.13

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **PASS-WITH-WARN. 0 BLOCK · 2 WARN · 7 INFO. No ESCALATE.** Both restatements implement Matt's Q96.1 and Q96.4 rulings exactly, with nothing added or dropped. **Under KP-178 law (a), the oracle passes every EXACT row of v1.13.** I re-measured this with my own code and my own oracle re-run, not only with gamora's script. Both WARNs are in § G.1a, the pre-attempt read. Neither makes the read able to fit a value. Both can be discharged without a v1.14: WARN-1 by how the H-7 read classifies a RED, and WARN-2 by an H-4 harness boot check.
**Target:** prereg v1.13, FILE `c35cca9ceb189b5f78a09b402f9df81b3bb126db132643a57049eb1cc8a46d68` (collab `066439a84`, re-derived). Instruments: collab `e904af653`, `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-prereg-v1.13-DRAFT/`. Its only predecessor is v1.12, FILE `a0454776…` (re-derived). Runtime pinned in § PINS.2: godot `05508a0`, tree `c9a7299e…`.
**Developer:** gamora (v1.13, instruments) · drax (counters, G3 at `c9a7299e`) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code), #4 (committed text and oracle source are the truth), #5 (severity matters). Disciplines #10 (attribution), #11 (empirical inspection over assumption), #12 (semantic restatement named). ADR-002. Charter KP-177 to KP-184. **KP-178 law (a) and law (b) bind this gate.**

**Read-only attestation:**
- I read godot only through git objects (`git show`, `git diff`, `git log`) and through `git archive 05508a0 kc2_runtime` into my scratchpad. drax's working tree was not touched.
- The engine was read and executed at `22cd2288`, with no tracked modification under `simulation/kc2`, `export` or `simulation/scripts`. The repo-wide porcelain count was 633 before and after my runs, so I changed nothing.
- Every oracle run held the heavy lock (`~/astra-burst/.heavy.lock`, flock) and wrote only to scratch.
- gamora's three scripts ran from a scratchpad copy of her folder, so nothing was written beside the originals.
- **No pre-read emission exists yet.** Godot has no PRE-READ evidence folder; HEAD is `05508a0`. I read no candidate (port-generator) cell at this gate.
- This file is the only thing I wrote to any repo.

---

## Per-item verdicts

| # | item | verdict |
|---|---|---|
| 1a | § F.2m: `TA-X-16` restated per played wave (Q96.1) | **PASS.** Faithful to *"Per played wave"* and KP-183's expansion, nothing more or less. Clause (d) is v1.12's third clause carried at the ruled grain, not a new clause. The oracle passes 25/25 on three independent instruments |
| 1b | § F.2n: `TA-X-08` identity 2 with the control term (Q96.4) | **PASS.** The term, `n_released` on D, and doubly-suppressed counted as released are all as ruled. (2p) was presented to Matt inside sub-choice 1 (draft § L item 4: *"`n_released` on **D** (with (2p) closing it)"*), so it is within the ruling. The oracle passes 25/25 (INFO-1) |
| 1c | `check_v1p13_draft.py` re-run | **CONFIRMED.** Exit 0. `results.json` and stdout are byte-identical to the committed files (`1f7e3c8a…`, `a255888d…`) |
| 1d | **KP-178 law (a): does the oracle pass every EXACT row of v1.13?** | **YES, every row** (table below). I re-audited it myself: an oracle re-run with my own evaluator, plus my ea0317306 audit for rows whose text did not change |
| 2 | § G.1a: the 28-row pre-attempt read (Q96.3) | **PASS-WITH-WARN.** The freeze precedes the read (verified). The HALT on any row change is stated twice. The rule for a graded emission that differs from the read is stated. **⚠ WARN-1:** the RED branch assumes a port defect, which is the one channel through which the read could fit. **⚠ WARN-2:** the same-digest rule has no stated enforcement and no stated consequence. INFO-2, INFO-3 |
| 3 | § G.1: the budget | **PASS.** 1 of 2 remains. The next run is v1.13 attempt 2 of 2 (overall 3), the last under the cap. Q85's four guards hold. INFO-4 |
| 4 | § C.9.5a (G3 control-term equality) and report-face rule 13 | **PASS** (INFO-5, INFO-6). G3 Σ of the term = **52** over 25 cells |
| 5 | The rest of the v1.12 → v1.13 delta, PINS, § PINS.2 re-pin, census convention | **PASS.** 115/115 pins reproduce under my re-run. I recomputed § PINS.2 independently, and the `fill_draft.py` re-fill reproduces v1.13 byte-identically. INFO-7 |
| 6 | KP-178 law (b) | Every row whose reading state changed was re-opened. **No defect** (table below) |

---

## Item 1 · The two restatements against Matt's rulings, and on the oracle

### 1a · § F.2m (`TA-X-16`)

**Fidelity to the ruling.** Matt's verbatim ruling is *"Per played wave"* (KP-183). The conductor's expansion: on every played wave, picks equal `[5,5,5,4,4,5,5,5,5,4]` at key grain, no p06 key is rolled, and filtered keys equal `[0,1,1,0,1,1,1,1,0,1]`. Each part maps to one clause:
- (a) picks equal the vector, per wave;
- (b) `n_pool_picks` is the sum of (a), so it adds no constraint beyond (a);
- (c) no p06 key, per cell and per wave;
- (d) the filtered-key counter, per wave.

v1.12's row had exactly three clauses: picks, `n_spawn_point_6_keys_rolled`, and *"a filtered-keys counter"*. v1.13 keeps all three at the ruled per-wave grain. **Nothing was added or dropped.** The 47 survives exactly where its premise holds, on a cell that clears w160.

**The vector, re-derived by my own code.** From `model/waves.json` alone: `[5,5,5,4,4,5,5,5,5,4]` (Σ 47); with p06 the sum is 54; `P06-KEY` is `[0,1,1,0,1,1,1,1,0,1]` (Σ 7). It equals the oracle's own `wave_engine.pools_for(w, False/True)` key sets for all ten waves. **No port number enters.**

**The oracle passes 25/25 on three independent instruments.** All three agree on every wave played of every cell:
1. my own hook re-run's `roll_wave → pools_for` keys;
2. the distinct spawn points of the actors in the trace;
3. drax's KP-180 oracle-side `_weighted_pick` hook (`ta_x_16` in the `05508a0` traces).

`bonus_spawns_enabled` was False on every roll. The old text (`== 47`) fails 0/25, as KP-177 found. Clause (a) is exercised on 1 to 6 waves per cell. **No reference cell exercises w157–w160** (disclosed in § F.2m.4). Those four entries rest on `pools_for`, which I verified for all ten waves.

### 1b · § F.2n (`TA-X-08`)

**Fidelity to the ruling.** Matt ruled Q96.4 *"Add control term"*, with `n_released` on D and a doubly-suppressed tick counted as released (KP-182). The restated identity (2) is exactly that, and its population is stated in § F.2n.3. Both choices come from the oracle's code:
- `tick_apply` decides and counts the verdict on every tick, control or not (`channel_policy.py:297-339`);
- `observe(already_suppressed=True)` only skips reading it (`:386-388`);
- so "the fold's verdict on a control-suppressed tick" is well defined. The hook reads it as `self._verdict`, which `tick_apply` set earlier in the same tick.

(2p) is gamora's population closure. It was put to Matt as part of the `n_released` sub-choice and accepted with it.

**The oracle passes 25/25, measured by me.** My hook re-run of the unchanged G3 oracle tool (godot `b4c1ff3`, FILE `51f46965…`) gave:
- traces byte-identical to the KP-177 MANIFEST, 25/25;
- hook records equal to gamora's, 25/25.

My own evaluator (scratch, not gamora's code) found:
- identity 1: 25/25;
- identity 2 as written: 6/25;
- **identity 2 restated: 25/25**;
- (2p) on the fold arms: 20/20, with `n_apply = n_observe = observed` and `n_desync = 0`. M0 has no fold, so the port must emit 0 = 0 + 0;
- the restated term equals the trace's control `channel` entries, 25/25. That is an independent instrument; on M0 it is the only one;
- every non-channelling D tick in the trace equals `n_released` + the term, 25/25;
- the tick law `chan = ¬cc ∧ ¬verdict` holds on every observed tick;
- doubly-suppressed ticks = 0, released PRE_FIGHT ticks = 0, control-suppressed PRE_FIGHT ticks = 0.

**So the reference cannot discriminate either sub-choice.** v1.13 discloses this (§ F.2n.3).

### 1d · KP-178 law (a), row by row: **the oracle passes every EXACT row of v1.13**

Reference: the oracle's five arms × five salts, leg A, at engine `22cd2288`. These are 12 distinct realisations, confirmed by me. **M** = I measured it this session with my own code. **C** = carried from my ea0317306 audit. A C row's text is unchanged since v1.12, and its traces are byte-identical to the ones I audited there.

| row | v1.13 text | oracle | basis |
|---|---|---|---|
| `TA-X-01` | carried; digest law printed | **PASS** | M: the re-run is byte-identical, 25/25 |
| `TA-X-02` | carried | **PASS** (structural) | C |
| `TA-X-03` | carried; zero-draw = absent | **PASS** 5/5 | M: full trace equal (streams record draws only, so zero-draw = absent is the trace's own convention) |
| `TA-X-04` | carried; zero-draw = absent | **PASS** 5/5 | M: full trace equal |
| `TA-X-05` | carried; same digest function | **PASS** (differs on 5/5 salts) | M: terminal waves differ on every salt |
| `TA-X-07` | carried | **PASS** (structural; (c) reference ≤ 1,168 ticks) | C |
| **`TA-X-08`** | **identity 2 restated; (2p); census convention** | **PASS 25/25** | M (Item 1b) |
| `TA-X-09` | carried | **PASS** (no run) | C; ROWSET reproduces |
| `TA-X-10` | carried | **PASS** (43.405 / 43.588 ≤ 43.758 m) | C; equal to gamora's measurement |
| `TA-X-11` | carried | **PASS** | C (H-9 pins reproduce) |
| `TA-X-12` | carried | **PASS** | C; equal to gamora's measurement |
| `TA-X-13` | carried | **PASS** (structural) | C |
| `TA-X-14` | carried | **PASS** (structural) | C |
| `TA-X-15` | carried | **PASS** ((a) tick 49, 25/25; (b) by construction) | C; equal to gamora's measurement |
| **`TA-X-16`** | **restated per played wave** | **PASS 25/25** | M (Item 1a) |
| `TA-X-17` | carried | **PASS** (7.9565 ≤ 8.0 m) | C; equal to gamora's measurement |
| `TA-X-18` | carried | **PASS** | C; bits reproduce (PINS) |
| `TA-X-19` | carried | **PASS-vacuous** | C |
| `TA-X-20` | carried | **PASS** (structural) | C |
| `TA-X-21` | carried | **PASS** | C (1561/1681/1714/2052, half-to-even) |
| `TA-X-22` | carried | **PASS** (structural) | C |
| `TA-X-24` | carried | **PASS** (structural) | C |
| `TA-X-25` | carried | **PASS** (structural; set digests reproduce) | C |
| `TA-X-26` | carried | **PASS** (no run) | C |
| `TA-X-27` | carried | **PASS** | C |
| `TA-X-28` | carried | **PASS** (structural) | C |
| `TA-X-29` | carried | **PASS** ((e) 643/643) | C |
| `TA-X-30` | carried | **PASS** (structural) | C |

`TA-X-06` is UNGRADEABLE-declared and `TA-X-23` is struck; neither is EXACT. **Result: 28/28.** The two rows that failed under v1.12 (`TA-X-16` 0/25; `TA-X-08` identity 2, 6/25) are the two that v1.13 restates. Both now pass.

---

## Item 2 · § G.1a: the pre-attempt read

**Each question in the brief:**
- **Is the freeze guaranteed before the read? YES.** v1.13 was committed alone at `066439a84` (14:52) and is immutable. Every expected value, tolerance, population, grain and antecedent the read applies is in it or carried into it. I verified that no pre-read emission exists.
- **Is the same digest enforced for the read and the attempt? STATED, NOT MECHANISED.** The text requires it in four places: § G.1a step 4 (*"tree FILE equal, checked at boot"*), step 5, § G.1's L2, and § G.3's `pre_attempt_read.runtime_digest`. It does not say who checks at boot, or what an attempt at a different digest is (WARN-2).
- **What if the graded emission differs from the read? STATED.** The graded emission governs, and any difference is printed on the report face. That is the correct rule: anything else would be grading the read (INFO-2).
- **Is the HALT on a post-read row change stated? YES, twice:** in the banner (*"ANY CHANGE AFTER A GRADED RUN OR THE § G.1a READ EXISTS AGAINST IT IS A HALT TO MATT (`WARN-16`)"*) and in § G.1a (*"a new dated version, never an edit"*).
- **Can the read be used to fit anything?** **Not a value.** No expected value, tolerance, grain or population can move, and I verified the freeze. Three channels remain, and the read sharpens each:
  1. **fitting the port to a defective row.** This is WARN-1.
  2. **a cell-keyed port repair.** The read shows the exact graded realisation, and a repair that branches on arm, salt, wave or tick could make those 25 cells green without implementing the law. My H-3 delta Gate-2 will **BLOCK** any such branch. Every post-read repair must cite the oracle line it conforms to and re-pass G3 25/25.
  3. **a post-read restatement.** This is guarded by the `WARN-16` HALT and by the § 0 legend: a RESTATED row is *"derived from the oracle's law and checked on the oracle's reference realisations"*.

  **With WARN-1 applied, the read cannot fit anything.**

### ⚠ WARN-1 · The RED branch assumes the defect is in the port

§ G.1a step 4: *"Any RED or UNGRADEABLE: … The port is repaired."* That is right for a port defect. It is wrong for the case attempt 1 actually hit: **a row that a faithful port fails on its own realisation.** "Repairing" the port there means making it unfaithful to satisfy the row. That is the `TA-X-16` shape (*"the row rewards infidelity"*), and it would be the read's one fitting channel.

Law (a) now passes every EXACT row on the reference. So a RED can only be one of two things:
- **(i) a port defect;**
- **(ii) a row that is ill-posed on a state the port's own realisation reaches and the reference never does.**

Case (ii) is concrete. The states the reference never reaches are:
- w157–w160. v1.12 § F.3a: port M-POL-2 salt 1 clears w160;
- a cleared cell (no lethal tick; PF = 10);
- a released PRE_FIGHT tick;
- a doubly-suppressed tick.

**Remedy, needing no v1.14:**
- My H-7 read classifies every RED or UNGRADEABLE as (i) or (ii), with the oracle-source argument for that one row.
- (i) goes to port repair. (ii) is a HALT to Matt and never a port repair.
- The conductor routes on that classification.

### ⚠ WARN-2 · Same-digest enforcement and its consequence are unstated

*"Checked at boot"* has no actor. The harness's `runtime_digest_boot` is its own digest, and nothing compares it with the read's digest. § G.3's `pre_attempt_read.runtime_digest` is an *equal to* assertion with no stated consequence for a mismatch. An attempt fired at another digest would have run with an L2 precondition unmet. Whether that attempt is consumed is then a question for Matt that need never arise.

**Remedy, needing no v1.14:**
- As part of H-4, the harness takes the read's digest as an input and **fails closed at boot** (before any cell runs) when its tree FILE differs. A mismatched attempt then cannot start, so nothing is spent.
- The harness writes `pre_attempt_read` from that input.
- I will check this at H-3.

---

## Item 3 · § G.1: the budget. PASS

- The allowance is v1.12's two (Matt KP-115). v1.12 attempt 1 is spent (STRUCTURAL, upheld at 347ce2e1e).
- v1.7 attempt 1 stays on the record, spent.
- Matt Q96.2 is *"Keep 1 remaining."*
- *"v1.13 attempt 2 of 2 (overall attempt 3)"* counts the allowance, not the version. This is consistent with § G.3's `attempt` field.
- A STRUCTURAL attempt 2 exhausts the cap, and what follows is Matt's. An INDETERMINATE result consumes nothing.
- Q85's four guards are restated and hold.

---

## Item 4 · § C.9.5a and report-face rule 13. PASS

- **The census equality** was already measured at `e584477b` (KP-179). drax's KP-180 G3 at `c9a7299e` gives census equal 25/25 (MANIFEST `4347e87d…`, re-derived by me).
- **The control-term equality.** drax's G3 compares `n_control_suppressed_channelling` (port) with the oracle trace's control `channel` entries: equal 25/25, **Σ 52**. G3 also compares every fine `TA-X-08` counter, the fold-derived oracle term included: equal 25/25. INFO-5.
- **Why the equality belongs in G3 and not in a row is sound.** On the port's own generator the term can be 0 everywhere, as it was in the 15 cells I read at ea0317306 (disclosed there). G3, on the oracle's draws, is the only place the term is exercised. It is named as a precondition, not a graded row (Discipline #12).
- **Rule 13** is mandatory and conditional, so it reads correctly whether or not the term is 0 on the attempt. INFO-6.

---

## Item 5 · The rest of the delta. PASS

- **PINS.** `pins_v1p13.py` re-run from scratch: exit 0, **115/115 carried pins reproduce**, 10 new. Stdout is byte-identical to `pins_stdout.txt`. `pins_v1p13.json` is identical except for one field: the hook's absolute path, which is my scratch path.
- **§ PINS.2, recomputed by my own code** (the make_manifest law: sorted `relpath  sha256` lines over `.gd/.sh/.py/.md`, `MANIFEST.json` excluded) on `git archive 05508a0`:
  - tree **`c9a7299e…`**, 85 members, member set and digests equal to the committed MANIFEST;
  - all 11 file pins equal;
  - KP-180 MANIFEST **`4347e87d…`**;
  - `kc2_runtime/` has no diff between `4fd523f` and `05508a0`.
- **v1.12 FILE `a0454776…` and v1.13 FILE `c35cca9c…`** re-derived.
- **`fill_draft.py`** applied to a copy of v1.13 with the committed JSONs reproduces **`c35cca9c…` byte for byte**, so no filled block was hand-edited.
- **§ F.2o (census convention).** Measured by my evaluator, 25/25:
  - one PRE_FIGHT per wave played;
  - no DEAD;
  - the lethal tick censused alive;
  - D equal to G3's `D_oracle`.

  This is the convention I required at 347ce2e1e WARN-1 and passed at ea0317306.
- **§ B.3a (P-2 reading and the digest law)** carries my ea0317306 INFO-2 (optional control (d), non-gating) and INFO-3 (fork order kept but inert; the digest law printed for `TA-X-01/03…05`) faithfully. *"Can only add equalities"* is correctly qualified for `TA-X-05`, whose one-sided inequality is on the same function. On the oracle it differs 5/5.
- **H-1.** The stale note at `kc2rt_roster.gd:1942` is gone at `05508a0` (grep). The counter names match § F.2m.5 and § F.2n.6.

---

## KP-178 law (b): rows whose reading state changed from v1.12 to v1.13, re-opened

| change | rows that read it | re-opened against | result |
|---|---|---|---|
| runtime `e584477b` → `c9a7299e` (emission counters only) | all graded rows | G3 25/25, deaths equal, (L2) operands byte-identical (drax KP-182) | **PASS** at `c9a7299e`. H-2 re-confirms at the attempt-2 digest |
| `TA-X-08` now reads control suppression | `TA-X-14`, `TA-X-22` (release **causes**); `TA-X-27(c)` (draw consumption); `TA-X-07` (packets) | `run.py:2810-2815`; `channel_policy.py:297-392` | **unaffected**. None counts channel ticks |
| `TA-X-16` now reads the terminal wave and the waves played | `TA-X-15(a)`, `TA-X-25(b)(c)` | re-opened at ea0317306 Item 8 | **PASS**. They read the schedule and membership, which do not truncate |
| digest law: zero-draw = absent | `TA-X-01`, `03`, `04`, `05`, P-2 | oracle full-trace relations (Item 1d) | **PASS** |
| census convention made operational | `TA-X-08`; `TA-B-02…09` (diagnostic) | `actor_state.py:252-261`; G3 census | **PASS** |
| per-wave grading reaches w157–160 on the port only | `TA-X-16` (a)/(d) | `pools_for` for all ten waves | **PASS** by derivation. No reference fight; WARN-1 case (ii) |

---

## INFO

- **INFO-1 · (2p) is nearly an identity by construction in the port at `05508a0`.** `kc2rt_fight.gd:1729-1733` increments `n_ticks_released` whenever `n_released` changed this tick. `_census` (`:5878-5881`) then moves that increment to `n_released_pre_fight` on a wave-first tick. The comment says it is *"a check between two counting sites, not an identity by construction"*, but both counts come from one increment. It cannot detect a PRE_FIGHT population error: if the port failed to rewind, (2p) would still close. **Identity (2) would catch that error instead**, so nothing is lost. I will check it at H-3: either count `n_ticks_released` at the fold's own verdict, or correct the comment. Not gating.
- **INFO-2 · Define the domain of the read-vs-attempt comparison.** "Byte for byte" will trip on label and path fields (the evidence folder, `pre_attempt_read`, `attempt`). Compare per-cell `cell_digest` and every graded row value. A non-empty difference at the same digest is direct evidence of non-determinism on more than `TA-X-01`'s one named cell. It cannot enter the verdict (rows are frozen), so print it prominently and treat it as a seal question for Matt.
- **INFO-3 · Seat independence for the read.** I read (H-7), and gamora grades the attempt. Both graders must agree row for row on a deterministic emission; gamora's grade should print any disagreement with the read. **I will author and FILE-pin my 28-row grader from v1.13's text before the PRE-READ emission lands**, so the emission cannot shape the grader.
- **INFO-4 · "Every item of § H" in § G.1's L2 includes H-5 and H-8.** By their own text those are seal conditions, and H-8 cannot precede the attempt because it rules on the graded digest. Precedent: v1.12 attempt 1 fired with `hole_closure` PENDING (H-5). Read L2 as H-1 to H-4, H-6 and H-7 (H-2 included). The launch sheet should say so.
- **INFO-5 · The operand named in § C.9.5a is the coarse one.** It counts control `channel` entries, which include doubly-suppressed and PRE_FIGHT ticks; the defined term excludes them. On G3's 25 realisations, which the oracle and pack fix, those are 0, so the two are equal and stay equal while the oracle does not move. drax's G3 also compares the fine counters (25/25).
- **INFO-6 · Rule 13's "G3 has [tested the control path]" covers one branch.** It is the control-suppressed-channelling branch (52 ticks). G3 exercises neither the doubly-suppressed booking nor the PRE_FIGHT branch. Print § F.2n.3's disclosure beside the rule-13 sentence.
- **INFO-7 · A carried imprecision in report-face cl. 7.** The sustain sentence reads *"KILLS THE PLAYER AT WAVES 152–156"*. That is true for the M-POL-2 arm of record, but M0 and M-POL-2-NULL salt 1 die at w151 (§ F.2m.4). It predates v1.13 and is mandatory text; a report face may add "(M-POL-2)" beside it.

---

## Ready for my next gates (noted per the brief)

- **H-3 (delta Gate-2 on drax's candidate digest).** The diff from `c9a7299e` must be harness-only (label, `prereg_sha256`, § G.3 blocks); `sim/` byte-unchanged, or G3 re-run. Also check:
  - **WARN-2's fail-closed boot check**, and `pre_attempt_read` written from the input;
  - G3 25/25 at the new digest, including § C.9.5a: control term Σ 52, census equal;
  - INFO-1;
  - `waves_played` equal to `[151 … terminal_wave]` on every cell (the board's `per_wave` keys must not run past T);
  - `n_ticks_released` = 0 on M0;
  - every counter counted at its source. `n_control_suppressed_channelling` is already verified at source (`:5870-5877`, control flag ∧ fold verdict);
  - **any arm-, salt-, wave- or tick-keyed branch is a BLOCK.**
- **H-2 ((L2) unchanged).** At the attempt-2 digest the `l2_operands_25cell.jsonl` operands must be byte-identical to KP-177's (`b5bcdb7b…`). Otherwise re-evaluate all 25.
- **H-7 (the 28-row read).**
  - My grader is FILE-pinned before the emission exists (INFO-3).
  - Antecedents P-1 to P-5, `TA-X-07(c)` (L2) and `TA-X-18` lossless; **C1** (arm `a8` ROWSETs, `declared_ungradeable` exactly `["TA-X-06"]`, G3 at the digest).
  - The read MANIFEST pins both `ta_manifest.json` and `ta_verdict.json`.
  - Every RED or UNGRADEABLE is classified (i) or (ii) under WARN-1, with the reference-unreached states checked first.
  - The rule-13 sentence with this emission's Σ and G3's 52.
  - The § G verdict the emission would take.

---

## Verdict

**v1.13: PASS-WITH-WARN** (0 BLOCK · 2 WARN · 7 INFO).
- Both restatements are faithful to Q96.1 and Q96.4, nothing more or less.
- **The oracle passes every EXACT row (law (a), 28/28).**
- Pins and re-pins reproduce.
- § G.1a is well defined on the freeze, the HALT and the divergence rule.

Discharge WARN-1 through how H-7 classifies a RED and WARN-2 through H-4/H-3. **Attempt 2 conditions are unchanged from § H:** H-4 → H-3 → H-2 → H-7 (28/28 GREEN at one digest) → fire at that digest.

## Rationale

- Matt Q96.1 to Q96.4, verbatim in KP-182 and KP-183, and the Q96 text in `canonical/matt_decision_needed/README.md`.
- KP-178 law (a)/(b).
- v1.12 § F.2, § G, § H; v1.1 § C.1.
- Oracle: `channel_policy.py:297-392`, `run.py:2810-2815`, `wave_engine.py:305-307`, `actor_state.py:252-261`.
- REVIEW_PROCESS #4 (re-measured on the oracle, not taken from the script) and #5 (WARN, not BLOCK: neither defect lets a value move, and both close operationally).
- Discipline #11. Discipline #12 (both restatements and § C.9.5a are named).
- ADR-002: row text after a graded run is Matt's, and he has ruled. The procedural remedies are within the gate and the conductor.

## Action

- [ ] **gandalf:** record H-6 PASS-WITH-WARN against KP-184. Put WARN-1's routing (H-7 classifies; class (ii) is a HALT to Matt, never a port repair) and INFO-4's reading of L2 on the attempt-2 launch sheet.
- [ ] **drax (H-4):** the harness takes the read's runtime digest as an input and fails closed at boot on any mismatch, before any cell runs (WARN-2). It writes `pre_attempt_read` from that input. Resolve INFO-1 (count `n_ticks_released` at the verdict, or correct the comment).
- [ ] **jack-ryan:** H-3, H-2 and H-7 per the list above. The grader is pinned before the emission (INFO-3).
- [ ] **gamora:** print the read-vs-attempt difference over the INFO-2 domain in the attempt-2 grade, and any disagreement with the read row by row.
- [ ] **Matt:** nothing needed at this gate.

## References

- Prereg: `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.13.md` (FILE `c35cca9c…`); `…-v1.12.md` (FILE `a0454776…`, § F.2, § F.5, § G, § H)
- Instruments: `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-prereg-v1.13-DRAFT/` (`check_v1p13_draft.py`, `pins_v1p13.py`, `fill_draft.py`, `oracle_channel_hook.py`, `oracle_hook/`, `results.json`, `run_stdout.txt`, `pins_stdout.txt`; draft § L)
- Godot (git objects only): `05508a0` `kc2_runtime/` (`sim/kc2rt_fight.gd:343-348, 1715-1740, 5840-5890`; `sim/kc2rt_board.gd:950-980`; `MANIFEST.json`; `tools/make_manifest.py`); `evidence/kc2-play/2026-10-01-g3-25cell-kp180/` (MANIFEST `4347e87d…`); `b4c1ff3` `evidence/kc2-play/2026-10-01-g3-25cell-kp177/` (MANIFEST `78bbcc8d…`), `kc2_runtime/tools/kc2rt_g3_oracle_trace.py` (FILE `51f46965…`); `9b0ad0c` attempt-1 cells
- Oracle (engine `22cd2288`): `simulation/kc2/channel_policy.py:297-392`; `run.py:2790-2815`; `wave_engine.py` `pools_for`; `actor_state.py:252-261`; the pack `kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/waves.json`
- Charter KP-177 to KP-184; Q96 in `canonical/matt_decision_needed/README.md`
- My prior findings: `agentic_orchestration/qa/findings/2026-10-01-kc2-play-attempt1-v1.12-grade-gate2.md` (347ce2e1e), `…-attempt1-repairs-gate2.md` (ea0317306)
