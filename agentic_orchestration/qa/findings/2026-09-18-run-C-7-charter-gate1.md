# Finding — 2026-09-18 — Run C-7 charter v1.0 (Gate-1, pre-GO)

**Reviewer:** jack-ryan (DESIGN-MODE, Gate-1)
**Verdict:** **BLOCK — narrow.** 3 BLOCK · 11 WARN · 6 INFO. No BLOCK is a design objection; all three are record-and-preregistration defects with named one-paragraph discharges, and none needs Matt. Arm B's survival is not in question in any of them.
**Target:** `agentic_orchestration/gandalf/notes/2026-09-17-vfx-run-C-7-charter.md` v1.0 (`sha256[:12] 8892ada80395`, 45 lines — **verified**) · ledger `astra_test_01/burst/runs/C-7/ledger.json` (R-C7-0…0e, 2 `grok_calls`) · account `agentic_orchestration/gandalf/notes/2026-09-17-c7-account.md` · cut manifest `runs/C-7/artifacts/BW-video-r1/frames.json`
**Author under review:** gandalf (ARCHITECT → RUN-CONDUCTOR on GO)
**Principles applied:** 1 (math-before-code) · 2 (smoke-gate) · 3 (cross-seam impact) · 4 (decisions-log as truth) · 5 (severity matters)
**Pattern / disciplines cited:** desirable-run-pattern § 3 (fit test F2/F3), § 4 (halt taxonomy), § 5.1/5.2/5.3/5.4 (standing safeties) · Disciplines #62(a), #63, #73, #75 cl. 6 · ADR-002, ADR-006 · C-5 charter § 8 · C-6 charter § 7

---

## 0. Verdict in one paragraph

The substrate pins in § 1 are the **first in this lane I could verify without amendment** — MANIFEST `f0851b83bb36` matches byte-for-byte, `export/` is clean in the shared working tree (no live freeze churn, unlike C-6 BLOCK-A), and `cliffside_v44` is genuinely the newest staged project. The video trial was conducted well: pre-registered before the first clip, two-attempt discipline applied to Grok as to bursts, the repair clip **diagnosed** rather than re-rolled, and every Matt word ledgered with its class. The three BLOCKs are all one shape — **the record does not carry what the run is relying on**: the charter has no HALT section at all though the account says it inherits one verbatim (BLOCK-A); the A/B is pre-registered as an *event* but not as a *decision rule*, and the two arms do not enter on equal evidence (BLOCK-B); and two pre-registered gates that did not pass are written up as a PASS (BLOCK-C). All three are clear in one editing pass plus one ledger line.

---

## 1. The eight questions, answered

**Q1 — exit predicate decidable, A/B pre-registered?** Half. (a)–(e) of the fire DONE list are decidable by trace; (f) is Matt's eye, correctly a *reserved ratification point* (pattern § 5.3) rather than a run-decidable predicate — the fit test's F2 is formally NO and that is fine, because the taste gate is declared. What is **not** pre-registered is the A/B's decision rule: § 2.1 fixes the *setup* (same landing spot, three casts each) and says "Matt's eye rules", but never enumerates the admissible verdicts, never equalises the evidence the two arms carry into the room, and never states the trace standard applied to arm B. → **BLOCK-B.** And the trial that produced arm B reports two failed gates as a pass → **BLOCK-C.**

**Q2 — substrate pins correct and complete?** Correct; not complete. Verified by hand: `shasum -a 256 MANIFEST.sha256` → `f0851b83bb36bef2…` ✓ · `git status --porcelain -- astra_test_01/burst/export/ …/MANIFEST.sha256` → **empty** (the freeze is still) ✓ · `runs/C-5/cliffside_v44` is the highest staged version, no v45 ✓ · `runs/C-7/specs/` empty, consistent with "filed at launch" ✓ · 79 GB free ✓. **Incomplete on two counts:** the inherited RED list is a subset of R-C5-139's (WARN-7), and the C-5 close-out debt is named in the STATUS line and § 6 — **correctly, as debt, not silently absorbed** — but the FL-6d double-VOID that sits inside it is carried as a fact with no disposition (WARN-8).

**Q3 — HALT rules restated or referenced unambiguously?** **No — they are absent.** `grep -niE "halt|safet"` over the charter returns **zero** matches. C-5 § 8 is referenced nowhere in the charter; it lives only in the account's P0 bullet. The charter's own STATUS line says *"intent residency by charter, not by conversation"* — so a rule that lives only in the conversation is, by the charter's own standard, not a rule this run holds. → **BLOCK-A.** On the sub-question: the pre-GO video trial is **correctly** a commitment-boundary ruling, not a conductor re-scope — `R-C7-0` is `"class": "matt"`, `veto_open: false`, carries Matt's verbatim *"Ok, go ahead"*, and the charter discloses it in § 3 as *"P0-v the video trial ran ahead of GO under R-C7-0"*. No halt rule was re-scoped in-run. Clean.

**Q4 — the video route and V15/V7?** The amendment is recorded with authority correctly attributed to Matt (R-C7-0, class `matt`), and V7's *rationale* is respected in substance: the clip carries the effect's **body** only, while the grammar and duration stay at runtime — the lob to frame 0, the tick clock (R-C7-0d), the 12-s scorch decal accumulating per cast (R-C7-0e cl. 2), the FL-5 smoke layer held out of the clip precisely because a grey band would collide with the four-plane ramp (R-C7-0e cl. 3), palette/tint/labels/floor light. That reasoning is exactly V7's, honoured. But the charter names **V15 only**, and V15 ("no-video first for bursts") is not the verdict arm B touches — **V7** ("no video as shipping frames") is, since the flipbook *is* shipping frames. → WARN-5, citation not substance.

**Q5 — sourcing class?** **Clean, verified.** Both `grok_calls` rows carry `still` = `runs/C-7/artifacts/BW-video-seed/bw_seed_01.png` (`697e30bd6d38`) — our own flask primitive on a green plate — and a prompt sha. No source clip appears as a Grok input, and no source clip appears as a burst input anywhere in the run. R-C7-0 states the rule (*"Grok gets our still + prompt, never a source clip"*). The defect is only that the rule lives in the ledger and not in the charter's § 5, where the next reader looks → WARN-6.

**Q6 — concurrency with C-6?** No collision found, but the law is one-sided. § 5 is a single line — *"Same law as C-6 charter § 7, mirrored"*. C-7 **owns the freeze**, and C-6 § 7.7 requires a **named disposition** whenever the MANIFEST sha in force changes and a consumed path moves; nothing in § 5 obliges C-7 to announce a freeze to C-6, so C-6 cannot discharge its own rule. The `.heavy.lock` (C-6 § 7.2, which explicitly *asked C-5's conductor* to adopt it — C-7 is that conductor's successor) is not named. C-6 § 7.9 says it outright: *"a law recorded on one side is the CLAUDE.md conflict-rule defect."* → WARN-9. Grok allowance is shared with no split or priority rule → WARN-11.

**Q7 — forks F1/F3/F4/F5 with P1 open?** **Yes, P1 (BL-2v) is launchable** — but the reader has to derive it. F1 (FF-08) gates **P2**, by § 1's own words *"blocking for E3-r1"*. F3 (Healing Hands radius) gates a skill behind the R-C5-125 PAUSE. F5 (fire lane on video) is gated by its own recommendation — *"(a) YES — **after** Blackwater's A/B verdict"* — and its alternative (b) is explicitly not recommended for exactly this reason. F4 (web cadence) touches only the deploy at (f), which § 3 already gates on Matt's word either way. So each open fork is either gated or off P1's path. One sentence in § 4 saying so would make this checkable instead of derivable (INFO-3). Two fork-register defects sit on top: F6-bis is listed open though Matt ruled it (WARN-2), and F3's recommendation contradicts its own source document (WARN-3).

**Q8 — instrument lineage (#62(a) / #75 cl. 6)?** **Recorded in prose, not in a form a later reader can bind numbers to.** R-C7-0a names the two fixes (hue key for the plate gate; pool-only footprint over the bottom 35 % of subject rows) and R-C7-0b names the third (O1 single-peak is an artefact — *"the O1 instrument must measure the flash outside the pool"*). `frames.json` pins the source clip (`b3e13cde28f6`) and its rulings. But **no version of `bw_cut.py` has a recorded sha**, clip 1's plate/footprint numbers were produced by the *pre-fix* instrument and are compared against clip 2's *post-fix* numbers inside a single ruling, and **O1 is knowingly still wrong and still unfixed** — clip 2's `single_peak FALSE` was overridden by conductor eye. #75 cl. 6 is the rule that names this: *a remedy does not inherit its predecessor's instrument.* → WARN-10.

---

## 2. BLOCK findings

### BLOCK-A — the charter carries no HALT rules, and by its own residency standard that means the run does not hold any

`grep -niE "halt|safet|kill"` over all 45 lines of the charter returns **nothing**. C-5 charter § 8 — the seven clauses the account says are inherited *verbatim* (two consecutive experiment FAILs · two VOIDs in a row · a JUDGE passing its control twice · three rate-limit backoffs · any write outside `out/` · the image cap un-enforced by the 999999 sentinel · **any medium or bar change**) — is not referenced anywhere in the document. The C-6 charter, by contrast, carries its safeties as § 8 and its concurrency law as a nine-clause § 7.

This matters for three named reasons, not one. **(i)** The charter's own STATUS line declares *"intent residency by charter, not by conversation"* and hands the run to *"a fresh gandalf session"* — a fresh conductor reading only this document inherits no halt rules at all. **(ii)** C-5 § 8's final clause is *"the conductor may not re-scope a halt rule in-run (H-C3-2 lesson, R-C3-22)"* — a clause that cannot bind a conductor who was never handed it. **(iii)** The "any medium or bar change" clause is live *right now*: arm B is a medium change (painted-2D → video-derived flipbook), authorised at commitment level by R-C7-0, which is exactly how that clause is supposed to work — and the charter does not record that the clause fired and was discharged by Matt.

**Minimal discharge (gandalf, no Matt needed):** add **§ 7 HALTs** — *"`2026-09-15-vfx-run-C-5-charter.md` § 8 inherited verbatim and restated here:"* followed by the seven clauses, **plus** the § 2 fallback already drafted (a skill failing (f) twice after a taste round → parked with the debt named), **plus** the disk floor C-6 § 7.5 carries (HALT under 10 GB free; 79 GB today, so this costs nothing to state), **plus** one line recording that the medium-change clause fired at R-C7-0 and was discharged by Matt's word.

### BLOCK-B — the A/B is pre-registered as an event, not as a decision rule, and the two arms do not enter on equal evidence

§ 2.1 gives the setup and the judge: *"Packet 106: both kits at the same landing spot, three casts each"*, *"ruled by Matt's eye"*. Three things it does not give:

1. **The admissible verdicts.** A wins / B wins / a **hybrid** (the clip for the pool body, runtime for the rest — the most likely outcome given R-C7-0e already splits smoke to runtime) / **neither**. § 2.1 branches only on *"If B wins"*. A verdict the charter has no branch for is a goalpost the run will have to move after seeing results, which is the one thing pattern § 5.1 exists to prevent.
2. **Equal evidence.** Arm B enters the room carrying **Matt's own "very good"** on the clip that is its body (R-C7-0c) and two rounds of measured gates. Arm A is `BL-1a-r1`, which per the account *"never had its own pack (rode the fire PACKs)"* — it has never been packed, never shown, never given a taste round. Asking one eye to choose between a polished arm and an unpacked one is not an A/B; it measures preparation, not route.
3. **The trace standard for arm B.** § 2.1 says *"the winner passes DONE (a)–(e) by trace"* — after the verdict. If arm B wins, (a) eight directions and (b) touch aim forward have to hold for a **flipbook field body**, which is a different question from holding for a runtime one, and the run would discover that post-verdict.

**Minimal discharge (gandalf, no Matt needed):** three sentences in § 2.1 — (i) enumerate the four admissible verdicts and say what each means for the decisions-log proposal (hybrid is a legitimate win for *both*, and should be named as such rather than discovered); (ii) *"arm A gets its own PACK and one taste round before Packet 106"* — or, if the conductor judges that unnecessary, record **why** in one line so the asymmetry is a decision and not an accident; (iii) *"(a)–(e) are traced for **both** arms before Matt looks; the packet carries both traces."*

### BLOCK-C — two pre-registered gates did not pass, and the ruling records the trial as passing its pre-registered gates

R-C7-0 pinned the gates before any clip existed — correct preregistration, and to the conductor's credit. Among them: **aspect 0.58 ± 0.05** and **flicker 3.3–3.6 Hz**, with the kill rule *"two clips fail → runtime Blackwater proceeds unchanged"*.

Clip 1 failed (R-C7-0a, real misses named honestly). Clip 2's own ruling records, verbatim: *"flicker 2.0 Hz coherence 0.04 (source 3.3–3.6)"* and *"pool aspect 0.45 (target 0.58)"* — **both outside their pre-registered bands**, the aspect by 2.6× the tolerance. Each is then discharged in the same sentence by a post-hoc remedy (a 1.3–2× retime at the bind; a bind-side y-scale of 1.29, already encoded as `y_scale: 1.281` in `frames.json`). The ruling's conclusion nevertheless reads: *"the video-spine route **PASSES its pre-registered gates** on the second clip."*

**I am not disputing that arm B should proceed.** Matt's *"clip two looks very good"* (R-C7-0c) is more authoritative than any gate this run could write, and R-C7-0d — *"clip 2 at 1× looks best… the 2.0 Hz flicker is accepted by eye over the source's 3.3–3.6 Hz"* — is a **commitment-boundary ratification of the flicker miss by name**, which is precisely the right instrument. The defect is that the record says the mechanism cleared the bar when the eye did, and that the aspect miss has **neither** a Matt word nor a kill-rule disposition — it was remedied bind-side by the conductor and then counted as a pass. Pattern § 5.1 and § 5.2 together: the run cannot move its own goalposts, and in-run reclassifications go to independent Gate-2. This reclassification never left the run.

**Minimal discharge (gandalf, one ledger line + one wording fix):** file **R-C7-0f** (conductor, veto-open) stating (i) clip 2 missed `aspect` (0.45 vs 0.58 ± 0.05) and `flicker` (2.0 Hz vs 3.3–3.6 Hz) as pre-registered; (ii) **R-C7-0c/0d are the commitment-boundary ratification** that disposes of the two-clip kill rule — the trial survives on Matt's eye, not on the gate sheet; (iii) the aspect miss is discharged **bind-side** by `y_scale 1.281`, a conductor disposition open to Matt's veto, and it is re-measured on the bound flipbook at BL-2v rather than assumed; and change § 2.1 / the STATUS line from *"passes its pre-registered gates"* to the accurate form. This BLOCK clears in about four lines and leaves arm B exactly where it is.

---

## 3. WARN findings — each with the edit that clears it

**WARN-1 — the ledger's charter pin is stale; six rulings are attributed to a superseded charter.** `ledger.json › charter_sha256_12` = **`4e8185d424d7`** (v0.1, per the account). The charter under review is **`8892ada80395`** (v1.0). R-C7-0…0e — including all five Matt rulings — are recorded against a version that no longer resolves. #73: the state changed and the record did not follow.
**Edit:** R-C7-1 restamps `charter_sha256_12` to `8892ada80395` and carries one line — *"R-C7-0…0e were ruled under v0.1 (`4e8185d424d7`); v1.0 was amended from them"* — so the attribution boundary is explicit rather than lost.

**WARN-2 — § 1 lists F6-bis as an open inherited decision; Matt ruled it, and ruled against the conductor's lean.** § 1's *"Open decisions inherited"* row reads *"F6-bis (Profane-Bloom lobe: conductor lean no)"*. **R-C5-125 (class `matt`, 2026-09-17)** rules PConc as the full Occultist combo *"+ Profane-Bloom fuchsia lobes at struck/killed bodies"* — i.e. **yes**, against the lean. The re-spec v2 already implements the ruling (per the account), so only the charter row is wrong — but it is the row Matt reads. Principle 4 (decisions-log as truth).
**Edit:** strike F6-bis from § 1's open list; it is RULED by R-C5-125. If the conductor still wants the lean heard, it is a re-opening request to Matt, not an open fork.

**WARN-3 — charter F3 recommends 220 px; the fork's own source document recommends ≈200 px and records 220 as the *pre-1.4* number.** Q80 F5 reads: *"the original 220 px radius matched [pre-1.4]… **Recommend (a): author 1.5 BH radius (≈ 200 px) as a register choice and mark it AUTHORED**"*. Charter F3(a) reads *"220 px authored (matches the pre-1.4 dome), marked AUTHORED"*. The account already spotted this (*"charter F3 says 220 px, Q80 F5 says ≈200 px, different quantities"*) — but the account is not what Matt reads, and the charter presents 220 as the single recommendation with no sign that its source said otherwise.
**Edit:** F3's row states both numbers, names which quantity each is (1.5 BH radius vs the pre-1.4 dome's 3.4–3.6 BH width match), and makes the fork the choice between them.

**WARN-4 — two live fork registers with colliding numbers, presented to the same reader.** Charter **F1** = Q80 **F4** (FF-08). Charter **F3** = Q80 **F5** (HH radius). § 1's inherited row cites the Q80 numbering (*"Q80 F3 … F4 … F5 … F6-bis"*) three lines above § 4's table using its own. #63.
**Edit:** label each § 4 row with its Q80 number inline — *"F1 (= Q80 F4) FF-08"*, *"F3 (= Q80 F5) Healing Hands radius"*.

**WARN-5 — the STATUS line amends V15; V7 is the verdict arm B actually touches.** V15 = *"no-video first for bursts"*; **V7 = "no video as shipping frames"**. Arm B ships video-derived frames as a flipbook, so it is V7's letter that is being amended. Its *rationale* — grammar and duration cannot live in a clip — is honoured by design (lob, tick clock, 12-s accumulating decal, FL-5 smoke all at runtime), and that is the load-bearing fact; it just isn't written down against the right verdict number.
**Edit:** STATUS line and § 2.1 read *"V15 re-opened **and V7 amended** for this trial by R-C7-0 (Matt): video may be a shipping frame source for an effect's **body** where the grammar — lob, tick clock, decal life, smoke, palette — stays at runtime. V7's rationale stands and is what the spine-from-CONTACT design is built on."*

**WARN-6 — the class-E sourcing rule lives only in a ledger ruling, not in the charter.** Verified clean in practice (Q5 above), and it is the rule most likely to be violated by a *fresh* conductor filling arm B's gaps from footage that is sitting right there on the Desktop.
**Edit:** § 5 gains one line — *"Source videos are class-E, measurement-only: never a burst input, never a Grok input. Grok receives our own still + prompt only (R-C7-0)."*

**WARN-7 — § 1's inherited-RED list is a subset of R-C5-139's, with no total.** § 1 names *"twelve stale-value tests + three Blackwater staged-copy tests"* = 15. R-C5-139 records *"outside suite **764 pass / 17 red / 3 error**: five standing + E3-r1 + twelve stale-value + three Blackwater"*. The five standing oracle reds and the E3-r1 red survive in § 6's debt list; the 3 errors appear nowhere. A later reader diffing a suite run against this pin will find six more reds than the charter led them to expect.
**Edit:** § 1 states the totals — *"764 pass / 17 red / 3 error at the post-FL-6c freeze (R-C5-139): five standing oracle + E3-r1 + twelve stale-value + three Blackwater staged-copy"*.

**WARN-8 — FL-6d and FL-6d-r1 both VOID = "two VOIDs in a row", a C-5 § 8 HALT condition, carried in as a fact with no disposition.** § 1 records *"FL-6d / FL-6d-r1 VOID exit 3"* flatly. C-5 § 8 lists *"two VOIDs in a row"* as a HALT to Matt. Whether C-5 halted, and what Matt said if it did, is not in the C-7 record — and the alignment wave that VOIDed twice is the one that was supposed to clear the reds C-7 is now inheriting. Compounds with BLOCK-A: a charter with no halt section cannot show that an inherited halt condition was dispositioned.
**Edit:** one line in § 1 or the new § 7 — either the disposition, or *"the FL-6d/FL-6d-r1 double-VOID is an inherited, un-dispositioned C-5 § 8 HALT, carried as debt and surfaced to Matt at R-C7-1."* Silence is not a disposition (C-6 § 7.7's own wording).

**WARN-9 — the concurrency law is one line, and the half that binds C-7 is missing.** § 5: *"Same law as C-6 charter § 7, mirrored."* C-7 **owns the freeze**. C-6 § 7.7 obliges C-6 to name a disposition whenever the MANIFEST sha in force changes *and* a consumed path moves — C-6 cannot perform that duty if C-7 does not tell it a freeze happened. C-6 § 7.2's shared advisory lock `~/astra-burst/.heavy.lock` was written with an explicit ask to *"C-5's conductor"* to adopt it; C-7 is that conductor's successor and does not name the lock. C-6 § 7.9: *"a law recorded on one side is the CLAUDE.md conflict-rule defect."*
**Edit:** § 5 gains two clauses — *"(i) every C-7 freeze is announced in C-6's `FOR-C-5-CONDUCTOR.md` (re-titled) with the new MANIFEST sha and the moved-path list, so C-6 can disposition per its § 7.7; (ii) C-7 takes `~/astra-burst/.heavy.lock` before any headless Godot run or test suite."*

**WARN-10 — instrument lineage is prose, no shas, and one instrument is knowingly still wrong.** `bw_cut.py` was fixed twice between clip 1 and clip 2 (hue key; pool-only footprint), and clip 1's plate `0.49` and drift `0.35` are *pre-fix* numbers compared against clip 2's *post-fix* `0.74` / `0.107` inside one ruling. **O1 single-peak remains broken by the conductor's own diagnosis** (*"the O1 instrument must measure the flash outside the pool"*) and clip 2's `single_peak FALSE` was overridden by eye. No version of the script has a recorded sha. #75 cl. 6 — *a remedy does not inherit its predecessor's instrument* — and #62(a)'s standing lesson that a check running is not a check passing.
**Edit:** record `bw_cut.py`'s `sha256` in the ledger **per version** with the ruling it served; mark clip 1's plate/footprint figures as pre-fix and therefore not comparable to clip 2's; and list the O1 fix as **owed before any further clip is measured**, not as a note in the account.

**WARN-11 — a shared Grok allowance with no split, no priority and no recorded size, and F5(a) would open a third consumer.** § 5: *"one weekly allowance shared with C-6's 40-clip queue; … 2 used at v1.0."* C-6's queue alone is 40 clips; the allowance size is nowhere recorded; F5(a) adds a bounded fire lap after the A/B. Two concurrent runs drawing on one externally-metered budget with no rule is the shape C-3 died in (402, balance exhausted).
**Edit:** one line — either *"C-6's 40-clip queue has right of way; C-7 clip calls are capped at N per phase and ledgered in `grok_calls[]`"*, or the split Matt prefers. Cheap now, expensive at the 402.

---

## 4. INFO findings

- **INFO-1 — the § 1 pins are the first in this lane I could verify without amendment. Credit where it is due.** `MANIFEST.sha256` → `f0851b83bb36bef2…` matches the charter exactly; `git status --porcelain` over `export/` and the MANIFEST returns **empty**, so unlike C-6's BLOCK-A the tool tree really is frozen, not re-freezing hourly; `cliffside_v44` really is the newest staged tree (v40–v44 present, no v45), so unlike C-6's WARN-7 the scene pin is not already stale. Three pins, three clean verifications.
- **INFO-2 — the trial's conduct is the pattern working, and should be said so plainly.** Gates pinned before clip 1 existed; the two-attempt discipline extended from bursts to Grok calls by explicit analogy (R-C7-0a); clip 2 was a **diagnosed repair** with each fix traced to a named miss, not a re-roll; the instrument artefacts were caught and labelled as artefacts rather than accepted as results. BLOCK-C is a write-up defect sitting on top of a well-run trial.
- **INFO-3 — the fork gating is correct but must be derived.** Per Q7. **Edit:** one sentence in § 4 — *"P1 is launchable with F1/F3/F4/F5 open: F1 gates P2, F3 gates a post-PAUSE skill, F5 is gated behind the A/B verdict by its own recommendation, F4 sets only deploy cadence and § 3 already gates the deploy on Matt's word."*
- **INFO-4 — (f) should be named as a reserved ratification point.** Pattern § 5.3. The run is taste-gated at every skill by design, so the fit test's F2 is formally NO — mitigated because (a)–(e) are decidable by trace and the taste gate is *declared*. Worth one line in § 2 so the stop at each (f) reads as a **commitment-boundary HALT** (pattern § 4, correct, keep forever) and never as a stalled run.
- **INFO-5 — `runs/C-7/specs/` is empty, so § 2 predicate 2 is un-evaluable at Gate-1.** Consistent with *"filed at launch"* and with the account. I am deferring the six re-specs — every number traced to Table B / § 12 or boxed HOUSE — to Gate-2, and the account's six OPEN items (HH radius, the `fire_burst_e0p_v2`/`_v3` spec mismatch, PConc `range_px` 480 vs 520, fan count, bloom trigger, `residue`/`collision` null admission) come with them. Flagging so no one reads this PASS as covering them.
- **INFO-6 — disk is not a concern this run.** 79 GB free against C-6 § 7.5's 10 GB floor. No action; the floor still gets stated, folded into BLOCK-A, because the cost of writing it is one clause and the cost of not having it was C-6's WARN-9.

---

## 5. Action summary

**gandalf (charter + ledger, all pre-GO, none needing Matt):**
- [ ] **BLOCK-A** — add § 7 HALTs: C-5 § 8's seven clauses restated verbatim + the § 2 fallback + the 10 GB disk floor + the line recording that the medium-change clause fired at R-C7-0 and was discharged by Matt.
- [ ] **BLOCK-B** — § 2.1: enumerate the four admissible A/B verdicts; give arm A its own PACK and taste round before Packet 106 (or record why not); trace (a)–(e) for **both** arms before Matt looks.
- [ ] **BLOCK-C** — file R-C7-0f naming the two missed gates, recording R-C7-0c/0d as the commitment-boundary ratification that disposes of the kill rule, and the aspect miss as a bind-side conductor disposition re-measured at BL-2v; fix the "passes its pre-registered gates" wording.
- [ ] WARN-1 restamp `charter_sha256_12` + attribution-boundary line · WARN-2 strike F6-bis (RULED, R-C5-125) · WARN-3 state 200 **and** 220 with their quantities · WARN-4 label forks with their Q80 numbers · WARN-5 name V7, not only V15 · WARN-6 class-E rule into § 5 · WARN-7 full 17 red / 3 error · WARN-8 disposition the inherited double-VOID · WARN-9 freeze-announcement + `.heavy.lock` into § 5 · WARN-10 `bw_cut.py` shas per version + O1 fix owed before the next measured clip · WARN-11 a Grok split or priority rule.
- [ ] INFO-3 one sentence on fork gating · INFO-4 name (f) a reserved ratification point.

**Matt (2 items, neither blocking P1):**
- [ ] **The fork letters already routed** — F1 (FF-08 scope), F3 (Healing Hands radius — **please read WARN-3 first: your own Q80 F5 recommended ≈200 px, the charter offers 220**), F4 (web cadence), F5 (the fire lane on video, gated behind the A/B by its own recommendation).
- [ ] **Grok allowance between C-7 and C-6.** One weekly allowance, C-6 holding a 40-clip queue, size unrecorded, F5(a) adding a third consumer. Right of way is yours to set. *(WARN-11.)*

**ADR-002 approval authority.** Every gandalf item above is charter wording, ledger record correction, or within-run conductor discipline — **mine to approve directly**, and I approve them on execution. No cross-seam schema change is proposed here (arm B consumes the exporter; BL-2v's flipbook mode is C-7's own TOOLING under a freeze it owns), and nothing needs a new ADR. If arm B wins the A/B, the *decisions-log proposal* that follows — "video spine from contact = the field-effect production method", amending V7 — is a **Matt** ratification and comes to me for the entry, per § 2.1 as written. That routing is correct as drafted.

**Gate-1 verdict: BLOCK — narrow.** Three record-and-preregistration defects, each with a named discharge, none touching the design and none needing Matt. On BLOCK-A's § 7, BLOCK-B's three sentences and BLOCK-C's one ledger line, **this charter is GO**. The substrate work behind § 1 is the cleanest this lane has produced, and the video trial was conducted the way the pattern says to conduct one — which is exactly why the write-up should not say the gates passed when the eye did.

---

## 6. References

**Under review**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-17-vfx-run-C-7-charter.md` (v1.0, `8892ada80395`, 45 lines)
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/ledger.json` (R-C7-0…0e; `charter_sha256_12` `4e8185d424d7`; 2 `grok_calls`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-17-c7-account.md`
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/artifacts/BW-video-r1/frames.json` (`source_sha12 b3e13cde28f6`, `y_scale 1.281`, 145 frame shas)

**Substrate verified by hand**
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/MANIFEST.sha256` → `f0851b83bb36bef2ef1913aa414a5cd2c9eccf22b2b4484861598b900f4a6db8`
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/cliffside_v44` (newest staged; v40–v44 present)
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/specs/` (empty)

**Authority consulted**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/operating-procedures/desirable-run-pattern.md` §§ 3–5
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-15-vfx-run-C-5-charter.md` § 8 (HALTs), line 37 (the V-register: V7, V15, V20)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-17-necromancer-run-C-6-charter.md` § 7 (concurrency law)
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-5/ledger.json` (R-C5-125…139)
- `/Users/admin/Games/reincarnated-collaboration/canonical/matt_decision_needed/2026-09-16-c5-e3-deployment-fit-zeus-healing-hands.md` (Q80 F3/F4/F5/F6/F6-bis/F7)

**Precedent**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-15-run-C-5-charter-gate1.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-17-run-C-6-charter-gate1.md`

---

## 7. Re-check — 2026-09-18, after the conductor's discharge

**Re-check verdict: PASS-WITH-WARNS.** All three BLOCKs are discharged at or above the minimal bar I named. **This charter is GO for P1 (BL-2v).** Nothing below blocks the launch; two items are new, one WARN is re-scoped rather than cleared, and one is deferred by design.

**Target re-verified:** charter `419cc6c04e97` (55 lines, was `8892ada80395` / 45) · ledger `runs/C-7/ledger.json` now R-C7-0…**0f** + note `N-C7-instruments` · new `astra_test_01/burst/runs/FREEZE_NOTICES.md` · new `runs/C-7/conductor_scripts/heavy_lock.py`, `wave.sh`, `bw_cut.py` v3 (`09086010aeb4`, matches the note's sha — **verified by hand**).

### 7.1 BLOCK discharges

**BLOCK-A — DISCHARGED, above the bar.** § 7 exists and carries C-5 § 8's **seven clauses** (checked one-for-one against `2026-09-15-vfx-run-C-5-charter.md` § 8: two experiment FAILs · two VOIDs · JUDGE control twice · three rate-limit backoffs · any write outside `out/` · the 999999 sentinel · any medium or bar change **with** the no-re-scope clause), plus the § 2 fallback, plus the 10 GB disk floor, plus the line I asked for recording that the medium-change clause **fired at R-C7-0 and was discharged by Matt's word**. It also adds a clause I did not ask for and that is the right instinct — *"a JUDGE/A-B packet whose arm A trace is not byte-identical to BL-1a-r1's → stop and diagnose before Matt looks"* — which is BLOCK-B's evidence-parity concern made mechanical. The experiment definition is correctly localised to this run (an A/B arm or an E3 skill lap).

**BLOCK-B — DISCHARGED, all three sentences.** § 2.1 now enumerates **four admissible verdicts** (A / B / **HYBRID** / NEITHER) and says what each means for the decisions-log proposal, with HYBRID named as a legitimate win for both routes rather than something to be discovered post-verdict. Evidence parity is discharged as **a recorded decision, not an accident** — the route I explicitly left open: arm A is not pre-packed, and the reason is given (R-C5-74, Matt's own *"the painted tar pool with licks and scorch LANDS — accepted as rendered"*; BL-1a-r1 changed numbers only), with *"if Matt asks for a taste round on A before ruling, it is granted before the verdict, not after."* That is a better discharge than the pre-pack I suggested, because it keeps the asymmetry visible to the person ruling. (a)–(e) are traced **for both arms before Matt looks**, with (a)/(b) explicitly *re-proved for a flipbook body, not assumed from arm A*.

**BLOCK-C — DISCHARGED, and it went further than I asked.** R-C7-0f (conductor, veto-open) names both missed gates with their numbers and the 2.6× tolerance, names the other seven as passed, states that **R-C7-0c/0d are the commitment-boundary ratification** that disposes of the two-clip kill rule, and records the aspect miss as a bind-side conductor disposition. Beyond the minimum: the aspect was **actually re-measured** on the cut frames — scorch bbox 365 × 228 = **0.62, inside the 0.58 ± 0.05 band** — and is re-measured again on the bound flipbook at BL-2v. The STATUS line now reads *"it missed two of its nine pre-registered gates … and survives on R-C7-0c/0d, a commitment-boundary ratification, not on the gate sheet."* `grep` over the charter for *"passes its pre-registered gates"* returns nothing. R-C7-0b retains its original wording, which is correct append-only ledger practice — the correction is a row, not an erasure.

### 7.2 WARN dispositions

| # | status | note |
|---|---|---|
| WARN-1 | **OPEN — deferred by design, accepted** | Ledger `charter_sha256_12` is still `4e8185d424d7`; restamp is R-C7-1 at GO. **One clause to add:** the restamp target is **`419cc6c04e97`**, not the `8892ada80395` I reviewed — the document self-labels **v1.0 across two distinct shas**, so the attribution line should name all three (`4e8185d424d7` v0.1 → `8892ada80395` v1.0 as Gate-1'd → `419cc6c04e97` v1.0 as discharged), or the Gate-1 BLOCKs and R-C7-0f end up attributed to a sha that no longer resolves — the same #73 shape WARN-1 was raised for. |
| WARN-2 | DISCHARGED | § 1 strikes F6-bis and marks it `RULED by Matt R-C5-125 … against the conductor's lean`. § 4 F2 carries the order ruling. |
| WARN-3 | **OPEN — re-scoped, not cleared.** See 7.3. | The one-number rule removes the *conflict* but asserts a quantity-class that contradicts its source. |
| WARN-4 | DISCHARGED | § 1 maps `Q80 F4 = charter F1` and `Q80 F5 = charter F3` explicitly; § 4's F1 row carries `(= Q80 F4)` inline. F3's row lacks the inline tag but the § 1 mapping is unambiguous. |
| WARN-5 | DISCHARGED | STATUS names **V7 amended** for the trial (*"the clip ships as a flipbook field body"*) with V15 untouched **and the reason given** — arm B is a field, not a burst. Correct on both verdicts. |
| WARN-6 | DISCHARGED | The class-E rule is a § 1 substrate row rather than § 5 — better placement than I proposed, since it sits with the pins a fresh conductor reads first. Carries the enforcement hook (`grok_calls[].still` must point under `runs/C-7/artifacts/`). |
| WARN-7 | DISCHARGED, residual | Totals stated (`764 pass / 17 red / 3 error`). **Residual:** the enumeration sums to **21** (5 standing + 1 E3-r1 + 12 stale-value + 3 Blackwater) against *"20 named"* = 17 + 3. Inherited from R-C5-139's own wording, not introduced here. Resolve at C-7's first suite run; it will resolve itself the moment anyone diffs. |
| WARN-8 | DISCHARGED, above the bar | § 1 gives a **cause** (receipt path absent after Matt's disk purge, `~/astra-burst/runs/C-5/FL-6d*` — not the build), not merely a disposition, and **re-owns the lap as BL-2w** after the A/B. |
| WARN-9 | DISCHARGED | § 5 now states the half that binds C-7: `heavy_lock.py` over every TOOLING burst / suite / headless Godot, `c5_c7_*.log` naming so C-6's glob sees a C-7 WAVE START/DONE, and freeze announcement to `runs/FREEZE_NOTICES.md`. Both files verified present; `FREEZE_NOTICES.md` already carries its first row and cites C-6 § 7.7 by number. |
| WARN-10 | DISCHARGED | R-C7-0f records the lineage **per version with what each version's numbers mean**: v1 = clip 1's `plate 0.49 / drift 0.35` as a green-key + flames-in-footprint **artefact** (so explicitly not comparable to clip 2's), v2 = hue key + pool-only footprint + `stable_from`, **both clips re-measured under v2**, v3 = the O1 fix. `bw_cut.py` sha12 `09086010aeb4` in `N-C7-instruments` matches the file on disk. The O1 defect is **fixed, not deferred** — better than the "owed before the next measured clip" I asked for. |
| WARN-11 | DISCHARGED | § 5: **C-6 has right of way** with the reason (its lap is clip-bound, C-7's is not), C-7 self-caps at 6 for the Blackwater lap (2 used), an F5 lap sets its own cap when ruled, and an out-of-budget reply is an external-state HALT — wired into § 7's rate-limit clause. |
| INFO-3 / INFO-4 | OPEN, non-blocking | § 4 still has no one-line fork-gating statement; (f) is not named a reserved ratification point. Both remain INFO. |

### 7.3 WARN-3 re-scoped — the one-number rule fixes the conflict by changing 220's quantity-class, and the arithmetic does not survive it

§ 1 now reads *"ONE number: 220 px = the measured pre-1.4 dome **diameter** 3.4 BH; Q80's '≈200' was a rounded radius guess and is withdrawn."* Q80 F5's own text reads *"a filled golden dome **3.4–3.6 BH wide** … the original **220 px radius** matched"*, and recommends *"1.5 BH radius (≈ 200 px)"*.

Q80 is internally consistent **only** if 220 is a radius: a 3.4 BH-wide dome ⇒ 1 BH ≈ 440/3.4 ≈ **129 px** ⇒ a 1.5 BH radius ≈ **194 px ≈ "≈200"**. Under the charter's re-classification (220 px = 3.4 BH **diameter** ⇒ 1 BH ≈ 64.7 px), a 1.5 BH radius is ≈ **97 px**, and Q80's own "≈200 px" becomes not a rounded guess but arithmetically impossible. So the withdrawal rests on a reading that makes its source incoherent rather than imprecise. The stake is **2× the effect's on-screen size** (220 px wide vs 440 px wide), and § 4's fork row is still titled *"Healing Hands radius"* while § 1 defines the number as a diameter — the same ambiguity WARN-3 named, one level down.

**Not blocking:** F3 gates Healing Hands, which sits behind the R-C5-125 PAUSE; P1 is untouched. **Discharge (one line, at R-C7-1 or when F3 goes to Matt):** state 220 px with its quantity-class **and** the BH-per-px scale it implies, and say which of the two readings of Q80 F5 the conductor is adopting. If 220 is a diameter, Q80's ≈200 needs re-deriving before Matt rules; if it is a radius, the two numbers are 194 vs 220 and the fork is live exactly as Q80 framed it.

### 7.4 New this pass

**WARN-12 (new) — a Matt word is quoted in the charter and is not in the ledger.** The title and STATUS line carry *"Fire lane: Matt cleared it 2026-09-18 (**"wasn't super happy with the result"** — see fork F5)"*. `grep -c "super happy"` over `runs/C-7/ledger.json` returns **0**; there is no `R-C7-0g` or equivalent. This is material, not cosmetic: R-C7-0's conductor default sets *"bind = one TOOLING burst AFTER the fire lane clears"*, so this word is **the precondition that releases P1**, and it is also the motivation for fork F5 — which § 4 still lists as open with a recommendation. Every other Matt word in this run is ledgered with its class (R-C7-0/0c/0d/0e), which is why this one stands out. Principle 4 (decisions-log as truth), #73. Note also that *"cleared"* does double duty — the lane's hold on the bind released, vs Matt being dissatisfied with v44's result; the ledger row should say which. **Discharge:** one `class: matt`, `veto_open: false` row carrying the verbatim word, its date, and what it released.

**WARN-13 (new) — `wave.sh` hardcodes an ephemeral, session-scoped scratchpad path, and the conductor is by charter a different session.** Line 4 of `runs/C-7/conductor_scripts/wave.sh` pins `S=/private/tmp/claude-501/…/4e83a458-9b8a-45f0-8e0c-8487cc714a21/scratchpad`, and every wave log, `*_run.json` and `*_run.err` is written there. That directory is **per-session and reaped**; the charter's STATUS line hands the run to *"a fresh gandalf session"*, whose scratchpad has a different UUID. Committed TOOLING that points at the authoring session's private temp directory will either write into a dead session's tree or fail outright — and § 5 (2)'s `c5_c7_*.log` visibility to C-6 depends on those logs existing where C-6 looks. **Discharge:** derive `S` at runtime (`${CLAUDE_SCRATCHPAD:-...}`, or a run-owned `runs/C-7/logs/`), or state in § 5 that the conductor re-points line 4 at first use. One line either way; cheaper now than at the first wave.

**INFO-R3 — § 7 is placed physically before § 6 in the file.** Cosmetic; noted only because a fresh conductor scanning for "the last section" will land on the C-5 close-out and may not scroll back up to the HALTs. Renumber or move when the charter is next touched.

### 7.5 Re-check action summary

**gandalf, at R-C7-1 (none blocking P1):**
- [ ] WARN-1 — restamp `charter_sha256_12` to **`419cc6c04e97`**; attribution line names all three shas and which rulings were made under which.
- [ ] WARN-12 — ledger the fire-lane Matt word as a `matt` row; say what it released.
- [ ] WARN-13 — un-hardcode `wave.sh`'s scratchpad path (or record that the conductor re-points it).
- [ ] WARN-3 — before F3 goes to Matt: 220 px with its quantity-class and implied BH scale, and which reading of Q80 F5 is adopted.
- [ ] WARN-7 residual (21 vs 20) · INFO-3 fork-gating line · INFO-4 name (f) a reserved ratification point · INFO-R3 section order.

**Matt — unchanged from § 5:** the four fork letters (F1/F3/F4/F5) and the Grok allowance, the latter now mitigated by C-7's self-declared right-of-way to C-6 and its 6-clip cap. **Read WARN-3 / § 7.3 before ruling F3.**

**ADR-002:** all re-check items are charter wording, ledger record correction, and within-run conductor tooling — **mine to approve, and I approve them on execution.** No new ADR, no cross-seam schema change. The decisions-log proposal that follows a B or HYBRID verdict remains a Matt ratification routed to me for the entry, per § 2.1 as written.

**Re-check verdict: PASS-WITH-WARNS — GO.** The three BLOCKs closed in one pass, two of them beyond the minimum: the aspect miss was re-measured rather than asserted, and the O1 instrument was fixed rather than merely owed. The remaining items are a deferred restamp, one unledgered Matt word, one path in a script, and a units question on a fork that sits behind a PAUSE.

**Re-check references**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-17-vfx-run-C-7-charter.md` (`419cc6c04e97`, 55 lines)
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/ledger.json` (R-C7-0…0f; `N-C7-instruments`; `charter_sha256_12` still `4e8185d424d7`)
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/FREEZE_NOTICES.md`
- `/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py` · `wave.sh` · `bw_cut.py` (`09086010aeb4`)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-15-vfx-run-C-5-charter.md` § 8 (seven clauses, checked one-for-one)
- `/Users/admin/Games/reincarnated-collaboration/canonical/matt_decision_needed/2026-09-16-c5-e3-deployment-fit-zeus-healing-hands.md` F5 (the 220 / ≈200 arithmetic)
