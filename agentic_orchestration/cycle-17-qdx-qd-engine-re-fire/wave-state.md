# Cycle 17 — QDX QD-Engine Workflow Re-Fire with WS1A.4-lite Integration — Wave State

**STATUS:** 🟢 OPEN (Phase 1 firing 2026-06-02)
**Date opened:** 2026-06-02
**Owner:** knight-rider (orchestrator)
**Authority:** Matt 2026-06-02 Pattern B substantive design session — gandalf transmission with QDX chain routing (Locks A-P preserved from EAA chain; Locks Q-T NEW for QDX scope)
**Cycle directory:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/`
**Total chain horizon:** 5-10 sessions wall-clock per gandalf transmission § COST + HORIZON SUMMARY
**Wave-close criterion:** QDX-8 wave-close record at `canonical/story/2026-06-XX-qdx-chain-wave-close-record.md` PASS + Matt strategic re-engagement signal

---

## 0. Architectural directive

The EAA chain (cycle-16; closed 2026-06-02) delivered INFRASTRUCTURE (kit-space output schema + WS1A.4-lite per-skill flavor LLM judgment + skip flags + emitter) but used **legacy `ClassGenerator`** as the generation source. The result: 25 kits with rich per-skill flavor naming but only 8 distinct kit identity types (3-4 generic per primary), no T4 selection, no faction emergence, no Pareto-from-large-pool richness.

**Matt's actual session-scope goal (verbatim from gandalf transmission):** "Cycle 14 wave-5-equivalent output" — the QD-engine workflow output per **canonical 39** (Pareto-from-large-pool + cohesion clustering faction emergence + Wave A/B identity LLM + multi-T4 selection per kit) PLUS WS1A.4-lite per-skill flavor naming applied throughout.

**THIS chain delivers that.** Wires WS1A.4-lite into QD-engine workflow's skill-naming phase + composes the full pipeline + fires it + emits to kit-space output schema (preserves Season-Archive Realm-Expansion pivot architectural commitment).

**End state at chain close:**
- ~30-40 distinct kits in `data/kit_space/` with rich identity emergence
- Each kit has unique Wave B emergent identity (no template-repeat)
- Faction emergence visible (≥3 named factions via Phase 5 cohesion)
- Multi-T4 selection populated per kit (canonical 43/44/47)
- Per-skill flavor-or-canonical naming via WS1A.4-lite + Q18 vocabulary
- Physical opt-out from WS1A.4-lite (Architecture A discipline)
- Modern caster weapons composed into appropriate kits
- Drax loadout app + engine page render the new output (Vercel deployed)

---

## 1. Pre-commitment package (Locks A-T)

### Locks A-P (PRESERVED from IA + EAA chain)

- **LOCK A** rocket+star-lord engine readiness autonomy
- **LOCK B** elrond audit autonomy
- **LOCK C** gandalf-as-subagent substrate-curation authority
- **LOCK D** gandalf canonical authoring authority
- **LOCK E** elrond ingest autonomy
- **LOCK F** drax MVP-discipline (load JSON + existing component layouts; no UI redesign)
- **LOCK G** Vercel auto-deploy on drax push
- **LOCK H** standard gandalf design-quality audit at workstream close (note-only)
- **LOCK I** seam-owner authority for cross-cycle scope amendments
- **LOCK J** bounded-scope architectural amendment authority (ADDITIVE-ONLY discipline; preserves SEMANTIC canonical integrity)
- **LOCK K** engine schema design authority for additive extensions
- **LOCK L** WS1A.4-lite LLM prompt design authority (2+ Gate-2 BLOCKs escalate)
- **LOCK M** R8 + cosmological_vocabulary skip-flag pattern (legacy preserved)
- **LOCK N** first kit-space-expansion fire parameters (n_kits range; bounded)
- **LOCK O** drax + engine page MVP-discipline (existing components only)
- **LOCK P** MM-P1-independence (engine work doesn't dictate MM-P1)

### Locks Q-T (NEW for QDX chain — gandalf transmission 2026-06-02)

#### LOCK Q — QD-engine workflow integration authority

rocket + star-lord authorized for additive integration work per LOCK J ADDITIVE-ONLY discipline:
- Wire `llm/ws1a4_lite_flavor_judgment.py` INTO Phase 5 skill naming (`generation/phase5_skill_naming.py`)
- Wire `export/kit_space_emitter.py` INTO QD-engine workflow terminal phase
- Author single-entry-point fire script (`scripts/qdx_qd_engine_re_fire_*.py`)
- All integration is ADDITIVE (no semantic changes to existing Phase 5 naming behavior for non-WS1A.4 callers; backward-compatible)
- jack-ryan Gate-1 + Gate-2 standard
- Escape clause: if integration surfaces semantic amendments to existing Phase 5 pipeline, escalate per LOCK J ADDITIVE-ONLY discipline

#### LOCK R — QDX-5 fire parameters

KR + rocket + star-lord authorized for fire parameters:
- n_candidates: Phase 2 candidate pool size (Cycle 14 wave-5 was ~650; KR-selected based on engine performance bounds; aim Cycle-14-equivalent)
- Pareto reduction target: ~30-40 surviving kits
- Cohesion clustering: ≥3 factions emerge (Phase 5b)
- Skill naming: WS1A.4-lite active per-skill (flavor-or-canonical decision + Q18 pool when flavor)
- Wave A faction naming LLM: active
- Wave B per-kit emergent identity LLM: active
- T4 selection: multi-T4 per kit (per canonical 43/44/47)
- Skip flags: skip_theme_coalescence + skip_cosmological_vocabulary defaults True (Realm Expansion architecture)
- Output schema: kit_space-entries per LOCK K
- Cost projection: $5-30 (Cycle 14 wave-5 scale; multi-hour wall-clock)
- No Matt-touch required for fire parameters within these bounds
- Escape clause: if cost projection >2× upper bound ($60+) OR kit count <20 surviving Pareto reduction, escalate

#### LOCK S — Integration-smoke-gate per Discipline #54

KR routes single-kit smoke fire BEFORE full Pareto-pool fire (per discipline ratified at EAA-8 wave-close). Smoke fire verifies:
- WS1A.4-lite integration fires correctly per-skill
- kit_space emitter accepts the QD-engine workflow output shape
- Wave A/B identity LLM produces non-template emergent identity (not "Element Archetype" generic)
- Multi-T4 selection populates per kit
- Smoke output has substantive content (non-empty skills, non-null T4)

If smoke passes, full fire proceeds. If smoke fails, iterate within seam authority per LOCK L pattern (2+ Gate-2 BLOCKs escalate).

#### LOCK T — Drax MVP refresh per LOCK O pattern

drax authorized for MVP-load-only pattern (extends LOCK O):
- reincarnated-loadout consumes new kit_space output (richer than EAA-5 v2 output; includes T4 selection + emergent identity + faction grouping)
- Render with EXISTING component layouts where possible
- Surface T4 selection if existing components support; if not, defer to post-QDX UX session per LOCK O escape clause
- Surface faction grouping if existing components support; if not, defer
- Surface emergent kit identity (kit name field) — likely existing component support
- Engine page chronicles QDX-5 fire as kit-space-expansion event
- NO new UI components; NO UI redesign
- jack-ryan Gate-1 + Gate-2 standard

### Updated escape clause (QDX scope — 9 items)

KR escalates to Matt for:

1. **Engine architectural changes BEYOND QDX integration scope** — if implementation surfaces need to amend semantic behavior of existing Phase 5 pipeline OR QD-engine workflow architecture beyond ADDITIVE-ONLY discipline (LOCK J/Q)
2. **LLM cost SUBSTANTIALLY exceeds projection** — actual cost >2× upper bound ($60+) signals cost-architecture surprise warranting Matt aesthetic-judgment on cost-vs-richness trade-off
3. **Kit count SUBSTANTIALLY BELOW expectations** — full fire produces <20 kits surviving Pareto reduction (signals Pareto-policy issue requiring substantive design call)
4. **2+ Gate-2 BLOCKs on QDX-5 fire** — substantive integration design failure; escalates per LOCK L pattern
5. **Wave B emergent identity LLM produces template-style output** (e.g., all kits named "Element Archetype" again) — signals identity LLM prompt design failure requiring Matt aesthetic judgment
6. **MM-P1 design session surfacing engine-architecture-impacting decisions** per LOCK P
7. **ADR-002 architectural-commitment-tier scope changes** beyond LOCK J ADDITIVE-ONLY discipline
8. **Cross-seam contract SEMANTIC changes** — additive output-format extensions pre-commit per LOCK K + LOCK Q; semantic changes escalate
9. **Strategic direction questions OUTSIDE QDX chain scope**

---

## 2. Workstream decomposition (QDX-1 through QDX-8)

### Phase 1 — Integration (parallel fire)

#### QDX-1 — WS1A.4-lite integration into Phase 5 skill naming

| Property | Value |
|---|---|
| **Owner** | rocket + star-lord per LOCK Q |
| **Status** | 🟢 FIRING (Phase 1) |
| **Dispatch** | `dispatches/2026-06-02-qdx-1-ws1a-4-lite-into-phase-5-skill-naming.md` |
| **Scope** | Integrate `llm/ws1a4_lite_flavor_judgment.py` into `generation/phase5_skill_naming.py`; preserve backward-compatibility for non-WS1A.4 callers |
| **Output** | `phase5_skill_naming.py` with optional WS1A.4-lite invocation; activates when `ws1a4_active=True` parameter passed |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 post-output |
| **Estimated** | ~1-2 sessions |

#### QDX-2 — kit_space_emitter wired into QD-engine workflow terminal

| Property | Value |
|---|---|
| **Owner** | star-lord + rocket per LOCK Q |
| **Status** | 🟢 FIRING (Phase 1) |
| **Dispatch** | `dispatches/2026-06-02-qdx-2-kit-space-emitter-into-qd-engine-terminal.md` |
| **Scope** | Enable QD-engine workflow output to emit to kit_space schema (`data/kit_space/`) instead of `seasons/season_NNNNNN/`; preserve legacy season output path for non-kit-space callers |
| **Output** | QD-engine workflow terminal phase supports kit_space emit path |
| **Gates** | jack-ryan Gate-1 + Gate-2 |
| **Estimated** | ~1 session |

#### QDX-3 — Single-entry-point fire script

| Property | Value |
|---|---|
| **Owner** | rocket per LOCK Q |
| **Status** | 🟢 FIRING (Phase 1) |
| **Dispatch** | `dispatches/2026-06-02-qdx-3-qd-engine-single-entry-point-fire-script.md` |
| **Scope** | `scripts/qdx_qd_engine_re_fire_*.py` orchestrating Phase 2 candidate gen → Phase 4 Pareto reduction → Phase 5 cohesion clustering → Phase 5 skill naming (WS1A.4-lite active) → Wave A faction naming LLM → Wave B per-kit emergent identity LLM → multi-T4 selection per kit → emit to kit_space schema |
| **Output** | Fireable script that produces Cycle 14-equivalent + WS1A.4-lite output in single invocation |
| **Gates** | jack-ryan Gate-1 + Gate-2 |
| **Estimated** | ~1-2 sessions |

Phase 1 PASS criterion: QDX-1 + QDX-2 + QDX-3 all jack-ryan Gate-2 PASS.

### Phase 2 — Integration smoke-gate (sequential after Phase 1 PASS)

#### QDX-4 — Integration-smoke-gate (per Discipline #54)

| Property | Value |
|---|---|
| **Owner** | KR + rocket + star-lord + jack-ryan per LOCK S |
| **Status** | ❌ NOT STARTED (gates on Phase 1 PASS) |
| **Scope** | Single-kit smoke fire (1 kit through full pipeline) before full Pareto-pool fire; verifies WS1A.4-lite integration + emitter composition + Wave A/B identity LLM + T4 selection |
| **Output** | Smoke kit JSON at `data/kit_space/kits/`; jack-ryan Gate-2 verifies per 7-criteria smoke checklist |
| **Gates on** | QDX-1 + QDX-2 + QDX-3 PASS |
| **Estimated** | ~0.5-1 session |

### Phase 3 — Full fire + verification (sequential after QDX-4 PASS)

#### QDX-5 — Full QD-engine workflow fire (THE empirical-truth-moment)

| Property | Value |
|---|---|
| **Owner** | KR + rocket + star-lord per LOCK R |
| **Status** | ❌ NOT STARTED (gates on QDX-4 PASS) |
| **Scope** | Full Pareto-pool fire (~30-40 kits surviving); multi-hour LLM execution; substantive cost ($5-30); produces Cycle 14-equivalent architectural richness + WS1A.4-lite per-skill flavor |
| **Output** | ~30-40 kits in `data/kit_space/` with full identity emergence |
| **Gates on** | QDX-4 smoke PASS |
| **Estimated** | ~1-3 sessions including generation execution |

#### QDX-6 — jack-ryan Gate-2 acceptance verification

| Property | Value |
|---|---|
| **Owner** | jack-ryan per LOCK L pattern |
| **Status** | ❌ NOT STARTED (gates on QDX-5 emit) |
| **Scope** | Verify QDX-5 output against 7-criteria: (1) Kit count 30-40 range; (2) Distinct emergent kit identities (no template-repeat); (3) Faction emergence ≥3 named clusters; (4) Multi-T4 selection populated on all kits; (5) ws1a4_flavor_rate > 0 + per-skill flavor metadata; (6) Substrate-led element distribution (not round-robin); (7) Per-skill flavor decisions thematically coherent (sample inspection) |
| **Output** | Gate-2 PASS / PASS-with-INFO / BLOCK |
| **If BLOCK** | iterate per LOCK L (seam re-fire authority on 1st BLOCK; Matt escalation on 2+ BLOCKs) |
| **Estimated** | ~0.5-1 session |

### Phase 4 — Drax MVP refresh (sequential after QDX-5 + QDX-6 PASS)

#### QDX-7 — Drax MVP refresh (loadout + engine page)

| Property | Value |
|---|---|
| **Owner** | drax per LOCK T |
| **Status** | ❌ NOT STARTED (gates on QDX-5 + QDX-6 PASS) |
| **Scope** | reincarnated-loadout consumes new richer kit_space output; reincarnated-loadout engine page chronicles QDX-5 expansion event; MVP-discipline (existing components only) |
| **Output** | Vercel deployed loadout + engine page rendering new output |
| **Gates on** | QDX-5 + QDX-6 PASS |
| **Estimated** | ~2-4 sessions |

### Phase 5 — Wave-close

#### QDX-8 — Wave-close discipline

| Property | Value |
|---|---|
| **Owner** | KR + gandalf design-quality audit + jack-ryan Gate-2 wave-close |
| **Status** | ❌ NOT STARTED (gates on QDX-7 PASS) |
| **Scope** | KR wave-close record + gandalf design-quality audit + jack-ryan engineering-disciplines.md amendments if applicable + ground-state § 1 update + strategic re-engagement signal to Matt |
| **Estimated** | ~1-2 sessions |

---

## 3. Sequencing

```
Phase 1 (parallel fire):
  QDX-1 (WS1A.4-lite into Phase 5 skill naming) — FIRING
  QDX-2 (kit_space_emitter into QD-engine terminal) — FIRING
  QDX-3 (single-entry-point fire script) — FIRING
        ↓
Phase 2 (sequential after Phase 1 PASS):
  QDX-4 (integration smoke-gate)
        ↓
Phase 3 (sequential after QDX-4 PASS):
  QDX-5 (full QD-engine fire) → QDX-6 (Gate-2 verification)
        ↓
Phase 4 (sequential after QDX-5 + QDX-6 PASS):
  QDX-7 (drax MVP refresh; Vercel deploy)
        ↓
Phase 5 (wave-close):
  QDX-8 (KR record + gandalf audit + jack-ryan ratification + Matt signal)
```

---

## 4. Cost + horizon summary

| Phase | Wall-clock | LLM cost |
|---|---|---|
| QDX-1/2/3 (integration parallel) | ~1-2 sessions | minimal (smoke tests) |
| QDX-4 (integration smoke-gate) | ~0.5-1 session | <$1 |
| QDX-5 (full fire) | ~1-3 sessions | $5-30 (Cycle 14 wave-5 scale) |
| QDX-6 (Gate-2 verification) | ~0.5-1 session | minimal |
| QDX-7 (drax MVP) | ~2-4 sessions | minimal |
| QDX-8 (wave-close) | ~1-2 sessions | minimal |
| **TOTAL** | **5-10 sessions** | **~$5-30 LLM** |

---

## 5. Push authorization

Per Matt 2026-06-02 explicit cycle-push authorization extending IA + EAA chain precedent. All KR-orchestrated commits auto-push to remote on standard cycle-push cadence. Vercel auto-deploy per LOCK G on drax push.

---

## 6. Discipline observations queued for jack-ryan QDX-8 ratification

Per QDX chain execution, candidates likely to surface:

1. **QD-engine workflow integration-via-LOCK-J ADDITIVE-ONLY** (composes with #53)
2. **Per-skill flavor LLM judgment composition with Wave A/B identity LLM** (cross-LLM-call composition discipline)
3. **Multi-pipeline (legacy ClassGenerator + QD-engine workflow) fire-script discipline** — when engine has multiple generators, explicit pipeline naming per Discipline #54 + #55 + EAA-8 generator-path-explicit-naming candidate

Plus **discipline #56 candidate from EAA chain** (generator-path explicit naming in dispatches) — QDX chain activates this DURING execution, not just queue for ratification, since it directly applies.

---

## 7. State to preserve

- All canonical commitments preserved (Season-Archive Realm-Expansion pivot; Q18 lock; Architecture A; canonical-7+1; BC axes; substrate composition policy; engineering disciplines #49-#55)
- IA chain + EAA chain wave-state files preserved as historical (CLOSED)
- EAA chain engine work preserved (WS1A.4-lite + skip flags + kit_space infrastructure all consumed by QDX chain; nothing thrown away)
- Existing seasons (`season_000001-200`) + EAA-5 v2 25 kits preserved as historical artifacts (Path α discipline; QDX-5 output is the canonical "current" kit space; EAA-5 v2 output preserved alongside as historical)

---

## 8. Cross-references

### Authoritative reading (load-bearing)
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` (architectural commitment; THE binding directive)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` (QD-engine workflow Phase 1-8 architecture — the pipeline being integrated)
- `canonical/00-ground-state.md` § 1 (current truth)
- `canonical/story/2026-06-02-eaa-chain-wave-close-record.md` (EAA chain wave-close — preceding chain; preserves engine infrastructure consumed by QDX)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (Q18 vocabulary lock; consumed by WS1A.4-lite)

### Engine integration targets
- `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py` (current Phase 5 skill naming; WS1A.4-lite must wire INTO this)
- `~/Games/reincarnated-engine/src/reincarnated/llm/ws1a4_lite_flavor_judgment.py` (the WS1A.4-lite module to integrate)
- `~/Games/reincarnated-engine/src/reincarnated/export/kit_space_emitter.py` (the kit-space emitter the QD-engine workflow output emits to)
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` (Cycle 13 wave 5 lineage; reference for fire-script architecture)
- `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py` (cohesion clustering)
- `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_t4_narration.py`
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py`

### Historical reference (richness target)
- `~/Games/reincarnated-loadout/public/engine-state/season-001/` (Cycle 14 wave-5 historical output for richness reference; Pareto + faction clusters + Wave B identity)

---

## 9. Status log

| Date | Event |
|---|---|
| 2026-06-02 | Wave-state authored by KR (this file) |
| 2026-06-02 | Wave-open dispatch authored |
| 2026-06-02 | QDX-1 + QDX-2 + QDX-3 dispatches authored |
| 2026-06-02 | jack-ryan Gate-1 routed on wave-open + Phase 1 dispatches |
| 2026-06-02 | Phase 1 fired in parallel (rocket + star-lord) |

---

**Authority composition:**
- Architectural commitment (gandalf 2026-06-02 + Matt ratification)
- KR orchestration (this file + dispatches + Gate-1 routing)
- Critique-pair coverage (jack-ryan Gate-1 + Gate-2 at every workstream)
- Specialist execution (rocket + star-lord + drax + gandalf-as-subagent + jack-ryan)
- LOCK Q ADDITIVE-ONLY integration discipline (no semantic amendments to existing Phase 5 pipeline)
- LOCK R bounded fire parameters
- LOCK S integration-smoke-gate discipline (Discipline #54)
- LOCK T drax MVP-load-only pattern

**End of QDX wave-state file (current).**
