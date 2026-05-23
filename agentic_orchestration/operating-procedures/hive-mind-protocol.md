# reincarnated-hive-mind-protocol — Work-Mode Skill

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting work-mode skill per `canonical/02-roadmap.md` § 2.2
>
> **Skill packaging:** this Markdown doc is the source for the eventual installable skill `reincarnated-hive-mind-protocol` (per doc 38 § 4 step 2 + Skill Creator pass). Until skill packaging lands, install by reading this doc when entering hive-mind state.

**Authored:** 2026-05-23
**Author:** gandalf (story-and-design steward; protocol author per § 18.2 of substrate protocol)
**Pattern:** cross-cutting work-mode skill — composes on top of per-agent OP skills when an agent enters hive-mind state
**Companion docs (substantive content):**
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate-acquisition P-series (current canonical hive-mind protocol)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — engine-rebuild parent P-series
- `agentic_orchestration/hive-mind-protocol-amendments-2026-05-21-evening.md` — amendments
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-hive-mind-skill-decision-routing-directive.md` — Matt's verbatim decision-routing directive (LOCKED; embedded in § 4 below)
- `agentic_orchestration/operating-procedures/knight-rider.md` § 2 Mode A + § 3.9 — immediate load-bearing application of decision-routing pattern
- `agentic_orchestration/dispatches/README.md` — dispatch authoring template
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #11, #18, #19, #20 (all load-bearing in hive-mind state)

---

## 0. What this skill IS and IS NOT

**IS:** the cross-cutting work-mode skill that activates when an agent enters **hive-mind state** — a coordinated multi-agent, multi-phase workstream operating against a shared substrate (catalogue DB, canonical artifact, or engine subsystem) with sustained background-process discipline, Wave-cycle cadence, and parallel sub-agent invocation. Captures the universal patterns that apply to ALL hive-mind cycles — not the substantive content of any one protocol.

**IS NOT:** the substantive protocol docs (those live in `canonical/story/hive-mind-protocol-*.md` per cycle subject — substrate, engine-rebuild, future M1 mythological-named-weapons, etc.). NOT the per-agent OP skill (that's `operating-procedures/<agent>.md`). NOT the dispatch authoring template (that's `dispatches/README.md`). NOT a substitute for `canonical/00-ground-state.md` first-read.

**Layering:** loaded on top of per-agent OP skill when in hive-mind mode. Knight-rider's OP § 1.5 names `reincarnated-hive-mind-protocol` as the Mode A companion. Specialists invoked sub-agent during a hive-mind cycle load this skill to understand the cadence + decision-routing surrounding their dispatch.

---

## 1. When to load this skill

| Trigger | Agent | Why |
|---|---|---|
| Knight-rider session entering Mode A (active substrate or engine-rebuild cycle) | knight-rider | Universal hive-mind orchestration patterns |
| Specialist sub-agent invocation during an active hive-mind cycle | rocket / gamora / star-lord / elrond / galadriel / drax / legolas | Understand cadence + decision-routing + checkpoint discipline surrounding the dispatch |
| Gandalf authoring or amending a hive-mind protocol doc | gandalf | Author against established universal patterns; substantive content goes in the protocol doc |
| Gandalf executing P4 cluster semantic labeling (or equivalent design-call phase) | gandalf | Understand cycle state, exit criteria, and where the design call sits in the sequence |
| Jack-ryan reviewing a Pattern-B Gate-1 dispatch authored against a hive-mind protocol | jack-ryan | Gate-1 review under hive-mind-cadence-aware framing |
| Matt opening a session mid-cycle to triage or unblock | (advisory; Matt does not load skills, but the protocol is structured to surface state for him via state files + JSON summaries) | — |

**Do NOT load this skill** for non-hive-mind work — routine dispatches, per-agent design dialogue, single-specialist tasks, demo/loadout work, ad-hoc research questions. Those follow per-agent OP skill patterns, not hive-mind patterns.

---

## 2. Hive-mind state — definition + entry/exit

### 2.1 Definition

Hive-mind state is active when ALL of the following hold:

1. **A canonical hive-mind protocol doc exists** (currently: substrate weapon-library-import; parent QD-engine-rebuild). Future cycles will have their own protocol docs.
2. **Matt has authorized firing** the cycle (verbal or written; captured in the protocol doc § 0 authority line).
3. **The cycle has not yet reached its final-phase milestone tag** (per protocol doc § 8 tag conventions).
4. **A live state file exists** at a known path (e.g., `agentic_orchestration/weapon-library-import-hive-mind-state.md`) capturing per-Wave / per-phase status.

When any of these fall away, hive-mind state has exited and routine patterns resume.

### 2.2 Entry protocol

| Step | Owner | Action |
|---|---|---|
| 1 | gandalf (or knight-rider for engine-rebuild cycles) | Author canonical hive-mind protocol doc with vision + operational layers, phase architecture, decision gates, risk register, discipline compliance matrix |
| 2 | jack-ryan | Gate-1 review of the protocol (or its first Wave dispatch) |
| 3 | Matt | Authorize firing — verbal or written; recorded in protocol § 0 |
| 4 | knight-rider | Create or initialize state file at known path; pre-flight checks per protocol § 3 (typically P0 in substrate cycles) |
| 5 | knight-rider | Fire first Wave / Phase 0 dispatch |

### 2.3 Exit protocol

| Step | Owner | Action |
|---|---|---|
| 1 | knight-rider | Final phase complete; final milestone tag cut per protocol § 8 |
| 2 | knight-rider | Wind-down summary authored — Matt-facing per § 9 of this skill |
| 3 | knight-rider | State file archived (rename with `-completed-YYYY-MM-DD` suffix; or move to `agentic_orchestration/historical/`) |
| 4 | knight-rider | CHANGELOG entry filed |
| 5 | gandalf | If post-cycle recognitions surface, author recognition record (canonical/story/) per OP § 2 recognition-record mode |

### 2.4 Mid-cycle crash recovery (per knight-rider 2026-05-23 Phase E-1 crash-triage precedent)

If the orchestrating session terminates mid-cycle (machine reset, session timeout, intentional pause):

1. **Read state file** for last known per-Wave / per-phase status
2. **Read latest JSON summaries** at known paths (per protocol doc § 12 cross-session continuity)
3. **Query DB row counts** directly to verify substrate state matches state-file claims
4. **Read latest skill_handoff** if knight-rider wrote one before termination
5. **Forensic determination** of what completed vs what was mid-flight (check committed vs uncommitted artifacts; check process completion outputs vs intermediate)
6. **Author crash-triage handoff** at `agentic_orchestration/skill_handoff_<YYYY-MM-DD>-<cycle>-crash-triage.md` capturing forensic + recovery plan
7. **Author thin continuation dispatch** that references the original dispatch as authoritative for scope + acceptance, names the specific resumption point, and instructs specialist to resume rather than re-do

---

## 3. Cycle cadence + structure

### 3.1 Phase architecture

The canonical protocol doc owns the substantive phase structure. The universal pattern across hive-mind cycles:

- **Pre-flight phase** (P0 in substrate; pre-Wave-0 in engine-rebuild): schema lock, API key checks, robots.txt verification per Discipline #20, DB greenfield confirmation
- **Acquisition / generation phases** (P1 substrate; W0-W1 engine-rebuild): the work-volume phases; multi-Wave; parallel sub-agent invocation; background processes per Discipline #19
- **Analysis phases** (P1.5 → P5 substrate; W2+ engine-rebuild): feature extraction, math-hotspot phases (P2 axis discovery, P3 clustering — see § 7 below), validation
- **Design-call phases** (P4 in substrate): gandalf + Matt focused review; not automatable; ~2-3 hours active Matt time per phase
- **Operational-ongoing phases** (PD Meshy gap-fill in substrate): post-final-tag; continuous; per-iteration summaries

### 3.2 Wave-cycle cadence within phases

A **Wave** is a parallel batch of sub-agent invocations within a phase, with aggregation + checkpoint + state-file update before the next Wave fires:

```
Wave N start
  ↓ knight-rider fires parallel sub-agent dispatches (multiple Agent tool calls in single message — see § 4.3)
  ↓ specialists execute background per Discipline #19
  ↓ knight-rider monitors via DB queries + JSON summary existence (NOT Agent tool — Discipline #19)
  ↓ all sub-agents complete OR explicit abort signal
  ↓ knight-rider aggregates returns; state-file updated; checkpoint tag if milestone
  ↓ Wave N+1 fires (or phase boundary)
```

**Wave-internal failure handling:** one sub-agent failing does not block siblings unless explicit data dependency. Failed sub-agent's work captured in state file; retry or scope-reduce per protocol risk register.

### 3.3 Decision gates within phases

Each protocol doc names its own gates (G1-G4 typical for substrate cycle). Universal pattern:

- Gates **hold dispatches pending input** — they are pause points, not auto-escalation points
- Gates resolved by seam-owning agent OR by Matt (per § 4 decision routing) — NEVER by knight-rider solo within seams he doesn't own
- Gate resolution captured in state file + protocol doc per gate metadata

---

## 4. Decision routing (VERBATIM Matt 2026-05-23 directive — LOAD-BEARING)

> *"knight-rider should always call upon the agent who owns each seam for decisions during hive mind run state. Only as a last resort if no amount of collaboration will solve the problem should the decision be made to wait for Matt. During hive mind state, knight-rider should always invoke agents per seam as sub-agents."*
>
> — Matt 2026-05-23 (verbatim verbal directive; LOCKED)

### 4.1 Seam-routing table

When a decision surfaces during an active hive-mind cycle, route to the seam-owning agent FIRST:

| Decision touches | Seam-owning agent (always-first decider) | Sub-agent invocation |
|---|---|---|
| Generation / element / anchor / foundation / engine-internal canonical | **rocket** | `Agent({ subagent_type: "rocket", prompt: "<scoped question>" })` |
| Simulation / spirit guide / balance / fight engine | **gamora** | `Agent({ subagent_type: "gamora", prompt: "<scoped question>" })` |
| Export / output / telemetry / LLM seam | **star-lord** | `Agent({ subagent_type: "star-lord", prompt: "<scoped question>" })` |
| Catalogue DB / abstraction-analysis / cross-cutting data | **elrond** | `Agent({ subagent_type: "elrond", prompt: "<scoped question>" })` |
| Visual perception / similarity scoring / benchmark rubrics | **galadriel** | `Agent({ subagent_type: "galadriel", prompt: "<scoped question>" })` |
| Demo / loadout / player-facing presentation | **drax** | `Agent({ subagent_type: "drax", prompt: "<scoped question>" })` |
| Research / catalogue crawl / external literature / methodology consultation | **legolas** | `Agent({ subagent_type: "legolas", prompt: "<scoped question>" })` |
| Design intent / thematic / experiential / canonical-story coherence | **gandalf** | `Agent({ subagent_type: "gandalf", prompt: "<scoped question>" })` |
| Process gate / QA / discipline citation / decisions-log | **jack-ryan** | `Agent({ subagent_type: "jack-ryan", prompt: "<scoped question>" })` |

### 4.2 Escalation hierarchy — Matt is LAST resort

Order of escalation during a hive-mind decision:

1. **Seam-owning agent decides within their authority** — default; no escalation
2. **Cross-seam collaboration via parallel sub-agent invocation** — knight-rider invokes multiple seam owners; aggregates; synthesizes
3. **Critique-pair invocation** — jack-ryan (process) and/or gandalf (design) invoked as sub-agents if concerns surface
4. **Re-attempt collaboration with refined framing** — if first pass didn't converge, re-scope and re-invoke
5. **Last resort — wait for Matt** — only when no amount of collaboration resolves

**"Last resort" means literally last resort.** Not "I'd like Matt to weigh in." Not "this seems important enough." Matt's bandwidth is the project's scarcest resource during hive-mind cycles; he is **escalation, not concurrence.**

### 4.3 Sub-agent invocation is the always-channel

During hive-mind state, knight-rider's decision-relay shape is:

- **NOT:** "I think we should X because Y" → wait for Matt confirmation
- **NOT:** drafting a dispatch and waiting for Matt review before invoking the seam owner
- **IS:** `Agent({ subagent_type: "<seam>", prompt: "<scoped question>" })` → seam owner returns decision → integrate → continue cycle

**Parallel invocation when independent.** Multiple seam touches in a single message = multiple Agent tool calls in that message (per Discipline #19 — don't sequence what can run in parallel; harness notifies on completion).

### 4.4 What this directive does NOT do

- **Does NOT** remove Matt's final decision authority. Architectural commitments, milestone tags, ADRs, cross-seam schema changes still require Matt per ADR-002.
- **Does NOT** remove jack-ryan's process-gate authority. Gate-1 review of Wave dispatches still fires per dispatches/README.md; Gate-2 BLOCKs still require remediation. The directive operates WITHIN gate structure, not around it.
- **Does NOT** remove gandalf's design-side critique-pair role. Design-side critiques during hive-mind cycles routed via gandalf sub-agent invocation per § 4.1.
- **Does NOT** apply outside hive-mind state. Routine sessions follow per-agent OP-skill routing patterns.

**Full directive capture:** `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-hive-mind-skill-decision-routing-directive.md`

---

## 5. Critique-pair structure during hive-mind state

Each hive-mind protocol declares its critique-pair structure per phase. Three universal patterns:

### 5.1 Pattern A — Design + Implementation

Specialist implements; another specialist (or gandalf for design dimension) critiques in parallel. Used when execution is well-scoped but design or methodology dimension warrants concurrent review.

Example: P1.5 feature extraction — rocket implements; gandalf reviews feature-class coverage; legolas Mode A reviews methodology rigor.

### 5.2 Pattern B — Spec + Review (Gate-1 dispatch pattern)

Specifier authors dispatch spec; reviewer (typically jack-ryan in DESIGN-MODE) reviews BEFORE execution fires. Gate-1 review pattern per `agentic_orchestration/dispatches/README.md`.

Example: P2 axis discovery — rocket/elrond authors math note + dispatch; jack-ryan Gate-1 review (Discipline #1, #11, #18 compliance); Matt amendments; FIRE-READY.

### 5.3 Pattern C — Critique-pair memo (sustained dialogue)

Sustained design dialogue captured as memo. Used for design-call phases (P4 cluster labeling) and per-iteration learnings (PD Meshy gap-fill galadriel summaries).

Example: P4 cluster semantic labeling — gandalf + Matt design call; jack-ryan reviews artifact post-session.

### 5.4 Gate routing during hive-mind state

- **Gate 1 (DESIGN-MODE)** fires per Pattern B before any Wave dispatch with new architectural scope or methodology choice
- **Gate 2 (DEV-MODE BLOCK authority)** fires per `REVIEW_PROCESS.md` after Wave execution; jack-ryan reviews for discipline compliance + scope drift
- **Critique-pair Gate-2 ratification** (autonomous-pair) — jack-ryan + gandalf can ratify minor closeouts under Matt pre-authorization per `dispatches/README.md` Pattern E (precedent: W0.7 cumulative close-out 2026-05-22)

### 5.5 Hive-mind sub-agent verdict pattern (substantive design-fit + methodology assessment)

When knight-rider's decision-routing (§ 4) surfaces a **multi-option assessment / ranked-recommendation / file-output question** during hive-mind state, the seam-owning sub-agent produces a **verdict artifact**, not an inline reply. This is the substantive analog to the gate routing above — used when the question shape exceeds what an inline structured-critique can carry.

#### 5.5.1 When this pattern fires

Knight-rider's invocation prompt triggers verdict pattern when ANY of:
- Invocation asks for ranked-preference across N options
- Invocation poses multiple numbered questions requiring per-question reasoning
- Invocation explicitly asks for file output at a named path
- Invocation is a design-fit assessment, methodology selection, or remediation-options assessment at a math hotspot

Inline structured-critique (5-10 bullets, ≤200 words) is **insufficient output shape** for these question shapes. The role-specific OP skill discriminator language defines the per-seam variant (e.g., gandalf OP § 2 Pattern A-deep).

#### 5.5.2 Knight-rider's invocation responsibilities

When invoking a sub-agent under verdict pattern:

1. **Name the file path explicitly** in the invocation prompt — e.g., "file verdict to `agentic_orchestration/gandalf/notes/<YYYY-MM-DD>-<topic>-verdict.md`"
2. **Carry the substantive premise** — don't expect sub-agent to derive hypotheses from scratch; include the design-side anchor docs, the empirical evidence, and the specific question shape
3. **Name the option set** — don't leave the sub-agent to invent options; provide knight-rider's option ranking as starting framing (sub-agent may add or refine)
4. **List the read-set** — concrete file paths the sub-agent should consult; include both the question-specific docs AND the sub-agent's own canonical authoring anchors

#### 5.5.3 Sub-agent's responsibilities

Sub-agent produces verdict with:
- **Top-line headline** + load-bearing additions or dissents from invoker's framing
- **Question-by-question** answers, anchored on canonical docs by section number
- **Per-option assessment** with seam-specific fidelity assessment + strengths/weaknesses + lean
- **Ranked recommendation** with explicit tier table
- **Sign-off** with author + date + anchor docs cited

Sub-agent pushes back where warranted — verdicts are where strong opinions land; deferential softening fails the role.

#### 5.5.4 File-write constraint

Sub-agent environment policy may prevent direct file write. In that case, sub-agent returns the verdict in full to invoker (knight-rider); invoker captures to the named path. **Knight-rider's capture is durable; the verdict's authority is sub-agent-authored.** This is not a failure mode — it's the documented coordination pattern when sub-agent write scope is restricted.

#### 5.5.5 Founding precedent

`agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md` (2026-05-23). Sub-agent gandalf returned substantive 7-option design-fit assessment + load-bearing E1 lineage audit higher-order finding + ranked tier table; knight-rider captured to gandalf/notes/ on sub-agent's behalf. This is the durable example of the pattern working correctly.

---

## 6. Discipline #19 + checkpoint protocol

### 6.1 Discipline #19 — Agent tool is not for waiting

**RATIFIED 2026-05-22.** All long-running phases as background processes. Status via:

- Direct Bash + DB queries (e.g., `sqlite3 /Users/admin/Games/reincarnated-loadout/data/telemetry.db "SELECT COUNT(*) FROM weapon_knowledge_entries;"`)
- JSON summary artifact existence at known paths (per protocol § 12)
- PID checks via `ps`
- `nohup ... &` for crawls / imports / ML runs that exceed terminal session
- Harness completion notifications when sub-agent invocations finish (no polling, no `sleep`-loop)

**NEVER:** repeatedly invoking Agent tool to "check on" a background process. **NEVER:** `sleep` loops as poor-man's-wait.

### 6.2 Checkpoint discipline

| Granularity | When | What |
|---|---|---|
| **Per-Wave checkpoint** | Wave completion | Aggregate sub-agent returns; update state file; commit Wave artifacts; optional intermediate tag |
| **Per-phase milestone tag** | Phase completion | `<cycle>/v<PHASE>.<WORKSTREAM>-<DESCRIPTOR>` intermediate tag (per protocol § 8) |
| **Matt-approved milestone tag** | Phase Matt-acceptance | `<cycle>-v<PHASE>.0-<phase-name>-shipped` milestone tag |
| **Cycle final tag** | All phases complete | `<cycle>-v<FINAL>.0-<cycle>-ready` final tag |

Per `~/Games/reincarnated-engine/design/decisions/decisions-log.md` ADR-001 tag convention.

### 6.3 PID tracking pattern

When firing background processes, capture PID + log path:

```bash
nohup python <script> > <log-path> 2>&1 &
echo $! > <pid-file>
```

State file logs per-Wave: { workstream, PID, log path, start time, expected duration, status }. Knight-rider checks PID liveness via `ps -p <pid>` between Wave checkpoints. If a PID dies unexpectedly, capture log + state and route to specialist for triage.

---

## 7. Math hotspots + Discipline #18

### 7.1 Math-hotspot phases

Per `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2 — current named hotspots:

| Hotspot | Phase | Owning seam | Methodology surface |
|---|---|---|---|
| **P2 axis discovery** | Substrate protocol P2 | elrond (execution); gandalf (design intent + acceptance criterion) | PCA vs factor analysis vs NMF vs UMAP vs t-SNE; variance-explained validation; axis-stability bootstrapping; interpretability scoring |
| **P3 multimodal clustering** | Substrate protocol P3 | elrond (execution); gandalf (design intent + acceptance criterion) | HDBSCAN vs k-means vs GMM vs spectral; silhouette + Davies-Bouldin + gap-statistic validation; multimodal-distance-metric design |
| **P5 cohesion-judge calibration** | Both protocols' P5 | star-lord (statistics); gandalf (design intent); gamora (simulation-side integration) | LLM-judge calibration; inter-rater reliability; significance testing; probability calibration via isotonic regression |

### 7.2 Discipline #18 — Methodology-before-execution

At every math hotspot:

1. **Commission legolas Mode A research first** for external-literature methodology grounding
2. **Design call locks the methodology** (gandalf + owning-seam + Matt) BEFORE any code runs
3. **Acceptance criteria defined upfront** — variance thresholds, validation metrics, interpretability scoring — not after looking at output
4. **Stability / sensitivity analysis required** at execution time (bootstrapping, cross-validation, ablation across hyperparameters)

**Failure mode this discipline guards against:** "looks-correct-but-subtly-wrong" — execution produces output that passes basic eyeball checks but is methodologically incorrect (wrong technique for data shape, unstable under resampling, miscalibrated at tails, variance-loaded on wrong subsets). Downstream validation cannot detect this because the methodology error is locked into the output's structure.

**Light hotspots** (worth flagging but lower severity): P1.5 feature extraction (embedding-model choice); P5 substrate-density precomputation (density-estimation technique). Follow Discipline #1 + #11 without full design-call ceremony.

---

## 8. State-file + cross-session continuity

### 8.1 State file at known path

Per active cycle, knight-rider maintains a state file:

- **Substrate cycle:** `agentic_orchestration/weapon-library-import-hive-mind-state.md`
- **Engine-rebuild cycle:** state file path declared in protocol § 12
- **Future cycles:** state file path declared in respective protocol doc § 12

### 8.2 State-file update cadence

| Event | Update |
|---|---|
| Wave start | Append Wave header with PID + log paths per sub-agent dispatch |
| Wave completion | Append Wave outcome; per-sub-agent return summary; aggregated state |
| Phase boundary | Phase milestone tag recorded; gate-resolution recorded if applicable |
| Cycle completion | Final tag + archive marker |
| Crash recovery | Triage handoff cross-referenced |

### 8.3 JSON summary artifacts

Per protocol § 12 cross-session continuity. Each dispatch produces a JSON summary at a known path. Mid-cycle recovery: read state file + JSON summaries + DB row counts → reconstruct cycle state without re-running any work.

### 8.4 Tag-as-state-marker

Milestone tags per protocol § 8 are the durable cross-session markers. DB state at tag-time is recoverable (restore DB from milestone-tagged backup if necessary).

---

## 9. Wind-down protocol

### 9.1 Per-phase wind-down

| Step | Owner | Action |
|---|---|---|
| 1 | knight-rider | Phase completion verified (per protocol § 6 phase success criteria) |
| 2 | knight-rider | Per-phase milestone tag cut |
| 3 | knight-rider | State-file phase marker appended |
| 4 | jack-ryan | Gate-2 discipline-compliance review (if phase scope warrants) |
| 5 | gandalf | Design-side check if phase produced design-impacting output (e.g., P2 discovered axes; P3 clustering output → P4 design call queued) |
| 6 | knight-rider | Next-phase dispatch authored (or cycle wind-down if final phase) |

### 9.2 Cycle wind-down (Matt-facing)

When the final phase tag is cut:

1. **Wind-down summary** at `agentic_orchestration/<cycle>-wind-down-summary-<YYYY-MM-DD>.md` (precedent: `weapon-library-import-wind-down-summary-2026-05-22.md`):
   - Cycle outcome — what landed; vs original scope; vs acceptance criterion
   - Per-phase summary with milestone tags
   - Open carries to next cycle (C-series typically)
   - Matt-facing decisions still queued
2. **State-file archival** — rename `<cycle>-hive-mind-state.md` to `<cycle>-hive-mind-state-completed-<YYYY-MM-DD>.md` OR move to `agentic_orchestration/historical/`
3. **CHANGELOG entry** for cycle completion
4. **Decisions-log entry** via jack-ryan for any architectural commitments locked during cycle
5. **Recognition record** (gandalf) at `canonical/story/` if post-cycle design recognitions surfaced

### 9.3 Anti-pattern — silent cycle drift

A hive-mind cycle without a final tag, archived state file, and wind-down summary leaves the team in ambiguous state. **Never let a cycle implicitly transition into "we just kind of moved on."** Either tag + archive + summarize, OR keep the state file live and continue executing — no third option.

---

## 10. Pre-flight + emergency protocols

### 10.1 Pre-flight checks (Phase 0 or equivalent)

Every hive-mind cycle has pre-flight checks specific to its scope. Universal checks:

- **Discipline #20 robots.txt verification** (jack-ryan parallel authoring per cycle; per-source `User-agent: ClaudeBot` + `User-agent: anthropic-ai` Disallow-list check) for any crawl-based source
- **API key persistence** (`echo "${KEY_NAME:0:4}"` in fresh terminal) for any API-dependent source
- **DB state confirmation** (greenfield or post-prior-cycle state expected)
- **Per-source TOS check** for any external-data source
- **Disk space** for substrate / asset / log volume estimates

### 10.2 Emergency protocols

| Emergency | Response |
|---|---|
| **Mid-phase specialist failure** | Specialist captures state in JSON; knight-rider intermediate-tags; pauses; routes to seam-owning sub-agent for triage |
| **Data corruption** | Restore DB from last milestone-tag backup; re-run affected phase from milestone state |
| **Resource exhaustion** (DB size, processing time, disk) | Scope reduction; defer non-blocking sources; re-prioritize per risk register |
| **Machine reset / session termination** | Crash-triage protocol per § 2.4 above (precedent: Phase E-1 crash-triage 2026-05-23) |
| **Methodology error caught post-execution** | Roll back to pre-methodology state via milestone tag; rerun Discipline #18 methodology consultation; re-execute |
| **Drift recognized mid-cycle** | jack-ryan Pattern-B Gate-1 rescope dispatch authored; Matt approval; cycle paused at clean boundary; rescoped Wave fires |

### 10.3 What this skill does NOT cover

- **Substantive protocol design** — substrate-specific or cycle-specific scoping lives in the canonical protocol doc, NOT this skill
- **Decision telemetry / archive format** — covered by `reincarnated-canonical-doc-format` skill (companion) and decisions-log format
- **Critique-pair gate protocol substantive** — covered by `reincarnated-critique-pair-gate-protocol` skill (companion) when authored
- **Dispatch authoring template** — covered by `dispatches/README.md` (companion)

---

## 11. Skills to install alongside this one

### Universal in hive-mind state
- **Per-agent OP skill** (always — the skill being composed on top of)
- `reincarnated-engineering-disciplines` (the 20 disciplines; especially #11, #18, #19, #20)
- `reincarnated-decision-log-format` (cycle-completion ADR-style entries)
- `reincarnated-canonical-doc-format` (protocol doc + recognition record authoring)

### Cross-cutting (load when relevant within hive-mind state)
- `reincarnated-substrate-vector-cheatsheet` (BC axes; load for design-spec-as-math work during P2 / P3 / P4)
- `reincarnated-critique-pair-gate-protocol` (load for Pattern-B Gate-1 dispatch authoring + review)

### Cycle-specific (load when in that cycle)
- Substrate cycle: `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` as substantive content
- Engine-rebuild cycle: `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` as substantive content
- Future cycles: respective canonical protocol doc

---

## 12. Update protocol for this skill

This is a cross-cutting work-mode skill — it evolves when:

- **A new hive-mind cycle starts** with patterns not yet captured (extend § 2 + § 3 with universal patterns; cycle-specific patterns go in the canonical protocol doc, not here)
- **A new discipline lands** affecting hive-mind state (extend § 6 + § 7)
- **A new decision-routing pattern is locked** (Matt directive amendment; extend § 4 with verbatim capture)
- **A new emergency protocol is observed in practice** (extend § 10.2)
- **A new wind-down pattern lands** (extend § 9)
- **A math hotspot is added or refined** (extend § 7.1 hotspot table — but the living source of truth is `gandalf/notes/2026-05-23-mathematical-seam-naming.md` § 2; this skill cross-references)

**Authored / maintained by gandalf** (story-and-design steward; protocol author lineage from substrate protocol § 18.2). Knight-rider may propose amendments from observed orchestration practice; jack-ryan reviews process-side compliance; specialist sub-agents may propose amendments via gandalf request artifacts. Gandalf approves before commit.

---

## 13. Cross-references

### Canonical (substantive content)
- `canonical/00-ground-state.md` — ground-state oracle (always first-read; § 4 first-reads by role)
- `canonical/02-roadmap.md` § 2.2 — Stream 3 placement of this skill
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate cycle protocol
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — engine-rebuild cycle protocol

### Operational
- `agentic_orchestration/AGENTS.md` — seam ownership map (basis for § 4.1 seam-routing)
- `agentic_orchestration/GOVERNANCE.md` — founding ADRs (ADR-002 final approval; ADR-001 tag convention; ADR-004 cross-repo coordination)
- `agentic_orchestration/REVIEW_PROCESS.md` — five principles + Gate-1 / Gate-2 framework
- `agentic_orchestration/dispatches/README.md` — dispatch authoring template
- `agentic_orchestration/operating-procedures/knight-rider.md` — knight-rider OP (especially § 2 Mode A + § 3.9 decision-routing application)
- `agentic_orchestration/operating-procedures/jack-ryan.md` — jack-ryan OP (Gate-1 / Gate-2 framing)
- `agentic_orchestration/operating-procedures/gandalf.md` — gandalf OP (Pattern A subagent / Pattern B dialogue framing)
- `agentic_orchestration/hive-mind-protocol-amendments-2026-05-21-evening.md` — protocol amendments

### Directive captures
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-hive-mind-skill-decision-routing-directive.md` — Matt's verbatim decision-routing directive (LOCKED; embedded in § 4 above)
- `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` — Mathematical Layer + math-hotspot living list (cross-referenced in § 7)

### Engineering disciplines
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — 20 disciplines; load-bearing in hive-mind state especially #11 empirical inspection, #18 methodology-before-execution, #19 Agent-tool-not-for-waiting, #20 robots.txt + Claude-agent directive respect

### Decisions-log
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — temporal decisions log; cycle-completion entries land here

---

## 14. Sign-off

**Author:** gandalf (story-and-design steward; protocol-author lineage)
**Authority:** Matt 2026-05-23 — Stream 3 work-mode skill authorization
**Status:** CURRENT — load-bearing for all hive-mind-state invocations
**Maintenance:** gandalf authors + maintains; knight-rider proposes amendments from observed orchestration practice; jack-ryan reviews process-compliance; specialists propose via gandalf request artifacts.

**For:** the universal work-mode skill that composes on top of per-agent OP skills when an agent enters hive-mind state. Captures: hive-mind-state definition + entry/exit; Wave-cycle cadence; decision routing (verbatim Matt 2026-05-23 directive); critique-pair structure; Discipline #19 + checkpoint discipline; math hotspots + Discipline #18; state-file + cross-session continuity; wind-down protocol; pre-flight + emergency protocols. Substantive cycle-specific content lives in the canonical protocol doc per cycle subject, NOT in this skill.
