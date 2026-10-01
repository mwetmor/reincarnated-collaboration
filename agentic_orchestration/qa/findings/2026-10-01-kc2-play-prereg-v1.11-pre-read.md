# Finding — 2026-10-01 — Run KC2-PLAY · T-A prereg v1.11 pre-read (H-7, partial: everything v1.12 will carry; § F.2k excluded)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **WARN**: 0 BLOCK · 0 ESCALATE · 5 WARN · 6 INFO. **No item blocks v1.12 from carrying v1.11's non-§ F.2k content.** Every WARN is a text change v1.12 is being written anyway to make.
**Target:** prereg v1.11, `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.11.md`, collab `f403c53c6`, **FILE sha256 `312d71aaf3b5a15ca44a8179cbb46c35a50343e5bca23ab5201c73ec9c8278cc`**. Compared against v1.10 (collab `690865868`, FILE `b1dd68efe2ce6009c2981d1c25bb182aba8c444945ec81f53a5c3c0c8b79061c`, never pre-read until now) and v1.9 (FILE `b787308c8c331e98fee6221c97174bf8f696a5b55d699611c5ab697625de95dd`). All three hashes were derived by me before reading and match the brief. Pack v3.7.1 (model PACK `48a4c94c…`, reference PACK `1887257f…`). Oracle at engine HEAD `22cd2288`.
**Developer:** gamora (author) · drax (port) · star-lord (pack) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code) · #4 (the committed record is the truth) · #5 (severity matters). Disciplines #11 (empirical inspection over assumption) · **#12 (semantic-shifting fixes need explicit framing)**. ADR-002. Charter KP-144 … KP-156, WARN-16.
**Scope, as briefed:** Matt ruled Q92 (a), compensated summation (KP-155). **§ F.2k (R-11) is rewritten in v1.12 and is NOT ruled here.** § 7 lists only what in § F.2k v1.12 must not carry.
**Read-before-result attestation:** no graded run exists under v1.10 or v1.11. I read godot only through git objects (`git show`/`git grep` at `ffb454e` and HEAD `fae29ec`), with no checkout and nothing written. I ran the oracle only through `SpawnStructureFold.offset`, with `PYTHONDONTWRITEBYTECODE=1`. *Disclosure:* one `git status --porcelain` I ran in the engine may have refreshed that repo's index stat cache. It changed no tracked content.

---

## What I found

### Pins re-derived (Discipline #11). Every one below was computed by me from the files, not read from the prereg

| claim | how I checked | result |
|---|---|---|
| Model PACK `48a4c94c…`, reference PACK `1887257f…`, cross-pin | The manifest's `pack_digest_law_exact` applied to the member rows; every member's FILE digest and byte count recomputed; the on-disk set checked equal to the manifest's | 19/19 and 7/7, no extra file and none missing; both digests reproduce; cross-pin equal ✓. Manifest FILEs `be5d2566…` / `212b8652…` ✓ |
| § B.5 member table (19 + 7 FILE digests and byte counts) | as above | all ✓ |
| v3.7 → v3.7.1: only `input_closure.json`, `meta.json` moved and `input_closure_v3p7p1.json` was added | member-by-member diff of the two manifests | ✓ (16 of 18 carried members are byte-identical) |
| The six new rowsets plus the all-rows digest `cb43d84e…`, 891 rows | the pack's ROWSET law over `⚑ v3p7p1_rows` | all seven ✓ and equal to `meta.json :: ⚑ v3p7p1_supersession` |
| v3.7.1 `k3` = v3.7 `k3` minus `IC7-K-0036/37/38/0255`, verbatim and in order; each withdrawn row appears in `w11` | script | ✓ (612 → 608) |
| `IC7-Q-0073` = 46373536579806 (= `0x2A2D2E2C_C0DE`, `control_application.py:117`); `IC7-Q-0387` = 70.0 | read off `k12` | ✓. The stream is a lazy `rng` property (`:784-787`), consistent with § A.4's "constructed on no graded arm" |
| The 62 closure-read files re-hash to their `f1`/`p2` rows | rehashed in both repos | **62/62** ✓ |
| v3.7 PACKs `9bee0357…` / `978bb893…` (v1.10's pins) | same law | ✓ |
| `TA-X-10` = `43.758085029822276` | `max‖spawn_xy‖` (p01, 35.758085029822276) + `placement_extents_m` 8.0, off v3.7.1 `arena.json` | ✓ |
| `P-i` `cb6a008b…` · closure tool `e5793c28…` · law `2c24ea92…` · receipt `a0ad8246…` | `shasum` | all ✓ |
| godot read pins `e6903095…` (`kc2rt_fight.gd`) · `406ffeca…` (`kc2rt_laws.gd`) at `ffb454e` | `git show ffb454e:<path>` | ✓. ⚑ At HEAD `fae29ec`, `kc2rt_fight.gd` is already `41310e5e…` (pass 3b) (§ 7) |
| Oracle POST terminals per arm (§ B.1a figures table) | read off the five `kc2-v3p7p1-POST-bare-*` files | all five rows ✓, seconds included. Sink digests also show `M-POL-2-NULL` ≡ `M0` and `W1-NULL` ≡ `M-POL-2` bitwise on all five salts, and `W1` ≢ `M-POL-2` on salts 0 and 4 |
| § F.3a statistics | recomputed | U = 17, exact permutation p = 0.4127 (252 splits); Clopper–Pearson 0/5 upper bounds 0.4507 / 0.5218; Fisher p = 1.0 ✓ |

---

### Item 1 · § A.5, the `TA-X-18` re-derivation → **PASS** (one WARN on the operational reading of "exact", carried to v1.12)

**Correction or fit? A correction.** Four independent grounds, each checked:
1. **I reproduced the value two ways.** By hand: θ = float32(2π)·0.5 = 3.1415927410125732, ρ = 8.0·0.5, giving `(cos θ·ρ, sin θ·ρ)` = `(-3.999999999999985, -3.49691120014899e-07)`. And by calling the oracle's `SpawnStructureFold().offset` (`POLAR_UNIFORM_RHO`, `CONTINUOUS`) with a stream that returns 0.5 twice: **the same value, bit for bit.** The code path is `spawn_structure.py:327-333` (`theta = FACING_SPAN_RAD * u1`, `return (math.cos(theta) * rho, math.sin(theta) * rho)`).
2. **The oracle has returned this value since before v1.1 existed.** `FACING_SPAN_RAD` is read from legolas' `pm4aa_placement_law.json :: random_facing.value` = 6.2831854820251465 (`0x40c90fdb`, which is exactly float32(2π)). That file has **one commit** (`b4a43cea8`, 2026-08-16) and hashes to the code's pinned `55506b69…`. v1.1 was authored 2026-09-20. The only later change to `spawn_structure.py` (`880f75ff`) is comment-only on the path. **So v1.1's `(−4.0, 0.0)` was a mis-derivation**, made by idealising θ = π, and no build of the oracle ever produced it.
3. **It moves away from port data, not toward it.** The only port value on record (v1.7 attempt 1) is the `math.tau` port's `(−4.0, 4.9e-16)`. The new expected value turns that port RED. A fit would have moved toward the port.
4. **No graded run existed under v1.10** when the value moved (D4 held).

**Is the new reading of "exact" sound? Yes, and it is a restoration, not a tightening.** v1.1 wrote "exact". The grade of record (2026-09-21) and v1.7 attempt 1 graded the row GREEN as "nearest of three laws, separation > 1e-6". That was **a looser rule than the written one**, applied silently, and under it the row cannot see a 2π-built port (a 3.5e-7 gap, inside 1e-6). v1.10 names the shift under Discipline #12: in § A.5, in the v1.10 commit body, and in ledger KP-149. Equality of float64 repr strings is equivalent to bitwise equality for finite values, with ±0 distinguished, so it is well-defined. `C-o` correctly does not cover the row, and a last-ulp libm disagreement routes to Matt under `F.1a` and is never widened by the grader. Both are the right handling. The row's scope widened from "which law" to "which law, with the oracle's θ constant", and that widening was always inside the written tolerance. **OQ-16 may be CLOSED on its lean, citing this finding.**

**⚠ WARN-1 · "at `repr` precision" is not yet operational.** As written it can be read as *string* equality with CPython's shortest repr. A GDScript emission printed `%.17g` (`-3.4969112001489899e-07`) is the **same float64**, yet it fails a string compare. A false RED here is `STRUCTURAL` and burns an attempt. Conversely, a lossy print (6 significant digits) must not be read as GREEN. **v1.12 must say:** parse each emitted component to float64 and compare bits (`==`, with the sign of zero checked); the port's emission of this probe must be round-trip lossless (17 significant digits or hex-float), or the row is `UNGRADEABLE`, not green. *(Disciplines #11, #12; Principle #5.)*

**INFO-1.** Discipline #12 also asks for a decisions-log entry. The run's ledger (KP-149) is its decision record, and I accept that as sufficient for a run-internal prereg semantic. No entry is owed.

---

### Item 2 · § B.1a, the arm table → **PASS** (WARN-2 on the `setup` job; INFO-2, INFO-3)

**Cited to a8 (pack v3.7.1, model PACK `48a4c94c…`): verified row by row.** Per-job id ranges are contiguous. Each count and each per-job ROWSET (`id`-ordered, the pack's law) reproduces exactly: `setup` 27 `c01d1dda…` · `M0` 70 `68549af0…` · `M-POL-2` 76 `e698d5f5…` · `M-POL-2-NULL` 76 `4393a14b…` · `W1` 78 `5188284d…` · `W1-NULL` 78 `b2abff69…` · `WALK` 54 `63c530ed…`. The total is 459 ✓. Each "distinguishing rows" claim is true on the wire:
- **`M0`**: no `ChannelPolicyFold` row and no `ArenaFold` row; `replay(channel_gate_fold)` omitted (`IC7-A-0208…0212`); `run_cell(seat=False, arena=None)` (`0218…0222`).
- **`M-POL-2`**: `ChannelPolicyFold(armed=True)` explicit, one per salt (`0089…0093`); `run_cell(seat=True, arena=None)`.
- **`M-POL-2-NULL`**: `armed=False` explicit (`0013…0017`).
- **`W1`**: `ArenaFold(armed=True)` (`0307`).
- **`W1-NULL`**: `ArenaFold(armed=False)` (`0229`), with the channel fold armed.
- **`WALK`**: `pools_for(bonus_spawns_enabled=True)` ×10, `fold_at(to_hit, attack_speed)` ×10.
- **PX-LO**: on exactly 51 rows as a direct argument (5 × 10 `KinematicsFold` + 1 in `setup`).

**`TA-B-01` grades on `M-POL-2`: confirmed.** The oracle's POST `M-POL-2` is `[156,152,155,152,152]`, and `W1` is `[…,155]`. v1.7 attempt 1 compared `TA-B-01` against `[M-POL2]` (verdict file, `diagnostics[TA-B-01].oracle_reference`). The KP-146 flag is closed correctly.

**Consistent with the oracle's code and with attempt 1:**
- `TA-X-03`, `TA-X-04` and `TA-X-05` hold bitwise at the oracle level (sink digests above), so the relations are attainable as written.
- Run-internal rows on all 25 cells match attempt 1's "25/25 throughout".
- `TA-X-10` on `W1` only matches attempt 1.
- `TA-X-25` per arm per salt matches attempt 1.
- `ArenaFold(armed=False)` still emits `n_wall_clamps_*` = 0 (`arena_fold.py:209-210, 442-443`), so `TA-X-11` on `W1-NULL` is gradeable rather than `NODATA`.

**⚠ WARN-2 · `setup` mixes configuration with a probe run, and the prereg tells the harness to apply both.** § B.1a: *"Each arm is the a8 job of the same name, plus the shared setup job"*, and § G makes an arm "not configured from its a8 rows" C1. The `setup` job's own scope reads *"make_runner + the tick-period probe"*. Its rows include the probe's `_overrides(policy=None, kinematics=None, seek_fold=True)` (`IC7-A-0457`), `run_cell(salt=0, seat=False, arena omitted)` (`IC7-A-0458`), a `replay(…)` (`IC7-A-0456`), and the fold constructions that run made. Read literally, "configure the arm from setup + arm rows" applies `policy=None` / `seat=False` to every arm. The pack does not mark rows individually as configuration or probe. **v1.12 must partition `setup` by id**: loader and configuration (`IC7-A-0435`, `0439`, `0446`, `0452`, `0453`, `0454`, …) versus the tick-period probe (`0455…0459` and the constructions made inside it), and state the harness obligation for each. *(Principle #5: C1 hinges on this sentence.)*

**INFO-2 · `TA-X-11`'s population grew without being named.** Attempt 1 graded `W1` only (*"clamps 0/0 on 5/5"*). v1.10 and v1.11 grade `W1` + `W1-NULL` (10 cells), per the text "every W1 arm". This is inside the written statistic, and on `W1-NULL` it is vacuous (disarmed, so 0 by construction). v1.12 should name it as a population note in Discipline #12's practice. No value moves.

**INFO-3 · `pet_special_gates`: the prose and the row differ on explicitness.** § B.6 prose writes `pet_special_gates=None` explicitly. The `setup` loader row `IC7-A-0453` records it **omitted** (default `None`), and the `WALK` row `IC7-A-0411` records it explicit. The values are equal, so nothing behavioural follows, and § B.6 already says the row governs. But § B.6's "they agree (checked by script)" did not check this argument, and explicitness is exactly what `a8` exists to record. v1.12: state it, or align the prose.

**INFO-4 · "configured from a8" is self-attested on the emission.** `arm_config_a8.configured_from_a8: true` plus a printed ROWSET proves the harness *had* the rows, not that it *used* them. The real evidence is H-1's G3 on all five arms. v1.12 should tie C1 conformance to the H-1 G3 evidence at the graded digest.

---

### Item 3 · § G.1, the pre-fire list (the KP-152 corrigendum) → **PASS on bounding; WARN-3 on G3's definition; INFO-5**

**Correctly bounded? Yes:**
- It changes **one L2 bullet** (an attempt precondition), not a graded row, a tolerance, an expected value or the declared set.
- It is named as a precondition change under Discipline #12 (§ G.1, § J).
- It resolves an inconsistency that already existed inside v1.10. v1.10 § F.3 called `TA-B-01` *"not evidence of fidelity either way"*, and § 0.5 item 3 placed the side-by-side *outside* the prereg, yet § G.1 required it to fire.
- It needs no Matt route. v1.8 § F.2d case 2 governs re-sizing clause (c) only, and no graded run exists under v1.10 or v1.11 (D4).
- It does not weaken the retained conditions. It **strengthens** KP-152's two arms to **five arms × five salts** (H-1: *"0 decision divergences on all five arms × five salts, death wave and tick equal"*), and keeps "ZERO injections".

**"Unattainable by construction" is accurate, with one scope note:** it holds because the port's PRNG is a different algorithm from the oracle's. Seeding with `engine_seed(9, w)` matches the seed, not the stream. It is a property of this port, not a law.

**⚠ WARN-3 · G3 is now the sole fidelity precondition, and the prereg series never defines it.** "G3" appears in v1.9 through v1.11 only by reference to ledger KP-144 (*"a per-wave loop-trace diff (G3) on the oracle's own draws"*). No prereg pins:
- the instrument or its digest;
- what "the oracle's draws" covers (the RNG tape only, or also the board);
- what counts as a "decision divergence";
- how death tick equality is read.

The label also **collides** with v1.6 and v1.8's "G3", which is a gate inside the `Z5-LAW` composition (*"leech rows DROPPED by G3"*, v1.8 § F.2a(b)). Now that the native per-salt match has been removed, the precondition rests entirely on this instrument. **v1.12 must define G3** (or cite the definition's FILE pin in my repair Gate-2 criteria) and rename or disambiguate one of the two G3s. *(Principle #4: the committed record, not the ledger, carries a firing condition.)*

**INFO-5 · The removal leaves the port's own generator graded by law only. Say so.** The graded run executes on the port's generator, and G3 compares logic on the *oracle's* draws. After the corrigendum, nothing before firing compares the port generator's *outcomes* to the oracle's. Its law is still graded: P-2, `TA-X-27(c)` consumption, `TA-X-15/16/17/25` structure. v1.12 should add a § E.2 declared ceiling: *"the port generator's realisation is graded by law, not by outcome; `TA-B-01` and § F.3a remain non-evidential"*, so a PASS is not read as covering it. Related to § F.3a's n-accounting: to the extent the ORACLE-config board is salt-independent (KP-144(a)), each side fights **one** board realisation, and the five salts are fight-stream replicates on it. So § F.3a remedy (ii), "n in the tens per side", would sample stream variance, not board variance, and cannot separate a board-realisation effect from a defect. This is diagnostic only. It gates nothing.

---

### Item 4 · OQ-15 and OQ-17 → **both correctly routed; neither blocks.** OQ-15 **PASS** (INFO-6); OQ-17 **PASS** (must be closed in v1.12)

**OQ-15 (`TA-X-26(b)` must hash the file the port loads). Not a firing hazard on the port as built.** At godot HEAD `fae29ec`, `kc2_runtime/loader/kc2rt_leech_table.gd:69-99` reads the path and `sha256` from the wire's `V1-JOIN-1`, opens `data_root/data/kc2/pm4p_leech_resistance.csv` (the engine file), hashes its bytes, and **aborts the load on mismatch**. So (b) is met by construction, provided H-4 prints `path_used` and `sha_measured` on the emission and the grader checks `sha_measured == P-i` there (not on a commit message). **INFO-6:** this makes the runtime not pack-self-contained for that one table (the KP-147 "side file" shape). If drax ever re-points the loader to `IC7-F-44` alone for closure purity, (b) goes **red by construction**, and a faithful port would take a STRUCTURAL. That re-point must therefore not happen before OQ-15 is resolved in a dated version. Any widening of (b) is a row change, so it goes to Matt (KP-137). Keep OQ-15 OPEN in v1.12 with this tripwire written in.

**OQ-17 (clause (c) always ignored the sinks).** v1.11's claim *"no past verdict changes"* is **true**. v1.7 attempt 1 was `STRUCTURAL` on `TA-X-25`, and `TA-X-07` was already `UNGRADEABLE` (`n_terms` not emitted). Clause (c) can only make a row `UNGRADEABLE`, and `STRUCTURAL` is evaluated first. It is correctly routed: KP-155 emits per-accumulator term counts and has v1.12 re-derive (c) over **all** accumulators, which closes the blind spot. **v1.12 must close OQ-17 by that re-keying. It must not carry "grade (c) as written".**

---

### Item 5 · Everything else that changed v1.9 → v1.10 → v1.11 → **PASS** (WARN-4, WARN-5)

- **Re-pins (v3.6.1 → v3.7 → v3.7.1).** All pins I could compute reproduce (table above). The epoch law § C.7 declares v3.7 ⟂ v3.7.1 non-comparable at the port level, and that is correct, since pass 3b re-points the loader. The oracle tree identity and the 62/62 inputs hold.
- **`TA-X-09` re-pin (v1.10: `math_rules.json` `969f8090…` → `3b1e2d01…`; v1.11: carried).** **Content verified.** Across v3.6.1, v3.7 and v3.7.1 the following hash identically under the pack's law: `rules` (15) · the nine vectors of the five normative rules (`CHANNEL-MOVEMENT` 2, `RELEASE-TYPE-A` 2, `RELEASE-TYPE-B` 1, `CAST-INTERRUPT-BINDING-EXCLUSIVITY` 2, `DMG-APPLIED` 2) · `vector_law` · `vector_weakness` · `lifted_mechanics` · `unlifted`. The only differences are `v3p2_rows.v12_counterplay[2]` (V12-PATHS-1: `value`, `provenance`) and the new `⚑ v3p7_corrected_rows`. The re-pin is substrate, and nothing graded moved.
  **⚠ WARN-4 · the "nine graded vectors ROWSET `0e692765`" is not a re-derivable pin.** It is truncated to 8 hex, its law (which object, which serialisation) is stated in neither v1.10 nor v1.11, and it appears nowhere else in the repo. Under the pack's ROWSET law, the plain nine-vector list gives `0e826ee0…`. I found no reading among 192 candidate forms (object shape × `sort_keys` × separators × `ensure_ascii` × trailing newline) that gives `0e692765`. This conflicts with v1.11's own "every digest computed and filled by script" and with KP-101. **v1.12 must give the full 64-hex digest and its law, or drop the line** (the FILE pin plus the content identity verified here carry the row). *(Principle #4; Discipline #11.)*
- **§ A.3 / § A.4 (withdrawn rows; new rowsets).** Verified as above. The `_FALLBACK_HITS` ≠ FALLBACK-158 distinction is correct and well stated.
- **INFO (ledger, not prereg) · KP-153's "+881 rows" does not reconcile.** The rowsets it lists sum to 887. The member carries 891 with `w11`'s 4 (the prereg's 891 is right). The conductor should correct the ledger by corrigendum.
- **INFO (wording) · § A.1** lists eleven *model* members under the "Reference:" sentence.
- **⚠ WARN-5 · the R-11 arm row changed population inside v1.11 without a delta line.** v1.10's arm table had *"R-11 smoke (`H-6`): `M-POL-2` × salt 0 (v1.8 § F.2d's cell)"*. v1.11's has *"every cell the graded run emits"*. That is stricter and correct, since clause (c) binds per cell, and § F.2k.5 states it. But § 0's delta tables do not list it. v1.12 rewrites this area anyway. **It must keep the 25-cell population and list the change in § 0** (Discipline #12).

---

### 7 · § F.2k: not ruled. What v1.12 must NOT carry over

1. **The 4,500-term budget as operative, and the "STANDS" / "cannot fire" conclusions** (§ F.2k title, .4, .5, the header's ⚑ R-11 paragraph, § 0.2 `TA-X-07` row, § F.2 tolerance cell, § G.1 R-11 bullet, § H H-6, § G.3 `r11_budget.budget_terms: 4500, outcome: "STANDS"`, § J box 1's framing). The history (v1.5's `1e-12/eps`) may be kept as lineage.
2. **The § F.2k.2 code reading at `ffb454e`.** `kc2rt_fight.gd` has already moved (`e6903095…` → `41310e5e…` at `fae29ec`). Every line citation must be re-read at the **compensated** pass-3b digest and re-pinned.
3. **The recursive-summation bound (γ_{m−1})** as the governing bound. In the Neumaier re-derivation (Higham § 4.3), v1.12 must not repeat OQ-17 in a new form:
   - the bound is relative to **Σ|xᵢ|**, and § F.2k.3 itself concedes `voided` terms can be negative, so per-accumulator **absolute sums** must be emitted (or non-negativity shown per accumulator), not only term counts;
   - the final six-way sum in `conservation_residual` (γ₅) and the per-term split roundings (`c·u`) must appear in the bound explicitly. KP-155's scope (seven accumulators + two inner sums) does not name the six-way sum;
   - the antecedent of the re-derived clause (c) must be computable from emitted fields alone.
4. **The measured depths 6,616 / 6,539** (pass-3 runtime, port generator). These must be re-measured on the graded compensated runtime, all 25 cells.
5. **The "routing tension" paragraph (§ F.2k.6) as open.** KP-154 / KP-155 resolved it (Matt ruled Q92). Record it as resolved.
6. **OQ-17's "until then grade (c) as written".**

**v1.12 may carry from § F.2k:** the "What is NOT a derivation" box (the residual cannot rescue · no `u`-for-`eps` re-reading · no post-hoc √n), and § E's trap-12 addition. Both are principles, not budget-specific. **v1.12 should require** that drax's fail-first probe show compensation is live in GDScript by matching a Python Neumaier reference bit for bit on a constructed vector where naive summation errs.

---

## Rationale

Verdicts per item: **1 PASS** (WARN-1) · **2 PASS** (WARN-2; INFO-2, -3, -4) · **3 PASS on bounding** (WARN-3; INFO-5) · **4 OQ-15 PASS, OQ-17 PASS** (INFO-6) · **5 PASS** (WARN-4, WARN-5; two INFO). Nothing BLOCKs:
- no expected value, tolerance or declared set moved toward a measurement;
- the one expected-value move (`TA-X-18`) was read off the oracle before any graded run, and moves *against* the only port data;
- every arm citation reproduces off the pack;
- the precondition change is bounded and named.

Nothing ESCALATEs: no item needs a Matt ruling now. The only Matt-routed contingency is a future widening of `TA-X-26(b)` (KP-137).

**Overall verdict: PASS-WITH-WARN for everything v1.12 will carry from v1.11. § F.2k is not ruled.** H-7 for v1.12 stays owed **in part**: the § F.2k rewrite plus the v1.11 → v1.12 delta. The rest of v1.12 may cite this finding.

## Action

- [ ] **gamora (v1.12), MUST CHANGE:**
  1. **§ F.2k**: rewrite per KP-155, avoiding the six items of § 7. Carry its knock-ons in the header, § 0.2, § 0.5 item 1, § F.2 `TA-X-07`, § G.1's R-11 bullet, § H H-6, § G.3 `r11_budget` and § J.
  2. **OQ-17**: close it by the re-keying.
  3. **`TA-X-18`**: define "exact at repr precision" operationally (parse to float64, bit equality with the sign of zero, lossless emission or `UNGRADEABLE`) (WARN-1). CLOSE OQ-16 citing this finding.
  4. **§ B.1a**: partition `setup` into configuration rows versus tick-period-probe rows by id, and state the harness obligation for each (WARN-2).
  5. **G3**: define it in the prereg (instrument and pin, the scope of injected draws, the decision taxonomy, death-tick equality) or cite its pinned definition, and disambiguate it from the `Z5-LAW` "G3" (WARN-3).
  6. **`TA-X-09`**: give the nine-vector ROWSET in full 64-hex with its law, or drop it (WARN-4).
  7. **§ 0**: list R-11's population change (smoke cell → 25 cells) (WARN-5).
  8. **Godot read pins**: re-pin them at the compensated runtime digest.
- [ ] **gamora (v1.12), SHOULD (INFO):**
  - name `TA-X-11`'s population (INFO-2);
  - align or annotate `pet_special_gates` explicitness (INFO-3);
  - tie C1 to H-1's G3 evidence (INFO-4);
  - add the generator-by-law ceiling to § E.2 and the board-realisation note to § F.3a (INFO-5);
  - write OQ-15's tripwire (INFO-6);
  - fix the § A.1 wording.
- [ ] **gamora (v1.12), MAY CARRY VERBATIM:**
  - § 0.1 P-1…P-5;
  - the PINS tables (P-a … P-o, set digests, sealed cells, documents of record), re-filled by script as the standing rule requires;
  - § A.1–A.4;
  - § B.1, the § B.1a arm table and ROWSETs (with the `setup` partition added), the oracle figures table, § B.5 / B.5a, § B.6 (if the pack does not move);
  - § C.7;
  - § E (plus the new ceiling);
  - § F.2 rows other than `TA-X-07`, the `TA-X-18` value, § F.3, § F.3a (plus the note), § F.4, § F.5;
  - § G's taxonomy and § G.2;
  - § G.1's pass-3b bullet (with G3 defined);
  - H-1…H-5, H-7, H-8;
  - OQ-14, OQ-15;
  - § J boxes 2–3 and its "Carried" line.
- [ ] **drax:** in H-4, print `kc2rt_leech_table` `path_used` + `sha_measured` on the emission. Do not re-point the leech table to `IC7-F-44` before OQ-15 is resolved. Emit `TA-X-18` losslessly.
- [ ] **gandalf (conductor):** issue a corrigendum for KP-153's "+881 rows" (887 listed; 891 with `w11`).
- [ ] **Matt:** nothing now.

## References

- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.11.md` (FILE `312d71aa…`), `…-v1.10.md` (`b1dd68ef…`), `…-v1.9.md` (`b787308c…`), `…-v1.1.md` (`TA-X-18` origin, line 178)
- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`, rows KP-144 … KP-156
- `agentic_orchestration/gamora/notes/2026-09-21-kc2-play-ta-grade.md` (`TA-X-18` row 125); `2026-09-29-kc2-play-ta-grade-v1p7-attempt1.md` and `…-verdict-v1p7-attempt1.json` (`TA-X-11` W1-only; `TA-B-01` vs `[M-POL2]`; verdict STRUCTURAL)
- engine `src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/` (+ reference twin; the v3.7 and v3.6.1 packs for comparison); `kc2-v3p7p1-POST-bare-{M0,M-POL-2,M-POL-2-NULL,W1,W1-NULL}-20261001_021247.json`
- engine `src/reincarnated/simulation/kc2/spawn_structure.py:168-169, 311-333`; `control_application.py:117, 784-787`; `arena_fold.py:185-210, 442-443`
- collab `agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-aa-referent-spawn-structure/pm4aa_placement_law.json` (`55506b69…`, sole commit `b4a43cea8`)
- godot (git objects only): `kc2_runtime/loader/kc2rt_leech_table.gd:69-99` at `fae29ec`; `kc2_runtime/sim/kc2rt_fight.gd` at `ffb454e` (`e6903095…`) and `fae29ec` (`41310e5e…`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 12
