# Software Factory — strategy of record

> **STATUS: STRATEGY-CURRENT** — authored 2026-08-10 by gandalf (SPEC-AUTHOR/CANON-STEWARD) from the
> 2026-08-10 Matt strategy session. Rulings D1–D5 are Matt's (§ 2). **jack-ryan ratification queued**
> per `canonical-doc-format.md § 6.7` (gandalf proposes + executes; jack-ryan ratifies process canon).
> **Companion:** `operating-procedures/desirable-run-pattern.md` — the CHARTER layer; this doc adds the
> SPINE and LABOR layers beneath it and changes nothing above it.

---

## 1 · The recognition

We already run a software factory — in prose. Charters, pre-registered gates, ruling ledgers,
batons, seam envelopes (MIGRATION notes), receipts-by-hand (run ledgers, commit maps): every
mechanism a factory needs exists in this project as *discipline executed by a conductor reading
documents*. The strategy is therefore **not adoption but compilation**: compile the factory we
already run into thin code, so that the mechanical fraction of a run executes at script cost
instead of conductor-attention cost.

The in-house evidence that mechanization pays:

- **R-BR-57 (the split cell):** agent edits, conductor renders — **13 tool calls vs 129–278**
  for the same deliverable class. A 10–20× reduction, measured, from moving the mechanical leg
  out of the agent loop.
- **BR-2's two gates that passed while failing** (G-14 presence clauses via the noise floor;
  G-5d via a soot prefab the burn-shader gate never saw) — both caught by Matt's eye, neither
  by a gate. The factory automates the *mechanical* verdicts and must never claim the
  owner-eye ones.
- **WR3/KC2 run record:** the per-landing law (reproduce the number from the artifact, not the
  report) caught defects at every endgame hop. That law is a *claim gate* — it compiles.

**What compiles: the run's mechanical fraction.** What never compiles: elicitation, design
dialogue, rulings, the owner's eye. The factory is the stagehand, not the playwright.

## 2 · Rulings of record (Matt, 2026-08-10 — "I agree with the plan generally")

| # | Ruling |
|---|---|
| **D1** | **Compile in-house.** Build our own thin spine; route labor through the two subscription-native harnesses (Claude Code headless + Codex CLI). **No pi-for-Claude** — see § 4. |
| **D2** | **Codex lane authorized.** ChatGPT-subscription Codex agents enter as workers; first use case = strictly-codified implementation (F2 pilot, § 9). Matt action T16 (`canonical/matt_to_do/`). |
| **D3** | **Privacy tier consciously accepted.** Work-product flows through two vendors' subscription channels; sovereignty-ladder tension noted and accepted at this project stage. |
| **D4** | **star-lord builds the spine** against gandalf's spec (`gandalf/notes/2026-08-10-factory-spine-spec.md`); gandalf writes no production code. |
| **D5** | **Sandboxes deferred.** Container/sandbox isolation is credential-incompatible with subscription auth today; permissions fingerprinting (§ 5) is the v1 containment. |

All five veto-open per standing practice; recorded here so the veto has a surface.

## 3 · Three layers

| Layer | What it is | Home | Status |
|---|---|---|---|
| **CHARTER** | What runs deserve to exist, who conducts, where authority halts. The desirable-run pattern, unchanged. | `operating-procedures/desirable-run-pattern.md` | Governing, untouched |
| **SPINE** | Thin in-house run harness: phase runner, envelopes, claim gates, receipts, permissions fingerprint, session dirs. Python + YAML + SQLite. | `agentic_orchestration/factory/` | To build (F1, star-lord) |
| **LABOR** | The harnesses that execute phases: **Claude Code headless** (`claude --agent <seam> -p`, named seam agents = the discipline stack loads with the name) and **Codex CLI** (F2). | subscription-native CLIs | Lane 1 live today; Lane 2 = T16 |

The spine ORCHESTRATES; the labor harnesses EXECUTE; the charter GOVERNS. A run that fails the
charter's fit test does not get a spine config — the factory cannot launder an undeserving run
into existence.

## 4 · Subscription economics — the decisive constraint

From the legolas probe (2026-08-10), quoting pi's `providers.md` verbatim: Claude Pro/Max usage
via third-party harness **"draws from extra usage and is billed per token, not against Claude
plan limits."** OpenAI Codex via ChatGPT Plus/Pro subscription carries no such caveat.

Consequences, ruled into D1:

1. **No third-party harness on the Claude lane.** pi (and SSSF's architecture, which presumes
   it) would silently convert our flat subscription into metered API spend.
2. **The two covered lanes** are Claude Code itself (headless `-p`, named `--agents`, the same
   subscription this team already runs on) and Codex CLI under a ChatGPT subscription.
3. **SSSF's Claude adapter is a stub** (`agent_cc.py`, ~15 lines, `NotImplementedError`) — the
   lane we'd most need from them does not exist in their code. Compile-in-house is not
   preference; it is the only path that keeps both lanes subscription-covered.

## 5 · Imports — mechanisms we take (with adaptation)

| Mechanism | Source | Our adaptation |
|---|---|---|
| **Default-fail phase primitive** | SSSF | Context-manager: a phase is FAILED unless exactly one `finish()` collapses it. Matches our default-deny gate posture (KC2 emit wall: no override path). |
| **Typed envelopes** | SSSF | `EnvelopeBase(status, summary, artifacts, notes_for_next_agent)` + **synced triad** (dataclass / JSON schema / prompt block in one module, test-asserted identical). Our MIGRATION-note discipline, typed. |
| **Post-hoc claim gates** | SSSF | `gate(envelope, run) -> GateReport` run against ARTIFACTS, never the envelope's word. v1 set: `artifacts_exist`, `files_non_empty`, `json_parses`, `diff_matches_claims`, `verdict_consistent`, `tests_pass(command)`. This is the per-landing law, compiled. |
| **Only-failures-travel** | SSSF | Never pass a passing test suite back into context; no "tester agent" — a command runs and its failures (only) enter the next prompt. |
| **Permissions change-set fingerprinting** | SSSF | Before/after tree diff per phase; writes outside the phase's allowlist → rollback + **abort, not retry** (a breach is evidence, not noise). |
| **Per-agent tool narrowing** | SSSF + external evidence (2/10 → 10/10 task success on narrowing, legolas annex § 11) | Already our practice via seam agents; the spine makes it config-enforced per phase. |
| **SQLite WAL receipts** | SSSF | Tables: sessions / phases / events / envelopes / gate_results / processes / agent_sessions. Plus `UsageBreakdown` (input / output / cache_read / cache_write / reasoning tokens + dollars; **reasoning is a share of output, never a fifth addend**). Our run ledger's mechanical shadow. |
| **Session dirs** | SSSF | `factory/sessions/{run_id}/` — context_handoff/, per-agent prompts/, raw_output.jsonl, envelope.json. Git-ignored working state; committed artifacts are configs, code, and deliberately promoted reports. |
| **Sub-agents recon-only** | SSSF, convergent with our § 4.10 routing | Fan-out for read-only reconnaissance; substantial pieces route to NAMED seam agents. |

## 6 · Refusals — their gaps, our standing counter-disciplines

| Their gap | Evidence | Our counter-discipline (already law) |
|---|---|---|
| **Spec drift** — agents wander off the spec mid-chain | MAST taxonomy: 41.8% of multi-agent failures are specification/drift class (legolas annex) | Pre-registration (#1 clause 1.3 candidate), DRIFT-CRITIC review, jack-ryan Gate-2 |
| **Observability theater** — gates that echo-exit-0; green UI over red exit code (bug found in their own repo) | legolas annex | **No stub gates, ever.** A gate that cannot run returns FAIL/NOT-RUNNABLE. Absences are NAMED-ABSENT-DECLARED (KC2 practice). |
| **Eye-replacement** — dashboard verdicts standing in for the owner's judgment | BR-2: two gates passed while failing; both caught by Matt's eye | Owner-eye is load-bearing and never automated (desirable-run-pattern § 6 obs. 2; Q52: Matt IS the player). |
| **No memory layer** — every run relearns | their pitch names it unsolved | Receipts → law harvest → config recompile (§ 9 F4): the loop we already run as wind-down → discipline → next charter, mechanized. |
| **Gate-gaming** — agents learn to satisfy the gate, not the intent | KC2 counter-practice | Falsification tests ON the gates (strip-it-and-the-reds-come-back); audits of greens, not just reds. |

## 7 · UI tier ladder

| Tier | Surface | Gate to build |
|---|---|---|
| **0** | `factory status` in the terminal + per-run generated report | Ships WITH F1 (star-lord) |
| **1** | Generated run reports (markdown, from receipts) | F1 |
| **2** | Glance dashboard answering exactly four questions: *what's running? what's red? what did it cost? what's waiting on Matt?* Plus the **New Run form** — which IS the proto-minigame-editor (see companion doc). | **Receipts schema stable across ≥2 compiled workflows.** drax builds per `gandalf/notes/2026-08-10-factory-ui-proto-editor-spec.md`. |
| **3** | Matt inbox — rulings + watches + veto windows, iOS-push surfaced | After Tier 2 earns trust |

**Three UI disciplines (non-negotiable):** (1) **one data path** — the UI reads the same SQLite
the gates write; a view is never truth; (2) **read-mostly** — interface verbs write only through
queue/ledger machinery; (3) **no dashboard before receipts** — Tier 2 cannot precede two real
workflows' worth of receipts, or it becomes observability theater with our name on it.

**Dual-audience tags:** every UI surface is stamped **SHOP-ONLY** (operator tooling) or
**PROTO-PRODUCT** (candidate player-facing lineage). Governed by
`canonical/reap-die-rise-game/minigame-editor-and-scenario-contracts.md`.

## 8 · Schema custody

Scenario / baton / receipt schemas that the ENGINE emits stay engine-side under star-lord
custody (drax countersign where consumed) — the factory **consumes** them and never forks them.
The factory's own receipts schema is star-lord's per Spec A. One schema, one custodian, many
readers: the KC2 baton discipline, generalized.

## 9 · Phases

| Phase | Content | Owner |
|---|---|---|
| **F0** | **Law harvest** — codify the BR/WR/KC2 minted rules (R-BR-51…57, per-landing law, split-cell economics) into *godot implementation law* + factory gate definitions. Separate artifact, gandalf-owed, next after this unit. | gandalf |
| **F1** | **Spine + one ported workflow.** Build `factory/` per Spec A; port the baton-scene MECHANICAL cells (digest gate, ffprobe gate, headless test wall) to run under it. **Founding-run lean (veto-open): the KC2 baton scene build proceeds AS the factory's founding run** — charter per desirable-run-pattern § 3 fit test (bounded substrate: the baton @ `d7ecd866…`; decidable target-state; pre-drainable forks; authority-resident), Rider-1 boundary respected verbatim. | star-lord (spine) · run charter separately |
| **F2** | **Codex pilot** — L1 baton consumer built by a Codex worker from the handoff note's ten semantics, judged **differentially against `export/baton_v1_stub_consumer.py`** (the executable reading). Strictly-codified implementation = the right first Codex use case *because the referee already exists*. Blocked on T16. | star-lord lane · gandalf judges |
| **F3** | **Parallel lanes** — multiple phases in flight under one receipts DB; split-cell pattern as the default shape. | KR sequences |
| **F4** | **Memory loop formalized** — wind-down harvest emits law-diffs; configs recompile from law. | gandalf + jack-ryan |

**Deferred (named, not taken):** sandboxes (D5) · router-agent / Kanban autonomy · any cloud
deployment. **Fit boundary:** workflows that compile well are mechanical-verdict shaped (render
cells, test walls, crawls, batch sims, differential builds). Workflows that must NOT be
compiled: elicitation, design dialogue, ruling-making, owner-eye judgment.

## 10 · Seam routing

| Seam | Factory role |
|---|---|
| **star-lord** | Spine build (D4); receipts schema custody; Codex-lane adapter |
| **drax** | Tier-2 UI + proto-editor form (Spec B); Godot-side consumers unchanged |
| **gandalf** | Specs, F0 law harvest, founding-run conduct (if fit test holds), DRIFT-CRITIC on builds |
| **knight-rider** | Dispatch sequencing (spine wave first); cross-seam routing |
| **jack-ryan** | This doc's ratification; Gate-2 on spine + every compiled workflow's first landing |
| **galadriel** | Screenshot-verify on every shipped UI surface |
| **legolas** | Evidence annex author (probe of record, § 11); future harness-surface probes |

## 11 · Evidence annex (legolas probe, 2026-08-10, folded here — sub-agent policy barred a standalone report)

- **SSSF pitch-vs-code:** the repo's Claude Code adapter is a `NotImplementedError` stub; the
  pitch's model roster (Kimi plans / Gemini builds / Opus reviews) contradicts the shipped
  config; no benchmark or evaluation evidence ships with the claims ("thousandth run" is
  aspiration, not measurement).
- **Billing trap:** pi `providers.md` (verbatim): Claude subscription use via third-party
  harness "draws from extra usage and is billed per token, not against Claude plan limits."
  Codex-via-ChatGPT carries no equivalent caveat in OpenAI's harness docs as probed.
- **External support for tool narrowing:** task-success movement from 2/10 → 10/10 on
  narrowing an agent's tool surface to the task's needs.
- **MAST:** 41.8% of catalogued multi-agent failures are specification/coordination-drift
  class — the gap our pre-registration + Gate-2 stack already targets.
- **Sound mechanisms worth importing regardless of pitch quality:** § 5 table.

## 12 · Ledger tail

- **Decisions-log entry recommended** (KR drafts, jack-ryan reviews): *Software-factory
  strategy adopted (D1–D5): compile-in-house spine, two subscription-native labor lanes,
  UI tier ladder, minigame-editor contract linkage.*
- **jack-ryan ratification** of this doc queued per § 6.7; desirable-run-pattern amendment
  candidates from WR3/BR2 wind-downs ride the same ratification sitting.
- **Matt queue:** T16 (Codex subscription + CLI + login) in `canonical/matt_to_do/`.
- **Companion canon:** `canonical/reap-die-rise-game/minigame-editor-and-scenario-contracts.md`.

**Signed:** gandalf, 2026-08-10.
