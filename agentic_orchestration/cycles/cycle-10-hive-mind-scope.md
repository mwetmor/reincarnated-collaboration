# cycle-10-hive-mind-scope

> **STATUS:** RATIFIED 2026-05-25 — Matt ratification per session dialogue
> **Cycle:** 10
> **Cycle subject:** v1 weapon-library substrate-curation + composition (Stages 0 → 3 → 3.5 → 4 + Sidecars A/B)
> **Canonical protocol doc:** none — Cycle 10 operates as a multi-stage non-hive-mind sprint per gandalf's 2026-05-23 multi-stage dispatch authoring (see `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md`)
> **Effective:** 2026-05-25 through Cycle-10-final-tag (estimated v1.0-weapon-substrate-cycle-10-shipped)
> **Pattern context:** Cycle 10 is the founding retroactive example of `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md` — authored mid-cycle to resolve recurring KR over-asking behavioral bug

---

## 0. Cycle state at scope-doc authoring

**Completed:**
- Stage 0 — v1 BC-target intent locked (Matt + gandalf design call 2026-05-24)
- Stage 1 — elrond cheap-proxy mechanical-fingerprint dispatch fired + executed
- Stage 1.5 — elrond per-source structured-field extractor dispatch fired + executed
- Stage 2 — elrond cross-tab thin-cell surfacing dispatch fired + executed
- Stage 2.5 — elrond quality-tier scoring dispatch fired + executed
- Stage 3 design call (D1-D7 locked; composition policy v1 canonical authored; Architecture B locked; sub-element rename)
- Wave 5 — Stage 3 execution dispatch FIRE-READY (per knight-rider commit `04509ad`)

**In-flight / queued:**
- Wave 5 — Stage 3 execution dispatch FIRE (elrond)
- Wave 6 — Stage 3.5 engine-authored gap-fill dispatch authoring + FIRE
- Wave 7 — Stage 4 mythological-NULL rescue dispatch authoring + FIRE
- Sidecar A — substrate-genre-flagging unified-architecture amendments *(terminology note: "Sidecar A" at scope-doc authoring time labeled a substrate-genre-flagging pass; in practice the Sidecar A workstream executed as a 5-weapon image-pass-through-vs-LLM-description Meshy pipeline comparison per gandalf weapon-nomination verdict 2026-05-23 at `agentic_orchestration/gandalf/notes/2026-05-23-sidecar-A-weapon-nomination-verdict.md`. Both framings are consistent: the Meshy comparison is the empirical instrument that gates the image-pass-through decision, which is itself substrate-genre-pipeline-adjacent work. Accept-document per jack-ryan judgment 2026-05-25 — founding-instance artifact preserved as-is with this clarifying note.)*
- Sidecar B — substrate-enrichment (off-hand items + thin-cell + thin-tradition)
- Cycle wind-down + final tag

**Out of cycle (separate workstream):**
- T4 algorithm-as-v1-deliverable design (gandalf canonical authoring queue; not under KR orchestration in Cycle 10)
- Loadout app readiness scoping (drax territory; separate workstream)

---

## 1. In-scope autonomous decisions (knight-rider fires without re-asking)

KR fires the following without per-decision Matt re-asking:

- **Dispatch authoring** for any cycle-scoped stage already named in the multi-stage dispatch (Stages 3, 3.5, 4; Sidecars A, B) — including authoring the dispatch text, sequencing parallel sub-agent invocations, defining acceptance criteria consistent with composition policy v1
- **Sub-agent invocation sequencing** — when to fire parallel vs sequential; which seam-owners to consult for cross-seam questions; how to integrate sub-agent returns
- **Wave-internal failure handling** — retry, scope-reduce, route-to-seam-owner per hive-mind-protocol.md § 3.2
- **Acceptance criterion application** — checking dispatch outputs against acceptance criteria; declaring Wave complete vs requiring rework
- **State-file updates** — per-Wave / per-Phase status capture
- **Intermediate tag-cutting** — per-Wave or per-Phase milestone tags per ADR-001 convention; Matt-approved final tag asks for explicit ratification
- **Gate-1 critique-pair coordination** — sending dispatches to jack-ryan / gandalf for critique-pair review per `dispatches/README.md`; integrating critique-pair returns
- **Decision-routing per hive-mind-protocol.md § 4** — seam-owner-first sub-agent invocation for any cross-seam decision surfacing in cycle execution

## 2. In-scope autonomous executions

KR executes the following without re-asking:

- All Wave 5 / 6 / 7 / Sidecar dispatches once authored + critique-pair-cleared
- Background-process firing per Discipline #19 (nohup, PID tracking, log capture)
- Sub-agent invocations per § 1 above
- Cross-seam parallel critique invocations (jack-ryan + gandalf simultaneously for Gate-1)
- DB queries against catalogue substrate for cycle-state verification
- State-file + JSON-summary reads for cross-session continuity

## 3. In-scope autonomous commits

Per CLAUDE.md § "Team commit + push discipline" addendum (2026-05-25), KR AUTO-COMMITS:

- Dispatch artifacts (newly authored dispatches)
- State-file updates
- Wave-closeout summaries
- Gate-1 critique-pair coordination artifacts
- Per-Wave intermediate tag commits
- Sub-agent return capture artifacts (when capturing on sub-agent's behalf per hive-mind-protocol.md § 5.5.4 file-write-constraint pattern)

Commit timing: at natural seams (Wave completion, dispatch authoring close, critique-pair clearance). Do not batch beyond a single workstream-day without strong reason.

## 4. Push posture for this cycle

**RATIFIED:** `push-per-wave` — auto-push after each Wave completion AND after each major artifact authoring (dispatch fire-ready, state-file update, scope-doc ratification).

**Rationale per Matt 2026-05-25 verbatim:** *"knight-rider could have chosen to delay commit/push (although I prefer he does commit push) and still followed hive mind protocol"* — Matt's explicit preference is commit+push for cycle work-products; this scope-doc ratifies that preference for Cycle 10.

**Override:** if a Wave includes uncommitted multi-day work that's mid-experiment (substrate-state mid-mutation, e.g.), KR can defer push until experiment stabilizes — flag deferral in state-file.

## 5. Out-of-scope — MUST escalate to Matt

KR escalates the following:

- **Architectural amendments** to canonical docs (composition policy v1, Architecture B, attribute-system, skill-system, off-hand-items, ground-state, roadmap) — gandalf authors; Matt ratifies; KR does NOT amend canonical without gandalf+Matt approval
- **Scope amendments to Cycle 10** — adding new stages beyond Stages 3/3.5/4 + Sidecars A/B; changing v1_scope target; changing composition policy
- **Cross-cycle commits** — anything outside Cycle 10 substrate-curation scope (e.g., Cycle 11 prep, T4 algorithm work, loadout app changes)
- **ADR-002 tier-2/3 decisions** — anything per `GOVERNANCE.md` ADR-002 requiring Matt
- **Final cycle tag** (`v1.0-weapon-substrate-cycle-10-shipped` or equivalent) — Matt ratifies before final tag is cut
- **Cycle wind-down summary author + close** — KR drafts; Matt reviews + ratifies before cycle officially closes

## 6. Pre-resolved known-unknowns

| If this happens | Then |
|---|---|
| Stage 3 execution surfaces a thin-cell pattern that composition policy v1 doesn't address | Route to gandalf sub-agent for design-fit critique; integrate return; fire forward without Matt re-asking unless gandalf escalates |
| Stage 3.5 engine-authored gap-fill produces results that contradict Stage 3 substrate-bound output | Route to rocket sub-agent for engine-side triage + gandalf sub-agent for design-fit; if both seam-owners converge on a path, fire forward; if divergent, escalate to Matt |
| Stage 4 mythological-NULL rescue produces fewer than expected named-personage forms | Apply per-cell composition policy fallbacks (Sketch F anchor disposition per D5); do NOT pause for Matt unless total v1_scope drops below ~1,700 items |
| Sidecar B substrate-enrichment surfaces a substrate-tagging artifact (Mode B/C/D per marginal-lineage pattern) | Apply semantic-layer rep-audit discipline per gandalf OP § 4.4; if cluster identity must be downgraded, route to gandalf sub-agent; do NOT escalate unless cluster downgrade affects > 5 cells |
| A Wave's specialist fails mid-execution | Apply hive-mind-protocol.md § 3.2 Wave-internal failure handling; route to seam-owning sub-agent for triage; do NOT pause cycle unless failure affects critical path |
| jack-ryan Gate-1 returns a BLOCK on a dispatch | KR works with jack-ryan on remediation; if remediation requires gandalf design input, invoke gandalf sub-agent; only escalate to Matt if remediation requires architectural amendment (per § 5) |
| KR encounters a decision genuinely unenumerated by this scope-doc | Default to in-scope per hive-mind-scope-discipline § 5.3 anti-pattern guard; fire forward via hive-mind decision-routing § 4 (seam-owner-first); flag the gap to gandalf for next-cycle scope-doc refinement |

## 7. Cross-cycle escalation triggers

Scope-doc applicability ENDS (triggers re-scoping) when:

- Cycle 10 final tag is cut (then Cycle 11 scope-doc authored)
- Matt issues a directive that materially changes Cycle 10 scope (e.g., "pause Cycle 10 to pivot to X")
- An architectural recognition surfaces mid-cycle that warrants protocol amendment (gandalf authors recognition record; Matt ratifies scope-doc amendment OR cycle-reset)

---

## 8. Sign-off

**Drafted by:** gandalf (story-and-design steward) 2026-05-25
**Ratified by:** Matt 2026-05-25 — session dialogue ("1 = ratify; 2 = default is right; 3 = yes, back-port it")
**Authority basis:**
- `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md` (the discipline this doc instantiates)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` (Cycle 10 multi-stage scope)
- Matt 2026-05-23 verbatim hive-mind decision-routing directive
- Matt 2026-05-25 verbatim push-preference: *"although I prefer he does commit push"*
- CLAUDE.md § "Team commit + push discipline" (2026-05-25)

**Effective on ratification.** Until ratified, the prior implicit-scope-inference pattern remains in effect (which is the failure mode this doc resolves — so prompt ratification matters).
