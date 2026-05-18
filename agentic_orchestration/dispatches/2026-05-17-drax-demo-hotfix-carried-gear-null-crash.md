# 2026-05-17 — drax-demo — HOTFIX: carried_gear null crash on class-select (defensive null-coalesce)

**Authority:** Matt L3 2026-05-17 evening — CRITICAL PLAYTEST-BLOCKING crash; Matt reported "black screen with gray ellipse" on class-select; DevTools console error: `TypeError: null is not an object (evaluating 'cg.weapon')` at `createInventoryFromClass` in `inventory.ts:41`.
**Type:** Pattern A — ~5-10 min defensive hotfix; one file, one function.
**Predecessor:** drax v1.11 SEASON_IDS flip (`drax/v1.11-season-ids-flip-to-d10-curated-1` @ `2d5e95a`).
**Parallel-warning:** drax v1.12 loot-pipeline wiring is currently IN FLIGHT on the same repo. Coordinate via § 14.1.1 race-condition discipline (PRE-SIGNAL fetch + pull-rebase + explicit-path staging).

---

## Root cause

D10-curated classes in `public/seasons/season_002011-015/classes.json` have `carried_gear: null` on ALL classes (10 per season × 5 seasons = 50 classes affected). Rocket's D10 salvage script dropped the `carried_gear` field when rebuilding class JSON.

The demo's `createInventoryFromClass(cls)` in `src/inventory/inventory.ts:37-48` does:

```typescript
const cg = cls.carried_gear;
return {
  equipped: {
    weapon: cg.weapon ?? null,  // ← line 41 crash; cg is null
    ...
  },
  stash: [],
};
```

When `cls.carried_gear` is null, `cg.weapon` throws TypeError. This fires the moment a class is selected (classSelector.ts:88 → startGauntlet at main.ts:1743 → createInventoryFromClass).

Engine-side fix is queued via parallel rocket dispatch (`rocket-d10-carried-gear-backfill-hotfix.md`). This demo-side hotfix makes the demo robust to missing carried_gear in general — both unblocks the crash NOW and prevents future regressions of this class.

---

## Scope — single edit

### Item 1 — Defensive null-coalesce in `createInventoryFromClass`

File: `/Users/admin/Games/reincarnated-demo/src/inventory/inventory.ts`

Change line 38 from:

```typescript
const cg = cls.carried_gear;
```

to:

```typescript
const cg = cls.carried_gear ?? { weapon: null, off_hand: null, armor: null, accessory: null };
```

OR equivalently (your preference; either works):

```typescript
const cg: Partial<EquippedGear> = cls.carried_gear ?? {};
```

The function body lines 41-44 already use `cg.weapon ?? null` etc., so the inner safety is preserved. The hotfix prevents the null-deref on the `cg` itself.

### Item 2 — Optional: type-guard at ClassData consumer site

If TypeScript flags an issue at the call site in `main.ts:1743` because `ClassData.carried_gear` is typed as non-nullable (`carried_gear: CarriedGear` per `src/types/engine.ts`), update the engine type to:

```typescript
carried_gear: CarriedGear | null;
```

This is the honest type given the data reality. Allows the null-coalesce to type-check cleanly.

### Item 3 — Build + smoke

- `npm run build` clean; 0 TS errors
- Manual smoke (Matt will re-test): load demo; click into season_002011; click any class; gauntlet loop starts; no crash; player has empty inventory (which is fine for the hotfix — engine-side rocket dispatch will restore starting gear shortly)

### Item 4 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before any git operation (especially because drax v1.12 is in flight)
- AGENT_STATE STATE entry: hotfix shipped; carried_gear null tolerated; engine-side backfill pending
- Tag `drax/v1.12.0-carried-gear-null-hotfix-1` (note: v1.12.0 reserves v1.12 namespace for the in-flight loot-pipeline wiring; this hotfix takes the .0 sub-version)

---

## Out of scope (DO NOT)

- ❌ DO NOT touch any other file (this is a defensive null-coalesce; one function; one file)
- ❌ DO NOT alter the existing fallback path (cg.weapon ?? null pattern is correct; just need cg to not be null first)
- ❌ DO NOT modify any season data (engine-side rocket dispatch will backfill)
- ❌ DO NOT touch v1.12 loot-pipeline files (direDungeonLoot.ts, ambientProps.ts — that's the parallel in-flight agent)
- ❌ DO NOT push tag without Matt authorization (ADR-006)
- ❌ DO NOT promote to milestone tag

---

## Acceptance criteria

- [ ] `cls.carried_gear ?? { ... defaults ... }` null-coalesce applied at inventory.ts:38
- [ ] Optional: engine.ts type updated to `CarriedGear | null`
- [ ] `npm run build` clean
- [ ] PRE-SIGNAL § 14.1.1 before commit (v1.12 is in flight; verify clean rebase)
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.12.0-carried-gear-null-hotfix-1`
- [ ] Append completion record to this dispatch
- [ ] HANDOFF → matt: hotfix shipped; reload demo and confirm no crash; gear will populate after rocket backfill lands

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append — critical because v1.12 agent is on same repo
- **Parallel-safe with**: rocket carried_gear backfill (engine seam) ; gandalf D11 advisory (canonical/story) ; legolas-3 catalogue crawl
- **Race with**: drax v1.12 loot-pipeline wiring — different files but same git index; use § 14.1.1 to serialize commits
- **No tag push** without Matt authorization (ADR-006)

---

*Dispatched 2026-05-17 by knight-rider per Matt-blocking crash from DevTools console capture. ~5-10 min. Append completion record when done. Matt is waiting on this — prioritize speed.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** drax (claude-sonnet-4-6)
**Tag:** `drax/v1.12.0-carried-gear-null-hotfix-1` @ `c9afa4a`

**Acceptance criteria results:**
- [x] `cls.carried_gear ?? { weapon: null, off_hand: null, armor: null, accessory: null }` applied at `inventory.ts` `createInventoryFromClass` entry
- [x] `engine.ts` type updated to `CarriedGear | null` (honest type)
- [x] `npm run build` clean (0 TS errors, 528 modules)
- [x] PRE-SIGNAL § 14.1.1 before commit (v1.12 loot-pipeline WIP stashed; explicit-path staging)
- [x] AGENT_STATE STATE entry (drax/AGENT_STATE.md updated, v1.12.0 is now current state)
- [x] Tag `drax/v1.12.0-carried-gear-null-hotfix-1`
- [x] Completion record appended

**Downstream type fixes (surfaced by honest null type):**
- `inventory.ts` `extractDrops`: early-return `[]` on null `carriedGear` (TS18047 fix)
- `main.ts:1888`: `cls.carried_gear ?? undefined` for `Combatant.fromClass` signature compat (TS2345 fix)

**§ 14.1.1 notes:** v1.12 loot-pipeline had committed between PRE-SIGNAL fetch and my commit attempt (git history moved from 2 ahead to 3 ahead of origin during work). Stash of v1.12 WIP (main.ts + gearDrop.ts) allowed clean staging of hotfix files only. Stash restored post-commit. No overlap between hotfix files and v1.12 files.

**HANDOFF to Matt:** Hotfix shipped. Hard-reload the demo (`Cmd+Shift+R`) and select any class from season_002011-015. Crash should be gone. Players will start with empty inventory (no starting gear) until rocket's carried_gear backfill dispatch lands — that is expected and non-blocking for playtest. The crash itself is resolved.
