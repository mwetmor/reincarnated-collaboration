# Next-Session Plan — Spike Continuation + PC Team-Coordination Architecture

**STATUS:** CURRENT (next-session plan; load-bearing for next gandalf invocation)
**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-06 directive: "Let's wait for today's session to complete and write this as the first task for tomorrow" + spike-continuation continuity from mantis session-1 close
**Companion:** Cosmograph Phase A close at `canonical/story/2026-06-06-cosmograph-phase-a-creation-moment-wave-close.md` (immediately-preceding cycle close); UE spike dispatch at `agentic_orchestration/dispatches/2026-06-06-mantis-ue-architecture-validation-spike.md`

---

## 0. TL;DR

Next session has TWO priority tracks:

1. **FIRST TASK** — PC team-coordination architecture decision (deferred from 2026-06-06 design call). Three-tier proposal on the table; Matt ratifies Tier 1 / Tier 2 / Tier 3 + I codify in mantis OP amendment.

2. **Spike continuation** — mantis session-2 re-engages with Matt-provided rigged FBX (Option C) + Crusader pre-rigged GLBs already on PC + remaining criteria 3.4 (Niagara) + 3.6 (TAA/TSR) + 3.7 STRETCH (3D cosmograph).

Trajectory: spike trending OVERALL GREEN with cost discipline ($3 of $20 burned). WS1 port commission scoping fires at spike close.

---

## 1. State of all sessions at wind-down

| Session | State | Wind-down disposition |
|---|---|---|
| **Gandalf (this session)** | Authored canonical pattern doc + mantis role + mantis OP + spike dispatch + supporting amendments + UE 5.7 migration test + Meshy + Crusader transfers + this plan | Commits pushed to origin; session winds down cleanly post-plan |
| **KR (Mac-side spike monitoring)** | In monitoring-quiet mode per Phase A2 / cosmograph pattern; legolas FAB survey delivered; spike fired; mantis session-1 closed | Direct KR to author session-boundary memo + wind down OR hold open across mantis re-engagements (judgment call at re-engagement) |
| **Mantis (PC-side spike execution)** | Session-1 closed cleanly; clean working tree; 3 commits landed (criterion 3.1 PASS + 3.3 PASS + 3.5 DEFERRED + cost discipline + UE 5.7 smoke test PASS) | Closed; AGENT_STATE.md authored on PC; criterion findings pushed; queue Crusader + Matt-rigged FBX for session-2 re-engagement |

---

## 2. First task — PC team-coordination architecture decision

Per Matt 2026-06-06: "We may be taking a step back with a solo dev on PC now."

### 2.1 The concerns surfaced (recap from 2026-06-06 design call)

- **Collaboration:** mantis can't easily fire gandalf/jack-ryan critique-pair locally on PC
- **Governance:** every cross-host signal requires Matt as relay
- **Speed:** Pattern E autonomous-pair ratification can't fire on PC
- **Team-learning:** lessons from cosmograph (substrate-led-at-rendering, Discipline #11 empirical, family-contraction audit) don't propagate to mantis's UE decisions
- **Pattern regression:** Phase A2 + cosmograph Phase A = 0 Matt-touches; mantis-solo = several Matt-touches already

### 2.2 Three-tier proposal (deferred to next session for ratification)

**Tier 1 — Path symmetry + sub-agent fan-out (RECOMMENDED IMMEDIATELY)**

1. Junction symlink on PC: `mklink /J C:\Users\mhwet\Games C:\dev` — `~/Games/...` paths in agent OPs work transparently on Windows
2. Mantis OP § 3 amendment codifying:
   - Sub-agent local fan-out pattern (mantis fires `Agent({ subagent_type: "gandalf" })` etc. locally on PC)
   - Cross-host coordination via commit + push + fetch (file-based message bus)
   - When to surface via terminal output vs file+push
3. Mantis re-engagement informed by amended OP

**Tier 2 — PC-resident KR scoped to UE-seam (CONDITIONAL)**

Fires if Tier 1 friction persists. PC-KR scoped strictly to UE-seam workstreams; Mac-KR handles non-UE + cross-seam. Empirical-evidence trigger: ≥3 Matt-touch friction instances OR Matt-detected team-learning gap within first month of WS1-WS2 port workstreams.

**Tier 3 — Full host symmetry (DEFERRED)**

Only if Tier 2 cross-host coordination becomes overhead Mac-KR + PC-KR can't absorb. Likely not needed near-term.

### 2.3 What gandalf does next session for first task

1. Matt confirms Tier 1 / Tier 2 / Tier 3 choice
2. If Tier 1 (recommended):
   - Junction symlink command fires from gandalf session via SSH (~30 sec)
   - Mantis OP § 3 amendment authored (~15-20 min)
   - Cross-host coordination message ready to fire to mantis at her session-2 entry
3. Estimated time: 30-45 min

### 2.4 Empirical-evidence trigger for Tier 2 re-evaluation

After WS1-WS2 port workstreams accumulate ~1 month of execution data, gandalf audits Matt-touch frequency + team-learning gap signals + reports Tier 2 recommendation to Matt.

---

## 3. Second task — Spike continuation (session 2)

### 3.1 Matt's manual Meshy rig step (Option C)

Matt completes between sessions:

1. Log into meshy.ai
2. Open each task by ID:
   - Kit A (Ember Sweeper): `019ea025-fe66-71d2-b139-2687d74b5aa5`
   - Kit B (Tide Warden): `019ea026-074b-705d-ac86-6d5f2405e8ec`
   - Kit C (Duskweaver): `019ea026-100e-7339-bc41-c57937bba495`
3. Click "Rig Character" on each → Meshy auto-detects humanoid skeleton
4. Export with "Unreal Engine" preset → FBX with Control Rig
5. Drop FBX files at `C:\dev\reincarnated-unreal\Reincarnated\Content\Characters\MeshyTest\` (mantis-suggested path)

### 3.2 Mantis session-2 priming prompt

When Matt re-fires mantis on PC:

```
Mantis session 2 — UE architecture-validation spike continuation. Session 1 closed clean (3.1 PASS / 3.3 PASS / 3.5 DEFERRED). Remaining: 3.2 (rigged FBX import + UE 5.7 verify) / 3.4 (Niagara JSON consume) / 3.6 (TAA/TSR readability) / 3.7 STRETCH (3D cosmograph viability).

Pull meta-repo: cd C:\dev\reincarnated-collaboration && git pull origin main. Pull any mantis OP amendments + Tier 1/2/3 PC team-coordination decisions Matt + gandalf locked in the prior gandalf session.

Criterion 3.2 inputs now available:
- Matt completed manual Meshy rig step on Kit A/B/C; rigged FBX at C:\dev\reincarnated-unreal\Reincarnated\Content\Characters\MeshyTest\
- Crusader pre-rigged Meshy outputs at C:\dev\reincarnated-collaboration\duskweaver\Meshy_AI_Crusader_of_the_Ember_biped\ (4 animation GLBs: Idle_03, Walking, Running, Roll_Dodge_4 — all with skin + skeleton + animation baked in)

Criterion 3.2 plan: test BOTH (Crusader primary; spike-generated FBX secondary). Crusader establishes known-good baseline; spike-generated FBX validates production pipeline empirically. Document Meshy Rig as separate 2-step pipeline (text-to-3d → rig) in criterion 3.2 finding for WS1 commission scoping.

Architectural context: legolas 2026-06-02 research recommends CC5 + Mutable as PRIMARY playable character pipeline; Meshy stays for weapons (canonical 38 § 4) + non-humanoid setpieces. Spike validates Meshy → UE works empirically; CC5 + Mutable validation is post-spike WS1 commission territory.

If gandalf + Matt locked Tier 1 PC team-coordination amendment in the prior session: you now have explicit sub-agent local fan-out pattern + cross-host coordination via file+push. Use sub-agent Agent({ subagent_type: "gandalf" }) for Pattern-A design queries locally; use file+push for cross-seam queries to KR/Mac.

Continue with criterion 3.2 → 3.4 → 3.6 → 3.7 STRETCH in sequence (or parallel where independent). Cost discipline: $3 of $20 burned; $17 remaining. Document each criterion completion + push.
```

### 3.3 Criteria remaining + estimated completion

| Criterion | Estimated time | Dependencies |
|---|---|---|
| 3.2 — UE 5.7 import of rigged FBX | ~1-2 hours | Crusader (already on PC) + Matt's rigged FBX (after manual step) |
| 3.4 — Niagara consumes engine JSON | ~2-4 hours | Independent; can fire anytime |
| 3.6 — TAA/TSR fast-combat readability | ~1-2 hours | UE5 Mannequin fallback OR rigged FBX from 3.2 |
| 3.7 STRETCH — 3D cosmograph viability | ~2-4 hours | Free FAB assets (Epic Niagara + VDB Nebula); mantis installs |

**Total estimate:** ~6-12 hours mantis work for criteria 3.2 + 3.4 + 3.6 + 3.7. Likely 1-2 additional mantis sessions.

### 3.4 Spike close trajectory

When all 6 primary criteria + 1 stretch resolve:

1. Mantis authors `port-workstream-gating-verdict.md` at spike packet path
2. Mantis authors `spike-findings-report.md` synthesizing per-criterion findings
3. Gandalf reviews verdict + ratifies via Pattern A-deep response (sub-agent or direct)
4. Jack-ryan Gate-2 verification (via KR routing OR sub-agent fan-out)
5. Spike close + wave-close record at `canonical/story/2026-06-XX-ue-architecture-validation-spike-wave-close.md`
6. WS1 port commission scoping fires (gandalf authors WS1 data-layer-port commission dispatch)

**Anticipated close timeline:** spike OVERALL GREEN within 1-2 additional sessions; WS1 commission scoping immediately after.

---

## 4. Deferred items + empirical-evidence triggers

### 4.1 CC5 + Mutable architectural decision

**Status:** DEFERRED to post-spike + WS1 commission scoping
**Why deferred:** spike is validating Meshy path empirically; CC5 + Mutable evaluation is a separate workstream that doesn't gate spike completion
**Empirical-evidence trigger for re-engagement:** spike OVERALL GREEN + WS1 commission scoping fires; at that point gandalf authors CC5 + Mutable evaluation dispatch (could fire as separate spike-2 OR as WS1 sub-task)
**Anchors:** `agentic_orchestration/legolas/research/2026-06-02-unreal-character-customization-research/synthesis.md`

### 4.2 Criterion 3.5 (PCG) deferred

**Status:** DEFERRED non-blocking (per spike dispatch § 6)
**Why deferred:** engine doesn't yet emit room-layout JSON; PCG ingest is gated on engine workstream that emits room geometry
**Empirical-evidence trigger:** engine emits room-layout JSON (separate gamora / rocket workstream); at that point criterion 3.5 fires as supplementary spike

### 4.3 Modular weapon architecture

**Status:** DEFERRED; flagged by Matt 2026-06-06 ("weapons won't work modularly but that's another process for another day")
**Why deferred:** spike-generated kit meshes had weapons baked in (combat-pose generation); UE socket-attachable weapons need different generation prompt + sub-mesh architecture
**Empirical-evidence trigger:** WS2 rendering layer work; mantis authors weapon-substrate-to-UE-socket-attachment prompt-engineering pattern
**Anchors:** mantis criterion 3.2 finding; legolas 2026-06-02 research on character customization patterns

### 4.4 Cosmograph WS2 port commission scoping

**Status:** DEFERRED to spike OVERALL GREEN
**Why deferred:** WS2 (rendering layer port) gates on spike PASS verdict; cosmograph 2D-vs-3D port direction informed by criterion 3.7 STRETCH outcome
**Empirical-evidence trigger:** spike OVERALL GREEN + criterion 3.7 STRETCH PASS / YELLOW / RED outcome
**Anchors:** cosmograph-pivot doc § 9.5 + my earlier UE port plan (3-5 months PC-side timeline)

### 4.5 Veo materialization payoff re-engagement

**Status:** DEFERRED (parked per cosmograph-pivot record)
**Why deferred:** cosmograph at /forge operational + Matt-validation = trigger for re-engagement
**Empirical-evidence trigger:** cosmograph creation-moment manifestation milestone DELIVERED (it has — `/forge` live at Vercel prod); next is materialization payoff design call. Composes with Duskweaver L50 artifacts on Mac (`/duskweaver/master_duskweaver.png` + Crusader pre-rigged set as visual identity references).
**Anchors:** `canonical/story/2026-06-05-cosmograph-pivot.md` § 9.5

---

## 5. Resume protocol (gandalf session start)

Next gandalf session, read in order:

1. `canonical/00-ground-state.md` (always first)
2. This plan doc (operational sequencing for next session)
3. `agentic_orchestration/dispatches/2026-06-06-mantis-ue-architecture-validation-spike.md` (spike dispatch context)
4. `canonical/story/2026-06-06-autonomous-fire-prompt-template.md` (canonical pattern reference)
5. `.claude/agents/mantis.md` + `.claude/skills/reincarnated-mantis-operating-procedure/SKILL.md` (mantis context for OP amendment)
6. Latest mantis criterion findings under `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/` (mantis session-1 outputs)
7. Latest KR notes under `agentic_orchestration/knight-rider/notes/` if any session-boundary memo authored at this wind-down

---

## 6. Push state at wind-down

- Meta-repo HEAD pushed to origin/main up to and including this plan commit
- Mantis criterion findings + UE pre-fire scoping + autonomous-fire prompt template + legolas FAB survey all on origin
- PC clone is in sync with origin per push pattern established for spike cycle
- No outstanding local commits expected on Mac at wind-down

---

## 7. Sign-off

**Authored:** gandalf 2026-06-07 per session wind-down protocol post-spike-session-1 close
**Empirical-evidence trigger for next session:** Matt re-engages gandalf for first-task PC team-coordination architecture decision + spike continuation guidance
**Routing:** informs next gandalf session-start + mantis session-2 priming + KR re-engagement coordination

**Wind-down sequence after this plan commits:**
1. Commit + push this plan + .gitignore update
2. Direct KR to wind down (session-boundary memo if needed) + close
3. Mantis already closed
4. Gandalf session winds down

**End of next-session plan.**
