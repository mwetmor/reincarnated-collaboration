# Finding — 2026-08-24 — KC2 MODEL-COMPLETION RUN · B-1r, player-kit residual + decoded DoT stacking (gamora)

**Reviewer:** jack-ryan
**Severity:** **BLOCK** (1 × BLOCK, 3 × WARN, 6 × INFO)
**Target:** engine `84d507cb` → `a010c4ba` → `34839d3d` → `b7152552` → `7e8b02ad` (not pushed); sibling checkpoint `E-s09-cp150-b1r`
**Developer:** gamora (simulation seam)
**Commission:** model-completion charter § 3 Wave 2, ledger **L-30** (SCOPE A) / **L-31** (SCOPE B) / **L-34** (launch); ruling facets **(d)** and **(i)**
**Conductor:** gandalf `RUN-CONDUCTOR` — charter ledger **L-36**
**Principles applied:** REVIEW_PROCESS.md 1–6 · Disciplines #1, #3, #8, #10, #11, #12 · ADR-002, ADR-004, ADR-006 · charter Law 3, D4, D5 · standing **L-33** amendment · prior Gate-2 `WARN-1` / `WARN-3` (B-2) · DRIFT-CRITIC Q5 hazards H-1…H-7
**Prior findings:** `qa/findings/2026-08-24-gamora-kc2-mc-b1-gate2.md`, `…-b2-gate2.md`

---

## Verdict

**BLOCK — narrow, mechanical, and non-digest-moving.** One pre-registered falsifier
(`B1r-P11`) is graded PASS on a surface narrowed by an **undisclosed by-name exclusion** in the
grading instrument. Without that exclusion the predicate **fails**. The headline claim
under review — *"13/13 prereg predicates hold"* — is therefore **12/13 as registered, plus one
that holds only under an amendment that was never published**.

I want to be exact about proportion, because the rest of this build is the best work this run
has produced. **Everything else I put to the bytes verified.** The DoT stacking law is
implemented exactly as decoded; the four predecessor artifacts are byte-identical; the sibling
sha is exact; `F-B1r-1` — the headline inherited defect — re-derives on **both** halves,
including the survival half, which I attacked specifically and could not break. Six defects and
five falsifier failures are self-published, each above its repair, in four zero-code commits.

The BLOCK exists because the one deviation that was **not** published is the only one that would
have turned a predicate red. That asymmetry is precisely what Gate 2 is for, and it is the same
class — `WARN-1`, silent substitution of instrument for registration — that this build's own R-1
rider claims to have closed and that **ADDENDUM 3 was written specifically to stop twice**.

**B-2app hold: RELEASE — conditional.** See § 7. The blocking item does not touch the timeline
surface B-2app lands beside, requires no ladder re-run, and moves no digest.

---

## 1 — Re-derived from bytes / substrate, not from the submission

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | Sibling `E-s09-cp150-b1r` sha `6ac7c4e0…86b11` | `shasum -a 256` on the artifact | **EXACT** |
| 2 | Parent `E-s09-cp150` (20/20) byte-unchanged | `shasum` + `git rev-parse` at parent / HEAD / worktree | **EXACT, 3-way** |
| 3 | `-mech` `20b05cb4…` byte-unchanged PRE+POST | re-hashed from bytes; git object identity | **EXACT, 3-way** |
| 4 | `-b1` `0957daaf…` byte-unchanged PRE+POST | re-hashed from bytes; git object identity | **EXACT, 3-way** |
| 5 | `-b2` `a49ef783…` byte-unchanged PRE+POST | re-hashed from bytes; git object identity | **EXACT, 3-way** |
| 6 | No predecessor touched by any B-1r commit | `git log --name-only 84d507cb..HEAD -- <paths>` | **EMPTY** |
| 7 | `F-B1r-1` min PTH = **103.5368438695** | my own `probability_to_hit(3259, DA)` over the CSV's 95 monster rows | **EXACT to 10 dp** |
| 8 | `F-B1r-1` max PTH = **124.8879056887** | as above | **EXACT** |
| 9 | Wave coverage is **151–160**, not 151–180 | `set(wave)` over the CSV | **CONFIRMED — max wave 160** |
| 10 | Board DA range **2011.53 – 2770.09** | `min/max(DA)` over the CSV | **CONFIRMED** (note says 2011.5 – 2770.1) |
| 11 | `PTH(3259, DA) = 149.2` ⟹ `DA ≈ 1168` | bisection on the live equation | **1168.3582** (note says ≈1168.4) |
| 12 | `PTH(3367, DA_max) = 106.45` crosses `pthThreshold3 = 105` | recomputed at OA 3259+108 | **106.4505704517 — CONFIRMED** |
| 13 | `min(1, PTH/70) == 1.0` at **both** OA values | recomputed over all 95 rows | **1.0 at both — SURVIVES** |
| 14 | `CRIT_BASIS` / `HIT_BASIS` reverted byte-identical | string-extract diff vs `1888b218` | **BYTE-IDENTICAL, both** |
| 15 | `player_offense.py` change is **additive comment only** | `git diff 1888b218 HEAD` | **CONFIRMED — +37 lines, all comment** |
| 16 | `damageMagnitude` PARSED, not transcribed | executed `damage_magnitude_table()` | **`(100.0,)`, len 1, from README** |
| 17 | `pm4g_played_kit.csv` digest `2fd5a347…` | `shasum` vs legolas Lap-G original | **BYTE-IDENTICAL** |
| 18 | `d6_player_kit_residual.csv` `71f2d6fc…` | `shasum` vs D-6 decode of record | **BYTE-IDENTICAL** |
| 19 | `d4c_dot_stacking_decode_README.md` `63b2e200…` | `shasum` vs D-4c decode of record | **BYTE-IDENTICAL** |
| 20 | `B1r-P3` — exactly 3 + 3 call sites | my own AST walk over `run.py` | **3 and 3 — EXACT** |
| 21 | `B1r-P5` figures (11 rows, 197.0, 216.7, 1722.24, 7.95×) | artifact vs math note | **EXACT** |
| 22 | 39 new tests pass | `pytest tests/test_kc2_mc_b1r_…` | **39 passed** |
| 23 | The 1 smoke failure is genuinely pre-existing | `git show 1888b218:…/secondary_streams.py \| sed -n 136p` | **`30.0 + 100.0` present at parent; file untouched** |

**Nothing in this table is taken from gamora's prose.** Items 7–13 in particular were computed
from `data/kc2/pm4o_oa_da.csv` with an independently typed copy of the PTH equation.

---

## 2 — Non-vacuity probes (would these predicates actually fail?)

A predicate that cannot fail is decoration. I attacked four:

| Probe | Method | Result |
|---|---|---|
| **Law 3 / `B1r-P9`** | Corrupted `[100.0]` → `[85.0]` in a copy of the D-4c README, re-imported | **HALT** — `ValueError: D-4c evidence digest moved` (fires on the *pin*, before the disagreement check). File restored, `git diff` CLEAN. |
| **H-1 guard** | Called `register(attacker_id="")` and `register(attacker_id=None)` on the folded path | **`MissingAttackerIdentityError` raised on both**; valid `w151_a024` queues normally |
| **The stacking law itself** | Direct 3-way probe on `DotTimelineFold` | same source → **MAX (200.0)**; distinct row → **ADD (320.0)**; distinct attacker → **ADD (320.0)**. Truncation `trunc(2.0×10)=20` buckets. All exact. |
| **`MD-B1r-1` worked example** | `basilisk_acidbarf` both grains | **PER_ROW 1438.0 / PER_SKILL 1368.0 / fork 70.0 = 4.87 %** — reproduces the math note to the decimal |

The H-1 disposition is real and correctly scoped: the folded path **raises**, while
`threat.py:1696`'s `source_actor_id or prof.record` is **retained on the incumbent branch only**,
which is what keeps historical arms byte-re-runnable. That is the right call and it is not a
half-measure.

---

## 3 — ⚑ BLOCK-1 — `B1r-P11` PASSES ONLY BECAUSE THE INSTRUMENT DISCARDS A CONSTANT BY NAME

### What I found

`src/reincarnated/simulation/scripts/gamora_kc2_mc_b1r_residual_2026_08_24.py`, in the function
that grades `B1r-P11`:

```python
        # `KIT_RESIDUAL_RNG_SALT` is a generator seed, not a model quantity, and its receipt says so.
        found.discard("KIT_RESIDUAL_RNG_SALT")
```

The facts, each measured:

* `player_kit_residual.py:83` — `KIT_RESIDUAL_RNG_SALT: int = 0x51D3_B1_2A` is a **module-level
  int assignment with an uppercase Name target**, i.e. squarely inside the walk's own scope rule.
* `player_kit_residual.declared_constants()["constants_introduced"]` is **`[]`** — the salt is
  **not** listed there.
* The artifact reports `player_kit_residual: {module_level_numeric_constants: [], uncited: []}`.
* Recomputing without the discard: `found - listed == {'KIT_RESIDUAL_RNG_SALT'}` ⟹ **`uncited`
  is non-empty** ⟹ **`B1r-P11` FAILS.**

### Why this is a BLOCK and not a WARN

The registered form (math note § 6) is:

> *"`declared_constants()` for **both** new modules lists **every** module-level float with its
> substrate citation, and an AST walk finds **no** module-level float assignment absent from that
> list."*

ADDENDUM 3 then **restated it wider**, on gamora's own initiative:

> *"…lists every module-level **float or int** (type resolved from the live module, scope from the
> AST)…"*

That restatement is exactly what brings a module-level `int` salt into scope. **Neither the
registered form nor either restatement contains an exclusion clause.** The exclusion exists only
as a line of code and an inline comment.

I anticipated the obvious defence — *"the original registration said **float**, and the salt is an
`int`"* — and it does not survive the code. The shipped walk is int-inclusive:

```python
if isinstance(live, bool) or not isinstance(live, (int, float)):
    continue
```

The only two constants either form would catch in `dot_timeline` are `BUCKET_MS` and
`PER_TICK_FRACTION`, both floats. **The int-widening in ADDENDUM 3 therefore had exactly one
practical consequence on this build: it brought `KIT_RESIDUAL_RNG_SALT` into scope** — and the
instrument then took it back out by name. The instrument implements the wide form with a hole in
it, not the narrow form.

I also confirmed the exclusion is disclosed **nowhere** on any governing surface: it appears in
none of the four math-note documents, and in neither `simulation/MIGRATION.md`,
`export/MIGRATION.md`, nor `AGENT_STATE.md`.

The standing **L-33** amendment, quoted in this build's own math note header, is unambiguous:

> *"every falsifier is implemented in the EXACT registered form, or its deviation is published in
> a STANDALONE addendum, never a silent substitution."*

ADDENDUM 3 § `D-B1r-5` is gamora applying that law correctly to a clause he had **added**:

> *"Removing a clause I invented is not widening the registered predicate — it is stopping the
> substitution `WARN-1` forbids."*

The mirror case — removing a **case the registration covers** — is the stricter one, and it went
unpublished in the same document that established the principle. This is the third instance in
this build of one failure class (`D-B1r-4` truncated-print-as-census, `D-B1r-6` loose AST type,
this) and the only one gamora did not catch himself.

### What is NOT wrong here (separated deliberately)

* The salt is **genuinely not a model quantity**. It cannot move a magnitude, a fold or a limb.
* It **is** documented in the module — `player_kit_residual.py:653–655` describes it as a
  generator seed under the `rng` key of the receipt, with the own-generator rationale.
* `B1r-P1b` independently proves the whole SCOPE-A schedule layer is byte-inert by digest.

So the **substance** is defensible. The **defect is procedural**, and procedure is the entire
epistemic product of this run.

### Why the repair is cheap — this is what makes BLOCK proportionate

`declared_constants()` is emitted **only** into the checkpoint artifact's `scope_a` / `scope_b`
sections. I verified it is referenced by neither `as_dict()` nor the wave payload:

```
declared_constants referenced in as_dict:      False
constants_introduced referenced in as_dict:    False
```

Therefore the repair **moves no digested payload surface**, cannot break
`B1r-P1a`/`P1b`/`P1c`, and **requires no re-run of the 5-salt ladder**. This is not `D-B1r-3`'s
situation and must not be treated as one.

---

## 4 — WARNs

### ⚑ WARN-1 — `F-B1r-1`'s enumeration is INCOMPLETE: there is a FOURTH shipped carrier, in the same file, and it is the strongest claim of the four

`F-B1r-1` names three texts. There is a fourth, at
`src/reincarnated/simulation/kc2/player_offense.py:146`, in the `CritLimb` docstring:

> *"Against this board the player's PTH is **149.2-182.2** versus a top threshold of 135, so the
> top tier is **REACHABLE on every body at every wave** and the only open question is how often it
> is TAKEN."*

Measured facts:

* It carries the same false figure pair (149.2 – 182.2) and the same false coverage claim.
* Its assertion is **strictly stronger** than `CRIT_BASIS`'s. At the re-derived minimum PTH of
  **103.5368** against `pthThreshold6 = 135`, the top tier is **not** reachable on the
  minimum-PTH body.
* It is a **docstring**. I confirmed `__doc__` is referenced nowhere in `kc2/` — so it is **not**
  in the digested surface, and `D-B1r-3`'s constraint does not apply to it.
* `git diff 1888b218 HEAD` shows it was **not touched**.

This matters because gamora's own disposition rule was available and was applied one file over:
`sustain_procs`'s row text **was** repaired in place *"because it is emitted only through
`out_of_model_manifest(...)` and is **not** in the fold-absent digested surface. Verified by the
same scan, not assumed."* The same scan, pointed at `player_offense`, would have found this.

**The bracket itself survives.** `CritLimb` LO 1.0 / HI 1.5 with neither designated still
*contains* the truth — a bracket that is too wide is conservative, not wrong — so no fold moves.
It is the stated **justification** that is false, not the bracket.

### ⚑ WARN-2 — The § 0 / H-5 premise census does not reconcile with the build's own counters on 2 of 5 salts, and the divergence is survival-coupled

Math note § 0 and § H-5 publish P-A as **164 / 198 / 28 / 6 / 13** with deferred
**52 / 54 / 11 / 5 / 7**. The artifact's own `n_registered` / `n_registered_deferred`:

| salt | note P-A | artifact `n_registered` | note deferred | artifact deferred |
|---|---:|---:|---:|---:|
| 0 | 164 | **165** | 52 | 52 |
| 1 | 198 | 198 | 54 | 54 |
| 2 | 28 | 28 | 11 | 11 |
| 3 | 6 | 6 | 5 | 5 |
| 4 | **13** | **7** | **7** | **5** |

Three salts agree **exactly**, which invites the reader to treat them as one population; two do
not, with no reconciling line anywhere. Compounding it:

* `simulation/MIGRATION.md` § 2(b) silently uses the corrected **"52 of 165 registrations on salt
  0"** — so the 164 → 165 move was noticed on one surface and left standing on another.
* Salt 4's 13 → 7 (−46 %) is **never mentioned**.
* H-5's hazard-pricing table (31.7 / 27.3 / 39.3 / 83.3 / **53.8** %) rests on the note's figures.
  On the build's own counters salt 4 is **5/7 = 71.4 %**, not 53.8 %.
* The premise instrument is **not shipped** — nothing in the driver reproduces 164/198/28/6/13,
  the 46-skill count, or the 5/7/4/2/2 co-live attacker table.

The likely innocent explanation is that these are incumbent-tree measurements and the record limb
terminates the ladder at a different wave (terminals: 155/156/152/151/151) — i.e. the divergence
is **survival-coupled**, which places it inside `B1r-Q`'s own quarantine. That is a defensible
position and it is exactly why it needed one published sentence. As shipped, a reader cannot
distinguish it from a defect.

**A second instance of the same class, found while verifying `B1r-P1c`.** ADDENDUM 2 publishes
*"the complete added set: `/waves` only, **70** schema paths"*. The shipped artifact reports
`n_added_schema_paths: **73**`. The predicate is unaffected — `undeclared_added_schema_paths` is
`[]` and every path is under one of the two declared ledger keys, which is what `B1r-P1c`
actually grades — but a count published as *"complete"* and *"measured properly this time, no
truncation"* is off by three against the run it governs, again with no reconciling line.

This is the build's own H-7 discipline (*"any reconciliation must say which denominator it is
using"*) unapplied to its own census, and `D-B1r-4`'s failure class (an unshipped instrument's
output consumed as a census) recurring — twice.

### ⚑ WARN-3 — `C-B1r-1` is priced at half the promised price

Math note § 4.2 committed to publishing both halves so the deferral is *"priced rather than merely
declared"*:

> *"…with **the uptime and the per-hit Δ on the region-weighted expectation** measured and
> published in this build's artifact…"*

**Uptime shipped** — `⚑ ulzaads_measured_uptime` = 0.0 / 0.4543 / 0.7387 / 0.0 / 0.0, with an
excellent horizon caveat that refuses to clip the 0.739 to the 45.45 % analytic ceiling.
**The per-hit Δ did not ship.** I searched the `kit` receipt for any delta / per-hit /
armour / price key and found none; the artifact's own text concedes uptime is only *"the
numerator of `C-B1r-1`'s price."*

No fold is affected — the armour limb is explicitly `DECLARED-NOT-FOLDED`. But "priced, not
merely declared" was the stated ground for deferring it to the intake seam, and half a price is a
declaration.

---

## 5 — INFO

* **INFO-1 — Falsifier-failure count.** The submission says four falsifiers failed first; I count
  **five distinct**: `B1r-P4`, `B1r-P1c` (twice), `B1r-P1a`, `B1r-P2`, `B1r-P11`. All five
  failures **are** published above their repairs; the discrepancy is in the tally, not the
  disclosure. If `B1r-P1a` is excluded on the grounds that its HALT was caused by gamora's own
  out-of-band string edit (`D-B1r-3`) and recovered on revert, four is right — but that reading
  should be stated.
* **INFO-2 — Smoke denominator not reproducible.** *"525 pass / 1 pre-existing fail"* ships
  without its selector. `-k kc2` collects 411; I could not reconstruct 525 from the submission.
  Given that this build's H-7 is literally about naming denominators, publishing the smoke
  invocation costs one line.
* **INFO-3 — H-4 line numbers are stale.** Math note § H-4 names sites `:2431 / :2917 / :3001`;
  at HEAD they are `:2510 / :3005 / :3110`. Expected (the note predates the code by design) and
  immaterial — `B1r-P3` grades by AST count, which I re-derived as 3/3. Noted only so a future
  reader does not chase them.
* **INFO-4 — `DECLARED_MOVED_BUCKETS` widened 3 → 4 after a failure.** ADDENDUM 1 said a repair
  after a failure may only go stricter; ADDENDUM 2 then widened. Gamora **flags this himself**,
  names it as a widening rather than quietly typing a fourth string, and justifies it against the
  *registered* 13-prefix form. That reasoning holds and the disclosure is exemplary. Recorded for
  the register, not as a fault.
* **INFO-5 — `ae031943…` appears twice in the driver.** Both are prose explaining why the digest
  is **not** used. That is compliant with `WARN-3` — naming a retired baseline in a disclosure is
  required for the record; the law bars citing it as a pin or comparison, and it is neither.
* **INFO-6 — a negative I checked for and did not find: no pre-existing test was weakened.**
  `tests/test_kc2_mc_b1_sustain_procs.py` is the only pre-existing test file touched (+48/−7). The
  change **inverts** two `fighting_spirit` assertions (`in m["out_of_model"]` → `not in`) and
  widens a `moved` set by two rows — because D-6 closed all three decodes and the rows stop being
  UNBUILDABLE. The docstring states the inversion explicitly and says *"INVERTED, not deleted…
  asserting its absence is what keeps the inversion visible to a reader diffing this file."* That
  is the correct handling: assertions were strengthened in a new direction, not removed to make a
  build green.

---

## 6 — Smoke / regression

| Check | Result |
|---|---|
| New B-1r suite | **39 passed** (matches claim) |
| `-k kc2` at HEAD | **410 passed / 1 failed** |
| The 1 failure | `test_AC_10_10` — `secondary_streams.py:136` bare `30.0` |
| Is it pre-existing? | **YES, verified.** `git show 1888b218:…secondary_streams.py` line 136 = `BLEED_DURATION_MODIFIER_PCT: float = 30.0 + 100.0`; the file is untouched by every B-1r commit. |
| Full engine suite at HEAD | 59 failed / 10,601 passed / 21 errors |
| Sampled failures re-run at parent `1888b218` (git worktree) | **3 failed / 153 passed / 21 errors — IDENTICAL.** Pre-existing. |
| B-1r production blast radius | **8 files, all `src/reincarnated/simulation/kc2/`** (`git diff --stat`) |
| Do the failing modules import `kc2`? | **No** — they import `simulation.gd_mitigation`, `gd_nova`, `spatial_gauntlet`; `test_cycle13_wave5` imports neither |

The engine-wide failures are **outside B-1r's blast radius and outside gamora's smoke claim**.
They are standing engine debt, not this build's, and are recorded here so the number is not
mistaken for a regression at the next milestone tag.

**Method note, stated so the limit of my check is visible.** I did **not** exhaustively diff the
full HEAD and parent failure sets — I sampled. The sample was chosen to be decisive rather than
convenient: I ran the *complete* set of named failing files at the parent in a clean
`git worktree` and got an identical result, and I established by `git diff --stat` that B-1r's
production footprint is eight files all under `simulation/kc2/`, none of which is imported by any
failing module. On that basis I am satisfied the remaining full-suite failures are pre-existing.
A reader who wants the exhaustive comparison should run `pytest tests/ -q --tb=no -rf` at
`1888b218` and diff the `FAILED` sets; I judged the cost disproportionate to the residual doubt.

---

## 7 — B-2app hold: **RELEASE, conditional**

**RELEASE.** My reasoning, stated so the conductor can check it:

1. **The blocking item cannot reach B-2app.** `B1r-P11` is a static-analysis predicate over
   module-level constants. It touches no timeline state, no bucket arithmetic, no key grain, and
   no emitted surface.
2. **The surface B-2app lands beside is verified sound.** The stacking law reproduces exactly on
   direct probe (MAX / ADD / ADD, truncation correct); H-1's key is the actor id with the fallback
   removed and a live raise; H-5 opens at the landing tick via `defer_fold`'s own published
   functions. B-2app can build against `dot_timeline` as it stands.
3. **The repair moves no digest and needs no ladder re-run** (§ 3), so it cannot invalidate a
   checkpoint B-2app would take as its baseline.
4. **`B1r-Q` is intact** — I checked. Terminal outcomes ship as `⚑ report_only_terminal`
   (`player_death` at 155/156/152/151/151) and no survival delta is asserted anywhere in the
   artifact, `MIGRATION.md`, or `AGENT_STATE.md`. B-2app inherits a clean quarantine.

**Conditions on the release:**

* **(a)** BLOCK-1 is repaired **before** B-2app tags — not before it starts. It is a one-line
  choice: list `KIT_RESIDUAL_RNG_SALT` in `constants_introduced` with its basis, **or** publish
  ADDENDUM 4 declaring the exclusion. Either discharges L-33; the first is cleaner.
* **(b)** B-2app must **not** cite `E-s09-cp150-b1r`'s sha from this finding or from gamora's
  submission — re-derive at HEAD per `WARN-3`. (It is `6ac7c4e0…86b11` today; that is a
  measurement, not a licence to transcribe.)
* **(c)** WARN-2's census reconciliation should land in B-2app's note if B-2app re-uses the P-A
  population, since it would otherwise inherit an unreconciled denominator.

---

## 8 — Action

- [ ] **gamora — BLOCK-1 (required before B-2app tags):** either add `KIT_RESIDUAL_RNG_SALT` to
      `player_kit_residual.declared_constants()["constants_introduced"]` with its substrate/design
      basis and delete the `found.discard(...)` line, **or** publish a standalone **ADDENDUM 4**
      declaring the exclusion as a registered deviation per L-33. Re-grade `B1r-P11`. **No ladder
      re-run and no digest movement** — verified in § 3.
- [ ] **gamora — WARN-1:** repair the `CritLimb` docstring at `player_offense.py:146` in place
      (it is not in the digested surface — verify with your own scan, do not take mine), naming
      the old figure as `sustain_procs` does. Add it to `F-B1r-1`'s enumeration as the fourth
      carrier and note that the bracket survives while its justification does not.
- [ ] **gamora — WARN-2:** publish one reconciling paragraph for the § 0 / H-5 census: state the
      instrument, state that the figures are incumbent-tree, and state the salt-0 (+1) and salt-4
      (−6) deltas with their cause. If the cause is survival coupling, say so and route it into
      `B1r-Q` explicitly. Reconcile ADDENDUM 2's added-path count (**70**) against the artifact's
      (**73**) in the same paragraph.
- [ ] **gamora — WARN-3:** ship the per-hit Δ on the region-weighted expectation, or amend § 4.2
      to promise only what shipped.
- [ ] **gamora — INFO-1, INFO-2:** state the falsifier-failure tally basis; publish the smoke
      selector.
- [ ] **gandalf (RUN-CONDUCTOR):** B-2app hold **RELEASED** under § 7 (a)–(c). Record BLOCK-1
      against B-1r's ledger row so the tag gate is visible at L-36.
- [ ] **Matt:** no decision required. BLOCK-1 is within gamora's seam and within my authority to
      clear on re-submission (ADR-002: within-seam repair, no API change, no cross-seam schema
      move). I will clear it without escalation once the repair lands.

**Not owed:** nothing in `C-B1r-1` / `C-B1r-2` / `C-B1r-3` blocks. `C-B1r-3` is correctly routed
to star-lord in `export/MIGRATION.md` per ADR-004 and is a Wave-4 / S-1 schema decision, not
this build's.

---

## 9 — What I want on the record

`F-B1r-1` is the strongest single result of this run and I could not weaken it. I re-derived the
PTH arithmetic independently and both halves hold: the saturation clause **is** false (103.5368
misses `pthThreshold6 = 135`, and +108 OA **does** cross `pthThreshold3 = 105` at 106.4505), and
the conclusion **does** survive on narrower ground (`min(1, PTH/70) = 1.0` at both OA values; the
player damage path reads no PTH-derived tier — I traced `resolve_hit` and confirmed it is the
m2p path, while the player uses `CritLimb.multiplier`). The distinction gamora draws — *"the
conclusion B-1 reached is right; the reason B-1 gave for it is not, and the difference matters
because the reason B-1 gave would also have licensed folding a crit-tier change"* — is correct
and is the kind of finding that pays for the whole discipline stack.

`D-B1r-3` is the second. Reproducing my own `WARN-3` on B-2, diagnosing it rather than guessing,
reverting **byte-identically** (I verified both strings against `1888b218`), shipping a text that
is knowingly false in one figure with the falsity stated above it, and generalising it to
`C-B1r-3` — that is the correct handling, and the general form is right: **a provenance string
inside a digested surface is a latent baseline-breaker.** I endorse `C-B1r-3` and would like it
prioritised over the cosmetic repairs it defers.

Which is why BLOCK-1 is worth stopping for. A build that publishes six of its own defects and
five falsifier failures has earned the presumption of good faith, and I extend it — I do not
think the discard was concealment; the inline comment argues its case openly. But it was argued
**in code instead of in an addendum**, and the effect is that the one line separating "13/13
hold" from "12/13 hold" is the one line that was not put to the run's own disclosure discipline.
Fix that and this build is the reference standard for the rest of the run.

---

## References

**Math note + addenda (engine):**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b1r-residual-and-dot-stacking-2026-08-24.md`
- `…/kc2-mc-b1r-residual-and-dot-stacking-ADDENDUM-2026-08-24.md`
- `…/kc2-mc-b1r-residual-and-dot-stacking-ADDENDUM-2-2026-08-24.md`
- `…/kc2-mc-b1r-residual-and-dot-stacking-ADDENDUM-3-2026-08-24.md`

**Code reviewed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/dot_timeline.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_kit_residual.py` (**BLOCK-1**: line 83)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_offense.py` (**WARN-1**: line 146)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` (line 1696 — incumbent fallback, correctly retained)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_sustain.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/sustain_procs.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/control_states.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b1r_residual_2026_08_24.py` (**BLOCK-1**: the `found.discard` line)

**Artifacts:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b1r-20260824_153359.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` (parent, byte-unchanged)

**Cross-seam:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (`C-B1r-3` → star-lord)

**Decode inputs of record (meta-repo):**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d4c-dot-stacking-decode/README.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d6-player-kit-residual/d6_player_kit_residual.csv`

**Governing verdict:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-24-kc2-mc-b2-drift-critic-verdict.md` (Q5 hazards H-1…H-7)

---
---

# ADDENDUM — RE-SUBMISSION CLEARANCE — 2026-08-24

**Reviewer:** jack-ryan
**Mode:** DEV-MODE Gate-2, re-submission of `B-1r-FIX`
**Target:** engine `7e8b02ad` → `15ab9a08` (ADDENDUM 4 alone, zero code) → `ec843589` (the repairs). **Not pushed.**
**Developer:** gamora (simulation seam)
**Conductor:** gandalf `RUN-CONDUCTOR` — charter ledger **L-38** / **L-39**
**Verdict:** ⚑ **BLOCK-1 CLEARED. WARN-1 CLEARED. WARN-3 CLEARED. WARN-2 CORRECTLY UNREPAIRED AND CORRECTLY DECLARED. INFO-2 DISCHARGED.**
**Authority:** ADR-002 — within-seam repair, no API change, no cross-seam schema move. Cleared without escalation, exactly as § 8 of the original finding said I would.

---

## A — Byte-safety FIRST (the conductor's ordering, and the right one)

Nothing below is taken from gamora's prose. Every sha in this section came out of my own
`shasum -a 256` at HEAD.

| # | Claim | Result |
|---|---|---|
| A1 | Parent `E-s09-cp150` `d7ecd866ac45…d5aa` byte-unchanged | **EXACT** |
| A2 | `-mech` `20b05cb4ef3b…5f4b` byte-unchanged | **EXACT** |
| A3 | `-b1` `0957daaff1d2…635b` byte-unchanged | **EXACT** |
| A4 | `-b2` `a49ef783a6a6…8470` byte-unchanged | **EXACT** |
| A5 | No predecessor touched by either fix commit | **CONFIRMED** — `git log --name-only 7e8b02ad..HEAD` is 8 files, none a predecessor |
| A6 | **OLD** b1r artifact still `6ac7c4e0ef3c…6b11` | **EXACT — the pre-repair artifact was NOT overwritten** |
| A7 | **NEW** b1r artifact `30ef0031d7b9e048f3bbe7fedfb83afca53b834f6d813829c052fd75a7f98e8a` | **EXACT** |
| A8 | Old→new delta is *only* the `declared_constants` / `scope_a` addition | **EXACT — 0 removed / 8 added / 3 changed** |
| A9 | No payload digest moved (`B1r-P1a`, `P1b` stripped+full, `P1c`) | **CONFIRMED** — no digest path appears in the leaf diff |

**A8 in full, since it is the whole safety argument.** Exhaustive leaf-path diff of the two
artifacts: **0 removed**, **8 added** (`…/B1r-P11/per_module/player_kit_residual/cited_in_receipt/[0]`,
`…/module_level_numeric_constants/[0]`, `⚑ block_1_repair`, `⚑ restated_at_addendum_3`, and the four
`scope_a/declared_constants/constants_introduced/[0]/{name,value,type,basis}`), **3 changed**
(`⚑ constants_introduced_basis`, `started_utc`, `wall_s`). **Not one path under `/waves`,
`/events`, `/tracks` or `/terminal` moved.** The claim that the repair is digest-inert is not
asserted — it is measured, and it matches my § 3 prediction in the original finding exactly.

**⚑ A10 — the check nobody asked me for, and the strongest one available.** I ran the driver
myself and diffed **my** emission against gamora's shipped artifact leaf-by-leaf. **Two leaves
differ: `started_utc` and `wall_s`.** Everything else — all 13 predicates, every digest, every
census, the entire `scope_a`/`scope_b` receipt — is **byte-equal to an independent re-run**.
`30ef0031…` is therefore not merely *a* valid emission, it is *the* emission the driver at HEAD
produces. (My re-run artifact `…164610.json` was deleted; the tree is as gamora left it.)

---

## B — ⚑ RULING: does emitting a SECOND b1r artifact satisfy the D5 sibling-immutability law?

**YES. The law is SATISFIED, and this is the disposition I want used for the rest of the run.**
The conductor's reading is correct; I am adopting it as governing and stating the reasoning so it
is citable.

D5 exists so that **a digest, once emitted and cited, never stops naming the same bytes**. The
mischief it forbids is *rewriting history under a name someone has already relied on*. Measured
against that purpose:

1. **The old artifact is byte-identical to its recorded sha** (A6). Every citation of
   `6ac7c4e0…6b11` — including the one in § 1 of the original finding above — still resolves to
   the bytes it resolved to when it was written. **Nothing that was relied upon has moved.**
2. **The new file is the fix's own emission, not an edit of the old one.** A repair that changes
   what a run *emits* must emit; the alternative — mutating `…153359.json` in place to carry
   post-repair content — is precisely the D5 violation.
3. **The pre-repair artifact is now evidentiary in its own right.** It is the object that carried
   the BLOCK. Retaining it is what makes A8's diff re-runnable by a third party, and a law that
   forced its deletion would destroy the evidence for its own enforcement.

**One governing condition, which the build already satisfies:** where two siblings share a stem,
the record must say **which is of record and which is retained-as-evidence**. `AGENT_STATE.md` and
ADDENDUM 4 both do this explicitly and both carry the *"re-derive at HEAD, do not transcribe"*
rider from release condition (b). **Sibling multiplicity is legal; sibling ambiguity is not.**

---

## C — BLOCK-1: CLEARED

Gamora took the **first** of the two dispositions I offered — cite the constant rather than declare
the exclusion — which is the one I named as cleaner, and it is cleaner for the reason that matters:
it leaves the predicate **falsifiable**, where an ADDENDUM declaring the exclusion would have left
`B1r-P11` grading a surface with a permanent hole in it.

| Check | Method | Result |
|---|---|---|
| The `found.discard(...)` is **deleted** | `git diff` on the driver | **DELETED** — replaced by an 8-line ⚑ comment naming the conviction |
| **No** by-name exclusion remains **anywhere** in the driver | `grep -n "discard\|exclu\|RNG_SALT\|remove("` over the whole file | **NONE** — all 5 hits are prose *about* the deleted line |
| Salt cited in `constants_introduced` with provenance + Law-3 argument | executed `declared_constants()` | **CITED** — `['KIT_RESIDUAL_RNG_SALT']`, value `0x51d3b12a`, `type: int`, **1,833-char basis** |
| **⚑ Non-vacuity probe** — patch the citation away | monkeypatched `constants_introduced` → `[]`, re-graded | **`holds=False`, `uncited=['KIT_RESIDUAL_RNG_SALT']` — REPRODUCES EXACTLY** |
| The walk is genuinely **unnarrowed** | baseline `per_module` | **`module_level_numeric_constants: ['KIT_RESIDUAL_RNG_SALT']`** — the salt is now **found**, where the artifact previously reported `[]`. This is the load-bearing change. |
| Driver re-run | ran it | **`all_predicates_hold=True`, 13 predicates, wall 11.75 s** |

**The distinction that makes this a clearance rather than a re-BLOCK:** before the repair the
artifact reported `module_level_numeric_constants: []` — the salt was invisible to the *instrument*.
It now reports the salt as **found** and separately as **cited**. The predicate passes because the
constant is **on a governing surface**, not because it is skipped. That is the difference between
a green light and a green light that cannot turn red.

**On the basis itself.** I read all 1,833 characters and it does the thing I did not require but
would have valued: it names the hazard it could have waved away (*"a salt IS in principle
searchable against an outcome, and 'it is only a seed' is exactly the argument that would conceal
one"*) and then bounds it three ways — `B1r-P1b`'s byte-inertness, the survival-only reach into
`B1r-Q`, and **git revision count as a salt-search detector**. The third is a genuinely good idea
and I have not seen it used before. It is also honest about provenance in the one way that is
hardest to be honest about: *"a fixed hexadecimal NONCE I typed"* — no invented substrate lineage
for a value that has none.

### C2 — Prereg immutability: **INTACT** (the unprompted disclosure, checked as a claim)

Gamora volunteered that the artifact's `registered_form` published only the narrow "float" form
while the code implemented ADDENDUM 3's wider "float or int" form — the `WARN-1` shape, self-caught.
The question for me was whether the fix *rewrote* the registration to make itself pass.

**It did not.** `⚑ registered_form` in `predicates/B1r-P11` is **byte-identical** between the old
and new artifacts (string equality, verified). The restatement ships **beside** it as two **new**
keys (`⚑ restated_at_addendum_3`, `⚑ block_1_repair`); old keys `{holds, per_module,
⚑ registered_form}` → new `{… + 2}`. **No registered text was altered anywhere** — the math note
and ADDENDA 1–3 are untouched by both commits (`git diff --stat` on `math/` is **one file, 409
insertions, zero deletions**: ADDENDUM 4, additive-only).

This is the correct handling of a widened registration and it is the exact inverse of what
BLOCK-1 convicted: the wider form is **published on the artifact** and then **graded**, instead of
being implemented in code and left off every governing surface.

### C3 — The inverted test: **SOUND and DISCLOSED**

`test_every_scope_a_magnitude_is_READ_from_the_pinned_d6_csv` had
`assert declared_constants()["constants_introduced"] == []` — an assertion the repair necessarily
falsifies. It was **inverted, not deleted**, and I agree it is **strictly stronger**:

- The new form is **exact list equality** on names (`== ["KIT_RESIDUAL_RNG_SALT"]`), so it still
  convicts any model magnitude typed into engine source instead of being read from the pinned D-6
  CSV — the original assertion's entire purpose is preserved.
- It adds two assertions the old form did not have: the cited **value** must match the live
  constant, and the **basis must be a basis** (`"fitted"` and `"random.random"` must appear) — so
  the citation cannot silently decay into a bare name.
- It now also convicts **the citation going missing again**, which is the BLOCK-1 regression.
- A 9-line docstring states the inversion, its cause, and why it is stronger.

This is the second inversion this build has handled correctly (INFO-6 was the first). The pattern
is right: **assertions strengthened in a new direction, never removed to make a build green.**

---

## D — WARN-1: CLEARED

- `player_offense.py:146` `CritLimb` docstring — the false licence is **replaced by a pointer** to
  `F-B1r-1`, with the old figures **named rather than deleted**, exactly as `sustain_procs` did.
- **⚑ The bracket VALUE is untouched, which was the requirement.** At HEAD: `LO = "crit-lo-1.0"`,
  `HI = "crit-hi-1.5"`, `return 1.0 if self is CritLimb.LO else 1.5`. The `player_offense` diff is
  **entirely inside the docstring**. What was falsified was the justification; the bracket is
  conservative and stays, with the Lap-O re-grade routed to Wave-4 (`L-37` / `F-2`). Correct.
- `simulation/MIGRATION.md` § 5 amended **three → four**, with a ⚑ block that says *the heading
  originally said "THREE" and the enumeration was short by one* rather than quietly retyping the
  numeral. The repair-in-place justification (`__doc__`/`getdoc`/`inspect` absent from `kc2/`,
  scanned not assumed) is restated, and the `D-B1r-3` freeze is correctly held off `CRIT_BASIS` /
  `HIT_BASIS` — both still carry `149.2-182.2` at HEAD, **as they must**, with their falsity
  stated above them.

---

## E — WARN-3: CLEARED — and this is now the best-priced deferral in the run

I did not spot-check this. **I re-derived it.**

| Check | Result |
|---|---|
| `Σ w_r = 1.0` | **EXACT** |
| `ᾱ = Σ w_r α_r = 0.987` | **EXACT** (`0.98×0.65 + 0.35`) |
| `A_r ∈ [2714.40, 3968.64]` | **CONFIRMED** from `intake.ARMOUR_OPERAND_LAPY` |
| **Closed form ≡ branch form** | Ran `Δ(p,a) = −(1−r)Σ w_r α_r clamp(p−A_r,0,a)` against `intake.armour_branch` over `p ∈ {7.4, 500, 2714.4, 2800, 3000, 3500, 3968.64, 4100, 11764.51} × a ∈ {190, 296.4} × r ∈ {0.16, 0.20}` — **agreement < 1e-9 on every cell** |
| Asymptotes −157.5252 / −150.0240 / −245.7393 / −234.0374 | **EXACT to 6 dp**, all four, and equal to `−a·ᾱ·(1−r)` |
| Δ = 0 below every operand | **CONFIRMED** — `Δ(2714.40) = 0.0`, `Δ(2000) = 0.0` |
| 615 lines = 173 + 50 + 392 | **SUMS**; shares **28.1301 % / 8.1301 % / 63.7398 %** — matches 28.13 / 8.13 / 63.74 |
| mean `−99.0938 / 2172.5701 = −4.5611 %` | **EXACT** |
| mean `−154.0984 / 2172.5701 = −7.0929 %` | **EXACT** |
| duty-cycled `0.2667 → −26.4250`; `0.4545 → −45.0426` | **EXACT** against `4/15` and `5/11` — the note used the **exact** rationals, not the printed 4-dp roundings |

I also checked the algebra by hand and it is right for the reason stated: below the branch `A_r` is
**absent from the expression**, so the refused addend changes nothing at all — not "a little". The
`clamp` form is the correct unification of the three regimes.

**Three things raise this above compliance.** (1) Both arms are run and **neither is designated** —
the composition question (`×1.56` or not) is left to the intake seam rather than decided inside a
stacking lap to produce a tidier number, which is the whole point of `C-B1r-1`. (2) The **three
limits are named before anyone had to find them** — first-order on the fold-absent trajectory,
duty-cycling assumes buff-independent hit arrival, salts 2/3/4 horizon-limited. (3) **The
instrument ships**, explicitly applying `WARN-2` / `D-B1r-4`'s lesson *prospectively*. Every figure
above is reproducible from the published block, which is why I could re-derive rather than trust.

`defensiveProtection +190` remains `DECLARED-NOT-FOLDED`; the price is reported and **graded by
nothing**. That is the correct shape for a deferral.

---

## F — WARN-2: CORRECTLY UNREPAIRED. INFO-2: DISCHARGED.

- **No WARN-2 surface was touched.** The math note and ADDENDA 1–3 have **zero** deletions
  (`math/` diff = ADDENDUM 4 only, additive). `MIGRATION.md`'s diff touches **§ 5 only** — § 2(b)'s
  census is untouched. The § 0 / H-5 figures and ADDENDUM 2's 70-vs-73 count stand as they were.
- The build **declares** this rather than leaving it to be noticed: ADDENDUM 4 § "WHAT ADDENDUM 4
  DOES NOT DO" states it is *"not repaired, not reconciled, and **not claimed to be**"*, and routes
  it into `B1r-Q` on survival coupling. That is the disposition I named as defensible in the
  original finding; what was missing was **one published sentence**, and it is now published.
  **WARN-2 remains open inside the quarantine** and is inherited by whichever build is first
  commissioned to speak about survival — per § 7(c), B-2app must reconcile it if it re-uses the P-A
  population.
- **INFO-2 discharged** — the smoke selector is published: `pytest tests/ -q -k kc2`. I ran exactly
  that at HEAD: **410 passed / 1 failed**, and the 1 is `test_AC_10_10`
  (`secondary_streams.py:136`), **the same pre-existing failure I verified at parent `1888b218`**.
  The earlier unreproducible "525" is retired.
- **INFO-1** — the falsifier-failure tally basis is not separately restated. Immaterial: every
  failure remains published above its repair, and BLOCK-1's own failure is now on the record in
  `AGENT_STATE.md` as *"the build shipped claiming 13/13; it was 12/13 as registered."* Not carried
  forward.

---

## G — VERDICT

**⚑ BLOCK-1 IS CLEARED.** `B1r-P11` holds in its **registered form**, on the **unnarrowed** walk,
with **no by-name exclusion anywhere in the instrument**, and a non-vacuity probe I ran myself
turns it **red** when the citation is removed. **13/13 as registered.**

**(a) B-1r SEALS on artifact sha**
`30ef0031d7b9e048f3bbe7fedfb83afca53b834f6d813829c052fd75a7f98e8a`
(`src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b1r-20260824_163444.json`),
**of record**; `6ac7c4e0…6b11` (`…-20260824_153359.json`) is **retained as pre-repair evidence,
byte-unchanged, and is NOT of record**. Per § B the D5 sibling-immutability law is **satisfied**.
⚑ **This sha is a measurement, not a licence to transcribe** — release condition (b) stands: any
downstream build re-derives it at HEAD.

**(b) The B-2app hold is RELEASED — UNCONDITIONALLY.** Conditions (a) and (b) of the original § 7
are **discharged** ((a) by this clearance; (b) is restated in `AGENT_STATE.md` and ADDENDUM 4 and
becomes a standing rider rather than a hold). **Condition (c) survives as an obligation on B-2app,
not as a hold on B-1r**: if B-2app re-uses the P-A population it must reconcile WARN-2's census in
its own note.

**Residual, carried and named:**
1. **WARN-2** — open, inside `B1r-Q`, correctly declared. Owed by the first build licensed to speak
   about survival.
2. **`CritLimb` bracket re-grade** on the Lap-O basis — Wave-4, `L-37` / `F-2`.
3. **`C-B1r-1` / `C-B1r-2`** routed to the intake cluster; **`C-B1r-3`** to star-lord per ADR-004.
   I renew my request that `C-B1r-3` be prioritised over the cosmetic repairs it defers — *a
   provenance string inside a digested surface is a latent baseline-breaker*, and this build hit it
   once already (`D-B1r-3`).
4. Engine-wide suite debt (59 failed / 21 errors at HEAD) is **pre-existing and outside B-1r's
   eight-file blast radius** — recorded again so it is not mistaken for a regression at the next
   milestone tag.

**Escalation to Matt: NONE.** ADR-002 — within-seam repair, no API change, no cross-seam schema
move, no locked decisions-log conflict. Cleared under my own authority, as § 8 committed.

---

## H — For the record

I wrote in § 9 that *"fix that and this build is the reference standard for the rest of the run."*
**It is.** The repair took the harder of the two paths I offered, and took it for the right reason.
It could have shipped an ADDENDUM declaring the exclusion — I said that would discharge L-33, and
it would have. Instead the constant went onto a governing surface where **a reader who disagrees
with the distinction can now see it and argue with it**, which is what `constants_introduced` is
for. The build then went **past** the finding: it disclosed a `registered_form`/code mismatch I had
not caught, published the wider form beside the registration instead of over it, inverted rather
than deleted the test the repair falsified, and completed `WARN-3`'s price with the instrument
attached so that I could re-derive every figure instead of accepting it.

One line is worth preserving as the run's standing lesson, and it is gamora's own:

> *12/13 BECOMES 13/13 BY CITING THE CONSTANT, NOT BY SKIPPING IT.*

**Two clearances now rest on measurements a third party can re-run**: A10 (independent re-run,
byte-equal but for two timestamps) and E (closed form re-derived against the live branch function).
Neither was requested. Both are why this cleared in one pass.

---

## References — re-submission

**Engine (`~/Games/reincarnated-engine/`) — not pushed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b1r-residual-and-dot-stacking-ADDENDUM-4-2026-08-24.md` (`15ab9a08`, zero code)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_mc_b1r_residual_2026_08_24.py` (**BLOCK-1 repair** — `found.discard` deleted, `_b1r_p11_ast`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_kit_residual.py` (**BLOCK-1 repair** — `declared_constants()`, salt cited)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/player_offense.py` (**WARN-1 repair** — `CritLimb` docstring; bracket untouched)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/intake.py` (read-only — WARN-3 re-derivation source)
- `/Users/admin/Games/reincarnated-engine/tests/test_kc2_mc_b1r_residual_and_dot_stacking.py` (the disclosed inversion)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (`F-B1r-1` three → four)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`

**Artifacts:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b1r-20260824_163444.json` — **OF RECORD**, `30ef0031…8e8a`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b1r-20260824_153359.json` — pre-repair evidence, `6ac7c4e0…6b11`, byte-unchanged
