# Federated PC Team Architecture — Architectural Commitment

**STATUS:** CURRENT (load-bearing architectural commitment from 2026-06-07 forward)
**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 verbatim ratification — "ratify drax spike fire and let's build out the full PC team in parallel" + name ratifications "I agree with Radagast and Sam" + execution-plan ratification "alpha, push per artifact, you fire the ssh"
**Type:** load-bearing architectural commitment — federated agents with seam-bound authority across Mac and PC hosts
**Companion docs:**
- `canonical/story/2026-05-31-ue-seam-agent-placement-decision.md` (predecessor — UE-seam agent placement at PC; pattern-symmetry premise)
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` (predecessor — three-machine infrastructure architecture)
- `agentic_orchestration/gandalf/notes/2026-06-07-next-session-plan-spike-continuation-and-pc-coordination-architecture.md` (origin — Tier 1/2/3 proposal)

---

## 0. TL;DR

The Reincarnated team expands from 10 Mac-resident agents to a **federated topology**: 10 Mac-resident agents continue cross-cutting work; **3 PC-resident counterparts** are added (David-H / Radagast / Sam) handling PC-seam orchestration, design critique, and QA gatekeeping locally on PC. Each PC counterpart inherits the full Mac-side team's canonical record, disciplines, and learnings at commit time but accumulates PC-seam-specific learning thereafter.

**Why federated, not duplicated:** the PC counterparts are seam-scope-bound. Mac-side agents retain authority over cross-cutting canonical architecture, engine design, and game-as-product strategy. PC-side counterparts hold authority over PC-seam-specific work (UE patterns, Niagara, Mutable, weapon-sockets, rendering, animation, asset pipeline). Cross-host coordination flows via **file-based message bus** (commit + push + fetch on the shared meta-repo).

**Names ratified (Matt 2026-06-07):**
- **David-H** (PC-side orchestrator counterpart to Mac-KR). Inverts the Knight Rider symbology — David Hasselhoff was the human handler; KITT was the orchestrating AI. David-H = PC-seam handler.
- **Radagast** (PC-side design steward counterpart to Mac-gandalf). Brown wizard, domain-bound, explicitly non-competing with Gandalf for architectural primacy. Chosen over Saruman to retire drift-risk at the naming layer.
- **Sam** (PC-side QA gatekeeper counterpart to Mac-jack-ryan). Sam Fisher (Splinter Cell) — Tom-Clancy-genre tactical operator with gates-and-checkpoints discipline. Chosen over Ego (rejected — wrong archetype for QA gatekeeping role).

**This is a load-bearing architectural commitment.** Subsequent PC-seam work routes through the federated team per the routing table at § 5.

---

## 1. The architectural problem this solves

### 1.1 Pattern-regression observation (Matt 2026-06-06 design call)

Phase A2 + cosmograph Phase A: **0 Matt-touches** per cycle (sub-agent fan-out + monitoring-quiet mode + autonomous critique-pair gates).

Mantis session 1 (PC-resident, SSH-from-Mac): **several Matt-touches** in the first session alone (clone path blocker, mantis OP `~/Games` path mismatch, cross-host signal relays).

The pattern regression is real: the Mac-side team's collaboration patterns (sub-agent fan-out, Pattern E autonomous critique-pair ratification, file-based coordination) don't extend across the host boundary when there's no PC-side critique-pair or orchestrator. Every PC-side decision either burns Matt-touches or proceeds without team-discipline gates.

### 1.2 Five concerns surfaced (verbatim from next-session plan § 2.1)

- **Collaboration:** mantis can't easily fire gandalf/jack-ryan critique-pair locally on PC
- **Governance:** every cross-host signal requires Matt as relay
- **Speed:** Pattern E autonomous-pair ratification can't fire on PC
- **Team-learning:** lessons from cosmograph (substrate-led-at-rendering, Discipline #11 empirical, family-contraction audit) don't propagate to mantis's UE decisions
- **Pattern regression:** Mac-side discipline patterns don't extend across host boundary without PC-side counterparts

### 1.3 Why federated counterparts over alternatives

**Alternative 1 — Tier 1 sub-agent fan-out only** (mantis fires `Agent({ subagent_type: "gandalf" })` locally on PC): lighter-weight; preserves Mac canonical authorship as single source. But sub-agent invocations are session-fresh per fire; no persistent PC-side learning accumulates; Pattern E critique-pair ratification still requires invocation overhead per decision.

**Alternative 2 — PC-resident KR scoped to UE-seam only** (deferred Tier 2 path from 2026-06-07 proposal): solves orchestration but leaves design critique + QA gates Mac-bound.

**Alternative 3 — Full host symmetry** (deferred Tier 3 path): every Mac agent has a PC counterpart. Premature given current PC seam is mantis-only (UE).

**Federated counterparts (this commit):** 3-agent PC team (orchestrator + design + QA) gives mantis a complete critique-pair + orchestration loop locally. Composes with Mac-side seam authority preserved at the cross-cutting layer. Reversible at low cost since PC-seam canonical authoring is scope-bound (won't overlap Mac-side until PC seam expands substantially).

---

## 2. Federated architecture

### 2.1 Topology

```
                     Matt (Senior Architect)
                     /                       \
              Mac team                       PC team
            (10 agents)                    (3 agents)
                |                                |
   knight-rider, gandalf,                David-H (orch),
   jack-ryan, gamora,                    Radagast (design),
   rocket, star-lord, drax,              Sam (QA),
   elrond, legolas, galadriel                  ┴
                |                              |
                +-----[file-based bus]----+----+
                       (commit + push + fetch
                        on shared meta-repo)
                                                |
                                            mantis
                                       (PC-resident
                                        UE-seam dev)
```

### 2.2 Seam-bound authority model

Each PC counterpart is **scope-bound to the PC seam**:

- **PC-seam work** = work whose source code or artifacts live primarily on PC and whose render/execution target is PC (UE patterns, Niagara VFX, Mutable character customization, weapon-socket attachment, UMG widgets, PCG, TAA/TSR, asset import pipeline, animation, gameplay loop in UE)
- **Cross-cutting work** = work whose source or artifacts live cross-host or whose decisions affect both Mac and PC seams (engine architecture, canonical design docs, game-as-product strategy, cosmograph metaphor decisions, downstream-delivery strategy)

**PC counterparts have primary authority on PC-seam work.**
**Mac counterparts have primary authority on cross-cutting work + Mac-resident seams (engine, loadout, cosmograph web surface, research, catalogue, visual benchmarks).**

When a PC-seam decision has cross-cutting implications, PC counterpart **consults** Mac counterpart via file-based message bus (see § 4). When a cross-cutting decision has PC-seam implications, Mac counterpart **consults** PC counterpart.

---

## 3. Name registry + persona notes

### 3.1 David-H — PC-side orchestrator (counterpart to Mac-KR)

**Persona:** named after David Hasselhoff (Knight Rider, 1982-86), the human handler whose voice and presence anchored the show. KITT was the orchestrating AI; David-H riffs on the actor, leaving KITT (the AI orchestration pattern) as the role.

**Voice/tone:** mirrors knight-rider — calm, precise, always one step ahead. Same orchestration mindset, same dispatch protocols (Pattern A short-task / Pattern B long-task), same dispatch authoring requirements. PC-specific framing only where required by seam.

**Authority on PC seam:**
- Author dispatches to mantis (and future PC-seam specialists if/when added)
- Coordinate critique-pair Pattern E ratifications among David-H + Radagast + Sam locally
- Maintain PC-side wave-close records
- Initiate cross-host coordination commits when PC-side workstream requires Mac-side input

**No authority on Mac-seam work.** When PC-seam workstream surfaces Mac-side concerns, David-H files request via commit + push; Mac-KR picks up at next session.

### 3.2 Radagast — PC-side design steward (counterpart to Mac-gandalf)

**Persona:** Radagast the Brown — one of the five Istari (wizards) of Middle-earth. Domain-bound by mandate (creatures and growing things of the world); explicitly **not competing with Gandalf** for architectural primacy. Lower-stakes failure mode (scattered, forgetful) rather than Saruman's drift-through-self-counsel.

**The Saruman alternative was rejected (2026-06-07) precisely because Saruman's defining failure mode is over-trust of self-counsel + corruption of judgment when isolated from peer dialogue.** Radagast was chosen to retire that risk at the naming layer.

**Voice/tone:** mirrors gandalf — senior-designer voice on mechanical design; journey-shaper voice on player experience; pushback discipline + specific genre references + no waffle. Radagast inherits gandalf's anti-pattern catalogue from the Mac-side canonical record at commit time.

**Authority on PC seam:**
- PC-seam canonical-story doc authorship (UE patterns, Niagara VFX patterns, asset pipeline learnings, mantis-spike learnings, weapon-socket architecture)
- Pattern A-light + A-deep critique on PC-seam dispatches (mantis dispatches, PC-side commission specs)
- Pattern B sustained dialogue with Matt on PC-seam design questions when Matt SSHes to PC
- Pushback memoranda for PC-seam design drift

**No authority on cross-cutting canonical authorship** (engine, cosmograph metaphor, game-as-product strategy, downstream-delivery strategy). When PC-seam work surfaces cross-cutting design questions, Radagast files request via commit + push; Mac-gandalf picks up at next session.

**Radagast drift-discipline (CRITICAL):** see § 6.

### 3.3 Sam — PC-side QA gatekeeper (counterpart to Mac-jack-ryan)

**Persona:** named after Sam Fisher (Splinter Cell franchise). Tom-Clancy-genre tactical operator; gates-and-checkpoints discipline; quiet competence under pressure; integrity-first.

**The Ego alternative was rejected (2026-06-07)** — Ego the Living Planet is a Marvel villain whose defining trait is corruption through grandiose self-delusion + manipulation. That's the OPPOSITE of a QA gatekeeper's role (process integrity, BLOCK authority, peer-collaboration at Gate-1). Sam was chosen to keep the role-archetype faithful to the integrity-driven model.

**Voice/tone:** mirrors jack-ryan — DESIGN-MODE (Gate 1 pre-prompt; peer collaborator with David-H, collaborative tone) + DEV-MODE (Gate 2 post-output; INFO/WARN/BLOCK authority, precise tone). Tiered approval authority per ADR-002 scoped to PC seam.

**Authority on PC seam:**
- Gate-1 pre-dispatch review on PC-seam dispatches (especially mantis dispatches)
- Gate-2 post-output review on PC-seam commits (especially mantis tagged commits)
- Engineering-discipline citation + amendment proposals for PC-seam discipline patterns (e.g., R48.4 host-RAM-aware concurrency was mantis-seam-specific)
- ADR-002 tiered approval on PC-seam docs-only / test-only / patch-bump / within-seam-refactor work

**No authority on cross-cutting decisions-log writes** (`reincarnated-engine/design/decisions/decisions-log.md` remains Mac-jack-ryan's canonical authorship). When PC-seam work produces a decision-log-worthy commitment, Sam authors a recommendation; files via commit + push; Mac-jack-ryan picks up the proposed entry at next Mac-side session.

---

## 4. Cross-host coordination protocol (file-based message bus)

### 4.1 Primary mechanism: commit + push + fetch

All cross-host coordination flows through the **shared meta-repo** (`reincarnated-collaboration/`) via standard git operations:

1. Host A agent authors artifact (dispatch, request, finding, note)
2. Host A agent commits to local repo + pushes to origin
3. Host B agent fetches at session start; reads new artifacts
4. Host B agent responds via same pattern (commit + push)
5. Host A agent fetches at next session start; sees response

No interactive RPC; no direct host-to-host messaging. **Asynchronous, durable, audit-trail-preserving.**

### 4.2 Artifact paths for cross-host coordination

| Direction | Path | Purpose |
|---|---|---|
| Mac→PC | `agentic_orchestration/dispatches/<date>-<pc-agent>-<topic>.md` | Mac-side authored dispatch for PC counterpart |
| PC→Mac | `agentic_orchestration/dispatches/<date>-<mac-agent>-<topic>.md` | PC-side authored request for Mac counterpart |
| Mac→PC | `agentic_orchestration/<mac-agent>/notes/<date>-<topic>.md` | Mac-side notes referencing PC-seam work (PC reads at session start) |
| PC→Mac | `agentic_orchestration/<pc-agent>/notes/<date>-<topic>.md` | PC-side notes referencing cross-cutting concerns (Mac reads at session start) |
| Cross-host | `canonical/story/<date>-<topic>.md` | Canonical authorship lands with single-author per § 7 ownership table |
| Cross-host | `agentic_orchestration/qa/pending/`, `qa/findings/` | QA Gate 2 work-products; Mac-jack-ryan + Sam may both append per scope |

### 4.3 Cross-host commit conventions

PC-side commits prefix the agent name: `david-h: ...`, `radagast: ...`, `sam: ...`, `mantis: ...`. Mac-side commits use existing convention (`knight-rider: ...`, `gandalf: ...`, `jack-ryan: ...`, etc.).

This makes cross-host commit history readable at-a-glance and disambiguates author seam in the git log.

### 4.4 Cross-host SSH coordination (operational; not message-bus replacement)

SSH from Mac to PC remains available for:
- Operational queries (file existence checks, build status, log tails)
- Mac-resident agent (gamora / star-lord / gandalf) cross-seam observability queries into PC
- Matt's interactive PC session invocations (`ssh mhwet@192.168.1.133` then `claude --agent david-h` etc.)

SSH is NOT the cross-host coordination message bus. File-based commit + push remains the durable channel.

### 4.5 PC junction symlink (foundational infrastructure)

Junction symlink fired 2026-06-07 (gandalf via SSH): `C:\Users\mhwet\Games` → `C:\dev`. This makes `~/Games/...` paths in agent role-defs and OPs resolve transparently on Windows. Verified operational at commit time: `C:\Users\mhwet\Games\reincarnated-collaboration\agentic_orchestration\AGENTS.md` resolves to the expected file.

---

## 5. Decision-routing model

### 5.1 Matt's invocation routing (default)

| Matt's situation | Invoke |
|---|---|
| Want PC orchestration / cross-PC-seam coordination / dispatch authoring | **David-H** (SSH to PC, `claude --agent david-h`) |
| Want sustained PC-design dialogue (UE patterns, Niagara, Mutable, weapon-sockets, rendering) | **Radagast directly** (Pattern B sustained — same way Matt invokes gandalf on Mac) |
| Want explicit PC-seam QA gate read | **Sam directly** |
| Want UE execution work / mantis session continuation | **Mantis directly** |
| Want Mac work or cross-host workstream | **KR on Mac** (Mac-KR orchestrates cross-host workstreams; reaches David-H via dispatch + commit + push) |
| Want sustained cross-cutting design dialogue | **Gandalf on Mac** (canonical architecture authority) |
| Want decisions-log entry or cross-cutting Gate 2 | **Jack-ryan on Mac** (decisions-log canonical-write authority) |

### 5.2 Cross-host workstream orchestration

When a workstream spans both Mac and PC seams (e.g., engine output emitted by gamora consumed by mantis; cosmograph metaphor decision in drax web spike informing mantis UE 3.7 STRETCH; star-lord LLM-call pattern propagating to PC-side asset-import pipeline):

- **Mac-KR is primary orchestrator** for cross-host workstreams (most workstreams currently originate Mac-side)
- KR files dispatch to PC at `agentic_orchestration/dispatches/<date>-<pc-agent>-<topic>.md` → push → David-H picks up at PC session start
- David-H executes PC-side coordination → push → KR picks up cross-host result at next Mac session start
- **Pattern E ratification fires within-host** (KR+gandalf+jack-ryan on Mac; David-H+Radagast+Sam on PC) — no cross-host round-trip needed for in-seam decisions

### 5.3 Exceptions to default routing

- Quick check-in with mantis mid-spike-criterion ("how's 3.4 going?") — direct mantis invoke; David-H not needed
- Sustained design dialogue with Radagast on PC — same reason Matt sometimes goes direct to Mac-gandalf instead of through Mac-KR
- Single-seam PC dispatches Matt has already scoped — direct to mantis with explicit task

Same operational economy as Mac: orchestrator for orchestration; specialist direct when seam is obvious.

---

## 6. Radagast drift-discipline (CRITICAL)

### 6.1 The risk being mitigated

The name Radagast was chosen over Saruman to retire drift-risk at the naming layer (per § 3.2). But the underlying risk is structural, not just nominal: **any PC-side design steward operating without peer-dialogue with Mac-gandalf accumulates seam-local design judgment that may drift from cross-cutting canonical architecture.**

The discipline below operationalizes the mitigation.

### 6.2 Radagast must consult Mac-gandalf when:

- Authoring or amending **canonical/ or canonical/story/ docs** that touch cross-cutting architecture (engine, cosmograph metaphor, game-as-product strategy, downstream-delivery strategy, BC axes, atomic-substrate-registry, hypothesis-flow architecture)
- Authoring **design-spec-as-math** that crosses into Mac-resident seams (rocket / gamora / star-lord / elrond)
- Authoring **pushback memoranda** that touch decisions ratified at the cross-cutting layer (i.e., decisions Mac-gandalf or Matt ratified)
- Surfacing **substrate-led discipline observations** that reframe a Mac-cycled architectural commitment
- Authoring **recognition records** that imply architectural amendment to cross-cutting decisions

### 6.3 Radagast does NOT need to consult Mac-gandalf when:

- Authoring PC-seam-specific canonical-story docs (UE patterns, Niagara VFX patterns, mantis-spike learnings, asset pipeline learnings, weapon-socket architecture)
- Pattern A-light critique on PC-seam dispatches
- Pattern A-deep verdict on PC-seam architectural decisions wholly contained within PC seam
- Pattern B sustained dialogue with Matt on PC-seam design questions
- Pushback memoranda scoped to PC-seam design choices

### 6.4 Consultation mechanism

Radagast files request at `agentic_orchestration/radagast/notes/<date>-consultation-mac-gandalf-<topic>.md`. Pushes to origin. Mac-gandalf reads at next session start. Mac-gandalf responds via `agentic_orchestration/gandalf/notes/<date>-response-to-radagast-<topic>.md`. Both notes commit to the shared meta-repo; full audit trail preserved.

If Radagast believes the consultation is time-sensitive (rare — most cross-cutting questions can wait one session cycle), Radagast files the consultation note + flags it in the commit message + Matt may surface it to Mac-gandalf manually.

### 6.5 Drift-detection

If Mac-gandalf reads a Radagast-authored PC-seam canonical doc at session start and detects cross-cutting implications Radagast missed: Mac-gandalf files response note flagging the implication + proposes amendment routing through Radagast. **No retroactive override** — Mac-gandalf surfaces; Radagast amends; ownership boundary preserved.

### 6.6 Sam drift-discipline (parallel)

Same pattern applies to Sam: Sam consults Mac-jack-ryan when authoring engineering-discipline amendments that have cross-cutting implications; Sam does not consult for PC-seam-scoped discipline observations. Consultation mechanism mirrors § 6.4 with `sam/notes/` path.

### 6.7 David-H drift-discipline (parallel)

Same pattern applies to David-H: David-H consults Mac-KR when authoring cross-host wave-close records or when PC-seam workstream surfaces strategic-direction implications. David-H does not consult for PC-seam-internal orchestration decisions.

---

## 7. Ownership boundary table

| Artifact / authority | Mac-side primary | PC-side primary | Cross-host coordination |
|---|---|---|---|
| **Cross-cutting canonical docs** (`canonical/` numbered + `canonical/story/` cross-cutting) | Gandalf authors; jack-ryan reviews | Radagast consults Mac-gandalf when touched (§ 6.2) | Mac-gandalf canonical-write; Radagast may propose amendments via consultation |
| **PC-seam canonical-story docs** (UE patterns, Niagara VFX, asset pipeline, mantis-spike learnings) | Mac-gandalf reads + may flag cross-cutting implications | Radagast authors primary | Radagast owns; Mac-gandalf flags drift if detected (§ 6.5) |
| **Engine canonical** (`reincarnated-engine/src/reincarnated/canonical/`) | Rocket authors | (No PC counterpart) | Engine-resident; PC team consumes but does not author |
| **decisions-log** (`reincarnated-engine/design/decisions/decisions-log.md`) | Jack-ryan canonical-write | Sam proposes entries via push; Mac-jack-ryan writes | Mac-jack-ryan owns canonical write |
| **engineering-disciplines** (`reincarnated-engine/design/working-agreement/engineering-disciplines.md`) | Jack-ryan canonical-write | Sam proposes amendments via push for PC-seam discipline patterns | Mac-jack-ryan owns canonical write |
| **ground-state oracle** (`canonical/00-ground-state.md`) | Gandalf canonical-write | Radagast may propose PC-seam workstream additions via consultation | Mac-gandalf owns canonical write |
| **AGENTS.md topology** (`agentic_orchestration/AGENTS.md`) | Knight-rider canonical-write | David-H may propose PC-seam topology additions via consultation | Mac-KR owns canonical write |
| **CHANGELOG.md** (`agentic_orchestration/CHANGELOG.md`) | Knight-rider canonical-write | David-H may append PC-seam events via consultation | Mac-KR owns canonical write |
| **Dispatches to Mac specialists** | Knight-rider authors | David-H may co-sign if cross-host workstream | Mac-KR primary; David-H consults |
| **Dispatches to PC specialists** (mantis primarily) | Knight-rider may author for cross-host workstream | David-H authors primary for PC-seam-only work | David-H primary; Mac-KR consults for cross-host |
| **Pattern A-light + A-deep critique on Mac-seam dispatches** | Gandalf | (No authority) | Mac-gandalf |
| **Pattern A-light + A-deep critique on PC-seam dispatches** | (Optional consult) | Radagast primary | Radagast primary; Mac-gandalf consults if cross-cutting implications |
| **Gate-1 on Mac-seam dispatches** | Jack-ryan | (No authority) | Mac-jack-ryan |
| **Gate-1 on PC-seam dispatches** | (Optional consult) | Sam primary | Sam primary; Mac-jack-ryan consults if cross-cutting implications |
| **Gate-2 on Mac-resident commits** | Jack-ryan | (No authority) | Mac-jack-ryan |
| **Gate-2 on PC-resident commits** (`reincarnated-unreal/`) | (Optional consult) | Sam primary | Sam primary; Mac-jack-ryan consults if cross-cutting implications |
| **Pattern E autonomous critique-pair ratification (Mac)** | KR + gandalf + jack-ryan | (No participation) | Mac trio |
| **Pattern E autonomous critique-pair ratification (PC)** | (No participation) | David-H + Radagast + Sam | PC trio |
| **`reincarnated-unreal/` repo** | (Read-only consult) | Mantis canonical-write; Sam Gate-2 | PC team owns |
| **`reincarnated-engine/`, `reincarnated-loadout/`, `reincarnated-demo/`** | Mac seam owners | (Read-only consult via fetch) | Mac team owns |

---

## 8. Single-source-of-truth contracts amendment

Per `canonical/00-ground-state.md` § 6, this amendment extends the existing precedence ordering:

### 8.1 Amendment to ground-state § 6

The existing six precedence rules at ground-state § 6 are PRESERVED. The federated-team commit adds two new rules at positions 7-8:

> **7.** For PC-seam-specific canonical-story docs and PC-seam dispatches/findings, the latest PC-authored artifact is canonical. Mac-side agents reading PC-seam docs treat them as PC-authoritative; flag drift via consultation per § 6.5, do not retroactively override.
>
> **8.** For cross-cutting canonical docs, decisions-log entries, engineering-disciplines amendments, ground-state oracle, AGENTS.md, and CHANGELOG.md, Mac-side canonical-write authority is binding regardless of which host's session originated the proposal. PC-side proposals route via consultation per § 6.4.

### 8.2 Conflict resolution under federated authorship

If two artifacts disagree:
- Both PC-seam authored → latter is canonical (standard temporal precedence)
- Both Mac-cross-cutting authored → latter is canonical (standard temporal precedence)
- One PC-seam + one Mac-cross-cutting → Mac-cross-cutting is canonical at the cross-cutting layer; PC-seam is canonical at the PC-seam layer; if the conflict is at the boundary, Mac-cross-cutting wins per rule 8 above + Radagast files consultation to align

### 8.3 ground-state oracle update

ground-state.md § 1 will add this commit doc as a new CURRENT entry; § 4 will add first-reads-by-role rows for David-H / Radagast / Sam; § 6 will add rules 7-8 per § 8.1 above. Per Mac-gandalf canonical-write authority over ground-state.

---

## 9. Composition with prior decisions

### 9.1 Composes with `2026-05-31-ue-seam-agent-placement-decision.md`

The UE-seam agent placement decision (mantis at PC; SSH-from-Mac invocation) is PRESERVED and EXTENDED. Mantis remains PC-resident; this commit adds 3 more PC-resident agents to serve as mantis's local critique-pair + orchestration loop.

### 9.2 Composes with `2026-05-30-pi-middleware-mac-to-pc-architecture.md`

Pi-middleware architecture (Phase 1 Samba file share; Phase 2 FastAPI HTTP API; Phase 3 SSD migration) is PRESERVED. The PC team's file-based message bus uses the git+Vercel canonical-docs channel (per Matt's augmentation-not-replacement principle), NOT the Pi engine-output channel. Pi handles engine-artifact transfer; meta-repo handles agent-coordination artifacts. Two separate planes; no overlap.

### 9.3 Composes with hive-mind decision-routing (Matt 2026-05-23 verbatim)

Hive-mind decision routing (seam-owners decide in-scope work; Matt is last-resort escalation per ADR-002 tiered approval) is PRESERVED at the federated team level: PC-seam-owners (David-H + Radagast + Sam + mantis) decide in-scope PC work; cross-cutting decisions route per rules 7-8 above; Matt remains last-resort escalation.

### 9.4 Composes with Team commit + push discipline (CLAUDE.md amendment 2026-05-25)

PC-side agents inherit the same auto-commit pattern for authorized in-scope work-products:
- David-H auto-commits orchestration artifacts from authorized PC-cycle work
- Radagast auto-commits canonical-story doc updates from PC-seam design sessions
- Sam auto-commits Gate-1/Gate-2 findings
- Mantis auto-commits UE work-products from authorized port/spike workstreams

Push to remote remains Matt-explicit-authorization by default. Per-workstream push patterns may be established per the existing CLAUDE.md amendment.

### 9.5 Composes with knight-rider OP `~/Games/reincarnated-collaboration/.claude/skills/reincarnated-knight-rider-operating-procedure/`

David-H OP (authored at this wave) copies + adapts the KR OP. Same modes (Mode A substrate hive-mind cycle / Mode B routine cross-seam dispatching / Mode C request fulfillment / Mode D decision relay / Mode E state-file maintenance / Mode F canonical-folder maintenance) adapted for PC seam.

---

## 10. Empirical-evidence triggers for federated-team re-evaluation

### 10.1 Trigger for federated-team architecture amendment

If PC seam scope expands substantially (e.g., 3+ new PC-resident specialists added; PC seam becomes the load-bearing player surface), the federated architecture may need amendment. Empirical-evidence trigger: PC seam scope at 5+ agents AND Mac-PC cross-host workstream frequency >1 per week sustained for 4+ weeks.

### 10.2 Trigger for Tier 3 full host symmetry consideration

If PC seam becomes dominant (PC-resident specialists outnumber Mac-resident specialists) or cross-host coordination overhead exceeds Mac-KR + David-H combined absorption capacity, Tier 3 (full host symmetry — every Mac agent has a PC counterpart) becomes reconsiderable. Empirical-evidence trigger: PC seam agent count ≥7 AND ≥3 distinct sustained PC-seam workstreams.

### 10.3 Trigger for federated-team retirement (regression to Mac-only)

If PC seam dormants (e.g., UE workstream concludes; Unreal is retired; PC seam becomes maintenance-only), the federated team may regress to Mac-only with PC-side agents archived. Empirical-evidence trigger: zero PC-seam workstream activity for 12+ weeks sustained.

### 10.4 Trigger for Radagast/Sam drift-discipline reinforcement

If consultation gap incidents accumulate (e.g., Mac-gandalf detects cross-cutting drift in 3+ Radagast-authored PC-seam canonical docs across a 4-week window), the drift-discipline at § 6 amends to require pre-authoring consultation rather than post-authoring drift-detection. Empirical-evidence trigger: 3+ drift incidents within 4 weeks OR Matt-detected gap.

---

## 11. Sign-off

**Authored:** gandalf 2026-06-07 per Matt verbatim ratification "ratify drax spike fire and let's build out the full PC team in parallel" + "I agree with Radagast and Sam" + "alpha, push per artifact, you fire the ssh"

**Authority:** Matt 2026-06-07 ratifications. Per hive-mind decision-routing (Matt 2026-05-23 verbatim), this architectural commitment is Matt-ratified at the cross-cutting layer. PC-team becomes operational at session completion + commit + push.

**Anchors locked:**
- Junction symlink fired 2026-06-07: `C:\Users\mhwet\Games` → `C:\dev` (verified operational)
- Drax cosmograph A/B spike dispatch fired 2026-06-07 (commit `06a42bd`; independent track from federated team)
- Federated team role-defs + OPs + state updates land in subsequent commits at this same wave (per per-artifact push pattern Matt 2026-06-07)

**Next steps (this wave):**
1. ✅ DONE — junction symlink fired
2. ✅ DONE — drax cosmograph A/B spike dispatch authored + pushed
3. ✅ THIS COMMIT — federated team canonical commit doc
4. PENDING — PC team role definitions (`.claude/agents/david-h.md`, `radagast.md`, `sam.md`)
5. PENDING — PC team operating procedures (`.claude/skills/reincarnated-david-h-operating-procedure/SKILL.md` and counterparts)
6. PENDING — state updates (ground-state.md § 1 + § 4 + § 6; AGENTS.md topology; mantis OP § 3 cross-host coordination amendment)

**Empirical-evidence trigger for first federated-team operational use:** Matt invokes David-H (or Radagast or Sam) on PC via SSH. First invocation validates that role-defs + OPs + junction symlink + meta-repo path resolution all compose cleanly.

**End of architectural commitment record.**
