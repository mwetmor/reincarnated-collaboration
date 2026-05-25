# CLAUDE.md — reincarnated-collaboration meta-repo

**You are in the meta-repo.** This directory is the design/coordination hub for the Reincarnated project. The actual codebases are siblings:

- `~/Games/reincarnated-engine/` — Python engine (content gen, simulation, balance, telemetry, LLM)
- `~/Games/reincarnated-demo/` — Pixi.js demo (player-facing demo1)
- `~/Games/reincarnated-loadout/` — React/Vite loadout web app (deployed to Vercel)

## Synthetic engineering team

A 6-entity agentic team operates across all repos. **Read `agentic_orchestration/AGENTS.md` first.**

Quick launch:

```bash
# Coordinator session (start of day)
cd ~/Games/reincarnated-collaboration && claude --agent knight-rider

# Specialist sessions (task work)
cd ~/Games/reincarnated-engine && claude --agent gamora       # or rocket, star-lord
cd ~/Games/reincarnated-loadout && claude --agent drax        # or reincarnated-demo

# QA session
cd ~/Games/reincarnated-collaboration && claude --agent jack-ryan
```

## Where to find things

| Need | Path |
|---|---|
| Team topology + scope map | `agentic_orchestration/AGENTS.md` |
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

The Claude Code system-default commit rule ("NEVER commit changes unless the user explicitly asks") was designed for single-user single-agent scenarios. The reincarnated-collaboration meta-repo runs a 10-entity synthetic engineering team (per `agentic_orchestration/AGENTS.md`) where routine in-scope work-products SHOULD auto-commit without per-commit re-asking.

This addendum refines the system-default rule for team-level operation:

### Commits — AUTO-FIRE without per-commit Matt re-asking

Seam-owning agents AUTO-COMMIT routine work-products from authorized in-scope work. Examples:

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

### Pushes — REQUIRE Matt-explicit-authorization (default)

Push to remote remains Matt-explicit-authorization per ADR-006 read-only-by-default external-systems rule. EXCEPTION: per-workstream push-pattern can be established by Matt authorization (e.g., "push pattern established for this cycle; push after each wave completes" = auto-push for that cycle).

### What anti-patterns this addendum retires

The following knight-rider patterns are EXPLICITLY ANTI-PATTERNS per this addendum:
- "Awaiting your direction on (1)+(2)+(3) before firing" for items where (1) and (2) are clearly in-scope orchestration decisions
- "Awaiting your 'commit + push' go" for routine work-products of authorized cycle work (commit auto-fires; push asks)
- "Confirm sequence to proceed" for items that are seam-owner's scope per hive-mind decision-routing directive (Matt 2026-05-23)

### Composition with hive-mind decision-routing (Matt 2026-05-23 verbatim)

This addendum composes with hive-mind decision-routing: seam-owners decide in-scope work AND auto-commit its work-products. Matt is LAST-resort escalation for (a) decisions exceeding seam authority per ADR-002 tiered approval, (b) push-to-remote (default), (c) scope-amendment.

### Authority

This addendum is authoritative per Matt 2026-05-25 directive to resolve recurring knight-rider over-asking behavioral bug. Supersedes strict-interpretation of Claude Code system-default commit rule WITHIN this project's multi-agent context. Does NOT affect single-agent Claude Code sessions outside this project.
