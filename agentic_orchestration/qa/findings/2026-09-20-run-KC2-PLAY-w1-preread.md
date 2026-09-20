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
