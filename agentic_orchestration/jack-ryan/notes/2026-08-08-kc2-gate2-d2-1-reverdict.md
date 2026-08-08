# Finding — 2026-08-08 — KC2-SIM Gate-2 **D2-1 RE-VERDICT**

**Reviewer:** jack-ryan (DEV-MODE, BLOCK authority live)
**Severity (overall):** **BLOCK D2-1 → LIFTED** · new findings: WARN ×3 · INFO ×4
**Targets:**
- **Leg 1** — spec working copy `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`
  @ sha256 `705d4353…` (236,424 B, 10:51:44), **re-verified @ sha256 `ab93c513…` (264,116 B, 11:00:42)**
  after the file grew ~28 KB mid-review · ledger @ sha256 `5969812a…` (10:51:01)
- **Leg 2** — engine `cbb29e683fbf330e8d163aaae4e417fcf7f80d07` (unpushed), tracked tree **clean**
- **Leg 3** — orphan transcript `/private/tmp/…/tasks/b3e8v9dmk.output` (20 lines, mtime 08:13)

**Developers:** gandalf `RUN-CONDUCTOR` (leg 1) · star-lord (leg 2)
**Authority:** desirable-run-pattern **standing safety #2** — the conductor does not self-clear.
Commissioned at ledger **L-47(h)**.
**Principles applied:** REVIEW_PROCESS #1 · #2 · #3 · #4 · #5. Disciplines **#1, #2, #8, #10, #12**.
ADR-002 · ADR-004 · ADR-006. desirable-run-pattern **§ 6.3 (rubric law)** — § 6 below names what this
verdict's green covers and what it does not.

---

## 0 — Verdict table

| leg | scope | verdict |
|---|---|---|
| 1 | conductor spec edits (i)–(iv) + the two L-47 AC-10.4 stragglers | **PASS** |
| 2 | engine `cbb29e68` — schema · validator · test · MIGRATION · AGENT_STATE | **PASS** |
| 3 | the orphaned 2-F transcript | **ADJUDICATED — pre-existing tree, not a `cbb29e68` failure** |
| — | VALUE-SET SWEEP standing-method extension (L-47(f)) | **RATIFIED-AS-AMENDED** (3 amendments) |

> ## **BLOCK D2-1 — LIFTED.**
> All four stated unblock conditions are met and I re-measured each on my own instruments.
> The lift is **on D2-1 grounds only**; § 6 states the residual gates.

**New findings — none is BLOCK.** Three WARN, four INFO. The most consequential is **R-1**: the
corrected value is not pinned, and the two-sided revert to the exact pre-fix state passes every
guard in the repo. That is a measured fact, not an inference.

---

## 1 — LEG 1: the conductor's spec edits — **PASS**

**The artifact is live-edited and moved three times under this review** (10:41 → 10:51 → 11:00,
+28 KB on the last move — the locomotion spec-amendment piece landing per L-47(h)). **Line numbers
are therefore not citable.** I verified at `705d4353…`, re-verified every anchor and re-ran the whole
sweep at `ab93c513…`, and cite by **anchor text** below. Both hashes agree byte-for-byte on all six
sites, and the ~28 KB of new material introduced **no new stale hits**.

| # | edit | anchor text | verdict |
|---|---|---|---|
| i | item-12 `fixture_p06_state` rewrite | ``…bonus_spawn_p06` splits [M-1], and the fixture side is ~~MEASURED~~ RULED-OFF`` | **CLEAN** |
| ii | § 11 M-1 row fixture-side `false`/RULED-OFF | ``M-1 \| split `bonus_spawn_p06` \| … fixture side ~~`true`, MEASURED (L-21)~~`` | **CLEAN** |
| iii | former-members U9-6 closure-cite correction | `U9-6 → ~~measured ON L-21~~ **RULED OFF L-37(b)**` | **CLEAN** |
| iv | § 10.5 fact-5 re-grade + 306.83→290.17 + basis note | `~~306.83~~ **290.17**` · `*(Denominator basis — D2-1 sweep annotation…` | **CLEAN** |
| + | L-47 stragglers: AC-10.4 live-tense ×2 | `…is DEMOTED-OPEN per L-33(g), which is why both limbs are carried` · `both p06 limbs are CARRIED because…` | **CLEAN** |

**(i) is the one D2-1 cared about most, and it is right.** D2-1's objection to `:1714` was not only
the wrong value — it was that the site restated the **L-33(g)-STRUCK** evidentiary leg ("the 5th body
*is* the p06 hero slot") as live. The rewrite strikes *both*, in the `:1033` lineage form, and adds
the § 10.8 consequence (**4 raw start bodies, not 5**) that the struck claim had been silently
carrying. Nothing was amputated.

**(iii) is better than what D2-1 asked for.** D2-1 asked for the cite to be corrected. The edit
states the **rule** — *"closure cites L-37(b), never L-21 (T-3's own rule)"* — which converts a
one-time fix into a guard against the next reader re-deriving the wrong closure basis.

**(iv) is the strongest edit in the volley, and it is a judgement I want on the record.** The
temptation was to restate 292 / ≈ 18 % from the live model. The conductor did not: the basis note
keeps the pin-era arithmetic **with its pin's lineage** and says why — § 12 T-2's tolerance-on-target
ruling makes the PINNED target the denominator by ruling, goalpost fixed at pin time. Rewriting those
percentages against 271.50 would have been a quiet in-run goalpost move dressed as a correction.
Declining it is standing safety #1 operating on an edit nobody would have questioned.

### 1.1 — Independent re-sweep: **the spec surface is EXHAUSTED**

I did not read the conductor's sweep transcript. I ran my own, case-insensitive, across the D2-1
value set **plus** the L-47 extension class — twice, once at each hash, with identical results:

| pattern | hits | adjudication |
|---|---:|---|
| `DEMOTED.OPEN` (prior state name) | 7 | 2 struck-in-lineage · 3 annotated `→ RULED OFF` · **2 tense-frozen at L-47** |
| `U9-6` | 3 | all three carry `~~…~~ → RULED OFF L-37(b)` |
| `306.83` | 2 | both inside the strike at `:1068–1069` |
| `316.5` | 5 | all correctly labelled pin-era / informative |
| `fixture_p06_state` · `u9_bonus_spawn_state` | 6 | `false` / `RULED-OFF` throughout |
| `5th body` / `fifth body` / `p06 hero` / `hero slot` | 7 | all struck or correctly framed |
| `MEASURED[ -]ON` · `RESOLVED[ -]ON` · `p06 (is\|=)? ?(ON\|true)` | — | zero surviving operative hits |

**Zero surviving unannotated live-tense hits on the spec, at both hashes.** The L-43(f) completeness
claim that D2-1 found false is now true of the artifact.

> **Scope caveat, stated because the artifact is live:** this exhaustion is certified at
> `ab93c513…` / 11:00:42. The file is under active edit. Any later fold re-opens the question for
> the material it adds — which is exactly what amendment **B** (§ 5) makes cheap to re-check.

**L-43(f) correction:** owned explicitly at L-45(a), quoting D2-1's own diagnosis back
(*"the set was right, the sweep wasn't run"*). Discharged.

**Standing-method registration:** landed at L-45(b), veto-open, and extended at L-47(f). Ratification
read at § 5.

---

## 2 — LEG 2: engine `cbb29e68` — **PASS**

Tracked tree at review time is **clean** (`git status --porcelain -uno` → empty); the working state
is untracked-only. Everything below was measured on my own instrument, not read from the commit
message.

### 2.1 — The defaults, as constructed

```
ConfigEncounter.fixture_p06_state   default = False      annotation = bool
Provenance.u9_bonus_spawn_state     default = "UNKNOWN"  annotation = str
```

End-to-end through the emitter, the emitted baton now carries
`fixture_p06_state=False, u9_bonus_spawn_state="UNKNOWN"` and validates with **zero** AC failures.
The state the emitter reaches **by doing nothing** is now the RULED state. That is precisely what
D2-1 required, and it is confirmed at the wire, not at the class definition.

### 2.2 — The vacuous-pass claim: **VERIFIED EXACTLY**

The commission asked me to verify star-lord's measurement that the old perturbation would pass
vacuously. It does. Full AC-11.4g truth table, measured:

| `fixture_p06_state` | `u9_bonus_spawn_state` | result |
|---|---|---|
| `True` | `"RESOLVED"` | PASS |
| `True` | `"UNKNOWN"` | **FAIL** ← the new perturbation, fires correctly |
| `False` | `"RESOLVED"` | FAIL |
| `False` | `"UNKNOWN"` | PASS ← **the old perturbation; would have passed vacuously** |
| `True` / `False` | `"RULED-OFF"` | FAIL / FAIL |

`_ac_11_4g(False, "UNKNOWN")` returns `None`. The claim is exact. **He measured it rather than
asserting it** — Discipline #10 — and that measurement is what makes BR-2's invert-don't-delete a
finding rather than a habit. It is the best thing in the commit.

`tests/test_baton_v1.py` → **51 passed**. The inverted test passes in isolation and asserts on the
specific AC id, so it cannot be satisfied by a collateral failure.

### 2.3 — The rest of the commit

- **Validator `:228` left UNCHANGED + anti-"repair" comment — correct.** A guard that is right
  should not be edited by a value fix, and the comment is the only thing that stops the next reader
  "restoring" the pair. Discipline #8.
- **ADR-004 reciprocation complete.** `export/MIGRATION.md` carries old/new defaults, the
  why-it-was-a-BLOCK paragraph, back-compat, and the type-gap fence. I reproduced the back-compat
  premise independently: `find . -name "*baton*.json*"` → **0 artifacts**, so no re-emission is owed.
- **Seam discipline held.** He did not touch `calibration.py:224` (gamora's) and did not edit
  `simulation/MIGRATION.md` (gamora's) despite his own MIGRATION entry closing her flag. Correct
  on both counts — see **R-7** for the bookkeeping residue.
- **Counts reproduced on my instrument at `cbb29e68`:** baton **51** · KC2 **155** (file-glob and
  `-k kc2` agree, so the selection basis is not a source of drift) · whole collection **10,361**.
  Blast radius 209 is subsumed by the full-suite result at § 3.

---

## 3 — LEG 3: the orphaned transcript — **ADJUDICATED**

> **The committed state at `cbb29e68` carries NO run-caused full-suite failures.**
> The orphan's 2 F's are `test_substrate_identity_loader` ×2 — **pre-existing tree**, already
> adjudicated at **L-39**, and they reproduce at `cbb29e68`.

### 3.1 — Provenance, settled by the clock

| artifact | time |
|---|---|
| **orphan transcript written** | **08:13** |
| `6927dee5` gamora beat-2 | 08:45:21 |
| `13451fdf` gamora beat-3 | 09:32:29 |
| `248f8738` star-lord docstring | 09:32:59 |
| **`cbb29e68` the commit under review** | **10:28:17** |

The orphan predates the commit under review by **three commits and 2 h 15 m**, and ran against a
mid-beat-2 working tree. It cannot be evidence about `cbb29e68` in either direction.

### 3.2 — The transcript is a WINDOW, not a census

The file is 20 lines, headed `=== SUITE PROCESS EXITED ===`, first visible progress line `[43%]`,
no summary. **Failures before 43 % are not absent from the run — they are absent from the file.**
"2 F's" is the count in a retained tail, and reading it as a failure total is a category error. My
own run at `cbb29e68` carries **45 F's before the 15 % mark** that a 20-line tail would not show.

### 3.3 — The two failures, NAMED

Signature match: orphan line `[51%]` = 2 F's separated by **11 dots**. My run at `cbb29e68`, line 75
`[52%]` = 2 F's separated by **11 dots** — same pair, shifted two positions by the +27 tests
`13451fdf` added after the orphan ran.

Named by positional index into the collection order:

```
tests/test_substrate_identity_loader.py::TestFoundationIntegration::test_rotating_elements_count_is_four
tests/test_substrate_identity_loader.py::TestFoundationIntegration::test_load_foundation_still_passes_element_count
```

**L-39's per-file tree census lists `substrate_identity_loader ×2`.** Exact match. Class:
**PRE-EXISTING TREE**, not D2-1 blast radius, not environment.

### 3.4 — Full-suite result at `cbb29e68`

Run by me, whole `tests/`, tracked tree clean. **Pre-registered before the run finished** (§ 3.3's
positional mapping let me predict it): 63 F / 21 E, per-file identical to L-39, zero novel failure
files.

```
63 failed, 10277 passed, 3 warnings, 21 errors in 1315.52s (0:21:55)   EXIT=1
```

**63 / 21 as predicted.** Per-file census from the `FAILED` / `ERROR` lines, against L-39's:

| file | mine @ `cbb29e68` | L-39 @ `2b562474` | class |
|---|---:|---:|---|
| `test_cycle12_layer4_convergence.py` | 33 | 33 | tree |
| `test_cycle12_layer6_t4_wireup.py` | 12 | 12 | tree |
| `test_foundation.py` | 4 | 4 | tree |
| `test_substrate_identity_loader.py` | **2** | **2** | tree ← **the orphan's two** |
| `test_wave5_swift_closure_path_x…` | 1 | 1 | tree |
| `test_no_canonical_four_in_llm_prompts.py` | 1 | 1 | tree |
| `test_kit_space_skill_naming.py` | 1 | 1 | tree |
| `test_dispatch_3b_phase5_seam1_pm1_gb.py` | 1 | 1 | tree |
| `test_cycle13_normal_season_export.py` | 1 | 1 | tree |
| `test_kit_space_emitter.py` | 4 | 4 | baseline |
| `test_wr2_d_nova_telegraph.py` | 2 | 2 | baseline |
| `test_wr1_m12_gd_mitigation_nova.py` | 1 | 1 | baseline |
| **failed** | **63** | **63** | 56 tree + 7 baseline |
| `test_cycle13_wave5_season_generation.py` (errors) | 21 | 21 | env (see R-8) |

**Every failing file and every erroring file is in L-39's adjudicated census, at the identical count.
Zero novel failure files. Zero novel error files. Run-caused failures attributable to `cbb29e68`:
ZERO.**

**And the growth is entirely green.** Collection **10,291 → 10,361 (+70)**; passed **10,207 →
10,277 (+70)**. Every test added since `2b562474` — the MO oracles, the s1 ramp, the baton
additions — passes. The failure set did not merely stay the same size; it stayed the same set.

`EXIT=1` is expected-red on the pre-existing tree, exactly as at L-39.

### 3.5 — This is the second instance of the same artifact

L-39 already wrote off gamora's own lap suite death — *"~55 %, unreturned, no summary"* — as MOOT as
evidence. The orphan is the same phenomenon at 51 %. Two instances is a pattern, and adjudicating it
case-by-case costs a full suite run each time. **Cheap standing fix:** background suite invocations
redirect to a file and append a terminal marker (`echo "EXIT=$?" >> …`), so an unreturned run is
distinguishable from a truncated one without re-running anything. That is how this run was made
adjudicable in one pass.

---

## 4 — FINDINGS

### R-1 — **WARN** — the corrected value is not pinned; the two-sided revert to the exact pre-fix state passes every guard

**Measured, on the emitted wire:**

| mutation | guards fired |
|---|---|
| one-sided revert `(True, "UNKNOWN")` | `AC-11.4g` — caught |
| one-sided revert `(False, "RESOLVED")` | `AC-11.4g` — caught |
| **two-sided revert `(True, "RESOLVED")` = the exact pre-fix state** | **NONE — all guards pass** |

D2-1 was a BLOCK because *"the superseded state is what the emitter reaches by doing nothing, and
every guard agrees with it."* The fix moved the default onto the ruled limb. **It did not change the
guard set.** The property "the emitter's do-nothing state agrees with the ruling" is still
**unpinned** — nothing in `tests/` asserts either default value; the only p06 test guards the
*mapping*. The three comment blocks are the whole defence, and comments are not a test.

**Cite:** Discipline **#8** (validate at the boundary) · Principle **#4**. **Not a BLOCK** — the value
is correct today and D2-1's stated unblock condition is met.
**Action:** star-lord — one test asserting the emitted defaults against **L-37(b)**
(`fixture_p06_state is False` and `u9_bonus_spawn_state == "UNKNOWN"` on the clean wire).
**ADR-002 test-addition tier — jack-ryan approved, no escalation.**

### R-2 — **WARN** — `run_p06_enabled` is the mirror hazard, and the only prior art is wrong

`baton_v1_emitter.py` contains **zero** references to p06 or `bonus_spawn`. The only module in the
repo that supplies `run_p06_enabled` is `baton_v1_fixture.py:362`, which hardcodes **`True`** — and
the baton I emitted carries `run_p06_enabled=True` while the sim of record runs
`calibration.py:224 S1_BONUS_SPAWNS_ENABLED = False`.

Not a live provenance defect: the fixture header disclaims every number in it, and the field is
required-with-no-default so it cannot be silently wrong. **But** at the Phase-E wiring it must be
sourced from the run config, and an executor searching for prior art finds the wrong value first.
That is the **D2-12 pattern exactly**, on the mirror field of the one D2-1 was about, at the emit
D2-1 was gating.

**Cite:** Principle **#3** · Discipline **#2**.
**Action:** conductor — register "`run_p06_enabled` sourced from the run config, not the fixture" as
a **Phase-E emit precondition**. star-lord — optionally retag `:362` `# FIXTURE VALUE — not the run
of record`, alongside the D2-12 retag already queued at `:61`.

### R-3 — **WARN** — sweep residual on the engine surface: one live-tense `DEMOTED-OPEN` survives

```
src/reincarnated/simulation/math/kc2-gd-wiring-relap-2026-08-08.md:354
  - **It does not resolve p06.** `u9_bonus_spawn_state` is **DEMOTED-OPEN** (L-33(g)); a galadriel
    probe is in flight.
```

Present tense, no strike, no annotation — and the probe has returned. It is the **L-47 extension's
own new value class** (prior state name), on a surface **inside** the standing method's declared
scope (*"the WHOLE artifact + code surfaces"*), and it survived. Every other `DEMOTED-OPEN` on the
engine surface carries lineage — `wave_engine.py:283/313/751`, `simulation/AGENT_STATE.md:17`,
`simulation/MIGRATION.md:27` — so this is an isolated corner, not a systemic miss.

It does **not** re-create the D2-1 condition (no consumer, no default, no guard agrees with it), and
the note's own § F convention is amend-in-place-with-a-dated-correction-block, which is the remedy.

**Why it matters more than its size:** star-lord could not have edited it (gamora's seam) and the
method gave him nowhere to record it. This is the seam between two sweeping hands, and it is the
evidence for ratification **amendment A**.

**Cite:** Discipline **#2** · Principle **#4**.
**Action:** gamora (via conductor) — dated correction block at `:354`, `→ RULED OFF (L-37(b)/F-10)`.

### R-4 — **INFO** — the queued rider is a MAPPING gap on one side and a TYPE gap on the other; it is two changes, not one

Measured: `u9_bonus_spawn_state` is annotated **`str`**, so `"RULED-OFF"` **is** an expressible
value — but `(False, "RULED-OFF")` **FAILS AC-11.4g**, because the validator's `expected = "RESOLVED"
if fixture is True else "UNKNOWN"` admits exactly two members. So on the `str` side the rider is a
**mapping widening**; on `fixture_p06_state: bool` it is a genuine **type extension**. The schema
comment's *"neither this `str` default nor the two-value mapping can carry"* is imprecise on the
first clause. Scoping matters because the spec's fixture YAML literally reads `RULED-OFF` and today
that value cannot round-trip.

**Action:** star-lord — one clause in the rider's scope at L-42(f)/L-43(f). No code change now.

### R-5 — **INFO** — citation-before-row: 13 live spec citations to `L-47` preceded the row by ~27 minutes

At 10:45 the spec carried **13** citations to **L-47** and the ledger's highest row was **L-46**. The
row landed at 10:51. **Self-cleared inside the fold**, so this is INFO and not WARN — but it is the
mirror of L-41(f)'s launch-then-record correction, inverted into cite-ahead-of-writing, and for those
27 minutes the artifact that goes to Matt pointed at nothing.

**Action:** companion rule, one line — *an annotation may cite the row being written at this fold,
and the fold does not close until that row is written.* Registered, not enforced retroactively.

### R-6 — **INFO** — no enumerated hit table exists on either hand

The commission describes star-lord's *"value-set hit table"* in the commit message and
`export/MIGRATION.md`. What is actually there is the **value set used**, the **surfaces swept**, and
the **one decisive hit** — which is more than the conductor's leg (prose in L-45(a)) and is why his
leg took me minutes to verify while the conductor's cost a full independent re-sweep. **Neither hand
produced an enumerated hit table with adjudications.** No criticism attaches: the method as written
does not ask for one. That asymmetry is the evidence for ratification **amendment B**.

### R-7 — **INFO** — the cross-seam flag closes in one direction only

`export/MIGRATION.md` closes gamora's flag and cites it by name. `simulation/MIGRATION.md:47–52`
still reads as open, with no back-pointer. star-lord was **right** not to edit her seam file. The
gap is the method's, not his — there is no handback step. Same root as R-3.

**Action:** gamora (via conductor) — one line on the flag: `CLOSED — export/MIGRATION.md [2026-08-08]`.

### R-8 — **INFO** — L-39 census corrigendum: the 21 env errors span two classes, not one

L-39 records the 21 errors as *"all `TestW5R3SeasonContentAuthoring`"*. Measured at `cbb29e68`:
**15 `TestW5R3SeasonContentAuthoring` + 6 `TestW5R2GauntletSimIntegration`**, both in
`tests/test_cycle13_wave5_season_generation.py`. Count, file and env-class adjudication are
**unchanged**; only the class attribution is one class short. Corrigendum forward, no re-litigation.

---

## 5 — RATIFICATION READ: the VALUE-SET SWEEP standing method

> ## **RATIFIED-AS-AMENDED** for OP § 4 + desirable-run-pattern § 6.5.
> The extension is correct and evidenced. It is **not yet sufficient**, and I have a live
> counter-example from this very fold (**R-3**). Three amendments, each with its own counter-example,
> before it graduates.

**The form under review.** L-45(b): (1) enumerate the claim's VALUE-SET — numerals, spellings,
abbreviations, derived percentages, code identifiers; (2) grep the WHOLE artifact + code surfaces,
never a remembered address list; (3) adjudicate EVERY hit operative/benign; (4) only then claim the
sweep — **before** any "fixed at this fold" claim. L-47(f) extends step (1) with **case-insensitive
matching** and **prior-STATE-NAMES-as-values**.

**Why the extension is right, and right in the right way.** It is derived from a **measured miss**,
not from theory: the un-extended pattern set did not hit the two AC-10.4 sites and the extended one
did. That is the correct provenance for a method amendment (Discipline #10). And the more important
of its two halves is the second: a superseded claim's **state name is a value of that claim**, exactly
as its numerals are. Without that term, a sweep retires the *conclusion* and leaves the *intermediate*
alive — which is what happened, because the D2-1 sweep-set was {p06 = ON · MEASURED ON · RESOLVED-ON ·
L-21 census}, four spellings of the ON limb and no term at all for the middle state `DEMOTED-OPEN`.

### Amendment A — declare the surface set, and HAND BACK what you may not edit

Step (2) names surfaces but no owner. This retirement was swept by **two hands** — the conductor over
the spec, star-lord over `src/` + `tests/` for the field-name set. Neither ran the *new* prior-state-name
class over the whole engine surface, and **R-3** is what fell through the seam. star-lord was correct
not to edit gamora's file; the method simply gave him nowhere to put it (**R-7** is the same gap on
the reciprocation side).

> **Amend:** the sweep declares its `(surface, owner)` pairs **before** it runs. Every hit on a surface
> the sweeper does not own is **handed back by name**. "Swept" is not claimable until the handbacks
> are placed.

### Amendment B — the sweep is discharged by a hit table, not by an assertion

Step (4) says "only then claim the sweep." **The claim that failed at L-43(f) was exactly of that
form** — *"fixed at this fold"* — and it was false. A method whose compliance is self-asserted cannot
repair a defect whose mechanism is self-assertion. **R-6** shows neither hand produced the artifact
this fold, and the verification asymmetry between the two legs is the argument.

> **Amend:** publish the pattern set, the surface set, and **every hit with its operative/benign
> adjudication**, in the artifact that carries the fix. This is what makes the method checkable at
> Gate 2 instead of re-derivable at Gate 2.

### Amendment C — a benign adjudication must record WHY

Step (3) requires adjudication but not a reason. On this artifact `L-21` appears many times and most
hits are correctly **benign** — L-21's bearing, timing and t+4.0 s start-anchor legs all survive;
**only its p06 census reading was superseded.** That distinction is load-bearing, it is recorded once
in L-45(a) prose, and it lives nowhere near the hits. The next sweeper either re-derives it or gets
it wrong.

> **Amend:** benign hits carry a one-clause reason, recorded once and cited by the hits.

### Landing and authority

**Content ratified; the OP § 4 and § 6.5 landing is gandalf's hand.** Per **ADR-002** this is a
documentation / process change and is **mine to approve — no Matt escalation**. Proposed § 6.5 title:
*"Superseded-claim retirement is a value-set sweep, not an address-list edit."*

**One escalation trigger, pre-registered.** This failure class has now run four folds — D-W3 at L-40,
~9 sites at L-41(e), 3 sites at D2-1/L-43(f), and R-3 at L-47. Registering it as a run-method at
L-45(b) was the right response and I am not second-guessing it. **If it recurs a fifth time after
amendments A–C are in force, it graduates from run-method to engineering discipline — and that one
is a Matt surface,** because it changes a project-wide standard rather than one run's practice.

---

## 6 — RUBRIC LAW: what this verdict's green covers (§ 6.3)

**COVERED — measured by me, at the pinned targets:**

1. The four D2-1 spec edits, the § 10.5 basis note, and the two L-47 AC-10.4 stragglers, at spec
   sha256 `705d4353…` **and re-verified at `ab93c513…` / 11:00:42**. The artifact is live-edited;
   the green does not extend past that hash.
2. **Exhaustion of the D2-1 value set — extended per L-47(f) — on the spec artifact.** Zero surviving
   unannotated live-tense hits.
3. Engine `cbb29e68` in full: all five files, the defaults as constructed, the AC-11.4g truth table,
   the vacuous-pass claim, the emitted-wire behaviour, and ADR-004 reciprocation.
4. Full-suite state at `cbb29e68` with a **clean tracked tree**, decomposed per-file against L-39.
5. The orphan's provenance, its two named failures, and their class.

**NOT COVERED — explicitly outside this verdict's green:**

1. **Everything else landed under the L-47 label.** L-47(e) records a **12-edit spec batch** — the
   § 14 F-13 full block, § 10.6 geometry-residency rewrite, F-9/F-10 status edits, § 12 T-3, the
   D2-2 digits annotation and the D2-3 survivor-gloss restatement. Those are the L-45(f) deferred
   batch plus the F-13 fold. **I reviewed none of them.** They are a separate Gate-2 surface and my
   green says nothing about them.
2. The **type/mapping rider** (L-42(f)/L-43(f)) — still queued; R-4 refines its scope only.
3. **D2-2 … D2-15** — open per their own L-45(d) dispositions; only D2-1 is re-verdicted here.
4. The **F-11 tree-state fork**. The Phase-E emit is unblocked *on D2-1 grounds*; it remains
   constrained by `AC-11.4e` while the tree grades `dirty`, and that is Matt's fork, not mine.
5. `run_p06_enabled` at the real Phase-E wiring (R-2) — a **forward** precondition, not a present
   defect, and not certified by this green.
6. The **locomotion lap**, the **legolas probe fold**, and the **galadriel fifth extraction**.
7. **Push.** Not fired, not authorised, not in scope.

**The green is narrow on purpose.** D2-1 named one defect with one unblock condition; this verdict
measures that condition and nothing adjacent to it.

---

## 7 — Instruments

- Spec / ledger sweeps: `grep -n -i -E` over the pinned files; hashes recorded in the header.
- AC-11.4g truth table and the reversion probes: direct calls to `_ac_11_4g` and
  `validate_baton_wire` on an emitter-built wire (`build_baton` + `to_wire`, `tree_state_override="dirty"`).
- Failure attribution: positional index of every `F` / `E` in the progress stream into
  `pytest tests/ --collect-only -q` order (10,361 items) — this is how the two orphan failures were
  named without a summary line.
- Counts: `--collect-only` on `tests/test_baton_v1.py`, `tests/test_kc2_*.py`, `-k kc2`, and `tests/`.
- Full suite: `python3 -m pytest tests/ -q`, single run, 21:55, transcript
  `/tmp/jr-reverdict/fullsuite-cbb29e68.txt`; per-file census from its `FAILED` / `ERROR` lines.

---

**Filed:** jack-ryan, DEV-MODE Gate-2 D2-1 re-verdict, 2026-08-08, KC2-SIM.
Spec, ledger and engine **not edited** (findings route back through this note).
Engine tracked tree verified clean at `cbb29e68` on exit; engine work was **read-and-run only** per
the commission. **Nothing committed** — this note is UNCOMMITTED and rides the fold, alongside the
conductor's live spec/ledger working copy. **Push NOT fired.**
