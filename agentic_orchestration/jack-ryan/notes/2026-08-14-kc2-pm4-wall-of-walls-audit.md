# Finding — 2026-08-14 — KC2-PM4 wall-of-walls audit (I-9 … I-12)

**Reviewer:** jack-ryan (DEV-MODE, read-only pattern audit)
**Severity:** WARN — no BLOCK issued; this cell is an audit, not a gate
**Commissioned by:** gandalf (`RUN-CONDUCTOR`, RUN KC2-PM4) per charter ruling **R-PM4-31 part (4)**
**Target:** engine drivers `8a826b67` (I-9) · `a9ac9483` (I-10) · `adacd009` (I-11) · `75c67298` (I-12)
**Developer:** gamora (self-routed: *"the wall needs its own wall, and I am not the right party to certify that"* — I-12 § 12.1)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log as truth), #5 (severity matters) · Disciplines #1, #3, #8, #10

---

## 0 — PROVENANCE CORRECTION, FIRST, BECAUSE THE PATTERN IS WORSE THAN REPORTED

Gamora's own chain string — reproduced verbatim in the commission — reads
`I-9 check 2 → I-10 check 12 → I-11 check 7 → I-12 check 5`, four laps, one RED each.

**Measured from the four findings artifacts, that string is wrong on two counts.**

| lap | artifact | wall | REDs, measured |
|---|---|---:|---|
| I-9 | `kc2-pm4-i9-findings-20260814_022801.json` | 18/20 | **checks 12 AND 18** |
| I-10 | `kc2-pm4-i10-findings-20260814_035800.json` | 18/20 | **checks 2 AND 12** |
| I-11 | `kc2-pm4-i11-findings-20260814_052659.json` | 21/22 | check 7 |
| I-12 | `kc2-pm4-i12-findings-20260814_065051.json` | 14/15 | check 5 |

1. **"I-9 check 2" is a transposition of I-10's check 2.** I-9 has no RED at check 2; I-9's check 2 (`pre-I-6 arm reproduces I-5's digests, FOUR folds back`) passed.
2. **The count is SIX wall REDs across four laps, not four.** I-9 and I-10 each carried two. The phrase "the lap's ONLY RED" is accurate for I-11 and I-12 only.

Both landing notes (I-9 § 10.1, I-10 § 10) report their two REDs correctly and in full. The compression happened when the *pattern claim* was authored at I-11 § 12.1 and then copied forward verbatim into I-12 § 12.1 without re-derivation from the artifacts. **Named because the chain string is the sentence the conductor acted on, and it under-states its own case by a third.**

---

## 1 — DEFECT TAXONOMY (all six, not four)

### D-1 · I-9 check 12 — closed band pinned at the convergent value (ULP edge)

`src/reincarnated/simulation/scripts/gamora_kc2_pm4_i9_sustain_actuation_2026_08_14.py:560-566`

```python
add(12, "⚑ War Cry uptime is now the MEASURED 29 % ceiling: reduced/raw in [0.28, 0.29]",
    all(0.275 <= (float(c["counterplay"]["telemetry"]["warcry_reduced"])
                  / float(c["counterplay"]["telemetry"]["raw_seen"])) <= 0.290
        for c in cells.values()), ...)
```

- **Class:** *closed-band-at-the-convergent-value.* The upper edge `0.290` is the exact value the quantity converges to.
- **Measured:** `0.2900000000000012` / `0.2899999999999949` / `0.2900000000000074` — two cells over the edge by **1.2e-15** and **7.4e-15**.
- **Did the property hold?** **YES.** `abs(ratio − 0.29) < 1e-12` on all three cells, by three orders of magnitude.
- **Fail direction:** CLOSED (over-strict).

### D-2 · I-9 check 18 — stale spec contradicting the author's own prior measurement

`…i9…:581-585`

```python
add(18, "⚑ THE INVARIANT I-8 LANDED SURVIVES — pairs above tolerance == 0 on every cell",
    all(c["convergence"]["⚑ invariant"]["pairs_above_tolerance_postsolve_total"] == 0.0
        for c in cells.values()), ...)
```

- **Class:** *stale spec.* I-8 had already MEASURED this quantity at 182 / 8 / 2 and banked it as `D-I8-2`. The check demands zero for a quantity the author's own previous lap proved non-zero.
- **Measured:** `182 / 8 / 2` — I-8's numbers digit for digit.
- **Did the property hold?** **YES**, on the question the check's *name* asks ("the invariant SURVIVES"): 182/8/2 at I-8, 182/8/2 at I-9, unmoved, sub-micrometre, cap not raised.
- **Fail direction:** CLOSED.

### D-3 · I-10 check 2 — unsatisfiable by construction, twice over

`…i10_arrival_variance…:706-707`

```python
add(2, "⚑ fold-OFF batons reproduce I-9's three baton digests byte-exactly",
    base.get("i9_batons") == I9_BATON_DIGEST, base.get("i9_batons"), I9_BATON_DIGEST)
```

- **Class:** *unsatisfiable-by-construction*, on **two independent grounds**: (a) the driver never builds the input — fold-off arms compute a surface digest and are discarded, so no baton can be emitted from them; `got=None`. (b) Even if it were built, a baton's `sim_pin` carries `engine_version_full` (the engine git SHA), so **two batons emitted at two commits cannot hash-match by construction.** A FULL-hash baton-identity check asserts that git does not advance.
- **Did the property hold?** **YES**, executed out of band: re-emitting `pm4-i9-cluster-defon` at I-10 HEAD gives masked digest `d8965c26…687d` on both.
- **Fail direction:** CLOSED. This one **could never have passed**, which is the clean case.

### D-4 · I-10 check 12 — invented threshold, wrong about the world's SCALE

`…i10…:758-761`

```python
add(12, "⚑ the I-8 invariant SURVIVES: worst post-solve penetration < 1e-6 m on every cell",
    all(v < 1.0e-6 for v in got_pen.values()), ...)
```

- **Class:** *invented threshold.* The math note rejected two wrong predicates for this same check in writing (`== 0`; equality-to-I-9's-counts) and then a third — a `1e-6` bound invented in the check body, with no measured basis.
- **Measured:** `8.96e-6 / 4.25e-6 / 7.48e-7` — I-9's `8.959519020246276e-06` identically.
- **Did the property hold?** **YES**, and EXACTLY: every convergence observable identical to I-9 on all three cells.
- **Fail direction:** CLOSED.
- ⚑ **This is D-2 recurring one lap later on the same underlying quantity, third specification attempt.**

### D-5 · I-11 check 7 — wrong FRAME, and the one true positive of the six

`…i11_player_offense…:652-662`

```python
for nm in ("S-CADENCE-LO", "S-CADENCE-LO-CH"):
    s = sens.get(nm)
    if s:
        nt, nh = s["n_ticks"], s["n_hit_ticks"]
        want = math.floor(nt * po.CadenceLimb.LO.hits_per_tick)
        acc_ok = acc_ok and abs(nh - want) <= 1
add(7, "⚑ the LO cadence accumulator fires exactly ⌊N × 0.9295408⌋ times (± 1 boundary tick)", acc_ok, ...)
```

- **Class:** *wrong frame.* The predicate is run-global; the accumulator is **per-wave** — `PlayerOffense` is constructed per wave (the mitigation board is keyed `(record, wave)`), so fractional credit is discarded at every wave boundary. Residual is `≈ n_waves / 3`, exactly what a uniform discarded remainder predicts.
- **Measured:** 1,192 vs 1,194 (6 waves); 3,068 vs 3,073 (15 waves).
- **Did the property hold?** **NO — and this is the exception.** The RED pointed at a genuine, previously undeclared modelling fact, banked as `D-I11-3`, materiality **≈0.06 % of hits** over a 20-wave ladder, unable to reach a T-verdict. **One of the six was a true positive.**
- ⚑ **Secondary defect, unbanked:** the `if s:` guard silently skips an absent sensitivity cell. Had both cells been absent, `acc_ok` stays `True` and the check passes vacuously. Same class as § 2's vacuity family, sitting inside the check that fired.

### D-6 · I-12 check 5 — bare truthiness on a container that is never empty

`…i12_secondary_streams…:594`, with `_law3_moved` at `…i4_match_and_fold…:527-546`

```python
add(5, "Law 3 — no constant moved", not _law3_moved(), _law3_moved())
```

```python
def _law3_moved() -> Dict[str, Any]:
    ...
    return {"witness": LAW3_WITNESS, "measured": got,
            "moved": {k: [LAW3_WITNESS[k], got[k]] for k in LAW3_WITNESS
                      if abs(got[k] - LAW3_WITNESS[k]) > 1e-9}}
```

- **Class:** *bare truthiness on a non-empty container.* The return is a three-key dict, **always** truthy, so `not _law3_moved()` is **always `False`**. The check is permanently RED regardless of the model.
- **Correct form, and the author already had it, twice:** `…i9…:576` and `…i11…:707` both read `_law3_moved().get("moved") == {}`.
- **Did the property hold?** **YES.** Artifact `assert_wall.checks[4].detail.moved == {}`.
- **Fail direction:** CLOSED — **by the accident of the `not`.** Written `add(5, …, _law3_moved(), …)` the identical class of defect is **permanently GREEN**. The class is polarity-symmetric; only the unary operator decided which side of the wall it landed on. *This is the single most important sentence in this audit.*

### D-6b · UNBANKED SIBLING — the same frame confusion in the EMISSION path

`…i12…:1003` — `"law_3": {"moved": _law3_moved()},`

The artifact therefore carries `law_3.moved` = a three-key dict, and the empty set is at **`law_3.moved.moved`**. I-11 (`…i11…:1105, 1154`) emits `"law_3": _law3_moved()` — un-nested. **I-12's landing note § 12.1 states "the findings artifact carries `law_3.moved: {}`" — that is false as written**; `law_3.moved` is `{witness, measured, moved}`. The property still holds one level down. Banked because the *evidence* offered in exoneration of the check is mis-framed by the same confusion as the check, and a downstream consumer reading `law_3.moved` gets a truthy object.

### Taxonomy roll-up

| # | lap · check | class | property held? | fail direction |
|---|---|---|---|---|
| D-1 | I-9 · 12 | closed band at convergent value (ULP) | YES | CLOSED |
| D-2 | I-9 · 18 | stale spec vs own prior measurement | YES | CLOSED |
| D-3 | I-10 · 2 | unsatisfiable by construction (×2 grounds) | YES | CLOSED |
| D-4 | I-10 · 12 | invented threshold, wrong scale | YES | CLOSED |
| D-5 | I-11 · 7 | wrong frame (per-wave vs run-global) | **NO — true positive** | CLOSED |
| D-6 | I-12 · 5 | bare truthiness on non-empty container | YES | CLOSED **by accident of `not`** |

**Six distinct classes. No class repeats across laps except D-2→D-4** (same quantity, third specification attempt).

---

## 2 — THE LOAD-BEARING QUESTION: COULD ANY OF THE SIX HAVE MASKED A MODEL DEFECT?

### 2.1 — Verdict on the six REDs: NO. Not one.

**All six failed CLOSED.** Each demanded *more* than the world offers, fired loudly, and was investigated and banked. A false-RED costs analyst time and dilutes the wall's signal; it cannot hide a model defect, because the model defect it might have hidden would have shown up as… a RED, which is what happened.

Two sharpenings:

- **D-3 is the honest limit case:** a check that could not have passed no matter what the model did carries **zero information about the model**. It is not a masking risk; it is a *dead* check. Its lap ran with 19 live checks, not 20.
- **D-6 is the warning shot.** `not <always-truthy>` is permanently RED; `<always-truthy>` is permanently GREEN. Same defect class, same author, same line, opposite consequence. **The four-lap pattern is not evidence that gamora's walls fail safe — it is evidence that gamora's walls fail *loudly when they happen to fail closed*, and we have no observation at all about the ones that failed open.** Which is exactly why the audit had to look at the greens.

### 2.2 — The greens. **I audited all 14 surviving I-12 greens, not a sample of 10.**

`src/reincarnated/simulation/scripts/gamora_kc2_pm4_i12_secondary_streams_2026_08_14.py:585-632`

| # | predicate (abridged) | class | false-GREEN capable? |
|---|---|---|---|
| 1 | `len(pins) == 5` | **cardinality proxy** for a name claiming "digests × 5 EXACT from bytes" | Not in practice — `po.verify_substrate()` raises `SubstrateDigestError` on mismatch (`kc2/player_offense.py:93`). Sound **only by out-of-band raise**; the predicate itself carries no exactness. |
| 2 | `all(base["i11"][k] == I11_SURFACE_DIGEST[k] for k in base["i11"])` | **iterates the GOT side.** Empty dict → vacuous `True`; a *missing* key is never compared. `base` is seeded `{"i11": {}}` at line 700 | **YES-capable**, neutralised only by the `raise AssertWallHalt` at line 720 |
| 3 | `base["absent_arm_ok"]` | **bare truthiness — the same class as the RED at check 5.** Seed `True`, `and`-folded across the CELLS loop → empty loop = `True` | **YES-capable** |
| 4 | `all(c["determinism"]["differences"] == 0 …)` | explicit comparison, 6 cells, counts in `detail` | NO — **sound** |
| 6 | `"random" not in <source text of sst>` | **name/predicate divergence.** Name says "the path draws ZERO"; the predicate greps module source. `cell_census: 13301` is reported and **never asserted** | Partial — the grep is a real proxy; the ZERO claim is unasserted |
| 7 | `n_soulfire_killable == 0 and n_killed_by_soulfire >= 0` | **second conjunct vacuous** — a count is always ≥ 0 | **Half-vacuous.** First conjunct real (`0`, `min_lightning_res 100.0`) |
| 8 | `max_concurrent_bleeds_per_target <= 1` | explicit comparison; `detail: 1` witnesses non-vacuity | NO — **sound** |
| 9 | `all(hp_after is not None for … if etype == "dot_tick")` | **empty-`all()`.** `detail` is the STRING `"checked over every dot_tick row of the record cell"` — **no row count** | **YES-capable, and UNFALSIFIABLE FROM THE ARTIFACT.** Green over 0 rows is indistinguishable from green over 50,000 |
| 10 | `all(float(e[_APPLIED] or 0.0) >= 0.0 …)` | empty-`all()`, **plus `or 0.0` coerces `None` → `0.0`, so a null applied value PASSES a null-hostile check**; `detail` again a string | **YES-capable** |
| 11 | `pre["roster"]["n_absent"] == 0 and pre["pets"]["n_absent"] == 0` | **SCOPE REGRESSION.** I-11's twin (`…i11…:686-693`) also asserted the RUNTIME `player_offense_wire` `n_absent`. I-12 kept only preflight | Runtime blind spot introduced silently |
| 12 | `pc["mismatches"] == 0` | **SCOPE REGRESSION.** I-11 check 5 (`…i11…:645-648`) asserted `pc["mismatches"] == 0 and pc["rows"] == 79_240`. **I-12 kept "79,240" in the check NAME and dropped it from the predicate.** `rows == 0` → GREEN | **YES-capable** |
| 13 | `abs(dps * dur − total) < 1e-6` | **constants vs constants** — verifies the spec against itself, touches no model output | Tautology-adjacent; not a masking risk, but not evidence either |
| 14 | `"ManaBurnDrain" not in json.dumps(rec["top_incoming"])` | **WRONG SCOPE.** `top_incoming(runs, n=8)` returns `sorted(...)[:8]` (`…i1_ehp_fold…:414-424`); the artifact carries exactly 8 rows, floor `55,615` applied. A **HALT-TRIGGER** check evaluated over a top-8 truncation | **YES — the strongest false-GREEN in the wall.** Any ManaBurnDrain contribution ranking 9th or lower is invisible, and "unreached" is precisely a *low-magnitude* claim |
| 15 | `add(15, "…brackets are verdict-identical", True, {…})` | **LITERAL `True`. Unconditional pass.** The three numbers (`205.2245` / `204.3265` / `205.3061`) are printed in `detail` and **never compared to anything** | **YES — the check asserts nothing at all.** It contributes a `PASS` to the 14/15 and carries zero information |

**Tally of 14 greens: 3 sound (4, 8, and 1-by-out-of-band-raise) · 2 assert nothing (14, 15) · 4 vacuous-capable (2, 3, 9, 10) · 2 silent scope regressions from their own I-11 twins (11, 12) · 1 half-vacuous (7) · 1 name/predicate divergence (6) · 1 tautology (13).**

### 2.3 — The finding that decides the discipline rule

`kc2/player_offense.py:511` — `chain_positive_control` compares with `if d > tolerance + 1e-9:` — **the correct epsilon-slack form**, the exact technique D-1 lacked. And the I-12 artifact records `worst_abs_diff = 0.005000000004656613` against `tolerance = 0.005` with `mismatches = 0`: the same ULP situation as D-1, landing GREEN because the epsilon was there.

**So the author demonstrably knows the correct ULP form and applies it inside the `kc2` module, and got it wrong in the wall one lap earlier.** Likewise `.get("moved") == {}` exists correctly at I-9:576 and I-11:707 and regressed at I-12:594. **The failure mode is not ignorance of technique. It is that the wall is authored as a §D appendix at landing time, under a different standard of care than the module code it is auditing.** Any remedy that teaches technique will miss; the remedy has to change *when and how the wall is specified and proven*.

### 2.4 — The answer, stated plainly for the conductor

> **The four-lap RED chain is annoying and honest. It masked nothing.** But the audit it prompted found **two I-12 checks that assert nothing at all (14, 15), four that can pass over an empty set, and two that were silently narrowed from their I-11 originals while keeping the original's claim in the check name.** The dangerous defects were never in the REDs. They were in the 14/15.
>
> ⚑ **Check 14 is the one to act on today:** `D-I8-3 ManaBurnDrain` is a declared **HALT trigger**, and its "unreached" verdict has been carried GREEN across I-11 and I-12 on a **top-8** membership test. It is a low-magnitude claim tested only against the eight largest contributors. **I make no claim that ManaBurnDrain was in fact reached — the point is that the wall cannot tell us, and has been reporting that it can.** Re-running that predicate over the full event stream is a ten-line change and is the highest-value single item in this file.

---

## 3 — DISCIPLINE RECOMMENDATION (CANDIDATE ONLY — NOT RATIFIED IN THIS CELL)

Filed as a **candidate** for `engineering-disciplines.md`. Per my own § 0 constraint and the commission's terms, **no canonical text is amended by this cell.** Ratification is a separate act and wants Matt's eye on W-4 (it has a cost).

### Candidate discipline — **"THE WALL GETS ITS OWN WALL"**

**W-1 · Explicit-comparison rule.** Every assert-wall predicate is a comparison, membership, or boolean composition **over named quantities**. Bare truthiness on a container or a function return is barred.
`not _law3_moved()` → `_law3_moved()["moved"] == {}`. Mechanically lintable over the `add(...)` call sites.

**W-2 · Non-vacuity witness.** Every `all(…)` / `any(…)` predicate (a) conjoins `n > 0` over the iterated set and (b) puts that `n` in its own `detail`. **A green over zero rows is a RED.** Retires the string-detail pattern at checks 9 and 10, where the artifact cannot distinguish "0 violations over 50,000 rows" from "0 rows examined."

**W-3 · Name–predicate correspondence.** Every number and every quantifier in a check's NAME must appear in its predicate. "79,240 rows reproduced" must assert `rows == 79_240`. **A check whose predicate is a literal `True` is a REPORT and is emitted with status `"report"`, never `PASS`, and is excluded from the `n/N` wall score.** Retires check 15 and the check-6 divergence, and would have caught the check-12 regression at authoring time.

**W-4 · Mutation self-test — the wall's own wall.** Before the lap's measured run, every check is forced RED **once** against a deliberately mutated version of the quantity it names. A check that stays GREEN under mutation of its own named quantity is a defect and **halts the lap**.
This is the load-bearing clause. Mechanically it catches: check 15 (immune to all mutation), checks 9/10/2/3 (green on the empty set), check 14 (green on a 9th-rank injection), check 12 (green on a truncated CSV) — **and every one of the six REDs, since a check that goes RED on the *unmutated* input fails the self-test's control arm.** It is the only proposed clause that catches both polarities with one mechanism.

**W-5 · The wall is specified in the MATH NOTE, and reviewed there.** The wall belongs in the math note as a first-class object — predicates written out, each with the measured basis for its threshold — and is the object of the Gate-1 read. It is not a §D appendix first seen at baton time. Rides free with Discipline #1 (math-before-code), which the run already honours for the *model*; § 2.3 shows the wall is not currently held to it.

**W-6 · Inherited checks may be narrowed only with a written reason.** A check carried forward from a prior lap that is strictly weaker than its predecessor must say so and say why, in the math note. I-12's checks 11 and 12 are strictly weaker than I-11's 11 and 5; **nobody noticed, because both went green.** Weakening a wall is invisible by construction — that is the whole argument for the clause.

### My lean, and the cost honestly stated

- **W-1, W-2, W-3, W-6 — adopt.** All four are cheap, mechanically enforceable by a lint over `add(...)` call sites, and cost roughly one line per check. Between them they retire every green-side defect in § 2.2 **except** check 14's scope error.
- **W-4 — adopt, but SCOPE IT.** Universal mutation self-testing roughly doubles wall authoring cost and is the clause most likely to be quietly dropped under lap pressure. **Recommend scoping it to checks whose name contains a numeric literal, or one of `EXACT` / `ZERO` / `ALL` / `NO` / `UNREACHED`** — i.e. the absolute-quantifier checks, which is where both false-GREEN classes live. That subset is 9 of I-12's 15.
- **W-5 — adopt, free.** No new machinery; it moves an existing artifact one gate earlier.
- **Gamora's own routing is correct and should be honoured:** *"the wall needs its own wall, and I am not the right party to certify that."* W-4 and W-5 together are the structural answer — one mechanical, one procedural — and W-5 in particular puts a second pair of eyes on the wall spec *before* the lap runs, which is the review this run has never had.

---

## 4 — ACTION

- [ ] **gamora (today, before the next lap):** re-scope I-12 check 14 from `rec["top_incoming"]` (top-8) to the full event stream. Ten-line change. A HALT trigger is being certified against a truncated summary. *(This is a description of what is owed, not a repair instruction for the landed lap — the I-10/I-11/I-12 precedent of not repairing a wall mid-lap stands and is correct.)*
- [ ] **gamora (next lap):** restore the two dropped conjuncts — `pc["rows"] == 79_240` at check 12, runtime `player_offense_wire` `n_absent` at check 11 — to match their I-11 originals.
- [ ] **gamora (next lap):** emit check 15 with status `"report"`, not `PASS`; it is excluded from the wall score until it has a predicate.
- [ ] **gamora (next lap):** `…i12…:1003` — emit `"law_3": _law3_moved()` un-nested, per I-11, and correct the I-12 § 12.1 sentence that reads `law_3.moved: {}`.
- [ ] **gandalf (conductor):** correct the chain string in the run ledger — six REDs across four laps (I-9 {12, 18}, I-10 {2, 12}, I-11 {7}, I-12 {5}); "I-9 check 2" is I-10's.
- [ ] **jack-ryan:** hold W-1…W-6 as a candidate. **No canonical amendment in this cell.** Ratification is a separate act.
- [ ] **Matt (ESCALATE, decision needed):** W-4 is the load-bearing clause and the only one with real cost. Adopt universally, adopt scoped to absolute-quantifier checks (my recommendation), or decline. W-1/W-2/W-3/W-5/W-6 are within my ADR-002 tier and I will ratify them on your nod to W-4's scope.

---

## 5 — REFERENCES

**Drivers (engine, `~/Games/reincarnated-engine`)**
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i9_sustain_actuation_2026_08_14.py` (wall §, L507-594) — `8a826b67`
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i10_arrival_variance_2026_08_14.py` (wall §, L701-790) — `a9ac9483`
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i11_player_offense_2026_08_14.py` (wall §, L634-736) — `adacd009`
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i12_secondary_streams_2026_08_14.py` (wall §, L570-638; emission L1003) — `75c67298`
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i4_match_and_fold_2026_08_13.py:527-546` — `_law3_moved()` definition
- `src/reincarnated/simulation/scripts/gamora_kc2_pm4_i1_ehp_fold_2026_08_13.py:414-424` — `top_incoming(..., n=8)`
- `src/reincarnated/simulation/kc2/player_offense.py:88-96` (`verify_substrate`), `:490-515` (`chain_positive_control`, the correct epsilon form)

**Artifacts (measured, read-only)**
- `src/reincarnated/simulation/output/kc2-pm4-i9-findings-20260814_022801.json`
- `src/reincarnated/simulation/output/kc2-pm4-i10-findings-20260814_035800.json`
- `src/reincarnated/simulation/output/kc2-pm4-i11-findings-20260814_052659.json`
- `src/reincarnated/simulation/output/kc2-pm4-i12-findings-20260814_065051.json`

**Landing notes (meta-repo)**
- `agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i9-sustain-actuation-landing.md` § 10.1
- `agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i10-arrival-variance-landing.md` § 10.1, § 10.2
- `agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i11-player-offense-landing.md` § 12.1
- `agentic_orchestration/gamora/notes/2026-08-14-kc2-pm4-i12-secondary-streams-landing.md` § 12.1, § 12.2
- `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (R-PM4-31)
