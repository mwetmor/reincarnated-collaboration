# AGENTS.md — root shim for non-Claude agents (Codex CLI et al.)

> **What this file is:** the translation layer for agent runtimes that auto-read `AGENTS.md`
> but do not read `CLAUDE.md` and **cannot invoke Claude Code skills by name** (OpenAI Codex
> CLI is the standing case). It is a **ROUTER, not a mirror** — content lives once, in the
> files it points to. If you are a Claude Code session, your charter is `CLAUDE.md`; nothing
> here overrides it.
>
> **Not to be confused with** `agentic_orchestration/AGENTS.md` — that is the team-topology
> document (who the 10 agents are, seam map). This root file is runtime plumbing only.
>
> **Maintenance rule (binding):** add POINTERS here, never copy content. A hand-mirrored
> charter drifts silently in the only reader with no other source of truth — this project has
> convicted that failure class three times (the ~6-week-stale skill copy; the push posture
> recorded in one session, not the wave; Discipline #73 generally). If `CLAUDE.md` changes,
> nothing here should need to change unless a *path* moved.

## 1. Read order (non-negotiable)

1. **`CLAUDE.md`** (this repo root) — read IN FULL. It is the charter: repo map, team commit
   + push discipline, standing push patterns, the `git -C` rule, conflict rules. This file
   adds only the translation layer below.
2. **`canonical/00-ground-state.md`** — the canon router. First read for every agent on every
   invocation, same law as the Claude lane.
3. Your **role file** + **operating procedure** (§ 2), then the session-start reads they name.

## 2. Role adoption + the skill-name translation

Claude Code sessions adopt roles via `--agent <name>` and load skills by name. You do it by
reading files:

- **Role files:** `.claude/agents/<name>.md` (drax, elrond, galadriel, gamora, gandalf,
  jack-ryan, knight-rider, legolas, legolas-crawler, rocket, star-lord).
- **Operating procedures — read the SOURCE, not the skill copy.** When any doc says *"invoke
  skill `reincarnated-<X>`"* or *"read your operating procedure skill"*, apply this mapping:

  | Skill name pattern | Read this file instead |
  |---|---|
  | `reincarnated-<agent>-operating-procedure` | `agentic_orchestration/operating-procedures/<agent>.md` |
  | `reincarnated-<topic>` (cross-cutting) | `agentic_orchestration/operating-procedures/<topic>.md` |

  (Uniform rule: strip the `reincarnated-` prefix; agent OPs also drop
  `-operating-procedure`.) The `.claude/skills/` directory holds **packaged COPIES** of these
  sources; the sync rule declares the source governs — going to the copy rebuilds the
  staleness trap this file exists to close.
- **Engineering disciplines (authoritative home):**
  `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (per the
  `CLAUDE.md` where-to-find-things table).

## 3. Codex-lane standing provisions (durable home — previously per-session prompt text)

- **Concurrency law (Matt ruling 2026-08-25 — SUPERSEDES the original serial law):**
  **one Codex session per available named agent seam, plus at most one open Codex lane.**
  Parallel Codex sessions are permitted provided EACH wears a distinct named seam (role file +
  OP read per § 2 — the seam's discipline stack loads with the name); the open lane covers
  unseamed general work. Never two Codex sessions in the same seam concurrently. This matches
  the grok-lane constraint. *Basis:* legolas Mode A findings
  (`agentic_orchestration/legolas/notes/2026-08-25-codex-parallel-fanout-personal-account-risk.md`)
  — compliance risk LOW, economics risk HIGH; the constraint is an **economics + attribution
  discipline, not a terms requirement.** The superseded serial law's compliance justification
  is evidentially dead and is recorded as such.
- **Internal subagent trees stay OFF (hard guard):** never raise
  `agents.max_concurrent_threads_per_session` or enable Codex's internal recursive subagents.
  Every severe quota incident on record (openai/codex #35463) traces to recursive internal
  trees under this project's exact model pin; **flat external `codex exec` fan-out is the only
  permitted parallel shape.** A quota-exhausted personal account fails hard, taking ordinary
  ChatGPT usage with it.
- **`codex login status` at session start** — verify auth before taking work.
- **Model pin** — `gpt-5.6-sol` @ `xhigh` effort, per Matt's standing agenda.
- **Fault-fallback** — on Codex-lane fault, the work falls back to the **named Claude agent**
  for that seam; record the fallback in the completion record.

## 4. Claude-only capabilities and your substitute

| Claude Code capability | Codex substitute |
|---|---|
| `Skill` tool (invoke by name) | Read the mapped source file (§ 2 table) |
| Named sub-agent spawning (`Agent` tool) | Not available — work serially in-session; escalate genuinely parallel needs to the Claude lane via knight-rider |
| Plugins / scheduled wake-ups / crons | Not available — flag, don't improvise |
| Auto-loaded `CLAUDE.md` | Read it yourself, first (§ 1) |

Commit + push discipline binds **identically** to both lanes — see the `CLAUDE.md` team
addendum (auto-commit for authorized in-scope work; push per standing pattern or explicit
word; `git -C <path>` on every cross-repo git operation).

---

*Authored by gandalf, 2026-08-25, at Matt's word — lesson imported from Matt's work-laptop
Codex fan-out practice ("Codex cannot invoke skills by name; point everything from AGENTS.md").
Adopted here in router form rather than mirror form; see the maintenance rule above for why.*
