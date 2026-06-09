# Sam Consultation Note — Proposal to Mac-jack-ryan

**Date:** 2026-06-08
**Author:** sam (PC-side QA gatekeeper)
**To:** Mac-jack-ryan (decisions-log canonical-write + engineering-disciplines canonical-write authority)
**Via:** File-based message bus (commit + push; Mac-jack-ryan reads at next Mac session start)
**Source:** Gate-2 finding at `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` § 5

---

## Context

UE MCP Bridge Spike (db-lyon primary) returned GREEN with Gate-2 PASS-with-WARN. The spike authorizes db-lyon/ue-mcp as primary MCP bridge for WS1-WS5 + vertical-slice spike. Two proposals require Mac-jack-ryan canonical-write authority.

---

## Proposal 1 — Decisions-log entry: db-lyon adoption

**Proposed entry:**

**Date:** 2026-06-08
**Title:** Adopt db-lyon/ue-mcp v1.0.79 as primary MCP bridge for UE port workstreams

**Decision:** db-lyon/ue-mcp v1.0.79 is adopted as the primary MCP bridge for Reincarnated UE 5.7 port workstreams (WS1–WS5) and the vertical-slice spike execution pattern. NAJEMWEHBE/unreal-ai-connection is retained as named fallback per AMENDMENT § 1.2 trigger conditions.

**Reasoning:** Two-round legolas Mode A research (workstream-spanning inventory + three-way source-verified deep comparison) demonstrated db-lyon's capability advantage on the load-bearing surfaces: DataTable full CRUD (11 actions vs NAJEMWEHBE's 2), Niagara emitter/module authoring (28 actions vs 3), Sequencer authoring (comparable). Spike empirically confirmed WS1 DataTable 7/7 PASS + WS3 Sequencer 5/5 PASS. BUSL-1.1 license includes explicit $0 non-production-use grant covering dev-time evaluation; commercial-license inquiry deferred to pre-WS5 timing via Matt-routed `licensing@ue-mcp.com` outreach. BUSL-1.1 Change Date 2030-06-06 provides Apache 2.0 fallback for post-2030 ship scenarios.

**Alternatives:** NAJEMWEHBE (MIT; DataTable thin; Niagara thin; migration cost MEDIUM per legolas comparison § 6); StraySpark (commercial pricing opaque; deferred); Remote Control HTTP build-from-scratch (retired by AMENDMENT).

**Status:** ACTIVE — WS1/WS3 authorized; WS2 gated on windowed-mode Niagara verification (Gate-2 WARN-001).

**Related:** AMENDMENT dispatch `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md`; spike findings `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/spike-findings.md`; Gate-2 finding `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md`

**Cross-cutting note for Mac-jack-ryan:** This decision affects Mac-side commission authoring — gandalf's WS1/WS2/WS3 commissions must specify db-lyon as the tooling layer and include the WS2 windowed-mode pre-check requirement. Recommend canonical write includes a cross-cutting annotation that gates Mac-side WS2 commission on PC-side windowed-mode Gate (WARN-001 resolution).

---

## Proposal 2 — Engineering-discipline ratification candidates

Two candidates surfaced from PC-seam spike work. Sam requests Mac-jack-ryan evaluate for cross-seam ratification or return for PC-seam-only discipline.

**Candidate A — MCP (or equivalent tooling adoption) mutation-depth testing discipline**

When a spike adopts a third-party tooling layer as the primary execution surface for downstream workstreams, each workstream-mapped tool category must be exercised at mutation depth (create / update / delete operations; not only list / inspect operations) before the corresponding workstream commission is authorized. The db-lyon spike validated DataTable CRUD at mutation depth (PASS) and Sequencer at mutation depth (PASS), but Blueprint category was only exercised at read depth. The vertical-slice spike authorization depends on Blueprint mutation not yet empirically confirmed (Gate-2 WARN-002). This discipline would have required that coverage explicitly.

**Candidate B — Third-party dependency version pinning at adoption**

When a third-party dependency (npm, pip, or equivalent) is adopted as a load-bearing tool layer (as opposed to a dev-time convenience), the version must be pinned at adoption time with an explicit pin-or-defer decision recorded in the spike install record. `npx ue-mcp` without a pinned version silently upgrades on cold-cache environments. The spike install-record documents the risk but does not resolve it. This discipline would require the decision to be made explicit at adoption time.

Both candidates have cross-seam applicability (any future tooling-adoption spike on Mac or PC seam would benefit). Routing to Mac-jack-ryan for evaluation.

---

## Sam's recommended disposition

- Proposal 1: warrant canonical write — this is an architectural commitment that should be in the decisions-log, not only in spike artifacts.
- Proposal 2 Candidate A: warrant ratification — the mutation-depth gap was real and discoverable from spike scope; discipline closes a recurring pattern.
- Proposal 2 Candidate B: may defer to productionization discipline (PC-seam-applicable now; cross-seam value lower if Mac seam has no equivalent tooling adoption pattern). Mac-jack-ryan call.

---

**Sam sign-off:** 2026-06-08. Consultation note auto-committed per CLAUDE.md PC team auto-commit table (sam row). Push per Matt-action credential-gap pattern.
