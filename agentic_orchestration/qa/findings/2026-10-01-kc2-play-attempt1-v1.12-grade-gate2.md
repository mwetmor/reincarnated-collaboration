# Finding — 2026-10-01 — Run KC2-PLAY · GATE-2 on gamora's grade of record, v1.12 graded attempt 1

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **PASS-WITH-WARN. 0 BLOCK · 1 WARN · 7 INFO.** The verdict **`STRUCTURAL` is upheld**. Attempt 1 is **consumed** (1 of 2 remains). **The Q96 HALT stands.** The one WARN is in the grade's *repair guidance* for `TA-X-08`, not in its verdict: the oracle does census the lethal tick, as a live tick. drax is repairing now, so WARN-1 goes to him first.
**Target:** grade collab `d2fe958ec`: note `agentic_orchestration/gamora/notes/2026-10-01-kc2-play-ta-attempt1-v1.12-grade.md`; script, `results.json` and verdict file FILE `af3754c7…` in `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-ta-attempt1-v1.12-grade/`. Evidence godot `9b0ad0c`. Runtime tree `a9b756cd…`. Prereg v1.12 FILE `a0454776…` (re-derived here). drax's P-2 diagnosis is godot `b215b11`.
**Developer:** gamora (grade) · drax (emission, diagnosis) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code), #4 (the committed record is the truth), #5 (severity matters). Disciplines #11 (empirical inspection over assumption) and #12 (semantic-shifting fixes need explicit framing). ADR-002. Charter KP-175 to KP-177.
**Read-only attestation:** I read godot through `git archive 9b0ad0c`, extracted into my scratchpad. I read the engine at HEAD `22cd2288`, which is the oracle pin, with no tracked modification to the files I cite. I hash-verified the sealed `[M-POL2]` cell (`ad61ad2a…`) and read it by key only (K-7). I re-ran the grading script from a **scratchpad copy**, so nothing was written beside the original. This file is the only thing I wrote.

---

## Per-item verdicts

| # | item | verdict |
|---|---|---|
| 1 | `STRUCTURAL`, § G precedence, attempt consumed, C1 | **CONCUR** |
| 2 | `TA-X-08` RED 25/25, port defect, off by one | **CONCUR on the RED, the defect and the arithmetic.** ⚠ **WARN-1 on the mechanism and the repair direction** |
| 3 | `TA-X-16` RED 20/25, prereg defect, HALT | **CONCUR. No reading of v1.12, or of the rows it carries, makes `TA-X-16` per-wave. The HALT stands** |
| 4 | the 8 UNGRADEABLE rows; the P-2 rulings | **CONCUR** (INFO-1, INFO-5) |
| 5 | the nine § G.3 fields are report-face defects, not antecedents | **CONCUR** (INFO-7) |
| 6 | independence re-run | **CONFIRMED: exits 0; all three outputs are byte-identical** |

---

## What I found

### Item 1 · The verdict and the attempt: CONCUR

- **Precedence.** v1.12 § G: *"Order: `STRUCTURAL → INDETERMINATE → PASS`; stop at the first hit."* `STRUCTURAL` is *"≥ 1 of the 28 EXACT rows RED."* Two EXACT rows are RED. P-2 red only feeds the `INDETERMINATE` antecedent (v1.8 § B.3, carried: *"`P-2` red → `TA-X-03…05` UNGRADEABLE → `INDETERMINATE`"*), and § G stops before it reaches that antecedent. **gamora's reading is correct, and the KP-176 "INDETERMINATE" reading was wrong.**
- **Either red alone decides the verdict.** So does `TA-X-08` alone, a genuine port defect (Item 2). The verdict does not depend on the disputed `TA-X-16` row.
- **The counter.** § G: `STRUCTURAL` *"consumes one of v1.12's two attempts"*. **1 of 2 remains.**
- **C1 conformance, re-derived from the emission:**
  - all five arms' `arm_config_a8.rowset` equal § B.1a's ROWSETs;
  - `setup_config_rowset` = `207ab21f…`, and `setup_probe_rows_applied` = 0 on all five arms;
  - the manifest `g3.per_cell` covers 25 cells, and every one has `passes`, `injected: []`, 0 decision divergences, 0 draw mismatches, no port-only stream and `death.equal`;
  - the G3 source is the KP-173 summaries at the same tree digest. The runtime is byte-unchanged from `0802ab1` to `9b0ad0c`, and gamora recomputed it.
  - **Every graded row is graded on a conforming arm.**

### Item 2 · `TA-X-08`: the RED, the defect and the arithmetic stand. The mechanism does not (WARN-1)

**Re-derived on all 25 cells, not only two.** D = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE, computed from each cell's own `state_counts`. On every cell:
- `n_player_ticks_observed − D − PRE_FIGHT = 1`;
- `(n_channelling + n_released) − D = 1`;
- `state_counts.DEAD = 1`;
- `n_player_ticks_observed = terminal.run_tick`.

Examples:

| cell | observed | D | PRE_FIGHT | chan + rel | DEAD |
|---|---:|---:|---:|---:|---:|
| M-POL-2 s0 | 467 | 466 | 0 | 467 | 1 |
| M0 s0 | 2,013 | 2,012 | 0 | 2,013 | 1 |
| W1 s4 | 483 | 482 | 0 | 483 | 1 |
| M0 s4 | 472 | 471 | 0 | 472 | 1 |

**The off-by-one is exactly as stated, and it is exactly the DEAD tick.** It is a port defect, because the basis of record satisfies both identities. In the sealed `[M-POL2]` cell, salt 0 has census 6 + 867 + 41 + 63 + 113 = 1,090 = `n_player_ticks_observed`, so 1,090 = 1,084 + 6. Salt 1 gives 307 = 305 + 2. No sealed census has a DEAD key.

**⚠ WARN-1: the grade says the oracle "does not census the death tick". The oracle source says otherwise.** The sealed arithmetic cannot tell apart "the lethal tick is omitted" and "the lethal tick is censused as alive". The oracle at `22cd2288` settles it:
- `run.py:2810`: `channel_gate_fold.observe(…)`, which increments `n_observe`, runs **before** the death check at `run.py:3885` (`if hp_player <= 0.0: player_dead = True`). The loop `break`s at `:4067`, after the tick's player row and channel track are already written.
- `run.py:4937`: `player_dead_tick = ledger_player[-1][0]`, i.e. the lethal tick itself.
- `actor_state.py:252`: `alive = player_dead_tick is None or rt <= player_dead_tick`. **The lethal tick is classified ALIVE**, under its live state, and is **inside D**.
- This code has not changed since 2026-08-25 00:27, which predates the seal (11:44 the same day). The sealed cell was produced by it.

So the defect is not that the port censuses the lethal tick. **It is that the port labels the lethal tick `DEAD`** (`kc2rt_fight.gd:5734–5735`, `if player_hp <= 0.0: s = ST_DEAD`) while still counting it in `n_player_ticks_observed` and `n_channelling`.

**Consequence.** Grade § 4.1 proposes *"Either do not census it, or exclude a `DEAD` tick from `n_player_ticks_observed` and from `n_channelling`/`n_released`"*, and § 9 item 1 repeats it. Both options turn the identities green with **D one tick short of the oracle's on every dying cell** (M-POL-2 s0 would give 466 where the oracle convention gives 467). `TA-X-08` checks an internal identity and cannot see that. **It would be a hollow green: the same shape as P-2's Fix A, which the same grade correctly refuses.** The faithful repair is to classify the lethal tick by its live state. `DEAD` applies only to ticks after the lethal tick, and leg A never reaches one. The result is observed 467 = D 467 + 0, and 405 + 62 = 467 = D.

**This is a repair-guidance defect. The verdict is unaffected:** the row is RED under either reading.

### Item 3 · `TA-X-16`: a prereg defect. The HALT stands

**I looked for a per-wave reading and did not find one.** Every reading I tried:

1. **The row text.** v1.12 § F.2: *"`n_pool_picks == 47`"*, an integer constant. It is carried unchanged from v1.8 § F.2 and v1.9–v1.11.
2. **The rows it carries by reference fix the window explicitly.** v1.6/v1.7 § F.2: *"distinct `(global_wave, spawn_point)` pairs **over waves 151–160**: `54` with p06, `47` without."* v1.5 § F.2c: *"Assert, under `p06: OFF`: `n_pool_picks == 47` …"*. v1.8 § F.2c's closing condition: *"the three counters are emitted"*. **None of them conditions the count on the waves played.**
3. **The per-wave vector is not in the text at all.** `V11-P06-1` occurs in **no** prereg version, v1.0 to v1.12 (grep, zero hits). The per-wave vector gamora checked comes from the harness manifest (`roster["⚑ TA-X-16_p06"]["V11-P06-1_expects"]`), not from the prereg.
4. **The "pack property" reading.** v1.5 calls the pick count *"a pack property"*, and the basis column reads `waves.json`. Read that way, 47 is the board's schedule, and the manifest-grain `active_points_per_wave` (sum 47) would make the row GREEN. **§ B.1a forecloses this:** `TA-X-16` sits in the *"all 25 cells"* run-internal group, not in the *"no run"* group with `TA-X-09`/`18`/`20`/`21`/`26`. It is a per-cell statistic. The reading would not be per-wave either. gamora was right to refuse it.
5. **The leg-A reading.** § B.1 says *"declared fight scope waves 151–160, leg A (stop at the player's first death)"*. That defines the run, not the statistic's window. No text restates 47 as a function of the terminal wave.

**Unsatisfiability, stated precisely and more strongly than in the grade.**
- G3 shows the port **decision-identical to the oracle on the oracle's own draws**, dying at the oracle's wave and tick on 25/25 (e.g. M-POL-2 s0: `[156, 88]` on both sides). On the reference realisation, terminal waves are `[156,152,155,152,152]` (M-POL-2), `[155,151,156,155,155]` (M0) and `[156,152,155,152,155]` (W1). **A port that is bit-faithful on the reference realisation would therefore score `TA-X-16` RED on 25/25.**
- On the port's own generator, the row passes only if all 25 cells reach w160. § F.3 calls that *"failed to be in [a hard board]"*.
- **So the row rewards infidelity.** gamora's "prereg defect, HALT to Matt" is correct. Restating an EXACT row after a graded run is Matt's decision (KP-137; v1.8 § F.2d). Firing attempt 2 under this text would spend the last attempt on a red that is known in advance.

**Within-row note (INFO-2).** Clauses 2 and 3 have **no per-cell counter** in the emission:
- `n_spawn_point_6_keys_rolled` is not emitted anywhere. gamora graded it by proxy: no point-6 row in the `TA-X-15` schedule.
- The filtered-key counter exists only at manifest grain (`picks_suppressed: 18`).

This does not change the verdict, because clause 1 is RED. But v1.8 § F.2c's closing condition (*"the three counters are emitted"*) is not met per cell. `picks_suppressed` counts p06 `wave_spawn` **rows** (`kc2rt_roster.gd:494–496`), 18 of them. That is not the 7 `(wave, point)` pairs behind 54 − 47.

### Item 4 · The 8 UNGRADEABLE rows and the P-2 rulings: CONCUR

- **`TA-X-03`/`04`/`05`.** v1.8 § B.3, carried, says verbatim: *"`P-2` red → `TA-X-03…05` UNGRADEABLE"*. gamora's scope correction (03…05, not the harness's 03…06) is right: *"`TA-X-06` is declared and enters no antecedent."*
- **Ruling 1: a probe-defect red still gates. CONCUR.** The text keys on the probe outcome. drax's corrected digest is a comparison computed after the fact, and § G says *"No post-hoc widening, by anyone."*
- **Ruling 2: Fix A alone would be a hollow green. CONCUR.** drax's own § 3.2 confirms that `declare_extra_site` forks no stream and nothing calls it. Fixing the digest without inserting a real fold proves only that adding a registry entry perturbs nothing. gamora's four requirements are right: a real fold, a measured zero, one digest function, and must-RED controls (+ a fresh pack per leg). INFO-5 adds one more.
- **`TA-X-09`/`20`/`21`, `27(b)` and `29(b)(c)`: UNGRADEABLE. CONCUR.** None has a value in the hash-pinned emission; only `tmp/` copies or pointers exist. This follows the run's precedent (v1.5 § F.2c: *"UNGRADEABLE — no value emitted"*). The stricter evidentiary rule moves rows toward UNGRADEABLE, never toward GREEN, so it is not a widening. Her v1.7 leniency was explicitly conditional on these values being folded into the emission, and they were not. INFO-1 corrects one supporting claim.

### Item 5 · The nine § G.3 fields: CONCUR

§ G's antecedents are the 28 EXACT rows, `P-1` to `P-5`, and `TA-X-07(c)`. None of the nine fields appears in any of them. H-4's harness obligations among § G.3's fields are `r11_bound`, `g3` and `ta_x_18`, and all three were emitted. `declared_ungradeable` is met in effect: the emission labels `TA-X-06` UNGRADEABLE-declared, and the verdict file carries exactly `["TA-X-06"]`. The grader assembled the verdict file and kept harness-emitted and grader-filled fields in separate blocks, which is the honest construction. INFO-7 notes that this is the established practice, not a gap.

### Item 6 · Independence: CONFIRMED

I copied `grade_attempt1_v1p12.py` (FILE `27eb4079…`) into my scratchpad and ran it with `python3`. It writes only beside itself (`HERE`). Results:
- **exit 0**, stderr empty;
- `results.json` `f061d05a5ebe9247ecf97f8f568eba796a78f303be3f3fef0dfdf75ccc4ca244`: **byte-identical** to the committed file;
- verdict file `af3754c701f8afb22a5501b0b955fb8b2dc36cf361d5033980daa23e4c86f2f0`: **byte-identical**;
- stdout `b5da5a9aabb02919800d548c1b8b33ad5ed65cc6c95d359f6bc9c136f8a39327`: **byte-identical** to `run_stdout.txt`.

The committed artifacts at `d2fe958ec` equal the worktree. The engine's tracked-modification count was 633 both before and after the run, so the run changed nothing there.

---

## INFO

- **INFO-1 · `TA-X-21`: "demonstrably not of the graded tree" is not demonstrated.** `2ce053d` changed one file, `kc2_runtime/tests/kc2rt_ta_emit.gd`, whose worktree mtime is **05:27:35**. The `tmp/` purity scan is 05:28:37, `t0_report` is 05:32:11 and the commit is 05:32:37. By mtime, both supplementary files **postdate the edit**; they predate only the commit. The commit message (*"SUITE GREEN after (purity 76 files / 0)"*) is consistent with the scan being the after-edit run. mtime is not proof either way. **The correct word is "unverifiable"**, and that is exactly why `tmp/` cannot carry a grade. The ruling stands on its primary ground.
- **INFO-2 · `TA-X-16` clauses 2 and 3 are not emitted per cell** (Item 3). For v1.13 and the emission repair: a named per-cell, per-wave `n_spawn_point_6_keys_rolled`; a per-cell, per-wave filtered-key counter with its grain declared (rows or pairs); and an expected value for each.
- **INFO-3 · Stale prose in the emission.** `roster["⚑ TA-X-16_p06"]["⚑ note"]` reads *"the port read the default and spawned p06 on seven waves"*. The same block's data (`active_points_per_wave` = V11-P06-1, no point-6 row on any cell) says the opposite. It is a report-face hazard, so remove it in the emission pass.
- **INFO-4 · `PRE_FIGHT` convention: the port records 0 on 25/25; the oracle records one per wave played.** `actor_state.py:255–261` gives each wave-run's first player row (no predecessor) `PRE_FIGHT`. Sealed: PF = 6 for a w156 death, 2 for w152, 1 for w151. The port never assigns `ST_PRE_FIGHT`. `TA-X-08`'s identities are internal, so this does not grade. But every D-based diagnostic (`TA-B-02` to `09`) differs from the oracle's convention by `n_waves` ticks. If it is cheap, align it in the same `_census` repair as WARN-1. If not, print it as a named convention difference.
- **INFO-5 · P-2's inserted fold should precede a live fold in fork order.** A fold appended **last** in fork order cannot expose a port whose stream seeds depend on fork index, because the indices of the existing folds do not move. Insert it at a position that precedes at least one live fold's `fork_stream`, and say so in the v1.13 operational reading (grade § 2.2 item 1).
- **INFO-6 · "Unsatisfiable by any faithful port" has a cleaner proof than the grade gives** (Item 3). G3's bit-faithfulness on the oracle draws, combined with the oracle's terminal waves, means a faithful port fails on the reference realisation on 25/25. Use that sentence in v1.13's rationale.
- **INFO-7 · A grader-assembled verdict file is precedent, not a harness gap.** v1.7's verdict file of record (FILE `9be2d56b…`, pinned in v1.10/v1.11 as *"attempt-1 verdict file"*) was written by gamora (collab `15d6f5ce8`). KP-176's *"a harness gap neither gate caught"* overstates it. gamora's recommendation still stands: the runtime should emit `runtime_digest` and `runtime_header` itself, so that its identity rests on the emission rather than on the seat.

---

## Why the repair Gate-2 and the delta Gate-2 did not catch `TA-X-08` or `TA-X-16`, honestly

**I ran both gates, and I also wrote the v1.12 pre-read. Neither row was caught at any of those three seats.**

1. **Every layer was scoped to the delta, so a row whose text never changed was never re-read.**
   - The v1.12 pre-read (H-7) was partial by design: *"the rest may cite jack-ryan's v1.11 pre-read"*.
   - The repair Gate-2 covered the repair items plus § H.
   - The delta Gate-2 covered only the diff (*"Items 1–8 above stand for every file the delta does not touch"*).
   - `TA-X-16` has read "CARRIED" since v1.8. `TA-X-08`'s text dates from v1.1.
   - **Delta review compounds:** each layer checks what moved, and nothing was assigned to check a row whose *regime* moved underneath it.
2. **The regime did move, and it was printed in front of me.**
   - Hole 2's repair (death check at the floor, before the heal) made death reachable. In v1.7 no cell died, and both rows were GREEN.
   - v1.12 § F.3a, a section I pre-read, prints the port's own M-POL-2 terminals as `[153, 160, 154, 154, 153]`: four of five salts end before w160. That is `TA-X-16`'s red, on the face of the prereg.
   - § B.1a's oracle table says the reference never reaches w160.
   - I read both as diagnostics and never joined them to the row whose expected value assumes w160.
3. **The port is deterministic, and the attempt's outcome was knowable before it fired.** I checked that knowledge for one row only.
   - The run already accepts pre-evaluating a row from the candidate's emission before firing: L2 required (L2) of `TA-X-07(c)` on all 25 cells *"evaluated from its emission before firing"*.
   - At the repair Gate-2, I ran the T-A emitter on one cell and **BLOCKed on a predicted `TA-X-29(e)` red**.
   - That emitter writes `TA-X-08`'s identities, with their own `holds` field, into every cell. **I read only the § H lines.**
   - The cells of the graded run say `"holds": false` in plain text.
4. **The lesson for gate briefs (proposed; Matt rules on point (c), because it bears on the cap):**
   - **(a) Reference-satisfiability audit, once per prereg version and not delta-scoped.** For each EXACT row, can the oracle's own arm outcomes pass it, on the arms and window it is graded on? This audit looks at no port outcome, so it raises no forking-paths concern. It catches `TA-X-16` mechanically.
   - **(b) Regime-change trigger.** When a repair makes a previously unreachable state reachable (death, a cap, a branch), every row that reads that state is re-opened and checked against the oracle source on the new branch. That would have caught `TA-X-08`, and WARN-1 shows why the check has to be against the source and not only the seal.
   - **(c) A full 28-row dry read of the candidate digest's emission** as an L2 precondition, extending what the run already does for `TA-X-07(c)` and did ad hoc for `TA-X-29(e)`. EXACT rows carry no tolerance to fit, and § G already forbids post-hoc widening, so this tests the port against fixed laws. It does not tune a statistic.

---

## Q96: my recommendation

**(a) Restate `TA-X-16` per-wave in a v1.13: YES.** Suggested form, per cell:
1. for each wave `w` in `[151, terminal_wave]`, `pool_picks(w) == V11-P06-1[w − 151]`, with the vector `[5,5,5,4,4,5,5,5,5,4]` **pinned in the prereg** and derived by script from `waves.json` at p06 OFF, with 54/47 as its checksum;
2. `n_pool_picks == Σ_{w ≤ terminal} V11-P06-1[w − 151]`;
3. `n_spawn_point_6_keys_rolled == 0`, as a named per-cell counter;
4. the filtered-key counter per cell per wave, with its grain declared, **equal to the p06 entries the board would have rolled on the waves played**. Graded, not only emitted, so that the counter proves the filter fired.

**Before committing v1.13, verify the restated row on the oracle's own G3 traces** (the reference-satisfiability audit, applied first to the row that motivated it). State in v1.13 that the restatement does not re-grade attempt 1, which stands `STRUCTURAL` on `TA-X-08` alone. Under Discipline #12 this is a semantic restatement (declared window → realised window), so it is correctly Matt's call. Fold in gamora's P-2 operational reading (+ INFO-5) and WARN-1's census reading in the same version.

**(b) The budget: KEEP it at 1 remaining. Do not reset.**
- **Counterfactual.** Had `TA-X-16` been caught before the fire, attempt 1 would have fired under a corrected v1.13 and still been `STRUCTURAL` on `TA-X-08`, a genuine port defect on 25/25 cells. The prereg defect did not cause the spend.
- The attempt bought real information: `TA-X-08`, P-2's unsoundness and the emission gaps.
- Q85 guard 3 (*"stays on the record, spent"*) is what gives the cap meaning.
- **The case for a reset, which Matt should weigh:** attempt 1 was `STRUCTURAL` by construction before it fired (§ F.3a printed it), and three gates missed that. § G.1's own rationale says not to fire an attempt whose outcome is fixed. If Matt treats that gate failure as decisive, a reset is defensible.
- **My lean is to keep 1 and protect it instead.** Make (a) and (c) of the gate lesson L2 preconditions for attempt 2, so the last attempt cannot be spent on a knowable red.

---

## Rationale

- § G (precedence, the attempt rule, "no post-hoc widening"); § B.1a (the per-row arm table, and C1 evidenced by G3); v1.8 § B.3 (P-2); v1.6/v1.7 § F.2 and v1.5 § F.2c (the `TA-X-16` window); v1.8 § F.2c (the counters).
- REVIEW_PROCESS #4: the grade is checked against the committed text and the oracle source, not against the ledger's summary.
- Discipline #11: WARN-1 is a case where the seal's arithmetic was consistent with two mechanisms, and only the source could decide between them.
- Discipline #12: the `TA-X-16` restatement.
- ADR-002: the verdict and the counter are within the gate's authority. The row restatement, the budget, and gate-lesson point (c) (because it touches the cap) escalate to Matt.

## Action

- [ ] **drax (now, before the repair is committed):** repair `TA-X-08` by classifying the lethal tick **by its live state** (`actor_state.py:252` convention: alive ⇔ `rt ≤ player_dead_tick`). **Do not drop it from the census.** Add a fail-first probe on a dying cell asserting observed = D + PF and chan + rel = D, **and** D equal to the oracle-convention count. Align `PRE_FIGHT` if cheap (INFO-4). In the emission pass, emit the per-cell `TA-X-16` counters (INFO-2) and remove the stale note (INFO-3).
- [ ] **jack-ryan (repair Gate-2):** I will check the `_census` repair against `actor_state.py`'s convention. A repair that drops the lethal tick is a hollow green and will be BLOCKed there. I will also run a full 28-row dry read of the candidate's emission, whether or not the brief asks for one.
- [ ] **gamora:** amend grade § 4.1 and § 9 item 1 per WARN-1, and § 3's `TA-X-21` wording per INFO-1, by addendum. The verdict is untouched. Draft v1.13 on Matt's word, with the restated row verified on the oracle traces first.
- [ ] **gandalf:** carry WARN-1 to drax immediately, and put the gate-lesson points (a)–(c) into the attempt-2 L2 list for Matt.
- [ ] **Matt (Q96):** (1) restate `TA-X-16` per-wave in v1.13: recommended **yes**; (2) budget: recommended **keep at 1**; (3) gate-lesson point (c) as an L2 precondition: recommended **yes**.

## References

- Grade: `agentic_orchestration/gamora/notes/2026-10-01-kc2-play-ta-attempt1-v1.12-grade.md`; `agentic_orchestration/gamora/analyses/2026-10-01-kc2-play-ta-attempt1-v1.12-grade/{grade_attempt1_v1p12.py, results.json, ta_verdict_v1p12_attempt1.json, run_stdout.txt}` (collab `d2fe958ec`)
- Prereg: `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md` (§ B.1, § B.1a, § F.2, § F.3, § F.3a, § G, § H); v1.8 § B.3, § F.2, § F.2c; v1.6/v1.7 § F.2; v1.5 § F.2c
- Evidence: godot `9b0ad0c`, `evidence/kc2-play/2026-10-01-ta-attempt1-v1.12-cells/` (25 cells, `ta_manifest.json`); `evidence/kc2-play/2026-10-01-g3-25cell-kp173/summaries/`
- Port: `kc2_runtime/sim/kc2rt_fight.gd:5731–5746` (`_census`); `kc2_runtime/sim/kc2rt_roster.gd:494–496`, `:1938`
- Oracle (engine `22cd2288`): `src/reincarnated/simulation/kc2/run.py:2810`, `:3885`, `:4067`, `:4937`; `actor_state.py:149–170`, `:234–262`; `channel_policy.py:361–376`
- Sealed: `reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` (FILE `ad61ad2a…`, read by key)
- drax diagnosis: godot `b215b11`, `docs/kc2-p2-diagnosis-2026-10-01.md`
- Charter: `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`, KP-175 to KP-177
- My prior gates: `agentic_orchestration/qa/findings/2026-10-01-kc2-play-repair-gate2.md` (+ delta addendum), `2026-10-01-kc2-play-prereg-v1.12-pre-read.md`
