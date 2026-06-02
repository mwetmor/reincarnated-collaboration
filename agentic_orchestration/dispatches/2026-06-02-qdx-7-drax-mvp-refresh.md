# Dispatch — 2026-06-02 — QDX-7 — Drax MVP refresh (loadout + engine page consume QDX-5 kit_space output)

**From:** knight-rider (orchestrator)
**To:** drax (PRIMARY — reincarnated-loadout React/Vite app + engine page chronicle)
**Authority:** Matt 2026-06-02 QDX chain Locks A-T preserved + LOCK O drax MVP-discipline + LOCK T drax QDX MVP refresh per LOCK O pattern (existing components only; NO new UI; NO redesign). QDX-6 jack-ryan Gate-2 PASS-with-INFO (commit `fc075ae`) cleared Phase 4 routing.
**Wave:** cycle-17 QDX QD-Engine Re-Fire — Phase 4 (gates on QDX-5 + QDX-6 ✅ achieved)
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Tag intent:** `drax/v1.5-qdx-7-loadout-engine-page-kit-space-1`
**Estimated horizon:** ~2-4 sessions

---

## 1. Authoritative reading (READ before any code work)

1. **`agentic_orchestration/dispatches/2026-06-02-qdx-7-drax-mvp-refresh.md`** (this dispatch)
2. **`agentic_orchestration/qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md`** (jack-ryan QDX-6 verdict; commit `fc075ae`) — **§ Phase 4 Routing Clearance has 3 routing notes for drax**
3. **`agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`** § 2 QDX-5 status + LOCK T scope (existing components; no UI redesign)
4. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** § 3.3-3.4 (continuous kit space; per-kit JSON entries; chronicle expansion events)
5. **`canonical/story/2026-06-02-eaa-chain-wave-close-record.md`** § Phase 3 EAA-6 + EAA-7 (drax MVP from EAA chain; reference for component reuse + Vercel preview pattern)
6. **EAA-6 + EAA-7 deliverables (drax precedent):**
   - `reincarnated-loadout/src/hooks/useKitSpaceData.ts` — kit_space data hook from EAA-6
   - `reincarnated-loadout/src/pages/KitSpace.tsx` — kit_space page from EAA-6
   - `reincarnated-loadout/src/data/kitSpaceTypes.ts` — kit_space types from EAA-6
   - `reincarnated-loadout/src/components/EngineState/ChronicleSection` — engine page chronicle from EAA-7
   - `reincarnated-loadout/src/components/EngineState/EngineStateChronicle` — engine state chronicle component from EAA-7
7. **QDX-5 emit artifacts:**
   - `~/Games/reincarnated-engine/data/kit_space/kit_space_chronicle.json` — chronicle event `kse_20260602_008` (the new QDX-5 event)
   - `~/Games/reincarnated-engine/data/kit_space/kits/kit_<primary>_<seq6>.json` × 37 (QDX-5 kits filtered by `kit_space_expansion_event_id == "kse_20260602_008"`)

---

## 2. Target seam + scope

**Owner seam:** drax (reincarnated-loadout React/Vite/Tailwind app deployed to Vercel)

**Target files (additive):**
- Existing components reused where possible (LOCK O MVP-discipline)
- May add additive types/hooks to consume QDX-5 schema if existing types don't support new fields

**Scope:**

Refresh the drax loadout app + engine page to consume the QDX-5 kit_space output (event `kse_20260602_008` — 37 kits with QDX richness: emergent identity + faction grouping + multi-T4 + WS1A.4-lite per-skill flavor metadata). MVP-load-only pattern per LOCK O + LOCK T: existing component layouts; no UI redesign.

**LOCK T scope per wave-state:**
- reincarnated-loadout consumes new kit_space output (richer than EAA-5 v2 output)
- Render with EXISTING component layouts where possible
- Surface T4 selection if existing components support; if not, defer
- Surface faction grouping if existing components support; if not, defer
- Surface emergent kit identity (kit name field) — likely existing component support
- Engine page chronicles QDX-5 fire as kit-space-expansion event
- **NO new UI components**
- **NO UI redesign**

**Out of scope (CRITICAL):**
- Chernoff celestial body Stage A UI (defers to MM-P1 design session per LOCK P)
- Faction-emergence visualization beyond existing chronicle component (if not supported, defer per LOCK O escape clause)
- Any aesthetic redesign

---

## 3. jack-ryan QDX-6 routing notes (CRITICAL — drax must implement)

Per QDX-6 Gate-2 finding (`fc075ae`):

### Note 1 — Faction grouping NOT in per-kit `emergent_kit_concept`
- Per-kit JSON's `emergent_kit_concept` field describes the kit's emergent identity (e.g., "Crusher Who Holds the Ground", "Ember Caster of Scorched Meridian")
- It does NOT contain the faction name
- Faction grouping data lives in **Phase 5a clustering output** (chronicle event's `generation_parameters` or separate field per chronicle schema)
- **Action**: drax must confirm faction data source before rendering faction views. If existing component doesn't naturally consume cluster data, defer faction visualization per LOCK O escape clause
- Wave A faction names from QDX-5: Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens

### Note 2 — Check `t4_selection.is_active` flag (NOT just null-check)
- Some kits have populated `t4_selection` field but `is_active=False`
- Example: `kit_lightning_000005` has populated but inactive T4
- **Action**: rendering logic should check both `t4_selection != null` AND `t4_selection.is_active == true` before displaying T4 details

### Note 3 — Filter to `kit_space_expansion_event_id == "kse_20260602_008"`
- Historical kits (events 001-007) have different schema shapes; cause render errors if not filtered
- QDX-5 (event_008) is the canonical "current" kit_space
- **Action**: drax loadout filter view to show only event_008 kits (37 kits)
- Historical events: kse_001 (EAA-5 v2 25 kits) + kse_002-007 (QDX-3/4 smokes; 13 kits across smokes); preserved per Path α but not rendered in current view

---

## 4. Acceptance criteria

### 4.1 Functional

1. **Loadout consumes QDX-5 kit_space output** — KitSpace.tsx or equivalent shows 37 kits from event `kse_20260602_008`; existing component layouts; per-kit detail rendering Wave B emergent identity + skill list + (when supported) multi-T4 selection
2. **Engine page chronicles QDX-5 event** — EngineStateChronicle or equivalent shows `kse_20260602_008` event entry (37 kits; B4.5 distribution; ClassGenerator + QDX richness pipeline; Matt's Cycle 14-equivalent goal empirically met)
3. **Routing note 1 implemented** — faction data source confirmed; faction visualization deferred per LOCK O escape if existing components don't support
4. **Routing note 2 implemented** — `t4_selection.is_active` check guards T4 rendering
5. **Routing note 3 implemented** — filter to `kse_20260602_008` for current view; historical kits preserved as kit_space_archive context
6. **Backward compatibility** — EAA-5 v2 historical kits (event `kse_001`) continue to be accessible (e.g., via separate "Historical seasons" link or filter)
7. **Vercel preview deploys cleanly** — per LOCK G auto-deploy on drax push; build PASS; TS check PASS; tests PASS

### 4.2 LOCK O / LOCK T compliance

8. **NO new UI components** — additive route-pages and additive hooks/types ALLOWED (per EAA-6/7 precedent)
9. **NO UI redesign** — existing component aesthetic preserved
10. **MVP discipline** — render what's directly supported; defer (don't force) what's not

### 4.3 Tests + lint

11. **TS check** PASS
12. **Existing test suite** PASS (no regressions)
13. **Build** PASS

---

## 5. Cross-repo workflow

drax operates in `~/Games/reincarnated-loadout/`. Engine outputs are at `~/Games/reincarnated-engine/data/kit_space/`. Drax loadout app may need to either:
- Read kit JSONs from a sync'd `public/engine-state/` directory (per EAA-6 precedent)
- OR fetch from a deployed API/static URL

Per EAA-6 EAA-7 precedent: `reincarnated-loadout/public/engine-state/` mirrors engine outputs. Drax must arrange for `kse_20260602_008` event + 37 kit JSONs to be accessible by the loadout app at runtime.

---

## 6. Tag intent + commit + push

Tag: `drax/v1.5-qdx-7-loadout-engine-page-kit-space-1`

Auto-commit + auto-push per CLAUDE.md drax auto-commit pattern + cycle-push.

LOCK G Vercel auto-deploy fires on push; preview URL returned in completion record.

---

## 7. Critique-pair coverage

- **Gate-1** (jack-ryan DESIGN-MODE pre-fire on this dispatch): SKIPPED by KR judgment — QDX-6 Gate-2 already cleared Phase 4; LOCK T scope is well-bounded by EAA-6/7 precedent + 3 explicit routing notes; LOCK O MVP-discipline + LOCK T scope-bounding makes Gate-1 BLOCK risk low. If drax surfaces architectural questions, surface via completion record.
- **Gate-2** (jack-ryan DEV-MODE post-output): standard Gate-2 review on tagged commit. Common Gate-2 catches: routing notes 1/2/3 not implemented; new UI components introduced; UI redesign; Vercel preview broken; TS errors; build failures; historical kit access broken.

---

## 8. Quality criterion

**Game-quality goal this dispatch serves:** Matt (and anyone viewing the loadout app + engine page) can SEE the QDX-5 empirical-truth-moment artifact through existing component layouts — 37 emergent kit identities, distribution visible, the Cycle 14 wave-5-equivalent richness goal empirically demonstrable via the deployed Vercel preview. The engine page chronicle shows the substantive expansion event (`kse_20260602_008`) replacing the EAA-5 v2 25-kit reference as the canonical current state.

**Refutation conditions** (drax surfaces if any apply):
- This dispatch contradicts LOCK O MVP-discipline (e.g., requires new UI components to satisfy routing notes)
- Alternative execution would serve the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., kits render but emergent identity buried)
- Dispatch framing pre-commits to a decision Matt has not ratified
- Existing components fundamentally don't support the new schema (LOCK O escape clause invocation warranted)

---

## 9. Required completion record

On work-completion, append a completion record to this dispatch file with:

```markdown
## Completion record

**Completed by:** drax (date)
**Tag:** `drax/v1.5-qdx-7-loadout-engine-page-kit-space-1`
**Loadout commit:** `<sha>`
**Vercel preview URL:** `<url>`
**Build:** <modules> / <TS error count> / <test pass count>
**LOCK O compliance:** PASS / DEFER + escape clause invocation rationale
**Routing notes disposition:**
- Note 1 (faction grouping): IMPLEMENTED / DEFERRED + rationale
- Note 2 (is_active check): IMPLEMENTED
- Note 3 (event_008 filter): IMPLEMENTED + historical accessibility preserved
**New artifacts:** <files added; additive hooks/types/pages only>
**Backward-compat:** EAA-5 v2 historical kit access preserved? (yes/no + how)
**Vercel preview verification:** /kit-space route shows 37 kits; engine page shows event_008 chronicle entry
**Sample-inspection of rendered kits:** <3-5 kit names + identity visible; faction visible if supported>
**Gate-2 verdict:** PASS / PASS-with-INFO / BLOCK + jack-ryan finding path
**Notes for QDX-8 wave-close:** <any aesthetic / UX observations; faction visualization status>
```

---

**End of QDX-7 dispatch.**
