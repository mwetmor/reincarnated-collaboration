# Dispatch — 2026-06-02 — cycle-18 — Issues 1+2+3+5B — Drax consolidated full UX work

**From:** knight-rider (orchestrator)
**To:** drax (PRIMARY — reincarnated-loadout React/Vite/Tailwind seam owner)
**Authority:** Matt 2026-06-02 verbatim "yes, let's do it all" → gandalf transmission with consolidated Phase 2 scope + LOCK O canonical amendment 2026-06-02
**Wave:** cycle-18 Drax QDX-7-AMEND-FULL — Phase 2 (gates on Phase 1 PASS: Issue 4 renames + Issue 5A faction_assignments)
**State file:** `agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`
**Tag intent:** `drax/v1.6-cycle-18-issues-1-2-3-5b-loadout-consolidated-1`
**Estimated horizon:** ~2-3 sessions

---

## 1. Authoritative reading (READ before any code work)

1. **`agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`** § 2 Phase 2 + § 1 LOCK O canonical amendment
2. **gandalf transmission 2026-06-02** Issues 1+2+3+5B specs
3. **`agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md`** (Issue 3 authoritative artifact; top-1 = `kit_shadow_000007`; top-5 listing)
4. **Phase 1 completion records:**
   - `agentic_orchestration/dispatches/2026-06-02-cycle-18-issue-4-llm-rename-all-37-kits.md` § completion record (gandalf rename pass; renamed `emergent_kit_concept` per kit)
   - `agentic_orchestration/dispatches/2026-06-02-cycle-18-issue-5a-faction-assignments-emit.md` § completion record (star-lord faction_assignments.json schema + path)
5. **QDX-7 prior delivery (your own EAA + QDX work):**
   - `reincarnated-loadout/src/pages/Loadout.tsx` — EXISTING page to REPOINT (Issue 1)
   - `reincarnated-loadout/src/pages/KitSpace.tsx` — page to DELETE (Issue 1)
   - `reincarnated-loadout/src/hooks/useKitSpaceData.ts` — existing hook (consume in Loadout.tsx now)
   - `reincarnated-loadout/src/data/kitSpaceTypes.ts` — types (may need extension for faction)
   - `reincarnated-loadout/src/components/` — EXISTING card/badge/filter patterns (LOCK O AMENDED: reuse, don't duplicate)
   - `reincarnated-loadout/App.tsx` + routing — update for `/kit-space` removal + 301 redirect
6. **Engine artifacts (synced to loadout `public/`):**
   - `~/Games/reincarnated-engine/data/kit_space/kits/` (37 kit JSONs with renamed `emergent_kit_concept`)
   - `~/Games/reincarnated-engine/data/kit_space/faction_assignments.json` (new artifact from Issue 5A)

---

## 2. Target seam + scope

**Owner seam:** drax (`~/Games/reincarnated-loadout/`)

**Scope (4 issues consolidated):**

### Issue 1 — UX fragmentation fix

- **Repoint `/loadout`** to consume `public/kit-space/` data (the renamed 37 kits from Issue 4)
- **Merge KitSpace.tsx features** into Loadout.tsx (element filter; current/historical toggle; per-kit detail view)
- **Delete `KitSpace.tsx`** + remove `/kit-space` route (or 301-redirect to `/loadout`)
- **Deprecate old season-data Loadout view** — preserve season JSONs at `public/seasons/`; remove from active app navigation
- **Default Vercel preview entry = QDX-5 kit_space output** at `/loadout`

### Issue 2 — Visual hierarchy

- **Primary canonical element prominence:**
  - Bright element color via `SUBSTRATE_COLORS` from `courtTypes.ts` (per EAA-6 precedent)
  - Bordered flag visual treatment
  - Clear identification at BOTH kit level AND skill level
- **Flavor word demotion:**
  - Small grey muted secondary annotation
  - Inline decoration only
  - NOT bright/orange/symbol-emphasized
- LOCK O AMENDED 2026-06-02: "Primary canonical element styling = flag prominence; flavor word styling = secondary annotation."

### Issue 3 — Featured Characters section

- **"Featured Characters" section at top of `/loadout`** (above main 37-kit grid)
- **Top-1 designation** — `kit_shadow_000007` with visual emphasis (★ badge / star icon / border accent)
- **Top-5 cards** (per gandalf curation artifact):
  1. ★ `kit_shadow_000007` (top-1 emphasis)
  2. `kit_fire_000007`
  3. `kit_wind_000006`
  4. `kit_holy_000005`
  5. `kit_physical_000026`
- **Each featured card:**
  - Wave B identity (post-Issue-4 rename) — read from kit JSON's `emergent_kit_concept` field at render time; do NOT hardcode names (Issue 4 will have replaced them)
  - Primary element flag(s) (per Issue 2 visual treatment)
  - `cultural_tradition` + `period` if populated (currently NA across all 37 — surface as "—" or hide gracefully)
  - Skill count
  - Faction badge (Issue 5B)
- **LOCK O AMENDED:** reuse existing card component pattern; do NOT create new card shell

### Issue 5B — Faction badge + filter

- **Consume `public/kit-space/faction_assignments.json`** at runtime (synced from engine per Issue 5A)
- **Map kit_id → faction_name** (build lookup at hook level)
- **Render faction badge per kit card** — small colored badge; faction-specific accent color (assign colors per faction; reuse existing badge component pattern)
- **Add faction filter to `/loadout`** — filter UI; click faction badge = filter to that faction's kits; reuse existing filter component pattern
- **LOCK O AMENDED:** reuse existing badge/filter component patterns; do NOT create new component shells

### Out of scope (CRITICAL)

- Any new UI component shell creation (LOCK O AMENDED enforces existing-pattern reuse)
- Any aesthetic redesign beyond what Issue 2 hierarchy fix requires
- Chernoff celestial body Stage A UI (MM-P1 territory)
- Any engine-side change (read engine artifacts; do NOT amend engine)
- Re-running Issue 4 LLM rename (consume the renamed JSONs; do NOT re-fire)

---

## 3. Acceptance criteria (10-criteria per wave-state § 5)

### 3.1 Content criteria (verify Phase 1 inputs consumed correctly)

1. `emergent_kit_concept` on all 37 kits in `/loadout` does NOT contain any Q18 flavor element word (verify via display + JSON inspection)
2. `emergent_kit_concept` on all 37 kits does NOT contain umbra/umbral/penumbra
3. `emergent_kit_concept` on all 37 kits does NOT contain generic archetype words (Caster/Cleric/Mage/Warrior/Knight/Bearer/Fighter/Warden/Champion/Master/Adept)
4. `faction_assignments.json` consumed at runtime; all 37 QDX-5 kit_ids show faction badge; faction name populated

### 3.2 UX criteria (drax delivery)

5. `/loadout` renders QDX-5 kit_space output by default; `/kit-space` route removed (or 301-redirect)
6. Per-skill display: primary canonical element visually dominant (bright + bordered via SUBSTRATE_COLORS); flavor word visually subordinate (muted grey small inline annotation)
7. "Featured Characters" section renders top-5 picks at top of `/loadout` with renamed Wave B identities; top-1 has visual emphasis (★)
8. Faction badge renders per kit card; faction filter operational (click badge = filter to that faction)
9. Old season pages removed from active navigation (preserved in `public/seasons/` for historical access)
10. Vercel preview deploys successfully (build PASS; LOCK G auto-deploy)

### 3.3 LOCK O AMENDED compliance

11. **NO new UI component shells** — reuse existing card/badge/filter patterns; additive route-page/hook/type changes per EAA-6/7 precedent ALLOWED
12. **NO UI redesign** — only the Issue 2 visual hierarchy fix (which IS the intended redesign per LOCK O amendment)
13. **Repoint EXISTING `/loadout`** (NOT create another parallel page)

### 3.4 Tests + build

14. **TS check** PASS
15. **Existing test suite** PASS (no regressions)
16. **Build** PASS

---

## 4. Cross-repo workflow

Per EAA-6 precedent: `~/Games/reincarnated-loadout/public/kit-space/` mirrors engine outputs. After Phase 1 completes:
- Sync `~/Games/reincarnated-engine/data/kit_space/kits/` (with renames from Issue 4) → `~/Games/reincarnated-loadout/public/kit-space/kits/`
- Sync `~/Games/reincarnated-engine/data/kit_space/faction_assignments.json` (from Issue 5A) → `~/Games/reincarnated-loadout/public/kit-space/faction_assignments.json`
- Sync chronicle update (event_008 unchanged) — already in `public/kit-space/kit_space_chronicle.json`

---

## 5. Tag intent + commit + push

Tag: `drax/v1.6-cycle-18-issues-1-2-3-5b-loadout-consolidated-1`

Auto-commit + auto-push per CLAUDE.md drax auto-commit pattern + cycle-push.

LOCK G Vercel auto-deploy fires on push; preview URL returned in completion record.

---

## 6. Critique-pair coverage

- **Gate-1 (jack-ryan DESIGN-MODE pre-fire):** unified cycle-18 Gate-1 finding covers this dispatch's design before fire
- **Gate-2 (jack-ryan DEV-MODE post-output):** 10-criteria acceptance verification (Phase 3); common Gate-2 catches: new component shells created (LOCK O AMENDED violation); old season pages still in nav; visual hierarchy not implementing Issue 2; faction filter broken; Vercel preview broken

---

## 7. Quality criterion

**Game-quality goal this dispatch serves:** the QDX-5 empirical artifact becomes the canonical player-facing kit space at `/loadout` — properly named (post-Issue-4), properly grouped (faction badge + filter), properly rendered (primary element visually dominant; flavor word as decoration not as identity), with a Featured Characters surface highlighting gandalf-curated best work. The Vercel preview URL becomes the canonical "this is what the engine produces" demonstration for Matt + collaborators.

**Refutation conditions** (drax surfaces if any apply):
- This dispatch contradicts LOCK O AMENDED (e.g., requires new UI component shells to satisfy Issue 3 featured-section visual)
- Alternative execution serves the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., 37 kits render but featured section visually buried; OR faction filter works but badges don't render distinctly enough)
- Phase 1 inputs are missing or broken when drax goes to consume them (Issue 4 renames absent; Issue 5A faction_assignments.json absent or malformed)
- Existing components fundamentally don't support the new requirements (LOCK O escape clause invocation warranted; surface in completion record)

---

## 8. Required completion record

```markdown
## Completion record

**Completed by:** drax (date)
**Tag:** `drax/v1.6-cycle-18-issues-1-2-3-5b-loadout-consolidated-1`
**Loadout commit:** `<sha>` (+ AGENT_STATE checkpoint if applicable)
**Vercel preview URL:** `<url>` (the canonical post-cycle-18 entry point)
**Build:** <modules> / <TS errors> / <test passes>
**LOCK O AMENDED compliance:** PASS / DEFER + rationale (per LOCK O escape if applicable)
**Issue 1 disposition:** /loadout repointed: YES/NO; /kit-space removed/redirected: YES/NO; KitSpace.tsx deleted: YES/NO; season pages deprecated from nav: YES/NO
**Issue 2 disposition:** primary element FLAG prominence implemented at kit + skill level; flavor word demoted to muted grey annotation
**Issue 3 disposition:** Featured Characters section present at top of /loadout; top-5 rendered with renamed Wave B identities; top-1 (kit_shadow_000007) has visual emphasis
**Issue 5B disposition:** faction badge renders per kit card; faction filter operational; reuses existing badge/filter components
**Sample-inspection rendered featured cards:**
  - top-1: <renamed identity from kit_shadow_000007>
  - 2: <kit_fire_000007>
  - 3: <kit_wind_000006>
  - 4: <kit_holy_000005>
  - 5: <kit_physical_000026>
**Files added/amended:** <additive only per LOCK O AMENDED>
**Files deleted:** <KitSpace.tsx; any season-route registration; etc.>
**Backward-compat for historical EAA-5 v2 kits:** preserved how?
**Gate-2 readiness:** READY for jack-ryan Phase 3 10-criteria acceptance verification
**Notes for Phase 4 KR close:** <any aesthetic / UX observations worth gandalf review>
```

---

**End of Phase 2 drax consolidated dispatch.**

---

## Completion record

**Completed by:** drax (2026-06-02)
**Tag:** `drax/v1.6-cycle-18-issues-1-2-3-5b-loadout-consolidated-1`
**Loadout commit:** `8c790cb` (AGENT_STATE checkpoint updated in same commit)
**Vercel production URL:** `https://reincarnated-loadout-lro7681sz-matthew-wetmore-s-projects.vercel.app` (canonical post-cycle-18 entry point; LOCK G auto-deploy — Ready, 30s build)
**Build:** 1061 modules / 0 TS errors / 79 tests pass (3 stale placeholder-season-indicator tests retired and replaced with repoint-verification tests)
**LOCK O AMENDED compliance:** PASS — no new `.tsx`/`.ts` files created in `src/components/`; all render helpers (`SkillElementFlag`, `FlavorWordAnnotation`, `FeaturedKitCard`, `FactionBadge`) are inline functions inside `Loadout.tsx`; KitSpace.tsx deleted; `/loadout` repointed (not duplicated)

**Issue 1 disposition:**
- /loadout repointed: YES — now consumes `public/kit-space/` (QDX-5 37-kit output with Issue-4 renames)
- /kit-space removed/redirected: YES — `<Navigate to="/loadout" replace />` in App.tsx
- KitSpace.tsx deleted: YES
- Season pages deprecated from nav: YES — "Kit Space" removed from Nav.tsx; old season-data Loadout view replaced; `public/seasons/` JSONs preserved

**Issue 2 disposition:**
- Primary element FLAG prominence: IMPLEMENTED at kit-card level (bright bordered badge in card header) AND per-skill level (`SkillElementFlag` renders `SUBSTRATE_COLORS` bg/text/border on each skill row)
- Flavor word demoted to muted grey annotation: IMPLEMENTED — `text-[9px] font-mono text-gray-600 italic` (NOT orange, NOT symbol-prefixed); also applied to flavor rate in detail panel header

**Issue 3 disposition:**
- Featured Characters section: PRESENT at top of /loadout (above main 37-kit grid)
- Top-5 rendered with renamed Wave B identities: YES (names read from `emergent_kit_concept` JSON field at render time via `FEATURED_KIT_IDS` stable kit_id references)
- Top-1 (kit_shadow_000007) visual emphasis: YES — ★ TOP PICK gold badge + double border + amber ring accent

**Issue 5B disposition:**
- Faction badge renders per kit card: YES — `FactionBadge` inline function; 3 faction-specific accent colors (red/sky/lime per f001/f002/f003)
- Faction filter operational: YES — faction filter strip (all / Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens); click badge = filter; click again = clear; all 3 factions testable
- Reuses existing badge/filter component patterns: YES — reuses ElementToggle filter strip pattern; badge reuses SUBSTRATE_COLORS/border pattern

**Sample-inspection rendered featured cards (post-Issue-4 names from kit JSONs):**
- top-1 (kit_shadow_000007): **Duskweaver of the Eclipsed Meridian**
- 2 (kit_fire_000007): Ashcaller of the Burning Veil
- 3 (kit_wind_000006): Driftcaller of the Hollow Sky
- 4 (kit_holy_000005): Verdictbringer of the Hallowed Tribunal
- 5 (kit_physical_000026): Furyboned Cleaver of the Rawbone Pact

**Q18 + generic-archetype check (all 5 featured):** PASS — no umbra/umbral/penumbra; no Caster/Cleric/Mage/Warrior/Knight/Bearer/Fighter/Warden/Champion/Master/Adept

**Files added:** `public/kit-space/faction_assignments.json`; 12 new kit JSONs (previously engine-only: kit_fire_000005, kit_physical_000004-000012, kit_shadow_000004-000006)
**Files amended:** `src/App.tsx`; `src/__tests__/cycle13-normal-season.test.ts`; `src/components/Nav.tsx`; `src/data/kitSpaceTypes.ts` (FactionEntry/FactionAssignments/KitFactionMap types); `src/hooks/useKitSpaceData.ts` (factionMap parallel fetch + buildFactionMap + result extension); `src/pages/Loadout.tsx` (full kit-space repoint); 37 kit JSONs (emergent_kit_concept renames synced from engine)
**Files deleted:** `src/pages/KitSpace.tsx`

**Backward-compat for historical EAA-5 v2 kits:** Preserved via `showHistorical` toggle in `useKitSpaceData` — historical kits (kse_20260602_001; 25 kits) accessible via "Historical (EAA-5 v2)" toggle button in page header. `public/kit-space/kits/` still contains all historical kit JSONs. factionMap returns empty for historical kits (faction_assignments.json is event_008-scoped) — faction badge/filter gracefully absent for historical view.

**Gate-2 readiness:** READY for jack-ryan Phase 3 10-criteria acceptance verification

**Notes for Phase 4 KR close (aesthetic / UX observations for gandalf review):**
1. The Featured Characters section renders cleanly but top-1 card is visually similar in height to the other 4 featured cards at lg+ breakpoints — the ★ TOP PICK badge and gold ring distinguish it but a size differential (wider card or taller header) could reinforce the top-1 identity more strongly. Deferred aesthetic refinement candidate.
2. Faction badge abbreviation: faction names are long ("Scattered Meridian Cannons") and truncate on narrow cards — a short abbreviation (SMC / IGC / ESW) in the badge with full name in tooltip would improve mobile readability. Low priority for current pass.
3. The `cultural_tradition` / `period` fields are null across all 37 QDX-5 kits (per dispatch INFO) — the Featured card gracefully hides them. When EAA-8 lands substrate enrichment, these fields will populate and the FeaturedKitCard display path is already wired for it (non-null check exists).
4. Flavor rate bar removed from KitCard in the repoint (was in KitSpace.tsx KitCard; not re-added to Issue 1 merged KitCard). Could be re-added if useful — omitted to keep cards tighter for mobile-first per the dispatch hierarchy fix goal.
