# PROPOSAL — Replace the TRUE-SOURCES founding evidence

**Author:** gandalf (CANON-STEWARD / DRIFT-CRITIC)
**Date:** 2026-07-24
**Status:** ✓ **RULED REFRAME (Matt, 2026-07-24)** — text sites (§ 5a) EXECUTED same session;
disciplines D-a/D-b (§ 5b) + the TSR-4 coverage tier (§ 5c) routed to jack-ryan for
ratification at `agentic_orchestration/qa/pending/2026-07-24-gandalf-true-sources-reframe-ratification.md`.
BROADEN (§ 6) parked for its own charter.

**Post-ruling addendum — a second worked example, ours.** The Edition-II diff found that our
own Edition-I freeze silently omitted `survivalmode2/resources/text_en.arc` (case-sensitive
`find`), while its 11/11 SHA-256 verification passed cleanly — a value-level check blind to a
missing population, committed in the same session this proposal was drafted. Left unrepaired
and annotated as the discipline's best evidence. See
`2026-07-24-gd-edition-I-freeze-fingerprint.md` § 5 and `2026-07-24-gd-edition-II-cut-record.md` § 5.
**Evidence:** `agentic_orchestration/research/knowledge/gd/2026-07-24-rank-array-adjudication.md` (legolas)
**Trigger:** Matt asked whether grimtools had simply been updated for the new DLC ahead of us.

---

## 1. The verdict

The founding claim is **false**, and was false in a more interesting way than I guessed.

**Current canon (paraphrased):** *"grimtools' community-harvested 60-rank arrays contradict
the `.arz`'s actual 26 ranks, and nobody noticed until a primary source was consulted."*

**What is actually true**, established byte-level by legolas:

- `all_skills.js` contains **exclusively** `nonplayerskills/` monster records plus item and
  component skills. **Player class records are entirely absent.** FoI's tag
  `tagGDX1Class07SkillName04A` appears zero times.
- `sk296` **byte-matches** `records/skills/nonplayerskills/bossskills/banegargoth_fireballnovabarrage.dbr`
  (`offensiveFireMin` first five 57, 83, 111, 140, 170; last five 2106, 2149, 2191, 2234, 2276).
  It is a boss ring-projectile skill. It was never Flames of Ignaffar.
- Monster copies genuinely carry `skillMaxLevel=60` **in the `.arz` itself**. Blade Arc's
  nonplayer copy `ironmaiden_bladearc1.dbr` scales monotonically to rank 60 with no plateau.
  The 60-element arrays are correct.
- **grimtools was accurate for every record it contains.** There was no data-quality failure.

**My own correction hypothesis was also wrong.** I proposed the 60s were UI padding to
gear-overcap length. They are not padding; they are authored 60-rank monster scaling tables.
I asked legolas to try to break that hypothesis and he broke it. Recorded because a
correction that quietly replaces one unverified inference with another is not a correction.

**Replacement sentence (legolas's, which I endorse as written):**

> The grimtools `all_skills.js` harvest contains exclusively nonplayer/monster skill records;
> player class skills are entirely absent from that payload. The `.arz` is the sole source
> for player skill data including true rank caps, rank arrays, cone geometry, and cast
> cadence. grimtools' 60-element arrays are correct for the monster records they represent;
> the discrepancy is a namespace mismatch, not a data-quality failure in the secondary source.

## 2. Why the corrected story is a STRONGER argument, not a weaker one

The instinct is to read this as "the program's justification collapsed." It didn't. It got
sharper, and it now names a hazard we are genuinely undefended against.

**Old hazard: secondary sources carry wrong values.** Detectable. Any cross-check surfaces
it. Our TSR-4 tier-3 sampled community-calculator spot-checks are built precisely for it.

**Real hazard: secondary sources have undocumented coverage boundaries.** *Undetectable by
any value-level check.* You cannot tell from a payload what it does not contain. Every row
you sample is correct. Every assert passes. You conclude the source is reliable — and it is
reliable, and simultaneously structurally incapable of answering your question.

That is strictly worse than wrong values, because wrong values announce themselves and
missing populations do not.

**And this exposes a real architectural gap.** TSR-4's three tiers — family anchors, in-pipe
mechanical asserts on every row, sampled community-calculator spot-checks — are **all
value-level**. Not one of them detects a coverage gap. Run all three against grimtools and
it passes cleanly while containing no player skills whatsoever.

So the primary-source argument survives, with a better warrant: **you need the primary source
not because secondaries lie, but because only the primary source reveals the shape of the
whole population.** grimtools cannot tell you player skills are missing. Only the `.arz` can.

## 3. The methodological failure, named precisely

The error was not bad data. It was **an unvalidated join read as a contradiction.**

Two records from two sources were compared without ever establishing that they were the same
record. Different display tags, different namespaces, different source archives, different
skill classes. Identity was assumed on the basis of "both are GD fire skills." That is not a
join key; it is a resemblance.

Once identity is unestablished, a value difference is not evidence of error in either source.
It is evidence that you are comparing populations, not records.

## 4. The uncomfortable part — the guard is mis-sited

The non-improvisation law was written **today**, for the cheap crawler, on the theory that
cheap models improvise and produce plausible wrong rows. I wrote it. Its stated justification
was this very grimtools story.

But the improvisation that actually occurred — *"these numbers differ, therefore the community
source is wrong"* — was performed by **expensive analysis**, not by a cheap crawler. The guard
was installed on the lane that hadn't failed.

I still think the law is right, and it would in fact have helped: a crawler told "expect 26"
and finding 60 would HALT, and that HALT surfaces the namespace question immediately. But the
law's real value is not "cheap models are careless." It is that **the law converts ambiguity
into escalation instead of into inference** — and that is valuable at *every* price point.

Three instances of the same error shape appeared in this thread alone:

| # | Inference | Outcome |
|---|---|---|
| 1 | *numbers differ → the secondary source is wrong* (original analyst) | **Banked as canon. Wrong.** |
| 2 | *2,888 skills at exactly 60 → it must be padding* (gandalf) | Routed to verification. Wrong, caught in ~20 min. |
| 3 | *grimtools may have updated ahead of us* (Matt) | Offered as hypothesis. Excluded on timestamps. |

All three were reasonable inferences from partial evidence. **The difference between the
failure and the two successes was not intelligence, model tier, or care. It was whether the
inference was banked or routed.** That is the finding worth keeping from this whole episode.

## 5. Proposed changes

### 5a. Three text sites (mechanical, once scope is ruled)

1. **`.claude/agents/legolas-crawler.md`** — "Why this law exists, in one sentence" currently
   cites the false story. Replace with the coverage-boundary framing plus the
   ambiguity-into-escalation rationale.
2. **`agentic_orchestration/AGENTS.md`** — the known/unknown split paragraph ends on the
   grimtools-60-vs-26 contradiction. Same replacement.
3. **TSR-3 in the rulings ledger** (`agentic_orchestration/gandalf/notes/2026-07-23-true-sources-grill-brief.md` § 4)
   — annotate with the corrected evidence. **Do not delete the original.** The error and its
   correction are both part of the record, and a ledger that silently self-heals cannot be
   audited.

### 5b. Two proposed disciplines (the substantive part)

- **D-a — Coverage-boundary declaration.** Every secondary or harvested source must carry an
  explicit, *verified* statement of the population it covers before any row from it is
  compared to anything. "What's in it" is insufficient; the required field is "what isn't."
- **D-b — Join validation before contradiction.** A value difference between two sources is
  not evidence of error until record identity is independently established. Establish the
  join, or you are comparing populations.

### 5c. One proposed architecture change

- **TSR-4 gains a coverage tier.** Tiers 1–3 are value-level and cannot detect a missing
  population. Add a tier that asserts the records a lane *requires* are actually present in
  the source, and that the source's namespace matches the question being asked. Design is
  elrond's; the requirement is this proposal's.

## 6. Scope options for Matt

- **NARROW** — fix the three text sites, change nothing else. Cheapest. Leaves the coverage
  hazard undefended and TSR-4 still blind to it.
- **REFRAME** *(gandalf lean)* — text sites + D-a + D-b + the TSR-4 coverage tier. Treats the
  episode as having taught us the actual hazard, and defends against it.
- **BROADEN** — REFRAME plus re-audit every existing lane (PoE1/PoE2, D2, LE) for undeclared
  coverage boundaries. Correct in principle; it is a real work item, not a doc edit, and I'd
  rather it be scheduled deliberately than smuggled in under a canon fix.

**My lean is REFRAME, with BROADEN queued rather than dropped.** The re-audit is the right
instinct — if grimtools' coverage boundary went unnoticed, others plausibly have too — but it
should be its own run with its own gates, not a tail appended to this one.

## 7. Ratification

gandalf proposes; Matt rules scope; jack-ryan ratifies into decisions-log and
engineering-disciplines. gandalf executes the text changes after the ruling.
