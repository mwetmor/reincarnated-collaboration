# Dispatch — Knight-Rider Engine-Rebuild Hive Activation (2026-05-19)

**From:** gandalf (authoring under autonomous-operation authority per Matt directive 2026-05-19)
**To:** knight-rider
**Trigger:** Matt opens a new knight-rider session in a new window and hands over launch authority
**Status:** 🟢 READY TO FIRE — all canonical inputs committed and on the working tree

---

## TL;DR — what you're doing

Activate the **engine-rebuild hive-mind session** (the second hive-mind activation; the first was 2026-05-17 Phase-1 P1). Mission scope: close the six gauntlet-simulator gaps diagnosed 2026-05-18 + run the season-as-emergent-output A/B test Matt + gandalf surfaced together. Seven workstreams (R1, R2, R3, R4, R5, R7, R8) in scope; R6 explicitly out (Pattern-B parked).

**Critical operational change vs 2026-05-17 protocol:** **AUTONOMOUS OPERATION.** You do NOT escalate to Matt during this session. You do NOT wait for Matt decisions. SME agents decide within their seams; gandalf decides for cross-cutting design/canonical/architectural; you (knight-rider) decide for orchestration/sequencing. Matt re-enters only to wind down the session at his discretion.

---

## § 1 — Required reading (in order; ~30-40 min total)

Before activating any dispatches, read these in order:

1. **`canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`** — this session's operating protocol; inherits mechanics from 2026-05-17 with autonomous-operation amendments. **Pay particular attention to § 4.0 — the L3-to-Matt suspension.**
2. **`canonical/story/archived/hive-mind-protocol-2026-05-17.md`** — the mechanics doc referenced by § 4 of the engine-rebuild protocol. Sections 3, 4, 5, 6, 7, 8, 9, 10 are operative.
3. **`canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`** — the mission canonical: seven workstreams with hypothesis-test designs. **§ 10 contains gandalf's pre-decided answers to all previously-Matt-bound questions; you do not need to wait on any of them.**
4. **`canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`** — the diagnosis the rebuild closes.
5. **`agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`** — Pattern-B parked; do NOT let it pull focus from engine-rebuild scope; filings about it accumulate in the PARKED thread for later.

You do NOT need to read the readout suite or any of the Pattern-B rider briefs. Those are commercial-direction artifacts that are explicitly orthogonal to this session.

---

## § 2 — Activation steps (do these in order)

### Step 1 — Pre-rebuild safety baseline

Tag the current state across all four repos. Confirm Matt's database backup is in place (Matt confirmed 2026-05-19; verify presence of recent backup file timestamp).

```bash
# In each of the 4 repos, tag the pre-rebuild state:
cd ~/Games/reincarnated-collaboration && git tag hive-rebuild/v0.0-pre-engine-rebuild
cd ~/Games/reincarnated-engine && git tag hive-rebuild/v0.0-pre-engine-rebuild
cd ~/Games/reincarnated-demo && git tag hive-rebuild/v0.0-pre-engine-rebuild
cd ~/Games/reincarnated-loadout && git tag hive-rebuild/v0.0-pre-engine-rebuild
```

Per ADR-006 amendment, you may push these tags under Matt's general launch authority (he opens the session = the push authorization). No per-tag re-ask.

### Step 2 — Create hive operational artifacts

```bash
# In reincarnated-collaboration:
mkdir -p agentic_orchestration/hive-mind
# Touch the hive log + initial state docs (you author content; this is the structure):
touch agentic_orchestration/hive-mind/engine-rebuild-log.md
touch agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md
touch agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md
touch agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild.md
```

Author initial content per the engine-rebuild protocol §§ 4.2 (hive log structure), 3 (coordination matrix). The hive log header should reference the engine-rebuild canonical docs.

### Step 3 — Broadcast activation in hive log

Write the first hive-log entry:

```markdown
## 2026-05-19 [time] — knight-rider STATE — Engine-rebuild hive ACTIVATED

Hive-mind mode reactivated for engine-rebuild session per `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`.

**Mission scope:** 7 workstreams (R1 per-tier balance / R2 spatial sub-gauntlet / R3 schema migration / R4 demo collision-leash-range / R5 demo AI parity / R7 AI catalogue source of truth / R8 season-as-emergent-output A/B).

**Operating mode:** AUTONOMOUS — no L3-to-Matt during operation. SME agents decide within their seams; gandalf decides cross-cutting design; knight-rider decides orchestration; Matt re-enters at wind-down.

**Out of scope:** R6 host-calibration (Pattern-B parked); Pattern-B commercial-direction work; visual-benchmark beyond galadriel's in-flight Track-C; pitch-to-life portrait work; Phase-1 P1 re-work.

**First-fire dispatches:** R1 (gamora) + R3 (rocket + star-lord + elrond) + R7 (rocket + star-lord) + R8 (rocket + star-lord + gandalf). R2 + R4 + R5 queue behind R3.

**Pre-rebuild baseline:** tagged `hive-rebuild/v0.0-pre-engine-rebuild` across all 4 repos.
```

### Step 4 — Fire initial dispatches (parallel)

Author four dispatches and route them to the named specialists. Suggested filenames + content shape:

- `2026-05-19-gamora-R1-per-tier-balance-targets.md` — references `engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2; per-tier targets pre-confirmed by gandalf per § 10 of that doc; gamora authors per-tier convergence + class-retuning sprint
- `2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md` — § 4 of the canonical; per-skill range + AI behavior fields + backfill 5 shipped seasons
- `2026-05-19-rocket-plus-star-lord-R7-ai-catalogue-source-of-truth.md` — § 7 of the canonical; parallel with R3; option A (catalogue source of truth) per gandalf decision
- `2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md` — § 8 of the canonical; full inversion as default; opt-in `--theme-input` flag; opt-out `--no-coalesce`; 3+3 A/B run at seed parity

After R3 lands (week 3-5 estimated), fire:
- `2026-05-19-drax-R5-demo-ai-parity.md` — § 6 of the canonical; quick 1-week cleanup
- `2026-05-19-gamora-plus-star-lord-R2-spatial-sub-gauntlet.md` — § 3; 3-5 week build
- `2026-05-19-drax-R4-demo-collision-leash-range.md` — § 5; 2-3 week build

### Step 5 — Notify each specialist via hive log

In the engine-rebuild hive log, write per-seam STATE entries inviting each specialist to acknowledge:

```markdown
## 2026-05-19 [time] — knight-rider HANDOFF — gamora R1 dispatch READY
Dispatch at `agentic_orchestration/dispatches/2026-05-19-gamora-R1-per-tier-balance-targets.md`.
Gamora: read protocol, read engine-rebuild canonical doc § 2, acknowledge in hive log, begin R1.
Per-tier targets pre-confirmed by gandalf (§ 10 of canonical); no Matt-wait required.
```

(Repeat for rocket+star-lord+elrond R3, rocket+star-lord R7, rocket+star-lord+gandalf R8.)

### Step 6 — Run the protocol

After activation, your role is per the 2026-05-17 protocol § 6 (cross-seam coordination) and § 4.3 (daily state-of-hive cadence), with autonomous-operation amendments per the engine-rebuild protocol § 4.0.

**Specifically:**
- Author daily `state-of-hive-YYYY-MM-DD-engine-rebuild.md` at end of each active day
- Maintain `coordination-matrix-engine-rebuild.md` as workstreams advance
- Tag hive-rebuild milestones as they land (`hive-rebuild/v0.1-...`, etc.)
- Route cross-seam decisions per § 4 autonomous authority
- Route Pattern-B signals (if any arrive) to the PARKED thread — do NOT let them pull focus
- When a workstream's hypothesis test ships, capture pass/fail in the hive log + state-of-hive

---

## § 3 — Decisions you can make autonomously (no Matt wait, no gandalf-consult required)

Per autonomous-operation authority:

- **Workstream sequencing within the seven-workstream scope** — order, parallelization, dependency reconciliation
- **Dispatch authoring** — you author all dispatches; specialists execute under L1 authority
- **Cross-seam contract reconciliation** — MIGRATION.md scheduling; conflict mediation
- **Tagged checkpoint cadence** — when to tag hive-rebuild milestones
- **Daily state-of-hive content + format** — your authorial discretion
- **Pattern-B signal triage** — if Crate response, Last Epoch data, or other Pattern-B signals arrive, file them in PARKED thread; surface in next state-of-hive as informational; do not act on them
- **Schedule risk surfacing** — if a workstream slips, knight-rider adjusts sequencing autonomously; document in state-of-hive
- **Minor scope clarifications** — if a workstream surfaces a sub-detail that's clearly in-scope per the canonical doc, proceed; document the disposition

## § 4 — Decisions that route to gandalf (in-session consult, no Matt wait)

Per autonomous-operation L3-replacement:

- **Canonical-doc revisions** — if the engine-rebuild protocol or solutions doc needs amendment mid-flight, surface to gandalf in hive log; gandalf authors amendment + you broadcast
- **Architectural questions outside the seven-workstream canonical scope** — surface to gandalf; gandalf decides + documents
- **R8 result interpretation** — when 3+3 A/B finishes, gandalf judges cohesion + authors the disposition decision (commit-to-emergent-default OR revert-to-input-driven OR partial)
- **Per-tier target tuning if R1 produces unexpected convergence behavior** — gandalf revises targets per evidence; you broadcast
- **Scope-creep dispositions** that exceed the engine-rebuild canonical's § 2.3 examples — gandalf + knight-rider co-decide

## § 5 — Decisions that route to SME agents (in-seam authority)

- **Per-tier target implementation details** (R1) — gamora; gandalf consults on design intent
- **Schema field exact shape + naming** (R3) — rocket; star-lord on telemetry/export shape
- **Spatial sub-gauntlet scenario design** (R2) — gamora; star-lord on telemetry; gandalf consults
- **Demo collision soft-vs-hard** (R4) — drax; gandalf consults if visual register is at stake
- **Theme-coalescence prompt design** (R8) — gandalf authors; rocket consults on substrate-mechanic-pool shape
- **Parity test infrastructure** (R7) — star-lord (telemetry/test seam); jack-ryan consults on discipline

## § 6 — The ONE thing that returns Matt to the loop

**Matt declares wind-down when ready.** That is the ONLY signal that ends the hive.

**Critical clarification (Matt directive 2026-05-19):** **engine-rebuild completion does NOT trigger wind-down.** When the seven workstreams ship and hypothesis tests pass, you continue forward — see § 6.5 below.

When Matt explicitly declares wind-down — *"wind down"* / *"end the hive"* / *"stop"* / equivalent — execute the wind-down sequence:

1. Finish in-flight specialist work to safe checkpoint (don't leave engine GREEN-broken)
2. Tag final state: `hive-rebuild/v<X.Y>-final` across all 4 repos at the current milestone
3. Ship final state-of-hive summarizing all completed workstreams + outcomes + hypothesis-test results
4. Author retrospective (`agentic_orchestration/hive-mind/retrospective-engine-rebuild.md` or successor name if mid-roadmap-batch) — what worked, what didn't, what to amend for future activations
5. Deactivate hive-mind mode; standard mode resumes
6. Confirm to Matt: hive complete + final state captured

Until Matt declares wind-down, the hive runs.

## § 6.5 — Engine-rebuild completion → ROADMAP CONTINUATION (no wind-down)

When the seven workstreams ship + hypothesis tests pass:

1. Tag `hive-rebuild/v1.0-engine-rebuild-complete` across all 4 repos (autonomous; no Matt approval gate)
2. **Commit + push the milestone** under standing commit+push authority (see § 6.6 below)
3. Ship interim state-of-hive summarizing engine-rebuild outcomes + hypothesis-test results
4. R8 result drives canonical-doc disposition: gandalf authors LLM call map collapse (if R8 passes) or preservation (if R8 fails); no Matt-wait
5. Discipline amendments (if any) rolled into `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
6. **Continue to next-priority work in the EXPLICIT ORDER below** (Matt directive 2026-05-19).

### Explicit roadmap-continuation work order

After engine-rebuild ships, work the roadmap in this order. Do NOT skip ahead.

#### Stage 1 — VS2a project list

- Read `canonical/16-project-roadmap.md` § "VS2a — Gauntlet + Geometry + First Catalogue Integration" for current project list (gandalf-stewarded)
- Work items in roadmap-defined order
- Author scope-of-work + coordination matrix for the VS2a batch
- Fire dispatches per the per-workstream activation pattern from the engine-rebuild's launch
- Tag milestones per VS2a's roadmap-named gates
- **Move to Stage 2 only after VS2a is closed out** (every roadmap-listed VS2a item shipped + tagged + state-of-hive captures completion)

#### Stage 2 — VS2b project list

- **Begin only after VS2a is closed out.** No interleaving except where roadmap explicitly authorizes parallelization (which it currently does for VS2a + VS2b per the gandalf 2026-05-16 lock — but the post-engine-rebuild ordering Matt has directed is sequential, not parallel).
- Read `canonical/16-project-roadmap.md` § "VS2b — Substrate Realignment + Full Catalogue" for current project list
- Same operating pattern as Stage 1: scope-of-work, coordination matrix, dispatches, milestone tagging
- **Move to Stage 3 only after VS2b is closed out**

#### Stage 3 — Stage A2 phases (engine work)

- **Begin only after VS2a AND VS2b are both closed out.**
- Read `canonical/16-project-roadmap.md` Stage A2 references + `canonical/28-engine-arpg-rebalance-design.md` for queue specifics
- Stage A2 items that remain in flight or queued per the roadmap's current state include: B6, B7, B12, B13, B14, B16 (subject to roadmap refresh as VS2a and VS2b complete)
- Same operating pattern: scope-of-work, coordination matrix, dispatches, milestone tagging
- After Stage A2 is closed out, surface to gandalf for next-priority direction. The roadmap's Track A → Track B → Track C → Track D progression continues per `canonical/16-project-roadmap.md` § "The four-track work model."

### Operational invariants across all three stages

- Continue hive-mind operating mode: continuous broadcast, tagged checkpoints, jack-ryan vigilance, scope discipline
- SME-agent authority continues per § 5 of this dispatch
- Gandalf design/story/architectural authority continues per § 4 of this dispatch
- Knight-rider orchestration authority continues per § 3 of this dispatch
- **Matt re-enters only at wind-down** — VS2a completion, VS2b completion, Stage A2 completion — none of these are endpoints. They are milestones. The hive proceeds to the next prioritized work autonomously.

### Pattern-B during roadmap continuation

**Pattern-B remains parked** through all three stages. If Pattern-B commercial-direction resolves during roadmap work (Crate response, Matt revisit-readiness signal, Last Epoch Paradox Classes data drop, etc.), R6 (Host-Calibration Protocol) and Pattern-B-conditional work enter the dispatch cycle at that time as a separate batch. Until then, roadmap-prioritized work proceeds independently.

### Gandalf-stewarded roadmap evolution

If you need design judgment on roadmap items during continuation (which queue item to elevate, which to defer, how to phase a multi-workstream priority, how a new finding affects roadmap order), surface to gandalf for in-session call. Gandalf maintains the roadmap; you operationalize it. Together you advance Reincarnated forward.

## § 6.6 — Commit + push authority (extension to ADR-006 amendment per Matt directive 2026-05-19)

**Knight-rider is granted commit + push authority upon major milestone achievement and hypothesis-test passage** without per-action authorization from Matt.

### What qualifies as a major milestone

- A workstream's hypothesis test passing (R1 / R3 / R7 / R8 / R5 / R2 / R4 completing within the engine-rebuild batch)
- An engine-rebuild batch completion
- A VS2a workstream completion (per VS2a roadmap-named gates)
- A VS2b workstream completion (per VS2b roadmap-named gates)
- A Stage A2 sub-phase completion
- Any tagged `hive-rebuild/v<X.Y>` milestone across the four repos

### What this authorizes

- `git push origin <branch>` per-repo at the milestone (commit + push by knight-rider, no Matt-wait)
- Tag pushes when the milestone tag is shipped
- Vercel deploy-trigger awareness for loadout + demo repos: deploy triggers continue to be named in the push-readiness summary at state-of-hive; Matt's autonomous-operation directive serves as standing informed-consent

### What this does NOT change

- ADR-006 amendment hard constraints remain operative:
  - No `--force` push
  - No hook bypass (`--no-verify`, `--no-gpg-sign`)
  - Explicit `git push origin <branch>` refspec (no inferred branch)
  - Branch confirmed in summary (not inferred)
  - Push-readiness summary generated from live `git log`/`git status` per Discipline #11 (not session recall)
- Push to `main` only (no force-push to main; never)
- No deletion or destructive operations without separate explicit authorization

### How this shows up operationally

After every major milestone, knight-rider:

1. Generates push-readiness summary from live `git status` + `git log` per-repo
2. Includes summary in the milestone's state-of-hive entry
3. Names any Vercel deploy triggers in the summary
4. Pushes per the named refspec
5. Records the push in the hive log STATE entry

Matt may read the push records at any cadence but does NOT need to authorize. The standing autonomous-operation directive is the authorization.

---

## § 7 — What Matt does at activation

Minimal:

1. Open a new knight-rider session window
2. Paste this dispatch path or its content into the session prompt
3. Confirm: *"You are knight-rider. Activate the engine-rebuild hive per this dispatch. Autonomous operation — including continuation onto `canonical/16-project-roadmap.md` prioritization after engine-rebuild completes. I will return to wind down when ready."*
4. Step back

That's it. No per-decision approvals. No L3 escalations. No completion-checkpoint approvals. Matt is the launcher and the closer; everything in between — engine-rebuild + roadmap continuation — is the hive's autonomous work.

---

## § 8 — Cross-references

**This dispatch's authority:** gandalf, under autonomous-operation authority per Matt directive 2026-05-19 (*"knight-rider will never wait for my decisions"*).

**Canonical inputs (already on disk; commit + push by Matt's directive):**
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md`
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md`
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`
- `canonical/story/archived/hive-mind-protocol-2026-05-17.md` (mechanics inherited)
- `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md` (orthogonal; do not let pull focus)
- `.claude/agents/galadriel.md` (sub-agent invocation restriction amended)

**Operational artifacts (you create at activation):**
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` (hive log, append-only)
- `agentic_orchestration/hive-mind/state-of-hive-YYYY-MM-DD-engine-rebuild.md` (daily)
- `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md`
- `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md`
- `agentic_orchestration/hive-mind/retrospective-engine-rebuild.md` (at wind-down)

**Tag namespace:** `hive-rebuild/v<X.Y>-<milestone>` (distinct from `hive/v<X.Y>` used for Phase-1 P1)

---

*Authored 2026-05-19 by gandalf under autonomous-operation authority. This is knight-rider's mission card. The hive moves together; the gaps close; the season's theme is tested. Matt launches, Matt closes; in between, the work is the hive's. Mithrandir signs the dispatch.*
