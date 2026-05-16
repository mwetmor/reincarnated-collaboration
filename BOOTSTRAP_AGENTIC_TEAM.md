# Bootstrap Agentic Team — Drop-in Brief

**Purpose:** A single drop-in markdown file that tells Claude to set up a 6-entity engineering team for THIS project — Knight Rider as orchestrator, Jack Ryan as analyst, Guardians of the Galaxy as developers. Drop this file into any project's root directory, open a Claude Code session there, and say: *"Use BOOTSTRAP_AGENTIC_TEAM.md to set up the team for this project."*

---

## Instructions to Claude

When the user references this file:

1. **If the `build-multi-agent-team` skill is installed on this machine** — invoke that skill. Use the pre-decided values below as Phase 3 and Phase 4 inputs. The skill still runs Phase 0 Survey, Phase 1 Protect, Phase 2 Decompose, and Phases 5–8 normally (the parts that REQUIRE project-specific input).
2. **If the skill is NOT installed** — walk through the same workflow manually using this brief as your specification. Produce the same artifact set listed below.

Either path, the contract is identical: produce a fully scaffolded team, committed on a feature branch (NEVER directly to `main` if `main` already has commits), with the user able to `claude --agent knight-rider` and continue immediately.

---

## Team topology — 6 entities

| Entity | Role | Model | Notes |
|---|---|---|---|
| **Senior Architect / Director** (the human) | Final approval; design direction | (you, the user) | Receives synthesized output; resolves jack-ryan BLOCKs |
| `knight-rider` | Orchestrator / Communicator | **Opus** | Coordinates work across all scopes; never writes production code directly |
| `jack-ryan` | Analyst / QA / Quality Guardian | **Sonnet** | Two modes — DESIGN-MODE (peer collaborator with knight-rider) and DEV-MODE (gatekeeper with BLOCK authority). Invoked at every Gate 1 and Gate 2. Writes findings to a dedicated QA folder; never writes production code. |
| `rocket` | Developer | Sonnet | Suggested for **input/ingestion/source** layer (assets, data, raw inputs) |
| `gamora` | Developer | Sonnet | Suggested for **core logic / precision** layer (the most analytically sensitive code in the project) |
| `star-lord` | Developer | Sonnet | Suggested for **orchestration / integration / final assembly** layer |
| `drax` *(optional 4th developer)* | Developer | Sonnet | Add if the project has 4 natural seams. Best for direct/numeric/raw-compute domains (rendering, math, numerics, network protocols). |

The Senior Architect + 5 agents = 6 entities. Add `drax` only if Phase 2 Decompose identifies a 4th seam.

---

## Pre-decided design choices (DO NOT re-debate)

These come from a worked precedent and should ship as defaults unless the user explicitly asks otherwise:

- **Model assignments** — Opus for orchestrator; Sonnet for analyst and all developers; **NO Haiku** for any agent in this team (Haiku is for explicit-checklist classification, not implicit reasoning)
- **ADR format** — Lightweight: decision / context / alternatives / consequences. Field structure is non-negotiable; content is per-ADR
- **Review gates** — Gate 1 (pre-prompt) + Gate 2 (post-output). Severity: INFO / WARN / BLOCK
- **jack-ryan two-mode operation** — design-mode peer dialogue with knight-rider before user sees anything; dev-mode gatekeeper at both gates
- **Survey-mode behavioral constraint** — every agent, when asked to survey/inventory/describe: reports what exists; does NOT interleave "should" statements with descriptive findings. "What is" and "what's wrong" are separate outputs
- **Re-entry principle** — every workflow boundary produces a durable artifact; conversational checkpoints do not count
- **External write authorization** — read-only by default for any database / API / cloud SDK / file system beyond agent scope / process spawning / messaging / credential mutation. Writes require per-statement user authorization. Authorization does not persist across sessions
- **Hard file prohibitions** — binaries (`.pbix`, `.exe`, `.dll`), credentials (`.env`, `secrets.*`, `*_key.json`, `*.pem`, `*.cer`), lock files for active package managers
- **PBIX → PBIP standing rule** — if any `.pbix` file exists, must be converted before any agent scope includes it
- **Git commit gate** — clean git state required BEFORE any agent work begins (ADR-007 pattern)

---

## Project-specific decisions to ask the user

These require dialogue — the brief does NOT pre-decide them:

1. **One-line description of this project.** (What is it?)
2. **Natural seams.** Walk the user through identifying 3–4 bounded domains. Game/engine examples: rendering, gameplay logic, asset pipeline, networking, AI/behavior, audio, UI, build system. Pick seams that are MUTUALLY EXCLUSIVE — no file owned by two devs.
3. **Number of developers** (3 or 4) based on the seams identified.
4. **Assign Guardians to seams.** Default suggestions above are starting points — the user picks which character maps to which seam.
5. **Git platform** — GitHub / GitLab / Bitbucket / Azure DevOps / self-hosted / none.
6. **Branch strategy** — trunk-based with feature branches (default) / GitFlow / custom.
7. **Commit convention** — free-form / Conventional Commits / custom.
8. **Documentation depth** — Minimal (scaffolding only) / Standard (governance + design template) / Full-from-survey (pre-populate design docs from code — NOT recommended on projects with mature existing design docs) / Custom.
9. **Existing project handling** — if the project already has commits and branches:
   - Run setup on a FEATURE BRANCH (e.g., `git checkout -b agentic-team-setup`)
   - Do NOT commit team setup directly to `main` or `develop`
   - Do NOT overwrite existing design docs without exact-diff per-artifact approval

---

## Artifacts to generate

After user dialogue, produce these files. Use exact paths.

```
.claude/agents/knight-rider.md
.claude/agents/jack-ryan.md
.claude/agents/rocket.md
.claude/agents/gamora.md
.claude/agents/star-lord.md
.claude/agents/drax.md                                   ← only if user chose 4 devs

agentic_orchestration/AGENTS.md                          ← team topology, scope map, model rationale, "how to launch agents"
agentic_orchestration/GOVERNANCE.md                      ← founding ADRs (topology / SAMSON-equivalent normalization / git commit gate / external write authorization / etc.)
agentic_orchestration/REVIEW_PROCESS.md                  ← 5 principles + change lifecycle + file-type rules + external-system execution rules
agentic_orchestration/CHANGELOG.md                       ← Day 0 founding entry

CLAUDE.md                                                ← project-root orientation, under 60 lines

agentic_orchestration/skill_handoff_<YYYY-MM-DD>.md      ← handoff context for orchestrator's first invocation
```

### Per-agent definition file structure

Each `.claude/agents/<name>.md` requires YAML frontmatter:

```yaml
---
name: <agent-name>
description: <Role>. <Scope summary>. <Key negative — "does not touch X">.
model: claude-opus-4-7 | claude-sonnet-4-6
scope: orchestrator | qa-analyst | <dev-scope-name>
---
```

Body sections: position in team / what you own / file-type rules / external system execution rules / design documents to read / survey-mode behavioral constraint / agent-specific rules / mindset. For the orchestrator, ADD: first-invocation behavior (read `skill_handoff_*.md`, then invoke analyst).

---

## After artifacts are written

1. Show the user the artifact manifest.
2. Stage all on a feature branch: `git checkout -b agentic-team-setup` (if not already done).
3. Commit. If a pre-commit hook (e.g., GitGuardian Shield) fails — never use `--no-verify` without explicit user authorization.
4. If git platform configured: push the feature branch; remind user to open a merge request before merging to main.
5. Print the runbook to the user:

```
Your synthetic engineering team is ready.

To launch:
  cd <this-project-directory>
  claude --agent knight-rider

knight-rider will:
1. Read CLAUDE.md and the skill_handoff_<date>.md
2. Invoke jack-ryan as a subagent for the first design dialogue
3. Be ready for your first dev cycle
```

---

## Why the manual session transition

Claude Code's session model fixes agent identity at session start via `--agent <name>`. There is no mechanism for a session to end itself and respawn under a different agent. After the setup session completes, the user opens a new terminal and runs `claude --agent knight-rider`. The handoff file makes that new session feel automatic from the orchestrator's perspective — it does not re-ask anything decided here.

---

## Canonical reference

This pattern was developed and refined for the **TFB Comms Audit Model** — a Snowflake SQL pipeline. The worked example lives at `<that-repo>/agentic_orchestration/`. Anything ambiguous in this brief defers to the canonical implementation.

The same pattern works for any structured engineering project: data pipelines, game engines, simulations, web applications, ML systems, libraries. Adjust the dev scopes to match your project's natural seams; everything else carries over.

---

*"Your synthetic engineering team is ready."*
