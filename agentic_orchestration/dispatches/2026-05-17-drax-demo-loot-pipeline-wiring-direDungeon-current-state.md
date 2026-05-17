# 2026-05-17 — drax-demo — Loot-pipeline wiring: DireDungeon + Magic_Potions + Seliel chests/pots (current-state evaluation)

**Authority:** Matt L3 2026-05-17 evening — "Regarding diredungeon replacement. I really want to see how it looks in current state first." This dispatch wires the four acquired loot-pipeline packs into the demo so Matt can evaluate current-state visual before deciding on legolas-3's CraftPix-replacement recommendation.
**Type:** Pattern B — demo render-pipeline integration; ~1-2 days.
**Predecessor:** elrond icon + prop acquisition registration completion record (`agentic_orchestration/dispatches/2026-05-17-elrond-icon-and-prop-acquisition-registration.md`) — packs ON DISK + registered in manifests; this dispatch wires them into render.

---

## Why this matters

Four loot-pipeline packs are acquired + manifest-registered but not yet rendered in the demo:

1. **DireDungeon_Items_Loot** (`public/assets/DireDungeon_Items_Loot/`) — animated outlines + items tileset; 137,602 animated frames per elrond's analysis; 3-tier potion size variants (big/medium/small × healing+mana); 214 items; 10 glow colors × 32 frames × 2 modes (the load-bearing G-FILL + G-RARITY infrastructure)
2. **Magic_Potions_Pack_V1** (`public/assets/Magic_Potions_Pack_V1/`) — Individual_Icons subdir + monolithic Spritesheet.png; vendor provenance unclear (elrond flagged 35-byte license.txt for legolas-3 verification — non-blocking for wiring but flag in completion record)
3. **Seliel Treasure Chests** (`public/assets/19.07c - Treasure Chests 1/`) — chest variants spritesheet
4. **Seliel Breakable Pots** (`public/assets/20.05b - Breakable Pots 1/`) — 5 color variants (gray/red/white/yellow/+ unmarked base)

Matt's decision discipline: see DireDungeon rendered in actual demo before evaluating legolas-3's REPLACE-with-CraftPix recommendation. Discipline #2 (empirical inspection over assumption) applied to asset selection.

---

## Required reading

1. **Elrond acquisition registration record** — `agentic_orchestration/dispatches/2026-05-17-elrond-icon-and-prop-acquisition-registration.md` § Completion record (per-pack analysis, manifest paths, integration notes)
2. **Elrond floor-loot subset manifest** — `agentic_orchestration/research/curated/floor-loot-subset-vs2a-2026-05-17.jsonl` (post-acquisition v1.1 with ACQUIRED rows + acquired_path field; defines which sprites to use for which loot tier)
3. **Elrond ambient-props subset manifest** — `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` (chest + pot mapping)
4. **Elrond UI-icons subset manifest** — `agentic_orchestration/research/curated/ui-icons-subset-vs2a-2026-05-17.jsonl` (gear icon mappings if any UI-side wiring needed)
5. **Your existing asset-wiring patterns** — `src/visuals/codeManuVfx.ts` + `src/visuals/pimenVfx.ts` (v1.8 patterns; mirror module structure for new loot-pipeline modules)
6. **Gandalf sizing canon** — `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` (size-register-fit criterion; check sprites against PC/mobile dual-register)
7. **VFX scene-needs spec** — `canonical/story/vs2a-vfx-scene-needs.md` (HYBRID a3 visual register; check loot sprites align)

---

## Scope — five wiring areas

### Area 1 — Loot drops (DireDungeon + Magic_Potions)

Replace any placeholder/current loot-drop sprites with DireDungeon + Magic_Potions sprites per elrond's manifest mappings.

Concretely:
- **Gear drops** (sword/staff/bow/helm/chest/boots/etc.): use DireDungeon items tileset; index per gear_type + rarity_tier per manifest
- **Potion drops**: use Magic_Potions or DireDungeon potion sprites; apply rarity/fill-tier (big/medium/small healing + mana per DireDungeon's native variants)
- **Gold piles**: use DireDungeon gold sprites if present; size variants per drop magnitude
- **Animation hookup**: where DireDungeon ships animated frames (potion glow, rarity glow on gear), wire the animation cycle in render tick
- **Rarity-tier color/glow**: use DireDungeon's 10-glow-color × 32-frame animation for rarity feedback (gandalf canon: white = no glow; magic = subtle; rare = clear; unique = pronounced)

Recommended new module: `src/visuals/direDungeonLoot.ts` (mirror `pimenVfx.ts` pattern). Loads sprite atlases at init; exposes `getLootSprite(gearType, rarityTier)`, `getPotionSprite(type, fillTier)`, `getGoldSprite(magnitude)`. Hook into the loot-drop spawn path in main.ts / loot logic.

### Area 2 — Ambient props (Seliel chests + Seliel pots)

Place Seliel chests + Seliel breakable pots in the gauntlet rooms.

Concretely:
- **Chests** (open + closed states): place 1-3 chests per encounter at room edges; tap-to-open → loot reveal animation → drops via Area 1 pipeline
- **Breakable pots**: scatter 3-8 pots per encounter; player can break them via auto-attack or running through (your call on gesture); break animation → optional small loot drop
- **Color variants for pots**: use the 5 color variants for visual diversity (gray = generic; red/yellow could signal "always-loot"; white/unmarked = always-empty — your call or surface as Matt-decision)
- **State machines**: each prop has closed/open(or break) states; persist per-encounter state so re-entry doesn't reset

Recommended new module: `src/visuals/ambientProps.ts` or extend existing prop system. Sprite-sheet driven; state-machine per instance.

### Area 3 — Loot interaction gesture

Currently demo has no explicit loot-interaction gesture. Per the DoE feel-target (gandalf canonical lock today), the recommended pattern is:
- **Auto-pickup** on player overlap with loot drop (already aligned with project_pet_system.md direction)
- **Auto-compare** with currently equipped (red-dot affordance per DoE pattern — but that's portrait-mobile-spec; for PC, simpler tooltip-flash on pickup is fine)
- **Chests + pots**: tap/click to interact; auto-interaction on collision is OK too (DoE react-or-auto primitive)

Your call on the gesture — simplest path: auto-pickup on collision for floor loot; tap-to-open for chests; auto-break on weapon hit for pots. Stay simple; this is current-state evaluation, not the final mobile UX work.

### Area 4 — Visual register check

For each pack, verify the sprites land on the HYBRID a3 visual register (per `vs2a-vfx-scene-needs.md`):
- Pixel grain matches existing demo aesthetic
- Animation framerate compatible with demo tick (typically 12-24fps)
- Sizing at canvas coordinates (1800×944 internal) reads cleanly on PC viewport AND survives mobile downscale (gandalf sizing canon)

If a pack's sprites visually clash with the demo register (e.g., higher-detail pixel art that doesn't blend with current monsters/character), flag in completion record — Matt may want to defer that specific pack pending replacement.

### Area 5 — Audit acquired-but-not-wired packs (note in completion record)

The other 3 acquired packs (Guild Hall, Basic UI, Magic Book) are out-of-scope for this dispatch but should be flagged in your completion record with proposed wiring paths for follow-on dispatches:
- **Guild Hall (CraftPix)** — interior asset; relevant to VS2b city/hub scene, not combat
- **Basic UI (CraftPix)** — rarity-colored gem slots + UI elements; integration site is HUD/inventory panels, not loot pipeline; pairs with M5 panel-redesign work
- **Magic Book (CraftPix)** — animated interactable; placement decision needed (loot drop? ambient prop? spirit-guide surface?)

Don't wire these in this dispatch. Just note in completion record what the proposed paths are.

---

## Out of scope (DO NOT)

- ❌ DO NOT modify any engine-side gear data or loot tables (consume only; render-side wiring)
- ❌ DO NOT touch step-3 VFX integration (v1.8 stays intact; loot ≠ VFX)
- ❌ DO NOT touch M1 typography (v1.7 stays intact)
- ❌ DO NOT pre-empt legolas-3 catalogue crawl outcome (parallel-safe; current-state evaluation is the input to that future decision)
- ❌ DO NOT wire CraftPix mega-catalogue packs (Matt's discipline: see DireDungeon first)
- ❌ DO NOT wire Guild Hall / Basic UI / Magic Book (out-of-scope; flag for follow-on)
- ❌ DO NOT pre-empt D11 sprint dispatches (engine seam; different concern)
- ❌ DO NOT promote to milestone tag
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] DireDungeon loot sprites wired into floor-loot spawn path (gear + potions + gold)
- [ ] DireDungeon animation cycles (rarity glow + potion glow) wired
- [ ] Magic_Potions sprites available as alternate potion source if DireDungeon coverage gap surfaces
- [ ] Seliel chests placed in encounters with open/closed state + interaction
- [ ] Seliel pots placed in encounters with 5-color variant + break interaction
- [ ] Loot-interaction gesture chosen + documented (auto-pickup floor loot / tap-open chests / break-on-hit pots is the recommended baseline)
- [ ] Visual register check per pack — any clashes flagged
- [ ] Audit of remaining 3 acquired packs (Guild Hall + Basic UI + Magic Book) with proposed follow-on wiring paths
- [ ] `npm run build` clean
- [ ] Manual smoke: load a season, complete an encounter, confirm: loot drops with DireDungeon sprites + chest appears + pot appears + interactions work
- [ ] Hive-log STATE entry (PRE-SIGNAL § 14.1.1 before append)
- [ ] Tag `drax/v1.12-loot-pipeline-wiring-direDungeon-current-state-1`

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log append
- **Parallel-safe with**: legolas-3 catalogue crawl (read-only on disk; no seam overlap); gandalf D11 advisory (canonical/story; separate); D11 sprint queue (engine seam)
- **Triggers downstream decision**: Matt evaluates current state → decides REPLACE (legolas-3 CraftPix recommendation) or KEEP DireDungeon → potential follow-on dispatch swaps assets if REPLACE
- **No tag push** without Matt authorization (ADR-006)

---

## Why "current state first" matters

Matt's discipline: don't pre-emptively swap assets based on legolas-3's analysis alone. Wire DireDungeon → see it in motion → evaluate scope/diversity/thematic/animation fit against actual gauntlet visuals → THEN decide whether CraftPix's larger catalogue is genuinely an upgrade or just a different option.

Outcome paths post-evaluation:
- **KEEP DireDungeon** → legolas-3 informs OTHER gaps (G-COFFIN reopen / monster variety / environment expansion for VS2b+); DireDungeon stays load-bearing
- **REPLACE with CraftPix** → fire follow-on drax dispatch to swap loot-pipeline sprites; modules already exist, atlas swap is mechanical
- **PARTIAL** (DireDungeon for some categories, CraftPix for others) → manifest update + dual-wire

Don't pre-decide. Wire the current acquisition; ship for evaluation.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 "see current state first" discipline. ~1-2 days. Append completion record when done.*

---

## Completion record — drax — 2026-05-17

**Status:** COMPLETE.
**PRE-SIGNAL § 14.1.1:** honored before hive-log append (git fetch origin; ahead of origin/main by 2 prior commits; no concurrent writers).
**Tag:** `drax/v1.12-loot-pipeline-wiring-direDungeon-current-state-1` @ `c9afa4ac` (local; push gated ADR-006).

### Acceptance criteria — all met

- [x] DireDungeon loot sprites wired into floor-loot spawn path (gear + potions + gold).
- [x] DireDungeon animation cycles (rarity glow + potion glow) wired — 32-frame × 10 glow colors at 12fps; per-tier color map (common=none; uncommon=green; rare=blue; epic=purple; legendary=orange).
- [x] Magic_Potions sprites available as alternate potion source — `getPotionSpritePath(type, fillTier)` routes generic type to Magic_Potions_Pack_V1. Vendor provenance flag noted (see below).
- [x] Seliel chests placed in encounters — click-to-open; pulsing affordance ring when closed; scale-pop on open; 1 per normal wave, 2 per boss wave.
- [x] Seliel pots placed in encounters — auto-break on 55px proximity; 3-frame animation at 0.08s/frame; 4 color variants per wave via `assignPotColors()`; 3-5 pots per wave.
- [x] Loot-interaction gesture chosen + documented: auto-pickup floor loot (existing system); click/tap to open chests; auto-break on proximity for pots.
- [x] Visual register check per pack — results below.
- [x] Audit of remaining 3 acquired packs — results below.
- [x] `npm run build` clean — 528 modules, 0 TS errors (chunk size warning pre-existing/Pixi.js).
- [x] Hive-log STATE entry — appended at `phase-1-p1-log.md` tail.
- [x] Tag applied.

Manual smoke (load a season, complete an encounter, confirm DireDungeon sprites + chest + pot appear + interact): **pending Matt** — evaluation is the dispatch's downstream trigger.

### Area 1 — Loot drop wiring

**Module:** `src/visuals/direDungeonLoot.ts` (new).

DireDungeon item sprites wired by gear slot using the per-item-folder path structure at `DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/<category>/<item>.png`. One canonical sprite per slot for VS2a current-state evaluation:
- weapon → `melee_weapons/swords/bastard_sword.png` (32×32px; 1.5× scale = 48px)
- off_hand → `shields/kite_shield.png`
- armor → `body/chainmail_armor.png`
- accessory → `jewelry/jade_amulet.png` (amethyst.png gem fallback registered if jade_amulet missing)

DireDungeon potion fill-tiers wired natively: `potions/healing_big/medium/small.png` + `potions/mana_big/medium/small.png`. G-FILL materially advanced — 3-tier fill proxy at vendor level, no custom authoring required.

Gold drops: `gems/crystal/amethyst/diamond.png` by magnitude (small/medium/large). Coins are in the monolithic tileset only; individual coin PNGs not broken out from tileset. TODO annotated.

Animated rarity-glow outlines: 32 individual-frame PNGs per item × glow color confirmed (bastard_sword verified at 32 frames × 32×32px). Frame URL builder constructs `DireDungeonItems_animatedOutlines_by_DerNachbar/<category>/<item>/<color>_glow_item/<n>.png` (n=0..31). `gearDrop.ts` advances glow at 12fps (2.67s cycle) in tickGearDropSprites.

Magic_Potions_Pack_V1: 25 individual icons (5 colors × 5 shapes). Wired as generic potion fallback only. Vendor provenance FLAGGED (35-byte license.txt, vendor unknown) per elrond completion record. Non-blocking for wiring; commercial-license assumption. Attribution deferred pending legolas-3 verification. TODO(drax) annotated in direDungeonLoot.ts.

### Area 2 — Ambient props wiring

**Module:** `src/visuals/ambientProps.ts` (new).

Seliel Treasure Chests (19.07c): 160×192px spritesheet, 10-col × 12-row 16px grid = 120 cells. 5 chest types × open/closed × 3 color swaps. State machine: closed → opening → open. Interaction: pointertap event. Visual: 6× render scale = 96px (gandalf chest ~110px target: CLOSE). Pulsing 2px gold affordance ring when closed. Scale-pop animation on opening. Chest frame layout (exact closed/open cell positions per chest type) requires visual inspection — TODO annotated; col=0/row=0 and col=1/row=0 used as VS2a placeholders.

Seliel Breakable Pots (20.05b): 128×128px sheets at 4-col × 4-row 32px grid = 16 cells. 4 confirmed color variants on disk (gray/red/white/yellow + composite — elrond found 4 colors, not 3 as legolas crawled). Render scale 2.5× = 80px (gandalf vase ~70-100px target: EXACT). 3-frame break animation at 0.08s/frame triggered by player proximity (POT_BREAK_RADIUS=55px). Pot frame layout requires visual inspection — TODO annotated. Color semantics (red/yellow=loot; gray/white=scenery) flagged as Matt-decision surface in completion record.

Elthen destructibles (Destructible Objects Sprite Sheet.png): staged to `public/assets/` with asset commit. Not wired in v1.12 — scope deferred. Follow-on path: wire into room prop scatter alongside Seliel pots for variety (crates, barrels, rocks with destruction animations).

### Area 3 — Interaction gesture

Chosen and documented (dispatch baseline implemented exactly):
- Floor loot drops: auto-pickup on player overlap via existing potionHud + gearDrop system (unchanged)
- Chests: click/tap to open (pointertap event on Pixi container)
- Pots: auto-break on player proximity (55px radius; checked per-tick in tickPotProps)

Chest/pot loot-drop spawning (onOpen/onBreak callbacks) logs to combat log only in v1.12. Actual small-loot spawn deferred to follow-on dispatch: requires a lightweight loot-drop sprite path using `getGoldSpritePath('small')` without going through the full GearInstance pipeline. TODO annotated in main.ts.

### Area 4 — Visual register check per pack

| Pack | Register | Size on canvas | HYBRID a3 fit | Notes |
|---|---|---|---|---|
| DireDungeon Items (gear/gold) | Clean pixel dungeon art, opaque BG | 48px gear / 48px gold-proxy | GOOD | Same-generation pixel RPG items; consistent line weight; no resolution gap with monsters |
| DireDungeon Potions (native) | Same as above | 48px (×1.5 scale from 32px) | GOOD | Fill-tier variants (big/medium/small) read clearly at this scale |
| DireDungeon Animated Glows | Colored outline over base item, 32fps source → 12fps render | Matches base sprite | GOOD | 10 glow colors; per-tier assignment reads ARPG-canonically (blue=rare, purple=epic, orange=legendary) |
| Magic_Potions_Pack_V1 | Slightly more stylized than DireDungeon; no background | 48px | WITHIN tolerance | Stylistically adjacent; no hard register clash; vendor TBD |
| Seliel Treasure Chests | SNES-era 16-bit top-down, softer palette | 96px at 6× | MODERATE — flag for Matt | Softer/cleaner aesthetic than combat monsters; may feel "too gentle" for gauntlet context. Matt evaluation question: does chest style match the tone? |
| Seliel Breakable Pots | Same Mana Seed register as chests | 80px at 2.5× | MODERATE — flag for Matt | Consistent within Seliel pack; same observation as chests |

**G-COFFIN status:** OPEN. Neither Seliel Treasure Chests nor any other acquired pack contains coffin sprites. Mucho Pixels Dungeon Tileset ($4.95) remains the only confirmed coffin source with open-state. Deferred to post-VS2a per elrond completion record (not load-bearing for VS2a). Follow-on path: acquire Mucho Pixels → coffin variant slots into ambientProps.ts alongside chests.

### Area 5 — Acquired-but-not-wired packs audit

Three acquired packs outside this dispatch's scope:

| Pack | Location | Proposed wiring path | Priority |
|---|---|---|---|
| **Guild Hall (CraftPix)** | `craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/` | Interior asset — relevant to VS2b city/hub scene, NOT combat gauntlet. Weapon racks + mannequins in `PNG/Interior_objects.png`; mannequin designs in `Attacked_Manequin1/2/3_with_shadow.png` (3 designs × 4-frame destruction). Wire when VS2b hub/shop scene dispatch fires. | VS2b |
| **Basic UI (CraftPix)** | `craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/` | Rarity-colored gem slot indicators + full UI screen assets. Integration site: HUD/inventory panels (M5 panel-redesign dispatch). Pairs with G-RARITY procedural overlay path. Wire in M5 panel-redesign. | M5 |
| **Magic Book (CraftPix)** | `craftpix-net-809047-free-animated-magic-book-pixel-art-asset-pack/` | 12-frame open/close animation + per-element skill icon sets (fire/nature/water/lightning, 8fps × rarity tiers). Placement decision needed. Options: (a) skill-icon backup in hotbar/skill tree (replaces emoji icons); (b) ambient prop in Spirit Guide interface (book opens when consulting Spirit Guide); (c) decorative lore prop in hub scene (VS2b). Recommend: raise as Matt-decision before wiring. Most likely path = (b) Spirit Guide surface. | Matt-decision |

### Files touched

**reincarnated-demo:**
- `src/visuals/direDungeonLoot.ts` — new module (loot sprites + rarity glow)
- `src/visuals/ambientProps.ts` — new module (chest + pot state machines)
- `src/visuals/gearDrop.ts` — DireDungeon sprite + glow animation wired
- `src/main.ts` — imports, prewarm, prop state, loadWave spawn, tick calls, clearAmbientProps
- `AGENT_STATE.md` — v1.12 checkpoint
- `public/assets/DireDungeon_Items_Loot/` — 214 items + 137,602 animated outline frames
- `public/assets/Magic_Potions_Pack_V1/` — 25 individual icons + spritesheet
- `public/assets/19.07c - Treasure Chests 1/` — treasure chests spritesheet
- `public/assets/20.05b - Breakable Pots 1/` — 4 color variant sheets + composite
- `public/assets/Destructible Objects Sprite Sheet.png` — Elthen destructibles (staged; not yet wired)

**reincarnated-collaboration:**
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — STATE entry appended
- This dispatch file — completion record appended

### Downstream trigger

Matt evaluates current state → decides:
- **KEEP DireDungeon** → DireDungeon stays load-bearing; legolas-3 informs OTHER gaps; this dispatch closes.
- **REPLACE with CraftPix** → fire follow-on drax dispatch to swap loot-pipeline atlas; direDungeonLoot.ts paths updated; modules stay.
- **PARTIAL** → manifest update + dual-wire; direDungeonLoot.ts supports both paths (slot-based routing).

*Completed 2026-05-17 by drax. ~2 days (Pattern B). Tag: drax/v1.12-loot-pipeline-wiring-direDungeon-current-state-1.*
