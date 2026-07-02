# CLAUDE.md — reincarnated-collaboration meta-repo

**You are in the meta-repo.** This directory is the design/coordination hub for the Reincarnated project. The actual codebases are siblings:

- `~/Games/reincarnated-engine/` — Python engine (content gen, simulation, balance, telemetry, LLM)
- `~/Games/reincarnated-demo/` — Pixi.js demo (player-facing demo1)
- `~/Games/reincarnated-loadout/` — React/Vite loadout web app (deployed to Vercel)
- `~/Games/reincarnated-godot/` — Godot 4.x / GDScript 3D-scene presentation prototype (Mac-resident; Synty POLYGON assets, Forward+/Metal renderer, MP4 walkthrough harness; enchanted-forest ravine combat level). Owned by drax (presentation seam) per Matt-approved scope amendment 2026-06-21. (Godot-on-Mac superseded the cancelled Unreal/PC seam, retired 2026-06-30.)

## Synthetic engineering team

  > **Orientation:** Engine first. Game second. Phase third.                                                                                                                                                                                                                                                                                  
  > Engine = architectural integrity (substrate-led discipline; canonical docs).
  > Game = player-facing quality. Phase = operational unit (waves, dispatches).                                                                                                                                                                                                                                                               
  > Conflict resolution: engine > game > phase. 

A **10-agent Mac-resident agentic team** (plus Matt) operates across all repos. **Read `agentic_orchestration/AGENTS.md` first.**

> **The PC-resident team (David-H, Radagast, Sam, Mantis) retired 2026-06-30.** It existed to serve Unreal-Engine work, which was cancelled in favor of Godot-on-Mac (drax owns `reincarnated-godot/`). The agents, their skills, the founding commit doc, and all two-host coordination machinery (SSH/WSL/tmux launch, PC pull/push discipline, PC Remote Control) were removed. Lineage is in git.

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
```

## Mobile-accessible sessions via Claude Code Remote Control (established 2026-06-08)

Claude Code Remote Control (v2.1.51+) makes local sessions mobile-accessible via the Claude iOS app. **Per-machine policy** (confirmed via hypothesis test 2026-06-08): one Remote Control server per host, with up to 32 concurrent sessions per server. Mac and PC count separately.

```bash
# === Mac Remote Control (gandalf / knight-rider / jack-ryan / specialists) ===
# In a separate Mac terminal window (not your active interactive session):
cd ~/Games/reincarnated-collaboration
claude remote-control --name "Mac RC"
# Spawn mode: 1 (same-dir; default) for shared working tree
# 2 (worktree) for isolated git worktrees per session
```

**Agent role adoption pattern (v2.1.169+ — `--agent` flag removed from `remote-control` subcommand):** Remote Control servers run as generic Claude Code spawn-servers. Agent role is set by **prompt at session engagement**, not at invocation. After connecting from iOS, prompt the session with role-adoption text:

```
Read your operating procedure skill (reincarnated-<agent>-operating-procedure) and execute session-start protocol per OP § 1. Then await my direction.
```

The session reads the OP + role definition + session-start docs and operates as that agent from that point.

**Operational notes:**
- Remote Control servers must keep their interactive process alive (Mac terminal window OR PC SSH session). Closing kills the server.
- Mac Mini configured for no-sleep supports this naturally
- Session conversation history persists across iOS app flips — switching from gandalf session to KR session in iOS doesn't kill either
- GitHub OAuth re-auth (Issue #44805 workaround): claude.ai → Settings → Account → GitHub
- Cross-cycle credential durability: switch git remote to SSH-key auth at project init for any host running Remote Control; HTTPS credential helpers (osxkeychain / wincredman) fail in non-interactive contexts

## Where to find things

| Need | Path |
|---|---|
| **Canon router — FIRST READ, every session** | `canonical/00-ground-state.md` (thin router to the three canon homes) |
| **STORY spec (end-state)** — *Reap. Die. Rise.* death-faith frame, keystone, gameplay loop, style register | `canonical/reap-die-rise-story/` (read `00-index.md` first) |
| **ENGINE spec (end-state)** — generation, simulation, balance, gear/stat/T4, progression, build/perf stack | `canonical/reap-die-rise-engine/` (read `00-index.md` first) |
| **Build-vs-spec deltas + forward sequencing** — what's owed, open queues (replaces the retired roadmap) | `canonical/current-to-end-state/` (`…-engine.md` / `…-story.md` / `…-game.md`) |
| **Matt decision queue** — human-in-the-loop items; check at session start/end | `canonical/matt_decision_needed/` |
| Team topology + scope map | `agentic_orchestration/AGENTS.md` |
| Founding ADRs | `agentic_orchestration/GOVERNANCE.md` |
| Review process + 5 principles | `agentic_orchestration/REVIEW_PROCESS.md` |
| Latest handoff context | `agentic_orchestration/skill_handoff_<date>.md` |
| Team event log | `agentic_orchestration/CHANGELOG.md` |
| Engineering disciplines | `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` |
| Decisions log | `~/Games/reincarnated-engine/design/decisions/decisions-log.md` |
| Anything older (superseded designs, wave records, the old numbered `canonical/NN` root docs) | **git history** — searchable, not pre-load |

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

The Claude Code system-default commit rule ("NEVER commit changes unless the user explicitly asks") was designed for single-user single-agent scenarios. The reincarnated-collaboration meta-repo runs a **10-agent Mac-resident synthetic engineering team** where routine in-scope work-products SHOULD auto-commit without per-commit re-asking.

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

**Authorization for auto-commit:** the work-producing TASK was Matt-authorized (e.g., "fire dispatch authoring" → dispatch authoring AND its commit are both authorized). Do not re-ask per-commit.

**Authorization scope:** auto-commit applies to work-products of the AUTHORIZED CYCLE / WORKSTREAM. Cross-cycle commits OR scope-amendment commits require fresh Matt-authorization.

### Pushes — REQUIRE Matt-explicit-authorization

Push to remote remains Matt-explicit-authorization per ADR-006 read-only-by-default external-systems rule. EXCEPTION: per-workstream push-pattern can be established by Matt authorization (e.g., "push pattern established for this cycle; push after each wave completes" = auto-push for that cycle).

### What anti-patterns this addendum retires

The following patterns are EXPLICITLY ANTI-PATTERNS per this addendum (originally surfaced as knight-rider over-asking behavioral bug):
- "Awaiting your direction on (1)+(2)+(3) before firing" for items where (1) and (2) are clearly in-scope orchestration / seam decisions
- "Awaiting your 'commit + push' go" for routine work-products of authorized cycle work (commit auto-fires; push asks)
- "Confirm sequence to proceed" for items that are seam-owner's scope per hive-mind decision-routing directive (Matt 2026-05-23)
- **Per-task confirmation requests during session-start protocol execution** — session-start protocol items (read ground-state, read role-def, read in-flight dispatches, read own notes) are NEVER permission-gated; they fire as part of the agent's normal session-start discipline. Asking "should I read X?" is anti-pattern.

### Composition with hive-mind decision-routing (Matt 2026-05-23 verbatim)

This addendum composes with hive-mind decision-routing: seam-owners decide in-scope work AND auto-commit its work-products. Matt is LAST-resort escalation for (a) decisions exceeding seam authority per ADR-002 tiered approval, (b) push-to-remote (default), (c) scope-amendment.

### Authority

This addendum is authoritative per Matt 2026-05-25 directive to resolve recurring knight-rider over-asking behavioral bug. Supersedes strict-interpretation of Claude Code system-default commit rule WITHIN this project's multi-agent context. Does NOT affect single-agent Claude Code sessions outside this project.
