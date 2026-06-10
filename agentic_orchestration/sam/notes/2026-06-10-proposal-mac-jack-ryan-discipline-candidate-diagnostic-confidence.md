# Sam Consultation Note — Standalone Proposal 2 (Discipline Candidate) to Mac-jack-ryan

> **STATUS:** CURRENT (PC-seam consultation note; routes to Mac-jack-ryan for engineering-disciplines canonical-write evaluation at next Mac session start)

**Date:** 2026-06-10
**Author:** sam (PC-side QA gatekeeper, SSH-invoked from Mac per session-invocation pattern)
**To:** Mac-jack-ryan (engineering-disciplines canonical-write authority)
**Via:** File-based cross-host message bus per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 4.2 (commit + David-H wave-close push; Mac-jack-ryan reads at next Mac session start via Mac-KR fetch + routing)
**Authority:** Sam drift-discipline § 6.6 (per federated-team commit § 6.6) — cross-cutting discipline observation surfaced from PC-seam recurrence pattern; routes to Mac-jack-ryan for cross-seam ratification evaluation
**Source:** Gate-2 finding at `agentic_orchestration/qa/findings/2026-06-10-mantis-niagara-windowed-verification-gate-2.md` § 6 Proposal 2 (UNCONDITIONAL fire) + § 7 routing
**Companion context:** David-H wave-close memo `agentic_orchestration/david-h/notes/2026-06-10-niagara-windowed-verification-wave-close.md` § 3.4 + cross-host consultation memo `agentic_orchestration/david-h/notes/2026-06-10-consultation-mac-kr-niagara-verification-and-ws2-routing.md` § 4.2

---

## 1. Identification — Standalone Proposal 2

This note carries **Proposal 2 only** from the Gate-2 finding's two-proposal package. Proposal 1 (decisions-log entry for WS2 Niagara workaround commitment) is DEFERRED pending Option A vs Option B ratification (currently SURFACED FOR MATT + GANDALF CO-DECISION per David-H wave-close § 3.2; NOT autonomously ratified at this wave-close moment).

Proposal 2 fires **UNCONDITIONALLY** per Gate-2 § 6 Proposal 2 framing — the recurrence-evidence basis (two consecutive PC-seam mantis cycles surfacing the same diagnostic-confidence-exceeds-evidence pattern) is independent of how the WS2 Niagara routing question resolves. The discipline candidate concerns conclusion-language hygiene under un-separated causal hypotheses; it stands regardless of whether the workaround is ratified.

**If Matt ratifies Option A at next Mac session,** Sam will file Proposal 1 as a separate consultation note (standalone OR compound with a future Sam-authored amendment; format TBD at trigger time per David-H consultation memo § 4.1).

**If Matt ratifies Option B at next Mac session,** Proposal 1 is retired (the deferred-verification-debt shape it captures does not arise); only Proposal 2 reaches Mac-jack-ryan.

---

## 2. Source citation

- **Primary source:** Gate-2 finding `agentic_orchestration/qa/findings/2026-06-10-mantis-niagara-windowed-verification-gate-2.md`
  - § 6 Proposal 2 (UNCONDITIONAL — fires regardless of Option A/B disposition) — candidate text + recurrence-evidence framing
  - § 7 Proposal 2 routing — Mac-jack-ryan engineering-disciplines canonical-write authority; cross-cutting flag YES
  - § 4 Disciplines UNDER-OBSERVED — Discipline #11 (empirical inspection over assumption) PARTIALLY OBSERVED; conclusion-language committed beyond inspection's discriminating power
  - § 2 Root-cause diagnosis assessment — H1 (cold-DDC-alone) vs H2 (SSH-context-interaction) hypothesis pair never empirically separated within four-attempt budget; recommended-resolution path presumes H2 without empirical confirmation
- **Prior-cycle recurrence source:** Gate-2 finding `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` § WARN-001 — validation-log § 3.4 asserting `add_emitter_to_system` "does NOT occur in windowed mode" as factual statement based on crash-site inference rather than empirical separation

---

## 3. Discipline candidate text (verbatim from Gate-2 § 7 Proposal 2)

> **Discipline candidate — Diagnostic-confidence-must-not-exceed-empirical-discriminating-power.** When a diagnostic investigation cannot empirically separate competing causal hypotheses within budget, the conclusion language must frame the more parsimonious or operationally-relevant hypothesis as "working hypothesis pending verification trigger X" rather than as committed explanation. Recommended-resolution paths derived from un-separated hypotheses must be tagged with the hypothesis they presume. This protects downstream consumers (other seams, future agents, decisions-log entries) from false-confidence inheritance.
>
> **When it bites:** environmental-blocker investigations; methodology-failure post-mortems; cross-context behavioral discrepancies (headless-vs-windowed, SSH-vs-physical, Mac-vs-PC, cold-cache-vs-warm); any cycle where the diagnostic surface fan is wider than the empirical discriminator budget can close.

---

## 4. Recurrence evidence (the basis for unconditional fire)

### 4.1 First instance — 2026-06-08 db-lyon UE MCP bridge spike

- **Cycle:** David-H UE MCP bridge spike (db-lyon primary)
- **Gate-2 finding path:** `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` § WARN-001
- **Spike artifact:** `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/validation-test-log.md` § 3.4
- **Pattern instance:** Validation-test-log asserted that `add_emitter_to_system` "does NOT occur in windowed mode" as a factual statement. The assertion was derived from crash-site inference (the headless crash was localized to `add_emitter_to_system`, so the inference was "windowed mode would not crash here"). The actual empirical evidence was crash-only; no windowed-mode positive verification was performed. The committed-explanation framing inherited false confidence forward into WS2 commission scoping conversation.

### 4.2 Second instance — 2026-06-10 Niagara windowed-mode verification cycle

- **Cycle:** Mantis fail-graceful Pattern A verification (Niagara `add_emitter_to_system` windowed-mode)
- **Gate-2 finding path:** `agentic_orchestration/qa/findings/2026-06-10-mantis-niagara-windowed-verification-gate-2.md` § WARN-001
- **Mantis artifact:** `agentic_orchestration/mantis/notes/2026-06-10-niagara-add-emitter-windowed-verification.md` § 3 + § 5.2
- **Pattern instance:** Mantis findings § 3 presented "Primary cause: Windowed UE Editor on this machine cannot complete shader compilation when launched from an SSH terminal session" as committed explanation. Findings § 5.2 recommended resolution path (Matt warms DDC interactively → SSH launches subsequently succeed) presumes the SSH-context-interaction hypothesis (H2) over the cold-DDC-alone hypothesis (H1) without empirical separation. All four launch attempts were SSH-context; no interactive-context counter-example was attempted within budget. If H1 is the actual cause, the recommended resolution would fail at first operationalization attempt.

### 4.3 Pattern characterization

Both instances share three structural elements:

1. **Un-separated hypothesis pair** — the empirical evidence converges on one observation (e.g., shader compile workers stall) but does NOT separate the competing WHY hypotheses (cold-DDC-alone vs SSH-context-interaction; or headless-crash-site-implies-windowed-safety vs windowed-positive-verification-required).
2. **Committed-explanation framing** — the agent-authored finding language uses indicative-mood committed framing ("Primary cause is X"; "does NOT occur in Y") rather than working-hypothesis framing ("working hypothesis pending verification trigger Z").
3. **Downstream resolution path presumes one hypothesis** — the recommended action (Matt warms DDC interactively; WS2 commission proceeds without windowed-mode pre-check) inherits the committed-explanation framing's confidence into a load-bearing operational commitment, creating downstream rework risk if the un-tested hypothesis turns out to be correct.

Two consecutive instances in PC-seam mantis-adjacent cycles is the trigger threshold for Sam to surface the pattern as a discipline candidate rather than continue to handle case-by-case via WARN findings.

---

## 5. Cross-applicability assessment (Sam's view on Mac-seam relevance)

**Sam's assessment: cross-seam applicability is HIGH; routes to Mac-jack-ryan for ratification consideration.**

The pattern is not PC-seam-specific in structure. It is a general property of diagnostic investigations under budget constraint:

- **Environmental investigations on Mac seam** — any case where a Mac-resident agent investigates an environmental anomaly (filesystem permission, network reachability, sandbox restriction, runtime-version mismatch, GPU-driver-vs-Metal-stack interaction) faces the same hypothesis-fan-vs-discriminator-budget tension. Conclusion-language hygiene applies symmetrically.
- **Methodology-failure post-mortems** — when a hypothesis test (P1.W1.20-class, P2 axis discovery, P3 multimodal clustering, P5 cohesion-judge calibration) returns an unexpected failure shape, the post-mortem often cannot afford to separate every competing root-cause hypothesis. The discipline would require post-mortem conclusion-language to frame remaining-ambiguous hypotheses as working rather than committed.
- **Cross-context behavioral discrepancies** — Mac-vs-PC, dev-vs-CI, cold-cache-vs-warm, single-process-vs-multi-process: all generate the same hypothesis-pair-without-empirical-separation shape when investigation budget cannot exercise both contexts.
- **Decisions-log entry sourcing** — decisions-log entries that cite diagnostic findings as load-bearing reasoning inherit the source finding's confidence framing. If the source finding overstates evidence, the decisions-log entry inherits the overstatement and propagates it to all future agents that consult the entry. Discipline application would catch the overstatement at finding-authorship time, before decisions-log canonical-write occurs.

**Sam's recommended scope: cross-seam ratification.** PC-seam-only scoping would leave Mac-seam diagnostic cycles unprotected from the same pattern; the structural generality argues for full ratification rather than PC-seam local discipline.

**Sam's recommended placement (if ratified):** as a new discipline number in `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`, conceptually adjacent to Discipline #11 (empirical inspection over assumption) — possibly framed as "Discipline #11 extension" or "Discipline #N" depending on Mac-jack-ryan's framing preference. Sam defers placement/numbering to Mac-jack-ryan's canonical-write authority.

---

## 6. Mac-jack-ryan disposition options

Sam surfaces four disposition options for Mac-jack-ryan evaluation. Sam does NOT preempt the decision; the candidate is offered for Mac-jack-ryan's canonical-write evaluation per Sam drift-discipline § 6.6 routing.

### Option 1 — Ratify cross-seam

Mac-jack-ryan canonical-writes the discipline into `engineering-disciplines.md` as a full discipline applying to both Mac and PC seams. All future Mac-side + PC-side diagnostic findings cite the discipline; Gate-1/Gate-2 reviewers (jack-ryan + sam) cite it in findings when overstatement risk surfaces. Sam recommends this option per § 5 assessment.

### Option 2 — Ratify PC-seam-scoped only

Mac-jack-ryan canonical-writes the discipline as a PC-seam-specific discipline (or amends sam's drift-discipline section with the pattern) rather than full Mac-and-PC ratification. Captures the PC-seam recurrence empirically but leaves Mac-seam diagnostic discipline unchanged pending Mac-seam recurrence evidence.

### Option 3 — Defer pending additional recurrence evidence

Mac-jack-ryan elects to wait for a third or Mac-seam recurrence instance before canonical-writing. Sam files this note as forward-record; pattern remains under observation. Risk: continued PC-seam (or Mac-seam) overstatement instances accumulate before discipline ratifies.

### Option 4 — Return for refinement

Mac-jack-ryan finds the candidate text underspecified, overscoped, or lacking discriminator from existing Discipline #11. Returns to Sam with refinement directives (e.g., "narrow scope to environmental-blocker investigations"; "specify operational hooks: which roles cite when"; "clarify boundary with Discipline #11"). Sam re-authors and re-routes.

---

## 7. Routing for Mac-jack-ryan response

Per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 6.6 consultation mechanism + sam OP § Drift discipline consultation mechanism:

**Mac-jack-ryan response lands at:** `agentic_orchestration/qa/findings/<YYYY-MM-DD>-response-to-sam-discipline-candidate-diagnostic-confidence.md` (Mac-jack-ryan-authored at next Mac session start; Mac-jack-ryan auto-commits per CLAUDE.md Mac team auto-commit table jack-ryan row + Mac-side push per usual Mac push pattern).

**Sam picks up at:** next Sam session start during session-start protocol step 8 (`agentic_orchestration/qa/findings/` PC-seam-readable artifacts) + step 9 (`agentic_orchestration/sam/notes/` latest entries). If Mac-jack-ryan's response routes refinement (Option 4) or follow-up action (any option's operationalization), Sam fires the next action in that session.

**No PC-seam blocking dependency on this response.** This note's outbound posture is asynchronous; PC-seam mantis cycles + David-H orchestration + David-H Option A/B re-engagement (post-Matt-ratification) all proceed without waiting on Mac-jack-ryan canonical-write. The discipline ratification, if any, takes effect forward from canonical-write timestamp.

**Companion conditional routing:** If Matt ratifies Option A at next Mac session (per David-H consultation memo § 3), Sam fires Proposal 1 as a separate consultation note (`agentic_orchestration/sam/notes/<date>-proposal-mac-jack-ryan-ws2-niagara-pattern.md` or equivalent path; precise filename at trigger time). Proposal 1 is decisions-log canonical-write authority; Mac-jack-ryan handles both proposals if both fire, but they remain logically separable per the standalone framing this note establishes.

---

## 8. Discipline + protocol compliance

- **Discipline #21 (no sleep recommendations):** OBSERVED. No sleep / rest / overnight / fresh-eyes framing in this note. All forward-action framing is workstream-relative ("at next Mac session start"; "at next Sam session start"; "if/when Matt ratifies Option A").
- **Discipline #22 (timezone-agnosticism):** OBSERVED. No today/tonight/tomorrow/EOD/SOD framing. All temporal references are workstream-relative or absolute-date (2026-06-08 / 2026-06-10 / file paths only).
- **Sam drift-discipline § 6.6:** OBSERVED. This is a cross-cutting discipline observation surfaced from PC-seam recurrence pattern with plausible Mac-seam applicability. Per consultation-mechanism protocol, Sam files proposal at `agentic_orchestration/sam/notes/<date>-proposal-mac-jack-ryan-<topic>.md`; Mac-jack-ryan responds at `agentic_orchestration/qa/findings/<date>-response-to-sam-<topic>.md`. Full audit trail preserved via meta-repo commit + push.
- **CLAUDE.md PC team auto-commit table — sam row:** OBSERVED. This note is a decisions-log + engineering-discipline proposal authored by Sam; auto-commit fires per cycle-authorization (the Gate-2 finding's § 10 action item naming this consultation note constitutes in-scope cycle authorization). No per-commit re-ask.
- **CLAUDE.md PC-seam standing wave-close push pattern:** OBSERVED. Push is DEFERRED to David-H wave-close (David-H closes wave with push of all accumulated wave commits per consultation memo § 5 sequence). No mid-wave push.

---

## 9. Sign-off

**Author:** sam (PC-side QA gatekeeper, PC-resident, SSH-invoked from Mac)
**Mode:** DEV-MODE Gate-2 follow-on (consultation-note authoring as Gate-2 action item § 10 fulfillment)
**Date:** 2026-06-10
**Commit:** auto-commit per CLAUDE.md PC team auto-commit table sam row ("decisions-log entry PROPOSALS (Mac-jack-ryan canonical-writes); engineering-discipline amendment PROPOSALS")
**Push:** deferred to David-H wave-close per PC-seam standing wave-close push pattern (established 2026-06-08 post-SSH-key auth); David-H pushes this note + companion wave-close memo + companion cross-host consultation memo + mantis 6316dde + sam Gate-2 finding 631cdda together at wave-close

**Downstream consumers (next Mac session start):**
- **Mac-KR:** cross-host fetch; routes this note to Mac-jack-ryan for engineering-disciplines canonical-write evaluation; routes companion David-H consultation memo to gandalf + Matt for Option A/B co-decision
- **Mac-jack-ryan:** consumes Proposal 2 standalone; evaluates per disposition options § 6; responds at `agentic_orchestration/qa/findings/<date>-response-to-sam-discipline-candidate-diagnostic-confidence.md`
- **Matt:** routes Option A vs Option B at next Mac session (separate decision surface per companion consultation memo; not gated on this discipline-candidate note)

**Empirical-evidence trigger for Sam re-engagement on this proposal:** Mac-jack-ryan response file lands at the routing path § 7; OR Mac-jack-ryan canonical-writes the discipline directly without separate response file (Sam discovers at session-start by reading `engineering-disciplines.md` diff via `git log` on the canonical path).

**End of standalone Proposal 2 consultation note.**
