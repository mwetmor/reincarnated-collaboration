# Cycle 16 — Engine Architectural Amendment (EAA) Chain — Wave State

**STATUS:** OPEN (wave-open authoring complete; Phase 1 fan-out pending Gate-1 PASS)
**Date opened:** 2026-06-02
**Owner:** knight-rider (orchestrator)
**Authority:** Matt 2026-06-02 Pattern B substantive design session ratification (canonical record at `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`); gandalf transmission with Locks A-P pre-commitment package
**Cycle directory:** `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/`
**Total chain horizon:** ~10-20 sessions wall-clock per canonical record § 7.1
**Wave-close criterion:** EAA-8 wave-close record at `canonical/story/2026-06-XX-eaa-chain-wave-close-record.md` PASS + Matt strategic re-engagement signal

---

## 0. Architectural directive (verbatim from gandalf transmission 2026-06-02)

Implement the engine architectural amendment per `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3. Scope:

- Retire R8 inverted-mode theme coalescence (Stage 1 skip-flag pattern; Stage 2 code removal deferred per LOCK M)
- Retire cosmological_vocabulary slot-fill mechanism (same two-stage pattern)
- Implement kit-space-expansion infrastructure (per-kit JSON entries; NOT per-season manifest)
- Implement WS1A.4-lite per-skill flavor-or-canonical LLM judgment (Q18 vocabulary consumed at per-skill flavor decision)
- Implement kit-space chronicle (parameter expansion event records)
- Cross-seam contract amendments per ADR-004 MIGRATION discipline
- First kit-space-expansion generation fire (20-30 kits with WS1A.4-lite + modern caster weapons in substrate)
- Drax MVP reframe (consume kit-space output; existing components only; MVP-discipline)
- Engine page MVP reframe (chronicle kit-space-expansion via existing EngineStatePipelineFlow component)

**End state at chain close:**
- 20+ kits generated into continuous kit space
- Per-skill flavor-or-canonical naming via Q18 vocabulary
- Modern caster weapon substrate already in pool (WS2.P2 ingested)
- Drax MVP renders kits via existing component layouts
- Engine page chronicles the kit-space-expansion event
- Canonical commitment fully operationalized at engine + drax layer

**Matt stated chain-close goal:** "20+ characters, similar to Cycle 14 output but also with LLM named skills and with those skill having names influenced by flavor elements where appropriate. The new engine gen should also have the modern caster weapon population fix."

---

## 1. Pre-commitment package (Locks A-P)

### Locks A-J (PRESERVED from IA chain per gandalf/notes/2026-06-01-session-close-out-IA-chain-resume.md)

- **LOCK A** rocket+star-lord engine readiness autonomy
- **LOCK B** elrond audit autonomy
- **LOCK C** gandalf-as-subagent substrate-curation authority
- **LOCK D** gandalf canonical authoring authority
- **LOCK E** elrond ingest autonomy
- **LOCK F** drax MVP-discipline (load JSON + existing component layouts; no UI redesign)
- **LOCK G** Vercel auto-deploy on drax push
- **LOCK H** standard gandalf design-quality audit at workstream close (note-only)
- **LOCK I** seam-owner authority for cross-cycle scope amendments
- **LOCK J** bounded-scope architectural amendment authority (ADDITIVE-ONLY discipline; ADDITIVE-AND-REVERSIBLE heuristic)

### Locks K-P (NEW for EAA chain)

- **LOCK K** engine schema design authority (rocket + elrond + star-lord; kit-space output schema + chronicle schema + WS1A.4-lite vocabulary-consumption schema; ADR-004 MIGRATION per cross-seam touch; jack-ryan Gate-1+Gate-2 standard)
- **LOCK L** WS1A.4-lite LLM prompt design authority (gandalf-as-subagent; iterate via jack-ryan Gate-2 reviews; escape clause = 2+ Gate-2 BLOCKs → Matt aesthetic judgment)
- **LOCK M** R8 + cosmological_vocabulary retirement scope (Stage 1 skip-flag pattern immediately; Stage 2 code removal deferred to later cleanup workstream; escape clause if Stage 1 surfaces unforeseen dependency)
- **LOCK N** first kit-space-expansion generation parameters (KR + rocket + star-lord; n_kits=20-30; pool.json v1.1 + WS2.P2 magic weapons substrate; WS1A.4-lite active; skip-flags active; output schema per LOCK K; no Matt-touch required)
- **LOCK O** drax + engine page reframe MVP-discipline (consume kit-space output via existing components; NO new UI components; NO chernoff celestial body UI — defers to MM-P1 design session; escape clause if existing components fundamentally don't support new data shape)
- **LOCK P** MM-P1-independence (EAA chain proceeds independently of MM-P1 design session; MM-P1-specific UX out-of-scope; if MM-P1 surfaces engine-architecture-impacting decisions, route to Matt — not auto-incorporated)

### Updated escape clause (7 items)

KR escalates to Matt for:

1. Engine architectural changes BEYOND canonical record § 3 scope (amendments to architectural commitment itself)
2. WS1A.4-lite LLM prompt design BLOCK after 2+ iterations (per LOCK L escape clause)
3. Generation output quality substantively below expectations (>10% evidently-non-grammatical-or-non-sensical at per-skill flavor naming)
4. MM-P1 design session surfacing engine-architecture-impacting decisions (per LOCK P)
5. ADR-002 architectural-commitment-tier scope changes beyond LOCK J ADDITIVE-ONLY discipline (semantic amendments to canonical-7+1 / BC axes / Q18 lock / substrate composition policy / foundation layer / canonical/library_schema)
6. Cross-seam contract SEMANTIC changes (additive output-format extensions pre-commit per LOCK K)
7. Strategic direction questions OUTSIDE EAA chain scope (long-arc reactivation / pivot direction / scope expansion beyond canonical record § 3)

---

## 2. Workstream decomposition (EAA-1 through EAA-8)

Workstream decomposition is ADVISORY per gandalf transmission; KR may amend per orchestration judgment within pre-commitment locks.

### Phase 1 (parallel fire after wave-open Gate-1 PASS)

#### EAA-1 — WS1A.4-lite implementation

| Property | Value |
|---|---|
| **Owner** | star-lord (LLM prompt + per-skill judgment integration) + rocket (engine skill-naming pipeline integration) |
| **Sub-agent** | gandalf-as-subagent for prompt template authoring per LOCK L |
| **Scope** | Per-skill LLM judgment fires per-skill; decides flavor-or-canonical binary; if flavor, picks from kit's primary element's Q18 pool |
| **Inputs** | pool.json v1.1 (Q18 lock state); canonical record § 3.2 example pattern (Shadow Necromancer 6-skill); canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md |
| **Output** | LLM prompt template + per-skill integration into skill-naming pipeline; jack-ryan Gate-2 reviews prompt fitness |
| **Estimated** | ~3-5 sessions including prompt iteration |
| **Gates** | jack-ryan Gate-1 pre-fire on dispatch + Gate-2 on each prompt iteration |

#### EAA-2 — Engine skip-flag pattern for R8 + cosmological_vocabulary

| Property | Value |
|---|---|
| **Owner** | rocket + star-lord |
| **Scope** | Engine flags (skip_theme_coalescence + skip_cosmological_vocabulary OR combined skip_legacy_seasonal_overlay) bypass R8 + cosmological mechanisms when set; old behavior remains in code for legacy needs per LOCK M Stage 1 |
| **Inputs** | season_orchestrator.py R8 inverted-mode pipeline; canonical/historical/19-llm-call-map.md R8 reference; cosmological_vocabulary mechanism |
| **Output** | Engine flag-based bypass; new generation fires with flags active; jack-ryan Gate-2 confirms bypass clean |
| **Estimated** | ~1-2 sessions |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 post-implementation |

#### EAA-3 — Kit-space output schema (additive)

| Property | Value |
|---|---|
| **Owner** | rocket + elrond + star-lord per LOCK K |
| **Scope** | Per-kit JSON entry schema (NOT per-season manifest); additive schema extensions; backward-compatible; ADR-004 MIGRATION.md authored per cross-seam touch |
| **Inputs** | pool.json schema patterns; lineage tags per WS1A.Q18 model; existing season manifest schema for backward-compat reference |
| **Output** | Per-kit JSON schema spec + MIGRATION.md cross-seam contract documentation |
| **Estimated** | ~2-3 sessions including jack-ryan Gate cycles |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 post-schema-spec |

#### EAA-4 — Kit-space chronicle infrastructure

| Property | Value |
|---|---|
| **Owner** | elrond + star-lord per LOCK K |
| **Scope** | Chronicle schema for parameter expansion event records; engine emits chronicle entry on each kit-space-expansion fire |
| **Inputs** | canonical record § 3.4 chronicle properties; existing engine telemetry/output infrastructure |
| **Output** | Chronicle schema + emission integration; jack-ryan Gate-2 confirms additive |
| **Estimated** | ~1-2 sessions |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 post-implementation |

### Phase 2 (sequential after Phase 1 PASS)

#### EAA-5 — First kit-space-expansion generation fire

| Property | Value |
|---|---|
| **Owner** | KR + rocket + star-lord per LOCK N |
| **Scope** | 20-30 kits generated into kit space with WS1A.4-lite + skip flags + modern caster weapons in substrate; elrond ingests |
| **Inputs** | EAA-1 WS1A.4-lite available; EAA-2 skip flags active; EAA-3 output schema ratified; EAA-4 chronicle infrastructure available; pool.json v1.1 + WS2.P2 substrate |
| **Output** | First kit-space-expansion generation event + 20-30 kit entries in kit space + chronicle entry recording the event |
| **Estimated** | ~1-3 sessions including generation execution time |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 on generation output quality (per LOCK L iteration discipline) |
| **Blocked-by** | EAA-1 + EAA-2 + EAA-3 + EAA-4 all PASS |

### Phase 3 (parallel after EAA-5 PASS)

#### EAA-6 — Drax MVP reframe (consume kit-space)

| Property | Value |
|---|---|
| **Owner** | drax per LOCK O |
| **Scope** | reincarnated-loadout consumes kit-space JSON entries via existing components; kit browser + per-kit detail view; NO new UI components; NO chernoff celestial body UI |
| **Inputs** | EAA-5 kit-space output available |
| **Output** | Loadout app renders kits from kit-space; Vercel preview deploy per LOCK G |
| **Estimated** | ~2-4 sessions |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 post-implementation |
| **Blocked-by** | EAA-5 PASS |

#### EAA-7 — Engine page MVP reframe (chronicle kit-space-expansion)

| Property | Value |
|---|---|
| **Owner** | drax + reincarnated-loadout per LOCK O |
| **Scope** | Engine page renders kit-space-expansion event via existing EngineStatePipelineFlow component pattern |
| **Inputs** | EAA-5 kit-space output + EAA-4 chronicle available |
| **Output** | Engine page chronicles kit-space-expansion; can parallel with EAA-6 |
| **Estimated** | ~2-3 sessions |
| **Gates** | jack-ryan Gate-1 pre-fire + Gate-2 post-implementation |
| **Blocked-by** | EAA-5 PASS + EAA-4 PASS |

### Phase 4 (wave-close)

#### EAA-8 — Wave-close discipline

| Property | Value |
|---|---|
| **Owner** | KR + gandalf design-quality audit + jack-ryan Gate-2 wave-close |
| **Output** | KR wave-close record at `canonical/story/2026-06-XX-eaa-chain-wave-close-record.md`; gandalf design-quality audit; jack-ryan engineering-disciplines amendments (if applicable); ground-state § 1 update; strategic re-engagement signal to Matt |
| **Estimated** | ~1-2 sessions |
| **Blocked-by** | All EAA-1 through EAA-7 PASS |

---

## 3. Workstream status table

| WS | Status | Notes |
|---|---|---|
| **Wave-open dispatch** | ✅ AUTHORED | KR (this cycle) |
| **Wave-open Gate-1** | ✅ COMPLETE (PASS-with-INFO) | jack-ryan; INFO-2 + INFO-3 incorporated in Phase 1 dispatches; INFO-1 deferred to Phase 3 authoring |
| **Phase 1 batch Gate-1** | ✅ COMPLETE (PASS-with-INFO) | jack-ryan; 3 amendments incorporated in EAA-2 + EAA-3 dispatches before specialist fire |
| **EAA-1** WS1A.4-lite implementation | ✅ COMPLETE | sha=54215d8 / tag=star-lord/v1.4-eaa-1-ws1a-4-lite-1; smoke=34/34 PASS; Gate-2=PASS-with-INFO (3 INFOs, 0 BLOCKs, 0 WARNs); finding at `qa/findings/2026-06-02-eaa-1-ws1a-4-lite-gate-2.md`; rocket pipeline integration pending (co-owner scope) |
| **EAA-2** Engine skip-flag pattern | ✅ COMPLETE | sha=c56db88 / tag=rocket/v1.4-eaa-2-skip-flag-1; smoke=PASS (5 classes, 30 fights, no_coalesce + both skips=True; season_theme_element=None; cosmological_vocabulary=None; classes=5; exit 0); Gate-2=PASS (jack-ryan; 2 INFOs non-blocking; 0 BLOCKs, 0 WARNs); flag-naming=two separate flags; MIGRATION.md authored; escape clause NOT triggered; finding at `qa/findings/2026-06-02-eaa-2-skip-flag-gate-2.md` |
| **EAA-3** Kit-space output schema | 🟡 ELROND-SIDE COMPLETE; awaiting rocket DRAFT + Gate-2 | Owner: rocket + elrond + star-lord. elrond joint spec at `elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md`; MIGRATION.md v1.8 at `research/curated/MIGRATION.md`; FK format LOCKED (`kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>` per pre-existing coordination note); kit_id format LOCKED (`kit_<primary>_<seq6>`); 5 iteration points named for rocket alignment per LOCK K DRAFT discipline |
| **EAA-4** Kit-space chronicle infrastructure | 🟡 ELROND-SIDE SCHEMA + STORAGE LOCKED; awaiting star-lord emit integration + Gate-2 | Owner: elrond + star-lord. elrond joint spec at `elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` § 3 (Option α filesystem source-of-truth + Option β-light shadow tables; chronicle JSON shape § 3.4; shadow-table DDL § 3.5); MIGRATION.md v1.8 at `research/curated/MIGRATION.md` |
| **EAA-5** First kit-space-expansion generation fire | ⏸ pending Phase 1 PASS | Owner: KR + rocket + star-lord |
| **EAA-6** Drax MVP reframe | ⏸ pending EAA-5 PASS | Owner: drax |
| **EAA-7** Engine page MVP reframe | ⏸ pending EAA-5 + EAA-4 PASS | Owner: drax |
| **EAA-8** Wave-close | ⏸ pending all PASS | Owner: KR + gandalf + jack-ryan |

---

## 4. Active dispatches

| Dispatch | Path | Status |
|---|---|---|
| EAA wave-open | `dispatches/2026-06-02-cycle-16-eaa-engine-architectural-amendment-wave-open.md` | ✅ AUTHORED |
| EAA wave-open Gate-1 finding | `qa/findings/2026-06-02-eaa-wave-open-gate-1.md` | ✅ AUTHORED (PASS-with-INFO) |
| EAA Phase 1 batch Gate-1 finding | `qa/findings/2026-06-02-eaa-phase-1-batch-gate-1.md` | ✅ AUTHORED (PASS-with-INFO; 3 amendments incorporated) |
| EAA-1 WS1A.4-lite | `dispatches/2026-06-02-eaa-1-ws1a-4-lite-implementation.md` | ✅ COMPLETE (star-lord seam; Gate-2 PASS-with-INFO; sha=54215d8; rocket pipeline integration pending) |
| EAA-2 skip-flag | `dispatches/2026-06-02-eaa-2-engine-skip-flag-retirement.md` | 🔥 FIRING (rocket+star-lord) |
| EAA-3 kit-space schema | `dispatches/2026-06-02-eaa-3-kit-space-output-schema.md` | 🔥 FIRING (rocket+elrond+star-lord) |
| EAA-4 chronicle | `dispatches/2026-06-02-eaa-4-kit-space-chronicle-infrastructure.md` | 🔥 FIRING (elrond+star-lord) |

---

## 5. Push discipline

Matt 2026-06-02 explicit cycle-push authorization for EAA chain (extends IA-chain push-pattern precedent). All KR-orchestrated commits auto-push to remote on standard cycle-push cadence. Vercel auto-deploy per LOCK G on drax push.

---

## 6. State preservation

Per gandalf transmission § STATE TO PRESERVE:
- WS1A.Q18 Architecture A LOCK unchanged
- Q18 vocabulary IMMUTABLE
- BC axes unchanged
- canonical-7+1 catalog unchanged
- Substrate composition policy semantic unchanged (additive-only per LOCK J + K)
- IA chain wave-state preserved as historical (CLOSED)
- Existing seasons (season_000001-000200) preserved as historical artifacts per Path α
- All Q18-era commits + IA-chain commits preserved

---

## 7. Strategic re-engagement at chain close

KR signals Matt at EAA-8 wave-close with state summary covering:
- EAA chain complete; canonical commitment fully operationalized
- 20+ kits generated into kit space with WS1A.4-lite per-skill flavor
- Modern caster weapon substrate composed
- Drax MVP loads kit-space output
- Engine page chronicles kit-space-expansion event
- Vercel preview URL for inspection
- Strategic options for next-direction (A: MM-P1 design session; B: continue iterating EAA outputs; C: open economic-veteran problem design session; D: pivot)

---

## 8. Discipline observations queued for jack-ryan

Per gandalf 2026-06-02 canonical record § 9 (queued for jack-ryan ratification at EAA chain close):

1. Substrate-led discipline at content-engagement layer (Disc #41 composition; Realm Expansion targeting underplayed kits)
2. Player-driven over dev-driven design discipline (meta-design distinction)
3. Conscious genre-departure commitment (ARPG seasonal convention → continuous kit space + Realm Expansion; deliberate)

Plus potential discipline candidates from EAA chain execution:
- WS1A.4-lite per-skill flavor-or-canonical LLM judgment quality discipline (if prompt iteration surfaces general lessons)
- Engine R8 retirement skip-flag pattern (if successful, becomes reusable retirement pattern for future engine cleanup)

KR signals jack-ryan to ratify at EAA-8 wave-close.

---

## 9. Cross-references

- **Authoritative architectural commitment:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`
- **Ground-state oracle:** `canonical/00-ground-state.md` § 1
- **Q18 vocabulary lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **IA chain close-out resume framing:** `agentic_orchestration/gandalf/notes/2026-06-01-session-close-out-IA-chain-resume.md`
- **Q18 PG-3 ratification:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md`
- **Pool.json v1.1 substrate:** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`
- **R8 inverted-mode pipeline (to be retired):** `~/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py`
- **canonical-7+1 catalog (preserved):** `~/Games/reincarnated-engine/src/reincarnated/foundation/elements.py`
- **Engineering disciplines:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- **ADR-004 cross-seam MIGRATION discipline:** see `agentic_orchestration/GOVERNANCE.md`

---

**End of cycle-16 EAA wave-state file. Wave OPEN.**
