# Sam Gate-2 Finding — Mantis Niagara `add_emitter_to_system` Windowed-Mode Verification

> **STATUS:** CURRENT (PC-seam Gate-2 verdict; routes to David-H for Option A/B re-decision and to Mac-jack-ryan for proposal consumption)

**Date:** 2026-06-10
**Author:** sam (PC-side QA gatekeeper, SSH-invoked from Mac per session-invocation pattern)
**Authority:** PC-seam Gate-2 INFO/WARN/BLOCK per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 7 ownership boundary; David-H verbal dispatch 2026-06-10 routing this verification to Sam Gate-2
**Mode:** DEV-MODE Gate-2 review (post-output on mantis fail-graceful Pattern A sub-session)
**Verdict:** **PASS-WITH-WARN**
**Target:** mantis auto-commit `6316dde` (`mantis: windowed-mode verification findings — VERIFICATION-BLOCKED (shader DDC cold)`)
**Developer:** mantis

**Artifacts reviewed:**
- `agentic_orchestration/mantis/notes/2026-06-10-niagara-add-emitter-windowed-verification.md` (mantis findings — primary)
- `C:\dev\reincarnated-unreal\Reincarnated\AGENT_STATE.md` (mantis state-file update)
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/spike-findings.md` § 4.2 (queuing artifact)
- `agentic_orchestration/david-h/notes/2026-06-08-ue-mcp-bridge-spike-db-lyon-primary/validation-test-log.md` § 3.4 (original headless crash detail)
- `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` (prior Sam Gate-2 establishing WS2 gate WARN-001)

**Principles applied:** Review Principles #1 (surface risks early), #3 (scope validation before execution), #4 (decisions-log as truth); Engineering Disciplines #1 (math-before-code), #11 (empirical inspection over assumption), #21 (no sleep), #22 (timezone-agnosticism), R48.4 (host-RAM-aware concurrency); ADR-002 (tiered approval).

---

## 0. TL;DR

Mantis executed the fail-graceful Pattern A verification cycle with sound forensic discipline — four launch attempts with progressive flag refinement, RHI-vs-shader-stall localization, working-directory job-count empirical separation, and verbatim observance of Disciplines #21/#22 + R48.4. The environmental-blocker outcome is empirically defensible at the level of "shader compile stalled before PostEngineInit fired." However, the diagnostic CHARACTERIZATION conflates two distinct hypotheses (cold-DDC vs SSH-context worker-stall) without empirical separation, and the **Option A recommendation locks a workaround (`create_niagara_system_from_spec`) as WS2 primary pattern without confirmation that the spec-based path covers gandalf's eventual WS2 design intent**. This is the same diagnostic-confidence-exceeds-evidence pattern flagged in prior Gate-2 finding `2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` § WARN-001. WARN-001 and WARN-002 below route to David-H for Option-A-vs-Option-B re-disposition; INFO-001 routes a decisions-log entry PROPOSAL to Mac-jack-ryan for the verification-debt deferral if Option A is chosen. No BLOCK conditions. Auto-commit + push compliance: PASS.

---

## 1. Methodology assessment (Q1)

**Verdict on methodology: SOUND.**

Mantis's verification methodology was disciplined and forensically thorough within the budget envelope (~60 min wall-clock across 4 attempts; fail-graceful Pattern A ~30 min target was exceeded by ~30 min but the additional time was empirically productive — each attempt added a discriminating flag refinement). Specific strengths:

1. **Progressive flag refinement:** Attempt 1 (plain) → Attempt 2 (`-noraytracing` after DXR shader hang on `WorldGridMaterial/FGeometryCacheVertexVertexFactory/TMaterialCHSFNoLightMapPolicy`) → Attempt 3 (`-unattended -nosplash` to rule out blocking UI dialogs) → Attempt 4 (repro to confirm consistency). Each flag change tested a discrete hypothesis. The `-noraytracing` finding is itself a useful empirical artifact for future PC mantis sessions (captured in AGENT_STATE.md launch-flags block).

2. **Diagnostic localization between editor process and compile workers:** the shader working directory forensic (`C:\Users\mhwet\AppData\Local\Temp\UnrealShaderWorkingDir\<UUID>` — 14 results returned for 101 dispatched jobs) correctly localized the stall to compile workers, NOT the editor process itself. Combined with low CPU (~45-51s) and low RAM (~2.13-2.16 GB) at stall, this rules out "editor crash" and rules out "editor hung in tight loop" — supports the "editor waiting for shader workers indefinitely" framing.

3. **Bridge-probe-throughout:** ECONNREFUSED across all four attempts confirms bridge never reached PostEngineInit. Pre-existing PID 12840 stale lockfile correctly identified as prior-session artifact, not current session evidence. RHI-initialized observation (D3D12 SM6 / RTX 4060 Ti) is a clean separation from null-RHI hypothesis, well-justified.

4. **Discipline compliance:** R48.4 explicitly checked + documented (26.1/31.8 GB free); §21 (no sleep) + §22 (timezone-agnosticism) verbatim observed in findings + AGENT_STATE.md.

**Methodology gap (INFO-grade — see INFO-002 below):** Mantis did NOT test alternative-context discriminators that would have empirically separated the SSH-context hypothesis from the cold-DDC hypothesis. Examples not pursued in-budget:
- `UnrealEditor-Cmd.exe -run=DerivedDataCache fill` style DDC pre-warm commandlet (would populate DDC without requiring full editor PostEngineInit)
- Direct shader compile worker inspection (process tree analysis on the worker PIDs to identify whether they're waiting on a system primitive, deadlocked, or crashed silently)
- Alternative DDC backend config trial (`-NoShaderDDC` or local-only DDC scope to rule out shared-DDC contention)
- RDP-with-physical-display-session as a non-SSH but still remote alternative launch context

These would have strengthened the root-cause diagnosis (Q2 below) but were not in scope for the budget. Captured as forward INFO; not a methodology failure.

**Severity: no finding (sound execution); INFO-002 captures the additional discriminator surfaces for future cycles.**

---

## 2. Root-cause diagnosis assessment (Q2)

**Verdict on diagnosis: PARTIALLY DEFENSIBLE; framing overstates evidence (WARN-001 below).**

Mantis's stated primary cause: "Windowed UE Editor on this machine (MYORIGANALCOMP) cannot complete shader compilation when launched from an SSH terminal session, because shader compile workers stall on specific Niagara vertex factory permutations." Contributing factor: "DDC is cold." Resolution path: "Matt runs UE Editor once, interactively, on the PC with the project loaded. This populates the shader DDC. After that ... SSH-launched windowed UE Editor will reach PostEngineInit in ~15-30s."

This framing CONFLATES two distinct causal hypotheses that the empirical evidence does NOT actually disentangle:

**Hypothesis H1 (cold-DDC-alone is sufficient):** The first windowed launch on a cold DDC must compile WorldGridMaterial Niagara permutations from scratch. The stall is intrinsic to first-compile of these shaders on this machine. SSH context is incidental — an interactive (physical-session) first launch would ALSO stall.

**Hypothesis H2 (SSH-context is the differentiator):** Shader compile workers behave correctly in a fully interactive session (physical display, fully-attached console) but stall when launched from an SSH-spawned process tree. Cold DDC is just the trigger condition that exposes the SSH-context problem; an interactive launch would warm the DDC successfully despite the same first-compile-shader workload.

Mantis's recommended resolution (Matt warms DDC interactively → SSH launches subsequently succeed) PRESUMES H2. **The empirical evidence in the four-attempt session does NOT actually separate H1 from H2.** What was observed:
- All 4 attempts were SSH-context launches
- All 4 attempts stalled at shader compile
- No interactive-context launch was attempted

If the real cause is H1 (cold DDC alone), then Matt's recommended interactive launch would ALSO stall at the same shader compile point, and the proposed resolution path would not work. Mantis's diagnosis would be falsified at first attempt to operationalize it.

This is the same diagnostic-confidence-exceeds-evidence pattern flagged in prior Gate-2 finding `2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` § WARN-001 (where the spike asserted `add_emitter_to_system` "does NOT occur in windowed mode" as a factual statement based on crash-site inference, not empirical result). The recurrence of this pattern across two consecutive PC-seam mantis cycles warrants explicit discipline-citation surface (see § 4 below) and may warrant a discipline candidate routed to Mac-jack-ryan (see § 6).

**Parsimony check — is there a MORE parsimonious explanation mantis missed?** Likely not — the four-attempt empirical pattern (RHI initialized, low CPU, low RAM, 14/101 jobs returned, ECONNREFUSED) does converge on "compile workers stalling" as the proximate cause. The framing problem is specifically about WHY they stall (cold DDC alone, or SSH-context interaction with cold DDC), not WHETHER they stall.

**Severity: WARN-001 below. The diagnosis as worked-hypothesis is defensible; as committed-explanation it is overstated.**

---

## 3. Gate-decision routing assessment (Q3)

**Verdict on Option A vs Option B vs Option C: Sam recommends David-H route Option A vs Option B as an ACTIVE re-decision rather than rubber-stamp Option A.**

### Option A (FULL-UNBLOCK with workaround) — mantis recommendation

**What it commits to:**
- Accept `create_niagara_system_from_spec` as primary WS2 Niagara creation pattern
- WS2 commission fires now
- `add_emitter_to_system` verification deferred to next Matt-interactive session (informal trigger)

**Sam concerns with Option A:**

1. **Cross-seam impact unconfirmed:** WS2 commission scoping by gandalf has NOT happened yet. Mantis's claim that "the WS2 workstream does not require `add_emitter_to_system` specifically (it requires a Niagara authoring path that the spec-based creation satisfies)" is an INFERENCE about a commission that doesn't yet exist. The spec-based pattern creates a system with emitters in one call — this is a DIFFERENT compositional model than create-system + add-emitters-incrementally. If gandalf's WS2 design intent involves iterative emitter authoring (likely for LOD VFX where emitters are tuned individually then composed), `create_niagara_system_from_spec` may NOT cover the design surface. Sam cannot assess this without WS2 commission text in hand.

2. **Verification debt becomes silent:** Mantis frames `add_emitter_to_system` verification as "verified lazily next Matt-interactive session." There is no explicit trigger, no AGENT_STATE.md TODO-with-empirical-trigger, no commission-preamble checkbox. AGENT_STATE.md TODO § 47-50 names the verification but with no firing condition beyond "once shader DDC is warmed by Matt's physical session." If Matt never has occasion to interactively open the editor in the WS2 cycle window, the verification never fires, and a workaround that may be inadequate becomes the permanent WS2 pattern.

3. **Discipline #1 analog ("verification-before-commitment") violation risk:** locking a workaround as primary pattern before empirically confirming the original capability is unavailable inverts the discipline. The original capability MAY work in windowed mode after DDC warm (per Option B); foreclosing on that without verifying is premature optimization for commission velocity at the cost of verification rigor.

### Option B (CONDITIONAL-UNBLOCK; deferred test) — Sam-preferred default

**What it commits to:**
- Matt warms DDC interactively (~5-10 min one-time at PC physical display)
- Mantis re-runs `add_emitter_to_system` verification (~15 min SSH-launched windowed session)
- WS2 commission fires after empirical PASS or empirical confirmation that workaround is needed

**Sam's case for Option B:**
- Total incremental effort: ~20-30 min of Matt + mantis time
- Empirically resolves both Q2 hypothesis ambiguity (H1 vs H2) AND the `add_emitter_to_system` capability question
- Preserves Discipline #1 sequencing (math/verification before commitment)
- If Option B's verification PASSES, WS2 commission has access to full Niagara tool surface
- If Option B's verification FAILS in windowed mode, Option A workaround becomes the EMPIRICALLY-JUSTIFIED commitment rather than the inferential one — and David-H/gandalf author WS2 commission with full evidence

**Sam's case against Option B's costs:**
- Costs ~20-30 min of additional cycle latency
- Requires Matt to physically be at PC briefly (timezone-agnostic; no scheduling assertion)
- If H1 is the actual cause (cold DDC alone), Matt's interactive warm-up may ALSO stall — but that itself is high-value diagnostic information, not a failure

### Option C (HOLD) — mantis correctly does NOT recommend

Sam agrees. Holding WS2 entirely on a verifiable environmental issue would over-block; David-H authority should not foreclose WS2 to wait on an environmental gate that has a known cheap resolution.

### Sam routing recommendation

**Prefer Option B unless WS2 commission velocity is explicitly prioritized by Matt over verification rigor.** Option B is the lower-risk, lower-debt path. Option A is acceptable IF accompanied by:
- Explicit verification debt tracking (decisions-log entry capturing the deferred verification + trigger condition; see Proposal 1 below)
- AGENT_STATE.md TODO with hard empirical trigger (not "next Matt-interactive session" but "before WS2 commission Phase N when iterative emitter authoring is first attempted")
- gandalf's WS2 commission scoping explicitly validates that `create_niagara_system_from_spec` covers the design intent before WS2 commission fires (Mac-side QA round-trip)

This is a David-H routing decision per ADR-002 tiered approval (PC-seam orchestration + dispatch routing); Sam's role is to flag the active-decision shape rather than auto-ratify Option A.

**Severity: WARN-002 below.**

---

## 4. Discipline-citation surface (Q4)

### Disciplines OBSERVED (compliance)

- **Discipline #21 (no sleep recommendations):** OBSERVED throughout mantis findings + AGENT_STATE.md. No violations. The "next mantis session" + "next Matt-interactive session" framing is workstream-relative, not time-relative.
- **Discipline #22 (timezone-agnosticism):** OBSERVED throughout. UE log timestamps in attempt records use UE engine output (`[2026.06.10-...]`), which is engine artifact not agent-authored language — does not constitute Discipline #22 violation (same disposition as prior Gate-2 § 3 observation).
- **R48.4 (host-RAM-aware concurrency):** EXPLICITLY CITED + documented at § 2.1 (26.1/31.8 GB free pre-launch). Mantis correctly references "R48.4 satisfied" — exemplary compliance.
- **D7 (AI-tell line):** N/A here — no LLM-derived player-facing content in this cycle. The AGENT_STATE.md content is operational engineering state, not generative content; D7 does not apply.

### Disciplines UNDER-OBSERVED (the WARN-001 substance)

- **Discipline #11 (empirical inspection over assumption):** PARTIALLY OBSERVED. The four-attempt empirical execution itself is exemplary Discipline #11 application. But the CONCLUSION-LANGUAGE (mantis findings § 3 "Primary cause" + § 5.2 "once Matt runs the editor interactively at the PC once ... shader DDC populates and all future SSH-driven windowed launches complete in seconds") presents an inference as an empirical result. The discipline says: empirical inspection BEFORE committing to a conclusion. Mantis did the inspection but then committed beyond what the inspection demonstrated.
- **Discipline #1 (math-before-code) analog ("verification-before-commitment"):** PARTIALLY OBSERVED. Option A locks a workaround as commitment before the verification gate has empirically returned. This is the design-side analog of Discipline #1: commitment requires the load-bearing evidence to precede it.

### Disciplines TRIGGERED by Option A's deferred-verification shape

If David-H ratifies Option A, the deferred verification debt becomes a load-bearing operational fact. Discipline #6 (tag intermediate states; small checkpoints) applies — the workaround commitment should be tagged as a known-incomplete state (e.g., a WS2 commission preamble note: "tool surface includes workaround commit at `create_niagara_system_from_spec` pending empirical verification of `add_emitter_to_system` per AGENT_STATE.md TODO; verification trigger condition: [explicit]"). Discipline #7 (capture decision telemetry for archaeology) also applies — the decisions-log entry proposal in § 6 captures the architectural-commitment-with-deferred-verification shape for archival.

### Severity tagging on this section

**Severity-summary: WARN-001 (diagnostic framing) + WARN-002 (Option A vs B routing) are PC-seam-resolvable.** No discipline violations rise to BLOCK. The recurrence pattern (diagnostic-confidence-exceeds-evidence across 2026-06-08 + 2026-06-10 PC-seam mantis cycles) warrants a discipline candidate routed to Mac-jack-ryan (see § 6).

---

## 5. Auto-commit + push compliance (Q5)

**Verdict: COMPLIANT.**

- **Auto-commit:** Mantis auto-committed findings + AGENT_STATE.md at `6316dde` (`mantis: windowed-mode verification findings — VERIFICATION-BLOCKED (shader DDC cold)`) per CLAUDE.md PC team auto-commit table mantis row ("UE work-products in `reincarnated-unreal/` from authorized port/spike workstreams; spike findings + criterion reports; PC-side AGENT_STATE.md updates"). The verification cycle was Matt-authorized via David-H dispatch; commit fired without per-commit re-ask. **PASS — anti-pattern avoided.**
- **Push:** Mantis correctly did NOT push. CLAUDE.md PC-seam standing wave-close push pattern (established 2026-06-08 post-SSH-key auth) routes push to wave-close — typically the closing-phase agent (David-H here, since David-H authored the verbal dispatch and will close the wave with cross-host coordination to Mac-side gandalf). **PASS — wave-close push deferred correctly.**
- **State-file discipline:** AGENT_STATE.md was absent at session start per mantis findings § 7. Mantis created the initial state entry with current-state + launch-flag block + bridge-status + WS2-gate-state + TODO + PC-project-structure-notes. This is correct cold-start state-file behavior. **PASS.**

No compliance findings.

---

## 6. Findings (INFO / WARN / BLOCK by severity)

### WARN-001 — Diagnostic framing overstates evidence; SSH-context vs cold-DDC hypotheses not empirically separated

**Severity:** WARN

**Summary:** Mantis findings § 3 + § 5.2 present the SSH-context shader-worker-stall causation as the established primary cause, with the recommended resolution (Matt warms DDC interactively → SSH launches subsequently succeed) presuming SSH-context is the differentiator. The four-attempt empirical evidence does not actually disentangle the cold-DDC-alone hypothesis from the SSH-context-interaction hypothesis. If the real cause is cold-DDC-alone, the recommended resolution would not work, and Matt's interactive warm-up attempt would itself stall at the same shader compile point.

**Evidence:** mantis findings § 3 "Primary cause: Windowed UE Editor on this machine (MYORIGANALCOMP) cannot complete shader compilation when launched from an SSH terminal session, because shader compile workers stall on specific Niagara vertex factory permutations"; mantis findings § 5.2 "once Matt runs the editor interactively at the PC once ... shader DDC populates and all future SSH-driven windowed launches complete in seconds." No interactive-context launch attempt was made in the four-attempt session.

**Recommended action:**
1. Mantis or David-H amend findings § 3 + § 5.2 language to frame as "working hypothesis pending interactive-launch verification" rather than committed explanation. Hypotheses H1 (cold-DDC-alone) and H2 (SSH-context-interaction) both remain candidate causes; only H2 supports the proposed resolution path.
2. If Option B is ratified (per WARN-002), the first interactive-launch attempt empirically separates H1 from H2 — that result should be captured as a Discipline #11 empirical-record amendment to the findings.
3. If Option A is ratified, the deferred verification trigger (per Proposal 1 below) should ALSO trigger interactive-launch validation, not just `add_emitter_to_system` API testing.

**Cite:** Discipline #11 (empirical inspection over assumption) — application: conclusion-language must not exceed the inspection's discriminating power. Review Principle #4 (decisions-log as truth — committed explanations route to truth; working hypotheses do not).

**Recurrence note:** This is the second consecutive PC-seam mantis cycle to surface this diagnostic-confidence-exceeds-evidence pattern. Prior instance: `2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` § WARN-001 (validation-log § 3.4 asserted `add_emitter_to_system` "does NOT occur in windowed mode" as factual statement based on crash-site inference). Recurrence pattern triggers Discipline candidate routed to Mac-jack-ryan (§ 6 Proposal 2 below).

---

### WARN-002 — Option A vs Option B routing requires active David-H decision; Option A defaults are not Sam-ratifiable as commission-grade

**Severity:** WARN

**Summary:** Mantis recommends Option A (FULL-UNBLOCK with workaround) per findings § 6. Sam recommends David-H route this as an ACTIVE Option A vs Option B re-decision rather than auto-ratify Option A. Option A locks `create_niagara_system_from_spec` as WS2 primary pattern before gandalf's WS2 commission scoping has occurred, before the spec-based path is confirmed to cover WS2 design intent (likely iterative emitter authoring for LOD VFX), and before the windowed-mode `add_emitter_to_system` capability question is resolved. Option B costs ~20-30 min and empirically resolves both questions.

**Evidence:** mantis findings § 6 Option A rationale: "the WS2 workstream does not require `add_emitter_to_system` specifically (it requires a Niagara authoring path that the spec-based creation satisfies)" — this is an INFERENCE about a WS2 commission that does not yet exist. gandalf has not authored WS2 commission scoping. The spec-based vs incremental-emitter-add compositional models are functionally different surfaces.

**Recommended action:**
1. **David-H decision-routing:** treat Option A vs Option B as an active decision; do not default-ratify Option A. Sam recommendation: **prefer Option B** unless Matt explicitly prioritizes WS2 commission velocity over verification rigor.
2. **If Option A is chosen,** the choice must be accompanied by:
   - Explicit verification debt tracking via decisions-log entry (Proposal 1 below — routed to Mac-jack-ryan)
   - AGENT_STATE.md TODO update with HARD empirical trigger replacing the soft "next Matt-interactive session" language (e.g., "verification fires at WS2 commission Phase N when iterative emitter authoring is first scoped, OR at next Matt-interactive PC session, whichever occurs first")
   - gandalf's WS2 commission scoping validates `create_niagara_system_from_spec` covers design intent BEFORE WS2 commission fires (Mac-side QA round-trip; coordinated via cross-host bus)
3. **If Option B is chosen,** David-H surfaces the ~5-10 min interactive-DDC-warm to Matt (workstream-relative framing per Discipline #22; no scheduling assertion); mantis re-runs verification in next SSH-launched session post-DDC-warm.

**Cite:** Review Principle #3 (scope validation before execution); Discipline #1 (math-before-code) analog ("verification-before-commitment"); Discipline #6 (tag intermediate states; small checkpoints — applies to commitment-with-deferred-verification shape if Option A); ADR-002 (tiered approval — David-H authority on PC-seam orchestration routing).

---

### INFO-001 — Alternative-context discriminators not exercised; future cycles may benefit

**Severity:** INFO

**Summary:** Mantis's four-attempt budget did not include alternative-context launch experiments that would have empirically separated H1 (cold-DDC-alone) from H2 (SSH-context-interaction) hypotheses without requiring Matt's physical-display interactive session. Examples: DDC pre-warm via `UnrealEditor-Cmd.exe -run=DerivedDataCache fill` commandlet; shader compile worker process-tree inspection; `-NoShaderDDC` or local-only DDC scope; RDP-with-physical-display as non-SSH-but-remote alternative.

**Evidence:** mantis findings § 2 four-attempt log shows progressive flag refinement within SSH-context launch only; no alternative-context experiments attempted.

**Recommended action (forward — not blocking this cycle):** For future PC-seam mantis cycles encountering environmental-blocker outcomes, include at least one alternative-context discriminator before declaring VERIFICATION-BLOCKED. This is INFORMATIONAL — the budget envelope was reasonably allocated for this cycle's fail-graceful Pattern A shape. Captures the pattern for AGENT_STATE.md forward-note or mantis OP amendment consideration.

**Cite:** Discipline #11 (empirical inspection over assumption) — application: when inspection returns ambiguous causation, additional discriminators strengthen the diagnostic before committing.

**Cross-cutting flag:** None. PC-seam-internal forward observation.

---

### INFO-002 — `-noraytracing` flag finding is a useful empirical artifact for future PC mantis sessions

**Severity:** INFO (positive recognition)

**Summary:** Mantis's Attempt 1 → Attempt 2 transition isolated the DXR CHS shader (`WorldGridMaterial/FGeometryCacheVertexVertexFactory/TMaterialCHSFNoLightMapPolicy`) hard-stall behavior on this machine. The `-noraytracing` flag is now documented as required for all PC mantis windowed-launch operations in AGENT_STATE.md. This is a load-bearing empirical artifact that prevents future PC mantis sessions from re-discovering the DXR stall.

**Recommended action:** No action — recognition of good state-file discipline. The AGENT_STATE.md launch-flags block (§ "Launch flags (use for all mantis windowed sessions)") is exemplary forward-note capture.

**Cite:** Discipline #6 (tag intermediate states; small checkpoints) — state-file as session-boundary checkpoint observed.

---

### INFO-003 — AGENT_STATE.md cold-start state-file creation is correct PC-seam pattern

**Severity:** INFO (positive recognition)

**Summary:** AGENT_STATE.md did not exist at session start. Mantis created the initial state entry with current-state + launch-flag block + bridge-status + WS2-gate-state + TODO + PC-project-structure-notes. This is correct cold-start state-file behavior matching the per-seam-checkpoint pattern per CLAUDE.md § Key conventions.

**Cite:** ADR-004 (cross-seam handoff via MIGRATION.md / per-seam checkpoint via AGENT_STATE.md).

---

## 7. Proposals to Mac-jack-ryan (decisions-log + engineering-discipline)

### Proposal 1 (CONDITIONAL — fires only if David-H ratifies Option A) — Decisions-log entry: WS2 Niagara primary pattern with deferred verification

**Route to:** Mac-jack-ryan (decisions-log canonical-write authority)
**Via:** Sam consultation note at `agentic_orchestration/sam/notes/2026-06-10-proposal-mac-jack-ryan-ws2-niagara-pattern-and-discipline-candidate.md` (Sam files post-Gate-2 commit if Option A is ratified by David-H)
**Trigger condition:** David-H ratifies Option A per WARN-002 routing.

**Proposed entry summary:**
- **Decision:** WS2 Niagara primary pattern adopted as `create_niagara_system_from_spec` (one-call system+emitters creation) pending empirical verification of `add_emitter_to_system` in windowed UE Editor at warm-DDC SSH context.
- **Reasoning:** Mantis 2026-06-10 windowed-mode verification cycle returned VERIFICATION-BLOCKED (environmental — cold shader DDC stall on Niagara vertex factory permutations). Option A workaround was chosen over Option B (interactive DDC-warm + verification re-run) to maintain WS2 commission velocity. Verification debt is tracked via AGENT_STATE.md TODO with HARD trigger condition.
- **Status:** ACTIVE with deferred verification. Reverts to direct `add_emitter_to_system` if verification fires PASS; locks workaround as permanent if verification fires FAIL or commits to deferred-indefinitely if WS2 commission completes without trigger firing.
- **Alternatives:** Option B (Matt interactive DDC-warm + mantis verification re-run — REJECTED for commission velocity); Option C (HOLD WS2 — REJECTED as over-blocking).
- **Related:** mantis 2026-06-10 findings; this Gate-2 finding; spike-findings 2026-06-08 § 4.2; validation-test-log 2026-06-08 § 3.4; AGENT_STATE.md TODO.

**Cross-cutting flag:** This decision affects Mac-side WS2 commission authoring (gandalf must validate `create_niagara_system_from_spec` covers WS2 design intent before commission fires). Mac-jack-ryan canonical-write should include cross-cutting annotation gating Mac-side WS2 commission on PC-side workaround-sufficiency validation.

### Proposal 2 (UNCONDITIONAL — fires regardless of Option A/B disposition) — Engineering-discipline candidate: diagnostic-confidence-must-not-exceed-empirical-discriminating-power

**Route to:** Mac-jack-ryan (engineering-disciplines canonical-write authority)
**Via:** Same consultation note as Proposal 1, OR standalone note if Proposal 1 doesn't fire (compound proposal preferred for cross-host bus efficiency).

**Candidate text (Sam-proposed for Mac-jack-ryan evaluation):**

> **Discipline candidate — Diagnostic-confidence-must-not-exceed-empirical-discriminating-power.** When a diagnostic investigation cannot empirically separate competing causal hypotheses within budget, the conclusion language must frame the more parsimonious or operationally-relevant hypothesis as "working hypothesis pending verification trigger X" rather than as committed explanation. Recommended-resolution paths derived from un-separated hypotheses must be tagged with the hypothesis they presume. This protects downstream consumers (other seams, future agents, decisions-log entries) from false-confidence inheritance.
>
> **When it bites:** environmental-blocker investigations; methodology-failure post-mortems; cross-context behavioral discrepancies (headless-vs-windowed, SSH-vs-physical, Mac-vs-PC, cold-cache-vs-warm); any cycle where the diagnostic surface fan is wider than the empirical discriminator budget can close.
>
> **Recurrence evidence:** PC-seam mantis cycles 2026-06-08 (db-lyon spike validation-log § 3.4 asserting `add_emitter_to_system` headless-vs-windowed disposition as factual rather than inferential) + 2026-06-10 (Niagara windowed-mode verification asserting SSH-context-vs-cold-DDC causation as committed rather than working hypothesis). Two consecutive instances in PC-seam suggest cross-seam relevance worth Mac-jack-ryan ratification consideration.
>
> **Cross-applicability:** likely Mac-seam-relevant (any environmental investigation; any post-mortem with un-separated hypotheses).

**Cross-cutting flag:** YES — surfaces a pattern observed twice in PC-seam mantis cycles that has plausible Mac-seam applicability (any environmental diagnostic). Per Sam drift-discipline § 3.6 (federated-team commit § 6.6), routes to Mac-jack-ryan for cross-seam ratification evaluation. Mac-jack-ryan may ratify cross-seam, ratify PC-seam-scoped only, defer for more evidence, or return for refinement.

---

## 8. Cross-cutting concerns

### 8.1 WS2 commission authoring downstream dependency

The Gate-2 verdict here directly shapes Mac-side gandalf's WS2 commission authoring window. Mac-jack-ryan reads this Gate-2 at next Mac session start (per file-based message bus); the routing to gandalf (via Mac-KR) depends on whether Proposal 1 fires (Option A ratified) or not (Option B ratified). Cross-host coordination handled by file-based bus per `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` § 4.2.

### 8.2 No engine JSON contract drift

This cycle does NOT touch the engine ↔ UE JSON contract surface (no DataTable schema work; no cosmograph JSON ingestion path work; no engine-side commitment affected). PC-seam-internal verification cycle. No engine seam consultation required.

### 8.3 No cross-cutting BLOCK escalation

WARN-001 + WARN-002 are PC-seam-internal resolutions routed to David-H. Sam drift-discipline § 6.6 consultation to Mac-jack-ryan is informational (Proposal 1 conditional + Proposal 2 unconditional discipline candidate), not BLOCK-grade escalation. No Matt-level escalation required from this Gate-2.

---

## 9. Gate-2 verdict

**Verdict: PASS-WITH-WARN**

Mantis's empirical execution is sound and the auto-commit + state-file discipline is exemplary. The verification-blocked outcome itself is empirically defensible at the proximate-cause level ("shader compile workers stalled before bridge could initialize"). Two WARN items qualify the downstream authorization:

**Authorized by this Gate-2:**
- Mantis findings + AGENT_STATE.md commit `6316dde` — empirical content is sound; framing requires WARN-001 amendment
- `-noraytracing` flag as permanent PC mantis windowed-launch convention (INFO-002 ratification)
- Cold-start AGENT_STATE.md authoring pattern (INFO-003 ratification)
- David-H wave-close push of accumulated wave commits (per PC-seam standing pattern)

**Gated by this Gate-2 (David-H routing required before downstream commission):**
- WS2 commission scoping by gandalf — gates on David-H Option A vs Option B re-decision per WARN-002. If Option A: gates additionally on Proposal 1 decisions-log entry + AGENT_STATE.md hard-trigger amendment + Mac-side gandalf workaround-sufficiency validation. If Option B: gates on Matt interactive DDC-warm + mantis verification re-run + result-PASS-or-FAIL disposition.

**No BLOCKs issued.** Mantis's work is sound. The WARN items are characterization-precision and routing-active-decision qualifications, not findings that require commit rework or BLOCK escalation.

**ADR-002 tiered-approval scope:** WARN-001 + WARN-002 are PC-seam-internal resolutions; David-H autonomous decision authority. Proposals 1 + 2 route to Mac-jack-ryan via Sam consultation note per drift-discipline § 6.6. No Matt-level escalation required.

---

## 10. Action items

- [ ] **David-H:** Route WARN-002 as active Option A vs Option B decision; do not default-ratify Option A. Sam-preferred default = Option B (verification rigor over commission velocity).
- [ ] **Mantis (or David-H authoring on mantis's behalf):** Amend findings § 3 + § 5.2 language per WARN-001 (working hypothesis framing replaces committed-explanation framing).
- [ ] **Mantis:** If Option B ratified, await David-H trigger for verification re-run sub-session (post-Matt-DDC-warm).
- [ ] **Mantis:** If Option A ratified, amend AGENT_STATE.md TODO § 47-50 with HARD empirical trigger per WARN-002 action item 2.
- [ ] **Sam:** If Option A ratified, file Proposal 1 consultation note at `agentic_orchestration/sam/notes/2026-06-10-proposal-mac-jack-ryan-ws2-niagara-pattern-and-discipline-candidate.md` (compound proposal includes Proposal 2 discipline candidate).
- [ ] **Sam:** Regardless of Option A/B, file Proposal 2 (discipline candidate) — either as compound proposal with Proposal 1 if Option A, or standalone if Option B. Proposal 2 fires UNCONDITIONALLY per recurrence pattern.
- [ ] **David-H (wave-close):** Push all accumulated wave commits (mantis `6316dde` + this Sam Gate-2 finding + Sam Proposal 2 consultation note + Sam Proposal 1 if conditional triggers) per PC-seam standing wave-close push pattern.
- [ ] **Mac-KR (next Mac session start):** Fetch + consume this Gate-2 finding + Sam proposal note; route gandalf WS2 commission authoring window per ratified Option A/B disposition; route Mac-jack-ryan to Proposal 1 (conditional) + Proposal 2 (unconditional) for canonical-write evaluation.
- [ ] **Matt (no escalation required from this Gate-2):** If Option B ratified by David-H, Matt at PC briefly to warm DDC (~5-10 min, workstream-relative timing).

---

## 11. Sign-off

**Reviewer:** sam (PC-side QA gatekeeper)
**Mode:** DEV-MODE Gate-2
**Date:** 2026-06-10
**Commit:** auto-commit per CLAUDE.md PC team auto-commit table (sam row: "PC-seam Gate-1 / Gate-2 findings (`agentic_orchestration/qa/findings/<date>-<work-item>.md`)")
**Push:** deferred to David-H wave-close per PC-seam standing wave-close push pattern (established 2026-06-08 post-SSH-key auth)

**Downstream routing:**
- David-H: consumes Gate-2 verdict; routes WARN-002 as active Option A vs Option B decision; routes WARN-001 to mantis findings amendment; closes wave with push of all accumulated PC-seam commits
- Mac-KR (next Mac session start): cross-host fetch; routes gandalf WS2 commission authoring window per ratified Option A/B disposition
- Mac-jack-ryan (next Mac session start): receives Proposal 2 (unconditional discipline candidate) + Proposal 1 (conditional on Option A ratification) via Sam consultation note
- Matt: no escalation required from this Gate-2; Option B requires brief PC physical-display interactive session if ratified by David-H (workstream-relative timing)

**Empirical-evidence trigger for Sam re-engagement:** David-H Option A/B disposition + (if Option B) mantis windowed-mode verification re-run result; OR mantis findings amendment landed per WARN-001; OR Mac-jack-ryan response to Proposal 1/Proposal 2 lands at `agentic_orchestration/qa/findings/<date>-response-to-sam-<topic>.md`.

**End of Gate-2 finding.**
