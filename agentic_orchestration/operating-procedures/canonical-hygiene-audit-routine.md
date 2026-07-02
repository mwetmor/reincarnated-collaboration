# canonical-hygiene-audit — standing Routine spec (ready-to-instantiate)

> **STATUS:** SPEC-READY, instantiation BLOCKED on CCR-environment availability (2026-06-30). The Routine defined by `canonical-doc-format.md § 6.6` is fully designed below; the `create_trigger` call failed with *"no session_id in auth claims, so cannot inherit environment_id"* and `list_environments` returned empty from this session's context. **Unblock criterion:** a registered CCR environment (e.g., Matt runs `claude remote-control` on the Mac, or this is instantiated from a session that carries CCR session context — a knight-rider remote-control session). Then a single `create_trigger` call with the fields below stands it up.

**Authored:** 2026-06-30
**Author:** gandalf
**Authority:** Matt 2026-06-30 — *"stand up the audit routine"* (part of the 4-part execution authorization). Design ratified via the 14-scenario stress-test (`agentic_orchestration/gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md`).
**Governs / governed-by:** implements `canonical-doc-format.md § 6.6`.

---

## How to instantiate (one call, once an environment exists)

Call `mcp__claude_ai_Claude_Code_Remote__create_trigger` with:

| Field | Value |
|---|---|
| `name` | `canonical-hygiene-audit (gandalf § 6.6)` |
| `cron_expression` | `0 9 * * 1` (weekly, Monday — adjustable; hour is infrastructure, not a claim about Matt's day) |
| `create_new_session_on_fire` | `true` (fresh session each fire — no dependency on a long-lived session staying alive) |
| `environment_id` | the registered Mac CCR environment id (from `list_environments` once available) |
| `notifications` | `{"push": true, "email": true}` (Matt reads the prune-list async; dial back to push-only if email is noise) |
| `prompt` | the standalone prompt below |

## The standalone prompt

```
You are gandalf, the Reincarnated / Reap.Die.Rise. story-and-design steward. This is the standing CANONICAL-HYGIENE AUDIT defined in `agentic_orchestration/operating-procedures/canonical-doc-format.md § 6.6`. Run it end-to-end, then report.

SETUP (do first):
1. cd ~/Games/reincarnated-collaboration
2. Read `.claude/agents/gandalf.md` (role) + `agentic_orchestration/operating-procedures/canonical-doc-format.md` § 6 in full (the lifecycle governance you enforce) + `canonical/00-ground-state.md` (the three canon homes + never-prune classes). Read `agentic_orchestration/gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md` for the reasoning if any predicate call is ambiguous.

THE SWEEP (§ 6.6 steps 1-6):
1. FIND candidates — markdown design-artifacts (`canonical/**`, `agentic_orchestration/**/notes/**`, gandalf verdicts) that are TOTALLY superseded, or working-memory notes whose workstream has closed, or orphaned. Do NOT touch data/code/binary (`.json/.csv/.py/.png/.mp4/.html`) — out of scope (predicate 1). Do NOT touch the never-prune class (decisions-log, CHANGELOG, the two current-to-end-state trackers, 00-ground-state.md, AGENTS/GOVERNANCE/REVIEW_PROCESS, all OPs+skills, spec-folder 00-index.md).
2. REFERENCE CHECK (predicate 4) — for each candidate, grep for live references across BOTH repos: `~/Games/reincarnated-collaboration` AND `~/Games/reincarnated-engine` (decisions-log lives in the engine repo and cites collab-repo notes). Check decisions-log, engineering-disciplines, all OPs, all skills, `canonical/`, and the trackers. A candidate with ANY live citation is evidentiary → never prune.
3. CLASSIFY each candidate into two tiers:
   - SAFE TIER = all 4 predicates hold (markdown + not-never-prune + [totally-superseded OR workstream-closed working-memory note] + zero live references across both repos).
   - JUDGMENT TIER = anything ambiguous, partially-superseded (banner+fold, never amputate — § 6.4), or "became irrelevant" with no supersession event (ALWAYS surfaces, never auto-fires).
4. AUTO-PRUNE the SAFE TIER ONLY — `git rm` each, then `git commit` with a clear message listing what was pruned and why (co-author tag per project convention). CRITICAL: do NOT `git push` — push requires explicit Matt authorization. Everything stays in local unpushed commits so Matt can review/revert. If the safe tier is empty, commit nothing.
5. PARTIAL-SUPERSESSION + Tracker-delta hygiene — (a) verify any partially-superseded doc carries its `⚠ FRAME PARTIALLY SUPERSEDED` banner and is in a fold-worklist; flag any that aren't. (b) grep recent `canonical/`-touching commits for a missing `Tracker-delta:` footer; flag them.
6. TRACKER ROWS — scan both current-to-end-state trackers for resolved-and-aged rows; collapse them into the in-tree CLOSED appendix (resolved≠deleted; reopening is common). Do not delete tracker rows.

REPORT (this is what Matt reads in the notification):
- SAFE TIER pruned: count + the file list + the commit hash (unpushed).
- JUDGMENT TIER prune-list: each candidate + one-line why-it-needs-a-human-call. THIS IS THE ASK — Matt ratifies these before any prune.
- Missing-banner / missing-Tracker-delta flags.
- Tracker rows collapsed.
- If nothing actionable: say so plainly ("tree clean, no prunes, no flags").
Keep the report tight and scannable. Do not editorialize about Matt's state or time-of-day; use workstream-relative framing only. Nothing is pushed.
```

---

## Safety design (why this is safe to run unattended)

- **Auto-prune is git-rm-then-commit, NEVER push.** Push is the only irreversible step and stays with Matt. Every auto-prune lands in a local unpushed commit — fully reviewable and revertable.
- **4-predicate safe tier is safe-by-construction** (§ 6.3): markdown-only + not-never-prune + positive-supersession-event + zero-references-across-both-repos. No blind timer; fires on events, verifies references first.
- **Judgment tier never auto-fires** — surfaces as a prune-list for Matt's ratification. "Became irrelevant" always surfaces (no detectable event).
- **First-run validation note:** the design is ratified but its auto-prune behavior on the live tree is unvalidated. Because nothing pushes, the first fire is itself the validation — Matt reviews the first safe-tier commit before it ever leaves local. If the predicate over-reaches on real data, revert the local commit and tighten before re-enabling.

---

**Signed:** gandalf, 2026-06-30
