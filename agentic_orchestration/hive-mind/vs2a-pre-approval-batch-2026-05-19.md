# VS2a Pre-Approval Batch — full dispatch set authored for Matt review

**Authored:** 2026-05-19 ~12:30Z by knight-rider per Matt directive 2026-05-19 ("Batch all of VS2a now so I can approve everything in advance").
**Authority:** Matt directive 2026-05-19 (autonomous-operation continues + pre-approval-batch mode for VS2a scope).
**Status:** ALL VS2a dispatches authored + committed + pushed. Awaiting Matt pre-approval review.

---

## § 0 — TL;DR

The complete VS2a dispatch set is authored and on the working tree. Twelve dispatches total — four FIRST-FIRE (already authored + active per prior turn) and eight DOWNSTREAM (authored in this turn). Activation gates per coordination matrix DAG; specialists pick up at their natural activation point without Matt intervention.

Matt approves the **batch shape + per-dispatch acceptance criteria** in this review. After approval, knight-rider operates autonomously through L1 ship + VS2b handoff per protocol § 4.9 (Matt only returns at wind-down).

---

## § 1 — The twelve dispatches (full inventory)

### § 1.1 — First-fire batch (no upstream gate; firing immediately)

| # | Dispatch | Owner(s) | Effort | Acceptance tag |
|---|---|---|---|---|
| **F2** | kit-redesign approach Gate-1 decision | gandalf | 0.5–1 day | `vs2a/v0.5-kit-redesign-approach-decided` |
| **F1** | `geometry_type` per-skill schema field | rocket + star-lord | 2–4 wk | `vs2a/v0.1-geometry-type-schema-shipped` |
| **F3** | Drift-14 + Drift-15 framework | gandalf | 0.5–1 day | `vs2a/v0.3` + `vs2a/v0.4` |
| **F4** | B6 skill-tree UI surface decomposition | drax | design 1-2d / proto 1-2 wk | `vs2a/v0.6-b6-skilltree-ui-decomposition` |

### § 1.2 — Second-fire batch (gated on F3)

| # | Dispatch | Owner(s) | Effort | Acceptance tag |
|---|---|---|---|---|
| **F5** | legolas Drift-14 pool × VFX-catalogue mapping audit + gandalf re-scoring | legolas + gandalf | ~1-2 days | `vs2a/v0.10-drift14-audit-complete` |
| **F6** | legolas Drift-15 environment-tileset Track A sweep | legolas | ~5-8h | `vs2a/v0.11-drift15-track-a-complete` |

### § 1.3 — Downstream batch (gated on F1 / F2 / S1 / etc.)

| # | Dispatch | Owner(s) | Gate | Effort | Acceptance tag |
|---|---|---|---|---|---|
| **R2-RT** | R2 H1 re-validation under explicit `geometry_type` | gamora | F1 lands | ~1-3 days | `vs2a/v0.2-r2-h1-revalidated` |
| **S1** | kit-redesign sprint (3-branch per F2) | rocket + gandalf consult | F2 + F1 | 4-6 wk (a) / 2-3 wk (b) / 3-5 wk (c) | `vs2a/v0.7-kit-redesign-sprint-complete` |
| **S2** | B6 main work (tree structure + tree-aware convergence) | rocket + gamora | F2 + rocket pre-work + S1 partial | ~1-2 wk | `vs2a/v0.8-b6-main-work-complete` |
| **S3** | Gate-3b sim MS extension | gamora | rocket schema-default + star-lord export-DTO (C1) | ~3-5 days | `vs2a/v0.9-sim-ms-gate3b-complete` |

### § 1.4 — Ship gate

| # | Dispatch | Owner(s) | Gate | Effort | Acceptance tag |
|---|---|---|---|---|---|
| **L1** | demo regen on single season — VS2a SHIP GATE | star-lord + gamora | all of F1, F4, S1, S2, S3, C1, C2, C3, F5 | ~1 wk | `vs2a/v1.0-vs2a-ship` |

### § 1.5 — Post-Matt-wind-down

| # | Dispatch | Owner(s) | Gate | Effort | Acceptance tag |
|---|---|---|---|---|---|
| **F6-D** | Drift-15 environment-tileset Track D drax integration | drax | M1 (Matt picks pack at wind-down) | ~3-5 days | `vs2a/v0.16-drift15-drax-integration-complete` |

---

## § 2 — In-flight items (no dispatch needed)

Per scope-of-work-vs2a § 2.5–§ 2.7 + AGENT_STATE.md across seams:

| # | Item | Owner(s) | Status |
|---|---|---|---|
| **C1** | Movement-speed baseline cascade | rocket + drax + gamora | 🟢 IN-FLIGHT (Option-B values LOCKED; per-seam impl in progress) |
| **C2** | B11 GREEN-list element VFX (11/13 elements) | drax + elrond | 🟢 IN-FLIGHT (Pimen ingest pipeline shipping iteratively) |
| **C3** | chierit character rendering | drax | 🟢 IN-FLIGHT (zip archives acquired; per-class rendering) |
| **C4** | Pimen curation pipeline + subset selection | elrond | 🟢 IN-FLIGHT |

---

## § 3 — Matt-gated items (HELD for wind-down)

| # | Item | Owner(s) | Trigger | Acceptance tag |
|---|---|---|---|---|
| **M1** | Drift-15 Matt-selection (3 environment tilesets) | Matt | F6 Track A complete + Matt wind-down | `vs2a/v0.15-drift15-matt-selected` |
| **M2** | Engine-rebuild playtest tag firings (v0.12 + v0.16) | Matt | Matt wind-down | `hive-rebuild/v0.12` + `hive-rebuild/v0.16` + notional `hive-rebuild/v1.1-engine-rebuild-final` |

---

## § 4 — Decision criteria across the batch (Matt's review surface)

Each dispatch includes:

1. **TL;DR** of what's being done + the SME's authority + Matt's involvement
2. **Required reading** list (precedent dispositions; canonical docs; AGENT_STATE checkpoints)
3. **Scope** with concrete deliverables per seam
4. **Cross-seam contract change?** Principle 6 gate explicit answer + MIGRATION.md requirements + round-trip smoke requirement (or not-applicable justification)
5. **Acceptance criteria** checklist
6. **Out of scope** explicit non-goals
7. **Open questions** for the agents to resolve under in-seam L1 / cross-seam L2 routing
8. **Activation gate** explicit — when the dispatch fires
9. **Authority** — autonomous-operation per protocol § 4.0 / § 4.9; no Matt-wait post-activation

---

## § 5 — DAG of activation gates (when each dispatch fires)

```
                    ENGINE-REBUILD CLOSED (v1.0)
                              │
                              ▼
                       VS2a kickoff (vs2a/v0.0 baseline)
                              │
              ┌───────────────┼───────────────┬──────────────┐
              ▼               ▼               ▼              ▼
            F2              F1              F3             F4
       (gandalf)       (rocket+SL)     (gandalf)        (drax)
         │ │               │              │ │              │
         │ │               │              │ │              │
         │ │               ▼              ▼ ▼              │
         │ │           R2-RT           F5  F6              │
         │ │          (gamora)        (legolas + gandalf re-scoring; legolas Mode B)
         │ │
         │ ▼
         └─► S1 (rocket+gandalf; 3-branch per F2 disposition)
                  │
                  ▼
                 S2 (rocket+gamora)
                  │
                  ▼
                 [rocket schema-default + star-lord export-DTO from C1 cascade]
                  │
                  ▼
                 S3 (gamora)
                  │
              ┌───┴───┐
              │       │
              ▼       ▼
            (C1 C2 C3 C4 — in-flight independent)
                  │
                  ▼
                 L1 SHIP (star-lord + gamora) → vs2a/v1.0-vs2a-ship
                  │
                  ▼
            (M1: Matt picks Drift-15 pack at wind-down)
                  │
                  ▼
            F6-D (drax integration)
                  │
                  ▼
            (M2: Matt fires engine-rebuild playtest tags + retrospective)
                  │
                  ▼
            VS2b kickoff
```

---

## § 6 — Matt approval pattern (what's being asked)

**Matt approves** (one decision, batched):

✅ The set of 12 dispatches as the complete VS2a scope
✅ Per-dispatch acceptance criteria as-stated
✅ The DAG of activation gates (which dispatch fires when)
✅ Knight-rider's autonomous L1 sequencing during execution
✅ Specialist L1 within-seam authority during execution
✅ Gandalf L2-equivalent on cross-cutting design decisions (F2 path; F3 framework; S1 cohesion gate; L1 cohesion sanity-check; re-disposition if metrics surface)
✅ The M1 + M2 Matt-gated steps held for wind-down (no autonomous mode bypass)

**Matt may request amendments** (surface in this review):
- Per-dispatch scope adjustments
- Activation gate clarifications
- Cross-seam coordination overrides
- Out-of-scope items moved into VS2a (would expand batch)
- In-scope items moved out (would shrink batch)

**Matt does NOT need to approve** (per protocol § 4.0 autonomous-mode):
- Per-task implementation details within dispatches
- L1 within-seam decisions during execution
- L2 cross-seam routing during execution
- gandalf disposition decisions surfacing during execution
- knight-rider tag-firing on milestone achievement
- Mid-flight canonical-doc amendments by gandalf

---

## § 7 — Pattern-B status (parked; unchanged)

Pattern-B remains PARKED at `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. R6 (Host-Calibration) enters dispatch cycle only when Pattern-B commercial-direction resolves. VS2a pre-approval does NOT alter Pattern-B status.

---

## § 8 — Wind-down sequence (post-L1 ship)

Per protocol § 4.9 + scope-of-work-vs2a § 5.1:

1. **L1 ships** → knight-rider tag-fires `vs2a/v1.0-vs2a-ship` + authors VS2a closeout state-of-hive
2. **Matt wind-down session** opens; Matt reviews:
   - VS2a closeout state-of-hive
   - Pending Matt-gated items (M1 environment-pack selection; M2 engine-rebuild playtest tag firings)
   - Decisions-log entries for VS2a arc
3. **Matt** picks environment pack (M1) → knight-rider drafts decisions-log entry + activates F6-D drax integration
4. **Matt** fires engine-rebuild playtest tags (M2 — `hive-rebuild/v0.12` + `hive-rebuild/v0.16`) + notional `v1.1-engine-rebuild-final`
5. **Engine-rebuild retrospective** authored by gandalf (per protocol § 14.3 pattern from 2026-05-17 invocation)
6. **VS2b kickoff** — knight-rider authors `scope-of-work-vs2b.md` + `coordination-matrix-vs2b.md` (potentially again under pre-approval pattern if Matt requests)

---

## § 9 — Cross-references

- VS2a scope-of-work: `agentic_orchestration/hive-mind/scope-of-work-vs2a.md`
- VS2a coordination matrix: `agentic_orchestration/hive-mind/coordination-matrix-vs2a.md`
- VS2a dispatches: `agentic_orchestration/dispatches/2026-05-19-*-vs2a-*.md` (12 total)
- Operating protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9
- Engine-rebuild closeout: `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild-v1.0.md`
- v1.0 disposition: `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md`
- Roadmap: `canonical/16-project-roadmap.md` § VS2a + § VS2b
- Decisions log: `reincarnated-engine/design/decisions/decisions-log.md`
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- AGENTS topology: `agentic_orchestration/AGENTS.md`
- GOVERNANCE ADRs: `agentic_orchestration/GOVERNANCE.md`

---

*Filed 2026-05-19 by knight-rider per Matt directive (pre-approval-batch mode for VS2a). The complete dispatch set awaits your eye; the DAG awaits your nod; the road continues once you confirm the shape.*
