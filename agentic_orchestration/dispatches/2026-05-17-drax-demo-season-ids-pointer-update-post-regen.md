# 2026-05-17 — drax-demo — SEASON_IDS pointer update post-regen

**Authority:** Matt L3 2026-05-17 (~21:30 EDT). Gamora standard-demo regen complete (process exited; 5 seasons + summary written).
**Type:** Pattern A — ~30 min micro-task.
**Predecessor:** gamora standard-demo fresh regen (`agentic_orchestration/dispatches/2026-05-17-gamora-standard-demo-fresh-regen-post-d3-pre-d10.md` — staging path: `reincarnated-engine/output/standard-demo-regen-2026-05-17/`).

---

## Why this matters

Gamora's regen wrote 5 fresh seasons (002011-002015) to staging. Per the regen dispatch's HANDOFF contract, drax-demo handles the copy + pointer-update so the demo consumes the new roster. All 7 canonical substrates present; 51 classes; substrate distribution per `regen_summary.json`. This is the pre-D10 build (mean convergence ~31% — expected per gandalf prediction; rough kits acceptable for visual variety playtest).

---

## Required reading

1. `reincarnated-engine/output/standard-demo-regen-2026-05-17/regen_summary.json` — substrate distribution + season IDs
2. `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/` (and 002012-002015) — staged season directories; each contains: classes/, classes.json, cosmological_vocabulary.json, damage_formula.md, design_context.md, fights.jsonl, gear/, gear_pool.json, generation_log.txt, manifest.json
3. `reincarnated-demo/public/seasons/` — current state (season_001001-001005 present)
4. `reincarnated-demo/src/data/loader.ts` — `SEASON_IDS` constant currently pointing at 001001-001005

---

## Scope

### Item 1 — Copy staged seasons into demo

Copy each of `season_002011-002015` from `reincarnated-engine/output/standard-demo-regen-2026-05-17/` to `reincarnated-demo/public/seasons/`.

Strategy: **REPLACE** the existing 001001-001005 set with 002011-002015 (cleaner; pre-D10 ship-target).

Optional alternative if any season-001 files are referenced by tests or anchor decisions-log entries: PRESERVE 001001-001005 alongside 002011-002015 (additive); document chosen strategy in completion record. Default = replace.

### Item 2 — SEASON_IDS pointer update

Edit `reincarnated-demo/src/data/loader.ts`:

```typescript
// BEFORE
export const SEASON_IDS = [
  'season_001001',
  'season_001002',
  'season_001003',
  'season_001004',
  'season_001005',
];

// AFTER (default replace strategy)
export const SEASON_IDS = [
  'season_002011',
  'season_002012',
  'season_002013',
  'season_002014',
  'season_002015',
];
```

### Item 3 — Verify demo loads new seasons cleanly

- `npm run build` clean; 0 TS errors
- Manual smoke: load demo; verify season selector shows the 5 new seasons; pick one; verify class selector populates with the new roster (canonical-7 substrates visible)
- Verify gear/pool data loads without runtime errors

### Item 4 — Hive log + tag

- PRE-SIGNAL § 14.1.1 (drax step-3 VS2a first VFX integration is in flight in parallel — race-condition discipline critical; pull-rebase before commit)
- STATE entry documenting: replace/additive strategy chosen; smoke result; ship-state of pre-D10 regen now consumable by demo
- Tag `drax/v1.9-season-ids-pointer-update-post-regen-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify any season-data content (engine-side artifacts; copy-as-is)
- ❌ DO NOT touch step-3 VFX integration work (different drax instance is handling that)
- ❌ DO NOT change M1 typography (locked at v1.7)
- ❌ DO NOT modify game logic to handle the new substrates (lightning/holy/shadow); demo already renders 7 substrates per v1.0+ work
- ❌ DO NOT promote this to a Matt-approved milestone tag (this is pre-D10 shim regen; not ship-target)

---

## Acceptance criteria

- [ ] season_002011-002015 directories copied to `reincarnated-demo/public/seasons/`
- [ ] `SEASON_IDS` updated in `src/data/loader.ts`
- [ ] Replace-vs-additive strategy documented in completion record
- [ ] `npm run build` clean; 0 TS errors
- [ ] Demo loads new seasons (manual smoke verified)
- [ ] Tag `drax/v1.9-season-ids-pointer-update-post-regen-1`
- [ ] Hive-log STATE entry

---

## Smoke test

1. `npm run build` clean
2. Load demo; season selector shows 002011-002015
3. Pick season_002011; class selector populates with 7-substrate roster
4. Pick a class; loads cleanly; loadout panel works
5. Run a gauntlet fight; no runtime errors

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append; pull-rebase before commit. Drax step-3 VS2a first VFX integration (different drax instance) is in flight in parallel; both touch the same demo repo. Race-condition discipline is critical here.
- **No engine-side changes** — staged regen output is authoritative

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 + regen completion. ~30 min. Append completion record when done.*
