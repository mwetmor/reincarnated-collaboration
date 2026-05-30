# Pi-Hosted Engine Control Dashboard Architecture — Recognition Record

> **STATUS:** CURRENT (recognition record; architectural commitments deferred per § 4 empirical-evidence triggers) — Matt 2026-05-30 design conversation surfaced a three-phase dashboard maturation pattern (α status surface → β control plane → γ runner decentralization). Phase α work AUTHORIZED for immediate drax dispatch per Matt 2026-05-30 verbatim "draft the work for KR to begin sending drax out for phase α now." Phases β + γ PRESERVED as design intent for later Pattern-B engagement.

**Date:** 2026-05-30
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-30 verbatim — "we should author phase β & γ to preserve them for later"
**Companion docs:**
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — canonical commitment for Pi-middleware infrastructure
- `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` — exhaustive HTML implementation plan
- `agentic_orchestration/gandalf/notes/2026-05-30-engine-state-season-003-flow-diagram.html` — static state-of-engine doc (Phase α scaffolding source)
- `canonical/00-ground-state.md` — will register new CURRENT entry on commit

---

## 0. TL;DR

Matt surfaced the design intent of converting the static state-of-engine doc into a dynamic dashboard with three-phase maturation:

| Phase | Scope | Status |
|---|---|---|
| **α (alpha)** — Status surface | Drax converts static HTML to dynamic React component; per-phase tiles render real data from JSON sources; mobile-accessible; refresh on demand. NO trigger buttons yet. | ✅ **AUTHORIZED for immediate drax dispatch** per Matt 2026-05-30 |
| **β (beta)** — Control plane | Each phase tile gains "fire this phase" button; Pi FastAPI control endpoints; engine subprocess execution via Pi proxy; per-phase progress + log tail + error surfacing | ⏳ **DEFERRED** — gates on Pi Phase 2 HTTP API maturity + Pattern-B engagement |
| **γ (gamma)** — Runner decentralization | Mac/Pi/PC interchangeable as engine runners; per-workload selection (heavy sim → PC, lightweight LLM → Pi, design + agent work → Mac); engine machine-portability refactor | 🔒 **DEFERRED with empirical-evidence triggers** — significant engine refactor; gates on Pi Phase 2 closure + Cycle 16+ scoping discussion |

This doc preserves β + γ as design intent. Phase α dispatch authored separately as immediate drax work-item.

---

## 1. Phase β — Control plane (preserved design intent)

### 1.1 Scope description

Each phase tile in the dashboard gains a **"fire this phase"** button. Clicking the button posts a control request to Pi's FastAPI service; Pi proxies to an engine runner (initially Mac via SSH or subprocess; eventually Mac/Pi/PC interchangeable per Phase γ). The dashboard receives status updates in real-time (WebSockets or polling), showing per-phase progress bars, log tail, error surfacing.

### 1.2 Architectural shape (preliminary)

Pi FastAPI endpoint family for control plane:

```
POST /control/v1/engine/run-phase/{phase_id}      Fire specified phase
POST /control/v1/engine/run-cascade/{from_phase}  Fire from phase through end
GET  /control/v1/engine/status                    Current run state
GET  /control/v1/engine/run-history               Past N runs
WS   /control/v1/engine/live-log                  Real-time log stream
POST /control/v1/engine/abort                     Halt current run
```

Pi-side concerns:
- Authentication: LAN-only initially; API token for hardening
- Concurrency: single-run semaphore (don't fire Phase 2 while Phase 2 already running)
- State machine: track current run state, pass through phases per cascade
- Logging: structured to PostgreSQL OR journald with web-accessible tail
- Error surfacing: structured error categories (substrate-fail, gauntlet-fail, LLM-fail, system-fail)

Mac-side concerns (in Phase β initial state):
- Mac runs a lightweight control daemon listening for Pi-routed trigger requests
- Daemon authenticates Pi requests
- Daemon spawns engine subprocess per trigger
- Daemon proxies subprocess stdout/stderr back to Pi for log streaming

Future PC-side concerns (when γ lands):
- PC runs equivalent control daemon
- Pi routes to PC when workload weight favors PC (per Phase γ runner selection)

### 1.3 UI affordances per phase tile

- **Status badge:** ✅ idle (last run timestamp + status) / ⏳ running (progress %) / ❌ error (latest error summary)
- **Fire button:** primary action; fires this phase
- **Cascade button:** secondary action; fires from this phase through end
- **History link:** opens detail view with last 10 runs
- **Live log link (during run):** opens streaming log panel
- **Abort button (during run):** halt current run

### 1.4 Empirical-evidence triggers for Phase β architectural commitment

Per recognition-validate-commit discipline (gandalf OP § 3.4):

1. **Pi Phase 1 Samba file sharing operational** for ≥1 week (canonical commitment doc § 6 Phase 1 acceptance)
2. **Pi Phase 2 HTTP API (data endpoints) operational** — control endpoints extend the same FastAPI service; depends on Phase 2 baseline
3. **Pattern-B design session** with Matt on dashboard control plane spec — gesture vocabulary, abort semantics, concurrency model, auth approach
4. **Phase α dashboard in production use** for ≥1 week — surfaces UX learnings that inform β scope
5. **Identified pain points from current Mac-only engine runs** — what does Matt actually want to trigger from anywhere? Probably specific surfaces (Wave-S regen / Wave B re-naming / Phase 5 cohesion re-fire / full-season cascade-resumption)

When triggers 1-5 satisfied, Phase β moves from recognition record to canonical-promotion candidate.

---

## 2. Phase γ — Runner decentralization (preserved design intent)

### 2.1 Scope description

Engine runs on Mac OR Pi OR PC interchangeably. Dashboard picks runner per workload weight. Engine code becomes machine-portable.

### 2.2 Per-workload runner selection (preliminary heuristics)

| Workload | Recommended runner | Why |
|---|---|---|
| **Wave-S regen** (single LLM call, ~$0.015, ~10sec) | Pi | Lightweight; Pi's network proximity to LLM proxy fastest |
| **Wave A faction re-naming** (3-4 LLM calls, ~$0.02, ~30sec) | Pi | Lightweight; same Pi-proximity benefit |
| **Wave B character re-naming** (~30-50 LLM calls, ~$0.34, ~50sec) | Pi | Same family; Pi orchestrates LLM proxy + writes results to share |
| **Phase 5 cohesion re-fire** (Path X re-fire on existing archive) | Pi or Mac | Modest workload; either works |
| **Full season cascade Phase 2-7** (gauntlet sim + emit) | PC | Heavy gauntlet sim benefits from i7-14700F 28 threads (3-5× faster than Mac) |
| **Engine generation experiments** (math hotspot dev work) | Mac | Familiar dev environment; agent CLI integration; iteration speed |
| **Design + agent orchestration** | Mac | Existing seam; doesn't change |
| **Visual coalescence Phase 6** (when implemented) | PC | GPU-bound work; Mac has no equivalent GPU; Pi has integrated GPU but inadequate |

### 2.3 Engine refactor requirements

Engine codebase needs:
- `--runner` flag selecting target machine
- Worker daemon per machine (Mac control daemon + Pi worker + PC worker)
- Common interface for spawning runs + streaming output
- Substrate routing: which artifacts land where per runner (composes with Pi shared folder per § 1.2 canonical commitment)
- Cross-machine state synchronization: how does dashboard know current state of run on PC vs Mac vs Pi
- Engine repo: Python remains canonical implementation; machine-portability achieved via venv + requirements.txt pinning + cross-platform Python

### 2.4 Significant engine work — not light

Phase γ is a substantial engine refactor. Estimate ~2-4 weeks of focused star-lord + rocket + gamora coordination. Worth doing eventually when:
- Mac engine runs become bottleneck for design iteration cadence
- PC's i7-14700F + 32GB RAM + Lumen/Nanite capacity becomes underutilized
- Wave 4 + Cycle 15+ scaling work needs sustained heavy compute

### 2.5 Empirical-evidence triggers for Phase γ architectural commitment

1. **Phase β control plane operational** for ≥2 weeks — UX validates the trigger-based workflow
2. **Mac engine run time measured as bottleneck** — specific workloads identified where PC would be 3-5× faster materially affects cadence
3. **Pattern-B design session** with Matt on engine machine-portability scope — specific workloads to decentralize first, abort semantics across machines, cross-machine state model
4. **Wave 4 + Cycle 15+ scaling work scoped** — gear_instance_generator at scale + Phase 6 visual coalescence + multi-season cascades benefit from PC compute meaningfully
5. **Engine machine-portability prototype** demonstrates Python venv + dependencies cross-platform on Pi + PC (likely smooth but verify)

When triggers 1-5 satisfied, Phase γ moves to canonical-promotion candidate. **Significant scope — at minimum a 2-4 week dedicated engine workstream.**

---

## 3. Composition with existing canon

### 3.1 Composes with Pi-middleware augmentation principle

Per `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` § 1.2 augmentation-not-replacement principle: Pi handles cross-machine concerns. The control plane + dashboard is canonically cross-machine — Mac fires now; PC could fire in γ; future-Matt-mobile-dashboard fires from anywhere. Pi-hosted control plane is the architecturally honest path.

### 3.2 Composes with Pi Phase 2 HTTP API scope expansion

Original Pi Phase 2 scope (per HTML implementation plan § 5) was "FastAPI HTTP API for Unreal dynamic queries" — pretty narrow. Phase β adds control plane endpoint family. Together with the LLM proxy recognition record (`canonical/story/2026-05-30-pi-llm-proxy-architecture-recognition.md`), **Pi Phase 2 expands from narrow data API to the architectural pivot point of the whole rollout: Pi as the cross-machine application layer.**

### 3.3 Composes with PC's i7-14700F + 32GB DDR5 capacity

Per PC profile in HTML § 9.1: i7-14700F exceeds CEILING tier recommendation; 28 threads + DDR5-5600 (post-XMP). PC compute capacity dramatically exceeds Mac mini's 8GB unified-memory machine. Phase γ runner decentralization unlocks this capacity — heavy gauntlet sims that take ~30sec on Mac may take ~10sec on PC.

### 3.4 Composes with cascade-r4 § 12 hero+gear flow

Drax's hero+gear extraction (cascade-r4 § 12) currently triggered via manual dispatch. Phase β control plane would expose "fire § 12 hero generation" as a button in the dashboard. Matt clicks; Pi orchestrates drax sub-agent invocation; result returns to dashboard. Cleaner workflow than manual dispatch authoring.

### 3.5 Composes with Hidden-Spirit-Discovery long-term vision

Per HTML engine-analysis § 23 Hidden-Spirit-Discovery recognition record: character creation surface via gesture interaction. The dashboard control plane is the **development-side analog** — Matt as designer fires pipeline blocks via UI affordances, observes substrate emerge, refines. Same pattern, different audience (designer vs player).

---

## 4. Empirical-evidence triggers for re-engagement (consolidated)

Per recognition-validate-commit discipline (Disc #21):

| Phase | Triggers for canonical-promotion |
|---|---|
| **α (alpha)** | Drax dispatch fires NOW per separate KR routing; not deferred |
| **β (beta)** | Pi Phase 1 + Phase 2 baseline operational + Phase α in production use ≥1 week + Pattern-B design session + identified pain points from current workflow |
| **γ (gamma)** | Phase β operational ≥2 weeks + Mac engine bottleneck quantified + Pattern-B design session + Wave 4 / Cycle 15+ scaling work scoped + machine-portability prototype |

---

## 5. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-30 verbatim "we should author phase β & γ to preserve them for later."

**For:** durable preservation of the dashboard maturation design intent at canonical layer so that future Pattern-B engagement has a substrate to consume. Phase α dispatch authored separately as immediate drax work-item per Matt 2026-05-30 verbatim "draft the work for KR to begin sending drax out for phase α now."

**Companion artifacts:**
- `canonical/story/2026-05-30-pi-llm-proxy-architecture-recognition.md` — second preserved recognition record (LLM API call centralization)
- KR fire prompt for drax Phase α dashboard (in gandalf session output; Matt-paste)
