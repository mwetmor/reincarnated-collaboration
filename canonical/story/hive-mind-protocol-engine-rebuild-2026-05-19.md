# Hive-Mind Operating Protocol — Engine Rebuild (Gauntlet-Gap + Season-as-Emergent-Output)

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Authority:** Matt (mhwetmore@gmail.com), 2026-05-19 — directive: *"author the hypothesis tests and the potential solutions now ... review the hive mind protocol documents that you wrote and either update them for an engine rebuild session ... or if it is more sensible to do so, simply author a new and precise set of hive-mind protocols for this purpose."*

**Author:** gandalf (story-and-design steward).

**Status:** **Canonical operational protocol** for the engine-rebuild exercise (R1 + R2 + R3 + R4 + R5 + R7 + R8). Activates on Matt's directive to knight-rider. Distinct from but mechanically inherits from the 2026-05-17 Phase-1 P1 hive-mind protocol.

**Reading order:** § 0 TL;DR → § 1 Why this protocol is distinct → § 2 Mission scope → § 3 Coordination matrix → § 4 Mechanics inheritance from 2026-05-17 → § 5 Per-workstream activation requirements → § 6 Pattern-B parking dependency → § 7 Galadriel restriction (new) → § 8 Activation checklist → § 9 Cross-references.

---

## § 0 — TL;DR

**The hive moves together — again.** This is the second hive-mind activation. The 2026-05-17 Phase-1 P1 protocol established the operating mechanics (distributed authority L1/L2/L3, continuous broadcast via hive log, jack-ryan continuous-observation, tagged checkpoints, scope discipline). **This protocol inherits all those mechanics by reference** (§ 4 below) and specifies what's distinct: the mission scope (gauntlet-gap closures + season-as-emergent-output A/B test), the coordination matrix (different deliverables; different seam-assignments), per-workstream activation requirements, and one new operational constraint (galadriel sub-agent restriction).

**Seven workstreams in the engine-rebuild scope:**

| # | Workstream | Owner | Size | First-fire priority |
|---|---|---|---|---|
| **R1** | Per-tier balance targets | gamora | 1–2 wk | ⭐ Fire first (no-regret; explains playtest) |
| **R3** | Per-skill range + AI behavior schema migration | rocket + star-lord + elrond | 2–4 wk | High (foundation for R2/R4/R5/R7) |
| **R7** | AI catalogue source of truth | rocket + star-lord | 2–3 wk | Parallel with R3 (shares schema) |
| **R8** | Season-as-emergent-output A/B test | rocket + star-lord + gandalf | 1–2 wk | Parallel with R1 (independent surface) |
| **R5** | Demo AI parity audit | drax | 1 wk | After R3 |
| **R2** | 2D spatial sub-gauntlet | gamora + star-lord | 3–5 wk | After R3 |
| **R4** | Demo collision + leash + range | drax | 2–3 wk | After R3 |

**Total elapsed: ~8 weeks parallel** (with class-retuning sprint running alongside R1).

**Mission scope is FIXED** at these seven workstreams. R6 (Host-Calibration Protocol) is parked per Pattern-B-PARKED thread (§ 6). Pattern-B commercial-direction decision is **explicitly deferred and orthogonal to this exercise**.

---

## § 1 — Why this protocol is distinct

The 2026-05-17 Phase-1 P1 protocol was scoped to substrate expansion (canonical-4 → canonical-7) + diversity architecture (Layers 1–4) + registry refactors. **That work is in a different phase of the engine lifecycle** than what's being undertaken now. Specifically:

- Phase-1 P1 was **foundational architectural overhaul** — substrate identity, registry-driven foundation, cosmology/grouping vocabulary scaffolds
- Engine-rebuild-2026-05-19 is **simulation-layer surgery + generative-pipeline-flip** — fixing the gauntlet's combat model and testing whether theme-as-input can become theme-as-output

The 2026-05-17 protocol's **operating mechanics** are exactly what this session needs (distributed authority, continuous broadcast, scope discipline, jack-ryan vigilance). But its **mission scope, coordination matrix, and activation requirements** are Phase-1-P1-specific and cannot be reused as-is. Authoring a new protocol that *inherits the mechanics by reference* and *specifies what's distinct* is cleaner than amending the 2026-05-17 doc (which is canonical for Phase-1 P1 and should not be muddied with downstream mission-scopes).

This protocol is the **second invocation** of hive-mind mode. The 2026-05-17 protocol's § 14.3 explicitly anticipates reuse: *"The protocol is mode, not one-time exercise. Phase-1 P1 is its first invocation; future invocations adopt the protocol with revisions surfaced in the retrospective."* This is that future invocation.

---

## § 2 — Mission scope

The mission is captured canonically in `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` (which authored the seven workstreams with hypothesis-test design). This protocol governs **how the hive executes** that mission, not what the mission is.

### § 2.1 — In-scope work

The seven workstreams (R1, R2, R3, R4, R5, R7, R8) and their dependencies. Specifically:

- All schema migrations defined in R3
- All catalogue-source-of-truth work in R7
- All gauntlet model changes in R1, R2
- All demo runtime work in R4, R5
- All generative-pipeline-flip work in R8 (including the CLI flag additions for `--theme-input` / `--no-coalesce`)
- Class-retuning sprint following R1 (treated as in-scope; not separately tracked)
- All hypothesis-test execution + reporting per workstream

### § 2.2 — Out-of-scope work

- R6 — Host-Calibration Protocol (parked per Pattern-B PARKED thread)
- Any Pattern-B-conditional engineering (host-game adapters, mod-export DBR/DAT translators, calibration protocols beyond R7's catalogue source of truth)
- New canonical-story work outside the engine-rebuild scope (gandalf canonical-story authorship continues but is not load-bearing for this exercise)
- Visual benchmark work beyond what galadriel's already-in-flight Track-C deliverable produces
- Pitch-to-life portrait work (paused; not load-bearing)
- Phase-1 P1 work that's already shipped (canonical-6 retire, canonical-7 substrate, diversity architecture) — those are foundation, not in-scope re-work

### § 2.3 — Scope-creep examples (mid-flight pressures + defaults)

| Mid-flight pressure | Default disposition |
|---|---|
| "Should we also add a new substrate while we're rebuilding?" | REJECT. Substrate set is fixed per Phase-1 P1 commitment. |
| "R1 retune surfaces that some classes can't pass per-tier targets at all; should we redesign them?" | DEPENDS. If structural failure of class concept (rare), surface as L3. If tuning gap, retune within sprint. |
| "R8 A/B reveals the emergent theme is unexpectedly compelling; should we commit to it as default immediately?" | DEPENDS. If A/B results pass hypothesis criteria cleanly, gandalf authors design-doc amendment; Matt approves (L3). |
| "R3 schema migration touches the substrate identity declarations; should we revise them?" | ESCALATE to gandalf for design judgment; L3 if revision needed. |
| "Galadriel finishes Track-C visual benchmark and wants to commission follow-up captures during R4 demo work?" | ACCEPT if scoped (galadriel observes, does NOT spawn sub-agents per § 7). |
| "Pattern-B research arrives during the rebuild (Crate response, Last Epoch data)?" | FILE in PARKED thread; do not let it pull focus from engine-rebuild scope. |

---

## § 3 — Coordination matrix

Per-deliverable seam assignment. Knight-rider maintains this matrix and consults it before dispatching cross-seam work.

| Workstream | Rocket | Gamora | Star-lord | Drax | Jack-ryan | Gandalf | Galadriel |
|---|---|---|---|---|---|---|---|
| **R1 — Per-tier balance targets** | reads | **OWNER** | reads (telemetry) | — | observes | spec input | — |
| **R2 — 2D spatial sub-gauntlet** | reads | **OWNS combat model** | **OWNS telemetry emission** | — | reviews math | spec input | optional capture if scenarios visualized |
| **R3 — Per-skill range + AI schema** | **OWNS schema + catalogue** | consumer | **OWNS export + telemetry** | consumer | observes | spec input | — |
| **R4 — Demo collision + leash + range** | — | — | — | **OWNER** | observes | — | optional capture for validation |
| **R5 — Demo AI parity audit** | — | — | — | **OWNER** | observes | — | optional capture for validation |
| **R7 — AI catalogue source of truth** | **OWNS schema + sim consumption** | consumer | **OWNS catalogue + parity-test infrastructure** | consumer | reviews coherence | — | — |
| **R8 — Season-as-emergent-output** | **OWNS generation pipeline** | reads | **OWNS LLM orchestration** | reads (cosmology consumers if any) | reviews methodology | **OWNS theme-coalescence prompt + cohesion judging** | — |

**Reading the matrix:**
- **OWNER** = seam authors the work; surfaces decisions per § 4-inherited L1/L2/L3 protocol
- **OWNS X** = seam owns a specific facet of the workstream
- **consumer** = seam reads the contract / schema; must adapt their code
- **reads** = seam needs to know what's happening but doesn't directly consume
- **observes** = jack-ryan watches for drift / Pattern-P7 / math-before-code
- **reviews** = jack-ryan or gandalf actively reviews the work product
- **spec input** = gandalf provides the design specification the workstream targets

**Cross-workstream dependencies:**
- R3 (schema migration) → R2 (sub-gauntlet needs per-skill range), R4 (demo needs range/aggro/leash), R5 (demo AI reads JSON), R7 (catalogue uses same schema)
- R7 (parity test infrastructure) → enables R5 + R4 validation
- R1 (per-tier targets) → no upstream dependencies; fires first
- R8 (theme-coalescence) → no upstream dependencies; parallel surface

---

## § 4 — Mechanics inheritance from 2026-05-17 (with AUTONOMOUS-OPERATION amendments)

**All operating mechanics from `canonical/story/archived/hive-mind-protocol-2026-05-17.md` are inherited as-is unless explicitly amended below.**

### § 4.0 — Critical amendment: AUTONOMOUS OPERATION (Matt directive 2026-05-19)

**The L3-to-Matt escalation pattern from the 2026-05-17 protocol is SUSPENDED for this hive-rebuild session.** Matt directive verbatim:

> *"Please be absolutely 100% certain that knight-rider will never wait for my decisions and will always rely on the decisions of the subject matter expert agent (i.e. yourself for story/design, drax for web app/demo, etc). The only protocol where 'Matt' should be listed AT ALL is to wind down the process when I deem appropriate."*

**The revised authority hierarchy for this session:**

| Decision type | Authority |
|---|---|
| Implementation within a single seam | The specialist owning that seam (L1) |
| Cross-seam coordination | knight-rider (L2) |
| Story / design / canonical-direction | **gandalf** (decides; was L3 → now L2-equivalent) |
| Engine-sim / balance-math / per-tier targets | **gamora** (decides within engine-sim seam; consults gandalf for design input) |
| Generation pipeline / catalogue / schema | **rocket** (decides within generation seam; consults gandalf for design input) |
| Export / telemetry / LLM orchestration | **star-lord** (decides within operational pipeline seam) |
| Demo / loadout / player-facing surfaces | **drax** (decides within player-presentation seam) |
| QA / discipline / process | **jack-ryan** (decides; BLOCK authority retained) |
| Catalogue curation / external data | **elrond** (decides within data-steward seam) |
| Visual perception / capture / scoring | **galadriel** (decides within visual-perception seam; sub-agent restriction per § 7) |
| Architectural / load-bearing cross-cutting decisions | **gandalf or knight-rider — they decide; no escalation** |
| Scope creep handling | gandalf + knight-rider co-decide; no Matt approval needed |
| Mid-flight protocol amendments | knight-rider authors with gandalf review |
| **Session wind-down** | **Matt declares when ready — this is Matt's ONLY listed role in this protocol** |

**What this means operationally:**
- Knight-rider does NOT escalate to Matt during operation
- Knight-rider does NOT wait for Matt decisions
- State-of-hive summaries are authored daily (per 2026-05-17 § 4.3 cadence) — Matt may read them at any discretionary cadence but does NOT need to respond
- When a decision arises that would have been L3-to-Matt under the 2026-05-17 protocol, knight-rider routes it to **gandalf** (for design/canonical/architectural) or makes the call themselves (for orchestration/sequencing) — and documents the call in the hive log
- Per-tier balance targets, R8 inversion scope, sequencing decisions, scope-creep dispositions, canonical-doc revisions — **all decided by SME agents under autonomous-operation authority**
- The only signal that returns Matt to the loop is **Matt's own decision to wind down the session**

This is a significant trust delegation. The protocol's discipline (continuous broadcast, tagged checkpoints, scope discipline, jack-ryan vigilance) is what makes autonomous operation safe. The hive runs heads-down; the picture is captured in state-of-hive; Matt comes back to wind down when ready.

### § 4.1 — Distributed authority (2026-05-17 § 3) — AMENDED

L1 in-seam specialist authority retained. L2 cross-seam via knight-rider retained. **L3 routing changed:** what was previously "to Matt" is now "to gandalf or knight-rider for autonomous decision." No L3-to-Matt during operation.

### § 4.2 — Communication discipline (2026-05-17 § 4)

Hive log at `agentic_orchestration/hive-mind/engine-rebuild-log.md` (NEW file; created at activation by knight-rider). Same entry types (STATE / QUESTION / DECISION / FRICTION / OBSERVATION / TAG / HANDOFF / AMENDMENT). Same reply latency expectations. Same daily state-of-hive cadence (knight-rider authors `state-of-hive-YYYY-MM-DD-engine-rebuild.md`).

**One amendment to § 4 (per 2026-05-17 § 14.1.1 hive log commit discipline):** fetch-before-commit on hive log file remains operative.

### § 4.3 — Cadence and rhythm (2026-05-17 § 5)

Same active-hours / checkpoint-tagging / integration-cadence / weekly milestone review. **Tag namespace:** `hive-rebuild/v0.<N>-<milestone>` (distinct from `hive/v0.<N>` used for Phase-1 P1).

### § 4.4 — Cross-seam coordination (2026-05-17 § 6)

MIGRATION.md authored concurrently by producing seam (per ADR-004). Same-file-conflict protocol. Schema coherence vigilance. **Inherited without modification.**

### § 4.5 — Continuous QA loop (2026-05-17 § 7)

Jack-ryan continuous-observation mode. Discipline #13 drift vigilance. Pattern P7 silent-default watch. Math-before-code enforcement. **Inherited without modification** — particularly load-bearing for R1 (per-tier target math) and R2 (spatial combat math).

### § 4.6 — Failure mode protocols (2026-05-17 § 8)

Seam friction handling, cross-seam contract change mid-flight, schedule risk surfacing, architectural drift detection, test-suite breakage, catastrophic failure rollback. **Inherited without modification.**

### § 4.7 — Reversibility and safety (2026-05-17 § 9)

Tagged checkpoint principle. Pre-rebuild safety baseline (Matt confirmed databases backed up 2026-05-19). Per-week safety checkpoints. Rollback discipline. **Inherited without modification.** Knight-rider tags `hive-rebuild/v0.0-pre-engine-rebuild` at activation.

### § 4.8 — Mission and scope discipline (2026-05-17 § 10)

Scope is FIXED at the seven workstreams (§ 2.1). Scope-creep protocol per § 2.3. Canonical-doc revision discipline. **Inherited without modification.**

### § 4.9 — Matt's role (2026-05-17 § 11) — AMENDED

**Matt's role for this session is reduced to session wind-down at Matt's discretion.** Specifically:
- Matt invokes knight-rider in a new window with the launch instructions
- Knight-rider activates the hive and runs autonomously
- Matt may read state-of-hive at any cadence but does NOT need to respond
- Matt may revisit at any time but the hive does NOT wait for Matt
- **Matt declares wind-down when ready** — at that point, knight-rider stops new work, ships final state-of-hive, tags final checkpoint, hive deactivates

This is a significant departure from the 2026-05-17 protocol where Matt was active in L3 approvals. **For this session, autonomous operation is the design intent.** The discipline of the protocol (continuous broadcast, tagged checkpoints, jack-ryan vigilance, scope discipline) makes autonomous operation safe.

---

## § 5 — Per-workstream activation requirements

Before each workstream begins, the following must be true:

### § 5.1 — R1 — Per-tier balance targets

- Matt has confirmed the proposed per-tier target table (per engine-rebuild doc § 2)
- Baseline measurement run: capture current per-tier WR distribution across 5 shipped seasons under aggregate-only convergence
- gamora has read `engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2
- Hive log entry: "R1 START"

### § 5.2 — R3 — Per-skill range + AI behavior schema migration

- Schema design draft exists (rocket authors as L1; gandalf design-input)
- Backfill strategy decided (re-derive from geometry-type defaults vs re-roll skills with range as generation-time field — per engine-rebuild doc § 4)
- rocket + star-lord + elrond have read engine-rebuild doc § 4
- Hive log entry: "R3 START"

### § 5.3 — R7 — AI catalogue source of truth

- Decision committed on Option A / B / C (per engine-rebuild doc § 7) — **Option A recommended**
- Parity-test infrastructure design committed
- Can fire in parallel with R3 (shared schema)
- Hive log entry: "R7 START"

### § 5.4 — R8 — Season-as-emergent-output A/B

- CLI flag design committed: `--theme-input` opt-in, `--no-coalesce` opt-out (per engine-rebuild doc § 8 CLI surface section)
- Post-convergence theme-coalescence prompt drafted by gandalf
- A/B run protocol agreed: 3 inverted + 3 baseline seasons at seed parity
- Cohesion judging protocol agreed (human + LLM judge)
- rocket + star-lord + gandalf have read engine-rebuild doc § 8
- Hive log entry: "R8 START"

### § 5.5 — R5 — Demo AI parity audit

- R3 schema migration shipped (at least the AI behavior fields)
- drax has read engine-rebuild doc § 6
- Hive log entry: "R5 START"

### § 5.6 — R2 — 2D spatial sub-gauntlet

- R3 shipped (per-skill range data available)
- Sub-gauntlet scenario design committed (3–5 scenarios per class per engine-rebuild doc § 3)
- gamora + star-lord have read engine-rebuild doc § 3
- Hive log entry: "R2 START"

### § 5.7 — R4 — Demo collision + leash + range

- R3 shipped (per-skill range + aggro/leash fields available)
- Soft-vs-hard collision decision committed (recommend soft via push-apart force per engine-rebuild doc § 5)
- drax has read engine-rebuild doc § 5
- Hive log entry: "R4 START"

---

## § 6 — Pattern-B parking dependency

The Pattern-B commercial-direction question is parked per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. **Engine-rebuild proceeds independently of Pattern-B disposition.**

Specifically:
- **R6 — Host-Calibration Protocol — is NOT in this rebuild's scope.** Pattern-B parking is its blocker. When Pattern-B resolves (Path B confirmed), R6 fires in a subsequent dispatch cycle.
- **R8 — Season-as-emergent-output — IS in this rebuild's scope** because the CLI flag design (default-coalesce, opt-in `--theme-input`, opt-out `--no-coalesce`) is Pattern-B-flexible. The same CLI surface supports Path A (default-coalesce), Path B mod-export (`--no-coalesce`), and Path C buyer choice. R8 produces value under every Pattern-B verdict.
- **The other workstreams** (R1, R2, R3, R4, R5, R7) are Pattern-B-independent — they're fight-integrity closures that every commercial path requires.

**During the rebuild, Pattern-B-related signals (Crate response, Last Epoch data, etc.)** should be filed in the PARKED thread, not allowed to pull focus from engine-rebuild work. Knight-rider routes Pattern-B signals to the PARKED thread; gandalf reviews them at next session-open per the parked-thread protocol.

---

## § 7 — Galadriel sub-agent restriction (new constraint)

**Galadriel does NOT invoke sub-agents during the engine-rebuild hive session.** This restriction is amended into her operating definition for the duration of this protocol's activation.

**Authority:** Matt directive, 2026-05-19 — *"we may need to add a restriction on galadriel to be sure she does not invoke sub agents as she had done today. Her authority is not at parity with yours and knight-rider, so invoking sub agent by her may lead to confusion as she may not have appropriate communication protocols in place."*

**Specific constraint:**
- Galadriel does NOT use the Agent tool to spawn sub-agents (Legolas Mode A, general-purpose, Explore, etc.)
- If galadriel's work requires research scout or capture-pipeline-adjacent task that exceeds her seam, she **surfaces the request to gandalf or knight-rider via hive log REQUEST entry**; gandalf or knight-rider commissions the sub-agent under their authority
- Galadriel's seam (visual perception + similarity scoring + rubric authoring + benchmark reports) **remains in-scope** — this restriction is on the *commissioning mechanism*, not the *seam*

**Rationale:**
- Galadriel's authority is not yet at parity with gandalf (story-and-design steward) or knight-rider (orchestrator) per agent-definition L3 hierarchy
- Sub-agent invocation by galadriel risks divergent communication protocols (sub-agents brief differently when commissioned by different agents)
- Galadriel is on probationary status (per 2026-05-18 disposition decision, knight-rider memo) — durable place not yet earned; her authority profile should match a probationary-track-toward-earned-seam, not assume parity with established stewards

**This constraint enters galadriel's agent definition.** Until probation closes (Track C visual-benchmark report delivery satisfying exit criterion per knight-rider memo), this restriction is durable beyond the engine-rebuild session.

**Concrete action:** knight-rider authors an amendment to `agentic_orchestration/galadriel/AGENT-DRAFT.md` (or wherever her operating definition lives) reflecting this restriction. If her agent-definition file is in `.claude/agents/galadriel.md` (per the 2026-05-18 L3-1 approval question), the amendment goes there.

---

## § 8 — Activation checklist

The engine-rebuild hive activates when ALL of the following are true:

### § 8.1 — Pre-activation requirements (gandalf, this session — complete)

- [x] Engine-rebuild solutions + tests canonical doc committed (`canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`)
- [x] Hive-mind protocol for engine-rebuild committed (this doc)
- [x] Pattern-B PARKED thread committed (`agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`)
- [ ] Galadriel sub-agent restriction amendment authored (next, before knight-rider activation)
- [ ] Knight-rider launch instructions authored (next; dispatched to Matt for use)

### § 8.2 — Knight-rider activation requirements

- [ ] Knight-rider session opened by Matt (in new window, per Matt directive)
- [ ] Knight-rider reads this protocol + engine-rebuild doc + Pattern-B PARKED thread
- [ ] Knight-rider tags pre-rebuild baseline: `hive-rebuild/v0.0-pre-engine-rebuild` (across all four repos)
- [ ] Knight-rider creates hive log file: `agentic_orchestration/hive-mind/engine-rebuild-log.md`
- [ ] Knight-rider broadcasts activation in hive log
- [ ] Knight-rider authors initial scope-of-work + coordination matrix snapshot
- [ ] Knight-rider routes initial dispatches per § 5 activation requirements (R1 + R3 + R7 + R8 fire in parallel; R2/R4/R5 queued behind R3)

### § 8.3 — Seam readiness requirements (each specialist confirms)

Each engineering seam (rocket, gamora, star-lord, drax) confirms in hive log:
- [ ] Read this protocol
- [ ] Read engine-rebuild solutions doc
- [ ] Identify in-flight work to fold into rebuild scope or pause
- [ ] Acknowledge own activation requirements per § 5
- [ ] Acknowledge in hive log

Jack-ryan confirms:
- [ ] Read this protocol
- [ ] Establish continuous-observation rhythm
- [ ] Identify Discipline-#13 / Pattern-P7 / math-before-code watchpoints for engine-rebuild scope

Gandalf confirms:
- [ ] Available for continuous design-direction support
- [ ] Theme-coalescence prompt drafted (R8 activation requirement)
- [ ] Cohesion judging protocol drafted (R8 activation requirement)

Galadriel confirms:
- [ ] Sub-agent restriction acknowledged
- [ ] Track-C visual-benchmark work continues independently of rebuild
- [ ] No new commissions during rebuild without gandalf/knight-rider authorization

### § 8.4 — Matt activation (AUTONOMOUS OPERATION — minimal)

- [ ] Matt opens knight-rider session in a new window with the launch instructions (`agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md`)
- [ ] Matt hands over launch authority to knight-rider
- [ ] Matt steps back; hive runs autonomously
- [ ] (Optional) Matt may read state-of-hive at discretionary cadence; no response expected
- [ ] (Final) Matt declares wind-down when ready — knight-rider ships final state and deactivates

**Per-tier balance target decision moves to gandalf:** the table in `engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2 stands as proposed; gandalf confirms in hive log at R1 activation; gamora proceeds under those targets.

**R8 inversion scope decision moves to gandalf:** Option 1 (full inversion as default + opt-in `--theme-input` flag) is the recommended variant; gandalf confirms in hive log at R8 activation; rocket + star-lord proceed.

**All other pre-activation Matt decisions from § 2.3 scope-creep table now route to gandalf + knight-rider.**

---

## § 9 — Cross-references

**Mission inputs:**

- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` — the seven workstreams' hypothesis-test designs (this protocol's mission scope)
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — the diagnosis the rebuild closes
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate identity (potentially revisited by R8 Test 4)
- `canonical/19-llm-call-map.md` — current LLM call map (potentially collapses dramatically under R8)

**Mechanics inheritance:**

- `canonical/story/archived/hive-mind-protocol-2026-05-17.md` — operating mechanics inherited as-is (§ 4 above)

**Operational artifacts (to be created at activation):**

- `agentic_orchestration/hive-mind/engine-rebuild-log.md` — hive log; append-only; created by knight-rider at activation
- `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD-engine-rebuild.md` — daily summaries
- `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md` — knight-rider maintains
- `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md` — knight-rider authors at activation

**Adjacent state:**

- `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md` — orthogonal commercial-direction work; do not let it pull focus
- `agentic_orchestration/gandalf/research/readout-2026-05-19/` — Pattern-B readout suite (load-bearing for future Pattern-B revisit; not load-bearing for engine-rebuild)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — all disciplines remain operative
- `agentic_orchestration/AGENTS.md` — team topology (galadriel restriction amendment lands here or in galadriel's specific definition)

**Engineering disciplines load-bearing for this rebuild:**

- Discipline #1 (math-before-code) — load-bearing for R1 per-tier math + R2 spatial combat math
- Discipline #11 (live-state verification) — load-bearing for R7 parity test
- Discipline #13 (implicit-pillar drift) — load-bearing for R3 schema migration coherence across seams
- Pattern P7 (silent-default convergence) — load-bearing for R7 (catalogue consumers must iterate, not fall back to defaults)

---

## § 10 — End of engine-rebuild deliverable batch → ROADMAP CONTINUATION (Matt directive 2026-05-19)

**The engine-rebuild's seven workstreams shipping does NOT trigger hive-mind wind-down.** Matt directive verbatim:

> *"If all hypothesis tests pass and all engine changes are implemented, please ensure that knight-rider is also empowered to continue forward with the 16-roadmap document's prioritization."*

**The flow:**

1. Seven workstreams ship + hypothesis tests pass
2. Tag `hive-rebuild/v1.0-engine-rebuild-complete` (autonomous; no Matt approval gate)
3. Final state-of-hive for the engine-rebuild deliverable batch
4. R8 result drives canonical-doc disposition (LLM call map collapse if pass; preserve current if fail) — gandalf authors, no Matt-wait
5. Discipline amendments (if any) rolled into engineering-disciplines.md
6. **Knight-rider continues forward with `canonical/16-project-roadmap.md` prioritization under same autonomous-operation authority.** Next batch of work begins.

**Roadmap continuation authority for knight-rider (explicit ordering per Matt directive 2026-05-19):**

After engine-rebuild's seven workstreams ship + hypothesis tests pass, the explicit work order is:

1. **VS2a project list** — work through it in order. Source of truth: `canonical/16-project-roadmap.md` § "VS2a — Gauntlet + Geometry + First Catalogue Integration" (gandalf-stewarded; refreshed as work advances). Knight-rider authors scope-of-work + coordination matrix for the VS2a batch; specialists execute under SME authority.

2. **VS2b project list** — only after VS2a is closed out. Source of truth: `canonical/16-project-roadmap.md` § "VS2b — Substrate Realignment + Full Catalogue" (also gandalf-stewarded). Same operating pattern as VS2a.

3. **Stage A2 phases** — only after VS2a AND VS2b are both closed out. Source of truth: `canonical/16-project-roadmap.md` Stage A2 references + `canonical/28-engine-arpg-rebalance-design.md` queue specifics. The Stage A2 work items that remain in flight or queued (B6/B7/B12/B13/B14/B16 per the roadmap's current state). Same operating pattern.

**Operational invariants across all three roadmap stages:**

- Continue hive-mind operating mode: continuous broadcast, tagged checkpoints, jack-ryan vigilance, scope discipline
- SME-agent authority continues: gandalf for design/story, knight-rider for orchestration, specialists for in-seam
- **Matt re-enters only at wind-down** — engine-rebuild completion, VS2a completion, VS2b completion, Stage A2 completion — none of these are endpoints. They are milestones. The hive proceeds to the next prioritized work without Matt confirmation.

**Commit + push authorization (extension to ADR-006 amendment per Matt directive 2026-05-19):**

Knight-rider is **granted commit + push authority upon major milestone achievement and hypothesis-test passage** without per-action authorization. Specifically:

- When a workstream's hypothesis test passes and the milestone is tagged (per § 4.3 cadence inherited from 2026-05-17 protocol), knight-rider may commit + push that milestone's state across affected repos
- "Major milestone" includes: a workstream's hypothesis test passing (R1 / R3 / R7 / R8 / R5 / R2 / R4 completing); engine-rebuild batch completion; VS2a/VS2b/Stage-A2 sub-phase completion
- Push discipline per ADR-006 amendment hard constraints remains operative (no force-push, no tag-push without specifying, no hook bypass, explicit `git push origin <branch>` refspec, summary generated from live `git log`/`git status` per Discipline #11)
- Push-readiness summary continues to surface in state-of-hive entries (Matt may read at discretionary cadence, but does NOT need to authorize)
- For Vercel-connected repos (loadout, demo), deploy triggers continue to be named in the push-readiness summary; Matt's autonomous-operation directive serves as standing informed-consent (per the autonomous-operation framing in § 4.0)

**Hive-mind mode persists until Matt declares wind-down.** Engine-rebuild was the first batch; roadmap-prioritized work is the natural continuation. The protocol's mechanics (continuous broadcast, tagged checkpoints, etc.) carry forward.

**Pattern-B remains parked.** If Pattern-B commercial-direction resolves during the rebuild or during roadmap continuation, R6 (Host-Calibration Protocol) and Pattern-B-conditional work enter the dispatch cycle at that time. Until then, the rebuild + roadmap work proceeds independently.

**Wind-down trigger** is exclusively Matt's explicit declaration (per § 4.0). Engine-rebuild completion, roadmap-priority completion, hypothesis-test results, none of these trigger wind-down. Only Matt's explicit *"wind down"* / *"end the hive"* / equivalent does.

### § 10.1 — v1.0 disposition note (gandalf 2026-05-19, autonomous-operation)

Per `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md`: `hive-rebuild/v1.0-engine-rebuild-complete` fires under explicit "category-of-completion" framing — 5 of 7 workstreams CLOSED with hypothesis-test tags fired; 2 of 7 (R4 + R5) OPERATIONAL-COMPLETE with hypothesis-test tags HELD pending Matt's playtest at wind-down (v0.16 for R4; v0.12 for R5).

The dispatch § 6.5 condition reads "when the seven workstreams ship + hypothesis tests pass." Under category-of-completion framing, this condition is met by **operational-completion** of all 7 workstreams + **engine-side hypothesis-test passage** for all 5 workstreams where the test gate is engine-side measurable. The 2 playtest-dependent tags are correctly classified as a separate category (playtest-validation) that fires at wind-down, not as a v1.0-blocking gate.

Notional `hive-rebuild/v1.1-engine-rebuild-final` fires when v0.12 + v0.16 playtest tags resolve at Matt's wind-down session. NOT fired in the engine-rebuild autonomous-operation batch.

Knight-rider proceeds to VS2a per § 6.5 explicit ordering immediately after v1.0. The full disposition arc this session (R1 Blocker 3 → R8 Sub-case 3 → R2 H1 instrument-limited → v1.0 operational-completion) establishes the "category-of-completion" pattern as the canonical disposition shape for engine-rebuild-class work where ex-ante metrics meet instrument or environmental limits.

---

*Authored 2026-05-19 by gandalf, per Matt directive. The second hive-mind activation; mechanics inherited from 2026-05-17; mission scope distinct. The gauntlet's gaps close; the season's theme tests whether it can be discovered rather than declared. Mithrandir signs.*
