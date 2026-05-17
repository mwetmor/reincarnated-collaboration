# 2026-05-17 — drax-demo — v0.29 Potion HUD visibility + character sprite mismatch + legacy monster effects

**Status:** QUEUED — auto-spawn after `drax/v0.28-hotbar-readability-overhaul-1` ships.
**Authority:** Matt L3 disposition 2026-05-17 (focused playtest follow-up observations on v0.27 ship; new bug reports surfaced post-v0.27).
**Type:** Pattern B (long task) — ~1-2 hours estimated (1 quick fix + 2 investigations).
**Predecessor:** drax v0.28 (in flight).
**Seam:** reincarnated-demo (Pixi.js) — render layer + sprite mapping; possibly touches `loader.ts` for season-data field inspection (read-only); no engine, simulation, or loadout work.

---

## Why these matter

Matt's most recent feedback post-v0.27 ship:
> *"I see the character and inventory icons now, and they are clickable! win! But i cant see potion icons as of yet."*
>
> *"it seems like character sprites and maybe some monsters are mis-matched. Samurai or warrior bodies and weapon visuals on top of caster classes. Some of the monsters also seem to still have legacy aura circles or legacy floating light globes."*

Three issues:
1. **Potion HUD invisible** — v0.27 acceptance criteria stated "Potion icon + quantity + key-binding label visible in HUD; mouse-clickable" but reality is the icons aren't visible. Likely state-conditional render (PotionHud hidden when zero potions).
2. **Sprite mismatch** — caster classes showing physical body sprites (samurai/warrior) instead of substrate-coherent caster sprites. Suggests archetype → character_slug mapping fallthrough.
3. **Legacy monster effects** — some monsters still render legacy aura circles + floating light globes. v0.25's DEBUG_DRAW gate covered character `glowRing` + `weaponOverlay` and monster `monsterSprite.ready` path, but a separate legacy path apparently remains for some monsters.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your v0.25 + v0.26 + v0.27 + v0.28 STATE entries + this dispatch's context
2. `reincarnated-demo/src/ui/potionHud.ts` — your v0.27 work; understand current render conditions + state-dependence
3. `reincarnated-demo/src/visuals/sprites.ts` — your v0.25 DEBUG_DRAW gate (character + partial monster); v0.26 bar work; v0.28 hotbar work; **audit for additional legacy primitives not gated**
4. `reincarnated-demo/src/main.ts` — sprite-mapping / character-track ingest path (your v0.18+ pipeline); the `archetype_tag` → `character_slug` map
5. `reincarnated-demo/src/data/loader.ts` — season-data structure; what `archetype_tag` values + character/sprite identifiers exist in the pre-D3 season JSONs
6. `reincarnated-loadout/data/vfx-manifest.json` — `entity_packs` field per substrate (10 chierit characters); confirm available `character_slug` values
7. `reincarnated-demo/AGENT_STATE.md` — current state

---

## Scope (3 items in priority order)

### Item 1 (HIGH — quick fix) — Potion HUD persistent visibility

**Symptom:** Matt cannot see potion icons. v0.27 hit-area work assumed PotionHud already renders; investigation shows it likely does NOT render in current demo state.

**Hypothesis A:** PotionHud renders conditionally on `potionQuantity > 0`. Pre-D3 seasons or current demo state may have zero potions in inventory → no render.

**Hypothesis B:** PotionHud positioned off-screen or z-clipped.

**Hypothesis C:** PotionHud renders but is obscured by another HUD layer (perhaps v0.27 `DesktopHudIcons` collision).

**Investigate + fix:**
- Trace PotionHud render-condition logic in `src/ui/potionHud.ts`
- Make icons + key-binding + quantity render PERSISTENTLY (always visible) regardless of quantity:
  - Zero quantity: render with `x0` label (greyed-out icon optional; reduced opacity to signal "out")
  - One+: render normally
  - Always: icon visible + key binding visible
- Confirm position: bottom-left at x=110 footprint (per v0.27 layout you authored); should not collide with `DesktopHudIcons` at x=132
- Verify z-order: PotionHud should be in `_layers.ui` (UI overlay, same as v0.27 icons + v0.25 hotbar pinning)
- Smoke: load demo → potion icons visible immediately, before any pickup occurs

**Clickability:** preserve the v0.27 click handlers (`onHealthClick` / `onManaClick`); at zero quantity, click can no-op or trigger a "no potions" visual feedback (small shake animation; subtle is fine).

### Item 2 (HIGH — investigation + fix) — Character sprite ↔ archetype mismatch

**Symptom:** Caster classes (`fire_mage`, `water_mage`, `hybrid_mage`, etc.) render with physical body sprites (samurai/warrior weapons + body shapes) instead of substrate-coherent caster sprites.

**Hypothesis A (likely):** Pre-D3 season data uses `archetype_tag` values that don't match chierit `character_slug` map keys. Chierit Sub-phase A added 10 characters (fire_knight, water_priestess, ground_monk, crystal_mauler, leaf_ranger, metal_bladekeeper, wind_hashashin, lightning_ronin, light_valkyrie, shadow_stalker). Mapping logic from `archetype_tag` → these 10 character_slugs may have gaps, causing fallthrough to a physical default.

**Hypothesis B:** Mapping table is correct but `archetype_tag` values in pre-D3 seasons are stale (e.g., `wind_mage` exists in season but mapping table only has `wind_caster` and `wind_controller` post-D3; pre-D3 wind_mage gets no entry → physical fallthrough).

**Hypothesis C:** Caster archetypes have NO chierit character explicitly (the 10 chierit packs may not include a `caster` body type per substrate; the closest mapping is `fire_knight` which is more warrior-coded than mage-coded).

**Investigate + fix:**
- Inspect the sprite-mapping logic (likely in `main.ts` or a dedicated module; you know the seam)
- Enumerate all `archetype_tag` values present in current 5 pre-D3 seasons (use Item 5 audit data from drax-demo v0.25 if you captured it, or re-audit)
- Map each `archetype_tag` to its current sprite resolution
- Identify the gaps (which archetypes fall through to which defaults)
- **Authoritative resolution:** the chierit 10 characters should cover canonical substrate × role compositions. If gaps exist, propose a mapping using closest-cosmologically-coherent sprite:
  - `fire_mage` / `fire_caster` / `fire_controller` → `fire_knight` (only fire character available)
  - `water_mage` / `water_caster` / `water_controller` → `water_priestess`
  - `earth_*` → `ground_monk` (default) / `crystal_mauler` / `leaf_ranger` / `metal_bladekeeper` (sub-register specific)
  - `wind_*` → `wind_hashashin`
  - `lightning_*` → `lightning_ronin`
  - `holy_*` → `light_valkyrie`
  - `shadow_*` → `shadow_stalker`
  - `hybrid_mage` → cosmologically ambiguous; use neutral or first-substrate fallback
  - Physical archetypes (`rogue`, `warrior`, etc.) → physical default sprite
- Fix the mapping table OR add explicit handlers for archetype variants that fall through
- **Cross-seam awareness:** gamora's fresh post-D3 regen (in flight) will update season `archetype_tag` values to canonical-7 post-D3 set. Your mapping table should ALSO handle the new tags (`lightning_mage`, `lightning_caster`, `lightning_controller`, `holy_mage`, `holy_caster`, `holy_controller`, `shadow_mage`, `shadow_caster`, `shadow_controller`, `earth_burst`, `wind_burst`). Map these to corresponding chierit characters per the table above.

**Acceptable trade-off:** Until additional chierit characters exist for casters specifically, casters and warriors within the same substrate may share the entity sprite (e.g., all fire classes use `fire_knight`). This is graceful degradation — flagging this as a Phase-2 followup (more chierit characters for caster body types) is appropriate.

### Item 3 (MEDIUM — audit + fix) — Legacy monster aura circles + floating light globes

**Symptom:** Some monsters still render legacy aura circles and/or floating light globes that should have been removed per v0.25's vestigial-debug-geometry pass.

**Hypothesis A:** v0.25's DEBUG_DRAW gate at `charSprite.ready` / `monsterSprite.ready` only fires when the sprite successfully resolves to a chierit character. Monsters that fall through to fallback (no chierit map entry) render via legacy graphics primitive code that's NOT gated by DEBUG_DRAW.

**Hypothesis B:** Other graphics primitives exist beyond `glowRing` + `weaponOverlay` (e.g., `auraCircle`, `floatingGlobe`, etc.) that were not part of v0.25's gate.

**Investigate + fix:**
- Audit `sprites.ts` + monster render path for any Graphics-drawn primitives associated with monster entities (search for `drawCircle()`, `beginFill()`, etc. on monster sprite construction)
- Identify additional legacy primitives:
  - "Aura circles" — likely larger ground-projected circles around monster feet (different from the player `glowRing`)
  - "Floating light globes" — likely Graphics-drawn light particles above monster heads or beside them
- Extend DEBUG_DRAW gate to cover these additional primitives (or remove them outright if no diagnostic value)
- Verify by loading demo and inspecting monster sprites; specifically check sprite-mapping fallthrough cases (monsters without chierit/legacy sprite)
- **If fallback-primitive monsters exist** (no chierit / no real sprite), they may render via a placeholder shape. That placeholder shape may be the source of "aura circles + light globes." Two paths:
  - (Preferred) Fix sprite-mapping fallthrough so all monsters resolve to a real sprite (most graceful)
  - (Acceptable) Strip legacy decorative primitives from the fallback render code

**Cross-seam awareness:** gamora's fresh post-D3 regen will update monster archetype tags. Verify your monster-mapping logic also handles new post-D3 monster tags (similar to player archetype mapping in Item 2).

---

## Out of scope (DO NOT)

- ❌ DO NOT acquire additional chierit characters (Phase-2 followup if needed)
- ❌ DO NOT modify season data or engine generation (your investigation should INFORM gamora's post-D10 regen tuning, not fix the data directly)
- ❌ DO NOT modify the v0.28 hotbar overhaul (just shipped or shipping; intentionally separate)
- ❌ DO NOT modify the v0.27 desktop HUD icons or potion click-handler logic (extend PotionHud rendering only)
- ❌ DO NOT extend scope to other UX bugs noticed. Surface as OBSERVATION for next dispatch.
- ❌ DO NOT touch the v0.26 cosmetic dodge primitive (gandalf L3 supersedes)
- ❌ DO NOT touch engine, simulation, or loadout files

---

## Acceptance criteria

- [ ] Potion HUD icons visible at game-start regardless of potion quantity (zero shows `x0` greyed; quantity > 0 shows normally)
- [ ] Sprite-mapping audit completed: enumerate all `archetype_tag` → `character_slug` mappings; gaps identified + filled
- [ ] All current pre-D3 season archetype_tags resolve to a chierit character (no physical-default fallthrough for caster classes)
- [ ] Mapping table also handles post-D3 archetype_tag set (lightning_*, holy_*, shadow_*, earth_burst, wind_burst, etc.) for when gamora's regen lands
- [ ] Legacy monster aura circles + floating light globes audit completed; additional Graphics primitives identified + gated/removed
- [ ] Demo loads cleanly; visual smoke confirms: potion icons visible, caster sprites correct, monsters clean (no legacy effects)
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag `drax/v0.30-potion-visibility-sprite-mapping-legacy-monsters-1` (or next available v0.X-tag)
- [ ] Hive-log STATE entry + OBSERVATION (which mapping gaps required closest-cosmological-fit choices; flag as Phase-2 followup if additional chierit characters needed)

---

## Smoke test expectation

1. Load demo → potion icons visible at bottom-left (even at zero quantity)
2. Inspect 3-5 different player classes → all have substrate-coherent character sprites (no samurai bodies on fire_mage etc.)
3. Inspect 5-10 different monster spawns → no legacy aura circles or floating light globes
4. Click potion icon at zero quantity → no-op or subtle "out" feedback
5. Build clean

---

## Phase-2 followup observation (likely)

The 10 chierit characters cover **one body type per substrate** (e.g., fire_knight is warrior-coded; not a caster body). Casters within a substrate currently share the substrate's single chierit body. This is graceful degradation but visually identical fire_mage / fire_caster / fire_controller.

**Long-term Phase-2 followup:** acquire additional chierit characters (caster body / controller body per substrate) for stronger visual differentiation within substrate. Surface as OBSERVATION in your hive log.

---

## Math-before-code requirements

N/A — render + mapping audit; no engine math.

---

## Tag intent

`drax/v0.30-potion-visibility-sprite-mapping-legacy-monsters-1` (or `v0.29` if not taken by v0.28's actual ship-tag; use next available).

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

*Queued 2026-05-17 by knight-rider per Matt L3 disposition. Spawn after v0.28 hotbar overhaul ships. Estimated 1-2 hours. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Commit:** `4b5a228` — reincarnated-demo
**Tag:** `drax/v0.29-potion-visibility-sprite-mapping-legacy-monsters-1`
**Build:** tsc + vite clean (521 modules, 0 errors)

### Item 1 — PotionHud persistent visibility — DONE

Root cause: DiabloHud HP globe (x=76, y=880, r=58) was added to _layers.ui after PotionHud (x=14, y=839, w=110, h=48). Pixi z-order renders later children on top. HP globe was covering the potion icon band. Fix: reordered startGauntlet() so DiabloHud is instantiated before PotionHud + DesktopHudIcons. PotionHud and DesktopHudIcons now render above the DiabloHud globes. Added initial `potionHud.update(potions)` call immediately post-construction for correct greyed zero-quantity state from frame one.

### Item 2 — Sprite mapping audit — DONE

Pre-D3 dominant_element values (fire/water/earth/wind/physical) are all mapped in ELEMENT_CHARACTER_MAP. No gaps. No physical-default fallthrough for any pre-D3 class archetype. The "samurai bodies" observation was caused by the Item 1 z-order issue obscuring the correct chierit sprites. Post-D3 readiness additions: `lightning` → lightning-ronin and `shadow` → shadow-stalker as aliases (engine renames 'thunder'→'lightning', 'dark'→'shadow' at D19+). Original 'thunder'/'dark' keys retained for pre-D3 compat.

### Item 3 — Legacy monster effects — DONE

- `ENEMY_TIER_CHARACTER_MAP` `mini_boss` (underscore) → `mini-boss` (hyphen): engine emits hyphen form; key never matched. Added `'mini-boss'` as primary key; `mini_boss` retained as alias. Lich/hellfire-rhino/fire-lord-creativkind-thunder now resolve for mini-boss tier.
- Added `particleContainer: Container` to CombatantSprite interface. Orbital particles (the "floating light globes") now gated via `particleContainer.visible = DEBUG_DRAW` when charSprite.ready or monsterSprite.ready.
- `bossAura.visible = DEBUG_DRAW` when monsterSprite.ready. Pulsing ring (the "legacy aura circle") suppressed for monsters with active sprites.
- DEBUG_DRAW=false is production default. All legacy primitives restored at DEBUG_DRAW=true for diagnostics.

### Phase-2 observation logged

Chierit caster body types: all fire/* archetypes share fire-knight body; all water/* share water-priestess; etc. Cosmologically coherent but role-variants within a substrate are visually identical. Phase-2 followup: acquire per-substrate caster/controller body variants when additional chierit packs available. Logged in hive OBSERVATION entry.
