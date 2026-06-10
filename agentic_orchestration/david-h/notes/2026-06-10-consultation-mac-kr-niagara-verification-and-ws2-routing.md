# Cross-Host Consultation — Mac-KR + gandalf — Niagara Verification VERIFICATION-BLOCKED + WS2 Commission Routing Decision Surface

> **STATUS:** CURRENT (cross-host consultation surface; Mac-KR fetches at next Mac session start; routes Matt + gandalf for Option A vs Option B WS2 commission decision)

**Date:** 2026-06-10
**Author:** david-h (PC-side orchestrator)
**Authority:** PC-seam Mode D cross-host coordination per OP § 4.1; federated-team commit § 4.2 file-based message bus
**Target:** Mac-KR (cross-host fetch + routing); gandalf (WS2 commission authoring window + design-intent input); Mac-jack-ryan (Sam Proposal 2 standalone discipline-candidate intake + conditional Proposal 1 standby); Matt (Option A vs Option B routing)
**Wave context:** `agentic_orchestration/david-h/notes/2026-06-10-niagara-windowed-verification-wave-close.md` (companion wave-close memo with full PC-side wave state)

---

## 0. TL;DR for Mac-side consumption

**PC-seam Niagara `add_emitter_to_system` windowed-mode verification gate returned PASS-WITH-WARN (Sam Gate-2), with the underlying mantis verification VERIFICATION-BLOCKED (environmental — cold shader DDC stall; bridge never reached PostEngineInit; API never invoked).**

**WS2 commission routing requires an active Option A vs Option B decision** at Matt + gandalf scope. **David-H deliberately did NOT unilaterally ratify** because both options have cross-cutting + Matt-action dimensions outside unilateral PC-seam authority.

**Sam-preferred default: Option B** (Matt warms DDC ~5-10 min + mantis re-runs ~15 min; ~20-30 min total; empirically resolves both diagnostic ambiguity AND capability question). **Mantis-preferred: Option A** (FULL-UNBLOCK with `create_niagara_system_from_spec` workaround; WS2 commission fires now; capability verified lazily). David-H neutral pending Matt + gandalf input — see § 3 trade-off matrix.

**Also intake at next Mac session:** Sam Proposal 2 standalone consultation note (discipline candidate — diagnostic-confidence-must-not-exceed-empirical-discriminating-power; recurrence-evidence-based; routes to Mac-jack-ryan for engineering-disciplines canonical-write evaluation). Sam Proposal 1 (decisions-log entry; conditional on Option A ratification) on standby.

---

## 1. PC-seam wave artifacts for Mac-side fetch (manifest)

| Artifact | Path | Author | Purpose for Mac-side consumption |
|---|---|---|---|
| Wave-close memo | `agentic_orchestration/david-h/notes/2026-06-10-niagara-windowed-verification-wave-close.md` | david-h | Full PC-side wave state + tmux deferred infrastructure note + WARN-001/002 disposition |
| This consultation memo | `agentic_orchestration/david-h/notes/2026-06-10-consultation-mac-kr-niagara-verification-and-ws2-routing.md` | david-h | THIS DOC — WS2 routing decision surface for Matt + gandalf |
| Sam Gate-2 finding | `agentic_orchestration/qa/findings/2026-06-10-mantis-niagara-windowed-verification-gate-2.md` | sam | Empirical + discipline assessment; WARN-001 + WARN-002 detail; Proposal 1 + 2 source text |
| Sam Proposal 2 standalone | `agentic_orchestration/sam/notes/2026-06-10-proposal-mac-jack-ryan-discipline-candidate-diagnostic-confidence.md` | sam (queued — final wave action) | Engineering-discipline candidate routed to Mac-jack-ryan; consumed at next Mac session |
| Mantis findings | `agentic_orchestration/mantis/notes/2026-06-10-niagara-add-emitter-windowed-verification.md` | mantis | Raw empirical record — 4 launch attempts, RHI-vs-compile-worker stall localization, shader-working-directory forensic |
| Mantis AGENT_STATE.md | `C:\dev\reincarnated-unreal\Reincarnated\AGENT_STATE.md` | mantis | PC-seam state-file (cold-start initial entry; includes launch-flag block + bridge status + WS2 gate state + TODO + PC project structure notes) |

---

## 2. Empirical record summary (for gandalf design-intent input)

### 2.1 What was attempted

Mantis launched windowed UE Editor 4 times with progressive flag refinement:
- Attempt 1: plain (`Reincarnated.uproject -stdout -FullStdOutLogOutput`)
- Attempt 2: `+ -noraytracing` (after DXR CHS shader hang on `WorldGridMaterial/FGeometryCacheVertexVertexFactory`)
- Attempt 3: `+ -unattended -nosplash`
- Attempt 4: repro confirmation

### 2.2 What was observed (across all 4 attempts)

- D3D12 SM6 RHI initialized successfully (RTX 4060 Ti)
- Shader compile dispatched 101-153 jobs; ~14 returned to working directory; remainder stalled indefinitely
- Editor process alive (~45-51s CPU, ~2.13-2.16 GB RAM — low; not a tight loop or crash)
- Bridge port 9877: ECONNREFUSED throughout — PostEngineInit callback never fired
- `add_emitter_to_system` API call NEVER reached (could not test)

### 2.3 Root-cause framing (Sam WARN-001 — characterization caveat)

Mantis frames cause as "SSH-context shader compile worker stall + cold DDC trigger." Sam WARN-001 notes this conflates two hypotheses without empirical separation:
- **H1 (cold-DDC-alone):** first windowed launch must compile WorldGridMaterial Niagara permutations from scratch; stall intrinsic to first-compile regardless of context
- **H2 (SSH-context-interaction):** workers stall specifically when launched from SSH process tree; physical interactive launch would NOT stall

Mantis's recommended resolution (Matt warms DDC interactively → subsequent SSH launches succeed) PRESUMES H2. If H1 is the actual cause, Matt's warm-up would ALSO stall.

**Note for gandalf:** the diagnostic ambiguity is itself relevant to WS2 commission scoping — if H1 is correct, ALL mantis windowed-editor work in WS2 may require a hands-on warm-up cycle from Matt before each cold-DDC scenario, not just the `add_emitter_to_system` verification. Option B's first interactive-launch attempt would discriminate H1 from H2 as a side-effect.

### 2.4 What was empirically established (independent of H1/H2)

- `-noraytracing` is REQUIRED for windowed launch on this PC (DXR CHS hard-stall otherwise) — documented in AGENT_STATE.md launch-flags block as standing PC mantis convention
- Headless mode `-nullrhi` skipped these shaders entirely (per 2026-06-08 spike); the `add_emitter_to_system` crash there was at `NiagaraHandlers.cpp:595` (likely null-RHI precondition)
- Bridge plugin source compiles correctly; bridge port lockfile reflects last successful initialization (from 2026-06-09 prior session)

---

## 3. Routing decision surface — Option A vs Option B trade-off matrix (for Matt + gandalf)

### 3.1 Option A — FULL-UNBLOCK with workaround (mantis recommendation)

| Dimension | Position |
|---|---|
| **What commits** | Accept `create_niagara_system_from_spec` as primary WS2 Niagara creation pattern; WS2 commission fires now; `add_emitter_to_system` verification deferred to next Matt-interactive PC session (informal trigger) OR HARD trigger per Sam Proposal 1 amendment |
| **Cost** | 0 incremental wall-clock; 0 Matt action this cycle |
| **Velocity** | WS2 commission can fire at next Mac session immediately |
| **Verification debt** | Yes — `add_emitter_to_system` capability remains empirically unverified in windowed mode; deferred to Matt's next interactive PC session; if Matt never has interactive session in WS2 cycle window, the workaround becomes permanent without evidence |
| **Cross-seam risk** | Workaround compositional model (`create_niagara_system_from_spec` = one-call system+emitters) is FUNCTIONALLY DIFFERENT from incremental emitter-add (likely needed for LOD VFX iterative authoring). gandalf evaluates whether spec-based path covers WS2 design intent BEFORE WS2 commission fires |
| **Sam stance** | Acceptable only if accompanied by Proposal 1 decisions-log entry + AGENT_STATE.md HARD empirical trigger + gandalf cross-host workaround-sufficiency validation |
| **Diagnostic ambiguity** | Persists — H1 vs H2 hypothesis question is not resolved; future PC-seam env-block incidents will inherit the same ambiguity |

### 3.2 Option B — CONDITIONAL-UNBLOCK with verification re-run (Sam recommendation)

| Dimension | Position |
|---|---|
| **What commits** | Matt warms DDC interactively at PC (~5-10 min one-time); mantis re-runs `add_emitter_to_system` verification (~15 min SSH-launched windowed session); WS2 commission fires after empirical PASS or empirical confirmation that workaround is needed |
| **Cost** | ~20-30 min Matt + mantis time total |
| **Velocity** | WS2 commission fires after one PC interactive session + one mantis sub-cycle (~next 1-2 PC sessions) |
| **Verification debt** | None — `add_emitter_to_system` either PASSes empirically (full Niagara tool surface available for WS2) OR FAILs empirically (workaround becomes EMPIRICALLY-JUSTIFIED commitment with full evidence) |
| **Cross-seam risk** | Lower — gandalf authors WS2 commission with full Niagara capability map; no inferential lock-in |
| **Sam stance** | Preferred default — verification rigor over commission velocity; preserves Discipline #1 analog (verification-before-commitment) sequencing |
| **Diagnostic ambiguity** | Resolved — Matt's interactive launch either succeeds (H2 confirmed; SSH-context is the differentiator) or stalls (H1 confirmed; cold-DDC-alone is sufficient; need DDC pre-warm commandlet or alternative approach for ALL future PC-seam windowed-editor work) |

### 3.3 Option C — HOLD WS2 commission entirely

Mantis correctly does NOT recommend. Sam agrees. Holding WS2 entirely on an environmental issue with cheap known resolution is over-blocking.

### 3.4 David-H neutral framing for Matt + gandalf co-decision

**David-H does not have a preference between Option A and Option B.** The trade-off is:
- Option A optimizes for commission velocity at the cost of deferred verification debt + cross-seam-risk if workaround doesn't cover gandalf's design intent
- Option B optimizes for verification rigor at the cost of ~20-30 min latency + Matt physical action

Both are defensible. Sam recommends Option B; mantis recommends Option A. The decision depends on:
1. **gandalf's WS2 design intent** — does iterative emitter authoring (likely for LOD VFX or runtime emitter tuning) feature in the commission? If yes, `add_emitter_to_system` matters → Option B preserves capability. If no, spec-based pattern suffices → Option A is cheaper
2. **Matt's PC-availability window** — Option B's ~5-10 min interactive session is workstream-relative (no scheduling assertion); if Matt has occasion at PC in the WS2 cycle window, Option B's cost is minimal. If Matt prefers Mac-only Mac-session work for the WS2 cycle, Option A may align better
3. **PC-seam diagnostic-confidence-baseline** — if Sam Proposal 2 (§ 4.2) is ratified by Mac-jack-ryan, the discipline pressure toward Option B intensifies (Option B aligns with new discipline; Option A inherits the diagnostic-confidence-exceeds-evidence pattern Proposal 2 targets)

---

## 4. Sam Proposals routing (for Mac-jack-ryan intake)

### 4.1 Proposal 1 (CONDITIONAL — fires only if Option A ratified)

**Type:** decisions-log entry
**Route:** Mac-jack-ryan canonical-write authority (Sam files consultation note post-Option-A-ratification at PC-side)
**Trigger:** Matt routes Option A at next Mac session

**Proposed entry content** (Sam-drafted in Gate-2 § 7 Proposal 1):
- **Decision:** WS2 Niagara primary pattern adopted as `create_niagara_system_from_spec` pending empirical verification of `add_emitter_to_system` in windowed UE Editor at warm-DDC SSH context
- **Reasoning:** Mantis 2026-06-10 windowed-mode verification cycle returned VERIFICATION-BLOCKED (environmental); Option A workaround chosen over Option B for WS2 commission velocity; verification debt tracked via AGENT_STATE.md TODO with HARD trigger condition
- **Status:** ACTIVE with deferred verification; reverts to direct `add_emitter_to_system` if verification fires PASS; locks workaround if verification fires FAIL or commits to deferred-indefinitely if WS2 commission completes without trigger firing
- **Alternatives:** Option B (REJECTED for commission velocity); Option C (REJECTED as over-blocking)
- **Related:** mantis 2026-06-10 findings; Sam Gate-2 2026-06-10; spike-findings 2026-06-08 § 4.2; AGENT_STATE.md TODO; this consultation memo
- **Cross-cutting flag:** YES — affects Mac-side WS2 commission authoring; gandalf must validate `create_niagara_system_from_spec` covers WS2 design intent before commission fires

### 4.2 Proposal 2 (UNCONDITIONAL — fires regardless of Option A/B)

**Type:** engineering-discipline candidate
**Route:** Mac-jack-ryan canonical-write authority (Sam files standalone consultation note as next sub-agent invocation in this wave OR defers to next Sam session)
**Trigger:** unconditional per Sam Gate-2 § 6 Proposal 2 (recurrence-evidence-based)

**Candidate text** (Sam-drafted; for Mac-jack-ryan evaluation):

> **Discipline candidate — Diagnostic-confidence-must-not-exceed-empirical-discriminating-power.** When a diagnostic investigation cannot empirically separate competing causal hypotheses within budget, the conclusion language must frame the more parsimonious or operationally-relevant hypothesis as "working hypothesis pending verification trigger X" rather than as committed explanation. Recommended-resolution paths derived from un-separated hypotheses must be tagged with the hypothesis they presume. This protects downstream consumers (other seams, future agents, decisions-log entries) from false-confidence inheritance.
>
> **When it bites:** environmental-blocker investigations; methodology-failure post-mortems; cross-context behavioral discrepancies (headless-vs-windowed, SSH-vs-physical, Mac-vs-PC, cold-cache-vs-warm); any cycle where the diagnostic surface fan is wider than the empirical discriminator budget can close.
>
> **Recurrence evidence:** PC-seam mantis cycles 2026-06-08 (db-lyon spike validation-log § 3.4 — `add_emitter_to_system` headless-vs-windowed disposition asserted as factual) + 2026-06-10 (Niagara windowed-mode verification — SSH-context-vs-cold-DDC causation asserted as committed). Two consecutive PC-seam instances; plausible Mac-seam applicability.
>
> **Cross-applicability:** likely Mac-seam-relevant (any environmental investigation; any post-mortem with un-separated hypotheses).

**Mac-jack-ryan disposition options:**
- Ratify cross-seam (Mac + PC engineering-disciplines canonical-write)
- Ratify PC-seam-scoped only (carry as PC-side discipline; revisit if Mac-seam evidence emerges)
- Defer for more evidence (await next env-block / post-mortem cycle)
- Return for refinement (request specific language amendments)

---

## 5. PC-seam wave-close push status

Wave-close push fires at this consultation memo + Sam Proposal 2 standalone landing. Per CLAUDE.md § "PC-seam standing wave-close push pattern (established 2026-06-08 post-SSH-key auth)" — the wave-close gate IS the authorization moment; no per-push re-ask required.

**Wave commits being pushed:**
1. `6316dde` mantis: windowed-mode verification findings — VERIFICATION-BLOCKED (shader DDC cold)
2. `631cdda` sam: Gate-2 PASS-WITH-WARN — mantis Niagara add_emitter_to_system windowed verification
3. (pending) david-h: wave-close memo + this consultation memo (single commit per OP § 5 single-commit-per-scope pattern)
4. (pending) sam: Proposal 2 standalone consultation note

If Sam Proposal 2 is deferred to next Sam session, David-H wave-close push fires with commits 1-3 only; Sam Proposal 2 commits + pushes at next Sam session start independently.

---

## 6. Mac-side action items at next Mac session start (sequenced)

| # | Owner | Action |
|---|---|---|
| 1 | Mac-KR | Fetch (`git pull`) — captures full wave manifest per § 1 |
| 2 | Mac-KR | Consume this consultation memo + companion wave-close memo |
| 3 | gandalf | Read mantis findings + Sam Gate-2 + this memo § 2 + § 3; evaluate WS2 design intent against Option A spec-based workaround vs Option B preserved direct `add_emitter_to_system` capability |
| 4 | Mac-KR | Route to Matt with gandalf's design-intent input + § 3.4 trade-off framing |
| 5 | Matt | Route Option A vs Option B with full information |
| 6a | (if Option A) gandalf | Validate `create_niagara_system_from_spec` covers WS2 commission design intent BEFORE WS2 commission fires; this gates WS2 commission landing |
| 6b | (if Option A) Sam (via PC re-engagement) | Files Proposal 1 standalone consultation note to Mac-jack-ryan |
| 6c | (if Option A) Mac-jack-ryan | Canonical-writes decisions-log entry per Proposal 1 |
| 6d | (if Option A) David-H | Routes mantis at next PC session for AGENT_STATE.md TODO HARD-trigger amendment |
| 7a | (if Option B) Matt at PC | ~5-10 min interactive editor session to warm shader DDC |
| 7b | (if Option B) David-H | Routes mantis at next PC session for verification re-run (~15 min) |
| 7c | (if Option B) Mantis | Re-runs verification; result-PASS-or-FAIL captured in amended findings document; AGENT_STATE.md updated; Sam Gate-2 re-fires on amended result |
| 8 | Mac-jack-ryan | Intakes Sam Proposal 2 standalone (UNCONDITIONAL); evaluates engineering-disciplines canonical-write per dispositions in § 4.2 |
| 9 | gandalf | Once Option A/B resolved + (if Option B) verification re-run completes, authors WS2 commission with full empirical context |

---

## 7. Empirical-evidence triggers for cross-host re-engagement

### 7.1 Trigger for Mac-KR cross-host fetch

Next Mac session start — per established federated-team commit § 4 file-based message bus protocol; Mac-KR session-start pulls origin + fetches PC-side consultation notes addressed to Mac team.

### 7.2 Trigger for PC-side David-H re-engagement

Matt's Option A vs Option B ratification — David-H fires next PC session at the empirical-evidence trigger of "Matt routes A or B and commits / pushes the decision to origin/main." David-H session-start pull captures the routing; David-H executes ratified path.

### 7.3 Trigger for cross-host loop close

WS2 commission lands at Mac side AND mantis WS2 execution proceeds at PC side without further routing escalations.

---

## 8. Sign-off

**Authored:** david-h 2026-06-10 per OP § 4.1 Mode D cross-host consultation pattern + Path A Matt authorization to surface cross-cutting routing decisions via file-based message bus.

**Routing target:** Mac-KR + gandalf + Mac-jack-ryan + Matt at next Mac session start.

**No Matt-action-this-cycle required.** PC-seam wave-close push lands PC-side artifacts at origin/main; Mac-side consumes at next Mac session.

**Disposition after this memo commits + Sam Proposal 2 commits + wave-close push:** David-H enters closed state pending Matt's Option A vs Option B ratification (per § 7.2 trigger).

**End of cross-host consultation memo.**
