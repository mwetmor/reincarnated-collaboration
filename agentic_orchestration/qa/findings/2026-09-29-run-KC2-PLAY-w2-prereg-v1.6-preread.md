# Finding — 2026-09-29 — Run KC2-PLAY SEAL LAP · W2 · prereg v1.6 PRE-READ (Gate-1 / DESIGN-MODE)

**Reviewer:** jack-ryan
**Severity:** **PASS-WITH-WARNS** — 4 WARN · 3 INFO · **0 BLOCK. W3 is not halted.**
**Target:** `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.6.md`
**File sha256 (derived this session, not retyped):** `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` — **matches the brief. Hash gate PASSED; no HALT.**
**Target commit:** collab `17daef900` (the file's own commit; session HEAD `ea574c3ad`)
**Developer:** gamora (simulation + spirit-guide seam), seat W2
**Substrate of record:** v3.4.2 · model pack `5cab7433…` (17) · reference pack `978f54ab…` (7)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code) · #2 (smoke-gate) · #4 (decisions-log / committed record as truth) · #5 (severity matters)
**Disciplines cited:** **#12** (semantic shift is not a bug fix) · **#73** (the state moved and the record did not follow) · **#75 cl. 6** (a remedy does not inherit its predecessor's instrument) · **#79 / Law 3** (no fitted constants) · **#80** (a row that cannot fail is not a test) · **#86** (does it run on the path?) · CLAUDE.md conflict-rule corollary (an escalation mooted rather than ruled)

---

## What I found

The document is the strongest prereg in this series. Every pin re-derived, both pack digests recomputed from member lists under the manifest's own law rather than read off it, D4 held (committed alone, zero code, before any graded run against v3.4.2 exists), and the author books three corrections **against himself** — including one he found while writing the very clause that warned about the defect class. I verified the load-bearing claims independently rather than reading them off the face: the file hash, the 29 EXACT / 19 DIAGNOSTIC counts (`TA-X-01…30` less the struck `TA-X-23` = 29 ✓; `TA-B-01…19` = 19 ✓), the sealed cell's `terminals` array (byte-exact `[156, 152, 151, 151, 156]`, all five `player_death` ✓), `Q83(b)`'s open status in the decision queue ✓, and the four `P-5` fold settings against KP-90 / KP-97 / KP-101 / KP-84-L1 ✓.

The four WARNs are not defects of derivation. **Three of them are the same shape: a state that moved and a carrier that did not follow (#73).** One is internal to the document — a reference point minted from a cell whose sibling figures the same document voids two sections earlier. Two are external — Matt's own decision carrier now understates the stakes of the question the seal depends on, and the ruling that defines the seal names a row count the instrument has since outgrown. Neither external item can be fixed by editing the prereg; both are the conductor's, on the ledger and the queue.

**On the author's three questions: carry `TA-X-06` as classed — correct. Ratify `TA-X-25`'s re-authoring — it is a substrate re-derivation, not a goalpost move. `TA-X-09` at 9 of 29 — honest scope, not a hole.** Reasoning in § Answers below.

---

## WARN-1 · `TA-B-01`'s oracle side reaches back two epochs, and § A.4 voided the widths from that same cell for exactly this reason

**Derived, not inferred.** The sealed cell `[M-POL2]` is `kc2-checkpoint-E-s09-cp150-mpol2-**20260825**_114420.json` — **2026-08-25**. The v3.3 monster-offense lift was authorized at Q82 on **2026-09-20**. The cell therefore predates v3.3 and belongs to **neither** epoch § C.7 names.

- **§ A.4** voids *every* band width because *"`P-a`'s widths are all derived from the sealed `M-POL-2` cell's per-salt values… New per-salt values ⇒ every width void."*
- **§ A.5** then reads `terminal_wave` out of **the same cell's per-salt array** and makes it `TA-B-01`'s oracle-side expectation at v1.6, and **§ F.5 cl. 7 makes a sentence built on it mandatory on the report face.**

Same cell, same per-salt grain, same board change — voided in one section, promoted to a mandatory reference point in the next. **§ C.7 says in terms: *"NO ROW, NO DIAGNOSTIC AND NO REPORT LINE MAY COMPARE ACROSS THEM."*** The mandatory sentence compares a pre-v3.3 soft-board oracle death (151–156, on a board where 338 records had no offense at all) against a v3.4.2 hard-board port survival (160).

**Two things keep this at WARN and not BLOCK.** `TA-B-01` is DIAGNOSTIC class V and gates nothing under F5 — it cannot move the verdict or the seal. And **the direction is conservative**: a harder board should kill the oracle *earlier*, so a fresh v3.4.2 oracle would likely terminate at or below 151–156, making the port's 160-clear worse than the printed sentence claims, never better.

**I also confirmed the ambiguity does not reach the verdict.** I walked all 29 EXACT rows: **not one requires an oracle-side execution.** Every EXACT row grades against the port itself (`TA-X-01`, `03`–`06`, `07`, `25`, `30(b)`), a pack constant (`09`, `10`, `16`–`18`, `26`, `27(d)`, `29`), an identity or structural zero (`08`, `11`–`15`, `19`–`22`, `24`), or a source-level structural claim (`28`). The cross-epoch exposure is confined to the diagnostic half.

- **Action (grader, at emission, no prereg edit):** print the array's provenance and epoch beside it — *"`[M-POL2]`, sealed 2026-08-25, pre-v3.3 substrate"* — so the mandatory sentence carries its own epoch. That satisfies § C.7's intent and strengthens the sentence rather than softening it.
- **Action (v1.7):** § C.7 names two epochs and the sealed cells belong to neither. Extend the law to name the sealed-cell epoch explicitly.

## WARN-2 · Q87 was ruled over **26** EXACT rows; the instrument now carries **29**

**KP-83, verbatim:** *"**Q87** REFERENT-v1 seals on all **26** EXACT rows green under v1.6 + coverage 89/89 + T-B reported DIAGNOSTIC + Matt's T-C yes."* The prereg restates this as *"ALL EXACT rows green"* and then adds `TA-X-28`, `TA-X-29`, `TA-X-30`.

The generalisation from a number to a quantifier is almost certainly Matt's intent — 26 was simply the count read off v1.5 on the day. **And the direction is against the author's own interest:** three more EXACT rows make a PASS strictly harder, and `OQ-3` argues for keeping them on exactly that ground (*"a seal on an instrument that cannot see the thing that went wrong is not a seal"*). I agree with that judgement. This is not a goalpost move.

**But Matt ruled a number, the number moved after he ruled it, and no carrier he reads says so.** If `TA-X-28/29/30` red, the seal fails on rows that did not exist when the seal criterion was set. That is #73 on the ruling itself.

- **Action (conductor):** one ledger line reconciling Q87's `26` to the instrument's `29`, naming the three additions and that they were added **after** the ruling and make the seal **stricter**. Owed **before a PASS is claimed under Q87**, not after.

## WARN-3 · The decision queue still tells Matt that `Q83(b)` is record-keeping. Under Q87 it decides whether a correct port can be sealed at all

`canonical/matt_decision_needed/README.md` row **Q83**, unchanged since 2026-09-21, reads: *"**(b) `TA-X-06` — reclassify post-hoc? (Rec: YES, to UNGRADEABLE-declared, for the RECORD not the outcome.)** … ⚑ **The cap trips either way, so nothing is rescued;** this is about whether the record says the instrument was wrong."*

**That was true at v1.4. Under Q87 it is false.** The prereg's own § F.2e and `OQ-1` establish the change: the seal now requires all EXACT rows green, `TA-X-06` is unfalsifiable in the honest direction, and *"the only route to green is to INVENT a veto rule — and then REFERENT-v1 is sealed on a fiction."* The stakes moved from bookkeeping to seal-blocking; **the row Matt will actually read still says nothing is at stake in the outcome.**

The failure mode is specific and not hypothetical: Matt reads *"nothing is rescued either way"*, reasonably declines to spend a post-hoc reclassification on a record-keeping matter, and the seal becomes unreachable on a correct port **with nobody having told him that was the consequence.** This run has already lost one escalation to supersession rather than ruling (CLAUDE.md conflict-rule corollary, drax's push conflict); this would be the same shape — a decision resolved on a description that stopped being true.

**I considered BLOCK and declined.** A BLOCK halts W3, and nothing here gates the graded run: attempt 1 can fire, `TA-X-06` will red or be declared, and the consequence lands at the seal (W4 / T-C), not at W3. Halting W3 over a queue-text staleness would cost the lap a day and buy nothing. **WARN with a hard deadline is the proportionate instrument.**

- **Action (conductor, BEFORE `Q83(b)` is routed to Matt — i.e. before W4, and ideally before W3):** amend the Q83 queue row to carry `H-5` / `OQ-1`'s framing: under Q87 this blocks the seal, the recommendation (`UNGRADEABLE-declared`) is unchanged, and the consequence of NOT ruling is a seal unreachable on a correct port.
- **Cheapest global discharge:** route `Q83(b)` to Matt **before attempt 1 fires.** It is already listed blocking at `H-5`. One word from Matt moots the entire `TA-X-06` branch, including the pre-ruling question below.

## WARN-4 · § F.5 cl. 6's instance list was not re-derived against the re-authored and the NEW rows

cl. 6 — *"EVERY EXACT ROW SATISFIED BY AN ABSENCE PRINTS THE ABSENCE"* — enumerates `TA-X-11`, `12`, `19`, `15(b)`, `17` and, new at v1.6, `TA-X-25(a)`. **Three further clauses now have that shape and are not on the list:**

| clause | why it is absence-satisfied or unexercised | class |
|---|---|---|
| `TA-X-25(c)` | `Σ n_nodata_spawn_inert == 0` is guaranteed by the substrate — `POOL-466` holds **zero** NO-DATA members (§ A.3). Satisfied by the same emptiness as `(a)`, which **is** listed | absence-satisfied |
| `TA-X-28(a)` | `n_leech_target_caps_applied == 0` / `n_leech_tick_caps_applied == 0` — neither side implements a cap, so the counters read zero because **the code path does not exist**. Precisely `TA-X-11`'s *"a port with no wall also scores zero"* (#80) | absence-satisfied |
| `TA-X-29(d)` | the 29 inert records take the identity path — but the document derives that **0 of the 29 fall inside waves 151–160**. The clause is **never exercised on the graded path** (#86) | unexercised |

**This closes with no edit and no HALT.** cl. 6 states a **rule** and then gives *"Instances:"* — an illustrative list, not an exhaustive one. Read the rule as binding and the list as incomplete, and all three clauses inherit the print obligation automatically.

Worth naming plainly, because the document itself supplies the moral at § J tally #6: ***"Naming a defect class does not immunise the sentence that names it."*** cl. 6 is the clause that catches green-by-absence, and its own instance list was carried rather than re-derived when four clauses changed shape — **#75 cl. 6, one level up: a remedy does not inherit its predecessor's instrument, and here the remedy did not re-run itself over its own new inputs.**

- **Action (grader):** apply cl. 6's rule to `TA-X-25(c)`, `TA-X-28(a)` and `TA-X-29(d)`; each prints what is absent and why the other value is impossible. `TA-X-29(d)` additionally prints *"unexercised: 0 of 29 inert records fall inside waves 151–160."*
- **Action (v1.7):** re-derive cl. 6's instance list mechanically from the EXACT set rather than maintaining it by hand.

---

## INFO-1 · § F.5 cl. 8's blanket wording vs `TA-X-29(d)` — resolve it now, before a grader has to

§ A row 6 and cl. 8: *"**NO ROW MAY GRADE A PORT RED ON ANY OF THEM**"*, naming `ABS-GLOBAL-MAGNITUDE-FOLD-INERT-RECORDS` (29 records). `TA-X-29(d)` is an EXACT row that reds the port on exactly those 29.

**There is no real conflict, and the direction disambiguates them:** cl. 8 forbids reddening a port for **not implementing** an absence — *"a port that does not implement them is CORRECT."* `TA-X-29(d)` reds a port for **inventing** supply the oracle declined to decode. Opposite directions; both stand.

Recorded here because a conscientious grader reading cl. 8 literally would mark `(d)` UNGRADEABLE → **INDETERMINATE** → nothing seals, a lap spent, no attempt consumed and no progress. **Stating the resolution before the run costs one paragraph; discovering it after costs a lap.**

## INFO-2 · Two grains under one fold name, in the fold the run added a row to catch grain errors

`P-5` declares the global-magnitude fold as reaching **344/344** — **actors** (KP-101: *"the attribute limb reaches 344/344, not I-14's 23/344"*). `TA-X-29(a)` grades **193 / 154 / 527 / 104** — **records**. Both are correct, both reproduce (193 − 39 = 154 and 527 − 423 = 104, exactly the Lap-O populations), and § E.1 trap 9 declares both grains in one sentence. **No defect.**

Flagged only because this run's own tally stands at six instances of *a statistic correct in its arithmetic and wrong in the population it ranged over*, and `344` and `193` will sit in the same verdict file under one fold name.

- **Action (grader):** label the grain in `gmag_conformance` — `attr_limb_records: 193` beside `attr_limb_actors: 344`, per § C.6.

## INFO-3 · `P-4` is RED at the time of writing, and the document says so

The `.app` header reports the v3.4 pack (`c8ab8952…`), not `5cab7433…`. This is scheduled work (`H-1` / drax W2f), declared on the face so *"a green `P-4` means something."* Noted only so a grader meeting a `P-4` red does not file it as a new finding. **Not a WARN — the record is ahead of the state, which is the correct direction.**

---

## Answers to the author's three questions

**OQ-1 · Is carrying `TA-X-06` AS CLASSED correct, so the document does not moot Matt's open question? — YES. Carry stands.**
Reclassifying inside the document that asks Matt to reclassify would answer the question by supersession rather than by ruling. That is the exact failure this run has already paid for once, and CLAUDE.md's conflict-rule corollary is explicit: *an escalation overtaken by events still requires a disposition; silence is not one.* The author declines to moot it for the third version running and routes it as the single highest-priority open item. **That is the correct call and the record should say so.** The consequence — one unruled question blocking the seal — is Matt's to resolve, not the author's to dissolve. My only addition is WARN-3: the carrier Matt reads must state the stakes as they now are.

**OQ-2 · Is `TA-X-25`'s re-authoring a substrate re-derivation (KP-80) or a goalpost move? — A SUBSTRATE RE-DERIVATION. Ratify.**
The test I applied: *does the re-authoring make a PASS easier in a way that could conceal a port defect, and does the author book the cost?*

It **is** easier — clause (c)'s `> 0` became `== 0`, a sign inversion. But:
1. **The easing is forced, and derived three ways.** `POOL-466`'s NO-DATA population is `338 → 0` (§ A.3), reproduced against `P-h` and the newly-pinned `P-k`, with the disjointness check `122 + 342 = 464` and the two-record residue (`basilisk_a01`, `yetidire_a01`) **predicted by name in the rebase note before measurement and confirmed by name on the shipped pack.** Carried unchanged, the old clause **reds a correct port on every arm** — that is KP-80's finding, not the author's convenience.
2. **The author books the cost in the losing direction.** § F.2f states plainly that the row *"HAS STOPPED PROVING"* the port draws from `POOL-466`, that *"the behavioural check is gone and the declaration is not a substitute"*, and that *"nothing replaced it."* § E.1 trap 6 is widened: *"v1.5 could say 'narrower again.' v1.6 must say 'wider.'"* **A goalpost move does not widen its own declared blind spot and refuse to let the change read as progress.**
3. **It was recommended before the document existed** (`OQ-B` of the rebase note, routed to the conductor), so it is adopted, not invented at the point of need.
4. **The identity form is more durable than what it replaced** — `F.1a`'s own lesson. An identity over a partition survives the next substrate move; a sign does not.

One residual, already covered by WARN-4: clause (c) is now substrate-guaranteed and belongs on cl. 6's print list.

**OQ-9 / `C-h` · `TA-X-09` grades 9 of 29 normative vectors, the 20 skipped govern mitigation order. Honest scope or hole? — HONEST SCOPE. Do not widen here.**
Refusing to grow the instrument in the session before a graded run is exactly what `F5` exists to enforce, and the author names it: *"an author who grows his own instrument at the last moment has built a goalpost, not a gate."* Widening now would be indistinguishable from the move the whole prereg discipline forbids. **Declaring it as `C-h` and routing it to `OQ-9` is the correct disposition, and it is a disclosure the previous five versions did not make.**

**One addition, because Q87 changed the consequence.** The document's own sentence — *"a port that reproduces 9 of 29 vectors and diverges on the mitigation order would pass `TA-X-09` and be wrong about every hit the player takes"* — is currently in an open question at the back of the file. Under Q87 a PASS **is** the seal, and this is the sharpest statement in the document of what a PASS does not buy. It belongs beside § F.5 cl. 10 on the **seal packet's** face, not only in `OQ-9`. That is a W4 packet obligation, not a prereg edit.

---

## Position on the conductor's pre-ruling (veto-open)

> *A `TA-X-06` red in attempt 1 does NOT trigger a repair or attempt 2, because no port change can move it; only Matt's `Q83(b)` can. Attempt 2 is reserved for port defects a repair can address.*

**AGREE on the substance. OBJECT to its incompleteness — it settles the repair and leaves the scarce resource unaddressed.**

The substance is right and follows from § F.2e: no port change can move `TA-X-06`, so requiring a repair would require inventing a veto rule nobody wrote, and `L2` would then gate attempt 2 on my Gate-2 PASS of a fiction. Correctly refused.

**What the pre-ruling does not say is whether the attempt is CONSUMED.** § G is unconditional: `STRUCTURAL` = *"≥ 1 EXACT row RED"* ⇒ *"consumes one of the two attempts."* So on the taxonomy as written, a `TA-X-06` red spends attempt 1 **whether or not a repair follows.** The pre-ruling frees the port from a pointless repair and leaves the cap exposed to a row that is not about the port.

The bad case is precise: **`TA-X-06` reds ALONE, every other EXACT row green.** The port is correct, the seal is unreachable for want of one unruled question, and **half of the allowance Q85 just reset has been spent on a row no port change could ever have moved.** Q85's reset came from outside the run because that is the only place it legitimately can — which makes burning an attempt this way expensive in a currency the run cannot re-mint for itself.

**Recommended disposition, in priority order:**

1. **PREFERRED — route `Q83(b)` to Matt before attempt 1 fires.** It is already `H-5`, already blocking, already carries a one-word recommendation Matt himself wrote (*"Rec: YES, to UNGRADEABLE-declared"*). One word moots the entire branch: no pre-ruling needed, no attempt at risk, and WARN-3 is discharged by the same action. **This is the cheapest path on the board and it costs the lap nothing to take.**
2. **IF attempt 1 fires first** — record **now, before any graded result exists**, that a run whose **only** EXACT red is `TA-X-06` is filed `STRUCTURAL @ TA-X-06-ONLY` and **does not consume an attempt**, on the same logic by which `INDETERMINATE` does not: the run is no further forward and the defect is not the port's. **Timing is the whole point — recorded before a result, this is a pre-registration; recorded after, it is post-hoc rescue and `WARN-16`.**
3. **Either way — record the pre-ruling against the WAVE, not only in this session.** CLAUDE.md's conflict rule, from this run's own escalation: *"A posture communicated to one session is not a posture the wave has."* The pre-ruling belongs in the lap plan or the charter ledger.

**No prereg edit is implied by any of the above.** The document is immutable on commit and every remedy here lands on the ledger, the queue, the W4 packet, or the grader's report face.

---

## Action

- [ ] **Conductor (gandalf) — before `Q83(b)` is routed, ideally before W3:** amend `canonical/matt_decision_needed/README.md` row `Q83` so (b) carries its Q87 stakes. **WARN-3.**
- [ ] **Conductor — before a PASS is claimed under Q87:** one ledger line reconciling Q87's `26` EXACT rows to the instrument's `29`. **WARN-2.**
- [ ] **Conductor — before attempt 1:** record the `TA-X-06` pre-ruling against the wave, including the attempt-consumption clause. **Pre-ruling § 2–3.**
- [ ] **Matt — `H-5` / `Q83(b)`:** one word. Unblocks the seal and moots the pre-ruling entirely. *(Escalated; not mine to approve.)*
- [ ] **Grader (gamora, W3) — at emission:** print `[M-POL2]`'s epoch beside `TA-B-01`'s array (**WARN-1**); apply cl. 6's print rule to `TA-X-25(c)`, `TA-X-28(a)`, `TA-X-29(d)` (**WARN-4**); label the `gmag_conformance` grain (**INFO-2**); treat `TA-X-29(d)` as gradable per **INFO-1**.
- [ ] **drax — `H-1`…`H-4`:** unchanged and still blocking. `P-4` stays red until the `.app` reports `5cab7433…`. **INFO-3.**
- [ ] **v1.7 (not now):** extend § C.7 to name the sealed-cell epoch; derive cl. 6's instance list mechanically; widen `TA-X-09` to 29 vectors as the FIRST row added (`OQ-9`).

**Verdict: PASS-WITH-WARNS. No BLOCK. W3 is clear to proceed.** The four WARNs are discharged at the ledger, the queue and the report face; none requires a change to the immutable document, and none gates the graded run.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.6.md` (`db2c0ca3…`) — the target
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` — ledger KP-80, KP-83 (Q85/Q87), KP-86 (F-3/F-4), KP-90, KP-97, KP-100, KP-101, KP-103
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-28-kc2-play-seal-lap-plan.md` — L1/L2/L3/L4, wave table, stops
- `/Users/admin/Games/reincarnated-collaboration/canonical/matt_decision_needed/README.md` — row `Q83` ((b) and (c) OPEN, verified this session) · row `Q84` (F4/F5 lineage)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` — `⚑ arms.M-POL-2.terminals` read for WARN-1; **hash-verified only, never executed. K-7 held.**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-21-run-KC2-PLAY-gate2-baton-v3p3.md` · `2026-09-20-run-KC2-PLAY-w1-preread.md` — predecessor gates

*Filed 2026-09-29 by jack-ryan, DESIGN-MODE Gate-1 pre-read, Run KC2-PLAY SEAL LAP seat W2. Target hash derived before reading, per the brief's HALT condition. No production code. No push.*
