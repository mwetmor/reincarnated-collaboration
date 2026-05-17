# 2026-05-17 — drax-demo — SEASON_IDS revert to historical (broken-data hotfix)

**Authority:** Matt L3 2026-05-17 (~23:00 EDT) per black-screen playtest finding + diagnostic root-cause analysis.
**Type:** Pattern A — ~10 min micro-task.
**Predecessor:** drax v1.9 SEASON_IDS pointer update (`drax/v1.9-season-ids-pointer-update-post-regen-1` @ `f6456f4`) — this hotfix UNDOES that ship.

---

## Why this matters

Diagnostic root-cause: the new season_002011-015 staged from gamora's pre-D10 shim regen contain incomplete class kits — **all 114 skills have `geometry_type: null`** and **`gear_pool.json` is empty (0 items)**. The demo's renderer consumes `skill.geometry_type` at 5+ critical sites (AOE indicator spawn, audio cast, weapon animation, range check); null geometry breaks the gauntlet loop → **black screen with gray ellipse fallback**.

The structural fix is engine-side (D10 substrate-coherent gen-math; gamora + rocket; ~2-3 days). This dispatch is the **temporary unblock** — restore season_001001-005 to demo so playtest stays viable while engine fixes land.

**Loadout retains both sets** (drax-loadout v1.1 has 001001-005 + 002011-015 alongside each other in `reincarnated-loadout/data/`) — so analytics + research view of the new seasons stays available even after this revert.

---

## Required reading

1. `reincarnated-demo/src/data/loader.ts` — current `SEASON_IDS` (points at 002011-015)
2. `reincarnated-demo/public/seasons/` — currently has 002011-015 only (drax v1.9 REPLACE strategy removed 001001-005)
3. Git history: prior commit `230c855` had season_001001-005 in `public/seasons/`; restore from there or from `reincarnated-engine/seasons/` if present

---

## Scope

### Item 1 — Restore season_001001-005 to demo

Source options (whichever is cleanest):
- **A.** `git checkout 230c855 -- public/seasons/season_001001 public/seasons/season_001002 ... 001005` (restore from git history)
- **B.** Copy from `reincarnated-engine/seasons/season_001001/...001005/` (engine-side authoritative; check structure matches loader expectations)
- **C.** Cherry-pick the specific files (metadata.json + classes.json + monsters.json + gear_pool.json) for each season

Recommended: **A** (git history is authoritative; preserves prior structure exactly).

### Item 2 — Update SEASON_IDS

Edit `reincarnated-demo/src/data/loader.ts`:

```typescript
// REVERT to historical (D10 hotfix; new seasons in loadout's data/ alongside)
export const SEASON_IDS = [
  'season_001001',
  'season_001002',
  'season_001003',
  'season_001004',
  'season_001005',
];
```

### Item 3 — Keep new seasons available in public/seasons/

**ADDITIVE strategy this time:** keep season_002011-015 in `public/seasons/` (don't delete) so any future investigation / preview / debugging has the data accessible. The `SEASON_IDS` constant gates what the demo's UI exposes; having extra dirs in public/seasons/ is harmless.

This is the inverse of v1.9's REPLACE strategy — we're now keeping both, gating via SEASON_IDS.

### Item 4 — Verify demo plays

- `npm run build` clean; 0 TS errors
- Manual smoke: load demo; click into season_001005; class selector populates; click a class; gauntlet loop renders properly (no black screen; geometry-typed skills visible)

### Item 5 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry: revert reason (engine-side data gap diagnosed); demo playable on historical seasons; loadout retains both sets
- Tag `drax/v1.10-season-ids-revert-to-historical-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT delete season_002011-015 from `public/seasons/` (keep additive)
- ❌ DO NOT modify any engine-side season data
- ❌ DO NOT touch step-3 VFX integration (v1.8 stays intact)
- ❌ DO NOT touch M1 typography (v1.7 stays intact)
- ❌ DO NOT promote to milestone tag
- ❌ DO NOT modify loadout (drax-loadout v1.1 retains both season sets correctly)

---

## Acceptance criteria

- [ ] season_001001-005 restored to `public/seasons/`
- [ ] season_002011-015 retained alongside (additive)
- [ ] `SEASON_IDS` reverted to 001001-005
- [ ] `npm run build` clean
- [ ] Manual smoke: demo plays season_001005 with no black screen
- [ ] Tag `drax/v1.10-season-ids-revert-to-historical-1`
- [ ] Hive-log STATE entry

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append
- **No parallel demo-repo agents** at moment of this dispatch (drax v1.8 + v1.9 already shipped)
- **Loadout untouched** — drax-loadout v1.1 retains both season sets correctly

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 hotfix + diagnostic root-cause. ~10 min. Append completion record when done.*
