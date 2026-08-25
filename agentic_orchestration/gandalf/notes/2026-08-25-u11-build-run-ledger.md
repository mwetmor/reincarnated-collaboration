# RUN U11-BUILD — run ledger (veto-open; every ruling reversible by Matt)

**Charter (Matt 2026-08-25, verbatim):** *"yes, let's adopt U-11. Please run it here."* — adopt U-11 (Claude-lane usage emitter) and conduct its build autonomously in this session.
**Conductor:** gandalf (RUN-CONDUCTOR). **Pattern:** `operating-procedures/desirable-run-pattern.md` — fit test F1–F4 all YES (ruled pre-launch, this session).
**Spec of record:** `agentic_orchestration/workflow-upgrades.md` § U-11 (ADOPTED stamp same commit as this ledger).
**Lineage:** direct sequel to RUN U1-BUILD (sealed 2026-08-25T01:28Z; seal report `gandalf/notes/2026-08-24-u1-build-run-SEAL.md`). Schema v1.1, THE LAW (#74), G-2c-R1 backfill ruling, and R-L47-2 derived-summary discipline all carry forward as standing law.

---

## Substrate (frozen at launch, 2026-08-25T14:10Z conductor census)

Claude Code session transcripts under `~/.claude/projects/`:

| project dir | top-level session transcripts | nested sub-agent tapes |
|---|---|---|
| `-Users-admin-Games-reincarnated-collaboration` | 26 | 647 (`<sessionId>/subagents/agent-*.jsonl`) |
| `…-collaboration-agentic-orchestration-factory` | 4 | — |
| `…-star-lord-notes-evidence-2026-08-11-tool-fence-probes` | 5 | — |
| other reincarnated dirs (demo/engine/loadout/side-seed) | 0 | — |

Each usage-bearing message carries `usage` (`input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`) + `sessionId`, `timestamp`, `cwd`, resolved model id (verified pre-adoption: 412 usage-bearing messages in the U1-BUILD conductor transcript alone). **Read-only substrate — zero write verbs against any transcript, ever.**

Live-session caveat: the substrate GROWS while the run breathes (this conductor session is itself in it). Bounding is by definition + quiescence rule (R-6), not by a frozen file list.

## Decidable target-state (the run checks these without Matt)

- **T1** — star-lord emitter exists (read-only; one data path; validator-clean rows appended to `flight/records-2026-08.jsonl` for the quiescent 2026-08 session set).
- **T2** — tape audits clean post-emission: schema validator, `check_append_only`, `retrospection_audit` (every U-11 row declares `backfill:true` per G-2c-R1 temporal ruling).
- **T3 (the empirical criterion, verbatim from the spec)** — Claude lanes render token + cache-hit% columns beside Codex's on the same board/report, derived from rows; U-3's before/after becomes a per-lane query.
- **T4** — jack-ryan gate G-U11 PASS (incl. the rev-1.2 provenance-trigger ruling recorded).
- **T5** — run lifecycle rows on tape (`run:U11-BUILD` OPEN/CLOSE); seal predicate = T1–T4 ✓ + fold commits pushed.

**Honorable fallback:** if per-session workstream attribution proves underivable at scale, rows land with honest-null `workstream` — T3 is a LANE-level criterion, not a per-workstream one. Attribution gaps are findings, not blockers.

## Gates (pre-registered)

- **G-U11 (jack-ryan, single gate):** schema v1.1 conformance (NO schema amendment expected — token fields exist); THE LAW audit (zero write verbs, one data path, honest nulls, no LLM in truth path); backfill declaration on every row; **rules whether U-11 is the rev-1.2 "first instrumented emitter" trigger** (conductor lean: NO — U-11 reads after the fact; the trigger stays armed for a live in-harness emitter); derived-not-literal tests (R-L47-2 standing — no hand-counted literals over the growing tape); append-only audit over the fold's commit range.
- **Conductor verification (no galadriel required):** `bin/flight_report` text render + board HTTP fetch show the Claude token/cache-hit% cells; prod Glance rides the push (`.vercelignore` already globs `flight/records-*.jsonl` — L-34 fix) with a DATA-PRESENCE assertion on the deployed state (the L-33/L-34 verification-target lesson, applied).

## Matt interface (declared)

Push-as-you-go at each fold; red-flag pings only; seal report at close. Commitment-boundaries (schema amendment, tape-law change, anything touching Matt-reserved territory) HALT.

---

## L-1 — Launch fork rulings (reasoning-boundaries, ruled in-run; veto-open)

- **R-1 · Row grain = one row per SESSION**, aggregating the session's main transcript **plus its `subagents/` tree** (the 647 nested tapes fold into their parent sessions — sub-agent tokens are the session's economy; omitting them would understate Claude-lane cost by potentially the majority share). `derived_from` pins the session dir. Per-message grain REJECTED (row explosion, no owner-question needs it).
- **R-2 · Scope = sessions in the three transcript-bearing reincarnated dirs whose usage messages fall in 2026-08**; month assignment by LAST usage timestamp (matches the monthly-tape law; a session spanning a month boundary lands once, in its closing month).
- **R-3 · Workstream mapping** derivable via the custody ledger (`lanes/agents/_custody.tsv` holder-session ids), run ledgers, and dispatch records; **honest-null where not derivable**. No inference, no guessing, no LLM in the truth path.
- **R-4 · Provenance:** every U-11 row is retrospective-authored → `backfill:true` (G-2c-R1: backfill is TEMPORAL). The rev-1.2 provenance-axis trigger question routes to jack-ryan at G-U11 (conductor lean recorded above).
- **R-5 · Schema v1.1 UNCHANGED.** Existing token fields carry the four usage axes (`cache_creation_input_tokens` → cache-write; `cache_read_input_tokens` → cached-input). Lane/currency vocabulary already carries Claude lanes + `anthropic-max`. Any field the builder finds missing is a HALT-to-conductor, not an improvised extension.
- **R-6 · Quiescence rule (the live-substrate fork):** emit rows only for sessions with no transcript mtime change for ≥60 min at scan; the emitter is idempotent and re-runnable (dedupe by sessionId — a session gets exactly one row, appended once it goes quiet). The conductor's own live session gets its row on a post-seal re-run, not mid-run. Correction rows (`corrects:` chain) remain the ONLY amendment path if a quiescent session later resumes — expected rare; a finding if frequent.
- **R-7 · No drax work chartered.** Board/report token columns fill from rows via the existing one-data-path derivations. If a render defect surfaces it is a FINDING routed post-run, not in-run scope growth.

## L-2 — Launch fold

Custody: star-lord seam verified FREE (last row RELEASE 01:51:27Z); jack-ryan FREE (RELEASE 02:52:33Z). CLAIM row for star-lord appended per § 11.3 in this fold. Adoption stamped in `workflow-upgrades.md` same commit. B-1 (emitter build) dispatches to the named star-lord sub-agent on push.

## L-3 — B-1 FOLDED (star-lord commit `7f71ee5b`; conductor re-verified)

**27 rows appended** (tape 75→102): 8,442,547,650 tok-in · **97.58% cache-hit** · 204.1M cache-write · 19.3M out · 49,590 API calls. Skips all classified: 4 non-quiescent (incl. this conductor session — R-6 working as designed), 4 non-August, 0 no-usage. **Idempotence proven on the live tape** (second run appended 0, 27× already-emitted). Suite **104/104 re-run from conductor hands**; whole-tape validator CLEAN (102), retrospection audit CLEAN (all U-11 rows `backfill:true`), `check_append_only` 27/0. Both T3 tests were red-before-emission — pre-registered goalposts doing their job. **T1 ✓ T2 ✓ T3 ✓ (conductor-verified in `flight/report.md`: anthropic row 8442.5M / 97.6% / 19.3M beside Codex 72.4M / 93.2%).** R-7 held: zero render work.

**Findings register (→ G-U11 unless noted):**
- **F-1 (RULING REQUESTED):** `tokens_input` = SUM of anthropic's three input components (anthropic's `input_tokens` EXCLUDES cache reads/writes; OpenAI's includes them). Conductor lean: **RATIFY** — sum is the cross-lane-comparable total; the alternative renders cache-hit at thousands of percent. jack-ryan rules.
- **F-2:** 42,595 repeated transcript lines (46%) discarded via `message.id` dedupe — double-count hazard measured, not guessed.
- **F-3:** mixed denominators on the anthropic scorecard row (`tok-in/artifact` 1055.3M over 8 artifacts; `med wall` 69m over 1 duration, across 29 units) — reported not patched (R-7); post-run render backlog.
- **F-4:** U-11 rows are host-local (`derived_from` absolute paths — transcripts live in no repo). Standing fact for consumers.
- **F-5 (governance candidate):** attribution 0/27 derived — the mechanical index works (fixture-proved) but **nothing durable in the repo records which session did which work**; the one real session-id fragment in custody belongs to the still-live conductor session. Candidate: session-id in completion records / custody rows as standing discipline.
- **F-6 (conductor-spotted, → G-U11):** the tool-fence-probe rows carry `model_echo:"<synthetic>"` with all-zero token fields — gate should confirm these are measured zeros (recorded usage blocks valued 0), not nulls rendered as zeros (honest-null law, colour-layer class).

R-3 fallback exercised as chartered: T3 is lane-level; workstream honest-null on 27/27. Custody: star-lord RELEASED this fold; jack-ryan CLAIM for G-U11 follows.
