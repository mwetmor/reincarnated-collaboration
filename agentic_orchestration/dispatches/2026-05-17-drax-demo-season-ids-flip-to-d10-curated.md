# 2026-05-17 — drax-demo — SEASON_IDS flip to D10-curated (002011-015)

**Authority:** Matt L3 2026-05-17 evening — accepting 37.1% convergence for playtest; D10 is a clear improvement; demo unblocks D11 empirical validation.
**Type:** Pattern A — ~10 min micro-task.
**Predecessor:** drax v1.10 SEASON_IDS revert to historical (`drax/v1.10-season-ids-revert-to-historical-1` @ `5606b9f`) + rocket v1.12 D10 salvage (`rocket/v1.12-d10-implementation-and-staged-data-salvage-1` @ `c0a622a`).

---

## Why this matters

Rocket D10 salvage shipped: all 5 staged seasons (002011-015) are now D10-curated. 51/51 classes retained, 572→473 skills (pruned per archetype ceilings + element-breadth gate + buff_damage limit), geometry_type populated on all 473 skills, 200 gear items per season (was empty), schema_version=v1.7, post_process_d10=True provenance.

Convergence: 37.1% average (range 20-45%) — below the 50% target but a clear +6.1pp improvement vs pre-D10. The shortfall is dominated by hybrid_mage structural over-generation; D11 sprint authorized to address. Matt's call: ship D10-curated to playtest NOW; D11 fix follows.

This dispatch flips SEASON_IDS from historical 001001-005 back to D10-curated 002011-015 so playtest validates the D10 substrate rules empirically.

---

## Required reading

1. `reincarnated-demo/src/data/loader.ts` — current `SEASON_IDS` (points at 001001-005 historical) + `TODO(drax)` override block lines 1-12 (now to be removed)
2. `reincarnated-demo/public/seasons/` — both sets currently present (additive); 002011-015 are D10-curated as of rocket v1.12
3. Rocket D10 completion record: `agentic_orchestration/dispatches/2026-05-17-rocket-d10-implementation-and-staged-data-salvage-queued.md` § Completion record
4. Verify a 002011-015 season locally: `reincarnated-demo/public/seasons/season_002011/classes.json` — confirm `geometry_type` populated (non-null) on at least 5 skills + `gear_pool.json` has 200 items

---

## Scope

### Item 1 — Update SEASON_IDS

Edit `reincarnated-demo/src/data/loader.ts`:

```typescript
// D10-curated seasons (post-substrate-coherent gen-math + salvage)
// 37.1% avg convergence (range 20-45%); D11 sprint authorized for hybrid_mage tuning
export const SEASON_IDS = [
  'season_002011',
  'season_002012',
  'season_002013',
  'season_002014',
  'season_002015',
];
```

### Item 2 — Remove TODO(drax) override block

The TODO(drax) override block at lines 1-12 (added in v1.10 revert) is no longer load-bearing — D10 landed; geometry_type is non-null; gear_pool is populated. Remove the block cleanly.

### Item 3 — Keep season_001001-005 in public/seasons/

ADDITIVE: leave 001001-005 in `public/seasons/` (no deletion). SEASON_IDS gates UI exposure; extra directories on disk are harmless and preserve fallback investigability.

### Item 4 — Sync to loadout (if needed)

Loadout already retains both sets per drax-loadout v1.1. If drax-loadout's `data/` does NOT have the D10-curated versions of 002011-015 (i.e., it has the pre-D10 broken versions from before rocket v1.12), this dispatch should also refresh loadout's data/ to point at the curated versions.

**Check first:** `reincarnated-loadout/data/season_002011/classes.json` — does at least one skill have `geometry_type` populated? If yes, loadout already has curated data; skip. If no, copy fresh from `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011-015/` (post-D10 outputs).

### Item 5 — Verify demo plays

- `npm run build` clean; 0 TS errors
- Manual smoke: load demo; click into season_002011; class selector populates; click a class; gauntlet loop renders (geometry-typed skills visible; no black screen; gear renders)
- Spot-check 2-3 hybrid_mage classes (these are the known unconverged set) — they should still render (just with floor modifiers, not crash)

### Item 6 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry: D10-curated seasons live; TODO(drax) override removed; loadout sync status noted
- Tag `drax/v1.11-season-ids-flip-to-d10-curated-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT delete season_001001-005 from `public/seasons/` (keep additive for fallback)
- ❌ DO NOT modify any engine-side season data (consume only)
- ❌ DO NOT touch step-3 VFX integration (v1.8 stays intact)
- ❌ DO NOT touch M1 typography (v1.7 stays intact)
- ❌ DO NOT promote to milestone tag
- ❌ DO NOT pre-empt D11 sprint (separate dispatch chain)

---

## Acceptance criteria

- [ ] `SEASON_IDS` flipped to 002011-015 in `src/data/loader.ts`
- [ ] TODO(drax) override block removed (no longer load-bearing)
- [ ] 001001-005 retained in `public/seasons/` (additive)
- [ ] Loadout `data/` sync verified (curated versions present)
- [ ] `npm run build` clean
- [ ] Manual smoke: demo plays 002011-015 with no black screen; geometry-typed skills render
- [ ] Tag `drax/v1.11-season-ids-flip-to-d10-curated-1`
- [ ] Hive-log STATE entry

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append
- **Parallel-safe with** D11 sprint dispatches (gandalf advisory + queued gamora/rocket); they operate on engine seam not demo
- **No tag push** without Matt authorization (ADR-006)

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 acceptance of 37.1% D10 outcome. ~10 min. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by drax
**Demo tag:** `drax/v1.11-season-ids-flip-to-d10-curated-1` @ `2d5e95a`
**Loadout companion commit:** `46ac06d` (data/season_002011-015 per-class + manifests refreshed)
**AGENT_STATE commit:** `bd700bd`

**Acceptance criteria status:**
- [x] `SEASON_IDS` flipped to 002011-015 in `src/data/loader.ts`
- [x] TODO(drax) override block removed (lines 1-12; no longer load-bearing)
- [x] 001001-005 retained in `public/seasons/` (additive)
- [x] Loadout `data/` sync verified and refreshed (D10 per-class files + manifests; geometry_type is a monolithic-only field, not present in per-class schema — noted in STATE)
- [x] `npm run build` clean (526 modules, 0 TS errors)
- [x] Smoke: geometry-typed skills present (473/473 across 5 seasons); gear_pool 200 items per season
- [x] Spot-check hybrid_mage: render with floor modifiers (damage_multiplier=1.0), no crash; geometry_type populated
- [x] Tag `drax/v1.11-season-ids-flip-to-d10-curated-1` applied (local; no push per ADR-006)
- [x] Hive-log STATE entry appended

**Non-blocking observation for knight-rider/rocket:**
Engine output per-class files (classes/ subdirectory) for seasons 002014 and 002015 have fewer skills than the monolithic classes.json in the same output directory (96 vs 98; 94 vs 97). The D10 pruning appears to have been applied to the monolithic file only, not back-propagated to the per-class files. Demo uses monolithic (correct source); loadout uses per-class (per its established consumer pattern). No demo or loadout defect — flagged for engine-side awareness.
