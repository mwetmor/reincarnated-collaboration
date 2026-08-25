# skill_handoff — 2026-08-25 (knight-rider, S2B Step-2 VFX build wave)

**Audience: Matt.** Decision queue first, then state, then the narrative.

---

## 1. Decisions owed by Matt — three, and only the first has anything waiting on it

| # | item | what it unblocks | criterion |
|---|---|---|---|
| **1** | **`reincarnated-godot` push authorization** | four S2B commits: `f29f12b` (whirlwind re-render at HEAD), `7dc58d3` (galadriel's occlusion-region audit), `0c38b79` + `0d26021` (the E-1 pre-registration and its result). **All four are S2B-in-scope; `origin/main..HEAD` carries nothing foreign.** | The standing "push as you go" pattern **explicitly excludes this repo by its own scope boundary.** This is the fresh ask that boundary requires. **A yes costs nothing and carries no other workstream's work.** |
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
- ⚑ **The one genuine open blocker: the whirlwind occlusion gate.** galadriel repaired its region definition and **measured that the verdict moves, PASS → FAIL on both corpora** — then **declined to adopt her own repair**, correctly. Her reason: the 20 % bar was calibrated against a denominator that was 99.6 % sky, so **the repaired FAIL is as uninterpretable as the original PASS.** It needs a re-derived bar, derived *before* the repaired number is looked at again — a pre-registration act, routed to jack-ryan — **and** a gandalf ruling on whether a live A/B's clean-room arm may re-score itself post-hoc. **Neither is yours and neither is hers.**
- **New item:** ww's `post` mark. Its stated reason for being unscored does not reproduce. drax **declined to switch it on**, because turning an N/A into a PASS moves favourably and was not pre-registered. Ratified — it gets its own registration or it stays N/A.

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

## 6. Next-session pickup

**First action: check whether KC2-MC has pushed.** If yes, all 35 blocked commits across two repos release with no further arbitration. If no, they wait — nothing degrades.

**Then:** the occlusion-bar re-derivation (jack-ryan) and the clean-room re-scoring licence (gandalf) are the two items between the wave and a tranche-2 seal. Both are filed; neither is fired.

*knight-rider, 2026-08-25. Every figure above was read from a receipt or a commit, not from an agent's summary — which is the discipline that produced § 4, and it caught something on every pass this session.*
