# U-1 — Fleet Flight-Recorder + Read-Only Board — build spec (DRAFT)

**Date:** 2026-08-24 · **Author:** gandalf (SPEC-AUTHOR; grill by ELICITOR — § 9)
**Status:** DRAFT — awaiting (1) Matt rulings on forks F-1…F-8 (§ 9; queue row Q61), (2) jack-ryan
ratification of the record schema + THE LAW as discipline. **On ratification, schema custody
transfers to star-lord** (software-factory § 8: one schema, one custodian, many readers) and this
doc's § 3 becomes the schema's founding version, versioned forward by star-lord.
**Governing docs:** `agentic_orchestration/workflow-upgrades.md` U-1 (the charter) ·
`operating-procedures/software-factory.md` § 7 (tier ladder + three UI disciplines) + § 8 (custody) ·
`operating-procedures/desirable-run-pattern.md` (run vocabulary the recorder captures) ·
`gandalf/notes/2026-08-10-factory-ui-proto-editor-spec.md` (Spec B — the Tier-2 UI lineage this
board composes with).
**Builders:** star-lord (recorder, § 4–§ 5) · drax (board, § 6, gated) · gandalf writes no code.

---

## 0 · The owner's question (rubric law — name it before the predicates)

Matt, verbatim (workflow-upgrades header): *"I need to see, historically, what happened so I can
work towards improvements on scope, cost, prompt success/efficiency, model success/efficiency."*

Operationalized as the four board questions (software-factory § 7 Tier 2):
**what's running? · what's red? · what did it cost? · what's waiting on Matt?**

Everything below serves that rubric. Any predicate in this spec that answers a narrower question
than these is intent leak (desirable-run-pattern § 6.3) and loses to the rubric.

## 1 · The founding corpus (this is not greenfield)

The VFX archetype-binding run (SEALED 2026-08-24) left the first receipts on disk at
`agentic_orchestration/research/vfx-p2-dossiers/`:

- **Lifecycle half:** `usage/_run-log.tsv` — 30 rows, schema `ts · job · rc · start/end · dossier_bytes`.
- **Usage half:** per-job raw Codex event streams (`usage/NN-*.jsonl`); each carries exactly one
  `turn.completed` row: `{"usage":{"input_tokens","cached_input_tokens","cache_write_input_tokens",
  "output_tokens","reasoning_output_tokens"}}`.
- **Emitter pattern:** `run_p2_serial.sh` — serial law, idempotency skip, per-job `.jsonl` + `.err`,
  TSV append at close.

Aggregate, reproduced from the artifacts (mechanical sum over the 30 `turn.completed` rows, per
the per-landing law — never from a report): **input 72,375,471 · cached 67,431,424 (93.2%) ·
output 259,471 · reasoning 154,000.** One founding observation falls out immediately: a 30-job
research lane consumed ~72M input tokens and the cache absorbed 93.2% of them — exactly the
measurement class U-3 needs and nothing was capturing before this run. The recorder makes this
routine instead of archaeological.

**What the founding corpus teaches the schema:** capture already splits into (a) lifecycle events
(cheap, TSV-shaped, harness-emitted) and (b) vendor usage streams (raw, vendor-shaped, format
varies by provider). The recorder therefore normalizes BOTH into one row stream while **retaining
the raw vendor stream beside it as evidence** — every normalized number must be reproducible from
a named raw artifact (`derived_from` pointer, § 3.5).

## 2 · Architecture — three layers, one law

| Layer | What | Owner |
|---|---|---|
| **CAPTURE** | Lane emitters append events at lifecycle boundaries (enqueue/start/gate/close…). Raw vendor streams retained beside. | each lane's operator; star-lord provides the appender |
| **RECORD** | ONE append-only normalized JSONL stream — the truth-of-record for fleet telemetry. Schema § 3. | star-lord (custody post-ratification) |
| **VIEW** | Tier-1 generated report → Tier-2 board, rendered FROM the record + read-only disk probes. Rebuilt on refresh; cannot desync. | drax (gated, § 6) |

### The constitution (carried verbatim; non-negotiable)

- **THE LAW (U-1):** the board is a VIEW. Zero authority. Never in the data path. No agent reads
  the board to decide anything; disk artifacts remain the only truth.
- **Three disciplines (software-factory § 7):** (1) **one data path** — the view reads the same
  store the emitters write; a view is never truth; (2) **read-mostly** — the board writes nothing
  in v1 (not even annotations; Spec B's annotate verb is factory-receipts-side, not fleet-side);
  (3) **no dashboard before receipts** — recorder (a) ships and accumulates BEFORE board (b)
  renders. The VFX corpus is workflow #1; the Tier-2 gate needs the schema stable across ≥2
  workflows (jack-ryan ratifies gate passage — not waivable here).
- **Append-only.** Rows are never edited or deleted. A wrong row is corrected by a superseding row
  (`corrects: <row_id>`), never by rewrite — the flight-recorder property is that the tape does
  not lie about what was believed at the time.
- **Telemetry, not content.** Rows carry identifiers, counts, timestamps, enums, artifact paths —
  never work-product bodies. (Keeps rows cheap, greppable, and clean under the D3 privacy posture.)

## 3 · The record schema — v1

**Grain: EVENT rows, joined by `unit_id`.** A unit's state is the fold of its events (latest
governs); IN-FLIGHT is "START seen, no terminal event"; staleness is `now − last event`. This is
what makes the board derivable rather than maintained — and it matches how the desirable-run
pattern already talks (charters, gates, HALTs, seals are *events* in a run's life).

### 3.1 Event types (v1)

| `event` | When | Terminal? |
|---|---|---|
| `ENQUEUE` | unit queued (dispatch authored, job queued) | no |
| `START` | execution begins (attempt N) | no |
| `GATE` | a gate fires (Gate-1 / Gate-2 / minted gate / curation gate) with a verdict | no |
| `HALT` | commitment-boundary halt to Matt; veto window open; honorable pause | no |
| `CURATION` | downstream verifier files WARN count / fabrication-check result | no |
| `SNAPSHOT` | subscription-meter reading (§ 5) — not unit-bound (`unit_id` null) | no |
| `CLOSE` | unit reaches a terminal verdict; carries cost totals + artifact refs | **yes** |

### 3.2 Common fields (every row)

| Field | Type | Notes |
|---|---|---|
| `v` | int | schema version, `1` |
| `ts` | ISO-8601 UTC | event time |
| `event` | enum § 3.1 | |
| `unit_id` | string | join key — dispatch/job/run/wave id (null on SNAPSHOT) |
| `unit_kind` | enum | `job · dispatch · run · wave · session` |
| `parent_id` | string? | hierarchy: job→run→wave. Makes the schema **grain-agnostic** — F-3 (card grain) binds only the board render, never the record |
| `workstream` | string | charter/run name (`VFX-AB`, `KC2-MC`, `U1-BUILD`, …) |
| `operator` | string | the NAMED seam agent that fired/owns it (lanes get operators, not seats — U-4) |
| `seam` / `repo` | string | seam touched / repo touched |
| `backfill` | bool | `true` only for U-2 retrospective rows — historical rows never masquerade as forward capture |
| `corrects` | string? | row-id of a superseded row (append-only correction path) |

### 3.3 Identity axes (on START and CLOSE)

| Field | Notes |
|---|---|
| `provider` | `anthropic · openai · xai · …` |
| `lane` | `claude-agent · claude-subagent · codex-serial · grok-judge(future) · cross-vendor-judge(future)` — U-8 needs a new enum value, not a new schema |
| `pin` | the config-of-record WE requested, e.g. `gpt-5.6-sol@xhigh` (U-4: pins are law; every banked lane statistic is measured at a pin) |
| `model_echo` | the model string the VENDOR reports back in-stream, verbatim, or `null` if the stream doesn't echo one. **Silent vendor version-change detection = `pin` vs `model_echo` drift over time**, surfaced in the board HEALTH lane |
| `harness` / `harness_version` | `codex-cli 0.147.0`, `claude-code 2.x`, `factory-spine 0.x` — a silent CLI update is a confound the same way a silent model change is; recorded so an A/B across time can hold it constant |
| `currency` | `anthropic-max · chatgpt-sub · api-metered` — the economy this unit burns (§ 5) |

### 3.4 Cost axes (on CLOSE; primitives only — metrics are DERIVED, never stored)

| Field | Source |
|---|---|
| `tokens_input · tokens_cached_input · tokens_cache_write · tokens_output · tokens_reasoning` | normalized from the vendor stream (Codex `turn.completed.usage` maps 1:1; Claude-lane per § 4.3). Reasoning is a share of output, never a fifth addend (Spec A convention) |
| `rc` | process exit code (mechanical lanes) |
| `attempt` / `retry_of` | attempt number; unit-id of the attempt this reworks — rework chains are LINKS, their length is a query |
| `artifacts` | paths + byte-sizes of primary outputs (the `dossier_bytes` pattern, generalized) |

**Derived-not-stored (the derived-summary discipline, R-L47-2 lineage):** cache hit-rate ·
wall-time · time-to-seal · first-pass gate rate · rework-chain length · per-model scorecards ·
window burn. All are queries over rows. A stored summary is a hand-written count waiting to be
wrong; four summary-count defects in one run (KC2-MC INFO-8 class) bought this rule.

### 3.5 Outcome axes (on GATE / CURATION / CLOSE)

| Field | Notes |
|---|---|
| `verdict` | `PASS · PASS-WITH-FINDINGS · BLOCK · REFUSAL · HALT · FALLBACK-TAKEN · FAILED · SKIP` (SKIP is real — `SKIP-EXISTS` idempotency rows exist in the founding TSV) |
| `gate_id` / `gatekeeper` | on GATE rows — which gate, which named agent judged |
| `warn_count` / `fabrication_check` | on CURATION rows (`pass · fail · not-run`) — the oversold-`whirlwind#1` catch class, made countable |
| `derived_from` | path to the raw vendor stream / artifact this row's numbers reproduce from — **every number in a row is reproducible from a named artifact** (per-landing law, compiled into the schema) |

### 3.6 The payoff queries (what the axes buy — the spec's acceptance shape)

1. **Per-model scorecard across time:** for each (`provider`,`pin`): first-pass gate rate, WARN
   rate, fabrication-check rate, tokens per accepted artifact, median wall-time — windowed by
   month. Answers "is the Codex lane's quality drifting" and "did the pin change move the gate
   rate" (U-4 A/B template becomes a query).
2. **Run cost card:** for a `workstream`: totals per currency, cache hit-rate, retries, time
   enqueue→seal. Answers "what did this run cost me in each currency."
3. **Attention ledger:** all open HALT events + veto windows, oldest first. The AWAITING-MATT lane.
4. **Drift tripwires:** `model_echo ≠ pin` incidents; `harness_version` changes mid-workstream;
   cache hit-rate collapse on a lane (the U-3 signature).

## 4 · Emitters — who writes rows, and honest coverage

### 4.1 Storage (lean; F-6/F-8 rule the final shape)

`agentic_orchestration/flight/records-YYYY-MM.jsonl` — fleet-wide home (the factory is one emitter
among several, so the record lives above `factory/`), monthly files, committed to git (durable,
multi-session-visible, small text). Raw vendor streams stay beside their runs (the VFX pattern);
rows point at them via `derived_from`.

### 4.2 Scripted lanes (full coverage, day one)

- **Codex serial lane:** the `run_p2_serial.sh` pattern generalized — star-lord's
  `factory/harness/codex.py` queue (Step-2 KR prompt) emits `ENQUEUE/START/CLOSE` rows natively,
  same schema, ONE data path. The queue's rows ARE its flight recorder from birth (U-1 charter).
- **Factory spine (F1, when it lands):** the spine's SQLite receipts remain workflow-internal
  detail; the spine emits one U-1 row per phase-close, derived from its own receipts. (F-6 lean:
  JSONL is fleet truth-of-record; any SQLite is either workflow-internal or a derived, rebuildable
  index — never a second truth.)
- **Background Bash/cron tasks:** a ~20-line appender (`flight_record.py` or shell function),
  star-lord-built, wraps any lane cheaply.

### 4.3 Interactive Claude sessions (partial coverage, declared — never fabricated)

Interactive sessions don't surface per-turn token usage the way `codex exec --json` does. v1 is
honest about this: **lifecycle rows only** (session START/CLOSE via Claude Code hooks —
SessionStart/Stop hooks are the candidate mechanism, star-lord's build call), token fields `null`,
plus SNAPSHOT events bracketing sessions where a `/usage`-class meter is readable. Token-coverage
depth for the Claude lane is fork **F-7**; the U-3 attribution audit is its natural empirical
input. **A null is a fact; an estimated token count in a truth-of-record stream is a fabrication.**

## 5 · Subscription-window attribution (the two-economies problem)

Claude Max (5-hour rolling windows + weekly caps) and Codex ChatGPT-subscription (its own limits)
are different currencies; neither exposes a queryable ledger API from our side. The recorder
therefore does not MODEL windows — it MEASURES them:

- **`SNAPSHOT` events:** whenever a meter is readable (session start/end `/usage` surface;
  Codex stream rate-limit fields where present; `codex login status`), append a snapshot row
  `{currency, meter_raw, ts}` with the meter's own vocabulary preserved raw. Window burn derives
  from differencing consecutive snapshots; window identity derives from timestamps + the known
  window mechanics. Reading the actual meter beats modeling it (empirical inspection over
  assumption, Discipline #10 lineage).
- Every CLOSE row's `currency` + `ts` + token primitives make per-window attribution a join, and
  the U-3 question ("how much of July-class burn was cache thrash?") a query over rows once the
  env-var fix lands — the recorder is how U-3 proves itself.
- Reporting shape (per-window table vs rolling daily) is presentation, fork **F-5** — the
  substrate above supports both.

## 6 · The board — lanes, tiers, probes

### 6.1 Tier mapping (software-factory § 7 ladder)

| Tier | Fleet-board form | Gate |
|---|---|---|
| **1** | `flight/report.md` — generated markdown, regenerated on demand by a read-only script; iOS-readable through any session | ships as soon as the recorder accumulates rows (recorder-first, always) |
| **2** | Local web board (drax; Spec B lineage — lean F-1: ONE dashboard, the Spec B factory board extended to fleet scope, not a second dashboard) | **receipts schema stable across ≥2 workflows** — jack-ryan ratifies passage; VFX corpus = workflow #1; the codex-queue's first real workload = workflow #2 candidate |
| **3** | Matt inbox, iOS-push (HALTs/veto windows/rulings) | after Tier 2 earns trust (F-4; lean: gate it, with the named criterion in § 8) |

### 6.2 Lanes (top to bottom — the order IS the priority statement)

1. **AWAITING MATT** — always first; this lane is the product (Matt's attention is the fleet's
   scarcest resource). Sources: open HALT rows + veto windows from the record; open-row counts +
   top items from `canonical/matt_decision_needed/` (Q-rows) and `canonical/matt_to_do/` (T-rows).
   The board RENDERS the queues; it never becomes them (§ 4.8 queue-rows-are-views precedent —
   the queues' markdown stays the truth the board parses).
2. **IN-FLIGHT** — units with START and no terminal event, each with **staleness age rendered
   loud** (amber/red per F-2 SLA). The exhibit this lane exists for: six engine-seam dispatches
   fired 2026-07-22 went silently stale for a month in terminal scrollback.
3. **AT GATE** — open GATE rows: Gate-1 / Gate-2 / minted-gate items, gatekeeper named.
4. **HEALTH** — read-only probes run at render time: Codex auth (`~/.codex/auth.json` +
   `codex login status`) · GitHub OAuth state · `ENABLE_PROMPT_CACHING_1H` env presence (the U-3
   lever, visible) · throttle/window state from latest SNAPSHOTs · scheduled crons/wakeups ·
   disk-space watchers (PL-5 precedent) · **unpushed commits across the four repos** · unswept
   `requests/` dirs (L-31: owners sweep at phase boundaries; the board shows the un-swept) ·
   **pin-drift alarms** (`model_echo ≠ pin`; `harness_version` change mid-workstream).
5. **SEALED / DONE** — terminal units with cost + verdict rollups; the per-model scorecards
   (§ 3.6-1) render here.

### 6.3 Render rules

Rebuilt from disk on every refresh — no board-side state, no cache that can disagree, no
board-side verdict derivation beyond fold-of-events. Probes are READS. galadriel
screenshot-verifies every shipped Tier-2 surface against disk truth (the green-pixel-over-red-exit
ancestor bug is the class she exists to catch). Every surface carries a **SHOP-ONLY** tag
(dual-audience doctrine; nothing here is PROTO-PRODUCT).

## 7 · What this build is NOT

- Not an orchestrator, router, or queue — it never carries traffic (a watcher that carries
  traffic is a middleman, not a monitor).
- Not a work-product archive — telemetry only (§ 2 constitution).
- Not a quality self-report — verdicts enter rows only from named gatekeepers/curators (GATE and
  CURATION events), never from the executing lane's self-assessment (the house method: judge
  externally, never self-report).
- Not a replacement for ledgers, trackers, or queues — those remain the truth; the record is the
  row-shaped shadow that makes them costable and the board is the glass over both.

## 8 · Empirical criteria (adoption gates, per the workflow-upgrades law)

1. **Recorder (U-1's own criterion):** after one full wave under the recorder, Matt answers from
   rows, not prose: what did this wave cost (per currency), where did the time go, what got
   reworked and why.
2. **Board Tier-1:** the four § 0 questions answered from `report.md` alone against live fleet
   state, cross-checked against disk truth with zero desyncs.
3. **Board Tier-2:** same check on the rendered board + galadriel screenshot-verification;
   schema held stable across ≥2 workflows (jack-ryan ratifies).
4. **Scorecard (U-5 rider):** two comparable dispatches scored end-to-end from rows alone.
5. **Tier-3 unlock (F-4 lean):** criteria 2+3 held for two consecutive workflows without a
   desync incident.

## 9 · The fork table (ELICITOR grill — Matt rules; leans are recommendations, never rulings)

| # | Fork | Options | gandalf lean | Status |
|---|---|---|---|---|
| **F-1** | Board home | (a) extend the Spec B factory dashboard to fleet scope (ONE local board) · (b) separate fleet web app · (c) terminal TUI only · (d) markdown report only | **(a)**, with Tier-1 markdown shipping first regardless — two dashboards would fork the one-data-path story; a TUI can't serve iOS; markdown-only under-serves the staleness/red rendering | OPEN |
| **F-2** | Staleness SLA (when IN-FLIGHT turns red) | per-class thresholds vs one global | **per-class**: scripted job amber at 2× / red at 5× its class median duration; agent dispatch amber 48 h / red 7 d; HALT/veto rows amber immediately (they're waiting on Matt by definition, but rendering them stale pressures the wrong party — they live in lane 1 instead) | OPEN |
| **F-3** | Card grain | dispatch vs run vs wave | **card = the unit that receives a verdict** (dispatch/job), grouped under run headers with wave rollups. Schema is grain-agnostic via `parent_id` either way — this fork binds only the render | OPEN |
| **F-4** | Tier-3 iOS push timing | now vs after Tier-2 earns trust | **gate it** (ladder discipline); unlock criterion § 8.5. The tempting exception (push HALTs early because AWAITING-MATT is the product) is exactly how a view acquires authority — resist | OPEN |
| **F-5** | Window reporting shape | per-window burn table vs rolling daily | **both from the same substrate**: per-window table for anthropic-max (windows are the real constraint), rolling daily+weekly for chatgpt-sub (its meter is murkier); SNAPSHOT rows support both | OPEN |
| **F-6** | Truth substrate | JSONL truth-of-record vs factory SQLite as fleet truth | **JSONL is fleet truth-of-record** (append-only, committable, survives with zero runtime); factory SQLite stays workflow-internal; any fleet SQLite is a derived, rebuildable index. Star-lord holds the implementation latitude within this constraint | OPEN |
| **F-7** | Claude-lane token capture depth | hooks+snapshots only (nulls honest) vs invest in deeper per-session attribution now | **hooks + SNAPSHOT brackets in v1; no fabricated numbers**; revisit with U-3's attribution audit as the empirical input | OPEN |
| **F-8** | Record git policy | committed monthly JSONL vs git-ignored + promoted rollups | **committed** — durability and multi-session visibility beat commit churn at this volume (30 jobs ≈ 30 CLOSE rows ≈ a few KB) | OPEN |

## 10 · Seam routing + sequencing (the KR request carries this — pinned here for one-doc reading)

| Seam | Role |
|---|---|
| **star-lord** | Builds recorder: schema module + appender + codex-queue native emission + VFX-corpus normalization (founding rows, `derived_from`-pinned) + SNAPSHOT capture + Tier-1 report generator. Owns schema post-ratification |
| **drax** | Builds Tier-2 board AFTER the ≥2-workflow gate; Spec B composition per F-1 ruling |
| **jack-ryan** | Ratifies schema v1 + THE LAW as discipline; ratifies Tier-2 gate passage |
| **galadriel** | Screenshot-verifies every shipped Tier-2 surface |
| **knight-rider** | Sequences; composes with the Step-2 build wave (the codex queue task emits U-1 rows from day one) |
| **legolas** | U-2 retrospective backfill (optional, Matt-gated; `backfill:true` rows only) |
| **gandalf** | This spec; DRIFT-CRITIC on the builds; **no code** |

**Sequencing law:** recorder before board (discipline 3); Tier-1 report before Tier-2 board;
Tier-2 before Tier-3. Nothing renders what wasn't recorded.

---

**Signed:** gandalf (SPEC-AUTHOR + ELICITOR), 2026-08-24. The tape must be boring, complete, and
incapable of opinion; the board must be loud, derived, and incapable of authority.
