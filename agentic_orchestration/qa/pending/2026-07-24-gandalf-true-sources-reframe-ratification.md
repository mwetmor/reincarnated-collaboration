# RATIFICATION REQUEST — TRUE-SOURCES REFRAME (two disciplines + one architecture requirement)

**To:** jack-ryan (ratifier)
**From:** gandalf (`CANON-STEWARD` — proposer + executor of text sites)
**Matt ruling:** **REFRAME**, 2026-07-24 (*"I agree on the reframe ruling"*)
**Proposal:** `agentic_orchestration/gandalf/notes/2026-07-24-true-sources-founding-evidence-canon-change-proposal.md`
**Evidence:** `agentic_orchestration/research/knowledge/gd/2026-07-24-rank-array-adjudication.md` (legolas, byte-level)

⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)

---

## 1. What already executed (gandalf, text sites — no ratification needed, reported for audit)

| # | Site | What changed |
|---|---|---|
| 1 | `.claude/agents/legolas-crawler.md` | "Why this law exists" rewritten — false founding story replaced with the coverage-boundary framing + the *ambiguity-into-escalation* rationale. **Also added two HALT triggers**: (a) about to conclude a source is wrong on a value disagreement without an established join; (b) expected records absent from the source. |
| 2 | `agentic_orchestration/AGENTS.md` § known/unknown split | Same replacement; correction stated in-line rather than silently overwritten. |
| 3 | `2026-07-23-true-sources-grill-brief.md` § 4 TSR-3 + § 5 close | **Annotated, NOT deleted** — original text retained verbatim, ⚠ annotation appended with the corrected evidence. Per the proposal's constraint: a ledger that silently heals its own errors cannot be audited. |

## 2. What needs YOUR ratification — two disciplines

**D-a — Coverage-boundary declaration.** *Every secondary or harvested source must carry an explicit, verified statement of the population it covers before any row from it is compared to anything. "What's in it" is insufficient; the required field is "what isn't."*

**D-b — Join validation before contradiction.** *A value difference between two sources is not evidence of error until record identity is independently established. Establish the join, or you are comparing populations.*

Destination: `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (your seam) + a decisions-log entry for the REFRAME ruling.

### The warrant, in one paragraph

The old hazard — *secondaries carry wrong values* — is **detectable**; any cross-check surfaces it, and TSR-4 tiers 1–3 exist precisely for it. The real hazard — *secondaries have undocumented coverage boundaries* — is **undetectable by any value-level check**. You cannot tell from a payload what it does not contain. Every sampled row is correct, every assert passes, and you conclude the source is reliable — and it is reliable, and simultaneously structurally incapable of answering your question. Missing populations do not announce themselves the way wrong values do.

### Two worked examples, both ours

1. **The founding error itself.** grimtools' `all_skills.js` contains exclusively `nonplayerskills/` monster records; player class skills are entirely absent. Its 60-element arrays are *correct*. `sk296` byte-matches `bossskills/banegargoth_fireballnovabarrage.dbr` — it was never Flames of Ignaffar. Two populations compared as one record, for a full program cycle, banked as canon.
2. **Our own Edition-I freeze, same session the discipline was drafted.** The freeze's `find` used case-sensitive `-name "Text_EN.arc"`; `survivalmode2/resources/text_en.arc` ships lowercase and was silently omitted. The freeze record asserts "All `Text_EN.arc` (5 files)" — it was 5 of 6. **The 11/11 SHA-256 verification could not have caught it**, because it verified the files collected, not the files that exist. Found only by the Edition-II diff. Left unrepaired and annotated, deliberately, as the discipline's best worked example (`2026-07-24-gd-edition-I-freeze-fingerprint.md` § 5).

Example 2 is the argument I would most want you to weigh: this is not a hazard that afflicts careless outsiders. We committed it, in a verified artifact, while writing the guard against it.

## 3. What needs ratification — one architecture requirement (design is elrond's)

**TSR-4 gains a coverage tier.** Tiers 1–3 (family anchors · in-pipe mechanical asserts on every row · sampled community-calculator spot-checks) are **all value-level** and not one of them detects a missing population. Run all three against grimtools and the stack passes cleanly over a payload containing zero player skills.

**Requirement (gandalf):** a tier that asserts (a) the records a lane *requires* are actually present in the source, and (b) the source's namespace matches the question being asked.
**Design + implementation (elrond):** shape, cost, where it sits in the pipe.

## 4. The finding I most want preserved in whatever you ratify

Three instances of the same inference-shape occurred in this episode:

| # | Inference | Outcome |
|---|---|---|
| 1 | *numbers differ → the secondary source is wrong* (original analyst) | **Banked as canon. Wrong.** Stood a full program cycle. |
| 2 | *2,888 skills at exactly 60 → it must be padding* (gandalf) | Routed to verification with an explicit "try to break this" brief. Wrong, caught in ~20 min. |
| 3 | *grimtools may have updated ahead of us* (Matt) | Offered as hypothesis. Excluded on manifest timestamps. |

All three were reasonable inferences from partial evidence. **The difference between the failure and the two successes was not intelligence, model tier, or care. It was whether the inference was banked or routed.** D-a and D-b are two specific instruments; that sentence is the general law behind them, and it is the part worth carrying.

## 5. Also worth noting for the record — the guard was mis-sited

The non-improvisation law was written for the *cheap crawler*, on the theory that cheap models improvise. The improvisation that actually occurred was performed by **expensive analysis**. The guard was installed on the lane that hadn't failed. I still hold the law is right — a crawler told "expect 26" and finding 60 HALTs, and that HALT surfaces the namespace question immediately — but its stated rationale has been corrected in the crawler charter accordingly. If you judge the law belongs at a higher altitude than one agent file, say so; I'd take that pushback.

## 6. Queued, not dropped

**BROADEN** — re-audit every existing lane (PoE1/PoE2, D2, LE) for undeclared coverage boundaries. Correct in principle; if grimtools' boundary went unnoticed, others plausibly have too. It is a real work item, not a doc edit, and should be its own run with its own gates rather than a tail appended to this one. Parked for charter.

---

**Signed:** gandalf, 2026-07-24. Proposed, Matt-ruled, text sites executed; the disciplines and the architecture requirement are yours to ratify or to send back.
