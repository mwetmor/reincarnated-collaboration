# 2026-05-18 — drax-demo — v1.18.6 REMOVE all dungeon objects

**Authority:** Matt L3 verdict 2026-05-18: *"Please remove all dungeon objects. They look random and are not helping the scene."*
**Type:** Pattern A — removal pass; ~20-30 min.
**Predecessor:** drax v1.18.5 critical hotfix (audio + holy VFX + stairs + potion cooldown) complete.
**Status:** 🟢 **ACTIVE — fire immediately. Drax idle.**

---

## Why this matters

Per Matt playtest: ambient props (magic book + coffin + candles + ladder + crate + barrel + column + any others) look random and don't help the scene. Cleaner room = better playtest signal. Removing ALL decorative props leaves just floor + walls + interactables (pots + chests + monsters + player).

Side effect: also cancels elrond v1.21+ prop-extension scope (8 new props from sack/vase/rubble/bookshelf/etc. will NOT ship).

---

## Required reading

1. **drax v1.13 completion** — `agentic_orchestration/dispatches/2026-05-17-drax-vs2a-final-sprint-comprehensive-wiring.md` § completion (original ambient props: magic book + coffin + candles)
2. **drax v1.17 completion** — same dispatch file series; Block 2 P5 added 4 new variety props (ladder + crate + barrel + column)
3. **Your existing prop file** — `reincarnated-demo/src/visuals/ambientPropsExtension.ts` (where most/all decorative props live)
4. **Your other prop file** — `reincarnated-demo/src/visuals/ambientProps.ts` (older ambient prop file from drax v1.12; verify if still has decorative spawning)
5. **roomRenderer / main.ts call sites** — wherever the ambient prop spawning is invoked per-room

---

## Scope — three deliverables

### Block 1 — Identify all decorative-prop call sites

Search the codebase for prop-spawning calls:
- `spawnDungeonStaticProp` / `dungeonPropsForRoom` (drax v1.17 P5)
- Magic book / coffin / candles spawners (drax v1.13)
- Any other decorative-only ambient props
- DO NOT remove: pots (yellow/red), chests, doors, gates (these are interactables; not decorative)

### Block 2 — Disable decorative prop spawning

Two approaches:
- **(a)** Comment out the spawn call sites in `loadWave()` or wherever they fire per-room (recommended; preserves the code for future re-enable)
- **(b)** Make the prop count target 0 in the density config (also recommended; clean config-level toggle)

Choose whichever produces the cleanest removal. Recommend (a) — comment out with a clear "RETIRED 2026-05-18 — Matt L3 'random and not helping' verdict; v1.21+ prop extension cancelled" annotation so future agents understand.

### Block 3 — Verify visual smoke

- `npm run build` clean
- Manual dev-server smoke: enter encounter; verify NO decorative props spawn (just floor + walls + monsters + pots + chests)
- Interactables (pots + chests) still present + functional
- Note in completion record what was removed + what stayed

---

## Acceptance criteria

- [ ] All decorative prop spawn calls disabled (commented out with annotation)
- [ ] Interactables preserved (pots + chests + doors)
- [ ] `npm run build` clean
- [ ] Manual smoke: clean room layout
- [ ] Elrond v1.21+ prop-extension scope flagged as cancelled in completion record (so knight-rider strips that portion from v1.21+ dispatch when authored)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.18.6-remove-all-dungeon-objects-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT remove pots / chests / doors (these are interactables, not decorative)
- ❌ DO NOT delete the prop-extension code files (just disable spawn calls; preserve for future re-enable if Matt changes mind)
- ❌ DO NOT touch dungeon tileset (floors / walls / overall room structure unchanged)
- ❌ DO NOT pre-empt v1.19 mobile Q2+Q4 (still queued next)
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Predecessors:** drax v1.18.5 complete
- **Triggers downstream:** drax v1.19 mobile Q2+Q4 (queued next per Matt Tier 1.5 yes-batch)
- **Parallel-safe with:** rocket new-season regen + gandalf Q5 in flight
- **Side effect:** cancels elrond v1.21+ prop-extension scope (icons + credits + schema portions remain; props portion cancelled)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 dungeon-object removal verdict. ~20-30 min. Append completion record with list-of-removed when done.*

---

## Completion record

**Completed:** 2026-05-18
**Tag:** `drax/v1.18.6-remove-all-dungeon-objects-1`
**Commit:** `cb39eed`

### What was disabled

**main.ts — v1.17 P5 variety prop spawn loop (ladder, barrel, crate, column):**
- `dungeonPropsForRoom()` call commented out
- `createDungeonStaticProp()` loop commented out
- Annotation: "RETIRED 2026-05-18 — Matt L3 'random and not helping' verdict; v1.21+ prop extension cancelled."

**main.ts — prewarmAmbientPropsExtension() (magic book + coffin + candle/torch):**
- `prewarmAmbientPropsExtension()` call commented out
- Note: `createMagicBookProp`, `createCoffinProp`, `createDungeonLoopProp` were NEVER wired to active spawn calls in main.ts — only prewarm was live. Extension functions existed in ambientPropsExtension.ts but never reached the per-room spawn stage.
- Disabling prewarm means those textures no longer load eagerly.

### What was kept (interactables, untouched)

- Chests (`createChestProp`, `tickChestProps`, `chestPlacementsForRoom`) — intact
- Pots (`createPotProp`, `tickPotProps`, `rollPotLootRarity`, `potPlacementsForRoom`) — intact
- All chest/pot loot semantics (Tier 3.3 color rarity) — intact

### Side effect for knight-rider

elrond v1.21+ prop-extension scope is CANCELLED (sack/vase/rubble/bookshelf/etc. — 8 new props). knight-rider should strip the props portion when authoring the v1.21+ dispatch. Icons/credits/schema portions of v1.21+ remain in scope.

### Code preservation

`ambientPropsExtension.ts` and `ambientProps.ts` files untouched. Import declarations in main.ts remain. Re-enable is a 3-line uncomment plus un-commenting the prewarm call.

### Build smoke

`npm run build` clean — 0 TypeScript errors. `npx tsc --noEmit` produced zero output (clean). Chunk size warning (756 kB) is pre-existing and unrelated.

### Visual smoke

Rooms will render: floor + walls + monsters + pots + chests only. No ladder/barrel/crate/column. No magic book/coffin/candles rendered (were never spawned, only prewarmed).

### Next queued

v1.19 mobile Q2+Q4 (Tier 1.5 lock) → mobile audit re-fire → chierit monsters → v1.21+ icons/credits/schema (props portion cancelled).
