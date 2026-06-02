# Dispatch — 2026-06-02 — EAA-6 + EAA-7 — Drax MVP reframe (sequential-within-drax)

**From:** knight-rider (orchestrator)
**Primary owner:** drax (reincarnated-loadout React/Vite/Tailwind + reincarnated-demo Pixi.js engine page)
**Co-owner:** star-lord (output pipeline reference if data-shape clarifications needed)
**Cycle:** cycle-16-eaa-engine-architectural-amendment (Phase 3 — parallel after EAA-5 PASS; sequenced sequential-within-drax per wave-open Gate-1 INFO-1)
**Authority:** Matt 2026-06-02 + Locks A-P (LOCK O active for drax MVP-discipline; LOCK G Vercel auto-deploy on push; LOCK F preserved)
**Wave tag:** `EAA-6` + `EAA-7` (combined sequential-within-drax dispatch)
**Wave-open dispatch:** `dispatches/2026-06-02-cycle-16-eaa-engine-architectural-amendment-wave-open.md`
**Wave-open Gate-1 INFO-1 disposition:** "if fired in parallel, need distinct branch scopes or sequential-within-drax ordering" — KR selects **sequential-within-drax** ordering to avoid same-repo merge collision
**State file:** `cycle-16-eaa-engine-architectural-amendment/wave-state.md`

**Predecessor closure:**
- EAA-5 v2 ✅ COMPLETE — engine `8e686bb` (`star-lord/v1.4-eaa-5-v2-class-generator-fire-1`) + meta-repo `c3e2d10`
- 25 kits + chronicle event `kse_20260602_001` landed at `reincarnated-engine/data/kit_space/`

**Estimated horizon:** ~2-4 sessions (per wave-open Phase 3 estimate)
**Gates:** jack-ryan Gate-1 pre-fire on this dispatch + Gate-2 on implementation

---

## 1. Authoritative reading (READ IN ORDER before any action)

1. `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 (continuous kit space) + § 3.4 (chronicle) + § 7.2 (drax + engine page reframe) — binding
2. Wave-open dispatch (see header) — chain context + LOCK O drax MVP-discipline
3. **Kit space substrate (READ TO UNDERSTAND DATA SHAPE):**
   - `~/Games/reincarnated-engine/data/kit_space/kit_space_chronicle.json` (chronicle event(s))
   - `~/Games/reincarnated-engine/data/kit_space/kits/kit_<primary>_<seq6>.json` (per-kit entries; 25 currently)
   - `~/Games/reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md` (schema reference)
4. **Joint design spec:** `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md` (kit_id format `kit_<primary>_<seq6>`; event_id format `kse_<YYYYMMDD>_<seq3>`)
5. **drax IA-3 close-out reference:** `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md` + `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-4-v2-iteration-close.md` — prior MVP discipline pattern + existing component inventory
6. **Existing loadout data-loading pattern:** `reincarnated-loadout/src/.../useSeasonData.ts` glob (consumed per-season manifests via Vite glob import; reference pattern for adapting to kit-space)
7. **Existing engine page pattern:** `reincarnated-loadout/src/.../EngineStatePipelineFlow.*` component (existing pipeline flow render; consumes pipeline state)

---

## 2. Scope (per LOCK O MVP-discipline)

**Two workstreams; sequential-within-drax to avoid same-repo collision:**

### EAA-6 — Loadout app consumes kit-space output (FIRST)

reincarnated-loadout React app renders kits from `data/kit_space/` via EXISTING components:
- Kit browser (list/grid view of all kits in kit_space) — via existing list/grid components
- Per-kit detail view — via existing detail components  
- Filter by primary element / cultural_tradition / period (per existing filter UI if available; otherwise simple)

**Data-loading mechanism:** adapt the existing `useSeasonData.ts` glob pattern (or equivalent) to consume `data/kit_space/kits/*.json` instead of (or alongside) per-season manifests. LOCK O permits ADDITIVE data-loading code; preserve historical season loading for V1/V2 reference.

**Component reuse mandate (LOCK O):**
- ✅ ALLOWED: adapt existing components to render kit-space data shape (props/types extensions; new useKitSpaceData hook)
- ✅ ALLOWED: minor type extensions to handle new per-kit fields (flavor_decision metadata, etc.)
- ❌ DISALLOWED: new UI component shells (no new "KitBrowser" with bespoke layout; reuse existing)
- ❌ DISALLOWED: chernoff celestial body UI (defer to MM-P1 per LOCK P)
- ❌ DISALLOWED: visual redesign (preserve existing aesthetic)

### EAA-7 — Engine page renders kit-space-expansion chronicle (SECOND; sequenced after EAA-6)

Engine page (`reincarnated-demo` Pixi.js engine page OR `reincarnated-loadout` engine page if that's where it lives — drax decides per existing routing) renders kit-space-expansion event via existing `EngineStatePipelineFlow` component pattern.

**Data-loading:** consume `data/kit_space/kit_space_chronicle.json` events[]. For now (n=1 event), render the single event. Schema accommodates future events.

**Component reuse mandate (LOCK O):**
- ✅ ALLOWED: adapt EngineStatePipelineFlow to render kit-space-expansion event data (events[] timeline view)
- ❌ DISALLOWED: new engine page redesign
- ❌ DISALLOWED: Realm Expansion event UX (out of scope; future workstream)

---

## 3. Sequencing — SEQUENTIAL-WITHIN-DRAX

Per wave-open Gate-1 INFO-1 (same-repo parallelism concern):

1. **EAA-6 lands first.** drax completes loadout kit-space integration; commits; verifies Vercel preview deploys.
2. **EAA-7 follows.** drax then adds engine page chronicle integration on top of the post-EAA-6 state. New commits stack cleanly without conflicts.

**Rationale:** both workstreams touch reincarnated-loadout (and potentially reincarnated-demo); committing serially in one drax session avoids merge collision risk surfaced in wave-open Gate-1 INFO-1.

**Alternative (NOT recommended):** firing two parallel drax invocations on separate branches and merging. KR rejects this; sequential serialization is simpler + safer for this single-session scope.

---

## 4. Smoke-test + validation discipline

Per Disc #2 + LOCK F MVP-discipline pattern from IA-3:

### Post-EAA-6 validation
- Loadout app loads kit_space data without runtime errors
- All 25 kits render in browser view
- Filter UI works (if extended to kit_space)
- Per-kit detail view renders skill list + flavor_decision metadata + chain_composition/t4_selection (note: some null per ClassGenerator path; EAA-8 INFO-1)
- 0 TS errors
- Vercel preview deploy succeeds (LOCK G auto-deploy)

### Post-EAA-7 validation
- Engine page loads chronicle data without runtime errors
- Single event renders via EngineStatePipelineFlow
- No regressions on existing engine page functionality (V1/V2 historical seasons still render if applicable)
- 0 TS errors
- Vercel preview deploy succeeds

### Backward-compat preservation
- V1/V2 IA-3 deployed seasons remain accessible as historical reference (per canonical record § 6 Path α + IA-3 close-out)
- Drax may add a clear UI separation if helpful (e.g., "Historical Seasons" tab vs "Kit Space" tab) — within LOCK O if uses existing tab/nav components

---

## 5. Out of scope (explicit non-goals)

- **Chernoff celestial body UI** — out of scope per LOCK P (defers to MM-P1)
- **New UI component shells** — LOCK O strict reuse
- **Visual redesign / aesthetic refresh** — LOCK O preserves existing aesthetic
- **Realm Expansion event UX** — gates on first Realm Expansion content design session (not Phase 3 scope)
- **Per-kit engagement telemetry rendering** — out of scope per canonical record § 7.4
- **Drax-side migration of historical seasons to kit-space schema** — Path α preserves historical as-is
- **Mobile/touch-specific UX** — out of EAA chain scope
- **Authoring NEW kits via UI** — engine emits; player browses; no creation surface

---

## 6. Cross-seam contract (Principle 6)

**Cross-seam touches:**
- star-lord output pipeline (already emitting kit_space output per EAA-3 + EAA-4) ↔ drax consumption
- Engine → loadout cross-repo data flow (loadout reads from `reincarnated-engine/data/kit_space/` via existing data-bundling/copy mechanism per drax's existing pattern)

**Discipline:** consumes ALREADY-RATIFIED Phase 1 + EAA-5 schemas. ADR-004 MIGRATION.md updates only if drax discovers a structural incompatibility surfacing escape clause.

**Round-trip:** not applicable — drax is consumer-side of locked contract; no new cross-seam surface introduced.

**Incompatibility-surfacing protocol** (per Gate-1 INFO-3 amendment): if drax discovers a structural incompatibility in the locked schemas (e.g., a required field is unrenderable via existing components), surface to KR as INFO **BEFORE** authoring any MIGRATION.md amendment. KR routes back to schema seam-owner (rocket/elrond/star-lord) for reconciliation. Drax does not unilaterally amend MIGRATION.md from consumer side.

**Concurrent-write coordination:** KR's last commit was `39d9068`; star-lord's last was `c3e2d10`. Drax committing into reincarnated-loadout (separate repo) doesn't collide with meta-repo + reincarnated-engine writes. Meta-repo Gate-2 finding + dispatch completion + wave-state updates fire to meta-repo cleanly.

---

## 7. Acceptance criterion

EAA-6 PASSES when:
1. Loadout app consumes kit_space JSON entries via existing components
2. All 25 kits accessible in kit browser view
3. Per-kit detail view renders all fields populated by EAA-5 v2 (primary, cultural_tradition, period, skills with flavor metadata, etc.). **Null fields (chain_composition / t4_selection per ClassGenerator path; pending EAA-8 INFO-1) render gracefully — no blank-screen crash; placeholder or omission acceptable** (per Gate-1 INFO-1 amendment).
4. 0 TS errors; smoke-test passes
5. Vercel preview deploy succeeds
6. jack-ryan Gate-2 PASS
7. Historical V1/V2 seasons remain accessible (backward-compat)

EAA-7 PASSES when:
1. Engine page renders kit_space_chronicle event(s) via existing EngineStatePipelineFlow component
2. `kse_20260602_001` event displays correctly (event_id + timestamp + event_scope + kit_count + substrate_inputs_changed)
3. 0 TS errors; smoke-test passes
4. Vercel preview deploy succeeds  
5. jack-ryan Gate-2 PASS
6. No regressions on existing engine page functionality

---

## 8. Tag intent + auto-commit/push

- EAA-6 commit tag: `drax/v1.4-eaa-6-loadout-kit-space-1`
- EAA-7 commit tag: `drax/v1.4-eaa-7-engine-page-chronicle-1`
- Per Matt 2026-06-02 explicit cycle-push authorization + LOCK G Vercel auto-deploy on push
- Auto-commit work-products as you go; auto-push per cycle pattern
- Vercel preview URLs reported back to KR for inspection

---

## 9. Report back to KR

On completion:
- EAA-6 commit shas + Vercel preview URL
- EAA-7 commit shas + Vercel preview URL  
- jack-ryan Gate-2 verdicts for both workstreams
- Smoke-test results (TS errors / runtime errors / 0 regressions)
- **Type extensions inventory** (per Gate-1 INFO-2 amendment): list which TS types were extended and what fields added (e.g., `KitData` extended with `flavor_decision`, `flavor_word_used`, `kit_space_expansion_event_id` etc.)
- Component reuse summary (which existing components consumed kit_space; any escape-clause triggers per LOCK O)
- Phase 4 readiness signal (EAA-8 wave-close becomes routable)
- Any drax-surfaced INFOs/concerns for jack-ryan EAA-8 wave-close ratification

---

## 10. References

- Canonical commitment: `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`
- Joint design spec: `agentic_orchestration/elrond/notes/2026-06-02-eaa-3-plus-4-joint-ingest-and-chronicle-spec.md`
- Chronicle schema: `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md`
- Wave-state: `cycle-16-eaa-engine-architectural-amendment/wave-state.md`
- IA-3 drax close-outs (reference pattern): `agentic_orchestration/drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md` + `2026-06-01-ia-3-phase-4-v2-iteration-close.md`
- LOCK O specification: wave-state.md § 1 + wave-open dispatch § 3
- ADR-004 cross-seam discipline: `agentic_orchestration/GOVERNANCE.md`

---

**End of EAA-6 + EAA-7 sequential-within-drax dispatch. Fires after jack-ryan Gate-1 PASS.**

---

## Completion record — EAA-6

**Completed:** 2026-06-02
**Commit:** `2f5fec4` (reincarnated-loadout)
**Tag:** `drax/v1.4-eaa-6-loadout-kit-space-1`
**Vercel preview:** `https://reincarnated-loadout-d1pvkgywc-matthew-wetmore-s-projects.vercel.app` — READY
**Gate-2:** PASS — `agentic_orchestration/qa/findings/2026-06-02-eaa-6-loadout-kit-space-gate-2.md`
**ACs:** 7/7 PASS
**Type extensions:** `KitSpaceChronicle`, `KitSpaceChronicleEvent`, `KitSpaceChronicleLineageTags`, `KitSpaceChronicleGenerationParameters`, `KitData`, `KitSkill`, `KitSubstrateTrace`, `KitChainComposition`, `LineageTags` — all new in `src/data/kitSpaceTypes.ts`
**Components reused:** `CourtBrowser` card grid pattern (adapted via `KitCard`); inline detail pattern (adapted via `KitDetailPanel`); `SubstrateToggle` pattern (adapted via `ElementToggle`); `useEngineStateData` fetch pattern (adapted via `useKitSpaceData`)
**No TODO(drax) overrides**

## Completion record — EAA-7

**Completed:** 2026-06-02
**Commit:** `42a0a0b` (reincarnated-loadout)
**Tag:** `drax/v1.4-eaa-7-engine-page-chronicle-1`
**Vercel preview:** `https://reincarnated-loadout-madl8913m-matthew-wetmore-s-projects.vercel.app` — READY
**Gate-2:** PASS (INFO) — `agentic_orchestration/qa/findings/2026-06-02-eaa-7-engine-page-chronicle-gate-2.md`
**ACs:** 6/6 PASS
**Type extensions:** none — reuses `KitSpaceChronicle` + `KitSpaceChronicleEvent` from EAA-6
**Components:** `EngineStateChronicle.tsx` (adapts EngineStatePipelineFlow section pattern); `useKitSpaceChronicleData.ts` (chronicle-only hook)
**Gate-2 INFOs queued for EAA-8:** INFO-1 (ChronicleSection inside season-gated block; hoist candidate); INFO-2 (refresh wire-up; remount-via-key functional equivalent)
**No TODO(drax) overrides**
**Phase 4 readiness:** EAA-8 wave-close routable; INFOs are non-blocking
