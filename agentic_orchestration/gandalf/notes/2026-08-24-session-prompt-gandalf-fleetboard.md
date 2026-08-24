# Session-launch prompt — gandalf: fleet flight-recorder + read-only board (U-1) spec-and-grill session (authored by gandalf at VFX-run close, 2026-08-24; Matt fires)

> Paste everything below the line into a fresh gandalf session.

---

Read your operating procedure skill (reincarnated-gandalf-operating-procedure) and execute session-start protocol. Then run this agenda. **This prompt is Matt's go-word for the spec-and-grill work in it. You are `ELICITOR` + `SPEC-AUTHOR` this session — you produce a spec, a grill, and a KR request. You write NO code.**

## The commission in one paragraph

Matt runs a 10-agent fleet across scattered terminals, and the fleet is about to go **multi-provider** (Claude lanes + the proven Codex lane; U-8 contemplates a cross-vendor judge; Grok has a door in U-4). Operational truth — what's running, what it cost, which model earned its tokens, what's waiting on Matt — currently lives in terminal scrollback and dies with the window. `workflow-upgrades.md` § U-1 charters the fix: **(a) a fleet flight-recorder** (forward JSONL capture of per-dispatch lifecycle + tokens + verdicts) and **(b) a read-only board** rendered FROM disk truth. Your job this session: turn U-1 from a backlog paragraph into a **buildable spec** with Matt's rulings elicited and banked, then hand the build to KR for seam routing. The VFX archetype-binding run (SEALED 2026-08-24, 34/34 Codex jobs rc=0, per-job usage JSONL already on disk) is the founding receipts corpus — this is not greenfield; the first data exists.

## Reads (in order, before authoring)

1. `agentic_orchestration/workflow-upgrades.md` — U-1 (the charter; note THE LAW verbatim), U-2 (retrospective mining — optional feeder), U-3 (cache lever — a cost line the recorder should make visible), U-5 (dispatch scorecard — its metrics are the board's outcome columns), U-8 (cross-vendor judge — a future lane the schema must not preclude).
2. `agentic_orchestration/operating-procedures/software-factory.md` — the UI tier ladder (Tier 0→3), the three disciplines (**one data path · read-mostly · no dashboard before receipts**), schema custody (star-lord), seam routing, and the Tier-2 gate (receipts schema stable across ≥2 workflows).
3. `agentic_orchestration/operating-procedures/desirable-run-pattern.md` — the run/ledger vocabulary the recorder must capture (charters, gates, HALTs, veto windows, seals).
4. **The founding receipts:** `agentic_orchestration/research/vfx-p2-dossiers/usage/` (per-job usage JSONL from the VFX run) + `run_p2_serial.sh` beside it (the emitting pattern). Read 2–3 JSONL rows raw — the spec's schema starts from what already exists, not from imagination.
5. `agentic_orchestration/gandalf/notes/2026-08-10-factory-ui-proto-editor-spec.md` — the prior drax UI spec lineage (Tier-2 Glance precedent).
6. `canonical/matt_decision_needed/README.md` + `canonical/matt_to_do/README.md` — the two Matt-queues; the board must surface both.

## Deliverable 1 — the U-1 spec (SPEC-AUTHOR)

File at `agentic_orchestration/gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md`. It must cover:

### Recorder schema — the dimensions (ultra-think these; Matt's explicit ask)

**Identity axes** (every row): provider (anthropic/openai/…) · model + config pin (e.g., `gpt-5.6-sol@xhigh` — pins are law per U-4; a silent vendor model-version change must be DETECTABLE from the record) · lane (claude-agent / codex-serial / future grok / cross-vendor-judge) · operator agent (which named seam agent fired it) · dispatch/run/wave ID (join key to the ledger world) · seam/repo touched.

**Cost axes:** tokens in/out/cached/reasoning · **subscription-window attribution** — Claude Max 5-hour windows + weekly caps vs Codex ChatGPT-subscription spend are DIFFERENT economies; the record must let Matt answer "what did this run cost me in each currency" and "which window did it burn" · wall-time · retry count · cache hit-rate (the U-3 lever needs a measurement to prove itself).

**Outcome axes** (U-5's scorecard, made queryable): verdict enum (PASS / PASS-with-findings / BLOCK / refusal / HALT / fallback-taken) · first-pass gate rate · rework-chain length · curation WARN rate · fabrication-check result · time-to-seal. **Per-model scorecards across time** is the payoff query: "is the Codex lane's quality drifting," "did the pin change move the gate rate," A/B pin history per U-4's template.

### Board content — what scattered terminals lose (the second half of Matt's ask)

The board is Tier-1/Tier-2 per the factory ladder, rendered FROM disk, and answers the four questions (what's running / what's red / what did it cost / what's waiting on Matt). Enumerate as board lanes at minimum:

- **AWAITING MATT** — top of board, always. HALTs, open veto windows, `matt_decision_needed/` + `matt_to_do/` queue states. Matt's attention is the fleet's scarcest resource; this lane IS the product.
- **IN-FLIGHT** — background agents + runs, with staleness age (the six stalled 2026-07-22 engine-seam dispatches are the exhibit: work went stale silently for a month; the board makes stale LOUD).
- **AT GATE** — Gate-1/Gate-2/minted-gate items with owner named.
- **HEALTH** — auth expiries (Codex `~/.codex/auth.json`, GitHub OAuth), throttle/window state, scheduled crons/wakeups, disk-space watchers (PL-5 precedent), **unpushed commits across the four repos**, unswept `requests/` dirs (the L-31 lesson: owners sweep at phase boundaries — the board can show the un-swept).
- **SEALED/DONE** — with cost + verdict rollups feeding the per-model scorecards.

### The constitution (carry verbatim into the spec)

- **THE LAW (U-1):** the board is a VIEW. Zero authority. Never in the data path. No agent reads the board to decide anything; disk artifacts remain the only truth.
- **Three disciplines (software-factory.md):** one data path · read-mostly · **no dashboard before receipts** — recorder (a) ships and accumulates BEFORE board (b) renders; the VFX usage JSONL partially satisfies this, a second workflow's receipts complete the Tier-2 gate.
- Recorder writes are append-only JSONL; schema custody is **star-lord's** once ratified.

## Deliverable 2 — the grill (ELICITOR; forks for Matt, decision-shaped, you lean but Matt rules)

At minimum: **F-1** board home (Glance app vs local markdown/HTML render vs terminal TUI — tradeoffs incl. iOS visibility) · **F-2** staleness SLA (when does IN-FLIGHT turn red — hours? days? per-class?) · **F-3** card grain (dispatch vs run vs wave — what's one card?) · **F-4** Tier-3 iOS-push timing (now, or only after Tier-2 proves itself — the ladder says gate it) · **F-5** subscription-window reporting shape (per-window burn report vs rolling daily) · plus any forks your read surfaces. File resolved rulings; anything unruled goes to `matt_decision_needed/`.

## Deliverable 3 — the KR carve-out request

File at `agentic_orchestration/gandalf/requests/<date>-knight-rider-u1-fleetboard-build.md` with the seam routing pinned: **star-lord** builds recorder (a) + owns receipts schema (per software-factory custody; composes with his `factory/harness/codex.py` queue task from the Step-2 KR prompt — the queue emits U-1 rows from day one, same schema, ONE data path) · **drax** builds board render (b) AFTER receipts accumulate · **jack-ryan** ratifies schema + THE LAW as discipline · **galadriel** screenshot-verifies any Tier-2 surface · **KR** sequences. gandalf specs and audits; gandalf builds nothing.

## Optional parallel commission

If Matt nods mid-session: **U-2 retrospective mining** as a legolas Mode-A style backfill — walk git history + CHANGELOG + old dispatch records to seed the scorecards with historical rows (clearly flagged `backfill=true`; forward capture stays the primary spine).

## Boundaries

- No code, no schema DDL, no board prototype this session — spec + grill + request only.
- Do not weaken THE LAW to make any fork easier; a board with authority is the rejected failure mode.
- Tier-2 gate (receipts stable across ≥2 workflows) is jack-ryan's to ratify, not yours to waive.
- Push discipline: commit deliverables per auto-commit addendum; ask Matt before push if no session pattern is set.
