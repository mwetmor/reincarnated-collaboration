# Gate-2 (DEV-MODE) — KC2-SIM Phase C seam work — 2026-08-08

**Reviewer:** jack-ryan (BLOCK authority)
**Commission:** gandalf `RUN-CONDUCTOR`, KC2-SIM charter § 3 G-C condition
(*"gamora tests green + jack-ryan Gate-2 PASS on the seam work"*)
**Target:** engine `~/Games/reincarnated-engine` @ HEAD `874302d5`
**Review surface:** gamora `8b0d6b5c · 9d44b00b · 409ce8a6 · 9ebc3ca1 · c5f9f74b · 874302d5` ·
star-lord `68e2e372` (tag `star-lord/v1.87-kc2-baton-v1-emitter-1`)
**Reviewed against:** battle spec `2026-08-08-kc2-sim-battle-spec.md` §§ 1–3, 5–6, 9–14 · charter
§§ 4.2 / 4.3 / 4.7 · ledger L-30 / L-31 / L-32 · both build reports · engineering disciplines
**Commit state:** NONE. Conductor commits the unit at gate close (charter § 4.7).

---

## VERDICTS

| Seam | Verdict |
|---|---|
| **gamora** (`simulation/`) | **BLOCK** — 1 BLOCK · 4 WARN · 4 INFO |
| **star-lord** (`export/`) | **PASS-with-findings** — 0 BLOCK · 2 WARN · 3 INFO |

**G-C is NOT MET.** Its first limb ("gamora tests green") is false at the blast-radius boundary
the seam itself defined: one pre-existing guardrail assertion that was **green at launch HEAD
`ebf13240` is red at `874302d5`**, was not amended, and is not declared. The fix is one assertion
using a pattern this same lap applied correctly four times. Everything else on both seams is
sound, and on the run's hardest rule — charter § 4.2, no free parameters, no fitted constants —
**both seams hold, including under adversarial reading.**

---

## § 1 — What I verified independently (method note, because it changes one claim's grade)

`reincarnated` is installed **editable via `.pth`** pointing at `~/Games/reincarnated-engine/src`.
A `git worktree` checkout at `ebf13240` therefore **imports HEAD source**, and a baseline taken
that way is worthless. My first pass was contaminated by exactly this and is discarded. Every
"pre-existing at `ebf13240`" statement below was re-taken with
`PYTHONPATH=<worktree>/src python3 -m pytest`, which the `.pth` mechanism does honour (verified:
`VALID_SHAPES` reads 7 values under the override, 8 without it).

gamora's own `git stash`-and-rerun method is **sound** — it reverts the tree the editable install
points at. This note records the hazard because the next agent to reach for a worktree baseline on
this repo will get a silent false green.

| Check | Method | Result |
|---|---|---|
| vendored CSV byte-truth | `cmp` ×6 vs `legolas/scratch/…` | **6/6 BYTE-IDENTICAL** |
| KC2 + baton suites | `pytest` | **113 passed** (78 + 35), matches both reports |
| guardrail amendments | `git diff ebf13240 874302d5` on the 3 amended files | retention limb intact + named-additions limb on all 4 cells |
| declared nova failures | worktree @ `ebf13240`, PYTHONPATH-correct | **pre-existing, test-ID for test-ID** ✓ |
| declared `kit_space_emitter` failures | same | **pre-existing, test-ID for test-ID** ✓ |
| seam boundaries | `git show --name-only` ×7 | **clean**; gamora ⊂ `simulation/` + `tests/` + `data/kc2/`, star-lord ⊂ `export/` + `tests/` |
| blast radius @ HEAD | `pytest -k "telegraph or spatial or encounter_ai or wr3 or br2 or export or migration or bundle"` | **4,594 passed / 5 failed** → 4 pre-existing, **1 NEW** (§ 2) |
| production consumers of the grown value-sets | `grep -rn VALID_SHAPES\|VALID_FAMILIES src/` | only `spatial_telemetry.py` itself — growth genuinely additive, `src/`-side risk nil |
| star-lord adjacent export suites | `pytest` | **177 passed** |
| tag → commit | `git rev-list -n1` | `star-lord/v1.87-kc2-baton-v1-emitter-1` → `68e2e372` ✓ |
| § 9.5 disclosure verbatimness | byte-compare spec ↔ both seams | both byte-exact, **scopes differ** (§ 4, S-W1) |

---

## § 2 — BLOCK

### **G-B1 — a fifth guardrail on the grown value-set was not amended, and it is red at HEAD**

**Severity: BLOCK.** **Traces to:** BR-2's own INVERT-DON'T-DELETE rule (invoked correctly four
times in `8b0d6b5c`) · Discipline #2 (smoke test / blast radius) · charter § 3 G-C limb 1.

```
tests/test_wr3_kite_commit_stage2b.py:357
  test_rect_is_a_valid_shape_and_the_enum_grew_deliberately

    assert TelegraphSpec.VALID_SHAPES == frozenset(
        {"circle", "cone", "line", "point", "rect", "trapezoid", "star"})

  @ ebf13240 (PYTHONPATH-isolated):  1 failed*, 37 passed  → this test PASSES
  @ 874302d5:                        FAILED — "Extra items in the left set: 'disc'"
```

\* the one failure at `ebf13240` in that file is a *different* test; this assertion was green.

**What it is.** `VALID_SHAPES` / `VALID_FAMILIES` carry **15 assertions across 5 test files**
(full census below). Four files were amended. `test_wr3_kite_commit_stage2b.py` was not — it was
outside the 7-file blast-radius selection, and a grep on the value-set names rather than a
file-list selection would have caught it.

```
tests/test_br2_resolve_truth_1.py       :135 :137 :139 :140 :153 :154   AMENDED ✓
tests/test_br2_trace_stage_1.py         :417 :418 :427 :428             AMENDED ✓
tests/test_wr3_stage2c.py               :418 :423 :424                  AMENDED ✓
tests/test_wr3_kite_commit_stage2b.py   :351 :357                       ⚑ NOT AMENDED — :357 RED
```

**Why this is BLOCK and not WARN.** gamora's report § 8 anticipated a surfacing and pre-classified
it as *"a finding about the growth, not a defect in the mechanisms."* That framing is right for a
downstream **consumer** enumerating without a default arm (the D-F4 action MIGRATION § 0 puts on
consumers). It is **not** right here: this is a **scope guardrail of the same class as the four
that were amended**, on the same two frozensets, and BR-2's own rule governs it. The test's own
docstring states the contract — *"The growth is pinned so it cannot be unnoticed."* The tripwire
worked; nobody looked. Leaving it red would also make the *next* growth's diff read as if only
four cells ever fenced this set.

**Action — developer (gamora), one assertion:** amend `:357` on the pattern already used four
times — keep the retention limb, add the named-additions limb:

```python
assert frozenset({"circle","cone","line","point","rect","trapezoid","star"}) <= TelegraphSpec.VALID_SHAPES
assert TelegraphSpec.VALID_SHAPES - frozenset(
    {"circle","cone","line","point","rect","trapezoid","star"}) == frozenset({"disc"})
```

with the same in-diff reason the other four carry. Re-run the blast radius. **Recommended
addition:** make the census mechanical — one test asserting the exact membership of both
frozensets *in one place*, so the fifth-file problem cannot recur.

**No BLOCK-class item was found on the star-lord seam.**

---

## § 3 — gamora seam — WARN

### **G-W1 — the t20 board's `values-pending` status is recorded NOWHERE in the seam**

**Severity: WARN.** **Traces to:** L-30(b) / spec § 6.2b / § 13 HALT-10 / § 12 T-8 · charter § 4.2 ·
Discipline #9 (attribution clarity).

```
grep -rn "F-7|L-30|values-pending" src/reincarnated/simulation/kc2/ \
     src/reincarnated/simulation/math/kc2-mechanism-stack-2026-08-08.md tests/test_kc2_*.py
→ (no output)
```

The conductor's ruling is explicit: *"`t20_wave160_board_ehp.csv` is mechanism-correct,
**values-pending**; … gamora's mechanism build consumes t20 unblocked … calibration consumes the
revision."* The engine now vendors that CSV at `data/kc2/t20_wave160_board_ehp.csv`
(SHA `01160fd0…`, the **pre-revision** emission) with **no in-repo marker** that its record→form
assignments are falsified for at least Zantarin, Archmage Aleksander and the applied hero band.
`load_wave160_board()` and `BoardEntry` carry no grade field; `opposition.py` mentions neither
F-7 nor L-30.

This is the one place where the package departs from its own stated discipline —
`fixture.py`'s header rule, *"THE PROVENANCE RIDES ON THE VALUE, NOT IN A COMMENT."* Every scalar
constant is a `Cited` with a grade; the single largest data dependency in the package (~9.4 M eHP
of opposition) has none, and its known-falsified status is invisible to a Phase-D consumer or to
the baton provenance.

**Action — developer:** (a) carry the grade on the loader (`BoardEntry.values_grade =
"VALUES-PENDING (F-7, L-30(b))"` or equivalent) so it can ride into provenance; (b) **pin the
vendored SHA in a test** with the comment *"bump when the F-7 revision lands"* — that converts a
silent staleness at G-D into a loud failure. Cost: one constant, one assertion.

### **G-W2 — a live test pins a ruling that L-30(c) struck**

**Severity: WARN.** **Traces to:** L-30(c) · spec § 6.2b · Discipline #12 (declare semantic shifts).

```
src/.../kc2/opposition.py:94   def kubacabra_phase_chain(...)
    """⚑ KUBACABRA IS THREE-PHASE AND THE SIM NEEDS ALL THREE (L-29). …"""
tests/test_kc2_opposition_wave_engine.py:67
    def test_kubacabra_is_three_phase_and_the_sim_carries_all_three():
```

Spec § 6.2b as it stands: *"the chain is **FALSIFIED ON CAMERA**, L-30(c) … **The sim models P1
ONLY** = 2,955,796 MEASURED; P2/P3 **declared-unmanifested**."* Lap 3's commit message likewise
says *"Kubacabra's 3-phase chain … **is carried**."*

**Behaviourally inert** — nothing in `run.py` calls `kubacabra_phase_chain()`, and the board loader
reads P1 from the CSV, so the *modelled* quantity already matches L-30. The defect is that code
and a test now **assert a superseded ruling as current**, and the test would make a future
L-30-compliant correction look like a deletion. Most plausible cause: gamora built § 6 against the
pre-L-30 spec text (the spec is uncommitted per charter § 4.7, so I cannot diff it) — the remedy is
a citation refresh, not a rebuild.

**Action — developer:** re-scope the docstring and the test to the true claim — *the DB wiring
carries three bios; the SIM models P1 only (L-30(c), P2/P3 declared-unmanifested)* — and add the
assertion that no P2/P3 body enters a roll, which is the fact worth pinning.

### **G-W3 — AC-6.1 / AC-6.2 / AC-6.3 are reported PASS on prose, not on tests**

**Severity: WARN.** **Traces to:** Discipline #2 · REVIEW_PROCESS principle "smoke-gate" ·
the seam's own rule (`devotion.py` header: *"an absence nobody can test is indistinguishable from
an oversight"*).

The report's § 6 acceptance table marks all five § 6 ACs **PASS**. Executable coverage:

| AC | Test | State |
|---|---|---|
| AC-6.1 subset-of-roster, weighted as emitted | — | evidence is a code-structure statement |
| AC-6.2 body count reproduces § 10.5 **to the integer, all 20 waves** | — | cross-referenced to AC-10.4, which asserts a **20-wave aggregate expectation** |
| AC-6.3 concurrent bosses **not capped** | — | prose: *"no concurrency cap exists in the model"* |
| AC-6.4 | `test_AC_6_4_…` | ✓ |
| AC-6.5 (+ multiplicative guard, + p04 band) | `test_AC_6_5_…` ×3 | ✓ |

AC-6.2's predicate is per-wave-to-the-integer; an aggregate can be right while a per-wave count is
wrong — and E-3 (wave-160 modified count 8 vs spec `≤ 7`) is precisely a per-wave discrepancy, so
this is not hypothetical. AC-6.3 is an *absence*, and this seam makes every other absence testable
(AC-9.1, AC-9.3, the rank-HP-term ban, AC-11.5). The module header also claims
*"Spec ACs: § 6.4 (AC-6.1…6.5)"* — a coverage claim over a range it does not deliver.

**Action — developer:** either add the three tests (AC-6.3 is two lines: assert no
concurrency-cap constant exists and that a roll can place ≥3 bosses), or **re-grade the report
table** to `PASS-BY-INSPECTION` / `NOT-TESTED` and correct the module header. Either is acceptable;
silently claiming PASS is not.

### **G-W4 — `IGNORE_GAME_BALANCE` is the one load-bearing value-set carried without provenance on the value**

**Severity: WARN.** **Traces to:** charter § 4.2 · `fixture.py`'s own header discipline ·
E-2 (conductor-ruled, citation probe in flight).

`wave_engine.py:89–97` carries the E-2 declared override as a bare `dict[str, bool]` with code
comments — *"field absent → additives"*, *"False (explicit)"* — while every other constant in the
package is a `Cited(value, cite, grade)`. Those per-record `False` entries read as DB reads but are
sourced from spec § 10.8's table, not from the emission (which carries no such column — that is
E-2's whole point). This is the value-set that decides AC-10.3 and moves AC-10.4 by exactly 4.0
bodies.

The *behaviour* is § 4.2-honest and the conductor has ruled it so: the override is declared, the
default is declared, and `WaveRoll.pools_on_default_exemption` counts how many rows ran on the
default. The finding is narrower: **the grade is not on the value**, so a reader (or the baton
provenance) cannot tell a DB-CITED entry from a spec-declared one.

**Action — developer:** wrap the six entries as `Cited(..., "spec §10.8", "DECLARED-OVERRIDE")`
(the grade vocabulary already exists in `fixture.VALID_GRADES` and can take one addition), so the
E-2 probe's return can be applied by grade rather than by memory.

---

## § 4 — star-lord seam — WARN

### **S-W1 — the two seams hold two different scopes of "the § 9.5 block verbatim"**

**Severity: WARN.** **Traces to:** CD-5 (RATIFIED, L-31) · AC-11.4h · AC-9.2.

Measured, byte-for-byte:

```
schema.DEVOTION_ENVELOPE_DISCLOSURE   == spec § 9.5 VALUE          → True   (CD-5 correct)
devotion.ENVELOPE_DISCLOSURE          == spec § 9.5 VALUE          → False
devotion.ENVELOPE_DISCLOSURE          == "devotion_envelope_disclosure:\n" + VALUE → True
devotion.ENVELOPE_DISCLOSURE[1:]      == schema.DEVOTION_ENVELOPE_DISCLOSURE       → True
```

Both are byte-exact against the spec; they differ by **one line of scope**. CD-5 ruled *"the
block's leading register-key line IS the wire key, not part of the value."* star-lord implements
that. gamora's constant **includes** the key line, and `run.out_of_model_manifest()` places it
under a dict key of the same name — i.e. the key would appear twice, once as the wire key and once
inside the value. Today the emitter defaults to its own constant, so nothing is broken **on the
emit path**; the exposure is at **Phase-D wiring**, where routing the sim's manifest into
provenance fails AC-11.4h.

**Action — developer (gamora, one-line):** split the constant —
`ENVELOPE_DISCLOSURE_KEY = "devotion_envelope_disclosure:"` +
`ENVELOPE_DISCLOSURE = <value only>` — matching CD-5 and star-lord.
**Action — developer (star-lord):** at Phase-D wiring, assert
`sim_manifest["devotion_envelope_disclosure"] == schema.DEVOTION_ENVELOPE_DISCLOSURE` so the seam
join is checked rather than assumed.

### **S-W2 — the only verbatimness guard silently skips when the meta-repo is absent**

**Severity: WARN.** **Traces to:** Discipline #2 · Discipline #9 · AC-9.2 / AC-11.4h.

```python
tests/test_baton_v1.py:134
def test_ac_11_4h_devotion_block_is_the_spec_text_verbatim():
    if not SPEC_NOTE.exists():
        pytest.skip("collaboration repo not present")
```

`SPEC_NOTE` is `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/…`. The
re-extraction-and-byte-compare design is *excellent* (Discipline #9 — the assertion is sourced,
not transcribed). But it is the **sole** enforcement of AC-11.4h/AC-9.2, and on any host without
the meta-repo a MUST becomes a no-op with no signal.

**Action — developer:** keep the cross-repo comparison, and add an **in-repo** pin that always
runs (assert the constant against a checked-in golden, or against `simulation.kc2.devotion`'s
value once S-W1 aligns them). Alternatively make the skip loud (`xfail(strict=False)` + a warning).

---

## § 5 — INFO (record, no action gate)

| # | Seam | Observation |
|---|---|---|
| **G-I1** | gamora | AC-10.4's *"63.0 expected champions"* is reproduced **EXACTLY on the p06-OFF limb only** — measured: p06 OFF → regulars 286.83 / champions **63.00**; p06 ON → regulars 306.83 / champions **81.00**. § 10.5 fact 5 pairs 63.0 with 292 regulars, i.e. p06-OFF, so the code's reading is defensible — but the fixture ran **p06 = ON** (L-21), and `test_AC_10_4b` asserts `champ_on == 81.0` against **no pinned target**. L-32(d)'s ratification of E-4 leans on *"reproduces the pinned 63.0 EXACTLY"* without stating the p06 scope. **Conductor may wish to** scope the 63.0 pin, or pin an 81.0 p06-ON figure. |
| **G-I2** | gamora | `run.py:173` hard-codes Tip-the-Scales leech uptime at **1.0** (`income_per_tick = (regen + leech_per_s_while_up) * period`) — not a `simulate_wave` parameter. Consistent with § 3.1's *"near-continuous"* and with E-1's non-stacking ruling, but uptime is an **opposition-model-dependent** quantity (§ 9.2(b) error-bar class) entering the harness undeclared. `EnergyModel.run_channel` correctly exposes `leech_uptime`; the harness does not. |
| **G-I3** | gamora | Math note § D.3 still reads *"the spec does not adjudicate"* on E-1; **L-32(a) RULED non-stacking**. The code matches the ruling; the note's currency lags. Same class as G-W2. |
| **G-I4** | — | A **third** pre-existing failure exists at `ebf13240` beyond the two declared to me: `test_wr1_m12_gd_mitigation_nova.py::test_INTEGRATION_the_nova_fires_telegraphs_and_lands_a_death2_class_blow`. Already on record — `simulation/AGENT_STATE.md` SESSION 102 names the `28eddef4`-era set as **2 + 1 + 4 = 7**. Declared-item list to Gate-2 said 6. No action; recorded so the conductor's milestone full-suite baseline is 7, not 6. |
| **S-I1** | star-lord | The ADR-006 AST guard scans `emitter`, `schema`, `stub` — **not** `baton_v1_validator.py` / `baton_v1_fixture.py` — while MIGRATION claims *"writes NO row … and no row anywhere else."* Two module names added to the tuple closes the gap. |
| **S-I2** | star-lord | Measured `rows-compact` MID = **17.4 MB** supersedes spec § 11.6.1's DERIVED *"roughly 9–12 MB"*. Still inside drax's ≈22 MB sign, so the signature holds and Discipline #10 was honoured (measured, not assumed) — but the spec row should carry the **measured** figure so a later reader does not plan against 9–12. |
| **S-I3** | star-lord | `68e2e372` carries **no `Co-Authored-By` trailer**; all six gamora commits do. Repo commit convention. |

---

## § 6 — What I checked hardest, and found clean (the positive record)

**Charter § 4.2 — no free parameters, no fitted constants. HELD ON BOTH SEAMS.** This is the run's
hardest rule and I read it adversarially.

- Every scalar in `kc2/` is a `Cited(value, cite, grade)`; the grade vocabulary distinguishes
  `DB-CITED` / `MEASURED` / `DERIVED` / `CLIENT-VERBATIM` / `INFERRED` /
  `MEASURED-EXACT-SOURCE-UNLOCATED` / `DECLARED-FREE-PARAMETER`. The two genuinely free values
  (`v_ref`, HALT-2; `contact_distance_m`, § 9.5 piloting class) are **graded as such and named in
  `out_of_model_manifest()`** — they are parameters, not epsilons.
- **AC-10.4's p06-ON limb is pinned AS A MISS** —
  `test_AC_10_4b_p06_on_MISSES_316_5_and_that_is_FINDING_E_2_not_a_tuning_target` asserts
  `306.83`, asserts `|306.83 − 316.5| > 1.9 %` ("the miss is real and must stay visible"), and adds
  a **sensitivity limb** proving the exemption table costs exactly 4.0 bodies. The miss **cannot be
  silently closed** without deleting a test that says so in its own name. This is the single best
  piece of § 4.2 evidence in the unit and I confirm it holds as declared. **The AC-10.4 miss stays
  a miss.**
- **E-5/F-8:** `SoulfireCostTerm(effective_per_s=0.0, grade="UNADJUDICATED")` with the
  admissibility bound exposed as a *function*, never folded into `drain_rate_per_s`. Correct
  handling of an over-constrained system.
- **E-6:** `compose_damage_basis()` explicitly declares it does not target the sheet band;
  `SHEET_EOR_DAMAGE_PER_HIT` is carried as a comparison. No coefficient introduced.
- **AC-6.5's structural guard** implements the *wrong* (multiplicative) build on purpose so the
  test can prove it fails at ×2.86 / ~5,700× tolerance. Falsifiability built in.
- `test_the_rank_HP_term_ban_is_executable` greps the module's own source for rank-keyed HP
  constants — a fit-prevention guard that runs.

**Math-before-code (Discipline #1) — HELD.** The 495-line math note lands in `8b0d6b5c`, the
first lap. **§ D.3a is the honest correction the commission asked me to check**: it is amended
**in place**, labelled *"written after the code ran (the note is amended, not silently edited)"*,
and names the self-caught defect — a 10 Hz sampler aliasing against a 12.25 Hz tick grid, caught
*because the test compared against the closed form rather than the integrator's own output*. The
discipline working, and correctly recorded. Closed form 69.51 s vs model 69.63 s (0.12 s).

**Guardrail amendments (the 4 that were found) — CORRECT.** Each keeps the retention limb verbatim
and adds a named-additions limb with the reason in the diff. This is the right pattern; G-B1 is
that it was applied four times instead of five.

**Vendored data — BYTE-TRUE.** `cmp` on all six against `legolas/scratch/…`: identical. SHAs in
the report match.

**Seam boundaries — CLEAN.** gamora ⊂ `simulation/` + `tests/` + `data/kc2/` (the
`spatial_gauntlet/spatial_telemetry.py` telegraph growth is in-seam); star-lord ⊂ `export/` +
`tests/`. No cross-seam edits in either direction.

**Cross-seam schema change → MIGRATION.md (ADR-004) — SATISFIED BOTH SIDES.** `export/MIGRATION.md`
carries the baton entry at the top in the current style with the **explicit ADR-006 answer** and the
**by-name drop list** (`damage_taken`, `skill_type`, `recovery_source`, `schema_version`) — AC-11.8
satisfied on inspection (untested; INFO-grade only). `simulation/MIGRATION.md` carries the
value-set growth with the D-F4 default-arm action on consumers.

**Coverage proven by reconstruction, not assertion (charter § 4.3) — HELD.**
`baton_v1_stub_consumer.py` imports **nothing** from `reincarnated` (verified: only `math`,
`collections.abc`, `dataclasses`, `typing`). The G-E bar is a genuine external reconstruction.

**ADR-006 — enforced structurally.** `test_adr_006_no_external_db_write` walks the AST for
forbidden imports and calls rather than grepping strings, so the module can *document* the answer
without tripping its own guard. Correct design (see S-I1 for the one scope gap).

---

## § 7 — Action list

| # | Sev | Owner | Action |
|---|---|---|---|
| **G-B1** | **BLOCK** | gamora | Amend `test_wr3_kite_commit_stage2b.py:357` on the four-times-used pattern; re-run blast radius. Recommended: one mechanical membership test so the census cannot fragment again. |
| G-W1 | WARN | gamora | Carry the F-7 `VALUES-PENDING` grade on the board loader; **pin the vendored t20 SHA in a test** so a missed re-vendor fails loudly before G-D. |
| G-W2 | WARN | gamora | Re-scope `kubacabra_phase_chain` docstring + its test to L-30(c) (sim models P1 only). |
| G-W3 | WARN | gamora | Add tests for AC-6.1 / 6.2 / 6.3 **or** re-grade the report table and the module header. |
| G-W4 | WARN | gamora | Wrap `IGNORE_GAME_BALANCE` entries as graded `Cited` values so E-2's return can be applied by grade. |
| S-W1 | WARN | gamora + star-lord | Align the § 9.5 block scope on CD-5 (key line is the wire key); assert the seam join at Phase-D wiring. |
| S-W2 | WARN | star-lord | Add an always-running in-repo pin behind the skippable cross-repo verbatim check. |
| S-I1 | INFO | star-lord | Extend the ADR-006 AST scan to `validator` + `fixture`. |
| S-I2 | INFO | conductor | Update spec § 11.6.1's 9–12 MB recomposition to the measured 17.4 MB. |
| G-I1 | INFO | conductor | Scope AC-10.4's 63.0 champion pin to p06-OFF, or pin the p06-ON figure. |
| G-I4 | INFO | conductor | Milestone full-suite baseline at `ebf13240` is **7** pre-existing failures (2 nova-telegraph + 1 wr1_m12 + 4 kit_space_emitter), not 6. |

**Re-review scope on resubmission:** G-B1 only. The WARNs do not gate G-C on my authority — they
are the conductor's to sequence against G-D. If the conductor elects to carry any WARN into Phase D
unresolved, **G-W1 is the one I would not carry**, because it is the only finding whose failure
mode is silent at the gate that consumes it.

---

**Signed:** jack-ryan, Gate-2 DEV-MODE, 2026-08-08.
*The work is disciplined and the hardest rule held under adversarial reading. One tripwire fired and
nobody was standing where it went off — which is the only reason this is a BLOCK and not a PASS.*

---
---

# § 8 — RE-REVIEW ON RESUBMISSION — 2026-08-08 — **G-B1 CLEARED, PASS**

**Reviewer:** jack-ryan (Gate-2 DEV-MODE, re-review)
**Commission:** gandalf `RUN-CONDUCTOR`, KC2-SIM Phase C fix cycle
**Scope:** **G-B1 only**, per § 7's re-review clause. Nothing else re-opened.
**Target:** engine `~/Games/reincarnated-engine` @ `bae60ce6` (base `874302d5`), branch `main`, not pushed
**Developer:** gamora · report `gamora/notes/2026-08-08-kc2-gb1-fix-report.md`
**Commit state:** NONE written in the engine repo by me. This note is uncommitted; it rides the
conductor's G-C gate-close unit.

## § 8.1 — VERDICT

> ### **G-B1 — REMEDIATION PASS.** The BLOCK is lifted.

**gamora's seam verdict moves BLOCK → PASS-with-findings** on the G-C limb-1 question
(*"gamora tests green"*). The four WARNs (G-W1…G-W4) and the INFOs stand **unchanged and
unre-opened** — they never gated G-C on my authority (§ 7) and they ride their assigned laps. G-W1's
absence from this diff is **per the conductor's ledger L-34(d)** ruling that it rides the G-D
r2-consumption wiring; it is **not** re-flagged here.

Every count in gamora's report reproduced **exactly** on my own instruments. Nothing in the diff
falls outside the two test files. No G-D work and no WARN-scope work is smuggled in.

## § 8.2 — Independent verification, measured not accepted

Method: `PYTHONPATH=<tree>/src python3 -m pytest`, per this note's own § 1 isolation rule. Isolation
re-self-checked before use — `VALID_SHAPES` reads **7** under the `ebf13240` override and **8**
without it, so the override is live.

| # | Check | Method | Result |
|---|---|---|---|
| 1 | Diff scope | `git diff --name-status 874302d5 bae60ce6` | **2 files, both tests** — `test_wr3_kite_commit_stage2b.py` **M** (+12/−2), `test_telegraph_value_set_census.py` **A** (88 lines). Matches her § 2 table exactly. |
| 2 | No `src/` or `data/` touched | `git diff --name-only … -- src/ data/` | **empty** |
| 3 | No WARN/G-D work smuggled | `git diff … \| grep -icE "kubacabra\|IGNORE_GAME_BALANCE\|values.pending\|BoardEntry\|AC_6_\|ENVELOPE_DISCLOSURE"` | **0** |
| 4 | Amended assertion == § 2 prescription | byte-compare | **token-for-token identical**, differing only in line-wrap. Retention limb `⊆`, named-additions limb `− … == {"disc"}`. ✓ |
| 5 | In-diff reason present + stacked | read `:357–369` | New `⚑ AMENDED, NOT DELETED` block sits **below** the pre-existing BR-2 block, which is untouched. Two successive recorded crossings, not one rewritten claim. ✓ |
| 6 | Census pins **exact** membership, both sets | read + run | Cell 1 `VALID_SHAPES == EXPECTED_SHAPES` (8), cell 2 `VALID_FAMILIES == EXPECTED_FAMILIES` (5), cell 3 never-REMOVED (`⊆`, both sets). ✓ |
| 7 | Census literals == source of truth | `spatial_telemetry.py:451,:512` | `VALID_FAMILIES` 5 values, `VALID_SHAPES` 8 values — **exact match** to the census literals. ✓ |
| 8 | 5 census files @ `874302d5` | worktree, isolated | **1 failed / 138 passed** ✓ (matches) |
| 9 | 5 census files + new @ `bae60ce6` | isolated | **142 passed / 0 failed** ✓ (matches) |
| 10 | kite file alone @ `874302d5` | worktree, isolated | **1 failed / 37 passed** ✓ (matches) |
| 11 | kite file alone @ `bae60ce6` | isolated | **38 passed / 0 failed** ✓ (matches) |
| 12 | The one before-failure **is** G-B1 and nothing else | `-q` FAILED lines | sole failure `::test_rect_is_a_valid_shape_and_the_enum_grew_deliberately` ✓ |
| 13 | Tree-wide collection | `--collect-only -q` | **10,268 collected, 0 collection errors** ✓ (matches) |
| 14 | Census non-vacuous — **re-run by me, not accepted** | in-memory injection, no file edited | control **3 passed**; growth `hexring` → **1 failed**, message `added=['hexring'] removed=[]`; removal `melee` → **2 failed** (cell 2 *and* cell 3 both fire), messages `removed=['melee']` and `a family was REMOVED: ['melee']`. ✓ |
| 15 | Working tree == `bae60ce6` | `git status --porcelain -uno` | **empty** — no uncommitted carry inflating the counts |
| 16 | Commit hygiene | `git log -1` | `Co-Authored-By` trailer present; the baseline anomaly is **declared in the commit message**, not buried in the report. ✓ |

**`:351` — her reasoning is CORRECT, checked against source.** The line is
`assert "rect" in TelegraphSpec.VALID_SHAPES`: a single-value membership test, **monotone under
growth** — adding `disc` cannot redden it — and it fails only on removal of `rect`, which is the
behaviour the cell's own docstring says it wants. It equality-pins nothing. **Leaving it unamended
is right**, and amending it would have been diff noise. Cell 3 of the census now backstops its
removal-guard intent.

**The fix is the class, not the instance — and I checked that claim.** The census goes red on any
future growth of either set and hands the grower the grep. It does **not** itself detect a *stale
fence* — it detects the *growth* and routes to the grep that finds the fences. gamora's docstring
says exactly that and does not overclaim. Independent check on the protocol's completeness: there
are **zero enumerating consumers** of either value-set outside `tests/` and outside the defining
module — `src/`, `scripts/`, `reincarnated-demo/src`, `reincarnated-loadout/src` all return nothing
but `spatial_telemetry.py`'s own definition and `validate()`. The `tests/`-scoped grep in step 2 is
therefore **complete today**.

## § 8.3 — CORRIGENDUM to § 2 of this note (dated 2026-08-08, post-resubmission)

> **gamora is right and I was wrong. § 2's baseline parenthetical is corrected below, and the
> footnote attached to it is WITHDRAWN.**

**§ 2 as written** reads, for `tests/test_wr3_kite_commit_stage2b.py`:

```
@ ebf13240 (PYTHONPATH-isolated):  1 failed*, 37 passed  → this test PASSES
* the one failure at ebf13240 in that file is a different test; this assertion was green.
```

**Re-measured, from a fresh detached worktree at `ebf13240`, both ways:**

```
@ ebf13240, PYTHONPATH=/tmp/jr-ebf13240/src  →  38 passed, 0 failed
@ ebf13240, NO override (.pth resolves to HEAD src)
   →  1 failed, 37 passed
   FAILED ::test_rect_is_a_valid_shape_and_the_enum_grew_deliberately
   tests/test_wr3_kite_commit_stage2b.py:357: AssertionError
```

**The `1 failed, 37 passed` figure is a CONTAMINATED-RUN RESIDUE** — the exact hazard § 1 of this
note was written to warn about, left un-swept in my own § 2 evidence line. The contaminated run
reads HEAD's 8-value `VALID_SHAPES` against `ebf13240`'s 7-value equality pin, so it fails at
`:357` — **the very test under review**, which also makes the footnote ("a *different* test") wrong.
The label `(PYTHONPATH-isolated)` was carried over onto a number that was not.

**Two independent facts corroborate gamora, both already inside this note:**
1. The kite test file is **byte-identical between `ebf13240` and `874302d5`**
   (`git diff --stat` → empty), so the file has the same 38 tests at both ends; only the *source*
   grew. A 38/38 green at `ebf13240` is exactly what the finding predicts.
2. **G-I4 of this very note** puts the `ebf13240` pre-existing set at **7**, itemised as
   `2 nova-telegraph + 1 wr1_m12 + 4 kit_space_emitter` — which allocates **zero** failures to the
   kite file. § 2's "1 failed" contradicted my own § 5 census. G-I4 was right; § 2 was wrong.

**Her placement of the two failures verified, test-ID for test-ID.**
`tests/test_wr2_d_nova_telegraph.py` @ `ebf13240`, isolated → **2 failed / 67 passed**,
`::test_the_minted_telegraph_carries_the_DERIVED_duration_under_the_arm` +
`::test_the_minted_telegraph_carries_the_MEASURED_0_750_off_the_arm_H_M2_f`. Exactly the two she
names, in the file she names.

> **CORRECTED § 2 EVIDENCE LINE — read § 2 with this substitution:**
> ```
> @ ebf13240 (PYTHONPATH-isolated):  38 passed, 0 failed   → this test PASSES
> @ 874302d5:                        1 failed, 37 passed   → FAILED "Extra items in the left set: 'disc'"
> ```
> The footnote is struck. **The load-bearing claim is untouched and now rests on a cleaner
> measurement than the one it was filed with:** `:357` green at `ebf13240`, red at `874302d5`,
> delta caused by the `disc` growth. **G-B1 was a correct BLOCK.** Only its parenthetical was dirty.

**Second corrigendum, same date — § 2's assertion total.** § 2 says *"15 assertions across 5 test
files."* AST-precise count at `874302d5` (assert-statements whose source names either value-set):

```
  6  tests/test_br2_resolve_truth_1.py    -> [134, 137, 139, 140, 153, 154]
  4  tests/test_br2_trace_stage_1.py      -> [417, 418, 426, 428]
  3  tests/test_wr3_stage2c.py            -> [418, 423, 424]
  2  tests/test_wr3_kite_commit_stage2b.py-> [351, 357]
  4  tests/test_kc2_channel_disc.py       -> [198, 199, 204, 205]
  ------------------------------------------------------------------
 19  across 5 files
```

**Read § 2 as "19 assertions across 5 test files"** — 15 in the four *equality*-fencing files the
§ 2 table tabulates, plus 4 **membership-only** cells in `tests/test_kc2_channel_disc.py`, which
were already green and correctly required no amendment. The **file count of 5 was right**; only the
assertion total was the 4-file subtotal. Two line numbers in the § 2 table also drift by one against
AST (`:135`→`:134`, `:427`→`:426`, multi-line asserts). **None of this moves the finding.** Recorded
because the "15" has propagated into gamora's commit message and the census docstring, and the
conductor may wish to let it stand rather than re-touch a committed message.

## § 8.4 — New findings on the resubmission (all INFO — none gates anything)

| # | Sev | Observation |
|---|---|---|
| **G-I5** | INFO | The census docstring's courtesy line-list carries `test_wr3_kite_commit_stage2b.py :351 :357` — but after this same commit's amendment, `:357` is the **amendment comment**, not an assertion (the limbs sit at `:365–366` and `:367–369`). **Stale at birth for the one file the commit edited.** Explicitly de-authorised in the docstring's own closing line (*"Line numbers drift; the grep in step 2 does not"*), so it misleads nobody who reads to the end — recorded, not actioned. |
| **G-I6** | INFO | Docstring line 27 reads `tests/test_kc2_channel_disc.py  (membership, not equality — see note below)`. **There is no such note below.** Dangling cross-reference. One clause on cell 3 would close it. |
| **G-I7** | INFO | `test_a_value_is_never_REMOVED_from_either_set` re-declares `ever_admitted_shapes` / `ever_admitted_families` as **literals separate from** `EXPECTED_SHAPES` / `EXPECTED_FAMILIES`, while protocol step 1 says only *"update the expected membership below"* (singular). A future grower who updates `EXPECTED_*` alone leaves the never-REMOVED floor **one value short** — the newest value would be unguarded against removal. Sound today (the two pairs are identical, and the separate literal is deliberate: it is a monotone floor, not a mirror). Naming both in step 1 removes the drift vector. |
| **G-I8** | INFO | Placement in a **new dedicated wave-neutral file** rather than appended to a wave-scoped one is the right call and I record it as such — the failure mode under repair was precisely that the census lived only where you already had to know to look. |

## § 8.5 — What the conductor needs from me

1. **G-C limb 1 ("gamora tests green") is now MET on my authority.** Both seams clear at Gate-2:
   gamora **PASS-with-findings** (4 WARN / 8 INFO), star-lord **PASS-with-findings** (2 WARN /
   3 INFO). No BLOCK-class item is open on either seam.
2. **G-W1 remains my one carry-forward concern** (§ 7's closing clause). L-34(d) has ruled it onto
   the G-D r2-consumption wiring; I do not contest the routing and do not re-flag its absence here.
   The concern is unchanged in substance: it is the only finding whose failure mode is **silent at
   the gate that consumes it**.
3. **No decisions-log entry is owed.** This resubmission amends test guardrails to record an
   already-ratified growth; no architectural commitment moved.
4. **ADR-002 tiering:** the resubmission is **test additions + a within-seam test amendment** —
   squarely inside my direct-approval tier. **No Matt escalation is required to clear G-B1.**

**Signed:** jack-ryan, Gate-2 DEV-MODE re-review, 2026-08-08.
*She fixed the instance, fixed the class, and caught an error in my own evidence line — reported it
up rather than quietly correcting it, which is the behaviour I would rather have than a clean
report. The correction is mine to carry and § 8.3 carries it.*
