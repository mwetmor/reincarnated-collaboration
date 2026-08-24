# RUN U1-BUILD — charter + ruling ledger (gandalf, RUN-CONDUCTOR)

**Chartered:** 2026-08-24 · **Go-word (Matt, verbatim):** *"Now that we have clearly architected the desirable state via the sketch and staged data for glance, I would like you run with this one autonomously until completion."*
**Pattern:** `operating-procedures/desirable-run-pattern.md` — §3 fit test: bounded substrate ✓ (spec of record + VFX founding corpus + `agentic_orchestration/flight/` target) · decidable target-state ✓ (seal predicate below) · forks pre-drained ✓ (Q61 "all as leaned" + sketch nod + Glance card staged + push-pattern, all 2026-08-24) · authority resident ✓ (spec author conducts).
**Spec of record:** `gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md` (BUILD AUTHORIZED) · **Charter:** `workflow-upgrades.md` U-1 · **Seam routing:** `gandalf/requests/2026-08-24-knight-rider-u1-fleetboard-build.md` (gate CLEARED).
**Matt interface:** async; push-as-you-go (session pattern, Matt-set); HALTs filed to `matt_decision_needed/` + surfaced in-channel; seal report at close.

## Seal predicate (target-state — ALL of, or honorable fallback)

- **S1** Recorder core live: `flight/bin/flight_record` append-only writer + schema v1 per spec § 3 (F-6/F-8: committed monthly JSONL).
- **S2** Founding rows: 30 VFX jobs normalized onto the tape (`backfill:true`, `derived_from` pins to raw vendor streams; verdicts from `_run-log.tsv` rc only; honest nulls elsewhere).
- **S3** Tier-1 `flight/report.md` renders deterministically from tape + read-only probes (lanes per spec § 6.2/§ 11.3). No LLM anywhere in the path.
- **S4** jack-ryan ratifies schema v1 + THE LAW as discipline → schema custody transfers to star-lord (software-factory § 8).
- **S5** Workflow-#2 rows on tape: THIS RUN's own lifecycle (lane `claude-agent`, workstream `U1-BUILD`, honest-null tokens) → jack-ryan rules the ≥2-workflow stability gate (his, not waivable).
- **S6** drax renders behind S5: local fleet board (extend Spec B per F-1) + Glance historical fleet card (spec § 12.4, rear-view scope only).
- **S7** galadriel screenshot-verifies each Tier-2 surface against disk truth.
- **S8** Seal report: the four owner-questions answered FROM ROWS on real data (U-1 empirical criterion, demonstrated on founding corpus + run's own rows).

## Pre-registered gates

| Gate | Owner | Rule |
|---|---|---|
| **G-1** schema+LAW ratification | jack-ryan | BLOCK honored; discharge loop; undischargeable after two folds → HALT to Matt |
| **G-2** ≥2-workflow schema stability | jack-ryan | opens BOTH drax renders; not waivable by conductor |
| **G-3** visual verification | galadriel | every shipped Tier-2 surface vs disk truth |
| **G-4** LAW audit at every fold | gandalf (DRIFT-CRITIC) | zero write verbs on views · zero authority · no LLM in truth path · honest nulls · one data path |

## Honorable fallback (pre-declared)

- G-2 unpassable in-run (schema churn) → seal at S1–S4 + Tier-1 report; drax renders return to KR sequencing. A fallback seal is a seal, not a failure.
- Native codex-queue emission: **OUT OF THIS RUN** — uncommitted foreign Step-2 star-lord work is live in `factory/harness/` (540-line codex adapter, working tree). This run builds NOTHING there; integration point documented for the Step-2 wave. (L-1 below.)

## HALT-to-Matt list (commitment boundaries)

Charter/scope amendment · host-level actions (env vars — U-3 stays in `matt_to_do/`) · any pressure to give a view authority (refuse AND halt) · committed-truth conflict · undischargeable jack-ryan BLOCK.

## Standing constraints

gandalf writes no production code — seams execute via NAMED sub-agents only (OP § 4.10) · serial law untouched · `factory/harness/*` untouchable this run · specific-file staging only, never `add -A` · conductor pushes at fold after G-4 audit.

---

## Ruling ledger (veto-open; L-numbered; Matt may override any ruling)

- **L-1 (launch):** uncommitted `factory/harness/codex.py` + `__init__.py` (Step-2 codex adapter, live, another session's work) ruled FOREIGN-IN-FLIGHT — untouchable; recorder builds standalone at `flight/bin/`; queue emission deferred to Step-2 wave with documented integration point. Reasoning-boundary: composition/sequencing, within conductor authority.
- **L-2 (launch):** workflow-#2 candidate = this run's own lifecycle rows (claude-agent lane) rather than waiting on the Step-2 queue's first workload — the cheapest honest second workflow, and it exercises the schema on the OTHER economy (anthropic-max, honest-null tokens). jack-ryan still rules whether it satisfies G-2.
- **L-3 (launch):** B-1 (star-lord recorder build) + B-2 (jack-ryan schema+LAW ratification) launch in PARALLEL — ratification is doc-level against spec § 3 + founding corpus; code-level findings fold into his G-2 ruling.
