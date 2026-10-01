# Finding — 2026-10-01 — Run KC2-PLAY · T-A prereg v1.12 pre-read (H-7, partial: § F.2k and the v1.11 → v1.12 delta)

**Reviewer:** jack-ryan (DEV-MODE, gatekeeper for Run KC2-PLAY; conductor gandalf)
**Severity:** **BLOCK (scoped to attempt 1):** 1 BLOCK · 0 ESCALATE (1 conditional route in the pre-attempt list) · 2 WARN · 10 INFO. **v1.12 stands as the prereg of record.** The BLOCK does not invalidate it. It says attempt 1 must not fire until one completeness defect in (L1) is discharged, and there are two discharge paths, one of which needs no new prereg version.
**Target:** prereg v1.12, `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md`, collab `a6bce6f5c`, **FILE sha256 `a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854`** (I derived it before reading; it matches the brief). Predecessor v1.11 FILE `312d71aa…` ✓. My v1.11 pre-read FILE `b9fd0654…` ✓, which equals v1.12's pin.
**Developer:** gamora (author) · drax (port, booking fix in flight) · gandalf (conductor)
**Principles applied:** REVIEW_PROCESS #1 (math before code) · #4 (the committed record is the truth) · #5 (severity matters). Disciplines #11 (empirical inspection over assumption) · #12 (semantic-shifting fixes need explicit framing). ADR-002. Charter KP-155, KP-158, KP-167, KP-168.
**Scope, as briefed:** § F.2k (L0, L1, L2, the census), the v1.11 → v1.12 delta against my must-change list, § C.9 (G3), the § B.1a `setup` split, and the `TA-X-09` ROWSET. Everything else in v1.12 cites my v1.11 pre-read (`607f3b23f`). **I judge the law, not numbers.** Every measured value is PENDING (KP-167), and I read none as evidence.
**Read-before-result attestation:** no graded run exists under v1.12. I read godot only through git objects (`git show 933b438:<path>`, `git show 1211d71:<path>`, `git diff 933b438 1211d71`, `git grep 1211d71`). Nothing was checked out, run or written there. I read the engine pack and oracle source only by `open()`/`sed`, and executed nothing in the engine.

---

## What I found

### Re-derived pins (Discipline #11). All computed by me

| claim in v1.12 | how I checked | result |
|---|---|---|
| godot READ pins at `933b438`: `kc2rt_fight.gd` `2277cc89…`, `kc2rt_laws.gd` `c234376e…`, G3 oracle side `49a044ed…`, G3 port side `574facb3…` | `git show 933b438:<path> \| shasum -a 256` | all four ✓ |
| § F.2k.1 line citations (`:6448`, `:6471–6489`, `:6519`, `:6539`, `:6551–6553`, `:6557`, `:3425–3469`, `:5358`, `:5491–5508`; laws `:479–506`, `:520`) | read at `933b438` | all ✓ |
| `setup` partition: 8 C rows `207ab21f…`, 19 T rows `ab319772…`, whole job `c01d1dda…` | the rule applied by script over `a8` (459 rows), with the pack's ROWSET law | **8 / 19 / 0 unclassed** ✓, both ROWSETs ✓ |
| `TA-X-09` nine-vector ROWSET `0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78` | the five rules' `test_vectors`, in file order (2+2+1+2+2), with the pack law (`ensure_ascii` either way) | ✓, matches mine bit for bit. `math_rules.json` FILE `3b1e2d01…` ✓ |
| `TA-X-18` bits `0xc00fffffffffffde`, `0xbe9777a5cf72cec6` | `struct.pack(">d", …)` on the carried value | ✓ (hex-float `-0x1.fffffffffffdep+1`, `-0x1.777a5cf72cec6p-22`) |
| `pet_special_gates`: OMITTED on `IC7-A-0453`, EXPLICIT `None` on `IC7-A-0411`; the other four arguments explicit on both | read off `a8` | ✓ |
| every arm's `run_cell` passes `period_s` explicitly; the probe's `IC7-A-0458` does not | read off `a8` | ✓ (25 arm rows explicit, `0.0816326530612245`; `0458` omitted) |
| `1e-12/u = 9,007.199`; the first-order limit of 94,907 terms; depth-alone ≈ 5.2 × 10⁹; `Λ ≤ 5` ⇒ margin 1,801.4; the negative-mass limit N/\|O\| ≈ 1,500 | by hand | all ✓ |

---

### Item 1 · § F.2k, the Neumaier law

#### 1a · (L0): **PASS** (INFO-1)

- **The citation is correct.** Ogita, Rump and Oishi (2005), *Accurate Sum and Dot Product*, Proposition 4.5, is the error bound for `Sum2` (Algorithm 4.4): `|res − s| ≤ eps·|s| + γ²_{n−1}·Σ|pᵢ|`, given n·eps < 1. Their `eps` is 2⁻⁵³, which is this file's `u`, and the bound holds even with underflow. Using `u|S| ≤ u·A` to reach `(u + γ²_{n−1})·A` is valid.
- **It is correctly applied to drax's `|s| ≥ |x|` branch.** At `933b438:6474–6478`:
  - when `|sv| ≥ |x|`, the code computes `fl(fl(sv − t) + x)`. Since `fl(sv − t) = −fl(t − sv)` exactly, this equals FastTwoSum's `fl(x − fl(t − sv))`, which is exact because `|sv| ≥ |x|`;
  - the other branch is FastTwoSum with the operands swapped;
  - Knuth's TwoSum returns the same unique pair `(t, err)`;
  - `cv` accumulates `err` with plain rounded additions in the same order as `Sum2`'s σ, and `conservation[k] = t + cv` (`:6489`) is `Sum2`'s final `fl(π + σ)`.

  The `s = 0` start adds one step that is exact with zero error. **So "bit for bit with `Sum2`" is sound.**
- **INFO-1.** One immaterial exception: a leading `−0.0` term gives `+0.0` here and `−0.0` in `Sum2`. Only the sign of a zero partial sum differs, and the bound is unaffected.
- **The antecedents are correctly scoped.** The algebra assumes binary64, round-to-nearest, no FMA and no extended precision. H-6 (d)'s fail-first probe, which must match a Python Neumaier reference bit for bit on a vector where naive summation errs, is the right empirical check. It must be re-shown at the graded digest, as v1.12 says.
- **`Â` and `A⁺`.** Each `Â_k` is itself a Neumaier sum of exact terms `absf(x)` (`:6484–6486`), so `A ≤ Â / (1 − u − γ²_{n−1})` holds. The inner sums' `Σ|term|` are also Neumaier sums (`_neu(inner_*_abs, …)` at `:3426`, `:3460`, `:5359`). The rule "a zero-sum tick has only zero-magnitude terms" holds because the stream terms are non-negative by construction (`maxf(0, …)` factors). Adding zero is an exact no-op in Neumaier.

#### 1b · (L1), the composition: **⛔ BLOCK-1: two classes of fight-path rounding on every graded cell are not in `B`, and the `q_k > 0` indicator cannot reach the accumulators they land in**

**What (L1) gets right.** The composition is correct for what it lists. I re-derived the chain:

`|Ô − T̂| ≤ |Ŝ_O − S_O| + |D| + Σ_j|S_j − Ŝ_j| + |ΣŜ_j − T̂|`, with one `(1+u)` each for the subtraction and the division.

That reproduces `B` term for term:
- the seven accumulators;
- the six-way sum at `(u + γ²₅)·Σ(1 + u + γ²)·A_j`;
- `E_inner` for the two inner sums;
- `E_split` for flagged differences.

`conservation` is initialised with all seven keys (`933b438:5750`), so `sink_terms_present = 6` always holds. Using the total inner term count as `N_I` is conservative. The γ_{2f} for F(f) correctly covers *both* sides of an independently formed pair (`2γ_f/(1 − γ_f) = γ_{2f}` exactly).

**What it misses.** Every graded arm is ORACLE, and on ORACLE the loop layer and the counterplay layer are armed: `933b438:3883–3884`, `loop_layer_on = is_oracle`, `cp_on = is_oracle and …`. On that path, monster→player damage reaches the sinks through roundings that (L1) does not name and the runtime does not flag:

1. **The packet sum, plain recursive.** `_pkt_direct += applied` (`:5469`, once per direct row, unflagged). This is fight path: the oracle does `direct += m.applied`, and v1.12 must not compensate it.
2. **The packet total.** `dmg = _pkt_direct + _pkt_pcl` (`:4059`, `:4083`), and at arrival `float(p["direct"]) + 0.0 + pcl_eff` (`:4101–4103`). One rounding each, unflagged.
3. **The counterplay remainders.** In `_cp_absorb` (`:3942–3972`): `dmg -= cut` and `dmg -= taken`, up to four per packet and per DoT burn. Each is a rounded difference, and none is flagged. `counterplay_absorbed` is booked with `cut`/`taken`, and the rounded remainder flows on to `_land`.

The per-row `voided = mag − applied` (S) books against the **row's** `applied`, while `applied`/`pool_truncated` in `_land` (`:5507–5508`) book against the **packet float** that items 1–3 produced. The two do not telescope. The gap is items 1–3's rounding error.

**Why neither `E_inner` nor `E_split` absorbs it:**
- `E_inner` names exactly two sums: the stream sum and the PCL raw sum. The packet sum is neither.
- `E_split` charges `φ` only on accumulators with `q_k > 0`, and `q_k` is the runtime's `n_split_roundings_by_accumulator`. **At `933b438`, `applied` (`:2815`, `:3479`, `:5507`) and `counterplay_absorbed` (`:3949`, `:3970`) are never flagged**, so `q_applied = q_cp = 0`. Those two accumulators are the ones that receive most of the mis-formed mass. A census that honestly classes `:5507` as F(f) still sets only `φ`. It cannot switch on the indicator.
- **§ F.2k.3's PCL telescoping example cites `:5499`, the non-loop `_land(…, pcl, …)`.** On every graded cell, the PCL component instead takes `:5495–5498` into `_pkt_pcl` and then goes through items 2 and 3. So that example describes a path no graded cell takes. This is failure mode (i), a mis-read of the summation, which § F.2k invited me to check.

**Consequence.** As written, (L1) is not a guaranteed bound on the graded path. Its own § F.2k.7 names the failure: *"Dropping any rounding from `B` … repeats OQ-17 in a new form."* The OQ-17 closure (§ I), and the "(iii) lists every one" claim, fall with it. **This is a defect in the law's completeness, not a forecast that (L2) will fail.** The omitted terms have the same order as terms `B` already counts (a few `u` per packet step on the landed mass), and nothing here predicts a verdict. It is a BLOCK because:
- the prereg makes completeness its own standard;
- the fix is cheapest now, before any graded run, while D4 still holds;
- attempt 1 cannot fire before drax's fix and the census anyway, so the BLOCK costs no schedule.

**Discharge: either path, gamora's and gandalf's choice:**
- **Path A (recommended, cleanest for the record): a v1.13 corrigendum to (L1)/(N3), committed alone (D4).** Add the packet path as a named term. For example, `E_pkt = γ_{M_pkt} · A_pkt`, where:
  - `M_pkt` = the maximum over packets of (rows summed into `_pkt_direct` + the `+ pcl` add + the arrival re-add + the `_cp_absorb` remainder steps);
  - `A_pkt` = Σ over packets of (Σ|appliedᵢ| + |pcl|).

  Both are emitted, and both are emission only, so the fight path is untouched and G3 is unaffected. Then replace the `[q_k > 0]` indicator with a census-derived one: any S or F site in accumulator `k`. This change only enlarges `B`, so it tightens gradeability and needs no Matt route. Its H-7 is a one-clause delta read.
- **Path B (no new version): satisfy (L1) as written.** drax passes `split = true` at every booking that is F-class or an unflagged difference: `applied`/`pool_truncated` in `_land` when they are fed a packet or a counterplay remainder, and `counterplay_absorbed` in `_cp_absorb`. These flags are emission only. The census then classes the packet path F(f), with `f` statically bounded from the pack's rows per slot plus the fixed add and remainder steps, and with the sign premise stated (Σ|appliedᵢ| = |Σ appliedᵢ| needs appliedᵢ ≥ 0, or the bound must use Σ|appliedᵢ|). `φ = γ_{2f_max}`. The H-6 discharge note must record that the packet path is carried by census F(f) rows, so the record says how (L1) covers it. **My repair Gate-2 will verify that every accumulator receiving a non-T term has `q_k > 0` at the graded digest.**

#### 1c · (L2), the antecedent, and Matt's Q92 (a): **PASS** (WARN-2; INFO-2, INFO-3)

- **Retiring the budget rather than re-sizing it faithfully executes Q92 (a).** Matt ruled *"(a) Compensated sum"*, with the budget *"restated only as the derivation gives it"* (KP-155). The derivation gives no term budget: depth enters only through `γ²`, and depth alone reaches 1e-12 near 5.2 × 10⁹ terms on the reference case, which I confirmed. Any re-sized number would be a reference-case artefact presented as a law. Stating the condition over `(n, Σ|term|)` and evaluating `β` exactly is what the derivation produces.
- **This is not a post-hoc relaxation in the sense that binds us.**
  - Clause (a) stays at 1e-12, and no expected value moves.
  - (L2) has **no free constant**: `u`, the γ's and 1e-12 are all fixed.
  - The budget's premise, a plain running sum, became false by Matt's ruled method change, not by a measurement.
  - (L2) is also **stricter** than v1.11 in its inputs: all accumulators, Σ|term|, every operand lossless, plus the census.
- **WARN-2 (Discipline #12): § 0.2's sentence that both changes "can only produce `UNGRADEABLE`, never green" is one-sided.** Clause (c) never makes a row green directly, true. But the re-keying also **removes** `UNGRADEABLE` outcomes the old clause produced: on the pass-3b runtime, five cells had more than 4,500 offered terms (KP-167). Under v1.11 those cells were ungradeable by count. Under (L2) they become gradeable if `β ≤ 1e-12`, and clause (a) can then grade them green. That direction was authorised by Q92 (a), so it is legitimate, but it must be **named as a relaxation in that direction**, so Matt does not read v1.12 as tightening only. **No prereg change is needed.** State it in gamora's H-6 discharge note and in the conductor's next ledger row.
- **The first-order condition `Λ ≤ 9,007.2` is correct and correctly demoted.** It is printed, never graded, and the grader evaluates `β`.
- **INFO-2.** *"The grader evaluates `β` exactly."* In binary64, `β` carries its own rounding error, a few `u` relative. That only matters at the knife edge, but it makes "exactly" literal only if `β` is evaluated with exact rationals (Python `fractions.Fraction` over the emitted floats is enough) or with upward rounding. State the method in the H-6 note and the H-4 harness.
- **INFO-3.** § J says the law was *"written before the numbers it will judge."* That is true of the **graded** numbers. The pass-3b counts (953–6,777 offered; deepest sink 12,239) were on the ledger (KP-167) before v1.12 was written. Since (L2) has no free constant, that exposure cannot have bent it, but the record should say so rather than imply the author was blind to them.

#### 1d · The booking census as an antecedent: **PASS as a mechanism; WARN-1 on well-definedness and checkability**

**The mechanism is right.** Making the static half of the booking proof an antecedent means a missed class surfaces as `UNGRADEABLE`, never as a silent pass. The KP-167 hunt shows it working: drax's fix (godot `fd7bef4`, `1211d71`) books wave-end in-flight packets `dropped`, and halts on the **after-death popped packets**, which no named sink covers. Under (L2) item 2, a census that cannot certify closure leaves those nine cells `UNGRADEABLE`, so the attempt does not fire. That is the intended behaviour.

**⚠ WARN-1: as written, the census is not yet well defined or mechanically checkable:**
- **(a) A per-line class is ill-posed for helpers reached by several paths.** `_land` (`:5507–5508`) is reached from five callers with different formation histories (the direct path, the PCL at `:5499`, `_land_attack_packet`, `_defer_arrivals`, `_land_dying_packet`, and `_burn_dots` through `_cp_absorb`). `_ss_hit` and `_cp_absorb` have the same shape. One line cannot carry one class. Rows must be per (booking site × caller path), with `φ` the maximum.
- **(b) S is defined by the runtime flag**, so an unflagged single difference (`dmg -= cut`) has no class except F(1). That couples to BLOCK-1.
- **(c) Completeness must be checkable by machine, not by assertion.** That means a site list generated by `git grep -n '_cons_add(\|_offer('` at the graded digest, matched row for row.
- **(d) Closure must enumerate every terminal path:** landing, wave-end drain, the death `break`, caster-death VOID if armed, and `dropped` at the DoT wave-close.

**No prereg change is needed.** (L2) item 2 already makes the census a Gate-2 object. **These are my repair Gate-2 criteria for the census**, binding on H-6 (c).

---

### Item 2 · The v1.11 → v1.12 delta against my must-change list

My v1.11 list had **eight** MUST items. v1.12's header and PINS row call the godot re-pin "jack-ryan item 9", while its own § 0.6 maps it to must 8 (INFO-10, cosmetic).

| # | what I asked | v1.12 | verdict |
|---|---|---|---|
| 1 | rewrite § F.2k and its knock-ons, avoiding my § 7's six items | done: retired the 4,500 budget, retired the `ffb454e` reading and re-read at `933b438`, bounded Neumaier on Σ\|term\|, put the six-way sum and the split roundings in `B`, retired 6,616/6,539, resolved the routing tension, did not carry "grade as written", and requires the H-6 (d) probe. The header, § 0.2, § 0.5, § F.2, § G.1, § H, § G.3 and § J are consistent (every remaining `4,500` is lineage or retirement, checked by grep) | **DISCHARGED IN FORM; completeness fails, see BLOCK-1** |
| 2 | close OQ-17 by the re-keying | closed | **DISCHARGED, conditional on BLOCK-1** (the "all roundings" claim is the part BLOCK-1 falsifies) |
| 3 | make `TA-X-18` "exact" operational; close OQ-16 | § F.2l: bits with the sign of zero, a lossless emitter, else `UNGRADEABLE`; OQ-16 closed. Bits verified | **DISCHARGED** (INFO-5) |
| 4 | partition `setup` | § B.1a, 8 / 19 | **DISCHARGED**, re-derived (Item 4) |
| 5 | define G3; rename the `Z5-LAW` G3 | § C.9; `UPN5-G3`. It also corrects my citation: the row is § F.2h(b), not § F.2a(b). Accepted | **DISCHARGED** (Item 3) |
| 6 | give the `TA-X-09` ROWSET in full with its law, or drop it | given in full | **DISCHARGED**, verified (Item 5) |
| 7 | list R-11's population change in § 0 | § 0.2 | **DISCHARGED** |
| 8 | re-pin godot at the compensated runtime | `933b438` pinned as READ, not as graded; the graded re-pin is PENDING (H-6 (a)) | **CORRECTLY PENDING** (the READ pins verified) |
| INFO-1…6, § A.1 wording | — | § 0.6 maps each. INFO-2 (`TA-X-11`), INFO-3 (`pet_special_gates`, verified), INFO-4 (C1 by G3), INFO-5 (`C-p`, F.3a note), INFO-6 (the OQ-15 tripwire), § A.1 corrigendum | **ALL DISCHARGED** |

**INFO-5 (§ F.2l).** Clause (i) admits three lossless formats: CPython repr, ≥ 17 significant digits, or hex-float. Clause (ii) certifies only an emitter that *"reproduces `repr(x)`"*, so a lossless `%.17g` or hex-float emitter would read `UNGRADEABLE`. This is moot for drax's emitter (`91c8fe1` is CPython repr). Read (ii) as "round-trips bitwise for every vector" if the emitter ever changes.

---

### Item 3 · § C.9, G3: **PASS as the definition and as the sole fidelity precondition (taken together with G2 705/705)** (INFO-6, INFO-7, INFO-8)

- **The instrument matches the text.** At `933b438`, `kc2rt_g3_loop_trace.gd`'s decision classes (`:605`) are exactly the eight in § C.9.4. The isolation switches (`:232–317`) are exactly the eight in § C.9.3. Draw mismatches (`_serve`, kind/arguments/past-end) are rule (i). The `port streams with no oracle counterpart` line is rule (ii). The `ORACLE DRAWS … the port opened NO such stream` line is rule (iii).
- **The two declared oracle-only streams are scoped acceptably.** The spawn FACING stream is unread. The Fighting Spirit / Ulzaad rolls are outcome-inert (`cp_state` names them HALTED). Any effect they had would surface in the decision classes (`dmg_sources`, `wave_end`), which are exact.
- **The coverage gap is stated honestly.** Only `M-POL-2` and `W1` have G3 records, and H-1 owes the other three arms (§ C.9.6). Checking each oracle trace against its arm's POST figures is the right way to show the oracle side composed the arm as `a8` does.
- **Sufficiency.** G3 shows that the decisions are equal on the oracle's draws. NUMBERS never pass or fail, damage amounts are G2's domain, and the generator's realisation is `C-p`. The § G.1 bullets require G3 at 0 **and** G2 705/705, and together those are sufficient for what a fidelity precondition must carry here. As a definition, G3 is complete.
- **INFO-6.** At `933b438`, C.9.5's terminal-wave equality and "outcome `death` on both sides" are **printed** (`port terminal: …`), not counted. Only `wave_end` is a counted class, and a port that *cleared* at the oracle's death tick would pass `wave_end`. H-1's emission must **compute** § G.3's `g3.death` object (terminal reason, wave, k, `equal`), not read it off the printout.
- **INFO-7.** The draw rule compares kind, arguments and order, not the `(wave, k)` stamp, and a shared stream left partly unconsumed is not a divergence. Both would almost surely surface as decision divergences, and `TA-X-27(c)` grades consumption on the graded run. Recorded so nobody reads rule (i) as a timing check. Also, the `player_kit_residual.py:286|…` exception is a **seed wildcard**. Say "any seed at that site", or pin the seeds.
- **INFO-8.** C1-by-G3 (INFO-4) depends on the G3 tool and the graded harness configuring arms through the same entry point with the same arguments. They do: `configure_arm_from_pack` at `kc2rt_g3_loop_trace.gd:223` and `kc2rt_ta.gd:416`, with `aprons` forced off under ORACLE (`kc2rt_fight.gd:1234`). A digest of the resolved `arm_config`, emitted on both, would make that tie checkable rather than inferred.
- **INFO-9 (C.9.5).** *"`period_s = 1/12.25`"* is one ulp off the wire. The arms and the port clock use `0.0816326530612245` (`0x3fb4e5e0a72f053a`), and `1/12.25` is `0x3fb4e5e0a72f0539`. The seconds are display only, the decision is on `k`, and no verdict moves. Read `period_s` as the wire value.

---

### Item 4 · The § B.1a `setup` split rule: **PASS** (INFO-10)

- **The rule reproduces off the pack by script.** I classified each `setup` callee by its presence in the five fight jobs' own rows:
  - **8 absent everywhere (C):** `0435`, `0439`, `0446`, `0452`, `0453`, `0454`, `0455`, `0459`;
  - **19 present in all five (T):** `0433`, `0434`, `0436`–`0438`, `0440`–`0445`, `0447`–`0451`, `0456`, `0457`, `0458`;
  - **0 in some but not all.**

  ROWSETs C `207ab21f…` ✓, T `ab319772…` ✓, whole `c01d1dda…` ✓.
- **Independent corroboration.** The partition coincides with caller depth: every C row is called from `run_cells` or `make_runner`, and every T row from `run_cell`, its lambdas, `spawn_factory` or `_overrides.patched`. So the rule is not an artefact of callee naming.
- **"Configure no arm from T" is safe.** Every arm carries its own instance of each T callee, and every arm's `run_cell` passes `period_s` explicitly, so no arm reads the probe's output.
- **INFO-10.** The rule is not total in general. A callee present in *some* fight jobs would be unclassed. There are none in this pack, which does not move. Any future pack should halt on such a row rather than guess. Separately, v1.12's "jack-ryan item 9" means my must 8 (cosmetic).

---

### Item 5 · `TA-X-09`, the nine-vector ROWSET `0e826ee0…`: **PASS**

The full 64-hex digest `0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78` reproduces under the stated law, with `ensure_ascii` either way. The rows are `RULE-CHANNEL-MOVEMENT` 2 · `RELEASE-TYPE-A` 2 · `RELEASE-TYPE-B` 1 · `CAST-INTERRUPT-BINDING-EXCLUSIVITY` 2 · `DMG-APPLIED` 2, in file order. Leaving the sixth rule (`RULE-MONSTER-TO-PLAYER-MITIGATION-ORDER`) out of scope is correct: folding it in would be a row change under KP-137.

---

### Side observation for the census (INFO, drax)

On the non-bound PCL path (`933b438:5366–5370`), `pcl_reclaim` is booked with `reclaimed` while `offered` receives only `pcl_effective`. The sinks over-book by `reclaimed`. v1.12 says this path is reached only when PCL is unbound (pre-v3.5). The census must show it is unreachable on every graded arm (`pcl_answer_bound`), or class it.

---

## Rationale

- **Item 1a (L0): PASS.** The citation, the constant and the bit-for-bit equivalence all hold (INFO-1).
- **Item 1b (L1): BLOCK-1.** Discipline #11 and Principle #1: the law omits fight-path roundings that every graded cell executes. Those are the loop-layer packet sums and the counterplay remainders, `:3883` arms both on ORACLE, and they land in accumulators the `q_k > 0` indicator cannot reach. By the prereg's own § F.2k.7, that is OQ-17 in a new form.
- **Item 1c (L2): PASS.** The retirement is faithful to Q92 (a) and the antecedent has no free constant. WARN-2 is a Discipline #12 framing note. INFO-2 and INFO-3.
- **Item 1d (census): PASS as a mechanism.** WARN-1 sets well-definedness and checkability as Gate-2 criteria.
- **Item 2: 7 of 8 MUST items discharged, item 8 correctly PENDING, and items 1 and 2 conditional on BLOCK-1.** All INFO items are discharged.
- **Item 3 (G3): PASS** (INFO-6 to INFO-9).
- **Item 4 (`setup`): PASS** (INFO-10).
- **Item 5 (`TA-X-09`): PASS.**

No ESCALATE on v1.12 itself. Every fix enlarges `B` or tightens evidence, so none needs Matt. The one Matt-conditional item is a booking ruling on the runtime (pre-attempt item 2), not a defect in v1.12.

**Overall verdict: BLOCK (1), scoped to attempt 1.** v1.12 stands as the prereg of record for everything except (L1)'s completeness, and the rest of v1.12 may cite this finding and my v1.11 pre-read. **Attempt 1 does not fire until BLOCK-1 is discharged by Path A (a v1.13 corrigendum, D4, plus a one-clause H-7 delta read) or Path B (runtime flags plus census F(f) rows, verified at my repair Gate-2 and recorded in the H-6 note).**

## Action

**Must be settled before attempt 1 (in addition to v1.12 § G.1 / § H):**
1. **BLOCK-1**, by Path A or Path B (owners: gamora and gandalf choose; drax implements B's flags if chosen). If Path A, jack-ryan does the H-7 delta read of v1.13.
2. **The after-death popped packets have no sink.** drax halted at `1211d71`: there is no named sink, and the residual on nine cells equals these packets. I verified on the oracle that `deferred_arrival.py:378–380` `due()` **pops**, and that `run.py:3484–3485` `break`s on death, so **the oracle's own deferred-arrival identity books them nowhere either.** A faithful port therefore cannot close `TA-X-07` on those cells without a booking decision. Until there is one, the census cannot certify closure and (L2) item 2 keeps them `UNGRADEABLE`.
   - **gandalf rules.** A reading that maps them to an existing named sink (`dropped`, as the death-closes-the-wave sibling of V5-LIMB-3 and `drain_at_wave_end`, is the natural candidate) is a conductor ruling, recorded with Discipline #12 framing.
   - ⚑ **ESCALATE to Matt only if** the ruling changes what the identity counts: removing them from `offered`, a new sink, or a carve-out. That is a `TA-X-07` row change (KP-137), and it needs a dated prereg version.
3. **drax, H-6 (a)–(d) at the graded digest.** The census must meet WARN-1's criteria (a)–(d), and BLOCK-1's Path-B flags if Path B is chosen.
4. **drax, H-1: G3 on all five arms.** Extend the oracle-trace tool to `M0`, `M-POL-2-NULL` and `W1-NULL`. Compute `g3.death`, not print it (INFO-6).
5. **drax, H-4: re-pin the harness to the prereg of record** (v1.12, or v1.13 under Path A). Evaluate `β` exactly (INFO-2). Do not read the stale `4500` and `n_terms_note` labels (N8).
6. **gamora, the H-6 discharge note.** Evaluate (L2) per cell. Name the relaxation direction (WARN-2). State the `β` method (INFO-2) and the INFO-3 exposure fact. Under Path B, record how the packet path is carried.
7. **jack-ryan, the repair Gate-2** on the KP-167-fixed runtime and the census (R-7), applying WARN-1 and, under Path B, BLOCK-1's indicator check.

- [ ] **gamora / gandalf:** choose the BLOCK-1 path. Under Path A, file v1.13 alone (D4).
- [ ] **gandalf:** the after-death sink ruling. Route to Matt only under the condition in item 2.
- [ ] **drax:** items 3–5, plus the side observation on `:5366–5370`.
- [ ] **gamora:** item 6.
- [ ] **Matt:** nothing now, unless item 2's condition is met.

## References

- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md` (FILE `a0454776…`, collab `a6bce6f5c`); `…-v1.11.md` (`312d71aa…`)
- `agentic_orchestration/qa/findings/2026-10-01-kc2-play-prereg-v1.11-pre-read.md` (FILE `b9fd0654…`, collab `607f3b23f`)
- `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md`, rows KP-155, KP-158, KP-167, KP-168
- godot (git objects only), at `933b438`:
  - `kc2_runtime/sim/kc2rt_fight.gd`: `:3405–3486` streams; `:3742–3744`, `:3883–3884` loop and counterplay armed on ORACLE; `:3942–3972` `_cp_absorb`; `:4057–4113` packet landing and arrivals; `:4500–4530`, `:4570–4590`, `:4660–4705` DoT; `:5340–5370`, `:5440–5530` PCL, the packet, `_land`; `:6448–6560` the accumulators; `:5744–5751` reset
  - `kc2_runtime/sim/kc2rt_laws.gd:479–520`
  - `kc2_runtime/tools/kc2rt_g3_loop_trace.gd` (`:60–130`, `:223`, `:232–317`, `:357–392`, `:585–640`)
- godot at `1211d71`: the `fd7bef4`/`1211d71` diff (wave-end packets booked `dropped`; after-death packets halted); `kc2_runtime/tests/kc2rt_ta.gd:416`; `kc2rt_fight.gd:1234`, `:1251`
- engine pack `src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247/model/input_closure_v3p7p1.json` (`a8`), `model/math_rules.json` (`3b1e2d01…`)
- engine oracle `src/reincarnated/simulation/kc2/deferred_arrival.py:378–430, 485–505`; `run.py:3478–3492`
- Ogita, Rump, Oishi (2005), SIAM J. Sci. Comput. 26(6), Algorithm 4.4 and Proposition 4.5; Higham (2002), § 4.3
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`, §§ 11, 12
