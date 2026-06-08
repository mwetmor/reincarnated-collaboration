# AMENDMENT — David-H UE MCP Bridge Spike: db-lyon Primary

**Date:** 2026-06-08
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-08 ratification of db-lyon-primary posture following three-way MCP deep comparison (NAJEMWEHBE vs StraySpark vs db-lyon)
**Amends:** `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` (sections superseded named below)
**To:** David-H (PC-side orchestrator; PC-resident) — Mantis invoked as Pattern A sub-agent for UE-side validation
**Critical anchors (new):**
- `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md` (ecosystem inventory)
- `agentic_orchestration/legolas/research/2026-06-08-three-way-mcp-comparison/synthesis.md` (three-way deep comparison; source of db-lyon-primary recommendation)
- https://github.com/db-lyon/ue-mcp (db-lyon repo)
- https://github.com/db-lyon/ue-mcp/blob/main/LICENSE (BUSL-1.1 LICENSE text — explicit $0 evaluation grant in base BUSL terms covers spike work)
- https://github.com/db-lyon/ue-mcp/blob/main/COMMERCIAL-LICENSE.md (commercial-license terms reference)

---

## 0. What this amendment changes

### 0.1 Headline shift

**Original spike scope (2026-06-07):** "Build a minimal-viable MCP server that wraps Unreal Engine's built-in Remote Control Plugin Web API."

**Amended spike scope (2026-06-08):** "Adopt **db-lyon/ue-mcp** as primary MCP bridge. Validate adoption viability + SSH-topology compatibility + WS1-relevant capability coverage. NAJEMWEHBE/unreal-ai-connection retained as named-fallback if db-lyon evaluation surfaces a project-killer during spike execution."

### 0.2 Why this changed

Two legolas Mode A research commissions surfaced in sequence:

1. **Ecosystem inventory (2026-06-08 commit `9579181`):** UE+MCP ecosystem expanded from 6 → 17 implementations beyond the prior commission's scope. Three implementations emerged as adoption candidates: NAJEMWEHBE (MIT, 148 tools, 607 tests), StraySpark (commercial via Fab, 359 tools, production-grade auth + transactions), db-lyon (BUSL-1.1, 21 categories with 569+ sub-actions, recent v1.0.79).

2. **Three-way deep comparison (2026-06-08 commit `554da75`):** source-code-verified depth equalization revealed db-lyon meaningfully more capable than NAJEMWEHBE across surfaces that matter — Niagara (28 sub-actions vs 3); DataTable (11 actions with full CRUD vs 2); Animation (54); Blueprint (59); Asset (60+). db-lyon's BUSL-1.1 LICENSE has an explicit $0 evaluation grant; commercial-license requirement triggers only at production commercial deployment.

**Decision drivers (Matt 2026-06-08):**
- Capability advantage (substantial)
- $0 dev-time cost (explicit license grant)
- Cleaner spike output (first-class MCP tools vs Python-exec workarounds)
- Migration plan accepted (Matt directive "explore with mindset of removal/replacement later if we can't get in touch")
- Change Date mitigation: BUSL-1.1 converts to Apache 2.0 four years after publication (v1.0.79 published 2026-06-06 → Change Date 2030-06-06; if Reincarnated ship lands 2030+, licensing risk auto-resolves)

### 0.3 Sections of the 2026-06-07 dispatch SUPERSEDED by this amendment

- **§ 0 TL;DR** — replaced with the amended scope above (§ 0.1)
- **§ 1.1 What David-H produces (orchestration)** — superseded by amended deliverables (this doc § 2)
- **§ 1.2 What Mantis produces (sub-agent invocations)** — superseded by amended validation tests (this doc § 3)
- **§ 1.3 What spike does NOT produce** — superseded by amended out-of-scope (this doc § 4)
- **§ 5 Spike verdict shape** (if section number — refer to original; spike verdict GREEN/YELLOW/RED logic preserved with updated success criteria; see this doc § 5)

### 0.4 Sections of the 2026-06-07 dispatch PRESERVED

- Spike type (empirical tooling-feasibility validation)
- David-H-led-with-mantis-sub-agent operational pattern
- Cost budget ($0 LLM; engineering session time only)
- Time budget (~4-8 hr wall-clock across 1-2 sessions)
- Critical anchors to mantis spike + jack-ryan Gate-2 findings + federated PC team architecture
- SSH-topology context

---

## 1. Amended spike scope

### 1.1 Primary path — Path A: db-lyon adoption

**Action:** install db-lyon/ue-mcp into `C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject` per repo install instructions. Run `npx ue-mcp init` interactive setup. Configure for SSH-tunneled mantis access from Mac-resident sessions if applicable.

**Validate:**

1. **Installation succeeds** — db-lyon repo install instructions complete cleanly on PC UE 5.7 project
2. **Mantis sub-agent can invoke db-lyon MCP tools** — David-H invokes mantis as Pattern A sub-agent; mantis successfully calls representative tool from each of 5+ db-lyon categories (Blueprints, Materials, Assets, VFX, DataTable)
3. **SSH-topology works** — mantis on PC, invoked via SSH from Mac-resident session, can drive db-lyon-bridged UE Editor (SSH port-forwarding of WebSocket transport if needed)
4. **WS1-relevant DataTable CRUD works** — exercise db-lyon's DataTable category (11 actions per legolas comparison): create table, define structure, write row, read row, update row, delete row. Validates cosmograph JSON ingestion path is unblocked at the tooling layer.
5. **WS2-relevant Niagara authoring works** — exercise db-lyon's Niagara category (28 sub-actions per legolas comparison): spawn at location, create emitter, configure module, set bound parameter. Validates Niagara iteration loop is unblocked.
6. **WS3-relevant Sequencer authoring works** — exercise db-lyon's Sequencer category (7 actions per legolas comparison): create sequence, add track, add section, set keyframes, set playback range. Validates materialization-cinematic authoring is unblocked.
7. **Latency characterization** — measure per-tool roundtrip latency under SSH-tunneled topology. Document.
8. **Reliability characterization** — exercise representative tool sequence 10-20 times under various editor states. Document failures + recovery patterns.
9. **License compliance during spike** — confirm spike work falls under db-lyon's base BUSL-1.1 non-production-use grant (internal evaluation, development, testing not intended for commercial deployment). Spike work IS evaluation by definition.

### 1.2 Fallback path — Path B: NAJEMWEHBE evaluation IF db-lyon surfaces project-killer

**Trigger:** Path A spike validation surfaces a fatal issue with db-lyon that cannot be resolved within spike scope. Examples of project-killers:

- Installation fails on PC UE 5.7 project after reasonable troubleshooting
- SSH-topology fundamentally incompatible
- Multiple core capabilities (DataTable / Niagara / Sequencer) broken or unreliable
- License compliance concern surfaces during evaluation

**Action if triggered:** abort Path A; switch to NAJEMWEHBE/unreal-ai-connection per same validation steps as Path A § 1.1. NAJEMWEHBE has DataTable gap (Python-exec workaround) and Niagara gap (emitter-creation not first-class) — accept these for spike viability if Path B is invoked.

### 1.3 NOT pursued in this spike

- **No build-from-scratch MCP server.** Original 2026-06-07 dispatch scope retired. db-lyon's existing capability obsoletes from-scratch build.
- **No StraySpark evaluation in spike.** StraySpark adoption gated on commercial-license pricing (Fab listing pricing-discovery is Matt-routed, not spike-blocking). Post-spike StraySpark assessment possible if pricing inquiry yields acceptable terms.
- **No commercial-license outreach during spike.** db-lyon `licensing@ue-mcp.com` outreach is Matt-routed; not spike-blocking; spike work covered by base BUSL non-production-use grant.

---

## 2. What David-H produces (amended)

Delivery packet at `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/`:

| Artifact | Format | Purpose |
|---|---|---|
| `spike-findings.md` | markdown | Spike verdict (GREEN/YELLOW/RED) + mantis sub-agent invocation log + per-validation-step result (§ 1.1 #1-9) + latency/reliability characterization + WS1-WS3 capability coverage assessment + path B trigger documentation if invoked |
| `db-lyon-install-record.md` | markdown | Installation steps executed + configuration choices + SSH-tunneling setup (if applicable) + reproducibility notes |
| `validation-test-log.md` | markdown | Per-tool exercise log: tool name, inputs, expected result, observed result, latency, pass/fail, notes |
| `session-boundary-memo.md` | markdown | David-H wind-down summary per OP § 5 |

If Path B triggered: add `path-b-najemwehbe-evaluation.md` with parallel structure to `db-lyon-install-record.md`.

---

## 3. What Mantis produces (sub-agent invocations) — amended

Per David-H sub-agent invocations:

- db-lyon plugin installed in `C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject` (one-time setup per § 1.1 #1)
- Validation tests per § 1.1 #2-9 executed
- Per-test: tool name + invocation parameters + expected behavior + observed behavior + latency measurement + pass/fail verdict + any notes for productionization

If Path A surfaces capability gaps that are NOT project-killers but ARE downstream-relevant (e.g., a missing DataTable sub-action; an unreliable Niagara tool): document for gandalf review at amendment authorship of WS1-WS5 commissions; do NOT abort Path A for gap-recovery work.

---

## 4. What spike does NOT produce (amended)

- **No production deployment of db-lyon.** Spike is evaluation only. Productionization decision deferred to post-spike Matt + gandalf review.
- **No commercial-license commitment.** Spike work is non-production use per base BUSL-1.1 grant. Commercial license discussion gated on Matt outreach + production decision; not spike-blocking.
- **No fork or modification of db-lyon source.** Spike uses unmodified upstream. Fork-and-extend (if needed) is separate workstream decision.
- **No SSH-tunneling productionization.** If SSH-tunneling needed for spike, prototype-grade is sufficient.
- **No WS4 (save-load) testing.** Confirmed exclusion: all surveyed implementations correctly identify WS4 as runtime concern, not editor concern.

---

## 5. Spike verdict shape (amended)

| Verdict | Trigger | Downstream action |
|---|---|---|
| **GREEN (Path A)** | db-lyon validation steps § 1.1 #1-9 pass at acceptable quality | Adopt db-lyon as primary MCP bridge for vertical-slice spike + WS1-WS5 workstreams. Matt + gandalf review productionization scope (commercial-license inquiry timing; fork-and-extend scope if needed). |
| **YELLOW (Path A, partial)** | db-lyon validation passes core capabilities but surfaces non-fatal issues (latency concerns; unreliable secondary tools; install friction; SSH-topology requires workarounds) | Adopt with documented caveats. Productionization scope incorporates caveat-resolution. NAJEMWEHBE evaluation may run post-spike for comparison. |
| **GREEN (Path B)** | Path A surfaced project-killer; switched to NAJEMWEHBE; NAJEMWEHBE passes adapted validation steps | Adopt NAJEMWEHBE as primary; plan NAJEMWEHBE-extension workstreams for DataTable + Niagara gap-fills. |
| **RED** | Both Path A and Path B (if invoked) fail | Re-engage gandalf for posture re-assessment; consider StraySpark commercial route OR Remote Control HTTP from-scratch revival (original 2026-06-07 dispatch scope). |

---

## 6. Composition with prior dispatches + canonical commitments

This amendment composes with:

- **`canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md`** — WS1-WS5 workstreams downstream of spike depend on MCP bridge capability; db-lyon's DataTable depth directly supports cosmograph JSON ingestion path
- **`canonical/story/2026-06-07-federated-pc-team-architecture-commit.md`** — David-H + mantis seam relationship preserved; spike execution pattern unchanged
- **`canonical/story/2026-06-07-cosmograph-cross-surface-LOD-architecture.md`** — WS2 Niagara iteration needs db-lyon's emitter-authoring depth for substrate-LOD VFX work
- **Prior 2026-06-07 dispatch** — preserved as historical record; sections SUPERSEDED named in § 0.3; sections PRESERVED named in § 0.4
- **legolas Mode A workflow** — two prior research commissions provided the evidence basis; third-party commercial-license inquiries are Matt-routed external actions

---

## 7. Anti-patterns

- **Don't pursue StraySpark evaluation during spike** — pricing-blocked; deferred to post-spike Matt-led inquiry
- **Don't attempt commercial-license inquiry during spike** — Matt-routed external action; spike work is non-production use per LICENSE
- **Don't switch to Path B prematurely** — Path A is primary; only switch on documented project-killer per § 1.2 trigger
- **Don't fork db-lyon during spike** — spike uses upstream unmodified
- **Don't expand spike scope to productionization** — productionization is separate post-spike decision

---

## 8. Sign-off

**Authored:** gandalf 2026-06-08 per Matt 2026-06-08 ratification of db-lyon-primary posture following deep three-way comparison evidence.

**Authority:** gandalf cross-cutting dispatch-amendment authority per canonical doc 38 + decisions-log temporal ground-truth + Team commit + push discipline per CLAUDE.md addendum (in-scope orchestration work + work-products auto-commit).

**Routing:** David-H consumes both the 2026-06-07 ORIGINAL dispatch (for preserved sections per § 0.4) + this 2026-06-08 AMENDMENT (for superseded sections per § 0.3). Spike fires when David-H session activates with both dispatch + amendment loaded.

**Empirical-evidence trigger for productionization decision:** spike verdict per § 5 — gandalf + Matt review GREEN/YELLOW/RED outcome; commercial-license inquiry timing decided post-verdict; WS1-WS5 commissions inherit spike's tooling-layer evidence.

**Composition with prior commissions:** AMENDS not REPLACES the 2026-06-07 dispatch. NAJEMWEHBE evaluation context preserved as Path B fallback; StraySpark deferred to pricing-dependent post-spike consideration.

**End of amendment.**
