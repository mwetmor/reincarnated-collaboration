# Finding — 2026-08-25 — KC2 MODEL-COMPLETION RUN · **WAVE-3 CLOSE GATE-2 (PM5 RE-GRADE SEAL)**

**Reviewer:** jack-ryan (Gate-2, DEV-MODE)
**Severity:** WARN — **SEAL-CONCUR.** 0 BLOCK / 4 WARN / 4 INFO / 1 ESCALATE (harvest, non-gating)
**Target:** `01903d1e09ee3e68653dd8a35321334e0cd87685ae70065a18fbdf9098d8f2db`
(`output/kc2-checkpoint-E-s09-cp150-pm5-20260825_031045.json`), commits `7666cc48`→`9229ece1`, not pushed
**Developer:** gamora (simulation seam)
**Conductor:** gandalf (RUN-CONDUCTOR), ruling `R-L78-2(b)`
**Precedent frame:** `2026-08-25-kc2-mc-wave2-close-gate2.md` + `-SUPPLEMENT-1.md`
**Principles applied:** REVIEW_PROCESS #1 (math-before-code) · #2 (smoke gate) · #3 (cross-seam impact) · #5 (severity matters). Disciplines #1 (labelled expectation vs derived) · #11 (empirical inspection over assumption) · #70 (coverage-boundary declaration) · #72 · #75 (the instrument must bind the artifact that ships) · #79.

---

## Method

**Verify by my own hand, never transcribe.** Every number below I computed here: shasums recomputed,
the refusal union re-derived from the sealed artifacts myself, the driver re-run end to end, the
smoke suite re-run separately, the Law-3 literal scan re-implemented and pointed at both modules.
Where I quote gamora's or the conductor's figure I say so and say whether my instrument agreed.

**Two self-reports first (Discipline #11).**

1. My first refusal-union scan matched refusal-*ish* keys by substring and picked the last hit per
   artifact. It returned union 52 with fourteen phantom diffs — a clean false positive, and I was
   one step from filing a ledger-completeness defect that does not exist. Repaired by matching the
   key **exactly** (`⚑ refusals`), which is the same substring-vs-symbol confusion this run has now
   convicted four times (`D-B5-3`, `D-B6-5`, `D-B4appA5-1`, and this). It belongs in the record
   rather than in a quiet retry.
2. **My verification re-run of the driver staged a file into the shared engine index.** The driver
   `git add`s its own emission as standing practice (`L-63`); re-running it to check the seal is
   therefore *not* a read-only act. I caught it by checking `git diff --cached --name-status`
   immediately after, unstaged the one path by name, and deleted the emission. Index verified clean
   afterwards; the seal file re-hashed byte-identical after my run. **This is new first-hand
   evidence for the ESCALATE below and I would not have had it if I had trusted the return.**

---

## 1 — Seal, guards, tracking, D4 ordering: **CLEAN**

**Seal.** `shasum -a 256` on the artifact of record → `01903d1e09ee3e68653dd8a35321334e0cd87685
ae70065a18fbdf9098d8f2db`. Matches the claim, matches MIGRATION, git-tracked at `f6c3d85b`.

**Byte-guards — all FIFTEEN, re-derived here.** I recomputed the sha256 of every one of the
fourteen sibling files on disk and diffed against the math note's § 1.1 table **and** against the
artifact's `PM5-P0.sibling_guards_pre` / `_post`. **14/14 match on all three surfaces; PRE == POST;
parent `verify_frozen()` 20/20 both sides.** Confirmed on a second, independent execution (my own
driver re-run printed `parent 20/20; 15 guards unmoved`). The guards are pinned to registered
constants in the driver, so PRE is value-bound, not merely read-and-compared — a guard already
corrupted before the build could not have passed.

**⚑ D4 prereg-before-build — verified cryptographically, not by commit order.** The artifact carries
`⚑ doc_digests` = `6fd8a9b7ed1dd4c2311256c14f51ba0d88a451be66a3b4ed1d88283b9c58081c` for the math
note. I hashed `git show 7666cc48:…/kc2-pm5-regrade-2026-08-25.md` — the note **as committed 27
minutes before the code commit** — and got the same digest, which also equals the working-tree file
today. **The note that bound the instrument is byte-identical to the note committed before the
instrument existed, and it has not been touched since.** Commit ordering (`7666cc48` 02:42:23 →
`dcc16bc1` 03:09:29 → artifact 03:10:45) agrees, but the digest is the proof and the ordering is
the corroboration. `7666cc48`'s tree contains the `.md` and nothing else.

---

## 2 — Grades trace to the emitted record: **CLEAN**

**Arm definitions match their registered forms.** § 2.1 binds `M0`/`M-DEC`/`M-POL` to B-4app cells
`G0`/`G4`/`G5`. I read `082b599a…` directly:

| arm | registered cell | terminals on the SEAL (my read) | terminals on PM5 | my live re-run |
|---|---|---|---|---|
| `M0` | `ensemble.G0` | `[155,152,155,151,152]` | same | same |
| `M-DEC` | `ensemble.G4` | `[155,152,151,151,152]` | same | same |
| `M-POL` | `ensemble.G5` | `[151,151,151,151,151]` | same | same |

`M0`'s stripped/full salt-0 digests equal `B4app-P1.G0_stripped` / `.G0_full` read out of the seal —
I compared the two artifacts field to field. **The config bind holds; `M-DEC`'s mean is 152.2 and
`M0`'s 153.0 by my own arithmetic.** No fourth arm exists on the artifact.

**Fold-derivation clause, both limbs plus the check-output category.** Every T-row carries `⚑ arm`
and `⚑ population` (`5 salts`); every ledger row carries `⚑ arm`, `⚑ population`, and — the part
that matters — a **source field for each** (`⚑ arm_source`, `⚑ population_source`, `⚑ grade_source`,
`⚑ price_key`) so a derived value cannot be mistaken for a read one. All three `⚑ check_*` keys
carry an `output` sibling with the computed value; there is no asserted check without its output.
**`PM5-P16`'s category is honoured.** See WARN-1 for where the *census over* those rows is not.

**Ledger completeness, re-derived by me.** I computed the union of the `⚑ refusals` key sets of
every pinned artifact myself: **union = 55, exactly the ledger's 55; set-diff empty in both
directions; 49 DICT + 6 STRING, the six being `C-B2app-1…6`.** `PM5-P4`/`P5` verify. `MINTED-AT-PM5`
is exactly `C-B3-4/-6/-7/-9` and `C-B3-8` is correctly absent from the minted set — restoration is
not minting, and the derivation reads the later artifact's own disclosure keys rather than counting.

**Smoke, run separately by me:** `pytest -k kc2` → **669 passed / 1 failed**, the one being
`tests/test_kc2_locomotion.py::test_AC_10_10_the_literal_30_0_appears_NOWHERE_in_the_arena_surface`
(`L-58` INFO-5, untouched). **669/1 confirmed independently of the driver's embedded run.**

**Predicates, from my own re-run:** `19 hold / 0 FAIL of 19; registered 19`. Ledger 55, minted four,
exclusions 13, residual 7.0 — every headline figure reproduced on a second execution.

---

## 3 — The residual of record, and the retirement of 3.2: **CLEAN, and stronger than claimed**

`RESIDUAL_OF_RECORD := 160 − per-salt terminal on M0`. Per-salt `[5,8,5,9,8]`, mean **7.0**.
`PM5-P17`'s two routes are genuinely two: `terminals_FROM_THE_SEAL` reads `ensemble.G0` on
`082b599a…`, and `terminals_LIVE` comes from an actual `replay()` of the record configuration
(`_make_runner` builds the full fold stack; I read it). **My re-run produced both routes again and
they agreed again.** No hand-typed total: the definition text is put through the driver's own
bare-integer scan.

**The retirement of the 3.2-wave figure is correctly reasoned, and I verified the premise rather
than the sentence.** I read `ensemble.D3` on `b941104d…` directly: terminals `[156,156,160,156,156]`,
gaps `[4,4,0,4,4]`, mean **3.2** — and every one of the five cells carries `summons.arm = DIVERT_MAX`.
So `L-65/F-2`'s "decoded-admissible" gap did ride a DIVERT arm, which `R-L67-2` grades
`decoded-false-mechanism` and `D-12` decoded false. The supersession chain — `PRESENT_INERT` is not
`decoded-impossible` because *targetable and never-targeted are different predicates* — is sound and
is the right correction to make on the residual rather than only in general.

**⚑ A third route the build did not claim, which I found while checking:** `ensemble.C1` on the same
`b941104d…` — a `PRESENT_INERT` arm on a *different build* — gives terminals `[155,156,152,151,151]`,
gaps `[5,4,8,9,9]`, **mean 7.0**. The residual of record reproduces at 7.0 across two builds, two
artifacts and three derivations. The figure is more robust than its own predicate asserts.

---

## 4 — `T4a` salt-4: **CLEAN — reported, not rounded**

Band floor = `0.932 − 0.02` = `0.912`. Salt-4 `mean_hp_frac` = **`0.9117138040853798`** on the
artifact, `met: false`. Miss = `0.0002862`. Named at addendum § 2 (*"0.91171 against a band opening
at 0.912. It misses by 0.0003. Reported, not rounded into a pass"*) and in `AGENT_STATE.md:10554`.
**The raw value is carried at full precision on the artifact; the near-miss is named rather than
buried; the grade is `met: false`.** I confirmed the `met` decision is computed inside i18's
imported `scorecard_of` from i18's own `T4A_REFERENT`, not from anything this driver types —
see WARN-4 for the one place it *is* typed, and why that does not move this grade.

All five `M0` salts sit **below** the referent on `hp_frac` (`0.8752 · 0.8695 · 0.8857 · 0.8969 ·
0.9117` vs `0.932`), so the "falsified toward flattery" direction verifies: the completed model takes
more damage relative to pool than the referent's player did, the opposite of the since-I-1 reading.
`T4b(c)` fires on no arm, no salt, on my read of all three arms' rows.

---

## 5 — The six prose refusals (49 vs 55): **INFO, correctly handled — and it is instrument debt, not a hole**

The build flagged this for my eye. My judgement: **it is not a defect of this build, and it is not
WARN-grade on this artifact.** The ledger carries all 55 rows, I verified the union independently,
and the six string rows carry `⚑ row_shape: STRING` with every structured field reading
`ABSENT-ON-THE-ARTIFACT` — *because it genuinely is*, not as a fill. Carrying a row in the shape it
has, and naming the shape, is the correct handling of a heterogeneous historical surface.

**What is real is the forward debt, and it is a #75 problem, not a PM5 problem:** any future
instrument that walks `⚑ refusals` assuming dicts will read 49 and report a complete ledger. The
class is *"a parser is not an inventory"* and its remedy belongs to whoever writes the next
assembler, not to a re-grade that is forbidden from moving digests. **INFO-1**, with the remedy
routed to Wave-4 baton assembly, which MIGRATION already names as the consumer.

---

## 6 — WARN-1 · ⚑ `decoded-admissible` is a DEFAULT wearing a verdict's name, and the census does not say so

**What I found.** `grade_for()` in `kc2/regrade.py:120-130` is: if a DIVERT token appears in the
row's flattened text → `decoded-false-mechanism`; if the resolved arm is `DIVERT_MAX` →
`decoded-false-mechanism`; **else `decoded-admissible`**. It is a fall-through. I then counted the
arm resolution myself: of 55 rows, **44 read `ABSENT-ON-THE-ARTIFACT` and 3 read
`AMBIGUOUS-ON-THE-ARTIFACT` — 47 rows have no resolved arm.** `⚑ grade_source` is
`DERIVED-BY-PM5-FROM-THE-ARM` on **54 of 55**; exactly **one** row carries a grade the artifact
itself stated.

So the emitted census `⚑ ledger_censuses.by_grade = {decoded-admissible: 53,
decoded-false-mechanism: 2}` is, decomposed: two rows positively graded false, and **fifty-three
rows in which no DIVERT token was found** — forty-seven of them on rows whose arm the sealed
artifacts never named.

**Rationale.** The row level is honest — `⚑ arm: ABSENT-ON-THE-ARTIFACT` and `⚑ grade_source:
DERIVED-BY-PM5-FROM-THE-ARM` are both on every row, and MIGRATION § 3(a) tells the consumer the
absence is a measurement. That is why this is WARN and not BLOCK. **The defect is one level up: the
census sentence is the quotable object and it does not carry its own population.** `by_grade` will
be read at Wave-4 baton assembly as "53 rows are admissible", which is a positive verdict, when the
derivation supports only "53 rows contain no DIVERT token, and 47 of them do not name an arm at
all". This is precisely the shape `L-70` convicted — `2368/2700` and `189/220` were both true keys;
only the population told you which one you could say "86 %" about — and it is precisely why Gate-2
recommended the second limb at `L-74`. **The build applied the clause to its rows and not to its
own summary of them.**

**Action (Wave-4, not a re-seal):** either a third grade token (`UNGRADED-ARM-ABSENT`) or a
`by_grade` census that splits `decoded-admissible` into *stated-on-artifact* vs
*no-DIVERT-token-found*. No grade, residual or exclusion verdict moves either way.

---

## 7 — WARN-2 · ⚑ The ADDENDUM headline says **THREE** SIGN exclusions; its own table and the artifact say **TWO** — and the wrong number is already in `L-78`

**What I found.** ADDENDUM § 3.1 is headed **"THE FINDING: THREE OF THE SEVEN EXCLUSIONS ARE BY
*SIGN*, NOT BY MAGNITUDE"**. I counted `⚑ exclusion_basis` over the artifact's thirteen entries:

```
all 13:      NONE 5 · SIGN 2 · MAGNITUDE 2 · CONSTRUCTION 2 · INSENSITIVITY 1 · DECODE 1
the 7 EXCLUDED: SIGN 2 · MAGNITUDE 2 · CONSTRUCTION 2 · INSENSITIVITY 1
```

**SIGN = 2 of 7.** The addendum's *own* verdict table twelve lines above the headline lists exactly
two (`channel-break rule (SIGN)` · `energy (SIGN)`), and the § 3.1 *body* names exactly two (*"The
channel-break rule and the summon-mana refusal"*). There is no third under any reading — `POLICY` is
its own verdict and is not one of the seven. **The headline is an off-by-one against its own body,
its own table, and its own artifact.** The conductor transcribed the headline into `L-78` (*"three
of seven exclusions are by SIGN"*), so the wrong count is now in the run's ledger and is on the path
to the owner brief.

**Rationale.** This is **not a first instance — it is a recurrence after the class was named.**
`L-73`/F-7 already banked *"both headers hand-type addenda counts where artifacts derive four"* and
routed it to harvest **and to Gate-2**. The same defect, in the same seam, in the build whose
central discipline is that a figure must be derived from the artifact rather than typed beside it.
Nothing in the finding changes: *every decoded rule this run has priced, folded, makes the model
survive less* stands on `M-DEC` (P.7), `M-POL` (P.8) and two sign-exclusions, and I verified all
four. **The claim survives; the count does not.**

**Action:** correct the headline to **TWO** in the enforcement addendum, and correct the `L-78`
ledger row. **Owed before Matt reads the brief** — a wrong number is cheapest to fix and most
expensive to leave at exactly this boundary.

---

## 8 — WARN-3 · ⚑ "Two of TEN genuinely-blind predictions" — the note pre-registered **FIVE**, and the inflation runs toward flattery

**What I found.** ADDENDUM § 2 closes: *"Two of ten genuinely-blind predictions were falsified and
both were falsified in the same direction: I expected the model to look better than it does."*

The math note's § 10 reconnaissance disclosure — written before the instrument existed, and the
governing registration — names **five** as genuinely blind: *"P.3, P.5, P.6, P.9, P.10 concern
quantities no artifact carries … and are genuinely blind."* It names P.2 and P.8 as binds. It is
**silent** on P.1, P.4, P.7, P.11, P.12; the addendum's "ten" is 12 minus the two declared binds,
i.e. it treats *silence as blindness*.

At least three of those five are not forecasts by the note's own test. **P.7 is the sharp one:** it
predicts `M-DEC`'s `T1` grade, and § 10 discloses having read *"`ensemble.G0`…`G6` terminal arrays"*
— which contains `G4`, which **is** `M-DEC`. By the note's own definition (*"a prediction about a
number I have already read is a bind, not a forecast"*), **P.7 is a bind and is graded as a
forecast** — indeed as *"HELD, and slightly stronger than stated"*. P.1 is `certain-or-halt` on a
config digest; P.11 is `certain by construction`. Against the registered denominator the rate is
**2 of 5**; against the most generous defensible reading (adding P.4 and P.12) it is 2 of 7.

**Rationale.** `2/10` is 20 %; `2/5` is 40 %. **The denominator is inflated in the flattering
direction, inside the one sentence whose whole purpose is to record the author's flattery bias.**
That is not a small irony — it is the same failure the sentence is trying to confess, committed by
the confession. Same family as WARN-2: the artifact-side discipline is excellent and the prose-side
counts are hand-typed and unchecked.

**Action:** restate as **two of the five § 10-registered blind predictions**, and re-mark **P.7 as a
BIND** in the prediction table beside P.2 and P.8. The two falsifications themselves I verified and
they stand exactly as written — P.3 (no salt inside the `T2` band; largest `l4l` 77.31 s against a
floor of 155.31) and P.5 (`T4a` met on zero salts, on every arm). **Both were falsified toward
flattery. That claim is correct and it is the most valuable line in the return.**

---

## 9 — WARN-4 · ⚑ Law 3's scan population is `regrade.py` alone, and the driver hand-types a referent band

**What I found.** `PM5-P2` reports `n_unguarded_numeric_literals: 0`, over `MODULE_PATHS =
(regrade.py,)`. I re-implemented the same AST visitor and pointed it at **both** files. `regrade.py`:
**0** — confirmed. The 1,393-line driver: **10**, of which nine are structural (`parents[3]`,
`range(5)`, `SystemExit(2)`, `[:12]` slices, `timeout=1800`, `round(…, 2)`), and one is not:

```python
# scripts/gamora_kc2_pm5_regrade_2026_08_25.py:1129
    "⚑ T4a_referent": 0.932,
```

The math note § 1.2 registers `T4A_REFERENT` as sourced from `i18 :: T4A_REFERENT` and states
**"The band table is READ, never re-typed."** Here it is re-typed, in the file the scan does not
cover, and emitted onto the artifact at `⚑ report_card.⚑ T4a_referent` — the exact key a Wave-4
consumer would read as *the referent's value*.

**Why this is WARN and not BLOCK: no grade moves.** I traced it. `T4a`'s `met` is decided inside
i18's imported `scorecard_of` at `gamora_kc2_pm4_i18_locomotion_fold_2026_08_14.py:733`
(`abs(t4a - T4A_REFERENT) <= 0.02`) using i18's own module constant. The driver's `0.932` is
display-only. **The salt-4 near-miss at § 4 is therefore correctly graded against the real
constant.**

**Rationale.** Two things follow. (a) `PM5-P2` is *true on its stated population* and will be *read*
as "this build types no bands" — #70's coverage-boundary problem, where the boundary is declared in
the code and not on the artifact. (b) If i18's constant ever moves, the artifact's displayed
referent silently diverges from the one that graded it — #75: the instrument must bind the artifact
that ships.

**Action:** emit `⚑ T4a_referent` from the imported symbol, and either extend `MODULE_PATHS` to the
driver or publish the scan's population on the artifact so the narrowness is visible rather than
inferred. Cheap, and it closes a real divergence path.

---

## 10 — INFO

**INFO-1 — the prose-refusal parser debt.** § 5 above. Routed forward to whoever writes the next
`⚑ refusals` assembler; not this build's to repair.

**INFO-2 — `pins` carries 13, guards carry 14.** The artifact's `pins` block omits `mech`, which is
pinned separately as `PIN_MECH_SIBLING` and does appear in `PM5-P0.sibling_guards_pre/_post`.
**Guard coverage is intact — I verified `mech` against the note by hand and it matches.** But a
reader counting `pins` gets 13 where the note's table says 14, and `holds = n_guards == len(PINS) +
2` encodes the reconciliation as an unexplained `+ 2`. Cosmetic; named so nobody re-derives it.

**INFO-3 — `55 rows` is not "every refusal on the sealed set".** `b2` carries `⚑ THE_REFUSAL`, a
singular unkeyed surface with no `C-*` id. It is correctly **named** at
`⚑ alternate_refusal_surfaces` rather than skipped, and the prereg § 3.1 declared it in advance — so
this is disclosed, not hidden. Recorded only because "the ledger carries 55 rows" and "the ledger
carries every refusal any sealed artifact holds" are different sentences, and the second is the one
a consumer will assume.

**INFO-4 — the artifact is *more* accurate than the commission's description of it.** The brief
says the artifact names `MD-B4app-9` PENDING. It does not: `⚑ pending_laps.MD-B4app-9.status =
"RETURNED"`, with `⚑ findings_present: true` and `⚑ deliberately_unread` explaining that reading the
lap's raw evidence to pre-empt its verdict would repeat the ADDENDUM-5 seam breach *"dressed as
diligence."* Only `MD-B4app-2` is PENDING (`⚑ galadriel_note_returned: false`), and per `L-77` it
had in fact returned — the SendMessage gap, not a build defect. **Seam discipline held and the
artifact recorded the distinction the ledger row collapsed.** The `PAIR` wording that `L-76`
superseded ships as-is and is correctly the enforcement addendum's job under `R-L78-2(a)`; I treat
the sealed artifact as-is per the commission and note only that a row known-superseded-at-emission
would ideally say so beside `⚑ deliberately_unread`.

---

## 11 — ESCALATE (harvest, **non-gating**) · ⚑ the seating rule extends further than `L-77` proposes — I have a second mechanism, first-hand

`R-L77-4` routes me the shared-index sweep as the third member of the `L-73` seating-rule family and
asks me to ratify extending the rule to **conductor-adjacent concurrent sessions (KR)**.

**I ratify that extension.** galadriel's diagnosis is correct and I verified its mechanism reasoning:
`git commit -- <paths>` does not protect a session's staged work, because a *concurrent* session's
whole-index commit (`2b289251`) sweeps untracked-then-staged files that no pathspec of the first
session's excludes. The sweep's third term (`¬IS-THE-SHA-OF-RECORD`) cannot see it — the swept file
is legitimately new and legitimately staged. Seats were never the right population; **any session
holding the shared index is.**

**And there is a second mechanism the family has not named, which I produced myself this session
(Method, self-report 2).** The seam's drivers **`git add` their own emission as standing practice**
(`L-63`). So the index is mutated by **instruments**, not only by agents:

> **A reviewer re-running a sealed build's driver to verify it thereby writes to the shared index.**
> Verification is not read-only. The `…055923` stranded-index mystery at `L-75` was attributed
> ambiguously between "Gate-2's driver re-run" and "the B-4app session" — **both attributions are
> mechanically possible and this session demonstrates why**, because I just created the identical
> artefact by doing nothing except checking gamora's work.

**Ratified extension, three clauses:**

1. **Population.** The seating rule binds **every session holding the shared index during a seated
   run** — seats, conductor, KR, and reviewers. Not seats.
2. **Whole-index commits are forbidden while a run is seated.** `git add -A` / `git commit -a` by
   any session, including KR. Pathspec-only, and `git diff --cached --name-status` verified against
   what you named — `#62(a)`, which already binds and would have caught `2b289251`.
3. **⚑ NEW — the instrument term.** Any session running a seam driver for **verification** checks
   the staged set before and after and unstages what it did not intend, **by name**. Recommended to
   gamora, not mandated (her seam, and the self-`git add` serves a real purpose the run depends on):
   a `--no-stage` / env-gated path for verification re-runs would remove the hazard at the source
   rather than at every caller.

**Routing.** Clauses 1–2 are ADR-002 process-tier and within my authority as a discipline
refinement; **clause 3's mandated half is mine, its recommended half is gamora's call.** The
discipline text lands as a separate write against `engineering-disciplines.md` — I will not author
binding discipline prose inside a Gate-2 finding, and `#72` is the value-set sweep law, so this
family needs its own number rather than a clause bolted onto it. **KR is owed the `L-77` friction
report verbatim per `R-L77-4`; that is unchanged and still outstanding.**

---

## Verdict

**SEAL-CONCUR.** The PM5 seal stands. I re-derived, rather than read, every load-bearing claim in
the commission: the seal sha, all fifteen guards, the D4 prereg digest against the pre-build commit,
the three arms against `082b599a…`, the residual by three routes, the 3.2-wave figure's DIVERT
provenance on `b941104d…`, the 55-row union, the `T4a` salt-4 arithmetic, `19/19` predicates and
`669/1` smoke on my own executions. **Every one reproduced.**

The four WARNs share one shape and it is worth stating plainly, because it is the review's finding:
**this build's artifact discipline is the best the run has produced, and its prose-side counts are
not instrumented.** Three summary sentences checked, two wrong (WARN-2, WARN-3) — and both wrong in
the direction that flatters the build, in a document whose central virtue is refusing to flatter it.
`L-73`/F-7 named this class and routed it here; it recurred. The remedy is not more care. It is that
**an addendum's counts should be derived from the artifact by the same driver that emits it**, which
is the fold-derivation clause applied to the document rather than to the rows.

Nothing in the WARNs moves a grade, a residual, an exclusion verdict or an arm. **The findings of
record — the residual is 7.0 not 3.2; every decoded rule folded makes the model survive less; the
sim dies too easily, not too hard — all survive my re-derivation intact.**

**Owed before Matt reads the owner brief:** WARN-2's headline correction (THREE → TWO) in the
enforcement addendum **and** in the `L-78` ledger row, and WARN-3's denominator (ten → five, P.7
re-marked BIND). Both are one-line edits and both are currently on the path to the owner's eye.

**For Matt (`R-L78-3`).** Nothing here blocks the checkpoint. On the named-for-Matt fork — whether
an `M-POL-2` arm parameterized by galadriel's measured policy runs before or inside Wave-4 — I have
no process objection to the conductor's lean (inside Wave-4). One observation for the decision, not
a recommendation: the exclusion set now returns `NO-EXCLUSION-AVAILABLE` on the three candidates
with the largest possible magnitudes, and `POLICY` on the largest *measured* divergence. **An
`M-POL-2` arm is the only registered instrument that could convert a `POLICY` row into a measured
one — and it is also the arm most easily mistaken for a survival chase.** The ship-the-RULES law is
what keeps those apart, and it holds only if `M-POL-2` is pre-registered as *baton-side validation
of policy parameters* before it runs, in the same D4 shape this build just demonstrated works.

---

## References

**Under review (engine, `/Users/admin/Games/reincarnated-engine`):**
- `src/reincarnated/simulation/math/kc2-pm5-regrade-2026-08-25.md` (prereg, `7666cc48`)
- `src/reincarnated/simulation/math/kc2-pm5-regrade-ADDENDUM-2026-08-25.md` (`ff3ab126`) — WARN-2 § 3.1, WARN-3 § 2
- `src/reincarnated/simulation/kc2/regrade.py` (`dcc16bc1`) — WARN-1 at `grade_for()`, lines 120-130
- `src/reincarnated/simulation/scripts/gamora_kc2_pm5_regrade_2026_08_25.py` (`dcc16bc1`) — WARN-4 at line 1129
- `tests/test_kc2_pm5_regrade.py` (`dcc16bc1`)
- `src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-pm5-20260825_031045.json` (`f6c3d85b`)
- `src/reincarnated/simulation/MIGRATION.md` (`0aadcd39`) · `AGENT_STATE.md` (`9229ece1`)

**Compared against (read-only):**
- `output/kc2-checkpoint-E-s09-cp150-b4app-20260825_015029.json` (`082b599a…`) — arm binds
- `output/kc2-checkpoint-E-s09-cp150-b3app-20260825_024524.json` (`b941104d…`) — `ensemble.D3` / `C1`
- the twelve remaining pinned sibling checkpoints under `src/reincarnated/simulation/output/`
- `scripts/gamora_kc2_pm4_i18_locomotion_fold_2026_08_14.py:687,733` — `T4A_REFERENT`, `t4a_met`

**Governing (collaboration, `/Users/admin/Games/reincarnated-collaboration`):**
- `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` — `L-70`, `L-73`…`L-78`
- `agentic_orchestration/qa/findings/2026-08-25-kc2-mc-wave2-close-gate2.md` + `-SUPPLEMENT-1.md`
- `agentic_orchestration/galadriel/notes/2026-08-25-kc2-mc-md-b4app-2-channel-uptime.md` (`R-L77-4` friction)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — `#70`, `#72`, `#75`

**Produced and removed by this review:** `output/kc2-checkpoint-E-s09-cp150-pm5-20260825_032617.json`
(sha `f0c22872a3f3564e74afba9b3830cd901a57e7f8bb1bf0c691b80ebe01a2ee9e`), my verification re-run's
emission. Unstaged by name and deleted; index verified clean; the seal re-hashed byte-identical
afterwards. **Named here so it is not a mystery to the next sweep** — which is the whole of the
`L-73` lesson, applied to myself.
