# Finding — 2026-09-16 — Run C-5 E1 ruling (R-C5-64), Gate 2

**Reviewer:** jack-ryan (DEV-MODE)
**Severity:** BLOCK (narrowly scoped — see § Scope of the BLOCK)
**Target:** `astra_test_01/burst/runs/C-5/ledger.json` ruling `R-C5-64`, ts 2026-09-16T07:00:33, class `conductor`, `veto_open: true`
**Developer / conductor:** gandalf (RUN-CONDUCTOR, autonomous stretch under Matt R-C5-36)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code / evidence-before-claim), #2 (smoke-gate), #4 (decisions-log as truth), #5 (severity matters)
**Disciplines cited:** #64 FRAME FORM · #73 (the record must carry the state) · #75 cl. 6 (a remedy does not inherit its predecessor's instrument)

---

## Scope of the BLOCK

**The decision is supported. The ruling as stated is not.**

ARM B over ARM A is carried by the evidence at **3–0 on three valid pairs**, with the control passed. What the ledger records — *"by 4–0 on four order-randomised in-scene pairs"* — is contradicted by the board pixels: **one of the four scored boards is not a pair.** Its two rows were captured at different locations in the level.

The BLOCK is on **propagating the "4–0 on four pairs" formulation** into the decisions-log, `vfx-workflow.md`, or any Matt-facing packet. It is **not** a block on route B, and it does not require re-running E1.

**Path forward (one of two, conductor's choice):**
- (a) Amend `R-C5-64` in place is not available — the ledger is append-only. File a **correcting ruling** that restates the result as *3–0 on three matched pairs, one board (pair 3) discarded as unmatched, control passed*; or
- (b) re-capture pair 3's arm-A row at pair 3's spot, rebuild board 2, and re-judge with a fresh instance — restoring a genuine 4-pair result.

Either way the comparability gate in § Action must land before the next JUDGE burst.

---

## What I found

**1. Board 2's two rows are not the same cast, the same spot, or the same framing.** Normalised cross-correlation of the pre-effect frame (`cast+2`) between the two rows, searched over ±90 px translation:

| board | key pair | key L / R | best NCC (rows to each other) | reading |
|---|---|---|---|---|
| 1 | 2 | A / B | **0.979** (dy 66, dx 2) | matched; 66 px camera pan between arms |
| 2 | 3 | A / B | **0.232** | **NOT MATCHED — different location** |
| 3 | 0 | A / A | **1.0000** (dy 0, dx 0) | control, byte-identical |
| 4 | 4 | B / A | **0.882** (dy 5, dx 8) | matched; small pan |
| 5 | 1 | A / B | **0.865** (dy −10, dx −19) | matched; small pan |

The same offset is recovered independently at panel 1 (`cast+2`) and panel 6 (`+40` residue) on every board, so these are static capture offsets, not measurement noise.

**The mechanism is identifiable.** Cross-correlating all eight scored rows against each other, board 2's **arm-A row matches board 5's arm-B row at NCC 0.885** — i.e. board 2's A row was sourced from **pair 1's spot**, not pair 3's. This is a row mis-assignment in board assembly, not a capture failure: the A capture exists, it is just the wrong one.

Visual confirmation, board 2 panel 1: the top row shows a shield-dummy and a distinct dummy arrangement; the bottom row shows a scarecrow-dummy beside a burning stump. Different props, different layout, different caster position.

**2. The judge was told a premise the stimulus does not satisfy.** The `E1-judge-03` brief states: *"Each board shows the SAME cast twice, LEFT and RIGHT… The two sides differ only in how the projectile's travel is drawn."* On board 2 that is materially false, and on boards 1/4/5 it is imprecise — the arms also differ by a camera pan of 5–66 px. The judge's board-4 note (*"foliage reduces certainty"*, lowest confidence 0.87) shows it reading scene context that was not held constant.

**3. `key.json`'s control entry does not describe the bytes.** The key records board 3 as `pair 0, LEFT: "A", RIGHT: "A"`. The two rows of board 3 are byte-identical to each other (verified: SHA-256 of the row band, `29de1346c845c903…`, dy/dx 0, NCC 1.0000) — **and byte-identical to board 2's RIGHT row, which the same key labels arm B.** The control was cloned from an arm-**B** capture and recorded as A/A.

This is a self-contradiction in the only document that makes the blind test auditable: exactly one of {board 2 RIGHT = B, board 3 = A/A} is wrong. **The judge's own data resolves it.** `coherent_with_burst` is `false` for the A side on all four scored boards and `true` for every B instance including both control rows — a perfectly consistent partition **only** if the control rows are B. Had the control truly been A/A, the judge would have had to rate A coherent on the control and incoherent on all four tests. So the control is B/B and the key's arm label for board 3 is the defective field. The 4-vs-3 tally is unaffected by this item.

**4. The claims that *are* clean, verified field by field.** Recomputed from `key.json` × `judgements.json`:

- **Tally** — board 1 → B, board 2 → B, board 4 → B, board 5 → B; board 3 → SAME. Arithmetic is right; the defect is in the stimulus, not the count.
- **Side-bias is excluded.** B sat on RIGHT for boards 1/2/5 and on LEFT for board 4, and the judge followed the arm across the flip. Neither a constant-LEFT nor a constant-RIGHT bias explains the result. *(Assignment was 3:1 by side, not 2:2 — the single flip is what carries the argument, and it is the board with the lowest confidence.)*
- **"Both arms read as painted"** — `reads_as_painted` is `true` for all ten rows, unanimous. **Supported.**
- **"A rated INCOHERENT with its burst on every board"** — `coherent_with_burst` false for the A side on 4/4 scored boards, 3/3 on the valid ones. **Supported.**
- **"Control passed (SAME, conf 1.0)"** — verified byte-identical, judge returned `SAME` at confidence 1.0. **Supported** (but see § 6 on the word *passed*).
- **"judge confidences 0.87–0.94"** — 0.87, 0.88, 0.90, 0.94. **Exact.**
- **Blinding** — `E1-judge-03` ran as a fresh `codex exec` burst (`gpt-6-astra`, codex-cli 0.153.4, exit 0, `image_calls` 0, no audit violations); the brief discloses no arm identity; `key.json` was conductor-held (M-C5-PACK-V27). **Sound.** No judge saw the same boards twice — judge-01 got v27, judge-02 v28, judge-03 v29 — so there is no carry-over between attempts.

**5. `417/330-px key widths against the 260-px streak` is unprovenanced.** These three scalars appear **only inside `R-C5-64` itself** — nowhere else in the ledger, notes, or any CHECK artifact. They are the ruling's stated causal mechanism for A's failure, quoted with no operator, no instrument and no capture geometry.

**6. Two of the five HALT triggers are stated in vocabulary the run now uses in the opposite sense.**

- **"a JUDGE passing its control twice"** (R-C5-36; `mechanical-process.md § 1.6`). `JUDGE_RUBRIC.md § 6` defines a control as a **known-bad** sample the judge must **fail**, and *"a judge that passes its control VOIDS the batch"* — there, *passing the control* is the judge's **failure**. `R-C5-64` records *"control passed"* to mean the judge answered **correctly**. The HALT trigger cannot be evaluated from ledger text while both polarities are in use.
- **"two VOIDs in a row"** (R-C5-36; `§ 1.6`). `mechanical-process.md § 2` defines VOID as wrapper exit 2. `E1-judge-01` and `E1-judge-02` both recorded **exit 0, zero audit violations** — no wrapper VOID. Both were **conductor-declared** voids, consecutively, on the same JUDGE of the same experiment. Under the wrapper sense the trigger did not fire; under a plain reading of Matt's authorization text it did. The run proceeded to a third attempt with no HALT packet and **no ledger entry recording why the condition was judged not to apply.**

**7. The control substituted is not the control the brief cites — and the substitution is defensible.** The `E1-judge-03` brief cites *"mechanical-process § 1 invariant 2: a known-bad control in every batch."* Invariant 2 actually says *"controls in every batch"* — satisfied. *Known-bad* comes from `JUDGE_RUBRIC.md § 6` and means a defect-injection. What ran is a **null control** (identical pair; correct answer "SAME"). For an A/B *preference* test the null control is the better-matched instrument — the dominant failure mode is a judge confabulating a winner, and that is precisely what it tests, at confidence 1.0. The defect is the **citation**, not the choice. Note what the null control cannot do: it cannot detect a judge insensitive to a real defect, and it was cloned from the **favoured** arm.

**8. The void reasoning on both earlier attempts holds — with one correction of attribution.**

- **`E1-judge-01` VOID (R-C5-54, "boards not comparable")** — holds, and is corroborated here. See § Rationale.
- **`E1-judge-02` VOID ("schema-literal receipt with no judgements")** — the outcome is confirmed byte-for-byte: `E1-judge-02/receipt.json` carries `files: []`, `images: []`, and a `self_report` containing only `obeyed_invariants` and one concern; there is **no** `judgements` key. But **the judge did not fail — the brief did.** The brief instructed it to return the array *"under `self_report.judgements`"* while the receipt schema has no such field, and the judge's single recorded concern is *"Used images: [] to comply with the receipt schema."* It obeyed the schema it was given over the prose it was given. `E1-judge-03` fixed this correctly by making the array a **file deliverable** — the right remedy. The ledger phrasing attributes to the judge a defect that belongs to brief design; worth one line of correction so the lane does not learn the wrong lesson.

**9. Pair count has eroded twice, and only the first erosion is ledgered.** Charter § 4 E1 pre-registered **five** order-randomised pairs. **Four** were captured (deviation ledgered, M-C5-PACK-V27). **Three** are valid (this finding, not previously recorded). The ruling therefore rests on 3 of the 5 pre-registered pairs.

---

## Rationale

**On the BLOCK (§ 1–2).** Review principle #1: a claim carries the evidence it names. `R-C5-64` names *"four order-randomised in-scene pairs"* and the pixels show three. The conclusion survives the correction — 3–0 with a passed control is unanimous, V13 (3–2 = inconclusive) is a **split** rule and 3–0 is not a split — but the ruling is headed for `vfx-workflow.md` as canon-on-Matt's-word and into a decisions-log commitment, and a number that travels into canon must be the number the evidence supports. Discipline #73: the record must carry the state.

**This is the second time E1's boards were not comparable, by a second mechanism, and the first remedy could not have caught it.** `R-C5-54` voided `E1-judge-01` for exactly this class — *"boards not comparable"* — and the remedy fixed the **peak detector** (*"detector fixed to search after frame 30"*). The detector was the instrument that failed the first time; **row sourcing was never instrumented at all.** Discipline #75 cl. 6 — *a remedy does not inherit its predecessor's instrument* — is squarely on point: the class was named "boards not comparable" and the fix was scoped to the one axis that had just embarrassed it. A rule that names axes stays one axis behind.

The corollary is that **comparability was never converted into a check.** `R-C5-54` is a conductor judgement recorded in prose; nothing in the lane asserts it mechanically. The per-board NCC in § 1 takes seconds to compute, is deterministic, and would have caught **both** failures — the detector latch in v27 and the row mis-assignment in v29. That is the remedy that terminates the sequence.

**On § 5.** Discipline **#64 FRAME FORM** (adopted 2026-08-24): *a comparison-load-bearing scalar carries its operator, scene and capture geometry at the point of quotation*; *a bar restated without its operator is not the bar*. `417/330` against `260` is the ruling's entire causal account of why A failed — as comparison-load-bearing as a number gets. The verdict does not rest on it (the 3–0 does), so this is WARN-class, and the remedy is small: state the frame, or mark the figures as conductor observation rather than measurement.

**On § 6.** Both items are the failure family CLAUDE.md's own git-instrument amendments were written about: **an instrument returning cleanly after it stopped answering the question.** A HALT trigger whose key term carries two opposite senses cannot be evaluated by reading the ledger — and this is an autonomous stretch, with Matt away, where the HALT conditions are the only thing standing between the run and an unreviewed commitment. The VOID-sense question is genuinely arguable in both directions and is **Matt's to settle** — he is the HALT recipient. What is not arguable is that the run passed a Matt-facing trigger without recording the reasoning. Per the conflict-rule corollary in CLAUDE.md, *an escalation overtaken by events still requires a disposition; silence is not one* — the same holds for a HALT condition judged not to apply.

**On what I am NOT finding.** The judge is not impeached. Its discriminating attribute was consistent across all four boards and is a property of the drawing, not the background — *"long thin ribbon"*, *"oversized broad body"*, *"balloons into a broad, heavy-contoured emblem"* against *"compact tapered tongues"*, *"preserves… a readable bright core"*. It declined to invent a preference on the control at confidence 1.0, and it followed the arm across the one side-flip. Discarding board 2 entirely leaves three matched pairs, one named reason, and no dissent. **Route B is the right call and the conductor reached it honestly.**

---

## Verdict per question

**(1) Does the evidence support the ruling as stated?** **Partly — BLOCK on "as stated".** *Both arms read as painted* (unanimous, 10/10) and *A incoherent with its burst* (4/4 scored, 3/3 valid) are **supported**. The **4–0 on four pairs is not**: board 2 is not a pair. Restated as **3–0 on three matched pairs, control passed**, the ruling is supported.

**(2) Is the process sound?** **Blinding, instance separation and the control are sound; stimulus construction is not.** Separate ephemeral burst ✓ · arms undisclosed ✓ · key conductor-held ✓ · control genuinely byte-identical and correctly answered ✓ · side-bias excluded by the flip ✓. Against that: one board's rows mis-sourced (§ 1), the brief asserting a constancy the boards do not have (§ 2), `key.json` self-contradictory on the control's arm (§ 3), and no mechanical comparability gate between the board builder and the JUDGE burst.

**(3) Ruling on four rather than five — objection?** **No objection to ruling on fewer than five; the pre-registered rule is not threatened by unanimity.** V13 makes a **3–2 split** inconclusive; 4–0 and 3–0 are not splits, and the missing pair is non-load-bearing against a unanimous result with a passed control. Two things to record rather than object to: V13's band was authored for n=5, so at n=4 a **2–2 or 3–1** outcome would have had **no pre-registered disposition** — the deviation quietly removed the tie-breaker, and that is worth a line in the ledger for the next experiment that drops a cell. And the real erosion is not 5→4 but **5→3** (§ 9), which reached the ruling unrecorded.

---

## Action

- [ ] **gandalf (conductor) — BLOCK, before the E1 result reaches canon, the decisions-log as accepted, or a Matt packet:** file a correcting ruling restating E1 as **3–0 on three matched pairs (pairs 1, 2, 4), board 2 / pair 3 discarded as unmatched (arm-A row sourced from pair 1's spot, NCC 0.232 within board vs 0.885 across), control passed** — or re-capture and re-judge pair 3 per § Scope (b).
- [ ] **gandalf — BLOCK, before the next JUDGE burst fires:** add a mechanical comparability gate to board assembly — per board, NCC of the pre-effect frame between the two rows (matched pairs here run 0.87–0.98; the defect ran 0.23), plus an assertion that the control's two row bands are byte-identical, plus an assertion that each row's source capture path matches its keyed pair. Emit it as `checks.json` alongside the boards. This is the remedy `R-C5-54` did not have.
- [ ] **gandalf — WARN:** correct `key.json`'s board-3 arm label (control is B/B, cloned from board 2's arm-B capture) by ledger note; the file itself is under `astra_test_01/burst/` and I have not touched it.
- [ ] **gandalf — WARN (#64 FRAME FORM):** give `417 / 330 / 260 px` their operator, scene and capture geometry, or mark them conductor observation.
- [ ] **gandalf — INFO:** one line correcting the `E1-judge-02` attribution (brief defect, not judge defect — § 8); and the `E1-judge-03` brief's prose opens *"JUDGE BURST E1-judge-01"* while `task_id` is `E1-judge-03` (copy-paste artifact, no effect on the result).
- [ ] **Matt — ESCALATE (autonomous-stretch governance, not the E1 result):** (a) does **"two VOIDs in a row"** in R-C5-36 count **conductor-declared** voids, or only wrapper exit-2 voids? Under the plain reading the run should have HALTed before `E1-judge-03`; under the drafting reading it should not. (b) Ratify or amend the **"control passed"** vocabulary so the *"JUDGE passing its control twice"* trigger has one polarity. Both are yours because you are the HALT recipient.
- [ ] **Matt — ratify or amend** the decisions-log entry filed PROPOSED at `reincarnated-engine/design/decisions/decisions-log.md` (2026-09-16, C-5 commitment set). Note it carries **V4**, which charter § 10 reserved to you and which stands only as a conductor working ruling.

---

## References

Reviewed byte-for-byte:
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/ledger.json` — `R-C5-64`, `R-C5-54`, `R-C5-61`, `R-C5-62`, `R-C5-36`, `R-C5-25`; bursts `E1-judge-01/02/03`; milestones `M-C5-PACK-V27`, `M-C5-PACK-V28R1`, `M-C5-E1-OPEN`; notes `N-C5-judge-01-void`, `N-C5-judge-02-brief`, `N-C5-v28-probe-error`, `N-C5-disk-full`; `halts: []`
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/artifacts/E1-judge-boards-v29/board_1..5.png` (sha256 `ef6c22ce…`, `ef75cc79…`, `8e21a954…`, `96653123…`, `8b7bb28b…`) and `key.json` (sha256 `8c3b6a66…`)
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/artifacts/E1-judge-03/judgements.json` · `receipt.json`
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/artifacts/E1-judge-02/receipt.json`
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/briefs/C-5/E1-judge-03.task.json` · `E1-judge-02.task.json`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-15-vfx-run-C-5-charter.md` §§ 3, 4, 8, 9, 10
- `/Users/admin/Games/reincarnated-collaboration/canonical/reap-die-rise-game/painted-2d-pipeline/mechanical-process.md` §§ 1, 2
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/JUDGE_RUBRIC.md` § 6

Measurement method (reproducible, read-only): row bands `y 30:330` (LEFT) and `y 340:640` (RIGHT) isolated from the flat separator runs at `y 330–339`; panels `w/6 = 425 px`; greyscale zero-mean normalised cross-correlation searched over ±90 px translation, recomputed independently at panel 1 (`cast+2`) and panel 6 (`+40`). Control board returns NCC 1.0000 at zero offset, which validates the instrument. **Note on my own first instrument:** a naive mid-height split straddled the separator band and reported the control as non-identical; a raw mean-absolute-difference then read 89–96 % of pixels differing on every scored board, which suggested "different scenes" and was wrong — on high-frequency painted foliage a few pixels of offset saturates that metric. Both were corrected before any finding was drawn. Same family as the finding itself, and recorded rather than tidied away.

**Nothing under `astra_test_01/burst/` was modified.**
