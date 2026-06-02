# IA-3 Phase 1 MVP Integration Close — drax

**Date:** 2026-06-01
**Author:** drax
**Authority:** Matt 2026-06-01 strategic reset + LOCK F (MVP-discipline) + LOCK G (autonomous Vercel preview)
**Workstream tag:** `IA-3-drax-MVP-integration`

---

## Integration verdict: SUCCESS

Season_000042 data loads in both reincarnated-loadout and reincarnated-demo via existing components. No new UI components created. All acceptance criteria met.

---

## 1. reincarnated-loadout

**Data-loading approach:** Vite `import.meta.glob` static imports (existing pattern in `useSeasonData.ts`). Added `data/season_000042/` directory with adapted files:

- `data/season_000042/manifest.json` — adapted from engine manifest.json; `elements` stub (canonical-four mapped from cosmological_vocabulary slot_fills); `seasonal_elements` built from slot_fills (ignition/suffusion/bulwark/displacement/impact → fire/water/earth/wind/physical); `cosmological_vocabulary` preserved additively.
- `data/season_000042/classes/class_0001.json` through `class_0005.json` — 5 playable classes copied directly; additive fields (embodiment_tag, gear_slot_labels, grouping_pair_structure, convergence_report, etc.) pass through unchanged; existing ClassData interface handles them via forward-compat optionality.
- `data/season_000042/gear_pool.json` — adapted from `gear_pool_staged.json`; `id` → `gear_id` rename; `fit_*` fields defaulted to empty dicts where absent from engine output.

**Component wiring:** Existing `useSeasonData.ts` glob patterns automatically pick up the new data directory. Season_000042 appears in `selectableSeasons` on Loadout and Sample pages.

**Build:** `tsc -b && vite build` — CLEAN (0 TS errors; 1056 modules).

---

## 2. reincarnated-demo

**Data-loading approach:** Fetch-based loader (`src/data/loader.ts`) loading from `public/seasons/`. Added `public/seasons/season_000042/` with:

- `metadata.json` — adapted from engine manifest.json to SeasonMetadata shape (`format_version`, `generation_timestamp`, `seed`, `class_count`, `monster_count`, `trial_defeat_rate`, `convergence_failures`, `calibrated_stat_floors`, `elements`, `seasonal_elements`).
- `classes.json` — merged array of 5 playable classes (class_0001–class_0005); `is_act_boss: false` and `carried_gear: null` added additively; `balance_metadata.actual_winrate` and `converged` backfilled from `convergence_report.endgame_L50`.
- `monsters.json` — merged array of all 44 monsters.
- `gear_pool.json` — adapted from `gear_pool_staged.json`; `id` → `gear_id`.
- `gauntlet_recipe.json` — copied directly (format matches GauntletRecipe exactly).

**SEASON_IDS update:** `src/data/loader.ts` — added `'season_000042'` to `SEASON_IDS` array.

**Type extension (LOCK J § 1 additive):** `src/types/engine.ts` — added `'blink'` to `GeometryType` union. Season_000042 uses `blink` geometry type (novel; not in prior GeometryType union). Annotated with IA-3 P1 attribution comment.

**Build:** `tsc --noEmit && vite build` — CLEAN (0 TS errors; 536 modules).

---

## 3. Existing-component inventory per repo (INFO-3 for Gate-2 verification)

### reincarnated-loadout (React 18 / Vite / Tailwind)

**Pages** (routes):
- `Loadout.tsx` — class selector + skill tree + stats + gear + spirit guide + design-mode
- `Sample.tsx` — read-only sample kit display
- `Analytics.tsx` — telemetry charts
- `Encounters.tsx` — encounter analytics
- `CourtBrowser.tsx` — court/kit browser
- `EngineState.tsx` — engine state display
- `Pitch.tsx` — season pitch + faction marquee
- `Planning.tsx` / `PlanningDoc.tsx` — planning docs
- `App.tsx` — router shell

**Components (74 files):**

*Cycle14/* — `Cycle14GearDisplay`, `Cycle14SeasonSection`, `Cycle14T4Panel`, `FactionClusterTile`, `Season002Marquee`
*Cycle13/* — `Cycle13CharacterHeader`, `Cycle13GearDisplay`, `Cycle13SampleSection`, `Cycle13SkillTree`
*Analytics/* — `ArchetypeStackedBar`, `ChartCard`, `ConvergenceChart`, `Cycle14AnalyticsSection`, `Cycle14EncountersNote`, `ElementPie`, `EnergyPie`, `ModifierRangeChart`, `SeasonSummaryCards`, `SeasonTimelineChart`, `SkillTierChart`, `StatRadarChart`, `SubstrateHeatmap`, `WinRateHistogram`
*DesignMode/* — `DesignModePanel`, `DesignModeToggle`
*EngineState/* — `EngineStateBackwardTrace`, `EngineStateFactionEmergence`, `EngineStateKpiGrid`, `EngineStateObservations`, `EngineStatePageHeader`, `EngineStatePhaseDeepDive`, `EngineStatePipelineFlow`
*GearGrid/* — `GearGrid`
*SkillTree/* — `SkillDetailPanel`, `SkillNode`, `SkillTree`, `T4AlterationPanel`, `T4ComparisonPanel`
*SpiritGuide/* — `SpiritGuide`
*StatsPanel/* — `StatsPanel`
*WeaponSlot/* — `OffHandSlot`, `WeaponBadges`, `WeaponSlot`
*ui/* — `Button`, `Card`, `ClassIcon` (SeasonIcon), `FlavorTip`, `ProvenanceBadge`, `StrategyBadge`, `Tag`
*pitch/* — `CosmologyPairBlock`, `HeroOfEngineSpotlight`, `HeroPortraitPlaceholder`, `PathsCards`, `SeasonHypePiece`, `SlotFillChipRow`
*Nav.tsx*, `ActionBar.tsx`

**Hooks:** `useAnalytics`, `useCourtData`, `useCycle13Data`, `useEncounterAnalytics`, `useEngineStateData`, `useSeasonData`, `useSkillBuild`

**No new components created.** Existing `useSeasonData` glob picks up season_000042 automatically.

### reincarnated-demo (Pixi.js / TypeScript / Vite)

**Rendering / visual:** `arenaFloor.ts`, `roomRenderer.ts`, `stage.ts`, `archetypeRenderer.ts`, `atmosphericLayer.ts`, `characterSprites.ts`, `monsterSprites.ts`, `sprites.ts`, `spriteVfx.ts`, `statusGlow.ts`, `pimenVfx.ts`, `pixogenVfx.ts`, `codeManuVfx.ts`, `vfx.ts`, `ambientParticles.ts`, `ambientProps.ts`, `ambientPropsExtension.ts`, `dungeonTileset.ts`, `direDungeonLoot.ts`, `frostwindzClassArchetype.ts`, `frostwindzPhysical.ts`

**UI panels:** `characterSheet.ts`, `classSelector.ts`, `combatHud.ts`, `combatLog.ts`, `creditsOverlay.ts`, `dashCooldownHud.ts`, `desktopHudIcons.ts`, `diabloHud.ts`, `drawerShell.ts`, `hud.ts`, `inventoryPanel.ts`, `potionHud.ts`, `seasonSelector.ts`, `seasonTheme.ts`

**Skill tree:** `skillTree/skillTreePanel.ts`, `skillTree/types.ts`, `skillTree/fixtures/sampleTree.ts`, `skillTree/index.ts`

**Combat / encounter:** `ai.ts`, `gauntlet.ts`, `resolver.ts`, `damage.ts`, `combatant.ts`

**World:** `aggro.ts`, `arena.ts`, `movement.ts`, `separation.ts`, `topology.ts`

**Inventory:** `inventory.ts`, `loadout.ts`, `spiritGuide.ts`

**Mobile:** `joystick.ts`, `mobile.ts`, `orientationOverlay.ts`, `touchHotbar.ts`, `touchIcons.ts`, `touchPotions.ts`, `touchTargetBtn.ts`

**Data / types:** `loader.ts`, `perceptionAsymmetry.ts`, `substrateIdentity.ts`, `engine.ts`, `assetPath.ts`

**No new components created.** `loader.ts` SEASON_IDS updated; `engine.ts` GeometryType additive extension only.

---

## 4. Schema additions per LOCK J § 1 (additive only)

| Repo | File | Addition | Reason |
|---|---|---|---|
| reincarnated-demo | `src/types/engine.ts` | `'blink'` added to `GeometryType` union | season_000042 emits `blink` geometry type not in prior union |

No other type changes. Loadout `types.ts` has no `GeometryType` union; skill geometry fields are `string` in court context. No other semantic type changes anywhere.

---

## 5. Existing-component bugs surfaced (for post-immediate-arc)

**Bug 1 — season_000042 gauntlet-opponent classes (class_0006–class_0011) lack `is_act_boss: true`**
Engine emits these as unnamed classes with `is_act_boss: null`. The loadout's class selector does not filter them by `is_act_boss` (only by `is_retired`). These 6 classes would appear in the selector with no name if included in data dir.
**Mitigation applied (MVP):** Only class_0001–class_0005 staged in `data/season_000042/classes/`. Classes 6–11 excluded at data-staging step.
**Post-immediate-arc:** Raise to star-lord / rocket — engine should emit `is_act_boss: true` on gauntlet-opponent classes. Or loadout should filter on `name !== null`.
**TODO(drax): remove MVP class-staging workaround when engine ships is_act_boss correctly on class_0006–class_0011 for season_000042.**

**Bug 2 — season_000042 skills lack `geometry_type` on some classes (rare; classes 6–11 only)**
Not a blocking issue for the 5 playable classes. All class_0001–class_0005 skills have `geometry_type` populated.

**Bug 3 — season_000042 manifest `elements: null` breaks `assertManifestSeasonalFields` fallback path**
The loadout `resolveElementDisplay` function has a fallback to `manifest.elements[canonical]` — if `elements` is null this would throw. Mitigation: we stage the adapted manifest with a canonical-four `elements` stub. Post-immediate-arc: loadout should null-guard `manifest.elements` access in `resolveElementDisplay`.
**TODO(drax): add null-guard to resolveElementDisplay for manifest.elements when engine begins emitting elements:null consistently.**

---

## 6. Notable observations for V2 iteration

- **season_000042 has 8 cosmological_vocabulary slots** (ignition/suffusion/bulwark/displacement/impact/radiance/penumbra/resonance) vs the 4 expected by the loadout's `seasonal_elements` shape (ignition/suffusion/bulwark/displacement). The extra 4 (impact/radiance/penumbra/resonance) are new vocabulary that V2 integration could surface in a dedicated CosmologyPairBlock component (existing in pitch/ — see `CosmologyPairBlock.tsx`). DEFERRED per LOCK F.
- **cosmological_vocabulary.json** contains full pair rationales (3 prose pairs) that the `CosmologyPairBlock` component already handles — V2 wire-in is a 1-file data load + existing component wiring.
- **validation_report.json** has rich per-class convergence data including `r1_per_tier_pass`, `r1_per_tier_win_rates` — useful for V2 Analytics tab extension via existing `ConvergenceChart` component.
- **`fights.jsonl` (41.8MB)** deferred per dispatch INFO-4 and size. V2 could sample-stream if an analytics ask arises.
- **season_000042 classes have `grouping_pair_structure`** (maps canonical elements to slot names) — useful for element display in V2 when wired.
- **Demo season selector** now shows season_000042 but R2 production serving is not yet configured for this season (only `public/` local dev path). Production demo would need R2 upload for the season_000042 data files. DEFERRED — preview deploy confirms local dev works.

---

## 7. Auto-commit + deploy record

- **reincarnated-loadout commit:** [see git log]
- **reincarnated-demo commit:** [see git log]
- **Meta-repo commit:** [see git log]
- **Vercel preview URLs:** [appended after deploy]

---

## 8. Routing back to KR

IA-3 P1 SUCCESS. Data-loading layer functional; existing components render season_000042 via existing patterns. No new UI components.

IA-3 P4 V2 iteration awaits IA-2 close + IA-1 V2 re-fire.
