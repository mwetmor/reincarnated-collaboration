# Dispatch — 2026-05-16 — jack-ryan — decisions-log reconciliation + Gate 1

**From:** knight-rider
**To:** jack-ryan (DESIGN-MODE — Gate 1)
**Approved by:** Matt at 2026-05-16 (Day 4 open)
**Status:** COMPLETE
**Estimated effort:** 1 session (~60-90 min)
**Acceptance:** Reconciliation report + Gate 1 verdicts filed; knight-rider has a clean instruction set for whether to commit, partially revert, or amend `decisions-log.md` before staging the commit.

## Context — the situation to untangle

There is a mismatch between two parts of the workflow that should be aligned:

1. **`qa/pending/` has 4 decisions-log drafts** authored by knight-rider on 2026-05-16, all marked "awaiting Matt approval → commit to decisions-log.md":
   - `2026-05-16-decisions-log-engine-balance-stewardship.md` (View A lock + multi-dimensional divergence framework + movement-modeling abstraction + B10.2 supersession)
   - `2026-05-16-decisions-log-court-and-enemy-viz.md` (Court of Forms + Enemy visual legibility)
   - `2026-05-16-decisions-log-style-register-and-naming-triad.md` (HD-2D-shaped pixel-art register + naming-triad architecture)
   - `2026-05-16-decisions-log-research-db-retired.md` (research.db retirement)

2. **`reincarnated-engine/design/decisions/decisions-log.md` already contains entries with those titles** — but the file is uncommitted (`M design/decisions/decisions-log.md` in working tree, +286 lines). The matching entries appear at:
   - L1024 `2026-05-15: Court of Forms as form-library framing; meaning-of-the-arc statement locked`
   - L1050 `2026-05-15: Enemy visual legibility — sprite-archetype registry; sprite-from-player-pool rejected as anti-pattern`
   - L1098 `2026-05-15: Style register locked — Hand-drawn pixel-art (HD-2D-shaped)`
   - L1120 `2026-05-15: Naming triad — Trial / Mirror / Passage locked as universal frame; per-season variation pattern locked`
   - L1166 `2026-05-16: research.db retired — consolidation deferral closed`
   - L1206 `2026-05-16: View A locked as AOE balance philosophy; multi-dimensional divergence framework adopted; movement-modeling abstraction limitation named`
   - L1272 `2026-05-16: B10.2 Two-Gauntlet Pattern superseded — Option 2 (exclude pack fights from convergence binary search) is the canonical pattern`

The handoff `skill_handoff_2026-05-16.md` (written end-of-Day-3) explicitly says: "the qa/pending entries above are SEPARATE and NOT included in this diff (they're staged for jack-ryan Gate 1 first)." But the entries appear to be in the diff. Something doesn't add up — either:

- **(a) The handoff is stale** and the entries did get written to the file before/during the crash and the qa/pending drafts are now redundant copies (in which case Gate 1 runs against the in-file text and qa/pending gets cleared post-pass).
- **(b) The entries were written prematurely**, bypassing the standard "draft → Gate 1 → Matt approve → commit" flow — in which case some surgical removal may be needed before commit, OR Gate 1 runs retroactively but with explicit note that process was skipped.
- **(c) Partial state** — some entries are drafts-only (only in qa/pending), some are in-file, some both. Possible if writes happened across multiple sessions and got interrupted.

**Matt's directive at Day 4 open:** reconcile, then run Gate 1 against whichever set is authoritative. Result is the prerequisite for committing the working-tree decisions-log changes.

## What to do

### Step 1 — Reconcile (read-only inventory pass)

For each of the 7 entry locations listed above:

1. Read the in-file text at that line range in `reincarnated-engine/design/decisions/decisions-log.md`.
2. Read the matching qa/pending draft.
3. Compare: is the in-file text essentially the same as the draft? Or does it diverge (additions / deletions / reorderings)?

Build a small reconciliation table:

| Entry | In file? | In qa/pending? | Diverges? | Notes |
|---|---|---|---|---|
| Court of Forms | yes/no | yes/no | yes/no with description | … |
| (...one row per entry...) | | | | |

Use `git diff HEAD -- design/decisions/decisions-log.md` to see exactly what the working tree changed vs the last commit — this is the cleanest way to isolate the +286 lines.

### Step 2 — Gate 1 verdict per entry

For each entry (in whichever form is authoritative), apply standard Gate 1 review per ADR-002. PASS / PASS WITH FLAGS / BLOCK. The four engine-balance-related items (View A, divergence framework, movement abstraction, B10.2 supersession) are the highest-stakes — they should get the deepest scrutiny. Filed verdicts at `agentic_orchestration/qa/findings/2026-05-16-decisions-log-gate-1-batch.md` (or split per-entry if cleaner).

If you find a BLOCK on any entry, **the entry must not commit** — knight-rider will revert it from the working tree and re-draft.

### Step 3 — Recommend disposition

Produce a `## Recommendation` block at the end of the findings file with explicit instructions to knight-rider:

- Which entries are clean to commit as-is (with the rest of the +286 lines)
- Which entries need a textual amendment before commit (specify the amendment)
- Which entries need to be removed from the working-tree diff entirely (revert to HEAD on that range)
- Whether the qa/pending drafts can be cleared (moved to `qa/findings/`) or should be retained as historical record

## Cross-seam impact

This Gate 1 unblocks:
- Commit of the engine working-tree decisions-log changes (currently held by Matt)
- Gamora's `v1.3-b10-4-swarm-calibration` milestone tag (blocked on View A lock landing in the committed decisions-log)
- Drax's downstream interpretation logic for v0.7 viz (already authored against View A as a working assumption — needs the canonical lock)

## Required reading before starting

- `agentic_orchestration/qa/pending/` — the 4 drafts (read all four end-to-end)
- `reincarnated-engine/design/decisions/decisions-log.md` — the 7 entry locations listed above
- `agentic_orchestration/skill_handoff_2026-05-16.md` § "qa/pending — 4 decisions-log drafts" + § "Engine working tree — uncommitted"
- `canonical/story/engine-balance-stewardship.md` (the canonical source for the engine-balance entry)
- `canonical/story/court-of-forms.md`, `enemy-visual-legibility.md`, `style-register.md`, `naming-triad.md` (canonical sources for the four 2026-05-15-dated entries)
- `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` § 3.4 (the audit grounding research.db retirement)
- `agentic_orchestration/GOVERNANCE.md` — ADR-002 (decisions-log review process)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — at minimum #1 (math-before-code), #11 (attribution clarity), #12 (semantic-shifting)

## Out of scope

- Don't rewrite or improve the entries. Gate 1 verdicts only — knight-rider handles any rewriting.
- Don't run Gate 2 against the engine code that the entries reference (e.g., the B10.4 Option 2 commits). That's a separate Gate 2 pass and is not blocking this one.
- Don't author new decisions-log entries.
- Don't touch the qa/pending files — leave them in place for knight-rider to dispose of after disposition.

## Open questions for jack-ryan to resolve

- Did the four 2026-05-15-dated entries (Court, Enemy viz, Style register, Naming triad) follow the proper draft → Gate 1 → Matt approve → commit flow? Or were they committed-to-file ahead of review? Examine `git log -- design/decisions/decisions-log.md` for the relevant commits and check whether jack-ryan findings exist in `qa/findings/` for those entries. If the process was followed for 2026-05-15 entries, the same expectation applies to the 2026-05-16 entries — and the qa/pending drafts indicate that flow was supposed to happen but didn't complete before they hit the file.
- For the **B10.2 supersession** entry specifically: this directly invalidates a prior decisions-log entry that was itself only days old. Gate 1 should explicitly check the supersession is well-formed (clear cross-link, status updates on the prior entry, alternatives-considered section honest about why the original framing failed).
- For the **View A lock**: Matt's three-question framing (divergence floor, divergence ceiling, experienced-cost parity) was the framing-language ask in the gandalf commission. Does the in-file or draft text adequately reflect Matt's locked positions, or has language drifted during drafting? Apply Discipline #12 (semantic shift discipline) — if convergence_winrate / actual_winrate language ambiguity propagated into the draft, flag it.

## References

- `agentic_orchestration/GOVERNANCE.md` ADR-002 (process)
- `agentic_orchestration/REVIEW_PROCESS.md` (5 principles)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md`

## Acceptance criteria

- [ ] Reconciliation table built (one row per entry)
- [ ] Gate 1 verdict filed per entry (PASS / PASS WITH FLAGS / BLOCK)
- [ ] Findings file written to `agentic_orchestration/qa/findings/2026-05-16-decisions-log-gate-1-batch.md`
- [ ] `## Recommendation` block at end gives knight-rider unambiguous commit / amend / revert instructions per entry
- [ ] Knight-rider notified at completion

---

## Completion record

**Completed:** 2026-05-16
**Findings file:** `agentic_orchestration/qa/findings/2026-05-16-decisions-log-gate-1-batch.md`
**Disposition recommendation summary:** Scenario (a) confirmed — entries written to file before Gate 1 closed; Gate 1 run retroactively by prior findings file; both WARNs resolved per end-of-Day-3 handoff. All 7 entries PASS Gate 1. No BLOCKs. Commit the +286-line diff as-is (optional: fix Status field body at L157 for research.db entry — cosmetic only). qa/pending files may be archived or left in place.
**Notes for knight-rider:** See findings file § Recommendation for explicit per-entry disposition. Short version: commit everything, no reverts needed. Gamora B10.4 milestone tag condition (a) is satisfied once the commit lands; Matt's authorization still required for the tag itself per ADR-003. One cosmetic fix optional before commit (L157 Status field body).
