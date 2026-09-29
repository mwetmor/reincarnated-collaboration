# Finding — 2026-09-29 — Run JOIN-1 charter v0.1 DRAFT (Gate-1, pre-launch)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Verdict:** **BLOCK — narrow, but the central invariant is one of them.** 7 BLOCK · 10 WARN · 7 INFO.
**Target:** `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md`, v0.1 DRAFT, 93 lines
**File sha256 (derived before reading, per the brief's HALT condition):** `b8c2cb9250b115f3fa0dc4f57306fc087ba85afb0f430ea7edda45f2af645ad5` — **matches `b8c2cb92…`. Hash gate PASSED; no HALT.**
**Author under review:** gandalf (`ARCHITECT` → prospective `RUN-CONDUCTOR`)
**Governing course:** `2026-09-28-join-key-architect-pass.md` § 8 (Q85–Q89 + E-1; KP-83)
**Principles applied:** 1 (math-before-code) · 2 (smoke-gate) · 3 (cross-seam impact) · 4 (committed record as truth) · 5 (severity matters)
**Pattern / disciplines cited:** desirable-run-pattern § 1, § 3 (F1–F4), § 4 (halt taxonomy), § 5.1–5.4, § 6.1 (coverage-before-accuracy), § 6.2 (owner-eye checkpoints), § 6.3 (rubric law / intent leak) · Disciplines #1, #11, #62(a), #64, #72, #73, #75 cl. 6, #79/Law 3, **#80**, **#86** · ADR-002, ADR-004, ADR-006 · CLAUDE.md conflict-rule corollary

---

## 0. Verdict in one paragraph

The design in § 2 is right and I have no better architecture to propose: *union of kit-internal mechanisms + one boundary rulebook + a golden master that the levers may not break* is the correct answer to Q86, and § 2.6 carries E-1 exactly as Matt ruled it. The seven BLOCKs are not design objections. **Six of them are the same species and it is the species this project keeps paying for: an instrument that returns cleanly after it stopped answering the question.** The golden master — the charter's own "line in the sand" — is substantially unfalsifiable against the very refactor it exists to guard (BLOCK-A), and nothing anywhere asserts that the refactor leaves the `ORACLE` config alone, while § 4.3 refactors the oracle by name (BLOCK-B). The self-join cannot fail as written (BLOCK-C). The lever row cannot evaluate as written (BLOCK-D). The coverage gate is gameable in two directions, which is the one lesson a FAILED run already paid for (BLOCK-E). A quantity inside a DONE predicate has no pinned substrate (BLOCK-F). And the two folds that mint durable classifications have no independent gate (BLOCK-G). Every one clears with a row, a clause, or a table cell. **None needs Matt except the launch-sheet widening at WARN-4.**

---

## 1. The asked questions, answered

**Fit test honesty (§ 3).**
**F1 — substantially YES, one arithmetic defect.** J-S1…J-S5 are enumerable, the kit is one, the lever set is closed at 16. I checked the census sub-counts by hand against `elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md`: BOUNDARY `8 AS-IS + 14 WIDEN + 3 GD-EMPTY = 25` ✓; per-kit AS-IS `3+3+1+1 = 8` ✓; WIDEN `6+4+2+2 = 14` ✓; GD-EMPTY `2+1 = 3` ✓; levers `14 settable + 2 build items = 16` ✓ against census § 9. **The headline does not close:** `15 + 25 + 5 + 1 = 46`, not 49 (**WARN-1**).
**F2 — NO, not yet, and this is the review's weight.** § 4 has six rows. **Row 2 cannot fail** (BLOCK-C), **row 3's gate is largely unfalsifiable** (BLOCK-A), **row 4 cannot evaluate** (BLOCK-D), **row 5 can be satisfied by relabelling** (BLOCK-E) **and contains an unsourced measurand** (BLOCK-F), and row 5 also carries the one word in § 4 that is not a predicate — *"playable"* (**WARN-6**). § 3 F2's own claim (*"YES, except the feel verdict"*) is honest about the feel verdict and silent about these. The pattern's test is *"'done' is a fact the run can check"* — on four of six rows it is not yet.
**F3 — YES, and the drain is real.** Five forks on the launch sheet, each with one recommendation. The residual — lever *forms* — is genuinely a reasoning boundary. One under-scoping (**WARN-4**) and one boundary-class mislabel in the other direction (**WARN-5**).
**F4 — YES**, and § 3 F4 raises the `SPEC-AUTHOR → DRIFT-CRITIC` switch against the conductor's own ARCHITECT pass unprompted. Credit.

**Is the target-state decidable without Matt?** Not as drafted — see F2 above. It becomes decidable on the seven BLOCK edits, and none of them requires Matt.

**Reasoning-boundary vs commitment-boundary mislabels.** One in each direction. **Commitment mislabelled as reasoning:** C-11 routed to J0 as a run item (**WARN-5**) — if the oracle's ~×1.9 over-lethality disposition would move the referent, the golden master's basis changes inside the run whose central invariant is replaying it; and § 2.3's *"declared default"* for a boundary where GD is silent is an invented constant wearing an inherited constant's label (**BLOCK-D(i)**). **Reasoning correctly kept as reasoning:** lever forms, the OUT-OF-ARENA bucket, the J0 ablation classes — all properly the conductor's, which is why BLOCK-G asks for a gate on the last of them rather than a HALT.

**Unit / label hygiene.** The disk floor is the best-stated in the series — *"free disk < 40 GiB by `df -h` (unit stated, per KP-91)"* applies KP-91's own proposed standing fix, in GiB, the unit Matt was shown (**INFO-2**). The digest labels do not (**WARN-2**): § 7 mandates *"digests derived, never retyped, **and labelled FILE vs ROWSET**, KP-101"* and § 1 prints `5cab7433…` / `978f54ab…` unlabelled, in the same document. **#75 cl. 6 one level up — the law is stated in § 7 and not applied to § 1 of the document stating it.**

---

## 2. BLOCK findings

### BLOCK-A — the golden master is substantially unfalsifiable against the refactor it exists to guard (#80, #86)

§ 2.4 and § 4.3 make one claim carry the whole run: *"the GD-REFERENT profile, run through the rulebook, must reproduce REFERENT-v1 on **every EXACT row of prereg v1.6**, on every commit that touches the join path. A lever change that breaks the replay is a regression, not a design choice."* **The EXACT set cannot bear that load, and I established why one lap ago in my own prereg pre-read** (`qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md`), which is the reason I can state it without re-deriving it here:

- **Not one of the 29 EXACT rows requires an oracle-side execution.** Walked row by row at the pre-read: every row grades against the port itself, a pack constant, an identity or structural zero, or a source-level structural claim. A gate with no oracle-side execution does not compare a refactored rulebook to the sealed fight; it compares it to constants that a refactor does not touch.
- **Eight of the 29 carry at least one clause satisfied by an absence or unexercised on the graded path** — `TA-X-11`, `12`, `15(b)`, `17`, `19`, `25(a)`, `25(c)`, `28(a)` absence-satisfied; `TA-X-29(d)` unexercised (0 of 29 inert records fall inside waves 151–160). **A row that scores zero because the code path does not exist scores zero again after any refactor that preserves the non-existence.** That is #80 verbatim — *"a port with no wall also scores zero"* — and #86 for the unexercised one.
- **`TA-X-06` cannot be honestly greened** and the seal is gated on Matt's `Q83(b)`. The golden master's basis is itself unsealed at the time of writing.

**Why this is a BLOCK and not a WARN.** The charter has exactly one structural safety against a refactor that changes behaviour, and it is this. § 2.4's sentence is quotable, memorable and, as specified, largely green-by-construction. The run would ship a rulebook, print GOLDEN MASTER GREEN, and have measured almost nothing about the thing it changed.

**Minimal discharge (conductor; § 4.3 gains one clause and § 1 gains one row).**
1. **Classify the 29 EXACT rows into three named sets:** `EXECUTES-THE-BOUNDARY-RULEBOOK` · `ABSENCE-SATISFIED` · `DOES-NOT-TOUCH-THE-JOIN-PATH`. Print the classification in § 4.3. **The first set must be non-empty and named, and the golden master's verdict is over that set;** the other two are reported, never quoted as the gate.
2. **Freeze REFERENT-v1's per-row NUMERIC outputs as a fixture** (a substrate row: the sealed run's emitted values, at their derived digest), and make the replay a **diff against that fixture**, not a re-grade of pass/fail predicates. A pass/fail re-grade is satisfiable by two systems that moved together; a numeric diff is not.
3. If a row in `EXECUTES-THE-BOUNDARY-RULEBOOK` cannot be found at all, say so on the charter's face — that is a finding about the instrument, and it is far cheaper to learn now than at J2.

### BLOCK-B — `ORACLE (unchanged)` and `PLAY (unchanged)` are prose in § 0, and § 4.3 refactors the oracle by name. Nothing asserts, gates or pins the invariance

§ 0 promises *"three configurations of one runtime: `ORACLE` (graded; **unchanged**), `PLAY` (Matt's; **unchanged**), and `JOIN`."* § 4.3 then reads: *"boundary rules extracted into a named module **in the oracle and in the port**."*

**The oracle is the artifact REFERENT-v1 was sealed against.** Refactoring both sides of a comparison, with the comparison expressed as pass/fail predicates rather than frozen numbers (BLOCK-A), permits **symmetric co-drift**: T-A still passes, the golden master still reads green, and both systems have moved off the sealed fight together. The seal record itself includes a **runtime digest**; after J2 that digest describes code that no longer runs, and the charter says nothing about re-deriving it or accounting the delta.

The prompt asked whether the ORACLE-config invariance is asserted anywhere. **It is asserted in one parenthesis and enforced nowhere.** § 4 has no invariance row; § 6's HALT list has no clause for it; the golden master is defined over the JOIN-side GD-REFERENT profile, which is not the same claim.

**Minimal discharge (conductor; one substrate row, one § 4 row, one HALT clause).**
1. **J-S6** — the sealed oracle at its commit and derived digest, plus the sealed runtime digest, pinned as frozen substrate. The pre-refactor oracle is preserved (tag or frozen copy), so the replay can run against **the sealed oracle**, not its successor.
2. **§ 4.7** — *"the `ORACLE` and `PLAY` configurations emit byte-identical output before and after every commit on the join path."* This is the negative control on the refactor itself, and it is the same instrument § 4.4 already demands of every lever — owed here first, because it is the refactor that can move everything at once.
3. **§ 6** — *"a change in `ORACLE` behaviour is a HALT to Matt, never a lever and never a J2 finding."*

### BLOCK-C — the self-join (B0) cannot fail as written, and its one possible failure is confounded (#80)

§ 4.2: *"Self-join (B0) graded: `gd-eor-warlord.json` → kit compiler → the arena, compared against REFERENT-v1. **Every lost quantity is listed as a named schema gap.**"*

**The prompt asked whether B0 can fail and what a failure means. As drafted it cannot fail, and a failure would mean nothing attributable.**

- **No threshold.** The predicate is satisfied by *listing* whatever is lost. A self-join that loses ninety per cent of its quantities satisfies § 4.2 completely. The architect pass called B0 *"same kit, same fight, **known answer**"* and *"the cheapest test of Failure Mode 2 we will ever get"* — the charter converted a test with a known answer into a census with no answer.
- **Confounded attribution.** `kits-export/gd-eor-warlord.json` is graded **APPROX** (J-S4; census § 0 finding 5: the GD rulebook's *operands* are welded to one character). REFERENT-v1 is sealed. Any divergence is un-attributable between **"the corpus path loses information"** (the thing B0 exists to measure) and **"the APPROX kit JSON was never accurate"** (a fact about the artifact). Without separating them, every B0 number means two things.
- **Its consumer is missing.** Architect § 5 carries **TL** (GD-SLICE template lock) as `GATED+TRACKED`, criterion *"B0 + B1 results"*. B1 landed 2026-09-28 with the verdict *"the shape is not ready to lock"*. § 4.2 produces the other half and the charter's § 8 has no TL row to receive it (**WARN-3**).

**Minimal discharge (conductor; two clauses in § 4.2).**
1. **A pass rule:** *"B0 PASSES when the corpus path reproduces the referent on the `EXECUTES-THE-BOUNDARY-RULEBOOK` set (BLOCK-A), **or** when every divergence carries a disposition in {`closes-in-J2` · `schema-change-owed` (→ J-L4) · `permanent, recorded`}. A gap list with an undisposed row is a B0 FAIL and a finding, not a deliverable."*
2. **Deconfound before grading:** re-grade `gd-eor-warlord.json` against the sealed pack first, **or** declare the APPROX ceiling on the B0 report face so no B0 figure is ever quoted without it. *(Same species as KC2-PLAY WARN-2's missing `instrument` attribution class.)*

### BLOCK-D — § 4.4's lever row cannot evaluate as written. Two limbs, and the first launders silence into a default (#79 / Law 3)

§ 4.4: *"Lever registry v0: 14 settable levers + 2 build items registered, **every one OPEN at GD's setting**, each with a negative control proving the lever is live."*

**(i) "At GD's setting" is false for at least four levers, and the census's remedy was dropped in the fold.** From census § 9: **L-03** `max_hp_change_policy` — *"no GD rule — Ascension is flat"*; **L-08** `proportional_damage_mitigable` — *"undefined"*; **L-11** `generic_damage_taken_mult` — *"no generic term"*; **L-16** `agency_model` — GD-EMPTY. The census anticipated exactly this and made a recommendation the charter does not carry (§ 7.1): *"the lever-registry schema should carry `status = OPEN` **plus** a `gd_referent_value` that can be **`NONE — no GD rule`**, distinct from a GD value that happens to be zero. **A registry that cannot say 'GD is silent here' will launder silence into a default.**"*

**L-03 is the live instance, and it is not cosmetic.** D2's Battle Orders raises max HP mid-fight. `preserve-current` vs `preserve-fraction` changes the joined kit's effective HP and therefore **its arena margin — the very quantity E-1 exists to record.** Recording the chosen value as *"GD's setting"* records an invented constant as an inherited one. That is Law 3 with the label on backwards.

**(ii) Negative controls are demanded for 14 levers and seated for 7.** § 5 J3 builds `crit_model` *"then the D2-needed six"* — eight lever ids under six headings (`pth_floor`/`pth_ceiling` and `proportional_damage_offense`/`_mitigable` are pairs). **L-09, L-10, L-11, L-12, L-13, L-16 are PoE1/PoE2/VS-driven and no seat builds their alternate settings.** A negative control requires the off-default path to exist. § 4 is headed *"DONE when every row evaluates"*; row 4 cannot evaluate TRUE under § 5's own wave plan. That is the pattern § 1 partial-function hazard inside the decidable list.

**(iii) A third-order inconsistency inside § 2.** § 2.3 — *"GD-EMPTY rows are build items, not levers"* — yields **3** build items (L-14, L-15, L-16) and 13 settable, contradicting § 4.4's 14 + 2 and the census, which classes only L-14 and L-15 as build items (*"a lever parameterises an existing mechanism, and there is no mechanism to parameterise"*). **L-16 `agency_model` is settable** — `{player-driven (GD default) | autonomous}`. As § 2.3 reads, L-16 escapes the negative-control discipline by misclassification.

**Minimal discharge (conductor; one schema field, one scope clause, one word).**
1. Registry schema gains **`gd_referent_value ∈ {value | NONE — no GD rule}`**, and § 4.4 reads *"every one OPEN at GD's setting **or, where GD is silent, at a DECLARED-INVENTED default carrying its author and its reason**."* Name L-03, L-08, L-11 as the instances on the charter's face.
2. § 4.4's negative-control clause scopes to *"every lever whose alternate setting is implemented in this run (the `crit_model` + D2 set, 8 ids); the remaining 6 are REGISTERED-UNEXERCISED and say so in the registry."*
3. § 2.3 reads *"the two GD-EMPTY rows with no mechanism to parameterise (L-14, L-15) are build items"*, not *"GD-EMPTY rows"*.

### BLOCK-E — the kit coverage gate is gameable in two directions. This is the one lesson a FAILED run already paid for (pattern § 6.1)

§ 4.5: *"every mechanism mapped INTERNAL / BOUNDARY / OUT-OF-ARENA, **zero unmapped** (a coverage gate on the kit's own census)."*

Pattern § 6.1, from KIT-FIDELITY: *"For any fidelity/twin run, the FIRST pre-registered gate is **coverage** of the watched surface … Run them in the wrong order and you **certify a sliver and call it a twin**."* This charter has a coverage gate — which is progress over KC2-PLAY, whose absence I BLOCKed on 2026-09-20 — but it is gameable twice:

- **The denominator is run-controlled.** *"the kit's own census"* is not pinned to the 14 D2 rows frozen at J-S2. If J4 re-censuses the kit, the run owns both numerator and denominator. **And `OUT-OF-ARENA` is an unconstrained escape hatch:** it is a class with no implementation obligation, D2 already has two rows in it, and nothing forbids a third being added when a mechanism proves expensive.
- **"Mapped" is not "implemented".** All nine D2 BOUNDARY rows can be mapped, with every WIDEN lever left OPEN at GD's default, and coverage reads **100 %** — a D2 Whirlwind Barbarian playing entirely under Grim Dawn's rules. That is 100 % coverage of a sliver, one level up from the failure the observation was written to prevent.

**Minimal discharge (conductor; one sentence in § 4.5).** *"The coverage denominator is **J-S2's frozen 14 D2 rows**. Any addition, removal or reclassification after launch — `OUT-OF-ARENA` especially — is a named finding carrying its reason, never a silent re-map. Beside the coverage fraction the run prints a second fraction: **of the BOUNDARY/WIDEN rows, how many have their D2 setting implemented and ACTIVE in the `JOIN` profile** versus left at GD's default."* The second number is the one that says whether a kit joined or merely compiled.

### BLOCK-F — "home margin" sits inside a DONE predicate and has no pinned substrate (#1, Principle 1)

§ 4.5 requires *"home margin and arena margin both recorded"*; § 2.6 makes the distance between them the **fidelity cost**, *"recorded and never hidden"*. That clause is E-1's honesty clause and it is the reason J-L3's *record-only* posture is defensible at all.

**Measuring D2's home-game margin requires D2's frontier** — monster HP, defences and resistances at the build point — and § 1 pins none of it. J-S3 pins `Skills.txt` rows 151 + 149, the D2 formula set, and the kit JSON: that is the **kit**, not the **frontier**. The census records `MonStats.txt` resist columns as *"held but not read this lap"* — unpinned, ungraded, and no seat in § 5 names them. § 5 J4 seats legolas for *"D2 formulas + primary rows"*, which might cover it and does not say so.

A frozen-substrate table headed *"count it, list it, diff it"* that omits the source of a quantity in the DONE predicate fails the pattern's own test. And the failure mode is specific: the run reaches J4, finds no frontier, and either derives one (a fitted constant inside the honesty clause) or drops the measurement (E-1's *"never hidden"* voided in silence).

**Minimal discharge (conductor; one substrate row, or one honest narrowing).** Either **J-S7** — the D2 frontier source at its pinned commit and build point, with its fidelity grade — **or** narrow § 4.5 to *"arena margin recorded; **home margin DEFERRED**, re-entry criterion: a pinned D2 frontier source"*, with the deferral printed **on the fidelity-cost table's own face** so the gap travels with the artifact rather than staying in the charter.

### BLOCK-G — the two folds that mint durable classifications have no independent gate (pattern § 5.2)

§ 5 seats jack-ryan at **J2** (Gate-2) and **J5** (handoff). It seats no gate at **J0** or **J1**, and both mint state the rest of the run inherits:

- **J0, the ablation map,** classes every mechanism **LOAD-BEARING / INCIDENTAL** by measurement, and § 2.5 says it *"yields GD's E-2 signature-feel checklist by measurement."* That is an in-run classification becoming **canon** (era-substrate § 7's E-2), and the lever registry's `load_class` column inherits it directly.
- **J1, the self-join,** produces the named schema-gap list that architect § 5 gates **TL** on and that J-L4's schema change is justified by.

Pattern § 5.2 routes in-run reclassifications to independent Gate-2; Run A's Gate-B is the founding exemplar; and **this is my own KC2-PLAY BLOCK-C one lap on** — *the reclassification never left the run*. By J2 the ablation classes are already load-bearing inputs, and a gate at J2 reviews a conclusion rather than the fold that produced it.

**Minimal discharge (conductor; two table cells).** § 5 J0 gate gains *"jack-ryan Gate-2 on the LOAD-BEARING / INCIDENTAL classification and on the derived E-2 checklist"*; § 5 J1 gate gains *"jack-ryan Gate-2 on the schema-gap list before it is quoted at J-L4 or against TL."*

---

## 3. WARN findings — each with the edit that clears it

**WARN-1 — J-S2's headline arithmetic does not close.** `15 INTERNAL + 25 BOUNDARY + 5 OUT-OF-ARENA + 1 HELD = **46**`, and the row says **49**. The census is explicit (§ 0): *"46 rows + 3 cross-cutting misfits (§ 7.3–7.5) = 49"*. The three dropped rows are not incidental — they are exactly the work § 5 J0 seats (the docket-disposition sweep is § 7.5; `mechanism_grade` / `magnitude_grade` are § 7.3). In a table headed *"frozen at launch"* the sum must close (#63).
**Edit:** *"**46 classed rows + 3 cross-cutting misfits (census § 7.3–7.5) = 49**"*.

**WARN-2 — J-S1's digests are unlabelled in the charter whose § 7 mandates the label.** § 7 carries *"digests derived, never retyped, **and labelled FILE vs ROWSET**, KP-101"*. J-S1 prints `model 5cab7433…` / `reference 978f54ab…` bare. Per prereg v1.6 (verified at my pre-read) both pack digests are **computed over member lists under the manifest's own law** — ROWSET-shaped identities, and KP-101's whole finding was that *"they are different objects under one word."* **#75 cl. 6, one level up: the law is stated in § 7 and not applied to § 1 of the same document.**
**Edit:** label both, or drop the tails and keep only derive-at-launch — the second is more in the row's own spirit.

**WARN-3 — three of the architect pass's four `GATED+TRACKED` items lost their carrier (#73).** Architect § 5 tracked **E-1** (now RULED ✓), **E-2**, **GV**, **TL**. Charter § 8 carries J-P1, C-11, `ABS-C-I14-2`, lever settings and J-L1…L5 — **no TL row at all**, though TL's criterion (*"B0 + B1 results"*) is now half-fired and the other half is § 4.2. **GV** appears only as a routing phrase inside a J0 table cell (*"the 675 MEASURED→DATAMINED re-grade routed to jack-ryan"*), not as a tracked fork. **E-2** appears only as a § 2.5 output. A tracked item whose gating criterion fires while its carrier is dropped is #73 exactly.
**Edit:** § 8 gains three rows — **TL** (`GATED`, criterion now B0 at § 4.2; B1's verdict already *"not ready to lock"*), **GV** (`OPEN — jack-ryan`, 675 rows, opens at J0), **E-2** (`DERIVED AT § 4.1`).

**WARN-4 — J-L1 asks Matt about one docket where the census names six more and a family, and warns the sweep must land before the registry is seeded.** Census § 7.5: docket **5** is the instance, *"the same tension will recur for dockets **1, 3, 4, 7, 8** … and for the `§5.2` family rows **9–19**. Q86 may have **re-opened a set of docket dispositions that were closed under the pre-union architecture** … worth a deliberate sweep **before B3 seeds the lever registry.**"* J-L1 routes the instance; § 5 J0 seats the sweep; nothing says where the sweep's further hits go. Matt rules once and the run meets six more collisions with no rule.
**Edit (this is the one Matt surface in the review):** J-L1 asks for the **rule** — *"Q86 supersedes any pre-union docket disposition that closed a kit-internal mechanism as `permanent-gap-record`; docket 5 is the first application; the J0 sweep's further hits are re-dispositioned under the same rule and returned to you as one batch, never silently."*

**WARN-5 — C-11 is routed to J0 as a run item, and its disposition may be a commitment boundary.** § 8: *"C-11: the oracle's ~×1.9 over-lethality (deaths at 151–156 vs 160) — `GATED+TRACKED`: issued if Matt's T-C says 'too deadly', else at JOIN-1 J0."* If C-11's finding would alter REFERENT-v1, **the golden master's basis changes inside the run whose central invariant is replaying it byte-green.** That is a Matt-reserved event wearing a J0 label.
**Edit:** § 6 gains *"a C-11 disposition that would alter REFERENT-v1 is a HALT to Matt, not a J0 finding."*

**WARN-6 — *"playable in the desktop build beside the Warlord"* is the one § 4 row that is not a predicate (pattern § 6.3, intent leak).** § 3 F2 honestly converts the **feel** verdict to the post-run HITL. *"Playable"* is neither converted nor defined, and it sits inside the list headed *"DONE when every row evaluates, **without Matt**."* Read one way it is mechanical; read another it is the owner's question, and a run cannot check the owner's question.
**Edit:** define it — *"the kit loads from `kits-export`, binds, and executes to a terminal state without exception across the scripted pilot, emitting both margins"* — and state that everything past that is the post-run HITL's, explicitly.

**WARN-7 — the damage-family registry is named BOUNDARY and exercised by no kit in JOIN-1; J-L2's deferral is defensible and unpriced.** Census § 6 B8 is called *"the census's most actionable warning"*: `threat.mitigate` **raises `KeyError`** on an unmapped family by design (GL-12: *"a silently-unresisted family is exactly how an invented number gets into a fight model"*), **the Q88 slate is four physical kits**, and *"a reader could conclude the registry is fine. It is not: it is a loaded refusal that the slate happens not to touch."* J-L2 defers non-physical kit #3 to JOIN-2 — good for decidability, and it means rulebook v0 and lever registry v0 are both **built and locked without the registry ever firing**, which is precisely *"before the adapter is built on the assumption that it passes."* Note also that **L-12 `control_family_registry` is in no J3 build set.**
**Edit:** J-L2's recommendation gains one clause — *"rulebook v0 declares the damage-family registry **UNEXERCISED-IN-JOIN-1** on its own face, and `mitigate`'s `KeyError`-on-unmapped is **preserved, never defaulted**"* — the oracle's own refuse-loudly precedent, which the census names.

**WARN-8 — the negative control's second half proves reversibility, not liveness (#86).** § 4.4: *"flipping it off-default moves the relevant metric; flipping it back restores the golden master byte-for-byte."* The first clause is the real control; the second is a round-trip check. A lever whose off-default path is never executed on the graded path round-trips perfectly and moves nothing.
**Edit:** *"…moves the **named** metric, in the **predicted direction**, by a **recorded magnitude**; the round-trip is reported beside it, never in place of it."*

**WARN-9 — no conductor-compaction / charter-freshness HALT, in a charter whose own model is intent-residency-by-charter.** § 6's HALT list is otherwise strong (see INFO-7) and carries no clause for conductor session loss, though the gandalf OP carries a post-compaction charter-freshness gate and a compacted conductor is the failure that model exists to survive. Same gap I raised at KC2-PLAY WARN-6(b).
**Edit:** *"on conductor session loss or compaction, the successor re-reads this charter and the ledger before any fold, and records a freshness line."*

**WARN-10 — the owner's eye is scheduled only after the run ends, and JOIN-1's output is a watched surface (pattern § 6.2).** § 0: *"Matt plays the joined kit after it, as a HITL session."* Observation 2 was paid for by KIT-FIDELITY: *"When the run's output is a watched surface, the owner's eye is not a briefing recipient; it is an **instrument of record** … Schedule the owner's eye as a gate, at named mid-run points, **before** downstream gates build on unviewed state."* Both KIT-FIDELITY catches were Matt's, mid-stream, after the run's own gates said green twice.
**Edit:** one named mid-run owner-eye checkpoint — the natural one is **after J3's `crit_model` lands and before J4 builds the D2 kit on top of it**, since `crit_model` is the widening every downstream kit inherits.

---

## 4. INFO findings

- **INFO-1 — the census arithmetic checks, and the one that does not is the headline.** Verified by hand against the P0 census: BOUNDARY `8 + 14 + 3 = 25` ✓; per-kit AS-IS `3+3+1+1 = 8` ✓; WIDEN `6+4+2+2 = 14` ✓; GD-EMPTY `2+1 = 3` ✓; levers `14 settable + 2 build items = 16` ✓ (§ 9); `d2-ww-barb` = 14 rows, 9 of them BOUNDARY ✓. Only the `46`/`49` headline fails (WARN-1). File hash `b8c2cb92…` matches the brief exactly.
- **INFO-2 — the disk HALT is the best-stated in this series, and the headroom is thin.** *"< 40 GiB by `df -h` (unit stated, per KP-91)"* applies KP-91's own proposed standing fix — the conductor's self-booked defect turned into a standing instrument, in the unit Matt was shown. **Measured this session: `/System/Volumes/Data` 59 GiB available** — 19 GiB above the HALT line, for a run that builds a desktop `.app` and encodes captures. KC2-PLAY's own seal lap lost 4 GiB in a single session and HALTed at 39.87 GiB. Not a defect; an operational fact the launch line should carry.
- **INFO-3 — both external WARNs from my prereg pre-read were discharged before this gate.** `canonical/matt_decision_needed/README.md` row **Q83 is RESTATED 2026-09-29 (KP-106)**: *"(b) IS NO LONGER RECORD-ONLY — IT BLOCKS THE SEAL AND GATES GRADED ATTEMPT 1"*, carrying the **26 → 29** EXACT-row reconciliation in the same row, *"said here so the number did not move silently."* Recorded because it means **J-P1's gating question is now correctly priced on the surface Matt reads**, which is a precondition of this charter being launchable at all.
- **INFO-4 — J-L5 re-asks for `reincarnated-godot` rather than inheriting it, and that is correct.** CLAUDE.md scopes the godot extension *"for the duration of **Run KC2-PLAY**"*; JOIN-1 is a new run, so the inheritance would have been silent scope growth. One obligation on landing: **CLAUDE.md's push-pattern section carries its own recording mandate** (*"recorded here, and not only in the session that received it"*), so the new posture is folded there, not only into the charter.
- **INFO-5 — J-L4 drops the property that made `vocab_scope` worth having.** The census calls it *"**mechanically derivable today** from the key prefix, therefore auditable rather than asserted, and it would have caught the drift in § 8.2 automatically."* J-L4 lists it as one of four additive columns with no such note. Carry the derivability; it is the difference between a column and a check. *(The two-column → four-column expansion, adding `mechanism_grade` / `magnitude_grade` from census § 7.3, is a legitimate consolidation and the `le-park` / `source_urls` freeze-not-drop precedent is the right one.)*
- **INFO-6 — pre-launch state is consistent with NOT LAUNCHED.** No `join*` tree under `agentic_orchestration/`; `simulation/kit_compiler/` and `research/curated/kits-export/` exist as pinned. Recorded so a re-check can tell what moved.
- **INFO-7 — what I could not fault, named, because it is most of the charter.** § 2 is the right architecture and I have no better one. § 6's HALT list carries the **committed-truth conflict** clause (my KC2-PLAY WARN-5), the **write-outside-the-named-tree** clause (WARN-6c), the **two-failed-attempts-at-one-gate** clause, and *"any lever moved off GD's setting outside kit #2's own profile"* — a HALT written against the run's own most likely temptation. § 7's standing-laws line carries the corrected `--only` / `--porcelain` / `show --stat` instrument (#62(a) fourth amendment) without being asked. § 3 F4 raises `SPEC-AUTHOR → DRIFT-CRITIC` against the conductor's own ARCHITECT pass. And § 7 ends *"derive, don't relay (KP-65, KP-86, KP-95, KP-100: **four relay defects in two laps, three of them the conductor's**)"* — **a charter that prints its own author's failure rate on its face is § 5.4 working.**

---

## 5. Action summary

**gandalf / conductor — pre-launch. Seven BLOCKs; none needs Matt:**
- [ ] **BLOCK-A** — classify the 29 EXACT rows into `EXECUTES-THE-BOUNDARY-RULEBOOK` / `ABSENCE-SATISFIED` / `DOES-NOT-TOUCH-THE-JOIN-PATH`; the golden master's verdict is over set 1, which must be non-empty and named. Freeze REFERENT-v1's per-row **numeric** outputs as a fixture and make the replay a diff, not a re-grade.
- [ ] **BLOCK-B** — J-S6 pins the sealed oracle + runtime digest and preserves the pre-refactor oracle; § 4.7 asserts `ORACLE`/`PLAY` byte-identical across every join-path commit; § 6 HALTs on any `ORACLE` behaviour change.
- [ ] **BLOCK-C** — give B0 a pass rule and a per-gap disposition set; deconfound the APPROX kit JSON from the corpus path before grading.
- [ ] **BLOCK-D** — registry gains `gd_referent_value = NONE — no GD rule`; declared-invented defaults named for L-03 / L-08 / L-11; negative controls scoped to the 8 implemented lever ids with the other 6 `REGISTERED-UNEXERCISED`; § 2.3 names L-14/L-15 rather than "GD-EMPTY rows".
- [ ] **BLOCK-E** — coverage denominator fixed to J-S2's 14 D2 rows, reclassification is a named finding, and a second fraction prints implemented-and-active WIDEN levers beside coverage.
- [ ] **BLOCK-F** — pin the D2 frontier source (J-S7) or narrow § 4.5 to arena margin with home margin DEFERRED, printed on the fidelity-cost table's face.
- [ ] **BLOCK-G** — § 5 seats jack-ryan Gate-2 at **J0** (ablation classification + E-2 checklist) and **J1** (schema-gap list).
- [ ] WARN-1 `46 + 3 = 49` · WARN-2 label FILE vs ROWSET · WARN-3 § 8 gains TL / GV / E-2 rows · WARN-5 C-11-alters-referent is a HALT · WARN-6 define "playable" · WARN-7 registry UNEXERCISED-IN-JOIN-1 + preserve the `KeyError` · WARN-8 negative control names metric, direction, magnitude · WARN-9 compaction / charter-freshness clause · WARN-10 one mid-run owner-eye checkpoint after J3's `crit_model`.
- [ ] INFO-2 carry the measured 59 GiB on the launch line · INFO-4 fold J-L5's posture into CLAUDE.md on landing · INFO-5 carry `vocab_scope`'s derivability.

**Matt — the launch sheet as drafted, with one widening:**
- [ ] **J-L1, widened (WARN-4).** Rule the **rule**, not only docket 5: does Q86 supersede *every* pre-union docket disposition that closed a kit-internal mechanism as `permanent-gap-record`? The census names dockets **1, 3, 4, 7, 8** and family rows **9–19** as the same collision and says the sweep must land **before** the lever registry is seeded. Conductor's recommendation on docket 5 is sound; it is the scope that needs your word.
- [ ] **J-L2, J-L3, J-L4, J-L5 as drafted** — each is genuinely yours, each carries exactly one recommendation, and I agree with all four. J-L2 wants one clause added (WARN-7); J-L3's *record-only* posture is the right call and is only honest once BLOCK-F gives "home margin" a source.

**ADR-002 approval authority.** Every conductor item above is charter wording, a substrate-row addition, gate placement, or a registry-schema field inside a not-yet-launched draft — **mine to approve directly, and I approve them on execution.** The one cross-seam schema change (`corpus.db` additive columns) is **J-L4, correctly routed to Matt** and correctly gated on a MIGRATION at § 5 J0 (ADR-004). **GV** — the 675 `exact_skill` rows carrying `fidelity_grade = MEASURED` where the era-substrate LAW § 4 says DATAMINED — is routed to my seam and I accept it; it opens at J0 and I will file it as a separate finding, not inside this gate.

**Gate-1 verdict: BLOCK — narrow.** Seven BLOCKs, seven edits, none of them a design objection and none of them Matt's. **The architecture in § 2 is correct and the launch sheet is well-drained.** What is missing is the same thing that was missing at C-7 and at KC2-PLAY, one level deeper each lap: **the run is relying on instruments that would return cleanly whether or not the thing they measure is true.** The golden master is the important one. Fix it and this charter is GO.

---

## 6. References

**Under review**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.1 DRAFT, `b8c2cb92…`, 93 lines)

**Authority + substrate consulted**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-28-join-key-architect-pass.md` (§ 8 governs; § 5 open-questions gate incl. TL / GV / E-2)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` (`78797db4b`) — §§ 0, 2–7, 8.2–8.3, 9
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/operating-procedures/desirable-run-pattern.md` — §§ 1, 3, 4, 5, 6.1, 6.2, 6.3
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` — ledger KP-82, KP-83, KP-84 (L3 paper-only), KP-85, KP-91 (disk unit), KP-101 (FILE vs ROWSET), KP-106, KP-107
- `/Users/admin/Games/reincarnated-collaboration/canonical/matt_decision_needed/README.md` — rows Q83 (RESTATED 2026-09-29), Q85–Q89
- `/Users/admin/Games/reincarnated-collaboration/canonical/00-ground-state.md` · `/Users/admin/Games/reincarnated-collaboration/CLAUDE.md` (push-pattern section, KC2-PLAY godot extension)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md` — the EXACT-row walk BLOCK-A rests on
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-20-run-KC2-PLAY-charter-gate1.md` — the precedent gate (BLOCK-B coverage, BLOCK-C independent gate, WARN-5/6 HALT clauses)

*Filed 2026-09-29 by jack-ryan, DESIGN-MODE Gate-1, pre-launch. Target hash derived before reading, per the brief's HALT condition. No production code. No push.*
