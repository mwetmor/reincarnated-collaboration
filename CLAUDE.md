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
