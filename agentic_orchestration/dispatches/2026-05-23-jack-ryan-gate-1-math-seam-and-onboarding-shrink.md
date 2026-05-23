# Dispatch — 2026-05-23 — jack-ryan — Gate-1 process review of math-seam-naming + onboarding-list shrink

**From:** knight-rider
**To:** jack-ryan (DESIGN-MODE; Gate-1 critique pair)
**Approved by:** Matt 2026-05-23 (cleanup-pass momentum continuation; option (a) confirmed in active session)
**Authority chain:** Matt 2026-05-23 → gandalf request → knight-rider dispatch → jack-ryan execution
**Estimated effort:** ~40-60 min (single Pattern-B session; two artifacts in one batch)
**Acceptance:** PASS / PASS-WITH-AMENDMENTS / BLOCK per-artifact judgment with concrete reasoning; output committed back to this dispatch as completion record

---

## Context

This is the second Pattern-B Gate-1 dispatch in the 2026-05-23 cleanup pass. The first dispatch (`2026-05-23-jack-ryan-gate-1-phase-D-dispatch.md`) scoped only the Phase D cleaning-pipeline review and returned PASS-WITH-AMENDMENTS (tag `jack-ryan/gate-1-phase-D-2026-05-23`; 5 amendments, 1 critical — Step 6.5 canonical-normalization).

Two additional cleanup-pass artifacts authored by gandalf still need your process-side review before knight-rider integrates them:

1. **Math-seam-naming declaration** — Mathematical Layer text for AGENTS.md + Discipline #1.1 (methodology-before-execution) + math-hotspot annotations on both active P-phase protocols
2. **Per-agent onboarding-list shrink** — Phase-1 read-list pruning per agent, anchored on `canonical/00-ground-state.md` + `canonical/38-downstream-delivery-strategy-2026-05-23.md` as universal first-reads

Both artifacts target high-leverage working-agreement changes. The math-seam artifact touches discipline numbering and AGENTS.md scope-mapping; the onboarding-shrink artifact touches every agent's Phase-1 invocation behavior. Process-side review is load-bearing before knight-rider applies either.

Critical context for both: Matt's 2026-05-23 morning diagnosis named documentation slowdown root causes — **epoch-collision-in-flat-namespace, no retirement protocol, decisions-log staleness, per-agent Phase-1 lists growing without bound**. The first three are addressed by the ground-state oracle + epoch-stamping pass (now landed in commit `fa8d070`). The fourth is what the onboarding-shrink request addresses. The math-seam naming is a parallel diagnostic outcome — Matt asked whether a dedicated mathematician agent was needed; gandalf's analysis concluded NO and surfaced this distributed-layer alternative with discipline-side guard.

---

## Artifact 1 — Math-seam-naming process review

**File:** `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md`

**Stress-test angles:**

1. **Discipline-numbering coherence.** Gandalf proposes "#1.1 as sub-discipline of #1 (math-before-code)." The current `engineering-disciplines.md` uses flat top-level numbering (#1, #2, ..., #17, #19 — note #18 gap). Is `#1.1` as a nested sub-discipline the right placement, or should this be top-level (e.g., `#18` filling the gap, or `#20` extending the sequence)? Argument for nested: methodology-before-execution is a refinement of math-before-code on a specific failure surface (hotspots). Argument for top-level: nested numbering is novel in this doc and may set a precedent the doc isn't ready for; flat #18/20 fits the existing style. Surface your preferred placement with reasoning.

2. **Cross-reference integrity.** Gandalf's note cites "Integration with Discipline #19 (right tool for the validation question)" — but in `engineering-disciplines.md`, **Discipline #4** is "Right tool for the validation question" and **Discipline #19** is "The Agent tool is not for waiting." Verify this cross-reference and flag the labeling error. Are there other cross-reference errors in the math-seam note (especially to AGENTS.md sections, hive-mind-protocol P-phase labels, or canonical doc paths)?

3. **Scope-creep risk on the Mathematical Layer declaration.** The proposed AGENTS.md insertion distributes math work across 5 named seams (gandalf / elrond / gamora / star-lord / galadriel) + legolas Mode A. Does this distribution create new ambiguity at seam boundaries? Specifically:
   - Is "design-spec-as-math (gandalf)" cleanly separable from "simulation-side math (gamora)" — e.g., when gandalf specifies a formula's algebraic structure and gamora implements its convergence behavior, who owns the math-hotspot determination?
   - Is "telemetry statistics (star-lord)" cleanly separable from "statistical methodology on catalogue data (elrond)" — both involve statistical methodology selection on data; is the data-source-locality split sufficient?
   - "Visual perception math (galadriel)" — does galadriel currently exist and own this work? Surface if this is forward-naming for a future agent.

4. **Math-hotspot annotation accuracy.** The note proposes inserting `[MATH HOTSPOT — ...]` annotations at P2/P3/P5 in both `hive-mind-protocol-weapon-library-import-2026-05-22.md` and `hive-mind-protocol-qd-engine-rebuild-2026-05-21.md`. Spot-check that the referenced phases (P2 axis discovery, P3 multimodal clustering, P5 cohesion-judge validation) actually exist in those protocols and are labeled as the gandalf note describes. If a phase numbering mismatch exists, the annotation will land at the wrong section.

5. **Integration-plan ordering (§ 5).** The proposed sequencing is: jack-ryan review → Matt approval → knight-rider integrates into AGENTS.md + engineering-disciplines.md + both hive-mind-protocol docs + ground-state oracle cross-reference. Is this ordering correct? Specifically: should the ground-state oracle entry land BEFORE or AFTER the AGENTS.md + engineering-disciplines.md edits? Should the hive-mind-protocol annotations land in the same commit or separate?

6. **Open questions in § 6.** Gandalf flags 3 open questions for Matt:
   - Should the doc be promoted to `canonical/story/` rather than `agentic_orchestration/gandalf/notes/`?
   - Should the named hotspot list be versioned in a single living doc (this doc § 2)?
   - Should the legolas-Mode-A-for-methodology pattern be formally named (MMC — Methodology Mode-A Consultation)?

   Each has a gandalf-recommended default. Do you concur with the defaults, push back, or surface a fourth question? These don't block draft acceptance but should be flagged in your judgment.

---

## Artifact 2 — Onboarding-list shrink per-agent review

**File:** `agentic_orchestration/gandalf/requests/2026-05-23-jack-ryan-onboarding-list-shrink.md`

**Stress-test angles:**

1. **Universal first-read pair holds for every role.** Gandalf proposes `canonical/00-ground-state.md` + `canonical/38-downstream-delivery-strategy-2026-05-23.md` as universal first-read across all 10 agents. Does this hold for every role? Specifically:
   - **legolas** — research-scout's Phase-1 budget is already lean (30-45 min); adding 2 universal reads on top of a task-specific commission may add overhead rather than reducing it. Is the universal pair load-bearing for legolas, or is `00-ground-state.md` alone sufficient (drop doc 38 for legolas)?
   - **drax** — player-facing developer rarely touches keystone delivery strategy day-to-day; is doc 38 load-bearing for drax's Phase-1, or consult-on-demand?
   - **jack-ryan (yourself)** — does the universal pair give you enough delivery-strategy context for Gate-1 reviews, or do you need additional docs not currently in the proposed list (e.g., REVIEW_PROCESS.md is removed from your Phase-1 — is that correct)?

2. **Per-agent shrink — load-bearing test.** For each of the 10 agents, is each named Phase-1 read truly load-bearing for that role's typical tasks, OR is the shrink too aggressive (missing a load-bearing doc)? Walk per-agent and flag any that look wrong:
   - **knight-rider** — 5 Phase-1 reads proposed (00 / 38 / latest skill_handoff / weapon-library-import state / AGENTS+GOVERNANCE+REVIEW_PROCESS). Sufficient for orchestrator role?
   - **jack-ryan** — 5 Phase-1 reads (00 / 38 / engineering-disciplines / decisions-log / current dispatch). Is REVIEW_PROCESS.md removal safe? You need it for the formal Gate-1/Gate-2 contract language.
   - **gandalf** — 5 reads (00 / 38 / own last 3 notes / style-register / legacy-categorical-cleanup-audit). Style-register inclusion correct? Last-3-notes-only is a tight limit.
   - **rocket** — 7 reads (00 / 38 / multi-dim-convergence / gear-substrate-rule-table / T4-architecture-defaults / engineering-disciplines / current dispatch). Heaviest per-agent list — is it justified by generation-seam's substrate-design density?
   - **gamora** — 6 reads. W1.13 rescope inclusion — load-bearing for current work or stale?
   - **star-lord** — 6 reads. `canonical/19-llm-call-map.md` inclusion — gandalf's open question #3 flags this; Matt should resolve. Default is to keep as Phase-1.
   - **elrond** — 6 reads. `weapon-library-import-wind-down-summary-2026-05-22.md` inclusion — is this still load-bearing post-Phase-D, or transitional only?
   - **galadriel** — 6 reads. Forward-naming agent or active agent? If forward-naming, the per-agent shrink is speculative.
   - **drax** — 5 reads, with 2 task-specific (current dispatch + relevant canonical/story/ docs named in dispatch). Fuzzy "relevant repo README + recent commits" — does this need tightening per gandalf open question #2?
   - **legolas** — 3 reads (00 / latest research request / cited docs within request). Tightest list — sufficient or under-scoped?

3. **Role-specific gaps.** Are there role-specific docs that should be added to any agent's first-reads that gandalf missed? Examples to consider:
   - Does **rocket** need `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` for asset-pipeline awareness (currently only in star-lord's list)?
   - Does **drax** need `canonical/story/style-register.md` for visual coherence (currently only in galadriel's list)?
   - Does **knight-rider** need `agentic_orchestration/REVIEW_PROCESS.md` in Phase-1 (currently named as session-start-read but not Phase-1 explicitly)?

4. **The five open questions in § 7.** Gandalf surfaces 5 open questions for you to resolve or defer:
   - Q1: Encode universal first-reads structurally per-agent or implicitly via working-agreement?
   - Q2: For drax, should "recent commits" be more specific (e.g., last 5)?
   - Q3: For star-lord, keep `19-llm-call-map.md` as permanent Phase-1 or only when task touches LLM calls?
   - Q4: Encode "consult on-demand" reading allowlist vs denylist, or trust agents to grep?
   - Q5: For knight-rider, clarify "latest skill_handoff" (most-recent-timestamp not most-recent-date-with-intra-day-variants)?

   Resolve each in your judgment, OR defer to Matt with reasoning. Each has a gandalf-recommended default in § 7.

5. **Risk-naming completeness (§ 5).** Gandalf names 5 risks with mitigations. Any risks missing? Specifically:
   - **Risk of false ground-state-oracle staleness.** If `00-ground-state.md` is the universal first-read and it goes stale between gandalf-maintained updates, every agent reads stale ground truth. What's the staleness-detection / retirement protocol?
   - **Risk of regression to pre-load.** Agents under context-pressure may default back to pre-loading the archive. Is Gate-1 enforcement adequate, or does this need a structural guard (e.g., a Phase-1-completion-statement the agent emits)?

6. **Aggregate-impact claim verification (§ 3).** Gandalf claims ~60-70% per-invocation read-budget reduction; ~3-5 hours per day reclaimed across team. Is the math reasonable? Spot-check 2-3 per-agent reductions for plausibility.

---

## Output format

Append a completion record to THIS dispatch file with structure:

**ARTIFACT 1 (math-seam-naming) — JUDGMENT:** BLOCK | PASS | PASS-WITH-AMENDMENTS
- 6 stress-test angles addressed
- Concrete amendments specified if PASS-WITH-AMENDMENTS

**ARTIFACT 2 (onboarding-list shrink) — JUDGMENT:** BLOCK | PASS | PASS-WITH-AMENDMENTS
- 6 stress-test angles addressed
- Concrete amendments specified if PASS-WITH-AMENDMENTS
- Per-agent table with PASS / PUSH-BACK / AMEND verdict

**Open-question resolutions:**
- 3 math-seam open questions (§ 6 of artifact 1) — concur / push back / surface alternative
- 5 onboarding-shrink open questions (§ 7 of artifact 2) — resolve or defer with reasoning

---

## Acceptance criteria

- [ ] Both artifacts addressed with separate judgments
- [ ] All stress-test angles answered per artifact (judgment per angle even if "no issues found")
- [ ] Concrete amendments specified if PASS-WITH-AMENDMENTS (with line / section / agent references)
- [ ] All 8 open questions resolved or explicitly deferred to Matt with reasoning
- [ ] Output committed as completion record appended to THIS dispatch file
- [ ] Round-trip: not applicable — Gate-1 critique only; no contract change
- [ ] Tag: `jack-ryan/gate-1-math-seam-onboarding-shrink-2026-05-23`

---

## Out of scope (explicit non-goals)

- **DO NOT** apply amendments to gandalf's source documents yourself — surface them; knight-rider applies on integration
- **DO NOT** integrate either artifact into AGENTS.md / engineering-disciplines.md / agent definitions / hive-mind-protocol docs — that's knight-rider's job after Gate-1 passes
- **DO NOT** modify or critique the Phase D dispatch (that work is complete; tag `jack-ryan/gate-1-phase-D-2026-05-23` already issued)
- **DO NOT** modify or critique `canonical/00-ground-state.md` or `canonical/38-downstream-delivery-strategy-2026-05-23.md` — both are gandalf-locked artifacts of the cleanup pass; in scope as referenced context only
- **DO NOT** re-open upstream design questions — the math-seam declaration is design-locked (Matt 2026-05-23 confirmed no dedicated mathematician agent); the onboarding-shrink rationale is locked (Matt 2026-05-23 approved cleanup pass); your scope is process-side review of the proposed integrations, not the underlying design calls

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` — artifact 1 under review
- `agentic_orchestration/gandalf/requests/2026-05-23-jack-ryan-onboarding-list-shrink.md` — artifact 2 under review
- `canonical/00-ground-state.md` — ground-state oracle (the universal first-read both artifacts anchor on)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — keystone delivery strategy (the universal second-read)
- `agentic_orchestration/AGENTS.md` — current agent definitions (target of math-seam Mathematical Layer insertion)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — current discipline numbering (target of #1.1 vs #18/20 insertion)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — target of math-hotspot annotations at P2/P3/P5
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — target of math-hotspot annotation at P5
- `agentic_orchestration/dispatches/2026-05-23-jack-ryan-gate-1-phase-D-dispatch.md` — first Pattern-B Gate-1 of this cleanup pass (template for completion-record format)
- ADR-001 (critique-pair pattern); ADR-006 (read-only by default)
- Discipline #1 (math-before-code); Discipline #2 (smoke-test); Discipline #4 (right tool); Discipline #11 (attribution / audit preservation); Discipline #14 (internal-vs-generative schema separation)

---

## What happens after you return

Knight-rider:
1. Reads your completion record per-artifact
2. If math-seam PASS / PASS-WITH-AMENDMENTS: integrates Mathematical Layer into `agentic_orchestration/AGENTS.md` + Discipline #1.1 (or alternative numbering per your amendment) into `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` + math-hotspot annotations into both hive-mind-protocol docs + cross-reference in `canonical/00-ground-state.md` Section 1
3. If onboarding-shrink PASS / PASS-WITH-AMENDMENTS: integrates per-agent Phase-1 read lists into agent definitions (Claude Code config) + cross-reference universal first-read in AGENTS.md
4. Commit granularity is knight-rider's call — either fold into a single working-agreement coherence commit, or split math-seam-integration from onboarding-shrink-integration if working-agreement signal is cleaner per separate commit
5. Surfaces to Matt: both artifacts Gate-1-approved, integrations landed, working-agreement coherent

---

**Signed:** knight-rider (dispatch authored 2026-05-23; second Pattern-B Gate-1 of cleanup-pass momentum continuation; Matt option (a) confirmed)
