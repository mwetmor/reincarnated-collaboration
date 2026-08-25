# MATT DECISION NEEDED — `agentic_orchestration/factory/` has no owner in AGENTS.md

> **Raised:** 2026-08-24, Step-2 VFX build-wave close (five-item ruling batch, item 3).
> **Chain:** jack-ryan Gate-1 INFO → star-lord re-raised and sharpened at build close → jack-ryan ruling batch.
> **Severity:** WARN. Not wave-blocking. Escalated because **seam-ownership assignment is architectural and exceeds ADR-002 documentation-tier**, not because the gap is urgent.
> **Interim in force while you rule:** star-lord holds operational custody of the lane (below). Nothing here pre-commits your ruling.

## The gap, measured

`agentic_orchestration/AGENTS.md` contains **zero occurrences of the string `factory`.** Verified by grep, 2026-08-24. Every other tree in the orchestration directory is attributed to an agent in the § seam map; this one is not.

## What the unowned tree actually holds

Not a scratch directory. Verified by inspection at ruling time:

| Surface | File | What it is |
|---|---|---|
| **Durable lock keyed to host state outside the repo** | `lane.py:210` | `~/.reincarnated/lane-locks/` (overridable via `REINCARNATED_LANE_LOCK_DIR`). Deliberately outside the credential home so an operator can `ls` it. **A repo-resident tree whose correctness depends on machine state no repo commit can see.** |
| **Second-vendor CLI spawn** | `harness/codex.py:180`, `:380`; `harness/grok.py:256` | `subprocess.run` against non-Anthropic vendor CLIs. **The only place in the ecosystem that spawns another vendor's agent.** |
| **Cost ledger** | `receipts.db`, `receipts.py`, `usage.py` | Committed SQLite ledger + accounting. |
| **Auth / permission surface** | `permissions.py`, `host.py`, `sessions/` | Credential-adjacent host configuration. |
| **The board (a view)** | `ui/board.py` | Renders lane state; per Discipline #74 it holds zero authority and imports the owner's derivation rather than deriving its own. |

Whoever owns this tree owns **lane uptime, the cost ledger, and auth health** — three concerns with no current name against them.

**AM-2 widens the same gap.** With the Grok lane admitted (jack-ryan ratification `58d22432`), the tree now spawns *two* vendors' CLIs, and the unowned surface grew rather than stabilised.

## What is being asked of you

One ruling, on a split I recommend rather than a single name.

### Recommendation — split by layer, not by tree

- **`factory/` (lane, harness, jobqueue, receipts, usage, host, permissions, workflow, runner) → star-lord.**
  Direct seam-analogy: star-lord already owns `reincarnated-engine/src/reincarnated/llm/` whose charter in AGENTS.md is *"LLM integration (vendor SDK, prompt templates, **cost tracking**, retries)"* — which is this tree's concern list verbatim, one repo over and one vendor wider. He also built the durable queue and is already the de facto data-path owner.
- **`factory/ui/` → drax.**
  Consistent with his presentation seam and with what the build already does: at ledger L-19 drax deleted his parallel `lane_probe.py` mid-build and imports star-lord's derivation wholesale, so that if the import fails the board renders RED and nothing else. That is Discipline #74 holding at the ownership boundary as well as the data boundary — the view's owner is not the truth's owner, by design.

### Alternatives, and why I did not recommend them

| Option | Assessment |
|---|---|
| **All of `factory/` to star-lord, including `ui/`** | Simpler line. Rejected: it makes one agent both the truth source and the view owner, which is exactly the coupling #74 exists to prevent, and it puts a UI surface in a non-presentation seam. |
| **All of `factory/` to knight-rider** | Defensible — the factory is dispatch-execution substrate and KR owns orchestration. Rejected: KR is a coordinator, not a seam-owning implementer (ADR-001 tier B vs tier C); assigning an uptime/cost/auth surface to the coordinator puts operational on-call in the orchestration layer. |
| **Leave unowned; treat as shared infrastructure** | Rejected: this is the status quo, and the status quo is what star-lord had to re-raise. An unowned lock keyed to host state has no one obliged to notice when it goes stale. |
| **New seam / new agent** | Rejected as premature — the tree's concerns map cleanly onto two existing charters. |

## Interim in force while you rule

**star-lord holds operational custody** of `factory/` — lane uptime, auth health, cost-ledger integrity — effective from this escalation. This is an orchestration-normal interim, not an ownership assignment: it names someone obliged to notice a failure, and it locks nothing. drax continues to own `ui/` de facto, as built.

If you rule differently, the interim unwinds with no artifact to reverse.

## Once you rule

`agentic_orchestration/AGENTS.md` § seam map gains the assignment (jack-ryan writes; documentation-tier once the architectural call is yours). No code moves in either case — this is an attribution gap, not a structural one.

---

**Raised by:** jack-ryan
**Cites:** ADR-001 (team topology tiers) · ADR-002 (tiered approval — seam-ownership assignment exceeds documentation-tier) · Discipline #74 (a view has zero authority) · AM-2 Grok-lane ratification `58d22432`
**Evidence paths:** `agentic_orchestration/factory/lane.py:186-210` · `agentic_orchestration/factory/harness/codex.py:180` · `agentic_orchestration/factory/harness/grok.py:256` · `agentic_orchestration/AGENTS.md` (grep `factory` → 0 hits)
