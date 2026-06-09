# Sam Gate-2 Finding — UE MCP Bridge Spike (db-lyon primary)

**Date:** 2026-06-08
**Author:** sam (PC-side QA gatekeeper, Pattern A sub-agent)
**Authority:** Matt 2026-06-08 spike-fire authorization; David-H Phase 4 routing per AMENDMENT execution sequencing
**Mode:** DEV-MODE Gate-2 review
**Verdict:** PASS-with-WARN

**Spike packet reviewed:**
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/db-lyon-install-record.md`
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/validation-test-log.md`
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/spike-findings.md`
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/session-boundary-memo.md`

**Evidence read:**
- `agentic_orchestration/legolas/research/2026-06-08-three-way-mcp-comparison/synthesis.md`
- `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md`
- `canonical/00-ground-state.md` (session anchor)
- `agentic_orchestration/GOVERNANCE.md` (ADR authority reference)

---

## 0. TL;DR

The spike packet is well-executed and the GREEN verdict is ratified with qualification. Math preceded tooling-pull (Discipline #1 satisfied — legolas two-round research preceded installation). The core validation surfaces (WS1 DataTable, WS3 Sequencer) are empirically cleared. One WARN surfaces: the spike characterizes the `add_emitter_to_system` headless crash as "non-project-killer" without empirical confirmation in windowed mode — that assertion is unverified and the conditional framing for WS2 is appropriately flagged but needs a harder gate before WS2 commission fires. Two INFO items address authority-boundary clarity and a decisions-log entry proposal. No BLOCK conditions found. Downstream commissions for WS1 and WS3 are authorized; WS2 commission remains gated pending windowed-mode verification. The spike's authority claims are compliant.

---

## 1. Per-principle review

### 1.1 Math-before-code (Discipline #1)

Satisfied. The spike did NOT begin with tooling-pull. The sequence was: (1) legolas Mode A workstream-spanning inventory (`9579181`), (2) legolas Mode A three-way deep comparison (`554da75`), (3) gandalf AMENDMENT dispatch authoring based on that evidence, (4) Matt ratification, (5) THEN mantis installation. This is textbook math-before-code sequence. Both legolas commissions are source-verified — the three-way comparison performed direct GitHub source-code inspection at action-name granularity, resolving the "5 of 9 unverified" flag from the prior synthesis. The evidence base is sound.

One minor observation: the three-way comparison synthesis TL;DR originally recommended ADOPT-AND-EXTEND (NAJEMWEHBE) before db-lyon received its empirical spike. Matt overrode this to db-lyon-primary on the capability-advantage + license-grant evidence. The spike correctly validated the capability claims. The legolas recommendation being overridden by Matt is not a principle violation — it is the correct decision-authority routing per ADR-002.

### 1.2 Smoke-gate coverage

Adequate for spike scope, with one conditional gap. Coverage:
- **WS1 DataTable CRUD:** 7/7 actions PASS empirically (validation-log § 3.3). Including `fill_datatable_from_json` which is the WS1 cosmograph JSON ingestion primitive. This is the load-bearing WS1 gate. CLEARED.
- **WS3 Sequencer authoring:** 5/5 actions PASS empirically (validation-log § 3.5). Per-channel keyframe authoring confirmed. WS3 gate CLEARED.
- **WS2 Niagara create/list/spawn:** PASS empirically. `add_emitter_to_system` CRASHES in headless mode (NiagaraHandlers.cpp:595). The spike claims this is "headless-specific" and "does not occur in windowed mode" (validation-log § 3.4) — but this is an inference, not an empirical result. The crash site is a C++ null-deref or factory-write violation in headless; that same handler executes differently in windowed mode but it has NOT been tested. Spike verdict correctly labels this YELLOW; the claim that it "does not occur in windowed mode" is asserted with confidence in excess of the evidence available.

**Critical surface NOT tested:** WS5 (mobile polish/LOD) is labeled TBD. The spike notes this as out-of-scope for current commissions, which is acceptable given WS5 is post-spike. No project-killer gap at this stage.

**Critical surface NOT tested:** Blueprint mutation operations. Only `list_node_types` was exercised (5ms, read-only). For vertical-slice spike gameplay code authoring (Blueprint / gameplay code), the "General iteration + gameplay code authoring" downstream action in spike-findings.md § 2 relies on Blueprint + Editor categories supporting "hot-reload + asset inspection workflows." These were not exercised at mutation depth. This is a forward INFO — not a WS1/WS3 blocker, but the vertical-slice spike should include Blueprint mutation smoke tests before deep authoring work begins.

### 1.3 Cross-seam impact

Adequately documented with two observations.

**What is documented well:** spike-findings.md § 3 identifies three cross-cutting implications (UE project structural amendment, MCP server registration path, protocol clarification). Session-boundary-memo § 2.2 correctly identifies the Mac-side seam consumers (Mac-KR + gandalf) and what they need (WS1/WS3 commission scoping; WS2 gate dependency).

**Observation on cross-host propagation:** The spike-findings.md is correctly designated as the cross-host coordination artifact for Mac-KR + gandalf consumption. This is adequate for the file-based message bus pattern per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 4.2. No gap here.

**Observation on ownership boundary for UE project structural amendment (see § 4 below):** The spike asserts this is PC-seam-internal authority. This is the correct call per § 7 of the federated architecture commit ("UE-project structure is PC-seam canonical-write"). No cross-cutting consultation needed. Sam ratifies this authority claim.

### 1.4 Decisions-log as truth

Authority claims are compliant throughout the spike packet. David-H and mantis do not claim decisions-log canonical-write authority. Spike-findings.md is correctly designated as a verdict document, not a decisions-log entry. The spike does NOT write a decisions-log entry itself — it correctly defers this.

However: the spike's GREEN verdict authorizes db-lyon adoption as the primary MCP bridge for all downstream workstreams. This is a load-bearing architectural commitment. The decisions-log does not yet have an entry capturing this adoption. A decisions-log entry proposal is warranted and is routed to Mac-jack-ryan per § 5 below.

The license posture section (spike-findings.md § 5) defers commercial-license inquiry to "Matt-routed at productionization decision" — this is the correct disposition per AMENDMENT § 0.3 anti-patterns. No overreach.

The AMENDMENT characterizes WS1-WS5 port workstreams as "likely still $0" for license. This is a reasonable inference from BUSL-1.1 non-production framing but is not confirmed by the license text. The spike correctly flags it as "deferred to Matt-routed inquiry." No overreach; the uncertainty is acknowledged.

### 1.5 Severity calibration

The YELLOW characterization of `add_emitter_to_system` is appropriate in spirit but slightly under-constrained in framing. Two angles:

**Correct:** It is correctly YELLOW not RED. The crash is headless-specific by crash-site analysis (the handler accesses subsystems that require full editor context). The spike correctly identifies that WS2 will use windowed Editor. The conditional gating (windowed-mode verification before WS2 commission authorization) is the right mitigation.

**Under-constrained:** The spike states the crash "does NOT occur in windowed mode" as a factual assertion (validation-log § 3.4: "The crash does NOT occur in windowed mode (the handler function itself is the crash site, not a platform limitation)"). This is a diagnostic inference, not an empirical result. The handler function crashing in headless does not prove it succeeds in windowed — the null-deref could have multiple call paths. The correct framing is "expected to pass in windowed mode based on crash-site analysis; requires empirical verification before WS2 authorization." The spike's WS2 gate (§ 4.2 "windowed-mode verification queued") correctly operationalizes this, but the confidence level in the characterization language is higher than the evidence warrants.

This raises severity to WARN (not BLOCK) because the WS2 gate itself is correctly placed — the issue is characterization precision, not missing risk coverage.

The headless crash is also a potential signal about broader headless-operation stability. The spike ran all other tests in headless mode successfully, so this does not indicate systemic instability. The specific handler crash is isolated. WARN characterization is correct at this scope.

---

## 2. Findings (INFO / WARN / BLOCK by severity)

### WARN-001 — Niagara windowed-mode claim overstated; WS2 gate requires empirical lock

**Severity:** WARN

**Summary:** Validation-log § 3.4 asserts that the `add_emitter_to_system` crash "does NOT occur in windowed mode" as a factual statement, based on crash-site analysis inference. The empirical result is that windowed-mode has NOT been tested. Spike-findings.md § 4.2 correctly queues windowed-mode verification; the issue is that the claim language in § 3.4 overstates certainty. The WS2 gate is operationally correct but the framing gives downstream consumers (gandalf commission authoring) false confidence that the YELLOW is "nearly resolved" when it is actually "unverified."

**Evidence:** validation-log § 3.4: "The crash does NOT occur in windowed mode (the handler function itself is the crash site, not a platform limitation)" — this is inference, not observation.

**Recommended action:** Mantis windowed-mode sub-session verifies `add_emitter_to_system` before WS2 commission fires. David-H ensures WS2 commission preamble (when gandalf authors it) includes explicit language: "windowed-mode verification of `add_emitter_to_system` is PREREQUISITE before commission execution — not a step within the commission." The distinction matters: if the verification gate is buried inside WS2 commission scope, gandalf may scope WS2 assuming the tool works.

**Cite:** Discipline #11 (empirical-first inspection); Review Principle #3 (scope validation before execution).

---

### WARN-002 — Blueprint mutation surface untested; vertical-slice spike should include BP authoring smoke test

**Severity:** WARN

**Summary:** Spike-findings.md § 2 authorizes db-lyon for "General iteration + gameplay code authoring — Blueprint / Asset / Editor categories support hot-reload + asset inspection workflows." The spike exercised Blueprint category at read-only depth (`list_node_types`: 5ms, 292 types). Blueprint creation, node addition, compilation, and variable authoring were not exercised. The vertical-slice spike is expected to involve gameplay code authoring via Blueprint. This creates an untested gap between spike authorization and vertical-slice execution.

**Evidence:** validation-log § 3.1: C2.2 Blueprint category test was `list_node_types` only. No Blueprint mutation tests in the validation criteria (AMENDMENT § 1.1 did not require them — this is a gap in the AMENDMENT scope, not a mantis execution failure).

**Recommended action:** Include a one-session mantis Blueprint mutation smoke test (create a Blueprint asset, add one variable, add one function node, compile) as a pre-fire gate for the vertical-slice spike specifically. Low effort; high signal. Not blocking WS1/WS3 commissions — those don't require Blueprint authoring.

**Cite:** Discipline #1 (math-before-code — empirical evidence before commissioning dependent work); Discipline #11 (empirical-first inspection at load-bearing surface).

---

### INFO-001 — Decisions-log entry warranted for db-lyon primary adoption

**Severity:** INFO

**Summary:** The spike output locks db-lyon as primary MCP bridge for all downstream workstreams (WS1-WS5 + vertical-slice spike). This is an architectural commitment. The decisions-log does not currently record it. A decisions-log entry proposal should route to Mac-jack-ryan for canonical write per sam-OP drift-discipline § 6.6.

**Scope:** Decisions-log entry proposal (this is a Mac-jack-ryan canonical-write; Sam proposes). See § 5 below.

**Cite:** sam-OP § 6.6 (proposals to Mac-jack-ryan); mac-jack-ryan decisions-log canonical-write authority; ADR-002 tiered approval.

---

### INFO-002 — `ue-mcp` package version not pinned; forward session risk

**Severity:** INFO

**Summary:** The install landed `ue-mcp@1.0.79` (current at spike time). The `.mcp.json` config does not pin a version (`"command": "npx", "args": ["ue-mcp", ...]` — `npx` without explicit version will fetch latest on first invocation in a cold-cache environment). If db-lyon publishes a breaking change, future mantis sessions on a cold npm cache could silently pull a different version.

**Evidence:** install-record § 8 explicitly notes "Future runs will pick up latest unless version-pinned." The spike identified this but did not resolve it.

**Recommended action (informational — not blocking):** Pin the version in `.mcp.json` args as `["ue-mcp@1.0.79", ...]` or add a project-level `package.json` with `ue-mcp` locked to `1.0.79`. Defer to productionization workstream if preferred; document the risk in session-boundary-memo or AGENT_STATE.md.

**Cite:** PC-seam internal; no cross-cutting implication.

---

### INFO-003 — BUSL-1.1 commercial deployment license gate requires Matt-explicit action before WS5

**Severity:** INFO (escalation trigger documented, not imminent)

**Summary:** Spike-findings.md § 5 correctly documents commercial-license inquiry timing as "pre-WS5." The `ue-mcp.com/pricing` page was unreachable per Matt 2026-06-08. If pricing is opaque at WS5 scoping time, there is a risk of arriving at productionization without having initiated the inquiry. The BUSL-1.1 Change Date mitigation (2030-06-06 → Apache 2.0) reduces but does not eliminate the risk for pre-2030 ship scenarios.

**Recommended action:** Ensure Mac-KR includes a commercial-license inquiry reminder in the WS4 commission (or standalone trigger) so that the inquiry fires before WS5 is scoped. Do not wait until WS5 commission authoring — if the inquiry returns concerning commercial terms, contingency planning time is needed.

**Cite:** spike-findings.md § 5; Principle #1 (surface risks early).

---

## 3. Discipline citations + candidates

### Disciplines observed

- **Discipline #1 (math-before-code):** OBSERVED. Legolas two-round research preceded installation and ratified the primary candidate.
- **Discipline #11 (empirical-first inspection):** OBSERVED for WS1 and WS3. PARTIALLY OBSERVED for WS2 — headless-mode crash documented but windowed-mode not yet empirically confirmed.
- **R48.4 (host-RAM-aware concurrency):** OBSERVED. Validation-log § 1.5 explicitly checks and documents RAM state before/after compile. Free RAM documented (~16.5 GB before launch; ~338 MB UE Editor headless working set). No concurrency violations.
- **Discipline #21 (no sleep recommendations):** OBSERVED throughout spike packet. No violations found.
- **Discipline #22 (timezone-agnosticism):** OBSERVED throughout spike packet. No violations found. One instance to note: UE log timestamps use UTC date notation (`[2026.06.09-01.08.21]`) — this is UE engine output, not agent-authored language, and does not constitute a Discipline #22 violation.

### Discipline candidates surfaced

**Candidate A — MCP tooling validation should distinguish read-only from mutation testing**

The spike validation tested mutation operations on DataTable (WS1) and Sequencer (WS3) but exercised Blueprint at read-only depth. A discipline candidate would specify: for any new MCP tooling adoption spike, each workstream-mapped tool category must be exercised at mutation depth (not just list/inspect operations) before the workstream commission is authorized. This distinguishes "bridge is reachable" from "bridge can author."

**Candidate B — Third-party dependency version pinning at adoption time**

When a third-party npm/pip/other dependency is adopted as a load-bearing tool layer (as opposed to a dev-only convenience), the version should be pinned at adoption time and recorded in the spike install record with an explicit pin-or-defer decision. Currently optional; should be explicit.

Both candidates are PC-seam-applicable observations with potential cross-seam relevance. Routing per sam-OP drift-discipline § 6.6: proposing to Mac-jack-ryan for cross-cutting ratification consideration.

---

## 4. Cross-cutting concerns

### 4.1 License compliance posture (BUSL-1.1)

**Assessment:** The spike's license framing is accurate. BUSL-1.1 non-production grant covers spike work definitionally. WS1-WS5 port workstreams are pre-launch internal development — the "likely still $0" framing is reasonable but unconfirmed. Commercial-license inquiry is correctly deferred to Matt-routed action.

**Decisions-log entry warranted?** YES — see § 5. The db-lyon adoption decision and its license posture (BUSL-1.1 with Change Date mitigation + commercial inquiry deferred to pre-WS5) should be captured as a decisions-log entry, not just a spike artifact.

**Escalation trigger:** If `ue-mcp.com/pricing` remains unreachable or inquiry returns opaque commercial terms, Matt needs early notification (not post-WS5). Mac-jack-ryan decisions-log entry proposal in § 5 includes this trigger.

### 4.2 UE project structural amendment (Blueprint-only → C++ project)

**Assessment:** Authority correctly claimed as PC-seam-internal per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 7. The `Source/` scaffold created is minimal (game module stub; no game logic). This is standard UE project structure for any plugin-augmented project. Sam ratifies this as PC-seam-internal decision. No Mac-gandalf consultation required.

**Composition note for downstream commissions:** Future WS1-WS5 mantis sessions that author gameplay C++ code will build on this `Source/` scaffold. The scaffold choices (BuildSettingsVersion.V6, IncludeOrderVersion.Unreal5_7) should be documented in mantis AGENT_STATE.md so future sessions don't re-derive them.

### 4.3 MCP server registration at user-level `~/.claude/settings.json`

**Assessment:** PC-seam-internal. The user-level settings path (`C:\Users\mhwet\.claude\settings.json`) is on PC user profile; Mac-side Claude Code sessions do not inherit this. No cross-host implication from the config write itself. Validation-log § 1.3 correctly notes the naming collision check (meta-repo has its own `.mcp.json`; UE project is a separate directory — no collision). Sam ratifies as PC-seam-internal.

**Forward note:** If a Mac-resident session ever needs MCP bridge access (SSH-tunnel scenario), a separate Mac-side registration step is required. This is documented and deferred — correct disposition.

### 4.4 SSH-tunnel cross-host scenario

**Assessment:** Correctly deferred to "Matt-driven validation if needed." The PC-resident mantis invocation pattern is the primary execution mode; SSH-L forwarding is architecturally compatible but untested. The deferred disposition is appropriate for now.

**Stronger disposition recommended:** Rather than open-ended deferral ("if Mac-resident direct-bridge-access were ever needed"), a discrete trigger should be defined: if Mac-KR or gandalf authors a commission that requires Mac-resident Claude Code sessions to drive PC-side UE Editor, that commission should include a SSH-tunnel validation step before the commission's tooling-layer work begins. This prevents the "discovered at commission-fire" failure mode.

This is a PC-seam-internal framing concern. No Mac-jack-ryan routing needed.

---

## 5. Proposals to Mac-jack-ryan (decisions-log + engineering-discipline)

### Proposal 1 — Decisions-log entry: db-lyon/ue-mcp adoption as primary MCP bridge

**Route to:** Mac-jack-ryan (decisions-log canonical-write authority per jack-ryan OP)
**Via:** Sam consultation note at `agentic_orchestration/sam/notes/2026-06-08-proposal-mac-jack-ryan-db-lyon-decisions-log.md`

**Proposed entry summary:**
- **Decision:** Adopt db-lyon/ue-mcp v1.0.79 as primary MCP bridge for Reincarnated UE 5.7 port workstreams (WS1-WS5 + vertical-slice spike execution)
- **Reasoning:** Three-way legolas comparison (legolas research `554da75`) demonstrated db-lyon's capability advantage over NAJEMWEHBE and StraySpark on the load-bearing WS1/WS2/WS3 surfaces (DataTable: 11 actions vs 2; Niagara: 28 actions vs 3; Sequencer: comparable). Spike empirically confirmed WS1 DataTable CRUD + WS3 Sequencer PASS. BUSL-1.1 $0 non-production grant covers dev-time evaluation; commercial-license inquiry deferred to pre-WS5 timing.
- **Status:** ACTIVE (conditional on windowed-mode Niagara verification before WS2)
- **Alternatives:** NAJEMWEHBE (MIT, migration cost MEDIUM per legolas § 6); StraySpark (commercial pricing opaque); Remote Control HTTP build-from-scratch (retired by AMENDMENT)
- **Related:** AMENDMENT dispatch 2026-06-08; spike-findings 2026-06-08; federated-pc-team-architecture-commit § 7

**Cross-cutting flag:** This decision affects Mac-side commission authoring (gandalf WS1/WS3/WS2 commissions inherit db-lyon tooling layer). Mac-jack-ryan should include a cross-cutting review note at canonical-write time.

### Proposal 2 — Engineering-discipline ratification candidates (Candidates A and B from § 3)

**Route to:** Mac-jack-ryan (engineering-disciplines.md canonical-write authority)
**Via:** Same consultation note as Proposal 1 (compound proposal)

**Candidate A:** MCP tooling adoption spike discipline — mutation-depth testing required per workstream-mapped category before commission authorization.
**Candidate B:** Third-party dependency version pinning at adoption — explicit pin-or-defer decision at adoption time.

Both candidates are PC-seam-surfaced with cross-seam applicability. Routing per sam-OP drift-discipline § 6.6. Mac-jack-ryan evaluates cross-seam scope; may ratify, defer, or return to Sam for PC-seam-only version.

---

## 6. Gate-2 verdict

**Verdict: PASS-with-WARN**

The spike GREEN verdict is ratified with the following qualifications:

**Authorized by this Gate-2:**
- WS1 commission authoring (gandalf) — DataTable CRUD empirically confirmed; cosmograph JSON ingestion primitive operational
- WS3 commission authoring (gandalf) — Sequencer authoring empirically confirmed
- Vertical-slice spike execution inheriting db-lyon tooling layer — with BP mutation smoke test as pre-fire addition (WARN-002)
- db-lyon as named primary MCP bridge — decisions-log entry proposal routed to Mac-jack-ryan (INFO-001)

**Gated by this Gate-2 (not yet authorized):**
- WS2 commission authoring — gates on windowed-mode empirical verification of `add_emitter_to_system` (WARN-001). This is a hard gate, not a recommendation. WS2 commission does NOT fire until mantis windowed-mode sub-session returns PASS or the workaround path (`create_niagara_system_from_spec`) is confirmed adequate.

**No BLOCKs issued.** The spike packet is complete, empirically grounded, and authority-compliant. WARN items are qualifications to downstream authorization scope, not findings that require spike rework.

**ADR-002 tiered-approval scope:** WARN items are PC-seam-internal resolutions; no Matt escalation required unless windowed-mode Niagara verification returns a failure (which would then require reassessment of WS2 commission scope and potentially a new spike decision).

---

## 7. Sign-off

**Reviewer:** sam (PC-side QA gatekeeper)
**Mode:** DEV-MODE Gate-2
**Date:** 2026-06-08
**Commit:** auto-commit per CLAUDE.md PC team auto-commit table (sam row: "PC-seam Gate-1 / Gate-2 findings")
**Push:** Matt-action required per session-boundary-memo § 5.1 credential-gap

**Downstream routing:**
- David-H: consumes Gate-2 verdict; routes WARN-001 to WS2 pre-commission gate; routes WARN-002 to vertical-slice spike pre-fire sequence
- Mac-KR: cross-host fetch at next Mac session; ensures gandalf WS2 commission preamble includes windowed-mode verification prerequisite language
- Mac-jack-ryan: receives Proposal 1 + Proposal 2 via sam consultation note at `agentic_orchestration/sam/notes/2026-06-08-proposal-mac-jack-ryan-db-lyon-decisions-log.md`
- Matt: no escalation actions required from this Gate-2; WARN items are PC-seam-resolvable

**End of Gate-2 finding.**
