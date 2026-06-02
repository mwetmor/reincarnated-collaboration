# Dispatch — 2026-06-01 — drax — IA-3 Phase 1: Drax MVP V1 integration

**From:** knight-rider (immediate-arc orchestrator)
**To:** drax (player-facing presentation seam — reincarnated-loadout React/Vite/Tailwind + reincarnated-demo Pixi.js)
**Approved by:** Matt 2026-06-01 strategic reset + pre-commitment ratification LOCK F (drax MVP-discipline; existing components ONLY; no new UI; defer all UI design questions to post-immediate-arc Pattern B) + LOCK G (autonomous Vercel deployment) + IA-1 V1 close (season_000042 produced)
**Workstream tag:** `IA-3-drax-MVP-integration`
**Phase / phase-gate:** IA-3 Phase 1 (workstream open + V1 integration scaffolding)
**Estimated effort:** ~1-2 sessions (data-loading layer + component wiring; existing components only)
**Acceptance:** V1 season output (season_000042) renders in reincarnated-loadout + reincarnated-demo via existing components; integration scaffolding documented

---

## 1. Context

IA-1 V1 SUCCESS — engine produced season_000042 at `~/Games/reincarnated-engine/seasons/season_000042/` (engine sha `cda99a5`; 1728.7s; validation PASSED; 5 classes / 44 monsters / 200 gear / 49.33% trial defeat; LLM-named cosmological_vocabulary with 8 slot fills + 3 pair rationales coalesced theme="forge").

Per LOCK F MVP-discipline: drax consumes V1 output via data-loading layer + existing components only. **NO new UI components. NO UI redesign. NO new feature additions beyond data-loading layer.**

Per LOCK G: autonomous Vercel preview deployment on drax MVP completion.

**Authoritative readings:**
- **IA-1 V1 close record (V1 substance):** `agentic_orchestration/ia-1-v1-close-record-2026-06-01.md`
- **Pre-commitment ratification (LOCK F + LOCK G + escape clause):** `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md`
- **Immediate-arc workstream queue:** `agentic_orchestration/immediate-arc-workstream-queue-2026-06-01.md`
- **Engine-repo V1 season output:** `~/Games/reincarnated-engine/seasons/season_000042/`
- **WS1A.Q18 canonical lock (vocabulary referenced for context):** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`

---

## 2. Scope (per LOCK F MVP-discipline)

### 2.1 Season output paths drax consumes (per IA-1 V1 close record § 6.2)

From `~/Games/reincarnated-engine/seasons/season_000042/`:
- `manifest.json` — header + cosmological_vocab summary
- `cosmological_vocabulary.json` — LLM-named slot fills + pair rationales
- `classes/*.json` — 5 class definitions (class_0001 through class_0005)
- `monsters/*.json` — 44 monster definitions
- `gauntlet_recipe.json` — gauntlet structure (12 L50 / 5 L33 / 5 L17)
- `gear_pool_staged.json` — 200 gear items (120 rare+)
- `trial.json` — trial configuration
- `fights.jsonl` — 41.8MB fight simulation telemetry (probably NOT for V1 MVP integration; flag if needed)
- `validation_report.json` — per-class convergence data
- `reference_gauntlet.json` — additional context

### 2.2 reincarnated-loadout MVP integration (React/Vite/Tailwind; Vercel-deployed)

**Existing component layouts ONLY:**
- Use existing loadout pages + components
- Wire data-loading layer to consume season_000042 JSON files
- Render kits + skills + weapons + factions per existing component shape
- DO NOT add new UI components
- DO NOT redesign existing components

**Data-loading layer scope:**
- Load season manifest + sub-files from engine repo path (or staged copy in loadout repo `public/` per drax-side judgment)
- Parse JSON; type per existing TypeScript shapes (extend types additively per LOCK J § 1 schema extension if needed)
- Surface to existing components

### 2.3 reincarnated-demo MVP integration (Pixi.js demo)

**Existing engine page Pixi.js components ONLY:**
- Use existing engine page layouts + Pixi.js renderers
- Wire data-loading layer to consume season_000042
- Render gameplay-adjacent data per existing component shape
- DO NOT add new UI components

### 2.4 What's IN scope (MVP)

- Data-loading layer (new code; consumes season output JSON; types per existing shapes)
- Component wiring (pass loaded data to existing components)
- Type additions (additive per LOCK J § 1; new schema fields where season output has fields existing types don't cover)
- Bug fixes if data-loading exposes existing component bugs (note for post-immediate-arc Pattern B)
- Routing / page additions IF strictly necessary to load season-data (minimal; existing page structure preferred)

### 2.5 What's OUT of scope (DEFERRED to post-immediate-arc Pattern B)

- NEW UI components
- UI redesign
- NEW feature additions beyond data-loading
- Visual design changes
- Cosmetic styling changes
- New pages/routes UNLESS strictly necessary for season-data loading
- Auth / user state changes
- Performance optimizations (unless data-loading exposes critical perf issues)

---

## 3. Decision authority

Per LOCK F: drax MVP scope decisions + data-loading layer implementation + component wiring are YOURS per drax seam authority. Matt is NOT in the loop. UI design questions deferred to post-immediate-arc Pattern B.

Per LOCK G: Vercel preview deployment autonomous on drax MVP completion.

**Escape-clause triggers (escalate to KR + Matt):**
- New UI component proposal beyond MVP scope (defer to post-immediate-arc)
- Architectural amendment (e.g., season-output schema change request → goes through star-lord output pipeline; semantic change escalates)
- Substantial bugs in existing components blocking integration (escalate for triage)
- Cross-seam contract SEMANTIC changes (additive consumer-format per LOCK J § 4 is autonomous)

**Non-escalation surfaces (you handle):**
- Data-loading layer implementation choices (React Query / SWR / vanilla fetch / etc.)
- TypeScript type additions (additive per LOCK J § 1)
- Vercel preview deployment configuration
- Existing-component minor bug fixes encountered during integration

---

## 4. Output expectations

### 4.1 reincarnated-loadout repo (`~/Games/reincarnated-loadout/`)
- Data-loading layer code (per your implementation choice)
- Type additions (additive TS shapes)
- Component wiring (existing components consume season data)
- Vercel preview deployment configuration verified

### 4.2 reincarnated-demo repo (`~/Games/reincarnated-demo/`)
- Data-loading layer code
- Component wiring (existing Pixi.js components consume season data)
- Vercel preview deployment configuration verified

### 4.3 Meta-repo
- IA-3 Phase 1 close summary at `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md`:
  - Integration verdict (SUCCESS / PARTIAL-SUCCESS / BLOCKED)
  - reincarnated-loadout integration state (Vercel URL + summary)
  - reincarnated-demo integration state (Vercel URL + summary)
  - Existing components used per repo
  - Schema additions per LOCK J § 1 (if any; brief)
  - Existing-component bugs surfaced (note for post-immediate-arc)
  - Notable observations for V2 iteration

### 4.4 Auto-commits + auto-push
- reincarnated-loadout repo: data-loading + wiring commits
- reincarnated-demo repo: data-loading + wiring commits
- Meta repo: IA-3 P1 close summary
- All pushed per cycle-push pattern + Matt strategic reset push authorization
- Vercel auto-deploys triggered by pushes per established pattern

---

## 5. Cross-seam contract change? (Principle 6)

**Answer:** Maybe-applicable. Drax consumes engine-output season JSON. If season output schema additions are needed (additive consumer-format per LOCK J § 4), star-lord coordination required for output pipeline format adjustments (autonomous per LOCK J § 4; cross-seam MIGRATION.md per ADR-004 if applicable).

If V1 season output schema is sufficient AS-IS for MVP load: no cross-seam contract change.

**Round-trip:** required IF additive output-schema amendment surfaces; not applicable if AS-IS sufficient.

---

## 6. Acceptance criteria

- [ ] season_000042 data loads in reincarnated-loadout (verified Vercel preview)
- [ ] season_000042 data loads in reincarnated-demo (verified Vercel preview)
- [ ] Existing components render the loaded data
- [ ] No new UI components added (verify against existing component inventory)
- [ ] Type additions additive only per LOCK J § 1
- [ ] Existing-component bugs surfaced + noted (not pre-fixed unless trivially blocking)
- [ ] IA-3 P1 close summary authored
- [ ] Auto-commit both player-surface repos + meta repo
- [ ] Auto-push + Vercel auto-deploy verified

---

## 7. Out of scope

- New UI components (DEFERRED post-immediate-arc Pattern B)
- UI redesign
- IA-3 Phase 4 V2 iteration (post-IA-2 close + IA-1 V2 re-fire)
- IA-2 workstreams (parallel; elrond + gandalf seams)
- IA-1 V2 re-fire (depends on IA-2 close)
- Long-arc deferred items

---

## 8. References

- All authoritative readings listed in § 1
- **Pre-commitment ratification:** `agentic_orchestration/immediate-arc-pre-commitment-ratification-2026-06-01.md`
- **IA-1 V1 close record:** `agentic_orchestration/ia-1-v1-close-record-2026-06-01.md`
- **reincarnated-loadout repo:** `~/Games/reincarnated-loadout/`
- **reincarnated-demo repo:** `~/Games/reincarnated-demo/`
- **drax OP:** `agentic_orchestration/operating-procedures/drax.md`

---

## Completion record (you append at completion)

---

## Completion record
**Completed:** 2026-06-01
**Integration verdict:** SUCCESS
**reincarnated-loadout commit + Vercel URL:** `75417f8` — data/season_000042/ (manifest + 5 classes + gear_pool) — Preview: `https://reincarnated-loadout-dkmj99vb8-matthew-wetmore-s-projects.vercel.app`
**reincarnated-demo commit + Vercel URL:** `0e511c4cb` — public/seasons/season_000042/ + loader.ts SEASON_IDS + engine.ts blink geometry — Preview: reincarnated-demo is fetch-from-R2 in production (local dev serves from public/; no Vercel deploy on demo side)
**Existing components used:** Loadout — useSeasonData (glob auto-picks up new data dir); Loadout.tsx + Sample.tsx (existing season selector + class display). Demo — existing loader.ts fetch pattern; SEASON_IDS expands to include season_000042; no new Pixi.js UI.
**Schema additions:** 1 additive — `'blink'` added to GeometryType union in reincarnated-demo/src/types/engine.ts (season_000042 emits blink geometry type; not in prior union).
**Existing-component bugs surfaced:** (1) class_0006–class_0011 lack is_act_boss:true — excluded from staging, noted for post-immediate-arc; (2) resolveElementDisplay null-guard needed for manifest.elements:null — mitigated at data-staging with elements stub, noted for post-immediate-arc; (3) blink geometry type new (not blocking; additive fix applied).
**IA-3 P1 close summary (meta repo):** `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md`
**Notable observations for V2 iteration:** cosmological_vocabulary has 8 slots (impact/radiance/penumbra/resonance not yet surfaced); CosmologyPairBlock already exists for pair rationales; validation_report.json has per-tier win-rate data for analytics; fights.jsonl deferred.
**Routing back to KR:** IA-3 P1 SUCCESS — IA-3 P4 V2 iteration awaits IA-1 V2 close + IA-2 close. No escape-clause triggers fired.

After your completion, IA-3 Phase 2-3 essentially complete on drax MVP scope (deployment is autonomous per LOCK G). IA-3 P4 V2 iteration awaits IA-2 close + IA-1 V2 re-fire.

---

**End of IA-3 Phase 1 drax MVP integration dispatch.**
