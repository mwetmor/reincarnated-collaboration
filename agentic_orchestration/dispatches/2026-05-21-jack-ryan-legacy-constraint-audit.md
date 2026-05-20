# Dispatch — Jack-Ryan DESIGN-MODE: Legacy Constraint Audit (QD-Engine Rebuild Prerequisite)

**Date:** 2026-05-21 (authored 2026-05-20 evening; fires overnight)
**Author:** gandalf
**Recipient:** jack-ryan (DESIGN-MODE — design-side canonical-doc steward + drift-detection authority)
**Status:** ACTIVE
**Priority:** HIGH (gates QD-engine rebuild planning)
**Estimated effort:** 8-16 hours of structured design-side analysis + synthesis

---

## 0. TL;DR

Before QD-engine rebuild planning starts in earnest, the project needs a **comprehensive design-side audit of every legacy constraint** in the engine. Matt's directive (2026-05-20 evening end-of-session): *"Should we send one or more agents to deep dive into engine mechanics to be sure we do not have any more legacy constraints in place? I believe that we do have the archetype constraint in place and the AOE skew. There may be more, and that will throw off our QD engine rebuild testing."*

Your task: enumerate every constraint (documented, implied, empirically-surfaced, suspected) that shapes engine behavior. For each, classify status, identify QD-rebuild risk, and recommend next-step disposition (verify / document / ablate / remove / preserve).

This audit is **design-side only.** You read canonical docs, decisions-log, engineering-disciplines, working-agreement, and gandalf/galadriel/jack-ryan memos. You do NOT do code-level enumeration — that's Phase 2 work assigned to seam specialists (rocket / gamora / star-lord) after the recompose-hive ships. Your output feeds the QD-engine rebuild hive-mind protocol gandalf is authoring in parallel.

---

## 1. Why this audit matters now

The QD-engine architecture commits to MAP-Elites over 8 BC axes, with measurements computed from simulation telemetry. **If undocumented constraints shape the substrate, the BC measurements will reflect those constraints rather than the true design space.** Concrete failure modes if constraints aren't surfaced:

- Archive cells fail to populate because a hidden constraint prevents kit-generation in that BC cell
- Measurements drift over time as constraints interact with new substrate
- Discipline #13b ablation experiments fire blindly without knowing which variable is responsible
- Profile A (Reincarnated Phase 0) ships with hidden biases

The recompose-validation hive is currently surfacing constraints empirically — that's reactive. A proactive design-side enumeration before rebuild planning gives us the full constraint inventory and lets us deal with each on its merits.

---

## 2. Reading list (in order)

### 2.1 Decisions and disciplines (start here)

1. `reincarnated-engine/design/decisions/decisions-log.md` — **complete read from earliest entry to current**. Every decision is a potential constraint; identify which ones encode behavioral lock-ins.
2. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — all 17 disciplines; note especially #13a (drift), #13b (per-variable attribution), #14 (terminology lock), #17 (calibration), #18 candidate (joint-gate).

### 2.2 Canonical design docs (architectural intent)

3. `canonical/09-geometry-palette-discussion.md` — 16-type geometry palette; any element-or-geometry biases documented?
4. `canonical/16-project-roadmap.md` — strategic phasing; identifies scope-deferred constraints
5. `canonical/17-gear-and-spirit-guide-design.md` — gear architecture; identify gear-vs-skill assumptions
6. `canonical/28-engine-arpg-rebalance-design.md` — balance loop; any baked-in convergence targets?
7. `canonical/29-design-overview.md` — strategic anchor
8. `canonical/30-engine-explainer-current.md` + `canonical/31-engine-explainer-future.md` — current vs future engine state; identify what's currently constrained that future state intends to free
9. `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` — progression structure; trait pool constraints, level gates
10. `canonical/34-monster-design-phase0-vs-production.md` — monster constraints
11. `canonical/35-*` through `canonical/37-form-bias-diagnosis-and-recovery.md` — **doc 37 is critical**: explicitly identifies the Cluster-B humanoid-fantasy substrate constraint. Read in full.

### 2.3 Story-layer docs (recent design work)

12. `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — the architectural target this audit serves
13. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the 8-axis operational spec; identifies known substrate flags
14. `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` — empirical investigation; surfaced constraints
15. All other `canonical/story/*.md` — read titles, prioritize ones touching engine mechanics
16. `canonical/story/gandalf-design-lineage.md` — gandalf's design-history influences

### 2.4 Recent memos + critique-pair artifacts

17. `agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html` — 11 surfaced decisions; some encode constraints
18. `agentic_orchestration/skill_handoff_*.md` — recent handoff docs; surfaced behaviors
19. `reincarnated-engine/AGENT_STATE.md` per-agent — current state snapshots
20. Any pushback memoranda at `agentic_orchestration/gandalf/pushback/*` or `agentic_orchestration/jack-ryan/*`

### 2.5 High-level code surface reference (NOT enumeration — orientation only)

21. Skim `reincarnated-engine/src/reincarnated/` directory structure to understand seam organization
22. Read `reincarnated-engine/src/reincarnated/canonical/` file list — these often encode default constraints
23. Look up `balance_loop.py` and `generation/` module list — confirm structural extent

**Do NOT read implementation files line-by-line.** That's Phase 2 (specialist code-audit). You're at design-side, identifying what the canonical record says and where drift candidates exist.

---

## 3. Constraint inventory schema

For each constraint identified, capture:

| Field | Values |
|---|---|
| `constraint_id` | Sequential (LC-001, LC-002, ...) |
| `constraint_name` | Short descriptive label |
| `description` | What the constraint does (1-3 sentences) |
| `source_documents` | File paths + line/section references where applicable |
| `status` | DOCUMENTED / IMPLIED / EMPIRICALLY-SURFACED / ABLATION-CANDIDATE / DRIFT-CANDIDATE |
| `engine_surface_affected` | Seam(s) likely affected: generation / simulation / spirit_guide / balance_loop / telemetry / export / canonical / other |
| `bc_axis_affected` | Which of 8 BC axes (or "cross-cutting") |
| `qd_rebuild_risk` | LOW / MEDIUM / HIGH — how badly does this contaminate BC measurement? |
| `recommended_disposition` | VERIFY (confirm via specialist audit) / DOCUMENT (add to canonical record) / ABLATE (run experiment) / REMOVE (post-rebuild) / PRESERVE (intentional, document explicitly) |
| `dependencies` | Other constraints (LC-N) related to this |
| `notes` | Context, history, references |

### 3.1 Status definitions

- **DOCUMENTED:** Decision-log entry exists; canonical doc specifies the constraint as intentional design.
- **IMPLIED:** Referenced in docs but no explicit decision; emergent from related decisions.
- **EMPIRICALLY-SURFACED:** Found via telemetry, sidecar analysis, or hive findings; not in canonical record.
- **ABLATION-CANDIDATE:** Suspected from indirect evidence but unverified; needs Discipline #13b experiment.
- **DRIFT-CANDIDATE:** Canonical doc states X; evidence suggests code does Y. Drift instance per Discipline #13a.

### 3.2 Risk definitions

- **LOW:** Constraint affects 0-1 BC axes marginally; can be carried into rebuild without measurement contamination.
- **MEDIUM:** Constraint affects 1-2 BC axes; measurement contamination possible; should be addressed during rebuild Phase 0.
- **HIGH:** Constraint affects 3+ BC axes or fundamentally shapes substrate; measurement contamination certain; MUST be addressed before rebuild Phase 2 (BC measurement implementation).

### 3.3 Disposition definitions

- **VERIFY:** Constraint suspected but needs specialist code-level confirmation (Phase 2).
- **DOCUMENT:** Constraint exists, is acceptable, but undocumented; add to canonical record.
- **ABLATE:** Run Discipline #13b experiment to measure constraint's actual effect; informs removal decision.
- **REMOVE:** Constraint identified as harmful to QD measurement; remove during rebuild.
- **PRESERVE:** Constraint is intentional design lock-in (e.g., Profile A scoping); document explicitly + keep.

---

## 4. Known starting points (preliminary — expand substantially)

These are constraints already identified by other work. Your audit confirms each + expands the list significantly.

| LC-prelim | Name | Status (prior) | Source |
|---|---|---|---|
| 01 | Archetype constraint (Cluster-B humanoid-fantasy substrate) | DOCUMENTED | Doc 37 form-bias work |
| 02 | AOE skew | EMPIRICALLY-SURFACED | B14.5 sidecar — fire 23.6% over-rep |
| 03 | Floor-lock at modifier=0.05 | DOCUMENTED + being-fixed | Recompose-hive Option A |
| 04 | Mana bug (structural) | DOCUMENTED + flagged | 2026-05-08 engine state findings |
| 05 | Hunter modifier range 1.82 | EMPIRICALLY-SURFACED | B14.5 sidecar |
| 06 | Element selection bias | EMPIRICALLY-SURFACED | B14.5 sidecar |
| 07 | Convergence iteration variance | EMPIRICALLY-SURFACED | B14.5 sidecar (controllers vs rogue/hunter) |
| 08 | Energy homogeneity | EMPIRICALLY-SURFACED | B14.5 sidecar |
| 09 | Cohesion-vs-mechanics gating | EMPIRICALLY-SURFACED | S1 split verdict (2026-05-19) |
| 10 | Generator-spender economy bias | ABLATION-CANDIDATE | Suspected; no direct evidence |
| 11 | Range-constraint logic for elements | EMPIRICALLY-SURFACED | B14.5 sidecar (close-range controllers) |
| 12 | 16-type geometry palette biases | IMPLIED | Doc 09 — palette is bounded |
| 13 | Spirit-guide swap assumptions | IMPLIED | Spirit-guide design depends on baseline behaviors |
| 14 | Implicit-pillar drift | Definitional | Engineering-disciplines #13a coverage |
| 15 | Canonical-four leakage potential | DOCUMENTED | Engineering-disciplines #14 |
| 16 | Per-tier WR convergence targets | DOCUMENTED | R1 disposition target structure |
| 17 | PackProxy ×8 multiplier (swarm tier) | DOCUMENTED | R1 sprint mechanism |
| 18 | R8 inverted-mode coalescence default | DOCUMENTED | Vision-doc § 5 IDC |

**Expand this list substantially.** Your audit should produce 30-60+ entries by reading the full canonical record. Many constraints are buried in doc footnotes, decision-log entries, or implied by architectural choices.

---

## 5. Deliverables

Produce a complete design-side audit at:

```
agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/
  ├── summary.md                              — synthesis (5-8 pages)
  ├── constraint-inventory.md                 — full enumerated list with all fields
  ├── high-risk-constraint-deep-dive.md       — extended treatment of HIGH-risk items
  ├── drift-candidates.md                     — Discipline #13a drift instances flagged
  ├── ablation-experiment-candidates.md       — Discipline #13b ablation proposals
  ├── qd-rebuild-prerequisites.md             — which constraints MUST resolve before each rebuild Phase
  ├── methodology-questions-for-gandalf.md    — scope/priority questions for hive-mind protocol authoring
  └── data/
      └── constraint-inventory.csv            — machine-readable format
```

### 5.1 summary.md structure

1. **Executive summary** — total constraints found; distribution by status; HIGH-risk count
2. **Top-10 most critical constraints for QD-rebuild measurement integrity**
3. **Drift candidates summary** — where canonical doc and behavioral evidence diverge
4. **Documented-but-forgotten constraints** — design decisions that were made but aren't actively tracked
5. **Cross-references to existing engineering disciplines** — which discipline each constraint exercises
6. **Recommended QD-rebuild prerequisite sequencing** — what MUST be done before rebuild Phase 0, 1, 2
7. **Open questions for gandalf + Matt**

### 5.2 constraint-inventory.md structure

The full enumerated list. Each entry uses the schema in § 3. Group by:
- Section 1: HIGH-risk constraints (most critical)
- Section 2: MEDIUM-risk constraints
- Section 3: LOW-risk constraints
- Section 4: PRESERVE-disposition constraints (intentional lock-ins)

### 5.3 high-risk-constraint-deep-dive.md structure

For each HIGH-risk constraint, extended treatment:
- Full history (when introduced, why, by whom)
- All affected engine surfaces with specific seam references
- All affected BC axes with specific bin impact
- Ablation experiment design (if ABLATE disposition)
- Removal sequencing (if REMOVE disposition)
- Risk of removal (what might break)

### 5.4 drift-candidates.md structure

Discipline #13a explicit findings. For each:
- Canonical doc location stating intended behavior
- Evidence of actual behavior diverging
- Drift instance characterization
- Recommended drift-correction path

### 5.5 ablation-experiment-candidates.md structure

Discipline #13b experiment proposals. For each:
- Constraint hypothesis (what we think is happening)
- Ablation design (what to remove/vary to test)
- Expected signal (what telemetry would confirm/deny)
- Cost estimate (effort + seasons + analysis time)
- Risk if ablation breaks engine (always-recoverable via tag)

### 5.6 qd-rebuild-prerequisites.md structure

For each rebuild Phase (P0 constraint-removal, P1 substrate-enrichment, P2 BC-measurement, P3 archive, P4 sim-extensions, P5 coalescence, P6 profiles, P7 validation), identify:
- Constraints that MUST resolve before this phase starts
- Constraints that CAN resolve during this phase
- Constraints that can be deferred past this phase

---

## 6. Methodology constraints

- **Read-only across all sources.** No code changes, no canonical-doc revisions, no decision-log entries. Pure analysis.
- **Cite specifically.** File paths + section/line references for every constraint claim. Vague citations rejected.
- **Don't invent.** If a constraint is suspected but not in the record, flag as ABLATION-CANDIDATE — don't assert as DOCUMENTED.
- **Stay in DESIGN-MODE.** This is your design-collaborator role, not your DEV-MODE BLOCK gatekeeper role. You're producing intelligence for rebuild planning, not gating any work.
- **Don't pre-empt removal decisions.** Your output is recommendations; Matt and gandalf decide what to remove/keep/ablate.
- **Surface drift cases honestly.** Even if the drift is between a doc you wrote and code someone else wrote, name it. Discipline #13a applies to everyone.

---

## 7. Cross-references

- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** — the 8-axis operational spec your audit informs
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — architectural vision
- `agentic_orchestration/dispatches/2026-05-20-legolas-substrate-sufficiency-audit.md` — parallel research commission (substrate audit; complementary to this one)
- `canonical/37-form-bias-diagnosis-and-recovery.md` — explicit constraint-identification work from earlier session
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #13a, #13b, #14, #17 directly applicable

---

## 8. Timing

- **Start:** immediately on dispatch receipt (overnight)
- **Target completion:** single Agent session (8-16 hours of effective research)
- **Blocks:** QD-engine rebuild hive-mind protocol authoring (gandalf is waiting)
- **Concurrent with:**
  - Legolas Phase 1 reconnaissance (substrate audit) — parallel
  - Recompose-validation hive — parallel, no interaction
  - Gandalf hive-mind protocol authoring — gandalf incorporates your output post-completion

When complete, report back to gandalf. Your findings feed directly into the rebuild hive-mind protocol authored before Matt resumes session.

---

## 9. Escalation

- **Methodology questions:** surface in `methodology-questions-for-gandalf.md`
- **Scope ambiguity:** flag in summary; don't expand scope unilaterally
- **If audit surfaces a constraint so structurally critical that rebuild planning needs to pivot:** flag immediately in summary § 7 (open questions); gandalf reads on completion

---

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine rebuild architectural integrity.
