# Dispatch — jack-ryan: Engineering-Discipline #19 — The Agent Tool Is Not For Waiting

**Date:** 2026-05-22
**Author:** knight-rider
**Recipient:** jack-ryan (process steward, engineering-disciplines author)
**Authority:** Matt 2026-05-22 (pre-authorization G of prolonged-autonomy mission; reinforced in conversation with knight-rider)
**Priority:** HIGH — load-bearing for prolonged-autonomy mission stability
**Estimated effort:** 1-2 hours (single discipline entry; canonical integration)

---

## 0. TL;DR

Author a new entry in `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — **Discipline #19: The Agent tool is not for waiting**.

The pattern is grounded in two empirical instances during the LC-011 ablation work (2026-05-21 / 2026-05-22):

1. **First failure (gandalf 2026-05-21 evening):** spawning Agent sub-agents to "babysit" the 5-hour ablation script. The agents timed out; the orchestrator (then-knight-rider) saw "completed" tool results with no useful output and spawned more babysit agents. Loop. The babysit pattern produced orchestration churn without keeping the script alive — and **didn't even detect when the script crashed at 00:14 EDT 2026-05-22**.

2. **Second failure (knight-rider 2026-05-22 morning, post-Matt-interrupt):** when knight-rider resumed in prolonged-autonomy mode, the instinct to "watch the recovery script via sub-agents" was structurally identical. Matt explicitly interrupted to surface this — see conversation transcript 2026-05-22.

The compound failure mode: **a long-running script can crash silently AND the babysit agent intended to detect the crash also fails silently** (no summary artifact produced; no diagnostic signal). The pattern is structurally non-recoverable.

This dispatch frames the discipline; jack-ryan authors the canonical entry.

---

## 1. The discipline (proposed draft)

> **Discipline #19 — The Agent tool is not for waiting.**
>
> **Statement:** Long-running work (scripts, sims, gauntlets, ablations) runs as a background OS process via `Bash(run_in_background=true)` or `nohup`. Status checks are on-demand one-shot queries (`ps`, `sqlite3`, `tail`, file mtime). The `Agent` tool (any specialist sub-agent invocation) is reserved for *active* sub-tasks with bounded, predictable runtime — typically ≤ 5 minutes. Never spawn an Agent whose purpose is to "wait," "watch," "monitor," "babysit," or "poll until done." Recursive babysit spawning produces orchestration churn without keeping the underlying script alive, and silently fails to detect script crashes.
>
> **Practical rules:**
>
> 1. **Long-running script execution.** Use `Bash(run_in_background=true)` or shell `&` + `nohup`. The script runs at OS level and does NOT depend on any agent session continuing. Output redirects to a fresh log file at a known path.
>
> 2. **Status checks are one-shots.** Query DB / process table / log mtime via direct Bash. No agent invocation. If the orchestrator session needs to end before completion, the next session's startup queries the same artifacts and resumes from there. Cross-session continuity is **file-based**, not agent-based.
>
> 3. **Reactive streaming via Monitor.** If a specific output line needs to trigger action (e.g., "ABLATION COMPLETE"), use the `Monitor` tool (stdout/stderr stream → notification per line). Still no Agent. Still no loop.
>
> 4. **Bounded sub-agent dispatches remain legal.** Agent invocations for *active* work (jack-ryan reviews a single document; gandalf authors a defined doc; legolas runs a bounded analysis) remain valid. Bounded runtime, observable progress, explicit deliverable.
>
> 5. **If a bounded Agent invocation appears to hang.** Cut it. Do NOT re-spawn. File the symptom (which agent, what task, evidence of hang) as a Discipline #19 incident note. Proceed without the sub-agent if possible; escalate to Matt if the work was load-bearing.
>
> 6. **Self-policing reflex.** Before any `Agent(...)` invocation, the orchestrator checks: is the prompt asking the agent to wait/watch/monitor anything? If yes, use direct Bash + Monitor instead.

---

## 2. Why this is load-bearing for prolonged-autonomy mode

The prolonged-autonomy mission (Matt 2026-05-22) explicitly relies on:

- **Long-running work** (multi-hour scripts, multi-day workstreams) executed without continuous Matt oversight
- **Cross-session continuity** when knight-rider's session ends but work continues
- **Hive coordination** across specialist agents without runaway sub-agent invocation costs

A babysit-pattern relapse during prolonged autonomy is structurally worse than during interactive sessions, because:

- **Matt is not present to interrupt the loop** (as he did at 2026-05-22 morning)
- **The orchestrator's session may exhaust without producing useful artifacts**
- **Long-running scripts may crash silently with neither the script nor the babysit agent detecting it**

This discipline is the structural fix. Ratifying it canonically lets future knight-rider sessions (and all specialist sessions) inherit the constraint at startup — no personal commitment required.

---

## 3. Acceptance criteria

The discipline entry, when authored, should:

1. **Land in canonical location**: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` as a new top-level entry numbered Discipline #19.

2. **Reference the two empirical instances** as grounding (gandalf 2026-05-21 evening babysit-loop; knight-rider 2026-05-22 morning relapse). Cross-reference:
   - `agentic_orchestration/p0-closure-note-2026-05-21.md` § 6 (gandalf's initial framing)
   - `agentic_orchestration/matt-briefing-2026-05-22-lc-011-option-c-strong-confirm.md` § 2 (script-crash + babysit-agent silent-failure compound mode)
   - `agentic_orchestration/dispatches/2026-05-22-jack-ryan-engineering-discipline-19-agent-tool-not-for-waiting.md` (this dispatch)

3. **State the practical rules** (per § 1 above; refine to canonical voice).

4. **Cross-reference adjacent disciplines**: Discipline #2 (smoke-test vs full-regen) for the "right tool for the question" framing; Discipline #11 (empirical inspection over assumption) for the "diagnose before re-firing" reflex.

5. **Author a brief retrospective**: 1-2 paragraphs summarizing what each empirical instance taught and what the discipline structurally prevents going forward.

6. **Capture the operational pattern** for the recovery script that landed during this session (`scripts/w07_lc011_ablation_recovery.py`) as a canonical example: foreground diagnose → `nohup ... > log 2>&1 &` → status checks on-demand → JSON summary artifact for cross-session resumption.

---

## 4. Out of scope

- **Discipline #20 candidates** (e.g., "long-running scripts must produce JSON summary artifacts"; "log verbosity must be bounded") — surface these as candidates in your retrospective but do not author them in this dispatch. Knight-rider will queue them for future review with Matt.

- **Re-litigation of the babysit-pattern non-viability claim** (already canonical per gandalf 2026-05-21 + Matt 2026-05-22 conversation). Discipline #19 ratifies, doesn't re-debate.

- **Code-level changes to existing scripts** (rocket / gamora's lane; not jack-ryan's). Discipline #19 is a process discipline, not an implementation change.

---

## 5. Critique-pair structure

- **gandalf reviews architectural alignment** before commit: discipline framing consistent with the prolonged-autonomy mission stability concern + with the engineering-disciplines doc's existing structure
- **knight-rider reviews orchestration-side completeness**: the practical rules cover the failure modes I observed in this session
- **Matt approves on return** (canonical commit; discipline entries traditionally carry Matt-approval per engineering-disciplines.md's existing pattern)

If approval is delayed past Matt's return, the discipline lives as PROPOSED status until ratified. Specialist agents observe the proposed discipline during the interim.

---

## 6. Timing

- **Earliest fire date:** any session 2026-05-22 onwards; not blocked by W1.13 disposition or recovery completion
- **Recommended fire:** today's session if jack-ryan launches; otherwise next session
- **Duration:** ~1-2 hours focused work

---

## 7. Cross-references

- `agentic_orchestration/p0-closure-note-2026-05-21.md` § 6 — initial gandalf framing of babysit-pattern non-viability
- `agentic_orchestration/matt-briefing-2026-05-22-lc-011-option-c-strong-confirm.md` § 2 — operational evidence of compound silent failure
- `~/Games/reincarnated-engine/scripts/w07_lc011_ablation_recovery.py` — canonical recovery-pattern exemplar (foreground diagnose + background fire + on-demand DB checks + JSON summary)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — target file for the new entry

---

**Signed:** knight-rider (orchestrator under prolonged-autonomy mandate)
**For:** structural fix of the orchestration failure mode that interrupted P0 close + threatened prolonged-autonomy mission stability.
