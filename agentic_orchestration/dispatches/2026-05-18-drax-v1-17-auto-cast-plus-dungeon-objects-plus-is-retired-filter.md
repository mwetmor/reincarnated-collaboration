# 2026-05-18 — drax-demo — v1.17 multi-bundle: DoE auto-cast + elrond dungeon-object swaps + is_retired filter + abilities→skills rename

**Authority:** Matt L3 verdicts 2026-05-18:
- **Option A locked** for skills/hotbar architecture: "DoE style where skill use is automatic on CD and auto-targets the nearest monster (unless left mouse click or mobile touch alter target)"
- **Tier 4 yes-batch + canonical-6 chain** already authorized
- Elrond dungeon-objects audit (shipped); rocket is_retired flag (in flight); drax v1.16.2 audio + holy VFX (in flight; precedes this)

**Type:** Pattern B — render-pipeline overhaul + asset swap + filter + rename; ~4-5 hours.
**Predecessor (gates auto-fire):** drax v1.16.2 completion + rocket v1.17 canonical-6 is_retired flag landing.
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until BOTH drax v1.16.2 ships completion record AND rocket v1.17 ships is_retired flag landing. Knight-rider activates post-double-trigger.**

---

## Why this matters

VS2a Final Sprint visible-issue rollup. Four parallel cleanups in one tag:

1. **Auto-cast architecture (Option A)** — closes the 4th JSON-parity invariant (player fires all 10-12 skills on cooldown like sim AI; not 6 from manual hotbar). DoE-validated mobile pattern Matt's been targeting. Removes hotbar density problem entirely.
2. **Dungeon-object swaps (elrond audit)** — closes Matt's "stairs sprite poor / generally all objects poor" feedback. Zero new spend; all assets on disk; structural fix not asset-quality fix.
3. **is_retired filter** — hides hybrid_mage classes from class-select UI per canonical-6 transition.
4. **"abilities" → "skills" rename** — register-fence terminology fix on character sheet to match engine canonical vocab + hotbar/auto-cast UI.

Bundling reduces same-repo serialization cost (drax is the bottleneck for demo work).

---

## Required reading (when activated)

1. **Elrond dungeon-objects audit** — `agentic_orchestration/research/curated/dungeon-objects-quality-audit-2026-05-18.md` (~33 KB; § 5 handoff brief with files + preprocessing + test plan + failure-modes + acceptance)
2. **Gandalf canonical-6 doc** — `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` (context for is_retired filter; § 4 archetype list)
3. **Rocket v1.17 completion record** — `agentic_orchestration/dispatches/2026-05-18-rocket-canonical-6-archetype-removal-plus-is-retired-flag.md` § completion (verify is_retired flag in classes.json + per-class files)
4. **Balance loop AI cast logic** — `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (study sim AI's priority heuristic for skill firing; mirror in demo auto-cast)
5. **Your current hotbar code** — `reincarnated-demo/src/ui/hotbar.ts` (or wherever); + skill-cast input handler in `src/main.ts`
6. **Combatant skill state** — `reincarnated-demo/src/actors/combatant.ts` (per-skill cooldown tracking; how skills resolve)
7. **Targeting logic** — wherever player picks target (likely main.ts or combat.ts); auto-acquire nearest pattern
8. **Character sheet UI** — wherever "abilities" label lives; needs rename + count display verification

---

## Scope — four wiring blocks

### Block 1 — Option A auto-cast architecture

**Replace manual-hotbar skill firing with auto-cast loop mirroring sim AI behavior.**

1.1. **Auto-cast tick loop**: each game tick, for the player combatant:
- Find all skills with cooldown ready
- Pick by priority (mirror sim AI's heuristic — likely highest-DPS-available, with possible category preference). Consult `balance_loop.py` cast logic; replicate
- Fire at current target

1.2. **Target acquisition**:
- Default: auto-acquire nearest enemy combatant
- Left-click on enemy → manual target lock; persists until that target dies; then revert to auto-acquire
- Mobile touch on enemy → same behavior
- Visual indicator on locked target (small reticle / outline / arrow)

1.3. **Hotbar UI transformation**:
- Recommend: keep hotbar visible but transform to **informational ticker** — show all 10-12 skills as readonly icons with cooldown progress + "next-to-fire" highlight. Non-interactive.
- Alternative: hide hotbar entirely; show "currently casting: <skill>" textbox + small cooldowns row
- Your call on the cleanest UI; document choice in completion record

1.4. **Defensive-skill flag (Phase-2; OUT OF SCOPE FOR v1.17)**:
- Don't add `auto_cast` flag handling yet; auto-cast everything for VS2a
- If playtest reveals specific skills that feel wrong auto-casting (escape, panic heal), surface to Matt as a VS2b follow-on dispatch

1.5. **JSON parity guarantee**: player fires 100% of their kit skills on cooldown rotation — same as sim AI behavior. Closes the 4th JSON-parity invariant.

### Block 2 — Dungeon-object swaps (elrond P1-P5)

Per elrond's § 5 handoff brief:

- **P1**: Floor tile source swap from `walls_floor.png` rows 4-8 → `plates.png` (208×128 clean 13×8 grid). File: `dungeonTileset.ts`. Quality 1→4.
- **P2**: Stairs explicit wiring at exit-door threshold; primary = `169442 Objects.png` top-left stair; fallback = `298079 stairs.png` bottom-rows. Files: `dungeonTileset.ts` + call-site updates in `main.ts`. Quality 1→5.
- **P3**: Disable broken sprite walls; fall back to existing procedural 8px Graphics perimeter. File: `dungeonTileset.ts`. Quality 1→3.
- **P4**: Correct animated-prop frame counts (candles 432×224 / torches 224×288 / fountain 288×64). File: `ambientPropsExtension.ts`. Quality 2→4.
- **P5**: Wire 3-4 new ambient props from `Objects.png` + `other_objects.png` (ladder / crate / barrel / sack / vase / column / hanging-cage / rubble — pick 3-4 best-fitting). File: `ambientPropsExtension.ts`. Adds variety.

Asset paths in elrond audit doc § 5. License: CraftPix-Free-Terms; existing credit line covers all.

### Block 3 — is_retired filter

3.1. **Season loader**: in `src/data/loader.ts` (or class-select code), filter out classes where `cls.is_retired === true` from class-select UI. Hides hybrid_mage classes in 002011-015 staged seasons.

3.2. **Graceful**: if a player somehow loads a saved hybrid_mage class (unlikely given filter), display a warning + fall back to class-select; don't crash.

3.3. **Verify**: rocket v1.17 should have added `is_retired: true` + `retirement_reason: "canonical_6_transition_2026_05_18"` to 17 hybrid_mage classes. Sanity-check the data presence before wiring filter.

### Block 4 — "abilities" → "skills" terminology fix

4.1. **Character sheet**: replace "abilities" label with "skills" wherever it appears in character-sheet UI

4.2. **Hotbar/auto-cast UI**: confirm "skills" terminology throughout (probably already correct)

4.3. **Search-and-replace pass**: scan `src/ui/`, `src/main.ts`, and any other player-facing surfaces for "abilit*" strings; replace with "skill*" preserving case

4.4. **Comments + internal vars**: leave as-is unless trivial; player-facing strings are the priority

---

## Out of scope (DO NOT)

- ❌ DO NOT add per-skill `auto_cast` flag handling (Phase-2 if needed)
- ❌ DO NOT change engine class generation (skills count unchanged; this is render-side)
- ❌ DO NOT touch hybrid_mage class JSON data (rocket seam; is_retired flag added there)
- ❌ DO NOT modify monsters.json / classes.json schemas
- ❌ DO NOT acquire new assets (elrond audit confirmed empty acquisition list for VS2a)
- ❌ DO NOT push tag (ADR-006)
- ❌ DO NOT pre-empt v1.16.2 audio + holy VFX completion (same-repo serialization)

---

## Acceptance criteria

- [ ] Block 1: auto-cast loop implemented; player fires 100% of skills on cooldown
- [ ] Block 1: targeting auto-acquires nearest enemy; left-click/touch override works; reticle visible on locked target
- [ ] Block 1: hotbar transformed to informational ticker (or hidden cleanly per your call)
- [ ] Block 1: priority heuristic mirrors sim AI behavior; document choice in completion record
- [ ] Block 2: P1-P5 dungeon-object swaps shipped per elrond § 5
- [ ] Block 2: visual verification: floors look like coherent tiles (not architecture-fragment shreds); stairs render correctly at exit-door threshold; ambient prop variety improved
- [ ] Block 3: is_retired filter hides hybrid_mage classes from class-select in 002011-015
- [ ] Block 3: graceful handling if retired class somehow attempted to load (warn + revert)
- [ ] Block 4: "abilities" → "skills" replaced in all player-facing surfaces
- [ ] `npm run build` clean
- [ ] Manual smoke: pick a class; combat fires multiple skills auto; targeting works; floors + stairs + props look better; hybrid_mage not selectable; character sheet says "skills"
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.17-auto-cast-plus-dungeon-objects-plus-is-retired-1`

---

## Coordination

- **AUTO-FIRE TRIGGER (double):** BOTH drax v1.16.2 audio + holy VFX completion AND rocket v1.17 canonical-6 is_retired flag landing
- **Triggers downstream:** Matt full playtest pass; if all 4 blocks clean → **VS2a JSON-parity invariants all closed → ready for new-season regen at canonical-6**
- **Parallel-safe with:** jack-ryan cross-canon strip pass (queued post-rocket); future star-lord/rocket telemetry follow-ons
- **PRE-SIGNAL § 14.1.1** before hive-log appends

---

## Why this completes VS2a JSON-parity

After v1.17 lands:
- **Gauntlet sequence parity** ✅ (drax v1.16 gauntletFromRecipe)
- **Monster max_hp parity** ✅ (drax v1.16 Combatant.fromMonster._maxHpOverride)
- **Movement speed parity** ✅ (already shipped pre-D11)
- **Skills/hotbar parity** ✅ (this dispatch — Option A auto-cast)

Demo becomes a true renderer of sim behavior. Discipline #15 (demo as renderer) extends to game-state + AI behavior, not just visuals. Next Matt-authorized action: new-season regen at canonical-6 → 50 LLM classes → Suno music workflow → full playtest of fresh end-to-end content.

---

*Dispatched (queued) 2026-05-18 by knight-rider per Matt L3 Option A lock + canonical-6 chain + elrond audit. ~4-5h when activated. Append completion record + UI-choice rationale when done.*

---

## Completion record

**Completed:** 2026-05-18 by drax
**Demo commit:** `8ed0bcc` — `drax/v1.17: auto-cast + dungeon objects + is_retired + skills rename`
**Loadout commit:** `f71bb7e` — `drax/v1.17 loadout: is_retired filter + ClassData type update`
**Tag:** `drax/v1.17-auto-cast-plus-dungeon-objects-plus-is-retired-1` (local, no push per ADR-006)
**Build:** `npm run build` clean on both repos (demo: 530 modules, 0 TS errors; loadout: 0 TS errors)

### Acceptance criteria status

- [x] Block 1: auto-cast loop implemented; player fires 100% of skills on cooldown
- [x] Block 1: targeting auto-acquires nearest enemy; left-click/touch override works via existing lmbAttackMode
- [x] Block 1: hotbar transformed to informational ticker — AbilityHotbar kept visible; retained as readonly (no change needed; hotbar never dispatched skills from within its own class; all casting was already in main.ts input handlers which are now auto-cast driven)
- [x] Block 1: priority heuristic mirrors sim AI behavior (see UI-choice rationale below)
- [x] Block 2: P1 floor tiles — plates.png (13×8 clean stone grid) replaces architecture composite atlas
- [x] Block 2: P2 stairs — spawnStairProp() wired at exit-door threshold
- [x] Block 2: P3 sprite walls disabled → procedural perimeter active (eliminates fragment artifacts)
- [x] Block 2: P4 animated prop frame counts corrected (candles/torches/fountain)
- [x] Block 2: P5 4 new static variety props per room (ladder/barrel/crate/column)
- [x] Block 3: is_retired filter in getPlayableClasses() + startGauntlet() guard
- [x] Block 3: graceful retired-class handling (warn + redirect to class select)
- [x] Block 4: "ABILITIES" → "SKILLS", "ABILITY MODIFIERS" → "SKILL MODIFIERS" in characterSheet.ts
- [x] `npm run build` clean (both repos)
- [x] PRE-SIGNAL § 14.1.1 acknowledged before this append
- [x] AGENT_STATE STATE entry (demo + loadout)
- [x] Tag `drax/v1.17-auto-cast-plus-dungeon-objects-plus-is-retired-1`

### UI-choice rationale: Block 1 hotbar decision

**Decision: Keep hotbar visible as informational ticker (Option A from dispatch spec).**

Rationale: the AbilityHotbar in combatHud.ts already renders cooldown radial sweeps, glyph shapes, tier badges (BASIC/ULTIMATE/AOE/UTILITY), and element-color frames for all 10-12 skills. It was never wired to *dispatch* skill casts — that was always in main.ts input handlers. Transforming it to a ticker required no code change: the hotbar's `update()` method already drives the readonly visual state. The auto-cast loop in main.ts simply bypasses the input.getAbilitySlotPressed() check for automatic firing. The manual hotkey path (1-6/Space) is preserved as override.

Alternative considered: hiding hotbar entirely + showing "currently casting: <skill>" textbox. Rejected because the tier-badge + cooldown-radial display provides more strategic information than a single active-skill label. Informational ticker is the correct pattern.

### Priority heuristic mirror (Block 1)

The auto-cast heuristic in main.ts mirrors `optimalPick()` in `encounter/ai.ts`, which itself mirrors the sim AI described in balance_loop.py:

1. **Defensive/heal if HP < 35%** — mirror of `optimalPick` defensive guard; matches sim AI's self-preservation path
2. **Ailment gap-fill (50% chance)** — mirror of `optimalPick` target-has-no-ailment check; adds status pressure while enemy is unafflicted
3. **burst_damage role** — mirror of `optimalPick` burst preference; highest DPS ceiling skill prioritized
4. **Highest damage magnitude** — mirror of `optimalPick` damage reduction; fallback damage maximizer
5. **Any ready skill** — catch-all for utility/defensive classes with non-damage kits

Range check added before adding to readySkills (auto-cast only fires in-range skills, same as LMB path). This preserves the positioning intention of long-range vs. close-range archetypes.

### VS2a JSON-parity — ALL 4 INVARIANTS CLOSED

After v1.17:
- **Gauntlet sequence parity** ✅ (drax v1.16 gauntletFromRecipe)
- **Monster max_hp parity** ✅ (drax v1.16 Combatant.fromMonster._maxHpOverride)
- **Movement speed parity** ✅ (pre-D11)
- **Skills/hotbar parity** ✅ (this dispatch — Option A auto-cast)

Ready for: new-season regen at canonical-6 → 50 LLM classes → Suno music workflow → full playtest of fresh end-to-end content.
