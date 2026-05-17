# Notice to knight-rider — roadmap doc structurally split

**From:** gandalf
**To:** knight-rider
**Date:** 2026-05-16 (Day 4, evening)
**Type:** Informational notice — no action required beyond awareness propagation
**Authorized by:** Matt directly ("yes restructure the roadmap now")

---

## TL;DR

`canonical/16-project-roadmap.md` was structurally split into three docs this session. **Forward-looking content stays at `16`; shipped history moved to `16a`; restructure meta-history captured in `16b`.** All three are uncommitted in working tree pending Matt review.

**What you need to know:**

1. **`canonical/16-project-roadmap.md`** is now ~360 lines (was 847) — forward-looking only. Use this for orientation, decision-loop staging, and dispatch authoring.
2. **`canonical/16a-roadmap-shipped-log.md`** — historical shipped record + closed/locked decisions reference. Append-only by convention. Reference when answering "is this decision settled?" or "when did X ship?".
3. **`canonical/16b-roadmap-archive-restructures.md`** — meta-history of restructures. Rarely consulted; preserves audit trail.

---

## Why this happened

Matt opened this session saying the roadmap was "bloated and disorganized" and that he couldn't make heads or tails of current state. I confirmed: 847 lines, mixed strategic anchor + per-stage detail + per-item commit logs + risk sections + interleaved playtest notes + retrofit annotations (*"PROMOTED 2026-05-16"*, *"split 2026-05-16"*, etc.). Forward planning competed for attention against historical record.

Decision: split. Matt authorized; gandalf executed.

---

## Where things live now (migration map)

| Looking for... | Go to... |
|---|---|
| What VS2a / VS2b need to ship | `16` § VS2a, § VS2b |
| Status snapshot of where everything is | `16` § "Where we are right now" |
| Open design decisions blocking next dispatches | `16` § "Open design decisions" — organized by what they block |
| What shipped today / this week | `16a` § Stage A2 sub-shipped log |
| Stage A1 detail (D1 rubric, B6 templates, A4 lock) | `16a` § Stage A1 |
| Stage A3-A7 forward scope tables | `16a` § "Stage detail (forward reference)" |
| Closed/locked decisions reference (incl. 2026-05-16 cluster) | `16a` § "Closed/locked decisions reference" |
| Memory cross-references | `16a` § "Memory cross-references" |
| Track A landing rhythm / single-season rule / refactor-vs-rewrite | `16` (kept; condensed) |
| Why a stage moved or got renumbered | `16b` |

For full migration map: see `16b` § "2026-05-16 (Day 4) — Three-doc split."

---

## What this changes for your work

**Nothing operationally.** Dispatch authoring, Gate-1 commissions, decisions-log drafts all continue. But:

1. **When you cite the roadmap in a dispatch, link to `16` for forward state and `16a` for shipped/closed decisions.** Both are at the same `canonical/` level; cross-link freely.
2. **When sub-items ship, append them to `16a` § Stage A2 sub-shipped log** rather than retrofitting `16`. Forward-looking `16` updates when a milestone closes or scope shifts, not on every sub-item.
3. **When you draft a decisions-log entry for a locked design position, the lock should appear in `16a` § "Closed/locked decisions reference"** as well as the decisions-log itself. I'll do that pass; you don't need to.
4. **First-invocation onboarding for new agents** — the AGENTS.md required-reading should still cite `canonical/16-project-roadmap.md` (same path; just trimmer now). No agent definition changes needed.

---

## What this does NOT change

- Stewardship locked: gandalf owns forward-looking `16`; appends to `16a`; appends to `16b` on restructures.
- Decisions-log authority unchanged (knight-rider drafts; Matt approves; jack-ryan reviews).
- File 28 (engine queue), file 29 (strategic anchor), file 32/33 (progression), canonical/story/* (L2 cosmology) all untouched.
- All paths preserved; no link rot expected from agents that previously referenced `canonical/16-project-roadmap.md`.

---

## Propagation request

Please surface this split in your next handoff doc (skill_handoff_2026-05-17 or equivalent) so other specialists notice the new layout on first invocation. Cheap one-line callout: *"`canonical/16-project-roadmap.md` is now forward-looking only; historical content in `16a` and `16b`."*

Otherwise — no action. Three docs are sitting uncommitted; Matt is reviewing before commit authorization.

— gandalf
