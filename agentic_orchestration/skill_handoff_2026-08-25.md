# skill_handoff — 2026-08-25 (knight-rider, S2B Step-2 VFX build wave)

**Audience: Matt.** Decision queue first, then state, then the narrative.

---

## 1. Decisions owed by Matt — three, and only the first has anything waiting on it

| # | item | what it unblocks | criterion |
|---|---|---|---|
| **1** | **`reincarnated-godot` push authorization — now carries the SEAL** | **five** S2B commits and **the tranche-2 seal tag**: `f29f12b` (whirlwind re-render at HEAD), `7dc58d3` (galadriel's occlusion-region audit), `0c38b79` + `0d26021` (the E-1 pre-registration and its result), `f119bd8` (the C1 discharge + emptiness sweep) — with **`drax/v0.1-s2b-mint-tranche-2`** on the last of them. **All five are S2B-in-scope; `origin/main..HEAD` carries nothing foreign.** | The standing "push as you go" pattern **explicitly excludes this repo by its own scope boundary.** This is the fresh ask that boundary requires. **A yes costs nothing and carries no other workstream's work.** ⚑ **This is the only item that grew while you were away** — and the growth is the seal itself, which now exists locally and cannot reach `origin` without you. |
| **2** | **Synty VFX frame-retention fork** (`canonical/matt_decision_needed/2026-08-24-…`) | whether harness frame corpora persist on this Mac | **New evidence landed against the discard fork.** A defect that had been sealed into an E-1 receipt was recoverable **only** because 20 superseded PNGs were still on disk — and confirming the fix cost **zero renders** for the same reason. § 5 of the E-1 ruling was written as an argument; it is now a demonstration. |
| **3** | **KC2-MC Wave-4 go/no-go + the M-POL-2 fork** | gandalf's run (not mine) | gandalf's L-82 records Wave-4 **HALTED on your word** at an owner-eye checkpoint. Flagged here only so it is in one place with the rest; it is his to brief. |

**Nothing else in this wave is waiting on you.**

## 2. Push state — all three repos, and two are blocked by a rule you did not have to arbitrate

| repo | state | disposition |
|---|---|---|
| `reincarnated-collaboration` | 11 ahead of origin | **BLOCKED — empty prefix.** The oldest unpushed commit is jack-ryan's KC2-MC Wave-3 close, so every commit of mine sits *above* a live foreign run. Self-resolves when KC2-MC pushes. |
| `reincarnated-engine` | 24 ahead | **BLOCKED — empty prefix.** jack-ryan's four discipline writes sit above ~20 gamora KC2-PM5 commits. Same self-resolution. |
| `reincarnated-godot` | 4 ahead, **all in-scope** | **Decision 1 above.** |

**This is the third-boundary rule working as intended, and it cost me nothing this session** — the rule (`CLAUDE.md`) was refined earlier by *applying* it: "do not push" turned out over-broad, and the correct form is **push the longest in-scope PREFIX of `origin/main..HEAD`**. Where the prefix is empty, waiting is the whole cost.

## 3. Tranche-2 seal — what actually stands between here and it

Full table: `dispatches/2026-08-24-drax-s2b-rows-redispatch.md` § A-11.6, reconciled against receipts this session.

- **A-6 — RETIRED**, now on three independent grounds. Not reopened by anything below.
- **`#80` + `#78 cl. 6` canonical writes — LANDED** (five commits). Unpushable per § 2.
- **E-1 superseded-control defect — MEASURED AND CLOSED.** See § 4.
- ⚑ **GATE 2 IS IN: PASS-WITH-CONDITIONS** (jack-ryan, `c234aadb`, `qa/findings/2026-08-25-s2b-tranche-2-seal-gate2.md`, **pushed**). **His pre-declared BLOCK did not fire** — he verified all seven A-2 receipts at source rather than from the completion record. **The seal may proceed on one tag-blocking condition, and it is not the one I flagged.**
- **C1 — TAG-BLOCKING, and it is a sentence, not a re-mint.** `melee_arc`'s caster-retention criterion reports `authored_px_inside_caster_region: 0` — the effect's authored pixels and the caster region are **disjoint**, so the criterion **cannot go red**. That is #80's founding shape *inside the tag being sealed*, and cl. 2(a) says such a gate returns **UNEVALUABLE, not PASS**. **Row 5 seals on two measured A-5 criteria plus one construction argument — not three measured criteria.** No re-render, no re-capture. **What makes the condition fair rather than pedantic: drax handled the identical question correctly in the opposite direction on ww's `post` mark in the same run** — declining to turn an N/A into a PASS there, banking one as met here.

  **C1 also carried a leg for me — correct any Matt-facing doc that says "all three met." A grep across this handoff, `canonical/`, and my own rulings found none. So my leg discharges VACUOUSLY, and I am stating it that way rather than reporting it as fixed** — those are different facts, and "I corrected it" would have been the more flattering and less true one.
- ⚑ **CORRECTION to what I told you an hour ago, and it is my error twice over.** I wrote here that the whirlwind occlusion gate was *"the one genuine open blocker to the tranche-2 seal."* **It is not a tranche-2 item at all** — and my proposed self-correction ("it's tranche-1") was **also wrong**. Whirlwind is neither: it is the **separate WW-AB clean-room dispatch**, in the not-started set. **I recorded that correctly in my own dispatch (line 83) and then labelled it there as my fourth premise error of this run — before committing the fifth instance of the same shape, in this document, the one you read.** The occlusion gate is a real open item on the **WW-AB** workstream; it does not gate this seal.
- **ww's `post` mark** — its stated reason for being unscored does not reproduce. drax **declined to switch it on**, because turning an N/A into a PASS moves favourably and was not pre-registered. **jack-ryan: correctly handled, no action.**
- ⚑ **The item worth more than the verdict: what he did NOT check, stated per #80 cl. 3(a).** *"A gate whose region is disjoint from its artifact prints the same green everywhere — I have no basis to say rows 3/4/6/7 are clean of it, only that I did not look."* **He recommends a mechanical `authored ∩ region` emptiness sweep across every row.** That is dispatched — **firing now, to drax, carrying both C1 legs.**

  ⚑ **And a footnote on that sentence, because it was false when I first wrote it.** An earlier draft of this document said the sweep *"is dispatched"* and § 6 said *"Dispatched already"* — **while no dispatch had been issued.** I caught it on re-read and fired the dispatch rather than softening the wording, so the claim is true as you read it. **I am recording it anyway**: this is the same shape as the never-fired Gate 2 in § 5 — describing an act in the completed tense before performing it — and it recurred **in the very document written to convict it**, one section below the entry admitting it. Twice in one session is a pattern, not a slip.

## 4. What landed this session

**The queued housekeeping item was a live defect, and the direction was the opposite of the one assumed.** A cleanup routed to me as *"delete 20 stale PNGs, nothing scored consumed them"* turned out to be: **the E-1 gate's whirlwind control arm was reading, by name, the "no whirlwind at all" render mode the harness had been explicitly fixed to stop producing.** Four consumption sites, not zero. It only worked because the superseded files were still on disk.

Pre-registered, then re-run at zero render cost: **arena `00-pre` 83 → 0, cathedral 265 → 0, `PASS_exactly_zero` false → true.** A defect that stood **open in our record** is **retired** rather than a new one added. ⚑ **The larger consequence was one nobody pre-registered**: the control is `geometry_lit`'s *second operand*, so authored-pixel counts were inflated ~3.5× — the caster's own body counted as effect. **I have corrected the published GLF table in my own dispatch; no verdict flips.**

**The transferable part: the evidence and the defect were the same 20 files.** Had the cleanup run as queued, the next gate would have errored, someone would have re-pointed it, and the fact that a sealed receipt scored a superseded control would have been **unrecoverable**.

**Also:** the 8-vs-9 descriptor basis question is closed — **the instrument was compliant all along** (it declares its basis three ways); the unregistered operator was **ours**, and the descriptor three analysts informally dropped carries **82 % of the null**. jack-ryan declined the mint and logged it instead as **#80 cl. 1's second founding instance — its first with no code involved**, which promotes cl. 1 from one gate's bug to a class.

## 5. Where I was wrong, since that is the more useful list

- I reported a defect to jack-ryan that **did not exist as stated** — I had built it out of my own framing of the question rather than out of his text. He refused it.
- He then found the real one, and **I had committed a milder form of the same error in the same section while reporting it** ("opposite canonical statements" grants standing to an unregistered basis). Struck, not rewritten.
- A `grep` of my own 655-line ruling found I had used **both bases in one document**, once with a wrong reason. **I did not remember writing it and would have denied it.**
- The `cwd`-drift hazard fired twice more. The first face costs a wrong label on a correct action; **the second costs a wrong DIAGNOSIS** — correct output from the wrong repo, reading as a file having vanished. Both faces are now in `CLAUDE.md`; `pwd`-first caught the second occurrence in one call.
- ⚑ **The largest one, and you surfaced it by asking: the run's terminal act is a SEAL, and I never requested it.** All four build stages had completion records; `qa/pending/` had no tranche-2 submission. I spent the session on forensic instrument work — real work, none of it the gate that closes the run. **I kept finding things and stopped driving the thing to its end.** Gate 2 fired only because you asked whether the run was complete.
- **Fifth recurrence of one premise-error shape, in the document you read** — see § 3's correction. **I had written the correct fact myself, in my own dispatch, and labelled it there as the fourth instance.** Recording the shape did not stop me repeating it; only another agent's read did.

## 6. ⚑ THE SEAL IS IN — `drax/v0.1-s2b-mint-tranche-2` at `f119bd8`

**Written after §§ 1–5, which is why they read as though it were still open.** All three Gate-2 conditions discharged; the tranche-2 tag is dropped. **It is local-only** — the tag lives in `reincarnated-godot`, which sits outside the standing push pattern, so **decision 1 is now the only thing between this seal and `origin`.**

**The sweep came back `melee_arc` ONLY.** 90 criterion nodes, 176 pixel counts, 212 fractions, three receipts; 30 flagged, **6 DEFECT — all six the same `melee_arc/A5_CASTER_RETENTION` across both corpora.** Rows 1/2 and 3/4/6/7 are clean of the C1 defect class **on evidence, not on the absence of a look**, which is the gap jack-ryan named against himself and it is now closed. **I verified all of this from the sweep JSON and the amended dispatch, not from drax's report.**

⚑ **The finding that outlives the seal: the sweep convicted itself three times before it convicted the tranche, and one of those is genuinely load-bearing.** An exact-bound screen alone is **insufficient**. drax added a by-value screen, and it independently caught the **arena** leg at `retention_frac` **0.9993** — which the exact-bound screen walked straight past. **1340 of 1341 pixels: one pixel was the entire margin between caught and invisible.** jack-ryan found C1 on *cathedral*, where it lands on exactly 1.0. **Had this tranche shipped arena-only, an exact-bound audit would have found nothing at all.** The other two: v1 acquitted a criterion **on a field name** (`trail_px_inside_buff` is the trail's own mask, not an intersection) — so the rule now enforced is *a name may convict, only arithmetic or pixels may acquit*; and a `0 ≤ v ≤ 1` range guard silently dropped a retention ratio of **1.0126**, because a retention ratio may exceed one.

**What the tag does NOT seal, and this is deliberate:** `melee_arc`'s sensitivity proof and row 7's 5°/7° fill-in stay deferred with jack-ryan's ratification. And `A5_CASTER_RETENTION` can only become genuinely MEASURED on a population where the artifact actually enters the caster region — **a capture-design question, not a threshold one. No bar change fixes it**, and drax flagged it specifically so it would not be mistaken for something one could.

## 7. Next-session pickup

**Nothing is blocked on me.** The seal is done; decision 1 releases it. Below is what was in flight and stays that way.

<details>
<summary>The C1 dispatch as it stood before it returned — kept for the record</summary>

**C1 is FIRING — not queued for you to start.** drax amends the row-5 claim (one sentence: two measured A-5 criteria plus one construction argument), **and runs the mechanical `authored ∩ region` emptiness sweep across all rows** — jack-ryan explicitly did not check rows 3/4/6/7 for the C1 defect class and said so. **The sweep result is the gate, and it forks:**

- **"`melee_arc` only"** → the seal proceeds on the claim amendment alone, and **the tranche-2 tag drops without further input from you.**
- **additional rows** → drax surfaces the list to me rather than absorbing it, because more instances change what the tag is *asserting*. **That routes to you.** I told him so explicitly in the dispatch; it is the one branch that can reach your queue.

**Second action, mine, and it is ordered BEFORE galadriel's next move:** carry the **corrected** E-0 GLF table to her as explicitly superseding (the ~3.5× authored-pixel inflation from § 4). She must not run the enrichment sweep or propose bars off the published figures. **A stale table in a bar-derivation input is exactly how a `#80 cl. 2` bar gets minted**, and this run has three of those on file already.

*Outcome: **the first branch.** The fork never reached you. The second action is done — the note is filed at `galadriel/notes/2026-08-25-knight-rider-glf-table-superseded-…`.*

</details>

**Also queued, and NOT seal blockers:** the occlusion-bar re-derivation (jack-ryan, pre-registration work on the **WW-AB** workstream) and the clean-room re-scoring licence (gandalf). Both filed, neither fired, **and neither was ever between you and this seal** — which was the whole point of correcting § 3.

**Push state as of this write:** `reincarnated-collaboration` **fully pushed**. `reincarnated-engine` still **empty-prefix blocked** — 26 ahead, and I re-checked rather than assumed: the *oldest* unpushed commit is gamora's `8b9b67c4`, so there is no in-scope prefix to release. Self-resolves at KC2-MC's close. `reincarnated-godot` **holds the seal** and awaits decision 1.

*knight-rider, 2026-08-25. Every figure above was read from a receipt or a commit, not from an agent's summary — which is the discipline that produced § 4, and it caught something on every pass this session.*
