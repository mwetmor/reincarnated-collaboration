# CLAUDE.md — reincarnated-collaboration meta-repo

**You are in the meta-repo.** This directory is the design/coordination hub for the Reincarnated project. The actual codebases are siblings:

- `~/Games/reincarnated-engine/` — Python engine (content gen, simulation, balance, telemetry, LLM)
- `~/Games/reincarnated-demo/` — Pixi.js demo (player-facing demo1)
- `~/Games/reincarnated-loadout/` — React/Vite loadout web app (deployed to Vercel)

## Synthetic engineering team

  > **Orientation:** Engine first. Game second. Phase third.                                                                                                                                                                                                                                                                                  
  > Engine = architectural integrity (substrate-led discipline; canonical docs).
  > Game = player-facing quality. Phase = operational unit (waves, dispatches).                                                                                                                                                                                                                                                               
  > Conflict resolution: engine > game > phase. 

A **14-entity federated agentic team** operates across all repos (10 Mac-resident specialists + 4 PC-resident — 3 PC counterparts to Mac orchestrator/design/QA + Mantis at PC for UE seam; team federated 2026-06-07 per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md`). **Read `agentic_orchestration/AGENTS.md` first.** PC-resident agents also first-read the federated team commit doc.

**PC-resident agents (David-H, Radagast, Sam, Mantis) operate with identical autonomy + auto-commit authority as Mac-resident agents.** SSH-invocation from Mac does NOT alter Matt-authorization scope. The Team commit + push discipline addendum below applies symmetrically to both hosts. PC team is NOT more cautious than Mac team.

Quick launch:

```bash
# === Mac-resident team ===

# Coordinator session (start of day)
cd ~/Games/reincarnated-collaboration && claude --agent knight-rider

# Specialist sessions (task work)
cd ~/Games/reincarnated-engine && claude --agent gamora       # or rocket, star-lord
cd ~/Games/reincarnated-loadout && claude --agent drax        # or reincarnated-demo

# QA session
cd ~/Games/reincarnated-collaboration && claude --agent jack-ryan

# === PC-resident team (SSH from Mac) ===
# Connection target: mhwet@192.168.1.133 (passwordless SSH from Mac per matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md)

# One-shot pattern (Warp-friendly; -t forces PTY for Claude Code TUI)
ssh -t mhwet@192.168.1.133 "cd C:\dev\reincarnated-collaboration && claude --agent david-h"   # or radagast, sam
ssh -t mhwet@192.168.1.133 "cd C:\dev\reincarnated-unreal\Reincarnated && claude --agent mantis"  # UE seam

# Two-step pattern (any terminal)
ssh mhwet@192.168.1.133
# then on PC shell:
cd C:\dev\reincarnated-collaboration
claude --agent david-h   # or radagast, sam
```

**CRITICAL — PC-side pull discipline at session-start.** PC clone is a git-tracked sibling of Mac clone. Mac-side commits do NOT reach PC until origin push + PC pull. PC agents MUST `git pull origin main` at session-start before reading task-specific dispatches. If session-opener prompt references files that don't exist after pull, the gap is Mac-side push-discipline failure, not authoring failure — surface clearly + halt; do NOT self-author cross-cutting artifacts to fill the gap.

## Mobile-accessible sessions via Claude Code Remote Control (established 2026-06-08)

Claude Code Remote Control (v2.1.51+) makes local sessions mobile-accessible via the Claude iOS app. **Per-machine policy** (confirmed via hypothesis test 2026-06-08): one Remote Control server per host, with up to 32 concurrent sessions per server. Mac and PC count separately.

```bash
# === Mac Remote Control (gandalf / knight-rider / jack-ryan / specialists) ===
# In a separate Mac terminal window (not your active interactive session):
cd ~/Games/reincarnated-collaboration
claude remote-control --name "Mac RC"
# Spawn mode: 1 (same-dir; default) for shared working tree
# 2 (worktree) for isolated git worktrees per session

# === PC Remote Control (david-h / sam / radagast / mantis) ===
# SSH from Mac into PC, then on PC shell:
ssh mhwet@192.168.1.133
cd C:\dev\reincarnated-collaboration
claude remote-control --name "DH Remote"
# Same spawn-mode choice; SSH session must stay open for the server to keep running
```

**Agent role adoption pattern (v2.1.169+ — `--agent` flag removed from `remote-control` subcommand):** Mac-side and PC-side Remote Control servers run as generic Claude Code spawn-servers. Agent role is set by **prompt at session engagement**, not at invocation. After connecting from iOS, prompt the session with role-adoption text:

```
Read your operating procedure skill (reincarnated-<agent>-operating-procedure) and execute session-start protocol per OP § 1. Then await my direction.
```

The session reads the OP + role definition + session-start docs and operates as that agent from that point.

**Operational notes:**
- Remote Control servers must keep their interactive process alive (Mac terminal window OR PC SSH session). Closing kills the server.
- Mac Mini configured for no-sleep supports this naturally
- PC SSH session-keep-alive is the constraint for PC Remote Control persistence (consider running under `tmux` or persistent shell if longer durability needed)
- Session conversation history persists across iOS app flips — switching from gandalf session to KR session in iOS doesn't kill either
- GitHub OAuth re-auth (Issue #44805 workaround): claude.ai → Settings → Account → GitHub
- Cross-cycle credential durability: switch git remote to SSH-key auth at project init for any host running Remote Control; HTTPS credential helpers (osxkeychain / wincredman) fail in non-interactive contexts

## Where to find things

| Need | Path |
|---|---|
| Team topology + scope map | `agentic_orchestration/AGENTS.md` |
| **Federated PC team architecture (PC team first-read)** | `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` |
| **SSH handoff + passwordless setup** | `matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md` |
| Founding ADRs | `agentic_orchestration/GOVERNANCE.md` |
| Review process + 5 principles | `agentic_orchestration/REVIEW_PROCESS.md` |
| Latest handoff context | `agentic_orchestration/skill_handoff_<date>.md` |
| Team event log | `agentic_orchestration/CHANGELOG.md` |
| Design discussion docs | `canonical/` (numbered: 09, 16, 17, 28, 29, 30, 31, 32, 33, ...) |
| Engineering disciplines (12) | `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` |
| Decisions log | `~/Games/reincarnated-engine/design/decisions/decisions-log.md` |
| Current roadmap (B-series) | `canonical/historical/16-project-roadmap.md` |

## Key conventions

- **Working branch (engine):** `main`
- **Tag prefix (intermediate):** `<seam>/v<X.Y>-<feature>-<n>` (e.g., `gamora/v1.3-b14-2`)
- **Tag prefix (milestone, Matt-approved):** `v<X.Y>-<feature>` (e.g., `v1.3-b14-5-secondary-loop`)
- **Cross-seam handoff:** `MIGRATION.md` per ADR-004
- **Per-seam checkpoint:** `AGENT_STATE.md` per agent

## Senior Architect

Matt (mhwetmore@gmail.com) — final approval, design direction, resolves jack-ryan BLOCKs.

---

## Team commit + push discipline (multi-agent refinement of system-default)

> **Authored 2026-05-25** per Matt directive to resolve recurring knight-rider over-asking behavioral bug.

The Claude Code system-default commit rule ("NEVER commit changes unless the user explicitly asks") was designed for single-user single-agent scenarios. The reincarnated-collaboration meta-repo runs a **14-entity federated synthetic engineering team** (10 Mac-resident specialists + 4 PC-resident — 3 PC counterparts to Mac orchestrator/design/QA + Mantis at PC for UE seam; team federated 2026-06-07 per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md`) where routine in-scope work-products SHOULD auto-commit without per-commit re-asking.

This addendum refines the system-default rule for team-level operation:

### Commits — AUTO-FIRE without per-commit Matt re-asking

Seam-owning agents AUTO-COMMIT routine work-products from authorized in-scope work. Examples:

**Mac-resident team (canonical authority for cross-cutting):**

| Agent | Auto-commit pattern (when authorized cycle work produces) |
|---|---|
| Knight-rider | Cycle orchestration dispatches; Gate-1 critique-pair coordination artifacts; state-file updates; wave-closeout summaries |
| Gandalf | Canonical doc updates from design sessions; recognition records; request artifacts; notes from Pattern-A/B dialogue |
| Elrond | Substrate-curation artifacts from dispatch execution; schema-extension MIGRATION docs; per-source extraction logs |
| Rocket | Generation-code amendments from authorized engine work; algorithm spec updates |
| Gamora | Simulation-code amendments from authorized engine work; balance-loop artifacts |
| Star-lord | Export-pipeline + telemetry amendments from authorized engine work; LLM-call infrastructure updates |
| Galadriel | CV-pipeline + visual benchmark artifacts from authorized vision work |
| Drax | Loadout / demo amendments from authorized player-surface work |
| Legolas | Research + crawl artifacts from authorized Mode A / Mode B work |
| Jack-ryan | Gate-1 / Gate-2 findings; engineering-discipline canonical writes; decisions-log entries |

**PC-resident team (added 2026-06-07 federated commit; auto-commit pattern explicitly extended):**

| Agent | Auto-commit pattern (when authorized cycle work produces) |
|---|---|
| David-H | PC-seam orchestration dispatches; Gate-1 critique-pair coordination artifacts (David-H + Radagast + Sam local trio); PC-side wave-close records; cross-host consultation notes to Mac-KR; session-boundary memos |
| Radagast | PC-seam canonical-story doc updates (UE patterns, Niagara VFX, Mutable, weapon-sockets, asset pipeline, mantis-spike learnings); PC-seam pushback memoranda; PC-side Pattern A-deep verdict files; PC-seam recognition records; cross-host consultation notes to Mac-gandalf |
| Sam | PC-seam Gate-1 / Gate-2 findings (`agentic_orchestration/qa/findings/<date>-<work-item>.md`); decisions-log entry PROPOSALS (Mac-jack-ryan canonical-writes); engineering-discipline amendment PROPOSALS; PC-side ADR-002 tiered approvals; cross-host consultation notes to Mac-jack-ryan |
| Mantis | UE work-products in `reincarnated-unreal/` from authorized port/spike workstreams; spike findings + criterion reports; PC-side AGENT_STATE.md updates; cross-host consultation notes to Mac-side seam owners when work touches cross-cutting interfaces |

**Authorization for auto-commit:** the work-producing TASK was Matt-authorized (e.g., "fire dispatch authoring" → dispatch authoring AND its commit are both authorized). Do not re-ask per-commit.

**Authorization scope:** auto-commit applies to work-products of the AUTHORIZED CYCLE / WORKSTREAM. Cross-cycle commits OR scope-amendment commits require fresh Matt-authorization.

### Pushes — REQUIRE Matt-explicit-authorization (default; Mac team + exceptions below)

Push to remote remains Matt-explicit-authorization per ADR-006 read-only-by-default external-systems rule. EXCEPTION: per-workstream push-pattern can be established by Matt authorization (e.g., "push pattern established for this cycle; push after each wave completes" = auto-push for that cycle).

### PC-seam standing wave-close push pattern (established 2026-06-08 post-SSH-key auth)

Following SSH-key-based git auth setup on PC 2026-06-08 (closes the wincredman credential gap; remote `origin` switched from HTTPS to SSH per `git@github.com:mwetmor/reincarnated-collaboration.git`), PC-seam push at wave-close is a STANDING PATTERN, not per-cycle ask. PC team agents (David-H, Radagast, Sam, Mantis) AUTO-PUSH at wave-close per this protocol:

**Pull at wave-start:**
- PC agent runs `git pull origin main` at session-start (already canonical per intro § CRITICAL)
- Additionally pulls at any wave-start within a multi-wave session (rare; explicit when needed)
- The pull captures Mac-side commits authored since the prior PC session — including dispatches, canonical updates, discipline amendments

**Push at wave-close (STANDING — no per-push re-ask):**
- After Sam Gate-2 PASS (or absence of Gate-2 requirement when the work is non-gating) AND David-H session-boundary-memo authored, AUTO-PUSH the wave's accumulated PC commits via `git push origin main`
- The wave-close gate IS the authorization moment; no further re-ask required
- Push fires per SSH-key auth (no credentials prompt; works in SSH session)
- For multi-agent waves (e.g., mantis Phase 1 + 2, david-h Phase 3, sam Phase 4), the wave-close-pushing agent pushes ALL accumulated wave commits together — typically David-H or Sam at the closing phase

**Mid-wave push (exception path; requires Matt-ask):**
- If cross-host coordination requires Mac-side visibility on a mid-wave commit (e.g., gandalf needs to consume a Sam Gate-1 finding before authoring a Mac-side dispatch), PC agent asks Matt for mid-wave push authorization
- Default mid-wave: NO push; accumulate to wave-close

**Cross-cycle / scope-amendment commits (preserved Matt-ask):**
- Still require fresh Matt-authorization per CLAUDE.md addendum standing rules
- Wave-close standing-push applies ONLY to in-scope cycle work products

**Asymmetry with Mac team is intentional:** Mac-side credential setup allows interactive auth flows; Mac push remains per-cycle Matt-ask to preserve ADR-006 read-only-default. PC-side SSH-key auth makes wave-close push operationally clean, and the wave-close gate provides the discipline anchor.

### What anti-patterns this addendum retires

The following patterns are EXPLICITLY ANTI-PATTERNS per this addendum (originally surfaced as knight-rider over-asking behavioral bug; **extended 2026-06-07 to all federated agents including PC team**):
- "Awaiting your direction on (1)+(2)+(3) before firing" for items where (1) and (2) are clearly in-scope orchestration / seam decisions
- "Awaiting your 'commit + push' go" for routine work-products of authorized cycle work (commit auto-fires; push asks)
- "Confirm sequence to proceed" for items that are seam-owner's scope per hive-mind decision-routing directive (Matt 2026-05-23)
- **Per-task confirmation requests during session-start protocol execution** — session-start protocol items (read ground-state, read role-def, pull origin, read in-flight dispatches, read own notes) are NEVER permission-gated; they fire as part of the agent's normal session-start discipline. Asking "should I read X?" is anti-pattern.
- **PC-resident agent over-asking** — PC team (David-H, Radagast, Sam, Mantis) inherits the same auto-commit + autonomous-execution disposition as Mac team. The fact that PC team is SSH-invoked from Mac does NOT make them more cautious; the Matt-authorization at session invocation is identical to Mac-side session invocation.

### Composition with hive-mind decision-routing (Matt 2026-05-23 verbatim)

This addendum composes with hive-mind decision-routing: seam-owners decide in-scope work AND auto-commit its work-products. Matt is LAST-resort escalation for (a) decisions exceeding seam authority per ADR-002 tiered approval, (b) push-to-remote (default), (c) scope-amendment.

### Authority

This addendum is authoritative per Matt 2026-05-25 directive to resolve recurring knight-rider over-asking behavioral bug. Supersedes strict-interpretation of Claude Code system-default commit rule WITHIN this project's multi-agent context. Does NOT affect single-agent Claude Code sessions outside this project.
