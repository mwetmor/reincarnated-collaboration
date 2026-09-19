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
