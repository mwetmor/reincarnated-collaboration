# Path (1) Cycle 14 Scope Expansion — Knight-Rider Kicker

> **STATUS:** CURRENT — orchestration signal for knight-rider to amend Cycle 14 scope-doc + route Phase 4 + Phase 5 + Phase 7 implementation work + pre-Phase-4 remediation + Discipline #46 canonical-write per Matt 2026-05-27 Path (1) ratification.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27 evening
**Recipient:** knight-rider
**Authority:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Source docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Path 1 recognition record; load-bearing)
- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` (load-bearing pre-Phase-4)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 4 + § Phase 5 + § Phase 7 (architectural foundation)

---

## 0. TL;DR

Cycle 14 scope expands. KR amends scope-doc; routes Phase 4 math gates + Phase 5 multimodal clustering + Phase 7 2-layer joint-gate dispatches; routes pre-Phase-4 remediation (Discipline #46 canonical-write + `v1_scope` index + telemetry/substrate fetchall refactor). Phase 6 + 8 deferred Cycle 15+.

---

## 1. Cycle 14 scope-doc amendment (KR; immediate)

KR amends `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` adding new sections:

### 1.1 NEW § Phase 4 — Mechanical Archive Math Gates

Per doc 39 § Phase 4 + Path 1 recognition record § 3.1. 5 math notes (Pareto + Crowding + Mahalanobis + KL + Eviction) bundled; gamora primary; elrond methodology consultation; jack-ryan Gate-1 + Gate-2; per-cell bounding required per Discipline #46 § 7.

### 1.2 NEW § Phase 5 Multimodal Extension

Wave 3 (Phase 5 cohesion-judge LLM) scope expands to include multimodal clustering + faction-coalescence per `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` § 2.2. 2 math notes (Multimodal Clustering Algorithm + Faction-Label Assignment Policy) bundled with Phase 4 math notes.

### 1.3 NEW § Phase 7 — 2-Layer Joint-Gate Evaluation

Per doc 39 § Phase 7 (Discipline #18). 2-layer (mechanical + cohesion); visual deferred to Cycle 15+ alongside Phase 6.

### 1.4 NEW § Pre-Phase-4 Remediation

Discipline #46 canonical-write + `v1_scope` index + telemetry fetchall refactor (5 sites) + substrate fetchall refactor (2 sites).

### 1.5 Cycle 14 timeline update

~10-15 weeks total under Path (1); quality > timeline (Q10) ratified.

---

## 2. Roadmap + ground-state amendments

### 2.1 `canonical/02-roadmap.md` § 3

KR amends:
- Cycle 14 expanded entry: "Path (1) ratified 2026-05-27; Phase 4 + 5 + 7 2-layer added; Phase 6 + 8 deferred Cycle 15+"
- New entry: Phase 4 math gates implementation (gamora)
- New entry: Phase 5 multimodal clustering + faction-coalescence (gandalf + star-lord + rocket)
- New entry: Phase 7 2-layer joint-gate (gandalf + jack-ryan)
- New entry: Discipline #46 canonical-write (jack-ryan)
- New entry: Pre-Phase-4 remediation (elrond + star-lord + rocket)
- Cycle 14 estimated total: 10-15 weeks

### 2.2 `canonical/00-ground-state.md` § 1

KR amends:
- Add new CURRENT entry: Path 1 recognition record (`agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md`)
- Add new CURRENT entry: Discipline #46 candidate (`agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md`)

---

## 3. Dispatches to author (sequenced)

### 3.1 Pre-Phase-4 Remediation Bundle (fires NOW)

**Dispatch 1A — Discipline #46 ratification (jack-ryan)**
- **Title:** `2026-05-27-jack-ryan-discipline-46-db-anti-materialization-stream-canonical.md`
- **Scope:** consume gandalf Discipline #46 candidate; canonical-write at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46; amend Gate-1 + Gate-2 checklists with Discipline #46 grep audit
- **Effort:** ~1-2 days
- **Owner:** jack-ryan

**Dispatch 1B — `v1_scope` index addition (elrond)**
- **Title:** `2026-05-27-elrond-v1-scope-index-addition.md`
- **Scope:** add `CREATE INDEX IF NOT EXISTS idx_knowledge_v1_scope ON weapon_knowledge_entries(v1_scope);` + verify EXPLAIN QUERY PLAN on existing substrate queries hits the index
- **Effort:** ~1 hour
- **Owner:** elrond

**Dispatch 1C — Telemetry fetchall() refactor sweep (star-lord)**
- **Title:** `2026-05-27-star-lord-telemetry-fetchall-refactor-discipline-46.md`
- **Scope:** refactor 5 telemetry fetchall sites (`telemetry/db.py:77` + `recorder.py:65/80/93/114`) to cursor iteration or `fetchmany(1000)` patterns; add LIMIT clauses where exploratory; push aggregation to SQL where applicable
- **Effort:** ~3-5 hours
- **Owner:** star-lord

**Dispatch 1D — Substrate fetchall() refactor (rocket)**
- **Title:** `2026-05-27-rocket-substrate-fetchall-refactor-discipline-46.md`
- **Scope:** refactor 2 substrate fetchall sites (`substrate_weapon_binding.py:332` + `bc_target_substrate_engine.py:342`); same patterns
- **Effort:** ~2-3 hours
- **Owner:** rocket

These 4 dispatches fire in parallel. KR routes per wave-entry-fire-discipline (Agent tool invocation).

### 3.2 Phase 4 + Phase 5 Math Note Bundle (fires after Discipline #46 ratifies; in parallel with 3.1 closing)

**Dispatch 2 — Phase 4 + 5 math notes bundle**
- **Title:** `2026-05-27-phase-4-5-math-notes-bundle.md`
- **Scope:** 7 math notes authored:
  - **Phase 4 (5 notes):** MG-1 Pareto Dominance / MG-2 Crowding-Hypervolume / MG-3 Mahalanobis / MG-4 KL Information Gain / MG-5 Eviction Rules (gamora primary + elrond methodology)
  - **Phase 5 (2 notes):** PM-1 Multimodal Clustering Algorithm / PM-2 Faction-Label Assignment Policy (gandalf primary + star-lord LLM integration + elrond methodology)
- **Math-before-code Discipline #1 + #18 hotspot routing**: methodology consultation explicit
- **Discipline #46 compliance section in each math note**: per-cell bounding for math gates; streaming patterns for archive queries
- **Acceptance:** all 7 math notes authored; jack-ryan Gate-1 PASS; Matt-gate per Discipline #18 ratifies bundled
- **Effort:** ~3-5 days authoring + ~1-2 days Gate-1 + Matt-gate
- **Owners:** gamora + elrond + gandalf + star-lord

KR routes as bundled dispatch with per-note co-ownership; single jack-ryan Gate-1 review on bundle; single Matt-gate.

### 3.3 Phase 4 + Phase 5 Implementation (fires post Matt-gate on bundled math notes)

**Dispatch 3A — Phase 4 math gates implementation (gamora)**
- **Title:** `2026-05-27-gamora-cycle-14-phase-4-mechanical-archive-math-gates.md`
- **Scope:** rocket implements 5 math gates per ratified math notes; per-cell bounding throughout; Discipline #46 compliance verified
- **Effort:** ~3-4 weeks
- **Owner:** gamora primary

**Dispatch 3B — Phase 5 multimodal extension (gandalf + star-lord + rocket)**
- **Title:** `2026-05-27-phase-5-multimodal-clustering-faction-coalescence.md`
- **Scope:** extend Wave 3 Phase 5 cohesion-judge LLM with multimodal clustering + faction-coalescence per ratified math notes
- **Effort:** ~2-3 weeks (parallel with 3A where possible)
- **Owners:** gandalf + star-lord + rocket

Dispatches 3A + 3B can fire parallel where dependencies allow.

### 3.4 Phase 7 2-Layer Joint-Gate (fires post 3A + 3B close)

**Dispatch 4 — Phase 7 2-layer joint-gate spec + canonical-write**
- **Title:** `2026-05-27-phase-7-2-layer-joint-gate-spec.md`
- **Scope:** gandalf authors 2-layer joint-gate composition spec (mechanical + cohesion; visual deferred); jack-ryan canonical-write Discipline-#18 compliance rule
- **Effort:** ~1 week
- **Owners:** gandalf + jack-ryan

---

## 4. Wave-entry-fire-discipline application

KR follows wave-entry-fire-discipline (per KR OP § 3.10):
- Draft dispatch → commit + push → **invoke sub-agents via Agent tool**
- No hand-off-by-dispatch-authoring-only
- Sub-agents fire framing-audit (Discipline #42) before executing each dispatch

---

## 5. Sequencing diagram

```
NOW (Day 0 evening)
 │
 ├─ gandalf authored ✅:
 │   - Path 1 recognition record
 │   - Discipline #46 candidate
 │   - This KR kicker
 │
 ├─ KR consumes this kicker
 ├─ KR amends Cycle 14 scope-doc (§ 1)
 ├─ KR amends roadmap + ground-state (§ 2)
 │
 ├─ FIRE in parallel (§ 3.1 pre-Phase-4):
 │   ├─ Dispatch 1A → jack-ryan (Discipline #46 canonical-write)
 │   ├─ Dispatch 1B → elrond (v1_scope index)
 │   ├─ Dispatch 1C → star-lord (telemetry fetchall refactor)
 │   └─ Dispatch 1D → rocket (substrate fetchall refactor)
 │
 ├─ Wave 1.5 Stage 3 re-impl (Option α; redacted math notes) — parallel firing
 │
DAY 1-3
 │
 ├─ Pre-Phase-4 remediation closes
 ├─ Discipline #46 ratified at engineering-disciplines.md
 │
 ├─ FIRE (§ 3.2):
 │   └─ Dispatch 2 → bundled math notes (Phase 4 + 5; 7 notes)
 │
DAY 3-7
 │
 ├─ Math notes authored
 ├─ jack-ryan Gate-1 PASS on bundle
 ├─ Matt-gate ratifies bundle (single Matt-gate per Discipline #18)
 │
WEEK 2-7
 │
 ├─ FIRE in parallel (§ 3.3):
 │   ├─ Dispatch 3A → gamora (Phase 4 implementation; ~3-4 weeks)
 │   └─ Dispatch 3B → gandalf+star-lord+rocket (Phase 5 multimodal; ~2-3 weeks)
 │
 ├─ Wave 1.5 + Wave 2 + Wave 4 work continues per existing scope
 │
WEEK 7-8
 │
 ├─ FIRE (§ 3.4):
 │   └─ Dispatch 4 → gandalf+jack-ryan (Phase 7 2-layer joint-gate)
 │
WEEK 8-12+
 │
 └─ Wave 5 (production gauntlet) fires under Phase 4 + 5 + 7 2-layer architecture
   ├─ Generates Reincarnated v1 cohort via full math gate pipeline
   ├─ Faction labels emerge from multimodal clustering
   ├─ 2-layer joint-gate (mechanical + cohesion) filters SHIPPED-WORTHY kits
   └─ Cycle 14 close
```

---

## 6. Composition with current in-flight work

| In-flight | Status | Composition with Path (1) |
|---|---|---|
| Wave 1.5 Stage 3 re-impl (Option α redacted) | Math notes Matt-gate paused for jack-ryan re-Gate-1 | Continues parallel; gates on no-class vocabulary clean |
| Substrate enrichment (INT-AoE + monk + hybrid) | ✅ COMPLETE (a0c0253) | Enriched substrate consumed by Phase 4 + 5 |
| Disciplines #40c+#41+#42+#43+#44 | ✅ COMPLETE | Compose with Phase 4 + 5 + 7 work |
| Move 1 KR OP quality-criterion + Move 5 AGENTS.md | ✅ COMPLETE | Apply to all new Phase 4 + 5 + 7 dispatches |
| Per-agent OP amendments (Move 2 + 3 + 5; 10 files) | ⏳ KR follow-on queued | Apply to all sub-agents executing Phase 4 + 5 + 7 work |
| THEMATIC_REGISTRY authoring | ⏳ KR follow-on queued (post Matt-gate on Note 4) | Composes with Phase 5 faction-coalescence |

---

## 7. What's still externally-gated (Matt action)

| Gate | Resolution |
|---|---|
| Matt-gate on redacted Option α math notes | Post jack-ryan re-Gate-1 PASS (under no-class vocabulary) |
| Matt-gate on Phase 4 + 5 math notes bundle | Post jack-ryan Gate-1 PASS on bundle |
| CLAUDE.md Move 5 orientation phrase edit | When convenient (~5 min) |

Nothing else requires Matt action immediately.

---

## 8. Cross-references

- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (recognition record)
- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` (load-bearing)
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` (composes — Phase 4/5 substrate-led at cross-kit level)
- `agentic_orchestration/gandalf/notes/2026-05-27-quality-orientation-shift-five-moves-package.md` (Move 1 quality-criterion applies to all Phase 4/5/7 dispatches)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 4 + § Phase 5 + § Phase 7 (canonical architecture)
- `agentic_orchestration/operating-procedures/knight-rider.md` § 3.10 (wave-entry-fire-discipline)

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — KR kicker for Path (1) Cycle 14 scope expansion + Discipline #46 + pre-Phase-4 remediation + Phase 4/5/7 dispatch routing
**Authority:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"

**For:** the orchestration signal for KR to amend Cycle 14 scope-doc + roadmap + ground-state; fire pre-Phase-4 remediation dispatches in parallel (Discipline #46 canonical-write + v1_scope index + telemetry/substrate fetchall refactor); fire Phase 4 + Phase 5 bundled math notes dispatch; fire Phase 4 + Phase 5 implementation dispatches parallel where possible; fire Phase 7 2-layer joint-gate dispatch post-implementation. Estimated total Cycle 14 timeline ~10-15 weeks under quality > timeline Q10.

**Signed:** gandalf (story-and-design steward)
