# QA/pending → jack-ryan — I swept 20 files of a live session's staged work into my own commit and pushed it, while running the check that was supposed to prevent exactly that

**Filed:** 2026-08-25 (knight-rider), minutes after the fact, self-reported. **Class:** incident + defective-instruction correction. **Severity:** WARN on the artifact; ⚑ **the instruction defect is the serious part, because I wrote it into two live dispatches.**

---

## What happened

Commit `d7835900`, pushed to `origin/main`. I intended it to carry **one** file — the wave record, recording Matt's push-posture extension. It carried **21**: my one, plus **20 files from a live concurrent legolas session** (`legolas/notes/2026-08-25-kc2-mc-lap-md-b4app-2d/` — decode scripts and Grim Dawn save binaries, file mtimes 11:53–12:02, i.e. minutes old and possibly mid-work).

**My `git add` did not stage them. They were already in the index**, put there by the other session in the shared working tree. My commit swept whatever the index held.

## ⚑ The part that matters: I ran the check. The check could not fire.

My command was, in one chain:

```
git add <one named file> && git diff --cached --name-status && git commit -q -m "…" && git push
```

**The verification ran. It printed all 21 files. And then the commit fired in the same breath**, because it was `&&`-chained to it. I read the 21-file listing *in the same tool result as the push confirmation* — after both were irreversible.

> **A verification step chained to the action it verifies is not a gate. It is a receipt.**
> A gate must be able to REFUSE. `A && B` cannot refuse B on the basis of A's *content* — only on A's exit status, and `git diff` exits 0 whether it lists one file or a thousand.

## ⚑ Why this is not just my mistake: the same defective check is in two live dispatches

I wrote into **3A and 3B**, as folded Gate-1 mandatory **M3**:

> *"Verify `git diff --cached --name-status` against the paths you named, before every commit."*

**drax can satisfy that instruction exactly as I did, and fail exactly as I did.** The wording says *when* to look but not *that the looking must be able to stop the commit* — and the natural way to "verify before every commit" in a scripted agent turn is precisely the `&&` chain that makes it inert. The instruction is **satisfiable without doing anything**, which is the failure signature I have been enforcing against all session (*"acceptance criteria satisfiable without producing the thing the dispatch exists to produce"*). **I shipped it in the check designed to stop that class of error.**

This is materially worse in his context than in mine: he **tags** his commits. `CLAUDE.md` — *"a tag that carries a sibling session's work is a defective seal even when every file in it is correct."* My defect produced a mis-attributed commit; the same defect on his side produces a **defective seal**.

## Corrected instruction (folded into both dispatches; ⚑ **NOT** delivered to the in-flight 3A session — see the addendum)

*(This heading originally read "and sent to the in-flight 3A session." **It was not sent — the send failed for want of the tool, and I wrote the heading before attempting it.** Struck and corrected rather than quietly reworded, because a false claim of a mitigation having been applied is worse than the gap it covers, and worst of all inside an incident record about claims outrunning their referents.)*

> **Staging verification must run as its OWN tool call, whose result you read, BEFORE the call that commits.** Never `&&`-chain `git diff --cached` to `git commit`. If the staged list contains a path you did not name, **unstage it (`git restore --staged <path>`) before committing** — do not commit and explain.
> **Rationale, from a live failure:** the chained form runs, prints, and commits in one breath; you read the evidence after the commit is irreversible. `git diff` exits 0 regardless of content, so `&&` cannot act on what it found.

## Disposition of the artifact — recorded, NOT rewritten

**No history rewrite.** It is pushed to a shared trunk that live sessions are working against; rewriting it to fix an attribution error would trade a recorded, harmless defect for a genuinely destructive one. That trade is not close.

**Assessed harm — deliberately not minimised, but also not inflated:**

- **Content:** legitimate project research artifacts (legolas KC2-MC / MD-B4 decode lap). Not secrets, not credentials. ~100 KB of binaries. They were going to be committed by legolas anyway.
- **Real defect 1 — attribution.** They landed under a knight-rider commit message about push posture, which says nothing about them. Anyone reading the log learns the wrong thing about who did what. (Discipline #11, attribution clarity.)
- **Real defect 2 — timing not chosen by the owner.** legolas's work was committed at a moment they did not pick, possibly mid-decode. Their next commit may now be a confusing partial.
- **Not a defect:** no seal, no tag, no gate verdict rests on `d7835900`.

**Routing:** legolas should be told rather than left to discover it — their next `git status` will be missing 20 files they never committed, which reads as *their* work having vanished. That is the FALSE-ALARM face of the pointer-staleness defect filed separately today, arriving from a different direction. **A wrong surprise costs more than a plain notice.**

## What I would have caught it with

Nothing exotic — **one tool call instead of zero.** The cost of the correct form is a single extra round trip. I skipped it while composing a commit message about the importance of recording postures before acting on them.

**Cross-references:** the fold in 3A/3B § Concurrency posture; `qa/pending/2026-08-25-completion-records-filed-while-headers-still-read-pending.md` (same day, adjacent class); `CLAUDE.md` § 62(a).

---

## ⚑ The in-flight session could NOT be reached — compensating control, named and owned

I attempted to send the corrected instruction to the live 3A session and **`SendMessage` is not available in this session's toolset.** So the correction sits in the dispatch file, which drax read at session start and **may or may not re-read before tagging.** I cannot assume he will.

**I am not treating "it's in the file" as mitigation.** That is precisely the pointer-that-no-longer-points defect filed today from the other direction: an instruction that exists but is not read at the moment it binds.

**Compensating control, which I own and which does not depend on him:**

> **Before requesting Gate-2 on `drax/v0.1-s2c-mint-tranche-3a`, knight-rider verifies the tag's own contents** — `git -C ~/Games/reincarnated-godot show --stat <tag>` and `git diff --name-status` across the tagged range — **against the eight rows the dispatch names.** If the tag carries a path belonging to a sibling session, **the seal request does not go out**; the defect is surfaced and the tag is re-cut before Gate-2 sees it.

This moves the check from "he remembers" to "I verify," which is the consumer-side corollary I argued for this morning in the adjacent filing — applied to myself, at my own cost, on the one occasion today it would have saved me. **The `reincarnated-godot` tree is the lower-risk one for this class anyway** (drax is the only agent working it), but "lower risk" is not the same as checked, and I have already spent today's allowance for treating a plausible premise as a verified one.
