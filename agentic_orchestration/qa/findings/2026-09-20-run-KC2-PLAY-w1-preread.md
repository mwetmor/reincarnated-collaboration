# Finding — 2026-09-20 — Run KC2-PLAY · WAVE-1 PRE-READ (the W1 seal)

**Reviewer:** jack-ryan (DESIGN-MODE — goalposts reviewed before any result exists)
**Verdict:** ⚑ **NO-SEAL** — 2 BLOCK · 5 WARN · 3 INFO. Both BLOCKs are **propagation defects with cheap discharges; neither needs Matt; neither indicts the prereg's content.**
**Target:** charter `c44d773d7294` (KP-2…KP-15) · prereg **v1.2** `72204f7a` · widths `a2150122` + Add. 1 `b1210565` + Add. 2 `5cd34a75` · register **v0.1** `540fd4b4` · galadriel W1 `10a85641` + follow-on `b3f175ff` · v3.2 lift `983485fb` · `reincarnated-godot/kc2_runtime/`
**Authors reviewed:** gandalf (`SPEC-AUTHOR`) · gamora · galadriel · drax
**Gate:** charter § 5 W1 gate column + Gate-1 **WARN-16** (a prereg reviewed after a result exists is not a prereg)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code) · #3 (cross-seam impact) · #4 (decisions-log / register as truth) · #5 (severity matters) · Disciplines #11 (empirical inspection over assumption) · #12 (semantic shift disclosed) · #73 (the state moved and the record did not follow) · K-7 · Law 3 · D4

---

## THE LINE THAT MATTERS

**The prereg is IMMUTABLE, and its T-A content is SOUND.** I sampled eight of the twenty-three `EXACT` rows against their cited sources and re-derived three bands from the sealed per-salt spreads; every one held, and `TA-X-24` — the row most exposed to the failure shape this run has hit three times — rests on the **driver of record**, not a module default. I found no reason to doubt a single graded row.

**It may not yet be used to grade.** Not because a row is wrong, but because **precondition P-1 cannot go green against the artifacts as they currently stand**: the mechanical gate that must emit `89/89` is hard-coded to `72`, and the prereg's own sha-pinned *governing* companion still states the coverage rule as `72 / 72`. P-1 is a precondition; T-A does not run until it is green. That is BLOCK-1, and it is fifteen minutes of propagation, not a design question.

---

## BLOCK-1 · The superseded denominator **72** is still live-tense in the normative gate text, in the runtime's executable constant, and in the prereg's own pinned governing companion

**KP-9 ruled the coverage denominator is 89 and said "S-2 corrected forward."** S-2 alone was annotated. The ruling never reached four other places, two of them normative and one of them executable:

| where | text as it stands | status |
|---|---|---|
| charter § 4.3 — `2026-09-20-kc2-play-run-charter.md:57` | *"All **72** census rows mapped mechanically … **counts sum to 72**; zero unmapped … every T-A band is reported as `value @ coverage k/72`"* | ⚑ **the normative gate clause**, unedited |
| charter § 4.4 — `…charter.md:59` | the T-B cap trips at *"coverage < **72/72**-mapped"* | ⚑ vs prereg § G **C3** *"coverage not **89/89**-mapped"* — **two trip conditions for one cap** |
| runtime — `reincarnated-godot/kc2_runtime/loader/kc2rt_coverage.gd:48` | `const CHARTER_DENOMINATOR := 72` · `:225` `var denominator_agrees := (total == CHARTER_DENOMINATOR)` | ⚑ **evaluates FALSE at 89.** `TRANSCRIPT.md:72` prints it live: `COVERAGE RED \| mapped 0/89 (charter pins 72)` |
| widths § E-3 — `…ta-band-widths.md:75-78` | *"Coverage — **72 / 72**, gate before grade … a band reported without `@ coverage k/72` beside it is not a T-A result. **I will not certify a band whose coverage line is absent.**"* | ⚑ this is the file **prereg v1.2 re-pinned at `6709cfe6…` and names as governing** |
| charter § 3 F1 (`:49`), § 9 BLOCK-B discharge row (`:138`) | "72 census rows" | lower-consequence, same defect |

**Rationale.** The coverage gate is deliberately *mechanical* — BLOCK-B bought it precisely so no prose could stand in for a count. A mechanical gate wired to a denominator its own ruling retired will refuse to close, and it will refuse **for a reason that is not the port's** — which is the exact sentence drax wrote into `README.md:82-83` when he escalated it. He was right, KP-9 answered him, and the answer did not travel. Discipline **#73**: the state moved and the record did not follow. The sharp edge is the widths file: the prereg pins it *by sha*, declares it *governing*, and re-pinned it at v1.2 **for exactly this class of reason** — and the governing text says 72.

**Action**
- [ ] **gandalf (conductor):** annotate charter § 4.3 / § 4.4 / § 3 F1 / § 9 forward to **89**, in the same strike-through form S-2 already carries. Propagation of KP-9, not a new ruling — **no Matt.**
- [ ] **drax:** `CHARTER_DENOMINATOR := 89` (or rename to `CENSUS_DENOMINATOR` and retire the disagreement branch); re-emit the transcript.
- [ ] **gamora:** Addendum 3 restating § E-3 at **89 / 89** and `@ coverage k/89`; the prereg then re-pins the widths sha.
- [ ] **jack-ryan:** re-check is a sha diff on four files. Minutes.

---

## BLOCK-2 · The divergence register cross-pins galadriel at a sha that **does not contain the content the register cites**

`…divergence-register-v0.1.md:7` pins *galadriel W1 T-B + `u` rider* at **`0411e6b805e2baa9…`**. Re-hashed: that digest is the **`10a85641`** state (16:24:39). The note was amended at **`b3f175ff`** (16:48:57) — `+38` lines, plus a new 473-line `…-w1-tb-release-labels.json`. Current digest **`8186202cc0c78ae9…`**. The register was committed at 16:55:26, **seven minutes after the amendment.**

This is not staleness. **The register consumes content that does not exist at the sha it pins:**

- **DIV-04** — *"⚑ **σ = 48 ms, MEASURED** — confirming Gate-1 WARN-17's strike."* That sentence is present **only** at `b3f175ff`; a grep of the pinned state returns **nothing**.
- **DIV-15** — ships T-B interrupt rows **slot-indexed** off `…-w1-tb-release-labels.json`, a file that **does not exist** at the pinned sha.
- The two JSON companions the register and prereg both consume (`…-expected-values.json` `a8b85331…`, `…-release-labels.json` `15dace60…`) are **pinned nowhere at all.**

**Rationale.** Law 3 and the run's own *"derived at use, never retyped"* discipline exist so that a downstream reader can dereference a pin and find the claim. Here the pin resolves to a document that **falsifies two of the register's rows**. § F then compounds it: every telemetry header carries `register_sha256`, and *"a recording whose header hash does not match the register in force at grading time is not comparable."* No recording exists yet (§ F ¶3, EPOCH 0 = zero recordings) — which is the one window in which this is free to fix.

**Action**
- [ ] **gandalf (conductor):** register **v0.2**, append-only, no edit to v0.1 — re-pin galadriel at `8186202cc0c78ae9…`; add the two JSON pins; re-pin widths at `6709cfe6…`; Companion line to prereg **v1.2**. Fires before the first recording, so nothing un-pools.

---

## WARN-1 · Prereg v1.2 carries the same stale galadriel pin — in the change table that re-pinned the *other* companion

`…prereg-v1.2.md:8` pins `0411e6b8…`; current is `8186202c…`. § A **row 7** re-pinned the width file with the reason *"a pin to a superseded file state would make `TA-B-09`'s width unlocatable and `TA-B-13`'s reclass invisible"* — and the same read left the second consumed pin at a superseded state, with **KP-10 (the amendment itself) sitting two ledger rows above the commission.**

**Content-innocent, and I want that on the record:** everything v1.2 actually uses from that note — § C.4's `LIVE-MAX`, 42.84 %, 39.76 %, the 181.0 s / 182.65 s windows — **is present at the pinned sha.** T-A gradeability is not compromised. What is compromised is the pin discipline that the whole immutability argument rests on.
**Discharge:** prereg **v1.3**, one-row change table, re-pin only. Legal — no graded run exists (WARN-16's window is still open).

## WARN-2 · Charter **L4** still reads *"two oracle limbs are known-bad"*; the measured answer is **ONE**

`…charter.md:89`. KP-5(7) moved it 2 → **3**; KP-7(ii) and register **ND-04** moved it 3 → **1** (`WarCryLimb.COOLDOWN` and `PotionLimb.TRACE_CONSISTENT` are the cell of record; only `LifeMonitorLimb.POLL_AT_SLOT` survives). S-2 received a strike-through annotation at KP-9; **L4 received none** — inconsistent treatment inside one document, and L4 is the source text for a Matt-facing handoff page he has already accepted.
**Discharge:** annotate L4 forward citing KP-7(ii), the way S-2 was. The register's rewritten handoff sentence is already correct and governs.

## WARN-3 · The register's canonicalisation rule is ambiguous where it must not be

§ F: *"rows sorted by `id`, keys sorted, UTF-8 NFC, **whitespace collapsed**, no insignificant JSON whitespace…"*. If *collapsed* reaches **inside string values**, the hash is not over the emitted bytes, and the runtime's emitter and the grader can implement it differently — at which point § F declares a perfectly good recording *"not comparable."* An EXACT-adjacent mechanism with an under-specified predicate.
**Discharge:** one clause stating whether collapse is structural-only or applies to string values. One line in v0.2.

## WARN-4 · KP-12's charter amendment is an **inference** from Matt's words, recorded as his word

Matt's verbatim asks (1) whether the art is re-used across both zooms and (2) for one image at burst start for style/register review, matching the cliffside and *"represent[ing] the cathedral from that scene."* It **does not narrow § 1's "no painted asset minting."** The conductor's narrowing is a *reasonable* reading, and **KP-14 ("agreed on interior nave") ratifies it downstream** — but the row labels the amendment *"Matt's word — a commitment boundary he owns"* while the quoted words carry only the depiction requirement.
**Rationale:** this is the distinction **BLOCK-D** was fought over and won at v0.2 — an inference laundered as a ruling. The reading here is sound and the outcome is right; only the attribution boundary slipped.
**Discharge:** one line at KP-12 separating what Matt said from what was inferred, naming KP-14 as the ratification. Costs nothing.

## WARN-5 · § F.2a's headline sentence, read literally, is **false of the oracle**

*"The word `round` must not appear anywhere on the threat path."* The **Python** threat path uses `int(round(…))` at all four LIVE sites — the table directly beneath says so. The disambiguating clause (*"a source scan of **the built runtime**"*) sits sixteen lines later. A builder or grader scanning `threat.py` against the headline reds a correct oracle.
**Discharge:** insert *"the port's"* into the headline. One word.

## INFO

1. **Register v0.1's Companion line still names prereg v1.1** — lineage only; folds into the v0.2 re-pin.
2. **The skeleton emits 9 divergence rows against the register's 23** (`TRANSCRIPT.md:72`, `divergence rows=9 | register=15b6107561d8`). Expected at skeleton stage; § F's *mismatch → COVERAGE FAIL at P-1* is the right catch and **will fire at T-0** unless the emitter is filled. Named so it is not met as a surprise.
3. **L1 extends the standing push pattern to a third repo (`reincarnated-godot`) and is recorded only in the charter.** `CLAUDE.md`'s own rule is that a posture is recorded where the posture lives, not only where it was received. Low consequence; named because that file asks for it explicitly.

---

## WHAT I VERIFIED AND WHAT HELD

**Every check below was run, not assumed.** Discipline #11.

**Pins, by re-hash.** widths `6709cfe6f742…aade9` ✓ exact · lifted rows `e011742935f1…1af96` ✓ exact (`e0117429…`) · **sealed cells hash-verified and never opened, K-7 held** — `ad61ad2a8c799d6e` / 123,564 B · `20b05cb4ef3bd888` / 2,125,271 B · `7a992c81ca6e56e5` / 403,084 B, **all three matching the census § 3b table on digest *and* byte count.** Working tree clean for all three notes, so on-disk == committed. The two failures are BLOCK-2 / WARN-1.

**Change table complete against the ledger.** KP-13(1) → row 1 · KP-13(2) → rows 2, 3, 4, 8 · KP-13(3) → row 5 · KP-15 → rows 6, 7. KP-5/7/11 consequences are v1.0→v1.1 lineage and correctly not re-tabled (v1.1's own § A carries them). Counts reconcile: **22 carried + 1 added = 23 EXACT**; **6 + 4 + 0 + 4 = 14 BAND**.

**Bands re-derived independently from the sealed per-salt spreads** (`t(0.975, df=4) · s · √(2/5) = 1.755978 · s`):

| row | my derivation | published | |
|---|---|---|---|
| `TA-B-09` | mean 0.1153946 · s 0.0058625 · hw 0.0102942 → **[0.1051004, 0.1256888]** | [0.105100, 0.125689] | ✓ |
| `TA-B-03` | mean 0.8574626 · s 0.0138547 · hw 0.0243288 → **[0.8331338, 0.8817914]** | [0.8331, 0.8818] | ✓ |
| `TA-B-13` | mean 42.2621766 · s 0.6387470 · hw 1.1216243 → [41.1405523, **43.3838009**] | oracle's own max **43.4048024 lies above it** | ✓ removal correct |

`TA-B-09` at `s = 0.005863` is genuinely **less than half** `TA-B-03`'s 0.013855 — the power-table displacement is real, not rhetorical. `TA-B-13`'s two stated reasons both hold on the numbers: an extreme is not a mean, and 4 of 5 salts return the identical structural `41.97652009526441`.

**The complement claim is exact.** `23/106 = 0.2169811 = 1 − 0.7830189` on `D` ✓; `23/107 = 0.2149533` on `D + PRE_FIGHT` ✓. The 0.215-vs-0.217 tell resolves **entirely** to a denominator difference, as claimed — and it located a real mismatch in the census quote rather than being explained away.

**The four rounding sites exist and are the built-in `round`.** `threat.py:1402` `max(1, int(round(per / mult * self.ticks_per_s)))` · `:1522` `max(1, int(round(s.delay_s * self.ticks_per_s)))` · `:1555` `tick + max(1, int(round(cd * self.ticks_per_s)))` · `:1867` `tick + max(1, int(round(r.dot_duration_s * self.ticks_per_s)))`. `threat.py` imports `csv, hashlib, math, random, dataclasses, enum, functools, pathlib, typing` — **no `numpy`, no `decimal`** ✓. `deferred_arrival.py:330` `int(math.ceil(raw))`, with `:329`'s `round` gated behind `QuantLimb.ROUND` ✓. **Banker's is the correct assertion.**

**`TA-X-24`'s antecedent is the DRIVER of record — this is the row I was told to BLOCK if it were a default, and it is not.** `run.py:696` `phase_model: "th.PhaseModel" = th.PhaseModel.HASH` and `threat.py:1246` `phase_model: "PhaseModel" = PhaseModel.HASH` are the **defaults**; the v3.2 lifted `V0` rowset carries the string **`PhaseModel.ENGAGE`**; and `threat.py:1419-1420` says it in the module's own words — *"the run brackets them (`PhaseModel.HASH` vs `PhaseModel.SPAWN`) and takes the zero-parameter reading (`PhaseModel.ENGAGE`) as the limb of record."* Correctly derived, correctly raised as § H OQ-1 for the conductor to strike. **Keep it** — it is one deterministic assertion against the one trap no band and no digest can see.

**The scatter discriminator is a genuine three-way separator.** At `u₁ = u₂ = 0.5`: polar `ρ = 8.0·u₂ = 4.0`, `θ = π` → **`(−4.0, 0.0)`** ✓ · uniform-in-area `ρ = 8.0·√0.5 = 5.656854` → **`(−5.6569, 0.0)`** ✓ · box `(8(2u₁−1), 8(2u₂−1))` → **`(0.0, 0.0)`** ✓. Box reach `8√2 = 11.313708` ✓. Box draws exceeding 8.0 m = `1 − π/4 = 0.214602` = **21.5 %** ✓. `TA-X-10` margin `43.758085 − 43.404802 = 0.353283` = **0.807 %** ✓.

**Inertness arm pairing is right, including the non-obvious one.** `TA-X-03` `M-POL-2-NULL ≡ M0`; `TA-X-04` `W1-NULL ≡ **M-POL-2**`, not M0 — correct, because each arm is a single-fold delta from *its own* base, so nulling a W1 arm returns to M-POL-2. The prereg flags it with a ⚑ rather than leaving it to be discovered.

**Conservation is decidable and its trap is named.** Seven terms, `1e-6`; gamora independently found the **live driver assert-wall that recomputes with six**, omitting `counterplay_absorbed` — *"a port that emits six terms and passes a six-term check has passed something that is not the identity."* That is the run catching its own instrument, which is the behaviour these gates exist to produce.

**P-2 is decidable and honestly bounded** — § B.3 declares what a null-fold probe does *not* cover (site census, board roll, lifted-vs-chosen assignment) rather than letting it imply more than it proves.

**§ E "outside reach" is honest and complete** against KP-8's five traps (V5-GUARD-2, V9-DEAD-2, V17, V4-LAW-1, V18+V19), the board roll, and V17's drawn-radius half (R2D-5 owns it, and the report is required to say so). It also volunteers the over-read limit on `TA-X-11` — ⚑ *"a port with no wall at all also scores zero"* — **which is the finding I would otherwise have written myself.** Declaring the board roll open rather than minting `TA-X-23` against `waves.json` is the correct call under `L-49`; inventing it would have indicted the port for the oracle's own behaviour.

**The attribution procedure is runnable, not judgment.** § E.2 Steps 0–4 each name a test with an OFF-state, ordered cheapest-falsifier-first; Step 2 branches mechanically (T-A red → PORT · green → MODEL GAP · absent → `UNATTRIBUTABLE-PENDING`); the default is **never PORT**; the tie-break forbids narrative plausibility. A grader can execute this. **Two-epoch rule buildable** — § F fires forward only, and EPOCH 0's zero recordings are **recorded** rather than left silent, which is the disposition-not-silence discipline applied to itself.

**Stale-value sweep — clean on five of seven.** Banner **×2.0**, potion **θ 0.49**, **u 0.1981**, cast rate **0.290**, **u 0.294**: every surviving occurrence sits in a historical *"v0 said"* column or an explicitly-flagged superseded block (charter S-7 on the geometry file's own `u`). The two that are **not** clean are **72** (BLOCK-1) and *"two known-bad limbs"* (WARN-2).

---

## ⚑ IS THE PREREG IMMUTABLE-AND-SOUND — MAY IT BE USED TO GRADE?

**IMMUTABLE: YES.** v1.0 (`5f2c27cf`) and v1.1 (`30111ac8`) are present and unedited; v1.2 supersedes forward with a complete, ledger-traceable change table; **no graded run exists against any version**, so v1.2 and any v1.3 are legal under WARN-16. The D4 *committed-alone* discipline held at every version.

**SOUND ON CONTENT: YES.** Every `EXACT` row I sampled is decidable against a driver-of-record antecedent; the three bands I re-derived reproduce to the published digit; the traps are scoped honestly, including the two the run cannot see.

**USABLE TO GRADE: NOT YET.** **Precondition P-1 cannot go green.** The prereg requires `89/89`; the mechanical gate that must emit it holds `const CHARTER_DENOMINATOR := 72` and prints `COVERAGE RED … (charter pins 72)`, the charter's own § 4.3 demands the counts sum to 72, and the prereg's sha-pinned *governing* companion states the rule as `72 / 72`. **T-A does not run until P-1 is green** — by the prereg's own § B.2 and the charter's own § 4.3.

**Discharge both BLOCKs and the seal follows.** Nothing here requires Matt, no ruling is reopened, no row changes, and no number moves: KP-9 and KP-7(ii) already decided everything at issue. **What is owed is propagation, not decision.** Re-present the four sha diffs and I will seal same-session.

**One line for the conductor, because it is the thing worth keeping:** *this run's instruments keep catching this run's instruments* — V0 caught two charter errors within one wave, gamora's complement tell caught a denominator mismatch, drax's refusal-to-close caught the denominator itself, and § E volunteered the limit on its own strongest wall row. **Both BLOCKs above are the same shape one level up: a ruling that was made correctly and then did not travel.** The gates are working. The postal service is what failed.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (`c44d773d7294`) — § 3 `:49`, § 4.3 `:57`, § 4.4 `:59`, L4 `:89`, KP-9 `:119`, KP-12 `:122`, KP-13 `:123`, KP-15 `:125`, § 9 `:138`
- `…/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.2.md` (`72204f7a`) — `:8` galadriel pin, § A `:19-26`, § B.2 `:46`, § E `:100-114`, § F.2 `:130-153`, § F.2a `:157-173`, § G `:216`
- `…/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.1.md` (`30111ac8`) · `…-ta-prereg.md` v1.0 (`5f2c27cf`) — lineage, unedited, verified present
- `…/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-divergence-register-v0.1.md` (`540fd4b4`) — `:7` source pins, § E.2 `:135-146`, § F `:154`
- `…/agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` (`a2150122` · `b1210565` · `5cd34a75`; sha256 `6709cfe6…` ✓) — § E-3 `:75-78`, B-3 `:177`, A1 complement `:316-342`, Add. 2 B1/B2/B3
- `…/agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` — pinned `0411e6b8…` = `10a85641`; **current `8186202c…` = `b3f175ff`**, σ = 48 ms at `:417`
- `…/agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values.json` (`a8b85331…`) · `…-w1-tb-release-labels.json` (`15dace60…`) — **consumed, pinned nowhere**
- `…/agentic_orchestration/gamora/notes/2026-09-20-kc2-play-p0a-traceability-census.md` `:225-227` — sealed-cell digests + byte counts
- `/Users/admin/Games/reincarnated-godot/kc2_runtime/loader/kc2rt_coverage.gd` `:48`, `:222-230` · `kc2_runtime/README.md` `:78-83` · `kc2_runtime/TRANSCRIPT.md` `:52`, `:72`, `:123`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kc2/threat.py` `:1169`, `:1246`, `:1402`, `:1408-1424`, `:1522`, `:1555`, `:1867` · `…/kc2/run.py` `:684-696` · `…/kc2/deferred_arrival.py` `:13-17`, `:327-330`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-lifted-rows-KC2PLAY-W1-v3p2-full-20260920_163932.json` (sha256 `e0117429…` ✓)
- Sealed cells (hash-verified, never opened, K-7): `…/output/kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` · `…-mech-20260816_124031.json` · `…-w1walls-20260825_220058.json`
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` — swept for KC2-PLAY contradictions; **none found.** No committed-truth conflict; the charter's three declared live contradictions (stale `runtime_containment`, the (c-2) mitigation claim, the geometry file's `u`) are all dispositioned — (c-2) **RESOLVED** at KP-7.

*Filed by jack-ryan, 2026-09-20, DESIGN-MODE Wave-1 pre-read, Run KC2-PLAY. Read-only but for this file. No production code, no push.*

---

# § RE-SEAL — 2026-09-20, same session

**Reviewer:** jack-ryan · **Verdict:** ⚑ **SEAL-WITH-WARNS**
**Discharge reviewed:** charter `9b7a8e08` (KP-16) · gamora Addendum 3 `16d1b6a7` · godot `49006be` · register **v0.2** `a987334b` + **v0.2.1** `e0664fb9` · prereg **v1.3** `66d2fc89` · ledger **KP-16…KP-20**
**Counts:** **2 BLOCK DISCHARGED · 5 WARN DISCHARGED · 3 INFO** (2 closed, 1 carried) · **new: 1 WARN · 2 INFO** · **0 BLOCK outstanding**

## ⚑ THE PREREG IS IMMUTABLE-AND-SOUND. IT MAY NOW BE USED TO GRADE.

**v1.3 (`66d2fc89`) is the grading instrument.** v1.2/v1.1/v1.0 present and unedited; supersession forward with a complete change table; **no graded run exists against any version**, so v1.3 is legal under WARN-16. **P-1 can now go green** — 89/89 is the number in the prereg, in the charter's gate clause, in the charter's cap clause, in the governing width file's Addendum 3, and in the executable constant. The single threshold that a cap needs, it now has.

## BLOCK-1 — **DISCHARGED.** Re-verified on disk, hostilely

| surface | now reads | |
|---|---|---|
| charter § 4.3 `:57` | `All ~~72~~ **89** … counts sum to ~~72~~ **89** … value @ coverage **k/89**` | ✓ |
| charter § 4.4 `:59` | ⚑ `coverage < **89/89**-mapped` — **the two-thresholds-for-one-cap defect is closed** | ✓ |
| charter § 3 F1 `:49` · § 9 BLOCK-B `:143` | `~~72~~ **89**` | ✓ |
| `kc2rt_coverage.gd:69` | `const CHARTER_DENOMINATOR := 89` | ✓ |
| `TRANSCRIPT.md:81` | ⚑ `COVERAGE RED \| mapped 0/89 (**charter pins 89**) \| unmapped 89 \| **blockers 1**` — the denominator blocker is gone; the gate is RED **by design** at 0/89 (nothing mapped yet), which is the correct pre-W3 state | ✓ |
| widths Addendum 3 | § E-3 `72/72 → 89/89`; **89 ids re-counted from her own tables: M 23 · D 19 · P 7 · K 26 · W 14** | ✓ |

⚑ **gamora's corrigendum is the part worth keeping.** She did not merely accept 89 — she went back and found *why* 72 does not enumerate: it is the class-share headline taken **after collapsing ~a dozen genuinely split rows** (`M3`, `M4b`, `D7`, `D11`, `K6`, `K8`, `K15`, `K16`, `K17`, `K25`, `W9`, `D13/D14`) to a primary class, **and the note never records which id collapses into which.** *"The 72 is mine and it does not enumerate."* That converts KP-9 from a ruling-by-authority into a ruling-by-arithmetic, and it names the twelve ids so the claim is checkable. **drax escalated it, KP-9 ruled it, gamora proved it.** That is the gate working end to end.

**Runtime sweep:** every remaining `72` in `kc2rt_coverage.gd` / `README.md` / `TRANSCRIPT.md` is **past-tense lineage** (*"demanded"*, *"pinned"*, *"retired at KP-9"*) or a line-number reference. **No live-tense coverage `72` survives** in prereg v1.3, register v0.2/v0.2.1, `kc2rt_coverage.gd`, or charter § 4. In v1.3 the digit-string `72` occurs only as Discipline `#72` and inside `47.072`.

## BLOCK-2 + WARN-1 — **DISCHARGED.** All four pins re-derived by me, independently

| pin | my `shasum -a 256` | matches | |
|---|---|---|---|
| widths (governing) | `1c971da9d5f1e1cb3385965e44c38a6a32d1d3f24fdd260757bea748b0d0a121` | P-a, prereg v1.3 + register v0.2/v0.2.1 | ✓ |
| galadriel note | `8186202cc0c78ae9ef428c57164fac35bd1adb0e14ec5310c395783361653158` | P-b — **the `b3f175ff` state, the one DIV-04 and DIV-15 actually cite** | ✓ |
| `…-expected-values.json` | `a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b` | P-c — **newly pinned** | ✓ |
| `…-release-labels.json` | `15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a` | P-d — **newly pinned** | ✓ |

⚑ **Deliberately NOT the pre-read's `6709cfe6…`, and the documents say why.** The register's P-a note reads: *"The pre-read named `6709cfe6…`; Addendum 3 has landed since, and pinning a superseded state is the very defect being closed — so this pins CURRENT and says so."* **That is the correct reading of my own finding against me** — a re-pin to the digest I quoted would have re-committed the defect in the act of discharging it. Taken, and right.

**KP-20's standing rule (i) is the generalisation I would have proposed:** *a document that pins anything re-derives every pin it carries at each version — never carries one forward.* The defect was a **carry-forward, twice in one wave**; the rule closes the mechanism, not the instance.

## WARN-3 — **DISCHARGED, and I reproduced the conformance test**

*"Whitespace collapsed"* is gone, replaced by an eight-clause rule whose **clause 5** is exactly the separation I asked for: *"String values are emitted VERBATIM … NO whitespace collapse, NO trimming, NO case folding, and NO Unicode normalisation is applied at hash time. Normalisation is an **authoring** rule … never a **hashing** rule."*

⚑ **I recomputed the worked example from its stated input, independently:**

```
bytes   : 497
sha256  : bf648e51d14fc9313c4fce7774c5567628e1d3aca48d68c6a29d0d9225fe165e
prefix  : [{"authority":"R-KP-0c","class":"DIVERGENCE","direction":"tighter: shorter time-to-contact","id":"DIV-01","ora…
```

**Byte length, digest and prefix all reproduce exactly.** An under-specified predicate has become a **mechanically falsifiable conformance test** — *"an implementation that does not reproduce `bf648e51…` from the input above is non-conforming."* That is a better discharge than the finding asked for.

## WARN-5 · WARN-4 · WARN-2 — **DISCHARGED**

- **W5** — § F.2a `:168-169`: *"No bare `round(` may appear on **THE PORT'S** threat path. The oracle's Python threat path **DOES** use `int(round(…))` at all four LIVE sites — and that is the point, not a contradiction."* The trap is now stated rather than merely avoided. ✓
- **W4** — charter KP-12 `:122` now separates **what Matt SAID** (quoted) from **what the conductor INFERRED**, cites this finding, and names **KP-14 as the ratification**. The BLOCK-D boundary is restored. ✓
- **W2** — charter L4 `:89`: `~~two oracle limbs are known-bad~~` **ONE — LifeMonitor `POLL_AT_SLOT`**, citing KP-7(ii). ✓
- **INFO-1** closed (register v0.2.1 companions prereg v1.3). **INFO-2** closed as a *scheduled* event (register v0.2 `:125`, now 9 vs 25, firing at T-0). **INFO-3** carried — see below.

## KP-19 / ART-LEADS-THE-BOUNDARY — reviewed, and **P-1 / T-A are untouched**

**Matt's G1–G4 are recorded verbatim at KP-19 and not extended.** G4 *"Potion Key = 1"*, G2/G3 *"agreed on G2 and G3"*, and G1's full sentence including *"I would prefer to fit it around the art rather than have the art fit the edges."* KP-17 records the defaults offered — and records that **G4 had no default** (*"the potion stays unbound until Matt names the key"*), which is the right call and the right thing to have written down.

**`DIV-16` is honestly stated — conspicuously so.** It names itself *"the largest single unquantified term in `PLAY`"*, classes the T-B expectation as **NAMED CONFOUND, DIRECTION UNBOUNDED**, says plainly that *"nobody can bound that before the painting exists"*, flags the compounding with `DIV-09`'s 1.32× window, and requires the mask's **area + max chord in the telemetry header beside every arena-sensitive row or the row is uninterpretable.** It also keeps `DIV-01` rather than collapsing it, so the inverted method stays on the record (OQ-3). ⚑ **This is a row that argues against its own convenience, which is what a register is for.**

**T-A is untouched, verified three ways:** `DIV-16`'s ORACLE cell reads *"unchanged and untouched — CIRCLE `R_wall = 43.758085029822276 m` … **T-A grades this config and no other** (`TA-X-10`, `TA-X-11`)"*; no `DIV` row is graded by T-A **by construction** (v0.2.1 header); and **P-1 counts census row ids**, which no boundary ruling moves. `TA-X-10`/`TA-X-11` still assert against the sealed `[W1W]` circle. **The seal I am giving is not weakened by KP-19.**

**The sha-registered-painting rule is honestly stated** — KP-20(ii): *"there is no frozen edge left to catch drift, so the sha is the edge."* Correct diagnosis of what G1 gave up and what replaces it.

---

## RESIDUAL — 1 WARN, 2 INFO. **None blocks the seal.**

**WARN-6 (new) · The widths file's § E-3 still reads `72 / 72` at the point a reader looks it up.** `…ta-band-widths.md:75-78` is unchanged: *"Coverage — **72 / 72**, gate before grade … a band reported without `@ coverage k/72` beside it is not a T-A result."* Addendum 3 states it *"supersedes its figure **in place**"* — but it is filed at `:600`, **~525 lines below**, and **§ E-3 carries no marker.** The prereg pins this file *by sha* and calls it **governing**; a grader who looks the coverage rule up where it is stated finds 72 and no pointer.
**Not blocking:** the correction is unambiguous, lives inside the pinned artifact, and both executable surfaces (prereg § B.2, `kc2rt_coverage.gd:69`) read 89.
**Discharge (gamora, one line):** a strike-through pointer at § E-3 — ⚑ `SUPERSEDED BY ADDENDUM 3 → 89 / 89`. **This does not violate append-only:** the charter discharged four of its own stale numbers by exactly this method (`~~72~~ **89**`, `~~two~~ **ONE**`) — **annotation in place is not rewriting**, and it is what "supersedes in place" has to mean to be true.

**INFO-4 (new) · Prereg v1.3's OQ-2 is stale by one minute.** It reads *"`kc2rt_coverage.gd:48` **still** holds `CHARTER_DENOMINATOR := 72` and the transcript prints `(charter pins 72)`"* — drax landed `:= 89` at `49006be` (17:15:57), **33 seconds before v1.3 committed** (17:16:30). Its recommendation (rename to `CENSUS_DENOMINATOR`, retire the branch) was **not** taken: drax kept the name at 89 and **re-aimed the branch to guard census drift** (`:49`, `:255-270`). That is a seam-owner's call on his own file and a defensible one — the branch still catches a real class of drift. Harmless; named so OQ-2 is not answered a second time against a premise that has already moved.

**INFO-3 (carried) · L1's push-posture extension to `reincarnated-godot` is still recorded only in the charter.** `49006be` was pushed under it (KP-20). `CLAUDE.md`'s own rule is that a posture lives where the posture is recorded. Unchanged from the pre-read; for KR, not for this run.

---

## WHAT I RE-RAN FOR THIS SEAL

All four pins re-hashed from disk (not read from any document) · charter / prereg v1.3 / register v0.2 + v0.2.1 / widths / `kc2rt_coverage.gd` / `README.md` / `TRANSCRIPT.md` swept for live-tense `72` · the transcript's gate line read literally · the canonicalisation worked example **recomputed from its stated input to 497 bytes and `bf648e51…`** · ledger KP-16…KP-20 read for Matt-verbatim fidelity and for any commitment boundary ruled without him (**none found** — KP-17/KP-19 are Matt's words; KP-18's figure-height ruling is a presentation choice inside the seam, registered as `DIV-17` and routed to T-C).

**Both BLOCKs were, as filed, rulings that did not travel. They have now travelled — into four documents and one executable constant — and the two standing rules adopted at KP-20 close the mechanism rather than the instance.** The discharge also corrected my own finding where it had gone stale, which is the behaviour I would rather see than compliance.

**⚑ SEAL GRANTED. Wave 1 is closed. T-A may be graded against prereg v1.3 once P-1 is green (89/89 mapped) and P-2 passes.** WARN-6 rides to W2; it is one line and it is not mine to write.

*Re-seal filed by jack-ryan, 2026-09-20, Run KC2-PLAY. Read-only but for this file. No production code, no push.*
